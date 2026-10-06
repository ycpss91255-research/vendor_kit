//! 單元測試：直接在暫存的安裝目錄跑 `remove`、`uninstall`。經執行檔的情況（add 後 remove、VK0046、
//! 答否、同意、VK0061、VK0002）在 test/e2e 的 remove.rs；這裡驗 `uninstall` 的整段、殘留進度的併入、
//! 其他紀錄檔跟著換 hash，與各個停下點。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::io::Cursor;
use std::sync::{Arc, Mutex};

use plan::{Header, RunId};

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
    with_env(fx, "r1", &argv, interactive, input, |env| {
        match argv[0].as_str() {
            REMOVE_VERB => remove(&argv[1], env),
            _ => uninstall(env),
        }
    })
}

/// 以 `run_id` 這次執行的環境跑 `f`。
fn with_env(
    fx: &Fx,
    run_id: &str,
    argv: &[String],
    interactive: bool,
    input: &str,
    f: impl FnOnce(&mut Env<'_, Shared, NoSink, Vec<u8>>) -> u8,
) -> Out {
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
    // 安裝目錄裡的覆寫不送 request；這裡沒有假啟動器，送了就等不到 result。
    let ctl = fx._tmp.path().join("ctl");
    let inbox = fx._tmp.path().join("in");
    let mut channel = Channel::new(&ctl, Header::new(1, RunId::parse(run_id).unwrap()).unwrap());
    let code = {
        let mut env = Env {
            dir: &fx.dir,
            host_root: "/h/proj",
            run_log: "/h/proj/.vendor_kit/log/r1.jsonl",
            inbox: &inbox,
            channel: &mut channel,
            poll: Duration::from_millis(1),
            tty: TtyState {
                stdin: interactive,
                stderr: interactive,
            },
            argv,
            run_id,
            written_by: WRITTEN_BY,
            stdin: &mut stdin,
            stdout: &mut stdout,
            prompt: &mut prompt,
            diags: &mut diags,
            log: &mut log,
        };
        f(&mut env)
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

/// 寫 `version.local.toml`：`tools` 是 `(repo, 本機開發來源)`。
fn write_local(fx: &Fx, tools: &[(&str, &str)]) {
    let mut local = LocalFile::new();
    for (repo, dir) in tools {
        local.set_tool(repo, dir).unwrap();
    }
    local.save_to(&fx.dir, WRITTEN_BY).unwrap();
}

/// 安裝目錄裡的本機開發來源 `work/other`：交付 `other` 與 `other-extra`。
const OTHER_SOURCE: &str = "work/other";

fn other_source(fx: &Fx) {
    let just = fx.dir.root().join(OTHER_SOURCE).join("just");
    fs::create_dir_all(&just).unwrap();
    fs::write(just.join("other.just"), "y:\n").unwrap();
    fs::write(just.join("other-extra.just"), "z:\n").unwrap();
}

/// `other` 開著覆寫（[`OTHER_SOURCE`]）時的入口檔。
const OTHER_LOCAL_ENTRY: &str = "mod? other '../../work/other/just/other.just'\n\
                                 mod? other-extra '../../work/other/just/other-extra.just'\n";

/// 用了 `other` 的覆寫的報告。
const OTHER_REPORT: &str = "other uses the local source work/other (local override).\n";

fn local_tools(fx: &Fx) -> Vec<(String, String)> {
    let local = LocalFile::load_from(&fx.dir).unwrap().unwrap();
    local
        .tools()
        .iter()
        .map(|(r, d)| (r.clone(), d.clone()))
        .collect()
}

#[test]
fn a_local_override_of_the_target_is_lifted_and_its_source_is_kept() {
    let fx = Fx::new();
    // 對象的來源不存在（覆寫來源失效）也不擋；其他工具的覆寫照留。
    other_source(&fx);
    write_local(&fx, &[("tool", "../gone"), ("other", OTHER_SOURCE)]);
    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "{OTHER_REPORT}\
             Removed tool v1.2.0 ({TOOL}).\n\
             Removed the local override of tool (../gone).\n\
             Kept the local development source of tool: ../gone\n\
             Removed inserted lines from .gitignore\nKept .gitignore\n"
        )
    );
    assert_eq!(out.events(), LANDED);
    assert_eq!(
        local_tools(&fx),
        [("other".to_owned(), OTHER_SOURCE.to_owned())]
    );
    assert_eq!(fx.read(".vendor_kit/gen/tools.just"), OTHER_LOCAL_ENTRY);
    assert!(fx.lock().tool("tool").is_none());
    assert!(!fx.vk().join("cache/tool").exists());
    assert!(fx.progress_left().is_empty());
}

#[test]
fn lifting_the_last_override_keeps_version_local_toml() {
    let fx = Fx::new();
    write_local(&fx, &[("tool", "../tool")]);
    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(fx.dir.version_local_toml().is_file());
    assert!(local_tools(&fx).is_empty());
}

#[test]
fn an_override_of_another_tool_is_applied_reported_and_left_untouched() {
    // 對象以外的覆寫：入口檔照本機開發來源重產、報告用了它，`version.local.toml` 不動。
    let fx = Fx::new();
    other_source(&fx);
    write_local(&fx, &[("other", OTHER_SOURCE)]);
    let before = fs::read(fx.dir.version_local_toml()).unwrap();
    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "{OTHER_REPORT}Removed tool v1.2.0 ({TOOL}).\n\
             Removed inserted lines from .gitignore\nKept .gitignore\n"
        )
    );
    assert_eq!(fx.read(".vendor_kit/gen/tools.just"), OTHER_LOCAL_ENTRY);
    assert_eq!(fs::read(fx.dir.version_local_toml()).unwrap(), before);
}

