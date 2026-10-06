//! `bootstrap.sh` 只檢查與 `--repair` 的引擎端（04 bootstrap.sh、ADR-0007）：經啟動器的入口 argv，`--` 之後只放
//! 保留入口 `@shell-check`、`@shell-repair`（engine/plan 的 `entry`；這裡不能依賴 engine crate，照抄名字）。
//!
//! 兩個入口都不送 request，不需要背景的假啟動器；引擎照常寫 `done`。薄殼模板以 [`shell::RELEASE_DIR_ENV`]
//! 從 fixture 目錄讀（[`e2e::shell`]）。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::Path;

use assert_cmd::Command;
use e2e::launcher::Mounts;
use e2e::{MOUNT_PREFIX_ENV, VERSION, shell, vendor_kit_bin};

const SHELL_CHECK: &str = "@shell-check";
const SHELL_REPAIR: &str = "@shell-repair";
const RUN_ID: &str = "r1";
const HOST_ROOT: &str = "/srv/proj";
const RUN_LOG: &str = ".vendor_kit/log/r1.jsonl";
const ENGINE: &str = "ghcr.io/ycpss91255-research/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const CONSISTENT: &str = "Shell files match this engine version's templates.\n";

/// 已安裝的目錄：版本鎖定行、跟這一版引擎一致的薄殼、出貨模板的 fixture。
fn installed(m: &Mounts) {
    let vk = m.root.join(".vendor_kit");
    fs::create_dir_all(vk.join("log")).unwrap();
    shell::install(&m.root, VERSION).unwrap();
    shell::release(&m.prefix.join("release")).unwrap();
    fs::write(
        vk.join("version.toml"),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n"
        ),
    )
    .unwrap();
    fs::write(m.root.join("justfile"), "import '.vendor_kit/entry.just'\n").unwrap();
}

/// 經啟動器的入口 argv 跑一次：P 是 `protocol`，`--` 之後是 `rest`。
fn run(m: &Mounts, protocol: u32, rest: &[&str]) -> (i32, String, String) {
    for d in [&m.ctl, &m.inbox] {
        fs::remove_dir_all(d).unwrap();
        fs::create_dir_all(d).unwrap();
    }
    fs::write(m.root.join(RUN_LOG), "").unwrap();
    let protocol = protocol.to_string();
    let mut args = vec![
        "--protocol",
        protocol.as_str(),
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
        .args(args)
        .env(MOUNT_PREFIX_ENV, &m.prefix)
        .env(shell::RELEASE_DIR_ENV, m.prefix.join("release"))
        .write_stdin("")
        .output()
        .unwrap();
    (
        out.status.code().unwrap(),
        String::from_utf8(out.stdout).unwrap(),
        String::from_utf8(out.stderr).unwrap(),
    )
}

fn done(m: &Mounts) -> String {
    fs::read_to_string(m.ctl.join("done")).unwrap()
}

/// 安裝目錄底下每個一般檔（相對路徑、內容），不含執行紀錄。
fn tree(m: &Mounts) -> Vec<(String, Vec<u8>)> {
    fn walk(root: &Path, dir: &Path, out: &mut Vec<(String, Vec<u8>)>) {
        for entry in fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                walk(root, &path, out);
            } else {
                let rel = path.strip_prefix(root).unwrap().display().to_string();
                out.push((rel, fs::read(&path).unwrap()));
            }
        }
    }
    let mut out = Vec::new();
    walk(&m.root, &m.root, &mut out);
    out.retain(|(p, _)| p != RUN_LOG);
    out.sort();
    out
}

/// 改掉一個薄殼檔的一個位元組（ADR-0007 驗收案例）。
fn flip_a_byte(m: &Mounts, name: &str) {
    let path = m.root.join(".vendor_kit").join(name);
    let mut bytes = fs::read(&path).unwrap();
    let last = bytes.len() - 2;
    bytes[last] ^= 0x01;
    fs::write(&path, bytes).unwrap();
}

#[test]
fn check_reports_consistent_even_outside_the_protocol_range() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    installed(&m);
    let before = tree(&m);
    // 這一版引擎只收 P=1；保留入口屬救援路徑，P=2 也照常回應。
    for protocol in [1, 2] {
        let (code, stdout, stderr) = run(&m, protocol, &[SHELL_CHECK]);
        assert_eq!(code, 0, "stderr: {stderr}");
        assert_eq!(stdout, CONSISTENT);
        assert_eq!(stderr, "");
        assert_eq!(done(&m), format!("vk-resolve/{protocol} r1 done 0\n"));
        assert_eq!(tree(&m), before);
    }
}

#[test]
fn check_reports_vk0006_and_writes_nothing() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    installed(&m);
    flip_a_byte(&m, "entry.just");
    let before = tree(&m);
    let (code, stdout, stderr) = run(&m, 1, &[SHELL_CHECK]);
    assert_eq!(code, 2, "stderr: {stderr}");
    assert_eq!(stdout, "");
    assert!(
        stderr.starts_with(
            "vendor_kit: error[VK0006]: Shell files do not match this engine version's templates: \
             .vendor_kit/entry.just (modified). No shell files were regenerated."
        ),
        "{stderr}"
    );
    assert_eq!(done(&m), "vk-resolve/1 r1 done 2\n");
    assert_eq!(tree(&m), before);
}

#[test]
fn repair_regenerates_the_modified_file_then_is_consistent() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    installed(&m);
    let good = tree(&m);
    flip_a_byte(&m, "log.sh");

    let (code, stdout, stderr) = run(&m, 1, &[SHELL_REPAIR]);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(
        stdout,
        "Shell files that do not match this engine version's templates:\n  \
         .vendor_kit/log.sh (modified)\nRegenerated .vendor_kit/log.sh.\n"
    );
    assert_eq!(stderr, "");
    assert_eq!(done(&m), "vk-resolve/1 r1 done 0\n");
    // 只重產 log.sh：其他檔（鎖定行、根目錄檔）不動，也沒有新檔。
    assert_eq!(tree(&m), good);

    // 一致時不重產。
    let (code, stdout, stderr) = run(&m, 1, &[SHELL_REPAIR]);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(stdout, CONSISTENT);
    assert_eq!(tree(&m), good);
}

#[test]
fn reserved_entries_take_no_other_arguments() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    installed(&m);
    flip_a_byte(&m, "log.sh");
    let before = tree(&m);
    for rest in [&[SHELL_REPAIR, "-y"][..], &[SHELL_CHECK, SHELL_CHECK]] {
        let (code, stdout, stderr) = run(&m, 1, rest);
        assert_eq!(code, 2, "{rest:?}");
        assert_eq!(stdout, "");
        assert!(
            stderr.starts_with("vendor_kit: error[VK0026]: "),
            "{stderr}"
        );
        assert!(stderr.contains(rest[0]), "{stderr}");
        assert_eq!(tree(&m), before);
    }
}
