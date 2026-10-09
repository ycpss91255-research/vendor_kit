//! `ctl/` 目錄裡的往返：寫 `req.<seq>`、讀 `res.<seq>`、最後寫 `done`。
//!
//! 引擎寫的檔一律先寫 `<名>.tmp` 再 rename，啟動器不會讀到寫一半的檔；啟動器寫 `res.<seq>` 也照同一個做法，
//! 所以 `res.<seq>` 一出現就是完整的。同一時間只有一個未完成的 request。
//!
//! 呼叫方的介面版不在引擎接受的區間內、而照救援路徑執行時，以 [`Channel::restrict_to_rescue`] 限定只送
//! [`crate::RESCUE_OPS`] 的 op（crate 文件「救援路徑」）；其餘 op 不寫檔，回 [`ChannelError::NotRescue`]。

use std::fmt;
use std::fs;
use std::io::{self, Write};
use std::path::{Path, PathBuf};
use std::thread;
use std::time::Duration;

use messages::Message;

use crate::wire::{Exit, Header, Op, OpKind, Outcome, ProtocolError, Reply, Seq};
use crate::{RESCUE_OPS, files};

/// 往返失敗：讀寫控制檔出錯，或啟動器回的東西不合協定。都是 VK0056。
#[derive(Debug)]
pub enum ChannelError {
    Io {
        path: PathBuf,
        source: io::Error,
    },
    Protocol(ProtocolError),
    /// 上一個 request 還沒收到結果就要送下一個，或還沒收完就要寫 done。
    Pending(Seq),
    /// 沒有未完成的 request 卻要收結果。
    Idle,
    /// seq 用完（9999）。
    Exhausted,
    /// 限定救援路徑時要送救援路徑以外的 op。
    NotRescue(OpKind),
}

impl ChannelError {
    /// 對應的訊息表條目（VK0056，內部錯誤）。
    pub fn message(&self) -> &'static Message {
        &messages::VK0056
    }
}

impl fmt::Display for ChannelError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ChannelError::Io { path, source } => write!(f, "{}: {source}", path.display()),
            ChannelError::Protocol(e) => write!(f, "{e}"),
            ChannelError::Pending(s) => write!(f, "request {s} is still pending"),
            ChannelError::Idle => f.write_str("no request is pending"),
            ChannelError::Exhausted => f.write_str("request sequence exhausted"),
            ChannelError::NotRescue(k) => write!(
                f,
                "op {} is outside the rescue path and the interface version is not supported",
                k.name()
            ),
        }
    }
}

impl std::error::Error for ChannelError {}

impl From<ProtocolError> for ChannelError {
    fn from(e: ProtocolError) -> ChannelError {
        ChannelError::Protocol(e)
    }
}

/// 引擎這一端的控制目錄。
#[derive(Debug)]
pub struct Channel {
    dir: PathBuf,
    header: Header,
    next: Option<Seq>,
    pending: Option<(Seq, OpKind)>,
    rescue_only: bool,
}

impl Channel {
    /// `dir` 是容器內的 `ctl/`（正式執行時是 [`crate::mount::CTL`]）。
    pub fn new(dir: impl Into<PathBuf>, header: Header) -> Channel {
        Channel {
            dir: dir.into(),
            header,
            next: Some(Seq::FIRST),
            pending: None,
            rescue_only: false,
        }
    }

    /// 之後只准送 [`RESCUE_OPS`] 的 op（呼叫方的介面版不在引擎接受的區間內時）。
    pub fn restrict_to_rescue(&mut self) {
        self.rescue_only = true;
    }

    pub fn header(&self) -> &Header {
        &self.header
    }

    /// 這次能不能送 `kind` 的 op：呼叫方的介面版要有它（[`OpKind::since`]），限定救援路徑時還要在
    /// [`RESCUE_OPS`] 裡。送不了的 op 由呼叫端改走舊的做法，不送。
    pub fn supports(&self, kind: OpKind) -> bool {
        self.header.protocol() >= kind.since()
            && (!self.rescue_only || RESCUE_OPS.contains(&kind.name()))
    }

