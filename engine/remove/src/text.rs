//! `remove`、`uninstall` 印到 stdout 的字句與詢問文字（英文，03 輸出）。這些不是診斷，訊息表不登錄；
//! 契約沒定字句，這裡是第一版的寫法。改動與保留的字句都有預演（`--dry-run`）的寫法：`dry` 為真時印「Would …」。

use retract::{Owner, Question};

/// 這次 `<repo>` 用的是本機開發來源 `<dir>`（正規化後、存進 `version.local.toml` 的值）；字句跟 engine/sync
/// 相同。
pub fn local_override(repo: &str, dir: &str) -> String {
    format!("{repo} uses the local source {dir} (local override).")
}

/// 答否的正常取消（03 輸出：不做變更，在 stdout 說明未變更）。
pub const NO_CHANGES: &str = "No changes were made.";

/// 預演時的動詞換成「Would <原形>」。
fn verb(dry: bool, done: &'static str, base: &'static str) -> String {
    if dry {
        format!("Would {base}")
    } else {
        done.to_owned()
    }
}

/// 解除了一個工具；預演時是會解除的。
pub fn removed(repo: &str, tag: &str, locked: &str, dry: bool) -> String {
    let v = verb(dry, "Removed", "remove");
    format!("{v} {repo} {tag} ({locked}).")
}

/// 這次一併完成了殘留的 `remove`（版本鎖定行裡已經沒有這個工具）；預演時是會一併完成。
pub fn recovered(repo: &str, dry: bool) -> String {
    let v = verb(dry, "Completed", "complete");
    format!("{v} the interrupted remove of {repo}.")
}

/// 移除了 VK；預演時是會移除。
pub fn uninstalled(install_dir: &str, dry: bool) -> String {
    let v = verb(dry, "Uninstalled", "uninstall");
    format!("{v} vendor_kit from {install_dir}.")
}

/// 收回了一個檔裡插入的行；預演時是會收回。
pub fn retracted(path: &str, dry: bool) -> String {
    let v = verb(dry, "Removed", "remove");
    format!("{v} inserted lines from {path}")
}

/// 保留清單的一項（04：`remove`、`uninstall` 保留初始檔，保留清單印到 stdout）；預演時是會保留。
pub fn kept(path: &str, dry: bool) -> String {
    let v = verb(dry, "Kept", "keep");
    format!("{v} {path}")
}

/// `remove` 解除了對象的本機覆寫（04 本機覆寫：報告用了哪個覆寫，不加診斷前綴）；預演時是會解除。
pub fn lifted_override(repo: &str, dir: &str, dry: bool) -> String {
    let v = verb(dry, "Removed", "remove");
    format!("{v} the local override of {repo} ({dir}).")
}

/// `remove`、`uninstall` 解除覆寫時保留的本機開發來源；預演時是會保留。
pub fn kept_local_source(repo: &str, dir: &str, dry: bool) -> String {
    let v = verb(dry, "Kept", "keep");
    format!("{v} the local development source of {repo}: {dir}")
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
