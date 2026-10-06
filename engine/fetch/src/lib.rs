//! 取件內容的驗證：把啟動器取到暫存處的內容，驗成可以交給 `txn` 落地的候選（[`Candidate`]）。
//!
//! 取件時序依 #372 定案與 ADR-0006：啟動器把候選內容取到這次呼叫專用、repo 外的暫存處，唯讀掛進
//! 引擎；引擎在詢問之前只驗、不寫，全部同意之後才由 `txn` 重驗並寫進 `cache/` 與印記。這個 crate
//! 只做詢問前那一段，不寫任何檔，也不呼叫 docker（docker 動作是 `plan` 協定的 op，由呼叫端發）。
//!
//! # 暫存內容的根目錄
//!
//! `plan` 的 `extract` 把工具 image 的 `/dist/.` 複製進 `in/<slot>`，所以暫存內容的根目錄就是
//! `dist/` 的內容：`<ns>` 檔在根目錄底下的 [`JUST_DIR`]`/<ns>.just`（文件寫的 `dist/just/<ns>.just`）。
//! `txn` 把這個根目錄整份換進 `cache/<repo>/`，印記的路徑也相對於它。
//!
//! # 驗證順序（[`verify`]）
//!
//! 1. digest：inspect 回來的 RepoDigests 要有一筆是 `<registry>/<路徑>@sha256:<digest>`，與版本鎖定行
//!    的 image 名稱與 digest 相同（RepoDigests 不帶 tag）。不符回 [`Error::DigestMismatch`]。
//! 2. dist 格式：[`JUST_DIR`] 是目錄，底下每一項都是一般檔、名為 `<ns>.just`，`<ns>` 是合法的 just
//!    名稱，而且 `<repo>.just` 存在（ADR-0004:39）。不符回 [`Error::Format`]。
//! 3. 逐檔指紋：以 `stamp` 算出暫存內容的逐檔 sha256，只算不寫印記（ADR-0006:21）。呼叫端給了同一個
//!    版本的既有印記時，檔案集合與逐檔指紋要一致，不符回 [`Error::Fingerprint`]。
//! 4. `<ns>` 撞名：讀出的全部 `<ns>` 整組比對 [`Taken`]（已裝工具、根 `justfile` 的 recipe 或 module、
//!    保留名 `vendor_kit`，04 命名空間），列出每一個撞到的名字，回 [`Error::Collision`]（VK0030）。
//!    同一個 `<repo>` 自己已裝的 `<ns>` 不算撞名（upgrade、sync 換同一個工具）。
//!
//! 落地前的重驗（ADR-0006 三層驗證的第三層）用 [`Candidate::recheck`]：重算暫存內容，與詢問前算出的
//! 逐檔指紋比對。
//!
//! # 原因代碼
//!
//! 只有撞名有代碼（VK0030）。digest 不符、逐檔指紋不符（#372 計畫的 G1）與 dist 格式不符（G2）目前
//! 沒有對應的代碼，[`Error::message`] 回 `None`；VK0043 只寫 sync 的情況，sync 的呼叫端可自行對應。
//! 逐檔指紋不符不用 VK0015：那是 sync 發現 `cache/` 不符、已重新取件的警告，不是暫存內容的錯誤。
//!
//! 已裝工具的 `cache/<repo>/` 讀不到（[`cached_namespaces`]）分成不在（草稿碼 VK0068，下一步 `sync`）與讀不到
//! 或損壞（草稿碼 VK0073）；兩個草稿碼登錄前，`add`、`upgrade`、`remove`、`dev` 以 VK0056 停下，`<reason>` 由
//! [`CacheCheck`] 收齊這次全部讀不到的工具再產生。
//!
//! # 呼叫端負責的事
//!
//! - inspect 輸出的解析：這裡收已經取出的 RepoDigests 字串。
//! - [`Taken`] 的內容：已裝工具的 `<ns>`（可用 [`namespaces`] 讀 `cache/<repo>/`）、根 `justfile` 的
//!   recipe 與 module 名稱。這裡不解析 justfile。
//! - `add vendor_kit`（VK0057）在取件前看參數字面就擋，不在這裡。
//!
//! # 本機開發來源
//!
//! `version.local.toml` 的工具覆寫指到的本機開發來源，正規化與交付格式的檢查在 [`local`]（`dev`、`sync`、
//! `upgrade`、`add`、`remove` 共用）。
//!
//! 這裡不印診斷；要怎麼印由呼叫端經 `diagnostics` 決定。

use std::collections::BTreeSet;
use std::fmt;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

