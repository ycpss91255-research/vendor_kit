//! 單元測試：以背景的假啟動器回 `ps` 與 `rm-container`，跑整段 `prune`。驗清理範圍（未鎖定的工具目錄與
//! 印記、VK 暫存、已停止容器）、不動的東西（鎖定的工具、進度檔、工具內容裡的 `.tmp.*`）、刪任何東西之前的
//! 停下點，以及殘留的 `prune` 進度檔。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex};
use std::thread::{self, JoinHandle};

use diagnostics::NoSink;
use plan::{Header, RunId};

use super::*;

const WRITTEN_BY: &str = "v0.0.0";
const ENGINE: &str = "ghcr.io/acme/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const TOOL: &str = "tool = \"ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222\"\n";
const GEN: &str = "mod tool '../cache/tool/just/tool.just'\n";

fn cid(c: char) -> String {
    c.to_string().repeat(64)
}

/// 安裝目錄與 session 目錄；版本鎖定行只有 `tool`，`cache/tool/` 與它的印記、入口檔都在。
struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
    ctl: PathBuf,
}

impl Fx {
    fn new() -> Fx {
        let tmp = tempfile::tempdir().unwrap();
        let root = tmp.path().join("root");
        let ctl = tmp.path().join("ctl");
        for d in [&root, &ctl] {
            fs::create_dir_all(d).unwrap();
        }
        let dir = InstallDir::new(&root);
        fs::create_dir_all(dir.vk_dir()).unwrap();
        fs::write(
            dir.version_toml(),
            format!(
                "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\n{TOOL}"
            ),
        )
        .unwrap();
        let fx = Fx {
            _tmp: tmp,
            dir,
            ctl,
        };
        fx.tool_dir("tool");
        fs::create_dir_all(fx.dir.gen_dir()).unwrap();
        fs::write(fx.dir.gen_dir().join("tools.just"), GEN).unwrap();
        fx
    }

    /// `cache/<repo>/` 與印記（內容只是要有檔）。
    fn tool_dir(&self, repo: &str) {
        let cache = self.dir.tool_cache(repo).unwrap();
        fs::create_dir_all(cache.join("just")).unwrap();
        fs::write(cache.join(format!("just/{repo}.just")), "x:\n").unwrap();
        fs::write(stamp::tool_file(&self.dir, repo), "stamp\n").unwrap();
    }

    fn vk(&self, rel: &str) -> PathBuf {
        self.dir.vk_dir().join(rel)
    }

    fn new_session(&self) {
        fs::remove_dir_all(&self.ctl).unwrap();
        fs::create_dir_all(&self.ctl).unwrap();
    }

    /// 安裝目錄底下每個路徑（相對）與一般檔的內容，用來比對「什麼都沒動」。
    fn snapshot(&self) -> Vec<(String, Option<Vec<u8>>)> {
        let mut out = Vec::new();
        walk(self.dir.root(), self.dir.root(), &mut out);
        out.sort();
        out
    }
}

fn walk(root: &Path, dir: &Path, out: &mut Vec<(String, Option<Vec<u8>>)>) {
    for e in fs::read_dir(dir).unwrap() {
        let p = e.unwrap().path();
        let rel = p.strip_prefix(root).unwrap().display().to_string();
        if p.is_dir() {
            out.push((rel, None));
            walk(root, &p, out);
        } else {
            out.push((rel, Some(fs::read(&p).unwrap())));
        }
    }
}

/// 假啟動器的行為。
#[derive(Clone, Default)]
struct Behavior {
    /// `ps` 列出的容器 ID。
    stopped: Vec<String>,
    /// `ps` 回 failed 1。
    fail_ps: bool,
    /// 這個容器的 `rm-container` 回 failed 1。
    fail_rm: Option<String>,
}

/// 假啟動器：回 `ps` 與 `rm-container`；`rm-container` 只收 `ps` 列過的 ID（同 launcher/launch.sh）。
struct Peer {
    stop: Arc<AtomicBool>,
    handle: JoinHandle<Vec<String>>,
}

