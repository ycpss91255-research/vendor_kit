//! 線上解析（模組說明「線上解析」「registry token 檔」「查詢失敗」）：假 registry 回 `tags/list` 與 HEAD
//! manifest，假啟動器回 inspect、pull、extract、`stage`。

use std::collections::BTreeMap;
use std::io::BufReader;
use std::net::{TcpListener, TcpStream};

use super::*;

/// 假 registry 認得的 PAT；其他 token 一律拒絕。
const GOOD_TOKEN: &str = "good";
/// 帶 [`GOOD_TOKEN`] 換 bearer 時的 Basic 認證：`base64("vendor_kit:good")`（帳號是 `registry::USERNAME`）。
const GOOD_BASIC: &str = "Basic dmVuZG9yX2tpdDpnb29k";
/// 跟 [`DIGEST`] 不同的 digest。
const OTHER_DIGEST: &str =
    "sha256:5555555555555555555555555555555555555555555555555555555555555555";
const OCI_INDEX: &str = "application/vnd.oci.image.index.v1+json";

/// 假 registry 裡的一個 image 路徑：tag 清單、每個 tag 指向的 digest、要不要 [`GOOD_TOKEN`]。
#[derive(Clone)]
pub(super) struct Repo {
    tags: Vec<&'static str>,
    digests: Vec<(&'static str, &'static str)>,
    pub(super) private: bool,
}

/// `acme/tool` 公開，列出 `tags`，每個 `vX.Y.Z` 都指向 [`DIGEST`]。
pub(super) fn public(tags: &[&'static str]) -> Repo {
    Repo {
        tags: tags.to_vec(),
        digests: tags.iter().map(|t| (*t, DIGEST)).collect(),
        private: false,
    }
}

/// GHCR 的樣子（token 認證）：沒帶 Bearer 回 401 加 challenge；`/token` 匿名給 `anon`，Basic 帶
/// [`GOOD_TOKEN`] 給 `pat`，其他 Basic 回 401；`tags/list` 與 HEAD `manifests/<tag>` 依 [`Repo`] 回，私有的
/// 匿名回 403，沒列的路徑或 tag 回 404。
pub(super) struct Registry {
    base: String,
    /// 收到的請求（`<方法> <目標>`）與有沒有帶 Bearer，依序。
    log: Arc<Mutex<Vec<(String, bool)>>>,
}

impl Registry {
    pub(super) fn start(path: &str, repo: Repo) -> Registry {
        let repos: BTreeMap<String, Repo> = [(path.to_owned(), repo)].into_iter().collect();
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
                let bearer = auth.as_deref().is_some_and(|a| a.starts_with("Bearer "));
                log2.lock().unwrap().push((line.clone(), bearer));
                let (status, headers) = respond(&repos, &base2, &line, auth.as_deref());
                write_response(stream, &line, status, &headers);
            }
        });
        Registry { base, log }
    }

    pub(super) fn client(&self) -> Client {
        Client::with_base_url(&self.base).unwrap()
    }

    /// 帶 Bearer 的請求（`<方法> <目標>`）：不含第一次沒帶認證被回 401 的那一次，也不含換 token 的 `/token`。
    pub(super) fn requests(&self) -> Vec<String> {
        let log = self.log.lock().unwrap();
        log.iter()
            .filter(|(_, bearer)| *bearer)
            .map(|(l, _)| l.clone())
            .collect()
    }

    /// 換 token（`/token`）的次數。
    fn token_exchanges(&self) -> usize {
        let log = self.log.lock().unwrap();
        log.iter().filter(|(l, _)| l.contains(" /token")).count()
    }
}

