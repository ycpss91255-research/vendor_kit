//! 單元測試：以 std `TcpListener` 在 127.0.0.1 起假 registry，不連外網。
//! 涵蓋匿名與帶 token 的 token 交換、分頁、HEAD 取 digest 與 Accept、錯誤分類、重試與逾時。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::io::{BufRead, BufReader, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{Arc, Mutex};
use std::time::Duration;

use super::*;

const DIGEST: &str = "sha256:1111111111111111111111111111111111111111111111111111111111111111";
const PAT: &str = "ghp_secretvalue";

/// 假 registry 收到的請求。
#[derive(Debug, Clone)]
struct Req {
    method: String,
    target: String,
    headers: Vec<(String, String)>,
}

impl Req {
    fn header(&self, name: &str) -> Option<&str> {
        self.headers
            .iter()
            .find(|(k, _)| k.eq_ignore_ascii_case(name))
            .map(|(_, v)| v.as_str())
    }
}

/// 假 registry 的回應。
struct Resp {
    status: u16,
    headers: Vec<(String, String)>,
    body: String,
}

fn resp(status: u16, headers: &[(&str, &str)], body: &str) -> Resp {
    Resp {
        status,
        headers: headers
            .iter()
            .map(|(k, v)| ((*k).to_owned(), (*v).to_owned()))
            .collect(),
        body: body.to_owned(),
    }
}

struct Server {
    base: String,
    log: Arc<Mutex<Vec<Req>>>,
}

impl Server {
    fn start<F>(handler: F) -> Server
    where
        F: Fn(&Req, &str) -> Resp + Send + 'static,
    {
        let listener = TcpListener::bind("127.0.0.1:0").unwrap();
        let base = format!("http://{}", listener.local_addr().unwrap());
        let log = Arc::new(Mutex::new(Vec::new()));
        let log2 = Arc::clone(&log);
        let base2 = base.clone();
        std::thread::spawn(move || {
            for stream in listener.incoming() {
                let Ok(stream) = stream else { continue };
                if let Some(req) = read_request(&stream) {
                    log2.lock().unwrap().push(req.clone());
                    let r = handler(&req, &base2);
                    write_response(stream, &req, &r);
                }
            }
        });
        Server { base, log }
    }

    fn client(&self) -> Client {
        test_client(&self.base)
    }

    fn requests(&self) -> Vec<Req> {
        self.log.lock().unwrap().clone()
    }
}

fn test_client(base: &str) -> Client {
    let mut c = Client::with_base_url(base).unwrap();
    c.retry_delay = Duration::ZERO;
    c
}

fn read_request(stream: &TcpStream) -> Option<Req> {
    let mut reader = BufReader::new(stream);
    let mut line = String::new();
    reader.read_line(&mut line).ok()?;
    let mut parts = line.split_whitespace();
    let method = parts.next()?.to_owned();
    let target = parts.next()?.to_owned();
    let mut headers = Vec::new();
    loop {
        let mut h = String::new();
        reader.read_line(&mut h).ok()?;
        let h = h.trim_end();
        if h.is_empty() {
            break;
        }
        if let Some((k, v)) = h.split_once(':') {
            headers.push((k.trim().to_owned(), v.trim().to_owned()));
        }
    }
    Some(Req {
        method,
        target,
        headers,
    })
}

fn write_response(mut stream: TcpStream, req: &Req, r: &Resp) {
    let mut out = format!("HTTP/1.1 {} X\r\n", r.status);
    for (k, v) in &r.headers {
        out.push_str(&format!("{k}: {v}\r\n"));
    }
    let body = if req.method == "HEAD" { "" } else { &r.body };
    out.push_str(&format!(
        "Content-Length: {}\r\nConnection: close\r\n\r\n{body}",
        body.len()
    ));
    let _ = stream.write_all(out.as_bytes());
}

