//! 診斷的唯一出口（03 訊息）。
//!
//! 引擎要印診斷只能經過這裡：訊息只能取自 `messages` 產生的常數，
//! 所以不會出現訊息表以外的原因代碼；第一行格式、續行與結束碼也只寫在這裡。

use std::io::{self, Write};

pub use messages::{Level, Message};

/// 診斷第一行的前綴名稱。
const NAME: &str = "vendor_kit";

/// 本文結尾指令可用的指令名（同 `script/doc/check_messages.py` 的 `COMMAND_NAMES`）。
pub const COMMAND_NAMES: [&str; 4] = ["just", "git", "sh", "cd"];

/// 結尾片段是不是指令：整段是單一占位符 `<name>`，或是指令名、一個空白、再接非空白開頭的其餘部分
/// （同 `script/doc/check_messages.py` 的 `COMMAND_TAIL`）。
fn is_command_tail(tail: &str) -> bool {
    if let Some(inner) = tail.strip_prefix('<').and_then(|t| t.strip_suffix('>')) {
        return !inner.is_empty() && !inner.contains(['<', '>']);
    }
    COMMAND_NAMES.iter().any(|name| {
        tail.strip_prefix(name)
            .and_then(|rest| rest.strip_prefix(' '))
            .and_then(|rest| rest.chars().next())
            .is_some_and(|c| !c.is_whitespace())
    })
}

/// docker 原文摘錄的上限（位元組，UTF-8）。
pub const DOCKER_STDERR_MAX: usize = 4096;

/// 一次 docker 呼叫的 stderr 摘錄（N20b）：只寫進執行紀錄，不印到 stderr、不決定結果（03:26）。
///
/// 摘錄是 docker 的原文，不承諾格式，可能含敏感資訊。超過 [`DOCKER_STDERR_MAX`] 時留最後的部分
/// （docker 的錯誤通常在結尾），在 UTF-8 字元邊界切，並記下有截斷。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DockerStderr {
    text: String,
    truncated: bool,
}

impl DockerStderr {
    /// 從一次呼叫的 stderr 位元組截取；不是 UTF-8 的位元組換成 U+FFFD。空的回 `None`（沒有可記的原文）。
    pub fn capture(raw: &[u8]) -> Option<Self> {
        if raw.is_empty() {
            return None;
        }
        let text = String::from_utf8_lossy(raw);
        if text.len() <= DOCKER_STDERR_MAX {
            return Some(Self {
                text: text.into_owned(),
                truncated: false,
            });
        }
        let mut start = text.len() - DOCKER_STDERR_MAX;
        while !text.is_char_boundary(start) {
            start += 1;
        }
        Some(Self {
            text: text[start..].to_owned(),
            truncated: true,
        })
    }

    /// 摘錄本身，不超過 [`DOCKER_STDERR_MAX`] 位元組、不是空字串。
    pub fn text(&self) -> &str {
        &self.text
    }

    /// 原文是否超過上限而被截掉開頭。
    pub fn truncated(&self) -> bool {
        self.truncated
    }
}

/// 一條待印的診斷：訊息表的一列，加上要換進占位符的值。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Diagnostic {
    message: &'static Message,
    args: Vec<(&'static str, String)>,
    docker_stderr: Option<DockerStderr>,
}

impl Diagnostic {
    pub fn new(message: &'static Message) -> Self {
        Self {
            message,
            args: Vec::new(),
            docker_stderr: None,
        }
    }

    /// 附上造成這條診斷的那一次 docker 呼叫的 stderr 摘錄；只進執行紀錄，[`Diagnostic::render`] 不印。
    pub fn with_docker_stderr(mut self, excerpt: DockerStderr) -> Self {
        self.docker_stderr = Some(excerpt);
        self
    }

    /// 附上的 docker 原文摘錄。
    pub fn docker_stderr(&self) -> Option<&DockerStderr> {
        self.docker_stderr.as_ref()
    }

