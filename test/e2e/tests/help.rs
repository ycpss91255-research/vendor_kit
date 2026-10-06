//! 各指令的 `-h`／`--help`（03 輸出、04 共同選項）：用法只印到 stdout、不加前綴，stderr 不印，以 0 結束；
//! 不動執行紀錄以外的檔。實際的 help 輸出就是唯一來源，這裡每份一個 golden。
//!
//! 救援呼叫的 `-h`（`install -h`、`upgrade --engine -h`、`sync -h`）在薄殼的 P 超出引擎的區間時也照印；
//! 其餘的 `-h` 跟一般呼叫一樣先報版本。這一版引擎只收 P=1，執行檔測得到的區間外只有 P 高於上限
//! （還沒有專屬代碼，計畫缺口 G6，暫以 VK0056）。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;

use assert_cmd::Command;
use e2e::launcher::Mounts;
use e2e::{MOUNT_PREFIX_ENV, vendor_kit_bin};
use snapbox::assert_data_eq;

const HOST_ROOT: &str = "/srv/proj";
const RUN_LOG: &str = ".vendor_kit/log/r1.jsonl";

/// 經假的啟動器入口跑一次（不回任何 request），安裝目錄只有空的執行紀錄；
/// 回傳結束碼、stdout、stderr、`done` 與 `.vendor_kit/` 底下除了 `log` 以外的檔名。
fn launch(protocol: u32, rest: &[&str]) -> (i32, String, String, String, Vec<String>) {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    fs::create_dir_all(m.root.join(".vendor_kit/log")).unwrap();
    fs::write(m.root.join(RUN_LOG), "").unwrap();
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
    let mut written: Vec<String> = fs::read_dir(m.root.join(".vendor_kit"))
        .unwrap()
        .map(|e| e.unwrap().file_name().into_string().unwrap())
        .filter(|n| n != "log")
        .collect();
    written.sort();
    (
        out.status.code().unwrap(),
        String::from_utf8(out.stdout).unwrap(),
        String::from_utf8(out.stderr).unwrap(),
        fs::read_to_string(m.ctl.join("done")).unwrap(),
        written,
    )
}

/// 介面版合（P=1）時印 `rest` 的用法：stdout 比 golden，stderr 空，以 0 結束，只寫執行紀錄。
fn help(rest: &[&str], expected: snapbox::data::Inline) {
    let (code, stdout, stderr, done, written) = launch(1, rest);
    assert_eq!(code, 0, "{rest:?}: {stderr}");
    assert_data_eq!(stdout, expected);
    assert_eq!(stderr, "", "{rest:?}");
    assert_eq!(done, "vk-resolve/1 r1 done 0\n");
    assert!(written.is_empty(), "{written:?}");
}