#[test]
fn answering_no_still_reports_the_override_of_another_tool() {
    let fx = Fx::new();
    other_source(&fx);
    write_local(&fx, &[("other", OTHER_SOURCE)]);
    let out = run(&fx, &["remove", "tool"], true, "n\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, format!("{OTHER_REPORT}No changes were made.\n"));
    assert!(out.events().is_empty());
}

#[test]
fn an_unreadable_override_of_another_tool_is_vk0052_before_asking() {
    // 重產入口檔要讀它（04 本機覆寫：覆寫來源失效只擋需讀它的動作）：在詢問與任何寫入之前停下。
    let fx = Fx::new();
    write_local(&fx, &[("other", "work/gone")]);
    let entry = fx.read(".vendor_kit/gen/tools.just");
    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0052]: Cannot read the local override source work/gone for other: \
         the directory does not exist. Run: just vendor_kit undev other\n"
    );
    assert_eq!(fx.read(".gitignore"), GITIGNORE);
    assert_eq!(fx.read(".vendor_kit/gen/tools.just"), entry);
    assert!(fx.lock().tool("tool").is_some());
    assert!(out.events().is_empty());
}

#[test]
fn an_orphan_override_of_another_tool_is_a_gap() {
    let fx = Fx::new();
    other_source(&fx);
    write_local(&fx, &[("ghost", OTHER_SOURCE)]);
    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 2);
    assert!(out.stderr.contains("error[VK0056]"), "{}", out.stderr);
    assert!(out.stderr.contains("ghost"), "{}", out.stderr);
    assert!(fx.lock().tool("tool").is_some());
    assert!(out.events().is_empty());
}

#[test]
fn answering_no_keeps_the_override() {
    let fx = Fx::new();
    write_local(&fx, &[("tool", "../tool")]);
    let before = fs::read(fx.dir.version_local_toml()).unwrap();
    let out = run(&fx, &["remove", "tool"], true, "n\n");
    assert_eq!(out.code, 0);
    assert_eq!(out.stdout, "No changes were made.\n");
    assert_eq!(fs::read(fx.dir.version_local_toml()).unwrap(), before);
    assert!(out.events().is_empty());
}

