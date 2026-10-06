//! `upgrade <repo>[@<tag>]`（04 指令表、成對與無害的工具升版流程、指定版本；03 輸出）：經假的啟動器跑。
//!
//! 每個測試在暫存目錄建好安裝目錄（工具 `tool` 已在 v1.0.0）與 session 的 `ctl/`、`in/`，以
//! [`MOUNT_PREFIX_ENV`] 讓引擎把它們當成 `/vk/root`、`/vk/ctl`、`/vk/in`；假啟動器在背景回 inspect、pull 與
//! extract。registry 一律以 [`REGISTRY_URL_ENV`] 接到假 registry（不需要 registry 的測試給連不到的位址），
//! 不連外網。
//!
//! 基準版合併、合併衝突（VK0021）、答否與不能互動都要工具交付初始檔，而 `init.toml` 的格式還沒定（見
//! engine/upgrade 的缺口），經執行檔做不出會詢問的工具，所以這幾種在 engine/upgrade 的單元測試裡驗；
//! 這裡驗工具交付 `init.toml` 時在任何寫入之前停下。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::{Path, PathBuf};

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply, Request, Seen};
use e2e::registry::{Registry, Repo};
use e2e::{MOUNT_PREFIX_ENV, REGISTRY_URL_ENV, vendor_kit_bin};
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
const OTHER_DIGEST: &str =
    "sha256:5555555555555555555555555555555555555555555555555555555555555555";
/// 不需要 registry 的執行：連不到的位址，連了就會失敗。
const NO_REGISTRY: &str = "http://127.0.0.1:9";

/// 安裝目錄：`version.toml` 有引擎與 `tool` v1.0.0、`cache/tool/` 是舊版內容、`gen/tools.just`、
/// 啟動器建好的空執行紀錄、根 `justfile`。
fn install(m: &Mounts) {
    let vk = m.root.join(".vendor_kit");
    fs::create_dir_all(vk.join("log")).unwrap();
    fs::write(
        vk.join("version.toml"),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"{OLD}\"\n"
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
    launcher_with(m, init, true, vec![format!("ghcr.io/acme/tool@{DIGEST}")])
}

/// 假啟動器：`local` 為假時本機沒有 `<路徑>:<tag>`（不帶 digest 的 inspect 回 failed 1，pull 之後以
/// `<路徑>@<digest>` inspect 照常回）；inspect 回的 RepoDigests 是 `digests`。
fn launcher_with(
    m: &Mounts,
    init: bool,
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
        "extract" if inbox.join(&req.args[1]).exists() => Reply::Failed(1),
        "extract" => {
            tool_content(&inbox.join(&req.args[1]), init);
            Reply::Ok
        }
        _ => Reply::Failed(1),
    })
}

/// 跑一次 `upgrade`，不需要 registry。
fn run(m: &Mounts, rest: &[&str]) -> (i32, String, String) {
    run_with(m, rest, NO_REGISTRY)
}

/// 跑一次 `upgrade`，registry 接到 `registry`（base URL）。
fn run_with(m: &Mounts, rest: &[&str], registry: &str) -> (i32, String, String) {
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

#[test]
fn upgrade_without_a_tag_lists_tags_and_pulls_the_latest_by_digest() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let reg = registry(
        &["v1.0.0", "v1.2.0", "v1.1.0", "latest"],
        &[("v1.2.0", DIGEST)],
    );
    let peer = launcher_with(
        &m,
        false,
        false,
        vec![format!("ghcr.io/acme/tool@{DIGEST}")],
    );

    let (code, stdout, stderr) = run_with(&m, &["upgrade", "tool"], reg.base());
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
Upgraded tool from v1.0.0 to v1.2.0 (ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222).

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
    assert_upgraded(&m);
}

#[test]
fn upgrade_to_a_tag_not_in_the_local_store_pulls_it_by_digest_without_listing() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let reg = registry(&["v1.2.0"], &[("v1.2.0", DIGEST)]);
    let peer = launcher_with(
        &m,
        false,
        false,
        vec![format!("ghcr.io/acme/tool@{DIGEST}")],
    );

    let (code, stdout, stderr) = run_with(&m, &["upgrade", "tool@v1.2.0"], reg.base());
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert!(
        stdout.starts_with("Upgraded tool from v1.0.0 to v1.2.0 "),
        "{stdout}"
    );
    assert_eq!(seen.requests, pulled());
    assert!(
        !reg.requests().iter().any(|r| r.contains("/tags/list")),
        "{:?}",
        reg.requests()
    );
    assert_upgraded(&m);
}

#[test]
fn same_tag_pointing_to_another_digest_is_rejected_before_any_write() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let before = snapshot(&m);
    let reg = registry(&["v1.2.0"], &[("v1.2.0", OTHER_DIGEST)]);
    let peer = launcher(&m, false);

    let (code, stdout, stderr) = run_with(&m, &["upgrade", "tool"], reg.base());
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
    assert_eq!(snapshot(&m), before);
}

#[test]
fn local_image_without_a_repo_digest_is_vk0031() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let before = snapshot(&m);
    let peer = launcher_with(&m, false, true, Vec::new());

    let (code, stdout, stderr) = run(&m, &["upgrade", "tool@v1.2.0"]);
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
    assert_eq!(snapshot(&m), before);
}

