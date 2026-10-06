//! 單元測試：以背景的假啟動器回 inspect 與 extract，跑整段 `add`。初始檔經 [`run_with`] 直接給，
//! 驗答否、不能互動、同意後的寫入（repo 檔、metadata、基準版副本）；另驗恢復殘留進度與各個停下點。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::io::Cursor;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread::{self, JoinHandle};

use diagnostics::NoSink;
use plan::{Header, RunId};

use super::*;

const WRITTEN_BY: &str = "v0.0.0";
const ENGINE: &str = "ghcr.io/acme/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const IMAGE: &str = "ghcr.io/acme/tool:v1.2.0";
const DIGEST: &str = "sha256:2222222222222222222222222222222222222222222222222222222222222222";
const IMAGE_ID: &str = "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";

fn locked() -> String {
    format!("{IMAGE}@{DIGEST}")
}

/// 安裝目錄與 session 目錄。
struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
    ctl: PathBuf,
    inbox: PathBuf,
}

impl Fx {
    fn new(tools: &str) -> Fx {
        let tmp = tempfile::tempdir().unwrap();
        let root = tmp.path().join("root");
        let ctl = tmp.path().join("ctl");
        let inbox = tmp.path().join("in");
        for d in [&root, &ctl, &inbox] {
            fs::create_dir_all(d).unwrap();
        }
        let dir = InstallDir::new(&root);
        fs::create_dir_all(dir.vk_dir()).unwrap();
        let tools = if tools.is_empty() {
            String::new()
        } else {
            format!("\n[tools]\n{tools}")
        };
        fs::write(
            dir.version_toml(),
            format!("vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n{tools}"),
        )
        .unwrap();
        Fx {
            _tmp: tmp,
            dir,
            ctl,
            inbox,
        }
    }

    fn lock_text(&self) -> String {
        fs::read_to_string(self.dir.version_toml()).unwrap()
    }

    /// 每次執行的 ctl 目錄是新的：上一次留下的 `req.*`、`res.*` 會被新的假啟動器或引擎誤讀。
    fn new_session(&self) {
        fs::remove_dir_all(&self.ctl).unwrap();
        fs::create_dir_all(&self.ctl).unwrap();
    }

    /// 執行前 ctl 目錄必須是空的（假啟動器啟動時清過）。
    fn assert_fresh_session(&self) {
        let left: Vec<_> = fs::read_dir(&self.ctl)
            .unwrap()
            .map(|e| e.unwrap().file_name())
            .collect();
        assert!(left.is_empty(), "ctl/ has leftovers: {left:?}");
    }

    fn root(&self) -> &Path {
        self.dir.root()
    }
}

fn header() -> Header {
    Header::new(1, RunId::parse("r1").unwrap()).unwrap()
}

/// 假啟動器：inspect 回 RepoDigests，extract 放進 `just/<ns>.just`；`fail` 讓指定的 op 回 failed 1。
struct Peer {
    stop: Arc<AtomicBool>,
    handle: JoinHandle<Vec<String>>,
}