    /// 拿掉 docker 原文摘錄的同一條診斷（帶摘錄的紀錄寫不進去時退回用）。
    pub fn without_docker_stderr(&self) -> Self {
        Self {
            docker_stderr: None,
            ..self.clone()
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
        self.fill(self.message.text)
    }

    /// 本文結尾的下一步指令（03 輸出：下一步指令直接寫在本文句尾），換好占位符；沒有回 `None`。
    ///
    /// 規則與 `script/doc/check_messages.py` 的 `ending_command` 相同，看的是訊息表的本文、不是換好值的
    /// 本文（值裡可能有「: 」）：最後一行最後一個「: 」之後的片段，是單一占位符，或以
    /// [`COMMAND_NAMES`] 之一加空白再接非空白開頭。執行紀錄把它寫成 `vendor_kit.next_step.command`（#118）。
    pub fn next_step(&self) -> Option<String> {
        let last = self.message.text.rsplit('\n').next()?;
        let (_, tail) = last.rsplit_once(": ")?;
        if !is_command_tail(tail) {
            return None;
        }
        Some(self.fill(tail))
    }

    /// 把 `text` 裡給過值的占位符換掉。
    fn fill(&self, text: &str) -> String {
        let mut text = text.to_owned();
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
    use messages::{VK0002, VK0004, VK0014, VK0024, VK0026, VK0028, VK0034, VK0061, VK0067};

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
    fn next_step_is_the_filled_ending_command() {
        let d = Diagnostic::new(&VK0002).arg("command_with_y", "./bootstrap.sh -y");
        assert_eq!(d.next_step().as_deref(), Some("./bootstrap.sh -y"));
        // 沒給值的占位符原樣留著，跟本文一致
        assert_eq!(
            Diagnostic::new(&VK0002).next_step().as_deref(),
            Some("<command_with_y>")
        );
        let d = Diagnostic::new(&VK0004).arg("repo", "ghcr.io/a/b");
        assert_eq!(
            d.next_step().as_deref(),
            Some("just vendor_kit add ghcr.io/a/b")
        );
        // 多行訊息看最後一行
        let d = Diagnostic::new(&VK0034)
            .arg("download_url", "u")
            .arg("install_command", "i");
        assert_eq!(d.next_step().as_deref(), Some("i"));
    }

    #[test]
    fn next_step_comes_from_the_template_not_the_filled_body() {
        // 值裡的「: 」不會被當成指令的開頭
        let d = Diagnostic::new(&VK0028).arg("install_dir", "/a: b");
        assert_eq!(d.next_step().as_deref(), Some("cd /a: b"));
        assert!(d.body().ends_with(": cd /a: b"));
    }

    #[test]
    fn diagnostics_without_an_ending_command_have_no_next_step() {
        // 沒有「: 」
        assert_eq!(Diagnostic::new(&VK0024).next_step(), None);
        // 多行訊息的最後一行「: 」之後是占位符加句點，不是指令
        assert_eq!(Diagnostic::new(&VK0067).next_step(), None);
        assert_eq!(Diagnostic::new(&VK0061).next_step(), None);
    }

    #[test]
    fn every_pending_message_has_a_next_step_and_it_ends_the_body() {
        for m in messages::ALL {
            let d = Diagnostic::new(m);
            if m.disposition == Some(messages::Disposition::Pending) {
                assert!(d.next_step().is_some(), "{} has no ending command", m.code);
            }
            if let Some(command) = d.next_step() {
                assert!(d.body().ends_with(&command), "{}", m.code);
            }
        }
    }

    #[test]
    fn command_tail_rule() {
        for ok in ["<x>", "just vendor_kit sync", "git a", "sh x", "cd /"] {
            assert!(is_command_tail(ok), "{ok}");
        }
        for bad in [
            "", "<>", "<a<b>", "<a> b", "just", "just ", "just  x", "justx", "Run x", "make x",
        ] {
            assert!(!is_command_tail(bad), "{bad}");
        }
    }

    #[test]
    fn args_keep_call_order() {
        let d = Diagnostic::new(&VK0061).arg("file", "a").arg("text", "t");
        assert_eq!(
            d.args(),
            [("file", "a".to_owned()), ("text", "t".to_owned())]
        );
    }

    #[test]
    fn docker_stderr_keeps_short_text() {
        assert_eq!(DockerStderr::capture(b""), None);
        let e = DockerStderr::capture(b"Error response from daemon: denied\n").unwrap();
        assert_eq!(e.text(), "Error response from daemon: denied\n");
        assert!(!e.truncated());
        let full = vec![b'a'; DOCKER_STDERR_MAX];
        let e = DockerStderr::capture(&full).unwrap();
        assert_eq!(e.text().len(), DOCKER_STDERR_MAX);
        assert!(!e.truncated());
    }

    #[test]
    fn docker_stderr_keeps_the_tail_on_a_char_boundary() {
        // 「中」是 3 位元組：上限 +1 個位元組時，切點落在字元中間，要往後挪到下一個邊界。
        let mut raw = "中".repeat(DOCKER_STDERR_MAX / 3 + 1).into_bytes();
        raw.extend_from_slice(b"end");
        let e = DockerStderr::capture(&raw).unwrap();
        assert!(e.truncated());
        assert!(e.text().len() <= DOCKER_STDERR_MAX);
        assert!(e.text().ends_with("中end"));
        assert!(e.text().starts_with('中'));
    }

    #[test]
    fn docker_stderr_replaces_invalid_utf8() {
        let e = DockerStderr::capture(b"bad \xff byte").unwrap();
        assert_eq!(e.text(), "bad \u{fffd} byte");
    }

    #[test]
    fn docker_stderr_is_not_rendered() {
        let plain = Diagnostic::new(&VK0024);
        let d = plain
            .clone()
            .with_docker_stderr(DockerStderr::capture(b"secret").unwrap());
        assert_eq!(d.render(), plain.render());
        assert_eq!(d.docker_stderr().unwrap().text(), "secret");
        assert_eq!(d.without_docker_stderr(), plain);
    }
}