fn challenge(base: &str) -> String {
    format!(r#"Bearer realm="{base}/token",service="ghcr.io",scope="repository:acme/tool:pull""#)
}

/// GHCR 的樣子：沒帶 Bearer 回 401 加 challenge；/token 匿名給 `anon`，Basic 帶對 PAT 給 `pat`；
/// 帶 Bearer 時交給 `ok` 決定回應。
fn ghcr<F>(ok: F) -> Server
where
    F: Fn(&Req, &str) -> Resp + Send + 'static,
{
    Server::start(move |req, base| {
        if req.target.starts_with("/token") {
            return match req.header("authorization") {
                None => resp(200, &[], r#"{"token":"anon"}"#),
                Some(a)
                    if a == format!("Basic {}", base64(format!("{USERNAME}:{PAT}").as_bytes())) =>
                {
                    resp(200, &[], r#"{"token":"pat"}"#)
                }
                Some(_) => resp(401, &[], r#"{"errors":[{"code":"UNAUTHORIZED"}]}"#),
            };
        }
        match req.header("authorization") {
            Some(a) if a.starts_with("Bearer ") => ok(req, base),
            _ => resp(401, &[("WWW-Authenticate", &challenge(base))], ""),
        }
    })
}

fn tags_page(tags: &[&str]) -> String {
    serde_json::json!({"name": "acme/tool", "tags": tags}).to_string()
}

// ---- 列 tag ----

#[test]
fn anonymous_token_exchange_then_lists_tags() {
    let server = ghcr(|req, _| {
        assert_eq!(req.header("authorization"), Some("Bearer anon"));
        resp(200, &[], &tags_page(&["v1.0.0", "latest"]))
    });
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    assert_eq!(repo.tags().unwrap(), ["v1.0.0", "latest"]);

    let reqs = server.requests();
    assert_eq!(reqs.len(), 3);
    assert_eq!(
        reqs[0].target,
        format!("/v2/acme/tool/tags/list?n={PAGE_SIZE}")
    );
    assert_eq!(reqs[0].header("authorization"), None);
    assert_eq!(
        reqs[1].target,
        "/token?service=ghcr.io&scope=repository:acme/tool:pull"
    );
    assert_eq!(reqs[1].header("authorization"), None);
}

#[test]
fn token_is_exchanged_with_basic_auth() {
    let server = ghcr(|req, _| {
        assert_eq!(req.header("authorization"), Some("Bearer pat"));
        resp(200, &[], &tags_page(&["v2.0.0"]))
    });
    let client = server.client();
    let token = Token::new(&format!("  {PAT}\n")).unwrap();
    let mut repo = client
        .repository("ghcr.io/acme/tool", Some(&token))
        .unwrap();
    assert_eq!(repo.tags().unwrap(), ["v2.0.0"]);
    let token_req = &server.requests()[1];
    assert_eq!(
        token_req.header("authorization"),
        Some(format!("Basic {}", base64(format!("vendor_kit:{PAT}").as_bytes())).as_str())
    );
}

#[test]
fn follows_link_pagination_and_reuses_bearer() {
    let server = ghcr(|req, _| {
        if req.target.contains("last=v1.1.0") {
            resp(200, &[], &tags_page(&["v1.2.0"]))
        } else {
            resp(
                200,
                &[(
                    "Link",
                    r#"</v2/acme/tool/tags/list?last=v1.1.0&n=100>; rel="next""#,
                )],
                &tags_page(&["v1.0.0", "v1.1.0"]),
            )
        }
    });
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    assert_eq!(repo.tags().unwrap(), ["v1.0.0", "v1.1.0", "v1.2.0"]);
    let reqs = server.requests();
    // 401、token、第一頁、第二頁；第二頁直接帶已換到的 bearer。
    assert_eq!(reqs.len(), 4);
    assert_eq!(reqs[3].target, "/v2/acme/tool/tags/list?last=v1.1.0&n=100");
    assert_eq!(reqs[3].header("authorization"), Some("Bearer anon"));
}

#[test]
fn absolute_next_link_on_same_origin_is_followed() {
    let server = ghcr(|req, base| {
        if req.target.contains("last=") {
            resp(200, &[], &tags_page(&[]))
        } else {
            let link = format!(r#"<{base}/v2/acme/tool/tags/list?last=a>; rel="next""#);
            resp(200, &[("Link", &link)], &tags_page(&["a"]))
        }
    });
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    assert_eq!(repo.tags().unwrap(), ["a"]);
}

#[test]
fn next_link_to_another_origin_is_protocol_error() {
    let server = ghcr(|_, _| {
        resp(
            200,
            &[("Link", r#"<https://evil.example/v2/x?last=a>; rel="next""#)],
            &tags_page(&["a"]),
        )
    });
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    assert_eq!(repo.tags().unwrap_err().kind(), ErrorKind::Protocol);
}

#[test]
fn null_tags_is_empty_list() {
    let server = ghcr(|_, _| resp(200, &[], r#"{"name":"acme/tool","tags":null}"#));
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    assert!(repo.tags().unwrap().is_empty());
}

#[test]
fn invalid_tags_json_is_protocol_error() {
    let server = ghcr(|_, _| resp(200, &[], "not json"));
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    assert_eq!(repo.tags().unwrap_err().kind(), ErrorKind::Protocol);
}

// ---- manifest digest ----

#[test]
fn manifest_head_sends_index_accept_and_reads_digest() {
    let server = ghcr(|req, _| {
        assert_eq!(req.method, "HEAD");
        resp(
            200,
            &[
                ("Docker-Content-Digest", DIGEST),
                ("Content-Type", INDEX_MEDIA_TYPES[0]),
            ],
            "",
        )
    });
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    let tag = Tag::parse("v1.2.3").unwrap();
    let m = repo.manifest(&tag).unwrap();
    assert_eq!(m.digest.to_string(), DIGEST);
    assert_eq!(m.media_type.as_deref(), Some(INDEX_MEDIA_TYPES[0]));

    let reqs = server.requests();
    let last = reqs.last().unwrap();
    assert_eq!(last.target, "/v2/acme/tool/manifests/v1.2.3");
    let accept = last.header("accept").unwrap();
    for media in INDEX_MEDIA_TYPES {
        assert!(accept.contains(media), "{accept}");
    }
}

#[test]
fn manifest_without_or_with_bad_digest_is_protocol_error() {
    for headers in [vec![], vec![("Docker-Content-Digest", "sha256:abc")]] {
        let headers: Vec<(String, String)> = headers
            .into_iter()
            .map(|(k, v)| (k.to_owned(), v.to_owned()))
            .collect();
        let server = ghcr(move |_, _| Resp {
            status: 200,
            headers: headers.clone(),
            body: String::new(),
        });
        let client = server.client();
        let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
        let err = repo.manifest(&Tag::parse("v1.0.0").unwrap()).unwrap_err();
        assert_eq!(err.kind(), ErrorKind::Protocol);
    }
}

#[test]
fn missing_manifest_is_not_found() {
    let server = ghcr(|_, _| resp(404, &[], ""));
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    let err = repo.manifest(&Tag::parse("v9.9.9").unwrap()).unwrap_err();
    assert_eq!(err.kind(), ErrorKind::NotFound);
}

// ---- 認證錯誤 ----

#[test]
fn denied_without_token_is_auth_required() {
    for status in [401, 403] {
        let server = ghcr(move |_, _| resp(status, &[], ""));
        let client = server.client();
        let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
        assert_eq!(repo.tags().unwrap_err().kind(), ErrorKind::AuthRequired);
    }
}

#[test]
fn rejected_token_is_not_retried_anonymously() {
    let server = ghcr(|_, _| resp(200, &[], &tags_page(&["v1.0.0"])));
    let client = server.client();
    let token = Token::new("wrong").unwrap();
    let mut repo = client
        .repository("ghcr.io/acme/tool", Some(&token))
        .unwrap();
    let err = repo.tags().unwrap_err();
    assert_eq!(err.kind(), ErrorKind::TokenRejected);
    // 401 challenge 與一次帶 Basic 的換 token；沒有匿名的換 token、沒有再送資源請求。
    let reqs = server.requests();
    assert_eq!(reqs.len(), 2);
    assert!(
        reqs[1]
            .header("authorization")
            .unwrap()
            .starts_with("Basic ")
    );
}

#[test]
fn token_accepted_by_exchange_but_denied_by_resource_is_rejected() {
    let server = ghcr(|_, _| resp(403, &[], ""));
    let client = server.client();
    let token = Token::new(PAT).unwrap();
    let mut repo = client
        .repository("ghcr.io/acme/tool", Some(&token))
        .unwrap();
    assert_eq!(repo.tags().unwrap_err().kind(), ErrorKind::TokenRejected);
}

#[test]
fn anonymous_exchange_denied_is_auth_required() {
    let server = Server::start(|req, base| {
        if req.target.starts_with("/token") {
            resp(401, &[], "")
        } else {
            resp(401, &[("WWW-Authenticate", &challenge(base))], "")
        }
    });
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    assert_eq!(repo.tags().unwrap_err().kind(), ErrorKind::AuthRequired);
}

#[test]
fn realm_on_another_origin_gets_no_token() {
    let server = Server::start(|_, _| {
        resp(
            401,
            &[(
                "WWW-Authenticate",
                r#"Bearer realm="https://evil.example/token",service="ghcr.io""#,
            )],
            "",
        )
    });
    let client = server.client();
    let token = Token::new(PAT).unwrap();
    let mut repo = client
        .repository("ghcr.io/acme/tool", Some(&token))
        .unwrap();
    assert_eq!(repo.tags().unwrap_err().kind(), ErrorKind::Protocol);
    assert_eq!(server.requests().len(), 1);
}

#[test]
fn unauthorized_without_challenge_is_protocol_error() {
    let server = Server::start(|_, _| resp(401, &[], ""));
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    assert_eq!(repo.tags().unwrap_err().kind(), ErrorKind::Protocol);
}

#[test]
fn default_scope_when_challenge_has_none() {
    let server = Server::start(|req, base| {
        if req.target.starts_with("/token") {
            return resp(200, &[], r#"{"access_token":"t"}"#);
        }
        match req.header("authorization") {
            Some("Bearer t") => resp(200, &[], &tags_page(&[])),
            _ => {
                let c = format!(r#"Bearer realm="{base}/token""#);
                resp(401, &[("WWW-Authenticate", &c)], "")
            }
        }
    });
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    assert!(repo.tags().unwrap().is_empty());
    assert_eq!(
        server.requests()[1].target,
        "/token?scope=repository:acme/tool:pull"
    );
}

// ---- 網路與重試 ----

#[test]
fn server_errors_are_retried_then_network() {
    let server = ghcr(|_, _| resp(503, &[], ""));
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    assert_eq!(repo.tags().unwrap_err().kind(), ErrorKind::Network);
    // 401 challenge、換 token，接著資源請求試 ATTEMPTS 次。
    assert_eq!(server.requests().len(), 2 + ATTEMPTS as usize);
}

#[test]
fn transient_error_recovers_on_retry() {
    let count = Arc::new(Mutex::new(0));
    let count2 = Arc::clone(&count);
    let server = ghcr(move |_, _| {
        let mut n = count2.lock().unwrap();
        *n += 1;
        if *n == 1 {
            resp(429, &[], "")
        } else {
            resp(200, &[], &tags_page(&["v1.0.0"]))
        }
    });
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    assert_eq!(repo.tags().unwrap(), ["v1.0.0"]);
}

#[test]
fn not_found_is_not_retried() {
    let server = ghcr(|_, _| resp(404, &[], ""));
    let client = server.client();
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    assert_eq!(repo.tags().unwrap_err().kind(), ErrorKind::NotFound);
    assert_eq!(server.requests().len(), 3);
}

#[test]
fn connection_refused_is_network() {
    let base = {
        let l = TcpListener::bind("127.0.0.1:0").unwrap();
        format!("http://{}", l.local_addr().unwrap())
    };
    let client = test_client(&base);
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    assert_eq!(repo.tags().unwrap_err().kind(), ErrorKind::Network);
}

#[test]
fn timeout_is_network() {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let base = format!("http://{}", listener.local_addr().unwrap());
    // 收下連線但永遠不回。
    std::thread::spawn(move || {
        let mut held = Vec::new();
        for s in listener.incoming() {
            held.push(s);
        }
    });
    let mut client = Client::build(base, Duration::from_millis(200), Duration::ZERO);
    client.attempts = 2;
    let mut repo = client.repository("ghcr.io/acme/tool", None).unwrap();
    let err = repo.tags().unwrap_err();
    assert_eq!(err.kind(), ErrorKind::Network);
    assert!(err.detail().contains("2 attempts"), "{err}");
}

// ---- 輸入與小工具 ----

#[test]
fn only_ghcr_images_are_accepted() {
    let client = test_client("http://127.0.0.1:1");
    for image in [
        "docker.io/acme/tool",
        "acme/tool",
        "tool",
        "ghcr.io/Acme/tool",
        "ghcr.io/",
    ] {
        let err = client.repository(image, None).unwrap_err();
        assert_eq!(err.kind(), ErrorKind::Protocol, "{image}");
    }
    assert!(client.repository("ghcr.io/acme/sub/tool", None).is_ok());
}

#[test]
fn base_url_must_be_scheme_and_host() {
    assert!(Client::with_base_url("http://127.0.0.1:5000").is_ok());
    assert!(Client::with_base_url("https://ghcr.io/").is_ok());
    for bad in [
        "ghcr.io",
        "ftp://ghcr.io",
        "https://",
        "https://ghcr.io/v2",
        "https://u@h",
    ] {
        assert!(Client::with_base_url(bad).is_err(), "{bad}");
    }
    assert_eq!(Client::new().base, BASE_URL);
}

#[test]
fn token_is_never_printed() {
    let token = Token::new(PAT).unwrap();
    assert!(!format!("{token:?}").contains(PAT));
    assert!(Token::new(" \n").is_none());

    let server = ghcr(|_, _| resp(403, &[], ""));
    let client = server.client();
    let mut repo = client
        .repository("ghcr.io/acme/tool", Some(&token))
        .unwrap();
    let err = repo.tags().unwrap_err();
    let debug = format!("{repo:?}");
    assert!(!debug.contains(PAT) && !debug.contains("pat\""), "{debug}");
    assert!(!format!("{err} {err:?}").contains(PAT));
}

#[test]
fn base64_matches_rfc4648_vectors() {
    for (input, want) in [
        ("", ""),
        ("f", "Zg=="),
        ("fo", "Zm8="),
        ("foo", "Zm9v"),
        ("foob", "Zm9vYg=="),
        ("fooba", "Zm9vYmE="),
        ("foobar", "Zm9vYmFy"),
    ] {
        assert_eq!(base64(input.as_bytes()), want);
    }
}

#[test]
fn challenge_parsing() {
    assert_eq!(
        parse_challenge(
            r#"Bearer realm="https://ghcr.io/token",service="ghcr.io",scope="repository:a/b:pull""#
        ),
        Some(Challenge {
            realm: "https://ghcr.io/token".into(),
            service: Some("ghcr.io".into()),
            scope: Some("repository:a/b:pull".into()),
        })
    );
    assert_eq!(parse_challenge(r#"Basic realm="x""#), None);
    assert_eq!(parse_challenge(r#"Bearer service="x""#), None);
}

#[test]
fn link_parsing() {
    assert_eq!(
        next_link(r#"</v2/a/tags/list?last=x>; rel="next""#).unwrap(),
        Some("/v2/a/tags/list?last=x".into())
    );
    assert_eq!(next_link(r#"</v2/a>; rel="prev""#).unwrap(), None);
    assert!(next_link("<broken").is_err());
}
