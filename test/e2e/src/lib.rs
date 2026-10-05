//! 端到端測試共用的輔助：找出受測的執行檔、扮演啟動器。測試本體在 `tests/`。

// 測試輔助：失敗就讓測試失敗，unwrap 放行（workspace lints 的測試例外）。
#[allow(clippy::unwrap_used, clippy::expect_used)]
pub mod launcher;

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