use imageref::ImageRef;
use messages::Message;
use stamp::{Diff, Entry, Stamp};

pub mod local;

#[cfg(test)]
mod tests;

/// 暫存內容根目錄底下放 `<ns>.just` 的目錄。
pub const JUST_DIR: &str = "just";
/// `<ns>` 檔的副檔名。
pub const JUST_EXT: &str = ".just";
/// VK 自己的命名空間，不給工具用（04 命名空間）。
pub const RESERVED: &str = "vendor_kit";

// ---------------------------------------------------------------------------
// 輸入

/// 一個工具取到暫存處的內容。
#[derive(Debug, Clone, Copy)]
pub struct Staged<'a> {
    /// 工具名 `<repo>`。
    pub repo: &'a str,
    /// 取件所依據的版本鎖定行的值。
    pub locked: &'a ImageRef,
    /// 暫存內容的根目錄（`dist/` 的內容）。
    pub root: &'a Path,
    /// inspect 回來的 RepoDigests，每筆 `<registry>/<路徑>@sha256:<digest>`。
    pub repo_digests: &'a [String],
}

/// 已經被占用的名字是誰的。
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub enum Owner {
    /// 已裝工具 `<repo>` 交付的 `<ns>`。
    Tool(String),
    /// 根 `justfile` 的 recipe。
    RootRecipe,
    /// 根 `justfile` 的 module。
    RootModule,
    /// 保留名 `vendor_kit`。
    Reserved,
}

impl fmt::Display for Owner {
    /// 填進 VK0030 的 `<owner>`。
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Owner::Tool(repo) => f.write_str(repo),
            Owner::RootRecipe => f.write_str("a recipe in the root justfile"),
            Owner::RootModule => f.write_str("a module in the root justfile"),
            Owner::Reserved => f.write_str(RESERVED),
        }
    }
}

/// 撞名判定的比對對象。[`Taken::new`] 已含保留名 `vendor_kit`。
#[derive(Debug, Clone)]
pub struct Taken {
    names: BTreeSet<(String, Owner)>,
}

impl Default for Taken {
    fn default() -> Self {
        Taken::new()
    }
}

impl Taken {
    /// 只含保留名 `vendor_kit`。
    pub fn new() -> Self {
        let mut names = BTreeSet::new();
        names.insert((RESERVED.to_owned(), Owner::Reserved));
        Taken { names }
    }

    /// 已裝工具 `repo` 交付的全部 `<ns>`。
    pub fn tool<I, S>(&mut self, repo: &str, namespaces: I) -> &mut Self
    where
        I: IntoIterator<Item = S>,
        S: Into<String>,
    {
        for ns in namespaces {
            self.names.insert((ns.into(), Owner::Tool(repo.to_owned())));
        }
        self
    }

    /// 根 `justfile` 的一個 recipe。
    pub fn root_recipe(&mut self, name: impl Into<String>) -> &mut Self {
        self.names.insert((name.into(), Owner::RootRecipe));
        self
    }

    /// 根 `justfile` 的一個 module。
    pub fn root_module(&mut self, name: impl Into<String>) -> &mut Self {
        self.names.insert((name.into(), Owner::RootModule));
        self
    }

    /// `repo` 交付的 `namespaces` 撞到的名字，依名字與擁有者排序；`repo` 自己已裝的不算。
    pub fn collisions(&self, repo: &str, namespaces: &[String]) -> Vec<Collision> {
        let wanted: BTreeSet<&str> = namespaces.iter().map(String::as_str).collect();
        self.names
            .iter()
            .filter(|(name, owner)| {
                wanted.contains(name.as_str()) && !matches!(owner, Owner::Tool(r) if r == repo)
            })
            .map(|(name, owner)| Collision {
                ns: name.clone(),
                owner: owner.clone(),
            })
            .collect()
    }
}

/// 一個撞名：`ns` 已由 `owner` 使用。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Collision {
    pub ns: String,
    pub owner: Owner,
}

// ---------------------------------------------------------------------------
// 驗證

/// 驗過的候選：詢問前算好的逐檔指紋與讀出的 `<ns>`，全部同意後交給 `txn` 落地。
#[derive(Debug, Clone)]
pub struct Candidate {
    repo: String,
    locked: ImageRef,
    root: PathBuf,
    stamp: Stamp,
    namespaces: Vec<String>,
}

impl Candidate {
    /// 工具名 `<repo>`。
    pub fn repo(&self) -> &str {
        &self.repo
    }

