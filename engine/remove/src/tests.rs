//! 單元測試：直接在暫存的安裝目錄跑 `remove`、`uninstall`。經執行檔的情況（add 後 remove、VK0046、
//! 答否、同意、VK0061、VK0002）在 test/e2e 的 remove.rs；這裡驗 `uninstall` 的整段、殘留進度的併入、
//! 其他紀錄檔跟著換 hash，與各個停下點。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::io::Cursor;
use std::sync::{Arc, Mutex};

use diagnostics::NoSink;
use metadata::FileHash;

use super::*;

const WRITTEN_BY: &str = "v0.0.0";
const ENGINE: &str = "ghcr.io/acme/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const TOOL: &str = "ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222";
const OTHER: &str = "ghcr.io/acme/other:v1.0.0@sha256:3333333333333333333333333333333333333333333333333333333333333333";
const GITIGNORE: &str = "user-owned\n.tool-cache\n";
const JUSTFILE: &str = "import '.vendor_kit/entry.just'\n\nbuild:\n    echo build\n";
const IMPORT: &str = "import '.vendor_kit/entry.just'";

/// 安裝目錄：`tool` 與 `other` 都已導入；`tool` 在根 `.gitignore` 插入一行，VK 在根 `justfile` 插入 `import`。
struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
}

impl Fx {
    fn new() -> Fx {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        let vk = dir.vk_dir();
        fs::create_dir_all(vk.join("log")).unwrap();
        fs::write(
            dir.version_toml(),
            format!(
                "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nother = \"{OTHER}\"\ntool = \"{TOOL}\"\n"
            ),
        )
        .unwrap();
        for repo in ["tool", "other"] {
            let cache = dir.tool_cache(repo).unwrap();
            fs::create_dir_all(cache.join("just")).unwrap();
            fs::write(cache.join(format!("just/{repo}.just")), "x:\n").unwrap();
            fs::write(stamp::tool_file(&dir, repo), "stamp\n").unwrap();
        }
        fs::create_dir_all(dir.gen_dir()).unwrap();
        fs::write(
            dir.gen_dir().join(txn::TOOLS_JUST),
            "mod? other '../cache/other/just/other.just'\nmod? tool '../cache/tool/just/tool.just'\n",
        )
        .unwrap();
        fs::write(dir.root().join(".gitignore"), GITIGNORE).unwrap();
        fs::write(dir.root().join("justfile"), JUSTFILE).unwrap();
        let fx = Fx { _tmp: tmp, dir };
        fx.record("baseline/tool.toml", ".gitignore", ".tool-cache", GITIGNORE);
        fs::create_dir_all(vk.join("baseline/tool")).unwrap();
        fs::write(vk.join("baseline/tool/.gitignore"), ".tool-cache\n").unwrap();
        fx
    }

    /// 寫一份只有一筆 append 紀錄的逐檔紀錄檔；`hash_of` 是紀錄的整檔 hash 依據的內容。
    fn record(&self, rel: &str, path: &str, line: &str, hash_of: &str) {
        let file = self.dir.vk_dir().join(rel);
        fs::create_dir_all(file.parent().unwrap()).unwrap();
        fs::write(
            file,
            format!(
                "schema = 1\nwritten_by = \"v0.0.0\"\n\n[[file]]\npath = \"{path}\"\nstate = \"appended\"\nlines = [\"{}\"]\nhash = \"{}\"\n",
                line,
                FileHash::of(hash_of.as_bytes())
            ),
        )
        .unwrap();
    }

    fn vk(&self) -> PathBuf {
        self.dir.vk_dir()
    }

    fn read(&self, rel: &str) -> String {
        fs::read_to_string(self.dir.root().join(rel)).unwrap()
    }

    fn lock(&self) -> LockFile {
        LockFile::load_from(&self.dir).unwrap().unwrap()
    }

    fn progress_left(&self) -> Vec<String> {
        progress::find(&self.dir)
            .unwrap()
            .into_iter()
            .map(|e| e.verb)
            .collect()
    }

