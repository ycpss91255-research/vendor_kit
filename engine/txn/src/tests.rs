//! 單元測試：完整順序的結果，以及以注入的故障在每一步中斷後，殘留狀態可被辨識。

use std::cell::Cell;
use std::fs;
use std::io;
use std::os::unix::fs::PermissionsExt;
use std::path::{Path, PathBuf};
use std::rc::Rc;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

use imageref::ImageRef;
use runlog::{Component, Condition, Header, Mode, Reason, Verdict, Writer};

use super::*;

const WRITTEN_BY: &str = "vendor_kit 0.0.0";
const ENGINE: &str = "ghcr.io/acme/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const TOOL: &str = "ghcr.io/acme/tool:v1.2.3@sha256:3333333333333333333333333333333333333333333333333333333333333333";
const TOOLS_JUST_TEXT: &[u8] = b"mod? tool '../cache/tool/dist/just/tool.just'\n";
const RECORD_PATH: &str = "baseline/tool.toml";
const RECORD_TEXT: &[u8] = b"schema = 1\n";
const JUSTFILE_TEXT: &[u8] = b"import '.vendor_kit/entry.just'\n";

fn fixed_time() -> SystemTime {
    UNIX_EPOCH + Duration::new(1_791_162_123, 4_000)
}

fn header(component: Component) -> Header {
    Header {
        version: "0.0.0".to_owned(),
        component,
        invocation_id: "inv-1".to_owned(),
    }
}

fn image(s: &str) -> ImageRef {
    ImageRef::parse(s).unwrap()
}

fn progress() -> Progress {
    Progress::new("add", "inv-1", &["add", "tool"]).unwrap()
}

/// 一個安裝目錄（已有 `version.toml` 與舊版的 `cache/tool/`），加上 repo 外的暫存目錄。
struct Fixture {
    _root: tempfile::TempDir,
    _staged: tempfile::TempDir,
    dir: InstallDir,
    staged: PathBuf,
    stamp_file: PathBuf,
}

impl Fixture {
    fn new() -> Fixture {
        let root = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(root.path());
        fs::create_dir_all(dir.vk_dir()).unwrap();
        LockFile::new(&image(ENGINE))
            .save_to(&dir, WRITTEN_BY)
            .unwrap();
        let old = dir.tool_cache("tool").unwrap();
        fs::create_dir_all(&old).unwrap();
        fs::write(old.join("stale.txt"), b"old\n").unwrap();

        let staged = tempfile::tempdir().unwrap();
        let just = staged.path().join("dist/just");
        fs::create_dir_all(&just).unwrap();
        fs::write(just.join("tool.just"), b"hello:\n    echo hi\n").unwrap();
        let bin = staged.path().join("bin/run.sh");
        fs::create_dir_all(bin.parent().unwrap()).unwrap();
        fs::write(&bin, b"#!/bin/sh\n").unwrap();
        fs::set_permissions(&bin, fs::Permissions::from_mode(0o755)).unwrap();

        Fixture {
            stamp_file: dir.vk_dir().join("stamps").join("tool.toml"),
            staged: staged.path().to_path_buf(),
            dir,
            _root: root,
            _staged: staged,
        }
    }

    fn tool(&self) -> ToolContent<'_> {
        ToolContent {
            repo: "tool",
            staged: &self.staged,
            version: TOOL,
            stamp_file: &self.stamp_file,
        }
    }

    fn lock_text(&self) -> Vec<u8> {
        fs::read(self.dir.version_toml()).unwrap()
    }

    fn record(&self) -> PathBuf {
        self.dir.vk_dir().join(RECORD_PATH)
    }

    fn tools_just(&self) -> PathBuf {
        self.dir.gen_dir().join(TOOLS_JUST)
    }

    fn progress_left(&self) -> bool {
        !progress::find(&self.dir).unwrap().is_empty()
    }

    fn cache_is_new(&self) -> bool {
        let cache = self.dir.tool_cache("tool").unwrap();
        cache.join("dist/just/tool.just").is_file() && !cache.join("stale.txt").exists()
    }
}

