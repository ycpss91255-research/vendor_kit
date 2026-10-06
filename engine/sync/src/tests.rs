//! 單元測試：以背景的假啟動器回 inspect、pull 與 extract，跑整段 `sync`。驗各種印記與 `cache/` 狀態的
//! 判定、逐工具處理前的停下點、殘留進度檔，以及只用救援路徑的 op。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::collections::BTreeSet;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};
use std::thread::{self, JoinHandle};

use diagnostics::NoSink;
use plan::{Header, RunId};
use progress::Progress;

use super::*;

const WRITTEN_BY: &str = "v0.0.0";
const ENGINE: &str = "ghcr.io/acme/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";

/// 薄殼四檔的模板本文（順序同 `layout::SHELL_FILES`）。
const BODIES: [&str; 4] = ["# entry\n", "# vendor\n", "# log\n", "cache/\ngen/\n"];

fn templates() -> [Vec<u8>; 4] {
    BODIES.map(|b| b.as_bytes().to_vec())
}

/// 一個假工具：名字、digest 的 hex 字元與交付的 `<ns>`。
struct Tool {
    name: &'static str,
    hex: char,
    namespaces: &'static [&'static str],
}

const TOOL: Tool = Tool {
    name: "tool",
    hex: '2',
    namespaces: &["tool", "tool-extra"],
};
/// 同一個工具的另一版（v1.3.0）。
const TOOL_V13: Tool = Tool {
    name: "tool",
    hex: '4',
    namespaces: &["tool", "tool-extra"],
};
const OTHER: Tool = Tool {
    name: "other",
    hex: '3',
    namespaces: &["other"],
};

impl Tool {
    fn digest(&self) -> String {
        format!("sha256:{}", self.hex.to_string().repeat(64))
    }
    fn locked(&self) -> String {
        format!("ghcr.io/acme/{}:v1.2.0@{}", self.name, self.digest())
    }
    fn line(&self) -> String {
        format!("{} = \"{}\"\n", self.name, self.locked())
    }
    fn pinned(&self) -> String {
        format!("ghcr.io/acme/{}@{}", self.name, self.digest())
    }
}

/// 安裝目錄與 session 目錄。
struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
    ctl: PathBuf,
    inbox: PathBuf,
}

impl Fx {
    fn new(tools: &[&Tool]) -> Fx {
        let tmp = tempfile::tempdir().unwrap();
        let root = tmp.path().join("root");
        let ctl = tmp.path().join("ctl");
        let inbox = tmp.path().join("in");
        for d in [&root, &ctl, &inbox] {
            fs::create_dir_all(d).unwrap();
        }
        let dir = InstallDir::new(&root);
        fs::create_dir_all(dir.vk_dir()).unwrap();
        let lines: String = tools.iter().map(|t| t.line()).collect();
        let tools = if lines.is_empty() {
            String::new()
        } else {
            format!("\n[tools]\n{lines}")
        };
        fs::write(
            dir.version_toml(),
            format!("vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n{tools}"),
        )
        .unwrap();
        let bodies = BODIES.map(str::as_bytes);
        let shell = Shell::render(compat::THIS.current_protocol, WRITTEN_BY, bodies).unwrap();
        shell.write(&dir).unwrap();
        Fx {
            _tmp: tmp,
            dir,
            ctl,
            inbox,
        }
    }

    /// 每次執行的 session 目錄是新的。
    fn new_session(&self) {
        for d in [&self.ctl, &self.inbox] {
            fs::remove_dir_all(d).unwrap();
            fs::create_dir_all(d).unwrap();
        }
    }

    fn entry(&self) -> Option<String> {
        fs::read_to_string(self.dir.gen_dir().join("tools.just")).ok()
    }

    fn stamp(&self, repo: &str) -> Option<Stamp> {
        Stamp::load(&stamp::tool_file(&self.dir, repo)).unwrap()
    }
}

/// 一個工具交付的內容：`just/<ns>.just` 各一檔，外加一個一般檔。
fn content(dir: &Path, namespaces: &[&str]) {
    let just = dir.join("just");
    fs::create_dir_all(&just).unwrap();
    for ns in namespaces {
        fs::write(just.join(format!("{ns}.just")), "x:\n").unwrap();
    }
    fs::create_dir_all(dir.join("share")).unwrap();
    fs::write(dir.join("share/readme.txt"), "tool files\n").unwrap();
}

