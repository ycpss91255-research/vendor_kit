//! `dev <repo> -p <dir>`、`undev <repo>`（04 指令表、成對與無害、本機覆寫；03 輸出）：經假的啟動器跑。
//! 開著覆寫與解除之後的 `sync`（04 sync、本機覆寫），以及開著覆寫時的 `upgrade`、其他工具的 `add`、`remove`
//! （04 本機覆寫）也在這裡。
//!
//! 本機開發來源在安裝目錄裡時，`dev`、`undev` 不送 request，假啟動器只收 `done`；在安裝目錄外時，`dev`、
//! `sync`、`upgrade`、`add`、`remove` 送 `stage-dir`，假啟動器把對應的目錄複製進 `in/<slot>`（[`stage_launcher`]；
//! `upgrade` 另要取件，用 [`stage_add_launcher`]；`add` 另一個工具用 [`stage_other_launcher`]）。`undev` 的對象 `cache/`
//! 跟版本鎖定行對不上時，`undev` 送 `inspect`、`pull`、`extract` 取件（[`fetch_launcher`]）。`add` 那一段照
//! tests/add.rs 回 inspect 與 extract。`sync` 要判薄殼，所以安裝目錄放好跟這一版引擎一致的薄殼，模板從
//! fixture 目錄讀（[`e2e::shell`]）。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::{Path, PathBuf};

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply, Request, Seen};
use e2e::{MOUNT_PREFIX_ENV, VERSION, shell, vendor_kit_bin};
use snapbox::assert_data_eq;

const RUN_ID: &str = "r1";
const HEADER: &str = "vk-resolve/1 r1";
const HOST_ROOT: &str = "/srv/proj";
const RUN_LOG: &str = ".vendor_kit/log/r1.jsonl";
const ENGINE: &str = "ghcr.io/ycpss91255-research/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const IMAGE: &str = "ghcr.io/acme/tool:v1.2.0";
const DIGEST: &str = "sha256:2222222222222222222222222222222222222222222222222222222222222222";
const IMAGE_ID: &str = "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";

/// 出貨輸入的 fixture 目錄。
fn release_dir(m: &Mounts) -> PathBuf {
    m.prefix.join("release")
}

/// 只有引擎行與薄殼的安裝目錄。
fn install(m: &Mounts) {
    let vk = m.root.join(".vendor_kit");
    fs::create_dir_all(vk.join("log")).unwrap();
    shell::install(&m.root, VERSION).unwrap();
    shell::release(&release_dir(m)).unwrap();
    fs::write(
        vk.join("version.toml"),
        format!("vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n"),
    )
    .unwrap();
    fs::write(m.root.join(RUN_LOG), "").unwrap();
    fs::write(m.root.join("justfile"), "import '.vendor_kit/entry.just'\n").unwrap();
}

/// 工具 image 交付的內容。
fn tool_content(dir: &Path) {
    fs::create_dir_all(dir.join("just")).unwrap();
    fs::write(dir.join("just/tool.just"), "hello:\n    echo hi\n").unwrap();
}

/// 回 inspect 與 extract 的假啟動器（給 `add`）；其他 op 一律失敗。
fn add_launcher(m: &Mounts) -> std::thread::JoinHandle<Seen> {
    let (ctl, inbox) = (m.ctl.clone(), m.inbox.clone());
    launcher::serve(&m.ctl, HEADER, move |req: &Request| {
        add_reply(&ctl, &inbox, req)
    })
}

/// [`add_launcher`] 對一個 request 的回應。
fn add_reply(ctl: &Path, inbox: &Path, req: &Request) -> Reply {
    match req.op.as_str() {
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
    }
}

/// 開著覆寫時 `git pull` 換上的新版本與它的 digest。
const NEW_DIGEST: &str = "sha256:5555555555555555555555555555555555555555555555555555555555555555";

/// `undev` 取件用的假啟動器：本機沒有 image（第一次 inspect 失敗），pull 之後 inspect 回 `NEW_DIGEST`，
/// extract 放新版的內容；其他 op 一律失敗。
fn fetch_launcher(m: &Mounts) -> std::thread::JoinHandle<Seen> {
    let (ctl, inbox) = (m.ctl.clone(), m.inbox.clone());
    let mut pulled = false;
    launcher::serve(&m.ctl, HEADER, move |req: &Request| match req.op.as_str() {
        "inspect" if pulled => {
            let digests = [format!("ghcr.io/acme/tool@{NEW_DIGEST}")];
            let digests: Vec<&str> = digests.iter().map(String::as_str).collect();
            fs::write(
                ctl.join(format!("res.{}.out", req.seq)),
                launcher::inspect_json(IMAGE_ID, &digests),
            )
            .unwrap();
            Reply::Ok
        }
        "pull" => {
            pulled = true;
            Reply::Ok
        }
        "extract" => {
            let dir = inbox.join(&req.args[1]);
            fs::create_dir_all(dir.join("just")).unwrap();
            fs::write(dir.join("just/tool.just"), "hello:\n    echo new\n").unwrap();
            Reply::Ok
        }
        _ => Reply::Failed(1),
    })
}

