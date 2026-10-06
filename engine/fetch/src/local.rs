//! 本機開發來源的正規化與檢查（GLOSSARY 本機開發來源；04 本機覆寫）：`dev`、`sync`、`upgrade`、
//! `add`、`remove` 共用。
//!
//! `version.local.toml` 的工具覆寫是 `dev <repo> -p <dir>` 寫進去、正規化過的值。讀它的指令照同一條規則
//! 以安裝目錄為準再正規化一次（[`normalize`]，手改過的值與 `dev` 認定同一個來源），再檢查目錄讀不讀得到、
//! 符不符合交付格式（[`check_dir`]）。
//!
//! # 安裝目錄裡與安裝目錄外（[`Source`]）
//!
//! - 落在安裝目錄裡：相對路徑沒跑出安裝目錄，或絕對路徑在主機上的安裝目錄（`--host-root`）底下。寫成 `/`
//!   分隔的相對路徑（整個是安裝目錄本身時寫 `.`），引擎直接讀安裝目錄底下那個目錄。
//! - 相對路徑以 `..` 跑出安裝目錄：寫成開頭是 `..` 的相對路徑，照使用者給的形式留相對路徑。
//! - 絕對路徑、不在 `--host-root` 底下：寫成正規化後的絕對路徑。
//!
//! 後兩種引擎容器看不到，由呼叫端請啟動器 `stage-dir` 把目錄複製進 `in/<slot>`（slot 名是
//! [`STAGE_SLOT_PREFIX`] 加這次執行裡的序號），再以 [`check_dir`] 檢查那份複本（`rel` 給 `.`）。送給啟動器的
//! 主機路徑是 [`Source::host_path`]：絕對路徑原樣；相對路徑是 `<--host-root>/<值>`，開頭的 `..` 不在引擎
//! 這邊消掉，跟 just 從 `.vendor_kit/gen/` 解析入口檔那一行一樣，都由主機照實際目錄解析，驗的跟載入的是
//! 同一個目錄。啟動器回 `failed` 時用 [`copy_failed`] 的說明。
//!
//! 這裡只看字面與讀檔，不寫檔、不送 `plan` 的 op（往返由呼叫端做，同這個 crate 的取件驗證）。

use std::ffi::OsStr;
use std::fs;
use std::io;
use std::path::{Component, Path};

use crate::{JUST_DIR, JUST_EXT, namespaces};

/// 安裝目錄外的本機開發來源經 `stage-dir` 放進 `in/` 的 slot 名前綴，後接這次執行裡的序號（`dev1`…）。
pub const STAGE_SLOT_PREFIX: &str = "dev";

/// 本機開發來源為什麼不能用。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PathProblem {
    /// 不存在、不是目錄或不符合交付格式（`dev` 的 VK0051、其他指令的 VK0052 的 `<reason>`）。
    Unusable(String),
    /// 契約或協定沒定的情況：值不是 UTF-8；含 `'`、`"`、反斜線或控制字元（放不進 just 單引號字串或
    /// `version.local.toml` 的無跳脫字串）；正規化後是根目錄 `/`；安裝目錄裡的路徑上有 symlink（容器裡解不出
    /// 主機上的目標）。值是說明。
    Gap(String),
}

impl PathProblem {
    /// 說明本身（不分哪一種）。
    pub fn reason(self) -> String {
        match self {
            PathProblem::Unusable(r) | PathProblem::Gap(r) => r,
        }
    }
}

/// 正規化後的本機開發來源（模組說明「安裝目錄裡與安裝目錄外」）。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Source {
    /// 落在安裝目錄裡：`/` 分隔的相對路徑，安裝目錄本身是 `.`。引擎直接讀。
    Inside(String),
    /// 安裝目錄外：開頭是 `..` 的相對路徑，或主機上的絕對路徑。經 `stage-dir` 讀。
    Outside(String),
}

impl Source {
    /// 存進 `version.local.toml`、寫進入口檔的值。
    pub fn as_str(&self) -> &str {
        match self {
            Source::Inside(s) | Source::Outside(s) => s,
        }
    }

    /// 安裝目錄外的來源請啟動器複製時用的主機路徑：絕對路徑原樣，相對路徑接在 `host_root` 後面
    /// （開頭的 `..` 留給主機解析）。安裝目錄裡的回 `None`。
    pub fn host_path(&self, host_root: &str) -> Option<String> {
        match self {
            Source::Inside(_) => None,
            Source::Outside(p) if p.starts_with('/') => Some(p.clone()),
            Source::Outside(p) => Some(format!("{}/{p}", host_root.trim_end_matches('/'))),
        }
    }
}