/// 假啟動器的行為。
#[derive(Clone, Default)]
struct Behavior {
    /// 一開始本機有哪些 image（依 pinned 引用）；不在的 inspect 回 failed 1，pull 之後才有。
    local: BTreeSet<String>,
    /// 這個 op 一律回 failed 1。
    fail: Option<&'static str>,
    /// inspect 回的 RepoDigests 換成這個 digest（digest 不符）。
    wrong_digest: Option<String>,
}

/// 假啟動器：認得 [`TOOL`] 與 [`OTHER`]；image ID 就是 digest。
struct Peer {
    stop: Arc<AtomicBool>,
    handle: JoinHandle<Vec<String>>,
}

impl Peer {
    fn start(fx: &Fx, behavior: Behavior) -> Peer {
        let (ctl, inbox) = (fx.ctl.clone(), fx.inbox.clone());
        let stop = Arc::new(AtomicBool::new(false));
        let flag = Arc::clone(&stop);
        let local = Arc::new(Mutex::new(behavior.local.clone()));
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
                let outcome = if Some(op.kind().name()) == behavior.fail {
                    Outcome::Failed(1)
                } else {
                    match &op {
                        Op::Inspect(r) if !local.lock().unwrap().contains(r.as_str()) => {
                            Outcome::Failed(1)
                        }
                        Op::Inspect(r) => {
                            let (name, digest) = r.as_str().split_once('@').unwrap();
                            let shown = behavior.wrong_digest.as_deref().unwrap_or(digest);
                            let json = format!(
                                "[{{\"Id\":\"{digest}\",\"RepoDigests\":[\"{name}@{shown}\"]}}]"
                            );
                            fs::write(ctl.join(format!("res.{s}.out")), json).unwrap();
                            Outcome::Ok
                        }
                        Op::Pull(r) => {
                            local.lock().unwrap().insert(r.as_str().to_owned());
                            Outcome::Ok
                        }
                        // 啟動器不收已存在的 slot（launcher/launch.sh 的 vk_launch_extract）。
                        Op::Extract(_, slot) if inbox.join(slot.as_str()).exists() => {
                            Outcome::Failed(1)
                        }
                        Op::Extract(id, slot) => {
                            let tool = [&TOOL, &TOOL_V13, &OTHER]
                                .into_iter()
                                .find(|t| t.digest() == id.as_str())
                                .unwrap();
                            content(&inbox.join(slot.as_str()), tool.namespaces);
                            Outcome::Ok
                        }
                        _ => Outcome::Failed(1),
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

/// 兩個工具的 image 都在本機。
fn all_local() -> Behavior {
    Behavior {
        local: [TOOL.pinned(), OTHER.pinned()].into_iter().collect(),
        ..Behavior::default()
    }
}

struct Out {
    code: u8,
    stdout: String,
    stderr: String,
    log: String,
    ops: Vec<String>,
}

impl Out {
    fn events(&self) -> Vec<String> {
        self.log
            .lines()
            .map(|l| {
                let rest = l.split_once("\"event_name\":\"").unwrap().1;
                rest.split_once('"').unwrap().0.to_owned()
            })
            .collect()
    }
}

fn run_sync(fx: &Fx, behavior: Behavior) -> Out {
    run_sync_with(fx, behavior, Some(&templates()))
}

fn run_sync_with(fx: &Fx, behavior: Behavior, shell_templates: Option<&[Vec<u8>; 4]>) -> Out {
    fx.new_session();
    let peer = Peer::start(fx, behavior);
    let mut channel = Channel::new(&fx.ctl, header());
    let mut stdout = Vec::new();
    let mut stderr = Vec::new();
    let mut diags = Diagnostics::with_sink(&mut stderr, NoSink);
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
            written_by: WRITTEN_BY,
            shell_templates,
            stdout: &mut stdout,
            diags: &mut diags,
            log: &mut log,
        };
        run(&mut env)
    };
    let ops = peer.finish();
    Out {
        code,
        stdout: String::from_utf8(stdout).unwrap(),
        stderr: String::from_utf8(stderr).unwrap(),
        log: String::from_utf8(log.into_inner()).unwrap(),
        ops,
    }
}

const BOTH_GEN: &str = "mod? other '../cache/other/just/other.just'\n\
                        mod? tool '../cache/tool/just/tool.just'\n\
                        mod? tool-extra '../cache/tool/just/tool-extra.just'\n";

/// 先同步一次，回傳之後要比對的 `version.toml`。
fn synced(fx: &Fx) -> Vec<u8> {
    let out = run_sync(fx, all_local());
    assert_eq!(out.code, 0, "{}", out.stderr);
    fs::read(fx.dir.version_toml()).unwrap()
}

// ---- 成功 ----

#[test]
fn fresh_checkout_fetches_every_tool_and_writes_gen() {
    let fx = Fx::new(&[&TOOL, &OTHER]);
    let lock_before = fs::read(fx.dir.version_toml()).unwrap();
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(
        out.stdout,
        format!(
            "Fetched other v1.2.0 ({}).\nFetched tool v1.2.0 ({}).\nUpdated .vendor_kit/gen/tools.just.\n",
            OTHER.locked(),
            TOOL.locked()
        )
    );
    assert_eq!(
        out.ops,
        ["inspect", "extract", "inspect", "extract"],
        "BTreeMap order: other, then tool"
    );
    assert_eq!(fx.entry().unwrap(), BOTH_GEN);
    for t in [&TOOL, &OTHER] {
        assert_eq!(fx.stamp(t.name).unwrap().version(), t.locked());
        let cache = fx.dir.tool_cache(t.name).unwrap();
        assert!(cache.join("share/readme.txt").is_file());
    }
    // 版本鎖定行不動（sync 不改追蹤檔）。
    assert_eq!(fs::read(fx.dir.version_toml()).unwrap(), lock_before);
    assert!(progress::find(&fx.dir).unwrap().is_empty());
    assert_eq!(out.events(), ["writes_started"], "no lock line events");
}

#[test]
fn already_synced_does_nothing() {
    let fx = Fx::new(&[&TOOL, &OTHER]);
    let lock = synced(&fx);
    let stamp_before = fs::read(stamp::tool_file(&fx.dir, "tool")).unwrap();
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, "");
    assert_eq!(out.stderr, "");
    assert!(out.ops.is_empty());
    assert!(out.log.is_empty());
    assert_eq!(fs::read(fx.dir.version_toml()).unwrap(), lock);
    assert_eq!(
        fs::read(stamp::tool_file(&fx.dir, "tool")).unwrap(),
        stamp_before
    );
    assert_eq!(fx.entry().unwrap(), BOTH_GEN);
}

#[test]
fn image_not_local_is_pulled_by_digest() {
    let fx = Fx::new(&[&TOOL]);
    let out = run_sync(&fx, Behavior::default());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.ops, ["inspect", "pull", "inspect", "extract"]);
}