    /// 寫一份殘留的進度檔。
    fn residual(&self, verb: &str, id: &str, repos: &[&str], repo_files: bool) {
        let mut p = Progress::new(verb, id, &[verb]).unwrap();
        let list: toml_edit::Array = repos.iter().copied().collect();
        p.document_mut().set(&[verb, REPOS_KEY], list).unwrap();
        p.document_mut()
            .set(&[verb, REPO_FILES_KEY], repo_files)
            .unwrap();
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
    /// 詢問與診斷，依序。
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

/// 跑一次；`argv` 的第一個是指令名，`remove` 時第二個是工具名。
fn run(fx: &Fx, argv: &[&str], interactive: bool, input: &str) -> Out {
    let argv: Vec<String> = argv.iter().map(|s| (*s).to_owned()).collect();
    let mut stdin = Cursor::new(input.as_bytes().to_vec());
    let mut stdout = Vec::new();
    let shared = Shared::default();
    let mut prompt = shared.clone();
    let mut diags = Diagnostics::with_sink(shared.clone(), NoSink);
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
            tty: TtyState {
                stdin: interactive,
                stderr: interactive,
            },
            argv: &argv,
            run_id: "r1",
            written_by: WRITTEN_BY,
            stdin: &mut stdin,
            stdout: &mut stdout,
            prompt: &mut prompt,
            diags: &mut diags,
            log: &mut log,
        };
        match argv[0].as_str() {
            REMOVE_VERB => remove(&argv[1], &mut env),
            _ => uninstall(&mut env),
        }
    };
    Out {
        code,
        stdout: String::from_utf8(stdout).unwrap(),
        stderr: shared.text(),
        log: String::from_utf8(log.into_inner()).unwrap(),
    }
}

const LANDED: [&str; 4] = [
    "writes_started",
    "lock_line_write_started",
    "lock_line_written",
    "progress_removed",
];

// ---- remove ----

#[test]
fn remove_keeps_the_other_tool_and_regenerates_the_entry() {
    let fx = Fx::new();
    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "Removed tool v1.2.0 ({TOOL}).\nRemoved inserted lines from .gitignore\nKept .gitignore\n"
        )
    );
    assert_eq!(
        out.stderr,
        "Remove the 1 line that tool appended to .gitignore? [y/N] "
    );
    assert_eq!(out.events(), LANDED);
    assert_eq!(fx.read(".gitignore"), "user-owned\n");
    assert_eq!(
        fx.read(".vendor_kit/gen/tools.just"),
        "mod? other '../cache/other/just/other.just'\n"
    );
    let lock = fx.lock();
    assert!(lock.tool("tool").is_none());
    assert!(lock.tool("other").is_some());
    for gone in [
        "cache/tool",
        "cache/tool.stamp.toml",
        "baseline/tool",
        "baseline/tool.toml",
    ] {
        assert!(!fx.vk().join(gone).exists(), "{gone}");
    }
    assert!(fx.vk().join("cache/other/just/other.just").is_file());
    assert!(fx.vk().join("cache/other.stamp.toml").is_file());
    assert!(fx.progress_left().is_empty());
}

#[test]
fn remove_updates_the_hash_in_other_records_of_the_same_file() {
    let fx = Fx::new();
    // other 也記了同一個 .gitignore（hash 是寫入前的內容），收回後換成寫入後的 hash。
    fx.record("baseline/other.toml", ".gitignore", "user-owned", GITIGNORE);
    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    let other = Metadata::load(&fx.vk().join("baseline/other.toml")).unwrap();
    assert_eq!(
        other.get(".gitignore").unwrap().hash,
        Some(FileHash::of(b"user-owned\n"))
    );
}

#[test]
fn remove_without_records_does_not_ask() {
    let fx = Fx::new();
    fs::remove_file(fx.vk().join("baseline/tool.toml")).unwrap();
    let out = run(&fx, &["remove", "tool"], false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, format!("Removed tool v1.2.0 ({TOOL}).\n"));
    assert_eq!(out.stderr, "");
    assert_eq!(fx.read(".gitignore"), GITIGNORE);
}

#[test]
fn remove_folds_in_a_residual_remove_and_deletes_it_after_landing() {
    let fx = Fx::new();
    // 上一次 remove other 停在版本鎖定行之後、刪進度檔之前：other 已不在版本鎖定行，cache 還在。
    let mut lock = fx.lock();
    lock.remove_tool("other").unwrap();
    lock.save_to(&fx.dir, WRITTEN_BY).unwrap();
    fx.residual(REMOVE_VERB, "r0", &["other"], false);

    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(
        out.stdout
            .contains("Completed the interrupted remove of other.\n")
    );
    assert!(fx.progress_left().is_empty());
    assert!(!fx.vk().join("cache/other").exists());
    assert!(!fx.vk().join("cache/other.stamp.toml").exists());
    assert!(fx.lock().tools().is_empty());
    assert_eq!(fx.read(".vendor_kit/gen/tools.just"), "");
}

