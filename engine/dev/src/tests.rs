//! 單元測試：直接在暫存的安裝目錄跑 `dev`、`undev`。驗覆寫與入口檔的寫入、未變更、各拒絕結果與缺口
//! （每個都不寫檔）、殘留進度的恢復，以及路徑正規化。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::ffi::OsString;
use std::path::PathBuf;

use diagnostics::NoSink;

use super::*;

const WRITTEN_BY: &str = "v0.0.0";
const ENGINE: &str = "ghcr.io/acme/vendor_kit:v1.4.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const TOOL: &str = "ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222";
const OTHER: &str = "ghcr.io/acme/other:v1.0.0@sha256:3333333333333333333333333333333333333333333333333333333333333333";
const GEN: &str =
    "mod? other '../cache/other/just/other.just'\nmod? tool '../cache/tool/just/tool.just'\n";
const DEV_GEN: &str = "mod? other '../cache/other/just/other.just'\n\
                       mod? tool '../../dev/tool/just/tool.just'\n\
                       mod? tool-extra '../../dev/tool/just/tool-extra.just'\n";

struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
}

impl Fx {
    /// `tool`、`other` 都已導入並同步好的安裝目錄，另有 `dev/tool/` 這份本機開發來源。
    fn new() -> Fx {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        fs::create_dir_all(dir.vk_dir().join("log")).unwrap();
        fs::write(
            dir.version_toml(),
            format!(
                "vendor_kit = \"{ENGINE}\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nother = \"{OTHER}\"\ntool = \"{TOOL}\"\n"
            ),
        )
        .unwrap();
        for (repo, version) in [("tool", TOOL), ("other", OTHER)] {
            let cache = dir.tool_cache(repo).unwrap();
            fs::create_dir_all(cache.join("just")).unwrap();
            fs::write(cache.join(format!("just/{repo}.just")), "x:\n    echo x\n").unwrap();
            let mut s = stamp::Stamp::compute_tool(&dir, repo, version).unwrap();
            s.save(&stamp::tool_file(&dir, repo), WRITTEN_BY).unwrap();
        }
        fs::create_dir_all(dir.gen_dir()).unwrap();
        fs::write(dir.gen_dir().join(txn::TOOLS_JUST), GEN).unwrap();
        let src = tmp.path().join("dev/tool/just");
        fs::create_dir_all(&src).unwrap();
        fs::write(src.join("tool.just"), "y:\n    echo y\n").unwrap();
        fs::write(src.join("tool-extra.just"), "z:\n    echo z\n").unwrap();
        Fx { _tmp: tmp, dir }
    }

