//! 單元測試：直接在暫存的安裝目錄跑 `install`。經執行檔的情況（空 repo、再跑一次、install → add →
//! remove → uninstall、根 `justfile` 已有內容時的詢問與答否）在 test/e2e 的 install.rs；這裡驗各個判定、
//! 殘留進度的併入、其他紀錄檔跟著換 hash，與各個停下點。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::io::Cursor;
use std::sync::{Arc, Mutex};

use diagnostics::NoSink;

use super::*;

const WRITTEN_BY: &str = "v0.0.0";
const ENGINE: &str = "ghcr.io/acme/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const OTHER_ENGINE: &str = "ghcr.io/acme/vendor_kit:v0.9.0@sha256:9999999999999999999999999999999999999999999999999999999999999999";
const TOOL: &str = "ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222";
const IMPORT: &str = "import '.vendor_kit/entry.just'";
const DEFAULT: &str = "default:\n    @just --list\n";
const BODIES: [&str; 4] = [
    "# entry\nimport? 'vendor.just'\n",
    "# vendor\nmod vendor_kit\n",
    "# log\nlog() { :; }\n",
    "cache/\ngen/\nlog/\nversion.local.toml\n.tmp.*\n",
];
const DOCKERIGNORE_LINES: [&str; 2] = [".vendor_kit/cache/", ".vendor_kit/log/"];

fn release() -> Release {
    Release {
        engine: Some(ImageRef::parse(ENGINE).unwrap()),
        shell: Some(BODIES.map(|b| b.as_bytes().to_vec())),
        justfile_import: Some(IMPORT.to_owned()),
        justfile_default: Some(DEFAULT.to_owned()),
        dockerignore: Some(DOCKERIGNORE_LINES.map(str::to_owned).to_vec()),
    }
}

/// 啟動器起引擎前的樣子：只有 `.vendor_kit/log/`。
struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
}

impl Fx {
    fn new() -> Fx {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        fs::create_dir_all(dir.log_dir()).unwrap();
        Fx { _tmp: tmp, dir }
    }

    fn vk(&self) -> PathBuf {
        self.dir.vk_dir()
    }

    fn write(&self, rel: &str, contents: &str) {
        let path = self.dir.root().join(rel);
        fs::create_dir_all(path.parent().unwrap()).unwrap();
        fs::write(path, contents).unwrap();
    }

    fn read(&self, rel: &str) -> String {
        fs::read_to_string(self.dir.root().join(rel)).unwrap()
    }

    fn exists(&self, rel: &str) -> bool {
        self.dir.root().join(rel).exists()
    }

    fn progress_left(&self) -> Vec<String> {
        progress::find(&self.dir)
            .unwrap()
            .into_iter()
            .map(|e| e.verb)
            .collect()
    }

    fn residual(&self, verb: &str, id: &str, repo_files: bool) {
        let mut p = Progress::new(verb, id, &[verb]).unwrap();
        p.document_mut()
            .set(&[verb, REPO_FILES_KEY], repo_files)
            .unwrap();
        p.create(&self.dir, WRITTEN_BY).unwrap();
    }