    /// 取件所依據的版本鎖定行的值。
    pub fn locked(&self) -> &ImageRef {
        &self.locked
    }

    /// 寫進印記的版本：版本鎖定行的值原文（[`ImageRef`] 的字串形式）。
    pub fn version(&self) -> &str {
        self.stamp.version()
    }

    /// 暫存內容的根目錄。
    pub fn root(&self) -> &Path {
        &self.root
    }

    /// 詢問前算出的逐檔指紋（沒寫成印記檔）。
    pub fn entries(&self) -> &[Entry] {
        self.stamp.entries()
    }

    /// 讀出的全部 `<ns>`，依位元組排序。
    pub fn namespaces(&self) -> &[String] {
        &self.namespaces
    }

    /// 落地前重驗：重算暫存內容，與詢問前算出的檔案集合與逐檔指紋比對。
    pub fn recheck(&self) -> Result<(), Error> {
        let now = Stamp::compute(self.stamp.version(), &self.root).map_err(Error::Fingerprints)?;
        let diff = self.stamp.compare(&now);
        if diff.is_match() {
            Ok(())
        } else {
            Err(Error::Fingerprint(diff))
        }
    }
}

/// 驗一個工具的暫存內容（順序見模組說明）。`previous` 是既有印記；版本與鎖定行相同時才拿來比對。
pub fn verify(
    staged: &Staged,
    taken: &Taken,
    previous: Option<&Stamp>,
) -> Result<Candidate, Error> {
    if !is_namespace(staged.repo) {
        return Err(Error::InvalidRepo(staged.repo.to_owned()));
    }
    check_digest(staged.locked, staged.repo_digests)?;

    let namespaces = namespaces(staged.root).map_err(Error::Format)?;
    if !namespaces.iter().any(|ns| ns == staged.repo) {
        return Err(Error::Format(FormatError::MissingRepoJust(
            staged.repo.to_owned(),
        )));
    }

    let version = staged.locked.to_string();
    let stamp = Stamp::compute(version.as_str(), staged.root).map_err(Error::Fingerprints)?;
    if let Some(prev) = previous.filter(|p| p.version() == version) {
        let diff = prev.compare(&stamp);
        if !diff.is_match() {
            return Err(Error::Fingerprint(diff));
        }
    }

    let collisions = taken.collisions(staged.repo, &namespaces);
    if !collisions.is_empty() {
        return Err(Error::Collision {
            repo: staged.repo.to_owned(),
            collisions,
        });
    }

    Ok(Candidate {
        repo: staged.repo.to_owned(),
        locked: staged.locked.clone(),
        root: staged.root.to_path_buf(),
        stamp,
        namespaces,
    })
}

/// RepoDigests 裡要有一筆與鎖定的 image 名稱與 digest 相同。
fn check_digest(locked: &ImageRef, repo_digests: &[String]) -> Result<(), Error> {
    let want = format!(
        "{}/{}@{}",
        locked.registry(),
        locked.path(),
        locked.digest()
    );
    if repo_digests.contains(&want) {
        Ok(())
    } else {
        Err(Error::DigestMismatch {
            expected: want,
            found: repo_digests.to_vec(),
        })
    }
}

/// 讀出工具內容根目錄 `root` 底下 [`JUST_DIR`] 裡的全部 `<ns>`，依位元組排序。
///
/// 每一項都要是一般檔（不收 symlink 與子目錄）、名為 `<ns>.just`，`<ns>` 是合法的 just 名稱。
/// 暫存內容與已裝工具的 `cache/<repo>/` 都用這一個讀法。
pub fn namespaces(root: &Path) -> Result<Vec<String>, FormatError> {
    let dir = root.join(JUST_DIR);
    match fs::symlink_metadata(&dir) {
        Ok(m) if m.is_dir() => {}
        Ok(_) => return Err(FormatError::NoJustDir),
        Err(e) if e.kind() == io::ErrorKind::NotFound => return Err(FormatError::NoJustDir),
        Err(source) => return Err(FormatError::Io { path: dir, source }),
    }
    let read = fs::read_dir(&dir).map_err(|source| FormatError::Io {
        path: dir.clone(),
        source,
    })?;
    let mut out = Vec::new();
    for item in read {
        let item = item.map_err(|source| FormatError::Io {
            path: dir.clone(),
            source,
        })?;
        let name = item.file_name();
        let shown = name.to_string_lossy().into_owned();
        let ty = item.file_type().map_err(|source| FormatError::Io {
            path: item.path(),
            source,
        })?;
        if !ty.is_file() {
            return Err(FormatError::NotAFile(shown));
        }
        let ns = name
            .to_str()
            .and_then(|n| n.strip_suffix(JUST_EXT))
            .ok_or_else(|| FormatError::NotJustFile(shown.clone()))?;
        if !is_namespace(ns) {
            return Err(FormatError::InvalidNamespace(shown));
        }
        out.push(ns.to_owned());
    }
    out.sort();
    Ok(out)
}