impl Peer {
    fn start(fx: &Fx, behavior: Behavior) -> Peer {
        let ctl = fx.ctl.clone();
        let stop = Arc::new(AtomicBool::new(false));
        let flag = Arc::clone(&stop);
        let listed = Arc::new(Mutex::new(Vec::<String>::new()));
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
                    Op::Ps if behavior.fail_ps => {
                        seen.push("ps".to_owned());
                        Outcome::Failed(1)
                    }
                    Op::Ps => {
                        seen.push("ps".to_owned());
                        let text: String =
                            behavior.stopped.iter().map(|c| format!("{c}\n")).collect();
                        fs::write(ctl.join(format!("res.{s}.out")), text).unwrap();
                        *listed.lock().unwrap() = behavior.stopped.clone();
                        Outcome::Ok
                    }
                    Op::RmContainer(c) => {
                        seen.push(format!("rm-container {}", c.as_str()));
                        assert!(listed.lock().unwrap().iter().any(|l| l == c.as_str()));
                        if behavior.fail_rm.as_deref() == Some(c.as_str()) {
                            Outcome::Failed(1)
                        } else {
                            Outcome::Ok
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

fn run_prune(fx: &Fx, behavior: Behavior) -> Out {
    fx.new_session();
    let peer = Peer::start(fx, behavior);
    let argv = vec!["prune".to_owned()];
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
            channel: &mut channel,
            poll: Duration::from_millis(1),
            argv: &argv,
            run_id: "r1",
            written_by: WRITTEN_BY,
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

// ---- 沒有殘留 ----

#[test]
fn nothing_to_prune_changes_nothing_and_prints_nothing() {
    let fx = Fx::new();
    // 工具內容裡叫 `.tmp.*` 的檔是工具的，不是 VK 暫存。
    fs::write(fx.vk("cache/tool/.tmp.keep"), "tool file\n").unwrap();
    let before = fx.snapshot();
    let out = run_prune(&fx, Behavior::default());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, "");
    assert_eq!(out.stderr, "");
    assert_eq!(out.ops, ["ps"]);
    assert!(out.events().is_empty());
    assert_eq!(fx.snapshot(), before);
}

// ---- 清理 ----

#[test]
fn unlocked_tool_dirs_stamps_and_temps_are_removed() {
    let fx = Fx::new();
    fx.tool_dir("old");
    fs::write(stamp::tool_file(&fx.dir, "gone"), "stamp\n").unwrap();
    fs::write(fx.vk(".tmp.version.toml.12.0"), "half\n").unwrap();
    fs::create_dir_all(fx.vk("cache/.tmp.tool.old")).unwrap();
    fs::write(fx.vk("cache/.tmp.tool.old/x"), "x\n").unwrap();
    fs::write(fx.vk("gen/.tmp.tools.just.12.1"), "half\n").unwrap();
    // 不是工具名、不是暫存的不動。
    fs::write(fx.vk("cache/notes.txt"), "user\n").unwrap();
    let lock_before = fs::read(fx.dir.version_toml()).unwrap();

    let out = run_prune(&fx, Behavior::default());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(
        out.stdout,
        "Removed .vendor_kit/.tmp.version.toml.12.0.\n\
         Removed .vendor_kit/cache/.tmp.tool.old/.\n\
         Removed .vendor_kit/cache/gone.stamp.toml.\n\
         Removed .vendor_kit/cache/old/.\n\
         Removed .vendor_kit/cache/old.stamp.toml.\n\
         Removed .vendor_kit/gen/.tmp.tools.just.12.1.\n"
    );
    for gone in [
        ".tmp.version.toml.12.0",
        "cache/.tmp.tool.old",
        "cache/gone.stamp.toml",
        "cache/old",
        "cache/old.stamp.toml",
        "gen/.tmp.tools.just.12.1",
    ] {
        assert!(!fx.vk(gone).exists(), "{gone}");
    }
    // 鎖定的工具、入口檔、版本鎖定行不動。
    assert!(fx.vk("cache/tool/just/tool.just").is_file());
    assert!(stamp::tool_file(&fx.dir, "tool").is_file());
    assert!(fx.vk("cache/notes.txt").is_file());
    assert_eq!(
        fs::read_to_string(fx.dir.gen_dir().join("tools.just")).unwrap(),
        GEN
    );
    assert_eq!(fs::read(fx.dir.version_toml()).unwrap(), lock_before);
    assert!(progress::find(&fx.dir).unwrap().is_empty());
    assert_eq!(out.events(), ["writes_started", "progress_removed"]);
}

#[test]
fn stopped_containers_are_removed_after_the_paths() {
    let fx = Fx::new();
    fx.tool_dir("old");
    let out = run_prune(
        &fx,
        Behavior {
            stopped: vec![cid('a'), cid('b'), cid('a')],
            ..Behavior::default()
        },
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.ops,
        [
            "ps".to_owned(),
            format!("rm-container {}", cid('a')),
            format!("rm-container {}", cid('b')),
        ]
    );
    assert_eq!(
        out.stdout,
        format!(
            "Removed .vendor_kit/cache/old/.\nRemoved .vendor_kit/cache/old.stamp.toml.\n\
             Removed stopped container {}.\nRemoved stopped container {}.\n",
            cid('a'),
            cid('b')
        )
    );
}

#[test]
fn only_containers_writes_no_files() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let out = run_prune(
        &fx,
        Behavior {
            stopped: vec![cid('c')],
            ..Behavior::default()
        },
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!("Removed stopped container {}.\n", cid('c'))
    );
    assert!(out.events().is_empty());
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn a_failed_container_removal_is_reported_and_the_rest_still_go() {
    let fx = Fx::new();
    let out = run_prune(
        &fx,
        Behavior {
            stopped: vec![cid('a'), cid('b')],
            fail_rm: Some(cid('a')),
            ..Behavior::default()
        },
    );
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stdout,
        format!("Removed stopped container {}.\n", cid('b'))
    );
    assert!(
        out.stderr.starts_with("vendor_kit: error[VK0056]: ")
            && out.stderr.contains(&format!(
                "docker rm exited with 1 for stopped container {}",
                cid('a')
            )),
        "{}",
        out.stderr
    );
}

#[test]
fn without_the_lock_containers_are_not_listed() {
    let fx = Fx::new();
    fs::write(fx.dir.config_toml(), "lock_enabled = false\n").unwrap();
    fx.tool_dir("old");
    let out = run_prune(
        &fx,
        Behavior {
            stopped: vec![cid('a')],
            ..Behavior::default()
        },
    );
    assert_eq!(out.code, 1, "{}", out.stderr);
    assert!(out.ops.is_empty());
    assert!(out.stderr.contains("[VK0060]"), "{}", out.stderr);
    assert!(!fx.vk("cache/old").exists());
}

#[test]
fn residual_prune_progress_is_completed_and_removed() {
    let fx = Fx::new();
    let mut p = Progress::new(VERB, "old1", &["prune"]).unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();
    let out = run_prune(&fx, Behavior::default());
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "Completed the interrupted prune recorded in .vendor_kit/.tmp.prune.old1.toml.\n"
    );
    assert!(progress::find(&fx.dir).unwrap().is_empty());
    assert_eq!(out.events(), ["writes_started", "progress_removed"]);
}

// ---- 停下 ----

#[test]
fn another_verbs_progress_stops_before_anything_is_removed() {
    let fx = Fx::new();
    // 中斷的 add：鎖定行最後才寫，`cache/new/` 看起來沒鎖定，但恢復要用。
    fx.tool_dir("new");
    fs::create_dir_all(fx.vk("cache/.tmp.new.new")).unwrap();
    let mut p = Progress::new("add", "old1", &["add", "new"]).unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();
    let before = fx.snapshot();
    let out = run_prune(
        &fx,
        Behavior {
            stopped: vec![cid('a')],
            ..Behavior::default()
        },
    );
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert!(out.ops.is_empty(), "{:?}", out.ops);
    assert!(
        out.stderr.contains("[VK0056]")
            && out
                .stderr
                .contains("incomplete add operation in .vendor_kit/.tmp.add.old1.toml")
            && out.stderr.contains("just vendor_kit add new"),
        "{}",
        out.stderr
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn an_unlocked_dir_still_in_the_entry_file_stops_everything() {
    let fx = Fx::new();
    fx.tool_dir("old");
    fs::write(
        fx.dir.gen_dir().join("tools.just"),
        format!("mod old '../cache/old/just/old.just'\n{GEN}"),
    )
    .unwrap();
    fs::write(fx.vk(".tmp.version.toml.12.0"), "half\n").unwrap();
    let before = fx.snapshot();
    let out = run_prune(&fx, Behavior::default());
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert!(out.ops.is_empty());
    assert!(
        out.stderr.contains("[VK0056]")
            && out.stderr.contains("pruning .vendor_kit/cache/old/")
            && out.stderr.contains("still references"),
        "{}",
        out.stderr
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn a_failed_ps_stops_before_anything_is_removed() {
    let fx = Fx::new();
    fx.tool_dir("old");
    let before = fx.snapshot();
    let out = run_prune(
        &fx,
        Behavior {
            fail_ps: true,
            ..Behavior::default()
        },
    );
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert!(
        out.stderr.contains("docker ps exited with 1"),
        "{}",
        out.stderr
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn missing_lock_file_is_an_internal_error() {
    let fx = Fx::new();
    fs::remove_file(fx.dir.version_toml()).unwrap();
    let out = run_prune(&fx, Behavior::default());
    assert_eq!(out.code, 2);
    assert!(out.ops.is_empty());
    assert!(out.stderr.contains("[VK0056]"), "{}", out.stderr);
}

// ---- ps 的輸出 ----

#[test]
fn ps_output_is_one_id_per_line() {
    assert_eq!(parse_ps("").unwrap(), Vec::<Container>::new());
    let ids = parse_ps(&format!("{}\n{}\n{}\n", cid('a'), cid('b'), cid('a'))).unwrap();
    let ids: Vec<&str> = ids.iter().map(Container::as_str).collect();
    assert_eq!(ids, [cid('a'), cid('b')]);
    for bad in [
        cid('a'),
        format!("{}\n\n", cid('a')),
        "abc\n".to_owned(),
        format!("{}\n", cid('A')),
    ] {
        assert!(parse_ps(&bad).is_err(), "{bad:?}");
    }
}
