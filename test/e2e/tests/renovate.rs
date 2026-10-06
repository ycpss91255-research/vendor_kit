//! Renovate preset（04 追蹤新版；`test/renovate/preset.json`）：VK 寫出的版本鎖定行要能由它辨識。
//!
//! 經假的啟動器跑 `install`，再 `add` 兩個工具，拿引擎寫出的 `.vendor_kit/version.toml` 套 preset 的
//! regex manager：檔案樣式要比得到 `version.toml`，matchStrings 只抓到引擎行與工具行，抓不到
//! `vendor_kit_protocols` 等其他根層欄位（鍵名的 `_` 斷開引擎行，ADR-0002）。
//!
//! Renovate 以 RE2 編 matchStrings，旗標只有 global（不加 multiline，`^` 是檔頭）；這裡用 `regex`
//! crate 的預設模式模擬：同樣不開 multiline，以 `find_iter` 走過整個檔。不連外網，也不跑 Renovate 本身。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::path::Path;

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply, Request, Seen};
use e2e::{MOUNT_PREFIX_ENV, VERSION, vendor_kit_bin};
use regex::Regex;
use serde_json::Value;

const PRESET: &str = concat!(env!("CARGO_MANIFEST_DIR"), "/../renovate/preset.json");
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
const IMAGE_ID: &str = "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
/// 要 `add` 的工具：工具名、image 的 repo、tag、digest。名字帶 `-` 與 `_`，涵蓋 TOML 裸鍵的字元。
const TOOLS: [(&str, &str, &str, &str); 2] = [
    (
        "tool",
        "ghcr.io/acme/tool",
        "v1.2.0",
        "sha256:2222222222222222222222222222222222222222222222222222222222222222",
    ),
    (
        "my-tool_2",
        "ghcr.io/acme/nested/other",
        "v10.0.3",
        "sha256:3333333333333333333333333333333333333333333333333333333333333333",
    ),
];
const SHELL: [(&str, &str); 4] = [
    ("entry.just", "# entry\nimport? 'vendor.just'\n"),
    ("vendor.just", "# vendor\n"),
    ("log.sh", "# log\n"),
    (
        ".gitignore",
        "cache/\ngen/\nlog/\nversion.local.toml\n.tmp.*\n",
    ),
];

/// 這個引擎自己的 pinned 引用（tag 是本引擎版）。
fn engine() -> String {
    format!("{ENGINE_REPO}:{VERSION}@{ENGINE_DIGEST}")
}

/// 每次執行前的 session：空的 `ctl/`、`in/`（含啟動器寫的引擎引用）與這次的空執行紀錄。
fn new_session(m: &Mounts) {
    for d in [&m.ctl, &m.inbox] {
        fs::remove_dir_all(d).unwrap();
        fs::create_dir_all(d).unwrap();
    }
    fs::create_dir_all(m.root.join(".vendor_kit/log")).unwrap();
    fs::write(m.root.join(RUN_LOG), "").unwrap();
    fs::write(m.inbox.join(IN_ENGINE), format!("{}\n", engine())).unwrap();
}

/// 什麼 op 都回失敗的假啟動器：`install` 不送 request。
fn idle_launcher(m: &Mounts) -> std::thread::JoinHandle<Seen> {
    launcher::serve(&m.ctl, HEADER, |_: &Request| Reply::Failed(1))
}

/// 回 inspect（帶 `repo@digest`）與 extract（放 `just/<name>.just`）的假啟動器（給 `add`）。
fn add_launcher(
    m: &Mounts,
    name: &'static str,
    repo: &'static str,
    digest: &'static str,
) -> std::thread::JoinHandle<Seen> {
    let (ctl, inbox) = (m.ctl.clone(), m.inbox.clone());
    launcher::serve(&m.ctl, HEADER, move |req: &Request| match req.op.as_str() {
        "inspect" => {
            let digests = [format!("{repo}@{digest}")];
            let digests: Vec<&str> = digests.iter().map(String::as_str).collect();
            fs::write(
                ctl.join(format!("res.{}.out", req.seq)),
                launcher::inspect_json(IMAGE_ID, &digests),
            )
            .unwrap();
            Reply::Ok
        }
        "extract" => {
            let dir = inbox.join(&req.args[1]);
            fs::create_dir_all(dir.join("just")).unwrap();
            fs::write(
                dir.join("just").join(format!("{name}.just")),
                "hello:\n    echo hi\n",
            )
            .unwrap();
            Reply::Ok
        }
        _ => Reply::Failed(1),
    })
}