    /// `.vendor_kit/` 下所有路徑（相對、排序），不含 `log/`。
    fn tree(&self) -> Vec<String> {
        fn walk(root: &Path, dir: &Path, out: &mut Vec<String>) {
            for entry in fs::read_dir(dir).unwrap() {
                let path = entry.unwrap().path();
                out.push(path.strip_prefix(root).unwrap().display().to_string());
                if path.is_dir() {
                    walk(root, &path, out);
                }
            }
        }
        let mut out = Vec::new();
        walk(&self.vk(), &self.vk(), &mut out);
        out.retain(|p| p != "log" && !p.starts_with("log/"));
        out.sort();
        out
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

fn run_with(fx: &Fx, release: &Release, yes: bool, interactive: bool, input: &str) -> Out {
    let argv: Vec<String> = if yes {
        vec!["install".to_owned(), "-y".to_owned()]
    } else {
        vec!["install".to_owned()]
    };
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
        run(&Request { yes, release }, &mut env)
    };
    Out {
        code,
        stdout: String::from_utf8(stdout).unwrap(),
        stderr: shared.text(),
        log: String::from_utf8(log.into_inner()).unwrap(),
    }
}

fn run_install(fx: &Fx, interactive: bool, input: &str) -> Out {
    run_with(fx, &release(), false, interactive, input)
}

const LANDED: [&str; 4] = [
    "writes_started",
    "lock_line_write_started",
    "lock_line_written",
    "progress_removed",
];
const LANDED_NO_LOCK: [&str; 2] = ["writes_started", "progress_removed"];

fn shell_file(i: usize) -> Vec<u8> {
    shell::render(
        compat::THIS.current_protocol,
        WRITTEN_BY,
        BODIES[i].as_bytes(),
    )
    .unwrap()
}

fn vk_record(fx: &Fx, path: &str) -> FileRecord {
    Metadata::load(&metadata::vk_path(&fx.dir))
        .unwrap()
        .get(path)
        .unwrap()
        .clone()
}

// ---- 首次導入 ----

#[test]
fn fresh_install_writes_the_skeleton_without_asking() {
    let fx = Fx::new();
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(
        out.stdout,
        format!(
            "Locked the engine to v1.0.0 ({ENGINE}).\n\
             Wrote .vendor_kit/entry.just\nWrote .vendor_kit/vendor.just\n\
             Wrote .vendor_kit/log.sh\nWrote .vendor_kit/.gitignore\n\
             Created justfile\nCreated .dockerignore\n\
             Installed vendor_kit {WRITTEN_BY} in /h/proj.\n"
        )
    );
    assert_eq!(out.events(), LANDED);
    assert_eq!(
        fx.tree(),
        [
            ".gitignore",
            "baseline",
            "baseline/.vendor_kit.toml",
            "entry.just",
            "log.sh",
            "vendor.just",
            "version.toml",
        ]
    );
    let lock = LockFile::load_from(&fx.dir).unwrap().unwrap();
    assert_eq!(lock.engine().to_string(), ENGINE);
    assert!(lock.tools().is_empty());
    for (i, name) in layout::SHELL_FILES.iter().enumerate() {
        assert_eq!(
            fs::read(fx.vk().join(name)).unwrap(),
            shell_file(i),
            "{name}"
        );
    }
    let justfile = format!("{IMPORT}\n\n{DEFAULT}");
    assert_eq!(fx.read(JUSTFILE), justfile);
    assert_eq!(
        fx.read(DOCKERIGNORE),
        ".vendor_kit/cache/\n.vendor_kit/log/\n"
    );
    let r = vk_record(&fx, JUSTFILE);
    assert_eq!(r.state, State::Appended);
    assert_eq!(r.lines, [IMPORT]);
    assert_eq!(r.hash, Some(FileHash::of(justfile.as_bytes())));
    let r = vk_record(&fx, DOCKERIGNORE);
    assert_eq!(r.lines, DOCKERIGNORE_LINES);
    assert!(fx.progress_left().is_empty());
}

#[test]
fn second_install_changes_nothing() {
    let fx = Fx::new();
    assert_eq!(run_install(&fx, false, "").code, 0);
    let before = fx.tree();
    let toml = fx.read(".vendor_kit/version.toml");
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "vendor_kit is already installed in /h/proj; no changes were made.\n"
    );
    assert_eq!(out.stderr, "");
    assert!(out.events().is_empty());
    assert_eq!(fx.tree(), before);
    assert_eq!(fx.read(".vendor_kit/version.toml"), toml);
}

