//! `update`、`update <repo>`（04 update 節、成對與無害；03 輸出）：經假的啟動器跑。
//!
//! `update` 是唯讀 recipe：不碰 docker，假啟動器只收 `done`；每個情況 `.vendor_kit/` 的檔逐位元組不變。
//! 列 registry 的 tag 還做不了（engine/update 的缺口），所以正常情況以 VK0056 停下、stdout 不印結果行。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::{Path, PathBuf};

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply, Request, Seen};
use e2e::{MOUNT_PREFIX_ENV, vendor_kit_bin};
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

fn run(m: &Mounts, rest: &[&str]) -> (i32, String, String) {
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
fn update_stops_at_the_tag_listing_gap_without_touching_anything() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let before = snapshot(&m);

    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run(&m, &["update"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2, "stderr: {stderr}");
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0056]: Internal vendor_kit error: listing tags from the registry for update (other (v1.0.0), tool (v1.2.0), vendor_kit (v1.4.0)) is not supported yet. This is a VK bug. Report it at https://github.com/ycpss91255-research/vendor_kit/issues and attach run log /srv/proj/.vendor_kit/log/r1.jsonl.

"#]]
    );
    assert!(seen.requests.is_empty());
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_eq!(snapshot(&m), before);
    let ev = events(&m);
    assert_eq!(ev.first().map(String::as_str), Some("engine_started"));
    assert_eq!(ev.last().map(String::as_str), Some("engine_finished"));
    assert!(!ev.iter().any(|e| e == "writes_started"), "{ev:?}");
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
