//! `add`／`upgrade` 處理初始檔（ADR-0003；04 使用者的檔與 VK 的檔、寫入既有檔的例外）。
//!
//! - 初始檔一落地就是使用者的檔：永不刪、永不覆蓋，要改先問（02 不變量第 1 條）。這裡只算每個初始檔
//!   要怎麼處理，不寫檔、不詢問：[`Plan::questions`] 收齊這次全部的問題，由呼叫端經 `prompt` 一次問完，
//!   全部同意才照 [`Plan::files`] 寫入（04 共同選項）。
//! - 輸入是指令（[`Command`]）、工具新版的初始檔（[`InitFile`]：路徑、內容、是不是 append 型）、這個工具的
//!   逐檔紀錄 [`Metadata`]（首次 `add` 傳 [`Metadata::new`]；紀錄缺失或損壞的 VK0013 在
//!   [`Metadata::load`] 就擋下），以及呼叫端注入的兩個讀檔函式：目前 repo 檔與基準版副本。
//!   基準版副本存在哪裡契約沒寫，所以這裡不碰路徑，新的基準版內容也交給呼叫端存。
//! - 判定（[`plan`]）逐個初始檔，依紀錄的 state 分：
//!
//!   | 紀錄 | 情況 | 判定 |
//!   |---|---|---|
//!   | 沒有 | 檔不在 | [`Verdict::Create`]：新建、不問，記 `managed` |
//!   | 沒有 | 檔在、append 型 | [`Verdict::Append`]：先問再 append，記 `appended` 與實際插入的行 |
//!   | 沒有 | 檔在、整份型、`add` | [`Verdict::Existing`]：不納管、不覆蓋，記 `unmanaged`，VK0018 |
//!   | `managed` | 新版與基準版相同 | [`Verdict::UpstreamUnchanged`]：不動 |
//!   | `managed` | 目前檔與基準版相同（只差行尾也算） | [`Verdict::Replace`]：未改過也先問是否換版 |
//!   | `managed` | 雙方都改過 | [`Verdict::Merge`]：先問是否合併；有衝突照樣寫入、留標記，VK0021 |
//!   | `managed` | 檔不在 | [`Verdict::UserDeleted`]：不重建，記 `deleted`，列進 stdout 清單 |
//!   | `appended` | 新版的行與紀錄相同 | [`Verdict::UpstreamUnchanged`]：不動 |
//!   | `unmanaged` | 不論 | [`Verdict::Unmanaged`]：不處理，VK0019 |
//!   | `declined` | `declined_hash` 等於新版 | [`Verdict::Declined`]：不問、不套用，VK0020 |
//!   | `deleted` | 檔不在 | [`Verdict::StillDeleted`]：不重建，列進 stdout 清單 |
//!
//!   其他組合契約沒寫到，不自己補規則，判成 [`Verdict::Gap`]（見 [`Gap`]）：不寫、不問、不改紀錄。
//! - 「使用者改過」以目前檔與基準版比（CRLF→LF 正規化後的指紋，[`files::fingerprint_normalized`]），
//!   不看紀錄的 `hash`：上次合併過的檔 hash 相符，內容卻不是基準版。
//! - 換版與合併都經 `merge` 算出寫入內容（基準版、目前檔、新版）；目前檔與基準版相同時結果就是新版，
//!   行尾跟著目前檔，只改行尾的使用者不會被換掉行尾。合併留下衝突時基準版照樣推到新版
//!   （scope_roadmap:32）。合併結果是 TOML／just 而解析不過的例外與 metadata `conflicts` 欄位這裡不做。
//! - 這裡不寫檔，寫入由呼叫端做：
//!   - [`FilePlan::write`]：要寫的 repo 檔，帶判定用的寫入前內容（新建時沒有）與寫入後內容。
//!   - [`FilePlan::baseline`]：要存的新基準版內容。
//!   - [`FilePlan::record`]：要 [`Metadata::put`] 進這個工具紀錄的新紀錄。新建、append 的紀錄已帶寫入後的
//!     `hash`；換版、合併不換紀錄（`None`），呼叫端對每一份含這個路徑的紀錄檔（這個工具的、其他工具的、
//!     `baseline/.vendor_kit.toml`）都以同一份寫入前內容呼叫 [`Metadata::record_write`]`(path, before, after)`。
//!     append 進別的工具也 append 過的檔時一樣，這裡只產這個工具的紀錄。
//! - 這裡不印診斷：每個判定對應的訊息表條目在 [`FilePlan::message`]，`<file>` 以外的欄位（VK0020 的
//!   `<repo>`、`<tag>`）由呼叫端填；要列進 stdout 清單的在 [`FilePlan::listed`]。

