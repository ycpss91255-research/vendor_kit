//! `remove`／`uninstall` 收回初始檔（ADR-0003；04 收回插入的行、remove 與 uninstall 的收回範圍）。
//!
//! - 初始檔本身一律保留，不刪、不覆蓋（02 不變量第 1 條）；這裡只決定 append 進既有檔的行收不收回。
//!   根 `justfile` 的 `import`、根 `.dockerignore` 的四行與工具 append 的行都是一般的 `[[file]]` 紀錄，
//!   規則相同，不另外分。
//! - 輸入是一份或多份逐檔紀錄（[`Source`]：哪一份紀錄檔、它的 [`Metadata`]），加上呼叫端注入的讀檔函式。
//!   `remove <repo>` 傳那個工具的一份；`uninstall` 傳每個工具的與 `baseline/.vendor_kit.toml`。
//!   紀錄缺失或損壞（VK0013）在 [`Metadata::load`] 就擋下，不會進到這裡。紀錄以外的檔一律不看。
//! - 判定（[`plan`]）逐筆紀錄：
//!   - `appended` 且有 `lines`：先比整檔 hash（CRLF→LF 正規化，[`FileHash::of`]）。紀錄沒有 hash、
//!     hash 與目前不同、檔不在，這筆的每一行都只列不刪；hash 相符才逐行數原文命中次數，恰好一處的行
//!     列進要問的收回，零處或多處的行只列不刪。不因其中一行對不上就整批放棄。
//!   - 其他 state 且沒有 `lines`：沒有要收回的行，檔保留（[`Verdict::Keep`]）。
//!   - 契約沒寫到的組合（非 `appended` 卻有 `lines`、`appended` 卻沒有 `lines`）：不收回、不自己補規則，
//!     標成 [`Verdict::Gap`] 交呼叫端。
//! - 原文比對只把 CRLF 與 LF 視為相同，其他（含行首行尾空白）都照原樣；行號從 1 起算。
//! - 同一個檔出現在好幾筆紀錄裡時，每個檔只讀一次，全部紀錄都以同一份寫入前的內容判定；要收回的行
//!   合併成一個 [`Edit`]，刪掉整行（含行尾），其他位元組（別行的 CRLF、最後一行沒有換行）原樣保留。
//! - 這裡不詢問：每次呼叫先問完所有問題、全部同意才寫入（04 共同選項；計畫矛盾 C8 以 04 為準），
//!   所以 [`Plan::questions`] 收齊這次全部的問題，一份紀錄的一個檔一題，由呼叫端經 `prompt` 一次問完；
//!   [`Plan::edits`] 是全部同意時要寫的內容。帶 `-y` 時不問，但改動仍由呼叫端印到 stdout。
//! - 這裡不寫檔：寫回、刪紀錄檔、對仍保留的紀錄呼叫 [`Metadata::record_write`]`(path, before, after)`
//!   都由呼叫端做；[`Edit`] 帶著判定用的 `before` 與收回後的 `after`。
//! - 只列不刪的每一行對應一則 VK0061（[`Unretracted::message`]），`<text>` 是原文、`<line_numbers>` 是
//!   [`Unretracted::matches`]，沒有相符行時印 `none`。這裡不印診斷，也不決定保留清單要列哪些 state：
//!   每筆紀錄的 state 都在 [`Plan::records`]，由呼叫端決定。

use std::collections::{BTreeMap, BTreeSet};
use std::fmt;
use std::io;

use messages::Message;
use metadata::{FileHash, FileRecord, Metadata, State};

// ---------------------------------------------------------------------------
// 輸入

/// 一份逐檔紀錄檔屬於誰。
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Owner {
    /// `baseline/<repo>.toml`。
    Tool(String),
    /// `baseline/.vendor_kit.toml`：不屬於任何工具的紀錄。
    Vk,
}

impl fmt::Display for Owner {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Owner::Tool(repo) => f.write_str(repo),
            Owner::Vk => f.write_str(".vendor_kit"),
        }
    }
}

/// 要收回的一份逐檔紀錄。
#[derive(Debug, Clone, Copy)]
pub struct Source<'a> {
    pub owner: &'a Owner,
    pub metadata: &'a Metadata,
}

