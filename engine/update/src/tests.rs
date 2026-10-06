//! 單元測試：直接在暫存的安裝目錄跑 `update`。驗查詢前的停下點（殘留進度、VK0046、檔案版過高）、
//! 本機覆寫提醒、列 tag 的缺口，以及每個情況都不動任何檔；另驗結果行格式與 `<original_command>` 的重組。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::io;
use std::path::PathBuf;
use std::sync::{Arc, Mutex};

use diagnostics::NoSink;
use progress::Progress;

use super::*;

const WRITTEN_BY: &str = "v0.0.0";
const ENGINE: &str = "ghcr.io/acme/vendor_kit:v1.4.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const TOOL: &str = "ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222";
const OTHER: &str = "ghcr.io/acme/other:v1.0.0@sha256:3333333333333333333333333333333333333333333333333333333333333333";

struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
}

impl Fx {
    /// `tool`、`other` 都已導入的安裝目錄。
    fn new() -> Fx {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        fs::create_dir_all(dir.vk_dir().join("log")).unwrap();
        fs::write(
            dir.version_toml(),
            format!(
                "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nother = \"{OTHER}\"\ntool = \"{TOOL}\"\n"
            ),
        )
        .unwrap();
        Fx { _tmp: tmp, dir }
    }

    /// `.vendor_kit/` 下每個檔的路徑與內容（不含 `log/` 與鎖檔），比對有沒有被動到。
    fn snapshot(&self) -> Vec<(PathBuf, Vec<u8>)> {
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
        walk(&self.dir.vk_dir(), &mut out);
        out.retain(|(p, _)| {
            !p.starts_with(self.dir.vk_dir().join("log"))
                && p.file_name()
                    .is_some_and(|n| !n.to_string_lossy().contains("lock"))
        });
        out.sort();
        out
    }

    /// 寫一份殘留的進度檔；`table` 是 recipe 自己的欄位（`[<verb>]` 下的 `key = value` 行）。
    fn residual(&self, verb: &str, command: &[&str], table: Option<(&str, &str)>) {
        let mut p = Progress::new(verb, "r0", command).unwrap();
        if let Some((key, value)) = table {
            p.document_mut().set(&[verb, key], value).unwrap();
        }
        p.create(&self.dir, WRITTEN_BY).unwrap();
    }
}

#[derive(Clone, Default)]
struct Shared(Arc<Mutex<Vec<u8>>>);

impl Write for Shared {
    fn write(&mut self, data: &[u8]) -> io::Result<usize> {
        self.0.lock().unwrap().extend_from_slice(data);
        Ok(data.len())
    }
    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}

impl Shared {
    fn text(&self) -> String {
        String::from_utf8(self.0.lock().unwrap().clone()).unwrap()
    }
}

struct Out {
    code: u8,
    stdout: String,
    /// 提醒與診斷，依序。
    stderr: String,
}

fn run_update(fx: &Fx, repo: Option<&str>) -> Out {
    let mut stdout = Vec::new();
    let shared = Shared::default();
    let mut plain = shared.clone();
    let mut diags = Diagnostics::with_sink(shared.clone(), NoSink);
    let code = {
        let mut env = Env {
            dir: &fx.dir,
            host_root: "/h/proj",
            run_log: "/h/proj/.vendor_kit/log/r1.jsonl",
            stdout: &mut stdout,
            stderr: &mut plain,
            diags: &mut diags,
        };
        run(&Request { repo }, &mut env)
    };
    Out {
        code,
        stdout: String::from_utf8(stdout).unwrap(),
        stderr: shared.text(),
    }
}

fn diag_codes(stderr: &str) -> Vec<&str> {
    stderr
        .lines()
        .filter_map(|l| l.strip_prefix("vendor_kit: "))
        .filter_map(|l| l.split_once('[').map(|(_, rest)| rest))
        .filter_map(|l| l.split_once("]: ").map(|(c, _)| c))
        .collect()
}

#[test]
fn result_line_format() {
    let t = |s: &str| Tag::parse(s).unwrap();
    assert_eq!(
        text::result_line("lint", t("v1.0.0"), Some(t("v1.3.0"))),
        "lint current: v1.0.0 latest: v1.3.0"
    );
    assert_eq!(
        text::result_line(text::ENGINE_NAME, t("v1.4.0"), None),
        "vendor_kit current: v1.4.0 latest: none"
    );
    // 04 指定版本：逐欄比數值、略過不合法的 tag，最新版可能比 current 舊。
    let latest = Tag::latest(["v1.10.0", "v1.9.9", "latest", "v01.0.0"]);
    assert_eq!(
        text::result_line("base", t("v2.0.0"), latest),
        "base current: v2.0.0 latest: v1.10.0"
    );
    assert_eq!(Tag::latest(["latest", "main"]), None);
}

#[test]
fn original_command_quotes_each_argument() {
    assert_eq!(
        original_command(&["remove", "tool"]),
        "just vendor_kit remove tool"
    );
    assert_eq!(
        original_command(&["dev", "tool", "-p", "my dir", "it's"]),
        r"just vendor_kit dev tool -p 'my dir' 'it'\''s'"
    );
    assert_eq!(original_command(&["x", ""]), "just vendor_kit x ''");
}

