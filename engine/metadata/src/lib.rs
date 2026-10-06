//! `.vendor_kit/baseline/` 下的逐檔紀錄（ADR-0003 內部機制）。
//!
//! - 每個工具一份 `baseline/<repo>.toml`；根 `.dockerignore` 那四行不屬於任何工具，記在
//!   `baseline/.vendor_kit.toml`。兩種檔格式相同：每個初始檔一筆 `[[file]]`，同一份檔裡同一個
//!   `path` 只能有一筆。
//! - `[[file]]` 的欄位：`path`（repo 相對路徑）、`state`（`managed`／`appended`／`declined`／
//!   `unmanaged`／`deleted`）、`lines`（實際插入的行原文，不記位置、不加標記）、`hash`（VK 最後一次
//!   寫入後的整檔 hash）、`declined_hash`（使用者拒絕的那一版）。`state`、`declined_hash` 與 `hash`
//!   是持久格式；hash 一律是 CRLF→LF 正規化後的 sha256（[`files::fingerprint_normalized`]）。
//! - 根層的 `conflicts`（scope_roadmap:32）：基準版合併的結果是 TOML／just 而解析不過、所以留原檔、
//!   該檔基準版不推的初始檔，以 repo 相對路徑的字串陣列記下，順序同加入的先後、不重複。之後那個檔
//!   合併寫入成功就從清單拿掉；清單空了就刪掉這個鍵（[`Metadata::set_conflict`]）。
//! - 寫入規則（[`Metadata::record_write`]）：VK 寫入某檔前，紀錄的 hash 與寫入前的內容相符，才更新成
//!   寫入後的 hash；不相符或沒有 hash 的紀錄保留原值，不拿這次寫入後的 hash 補上。
//! - 讀寫經 `schema`：檔案版過高回 VK0008；未知欄位（含 `[[file]]` 裡的）讀時忽略、寫時保留。
//! - 紀錄缺失（檔不在）或損壞（語法、`schema`、欄位型別或值不合）都回 VK0013，不猜、不補。
//!   首次建立紀錄用 [`Metadata::new`]，不經讀檔。
//!
//! 這裡不印診斷；要怎麼印由呼叫端經 `diagnostics` 決定，`<file>` 以外的欄位也由呼叫端填。

use std::collections::BTreeSet;
use std::fmt;
use std::fs;
use std::io;
use std::path::{Component, Path, PathBuf};

use files::Fingerprint;
use layout::{InstallDir, InvalidName, NameKind};
use messages::Message;
use schema::{Document, ReadError, TooNew, WriteError};
use toml_edit::{Array, Item, Table};

/// 逐檔紀錄的陣列表名。
pub const FILE_KEY: &str = "file";
/// 初始檔的 repo 相對路徑。
pub const PATH_KEY: &str = "path";
/// 納管狀態。
pub const STATE_KEY: &str = "state";
/// 插入行的原文。
pub const LINES_KEY: &str = "lines";
/// VK 最後一次寫入後的整檔 hash。
pub const HASH_KEY: &str = "hash";
/// 使用者拒絕的版本的 hash。
pub const DECLINED_HASH_KEY: &str = "declined_hash";
/// 根層：合併結果解析不過、留原檔且基準版沒推的初始檔（scope_roadmap:32）。
pub const CONFLICTS_KEY: &str = "conflicts";

/// `baseline/<repo>.toml`：工具 `<repo>` 的逐檔紀錄。
///
/// `<repo>` 必須是單一路徑段，且不以 `.` 開頭，才不會跟 `baseline/.vendor_kit.toml` 撞名。
pub fn tool_path(dir: &InstallDir, repo: &str) -> Result<PathBuf, InvalidName> {
    if repo.is_empty() || repo.starts_with('.') || repo.contains(['/', '\0']) {
        return Err(InvalidName {
            kind: NameKind::Repo,
            name: repo.to_owned(),
        });
    }
    Ok(dir.baseline_dir().join(format!("{repo}.toml")))
}

/// `baseline/.vendor_kit.toml`：不屬於任何工具的紀錄（根 `.dockerignore` 的四行）。
pub fn vk_path(dir: &InstallDir) -> PathBuf {
    dir.baseline_vk()
}

// ---------------------------------------------------------------------------
// 紀錄

