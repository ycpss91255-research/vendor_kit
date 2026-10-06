//! 單元測試：以背景的假啟動器回 inspect、pull、extract、`stage` 與 `stage-dir`，跑整段 `upgrade <repo>`。初始檔經 [`run_with`]
//! 直接給（`init.toml` 格式未定，經執行檔做不出會詢問的工具），驗基準版合併、合併衝突、答否、不能互動、
//! `-y`；另驗恢復殘留進度與各個停下點。向假 registry 線上解析 tag 與 digest 的測試在 [`online`]。
#![allow(clippy::unwrap_used, clippy::expect_used)]

mod engine;
mod online;

use std::io::Cursor;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};
use std::thread::{self, JoinHandle};

use diagnostics::NoSink;
use metadata::{FileHash, FileRecord, State};
use plan::{Header, RunId};

use super::*;

const WRITTEN_BY: &str = "v0.0.0";
const ENGINE: &str = "ghcr.io/acme/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const OLD: &str = "ghcr.io/acme/tool:v1.0.0@sha256:3333333333333333333333333333333333333333333333333333333333333333";
const NEW_REF: &str = "ghcr.io/acme/tool:v1.2.0";
const DIGEST: &str = "sha256:2222222222222222222222222222222222222222222222222222222222222222";
const IMAGE_ID: &str = "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";

fn new_locked() -> String {
    format!("{NEW_REF}@{DIGEST}")
}

/// 安裝目錄（工具 `tool` 已在 v1.0.0，`cache/tool/` 有一個 `<ns>`）與 session 目錄。
struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
    ctl: PathBuf,
    inbox: PathBuf,
}

impl Fx {
    fn new() -> Fx {
        let tmp = tempfile::tempdir().unwrap();
        let root = tmp.path().join("root");
        let ctl = tmp.path().join("ctl");
        let inbox = tmp.path().join("in");
        for d in [&root, &ctl, &inbox] {
            fs::create_dir_all(d).unwrap();
        }
        let dir = InstallDir::new(&root);
        fs::create_dir_all(dir.vk_dir()).unwrap();
        fs::write(
            dir.version_toml(),
            format!(
                "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"{OLD}\"\n"
            ),
        )
        .unwrap();
        let just = dir.cache_dir().join("tool/just");
        fs::create_dir_all(&just).unwrap();
        fs::write(just.join("tool.just"), "old:\n").unwrap();
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

    /// 假啟動器的主機目錄：主機路徑 `/h/<x>` 對到這裡的 `<x>`（安裝目錄是 `/h/proj`）。
    fn host(&self) -> PathBuf {
        self._tmp.path().join("host")
    }

    /// 一個已納管的整份型初始檔：基準版副本是 `base`、目前檔是 `now`，紀錄的 hash 是 VK 上次寫的 `base`。
    fn managed(&self, path: &str, base: &str, now: &str) {
        fs::write(self.root().join(path), now).unwrap();
        let copy = self.dir.vk_dir().join(baseline_file("tool", path));
        fs::create_dir_all(copy.parent().unwrap()).unwrap();
        fs::write(copy, base).unwrap();
        let meta_path = metadata::tool_path(&self.dir, "tool").unwrap();
        let mut meta = if meta_path.exists() {
            Metadata::load(&meta_path).unwrap()
        } else {
            Metadata::new()
        };
        let mut record = FileRecord::new(path, State::Managed);
        record.hash = Some(FileHash::of(base.as_bytes()));
        meta.put(record).unwrap();
        fs::create_dir_all(meta_path.parent().unwrap()).unwrap();
        meta.save(&meta_path, WRITTEN_BY).unwrap();
    }

    fn baseline(&self, path: &str) -> String {
        fs::read_to_string(self.dir.vk_dir().join(baseline_file("tool", path))).unwrap()
    }

    fn read(&self, path: &str) -> String {
        fs::read_to_string(self.root().join(path)).unwrap()
    }

    /// `.vendor_kit/` 與 repo 根目錄下每個檔的內容（依路徑排序），比對有沒有任何寫入。
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
        walk(self.root(), &mut out);
        out.sort();
        out
    }
}

fn copy_dir(from: &Path, to: &Path) {
    fs::create_dir(to).unwrap();
    for entry in fs::read_dir(from).unwrap() {
        let entry = entry.unwrap();
        let target = to.join(entry.file_name());
        if entry.file_type().unwrap().is_dir() {
            copy_dir(&entry.path(), &target);
        } else {
            fs::copy(entry.path(), target).unwrap();
        }
    }
}

fn header() -> Header {
    Header::new(1, RunId::parse("r1").unwrap()).unwrap()
}

