//! 進度檔 `.vendor_kit/.tmp.<verb>.<id>.toml`：記錄可寫 recipe 未完成狀態的 VK 檔（GLOSSARY）。
//!
//! - 依 ADR-0004 的內部機制：可寫 recipe 在第一個 repo 檔或 VK 檔寫入之前建進度檔，全部寫完才刪；
//!   刪進度檔是這次操作唯一的完成點。進度檔還在，就表示操作沒做完，任何後續檢查都看得出來
//!   （02 不變量第 4 條：未完成的狀態必須可辨識、可恢復）。
//! - 這裡只給原語：[`Progress::create`]（建立）、[`load`]／[`Entry::load`]（讀回未完成的操作內容）、
//!   [`find`]（列出殘留）、[`delete`]（完成點）。寫入順序、何時恢復、殘留要報哪個代碼
//!   （VK0004、VK0023、VK0041、VK0053、VK0054 等）都由 recipe 決定，不在這裡。
//! - 建立與改寫都經 `files::write_atomic`：先寫同目錄的暫存檔、fsync 後 rename 成進度檔，不會留下
//!   半份的進度檔。暫存檔名是 `.tmp.<檔名>.<pid>.<序號>`，結尾不是 `.toml`，[`find`] 不把它認成
//!   進度檔：建立中斷時還沒有任何寫入，沒有要恢復的東西。
//! - 檔名由 `layout` 組（`<verb>`、`<id>` 各是一段不含 `.` 的名字），[`find`] 照同一條規則拆回去。
//! - 內容是 VK 寫的 TOML，經 `schema` 讀寫：先過檔案版門檻（過高回 VK0008），未知欄位讀時忽略、
//!   寫時保留（ADR-0008）。已知欄位只有 `command`：原指令的參數（`just vendor_kit` 之後的每一段），
//!   給 recipe 重組 `<original_command>`；其餘欄位由 recipe 經 [`Progress::document_mut`] 自己放。
//! - 第一版禁止 symlink：進度檔是 symlink 時一律回錯，不跟隨。
//! - 建立時同名進度檔已在就拒絕（[`Error::Exists`]），不蓋掉另一次未完成操作的恢復證據。檢查與
//!   rename 之間不是原子的，呼叫端要先持安裝目錄的排他鎖（`filelock`）。
//!
//! 這裡不印診斷；要怎麼印由呼叫端經 `diagnostics` 決定。

use std::fmt;
use std::fs::{self, File};
use std::io;
use std::path::{Path, PathBuf};

use layout::{InstallDir, InvalidName};
use messages::Message;
use schema::{Document, ReadError, WriteError};
use toml_edit::{Array, Value};

/// 原指令參數欄位的鍵。
pub const COMMAND_KEY: &str = "command";

/// `upgrade` 的進度檔（`.tmp.upgrade.<id>.toml`）另記的 `[upgrade]` 表。
///
/// 契約只要求唯讀 recipe 從進度檔辨識未完成的工具 upgrade（VK0041）或引擎 upgrade（VK0023），沒定格式；
/// 寫的是 `engine/upgrade`，讀的還有 `update`、`sync` 等其他指令，而指令之間互不依賴，所以格式定在這裡：
///
/// | 鍵 | 值 |
/// |---|---|
/// | [`upgrade::TARGET`] | 對象：工具填 `<repo>`，引擎填 [`upgrade::ENGINE_TARGET`] |
/// | [`upgrade::IMAGE`] | 這次換上的版本鎖定行的值（`<registry>/<路徑>:<tag>@<digest>`）；引擎的是目標引擎，tag 填 VK0023 的 `<vY>` |
/// | [`upgrade::INIT_FILES`] | 工具：這次有沒有寫初始檔相關的檔（repo 檔、逐檔紀錄、基準版副本）；引擎不記 |
///
/// 原指令仍在共同欄位 [`COMMAND_KEY`]。
pub mod upgrade {
    use super::Progress;

    /// 進度檔名裡的 `<verb>`，也是表名。
    pub const VERB: &str = "upgrade";
    pub const TABLE: &str = "upgrade";
    pub const TARGET: &str = "target";
    /// 引擎的對象值；`vendor_kit` 是保留名，不會是工具名（04 命名空間）。
    pub const ENGINE_TARGET: &str = "vendor_kit";
    pub const IMAGE: &str = "image";
    pub const INIT_FILES: &str = "init_files";

