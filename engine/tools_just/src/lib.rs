//! 入口檔 `.vendor_kit/gen/tools.just` 的內容（ADR-0004：`gen/tools.just` 每個 `<ns>` 一行；
//! 04 命名空間：工具 recipe 的呼叫是 `just <ns> …`）。
//!
//! - 一行是 `mod <ns> '../cache/<repo>/just/<ns>.just'`。`just <ns> …` 要的是 module，所以用 `mod`，
//!   不用 `import`（`import` 會把 recipe 併進上一層，沒有 `<ns>` 這一層）。
//! - 路徑相對於 `gen/tools.just` 本身所在的目錄：just 解析 `mod` 的路徑時以寫著那一行的檔為準，
//!   被 `import` 進來的檔也一樣（just 1.53.0 實測；1.33.0 待驗收層實測）。`cache/<repo>/` 是取件內容
//!   的根目錄（`fetch` 的暫存根目錄整份換進去），所以底下是 `just/<ns>.just`，沒有 `dist/`。
//! - `<repo>` 與 `<ns>` 都是 just 名稱（`[A-Za-z_][A-Za-z0-9_-]*`），放進單引號字串不必跳脫；
//!   不是 just 名稱就拒絕（[`Error`]），不產出 just 解析不了的檔。
//! - 依 `<ns>` 的位元組順序排列，同一組工具只有一種內容（ADR-0012）。同一個 `<ns>` 出現兩次
//!   （撞名，應該在 `fetch` 就擋下）也拒絕。沒有工具時內容是空的。
//! - 沒有檔頭或註解：檔的每一行都是一個 `<ns>`。
//!
//! 這裡只算內容，不寫檔；寫入由 `txn` 在 `cache/` 換好之後做。誰載入 `gen/tools.just`
//! （薄殼 `entry.just` 的模板）不在這裡。

use std::collections::BTreeMap;
use std::fmt;

/// 一個工具與它交付的全部 `<ns>`。
#[derive(Debug, Clone, Copy)]
pub struct Tool<'a> {
    pub repo: &'a str,
    pub namespaces: &'a [String],
}

/// 產不出入口檔。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Error {
    /// `<repo>` 不是 just 名稱。
    InvalidRepo(String),
    /// `<ns>` 不是 just 名稱。
    InvalidNamespace(String),
    /// 同一個 `<ns>` 由兩個工具交付。
    Duplicate {
        ns: String,
        first: String,
        second: String,
    },
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::InvalidRepo(r) => write!(f, "tool name {r:?} is not a just name"),
            Error::InvalidNamespace(n) => write!(f, "namespace {n:?} is not a just name"),
            Error::Duplicate { ns, first, second } => {
                write!(
                    f,
                    "namespace {ns} is delivered by both {first} and {second}"
                )
            }
        }
    }
}

impl std::error::Error for Error {}

/// just 的名稱：`[A-Za-z_][A-Za-z0-9_-]*`（與 `fetch::is_namespace` 同一條規則）。
fn is_name(s: &str) -> bool {
    let mut b = s.bytes();
    b.next()
        .is_some_and(|c| c.is_ascii_alphabetic() || c == b'_')
        && b.all(|c| c.is_ascii_alphanumeric() || c == b'_' || c == b'-')
}

/// 一個 `<ns>` 的那一行（含結尾 LF）。
pub fn line(repo: &str, ns: &str) -> String {
    format!("mod {ns} '../cache/{repo}/just/{ns}.just'\n")
}

/// 全部工具的入口檔內容。
pub fn render(tools: &[Tool]) -> Result<String, Error> {
    let mut by_ns: BTreeMap<&str, &str> = BTreeMap::new();
    for tool in tools {
        if !is_name(tool.repo) {
            return Err(Error::InvalidRepo(tool.repo.to_owned()));
        }
        for ns in tool.namespaces {
            if !is_name(ns) {
                return Err(Error::InvalidNamespace(ns.clone()));
            }
            if let Some(first) = by_ns.insert(ns, tool.repo) {
                return Err(Error::Duplicate {
                    ns: ns.clone(),
                    first: first.to_owned(),
                    second: tool.repo.to_owned(),
                });
            }
        }
    }
    Ok(by_ns.into_iter().map(|(ns, repo)| line(repo, ns)).collect())
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    fn ns(names: &[&str]) -> Vec<String> {
        names.iter().map(|s| (*s).to_owned()).collect()
    }

    #[test]
    fn one_line_per_namespace_sorted_by_namespace() {
        let a = ns(&["lint", "a_tool"]);
        let b = ns(&["base"]);
        let text = render(&[
            Tool {
                repo: "a_tool",
                namespaces: &a,
            },
            Tool {
                repo: "base",
                namespaces: &b,
            },
        ])
        .unwrap();
        assert_eq!(
            text,
            "mod a_tool '../cache/a_tool/just/a_tool.just'\n\
             mod base '../cache/base/just/base.just'\n\
             mod lint '../cache/a_tool/just/lint.just'\n"
        );
    }

    #[test]
    fn no_tools_is_empty() {
        assert_eq!(render(&[]).unwrap(), "");
    }

    #[test]
    fn duplicate_and_invalid_names_are_rejected() {
        let a = ns(&["x"]);
        let err = render(&[
            Tool {
                repo: "a",
                namespaces: &a,
            },
            Tool {
                repo: "b",
                namespaces: &a,
            },
        ])
        .unwrap_err();
        assert_eq!(
            err,
            Error::Duplicate {
                ns: "x".into(),
                first: "a".into(),
                second: "b".into()
            }
        );
        let bad = ns(&["x'y"]);
        assert_eq!(
            render(&[Tool {
                repo: "a",
                namespaces: &bad
            }])
            .unwrap_err(),
            Error::InvalidNamespace("x'y".into())
        );
        assert_eq!(
            render(&[Tool {
                repo: "../a",
                namespaces: &a
            }])
            .unwrap_err(),
            Error::InvalidRepo("../a".into())
        );
    }
}
