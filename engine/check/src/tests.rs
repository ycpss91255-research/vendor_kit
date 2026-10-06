//! 單元測試：在暫存的安裝目錄排出各種 `cache/`、印記、`gen/`、覆寫與進度檔狀態，跑整段檢查。
//! 驗通過與各停下點的診斷，以及不寫任何檔（鎖是 `flock` 安裝目錄本身，不建檔）。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::path::PathBuf;

use diagnostics::NoSink;
use progress::Progress;

use super::*;

mod user;

const WRITTEN_BY: &str = "v0.0.0";
const ENGINE: &str = "ghcr.io/acme/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const HOST_ROOT: &str = "/h/proj";

/// 薄殼四檔的模板本文（順序同 `layout::SHELL_FILES`）。
const BODIES: [&str; 4] = ["# entry\n", "# vendor\n", "# log\n", "cache/\ngen/\n"];

fn templates() -> [Vec<u8>; 4] {
    BODIES.map(|b| b.as_bytes().to_vec())
}

/// 一個假工具：名字、digest 的 hex 字元與交付的 `<ns>`。
struct Tool {
    name: &'static str,
    hex: char,
    namespaces: &'static [&'static str],
}

const TOOL: Tool = Tool {
    name: "tool",
    hex: '2',
    namespaces: &["tool", "tool-extra"],
};
const OTHER: Tool = Tool {
    name: "other",
    hex: '3',
    namespaces: &["other"],
};

impl Tool {
    fn locked(&self) -> String {
        format!(
            "ghcr.io/acme/{}:v1.2.0@sha256:{}",
            self.name,
            self.hex.to_string().repeat(64)
        )
    }
}

struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
}

impl Fx {
    /// 跟這一版引擎一致的薄殼與 `version.toml`；`cache/`、`gen/` 都還沒有（全新 checkout）。
    fn checkout(tools: &[&Tool]) -> Fx {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path().join("root"));
        fs::create_dir_all(dir.vk_dir()).unwrap();
        let lines: String = tools
            .iter()
            .map(|t| format!("{} = \"{}\"\n", t.name, t.locked()))
            .collect();
        let tools = if lines.is_empty() {
            String::new()
        } else {
            format!("\n[tools]\n{lines}")
        };
        fs::write(
            dir.version_toml(),
            format!(
                "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n{tools}"
            ),
        )
        .unwrap();
        let bodies = BODIES.map(str::as_bytes);
        Shell::render(compat::THIS.current_protocol, WRITTEN_BY, bodies)
            .unwrap()
            .write(&dir)
            .unwrap();
        Fx { _tmp: tmp, dir }
    }

    /// 全新 checkout 之後照 `sync` 的結果排好 `cache/`、印記與 `gen/tools.just`。
    fn synced(tools: &[&Tool]) -> Fx {
        let fx = Fx::checkout(tools);
        let mut entry: Vec<tools_just::Tool> = Vec::new();
        let ns: Vec<Vec<String>> = tools
            .iter()
            .map(|t| t.namespaces.iter().map(|s| (*s).to_owned()).collect())
            .collect();
        for (t, ns) in tools.iter().zip(&ns) {
            fx.cache(t);
            entry.push(tools_just::Tool {
                repo: t.name,
                namespaces: ns,
            });
        }
        if !tools.is_empty() {
            fs::create_dir_all(fx.dir.gen_dir()).unwrap();
            fs::write(fx.entry(), tools_just::render(&entry).unwrap()).unwrap();
        }
        fx
    }

    /// 一個工具的 `cache/<repo>/` 與印記。
    fn cache(&self, t: &Tool) {
        let root = self.dir.tool_cache(t.name).unwrap();
        fs::create_dir_all(root.join("just")).unwrap();
        for ns in t.namespaces {
            fs::write(root.join("just").join(format!("{ns}.just")), "x:\n").unwrap();
        }
        fs::create_dir_all(root.join("share")).unwrap();
        fs::write(root.join("share/readme.txt"), "tool files\n").unwrap();
        Stamp::compute(t.locked(), &root)
            .unwrap()
            .save(&stamp::tool_file(&self.dir, t.name), WRITTEN_BY)
            .unwrap();
    }

    fn entry(&self) -> PathBuf {
        self.dir.gen_dir().join(TOOLS_JUST)
    }

    fn progress(&self, verb: &str, command: &[&str], field: Option<(&str, &str, &str)>) {
        let mut p = Progress::new(verb, "old1", command).unwrap();
        if let Some((table, key, value)) = field {
            p.document_mut().set(&[table, key], value).unwrap();
        }
        p.create(&self.dir, WRITTEN_BY).unwrap();
    }

    /// 安裝目錄下每個一般檔的路徑與內容；符號連結記它指到哪裡，不跟過去。
    fn snapshot(&self) -> Vec<(String, Vec<u8>)> {
        fn walk(root: &Path, dir: &Path, out: &mut Vec<(String, Vec<u8>)>) {
            for entry in fs::read_dir(dir).unwrap() {
                let path = entry.unwrap().path();
                let meta = fs::symlink_metadata(&path).unwrap();
                let rel = path.strip_prefix(root).unwrap().display().to_string();
                if meta.is_symlink() {
                    let target = fs::read_link(&path).unwrap();
                    out.push((rel, target.display().to_string().into_bytes()));
                } else if meta.is_dir() {
                    walk(root, &path, out);
                } else {
                    out.push((rel, fs::read(&path).unwrap()));
                }
            }
        }
        let mut out = Vec::new();
        walk(self.dir.root(), self.dir.root(), &mut out);
        out.sort();
        out
    }
}

