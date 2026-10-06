//! `add`（04 指令表、03 輸出）：經假的啟動器跑完整的 `add <repo> -i <image>` 與線上 `add <repo>[@<tag>]`。
//!
//! 每個測試在暫存目錄建好安裝目錄與 session 的 `ctl/`、`in/`，以 [`MOUNT_PREFIX_ENV`] 讓引擎把它們
//! 當成 `/vk/root`、`/vk/ctl`、`/vk/in`；假啟動器在背景回 inspect、pull 與 extract。registry 一律以
//! [`REGISTRY_URL_ENV`] 接到假 registry（不需要 registry 的測試給連不到的位址），不連外網。
//!
//! 答否與不能互動要有詢問，而 `add` 的詢問只來自初始檔；工具交付初始檔的 `init.toml` 格式還沒定
//! （見 engine/add 的缺口），經執行檔還做不出會詢問的工具，所以這兩種只在 engine/add 的單元測試裡驗。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::Path;

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply, Request, Seen};
use e2e::registry::{GOOD_TOKEN, Registry, Repo};
use e2e::{MOUNT_PREFIX_ENV, REGISTRY_URL_ENV, vendor_kit_bin};
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
const OTHER_DIGEST: &str =
    "sha256:5555555555555555555555555555555555555555555555555555555555555555";
/// 不需要 registry 的執行：連不到的位址，連了就會失敗。
const NO_REGISTRY: &str = "http://127.0.0.1:9";

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
    launcher_with(
        m,
        namespaces,
        true,
        vec![format!("ghcr.io/acme/tool@{DIGEST}")],
    )
}