/// 假啟動器的行為。
#[derive(Clone, Copy)]
struct Script {
    /// extract 放進 `just/<ns>.just` 的 `<ns>`。
    namespaces: &'static [&'static str],
    /// 讓這種 op 回 failed 1。
    fail: Option<&'static str>,
    /// inspect 回的 RepoDigests。
    digests: &'static [&'static str],
    /// 本機有 `<registry>/<路徑>:<tag>`；`false` 時不帶 digest 的 inspect 回 failed 1（帶 digest 的照常，
    /// 當成 pull 進來了）。
    local: bool,
    /// inspect 回的 `Config.Labels`（JSON 物件的內容，不含大括號）；空的就不帶 `Config`。
    labels: &'static str,
}

const NEW: Script = Script {
    namespaces: &["tool"],
    fail: None,
    digests: &[
        "ghcr.io/acme/tool@sha256:2222222222222222222222222222222222222222222222222222222222222222",
    ],
    local: true,
    labels: "",
};

/// 假啟動器：inspect 回 RepoDigests，extract 放進 `just/<ns>.just`；`stage` 與 `stage-dir` 把主機路徑
/// `/h/<x>` 對到的 [`Fx::host`]`/<x>`（檔或目錄）複製進 `in/<slot>`。回傳看到的 op 行。
struct Peer {
    stop: Arc<AtomicBool>,
    handle: JoinHandle<Vec<String>>,
}