/// 在第 `fail_at` 次呼叫（從 0 起算）回錯、不做那一步的 [`Effects`]；其他呼叫照原樣交給 `inner`。
struct Faulty<E> {
    inner: E,
    fail_at: Option<usize>,
    calls: usize,
}

impl<E: Effects> Faulty<E> {
    fn new(inner: E, fail_at: Option<usize>) -> Self {
        Faulty {
            inner,
            fail_at,
            calls: 0,
        }
    }

    fn tick(&mut self) -> Result<(), Error> {
        let n = self.calls;
        self.calls += 1;
        if self.fail_at == Some(n) {
            return Err(Error::Io {
                path: PathBuf::from("injected"),
                source: io::Error::other("injected fault"),
            });
        }
        Ok(())
    }
}

impl<E: Effects> Effects for Faulty<E> {
    fn log(&mut self, event: &Event) -> Result<(), Error> {
        self.tick()?;
        self.inner.log(event)
    }
    fn create_progress(&mut self, progress: &mut Progress) -> Result<PathBuf, Error> {
        self.tick()?;
        self.inner.create_progress(progress)
    }
    fn swap_cache(&mut self, tool: &ToolContent) -> Result<(), Error> {
        self.tick()?;
        self.inner.swap_cache(tool)
    }
    fn write_repo_file(&mut self, file: &RepoFile) -> Result<(), Error> {
        self.tick()?;
        self.inner.write_repo_file(file)
    }
    fn write_record_file(&mut self, file: &RecordFile) -> Result<(), Error> {
        self.tick()?;
        self.inner.write_record_file(file)
    }
    fn write_tools_just(&mut self, contents: &[u8]) -> Result<(), Error> {
        self.tick()?;
        self.inner.write_tools_just(contents)
    }
    fn save_lock(&mut self, lock: &mut LockFile) -> Result<(), Error> {
        self.tick()?;
        self.inner.save_lock(lock)
    }
    fn delete_progress(&mut self, progress: &Progress) -> Result<(), Error> {
        self.tick()?;
        self.inner.delete_progress(progress)
    }
    fn remove_tools_just(&mut self) -> Result<(), Error> {
        self.tick()?;
        self.inner.remove_tools_just()
    }
    fn remove_vk_path(&mut self, path: &Path) -> Result<(), Error> {
        self.tick()?;
        self.inner.remove_vk_path(path)
    }
    fn remove_lock(&mut self) -> Result<(), Error> {
        self.tick()?;
        self.inner.remove_lock()
    }
}

/// 完整順序走一次：一個工具、一個 repo 檔、一個紀錄檔、寫入口檔、改工具的版本鎖定行。
fn sequence<E: Effects>(fx: &mut E, f: &Fixture, target: Target) -> Result<Done, Failed> {
    let mut lock = LockFile::load_from(&f.dir).unwrap().unwrap();
    lock.set_tool("tool", &image(TOOL)).unwrap();
    let repo = [RepoFile {
        path: Path::new("justfile"),
        contents: JUSTFILE_TEXT,
    }];
    let records = [RecordFile {
        path: Path::new(RECORD_PATH),
        contents: RECORD_TEXT,
    }];
    Txn::begin(fx, progress())?
        .swap_cache(&[f.tool()])?
        .write_repo_files(&repo)?
        .write_records(&records)?
        .write_tools_just(Some(TOOLS_JUST_TEXT))?
        .write_lock_line(&mut lock, target)?
        .complete()
}

/// 跑一次，回傳結果、引擎寫出的紀錄原文，與這次一共呼叫 [`Effects`] 幾次。
fn run(f: &Fixture, fail_at: Option<usize>, target: Target) -> (Result<Done, Failed>, Vec<u8>) {
    let mut w = Writer::new(Vec::new(), header(Component::Engine)).with_clock(fixed_time);
    let result = {
        let mut fx = Faulty::new(Disk::new(&f.dir, &mut w, WRITTEN_BY), fail_at);
        sequence(&mut fx, f, target)
    };
    (result, w.into_inner())
}