// ---------------------------------------------------------------------------
// 輸出

/// 檔裡的一行：原文（不含行尾）與行號（從 1 起算）。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Line {
    pub text: String,
    pub number: usize,
}

/// 要問的一題：同意後收回 `path` 裡這份紀錄的 `lines`。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Question {
    pub owner: Owner,
    pub path: String,
    pub lines: Vec<Line>,
}

/// 只列不刪的原因（都對應 VK0061）。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Reason {
    /// 檔不在：沒有目前內容，hash 不可能相符。
    FileMissing,
    /// 舊紀錄沒有整檔 hash，歸因不確定。
    NoHash,
    /// 整檔 hash 與 VK 上次寫入後記的不同。
    HashMismatch,
    /// hash 相符，但原文不是恰好一處。
    NotUnique,
}

impl Reason {
    pub const fn as_str(self) -> &'static str {
        match self {
            Reason::FileMissing => "file missing",
            Reason::NoHash => "no recorded hash",
            Reason::HashMismatch => "hash differs",
            Reason::NotUnique => "not exactly one match",
        }
    }
}

impl fmt::Display for Reason {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

/// 不收回的一行。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Unretracted {
    pub owner: Owner,
    /// 填 `<file>`。
    pub path: String,
    /// 填 `<text>`：紀錄裡的原文。
    pub text: String,
    /// 填 `<line_numbers>`：目前所有相符的行號，從 1 起算；空的時候印 `none`。
    pub matches: Vec<usize>,
    pub reason: Reason,
}

impl Unretracted {
    /// 對應的訊息表條目。
    pub fn message(&self) -> &'static Message {
        &messages::VK0061
    }
}

/// 全部同意時對一個檔的改動。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Edit {
    pub path: String,
    /// 判定用的寫入前內容。
    pub before: Vec<u8>,
    /// 收回後的內容。
    pub after: Vec<u8>,
    /// 刪掉的行號（`before` 裡的，從 1 起算，遞增、不重複）。
    pub removed: Vec<usize>,
}

/// 契約沒寫到的紀錄組合。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Gap {
    /// state 不是 `appended`，卻有 `lines`。
    LinesInOtherState,
    /// state 是 `appended`，卻沒有 `lines`。
    AppendedWithoutLines,
}

/// 一筆紀錄的判定。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Verdict {
    /// 沒有插入行：檔保留，沒有要收回的。
    Keep,
    /// append 型：插入行逐行判定，結果在 [`Plan::questions`] 與 [`Plan::unretracted`]。
    Judged,
    /// 契約沒寫到：不收回、不判定。
    Gap(Gap),
}

/// 一筆紀錄。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RecordPlan {
    pub owner: Owner,
    pub path: String,
    pub state: State,
    pub verdict: Verdict,
}

/// 這次收回的動作清單與要問的問題。
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Plan {
    /// 每筆紀錄，順序同輸入。
    pub records: Vec<RecordPlan>,
    /// 這次全部要問的問題，順序同輸入。
    pub questions: Vec<Question>,
    /// 只列不刪的行，順序同輸入。
    pub unretracted: Vec<Unretracted>,
    /// 全部同意時要寫的檔，依路徑排序。
    pub edits: Vec<Edit>,
}

// ---------------------------------------------------------------------------
// 判定