impl Peer {
    fn start(fx: &Fx, namespaces: &'static [&'static str], fail: Option<&'static str>) -> Peer {
        Peer::start_each(fx, vec![namespaces], fail)
    }

    /// 第 k 次 extract 放 `each[k]` 的 `<ns>`（超過的沿用最後一組）。
    fn start_each(fx: &Fx, each: Vec<&'static [&'static str]>, fail: Option<&'static str>) -> Peer {
        // 先清 ctl/ 再起執行緒：新的假啟動器不能讀到上一次的 req.1。
        fx.new_session();
        let (ctl, inbox) = (fx.ctl.clone(), fx.inbox.clone());
        let stop = Arc::new(AtomicBool::new(false));
        let flag = Arc::clone(&stop);
        let handle = thread::spawn(move || {
            let header = header();
            let mut seen = Vec::new();
            let mut seq = 1u16;
            let mut extracts = 0usize;
            while !flag.load(Ordering::SeqCst) {
                let Ok(bytes) = fs::read(ctl.join(format!("req.{seq}"))) else {
                    thread::sleep(Duration::from_millis(2));
                    continue;
                };
                let (s, op) = Op::parse_request(&bytes, &header).unwrap();
                seen.push(op.kind().name().to_owned());
                let mut return_failed = false;
                let outcome = if Some(op.kind().name()) == fail {
                    Outcome::Failed(1)
                } else {
                    match &op {
                        // 啟動器不收已存在的 slot（launcher/launch.sh 的 vk_launch_extract）。
                        Op::Extract(_, slot) if inbox.join(slot.as_str()).exists() => {
                            return_failed = true;
                        }
                        Op::Inspect(_) => {
                            let json = format!(
                                "[{{\"Id\":\"{IMAGE_ID}\",\"RepoDigests\":[\"ghcr.io/acme/tool@{DIGEST}\"]}}]"
                            );
                            fs::write(ctl.join(format!("res.{s}.out")), json).unwrap();
                        }
                        Op::Extract(_, slot) => {
                            let just = inbox.join(slot.as_str()).join("just");
                            fs::create_dir_all(&just).unwrap();
                            let namespaces = each[extracts.min(each.len() - 1)];
                            extracts += 1;
                            for ns in namespaces {
                                fs::write(just.join(format!("{ns}.just")), "x:\n").unwrap();
                            }
                        }
                        _ => {}
                    }
                    if return_failed {
                        Outcome::Failed(1)
                    } else {
                        Outcome::Ok
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

/// image tar 的假啟動器怎麼回：`digest` 是旁檔內容（`None`＝旁檔不在，`stage` 回 failed 1）；`load` 是
/// `docker load -q` 的 stdout（`None`＝load 回 failed 1）；`tags` 是 inspect 的 RepoTags。RepoDigests 一律
/// 是空的（classic image store 載入 tar 的樣子）。
#[derive(Clone, Copy)]
struct TarImage {
    digest: Option<&'static str>,
    load: Option<&'static str>,
    tags: &'static [&'static str],
}

const TAR_DIGEST: &str = "sha256:4444444444444444444444444444444444444444444444444444444444444444";
const TAR: TarImage = TarImage {
    digest: Some("sha256:4444444444444444444444444444444444444444444444444444444444444444\n"),
    load: Some("Loaded image: ghcr.io/acme/tool:v1.2.0\n"),
    tags: &["ghcr.io/acme/tool:v1.2.0"],
};

/// image tar 的假啟動器；回傳依序的請求（`stage`、`load` 帶主機路徑，`inspect` 帶引用）。
struct TarPeer {
    stop: Arc<AtomicBool>,
    handle: JoinHandle<Vec<String>>,
}

impl TarPeer {
    fn start(fx: &Fx, image: TarImage) -> TarPeer {
        // 每次 session 的 in/ 也是新的：上一次 stage 的旁檔留著，啟動器不收已存在的 slot。
        fx.new_session();
        fs::remove_dir_all(&fx.inbox).unwrap();
        fs::create_dir_all(&fx.inbox).unwrap();
        let (ctl, inbox) = (fx.ctl.clone(), fx.inbox.clone());
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
                let out = ctl.join(format!("res.{s}.out"));
                let ok = match &op {
                    Op::Stage(f, slot) => {
                        seen.push(format!("stage {}", String::from_utf8_lossy(f.as_bytes())));
                        match image.digest {
                            Some(d) if !inbox.join(slot.as_str()).exists() => {
                                fs::write(inbox.join(slot.as_str()), d).unwrap();
                                true
                            }
                            _ => false,
                        }
                    }
                    Op::Load(f) => {
                        seen.push(format!("load {}", String::from_utf8_lossy(f.as_bytes())));
                        match image.load {
                            Some(text) => {
                                fs::write(&out, text).unwrap();
                                true
                            }
                            None => false,
                        }
                    }
                    Op::Inspect(r) => {
                        seen.push(format!("inspect {}", r.as_str()));
                        let tags: Vec<String> =
                            image.tags.iter().map(|t| format!("\"{t}\"")).collect();
                        let json = format!(
                            "[{{\"Id\":\"{IMAGE_ID}\",\"RepoTags\":[{}],\"RepoDigests\":[]}}]",
                            tags.join(",")
                        );
                        fs::write(&out, json).unwrap();
                        true
                    }
                    Op::Extract(id, slot) => {
                        seen.push(format!("extract {}", id.as_str()));
                        let just = inbox.join(slot.as_str()).join("just");
                        fs::create_dir_all(&just).unwrap();
                        fs::write(just.join("tool.just"), "x:\n").unwrap();
                        true
                    }
                    other => {
                        seen.push(other.kind().name().to_owned());
                        false
                    }
                };
                let outcome = if ok { Outcome::Ok } else { Outcome::Failed(1) };
                let tmp = ctl.join(format!("res.{s}.tmp"));
                fs::write(&tmp, outcome.encode_response(&header, s)).unwrap();
                fs::rename(&tmp, ctl.join(format!("res.{s}"))).unwrap();
                seq += 1;
            }
            seen
        });
        TarPeer { stop, handle }
    }

    fn finish(self) -> Vec<String> {
        self.stop.store(true, Ordering::SeqCst);
        self.handle.join().unwrap()
    }
}

struct Out {
    code: u8,
    stdout: String,
    /// 詢問與診斷，依序。
    stderr: String,
    log: String,
}

fn tty(interactive: bool) -> Tty {
    Tty {
        stdin: interactive,
        stdout: interactive,
        stderr: interactive,
    }
}

fn run_add(fx: &Fx, argv: &[&str], init: Vec<OwnedInit>, tty: Tty, input: &str) -> Out {
    let value = |opt: &str| argv.iter().position(|a| *a == opt).map(|i| argv[i + 1]);
    let (repo, tag) = match argv[1].split_once('@') {
        Some((r, t)) => (r, Some(Tag::parse(t).unwrap())),
        None => (argv[1], None),
    };
    let req = Request {
        repo,
        tag,
        image: value("-i").map(OsStr::new),
        yes: argv.iter().any(|a| matches!(*a, "-y" | "--yes")),
        image_path: value("--image-path"),
        registry_token_file: None,
    };
    // 這裡的測試都不該連到 registry：給一個不會被用到的位址（線上解析的 e2e 接假 registry）。
    let registry = Client::with_base_url("http://127.0.0.1:9").unwrap();
    let argv: Vec<String> = argv.iter().map(|s| (*s).to_owned()).collect();
    fx.assert_fresh_session();
    let mut channel = Channel::new(&fx.ctl, header());
    let mut stdin = Cursor::new(input.as_bytes().to_vec());
    let mut stdout = Vec::new();
    // 詢問與診斷寫進同一條 stderr：兩邊都寫進共用的緩衝。
    let shared = Shared::default();
    let mut prompt = shared.clone();
    let mut diags = Diagnostics::with_sink(shared.clone(), NoSink);
    let mut log = runlog::Writer::new(
        Vec::new(),
        runlog::Header {
            version: WRITTEN_BY.to_owned(),
            component: runlog::Component::Engine,
            invocation_id: "r1".to_owned(),
        },
    );
    let code = {
        let mut env = Env {
            dir: &fx.dir,
            host_root: "/h/proj",
            run_log: "/h/proj/.vendor_kit/log/r1.jsonl",
            inbox: &fx.inbox,
            channel: &mut channel,
            poll: Duration::from_millis(1),
            registry: &registry,
            tty,
            argv: &argv,
            run_id: "r1",
            written_by: WRITTEN_BY,
            stdin: &mut stdin,
            stdout: &mut stdout,
            prompt: &mut prompt,
            diags: &mut diags,
            log: &mut log,
        };
        let init = move |_: &Path| Ok(init.clone());
        run_with(&req, &mut env, &init)
    };
    Out {
        code,
        stdout: String::from_utf8(stdout).unwrap(),
        stderr: shared.text(),
        log: String::from_utf8(log.into_inner()).unwrap(),
    }
}

#[derive(Clone, Default)]
struct Shared(Arc<std::sync::Mutex<Vec<u8>>>);

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

fn append(path: &str, contents: &str) -> OwnedInit {
    OwnedInit {
        path: path.to_owned(),
        strategy: Strategy::Append,
        contents: contents.as_bytes().to_vec(),
    }
}

fn whole(path: &str, contents: &str) -> OwnedInit {
    OwnedInit {
        path: path.to_owned(),
        strategy: Strategy::Whole,
        contents: contents.as_bytes().to_vec(),
    }
}

const ADD: [&str; 4] = ["add", "tool", "-i", IMAGE];

/// `.vendor_kit/` 下除了 `cache/`、`gen/` 以外有沒有東西被寫（version.toml 不算）。
fn untouched(fx: &Fx, lock_before: &str) -> bool {
    fx.lock_text() == lock_before
        && !fx.dir.cache_dir().exists()
        && !fx.dir.gen_dir().exists()
        && !fx.dir.baseline_dir().exists()
        && progress::find(&fx.dir).unwrap().is_empty()
}

// ---- 成功 ----

#[test]
fn success_without_init_files() {
    let fx = Fx::new("");
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(&fx, &ADD, Vec::new(), tty(false), "");
    assert_eq!(peer.finish(), ["inspect", "extract"]);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, format!("Added tool v1.2.0 ({}).\n", locked()));
    assert_eq!(out.stderr, "");
    assert!(
        fx.lock_text()
            .ends_with(&format!("[tools]\ntool = \"{}\"\n", locked()))
    );
    assert_eq!(
        fs::read_to_string(fx.dir.gen_dir().join("tools.just")).unwrap(),
        "mod? tool '../cache/tool/just/tool.just'\n"
    );
    let stamp = stamp::Stamp::load(&stamp_file(&fx.dir, "tool"))
        .unwrap()
        .unwrap();
    assert_eq!(stamp.version(), locked());
    assert!(progress::find(&fx.dir).unwrap().is_empty());
    for e in ["writes_started", "lock_line_written", "progress_removed"] {
        assert!(out.log.contains(&format!("\"event_name\":\"{e}\"")), "{e}");
    }
}

