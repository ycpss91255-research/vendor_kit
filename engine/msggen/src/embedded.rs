//! 組好的 `bootstrap.sh` 對訊息表的「內嵌清單 ⊆ 真本」檢查（#372 的 N1、ADR-0005:24）。
//!
//! - 內嵌的訊息片段要跟訊息表這次產出的 [`crate::render::bash`] 逐位元組相同（片段是舊表產的就擋）。
//! - 從入口走得到的函式裡用到的原因代碼，都要是訊息表裡 active、`source` 含 `bootstrap` 的代碼。
//!   bootstrap.sh 跟 VK recipe 共用 `launcher/` 的檔，裡面也有只在 VK recipe 走到的函式與代碼
//!   （例如 `launch.sh` 判介面版的 VK0009），所以不能把整份檔的代碼都算進來。
//!
//! 走法（只認 `launcher/` 的寫法，認不出的不猜、照算）：
//! - 函式定義是頂格的 `name() {`，到頂格的 `}` 為止；其他行是頂層。整行註解（含 shebang）不看。
//! - 起點是頂層各行提到的函式名；函式本文提到的函式名再往下走。入口 [`ENTRY`] 一定要有定義。
//! - 用到的代碼是前後都不接 `[A-Za-z0-9_]` 的 `VK` 加四位數字；前面緊接 `draft ` 的是過渡做法裡的草稿碼
//!   （「reason code pending (draft VKnnnn, Nxx)」），不是用到的代碼。
//! - 行尾註解不分辨，裡面的代碼也算用到（寧可擋錯，不放過）。

use std::collections::{BTreeMap, BTreeSet};

use crate::render;
use crate::table::{Row, Source};

/// bootstrap.sh 的入口函式（`launcher/bootstrap_main.sh`）。
pub const ENTRY: &str = "vk_bootstrap_main";

const DRAFT: &str = "draft ";

/// 檢查組好的 bootstrap.sh；全部的問題一次列出，一個一行。
pub fn check(script: &str, rows: &[Row]) -> Result<(), String> {
    let fragment = render::bash(rows);
    let Some(at) = script.find(&fragment) else {
        return Err("the embedded message fragment differs from the message table".to_owned());
    };
    let rest = format!("{}{}", &script[..at], &script[at + fragment.len()..]);
    let used = used_codes(&rest)?;
    let mut problems = Vec::new();
    for code in &used {
        match rows.iter().find(|r| r.code == *code) {
            None => problems.push(format!("{code} is not an active code in the message table")),
            Some(row) if !row.sources.contains(&Source::Bootstrap) => {
                problems.push(format!(
                    "{code} is used, but its source does not include bootstrap"
                ));
            }
            Some(_) => {}
        }
    }
    if problems.is_empty() {
        Ok(())
    } else {
        Err(problems.join("\n"))
    }
}

/// 從頂層與入口走得到的函式裡用到的代碼。
fn used_codes(script: &str) -> Result<BTreeSet<String>, String> {
    let mut functions: BTreeMap<&str, Vec<&str>> = BTreeMap::new();
    let mut top = Vec::new();
    let mut current: Option<&str> = None;
    for line in script.lines() {
        if line.trim_start().starts_with('#') {
            continue;
        }
        if let Some(name) = current {
            if line == "}" {
                current = None;
            } else {
                functions.entry(name).or_default().push(line);
            }
            continue;
        }
        if let Some(name) = function_start(line) {
            if functions.insert(name, Vec::new()).is_some() {
                return Err(format!("function {name} is defined twice"));
            }
            current = Some(name);
            continue;
        }
        top.push(line);
    }
    if let Some(name) = current {
        return Err(format!("function {name} is not closed"));
    }
    if !functions.contains_key(ENTRY) {
        return Err(format!("the entry function {ENTRY} is not defined"));
    }

    let mut codes = BTreeSet::new();
    let mut seen = BTreeSet::new();
    let mut todo: Vec<&str> = Vec::new();
    for line in &top {
        codes.extend(codes_in(line));
        todo.extend(words(line).filter(|w| functions.contains_key(w)));
    }
    todo.push(ENTRY);
    while let Some(name) = todo.pop() {
        if !seen.insert(name) {
            continue;
        }
        for line in functions.get(name).into_iter().flatten() {
            codes.extend(codes_in(line));
            todo.extend(words(line).filter(|w| functions.contains_key(w)));
        }
    }
    Ok(codes)
}

/// 頂格的 `name() {` 回 name。
fn function_start(line: &str) -> Option<&str> {
    let name = line.strip_suffix("() {")?;
    let mut bytes = name.bytes();
    let first = bytes.next()?;
    (is_word_start(first) && bytes.all(is_word)).then_some(name)
}

fn is_word_start(b: u8) -> bool {
    b.is_ascii_alphabetic() || b == b'_'
}

