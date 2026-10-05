//! `remove`、`uninstall` 印到 stdout 的字句與詢問文字（英文，03 輸出）。這些不是診斷，訊息表不登錄；
//! 契約沒定字句，這裡是第一版的寫法。

use retract::{Owner, Question};

/// 答否的正常取消（03 輸出：不做變更，在 stdout 說明未變更）。
pub const NO_CHANGES: &str = "No changes were made.";

/// 解除了一個工具。
pub fn removed(repo: &str, tag: &str, locked: &str) -> String {
    format!("Removed {repo} {tag} ({locked}).")
}

/// 這次一併完成了殘留的 `remove`（版本鎖定行裡已經沒有這個工具）。
pub fn recovered(repo: &str) -> String {
    format!("Completed the interrupted remove of {repo}.")
}

/// 移除了 VK。
pub fn uninstalled(install_dir: &str) -> String {
    format!("Uninstalled vendor_kit from {install_dir}.")
}

/// 收回了一個檔裡插入的行。
pub fn retracted(path: &str) -> String {
    format!("Removed inserted lines from {path}")
}

/// 保留清單的一項（04：`remove`、`uninstall` 保留初始檔，保留清單印到 stdout）。
pub fn kept(path: &str) -> String {
    format!("Kept {path}")
}

/// `uninstall` 解除覆寫時保留的本機開發來源。
pub fn kept_local_source(repo: &str, dir: &str) -> String {
    format!("Kept the local development source of {repo}: {dir}")
}

/// 一題詢問（`prompt` 會在後面接 ` [y/N] `）。
pub fn question(q: &Question) -> String {
    let count = q.lines.len();
    let lines = if count == 1 { "line" } else { "lines" };
    match &q.owner {
        Owner::Tool(repo) => {
            format!(
                "Remove the {count} {lines} that {repo} appended to {}?",
                q.path
            )
        }
        Owner::Vk => format!(
            "Remove the {count} {lines} that vendor_kit appended to {}?",
            q.path
        ),
    }
}

/// VK0061 的 `<line_numbers>`：沒有相符行時印 `none`。
pub fn line_numbers(numbers: &[usize]) -> String {
    if numbers.is_empty() {
        return "none".to_owned();
    }
    let parts: Vec<String> = numbers.iter().map(usize::to_string).collect();
    parts.join(", ")
}
