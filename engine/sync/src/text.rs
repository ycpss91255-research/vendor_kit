//! `sync` 印到 stdout 的字句（英文，03 輸出：成功時改了什麼印到 stdout）。這些不是診斷，訊息表不登錄；
//! 契約沒定字句，這裡是第一版的寫法。
//!
//! 什麼都沒改時只報告用了哪個覆寫（04 本機覆寫：每次報告用了哪個覆寫，不加診斷前綴，`update` 以外到
//! stdout），沒有覆寫就不印任何字：03 輸出只要求印「改了什麼」，`sync` 不在 04「stdout 說明未變更」的
//! 指令裡。

use imageref::ImageRef;

/// 這次 `<repo>` 用的是本機開發來源 `<dir>`（正規化後、相對於安裝目錄）。
pub fn local_override(repo: &str, dir: &str) -> String {
    format!("{repo} uses the local source {dir} (local override).")
}

/// 依版本鎖定行取件並換好 `cache/<repo>/`。
pub fn fetched(repo: &str, locked: &ImageRef) -> String {
    format!("Fetched {repo} {} ({locked}).", locked.tag())
}

/// 重產了入口檔。
pub const TOOLS_JUST_UPDATED: &str = "Updated .vendor_kit/gen/tools.just.";

/// VK0055 的 `<reason>`：啟動器代做的 docker 動作失敗。
pub fn docker_failed(op: &str, rc: u8) -> String {
    format!("docker {op} exited with {rc}")
}