    fn root(&self) -> &Path {
        self.dir.root()
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

    fn entry(&self) -> String {
        fs::read_to_string(self.dir.gen_dir().join(txn::TOOLS_JUST)).unwrap()
    }

    fn local(&self) -> Option<LocalFile> {
        LocalFile::load_from(&self.dir).unwrap()
    }

    fn write_local(&self, body: &str) {
        fs::write(
            self.dir.version_local_toml(),
            format!("schema = 1\nwritten_by = \"v0.0.0\"\n{body}"),
        )
        .unwrap();
    }

    /// 寫一份殘留的進度檔；`fields` 是 `[<verb>]` 下的欄位。
    fn residual(&self, verb: &str, command: &[&str], fields: &[(&str, &str)]) {
        let mut p = Progress::new(verb, "r0", command).unwrap();
        for (key, value) in fields {
            p.document_mut().set(&[verb, key], *value).unwrap();
        }
        p.create(&self.dir, WRITTEN_BY).unwrap();
    }

    fn progress_files(&self) -> Vec<String> {
        progress::find(&self.dir)
            .unwrap()
            .into_iter()
            .map(|e| format!("{}.{}", e.verb, e.id))
            .collect()
    }
}

struct Out {
    code: u8,
    stdout: String,
    stderr: String,
    log: String,
}

impl Out {
    fn events(&self) -> Vec<String> {
        self.log
            .lines()
            .map(|l| {
                let rest = l.split_once("\"event_name\":\"").unwrap().1;
                rest.split_once('"').unwrap().0.to_owned()
            })
            .collect()
    }
}

fn run_with(fx: &Fx, req: &Request<'_>, argv: &[&str]) -> Out {
    let argv: Vec<String> = argv.iter().map(|s| (*s).to_owned()).collect();
    let mut stdout = Vec::new();
    let mut stderr = Vec::new();
    let mut diags = Diagnostics::with_sink(&mut stderr, NoSink);
    let mut log = runlog::Writer::new(
        Vec::new(),
        runlog::Header {
            version: WRITTEN_BY.to_owned(),
            component: runlog::Component::Engine,
            invocation_id: "r1".to_owned(),
        },
    );
    let code = {
        let mut env = Env {
            dir: &fx.dir,
            host_root: "/h/proj",
            run_log: "/h/proj/.vendor_kit/log/r1.jsonl",
            argv: &argv,
            run_id: "r1",
            written_by: WRITTEN_BY,
            stdout: &mut stdout,
            diags: &mut diags,
            log: &mut log,
        };
        run(req, &mut env)
    };
    Out {
        code,
        stdout: String::from_utf8(stdout).unwrap(),
        stderr: String::from_utf8(stderr).unwrap(),
        log: String::from_utf8(log.into_inner()).unwrap(),
    }
}

fn dev(fx: &Fx, repo: &str, path: &str) -> Out {
    let p = OsString::from(path);
    run_with(
        fx,
        &Request::DevTool {
            repo,
            path: p.as_os_str(),
        },
        &["dev", repo, "-p", path],
    )
}

fn undev(fx: &Fx, repo: &str) -> Out {
    run_with(fx, &Request::UndevTool { repo }, &["undev", repo])
}

fn undev_engine(fx: &Fx) -> Out {
    run_with(fx, &Request::UndevEngine, &["undev", "--engine"])
}

fn diag_codes(stderr: &str) -> Vec<&str> {
    stderr
        .lines()
        .filter_map(|l| l.strip_prefix("vendor_kit: "))
        .filter_map(|l| l.split_once('[').map(|(_, rest)| rest))
        .filter_map(|l| l.split_once("]: ").map(|(c, _)| c))
        .collect()
}

const LANDED: [&str; 2] = ["writes_started", "progress_removed"];

// ---- 成功 ----

#[test]
fn dev_points_the_entry_at_the_local_source_and_undev_points_it_back() {
    let fx = Fx::new();
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    let cache = fs::read(fx.dir.tool_cache("tool").unwrap().join("just/tool.just")).unwrap();
    let stamp = fs::read(stamp::tool_file(&fx.dir, "tool")).unwrap();

    let out = dev(&fx, "tool", "./dev/tool/");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(
        out.stdout,
        "tool now uses the local source dev/tool (local override).\n\
         Updated .vendor_kit/gen/tools.just.\n"
    );
    assert_eq!(fx.entry(), DEV_GEN);
    assert_eq!(fx.local().unwrap().tool("tool"), Some("dev/tool"));
    assert_eq!(out.events(), LANDED);
    assert!(fx.progress_files().is_empty());
    // cache/、印記、版本鎖定行都不動。
    assert_eq!(fs::read(fx.dir.version_toml()).unwrap(), lock);
    assert_eq!(
        fs::read(fx.dir.tool_cache("tool").unwrap().join("just/tool.just")).unwrap(),
        cache
    );
    assert_eq!(fs::read(stamp::tool_file(&fx.dir, "tool")).unwrap(), stamp);

    let out = undev(&fx, "tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "Removed the local override of tool; tool uses v1.2.0 ({TOOL}).\n\
             Updated .vendor_kit/gen/tools.just.\n"
        )
    );
    assert_eq!(fx.entry(), GEN);
    assert_eq!(fx.local().unwrap().tool("tool"), None);
    assert_eq!(out.events(), LANDED);
    assert!(fx.progress_files().is_empty());
    assert_eq!(fs::read(fx.dir.version_toml()).unwrap(), lock);
    assert_eq!(fs::read(stamp::tool_file(&fx.dir, "tool")).unwrap(), stamp);
}