#[test]
fn crlf_checkout_of_the_shell_changes_nothing() {
    let fx = Fx::new();
    assert_eq!(run_install(&fx, false, "").code, 0);
    let mut crlf = Vec::new();
    for name in layout::SHELL_FILES {
        let path = fx.vk().join(name);
        let text = String::from_utf8(fs::read(&path).unwrap()).unwrap();
        let converted = text.replace('\n', "\r\n");
        fs::write(&path, &converted).unwrap();
        crlf.push(converted);
    }
    let before = fx.tree();
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "vendor_kit is already installed in /h/proj; no changes were made.\n"
    );
    assert!(out.events().is_empty());
    assert_eq!(fx.tree(), before);
    for (name, converted) in layout::SHELL_FILES.iter().zip(&crlf) {
        let contents = fs::read(fx.vk().join(name)).unwrap();
        assert_eq!(contents, converted.as_bytes(), "{name}");
    }
}

// ---- 使用者既有的根目錄檔 ----

const USER_JUSTFILE: &str = "build:\n    echo build\n";
const USER_DOCKERIGNORE: &str = "target/";

#[test]
fn existing_root_files_are_appended_after_asking() {
    let fx = Fx::new();
    fx.write(JUSTFILE, USER_JUSTFILE);
    fx.write(DOCKERIGNORE, USER_DOCKERIGNORE);
    let out = run_install(&fx, true, "y\nyes\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stderr,
        "Append 1 vendor_kit line to the existing justfile? [y/N] \
         Append 2 vendor_kit lines to the existing .dockerignore? [y/N] "
    );
    assert!(
        out.stdout
            .contains("Appended to justfile\nAppended to .dockerignore\n")
    );
    let justfile = format!("{USER_JUSTFILE}{IMPORT}\n");
    assert_eq!(fx.read(JUSTFILE), justfile);
    // 最後一行沒有換行時先補一個（initfiles 的 append）。
    let dockerignore = "target/\n.vendor_kit/cache/\n.vendor_kit/log/\n";
    assert_eq!(fx.read(DOCKERIGNORE), dockerignore);
    let r = vk_record(&fx, JUSTFILE);
    assert_eq!(r.lines, [IMPORT]);
    assert_eq!(r.hash, Some(FileHash::of(justfile.as_bytes())));
    assert_eq!(
        vk_record(&fx, DOCKERIGNORE).hash,
        Some(FileHash::of(dockerignore.as_bytes()))
    );
}