impl Peer {
    fn start(fx: &Fx, script: Script) -> Peer {
        // 先清 ctl/ 再起執行緒：新的假啟動器不能讀到上一次的 req.1。
        fx.new_session();
        let (ctl, inbox, host) = (fx.ctl.clone(), fx.inbox.clone(), fx.host());
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
                let line = String::from_utf8_lossy(&bytes)
                    .lines()
                    .nth(1)
                    .unwrap_or_default()
                    .to_owned();
                seen.push(line);
                let outcome = if Some(op.kind().name()) == script.fail {
                    Outcome::Failed(1)
                } else {
                    match &op {
                        // 啟動器不收已存在的 slot（launcher/launch.sh 的 vk_launch_extract）。
                        Op::Extract(_, slot) if inbox.join(slot.as_str()).exists() => {
                            Outcome::Failed(1)
                        }
                        // launcher/launch.sh 的 vk_launch_stage_dir：來源不是目錄或 slot 已存在回 failed 1。
                        Op::StageDir(path, slot) => {
                            let path = String::from_utf8(path.as_bytes().to_vec()).unwrap();
                            let src = path.strip_prefix("/h/").map(|rest| host.join(rest));
                            let dest = inbox.join(slot.as_str());
                            match src {
                                Some(src) if src.is_dir() && !dest.exists() => {
                                    copy_dir(&src, &dest);
                                    Outcome::Ok
                                }
                                _ => Outcome::Failed(1),
                            }
                        }
                        // launcher/launch.sh 的 vk_launch_stage：來源不是檔或 slot 已存在回 failed 1。
                        Op::Stage(path, slot) => {
                            let path = String::from_utf8(path.as_bytes().to_vec()).unwrap();
                            let src = path.strip_prefix("/h/").map(|rest| host.join(rest));
                            let dest = inbox.join(slot.as_str());
                            match src {
                                Some(src) if src.is_file() && !dest.exists() => {
                                    fs::copy(&src, &dest).unwrap();
                                    Outcome::Ok
                                }
                                _ => Outcome::Failed(1),
                            }
                        }
                        Op::Inspect(r) if !script.local && !r.is_pinned() => Outcome::Failed(1),
                        Op::Inspect(_) => {
                            let ds: Vec<String> =
                                script.digests.iter().map(|d| format!("\"{d}\"")).collect();
                            let config = if script.labels.is_empty() {
                                String::new()
                            } else {
                                format!(",\"Config\":{{\"Labels\":{{{}}}}}", script.labels)
                            };
                            let json = format!(
                                "[{{\"Id\":\"{IMAGE_ID}\",\"RepoDigests\":[{}]{config}}}]",
                                ds.join(",")
                            );
                            fs::write(ctl.join(format!("res.{s}.out")), json).unwrap();
                            Outcome::Ok
                        }
                        Op::Extract(_, slot) => {
                            let just = inbox.join(slot.as_str()).join("just");
                            fs::create_dir_all(&just).unwrap();
                            for ns in script.namespaces {
                                fs::write(just.join(format!("{ns}.just")), "new:\n").unwrap();
                            }
                            Outcome::Ok
                        }
                        _ => Outcome::Ok,
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

/// 不該連到 registry 的執行：給一個不會被用到的位址。
fn unused_registry() -> Client {
    Client::with_base_url("http://127.0.0.1:9").unwrap()
}

/// 跑一次 `upgrade`：`argv` 是 `just vendor_kit` 之後的參數，`<repo>[@<tag>]` 與 `-y` 從裡面取。
fn run_upgrade(fx: &Fx, argv: &[&str], init: Vec<OwnedInit>, tty: Tty, input: &str) -> Out {
    let registry = unused_registry();
    let call = Online {
        registry: &registry,
        token_file: None,
    };
    run_online(fx, argv, init, tty, input, &call)
}

/// 線上解析用的 registry 與 `--registry-token-file`。
struct Online<'a> {
    registry: &'a Client,
    token_file: Option<&'a str>,
}

fn run_online(
    fx: &Fx,
    argv: &[&str],
    init: Vec<OwnedInit>,
    tty: Tty,
    input: &str,
    online: &Online<'_>,
) -> Out {
    let target = argv[1];
    let (repo, tag) = match target.split_once('@') {
        Some((r, t)) => (r, Some(Tag::parse(t).unwrap())),
        None => (target, None),
    };
    let req = Request {
        repo,
        tag,
        yes: argv.contains(&"-y"),
        registry_token_file: online.token_file.map(OsStr::new),
    };
    let argv: Vec<String> = argv.iter().map(|s| (*s).to_owned()).collect();
    fx.assert_fresh_session();
    let mut channel = Channel::new(&fx.ctl, header());
    let mut stdin = Cursor::new(input.as_bytes().to_vec());
    let mut stdout = Vec::new();
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
            registry: online.registry,
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

fn whole(path: &str, contents: &str) -> OwnedInit {
    OwnedInit {
        path: path.to_owned(),
        strategy: Strategy::Whole,
        contents: contents.as_bytes().to_vec(),
    }
}

const UPGRADE: [&str; 2] = ["upgrade", "tool@v1.2.0"];
const UPGRADE_Y: [&str; 3] = ["upgrade", "tool@v1.2.0", "-y"];

fn upgraded_line() -> String {
    format!("Upgraded tool from v1.0.0 to v1.2.0 ({}).\n", new_locked())
}

/// 換版之後的版本鎖定行、`cache/`、印記、入口檔都指向新版，進度檔不在。
fn assert_landed(fx: &Fx) {
    assert!(
        fx.lock_text()
            .ends_with(&format!("[tools]\ntool = \"{}\"\n", new_locked())),
        "{}",
        fx.lock_text()
    );
    assert_eq!(
        fs::read_to_string(fx.dir.cache_dir().join("tool/just/tool.just")).unwrap(),
        "new:\n"
    );
    let stamp = stamp::Stamp::load(&stamp::tool_file(&fx.dir, "tool"))
        .unwrap()
        .unwrap();
    assert_eq!(stamp.version(), new_locked());
    assert_eq!(
        fs::read_to_string(fx.dir.gen_dir().join("tools.just")).unwrap(),
        "mod? tool '../cache/tool/just/tool.just'\n"
    );
    assert!(progress::find(&fx.dir).unwrap().is_empty());
}

// ---- 成功 ----

#[test]
fn upgrade_to_a_local_tag_lands_everything_and_the_lock_line_last() {
    let fx = Fx::new();
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
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
    assert_landed(&fx);
    let events: Vec<&str> = out
        .log
        .lines()
        .map(|l| {
            let rest = l.split_once("\"event_name\":\"").unwrap().1;
            rest.split_once('"').unwrap().0
        })
        .collect();
    assert_eq!(
        events,
        [
            "writes_started",
            "lock_line_write_started",
            "lock_line_written",
            "progress_removed"
        ]
    );
}

#[test]
fn same_tag_is_unchanged_without_any_docker_action() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(&fx, &["upgrade", "tool@v1.0.0"], Vec::new(), tty(false), "");
    assert!(peer.finish().is_empty());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "tool is already at v1.0.0; no changes were made.\n"
    );
    assert_eq!(out.stderr, "");
    assert_eq!(fx.snapshot(), before);
    assert_eq!(out.log, "");
}

#[test]
fn downgrade_to_an_older_tag_is_allowed() {
    let fx = Fx::new();
    let peer = Peer::start(
        &fx,
        Script {
            digests: &[
                "ghcr.io/acme/tool@sha256:4444444444444444444444444444444444444444444444444444444444444444",
            ],
            ..NEW
        },
    );
    let out = run_upgrade(&fx, &["upgrade", "tool@v0.9.0"], Vec::new(), tty(false), "");
    peer.finish();
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(
        out.stdout.starts_with(
            "Upgraded tool from v1.0.0 to v0.9.0 (ghcr.io/acme/tool:v0.9.0@sha256:4444"
        ),
        "{}",
        out.stdout
    );
}

// ---- 初始檔 ----

#[test]
fn modified_init_file_is_merged_with_the_baseline_after_asking() {
    let fx = Fx::new();
    fx.managed(
        "tool.toml",
        "a = 1\nb = 2\nc = 3\n",
        "a = 1\nb = 2\nc = 3\nmine = 1\n",
    );
    let peer = Peer::start(&fx, NEW);
    let init = vec![whole("tool.toml", "a = 10\nb = 2\nc = 3\n")];
    let out = run_upgrade(&fx, &UPGRADE, init, tty(true), "y\n");
    peer.finish();
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stderr,
        "Merge the new version of tool.toml from tool? [y/N] "
    );
    assert_eq!(out.stdout, format!("{}Merged tool.toml\n", upgraded_line()));
    assert_eq!(fx.read("tool.toml"), "a = 10\nb = 2\nc = 3\nmine = 1\n");
    assert_eq!(fx.baseline("tool.toml"), "a = 10\nb = 2\nc = 3\n");
    assert_landed(&fx);
}

#[test]
fn unmodified_init_file_is_replaced_and_its_hash_follows() {
    let fx = Fx::new();
    fx.managed("tool.toml", "v = 1\n", "v = 1\n");
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(
        &fx,
        &UPGRADE,
        vec![whole("tool.toml", "v = 2\n")],
        tty(true),
        "y\n",
    );
    peer.finish();
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stderr,
        "Replace tool.toml with the new version from tool? [y/N] "
    );
    assert_eq!(fx.read("tool.toml"), "v = 2\n");
    assert_eq!(fx.baseline("tool.toml"), "v = 2\n");
    let meta = Metadata::load(&metadata::tool_path(&fx.dir, "tool").unwrap()).unwrap();
    assert_eq!(
        meta.get("tool.toml").unwrap().hash,
        Some(FileHash::of(b"v = 2\n"))
    );
}

