//! 控制檔的位元組：req、res、done 的寫法與讀法（文法見 crate 文件）。

use std::fmt;

use messages::Message;

use crate::GRAMMAR;
use crate::field::{Field, FieldError};

/// 協定不合：文法、header、seq 不符，或 op 與 result 不配對。這是 VK 的 bug（VK0056）。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProtocolError {
    reason: String,
}

impl ProtocolError {
    pub(crate) fn new(reason: impl Into<String>) -> ProtocolError {
        ProtocolError {
            reason: reason.into(),
        }
    }

    /// 英文的原因，給 VK0056 的 `<reason>`。
    pub fn reason(&self) -> &str {
        &self.reason
    }

    /// 對應的訊息表條目（VK0056，內部錯誤）。
    pub fn message(&self) -> &'static Message {
        &messages::VK0056
    }
}

impl fmt::Display for ProtocolError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{GRAMMAR} protocol error: {}", self.reason)
    }
}

impl std::error::Error for ProtocolError {}

impl From<FieldError> for ProtocolError {
    fn from(e: FieldError) -> ProtocolError {
        ProtocolError::new(e.to_string())
    }
}

fn is_lower_hex(s: &str, len: usize) -> bool {
    s.len() == len
        && s.bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}

/// 不補零的十進位：第一位不是 0（單獨的 "0" 只在 `allow_zero` 時收）。
fn decimal(s: &str, allow_zero: bool) -> Option<u64> {
    let bytes = s.as_bytes();
    if bytes.is_empty() || bytes.len() > 19 || !bytes.iter().all(u8::is_ascii_digit) {
        return None;
    }
    if bytes[0] == b'0' {
        return (allow_zero && bytes.len() == 1).then_some(0);
    }
    s.parse().ok()
}

/// `run-id`：小寫字母、數字與 `-`，1–64 個字元。
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct RunId(String);

impl RunId {
    pub fn parse(s: &str) -> Option<RunId> {
        let ok = (1..=64).contains(&s.len())
            && s.bytes()
                .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'-');
        ok.then(|| RunId(s.to_owned()))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

/// 每個控制檔第一行開頭的 `vk-resolve/<P> <run-id>`；P、run-id 是 argv 傳進來的值。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Header {
    protocol: u32,
    run_id: RunId,
}

impl Header {
    /// P 從 1 起算；0 回 `None`。
    pub fn new(protocol: u32, run_id: RunId) -> Option<Header> {
        (protocol >= 1).then_some(Header { protocol, run_id })
    }

    pub fn protocol(&self) -> u32 {
        self.protocol
    }

    pub fn run_id(&self) -> &RunId {
        &self.run_id
    }

    fn line(&self) -> String {
        format!("{GRAMMAR}/{} {}", self.protocol, self.run_id.0)
    }
}

/// request 的序號：1–9999，從 1 起連續。
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Seq(u16);

impl Seq {
    pub const FIRST: Seq = Seq(1);
    pub const MAX: u16 = 9999;

    pub fn new(n: u16) -> Option<Seq> {
        (1..=Seq::MAX).contains(&n).then_some(Seq(n))
    }

    pub fn get(self) -> u16 {
        self.0
    }

    /// 下一個序號；用完 9999 回 `None`。
    pub fn next(self) -> Option<Seq> {
        Seq::new(self.0 + 1)
    }

    fn parse(s: &str) -> Option<Seq> {
        if s.len() > 4 {
            return None;
        }
        decimal(s, false)
            .and_then(|n| u16::try_from(n).ok())
            .and_then(Seq::new)
    }
}

impl fmt::Display for Seq {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

/// `ref`：小寫字母或數字開頭，之後是小寫字母、數字與 `._/:@-`。
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct ImageRef(String);

impl ImageRef {
    pub fn parse(s: &str) -> Option<ImageRef> {
        let mut bytes = s.bytes();
        let first = bytes.next()?;
        let ok = (first.is_ascii_lowercase() || first.is_ascii_digit())
            && bytes
                .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b"._/:@-".contains(&b));
        ok.then(|| ImageRef(s.to_owned()))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }

