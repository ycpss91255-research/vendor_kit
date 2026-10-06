//! `upgrade --engine`、`upgrade --engine=<tag>` 的第一段（04 upgrade --engine、指定版本；訊息表 VK0007、VK0023）：
//! 經假的啟動器跑。
//!
//! 每個測試在暫存目錄建好安裝目錄（引擎鎖定在 v1.0.0、工具 `tool` 已導入），假啟動器回帶 LABEL 的 inspect 與
//! pull。第一段換好引擎鎖定行與介面版列表、留下進度檔，以 VK0023 停下；之後唯讀的 `update` 照進度檔報 VK0023。
//! 第二段（新引擎重產薄殼、刪進度檔）還沒做，重跑停在 VK0056。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::{Path, PathBuf};

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply, Request, Seen};
use e2e::registry::{Registry, Repo};
use e2e::{MOUNT_PREFIX_ENV, REGISTRY_URL_ENV, vendor_kit_bin};

const RUN_ID: &str = "r1";
const HOST_ROOT: &str = "/srv/proj";
const RUN_LOG: &str = ".vendor_kit/log/r1.jsonl";
const ENGINE_REPO: &str = "ghcr.io/ycpss91255-research/vendor_kit";
const OLD_ENGINE: &str = "ghcr.io/ycpss91255-research/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const TOOL: &str = "ghcr.io/acme/tool:v1.0.0@sha256:3333333333333333333333333333333333333333333333333333333333333333";
const DIGEST: &str = "sha256:2222222222222222222222222222222222222222222222222222222222222222";
const IMAGE_ID: &str = "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
/// 不需要 registry 的執行：連不到的位址，連了就會失敗。
const NO_REGISTRY: &str = "http://127.0.0.1:9";

fn target() -> String {
    format!("{ENGINE_REPO}:v1.2.0")
}

fn target_locked() -> String {
    format!("{}@{DIGEST}", target())
}

/// 安裝目錄：`version.toml` 有引擎 v1.0.0 與 `tool`，啟動器建好的空執行紀錄。
fn install(m: &Mounts) {
    let vk = m.root.join(".vendor_kit");
    fs::create_dir_all(vk.join("log")).unwrap();
    fs::write(
        vk.join("version.toml"),
        format!(
            "vendor_kit = \"{OLD_ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"{TOOL}\"\n"
        ),
    )
    .unwrap();
    fs::write(m.root.join(RUN_LOG), "").unwrap();
}

/// 目標引擎 image 的 inspect 輸出：RepoDigests 與 LABEL（介面版 [1, 2]、檔案版上限 `schema_max`）。
fn inspect_json(schema_max: u32) -> String {
    format!(
        "[\n    {{\n        \"Id\": \"{IMAGE_ID}\",\n        \"RepoTags\": [],\n        \"RepoDigests\": [\"{ENGINE_REPO}@{DIGEST}\"],\n        \"Config\": {{\n            \"Labels\": {{\n                \"org.opencontainers.image.version\": \"v1.2.0\",\n                \"vendor_kit.protocol.current\": \"2\",\n                \"vendor_kit.protocol.floor\": \"1\",\n                \"vendor_kit.schema.max\": \"{schema_max}\"\n            }}\n        }}\n    }}\n]\n"
    )
}

/// 假啟動器：`local` 為假時本機沒有 `<路徑>:<tag>`（不帶 digest 的 inspect 回 failed 1，pull 之後以
/// `<路徑>@<digest>` inspect 照常回）。
fn launcher(
    m: &Mounts,
    header: &str,
    local: bool,
    schema_max: u32,
) -> std::thread::JoinHandle<Seen> {
    let ctl = m.ctl.clone();
    launcher::serve(&m.ctl, header, move |req: &Request| match req.op.as_str() {
        "inspect" if !local && !req.args[0].contains('@') => Reply::Failed(1),
        "pull" => Reply::Ok,
        "inspect" => {
            fs::write(
                ctl.join(format!("res.{}.out", req.seq)),
                inspect_json(schema_max),
            )
            .unwrap();
            Reply::Ok
        }
        _ => Reply::Failed(1),
    })
}

