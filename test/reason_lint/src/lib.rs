//! 原因代碼使用檢查（#136）：比對訊息表 `doc/contract/reason_codes.csv` 登錄的代碼，
//! 與 repo 原始碼裡實際出現的 `VKnnnn`。
//!
//! - 擋：出現訊息表沒登錄的代碼、出現已退役的代碼。測試故意用的代碼列在例外清單 [`Allow`]；
//!   例外清單裡對不上任何出現處的項目也擋，免得清單過時。
//! - 只列不擋：登錄為使用中、`source` 含 `engine`，但 `engine/` 裡還沒有以 `messages::VKnnnn`
//!   用到的代碼（引擎還沒寫完）。清單印在 stderr，`cargo test -p reason_lint -- --nocapture` 看得到。
//!
//! 這是讀原始碼文字的靜態檢查（同 test/boundary），不是驗收測試；檢查本體在 `tests/`。

use std::collections::BTreeMap;
use std::path::Path;

/// 訊息表一列的狀態（`status` 欄）。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Status {
    Active,
    Retired,
}

/// 訊息表一列裡這個檢查用到的欄位。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Entry {
    pub status: Status,
    /// `source` 欄以空白分開的入口，例如 `engine`、`bootstrap`。
    pub sources: Vec<String>,
}

/// 代碼 → 訊息表的列。
pub type Table = BTreeMap<String, Entry>;

const BOM: &[u8] = b"\xEF\xBB\xBF";

/// 讀訊息表的 `code`、`status`、`source` 三欄；格式由 msggen 驗，這裡只擋讀不懂的狀態與重複代碼。
pub fn parse_table(bytes: &[u8]) -> Result<Table, String> {
    let body = bytes.strip_prefix(BOM).unwrap_or(bytes);
    let mut reader = csv::ReaderBuilder::new()
        .has_headers(true)
        .from_reader(body);
    let headers = reader
        .headers()
        .map_err(|e| format!("cannot read header: {e}"))?
        .clone();
    let column = |name: &str| {
        headers
            .iter()
            .position(|h| h == name)
            .ok_or_else(|| format!("missing column: {name}"))
    };
    let (code_i, status_i, source_i) = (column("code")?, column("status")?, column("source")?);

    let mut table = Table::new();
    for (n, record) in reader.records().enumerate() {
        let line = n + 2;
        let record = record.map_err(|e| format!("row {line}: {e}"))?;
        let field = |i: usize| record.get(i).unwrap_or("");
        let code = field(code_i).to_owned();
        let status = match field(status_i) {
            "active" => Status::Active,
            "retired" => Status::Retired,
            other => return Err(format!("row {line}: unknown status {other:?}")),
        };
        let sources = field(source_i)
            .split_whitespace()
            .map(str::to_owned)
            .collect();
        if table
            .insert(code.clone(), Entry { status, sources })
            .is_some()
        {
            return Err(format!("row {line}: duplicate code {code}"));
        }
    }
    Ok(table)
}

/// 原始碼裡出現一次代碼。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Occurrence {
    /// repo 相對路徑，以 `/` 分隔。
    pub path: String,
    /// 從 1 起算的行號。
    pub line: usize,
    pub code: String,
    /// 寫成 `messages::VKnnnn`（引擎取訊息表常數的寫法）。
    pub via_messages: bool,
}

/// 找出一段文字裡所有 `VK` 後接剛好四位數字的代碼；前後緊接英數字或底線的不算。
pub fn scan_text(path: &str, text: &str) -> Vec<Occurrence> {
    let mut found = Vec::new();
    for (n, line) in text.lines().enumerate() {
        let bytes = line.as_bytes();
        let mut i = 0;
        while let Some(off) = line[i..].find("VK") {
            let start = i + off;
            let digits = &bytes[start + 2..];
            let is_word = |b: u8| b.is_ascii_alphanumeric() || b == b'_';
            let four = digits.len() >= 4 && digits[..4].iter().all(u8::is_ascii_digit);
            let ends = digits.get(4).is_none_or(|b| !is_word(*b));
            let begins = start == 0 || !is_word(bytes[start - 1]);
            if four && ends && begins {
                found.push(Occurrence {
                    path: path.to_owned(),
                    line: n + 1,
                    code: line[start..start + 6].to_owned(),
                    via_messages: line[..start].ends_with("messages::"),
                });
            }
            i = start + 2;
        }
    }
    found
}