struct Out {
    code: u8,
    stdout: String,
    stderr: String,
}

fn run_check(fx: &Fx) -> Out {
    run_with(fx, Some(&templates()))
}

fn run_with(fx: &Fx, shell_templates: Option<&[Vec<u8>; 4]>) -> Out {
    let before = fx.snapshot();
    let mut stdout = Vec::new();
    let mut stderr = Vec::new();
    let code = {
        let mut diags = Diagnostics::with_sink(&mut stderr, NoSink);
        let mut env = Env {
            dir: &fx.dir,
            host_root: HOST_ROOT,
            run_log: "/h/proj/.vendor_kit/log/r1.jsonl",
            written_by: WRITTEN_BY,
            shell_templates,
            stdout: &mut stdout,
            diags: &mut diags,
        };
        run(&mut env)
    };
    assert_eq!(fx.snapshot(), before, "test must not write any file");
    Out {
        code,
        stdout: String::from_utf8(stdout).unwrap(),
        stderr: String::from_utf8(stderr).unwrap(),
    }
}

/// stderr 裡每條診斷的代碼，依序。
fn codes(stderr: &str) -> Vec<String> {
    stderr
        .lines()
        .filter_map(|l| l.split_once("[VK").map(|(_, r)| format!("VK{}", &r[..4])))
        .collect()
}

#[test]
fn synced_install_passes() {
    let fx = Fx::synced(&[&TOOL, &OTHER]);
    let out = run_check(&fx);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, format!("{}\n", text::PASSED));
    assert_eq!(out.stderr, "");
}

#[test]
fn no_tools_checks_shell_and_engine_and_passes_without_gen() {
    let fx = Fx::synced(&[]);
    assert!(!fx.entry().exists());
    let out = run_check(&fx);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, format!("{}\n", text::PASSED));
}

#[test]
fn no_tools_still_reports_a_shell_mismatch() {
    let fx = Fx::synced(&[]);
    fs::write(fx.dir.vk_dir().join("vendor.just"), "# edited\n").unwrap();
    let out = run_check(&fx);
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(codes(&out.stderr), ["VK0006"]);
    assert!(
        out.stderr.contains(".vendor_kit/vendor.just"),
        "{}",
        out.stderr
    );
}

