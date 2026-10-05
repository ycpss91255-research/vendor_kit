//! `add`（04 指令表、03 輸出）：經假的啟動器跑完整的 `add <repo> -i <image>`。
//!
//! 每個測試在暫存目錄建好安裝目錄與 session 的 `ctl/`、`in/`，以 [`MOUNT_PREFIX_ENV`] 讓引擎把它們
//! 當成 `/vk/root`、`/vk/ctl`、`/vk/in`；假啟動器在背景回 inspect 與 extract。
//!
//! 答否與不能互動要有詢問，而 `add` 的詢問只來自初始檔；工具交付初始檔的 `init.toml` 格式還沒定
//! （見 engine/add 的缺口），經執行檔還做不出會詢問的工具，所以這兩種只在 engine/add 的單元測試裡驗。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::Path;

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply, Request, Seen};
use e2e::{MOUNT_PREFIX_ENV, vendor_kit_bin};
use snapbox::assert_data_eq;

const RUN_ID: &str = "r1";
const HEADER: &str = "vk-resolve/1 r1";
const HOST_ROOT: &str = "/srv/proj";
const RUN_LOG: &str = ".vendor_kit/log/r1.jsonl";
const ENGINE: &str = "ghcr.io/ycpss91255-research/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const IMAGE: &str = "ghcr.io/acme/tool:v1.2.0";
const DIGEST: &str = "sha256:2222222222222222222222222222222222222222222222222222222222222222";
const IMAGE_ID: &str = "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const TOOL_JUST: &str = "hello:\n    echo hi\n";

/// 安裝目錄：只有引擎行的 `version.toml`、啟動器建好的空執行紀錄、根 `justfile`。
fn install(m: &Mounts, extra_tools: &str) {
    let vk = m.root.join(".vendor_kit");
    fs::create_dir_all(vk.join("log")).unwrap();
    let tools = if extra_tools.is_empty() {
        String::new()
    } else {
        format!("\n[tools]\n{extra_tools}")
    };
    fs::write(
        vk.join("version.toml"),
        format!("vendor_kit = \"{ENGINE}\"\nschema = 1\nwritten_by = \"v0.0.0\"\n{tools}"),
    )
    .unwrap();
    fs::write(m.root.join(RUN_LOG), "").unwrap();
    fs::write(
        m.root.join("justfile"),
        "import '.vendor_kit/entry.just'\n\nbuild:\n    echo build\n",
    )
    .unwrap();
}

/// 工具內容：`just/<ns>.just` 各一檔，外加一個一般檔。
fn tool_content(dir: &Path, namespaces: &[&str]) {
    fs::create_dir_all(dir.join("just")).unwrap();
    for ns in namespaces {
        fs::write(dir.join("just").join(format!("{ns}.just")), TOOL_JUST).unwrap();
    }
    fs::create_dir_all(dir.join("share")).unwrap();
    fs::write(dir.join("share/readme.txt"), "tool files\n").unwrap();
}

/// 回 inspect（帶 RepoDigests）與 extract（放進 `namespaces` 的工具內容）的假啟動器。
fn launcher(m: &Mounts, namespaces: &'static [&'static str]) -> std::thread::JoinHandle<Seen> {
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
        // 啟動器不收已存在的 slot（launcher/launch.sh 的 vk_launch_extract）。
        "extract" if inbox.join(&req.args[1]).exists() => Reply::Failed(1),
        "extract" => {
            tool_content(&inbox.join(&req.args[1]), namespaces);
            Reply::Ok
        }
        _ => Reply::Failed(1),
    })
}