#[test]
fn recovery_after_the_override_was_lifted_removes_the_lock_line() {
    // 半套一：上一次停在紀錄檔之後、版本鎖定行之前：覆寫已解除，鎖定行還在。
    let fx = Fx::new();
    write_local(&fx, &[]);
    fs::remove_dir_all(fx.vk().join("cache/tool")).unwrap();
    fx.residual(REMOVE_VERB, "r0", &["tool"], false);
    fs::remove_file(fx.vk().join("baseline/tool.toml")).unwrap();

    let out = run(&fx, &["remove", "tool"], false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, format!("Removed tool v1.2.0 ({TOOL}).\n"));
    assert!(fx.lock().tool("tool").is_none());
    assert!(local_tools(&fx).is_empty());
    assert!(fx.progress_left().is_empty());
}

#[test]
fn recovery_after_the_lock_line_was_removed_lifts_the_override() {
    // 半套二：鎖定行已拿掉、覆寫還在，殘留的 remove 記著對象。
    let fx = Fx::new();
    let mut lock = fx.lock();
    lock.remove_tool("tool").unwrap();
    lock.save_to(&fx.dir, WRITTEN_BY).unwrap();
    fs::remove_file(fx.vk().join("baseline/tool.toml")).unwrap();
    other_source(&fx);
    write_local(&fx, &[("tool", "../tool"), ("other", OTHER_SOURCE)]);
    fx.residual(REMOVE_VERB, "r0", &["tool"], false);

    let out = run(&fx, &["remove", "tool"], false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "other uses the local source work/other (local override).\n\
         Completed the interrupted remove of tool.\n\
         Removed the local override of tool (../tool).\n\
         Kept the local development source of tool: ../tool\n"
    );
    assert_eq!(
        local_tools(&fx),
        [("other".to_owned(), OTHER_SOURCE.to_owned())]
    );
    assert!(!fx.vk().join("cache/tool").exists());
    // 版本鎖定行沒有要改的：不記鎖定行的事件。
    assert_eq!(out.events(), ["writes_started", "progress_removed"]);
    assert!(fx.progress_left().is_empty());
}

#[test]
fn an_orphan_override_without_a_residual_is_vk0046() {
    let fx = Fx::new();
    let mut lock = fx.lock();
    lock.remove_tool("tool").unwrap();
    lock.save_to(&fx.dir, WRITTEN_BY).unwrap();
    write_local(&fx, &[("tool", "../tool")]);
    let before = fs::read(fx.dir.version_local_toml()).unwrap();
    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 2);
    assert!(out.stderr.contains("error[VK0046]"), "{}", out.stderr);
    assert_eq!(fs::read(fx.dir.version_local_toml()).unwrap(), before);
    assert!(out.events().is_empty());
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

/// 自相矛盾的逐檔紀錄（#372 N86）：每份紀錄檔一則 VK0013，不收回、不寫任何檔。
#[test]
fn a_self_contradictory_record_is_vk0013() {
    let records = [
        // appended 卻沒有 lines。
        "schema = 1\n\n[[file]]\npath = \".gitignore\"\nstate = \"appended\"\n",
        // 非 appended 卻有 lines。
        "schema = 1\n\n[[file]]\npath = \".gitignore\"\nstate = \"managed\"\nlines = [\"x\"]\n",
    ];
    for record in records {
        let fx = Fx::new();
        fs::write(fx.vk().join("baseline/tool.toml"), record).unwrap();
        let out = run(&fx, &["remove", "tool"], true, "y\n");
        assert_eq!(out.code, 2);
        assert_eq!(
            out.stderr,
            "vendor_kit: error[VK0013]: Cannot process .vendor_kit/baseline/tool.toml: metadata is missing \
             or corrupt and cannot be restored reliably. vendor_kit does not guess when records are \
             unavailable; no files of the tool that .vendor_kit/baseline/tool.toml belongs to were \
             modified. Preserve .vendor_kit/baseline/tool.toml and run log /h/proj/.vendor_kit/log/r1.jsonl. \
             If the metadata was committed to Git, restore it from Git and retry. Otherwise, report the \
             issue at https://github.com/ycpss91255-research/vendor_kit/issues and attach both files.\n"
        );
        assert_eq!(fx.read(".gitignore"), GITIGNORE);
        assert!(fx.lock().tool("tool").is_some());
        assert!(out.events().is_empty());
    }
}

