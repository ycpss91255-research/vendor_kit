//! 基準版合併：升級初始檔時，拿上次套用的基準版全文當共同祖先，與目前 repo 檔、新版初始檔做逐檔
//! 三方合併（ADR-0003）。
//!
//! - 機制是 `git merge-file -p --diff3`：結果只從 stdout 收回，git 不改任何輸入檔；結果寫到哪裡、
//!   什麼時候寫，由呼叫端決定。git 從 `PATH` 找（引擎 image 帶 git，ADR-0014）。
//! - 衝突標記用 `-L` 標上 [`CURRENT_LABEL`]、[`BASELINE_LABEL`]、[`NEW_LABEL`]。git 把第一個標籤
//!   （目前檔）放在 `<<<<<<<` 那行、第二個（基準版）放在 `|||||||`、第三個（新版）放在 `>>>>>>>`。
//!   scope_roadmap:32 定的標記是 `<<<<<<< vendor_kit:baseline`，所以三個標籤都以 `vendor_kit:baseline`
//!   開頭：`<<<<<<<` 那行是 `<<<<<<< vendor_kit:baseline current`，以 [`CONFLICT_MARKER`] 開頭，
//!   後面接哪一邊的名稱，讓使用者看得出這段是誰的內容。
//! - 行尾（ADR-0012）：三份輸入先把 CRLF 正規化成 LF 再合併，只差行尾不算衝突。只處理緊接 `\n`
//!   的 `\r`，單獨的 `\r` 照原樣（同 `files::fingerprint_normalized`）。結果的行尾跟著目前檔：
//!   目前檔的 CRLF 行多於單獨 LF 的行，結果每個 `\n` 都寫成 `\r\n`（衝突標記行也是）；否則結果用 LF。
//!   混用行尾的檔取多數、平手用 LF，所以少數那種行尾的行會被統一，這是混用檔唯一會改行尾的情形。
//! - git 的原生結束狀態不直接當結束碼（ADR-0003），在這裡映射成三種：`0` 是乾淨合併
//!   （[`Outcome::Clean`]）；`1..=127` 是衝突數（git 超過 127 個衝突也回 127），回
//!   [`Outcome::Conflicts`]，對應 VK0021（warn，結束碼 `1`）；其他狀態（git 出錯時是負值，例如
//!   二進位檔）、被訊號終止、叫不起 git 都回 [`Error`]。
//! - git 的設定不影響結果：不讀系統與使用者的 git 設定，也不在任何 repo 裡執行。
//!
//! scope_roadmap:32 的例外（合併結果是 TOML／just 而解析不過時留原檔、該檔基準版不推、記入 metadata
//! `conflicts`）由呼叫端判斷；這裡不解析合併結果，也不決定基準版推不推。
//!
//! 這裡不印診斷；要怎麼印由呼叫端經 `diagnostics` 決定，`<file>` 等欄位也由呼叫端填。

use std::ffi::OsStr;
use std::fmt;
use std::fs;
use std::io;
use std::process::{Command, Stdio};

use messages::Message;

/// 目前 repo 檔那一邊的標籤，在 `<<<<<<<` 那行。
pub const CURRENT_LABEL: &str = "vendor_kit:baseline current";
/// 基準版（共同祖先）的標籤，在 `|||||||` 那行。
pub const BASELINE_LABEL: &str = "vendor_kit:baseline";
/// 新版初始檔那一邊的標籤，在 `>>>>>>>` 那行。
pub const NEW_LABEL: &str = "vendor_kit:baseline new";
/// 合併留下衝突時，衝突開頭那行以這段開頭（scope_roadmap:32）。
pub const CONFLICT_MARKER: &str = "<<<<<<< vendor_kit:baseline";

/// 預設呼叫的 git。
const GIT: &str = "git";

/// 三方合併的三份輸入，都是原樣內容。
#[derive(Debug, Clone, Copy)]
pub struct Inputs<'a> {
    /// 上次套用的基準版全文（共同祖先）。
    pub baseline: &'a [u8],
    /// 目前 repo 裡的檔。
    pub current: &'a [u8],
    /// 新版初始檔。
    pub new: &'a [u8],
}

/// 合併結果。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Outcome {
    /// 乾淨合併。
    Clean(Vec<u8>),
    /// 合併留下衝突標記；`count` 是衝突段數（git 最多回報 127）。
    Conflicts { contents: Vec<u8>, count: u32 },
}

impl Outcome {
    /// 合併後的內容，行尾已依目前檔還原。
    pub fn contents(&self) -> &[u8] {
        match self {
            Outcome::Clean(c) => c,
            Outcome::Conflicts { contents, .. } => contents,
        }
    }

    pub fn into_contents(self) -> Vec<u8> {
        match self {
            Outcome::Clean(c) => c,
            Outcome::Conflicts { contents, .. } => contents,
        }
    }

    pub fn is_clean(&self) -> bool {
        matches!(self, Outcome::Clean(_))
    }

    /// 對應的訊息表條目：有衝突是 VK0021；乾淨合併回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            Outcome::Clean(_) => None,
            Outcome::Conflicts { .. } => Some(&messages::VK0021),
        }
    }
}

