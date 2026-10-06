//! `add` 印到 stdout 的字句與詢問文字（英文，03 輸出）。這些不是診斷，訊息表不登錄；
//! 契約沒定字句，這裡是第一版的寫法。

use imageref::ImageRef;
use initfiles::{Ask, FilePlan, Verdict};

/// 這次 `<repo>` 用的是本機開發來源 `<dir>`（正規化後、存進 `version.local.toml` 的值）；字句跟 engine/sync
/// 相同。
pub fn local_override(repo: &str, dir: &str) -> String {
    format!("{repo} uses the local source {dir} (local override).")
}

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

/// 預演：會導入的版本（`--dry-run`，見 crate 文件「預演」）。
pub fn would_add(repo: &str, locked: &ImageRef) -> String {
    format!("Would add {repo} {} ({locked}).", locked.tag())
}

/// 預演：會一併完成的殘留 `add`。
pub fn would_recover(repo: &str, locked: &ImageRef) -> String {
    format!(
        "Would complete the interrupted add of {repo} {} ({locked}).",
        locked.tag()
    )
}

/// 預演：一個初始檔會寫什麼；沒有寫入的判定回 `None`。
pub fn would_file_line(f: &FilePlan) -> Option<String> {
    let word = match f.verdict {
        Verdict::Create => "create",
        Verdict::Append => "append to",
        Verdict::Replace => "update",
        Verdict::Merge { .. } => "merge",
        _ => return None,
    };
    Some(format!("Would {word} {}", f.path))
}

/// 一題詢問（`prompt` 會在後面接 ` [y/N] `）。
pub fn question(repo: &str, path: &str, ask: Ask) -> String {
    match ask {
        Ask::Append => format!("Append the lines from {repo} to the existing {path}?"),
        Ask::Replace => format!("Replace {path} with the version from {repo}?"),
        Ask::Merge => format!("Merge the new version of {path} from {repo}?"),
    }
}

/// 帶 `-y` 又不能互動、卻有要 append 進既有檔的詢問：VK0056 的 `<reason>`（不含結尾的草稿碼）。
pub fn yes_append(files: &[&str]) -> String {
    format!(
        "-y does not append to existing files that are not yet managed ({}); run from a terminal to answer",
        files.join(", ")
    )
}

/// VK0031 的 `<reason>`：inspect 的 RepoDigests 沒有這個 image 名稱的 digest。
pub fn no_repo_digest(name: &str) -> String {
    format!("it has no repository digest for {name}")
}

/// VK0055 的 `<reason>`：啟動器代做的 docker 動作失敗。
pub fn docker_failed(op: &str, rc: u8) -> String {
    format!("docker {op} exited with {rc}")
}

/// VK0031 的 `<reason>`：線上解析時本機 image 沒有這個 registry 與路徑的 RepoDigest（訊息表列的填法之一）。
pub const DIGEST_MISSING: &str = "required digest information is missing";

/// VK0055 的 `<reason>`：registry 列得到、但一個 tag 都沒有（同 engine/update；模組說明的缺口）。
pub const NO_TAGS: &str = "the registry lists no tags";

/// VK0055 的 `<reason>`：token 檔不是 UTF-8（同 engine/update）。
pub const TOKEN_NOT_UTF8: &str = "the registry token file is not UTF-8";

/// VK0055 的 `<reason>`：token 檔去掉前後空白後是空的（同 engine/update）。
pub const TOKEN_EMPTY: &str = "the registry token file is empty";

/// VK0055 的 `<reason>`：讀 token 檔失敗（同 engine/update）。
pub fn token_unreadable(error: &str) -> String {
    format!("cannot read the registry token file: {error}")
}

/// VK0055 的 `<reason>`：token 檔的主機路徑放不進往返協定的欄位（同 engine/update）。
pub fn token_unpassable(error: &str) -> String {
    format!("cannot pass the registry token file path to the launcher: {error}")
}

/// VK0055 的 `<reason>`：啟動器複製 token 檔失敗（同 engine/update）。
pub fn token_copy_failed(rc: u8) -> String {
    format!("the launcher could not copy the registry token file (exit {rc})")
}

/// 同一個 tag 指向不同 digest（VK0056 的 `<reason>` 前段，後面接草稿碼的說明；同 engine/upgrade）：
/// `<image>` 是 `<registry>/<路徑>:<tag>`，`digests` 依找到的順序（本機的在前、registry 的在後）。
pub fn tag_digests(image: &str, digests: &[String]) -> String {
    format!(
        "{image} points to more than one digest ({})",
        digests.join(", ")
    )
}