/// 什麼 op 都回失敗的假啟動器：`dev`、`undev` 不該送任何 request。
fn idle_launcher(m: &Mounts) -> std::thread::JoinHandle<Seen> {
    launcher::serve(&m.ctl, HEADER, |_: &Request| Reply::Failed(1))
}

fn copy_dir(from: &Path, to: &Path) {
    fs::create_dir(to).unwrap();
    for entry in fs::read_dir(from).unwrap() {
        let entry = entry.unwrap();
        let target = to.join(entry.file_name());
        if entry.file_type().unwrap().is_dir() {
            copy_dir(&entry.path(), &target);
        } else {
            fs::copy(entry.path(), target).unwrap();
        }
    }
}

/// 回 `stage-dir` 的假啟動器：主機路徑 `/srv/<x>` 對到 `host/<x>`，是目錄就複製進 `in/<slot>`
/// （launcher/launch.sh 的 vk_launch_stage_dir），否則回 failed 1；其他 op 一律失敗。
fn stage_launcher(m: &Mounts, host: &Path) -> std::thread::JoinHandle<Seen> {
    let (inbox, host) = (m.inbox.clone(), host.to_path_buf());
    launcher::serve(&m.ctl, HEADER, move |req: &Request| {
        stage_reply(&inbox, &host, req)
    })
}

/// [`stage_launcher`] 對一個 request 的回應。
fn stage_reply(inbox: &Path, host: &Path, req: &Request) -> Reply {
    let src = req.args[0]
        .strip_prefix("e:/srv/")
        .map(|rest| host.join(rest));
    let dest = inbox.join(&req.args[1]);
    match src {
        Some(src) if req.op == "stage-dir" && src.is_dir() && !dest.exists() => {
            copy_dir(&src, &dest);
            Reply::Ok
        }
        _ => Reply::Failed(1),
    }
}

/// `stage-dir` 照 [`stage_launcher`]，inspect 與 extract 照 [`add_launcher`]（給開著安裝目錄外覆寫的
/// `upgrade`）。
fn stage_add_launcher(m: &Mounts, host: &Path) -> std::thread::JoinHandle<Seen> {
    let (ctl, inbox, host) = (m.ctl.clone(), m.inbox.clone(), host.to_path_buf());
    launcher::serve(&m.ctl, HEADER, move |req: &Request| {
        if req.op == "stage-dir" {
            stage_reply(&inbox, &host, req)
        } else {
            add_reply(&ctl, &inbox, req)
        }
    })
}

/// 另一個工具 `other` 的 image 與 digest（開著 `tool` 的覆寫時 `add other`、`remove other`）。
const OTHER_IMAGE: &str = "ghcr.io/acme/other:v1.0.0";
const OTHER_DIGEST: &str =
    "sha256:6666666666666666666666666666666666666666666666666666666666666666";

/// `stage-dir` 照 [`stage_launcher`]；inspect 回 `other` 的 RepoDigests，extract 放 `other` 的內容。
fn stage_other_launcher(m: &Mounts, host: &Path) -> std::thread::JoinHandle<Seen> {
    let (ctl, inbox, host) = (m.ctl.clone(), m.inbox.clone(), host.to_path_buf());
    launcher::serve(&m.ctl, HEADER, move |req: &Request| match req.op.as_str() {
        "stage-dir" => stage_reply(&inbox, &host, req),
        "inspect" => {
            let digests = [format!("ghcr.io/acme/other@{OTHER_DIGEST}")];
            let digests: Vec<&str> = digests.iter().map(String::as_str).collect();
            fs::write(
                ctl.join(format!("res.{}.out", req.seq)),
                launcher::inspect_json(IMAGE_ID, &digests),
            )
            .unwrap();
            Reply::Ok
        }
        "extract" => {
            let dir = inbox.join(&req.args[1]).join("just");
            fs::create_dir_all(&dir).unwrap();
            fs::write(dir.join("other.just"), "hi:\n    echo other\n").unwrap();
            Reply::Ok
        }
        _ => Reply::Failed(1),
    })
}

/// 經 [`stage_launcher`] 跑一次，回傳結果與看到的 request。
fn run_staged(m: &Mounts, host: &Path, rest: &[&str]) -> ((i32, String, String), Vec<String>) {
    new_session(m);
    let peer = stage_launcher(m, host);
    let out = run(m, rest);
    let seen = peer.join().unwrap();
    assert_eq!(
        seen.done.as_deref(),
        Some(format!("vk-resolve/1 r1 done {}\n", out.0).as_str())
    );
    (out, seen.requests)
}

/// 每次執行的 session 目錄與執行紀錄是新的。
fn new_session(m: &Mounts) {
    for d in [&m.ctl, &m.inbox] {
        fs::remove_dir_all(d).unwrap();
        fs::create_dir_all(d).unwrap();
    }
    fs::write(m.root.join(RUN_LOG), "").unwrap();
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
        .env(shell::RELEASE_DIR_ENV, release_dir(m))
        .output()
        .unwrap();
    (
        out.status.code().unwrap(),
        String::from_utf8(out.stdout).unwrap(),
        String::from_utf8(out.stderr).unwrap(),
    )
}

