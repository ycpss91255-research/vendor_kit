//! 03 輸出：只打 `just vendor_kit`、不帶指令時，stderr 依序印版本行、
//! VK0024 診斷與簡短用法，以 2 結束；stdout 不印，不動任何檔。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use assert_cmd::Command;
use e2e::{VERSION, vendor_kit_bin};
use snapbox::assert_data_eq;

/// 列出目錄下所有路徑（相對、排序），用來比對檔案樹沒被動過。
fn tree(root: &std::path::Path) -> Vec<String> {
    fn walk(root: &std::path::Path, dir: &std::path::Path, out: &mut Vec<String>) {
        for entry in std::fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            out.push(path.strip_prefix(root).unwrap().display().to_string());
            if path.is_dir() {
                walk(root, &path, out);
            }
        }
    }
    let mut out = Vec::new();
    walk(root, root, &mut out);
    out.sort();
    out
}

#[test]
fn no_command_prints_version_diagnostic_and_usage() {
    let dir = tempfile::tempdir().unwrap();
    std::fs::write(dir.path().join("justfile"), "default:\n").unwrap();
    let before = tree(dir.path());

    let assert = Command::new(vendor_kit_bin().unwrap())
        .current_dir(dir.path())
        .assert()
        .code(2);
    let output = assert.get_output();

    assert_data_eq!(String::from_utf8(output.stdout.clone()).unwrap(), "");
    assert_data_eq!(
        String::from_utf8(output.stderr.clone())
            .unwrap()
            .replace(VERSION, "[VERSION]"),
        snapbox::str![[r#"
vendor_kit [VERSION]
vendor_kit: error[VK0024]: No command was specified.
Usage: just vendor_kit <cmd> [arguments] [options]

"#]]
    );
    assert_eq!(tree(dir.path()), before);
}
