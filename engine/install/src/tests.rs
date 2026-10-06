//! 單元測試：直接在暫存的安裝目錄跑 `install`。經執行檔的情況（空 repo、再跑一次、install → add →
//! remove → uninstall、根 `justfile` 已有內容時的詢問與答否）在 test/e2e 的 install.rs；這裡驗各個判定、
//! 殘留進度的併入、其他紀錄檔跟著換 hash，與各個停下點。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::io::Cursor;
use std::sync::{Arc, Mutex};

use diagnostics::NoSink;

use super::*;

const WRITTEN_BY: &str = "v0.0.0";
/// 啟動器放在 `in/engine` 的引用：本 repo 的引擎、tag 是 [`WRITTEN_BY`]。
const ENGINE: &str = "ghcr.io/ycpss91255-research/vendor_kit:v0.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
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
/// 判定邏輯用的 `config.toml` 模板，跟出貨的常數無關（常數另驗）。
const CONFIG: &str = "# lock_timeout_seconds = 60\n";

/// 判定邏輯用的出貨輸入：`.dockerignore` 故意只給兩行，跟出貨的常數無關（常數另驗）。
fn release() -> Release {
    Release {
        shell: Some(BODIES.map(|b| b.as_bytes().to_vec())),
        justfile_import: IMPORT.to_owned(),
        justfile_default: DEFAULT.to_owned(),
        dockerignore: DOCKERIGNORE_LINES.map(str::to_owned).to_vec(),
        config: CONFIG.to_owned(),
    }
}

/// 啟動器起引擎前的樣子：安裝目錄只有 `.vendor_kit/log/`；收件目錄有引擎引用檔。
struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
    _in: tempfile::TempDir,
    inbox: PathBuf,
}

impl Fx {
    fn new() -> Fx {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        fs::create_dir_all(dir.log_dir()).unwrap();
        let inn = tempfile::tempdir().unwrap();
        let inbox = inn.path().to_owned();
        let fx = Fx {
            _tmp: tmp,
            dir,
            _in: inn,
            inbox,
        };
        fx.engine_ref(&format!("{ENGINE}\n"));
        fx
    }

    /// 改寫收件目錄的引擎引用檔。
    fn engine_ref(&self, contents: &str) {
        fs::write(self.inbox.join(plan::files::IN_ENGINE), contents).unwrap();
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
            inbox: &fx.inbox,
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
            "Locked the engine to v0.0.0 ({ENGINE}).\n\
             Wrote .vendor_kit/entry.just\nWrote .vendor_kit/vendor.just\n\
             Wrote .vendor_kit/log.sh\nWrote .vendor_kit/.gitignore\n\
             Created justfile\nCreated .dockerignore\nCreated .vendor_kit/config.toml\n\
             Installed vendor_kit {WRITTEN_BY} in /h/proj.\n"
        )
    );
    assert_eq!(out.events(), LANDED);
    assert_eq!(
        fx.tree(),
        [
            ".gitignore",
            "baseline",
            "baseline/.vendor_kit",
            "baseline/.vendor_kit.toml",
            "baseline/.vendor_kit/config.toml",
            "config.toml",
            "entry.just",
            "gen",
            "gen/.stamp",
            "log.sh",
            "vendor.just",
            "version.toml",
        ]
    );
    let lock = LockFile::load_from(&fx.dir).unwrap().unwrap();
    assert_eq!(lock.engine().to_string(), ENGINE);
    assert_eq!(fx.read(".vendor_kit/gen/.stamp"), format!("{ENGINE}\n"));
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
    assert_config_managed(&fx);
    assert!(fx.progress_left().is_empty());
}

/// `config.toml` 是模板原樣，`baseline/.vendor_kit.toml` 記 `managed` 與它的 hash，基準版副本也是模板。
fn assert_config_managed(fx: &Fx) {
    assert_eq!(fx.read(CONFIG_TOML), CONFIG);
    let r = vk_record(fx, CONFIG_TOML);
    assert_eq!(r.state, State::Managed);
    assert!(r.lines.is_empty());
    assert_eq!(r.hash, Some(FileHash::of(CONFIG.as_bytes())));
    assert_eq!(
        fs::read_to_string(fx.dir.config_baseline()).unwrap(),
        CONFIG
    );
}

// ---- config.toml ----