/// 經 idle 假啟動器跑一次，確認沒有 request、`done` 帶同一個結束碼。
fn run_idle(m: &Mounts, rest: &[&str]) -> (i32, String, String) {
    new_session(m);
    let peer = idle_launcher(m);
    let out = run(m, rest);
    let seen = peer.join().unwrap();
    assert!(seen.requests.is_empty(), "{rest:?}");
    assert_eq!(
        seen.done.as_deref(),
        Some(format!("vk-resolve/1 r1 done {}\n", out.0).as_str())
    );
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

/// `.vendor_kit/` 下每個檔的路徑與內容（不含執行紀錄與鎖檔）。
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

/// `.vendor_kit/` 下 `cache/`、`gen/`、`version.toml` 的檔與內容：`undev` 之後要回到 `add` 之後的樣子。
fn locked_state(m: &Mounts) -> Vec<(PathBuf, Vec<u8>)> {
    let vk = m.root.join(".vendor_kit");
    snapshot(m)
        .into_iter()
        .filter(|(p, _)| {
            p.starts_with(vk.join("cache"))
                || p.starts_with(vk.join("gen"))
                || *p == vk.join("version.toml")
        })
        .collect()
}

const LANDED_EVENTS: [&str; 4] = [
    "engine_started",
    "writes_started",
    "progress_removed",
    "engine_finished",
];

/// `sync` 落地時的事件：唯讀 recipe 不建進度檔，所以沒有 `progress_removed`。
const SYNC_LANDED_EVENTS: [&str; 3] = ["engine_started", "writes_started", "engine_finished"];

#[test]
fn add_then_dev_uses_the_local_source_and_undev_returns_to_the_locked_version() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let vk = m.root.join(".vendor_kit");

    let peer = add_launcher(&m);
    let (code, _, stderr) = run(&m, &["add", "tool", "-i", IMAGE]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    let after_add = locked_state(&m);
    assert_eq!(
        fs::read_to_string(vk.join("gen/tools.just")).unwrap(),
        "mod? tool '../cache/tool/just/tool.just'\n"
    );

    // 本機開發來源：安裝目錄裡的 work/tool/，另多交付一個 <ns>。
    let src = m.root.join("work/tool/just");
    fs::create_dir_all(&src).unwrap();
    fs::write(src.join("tool.just"), "hello:\n    echo local\n").unwrap();
    fs::write(src.join("tool-extra.just"), "extra:\n    echo extra\n").unwrap();

    let (code, stdout, stderr) = run_idle(&m, &["dev", "tool", "-p", "./work/tool"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
tool now uses the local source work/tool (local override).
Updated .vendor_kit/gen/tools.just.

"#]]
    );
    assert_data_eq!(stderr, "");
    assert_eq!(
        fs::read_to_string(vk.join("gen/tools.just")).unwrap(),
        "mod? tool '../../work/tool/just/tool.just'\n\
         mod? tool-extra '../../work/tool/just/tool-extra.just'\n"
    );
    let local = fs::read_to_string(vk.join("version.local.toml")).unwrap();
    assert!(local.contains("[tools]\ntool = \"work/tool\"\n"), "{local}");
    assert_eq!(events(&m), LANDED_EVENTS);
    // 開著覆寫時 cache/ 與版本鎖定行不動，只有入口檔改指本機目錄。
    let vk_gen = vk.join("gen");
    let unchanged: Vec<_> = after_add
        .iter()
        .filter(|(p, _)| !p.starts_with(&vk_gen))
        .cloned()
        .collect();
    let now: Vec<_> = locked_state(&m)
        .into_iter()
        .filter(|(p, _)| !p.starts_with(&vk_gen))
        .collect();
    assert_eq!(now, unchanged);

    // 再 dev 同來源：未變更。
    let before = snapshot(&m);
    let (code, stdout, _) = run_idle(&m, &["dev", "tool", "-p", "work/tool"]);
    assert_eq!(code, 0);
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
tool already uses the local source work/tool. No changes were made.

"#]]
    );
    assert_eq!(snapshot(&m), before);
    assert_eq!(events(&m), ["engine_started", "engine_finished"]);

    // 不同來源：VK0050，不取代。
    let (code, stdout, stderr) = run_idle(&m, &["dev", "tool", "-p", "other"]);
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0050]: A different local override is already active for tool. Run first: just vendor_kit undev tool

"#]]
    );
    assert_eq!(snapshot(&m), before);

    // undev：回到鎖定版本，cache/、印記、入口檔、版本鎖定行都跟 add 之後逐位元組相同。
    let (code, stdout, stderr) = run_idle(&m, &["undev", "tool"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
Removed the local override of tool; tool uses v1.2.0 (ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222).
Updated .vendor_kit/gen/tools.just.

"#]]
    );
    assert_data_eq!(stderr, "");
    assert_eq!(locked_state(&m), after_add);
    let local = fs::read_to_string(vk.join("version.local.toml")).unwrap();
    assert!(!local.contains("tool ="), "{local}");
    assert_eq!(events(&m), LANDED_EVENTS);
    // 本機開發來源不動。
    assert_eq!(
        fs::read_to_string(src.join("tool.just")).unwrap(),
        "hello:\n    echo local\n"
    );

    // 再 undev：沒有覆寫，未變更。
    let before = snapshot(&m);
    let (code, stdout, _) = run_idle(&m, &["undev", "tool"]);
    assert_eq!(code, 0);
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
tool has no local override. No changes were made.

"#]]
    );
    assert_eq!(snapshot(&m), before);
}

