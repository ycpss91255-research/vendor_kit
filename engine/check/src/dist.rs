//! `test dist`：檢查提供工具的 repo 交付的內容（04 檢查 (test)：給提供工具的 repo 在 CI 用，不能混用 path）。
//!
//! 固定讀 `<安裝目錄>/dist/`（[`DIST_DIR`]），不收 path、不往上找（#372 PR74；04 寫明前提是安裝目錄跟 `dist/`
//! 在同一層）。只讀 `dist/`，不讀 `.vendor_kit/` 的任何狀態，除執行紀錄外零寫入。依序做：
//!
//! 1. `dist/` 不在、或底下一個一般檔都沒有：VK0048，`<path>` 是主機上的 `<安裝目錄>/dist`。`dist/` 在但不是
//!    目錄（一般檔或 symlink）：交付內容不合格式（見下）。
//! 2. 逐條檢查交付規則；有任何一條不過就把每一條都印出來再停下（02 不變量 4：列出每個原因）：
//!    - `dist/init.toml`：初始檔的格式還沒定（#372 N3），有這個檔就以 VK0056 停下（同 engine/add 讀
//!      `init.toml` 的地方），見「缺口」。
//!    - `dist/just/<ns>.just` 每檔一個頂層命名空間（scope_roadmap 多命名空間工具）：跟 `add`、`sync` 取件時
//!      驗的是同一個讀法（`fetch::namespaces`），`just/` 是目錄，底下每一項都是一般檔、名為 `<ns>.just`，
//!      `<ns>` 是合法的 just 名稱。
//!    - `dist/` 底下的每一項都是一般檔或目錄：symlink、FIFO 等在取件時落不了地（`stamp` 走訪會拒絕）。
//!    - 文字檔一律 LF，含 CR 就失敗（ADR-0012：dist/ 的文字檔一律 LF；#372 N24：只查 LF，不用 `.gitattributes`）。
//! 3. 全部通過：stdout 印一行通過（[`text::DIST_PASSED`]），回 0。
//!
//! 不合格的那幾條還沒有專屬代碼，以 VK0056 停下，原因寫明違反哪一條與草稿碼（[`DRAFT_FORMAT`]、
//! [`DRAFT_LF`]）。
//!
//! # 這次自訂的內部細節（契約沒寫）
//!
//! - 「文字檔」：內容不含 NUL 位元組的一般檔；含 NUL 的當二進位檔，不查行尾。
//! - 不讀設定、不取鎖：`dist/` 不是 VK 管的檔，`test dist` 不讀 `.vendor_kit/` 底下的任何狀態，04 鎖與逾時的
//!   「讀取持共享鎖」管的是安裝目錄的狀態。
//! - 違反的規則每一條印一個 VK0056，`<reason>` 寫 `dist/<相對路徑>: <違反什麼>; <草稿碼>`；檔依整條相對路徑的
//!   位元組排序。
//! - 通過時 stdout 的字句（[`text::DIST_PASSED`]）。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則）
//!
//! - `<repo>.just` 必須存在（scope_roadmap 多命名空間工具）：`test dist` 在工具自己的 repo 跑，這個 repo 的
//!   `<repo>` 從哪裡來沒定，先不查。
//! - `init.toml` 的交付規則（例如 append 型的 `.gitignore` 類不能用 copy，scope_roadmap `.gitignore` 類初始檔
//!   的處理）：等 #372 N3 定 `init.toml` 的欄位名；有 `init.toml` 就以 VK0056 停下。
//! - 交付內容不合格式還沒有專屬代碼（草稿 VK0075，N78、N24），以 VK0056 停下。

use std::fs;
use std::io::{self, Read, Write};
use std::os::unix::ffi::OsStrExt;
use std::path::{Path, PathBuf};

use diagnostics::{Diagnostic, Sink};

use super::{Check, Env, text};

/// 交付內容的資料夾，在安裝目錄底下。
pub const DIST_DIR: &str = "dist";
/// 工具交付初始檔清單的檔名（engine/add 的 `INIT_TOML`；指令之間互不依賴，照抄）。
pub const INIT_TOML: &str = "init.toml";

/// 交付內容不合格式的草稿碼（#372 B 清單；定案登錄前以 VK0056 停下，原因寫明草稿碼）。
pub const DRAFT_FORMAT: &str = "reason code pending (draft VK0075, N78)";
/// 文字檔含 CR 的草稿碼。
pub const DRAFT_LF: &str = "reason code pending (draft VK0075, N24)";

/// 讀檔找 NUL、CR 時一次讀多少。
const CHUNK: usize = 64 * 1024;

/// 跑一次 `test dist`，回傳結束碼。
pub fn run<W: Write, S: Sink>(env: &mut Env<'_, W, S>) -> u8 {
    let mut check = Check { env, code: 0 };
    if check.dist() {
        check.say(text::DIST_PASSED);
    }
    check.code
}

/// 一個文字檔的行尾。
#[derive(Debug, PartialEq, Eq)]
enum Content {
    /// 含 NUL：二進位檔，不查。
    Binary,
    /// 文字檔，含 CR。
    HasCr,
    /// 文字檔，只有 LF。
    Lf,
}