/// `uninstall` 也一樣，只報有矛盾紀錄的那幾份，在詢問之前停下。
#[test]
fn uninstall_reports_each_self_contradictory_record_file() {
    let fx = Fx::new();
    fx.record("baseline/.vendor_kit.toml", "justfile", IMPORT, JUSTFILE);
    fs::write(
        fx.vk().join("baseline/tool.toml"),
        "schema = 1\n\n[[file]]\npath = \".gitignore\"\nstate = \"appended\"\n",
    )
    .unwrap();
    let out = run(&fx, &["uninstall"], true, "y\ny\n");
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr.matches("error[VK0013]").count(),
        1,
        "{}",
        out.stderr
    );
    assert!(
        out.stderr
            .contains("Cannot process .vendor_kit/baseline/tool.toml:"),
        "{}",
        out.stderr
    );
    assert!(!out.stderr.contains("[y/N]"), "{}", out.stderr);
    assert_eq!(fx.read(".gitignore"), GITIGNORE);
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

// ---- 照進度檔記的 repo 檔恢復（#372 N47、N95）----

/// 以真的 `remove <repo>`／`uninstall` 判定（同意全部收回）建一份殘留進度檔（id `r0`），回傳它記的 repo 檔。
/// 之後由測試自己做「中斷前已寫的部分」。
fn interrupted(fx: &Fx, argv: &[&str]) -> Vec<WrittenFile> {
    let argv: Vec<String> = argv.iter().map(|s| (*s).to_owned()).collect();
    let verb = if argv[0] == REMOVE_VERB {
        REMOVE_VERB
    } else {
        UNINSTALL_VERB
    };
    let out = with_env(fx, "r0", &argv, false, "", |env| {
        let mut run = Run::new(env);
        let (records, targets) = if verb == REMOVE_VERB {
            let Ok(path) = run.tool_metadata(&argv[1]) else {
                panic!("metadata path")
            };
            let metadata = Metadata::load(&path).unwrap();
            let owner = Owner::Tool(argv[1].clone());
            let records = vec![Record {
                owner,
                path,
                metadata,
            }];
            (records, BTreeSet::from([argv[1].clone()]))
        } else {
            let Ok(records) = run.all_records() else {
                panic!("records")
            };
            let targets = BTreeSet::from(["other".to_owned(), "tool".to_owned()]);
            (records, targets)
        };
        let Ok(plan) = run.plan(&records, &[]) else {
            panic!("plan")
        };
        let Ok(mut p) = run.progress(verb, &targets, &plan) else {
            panic!("progress")
        };
        p.create(&fx.dir, WRITTEN_BY).unwrap();
        0
    });
    assert_eq!(out.stderr, "");
    let p = progress::load(&fx.dir, verb, "r0").unwrap().unwrap();
    assert_eq!(
        p.document()
            .get(&[verb, REPO_FILES_KEY])
            .and_then(|i| i.as_bool()),
        Some(true)
    );
    repo_files::read(&p).unwrap().unwrap()
}

#[test]
fn the_progress_file_records_the_repo_files_to_write() {
    let fx = Fx::new();
    let files = interrupted(&fx, &["remove", "tool"]);
    assert_eq!(
        files,
        [WrittenFile::new(
            ".gitignore",
            Some(GITIGNORE.as_bytes()),
            b"user-owned\n"
        )]
    );
    assert_eq!(files[0].action, repo_files::Action::Modify);
}

