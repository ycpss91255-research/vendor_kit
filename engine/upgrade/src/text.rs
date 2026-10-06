//! `upgrade` 印到 stdout 的字句與詢問文字（英文，03 輸出）。這些不是診斷，訊息表不登錄；
//! 契約沒定字句，這裡是第一版的寫法。改動的字句都有預演（`--dry-run`）的寫法：`dry` 為真時印「Would …」。

use imageref::{ImageRef, Tag};
use initfiles::{Ask, FilePlan, Gap, Syntax, Verdict};

/// 答否的正常取消（03 輸出：不做變更，在 stdout 說明未變更）。
pub const NO_CHANGES: &str = "No changes were made.";

/// 這次 `<repo>` 用的是本機開發來源 `<dir>`（正規化後、存進 `version.local.toml` 的值：安裝目錄裡的是相對
/// 路徑，安裝目錄外的是開頭為 `..` 的相對路徑或絕對路徑）；字句跟 engine/sync 相同。
pub fn local_override(repo: &str, dir: &str) -> String {
    format!("{repo} uses the local source {dir} (local override).")
}

/// 換版完成；預演時是會換的版本。
pub fn upgraded(repo: &str, from: &ImageRef, to: &ImageRef, dry: bool) -> String {
    let verb = if dry { "Would upgrade" } else { "Upgraded" };
    format!("{verb} {repo} from {} to {} ({to}).", from.tag(), to.tag())
}

/// 已是指定的版本（04 成對與無害：已完整且一致的 `upgrade`，stdout 說明未變更）。
pub fn unchanged(repo: &str, tag: Tag) -> String {
    format!("{repo} is already at {tag}; no changes were made.")
}

/// 恢復了殘留的 `upgrade`；預演時是會一併完成的。
pub fn recovered(repo: &str, locked: &ImageRef, dry: bool) -> String {
    let verb = if dry { "Would complete" } else { "Completed" };
    format!(
        "{verb} the interrupted upgrade of {repo} to {} ({locked}).",
        locked.tag()
    )
}

/// `upgrade --engine` 第二段重產了一個薄殼檔（同 engine/install 的字句）；預演時是會重產的。
pub fn wrote_shell(name: &str, dry: bool) -> String {
    let verb = if dry { "Would write" } else { "Wrote" };
    format!("{verb} .vendor_kit/{name}")
}

/// `upgrade --engine` 第二段把一個 VK 檔（安裝目錄相對路徑）從檔案版 `from` 升到 `to`；預演時是會升的。
pub fn migrated(file: &str, from: u32, to: u32, dry: bool) -> String {
    let verb = if dry { "Would migrate" } else { "Migrated" };
    format!("{verb} {file} from schema version {from} to {to}")
}

/// `upgrade --engine` 第二段做完；預演時是會做完的。
pub fn engine_upgraded(locked: &ImageRef, dry: bool) -> String {
    let verb = if dry { "Would complete" } else { "Completed" };
    format!("{verb} the engine upgrade to {} ({locked}).", locked.tag())
}

/// 預演 `upgrade --engine` 第一段：會換上的引擎版本鎖定行（同 engine/install 的字句）。
pub fn would_lock_engine(locked: &ImageRef) -> String {
    format!("Would lock the engine to {} ({locked}).", locked.tag())
}

/// 預演 `upgrade --engine` 第一段：第二段由新的引擎做，這一版算不出來（engine 模組說明「預演」）。
pub fn would_finish_on(tag: Tag) -> String {
    format!("The rest of the engine upgrade would run on {tag} when the command is run again.")
}

/// 一個初始檔寫了什麼；沒有寫入的判定回 `None`。預演時是會寫什麼。
pub fn file_line(f: &FilePlan, dry: bool) -> Option<String> {
    let word = match (&f.verdict, dry) {
        (Verdict::Create, false) => "Created",
        (Verdict::Create, true) => "Would create",
        (Verdict::Append, false) => "Appended to",
        (Verdict::Append, true) => "Would append to",
        (Verdict::Replace, false) => "Updated",
        (Verdict::Replace, true) => "Would update",
        (Verdict::Merge { .. }, false) => "Merged",
        (Verdict::Merge { .. }, true) => "Would merge",
        (Verdict::Unparsable { syntax, .. }, _) => {
            let kind = match syntax {
                Syntax::Toml => "TOML",
                Syntax::Just => "just",
            };
            let (kept, recorded) = if dry {
                ("Would keep", "would record it")
            } else {
                ("Kept", "recorded")
            };
            return Some(format!(
                "{kept} {}: the merged version is not valid {kind}; {recorded} in conflicts",
                f.path
            ));
        }
        _ => return None,
    };
    Some(format!("{word} {}", f.path))
}

/// 04 寫入既有檔的例外：新版不再提供的初始檔、使用者已刪的納管初始檔，不刪、不重建，只列清單。
/// 不在清單裡的判定回 `None`。預演時是會怎麼列。
pub fn listed_line(repo: &str, tag: Tag, f: &FilePlan, dry: bool) -> Option<String> {
    match f.verdict {
        Verdict::UserDeleted | Verdict::StillDeleted => {
            let not = if dry {
                "Would not recreate"
            } else {
                "Not recreated"
            };
            Some(format!("{not} (deleted): {}", f.path))
        }
        Verdict::Gap(Gap::NoLongerProvided) => {
            let kept = if dry { "Would keep" } else { "Kept" };
            Some(format!(
                "{kept} (no longer provided by {repo} {tag}): {}",
                f.path
            ))
        }
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

/// VK0031 的 `<reason>`：本機 image 沒有這個 registry 與路徑的 RepoDigest（訊息表列的填法之一）。
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

/// 同一個 tag 指向不同 digest（VK0056 的 `<reason>` 前段，後面接草稿碼的說明）：`<image>` 是
/// `<registry>/<路徑>:<tag>`，`digests` 依找到的順序（本機的在前、registry 的在後）。
pub fn tag_digests(image: &str, digests: &[String]) -> String {
    format!(
        "{image} points to more than one digest ({})",
        digests.join(", ")
    )
}