/// 跑一次引擎（不能互動）；`release` 是出貨輸入目錄。
fn run(m: &Mounts, release: &Path, rest: &[&str]) -> (i32, String) {
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
        .env(RELEASE_DIR_ENV, release)
        .write_stdin("")
        .output()
        .unwrap();
    (
        out.status.code().unwrap(),
        String::from_utf8(out.stderr).unwrap(),
    )
}

/// 空的 repo 裡 `install`，再依序 `add` [`TOOLS`]；回引擎寫出的 `version.toml`。
fn written_lock_file(tmp: &Path) -> String {
    let m = Mounts::create(&tmp.join("m"));
    let rel = tmp.join("release");
    fs::create_dir_all(rel.join("shell")).unwrap();
    for (name, body) in SHELL {
        fs::write(rel.join("shell").join(name), body).unwrap();
    }

    new_session(&m);
    let peer = idle_launcher(&m);
    let (code, stderr) = run(&m, &rel, &["install"]);
    peer.join().unwrap();
    assert_eq!(code, 0, "install stderr: {stderr}");

    for (name, repo, tag, digest) in TOOLS {
        new_session(&m);
        let peer = add_launcher(&m, name, repo, digest);
        let image = format!("{repo}:{tag}");
        let (code, stderr) = run(&m, &rel, &["add", name, "-i", &image]);
        peer.join().unwrap();
        assert_eq!(code, 0, "add {name} stderr: {stderr}");
    }
    fs::read_to_string(m.root.join(".vendor_kit/version.toml")).unwrap()
}

/// preset 裡唯一的 regex manager。
fn manager() -> Value {
    let preset: Value = serde_json::from_str(&fs::read_to_string(PRESET).unwrap()).unwrap();
    let managers = preset["customManagers"].as_array().unwrap();
    assert_eq!(managers.len(), 1, "{preset}");
    let manager = managers[0].clone();
    assert_eq!(manager["customType"], "regex");
    assert_eq!(manager["datasourceTemplate"], "docker");
    manager
}

/// `managerFilePatterns` 的一項：`/<regex>/` 是 regex，其餘是 glob（這份 preset 只用 regex）。
fn file_patterns(manager: &Value) -> Vec<Regex> {
    manager["managerFilePatterns"]
        .as_array()
        .unwrap()
        .iter()
        .map(|p| {
            let p = p.as_str().unwrap();
            let body = p
                .strip_prefix('/')
                .and_then(|p| p.strip_suffix('/'))
                .unwrap_or_else(|| panic!("not a /regex/ pattern: {p}"));
            Regex::new(body).unwrap()
        })
        .collect()
}

/// matchStrings 抓到的一筆：抓到的原文與三個具名群組。
#[derive(Debug, PartialEq, Eq)]
struct Dep {
    line: String,
    dep_name: String,
    current_value: String,
    current_digest: String,
}

/// 照 Renovate 的 `matchStringsStrategy: any`（預設）：每條 matchString 各自走過整個檔。
fn deps(manager: &Value, text: &str) -> Vec<Dep> {
    let mut out = Vec::new();
    for s in manager["matchStrings"].as_array().unwrap() {
        let re = Regex::new(s.as_str().unwrap()).unwrap();
        for c in re.captures_iter(text) {
            out.push(Dep {
                line: c[0].trim_start_matches('\n').to_owned(),
                dep_name: c["depName"].to_owned(),
                current_value: c["currentValue"].to_owned(),
                current_digest: c["currentDigest"].to_owned(),
            });
        }
    }
    out
}