/// 依 `sources` 的逐檔紀錄算出收回的動作與問題。
///
/// `read(path)` 回傳 repo 相對路徑 `path` 目前的內容，檔不在回 `Ok(None)`；每個路徑只讀一次。
pub fn plan<F>(sources: &[Source<'_>], mut read: F) -> Result<Plan, ReadError>
where
    F: FnMut(&str) -> io::Result<Option<Vec<u8>>>,
{
    let mut contents: BTreeMap<String, Option<Vec<u8>>> = BTreeMap::new();
    let mut removals: BTreeMap<String, BTreeSet<usize>> = BTreeMap::new();
    let mut plan = Plan::default();

    for source in sources {
        for record in source.metadata.files() {
            let verdict = verdict(record);
            plan.records.push(RecordPlan {
                owner: source.owner.clone(),
                path: record.path.clone(),
                state: record.state,
                verdict,
            });
            if verdict != Verdict::Judged {
                continue;
            }
            if !contents.contains_key(&record.path) {
                let current = read(&record.path).map_err(|source| ReadError {
                    path: record.path.clone(),
                    source,
                })?;
                contents.insert(record.path.clone(), current);
            }
            let current = contents.get(&record.path).and_then(Option::as_deref);
            let retract = judge(source.owner, record, current, &mut plan.unretracted);
            if !retract.is_empty() {
                removals
                    .entry(record.path.clone())
                    .or_default()
                    .extend(retract.iter().map(|l| l.number));
                plan.questions.push(Question {
                    owner: source.owner.clone(),
                    path: record.path.clone(),
                    lines: retract,
                });
            }
        }
    }

    for (path, removed) in removals {
        let before = contents
            .get(&path)
            .and_then(Option::as_deref)
            .unwrap_or_default();
        plan.edits.push(Edit {
            after: remove_lines(before, &removed),
            before: before.to_vec(),
            removed: removed.into_iter().collect(),
            path,
        });
    }
    Ok(plan)
}

fn verdict(record: &FileRecord) -> Verdict {
    match (record.state, record.lines.is_empty()) {
        (State::Appended, false) => Verdict::Judged,
        (State::Appended, true) => Verdict::Gap(Gap::AppendedWithoutLines),
        (_, false) => Verdict::Gap(Gap::LinesInOtherState),
        (_, true) => Verdict::Keep,
    }
}

/// 判定一筆 append 型紀錄：回傳要問的行，只列不刪的行推進 `unretracted`。
fn judge(
    owner: &Owner,
    record: &FileRecord,
    current: Option<&[u8]>,
    unretracted: &mut Vec<Unretracted>,
) -> Vec<Line> {
    let mut push = |text: &str, matches: Vec<usize>, reason: Reason| {
        unretracted.push(Unretracted {
            owner: owner.clone(),
            path: record.path.clone(),
            text: text.to_owned(),
            matches,
            reason,
        });
    };
    let Some(current) = current else {
        for text in &record.lines {
            push(text, Vec::new(), Reason::FileMissing);
        }
        return Vec::new();
    };
    let lines = split_lines(current);
    let gate = match &record.hash {
        None => Some(Reason::NoHash),
        Some(h) if *h != FileHash::of(current) => Some(Reason::HashMismatch),
        Some(_) => None,
    };
    let mut retract = Vec::new();
    for text in &record.lines {
        let matches = find(&lines, text);
        match (gate, matches.as_slice()) {
            (Some(reason), _) => push(text, matches, reason),
            (None, [number]) => retract.push(Line {
                text: text.clone(),
                number: *number,
            }),
            (None, _) => push(text, matches, Reason::NotUnique),
        }
    }
    retract
}

/// 切成行，每行含行尾；最後沒有換行的殘段也算一行，結尾的空段不算。
fn split_lines(bytes: &[u8]) -> Vec<&[u8]> {
    bytes.split_inclusive(|&b| b == b'\n').collect()
}

/// 一行去掉行尾後的原文：`\n` 或 `\r\n` 都算行尾；單獨的 `\r` 照原樣。
fn content(line: &[u8]) -> &[u8] {
    match line.strip_suffix(b"\n") {
        Some(rest) => rest.strip_suffix(b"\r").unwrap_or(rest),
        None => line,
    }
}

/// `text` 在 `lines` 裡相符的所有行號，從 1 起算。
fn find(lines: &[&[u8]], text: &str) -> Vec<usize> {
    lines
        .iter()
        .enumerate()
        .filter(|(_, line)| content(line) == text.as_bytes())
        .map(|(i, _)| i + 1)
        .collect()
}

/// 刪掉 `removed` 這些行（含行尾），其他位元組原樣保留。
fn remove_lines(bytes: &[u8], removed: &BTreeSet<usize>) -> Vec<u8> {
    split_lines(bytes)
        .into_iter()
        .enumerate()
        .filter(|(i, _)| !removed.contains(&(i + 1)))
        .flat_map(|(_, line)| line.iter().copied())
        .collect()
}

// ---------------------------------------------------------------------------
// 錯誤

/// 讀目前內容失敗（檔不在不算，那是 `Ok(None)`）。系統呼叫失敗還沒有代碼。
#[derive(Debug)]
pub struct ReadError {
    pub path: String,
    pub source: io::Error,
}

impl fmt::Display for ReadError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "cannot read {}: {}", self.path, self.source)
    }
}

