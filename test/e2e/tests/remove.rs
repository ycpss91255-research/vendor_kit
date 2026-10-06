//! `remove <repo>`（04 指令表、收回插入的行、remove 與 uninstall 的收回範圍；03 輸出）：經假的啟動器跑。
//!
//! `remove` 不碰 docker，假啟動器只收 `done`；`add` 那一段照 tests/add.rs 回 inspect 與 extract。
//!
//! 工具交付初始檔的 `init.toml` 格式還沒定（見 engine/add 的缺口），經執行檔的 `add` 做不出插入行，
//! 所以有初始檔的情況直接寫好安裝目錄：版本鎖定行、`cache/tool/`、`baseline/tool.toml` 的逐檔紀錄。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::Path;

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply, Request, Seen};
use e2e::{MOUNT_PREFIX_ENV, vendor_kit_bin};
use sha2::{Digest, Sha256};
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
/// 根 `.gitignore`：使用者原本的一行，加上工具插入的一行。
const GITIGNORE: &str = "user-owned\n.tool-cache\n";
const INSERTED: &str = ".tool-cache";

/// 安裝目錄：只有引擎行的 `version.toml`（`tools` 是額外的 `[tools]` 內容）、空的執行紀錄、根 `justfile`。
fn install(m: &Mounts, tools: &str) {
    let vk = m.root.join(".vendor_kit");
    fs::create_dir_all(vk.join("log")).unwrap();
    let tools = if tools.is_empty() {
        String::new()
    } else {
        format!("\n[tools]\n{tools}")
    };
    fs::write(
        vk.join("version.toml"),
        format!("vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n{tools}"),
    )
    .unwrap();
    fs::write(m.root.join(RUN_LOG), "").unwrap();
    fs::write(
        m.root.join("justfile"),
        "import '.vendor_kit/entry.just'\n\nbuild:\n    echo build\n",
    )
    .unwrap();
}

/// 工具內容：`just/tool.just` 與一個一般檔。
fn tool_content(dir: &Path) {
    fs::create_dir_all(dir.join("just")).unwrap();
    fs::write(dir.join("just/tool.just"), TOOL_JUST).unwrap();
    fs::create_dir_all(dir.join("share")).unwrap();
    fs::write(dir.join("share/readme.txt"), "tool files\n").unwrap();
}

/// 已導入 `tool`、`tool` 在根 `.gitignore` 插入過一行的安裝目錄。`hash_of` 是紀錄的整檔 hash 依據的內容。
fn installed_with_insert(m: &Mounts, hash_of: &str) {
    install(m, &format!("tool = \"{IMAGE}@{DIGEST}\"\n"));
    let vk = m.root.join(".vendor_kit");
    tool_content(&vk.join("cache/tool"));
    fs::create_dir_all(vk.join("gen")).unwrap();
    fs::write(
        vk.join("gen/tools.just"),
        "mod? tool '../cache/tool/just/tool.just'\n",
    )
    .unwrap();
    fs::write(m.root.join(".gitignore"), GITIGNORE).unwrap();
    fs::create_dir_all(vk.join("baseline")).unwrap();
    fs::write(
        vk.join("baseline/tool.toml"),
        format!(
            "schema = 1\nwritten_by = \"v0.0.0\"\n\n[[file]]\npath = \".gitignore\"\nstate = \"appended\"\nlines = [\"{INSERTED}\"]\nhash = \"{}\"\n",
            file_hash(hash_of)
        ),
    )
    .unwrap();
}

/// 逐檔紀錄的整檔 hash：CRLF 正規化成 LF 後 sha256 的小寫十六進位（engine/metadata 的 `FileHash::of`）。
fn file_hash(contents: &str) -> String {
    let digest = Sha256::digest(contents.replace("\r\n", "\n").as_bytes());
    digest.iter().map(|b| format!("{b:02x}")).collect()
}