use std::collections::BTreeSet;
use std::fmt;
use std::io;

use messages::Message;
use metadata::{FileHash, FileRecord, Metadata, State};

#[cfg(test)]
mod tests;

// ---------------------------------------------------------------------------
// 輸入

/// 哪個指令在處理初始檔。`update` 只查不換版（04），不會走到這裡。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Command {
    /// 首次導入工具。
    Add,
    /// 工具換版。
    Upgrade,
}

/// 初始檔怎麼落地（工具 `init.toml` 的 `strategy`；這裡不解析 `init.toml`）。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Strategy {
    /// 整份初始檔。
    Whole,
    /// `strategy = "append"`：把內容的每一行插進既有檔。
    Append,
}

/// 工具新版的一個初始檔。
#[derive(Debug, Clone, Copy)]
pub struct InitFile<'a> {
    /// repo 相對路徑。
    pub path: &'a str,
    pub strategy: Strategy,
    /// 新版內容；append 型是要插入的行。
    pub contents: &'a [u8],
}

// ---------------------------------------------------------------------------
// 輸出

/// 要問的事。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Ask {
    /// 檔已存在，是否 append。
    Append,
    /// 使用者沒改過，是否換成新版。
    Replace,
    /// 雙方都改過，是否合併。
    Merge,
}

/// 要問的一題。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Question {
    pub path: String,
    pub ask: Ask,
}

/// 全部同意時對一個 repo 檔的寫入。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Write {
    /// 判定用的寫入前內容；新建時是 `None`。
    pub before: Option<Vec<u8>>,
    /// 寫入後的內容。
    pub after: Vec<u8>,
}

/// 契約沒寫到的情況：不寫、不問、不改紀錄，交呼叫端。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Gap {
    /// append 型初始檔的目標不存在：04 說不存在就新建，但沒說記成哪個 state。
    AppendTargetMissing,
    /// 要 append 的行有些已在檔裡：04 只說未收回的內容不得無條件再 append。
    LinesAlreadyPresent,
    /// append 型初始檔沒有任何一行。
    EmptyAppend,
    /// `upgrade` 遇到新版才有的初始檔，而 repo 裡已有不適用 append 的同名檔（VK0018 只寫 add）。
    ExistingOnUpgrade,
    /// `add` 時這個工具已有這個檔的紀錄。
    RecordOnAdd,
    /// 新版改了初始檔的落地方式（整份型與 append 型互換）。
    StrategyChanged,
    /// `appended` 的紀錄遇到新版要插的行不同：契約沒寫 append 型怎麼升版。
    AppendedLinesChanged,
    /// `declined` 的紀錄遇到別的版本，或紀錄沒有 `declined_hash`：拒絕記錄的保存方式待 #47。
    DeclinedOtherVersion,
    /// `deleted` 的紀錄，檔又出現了。
    DeletedReappeared,
    /// `managed` 的目前檔已等於新版、卻不等於基準版：repo 檔不變，契約沒寫要不要問、基準版推不推。
    CurrentIsNew,
    /// 紀錄裡有、新版不再提供的初始檔：04 說只列清單，但沒說紀錄記成什麼。
    NoLongerProvided,
}

/// 一個初始檔的判定。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Verdict {
    /// 檔不在：新建、不問。
    Create,
    /// 檔已存在：問過後 append。
    Append,
    /// `add` 遇到已存在、不適用 append 的檔：不納管、不覆蓋（VK0018）。
    Existing,
    /// 新版沒變：不動。
    UpstreamUnchanged,
    /// 使用者沒改過：問過後換成新版。
    Replace,
    /// 雙方都改過：問過後合併；`conflicts` 是衝突段數（VK0021），乾淨合併是 `None`。
    Merge { conflicts: Option<u32> },
    /// 未納管：不處理（VK0019）。
    Unmanaged,
    /// 這一版先前被拒絕：不問、不套用（VK0020）。
    Declined,
    /// 使用者刪掉了納管的初始檔：不重建，記 `deleted`。
    UserDeleted,
    /// 先前就記成 `deleted`：不重建。
    StillDeleted,
    /// 契約沒寫到。
    Gap(Gap),
}