#[test]
fn merge_conflict_leaves_markers_and_warns_vk0021() {
    let fx = Fx::new();
    fx.managed("tool.conf", "v = 1\n", "v = mine\n");
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(
        &fx,
        &UPGRADE_Y,
        vec![whole("tool.conf", "v = 2\n")],
        tty(false),
        "",
    );
    peer.finish();
    assert_eq!(out.code, 1, "{}", out.stderr);
    assert_eq!(
        out.stderr,
        "vendor_kit: warn[VK0021]: tool.conf contains merge conflicts. Review and resolve them: git status\n"
    );
    let merged = fx.read("tool.conf");
    assert!(merged.contains("<<<<<<<"), "{merged}");
    assert!(merged.contains("v = mine"), "{merged}");
    assert!(merged.contains("v = 2"), "{merged}");
    // 合併留下衝突時基準版照樣推到新版。
    assert_eq!(fx.baseline("tool.conf"), "v = 2\n");
    let meta = Metadata::load(&metadata::tool_path(&fx.dir, "tool").unwrap()).unwrap();
    assert!(meta.conflicts().is_empty(), "{:?}", meta.conflicts());
    assert_landed(&fx);
}

#[test]
fn unparsable_toml_merge_keeps_the_file_and_records_conflicts() {
    let fx = Fx::new();
    fx.managed("config.toml", "v = 1\n", "v = \"mine\"\n");
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(
        &fx,
        &UPGRADE_Y,
        vec![whole("config.toml", "v = 2\n")],
        tty(false),
        "",
    );
    peer.finish();
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(
        out.stdout,
        format!(
            "{}Kept config.toml: the merged version is not valid TOML; recorded in conflicts\n",
            upgraded_line()
        )
    );
    // 留原檔、該檔基準版不推、記入 metadata `conflicts`（scope_roadmap:32）。
    assert_eq!(fx.read("config.toml"), "v = \"mine\"\n");
    assert_eq!(fx.baseline("config.toml"), "v = 1\n");
    let meta = Metadata::load(&metadata::tool_path(&fx.dir, "tool").unwrap()).unwrap();
    assert_eq!(meta.conflicts(), ["config.toml"]);
    assert_landed(&fx);
}

#[test]
fn successful_merge_clears_a_recorded_conflict() {
    let fx = Fx::new();
    fx.managed(
        "config.toml",
        "a = 1\nb = 2\nc = 3\n",
        "a = 1\nb = 2\nc = 3\nmine = 1\n",
    );
    let meta_path = metadata::tool_path(&fx.dir, "tool").unwrap();
    let mut meta = Metadata::load(&meta_path).unwrap();
    meta.set_conflict("config.toml", true).unwrap();
    meta.save(&meta_path, WRITTEN_BY).unwrap();
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(
        &fx,
        &UPGRADE_Y,
        vec![whole("config.toml", "a = 10\nb = 2\nc = 3\n")],
        tty(false),
        "",
    );
    peer.finish();
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(fx.read("config.toml"), "a = 10\nb = 2\nc = 3\nmine = 1\n");
    assert_eq!(fx.baseline("config.toml"), "a = 10\nb = 2\nc = 3\n");
    let meta = Metadata::load(&meta_path).unwrap();
    assert!(meta.conflicts().is_empty(), "{:?}", meta.conflicts());
    assert_landed(&fx);
}