/// 使用者已有自己的 `config.toml`、VK 沒有它的紀錄：不碰、不記、不存副本（04：目標不存在才新建）。
#[test]
fn existing_config_toml_without_a_record_is_left_alone() {
    let fx = Fx::new();
    fx.write(CONFIG_TOML, "lock_timeout_seconds = 5\n");
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert!(!out.stdout.contains("config.toml"), "{}", out.stdout);
    assert_eq!(fx.read(CONFIG_TOML), "lock_timeout_seconds = 5\n");
    let vk = Metadata::load(&metadata::vk_path(&fx.dir)).unwrap();
    assert!(vk.get(CONFIG_TOML).is_none());
    assert!(!fx.dir.config_baseline().exists());
}

/// 已納管的 `config.toml` 被使用者刪了：不重建（換版與合併歸 `upgrade`），什麼都不改。
#[test]
fn deleted_managed_config_toml_is_not_recreated() {
    let fx = Fx::new();
    assert_eq!(run_install(&fx, false, "").code, 0);
    fs::remove_file(fx.dir.config_toml()).unwrap();
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "vendor_kit is already installed in /h/proj; no changes were made.\n"
    );
    assert!(!fx.exists(CONFIG_TOML));
}

/// 使用者改過已納管的 `config.toml`：`install` 不動它，也不動紀錄。
#[test]
fn edited_managed_config_toml_is_kept() {
    let fx = Fx::new();
    assert_eq!(run_install(&fx, false, "").code, 0);
    fx.write(CONFIG_TOML, "lock_enabled = true\n");
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(out.events().is_empty());
    assert_eq!(fx.read(CONFIG_TOML), "lock_enabled = true\n");
    assert_eq!(
        vk_record(&fx, CONFIG_TOML).hash,
        Some(FileHash::of(CONFIG.as_bytes()))
    );
}

/// `config.toml` 是 symlink 時也算已有東西：不寫穿過去。
#[cfg(unix)]
#[test]
fn config_toml_symlink_is_left_alone() {
    let fx = Fx::new();
    std::os::unix::fs::symlink("elsewhere.toml", fx.dir.config_toml()).unwrap();
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(!fx.exists("elsewhere.toml"));
    assert!(!fx.exists(".vendor_kit/elsewhere.toml"));
    assert!(!fx.dir.config_baseline().exists());
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

/// 新 checkout 沒有 `gen/`（不進 git）：只補 `gen/.stamp`，其他不動。
#[test]
fn checkout_without_gen_only_writes_the_stamp() {
    let fx = Fx::new();
    assert_eq!(run_install(&fx, false, "").code, 0);
    let before = fx.tree();
    let toml = fx.read(".vendor_kit/version.toml");
    fs::remove_dir_all(fx.dir.gen_dir()).unwrap();
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!("Installed vendor_kit {WRITTEN_BY} in /h/proj.\n")
    );
    assert_eq!(out.stderr, "");
    assert_eq!(fx.tree(), before);
    assert_eq!(fx.read(".vendor_kit/version.toml"), toml);
    assert_eq!(fx.read(".vendor_kit/gen/.stamp"), format!("{ENGINE}\n"));
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

    // 既有安裝目錄不讀引擎引用檔：沿用既有的鎖定行。
    fs::remove_file(fx.inbox.join(plan::files::IN_ENGINE)).unwrap();
    let out = run_install(&fx, false, "");
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
    // `gen/.stamp` 記沿用的鎖定行，不是本引擎的引用檔。
    assert_eq!(
        fx.read(".vendor_kit/gen/.stamp"),
        format!("{OTHER_ENGINE}\n")
    );
    assert_eq!(
        fs::read(fx.vk().join("vendor.just")).unwrap(),
        shell_file(1)
    );
    assert_eq!(fs::read(fx.vk().join("log.sh")).unwrap(), shell_file(2));
}

#[test]
fn release_without_shell_templates_stops() {
    let fx = Fx::new();
    let out = run_with(&fx, &Release::without_shell(), false, false, "");
    assert_eq!(out.code, 2);
    assert_eq!(out.stdout, "");
    assert!(
        out.stderr.starts_with(
            "vendor_kit: error[VK0056]: Internal vendor_kit error: \
             install without the shell templates, which this engine image does not ship"
        ),
        "{}",
        out.stderr
    );
    assert!(out.events().is_empty());
    assert!(fx.tree().is_empty());
}

