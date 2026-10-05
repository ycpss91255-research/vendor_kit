//! 執行紀錄 JSONL（ADR-0005）：事件註冊表、引擎端的寫入、診斷的 sink，與未完成首次導入的判定。
//!
//! - 一行一筆、LF 結尾、UTF-8；鍵序與空白固定（[`json`] 的正規形），所以同一筆事件只有一種寫法，
//!   不帶 JSON 解析器的讀取端也能逐行比對（ADR-0007:30–31）。
//! - 欄位骨架照 #118／#114，依序是 `timestamp`（UTC、六位小數、`Z`）、`severity_text`、
//!   `severity_number`、`event_name`、`body`（英文，03 輸出）、`resource`（`service.name`、
//!   `service.version`）、`attributes`。`attributes` 依序先放 `vendor_kit.log_format`、
//!   `vendor_kit.component`、`vendor_kit.invocation_id`，再放各事件自己的欄位（見 [`Event`]）。
//! - 事件名只能取自註冊表 `log-events.txt`（真本在這個 crate，隨引擎 image 出貨）。寫紀錄前查表，
//!   未登錄就回 [`Error::Unregistered`]，呼叫端以 VK0056 停下（ADR-0005:26）。
//! - 判定 [`assess`] 會讀的 attribute 值（mode、target、stop_reason_code）都是封閉列舉，
//!   寫與讀共用同一份型別，拼錯就讀不進來。
//! - 未完成首次導入用里程碑事件判定（#372 定案）：寫入前先記意圖（`writes_started`、
//!   `lock_line_write_started`），寫成功再記結果（`lock_line_written`）。
//!
//! 紀錄檔的命名、建立與「最近一筆」的挑選由啟動器做（ADR-0005:7、ADR-0007），不在這裡；
//! 引擎只接著啟動器建好的檔往後寫（[`open_append`]）。

mod json;
mod read;
mod time;

use std::fmt;
use std::fs::{File, OpenOptions};
use std::io::{self, Write};
use std::path::Path;
use std::time::SystemTime;

use diagnostics::{Diagnostic, Level, Sink};
use messages::Message;

pub use read::{Condition, Reason, Verdict, assess};

/// 執行紀錄格式版本：每行 `attributes` 的第一個鍵 `vendor_kit.log_format` 的值。
/// 讀取端只認這個版本，不符就不拿來判定。
pub const LOG_FORMAT: &str = "1";

/// `resource."service.name"` 的值。
pub const SERVICE_NAME: &str = "vendor_kit";

/// 事件註冊表真本（ADR-0005:26）：一行一個事件名，`#` 開頭與空行不算。
pub const REGISTRY_SOURCE: &str = include_str!("../log-events.txt");

/// 註冊表裡的事件名，依檔內順序。
pub fn registry() -> impl Iterator<Item = &'static str> {
    REGISTRY_SOURCE
        .lines()
        .map(str::trim)
        .filter(|l| !l.is_empty() && !l.starts_with('#'))
}

/// 事件名在不在註冊表裡。
pub fn is_registered(name: &str) -> bool {
    registry().any(|n| n == name)
}

/// 寫這筆紀錄的元件（`attributes."vendor_kit.component"`）。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Component {
    Launcher,
    Engine,
}

impl Component {
    pub const ALL: [Component; 2] = [Component::Launcher, Component::Engine];

    pub const fn as_str(self) -> &'static str {
        match self {
            Component::Launcher => "launcher",
            Component::Engine => "engine",
        }
    }

    pub fn parse(s: &str) -> Option<Component> {
        Self::ALL.into_iter().find(|c| c.as_str() == s)
    }
}

/// 這次呼叫的模式（`run_started` 的 `vendor_kit.mode`，ADR-0007:31）。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Mode {
    /// 首次導入（bootstrap.sh 不帶參數、-y、-i）。
    InitialImport,
    /// bootstrap.sh 只檢查。
    Check,
    /// bootstrap.sh --repair。
    Repair,
    /// VK recipe（`just vendor_kit <cmd>`）。
    Recipe,
}