/// 回 inspect 與 extract 的假啟動器（給 `add`）；其他 op 一律失敗。
fn add_launcher(m: &Mounts) -> std::thread::JoinHandle<Seen> {
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
        "extract" => {
            tool_content(&inbox.join(&req.args[1]));
            Reply::Ok
        }
        _ => Reply::Failed(1),
    })
}

/// 什麼 op 都回失敗的假啟動器：`remove` 不該送任何 request。
fn idle_launcher(m: &Mounts) -> std::thread::JoinHandle<Seen> {
    launcher::serve(&m.ctl, HEADER, |_: &Request| Reply::Failed(1))
}

/// 每次執行的 session 目錄與執行紀錄是新的。
fn new_session(m: &Mounts) {
    for d in [&m.ctl, &m.inbox] {
        fs::remove_dir_all(d).unwrap();
        fs::create_dir_all(d).unwrap();
    }
    fs::write(m.root.join(RUN_LOG), "").unwrap();
}

/// 跑一次引擎：`--tty` 給三位旗標，`stdin` 是使用者的輸入。
fn run(m: &Mounts, tty: &str, stdin: &str, rest: &[&str]) -> (i32, String, String) {
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
        tty,
        "--no-color",
        "1",
        "--",
    ];
    args.extend_from_slice(rest);
    let out = Command::new(vendor_kit_bin().unwrap())
        .args(&args)
        .env(MOUNT_PREFIX_ENV, &m.prefix)
        .write_stdin(stdin)
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

const REMOVED_EVENTS: [&str; 6] = [
    "engine_started",
    "writes_started",
    "lock_line_write_started",
    "lock_line_written",
    "progress_removed",
    "engine_finished",
];

#[test]
fn add_then_remove_returns_to_a_clean_install_directory() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    let vk = m.root.join(".vendor_kit");
    let justfile = fs::read(m.root.join("justfile")).unwrap();

    let peer = add_launcher(&m);
    let (code, _, stderr) = run(&m, "000", "", &["add", "tool", "-i", IMAGE]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    assert!(vk.join("cache/tool/just/tool.just").is_file());

    new_session(&m);
    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run(&m, "000", "", &["remove", "tool"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
Removed tool v1.2.0 (ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222).

"#]]
    );
    assert_data_eq!(stderr, "");
    assert!(seen.requests.is_empty());
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));

    // 工具的痕跡都收回：cache/tool/、印記、入口檔裡的行、版本鎖定行；引擎行與根 justfile 不動。
    assert_eq!(
        vk_tree(&m),
        ["cache", "gen", "gen/tools.just", "version.toml"]
    );
    assert_eq!(fs::read_to_string(vk.join("gen/tools.just")).unwrap(), "");
    let lock = fs::read_to_string(vk.join("version.toml")).unwrap();
    assert!(
        lock.starts_with(&format!("vendor_kit = \"{ENGINE}\"\n")),
        "{lock}"
    );
    assert!(!lock.contains("tool ="), "{lock}");
    assert_eq!(fs::read(m.root.join("justfile")).unwrap(), justfile);
    assert_eq!(events(&m), REMOVED_EVENTS);

    // 再 remove 一次：工具已不在版本鎖定行（VK0046），不寫檔。
    new_session(&m);
    let before = vk_tree(&m);
    let lock_before = fs::read(vk.join("version.toml")).unwrap();
    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run(&m, "000", "", &["remove", "tool"]);
    peer.join().unwrap();
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0046]: Tool tool is not in the lock version lines. The requested operation did not complete.

"#]]
    );
    assert_eq!(vk_tree(&m), before);
    assert_eq!(fs::read(vk.join("version.toml")).unwrap(), lock_before);
}