    /// `[upgrade]` 表裡的字串欄位；不在或不是字串回 `None`。
    pub fn field<'p>(progress: &'p Progress, key: &str) -> Option<&'p str> {
        progress
            .document()
            .get(&[TABLE, key])
            .and_then(|i| i.as_str())
    }

    /// `[upgrade]` 表裡的布林欄位；不在或不是布林回 `None`。
    pub fn flag(progress: &Progress, key: &str) -> Option<bool> {
        progress
            .document()
            .get(&[TABLE, key])
            .and_then(|i| i.as_bool())
    }
}

/// 進度檔名的前綴與副檔名（`layout::InstallDir::progress_file` 的格式）。
const PREFIX: &str = ".tmp.";
const SUFFIX: &str = ".toml";

/// 一份進度檔的內容。
#[derive(Debug, Clone)]
pub struct Progress {
    verb: String,
    id: String,
    command: Vec<String>,
    doc: Document,
}

impl Progress {
    /// 新的進度內容。`command` 是原指令在 `just vendor_kit` 之後的參數，至少一段。
    pub fn new<S: AsRef<str>>(verb: &str, id: &str, command: &[S]) -> Result<Progress, NewError> {
        check_names(verb, id).map_err(NewError::Name)?;
        let command: Vec<String> = command.iter().map(|s| s.as_ref().to_owned()).collect();
        if command.is_empty() {
            return Err(NewError::EmptyCommand);
        }
        let mut doc = Document::new();
        doc.set(&[COMMAND_KEY], command_value(&command))
            .map_err(NewError::Write)?;
        Ok(Progress {
            verb: verb.to_owned(),
            id: id.to_owned(),
            command,
            doc,
        })
    }

    /// 解析內容；`verb`、`id` 來自檔名。
    pub fn parse(verb: &str, id: &str, text: &str) -> Result<Progress, ParseError> {
        check_names(verb, id).map_err(ParseError::Name)?;
        let doc = Document::parse(text).map_err(ParseError::Read)?;
        let command = read_command(&doc)?;
        Ok(Progress {
            verb: verb.to_owned(),
            id: id.to_owned(),
            command,
            doc,
        })
    }

    /// 進度檔名裡的 `<verb>`。
    pub fn verb(&self) -> &str {
        &self.verb
    }

    /// 進度檔名裡的 `<id>`。
    pub fn id(&self) -> &str {
        &self.id
    }

    /// 原指令在 `just vendor_kit` 之後的參數。
    pub fn command(&self) -> &[String] {
        &self.command
    }

    /// 整份文件，給 recipe 讀自己放的欄位。
    pub fn document(&self) -> &Document {
        &self.doc
    }

    /// 整份文件，給 recipe 放自己的欄位。`command` 改壞了，[`Progress::render`] 會拒絕。
    pub fn document_mut(&mut self) -> &mut Document {
        &mut self.doc
    }

    /// 這份進度檔在安裝目錄裡的路徑。
    pub fn path(&self, dir: &InstallDir) -> PathBuf {
        match dir.progress_file(&self.verb, &self.id) {
            Ok(path) => path,
            // `verb`、`id` 在建構時已經過同一條檢查。
            Err(_) => unreachable!("names were checked on construction"),
        }
    }

    /// 蓋上寫入者，確認沒有少寫、輸出讀得回來後回傳要寫的內容。
    pub fn render(&mut self, written_by: &str) -> Result<String, RenderError> {
        let text = self.doc.render(written_by).map_err(RenderError::Write)?;
        match Progress::parse(&self.verb, &self.id, &text) {
            Ok(back) => {
                self.command = back.command;
                Ok(text)
            }
            Err(e) => Err(RenderError::Unreadable(e)),
        }
    }

    /// 建立進度檔：先寫暫存檔再原子 rename。同名進度檔已在回 [`Error::Exists`]，不覆蓋。
    /// `.vendor_kit/` 不在時不建，回錯：進度檔只建在既有的安裝目錄裡。
    pub fn create(&mut self, dir: &InstallDir, written_by: &str) -> Result<PathBuf, Error> {
        let path = self.path(dir);
        if exists(&path)? {
            return Err(Error::Exists { file: path });
        }
        self.write(&path, written_by)?;
        Ok(path)
    }

