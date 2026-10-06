//! `.vendor_kit/version.toml`（版本鎖定行）與 `.vendor_kit/version.local.toml`（本機覆寫）的讀寫。
//!
//! - 兩個檔都是 VK 寫的 TOML，讀寫經 `schema`：先過檔案版門檻（過高回 VK0008），再查形狀；
//!   未知欄位讀時忽略、寫時保留（ADR-0008）。路徑取自 `layout`（ADR-0002）。
//! - `version.toml` 只認一種正規形（ADR-0002），啟動器的 `grep`、引擎的解析、Renovate 的 regex
//!   三處共用：
//!   - 沒有 BOM。
//!   - 符合 `^vendor_kit[[:space:]]*=`（POSIX）的行恰好一行，而且就是根層的引擎行。這條以原文逐行
//!     計數，跟啟動器的 `grep` 看到的一樣：`[tools]` 下名叫 `vendor_kit` 的工具、多行字串裡的同形行、
//!     縮排或加引號的鍵，都會讓命中數不是 1。
//!   - 工具行都在 `[tools]` 表下，一個工具一行；`tools.x = …`、`tools = {…}`、`[tools.x]`、
//!     `[[tools]]` 這些繞過 `[tools]` 表的寫法不接受。
//!   - 每行是 `<鍵> = "<值>"`：鍵不加引號，值是不含跳脫的雙引號字串，內容是完整的 image 引用
//!     （`imageref`）。重複鍵是 TOML 語法錯誤，由 `schema` 擋下。
//!   - `[tools]` 表裡只能放工具行；`[tools]` 表外的未知欄位照 `schema` 的約定保留。
//!   - 根層有 `vendor_kit_protocols = "<列表>"`：鎖定的引擎接受的介面版，由它的 `[floor, current]`
//!     逐一展開、由小到大、以一個空白分隔（`compat::Compat::protocol_list`，例如 `"1"`、`"2 3 4"`）。
//!     本機沒有引擎 image 時，啟動器拿薄殼標頭的介面版跟這串逐項做字串相等比對（N13、#42）。鍵名的
//!     `_` 讓它不被 `^vendor_kit[[:space:]]*=` 命中。缺少或格式錯（不是 `<鍵> = "<值>"`、有前導零或 0、
//!     多餘空白、不是連續遞增）都拒絕；只查形狀，不跟本引擎的區間比，因為記的是鎖定的那一版引擎的區間。
//!     訊息表還沒有代碼，原因寫明草稿碼（VK0070），由呼叫端以 VK0056 停下。
//! - 非正規形一律拒絕並列出全部差異（[`Problem`]），不自動改寫：`version.toml` 進 git，自動改寫等於
//!   自動化寫追蹤檔（不變量 3）。訊息表目前沒有非正規形的代碼（計畫缺口 G3），
//!   [`ParseError::message`] 先回 `None`。
//! - `version.local.toml` 的形狀同上，差別只在：引擎行可以沒有（命中數 0 或 1），值是本機開發來源的
//!   原字串，不解析成 image 引用。引擎是 `vendor_kit = "<image>"`（ADR-0010），工具是 `[tools]` 下
//!   `<repo> = "<本機目錄>"`，相對路徑以安裝目錄為準，由呼叫端解讀。
//! - 本機覆寫只覆蓋已存在的版本鎖定行（GLOSSARY、02 第 2 條）：[`Versions::new`] 遇到指向不存在
//!   鎖定行的覆寫就回 [`OrphanOverrides`]，不悄悄忽略。[`Versions`] 給生效的來源（覆寫優先）；
//!   不套用覆寫的場合（既有安裝目錄的檢查與修復、`update` 照鎖定行查等，見 04）直接讀 [`LockFile`]。
//! - 寫出前用同一套規則再查一次輸出，查不過就拒絕寫，不寫出自己讀不回來的檔。
//!   新的 `version.toml` 第一行是引擎行、第二行是介面版列表，這是 `install` 寫出的慣例，讀取不依賴它
//!   （ADR-0002）。
//!
//! 這裡不印診斷；要怎麼印由呼叫端經 `diagnostics` 決定。

use std::collections::BTreeMap;
use std::fmt;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

use compat::Compat;
use imageref::{ImageRef, ImageRefError};
use layout::InstallDir;
use messages::Message;
use schema::{Document, ReadError, WriteError};
use toml_edit::{Item, Table, Value};

/// 引擎行的鍵。
pub const ENGINE_KEY: &str = "vendor_kit";
/// 工具行所在的表名。
pub const TOOLS_KEY: &str = "tools";
/// 引擎鎖定行旁記的介面版列表的鍵（N13）。
pub const PROTOCOLS_KEY: &str = "vendor_kit_protocols";

/// `version.toml`：引擎與各工具的版本鎖定行。
#[derive(Debug, Clone)]
pub struct LockFile {
    doc: Document,
    engine: ImageRef,
    protocols: Vec<u32>,
    tools: BTreeMap<String, ImageRef>,
}

impl LockFile {
    /// 新檔，只有引擎行與本引擎接受的介面版列表；引擎行寫在第一行、列表緊接在下（`install` 的慣例）。
    pub fn new(engine: &ImageRef) -> LockFile {
        let text = format!(
            "{ENGINE_KEY} = \"{engine}\"\n{PROTOCOLS_KEY} = \"{}\"\n{} = {}\n{} = \"\"\n",
            compat::THIS.protocol_list(),
            schema::SCHEMA_KEY,
            compat::THIS.max_schema,
            schema::WRITTEN_BY_KEY,
        );
        match LockFile::parse(&text) {
            Ok(lock) => lock,
            // 上面的字串由合法的 image 引用組成，必定是正規形。
            Err(_) => unreachable!("template is canonical"),
        }
    }

    /// 解析內容：先過 `schema` 的讀取門檻，再查正規形。
    pub fn parse(text: &str) -> Result<LockFile, ParseError> {
        let doc = Document::parse(text).map_err(ParseError::Read)?;
        let mut problems = Vec::new();
        let (engine, tools) = check_shape(text, &doc, Kind::Lock, &mut problems);
        let engine = engine.and_then(|v| parse_ref(ENGINE_KEY, &v, &mut problems));
        let protocols = check_protocols(&doc, &mut problems);
        let tools: BTreeMap<String, ImageRef> = tools
            .into_iter()
            .filter_map(|(repo, v)| {
                let r = parse_ref(&repo, &v, &mut problems)?;
                Some((repo, r))
            })
            .collect();
        match (engine, protocols) {
            (Some(engine), Some(protocols)) if problems.is_empty() => Ok(LockFile {
                doc,
                engine,
                protocols,
                tools,
            }),
            _ => Err(ParseError::NotCanonical(problems)),
        }
    }

