//! 單元測試：以背景的假啟動器回 inspect、pull 與 extract，跑整段 `upgrade <repo>`。初始檔經 [`run_with`]
//! 直接給（`init.toml` 格式未定，經執行檔做不出會詢問的工具），驗基準版合併、合併衝突、答否、不能互動、
//! `-y`；另驗恢復殘留進度與各個停下點。
#![allow(clippy::unwrap_used, clippy::expect_used)]

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
                "vendor_kit = \"{ENGINE}\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"{OLD}\"\n"
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

    fn root(&self) -> &Path {
        self.dir.root()
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
}

const NEW: Script = Script {
    namespaces: &["tool"],
    fail: None,
    digests: &[
        "ghcr.io/acme/tool@sha256:2222222222222222222222222222222222222222222222222222222222222222",
    ],
};

/// 假啟動器：inspect 回 RepoDigests，extract 放進 `just/<ns>.just`。回傳看到的 op 行。
struct Peer {
    stop: Arc<AtomicBool>,
    handle: JoinHandle<Vec<String>>,
}

impl Peer {
    fn start(fx: &Fx, script: Script) -> Peer {
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
                        Op::Inspect(_) => {
                            let ds: Vec<String> =
                                script.digests.iter().map(|d| format!("\"{d}\"")).collect();
                            let json = format!(
                                "[{{\"Id\":\"{IMAGE_ID}\",\"RepoDigests\":[{}]}}]",
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

/// 跑一次 `upgrade`：`argv` 是 `just vendor_kit` 之後的參數，`<repo>[@<tag>]` 與 `-y` 從裡面取。
fn run_upgrade(fx: &Fx, argv: &[&str], init: Vec<OwnedInit>, tty: Tty, input: &str) -> Out {
    let target = argv[1];
    let (repo, tag) = match target.split_once('@') {
        Some((r, t)) => (r, Some(Tag::parse(t).unwrap())),
        None => (target, None),
    };
    let req = Request {
        repo,
        tag,
        yes: argv.contains(&"-y"),
    };
    let argv: Vec<String> = argv.iter().map(|s| (*s).to_owned()).collect();
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
        "mod tool '../cache/tool/just/tool.just'\n"
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
    fx.managed("tool.toml", "v = 1\n", "v = mine\n");
    let peer = Peer::start(&fx, NEW);
    let out = run_upgrade(
        &fx,
        &UPGRADE_Y,
        vec![whole("tool.toml", "v = 2\n")],
        tty(false),
        "",
    );
    peer.finish();
    assert_eq!(out.code, 1, "{}", out.stderr);
    assert_eq!(
        out.stderr,
        "vendor_kit: warn[VK0021]: tool.toml contains merge conflicts. Review and resolve them: git status\n"
    );
    let merged = fx.read("tool.toml");
    assert!(merged.contains("<<<<<<<"), "{merged}");
    assert!(merged.contains("v = mine"), "{merged}");
    assert!(merged.contains("v = 2"), "{merged}");
    // 合併留下衝突時基準版照樣推到新版。
    assert_eq!(fx.baseline("tool.toml"), "v = 2\n");
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
    let out = run_upgrade(&fx, &["upgrade", "tool"], Vec::new(), tty(false), "");
    assert_gap(&out, "upgrade tool without @<tag> (listing tags");
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
}

#[test]
fn tag_that_is_not_a_local_image_is_a_gap() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let peer = Peer::start(
        &fx,
        Script {
            fail: Some("inspect"),
            ..NEW
        },
    );
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert_eq!(peer.finish(), [format!("inspect {NEW_REF}")]);
    assert_gap(&out, "which is not a local image");
    assert_eq!(fx.snapshot(), before);

    let peer = Peer::start(
        &fx,
        Script {
            digests: &[],
            ..NEW
        },
    );
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    peer.finish();
    assert_gap(&out, "without a repository digest for ghcr.io/acme/tool");
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
            "vendor_kit = \"{ENGINE}\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nother = \"ghcr.io/acme/other:v1.0.0@{DIGEST}\"\ntool = \"{OLD}\"\n"
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

#[test]
fn local_override_is_a_gap() {
    let fx = Fx::new();
    fs::write(
        fx.dir.version_local_toml(),
        "schema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"../tool\"\n",
    )
    .unwrap();
    let before = fx.snapshot();
    let out = run_upgrade(&fx, &UPGRADE, Vec::new(), tty(false), "");
    assert_gap(&out, "upgrade while tool has a local override");
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