#[test]
fn only_rescue_path_ops_are_used() {
    // ADR-0008：sync 的判定是救援路徑，只准用凍結的 op 子集。
    let fx = Fx::new(&[&TOOL, &OTHER]);
    let out = run_sync(&fx, Behavior::default());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(!out.ops.is_empty());
    for op in &out.ops {
        assert!(plan::RESCUE_OPS.contains(&op.as_str()), "{op}");
    }
}

#[test]
fn no_tools_writes_an_empty_entry_once() {
    let fx = Fx::new(&[]);
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, "Updated .vendor_kit/gen/tools.just.\n");
    assert_eq!(fx.entry().unwrap(), "");
    let again = run_sync(&fx, all_local());
    assert_eq!(again.stdout, "");
    assert!(again.log.is_empty());
}

#[test]
fn changed_and_extra_cache_files_are_refetched_with_vk0015() {
    let fx = Fx::new(&[&TOOL, &OTHER]);
    synced(&fx);
    let cache = fx.dir.tool_cache("tool").unwrap();
    fs::write(cache.join("share/readme.txt"), "edited\n").unwrap();
    fs::write(cache.join("share/extra.txt"), "extra\n").unwrap();

    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 1, "{}", out.stderr);
    assert_eq!(out.ops, ["inspect", "extract"], "only tool is refetched");
    assert_eq!(
        out.stdout,
        format!("Fetched tool v1.2.0 ({}).\n", TOOL.locked())
    );
    assert_eq!(
        out.stderr,
        "vendor_kit: warn[VK0015]: The file set or per-file digests in cache/ for tool did not match; refetched according to the lock version line.\n"
    );
    assert_eq!(
        fs::read_to_string(cache.join("share/readme.txt")).unwrap(),
        "tool files\n"
    );
    assert!(!cache.join("share/extra.txt").exists());
    assert_eq!(fx.entry().unwrap(), BOTH_GEN);
}