    /// 讀 `path`。檔不在回 `Ok(None)`，要不要當錯由呼叫端決定。
    pub fn load(path: &Path) -> Result<Option<LockFile>, Error> {
        match read_text(path)? {
            None => Ok(None),
            Some(text) => LockFile::parse(&text)
                .map(Some)
                .map_err(|source| Error::Parse {
                    file: path.to_path_buf(),
                    source,
                }),
        }
    }

    /// 讀安裝目錄的 `.vendor_kit/version.toml`。
    pub fn load_from(dir: &InstallDir) -> Result<Option<LockFile>, Error> {
        LockFile::load(&dir.version_toml())
    }

    /// 引擎的鎖定版本。
    pub fn engine(&self) -> &ImageRef {
        &self.engine
    }

    /// 鎖定的引擎接受的介面版，由小到大。
    pub fn protocols(&self) -> &[u32] {
        &self.protocols
    }

    /// 全部工具的鎖定版本，依工具名排序。
    pub fn tools(&self) -> &BTreeMap<String, ImageRef> {
        &self.tools
    }

    /// 一個工具的鎖定版本；沒有這條鎖定行是 `None`。
    pub fn tool(&self, repo: &str) -> Option<&ImageRef> {
        self.tools.get(repo)
    }

    /// 換引擎的鎖定版本，原地改值，行的位置與註解不動。介面版列表不跟著改：換上的引擎才知道自己的區間，
    /// 由它經 [`LockFile::set_protocols`] 寫。
    pub fn set_engine(&mut self, engine: &ImageRef) -> Result<(), EditError> {
        self.doc
            .set(&[ENGINE_KEY], engine.to_string())
            .map_err(EditError::Write)?;
        self.engine = engine.clone();
        Ok(())
    }

    /// 把介面版列表換成 `compat` 的區間展開的那一串，原地改值，行的位置與註解不動。
    pub fn set_protocols(&mut self, compat: &Compat) -> Result<(), EditError> {
        self.doc
            .set(&[PROTOCOLS_KEY], compat.protocol_list())
            .map_err(EditError::Write)?;
        self.protocols = (compat.floor_protocol..=compat.current_protocol).collect();
        Ok(())
    }

    /// 新增或換掉一個工具的鎖定版本。
    pub fn set_tool(&mut self, repo: &str, image: &ImageRef) -> Result<(), EditError> {
        check_repo(repo)?;
        self.doc
            .set(&[TOOLS_KEY, repo], image.to_string())
            .map_err(EditError::Write)?;
        self.tools.insert(repo.to_owned(), image.clone());
        Ok(())
    }

    /// 拿掉一個工具的鎖定行；本來就沒有回 `Ok(None)`。
    pub fn remove_tool(&mut self, repo: &str) -> Result<Option<ImageRef>, EditError> {
        check_repo(repo)?;
        self.doc
            .remove(&[TOOLS_KEY, repo])
            .map_err(EditError::Write)?;
        Ok(self.tools.remove(repo))
    }

    /// 蓋上寫入者，確認沒有少寫、輸出仍是正規形後回傳要寫回的內容。
    pub fn render(&mut self, written_by: &str) -> Result<String, RenderError> {
        let text = self.doc.render(written_by).map_err(RenderError::Write)?;
        match LockFile::parse(&text) {
            Ok(_) => Ok(text),
            Err(e) => Err(RenderError::NotCanonical(e)),
        }
    }

    /// 原子寫到 `path`；上層目錄不在時先建。
    pub fn save(&mut self, path: &Path, written_by: &str) -> Result<(), Error> {
        let text = self.render(written_by).map_err(|source| Error::Render {
            file: path.to_path_buf(),
            source,
        })?;
        write_text(path, &text)
    }

    /// 寫到安裝目錄的 `.vendor_kit/version.toml`。
    pub fn save_to(&mut self, dir: &InstallDir, written_by: &str) -> Result<(), Error> {
        self.save(&dir.version_toml(), written_by)
    }
}

/// `version.local.toml`：本機覆寫，指到本機開發來源，不進 git。
#[derive(Debug, Clone, Default)]
pub struct LocalFile {
    doc: Document,
    engine: Option<String>,
    tools: BTreeMap<String, String>,
}

impl LocalFile {
    /// 新檔，沒有任何覆寫。
    pub fn new() -> LocalFile {
        LocalFile::default()
    }

    /// 解析內容：先過 `schema` 的讀取門檻，再查形狀。
    pub fn parse(text: &str) -> Result<LocalFile, ParseError> {
        let doc = Document::parse(text).map_err(ParseError::Read)?;
        let mut problems = Vec::new();
        let (engine, tools) = check_shape(text, &doc, Kind::Local, &mut problems);
        if problems.is_empty() {
            Ok(LocalFile { doc, engine, tools })
        } else {
            Err(ParseError::NotCanonical(problems))
        }
    }

    /// 讀 `path`。檔不在回 `Ok(None)`：沒有任何覆寫。
    pub fn load(path: &Path) -> Result<Option<LocalFile>, Error> {
        match read_text(path)? {
            None => Ok(None),
            Some(text) => LocalFile::parse(&text)
                .map(Some)
                .map_err(|source| Error::Parse {
                    file: path.to_path_buf(),
                    source,
                }),
        }
    }

    /// 讀安裝目錄的 `.vendor_kit/version.local.toml`。
    pub fn load_from(dir: &InstallDir) -> Result<Option<LocalFile>, Error> {
        LocalFile::load(&dir.version_local_toml())
    }

    /// 引擎的本機 image；沒有覆寫是 `None`。
    pub fn engine(&self) -> Option<&str> {
        self.engine.as_deref()
    }

    /// 全部工具的本機目錄，依工具名排序。
    pub fn tools(&self) -> &BTreeMap<String, String> {
        &self.tools
    }

    /// 一個工具的本機目錄；沒有覆寫是 `None`。
    pub fn tool(&self, repo: &str) -> Option<&str> {
        self.tools.get(repo).map(String::as_str)
    }

    /// 沒有任何覆寫。
    pub fn is_empty(&self) -> bool {
        self.engine.is_none() && self.tools.is_empty()
    }