#[test]
fn listing_tags_is_a_gap_for_all_tools_and_the_engine() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let out = run_update(&fx, None);
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(
        out.stderr.contains(
            "listing tags from the registry for update (other (v1.0.0), tool (v1.2.0), vendor_kit (v1.4.0)) is not supported yet"
        ),
        "{}",
        out.stderr
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn update_repo_queries_only_that_tool() {
    let fx = Fx::new();
    let out = run_update(&fx, Some("tool"));
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert!(
        out.stderr
            .contains("for update (tool (v1.2.0)) is not supported yet"),
        "{}",
        out.stderr
    );
}

#[test]
fn update_of_a_tool_not_in_the_lock_lines_is_vk0046() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let out = run_update(&fx, Some("missing"));
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0046]: Tool missing is not in the lock version lines. The requested operation did not complete.\n"
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn residual_progress_is_detected_before_the_target_check_and_left_alone() {
    let fx = Fx::new();
    fx.residual("add", &["add", "new", "-i", "x"], Some(("repo", "new")));
    fx.residual("remove", &["remove", "tool"], None);
    let before = fx.snapshot();
    let out = run_update(&fx, Some("missing"));
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        diag_codes(&out.stderr),
        ["VK0004", "VK0054"],
        "{}",
        out.stderr
    );
    assert!(
        out.stderr
            .contains("Import of new is incomplete. Run: just vendor_kit add new"),
        "{}",
        out.stderr
    );
    assert!(
        out.stderr.contains(
            "Operation remove in /h/proj is incomplete. Run again: just vendor_kit remove tool"
        ),
        "{}",
        out.stderr
    );
    // 唯讀 recipe：不恢復、不刪進度檔。
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn residual_tool_upgrade_progress_is_vk0041_with_the_original_command() {
    let fx = Fx::new();
    fx.residual(
        UPGRADE_VERB,
        &[UPGRADE_VERB, "tool@v1.3.0", "-y"],
        Some((progress::upgrade::TARGET, "tool")),
    );
    let before = fx.snapshot();
    let out = run_update(&fx, None);
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0041]: Upgrade of tool is incomplete. Run again: just vendor_kit upgrade tool@v1.3.0 -y\n"
    );
    // 唯讀 recipe：不恢復、不刪進度檔。
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn residual_engine_upgrade_or_upgrade_without_target_is_a_gap() {
    let fx = Fx::new();
    fx.residual(
        UPGRADE_VERB,
        &[UPGRADE_VERB, "--engine"],
        Some((progress::upgrade::TARGET, progress::upgrade::ENGINE_TARGET)),
    );
    let out = run_update(&fx, None);
    assert_eq!(out.code, 2);
    assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(
        out.stderr
            .contains("reporting the incomplete engine upgrade"),
        "{}",
        out.stderr
    );

    let fx = Fx::new();
    fx.residual(UPGRADE_VERB, &[UPGRADE_VERB, "tool"], None);
    let out = run_update(&fx, None);
    assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(out.stderr.contains("without its [upgrade] target field"));
}

#[test]
fn residual_undev_progress_is_vk0053_with_the_original_command() {
    let fx = Fx::new();
    fx.residual(
        UNDEV_VERB,
        &[UNDEV_VERB, "tool"],
        Some((UNDEV_TARGET_KEY, "tool")),
    );
    let before = fx.snapshot();
    let out = run_update(&fx, None);
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0053]: The undev operation for tool is incomplete. Run again: just vendor_kit undev tool\n"
    );
    assert_eq!(fx.snapshot(), before);

    // 沒有 `[undev] target` 欄位：缺口。
    let fx = Fx::new();
    fx.residual(UNDEV_VERB, &[UNDEV_VERB, "--engine"], None);
    let out = run_update(&fx, None);
    assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(out.stderr.contains("without its [undev] target field"));
}

#[test]
fn residual_add_without_its_repo_field_is_a_gap() {
    let fx = Fx::new();
    fx.residual("add", &["add", "new"], None);
    let out = run_update(&fx, None);
    assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(out.stderr.contains("without its [add] repo field"));
}

#[test]
fn local_overrides_are_reminded_on_stderr_without_a_prefix() {
    let fx = Fx::new();
    fs::write(
        fx.dir.version_local_toml(),
        "vendor_kit = \"ghcr.io/acme/vendor_kit:dev\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"../tool\"\n",
    )
    .unwrap();
    let before = fx.snapshot();

    let out = run_update(&fx, None);
    let lines: Vec<&str> = out.stderr.lines().collect();
    assert_eq!(
        lines[..2],
        [
            "tool uses the local override ../tool; update checks the lock version line.",
            "vendor_kit uses the local override ghcr.io/acme/vendor_kit:dev; update checks the lock version line.",
        ],
        "{}",
        out.stderr
    );
    assert_eq!(diag_codes(&out.stderr), ["VK0056"]);

    // `update <repo>` 只提醒那個工具的覆寫，不提引擎。
    let out = run_update(&fx, Some("other"));
    assert!(!out.stderr.contains("local override"), "{}", out.stderr);
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn lock_file_too_new_is_vk0008() {
    let fx = Fx::new();
    fs::write(
        fx.dir.version_toml(),
        format!("vendor_kit = \"{ENGINE}\"\nschema = 99\nwritten_by = \"v9.0.0\"\n"),
    )
    .unwrap();
    let out = run_update(&fx, None);
    assert_eq!(out.code, 3);
    assert_eq!(diag_codes(&out.stderr), ["VK0008"], "{}", out.stderr);
}
