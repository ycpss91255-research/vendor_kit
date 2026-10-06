//! `test` 與 `test <path>`（04 檢查 (test)、04 test 路徑與 runner、03 輸出）：經假的啟動器跑完整安裝檢查與
//! 使用者測試。
//!
//! 安裝目錄先照 `sync` 的 e2e 排好全新 checkout（兩個工具、跟這一版引擎一致的薄殼），需要時先跑一次 `sync`
//! 取件（假啟動器回 inspect 與 extract），再跑 `test`。不帶 path 的 `test` 不送任何 docker 動作；`test <path>`
//! 只送一個 `runner` op（假啟動器回測試指定的 runner result）。兩者除執行紀錄外都不寫任何檔。
//! 檔名不叫 `test.rs`：測試 target 叫 `test` 會跟 libtest 的 `test` crate 撞名。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::{Path, PathBuf};

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply, Request, Seen};
use e2e::{MOUNT_PREFIX_ENV, VERSION, shell, vendor_kit_bin};
use snapbox::assert_data_eq;

const RUN_ID: &str = "r1";
const HOST_ROOT: &str = "/srv/proj";
const RUN_LOG: &str = ".vendor_kit/log/r1.jsonl";
const ENGINE: &str = "ghcr.io/ycpss91255-research/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const TOOL_DIGEST: &str = "sha256:2222222222222222222222222222222222222222222222222222222222222222";
const OTHER_DIGEST: &str =
    "sha256:3333333333333333333333333333333333333333333333333333333333333333";

fn release_dir(m: &Mounts) -> PathBuf {
    m.prefix.join("release")
}

/// 全新 checkout：`version.toml` 有 `tools` 列的工具、跟這一版引擎一致的薄殼，沒有 `cache/`、`gen/`。
fn checkout(m: &Mounts, tools: bool) {
    let vk = m.root.join(".vendor_kit");
    fs::create_dir_all(vk.join("log")).unwrap();
    shell::install(&m.root, VERSION).unwrap();
    shell::release(&release_dir(m)).unwrap();
    let tools = if tools {
        format!(
            "\n[tools]\n\
             other = \"ghcr.io/acme/other:v2.0.0@{OTHER_DIGEST}\"\n\
             tool = \"ghcr.io/acme/tool:v1.2.0@{TOOL_DIGEST}\"\n"
        )
    } else {
        String::new()
    };
    fs::write(
        vk.join("version.toml"),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n{tools}"
        ),
    )
    .unwrap();
}

fn tool_content(dir: &Path, namespaces: &[&str]) {
    fs::create_dir_all(dir.join("just")).unwrap();
    for ns in namespaces {
        fs::write(
            dir.join("just").join(format!("{ns}.just")),
            "hello:\n    echo hi\n",
        )
        .unwrap();
    }
    fs::create_dir_all(dir.join("share")).unwrap();
    fs::write(dir.join("share/readme.txt"), "tool files\n").unwrap();
}

/// 假啟動器：兩個工具的 image 都在本機；image ID 就是 digest。`runner` op 回 `runner <runner>`。
fn launcher(m: &Mounts, runner: &'static str) -> std::thread::JoinHandle<Seen> {
    let (ctl, inbox) = (m.ctl.clone(), m.inbox.clone());
    launcher::serve(
        &m.ctl,
        &format!("vk-resolve/1 {RUN_ID}"),
        move |req: &Request| match req.op.as_str() {
            "inspect" => {
                let reference = &req.args[0];
                let (_, digest) = reference.split_once('@').unwrap();
                fs::write(
                    ctl.join(format!("res.{}.out", req.seq)),
                    launcher::inspect_json(digest, &[reference.as_str()]),
                )
                .unwrap();
                Reply::Ok
            }
            "extract" if req.args[0] == TOOL_DIGEST => {
                tool_content(&inbox.join(&req.args[1]), &["tool", "tool-extra"]);
                Reply::Ok
            }
            "extract" if req.args[0] == OTHER_DIGEST => {
                tool_content(&inbox.join(&req.args[1]), &["other"]);
                Reply::Ok
            }
            "runner" => Reply::Runner(runner),
            _ => Reply::Failed(1),
        },
    )
}

/// 跑一次引擎；每次執行的 session 目錄與執行紀錄都是新的（啟動器建好空的執行紀錄）。
fn run(m: &Mounts, rest: &[&str]) -> (i32, String, String, Seen) {
    run_with(m, rest, "notstarted")
}