/// 紀錄裡依序的事件名。
fn events(log: &[u8]) -> Vec<String> {
    let text = std::str::from_utf8(log).unwrap();
    text.lines()
        .map(|line| {
            let rest = line.split_once("\"event_name\":\"").unwrap().1;
            rest.split_once('"').unwrap().0.to_owned()
        })
        .collect()
}

/// 每一步之前已寫的紀錄事件。
fn expected_events(before: Step) -> Vec<String> {
    let all = [
        (Step::WritesStarted, "writes_started"),
        (Step::LockLineWriteStarted, "lock_line_write_started"),
        (Step::LockLineWritten, "lock_line_written"),
        (Step::ProgressRemoved, "progress_removed"),
    ];
    all.iter()
        .filter(|(s, _)| *s < before)
        .map(|(_, n)| (*n).to_owned())
        .collect()
}

// ---- 完整順序 ----

#[test]
fn full_sequence_lands_everything_in_order() {
    let f = Fixture::new();
    let before = f.lock_text();
    let (result, log) = run(&f, None, Target::Tool);
    let done = result.unwrap();
    assert_eq!(done.progress_file, ".tmp.add.inv-1.toml");

    assert_eq!(
        events(&log),
        [
            "writes_started",
            "lock_line_write_started",
            "lock_line_written",
            "progress_removed"
        ]
    );
    assert!(
        String::from_utf8(log)
            .unwrap()
            .contains("\"vendor_kit.progress_file\":\".tmp.add.inv-1.toml\"")
    );
    assert!(!f.progress_left());

    // cache/tool/ 換成暫存內容，舊檔不留，權限位元照搬，暫存的兄弟目錄不留。
    assert!(f.cache_is_new());
    let run_sh = f.dir.tool_cache("tool").unwrap().join("bin/run.sh");
    assert_eq!(
        fs::metadata(run_sh).unwrap().permissions().mode() & 0o777,
        0o755
    );
    let names: Vec<String> = fs::read_dir(f.dir.cache_dir())
        .unwrap()
        .map(|e| e.unwrap().file_name().to_string_lossy().into_owned())
        .collect();
    assert_eq!(names, ["tool"]);

    // 印記記的是版本鎖定行的值，並與落地的 cache/tool/ 一致。
    let stamp = Stamp::load(&f.stamp_file).unwrap().unwrap();
    assert_eq!(stamp.version(), TOOL);
    assert_eq!(stamp.entries().len(), 2);
    let cache = f.dir.tool_cache("tool").unwrap();
    assert!(stamp.verify(&cache).unwrap().is_match());

    assert_eq!(
        fs::read(f.dir.root().join("justfile")).unwrap(),
        JUSTFILE_TEXT
    );
    assert_eq!(fs::read(f.record()).unwrap(), RECORD_TEXT);
    assert_eq!(fs::read(f.tools_just()).unwrap(), TOOLS_JUST_TEXT);

    assert_ne!(f.lock_text(), before);
    let lock = LockFile::load_from(&f.dir).unwrap().unwrap();
    assert_eq!(lock.tool("tool"), Some(&image(TOOL)));
}

#[test]
fn empty_steps_and_kept_lock_line_write_only_progress_events() {
    let f = Fixture::new();
    let before = f.lock_text();
    let mut w = Writer::new(Vec::new(), header(Component::Engine)).with_clock(fixed_time);
    {
        let mut fx = Disk::new(&f.dir, &mut w, WRITTEN_BY);
        Txn::begin(&mut fx, progress())
            .unwrap()
            .swap_cache(&[])
            .unwrap()
            .write_repo_files(&[])
            .unwrap()
            .write_records(&[])
            .unwrap()
            .write_tools_just(None)
            .unwrap()
            .keep_lock_line()
            .complete()
            .unwrap();
    }
    assert_eq!(
        events(&w.into_inner()),
        ["writes_started", "progress_removed"]
    );
    assert_eq!(f.lock_text(), before);
    assert!(!f.tools_just().exists());
    assert!(!f.cache_is_new());
    assert!(!f.progress_left());
}