#[test]
fn answering_no_writes_nothing() {
    let fx = Fx::new();
    fx.managed("tool.toml", "v = 1\n", "v = 1\n");
    let before = fx.snapshot();
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(
        &fx,
        &UPGRADE,
        vec![whole("tool.toml", "v = 2\n")],
        tty(true),
        "n\n",
    );
    peer.finish();
    assert_eq!(out.code, 0);
    assert_eq!(out.stdout, "No changes were made.\n");
    assert_eq!(fx.snapshot(), before);
    assert_eq!(out.log, "");
}

#[test]
fn no_terminal_is_vk0002_with_y_appended() {
    let fx = Fx::new();
    fx.managed("tool.toml", "v = 1\n", "v = 1\n");
    let before = fx.snapshot();
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(
        &fx,
        &UPGRADE,
        vec![whole("tool.toml", "v = 2\n")],
        tty(false),
        "y\n",
    );
    peer.finish();
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0002]: Confirmation is required, but no terminal is available for interaction. No files were modified except the run log. Run from a terminal, or rerun with -y: just vendor_kit upgrade tool@v1.2.0 -y\n"
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn yes_skips_every_question() {
    let fx = Fx::new();
    fx.managed("tool.toml", "v = 1\n", "v = 1\n");
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(
        &fx,
        &UPGRADE_Y,
        vec![whole("tool.toml", "v = 2\n")],
        tty(false),
        "",
    );
    peer.finish();
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(
        out.stdout,
        format!("{}Updated tool.toml\n", upgraded_line())
    );
    assert_eq!(fx.read("tool.toml"), "v = 2\n");
}

#[test]
fn deleted_and_no_longer_provided_files_are_listed_not_recreated() {
    let fx = Fx::new();
    fx.managed("gone.toml", "g = 1\n", "g = 1\n");
    fx.managed("tool.toml", "v = 1\n", "v = 1\n");
    fs::remove_file(fx.root().join("tool.toml")).unwrap();
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(
        &fx,
        &UPGRADE,
        vec![whole("tool.toml", "v = 2\n")],
        tty(false),
        "",
    );
    peer.finish();
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "{}Not recreated (deleted): tool.toml\nKept (no longer provided by tool v1.2.0): gone.toml\n",
            upgraded_line()
        )
    );
    assert!(!fx.root().join("tool.toml").exists());
    assert_eq!(fx.read("gone.toml"), "g = 1\n");
    let meta = Metadata::load(&metadata::tool_path(&fx.dir, "tool").unwrap()).unwrap();
    assert_eq!(meta.get("tool.toml").unwrap().state, State::Deleted);
    assert_eq!(meta.get("gone.toml").unwrap().state, State::Managed);
}

#[test]
fn init_toml_from_the_tool_is_a_gap() {
    let tmp = tempfile::tempdir().unwrap();
    assert_eq!(discover_init_files(tmp.path()), Ok(Vec::new()));
    fs::write(tmp.path().join(INIT_TOML), "").unwrap();
    assert!(
        discover_init_files(tmp.path())
            .unwrap_err()
            .contains("format is not specified yet")
    );
}

// ---- 停下點 ----

fn assert_gap(out: &Out, needle: &str) {
    assert_eq!(out.code, 2, "{}", out.stderr);
    assert!(
        out.stderr
            .starts_with("vendor_kit: error[VK0056]: Internal vendor_kit error: "),
        "{}",
        out.stderr
    );
    assert!(out.stderr.contains(needle), "{needle}: {}", out.stderr);
    assert_eq!(out.stdout, "");
}

#[test]
fn stops_before_fetching() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(
        &fx,
        &["upgrade", "other@v1.0.0"],
        Vec::new(),
        tty(false),
        "",
    );
    assert_gap(
        &out,
        "upgrade of other, which is not in the lock version lines",
    );
    assert!(peer.finish().is_empty());
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn same_tag_with_init_file_records_is_a_gap() {
    let fx = Fx::new();
    fx.managed("tool.toml", "v = 1\n", "v = 1\n");
    let before = fx.snapshot();
    let out = run_upgrade(&fx, &["upgrade", "tool@v1.0.0"], Vec::new(), tty(false), "");
    assert_gap(&out, "judging whether the baseline of tool is behind");
    assert_eq!(fx.snapshot(), before);
    // 不帶 tag 也一樣：在讀 token 檔、連 registry 之前停下（registry 給的是連不到的位址）。
    let out = run_upgrade(&fx, &["upgrade", "tool"], Vec::new(), tty(false), "");
    assert_gap(&out, "judging whether the baseline of tool is behind");
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn extract_failure_is_vk0055() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let peer = Peer::start(
        &fx,
        Script {
            fail: Some("extract"),
            ..NEW
        },
    );
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    peer.finish();
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        format!(
            "vendor_kit: error[VK0055]: Cannot access {} for tool: docker extract exited with 1. The requested operation did not complete.\n",
            new_locked()
        )
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn namespace_collision_is_a_gap() {
    let fx = Fx::new();
    fs::write(
        fx.dir.version_toml(),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nother = \"ghcr.io/acme/other:v1.0.0@{DIGEST}\"\ntool = \"{OLD}\"\n"
        ),
    )
    .unwrap();
    let just = fx.dir.cache_dir().join("other/just");
    fs::create_dir_all(&just).unwrap();
    fs::write(just.join("other.just"), "x:\n").unwrap();
    fs::write(just.join("shared.just"), "x:\n").unwrap();
    let before = fx.snapshot();
    let peer = Peer::start(
        &fx,
        Script {
            namespaces: &["tool", "shared"],
            ..NEW
        },
    );
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    peer.finish();
    assert_gap(&out, "colliding namespaces: shared (used by other)");
    assert_eq!(fx.snapshot(), before);
}