/// 同 [`run`]，假啟動器的 runner 回 `runner <runner>`。
fn run_with(m: &Mounts, rest: &[&str], runner: &'static str) -> (i32, String, String, Seen) {
    for d in [&m.ctl, &m.inbox] {
        fs::remove_dir_all(d).unwrap();
        fs::create_dir_all(d).unwrap();
    }
    fs::write(m.root.join(RUN_LOG), "").unwrap();
    let peer = launcher(m, runner);
    let out = Command::new(vendor_kit_bin().unwrap())
        .args([
            "--protocol",
            "1",
            "--run-id",
            RUN_ID,
            "--host-root",
            HOST_ROOT,
            "--host-cwd",
            HOST_ROOT,
            "--run-log",
            RUN_LOG,
            "--tty",
            "000",
            "--no-color",
            "1",
            "--",
        ])
        .args(rest)
        .env(MOUNT_PREFIX_ENV, &m.prefix)
        .env(shell::RELEASE_DIR_ENV, release_dir(m))
        .write_stdin("")
        .output()
        .unwrap();
    let seen = peer.join().unwrap();
    (
        out.status.code().unwrap(),
        String::from_utf8(out.stdout).unwrap(),
        String::from_utf8(out.stderr).unwrap(),
        seen,
    )
}

/// 安裝目錄下每個一般檔的路徑與內容，不含執行紀錄。
fn contents(m: &Mounts) -> Vec<(String, Vec<u8>)> {
    fn walk(root: &Path, dir: &Path, out: &mut Vec<(String, Vec<u8>)>) {
        for entry in fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                walk(root, &path, out);
            } else {
                let rel = path.strip_prefix(root).unwrap().display().to_string();
                out.push((rel, fs::read(&path).unwrap()));
            }
        }
    }
    let mut out = Vec::new();
    walk(&m.root, &m.root, &mut out);
    out.retain(|(p, _)| !p.starts_with(".vendor_kit/log"));
    out.sort();
    out
}

fn events(m: &Mounts) -> Vec<String> {
    fs::read_to_string(m.root.join(RUN_LOG))
        .unwrap()
        .lines()
        .map(|l| {
            let rest = l.split_once("\"event_name\":\"").unwrap().1;
            rest.split_once('"').unwrap().0.to_owned()
        })
        .collect()
}

/// 跑 `test`：不送 docker 動作、除執行紀錄外不寫檔，`done` 帶整次的結束碼。
fn run_test(m: &Mounts) -> (i32, String, String) {
    let before = contents(m);
    let (code, stdout, stderr, seen) = run(m, &["test"]);
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(
        seen.done.as_deref(),
        Some(format!("vk-resolve/1 {RUN_ID} done {code}\n").as_str())
    );
    assert_eq!(contents(m), before, "test must not write any file");
    let events = events(m);
    assert_eq!(events.first().map(String::as_str), Some("engine_started"));
    assert_eq!(events.last().map(String::as_str), Some("engine_finished"));
    assert!(!events.iter().any(|e| e == "writes_started"), "{events:?}");
    (code, stdout, stderr)
}

#[test]
fn after_sync_the_install_check_passes() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m, true);
    let (code, _, stderr, _) = run(&m, &["sync"]);
    assert_eq!(code, 0, "{stderr}");

    let (code, stdout, stderr) = run_test(&m);
    assert_eq!(code, 0, "{stderr}");
    assert_data_eq!(stdout, "Install check passed.\n");
    assert_data_eq!(stderr, "");
}

/// 04 檢查：沒有工具也檢查薄殼與引擎；`gen/tools.just` 不在也算一致。
#[test]
fn without_tools_the_shell_is_still_checked() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m, false);

    let (code, stdout, stderr) = run_test(&m);
    assert_eq!(code, 0, "{stderr}");
    assert_data_eq!(stdout, "Install check passed.\n");

    fs::write(m.root.join(".vendor_kit/vendor.just"), "# edited\n").unwrap();
    let (code, stdout, stderr) = run_test(&m);
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with("vendor_kit: error[VK0006]: "),
        "{stderr}"
    );
    assert!(stderr.contains(".vendor_kit/vendor.just"), "{stderr}");
}

/// #372 N12：全新 checkout 還沒取件算缺件，下一步是 sync。
#[test]
fn fresh_checkout_reports_missing_files() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m, true);

    let (code, stdout, stderr) = run_test(&m);
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0047]: Cannot complete checks for other: required local files are missing: .vendor_kit/cache/other.stamp.toml (missing), .vendor_kit/cache/other/ (missing). Run: just vendor_kit sync
vendor_kit: error[VK0047]: Cannot complete checks for tool: required local files are missing: .vendor_kit/cache/tool.stamp.toml (missing), .vendor_kit/cache/tool/ (missing). Run: just vendor_kit sync
vendor_kit: error[VK0047]: Cannot complete checks for /srv/proj: required local files are missing: .vendor_kit/gen/tools.just (missing). Run: just vendor_kit sync

"#]]
    );
}