/// 初始檔的納管狀態。
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum State {
    /// 整份由 VK 建立並納管，升級時做基準版合併。
    Managed,
    /// append 型：VK 只在既有檔插入了 `lines`。
    Appended,
    /// 使用者拒絕了 `declined_hash` 那一版。
    Declined,
    /// 已存在但不納管，後續不做基準版合併。
    Unmanaged,
    /// 使用者已刪掉這個納管初始檔；不重建。
    Deleted,
}

impl State {
    /// 全部狀態，順序固定。
    pub const ALL: [State; 5] = [
        State::Managed,
        State::Appended,
        State::Declined,
        State::Unmanaged,
        State::Deleted,
    ];

    /// 寫在檔裡的字。
    pub const fn as_str(self) -> &'static str {
        match self {
            State::Managed => "managed",
            State::Appended => "appended",
            State::Declined => "declined",
            State::Unmanaged => "unmanaged",
            State::Deleted => "deleted",
        }
    }

    /// 由檔裡的字解析；不認得回 `None`。
    pub fn parse(s: &str) -> Option<State> {
        State::ALL.into_iter().find(|st| st.as_str() == s)
    }
}

impl fmt::Display for State {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

/// 整檔 hash：CRLF→LF 正規化後 sha256 的小寫十六進位，64 字元。
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct FileHash(String);

impl FileHash {
    /// 內容的 hash（先把 CRLF 正規化成 LF）。
    pub fn of(contents: &[u8]) -> FileHash {
        FileHash::from(files::fingerprint_normalized(contents))
    }

    /// 由檔裡的字解析；不是 64 個小寫十六進位字元回 `None`。
    pub fn parse(s: &str) -> Option<FileHash> {
        let ok = s.len() == 64 && s.bytes().all(|b| matches!(b, b'0'..=b'9' | b'a'..=b'f'));
        ok.then(|| FileHash(s.to_owned()))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl From<Fingerprint> for FileHash {
    fn from(fp: Fingerprint) -> Self {
        FileHash(fp.to_hex())
    }
}

impl fmt::Display for FileHash {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.0)
    }
}

/// 一筆 `[[file]]`。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FileRecord {
    /// repo 相對路徑。
    pub path: String,
    pub state: State,
    /// 實際插入的行原文，不含行尾；沒有插入行時是空的。
    pub lines: Vec<String>,
    /// VK 最後一次寫入後的整檔 hash；舊紀錄可能沒有。
    pub hash: Option<FileHash>,
    /// 使用者拒絕的版本。
    pub declined_hash: Option<FileHash>,
}

impl FileRecord {
    /// 只有路徑與狀態的紀錄。
    pub fn new(path: impl Into<String>, state: State) -> Self {
        FileRecord {
            path: path.into(),
            state,
            lines: Vec::new(),
            hash: None,
            declined_hash: None,
        }
    }
}

/// [`Metadata::record_write`] 對一筆紀錄做了什麼。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum WriteOutcome {
    /// 寫入前相符，已更新成寫入後的 hash。
    Updated,
    /// 寫入前就不相符，保留原 hash。
    Mismatch,
    /// 紀錄沒有 hash，不補。
    NoHash,
    /// 這份檔沒有這個路徑的紀錄。
    NoRecord,
}

// ---------------------------------------------------------------------------
// 檔

/// 一份逐檔紀錄檔。
#[derive(Debug, Clone)]
pub struct Metadata {
    doc: Document,
    /// 與 `[[file]]` 同順序，`records[i]` 就是第 `i` 個表。
    records: Vec<FileRecord>,
    /// 根層 `conflicts`，順序同檔裡。
    conflicts: Vec<String>,
}

impl Metadata {
    /// 新的空紀錄檔（首次建立紀錄時用）。
    pub fn new() -> Metadata {
        Metadata {
            doc: Document::new(),
            records: Vec::new(),
            conflicts: Vec::new(),
        }
    }