/// 回 (狀態碼, 標頭與 body)；body 放在 `"body"` 鍵。
fn respond(
    repos: &BTreeMap<String, Repo>,
    base: &str,
    line: &str,
    auth: Option<&str>,
) -> (u16, Vec<(String, String)>) {
    let target = line.split(' ').nth(1).unwrap_or("");
    let body = |s: String| vec![("body".to_owned(), s)];
    if target.starts_with("/token") {
        return match auth {
            None => (200, body(r#"{"token":"anon"}"#.to_owned())),
            Some(GOOD_BASIC) => (200, body(r#"{"token":"pat"}"#.to_owned())),
            Some(_) => (401, vec![]),
        };
    }
    let Some(rest) = target.strip_prefix("/v2/") else {
        return (404, vec![]);
    };
    let (path, what) = if let Some((p, _)) = rest.split_once("/tags/list") {
        (p, None)
    } else if let Some((p, tag)) = rest.split_once("/manifests/") {
        (p, Some(tag))
    } else {
        return (404, vec![]);
    };
    let Some(bearer) = auth.and_then(|a| a.strip_prefix("Bearer ")) else {
        let challenge = format!(
            r#"Bearer realm="{base}/token",service="ghcr.io",scope="repository:{path}:pull""#
        );
        return (401, vec![("WWW-Authenticate".to_owned(), challenge)]);
    };
    let Some(repo) = repos.get(path) else {
        return (404, vec![]);
    };
    if repo.private && bearer != "pat" {
        return (403, vec![]);
    }
    match what {
        None => {
            let list: Vec<String> = repo.tags.iter().map(|t| format!("\"{t}\"")).collect();
            let json = format!(r#"{{"name":"{path}","tags":[{}]}}"#, list.join(","));
            (200, body(json))
        }
        Some(tag) => match repo.digests.iter().find(|(t, _)| *t == tag) {
            Some((_, digest)) => (
                200,
                vec![
                    ("Docker-Content-Digest".to_owned(), (*digest).to_owned()),
                    ("Content-Type".to_owned(), OCI_INDEX.to_owned()),
                ],
            ),
            None => (404, vec![]),
        },
    }
}

/// 讀一個請求：請求行與 `Authorization`。
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

/// 寫回應；HEAD 只寫標頭、不寫 body。
fn write_response(mut stream: TcpStream, line: &str, status: u16, headers: &[(String, String)]) {
    let mut out = format!("HTTP/1.1 {status} X\r\n");
    let mut body = String::new();
    for (k, v) in headers {
        if k == "body" {
            body = v.clone();
        } else {
            out.push_str(&format!("{k}: {v}\r\n"));
        }
    }
    out.push_str(&format!(
        "Content-Length: {}\r\nConnection: close\r\n\r\n",
        body.len()
    ));
    if !line.starts_with("HEAD ") {
        out.push_str(&body);
    }
    let _ = stream.write_all(out.as_bytes());
}

fn run(fx: &Fx, argv: &[&str], registry: &Registry, token_file: Option<&str>) -> Out {
    let client = registry.client();
    let online = Online {
        registry: &client,
        token_file,
    };
    run_online(fx, argv, Vec::new(), tty(false), "", &online)
}

const TAGS_LIST: &str = "GET /v2/acme/tool/tags/list?n=100";

fn manifest(tag: &str) -> String {
    format!("HEAD /v2/acme/tool/manifests/{tag}")
}

fn pinned() -> String {
    format!("ghcr.io/acme/tool@{DIGEST}")
}

/// 不在本機：先 inspect `<路徑>:<tag>` 失敗，pull 與 inspect 都用 `<路徑>@<digest>`。
fn pulled_requests() -> [String; 4] {
    [
        format!("inspect {NEW_REF}"),
        format!("pull {}", pinned()),
        format!("inspect {}", pinned()),
        format!("extract {IMAGE_ID} tool1"),
    ]
}

const NOT_LOCAL: Script = Script {
    local: false,
    ..NEW
};

// ---- 不帶 tag：列 tag 取最新版 ----

#[test]
fn without_a_tag_the_latest_local_version_is_checked_against_the_registry_digest() {
    let fx = Fx::new();
    let registry = Registry::start(
        "acme/tool",
        public(&["v1.0.0", "v1.2.0", "v1.1.9", "latest"]),
    );
    let peer = Peer::start(&fx, NEW);
    let out = run(&fx, &["upgrade", "tool"], &registry, None);
    assert_eq!(
        peer.finish(),
        [
            format!("inspect {NEW_REF}"),
            format!("extract {IMAGE_ID} tool1")
        ]
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, upgraded_line());
    assert_eq!(out.stderr, "");
    assert_eq!(
        registry.requests(),
        [TAGS_LIST.to_owned(), manifest("v1.2.0")]
    );
    assert_landed(&fx);
}

#[test]
fn without_a_tag_a_version_not_in_the_local_store_is_pulled_by_digest() {
    let fx = Fx::new();
    let registry = Registry::start("acme/tool", public(&["v1.0.0", "v1.2.0"]));
    let peer = Peer::start(&fx, NOT_LOCAL);
    let out = run(&fx, &["upgrade", "tool"], &registry, None);
    assert_eq!(peer.finish(), pulled_requests());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, upgraded_line());
    assert_eq!(
        registry.requests(),
        [TAGS_LIST.to_owned(), manifest("v1.2.0")]
    );
    assert_landed(&fx);
}

#[test]
fn without_a_tag_already_at_the_latest_version_is_unchanged() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let registry = Registry::start("acme/tool", public(&["v0.9.0", "v1.0.0"]));
    let peer = Peer::start(&fx, NEW);
    let out = run(&fx, &["upgrade", "tool"], &registry, None);
    assert!(peer.finish().is_empty());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "tool is already at v1.0.0; no changes were made.\n"
    );
    assert_eq!(out.stderr, "");
    // 同一 tag 改指別的 digest 不算新版：不查 digest。
    assert_eq!(registry.requests(), [TAGS_LIST]);
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn without_a_tag_a_latest_version_older_than_the_lock_line_is_a_gap() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let registry = Registry::start("acme/tool", public(&["v0.9.0"]));
    let peer = Peer::start(&fx, NEW);
    let out = run(&fx, &["upgrade", "tool"], &registry, None);
    assert!(peer.finish().is_empty());
    assert_gap(&out, "the latest version in the registry (v0.9.0) is older");
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn local_digest_different_from_the_registry_is_rejected_before_any_write() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let mut repo = public(&["v1.2.0"]);
    repo.digests = vec![("v1.2.0", OTHER_DIGEST)];
    let registry = Registry::start("acme/tool", repo);
    let peer = Peer::start(&fx, NEW);
    let out = run(&fx, &["upgrade", "tool"], &registry, None);
    assert_eq!(peer.finish(), [format!("inspect {NEW_REF}")]);
    assert_gap(
        &out,
        &format!(
            "{NEW_REF} points to more than one digest ({DIGEST}, {OTHER_DIGEST}); {DRAFT_TAG_DIGESTS}"
        ),
    );
    assert_eq!(fx.snapshot(), before);
}

// ---- 查詢失敗 ----

#[test]
fn private_tags_without_a_token_file_is_vk0001() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let mut repo = public(&["v1.2.0"]);
    repo.private = true;
    let registry = Registry::start("acme/tool", repo);
    let peer = Peer::start(&fx, NEW);
    let out = run(&fx, &["upgrade", "tool"], &registry, None);
    assert!(peer.finish().is_empty());
    assert_eq!(out.code, 2);
    assert!(
        out.stderr.starts_with(
            "vendor_kit: error[VK0001]: Cannot list versions for tool: registry read access is required"
        ),
        "{}",
        out.stderr
    );
    assert!(
        out.stderr.contains("just vendor_kit upgrade tool@<tag>"),
        "{}",
        out.stderr
    );
    assert_eq!(out.stdout, "");
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn a_token_file_inside_the_install_dir_is_read_and_reused_for_the_digest() {
    let fx = Fx::new();
    fs::create_dir_all(fx.root().join("secrets")).unwrap();
    fs::write(fx.root().join("secrets/ghcr"), format!(" {GOOD_TOKEN}\n")).unwrap();
    let mut repo = public(&["v1.2.0"]);
    repo.private = true;
    let registry = Registry::start("acme/tool", repo);
    let peer = Peer::start(&fx, NOT_LOCAL);
    let out = run(&fx, &["upgrade", "tool"], &registry, Some("secrets/ghcr"));
    assert_eq!(peer.finish(), pulled_requests());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        registry.requests(),
        [TAGS_LIST.to_owned(), manifest("v1.2.0")]
    );
    // 換一次 token，取 digest 沿用同一個 bearer。
    assert_eq!(registry.token_exchanges(), 1);
    assert_landed(&fx);
}

#[test]
fn a_token_file_outside_the_install_dir_is_staged() {
    let fx = Fx::new();
    fs::create_dir_all(fx.host().join("home")).unwrap();
    fs::write(fx.host().join("home/ghcr"), GOOD_TOKEN).unwrap();
    let mut repo = public(&["v1.2.0"]);
    repo.private = true;
    let registry = Registry::start("acme/tool", repo);
    let peer = Peer::start(&fx, NEW);
    let out = run(&fx, &["upgrade", "tool"], &registry, Some("/h/home/ghcr"));
    assert_eq!(
        peer.finish(),
        [
            "stage e:/h/home/ghcr token".to_owned(),
            format!("inspect {NEW_REF}"),
            format!("extract {IMAGE_ID} tool1"),
        ]
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_landed(&fx);
}

#[test]
fn an_unreadable_or_empty_token_file_is_vk0055_before_contacting_the_registry() {
    let fx = Fx::new();
    fs::write(fx.root().join("empty"), " \n").unwrap();
    let before = fx.snapshot();
    let registry = Registry::start("acme/tool", public(&["v1.2.0"]));
    for (given, reason, ops) in [
        ("empty", "the registry token file is empty", 0),
        ("missing", "cannot read the registry token file: ", 0),
        (
            "/h/nowhere",
            "the launcher could not copy the registry token file (exit 1)",
            1,
        ),
    ] {
        let peer = Peer::start(&fx, NEW);
        let out = run(&fx, &["upgrade", "tool"], &registry, Some(given));
        assert_eq!(peer.finish().len(), ops, "{given}");
        assert_eq!(out.code, 2, "{given}");
        assert!(
            out.stderr.starts_with(&format!(
                "vendor_kit: error[VK0055]: Cannot access {given} for tool: {reason}"
            )),
            "{given}: {}",
            out.stderr
        );
        assert_eq!(fx.snapshot(), before);
    }
    assert!(registry.log.lock().unwrap().is_empty());
}

#[test]
fn a_tag_given_never_reads_the_token_file() {
    let fx = Fx::new();
    let registry = Registry::start("acme/tool", public(&["v1.2.0"]));
    let peer = Peer::start(&fx, NOT_LOCAL);
    let out = run(&fx, &UPGRADE, &registry, Some("/h/nowhere"));
    assert_eq!(peer.finish(), pulled_requests());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_landed(&fx);
}

#[test]
fn tags_that_are_not_versions_are_vk0058_and_no_tags_is_vk0055() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let registry = Registry::start("acme/tool", public(&["latest", "v1.2"]));
    let peer = Peer::start(&fx, NEW);
    let out = run(&fx, &["upgrade", "tool"], &registry, None);
    assert!(peer.finish().is_empty());
    assert_eq!(out.code, 2);
    assert!(
        out.stderr
            .starts_with("vendor_kit: error[VK0058]: Cannot determine the latest version of tool"),
        "{}",
        out.stderr
    );

    let registry = Registry::start("acme/tool", public(&[]));
    let peer = Peer::start(&fx, NEW);
    let out = run(&fx, &["upgrade", "tool"], &registry, None);
    assert!(peer.finish().is_empty());
    assert!(
        out.stderr.starts_with(
            "vendor_kit: error[VK0055]: Cannot access ghcr.io/acme/tool for tool: the registry lists no tags"
        ),
        "{}",
        out.stderr
    );
    assert_eq!(fx.snapshot(), before);
}

// ---- `@<tag>` ----

#[test]
fn a_tag_not_in_the_local_store_is_pulled_by_digest_without_listing() {
    let fx = Fx::new();
    let registry = Registry::start("acme/tool", public(&["v1.2.0"]));
    let peer = Peer::start(&fx, NOT_LOCAL);
    let out = run(&fx, &UPGRADE, &registry, None);
    assert_eq!(peer.finish(), pulled_requests());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, upgraded_line());
    assert_eq!(registry.requests(), [manifest("v1.2.0")]);
    assert_landed(&fx);
}