#[test]
fn answering_no_writes_nothing() {
    let fx = Fx::new();
    fx.write(JUSTFILE, USER_JUSTFILE);
    let out = run_install(&fx, true, "n\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, "No changes were made.\n");
    assert!(out.events().is_empty());
    assert_eq!(fx.read(JUSTFILE), USER_JUSTFILE);
    assert!(fx.tree().is_empty());
    assert!(!fx.exists(DOCKERIGNORE));
}

#[test]
fn not_interactive_without_yes_is_vk0002() {
    let fx = Fx::new();
    fx.write(JUSTFILE, USER_JUSTFILE);
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert!(
        out.stderr.starts_with("vendor_kit: error[VK0002]: ")
            && out.stderr.contains("just vendor_kit install -y"),
        "{}",
        out.stderr
    );
    assert!(out.events().is_empty());
    assert_eq!(fx.read(JUSTFILE), USER_JUSTFILE);
    assert!(fx.tree().is_empty());
}

#[test]
fn yes_appends_without_asking() {
    let fx = Fx::new();
    fx.write(JUSTFILE, USER_JUSTFILE);
    let out = run_with(&fx, &release(), true, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(fx.read(JUSTFILE), format!("{USER_JUSTFILE}{IMPORT}\n"));
}

#[test]
fn root_file_that_already_has_the_line_without_a_record_stops() {
    let fx = Fx::new();
    fx.write(JUSTFILE, &format!("{IMPORT}\n{USER_JUSTFILE}"));
    let out = run_install(&fx, true, "y\ny\n");
    assert_eq!(out.code, 2);
    assert!(
        out.stderr.starts_with("vendor_kit: error[VK0056]: ") && out.stderr.contains("justfile"),
        "{}",
        out.stderr
    );
    assert!(out.events().is_empty());
    assert!(fx.tree().is_empty());
}

#[test]
fn other_tool_records_of_the_same_file_follow_the_new_hash() {
    let fx = Fx::new();
    let fresh = run_install(&fx, false, "");
    assert_eq!(fresh.code, 0, "{}", fresh.stderr);
    // 已導入 tool，tool 在 .dockerignore 插入過一行；VK 的紀錄不見了（例如被使用者刪掉）。
    let mut lock = LockFile::load_from(&fx.dir).unwrap().unwrap();
    lock.set_tool("tool", &ImageRef::parse(TOOL).unwrap())
        .unwrap();
    lock.save_to(&fx.dir, WRITTEN_BY).unwrap();
    let ignore = "target/\n.tool\n";
    fx.write(DOCKERIGNORE, ignore);
    let mut tool = Metadata::new();
    let mut r = FileRecord::new(DOCKERIGNORE, State::Appended);
    r.lines = vec![".tool".to_owned()];
    r.hash = Some(FileHash::of(ignore.as_bytes()));
    tool.put(r).unwrap();
    tool.save(&metadata::tool_path(&fx.dir, "tool").unwrap(), WRITTEN_BY)
        .unwrap();
    let mut vk = Metadata::load(&metadata::vk_path(&fx.dir)).unwrap();
    let justfile_record = vk.get(JUSTFILE).unwrap().clone();
    vk = Metadata::new();
    vk.put(justfile_record).unwrap();
    vk.save(&metadata::vk_path(&fx.dir), WRITTEN_BY).unwrap();

    let out = run_install(&fx, true, "y\n");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.events(), LANDED_NO_LOCK);
    let after = "target/\n.tool\n.vendor_kit/cache/\n.vendor_kit/log/\n";
    assert_eq!(fx.read(DOCKERIGNORE), after);
    let tool = Metadata::load(&metadata::tool_path(&fx.dir, "tool").unwrap()).unwrap();
    assert_eq!(
        tool.get(DOCKERIGNORE).unwrap().hash,
        Some(FileHash::of(after.as_bytes()))
    );
}

// ---- 既有安裝目錄 ----

#[test]
fn existing_lock_line_is_kept_and_shell_is_rewritten() {
    let fx = Fx::new();
    assert_eq!(run_install(&fx, false, "").code, 0);
    let mut lock = LockFile::load_from(&fx.dir).unwrap().unwrap();
    lock.set_engine(&ImageRef::parse(OTHER_ENGINE).unwrap())
        .unwrap();
    lock.save_to(&fx.dir, WRITTEN_BY).unwrap();
    fx.write(".vendor_kit/vendor.just", "changed\n");
    fs::remove_file(fx.vk().join("log.sh")).unwrap();

    // 出貨輸入沒有引擎行也不用：沿用既有的。
    let mut r = release();
    r.engine = None;
    let out = run_with(&fx, &r, false, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "Wrote .vendor_kit/vendor.just\nWrote .vendor_kit/log.sh\n\
             Installed vendor_kit {WRITTEN_BY} in /h/proj.\n"
        )
    );
    assert_eq!(out.events(), LANDED_NO_LOCK);
    let lock = LockFile::load_from(&fx.dir).unwrap().unwrap();
    assert_eq!(lock.engine().to_string(), OTHER_ENGINE);
    assert_eq!(
        fs::read(fx.vk().join("vendor.just")).unwrap(),
        shell_file(1)
    );
    assert_eq!(fs::read(fx.vk().join("log.sh")).unwrap(), shell_file(2));
}

#[test]
fn shipped_release_stops_and_lists_every_missing_input() {
    let fx = Fx::new();
    let out = run_with(&fx, &Release::shipped(), false, false, "");
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert!(
        out.stderr.starts_with("vendor_kit: error[VK0056]: "),
        "{}",
        out.stderr
    );
    for item in [
        "the engine lock line value",
        "the shell templates",
        "the root justfile import line",
        "the default recipe of a new root justfile",
        "the root .dockerignore lines",
    ] {
        assert!(out.stderr.contains(item), "{item}: {}", out.stderr);
    }
    assert!(out.events().is_empty());
    assert!(fx.tree().is_empty());
}

