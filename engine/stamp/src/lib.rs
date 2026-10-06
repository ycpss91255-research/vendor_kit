//! 印記：記錄本機工具內容對應的版本與逐檔指紋（GLOSSARY 的印記、逐檔指紋）。
//!
//! - 印記記兩件事：`version` 是取件所依據的版本鎖定行的值（image 引用原文，不解析、不正規化，
//!   比對只用字串相等），`[[file]]` 是取出的每個一般檔一筆：`path`（相對於工具內容根目錄、以 `/`
//!   分隔）與 `sha256`（原樣內容的 sha256，[`files::fingerprint`]）。
//! - 逐檔指紋不做 CRLF 正規化：ADR-0006 要證的是位元組相同，只改行尾也算內容不同。
//! - [`Stamp::compute`] 由任何一個目錄算印記（`cache/<repo>/`，或取件時的暫存目錄）；
//!   [`Stamp::verify`] 拿印記比對目錄現況，多出的檔、少掉的檔、內容不同的檔分開列
//!   （04 sync 表：判定 cache 檔案集合與逐檔指紋，包括多出的檔案）。不一致對應 VK0015。
//! - 讀寫經 `schema`：檔案版過高回 VK0008；未知欄位（含 `[[file]]` 裡的）讀時忽略、寫時保留。
//! - 印記不在回 `Ok(None)`：首次取件原本沒有印記，不算損壞（04 sync 表）。既有印記損壞
//!   （語法、`schema`、欄位型別或值不合、同一路徑兩筆）回 [`Error::Corrupt`]，對應 VK0044。
//!
//! 這裡只提供「算、讀、寫、比」，不決定何時寫印記：正式印記何時寫由呼叫端照 `txn` 的順序決定
//! （#372 取件時機定案：先取到 repo 外暫存，全部同意才寫 cache／印記／gen）。印記的位置是
//! [`layout::InstallDir::tool_stamp`]（[`tool_file`] 轉呼叫，各 crate 共用），讀寫仍由呼叫端給路徑。
//! ADR-0008 把「印記第一行語意」列為介面版的升版觸發；這裡寫出的第一行是 `schema`（由 `schema` 決定），
//! 啟動器要以字串比對讀哪一行，等那個決議定案再改。
//!
//! 這裡不印診斷；要怎麼印由呼叫端經 `diagnostics` 決定，`<repo>` 等欄位也由呼叫端填。

use std::collections::{BTreeMap, BTreeSet};
use std::fmt;
use std::fs;
use std::io;
use std::path::{Component, Path, PathBuf};

use layout::{InstallDir, InvalidName};
use messages::Message;
use schema::{Document, ReadError, TooNew, WriteError};
use toml_edit::{Item, Table};

/// 版本鎖定行的值。
pub const VERSION_KEY: &str = "version";
/// 逐檔指紋的陣列表名。
pub const FILE_KEY: &str = "file";
/// 相對於工具內容根目錄的路徑。
pub const PATH_KEY: &str = "path";
/// 原樣內容的 sha256。
pub const SHA256_KEY: &str = "sha256";

/// 一個工具的印記檔：`.vendor_kit/cache/<repo>.stamp.toml`（[`layout::InstallDir::tool_stamp`]）。
///
/// `<repo>` 由呼叫端先驗過是單一路徑段。
pub fn tool_file(dir: &InstallDir, repo: &str) -> PathBuf {
    dir.tool_stamp(repo)
}

// ---------------------------------------------------------------------------
// 逐檔指紋

/// 原樣內容 sha256 的小寫十六進位，64 字元。
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Digest(String);

impl Digest {
    /// 內容原樣的 sha256，不正規化行尾。
    pub fn of(contents: &[u8]) -> Digest {
        Digest(files::fingerprint(contents).to_hex())
    }

    /// 由檔裡的字解析；不是 64 個小寫十六進位字元回 `None`。
    pub fn parse(s: &str) -> Option<Digest> {
        let ok = s.len() == 64 && s.bytes().all(|b| matches!(b, b'0'..=b'9' | b'a'..=b'f'));
        ok.then(|| Digest(s.to_owned()))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl fmt::Display for Digest {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.0)
    }
}

/// 一筆 `[[file]]`。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Entry {
    /// 相對於工具內容根目錄的路徑，以 `/` 分隔。
    pub path: String,
    pub sha256: Digest,
}