/// 只看字面逐段正規化：`.` 略過，`..` 往上一層（根目錄的上一層還是根目錄）。回傳是不是絕對路徑、開頭
/// 跑出起點的 `..` 層數，與剩下的一般路徑段。
fn lexical(path: &Path) -> Option<(bool, usize, Vec<&str>)> {
    let mut absolute = false;
    let mut ups = 0;
    let mut parts: Vec<&str> = Vec::new();
    for c in path.components() {
        match c {
            Component::RootDir => absolute = true,
            Component::CurDir => {}
            Component::ParentDir => {
                if parts.pop().is_none() && !absolute {
                    ups += 1;
                }
            }
            Component::Normal(seg) => parts.push(seg.to_str()?),
            Component::Prefix(_) => return None,
        }
    }
    Some((absolute, ups, parts))
}

/// 把本機開發來源的路徑正規化（模組說明）：相對路徑以安裝目錄為準，絕對路徑在 `host_root` 底下時換成
/// 相對於安裝目錄的寫法。只看字面，不碰檔案系統。
pub fn normalize(given: &OsStr, host_root: &str) -> Result<Source, PathProblem> {
    let Some(text) = given.to_str() else {
        return Err(PathProblem::Gap(format!(
            "a local source path that is not UTF-8 ({})",
            given.to_string_lossy()
        )));
    };
    if text.is_empty() {
        return Err(PathProblem::Unusable("the path is empty".to_owned()));
    }
    let unfit = || {
        PathProblem::Gap(format!(
            "a local source path containing a quote, a double quote, a backslash, or a control \
             character, or the root directory ({text})"
        ))
    };
    let (absolute, ups, parts) = lexical(Path::new(text)).ok_or_else(unfit)?;
    let inside = |parts: &[&str]| {
        if parts.is_empty() {
            ".".to_owned()
        } else {
            parts.join("/")
        }
    };
    let source = if absolute {
        let root = lexical(Path::new(host_root))
            .filter(|(abs, _, _)| *abs)
            .map(|(_, _, root)| root);
        match root {
            Some(root) if parts.starts_with(&root) => Source::Inside(inside(&parts[root.len()..])),
            _ => Source::Outside(format!("/{}", parts.join("/"))),
        }
    } else if ups == 0 {
        Source::Inside(inside(&parts))
    } else {
        let mut segs = vec![".."; ups];
        segs.extend(parts);
        Source::Outside(segs.join("/"))
    };
    let value = source.as_str();
    if tools_just::is_local_dir(value) && !value.contains('"') {
        Ok(source)
    } else {
        Err(unfit())
    }
}

/// 檢查正規化後的本機目錄 `rel`（相對於 `root`）：每一段都不是 symlink、存在、最後是目錄，而且符合交付
/// 格式、交付了 `<repo>.just`。回傳它交付的全部 `<ns>`。
pub fn check_dir(root: &Path, rel: &str, repo: &str) -> Result<Vec<String>, PathProblem> {
    let mut at = root.to_path_buf();
    if rel != "." {
        for seg in rel.split('/') {
            at.push(seg);
            match fs::symlink_metadata(&at) {
                Ok(m) if m.file_type().is_symlink() => {
                    return Err(PathProblem::Gap(format!(
                        "a local source path through a symlink ({})",
                        at.strip_prefix(root).unwrap_or(&at).display()
                    )));
                }
                Ok(_) => {}
                Err(e) if e.kind() == io::ErrorKind::NotFound => {
                    return Err(PathProblem::Unusable(
                        "the directory does not exist".to_owned(),
                    ));
                }
                Err(e) => return Err(PathProblem::Unusable(e.to_string())),
            }
        }
    }
    if !at.is_dir() {
        return Err(PathProblem::Unusable("it is not a directory".to_owned()));
    }
    let ns = namespaces(&at).map_err(|e| PathProblem::Unusable(e.to_string()))?;
    if !ns.iter().any(|n| n == repo) {
        return Err(PathProblem::Unusable(format!(
            "{JUST_DIR}/{repo}{JUST_EXT} is missing"
        )));
    }
    Ok(ns)
}

