//! 判定「未完成首次導入」（04:121–130、VK0037、ADR-0007:31）：讀最近一筆執行紀錄的內容，
//! 回答 bootstrap.sh 能不能把它當成未完成的首次導入、允許帶 -y 重跑。
//!
//! 規則（#372 定案的里程碑事件）：
//! 1. 讀得出有效引擎版本鎖定行就不套用（04:126）。
//! 2. 每一行都要完整：LF 結尾、是正規形（[`crate::json`]）、`vendor_kit.log_format` 是支援的版本、
//!    鍵序與值都合法。任一行不過就不套用（04:130），不往回查更舊的紀錄。
//! 3. 第一行是唯一的 `run_started`，整份只有一個 `invocation_id`；不然無法唯一判定。
//! 4. `run_started` 的 mode 要是 `initial_import`。
//! 5. 要有 `engine_finished` 或 `run_finished`；兩個都沒有表示還在跑或被中途殺掉，無法確定。
//! 6. `lock_line_write_started` 與 `progress_removed` 要在 `writes_started` 之後；
//!    每筆 `lock_line_write_started` 都要有對應的 `lock_line_written`；有 started 沒有 written 不套用。
//! 7. `run_finished` 的 stop_reason_code 若是代碼，同一份紀錄裡要有同代碼的 `diagnostic_emitted`。
//! 8. 條件 (a)：`run_finished` 停在 VK0002，且沒有 `writes_started`。
//!    條件 (b)：沒有 target=engine 的 `lock_line_write_started`。
//!
//! 紀錄檔怎麼挑出「最近一筆」（檔名排序、同時執行）由啟動器端定，不在這裡。

use crate::json::{self, Value};
use crate::{
    Component, EventName, LOG_FORMAT, Mode, SERVICE_NAME, StopReason, Target, key, severity, time,
};

/// 判定結果。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Verdict {
    /// 是未完成的首次導入。
    Applies(Condition),
    /// 不套用例外；照一般規則處理（VK0037）。
    NotApplicable(Reason),
}

/// 符合哪一個條件（04:121）。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Condition {
    /// (a) 停在 VK0002，除執行紀錄外沒改檔。
    StoppedAtPrompt,
    /// (b) 建紀錄之後、寫引擎版本鎖定行之前結束。
    BeforeEngineLockLine,
}

/// 不套用的原因。`line` 從 1 起算。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Reason {
    /// 讀得出有效引擎版本鎖定行。
    EngineLockLineReadable,
    /// 紀錄是空的。
    Empty,
    /// 最後一行沒有 LF（寫到一半）。
    Truncated { line: usize },
    /// 這一行的 `vendor_kit.log_format` 不是支援的版本。
    UnsupportedFormat { line: usize },
    /// 這一行不是合格的紀錄行。
    InvalidLine { line: usize },
    /// 沒有 `run_started`。
    MissingRunStarted,
    /// 無法唯一判定：`run_started` 不在第一行或不只一筆、invocation_id 不只一個、事件順序不合理。
    NotUnique,
    /// 不是首次導入。
    NotInitialImport,
    /// 沒有結束事件，可能還在跑。
    NotFinished,
    /// 有 `lock_line_write_started` 沒有對應的 `lock_line_written`。
    LockLineWriteUnconfirmed,
    /// 停下原因的代碼在這份紀錄裡沒有對應的診斷。
    StopReasonNotDiagnosed,
    /// 引擎版本鎖定行已經寫過（之後又讀不出來），不是未完成的首次導入。
    EngineLockLineWritten,
}

/// 解析好的一行：判定需要的部分。
#[derive(Debug, Clone, PartialEq, Eq)]
struct Entry {
    invocation_id: String,
    kind: Kind,
}