/// 讀完整個檔：有 NUL 就是二進位；否則看有沒有 CR。
fn content(path: &Path) -> io::Result<Content> {
    let mut file = fs::File::open(path)?;
    let mut buf = vec![0u8; CHUNK];
    let mut cr = false;
    loop {
        let n = file.read(&mut buf)?;
        if n == 0 {
            break;
        }
        let chunk = &buf[..n];
        if chunk.contains(&0) {
            return Ok(Content::Binary);
        }
        cr |= chunk.contains(&b'\r');
    }
    Ok(if cr { Content::HasCr } else { Content::Lf })
}

/// `dist/` 底下的一項。
enum Item {
    File(PathBuf),
    /// symlink、FIFO 等：一般檔與目錄以外的東西。
    Other(PathBuf),
}

impl Item {
    fn path(&self) -> &Path {
        match self {
            Item::File(p) | Item::Other(p) => p,
        }
    }
}

/// 走訪 `dir`（不跟隨 symlink），把相對於 `root` 的每一項放進 `out`。
fn walk(root: &Path, rel: &Path, out: &mut Vec<Item>) -> io::Result<()> {
    for entry in fs::read_dir(root.join(rel))? {
        let entry = entry?;
        let child = rel.join(entry.file_name());
        // DirEntry::file_type 不跟隨 symlink。
        let ty = entry.file_type()?;
        if ty.is_dir() {
            walk(root, &child, out)?;
        } else if ty.is_file() {
            out.push(Item::File(child));
        } else {
            out.push(Item::Other(child));
        }
    }
    Ok(())
}

impl<W: Write, S: Sink> Check<'_, '_, W, S> {
    /// 檢查 `dist/`（模組說明）；通過回 `true`，否則診斷已印。
    fn dist(&mut self) -> bool {
        let root = self.env.dir.root().join(DIST_DIR);
        let shown = |rel: &Path| format!("{DIST_DIR}/{}", rel.display());
        let no_content = |this: &Self| {
            Diagnostic::new(&messages::VK0048)
                .arg("path", format!("{}/{DIST_DIR}", this.env.host_root))
        };
        match fs::symlink_metadata(&root) {
            Ok(m) if m.is_dir() => {}
            Ok(_) => {
                let d =
                    self.internal_diag(format!("{DIST_DIR} is not a directory; {DRAFT_FORMAT}"));
                self.emit(d);
                return false;
            }
            Err(e) if e.kind() == io::ErrorKind::NotFound => {
                let d = no_content(self);
                self.emit(d);
                return false;
            }
            Err(e) => {
                let d = self.internal_diag(format!("{DIST_DIR}: {e}"));
                self.emit(d);
                return false;
            }
        }

        let mut items = Vec::new();
        if let Err(e) = walk(&root, Path::new(""), &mut items) {
            let d = self.internal_diag(format!("{DIST_DIR}: {e}"));
            self.emit(d);
            return false;
        }
        if items.is_empty() {
            let d = no_content(self);
            self.emit(d);
            return false;
        }
        items.sort_by(|a, b| {
            a.path()
                .as_os_str()
                .as_bytes()
                .cmp(b.path().as_os_str().as_bytes())
        });

        let mut blocked: Vec<Diagnostic> = Vec::new();
        if fs::symlink_metadata(root.join(INIT_TOML)).is_ok() {
            blocked.push(self.gap_diag(format_args!(
                "checking the delivery rules of {DIST_DIR}/{INIT_TOML} (waits for N3)"
            )));
        }
        if let Err(e) = fetch::namespaces(&root) {
            let what = match e {
                fetch::FormatError::NoJustDir => e.to_string(),
                e => format!("{DIST_DIR}/{e}"),
            };
            blocked.push(self.internal_diag(format!("{what}; {DRAFT_FORMAT}")));
        }
        for item in &items {
            match item {
                // `just/` 底下的已由 `fetch::namespaces` 報過。
                Item::Other(rel) if rel.parent() == Some(Path::new(fetch::JUST_DIR)) => {}
                Item::Other(rel) => blocked.push(self.internal_diag(format!(
                    "{}: not a regular file or directory; {DRAFT_FORMAT}",
                    shown(rel)
                ))),
                Item::File(rel) => match content(&root.join(rel)) {
                    Ok(Content::HasCr) => blocked.push(self.internal_diag(format!(
                        "{}: text file contains CR, line endings must be LF; {DRAFT_LF}",
                        shown(rel)
                    ))),
                    Ok(_) => {}
                    Err(e) => blocked.push(self.internal_diag(format!("{}: {e}", shown(rel)))),
                },
            }
        }

        if blocked.is_empty() {
            return true;
        }
        for d in blocked {
            self.emit(d);
        }
        false
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    #[test]
    fn content_tells_binary_cr_and_lf_apart() {
        let tmp = tempfile::tempdir().unwrap();
        let cases: [(&[u8], Content); 5] = [
            (b"a\nb\n", Content::Lf),
            (b"", Content::Lf),
            (b"a\r\nb\r\n", Content::HasCr),
            (b"a\rb", Content::HasCr),
            (b"\r\n\0", Content::Binary),
        ];
        for (i, (bytes, want)) in cases.into_iter().enumerate() {
            let p = tmp.path().join(format!("f{i}"));
            fs::write(&p, bytes).unwrap();
            assert_eq!(content(&p).unwrap(), want, "{bytes:?}");
        }
    }
}