    /// 改寫既有的進度檔（記下新的未完成狀態），同樣原子替換。進度檔不在回 [`Error::Missing`]：
    /// 不在表示已經完成或從沒建過，不該悄悄重建。
    pub fn save(&mut self, dir: &InstallDir, written_by: &str) -> Result<(), Error> {
        let path = self.path(dir);
        if !exists(&path)? {
            return Err(Error::Missing { file: path });
        }
        self.write(&path, written_by)
    }

    fn write(&mut self, path: &Path, written_by: &str) -> Result<(), Error> {
        let text = self.render(written_by).map_err(|source| Error::Render {
            file: path.to_path_buf(),
            source,
        })?;
        files::write_atomic(path, text.as_bytes()).map_err(Error::Write)
    }
}

/// [`find`] 找到的一份進度檔。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Entry {
    pub verb: String,
    pub id: String,
    pub path: PathBuf,
}

impl Entry {
    /// 讀回這份進度檔的內容。
    pub fn load(&self) -> Result<Progress, Error> {
        match read_file(&self.verb, &self.id, &self.path)? {
            Some(p) => Ok(p),
            None => Err(Error::Missing {
                file: self.path.clone(),
            }),
        }
    }
}

/// 列出安裝目錄裡所有進度檔（未完成的操作），依檔名的位元組排序。`.vendor_kit/` 不在回空清單。
///
/// 名字合乎進度檔格式卻是 symlink 或不是一般檔，回錯，不略過：那是看不懂的殘留。
pub fn find(dir: &InstallDir) -> Result<Vec<Entry>, Error> {
    let vk = dir.vk_dir();
    let read = match fs::read_dir(&vk) {
        Ok(read) => read,
        Err(e) if e.kind() == io::ErrorKind::NotFound => return Ok(Vec::new()),
        Err(source) => return Err(Error::Io { file: vk, source }),
    };
    let mut found = Vec::new();
    for entry in read {
        let entry = entry.map_err(|source| Error::Io {
            file: vk.clone(),
            source,
        })?;
        let name = entry.file_name();
        let Some((verb, id)) = name.to_str().and_then(split_name) else {
            continue;
        };
        let path = entry.path();
        check_regular(&path)?;
        found.push(Entry {
            verb: verb.to_owned(),
            id: id.to_owned(),
            path,
        });
    }
    found.sort_by(|a, b| a.path.as_os_str().cmp(b.path.as_os_str()));
    Ok(found)
}

/// 讀一份指定的進度檔；不在回 `Ok(None)`。
pub fn load(dir: &InstallDir, verb: &str, id: &str) -> Result<Option<Progress>, Error> {
    let path = dir.progress_file(verb, id).map_err(Error::Name)?;
    read_file(verb, id, &path)
}

/// 刪除進度檔並 fsync `.vendor_kit/`：這是操作唯一的完成點，刪除要落盤才算完成。
/// 進度檔不在回 [`Error::Missing`]。
pub fn delete(dir: &InstallDir, verb: &str, id: &str) -> Result<(), Error> {
    let path = dir.progress_file(verb, id).map_err(Error::Name)?;
    if !exists(&path)? {
        return Err(Error::Missing { file: path });
    }
    fs::remove_file(&path).map_err(|source| Error::Io {
        file: path.clone(),
        source,
    })?;
    let vk = dir.vk_dir();
    File::open(&vk)
        .and_then(|d| d.sync_all())
        .map_err(|source| Error::Io { file: vk, source })
}

/// `.tmp.<verb>.<id>.toml` 拆回 `(verb, id)`；格式不合回 `None`。
fn split_name(name: &str) -> Option<(&str, &str)> {
    let rest = name.strip_prefix(PREFIX)?.strip_suffix(SUFFIX)?;
    let (verb, id) = rest.split_once('.')?;
    if id.contains('.') || check_names(verb, id).is_err() {
        return None;
    }
    Some((verb, id))
}

/// 名字的規則交給 `layout`，組得出路徑才算合法。
fn check_names(verb: &str, id: &str) -> Result<(), InvalidName> {
    InstallDir::new("").progress_file(verb, id).map(|_| ())
}

fn command_value(command: &[String]) -> Value {
    let mut array = Array::new();
    for arg in command {
        array.push(arg.as_str());
    }
    Value::Array(array)
}

fn read_command(doc: &Document) -> Result<Vec<String>, ParseError> {
    let item = doc.get(&[COMMAND_KEY]).ok_or(ParseError::MissingCommand)?;
    let array = item.as_array().ok_or(ParseError::BadCommand)?;
    let command: Vec<String> = array
        .iter()
        .map(|v| v.as_str().map(str::to_owned))
        .collect::<Option<_>>()
        .ok_or(ParseError::BadCommand)?;
    if command.is_empty() {
        return Err(ParseError::BadCommand);
    }
    Ok(command)
}