// ---- 每一步中斷 ----

#[test]
fn a_fault_at_each_step_leaves_a_recognizable_state() {
    for (n, step) in Step::ALL.into_iter().enumerate() {
        let f = Fixture::new();
        let before = f.lock_text();
        let (result, log) = run(&f, Some(n), Target::Tool);
        let failed = match result {
            Ok(_) => panic!("fault at call {n} did not fail"),
            Err(failed) => failed,
        };
        assert_eq!(failed.step, step, "call {n}");
        // 中途寫檔失敗沒有代碼（G4）。
        assert!(failed.message().is_none(), "{step}");

        // 失敗那一步之前的事件都在，之後的都沒有。
        assert_eq!(events(&log), expected_events(step), "{step}");

        // 進度檔從建好到刪掉之間的每一步中斷，進度檔都還在。
        let progress_left = (Step::SwapCache..=Step::DeleteProgress).contains(&step);
        assert_eq!(f.progress_left(), progress_left, "{step}");

        // 建進度檔之前沒有任何非紀錄檔寫入。
        if step <= Step::CreateProgress {
            assert!(!f.cache_is_new(), "{step}");
            assert!(!f.dir.root().join("justfile").exists(), "{step}");
        }

        // 每一步都在前一步完成之後才做。
        assert_eq!(f.cache_is_new(), step > Step::SwapCache, "{step}");
        assert_eq!(f.stamp_file.exists(), step > Step::SwapCache, "{step}");
        assert_eq!(
            f.dir.root().join("justfile").exists(),
            step > Step::RepoFile,
            "{step}"
        );
        assert_eq!(f.record().exists(), step > Step::Records, "{step}");
        assert_eq!(f.tools_just().exists(), step > Step::ToolsJust, "{step}");

        // 版本鎖定行最後才改：寫成之前中斷，版本鎖定行不動。
        assert_eq!(f.lock_text() == before, step <= Step::LockLine, "{step}");

        assert_eq!(failed.step.completed(), step == Step::ProgressRemoved);
        // 可辨識：要嘛進度檔還在，要嘛除紀錄外沒寫任何檔，要嘛已過完成點。
        let untouched = f.lock_text() == before && !f.cache_is_new() && !f.tools_just().exists();
        assert!(
            progress_left || untouched || failed.step.completed(),
            "{step}"
        );
    }
}

#[test]
fn every_effect_call_is_one_step() {
    // 完整順序剛好呼叫 Step::ALL 那麼多次：上一個測試的第 N 次呼叫就是第 N 步。
    let f = Fixture::new();
    let mut w = Writer::new(Vec::new(), header(Component::Engine)).with_clock(fixed_time);
    let mut fx = Faulty::new(Disk::new(&f.dir, &mut w, WRITTEN_BY), None);
    sequence(&mut fx, &f, Target::Tool).unwrap();
    assert_eq!(fx.calls, Step::ALL.len());
}

/// 啟動器的 `run_started`（首次導入）＋引擎這次寫的紀錄＋`engine_finished`。
fn initial_import_log(engine: &[u8], exit_code: u8) -> Vec<u8> {
    let argv = ["-y".to_owned()];
    let mut launcher = Writer::new(Vec::new(), header(Component::Launcher)).with_clock(fixed_time);
    launcher
        .write(&Event::RunStarted {
            mode: Mode::InitialImport,
            argv: &argv,
        })
        .unwrap();
    let mut log = launcher.into_inner();
    log.extend_from_slice(engine);
    let mut tail = Writer::new(Vec::new(), header(Component::Engine)).with_clock(fixed_time);
    tail.write(&Event::EngineFinished { exit_code }).unwrap();
    log.extend(tail.into_inner());
    log
}

