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

    /// 給過值的占位符，依 [`Diagnostic::arg`] 的呼叫順序。
    pub fn args(&self) -> &[(&'static str, String)] {
        &self.args
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

/// 診斷的另一個出口：每印一條診斷就交給它一次（ADR-0005：每條帶原因代碼的 stderr 診斷
/// 恰好寫一筆 `diagnostic_emitted`）。執行紀錄由 `runlog` 實作；這裡不知道紀錄的格式。
pub trait Sink {
    fn record(&mut self, diagnostic: &Diagnostic) -> io::Result<()>;
}

/// 沒有執行紀錄時的 sink：什麼都不做。用在契約明定建紀錄前就拒絕的情況，
/// 以及建不出執行紀錄的那條診斷（ADR-0005 的例外）。
#[derive(Debug, Default, Clone, Copy)]
pub struct NoSink;

impl Sink for NoSink {
    fn record(&mut self, _: &Diagnostic) -> io::Result<()> {
        Ok(())
    }
}

/// 一次執行的診斷出口：把診斷寫到 stderr，並記住整次的結束碼。
///
/// 結束碼取所有診斷裡最大的那個；沒有診斷時為 `0`（03 結束碼）。
pub struct Diagnostics<W: Write, S: Sink = NoSink> {
    stderr: W,
    sink: S,
    exit_code: u8,
}

impl<W: Write> Diagnostics<W> {
    /// 還沒有執行紀錄的出口：只印 stderr。
    pub fn new(stderr: W) -> Self {
        Self::with_sink(stderr, NoSink)
    }
}

impl<W: Write, S: Sink> Diagnostics<W, S> {
    /// 有執行紀錄的出口：每條診斷先交給 `sink`，再印到 stderr。
    pub fn with_sink(stderr: W, sink: S) -> Self {
        Self {
            stderr,
            sink,
            exit_code: 0,
        }
    }

    /// 先記紀錄、再印 stderr：先留紀錄再有輸出（02 不變量：副作用之前先留紀錄）。
    /// 紀錄寫不進去時回錯、不印 stderr，由呼叫端決定怎麼收尾。
    pub fn emit(&mut self, diagnostic: &Diagnostic) -> io::Result<()> {
        self.sink.record(diagnostic)?;
        self.exit_code = self.exit_code.max(diagnostic.message.exit_code());
        self.stderr.write_all(diagnostic.render().as_bytes())
    }

    pub fn exit_code(&self) -> u8 {
        self.exit_code
    }

    pub fn into_inner(self) -> W {
        self.stderr
    }

    /// 拆回 stderr 與 sink。
    pub fn into_parts(self) -> (W, S) {
        (self.stderr, self.sink)
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

    #[derive(Default)]
    struct Recorded(Vec<String>);

    impl Sink for Recorded {
        fn record(&mut self, d: &Diagnostic) -> io::Result<()> {
            self.0.push(d.message().code.to_owned());
            Ok(())
        }
    }

    #[test]
    fn each_emit_reaches_the_sink_exactly_once() {
        let mut d = Diagnostics::with_sink(Vec::new(), Recorded::default());
        d.emit(&Diagnostic::new(&VK0024)).unwrap();
        d.emit(&Diagnostic::new(&VK0014).arg("repo", "a")).unwrap();
        let (stderr, sink) = d.into_parts();
        assert_eq!(sink.0, ["VK0024", "VK0014"]);
        assert_eq!(String::from_utf8(stderr).unwrap().lines().count(), 2);
    }

    struct Broken;

    impl Sink for Broken {
        fn record(&mut self, _: &Diagnostic) -> io::Result<()> {
            Err(io::Error::other("disk full"))
        }
    }

    #[test]
    fn a_failed_record_prints_nothing() {
        let mut d = Diagnostics::with_sink(Vec::new(), Broken);
        assert!(d.emit(&Diagnostic::new(&VK0024)).is_err());
        assert_eq!(d.exit_code(), 0);
        assert!(d.into_inner().is_empty());
    }

    #[test]
    fn args_keep_call_order() {
        let d = Diagnostic::new(&VK0061).arg("file", "a").arg("text", "t");
        assert_eq!(
            d.args(),
            [("file", "a".to_owned()), ("text", "t".to_owned())]
        );
    }
}
