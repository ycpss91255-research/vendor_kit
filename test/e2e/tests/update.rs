//! `update`、`update <repo>`（04 update 節、成對與無害；03 輸出）：經假的啟動器跑。
//!
//! `update` 是唯讀 recipe：不碰 docker，每個情況 `.vendor_kit/` 的檔逐位元組不變。tag 向假 registry 列
//! （[`e2e::registry`]，經 `VK_TEST_REGISTRY_URL`）；`--registry-token-file` 在安裝目錄外時，假啟動器回應
//! `stage` 把檔複製進 `in/token`，其他情況假啟動器只收 `done`。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::{Path, PathBuf};

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply, Request, Seen};
use e2e::registry::{GOOD_TOKEN, Registry, Repo};
use e2e::{MOUNT_PREFIX_ENV, REGISTRY_URL_ENV, vendor_kit_bin};
use snapbox::assert_data_eq;

const RUN_ID: &str = "r1";
const HEADER: &str = "vk-resolve/1 r1";
const HOST_ROOT: &str = "/srv/proj";
const RUN_LOG: &str = ".vendor_kit/log/r1.jsonl";
const ENGINE: &str = "ghcr.io/ycpss91255-research/vendor_kit:v1.4.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const TOOL: &str = "ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222";
const OTHER: &str = "ghcr.io/acme/other:v1.0.0@sha256:3333333333333333333333333333333333333333333333333333333333333333";

/// 已導入 `tool`、`other` 的安裝目錄。
fn install(m: &Mounts) {
    let vk = m.root.join(".vendor_kit");
    fs::create_dir_all(vk.join("log")).unwrap();
    fs::write(
        vk.join("version.toml"),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nother = \"{OTHER}\"\ntool = \"{TOOL}\"\n"
        ),
    )
    .unwrap();
    fs::write(m.root.join(RUN_LOG), "").unwrap();
}

/// 什麼 op 都回失敗的假啟動器：`update` 不該送任何 request。
fn idle_launcher(m: &Mounts) -> std::thread::JoinHandle<Seen> {
    launcher::serve(&m.ctl, HEADER, |_: &Request| Reply::Failed(1))
}

/// 回 `stage` 的假啟動器：主機路徑 `e:/srv/<x>` 對到 `host/<x>`，是檔就複製進 `in/<slot>`
/// （launcher/launch.sh 的 stage：slot 已存在或 cp 失敗回 failed 1）；其他 op 一律失敗。
fn stage_launcher(m: &Mounts, host: &Path) -> std::thread::JoinHandle<Seen> {
    let (inbox, host) = (m.inbox.clone(), host.to_path_buf());
    launcher::serve(&m.ctl, HEADER, move |req: &Request| {
        let src = req.args[0]
            .strip_prefix("e:/srv/")
            .map(|rest| host.join(rest));
        let dest = inbox.join(&req.args[1]);
        match src {
            Some(src) if req.op == "stage" && src.is_file() && !dest.exists() => {
                fs::copy(&src, &dest).unwrap();
                Reply::Ok
            }
            _ => Reply::Failed(1),
        }
    })
}

/// 三個對象都公開的假 registry：工具查鎖定行的路徑，引擎查 ghcr.io/ycpss91255-research/vendor_kit。
fn public_registry() -> Registry {
    Registry::start(&[
        ("acme/tool", Repo::public(&["v1.0.0", "v1.3.0", "latest"])),
        ("acme/other", Repo::public(&["v1.0.0"])),
        (
            "ycpss91255-research/vendor_kit",
            Repo::public(&["v1.4.0", "v1.10.0", "v1.9.0"]),
        ),
    ])
}

/// 查詢前就停下的情況：registry 不該被連到，給一個不會被用到的位址。
const UNUSED_REGISTRY: &str = "http://127.0.0.1:9";

fn run(m: &Mounts, rest: &[&str]) -> (i32, String, String) {
    run_at(m, UNUSED_REGISTRY, rest)
}

fn run_at(m: &Mounts, registry: &str, rest: &[&str]) -> (i32, String, String) {
    let mut args = vec![
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
    ];
    args.extend_from_slice(rest);
    let out = Command::new(vendor_kit_bin().unwrap())
        .args(&args)
        .env(MOUNT_PREFIX_ENV, &m.prefix)
        .env(REGISTRY_URL_ENV, registry)
        .output()
        .unwrap();
    (
        out.status.code().unwrap(),
        String::from_utf8(out.stdout).unwrap(),
        String::from_utf8(out.stderr).unwrap(),
    )
}

/// `.vendor_kit/` 下每個檔的路徑與內容，不含執行紀錄與鎖檔。
fn snapshot(m: &Mounts) -> Vec<(PathBuf, Vec<u8>)> {
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
    let vk = m.root.join(".vendor_kit");
    let mut out = Vec::new();
    walk(&vk, &mut out);
    out.retain(|(p, _)| {
        !p.starts_with(vk.join("log"))
            && p.file_name()
                .is_some_and(|n| !n.to_string_lossy().contains("lock"))
    });
    out.sort();
    out
}

/// 執行紀錄裡依序的事件名。
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