#[derive(Debug, Clone, PartialEq, Eq)]
enum Kind {
    RunStarted(Mode),
    EngineStarted,
    DiagnosticEmitted(&'static str),
    WritesStarted,
    LockLineWriteStarted(Target),
    LockLineWritten(Target),
    ProgressRemoved,
    EngineFinished,
    RunFinished(StopReason),
}

/// 判定。`log` 是最近一筆紀錄檔的完整內容；`engine_lock_line_readable` 是呼叫端讀
/// `.vendor_kit/version.toml` 的結果（讀得出恰好一行有效的引擎版本鎖定行）。
pub fn assess(log: &[u8], engine_lock_line_readable: bool) -> Verdict {
    use Verdict::NotApplicable as No;
    if engine_lock_line_readable {
        return No(Reason::EngineLockLineReadable);
    }
    let entries = match parse_log(log) {
        Ok(e) => e,
        Err(reason) => return No(reason),
    };
    let Some(first) = entries.first() else {
        return No(Reason::Empty);
    };
    let started = entries
        .iter()
        .filter(|e| matches!(e.kind, Kind::RunStarted(_)))
        .count();
    let mode = match first.kind {
        Kind::RunStarted(mode) if started == 1 => mode,
        _ if started == 0 => return No(Reason::MissingRunStarted),
        _ => return No(Reason::NotUnique),
    };
    if entries
        .iter()
        .any(|e| e.invocation_id != first.invocation_id)
    {
        return No(Reason::NotUnique);
    }
    if mode != Mode::InitialImport {
        return No(Reason::NotInitialImport);
    }

    let mut finished = false;
    let mut writes_started = false;
    let mut engine_lock_started = false;
    let mut pending = [0usize; 2];
    let mut stop = None;
    let mut diagnosed: Vec<&str> = Vec::new();
    for e in &entries {
        match e.kind {
            Kind::RunStarted(_) | Kind::EngineStarted => {}
            // 改檔一定在 writes_started 之後（ADR-0004:33：進度檔是第一筆非紀錄檔寫入）；
            // 順序不對就不是正常引擎寫得出來的紀錄，無法判定。
            Kind::LockLineWriteStarted(_) | Kind::ProgressRemoved if !writes_started => {
                return No(Reason::NotUnique);
            }
            Kind::ProgressRemoved => {}
            Kind::DiagnosticEmitted(code) => diagnosed.push(code),
            Kind::WritesStarted => writes_started = true,
            Kind::LockLineWriteStarted(t) => {
                pending[t as usize] += 1;
                if t == Target::Engine {
                    engine_lock_started = true;
                }
            }
            Kind::LockLineWritten(t) => {
                // written 之前一定要有 started。
                if pending[t as usize] == 0 {
                    return No(Reason::NotUnique);
                }
                pending[t as usize] -= 1;
            }
            Kind::EngineFinished => finished = true,
            Kind::RunFinished(reason) => {
                if stop.is_some() {
                    return No(Reason::NotUnique);
                }
                finished = true;
                stop = Some(reason);
            }
        }
    }
    if !finished {
        return No(Reason::NotFinished);
    }
    if pending.iter().any(|&n| n > 0) {
        return No(Reason::LockLineWriteUnconfirmed);
    }
    if let Some(StopReason::Code(m)) = stop
        && !diagnosed.contains(&m.code)
    {
        return No(Reason::StopReasonNotDiagnosed);
    }
    if !writes_started
        && let Some(StopReason::Code(m)) = stop
        && m.code == messages::VK0002.code
    {
        return Verdict::Applies(Condition::StoppedAtPrompt);
    }
    if !engine_lock_started {
        return Verdict::Applies(Condition::BeforeEngineLockLine);
    }
    No(Reason::EngineLockLineWritten)
}

fn parse_log(log: &[u8]) -> Result<Vec<Entry>, Reason> {
    let mut entries = Vec::new();
    let mut rest = log;
    let mut line_no = 0;
    while !rest.is_empty() {
        line_no += 1;
        let Some(end) = rest.iter().position(|&b| b == b'\n') else {
            return Err(Reason::Truncated { line: line_no });
        };
        let line = &rest[..end];
        rest = &rest[end + 1..];
        entries.push(parse_line(line, line_no)?);
    }
    Ok(entries)
}

/// 讀一行（不含 LF）。
fn parse_line(line: &[u8], line_no: usize) -> Result<Entry, Reason> {
    let invalid = Reason::InvalidLine { line: line_no };
    let text = std::str::from_utf8(line).map_err(|_| invalid)?;
    let value = json::parse(text).ok_or(invalid)?;
    // 先看格式版本：版本不同時其他欄位可能本來就不一樣，要跟「壞行」分開報。
    if let Some(format) = log_format(&value)
        && format != LOG_FORMAT
    {
        return Err(Reason::UnsupportedFormat { line: line_no });
    }
    // 正規形：重新序列化要跟原行逐位元組相等（鍵序、空白、跳脫寫法都固定）。
    if value.to_line() != text {
        return Err(invalid);
    }
    decode(&value).ok_or(invalid)
}

fn log_format(value: &Value) -> Option<&str> {
    let Value::Object(top) = value else {
        return None;
    };
    let (_, Value::Object(attrs)) = top.iter().find(|(k, _)| k == "attributes")? else {
        return None;
    };
    match attrs.first()? {
        (k, Value::Str(v)) if k == key::LOG_FORMAT => Some(v),
        _ => None,
    }
}

/// 依序取出物件的成員，鍵要剛好照順序。
struct Fields<'a> {
    members: std::slice::Iter<'a, (String, Value)>,
}