/// 讀已裝工具的 `cache/<repo>/`（`cache` 是那個目錄）裡的全部 `<ns>`，讀不到時分成兩種（N4）：
///
/// - `cache/<repo>/` 本身不在（全新 checkout 還沒 `sync`、手動刪掉）：[`CacheError::Missing`]，`sync` 補得好。
/// - 在，但讀不到或內容不合交付格式（權限、損壞）：[`CacheError::Unreadable`]，保留實際原因。
pub fn cached_namespaces(cache: &Path) -> Result<Vec<String>, CacheError> {
    match fs::symlink_metadata(cache) {
        Ok(_) => namespaces(cache).map_err(CacheError::Unreadable),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Err(CacheError::Missing),
        Err(source) => Err(CacheError::Unreadable(FormatError::Io {
            path: cache.to_path_buf(),
            source,
        })),
    }
}

/// 收齊一次執行裡讀不到 `cache/<repo>/` 的已裝工具（N4），在任何寫入之前一起報。
///
/// 草稿碼 VK0068（`cache/<repo>/` 不在，下一步 `sync`）與 VK0073（VK 管的檔讀不到）登錄前，呼叫端以 VK0056
/// 停下，`<reason>` 用 [`CacheCheck::reasons`]：缺的工具合成一則、結尾是 [`DRAFT_CACHE_MISSING`]；讀不到的
/// 每個工具一則、結尾是 [`DRAFT_CACHE_UNREADABLE`]。
#[derive(Debug, Default)]
pub struct CacheCheck {
    missing: Vec<String>,
    unreadable: Vec<(String, FormatError)>,
}

impl CacheCheck {
    /// 記下一個讀不到的工具。
    pub fn push(&mut self, repo: &str, e: CacheError) {
        match e {
            CacheError::Missing => self.missing.push(repo.to_owned()),
            CacheError::Unreadable(e) => self.unreadable.push((repo.to_owned(), e)),
        }
    }

    /// 全部讀得到。
    pub fn is_empty(&self) -> bool {
        self.missing.is_empty() && self.unreadable.is_empty()
    }

    /// 每則 VK0056 的 `<reason>`：缺的工具（依記下的順序）合成一則在前，讀不到的每個工具各一則在後。
    pub fn reasons(&self) -> Vec<String> {
        let mut out = Vec::new();
        if !self.missing.is_empty() {
            let dirs: Vec<String> = self
                .missing
                .iter()
                .map(|r| format!(".vendor_kit/cache/{r}/"))
                .collect();
            out.push(format!(
                "the cache of installed tools is missing: {}; run just vendor_kit sync first; \
                 {DRAFT_CACHE_MISSING}",
                dirs.join(", ")
            ));
        }
        for (repo, e) in &self.unreadable {
            out.push(format!(
                "the cache of installed tool {repo} (.vendor_kit/cache/{repo}/) cannot be read: {e}; \
                 {DRAFT_CACHE_UNREADABLE}"
            ));
        }
        out
    }
}

/// `cache/<repo>/` 不在：草稿碼 VK0068（N4）登錄前，以 VK0056 停下時 `<reason>` 的結尾。
pub const DRAFT_CACHE_MISSING: &str = "reason code pending (draft VK0068, N4)";
/// `cache/<repo>/` 讀不到或損壞：草稿碼 VK0073（N4）登錄前，以 VK0056 停下時 `<reason>` 的結尾。
pub const DRAFT_CACHE_UNREADABLE: &str = "reason code pending (draft VK0073, N4)";

/// just 的名稱：`[A-Za-z_][A-Za-z0-9_-]*`。
pub fn is_namespace(s: &str) -> bool {
    let mut b = s.bytes();
    b.next()
        .is_some_and(|c| c.is_ascii_alphabetic() || c == b'_')
        && b.all(|c| c.is_ascii_alphanumeric() || c == b'_' || c == b'-')
}

// ---------------------------------------------------------------------------
// 錯誤