/// 假啟動器：`local` 為假時本機沒有 `<路徑>:<tag>`（不帶 digest 的 inspect 回 failed 1，pull 之後以
/// `<路徑>@<digest>` inspect 照常回）；inspect 回的 RepoDigests 是 `digests`。
fn launcher_with(
    m: &Mounts,
    namespaces: &'static [&'static str],
    local: bool,
    digests: Vec<String>,
) -> std::thread::JoinHandle<Seen> {
    let (ctl, inbox) = (m.ctl.clone(), m.inbox.clone());
    launcher::serve(&m.ctl, HEADER, move |req: &Request| match req.op.as_str() {
        "inspect" if !local && !req.args[0].contains('@') => Reply::Failed(1),
        "pull" => Reply::Ok,
        "inspect" => {
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

/// 跑一次 `add`：`--tty` 給三位旗標，`cwd` 是使用者下指令時的目錄；不需要 registry。
fn run(m: &Mounts, cwd: &str, tty: &str, rest: &[&str]) -> (i32, String, String) {
    run_with(m, cwd, tty, rest, NO_REGISTRY)
}

/// 同 [`run`]，registry 接到 `registry`（base URL）。
fn run_with(
    m: &Mounts,
    cwd: &str,
    tty: &str,
    rest: &[&str],
    registry: &str,
) -> (i32, String, String) {
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
        .env(REGISTRY_URL_ENV, registry)
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
mod? tool '../cache/tool/just/tool.just'
mod? tool-extra '../cache/tool/just/tool-extra.just'

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

// ---- 線上 add（--image-path、列 tag、以 digest pull） ----

const ONLINE_PATH: &str = "ghcr.io/acme/tool";

/// `acme/tool` 公開，列出 `tags`；`digests` 是 `(tag, digest)`。
fn registry(tags: &[&str], digests: &[(&str, &str)]) -> Registry {
    let digests: Vec<(&str, &str, &str)> =
        digests.iter().map(|(t, d)| ("acme/tool", *t, *d)).collect();
    Registry::start_with(&[("acme/tool", Repo::public(tags))], &digests)
}

/// 本機沒有時送出的 docker 動作：inspect 不到 → 以 digest pull → 以同一個引用 inspect → extract。
fn pulled() -> Vec<String> {
    let pinned = format!("ghcr.io/acme/tool@{DIGEST}");
    vec![
        format!("inspect {IMAGE}"),
        format!("pull {pinned}"),
        format!("inspect {pinned}"),
        format!("extract {IMAGE_ID} tool1"),
    ]
}

/// 線上 add 落地後的版本鎖定行與工具內容。
fn assert_added(m: &Mounts) {
    let vk = m.root.join(".vendor_kit");
    let lock = fs::read_to_string(vk.join("version.toml")).unwrap();
    assert!(
        lock.ends_with(&format!("[tools]\ntool = \"{IMAGE}@{DIGEST}\"\n")),
        "{lock}"
    );
    assert_eq!(
        fs::read_to_string(vk.join("cache/tool/just/tool.just")).unwrap(),
        TOOL_JUST
    );
}

#[test]
fn add_without_a_tag_lists_tags_and_pulls_the_latest_by_digest() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    let reg = registry(
        &["v1.0.0", "v1.2.0", "v1.1.0", "latest"],
        &[("v1.2.0", DIGEST)],
    );
    let peer = launcher_with(
        &m,
        &["tool"],
        false,
        vec![format!("{ONLINE_PATH}@{DIGEST}")],
    );

    let (code, stdout, stderr) = run_with(
        &m,
        HOST_ROOT,
        "000",
        &["add", "tool", "--image-path", ONLINE_PATH],
        reg.base(),
    );
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
Added tool v1.2.0 (ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222).

"#]]
    );
    assert_data_eq!(stderr, "");
    assert_eq!(seen.requests, pulled());
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    let asked: Vec<String> = reg
        .requests()
        .into_iter()
        .filter(|r| !r.contains("/token"))
        .collect();
    assert!(
        asked.iter().any(|r| r.contains("/tags/list"))
            && asked
                .iter()
                .any(|r| r == "HEAD /v2/acme/tool/manifests/v1.2.0"),
        "{asked:?}"
    );
    assert_added(&m);
}

#[test]
fn add_at_a_tag_not_in_the_local_store_pulls_it_by_digest_without_listing() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    let reg = registry(&["v1.2.0"], &[("v1.2.0", DIGEST)]);
    let peer = launcher_with(
        &m,
        &["tool"],
        false,
        vec![format!("{ONLINE_PATH}@{DIGEST}")],
    );

    let (code, stdout, stderr) = run_with(
        &m,
        HOST_ROOT,
        "000",
        &["add", "tool@v1.2.0", "--image-path", ONLINE_PATH],
        reg.base(),
    );
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert!(stdout.starts_with("Added tool v1.2.0 "), "{stdout}");
    assert_eq!(seen.requests, pulled());
    assert!(
        !reg.requests().iter().any(|r| r.contains("/tags/list")),
        "{:?}",
        reg.requests()
    );
    assert_added(&m);
}

#[test]
fn private_tool_is_listed_with_the_token_file() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    fs::write(m.root.join("ghcr.token"), format!("{GOOD_TOKEN}\n")).unwrap();
    let reg = Registry::start_with(
        &[("acme/tool", Repo::private(&["v1.2.0"]))],
        &[("acme/tool", "v1.2.0", DIGEST)],
    );
    let peer = launcher_with(
        &m,
        &["tool"],
        false,
        vec![format!("{ONLINE_PATH}@{DIGEST}")],
    );

    let (code, stdout, stderr) = run_with(
        &m,
        HOST_ROOT,
        "000",
        &[
            "add",
            "tool",
            "--image-path",
            ONLINE_PATH,
            "--registry-token-file",
            "ghcr.token",
        ],
        reg.base(),
    );
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert!(stdout.starts_with("Added tool v1.2.0 "), "{stdout}");
    assert_eq!(seen.requests, pulled());
    assert_added(&m);
}

#[test]
fn online_add_without_a_lock_line_needs_image_path() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    let before = vk_tree(&m);
    let peer = launcher(&m, &["tool"]);

    let (code, stdout, stderr) = run(&m, HOST_ROOT, "000", &["add", "tool"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0025]: Required argument is missing: --image-path.

"#]]
    );
    assert!(seen.requests.is_empty());
    assert_eq!(vk_tree(&m), before);
}