// ---------------------------------------------------------------------------
// 印記

/// 一份印記。
#[derive(Debug, Clone)]
pub struct Stamp {
    doc: Document,
    version: String,
    /// 依路徑的位元組排序；讀進來的檔照檔裡的順序。
    entries: Vec<Entry>,
}

impl Stamp {
    /// 由 `root` 底下的全部一般檔算出印記，`version` 是取件所依據的版本鎖定行的值。
    ///
    /// `root` 可以是 `cache/<repo>/`，也可以是取件時的暫存目錄；這裡不寫檔。
    /// symlink、FIFO 等非一般檔回錯誤（[`files::walk_sorted`]）。
    pub fn compute(version: impl Into<String>, root: &Path) -> Result<Stamp, ComputeError> {
        let version = version.into();
        if version.is_empty() {
            return Err(ComputeError::EmptyVersion);
        }
        let entries = digests(root)?;
        let mut doc = Document::new();
        doc.set(&[VERSION_KEY], version.as_str())
            .map_err(ComputeError::Build)?;
        for (i, e) in entries.iter().enumerate() {
            let index = doc.push_table(FILE_KEY).map_err(ComputeError::Build)?;
            debug_assert_eq!(index, i);
            doc.set_in(FILE_KEY, index, PATH_KEY, e.path.as_str())
                .map_err(ComputeError::Build)?;
            doc.set_in(FILE_KEY, index, SHA256_KEY, e.sha256.as_str())
                .map_err(ComputeError::Build)?;
        }
        Ok(Stamp {
            doc,
            version,
            entries,
        })
    }

    /// 由安裝目錄的 `cache/<repo>/` 算出印記（[`InstallDir::tool_cache`]）。
    pub fn compute_tool(
        dir: &InstallDir,
        repo: &str,
        version: impl Into<String>,
    ) -> Result<Stamp, ComputeError> {
        let root = dir.tool_cache(repo).map_err(ComputeError::InvalidName)?;
        Stamp::compute(version, &root)
    }

    /// 讀印記。檔不在回 `Ok(None)`（首次取件，不算損壞）。
    pub fn load(path: &Path) -> Result<Option<Stamp>, Error> {
        let text = match fs::read_to_string(path) {
            Ok(text) => text,
            Err(e) if e.kind() == io::ErrorKind::NotFound => return Ok(None),
            Err(e) if e.kind() == io::ErrorKind::InvalidData => {
                return Err(Error::Corrupt {
                    file: path.to_path_buf(),
                    reason: Invalid::new("not valid UTF-8"),
                });
            }
            Err(source) => {
                return Err(Error::Io {
                    file: path.to_path_buf(),
                    source,
                });
            }
        };
        Stamp::parse(&text).map(Some).map_err(|e| e.at(path))
    }

    /// 解析印記內容：先過 `schema` 的讀取門檻，再檢查 `version` 與逐筆 `[[file]]`。
    pub fn parse(text: &str) -> Result<Stamp, ParseError> {
        let doc = Document::parse(text).map_err(|e| match e {
            ReadError::TooNew(t) => ParseError::TooNew(t),
            other => ParseError::Invalid(Invalid::new(other.to_string())),
        })?;
        let version = match doc.root().get(VERSION_KEY).filter(|i| !i.is_none()) {
            None => return Err(ParseError::Invalid(Invalid::new("missing `version`"))),
            Some(item) => item
                .as_str()
                .filter(|s| !s.is_empty())
                .ok_or_else(|| {
                    ParseError::Invalid(Invalid::new("`version` is not a non-empty string"))
                })?
                .to_owned(),
        };
        let entries = read_entries(&doc).map_err(ParseError::Invalid)?;
        Ok(Stamp {
            doc,
            version,
            entries,
        })
    }

    /// 版本鎖定行的值。
    pub fn version(&self) -> &str {
        &self.version
    }

    /// 全部逐檔指紋。
    pub fn entries(&self) -> &[Entry] {
        &self.entries
    }

    /// 拿這份印記比對另一份（通常是 [`Stamp::compute`] 算出的現況）的檔案集合與逐檔指紋。
    /// `version` 不在比對內：版本是否相符由呼叫端以 [`Stamp::version`] 字串比對。
    pub fn compare(&self, actual: &Stamp) -> Diff {
        compare_entries(&self.entries, &actual.entries)
    }