#[test]
fn agreeing_writes_repo_files_metadata_and_baselines() {
    let fx = Fx::new("");
    fs::write(fx.root().join(".gitignore"), "target/\n").unwrap();
    let peer = Peer::start(&fx, &["tool"], None);
    let init = vec![
        append(".gitignore", "/.tool/\n"),
        whole("tool.toml", "[tool]\n"),
    ];
    let out = run_add(&fx, &ADD, init, tty(true), "y\n");
    peer.finish();
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stderr,
        "Append the lines from tool to the existing .gitignore? [y/N] "
    );
    assert_eq!(
        out.stdout,
        format!(
            "Added tool v1.2.0 ({}).\nAppended to .gitignore\nCreated tool.toml\n",
            locked()
        )
    );
    assert_eq!(
        fs::read_to_string(fx.root().join(".gitignore")).unwrap(),
        "target/\n/.tool/\n"
    );
    assert_eq!(
        fs::read_to_string(fx.root().join("tool.toml")).unwrap(),
        "[tool]\n"
    );
    let meta = Metadata::load(&metadata::tool_path(&fx.dir, "tool").unwrap()).unwrap();
    let states: Vec<(&str, &str)> = meta
        .files()
        .iter()
        .map(|r| (r.path.as_str(), r.state.as_str()))
        .collect();
    assert_eq!(
        states,
        [(".gitignore", "appended"), ("tool.toml", "managed")]
    );
    assert_eq!(
        fs::read_to_string(fx.dir.vk_dir().join(baseline_file("tool", "tool.toml"))).unwrap(),
        "[tool]\n"
    );
}

#[test]
fn existing_whole_file_is_left_alone_with_a_warning() {
    let fx = Fx::new("");
    fs::write(fx.root().join("tool.toml"), "mine\n").unwrap();
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(
        &fx,
        &ADD,
        vec![whole("tool.toml", "[tool]\n")],
        tty(false),
        "",
    );
    peer.finish();
    assert_eq!(out.code, 1);
    assert_eq!(
        out.stderr,
        "vendor_kit: warn[VK0018]: tool.toml already exists and is unmanaged; it was neither overwritten nor brought under management.\n"
    );
    assert_eq!(
        fs::read_to_string(fx.root().join("tool.toml")).unwrap(),
        "mine\n"
    );
    assert!(fx.lock_text().contains("[tools]"));
}

// ---- 答否與不能互動 ----