#[test]
fn undev_after_the_lock_line_changed_fetches_the_locked_version() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let vk = m.root.join(".vendor_kit");

    let peer = add_launcher(&m);
    let (code, _, stderr) = run(&m, &["add", "tool", "-i", IMAGE]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    let src = m.root.join("work/tool/just");
    fs::create_dir_all(&src).unwrap();
    fs::write(src.join("tool.just"), "hello:\n    echo local\n").unwrap();
    let (code, _, stderr) = run_idle(&m, &["dev", "tool", "-p", "work/tool"]);
    assert_eq!(code, 0, "stderr: {stderr}");

    // 開著覆寫時 git pull 換了版本鎖定行：cache/ 與印記還是舊版。
    let lock_path = vk.join("version.toml");
    let lock = fs::read_to_string(&lock_path).unwrap();
    let old_line = format!("tool = \"{IMAGE}@{DIGEST}\"\n");
    let new_ref = format!("ghcr.io/acme/tool:v1.3.0@{NEW_DIGEST}");
    assert!(lock.contains(&old_line), "{lock}");
    let lock = lock.replace(&old_line, &format!("tool = \"{new_ref}\"\n"));
    fs::write(&lock_path, &lock).unwrap();

    // undev：解除覆寫，不叫使用者先 sync，依鎖定行取件、換 cache/、指回去。
    new_session(&m);
    let peer = fetch_launcher(&m);
    let (code, stdout, stderr) = run(&m, &["undev", "tool"]);
    let seen = peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(stderr, "");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
Removed the local override of tool; tool uses v1.3.0 (ghcr.io/acme/tool:v1.3.0@sha256:5555555555555555555555555555555555555555555555555555555555555555).
Fetched tool v1.3.0 (ghcr.io/acme/tool:v1.3.0@sha256:5555555555555555555555555555555555555555555555555555555555555555).
Updated .vendor_kit/gen/tools.just.

"#]]
    );
    let pinned = format!("ghcr.io/acme/tool@{NEW_DIGEST}");
    assert_eq!(
        seen.requests,
        [
            format!("inspect {pinned}"),
            format!("pull {pinned}"),
            format!("inspect {pinned}"),
            format!("extract {IMAGE_ID} tool1"),
        ]
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert_eq!(events(&m), LANDED_EVENTS);
    assert_eq!(
        fs::read_to_string(vk.join("cache/tool/just/tool.just")).unwrap(),
        "hello:\n    echo new\n"
    );
    let stamp = fs::read_to_string(vk.join("cache/tool.stamp.toml")).unwrap();
    assert!(stamp.contains(&new_ref), "{stamp}");
    assert_eq!(
        fs::read_to_string(vk.join("gen/tools.just")).unwrap(),
        "mod? tool '../cache/tool/just/tool.just'\n"
    );
    let local = fs::read_to_string(vk.join("version.local.toml")).unwrap();
    assert!(!local.contains("tool ="), "{local}");
    // 版本鎖定行不動，本機開發來源不動。
    assert_eq!(fs::read_to_string(&lock_path).unwrap(), lock);
    assert_eq!(
        fs::read_to_string(src.join("tool.just")).unwrap(),
        "hello:\n    echo local\n"
    );
}