#[test]
fn repeated_dev_with_the_same_source_and_undev_without_override_are_unchanged() {
    let fx = Fx::new();
    assert_eq!(dev(&fx, "tool", "dev/tool").code, 0);
    let before = fx.snapshot();

    let out = dev(&fx, "tool", "dev/x/../tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "tool already uses the local source dev/tool. No changes were made.\n"
    );
    assert!(out.events().is_empty());
    assert_eq!(fx.snapshot(), before);

    let out = undev(&fx, "other");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "other has no local override. No changes were made.\n"
    );
    assert!(out.events().is_empty());
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn undev_engine_removes_only_the_engine_override() {
    let fx = Fx::new();
    fx.write_local(
        "vendor_kit = \"ghcr.io/acme/vendor_kit:dev\"\n\n[tools]\ntool = \"dev/tool\"\n",
    );
    let entry = fx.entry();
    let out = undev_engine(&fx);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!("Removed the local override of the engine; the engine uses v1.4.0 ({ENGINE}).\n")
    );
    let local = fx.local().unwrap();
    assert_eq!(local.engine(), None);
    assert_eq!(local.tool("tool"), Some("dev/tool"));
    assert_eq!(fx.entry(), entry);
    assert_eq!(out.events(), LANDED);

    let before = fx.snapshot();
    let out = undev_engine(&fx);
    assert_eq!(
        out.stdout,
        "The engine has no local override. No changes were made.\n"
    );
    assert_eq!(fx.snapshot(), before);
}

// ---- 恢復 ----