#[test]
fn invalid_image_path_is_a_usage_error() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    let before = vk_tree(&m);

    let (code, stdout, stderr) = run(
        &m,
        HOST_ROOT,
        "000",
        &["add", "tool", "--image-path", "ghcr.io/acme/tool:v1.2.0"],
    );

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with(
            "vendor_kit: error[VK0026]: Unknown, extra, or disallowed argument: ghcr.io/acme/tool:v1.2.0.\n"
        ),
        "{stderr}"
    );
    assert_eq!(vk_tree(&m), before);
}

#[test]
fn listing_a_private_tool_without_a_token_file_is_vk0001() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    let before = vk_tree(&m);
    let reg = Registry::start(&[("acme/tool", Repo::private(&["v1.2.0"]))]);
    let peer = launcher(&m, &["tool"]);

    let (code, stdout, stderr) = run_with(
        &m,
        HOST_ROOT,
        "000",
        &["add", "tool", "--image-path", ONLINE_PATH],
        reg.base(),
    );
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with("vendor_kit: error[VK0001]: Cannot list versions for tool: ")
            && stderr.contains("just vendor_kit add tool@<tag>"),
        "{stderr}"
    );
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(vk_tree(&m), before);
}

#[test]
fn same_tag_pointing_to_another_digest_is_rejected_before_any_write() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    let before = vk_tree(&m);
    let reg = registry(&["v1.2.0"], &[("v1.2.0", OTHER_DIGEST)]);
    let peer = launcher(&m, &["tool"]);

    let (code, stdout, stderr) = run_with(
        &m,
        HOST_ROOT,
        "000",
        &["add", "tool", "--image-path", ONLINE_PATH],
        reg.base(),
    );
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with(&format!(
            "vendor_kit: error[VK0056]: Internal vendor_kit error: {IMAGE} points to more than one digest ({DIGEST}, {OTHER_DIGEST}); reason code pending (draft VK0078, N53)."
        )),
        "{stderr}"
    );
    assert_eq!(seen.requests, [format!("inspect {IMAGE}")]);
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_eq!(vk_tree(&m), before);
}

#[test]
fn local_image_without_a_repo_digest_is_vk0031() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    let before = vk_tree(&m);
    let peer = launcher_with(&m, &["tool"], true, Vec::new());

    let (code, stdout, stderr) = run(
        &m,
        HOST_ROOT,
        "000",
        &["add", "tool@v1.2.0", "--image-path", ONLINE_PATH],
    );
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with(&format!(
            "vendor_kit: error[VK0031]: Cannot use image {IMAGE}: required digest information is missing. The supplied image was not used."
        )),
        "{stderr}"
    );
    assert_eq!(seen.requests, [format!("inspect {IMAGE}")]);
    assert_eq!(vk_tree(&m), before);
}

// ---- image tar（ADR-0009） ----

/// image tar 的 index digest（只在旁檔裡；載入的 image 沒有 RepoDigests）。
const TAR_DIGEST: &str = "sha256:6666666666666666666666666666666666666666666666666666666666666666";