#[test]
fn a_residual_remove_of_the_same_tool_is_not_vk0046() {
    let fx = Fx::new();
    let mut lock = fx.lock();
    lock.remove_tool("tool").unwrap();
    lock.save_to(&fx.dir, WRITTEN_BY).unwrap();
    fs::remove_file(fx.vk().join("baseline/tool.toml")).unwrap();
    fx.residual(REMOVE_VERB, "r0", &["tool"], false);

    let out = run(&fx, &["remove", "tool"], false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, "Completed the interrupted remove of tool.\n");
    assert!(!fx.vk().join("cache/tool").exists());
    // 版本鎖定行沒有要改的：不記鎖定行的事件。
    assert_eq!(out.events(), ["writes_started", "progress_removed"]);
    assert!(fx.progress_left().is_empty());
}

#[test]
fn answering_no_keeps_the_residual_progress_file() {
    let fx = Fx::new();
    fx.residual(REMOVE_VERB, "r0", &["other"], false);
    let out = run(&fx, &["remove", "tool"], true, "n\n");
    assert_eq!(out.code, 0);
    assert_eq!(out.stdout, "No changes were made.\n");
    assert_eq!(fx.progress_left(), ["remove"]);
    assert!(fx.vk().join("cache/other").exists());
    assert!(out.events().is_empty());
}

#[test]
fn residuals_that_cannot_be_folded_in_stop_before_any_write() {
    for (verb, repo_files) in [("add", false), ("install", false), (REMOVE_VERB, true)] {
        let fx = Fx::new();
        fx.residual(verb, "r0", &["other"], repo_files);
        let out = run(&fx, &["remove", "tool"], true, "y\n");
        assert_eq!(out.code, 2, "{verb}");
        assert!(
            out.stderr.contains("error[VK0056]"),
            "{verb}: {}",
            out.stderr
        );
        assert!(out.events().is_empty(), "{verb}");
        assert_eq!(fx.read(".gitignore"), GITIGNORE, "{verb}");
        assert!(fx.lock().tool("tool").is_some(), "{verb}");
    }
}

#[test]
fn a_local_override_of_the_target_stops_with_a_gap() {
    let fx = Fx::new();
    let mut local = LocalFile::new();
    local.set_tool("tool", "../tool").unwrap();
    local.save_to(&fx.dir, WRITTEN_BY).unwrap();
    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 2);
    assert!(out.stderr.contains("local override"), "{}", out.stderr);
    assert!(fx.lock().tool("tool").is_some());
}

#[test]
fn a_too_new_record_file_is_vk0008() {
    let fx = Fx::new();
    fs::write(fx.vk().join("baseline/tool.toml"), "schema = 99\n").unwrap();
    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 3);
    assert!(out.stderr.contains("fatal[VK0008]"), "{}", out.stderr);
    assert!(fx.lock().tool("tool").is_some());
}

#[test]
fn an_unreadable_cache_of_a_remaining_tool_stops_before_any_write() {
    let fx = Fx::new();
    fs::remove_dir_all(fx.vk().join("cache/other")).unwrap();
    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 2);
    assert!(
        out.stderr.contains("run just vendor_kit sync first"),
        "{}",
        out.stderr
    );
    assert_eq!(fx.read(".gitignore"), GITIGNORE);
    assert!(out.events().is_empty());
}

#[test]
fn an_appended_record_without_lines_is_a_gap() {
    let fx = Fx::new();
    fs::write(
        fx.vk().join("baseline/tool.toml"),
        "schema = 1\n\n[[file]]\npath = \".gitignore\"\nstate = \"appended\"\n",
    )
    .unwrap();
    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 2);
    assert!(out.stderr.contains("error[VK0056]"), "{}", out.stderr);
    assert!(fx.lock().tool("tool").is_some());
}

// ---- uninstall ----