#[test]
fn add_help() {
    help(
        &["add", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit add <repo>[@<tag>] [options]

Add a tool at its latest version, at <tag>, or from a local image.

Options:
  -i, --image <image>               Use a local image or image tar instead of the registry
      --image-path <registry>/<path>
                                    Registry path of a tool not yet in the lock file
  -y, --yes                         Answer yes to the questions add asks
      --dry-run                     Print the changes without making them
      --registry-token-file <path>  Read a registry token from <path> to list versions
  -h, --help                        Print this help

"#]],
    );
}

#[test]
fn upgrade_help() {
    help(
        &["upgrade", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit upgrade <repo>[@<tag>] [options]

Move a tool to its latest version, or to <tag>, which may be older.

Options:
  -y, --yes                         Answer yes to the questions upgrade asks
      --dry-run                     Print the changes without making them
      --registry-token-file <path>  Read a registry token from <path> to list versions
  -h, --help                        Print this help

For the engine: just vendor_kit upgrade --engine -h

"#]],
    );
}

#[test]
fn upgrade_engine_help() {
    help(
        &["upgrade", "--engine", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit upgrade --engine[=<tag>] [options]

Move the engine to its latest version, or to <tag>, which may be older.
The first run switches the engine and stops; rerun the command it prints to finish.

Options:
  -y, --yes                         Answer yes to the questions upgrade asks
      --dry-run                     Print the changes without making them
  -h, --help                        Print this help

"#]],
    );
}

#[test]
fn dev_help() {
    help(
        &["dev", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit dev <repo> -p <dir> [options]

Use a local directory as the source of a tool in this working directory.

Options:
  -p, --path <dir>                  Local tool directory, relative to the install directory
      --dry-run                     Print the changes without making them
  -h, --help                        Print this help

For the engine: just vendor_kit dev --engine -h

"#]],
    );
}

#[test]
fn dev_engine_help() {
    help(
        &["dev", "--engine", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit dev --engine -i <image> [options]

Use a local engine image in this working directory.

Options:
  -i, --image <image>               Local engine image
      --dry-run                     Print the changes without making them
  -h, --help                        Print this help

"#]],
    );
}

#[test]
fn undev_help() {
    help(
        &["undev", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit undev <repo> [options]

Stop using the local source of a tool and sync it to its pinned version.

Options:
      --dry-run                     Print the changes without making them
  -h, --help                        Print this help

For the engine: just vendor_kit undev --engine -h

"#]],
    );
}

#[test]
fn undev_engine_help() {
    help(
        &["undev", "--engine", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit undev --engine [options]

Stop using the local engine image and return to the pinned engine.

Options:
      --dry-run                     Print the changes without making them
  -h, --help                        Print this help

"#]],
    );
}

#[test]
fn remove_help() {
    help(
        &["remove", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit remove <repo> [options]

Remove a tool. Init files are kept.

Options:
  -y, --yes                         Answer yes to the questions remove asks
      --dry-run                     Print the changes without making them
  -h, --help                        Print this help

"#]],
    );
}

#[test]
fn update_help() {
    help(
        &["update", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit update [<repo>] [options]

Check for new versions of all tools and the engine, or of <repo> only.
Prints one line per item: <repo> current: <tag> latest: <tag>

Options:
      --registry-token-file <path>  Read a registry token from <path> to list versions
  -h, --help                        Print this help

"#]],
    );
}

#[test]
fn sync_help() {
    help(
        &["sync", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit sync

Bring the content of every pinned tool in line with its pinned version.
Tool recipes run this first.

Options:
  -h, --help                        Print this help

"#]],
    );
}

#[test]
fn install_help() {
    help(
        &["install", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit install [options]

Finish or redo the VK install in this directory.

Options:
  -y, --yes                         Answer yes to the questions install asks
      --dry-run                     Print the changes without making them
  -h, --help                        Print this help

"#]],
    );
}

#[test]
fn uninstall_help() {
    help(
        &["uninstall", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit uninstall [options]

Remove VK from this directory. Init files are kept.

Options:
  -y, --yes                         Answer yes to the questions uninstall asks
      --dry-run                     Print the changes without making them
  -h, --help                        Print this help

"#]],
    );
}

#[test]
fn prune_help() {
    help(
        &["prune", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit prune [options]

Remove local resources no longer in use: caches of unpinned tools,
VK temporary files, and stopped containers VK created.

Options:
      --dry-run                     Print the changes without making them
  -h, --help                        Print this help

"#]],
    );
}

#[test]
fn test_help() {
    help(
        &["test", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit test [<path>]

Check the install. With <path>, then run your tests under <path>.

Options:
  -h, --help                        Print this help

To check a tool delivery: just vendor_kit test dist -h

"#]],
    );
}

#[test]
fn test_dist_help() {
    help(
        &["test", "dist", "-h"],
        snapbox::str![[r#"
Usage: just vendor_kit test dist

Check the tool delivery in this repo.

Options:
  -h, --help                        Print this help

"#]],
    );
}

#[test]
fn long_and_short_help_print_the_same_usage() {
    for (short, long) in [
        (&["add", "-h"][..], &["add", "--help"][..]),
        (
            &["upgrade", "--engine", "-h"],
            &["upgrade", "--help", "--engine"],
        ),
        (&["test", "dist", "-h"], &["test", "--help", "dist"]),
    ] {
        let (_, a, ..) = launch(1, short);
        let (code, b, ..) = launch(1, long);
        assert_eq!(code, 0, "{long:?}");
        assert_eq!(a, b, "{short:?} {long:?}");
    }
}

#[test]
fn rescue_help_still_prints_when_the_versions_do_not_match() {
    for rest in [
        &["install", "-h"][..],
        &["install", "--help"],
        &["upgrade", "--engine", "-h"],
        &["upgrade", "--engine", "--help"],
        &["sync", "-h"],
        &["sync", "--help"],
    ] {
        let (_, expected, ..) = launch(1, rest);
        let (code, stdout, stderr, done, written) = launch(2, rest);
        assert_eq!(code, 0, "{rest:?}: {stderr}");
        assert_eq!(stdout, expected, "{rest:?}");
        assert!(stdout.starts_with("Usage: just vendor_kit "), "{rest:?}");
        assert_eq!(stderr, "", "{rest:?}");
        assert_eq!(done, "vk-resolve/2 r1 done 0\n");
        assert!(written.is_empty(), "{written:?}");
    }
}

#[test]
fn other_help_reports_the_version_first_when_the_versions_do_not_match() {
    for rest in [&["add", "-h"][..], &["upgrade", "-h"], &["prune", "--help"]] {
        let (code, stdout, stderr, done, written) = launch(2, rest);
        assert_eq!(code, 2, "{rest:?}");
        assert_eq!(stdout, "", "{rest:?}");
        assert!(
            stderr.starts_with("vendor_kit: error[VK0056]: Internal vendor_kit error: interface version 2 is outside the supported range [1, 1]; reason code pending (G6)."),
            "{stderr}"
        );
        assert_eq!(done, "vk-resolve/2 r1 done 2\n");
        assert!(written.is_empty(), "{written:?}");
    }
}
