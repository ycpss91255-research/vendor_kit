//! 訊息產生器：讀訊息表 `doc/contract/reason_codes.csv`，產出
//!
//! - `engine/messages/src/generated.rs`：引擎用的常數，進 git；
//! - 主機端 bash（`bootstrap.sh`、啟動器 `launcher/`）用的片段：只寫到建置輸出目錄，不進 git。
//!
//! 另外檢查組好的 `bootstrap.sh`（`--embedded`）：內嵌的片段跟訊息表一致，從入口走得到的代碼都是
//! source 含 bootstrap 的 active 代碼（見 [`embedded`]）。
//!
//! 輸出只由 CSV 內容決定：依代碼排序、不讀時間與環境（ADR-0012）。
//! 不用 build.rs：產生是明確的一步，`--check` 讓漏跑在建置時就紅。
//!
//! 用法：
//!
//! ```text
//! msggen --csv <reason_codes.csv> --rust <generated.rs> [--check] [--bash-out <file>] [--embedded <bootstrap.sh>]
//! ```
//!
//! `--check` 不寫 `--rust`，只比對；不一致時以 1 結束。`--embedded` 檢查不過也以 1 結束。

mod embedded;
mod render;
mod table;

use std::ffi::OsString;
use std::path::PathBuf;
use std::process::ExitCode;

struct Args {
    csv: PathBuf,
    rust: PathBuf,
    check: bool,
    bash_out: Option<PathBuf>,
    embedded: Option<PathBuf>,
}

fn parse_args(raw: impl IntoIterator<Item = OsString>) -> Result<Args, String> {
    let mut csv = None;
    let mut rust = None;
    let mut check = false;
    let mut bash_out = None;
    let mut embedded = None;
    let mut it = raw.into_iter();
    while let Some(arg) = it.next() {
        match arg.to_str() {
            Some("--csv") => csv = it.next().map(PathBuf::from),
            Some("--rust") => rust = it.next().map(PathBuf::from),
            Some("--bash-out") => bash_out = it.next().map(PathBuf::from),
            Some("--embedded") => embedded = it.next().map(PathBuf::from),
            Some("--check") => check = true,
            _ => return Err(format!("unknown argument: {}", arg.to_string_lossy())),
        }
    }
    Ok(Args {
        csv: csv.ok_or("missing --csv <path>")?,
        rust: rust.ok_or("missing --rust <path>")?,
        check,
        bash_out,
        embedded,
    })
}

fn run(args: &Args) -> Result<(), String> {
    let bytes =
        std::fs::read(&args.csv).map_err(|e| format!("cannot read {}: {e}", args.csv.display()))?;
    let rows = table::parse(&bytes)?;
    let rust = render::rust(&rows);
    if args.check {
        let current = std::fs::read_to_string(&args.rust)
            .map_err(|e| format!("cannot read {}: {e}", args.rust.display()))?;
        if current != rust {
            return Err(format!(
                "{} is out of date with {}; rerun msggen without --check",
                args.rust.display(),
                args.csv.display()
            ));
        }
    } else {
        std::fs::write(&args.rust, &rust)
            .map_err(|e| format!("cannot write {}: {e}", args.rust.display()))?;
    }
    if let Some(path) = &args.bash_out {
        if let Some(dir) = path.parent().filter(|d| !d.as_os_str().is_empty()) {
            std::fs::create_dir_all(dir)
                .map_err(|e| format!("cannot create {}: {e}", dir.display()))?;
        }
        std::fs::write(path, render::bash(&rows))
            .map_err(|e| format!("cannot write {}: {e}", path.display()))?;
    }
    if let Some(path) = &args.embedded {
        let script = std::fs::read_to_string(path)
            .map_err(|e| format!("cannot read {}: {e}", path.display()))?;
        embedded::check(&script, &rows).map_err(|e| format!("{}:\n{e}", path.display()))?;
    }
    Ok(())
}

fn main() -> ExitCode {
    match parse_args(std::env::args_os().skip(1)).and_then(|a| run(&a)) {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => {
            eprintln!("msggen: {e}");
            ExitCode::FAILURE
        }
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;
    use std::path::Path;

    fn repo_root() -> PathBuf {
        Path::new(env!("CARGO_MANIFEST_DIR")).join("../..")
    }

    /// 產物進 git，所以改了 CSV 忘了重跑 msggen 要在這裡紅。
    #[test]
    fn committed_rust_matches_csv() {
        let root = repo_root();
        let bytes = std::fs::read(root.join("doc/contract/reason_codes.csv")).unwrap();
        let rows = table::parse(&bytes).unwrap();
        let committed =
            std::fs::read_to_string(root.join("engine/messages/src/generated.rs")).unwrap();
        assert!(
            committed == render::rust(&rows),
            "engine/messages/src/generated.rs is out of date; run: cargo run -p msggen -- --csv doc/contract/reason_codes.csv --rust engine/messages/src/generated.rs"
        );
    }

    #[test]
    fn parse_args_requires_paths() {
        assert!(parse_args(Vec::<OsString>::new()).is_err());
        let a = parse_args(["--csv", "a", "--rust", "b", "--check"].map(OsString::from)).unwrap();
        assert!(a.check);
        assert!(a.bash_out.is_none());
        assert!(a.embedded.is_none());
        let a = parse_args(["--csv", "a", "--rust", "b", "--embedded", "c"].map(OsString::from))
            .unwrap();
        assert_eq!(a.embedded, Some(PathBuf::from("c")));
    }
}