/// 首次導入時引擎引用檔不合：VK0056 寫明哪裡不一致，什麼都不寫。
fn bad_engine_ref(contents: Option<&str>, reason: &str) {
    let fx = Fx::new();
    match contents {
        Some(c) => fx.engine_ref(c),
        None => fs::remove_file(fx.inbox.join(plan::files::IN_ENGINE)).unwrap(),
    }
    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 2, "{}", out.stderr);
    assert_eq!(out.stdout, "");
    assert!(
        out.stderr.starts_with(
            "vendor_kit: error[VK0056]: Internal vendor_kit error: \
             the engine reference in/engine from the launcher"
        ) && out.stderr.contains(reason),
        "{reason}: {}",
        out.stderr
    );
    assert!(out.events().is_empty());
    assert!(fx.tree().is_empty());
    assert!(!fx.exists(JUSTFILE));
    assert!(!fx.exists(DOCKERIGNORE));
}

#[test]
fn missing_engine_ref_is_vk0056_without_writes() {
    bad_engine_ref(None, "is missing");
}

#[test]
fn engine_ref_that_is_not_one_pinned_line_is_vk0056_without_writes() {
    bad_engine_ref(Some(""), "engine must be exactly one line");
    bad_engine_ref(Some(&format!("{ENGINE}\n{ENGINE}\n")), "exactly one line");
    bad_engine_ref(
        Some("ghcr.io/ycpss91255-research/vendor_kit:v0.0.0\n"),
        "is not a pinned reference",
    );
}

#[test]
fn engine_ref_of_another_repo_is_vk0056_without_writes() {
    bad_engine_ref(
        Some(&format!("{OTHER_ENGINE}\n")),
        "names ghcr.io/acme/vendor_kit, not this engine's ghcr.io/ycpss91255-research/vendor_kit",
    );
}

#[test]
fn engine_ref_of_another_version_is_vk0056_without_writes() {
    let other = ENGINE.replace(":v0.0.0@", ":v1.0.0@");
    bad_engine_ref(
        Some(&format!("{other}\n")),
        "has tag v1.0.0, not this engine's v0.0.0",
    );
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

/// 寫一份殘留的 `install` 進度檔，記它要寫的每個 repo 檔：路徑、行、寫入後的內容。
fn residual_with_files(fx: &Fx, files: &[(&str, &[&str], &str)]) {
    let mut p = Progress::new(INSTALL_VERB, "r0", &["install"]).unwrap();
    let files: toml_edit::Array = files
        .iter()
        .map(|(path, lines, after)| {
            let mut t = toml_edit::InlineTable::new();
            t.insert(PATH_KEY, (*path).into());
            let lines: toml_edit::Array = lines.iter().copied().collect();
            t.insert(LINES_KEY, lines.into());
            t.insert(HASH_KEY, FileHash::of(after.as_bytes()).as_str().into());
            toml_edit::Value::from(t)
        })
        .collect();
    p.document_mut()
        .set(&[INSTALL_VERB, REPO_FILES_KEY], true)
        .unwrap();
    p.document_mut()
        .set(&[INSTALL_VERB, FILES_KEY], files)
        .unwrap();
    p.create(&fx.dir, WRITTEN_BY).unwrap();
}

#[test]
fn interrupted_first_install_after_writing_config_toml_is_completed() {
    let fx = Fx::new();
    // 上一次首次導入寫完 repo 檔（含 config.toml）就斷了：紀錄、基準版副本、薄殼、版本鎖定行都沒寫。
    let justfile = format!("{IMPORT}\n\n{DEFAULT}");
    let ignore = ".vendor_kit/cache/\n.vendor_kit/log/\n";
    fx.write(JUSTFILE, &justfile);
    fx.write(DOCKERIGNORE, ignore);
    fx.write(CONFIG_TOML, CONFIG);
    residual_with_files(
        &fx,
        &[
            (JUSTFILE, &[IMPORT], &justfile),
            (DOCKERIGNORE, &DOCKERIGNORE_LINES, ignore),
            (CONFIG_TOML, &[], CONFIG),
        ],
    );

    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(out.events(), LANDED);
    assert!(out.stdout.contains("Completed the interrupted install.\n"));
    assert!(!out.stdout.contains("Created"), "{}", out.stdout);
    assert_config_managed(&fx);
    assert!(fx.progress_left().is_empty());

    let out = run_install(&fx, false, "");
    assert!(
        out.stdout.contains("no changes were made"),
        "{}",
        out.stdout
    );
}

/// 斷掉之後使用者又改了 `config.toml`：那次寫的已認不出來，照「已有、沒有紀錄」不碰、不記。
#[test]
fn interrupted_install_whose_config_toml_changed_afterwards_leaves_it_alone() {
    let fx = Fx::new();
    fx.write(CONFIG_TOML, "lock_timeout_seconds = 5\n");
    residual_with_files(&fx, &[(CONFIG_TOML, &[], CONFIG)]);

    let out = run_install(&fx, false, "");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(fx.read(CONFIG_TOML), "lock_timeout_seconds = 5\n");
    let vk = Metadata::load(&metadata::vk_path(&fx.dir)).unwrap();
    assert!(vk.get(CONFIG_TOML).is_none());
    assert!(!fx.dir.config_baseline().exists());
    assert!(fx.progress_left().is_empty());
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
    let edits = [
        RootEdit {
            path: JUSTFILE,
            before: None,
            after: b"x\n".to_vec(),
            ask: false,
            lines: vec![IMPORT.to_owned()],
        },
        RootEdit {
            path: CONFIG_TOML,
            before: None,
            after: b"y\n".to_vec(),
            ask: false,
            lines: Vec::new(),
        },
    ];
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
        inbox: &fx.inbox,
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
        [
            Written {
                path: JUSTFILE.to_owned(),
                lines: vec![IMPORT.to_owned()],
                hash: FileHash::of(b"x\n"),
            },
            Written {
                path: CONFIG_TOML.to_owned(),
                lines: Vec::new(),
                hash: FileHash::of(b"y\n"),
            },
        ]
    );
}