/// 合併沒有完成。
#[derive(Debug)]
pub enum Error {
    /// 建暫存目錄、寫暫存檔或刪暫存目錄失敗。
    Temp(io::Error),
    /// 叫不起 git。
    Spawn(io::Error),
    /// git 以衝突數以外的狀態結束；`status` 是 `None` 時是被訊號終止。`stderr` 是 git 的原文。
    Git { status: Option<i32>, stderr: String },
}

impl Error {
    /// 對應的訊息表條目：合併出錯還沒有代碼，回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        None
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Temp(e) => write!(f, "merge temporary files: {e}"),
            Error::Spawn(e) => write!(f, "cannot run git merge-file: {e}"),
            Error::Git {
                status: Some(code),
                stderr,
            } => write!(
                f,
                "git merge-file exited with {code}: {}",
                stderr.trim_end()
            ),
            Error::Git {
                status: None,
                stderr,
            } => write!(
                f,
                "git merge-file was terminated by a signal: {}",
                stderr.trim_end()
            ),
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Error::Temp(e) | Error::Spawn(e) => Some(e),
            Error::Git { .. } => None,
        }
    }
}

/// 用 `PATH` 上的 git 做三方合併。
pub fn merge(inputs: &Inputs<'_>) -> Result<Outcome, Error> {
    merge_with(OsStr::new(GIT), inputs)
}

/// 用指定的 git 執行檔做三方合併。
pub fn merge_with(git: &OsStr, inputs: &Inputs<'_>) -> Result<Outcome, Error> {
    let crlf = uses_crlf(inputs.current);
    let dir = tempfile::Builder::new()
        .prefix("vendor_kit-merge-")
        .tempdir()
        .map_err(Error::Temp)?;
    let current = dir.path().join("current");
    let baseline = dir.path().join("baseline");
    let new = dir.path().join("new");
    for (path, contents) in [
        (&current, inputs.current),
        (&baseline, inputs.baseline),
        (&new, inputs.new),
    ] {
        fs::write(path, to_lf(contents)).map_err(Error::Temp)?;
    }

    let output = Command::new(git)
        .args(["merge-file", "-p", "--diff3"])
        .args(["-L", CURRENT_LABEL, "-L", BASELINE_LABEL, "-L", NEW_LABEL])
        .arg(&current)
        .arg(&baseline)
        .arg(&new)
        .current_dir(dir.path())
        .env("GIT_CONFIG_NOSYSTEM", "1")
        .env("GIT_CONFIG_GLOBAL", "/dev/null")
        .env_remove("GIT_DIR")
        .env_remove("GIT_WORK_TREE")
        .env_remove("GIT_CONFIG")
        .env_remove("GIT_CONFIG_PARAMETERS")
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output()
        .map_err(Error::Spawn)?;
    // 暫存目錄的刪除錯誤由這裡回傳，不靠 Drop（ADR-0014）。
    dir.close().map_err(Error::Temp)?;

    let contents = if crlf {
        to_crlf(&output.stdout)
    } else {
        output.stdout
    };
    match output.status.code() {
        Some(0) => Ok(Outcome::Clean(contents)),
        Some(n @ 1..=127) => Ok(Outcome::Conflicts {
            contents,
            count: n.unsigned_abs(),
        }),
        status => Err(Error::Git {
            status,
            stderr: String::from_utf8_lossy(&output.stderr).into_owned(),
        }),
    }
}

/// CRLF 行多於單獨 LF 的行。
fn uses_crlf(contents: &[u8]) -> bool {
    let mut crlf = 0usize;
    let mut lf = 0usize;
    for (i, &b) in contents.iter().enumerate() {
        if b == b'\n' {
            if i > 0 && contents[i - 1] == b'\r' {
                crlf += 1;
            } else {
                lf += 1;
            }
        }
    }
    crlf > lf
}

/// 把緊接 `\n` 的 `\r` 拿掉；單獨的 `\r` 照原樣。
fn to_lf(contents: &[u8]) -> Vec<u8> {
    let mut out = Vec::with_capacity(contents.len());
    for (i, &b) in contents.iter().enumerate() {
        if b == b'\r' && contents.get(i + 1) == Some(&b'\n') {
            continue;
        }
        out.push(b);
    }
    out
}