#[test]
fn fresh_checkout_counts_as_missing_files() {
    let fx = Fx::checkout(&[&TOOL, &OTHER]);
    let out = run_check(&fx);
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(codes(&out.stderr), ["VK0047", "VK0047", "VK0047"]);
    for needle in [
        "Cannot complete checks for other: required local files are missing: \
         .vendor_kit/cache/other.stamp.toml (missing), .vendor_kit/cache/other/ (missing)",
        "Cannot complete checks for tool: required local files are missing: \
         .vendor_kit/cache/tool.stamp.toml (missing), .vendor_kit/cache/tool/ (missing)",
        "Cannot complete checks for /h/proj: required local files are missing: \
         .vendor_kit/gen/tools.just (missing)",
    ] {
        assert!(out.stderr.contains(needle), "{needle}\n{}", out.stderr);
    }
}

#[test]
fn cache_that_does_not_match_its_stamp_is_reported_file_by_file() {
    let fx = Fx::synced(&[&TOOL, &OTHER]);
    let cache = fx.dir.tool_cache("tool").unwrap();
    fs::write(cache.join("share/readme.txt"), "edited\n").unwrap();
    fs::write(cache.join("share/new.txt"), "new\n").unwrap();
    fs::remove_file(cache.join("just/tool-extra.just")).unwrap();
    let out = run_check(&fx);
    assert_eq!(out.code, 2);
    assert_eq!(codes(&out.stderr), ["VK0047"]);
    assert!(
        out.stderr.contains(
            "Cannot complete checks for tool: required local files are missing: \
             .vendor_kit/cache/tool/just/tool-extra.just (missing), \
             .vendor_kit/cache/tool/share/new.txt (extra), \
             .vendor_kit/cache/tool/share/readme.txt (changed)"
        ),
        "{}",
        out.stderr
    );
}

#[test]
fn whole_cache_dir_missing_with_a_stamp() {
    let fx = Fx::synced(&[&TOOL]);
    fs::remove_dir_all(fx.dir.tool_cache("tool").unwrap()).unwrap();
    let out = run_check(&fx);
    assert_eq!(codes(&out.stderr), ["VK0047"]);
    assert!(
        out.stderr.contains(
            "for tool: required local files are missing: .vendor_kit/cache/tool/ (missing)"
        ),
        "{}",
        out.stderr
    );
}

#[test]
fn stamp_of_another_version_or_corrupt_is_inconsistent() {
    let fx = Fx::synced(&[&TOOL, &OTHER]);
    let lock = fs::read_to_string(fx.dir.version_toml()).unwrap();
    fs::write(
        fx.dir.version_toml(),
        lock.replace("tool:v1.2.0", "tool:v1.3.0"),
    )
    .unwrap();
    fs::write(stamp::tool_file(&fx.dir, "other"), "not = [toml\n").unwrap();
    let out = run_check(&fx);
    assert_eq!(out.code, 2);
    assert_eq!(codes(&out.stderr), ["VK0047", "VK0047"]);
    assert!(
        out.stderr
            .contains(".vendor_kit/cache/other.stamp.toml (corrupt)"),
        "{}",
        out.stderr
    );
    assert!(
        out.stderr
            .contains(".vendor_kit/cache/tool.stamp.toml (other version)"),
        "{}",
        out.stderr
    );
}

#[test]
fn entry_file_missing_or_changed() {
    let fx = Fx::synced(&[&TOOL]);
    fs::write(fx.entry(), "mod? tool 'elsewhere.just'\n").unwrap();
    let out = run_check(&fx);
    assert_eq!(codes(&out.stderr), ["VK0047"]);
    assert!(
        out.stderr.contains(".vendor_kit/gen/tools.just (changed)"),
        "{}",
        out.stderr
    );

    fs::remove_file(fx.entry()).unwrap();
    let out = run_check(&fx);
    assert_eq!(codes(&out.stderr), ["VK0047"]);
    assert!(
        out.stderr.contains(".vendor_kit/gen/tools.just (missing)"),
        "{}",
        out.stderr
    );
}