/// 跑一次 `add`：`--tty` 給三位旗標，`cwd` 是使用者下指令時的目錄。
fn run(m: &Mounts, cwd: &str, tty: &str, rest: &[&str]) -> (i32, String, String) {
    let mut args = vec![
        "--protocol",
        "1",
        "--run-id",
        RUN_ID,
        "--host-root",
        HOST_ROOT,
        "--host-cwd",
        cwd,
        "--run-log",
        RUN_LOG,
        "--tty",
        tty,
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

/// `.vendor_kit/` 下所有路徑（相對、排序），不含執行紀錄。
fn vk_tree(m: &Mounts) -> Vec<String> {
    fn walk(root: &Path, dir: &Path, out: &mut Vec<String>) {
        for entry in fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            out.push(path.strip_prefix(root).unwrap().display().to_string());
            if path.is_dir() {
                walk(root, &path, out);
            }
        }
    }
    let root = m.root.join(".vendor_kit");
    let mut out = Vec::new();
    walk(&root, &root, &mut out);
    out.retain(|p| !p.starts_with("log"));
    out.sort();
    out
}

#[test]
fn add_from_a_local_image_lands_cache_stamp_entry_and_lock_line() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    let peer = launcher(&m, &["tool", "tool-extra"]);

    let (code, stdout, stderr) = run(&m, HOST_ROOT, "000", &["add", "tool", "-i", IMAGE]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
Added tool v1.2.0 (ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222).

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
    assert_data_eq!(
        fs::read_to_string(vk.join("gen/tools.just")).unwrap(),
        snapbox::str![[r#"
mod tool '../cache/tool/just/tool.just'
mod tool-extra '../cache/tool/just/tool-extra.just'

"#]]
    );
    assert_eq!(
        fs::read_to_string(vk.join("cache/tool/just/tool.just")).unwrap(),
        TOOL_JUST
    );
    let stamp = fs::read_to_string(vk.join("cache/tool.stamp.toml")).unwrap();
    assert!(
        stamp.contains(&format!("version = \"{IMAGE}@{DIGEST}\"")),
        "{stamp}"
    );
    assert_eq!(
        vk_tree(&m),
        [
            "cache",
            "cache/tool",
            "cache/tool.stamp.toml",
            "cache/tool/just",
            "cache/tool/just/tool-extra.just",
            "cache/tool/just/tool.just",
            "cache/tool/share",
            "cache/tool/share/readme.txt",
            "gen",
            "gen/tools.just",
            "version.toml",
        ]
    );
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

    // 同一個版本再 add 一次：stdout 說明未變更，不再取件、不寫檔。每次執行的 session 目錄是新的。
    let before = vk_tree(&m);
    let lock_before = fs::read(vk.join("version.toml")).unwrap();
    for d in [&m.ctl, &m.inbox] {
        fs::remove_dir_all(d).unwrap();
        fs::create_dir_all(d).unwrap();
    }
    let peer = launcher(&m, &["tool", "tool-extra"]);
    let (code, stdout, stderr) = run(&m, HOST_ROOT, "000", &["add", "tool", "-i", IMAGE]);
    let seen = peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
tool v1.2.0 is already added; no changes were made.

"#]]
    );
    assert_eq!(seen.requests, [format!("inspect {IMAGE}")]);
    assert_eq!(vk_tree(&m), before);
    assert_eq!(fs::read(vk.join("version.toml")).unwrap(), lock_before);
}

#[test]
fn namespace_collision_stops_before_any_write() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    // 已裝的 other 交付 shared；新工具也交付 shared。
    install(
        &m,
        "other = \"ghcr.io/acme/other:v1.0.0@sha256:3333333333333333333333333333333333333333333333333333333333333333\"\n",
    );
    tool_content(
        &m.root.join(".vendor_kit/cache/other"),
        &["other", "shared"],
    );
    let before = vk_tree(&m);
    let lock_before = fs::read(m.root.join(".vendor_kit/version.toml")).unwrap();
    let peer = launcher(&m, &["tool", "shared"]);

    let (code, stdout, stderr) = run(&m, HOST_ROOT, "000", &["add", "tool", "-i", IMAGE]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0030]: Cannot add tool: namespace shared is already used by other.

"#]]
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_eq!(vk_tree(&m), before);
    assert_eq!(
        fs::read(m.root.join(".vendor_kit/version.toml")).unwrap(),
        lock_before
    );
    assert_eq!(
        events(&m),
        ["engine_started", "diagnostic_emitted", "engine_finished"]
    );
}

#[test]
fn reserved_name_is_rejected_without_fetching() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    let before = vk_tree(&m);
    let peer = launcher(&m, &["vendor_kit"]);

    let (code, stdout, stderr) = run(&m, HOST_ROOT, "111", &["add", "vendor_kit", "-i", IMAGE]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0057]: Cannot add vendor_kit: vendor_kit is a reserved name. Use a different tool name.

"#]]
    );
    assert!(seen.requests.is_empty());
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_eq!(vk_tree(&m), before);
}

#[test]
fn outside_the_install_directory_is_pending_with_cd() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    let before = vk_tree(&m);
    let peer = launcher(&m, &["tool"]);

    let (code, stdout, stderr) = run(&m, "/srv/proj/sub", "000", &["add", "tool", "-i", IMAGE]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0028]: The current directory is not an install directory. Run: cd /srv/proj

"#]]
    );
    assert!(seen.requests.is_empty());
    assert_eq!(vk_tree(&m), before);
}