    /// 設定引擎的本機 image。
    pub fn set_engine(&mut self, image: &str) -> Result<(), EditError> {
        check_plain(ENGINE_KEY, image)?;
        self.doc
            .set(&[ENGINE_KEY], image)
            .map_err(EditError::Write)?;
        self.engine = Some(image.to_owned());
        Ok(())
    }

    /// 解除引擎覆寫；本來就沒有回 `Ok(None)`。
    pub fn remove_engine(&mut self) -> Result<Option<String>, EditError> {
        self.doc.remove(&[ENGINE_KEY]).map_err(EditError::Write)?;
        Ok(self.engine.take())
    }

    /// 設定工具的本機目錄。
    pub fn set_tool(&mut self, repo: &str, dir: &str) -> Result<(), EditError> {
        check_repo(repo)?;
        check_plain(repo, dir)?;
        self.doc
            .set(&[TOOLS_KEY, repo], dir)
            .map_err(EditError::Write)?;
        self.tools.insert(repo.to_owned(), dir.to_owned());
        Ok(())
    }

    /// 解除工具覆寫；本來就沒有回 `Ok(None)`。
    pub fn remove_tool(&mut self, repo: &str) -> Result<Option<String>, EditError> {
        check_repo(repo)?;
        self.doc
            .remove(&[TOOLS_KEY, repo])
            .map_err(EditError::Write)?;
        Ok(self.tools.remove(repo))
    }

    /// 蓋上寫入者，確認沒有少寫、輸出讀得回來後回傳要寫回的內容。
    pub fn render(&mut self, written_by: &str) -> Result<String, RenderError> {
        let text = self.doc.render(written_by).map_err(RenderError::Write)?;
        match LocalFile::parse(&text) {
            Ok(_) => Ok(text),
            Err(e) => Err(RenderError::NotCanonical(e)),
        }
    }

    /// 原子寫到 `path`；上層目錄不在時先建。
    pub fn save(&mut self, path: &Path, written_by: &str) -> Result<(), Error> {
        let text = self.render(written_by).map_err(|source| Error::Render {
            file: path.to_path_buf(),
            source,
        })?;
        write_text(path, &text)
    }

    /// 寫到安裝目錄的 `.vendor_kit/version.local.toml`。
    pub fn save_to(&mut self, dir: &InstallDir, written_by: &str) -> Result<(), Error> {
        self.save(&dir.version_local_toml(), written_by)
    }
}

/// 生效的來源。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Source<'a> {
    /// 鎖定版本。
    Locked(&'a ImageRef),
    /// 本機開發來源：引擎是本機 image，工具是本機目錄（原字串）。
    Local(&'a str),
}

/// 版本鎖定行套上本機覆寫後的結果：覆寫優先。
#[derive(Debug, Clone, Copy)]
pub struct Versions<'a> {
    lock: &'a LockFile,
    local: Option<&'a LocalFile>,
}

impl<'a> Versions<'a> {
    /// 組合鎖定行與覆寫。覆寫的工具不在鎖定行時回錯：覆寫只能覆蓋已存在的版本鎖定行。
    pub fn new(
        lock: &'a LockFile,
        local: Option<&'a LocalFile>,
    ) -> Result<Versions<'a>, OrphanOverrides> {
        let repos: Vec<String> = local
            .map(|l| {
                l.tools
                    .keys()
                    .filter(|repo| !lock.tools.contains_key(*repo))
                    .cloned()
                    .collect()
            })
            .unwrap_or_default();
        if repos.is_empty() {
            Ok(Versions { lock, local })
        } else {
            Err(OrphanOverrides { repos })
        }
    }

    /// 版本鎖定行（不套用覆寫）。
    pub fn lock(&self) -> &'a LockFile {
        self.lock
    }

    /// 生效的引擎來源。
    pub fn engine(&self) -> Source<'a> {
        match self.local.and_then(LocalFile::engine) {
            Some(image) => Source::Local(image),
            None => Source::Locked(&self.lock.engine),
        }
    }

    /// 生效的工具來源；工具不在鎖定行是 `None`。
    pub fn tool(&self, repo: &str) -> Option<Source<'a>> {
        let locked = self.lock.tools.get(repo)?;
        Some(match self.local.and_then(|l| l.tool(repo)) {
            Some(dir) => Source::Local(dir),
            None => Source::Locked(locked),
        })
    }

    /// 全部工具的生效來源，依工具名排序。
    pub fn tools(&self) -> Vec<(&'a str, Source<'a>)> {
        let lock: &'a LockFile = self.lock;
        lock.tools
            .iter()
            .map(|(repo, locked)| {
                let source = match self.local.and_then(|l| l.tools.get(repo)) {
                    Some(dir) => Source::Local(dir.as_str()),
                    None => Source::Locked(locked),
                };
                (repo.as_str(), source)
            })
            .collect()
    }

    /// 有沒有任何覆寫在作用中。
    pub fn has_override(&self) -> bool {
        self.local.is_some_and(|l| !l.is_empty())
    }
}

/// 本機覆寫指到不存在的版本鎖定行。訊息表還沒有對應碼，回 `None`。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OrphanOverrides {
    /// 覆寫裡有、鎖定行裡沒有的工具，依名排序。
    pub repos: Vec<String>,
}

impl OrphanOverrides {
    /// 對應的訊息表條目：目前沒有。
    pub fn message(&self) -> Option<&'static Message> {
        None
    }
}

impl fmt::Display for OrphanOverrides {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "local override for tools without a lock version line: {}",
            self.repos.join(", ")
        )
    }
}

impl std::error::Error for OrphanOverrides {}

/// 不合正規形的一處。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Problem {
    /// 檔頭有 BOM。
    Bom,
    /// 符合 `^vendor_kit[[:space:]]*=` 的行數不對：`version.toml` 要恰好 1，`version.local.toml` 最多 1。
    EngineLineCount(usize),
    /// 根層沒有引擎行。
    EngineMissing,
    /// 根層沒有介面版列表（`vendor_kit_protocols`）。訊息表還沒有代碼（草稿 VK0070，N13）。
    ProtocolsMissing,
    /// 介面版列表不是 `vendor_kit_protocols = "<列表>"`，或列表不是以一個空白分隔、沒有前導零、
    /// 從 1 以上連續遞增的整數。訊息表還沒有代碼（草稿 VK0070，N13）。
    BadProtocols,
    /// 這一項不是 `<鍵> = "<值>"`：鍵加了引號或用了點、值不是不含跳脫的雙引號字串、或是空字串。
    NotPlainLine { key: String },
    /// 鎖定行的值不是完整的 image 引用。
    BadImageRef { key: String, error: ImageRefError },
    /// `tools` 不是 `[tools]` 標準表（`tools.x = …`、`tools = {…}`、`[[tools]]`，或只有 `[tools.x]`）。
    ToolsNotTable,
    /// `[tools]` 下有工具行以外的東西（子表、dotted key、不是字串的值）。
    NotToolLine { key: String },
}