/// 一個初始檔的動作。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FilePlan {
    pub path: String,
    pub verdict: Verdict,
    /// 寫入前要問的事；`None` 是不用問。
    pub ask: Option<Ask>,
    /// 全部同意時要寫的 repo 檔。
    pub write: Option<Write>,
    /// 全部同意時要存的新基準版內容。
    pub baseline: Option<Vec<u8>>,
    /// 全部同意時要 [`Metadata::put`] 的紀錄；`None` 是不換紀錄。
    pub record: Option<FileRecord>,
}

impl FilePlan {
    fn new(path: &str, verdict: Verdict) -> Self {
        FilePlan {
            path: path.to_owned(),
            verdict,
            ask: None,
            write: None,
            baseline: None,
            record: None,
        }
    }

    /// 對應的訊息表條目；沒有診斷回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self.verdict {
            Verdict::Existing => Some(&messages::VK0018),
            Verdict::Unmanaged => Some(&messages::VK0019),
            Verdict::Declined => Some(&messages::VK0020),
            Verdict::Merge {
                conflicts: Some(_), ..
            } => Some(&messages::VK0021),
            _ => None,
        }
    }

    /// 要列進 stdout 清單：不刪、不重建的納管初始檔（04 寫入既有檔的例外）。
    pub fn listed(&self) -> bool {
        matches!(self.verdict, Verdict::UserDeleted | Verdict::StillDeleted)
    }
}

/// 這次初始檔的動作清單與要問的問題。
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Plan {
    /// 每個初始檔一筆，順序同輸入；後面接紀錄裡有、新版不再提供的檔，順序同紀錄。
    pub files: Vec<FilePlan>,
    /// 這次全部要問的問題，順序同 `files`。
    pub questions: Vec<Question>,
}

impl Plan {
    /// 契約沒寫到的檔。
    pub fn gaps(&self) -> impl Iterator<Item = (&str, Gap)> {
        self.files.iter().filter_map(|f| match f.verdict {
            Verdict::Gap(gap) => Some((f.path.as_str(), gap)),
            _ => None,
        })
    }
}

// ---------------------------------------------------------------------------
// 錯誤

/// 讀的是哪一份。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Side {
    /// 目前 repo 檔。
    Current,
    /// 基準版副本。
    Baseline,
}

/// 判定沒有完成。
#[derive(Debug)]
pub enum Error {
    /// 讀檔失敗。
    Read {
        path: String,
        side: Side,
        source: io::Error,
    },
    /// `managed` 的紀錄找不到基準版副本：不猜、不改用兩方比對或覆蓋（ADR-0003）。
    BaselineMissing { path: String },
    /// append 型初始檔不是 UTF-8，行原文記不進紀錄。
    NotUtf8 { path: String },
    /// 新版的初始檔清單裡同一個路徑出現兩次。
    DuplicatePath { path: String },
    /// 基準版合併沒有完成。
    Merge { path: String, source: merge::Error },
}

impl Error {
    /// 對應的訊息表條目：這些情況還沒有代碼，回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            Error::Merge { source, .. } => source.message(),
            _ => None,
        }
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Read { path, side, source } => {
                let side = match side {
                    Side::Current => "file",
                    Side::Baseline => "baseline of",
                };
                write!(f, "cannot read {side} {path}: {source}")
            }
            Error::BaselineMissing { path } => write!(f, "baseline of managed {path} is missing"),
            Error::NotUtf8 { path } => write!(f, "append init file {path} is not valid UTF-8"),
            Error::DuplicatePath { path } => write!(f, "init file {path} is listed twice"),
            Error::Merge { path, source } => write!(f, "baseline merge of {path}: {source}"),
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Error::Read { source, .. } => Some(source),
            Error::Merge { source, .. } => Some(source),
            _ => None,
        }
    }
}

// ---------------------------------------------------------------------------
// 判定

