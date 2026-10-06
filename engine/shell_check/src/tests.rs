//! 單元測試：只檢查與修復的判定（一致、不符、引擎升級未完成）與修復的寫入範圍。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::collections::BTreeMap;
use std::fs;
use std::path::PathBuf;

use diagnostics::NoSink;
use progress::Progress;

use super::*;

const WRITTEN_BY: &str = "v0.0.0";
const ENGINE: &str = "ghcr.io/acme/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const RUN_LOG: &str = "/srv/proj/.vendor_kit/log/r1.jsonl";

/// 薄殼四檔的模板本文（順序同 `layout::SHELL_FILES`）。
const BODIES: [&str; 4] = ["# entry\n", "# vendor\n", "# log\n", "cache/\ngen/\n"];

const VK0006_FIX: &str = "No shell files were regenerated. Review the following differences; \
     download bootstrap.sh again from the Release, run chmod +x bootstrap.sh, then run \
     ./bootstrap.sh --repair in the install directory.";

fn templates() -> [Vec<u8>; 4] {
    BODIES.map(|b| b.as_bytes().to_vec())
}

/// 已安裝的目錄：版本鎖定行、`gen/.stamp`、這一版的薄殼四檔。
struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
}

impl Fx {
    fn new() -> Fx {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        fs::create_dir_all(dir.vk_dir().join("gen")).unwrap();
        fs::create_dir_all(dir.vk_dir().join("log")).unwrap();
        fs::write(
            dir.version_toml(),
            format!("vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n"),
        )
        .unwrap();
        fs::write(dir.vk_dir().join("gen/.stamp"), "stamp\n").unwrap();
        fs::write(
            tmp.path().join("justfile"),
            "import '.vendor_kit/entry.just'\n",
        )
        .unwrap();
        Fx::shell().write(&dir).unwrap();
        Fx { _tmp: tmp, dir }
    }

    fn shell() -> Shell {
        Shell::render(
            compat::THIS.current_protocol,
            WRITTEN_BY,
            BODIES.map(str::as_bytes),
        )
        .unwrap()
    }

    fn shell_file(&self, name: &str) -> PathBuf {
        self.dir.vk_dir().join(name)
    }

    /// 安裝目錄底下每個檔的路徑與內容。
    fn snapshot(&self) -> BTreeMap<PathBuf, Vec<u8>> {
        let mut out = BTreeMap::new();
        let mut stack = vec![self.dir.root().to_path_buf()];
        while let Some(d) = stack.pop() {
            for e in fs::read_dir(&d).unwrap() {
                let p = e.unwrap().path();
                if p.is_dir() {
                    stack.push(p);
                } else {
                    let rel = p.strip_prefix(self.dir.root()).unwrap().to_path_buf();
                    out.insert(rel, fs::read(&p).unwrap());
                }
            }
        }
        out
    }

    fn progress(&self, verb: &str, command: &[&str], target: Option<&str>) {
        let mut p = Progress::new(verb, "old1", command).unwrap();
        if let Some(t) = target {
            p.document_mut()
                .set(&[progress::upgrade::TABLE, progress::upgrade::TARGET], t)
                .unwrap();
        }
        p.create(&self.dir, WRITTEN_BY).unwrap();
    }

    /// 引擎升級的進度檔；`image` 是 `[upgrade] image`（engine/upgrade 換上的引擎版本鎖定行值）。
    fn engine_progress(&self, command: &[&str], image: Option<&str>) {
        let mut p = Progress::new(progress::upgrade::VERB, "old1", command).unwrap();
        let doc = p.document_mut();
        doc.set(
            &[progress::upgrade::TABLE, progress::upgrade::TARGET],
            progress::upgrade::ENGINE_TARGET,
        )
        .unwrap();
        if let Some(i) = image {
            doc.set(&[progress::upgrade::TABLE, progress::upgrade::IMAGE], i)
                .unwrap();
        }
        p.create(&self.dir, WRITTEN_BY).unwrap();
    }
}

/// 引擎 v2.0.0 的版本鎖定行值。
const ENGINE_V2: &str = "ghcr.io/ycpss91255-research/vendor_kit:v2.0.0@sha256:2222222222222222222222222222222222222222222222222222222222222222";

struct Out {
    code: u8,
    stdout: String,
    stderr: String,
}

