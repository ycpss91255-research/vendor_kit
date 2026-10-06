//! `upgrade <repo>@<tag>`（04 指令表、成對與無害的工具升版流程、指定版本；03 輸出）：經假的啟動器跑。
//!
//! 每個測試在暫存目錄建好安裝目錄（工具 `tool` 已在 v1.0.0）與 session 的 `ctl/`、`in/`，以
//! [`MOUNT_PREFIX_ENV`] 讓引擎把它們當成 `/vk/root`、`/vk/ctl`、`/vk/in`；假啟動器在背景回 inspect 與
//! extract。
//!
//! 基準版合併、合併衝突（VK0021）、答否與不能互動都要工具交付初始檔，而 `init.toml` 的格式還沒定（見
//! engine/upgrade 的缺口），經執行檔做不出會詢問的工具，所以這幾種在 engine/upgrade 的單元測試裡驗；
//! 這裡驗工具交付 `init.toml` 時在任何寫入之前停下。
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
const ENGINE: &str = "ghcr.io/ycpss91255-research/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const OLD: &str = "ghcr.io/acme/tool:v1.0.0@sha256:3333333333333333333333333333333333333333333333333333333333333333";
const IMAGE: &str = "ghcr.io/acme/tool:v1.2.0";
const DIGEST: &str = "sha256:2222222222222222222222222222222222222222222222222222222222222222";
const IMAGE_ID: &str = "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";

/// 安裝目錄：`version.toml` 有引擎與 `tool` v1.0.0、`cache/tool/` 是舊版內容、`gen/tools.just`、
/// 啟動器建好的空執行紀錄、根 `justfile`。
fn install(m: &Mounts) {
    let vk = m.root.join(".vendor_kit");
    fs::create_dir_all(vk.join("log")).unwrap();
    fs::write(
        vk.join("version.toml"),
        format!(
            "vendor_kit = \"{ENGINE}\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"{OLD}\"\n"
        ),
    )
    .unwrap();
    fs::create_dir_all(vk.join("cache/tool/just")).unwrap();
    fs::write(vk.join("cache/tool/just/tool.just"), "old:\n    echo old\n").unwrap();
    fs::create_dir_all(vk.join("gen")).unwrap();
    fs::write(
        vk.join("gen/tools.just"),
        "mod? tool '../cache/tool/just/tool.just'\n",
    )
    .unwrap();
    fs::write(m.root.join(RUN_LOG), "").unwrap();
    fs::write(
        m.root.join("justfile"),
        "import '.vendor_kit/entry.just'\n\nbuild:\n    echo build\n",
    )
    .unwrap();
}

/// 新版工具內容：`just/tool.just`、一個一般檔；`init` 為真時另交付 `init.toml`。
fn tool_content(dir: &Path, init: bool) {
    fs::create_dir_all(dir.join("just")).unwrap();
    fs::write(dir.join("just/tool.just"), "hello:\n    echo hi\n").unwrap();
    fs::create_dir_all(dir.join("share")).unwrap();
    fs::write(dir.join("share/readme.txt"), "tool files v1.2.0\n").unwrap();
    if init {
        fs::write(dir.join("init.toml"), "").unwrap();
    }
}

/// 回 inspect（帶 RepoDigests）與 extract 的假啟動器。
fn launcher(m: &Mounts, init: bool) -> std::thread::JoinHandle<Seen> {
    let (ctl, inbox) = (m.ctl.clone(), m.inbox.clone());
    launcher::serve(&m.ctl, HEADER, move |req: &Request| match req.op.as_str() {
        "inspect" => {
            let digests = [format!("ghcr.io/acme/tool@{DIGEST}")];
            let digests: Vec<&str> = digests.iter().map(String::as_str).collect();
            fs::write(
                ctl.join(format!("res.{}.out", req.seq)),
                launcher::inspect_json(IMAGE_ID, &digests),
            )
            .unwrap();
            Reply::Ok
        }
        "extract" if inbox.join(&req.args[1]).exists() => Reply::Failed(1),
        "extract" => {
            tool_content(&inbox.join(&req.args[1]), init);
            Reply::Ok
        }
        _ => Reply::Failed(1),
    })
}

/// 跑一次 `upgrade`。
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
        .write_stdin("")
        .output()
        .unwrap();
    (
        out.status.code().unwrap(),
        String::from_utf8(out.stdout).unwrap(),
        String::from_utf8(out.stderr).unwrap(),
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

/// 安裝目錄下每個檔的內容（依路徑排序），不含執行紀錄。
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
    let mut out = Vec::new();
    walk(&m.root, &mut out);
    out.retain(|(p, _)| !p.ends_with(RUN_LOG));
    out.sort();
    out
}