#[test]
fn missing_cache_directory_with_a_stamp_is_refetched_with_vk0015() {
    let fx = Fx::new(&[&TOOL]);
    synced(&fx);
    fs::remove_dir_all(fx.dir.tool_cache("tool").unwrap()).unwrap();
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 1);
    assert!(out.stderr.contains("warn[VK0015]"), "{}", out.stderr);
    assert!(fx.dir.tool_cache("tool").unwrap().join("just").is_dir());
}

#[test]
fn corrupt_stamp_is_rebuilt_with_vk0044() {
    let fx = Fx::new(&[&TOOL]);
    synced(&fx);
    fs::write(stamp::tool_file(&fx.dir, "tool"), "not toml [").unwrap();
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 1);
    assert_eq!(
        out.stderr,
        "vendor_kit: warn[VK0044]: The existing stamp for tool was corrupt; refetched according to the lock version line and rebuilt the stamp.\n"
    );
    assert_eq!(fx.stamp("tool").unwrap().version(), TOOL.locked());
}

#[test]
fn lock_line_changed_since_the_stamp_refetches_without_warning() {
    let fx = Fx::new(&[&TOOL]);
    synced(&fx);
    // 鎖定行換成另一版（例如 git pull 換了版本）。
    let new_locked = format!("ghcr.io/acme/tool:v1.3.0@{}", TOOL_V13.digest());
    let moved = format!(
        "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"{new_locked}\"\n"
    );
    fs::write(fx.dir.version_toml(), &moved).unwrap();
    let behavior = Behavior {
        local: [TOOL_V13.pinned()].into_iter().collect(),
        ..Behavior::default()
    };
    let out = run_sync(&fx, behavior);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(fx.stamp("tool").unwrap().version(), new_locked);
    assert_eq!(fs::read_to_string(fx.dir.version_toml()).unwrap(), moved);
}

#[test]
fn landing_writes_no_progress_file() {
    let fx = Fx::new(&[&TOOL]);
    synced(&fx);
    // 換到一半斷掉的樣子：cache/ 少了一個檔。重跑就是恢復，照樣不建進度檔。
    let cache = fx.dir.tool_cache("tool").unwrap();
    fs::remove_file(cache.join("share/readme.txt")).unwrap();
    let out = run_sync(&fx, all_local());
    // VK0015 是警告：結束碼 1。
    assert_eq!(out.code, 1, "{}", out.stderr);
    assert!(out.stderr.contains("warn[VK0015]"), "{}", out.stderr);
    assert!(progress::find(&fx.dir).unwrap().is_empty());
    let names: Vec<String> = fs::read_dir(fx.dir.vk_dir())
        .unwrap()
        .map(|e| e.unwrap().file_name().to_string_lossy().into_owned())
        .collect();
    assert!(names.iter().all(|n| !n.starts_with(".tmp.")), "{names:?}");
    assert_eq!(out.events(), ["writes_started"]);
}

// ---- 停下 ----

/// `.vendor_kit/` 下 `cache/`、`gen/` 都沒建，也沒有進度檔。
fn untouched(fx: &Fx, lock_before: &[u8]) -> bool {
    fs::read(fx.dir.version_toml()).unwrap() == lock_before
        && !fx.dir.cache_dir().exists()
        && !fx.dir.gen_dir().exists()
        && progress::find(&fx.dir).unwrap().is_empty()
}

#[test]
fn digest_mismatch_is_vk0043_and_lands_nothing() {
    let fx = Fx::new(&[&TOOL, &OTHER]);
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    let behavior = Behavior {
        wrong_digest: Some(format!("sha256:{}", "9".repeat(64))),
        ..all_local()
    };
    let out = run_sync(&fx, behavior);
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    // 每個工具的原因都列出來（02 不變量 4）。
    assert_eq!(
        out.stderr.matches("error[VK0043]").count(),
        2,
        "{}",
        out.stderr
    );
    assert!(out.stderr.contains(&format!(
        "Downloaded image {} for tool does not match locked digest {}. Synchronization did not complete.",
        TOOL.locked(),
        TOOL.digest()
    )));
    assert!(!out.stderr.contains("VK0015"));
    assert!(untouched(&fx, &lock));
    assert!(out.log.is_empty());
}