#[test]
fn local_overrides_block_for_tools_and_engine() {
    let fx = Fx::synced(&[&TOOL, &OTHER]);
    fs::write(
        fx.dir.version_local_toml(),
        "vendor_kit = \"ghcr.io/acme/vendor_kit:dev\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"work/tool\"\n",
    )
    .unwrap();
    let out = run_check(&fx);
    assert_eq!(out.code, 2);
    assert_eq!(codes(&out.stderr), ["VK0032", "VK0032"]);
    assert!(
        out.stderr.contains(
            "Test cannot run while a local override of vendor_kit is active. \
             Run: just vendor_kit undev --engine"
        ),
        "{}",
        out.stderr
    );
    assert!(
        out.stderr.contains(
            "Test cannot run while a local override of tool is active. \
             Run: just vendor_kit undev tool"
        ),
        "{}",
        out.stderr
    );
}

#[test]
fn override_without_a_lock_line_is_a_pending_code() {
    let fx = Fx::synced(&[&TOOL]);
    fs::write(
        fx.dir.version_local_toml(),
        "schema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nghost = \"work/ghost\"\n",
    )
    .unwrap();
    let out = run_check(&fx);
    assert_eq!(codes(&out.stderr), ["VK0056", "VK0032"]);
    assert!(out.stderr.contains(DRAFT_ORPHAN_OVERRIDE), "{}", out.stderr);
}

#[test]
fn residual_progress_files_are_reported_and_kept() {
    let fx = Fx::synced(&[&TOOL, &OTHER]);
    fx.progress("add", &["add", "other"], Some(("add", "repo", "other")));
    let out = run_check(&fx);
    assert_eq!(codes(&out.stderr), ["VK0004"]);
    assert!(
        out.stderr
            .contains("Import of other is incomplete. Run: just vendor_kit add other"),
        "{}",
        out.stderr
    );
}

#[test]
fn each_kind_of_residual_progress_file() {
    for (verb, command, field, code) in [
        (
            "upgrade",
            &["upgrade", "tool", "-y"][..],
            Some(("upgrade", "target", "tool")),
            "VK0041",
        ),
        (
            "undev",
            &["undev", "tool"][..],
            Some(("undev", "target", "tool")),
            "VK0053",
        ),
        ("remove", &["remove", "other"][..], None, "VK0054"),
    ] {
        let fx = Fx::synced(&[&TOOL, &OTHER]);
        fx.progress(verb, command, field);
        let out = run_check(&fx);
        assert_eq!(out.code, 2, "{verb}");
        assert_eq!(codes(&out.stderr), [code], "{verb}: {}", out.stderr);
        let full = full_command(command);
        assert!(out.stderr.contains(&full), "{full}\n{}", out.stderr);
    }
}