/// 依新版初始檔與這個工具的逐檔紀錄算出動作與問題。
///
/// `current(path)` 回傳 repo 相對路徑 `path` 目前的內容，`baseline(path)` 回傳它的基準版副本；
/// 檔不在都回 `Ok(None)`。基準版只在 `managed` 的紀錄需要時才讀。
pub fn plan<C, B>(
    command: Command,
    init_files: &[InitFile<'_>],
    metadata: &Metadata,
    mut current: C,
    mut baseline: B,
) -> Result<Plan, Error>
where
    C: FnMut(&str) -> io::Result<Option<Vec<u8>>>,
    B: FnMut(&str) -> io::Result<Option<Vec<u8>>>,
{
    let mut seen = BTreeSet::new();
    let mut plan = Plan::default();
    for file in init_files {
        if !seen.insert(file.path) {
            return Err(Error::DuplicatePath {
                path: file.path.to_owned(),
            });
        }
        let now = current(file.path).map_err(|source| Error::Read {
            path: file.path.to_owned(),
            side: Side::Current,
            source,
        })?;
        let file_plan = match metadata.get(file.path) {
            None => first_import(command, file, now)?,
            Some(_) if command == Command::Add => {
                FilePlan::new(file.path, Verdict::Gap(Gap::RecordOnAdd))
            }
            Some(record) => upgrade(file, record, now, &mut baseline)?,
        };
        if let Some(ask) = file_plan.ask {
            plan.questions.push(Question {
                path: file_plan.path.clone(),
                ask,
            });
        }
        plan.files.push(file_plan);
    }
    for record in metadata.files() {
        if !seen.contains(record.path.as_str()) {
            plan.files.push(FilePlan::new(
                &record.path,
                Verdict::Gap(Gap::NoLongerProvided),
            ));
        }
    }
    Ok(plan)
}

/// 這個工具還沒有這個檔的紀錄。
fn first_import(
    command: Command,
    file: &InitFile<'_>,
    now: Option<Vec<u8>>,
) -> Result<FilePlan, Error> {
    let gap = |gap| Ok(FilePlan::new(file.path, Verdict::Gap(gap)));
    match (file.strategy, now) {
        (Strategy::Whole, None) => {
            let mut p = FilePlan::new(file.path, Verdict::Create);
            let mut record = FileRecord::new(file.path, State::Managed);
            record.hash = Some(FileHash::of(file.contents));
            p.write = Some(Write {
                before: None,
                after: file.contents.to_vec(),
            });
            p.baseline = Some(file.contents.to_vec());
            p.record = Some(record);
            Ok(p)
        }
        (Strategy::Append, None) => gap(Gap::AppendTargetMissing),
        (Strategy::Whole, Some(_)) if command == Command::Add => {
            let mut p = FilePlan::new(file.path, Verdict::Existing);
            p.record = Some(FileRecord::new(file.path, State::Unmanaged));
            Ok(p)
        }
        (Strategy::Whole, Some(_)) => gap(Gap::ExistingOnUpgrade),
        (Strategy::Append, Some(before)) => {
            let lines = append_lines(file)?;
            if lines.is_empty() {
                return gap(Gap::EmptyAppend);
            }
            let present: BTreeSet<&[u8]> = split_lines(&before).into_iter().map(content).collect();
            if lines.iter().any(|l| present.contains(l.as_bytes())) {
                return gap(Gap::LinesAlreadyPresent);
            }
            let after = append(&before, &lines);
            let mut record = FileRecord::new(file.path, State::Appended);
            record.hash = Some(FileHash::of(&after));
            record.lines = lines;
            let mut p = FilePlan::new(file.path, Verdict::Append);
            p.ask = Some(Ask::Append);
            p.write = Some(Write {
                before: Some(before),
                after,
            });
            p.record = Some(record);
            Ok(p)
        }
    }
}

/// `upgrade`：這個工具已有這個檔的紀錄。
fn upgrade<B>(
    file: &InitFile<'_>,
    record: &FileRecord,
    now: Option<Vec<u8>>,
    baseline: &mut B,
) -> Result<FilePlan, Error>
where
    B: FnMut(&str) -> io::Result<Option<Vec<u8>>>,
{
    let p = |verdict| Ok(FilePlan::new(file.path, verdict));
    match (record.state, file.strategy) {
        (State::Unmanaged, _) => p(Verdict::Unmanaged),
        (State::Declined, _) => {
            if record.declined_hash.as_ref() == Some(&FileHash::of(file.contents)) {
                p(Verdict::Declined)
            } else {
                p(Verdict::Gap(Gap::DeclinedOtherVersion))
            }
        }
        (State::Deleted, _) => match now {
            None => p(Verdict::StillDeleted),
            Some(_) => p(Verdict::Gap(Gap::DeletedReappeared)),
        },
        (State::Appended, Strategy::Append) => {
            if append_lines(file)? == record.lines {
                p(Verdict::UpstreamUnchanged)
            } else {
                p(Verdict::Gap(Gap::AppendedLinesChanged))
            }
        }
        (State::Managed, Strategy::Whole) => managed(file, record, now, baseline),
        (State::Appended, Strategy::Whole) | (State::Managed, Strategy::Append) => {
            p(Verdict::Gap(Gap::StrategyChanged))
        }
    }
}

/// `managed` 的整份型初始檔換版。
fn managed<B>(
    file: &InitFile<'_>,
    record: &FileRecord,
    now: Option<Vec<u8>>,
    baseline: &mut B,
) -> Result<FilePlan, Error>
where
    B: FnMut(&str) -> io::Result<Option<Vec<u8>>>,
{
    let Some(now) = now else {
        let mut p = FilePlan::new(file.path, Verdict::UserDeleted);
        let mut deleted = record.clone();
        deleted.state = State::Deleted;
        p.record = Some(deleted);
        return Ok(p);
    };
    let base = baseline(file.path)
        .map_err(|source| Error::Read {
            path: file.path.to_owned(),
            side: Side::Baseline,
            source,
        })?
        .ok_or_else(|| Error::BaselineMissing {
            path: file.path.to_owned(),
        })?;
    if same(&base, file.contents) {
        return Ok(FilePlan::new(file.path, Verdict::UpstreamUnchanged));
    }
    let user_unchanged = same(&now, &base);
    if !user_unchanged && same(&now, file.contents) {
        return Ok(FilePlan::new(file.path, Verdict::Gap(Gap::CurrentIsNew)));
    }
    let outcome = merge::merge(&merge::Inputs {
        baseline: &base,
        current: &now,
        new: file.contents,
    })
    .map_err(|source| Error::Merge {
        path: file.path.to_owned(),
        source,
    })?;
    let (verdict, ask) = match (&outcome, user_unchanged) {
        (merge::Outcome::Clean(_), true) => (Verdict::Replace, Ask::Replace),
        (merge::Outcome::Clean(_), false) => (Verdict::Merge { conflicts: None }, Ask::Merge),
        (merge::Outcome::Conflicts { count, .. }, _) => (
            Verdict::Merge {
                conflicts: Some(*count),
            },
            Ask::Merge,
        ),
    };
    let mut p = FilePlan::new(file.path, verdict);
    p.ask = Some(ask);
    p.write = Some(Write {
        before: Some(now),
        after: outcome.into_contents(),
    });
    p.baseline = Some(file.contents.to_vec());
    Ok(p)
}

// ---------------------------------------------------------------------------
// 內容

/// CRLF→LF 正規化後相同。
fn same(a: &[u8], b: &[u8]) -> bool {
    files::fingerprint_normalized(a) == files::fingerprint_normalized(b)
}

/// append 型初始檔要插入的行，不含行尾；最後沒有換行的殘段也算一行。
fn append_lines(file: &InitFile<'_>) -> Result<Vec<String>, Error> {
    let text = std::str::from_utf8(file.contents).map_err(|_| Error::NotUtf8 {
        path: file.path.to_owned(),
    })?;
    Ok(split_lines(text.as_bytes())
        .into_iter()
        .map(|line| String::from_utf8_lossy(content(line)).into_owned())
        .collect())
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

/// 把 `lines` 接在 `before` 後面，行尾跟著 `before`：CRLF 行多於單獨 LF 的行就用 CRLF，否則用 LF
/// （同 `merge`）。`before` 最後一行沒有換行時先補一個；其他位元組原樣保留。
fn append(before: &[u8], lines: &[String]) -> Vec<u8> {
    let eol: &[u8] = if uses_crlf(before) { b"\r\n" } else { b"\n" };
    let mut out = before.to_vec();
    if !out.is_empty() && !out.ends_with(b"\n") {
        out.extend_from_slice(eol);
    }
    for line in lines {
        out.extend_from_slice(line.as_bytes());
        out.extend_from_slice(eol);
    }
    out
}

/// CRLF 行多於單獨 LF 的行。
fn uses_crlf(contents: &[u8]) -> bool {
    let (mut crlf, mut lf) = (0usize, 0usize);
    for line in split_lines(contents) {
        if line.ends_with(b"\r\n") {
            crlf += 1;
        } else if line.ends_with(b"\n") {
            lf += 1;
        }
    }
    crlf > lf
}
