//! `prune`（04 成對與無害、03 輸出）：經假的啟動器跑完整的 `prune`。
//!
//! 每個測試在暫存目錄建好安裝目錄與 session 的 `ctl/`、`in/`，以 [`MOUNT_PREFIX_ENV`] 讓引擎把它們
//! 當成 `/vk/root`、`/vk/ctl`、`/vk/in`；假啟動器在背景回 `ps`（列出已停止的 VK 容器）與 `rm-container`。
//! 版本鎖定行有一個工具 `tool`，它的 `cache/tool/`、印記與入口檔都在。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::Path;
use std::sync::{Arc, Mutex};

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply, Request, Seen};
use e2e::{MOUNT_PREFIX_ENV, vendor_kit_bin};
use snapbox::assert_data_eq;

const RUN_ID: &str = "r1";
const HEADER: &str = "vk-resolve/1 r1";
const HOST_ROOT: &str = "/srv/proj";
const RUN_LOG: &str = ".vendor_kit/log/r1.jsonl";
const ENGINE: &str = "ghcr.io/ycpss91255-research/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const TOOL_DIGEST: &str = "sha256:2222222222222222222222222222222222222222222222222222222222222222";
const GEN: &str = "mod tool '../cache/tool/just/tool.just'\n";
const STOPPED: &str = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";

/// 已同步的安裝目錄：版本鎖定行有 `tool`，`cache/tool/`、印記、入口檔都在。
fn installed(m: &Mounts) {
    let vk = m.root.join(".vendor_kit");
    fs::create_dir_all(vk.join("log")).unwrap();
    fs::write(
        vk.join("version.toml"),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\n\
             tool = \"ghcr.io/acme/tool:v1.2.0@{TOOL_DIGEST}\"\n"
        ),
    )
    .unwrap();
    fs::write(
        m.root.join("justfile"),
        "import '.vendor_kit/entry.just'\n\nbuild:\n    echo build\n",
    )
    .unwrap();
    tool_dir(m, "tool");
    fs::create_dir_all(vk.join("gen")).unwrap();
    fs::write(vk.join("gen/tools.just"), GEN).unwrap();
}

/// `cache/<repo>/` 與它的印記（內容只是要有檔）。
fn tool_dir(m: &Mounts, repo: &str) {
    let cache = m.root.join(".vendor_kit/cache");
    fs::create_dir_all(cache.join(repo).join("just")).unwrap();
    fs::write(cache.join(format!("{repo}/just/{repo}.just")), "x:\n").unwrap();
    fs::write(cache.join(format!("{repo}.stamp.toml")), "stamp\n").unwrap();
}

/// 假啟動器：`ps` 列出 `stopped`；`rm-container` 只收 `ps` 列過的 ID（同 launcher/launch.sh），刪了就從清單拿掉。
fn launcher(m: &Mounts, stopped: Arc<Mutex<Vec<String>>>) -> std::thread::JoinHandle<Seen> {
    let ctl = m.ctl.clone();
    let listed = Arc::new(Mutex::new(Vec::<String>::new()));
    launcher::serve(&m.ctl, HEADER, move |req: &Request| match req.op.as_str() {
        "ps" => {
            let now = stopped.lock().unwrap().clone();
            let text: String = now.iter().map(|c| format!("{c}\n")).collect();
            fs::write(ctl.join(format!("res.{}.out", req.seq)), text).unwrap();
            *listed.lock().unwrap() = now;
            Reply::Ok
        }
        "rm-container" if listed.lock().unwrap().contains(&req.args[0]) => {
            stopped.lock().unwrap().retain(|c| c != &req.args[0]);
            Reply::Ok
        }
        _ => Reply::Failed(1),
    })
}

/// 跑一次 `prune`。每次執行的 session 目錄與執行紀錄都是新的（啟動器建好空的執行紀錄）。
fn run(m: &Mounts, stopped: &Arc<Mutex<Vec<String>>>) -> (i32, String, String, Seen) {
    run_with(m, stopped, &[])
}