impl<'a> Fields<'a> {
    fn new(value: &'a Value) -> Option<Fields<'a>> {
        match value {
            Value::Object(m) => Some(Fields { members: m.iter() }),
            _ => None,
        }
    }

    fn next(&mut self, key: &str) -> Option<&'a Value> {
        let (k, v) = self.members.next()?;
        (k == key).then_some(v)
    }

    fn str(&mut self, key: &str) -> Option<&'a str> {
        match self.next(key)? {
            Value::Str(s) => Some(s),
            _ => None,
        }
    }

    fn int(&mut self, key: &str) -> Option<i64> {
        match self.next(key)? {
            Value::Int(n) => Some(*n),
            _ => None,
        }
    }

    fn peek_key(&self) -> Option<&'a str> {
        self.members.clone().next().map(|(k, _)| k.as_str())
    }

    fn done(mut self) -> Option<()> {
        self.members.next().is_none().then_some(())
    }
}

fn exit_code(n: i64) -> Option<()> {
    (0..=255).contains(&n).then_some(())
}

fn decode(value: &Value) -> Option<Entry> {
    let mut top = Fields::new(value)?;
    let timestamp = top.str("timestamp")?;
    let sev_text = top.str("severity_text")?;
    let sev_number = top.int("severity_number")?;
    let name = EventName::parse(top.str("event_name")?)?;
    let body = top.str("body")?;
    let mut resource = Fields::new(top.next("resource")?)?;
    let attributes = top.next("attributes")?;
    top.done()?;

    if !time::is_valid(timestamp) || !crate::is_registered(name.as_str()) {
        return None;
    }
    (resource.str("service.name")? == SERVICE_NAME).then_some(())?;
    (!resource.str("service.version")?.is_empty()).then_some(())?;
    resource.done()?;

    let mut attrs = Fields::new(attributes)?;
    (attrs.str(key::LOG_FORMAT)? == LOG_FORMAT).then_some(())?;
    let component = Component::parse(attrs.str(key::COMPONENT)?)?;
    let invocation_id = attrs.str(key::INVOCATION_ID)?;
    if invocation_id.is_empty() || !name.writable_by(component) {
        return None;
    }

    // 診斷以外的事件：body 固定、嚴重度是 info。診斷的嚴重度跟訊息表的 level 對照（見下）。
    if name != EventName::DiagnosticEmitted
        && (Some(body) != name.fixed_body() || (sev_text, sev_number) != severity(None))
    {
        return None;
    }
    let kind = match name {
        EventName::RunStarted => {
            let mode = Mode::parse(attrs.str(key::MODE)?)?;
            match attrs.next(key::ARGV)? {
                Value::Array(items) if items.iter().all(|v| matches!(v, Value::Str(_))) => {}
                _ => return None,
            }
            Kind::RunStarted(mode)
        }
        EventName::EngineStarted => Kind::EngineStarted,
        EventName::DiagnosticEmitted => {
            let code = attrs.str(key::REASON_CODE)?;
            let message = crate::find_message(code)?;
            if (sev_text, sev_number) != severity(Some(message.level)) {
                return None;
            }
            while let Some(k) = attrs.peek_key() {
                let placeholder = k.strip_prefix(key::PLACEHOLDER_PREFIX)?;
                if placeholder.is_empty() {
                    return None;
                }
                attrs.str(k)?;
            }
            Kind::DiagnosticEmitted(message.code)
        }
        EventName::WritesStarted => Kind::WritesStarted,
        EventName::LockLineWriteStarted => {
            Kind::LockLineWriteStarted(Target::parse(attrs.str(key::TARGET)?)?)
        }
        EventName::LockLineWritten => {
            Kind::LockLineWritten(Target::parse(attrs.str(key::TARGET)?)?)
        }
        EventName::ProgressRemoved => {
            (!attrs.str(key::PROGRESS_FILE)?.is_empty()).then_some(())?;
            Kind::ProgressRemoved
        }
        EventName::EngineFinished => {
            exit_code(attrs.int(key::EXIT_CODE)?)?;
            Kind::EngineFinished
        }
        EventName::RunFinished => {
            exit_code(attrs.int(key::EXIT_CODE)?)?;
            match attrs.next(key::ENGINE_EXIT_CODE)? {
                Value::Null => {}
                Value::Int(n) => exit_code(*n)?,
                _ => return None,
            }
            Kind::RunFinished(StopReason::parse(attrs.str(key::STOP_REASON_CODE)?)?)
        }
    };
    attrs.done()?;
    Some(Entry {
        invocation_id: invocation_id.to_owned(),
        kind,
    })
}