fn is_word(b: u8) -> bool {
    b.is_ascii_alphanumeric() || b == b'_'
}

/// 行裡的識別字（`[A-Za-z_][A-Za-z0-9_]*`；數字開頭的片段不算）。
fn words(line: &str) -> impl Iterator<Item = &str> {
    line.split(|c: char| !(c.is_ascii_alphanumeric() || c == '_'))
        .filter(|w| w.bytes().next().is_some_and(is_word_start))
}

/// 行裡用到的代碼（見模組說明）。
fn codes_in(line: &str) -> Vec<String> {
    let bytes = line.as_bytes();
    let mut out = Vec::new();
    let mut i = 0;
    while let Some(off) = line[i..].find("VK") {
        let at = i + off;
        let end = at + 6;
        i = at + 2;
        if end > bytes.len() || !bytes[at + 2..end].iter().all(u8::is_ascii_digit) {
            continue;
        }
        if at > 0 && is_word(bytes[at - 1]) {
            continue;
        }
        if bytes.get(end).is_some_and(|b| is_word(*b)) {
            continue;
        }
        if line[..at].ends_with(DRAFT) {
            continue;
        }
        out.push(line[at..end].to_owned());
    }
    out
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;
    use crate::table::Level;

    fn row(code: &str, sources: Vec<Source>) -> Row {
        Row {
            code: code.into(),
            level: Level::Error,
            disposition: None,
            sources,
            message_en: format!("{code} text."),
        }
    }

    fn rows() -> Vec<Row> {
        vec![
            row("VK0002", vec![Source::Bootstrap, Source::Engine]),
            row("VK0009", vec![Source::Launcher]),
            row("VK0036", vec![Source::Bootstrap, Source::Launcher]),
            row(
                "VK0056",
                vec![Source::Bootstrap, Source::Engine, Source::Launcher],
            ),
        ]
    }

    /// 片段放在 shebang 與內嵌引用之後，後面接函式；body 是片段之後的部分。
    fn script(rows: &[Row], body: &str) -> String {
        format!(
            "#!/usr/bin/env bash\nvk_bootstrap_engine='e'\n{}{body}",
            render::bash(rows)
        )
    }

    const BASE: &str = "\
vk_pending='reason code pending (draft VK0009, N13)'
vk_fail() {
    vk_diag VK0036 # 只在 bootstrap 用
}
# vk_diag VK0009 在註解裡不算
vk_interface() {
    vk_diag VK0009
}
vk_bootstrap_main() {
    vk_fail || vk_diag VK0002
}
if [[ ${BASH_SOURCE[0]} == \"$0\" ]]; then
    vk_bootstrap_main \"$@\"
fi
";

    #[test]
    fn unreachable_launcher_codes_and_drafts_pass() {
        let rows = rows();
        check(&script(&rows, BASE), &rows).unwrap();
        let used = used_codes(BASE).unwrap();
        assert_eq!(used.into_iter().collect::<Vec<_>>(), ["VK0002", "VK0036"]);
    }

    #[test]
    fn a_reachable_launcher_only_code_fails() {
        let rows = rows();
        let body = BASE.replace("vk_fail || vk_diag VK0002", "vk_interface");
        let err = check(&script(&rows, &body), &rows).unwrap_err();
        assert_eq!(
            err,
            "VK0009 is used, but its source does not include bootstrap"
        );
    }

    #[test]
    fn a_code_reached_from_top_level_counts() {
        let rows = rows();
        let body = format!("{BASE}vk_interface\n");
        assert!(check(&script(&rows, &body), &rows).is_err());
    }

    #[test]
    fn a_code_missing_from_the_table_fails() {
        let rows = rows();
        let body = BASE.replace("vk_diag VK0002", "vk_diag VK0002 || vk_diag VK0004");
        let err = check(&script(&rows, &body), &rows).unwrap_err();
        assert_eq!(err, "VK0004 is not an active code in the message table");
    }

    #[test]
    fn a_stale_fragment_fails() {
        let rows = rows();
        let text = script(&rows, BASE).replace("VK0036 text.", "Old text.");
        let err = check(&text, &rows).unwrap_err();
        assert!(err.contains("fragment"), "{err}");
    }

    #[test]
    fn the_entry_must_be_defined() {
        let rows = rows();
        let body = BASE.replace("vk_bootstrap_main() {", "vk_other() {");
        assert!(check(&script(&rows, &body), &rows).is_err());
        assert!(used_codes("f() {\n").is_err());
    }

    #[test]
    fn code_tokens_need_word_boundaries() {
        assert_eq!(codes_in("vk_msg_VK0009_level=error"), Vec::<String>::new());
        assert_eq!(codes_in("VK00091 xVK0009 VK009"), Vec::<String>::new());
        assert_eq!(codes_in("(draft VK0009, N1) VK0056"), ["VK0056"]);
        assert_eq!(codes_in("\"VK0031\""), ["VK0031"]);
    }
}