/// 跑一次 `prune`，後面接 `extra`（例如 `--dry-run`）。
fn run_with(
    m: &Mounts,
    stopped: &Arc<Mutex<Vec<String>>>,
    extra: &[&str],
) -> (i32, String, String, Seen) {
    for d in [&m.ctl, &m.inbox] {
        fs::remove_dir_all(d).unwrap();
        fs::create_dir_all(d).unwrap();
    }
    fs::write(m.root.join(RUN_LOG), "").unwrap();
    let peer = launcher(m, Arc::clone(stopped));
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
        "prune",
    ];
    args.extend_from_slice(extra);
    let out = Command::new(vendor_kit_bin().unwrap())
        .args(&args)
        .env(MOUNT_PREFIX_ENV, &m.prefix)
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

/// 安裝目錄下每個路徑（相對、排序）與一般檔的內容，不含執行紀錄。
fn tree(m: &Mounts) -> Vec<(String, Option<Vec<u8>>)> {
    fn walk(root: &Path, dir: &Path, out: &mut Vec<(String, Option<Vec<u8>>)>) {
        for entry in fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            let rel = path.strip_prefix(root).unwrap().display().to_string();
            if path.is_dir() {
                out.push((rel, None));
                walk(root, &path, out);
            } else {
                out.push((rel, Some(fs::read(&path).unwrap())));
            }
        }
    }
    let mut out = Vec::new();
    walk(&m.root, &m.root, &mut out);
    out.retain(|(p, _)| !p.starts_with(".vendor_kit/log"));
    out.sort();
    out
}

fn paths(m: &Mounts) -> Vec<String> {
    tree(m).into_iter().map(|(p, _)| p).collect()
}

#[test]
fn residue_is_cleaned_and_listed() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    installed(&m);
    // `remove` 留給 `prune` 的：未鎖定的工具目錄與印記；寫檔中斷留下的暫存；已停止的 VK 容器。
    tool_dir(&m, "old");
    fs::write(m.root.join(".vendor_kit/.tmp.version.toml.7.0"), "half\n").unwrap();
    let lock_before = fs::read(m.root.join(".vendor_kit/version.toml")).unwrap();
    let stopped = Arc::new(Mutex::new(vec![STOPPED.to_owned()]));

    let (code, stdout, stderr, seen) = run(&m, &stopped);

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
Removed .vendor_kit/.tmp.version.toml.7.0.
Removed .vendor_kit/cache/old/.
Removed .vendor_kit/cache/old.stamp.toml.
Removed stopped container aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.

"#]]
    );
    assert_data_eq!(stderr, "");
    assert_eq!(
        seen.requests,
        ["ps".to_owned(), format!("rm-container {STOPPED}")]
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert!(stopped.lock().unwrap().is_empty());
    // 仍被引用的不動：鎖定的工具目錄與印記、入口檔、版本鎖定行、repo 檔。
    assert_eq!(
        paths(&m),
        [
            ".vendor_kit",
            ".vendor_kit/cache",
            ".vendor_kit/cache/tool",
            ".vendor_kit/cache/tool.stamp.toml",
            ".vendor_kit/cache/tool/just",
            ".vendor_kit/cache/tool/just/tool.just",
            ".vendor_kit/gen",
            ".vendor_kit/gen/tools.just",
            ".vendor_kit/version.toml",
            "justfile",
        ]
    );
    assert_eq!(
        fs::read(m.root.join(".vendor_kit/version.toml")).unwrap(),
        lock_before
    );
    assert_eq!(
        fs::read_to_string(m.root.join(".vendor_kit/gen/tools.just")).unwrap(),
        GEN
    );
    assert_eq!(
        events(&m),
        [
            "engine_started",
            "writes_started",
            "progress_removed",
            "engine_finished"
        ]
    );

    // 再跑一次：已經沒有殘留。
    let before = tree(&m);
    let (code, stdout, stderr, seen) = run(&m, &stopped);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(stdout, "");
    assert_data_eq!(stderr, "");
    assert_eq!(seen.requests, ["ps"]);
    assert_eq!(tree(&m), before);
    assert_eq!(events(&m), ["engine_started", "engine_finished"]);
}

