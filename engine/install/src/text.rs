//! `install` 印到 stdout 的字句與詢問文字（英文，03 輸出）。這些不是診斷，訊息表不登錄；
//! 契約沒定字句，這裡是第一版的寫法。

use imageref::ImageRef;

/// 答否的正常取消（03 輸出：不做變更，在 stdout 說明未變更）。
pub const NO_CHANGES: &str = "No changes were made.";

/// 安裝完成。
pub fn installed(version: &str, install_dir: &str) -> String {
    format!("Installed vendor_kit {version} in {install_dir}.")
}

/// 已完整且一致（04 成對與無害：stdout 說明未變更）。
pub fn unchanged(install_dir: &str) -> String {
    format!("vendor_kit is already installed in {install_dir}; no changes were made.")
}

/// 這次一併完成了殘留的 `install`。
pub const RECOVERED: &str = "Completed the interrupted install.";

/// 寫了引擎版本鎖定行。
pub fn locked(engine: &ImageRef) -> String {
    format!("Locked the engine to {} ({engine}).", engine.tag())
}

/// 寫了一個薄殼檔（`.vendor_kit/` 下的檔名）。
pub fn wrote_shell(name: &str) -> String {
    format!("Wrote .vendor_kit/{name}")
}

/// 新建了一個根目錄的檔。
pub fn created(path: &str) -> String {
    format!("Created {path}")
}

/// 在既有的根目錄檔插入了行。
pub fn appended(path: &str) -> String {
    format!("Appended to {path}")
}

/// 一題詢問（`prompt` 會在後面接 ` [y/N] `）。
pub fn question(path: &str, count: usize) -> String {
    let lines = if count == 1 { "line" } else { "lines" };
    format!("Append {count} vendor_kit {lines} to the existing {path}?")
}