// ---- 出貨輸入 ----

#[test]
fn release_reads_back_from_a_directory() {
    let tmp = tempfile::tempdir().unwrap();
    let d = tmp.path();
    assert_eq!(Release::from_dir(d).unwrap(), Release::without_shell());
    fs::create_dir(d.join(release::SHELL_DIR)).unwrap();
    for (name, body) in layout::SHELL_FILES.iter().zip(BODIES) {
        fs::write(d.join(release::SHELL_DIR).join(name), body).unwrap();
    }
    assert_eq!(
        Release::from_dir(d).unwrap(),
        Release {
            shell: Some(BODIES.map(|b| b.as_bytes().to_vec())),
            ..Release::without_shell()
        }
    );
    fs::remove_file(d.join(release::SHELL_DIR).join(layout::SHELL_FILES[3])).unwrap();
    assert_eq!(Release::from_dir(d).unwrap(), Release::without_shell());
}

/// 根目錄檔的逐字內容（04 草稿照這裡寫；改了要同步改 04）。
#[test]
fn shipped_root_file_contents_are_pinned() {
    let r = Release::without_shell();
    assert_eq!(r.shell, None);
    assert_eq!(r.missing(), ["the shell templates"]);
    assert_eq!(r.justfile_import, "import '.vendor_kit/entry.just'");
    assert_eq!(r.justfile_default, "default:\n    @just --list\n");
    assert_eq!(
        r.dockerignore,
        [
            ".vendor_kit/cache/",
            ".vendor_kit/gen/",
            ".vendor_kit/log/",
            ".vendor_kit/version.local.toml",
        ]
    );
    assert_eq!(
        release::ENGINE_REPO,
        "ghcr.io/ycpss91255-research/vendor_kit"
    );
    assert_eq!(r.config, release::CONFIG_TEMPLATE);
}

/// 出貨的 `config.toml` 模板：讀起來就是預設值（每個欄位都註解掉），而且每個 04 設定的欄位都寫出來了。
#[test]
fn shipped_config_template_reads_as_the_defaults() {
    let t = release::CONFIG_TEMPLATE;
    assert_eq!(Config::parse(t).unwrap(), Config::default());
    assert!(t.ends_with('\n') && !t.contains('\r'));
    for line in t.lines() {
        assert!(line.is_empty() || line.starts_with('#'), "{line}");
    }
    for want in [
        "# lock_timeout_seconds = 60\n",
        "# lock_enabled = true\n",
        "# [test]\n",
        "# image = ",
        "# command = [",
    ] {
        assert!(t.contains(want), "{want}");
    }
    // 拿掉註解記號後是合法的設定：欄位名與型別都對得上 `config`。
    let uncommented: String = t
        .lines()
        .filter_map(|l| l.strip_prefix("# "))
        .filter(|l| {
            [
                "lock_timeout_seconds = ",
                "lock_enabled = ",
                "[test]",
                "image = ",
                "command = ",
            ]
            .iter()
            .any(|k| l.starts_with(k))
        })
        .map(|l| format!("{l}\n"))
        .collect();
    let c = Config::parse(&uncommented).unwrap();
    assert!(c.runner().is_ok());
}