#[test]
fn lock_line_fault_is_seen_by_the_log_reader_as_unconfirmed() {
    let f = Fixture::new();
    let call = Step::ALL.iter().position(|s| *s == Step::LockLine).unwrap();
    let (result, log) = run(&f, Some(call), Target::Engine);
    assert_eq!(result.err().map(|e| e.step), Some(Step::LockLine));
    assert_eq!(
        runlog::assess(&initial_import_log(&log, 2), false),
        Verdict::NotApplicable(Reason::LockLineWriteUnconfirmed)
    );
}

#[test]
fn fault_before_the_engine_lock_line_is_an_unfinished_initial_import() {
    let f = Fixture::new();
    let call = Step::ALL
        .iter()
        .position(|s| *s == Step::ToolsJust)
        .unwrap();
    let (result, log) = run(&f, Some(call), Target::Engine);
    assert_eq!(result.err().map(|e| e.step), Some(Step::ToolsJust));
    assert_eq!(
        runlog::assess(&initial_import_log(&log, 2), false),
        Verdict::Applies(Condition::BeforeEngineLockLine)
    );
}

// ---- 實際的寫檔失敗 ----

#[test]
fn existing_progress_file_stops_before_any_other_write() {
    let f = Fixture::new();
    progress().create(&f.dir, WRITTEN_BY).unwrap();
    let before = f.lock_text();
    let (result, log) = run(&f, None, Target::Tool);
    let failed = result.err().unwrap();
    assert_eq!(failed.step, Step::CreateProgress);
    assert!(matches!(
        failed.error,
        Error::Progress(progress::Error::Exists { .. })
    ));
    assert!(failed.message().is_none());
    assert_eq!(events(&log), ["writes_started"]);
    assert!(!f.cache_is_new());
    assert_eq!(f.lock_text(), before);
}

#[test]
fn stamp_write_failure_after_cache_swap_leaves_the_progress_file() {
    let mut f = Fixture::new();
    // 印記的上層是一般檔，建不了目錄：cache/tool/ 已換好，印記寫不出來。
    let blocker = f.dir.vk_dir().join("blocker");
    fs::write(&blocker, b"").unwrap();
    f.stamp_file = blocker.join("tool.toml");
    let before = f.lock_text();
    let (result, log) = run(&f, None, Target::Tool);
    let failed = result.err().unwrap();
    assert_eq!(failed.step, Step::SwapCache);
    assert!(matches!(failed.error, Error::Stamp(_)));
    assert!(failed.message().is_none());
    assert_eq!(events(&log), ["writes_started"]);
    assert!(f.cache_is_new());
    assert!(f.progress_left());
    assert!(!f.tools_just().exists());
    assert_eq!(f.lock_text(), before);
}

#[test]
fn symlink_in_staged_content_keeps_the_old_cache() {
    let f = Fixture::new();
    std::os::unix::fs::symlink("run.sh", f.staged.join("bin/link")).unwrap();
    let (result, _) = run(&f, None, Target::Tool);
    let failed = result.err().unwrap();
    assert_eq!(failed.step, Step::SwapCache);
    assert!(matches!(
        failed.error,
        Error::Write(files::Error::Symlink { .. })
    ));
    // 舊的 cache/tool/ 還沒被換掉，進度檔還在。
    assert!(
        f.dir
            .tool_cache("tool")
            .unwrap()
            .join("stale.txt")
            .is_file()
    );
    assert!(f.progress_left());
}

#[test]
fn repo_file_paths_must_stay_inside_the_repo() {
    let f = Fixture::new();
    let mut w = Writer::new(Vec::new(), header(Component::Engine)).with_clock(fixed_time);
    let mut fx = Disk::new(&f.dir, &mut w, WRITTEN_BY);
    for bad in ["", "/etc/passwd", "../x", "a/../b", "./a"] {
        let file = RepoFile {
            path: Path::new(bad),
            contents: b"x",
        };
        assert!(
            matches!(fx.write_repo_file(&file), Err(Error::BadPath(_))),
            "{bad:?}"
        );
    }
    let ok = RepoFile {
        path: Path::new("sub/dir/file.txt"),
        contents: b"x",
    };
    fx.write_repo_file(&ok).unwrap();
    assert_eq!(
        fs::read(f.dir.root().join("sub/dir/file.txt")).unwrap(),
        b"x"
    );
}

