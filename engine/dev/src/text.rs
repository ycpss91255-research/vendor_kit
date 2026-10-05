//! `dev`、`undev` 印到 stdout 的字句（英文，03 輸出：成功時改了什麼印到 stdout；04 本機覆寫：重複 `dev`
//! 同來源、或工具存在但無覆寫與未完成操作的 `undev`，stdout 說明未變更；每次報告用了哪個覆寫）。
//! 這些不是診斷，訊息表不登錄；契約沒定字句，這裡是第一版的寫法。

use imageref::ImageRef;

/// `dev <repo> -p <dir>` 開好覆寫。
pub fn dev_enabled(repo: &str, dir: &str) -> String {
    format!("{repo} now uses the local source {dir} (local override).")
}

/// 重複 `dev` 同來源。
pub fn dev_unchanged(repo: &str, dir: &str) -> String {
    format!("{repo} already uses the local source {dir}. No changes were made.")
}

/// `undev <repo>` 解除覆寫，回到鎖定版本。
pub fn undev_tool(repo: &str, locked: &ImageRef) -> String {
    format!(
        "Removed the local override of {repo}; {repo} uses {} ({locked}).",
        locked.tag()
    )
}

/// `undev --engine` 解除覆寫，回到鎖定版本。
pub fn undev_engine(locked: &ImageRef) -> String {
    format!(
        "Removed the local override of the engine; the engine uses {} ({locked}).",
        locked.tag()
    )
}

/// 工具存在但無覆寫與未完成操作的 `undev <repo>`。
pub fn undev_tool_unchanged(repo: &str) -> String {
    format!("{repo} has no local override. No changes were made.")
}

/// 沒有引擎覆寫與未完成操作的 `undev --engine`。
pub const UNDEV_ENGINE_UNCHANGED: &str = "The engine has no local override. No changes were made.";

/// 重產了入口檔。
pub const TOOLS_JUST_UPDATED: &str = "Updated .vendor_kit/gen/tools.just.";

/// 完成了殘留的 `dev` 或 `undev`（進度檔已刪）。
pub fn recovered(verb: &str, file: &str) -> String {
    format!("Completed the interrupted {verb} recorded in {file}.")
}