#[test]
fn answering_no_is_a_normal_cancel() {
    let fx = Fx::new("");
    fs::write(fx.root().join(".gitignore"), "target/\n").unwrap();
    let before = fx.lock_text();
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(
        &fx,
        &ADD,
        vec![append(".gitignore", "/.tool/\n")],
        tty(true),
        "\n",
    );
    peer.finish();
    assert_eq!(out.code, 0);
    assert_eq!(out.stdout, "No changes were made.\n");
    assert_eq!(
        out.stderr,
        "Append the lines from tool to the existing .gitignore? [y/N] "
    );
    assert_eq!(
        fs::read_to_string(fx.root().join(".gitignore")).unwrap(),
        "target/\n"
    );
    assert!(untouched(&fx, &before));
    assert_eq!(out.log, "");
}

#[test]
fn no_terminal_is_vk0002_without_writes() {
    let fx = Fx::new("");
    fs::write(fx.root().join(".gitignore"), "target/\n").unwrap();
    let before = fx.lock_text();
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(
        &fx,
        &ADD,
        vec![append(".gitignore", "/.tool/\n")],
        tty(false),
        "y\n",
    );
    peer.finish();
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        format!(
            "vendor_kit: error[VK0002]: Confirmation is required, but no terminal is available for interaction. No files were modified except the run log. Run from a terminal, or rerun with -y: just vendor_kit add tool -i {IMAGE} -y\n"
        )
    );
    assert!(untouched(&fx, &before));
}

#[test]
fn yes_answers_the_questions_without_a_terminal() {
    // VK0002 的下一步（把 `-y` 插進原參數）照著跑就會成功。
    let fx = Fx::new("");
    fs::write(fx.root().join(".gitignore"), "target/\n").unwrap();
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(
        &fx,
        &["add", "tool", "-i", IMAGE, "-y"],
        vec![append(".gitignore", "/.tool/\n")],
        tty(false),
        "",
    );
    peer.finish();
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(
        out.stdout,
        format!(
            "Added tool v1.2.0 ({}).\nAppended to .gitignore\n",
            locked()
        )
    );
    assert_eq!(
        fs::read_to_string(fx.root().join(".gitignore")).unwrap(),
        "target/\n/.tool/\n"
    );
}

#[test]
fn yes_does_not_bring_an_existing_whole_file_under_management() {
    // -y 只省略詢問，不擴大授權（04 寫入既有檔的例外）：不適用 append 的既有檔照樣 VK0018。
    let fx = Fx::new("");
    fs::write(fx.root().join("tool.toml"), "mine\n").unwrap();
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(
        &fx,
        &["add", "tool", "-i", IMAGE, "--yes"],
        vec![whole("tool.toml", "[tool]\n")],
        tty(false),
        "",
    );
    peer.finish();
    assert_eq!(out.code, 1);
    assert_eq!(
        out.stderr,
        "vendor_kit: warn[VK0018]: tool.toml already exists and is unmanaged; it was neither overwritten nor brought under management.\n"
    );
    assert_eq!(
        fs::read_to_string(fx.root().join("tool.toml")).unwrap(),
        "mine\n"
    );
    let meta = Metadata::load(&metadata::tool_path(&fx.dir, "tool").unwrap()).unwrap();
    let states: Vec<(&str, &str)> = meta
        .files()
        .iter()
        .map(|r| (r.path.as_str(), r.state.as_str()))
        .collect();
    assert_eq!(states, [("tool.toml", "unmanaged")]);
}

#[test]
fn end_of_input_is_not_consent() {
    let fx = Fx::new("");
    fs::write(fx.root().join(".gitignore"), "target/\n").unwrap();
    let before = fx.lock_text();
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(
        &fx,
        &ADD,
        vec![append(".gitignore", "/.tool/\n")],
        tty(true),
        "",
    );
    peer.finish();
    assert_eq!(out.code, 2);
    assert!(out.stderr.contains("error[VK0002]"), "{}", out.stderr);
    assert!(untouched(&fx, &before));
}

// ---- 停下點 ----

#[test]
fn reserved_name_and_online_add_without_image_path_stop_before_fetching() {
    let fx = Fx::new("");
    let before = fx.lock_text();
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(
        &fx,
        &["add", "vendor_kit", "-i", IMAGE],
        Vec::new(),
        tty(false),
        "",
    );
    assert_eq!(out.code, 2);
    assert!(
        out.stderr.starts_with("vendor_kit: error[VK0057]"),
        "{}",
        out.stderr
    );
    // 線上 add：沒有版本鎖定行又沒給 --image-path，不知道去哪裡查（VK0025）。
    let out = run_add(&fx, &["add", "tool"], Vec::new(), tty(false), "");
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0025]: Required argument is missing: --image-path.\n"
    );
    assert!(peer.finish().is_empty());
    assert!(untouched(&fx, &before));
}

#[test]
fn different_tag_already_added_points_to_upgrade() {
    let other = "ghcr.io/acme/tool:v1.0.0@sha256:3333333333333333333333333333333333333333333333333333333333333333";
    let fx = Fx::new(&format!("tool = \"{other}\"\n"));
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(&fx, &ADD, Vec::new(), tty(false), "");
    assert!(peer.finish().is_empty());
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0045]: Cannot add tool at v1.2.0: it is already imported at v1.0.0. Run: just vendor_kit upgrade tool@v1.2.0\n"
    );
}