    /// 以 `@sha256:<64 位小寫 hex>` 結尾，而且全串只有這一個 `@`（pull 只收這種）。
    pub fn is_pinned(&self) -> bool {
        match self.0.split_once('@') {
            Some((name, digest)) => {
                !name.is_empty()
                    && digest
                        .strip_prefix("sha256:")
                        .is_some_and(|h| is_lower_hex(h, 64))
            }
            None => false,
        }
    }
}

/// extract 的對象：`sha256:<64 位小寫 hex>` 的 image ID，不收 tag 或 digest 引用。
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct ImageId(String);

impl ImageId {
    pub fn parse(s: &str) -> Option<ImageId> {
        s.strip_prefix("sha256:")
            .is_some_and(|h| is_lower_hex(h, 64))
            .then(|| ImageId(s.to_owned()))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

/// 容器 ID：64 位小寫 hex。
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Container(String);

impl Container {
    pub fn parse(s: &str) -> Option<Container> {
        is_lower_hex(s, 64).then(|| Container(s.to_owned()))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

/// `in/` 底下的收件格名：小寫字母與數字，1–16 個字元。
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Slot(String);

impl Slot {
    pub fn parse(s: &str) -> Option<Slot> {
        let ok = (1..=16).contains(&s.len())
            && s.bytes()
                .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit());
        ok.then(|| Slot(s.to_owned()))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

/// op 的種類；名稱就是 [`crate::OPS`]。
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum OpKind {
    Pull,
    Load,
    Inspect,
    Extract,
    Stage,
    StageDir,
    Ps,
    RmContainer,
    Runner,
}

impl OpKind {
    /// 依 [`crate::OPS`] 的順序。
    pub const ALL: [OpKind; 9] = [
        OpKind::Pull,
        OpKind::Load,
        OpKind::Inspect,
        OpKind::Extract,
        OpKind::Stage,
        OpKind::StageDir,
        OpKind::Ps,
        OpKind::RmContainer,
        OpKind::Runner,
    ];

    pub fn name(self) -> &'static str {
        match self {
            OpKind::Pull => "pull",
            OpKind::Load => "load",
            OpKind::Inspect => "inspect",
            OpKind::Extract => "extract",
            OpKind::Stage => "stage",
            OpKind::StageDir => "stage-dir",
            OpKind::Ps => "ps",
            OpKind::RmContainer => "rm-container",
            OpKind::Runner => "runner",
        }
    }

    fn from_name(s: &str) -> Option<OpKind> {
        OpKind::ALL.into_iter().find(|k| k.name() == s)
    }
}

/// 引擎要啟動器代做的一個動作。主機路徑是絕對路徑；runner 至少有 command。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Op {
    /// `docker pull`；只收帶 digest 的引用。
    Pull(ImageRef),
    /// `docker load -i <主機路徑>`。
    Load(Field),
    /// `docker image inspect`，輸出寫 `res.<seq>.out`。
    Inspect(ImageRef),
    /// 由 image ID 建容器、`docker cp /dist/.` 進 `in/<slot>`、刪容器；不 run。
    Extract(ImageId, Slot),
    /// 把主機檔複製進 `in/<slot>`。
    Stage(Field, Slot),
    /// 把主機上的目錄整個複製進 `in/<slot>`（`dev`、`sync`、`upgrade` 讀安裝目錄外的本機開發來源）。
    StageDir(Field, Slot),
    /// 列本安裝目錄 label 的已停止容器，輸出寫 `res.<seq>.out`。
    Ps,
    /// 刪本次 ps 列出的一個容器，不加 -f。
    RmContainer(Container),
    /// 在使用者指定的 image 跑 test runner：command 加參數，不經 shell。
    Runner {
        image: ImageRef,
        command: Field,
        args: Vec<Field>,
    },
}

fn host_path(f: &Field) -> Result<(), ProtocolError> {
    if f.as_bytes().first() == Some(&b'/') {
        Ok(())
    } else {
        Err(ProtocolError::new("host path is not absolute"))
    }
}

impl Op {
    pub fn kind(&self) -> OpKind {
        match self {
            Op::Pull(_) => OpKind::Pull,
            Op::Load(_) => OpKind::Load,
            Op::Inspect(_) => OpKind::Inspect,
            Op::Extract(..) => OpKind::Extract,
            Op::Stage(..) => OpKind::Stage,
            Op::StageDir(..) => OpKind::StageDir,
            Op::Ps => OpKind::Ps,
            Op::RmContainer(_) => OpKind::RmContainer,
            Op::Runner { .. } => OpKind::Runner,
        }
    }

    /// 型別保證不了的條件：pull 帶 digest、load、stage 與 stage-dir 的路徑是絕對路徑。
    pub fn validate(&self) -> Result<(), ProtocolError> {
        match self {
            Op::Pull(r) if !r.is_pinned() => {
                Err(ProtocolError::new("pull reference is not pinned by digest"))
            }
            Op::Load(p) | Op::Stage(p, _) | Op::StageDir(p, _) => host_path(p),
            _ => Ok(()),
        }
    }

    fn line(&self) -> String {
        let name = self.kind().name();
        match self {
            Op::Pull(r) | Op::Inspect(r) => format!("{name} {}", r.0),
            Op::Load(p) => format!("{name} {}", p.encode()),
            Op::Extract(id, slot) => format!("{name} {} {}", id.0, slot.0),
            Op::Stage(p, slot) | Op::StageDir(p, slot) => {
                format!("{name} {} {}", p.encode(), slot.0)
            }
            Op::Ps => name.to_owned(),
            Op::RmContainer(c) => format!("{name} {}", c.0),
            Op::Runner {
                image,
                command,
                args,
            } => {
                let mut s = format!("{name} {} {}", image.0, command.encode());
                for a in args {
                    s.push(' ');
                    s.push_str(&a.encode());
                }
                s
            }
        }
    }

    /// `req.<seq>` 的確切位元組；不合 [`Op::validate`] 就回錯。
    pub fn encode_request(&self, header: &Header, seq: Seq) -> Result<Vec<u8>, ProtocolError> {
        self.validate()?;
        Ok(format!("{} {seq}\n{}\n", header.line(), self.line()).into_bytes())
    }

    /// 讀 `req.<seq>`（bash 端驗證的同一份規則）：header 必須等於 `header`。
    pub fn parse_request(bytes: &[u8], header: &Header) -> Result<(Seq, Op), ProtocolError> {
        let [first, second] = lines::<2>(bytes)?;
        let seq = parse_first_line(first, header, |rest| match rest {
            [s] => Seq::parse(s).ok_or_else(|| ProtocolError::new("invalid seq")),
            _ => Err(ProtocolError::new("invalid request header")),
        })?;
        let op = parse_op(&tokens(second)?)?;
        op.validate()?;
        Ok((seq, op))
    }
}

fn parse_op(t: &[&str]) -> Result<Op, ProtocolError> {
    let (&name, rest) = t
        .split_first()
        .ok_or_else(|| ProtocolError::new("empty op"))?;
    let kind = OpKind::from_name(name)
        .ok_or_else(|| ProtocolError::new(format!("unknown op {name:?}")))?;
    let bad = || ProtocolError::new(format!("invalid operands for op {name}"));
    let image = |s: &str| ImageRef::parse(s).ok_or_else(bad);
    let slot = |s: &str| Slot::parse(s).ok_or_else(bad);
    Ok(match (kind, rest) {
        (OpKind::Pull, [r]) => Op::Pull(image(r)?),
        (OpKind::Load, [p]) => Op::Load(Field::decode(p)?),
        (OpKind::Inspect, [r]) => Op::Inspect(image(r)?),
        (OpKind::Extract, [id, s]) => Op::Extract(ImageId::parse(id).ok_or_else(bad)?, slot(s)?),
        (OpKind::Stage, [p, s]) => Op::Stage(Field::decode(p)?, slot(s)?),
        (OpKind::StageDir, [p, s]) => Op::StageDir(Field::decode(p)?, slot(s)?),
        (OpKind::Ps, []) => Op::Ps,
        (OpKind::RmContainer, [c]) => Op::RmContainer(Container::parse(c).ok_or_else(bad)?),
        (OpKind::Runner, [r, cmd, args @ ..]) => Op::Runner {
            image: image(r)?,
            command: Field::decode(cmd)?,
            args: args
                .iter()
                .map(|a| Field::decode(a))
                .collect::<Result<_, _>>()?,
        },
        _ => return Err(bad()),
    })
}

/// runner 的結果：起來沒、自己的結束碼、是不是被 VK 停掉。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RunnerOutcome {
    /// 沒起來（create 或 start 失敗）。
    NotStarted,
    /// 起來了、自己結束，帶結束碼。
    Exited(u8),
    /// 起來了、被 VK 停掉（例如收到中斷）；拿得到結束碼才帶。
    Stopped(Option<u8>),
}

impl RunnerOutcome {
    pub fn started(self) -> bool {
        !matches!(self, RunnerOutcome::NotStarted)
    }

    /// runner 自己的結束碼；沒有就是 `None`（診斷續行印 unavailable）。
    pub fn process_rc(self) -> Option<u8> {
        match self {
            RunnerOutcome::NotStarted => None,
            RunnerOutcome::Exited(rc) => Some(rc),
            RunnerOutcome::Stopped(rc) => rc,
        }
    }

    pub fn stopped_by_vk(self) -> bool {
        matches!(self, RunnerOutcome::Stopped(_))
    }

    /// 要報的原因代碼：起不來或被 VK 停掉是 VK0066，自己結束且非 0 是 VK0067，0 則沒有。
    pub fn failure(self) -> Option<&'static Message> {
        match self {
            RunnerOutcome::NotStarted | RunnerOutcome::Stopped(_) => Some(&messages::VK0066),
            RunnerOutcome::Exited(0) => None,
            RunnerOutcome::Exited(_) => Some(&messages::VK0067),
        }
    }
}

/// 啟動器回的結果。runner 只回 [`Outcome::Runner`]，其他 op 只回 `Ok` 或 `Failed`。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Outcome {
    Ok,
    /// docker 指令失敗，帶它的結束碼。
    Failed(u8),
    Runner(RunnerOutcome),
}