// ---- 本機覆寫 ----

/// `version.local.toml` 的工具覆寫（`<repo>` → 本機開發來源）。
fn overrides(fx: &Fx, tools: &[(&str, &str)]) {
    let lines: Vec<String> = tools
        .iter()
        .map(|(r, d)| format!("{r} = \"{d}\"\n"))
        .collect();
    fs::write(
        fx.dir.version_local_toml(),
        format!(
            "schema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\n{}",
            lines.concat()
        ),
    )
    .unwrap();
}

/// 安裝目錄裡的本機開發來源 `dir`，交付 `just/<ns>.just`。
fn local_source(fx: &Fx, dir: &str, namespaces: &[&str]) {
    let just = fx.root().join(dir).join("just");
    fs::create_dir_all(&just).unwrap();
    for ns in namespaces {
        fs::write(just.join(format!("{ns}.just")), "local:\n").unwrap();
    }
}

#[test]
fn local_override_of_the_target_upgrades_and_keeps_the_entry_on_the_local_source() {
    let fx = Fx::new();
    local_source(&fx, "work/tool", &["tool", "extra"]);
    overrides(&fx, &[("tool", "./work/tool")]);
    let local_toml = fs::read(fx.dir.version_local_toml()).unwrap();
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert_eq!(
        peer.finish(),
        [
            format!("inspect {NEW_REF}"),
            format!("extract {IMAGE_ID} tool1")
        ]
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "tool uses the local source work/tool (local override).\n{}",
            upgraded_line()
        )
    );
    assert_eq!(out.stderr, "");
    // 版本鎖定行、`cache/`、印記照常換；入口檔用本機開發來源的 `<ns>`，指向本機目錄。
    assert!(
        fx.lock_text()
            .ends_with(&format!("tool = \"{}\"\n", new_locked()))
    );
    assert_eq!(
        fs::read_to_string(fx.dir.cache_dir().join("tool/just/tool.just")).unwrap(),
        "new:\n"
    );
    let stamp = stamp::Stamp::load(&stamp::tool_file(&fx.dir, "tool"))
        .unwrap()
        .unwrap();
    assert_eq!(stamp.version(), new_locked());
    assert_eq!(
        fs::read_to_string(fx.dir.gen_dir().join("tools.just")).unwrap(),
        "mod? extra '../../work/tool/just/extra.just'\nmod? tool '../../work/tool/just/tool.just'\n"
    );
    assert_eq!(fs::read(fx.dir.version_local_toml()).unwrap(), local_toml);
    assert!(progress::find(&fx.dir).unwrap().is_empty());

    // 已是該版：照樣報告覆寫。每次執行的 ctl 目錄是新的。
    fx.new_session();
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "tool uses the local source work/tool (local override).\ntool is already at v1.2.0; no changes were made.\n"
    );
}

#[test]
fn local_override_of_another_tool_keeps_its_entry_lines_and_namespaces() {
    let fx = Fx::new();
    fs::write(
        fx.dir.version_toml(),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nother = \"ghcr.io/acme/other:v1.0.0@{DIGEST}\"\ntool = \"{OLD}\"\n"
        ),
    )
    .unwrap();
    let cache = fx.dir.cache_dir().join("other/just");
    fs::create_dir_all(&cache).unwrap();
    fs::write(cache.join("other.just"), "x:\n").unwrap();
    // 本機開發來源多交付 `shared`：撞名判定以生效的本機開發來源為準。
    local_source(&fx, "dev/other", &["other", "shared"]);
    overrides(&fx, &[("other", "dev/other")]);
    let before = fx.snapshot();
    let peer = Peer::start(
        &fx,
        Script {
            namespaces: &["tool", "shared"],
            ..NEW
        },
    );
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    peer.finish();
    assert_gap(&out, "colliding namespaces: shared (used by other)");
    assert_eq!(fx.snapshot(), before);

    // 每次執行的收件目錄是新的。
    fs::remove_dir_all(&fx.inbox).unwrap();
    fs::create_dir_all(&fx.inbox).unwrap();
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    peer.finish();
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "other uses the local source dev/other (local override).\n{}",
            upgraded_line()
        )
    );
    assert_eq!(
        fs::read_to_string(fx.dir.gen_dir().join("tools.just")).unwrap(),
        "mod? other '../../dev/other/just/other.just'\nmod? shared '../../dev/other/just/shared.just'\nmod? tool '../cache/tool/just/tool.just'\n"
    );
}