/// 啟動器回 `stage-dir` 的 `failed <rc>` 時的說明：啟動器分不出是不存在、不是目錄還是讀不到。
pub fn copy_failed(rc: u8) -> PathProblem {
    PathProblem::Unusable(format!(
        "the launcher could not copy it (exit {rc}): it does not exist, \
         is not a directory, or cannot be read"
    ))
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    const HOST_ROOT: &str = "/h/proj";

    #[test]
    fn normalize_resolves_against_the_install_directory() {
        let n = |s: &str| normalize(OsStr::new(s), HOST_ROOT);
        let inside = |s: &str| Source::Inside(s.to_owned());
        let outside = |s: &str| Source::Outside(s.to_owned());
        assert_eq!(n("dev/tool").unwrap(), inside("dev/tool"));
        assert_eq!(n("./dev//tool/").unwrap(), inside("dev/tool"));
        assert_eq!(n("a/../b").unwrap(), inside("b"));
        assert_eq!(n("work/x/../tool").unwrap(), inside("work/tool"));
        assert_eq!(n(".").unwrap(), inside("."));
        assert_eq!(n("/h/proj/").unwrap(), inside("."));
        assert_eq!(n("/h/proj/./a/../dev").unwrap(), inside("dev"));
        assert_eq!(n("..").unwrap(), outside(".."));
        assert_eq!(n("a/../../b/").unwrap(), outside("../b"));
        assert_eq!(n("../../x/./y").unwrap(), outside("../../x/y"));
        // 相對路徑跑出去又繞回來，照樣算安裝目錄外（`..` 留給主機解析，不在這裡消掉）。
        assert_eq!(n("../proj/dev").unwrap(), outside("../proj/dev"));
        assert_eq!(n("/abs//x/").unwrap(), outside("/abs/x"));
        assert_eq!(n("/h/projx").unwrap(), outside("/h/projx"));
        assert_eq!(n("/../srv").unwrap(), outside("/srv"));
        assert_eq!(
            n("").unwrap_err(),
            PathProblem::Unusable("the path is empty".to_owned())
        );
        for bad in ["/", "/..", "it's", "a\\b", "../a\"b", "/x\ty"] {
            assert!(matches!(n(bad), Err(PathProblem::Gap(_))), "{bad:?}");
        }
    }

    #[test]
    fn host_path_is_only_for_outside_sources() {
        let outside = |s: &str| Source::Outside(s.to_owned());
        assert_eq!(
            outside("/abs").host_path(HOST_ROOT).as_deref(),
            Some("/abs")
        );
        assert_eq!(
            outside("../b").host_path(HOST_ROOT).as_deref(),
            Some("/h/proj/../b")
        );
        assert_eq!(
            outside("../b").host_path("/h/proj/").as_deref(),
            Some("/h/proj/../b")
        );
        assert_eq!(Source::Inside("b".to_owned()).host_path(HOST_ROOT), None);
    }

    #[test]
    fn check_dir_reads_namespaces_and_requires_the_repo_file() {
        let tmp = tempfile::tempdir().unwrap();
        let root = tmp.path();
        assert_eq!(
            check_dir(root, "work/tool", "tool").unwrap_err(),
            PathProblem::Unusable("the directory does not exist".to_owned())
        );
        fs::create_dir_all(root.join("work/tool/just")).unwrap();
        fs::write(root.join("work/tool/just/extra.just"), "").unwrap();
        assert!(
            check_dir(root, "work/tool", "tool")
                .unwrap_err()
                .reason()
                .ends_with("tool.just is missing")
        );
        fs::write(root.join("work/tool/just/tool.just"), "").unwrap();
        let mut ns = check_dir(root, "work/tool", "tool").unwrap();
        ns.sort();
        assert_eq!(ns, ["extra", "tool"]);
        // 複本的根目錄本身（`stage-dir` 之後）。
        let mut ns = check_dir(&root.join("work/tool"), ".", "tool").unwrap();
        ns.sort();
        assert_eq!(ns, ["extra", "tool"]);
        fs::write(root.join("file"), "").unwrap();
        assert_eq!(
            check_dir(root, "file", "tool").unwrap_err(),
            PathProblem::Unusable("it is not a directory".to_owned())
        );
    }

    #[cfg(unix)]
    #[test]
    fn check_dir_refuses_a_symlink_on_the_path() {
        let tmp = tempfile::tempdir().unwrap();
        let root = tmp.path();
        fs::create_dir_all(root.join("real/just")).unwrap();
        fs::write(root.join("real/just/tool.just"), "").unwrap();
        std::os::unix::fs::symlink(root.join("real"), root.join("link")).unwrap();
        assert!(matches!(
            check_dir(root, "link", "tool"),
            Err(PathProblem::Gap(_))
        ));
    }

    #[test]
    fn copy_failed_names_the_exit_code() {
        assert!(copy_failed(3).reason().contains("(exit 3)"));
    }
}