#[test]
fn residual_undev_of_the_same_tool_is_completed() {
    let fx = Fx::new();
    // 上一次 undev 已解除覆寫、入口檔還指著本機目錄就斷了。
    fx.write_local("");
    fs::write(fx.dir.gen_dir().join(txn::TOOLS_JUST), DEV_GEN).unwrap();
    fx.residual(UNDEV_VERB, &["undev", "tool"], &[(TARGET_KEY, "tool")]);

    let out = undev(&fx, "tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(fx.entry(), GEN);
    assert!(fx.progress_files().is_empty());
    assert!(
        out.stdout.ends_with(
            "Completed the interrupted undev recorded in .vendor_kit/.tmp.undev.r0.toml.\n"
        ),
        "{}",
        out.stdout
    );
}

#[test]
fn residual_dev_of_the_same_tool_is_completed_before_undev() {
    let fx = Fx::new();
    // 上一次 dev 建好進度檔就斷了：覆寫與入口檔都還沒寫。
    fx.residual(
        DEV_VERB,
        &["dev", "tool", "-p", "dev/tool"],
        &[(TARGET_KEY, "tool"), (PATH_KEY, "dev/tool")],
    );
    let out = dev(&fx, "tool", "dev/tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(fx.entry(), DEV_GEN);
    assert_eq!(fx.local().unwrap().tool("tool"), Some("dev/tool"));
    assert!(fx.progress_files().is_empty());

    // 同樣的殘留改跑 undev：併進來後再解除，回到鎖定版本。
    let fx = Fx::new();
    fx.residual(
        DEV_VERB,
        &["dev", "tool", "-p", "dev/tool"],
        &[(TARGET_KEY, "tool"), (PATH_KEY, "dev/tool")],
    );
    let out = undev(&fx, "tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(fx.entry(), GEN);
    assert!(fx.progress_files().is_empty());
}

#[test]
fn other_residual_progress_stops_before_the_target_check_without_writing() {
    let fx = Fx::new();
    fx.residual("sync", &["sync"], &[]);
    fx.residual(UNDEV_VERB, &["undev", "other"], &[(TARGET_KEY, "other")]);
    let before = fx.snapshot();
    let out = undev(&fx, "missing");
    assert_eq!(out.code, 2);
    assert_eq!(
        diag_codes(&out.stderr),
        ["VK0056", "VK0056"],
        "{}",
        out.stderr
    );
    assert!(
        out.stderr.contains("incomplete sync operation"),
        "{}",
        out.stderr
    );
    assert!(
        out.stderr.contains("incomplete undev of other"),
        "{}",
        out.stderr
    );
    assert!(out.events().is_empty());
    assert_eq!(fx.snapshot(), before);
}

// ---- 拒絕與缺口 ----

#[test]
fn undev_of_a_tool_not_in_the_lock_lines_is_vk0046() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let out = undev(&fx, "missing");
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0046]: Tool missing is not in the lock version lines. The requested operation did not complete.\n"
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn dev_with_a_different_source_is_vk0050() {
    let fx = Fx::new();
    fx.write_local("\n[tools]\ntool = \"elsewhere\"\n");
    let before = fx.snapshot();
    let out = dev(&fx, "tool", "dev/tool");
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0050]: A different local override is already active for tool. Run first: just vendor_kit undev tool\n"
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn dev_with_an_unusable_directory_is_vk0051() {
    let fx = Fx::new();
    fs::create_dir_all(fx.root().join("empty")).unwrap();
    fs::create_dir_all(fx.root().join("wrong/just")).unwrap();
    fs::write(fx.root().join("wrong/just/other-name.just"), "").unwrap();
    fs::write(fx.root().join("file"), "").unwrap();
    let before = fx.snapshot();
    for (path, reason) in [
        ("nowhere", "the directory does not exist"),
        ("file", "it is not a directory"),
        ("wrong", "just/tool.just is missing"),
    ] {
        let out = dev(&fx, "tool", path);
        assert_eq!(out.code, 2, "{path}");
        assert_eq!(
            out.stderr,
            format!(
                "vendor_kit: error[VK0051]: Cannot use local source {path} for tool: {reason}. The local override was not enabled.\n"
            )
        );
    }
    let out = dev(&fx, "tool", "empty");
    assert_eq!(diag_codes(&out.stderr), ["VK0051"], "{}", out.stderr);
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn contract_gaps_stop_with_vk0056_without_writing() {
    let fx = Fx::new();
    std::os::unix::fs::symlink(fx.root().join("dev"), fx.root().join("link")).unwrap();
    let before = fx.snapshot();
    let gaps = [
        (
            dev(&fx, "tool", "/abs/tool"),
            "outside the install directory",
        ),
        (dev(&fx, "tool", "../tool"), "outside the install directory"),
        (dev(&fx, "tool", "link/tool"), "through a symlink (link)"),
        (
            dev(&fx, "missing", "dev/tool"),
            "not in the lock version lines",
        ),
        (
            run_with(
                &fx,
                &Request::DevEngine {
                    image: OsStr::new("vk:dev"),
                },
                &["dev", "--engine", "-i", "vk:dev"],
            ),
            "dev --engine -i vk:dev",
        ),
    ];
    for (out, what) in gaps {
        assert_eq!(out.code, 2, "{what}");
        assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
        assert!(out.stderr.contains(what), "{what}: {}", out.stderr);
        assert!(out.events().is_empty());
    }
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn dev_namespace_collision_is_a_gap() {
    let fx = Fx::new();
    fs::write(fx.root().join("dev/tool/just/other.just"), "").unwrap();
    let before = fx.snapshot();
    let out = dev(&fx, "tool", "dev/tool");
    assert_eq!(out.code, 2);
    assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(
        out.stderr
            .contains("namespace other is delivered by both other and tool"),
        "{}",
        out.stderr
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn undev_when_the_cache_does_not_match_the_lock_line_is_a_gap() {
    let fx = Fx::new();
    assert_eq!(dev(&fx, "tool", "dev/tool").code, 0);
    fs::write(
        fx.dir.tool_cache("tool").unwrap().join("just/tool.just"),
        "changed\n",
    )
    .unwrap();
    let before = fx.snapshot();
    let out = undev(&fx, "tool");
    assert_eq!(out.code, 2);
    assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(
        out.stderr.contains("cache/tool/ does not match"),
        "{}",
        out.stderr
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn another_override_whose_source_is_gone_is_vk0052() {
    let fx = Fx::new();
    fx.write_local("\n[tools]\nother = \"gone\"\n");
    let before = fx.snapshot();
    let out = dev(&fx, "tool", "dev/tool");
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0052]: Cannot read the local override source gone for other: the directory does not exist. Run: just vendor_kit undev other\n"
    );
    assert_eq!(fx.snapshot(), before);
}

// ---- 純函式 ----

#[test]
fn normalize_resolves_against_the_install_directory() {
    let n = |s: &str| normalize(OsStr::new(s));
    assert_eq!(n("dev/tool").unwrap(), "dev/tool");
    assert_eq!(n("./dev//tool/").unwrap(), "dev/tool");
    assert_eq!(n("a/../b").unwrap(), "b");
    assert_eq!(n(".").unwrap(), ".");
    assert_eq!(
        n("").unwrap_err(),
        PathProblem::Unusable("the path is empty".to_owned())
    );
    for bad in ["/abs", "..", "a/../../b", "it's", "a\\b"] {
        assert!(matches!(n(bad), Err(PathProblem::Gap(_))), "{bad:?}");
    }
}

#[test]
fn commands_are_quoted_for_posix_shells() {
    assert_eq!(undev_command("tool"), "just vendor_kit undev tool");
    assert_eq!(
        undev_command(ENGINE_TARGET),
        "just vendor_kit undev --engine"
    );
    assert_eq!(
        full_command(&["dev", "tool", "-p", "my dir"]),
        "just vendor_kit dev tool -p 'my dir'"
    );
}
