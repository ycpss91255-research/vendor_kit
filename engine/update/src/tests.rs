//! 單元測試：直接在暫存的安裝目錄跑 `update`。驗查詢前的停下點（殘留進度、VK0046、檔案版過高）、
//! 本機覆寫提醒、向假 registry 列 tag 印結果行與各種查詢失敗、token 檔的讀法（安裝目錄裡直接讀、外面經
//! `stage`），以及每個情況都不動任何檔；另驗結果行格式、`<original_command>` 的重組與 token 路徑的判定。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::collections::BTreeMap;
use std::ffi::OsString;
use std::io::{self, BufRead, BufReader};
use std::net::{TcpListener, TcpStream};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};
use std::thread::{self, JoinHandle};

use diagnostics::NoSink;
use plan::{Header, RunId};
use progress::Progress;

use super::*;

const WRITTEN_BY: &str = "v0.0.0";
const ENGINE: &str = "ghcr.io/acme/vendor_kit:v1.4.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const TOOL: &str = "ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222";
const OTHER: &str = "ghcr.io/acme/other:v1.0.0@sha256:3333333333333333333333333333333333333333333333333333333333333333";

/// 主機上的安裝目錄（`--host-root`）；`/h/` 底下的主機路徑對到 [`Fx::host`]。
const HOST_ROOT: &str = "/h/proj";
/// 假 registry 認得的 PAT；其他 token 一律拒絕。
const GOOD_TOKEN: &str = "good";
/// 帶 [`GOOD_TOKEN`] 換 bearer 時的 Basic 認證：`base64("vendor_kit:good")`（帳號是 `registry::USERNAME`）。
const GOOD_BASIC: &str = "Basic dmVuZG9yX2tpdDpnb29k";

struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
    ctl: PathBuf,
    inbox: PathBuf,
    /// 主機的 `/h/`：`stage` 的主機路徑 `/h/<x>` 對到這裡的 `<x>`；安裝目錄不在這底下。
    host: PathBuf,
}

impl Fx {
    /// `tool`、`other` 都已導入的安裝目錄。
    fn new() -> Fx {
        let tmp = tempfile::tempdir().unwrap();
        let ctl = tmp.path().join("ctl");
        let inbox = tmp.path().join("in");
        let host = tmp.path().join("host");
        for d in [&ctl, &inbox, &host.join("proj")] {
            fs::create_dir_all(d).unwrap();
        }
        let dir = InstallDir::new(tmp.path().join("root"));
        fs::create_dir_all(dir.vk_dir().join("log")).unwrap();
        fs::write(
            dir.version_toml(),
            format!(
                "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nother = \"{OTHER}\"\ntool = \"{TOOL}\"\n"
            ),
        )
        .unwrap();
        Fx {
            _tmp: tmp,
            dir,
            ctl,
            inbox,
            host,
        }
    }

    /// `.vendor_kit/` 下每個檔的路徑與內容（不含 `log/` 與鎖檔），比對有沒有被動到。
    fn snapshot(&self) -> Vec<(PathBuf, Vec<u8>)> {
        fn walk(dir: &Path, out: &mut Vec<(PathBuf, Vec<u8>)>) {
            for entry in fs::read_dir(dir).unwrap() {
                let path = entry.unwrap().path();
                if path.is_dir() {
                    walk(&path, out);
                } else {
                    out.push((path.clone(), fs::read(&path).unwrap()));
                }
            }
        }
        let mut out = Vec::new();
        walk(&self.dir.vk_dir(), &mut out);
        out.retain(|(p, _)| {
            !p.starts_with(self.dir.vk_dir().join("log"))
                && p.file_name()
                    .is_some_and(|n| !n.to_string_lossy().contains("lock"))
        });
        out.sort();
        out
    }