#[test]
fn nothing_to_prune_changes_nothing() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    installed(&m);
    let before = tree(&m);
    let stopped = Arc::new(Mutex::new(Vec::new()));

    let (code, stdout, stderr, seen) = run(&m, &stopped);

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(stdout, "");
    assert_data_eq!(stderr, "");
    assert_eq!(seen.requests, ["ps"]);
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert_eq!(tree(&m), before);
    assert_eq!(events(&m), ["engine_started", "engine_finished"]);
}

#[test]
fn an_unlocked_dir_the_entry_file_still_uses_is_left_alone() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    installed(&m);
    // `git pull` 拿掉了 `old` 的鎖定行，還沒 `sync`：入口檔仍指著 `cache/old/`。
    tool_dir(&m, "old");
    fs::write(
        m.root.join(".vendor_kit/gen/tools.just"),
        format!("mod old '../cache/old/just/old.just'\n{GEN}"),
    )
    .unwrap();
    let before = tree(&m);
    let stopped = Arc::new(Mutex::new(vec![STOPPED.to_owned()]));

    let (code, stdout, stderr, seen) = run(&m, &stopped);

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with("vendor_kit: error[VK0056]: ")
            && stderr.contains(".vendor_kit/cache/old/")
            && stderr.contains("still references"),
        "{stderr}"
    );
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_eq!(tree(&m), before);
    assert_eq!(stopped.lock().unwrap().len(), 1);
}

#[test]
fn an_incomplete_add_is_not_pruned() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    installed(&m);
    // 中斷的 add：鎖定行最後才寫，`cache/new/` 看起來沒鎖定，但恢復要用它。
    tool_dir(&m, "new");
    fs::write(
        m.root.join(".vendor_kit/.tmp.add.r0.toml"),
        "command = [\"add\", \"new\"]\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[add]\nrepo = \"new\"\n",
    )
    .unwrap();
    let before = tree(&m);
    let stopped = Arc::new(Mutex::new(Vec::new()));

    let (code, stdout, stderr, seen) = run(&m, &stopped);

    assert_eq!(code, 2, "stderr: {stderr}");
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with("vendor_kit: error[VK0056]: ")
            && stderr.contains("incomplete add operation in .vendor_kit/.tmp.add.r0.toml"),
        "{stderr}"
    );
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(tree(&m), before);
}

// ---- 預演（--dry-run，#372 N11） ----

#[test]
fn dry_run_lists_the_residue_and_removes_nothing() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    installed(&m);
    tool_dir(&m, "old");
    fs::write(m.root.join(".vendor_kit/.tmp.version.toml.7.0"), "half\n").unwrap();
    let before = tree(&m);
    let stopped = Arc::new(Mutex::new(vec![STOPPED.to_owned()]));

    let (code, stdout, stderr, seen) = run_with(&m, &stopped, &["--dry-run"]);

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
Would remove .vendor_kit/.tmp.version.toml.7.0.
Would remove .vendor_kit/cache/old/.
Would remove .vendor_kit/cache/old.stamp.toml.
Would remove stopped container aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.
Dry run: no changes were made.

"#]]
    );
    assert_data_eq!(stderr, "");
    // ps 照送（只讀），rm-container 不送。
    assert_eq!(seen.requests, ["ps"]);
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert_eq!(stopped.lock().unwrap().as_slice(), [STOPPED]);
    assert_eq!(tree(&m), before);
    assert_eq!(events(&m), ["engine_started", "engine_finished"]);
}
