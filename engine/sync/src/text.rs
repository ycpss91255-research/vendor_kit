//! `sync` 印到 stdout 的字句（英文，03 輸出：成功時改了什麼印到 stdout）。這些不是診斷，訊息表不登錄；
//! 契約沒定字句，這裡是第一版的寫法。
//!
//! 什麼都沒改時不印任何字：03 輸出只要求印「改了什麼」，`sync` 不在 04「stdout 說明未變更」的指令裡，
//! 而且工具 recipe 前的自動 `sync` 回 `0` 時 stdout、stderr 都不印（#119）。

use imageref::ImageRef;

/// 依版本鎖定行取件並換好 `cache/<repo>/`。
pub fn fetched(repo: &str, locked: &ImageRef) -> String {
    format!("Fetched {repo} {} ({locked}).", locked.tag())
}

/// 重產了入口檔。
pub const TOOLS_JUST_UPDATED: &str = "Updated .vendor_kit/gen/tools.just.";

/// 完成了殘留的 `sync`（進度檔已刪）。
pub fn recovered(file: &str) -> String {
    format!("Completed the interrupted sync recorded in {file}.")
}

/// VK0055 的 `<reason>`：啟動器代做的 docker 動作失敗。
pub fn docker_failed(op: &str, rc: u8) -> String {
    format!("docker {op} exited with {rc}")
}