fn parse_rc(s: &str) -> Option<u8> {
    decimal(s, true).and_then(|n| u8::try_from(n).ok())
}

impl Outcome {
    /// 這個結果能不能回給 `kind` 的 op。
    pub fn fits(self, kind: OpKind) -> bool {
        matches!(self, Outcome::Runner(_)) == (kind == OpKind::Runner)
    }

    fn line(self) -> String {
        match self {
            Outcome::Ok => "ok".to_owned(),
            Outcome::Failed(rc) => format!("failed {rc}"),
            Outcome::Runner(RunnerOutcome::NotStarted) => "runner notstarted".to_owned(),
            Outcome::Runner(RunnerOutcome::Exited(rc)) => format!("runner exited {rc}"),
            Outcome::Runner(RunnerOutcome::Stopped(Some(rc))) => format!("runner stopped {rc}"),
            Outcome::Runner(RunnerOutcome::Stopped(None)) => {
                "runner stopped unavailable".to_owned()
            }
        }
    }

    /// `res.<seq>` 的確切位元組（啟動器寫的那一份；測試與 golden 用）。
    pub fn encode_response(self, header: &Header, seq: Seq) -> Vec<u8> {
        format!("{} {seq}\n{}\n", header.line(), self.line()).into_bytes()
    }