#[test]
fn pull_failure_is_vk0055() {
    let fx = Fx::new(&[&TOOL]);
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    let behavior = Behavior {
        fail: Some("pull"),
        ..Behavior::default()
    };
    let out = run_sync(&fx, behavior);
    assert_eq!(out.code, 2);
    assert_eq!(out.ops, ["inspect", "pull"]);
    assert_eq!(
        out.stderr,
        format!(
            "vendor_kit: error[VK0055]: Cannot access {} for tool: docker pull exited with 1. The requested operation did not complete.\n",
            TOOL.locked()
        )
    );
    assert!(untouched(&fx, &lock));
}

const VK0006_FIX: &str = "No shell files were regenerated. Review the following differences; \
                          download bootstrap.sh again from the Release, run chmod +x bootstrap.sh, \
                          then run ./bootstrap.sh --repair in the install directory.";

#[test]
fn shell_mismatch_is_vk0006_before_any_fetch() {
    let fx = Fx::new(&[&TOOL]);
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    let log_sh = fx.dir.vk_dir().join("log.sh");
    let mut changed = fs::read(&log_sh).unwrap();
    changed.extend_from_slice(b"echo extra\n");
    fs::write(&log_sh, changed).unwrap();
    fs::remove_file(fx.dir.vk_dir().join("vendor.just")).unwrap();
    let shell_before: Vec<Option<Vec<u8>>> = fx
        .dir
        .shell_files()
        .iter()
        .map(|p| fs::read(p).ok())
        .collect();
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 2);
    assert!(out.ops.is_empty());
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        format!(
            "vendor_kit: error[VK0006]: Shell files do not match this engine version's templates: \
             .vendor_kit/vendor.just (missing), .vendor_kit/log.sh (modified). {VK0006_FIX}\n"
        )
    );
    assert!(untouched(&fx, &lock));
    let shell_after: Vec<Option<Vec<u8>>> = fx
        .dir
        .shell_files()
        .iter()
        .map(|p| fs::read(p).ok())
        .collect();
    assert_eq!(shell_after, shell_before);
}

#[test]
fn shell_of_another_engine_version_is_vk0006() {
    let fx = Fx::new(&[&TOOL]);
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    let bodies = BODIES.map(str::as_bytes);
    let other = Shell::render(compat::THIS.current_protocol, "v9.9.9", bodies).unwrap();
    other.write(&fx.dir).unwrap();
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 2);
    assert!(out.ops.is_empty());
    assert!(
        out.stderr.starts_with(
            "vendor_kit: error[VK0006]: Shell files do not match this engine version's templates: \
             .vendor_kit/entry.just (not this engine version's template), "
        ),
        "{}",
        out.stderr
    );
    assert!(untouched(&fx, &lock));
}

/// 薄殼不符跟其他逐工具處理前的停下原因一起列出（02 不變量 4）。
#[test]
fn shell_mismatch_is_listed_with_the_other_blockers() {
    let fx = Fx::new(&[&TOOL]);
    fs::write(fx.dir.vk_dir().join("entry.just"), "changed\n").unwrap();
    let mut p = Progress::new(ADD_VERB, "old1", &["add", "other"]).unwrap();
    p.document_mut().set(&[ADD_VERB, "repo"], "other").unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 2);
    assert!(out.ops.is_empty());
    assert_eq!(
        out.stderr,
        format!(
            "vendor_kit: error[VK0006]: Shell files do not match this engine version's templates: \
             .vendor_kit/entry.just (modified). {VK0006_FIX}\n\
             vendor_kit: error[VK0004]: Import of other is incomplete. Run: just vendor_kit add other\n"
        )
    );
}

#[test]
fn shell_matching_with_crlf_line_endings_syncs() {
    let fx = Fx::new(&[&TOOL]);
    for path in fx.dir.shell_files() {
        let text = fs::read_to_string(&path).unwrap();
        fs::write(&path, text.replace('\n', "\r\n")).unwrap();
    }
    let behavior = Behavior {
        local: [TOOL.pinned()].into_iter().collect(),
        ..Behavior::default()
    };
    let out = run_sync(&fx, behavior);
    assert_eq!(out.code, 0, "{}", out.stderr);
}

