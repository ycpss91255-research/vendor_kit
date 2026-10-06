//! `install` 要寫進安裝目錄的輸入：隨引擎出貨的內容，與啟動器交給引擎的引擎引用。
//!
//! - 首次導入的引擎版本鎖定行的值：引擎 image 不可能含有自己的 index digest，救援 argv 又凍結，所以由
//!   啟動器在起引擎前寫成 `in/` 裡的 [`plan::files::IN_ENGINE`]（N37）。[`engine_from`] 讀它並驗證是這個
//!   引擎自己：pinned 引用、`<registry>/<路徑>` 等於 [`ENGINE_REPO`]、tag 等於本引擎版。
//! - 根 `justfile` 的那一行 `import`（[`JUSTFILE_IMPORT`]）、根 `justfile` 不存在時建檔附的 `default`
//!   （[`JUSTFILE_DEFAULT`]，04 寫入既有檔的例外），與根 `.dockerignore` 的四行（[`DOCKERIGNORE_LINES`]）。
//!   逐字內容是這裡定的，04 的草稿之後照這裡寫。
//! - 薄殼四檔的模板本文（`shell::Shell::render` 要呼叫端給，ADR-0007 說模板隨 image 出貨）：image 建置時由
//!   `launcher/shell/assemble.sh` 組好，放在 [`SHIPPED_DIR`] 的 [`SHELL_DIR`] 下（image/Dockerfile），
//!   [`Release::shipped`] 從那裡讀。讀不到（四檔不齊）時 `shell` 是 `None`，`install` 與 `sync` 以 VK0056 停下
//!   並列出缺的項目，不自己補。端到端測試以 [`Release::from_dir`] 從測試目錄讀進模板。

use std::fs;
use std::io;
use std::path::Path;

use imageref::ImageRef;
use layout::SHELL_FILES;

/// 引擎 image 的 `<registry>/<路徑>`；引擎引用檔的值必須是這個 repo 的。
pub const ENGINE_REPO: &str = "ghcr.io/ycpss91255-research/vendor_kit";
/// 根 `justfile` 的 `import` 行，不含行尾。
pub const JUSTFILE_IMPORT: &str = "import '.vendor_kit/entry.just'";
/// 根 `justfile` 不存在時建檔附的 `default`（整段，含行尾）。
pub const JUSTFILE_DEFAULT: &str = "default:\n    @just --list\n";
/// 根 `.dockerignore` 的四行，不含行尾：`.vendor_kit/` 下只在本機、不該進 build context 的路徑。
pub const DOCKERIGNORE_LINES: [&str; 4] = [
    ".vendor_kit/cache/",
    ".vendor_kit/gen/",
    ".vendor_kit/log/",
    ".vendor_kit/version.local.toml",
];
/// 引擎 image 裡隨 image 出貨的輸入所在的目錄（image/Dockerfile 的最終 stage 把薄殼模板 COPY 到這裡的
/// [`SHELL_DIR`] 下）。
pub const SHIPPED_DIR: &str = "/usr/share/vendor_kit";
/// [`Release::from_dir`] 的目錄裡，薄殼模板本文所在的子目錄，檔名同 [`layout::SHELL_FILES`]。
pub const SHELL_DIR: &str = "shell";

/// `install` 的出貨輸入。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Release {
    /// 薄殼四檔的模板本文，順序同 [`layout::SHELL_FILES`]；`None` 是這一版沒有。
    pub shell: Option<[Vec<u8>; SHELL_FILES.len()]>,
    /// 根 `justfile` 的 `import` 行，不含行尾。
    pub justfile_import: String,
    /// 根 `justfile` 不存在時建檔附的 `default`（整段，含行尾）。
    pub justfile_default: String,
    /// 根 `.dockerignore` 的行，不含行尾。
    pub dockerignore: Vec<String>,
}

impl Release {
    /// 這一版引擎隨 image 出貨的輸入：根目錄檔的內容，加上從 [`SHIPPED_DIR`] 讀進的薄殼模板。
    pub fn shipped() -> io::Result<Release> {
        Release::from_dir(Path::new(SHIPPED_DIR))
    }

    /// 只有根目錄檔的內容、沒有薄殼模板的出貨輸入。
    pub fn without_shell() -> Release {
        Release {
            shell: None,
            justfile_import: JUSTFILE_IMPORT.to_owned(),
            justfile_default: JUSTFILE_DEFAULT.to_owned(),
            dockerignore: DOCKERIGNORE_LINES.map(str::to_owned).to_vec(),
        }
    }

    /// [`Release::without_shell`] 加上從目錄的 [`SHELL_DIR`] 讀進的薄殼模板；四檔不齊就是 `None`。
    pub fn from_dir(dir: &Path) -> io::Result<Release> {
        let mut bodies: Vec<Vec<u8>> = Vec::new();
        for name in SHELL_FILES {
            match read_bytes(&dir.join(SHELL_DIR).join(name))? {
                Some(b) => bodies.push(b),
                None => break,
            }
        }
        Ok(Release {
            shell: <[Vec<u8>; SHELL_FILES.len()]>::try_from(bodies).ok(),
            ..Release::without_shell()
        })
    }

    /// 這次缺的項目名。
    pub fn missing(&self) -> Vec<&'static str> {
        let mut out = Vec::new();
        if self.shell.is_none() {
            out.push("the shell templates");
        }
        out
    }
}

/// 讀 `inbox` 裡啟動器寫的引擎引用檔，驗證是 `version`（`v<X.Y.Z>`）這一版的引擎自己。
/// 不合回原因（英文，填 VK0056 的 `<reason>`）。
pub fn engine_from(inbox: &Path, version: &str) -> Result<ImageRef, String> {
    let name = plan::files::IN_ENGINE;
    let what = format!("the engine reference in/{name} from the launcher");
    let text = match read_text(&inbox.join(name)) {
        Ok(Some(t)) => t,
        Ok(None) => return Err(format!("{what} is missing")),
        Err(e) => return Err(format!("{what}: {e}")),
    };
    let line = one_line(&text, name).map_err(|e| format!("{what}: {e}"))?;
    let engine = ImageRef::parse(&line)
        .map_err(|e| format!("{what} is not a pinned reference ({e}): {line}"))?;
    let repo = format!("{}/{}", engine.registry(), engine.path());
    if repo != ENGINE_REPO {
        return Err(format!(
            "{what} names {repo}, not this engine's {ENGINE_REPO}: {line}"
        ));
    }
    let tag = engine.tag().to_string();
    if tag != version {
        return Err(format!(
            "{what} has tag {tag}, not this engine's {version}: {line}"
        ));
    }
    Ok(engine)
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
            .map_err(|_| invalid("not UTF-8".to_owned())),
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