    /// 寫一份殘留的進度檔；`table` 是 recipe 自己的欄位（`[<verb>]` 下的 `key = value` 行）。
    fn residual(&self, verb: &str, command: &[&str], table: Option<(&str, &str)>) {
        let mut p = Progress::new(verb, "r0", command).unwrap();
        if let Some((key, value)) = table {
            p.document_mut().set(&[verb, key], value).unwrap();
        }
        p.create(&self.dir, WRITTEN_BY).unwrap();
    }
}

#[derive(Clone, Default)]
struct Shared(Arc<Mutex<Vec<u8>>>);

impl Write for Shared {
    fn write(&mut self, data: &[u8]) -> io::Result<usize> {
        self.0.lock().unwrap().extend_from_slice(data);
        Ok(data.len())
    }
    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}

impl Shared {
    fn text(&self) -> String {
        String::from_utf8(self.0.lock().unwrap().clone()).unwrap()
    }
}

// ---- 假 registry ----

/// 假 registry 裡的一個 image 路徑。
#[derive(Clone)]
enum Repo {
    /// 匿名就能列。
    Public(Vec<&'static str>),
    /// 要帶 [`GOOD_TOKEN`] 才能列。
    Private(Vec<&'static str>),
}

/// GHCR 的樣子（token 認證）：沒帶 Bearer 回 401 加 challenge；`/token` 匿名給 `anon`，Basic 帶
/// [`GOOD_TOKEN`] 給 `pat`，其他 Basic 回 401；`tags/list` 依 [`Repo`] 回，沒列的路徑回 404。
struct Registry {
    base: String,
    /// 收到的請求行（方法與目標），依序。
    log: Arc<Mutex<Vec<String>>>,
}

impl Registry {
    fn start(repos: &[(&str, Repo)]) -> Registry {
        let repos: BTreeMap<String, Repo> = repos
            .iter()
            .map(|(p, r)| ((*p).to_owned(), r.clone()))
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
                let (status, headers, body) = respond(&repos, &base2, &line, auth.as_deref());
                write_response(stream, status, &headers, &body);
            }
        });
        Registry { base, log }
    }

    fn client(&self) -> Client {
        Client::with_base_url(&self.base).unwrap()
    }

    fn requests(&self) -> Vec<String> {
        self.log.lock().unwrap().clone()
    }
}

