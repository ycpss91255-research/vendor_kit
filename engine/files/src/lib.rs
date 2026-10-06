//! 檔案基礎操作：原子寫入、sha256 指紋、排序走訪。
//!
//! - 原子寫入：先寫同目錄的 `.tmp.*`，fsync、明確關檔後 rename 成目標檔，再 fsync 目錄；
//!   關檔錯誤由呼叫回傳，不靠 `Drop`（ADR-0014）。任何一步失敗都刪掉暫存檔，目標檔不會變成半份。
//! - 指紋：整檔 sha256，以及 CRLF→LF 正規化後的 sha256（ADR-0003、ADR-0012）；正規化後的內容本身由
//!   [`normalize_crlf`] 給，兩者的正規化規則相同。
//! - 走訪：回傳根目錄下所有一般檔的相對路徑，按整條相對路徑的位元組排序，不隨 locale（ADR-0012），
//!   也不靠 `HashMap` 的順序（ADR-0014）。
//! - symlink 第一版禁止（scope_roadmap）：寫入目標、走訪根目錄或走訪途中遇到 symlink 都回錯誤。
//!
//! 錯誤一律用 [`Error`] 回傳，這裡不印診斷；要印什麼由呼叫端經 `diagnostics` 決定。

use std::borrow::Cow;
use std::ffi::OsString;
use std::fmt;
use std::fs::{self, File, OpenOptions};
use std::io::{self, Write};
use std::os::unix::ffi::OsStrExt;
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicU64, Ordering};

use sha2::{Digest, Sha256};

/// 失敗時正在做的動作。
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Op {
    /// 讀目標或走訪項目的檔案資訊（不跟隨 symlink）。
    Stat,
    /// 建立暫存檔。
    CreateTemp,
    /// 寫入暫存檔。
    Write,
    /// 設定暫存檔的權限（沿用既有目標檔的權限）。
    SetPermissions,
    /// fsync 檔案或目錄。
    Sync,
    /// 關檔。
    Close,
    /// 把暫存檔 rename 成目標檔。
    Rename,
    /// 開啟目錄（fsync 用）。
    OpenDir,
    /// 讀目錄內容。
    ReadDir,
}

impl fmt::Display for Op {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let s = match self {
            Op::Stat => "stat",
            Op::CreateTemp => "create temp file",
            Op::Write => "write",
            Op::SetPermissions => "set permissions",
            Op::Sync => "fsync",
            Op::Close => "close",
            Op::Rename => "rename",
            Op::OpenDir => "open directory",
            Op::ReadDir => "read directory",
        };
        f.write_str(s)
    }
}

/// 這個 crate 的錯誤。
#[derive(Debug)]
pub enum Error {
    /// 系統呼叫失敗。
    Io {
        op: Op,
        path: PathBuf,
        source: io::Error,
    },
    /// 遇到 symlink（第一版禁止）。
    Symlink { path: PathBuf },
    /// 走訪時遇到既不是一般檔也不是目錄的項目（FIFO、socket、裝置檔）。
    NotRegular { path: PathBuf },
    /// 寫入目標沒有檔名（例如以 `/` 或 `..` 結尾）。
    NoFileName { path: PathBuf },
}

impl Error {
    fn io(op: Op, path: &Path, source: io::Error) -> Self {
        Error::Io {
            op,
            path: path.to_path_buf(),
            source,
        }
    }

    /// 出錯的路徑。
    pub fn path(&self) -> &Path {
        match self {
            Error::Io { path, .. }
            | Error::Symlink { path }
            | Error::NotRegular { path }
            | Error::NoFileName { path } => path,
        }
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Io { op, path, source } => {
                write!(f, "{op} {}: {source}", path.display())
            }
            Error::Symlink { path } => write!(f, "symlink not allowed: {}", path.display()),
            Error::NotRegular { path } => {
                write!(f, "not a regular file or directory: {}", path.display())
            }
            Error::NoFileName { path } => write!(f, "no file name: {}", path.display()),
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Error::Io { source, .. } => Some(source),
            _ => None,
        }
    }
}

pub type Result<T> = std::result::Result<T, Error>;

// ---------------------------------------------------------------------------
// 原子寫入

/// 同一個行程內的暫存檔序號，讓暫存檔名不重複。
static TEMP_SEQ: AtomicU64 = AtomicU64::new(0);

/// 建暫存檔撞名時的重試次數。
const TEMP_ATTEMPTS: u32 = 16;