    /// 拿這份印記比對 `root` 目錄現況。`root` 不在時當成空目錄：每個檔都算少掉。
    pub fn verify(&self, root: &Path) -> Result<Diff, ComputeError> {
        let actual = match fs::symlink_metadata(root) {
            Err(e) if e.kind() == io::ErrorKind::NotFound => Vec::new(),
            _ => digests(root)?,
        };
        Ok(compare_entries(&self.entries, &actual))
    }

    /// 蓋上寫入者，確認沒有少寫後回傳要寫回的內容。
    pub fn render(&mut self, written_by: &str) -> Result<String, WriteError> {
        self.doc.render(written_by)
    }

    /// 原子寫到 `path`；上層目錄不在時先建。
    pub fn save(&mut self, path: &Path, written_by: &str) -> Result<(), Error> {
        let text = self.render(written_by).map_err(|source| Error::Render {
            file: path.to_path_buf(),
            source,
        })?;
        if let Some(parent) = path.parent().filter(|p| !p.as_os_str().is_empty()) {
            fs::create_dir_all(parent).map_err(|source| Error::Io {
                file: parent.to_path_buf(),
                source,
            })?;
        }
        files::write_atomic(path, text.as_bytes()).map_err(Error::Write)
    }
}

/// `root` 底下每個一般檔的逐檔指紋，依路徑的位元組排序。
fn digests(root: &Path) -> Result<Vec<Entry>, ComputeError> {
    let paths = files::walk_sorted(root).map_err(ComputeError::Walk)?;
    let mut out = Vec::with_capacity(paths.len());
    for rel in paths {
        let path = rel_to_string(&rel).ok_or_else(|| ComputeError::NonUtf8Path {
            path: root.join(&rel),
        })?;
        let full = root.join(&rel);
        let contents =
            fs::read(&full).map_err(|source| ComputeError::Read { file: full, source })?;
        out.push(Entry {
            path,
            sha256: Digest::of(&contents),
        });
    }
    Ok(out)
}

/// 相對路徑轉成以 `/` 分隔的字串；有非 UTF-8 的段回 `None`。
fn rel_to_string(rel: &Path) -> Option<String> {
    let mut segs = Vec::new();
    for c in rel.components() {
        match c {
            Component::Normal(s) => segs.push(s.to_str()?),
            _ => return None,
        }
    }
    Some(segs.join("/"))
}

fn compare_entries(expected: &[Entry], actual: &[Entry]) -> Diff {
    let want: BTreeMap<&str, &Digest> = expected
        .iter()
        .map(|e| (e.path.as_str(), &e.sha256))
        .collect();
    let have: BTreeMap<&str, &Digest> = actual
        .iter()
        .map(|e| (e.path.as_str(), &e.sha256))
        .collect();
    let mut diff = Diff::default();
    for (path, digest) in &want {
        match have.get(path) {
            None => diff.missing.push((*path).to_owned()),
            Some(d) if d != digest => diff.changed.push((*path).to_owned()),
            Some(_) => {}
        }
    }
    for path in have.keys() {
        if !want.contains_key(path) {
            diff.extra.push((*path).to_owned());
        }
    }
    diff
}

fn read_entries(doc: &Document) -> Result<Vec<Entry>, Invalid> {
    let tables = match doc.get(&[FILE_KEY]) {
        None | Some(Item::None) => return Ok(Vec::new()),
        Some(Item::ArrayOfTables(a)) => a,
        Some(_) => {
            return Err(Invalid::new(format!(
                "`{FILE_KEY}` is not an array of tables"
            )));
        }
    };
    let mut seen = BTreeSet::new();
    let mut entries = Vec::with_capacity(tables.len());
    for (i, table) in tables.iter().enumerate() {
        let entry = read_entry(table).map_err(|e| e.in_entry(i))?;
        if !seen.insert(entry.path.clone()) {
            return Err(Invalid::new(format!("duplicate path {:?}", entry.path)).in_entry(i));
        }
        entries.push(entry);
    }
    Ok(entries)
}