/// 走訪 `root` 底下的 `dirs`（repo 相對路徑），掃每個 UTF-8 文字檔；
/// 跳過名為 `target` 的目錄與 `skip` 列的路徑（目錄或檔）。結果依路徑排序。
pub fn scan_tree(root: &Path, dirs: &[&str], skip: &[&str]) -> Result<Vec<Occurrence>, String> {
    let mut found = Vec::new();
    let mut stack: Vec<String> = dirs.iter().map(|d| (*d).to_owned()).collect();
    while let Some(rel) = stack.pop() {
        if skip.contains(&rel.as_str()) {
            continue;
        }
        let abs = root.join(&rel);
        if abs.is_dir() {
            if abs.file_name().is_some_and(|n| n == "target") {
                continue;
            }
            let entries = std::fs::read_dir(&abs).map_err(|e| format!("{rel}: {e}"))?;
            for entry in entries {
                let entry = entry.map_err(|e| format!("{rel}: {e}"))?;
                let name = entry.file_name().to_string_lossy().into_owned();
                stack.push(format!("{rel}/{name}"));
            }
        } else if let Ok(text) = std::fs::read_to_string(&abs) {
            found.extend(scan_text(&rel, &text));
        }
    }
    found.sort_by(|a, b| (&a.path, a.line).cmp(&(&b.path, b.line)));
    Ok(found)
}

/// 例外：某個檔可以出現某個未登錄或已退役的代碼。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Allow {
    pub path: &'static str,
    pub code: &'static str,
    /// 為什麼可以（寫給讀者，不參與比對）。
    pub reason: &'static str,
}

/// 比對結果。
#[derive(Debug, Default, PartialEq, Eq)]
pub struct Report {
    /// 訊息表沒登錄的代碼（擋）。
    pub unregistered: Vec<Occurrence>,
    /// 已退役的代碼（擋）。
    pub retired: Vec<Occurrence>,
    /// 對不上任何出現處的例外（擋）。
    pub stale_allows: Vec<Allow>,
    /// 引擎該用、還沒用到的代碼（只列）。
    pub unused: Vec<String>,
}

impl Report {
    /// 要擋下的問題，一行一項；沒有就是空的。
    pub fn problems(&self) -> Vec<String> {
        let at = |o: &Occurrence| format!("{}:{} {}", o.path, o.line, o.code);
        let mut out = Vec::new();
        out.extend(
            self.unregistered
                .iter()
                .map(|o| format!("訊息表沒登錄：{}", at(o))),
        );
        out.extend(self.retired.iter().map(|o| format!("已退役：{}", at(o))));
        out.extend(
            self.stale_allows
                .iter()
                .map(|a| format!("例外對不上任何出現處：{} {}", a.path, a.code)),
        );
        out
    }
}