impl Mode {
    pub const ALL: [Mode; 4] = [Mode::InitialImport, Mode::Check, Mode::Repair, Mode::Recipe];

    pub const fn as_str(self) -> &'static str {
        match self {
            Mode::InitialImport => "initial_import",
            Mode::Check => "check",
            Mode::Repair => "repair",
            Mode::Recipe => "recipe",
        }
    }

    pub fn parse(s: &str) -> Option<Mode> {
        Self::ALL.into_iter().find(|m| m.as_str() == s)
    }
}

/// 要寫的版本鎖定行屬於誰（`vendor_kit.target`）。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Target {
    /// 引擎版本鎖定行。
    Engine,
    /// 某個工具的版本鎖定行。
    Tool,
}

impl Target {
    pub const ALL: [Target; 2] = [Target::Engine, Target::Tool];

    pub const fn as_str(self) -> &'static str {
        match self {
            Target::Engine => "engine",
            Target::Tool => "tool",
        }
    }

    pub fn parse(s: &str) -> Option<Target> {
        Self::ALL.into_iter().find(|t| t.as_str() == s)
    }
}

/// `run_finished` 的停下原因（`vendor_kit.stop_reason_code`）：訊息表裡的代碼，或 `none`。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StopReason {
    /// 沒有因診斷停下。
    None,
    /// 因這個代碼停下；同一份紀錄裡必須有同代碼的 `diagnostic_emitted`。
    Code(&'static Message),
}

impl StopReason {
    pub const NONE: &'static str = "none";

    pub fn as_str(self) -> &'static str {
        match self {
            StopReason::None => Self::NONE,
            StopReason::Code(m) => m.code,
        }
    }

    /// 只認 `none` 與訊息表裡使用中的代碼。
    pub fn parse(s: &str) -> Option<StopReason> {
        if s == Self::NONE {
            return Some(StopReason::None);
        }
        find_message(s).map(StopReason::Code)
    }
}

fn find_message(code: &str) -> Option<&'static Message> {
    messages::ALL.iter().find(|m| m.code == code)
}

/// 註冊表裡的事件名。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EventName {
    RunStarted,
    EngineStarted,
    DiagnosticEmitted,
    WritesStarted,
    LockLineWriteStarted,
    LockLineWritten,
    ProgressRemoved,
    EngineFinished,
    RunFinished,
}

impl EventName {
    pub const ALL: [EventName; 9] = [
        EventName::RunStarted,
        EventName::EngineStarted,
        EventName::DiagnosticEmitted,
        EventName::WritesStarted,
        EventName::LockLineWriteStarted,
        EventName::LockLineWritten,
        EventName::ProgressRemoved,
        EventName::EngineFinished,
        EventName::RunFinished,
    ];

    pub const fn as_str(self) -> &'static str {
        match self {
            EventName::RunStarted => "run_started",
            EventName::EngineStarted => "engine_started",
            EventName::DiagnosticEmitted => "diagnostic_emitted",
            EventName::WritesStarted => "writes_started",
            EventName::LockLineWriteStarted => "lock_line_write_started",
            EventName::LockLineWritten => "lock_line_written",
            EventName::ProgressRemoved => "progress_removed",
            EventName::EngineFinished => "engine_finished",
            EventName::RunFinished => "run_finished",
        }
    }

    pub fn parse(s: &str) -> Option<EventName> {
        Self::ALL.into_iter().find(|e| e.as_str() == s)
    }

    /// 可以寫這個事件的元件：`run_started`、`run_finished` 只由啟動器寫，
    /// `diagnostic_emitted` 由實際印出診斷的一端寫，其餘只由引擎寫（ADR-0005:7）。
    pub fn writable_by(self, component: Component) -> bool {
        match self {
            EventName::RunStarted | EventName::RunFinished => component == Component::Launcher,
            EventName::DiagnosticEmitted => true,
            _ => component == Component::Engine,
        }
    }

    /// 診斷以外的事件固定的英文 body；`diagnostic_emitted` 的 body 是換好占位符的診斷本文。
    pub const fn fixed_body(self) -> Option<&'static str> {
        Some(match self {
            EventName::RunStarted => "Run started.",
            EventName::EngineStarted => "Engine started.",
            EventName::DiagnosticEmitted => return None,
            EventName::WritesStarted => "Writes started.",
            EventName::LockLineWriteStarted => "Lock line write started.",
            EventName::LockLineWritten => "Lock line written.",
            EventName::ProgressRemoved => "Progress file removed.",
            EventName::EngineFinished => "Engine finished.",
            EventName::RunFinished => "Run finished.",
        })
    }
}