#[test]
fn missing_shell_templates_is_vk0056_before_any_fetch() {
    let fx = Fx::new(&[&TOOL]);
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    let out = run_sync_with(&fx, all_local(), None);
    assert_eq!(out.code, 2);
    assert!(out.ops.is_empty());
    assert!(
        out.stderr.starts_with(
            "vendor_kit: error[VK0056]: Internal vendor_kit error: \
             sync without the shell templates, which this engine image does not ship"
        ),
        "{}",
        out.stderr
    );
    assert!(untouched(&fx, &lock));
}

#[test]
fn residual_add_is_vk0004_before_any_fetch() {
    let fx = Fx::new(&[&TOOL]);
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    let mut p = Progress::new(ADD_VERB, "old1", &["add", "other"]).unwrap();
    p.document_mut().set(&[ADD_VERB, "repo"], "other").unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 2);
    assert!(out.ops.is_empty());
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0004]: Import of other is incomplete. Run: just vendor_kit add other\n"
    );
    assert_eq!(fs::read(fx.dir.version_toml()).unwrap(), lock);
    assert!(!fx.dir.cache_dir().exists());
    assert_eq!(progress::find(&fx.dir).unwrap().len(), 1);
}

#[test]
fn stamp_schema_too_new_is_fatal_before_any_fetch() {
    let fx = Fx::new(&[&TOOL]);
    synced(&fx);
    let cache = fx.dir.tool_cache("tool").unwrap();
    fs::write(cache.join("share/readme.txt"), "edited\n").unwrap();
    fs::write(
        stamp::tool_file(&fx.dir, "tool"),
        "schema = 99\nwritten_by = \"v9.0.0\"\nversion = \"x\"\n",
    )
    .unwrap();
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 3);
    assert!(out.ops.is_empty());
    assert!(
        out.stderr.starts_with("vendor_kit: fatal[VK0008]: "),
        "{}",
        out.stderr
    );
    assert!(
        out.stderr.contains(".vendor_kit/cache/tool.stamp.toml"),
        "{}",
        out.stderr
    );
    // 零寫入：被改過的 cache 也不重取。
    assert_eq!(
        fs::read_to_string(cache.join("share/readme.txt")).unwrap(),
        "edited\n"
    );
}

/// `tool` 開著本機覆寫，指到安裝目錄裡的 `work/tool/`（交付 `tool`、`tool-extra`）。
fn override_tool(fx: &Fx, source: &str) {
    content(&fx.dir.root().join("work/tool"), TOOL.namespaces);
    fs::write(
        fx.dir.version_local_toml(),
        format!("schema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"{source}\"\n"),
    )
    .unwrap();
}

const OVERRIDE_GEN: &str = "mod? other '../cache/other/just/other.just'\n\
                            mod? tool '../../work/tool/just/tool.just'\n\
                            mod? tool-extra '../../work/tool/just/tool-extra.just'\n";

#[test]
fn local_override_uses_the_local_source_and_other_tools_sync_as_usual() {
    let fx = Fx::new(&[&TOOL, &OTHER]);
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    override_tool(&fx, "./work/x/../tool");
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(out.ops, ["inspect", "extract"], "only other is fetched");
    assert_eq!(
        out.stdout,
        format!(
            "tool uses the local source work/tool (local override).\n\
             Fetched other v1.2.0 ({}).\n\
             Updated .vendor_kit/gen/tools.just.\n",
            OTHER.locked()
        )
    );
    assert_eq!(fx.entry().unwrap(), OVERRIDE_GEN);
    // 覆寫的工具不取件、不寫 cache/ 與印記；其他工具照常。
    assert!(!fx.dir.tool_cache("tool").unwrap().exists());
    assert!(fx.stamp("tool").is_none());
    assert_eq!(fx.stamp("other").unwrap().version(), OTHER.locked());
    assert_eq!(fs::read(fx.dir.version_toml()).unwrap(), lock);
    assert!(progress::find(&fx.dir).unwrap().is_empty());

    // 再 sync：沒有變更，照樣報告用了哪個覆寫，什麼都不寫。
    let again = run_sync(&fx, all_local());
    assert_eq!(again.code, 0, "{}", again.stderr);
    assert!(again.ops.is_empty());
    assert_eq!(
        again.stdout,
        "tool uses the local source work/tool (local override).\n"
    );
    assert!(again.log.is_empty());
    assert_eq!(fx.entry().unwrap(), OVERRIDE_GEN);
}