#[test]
fn listing_a_private_tool_without_a_token_file_is_vk0001() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let before = snapshot(&m);
    let reg = Registry::start(&[("acme/tool", Repo::private(&["v1.2.0"]))]);
    let peer = launcher(&m, false);

    let (code, stdout, stderr) = run_with(&m, &["upgrade", "tool"], reg.base());
    let seen = peer.join().unwrap();

    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with("vendor_kit: error[VK0001]: Cannot list versions for tool: "),
        "{stderr}"
    );
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(snapshot(&m), before);
}

/// `tool` 之外再裝 alpha、beta（版本鎖定行），兩者的 `cache/<repo>/` 都還沒放。
fn install_with_others(m: &Mounts) {
    install(m);
    fs::write(
        m.root.join(".vendor_kit/version.toml"),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nalpha = \"ghcr.io/acme/alpha:v1.0.0@{OTHER_DIGEST}\"\nbeta = \"ghcr.io/acme/beta:v1.0.0@{OTHER_DIGEST}\"\ntool = \"{OLD}\"\n"
        ),
    )
    .unwrap();
}

#[test]
fn other_tools_whose_cache_cannot_be_read_are_all_named_before_any_write() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install_with_others(&m);
    // alpha 還沒 sync；beta 的 cache 損壞（just/ 是一般檔），保留實際原因。
    fs::create_dir_all(m.root.join(".vendor_kit/cache/beta")).unwrap();
    fs::write(
        m.root.join(".vendor_kit/cache/beta/just"),
        "not a directory\n",
    )
    .unwrap();
    let before = snapshot(&m);
    let peer = launcher(&m, false);

    let (code, stdout, stderr) = run(&m, &["upgrade", "tool@v1.2.0"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2, "stderr: {stderr}");
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0056]: Internal vendor_kit error: the cache of installed tools is missing: .vendor_kit/cache/alpha/; run just vendor_kit sync first; reason code pending (draft VK0068, N4). This is a VK bug. Report it at https://github.com/ycpss91255-research/vendor_kit/issues and attach run log /srv/proj/.vendor_kit/log/r1.jsonl.
vendor_kit: error[VK0056]: Internal vendor_kit error: the cache of installed tool beta (.vendor_kit/cache/beta/) cannot be read: dist has no just/ directory; reason code pending (draft VK0073, N4). This is a VK bug. Report it at https://github.com/ycpss91255-research/vendor_kit/issues and attach run log /srv/proj/.vendor_kit/log/r1.jsonl.

"#]]
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_eq!(snapshot(&m), before);
    assert!(!events(&m).iter().any(|e| e == "writes_started"));
}

#[test]
fn an_unchanged_upgrade_does_not_read_other_tools() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install_with_others(&m);
    let before = snapshot(&m);
    let peer = launcher(&m, false);

    let (code, _stdout, stderr) = run(&m, &["upgrade", "tool@v1.0.0"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(stderr, "");
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(snapshot(&m), before);
}

// ---- 沿用既有原因代碼（#372 N79、N80、N84） ----

#[test]
fn a_tool_name_that_is_not_a_just_name_is_a_usage_error() {
    for arg in ["li.nt", "1tool@v1.2.0"] {
        let tmp = tempfile::tempdir().unwrap();
        let m = Mounts::create(tmp.path());
        install(&m);
        let before = snapshot(&m);
        let peer = launcher(&m, false);
        let (code, stdout, stderr) = run(&m, &["upgrade", arg]);
        let seen = peer.join().unwrap();
        assert_eq!(code, 2, "stderr: {stderr}");
        assert_data_eq!(stdout, "");
        assert!(
            stderr.starts_with(&format!(
                "vendor_kit: error[VK0026]: Unknown, extra, or disallowed argument: {arg}.\n"
            )),
            "{stderr}"
        );
        assert!(seen.requests.is_empty(), "{:?}", seen.requests);
        assert_eq!(snapshot(&m), before);
    }
}

#[test]
fn a_tool_not_in_the_lock_lines_is_vk0046() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let before = snapshot(&m);
    let peer = launcher(&m, false);

    let (code, stdout, stderr) = run(&m, &["upgrade", "ghost@v1.2.0"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2, "stderr: {stderr}");
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0046]: Tool ghost is not in the lock version lines. The requested operation did not complete.

"#]]
    );
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(snapshot(&m), before);
}

#[test]
fn a_new_version_colliding_with_another_tool_is_vk0030_before_any_write() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let vk = m.root.join(".vendor_kit");
    fs::write(
        vk.join("version.toml"),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nalpha = \"ghcr.io/acme/alpha:v1.0.0@{OTHER_DIGEST}\"\ntool = \"{OLD}\"\n"
        ),
    )
    .unwrap();
    // alpha 也交付 `tool`：新版的 `tool` 撞到它（舊版的 `tool` 是自己的，不算）。
    fs::create_dir_all(vk.join("cache/alpha/just")).unwrap();
    fs::write(vk.join("cache/alpha/just/alpha.just"), "a:\n").unwrap();
    fs::write(vk.join("cache/alpha/just/tool.just"), "a:\n").unwrap();
    let before = snapshot(&m);
    let peer = launcher(&m, false);

    let (code, stdout, stderr) = run(&m, &["upgrade", "tool@v1.2.0"]);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2, "stderr: {stderr}");
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0030]: Cannot add tool: namespace tool is already used by alpha.

"#]]
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_eq!(snapshot(&m), before);
    assert!(!events(&m).iter().any(|e| e == "writes_started"));
}
