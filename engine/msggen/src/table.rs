//! 讀訊息表並驗證格式（03 訊息「訊息表怎麼讀」）。

use std::collections::HashMap;

use message_types::{Disposition, Level, Source};

/// 一列使用中的代碼；停用的列只參與代碼排序檢查，不產生輸出。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Row {
    pub code: String,
    pub level: Level,
    pub disposition: Option<Disposition>,
    pub sources: Vec<Source>,
    pub message_en: String,
}

const BOM: &[u8] = b"\xEF\xBB\xBF";
const COLUMNS: [&str; 7] = [
    "code",
    "status",
    "level",
    "exit_code",
    "disposition",
    "source",
    "message.en",
];

/// 解析整份 CSV；任何不合格式的地方都回錯，不猜。
pub fn parse(bytes: &[u8]) -> Result<Vec<Row>, String> {
    let body = bytes.strip_prefix(BOM).unwrap_or(bytes);
    let mut reader = csv::ReaderBuilder::new()
        .has_headers(true)
        .from_reader(body);
    let headers = reader
        .headers()
        .map_err(|e| format!("cannot read header: {e}"))?
        .clone();
    let index: HashMap<&str, usize> = headers.iter().enumerate().map(|(i, h)| (h, i)).collect();
    let mut col = HashMap::new();
    for name in COLUMNS {
        let i = index
            .get(name)
            .ok_or_else(|| format!("missing column: {name}"))?;
        col.insert(name, *i);
    }

    let mut rows = Vec::new();
    let mut previous: Option<String> = None;
    for (n, record) in reader.records().enumerate() {
        let line = n + 2;
        let record = record.map_err(|e| format!("row {line}: {e}"))?;
        let field = |name: &str| -> &str {
            col.get(name)
                .and_then(|i| record.get(*i))
                .unwrap_or_default()
        };
        let code = field("code").to_owned();
        if !is_code(&code) {
            return Err(format!("row {line}: invalid code {code:?}"));
        }
        if let Some(prev) = &previous
            && code <= *prev
        {
            return Err(format!("row {line}: {code} is not after {prev}"));
        }
        previous = Some(code.clone());
        match field("status") {
            "retired" => continue,
            "active" => {}
            other => return Err(format!("{code}: invalid status {other:?}")),
        }
        let level = match field("level") {
            "warn" => Level::Warn,
            "error" => Level::Error,
            "fatal" => Level::Fatal,
            other => return Err(format!("{code}: invalid level {other:?}")),
        };
        if field("exit_code") != level.exit_code().to_string() {
            return Err(format!(
                "{code}: exit_code {:?} does not match level",
                field("exit_code")
            ));
        }
        let disposition = match field("disposition") {
            "" => None,
            "pending" => Some(Disposition::Pending),
            "failed" => Some(Disposition::Failed),
            other => return Err(format!("{code}: invalid disposition {other:?}")),
        };
        let sources = parse_sources(field("source")).map_err(|e| format!("{code}: {e}"))?;
        let message_en = field("message.en").to_owned();
        if message_en.is_empty() || message_en.contains('\r') {
            return Err(format!("{code}: message.en must be nonempty and LF-only"));
        }
        rows.push(Row {
            code,
            level,
            disposition,
            sources,
            message_en,
        });
    }
    Ok(rows)
}

fn is_code(s: &str) -> bool {
    s.len() == 6 && s.starts_with("VK") && s[2..].bytes().all(|b| b.is_ascii_digit())
}

fn parse_sources(s: &str) -> Result<Vec<Source>, String> {
    let mut out = Vec::new();
    for word in s.split(' ') {
        let src = match word {
            "bootstrap" => Source::Bootstrap,
            "engine" => Source::Engine,
            "launcher" => Source::Launcher,
            "test" => Source::Test,
            other => return Err(format!("invalid source {other:?}")),
        };
        if out.last().is_some_and(|last| *last >= src) {
            return Err(format!("source {s:?} is not in the fixed order"));
        }
        out.push(src);
    }
    Ok(out)
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    const HEADER: &str = "\u{feff}code,status,level,exit_code,disposition,source,situation.zh-TW,message.zh-TW,situation.en,message.en\n";

    fn table(rows: &str) -> Result<Vec<Row>, String> {
        parse(format!("{HEADER}{rows}").as_bytes())
    }

    #[test]
    fn reads_active_rows_and_skips_retired() {
        let rows = table(
            "VK0001,active,error,2,failed,bootstrap engine,s,m,s,\"Line one.\nLine two.\"\n\
             VK0002,retired,,,,,s,,s,\n",
        )
        .unwrap();
        assert_eq!(rows.len(), 1);
        assert_eq!(rows[0].sources, vec![Source::Bootstrap, Source::Engine]);
        assert_eq!(rows[0].message_en, "Line one.\nLine two.");
    }

    #[test]
    fn rejects_exit_code_that_does_not_match_level() {
        assert!(table("VK0001,active,warn,2,,engine,s,m,s,M\n").is_err());
    }

    #[test]
    fn rejects_codes_out_of_order() {
        assert!(
            table("VK0002,active,warn,1,,engine,s,m,s,M\nVK0001,active,warn,1,,engine,s,m,s,M\n")
                .is_err()
        );
    }

    #[test]
    fn rejects_sources_out_of_order() {
        assert!(table("VK0001,active,warn,1,,engine bootstrap,s,m,s,M\n").is_err());
    }

    #[test]
    fn real_table_parses() {
        let path = concat!(
            env!("CARGO_MANIFEST_DIR"),
            "/../../doc/contract/reason_codes.csv"
        );
        let rows = parse(&std::fs::read(path).unwrap()).unwrap();
        assert!(rows.iter().any(|r| r.code == "VK0024"));
    }
}