#[test]
fn record_file_paths_must_stay_inside_the_vk_dir() {
    let f = Fixture::new();
    let mut w = Writer::new(Vec::new(), header(Component::Engine)).with_clock(fixed_time);
    let mut fx = Disk::new(&f.dir, &mut w, WRITTEN_BY);
    for bad in ["", "/etc/passwd", "../justfile", "baseline/../../x"] {
        let file = RecordFile {
            path: Path::new(bad),
            contents: b"x",
        };
        assert!(
            matches!(fx.write_record_file(&file), Err(Error::BadPath(_))),
            "{bad:?}"
        );
    }
    let ok = RecordFile {
        path: Path::new("baseline/tool/a/b.txt"),
        contents: b"x",
    };
    fx.write_record_file(&ok).unwrap();
    assert_eq!(
        fs::read(f.dir.vk_dir().join("baseline/tool/a/b.txt")).unwrap(),
        b"x"
    );
}

/// 寫幾行之後就回錯的紀錄輸出。
struct FailingLog {
    lines_left: Rc<Cell<usize>>,
}

impl io::Write for FailingLog {
    fn write(&mut self, buf: &[u8]) -> io::Result<usize> {
        if self.lines_left.get() == 0 {
            return Err(io::Error::other("disk full"));
        }
        self.lines_left.set(self.lines_left.get() - 1);
        Ok(buf.len())
    }
    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}

#[test]
fn log_write_failure_is_a_step_failure_without_a_code() {
    let f = Fixture::new();
    let lines_left = Rc::new(Cell::new(0));
    let out = FailingLog {
        lines_left: Rc::clone(&lines_left),
    };
    let mut w = Writer::new(out, header(Component::Engine)).with_clock(fixed_time);
    let mut fx = Disk::new(&f.dir, &mut w, WRITTEN_BY);
    let failed = sequence(&mut fx, &f, Target::Tool).err().unwrap();
    assert_eq!(failed.step, Step::WritesStarted);
    assert!(matches!(failed.error, Error::Log(runlog::Error::Io(_))));
    assert!(failed.message().is_none());
    assert!(!f.progress_left());

    // 寫了 writes_started、lock_line_write_started 之後紀錄寫不進去：版本鎖定行已寫，進度檔還在。
    let f = Fixture::new();
    lines_left.set(2);
    let before = f.lock_text();
    let mut fx = Disk::new(&f.dir, &mut w, WRITTEN_BY);
    let failed = sequence(&mut fx, &f, Target::Tool).err().unwrap();
    assert_eq!(failed.step, Step::LockLineWritten);
    assert!(failed.message().is_none());
    assert_ne!(f.lock_text(), before);
    assert!(f.progress_left());
}

#[test]
fn unregistered_codes_pass_through_from_lower_crates() {
    let e = Error::Log(runlog::Error::Unregistered("x"));
    assert_eq!(e.message().map(|m| m.code), Some(messages::VK0056.code));
    let e = Error::Io {
        path: PathBuf::from("p"),
        source: io::Error::other("x"),
    };
    assert!(e.message().is_none());
}

// ---- 收回的順序 ----

/// 已導入 `tool` 的安裝目錄：`cache/tool/`、印記、metadata、入口檔、版本鎖定行、插入過一行的 `.gitignore`。
fn retract_fixture() -> Fixture {
    let f = Fixture::new();
    let mut lock = LockFile::load_from(&f.dir).unwrap().unwrap();
    lock.set_tool("tool", &image(TOOL)).unwrap();
    lock.save_to(&f.dir, WRITTEN_BY).unwrap();
    fs::create_dir_all(f.stamp_file.parent().unwrap()).unwrap();
    fs::write(&f.stamp_file, b"stamp\n").unwrap();
    fs::create_dir_all(f.record().parent().unwrap()).unwrap();
    fs::write(f.record(), RECORD_TEXT).unwrap();
    fs::create_dir_all(f.dir.gen_dir()).unwrap();
    fs::write(f.tools_just(), TOOLS_JUST_TEXT).unwrap();
    fs::write(f.dir.root().join(".gitignore"), b"keep\nadded\n").unwrap();
    f
}

