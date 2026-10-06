//! 只檢查與修復印到 stdout 的字句（英文，03 輸出：成功時改了什麼、檢查結果印到 stdout，不加前綴）。
//! 這些不是診斷，訊息表不登錄；契約沒定字句，這裡是第一版的寫法。

use shell::Status;

/// 四檔都跟這一版引擎的模板一致（只檢查與修復都印；修復時表示沒有重產）。
pub const CONSISTENT: &str = "Shell files match this engine version's templates.";

/// 修復時，逐檔列出差異前的一行。
pub const DIFFERENCES: &str = "Shell files that do not match this engine version's templates:";

/// 一個不符的檔：`.vendor_kit/<檔名> (<哪一種>)`，跟 VK0006 的 `<files>` 同一種寫法。
pub fn file(name: &str, status: Status) -> String {
    format!("{}/{name} ({status})", layout::VK_DIR)
}

/// 修復時重產了一個檔。
pub fn regenerated(name: &str) -> String {
    format!("Regenerated {}/{name}.", layout::VK_DIR)
}