/// attribute 的鍵。
pub mod key {
    pub const LOG_FORMAT: &str = "vendor_kit.log_format";
    pub const COMPONENT: &str = "vendor_kit.component";
    pub const INVOCATION_ID: &str = "vendor_kit.invocation_id";
    pub const MODE: &str = "vendor_kit.mode";
    pub const ARGV: &str = "vendor_kit.argv";
    pub const REASON_CODE: &str = "vendor_kit.reason_code";
    /// 診斷占位符的鍵是這個前綴加占位符名，例如 `vendor_kit.placeholder.repo`。
    pub const PLACEHOLDER_PREFIX: &str = "vendor_kit.placeholder.";
    pub const TARGET: &str = "vendor_kit.target";
    pub const PROGRESS_FILE: &str = "vendor_kit.progress_file";
    pub const EXIT_CODE: &str = "vendor_kit.exit_code";
    pub const ENGINE_EXIT_CODE: &str = "vendor_kit.engine.exit_code";
    pub const STOP_REASON_CODE: &str = "vendor_kit.stop_reason_code";
}

/// 一筆事件與它自己的 attribute（依列出的順序寫在共同欄位之後）。
#[derive(Debug, Clone, Copy)]
pub enum Event<'a> {
    /// 啟動器建好紀錄後的第一筆：`vendor_kit.mode`、`vendor_kit.argv`（逐項字串）。
    RunStarted { mode: Mode, argv: &'a [String] },
    /// 引擎開始（flow-launch e1）。
    EngineStarted,
    /// 每印一條診斷寫一筆：`vendor_kit.reason_code`，再依序放 `vendor_kit.placeholder.<name>`。
    DiagnosticEmitted(&'a Diagnostic),
    /// 第一筆非紀錄檔寫入（建進度檔，ADR-0004:33）之前。
    WritesStarted,
    /// 寫版本鎖定行之前：`vendor_kit.target`。
    LockLineWriteStarted { target: Target },
    /// 版本鎖定行寫成功之後：`vendor_kit.target`。
    LockLineWritten { target: Target },
    /// 刪進度檔（完成點，ADR-0004:38）之後：`vendor_kit.progress_file`（檔名）。
    ProgressRemoved { file: &'a str },
    /// 引擎結束前：`vendor_kit.exit_code`。
    EngineFinished { exit_code: u8 },
    /// 啟動器收尾：`vendor_kit.exit_code`、`vendor_kit.engine.exit_code`（沒起引擎時為 `null`）、
    /// `vendor_kit.stop_reason_code`。
    RunFinished {
        exit_code: u8,
        engine_exit_code: Option<u8>,
        stop_reason: StopReason,
    },
}

impl Event<'_> {
    pub fn name(&self) -> EventName {
        match self {
            Event::RunStarted { .. } => EventName::RunStarted,
            Event::EngineStarted => EventName::EngineStarted,
            Event::DiagnosticEmitted(_) => EventName::DiagnosticEmitted,
            Event::WritesStarted => EventName::WritesStarted,
            Event::LockLineWriteStarted { .. } => EventName::LockLineWriteStarted,
            Event::LockLineWritten { .. } => EventName::LockLineWritten,
            Event::ProgressRemoved { .. } => EventName::ProgressRemoved,
            Event::EngineFinished { .. } => EventName::EngineFinished,
            Event::RunFinished { .. } => EventName::RunFinished,
        }
    }

    fn level(&self) -> Option<Level> {
        match self {
            Event::DiagnosticEmitted(d) => Some(d.message().level),
            _ => None,
        }
    }

    fn body(&self) -> String {
        match self {
            Event::DiagnosticEmitted(d) => d.body(),
            other => other.name().fixed_body().unwrap_or_default().to_owned(),
        }
    }

    fn attributes(&self) -> Vec<(String, json::Value)> {
        use json::Value;
        let s = |k: &str, v: &str| (k.to_owned(), Value::str(v));
        let n = |k: &str, v: u8| (k.to_owned(), Value::Int(i64::from(v)));
        match self {
            Event::RunStarted { mode, argv } => vec![
                s(key::MODE, mode.as_str()),
                (
                    key::ARGV.to_owned(),
                    Value::Array(argv.iter().map(|a| Value::str(a.as_str())).collect()),
                ),
            ],
            Event::DiagnosticEmitted(d) => {
                let mut attrs = vec![s(key::REASON_CODE, d.message().code)];
                for (name, value) in d.args() {
                    attrs.push(s(&format!("{}{name}", key::PLACEHOLDER_PREFIX), value));
                }
                attrs
            }
            Event::LockLineWriteStarted { target } | Event::LockLineWritten { target } => {
                vec![s(key::TARGET, target.as_str())]
            }
            Event::ProgressRemoved { file } => vec![s(key::PROGRESS_FILE, file)],
            Event::EngineFinished { exit_code } => vec![n(key::EXIT_CODE, *exit_code)],
            Event::RunFinished {
                exit_code,
                engine_exit_code,
                stop_reason,
            } => vec![
                n(key::EXIT_CODE, *exit_code),
                (
                    key::ENGINE_EXIT_CODE.to_owned(),
                    engine_exit_code.map_or(Value::Null, |c| Value::Int(i64::from(c))),
                ),
                s(key::STOP_REASON_CODE, stop_reason.as_str()),
            ],
            Event::EngineStarted | Event::WritesStarted => Vec::new(),
        }
    }
}

/// `severity_text` 與 `severity_number`：info 9、warn 13、error 17、fatal 21（#118）。
/// 診斷以外的事件都是 info（03 輸出：info 只用在成功結果與執行紀錄）。
pub fn severity(level: Option<Level>) -> (&'static str, i64) {
    match level {
        None => ("info", 9),
        Some(Level::Warn) => ("warn", 13),
        Some(Level::Error) => ("error", 17),
        Some(Level::Fatal) => ("fatal", 21),
    }
}

/// 一行紀錄的共同欄位。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Header {
    /// 這一端的版本（`resource."service.version"`）。
    pub version: String,
    pub component: Component,
    /// 這次呼叫的識別（兩端寫同一個值）。
    pub invocation_id: String,
}