impl fmt::Display for Problem {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Problem::Bom => f.write_str("file starts with a BOM"),
            Problem::EngineLineCount(n) => {
                write!(f, "{n} lines match ^{ENGINE_KEY}[[:space:]]*=")
            }
            Problem::EngineMissing => write!(f, "no top-level `{ENGINE_KEY}` line"),
            Problem::ProtocolsMissing => write!(
                f,
                "no top-level `{PROTOCOLS_KEY}` line; {PROTOCOLS_PENDING}"
            ),
            Problem::BadProtocols => write!(
                f,
                "`{PROTOCOLS_KEY}` is not written as {PROTOCOLS_KEY} = \"<versions>\" with consecutive \
                 interface versions separated by single spaces; {PROTOCOLS_PENDING}"
            ),
            Problem::NotPlainLine { key } => {
                write!(f, "`{key}` is not written as <key> = \"<value>\"")
            }
            Problem::BadImageRef { key, error } => {
                write!(f, "`{key}` is not a full image reference: {error}")
            }
            Problem::ToolsNotTable => write!(f, "tools are not under a [{TOOLS_KEY}] table"),
            Problem::NotToolLine { key } => {
                write!(f, "[{TOOLS_KEY}] entry `{key}` is not a tool line")
            }
        }
    }
}

/// 解析失敗。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ParseError {
    /// 沒過 `schema` 的讀取門檻：TOML 語法錯（含重複鍵）、`schema` 缺漏或不合、檔案版過高。
    Read(ReadError),
    /// TOML 合法但不是正規形；列出全部差異。
    NotCanonical(Vec<Problem>),
}

impl ParseError {
    /// 對應的訊息表條目：檔案版過高是 VK0008；其他訊息表還沒有代碼（計畫缺口 G3），回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            ParseError::Read(e) => e.message(),
            ParseError::NotCanonical(_) => None,
        }
    }
}

impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ParseError::Read(e) => e.fmt(f),
            ParseError::NotCanonical(problems) => {
                f.write_str("not in canonical form:")?;
                for p in problems {
                    write!(f, "\n  - {p}")?;
                }
                Ok(())
            }
        }
    }
}

impl std::error::Error for ParseError {}

/// 改值失敗，文件不變。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum EditError {
    /// 工具名不是不加引號就能寫的 TOML 鍵（只收英數、`-`、`_`）。
    InvalidRepo(String),
    /// 值是空的，或含 `"`、`\`、控制字元，寫不成不含跳脫的雙引號字串。
    InvalidValue { key: String },
    /// 文件樹拒絕改動。
    Write(WriteError),
}

impl fmt::Display for EditError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            EditError::InvalidRepo(repo) => write!(f, "invalid tool name {repo:?}"),
            EditError::InvalidValue { key } => {
                write!(f, "value for `{key}` cannot be written as a plain string")
            }
            EditError::Write(e) => e.fmt(f),
        }
    }
}

impl std::error::Error for EditError {}

/// 寫出前檢查失敗。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RenderError {
    /// 會少寫原本的值。
    Write(WriteError),
    /// 輸出不是正規形（例如讀進來的未知欄位與新寫的行撞形）。
    NotCanonical(ParseError),
}

impl fmt::Display for RenderError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            RenderError::Write(e) => e.fmt(f),
            RenderError::NotCanonical(e) => write!(f, "output {e}"),
        }
    }
}

impl std::error::Error for RenderError {}

/// 讀寫檔失敗。檔不在不是錯誤，見 [`LockFile::load`]、[`LocalFile::load`]。
#[derive(Debug)]
pub enum Error {
    /// 內容讀不進來或不是正規形。
    Parse { file: PathBuf, source: ParseError },
    /// 檔不是 UTF-8。
    NotUtf8 { file: PathBuf },
    /// 讀檔或建目錄的系統呼叫失敗。
    Io { file: PathBuf, source: io::Error },
    /// 拒絕寫回。
    Render { file: PathBuf, source: RenderError },
    /// 原子寫入失敗。
    Write(files::Error),
}

impl Error {
    /// 出錯的檔。
    pub fn file(&self) -> &Path {
        match self {
            Error::Parse { file, .. }
            | Error::NotUtf8 { file }
            | Error::Io { file, .. }
            | Error::Render { file, .. } => file,
            Error::Write(e) => e.path(),
        }
    }

    /// 對應的訊息表條目：檔案版過高是 VK0008；其他訊息表還沒有代碼，回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            Error::Parse { source, .. } => source.message(),
            Error::NotUtf8 { .. } | Error::Io { .. } | Error::Render { .. } | Error::Write(_) => {
                None
            }
        }
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Parse { file, source } => write!(f, "{}: {source}", file.display()),
            Error::NotUtf8 { file } => write!(f, "{}: not valid UTF-8", file.display()),
            Error::Io { file, source } => write!(f, "{}: {source}", file.display()),
            Error::Render { file, source } => write!(f, "{}: {source}", file.display()),
            Error::Write(e) => e.fmt(f),
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Error::Parse { source, .. } => Some(source),
            Error::Io { source, .. } => Some(source),
            Error::Render { source, .. } => Some(source),
            Error::Write(e) => Some(e),
            Error::NotUtf8 { .. } => None,
        }
    }
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum Kind {
    Lock,
    Local,
}

/// 查兩個檔共用的形狀，回傳引擎行與工具行的原字串值；不合的地方全部記進 `problems`。
fn check_shape(
    text: &str,
    doc: &Document,
    kind: Kind,
    problems: &mut Vec<Problem>,
) -> (Option<String>, BTreeMap<String, String>) {
    if text.starts_with('\u{feff}') {
        problems.push(Problem::Bom);
    }
    let hits = text.split('\n').filter(|l| is_engine_line(l)).count();
    let root = doc.root();
    let engine = match root.get(ENGINE_KEY) {
        None | Some(Item::None) => {
            if kind == Kind::Lock {
                problems.push(Problem::EngineMissing);
            }
            None
        }
        Some(item) => plain_value(root, ENGINE_KEY, item, problems),
    };
    let hits_ok = match kind {
        Kind::Lock => hits == 1,
        Kind::Local => hits == usize::from(root.contains_key(ENGINE_KEY)),
    };
    if !hits_ok {
        problems.push(Problem::EngineLineCount(hits));
    }
    let mut tools = BTreeMap::new();
    match root.get(TOOLS_KEY) {
        None | Some(Item::None) => {}
        Some(Item::Table(t)) if !t.is_dotted() && !t.is_implicit() => {
            for (key, item) in t.iter() {
                match item {
                    Item::Value(Value::String(_)) => {
                        if let Some(v) = plain_value(t, key, item, problems) {
                            tools.insert(key.to_owned(), v);
                        }
                    }
                    _ => problems.push(Problem::NotToolLine {
                        key: key.to_owned(),
                    }),
                }
            }
        }
        Some(_) => problems.push(Problem::ToolsNotTable),
    }
    (engine, tools)
}