impl std::error::Error for ReadError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        Some(&self.source)
    }
}

// ---------------------------------------------------------------------------

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;
    use metadata::WriteOutcome;

    const PATH: &str = ".gitignore";

    fn tool(repo: &str) -> Owner {
        Owner::Tool(repo.to_owned())
    }

    fn appended(path: &str, lines: &[&str], hash_of: Option<&[u8]>) -> FileRecord {
        let mut r = FileRecord::new(path, State::Appended);
        r.lines = lines.iter().map(|s| (*s).to_owned()).collect();
        r.hash = hash_of.map(FileHash::of);
        r
    }

    fn meta(records: Vec<FileRecord>) -> Metadata {
        let mut m = Metadata::new();
        for r in records {
            m.put(r).unwrap();
        }
        m
    }

    fn files(entries: &[(&str, &[u8])]) -> BTreeMap<String, Vec<u8>> {
        entries
            .iter()
            .map(|(p, c)| ((*p).to_owned(), c.to_vec()))
            .collect()
    }

    fn run(sources: &[(Owner, Metadata)], disk: &BTreeMap<String, Vec<u8>>) -> Plan {
        let sources: Vec<Source<'_>> = sources
            .iter()
            .map(|(owner, metadata)| Source { owner, metadata })
            .collect();
        plan(&sources, |p| Ok(disk.get(p).cloned())).unwrap()
    }

    fn one(record: FileRecord, current: Option<&[u8]>) -> Plan {
        let disk = match current {
            Some(c) => files(&[(record.path.as_str(), c)]),
            None => BTreeMap::new(),
        };
        run(&[(tool("a"), meta(vec![record]))], &disk)
    }

    fn line(text: &str, number: usize) -> Line {
        Line {
            text: text.to_owned(),
            number,
        }
    }

    fn reasons(p: &Plan) -> Vec<(String, Vec<usize>, Reason)> {
        p.unretracted
            .iter()
            .map(|u| (u.text.clone(), u.matches.clone(), u.reason))
            .collect()
    }

    // --- 逐種 state ---------------------------------------------------------

    #[test]
    fn states_without_lines_are_kept_and_not_read() {
        for state in [
            State::Managed,
            State::Declined,
            State::Unmanaged,
            State::Deleted,
        ] {
            let m = meta(vec![FileRecord::new("x/init.sh", state)]);
            let owner = tool("a");
            let mut reads = 0;
            let p = plan(
                &[Source {
                    owner: &owner,
                    metadata: &m,
                }],
                |_| {
                    reads += 1;
                    Ok(None)
                },
            )
            .unwrap();
            assert_eq!(reads, 0, "{state}");
            assert_eq!(
                p.records,
                vec![RecordPlan {
                    owner: tool("a"),
                    path: "x/init.sh".to_owned(),
                    state,
                    verdict: Verdict::Keep,
                }],
                "{state}"
            );
            assert!(p.questions.is_empty() && p.unretracted.is_empty() && p.edits.is_empty());
        }
    }

    #[test]
    fn states_other_than_appended_with_lines_are_a_gap() {
        for state in [
            State::Managed,
            State::Declined,
            State::Unmanaged,
            State::Deleted,
        ] {
            let before = b"keep\n";
            let mut r = appended(PATH, &["keep"], Some(before));
            r.state = state;
            let p = one(r, Some(before));
            assert_eq!(
                p.records[0].verdict,
                Verdict::Gap(Gap::LinesInOtherState),
                "{state}"
            );
            assert!(p.questions.is_empty() && p.unretracted.is_empty() && p.edits.is_empty());
        }
    }

    #[test]
    fn appended_without_lines_is_a_gap() {
        let p = one(FileRecord::new(PATH, State::Appended), Some(b"x\n"));
        assert_eq!(
            p.records[0].verdict,
            Verdict::Gap(Gap::AppendedWithoutLines)
        );
        assert!(p.questions.is_empty() && p.unretracted.is_empty() && p.edits.is_empty());
    }

    #[test]
    fn every_state_is_covered() {
        for state in State::ALL {
            let mut r = FileRecord::new(PATH, state);
            r.lines = vec!["x".to_owned()];
            let with = verdict(&r);
            r.lines.clear();
            let without = verdict(&r);
            let expected = match state {
                State::Appended => (Verdict::Judged, Verdict::Gap(Gap::AppendedWithoutLines)),
                State::Managed | State::Declined | State::Unmanaged | State::Deleted => {
                    (Verdict::Gap(Gap::LinesInOtherState), Verdict::Keep)
                }
            };
            assert_eq!((with, without), expected, "{state}");
        }
    }

    // --- ADR-0003 的收回情境 ------------------------------------------------

    #[test]
    fn unchanged_file_with_unique_line_is_asked() {
        let before = b"node_modules/\ncache/\n";
        let p = one(appended(PATH, &["cache/"], Some(before)), Some(before));
        assert_eq!(p.records[0].verdict, Verdict::Judged);
        assert_eq!(
            p.questions,
            vec![Question {
                owner: tool("a"),
                path: PATH.to_owned(),
                lines: vec![line("cache/", 2)],
            }]
        );
        assert!(p.unretracted.is_empty());
        assert_eq!(
            p.edits,
            vec![Edit {
                path: PATH.to_owned(),
                before: before.to_vec(),
                after: b"node_modules/\n".to_vec(),
                removed: vec![2],
            }]
        );
    }

    #[test]
    fn changed_file_is_not_retracted_even_with_unique_line() {
        let written = b"cache/\n";
        let p = one(
            appended(PATH, &["cache/"], Some(written)),
            Some(b"cache/\nmine\n"),
        );
        assert_eq!(
            reasons(&p),
            vec![("cache/".to_owned(), vec![1], Reason::HashMismatch)]
        );
        assert!(p.questions.is_empty() && p.edits.is_empty());
    }

    #[test]
    fn zero_or_many_matches_are_not_retracted() {
        let many = b"cache/\nx\ncache/\n";
        let p = one(appended(PATH, &["cache/", "gen/"], Some(many)), Some(many));
        assert_eq!(
            reasons(&p),
            vec![
                ("cache/".to_owned(), vec![1, 3], Reason::NotUnique),
                ("gen/".to_owned(), vec![], Reason::NotUnique),
            ]
        );
        assert!(p.questions.is_empty() && p.edits.is_empty());
    }

    #[test]
    fn line_ending_change_only_is_still_asked() {
        let written = b"a\ncache/\nb\n";
        let current = b"a\r\ncache/\r\nb\r\n";
        let p = one(appended(PATH, &["cache/"], Some(written)), Some(current));
        assert_eq!(p.questions[0].lines, vec![line("cache/", 2)]);
        assert_eq!(p.edits[0].after, b"a\r\nb\r\n");
    }

    #[test]
    fn reordering_changes_the_hash() {
        let written = b"a\ncache/\n";
        let p = one(
            appended(PATH, &["cache/"], Some(written)),
            Some(b"cache/\na\n"),
        );
        assert_eq!(
            reasons(&p),
            vec![("cache/".to_owned(), vec![1], Reason::HashMismatch)]
        );
    }

    #[test]
    fn rewritten_elsewhere_is_not_retracted() {
        let written = b"a\ncache/\nb\n";
        let p = one(
            appended(PATH, &["cache/"], Some(written)),
            Some(b"cache/\na\nb\n"),
        );
        assert_eq!(p.unretracted[0].reason, Reason::HashMismatch);
        assert!(p.edits.is_empty());
    }

    #[test]
    fn rewritten_in_place_is_asked() {
        // 刪掉後在原位置寫回同一行：內容與紀錄相同，依紀錄判定，先問。
        let written = b"a\ncache/\nb\n";
        let p = one(appended(PATH, &["cache/"], Some(written)), Some(written));
        assert_eq!(p.questions[0].lines, vec![line("cache/", 2)]);
    }

    #[test]
    fn cross_tool_write_after_user_edit_keeps_old_hash() {
        // a 寫入後使用者改檔，b 再由 VK 寫入同一檔：a 的紀錄保留舊 hash，收回時不刪 a 的行。
        let a_written = b"cache/\n".to_vec();
        let edited = b"cache/\nmine\n".to_vec();
        let b_written = b"cache/\nmine\ngen/\n".to_vec();
        let mut a = meta(vec![appended(PATH, &["cache/"], Some(&a_written))]);
        assert_eq!(
            a.record_write(PATH, &edited, &b_written).unwrap(),
            WriteOutcome::Mismatch
        );
        let b = meta(vec![appended(PATH, &["gen/"], Some(&b_written))]);
        let p = run(
            &[(tool("a"), a), (tool("b"), b)],
            &files(&[(PATH, &b_written)]),
        );
        assert_eq!(
            reasons(&p),
            vec![("cache/".to_owned(), vec![1], Reason::HashMismatch)]
        );
        assert_eq!(p.questions.len(), 1);
        assert_eq!(p.questions[0].owner, tool("b"));
        assert_eq!(p.edits[0].after, b"cache/\nmine\n");
    }

    #[test]
    fn record_without_hash_is_listed_only() {
        let current = b"cache/\n";
        let p = one(appended(PATH, &["cache/"], None), Some(current));
        assert_eq!(
            reasons(&p),
            vec![("cache/".to_owned(), vec![1], Reason::NoHash)]
        );
        assert!(p.edits.is_empty());
    }

    #[test]
    fn missing_file_is_listed_with_no_matches() {
        let p = one(appended(PATH, &["cache/", "gen/"], Some(b"cache/\n")), None);
        assert_eq!(
            reasons(&p),
            vec![
                ("cache/".to_owned(), vec![], Reason::FileMissing),
                ("gen/".to_owned(), vec![], Reason::FileMissing),
            ]
        );
        assert!(p.questions.is_empty() && p.edits.is_empty());
    }

    #[test]
    fn one_bad_line_does_not_drop_the_record() {
        let written = b"cache/\nx\nx\ngen/\n";
        let p = one(
            appended(PATH, &["cache/", "x", "gen/"], Some(written)),
            Some(written),
        );
        assert_eq!(
            p.questions[0].lines,
            vec![line("cache/", 1), line("gen/", 4)]
        );
        assert_eq!(
            reasons(&p),
            vec![("x".to_owned(), vec![2, 3], Reason::NotUnique)]
        );
        assert_eq!(p.edits[0].after, b"x\nx\n");
        assert_eq!(p.edits[0].removed, vec![1, 4]);
    }

    #[test]
    fn whitespace_is_not_ignored() {
        let written = b"cache/ \n cache/\n";
        let p = one(appended(PATH, &["cache/"], Some(written)), Some(written));
        assert_eq!(
            reasons(&p),
            vec![("cache/".to_owned(), vec![], Reason::NotUnique)]
        );
    }

    // --- 多份紀錄 -----------------------------------------------------------

    #[test]
    fn uninstall_merges_records_on_one_file_into_one_edit() {
        let written = b"mine\ncache/\ngen/\n".to_vec();
        let a = meta(vec![appended(PATH, &["cache/"], Some(&written))]);
        let b = meta(vec![appended(PATH, &["gen/"], Some(&written))]);
        let vk = meta(vec![appended(".dockerignore", &["log/"], Some(b"log/\n"))]);
        let disk = files(&[(PATH, &written), (".dockerignore", b"log/\n")]);
        let p = run(&[(tool("a"), a), (tool("b"), b), (Owner::Vk, vk)], &disk);
        assert_eq!(p.questions.len(), 3);
        assert_eq!(p.questions[2].owner, Owner::Vk);
        assert_eq!(
            p.edits,
            vec![
                Edit {
                    path: ".dockerignore".to_owned(),
                    before: b"log/\n".to_vec(),
                    after: Vec::new(),
                    removed: vec![1],
                },
                Edit {
                    path: PATH.to_owned(),
                    before: written,
                    after: b"mine\n".to_vec(),
                    removed: vec![2, 3],
                },
            ]
        );
    }

    #[test]
    fn remove_one_tool_then_remaining_record_updates() {
        let written = b"mine\ncache/\ngen/\n".to_vec();
        let a = meta(vec![appended(PATH, &["cache/"], Some(&written))]);
        let mut b = meta(vec![appended(PATH, &["gen/"], Some(&written))]);
        let p = run(&[(tool("a"), a)], &files(&[(PATH, &written)]));
        let edit = &p.edits[0];
        assert_eq!(edit.after, b"mine\ngen/\n");
        assert_eq!(
            b.record_write(PATH, &edit.before, &edit.after).unwrap(),
            WriteOutcome::Updated
        );
        assert_eq!(b.get(PATH).unwrap().hash, Some(FileHash::of(&edit.after)));
    }

    #[test]
    fn same_line_claimed_twice_is_removed_once() {
        let written = b"cache/\n".to_vec();
        let a = meta(vec![appended(PATH, &["cache/"], Some(&written))]);
        let b = meta(vec![appended(PATH, &["cache/"], Some(&written))]);
        let p = run(
            &[(tool("a"), a), (tool("b"), b)],
            &files(&[(PATH, &written)]),
        );
        assert_eq!(p.questions.len(), 2);
        assert_eq!(p.edits[0].removed, vec![1]);
        assert_eq!(p.edits[0].after, b"");
    }

    #[test]
    fn each_path_is_read_once() {
        let written = b"cache/\ngen/\n".to_vec();
        let a = meta(vec![appended(PATH, &["cache/"], Some(&written))]);
        let b = meta(vec![appended(PATH, &["gen/"], Some(&written))]);
        let (oa, ob) = (tool("a"), tool("b"));
        let mut reads = Vec::new();
        plan(
            &[
                Source {
                    owner: &oa,
                    metadata: &a,
                },
                Source {
                    owner: &ob,
                    metadata: &b,
                },
            ],
            |p| {
                reads.push(p.to_owned());
                Ok(Some(written.clone()))
            },
        )
        .unwrap();
        assert_eq!(reads, vec![PATH.to_owned()]);
    }

    #[test]
    fn read_error_is_returned() {
        let m = meta(vec![appended(PATH, &["cache/"], Some(b"cache/\n"))]);
        let owner = tool("a");
        let err = plan(
            &[Source {
                owner: &owner,
                metadata: &m,
            }],
            |_| Err(io::Error::from(io::ErrorKind::PermissionDenied)),
        )
        .unwrap_err();
        assert_eq!(err.path, PATH);
        assert_eq!(err.source.kind(), io::ErrorKind::PermissionDenied);
    }

    // --- 位元組保留 ---------------------------------------------------------

    #[test]
    fn removing_lines_keeps_other_bytes() {
        let set = |ns: &[usize]| ns.iter().copied().collect::<BTreeSet<_>>();
        assert_eq!(remove_lines(b"a\r\nb\nc", &set(&[2])), b"a\r\nc");
        assert_eq!(remove_lines(b"a\r\nb\nc", &set(&[3])), b"a\r\nb\n");
        assert_eq!(remove_lines(b"a\r\nb\nc", &set(&[1])), b"b\nc");
        assert_eq!(remove_lines(b"a\n\nb\n", &set(&[2])), b"a\nb\n");
    }

    #[test]
    fn last_line_without_newline_matches() {
        let written = b"mine\ncache/";
        let p = one(appended(PATH, &["cache/"], Some(written)), Some(written));
        assert_eq!(p.edits[0].after, b"mine\n");
    }

    #[test]
    fn lone_carriage_return_is_content() {
        assert_eq!(content(b"a\r"), b"a\r");
        assert_eq!(content(b"a\r\n"), b"a");
        assert_eq!(content(b"a\n"), b"a");
        let lines = split_lines(b"a\rb\n");
        assert_eq!(find(&lines, "a"), Vec::<usize>::new());
    }

    #[test]
    fn unretracted_is_vk0061() {
        let p = one(appended(PATH, &["cache/"], None), Some(b"cache/\n"));
        assert_eq!(p.unretracted[0].message().code, "VK0061");
    }
}