const RETRACTED_GITIGNORE: &[u8] = b"keep\n";
/// 收回時仍保留、要改寫的紀錄檔。
const KEPT_RECORD: &str = "baseline/.vendor_kit.toml";

/// 收回順序走一次：一個 repo 檔、入口檔換成空的、改寫一個保留的紀錄檔、刪 `cache/tool/`、印記與 metadata、拿掉工具的版本鎖定行。
fn retract_sequence<E: Effects>(fx: &mut E, f: &Fixture) -> Result<Done, Failed> {
    let mut lock = LockFile::load_from(&f.dir).unwrap().unwrap();
    lock.remove_tool("tool").unwrap();
    let repo = [RepoFile {
        path: Path::new(".gitignore"),
        contents: RETRACTED_GITIGNORE,
    }];
    let stamp = f.stamp_file.strip_prefix(f.dir.vk_dir()).unwrap();
    let removes = [Path::new("cache/tool"), stamp, Path::new(RECORD_PATH)];
    let writes = [RecordFile {
        path: Path::new(KEPT_RECORD),
        contents: RECORD_TEXT,
    }];
    Txn::begin(
        fx,
        Progress::new("remove", "inv-1", &["remove", "tool"]).unwrap(),
    )?
    .retract_repo_files(&repo)?
    .retract_tools_just(Entry::Write(b""))?
    .retract_records(&writes, &removes)?
    .write_lock_line(&mut lock, Target::Tool)?
    .complete()
}

fn run_retract(f: &Fixture, fail_at: Option<usize>) -> (Result<Done, Failed>, Vec<u8>) {
    let mut w = Writer::new(Vec::new(), header(Component::Engine)).with_clock(fixed_time);
    let result = {
        let mut fx = Faulty::new(Disk::new(&f.dir, &mut w, WRITTEN_BY), fail_at);
        retract_sequence(&mut fx, f)
    };
    (result, w.into_inner())
}

#[test]
fn retract_sequence_removes_everything_in_order() {
    let f = retract_fixture();
    let (result, log) = run_retract(&f, None);
    assert_eq!(result.unwrap().progress_file, ".tmp.remove.inv-1.toml");
    assert_eq!(
        events(&log),
        [
            "writes_started",
            "lock_line_write_started",
            "lock_line_written",
            "progress_removed"
        ]
    );
    assert!(!f.progress_left());
    assert!(!f.dir.tool_cache("tool").unwrap().exists());
    assert!(!f.stamp_file.exists());
    assert!(!f.record().exists());
    assert_eq!(fs::read(f.tools_just()).unwrap(), b"");
    assert_eq!(
        fs::read(f.dir.root().join(".gitignore")).unwrap(),
        RETRACTED_GITIGNORE
    );
    let lock = LockFile::load_from(&f.dir).unwrap().unwrap();
    assert!(lock.tools().is_empty());
}

#[test]
fn every_retract_effect_call_is_one_step() {
    let f = retract_fixture();
    let mut w = Writer::new(Vec::new(), header(Component::Engine)).with_clock(fixed_time);
    let mut fx = Faulty::new(Disk::new(&f.dir, &mut w, WRITTEN_BY), None);
    retract_sequence(&mut fx, &f).unwrap();
    // 三個路徑各刪一次，所以比 Step::RETRACT 多兩次呼叫。
    assert_eq!(fx.calls, Step::RETRACT.len() + 2);
}

