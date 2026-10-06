//! 單元測試：直接在暫存的安裝目錄跑 `dev`、`undev`。驗覆寫與入口檔的寫入、未變更、各拒絕結果與缺口
//! （每個都不寫檔）、殘留進度的恢復，以及路徑正規化。安裝目錄外的本機開發來源由背景的假啟動器回
//! `stage-dir`：主機路徑的 `/h/` 對到暫存的「主機」目錄。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::ffi::OsString;
use std::path::PathBuf;
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};
use std::thread::{self, JoinHandle};

use diagnostics::NoSink;
use plan::{Header, RunId};

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

/// 測試用的主機上的安裝目錄（`--host-root`）。
const HOST_ROOT: &str = "/h/proj";

struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
    /// session 目錄與「主機」目錄：跟安裝目錄分開，不進快照。
    _session: tempfile::TempDir,
    ctl: PathBuf,
    inbox: PathBuf,
    /// 主機路徑 `/h/<x>` 對到這裡的 `<x>`。
    host: PathBuf,
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
                "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\nother = \"{OTHER}\"\ntool = \"{TOOL}\"\n"
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
        let session = tempfile::tempdir().unwrap();
        let (ctl, inbox, host) = (
            session.path().join("ctl"),
            session.path().join("in"),
            session.path().join("host"),
        );
        // 相對路徑的主機路徑是 `/h/proj/../…`：主機上要有 proj 這一層。
        fs::create_dir_all(host.join("proj")).unwrap();
        Fx {
            _tmp: tmp,
            dir,
            _session: session,
            ctl,
            inbox,
            host,
        }
    }

    /// 在「主機」上（安裝目錄外）放一份本機開發來源：`/h/<at>/just/<ns>.just`。
    fn host_source(&self, at: &str, namespaces: &[&str]) {
        let just = self.host.join(at).join("just");
        fs::create_dir_all(&just).unwrap();
        for ns in namespaces {
            fs::write(just.join(format!("{ns}.just")), "w:\n    echo w\n").unwrap();
        }
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
    /// 假啟動器收到的 request（`<op> <主機路徑> <slot>`）。
    ops: Vec<String>,
}

fn header() -> Header {
    Header::new(1, RunId::parse("r1").unwrap()).unwrap()
}

fn copy_dir(from: &Path, to: &Path) {
    fs::create_dir(to).unwrap();
    for entry in fs::read_dir(from).unwrap() {
        let entry = entry.unwrap();
        let target = to.join(entry.file_name());
        if entry.file_type().unwrap().is_dir() {
            copy_dir(&entry.path(), &target);
        } else {
            fs::copy(entry.path(), target).unwrap();
        }
    }
}

/// 假啟動器：`stage-dir` 把 `/h/<x>` 對到的目錄複製進 `in/<slot>`（launcher/launch.sh 的
/// vk_launch_stage_dir：來源不是目錄或 slot 已存在回 failed 1）；其他 op 一律 failed 1。
struct Peer {
    stop: Arc<AtomicBool>,
    handle: JoinHandle<Vec<String>>,
}

impl Peer {
    fn start(fx: &Fx) -> Peer {
        // 每次執行的 session 是新的：上一次的 req.1 不能被這次讀到。
        for d in [&fx.ctl, &fx.inbox] {
            let _ = fs::remove_dir_all(d);
            fs::create_dir_all(d).unwrap();
        }
        let (ctl, inbox, host) = (fx.ctl.clone(), fx.inbox.clone(), fx.host.clone());
        let stop = Arc::new(AtomicBool::new(false));
        let flag = Arc::clone(&stop);
        let handle = thread::spawn(move || {
            let header = header();
            let mut seen = Vec::new();
            let mut seq = 1u16;
            while !flag.load(Ordering::SeqCst) {
                let Ok(bytes) = fs::read(ctl.join(format!("req.{seq}"))) else {
                    thread::sleep(Duration::from_millis(2));
                    continue;
                };
                let (s, op) = Op::parse_request(&bytes, &header).unwrap();
                let outcome = match &op {
                    Op::StageDir(path, slot) => {
                        let path = String::from_utf8(path.as_bytes().to_vec()).unwrap();
                        seen.push(format!("stage-dir {path} {}", slot.as_str()));
                        let src = path.strip_prefix("/h/").map(|rest| host.join(rest));
                        let dest = inbox.join(slot.as_str());
                        match src {
                            Some(src) if src.is_dir() && !dest.exists() => {
                                copy_dir(&src, &dest);
                                Outcome::Ok
                            }
                            _ => Outcome::Failed(1),
                        }
                    }
                    other => {
                        seen.push(other.kind().name().to_owned());
                        Outcome::Failed(1)
                    }
                };
                let tmp = ctl.join(format!("res.{s}.tmp"));
                fs::write(&tmp, outcome.encode_response(&header, s)).unwrap();
                fs::rename(&tmp, ctl.join(format!("res.{s}"))).unwrap();
                seq += 1;
            }
            seen
        });
        Peer { stop, handle }
    }