/// 把 `contents` 原子寫到 `path`：成功時目標檔是完整的新內容，失敗時目標檔維持原樣、不留暫存檔。
///
/// 目標檔已存在時沿用它的權限；目標是 symlink 時回 [`Error::Symlink`]，不寫入。
pub fn write_atomic(path: &Path, contents: &[u8]) -> Result<()> {
    let name = path.file_name().ok_or_else(|| Error::NoFileName {
        path: path.to_path_buf(),
    })?;
    let dir = match path.parent() {
        Some(p) if !p.as_os_str().is_empty() => p,
        _ => Path::new("."),
    };

    let existing = match fs::symlink_metadata(path) {
        Ok(meta) if meta.file_type().is_symlink() => {
            return Err(Error::Symlink {
                path: path.to_path_buf(),
            });
        }
        Ok(meta) => Some(meta.permissions()),
        Err(e) if e.kind() == io::ErrorKind::NotFound => None,
        Err(e) => return Err(Error::io(Op::Stat, path, e)),
    };

    let (tmp_path, file) = create_temp(dir, name)?;
    let written = fill_temp(file, &tmp_path, contents, existing)
        .and_then(|()| fs::rename(&tmp_path, path).map_err(|e| Error::io(Op::Rename, path, e)));
    if let Err(e) = written {
        // 清掉暫存檔；刪除失敗時仍回報原本的錯誤，原因在前。
        let _ = fs::remove_file(&tmp_path);
        return Err(e);
    }
    sync_dir(dir)
}

/// 在 `dir` 建 `.tmp.<name>.<pid>.<序號>`，只建新檔（不覆蓋、不跟隨既有 symlink）。
fn create_temp(dir: &Path, name: &std::ffi::OsStr) -> Result<(PathBuf, File)> {
    let pid = std::process::id();
    let mut last = None;
    for _ in 0..TEMP_ATTEMPTS {
        let seq = TEMP_SEQ.fetch_add(1, Ordering::Relaxed);
        let mut tmp_name = OsString::from(".tmp.");
        tmp_name.push(name);
        tmp_name.push(format!(".{pid}.{seq}"));
        let tmp_path = dir.join(tmp_name);
        match OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&tmp_path)
        {
            Ok(file) => return Ok((tmp_path, file)),
            Err(e) if e.kind() == io::ErrorKind::AlreadyExists => last = Some((tmp_path, e)),
            Err(e) => return Err(Error::io(Op::CreateTemp, &tmp_path, e)),
        }
    }
    match last {
        Some((p, e)) => Err(Error::io(Op::CreateTemp, &p, e)),
        None => Err(Error::io(
            Op::CreateTemp,
            dir,
            io::Error::from(io::ErrorKind::AlreadyExists),
        )),
    }
}

/// 寫入、設權限、fsync，再明確關檔；任何一步失敗都回錯誤。
fn fill_temp(
    mut file: File,
    tmp_path: &Path,
    contents: &[u8],
    permissions: Option<fs::Permissions>,
) -> Result<()> {
    let filled = file
        .write_all(contents)
        .map_err(|e| Error::io(Op::Write, tmp_path, e))
        .and_then(|()| match permissions {
            Some(p) => file
                .set_permissions(p)
                .map_err(|e| Error::io(Op::SetPermissions, tmp_path, e)),
            None => Ok(()),
        })
        .and_then(|()| {
            file.sync_all()
                .map_err(|e| Error::io(Op::Sync, tmp_path, e))
        });
    // 不論前面成敗都明確關檔；前面的錯誤優先。
    let closed = close(file, tmp_path);
    filled.and(closed)
}

/// fsync 目錄，讓 rename 本身落到磁碟。
fn sync_dir(dir: &Path) -> Result<()> {
    let handle = File::open(dir).map_err(|e| Error::io(Op::OpenDir, dir, e))?;
    let synced = handle.sync_all().map_err(|e| Error::io(Op::Sync, dir, e));
    let closed = close(handle, dir);
    synced.and(closed)
}

/// 明確關檔並回傳 close(2) 的錯誤；std 的 `File` 只在 `Drop` 裡關檔且吞掉錯誤。
fn close(file: File, path: &Path) -> Result<()> {
    nix::unistd::close(file).map_err(|errno| Error::io(Op::Close, path, io::Error::from(errno)))
}

// ---------------------------------------------------------------------------
// 指紋

/// sha256 指紋。
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Debug)]
pub struct Fingerprint([u8; 32]);