#[test]
fn unreadable_local_source_is_vk0052_before_any_docker_action() {
    let fx = Fx::new();
    overrides(&fx, &[("tool", "work/missing")]);
    let before = fx.snapshot();
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert!(peer.finish().is_empty());
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0052]: Cannot read the local override source work/missing for tool: the directory does not exist. Run: just vendor_kit undev tool\n"
    );
    assert_eq!(fx.snapshot(), before);
}

/// 主機上安裝目錄（`/h/proj`）外的本機開發來源 `/h/<dir>`，交付 `just/<ns>.just`。
fn outside_source(fx: &Fx, dir: &str, namespaces: &[&str]) {
    fs::create_dir_all(fx.host().join("proj")).unwrap();
    let just = fx.host().join(dir).join("just");
    fs::create_dir_all(&just).unwrap();
    for ns in namespaces {
        fs::write(just.join(format!("{ns}.just")), "local:\n").unwrap();
    }
}

#[test]
fn outside_local_source_is_staged_before_the_upgrade_and_the_entry_points_at_it() {
    let fx = Fx::new();
    outside_source(&fx, "elsewhere/tool", &["tool", "extra"]);
    overrides(&fx, &[("tool", "/h/elsewhere/tool")]);
    let local_toml = fs::read(fx.dir.version_local_toml()).unwrap();
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert_eq!(
        peer.finish(),
        [
            "stage-dir e:/h/elsewhere/tool dev1".to_owned(),
            format!("inspect {NEW_REF}"),
            format!("extract {IMAGE_ID} tool1")
        ],
        "stage-dir has its own slot numbering"
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "tool uses the local source /h/elsewhere/tool (local override).\n{}",
            upgraded_line()
        )
    );
    assert_eq!(out.stderr, "");
    assert!(
        fx.lock_text()
            .ends_with(&format!("tool = \"{}\"\n", new_locked()))
    );
    assert_eq!(
        fs::read_to_string(fx.dir.cache_dir().join("tool/just/tool.just")).unwrap(),
        "new:\n"
    );
    assert_eq!(
        fs::read_to_string(fx.dir.gen_dir().join("tools.just")).unwrap(),
        "mod? extra '/h/elsewhere/tool/just/extra.just'\nmod? tool '/h/elsewhere/tool/just/tool.just'\n"
    );
    assert_eq!(fs::read(fx.dir.version_local_toml()).unwrap(), local_toml);
    assert!(progress::find(&fx.dir).unwrap().is_empty());
}

#[test]
fn relative_outside_local_source_of_another_tool_is_staged_from_under_the_host_root() {
    let fx = Fx::new();
    fs::write(
        fx.dir.version_toml(),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nother = \"ghcr.io/acme/other:v1.0.0@{DIGEST}\"\ntool = \"{OLD}\"\n"
        ),
    )
    .unwrap();
    outside_source(&fx, "other", &["other"]);
    overrides(&fx, &[("other", "../other")]);
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert_eq!(peer.finish()[0], "stage-dir e:/h/proj/../other dev1");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        fs::read_to_string(fx.dir.gen_dir().join("tools.just")).unwrap(),
        "mod? other '../../../other/just/other.just'\nmod? tool '../cache/tool/just/tool.just'\n"
    );
}

#[test]
fn outside_local_source_that_cannot_be_copied_is_vk0052_before_any_docker_action() {
    let fx = Fx::new();
    overrides(&fx, &[("tool", "/h/nowhere")]);
    let before = fx.snapshot();
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert_eq!(peer.finish(), ["stage-dir e:/h/nowhere dev1"]);
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0052]: Cannot read the local override source /h/nowhere for tool: the launcher could not copy it (exit 1): it does not exist, is not a directory, or cannot be read. Run: just vendor_kit undev tool\n"
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn recovering_a_residual_upgrade_keeps_the_override_in_the_entry() {
    let fx = Fx::new();
    local_source(&fx, "work/tool", &["tool"]);
    overrides(&fx, &[("tool", "work/tool")]);
    residual(&fx, "tool", &new_locked(), false);
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    peer.finish();
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "Completed the interrupted upgrade of tool to v1.2.0 ({}).\ntool uses the local source work/tool (local override).\ntool is already at v1.2.0; no changes were made.\n",
            new_locked()
        )
    );
    assert_eq!(
        fs::read_to_string(fx.dir.gen_dir().join("tools.just")).unwrap(),
        "mod? tool '../../work/tool/just/tool.just'\n"
    );
    assert!(progress::find(&fx.dir).unwrap().is_empty());
}