#[test]
fn a_residual_engine_upgrade_reports_its_target_version() {
    let image = "ghcr.io/ycpss91255-research/vendor_kit:v2.0.0@sha256:2222222222222222222222222222222222222222222222222222222222222222";
    let fx = Fx::synced(&[&TOOL, &OTHER]);
    let mut p = Progress::new("upgrade", "old1", &["upgrade", "--engine", "-y"]).unwrap();
    let doc = p.document_mut();
    doc.set(&["upgrade", "target"], "vendor_kit").unwrap();
    doc.set(&["upgrade", "image"], image).unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();
    let out = run_check(&fx);
    assert_eq!(out.code, 2);
    assert_eq!(codes(&out.stderr), ["VK0023"], "{}", out.stderr);
    // `<vY>` 是進度檔記的目標版，不是本引擎版。
    assert!(
        out.stderr.contains(
            "Engine v2.0.0 is now installed. Run again: just vendor_kit upgrade --engine -y"
        ),
        "{}",
        out.stderr
    );

    // 沒有 `[upgrade] image`：說不出目標版，停下。
    let fx = Fx::synced(&[&TOOL, &OTHER]);
    fx.progress(
        "upgrade",
        &["upgrade", "--engine"],
        Some(("upgrade", "target", "vendor_kit")),
    );
    let out = run_check(&fx);
    assert_eq!(codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(
        out.stderr.contains("without its [upgrade] image field"),
        "{}",
        out.stderr
    );
}

#[test]
fn every_reason_is_listed_before_stopping() {
    let fx = Fx::checkout(&[&TOOL]);
    fs::write(fx.dir.vk_dir().join("log.sh"), "# edited\n").unwrap();
    fx.progress("add", &["add", "tool"], Some(("add", "repo", "tool")));
    let out = run_check(&fx);
    assert_eq!(out.code, 2);
    assert_eq!(codes(&out.stderr), ["VK0006", "VK0004", "VK0047", "VK0047"]);
}

#[test]
fn version_file_too_new_and_not_canonical() {
    let fx = Fx::synced(&[&TOOL]);
    let lock = fs::read_to_string(fx.dir.version_toml()).unwrap();
    fs::write(
        fx.dir.version_toml(),
        lock.replace("schema = 1", "schema = 99"),
    )
    .unwrap();
    let out = run_check(&fx);
    assert_eq!(out.code, 3);
    assert_eq!(codes(&out.stderr), ["VK0008"]);

    fs::write(
        fx.dir.version_toml(),
        lock.replace("vendor_kit_protocols = \"1\"\n", ""),
    )
    .unwrap();
    let out = run_check(&fx);
    assert_eq!(out.code, 2);
    assert_eq!(codes(&out.stderr), ["VK0056"]);
    assert!(out.stderr.contains(DRAFT_NOT_CANONICAL), "{}", out.stderr);
}

#[test]
fn invalid_config_stops_before_anything_else() {
    let fx = Fx::checkout(&[&TOOL]);
    fs::write(fx.dir.config_toml(), "lock_timeout_seconds = -5\n").unwrap();
    let out = run_check(&fx);
    assert_eq!(out.code, 2);
    assert_eq!(codes(&out.stderr), ["VK0059"]);
}

#[test]
fn lock_disabled_warns_and_still_passes() {
    let fx = Fx::synced(&[&TOOL]);
    fs::write(fx.dir.config_toml(), "lock_enabled = false\n").unwrap();
    let out = run_check(&fx);
    assert_eq!(out.code, 1);
    assert_eq!(codes(&out.stderr), ["VK0060"]);
    assert_eq!(out.stdout, format!("{}\n", text::PASSED));
}

#[test]
fn baseline_behind_is_a_gap_while_metadata_exists() {
    let fx = Fx::synced(&[&TOOL]);
    let path = metadata::tool_path(&fx.dir, "tool").unwrap();
    fs::create_dir_all(path.parent().unwrap()).unwrap();
    fs::write(&path, "").unwrap();
    let out = run_check(&fx);
    assert_eq!(codes(&out.stderr), ["VK0056"]);
    assert!(
        out.stderr.contains("VK0014 waits for N3 and N52"),
        "{}",
        out.stderr
    );
}

#[test]
fn missing_shell_templates_is_internal() {
    let fx = Fx::synced(&[]);
    let out = run_with(&fx, None);
    assert_eq!(out.code, 2);
    assert_eq!(codes(&out.stderr), ["VK0056"]);
}

#[test]
fn full_command_quotes_like_posix_shell() {
    assert_eq!(
        full_command(&["upgrade", "it's", "-y"]),
        r"just vendor_kit upgrade 'it'\''s' -y"
    );
}