/// 介面版列表的問題還沒有訊息表代碼時附在原因後面（共同規則：過渡做法）。
const PROTOCOLS_PENDING: &str = "reason code pending (draft VK0070, N13)";

/// 查根層的介面版列表（只有 `version.toml`）；合格時回由小到大的介面版，不合記一筆。
fn check_protocols(doc: &Document, problems: &mut Vec<Problem>) -> Option<Vec<u32>> {
    let root = doc.root();
    let item = match root.get(PROTOCOLS_KEY) {
        None | Some(Item::None) => {
            problems.push(Problem::ProtocolsMissing);
            return None;
        }
        Some(item) => item,
    };
    // 形狀不合時只記 `BadProtocols`，不另記 `NotPlainLine`。
    let parsed =
        plain_value(root, PROTOCOLS_KEY, item, &mut Vec::new()).and_then(|v| parse_protocols(&v));
    if parsed.is_none() {
        problems.push(Problem::BadProtocols);
    }
    parsed
}

/// `"1"`、`"2 3 4"`：一個空白分隔、沒有前導零、從 1 以上連續遞增的整數。
fn parse_protocols(value: &str) -> Option<Vec<u32>> {
    let mut out: Vec<u32> = Vec::new();
    for token in value.split(' ') {
        let digits = !token.is_empty() && token.bytes().all(|b| b.is_ascii_digit());
        if !digits || token.starts_with('0') {
            return None;
        }
        let p: u32 = token.parse().ok()?;
        if out
            .last()
            .is_some_and(|last| last.checked_add(1) != Some(p))
        {
            return None;
        }
        out.push(p);
    }
    Some(out)
}

/// `^vendor_kit[[:space:]]*=`：POSIX 的 `[[:space:]]` 是空白、`\t`、`\n`、`\v`、`\f`、`\r`。
fn is_engine_line(line: &str) -> bool {
    line.strip_prefix(ENGINE_KEY).is_some_and(|rest| {
        rest.trim_start_matches([' ', '\t', '\n', '\u{b}', '\u{c}', '\r'])
            .starts_with('=')
    })
}

/// `item` 是 `<鍵> = "<值>"` 時回值；鍵加引號、值不是不含跳脫的雙引號字串或是空的，記一筆。
fn plain_value(
    table: &Table,
    key: &str,
    item: &Item,
    problems: &mut Vec<Problem>,
) -> Option<String> {
    let bad = || Problem::NotPlainLine {
        key: key.to_owned(),
    };
    let Some(Value::String(s)) = item.as_value() else {
        problems.push(bad());
        return None;
    };
    let value = s.value();
    let key_ok = is_bare_key(key)
        && table
            .key(key)
            .is_some_and(|k| k.display_repr().as_ref() == key);
    let value_ok = is_plain(value) && s.display_repr().as_ref() == format!("\"{value}\"");
    if key_ok && value_ok {
        Some(value.clone())
    } else {
        problems.push(bad());
        None
    }
}

fn parse_ref(key: &str, value: &str, problems: &mut Vec<Problem>) -> Option<ImageRef> {
    match ImageRef::parse(value) {
        Ok(r) => Some(r),
        Err(error) => {
            problems.push(Problem::BadImageRef {
                key: key.to_owned(),
                error,
            });
            None
        }
    }
}

/// 不加引號就能寫的 TOML 鍵。
fn is_bare_key(key: &str) -> bool {
    !key.is_empty()
        && key
            .bytes()
            .all(|b| b.is_ascii_alphanumeric() || b == b'-' || b == b'_')
}

/// 能寫成不含跳脫的雙引號字串的非空值。
fn is_plain(value: &str) -> bool {
    !value.is_empty()
        && !value
            .chars()
            .any(|c| c == '"' || c == '\\' || c.is_control())
}

fn check_repo(repo: &str) -> Result<(), EditError> {
    if is_bare_key(repo) && repo != ENGINE_KEY {
        Ok(())
    } else {
        Err(EditError::InvalidRepo(repo.to_owned()))
    }
}

fn check_plain(key: &str, value: &str) -> Result<(), EditError> {
    if is_plain(value) {
        Ok(())
    } else {
        Err(EditError::InvalidValue {
            key: key.to_owned(),
        })
    }
}

fn read_text(path: &Path) -> Result<Option<String>, Error> {
    match fs::read_to_string(path) {
        Ok(text) => Ok(Some(text)),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(None),
        Err(e) if e.kind() == io::ErrorKind::InvalidData => Err(Error::NotUtf8 {
            file: path.to_path_buf(),
        }),
        Err(source) => Err(Error::Io {
            file: path.to_path_buf(),
            source,
        }),
    }
}

