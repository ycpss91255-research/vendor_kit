//! `test dist`（04 檢查 (test)、03 輸出）：經假的啟動器檢查安裝目錄底下 `dist/` 的工具交付內容。
//!
//! 安裝目錄先排好跟這一版引擎一致的薄殼與 `version.toml`（提供工具的 repo 也要先導入 VK），再在旁邊放
//! `dist/`。`test dist` 不送任何 docker 動作，除執行紀錄外不寫任何檔。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::Path;

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply};
use e2e::{MOUNT_PREFIX_ENV, VERSION, shell, vendor_kit_bin};
use snapbox::assert_data_eq;

const RUN_ID: &str = "r1";
const HOST_ROOT: &str = "/srv/proj";
const RUN_LOG: &str = ".vendor_kit/log/r1.jsonl";
const ENGINE: &str = "ghcr.io/ycpss91255-research/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";

/// 導入過 VK、沒有接任何工具的 repo。
fn checkout(m: &Mounts) {
    let vk = m.root.join(".vendor_kit");
    fs::create_dir_all(vk.join("log")).unwrap();
    shell::install(&m.root, VERSION).unwrap();
    fs::write(
        vk.join("version.toml"),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n"
        ),
    )
    .unwrap();
}

/// 合格的交付內容：兩個 `<ns>`、一個子資料夾裡的文字檔與一個含 CR 的二進位檔。
fn dist(m: &Mounts) {
    let dist = m.root.join("dist");
    fs::create_dir_all(dist.join("just")).unwrap();
    fs::write(dist.join("just/tool.just"), "hello:\n    echo hi\n").unwrap();
    fs::write(dist.join("just/tool-extra.just"), "bye:\n    echo bye\n").unwrap();
    fs::create_dir_all(dist.join("share")).unwrap();
    fs::write(dist.join("share/readme.txt"), "tool files\n").unwrap();
    fs::write(dist.join("share/blob.bin"), b"\x00\r\n\x01").unwrap();
}

/// 安裝目錄下每個一般檔的路徑與內容，不含執行紀錄。
fn contents(m: &Mounts) -> Vec<(String, Vec<u8>)> {
    fn walk(root: &Path, dir: &Path, out: &mut Vec<(String, Vec<u8>)>) {
        for entry in fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            if path.is_symlink() {
                continue;
            }
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
    out.retain(|(p, _)| !p.starts_with(".vendor_kit/log"));
    out.sort();
    out
}

/// 跑 `test dist`：不送 docker 動作、除執行紀錄外不寫檔，`done` 帶整次的結束碼。
fn run_dist(m: &Mounts) -> (i32, String, String) {
    for d in [&m.ctl, &m.inbox] {
        fs::remove_dir_all(d).unwrap();
        fs::create_dir_all(d).unwrap();
    }
    fs::write(m.root.join(RUN_LOG), "").unwrap();
    let before = contents(m);
    let peer = launcher::serve(&m.ctl, &format!("vk-resolve/1 {RUN_ID}"), |_| {
        Reply::Failed(1)
    });
    let out = Command::new(vendor_kit_bin().unwrap())
        .args([
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
            "test",
            "dist",
        ])
        .env(MOUNT_PREFIX_ENV, &m.prefix)
        .write_stdin("")
        .output()
        .unwrap();
    let seen = peer.join().unwrap();
    let code = out.status.code().unwrap();
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(
        seen.done.as_deref(),
        Some(format!("vk-resolve/1 {RUN_ID} done {code}\n").as_str())
    );
    assert_eq!(contents(m), before, "test dist must not write any file");
    (
        code,
        String::from_utf8(out.stdout).unwrap(),
        String::from_utf8(out.stderr).unwrap(),
    )
}

#[test]
fn valid_delivery_passes() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m);
    dist(&m);

    let (code, stdout, stderr) = run_dist(&m);
    assert_eq!(code, 0, "{stderr}");
    assert_data_eq!(stdout, "Delivery check passed.\n");
    assert_data_eq!(stderr, "");
}

/// 訊息表 VK0048：沒有 `dist/`、或 `dist/` 底下沒有任何檔。
#[test]
fn no_delivery_content_is_vk0048() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m);

    let expected = "vendor_kit: error[VK0048]: Cannot check tool delivery content: /srv/proj/dist contains no delivery content.\n";
    let (code, stdout, stderr) = run_dist(&m);
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(stderr, expected);

    fs::create_dir_all(m.root.join("dist/just")).unwrap();
    let (code, stdout, stderr) = run_dist(&m);
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert_data_eq!(stderr, expected);
}

/// #372 N24：文字檔一律 LF，含 CR 就失敗；每個違反的檔各一條，依路徑排序，二進位檔不查。
#[test]
fn text_files_with_cr_fail() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m);
    dist(&m);
    fs::write(
        m.root.join("dist/just/tool.just"),
        "hello:\r\n    echo hi\r\n",
    )
    .unwrap();
    fs::write(m.root.join("dist/share/readme.txt"), "old mac\r").unwrap();

    let (code, stdout, stderr) = run_dist(&m);
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    let lines: Vec<&str> = stderr
        .lines()
        .filter(|l| l.starts_with("vendor_kit: "))
        .collect();
    assert_eq!(lines.len(), 2, "{stderr}");
    assert!(
        lines[0].starts_with(
            "vendor_kit: error[VK0056]: Internal vendor_kit error: dist/just/tool.just: text file contains CR, line endings must be LF; reason code pending (draft VK0075, N24)."
        ),
        "{stderr}"
    );
    assert!(
        lines[1].starts_with(
            "vendor_kit: error[VK0056]: Internal vendor_kit error: dist/share/readme.txt: text file contains CR, line endings must be LF; reason code pending (draft VK0075, N24)."
        ),
        "{stderr}"
    );
}

/// scope_roadmap 多命名空間工具：`dist/just/` 底下每一項都是 `<ns>.just`；`dist/` 底下不收 symlink。
#[test]
fn bad_layout_fails() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m);
    dist(&m);
    fs::write(m.root.join("dist/just/notes.txt"), "notes\n").unwrap();
    std::os::unix::fs::symlink("readme.txt", m.root.join("dist/share/link")).unwrap();

    let (code, stdout, stderr) = run_dist(&m);
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    let lines: Vec<&str> = stderr
        .lines()
        .filter(|l| l.starts_with("vendor_kit: "))
        .collect();
    assert_eq!(lines.len(), 2, "{stderr}");
    assert!(
        lines[0].starts_with(
            "vendor_kit: error[VK0056]: Internal vendor_kit error: dist/just/notes.txt is not named <ns>.just; reason code pending (draft VK0075, N78)."
        ),
        "{stderr}"
    );
    assert!(
        lines[1].starts_with(
            "vendor_kit: error[VK0056]: Internal vendor_kit error: dist/share/link: not a regular file or directory; reason code pending (draft VK0075, N78)."
        ),
        "{stderr}"
    );
}

/// #372 N3：`init.toml` 的欄位名沒定，有這個檔就以 VK0056 停下（同 `add`）。
#[test]
fn init_toml_waits_for_n3() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m);
    dist(&m);
    fs::write(m.root.join("dist/init.toml"), "# initial files\n").unwrap();

    let (code, stdout, stderr) = run_dist(&m);
    assert_eq!(code, 2);
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with(
            "vendor_kit: error[VK0056]: Internal vendor_kit error: checking the delivery rules of dist/init.toml (waits for N3) is not supported yet."
        ),
        "{stderr}"
    );
}