#[test]
fn local_override_keeps_the_locked_cache_untouched() {
    let fx = Fx::new(&[&TOOL]);
    synced(&fx);
    let cache = fx.dir.tool_cache("tool").unwrap();
    let stamp_before = fs::read(stamp::tool_file(&fx.dir, "tool")).unwrap();
    // 鎖定版本的 cache 被改過：覆寫期間 sync 不看它。
    fs::write(cache.join("share/readme.txt"), "edited\n").unwrap();
    override_tool(&fx, "work/tool");
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert!(out.ops.is_empty());
    assert_eq!(
        fx.entry().unwrap(),
        "mod? tool '../../work/tool/just/tool.just'\n\
         mod? tool-extra '../../work/tool/just/tool-extra.just'\n"
    );
    assert_eq!(
        fs::read_to_string(cache.join("share/readme.txt")).unwrap(),
        "edited\n"
    );
    assert_eq!(
        fs::read(stamp::tool_file(&fx.dir, "tool")).unwrap(),
        stamp_before
    );
}

#[test]
fn unreadable_local_source_is_vk0052_and_writes_nothing() {
    let fx = Fx::new(&[&TOOL, &OTHER]);
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    fs::write(
        fx.dir.version_local_toml(),
        "schema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"work/tool\"\n",
    )
    .unwrap();
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 2);
    assert!(out.ops.is_empty(), "other is not fetched either");
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0052]: Cannot read the local override source work/tool for tool: the directory does not exist. Run: just vendor_kit undev tool\n"
    );
    assert!(untouched(&fx, &lock));
    assert!(out.log.is_empty());
}

#[test]
fn override_without_a_lock_version_line_stops_as_a_gap() {
    let fx = Fx::new(&[&OTHER]);
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    override_tool(&fx, "work/tool");
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 2);
    assert!(out.ops.is_empty());
    assert!(
        out.stderr.starts_with("vendor_kit: error[VK0056]: "),
        "{}",
        out.stderr
    );
    assert!(out.stderr.contains("tool"), "{}", out.stderr);
    assert!(untouched(&fx, &lock));
}

#[test]
fn residual_undev_is_vk0053_and_is_left_in_place() {
    let fx = Fx::new(&[&TOOL]);
    synced(&fx);
    let entry_before = fx.entry().unwrap();
    let mut p = Progress::new(UNDEV_VERB, "old1", &["undev", "tool"]).unwrap();
    p.document_mut()
        .set(&[UNDEV_VERB, UNDEV_TARGET_KEY], "tool")
        .unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();
    // 入口檔還指著本機目錄（undev 解除覆寫後、入口檔寫好前斷掉）。
    fs::write(
        fx.dir.gen_dir().join("tools.just"),
        "mod? tool '../../work/tool/just/tool.just'\n",
    )
    .unwrap();
    let out = run_sync(&fx, all_local());
    assert_eq!(out.code, 2);
    assert!(out.ops.is_empty());
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0053]: The undev operation for tool is incomplete. Run again: just vendor_kit undev tool\n"
    );
    // sync 不代替 undev 完成或清掉進度檔。
    assert_eq!(progress::find(&fx.dir).unwrap().len(), 1);
    assert_ne!(fx.entry().unwrap(), entry_before);
}

/// 留一份 `verb` 的進度檔，`[<table>] <key>` 填 `value`（`table` 是 `None` 就只有共同欄位）。
fn residual(fx: &Fx, verb: &str, command: &[&str], field: Option<(&str, &str, &str)>) {
    let mut p = Progress::new(verb, "old1", command).unwrap();
    if let Some((table, key, value)) = field {
        p.document_mut().set(&[table, key], value).unwrap();
    }
    p.create(&fx.dir, WRITTEN_BY).unwrap();
}