    /// 讀紀錄檔。檔不在回 [`Error::Missing`]（VK0013）；首次建立紀錄改用 [`Metadata::new`]。
    pub fn load(path: &Path) -> Result<Metadata, Error> {
        let text = match fs::read_to_string(path) {
            Ok(text) => text,
            Err(e) if e.kind() == io::ErrorKind::NotFound => {
                return Err(Error::Missing {
                    file: path.to_path_buf(),
                });
            }
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
        Metadata::parse(&text).map_err(|e| e.at(path))
    }

    /// 解析紀錄檔內容：先過 `schema` 的讀取門檻，再逐筆檢查 `[[file]]`。
    pub fn parse(text: &str) -> Result<Metadata, ParseError> {
        let doc = Document::parse(text).map_err(|e| match e {
            ReadError::TooNew(t) => ParseError::TooNew(t),
            other => ParseError::Invalid(Invalid::new(other.to_string())),
        })?;
        let records = read_records(&doc).map_err(ParseError::Invalid)?;
        let conflicts = read_conflicts(&doc).map_err(ParseError::Invalid)?;
        Ok(Metadata {
            doc,
            records,
            conflicts,
        })
    }

    /// 全部紀錄，順序同檔裡的 `[[file]]`。
    pub fn files(&self) -> &[FileRecord] {
        &self.records
    }

    /// `path` 的紀錄。
    pub fn get(&self, path: &str) -> Option<&FileRecord> {
        self.records.iter().find(|r| r.path == path)
    }

    /// 根層 `conflicts`：合併結果解析不過、留原檔且基準版沒推的初始檔，順序同檔裡。
    pub fn conflicts(&self) -> &[String] {
        &self.conflicts
    }

    /// 把 `path` 加進（`conflicted` 是 `true`）或移出（`false`）根層 `conflicts`；回傳清單有沒有變。
    /// 加進時接在最後，已在清單裡就不動；移出後清單空了就刪掉這個鍵。
    pub fn set_conflict(&mut self, path: &str, conflicted: bool) -> Result<bool, PutError> {
        check_path(path).map_err(PutError::Invalid)?;
        let present = self.conflicts.iter().any(|p| p == path);
        if present == conflicted {
            return Ok(false);
        }
        let mut next = self.conflicts.clone();
        if conflicted {
            next.push(path.to_owned());
        } else {
            next.retain(|p| p != path);
        }
        if next.is_empty() {
            self.doc.remove(&[CONFLICTS_KEY])?;
        } else {
            let array: Array = next.iter().map(String::as_str).collect();
            self.doc.set(&[CONFLICTS_KEY], array)?;
        }
        self.conflicts = next;
        Ok(true)
    }

    /// 新增或換掉 `record.path` 的紀錄。只改有變的欄位，同一筆裡的未知欄位與其他筆都保留。
    pub fn put(&mut self, record: FileRecord) -> Result<(), PutError> {
        check_path(&record.path).map_err(PutError::Invalid)?;
        let (index, old) = match self.records.iter().position(|r| r.path == record.path) {
            Some(i) => (i, Some(self.records[i].clone())),
            None => {
                let i = self.doc.push_table(FILE_KEY)?;
                (i, None)
            }
        };
        let old = old.as_ref();
        if old.map(|o| &o.path) != Some(&record.path) {
            self.doc
                .set_in(FILE_KEY, index, PATH_KEY, record.path.as_str())?;
        }
        if old.map(|o| o.state) != Some(record.state) {
            self.doc
                .set_in(FILE_KEY, index, STATE_KEY, record.state.as_str())?;
        }
        if old.map(|o| &o.lines) != Some(&record.lines) {
            if record.lines.is_empty() {
                self.doc.remove_in(FILE_KEY, index, LINES_KEY)?;
            } else {
                let lines: Array = record.lines.iter().map(String::as_str).collect();
                self.doc.set_in(FILE_KEY, index, LINES_KEY, lines)?;
            }
        }
        self.put_hash(index, HASH_KEY, old.map(|o| &o.hash), &record.hash)?;
        self.put_hash(
            index,
            DECLINED_HASH_KEY,
            old.map(|o| &o.declined_hash),
            &record.declined_hash,
        )?;
        if index == self.records.len() {
            self.records.push(record);
        } else {
            self.records[index] = record;
        }
        Ok(())
    }

    fn put_hash(
        &mut self,
        index: usize,
        key: &str,
        old: Option<&Option<FileHash>>,
        new: &Option<FileHash>,
    ) -> Result<(), WriteError> {
        if old == Some(new) || (old.is_none() && new.is_none()) {
            return Ok(());
        }
        match new {
            Some(h) => self.doc.set_in(FILE_KEY, index, key, h.as_str()),
            None => self.doc.remove_in(FILE_KEY, index, key).map(|_| ()),
        }
    }

    /// VK 把 `path` 從 `before` 寫成 `after` 時更新這份檔裡該路徑的紀錄（ADR-0003）：
    /// 紀錄的 hash 與 `before` 相符才換成 `after` 的 hash；不相符或沒有 hash 都保留原值。
    ///
    /// 新插入的紀錄不經這裡：建紀錄時直接把 `hash` 設成 [`FileHash::of`]`(after)` 再 [`Metadata::put`]。
    /// 同一個檔可能出現在好幾份紀錄檔裡（各工具與 `.vendor_kit.toml`），呼叫端要對每一份都以
    /// 同一份 `before` 呼叫，判定才都以寫入前的內容為準。
    pub fn record_write(
        &mut self,
        path: &str,
        before: &[u8],
        after: &[u8],
    ) -> Result<WriteOutcome, WriteError> {
        let Some(index) = self.records.iter().position(|r| r.path == path) else {
            return Ok(WriteOutcome::NoRecord);
        };
        let Some(hash) = &self.records[index].hash else {
            return Ok(WriteOutcome::NoHash);
        };
        if *hash != FileHash::of(before) {
            return Ok(WriteOutcome::Mismatch);
        }
        let new = FileHash::of(after);
        if *hash != new {
            self.doc.set_in(FILE_KEY, index, HASH_KEY, new.as_str())?;
            self.records[index].hash = Some(new);
        }
        Ok(WriteOutcome::Updated)
    }

    /// 蓋上寫入者，確認沒有少寫後回傳要寫回的內容。
    pub fn render(&mut self, written_by: &str) -> Result<String, WriteError> {
        self.doc.render(written_by)
    }

    /// 原子寫回 `path`；`baseline/` 不在時先建。
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

impl Default for Metadata {
    fn default() -> Self {
        Metadata::new()
    }
}

fn read_records(doc: &Document) -> Result<Vec<FileRecord>, Invalid> {
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
    let mut records = Vec::with_capacity(tables.len());
    for (i, table) in tables.iter().enumerate() {
        let record = read_record(table).map_err(|e| e.in_entry(i))?;
        if !seen.insert(record.path.clone()) {
            return Err(Invalid::new(format!("duplicate path {:?}", record.path)).in_entry(i));
        }
        records.push(record);
    }
    Ok(records)
}

fn read_conflicts(doc: &Document) -> Result<Vec<String>, Invalid> {
    let Some(item) = present(doc.get(&[CONFLICTS_KEY])) else {
        return Ok(Vec::new());
    };
    let bad = || Invalid::new(format!("`{CONFLICTS_KEY}` is not an array of strings"));
    let mut seen = BTreeSet::new();
    let mut out = Vec::new();
    for v in item.as_array().ok_or_else(bad)? {
        let path = v.as_str().ok_or_else(bad)?;
        check_path(path).map_err(|e| Invalid::new(format!("`{CONFLICTS_KEY}`: {e}")))?;
        if !seen.insert(path) {
            return Err(Invalid::new(format!(
                "`{CONFLICTS_KEY}` lists {path:?} twice"
            )));
        }
        out.push(path.to_owned());
    }
    Ok(out)
}

fn read_record(table: &Table) -> Result<FileRecord, Invalid> {
    let path = required_str(table, PATH_KEY)?;
    check_path(path)?;
    let state_str = required_str(table, STATE_KEY)?;
    let state = State::parse(state_str)
        .ok_or_else(|| Invalid::new(format!("unknown `{STATE_KEY}` {state_str:?}")))?;
    let lines = match present(table.get(LINES_KEY)) {
        None => Vec::new(),
        Some(item) => {
            let bad = || Invalid::new(format!("`{LINES_KEY}` is not an array of strings"));
            item.as_array()
                .ok_or_else(bad)?
                .iter()
                .map(|v| v.as_str().map(str::to_owned).ok_or_else(bad))
                .collect::<Result<Vec<_>, _>>()?
        }
    };
    Ok(FileRecord {
        path: path.to_owned(),
        state,
        lines,
        hash: optional_hash(table, HASH_KEY)?,
        declined_hash: optional_hash(table, DECLINED_HASH_KEY)?,
    })
}

fn present(item: Option<&Item>) -> Option<&Item> {
    item.filter(|i| !i.is_none())
}

fn required_str<'a>(table: &'a Table, key: &str) -> Result<&'a str, Invalid> {
    match present(table.get(key)) {
        None => Err(Invalid::new(format!("missing `{key}`"))),
        Some(item) => item
            .as_str()
            .ok_or_else(|| Invalid::new(format!("`{key}` is not a string"))),
    }
}