/// 依訊息表檢查出現處。`unused` 只算 `engine/` 底下以 `messages::VKnnnn` 寫的出現處。
pub fn check(table: &Table, found: &[Occurrence], allows: &[Allow]) -> Report {
    let mut report = Report::default();
    let allowed = |o: &Occurrence| allows.iter().any(|a| a.path == o.path && a.code == o.code);
    for o in found {
        let status = table.get(&o.code).map(|e| e.status);
        if status == Some(Status::Active) || allowed(o) {
            continue;
        }
        match status {
            None => report.unregistered.push(o.clone()),
            Some(_) => report.retired.push(o.clone()),
        }
    }
    report.stale_allows = allows
        .iter()
        .filter(|a| {
            let registered = table
                .get(a.code)
                .is_some_and(|e| e.status == Status::Active);
            registered || !found.iter().any(|o| o.path == a.path && o.code == a.code)
        })
        .copied()
        .collect();
    report.unused = table
        .iter()
        .filter(|(_, e)| e.status == Status::Active && e.sources.iter().any(|s| s == "engine"))
        .filter(|(code, _)| {
            !found
                .iter()
                .any(|o| o.via_messages && o.path.starts_with("engine/") && &o.code == *code)
        })
        .map(|(code, _)| code.clone())
        .collect();
    report
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    const HEADER: &str = "\u{feff}code,status,level,exit_code,disposition,source,situation.zh-TW,message.zh-TW,situation.en,message.en\n";

    fn table() -> Table {
        parse_table(
            format!(
                "{HEADER}VK0001,active,error,2,failed,engine,s,m,s,M\n\
                 VK0002,retired,,,,,s,,s,\n\
                 VK0003,active,error,2,failed,bootstrap,s,m,s,M\n\
                 VK0004,active,warn,1,,bootstrap engine,s,m,s,M\n"
            )
            .as_bytes(),
        )
        .unwrap()
    }

    fn occ(path: &str, code: &str, via_messages: bool) -> Occurrence {
        Occurrence {
            path: path.to_owned(),
            line: 1,
            code: code.to_owned(),
            via_messages,
        }
    }

    #[test]
    fn parses_status_and_sources() {
        let t = table();
        assert_eq!(t["VK0002"].status, Status::Retired);
        assert_eq!(t["VK0004"].sources, vec!["bootstrap", "engine"]);
    }

    #[test]
    fn rejects_unknown_status_and_duplicates() {
        let bad = format!("{HEADER}VK0001,draft,,,,,s,,s,\n");
        assert!(parse_table(bad.as_bytes()).is_err());
        let dup = format!("{HEADER}VK0001,retired,,,,,s,,s,\nVK0001,retired,,,,,s,,s,\n");
        assert!(parse_table(dup.as_bytes()).is_err());
    }

    #[test]
    fn scans_codes_and_messages_paths() {
        let text = "let _ = &messages::VK0001;\n// see VK0002, error[VK0003]: x\n\"VK0004\"";
        let found = scan_text("engine/a.rs", text);
        let got: Vec<(usize, &str, bool)> = found
            .iter()
            .map(|o| (o.line, o.code.as_str(), o.via_messages))
            .collect();
        assert_eq!(
            got,
            vec![
                (1, "VK0001", true),
                (2, "VK0002", false),
                (2, "VK0003", false),
                (3, "VK0004", false),
            ]
        );
    }

    #[test]
    fn ignores_tokens_that_are_not_codes() {
        let found = scan_text("x", "VK001 VK00011 XVK0001 VK0001a VK_0001 VK");
        assert!(found.is_empty(), "{found:?}");
    }

    #[test]
    fn active_codes_pass_and_engine_use_counts_only_via_messages() {
        let found = [
            occ("engine/a/src/lib.rs", "VK0001", true),
            occ("engine/a/src/lib.rs", "VK0004", false),
            occ("test/e2e/tests/x.rs", "VK0004", true),
        ];
        let report = check(&table(), &found, &[]);
        assert!(report.problems().is_empty());
        // VK0003 只屬 bootstrap，不算引擎該用的；VK0004 只在註解或 engine/ 外出現，還算沒用到。
        assert_eq!(report.unused, vec!["VK0004"]);
    }

    #[test]
    fn blocks_unregistered_and_retired_codes() {
        let found = [
            occ("engine/a.rs", "VK0099", false),
            occ("test/e2e/x.rs", "VK0002", false),
        ];
        let report = check(&table(), &found, &[]);
        assert_eq!(report.unregistered, vec![found[0].clone()]);
        assert_eq!(report.retired, vec![found[1].clone()]);
        assert_eq!(report.problems().len(), 2);
    }

    #[test]
    fn allow_lets_one_file_use_an_unregistered_code() {
        let allow = Allow {
            path: "engine/a.rs",
            code: "VK0099",
            reason: "test",
        };
        let found = [
            occ("engine/a.rs", "VK0099", false),
            occ("engine/b.rs", "VK0099", false),
        ];
        let report = check(&table(), &found, &[allow]);
        assert!(report.stale_allows.is_empty());
        assert_eq!(report.unregistered, vec![found[1].clone()]);
    }

    #[test]
    fn stale_or_needless_allows_are_blocked() {
        let unmatched = Allow {
            path: "engine/a.rs",
            code: "VK0099",
            reason: "gone",
        };
        let needless = Allow {
            path: "engine/a.rs",
            code: "VK0001",
            reason: "registered",
        };
        let found = [occ("engine/a.rs", "VK0001", true)];
        let report = check(&table(), &found, &[unmatched, needless]);
        assert_eq!(report.stale_allows, vec![unmatched, needless]);
    }
}
