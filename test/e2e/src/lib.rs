//! 端到端測試共用的輔助：找出受測的執行檔、扮演啟動器與 registry、產生薄殼 fixture。測試本體在 `tests/`。

// 測試輔助：失敗就讓測試失敗，unwrap 放行（workspace lints 的測試例外）。
#[allow(clippy::unwrap_used, clippy::expect_used)]
pub mod launcher;
// 同上：假 registry。
#[allow(clippy::unwrap_used, clippy::expect_used)]
pub mod registry;

use std::path::PathBuf;

/// 受測的 `vendor_kit` 執行檔。
///
/// 有 `VK_BIN` 就用它（image 的建置 stage 指向靜態編譯的成品）；
/// 沒有就找同一個 target 目錄裡 `cargo build` 出來的那一份。
pub fn vendor_kit_bin() -> Result<PathBuf, String> {
    if let Some(path) = std::env::var_os("VK_BIN") {
        return Ok(PathBuf::from(path));
    }
    // 測試執行檔在 target/<profile>/deps/ 下，引擎在 target/<profile>/。
    let exe = std::env::current_exe().map_err(|e| e.to_string())?;
    let profile_dir = exe
        .parent()
        .and_then(|deps| deps.parent())
        .ok_or("cannot locate the target directory")?;
    let bin = profile_dir.join("vendor_kit");
    if bin.is_file() {
        Ok(bin)
    } else {
        Err(format!(
            "{} not found; run `cargo build -p vendor_kit` or set VK_BIN",
            bin.display()
        ))
    }
}

/// 版本行用的版本；引擎與這個 crate 共用 workspace 的版本號。
pub const VERSION: &str = concat!("v", env!("CARGO_PKG_VERSION"));

/// 引擎的測試用環境變數：三個掛載點改到 `<值>/vk/root`、`<值>/vk/ctl`、`<值>/vk/in`
/// （engine/vendor_kit 的 `MOUNT_PREFIX_ENV`；這裡不能依賴 engine crate，照抄名字）。
pub const MOUNT_PREFIX_ENV: &str = "VK_TEST_MOUNT_PREFIX";

/// 引擎的測試用環境變數：registry client 改連這個 base URL（engine/vendor_kit 的 `REGISTRY_URL_ENV`；照抄名字）。
/// 給 [`registry::Registry::base`]，不連外網。
pub const REGISTRY_URL_ENV: &str = "VK_TEST_REGISTRY_URL";

/// 薄殼的 fixture：隨 image 出貨的模板目錄，與安裝目錄裡跟這一版引擎一致的薄殼四檔。
///
/// 標頭格式照 engine/shell（這裡不能依賴 engine crate，照抄）：介面版、引擎版、其餘內容的 sha256 三行。
/// e2e 在主機上直接跑執行檔，沒有 image 裡的模板，所以以 [`RELEASE_DIR_ENV`] 指到 [`release`] 建的目錄。
pub mod shell {
    use std::fs;
    use std::path::Path;

    use sha2::{Digest, Sha256};

    /// 引擎讀出貨輸入的測試用目錄（engine/vendor_kit 的 `RELEASE_DIR_ENV`；照抄名字）。
    pub const RELEASE_DIR_ENV: &str = "VK_TEST_RELEASE_DIR";
    /// 這一版引擎的介面版（engine/compat 的 `THIS.current_protocol`；照抄）。
    pub const INTERFACE: u32 = 1;
    /// 薄殼四檔的檔名與模板本文，順序同 engine/layout 的 `SHELL_FILES`。
    pub const TEMPLATES: [(&str, &str); 4] = [
        ("entry.just", "# entry\nimport? 'vendor.just'\n"),
        ("vendor.just", "# vendor\n"),
        ("log.sh", "# log\n"),
        (
            ".gitignore",
            "cache/\ngen/\nlog/\nversion.local.toml\n.tmp.*\n",
        ),
    ];

    /// 標頭三行接著原樣的 `body`；sha256 是 `body` CRLF→LF 正規化後的。
    pub fn render(interface: u32, engine: &str, body: &str) -> String {
        let normalized = body.replace("\r\n", "\n");
        let sha: String = Sha256::digest(normalized.as_bytes())
            .iter()
            .map(|b| format!("{b:02x}"))
            .collect();
        format!(
            "# vendor_kit-shell interface {interface}\n\
             # vendor_kit-shell engine {engine}\n\
             # vendor_kit-shell sha256 {sha}\n{body}"
        )
    }

    /// 在 `dir` 建出貨輸入的目錄：`shell/` 下放 [`TEMPLATES`]。
    pub fn release(dir: &Path) -> std::io::Result<()> {
        fs::create_dir_all(dir.join("shell"))?;
        for (name, body) in TEMPLATES {
            fs::write(dir.join("shell").join(name), body)?;
        }
        Ok(())
    }

    /// 在安裝目錄的 `.vendor_kit/` 寫跟這一版引擎（`engine` 是引擎版 `v<X.Y.Z>`）一致的薄殼四檔。
    pub fn install(root: &Path, engine: &str) -> std::io::Result<()> {
        let vk = root.join(".vendor_kit");
        fs::create_dir_all(&vk)?;
        for (name, body) in TEMPLATES {
            fs::write(vk.join(name), render(INTERFACE, engine, body))?;
        }
        Ok(())
    }
}
