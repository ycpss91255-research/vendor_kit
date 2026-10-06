//! 假的啟動器：在測試裡扮演 `plan` 協定（`vk-resolve/1`）的另一端。
//!
//! 引擎在 `ctl/` 寫 `req.<seq>`，這裡讀到後交給測試給的處理函式（它可以寫 `res.<seq>.out`、
//! 往 `in/<slot>` 放檔），再照文法寫 `res.<seq>`（先寫 `.tmp` 再 rename）；看到 `done` 就停。
//! 不依賴任何 engine crate（test/boundary 檢查），文法照 `engine/plan` 的說明手寫。

use std::fs;
use std::path::{Path, PathBuf};
use std::thread::{self, JoinHandle};
use std::time::{Duration, Instant};

/// 等引擎的上限；超過就讓測試失敗，不無限等。
const TIMEOUT: Duration = Duration::from_secs(60);
const POLL: Duration = Duration::from_millis(5);

/// 一次測試的掛載點：`<prefix>/vk/root`、`<prefix>/vk/ctl`、`<prefix>/vk/in`。
pub struct Mounts {
    pub prefix: PathBuf,
    pub root: PathBuf,
    pub ctl: PathBuf,
    pub inbox: PathBuf,
}

impl Mounts {
    /// 在 `prefix` 底下建好三個目錄。
    pub fn create(prefix: &Path) -> Mounts {
        let m = Mounts {
            prefix: prefix.to_path_buf(),
            root: prefix.join("vk/root"),
            ctl: prefix.join("vk/ctl"),
            inbox: prefix.join("vk/in"),
        };
        for d in [&m.root, &m.ctl, &m.inbox] {
            fs::create_dir_all(d).unwrap_or_else(|e| panic!("{}: {e}", d.display()));
        }
        m
    }
}

/// 引擎送來的一個 request。
#[derive(Debug, Clone)]
pub struct Request {
    pub seq: u32,
    /// op 那一行原文，例如 `inspect ghcr.io/acme/tool:v1.2.0`。
    pub line: String,
    pub op: String,
    pub args: Vec<String>,
}

/// 啟動器回的 result 行：runner 以外的 op 回 `Ok`、`Failed`，runner 回 `Runner`。
pub enum Reply {
    Ok,
    Failed(u8),
    /// `runner` 之後那一段原文，例如 `exited 0`、`notstarted`、`stopped 130`、`stopped unavailable`。
    Runner(&'static str),
}

/// 假啟動器跑完後看到的東西。
#[derive(Debug, Clone)]
pub struct Seen {
    /// 每個 request 的 op 行，依序。
    pub requests: Vec<String>,
    /// `done` 的原文。
    pub done: Option<String>,
}

/// 在背景跑假啟動器，直到 `done` 出現或逾時。`header` 是 `vk-resolve/1 <run-id>`。
pub fn serve<F>(ctl: &Path, header: &str, mut handle: F) -> JoinHandle<Seen>
where
    F: FnMut(&Request) -> Reply + Send + 'static,
{
    let ctl = ctl.to_path_buf();
    let header = header.to_owned();
    thread::spawn(move || {
        let start = Instant::now();
        let mut seq = 1;
        let mut requests = Vec::new();
        loop {
            let req = ctl.join(format!("req.{seq}"));
            if let Ok(text) = fs::read_to_string(&req) {
                let request = parse(&text, &header, seq);
                requests.push(request.line.clone());
                let result = match handle(&request) {
                    Reply::Ok => "ok".to_owned(),
                    Reply::Failed(rc) => format!("failed {rc}"),
                    Reply::Runner(out) => format!("runner {out}"),
                };
                let res = ctl.join(format!("res.{seq}"));
                let tmp = ctl.join(format!("res.{seq}.tmp"));
                fs::write(&tmp, format!("{header} {seq}\n{result}\n")).unwrap();
                fs::rename(&tmp, &res).unwrap();
                seq += 1;
                continue;
            }
            if let Ok(done) = fs::read_to_string(ctl.join("done")) {
                return Seen {
                    requests,
                    done: Some(done),
                };
            }
            if start.elapsed() > TIMEOUT {
                return Seen {
                    requests,
                    done: None,
                };
            }
            thread::sleep(POLL);
        }
    })
}

fn parse(text: &str, header: &str, seq: u32) -> Request {
    let (first, rest) = text
        .split_once('\n')
        .unwrap_or_else(|| panic!("request {seq} has no LF: {text:?}"));
    assert_eq!(first, format!("{header} {seq}"), "request {seq} header");
    let line = rest
        .strip_suffix('\n')
        .unwrap_or_else(|| panic!("request {seq} does not end with LF: {text:?}"));
    assert!(
        !line.contains('\n'),
        "request {seq} has extra lines: {text:?}"
    );
    let mut words = line.split(' ').map(str::to_owned);
    let op = words.next().unwrap_or_default();
    Request {
        seq,
        line: line.to_owned(),
        op,
        args: words.collect(),
    }
}

/// `docker image inspect` 的輸出（只放引擎會讀的欄位，排版照 docker 的縮排 JSON）。
pub fn inspect_json(id: &str, repo_digests: &[&str]) -> String {
    let digests: Vec<String> = repo_digests.iter().map(|d| format!("\"{d}\"")).collect();
    format!(
        "[\n    {{\n        \"Id\": \"{id}\",\n        \"RepoTags\": [],\n        \"RepoDigests\": [{}],\n        \"Size\": 1024\n    }}\n]\n",
        digests.join(", ")
    )
}