impl Fingerprint {
    pub fn as_bytes(&self) -> &[u8; 32] {
        &self.0
    }

    /// 小寫十六進位，64 字元。
    pub fn to_hex(&self) -> String {
        self.to_string()
    }
}

impl fmt::Display for Fingerprint {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for b in self.0 {
            write!(f, "{b:02x}")?;
        }
        Ok(())
    }
}

/// 原樣內容的 sha256。
pub fn fingerprint(contents: &[u8]) -> Fingerprint {
    Fingerprint(Sha256::digest(contents).into())
}

/// 把 CRLF 正規化成 LF 之後的 sha256（ADR-0003）：只改行尾的兩份內容得到同一個指紋。
/// 只處理緊接 `\n` 的 `\r`；單獨的 `\r` 照原樣算。
pub fn fingerprint_normalized(contents: &[u8]) -> Fingerprint {
    let mut hasher = Sha256::new();
    let mut start = 0;
    let mut i = 0;
    while i + 1 < contents.len() {
        if contents[i] == b'\r' && contents[i + 1] == b'\n' {
            hasher.update(&contents[start..i]);
            start = i + 1;
            i += 2;
        } else {
            i += 1;
        }
    }
    hasher.update(&contents[start..]);
    Fingerprint(hasher.finalize().into())
}

/// 把 CRLF 正規化成 LF 之後的內容，規則同 [`fingerprint_normalized`]：只處理緊接 `\n` 的 `\r`，
/// 單獨的 `\r` 照原樣保留。沒有 CRLF 時不複製。
pub fn normalize_crlf(contents: &[u8]) -> Cow<'_, [u8]> {
    if !contents.windows(2).any(|w| w == b"\r\n") {
        return Cow::Borrowed(contents);
    }
    let mut out = Vec::with_capacity(contents.len());
    let mut i = 0;
    while i < contents.len() {
        if contents[i] == b'\r' && contents.get(i + 1) == Some(&b'\n') {
            i += 1;
            continue;
        }
        out.push(contents[i]);
        i += 1;
    }
    Cow::Owned(out)
}

// ---------------------------------------------------------------------------
// 走訪

/// 走訪 `root` 底下所有一般檔，回傳相對於 `root` 的路徑，按整條相對路徑的位元組排序。
///
/// 順序只看位元組，不隨 locale 或檔案系統的 readdir 順序；例如 `a-b` 排在 `a/b` 前（`-` 是 0x2d、`/` 是 0x2f）。
/// 目錄本身不列出。`root` 或其中任何項目是 symlink 時回 [`Error::Symlink`]；
/// 遇到 FIFO、socket、裝置檔回 [`Error::NotRegular`]。
pub fn walk_sorted(root: &Path) -> Result<Vec<PathBuf>> {
    let meta = fs::symlink_metadata(root).map_err(|e| Error::io(Op::Stat, root, e))?;
    if meta.file_type().is_symlink() {
        return Err(Error::Symlink {
            path: root.to_path_buf(),
        });
    }
    if !meta.is_dir() {
        return Err(Error::io(
            Op::ReadDir,
            root,
            io::Error::from(io::ErrorKind::NotADirectory),
        ));
    }
    let mut out = Vec::new();
    walk_dir(root, Path::new(""), &mut out)?;
    out.sort_by(|a, b| a.as_os_str().as_bytes().cmp(b.as_os_str().as_bytes()));
    Ok(out)
}