/// 每個 `\n` 寫成 `\r\n`，是 [`to_lf`] 的反向。
fn to_crlf(contents: &[u8]) -> Vec<u8> {
    let mut out = Vec::with_capacity(contents.len() + contents.len() / 16);
    for &b in contents {
        if b == b'\n' {
            out.push(b'\r');
        }
        out.push(b);
    }
    out
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    fn run(baseline: &str, current: &str, new: &str) -> Outcome {
        merge(&Inputs {
            baseline: baseline.as_bytes(),
            current: current.as_bytes(),
            new: new.as_bytes(),
        })
        .unwrap()
    }

    fn text(outcome: &Outcome) -> &str {
        std::str::from_utf8(outcome.contents()).unwrap()
    }

    #[test]
    fn clean_merge_keeps_both_sides() {
        let out = run("a\nb\nc\nd\ne\n", "A\nb\nc\nd\ne\n", "a\nb\nc\nd\nE\n");
        assert!(out.is_clean());
        assert_eq!(text(&out), "A\nb\nc\nd\nE\n");
        assert_eq!(out.message(), None);
    }

    #[test]
    fn identical_inputs_merge_clean_and_unchanged() {
        let out = run("a\n", "a\n", "a\n");
        assert_eq!(out, Outcome::Clean(b"a\n".to_vec()));
    }

    #[test]
    fn conflict_leaves_vendor_kit_markers() {
        let out = run("a\nb\nc\n", "a\nX\nc\n", "a\nY\nc\n");
        assert_eq!(
            text(&out),
            "a\n\
             <<<<<<< vendor_kit:baseline current\n\
             X\n\
             ||||||| vendor_kit:baseline\n\
             b\n\
             =======\n\
             Y\n\
             >>>>>>> vendor_kit:baseline new\n\
             c\n"
        );
        assert!(matches!(out, Outcome::Conflicts { count: 1, .. }));
        assert_eq!(out.message().map(|m| m.code), Some("VK0021"));
        assert!(text(&out).lines().any(|l| l.starts_with(CONFLICT_MARKER)));
    }

    #[test]
    fn conflict_count_is_reported() {
        let out = run(
            "a\n1\n2\n3\n4\n5\nb\n",
            "X\n1\n2\n3\n4\n5\nZ\n",
            "Y\n1\n2\n3\n4\n5\nW\n",
        );
        assert!(matches!(out, Outcome::Conflicts { count: 2, .. }));
    }

    #[test]
    fn crlf_current_merges_with_lf_files_and_stays_crlf() {
        let out = run(
            "a\nb\nc\nd\ne\n",
            "A\r\nb\r\nc\r\nd\r\ne\r\n",
            "a\nb\nc\nd\nE\n",
        );
        assert!(out.is_clean(), "{:?}", text(&out));
        assert_eq!(text(&out), "A\r\nb\r\nc\r\nd\r\nE\r\n");
    }

    #[test]
    fn line_ending_only_changes_are_not_conflicts() {
        // 基準版與新版只差行尾：結果就是目前檔，行尾不變。
        let out = run("a\r\nb\r\nc\r\n", "a\nB\nc\n", "a\nb\nc\n");
        assert_eq!(out, Outcome::Clean(b"a\nB\nc\n".to_vec()));
        // 目前檔只改行尾、新版改了內容：取新版內容，行尾跟目前檔。
        let out = run("a\nb\nc\n", "a\r\nb\r\nc\r\n", "a\nB\nc\n");
        assert_eq!(out, Outcome::Clean(b"a\r\nB\r\nc\r\n".to_vec()));
    }

    #[test]
    fn crlf_conflict_markers_use_crlf() {
        let out = run("a\nb\nc\n", "a\r\nX\r\nc\r\n", "a\nY\nc\n");
        assert!(matches!(out, Outcome::Conflicts { count: 1, .. }));
        let t = text(&out);
        assert!(
            t.contains("<<<<<<< vendor_kit:baseline current\r\n"),
            "{t:?}"
        );
        assert!(!t.replace("\r\n", "").contains('\n'), "{t:?}");
    }

    #[test]
    fn lone_cr_is_kept() {
        let out = run("a\rb\nc\n", "a\rb\nc\n", "a\rb\nC\n");
        assert_eq!(out, Outcome::Clean(b"a\rb\nC\n".to_vec()));
    }

    #[test]
    fn mixed_line_endings_follow_the_majority() {
        assert!(uses_crlf(b"a\r\nb\r\nc\n"));
        assert!(!uses_crlf(b"a\r\nb\nc\n"));
        assert!(!uses_crlf(b"a\r\nb\n"));
        assert!(!uses_crlf(b"no newline"));
        assert!(uses_crlf(b"\r\n"));
    }

    #[test]
    fn binary_input_is_an_error() {
        let err = merge(&Inputs {
            baseline: b"a\0b\n",
            current: b"a\0c\n",
            new: b"a\0d\n",
        })
        .unwrap_err();
        assert!(
            matches!(&err, Error::Git { status: Some(s), .. } if !(0..=127).contains(s)),
            "{err:?}"
        );
        assert_eq!(err.message(), None);
    }

    #[test]
    fn missing_git_is_a_spawn_error() {
        let err = merge_with(
            OsStr::new("vendor_kit-no-such-git"),
            &Inputs {
                baseline: b"a\n",
                current: b"a\n",
                new: b"a\n",
            },
        )
        .unwrap_err();
        assert!(matches!(err, Error::Spawn(_)), "{err:?}");
    }

    #[test]
    fn line_ending_conversions_round_trip() {
        assert_eq!(to_lf(b"a\r\nb\rc\r\r\n"), b"a\nb\rc\r\n");
        assert_eq!(to_crlf(b"a\nb\rc\r\n"), b"a\r\nb\rc\r\r\n");
    }
}