#[test]
fn online_add_of_an_added_tool_does_not_query() {
    let fx = Fx::new(&format!("tool = \"{}\"\n", locked()));
    let before = fx.lock_text();
    let peer = Peer::start(&fx, &["tool"], None);
    // 不帶 tag、或同一個 tag：已完整導入，未變更；--image-path 不看（一律讀鎖定行）。
    for argv in [
        &["add", "tool"][..],
        &["add", "tool@v1.2.0", "--image-path", "ghcr.io/acme/other"],
    ] {
        let out = run_add(&fx, argv, Vec::new(), tty(false), "");
        assert_eq!(out.code, 0, "{}", out.stderr);
        assert_eq!(
            out.stdout,
            "tool v1.2.0 is already added; no changes were made.\n"
        );
    }
    // 別的 tag：改用 upgrade（VK0045），不連 registry。
    let out = run_add(&fx, &["add", "tool@v1.3.0"], Vec::new(), tty(false), "");
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0045]: Cannot add tool at v1.3.0: it is already imported at v1.2.0. Run: just vendor_kit upgrade tool@v1.3.0\n"
    );
    assert!(peer.finish().is_empty());
    assert_eq!(fx.lock_text(), before);
}

#[test]
fn online_add_at_a_tag_in_the_local_store_does_not_query() {
    let fx = Fx::new("");
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(
        &fx,
        &["add", "tool@v1.2.0", "--image-path", "ghcr.io/acme/tool"],
        Vec::new(),
        tty(false),
        "",
    );
    assert_eq!(peer.finish(), ["inspect", "extract"]);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, format!("Added tool v1.2.0 ({}).\n", locked()));
    assert!(
        fx.lock_text()
            .ends_with(&format!("[tools]\ntool = \"{}\"\n", locked()))
    );
}

#[test]
fn docker_failures_and_missing_digest() {
    let fx = Fx::new("");
    let before = fx.lock_text();
    let peer = Peer::start(&fx, &["tool"], Some("inspect"));
    let out = run_add(&fx, &ADD, Vec::new(), tty(false), "");
    peer.finish();
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        format!(
            "vendor_kit: error[VK0055]: Cannot access {IMAGE} for tool: docker inspect exited with 1. The requested operation did not complete.\n"
        )
    );
    assert!(untouched(&fx, &before));

    // RepoDigests 沒有 -i 那個名字：VK0031。
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(
        &fx,
        &["add", "tool", "-i", "ghcr.io/acme/other:v1.2.0"],
        Vec::new(),
        tty(false),
        "",
    );
    peer.finish();
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0031]: Cannot use image ghcr.io/acme/other:v1.2.0: it has no repository digest for ghcr.io/acme/other. The supplied image was not used.\n"
    );
    assert!(untouched(&fx, &before));
}

#[test]
fn missing_repo_just_and_init_toml_are_gaps() {
    // 工具內容沒有 just/tool.just（dist 格式不符，沒有代碼）：停下，不寫檔。
    let fx = Fx::new("");
    let before = fx.lock_text();
    let peer = Peer::start(&fx, &["other"], None);
    let out = run_add(&fx, &ADD, Vec::new(), tty(false), "");
    peer.finish();
    assert_eq!(out.code, 2);
    assert!(out.stderr.contains("error[VK0056]"), "{}", out.stderr);
    assert!(untouched(&fx, &before));

    // 工具交付 init.toml：格式未定，正式的讀法停下；沒有就是沒有初始檔。
    let tmp = tempfile::tempdir().unwrap();
    assert_eq!(discover_init_files(tmp.path()).unwrap(), Vec::new());
    fs::write(tmp.path().join(INIT_TOML), "").unwrap();
    assert!(
        discover_init_files(tmp.path())
            .unwrap_err()
            .contains(INIT_TOML)
    );
}

// ---- 恢復 ----

#[test]
fn leftover_add_is_completed_before_the_new_one() {
    let fx = Fx::new("");
    // 上一次 add 建了進度檔就中斷。
    let mut p = Progress::new(VERB, "old", &["add", "tool", "-i", IMAGE]).unwrap();
    let doc = p.document_mut();
    doc.set(&[PROGRESS_TABLE, "repo"], "tool").unwrap();
    doc.set(&[PROGRESS_TABLE, "image"], locked()).unwrap();
    doc.set(&[PROGRESS_TABLE, "repo_files"], false).unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();

    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(&fx, &ADD, Vec::new(), tty(false), "");
    // 恢復：inspect＋extract；接著原本的 add 只 inspect，發現已導入。
    assert_eq!(peer.finish(), ["inspect", "extract", "inspect"]);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "Completed the interrupted add of tool v1.2.0 ({}).\ntool v1.2.0 is already added; no changes were made.\n",
            locked()
        )
    );
    assert!(progress::find(&fx.dir).unwrap().is_empty());
    assert!(fx.lock_text().contains(&locked()));
}

/// 殘留的 `add`：上一次以 [`locked`] 導入 `repo`、沒有 repo 檔要寫，建了進度檔就中斷。
fn leftover(fx: &Fx, repo: &str) {
    let mut p = Progress::new(VERB, "old", &["add", repo, "-i", IMAGE]).unwrap();
    let doc = p.document_mut();
    doc.set(&[PROGRESS_TABLE, "repo"], repo).unwrap();
    doc.set(&[PROGRESS_TABLE, "image"], locked()).unwrap();
    doc.set(&[PROGRESS_TABLE, "repo_files"], false).unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();
}