#[test]
fn removing_a_tool_that_was_never_added_is_vk0046_without_writes() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    let before = vk_tree(&m);
    let lock_before = fs::read(m.root.join(".vendor_kit/version.toml")).unwrap();
    let peer = idle_launcher(&m);

    let (code, stdout, stderr) = run(&m, "000", "", &["remove", "ghost"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0046]: Tool ghost is not in the lock version lines. The requested operation did not complete.

"#]]
    );
    assert!(seen.requests.is_empty());
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
fn answering_no_keeps_the_init_file_and_everything_else() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    installed_with_insert(&m, GITIGNORE);
    let before = vk_tree(&m);
    let lock_before = fs::read(m.root.join(".vendor_kit/version.toml")).unwrap();
    let peer = idle_launcher(&m);

    let (code, stdout, stderr) = run(&m, "111", "n\n", &["remove", "tool"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
No changes were made.

"#]]
    );
    assert_data_eq!(
        stderr,
        "Remove the 1 line that tool appended to .gitignore? [y/N] "
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert_eq!(
        fs::read_to_string(m.root.join(".gitignore")).unwrap(),
        GITIGNORE
    );
    assert_eq!(vk_tree(&m), before);
    assert_eq!(
        fs::read(m.root.join(".vendor_kit/version.toml")).unwrap(),
        lock_before
    );
    assert_eq!(events(&m), ["engine_started", "engine_finished"]);
}

#[test]
fn answering_yes_retracts_the_inserted_line_and_keeps_the_file() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    installed_with_insert(&m, GITIGNORE);
    let peer = idle_launcher(&m);

    let (code, stdout, stderr) = run(&m, "111", "y\n", &["remove", "tool"]);
    peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
Removed tool v1.2.0 (ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222).
Removed inserted lines from .gitignore
Kept .gitignore

"#]]
    );
    assert_eq!(
        fs::read_to_string(m.root.join(".gitignore")).unwrap(),
        "user-owned\n"
    );
    assert_eq!(
        vk_tree(&m),
        ["baseline", "cache", "gen", "gen/tools.just", "version.toml"]
    );
    assert_eq!(events(&m), REMOVED_EVENTS);
}

#[test]
fn a_user_edited_init_file_is_kept_with_vk0061() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    // 紀錄的 hash 是工具插入後的內容；使用者之後又改了檔，hash 不同，只列不刪、不詢問。
    installed_with_insert(&m, GITIGNORE);
    let edited = format!("{GITIGNORE}user-added\n");
    fs::write(m.root.join(".gitignore"), &edited).unwrap();
    let peer = idle_launcher(&m);

    let (code, stdout, stderr) = run(&m, "000", "", &["remove", "tool"]);
    peer.join().unwrap();

    assert_eq!(code, 1, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
Removed tool v1.2.0 (ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222).
Kept .gitignore

"#]]
    );
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: warn[VK0061]: Cannot reclaim inserted lines from .gitignore: the recorded whole-file hash is missing or differs from the current hash, or the original text does not occur exactly once. The lines were not removed. Handle them manually.
Original text: .tool-cache
Currently matching line numbers: 2.

"#]]
    );
    assert_eq!(
        fs::read_to_string(m.root.join(".gitignore")).unwrap(),
        edited
    );
    assert_eq!(
        vk_tree(&m),
        ["baseline", "cache", "gen", "gen/tools.just", "version.toml"]
    );
}

#[test]
fn a_question_without_a_terminal_is_vk0002_without_writes() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    installed_with_insert(&m, GITIGNORE);
    let before = vk_tree(&m);
    let peer = idle_launcher(&m);

    let (code, stdout, stderr) = run(&m, "000", "", &["remove", "tool"]);
    peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0002]: Confirmation is required, but no terminal is available for interaction. No files were modified except the run log. Run from a terminal, or rerun with -y: just vendor_kit remove tool -y

"#]]
    );
    assert_eq!(
        fs::read_to_string(m.root.join(".gitignore")).unwrap(),
        GITIGNORE
    );
    assert_eq!(vk_tree(&m), before);
}