/// 路徑在不在（不跟隨 symlink）；在的話必須是一般檔。
fn exists(path: &Path) -> Result<bool, Error> {
    match fs::symlink_metadata(path) {
        Ok(_) => check_regular(path).map(|()| true),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(false),
        Err(source) => Err(Error::Io {
            file: path.to_path_buf(),
            source,
        }),
    }
}

fn check_regular(path: &Path) -> Result<(), Error> {
    let meta = fs::symlink_metadata(path).map_err(|source| Error::Io {
        file: path.to_path_buf(),
        source,
    })?;
    let ty = meta.file_type();
    if ty.is_symlink() {
        Err(Error::Symlink {
            file: path.to_path_buf(),
        })
    } else if ty.is_file() {
        Ok(())
    } else {
        Err(Error::NotRegular {
            file: path.to_path_buf(),
        })
    }
}

fn read_file(verb: &str, id: &str, path: &Path) -> Result<Option<Progress>, Error> {
    if !exists(path)? {
        return Ok(None);
    }
    let text = match fs::read_to_string(path) {
        Ok(text) => text,
        Err(e) if e.kind() == io::ErrorKind::NotFound => return Ok(None),
        Err(e) if e.kind() == io::ErrorKind::InvalidData => {
            return Err(Error::NotUtf8 {
                file: path.to_path_buf(),
            });
        }
        Err(source) => {
            return Err(Error::Io {
                file: path.to_path_buf(),
                source,
            });
        }
    };
    Progress::parse(verb, id, &text)
        .map(Some)
        .map_err(|source| Error::Parse {
            file: path.to_path_buf(),
            source,
        })
}

/// [`Progress::new`] 失敗。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum NewError {
    /// `<verb>` 或 `<id>` 組不成進度檔名。
    Name(InvalidName),
    /// 原指令沒有任何參數。
    EmptyCommand,
    /// 寫進文件失敗。
    Write(WriteError),
}

impl fmt::Display for NewError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            NewError::Name(e) => e.fmt(f),
            NewError::EmptyCommand => write!(f, "`{COMMAND_KEY}` must not be empty"),
            NewError::Write(e) => e.fmt(f),
        }
    }
}

impl std::error::Error for NewError {}

/// 內容讀不進來。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ParseError {
    /// `<verb>` 或 `<id>` 組不成進度檔名。
    Name(InvalidName),
    /// 沒過 `schema` 的讀取門檻。
    Read(ReadError),
    /// 沒有 `command`。
    MissingCommand,
    /// `command` 不是非空的字串陣列。
    BadCommand,
}

impl ParseError {
    /// 對應的訊息表條目：檔案版過高是 VK0008；其他訊息表還沒有代碼，回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            ParseError::Read(e) => e.message(),
            ParseError::Name(_) | ParseError::MissingCommand | ParseError::BadCommand => None,
        }
    }
}

impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ParseError::Name(e) => e.fmt(f),
            ParseError::Read(e) => e.fmt(f),
            ParseError::MissingCommand => write!(f, "missing `{COMMAND_KEY}`"),
            ParseError::BadCommand => {
                write!(f, "`{COMMAND_KEY}` is not a non-empty array of strings")
            }
        }
    }
}

impl std::error::Error for ParseError {}

/// 拒絕寫出。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RenderError {
    /// 照做會少寫原本的內容。
    Write(WriteError),
    /// 輸出讀不回來（例如 `command` 被改壞）。
    Unreadable(ParseError),
}

impl fmt::Display for RenderError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            RenderError::Write(e) => e.fmt(f),
            RenderError::Unreadable(e) => write!(f, "output would not read back: {e}"),
        }
    }
}

impl std::error::Error for RenderError {}