#[test]
fn leftover_add_waits_for_the_answers_of_this_add() {
    // 恢復跟這次的詢問一起問完，全部同意才一起落地（04 共同選項，#372 N65）：答否時恢復也不寫。
    let fx = Fx::new("");
    fs::write(fx.root().join(".gitignore"), "target/\n").unwrap();
    let before = fx.lock_text();
    leftover(&fx, "other");
    let peer = Peer::start_each(&fx, vec![&["other"], &["tool"]], None);
    let out = run_add(
        &fx,
        &ADD,
        vec![append(".gitignore", "/.tool/\n")],
        tty(true),
        "\n",
    );
    assert_eq!(peer.finish(), ["inspect", "extract", "inspect", "extract"]);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, "No changes were made.\n");
    assert_eq!(
        out.stderr,
        "Append the lines from tool to the existing .gitignore? [y/N] "
    );
    assert_eq!(fx.lock_text(), before);
    assert!(!fx.dir.cache_dir().exists() && !fx.dir.gen_dir().exists());
    assert_eq!(progress::find(&fx.dir).unwrap().len(), 1);
    assert_eq!(out.log, "");

    // 不能互動：VK0002，恢復也不寫，殘留的進度檔照留。每次 session 的 in/ 是新的。
    fs::remove_dir_all(&fx.inbox).unwrap();
    fs::create_dir_all(&fx.inbox).unwrap();
    let peer = Peer::start_each(&fx, vec![&["other"], &["tool"]], None);
    let out = run_add(
        &fx,
        &ADD,
        vec![append(".gitignore", "/.tool/\n")],
        tty(false),
        "",
    );
    peer.finish();
    assert_eq!(out.code, 2);
    assert!(out.stderr.contains("error[VK0002]"), "{}", out.stderr);
    assert_eq!(out.stdout, "");
    assert_eq!(fx.lock_text(), before);
    assert!(!fx.dir.cache_dir().exists() && !fx.dir.gen_dir().exists());
    assert_eq!(progress::find(&fx.dir).unwrap().len(), 1);
}

#[test]
fn leftover_add_lands_before_this_add_once_everything_is_agreed() {
    let fx = Fx::new("");
    fs::write(fx.root().join(".gitignore"), "target/\n").unwrap();
    leftover(&fx, "other");
    let peer = Peer::start_each(&fx, vec![&["other"], &["tool"]], None);
    let out = run_add(
        &fx,
        &ADD,
        vec![append(".gitignore", "/.tool/\n")],
        tty(true),
        "y\n",
    );
    assert_eq!(peer.finish(), ["inspect", "extract", "inspect", "extract"]);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(
        out.stdout.starts_with(&format!(
            "Completed the interrupted add of other v1.2.0 ({0}).\nAdded tool v1.2.0 ({0}).\n",
            locked()
        )),
        "{}",
        out.stdout
    );
    let lock = fx.lock_text();
    assert!(
        lock.contains(&format!("other = \"{}\"", locked()))
            && lock.contains(&format!("tool = \"{}\"", locked())),
        "{lock}"
    );
    // 這次的撞名判定與入口檔以恢復的暫存內容為準（cache/other/ 在判定時還沒換）。
    assert_eq!(
        fs::read_to_string(fx.dir.gen_dir().join("tools.just")).unwrap(),
        "mod? other '../cache/other/just/other.just'\n\
         mod? tool '../cache/tool/just/tool.just'\n"
    );
    assert!(progress::find(&fx.dir).unwrap().is_empty());
}

#[test]
fn two_leftover_adds_each_get_their_own_slot() {
    let fx = Fx::new("");
    for id in ["old1", "old2"] {
        let mut p = Progress::new(VERB, id, &["add", "tool", "-i", IMAGE]).unwrap();
        let doc = p.document_mut();
        doc.set(&[PROGRESS_TABLE, "repo"], "tool").unwrap();
        doc.set(&[PROGRESS_TABLE, "image"], locked()).unwrap();
        doc.set(&[PROGRESS_TABLE, "repo_files"], false).unwrap();
        p.create(&fx.dir, WRITTEN_BY).unwrap();
    }
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(&fx, &ADD, Vec::new(), tty(false), "");
    assert_eq!(
        peer.finish(),
        ["inspect", "extract", "inspect", "extract", "inspect"]
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(fx.inbox.join("tool1").is_dir() && fx.inbox.join("tool2").is_dir());
    assert!(progress::find(&fx.dir).unwrap().is_empty());
}

#[test]
fn progress_records_the_repo_files_to_write() {
    // 落地中途的進度檔記下這次要寫的 repo 檔、內容 hash 與動作（#372 N47、N95）。
    let fx = Fx::new("");
    let registry = Client::with_base_url("http://127.0.0.1:9").unwrap();
    let mut add = Add {
        env: &mut Env {
            dir: &fx.dir,
            host_root: "/h",
            run_log: "/h/log",
            inbox: &fx.inbox,
            channel: &mut Channel::new(&fx.ctl, header()),
            poll: Duration::from_millis(1),
            registry: &registry,
            tty: tty(false),
            argv: &["add".to_owned(), "tool".to_owned()],
            run_id: "r9",
            written_by: WRITTEN_BY,
            stdin: &mut Cursor::new(Vec::new()),
            stdout: &mut Vec::new(),
            prompt: &mut Vec::new(),
            diags: &mut Diagnostics::with_sink(Vec::new(), NoSink),
            log: &mut runlog::Writer::new(
                Vec::new(),
                runlog::Header {
                    version: WRITTEN_BY.to_owned(),
                    component: runlog::Component::Engine,
                    invocation_id: "r9".to_owned(),
                },
            ),
        },
        init: &|_: &Path| Ok(Vec::new()),
        yes: false,
        code: 0,
        extracts: 0,
        stages: 0,
        local: BTreeMap::new(),
        pending: Vec::new(),
    };
    let locked = ImageRef::parse(&locked()).unwrap();
    let files = [
        WrittenFile::new(".gitignore", Some(b"a\n"), b"a\n.tool\n"),
        WrittenFile::new("tool.toml", None, b"x = 1\n"),
    ];
    let Ok(mut p) = add.progress("tool", &locked, &files) else {
        panic!("progress");
    };
    p.create(&fx.dir, WRITTEN_BY).unwrap();
    let back = progress::load(&fx.dir, VERB, "r9").unwrap().unwrap();
    let flag = back
        .document()
        .get(&[PROGRESS_TABLE, "repo_files"])
        .and_then(|i| i.as_bool());
    assert_eq!(flag, Some(true));
    assert_eq!(repo_files::read(&back), Ok(Some(files.to_vec())));

    let Ok(mut p) = add.progress("tool", &locked, &[]) else {
        panic!("progress");
    };
    progress::delete(&fx.dir, VERB, "r9").unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();
    let back = progress::load(&fx.dir, VERB, "r9").unwrap().unwrap();
    assert_eq!(repo_files::read(&back), Ok(None));
}

#[test]
fn leftover_of_another_verb_stops() {
    let fx = Fx::new("");
    let before = fx.lock_text();
    let mut p = Progress::new("remove", "old", &["remove", "x"]).unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(&fx, &ADD, Vec::new(), tty(false), "");
    assert!(peer.finish().is_empty());
    assert_eq!(out.code, 2);
    assert!(
        out.stderr.contains("recovering the incomplete remove operation in .vendor_kit/.tmp.remove.old.toml is not supported yet"),
        "{}",
        out.stderr
    );
    assert_eq!(fx.lock_text(), before);
    assert_eq!(progress::find(&fx.dir).unwrap().len(), 1);
}

// ---- image tar（ADR-0009） ----

const ADD_TAR: [&str; 4] = ["add", "tool", "-i", "dist/tool.tar"];

fn tar_locked() -> String {
    format!("{IMAGE}@{TAR_DIGEST}")
}

#[test]
fn image_tar_pins_the_sidecar_digest() {
    let fx = Fx::new("");
    let peer = TarPeer::start(&fx, TAR);
    let out = run_add(&fx, &ADD_TAR, Vec::new(), tty(false), "");
    assert_eq!(
        peer.finish(),
        [
            "stage /h/proj/dist/tool.digest".to_owned(),
            "load /h/proj/dist/tool.tar".to_owned(),
            format!("inspect {IMAGE}"),
            format!("extract {IMAGE_ID}"),
        ]
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!("Added tool v1.2.0 ({}).\n", tar_locked())
    );
    assert!(
        fx.lock_text()
            .ends_with(&format!("[tools]\ntool = \"{}\"\n", tar_locked()))
    );
    // 同一個 tar 再跑一次：已導入，未變更。
    let peer = TarPeer::start(&fx, TAR);
    let out = run_add(&fx, &ADD_TAR, Vec::new(), tty(false), "");
    assert_eq!(peer.finish().len(), 3);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "tool v1.2.0 is already added; no changes were made.\n"
    );
}