/// 把一筆事件格式化成一行（含結尾 LF）。不查註冊表、不檢查元件；那些由 [`Writer`] 做。
pub fn format_line(header: &Header, timestamp: &str, event: &Event) -> String {
    use json::Value;
    let name = event.name();
    let (sev_text, sev_number) = severity(event.level());
    let mut attributes = vec![
        (key::LOG_FORMAT.to_owned(), Value::str(LOG_FORMAT)),
        (
            key::COMPONENT.to_owned(),
            Value::str(header.component.as_str()),
        ),
        (
            key::INVOCATION_ID.to_owned(),
            Value::str(header.invocation_id.as_str()),
        ),
    ];
    attributes.extend(event.attributes());
    let record = Value::Object(vec![
        ("timestamp".to_owned(), Value::str(timestamp)),
        ("severity_text".to_owned(), Value::str(sev_text)),
        ("severity_number".to_owned(), Value::Int(sev_number)),
        ("event_name".to_owned(), Value::str(name.as_str())),
        ("body".to_owned(), Value::Str(event.body())),
        (
            "resource".to_owned(),
            Value::Object(vec![
                ("service.name".to_owned(), Value::str(SERVICE_NAME)),
                (
                    "service.version".to_owned(),
                    Value::str(header.version.as_str()),
                ),
            ]),
        ),
        ("attributes".to_owned(), Value::Object(attributes)),
    ]);
    let mut line = record.to_line();
    line.push('\n');
    line
}

