//! 本機開發來源的正規化與檢查（engine/dev 的 `normalize`、`check_dir` 裡安裝目錄那一半，engine/sync 也照抄同一份；指令之間互不依賴，照抄）。
//!
//! `version.local.toml` 的工具覆寫是 `dev` 寫進去、正規化過的值：安裝目錄裡的是相對路徑，安裝目錄外的是
//! 開頭為 `..` 的相對路徑或絕對路徑（engine/dev 的「本機目錄」）。這裡照同一條規則以安裝目錄為準再正規化
//! 一次（手改過的值與 `dev` 認定同一個來源），只收安裝目錄裡的值（安裝目錄外的見模組說明「缺口」），再檢查
//! 目錄讀不讀得到、符不符合交付格式。

use std::ffi::OsStr;
use std::fs;
use std::io;
use std::path::{Component, Path};

/// 本機開發來源為什麼讀不到（VK0052 的 `<reason>`）。
pub type Problem = String;

/// 把覆寫的值以安裝目錄為準逐段正規化成 `/` 分隔的相對路徑（安裝目錄本身是 `.`）。只看字面，不碰檔案系統。
pub fn normalize(given: &OsStr) -> Result<String, Problem> {
    let Some(text) = given.to_str() else {
        return Err(format!(
            "the path is not UTF-8 ({})",
            given.to_string_lossy()
        ));
    };
    if text.is_empty() {
        return Err("the path is empty".to_owned());
    }
    let outside = || format!("the path is outside the install directory ({text})");
    let mut parts: Vec<&str> = Vec::new();
    for c in Path::new(text).components() {
        match c {
            Component::CurDir => {}
            Component::ParentDir => {
                parts.pop().ok_or_else(outside)?;
            }
            Component::Normal(seg) => parts.push(seg.to_str().ok_or_else(outside)?),
            Component::RootDir | Component::Prefix(_) => return Err(outside()),
        }
    }
    let joined = if parts.is_empty() {
        ".".to_owned()
    } else {
        parts.join("/")
    };
    if tools_just::is_local_dir(&joined) {
        Ok(joined)
    } else {
        Err(format!(
            "the path contains a quote, a backslash, or a control character ({text})"
        ))
    }
}

/// 檢查正規化後的本機目錄 `rel`（相對於 `root`）：每一段都不是 symlink、存在、最後是目錄，而且符合交付
/// 格式、交付了 `<repo>.just`。回傳它交付的全部 `<ns>`。
pub fn check_dir(root: &Path, rel: &str, repo: &str) -> Result<Vec<String>, Problem> {
    let mut at = root.to_path_buf();
    if rel != "." {
        for seg in rel.split('/') {
            at.push(seg);
            match fs::symlink_metadata(&at) {
                Ok(m) if m.file_type().is_symlink() => {
                    return Err(format!(
                        "the path goes through a symlink ({})",
                        at.strip_prefix(root).unwrap_or(&at).display()
                    ));
                }
                Ok(_) => {}
                Err(e) if e.kind() == io::ErrorKind::NotFound => {
                    return Err("the directory does not exist".to_owned());
                }
                Err(e) => return Err(e.to_string()),
            }
        }
    }
    if !at.is_dir() {
        return Err("it is not a directory".to_owned());
    }
    let ns = fetch::namespaces(&at).map_err(|e| e.to_string())?;
    if !ns.iter().any(|n| n == repo) {
        return Err(format!(
            "{}/{repo}{} is missing",
            fetch::JUST_DIR,
            fetch::JUST_EXT
        ));
    }
    Ok(ns)
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    #[test]
    fn normalizes_like_dev() {
        for (given, want) in [
            ("work/tool", "work/tool"),
            ("./work/./tool/", "work/tool"),
            ("work/x/../tool", "work/tool"),
            (".", "."),
        ] {
            assert_eq!(normalize(OsStr::new(given)).unwrap(), want, "{given}");
        }
        for bad in ["", "/abs", "../up", "it's"] {
            assert!(normalize(OsStr::new(bad)).is_err(), "{bad:?}");
        }
    }

    #[test]
    fn check_dir_reads_namespaces_and_requires_the_repo_file() {
        let tmp = tempfile::tempdir().unwrap();
        let root = tmp.path();
        assert_eq!(
            check_dir(root, "work/tool", "tool").unwrap_err(),
            "the directory does not exist"
        );
        fs::create_dir_all(root.join("work/tool/just")).unwrap();
        fs::write(root.join("work/tool/just/extra.just"), "").unwrap();
        assert!(
            check_dir(root, "work/tool", "tool")
                .unwrap_err()
                .ends_with("tool.just is missing")
        );
        fs::write(root.join("work/tool/just/tool.just"), "").unwrap();
        let mut ns = check_dir(root, "work/tool", "tool").unwrap();
        ns.sort();
        assert_eq!(ns, ["extra", "tool"]);
        fs::write(root.join("file"), "").unwrap();
        assert_eq!(
            check_dir(root, "file", "tool").unwrap_err(),
            "it is not a directory"
        );
    }
}