#[test]
fn too_new_version_file_is_vk0008() {
    let fx = Fx::new();
    fx.write(
        ".vendor_kit/version.toml",
        &format!("vendor_kit = \"{ENGINE}\"\nschema = 99\nwritten_by = \"v9.0.0\"\n"),
    );
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 3);
    assert!(
        out.stderr.starts_with("vendor_kit: fatal[VK0008]: "),
        "{}",
        out.stderr
    );
    assert!(out.events().is_empty());
}

// ---- 恢復 ----

#[test]
fn residual_install_is_completed_and_removed() {
    let fx = Fx::new();
    fx.residual(INSTALL_VERB, "r0", false);
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(out.stdout.contains("Completed the interrupted install.\n"));
    assert!(fx.progress_left().is_empty());

    // 全部都已對齊時，殘留的進度檔照樣經 txn 刪掉。
    fx.residual(INSTALL_VERB, "r2", false);
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.events(), LANDED_NO_LOCK);
    assert!(fx.progress_left().is_empty());
}

#[test]
fn residual_of_another_verb_or_with_repo_files_stops() {
    for (verb, repo_files) in [("add", false), (INSTALL_VERB, true)] {
        let fx = Fx::new();
        fx.residual(verb, "r0", repo_files);
        let out = run_install(&fx, false, "");
        assert_eq!(out.code, 2, "{verb}");
        assert!(
            out.stderr.starts_with("vendor_kit: error[VK0056]: "),
            "{}",
            out.stderr
        );
        assert!(out.events().is_empty());
        assert_eq!(fx.progress_left(), [verb]);
        assert!(!fx.exists(JUSTFILE));
    }
}

/// 寫一份殘留的 `install` 進度檔，記它要寫的根 `justfile`（寫入後內容是 `after`）。
fn residual_with_justfile(fx: &Fx, after: &str) {
    let mut p = Progress::new(INSTALL_VERB, "r0", &["install"]).unwrap();
    let mut t = toml_edit::InlineTable::new();
    t.insert(PATH_KEY, JUSTFILE.into());
    let lines: toml_edit::Array = [IMPORT].into_iter().collect();
    t.insert(LINES_KEY, lines.into());
    t.insert(HASH_KEY, FileHash::of(after.as_bytes()).as_str().into());
    let files: toml_edit::Array = [toml_edit::Value::from(t)].into_iter().collect();
    p.document_mut()
        .set(&[INSTALL_VERB, REPO_FILES_KEY], true)
        .unwrap();
    p.document_mut()
        .set(&[INSTALL_VERB, FILES_KEY], files)
        .unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();
}

#[test]
fn interrupted_first_install_after_writing_root_files_is_completed() {
    let fx = Fx::new();
    // 上一次首次導入寫完根 justfile 就斷了：進度檔還在，紀錄、薄殼、版本鎖定行都沒寫。
    let justfile = format!("{IMPORT}\n\n{DEFAULT}");
    fx.write(JUSTFILE, &justfile);
    residual_with_justfile(&fx, &justfile);

    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(out.events(), LANDED);
    assert!(out.stdout.contains("Completed the interrupted install.\n"));
    assert!(!out.stdout.contains("justfile"), "{}", out.stdout);
    assert_eq!(fx.read(JUSTFILE), justfile);
    let r = vk_record(&fx, JUSTFILE);
    assert_eq!(r.lines, [IMPORT]);
    assert_eq!(r.hash, Some(FileHash::of(justfile.as_bytes())));
    assert!(fx.exists(".vendor_kit/version.toml"));
    assert!(fx.progress_left().is_empty());

    // 補好之後再跑：沒有變更。
    let out = run_install(&fx, false, "");
    assert!(
        out.stdout.contains("no changes were made"),
        "{}",
        out.stdout
    );
}