/// 寫紀錄失敗。
#[derive(Debug)]
pub enum Error {
    /// 事件名不在註冊表裡（VK0056）。
    Unregistered(&'static str),
    /// 這一端不該寫這個事件（VK0056）。
    WrongComponent {
        event: &'static str,
        component: Component,
    },
    /// 時鐘早於 1970 或晚於 9999 年，寫不出時間戳（VK0056）。
    Clock,
    /// 寫檔失敗。
    Io(io::Error),
}

impl Error {
    /// 對應的訊息表代碼；寫檔失敗由呼叫端依時機決定，這裡回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            Error::Unregistered(_) | Error::WrongComponent { .. } | Error::Clock => {
                Some(&messages::VK0056)
            }
            Error::Io(_) => None,
        }
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Unregistered(name) => {
                write!(f, "event name {name} is not in the event registry")
            }
            Error::WrongComponent { event, component } => {
                write!(
                    f,
                    "event {event} cannot be written by {}",
                    component.as_str()
                )
            }
            Error::Clock => f.write_str("the system clock is outside the supported range"),
            Error::Io(e) => write!(f, "{e}"),
        }
    }
}

impl std::error::Error for Error {}

/// 開啟啟動器已建好的紀錄檔，接在後面寫；檔不存在就回錯，不另建（建檔是啟動器的事）。
pub fn open_append(path: &Path) -> io::Result<File> {
    OpenOptions::new().append(true).open(path)
}

/// 一端的紀錄寫入：每筆先查註冊表與元件，再整行一次寫出並 flush。
pub struct Writer<W: Write> {
    out: W,
    header: Header,
    clock: Box<dyn FnMut() -> SystemTime>,
}

impl<W: Write> Writer<W> {
    pub fn new(out: W, header: Header) -> Self {
        Self {
            out,
            header,
            clock: Box::new(SystemTime::now),
        }
    }

    /// 換掉時鐘（測試用固定時間）。
    pub fn with_clock(mut self, clock: impl FnMut() -> SystemTime + 'static) -> Self {
        self.clock = Box::new(clock);
        self
    }

    pub fn write(&mut self, event: &Event) -> Result<(), Error> {
        let name = event.name();
        if !is_registered(name.as_str()) {
            return Err(Error::Unregistered(name.as_str()));
        }
        if !name.writable_by(self.header.component) {
            return Err(Error::WrongComponent {
                event: name.as_str(),
                component: self.header.component,
            });
        }
        let timestamp = time::format((self.clock)()).ok_or(Error::Clock)?;
        let line = format_line(&self.header, &timestamp, event);
        self.out.write_all(line.as_bytes()).map_err(Error::Io)?;
        self.out.flush().map_err(Error::Io)
    }

    pub fn into_inner(self) -> W {
        self.out
    }
}

/// 每條診斷恰好寫一筆 `diagnostic_emitted`（ADR-0005:7）。
impl<W: Write> Sink for Writer<W> {
    fn record(&mut self, diagnostic: &Diagnostic) -> io::Result<()> {
        self.write(&Event::DiagnosticEmitted(diagnostic))
            .map_err(|e| match e {
                Error::Io(e) => e,
                other => io::Error::other(other),
            })
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests;