#[test]
fn uninstall_retracts_vk_state_and_keeps_user_files() {
    let fx = Fx::new();
    fx.record("baseline/.vendor_kit.toml", "justfile", IMPORT, JUSTFILE);
    for shell in layout::SHELL_FILES {
        fs::write(fx.vk().join(shell), "shell\n").unwrap();
    }
    let mut local = LocalFile::new();
    local.set_tool("other", "../other-src").unwrap();
    local.save_to(&fx.dir, WRITTEN_BY).unwrap();
    fs::write(fx.dir.config_toml(), "lock_timeout_seconds = 5\n").unwrap();
    fs::write(fx.vk().join("notes.txt"), "mine\n").unwrap();

    let out = run(&fx, &["uninstall"], true, "y\ny\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stderr,
        "Remove the 1 line that tool appended to .gitignore? [y/N] \
         Remove the 1 line that vendor_kit appended to justfile? [y/N] "
    );
    assert_eq!(
        out.stdout,
        "Uninstalled vendor_kit from /h/proj.\n\
         Removed inserted lines from .gitignore\n\
         Removed inserted lines from justfile\n\
         Kept .gitignore\n\
         Kept justfile\n\
         Kept the local development source of other: ../other-src\n\
         Kept .vendor_kit/config.toml\n\
         Kept .vendor_kit/log/\n\
         Kept .vendor_kit/notes.txt\n"
    );
    assert_eq!(out.events(), LANDED);
    assert_eq!(fx.read(".gitignore"), "user-owned\n");
    assert_eq!(fx.read("justfile"), "\nbuild:\n    echo build\n");
    let mut left: Vec<String> = fs::read_dir(fx.vk())
        .unwrap()
        .map(|e| e.unwrap().file_name().to_string_lossy().into_owned())
        .collect();
    left.sort();
    assert_eq!(left, ["config.toml", "log", "notes.txt"]);
}

/// `install` 建的 `config.toml` 記成 `managed`：保留清單只列一次，基準版副本跟著 `baseline/` 刪掉。
#[test]
fn uninstall_lists_a_managed_config_toml_once() {
    let fx = Fx::new();
    let config = "# lock_timeout_seconds = 60\n";
    fs::write(fx.dir.config_toml(), config).unwrap();
    let copy = fx.dir.config_baseline();
    fs::create_dir_all(copy.parent().unwrap()).unwrap();
    fs::write(&copy, config).unwrap();
    fs::write(
        fx.dir.baseline_vk(),
        format!(
            "schema = 1\nwritten_by = \"v0.0.0\"\n\n[[file]]\npath = \".vendor_kit/config.toml\"\nstate = \"managed\"\nhash = \"{}\"\n",
            FileHash::of(config.as_bytes())
        ),
    )
    .unwrap();

    let out = run(&fx, &["uninstall"], true, "y\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout.matches("Kept .vendor_kit/config.toml\n").count(),
        1,
        "{}",
        out.stdout
    );
    assert_eq!(fx.read(".vendor_kit/config.toml"), config);
    assert!(!fx.dir.baseline_dir().exists());
}

#[test]
fn uninstall_answering_no_changes_nothing() {
    let fx = Fx::new();
    let out = run(&fx, &["uninstall"], true, "n\n");
    assert_eq!(out.code, 0);
    assert_eq!(out.stdout, "No changes were made.\n");
    assert!(fx.dir.version_toml().is_file());
    assert_eq!(fx.read(".gitignore"), GITIGNORE);
    assert!(out.events().is_empty());
}

#[test]
fn uninstall_without_a_terminal_is_vk0002() {
    let fx = Fx::new();
    let out = run(&fx, &["uninstall"], false, "");
    assert_eq!(out.code, 2);
    assert!(
        out.stderr
            .ends_with("rerun with -y: just vendor_kit uninstall -y\n"),
        "{}",
        out.stderr
    );
    assert!(fx.dir.version_toml().is_file());
}

#[test]
fn uninstall_folds_in_residual_uninstall_and_remove() {
    let fx = Fx::new();
    fs::remove_file(fx.vk().join("baseline/tool.toml")).unwrap();
    fx.residual(UNINSTALL_VERB, "r0", &["other", "tool"], false);
    fx.residual(REMOVE_VERB, "r00", &["gone"], false);
    let out = run(&fx, &["uninstall"], false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(fx.progress_left().is_empty());
    assert!(!fx.dir.version_toml().exists());
}

#[test]
fn uninstall_lists_lines_it_cannot_retract() {
    let fx = Fx::new();
    fs::write(
        fx.dir.root().join(".gitignore"),
        "user-owned\n.tool-cache\nmore\n",
    )
    .unwrap();
    let out = run(&fx, &["uninstall"], false, "");
    assert_eq!(out.code, 1, "{}", out.stderr);
    assert!(
        out.stderr.starts_with("vendor_kit: warn[VK0061]: "),
        "{}",
        out.stderr
    );
    assert!(
        out.stderr.contains("Currently matching line numbers: 2."),
        "{}",
        out.stderr
    );
    assert_eq!(fx.read(".gitignore"), "user-owned\n.tool-cache\nmore\n");
    assert!(!fx.dir.version_toml().exists());
}

#[test]
fn line_numbers_are_listed_or_none() {
    assert_eq!(text::line_numbers(&[]), "none");
    assert_eq!(text::line_numbers(&[2]), "2");
    assert_eq!(text::line_numbers(&[2, 5]), "2, 5");
}
