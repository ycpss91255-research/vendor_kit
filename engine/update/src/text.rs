//! `update` 印的字句（英文）。結果行的格式是 04 update 節定的固定格式；本機覆寫的提醒是 04 本機覆寫
//! 要求印到 stderr、不加診斷前綴的那一行，契約沒定字句，這裡是第一版的寫法。這些都不是診斷，訊息表不登錄。

use imageref::Tag;

/// 引擎在結果行的工具名欄（04 update：引擎的工具名欄用 `vendor_kit`）。
pub const ENGINE_NAME: &str = "vendor_kit";

/// 查詢失敗、或 registry 有 tag 卻沒有合法 `vX.Y.Z` 時 `latest:` 的顯示值。
pub const NONE: &str = "none";

/// 一個查詢對象的結果行：`<repo> current: <tag> latest: <tag>`。欄位以單一 ASCII 空白分隔，欄名以
/// 半形冒號結尾；`latest` 是 `None` 時印 `latest: none`。
pub fn result_line(repo: &str, current: Tag, latest: Option<Tag>) -> String {
    let latest = latest.map_or_else(|| NONE.to_owned(), |t| t.to_string());
    format!("{repo} current: {current} latest: {latest}")
}

/// 本機覆寫的提醒（stderr，不加前綴）：`update` 仍照版本鎖定行查，不查覆寫來源。
pub fn override_notice(target: &str, source: &str) -> String {
    format!("{target} uses the local override {source}; update checks the lock version line.")
}
