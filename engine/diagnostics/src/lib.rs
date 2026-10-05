//! 診斷的唯一出口（03 訊息）。
//!
//! 引擎要印診斷只能經過這裡：訊息只能取自 `messages` 產生的常數，
//! 所以不會出現訊息表以外的原因代碼；第一行格式、續行與結束碼也只寫在這裡。

use std::io::{self, Write};

pub use messages::{Level, Message};

/// 診斷第一行的前綴名稱。
const NAME: &str = "vendor_kit";

/// 一條待印的診斷：訊息表的一列，加上要換進占位符的值。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Diagnostic {
    message: &'static Message,
    args: Vec<(&'static str, String)>,
}

impl Diagnostic {
    pub fn new(message: &'static Message) -> Self {
        Self {
            message,
            args: Vec::new(),
        }
    }

    /// 把本文的 `<name>` 換成 `value`；沒給值的占位符原樣印出
    /// （訊息表有些占位符就是要原樣印給使用者代換）。
    pub fn arg(mut self, name: &'static str, value: impl Into<String>) -> Self {
        self.args.push((name, value.into()));
        self
    }

    pub fn message(&self) -> &'static Message {
        self.message
    }

    /// 換好占位符的本文，不含前綴；多行時以 `\n` 分隔。
    pub fn body(&self) -> String {
        let mut text = self.message.text.to_owned();
        for (name, value) in &self.args {
            text = text.replace(&format!("<{name}>"), value);
        }
        text
    }

    /// 印到 stderr 的完整文字：第一行加 `vendor_kit: <level>[VKnnnn]: `，續行原樣，以換行結尾。
    pub fn render(&self) -> String {
        format!(
            "{NAME}: {}[{}]: {}\n",
            self.message.level.as_str(),
            self.message.code,
            self.body()
        )
    }
}

/// 一次執行的診斷出口：把診斷寫到 stderr，並記住整次的結束碼。
///
/// 結束碼取所有診斷裡最大的那個；沒有診斷時為 `0`（03 結束碼）。
pub struct Diagnostics<W: Write> {
    stderr: W,
    exit_code: u8,
}

impl<W: Write> Diagnostics<W> {
    pub fn new(stderr: W) -> Self {
        Self {
            stderr,
            exit_code: 0,
        }
    }

    pub fn emit(&mut self, diagnostic: &Diagnostic) -> io::Result<()> {
        self.exit_code = self.exit_code.max(diagnostic.message.exit_code());
        self.stderr.write_all(diagnostic.render().as_bytes())
    }

    pub fn exit_code(&self) -> u8 {
        self.exit_code
    }

    pub fn into_inner(self) -> W {
        self.stderr
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;
    use messages::{VK0014, VK0024, VK0026, VK0061};

    #[test]
    fn first_line_has_fixed_prefix() {
        assert_eq!(
            Diagnostic::new(&VK0024).render(),
            "vendor_kit: error[VK0024]: No command was specified.\n"
        );
    }

    #[test]
    fn placeholders_are_filled() {
        let d = Diagnostic::new(&VK0026).arg("value", "--bogus");
        assert_eq!(
            d.render(),
            "vendor_kit: error[VK0026]: Unknown, extra, or disallowed argument: --bogus.\n"
        );
    }

    #[test]
    fn continuation_lines_are_printed_as_is() {
        let d = Diagnostic::new(&VK0061)
            .arg("file", "a")
            .arg("text", "t")
            .arg("line_numbers", "none");
        let out = d.render();
        let lines: Vec<&str> = out.lines().collect();
        assert_eq!(lines.len(), 3);
        assert!(lines[0].starts_with("vendor_kit: warn[VK0061]: Cannot reclaim"));
        assert_eq!(lines[1], "Original text: t");
        assert_eq!(lines[2], "Currently matching line numbers: none.");
    }

    #[test]
    fn exit_code_is_the_maximum() {
        let mut d = Diagnostics::new(Vec::new());
        assert_eq!(d.exit_code(), 0);
        d.emit(&Diagnostic::new(&VK0024)).unwrap();
        d.emit(&Diagnostic::new(&VK0014).arg("repo", "a")).unwrap();
        assert_eq!(d.exit_code(), 2);
        let text = String::from_utf8(d.into_inner()).unwrap();
        assert_eq!(text.lines().count(), 2);
    }
}