fn respond(
    repos: &BTreeMap<String, Repo>,
    base: &str,
    line: &str,
    auth: Option<&str>,
) -> (u16, Vec<(String, String)>, String) {
    let target = line.split(' ').nth(1).unwrap_or("");
    if target.starts_with("/token") {
        return match auth {
            None => (200, vec![], r#"{"token":"anon"}"#.to_owned()),
            Some(GOOD_BASIC) => (200, vec![], r#"{"token":"pat"}"#.to_owned()),
            Some(_) => (401, vec![], String::new()),
        };
    }
    let Some(path) = target
        .strip_prefix("/v2/")
        .and_then(|t| t.split_once("/tags/list"))
        .map(|(p, _)| p)
    else {
        return (404, vec![], String::new());
    };
    let bearer = auth.and_then(|a| a.strip_prefix("Bearer "));
    let Some(bearer) = bearer else {
        let challenge = format!(
            r#"Bearer realm="{base}/token",service="ghcr.io",scope="repository:{path}:pull""#
        );
        return (
            401,
            vec![("WWW-Authenticate".to_owned(), challenge)],
            String::new(),
        );
    };
    let tags = match repos.get(path) {
        None => return (404, vec![], String::new()),
        Some(Repo::Public(tags)) => tags,
        Some(Repo::Private(tags)) if bearer == "pat" => tags,
        Some(Repo::Private(_)) => return (403, vec![], String::new()),
    };
    let list: Vec<String> = tags.iter().map(|t| format!("\"{t}\"")).collect();
    let body = format!(r#"{{"name":"{path}","tags":[{}]}}"#, list.join(","));
    (200, vec![], body)
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

fn write_response(mut stream: TcpStream, status: u16, headers: &[(String, String)], body: &str) {
    let mut out = format!("HTTP/1.1 {status} X\r\n");
    for (k, v) in headers {
        out.push_str(&format!("{k}: {v}\r\n"));
    }
    out.push_str(&format!(
        "Content-Length: {}\r\nConnection: close\r\n\r\n{body}",
        body.len()
    ));
    let _ = stream.write_all(out.as_bytes());
}

/// 三個對象都公開、各有合法 tag 的 registry：工具查鎖定行的路徑，引擎查 [`ENGINE_REPO`]。
fn all_public() -> Registry {
    Registry::start(&[
        (
            "acme/tool",
            Repo::Public(vec!["v1.0.0", "v1.3.0", "latest"]),
        ),
        ("acme/other", Repo::Public(vec!["v1.0.0"])),
        (
            "ycpss91255-research/vendor_kit",
            Repo::Public(vec!["v1.4.0", "v1.10.0", "v1.9.0"]),
        ),
    ])
}

// ---- 假啟動器（只做 `stage`） ----

/// 假啟動器：`stage <主機路徑> <slot>` 把 `/h/<x>` 對到 [`Fx::host`] 的 `<x>` 複製進 `in/<slot>`
/// （launcher/launch.sh：來源讀不到或 slot 已存在回 failed 1）；其他 op 一律 failed 1。
struct Peer {
    stop: Arc<AtomicBool>,
    handle: JoinHandle<Vec<String>>,
}

impl Peer {
    fn start(fx: &Fx) -> Peer {
        let (ctl, inbox, host) = (fx.ctl.clone(), fx.inbox.clone(), fx.host.clone());
        let stop = Arc::new(AtomicBool::new(false));
        let flag = Arc::clone(&stop);
        let handle = thread::spawn(move || {
            let header = header();
            let mut seen = Vec::new();
            let mut seq = 1u16;
            while !flag.load(Ordering::SeqCst) {
                let Ok(bytes) = fs::read(ctl.join(format!("req.{seq}"))) else {
                    thread::sleep(Duration::from_millis(2));
                    continue;
                };
                let (s, op) = Op::parse_request(&bytes, &header).unwrap();
                let outcome = match &op {
                    Op::Stage(path, slot) => {
                        let path = String::from_utf8(path.as_bytes().to_vec()).unwrap();
                        seen.push(format!("stage {path} {}", slot.as_str()));
                        let dest = inbox.join(slot.as_str());
                        let src = path.strip_prefix("/h/").map(|rest| host.join(rest));
                        match src {
                            Some(src) if !dest.exists() && fs::copy(&src, &dest).is_ok() => {
                                Outcome::Ok
                            }
                            _ => Outcome::Failed(1),
                        }
                    }
                    other => {
                        seen.push(other.kind().name().to_owned());
                        Outcome::Failed(1)
                    }
                };
                let tmp = ctl.join(format!("res.{s}.tmp"));
                fs::write(&tmp, outcome.encode_response(&header, s)).unwrap();
                fs::rename(&tmp, ctl.join(format!("res.{s}"))).unwrap();
                seq += 1;
            }
            seen
        });
        Peer { stop, handle }
    }

    fn finish(self) -> Vec<String> {
        self.stop.store(true, Ordering::SeqCst);
        self.handle.join().unwrap()
    }
}

fn header() -> Header {
    Header::new(1, RunId::parse("r1").unwrap()).unwrap()
}

struct Out {
    code: u8,
    stdout: String,
    /// 提醒與診斷，依序。
    stderr: String,
    /// 假啟動器收到的 op。
    launcher: Vec<String>,
}

/// 一次 `update` 的呼叫。
#[derive(Default)]
struct Call<'a> {
    repo: Option<&'a str>,
    token_file: Option<&'a str>,
}

/// 查詢前就停下的情況：registry 不該被連到，給一個不會被用到的位址。
fn unused_registry() -> Client {
    Client::with_base_url("http://127.0.0.1:9").unwrap()
}

fn run_update(fx: &Fx, repo: Option<&str>) -> Out {
    run_with(
        fx,
        &unused_registry(),
        &Call {
            repo,
            token_file: None,
        },
    )
}

fn run_with(fx: &Fx, registry: &Client, call: &Call<'_>) -> Out {
    // 每次執行是新的 session：清掉上次的 ctl/ 與 in/。
    for d in [&fx.ctl, &fx.inbox] {
        fs::remove_dir_all(d).unwrap();
        fs::create_dir_all(d).unwrap();
    }
    let peer = Peer::start(fx);
    let mut channel = Channel::new(&fx.ctl, header());
    let mut stdout = Vec::new();
    let shared = Shared::default();
    let mut plain = shared.clone();
    let mut diags = Diagnostics::with_sink(shared.clone(), NoSink);
    let token_file = call.token_file.map(OsString::from);
    let code = {
        let mut env = Env {
            dir: &fx.dir,
            inbox: &fx.inbox,
            channel: &mut channel,
            poll: Duration::from_millis(1),
            registry,
            host_root: HOST_ROOT,
            run_log: "/h/proj/.vendor_kit/log/r1.jsonl",
            stdout: &mut stdout,
            stderr: &mut plain,
            diags: &mut diags,
        };
        let req = Request {
            repo: call.repo,
            registry_token_file: token_file.as_deref(),
        };
        run(&req, &mut env)
    };
    Out {
        code,
        stdout: String::from_utf8(stdout).unwrap(),
        stderr: shared.text(),
        launcher: peer.finish(),
    }
}

fn diag_codes(stderr: &str) -> Vec<&str> {
    stderr
        .lines()
        .filter_map(|l| l.strip_prefix("vendor_kit: "))
        .filter_map(|l| l.split_once('[').map(|(_, rest)| rest))
        .filter_map(|l| l.split_once("]: ").map(|(c, _)| c))
        .collect()
}

#[test]
fn result_line_format() {
    let t = |s: &str| Tag::parse(s).unwrap();
    assert_eq!(
        text::result_line("lint", t("v1.0.0"), Some(t("v1.3.0"))),
        "lint current: v1.0.0 latest: v1.3.0"
    );
    assert_eq!(
        text::result_line(text::ENGINE_NAME, t("v1.4.0"), None),
        "vendor_kit current: v1.4.0 latest: none"
    );
    // 04 指定版本：逐欄比數值、略過不合法的 tag，最新版可能比 current 舊。
    let latest = Tag::latest(["v1.10.0", "v1.9.9", "latest", "v01.0.0"]);
    assert_eq!(
        text::result_line("base", t("v2.0.0"), latest),
        "base current: v2.0.0 latest: v1.10.0"
    );
    assert_eq!(Tag::latest(["latest", "main"]), None);
}

#[test]
fn original_command_quotes_each_argument() {
    assert_eq!(
        original_command(&["remove", "tool"]),
        "just vendor_kit remove tool"
    );
    assert_eq!(
        original_command(&["dev", "tool", "-p", "my dir", "it's"]),
        r"just vendor_kit dev tool -p 'my dir' 'it'\''s'"
    );
    assert_eq!(original_command(&["x", ""]), "just vendor_kit x ''");
}

#[test]
fn update_prints_one_result_line_per_tool_and_the_engine() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let registry = all_public();
    let out = run_with(&fx, &registry.client(), &Call::default());
    assert_eq!(out.code, 0, "{}", out.stderr);
    // 已最新也印；引擎的工具名欄是 vendor_kit，查的是 ENGINE_REPO（鎖定行寫 acme/vendor_kit 也一樣）；
    // 最新版逐欄比數值（v1.10.0 > v1.9.0），不合法的 tag（latest）略過。
    assert_eq!(
        out.stdout,
        "other current: v1.0.0 latest: v1.0.0\n\
         tool current: v1.2.0 latest: v1.3.0\n\
         vendor_kit current: v1.4.0 latest: v1.10.0\n"
    );
    assert_eq!(out.stderr, "");
    assert!(out.launcher.is_empty(), "{:?}", out.launcher);
    let listed: Vec<String> = registry
        .requests()
        .into_iter()
        .filter(|r| r.contains("/tags/list"))
        .collect();
    assert!(
        listed
            .iter()
            .any(|r| r.contains("/v2/ycpss91255-research/vendor_kit/tags/list")),
        "{listed:?}"
    );
    assert!(!listed.iter().any(|r| r.contains("acme/vendor_kit")));
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn update_repo_queries_only_that_tool() {
    let fx = Fx::new();
    let registry = all_public();
    let out = run_with(
        &fx,
        &registry.client(),
        &Call {
            repo: Some("tool"),
            ..Call::default()
        },
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, "tool current: v1.2.0 latest: v1.3.0\n");
    assert!(
        registry
            .requests()
            .iter()
            .all(|r| !r.contains("/tags/list") || r.contains("/v2/acme/tool/")),
        "{:?}",
        registry.requests()
    );
}

#[test]
fn a_failed_query_prints_latest_none_and_does_not_stop_the_others() {
    let fx = Fx::new();
    let before = fx.snapshot();
    // tool 要 token、other 沒有合法 tag、引擎的路徑不存在（404）。
    let registry = Registry::start(&[
        ("acme/tool", Repo::Private(vec!["v1.3.0"])),
        ("acme/other", Repo::Public(vec!["latest", "v01.0.0"])),
    ]);
    let out = run_with(&fx, &registry.client(), &Call::default());
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stdout,
        "other current: v1.0.0 latest: none\n\
         tool current: v1.2.0 latest: none\n\
         vendor_kit current: v1.4.0 latest: none\n"
    );
    assert_eq!(
        diag_codes(&out.stderr),
        ["VK0058", "VK0001", "VK0055"],
        "{}",
        out.stderr
    );
    assert!(
        out.stderr.contains(
            "error[VK0058]: Cannot determine the latest version of other: the registry has tags, but none is a valid vX.Y.Z tag."
        ),
        "{}",
        out.stderr
    );
    // VK0001：<cmd> 在 update 時印 upgrade，<path> 與 <tag> 原樣印出。
    assert!(
        out.stderr.contains(
            "error[VK0001]: Cannot list versions for tool: registry read access is required; pulling still uses the host's Docker credentials. Add --registry-token-file <path> and rerun, or specify a version directly: just vendor_kit upgrade tool@<tag>"
        ),
        "{}",
        out.stderr
    );
    assert!(
        out.stderr.contains(
            "error[VK0055]: Cannot access ghcr.io/ycpss91255-research/vendor_kit for vendor_kit: registry returned HTTP 404"
        ),
        "{}",
        out.stderr
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn a_registry_without_any_tag_is_vk0055() {
    let fx = Fx::new();
    let registry = Registry::start(&[("acme/tool", Repo::Public(vec![]))]);
    let out = run_with(
        &fx,
        &registry.client(),
        &Call {
            repo: Some("tool"),
            ..Call::default()
        },
    );
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "tool current: v1.2.0 latest: none\n");
    assert_eq!(
        out.stderr,
        format!(
            "vendor_kit: error[VK0055]: Cannot access ghcr.io/acme/tool for tool: {}. The requested operation did not complete.\n",
            text::NO_TAGS
        )
    );
}

/// 只有 tool 是私有的 registry；另兩個公開。
fn private_tool() -> Registry {
    Registry::start(&[
        ("acme/tool", Repo::Private(vec!["v1.3.0"])),
        ("acme/other", Repo::Public(vec!["v1.0.0"])),
        (
            "ycpss91255-research/vendor_kit",
            Repo::Public(vec!["v1.4.0"]),
        ),
    ])
}

#[test]
fn a_token_file_inside_the_install_dir_is_read_directly() {
    let fx = Fx::new();
    fs::create_dir_all(fx.dir.root().join("secrets")).unwrap();
    fs::write(
        fx.dir.root().join("secrets/ghcr"),
        format!("  {GOOD_TOKEN}\n"),
    )
    .unwrap();
    let before = fx.snapshot();
    let registry = private_tool();
    // 相對路徑以安裝目錄為準；絕對路徑在 --host-root 底下也算安裝目錄裡。
    for given in [
        "secrets/ghcr",
        "./x/../secrets/ghcr",
        "/h/proj/secrets/ghcr",
    ] {
        let out = run_with(
            &fx,
            &registry.client(),
            &Call {
                token_file: Some(given),
                ..Call::default()
            },
        );
        assert_eq!(out.code, 0, "{given}: {}", out.stderr);
        assert_eq!(
            out.stdout,
            "other current: v1.0.0 latest: v1.0.0\n\
             tool current: v1.2.0 latest: v1.3.0\n\
             vendor_kit current: v1.4.0 latest: v1.4.0\n"
        );
        assert!(out.launcher.is_empty(), "{given}: {:?}", out.launcher);
    }
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn a_token_file_outside_the_install_dir_is_staged_once() {
    let fx = Fx::new();
    fs::create_dir_all(fx.host.join("home")).unwrap();
    fs::write(fx.host.join("home/ghcr"), GOOD_TOKEN).unwrap();
    fs::write(fx.host.join("ghcr"), GOOD_TOKEN).unwrap();
    let before = fx.snapshot();
    let registry = private_tool();

    let out = run_with(
        &fx,
        &registry.client(),
        &Call {
            token_file: Some("/h/home/ghcr"),
            ..Call::default()
        },
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(out.stdout.contains("tool current: v1.2.0 latest: v1.3.0\n"));
    // 一次執行只讀一次：三個對象共用一份 token。
    assert_eq!(out.launcher, ["stage /h/home/ghcr token"]);

    // 相對路徑以 .. 跑出安裝目錄：主機路徑是 <--host-root>/<原值>，.. 留給主機解析。
    let out = run_with(
        &fx,
        &registry.client(),
        &Call {
            token_file: Some("../ghcr"),
            ..Call::default()
        },
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.launcher, ["stage /h/proj/../ghcr token"]);
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn an_unreadable_or_empty_token_file_is_vk0055_for_every_target() {
    let fx = Fx::new();
    fs::write(fx.dir.root().join("empty"), " \n").unwrap();
    let registry = private_tool();
    for (given, reason) in [
        ("empty", text::TOKEN_EMPTY),
        ("missing", "cannot read the registry token file"),
        (
            "/h/missing",
            "the launcher could not copy the registry token file (exit 1)",
        ),
    ] {
        let out = run_with(
            &fx,
            &registry.client(),
            &Call {
                token_file: Some(given),
                ..Call::default()
            },
        );
        assert_eq!(out.code, 2, "{given}");
        assert_eq!(
            out.stdout,
            "other current: v1.0.0 latest: none\n\
             tool current: v1.2.0 latest: none\n\
             vendor_kit current: v1.4.0 latest: none\n",
            "{given}"
        );
        assert_eq!(
            diag_codes(&out.stderr),
            ["VK0055", "VK0055", "VK0055"],
            "{given}: {}",
            out.stderr
        );
        assert!(
            out.stderr.contains(&format!(
                "error[VK0055]: Cannot access {given} for tool: {reason}"
            )),
            "{given}: {}",
            out.stderr
        );
    }
    // token 讀不到就不連 registry。
    assert!(registry.requests().is_empty(), "{:?}", registry.requests());
}

#[test]
fn a_rejected_token_is_vk0055_without_an_anonymous_retry() {
    let fx = Fx::new();
    fs::write(fx.dir.root().join("tok"), "bad").unwrap();
    let registry = private_tool();
    let out = run_with(
        &fx,
        &registry.client(),
        &Call {
            repo: Some("tool"),
            token_file: Some("tok"),
        },
    );
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "tool current: v1.2.0 latest: none\n");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0055]: Cannot access ghcr.io/acme/tool for tool: registry rejected the supplied token (HTTP 401). The requested operation did not complete.\n"
    );
    let tokens = registry
        .requests()
        .iter()
        .filter(|r| r.contains("/token"))
        .count();
    assert_eq!(tokens, 1, "{:?}", registry.requests());
}

#[test]
fn a_stop_before_the_query_does_not_read_the_token_file() {
    let fx = Fx::new();
    fx.residual("remove", &["remove", "tool"], None);
    let out = run_with(
        &fx,
        &unused_registry(),
        &Call {
            repo: None,
            token_file: Some("/h/missing"),
        },
    );
    assert_eq!(diag_codes(&out.stderr), ["VK0054"], "{}", out.stderr);
    assert!(out.launcher.is_empty(), "{:?}", out.launcher);

    let fx = Fx::new();
    let out = run_with(
        &fx,
        &unused_registry(),
        &Call {
            repo: Some("missing"),
            token_file: Some("/h/missing"),
        },
    );
    assert_eq!(diag_codes(&out.stderr), ["VK0046"], "{}", out.stderr);
    assert!(out.launcher.is_empty(), "{:?}", out.launcher);
}

#[test]
fn token_paths_are_located_against_the_install_dir() {
    let inside = |p: &str| TokenPath::Inside(PathBuf::from(p));
    let outside = |p: &str| TokenPath::Outside(p.as_bytes().to_vec());
    let at = |p: &str| locate(OsStr::new(p), HOST_ROOT);
    assert_eq!(at("tok"), inside("tok"));
    assert_eq!(at("./a/../b/tok"), inside("b/tok"));
    assert_eq!(at("/h/proj/s/tok"), inside("s/tok"));
    assert_eq!(at("/h/proj/../proj/tok"), inside("tok"));
    assert_eq!(at("../tok"), outside("/h/proj/../tok"));
    assert_eq!(at("a/../../tok"), outside("/h/proj/a/../../tok"));
    assert_eq!(at("/h/other/./tok"), outside("/h/other/tok"));
    assert_eq!(at("/h/projx/tok"), outside("/h/projx/tok"));
}

#[test]
fn update_of_a_tool_not_in_the_lock_lines_is_vk0046() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let out = run_update(&fx, Some("missing"));
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0046]: Tool missing is not in the lock version lines. The requested operation did not complete.\n"
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn residual_progress_is_detected_before_the_target_check_and_left_alone() {
    let fx = Fx::new();
    fx.residual("add", &["add", "new", "-i", "x"], Some(("repo", "new")));
    fx.residual("remove", &["remove", "tool"], None);
    let before = fx.snapshot();
    let out = run_update(&fx, Some("missing"));
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        diag_codes(&out.stderr),
        ["VK0004", "VK0054"],
        "{}",
        out.stderr
    );
    assert!(
        out.stderr
            .contains("Import of new is incomplete. Run: just vendor_kit add new"),
        "{}",
        out.stderr
    );
    assert!(
        out.stderr.contains(
            "Operation remove in /h/proj is incomplete. Run again: just vendor_kit remove tool"
        ),
        "{}",
        out.stderr
    );
    // 唯讀 recipe：不恢復、不刪進度檔。
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn residual_tool_upgrade_progress_is_vk0041_with_the_original_command() {
    let fx = Fx::new();
    fx.residual(
        UPGRADE_VERB,
        &[UPGRADE_VERB, "tool@v1.3.0", "-y"],
        Some((progress::upgrade::TARGET, "tool")),
    );
    let before = fx.snapshot();
    let out = run_update(&fx, None);
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0041]: Upgrade of tool is incomplete. Run again: just vendor_kit upgrade tool@v1.3.0 -y\n"
    );
    // 唯讀 recipe：不恢復、不刪進度檔。
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn residual_engine_upgrade_or_upgrade_without_target_is_a_gap() {
    let fx = Fx::new();
    fx.residual(
        UPGRADE_VERB,
        &[UPGRADE_VERB, "--engine"],
        Some((progress::upgrade::TARGET, progress::upgrade::ENGINE_TARGET)),
    );
    let out = run_update(&fx, None);
    assert_eq!(out.code, 2);
    assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(
        out.stderr
            .contains("reporting the incomplete engine upgrade"),
        "{}",
        out.stderr
    );

    let fx = Fx::new();
    fx.residual(UPGRADE_VERB, &[UPGRADE_VERB, "tool"], None);
    let out = run_update(&fx, None);
    assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(out.stderr.contains("without its [upgrade] target field"));
}

#[test]
fn residual_undev_progress_is_vk0053_with_the_original_command() {
    let fx = Fx::new();
    fx.residual(
        UNDEV_VERB,
        &[UNDEV_VERB, "tool"],
        Some((UNDEV_TARGET_KEY, "tool")),
    );
    let before = fx.snapshot();
    let out = run_update(&fx, None);
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0053]: The undev operation for tool is incomplete. Run again: just vendor_kit undev tool\n"
    );
    assert_eq!(fx.snapshot(), before);

    // 沒有 `[undev] target` 欄位：缺口。
    let fx = Fx::new();
    fx.residual(UNDEV_VERB, &[UNDEV_VERB, "--engine"], None);
    let out = run_update(&fx, None);
    assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(out.stderr.contains("without its [undev] target field"));
}

