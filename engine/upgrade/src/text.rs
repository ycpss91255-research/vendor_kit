//! `upgrade` 印到 stdout 的字句與詢問文字（英文，03 輸出）。這些不是診斷，訊息表不登錄；
//! 契約沒定字句，這裡是第一版的寫法。

use imageref::{ImageRef, Tag};
use initfiles::{Ask, FilePlan, Gap, Syntax, Verdict};

/// 答否的正常取消（03 輸出：不做變更，在 stdout 說明未變更）。
pub const NO_CHANGES: &str = "No changes were made.";

/// 這次 `<repo>` 用的是本機開發來源 `<dir>`（正規化後、相對於安裝目錄）；字句跟 engine/sync 相同。
pub fn local_override(repo: &str, dir: &str) -> String {
    format!("{repo} uses the local source {dir} (local override).")
}

/// 換版完成。
pub fn upgraded(repo: &str, from: &ImageRef, to: &ImageRef) -> String {
    format!(
        "Upgraded {repo} from {} to {} ({to}).",
        from.tag(),
        to.tag()
    )
}

/// 已是指定的版本（04 成對與無害：已完整且一致的 `upgrade`，stdout 說明未變更）。
pub fn unchanged(repo: &str, tag: Tag) -> String {
    format!("{repo} is already at {tag}; no changes were made.")
}

/// 恢復了殘留的 `upgrade`。
pub fn recovered(repo: &str, locked: &ImageRef) -> String {
    format!(
        "Completed the interrupted upgrade of {repo} to {} ({locked}).",
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
        Verdict::Unparsable { syntax, .. } => {
            let kind = match syntax {
                Syntax::Toml => "TOML",
                Syntax::Just => "just",
            };
            return Some(format!(
                "Kept {}: the merged version is not valid {kind}; recorded in conflicts",
                f.path
            ));
        }
        _ => return None,
    };
    Some(format!("{word} {}", f.path))
}

/// 04 寫入既有檔的例外：新版不再提供的初始檔、使用者已刪的納管初始檔，不刪、不重建，只列清單。
/// 不在清單裡的判定回 `None`。
pub fn listed_line(repo: &str, tag: Tag, f: &FilePlan) -> Option<String> {
    match f.verdict {
        Verdict::UserDeleted | Verdict::StillDeleted => {
            Some(format!("Not recreated (deleted): {}", f.path))
        }
        Verdict::Gap(Gap::NoLongerProvided) => Some(format!(
            "Kept (no longer provided by {repo} {tag}): {}",
            f.path
        )),
        _ => None,
    }
}

/// 一題詢問（`prompt` 會在後面接 ` [y/N] `）。
pub fn question(repo: &str, path: &str, ask: Ask) -> String {
    match ask {
        Ask::Append => format!("Append the lines from {repo} to the existing {path}?"),
        Ask::Replace => format!("Replace {path} with the new version from {repo}?"),
        Ask::Merge => format!("Merge the new version of {path} from {repo}?"),
    }
}

/// VK0055 的 `<reason>`：啟動器代做的 docker 動作失敗。
pub fn docker_failed(op: &str, rc: u8) -> String {
    format!("docker {op} exited with {rc}")
}
