//! `add` 印到 stdout 的字句與詢問文字（英文，03 輸出）。這些不是診斷，訊息表不登錄；
//! 契約沒定字句，這裡是第一版的寫法。

use imageref::ImageRef;
use initfiles::{Ask, FilePlan, Verdict};

/// 答否的正常取消（03 輸出：不做變更，在 stdout 說明未變更）。
pub const NO_CHANGES: &str = "No changes were made.";

/// 導入完成。
pub fn added(repo: &str, locked: &ImageRef) -> String {
    format!("Added {repo} {} ({locked}).", locked.tag())
}

/// 已完整導入同一個版本（04 成對與無害：stdout 說明未變更）。
pub fn unchanged(repo: &str, locked: &ImageRef) -> String {
    format!(
        "{repo} {} is already added; no changes were made.",
        locked.tag()
    )
}

/// 恢復了殘留的 `add`。
pub fn recovered(repo: &str, locked: &ImageRef) -> String {
    format!(
        "Completed the interrupted add of {repo} {} ({locked}).",
        locked.tag()
    )
}

/// 一個初始檔寫了什麼；沒有寫入的判定回 `None`。
pub fn file_line(f: &FilePlan) -> Option<String> {
    let word = match f.verdict {
        Verdict::Create => "Created",
        Verdict::Append => "Appended to",
        Verdict::Replace => "Updated",
        Verdict::Merge { .. } => "Merged",
        _ => return None,
    };
    Some(format!("{word} {}", f.path))
}

/// 一題詢問（`prompt` 會在後面接 ` [y/N] `）。
pub fn question(repo: &str, path: &str, ask: Ask) -> String {
    match ask {
        Ask::Append => format!("Append the lines from {repo} to the existing {path}?"),
        Ask::Replace => format!("Replace {path} with the version from {repo}?"),
        Ask::Merge => format!("Merge the new version of {path} from {repo}?"),
    }
}

/// VK0031 的 `<reason>`：inspect 的 RepoDigests 沒有這個 image 名稱的 digest。
pub fn no_repo_digest(name: &str) -> String {
    format!("it has no repository digest for {name}")
}

/// VK0055 的 `<reason>`：啟動器代做的 docker 動作失敗。
pub fn docker_failed(op: &str, rc: u8) -> String {
    format!("docker {op} exited with {rc}")
}