#[test]
fn an_interrupted_remove_is_completed_from_its_recorded_repo_files() {
    let fx = Fx::new();
    fx.record("baseline/other.toml", ".gitignore", "user-owned", GITIGNORE);
    interrupted(&fx, &["remove", "tool"]);
    // 上一次停在寫完 repo 檔之後：紀錄檔、cache、版本鎖定行都還沒動。重新判定會因整檔 hash 變了
    // 報 VK0061；照記錄算做完。
    fs::write(fx.dir.root().join(".gitignore"), "user-owned\n").unwrap();

    let out = run(&fx, &["remove", "tool"], false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(
        out.stdout,
        format!("Removed tool v1.2.0 ({TOOL}).\nKept .gitignore\n")
    );
    assert_eq!(fx.read(".gitignore"), "user-owned\n");
    // other 的紀錄補上那次該換的 hash。
    let other = Metadata::load(&fx.vk().join("baseline/other.toml")).unwrap();
    assert_eq!(
        other.get(".gitignore").unwrap().hash,
        Some(FileHash::of(b"user-owned\n"))
    );
    for gone in ["cache/tool", "baseline/tool", "baseline/tool.toml"] {
        assert!(!fx.vk().join(gone).exists(), "{gone}");
    }
    assert!(fx.lock().tool("tool").is_none());
    assert!(fx.progress_left().is_empty());
}

#[test]
fn a_recorded_repo_file_not_yet_written_is_judged_as_usual() {
    let fx = Fx::new();
    fx.record("baseline/other.toml", ".gitignore", "user-owned", GITIGNORE);
    interrupted(&fx, &["remove", "tool"]);

    let out = run(&fx, &["remove", "tool"], true, "y\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stderr,
        "Remove the 1 line that tool appended to .gitignore? [y/N] "
    );
    assert!(
        out.stdout
            .contains("Removed inserted lines from .gitignore\n")
    );
    assert_eq!(fx.read(".gitignore"), "user-owned\n");
    let other = Metadata::load(&fx.vk().join("baseline/other.toml")).unwrap();
    assert_eq!(
        other.get(".gitignore").unwrap().hash,
        Some(FileHash::of(b"user-owned\n"))
    );
    assert!(fx.progress_left().is_empty());
}

#[test]
fn a_recorded_repo_file_changed_after_the_interruption_is_judged_as_usual() {
    let fx = Fx::new();
    interrupted(&fx, &["remove", "tool"]);
    // 收回之後使用者又改了：不是那次寫的內容，照常判定，只列不刪是真的。
    fs::write(fx.dir.root().join(".gitignore"), "user-owned\nmine\n").unwrap();

    let out = run(&fx, &["remove", "tool"], false, "");
    assert_eq!(out.code, 1, "{}", out.stderr);
    assert!(
        out.stderr.starts_with("vendor_kit: warn[VK0061]: "),
        "{}",
        out.stderr
    );
    assert_eq!(fx.read(".gitignore"), "user-owned\nmine\n");
    assert!(fx.progress_left().is_empty());
}

#[test]
fn an_interrupted_uninstall_is_completed_from_its_recorded_repo_files() {
    let fx = Fx::new();
    fx.record("baseline/.vendor_kit.toml", "justfile", IMPORT, JUSTFILE);
    let files = interrupted(&fx, &["uninstall"]);
    let paths: Vec<&str> = files.iter().map(|f| f.path.as_str()).collect();
    assert_eq!(paths, [".gitignore", "justfile"]);
    // 上一次只寫完 .gitignore：justfile 還是寫入前的樣子，照常判定、照常問。
    fs::write(fx.dir.root().join(".gitignore"), "user-owned\n").unwrap();

    let out = run(&fx, &["uninstall"], true, "y\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(!out.stderr.contains("VK0061"), "{}", out.stderr);
    assert!(!out.stderr.contains(".gitignore"), "{}", out.stderr);
    assert!(out.stderr.contains("justfile"), "{}", out.stderr);
    assert_eq!(fx.read(".gitignore"), "user-owned\n");
    assert_eq!(fx.read("justfile"), "\nbuild:\n    echo build\n");
    assert!(!fx.dir.version_toml().exists());
    assert!(fx.progress_left().is_empty());
}
