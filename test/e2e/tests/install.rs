//! `install`（04 指令表、首次導入還是既有安裝目錄、寫入既有檔的例外、成對與無害；03 輸出）：
//! 經假的啟動器跑。
//!
//! `install` 不碰 docker，假啟動器只收 `done`；`add` 那一段照 tests/add.rs 回 inspect 與 extract。
//! 薄殼模板隨 image 出貨（放在 image 裡的固定目錄），e2e 在主機上直接跑執行檔讀不到，所以除了驗沒有模板的
//! 那一則，都以測試用的 `VK_TEST_RELEASE_DIR`（engine/vendor_kit 的 `RELEASE_DIR_ENV`）從 fixture 目錄讀進模板；
//! 根 `justfile` 與 `.dockerignore` 的內容是引擎出貨的常數。啟動器在起引擎前已建好 `.vendor_kit/log/` 與這次的執行紀錄，
//! 並把這次的引擎引用寫成 `in/engine`，fixture 每次執行都照做。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::Path;

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply, Request, Seen};
use e2e::{MOUNT_PREFIX_ENV, VERSION, vendor_kit_bin};

const RUN_ID: &str = "r1";
const HEADER: &str = "vk-resolve/1 r1";
const HOST_ROOT: &str = "/srv/proj";
const RUN_LOG: &str = ".vendor_kit/log/r1.jsonl";
/// 測試用的出貨輸入目錄（engine/vendor_kit 的 `RELEASE_DIR_ENV`；這裡不能依賴 engine crate，照抄名字）。
const RELEASE_DIR_ENV: &str = "VK_TEST_RELEASE_DIR";
/// 啟動器放引擎引用的檔（`in/` 裡；engine/plan 的 `files::IN_ENGINE`，照抄名字）。
const IN_ENGINE: &str = "engine";
const ENGINE_REPO: &str = "ghcr.io/ycpss91255-research/vendor_kit";
const ENGINE_DIGEST: &str =
    "sha256:1111111111111111111111111111111111111111111111111111111111111111";
const IMAGE: &str = "ghcr.io/acme/tool:v1.2.0";
const DIGEST: &str = "sha256:2222222222222222222222222222222222222222222222222222222222222222";
const IMAGE_ID: &str = "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const IMPORT: &str = "import '.vendor_kit/entry.just'";
const DEFAULT: &str = "default:\n    @just --list\n";
const SHELL: [(&str, &str); 4] = [
    ("entry.just", "# entry\nimport? 'vendor.just'\n"),
    ("vendor.just", "# vendor\n"),
    ("log.sh", "# log\n"),
    (
        ".gitignore",
        "cache/\ngen/\nlog/\nversion.local.toml\n.tmp.*\n",
    ),
];
const DOCKERIGNORE: &str =
    ".vendor_kit/cache/\n.vendor_kit/gen/\n.vendor_kit/log/\n.vendor_kit/version.local.toml\n";
const USER_JUSTFILE: &str = "build:\n    echo build\n";
const USER_DOCKERIGNORE: &str = "target/\n";

const LANDED: [&str; 6] = [
    "engine_started",
    "writes_started",
    "lock_line_write_started",
    "lock_line_written",
    "progress_removed",
    "engine_finished",
];

/// 這個引擎自己的 pinned 引用（tag 是本引擎版）。
fn engine() -> String {
    format!("{ENGINE_REPO}:{VERSION}@{ENGINE_DIGEST}")
}

/// 出貨輸入的 fixture 目錄：薄殼模板。
fn release(dir: &Path) {
    fs::create_dir_all(dir.join("shell")).unwrap();
    for (name, body) in SHELL {
        fs::write(dir.join("shell").join(name), body).unwrap();
    }
}

/// 啟動器起引擎前寫的引擎引用檔。
fn engine_ref(m: &Mounts, contents: &str) {
    fs::write(m.inbox.join(IN_ENGINE), contents).unwrap();
}

/// 啟動器起引擎前的安裝目錄與 session：`.vendor_kit/log/`、空的執行紀錄與引擎引用檔。
fn fresh(m: &Mounts) {
    fs::create_dir_all(m.root.join(".vendor_kit/log")).unwrap();
    fs::write(m.root.join(RUN_LOG), "").unwrap();
    engine_ref(m, &format!("{}\n", engine()));
}