    /// `req.<seq>` 的路徑。
    pub fn request_path(&self, seq: Seq) -> PathBuf {
        self.dir.join(format!("{}{seq}", files::REQ_PREFIX))
    }

    /// `res.<seq>` 的路徑。
    pub fn response_path(&self, seq: Seq) -> PathBuf {
        self.dir.join(format!("{}{seq}", files::RES_PREFIX))
    }

    /// `res.<seq>.out` 的路徑：inspect、ps、load 的原始輸出。load 的是 #589 起才寫的，讀的一端要容許檔不存在。
    pub fn output_path(&self, seq: Seq) -> PathBuf {
        self.dir
            .join(format!("{}{seq}{}", files::RES_PREFIX, files::OUT_SUFFIX))
    }

    /// `done` 的路徑。
    pub fn done_path(&self) -> PathBuf {
        self.dir.join(files::DONE)
    }

    /// 送出一個 request：寫 `req.<seq>.tmp` 再 rename 成 `req.<seq>`。
    pub fn send(&mut self, op: &Op) -> Result<Seq, ChannelError> {
        if let Some((seq, _)) = self.pending {
            return Err(ChannelError::Pending(seq));
        }
        if self.rescue_only && !RESCUE_OPS.contains(&op.kind().name()) {
            return Err(ChannelError::NotRescue(op.kind()));
        }
        let seq = self.next.ok_or(ChannelError::Exhausted)?;
        let bytes = op.encode_request(&self.header, seq)?;
        write_atomic(&self.request_path(seq), &bytes)?;
        self.pending = Some((seq, op.kind()));
        self.next = seq.next();
        Ok(seq)
    }

    /// 看結果到了沒：`res.<seq>` 還不存在回 `None`；存在就解析，不合協定回錯。
    pub fn try_receive(&mut self) -> Result<Option<Reply>, ChannelError> {
        let (seq, kind) = self.pending.ok_or(ChannelError::Idle)?;
        let path = self.response_path(seq);
        let bytes = match fs::read(&path) {
            Ok(b) => b,
            Err(e) if e.kind() == io::ErrorKind::NotFound => return Ok(None),
            Err(source) => return Err(ChannelError::Io { path, source }),
        };
        let outcome = Outcome::parse_response(&bytes, &self.header, seq, kind)?;
        self.pending = None;
        Ok(Some(Reply { seq, kind, outcome }))
    }

    /// 等到結果為止，每 `poll` 看一次。啟動器中斷時會停掉引擎容器，所以這裡不設逾時。
    pub fn receive(&mut self, poll: Duration) -> Result<Reply, ChannelError> {
        loop {
            if let Some(reply) = self.try_receive()? {
                return Ok(reply);
            }
            thread::sleep(poll);
        }
    }

    /// 寫 `done`，結束這次往返；還有未完成的 request 就回錯。
    pub fn finish(self, exit: Exit) -> Result<(), ChannelError> {
        if let Some((seq, _)) = self.pending {
            return Err(ChannelError::Pending(seq));
        }
        write_atomic(&self.done_path(), &exit.encode_done(&self.header))
    }
}

/// 先寫 `<path>.tmp`、flush 到磁碟，再 rename 成 `path`。
fn write_atomic(path: &Path, bytes: &[u8]) -> Result<(), ChannelError> {
    let mut tmp = path.as_os_str().to_owned();
    tmp.push(files::TMP_SUFFIX);
    let tmp = PathBuf::from(tmp);
    let io = |path: &Path| {
        let path = path.to_owned();
        move |source| ChannelError::Io { path, source }
    };
    let mut f = fs::File::create(&tmp).map_err(io(&tmp))?;
    f.write_all(bytes).map_err(io(&tmp))?;
    f.sync_all().map_err(io(&tmp))?;
    drop(f);
    fs::rename(&tmp, path).map_err(io(path))
}
