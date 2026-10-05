//! 引擎入口的 argv：啟動器傳的上下文，與 `--` 之後原樣轉來的 recipe 與參數。
//!
//! 形式固定（[`crate::argv::ORDER`] 的順序，每個選項剛好一次、各帶一個值，接著 `--`）：
//!
//! ```text
//! vendor_kit --protocol <P> --run-id <id> --host-root <root> --host-cwd <cwd> --run-log <path>
//!            --tty <stdin><stdout><stderr> --no-color <0|1> -- <recipe 與使用者參數原樣>
//! ```
//!
//! - `<P>`：不補零的十進位整數，從 1 起；接不接受由呼叫端經 `compat` 判定（ADR-0008:24）。
//! - `<id>`：同文法的 `run-id`。
//! - `<root>`、`<cwd>`：主機絕對路徑；`<cwd>` 是使用者下指令時的目錄（04 VK recipe 檢查的是這個），
//!   啟動器先解掉 symlink。兩者的關係（在不在安裝目錄裡）由引擎之後判定，這裡不看。
//! - `<path>`：執行紀錄，相對安裝目錄的路徑，不收空字串、絕對路徑與 `..`。
//! - `--tty`：三位 `0`／`1`，依序是 stdin、stdout、stderr 是不是 TTY（容器不帶 -t，引擎自己看不到）。
//! - `--no-color`：`1` 表示 `NO_COLOR` 非空（03 輸出）。
//! - `--` 之後可以是零個參數（`just vendor_kit` 的用法呼叫）；之後的內容一律不在這裡解讀，交給 `args`。

use std::ffi::{OsStr, OsString};
use std::fmt;
use std::os::unix::ffi::OsStrExt;
use std::path::{Component, PathBuf};

use messages::Message;

use crate::argv;
use crate::wire::RunId;

/// stdin、stdout、stderr 各自是不是 TTY。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Tty {
    pub stdin: bool,
    pub stdout: bool,
    pub stderr: bool,
}

/// 解析好的入口 argv。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Invocation {
    pub protocol: u32,
    pub run_id: RunId,
    pub host_root: PathBuf,
    pub host_cwd: PathBuf,
    pub run_log: PathBuf,
    pub tty: Tty,
    pub no_color: bool,
    /// `--` 之後的參數原樣（第一個是指令名）。
    pub rest: Vec<OsString>,
}

/// 入口 argv 不合。除了 [`ArgvError::NoProtocol`]，都是啟動器與引擎不合，屬 VK 的 bug（VK0056）。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ArgvError {
    /// 第一個參數不是 `--protocol`：不是經啟動器的呼叫。怎麼處理待決議（#457）。
    NoProtocol,
    /// 這個位置應該是這個選項（或它的值），但沒有或順序不對。
    Expected(&'static str),
    /// 選項的值不合。
    Invalid {
        option: &'static str,
        value: OsString,
    },
}

impl ArgvError {
    /// 對應的訊息表條目：經啟動器的呼叫卻不合，是 VK0056；沒有 `--protocol` 時待 #457，回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            ArgvError::NoProtocol => None,
            _ => Some(&messages::VK0056),
        }
    }
}

impl fmt::Display for ArgvError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ArgvError::NoProtocol => write!(f, "engine was not invoked with {}", argv::PROTOCOL),
            ArgvError::Expected(o) => write!(f, "expected {o} in engine arguments"),
            ArgvError::Invalid { option, value } => {
                write!(f, "invalid value for {option}: {value:?}")
            }
        }
    }
}

impl std::error::Error for ArgvError {}

fn absolute(v: &OsStr) -> Option<PathBuf> {
    (v.as_bytes().first() == Some(&b'/')).then(|| PathBuf::from(v))
}

fn relative(v: &OsStr) -> Option<PathBuf> {
    let p = PathBuf::from(v);
    let ok = !v.is_empty()
        && p.components()
            .all(|c| matches!(c, Component::Normal(_) | Component::CurDir));
    ok.then_some(p)
}

fn flag(v: u8) -> Option<bool> {
    match v {
        b'0' => Some(false),
        b'1' => Some(true),
        _ => None,
    }
}

fn protocol(v: &OsStr) -> Option<u32> {
    let b = v.as_bytes();
    if b.first().is_none_or(|&c| !(b'1'..=b'9').contains(&c)) || !b.iter().all(u8::is_ascii_digit) {
        return None;
    }
    v.to_str()?.parse().ok()
}

fn tty(v: &OsStr) -> Option<Tty> {
    match *v.as_bytes() {
        [i, o, e] => Some(Tty {
            stdin: flag(i)?,
            stdout: flag(o)?,
            stderr: flag(e)?,
        }),
        _ => None,
    }
}

fn no_color(v: &OsStr) -> Option<bool> {
    match *v.as_bytes() {
        [c] => flag(c),
        _ => None,
    }
}

impl Invocation {
    /// 解析 `vendor_kit` 之後的參數（不含程式名）。
    pub fn parse(args: &[OsString]) -> Result<Invocation, ArgvError> {
        if args.first().map(OsString::as_os_str) != Some(OsStr::new(argv::PROTOCOL)) {
            return Err(ArgvError::NoProtocol);
        }
        let mut values: Vec<&OsStr> = Vec::with_capacity(argv::ORDER.len());
        let mut it = args.iter();
        for option in argv::ORDER {
            if it.next().map(OsString::as_os_str) != Some(OsStr::new(option)) {
                return Err(ArgvError::Expected(option));
            }
            values.push(it.next().ok_or(ArgvError::Expected(option))?);
        }
        if it.next().map(OsString::as_os_str) != Some(OsStr::new(argv::END)) {
            return Err(ArgvError::Expected(argv::END));
        }
        let rest = it.cloned().collect();

        // 第 i 個選項的值，經 `f` 轉成型別；轉不了就回該選項的 Invalid。
        fn get<T>(
            values: &[&OsStr],
            i: usize,
            f: impl FnOnce(&OsStr) -> Option<T>,
        ) -> Result<T, ArgvError> {
            f(values[i]).ok_or_else(|| ArgvError::Invalid {
                option: argv::ORDER[i],
                value: values[i].to_owned(),
            })
        }
        let protocol = get(&values, 0, protocol)?;
        let run_id = get(&values, 1, |v| v.to_str().and_then(RunId::parse))?;
        let host_root = get(&values, 2, absolute)?;
        let host_cwd = get(&values, 3, absolute)?;
        let run_log = get(&values, 4, relative)?;
        let tty = get(&values, 5, tty)?;
        let no_color = get(&values, 6, no_color)?;

        Ok(Invocation {
            protocol,
            run_id,
            host_root,
            host_cwd,
            run_log,
            tty,
            no_color,
            rest,
        })
    }
}