/// 每次執行的 session 目錄與執行紀錄是新的。
fn new_session(m: &Mounts) {
    for d in [&m.ctl, &m.inbox] {
        fs::remove_dir_all(d).unwrap();
        fs::create_dir_all(d).unwrap();
    }
    fs::write(m.root.join(RUN_LOG), "").unwrap();
    engine_ref(m, &format!("{}\n", engine()));
}

/// 工具內容：`just/tool.just` 與一個一般檔。
fn tool_content(dir: &Path) {
    fs::create_dir_all(dir.join("just")).unwrap();
    fs::write(dir.join("just/tool.just"), "hello:\n    echo hi\n").unwrap();
    fs::create_dir_all(dir.join("share")).unwrap();
    fs::write(dir.join("share/readme.txt"), "tool files\n").unwrap();
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

/// 什麼 op 都回失敗的假啟動器：`install`、`remove`、`uninstall` 不該送任何 request。
fn idle_launcher(m: &Mounts) -> std::thread::JoinHandle<Seen> {
    launcher::serve(&m.ctl, HEADER, |_: &Request| Reply::Failed(1))
}

/// 跑一次引擎：`--tty` 給三位旗標，`stdin` 是使用者的輸入；`release` 是出貨輸入目錄。
fn run(
    m: &Mounts,
    release: Option<&Path>,
    tty: &str,
    stdin: &str,
    rest: &[&str],
) -> (i32, String, String) {
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
    let mut cmd = Command::new(vendor_kit_bin().unwrap());
    cmd.args(&args).env(MOUNT_PREFIX_ENV, &m.prefix);
    match release {
        Some(dir) => cmd.env(RELEASE_DIR_ENV, dir),
        None => cmd.env_remove(RELEASE_DIR_ENV),
    };
    let out = cmd.write_stdin(stdin).output().unwrap();
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
    out.retain(|p| p != "log" && !p.starts_with("log/"));
    out.sort();
    out
}

fn read(m: &Mounts, rel: &str) -> String {
    fs::read_to_string(m.root.join(rel)).unwrap()
}

const INSTALLED_TREE: [&str; 12] = [
    ".gitignore",
    "baseline",
    "baseline/.vendor_kit",
    "baseline/.vendor_kit.toml",
    "baseline/.vendor_kit/config.toml",
    "config.toml",
    "entry.just",
    "gen",
    "gen/.stamp",
    "log.sh",
    "vendor.just",
    "version.toml",
];

#[test]
fn install_in_an_empty_repo_writes_everything_without_asking() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(&tmp.path().join("m"));
    let rel = tmp.path().join("release");
    release(&rel);
    fresh(&m);
    let peer = idle_launcher(&m);

    let (code, stdout, stderr) = run(&m, Some(&rel), "000", "", &["install"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    let engine = engine();
    assert_eq!(
        stdout,
        format!(
            "Locked the engine to {VERSION} ({engine}).\n\
             Wrote .vendor_kit/entry.just\nWrote .vendor_kit/vendor.just\n\
             Wrote .vendor_kit/log.sh\nWrote .vendor_kit/.gitignore\n\
             Created justfile\nCreated .dockerignore\nCreated .vendor_kit/config.toml\n\
             Installed vendor_kit {VERSION} in {HOST_ROOT}.\n"
        )
    );
    assert_eq!(stderr, "");
    assert!(seen.requests.is_empty());
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert_eq!(vk_tree(&m), INSTALLED_TREE);
    assert_eq!(events(&m), LANDED);
    // 引擎鎖定行在第一行，緊接著記這版引擎接受的介面版（N13）。
    let lock = read(&m, ".vendor_kit/version.toml");
    assert!(
        lock.starts_with(&format!(
            "vendor_kit = \"{engine}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \""
        )),
        "{lock}"
    );
    assert_eq!(read(&m, "justfile"), format!("{IMPORT}\n\n{DEFAULT}"));
    assert_eq!(read(&m, ".dockerignore"), DOCKERIGNORE);
    // 薄殼帶自描述標頭，其餘是模板本文原樣。
    let entry = read(&m, ".vendor_kit/entry.just");
    assert!(
        entry.starts_with("# vendor_kit-shell interface 1\n") && entry.ends_with(SHELL[0].1),
        "{entry}"
    );
    // `gen/.stamp`：產生薄殼的引擎 ref。
    assert_eq!(read(&m, ".vendor_kit/gen/.stamp"), format!("{engine}\n"));
    // `config.toml`：引擎出貨的模板，欄位全部註解掉；基準版副本是同一份，紀錄記成 `managed`。
    let config = read(&m, ".vendor_kit/config.toml");
    assert!(
        config.contains("# lock_timeout_seconds = 60\n")
            && config.lines().all(|l| l.is_empty() || l.starts_with('#')),
        "{config}"
    );
    assert_eq!(
        read(&m, ".vendor_kit/baseline/.vendor_kit/config.toml"),
        config
    );
    let record = read(&m, ".vendor_kit/baseline/.vendor_kit.toml");
    assert!(
        record.contains("path = \".vendor_kit/config.toml\"\nstate = \"managed\"\n"),
        "{record}"
    );
}

/// `install` 寫的薄殼就是 `sync` 判薄殼時用的同一份模板產生的：接著跑 `sync` 不報 VK0006。
#[test]
fn sync_after_install_accepts_the_shell() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(&tmp.path().join("m"));
    let rel = tmp.path().join("release");
    release(&rel);
    fresh(&m);
    let peer = idle_launcher(&m);
    let (code, _, stderr) = run(&m, Some(&rel), "000", "", &["install"]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");

    new_session(&m);
    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run(&m, Some(&rel), "000", "", &["sync"]);
    let seen = peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(stderr, "");
    assert!(seen.requests.is_empty());
    assert_eq!(stdout, "Updated .vendor_kit/gen/tools.just.\n");
}

#[test]
fn installing_again_changes_nothing() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(&tmp.path().join("m"));
    let rel = tmp.path().join("release");
    release(&rel);
    fresh(&m);
    let peer = idle_launcher(&m);
    let (code, _, stderr) = run(&m, Some(&rel), "000", "", &["install"]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    let before = vk_tree(&m);
    let lock = read(&m, ".vendor_kit/version.toml");
    let justfile = read(&m, "justfile");

    new_session(&m);
    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run(&m, Some(&rel), "000", "", &["install"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(
        stdout,
        format!("vendor_kit is already installed in {HOST_ROOT}; no changes were made.\n")
    );
    assert_eq!(stderr, "");
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert_eq!(events(&m), ["engine_started", "engine_finished"]);
    assert_eq!(vk_tree(&m), before);
    assert_eq!(read(&m, ".vendor_kit/version.toml"), lock);
    assert_eq!(read(&m, "justfile"), justfile);
}

#[test]
fn install_add_remove_uninstall_returns_to_a_clean_repo() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(&tmp.path().join("m"));
    let rel = tmp.path().join("release");
    release(&rel);
    fresh(&m);
    fs::write(m.root.join("justfile"), USER_JUSTFILE).unwrap();
    fs::write(m.root.join(".dockerignore"), USER_DOCKERIGNORE).unwrap();

    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run(&m, Some(&rel), "111", "y\ny\n", &["install"]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(
        stderr,
        "Append 1 vendor_kit line to the existing justfile? [y/N] \
         Append 4 vendor_kit lines to the existing .dockerignore? [y/N] "
    );
    assert!(
        stdout.contains("Appended to justfile\nAppended to .dockerignore\n"),
        "{stdout}"
    );
    assert_eq!(read(&m, "justfile"), format!("{USER_JUSTFILE}{IMPORT}\n"));
    assert_eq!(
        read(&m, ".dockerignore"),
        format!("{USER_DOCKERIGNORE}{DOCKERIGNORE}")
    );

    new_session(&m);
    let peer = add_launcher(&m);
    let (code, _, stderr) = run(&m, None, "000", "", &["add", "tool", "-i", IMAGE]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    assert!(
        m.root
            .join(".vendor_kit/cache/tool/just/tool.just")
            .is_file()
    );

    new_session(&m);
    let peer = idle_launcher(&m);
    let (code, _, stderr) = run(&m, None, "000", "", &["remove", "tool"]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");

    new_session(&m);
    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run(&m, None, "111", "y\ny\n", &["uninstall"]);
    let seen = peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(
        stderr,
        "Remove the 1 line that vendor_kit appended to justfile? [y/N] \
         Remove the 4 lines that vendor_kit appended to .dockerignore? [y/N] "
    );
    assert!(seen.requests.is_empty());
    assert!(
        stdout.starts_with(&format!("Uninstalled vendor_kit from {HOST_ROOT}.\n")),
        "{stdout}"
    );

    // `config.toml` 是使用者維護的檔（04 uninstall 保留），stdout 列一次。
    assert_eq!(
        stdout.matches("Kept .vendor_kit/config.toml\n").count(),
        1,
        "{stdout}"
    );

    // 使用者的檔回到 install 之前，`.vendor_kit/` 只剩執行紀錄與 `config.toml`。
    assert_eq!(read(&m, "justfile"), USER_JUSTFILE);
    assert_eq!(read(&m, ".dockerignore"), USER_DOCKERIGNORE);
    assert_eq!(vk_tree(&m), ["config.toml"]);
}

#[test]
fn uninstall_without_a_terminal_follows_the_next_step_of_vk0002() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(&tmp.path().join("m"));
    let rel = tmp.path().join("release");
    release(&rel);
    fresh(&m);
    fs::write(m.root.join("justfile"), USER_JUSTFILE).unwrap();
    fs::write(m.root.join(".dockerignore"), USER_DOCKERIGNORE).unwrap();
    let peer = idle_launcher(&m);
    let (code, _, stderr) = run(&m, Some(&rel), "000", "", &["install", "-y"]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");

    // 沒有終端機：uninstall 要問收回根目錄的插入行，回 VK0002，除執行紀錄外不寫。
    new_session(&m);
    let before = vk_tree(&m);
    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run(&m, None, "000", "", &["uninstall"]);
    peer.join().unwrap();
    assert_eq!(code, 2, "stderr: {stderr}");
    assert_eq!(stdout, "");
    assert_eq!(
        stderr,
        "vendor_kit: error[VK0002]: Confirmation is required, but no terminal is available for interaction. No files were modified except the run log. Run from a terminal, or rerun with -y: just vendor_kit uninstall -y\n"
    );
    assert_eq!(vk_tree(&m), before);

    // 照它的下一步跑（#638 發現這一步原本是用法錯誤 VK0026）。
    let (_, next) = stderr
        .trim_end()
        .split_once("rerun with -y: just vendor_kit ")
        .unwrap();
    let next: Vec<&str> = next.split(' ').collect();
    new_session(&m);
    let peer = idle_launcher(&m);
    let (code, stdout, stderr) = run(&m, None, "000", "", &next);
    let seen = peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(stderr, "");
    assert!(seen.requests.is_empty());
    assert!(
        stdout.starts_with(&format!("Uninstalled vendor_kit from {HOST_ROOT}.\n")),
        "{stdout}"
    );
    assert_eq!(read(&m, "justfile"), USER_JUSTFILE);
    assert_eq!(read(&m, ".dockerignore"), USER_DOCKERIGNORE);
    assert_eq!(vk_tree(&m), ["config.toml"]);
}

#[test]
fn answering_no_for_an_existing_justfile_writes_nothing() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(&tmp.path().join("m"));
    let rel = tmp.path().join("release");
    release(&rel);
    fresh(&m);
    fs::write(m.root.join("justfile"), USER_JUSTFILE).unwrap();
    let peer = idle_launcher(&m);

    let (code, stdout, stderr) = run(&m, Some(&rel), "111", "n\n", &["install"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(stdout, "No changes were made.\n");
    assert_eq!(
        stderr,
        "Append 1 vendor_kit line to the existing justfile? [y/N] "
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert_eq!(events(&m), ["engine_started", "engine_finished"]);
    assert_eq!(read(&m, "justfile"), USER_JUSTFILE);
    assert!(!m.root.join(".dockerignore").exists());
    assert!(vk_tree(&m).is_empty());
}

#[test]
fn an_existing_justfile_without_a_terminal_is_vk0002_without_writes() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(&tmp.path().join("m"));
    let rel = tmp.path().join("release");
    release(&rel);
    fresh(&m);
    fs::write(m.root.join("justfile"), USER_JUSTFILE).unwrap();
    let peer = idle_launcher(&m);

    let (code, stdout, stderr) = run(&m, Some(&rel), "000", "", &["install"]);
    peer.join().unwrap();

    assert_eq!(code, 2);
    assert_eq!(stdout, "");
    assert_eq!(
        stderr,
        "vendor_kit: error[VK0002]: Confirmation is required, but no terminal is available for interaction. No files were modified except the run log. Run from a terminal, or rerun with -y: just vendor_kit install -y\n"
    );
    assert_eq!(read(&m, "justfile"), USER_JUSTFILE);
    assert!(vk_tree(&m).is_empty());
}

#[test]
fn install_without_the_shipped_inputs_is_vk0056_without_writes() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(&tmp.path().join("m"));
    fresh(&m);
    let peer = idle_launcher(&m);

    let (code, stdout, stderr) = run(&m, None, "000", "", &["install"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_eq!(stdout, "");
    assert!(
        stderr.starts_with("vendor_kit: error[VK0056]: ")
            && stderr.contains(
                "install without the shell templates, which this engine image does not ship"
            )
            && !stderr.contains("engine reference"),
        "{stderr}"
    );
    assert!(seen.requests.is_empty());
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_eq!(
        events(&m),
        ["engine_started", "diagnostic_emitted", "engine_finished"]
    );
    assert!(vk_tree(&m).is_empty());
    assert!(!m.root.join("justfile").exists());
}

/// 首次導入時 `in/engine` 不合：VK0056 寫明哪裡不一致，除執行紀錄外什麼都不寫。
fn bad_engine_ref(contents: Option<&str>, reason: &str) {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(&tmp.path().join("m"));
    let rel = tmp.path().join("release");
    release(&rel);
    fresh(&m);
    match contents {
        Some(c) => engine_ref(&m, c),
        None => fs::remove_file(m.inbox.join(IN_ENGINE)).unwrap(),
    }
    let peer = idle_launcher(&m);

    let (code, stdout, stderr) = run(&m, Some(&rel), "000", "", &["install"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2, "stderr: {stderr}");
    assert_eq!(stdout, "");
    assert!(
        stderr.starts_with(
            "vendor_kit: error[VK0056]: Internal vendor_kit error: \
             the engine reference in/engine from the launcher"
        ) && stderr.contains(reason),
        "{reason}: {stderr}"
    );
    assert!(seen.requests.is_empty());
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_eq!(
        events(&m),
        ["engine_started", "diagnostic_emitted", "engine_finished"]
    );
    assert!(vk_tree(&m).is_empty());
    assert!(!m.root.join("justfile").exists());
    assert!(!m.root.join(".dockerignore").exists());
}

#[test]
fn engine_ref_with_another_tag_is_vk0056_without_writes() {
    let other = format!("{ENGINE_REPO}:v99.0.0@{ENGINE_DIGEST}");
    bad_engine_ref(
        Some(&format!("{other}\n")),
        &format!("has tag v99.0.0, not this engine's {VERSION}"),
    );
}

#[test]
fn engine_ref_with_another_path_is_vk0056_without_writes() {
    let other = format!("ghcr.io/acme/vendor_kit:{VERSION}@{ENGINE_DIGEST}");
    bad_engine_ref(
        Some(&format!("{other}\n")),
        &format!("names ghcr.io/acme/vendor_kit, not this engine's {ENGINE_REPO}"),
    );
}

#[test]
fn missing_engine_ref_is_vk0056_without_writes() {
    bad_engine_ref(None, "is missing");
}

// ---- 預演（--dry-run，#372 N11） ----

/// 安裝目錄裡全部的檔與內容（相對路徑、排序），不含 `.vendor_kit/log/`：比對預演前後一個位元組都沒變。
fn snapshot(m: &Mounts) -> Vec<(String, Option<Vec<u8>>)> {
    fn walk(root: &Path, dir: &Path, out: &mut Vec<(String, Option<Vec<u8>>)>) {
        for entry in fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            let rel = path.strip_prefix(root).unwrap().display().to_string();
            if rel == ".vendor_kit/log" {
                continue;
            }
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
    out.sort();
    out
}

#[test]
fn install_dry_run_prints_the_plan_and_writes_only_the_run_log() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(&tmp.path().join("m"));
    let rel = tmp.path().join("release");
    release(&rel);
    fresh(&m);
    fs::write(m.root.join("justfile"), USER_JUSTFILE).unwrap();
    let before = snapshot(&m);
    let engine = engine();
    let expected = format!(
        "Would lock the engine to {VERSION} ({engine}).\n\
         Would write .vendor_kit/entry.just\nWould write .vendor_kit/vendor.just\n\
         Would write .vendor_kit/log.sh\nWould write .vendor_kit/.gitignore\n\
         Would append to justfile\nWould create .dockerignore\n\
         Would create .vendor_kit/config.toml\n\
         Would install vendor_kit {VERSION} in {HOST_ROOT}.\n\
         Dry run: no changes were made.\n"
    );
    // 沒有終端也不問、不報 VK0002；-y 並用沒有作用。
    for rest in [
        &["install", "--dry-run"][..],
        &["install", "-y", "--dry-run"],
    ] {
        new_session(&m);
        let peer = idle_launcher(&m);
        let (code, stdout, stderr) = run(&m, Some(&rel), "000", "", rest);
        let seen = peer.join().unwrap();
        assert_eq!(code, 0, "stderr: {stderr}");
        assert_eq!(stderr, "");
        assert_eq!(stdout, expected);
        assert!(seen.requests.is_empty());
        assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
        assert_eq!(events(&m), ["engine_started", "engine_finished"]);
        assert_eq!(snapshot(&m), before);
    }
}

#[test]
fn uninstall_dry_run_prints_the_plan_and_writes_only_the_run_log() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(&tmp.path().join("m"));
    let rel = tmp.path().join("release");
    release(&rel);
    fresh(&m);
    fs::write(m.root.join("justfile"), USER_JUSTFILE).unwrap();
    fs::write(m.root.join(".dockerignore"), USER_DOCKERIGNORE).unwrap();
    let peer = idle_launcher(&m);
    let (code, _, stderr) = run(&m, Some(&rel), "000", "", &["install", "-y"]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    let before = snapshot(&m);

    // 沒有終端也不問、不報 VK0002；-y 並用沒有作用。
    for rest in [
        &["uninstall", "--dry-run"][..],
        &["uninstall", "--dry-run", "-y"],
    ] {
        new_session(&m);
        let peer = idle_launcher(&m);
        let (code, stdout, stderr) = run(&m, None, "000", "", rest);
        let seen = peer.join().unwrap();
        assert_eq!(code, 0, "stderr: {stderr}");
        assert_eq!(stderr, "");
        assert_eq!(
            stdout,
            format!(
                "Would uninstall vendor_kit from {HOST_ROOT}.\n\
                 Would remove inserted lines from .dockerignore\n\
                 Would remove inserted lines from justfile\n\
                 Would keep .dockerignore\n\
                 Would keep .vendor_kit/config.toml\n\
                 Would keep justfile\n\
                 Would keep .vendor_kit/log/\n\
                 Dry run: no changes were made.\n"
            )
        );
        assert!(seen.requests.is_empty());
        assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
        assert_eq!(events(&m), ["engine_started", "engine_finished"]);
        assert_eq!(snapshot(&m), before);
    }
}

#[test]
fn dry_run_is_not_accepted_by_sync_or_with_help() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(&tmp.path().join("m"));
    let rel = tmp.path().join("release");
    release(&rel);
    fresh(&m);
    for rest in [&["sync", "--dry-run"][..], &["install", "--dry-run", "-h"]] {
        new_session(&m);
        let peer = idle_launcher(&m);
        let (code, stdout, stderr) = run(&m, Some(&rel), "000", "", rest);
        peer.join().unwrap();
        assert_eq!(code, 2, "{rest:?}: {stderr}");
        assert_eq!(stdout, "");
        assert!(
            stderr.starts_with(
                "vendor_kit: error[VK0026]: Unknown, extra, or disallowed argument: --dry-run.\n"
            ),
            "{rest:?}: {stderr}"
        );
        assert!(vk_tree(&m).is_empty());
    }
}