#[test]
fn unnamed_image_tar_takes_the_name_from_repo_tags() {
    let fx = Fx::new("");
    let image = TarImage {
        digest: Some("sha256:4444444444444444444444444444444444444444444444444444444444444444\r\n"),
        load: Some(
            "Loaded image ID: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n",
        ),
        tags: &["tool:dev", IMAGE],
    };
    let peer = TarPeer::start(&fx, image);
    let out = run_add(
        &fx,
        &["add", "tool", "-i", "/srv/img/tool.tar"],
        Vec::new(),
        tty(false),
        "",
    );
    assert_eq!(
        peer.finish(),
        [
            "stage /srv/img/tool.digest".to_owned(),
            "load /srv/img/tool.tar".to_owned(),
            format!("inspect {IMAGE_ID}"),
            format!("extract {IMAGE_ID}"),
        ]
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(fx.lock_text().contains(&tar_locked()));
}

#[test]
fn image_tar_without_a_usable_digest_is_vk0031_before_loading() {
    for digest in [None, Some("sha256:XYZ\n"), Some("")] {
        let fx = Fx::new("");
        let before = fx.lock_text();
        let peer = TarPeer::start(&fx, TarImage { digest, ..TAR });
        let out = run_add(&fx, &ADD_TAR, Vec::new(), tty(false), "");
        assert_eq!(peer.finish(), ["stage /h/proj/dist/tool.digest"]);
        assert_eq!(out.code, 2);
        assert_eq!(out.stdout, "");
        assert_eq!(
            out.stderr,
            "vendor_kit: error[VK0031]: Cannot use image dist/tool.tar: required digest information is missing. The supplied image was not used.\n"
        );
        assert!(untouched(&fx, &before));
    }
}

#[test]
fn image_tar_load_failures_and_names_stop_before_writing() {
    let fx = Fx::new("");
    let before = fx.lock_text();
    let peer = TarPeer::start(&fx, TarImage { load: None, ..TAR });
    let out = run_add(&fx, &ADD_TAR, Vec::new(), tty(false), "");
    assert_eq!(peer.finish().len(), 2);
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0055]: Cannot access dist/tool.tar for tool: docker load exited with 1. The requested operation did not complete.\n"
    );
    assert!(untouched(&fx, &before));

    // load 報了兩個 image、無名 tar 沒有可用的名稱、或有兩個：缺口（VK0056），不寫檔。
    let cases = [
        TarImage {
            load: Some(
                "Loaded image: ghcr.io/acme/tool:v1.2.0\nLoaded image: ghcr.io/acme/x:v1.0.0\n",
            ),
            ..TAR
        },
        TarImage {
            load: Some(
                "Loaded image ID: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n",
            ),
            tags: &[],
            ..TAR
        },
        TarImage {
            load: Some(
                "Loaded image ID: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n",
            ),
            tags: &[IMAGE, "ghcr.io/acme/tool:v1.3.0"],
            ..TAR
        },
    ];
    for (image, what) in
        cases
            .into_iter()
            .zip(["exactly one image", "no ghcr.io", "more than one name"])
    {
        let peer = TarPeer::start(&fx, image);
        let out = run_add(&fx, &ADD_TAR, Vec::new(), tty(false), "");
        peer.finish();
        assert_eq!(out.code, 2);
        assert!(
            out.stderr.starts_with("vendor_kit: error[VK0056]") && out.stderr.contains(what),
            "{}",
            out.stderr
        );
        assert!(untouched(&fx, &before));
    }
}