/// 跑一次：介面版 `protocol`，registry 接到 `registry`（base URL）。
fn run(m: &Mounts, protocol: u32, rest: &[&str], registry: &str) -> (i32, String, String) {
    let p = protocol.to_string();
    let mut args = vec![
        "--protocol",
        &p,
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

fn header(protocol: u32) -> String {
    format!("vk-resolve/{protocol} {RUN_ID}")
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

/// 新的 session：上一次留下的 `ctl/` 控制檔會被新的假啟動器誤讀。
fn new_session(m: &Mounts) {
    fs::remove_dir_all(&m.ctl).unwrap();
    fs::create_dir_all(&m.ctl).unwrap();
}

/// 第一段做完：引擎鎖定行與介面版列表是目標，工具鎖定行不動，留下一份進度檔。
fn assert_switched(m: &Mounts) {
    let vk = m.root.join(".vendor_kit");
    assert_eq!(
        fs::read_to_string(vk.join("version.toml")).unwrap(),
        format!(
            "vendor_kit = \"{}\"\nvendor_kit_protocols = \"1 2\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"{TOOL}\"\n",
            target_locked()
        )
    );
    let progress: Vec<String> = fs::read_dir(&vk)
        .unwrap()
        .filter_map(|e| {
            let name = e.unwrap().file_name().to_string_lossy().into_owned();
            name.starts_with(".tmp.").then_some(name)
        })
        .collect();
    assert_eq!(progress, [".tmp.upgrade.r1.toml"]);
    let text = fs::read_to_string(vk.join(".tmp.upgrade.r1.toml")).unwrap();
    assert!(text.contains("target = \"vendor_kit\""), "{text}");
    assert!(
        text.contains(&format!("image = \"{}\"", target_locked())),
        "{text}"
    );
}

#[test]
fn first_stage_switches_the_lock_line_and_asks_to_run_again() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let peer = launcher(&m, &header(1), true, 1);

    let (code, stdout, stderr) = run(&m, 1, &["upgrade", "--engine=v1.2.0", "-y"], NO_REGISTRY);
    let seen = peer.join().unwrap();

    assert_eq!(code, 2, "{stderr}");
    assert_eq!(stdout, "");
    assert_eq!(
        stderr,
        "vendor_kit: error[VK0023]: Engine v1.2.0 is now installed. Run again: just vendor_kit upgrade --engine=v1.2.0 -y\n"
    );
    assert_eq!(seen.requests, [format!("inspect {}", target())]);
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_switched(&m);
    assert_eq!(
        events(&m),
        [
            "engine_started",
            "writes_started",
            "lock_line_write_started",
            "lock_line_written",
            "diagnostic_emitted",
            "engine_finished",
        ]
    );

    // 唯讀的 update 照進度檔報 VK0023，不查 registry、不動任何檔。
    new_session(&m);
    let before = snapshot(&m);
    let peer = launcher::serve(&m.ctl, &header(1), |_: &Request| Reply::Failed(1));
    let (code, stdout, stderr) = run(&m, 1, &["update"], NO_REGISTRY);
    let seen = peer.join().unwrap();
    assert_eq!(code, 2, "{stderr}");
    assert_eq!(stdout, "");
    assert_eq!(
        stderr,
        "vendor_kit: error[VK0023]: Engine v1.2.0 is now installed. Run again: just vendor_kit upgrade --engine=v1.2.0 -y\n"
    );
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(snapshot(&m), before);

    // 重跑原指令：第二段還沒做，停下，不再寫任何檔。
    new_session(&m);
    let peer = launcher::serve(&m.ctl, &header(1), |_: &Request| Reply::Failed(1));
    let (code, _, stderr) = run(&m, 1, &["upgrade", "--engine=v1.2.0", "-y"], NO_REGISTRY);
    let seen = peer.join().unwrap();
    assert_eq!(code, 2);
    assert!(
        stderr.starts_with("vendor_kit: error[VK0056]: Internal vendor_kit error: completing the engine upgrade recorded in .vendor_kit/.tmp.upgrade.r1.toml"),
        "{stderr}"
    );
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(snapshot(&m), before);
}

#[test]
fn without_a_tag_the_latest_engine_is_pulled_by_digest_even_from_a_newer_shell() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    let path = "ycpss91255-research/vendor_kit";
    let registry = Registry::start_with(
        &[(path, Repo::public(&["v1.0.0", "v1.2.0", "latest"]))],
        &[(path, "v1.2.0", DIGEST)],
    );
    // 薄殼的 P（2）超出這版引擎的區間：救援路徑照常執行，往返只送救援 op，以呼叫方的 P 回應。
    let peer = launcher(&m, &header(2), false, 1);

    let (code, stdout, stderr) = run(&m, 2, &["upgrade", "--engine"], registry.base());
    let seen = peer.join().unwrap();

    assert_eq!(code, 2, "{stderr}");
    assert_eq!(stdout, "");
    assert_eq!(
        stderr,
        "vendor_kit: error[VK0023]: Engine v1.2.0 is now installed. Run again: just vendor_kit upgrade --engine\n"
    );
    let pinned = format!("{ENGINE_REPO}@{DIGEST}");
    assert_eq!(
        seen.requests,
        [
            format!("inspect {}", target()),
            format!("pull {pinned}"),
            format!("inspect {pinned}"),
        ]
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/2 r1 done 2\n"));
    assert_switched(&m);
}

#[test]
fn a_target_that_cannot_read_the_existing_files_is_vk0007_without_writes() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install(&m);
    // 工具的印記是檔案版 2，目標引擎的上限是 1。
    fs::create_dir_all(m.root.join(".vendor_kit/cache")).unwrap();
    fs::write(
        m.root.join(".vendor_kit/cache/tool.stamp.toml"),
        "schema = 2\nwritten_by = \"v9.0.0\"\n",
    )
    .unwrap();
    let before = snapshot(&m);
    let peer = launcher(&m, &header(1), true, 1);

    let (code, stdout, stderr) = run(&m, 1, &["upgrade", "--engine=v1.2.0"], NO_REGISTRY);
    let seen = peer.join().unwrap();

    assert_eq!(code, 3, "{stderr}");
    assert_eq!(stdout, "");
    assert_eq!(
        stderr,
        "vendor_kit: fatal[VK0007]: Target engine v1.2.0 (interface version 2, schema version 1) cannot read the existing files (schema version 2) without loss. No files were modified except the run log. Specify a version that can read schema version 2: just vendor_kit upgrade --engine=<tag>\n"
    );
    assert_eq!(seen.requests, [format!("inspect {}", target())]);
    assert_eq!(snapshot(&m), before);
}
