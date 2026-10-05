//! `install` 要寫進安裝目錄、但契約與現有 crate 都還沒定內容的輸入（隨引擎 image 出貨的部分）。
//!
//! - 首次導入的引擎版本鎖定行的值：引擎不知道自己的 image 引用與 digest。啟動器手上有（`docker create`
//!   用的那個引用），但入口 argv（`plan::argv`）沒有傳，而且救援路徑的 argv 跨介面版永久不變。
//! - 薄殼四檔的模板本文（`shell::Shell::render` 要呼叫端給，ADR-0007 說模板隨 image 出貨）。
//! - 根 `justfile` 的那一行 `import`，與根 `justfile` 不存在時建檔附的 `default`（04 寫入既有檔的例外）。
//! - 根 `.dockerignore` 的四行（04、ADR-0003 只說「那四行」，沒列內容）。
//!
//! 這一版引擎一項都沒有出貨（[`Release::shipped`] 全是 `None`），`install` 缺哪一項就以 VK0056 停下並列出
//! 缺的項目，不自己補內容。端到端測試以 [`Release::from_dir`] 從測試目錄讀進同樣的輸入，驗其餘的流程。

use std::fs;
use std::io;
use std::path::Path;

use imageref::ImageRef;
use layout::SHELL_FILES;

/// [`Release::from_dir`] 的目錄裡，引擎版本鎖定行的值（一行）。
pub const ENGINE_FILE: &str = "engine";
/// 薄殼模板本文所在的子目錄，檔名同 [`layout::SHELL_FILES`]。
pub const SHELL_DIR: &str = "shell";
/// 根 `justfile` 的 `import` 行（一行）。
pub const JUSTFILE_IMPORT_FILE: &str = "justfile.import";
/// 根 `justfile` 不存在時建檔附的 `default`。
pub const JUSTFILE_DEFAULT_FILE: &str = "justfile.default";
/// 根 `.dockerignore` 的行，一行一個。
pub const DOCKERIGNORE_FILE: &str = "dockerignore";

/// `install` 的出貨輸入；`None` 是這一版沒有。
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Release {
    /// 首次導入時寫進 `version.toml` 的引擎版本鎖定行。
    pub engine: Option<ImageRef>,
    /// 薄殼四檔的模板本文，順序同 [`layout::SHELL_FILES`]。
    pub shell: Option<[Vec<u8>; SHELL_FILES.len()]>,
    /// 根 `justfile` 的 `import` 行，不含行尾。
    pub justfile_import: Option<String>,
    /// 根 `justfile` 不存在時建檔附的 `default`（整段，含行尾）。
    pub justfile_default: Option<String>,
    /// 根 `.dockerignore` 的行，不含行尾。
    pub dockerignore: Option<Vec<String>>,
}

impl Release {
    /// 這一版引擎隨 image 出貨的輸入：目前一項都沒有。
    pub fn shipped() -> Release {
        Release::default()
    }

    /// 從目錄讀（檔名見各常數）；檔不在的那一項是 `None`。內容不合（不是 UTF-8、引用不合、
    /// 該一行的檔有多行）回錯誤。
    pub fn from_dir(dir: &Path) -> io::Result<Release> {
        let engine = match read_text(&dir.join(ENGINE_FILE))? {
            Some(text) => {
                let line = one_line(&text, ENGINE_FILE)?;
                Some(ImageRef::parse(&line).map_err(|e| invalid(format!("{ENGINE_FILE}: {e}")))?)
            }
            None => None,
        };
        let mut bodies: Vec<Vec<u8>> = Vec::new();
        for name in SHELL_FILES {
            match read_bytes(&dir.join(SHELL_DIR).join(name))? {
                Some(b) => bodies.push(b),
                None => break,
            }
        }
        let shell = <[Vec<u8>; SHELL_FILES.len()]>::try_from(bodies).ok();
        let justfile_import = match read_text(&dir.join(JUSTFILE_IMPORT_FILE))? {
            Some(text) => Some(one_line(&text, JUSTFILE_IMPORT_FILE)?),
            None => None,
        };
        let justfile_default = read_text(&dir.join(JUSTFILE_DEFAULT_FILE))?;
        let dockerignore = read_text(&dir.join(DOCKERIGNORE_FILE))?
            .map(|t| t.lines().map(str::to_owned).collect::<Vec<_>>());
        Ok(Release {
            engine,
            shell,
            justfile_import,
            justfile_default,
            dockerignore,
        })
    }

    /// 這次缺的項目名；`need_engine` 是這次要不要新寫引擎版本鎖定行。
    pub fn missing(&self, need_engine: bool) -> Vec<&'static str> {
        let mut out = Vec::new();
        if need_engine && self.engine.is_none() {
            out.push("the engine lock line value");
        }
        if self.shell.is_none() {
            out.push("the shell templates");
        }
        if self.justfile_import.is_none() {
            out.push("the root justfile import line");
        }
        if self.justfile_default.is_none() {
            out.push("the default recipe of a new root justfile");
        }
        if self.dockerignore.as_ref().is_none_or(Vec::is_empty) {
            out.push("the root .dockerignore lines");
        }
        out
    }
}

fn invalid(msg: String) -> io::Error {
    io::Error::new(io::ErrorKind::InvalidData, msg)
}

fn read_bytes(path: &Path) -> io::Result<Option<Vec<u8>>> {
    match fs::read(path) {
        Ok(b) => Ok(Some(b)),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(None),
        Err(e) => Err(e),
    }
}

fn read_text(path: &Path) -> io::Result<Option<String>> {
    match read_bytes(path)? {
        Some(b) => String::from_utf8(b)
            .map(Some)
            .map_err(|_| invalid(format!("{} is not UTF-8", path.display()))),
        None => Ok(None),
    }
}

/// 只有一行的檔：去掉結尾的行尾；多於一行或空的回錯誤。
fn one_line(text: &str, name: &str) -> io::Result<String> {
    let line = text.strip_suffix('\n').unwrap_or(text);
    let line = line.strip_suffix('\r').unwrap_or(line);
    if line.is_empty() || line.contains(['\n', '\r']) {
        return Err(invalid(format!("{name} must be exactly one line")));
    }
    Ok(line.to_owned())
}