    /// 讀 `res.<seq>`：header、seq 必須相等，結果必須配得上 `kind`。
    pub fn parse_response(
        bytes: &[u8],
        header: &Header,
        seq: Seq,
        kind: OpKind,
    ) -> Result<Outcome, ProtocolError> {
        let [first, second] = lines::<2>(bytes)?;
        let got = parse_first_line(first, header, |rest| match rest {
            [s] => Seq::parse(s).ok_or_else(|| ProtocolError::new("invalid seq")),
            _ => Err(ProtocolError::new("invalid result header")),
        })?;
        if got != seq {
            return Err(ProtocolError::new(format!(
                "result seq {got} does not match request seq {seq}"
            )));
        }
        let bad = || ProtocolError::new(format!("invalid result {second:?}"));
        let rc = |s: &str| parse_rc(s).ok_or_else(bad);
        let outcome = match tokens(second)?.as_slice() {
            ["ok"] => Outcome::Ok,
            ["failed", n] => Outcome::Failed(rc(n)?),
            ["runner", "notstarted"] => Outcome::Runner(RunnerOutcome::NotStarted),
            ["runner", "exited", n] => Outcome::Runner(RunnerOutcome::Exited(rc(n)?)),
            ["runner", "stopped", "unavailable"] => Outcome::Runner(RunnerOutcome::Stopped(None)),
            ["runner", "stopped", n] => Outcome::Runner(RunnerOutcome::Stopped(Some(rc(n)?))),
            _ => return Err(bad()),
        };
        if !outcome.fits(kind) {
            return Err(ProtocolError::new(format!(
                "result {second:?} does not fit op {}",
                kind.name()
            )));
        }
        Ok(outcome)
    }
}

