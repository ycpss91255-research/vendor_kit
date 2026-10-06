//! `test`、`test dist` 印到 stdout 的字句（英文，03 輸出：檢查結果印到 stdout，不加前綴），與 VK0047 `<files>` 裡標出
//! 「是哪一種」的字。這些不是診斷，訊息表不登錄；契約沒定字句，這裡是第一版的寫法。

use std::fmt::Display;

/// 完整安裝檢查全部通過。
pub const PASSED: &str = "Install check passed.";
/// `test dist` 的交付規則全部通過。
pub const DIST_PASSED: &str = "Delivery check passed.";

/// 該有的檔或目錄不在。
pub const MISSING: &str = "missing";
/// 印記沒有、`cache/<repo>/` 裡多出的檔。
pub const EXTRA: &str = "extra";
/// 內容跟印記（或應有的入口檔）不同。
pub const CHANGED: &str = "changed";
/// 印記損壞。
pub const CORRUPT: &str = "corrupt";
/// 印記記的版本跟版本鎖定行不同。
pub const OTHER_VERSION: &str = "other version";

/// `<files>` 的一項：`<相對於安裝目錄的路徑> (<哪一種>)`，跟 VK0006 同一種寫法。
pub fn file(path: &str, kind: impl Display) -> String {
    format!("{path} ({kind})")
}