#[test]
fn residual_add_without_its_repo_field_is_a_gap() {
    let fx = Fx::new();
    fx.residual("add", &["add", "new"], None);
    let out = run_update(&fx, None);
    assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(out.stderr.contains("without its [add] repo field"));
}

#[test]
fn local_overrides_are_reminded_on_stderr_without_a_prefix() {
    let fx = Fx::new();
    fs::write(
        fx.dir.version_local_toml(),
        "vendor_kit = \"ghcr.io/acme/vendor_kit:dev\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"../tool\"\n",
    )
    .unwrap();
    let before = fx.snapshot();
    let registry = all_public();

    // 仍照版本鎖定行查：結果行跟沒有覆寫時一樣。
    let out = run_with(&fx, &registry.client(), &Call::default());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(
        out.stdout.contains("tool current: v1.2.0 latest: v1.3.0\n"),
        "{}",
        out.stdout
    );
    let lines: Vec<&str> = out.stderr.lines().collect();
    assert_eq!(
        lines[..2],
        [
            "tool uses the local override ../tool; update checks the lock version line.",
            "vendor_kit uses the local override ghcr.io/acme/vendor_kit:dev; update checks the lock version line.",
        ],
        "{}",
        out.stderr
    );
    assert_eq!(diag_codes(&out.stderr), Vec::<&str>::new());

    // `update <repo>` 只提醒那個工具的覆寫，不提引擎。
    let out = run_with(
        &fx,
        &registry.client(),
        &Call {
            repo: Some("other"),
            ..Call::default()
        },
    );
    assert!(!out.stderr.contains("local override"), "{}", out.stderr);
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn lock_file_too_new_is_vk0008() {
    let fx = Fx::new();
    fs::write(
        fx.dir.version_toml(),
        format!("vendor_kit = \"{ENGINE}\"\nschema = 99\nwritten_by = \"v9.0.0\"\n"),
    )
    .unwrap();
    let out = run_update(&fx, None);
    assert_eq!(out.code, 3);
    assert_eq!(diag_codes(&out.stderr), ["VK0008"], "{}", out.stderr);
}
