//! `--registry-token-file <path>` 的位置判定。照抄 engine/update 的 `locate`：指令之間互不依賴。

use std::ffi::OsStr;
use std::os::unix::ffi::OsStrExt;
use std::path::{Component, Path, PathBuf};

/// token 檔路徑只看字面正規化後的位置（模組說明「registry token 檔」）。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TokenPath {
    /// 落在安裝目錄裡：相對於安裝目錄的路徑（安裝目錄本身是空路徑）。
    Inside(PathBuf),
    /// 在安裝目錄外：請啟動器 `stage` 時送的主機路徑。
    Outside(Vec<u8>),
}

/// 判 token 檔在安裝目錄裡還是外（只看字面：`.` 略過、`..` 往上一層，不碰檔案系統）。相對路徑以安裝目錄
/// 為準；絕對路徑在 `host_root` 底下時換成相對於安裝目錄的寫法。
pub fn locate(given: &OsStr, host_root: &str) -> TokenPath {
    fn lexical(path: &Path) -> (bool, usize, Vec<&OsStr>) {
        let (mut absolute, mut ups, mut parts) = (false, 0, Vec::new());
        for c in path.components() {
            match c {
                Component::RootDir => absolute = true,
                Component::CurDir | Component::Prefix(_) => {}
                Component::ParentDir => {
                    if parts.pop().is_none() && !absolute {
                        ups += 1;
                    }
                }
                Component::Normal(seg) => parts.push(seg),
            }
        }
        (absolute, ups, parts)
    }
    let join = |parts: &[&OsStr]| parts.iter().collect::<PathBuf>();
    let (absolute, ups, parts) = lexical(Path::new(given));
    if absolute {
        let (_, _, root) = lexical(Path::new(host_root));
        if parts.starts_with(&root) {
            return TokenPath::Inside(join(&parts[root.len()..]));
        }
        let mut host = Vec::new();
        for p in &parts {
            host.push(b'/');
            host.extend_from_slice(p.as_bytes());
        }
        if host.is_empty() {
            host.push(b'/');
        }
        return TokenPath::Outside(host);
    }
    if ups == 0 {
        return TokenPath::Inside(join(&parts));
    }
    let mut host = host_root.trim_end_matches('/').as_bytes().to_vec();
    host.push(b'/');
    host.extend_from_slice(given.as_bytes());
    TokenPath::Outside(host)
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    #[test]
    fn token_paths_are_located_against_the_install_dir() {
        let at = |s: &str| locate(OsStr::new(s), "/h/proj");
        assert_eq!(at("secrets/ghcr"), TokenPath::Inside("secrets/ghcr".into()));
        assert_eq!(at("./a/../ghcr"), TokenPath::Inside("ghcr".into()));
        assert_eq!(at("/h/proj/s/t"), TokenPath::Inside("s/t".into()));
        assert_eq!(at("/h/home/t"), TokenPath::Outside(b"/h/home/t".to_vec()));
        assert_eq!(at("../t"), TokenPath::Outside(b"/h/proj/../t".to_vec()));
    }
}