fn optional_hash(table: &Table, key: &str) -> Result<Option<FileHash>, Invalid> {
    match present(table.get(key)) {
        None => Ok(None),
        Some(item) => item
            .as_str()
            .and_then(FileHash::parse)
            .map(Some)
            .ok_or_else(|| {
                Invalid::new(format!(
                    "`{key}` is not a 64-character lowercase hex sha256"
                ))
            }),
    }
}

/// repo 相對路徑：非空、不是絕對路徑、不含 `..`、`.` 或 NUL，跳不出 repo。
fn check_path(path: &str) -> Result<(), Invalid> {
    let bad = || {
        Invalid::new(format!(
            "`{PATH_KEY}` is not a plain repo-relative path: {path:?}"
        ))
    };
    if path.is_empty() || path.contains('\0') || path.ends_with('/') {
        return Err(bad());
    }
    let p = Path::new(path);
    if !p.components().all(|c| matches!(c, Component::Normal(_)))
        || path.split('/').any(|seg| seg.is_empty() || seg == ".")
    {
        return Err(bad());
    }
    Ok(())
}

// ---------------------------------------------------------------------------
// 錯誤

/// 紀錄內容不合：語法、`schema` 或 `[[file]]` 的欄位。
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

/// [`Metadata::parse`] 失敗。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ParseError {
    /// 檔案版過高（VK0008）。
    TooNew(TooNew),
    /// 紀錄損壞（VK0013）。
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
            ParseError::Invalid(_) => &messages::VK0013,
        }
    }
}

impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ParseError::TooNew(t) => t.fmt(f),
            ParseError::Invalid(e) => write!(f, "corrupt metadata: {e}"),
        }
    }
}

impl std::error::Error for ParseError {}

/// [`Metadata::put`] 失敗：紀錄本身不合，或寫進文件樹時會蓋掉保留不了的內容。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PutError {
    Invalid(Invalid),
    Write(WriteError),
}

impl From<WriteError> for PutError {
    fn from(e: WriteError) -> Self {
        PutError::Write(e)
    }
}

impl fmt::Display for PutError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            PutError::Invalid(e) => write!(f, "invalid record: {e}"),
            PutError::Write(e) => e.fmt(f),
        }
    }
}

impl std::error::Error for PutError {}

/// 讀寫紀錄檔失敗。
#[derive(Debug)]
pub enum Error {
    /// 紀錄檔不在（VK0013）。
    Missing { file: PathBuf },
    /// 紀錄檔損壞（VK0013）。
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
    /// 填訊息 `<file>` 的路徑。
    pub fn file(&self) -> &Path {
        match self {
            Error::Missing { file }
            | Error::Corrupt { file, .. }
            | Error::TooNew { file, .. }
            | Error::Io { file, .. }
            | Error::Render { file, .. } => file,
            Error::Write(e) => e.path(),
        }
    }