#[test]
fn a_local_tag_does_not_contact_the_registry() {
    let fx = Fx::new();
    let peer = Peer::start(&fx, NEW);
    // registry 是連不到的位址：連了就會失敗。
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    peer.finish();
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_landed(&fx);
}

#[test]
fn a_tag_missing_from_the_registry_is_vk0055() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let registry = Registry::start("acme/tool", public(&["v1.0.0"]));
    let peer = Peer::start(&fx, NOT_LOCAL);
    let out = run(&fx, &UPGRADE, &registry, None);
    assert_eq!(peer.finish(), [format!("inspect {NEW_REF}")]);
    assert_eq!(out.code, 2);
    assert!(
        out.stderr.starts_with(&format!(
            "vendor_kit: error[VK0055]: Cannot access {NEW_REF} for tool: "
        )),
        "{}",
        out.stderr
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn a_failed_pull_is_vk0055() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let registry = Registry::start("acme/tool", public(&["v1.2.0"]));
    let peer = Peer::start(
        &fx,
        Script {
            fail: Some("pull"),
            ..NOT_LOCAL
        },
    );
    let out = run(&fx, &UPGRADE, &registry, None);
    assert_eq!(
        peer.finish(),
        [format!("inspect {NEW_REF}"), format!("pull {}", pinned())]
    );
    assert_eq!(out.code, 2);
    assert!(
        out.stderr.starts_with(&format!(
            "vendor_kit: error[VK0055]: Cannot access {NEW_REF}@{DIGEST} for tool: docker pull exited with 1"
        )),
        "{}",
        out.stderr
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn a_local_image_without_a_repo_digest_is_vk0031() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let peer = Peer::start(
        &fx,
        Script {
            digests: &[
                "ghcr.io/acme/other@sha256:2222222222222222222222222222222222222222222222222222222222222222",
            ],
            ..NEW
        },
    );
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert_eq!(peer.finish(), [format!("inspect {NEW_REF}")]);
    assert_eq!(out.code, 2);
    assert!(
        out.stderr.starts_with(&format!(
            "vendor_kit: error[VK0031]: Cannot use image {NEW_REF}: required digest information is missing. The supplied image was not used."
        )),
        "{}",
        out.stderr
    );
    assert_eq!(out.stdout, "");
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn a_local_image_with_two_digests_for_the_tag_is_rejected() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let peer = Peer::start(
        &fx,
        Script {
            digests: &[
                "ghcr.io/acme/tool@sha256:2222222222222222222222222222222222222222222222222222222222222222",
                "ghcr.io/acme/tool@sha256:5555555555555555555555555555555555555555555555555555555555555555",
            ],
            ..NEW
        },
    );
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    peer.finish();
    assert_gap(
        &out,
        &format!("{NEW_REF} points to more than one digest ({DIGEST}, {OTHER_DIGEST})"),
    );
    assert!(out.stderr.contains(DRAFT_TAG_DIGESTS), "{}", out.stderr);
    assert_eq!(fx.snapshot(), before);
}