#[test]
fn dev_outside_the_install_directory_stages_the_source_through_the_launcher() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let vk = m.root.join(".vendor_kit");

    let peer = add_launcher(&m);
    let (code, _, stderr) = run(&m, &["add", "tool", "-i", IMAGE]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    let after_add = locked_state(&m);

    // 主機上安裝目錄（/srv/proj）旁邊的 /srv/elsewhere/tool；引擎容器看不到，經 stage-dir 取進來驗。
    let host = tmp.path().join("host");
    fs::create_dir_all(host.join("proj")).unwrap();
    let src = host.join("elsewhere/tool/just");
    fs::create_dir_all(&src).unwrap();
    fs::write(src.join("tool.just"), "hello:\n    echo outside\n").unwrap();

    // 絕對路徑：入口檔寫絕對路徑。
    let ((code, stdout, stderr), requests) =
        run_staged(&m, &host, &["dev", "tool", "-p", "/srv/elsewhere/tool/"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(requests, ["stage-dir e:/srv/elsewhere/tool dev1"]);
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
tool now uses the local source /srv/elsewhere/tool (local override).
Updated .vendor_kit/gen/tools.just.

"#]]
    );
    assert_data_eq!(stderr, "");
    assert_eq!(
        fs::read_to_string(vk.join("gen/tools.just")).unwrap(),
        "mod? tool '/srv/elsewhere/tool/just/tool.just'\n"
    );
    let local = fs::read_to_string(vk.join("version.local.toml")).unwrap();
    assert!(
        local.contains("[tools]\ntool = \"/srv/elsewhere/tool\"\n"),
        "{local}"
    );
    assert_eq!(events(&m), LANDED_EVENTS);

    // undev 不讀本機開發來源，不送 request；回到 add 之後的樣子。
    let (code, _, stderr) = run_idle(&m, &["undev", "tool"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(locked_state(&m), after_add);

    // 以 `..` 跑出安裝目錄的相對路徑：入口檔留相對路徑，主機路徑接在 --host-root 後面。
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let vk = m.root.join(".vendor_kit");
    let peer = add_launcher(&m);
    let (code, _, stderr) = run(&m, &["add", "tool", "-i", IMAGE]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    let ((code, _, stderr), requests) =
        run_staged(&m, &host, &["dev", "tool", "-p", "../elsewhere/tool"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(requests, ["stage-dir e:/srv/proj/../elsewhere/tool dev1"]);
    assert_eq!(
        fs::read_to_string(vk.join("gen/tools.just")).unwrap(),
        "mod? tool '../../../elsewhere/tool/just/tool.just'\n"
    );

    // 啟動器複製不了（不存在）：VK0051，什麼都不寫。
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let peer = add_launcher(&m);
    let (code, _, stderr) = run(&m, &["add", "tool", "-i", IMAGE]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    let before = snapshot(&m);
    let ((code, stdout, stderr), requests) =
        run_staged(&m, &host, &["dev", "tool", "-p", "/srv/nowhere"]);
    assert_eq!(code, 2);
    assert_eq!(requests, ["stage-dir e:/srv/nowhere dev1"]);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0051]: Cannot use local source /srv/nowhere for tool: the launcher could not copy it (exit 1): it does not exist, is not a directory, or cannot be read. The local override was not enabled.

"#]]
    );
    assert_eq!(snapshot(&m), before);
}

#[test]
fn sync_uses_the_local_source_during_dev_and_the_locked_version_after_undev() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let vk = m.root.join(".vendor_kit");
    let entry = vk.join("gen/tools.just");

    let peer = add_launcher(&m);
    let (code, _, stderr) = run(&m, &["add", "tool", "-i", IMAGE]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    let after_add = locked_state(&m);

    let src = m.root.join("work/tool/just");
    fs::create_dir_all(&src).unwrap();
    fs::write(src.join("tool.just"), "hello:\n    echo local\n").unwrap();
    let (code, _, stderr) = run_idle(&m, &["dev", "tool", "-p", "work/tool"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    let local_entry = "mod? tool '../../work/tool/just/tool.just'\n";
    assert_eq!(fs::read_to_string(&entry).unwrap(), local_entry);

    // 開著覆寫時 sync 重產入口檔：指向本機開發來源，不取件（沒有 request），cache/、印記、版本鎖定行不動。
    fs::remove_file(&entry).unwrap();
    let (code, stdout, stderr) = run_idle(&m, &["sync"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
tool uses the local source work/tool (local override).
Updated .vendor_kit/gen/tools.just.

"#]]
    );
    assert_data_eq!(stderr, "");
    assert_eq!(fs::read_to_string(&entry).unwrap(), local_entry);
    assert_eq!(events(&m), SYNC_LANDED_EVENTS);
    let vk_gen = vk.join("gen");
    let without_gen = |state: Vec<(PathBuf, Vec<u8>)>| -> Vec<(PathBuf, Vec<u8>)> {
        state
            .into_iter()
            .filter(|(p, _)| !p.starts_with(&vk_gen))
            .collect()
    };
    assert_eq!(
        without_gen(locked_state(&m)),
        without_gen(after_add.clone())
    );

    // 再 sync：沒有變更，照樣報告用了哪個覆寫。
    let before = snapshot(&m);
    let (code, stdout, _) = run_idle(&m, &["sync"]);
    assert_eq!(code, 0);
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
tool uses the local source work/tool (local override).

"#]]
    );
    assert_eq!(snapshot(&m), before);
    assert_eq!(events(&m), ["engine_started", "engine_finished"]);

    // undev 之後 sync：回到鎖定版本，什麼都不改、不印。
    let (code, _, stderr) = run_idle(&m, &["undev", "tool"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    let (code, stdout, stderr) = run_idle(&m, &["sync"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(stdout, "");
    assert_data_eq!(stderr, "");
    assert_eq!(locked_state(&m), after_add);
    assert_eq!(
        fs::read_to_string(&entry).unwrap(),
        "mod? tool '../cache/tool/just/tool.just'\n"
    );
    assert_eq!(events(&m), ["engine_started", "engine_finished"]);
}

#[test]
fn upgrade_during_dev_swaps_the_locked_version_and_keeps_the_override() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let vk = m.root.join(".vendor_kit");
    let entry = vk.join("gen/tools.just");

    let peer = add_launcher(&m);
    let (code, _, stderr) = run(&m, &["add", "tool", "-i", IMAGE]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");

    let src = m.root.join("work/tool/just");
    fs::create_dir_all(&src).unwrap();
    fs::write(src.join("tool.just"), "hello:\n    echo local\n").unwrap();
    let (code, _, stderr) = run_idle(&m, &["dev", "tool", "-p", "work/tool"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    let local_toml = fs::read(vk.join("version.local.toml")).unwrap();
    let local_entry = "mod? tool '../../work/tool/just/tool.just'\n";
    assert_eq!(fs::read_to_string(&entry).unwrap(), local_entry);

    // 開著覆寫時 upgrade 照常換鎖定行、cache/、印記，入口檔仍指本機開發來源，stdout 先報告覆寫。
    new_session(&m);
    let peer = add_launcher(&m);
    let (code, stdout, stderr) = run(&m, &["upgrade", "tool@v1.3.0"]);
    let seen = peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
tool uses the local source work/tool (local override).
Upgraded tool from v1.2.0 to v1.3.0 (ghcr.io/acme/tool:v1.3.0@sha256:2222222222222222222222222222222222222222222222222222222222222222).

"#]]
    );
    assert_data_eq!(stderr, "");
    assert_eq!(
        seen.requests,
        [
            "inspect ghcr.io/acme/tool:v1.3.0".to_owned(),
            format!("extract {IMAGE_ID} tool1"),
        ]
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    let lock = fs::read_to_string(vk.join("version.toml")).unwrap();
    assert!(
        lock.ends_with(&format!("tool = \"ghcr.io/acme/tool:v1.3.0@{DIGEST}\"\n")),
        "{lock}"
    );
    let stamp = fs::read_to_string(vk.join("cache/tool.stamp.toml")).unwrap();
    assert!(stamp.contains("ghcr.io/acme/tool:v1.3.0@"), "{stamp}");
    assert_eq!(fs::read(vk.join("version.local.toml")).unwrap(), local_toml);
    assert_eq!(fs::read_to_string(&entry).unwrap(), local_entry);

    // undev 之後回到換好的新版。
    let (code, stdout, stderr) = run_idle(&m, &["undev", "tool"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert!(stdout.contains("tool uses v1.3.0 "), "{stdout}");
    assert_eq!(
        fs::read_to_string(&entry).unwrap(),
        "mod? tool '../cache/tool/just/tool.just'\n"
    );
    let local = fs::read_to_string(vk.join("version.local.toml")).unwrap();
    assert!(!local.contains("tool ="), "{local}");
}

#[test]
fn sync_and_upgrade_stage_an_outside_local_source_through_the_launcher() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let vk = m.root.join(".vendor_kit");
    let entry = vk.join("gen/tools.just");

    let peer = add_launcher(&m);
    let (code, _, stderr) = run(&m, &["add", "tool", "-i", IMAGE]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    let after_add = locked_state(&m);

    // 主機上安裝目錄（/srv/proj）外的 /srv/elsewhere/tool。
    let host = tmp.path().join("host");
    fs::create_dir_all(host.join("proj")).unwrap();
    let src = host.join("elsewhere/tool/just");
    fs::create_dir_all(&src).unwrap();
    fs::write(src.join("tool.just"), "hello:\n    echo outside\n").unwrap();
    let ((code, _, stderr), _) =
        run_staged(&m, &host, &["dev", "tool", "-p", "/srv/elsewhere/tool"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    let local_entry = "mod? tool '/srv/elsewhere/tool/just/tool.just'\n";
    assert_eq!(fs::read_to_string(&entry).unwrap(), local_entry);

    // sync 經 stage-dir 讀覆寫、重產入口檔；只複製進 session 目錄，cache/、印記、版本鎖定行不動。
    fs::remove_file(&entry).unwrap();
    let ((code, stdout, stderr), requests) = run_staged(&m, &host, &["sync"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(requests, ["stage-dir e:/srv/elsewhere/tool dev1"]);
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
tool uses the local source /srv/elsewhere/tool (local override).
Updated .vendor_kit/gen/tools.just.

"#]]
    );
    assert_data_eq!(stderr, "");
    assert_eq!(fs::read_to_string(&entry).unwrap(), local_entry);
    assert_eq!(events(&m), SYNC_LANDED_EVENTS);
    let vk_gen = vk.join("gen");
    let without_gen = |state: Vec<(PathBuf, Vec<u8>)>| -> Vec<(PathBuf, Vec<u8>)> {
        state
            .into_iter()
            .filter(|(p, _)| !p.starts_with(&vk_gen))
            .collect()
    };
    assert_eq!(
        without_gen(locked_state(&m)),
        without_gen(after_add.clone())
    );

    // 再 sync：照樣經 stage-dir 讀，沒有變更就什麼都不寫。
    let before = snapshot(&m);
    let ((code, stdout, _), requests) = run_staged(&m, &host, &["sync"]);
    assert_eq!(code, 0);
    assert_eq!(requests, ["stage-dir e:/srv/elsewhere/tool dev1"]);
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
tool uses the local source /srv/elsewhere/tool (local override).

"#]]
    );
    assert_eq!(snapshot(&m), before);

    // 主機上的來源不見了：sync 照讀不到回 VK0052，什麼都不寫。
    fs::remove_dir_all(host.join("elsewhere")).unwrap();
    let ((code, stdout, stderr), requests) = run_staged(&m, &host, &["sync"]);
    assert_eq!(code, 2);
    assert_eq!(requests, ["stage-dir e:/srv/elsewhere/tool dev1"]);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0052]: Cannot read the local override source /srv/elsewhere/tool for tool: the launcher could not copy it (exit 1): it does not exist, is not a directory, or cannot be read. Run: just vendor_kit undev tool

"#]]
    );
    assert_eq!(snapshot(&m), before);

    // upgrade 先經 stage-dir 讀覆寫，再照常取件換版；入口檔仍指主機上的本機開發來源。
    fs::create_dir_all(&src).unwrap();
    fs::write(src.join("tool.just"), "hello:\n    echo outside\n").unwrap();
    new_session(&m);
    let peer = stage_add_launcher(&m, &host);
    let (code, stdout, stderr) = run(&m, &["upgrade", "tool@v1.3.0"]);
    let seen = peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(
        seen.requests,
        [
            "stage-dir e:/srv/elsewhere/tool dev1".to_owned(),
            "inspect ghcr.io/acme/tool:v1.3.0".to_owned(),
            format!("extract {IMAGE_ID} tool1"),
        ]
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
tool uses the local source /srv/elsewhere/tool (local override).
Upgraded tool from v1.2.0 to v1.3.0 (ghcr.io/acme/tool:v1.3.0@sha256:2222222222222222222222222222222222222222222222222222222222222222).

"#]]
    );
    assert_data_eq!(stderr, "");
    let lock = fs::read_to_string(vk.join("version.toml")).unwrap();
    assert!(
        lock.ends_with(&format!("tool = \"ghcr.io/acme/tool:v1.3.0@{DIGEST}\"\n")),
        "{lock}"
    );
    assert_eq!(fs::read_to_string(&entry).unwrap(), local_entry);
}

#[test]
fn add_and_remove_of_another_tool_keep_and_report_an_outside_override() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let entry = m.root.join(".vendor_kit/gen/tools.just");

    let peer = add_launcher(&m);
    let (code, _, stderr) = run(&m, &["add", "tool", "-i", IMAGE]);
    peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");

    // 主機上安裝目錄（/srv/proj）外的 /srv/elsewhere/tool。
    let host = tmp.path().join("host");
    fs::create_dir_all(host.join("proj")).unwrap();
    let src = host.join("elsewhere/tool/just");
    fs::create_dir_all(&src).unwrap();
    fs::write(src.join("tool.just"), "hello:\n    echo outside\n").unwrap();
    let ((code, _, stderr), _) =
        run_staged(&m, &host, &["dev", "tool", "-p", "/srv/elsewhere/tool"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    let local_entry = "mod? tool '/srv/elsewhere/tool/just/tool.just'\n";
    assert_eq!(fs::read_to_string(&entry).unwrap(), local_entry);
    let report = "tool uses the local source /srv/elsewhere/tool (local override).\n";
    let other_locked = format!("{OTHER_IMAGE}@{OTHER_DIGEST}");

    // add other：先經 stage-dir 讀 tool 的覆寫，重產的入口檔裡 tool 仍指主機上的本機開發來源。
    new_session(&m);
    let peer = stage_other_launcher(&m, &host);
    let (code, stdout, stderr) = run(&m, &["add", "other", "-i", OTHER_IMAGE]);
    let seen = peer.join().unwrap();
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(
        seen.requests,
        [
            "stage-dir e:/srv/elsewhere/tool dev1".to_owned(),
            format!("inspect {OTHER_IMAGE}"),
            format!("extract {IMAGE_ID} tool1"),
        ]
    );
    assert_eq!(
        stdout,
        format!("{report}Added other v1.0.0 ({other_locked}).\n")
    );
    assert_data_eq!(stderr, "");
    assert_eq!(
        fs::read_to_string(&entry).unwrap(),
        format!("mod? other '../cache/other/just/other.just'\n{local_entry}")
    );

    // 主機上的來源不見了：remove other 要重產入口檔、讀不到 tool 的覆寫，回 VK0052，什麼都不寫。
    fs::remove_dir_all(host.join("elsewhere")).unwrap();
    let before = snapshot(&m);
    let ((code, stdout, stderr), requests) = run_staged(&m, &host, &["remove", "other"]);
    assert_eq!(code, 2);
    assert_eq!(requests, ["stage-dir e:/srv/elsewhere/tool dev1"]);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0052]: Cannot read the local override source /srv/elsewhere/tool for tool: the launcher could not copy it (exit 1): it does not exist, is not a directory, or cannot be read. Run: just vendor_kit undev tool

"#]]
    );
    assert_eq!(snapshot(&m), before);

    // 來源回來：remove other 照常收回，入口檔留下 tool 指本機開發來源的那一行。
    fs::create_dir_all(&src).unwrap();
    fs::write(src.join("tool.just"), "hello:\n    echo outside\n").unwrap();
    let ((code, stdout, stderr), requests) = run_staged(&m, &host, &["remove", "other"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(requests, ["stage-dir e:/srv/elsewhere/tool dev1"]);
    assert_eq!(
        stdout,
        format!("{report}Removed other v1.0.0 ({other_locked}).\n")
    );
    assert_eq!(fs::read_to_string(&entry).unwrap(), local_entry);

    // 來源又不見了：add other 在任何 docker 動作之前回 VK0052。
    fs::remove_dir_all(host.join("elsewhere")).unwrap();
    let before = snapshot(&m);
    new_session(&m);
    let peer = stage_other_launcher(&m, &host);
    let (code, stdout, stderr) = run(&m, &["add", "other", "-i", OTHER_IMAGE]);
    let seen = peer.join().unwrap();
    assert_eq!(code, 2);
    assert_eq!(seen.requests, ["stage-dir e:/srv/elsewhere/tool dev1"]);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with("vendor_kit: error[VK0052]: "),
        "{stderr}"
    );
    assert_eq!(snapshot(&m), before);
}

#[test]
fn tools_that_were_never_added_report_their_reason_codes() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    fs::create_dir_all(m.root.join("work/tool/just")).unwrap();
    fs::write(m.root.join("work/tool/just/tool.just"), "").unwrap();
    let before = snapshot(&m);

    let (code, stdout, stderr) = run_idle(&m, &["undev", "tool"]);
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0046]: Tool tool is not in the lock version lines. The requested operation did not complete.

"#]]
    );
    assert_eq!(snapshot(&m), before);
    assert_eq!(
        events(&m),
        ["engine_started", "diagnostic_emitted", "engine_finished"]
    );

    // dev 未導入的工具：訊息表沒有代碼（VK0046 只寫 remove、undev、update），以 VK0056 停下。
    let (code, stdout, stderr) = run_idle(&m, &["dev", "tool", "-p", "work/tool"]);
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with("vendor_kit: error[VK0056]: Internal vendor_kit error: dev for tool, which is not in the lock version lines"),
        "{stderr}"
    );
    assert_eq!(snapshot(&m), before);
}

#[test]
fn dev_names_every_other_tool_whose_cache_cannot_be_read_before_any_write() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let vk = m.root.join(".vendor_kit");
    // 全新 checkout：alpha、gamma 還沒 sync；beta 的 cache 損壞（just/ 是一般檔）。
    fs::write(
        vk.join("version.toml"),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nalpha = \"ghcr.io/acme/alpha:v1.0.0@{DIGEST}\"\nbeta = \"ghcr.io/acme/beta:v1.0.0@{DIGEST}\"\ngamma = \"ghcr.io/acme/gamma:v1.0.0@{DIGEST}\"\ntool = \"{IMAGE}@{DIGEST}\"\n"
        ),
    )
    .unwrap();
    fs::create_dir_all(vk.join("cache/beta")).unwrap();
    fs::write(vk.join("cache/beta/just"), "not a directory\n").unwrap();
    let src = m.root.join("work/tool/just");
    fs::create_dir_all(&src).unwrap();
    fs::write(src.join("tool.just"), "hello:\n    echo local\n").unwrap();
    let before = snapshot(&m);

    let (code, stdout, stderr) = run_idle(&m, &["dev", "tool", "-p", "./work/tool"]);

    assert_eq!(code, 2, "stderr: {stderr}");
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0056]: Internal vendor_kit error: the cache of installed tools is missing: .vendor_kit/cache/alpha/, .vendor_kit/cache/gamma/; run just vendor_kit sync first; reason code pending (draft VK0068, N4). This is a VK bug. Report it at https://github.com/ycpss91255-research/vendor_kit/issues and attach run log /srv/proj/.vendor_kit/log/r1.jsonl.
vendor_kit: error[VK0056]: Internal vendor_kit error: the cache of installed tool beta (.vendor_kit/cache/beta/) cannot be read: dist has no just/ directory; reason code pending (draft VK0073, N4). This is a VK bug. Report it at https://github.com/ycpss91255-research/vendor_kit/issues and attach run log /srv/proj/.vendor_kit/log/r1.jsonl.

"#]]
    );
    assert_eq!(snapshot(&m), before);
    assert!(!events(&m).iter().any(|e| e == "writes_started"));
}