fn walk_dir(root: &Path, rel: &Path, out: &mut Vec<PathBuf>) -> Result<()> {
    let dir = root.join(rel);
    let entries = fs::read_dir(&dir).map_err(|e| Error::io(Op::ReadDir, &dir, e))?;
    for entry in entries {
        let entry = entry.map_err(|e| Error::io(Op::ReadDir, &dir, e))?;
        let child = rel.join(entry.file_name());
        let full = root.join(&child);
        // DirEntry::file_type 不跟隨 symlink。
        let ty = entry
            .file_type()
            .map_err(|e| Error::io(Op::Stat, &full, e))?;
        if ty.is_symlink() {
            return Err(Error::Symlink { path: full });
        } else if ty.is_dir() {
            walk_dir(root, &child, out)?;
        } else if ty.is_file() {
            out.push(child);
        } else {
            return Err(Error::NotRegular { path: full });
        }
    }
    Ok(())
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;
    use std::os::unix::fs::{PermissionsExt, symlink};

    fn temp_leftovers(dir: &Path) -> Vec<String> {
        fs::read_dir(dir)
            .unwrap()
            .map(|e| e.unwrap().file_name().to_string_lossy().into_owned())
            .filter(|n| n.starts_with(".tmp."))
            .collect()
    }

    #[test]
    fn write_atomic_creates_and_replaces() {
        let dir = tempfile::tempdir().unwrap();
        let path = dir.path().join("a.toml");
        write_atomic(&path, b"one\n").unwrap();
        assert_eq!(fs::read(&path).unwrap(), b"one\n");
        write_atomic(&path, b"two\n").unwrap();
        assert_eq!(fs::read(&path).unwrap(), b"two\n");
        assert!(temp_leftovers(dir.path()).is_empty());
    }

    #[test]
    fn write_atomic_keeps_existing_permissions() {
        let dir = tempfile::tempdir().unwrap();
        let path = dir.path().join("run.sh");
        fs::write(&path, b"old").unwrap();
        fs::set_permissions(&path, fs::Permissions::from_mode(0o751)).unwrap();
        write_atomic(&path, b"new").unwrap();
        let mode = fs::metadata(&path).unwrap().permissions().mode() & 0o777;
        assert_eq!(mode, 0o751);
    }

    /// rename 失敗（目標是非空目錄）：回 Rename 錯誤、目標原樣、不留暫存檔。
    /// 用目錄而不用權限造失敗，因為 test stage 以 root 執行，權限擋不住。
    #[test]
    fn rename_failure_leaves_no_partial_file() {
        let dir = tempfile::tempdir().unwrap();
        let target = dir.path().join("busy");
        fs::create_dir(&target).unwrap();
        fs::write(target.join("keep"), b"x").unwrap();

        let err = write_atomic(&target, b"payload").unwrap_err();
        assert!(
            matches!(err, Error::Io { op: Op::Rename, .. }),
            "unexpected error: {err:?}"
        );
        assert!(target.is_dir());
        assert_eq!(fs::read(target.join("keep")).unwrap(), b"x");
        assert!(temp_leftovers(dir.path()).is_empty());
    }

    #[test]
    fn create_failure_leaves_nothing() {
        let dir = tempfile::tempdir().unwrap();
        let path = dir.path().join("missing").join("a.txt");
        let err = write_atomic(&path, b"x").unwrap_err();
        assert!(
            matches!(
                err,
                Error::Io {
                    op: Op::CreateTemp,
                    ..
                }
            ),
            "unexpected error: {err:?}"
        );
        assert!(!dir.path().join("missing").exists());
    }

    #[test]
    fn write_atomic_rejects_symlink_target() {
        let dir = tempfile::tempdir().unwrap();
        let real = dir.path().join("real");
        fs::write(&real, b"original").unwrap();
        let link = dir.path().join("link");
        symlink(&real, &link).unwrap();

        let err = write_atomic(&link, b"new").unwrap_err();
        assert!(
            matches!(err, Error::Symlink { .. }),
            "unexpected error: {err:?}"
        );
        assert_eq!(fs::read(&real).unwrap(), b"original");
        assert!(
            fs::symlink_metadata(&link)
                .unwrap()
                .file_type()
                .is_symlink()
        );
        assert!(temp_leftovers(dir.path()).is_empty());
    }

    #[test]
    fn write_atomic_rejects_path_without_file_name() {
        let err = write_atomic(Path::new("/"), b"x").unwrap_err();
        assert!(
            matches!(err, Error::NoFileName { .. }),
            "unexpected error: {err:?}"
        );
    }

    #[test]
    fn fingerprint_is_sha256_hex() {
        assert_eq!(
            fingerprint(b"").to_hex(),
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        );
        assert_eq!(
            fingerprint(b"abc").to_hex(),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        );
    }

    #[test]
    fn crlf_and_lf_have_same_normalized_fingerprint() {
        let lf = b"a\nb\n\nc";
        let crlf = b"a\r\nb\r\n\r\nc";
        assert_eq!(fingerprint_normalized(lf), fingerprint_normalized(crlf));
        assert_eq!(fingerprint_normalized(lf), fingerprint(lf));
        assert_ne!(fingerprint(lf), fingerprint(crlf));
    }

    #[test]
    fn normalize_crlf_matches_normalized_fingerprint() {
        for input in [
            &b""[..],
            b"a\nb\n",
            b"a\r\nb\r\n\r\nc",
            b"a\rb\r\r\nc\r",
            b"\r\n",
        ] {
            assert_eq!(
                fingerprint(&normalize_crlf(input)),
                fingerprint_normalized(input),
                "{input:?}"
            );
        }
        assert_eq!(&*normalize_crlf(b"a\r\nb\rc\r\n"), b"a\nb\rc\n");
        assert!(matches!(normalize_crlf(b"a\nb\r"), Cow::Borrowed(_)));
    }

    #[test]
    fn mixed_line_endings_normalize_the_same() {
        assert_eq!(
            fingerprint_normalized(b"a\r\nb\nc\r\n"),
            fingerprint(b"a\nb\nc\n")
        );
    }

    #[test]
    fn lone_cr_is_content() {
        assert_ne!(fingerprint_normalized(b"a\rb"), fingerprint(b"ab"));
        assert_eq!(fingerprint_normalized(b"a\rb"), fingerprint(b"a\rb"));
        assert_eq!(fingerprint_normalized(b"a\r"), fingerprint(b"a\r"));
        assert_eq!(fingerprint_normalized(b"a\r\r\n"), fingerprint(b"a\r\n"));
    }

    #[test]
    fn content_change_changes_normalized_fingerprint() {
        assert_ne!(
            fingerprint_normalized(b"a\nb\n"),
            fingerprint_normalized(b"b\na\n")
        );
    }

    #[test]
    fn walk_order_is_byte_order() {
        let dir = tempfile::tempdir().unwrap();
        let root = dir.path();
        // 建立順序刻意打亂；locale 排序會把大小寫、底線、非 ASCII 排到別處。
        for name in ["é", "b", "_x", "Z", "a-b", "B", "a"] {
            fs::write(root.join(name), b"").unwrap();
        }
        fs::create_dir(root.join("a.d")).unwrap();
        fs::write(root.join("a.d").join("z"), b"").unwrap();
        fs::write(root.join("a.d").join("A"), b"").unwrap();
        fs::create_dir_all(root.join("empty")).unwrap();

        let got = walk_sorted(root).unwrap();
        let want: Vec<PathBuf> = ["B", "Z", "_x", "a", "a-b", "a.d/A", "a.d/z", "b", "é"]
            .iter()
            .map(PathBuf::from)
            .collect();
        assert_eq!(got, want);
    }

    /// 整條路徑比位元組：`a-b`（0x2d）在 `a/b`（0x2f）前、`a0`（0x30）在後。
    #[test]
    fn walk_compares_whole_path_not_components() {
        let dir = tempfile::tempdir().unwrap();
        let root = dir.path();
        fs::create_dir(root.join("a")).unwrap();
        fs::write(root.join("a").join("b"), b"").unwrap();
        fs::write(root.join("a-b"), b"").unwrap();
        fs::write(root.join("a0"), b"").unwrap();

        let got = walk_sorted(root).unwrap();
        let want: Vec<PathBuf> = ["a-b", "a/b", "a0"].iter().map(PathBuf::from).collect();
        assert_eq!(got, want);
    }

    #[test]
    fn walk_rejects_symlink_inside() {
        let dir = tempfile::tempdir().unwrap();
        let root = dir.path();
        fs::create_dir(root.join("sub")).unwrap();
        fs::write(root.join("sub").join("real"), b"").unwrap();
        symlink("real", root.join("sub").join("link")).unwrap();

        let err = walk_sorted(root).unwrap_err();
        assert!(
            matches!(err, Error::Symlink { .. }),
            "unexpected error: {err:?}"
        );
        assert_eq!(err.path(), root.join("sub").join("link"));
    }

    #[test]
    fn walk_rejects_dangling_symlink() {
        let dir = tempfile::tempdir().unwrap();
        symlink("nowhere", dir.path().join("dangling")).unwrap();
        let err = walk_sorted(dir.path()).unwrap_err();
        assert!(
            matches!(err, Error::Symlink { .. }),
            "unexpected error: {err:?}"
        );
    }

    #[test]
    fn walk_rejects_symlinked_root() {
        let dir = tempfile::tempdir().unwrap();
        let real = dir.path().join("real");
        fs::create_dir(&real).unwrap();
        let link = dir.path().join("link");
        symlink(&real, &link).unwrap();

        let err = walk_sorted(&link).unwrap_err();
        assert!(
            matches!(err, Error::Symlink { .. }),
            "unexpected error: {err:?}"
        );
    }
}