/// 殘留的進度檔讓 `sync` 在取件前停下：版本鎖定行與 `cache/` 不動，進度檔留著。
fn stopped_by_residual(fx: &Fx, lock: &[u8], out: &Out) {
    assert_eq!(out.code, 2, "{}", out.stderr);
    assert!(out.ops.is_empty());
    assert_eq!(out.stdout, "");
    assert!(out.events().is_empty(), "{:?}", out.events());
    assert_eq!(fs::read(fx.dir.version_toml()).unwrap(), lock);
    assert!(!fx.dir.cache_dir().exists());
    assert_eq!(progress::find(&fx.dir).unwrap().len(), 1);
}

#[test]
fn residual_tool_upgrade_is_vk0041_with_the_original_command() {
    let fx = Fx::new(&[&TOOL]);
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    residual(
        &fx,
        UPGRADE_VERB,
        &["upgrade", "tool@v1.3.0", "-y"],
        Some((progress::upgrade::TABLE, progress::upgrade::TARGET, "tool")),
    );
    let out = run_sync(&fx, all_local());
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0041]: Upgrade of tool is incomplete. Run again: just vendor_kit upgrade tool@v1.3.0 -y\n"
    );
    stopped_by_residual(&fx, &lock, &out);
}

#[test]
fn residual_engine_upgrade_stops_as_a_gap_with_the_original_command() {
    let fx = Fx::new(&[&TOOL]);
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    residual(
        &fx,
        UPGRADE_VERB,
        &["upgrade", "--engine", "-y"],
        Some((
            progress::upgrade::TABLE,
            progress::upgrade::TARGET,
            progress::upgrade::ENGINE_TARGET,
        )),
    );
    let out = run_sync(&fx, all_local());
    assert!(
        out.stderr.starts_with("vendor_kit: error[VK0056]: "),
        "{}",
        out.stderr
    );
    assert!(
        out.stderr
            .contains("incomplete engine upgrade in .vendor_kit/.tmp.upgrade.old1.toml"),
        "{}",
        out.stderr
    );
    assert!(
        out.stderr
            .contains("run again: just vendor_kit upgrade --engine -y"),
        "{}",
        out.stderr
    );
    stopped_by_residual(&fx, &lock, &out);
}

#[test]
fn residual_of_another_writing_recipe_is_vk0054_with_the_original_command() {
    for (verb, command) in [
        ("remove", &["remove", "tool"][..]),
        ("install", &["install", "-y"][..]),
        ("dev", &["dev", "tool", "-p", "my dir"][..]),
    ] {
        let fx = Fx::new(&[&TOOL]);
        let lock = fs::read(fx.dir.version_toml()).unwrap();
        residual(&fx, verb, command, None);
        let out = run_sync(&fx, all_local());
        let shown = full_command(command);
        assert_eq!(
            out.stderr,
            format!(
                "vendor_kit: error[VK0054]: Operation {verb} in /h/proj is incomplete. Run again: {shown}\n"
            ),
            "{verb}"
        );
        stopped_by_residual(&fx, &lock, &out);
    }
}

#[test]
fn residual_sync_progress_stops_as_a_gap_instead_of_asking_to_rerun_sync() {
    let fx = Fx::new(&[&TOOL]);
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    residual(&fx, VERB, &["sync"], None);
    let out = run_sync(&fx, all_local());
    assert!(
        out.stderr.starts_with("vendor_kit: error[VK0056]: "),
        "{}",
        out.stderr
    );
    assert!(
        out.stderr.contains(".vendor_kit/.tmp.sync.old1.toml"),
        "{}",
        out.stderr
    );
    stopped_by_residual(&fx, &lock, &out);
}

#[test]
fn inspect_output_parsing() {
    let d = format!("sha256:{}", "2".repeat(64));
    let json = format!("[{{\"Id\":\"{d}\",\"RepoDigests\":[\"ghcr.io/a/t@{d}\"],\"Size\":1}}]");
    let i = parse_inspect(json.as_bytes()).unwrap();
    assert_eq!(i.id, d);
    assert_eq!(i.repo_digests, [format!("ghcr.io/a/t@{d}")]);
    let none = parse_inspect(br#"[{"Id":"sha256:1","RepoDigests":null}]"#).unwrap();
    assert!(none.repo_digests.is_empty());
    assert!(parse_inspect(b"[]").is_err());
    assert!(parse_inspect(b"{}").is_err());
    assert!(parse_inspect(b"not json").is_err());
}