fn read_entry(table: &Table) -> Result<Entry, Invalid> {
    let path = required_str(table, PATH_KEY)?;
    check_path(path)?;
    let sha256 = Digest::parse(required_str(table, SHA256_KEY)?).ok_or_else(|| {
        Invalid::new(format!(
            "`{SHA256_KEY}` is not a 64-character lowercase hex sha256"
        ))
    })?;
    Ok(Entry {
        path: path.to_owned(),
        sha256,
    })
}

fn required_str<'a>(table: &'a Table, key: &str) -> Result<&'a str, Invalid> {
    match table.get(key).filter(|i| !i.is_none()) {
        None => Err(Invalid::new(format!("missing `{key}`"))),
        Some(item) => item
            .as_str()
            .ok_or_else(|| Invalid::new(format!("`{key}` is not a string"))),
    }
}

/// 相對路徑：非空、不是絕對路徑、不含 `..`、`.`、空段或 NUL，跳不出工具內容根目錄。
fn check_path(path: &str) -> Result<(), Invalid> {
    let bad = || {
        Invalid::new(format!(
            "`{PATH_KEY}` is not a plain relative path: {path:?}"
        ))
    };
    if path.is_empty() || path.contains('\0') || path.ends_with('/') {
        return Err(bad());
    }
    if !Path::new(path)
        .components()
        .all(|c| matches!(c, Component::Normal(_)))
        || path.split('/').any(|seg| seg.is_empty() || seg == ".")
    {
        return Err(bad());
    }
    Ok(())
}

// ---------------------------------------------------------------------------
// 比對結果

/// 印記與現況的差異；三份清單都依路徑的位元組排序。
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Diff {
    /// 現況有、印記沒有的檔。
    pub extra: Vec<String>,
    /// 印記有、現況沒有的檔。
    pub missing: Vec<String>,
    /// 兩邊都有但指紋不同的檔。
    pub changed: Vec<String>,
}

impl Diff {
    /// 檔案集合與逐檔指紋都一致。
    pub fn is_match(&self) -> bool {
        self.extra.is_empty() && self.missing.is_empty() && self.changed.is_empty()
    }

    /// 不一致時對應的訊息表條目（VK0015：sync 依版本鎖定行重新取件）；一致回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        (!self.is_match()).then_some(&messages::VK0015)
    }
}

// ---------------------------------------------------------------------------
// 錯誤

/// 印記內容不合：語法、`schema`、`version` 或 `[[file]]` 的欄位。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Invalid {
    reason: String,
}

impl Invalid {
    fn new(reason: impl Into<String>) -> Self {
        Invalid {
            reason: reason.into(),
        }
    }

    fn in_entry(self, index: usize) -> Self {
        Invalid::new(format!("{FILE_KEY}[{index}]: {}", self.reason))
    }

    /// 哪裡不合。
    pub fn reason(&self) -> &str {
        &self.reason
    }
}

impl fmt::Display for Invalid {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.reason)
    }
}

impl std::error::Error for Invalid {}

/// [`Stamp::parse`] 失敗。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ParseError {
    /// 檔案版過高（VK0008）。
    TooNew(TooNew),
    /// 印記損壞（VK0044）。
    Invalid(Invalid),
}

impl ParseError {
    fn at(self, file: &Path) -> Error {
        let file = file.to_path_buf();
        match self {
            ParseError::TooNew(too_new) => Error::TooNew { file, too_new },
            ParseError::Invalid(reason) => Error::Corrupt { file, reason },
        }
    }

    /// 對應的訊息表條目。
    pub fn message(&self) -> &'static Message {
        match self {
            ParseError::TooNew(t) => t.message(),
            ParseError::Invalid(_) => &messages::VK0044,
        }
    }
}

impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ParseError::TooNew(t) => t.fmt(f),
            ParseError::Invalid(e) => write!(f, "corrupt stamp: {e}"),
        }
    }
}

impl std::error::Error for ParseError {}

/// 算印記或比對現況失敗。
#[derive(Debug)]
pub enum ComputeError {
    /// 版本鎖定行的值是空的。
    EmptyVersion,
    /// `<repo>` 不是單一路徑段。
    InvalidName(InvalidName),
    /// 走訪失敗：系統呼叫失敗、遇到 symlink 或非一般檔。
    Walk(files::Error),
    /// 讀檔失敗。
    Read { file: PathBuf, source: io::Error },
    /// 路徑有非 UTF-8 的段，寫不進印記。
    NonUtf8Path { path: PathBuf },
    /// 組文件樹失敗。
    Build(WriteError),
}

