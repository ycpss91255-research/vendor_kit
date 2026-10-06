//! `prune` 印到 stdout 的字句（英文，03 輸出：成功時改了什麼印到 stdout）。這些不是診斷，訊息表不登錄；
//! 契約沒定字句，這裡是第一版的寫法。
//!
//! 04 成對與無害：`prune` 不詢問，stdout 列出清理內容。什麼都沒清時不印任何字：03 輸出只要求印
//! 「改了什麼」，`prune` 不在 04「stdout 說明未變更」的指令裡（同 engine/sync 的做法）。預演（`--dry-run`）
//! 時改動的字句換成「Would …」，最後一行是 `prompt::DRY_RUN_DONE`（crate 文件「預演」）。

/// 刪了安裝目錄裡的一個路徑（相對於安裝目錄；目錄以 `/` 結尾）；預演（`--dry-run`）時是會刪的。
pub fn removed(path: &str, dry: bool) -> String {
    let verb = if dry { "Would remove" } else { "Removed" };
    format!("{verb} {path}.")
}

/// 請啟動器刪了一個已停止的 VK 容器。
pub fn removed_container(id: &str) -> String {
    format!("Removed stopped container {id}.")
}

/// 預演：會請啟動器刪的一個已停止的 VK 容器。
pub fn would_remove_container(id: &str) -> String {
    format!("Would remove stopped container {id}.")
}

/// 完成了殘留的 `prune`（進度檔已刪）；預演時是會完成的。
pub fn recovered(file: &str, dry: bool) -> String {
    let verb = if dry { "Would complete" } else { "Completed" };
    format!("{verb} the interrupted prune recorded in {file}.")
}

/// VK0056 的 `<reason>` 裡的一段：啟動器代做的 docker 動作失敗。
pub fn docker_failed(op: &str, rc: u8) -> String {
    format!("docker {op} exited with {rc}")
}