    /// 對應的訊息表條目：缺失或損壞是 VK0013，檔案版過高是 VK0008；系統呼叫失敗還沒有代碼，回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            Error::Missing { .. } | Error::Corrupt { .. } => Some(&messages::VK0013),
            Error::TooNew { too_new, .. } => Some(too_new.message()),
            Error::Io { .. } | Error::Render { .. } | Error::Write(_) => None,
        }
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Missing { file } => write!(f, "metadata missing: {}", file.display()),
            Error::Corrupt { file, reason } => {
                write!(f, "corrupt metadata {}: {reason}", file.display())
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
            Error::Io { source, .. } => Some(source),
            Error::Render { source, .. } => Some(source),
            Error::Write(e) => Some(e),
            Error::Corrupt { reason, .. } => Some(reason),
            Error::TooNew { .. } | Error::Missing { .. } => None,
        }
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    fn hash(contents: &str) -> FileHash {
        FileHash::of(contents.as_bytes())
    }

    fn record(path: &str, state: State) -> FileRecord {
        let mut r = FileRecord::new(path, state);
        match state {
            State::Appended => {
                r.lines = vec!["target/".to_owned(), "*.log".to_owned()];
                r.hash = Some(hash("a\ntarget/\n*.log\n"));
            }
            State::Declined => {
                r.hash = Some(hash("mine\n"));
                r.declined_hash = Some(hash("theirs\n"));
            }
            State::Managed => r.hash = Some(hash("init\n")),
            State::Unmanaged | State::Deleted => {}
        }
        r
    }

    #[test]
    fn every_state_round_trips() {
        let mut md = Metadata::new();
        let want: Vec<FileRecord> = State::ALL
            .into_iter()
            .map(|st| record(&format!("dir/{st}.txt"), st))
            .collect();
        for r in &want {
            md.put(r.clone()).unwrap();
        }
        let text = md.render("v0.1.0").unwrap();
        let again = Metadata::parse(&text).unwrap();
        assert_eq!(again.files(), &want[..]);
        for st in State::ALL {
            assert!(text.contains(&format!("state = \"{st}\"")), "{text}");
            assert_eq!(State::parse(st.as_str()), Some(st));
        }
    }

    #[test]
    fn record_write_updates_only_matching_hash() {
        let before = "a\ntarget/\n";
        let after = "a\ntarget/\nnew\n";
        let mut md = Metadata::new();
        let mut r = FileRecord::new(".gitignore", State::Appended);
        r.lines = vec!["target/".to_owned()];
        r.hash = Some(hash(before));
        md.put(r).unwrap();
        assert_eq!(
            md.record_write(".gitignore", before.as_bytes(), after.as_bytes()),
            Ok(WriteOutcome::Updated)
        );
        assert_eq!(md.get(".gitignore").unwrap().hash, Some(hash(after)));
        let text = md.render("v0.1.0").unwrap();
        assert_eq!(
            Metadata::parse(&text)
                .unwrap()
                .get(".gitignore")
                .unwrap()
                .hash,
            Some(hash(after))
        );
    }

    #[test]
    fn record_write_keeps_mismatched_hash() {
        let recorded = "a\ntarget/\n";
        let user_edited = "a\ntarget/\nmine\n";
        let mut md = Metadata::new();
        let mut r = FileRecord::new(".gitignore", State::Appended);
        r.hash = Some(hash(recorded));
        md.put(r).unwrap();
        let mut md = Metadata::parse(&md.render("v0.1.0").unwrap()).unwrap();
        let before_text = md.render("v0.1.0").unwrap();
        assert_eq!(
            md.record_write(
                ".gitignore",
                user_edited.as_bytes(),
                "a\ntarget/\nmine\nvk\n".as_bytes()
            ),
            Ok(WriteOutcome::Mismatch)
        );
        assert_eq!(md.get(".gitignore").unwrap().hash, Some(hash(recorded)));
        assert_eq!(md.render("v0.1.0").unwrap(), before_text);
    }

    #[test]
    fn record_write_does_not_backfill_missing_hash() {
        let text = "schema = 1\nwritten_by = \"v0.0.1\"\n\n[[file]]\npath = \".dockerignore\"\nstate = \"appended\"\nlines = [\".git\"]\n";
        let mut md = Metadata::parse(text).unwrap();
        assert_eq!(
            md.record_write(".dockerignore", b".git\n", b".git\nmore\n"),
            Ok(WriteOutcome::NoHash)
        );
        assert_eq!(md.get(".dockerignore").unwrap().hash, None);
        assert_eq!(
            md.record_write("other", b"", b"x"),
            Ok(WriteOutcome::NoRecord)
        );
        assert_eq!(md.render("v0.0.1").unwrap(), text);
    }

    #[test]
    fn record_write_treats_crlf_as_lf() {
        let mut md = Metadata::new();
        let mut r = FileRecord::new(".editorconfig", State::Appended);
        r.hash = Some(hash("root = true\n"));
        md.put(r).unwrap();
        assert_eq!(
            md.record_write(".editorconfig", b"root = true\r\n", b"root = true\r\nx\r\n"),
            Ok(WriteOutcome::Updated)
        );
        assert_eq!(
            md.get(".editorconfig").unwrap().hash,
            Some(hash("root = true\nx\n"))
        );
    }

    #[test]
    fn same_file_in_two_metadata_files_is_judged_separately() {
        // 工具的紀錄跟上 VK 上次寫入；`.vendor_kit.toml` 的紀錄是使用者改過之前的，寫入前就不符。
        let before = ".git\ntarget/\n";
        let after = ".git\ntarget/\nnode_modules/\n";
        let mut tool = Metadata::new();
        let mut r = FileRecord::new(".dockerignore", State::Appended);
        r.hash = Some(hash(before));
        tool.put(r).unwrap();
        let mut vk = Metadata::new();
        let mut r = FileRecord::new(".dockerignore", State::Appended);
        r.hash = Some(hash(".git\n"));
        vk.put(r).unwrap();
        let outcomes: Vec<WriteOutcome> = [&mut tool, &mut vk]
            .into_iter()
            .map(|md| {
                md.record_write(".dockerignore", before.as_bytes(), after.as_bytes())
                    .unwrap()
            })
            .collect();
        assert_eq!(outcomes, [WriteOutcome::Updated, WriteOutcome::Mismatch]);
        assert_eq!(tool.get(".dockerignore").unwrap().hash, Some(hash(after)));
        assert_eq!(vk.get(".dockerignore").unwrap().hash, Some(hash(".git\n")));
    }

    #[test]
    fn put_keeps_unknown_fields_and_other_entries() {
        let text = format!(
            "schema = 1\nwritten_by = \"v0.1.0\"\nlater = [\"x\"]\n\n[[file]]\npath = \"a\"\nstate = \"managed\" # keep\nhash = \"{}\"\nfuture = 1\n\n[[file]]\npath = \"b\"\nstate = \"unmanaged\"\nnote = \"later\"\n",
            hash("a\n")
        );
        let mut md = Metadata::parse(&text).unwrap();
        let mut a = md.get("a").unwrap().clone();
        a.state = State::Declined;
        a.declined_hash = Some(hash("new\n"));
        md.put(a.clone()).unwrap();
        let out = md.render("v0.2.0").unwrap();
        assert!(out.contains("future = 1"), "{out}");
        assert!(out.contains("note = \"later\""), "{out}");
        assert!(out.contains("later = [\"x\"]"), "{out}");
        assert!(out.contains("state = \"declined\" # keep"), "{out}");
        let again = Metadata::parse(&out).unwrap();
        assert_eq!(again.get("a"), Some(&a));
        assert_eq!(again.get("b").unwrap().state, State::Unmanaged);
    }

    #[test]
    fn put_clears_fields_that_become_empty() {
        let mut md = Metadata::new();
        md.put(record("x", State::Declined)).unwrap();
        let mut r = md.get("x").unwrap().clone();
        r.state = State::Managed;
        r.declined_hash = None;
        md.put(r.clone()).unwrap();
        let out = md.render("v0.1.0").unwrap();
        assert!(!out.contains(DECLINED_HASH_KEY), "{out}");
        assert_eq!(Metadata::parse(&out).unwrap().files(), &[r]);
    }

    #[test]
    fn put_rejects_bad_path() {
        let mut md = Metadata::new();
        for p in ["", "/etc/passwd", "../x", "a/../b", "./a", "a//b", "a/"] {
            assert!(
                matches!(
                    md.put(FileRecord::new(p, State::Managed)),
                    Err(PutError::Invalid(_))
                ),
                "{p:?}"
            );
        }
        assert!(md.files().is_empty());
    }

    #[test]
    fn conflicts_round_trip_and_key_goes_away_when_empty() {
        let text = "schema = 1\nwritten_by = \"v0.1.0\"\nfuture = 1\n\n[[file]]\npath = \"a\"\nstate = \"managed\"\n";
        let mut md = Metadata::parse(text).unwrap();
        assert!(md.conflicts().is_empty());
        assert!(md.set_conflict("config.toml", true).unwrap());
        assert!(md.set_conflict("justfile", true).unwrap());
        assert!(!md.set_conflict("config.toml", true).unwrap());
        let out = md.render("v0.2.0").unwrap();
        assert!(
            out.contains("conflicts = [\"config.toml\", \"justfile\"]"),
            "{out}"
        );
        assert!(out.contains("future = 1"), "{out}");
        let mut again = Metadata::parse(&out).unwrap();
        assert_eq!(again.conflicts(), ["config.toml", "justfile"]);
        assert!(again.get("a").is_some());

        assert!(again.set_conflict("config.toml", false).unwrap());
        assert!(!again.set_conflict("config.toml", false).unwrap());
        assert_eq!(again.conflicts(), ["justfile"]);
        assert!(again.set_conflict("justfile", false).unwrap());
        let out = again.render("v0.2.0").unwrap();
        assert!(!out.contains("conflicts"), "{out}");
        assert!(Metadata::parse(&out).unwrap().conflicts().is_empty());
    }

    #[test]
    fn set_conflict_rejects_bad_path() {
        let mut md = Metadata::new();
        assert!(matches!(
            md.set_conflict("../x", true),
            Err(PutError::Invalid(_))
        ));
        assert!(md.conflicts().is_empty());
    }

    #[test]
    fn corrupt_records_are_vk0013() {
        let h = hash("x");
        let cases = [
            "schema = 1\nfile = 1\n".to_owned(),
            "schema = 1\n[[file]]\nstate = \"managed\"\n".to_owned(),
            "schema = 1\n[[file]]\npath = \"a\"\n".to_owned(),
            "schema = 1\n[[file]]\npath = \"a\"\nstate = \"owned\"\n".to_owned(),
            "schema = 1\n[[file]]\npath = 1\nstate = \"managed\"\n".to_owned(),
            "schema = 1\n[[file]]\npath = \"a\"\nstate = \"managed\"\nlines = \"x\"\n".to_owned(),
            "schema = 1\n[[file]]\npath = \"a\"\nstate = \"managed\"\nlines = [1]\n".to_owned(),
            "schema = 1\n[[file]]\npath = \"a\"\nstate = \"managed\"\nhash = \"ABC\"\n".to_owned(),
            format!(
                "schema = 1\n[[file]]\npath = \"a\"\nstate = \"managed\"\nhash = \"{}\"\n",
                h.as_str().to_uppercase()
            ),
            "schema = 1\n[[file]]\npath = \"a\"\nstate = \"declined\"\ndeclined_hash = 3\n"
                .to_owned(),
            "schema = 1\n[[file]]\npath = \"../a\"\nstate = \"managed\"\n".to_owned(),
            "schema = 1\n[[file]]\npath = \"a\"\nstate = \"managed\"\n[[file]]\npath = \"a\"\nstate = \"deleted\"\n".to_owned(),
            "not toml = = \n".to_owned(),
            "[[file]]\npath = \"a\"\nstate = \"managed\"\n".to_owned(),
            "schema = 0\n".to_owned(),
            "schema = 1\nconflicts = \"a\"\n".to_owned(),
            "schema = 1\nconflicts = [1]\n".to_owned(),
            "schema = 1\nconflicts = [\"../a\"]\n".to_owned(),
            "schema = 1\nconflicts = [\"a\", \"a\"]\n".to_owned(),
        ];
        for text in &cases {
            let err = Metadata::parse(text).unwrap_err();
            assert!(matches!(err, ParseError::Invalid(_)), "{text}: {err}");
            assert_eq!(err.message().code, "VK0013", "{text}");
        }
    }

    #[test]
    fn schema_too_new_is_vk0008() {
        let text = format!("schema = {}\nwritten_by = \"v9\"\n", u64::from(u32::MAX));
        let err = Metadata::parse(&text).unwrap_err();
        assert!(matches!(err, ParseError::TooNew(_)), "{err}");
        assert_eq!(err.message().code, "VK0008");
    }

    #[test]
    fn missing_file_is_vk0013_and_save_load_round_trips() {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        let path = tool_path(&dir, "docker").unwrap();
        let err = Metadata::load(&path).unwrap_err();
        assert!(matches!(err, Error::Missing { .. }), "{err}");
        assert_eq!(err.message().map(|m| m.code), Some("VK0013"));
        assert_eq!(err.file(), path);

        let mut md = Metadata::new();
        md.put(record(".gitignore", State::Appended)).unwrap();
        md.save(&path, "v0.1.0").unwrap();
        let loaded = Metadata::load(&path).unwrap();
        assert_eq!(loaded.files(), md.files());

        fs::write(&path, "schema = 1\nfile = 2\n").unwrap();
        let err = Metadata::load(&path).unwrap_err();
        assert!(matches!(err, Error::Corrupt { .. }), "{err}");
        assert_eq!(err.message().map(|m| m.code), Some("VK0013"));
    }

    #[test]
    fn paths_under_baseline() {
        let dir = InstallDir::new("/r");
        assert_eq!(
            tool_path(&dir, "docker").unwrap(),
            PathBuf::from("/r/.vendor_kit/baseline/docker.toml")
        );
        assert_eq!(
            vk_path(&dir),
            PathBuf::from("/r/.vendor_kit/baseline/.vendor_kit.toml")
        );
        for bad in ["", ".vendor_kit", "..", "a/b", "a\0"] {
            assert!(tool_path(&dir, bad).is_err(), "{bad:?}");
        }
    }

    #[test]
    fn file_hash_parse() {
        let h = hash("x");
        assert_eq!(FileHash::parse(h.as_str()), Some(h.clone()));
        assert_eq!(FileHash::parse(&h.as_str()[1..]), None);
        assert_eq!(FileHash::parse(&h.as_str().to_uppercase()), None);
    }
}