fn run_mode(fx: &Fx, mode: Mode, templates: Option<&[Vec<u8>; 4]>) -> Out {
    let mut stdout = Vec::new();
    let mut stderr = Vec::new();
    let mut diags = Diagnostics::with_sink(&mut stderr, NoSink);
    let mut env = Env {
        dir: &fx.dir,
        host_root: "/srv/proj",
        run_log: RUN_LOG,
        written_by: WRITTEN_BY,
        shell_templates: templates,
        stdout: &mut stdout,
        diags: &mut diags,
    };
    let code = run(mode, &mut env);
    Out {
        code,
        stdout: String::from_utf8(stdout).unwrap(),
        stderr: String::from_utf8(stderr).unwrap(),
    }
}

fn check(fx: &Fx) -> Out {
    run_mode(fx, Mode::Check, Some(&templates()))
}

fn repair(fx: &Fx) -> Out {
    run_mode(fx, Mode::Repair, Some(&templates()))
}

// ---- 只檢查 ----

#[test]
fn check_reports_consistent_on_stdout() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let out = check(&fx);
    assert_eq!(out.code, 0);
    assert_eq!(out.stdout, format!("{}\n", text::CONSISTENT));
    assert_eq!(out.stderr, "");
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn check_treats_crlf_as_consistent() {
    let fx = Fx::new();
    let path = fx.shell_file("log.sh");
    let crlf = fs::read_to_string(&path).unwrap().replace('\n', "\r\n");
    fs::write(&path, crlf).unwrap();
    let out = check(&fx);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, format!("{}\n", text::CONSISTENT));
}