/// 這個 crate 的錯誤。
#[derive(Debug)]
pub enum Error {
    /// `<verb>` 或 `<id>` 組不成進度檔名。
    Name(InvalidName),
    /// 建立時同名進度檔已在。
    Exists { file: PathBuf },
    /// 改寫或刪除時進度檔不在。
    Missing { file: PathBuf },
    /// 進度檔是 symlink（第一版禁止）。
    Symlink { file: PathBuf },
    /// 進度檔不是一般檔。
    NotRegular { file: PathBuf },
    /// 內容讀不進來。
    Parse { file: PathBuf, source: ParseError },
    /// 檔不是 UTF-8。
    NotUtf8 { file: PathBuf },
    /// 拒絕寫出。
    Render { file: PathBuf, source: RenderError },
    /// 讀檔、讀目錄、刪檔或 fsync 目錄的系統呼叫失敗。
    Io { file: PathBuf, source: io::Error },
    /// 原子寫入失敗。
    Write(files::Error),
}

impl Error {
    /// 對應的訊息表條目：檔案版過高是 VK0008；其他訊息表還沒有代碼，回 `None`。
    /// 殘留的進度檔不是這裡的錯誤，要報哪個代碼由 recipe 決定。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            Error::Parse { source, .. } => source.message(),
            _ => None,
        }
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Name(e) => e.fmt(f),
            Error::Exists { file } => {
                write!(f, "{}: progress file already exists", file.display())
            }
            Error::Missing { file } => write!(f, "{}: progress file not found", file.display()),
            Error::Symlink { file } => write!(f, "symlink not allowed: {}", file.display()),
            Error::NotRegular { file } => write!(f, "not a regular file: {}", file.display()),
            Error::Parse { file, source } => write!(f, "{}: {source}", file.display()),
            Error::NotUtf8 { file } => write!(f, "{}: not valid UTF-8", file.display()),
            Error::Render { file, source } => write!(f, "{}: {source}", file.display()),
            Error::Io { file, source } => write!(f, "{}: {source}", file.display()),
            Error::Write(e) => e.fmt(f),
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Error::Name(e) => Some(e),
            Error::Parse { source, .. } => Some(source),
            Error::Render { source, .. } => Some(source),
            Error::Io { source, .. } => Some(source),
            Error::Write(e) => Some(e),
            Error::Exists { .. }
            | Error::Missing { .. }
            | Error::Symlink { .. }
            | Error::NotRegular { .. }
            | Error::NotUtf8 { .. } => None,
        }
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;
    use std::os::unix::fs::symlink;

    fn install() -> (tempfile::TempDir, InstallDir) {
        let tmp = tempfile::tempdir().unwrap();
        fs::create_dir(tmp.path().join(layout::VK_DIR)).unwrap();
        let dir = InstallDir::new(tmp.path());
        (tmp, dir)
    }

    fn upgrade() -> Progress {
        Progress::new("upgrade", "42", &["upgrade", "acme/tool", "v1.2.0", "-y"]).unwrap()
    }

    fn names(dir: &InstallDir) -> Vec<String> {
        let mut v: Vec<String> = fs::read_dir(dir.vk_dir())
            .unwrap()
            .map(|e| e.unwrap().file_name().to_string_lossy().into_owned())
            .collect();
        v.sort();
        v
    }

    #[test]
    fn upgrade_table_round_trips() {
        let (_t, dir) = install();
        let mut p = Progress::new(upgrade::VERB, "42", &["upgrade", "tool@v1.2.0", "-y"]).unwrap();
        let doc = p.document_mut();
        doc.set(&[upgrade::TABLE, upgrade::TARGET], "tool").unwrap();
        doc.set(
            &[upgrade::TABLE, upgrade::IMAGE],
            "ghcr.io/a/tool:v1.2.0@sha256:1",
        )
        .unwrap();
        doc.set(&[upgrade::TABLE, upgrade::INIT_FILES], false)
            .unwrap();
        p.create(&dir, "v1").unwrap();
        let back = load(&dir, upgrade::VERB, "42").unwrap().unwrap();
        assert_eq!(upgrade::field(&back, upgrade::TARGET), Some("tool"));
        assert_eq!(
            upgrade::field(&back, upgrade::IMAGE),
            Some("ghcr.io/a/tool:v1.2.0@sha256:1")
        );
        assert_eq!(upgrade::flag(&back, upgrade::INIT_FILES), Some(false));
        assert_eq!(upgrade::field(&back, upgrade::INIT_FILES), None);
        assert_eq!(upgrade::flag(&back, upgrade::TARGET), None);
        assert_eq!(upgrade::field(&upgrade(), upgrade::TARGET), None);
    }

    #[test]
    fn create_writes_progress_file_and_reads_back() {
        let (_t, dir) = install();
        let mut p = upgrade();
        p.document_mut().set(&["step"], "fetched").unwrap();
        let path = p.create(&dir, "v1.0.0").unwrap();
        assert_eq!(path, dir.vk_dir().join(".tmp.upgrade.42.toml"));
        // 只有進度檔本身，沒有留下 files 的暫存檔。
        assert_eq!(names(&dir), vec![".tmp.upgrade.42.toml"]);

        let back = load(&dir, "upgrade", "42").unwrap().unwrap();
        assert_eq!(back.verb(), "upgrade");
        assert_eq!(back.id(), "42");
        assert_eq!(back.command(), ["upgrade", "acme/tool", "v1.2.0", "-y"]);
        assert_eq!(
            back.document().get(&["step"]).and_then(|i| i.as_str()),
            Some("fetched")
        );
        assert_eq!(back.document().written_by(), Some("v1.0.0"));
    }

    #[test]
    fn create_refuses_to_overwrite_existing_progress() {
        let (_t, dir) = install();
        upgrade().create(&dir, "v1").unwrap();
        let before = fs::read(dir.vk_dir().join(".tmp.upgrade.42.toml")).unwrap();
        let mut other = Progress::new("upgrade", "42", &["upgrade", "other"]).unwrap();
        let err = other.create(&dir, "v1").unwrap_err();
        assert!(matches!(err, Error::Exists { .. }), "{err:?}");
        assert_eq!(
            fs::read(dir.vk_dir().join(".tmp.upgrade.42.toml")).unwrap(),
            before
        );
    }

    #[test]
    fn create_needs_existing_vk_dir() {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        let err = upgrade().create(&dir, "v1").unwrap_err();
        assert!(matches!(err, Error::Write(_)), "{err:?}");
        assert!(!dir.vk_dir().exists());
    }

    #[test]
    fn find_lists_leftovers_sorted() {
        let (_t, dir) = install();
        Progress::new("undev", "7", &["undev", "acme/tool"])
            .unwrap()
            .create(&dir, "v1")
            .unwrap();
        Progress::new("add", "9", &["add", "acme/tool"])
            .unwrap()
            .create(&dir, "v1")
            .unwrap();
        let found = find(&dir).unwrap();
        let keys: Vec<(&str, &str)> = found
            .iter()
            .map(|e| (e.verb.as_str(), e.id.as_str()))
            .collect();
        assert_eq!(keys, vec![("add", "9"), ("undev", "7")]);
        let p = found[1].load().unwrap();
        assert_eq!(p.command(), ["undev", "acme/tool"]);
    }

    /// files 原子寫入留下的暫存檔與其他檔都不算進度檔。
    #[test]
    fn find_ignores_non_progress_files() {
        let (_t, dir) = install();
        let vk = dir.vk_dir();
        for name in [
            "version.toml",
            ".tmp.version.toml.123.0",
            ".tmp.gitignore.123.1",
            ".tmp..tmp.add.9.toml.123.2",
            ".tmp.a.b.c.toml",
            ".tmp..x.toml",
            ".tmp.x..toml",
            ".tmp.x.toml",
        ] {
            fs::write(vk.join(name), b"").unwrap();
        }
        assert!(find(&dir).unwrap().is_empty());
    }

    #[test]
    fn find_without_vk_dir_is_empty() {
        let tmp = tempfile::tempdir().unwrap();
        assert!(find(&InstallDir::new(tmp.path())).unwrap().is_empty());
    }

    #[test]
    fn find_rejects_symlinked_or_odd_progress_entries() {
        let (t, dir) = install();
        let real = t.path().join("real.toml");
        fs::write(&real, b"").unwrap();
        symlink(&real, dir.vk_dir().join(".tmp.add.1.toml")).unwrap();
        assert!(matches!(find(&dir), Err(Error::Symlink { .. })));

        fs::remove_file(dir.vk_dir().join(".tmp.add.1.toml")).unwrap();
        fs::create_dir(dir.vk_dir().join(".tmp.add.2.toml")).unwrap();
        assert!(matches!(find(&dir), Err(Error::NotRegular { .. })));
    }

    #[test]
    fn delete_removes_progress_file() {
        let (_t, dir) = install();
        upgrade().create(&dir, "v1").unwrap();
        delete(&dir, "upgrade", "42").unwrap();
        assert!(names(&dir).is_empty());
        assert!(find(&dir).unwrap().is_empty());
        assert!(load(&dir, "upgrade", "42").unwrap().is_none());
    }

    #[test]
    fn delete_missing_is_an_error() {
        let (_t, dir) = install();
        let err = delete(&dir, "upgrade", "42").unwrap_err();
        assert!(matches!(err, Error::Missing { .. }), "{err:?}");
    }

    #[test]
    fn delete_refuses_symlink() {
        let (t, dir) = install();
        let real = t.path().join("real.toml");
        fs::write(&real, b"keep").unwrap();
        symlink(&real, dir.vk_dir().join(".tmp.upgrade.42.toml")).unwrap();
        let err = delete(&dir, "upgrade", "42").unwrap_err();
        assert!(matches!(err, Error::Symlink { .. }), "{err:?}");
        assert_eq!(fs::read(&real).unwrap(), b"keep");
    }

    #[test]
    fn save_rewrites_existing_and_keeps_unknown_fields() {
        let (_t, dir) = install();
        let path = dir.vk_dir().join(".tmp.upgrade.42.toml");
        fs::write(
            &path,
            "schema = 1\nwritten_by = \"v0\"\ncommand = [\"upgrade\", \"--engine\"]\n\
             # 註解\nfuture = \"keep\"\n\n[later]\nx = 1\n",
        )
        .unwrap();
        let mut p = load(&dir, "upgrade", "42").unwrap().unwrap();
        p.document_mut().set(&["step"], "engine-installed").unwrap();
        p.save(&dir, "v1").unwrap();

        let text = fs::read_to_string(&path).unwrap();
        assert!(text.contains("future = \"keep\""), "{text}");
        assert!(text.contains("# 註解"), "{text}");
        assert!(text.contains("[later]\nx = 1"), "{text}");
        let back = load(&dir, "upgrade", "42").unwrap().unwrap();
        assert_eq!(back.command(), ["upgrade", "--engine"]);
        assert_eq!(
            back.document().get(&["step"]).and_then(|i| i.as_str()),
            Some("engine-installed")
        );
    }

    #[test]
    fn save_missing_is_an_error() {
        let (_t, dir) = install();
        let err = upgrade().save(&dir, "v1").unwrap_err();
        assert!(matches!(err, Error::Missing { .. }), "{err:?}");
        assert!(names(&dir).is_empty());
    }

    #[test]
    fn new_rejects_bad_names_and_empty_command() {
        let none: [&str; 0] = [];
        assert!(matches!(
            Progress::new("up.grade", "1", &["x"]),
            Err(NewError::Name(_))
        ));
        assert!(matches!(
            Progress::new("add", "a/b", &["x"]),
            Err(NewError::Name(_))
        ));
        assert!(matches!(
            Progress::new("add", "1", &none),
            Err(NewError::EmptyCommand)
        ));
        assert!(matches!(load(&install().1, "", "1"), Err(Error::Name(_))));
    }

    #[test]
    fn parse_requires_command() {
        let missing = Progress::parse("add", "1", "schema = 1\n").unwrap_err();
        assert_eq!(missing, ParseError::MissingCommand);
        assert!(missing.message().is_none());
        for bad in [
            "command = \"add\"",
            "command = []",
            "command = [\"add\", 1]",
        ] {
            let text = format!("schema = 1\n{bad}\n");
            assert_eq!(
                Progress::parse("add", "1", &text).unwrap_err(),
                ParseError::BadCommand,
                "{bad}"
            );
        }
    }

    #[test]
    fn too_new_schema_maps_to_vk0008() {
        let (_t, dir) = install();
        let path = dir.vk_dir().join(".tmp.add.1.toml");
        fs::write(
            &path,
            "schema = 999\nwritten_by = \"v9\"\ncommand = [\"add\"]\n",
        )
        .unwrap();
        let err = find(&dir).unwrap()[0].load().unwrap_err();
        assert!(matches!(err, Error::Parse { .. }), "{err:?}");
        assert_eq!(err.message().map(|m| m.code), Some("VK0008"));
    }

    #[test]
    fn render_rejects_broken_command() {
        let (_t, dir) = install();
        let mut p = upgrade();
        p.document_mut()
            .set(&[COMMAND_KEY], "not an array")
            .unwrap();
        let err = p.create(&dir, "v1").unwrap_err();
        assert!(
            matches!(
                err,
                Error::Render {
                    source: RenderError::Unreadable(ParseError::BadCommand),
                    ..
                }
            ),
            "{err:?}"
        );
        assert!(names(&dir).is_empty());
    }
}