fn write_text(path: &Path, text: &str) -> Result<(), Error> {
    if let Some(parent) = path.parent().filter(|p| !p.as_os_str().is_empty()) {
        fs::create_dir_all(parent).map_err(|source| Error::Io {
            file: parent.to_path_buf(),
            source,
        })?;
    }
    files::write_atomic(path, text.as_bytes()).map_err(Error::Write)
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    const ENGINE: &str = "ghcr.io/acme/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
    const ENGINE2: &str = "ghcr.io/acme/vendor_kit:v1.1.0@sha256:2222222222222222222222222222222222222222222222222222222222222222";
    const TOOL: &str = "ghcr.io/acme/tool:v1.2.3@sha256:3333333333333333333333333333333333333333333333333333333333333333";
    const TOOL2: &str = "ghcr.io/acme/tool:v1.3.0@sha256:4444444444444444444444444444444444444444444444444444444444444444";

    fn r(s: &str) -> ImageRef {
        ImageRef::parse(s).unwrap()
    }

    fn canonical() -> String {
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"x\"\n\n[tools]\ntool = \"{TOOL}\"\n"
        )
    }

    fn problems(text: &str) -> Vec<Problem> {
        match LockFile::parse(text) {
            Err(ParseError::NotCanonical(p)) => p,
            other => panic!("expected NotCanonical, got {other:?}"),
        }
    }

    // ---- 正規形 ----

    #[test]
    fn accepts_canonical_form() {
        let lock = LockFile::parse(&canonical()).unwrap();
        assert_eq!(lock.engine(), &r(ENGINE));
        assert_eq!(lock.tool("tool"), Some(&r(TOOL)));
        assert_eq!(lock.tools().len(), 1);
    }

    #[test]
    fn engine_line_need_not_be_first() {
        let text = format!(
            "# header comment\nschema = 1\nwritten_by = \"x\"\nvendor_kit   =   \"{ENGINE}\" # pinned\nvendor_kit_protocols = \"1\"\n"
        );
        let lock = LockFile::parse(&text).unwrap();
        assert_eq!(lock.engine(), &r(ENGINE));
        assert!(lock.tools().is_empty());
    }

    #[test]
    fn unknown_fields_outside_tools_are_accepted_and_kept() {
        let text = format!("{}\n[extra]\nnote = \"keep\"\n", canonical());
        let mut lock = LockFile::parse(&text).unwrap();
        lock.set_tool("tool", &r(TOOL2)).unwrap();
        let out = lock.render("vk 1").unwrap();
        assert!(out.contains("[extra]\nnote = \"keep\""), "{out}");
    }

    #[test]
    fn engine_line_matcher_follows_posix_space_class() {
        assert!(is_engine_line("vendor_kit=\"x\""));
        assert!(is_engine_line("vendor_kit \t\u{b}\u{c}\r= \"x\""));
        assert!(!is_engine_line(" vendor_kit = \"x\""));
        assert!(!is_engine_line("\"vendor_kit\" = \"x\""));
        assert!(!is_engine_line("vendor_kit_x = \"x\""));
        assert!(!is_engine_line("vendor_kit.x = \"x\""));
    }

    // ---- 介面版列表（N13） ----

    #[test]
    fn protocols_key_is_not_an_engine_line() {
        // 鍵名的 `_` 斷開 `^vendor_kit[[:space:]]*=`：啟動器的比對、Renovate 的 regex 都只看到引擎行。
        assert!(!is_engine_line(&format!("{PROTOCOLS_KEY} = \"1\"")));
        let text = LockFile::new(&r(ENGINE)).render("x").unwrap();
        assert_eq!(text.split('\n').filter(|l| is_engine_line(l)).count(), 1);
    }

    #[test]
    fn new_file_records_this_engines_protocols_under_the_engine_line() {
        let lock = LockFile::new(&r(ENGINE));
        let range: Vec<u32> =
            (compat::THIS.floor_protocol..=compat::THIS.current_protocol).collect();
        assert_eq!(lock.protocols(), range.as_slice());
        let out = LockFile::new(&r(ENGINE)).render("vk 1").unwrap();
        assert_eq!(
            out,
            format!(
                "vendor_kit = \"{ENGINE}\"\n{PROTOCOLS_KEY} = \"{}\"\nschema = {}\nwritten_by = \"vk 1\"\n",
                compat::THIS.protocol_list(),
                compat::THIS.max_schema
            )
        );
    }

    #[test]
    fn accepts_consecutive_protocol_lists() {
        for (value, want) in [
            ("1", vec![1]),
            ("2 3 4", vec![2, 3, 4]),
            ("10 11", vec![10, 11]),
        ] {
            let text =
                canonical().replace("protocols = \"1\"", &format!("protocols = \"{value}\""));
            let lock = LockFile::parse(&text).unwrap();
            assert_eq!(lock.protocols(), want.as_slice(), "{value:?}");
        }
    }

    #[test]
    fn rejects_missing_protocols() {
        let text = canonical().replace("vendor_kit_protocols = \"1\"\n", "");
        assert_eq!(problems(&text), vec![Problem::ProtocolsMissing]);
        let err = LockFile::parse(&text).unwrap_err();
        assert_eq!(err.message(), None);
        assert!(
            err.to_string()
                .contains("reason code pending (draft VK0070, N13)"),
            "{err}"
        );
    }

    #[test]
    fn rejects_malformed_protocols() {
        for line in [
            "vendor_kit_protocols = \"\"",
            "vendor_kit_protocols = \"0\"",
            "vendor_kit_protocols = \"01\"",
            "vendor_kit_protocols = \"1  2\"",
            "vendor_kit_protocols = \" 1\"",
            "vendor_kit_protocols = \"1 \"",
            "vendor_kit_protocols = \"1\t2\"",
            "vendor_kit_protocols = \"1,2\"",
            "vendor_kit_protocols = \"2 1\"",
            "vendor_kit_protocols = \"1 3\"",
            "vendor_kit_protocols = \"1 1\"",
            "vendor_kit_protocols = \"+1\"",
            "vendor_kit_protocols = \"99999999999\"",
            "vendor_kit_protocols = '1'",
            "\"vendor_kit_protocols\" = \"1\"",
            "vendor_kit_protocols = 1",
            "vendor_kit_protocols = [1]",
        ] {
            let text = canonical().replace("vendor_kit_protocols = \"1\"", line);
            assert_eq!(problems(&text), vec![Problem::BadProtocols], "{line}");
        }
    }

    #[test]
    fn set_protocols_rewrites_the_list_in_place() {
        let mut lock = LockFile::parse(&canonical()).unwrap();
        let next = Compat {
            floor_protocol: 2,
            current_protocol: 3,
            max_schema: 1,
        };
        lock.set_engine(&r(ENGINE2)).unwrap();
        assert_eq!(lock.protocols(), &[1]);
        lock.set_protocols(&next).unwrap();
        assert_eq!(lock.protocols(), &[2, 3]);
        let out = lock.render("x").unwrap();
        assert_eq!(
            out,
            canonical()
                .replace(ENGINE, ENGINE2)
                .replace("protocols = \"1\"", "protocols = \"2 3\"")
        );
    }

    #[test]
    fn local_file_does_not_need_protocols() {
        assert!(LocalFile::parse("schema = 1\n").unwrap().is_empty());
    }

    // ---- 非正規形 ----

    #[test]
    fn rejects_bom() {
        let text = format!("\u{feff}{}", canonical());
        match LockFile::parse(&text) {
            // BOM 黏在第一行前面，啟動器的 grep 也就找不到引擎行。
            Err(ParseError::NotCanonical(p)) => {
                assert_eq!(p, vec![Problem::Bom, Problem::EngineLineCount(0)])
            }
            other => panic!("BOM not reported: {other:?}"),
        }
    }

    #[test]
    fn rejects_missing_engine_line() {
        let text = format!("schema = 1\n[tools]\ntool = \"{TOOL}\"\n");
        let p = problems(&text);
        assert!(p.contains(&Problem::EngineMissing), "{p:?}");
        assert!(p.contains(&Problem::EngineLineCount(0)), "{p:?}");
    }

    #[test]
    fn rejects_tool_named_like_the_engine_line() {
        let text = format!("{}vendor_kit = \"{TOOL}\"\n", canonical());
        assert_eq!(problems(&text), vec![Problem::EngineLineCount(2)]);
    }

    #[test]
    fn rejects_engine_line_inside_multiline_string() {
        let text = format!(
            "{}\n[extra]\nnote = \"\"\"\nvendor_kit = \"y\"\n\"\"\"\n",
            canonical()
        );
        assert_eq!(problems(&text), vec![Problem::EngineLineCount(2)]);
    }

    #[test]
    fn rejects_indented_engine_line() {
        let text =
            format!("  vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\n");
        assert_eq!(problems(&text), vec![Problem::EngineLineCount(0)]);
    }

    #[test]
    fn rejects_quoted_keys_and_values() {
        let text = format!("\"vendor_kit\" = \"{ENGINE}\"\nschema = 1\n");
        let p = problems(&text);
        assert!(p.contains(&Problem::EngineLineCount(0)), "{p:?}");
        assert!(
            p.contains(&Problem::NotPlainLine {
                key: "vendor_kit".into()
            }),
            "{p:?}"
        );

        let text = format!(
            "vendor_kit = '{ENGINE}'\nvendor_kit_protocols = \"1\"\nschema = 1\n[tools]\n\"tool\" = \"{TOOL}\"\n"
        );
        let p = problems(&text);
        assert_eq!(
            p,
            vec![
                Problem::NotPlainLine {
                    key: "vendor_kit".into()
                },
                Problem::NotPlainLine { key: "tool".into() },
            ]
        );
    }

    #[test]
    fn rejects_duplicate_keys() {
        let text = format!("{}tool = \"{TOOL2}\"\n", canonical());
        assert!(matches!(
            LockFile::parse(&text),
            Err(ParseError::Read(ReadError::Syntax(_)))
        ));
    }

    #[test]
    fn rejects_tools_bypassing_the_tools_table() {
        let head = format!("vendor_kit = \"{ENGINE}\"\nschema = 1\n");
        for tail in [
            format!("tools.tool = \"{TOOL}\"\n"),
            format!("tools = {{ tool = \"{TOOL}\" }}\n"),
            format!("[[tools]]\ntool = \"{TOOL}\"\n"),
            format!("[tools.tool]\nimage = \"{TOOL}\"\n"),
        ] {
            let p = problems(&format!("{head}{tail}"));
            assert!(p.contains(&Problem::ToolsNotTable), "{tail}: {p:?}");
        }
    }

    #[test]
    fn rejects_non_tool_entries_in_tools_table() {
        let text = format!(
            "{}a.b = \"{TOOL}\"\nn = 1\n\n[tools.sub]\nx = \"{TOOL}\"\n",
            canonical()
        );
        let p = problems(&text);
        assert_eq!(
            p,
            vec![
                Problem::NotToolLine { key: "a".into() },
                Problem::NotToolLine { key: "n".into() },
                Problem::NotToolLine { key: "sub".into() },
            ]
        );
    }

    #[test]
    fn rejects_values_that_are_not_full_image_refs() {
        let text = "vendor_kit = \"ghcr.io/acme/vendor_kit:v1.0.0\"\nvendor_kit_protocols = \"1\"\nschema = 1\n[tools]\ntool = \"\"\n";
        let p = problems(text);
        assert_eq!(
            p,
            vec![
                Problem::NotPlainLine { key: "tool".into() },
                Problem::BadImageRef {
                    key: "vendor_kit".into(),
                    error: ImageRefError::Digest
                },
            ]
        );
    }

    #[test]
    fn lists_every_problem_at_once() {
        let text = format!(
            "\u{feff}schema = 1\ntools = {{ tool = \"{TOOL}\" }}\n[x]\nvendor_kit = \"a\"\nvendor_kit_b = 1\n"
        );
        let p = problems(&text);
        assert!(p.contains(&Problem::Bom), "{p:?}");
        // `[x]` 下的同形行讓命中數剛好是 1，但根層沒有引擎行，照樣擋下。
        assert!(p.contains(&Problem::EngineMissing), "{p:?}");
        assert!(p.contains(&Problem::ToolsNotTable), "{p:?}");
        assert!(!p.contains(&Problem::EngineLineCount(1)), "{p:?}");
    }

    #[test]
    fn not_canonical_has_no_reason_code_yet() {
        let err = LockFile::parse("schema = 1\n").unwrap_err();
        assert_eq!(err.message(), None);
        assert!(err.to_string().contains("not in canonical form"), "{err}");
    }

    #[test]
    fn schema_gate_comes_first() {
        let text = "schema = 99\nwritten_by = \"vk 9\"\nvendor_kit = 1\n";
        let err = LockFile::parse(text).unwrap_err();
        assert!(
            matches!(err, ParseError::Read(ReadError::TooNew(_))),
            "{err:?}"
        );
        assert_eq!(err.message().map(|m| m.code), Some("VK0008"));
        assert!(matches!(
            LockFile::parse(&format!("vendor_kit = \"{ENGINE}\"\n")),
            Err(ParseError::Read(ReadError::MissingSchema))
        ));
    }

    // ---- 往返 ----

    #[test]
    fn new_file_round_trips_with_engine_line_first() {
        let mut lock = LockFile::new(&r(ENGINE));
        lock.set_tool("tool", &r(TOOL)).unwrap();
        lock.set_tool("other-tool_2", &r(TOOL2)).unwrap();
        let out = lock.render("vk 1.0.0").unwrap();
        assert!(
            out.starts_with(&format!("vendor_kit = \"{ENGINE}\"\n")),
            "{out}"
        );
        assert!(out.contains("\n[tools]\n"), "{out}");
        assert!(!out.contains("tools."), "{out}");
        let back = LockFile::parse(&out).unwrap();
        assert_eq!(back.engine(), &r(ENGINE));
        assert_eq!(back.tool("tool"), Some(&r(TOOL)));
        assert_eq!(back.tool("other-tool_2"), Some(&r(TOOL2)));
    }

    #[test]
    fn edits_keep_comments_and_order() {
        let text = format!(
            "# lock\nvendor_kit = \"{ENGINE}\" # engine\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"x\"\n\n[tools]\n# the tool\ntool = \"{TOOL}\"\n"
        );
        let mut lock = LockFile::parse(&text).unwrap();
        lock.set_engine(&r(ENGINE2)).unwrap();
        lock.set_tool("tool", &r(TOOL2)).unwrap();
        let out = lock.render("x").unwrap();
        let expected = format!(
            "# lock\nvendor_kit = \"{ENGINE2}\" # engine\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"x\"\n\n[tools]\n# the tool\ntool = \"{TOOL2}\"\n"
        );
        assert_eq!(out, expected);
    }

    #[test]
    fn remove_tool_and_save_load() {
        let dir = tempfile::tempdir().unwrap();
        let install = InstallDir::new(dir.path());
        assert!(LockFile::load_from(&install).unwrap().is_none());
        let mut lock = LockFile::parse(&canonical()).unwrap();
        assert_eq!(lock.remove_tool("tool").unwrap(), Some(r(TOOL)));
        assert_eq!(lock.remove_tool("tool").unwrap(), None);
        lock.save_to(&install, "vk 1").unwrap();
        let back = LockFile::load_from(&install).unwrap().unwrap();
        assert!(back.tools().is_empty());
        assert_eq!(back.engine(), &r(ENGINE));
    }

    #[test]
    fn rejects_bad_tool_names_on_edit() {
        let mut lock = LockFile::new(&r(ENGINE));
        for bad in ["", "a.b", "a b", "vendor_kit", "\"x\""] {
            assert!(
                matches!(lock.set_tool(bad, &r(TOOL)), Err(EditError::InvalidRepo(_))),
                "{bad:?}"
            );
        }
    }

    #[test]
    fn load_reports_file_on_parse_error() {
        let dir = tempfile::tempdir().unwrap();
        let path = dir.path().join("version.toml");
        fs::write(&path, "schema = 1\n").unwrap();
        let err = LockFile::load(&path).unwrap_err();
        assert_eq!(err.file(), path);
        assert_eq!(err.message(), None);
        fs::write(&path, [0xff, 0xfe]).unwrap();
        assert!(matches!(LockFile::load(&path), Err(Error::NotUtf8 { .. })));
    }

    // ---- 本機覆寫 ----

    fn local(text: &str) -> LocalFile {
        LocalFile::parse(text).unwrap()
    }

    #[test]
    fn local_file_round_trips() {
        let mut l = LocalFile::new();
        assert!(l.is_empty());
        l.set_engine("vendor_kit:dev").unwrap();
        l.set_tool("tool", "../tool").unwrap();
        let out = l.render("vk 1").unwrap();
        assert!(out.contains("vendor_kit = \"vendor_kit:dev\""), "{out}");
        assert!(out.contains("\n[tools]\ntool = \"../tool\""), "{out}");
        let mut back = LocalFile::parse(&out).unwrap();
        assert_eq!(back.engine(), Some("vendor_kit:dev"));
        assert_eq!(back.tool("tool"), Some("../tool"));
        assert_eq!(
            back.remove_engine().unwrap().as_deref(),
            Some("vendor_kit:dev")
        );
        assert_eq!(
            back.remove_tool("tool").unwrap().as_deref(),
            Some("../tool")
        );
        assert!(back.is_empty());
        let out = back.render("vk 1").unwrap();
        assert!(LocalFile::parse(&out).unwrap().is_empty());
    }

    #[test]
    fn local_file_follows_the_same_shape_rules() {
        assert!(local("schema = 1\n").is_empty());
        let p = match LocalFile::parse("schema = 1\n[tools]\nvendor_kit = \"x\"\n") {
            Err(ParseError::NotCanonical(p)) => p,
            other => panic!("{other:?}"),
        };
        assert_eq!(p, vec![Problem::EngineLineCount(1)]);
        let p = match LocalFile::parse("schema = 1\ntools.tool = \"../t\"\n") {
            Err(ParseError::NotCanonical(p)) => p,
            other => panic!("{other:?}"),
        };
        assert_eq!(p, vec![Problem::ToolsNotTable]);
        assert!(matches!(
            LocalFile::new().set_engine("a\"b"),
            Err(EditError::InvalidValue { .. })
        ));
    }

    #[test]
    fn override_takes_precedence() {
        let lock = LockFile::parse(&format!("{}other = \"{TOOL2}\"\n", canonical())).unwrap();
        let l = local("schema = 1\nvendor_kit = \"vendor_kit:dev\"\n[tools]\ntool = \"../tool\"\n");
        let v = Versions::new(&lock, Some(&l)).unwrap();
        assert!(v.has_override());
        assert_eq!(v.engine(), Source::Local("vendor_kit:dev"));
        assert_eq!(v.tool("tool"), Some(Source::Local("../tool")));
        assert_eq!(v.tool("other"), Some(Source::Locked(&r(TOOL2))));
        assert_eq!(v.tool("missing"), None);
        assert_eq!(
            v.tools(),
            vec![
                ("other", Source::Locked(&r(TOOL2))),
                ("tool", Source::Local("../tool")),
            ]
        );
        // 不套用覆寫的場合讀鎖定行本身。
        assert_eq!(v.lock().engine(), &r(ENGINE));
        assert_eq!(v.lock().tool("tool"), Some(&r(TOOL)));
    }

    #[test]
    fn without_override_uses_locked_versions() {
        let lock = LockFile::parse(&canonical()).unwrap();
        for l in [None, Some(&LocalFile::new())] {
            let v = Versions::new(&lock, l).unwrap();
            assert!(!v.has_override());
            assert_eq!(v.engine(), Source::Locked(&r(ENGINE)));
            assert_eq!(v.tool("tool"), Some(Source::Locked(&r(TOOL))));
        }
    }

    #[test]
    fn override_only_covers_existing_lock_lines() {
        let lock = LockFile::parse(&canonical()).unwrap();
        let l =
            local("schema = 1\n[tools]\nghost = \"../ghost\"\nzzz = \"../z\"\ntool = \"../t\"\n");
        let err = Versions::new(&lock, Some(&l)).unwrap_err();
        assert_eq!(err.repos, vec!["ghost".to_owned(), "zzz".to_owned()]);
        assert_eq!(err.message(), None);
    }
}