/// image tar 的假啟動器：主機路徑 `e:/srv/proj/<x>` 對到安裝目錄的 `<x>`，`stage` 是檔就複製進 `in/<slot>`；
/// `load` 回 `Loaded image: <IMAGE>`；inspect 回 RepoTags 有 `IMAGE`、沒有 RepoDigests（classic image store
/// 載入 tar 的樣子）；extract 放進工具內容。
fn tar_launcher(m: &Mounts) -> std::thread::JoinHandle<Seen> {
    let (ctl, inbox, root) = (m.ctl.clone(), m.inbox.clone(), m.root.clone());
    launcher::serve(&m.ctl, HEADER, move |req: &Request| match req.op.as_str() {
        "stage" => {
            let src = req.args[0]
                .strip_prefix("e:/srv/proj/")
                .map(|rest| root.join(rest));
            let dest = inbox.join(&req.args[1]);
            match src {
                Some(src) if src.is_file() && !dest.exists() => {
                    fs::copy(&src, &dest).unwrap();
                    Reply::Ok
                }
                _ => Reply::Failed(1),
            }
        }
        "load" => {
            fs::write(
                ctl.join(format!("res.{}.out", req.seq)),
                format!("Loaded image: {IMAGE}\n"),
            )
            .unwrap();
            Reply::Ok
        }
        "inspect" => {
            fs::write(
                ctl.join(format!("res.{}.out", req.seq)),
                format!(
                    "[\n    {{\n        \"Id\": \"{IMAGE_ID}\",\n        \"RepoTags\": [\"{IMAGE}\"],\n        \"RepoDigests\": []\n    }}\n]\n"
                ),
            )
            .unwrap();
            Reply::Ok
        }
        "extract" if inbox.join(&req.args[1]).exists() => Reply::Failed(1),
        "extract" => {
            tool_content(&inbox.join(&req.args[1]), &["tool"]);
            Reply::Ok
        }
        _ => Reply::Failed(1),
    })
}

/// 安裝目錄裡的 `dist/tool.tar`，`digest` 有給就放同名旁檔 `dist/tool.digest`。
fn tar_files(m: &Mounts, digest: Option<&str>) {
    let dist = m.root.join("dist");
    fs::create_dir_all(&dist).unwrap();
    fs::write(dist.join("tool.tar"), "tar\n").unwrap();
    if let Some(d) = digest {
        fs::write(dist.join("tool.digest"), d).unwrap();
    }
}

#[test]
fn add_from_an_image_tar_pins_the_sidecar_digest() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    tar_files(&m, Some(&format!("{TAR_DIGEST}\n")));
    let peer = tar_launcher(&m);

    let (code, stdout, stderr) = run(
        &m,
        HOST_ROOT,
        "000",
        &["add", "tool", "-i", "dist/tool.tar"],
    );
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(
        stdout,
        format!("Added tool v1.2.0 ({IMAGE}@{TAR_DIGEST}).\n")
    );
    assert_data_eq!(stderr, "");
    assert_eq!(
        seen.requests,
        [
            "stage e:/srv/proj/dist/tool.digest digest".to_owned(),
            "load e:/srv/proj/dist/tool.tar".to_owned(),
            format!("inspect {IMAGE}"),
            format!("extract {IMAGE_ID} tool1"),
        ]
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    let lock = fs::read_to_string(m.root.join(".vendor_kit/version.toml")).unwrap();
    assert!(
        lock.ends_with(&format!("[tools]\ntool = \"{IMAGE}@{TAR_DIGEST}\"\n")),
        "{lock}"
    );
}

/// ADR-0009 驗收：拿掉旁檔跑 `add <repo> -i <image tar>`，結束碼 2，版本鎖定行不動、不載入。
#[test]
fn image_tar_without_its_digest_sidecar_exits_2_and_leaves_the_lock_alone() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m, "");
    tar_files(&m, None);
    let before = vk_tree(&m);
    let lock_before = fs::read_to_string(m.root.join(".vendor_kit/version.toml")).unwrap();
    let peer = tar_launcher(&m);

    let (code, stdout, stderr) = run(
        &m,
        HOST_ROOT,
        "000",
        &["add", "tool", "-i", "dist/tool.tar"],
    );
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with(
            "vendor_kit: error[VK0031]: Cannot use image dist/tool.tar: required digest information is missing. The supplied image was not used."
        ),
        "{stderr}"
    );
    assert_eq!(seen.requests, ["stage e:/srv/proj/dist/tool.digest digest"]);
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_eq!(vk_tree(&m), before);
    assert_eq!(
        fs::read_to_string(m.root.join(".vendor_kit/version.toml")).unwrap(),
        lock_before
    );
}