#[test]
fn a_fault_at_each_retract_step_leaves_a_recognizable_state() {
    // 第 N 次呼叫對應的步驟：RemovePaths 佔三次呼叫。
    let mut calls: Vec<Step> = Vec::new();
    for step in Step::RETRACT {
        let n = if step == Step::RemovePaths { 3 } else { 1 };
        calls.extend(std::iter::repeat_n(step, n));
    }
    for (n, step) in calls.into_iter().enumerate() {
        let f = retract_fixture();
        let lock_before = f.lock_text();
        let (result, _) = run_retract(&f, Some(n));
        let failed = result.err().unwrap_or_else(|| panic!("call {n}"));
        assert_eq!(failed.step, step, "call {n}");
        let pos = Step::RETRACT.iter().position(|s| *s == step).unwrap();
        let after = |s: Step| pos > Step::RETRACT.iter().position(|x| *x == s).unwrap();

        let progress_left = after(Step::CreateProgress) && !after(Step::DeleteProgress);
        assert_eq!(f.progress_left(), progress_left, "{step}");
        assert_eq!(
            fs::read(f.dir.root().join(".gitignore")).unwrap() == RETRACTED_GITIGNORE,
            after(Step::RepoFile),
            "{step}"
        );
        // 入口檔先拿掉工具的行，cache/ 才刪：入口檔還指著工具時 cache/tool/ 一定還在。
        let entry_points = fs::read(f.tools_just()).unwrap() == TOOLS_JUST_TEXT;
        assert_eq!(entry_points, !after(Step::ToolsJust), "{step}");
        if entry_points {
            assert!(f.dir.tool_cache("tool").unwrap().exists(), "{step}");
        }
        assert_eq!(
            f.dir.vk_dir().join(KEPT_RECORD).exists(),
            after(Step::Records),
            "{step}"
        );
        if !after(Step::RemovePaths) && step != Step::RemovePaths {
            assert!(f.record().exists(), "{step}");
        }
        assert_eq!(
            f.lock_text() == lock_before,
            !after(Step::LockLine),
            "{step}"
        );
    }
}

#[test]
fn remove_lock_file_and_entry_remove_delete_the_files() {
    let f = retract_fixture();
    let mut w = Writer::new(Vec::new(), header(Component::Engine)).with_clock(fixed_time);
    {
        let mut fx = Disk::new(&f.dir, &mut w, WRITTEN_BY);
        Txn::begin(
            &mut fx,
            Progress::new("uninstall", "inv-1", &["uninstall"]).unwrap(),
        )
        .unwrap()
        .retract_repo_files(&[])
        .unwrap()
        .retract_tools_just(Entry::Remove)
        .unwrap()
        .retract_records(
            &[],
            &[Path::new("cache"), Path::new("gen"), Path::new("absent")],
        )
        .unwrap()
        .remove_lock_file(Target::Engine)
        .unwrap()
        .complete()
        .unwrap();
    }
    assert_eq!(
        events(&w.into_inner()),
        [
            "writes_started",
            "lock_line_write_started",
            "lock_line_written",
            "progress_removed"
        ]
    );
    assert!(!f.dir.version_toml().exists());
    assert!(!f.dir.cache_dir().exists());
    assert!(!f.dir.gen_dir().exists());
    assert!(f.record().exists());
    assert!(f.dir.vk_dir().is_dir());
}

#[test]
fn removed_paths_must_stay_inside_the_vk_dir() {
    let f = Fixture::new();
    let mut w = Writer::new(Vec::new(), header(Component::Engine)).with_clock(fixed_time);
    let mut fx = Disk::new(&f.dir, &mut w, WRITTEN_BY);
    for bad in ["", "/etc", "../x", "a/../b", "./a"] {
        assert!(
            matches!(fx.remove_vk_path(Path::new(bad)), Err(Error::BadPath(_))),
            "{bad:?}"
        );
    }
    // symlink 只刪它本身，不跟過去。
    let outside = tempfile::tempdir().unwrap();
    fs::write(outside.path().join("keep"), b"x").unwrap();
    std::os::unix::fs::symlink(outside.path(), f.dir.vk_dir().join("link")).unwrap();
    fx.remove_vk_path(Path::new("link")).unwrap();
    assert!(outside.path().join("keep").is_file());
    assert!(fs::symlink_metadata(f.dir.vk_dir().join("link")).is_err());
}