/// 換版成功之後的狀態：版本鎖定行最後一行是新版，`cache/`、印記、入口檔跟著換，進度檔不在。
fn assert_upgraded(m: &Mounts) {
    let vk = m.root.join(".vendor_kit");
    let lock = fs::read_to_string(vk.join("version.toml")).unwrap();
    assert!(
        lock.ends_with(&format!("[tools]\ntool = \"{IMAGE}@{DIGEST}\"\n")),
        "{lock}"
    );
    assert!(
        lock.starts_with(&format!("vendor_kit = \"{ENGINE}\"\n")),
        "{lock}"
    );
    assert_eq!(
        fs::read_to_string(vk.join("cache/tool/just/tool.just")).unwrap(),
        "hello:\n    echo hi\n"
    );
    assert_eq!(
        fs::read_to_string(vk.join("cache/tool/share/readme.txt")).unwrap(),
        "tool files v1.2.0\n"
    );
    let stamp = fs::read_to_string(vk.join("cache/tool.stamp.toml")).unwrap();
    assert!(
        stamp.contains(&format!("version = \"{IMAGE}@{DIGEST}\"")),
        "{stamp}"
    );
    assert_data_eq!(
        fs::read_to_string(vk.join("gen/tools.just")).unwrap(),
        snapbox::str![[r#"
mod? tool '../cache/tool/just/tool.just'

"#]]
    );
    let progress: Vec<_> = fs::read_dir(&vk)
        .unwrap()
        .filter_map(|e| {
            let name = e.unwrap().file_name().to_string_lossy().into_owned();
            name.starts_with(".tmp.").then_some(name)
        })
        .collect();
    assert!(progress.is_empty(), "{progress:?}");
}

#[test]
fn upgrade_to_a_new_tag_lands_cache_stamp_entry_and_lock_line() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let peer = launcher(&m, false);

    let (code, stdout, stderr) = run(&m, &["upgrade", "tool@v1.2.0"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
Upgraded tool from v1.0.0 to v1.2.0 (ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222).

"#]]
    );
    assert_data_eq!(stderr, "");
    assert_eq!(
        seen.requests,
        [
            format!("inspect {IMAGE}"),
            format!("extract {IMAGE_ID} tool1"),
        ]
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert_upgraded(&m);
    assert_eq!(
        events(&m),
        [
            "engine_started",
            "writes_started",
            "lock_line_write_started",
            "lock_line_written",
            "progress_removed",
            "engine_finished",
        ]
    );

    // 已是該版：stdout 說明未變更，不送任何 docker 動作、不寫檔。每次執行的 session 目錄是新的。
    let before = snapshot(&m);
    for d in [&m.ctl, &m.inbox] {
        fs::remove_dir_all(d).unwrap();
        fs::create_dir_all(d).unwrap();
    }
    fs::write(m.root.join(RUN_LOG), "").unwrap();
    let peer = launcher(&m, false);
    let (code, stdout, stderr) = run(&m, &["upgrade", "tool@v1.2.0"]);
    let seen = peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
tool is already at v1.2.0; no changes were made.

"#]]
    );
    assert_data_eq!(stderr, "");
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(snapshot(&m), before);
    assert_eq!(events(&m), ["engine_started", "engine_finished"]);
}

#[test]
fn yes_is_accepted_and_skips_the_prompt() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let peer = launcher(&m, false);

    // `--tty 000`：沒有終端也照樣做完（沒有初始檔時本來就沒有詢問，`-y` 不改變結果）。
    let (code, stdout, stderr) = run(&m, &["upgrade", "-y", "tool@v1.2.0"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert!(
        stdout.starts_with("Upgraded tool from v1.0.0 to v1.2.0 "),
        "{stdout}"
    );
    assert_data_eq!(stderr, "");
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert_upgraded(&m);
}

#[test]
fn tool_delivering_init_toml_stops_before_any_write() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let before = snapshot(&m);
    let peer = launcher(&m, true);

    let (code, stdout, stderr) = run(&m, &["upgrade", "tool@v1.2.0"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with(
            "vendor_kit: error[VK0056]: Internal vendor_kit error: the tool delivers init.toml, but its format is not specified yet"
        ),
        "{stderr}"
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_eq!(snapshot(&m), before);
    assert_eq!(
        events(&m),
        ["engine_started", "diagnostic_emitted", "engine_finished"]
    );
}

#[test]
fn upgrade_without_a_tag_stops_at_the_tag_listing_gap() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let before = snapshot(&m);
    let peer = launcher(&m, false);

    let (code, stdout, stderr) = run(&m, &["upgrade", "tool"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.contains("error[VK0056]") && stderr.contains("listing tags from the registry"),
        "{stderr}"
    );
    assert!(seen.requests.is_empty());
    assert_eq!(snapshot(&m), before);
}