#[test]
fn interrupted_install_whose_file_changed_afterwards_stops() {
    let fx = Fx::new();
    let justfile = format!("{IMPORT}\n\n{DEFAULT}");
    fx.write(JUSTFILE, &format!("{justfile}user:\n    echo user\n"));
    residual_with_justfile(&fx, &justfile);

    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 2);
    assert!(
        out.stderr.starts_with("vendor_kit: error[VK0056]: "),
        "{}",
        out.stderr
    );
    assert!(out.events().is_empty());
    assert_eq!(fx.progress_left(), [INSTALL_VERB]);
}

#[test]
fn interrupted_install_before_writing_root_files_plans_them_again() {
    let fx = Fx::new();
    // 進度檔記了要寫的根 justfile，但那次還沒寫到：照常新建。
    residual_with_justfile(&fx, &format!("{IMPORT}\n\n{DEFAULT}"));
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(out.stdout.contains("Created justfile\n"), "{}", out.stdout);
    assert_eq!(fx.read(JUSTFILE), format!("{IMPORT}\n\n{DEFAULT}"));
    assert!(fx.progress_left().is_empty());
}

#[test]
fn progress_records_each_root_file_written() {
    let fx = Fx::new();
    let edits = [RootEdit {
        path: JUSTFILE,
        before: None,
        after: b"x\n".to_vec(),
        ask: false,
        lines: vec![IMPORT.to_owned()],
    }];
    let argv = vec!["install".to_owned()];
    let mut stdin = Cursor::new(Vec::new());
    let (mut stdout, mut prompt) = (Vec::new(), Vec::new());
    let mut diags = Diagnostics::with_sink(Vec::new(), NoSink);
    let mut log = runlog::Writer::new(
        Vec::new(),
        runlog::Header {
            version: WRITTEN_BY.to_owned(),
            component: runlog::Component::Engine,
            invocation_id: "r1".to_owned(),
        },
    );
    let mut env = Env {
        dir: &fx.dir,
        host_root: "/h/proj",
        run_log: "log",
        tty: TtyState::default(),
        argv: &argv,
        run_id: "r1",
        written_by: WRITTEN_BY,
        stdin: &mut stdin,
        stdout: &mut stdout,
        prompt: &mut prompt,
        diags: &mut diags,
        log: &mut log,
    };
    let mut run = Run {
        env: &mut env,
        code: 0,
    };
    let Ok(p) = run.progress(&edits) else {
        panic!("progress");
    };
    let files = p
        .document()
        .get(&[INSTALL_VERB, FILES_KEY])
        .and_then(|i| i.as_array())
        .unwrap();
    let got: Vec<Written> = files.iter().map(|v| written(v).unwrap()).collect();
    assert_eq!(
        got,
        [Written {
            path: JUSTFILE.to_owned(),
            lines: vec![IMPORT.to_owned()],
            hash: FileHash::of(b"x\n"),
        }]
    );
}

// ---- 出貨輸入 ----

#[test]
fn release_reads_back_from_a_directory() {
    let tmp = tempfile::tempdir().unwrap();
    let d = tmp.path();
    assert_eq!(Release::from_dir(d).unwrap(), Release::shipped());
    fs::write(d.join(release::ENGINE_FILE), format!("{ENGINE}\n")).unwrap();
    fs::create_dir(d.join(release::SHELL_DIR)).unwrap();
    for (name, body) in layout::SHELL_FILES.iter().zip(BODIES) {
        fs::write(d.join(release::SHELL_DIR).join(name), body).unwrap();
    }
    fs::write(d.join(release::JUSTFILE_IMPORT_FILE), format!("{IMPORT}\n")).unwrap();
    fs::write(d.join(release::JUSTFILE_DEFAULT_FILE), DEFAULT).unwrap();
    fs::write(
        d.join(release::DOCKERIGNORE_FILE),
        DOCKERIGNORE_LINES.join("\n"),
    )
    .unwrap();
    assert_eq!(Release::from_dir(d).unwrap(), release());

    fs::write(d.join(release::ENGINE_FILE), "a\nb\n").unwrap();
    assert!(Release::from_dir(d).is_err());
}