impl fmt::Display for ComputeError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ComputeError::EmptyVersion => f.write_str("empty lock version value"),
            ComputeError::InvalidName(e) => e.fmt(f),
            ComputeError::Walk(e) => e.fmt(f),
            ComputeError::Read { file, source } => {
                write!(f, "read {}: {source}", file.display())
            }
            ComputeError::NonUtf8Path { path } => {
                write!(f, "path is not valid UTF-8: {}", path.display())
            }
            ComputeError::Build(e) => e.fmt(f),
        }
    }
}

impl std::error::Error for ComputeError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            ComputeError::InvalidName(e) => Some(e),
            ComputeError::Walk(e) => Some(e),
            ComputeError::Read { source, .. } => Some(source),
            ComputeError::Build(e) => Some(e),
            ComputeError::EmptyVersion | ComputeError::NonUtf8Path { .. } => None,
        }
    }
}

/// 讀寫印記檔失敗。印記不在不是錯誤，見 [`Stamp::load`]。
#[derive(Debug)]
pub enum Error {
    /// 既有印記損壞（VK0044）。
    Corrupt { file: PathBuf, reason: Invalid },
    /// 檔案版高於本引擎上限（VK0008）。
    TooNew { file: PathBuf, too_new: TooNew },
    /// 讀檔或建目錄的系統呼叫失敗。
    Io { file: PathBuf, source: io::Error },
    /// 拒絕寫回：會少寫原本的值。
    Render { file: PathBuf, source: WriteError },
    /// 原子寫入失敗。
    Write(files::Error),
}

impl Error {
    /// 出錯的檔。
    pub fn file(&self) -> &Path {
        match self {
            Error::Corrupt { file, .. }
            | Error::TooNew { file, .. }
            | Error::Io { file, .. }
            | Error::Render { file, .. } => file,
            Error::Write(e) => e.path(),
        }
    }

