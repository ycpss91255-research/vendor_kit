//! 非診斷的輸出（03 輸出）。
//!
//! stdout 只放正常結果與 `-h`／`--help` 的用法；stderr 上不是診斷的字句
//! （不帶指令時的版本行、用法錯誤後附的簡短用法）也從這裡印，不加前綴。
//! 診斷一律走 `diagnostics`，不經過這裡。各指令的用法文字在 [`Help`]。
//!
//! v1 不上色（#372 N72）：03 只定了要上色時的規則，沒要求一定上色；這裡印的字句與診斷都不帶顏色，
//! 啟動器傳來的 `--no-color` 收下不用。之後要上色另開 issue。

mod help;

use std::io::{self, Write};

pub use help::Help;

/// 版本行與用法裡的名稱。
const NAME: &str = "vendor_kit";

/// 用法錯誤後附在 stderr 的簡短用法（03 輸出、04 命名空間）。
pub const SHORT_USAGE: &str = "Usage: just vendor_kit <cmd> [arguments] [options]";

/// 不帶指令時第一行的版本行：`vendor_kit <version>`。
pub fn version_line(version: &str) -> String {
    format!("{NAME} {version}")
}

/// 一次執行的正常輸出。
pub struct Output<O: Write, E: Write> {
    stdout: O,
    stderr: E,
}

impl<O: Write, E: Write> Output<O, E> {
    pub fn new(stdout: O, stderr: E) -> Self {
        Self { stdout, stderr }
    }

    /// stdout 的一行正常結果。
    pub fn result_line(&mut self, line: &str) -> io::Result<()> {
        writeln!(self.stdout, "{line}")
    }

    /// `-h`／`--help` 的用法全文，印到 stdout。
    pub fn help(&mut self, help: Help) -> io::Result<()> {
        self.stdout.write_all(help.text().as_bytes())
    }

    /// stderr 上不是診斷的一行（版本行、簡短用法）。
    pub fn stderr_line(&mut self, line: &str) -> io::Result<()> {
        writeln!(self.stderr, "{line}")
    }

    pub fn flush(&mut self) -> io::Result<()> {
        self.stdout.flush()?;
        self.stderr.flush()
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    #[test]
    fn version_line_has_no_prefix() {
        assert_eq!(version_line("v1.4.0"), "vendor_kit v1.4.0");
    }

    #[test]
    fn lines_go_to_their_streams() {
        let mut out = Output::new(Vec::new(), Vec::new());
        out.result_line("a current: v1.0.0 latest: v1.0.0").unwrap();
        out.stderr_line(SHORT_USAGE).unwrap();
        let Output { stdout, stderr } = out;
        assert_eq!(stdout, b"a current: v1.0.0 latest: v1.0.0\n");
        assert_eq!(
            stderr,
            b"Usage: just vendor_kit <cmd> [arguments] [options]\n"
        );
    }

    #[test]
    fn help_goes_to_stdout_only() {
        let mut out = Output::new(Vec::new(), Vec::new());
        out.help(Help::Sync).unwrap();
        let Output { stdout, stderr } = out;
        assert_eq!(stdout, Help::Sync.text().as_bytes());
        assert!(stderr.is_empty());
    }

    #[test]
    fn every_help_has_the_same_shape() {
        for help in Help::ALL {
            let text = help.text();
            let lines: Vec<&str> = text.lines().collect();
            assert!(lines[0].starts_with("Usage: just vendor_kit "), "{help:?}");
            assert!(text.ends_with('\n') && !text.ends_with("\n\n"), "{help:?}");
            assert!(lines.contains(&"Options:"), "{help:?}");
            assert!(
                lines.iter().any(|l| l.starts_with("  -h, --help ")),
                "{help:?}"
            );
            // 不加前綴、不上色、純 ASCII、行尾沒有空白。
            assert!(!text.contains("vendor_kit:"), "{help:?}");
            assert!(text.is_ascii() && !text.contains('\x1b'), "{help:?}");
            assert!(lines.iter().all(|l| l.trim_end() == *l), "{help:?}");
        }
        let mut seen = std::collections::HashSet::new();
        assert!(Help::ALL.iter().all(|h| seen.insert(h.text())));
    }
}