    fn finish(self) -> Vec<String> {
        self.stop.store(true, Ordering::SeqCst);
        self.handle.join().unwrap()
    }
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
    let peer = Peer::start(fx);
    let mut channel = Channel::new(&fx.ctl, header());
    let code = {
        let mut env = Env {
            dir: &fx.dir,
            host_root: HOST_ROOT,
            inbox: &fx.inbox,
            channel: &mut channel,
            poll: Duration::from_millis(2),
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
    let ops = peer.finish();
    Out {
        code,
        stdout: String::from_utf8(stdout).unwrap(),
        stderr: String::from_utf8(stderr).unwrap(),
        log: String::from_utf8(log.into_inner()).unwrap(),
        ops,
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
    // 安裝目錄裡的來源引擎直接讀，不請啟動器代做。
    assert!(out.ops.is_empty(), "{:?}", out.ops);
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
fn dev_outside_the_install_directory_stages_the_source_and_keeps_the_given_form() {
    let fx = Fx::new();
    fx.host_source("elsewhere/tool", &["tool", "tool-extra"]);

    // 絕對路徑：請啟動器複製進 in/dev1、在複本上驗，入口檔寫絕對路徑。
    let out = dev(&fx, "tool", "/h/elsewhere/./tool/");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.ops, ["stage-dir /h/elsewhere/tool dev1"]);
    assert_eq!(
        out.stdout,
        "tool now uses the local source /h/elsewhere/tool (local override).\n\
         Updated .vendor_kit/gen/tools.just.\n"
    );
    assert_eq!(
        fx.entry(),
        "mod? other '../cache/other/just/other.just'\n\
         mod? tool '/h/elsewhere/tool/just/tool.just'\n\
         mod? tool-extra '/h/elsewhere/tool/just/tool-extra.just'\n"
    );
    assert_eq!(fx.local().unwrap().tool("tool"), Some("/h/elsewhere/tool"));
    assert_eq!(out.events(), LANDED);

    // 同來源再跑一次：比正規化後的值，不再複製。
    let before = fx.snapshot();
    let out = dev(&fx, "tool", "/h/elsewhere/x/../tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(out.ops.is_empty(), "{:?}", out.ops);
    assert_eq!(fx.snapshot(), before);

    // 以 `..` 跑出安裝目錄的相對路徑：留相對路徑；主機路徑接在 --host-root 後面，`..` 留給主機解析。
    let fx = Fx::new();
    fx.host_source("elsewhere/tool", &["tool", "tool-extra"]);
    let out = dev(&fx, "tool", "./x/../../elsewhere/tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.ops, ["stage-dir /h/proj/../elsewhere/tool dev1"]);
    assert_eq!(
        fx.entry(),
        "mod? other '../cache/other/just/other.just'\n\
         mod? tool '../../../elsewhere/tool/just/tool.just'\n\
         mod? tool-extra '../../../elsewhere/tool/just/tool-extra.just'\n"
    );
    assert_eq!(fx.local().unwrap().tool("tool"), Some("../elsewhere/tool"));

    // 絕對路徑落在 --host-root 底下：當成安裝目錄裡的來源，直接讀。
    let fx = Fx::new();
    let out = dev(&fx, "tool", "/h/proj/dev/tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(out.ops.is_empty(), "{:?}", out.ops);
    assert_eq!(fx.entry(), DEV_GEN);
    assert_eq!(fx.local().unwrap().tool("tool"), Some("dev/tool"));
}

#[test]
fn dev_outside_the_install_directory_that_cannot_be_used_is_vk0051() {
    let fx = Fx::new();
    fs::create_dir_all(fx.host.join("wrong/just")).unwrap();
    let before = fx.snapshot();
    for (path, reason) in [
        (
            "/h/nowhere",
            "the launcher could not copy it (exit 1): it does not exist, is not a directory, or cannot be read",
        ),
        ("../wrong", "just/tool.just is missing"),
    ] {
        let out = dev(&fx, "tool", path);
        assert_eq!(out.code, 2, "{path}");
        assert_eq!(out.ops.len(), 1, "{:?}", out.ops);
        assert_eq!(
            out.stderr,
            format!(
                "vendor_kit: error[VK0051]: Cannot use local source {path} for tool: {reason}. The local override was not enabled.\n"
            )
        );
        assert!(out.events().is_empty());
    }
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn another_override_outside_the_install_directory_is_staged_too() {
    let fx = Fx::new();
    fx.host_source("o", &["other"]);
    fx.write_local("\n[tools]\nother = \"/h/o\"\n");
    let out = dev(&fx, "tool", "dev/tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.ops, ["stage-dir /h/o dev1"]);
    assert_eq!(
        fx.entry(),
        "mod? other '/h/o/just/other.just'\n\
         mod? tool '../../dev/tool/just/tool.just'\n\
         mod? tool-extra '../../dev/tool/just/tool-extra.just'\n"
    );

    // 讀不到時是 VK0052，跟安裝目錄裡的一樣。
    let fx = Fx::new();
    fx.write_local("\n[tools]\nother = \"../gone\"\n");
    let before = fx.snapshot();
    let out = dev(&fx, "tool", "dev/tool");
    assert_eq!(out.code, 2);
    assert_eq!(out.ops, ["stage-dir /h/proj/../gone dev1"]);
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0052]: Cannot read the local override source ../gone for other: the launcher could not copy it (exit 1): it does not exist, is not a directory, or cannot be read. Run: just vendor_kit undev other\n"
    );
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
    fx.residual("install", &["install"], &[]);
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
        out.stderr.contains("incomplete install operation"),
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
        (dev(&fx, "tool", "/h/it's"), "a quote"),
        (dev(&fx, "tool", "../a\"b"), "a double quote"),
        (dev(&fx, "tool", "/.."), "the root directory"),
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
        // 停在請啟動器複製之前。
        assert!(out.ops.is_empty(), "{what}: {:?}", out.ops);
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
    let n = |s: &str| normalize(OsStr::new(s), HOST_ROOT);
    let inside = |s: &str| Source::Inside(s.to_owned());
    let outside = |s: &str| Source::Outside(s.to_owned());
    assert_eq!(n("dev/tool").unwrap(), inside("dev/tool"));
    assert_eq!(n("./dev//tool/").unwrap(), inside("dev/tool"));
    assert_eq!(n("a/../b").unwrap(), inside("b"));
    assert_eq!(n(".").unwrap(), inside("."));
    assert_eq!(n("/h/proj/").unwrap(), inside("."));
    assert_eq!(n("/h/proj/./a/../dev").unwrap(), inside("dev"));
    assert_eq!(n("..").unwrap(), outside(".."));
    assert_eq!(n("a/../../b/").unwrap(), outside("../b"));
    assert_eq!(n("../../x/./y").unwrap(), outside("../../x/y"));
    // 相對路徑跑出去又繞回來，照樣算安裝目錄外（`..` 留給主機解析，不在這裡消掉）。
    assert_eq!(n("../proj/dev").unwrap(), outside("../proj/dev"));
    assert_eq!(n("/abs//x/").unwrap(), outside("/abs/x"));
    assert_eq!(n("/h/projx").unwrap(), outside("/h/projx"));
    assert_eq!(n("/../srv").unwrap(), outside("/srv"));
    assert_eq!(
        n("").unwrap_err(),
        PathProblem::Unusable("the path is empty".to_owned())
    );
    for bad in ["/", "/..", "it's", "a\\b", "../a\"b", "/x\ty"] {
        assert!(matches!(n(bad), Err(PathProblem::Gap(_))), "{bad:?}");
    }
    assert_eq!(
        outside("/abs").host_path(HOST_ROOT).as_deref(),
        Some("/abs")
    );
    assert_eq!(
        outside("../b").host_path(HOST_ROOT).as_deref(),
        Some("/h/proj/../b")
    );
    assert_eq!(inside("b").host_path(HOST_ROOT), None);
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
