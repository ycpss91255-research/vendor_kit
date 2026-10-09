//! `test <path>`：選測試、工具交付的判定、`[test]` 設定、安裝檢查不過時不跑，以及各種 runner result 的發碼。
//! 假的啟動器在背景執行緒回 runner result，記下收到的 op 行。

use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread::{self, JoinHandle};
use std::time::Duration;

use metadata::{FileRecord, Metadata, State};
use plan::{Channel, Header, Op, Outcome, RunId, RunnerOutcome};

use super::*;
use crate::user_test::{self, Runner};

const CONFIG: &str =
    "[test]\nimage = \"ghcr.io/acme/runner:v1\"\ncommand = [\"bats\", \"--tap\"]\n";

fn header(protocol: u32) -> Header {
    Header::new(protocol, RunId::parse("r1").unwrap()).unwrap()
}

/// 假啟動器：每個 request 都回 `outcome`，記下 op 行。
struct Peer {
    stop: Arc<AtomicBool>,
    handle: JoinHandle<Vec<String>>,
}

impl Peer {
    fn start(ctl: PathBuf, outcome: RunnerOutcome, protocol: u32) -> Peer {
        let stop = Arc::new(AtomicBool::new(false));
        let flag = Arc::clone(&stop);
        let handle = thread::spawn(move || {
            let header = header(protocol);
            let mut seen = Vec::new();
            let mut seq = 1u16;
            while !flag.load(Ordering::SeqCst) {
                let Ok(bytes) = fs::read(ctl.join(format!("req.{seq}"))) else {
                    thread::sleep(Duration::from_millis(2));
                    continue;
                };
                let (s, op) = Op::parse_request(&bytes, &header).unwrap();
                let text = String::from_utf8(bytes).unwrap();
                seen.push(text.lines().nth(1).unwrap().to_owned());
                let reply = match op {
                    Op::Runner { .. } => Outcome::Runner(outcome),
                    _ => Outcome::Failed(1),
                };
                let tmp = ctl.join(format!("res.{s}.tmp"));
                fs::write(&tmp, reply.encode_response(&header, s)).unwrap();
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

struct UserOut {
    out: Out,
    ops: Vec<String>,
}

fn run_user(fx: &Fx, path: &str, outcome: RunnerOutcome) -> UserOut {
    run_user_at(fx, path, outcome, 1)
}

/// 同 [`run_user`]，呼叫方的介面版是 `protocol`。
fn run_user_at(fx: &Fx, path: &str, outcome: RunnerOutcome, protocol: u32) -> UserOut {
    let ctl = fx._tmp.path().join(format!("ctl-{}", fx.sessions()));
    fs::create_dir_all(&ctl).unwrap();
    let before = fx.snapshot();
    let peer = Peer::start(ctl.clone(), outcome, protocol);
    let mut channel = Channel::new(&ctl, header(protocol));
    let mut stdout = Vec::new();
    let mut stderr = Vec::new();
    let code = {
        let mut diags = Diagnostics::with_sink(&mut stderr, NoSink);
        let templates = templates();
        let mut env = Env {
            dir: &fx.dir,
            host_root: HOST_ROOT,
            run_log: "/h/proj/.vendor_kit/log/r1.jsonl",
            written_by: WRITTEN_BY,
            shell_templates: Some(&templates),
            stdout: &mut stdout,
            diags: &mut diags,
        };
        let mut runner = Runner {
            channel: &mut channel,
            poll: Duration::from_millis(1),
        };
        user_test::run(std::ffi::OsStr::new(path), &mut runner, &mut env)
    };
    let ops = peer.finish();
    assert_eq!(fx.snapshot(), before, "test must not write any file");
    UserOut {
        out: Out {
            code,
            stdout: String::from_utf8(stdout).unwrap(),
            stderr: String::from_utf8(stderr).unwrap(),
        },
        ops,
    }
}

impl Fx {
    /// 每次 `run_user` 用新的 ctl 目錄。
    fn sessions(&self) -> usize {
        fs::read_dir(self._tmp.path())
            .unwrap()
            .filter(|e| {
                e.as_ref()
                    .unwrap()
                    .file_name()
                    .to_string_lossy()
                    .starts_with("ctl-")
            })
            .count()
    }

    /// 已 sync 的安裝目錄，加上 `[test]` 設定與 `test/unit/a.bats`、`test/unit/deep/b.bats`。
    fn with_tests(tools: &[&Tool]) -> Fx {
        let fx = Fx::synced(tools);
        fs::write(fx.dir.config_toml(), CONFIG).unwrap();
        fs::create_dir_all(fx.dir.root().join("test/unit/deep")).unwrap();
        fs::write(
            fx.dir.root().join("test/unit/a.bats"),
            "@test a { true; }\n",
        )
        .unwrap();
        fs::write(
            fx.dir.root().join("test/unit/deep/b.bats"),
            "@test b { true; }\n",
        )
        .unwrap();
        fx
    }
}

#[test]
fn passing_check_runs_the_runner_with_the_path_appended() {
    let fx = Fx::with_tests(&[&TOOL]);
    let r = run_user(&fx, "test/unit", RunnerOutcome::Exited(0));
    assert_eq!(r.out.code, 0, "{}", r.out.stderr);
    assert_eq!(r.out.stderr, "");
    assert_eq!(r.out.stdout, format!("{}\n", text::PASSED));
    assert_eq!(
        r.ops,
        ["runner ghcr.io/acme/runner:v1 e:bats e:--tap e:test/unit"]
    );
}

#[test]
fn single_file_and_whole_test_dir_are_selectable() {
    let fx = Fx::with_tests(&[]);
    for path in ["test/unit/a.bats", "test", "test/"] {
        let r = run_user(&fx, path, RunnerOutcome::Exited(0));
        assert_eq!(r.out.code, 0, "{path}: {}", r.out.stderr);
        assert_eq!(r.ops.len(), 1, "{path}");
        assert!(r.ops[0].ends_with(&format!(" e:{path}")), "{:?}", r.ops);
    }
}

#[test]
fn runner_failure_is_vk0067_with_the_runner_exit_code() {
    let fx = Fx::with_tests(&[&TOOL]);
    let r = run_user(&fx, "test/unit", RunnerOutcome::Exited(130));
    assert_eq!(r.out.code, 2);
    assert_eq!(codes(&r.out.stderr), ["VK0067"]);
    assert!(
        r.out.stderr.contains("Tests failed for test/unit."),
        "{}",
        r.out.stderr
    );
    assert!(
        r.out.stderr.contains("Runner exit code: 130."),
        "{}",
        r.out.stderr
    );
}

#[test]
fn runner_not_started_or_stopped_is_vk0066() {
    let fx = Fx::with_tests(&[&TOOL]);
    for (outcome, reason, rc) in [
        (
            RunnerOutcome::NotStarted,
            "the runner did not start",
            "unavailable",
        ),
        (
            RunnerOutcome::Stopped(Some(143)),
            "the runner was stopped by vendor_kit",
            "143",
        ),
        (
            RunnerOutcome::Stopped(None),
            "the runner was stopped by vendor_kit",
            "unavailable",
        ),
    ] {
        let r = run_user(&fx, "test/unit", outcome);
        assert_eq!(r.out.code, 2, "{outcome:?}");
        assert_eq!(codes(&r.out.stderr), ["VK0066"], "{outcome:?}");
        assert!(
            r.out.stderr.contains(&format!(
                "Cannot complete the test runner for test/unit: {reason}."
            )),
            "{}",
            r.out.stderr
        );
        assert!(
            r.out.stderr.contains(&format!("Runner exit code: {rc}.")),
            "{}",
            r.out.stderr
        );
    }
}

#[test]
fn invalid_paths_are_vk0063_and_nothing_runs() {
    let fx = Fx::with_tests(&[&TOOL]);
    let root = fx.dir.root().to_path_buf();
    std::os::unix::fs::symlink(root.join(".vendor_kit/config.toml"), root.join("test/out"))
        .unwrap();
    fs::create_dir_all(root.join("test/linked")).unwrap();
    std::os::unix::fs::symlink(root.join("README"), root.join("test/linked/dangling")).unwrap();
    fs::create_dir_all(root.join("unit")).unwrap();
    fs::write(root.join("unit/x.bats"), "x\n").unwrap();
    for (path, reason) in [
        ("unit", "it is not written as test/..."),
        ("./test/unit", "it is not written as test/..."),
        ("/vk/root/test/unit", "it is not written as test/..."),
        (".vendor_kit/config.toml", "it is not written as test/..."),
        ("test/../unit", "it contains a .. component"),
        ("test/missing", "it does not exist"),
        (
            "test/out",
            "test/out resolves outside test/ of the install directory",
        ),
        (
            "test/linked",
            "test/linked/dangling is a broken symbolic link",
        ),
    ] {
        let r = run_user(&fx, path, RunnerOutcome::Exited(0));
        assert_eq!(r.out.code, 2, "{path}");
        assert_eq!(codes(&r.out.stderr), ["VK0063"], "{path}");
        assert!(
            r.out
                .stderr
                .contains(&format!("Invalid test path {path}: {reason}.")),
            "{path}: {}",
            r.out.stderr
        );
        assert!(r.ops.is_empty(), "{path}: {:?}", r.ops);
        assert_eq!(r.out.stdout, "");
    }
}

#[test]
fn a_directory_symlink_inside_test_is_checked_but_not_followed() {
    let fx = Fx::with_tests(&[]);
    let root = fx.dir.root().to_path_buf();
    fs::create_dir_all(root.join("test/loop")).unwrap();
    std::os::unix::fs::symlink(root.join("test"), root.join("test/loop/up")).unwrap();
    let r = run_user(&fx, "test", RunnerOutcome::Exited(0));
    assert_eq!(r.out.code, 0, "{}", r.out.stderr);
    assert_eq!(r.ops.len(), 1);
}

#[test]
fn nothing_selected_is_vk0065() {
    let fx = Fx::with_tests(&[]);
    fs::create_dir_all(fx.dir.root().join("test/empty/inner")).unwrap();
    let r = run_user(&fx, "test/empty", RunnerOutcome::Exited(0));
    assert_eq!(r.out.code, 2);
    assert_eq!(codes(&r.out.stderr), ["VK0065"]);
    assert!(r.ops.is_empty());
}

#[test]
fn missing_test_settings_are_vk0059() {
    for (config, field) in [
        ("", "[test]"),
        ("[test]\ncommand = [\"bats\"]\n", "[test].image"),
        (
            "[test]\nimage = \"ghcr.io/acme/runner:v1\"\n",
            "[test].command",
        ),
    ] {
        let fx = Fx::with_tests(&[]);
        fs::write(fx.dir.config_toml(), config).unwrap();
        let r = run_user(&fx, "test/unit", RunnerOutcome::Exited(0));
        assert_eq!(r.out.code, 2, "{config}");
        assert_eq!(codes(&r.out.stderr), ["VK0059"], "{config}");
        assert!(
            r.out.stderr.contains(&format!("{field} = missing")),
            "{}",
            r.out.stderr
        );
        assert!(r.ops.is_empty());
    }
}

#[test]
fn failing_check_is_vk0062_and_the_runner_does_not_start() {
    let fx = Fx::with_tests(&[&TOOL]);
    fs::remove_dir_all(fx.dir.tool_cache("tool").unwrap()).unwrap();
    let r = run_user(&fx, "test/unit", RunnerOutcome::Exited(0));
    assert_eq!(r.out.code, 2);
    assert_eq!(codes(&r.out.stderr), ["VK0047", "VK0062"]);
    assert!(
        r.out
            .stderr
            .contains("Installation checks returned 2. No tests were started for test/unit."),
        "{}",
        r.out.stderr
    );
    assert_eq!(r.out.stdout, "");
    assert!(r.ops.is_empty());
}

#[test]
fn lock_disabled_is_not_a_check_failure() {
    let fx = Fx::with_tests(&[]);
    fs::write(
        fx.dir.config_toml(),
        format!("lock_enabled = false\n{CONFIG}"),
    )
    .unwrap();
    let r = run_user(&fx, "test/unit", RunnerOutcome::Exited(0));
    assert_eq!(r.out.code, 1, "{}", r.out.stderr);
    assert_eq!(codes(&r.out.stderr), ["VK0060"]);
    assert_eq!(r.ops.len(), 1);

    let r = run_user(&fx, "test/unit", RunnerOutcome::Exited(1));
    assert_eq!(r.out.code, 2);
    assert_eq!(codes(&r.out.stderr), ["VK0060", "VK0067"]);
}

#[test]
fn tool_delivered_tests_are_vk0064() {
    let fx = Fx::with_tests(&[&TOOL, &OTHER]);
    let file = metadata::tool_path(&fx.dir, "tool").unwrap();
    fs::create_dir_all(file.parent().unwrap()).unwrap();
    let mut records = Metadata::new();
    records
        .put(FileRecord::new("test/unit/deep/b.bats", State::Managed))
        .unwrap();
    records
        .put(FileRecord::new("test/unit/a.bats", State::Unmanaged))
        .unwrap();
    records.save(&file, WRITTEN_BY).unwrap();

    // 選取範圍含工具交付的檔：整次不跑。
    for path in ["test/unit", "test/unit/deep/b.bats", "test"] {
        let r = run_user(&fx, path, RunnerOutcome::Exited(0));
        assert_eq!(r.out.code, 2, "{path}");
        assert_eq!(codes(&r.out.stderr), ["VK0064"], "{path}");
        assert!(
            r.out.stderr.contains(&format!(
                "Cannot run {path}: VK recorded this test as delivered by tool tool."
            )),
            "{}",
            r.out.stderr
        );
        assert!(r.ops.is_empty());
    }
    // `unmanaged` 不是工具交付的：照常往下（這裡停在 metadata 存在時的 VK0014 缺口）。
    let r = run_user(&fx, "test/unit/a.bats", RunnerOutcome::Exited(0));
    assert_eq!(
        codes(&r.out.stderr),
        ["VK0056", "VK0062"],
        "{}",
        r.out.stderr
    );
}

#[test]
fn image_the_protocol_cannot_carry_is_vk0066() {
    let fx = Fx::with_tests(&[]);
    fs::write(
        fx.dir.config_toml(),
        "[test]\nimage = \"ghcr.io/acme/runner:V1\"\ncommand = [\"bats\"]\n",
    )
    .unwrap();
    let r = run_user(&fx, "test/unit", RunnerOutcome::Exited(0));
    assert_eq!(r.out.code, 2);
    assert_eq!(codes(&r.out.stderr), ["VK0066"]);
    assert!(r.out.stderr.contains("Runner exit code: unavailable."));
    assert!(r.ops.is_empty());
}

#[test]
fn from_interface_version_2_the_image_is_a_free_text_field_and_docker_decides() {
    let fx = Fx::with_tests(&[]);
    fs::write(
        fx.dir.config_toml(),
        "[test]\nimage = \"ghcr.io/acme/runner:V1\"\ncommand = [\"bats\"]\n",
    )
    .unwrap();
    let r = run_user_at(&fx, "test/unit", RunnerOutcome::Exited(0), 2);
    assert_eq!(r.out.code, 0, "{}", r.out.stderr);
    assert_eq!(
        r.ops,
        ["runner e:ghcr.io/acme/runner:V1 e:bats e:test/unit"]
    );
    // 以 - 開頭的會被 docker create 當成選項：照樣送不出，VK0066
    fs::write(
        fx.dir.config_toml(),
        "[test]\nimage = \"--privileged\"\ncommand = [\"bats\"]\n",
    )
    .unwrap();
    let r = run_user_at(&fx, "test/unit", RunnerOutcome::Exited(0), 2);
    assert_eq!(r.out.code, 2);
    assert_eq!(codes(&r.out.stderr), ["VK0066"]);
    assert!(r.out.stderr.contains("must not be empty or start with -"));
    assert!(r.ops.is_empty());
}

#[test]
fn arguments_with_spaces_are_encoded_as_fields() {
    let fx = Fx::with_tests(&[]);
    fs::create_dir_all(fx.dir.root().join("test/my dir")).unwrap();
    fs::write(fx.dir.root().join("test/my dir/c.bats"), "x\n").unwrap();
    let r = run_user(&fx, "test/my dir", RunnerOutcome::Exited(0));
    assert_eq!(r.out.code, 0, "{}", r.out.stderr);
    assert_eq!(
        r.ops,
        [r"runner ghcr.io/acme/runner:v1 e:bats e:--tap e:test/my\040dir"]
    );
}
