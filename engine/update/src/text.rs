//! `update` 印的字句（英文）。結果行的格式是 04 update 節定的固定格式；本機覆寫的提醒是 04 本機覆寫
//! 要求印到 stderr、不加診斷前綴的那一行，契約沒定字句，這裡是第一版的寫法。這些都不是診斷，訊息表不登錄。
//! 另有填進 VK0055 `<reason>` 的說明（token 檔讀不到、registry 沒有 tag），也是這裡第一版的寫法。

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

/// VK0055 的 `<reason>`：registry 列得到、但一個 tag 都沒有（模組說明的缺口）。
pub const NO_TAGS: &str = "the registry lists no tags";

/// VK0055 的 `<reason>`：token 檔不是 UTF-8。
pub const TOKEN_NOT_UTF8: &str = "the registry token file is not UTF-8";

/// VK0055 的 `<reason>`：token 檔去掉前後空白後是空的。
pub const TOKEN_EMPTY: &str = "the registry token file is empty";

/// VK0055 的 `<reason>`：讀 token 檔失敗。
pub fn token_unreadable(error: &str) -> String {
    format!("cannot read the registry token file: {error}")
}

/// VK0055 的 `<reason>`：token 檔的主機路徑放不進往返協定的欄位。
pub fn token_unpassable(error: &str) -> String {
    format!("cannot pass the registry token file path to the launcher: {error}")
}

/// VK0055 的 `<reason>`：啟動器複製 token 檔失敗。
pub fn token_copy_failed(rc: u8) -> String {
    format!("the launcher could not copy the registry token file (exit {rc})")
}
