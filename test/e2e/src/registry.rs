//! 假的 registry：在 127.0.0.1 起 std `TcpListener`，照 GHCR 的 token 認證回應 `tags/list` 與 HEAD
//! manifest，不連外網。
//!
//! - 沒帶 Bearer 的請求回 401 加 `WWW-Authenticate: Bearer realm=<base>/token,…`。
//! - `/token`：匿名給 `anon`；Basic 認證帶 [`GOOD_TOKEN`] 給 `pat`；其他 Basic 回 401。
//! - `/v2/<路徑>/tags/list`：依 [`Repo`] 回 tag；沒列的路徑回 404。
//! - `HEAD /v2/<路徑>/manifests/<tag>`：依 [`Registry::start_with`] 給的 digest 回 `Docker-Content-Digest`
//!   （認證跟同一個路徑的 `tags/list` 一樣）；沒給的 tag 或路徑回 404。
//!
//! 不依賴任何 engine crate（test/boundary 檢查），協定照 engine/registry 的說明手寫。

use std::collections::BTreeMap;
use std::io::{BufRead, BufReader, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{Arc, Mutex};
use std::thread;

/// 假 registry 認得的 PAT；其他 token 一律拒絕。
pub const GOOD_TOKEN: &str = "good";
/// 帶 [`GOOD_TOKEN`] 換 bearer 時的 Basic 認證：`base64("vendor_kit:good")`（帳號是 engine/registry 的 `USERNAME`）。
const GOOD_BASIC: &str = "Basic dmVuZG9yX2tpdDpnb29k";

/// 一個 image 路徑。
#[derive(Debug, Clone)]
pub enum Repo {
    /// 匿名就能列。
    Public(Vec<String>),
    /// 要帶 [`GOOD_TOKEN`] 才能列；匿名回 403。
    Private(Vec<String>),
}

impl Repo {
    pub fn public(tags: &[&str]) -> Repo {
        Repo::Public(tags.iter().map(|t| (*t).to_owned()).collect())
    }

    pub fn private(tags: &[&str]) -> Repo {
        Repo::Private(tags.iter().map(|t| (*t).to_owned()).collect())
    }
}

/// 背景跑著的假 registry。
pub struct Registry {
    base: String,
    log: Arc<Mutex<Vec<String>>>,
}

impl Registry {
    /// 起一個假 registry；`repos` 是 `(路徑, 內容)`，路徑不含 `ghcr.io/`。
    pub fn start(repos: &[(&str, Repo)]) -> Registry {
        Registry::start_with(repos, &[])
    }

    /// 同 [`Registry::start`]，另給 tag 指向的 digest：`(路徑, tag, digest)`。
    pub fn start_with(repos: &[(&str, Repo)], digests: &[(&str, &str, &str)]) -> Registry {
        let repos: BTreeMap<String, Repo> = repos
            .iter()
            .map(|(p, r)| ((*p).to_owned(), r.clone()))
            .collect();
        let digests: BTreeMap<(String, String), String> = digests
            .iter()
            .map(|(p, t, d)| (((*p).to_owned(), (*t).to_owned()), (*d).to_owned()))
            .collect();
        let listener = TcpListener::bind("127.0.0.1:0").unwrap();
        let base = format!("http://{}", listener.local_addr().unwrap());
        let log = Arc::new(Mutex::new(Vec::new()));
        let (log2, base2) = (Arc::clone(&log), base.clone());
        thread::spawn(move || {
            for stream in listener.incoming() {
                let Ok(stream) = stream else { continue };
                let Some((line, auth)) = read_request(&stream) else {
                    continue;
                };
                log2.lock().unwrap().push(line.clone());
                let (status, header, body) =
                    respond(&repos, &digests, &base2, &line, auth.as_deref());
                let body = if line.starts_with("HEAD ") { "" } else { &body };
                write_response(stream, status, header.as_deref(), body);
            }
        });
        Registry { base, log }
    }

    /// 給 [`crate::REGISTRY_URL_ENV`] 的 base URL。
    pub fn base(&self) -> &str {
        &self.base
    }

    /// 收到的請求（`<方法> <目標>`），依序。
    pub fn requests(&self) -> Vec<String> {
        self.log.lock().unwrap().clone()
    }
}

fn respond(
    repos: &BTreeMap<String, Repo>,
    digests: &BTreeMap<(String, String), String>,
    base: &str,
    line: &str,
    auth: Option<&str>,
) -> (u16, Option<String>, String) {
    let target = line.split(' ').nth(1).unwrap_or("");
    if target.starts_with("/token") {
        return match auth {
            None => (200, None, r#"{"token":"anon"}"#.to_owned()),
            Some(GOOD_BASIC) => (200, None, r#"{"token":"pat"}"#.to_owned()),
            Some(_) => (401, None, String::new()),
        };
    }
    let rest = target.strip_prefix("/v2/").unwrap_or("");
    let (path, tag) = if let Some((p, _)) = rest.split_once("/tags/list") {
        (p, None)
    } else if let Some((p, t)) = rest.split_once("/manifests/") {
        (p, Some(t))
    } else {
        return (404, None, String::new());
    };
    let Some(bearer) = auth.and_then(|a| a.strip_prefix("Bearer ")) else {
        let challenge = format!(
            r#"WWW-Authenticate: Bearer realm="{base}/token",service="ghcr.io",scope="repository:{path}:pull""#
        );
        return (401, Some(challenge), String::new());
    };
    let tags = match repos.get(path) {
        None => return (404, None, String::new()),
        Some(Repo::Public(tags)) => tags,
        Some(Repo::Private(tags)) if bearer == "pat" => tags,
        Some(Repo::Private(_)) => return (403, None, String::new()),
    };
    if let Some(tag) = tag {
        return match digests.get(&(path.to_owned(), tag.to_owned())) {
            Some(d) => (
                200,
                Some(format!("Docker-Content-Digest: {d}")),
                String::new(),
            ),
            None => (404, None, String::new()),
        };
    }
    let list: Vec<String> = tags.iter().map(|t| format!("\"{t}\"")).collect();
    let body = format!(r#"{{"name":"{path}","tags":[{}]}}"#, list.join(","));
    (200, None, body)
}

/// 讀一個請求：請求行（`<方法> <目標>`）與 `Authorization`。
fn read_request(stream: &TcpStream) -> Option<(String, Option<String>)> {
    let mut reader = BufReader::new(stream);
    let mut line = String::new();
    reader.read_line(&mut line).ok()?;
    let mut auth = None;
    loop {
        let mut h = String::new();
        reader.read_line(&mut h).ok()?;
        let h = h.trim_end();
        if h.is_empty() {
            break;
        }
        if let Some((k, v)) = h.split_once(':')
            && k.trim().eq_ignore_ascii_case("authorization")
        {
            auth = Some(v.trim().to_owned());
        }
    }
    let mut parts = line.split_whitespace();
    let request = format!("{} {}", parts.next()?, parts.next()?);
    Some((request, auth))
}

fn write_response(mut stream: TcpStream, status: u16, header: Option<&str>, body: &str) {
    let mut out = format!("HTTP/1.1 {status} X\r\n");
    if let Some(h) = header {
        out.push_str(h);
        out.push_str("\r\n");
    }
    out.push_str(&format!(
        "Content-Length: {}\r\nConnection: close\r\n\r\n{body}",
        body.len()
    ));
    let _ = stream.write_all(out.as_bytes());
}