#[test]
fn check_reports_vk0006_and_writes_nothing() {
    let fx = Fx::new();
    fs::remove_file(fx.shell_file("vendor.just")).unwrap();
    let mut log = fs::read(fx.shell_file("log.sh")).unwrap();
    log.extend_from_slice(b"echo hi\n");
    fs::write(fx.shell_file("log.sh"), log).unwrap();
    let before = fx.snapshot();
    let out = check(&fx);
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        format!(
            "vendor_kit: error[VK0006]: Shell files do not match this engine version's templates: \
             .vendor_kit/vendor.just (missing), .vendor_kit/log.sh (modified). {VK0006_FIX}\n"
        )
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn check_reports_a_template_of_another_engine_version() {
    let fx = Fx::new();
    let other = shell::render(
        compat::THIS.current_protocol,
        "v9.9.9",
        BODIES[0].as_bytes(),
    )
    .unwrap();
    fs::write(fx.shell_file("entry.just"), other).unwrap();
    let out = check(&fx);
    assert_eq!(out.code, 2);
    assert!(
        out.stderr
            .contains(".vendor_kit/entry.just (not this engine version's template)."),
        "{}",
        out.stderr
    );
}

// ---- 引擎升級未完成 ----

#[test]
fn engine_upgrade_progress_reports_vk0023_without_comparing() {
    for mode in [Mode::Check, Mode::Repair] {
        let fx = Fx::new();
        fs::remove_file(fx.shell_file("log.sh")).unwrap();
        fx.engine_progress(&["upgrade", "--engine=v2.0.0", "-y"], Some(ENGINE_V2));
        let before = fx.snapshot();
        let out = run_mode(&fx, mode, Some(&templates()));
        assert_eq!(out.code, 2, "{mode:?}");
        assert_eq!(out.stdout, "", "{mode:?}");
        // `<vY>` 是進度檔記的目標版，不是本引擎版（第一段還沒換鎖定行就中斷時，跑的仍是舊引擎）。
        assert_eq!(
            out.stderr,
            "vendor_kit: error[VK0023]: Engine v2.0.0 is now installed. Run again: \
             just vendor_kit upgrade --engine=v2.0.0 -y\n",
            "{mode:?}"
        );
        // 不比對也不重產：缺的 log.sh 還是缺，進度檔留著。
        assert_eq!(fx.snapshot(), before, "{mode:?}");
    }
}

#[test]
fn engine_upgrade_progress_without_its_image_is_vk0056() {
    let fx = Fx::new();
    fx.engine_progress(&["upgrade", "--engine"], None);
    let before = fx.snapshot();
    let out = run_mode(&fx, Mode::Repair, Some(&templates()));
    assert_eq!(out.code, 2);
    assert!(
        out.stderr.starts_with("vendor_kit: error[VK0056]: ")
            && out.stderr.contains("without its [upgrade] image field"),
        "{}",
        out.stderr
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn other_progress_files_do_not_block() {
    let fx = Fx::new();
    fx.progress("add", &["add", "lint"], None);
    fx.progress(progress::upgrade::VERB, &["upgrade", "lint"], Some("lint"));
    let out = check(&fx);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, format!("{}\n", text::CONSISTENT));
}

#[test]
fn too_new_progress_file_reports_vk0008() {
    let fx = Fx::new();
    let path = fx
        .dir
        .progress_file(progress::upgrade::VERB, "old1")
        .unwrap();
    fs::write(
        &path,
        "command = [\"upgrade\", \"--engine\"]\nschema = 99\nwritten_by = \"v9.0.0\"\n",
    )
    .unwrap();
    let out = check(&fx);
    assert_eq!(out.code, 3, "{}", out.stderr);
    assert!(
        out.stderr.starts_with("vendor_kit: fatal[VK0008]: "),
        "{}",
        out.stderr
    );
}

// ---- 修復 ----

#[test]
fn repair_regenerates_only_mismatched_files_and_nothing_else() {
    let fx = Fx::new();
    // entry.just 只是行尾變 CRLF：一致，不重產，位元組留著。
    let entry = fx.shell_file("entry.just");
    let crlf = fs::read_to_string(&entry).unwrap().replace('\n', "\r\n");
    fs::write(&entry, &crlf).unwrap();
    fs::remove_file(fx.shell_file("vendor.just")).unwrap();
    fs::write(fx.shell_file("log.sh"), "# hand edited\n").unwrap();
    let before = fx.snapshot();

    let out = repair(&fx);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(
        out.stdout,
        format!(
            "{}\n  .vendor_kit/vendor.just (missing)\n  .vendor_kit/log.sh (modified)\n\
             Regenerated .vendor_kit/vendor.just.\nRegenerated .vendor_kit/log.sh.\n",
            text::DIFFERENCES
        )
    );

    // 只有兩個不符的檔變了；鎖定行、gen/.stamp、根目錄檔、一致的 entry.just 都不動，也沒有新檔。
    let after = fx.snapshot();
    let shell = Fx::shell();
    let mut want = before.clone();
    for name in ["vendor.just", "log.sh"] {
        want.insert(
            PathBuf::from(layout::VK_DIR).join(name),
            shell.file(name).unwrap().to_vec(),
        );
    }
    assert_eq!(after, want);
    assert_eq!(fs::read_to_string(&entry).unwrap(), crlf);

    // 之後再檢查就一致。
    let out = check(&fx);
    assert_eq!(out.code, 0, "{}", out.stderr);
}

#[test]
fn repair_when_consistent_regenerates_nothing() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let out = repair(&fx);
    assert_eq!(out.code, 0);
    assert_eq!(out.stdout, format!("{}\n", text::CONSISTENT));
    assert_eq!(out.stderr, "");
    assert_eq!(fx.snapshot(), before);
}

// ---- 判不了 ----

#[test]
fn missing_templates_is_an_internal_error() {
    let fx = Fx::new();
    for mode in [Mode::Check, Mode::Repair] {
        let out = run_mode(&fx, mode, None);
        assert_eq!(out.code, 2);
        assert!(
            out.stderr.starts_with("vendor_kit: error[VK0056]: "),
            "{}",
            out.stderr
        );
    }
}

#[test]
fn symlinked_shell_file_is_an_internal_error_and_not_followed() {
    let fx = Fx::new();
    let log = fx.shell_file("log.sh");
    let real = fx.dir.root().join("real.sh");
    fs::rename(&log, &real).unwrap();
    std::os::unix::fs::symlink(&real, &log).unwrap();
    let before = fs::read(&real).unwrap();
    let out = repair(&fx);
    assert_eq!(out.code, 2);
    assert!(
        out.stderr.starts_with("vendor_kit: error[VK0056]: "),
        "{}",
        out.stderr
    );
    assert_eq!(fs::read(&real).unwrap(), before);
    assert!(fs::symlink_metadata(&log).unwrap().file_type().is_symlink());
}

#[test]
fn original_command_quotes_like_the_other_commands() {
    assert_eq!(
        original_command(&["upgrade", "--engine=v2.0.0", "a b"]),
        "just vendor_kit upgrade --engine=v2.0.0 'a b'"
    );
}
