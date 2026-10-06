//! `dev`、`undev` 印到 stdout 的字句（英文，03 輸出：成功時改了什麼印到 stdout；04 本機覆寫：重複 `dev`
//! 同來源、或工具存在但無覆寫與未完成操作的 `undev`，stdout 說明未變更；每次報告用了哪個覆寫）。
//! 這些不是診斷，訊息表不登錄；契約沒定字句，這裡是第一版的寫法。改動的字句都有預演（`--dry-run`）的寫法：
//! `dry` 為真時印「Would …」；未變更的字句預演時照印。

use imageref::ImageRef;

/// `dev <repo> -p <dir>` 開好覆寫；預演（`--dry-run`）時是會開的。
pub fn dev_enabled(repo: &str, dir: &str, dry: bool) -> String {
    let verb = if dry { "would use" } else { "now uses" };
    format!("{repo} {verb} the local source {dir} (local override).")
}

/// 重複 `dev` 同來源。
pub fn dev_unchanged(repo: &str, dir: &str) -> String {
    format!("{repo} already uses the local source {dir}. No changes were made.")
}

/// `dev --engine -i <image>` 開好覆寫；預演時是會開的。
pub fn dev_engine_enabled(image: &str, dry: bool) -> String {
    let verb = if dry { "would use" } else { "now uses" };
    format!("The engine {verb} the local image {image} (local override).")
}

/// 重複 `dev --engine` 同一個 image。
pub fn dev_engine_unchanged(image: &str) -> String {
    format!("The engine already uses the local image {image}. No changes were made.")
}

/// `undev <repo>` 解除覆寫，回到鎖定版本；預演時是會解除的。
pub fn undev_tool(repo: &str, locked: &ImageRef, dry: bool) -> String {
    let (removed, uses) = if dry {
        ("Would remove", "would use")
    } else {
        ("Removed", "uses")
    };
    format!(
        "{removed} the local override of {repo}; {repo} {uses} {} ({locked}).",
        locked.tag()
    )
}

/// `undev --engine` 解除覆寫，回到鎖定版本；預演時是會解除的。
pub fn undev_engine(locked: &ImageRef, dry: bool) -> String {
    let (removed, uses) = if dry {
        ("Would remove", "would use")
    } else {
        ("Removed", "uses")
    };
    format!(
        "{removed} the local override of the engine; the engine {uses} {} ({locked}).",
        locked.tag()
    )
}

/// 工具存在但無覆寫與未完成操作的 `undev <repo>`。
pub fn undev_tool_unchanged(repo: &str) -> String {
    format!("{repo} has no local override. No changes were made.")
}

/// 沒有引擎覆寫與未完成操作的 `undev --engine`。
pub const UNDEV_ENGINE_UNCHANGED: &str = "The engine has no local override. No changes were made.";

/// `undev <repo>` 依版本鎖定行取件並換好 `cache/<repo>/`（字句同 engine/sync）；預演時是取到、會換的。
pub fn fetched(repo: &str, locked: &ImageRef, dry: bool) -> String {
    let verb = if dry { "Would fetch" } else { "Fetched" };
    format!("{verb} {repo} {} ({locked}).", locked.tag())
}

/// 重產了入口檔；預演時是會重產。
pub fn tools_just_updated(dry: bool) -> &'static str {
    if dry {
        "Would update .vendor_kit/gen/tools.just."
    } else {
        "Updated .vendor_kit/gen/tools.just."
    }
}

/// 完成了殘留的 `dev` 或 `undev`（進度檔已刪）；預演時是會完成的。
pub fn recovered(verb: &str, file: &str, dry: bool) -> String {
    let v = if dry { "Would complete" } else { "Completed" };
    format!("{v} the interrupted {verb} recorded in {file}.")
}
