//! 介面版（ADR-0008:26、#372 N61、N19）：薄殼的 P 超出引擎的區間時，救援呼叫照常、以薄殼的 P 回應；
//! 其餘呼叫先報版本，不報用法錯誤，也不寫執行紀錄以外的檔。
//!
//! 這一版引擎收 P=1、2，執行檔測得到的區間外只有 P 高於上限（這裡用 3）；那一邊還沒有專屬代碼（計畫缺口 G6），
//! 暫以 VK0056 停下。P 低於 floor 的 VK0009（fatal 3）在 engine/vendor_kit 的 unit 測試以注入的區間驗。
//! 救援的 `sync` 實際跑完的案例在 `sync.rs`。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;

use assert_cmd::Command;
use e2e::launcher::Mounts;
use e2e::{MOUNT_PREFIX_ENV, vendor_kit_bin};

const HOST_ROOT: &str = "/srv/proj";
const RUN_LOG: &str = ".vendor_kit/log/r1.jsonl";

/// 安裝目錄只有 `.vendor_kit/log/` 與空的執行紀錄。
fn install_dir(m: &Mounts) {
    fs::create_dir_all(m.root.join(".vendor_kit/log")).unwrap();
    fs::write(m.root.join(RUN_LOG), "").unwrap();
}

/// 經假的啟動器入口跑一次（不回任何 request）；回傳結束碼、stdout、stderr 與 `done`。
fn launch(m: &Mounts, protocol: u32, rest: &[&str]) -> (i32, String, String, String) {
    let protocol = protocol.to_string();
    let mut args = vec![
        "--protocol",
        protocol.as_str(),
        "--run-id",
        "r1",
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
        fs::read_to_string(m.ctl.join("done")).unwrap(),
    )
}

/// `.vendor_kit/` 底下除了執行紀錄以外的路徑。
fn written(m: &Mounts) -> Vec<String> {
    let vk = m.root.join(".vendor_kit");
    let mut out: Vec<String> = fs::read_dir(&vk)
        .unwrap()
        .map(|e| e.unwrap().file_name().into_string().unwrap())
        .filter(|n| n != "log")
        .collect();
    out.sort();
    out
}

const NEWER_SHELL: &str = "vendor_kit: error[VK0056]: Internal vendor_kit error: interface version 3 is outside the supported range [1, 2]; reason code pending (G6).";

#[test]
fn general_recipe_outside_the_range_reports_the_version_before_any_write() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install_dir(&m);
    let (code, stdout, stderr, done) = launch(&m, 3, &["prune"]);
    assert_eq!(code, 2);
    assert_eq!(stdout, "");
    assert!(stderr.starts_with(NEWER_SHELL), "{stderr}");
    assert_eq!(stderr.lines().count(), 1, "{stderr}");
    assert_eq!(done, "vk-resolve/3 r1 done 2\n");
    assert!(written(&m).is_empty(), "{:?}", written(&m));
}

#[test]
fn rescue_candidate_with_a_usage_error_reports_the_version_first() {
    // 版本合：用法錯誤（VK0026）並附用法。
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install_dir(&m);
    let (code, _, stderr, done) = launch(&m, 1, &["upgrade", "--engine", "--bogus"]);
    assert_eq!(code, 2);
    assert!(
        stderr.starts_with(
            "vendor_kit: error[VK0026]: Unknown, extra, or disallowed argument: --bogus."
        ),
        "{stderr}"
    );
    assert_eq!(done, "vk-resolve/1 r1 done 2\n");

    // 版本不合：先報版本，不報用法錯誤。
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install_dir(&m);
    let (code, _, stderr, done) = launch(&m, 3, &["upgrade", "--engine", "--bogus"]);
    assert_eq!(code, 2);
    assert!(stderr.starts_with(NEWER_SHELL), "{stderr}");
    assert!(!stderr.contains("VK0026"), "{stderr}");
    assert_eq!(done, "vk-resolve/3 r1 done 2\n");
}

#[test]
fn usage_call_outside_the_range_still_prints_usage() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    install_dir(&m);
    let (code, stdout, stderr, done) = launch(&m, 3, &[]);
    assert_eq!(code, 2);
    assert_eq!(stdout, "");
    assert!(
        stderr.contains("error[VK0024]: No command was specified."),
        "{stderr}"
    );
    assert!(!stderr.contains("VK0056"), "{stderr}");
    assert_eq!(done, "vk-resolve/3 r1 done 2\n");
}
