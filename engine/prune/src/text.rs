//! `prune` 印到 stdout 的字句（英文，03 輸出：成功時改了什麼印到 stdout）。這些不是診斷，訊息表不登錄；
//! 契約沒定字句，這裡是第一版的寫法。
//!
//! 04 成對與無害：`prune` 不詢問，stdout 列出清理內容。什麼都沒清時不印任何字：03 輸出只要求印
//! 「改了什麼」，`prune` 不在 04「stdout 說明未變更」的指令裡（同 engine/sync 的做法）。

/// 刪了安裝目錄裡的一個路徑（相對於安裝目錄；目錄以 `/` 結尾）。
pub fn removed(path: &str) -> String {
    format!("Removed {path}.")
}

/// 請啟動器刪了一個已停止的 VK 容器。
pub fn removed_container(id: &str) -> String {
    format!("Removed stopped container {id}.")
}

/// 完成了殘留的 `prune`（進度檔已刪）。
pub fn recovered(file: &str) -> String {
    format!("Completed the interrupted prune recorded in {file}.")
}

/// VK0056 的 `<reason>` 裡的一段：啟動器代做的 docker 動作失敗。
pub fn docker_failed(op: &str, rc: u8) -> String {
    format!("docker {op} exited with {rc}")
}