#[test]
fn update_prints_a_result_line_for_each_tool_and_the_engine_without_touching_anything() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let before = snapshot(&m);
    let registry = public_registry();

    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run_at(&m, registry.base(), &["update"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
other current: v1.0.0 latest: v1.0.0
tool current: v1.2.0 latest: v1.3.0
vendor_kit current: v1.4.0 latest: v1.10.0

"#]]
    );
    assert_data_eq!(stderr, "");
    assert!(seen.requests.is_empty());
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert_eq!(snapshot(&m), before);
    let ev = events(&m);
    assert_eq!(ev.first().map(String::as_str), Some("engine_started"));
    assert_eq!(ev.last().map(String::as_str), Some("engine_finished"));
    assert!(!ev.iter().any(|e| e == "writes_started"), "{ev:?}");
}

#[test]
fn update_reports_each_failed_query_and_prints_latest_none() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let before = snapshot(&m);
    // tool 要 token、other 沒有合法 tag、引擎的路徑不存在（404）。
    let registry = Registry::start(&[
        ("acme/tool", Repo::private(&["v1.3.0"])),
        ("acme/other", Repo::public(&["latest"])),
    ]);

    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run_at(&m, registry.base(), &["update"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
other current: v1.0.0 latest: none
tool current: v1.2.0 latest: none
vendor_kit current: v1.4.0 latest: none

"#]]
    );
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0058]: Cannot determine the latest version of other: the registry has tags, but none is a valid vX.Y.Z tag. The query did not complete.
vendor_kit: error[VK0001]: Cannot list versions for tool: registry read access is required; pulling still uses the host's Docker credentials. Add --registry-token-file <path> and rerun, or specify a version directly: just vendor_kit upgrade tool@<tag>
vendor_kit: error[VK0055]: Cannot access ghcr.io/ycpss91255-research/vendor_kit for vendor_kit: registry returned HTTP 404 for [..]/v2/ycpss91255-research/vendor_kit/tags/list?n=100. The requested operation did not complete.

"#]]
    );
    assert!(seen.requests.is_empty());
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_eq!(snapshot(&m), before);
}

#[test]
fn update_reads_a_token_file_outside_the_install_dir_through_stage() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let host = tmp.path().join("host");
    fs::create_dir_all(host.join("home")).unwrap();
    fs::write(host.join("home/ghcr"), format!("{GOOD_TOKEN}\n")).unwrap();
    let before = snapshot(&m);
    let registry = Registry::start(&[("acme/tool", Repo::private(&["v1.2.0", "v2.0.0"]))]);

    let peer = stage_launcher(&m, &host);
    let (code, stdout, stderr) = run_at(
        &m,
        registry.base(),
        &["update", "tool", "--registry-token-file", "/srv/home/ghcr"],
    );
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(stdout, "tool current: v1.2.0 latest: v2.0.0\n");
    assert_data_eq!(stderr, "");
    assert_eq!(seen.requests, ["stage e:/srv/home/ghcr token"]);
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert_eq!(snapshot(&m), before);
}

#[test]
fn update_reads_a_token_file_inside_the_install_dir_directly_and_reports_a_rejected_one() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    fs::write(m.root.join("good"), GOOD_TOKEN).unwrap();
    fs::write(m.root.join("bad"), "nope").unwrap();
    let before = snapshot(&m);
    let registry = Registry::start(&[("acme/tool", Repo::private(&["v1.3.0"]))]);

    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run_at(
        &m,
        registry.base(),
        &["update", "tool", "--registry-token-file", "good"],
    );
    let seen = peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(stdout, "tool current: v1.2.0 latest: v1.3.0\n");
    assert!(seen.requests.is_empty());

    let tmp2 = tempfile::tempdir().unwrap();
    let m2 = Mounts::create(tmp2.path());
    install(&m2);
    fs::write(m2.root.join("bad"), "nope").unwrap();
    let peer = idle_launcher(&m2);
    let (code, stdout, stderr) = run_at(
        &m2,
        registry.base(),
        &["update", "tool", "--registry-token-file", "/srv/proj/bad"],
    );
    let seen = peer.join().unwrap();
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "tool current: v1.2.0 latest: none\n");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0055]: Cannot access ghcr.io/acme/tool for tool: registry rejected the supplied token (HTTP 401). The requested operation did not complete.

"#]]
    );
    assert!(seen.requests.is_empty());
    assert_eq!(snapshot(&m), before);
}

#[test]
fn update_of_a_tool_that_is_not_installed_is_vk0046() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let before = snapshot(&m);

    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run(&m, &["update", "missing"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0046]: Tool missing is not in the lock version lines. The requested operation did not complete.

"#]]
    );
    assert!(seen.requests.is_empty());
    assert_eq!(snapshot(&m), before);
}

#[test]
fn update_detects_an_incomplete_add_and_leaves_its_progress_file() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let progress = m.root.join(".vendor_kit/.tmp.add.r0.toml");
    fs::write(
        &progress,
        "command = [\"add\", \"new\", \"-i\", \"ghcr.io/acme/new:v1.0.0\"]\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[add]\nrepo = \"new\"\n",
    )
    .unwrap();
    let before = snapshot(&m);

    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run(&m, &["update", "tool"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0004]: Import of new is incomplete. Run: just vendor_kit add new

"#]]
    );
    assert!(seen.requests.is_empty());
    // 唯讀 recipe 只偵測：進度檔留著，其他檔也不動。
    assert!(progress.is_file());
    assert_eq!(snapshot(&m), before);
}