/// #372 N87：cache 跟印記不一致也報 VK0047；本機覆寫仍會擋下（VK0032）。
#[test]
fn modified_cache_and_local_override_block() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m, true);
    let (code, _, stderr, _) = run(&m, &["sync"]);
    assert_eq!(code, 0, "{stderr}");
    fs::write(
        m.root.join(".vendor_kit/cache/other/share/readme.txt"),
        "edited\n",
    )
    .unwrap();
    fs::write(
        m.root.join(".vendor_kit/version.local.toml"),
        "schema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"work/tool\"\n",
    )
    .unwrap();

    let (code, stdout, stderr) = run_test(&m);
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0032]: Test cannot run while a local override of tool is active. Run: just vendor_kit undev tool
vendor_kit: error[VK0047]: Cannot complete checks for other: required local files are missing: .vendor_kit/cache/other/share/readme.txt (changed). Run: just vendor_kit sync

"#]]
    );
}

/// 已 sync、有 `[test]` 設定與使用者測試的安裝目錄。
fn with_tests(m: &Mounts) {
    checkout(m, true);
    let (code, _, stderr, _) = run(m, &["sync"]);
    assert_eq!(code, 0, "{stderr}");
    fs::write(
        m.root.join(".vendor_kit/config.toml"),
        "[test]\nimage = \"ghcr.io/acme/runner:v1\"\ncommand = [\"bats\", \"--tap\"]\n",
    )
    .unwrap();
    fs::create_dir_all(m.root.join("test/unit")).unwrap();
    fs::write(m.root.join("test/unit/a.bats"), "@test a { true; }\n").unwrap();
}

/// 跑 `test <path>`：除執行紀錄外不寫檔，`done` 帶整次的結束碼；回收到的 op 行。
fn run_user(m: &Mounts, path: &str, runner: &'static str) -> (i32, String, String, Vec<String>) {
    let before = contents(m);
    let (code, stdout, stderr, seen) = run_with(m, &["test", path], runner);
    assert_eq!(
        seen.done.as_deref(),
        Some(format!("vk-resolve/1 {RUN_ID} done {code}\n").as_str())
    );
    assert_eq!(contents(m), before, "test must not write any file");
    (code, stdout, stderr, seen.requests)
}

/// 04 test 路徑與 runner：檢查通過後在 `[test].image` 跑 `[test].command` 加上 path。
#[test]
fn test_with_a_path_runs_the_runner_after_the_check() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    with_tests(&m);

    let (code, stdout, stderr, ops) = run_user(&m, "test/unit", "exited 0");
    assert_eq!(code, 0, "{stderr}");
    assert_data_eq!(stdout, "Install check passed.\n");
    assert_data_eq!(stderr, "");
    assert_eq!(
        ops,
        ["runner ghcr.io/acme/runner:v1 e:bats e:--tap e:test/unit"]
    );
}

/// 啟動器回的各種 runner result 由引擎發碼（#372 N71）：自己結束且非 0 是 VK0067，起不來或被停掉是 VK0066。
#[test]
fn runner_results_map_to_vk0066_and_vk0067() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    with_tests(&m);

    for (runner, code_line, rc) in [
        ("exited 1", "VK0067", "1"),
        ("exited 255", "VK0067", "255"),
        ("notstarted", "VK0066", "unavailable"),
        ("stopped 130", "VK0066", "130"),
        ("stopped unavailable", "VK0066", "unavailable"),
    ] {
        let (code, stdout, stderr, ops) = run_user(&m, "test/unit", runner);
        assert_eq!(code, 2, "{runner}: {stderr}");
        assert_data_eq!(stdout, "Install check passed.\n");
        assert!(
            stderr.starts_with(&format!("vendor_kit: error[{code_line}]: ")),
            "{runner}: {stderr}"
        );
        assert!(
            stderr.contains(&format!("Runner exit code: {rc}.")),
            "{runner}: {stderr}"
        );
        assert_eq!(ops.len(), 1, "{runner}");
    }
}

/// path 無效（VK0063）或安裝檢查不過（VK0062，整次 max(檢查碼, 2)）：runner 不啟動。
#[test]
fn invalid_path_or_failing_check_does_not_start_the_runner() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    with_tests(&m);

    let (code, stdout, stderr, ops) = run_user(&m, "unit", "exited 0");
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with(
            "vendor_kit: error[VK0063]: Invalid test path unit: it is not written as test/...."
        ),
        "{stderr}"
    );
    assert!(ops.is_empty(), "{ops:?}");

    fs::remove_file(m.root.join(".vendor_kit/gen/tools.just")).unwrap();
    let (code, stdout, stderr, ops) = run_user(&m, "test/unit", "exited 0");
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0047]: Cannot complete checks for /srv/proj: required local files are missing: .vendor_kit/gen/tools.just (missing). Run: just vendor_kit sync
vendor_kit: error[VK0062]: Installation checks returned 2. No tests were started for test/unit. Resolve the check diagnostics and retry.

"#]]
    );
    assert!(ops.is_empty(), "{ops:?}");
}