/// 收到的一筆結果。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Reply {
    pub seq: Seq,
    pub kind: OpKind,
    pub outcome: Outcome,
}

/// 引擎寫進 `done` 的結束碼：0–3。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Exit(u8);

impl Exit {
    pub fn new(code: u8) -> Option<Exit> {
        (code <= 3).then_some(Exit(code))
    }

    pub fn code(self) -> u8 {
        self.0
    }

    /// `done` 的確切位元組。
    pub fn encode_done(self, header: &Header) -> Vec<u8> {
        format!("{} done {}\n", header.line(), self.0).into_bytes()
    }

    /// 讀 `done`（bash 端驗證的同一份規則）。
    pub fn parse_done(bytes: &[u8], header: &Header) -> Result<Exit, ProtocolError> {
        let [line] = lines::<1>(bytes)?;
        parse_first_line(line, header, |rest| match rest {
            ["done", c] if c.len() == 1 => c
                .parse()
                .ok()
                .and_then(Exit::new)
                .ok_or_else(|| ProtocolError::new("invalid done exit code")),
            _ => Err(ProtocolError::new("invalid done line")),
        })
    }
}

/// 拆成剛好 `N` 行：全是可見 ASCII 加空白，以 LF 結尾，沒有空行。
fn lines<const N: usize>(bytes: &[u8]) -> Result<[&str; N], ProtocolError> {
    let body = bytes
        .strip_suffix(b"\n")
        .ok_or_else(|| ProtocolError::new("control file does not end with LF"))?;
    if !body
        .iter()
        .all(|&b| b == b'\n' || b == b' ' || (0x21..=0x7E).contains(&b))
    {
        return Err(ProtocolError::new(
            "control file has bytes outside printable ASCII",
        ));
    }
    let text =
        std::str::from_utf8(body).map_err(|_| ProtocolError::new("control file is not ASCII"))?;
    let v: Vec<&str> = text.split('\n').collect();
    v.try_into()
        .map_err(|_| ProtocolError::new(format!("control file must have exactly {N} line(s)")))
}

/// 以單一空白分欄；開頭、結尾或連續的空白都不收。
fn tokens(line: &str) -> Result<Vec<&str>, ProtocolError> {
    let t: Vec<&str> = line.split(' ').collect();
    if t.iter().any(|s| s.is_empty()) {
        return Err(ProtocolError::new(format!("stray space in {line:?}")));
    }
    Ok(t)
}

/// 第一行：前兩欄必須等於 `header`，剩下的欄交給 `rest`。
fn parse_first_line<T>(
    line: &str,
    header: &Header,
    rest: impl FnOnce(&[&str]) -> Result<T, ProtocolError>,
) -> Result<T, ProtocolError> {
    let t = tokens(line)?;
    let expected = format!("{GRAMMAR}/{}", header.protocol);
    match t.as_slice() {
        [g, id, more @ ..] if *g == expected && *id == header.run_id.0 => rest(more),
        _ => Err(ProtocolError::new(format!(
            "header does not match {}",
            header.line()
        ))),
    }
}