#[test]
fn file_patterns_match_the_lock_file_only() {
    let patterns = file_patterns(&manager());
    let matches = |path: &str| patterns.iter().any(|p| p.is_match(path));
    assert!(matches(".vendor_kit/version.toml"));
    assert!(matches("sub/dir/.vendor_kit/version.toml"));
    // 本機覆寫不進 git，值也不是 image 引用。
    assert!(!matches(".vendor_kit/version.local.toml"));
    assert!(!matches("version.toml"));
    assert!(!matches("x.vendor_kit/version.toml"));
}

#[test]
fn match_strings_find_the_engine_and_tool_lines_only() {
    let tmp = tempfile::tempdir().unwrap();
    let lock = written_lock_file(tmp.path());
    let found = deps(&manager(), &lock);

    let mut want = vec![Dep {
        line: format!("vendor_kit = \"{}\"", engine()),
        dep_name: ENGINE_REPO.to_owned(),
        current_value: VERSION.to_owned(),
        current_digest: ENGINE_DIGEST.to_owned(),
    }];
    for (name, repo, tag, digest) in TOOLS {
        want.push(Dep {
            line: format!("{name} = \"{repo}:{tag}@{digest}\""),
            dep_name: repo.to_owned(),
            current_value: tag.to_owned(),
            current_digest: digest.to_owned(),
        });
    }
    let sorted = |mut v: Vec<Dep>| {
        v.sort_by(|a, b| a.line.cmp(&b.line));
        v
    };
    assert_eq!(sorted(found), sorted(want), "{lock}");

    // 抓到的每一筆都是檔裡完整的一行；介面版列表那一行在檔裡，但沒被抓到。
    let lines: Vec<&str> = lock.lines().collect();
    let protocols = lines
        .iter()
        .find(|l| l.starts_with("vendor_kit_protocols = "))
        .unwrap_or_else(|| panic!("no protocols line: {lock}"));
    for dep in deps(&manager(), &lock) {
        assert!(lines.contains(&dep.line.as_str()), "{dep:?}\n{lock}");
        assert_ne!(dep.line, *protocols);
    }
}

#[test]
fn match_strings_skip_lines_that_are_not_release_lock_lines() {
    let manager = manager();
    let digest = ENGINE_DIGEST;
    for text in [
        // 介面版列表與其他根層欄位：值不是 image 引用。
        "vendor_kit_protocols = \"1\"\n",
        "written_by = \"v0.0.0\"\n",
        // 不是正式版 tag、沒有 digest、不是 GHCR。
        &format!("tool = \"ghcr.io/acme/tool:latest@{digest}\"\n"),
        "tool = \"ghcr.io/acme/tool:v1.2.0\"\n",
        &format!("tool = \"docker.io/acme/tool:v1.2.0@{digest}\"\n"),
        // 縮排、加引號的鍵、註解：都不是正規形的鎖定行。
        &format!("  tool = \"ghcr.io/acme/tool:v1.2.0@{digest}\"\n"),
        &format!("\"tool\" = \"ghcr.io/acme/tool:v1.2.0@{digest}\"\n"),
        &format!("# tool = \"ghcr.io/acme/tool:v1.2.0@{digest}\"\n"),
    ] {
        assert_eq!(deps(&manager, text), [], "{text}");
    }
}

#[test]
fn versioning_accepts_release_tags_only() {
    let manager = manager();
    let template = manager["versioningTemplate"].as_str().unwrap();
    let re = Regex::new(template.strip_prefix("regex:").unwrap()).unwrap();
    for tag in ["v0.0.0", "v1.2.3", "v10.20.30"] {
        assert!(re.is_match(tag), "{tag}");
    }
    for tag in ["1.2.3", "v1.2", "v01.2.3", "v1.2.3-rc.1", "latest"] {
        assert!(!re.is_match(tag), "{tag}");
    }
}