#[test]
fn image_tar_of_another_tag_points_to_upgrade() {
    let other = "ghcr.io/acme/tool:v1.0.0@sha256:3333333333333333333333333333333333333333333333333333333333333333";
    let fx = Fx::new(&format!("tool = \"{other}\"\n"));
    let before = fx.lock_text();
    let peer = TarPeer::start(&fx, TAR);
    let out = run_add(&fx, &ADD_TAR, Vec::new(), tty(false), "");
    assert_eq!(peer.finish().len(), 3);
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0045]: Cannot add tool at v1.2.0: it is already imported at v1.0.0. Run: just vendor_kit upgrade tool@v1.2.0\n"
    );
    assert_eq!(fx.lock_text(), before);
}

// ---- 其他工具開著本機覆寫 ----

const OTHER: &str = "ghcr.io/acme/other:v1.0.0@sha256:3333333333333333333333333333333333333333333333333333333333333333";

/// `other` 已導入、開著覆寫指到安裝目錄裡的 `work/other`（交付 `other` 與 `other-extra`）；`cache/other/`
/// 不在：開著覆寫的工具不讀它。
fn fx_with_other_override(source: &str) -> Fx {
    let fx = Fx::new(&format!("other = \"{OTHER}\"\n"));
    let just = fx.root().join("work/other/just");
    fs::create_dir_all(&just).unwrap();
    fs::write(just.join("other.just"), "y:\n").unwrap();
    fs::write(just.join("other-extra.just"), "z:\n").unwrap();
    let mut local = LocalFile::new();
    local.set_tool("other", source).unwrap();
    local.save_to(&fx.dir, WRITTEN_BY).unwrap();
    fx
}

#[test]
fn another_tool_override_is_applied_to_the_entry_and_reported() {
    let fx = fx_with_other_override("work/other");
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(&fx, &ADD, Vec::new(), tty(false), "");
    assert_eq!(peer.finish(), ["inspect", "extract"]);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "other uses the local source work/other (local override).\n\
             Added tool v1.2.0 ({}).\n",
            locked()
        )
    );
    assert_eq!(
        fs::read_to_string(fx.dir.gen_dir().join("tools.just")).unwrap(),
        "mod? other '../../work/other/just/other.just'\n\
         mod? other-extra '../../work/other/just/other-extra.just'\n\
         mod? tool '../cache/tool/just/tool.just'\n"
    );

    // 已導入同一版：未變更，照樣報告覆寫。
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(&fx, &ADD, Vec::new(), tty(false), "");
    assert_eq!(peer.finish(), ["inspect"]);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "other uses the local source work/other (local override).\n\
         tool v1.2.0 is already added; no changes were made.\n"
    );
}

#[test]
fn collisions_are_judged_against_the_local_source_of_an_override() {
    let fx = fx_with_other_override("work/other");
    let lock_before = fx.lock_text();
    let peer = Peer::start(&fx, &["tool", "other-extra"], None);
    let out = run_add(&fx, &ADD, Vec::new(), tty(false), "");
    assert_eq!(peer.finish(), ["inspect", "extract"]);
    assert_eq!(out.code, 2);
    assert!(out.stderr.contains("error[VK0030]"), "{}", out.stderr);
    assert!(out.stderr.contains("other-extra"), "{}", out.stderr);
    assert_eq!(out.stdout, "");
    assert!(untouched(&fx, &lock_before));
}

#[test]
fn an_unreadable_override_of_another_tool_is_vk0052_before_any_request() {
    let fx = fx_with_other_override("work/gone");
    let lock_before = fx.lock_text();
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(&fx, &ADD, Vec::new(), tty(false), "");
    assert!(peer.finish().is_empty());
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0052]: Cannot read the local override source work/gone for other: \
         the directory does not exist. Run: just vendor_kit undev other\n"
    );
    assert!(untouched(&fx, &lock_before));
}

#[test]
fn recovering_a_leftover_add_applies_the_override_too() {
    let fx = fx_with_other_override("work/other");
    let mut p = Progress::new(VERB, "old", &["add", "tool", "-i", IMAGE]).unwrap();
    let doc = p.document_mut();
    doc.set(&[PROGRESS_TABLE, "repo"], "tool").unwrap();
    doc.set(&[PROGRESS_TABLE, "image"], locked()).unwrap();
    doc.set(&[PROGRESS_TABLE, "repo_files"], false).unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();
    // 恢復寫好的入口檔，跟著這次的 add（已導入、不重產）留下來。
    let peer = Peer::start(&fx, &["tool"], None);
    let out = run_add(&fx, &ADD, Vec::new(), tty(false), "");
    assert_eq!(peer.finish(), ["inspect", "extract", "inspect"]);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "Completed the interrupted add of tool v1.2.0 ({0}).\n\
             other uses the local source work/other (local override).\n\
             tool v1.2.0 is already added; no changes were made.\n",
            locked()
        )
    );
    assert!(
        fs::read_to_string(fx.dir.gen_dir().join("tools.just"))
            .unwrap()
            .starts_with("mod? other '../../work/other/just/other.just'\n")
    );
}
