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
            format!("vendor_kit = \"{ENGINE}\"\nschema = 1\nwritten_by = \"v0.0.0\"\n{tools}"),
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
        // 先清 ctl/ 再起執行緒：新的假啟動器不能讀到上一次的 req.1。
        fx.new_session();
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
    let image = argv
        .iter()
        .position(|a| *a == "-i")
        .map(|i| OsStr::new(argv[i + 1]));
    let req = Request {
        repo: argv[1],
        tag: None,
        image,
    };
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
fn reserved_name_and_online_add_stop_before_fetching() {
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
    let out = run_add(&fx, &["add", "tool"], Vec::new(), tty(false), "");
    assert_eq!(out.code, 2);
    assert!(
        out.stderr
            .starts_with("vendor_kit: error[VK0056]: Internal vendor_kit error: add without -i"),
        "{}",
        out.stderr
    );
    let out = run_add(
        &fx,
        &["add", "tool", "-i", "./tool.tar"],
        Vec::new(),
        tty(false),
        "",
    );
    assert!(out.stderr.contains("image tar"), "{}", out.stderr);
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