/// dist 格式不符（#372 計畫的 G2，目前沒有代碼）。
#[derive(Debug)]
pub enum FormatError {
    /// 根目錄底下沒有 [`JUST_DIR`] 目錄（不在、是一般檔或 symlink）。
    NoJustDir,
    /// [`JUST_DIR`] 底下有子目錄、symlink 或其他非一般檔。
    NotAFile(String),
    /// [`JUST_DIR`] 底下的檔名不是 `<ns>.just`。
    NotJustFile(String),
    /// `<ns>` 不是合法的 just 名稱。
    InvalidNamespace(String),
    /// `<repo>.just` 不在。
    MissingRepoJust(String),
    /// 讀目錄的系統呼叫失敗。
    Io { path: PathBuf, source: io::Error },
}

impl fmt::Display for FormatError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            FormatError::NoJustDir => write!(f, "dist has no {JUST_DIR}/ directory"),
            FormatError::NotAFile(n) => write!(f, "{JUST_DIR}/{n} is not a regular file"),
            FormatError::NotJustFile(n) => {
                write!(f, "{JUST_DIR}/{n} is not named <ns>{JUST_EXT}")
            }
            FormatError::InvalidNamespace(n) => {
                write!(f, "{JUST_DIR}/{n} is not a valid just namespace")
            }
            FormatError::MissingRepoJust(repo) => {
                write!(f, "{JUST_DIR}/{repo}{JUST_EXT} is missing")
            }
            FormatError::Io { path, source } => write!(f, "{}: {source}", path.display()),
        }
    }
}

impl std::error::Error for FormatError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            FormatError::Io { source, .. } => Some(source),
            _ => None,
        }
    }
}

/// [`cached_namespaces`] 讀不到已裝工具的 `cache/<repo>/`。
#[derive(Debug)]
pub enum CacheError {
    /// `cache/<repo>/` 不在：先 `sync`（草稿碼 VK0068）。
    Missing,
    /// `cache/<repo>/` 在，但讀不到或不合交付格式：`sync` 不一定修得好，保留實際原因（草稿碼 VK0073）。
    Unreadable(FormatError),
}

impl fmt::Display for CacheError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            CacheError::Missing => write!(f, "the cache directory does not exist"),
            CacheError::Unreadable(e) => e.fmt(f),
        }
    }
}

/// [`verify`] 或 [`Candidate::recheck`] 失敗。
#[derive(Debug)]
pub enum Error {
    /// `<repo>` 不是合法的 just 名稱（`<repo>.just` 必須是一個 `<ns>`）。
    InvalidRepo(String),
    /// RepoDigests 沒有一筆與鎖定的 image 名稱與 digest 相同（G1）。
    DigestMismatch {
        /// 要找的 `<registry>/<路徑>@sha256:<digest>`。
        expected: String,
        /// inspect 回來的 RepoDigests。
        found: Vec<String>,
    },
    /// dist 格式不符（G2）。
    Format(FormatError),
    /// 算逐檔指紋失敗：symlink、非一般檔、非 UTF-8 路徑或讀檔失敗。
    Fingerprints(stamp::ComputeError),
    /// 檔案集合或逐檔指紋不符：多出的檔、少掉的檔、內容不同的檔分開列（G1）。
    Fingerprint(Diff),
    /// `<ns>` 撞名（VK0030）；列出每一個撞到的名字。
    Collision {
        repo: String,
        collisions: Vec<Collision>,
    },
}

impl Error {
    /// 對應的訊息表條目：撞名是 VK0030；其餘目前沒有代碼（G1、G2），回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            Error::Collision { .. } => Some(&messages::VK0030),
            Error::InvalidRepo(_)
            | Error::DigestMismatch { .. }
            | Error::Format(_)
            | Error::Fingerprints(_)
            | Error::Fingerprint(_) => None,
        }
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::InvalidRepo(repo) => write!(f, "invalid tool name {repo:?}"),
            Error::DigestMismatch { expected, found } => {
                write!(f, "no repo digest matches {expected}; found {found:?}")
            }
            Error::Format(e) => write!(f, "invalid dist layout: {e}"),
            Error::Fingerprints(e) => e.fmt(f),
            Error::Fingerprint(d) => write!(
                f,
                "staged content does not match per-file digests: extra {:?}, missing {:?}, changed {:?}",
                d.extra, d.missing, d.changed
            ),
            Error::Collision { repo, collisions } => {
                write!(f, "cannot add {repo}:")?;
                for c in collisions {
                    write!(f, " namespace {} is already used by {};", c.ns, c.owner)?;
                }
                Ok(())
            }
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Error::Format(e) => Some(e),
            Error::Fingerprints(e) => Some(e),
            _ => None,
        }
    }
}