#[test]
fn override_of_a_tool_without_a_lock_line_is_a_gap() {
    let fx = Fx::new();
    local_source(&fx, "work/ghost", &["ghost"]);
    overrides(&fx, &[("ghost", "work/ghost")]);
    let before = fx.snapshot();
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert_gap(&out, "(no reason code)");
    assert_eq!(fx.snapshot(), before);
}

// ---- 恢復 ----

/// 殘留的工具 `upgrade` 進度檔（別次執行 `r0`）。
fn residual(fx: &Fx, target: &str, image: &str, init_files: bool) {
    let mut p = Progress::new(VERB, "r0", &["upgrade", "tool@v1.2.0", "-y"]).unwrap();
    let doc = p.document_mut();
    doc.set(&[table::TABLE, table::TARGET], target).unwrap();
    doc.set(&[table::TABLE, table::IMAGE], image).unwrap();
    doc.set(&[table::TABLE, table::INIT_FILES], init_files)
        .unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();
}

#[test]
fn residual_upgrade_is_recovered_before_judging_the_repeat() {
    let fx = Fx::new();
    residual(&fx, "tool", &new_locked(), false);
    let peer = Peer::start(&fx, NEW);
    // 恢復之後版本鎖定行已是 v1.2.0：同一個 tag 就是未變更。
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert_eq!(
        peer.finish(),
        [
            format!("inspect ghcr.io/acme/tool@{DIGEST}"),
            format!("extract {IMAGE_ID} tool1"),
        ]
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "Completed the interrupted upgrade of tool to v1.2.0 ({}).\ntool is already at v1.2.0; no changes were made.\n",
            new_locked()
        )
    );
    assert_landed(&fx);
}

#[test]
fn residual_upgrade_pulls_by_digest_when_the_image_is_not_local() {
    let fx = Fx::new();
    residual(&fx, "tool", &new_locked(), false);
    // 第一次 inspect 失敗、pull 成功；這個假啟動器讓所有 inspect 都失敗，所以停在 pull 後的 inspect。
    let peer = Peer::start(
        &fx,
        Script {
            fail: Some("inspect"),
            ..NEW
        },
    );
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    let pinned = format!("ghcr.io/acme/tool@{DIGEST}");
    assert_eq!(
        peer.finish(),
        [
            format!("inspect {pinned}"),
            format!("pull {pinned}"),
            format!("inspect {pinned}"),
        ]
    );
    assert_eq!(out.code, 2);
    assert!(
        out.stderr.contains("error[VK0055]: Cannot access"),
        "{}",
        out.stderr
    );
    // 進度檔還在，下次照樣認得出來。
    assert_eq!(progress::find(&fx.dir).unwrap().len(), 1);
}

#[test]
fn residuals_that_cannot_be_recovered_are_gaps() {
    let fx = Fx::new();
    residual(&fx, "tool", &new_locked(), true);
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert_gap(&out, "which writes init files");

    let fx = Fx::new();
    residual(&fx, table::ENGINE_TARGET, ENGINE, false);
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert_gap(&out, "recovering the incomplete engine upgrade");

    let fx = Fx::new();
    Progress::new("add", "r0", &["add", "new", "-i", "x"])
        .unwrap()
        .create(&fx.dir, WRITTEN_BY)
        .unwrap();
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert_gap(&out, "upgrade while the incomplete add operation");
}

#[test]
fn progress_records_the_upgrade_table_while_landing() {
    // 落地中途的進度檔要讓 update 認得：`[upgrade]` 的 target、image、init_files 與原指令。
    let fx = Fx::new();
    let mut up = Upgrade {
        env: &mut Env {
            dir: &fx.dir,
            host_root: "/h",
            run_log: "/h/log",
            inbox: &fx.inbox,
            channel: &mut Channel::new(&fx.ctl, header()),
            poll: Duration::from_millis(1),
            registry: &unused_registry(),
            tty: tty(false),
            argv: &["upgrade".to_owned(), "tool@v1.2.0".to_owned()],
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
        code: 0,
        extracts: 0,
        stages: 0,
        local: BTreeMap::new(),
        engine: false,
    };
    let locked = ImageRef::parse(&new_locked()).unwrap();
    let Ok(mut p) = up.progress(&["upgrade", "tool@v1.2.0"], "tool", &locked, true) else {
        panic!("progress");
    };
    p.create(&fx.dir, WRITTEN_BY).unwrap();
    let back = progress::load(&fx.dir, VERB, "r9").unwrap().unwrap();
    assert_eq!(table::field(&back, table::TARGET), Some("tool"));
    assert_eq!(
        table::field(&back, table::IMAGE),
        Some(new_locked().as_str())
    );
    assert_eq!(table::flag(&back, table::INIT_FILES), Some(true));
    assert_eq!(back.command(), ["upgrade", "tool@v1.2.0"]);
}