    /// 對應的訊息表條目：損壞是 VK0044，檔案版過高是 VK0008；系統呼叫失敗還沒有代碼，回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            Error::Corrupt { .. } => Some(&messages::VK0044),
            Error::TooNew { too_new, .. } => Some(too_new.message()),
            Error::Io { .. } | Error::Render { .. } | Error::Write(_) => None,
        }
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Corrupt { file, reason } => {
                write!(f, "corrupt stamp {}: {reason}", file.display())
            }
            Error::TooNew { file, too_new } => write!(f, "{}: {too_new}", file.display()),
            Error::Io { file, source } => write!(f, "{}: {source}", file.display()),
            Error::Render { file, source } => write!(f, "{}: {source}", file.display()),
            Error::Write(e) => e.fmt(f),
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Error::Corrupt { reason, .. } => Some(reason),
            Error::Io { source, .. } => Some(source),
            Error::Render { source, .. } => Some(source),
            Error::Write(e) => Some(e),
            Error::TooNew { .. } => None,
        }
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    const REF: &str = "ghcr.io/acme/tool:v1.2.3@sha256:0000000000000000000000000000000000000000000000000000000000000000";

    fn tree(files: &[(&str, &[u8])]) -> tempfile::TempDir {
        let dir = tempfile::tempdir().unwrap();
        for (path, contents) in files {
            let full = dir.path().join(path);
            fs::create_dir_all(full.parent().unwrap()).unwrap();
            fs::write(full, contents).unwrap();
        }
        dir
    }

    fn base() -> tempfile::TempDir {
        tree(&[
            ("recipe.just", b"a\n"),
            ("dist/b.txt", b"b\n"),
            ("dist/c/d.sh", b"d\n"),
        ])
    }

    #[test]
    fn compute_lists_every_file_sorted_with_raw_sha256() {
        let dir = base();
        let s = Stamp::compute(REF, dir.path()).unwrap();
        assert_eq!(s.version(), REF);
        let paths: Vec<&str> = s.entries().iter().map(|e| e.path.as_str()).collect();
        assert_eq!(paths, ["dist/b.txt", "dist/c/d.sh", "recipe.just"]);
        assert_eq!(s.entries()[0].sha256, Digest::of(b"b\n"));
        assert_eq!(
            Digest::of(b"").as_str(),
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        );
    }

    #[test]
    fn unchanged_tree_matches() {
        let dir = base();
        let s = Stamp::compute(REF, dir.path()).unwrap();
        let diff = s.verify(dir.path()).unwrap();
        assert!(diff.is_match());
        assert_eq!(diff.message(), None);
    }

    #[test]
    fn extra_file_is_reported() {
        let dir = base();
        let s = Stamp::compute(REF, dir.path()).unwrap();
        fs::write(dir.path().join("dist/extra"), b"x").unwrap();
        let diff = s.verify(dir.path()).unwrap();
        assert_eq!(diff.extra, ["dist/extra"]);
        assert!(diff.missing.is_empty() && diff.changed.is_empty());
        assert_eq!(diff.message().map(|m| m.code), Some("VK0015"));
    }

    #[test]
    fn missing_file_is_reported() {
        let dir = base();
        let s = Stamp::compute(REF, dir.path()).unwrap();
        fs::remove_file(dir.path().join("dist/c/d.sh")).unwrap();
        let diff = s.verify(dir.path()).unwrap();
        assert_eq!(diff.missing, ["dist/c/d.sh"]);
        assert!(diff.extra.is_empty() && diff.changed.is_empty());
        assert_eq!(diff.message().map(|m| m.code), Some("VK0015"));
    }

    #[test]
    fn changed_content_is_reported() {
        let dir = base();
        let s = Stamp::compute(REF, dir.path()).unwrap();
        fs::write(dir.path().join("recipe.just"), b"changed\n").unwrap();
        let diff = s.verify(dir.path()).unwrap();
        assert_eq!(diff.changed, ["recipe.just"]);
        assert!(diff.extra.is_empty() && diff.missing.is_empty());
        assert_eq!(diff.message().map(|m| m.code), Some("VK0015"));
    }

    #[test]
    fn crlf_only_change_counts_as_changed() {
        let dir = base();
        let s = Stamp::compute(REF, dir.path()).unwrap();
        fs::write(dir.path().join("recipe.just"), b"a\r\n").unwrap();
        assert_eq!(s.verify(dir.path()).unwrap().changed, ["recipe.just"]);
    }

    #[test]
    fn all_three_kinds_at_once_are_sorted() {
        let dir = base();
        let s = Stamp::compute(REF, dir.path()).unwrap();
        fs::remove_file(dir.path().join("dist/b.txt")).unwrap();
        fs::write(dir.path().join("z"), b"z").unwrap();
        fs::write(dir.path().join("a"), b"a").unwrap();
        fs::write(dir.path().join("dist/c/d.sh"), b"D\n").unwrap();
        let diff = s.verify(dir.path()).unwrap();
        assert_eq!(diff.extra, ["a", "z"]);
        assert_eq!(diff.missing, ["dist/b.txt"]);
        assert_eq!(diff.changed, ["dist/c/d.sh"]);
    }

    #[test]
    fn missing_root_counts_every_file_as_missing() {
        let dir = base();
        let s = Stamp::compute(REF, dir.path()).unwrap();
        let gone = dir.path().join("nope");
        let diff = s.verify(&gone).unwrap();
        assert_eq!(diff.missing.len(), 3);
        assert!(Stamp::compute(REF, &gone).is_err());
    }

    #[test]
    fn symlink_in_tree_is_an_error() {
        let dir = base();
        std::os::unix::fs::symlink("recipe.just", dir.path().join("link")).unwrap();
        assert!(matches!(
            Stamp::compute(REF, dir.path()),
            Err(ComputeError::Walk(files::Error::Symlink { .. }))
        ));
    }

    #[test]
    fn empty_version_is_rejected() {
        let dir = base();
        assert!(matches!(
            Stamp::compute("", dir.path()),
            Err(ComputeError::EmptyVersion)
        ));
    }

    #[test]
    fn save_load_round_trip_matches() {
        let dir = base();
        let out = tempfile::tempdir().unwrap();
        let path = out.path().join("sub/stamp.toml");
        let mut s = Stamp::compute(REF, dir.path()).unwrap();
        s.save(&path, "v0.1.0").unwrap();
        let loaded = Stamp::load(&path).unwrap().unwrap();
        assert_eq!(loaded.version(), REF);
        assert_eq!(loaded.entries(), s.entries());
        assert!(loaded.verify(dir.path()).unwrap().is_match());
        assert!(loaded.compare(&s).is_match());
        let text = fs::read_to_string(&path).unwrap();
        assert!(text.contains("written_by = \"v0.1.0\""));
    }

    #[test]
    fn compute_tool_uses_cache_dir() {
        let root = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(root.path());
        let cache = dir.tool_cache("tool").unwrap();
        fs::create_dir_all(&cache).unwrap();
        fs::write(cache.join("f"), b"f").unwrap();
        let s = Stamp::compute_tool(&dir, "tool", REF).unwrap();
        assert_eq!(s.entries().len(), 1);
        assert!(matches!(
            Stamp::compute_tool(&dir, "../x", REF),
            Err(ComputeError::InvalidName(_))
        ));
    }

    #[test]
    fn no_stamp_is_not_corrupt() {
        let out = tempfile::tempdir().unwrap();
        assert!(Stamp::load(&out.path().join("absent")).unwrap().is_none());
    }

    fn corrupt(text: &str) -> Error {
        let out = tempfile::tempdir().unwrap();
        let path = out.path().join("stamp.toml");
        fs::write(&path, text).unwrap();
        Stamp::load(&path).unwrap_err()
    }

    #[test]
    fn corrupt_stamps_map_to_vk0044() {
        let sha = "a".repeat(64);
        for text in [
            "not = [toml".to_owned(),
            format!("version = \"{REF}\"\n"),
            "schema = 1\n".to_owned(),
            "schema = 1\nversion = \"\"\n".to_owned(),
            "schema = 1\nversion = 3\n".to_owned(),
            format!("schema = 1\nversion = \"{REF}\"\nfile = 1\n"),
            format!("schema = 1\nversion = \"{REF}\"\n[[file]]\nsha256 = \"{sha}\"\n"),
            format!("schema = 1\nversion = \"{REF}\"\n[[file]]\npath = \"a\"\n"),
            format!("schema = 1\nversion = \"{REF}\"\n[[file]]\npath = \"a\"\nsha256 = \"XYZ\"\n"),
            format!(
                "schema = 1\nversion = \"{REF}\"\n[[file]]\npath = \"../a\"\nsha256 = \"{sha}\"\n"
            ),
            format!(
                "schema = 1\nversion = \"{REF}\"\n[[file]]\npath = \"/a\"\nsha256 = \"{sha}\"\n"
            ),
            format!(
                "schema = 1\nversion = \"{REF}\"\n[[file]]\npath = \"a//b\"\nsha256 = \"{sha}\"\n"
            ),
            format!(
                "schema = 1\nversion = \"{REF}\"\n[[file]]\npath = \"a\"\nsha256 = \"{sha}\"\n[[file]]\npath = \"a\"\nsha256 = \"{sha}\"\n"
            ),
        ] {
            let err = corrupt(&text);
            assert!(matches!(err, Error::Corrupt { .. }), "{text:?}: {err}");
            assert_eq!(err.message().map(|m| m.code), Some("VK0044"), "{text:?}");
        }
    }

    #[test]
    fn non_utf8_stamp_is_corrupt() {
        let out = tempfile::tempdir().unwrap();
        let path = out.path().join("stamp.toml");
        fs::write(&path, [0xff, 0xfe]).unwrap();
        assert!(matches!(
            Stamp::load(&path).unwrap_err(),
            Error::Corrupt { .. }
        ));
    }

    #[test]
    fn too_new_schema_maps_to_vk0008() {
        let err = corrupt(&format!("schema = 999\nversion = \"{REF}\"\n"));
        assert!(matches!(err, Error::TooNew { .. }));
        assert_eq!(err.message().map(|m| m.code), Some("VK0008"));
    }

    #[test]
    fn unknown_fields_survive_a_rewrite() {
        let sha = "b".repeat(64);
        let text = format!(
            "schema = 1\nversion = \"{REF}\"\nextra = \"keep\"\n[[file]]\npath = \"a\"\nsha256 = \"{sha}\"\nnote = \"keep too\"\n"
        );
        let mut s = Stamp::parse(&text).unwrap();
        let out = s.render("v0.1.0").unwrap();
        assert!(out.contains("extra = \"keep\""));
        assert!(out.contains("note = \"keep too\""));
    }
}
