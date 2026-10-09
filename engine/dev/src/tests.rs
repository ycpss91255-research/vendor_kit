//! 單元測試：直接在暫存的安裝目錄跑 `dev`、`undev`。驗覆寫與入口檔的寫入、未變更、各拒絕結果與缺口
//! （每個都不寫檔）、殘留進度的恢復，以及路徑正規化。安裝目錄外的本機開發來源由背景的假啟動器回
//! `stage-dir`：主機路徑的 `/h/` 對到暫存的「主機」目錄。`undev` 取件時，假啟動器照 [`Registry`] 回
//! `inspect`、`pull`、`extract`。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::cell::RefCell;
use std::collections::BTreeSet;
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
/// 開著覆寫時 `git pull` 換上的新鎖定行。
const NEW_TOOL: &str = "ghcr.io/acme/tool:v1.3.0@sha256:4444444444444444444444444444444444444444444444444444444444444444";
const NEW_PINNED: &str =
    "ghcr.io/acme/tool@sha256:4444444444444444444444444444444444444444444444444444444444444444";
const PINNED: &str =
    "ghcr.io/acme/tool@sha256:2222222222222222222222222222222222222222222222222222222222222222";
const IMAGE_ID: &str = "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
/// `Fx::new` 放進 `cache/<repo>/just/<repo>.just` 的本文。
const CACHED_TEXT: &str = "x:\n    echo x\n";

/// 假啟動器回 `inspect`、`pull`、`extract` 用的一個 image。
#[derive(Debug, Clone)]
struct Image {
    /// 帶 digest 的引用，`inspect`、`pull` 收的就是它。
    pinned: String,
    /// inspect 回的 RepoDigests 那一筆。
    repo_digest: String,
    /// 一開始就在本機（不用 `pull`）。
    local: bool,
    /// `extract` 放進 `in/<slot>` 的檔：相對路徑與本文。
    files: Vec<(String, String)>,
    /// inspect 回的 `Config.Labels`（JSON 物件的內容，不含大括號）；`None` 就不帶 `Config`。
    labels: Option<String>,
}

impl Image {
    fn new(pinned: &str, local: bool, tool_text: &str) -> Image {
        Image {
            pinned: pinned.to_owned(),
            repo_digest: pinned.to_owned(),
            local,
            files: vec![("just/tool.just".to_owned(), tool_text.to_owned())],
            labels: None,
        }
    }

    /// 本機的引擎 image：`reference` 原樣給 `inspect`，帶 `labels`。
    fn engine(reference: &str, labels: &str) -> Image {
        Image {
            pinned: reference.to_owned(),
            repo_digest: reference.to_owned(),
            local: true,
            files: Vec::new(),
            labels: Some(labels.to_owned()),
        }
    }
}

/// 假啟動器看得到的 registry：沒列的引用 `inspect`、`pull` 都失敗。
#[derive(Debug, Clone, Default)]
struct Registry {
    images: Vec<Image>,
}

struct Fx {
    _tmp: tempfile::TempDir,
    dir: InstallDir,
    /// session 目錄與「主機」目錄：跟安裝目錄分開，不進快照。
    _session: tempfile::TempDir,
    ctl: PathBuf,
    inbox: PathBuf,
    /// 主機路徑 `/h/<x>` 對到這裡的 `<x>`。
    host: PathBuf,
    /// 假啟動器回取件 op 用的 image。
    registry: RefCell<Registry>,
    /// 這次呼叫的薄殼介面版（`plan` header 的 P）。
    protocol: std::cell::Cell<u32>,
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
            registry: RefCell::new(Registry::default()),
            protocol: std::cell::Cell::new(1),
        }
    }

    /// 把工具的版本鎖定行換成 `version`（開著覆寫時 `git pull` 換了鎖定行）。
    fn set_lock_line(&self, version: &str) {
        let mut lock = LockFile::load_from(&self.dir).unwrap().unwrap();
        lock.set_tool("tool", &ImageRef::parse(version).unwrap())
            .unwrap();
        lock.save_to(&self.dir, WRITTEN_BY).unwrap();
    }

    fn cached_text(&self) -> String {
        fs::read_to_string(self.dir.tool_cache("tool").unwrap().join("just/tool.just")).unwrap()
    }

    fn stamp_version(&self) -> String {
        stamp::Stamp::load(&stamp::tool_file(&self.dir, "tool"))
            .unwrap()
            .unwrap()
            .version()
            .to_owned()
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

fn header(protocol: u32) -> Header {
    Header::new(protocol, RunId::parse("r1").unwrap()).unwrap()
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
        let registry = fx.registry.borrow().clone();
        let protocol = fx.protocol.get();
        let stop = Arc::new(AtomicBool::new(false));
        let flag = Arc::clone(&stop);
        let handle = thread::spawn(move || {
            let header = header(protocol);
            let mut seen = Vec::new();
            let mut pulled: BTreeSet<String> = BTreeSet::new();
            let find = |r: &str| registry.images.iter().find(|i| i.pinned == r).cloned();
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
                    Op::Inspect(r) => {
                        seen.push(format!("inspect {}", r.as_str()));
                        match find(r.as_str()) {
                            Some(i) if i.local || pulled.contains(&i.pinned) => {
                                let config = i
                                    .labels
                                    .as_ref()
                                    .map(|l| format!(",\"Config\":{{\"Labels\":{{{l}}}}}"))
                                    .unwrap_or_default();
                                let json = format!(
                                    "[{{\"Id\":\"{IMAGE_ID}\",\"RepoDigests\":[\"{}\"]{config}}}]",
                                    i.repo_digest
                                );
                                fs::write(ctl.join(format!("res.{s}.out")), json).unwrap();
                                Outcome::Ok
                            }
                            _ => Outcome::Failed(1),
                        }
                    }
                    Op::Pull(r) => {
                        seen.push(format!("pull {}", r.as_str()));
                        match find(r.as_str()) {
                            Some(i) => {
                                pulled.insert(i.pinned);
                                Outcome::Ok
                            }
                            None => Outcome::Failed(1),
                        }
                    }
                    Op::Extract(id, slot) => {
                        seen.push(format!("extract {} {}", id.as_str(), slot.as_str()));
                        let image = registry
                            .images
                            .iter()
                            .find(|i| i.local || pulled.contains(&i.pinned));
                        match image {
                            Some(i) => {
                                let dest = inbox.join(slot.as_str());
                                for (rel, text) in &i.files {
                                    let path = dest.join(rel);
                                    fs::create_dir_all(path.parent().unwrap()).unwrap();
                                    fs::write(path, text).unwrap();
                                }
                                Outcome::Ok
                            }
                            None => Outcome::Failed(1),
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
    run_as(fx, req, argv, "r1")
}

/// 以 `run_id` 跑一次（重跑時進度檔的 `<id>` 跟殘留的不同）。
fn run_as(fx: &Fx, req: &Request<'_>, argv: &[&str], run_id: &str) -> Out {
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
    let mut channel = Channel::new(&fx.ctl, header(fx.protocol.get()));
    let code = {
        let mut env = Env {
            dir: &fx.dir,
            host_root: HOST_ROOT,
            inbox: &fx.inbox,
            channel: &mut channel,
            poll: Duration::from_millis(2),
            run_log: "/h/proj/.vendor_kit/log/r1.jsonl",
            argv: &argv,
            run_id,
            written_by: WRITTEN_BY,
            stdout: &mut stdout,
            diags: &mut diags,
            log: &mut log,
        };
        run(req, argv.iter().any(|a| a == "--dry-run"), &mut env)
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

fn dev_engine(fx: &Fx, image: &str) -> Out {
    run_with(
        fx,
        &Request::DevEngine {
            image: OsStr::new(image),
        },
        &["dev", "--engine", "-i", image],
    )
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
fn dev_again_after_undev_removed_the_last_override() {
    // undev 解除最後一個覆寫後，version.local.toml 留下空的 [tools]；再 dev 不是少寫。
    let fx = Fx::new();
    assert_eq!(dev(&fx, "tool", "dev/tool").code, 0);
    assert_eq!(undev(&fx, "tool").code, 0);
    assert_eq!(fx.local().unwrap().tool("tool"), None);

    let out = dev(&fx, "tool", "dev/tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(fx.entry(), DEV_GEN);
    assert_eq!(fx.local().unwrap().tool("tool"), Some("dev/tool"));
    assert_eq!(out.events(), LANDED);
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

    // 以下各情境在同一個安裝目錄串著跑，每次先 undev。
    // 以 `..` 跑出安裝目錄的相對路徑：留相對路徑；主機路徑接在 --host-root 後面，`..` 留給主機解析。
    assert_eq!(undev(&fx, "tool").code, 0);
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
    assert_eq!(undev(&fx, "tool").code, 0);
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

/// 本機引擎 image 的 LABEL：介面版區間 `[floor, current]`（其他 LABEL 不看）。
fn engine_labels(floor: &str, current: &str) -> String {
    format!(
        r#""vendor_kit.protocol.floor":"{floor}","vendor_kit.protocol.current":"{current}","vendor_kit.schema.max":"1""#
    )
}

/// `dev --engine -i` 驗過 LABEL 才寫引擎行，入口檔不動；重複同一個 image 未變更；之後 `undev --engine` 拿掉。
#[test]
fn dev_engine_checks_the_interface_version_and_writes_the_engine_override() {
    let fx = Fx::new();
    fx.registry
        .borrow_mut()
        .images
        .push(Image::engine("vendor_kit:dev", &engine_labels("1", "2")));
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    let entry = fx.entry();

    let out = dev_engine(&fx, "vendor_kit:dev");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(out.ops, ["inspect vendor_kit:dev"]);
    assert_eq!(
        out.stdout,
        "The engine now uses the local image vendor_kit:dev (local override).\n"
    );
    assert_eq!(fx.local().unwrap().engine(), Some("vendor_kit:dev"));
    assert_eq!(fx.entry(), entry);
    assert_eq!(fs::read(fx.dir.version_toml()).unwrap(), lock);
    assert_eq!(out.events(), LANDED);
    assert!(fx.progress_files().is_empty());

    let before = fx.snapshot();
    let out = dev_engine(&fx, "vendor_kit:dev");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(out.ops.is_empty(), "{:?}", out.ops);
    assert_eq!(
        out.stdout,
        "The engine already uses the local image vendor_kit:dev. No changes were made.\n"
    );
    assert_eq!(fx.snapshot(), before);

    let out = undev_engine(&fx);
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(fx.local().unwrap().engine(), None);
    assert_eq!(fx.entry(), entry);
}

/// 已有另一個 image 的引擎覆寫：VK0050，不 inspect、不取代。
#[test]
fn dev_engine_with_a_different_image_is_vk0050() {
    let fx = Fx::new();
    fx.write_local("vendor_kit = \"vendor_kit:old\"\n");
    let before = fx.snapshot();
    let out = dev_engine(&fx, "vendor_kit:dev");
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0050]: A different local override is already active for vendor_kit. Run first: just vendor_kit undev --engine\n"
    );
    assert!(out.ops.is_empty(), "{:?}", out.ops);
    assert_eq!(fx.snapshot(), before);
}

/// 比薄殼舊的引擎（區間上限低於薄殼的 P）：草稿碼登錄前以 VK0056 停下（[`DRAFT_ENGINE_TOO_OLD`]），不寫檔。
#[test]
fn dev_engine_older_than_the_shell_is_refused_with_the_draft_code() {
    let fx = Fx::new();
    fx.protocol.set(2);
    fx.registry
        .borrow_mut()
        .images
        .push(Image::engine("vendor_kit:old", &engine_labels("1", "1")));
    let before = fx.snapshot();
    let out = dev_engine(&fx, "vendor_kit:old");
    assert_eq!(out.code, 2, "{}", out.stderr);
    assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(
        out.stderr.contains(&format!(
            "accepts interface versions [1, 1], older than the shell interface version 2, \
             and must not regenerate the shell; {DRAFT_ENGINE_TOO_OLD}"
        )),
        "{}",
        out.stderr
    );
    assert_eq!(out.ops, ["inspect vendor_kit:old"]);
    assert!(out.events().is_empty());
    assert_eq!(fx.snapshot(), before);
}

/// 區間含薄殼的 P 的較舊引擎照樣接受（ADR-0010：允許跑）。
#[test]
fn dev_engine_whose_range_still_contains_the_shell_is_accepted() {
    let fx = Fx::new();
    fx.protocol.set(2);
    fx.registry
        .borrow_mut()
        .images
        .push(Image::engine("vendor_kit:old", &engine_labels("2", "3")));
    let out = dev_engine(&fx, "vendor_kit:old");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(fx.local().unwrap().engine(), Some("vendor_kit:old"));
}

/// 引用不合法、inspect 失敗、LABEL 缺或值不合、區間下限高於薄殼的 P：都以 VK0056 停下，不寫檔。
#[test]
fn dev_engine_problems_stop_with_vk0056_without_writing() {
    let fx = Fx::new();
    {
        let mut registry = fx.registry.borrow_mut();
        for (reference, labels) in [
            ("vk:none", String::new()),
            ("vk:zero", engine_labels("01", "1")),
            ("vk:flip", engine_labels("2", "1")),
            ("vk:new", engine_labels("2", "3")),
        ] {
            registry.images.push(Image::engine(reference, &labels));
        }
        let mut no_config = Image::engine("vk:bare", "");
        no_config.labels = None;
        registry.images.push(no_config);
    }
    let before = fx.snapshot();
    let cases: [(&str, &str, &[&str]); 7] = [
        ("Vk:Dev", "\"Vk:Dev\" is not a valid image reference", &[]),
        (
            "vk:gone",
            "could not inspect the local engine image vk:gone (exit 1)",
            &["inspect vk:gone"],
        ),
        (
            "vk:none",
            "has no vendor_kit.protocol.floor label",
            &["inspect vk:none"],
        ),
        (
            "vk:bare",
            "has no vendor_kit.protocol.floor label",
            &["inspect vk:bare"],
        ),
        (
            "vk:zero",
            "has vendor_kit.protocol.floor=\"01\"",
            &["inspect vk:zero"],
        ),
        (
            "vk:flip",
            "vendor_kit.protocol.floor=2 above vendor_kit.protocol.current=1",
            &["inspect vk:flip"],
        ),
        (
            "vk:new",
            "interface versions [2, 3] are all newer than the shell interface version 1 is not supported yet",
            &["inspect vk:new"],
        ),
    ];
    for (image, what, ops) in cases {
        let out = dev_engine(&fx, image);
        assert_eq!(out.code, 2, "{image}: {}", out.stderr);
        assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
        assert!(out.stderr.contains(what), "{image}: {}", out.stderr);
        assert_eq!(out.ops, ops, "{image}");
        assert!(out.events().is_empty());
    }
    assert_eq!(fx.snapshot(), before);
}

// ---- 恢復 ----

/// 殘留的引擎 `dev`（覆寫還沒寫進檔就斷了）：同一個 image 重跑時併入，不再 inspect。
#[test]
fn residual_dev_of_the_engine_is_completed() {
    let fx = Fx::new();
    fx.residual(
        DEV_VERB,
        &["dev", "--engine", "-i", "vendor_kit:dev"],
        &[(TARGET_KEY, ENGINE_TARGET), (IMAGE_KEY, "vendor_kit:dev")],
    );
    let entry = fx.entry();
    let out = run_as(
        &fx,
        &Request::DevEngine {
            image: OsStr::new("vendor_kit:dev"),
        },
        &["dev", "--engine", "-i", "vendor_kit:dev"],
        "r2",
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(out.ops.is_empty(), "{:?}", out.ops);
    assert_eq!(
        out.stdout,
        "The engine now uses the local image vendor_kit:dev (local override).\n\
         Completed the interrupted dev recorded in .vendor_kit/.tmp.dev.r0.toml.\n"
    );
    assert_eq!(fx.local().unwrap().engine(), Some("vendor_kit:dev"));
    assert_eq!(fx.entry(), entry);
    assert!(fx.progress_files().is_empty());
}

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
        ["VK0054", "VK0053"],
        "{}",
        out.stderr
    );
    assert!(
        out.stderr.contains(
            "Operation install in /h/proj is incomplete. Run again: just vendor_kit install\n"
        ),
        "{}",
        out.stderr
    );
    assert!(
        out.stderr.contains(
            "The undev operation for other is incomplete. Run again: just vendor_kit undev other\n"
        ),
        "{}",
        out.stderr
    );
    assert!(out.events().is_empty());
    assert_eq!(fx.snapshot(), before);
}

/// `dev` 遇到對象不同的 `dev`、`undev` 殘留（#372 N81）：VK0054、VK0053，下一步是重跑原指令；不恢復、不刪。
#[test]
fn residual_of_another_target_is_vk0053_or_vk0054() {
    let fx = Fx::new();
    fx.residual(
        DEV_VERB,
        &["dev", "other", "-p", "dev/it's"],
        &[(TARGET_KEY, "other"), (PATH_KEY, "dev/it's")],
    );
    fx.residual(
        UNDEV_VERB,
        &["undev", "--engine"],
        &[(TARGET_KEY, ENGINE_TARGET)],
    );
    let before = fx.snapshot();
    let out = dev(&fx, "tool", "dev/tool");
    assert_eq!(out.code, 2);
    let mut lines: Vec<&str> = out.stderr.lines().collect();
    lines.sort_unstable();
    assert_eq!(
        lines,
        [
            "vendor_kit: error[VK0053]: The undev operation for vendor_kit is incomplete. Run again: just vendor_kit undev --engine",
            "vendor_kit: error[VK0054]: Operation dev in /h/proj is incomplete. Run again: just vendor_kit dev other -p 'dev/it'\\''s'",
        ]
    );
    assert!(out.events().is_empty());
    assert!(out.ops.is_empty(), "{:?}", out.ops);
    assert_eq!(fx.snapshot(), before);
}

/// 殘留的 `add` 導入的工具（不在版本鎖定行）。
const FRESH: &str = "ghcr.io/acme/fresh:v2.0.0@sha256:5555555555555555555555555555555555555555555555555555555555555555";
const FRESH_PINNED: &str =
    "ghcr.io/acme/fresh@sha256:5555555555555555555555555555555555555555555555555555555555555555";
/// 恢復殘留的 `add`、`upgrade` 落地時的里程碑事件（寫版本鎖定行）。
const RECOVERY_LANDED: [&str; 4] = [
    "writes_started",
    "lock_line_write_started",
    "lock_line_written",
    "progress_removed",
];
/// 恢復殘留的 `add fresh` 之後，入口檔多出的那一行。
const FRESH_LINE: &str = "mod? fresh '../cache/fresh/just/fresh.just'\n";

impl Fx {
    /// 寫一份殘留的 `add` 或工具 `upgrade` 進度檔：`[<verb>]` 下記對象、版本鎖定行的值與
    /// 有沒有要寫的初始檔（`add` 是 `repo`、`image`、`repo_files`；`upgrade` 是 `target`、`image`、`init_files`）。
    fn recoverable(&self, verb: &str, repo: &str, image: &str, files: bool) {
        let (target, flag) = if verb == ADD_VERB {
            (ADD_REPO, ADD_REPO_FILES)
        } else {
            (progress::upgrade::TARGET, progress::upgrade::INIT_FILES)
        };
        let mut p = Progress::new(verb, "r0", &[verb, repo]).unwrap();
        let doc = p.document_mut();
        doc.set(&[verb, target], repo).unwrap();
        doc.set(&[verb, "image"], image).unwrap();
        doc.set(&[verb, flag], files).unwrap();
        p.create(&self.dir, WRITTEN_BY).unwrap();
    }

    /// 本機有 `fresh` 的 image（殘留的 `add` 只 inspect、不 pull），交付 `files` 這幾個 `<ns>`。
    fn fresh_image(&self, namespaces: &[&str]) {
        let mut image = Image::new(FRESH_PINNED, true, "");
        image.files = namespaces
            .iter()
            .map(|ns| (format!("just/{ns}.just"), "f:\n    echo f\n".to_owned()))
            .collect();
        self.registry.borrow_mut().images.push(image);
    }

    fn lock_line(&self, repo: &str) -> Option<String> {
        LockFile::load_from(&self.dir)
            .unwrap()
            .unwrap()
            .tool(repo)
            .map(ToString::to_string)
    }
}

/// `dev` 遇到另一個工具殘留的 `add`（04：可寫 recipe 先恢復再做自己的事）：恢復先落地（`cache/`、印記、
/// 入口檔、版本鎖定行），再開這次的覆寫；殘留的進度檔刪掉，以 0 結束。
#[test]
fn residual_add_of_another_tool_is_recovered_before_dev() {
    let fx = Fx::new();
    fx.fresh_image(&["fresh"]);
    fx.recoverable(ADD_VERB, "fresh", FRESH, false);
    let out = dev(&fx, "tool", "dev/tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.ops,
        [
            format!("inspect {FRESH_PINNED}"),
            format!("extract {IMAGE_ID} tool1"),
        ]
    );
    assert_eq!(
        out.stdout,
        format!(
            "Completed the interrupted add of fresh v2.0.0 ({FRESH}).\n\
             tool now uses the local source dev/tool (local override).\n\
             Updated .vendor_kit/gen/tools.just.\n"
        )
    );
    assert_eq!(fx.lock_line("fresh").as_deref(), Some(FRESH));
    assert_eq!(fx.entry(), format!("{FRESH_LINE}{DEV_GEN}"));
    assert_eq!(fx.local().unwrap().tool("tool"), Some("dev/tool"));
    let cache = fx.dir.tool_cache("fresh").unwrap();
    assert!(cache.join("just/fresh.just").is_file());
    let stamp = stamp::Stamp::load(&stamp::tool_file(&fx.dir, "fresh"))
        .unwrap()
        .unwrap();
    assert_eq!(stamp.version(), FRESH);
    assert!(fx.progress_files().is_empty());
    // 恢復（寫版本鎖定行）與這次各走一次落地。
    assert_eq!(out.events(), [&RECOVERY_LANDED[..], &LANDED[..]].concat());
}

/// `dev` 的對象就是殘留 `add` 導入到一半的工具：先恢復，版本鎖定行有它了，不報 VK0046。
#[test]
fn dev_of_a_tool_whose_add_is_incomplete_recovers_it_first() {
    let fx = Fx::new();
    fx.fresh_image(&["fresh"]);
    fx.recoverable(ADD_VERB, "fresh", FRESH, false);
    let src = fx.root().join("dev/fresh/just");
    fs::create_dir_all(&src).unwrap();
    fs::write(src.join("fresh.just"), "g:\n    echo g\n").unwrap();
    let out = dev(&fx, "fresh", "dev/fresh");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(fx.lock_line("fresh").as_deref(), Some(FRESH));
    assert_eq!(fx.local().unwrap().tool("fresh"), Some("dev/fresh"));
    assert_eq!(
        fx.entry(),
        format!("mod? fresh '../../dev/fresh/just/fresh.just'\n{GEN}")
    );
    assert!(fx.progress_files().is_empty());
}

/// `undev` 的對象有殘留的 `upgrade`：照 engine/upgrade 的恢復 pull 後取件一次，恢復換好 `cache/` 與鎖定行，
/// 解除覆寫時直接指回去，不再取件。
#[test]
fn undev_with_a_residual_upgrade_of_the_same_tool_fetches_once() {
    let fx = Fx::new();
    fx.write_local("\n[tools]\ntool = \"dev/tool\"\n");
    fs::write(fx.dir.gen_dir().join(txn::TOOLS_JUST), DEV_GEN).unwrap();
    fx.registry
        .borrow_mut()
        .images
        .push(Image::new(NEW_PINNED, false, "n:\n    echo n\n"));
    fx.recoverable(progress::upgrade::VERB, "tool", NEW_TOOL, false);
    let out = undev(&fx, "tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.ops,
        [
            format!("inspect {NEW_PINNED}"),
            format!("pull {NEW_PINNED}"),
            format!("inspect {NEW_PINNED}"),
            format!("extract {IMAGE_ID} tool1"),
        ]
    );
    assert_eq!(
        out.stdout,
        format!(
            "Completed the interrupted upgrade of tool to v1.3.0 ({NEW_TOOL}).\n\
             Removed the local override of tool; tool uses v1.3.0 ({NEW_TOOL}).\n\
             Updated .vendor_kit/gen/tools.just.\n"
        )
    );
    assert_eq!(fx.lock_line("tool").as_deref(), Some(NEW_TOOL));
    assert_eq!(fx.stamp_version(), NEW_TOOL);
    assert_eq!(fx.cached_text(), "n:\n    echo n\n");
    assert_eq!(fx.entry(), GEN);
    assert_eq!(fx.local().unwrap().tool("tool"), None);
    assert!(fx.progress_files().is_empty());
}

/// 這次本身未變更（重複 `dev` 同來源）也照樣落地恢復；入口檔照檔上的覆寫算。
#[test]
fn unchanged_dev_still_lands_the_recovery() {
    let fx = Fx::new();
    fx.write_local("\n[tools]\ntool = \"dev/tool\"\n");
    fs::write(fx.dir.gen_dir().join(txn::TOOLS_JUST), DEV_GEN).unwrap();
    fx.fresh_image(&["fresh"]);
    fx.recoverable(ADD_VERB, "fresh", FRESH, false);
    let out = dev(&fx, "tool", "dev/tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "Completed the interrupted add of fresh v2.0.0 ({FRESH}).\n\
             tool already uses the local source dev/tool. No changes were made.\n"
        )
    );
    assert_eq!(fx.lock_line("fresh").as_deref(), Some(FRESH));
    assert_eq!(fx.entry(), format!("{FRESH_LINE}{DEV_GEN}"));
    assert!(fx.progress_files().is_empty());
    // 這次沒有要寫的，只有恢復那一次落地。
    assert_eq!(out.events(), RECOVERY_LANDED);
}

/// 這次停下（VK0050）時恢復也不落地：除了取件的暫存處，什麼都不寫，殘留照留。
#[test]
fn a_stop_keeps_the_residual_add_and_writes_nothing() {
    let fx = Fx::new();
    fx.write_local("\n[tools]\ntool = \"dev/tool\"\n");
    fx.fresh_image(&["fresh"]);
    fx.recoverable(ADD_VERB, "fresh", FRESH, false);
    let before = fx.snapshot();
    let out = dev(&fx, "tool", "dev/elsewhere");
    assert_eq!(out.code, 2);
    assert_eq!(diag_codes(&out.stderr), ["VK0050"], "{}", out.stderr);
    assert!(out.events().is_empty());
    assert_eq!(fx.snapshot(), before);
    assert_eq!(fx.progress_files(), ["add.r0"]);
}

/// 預演：恢復照樣取件、驗證，只印會完成哪一份，殘留照留。
#[test]
fn dry_run_only_reports_the_recovery() {
    let fx = Fx::new();
    fx.fresh_image(&["fresh"]);
    fx.recoverable(ADD_VERB, "fresh", FRESH, false);
    let before = fx.snapshot();
    let out = run_with(
        &fx,
        &Request::DevTool {
            repo: "tool",
            path: OsStr::new("dev/tool"),
        },
        &["dev", "tool", "-p", "dev/tool", "--dry-run"],
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "Would complete the interrupted add of fresh v2.0.0 ({FRESH}).\n\
             tool would use the local source dev/tool (local override).\n\
             Would update .vendor_kit/gen/tools.just.\n\
             Dry run: no changes were made.\n"
        )
    );
    assert!(out.events().is_empty());
    assert_eq!(fx.snapshot(), before);
}

/// 恢復時撞名照 engine/add 判（VK0030），在任何寫入之前停下；根 `justfile` 的 recipe 也算。
#[test]
fn residual_add_whose_namespace_collides_is_vk0030() {
    for (namespaces, justfile) in [
        (&["fresh", "other"][..], None),
        (&["fresh"][..], Some("fresh:\n    echo r\n")),
    ] {
        let fx = Fx::new();
        if let Some(text) = justfile {
            fs::write(fx.root().join("justfile"), text).unwrap();
        }
        fx.fresh_image(namespaces);
        fx.recoverable(ADD_VERB, "fresh", FRESH, false);
        let before = fx.snapshot();
        let out = dev(&fx, "tool", "dev/tool");
        assert_eq!(out.code, 2);
        assert_eq!(diag_codes(&out.stderr), ["VK0030"], "{}", out.stderr);
        assert!(out.events().is_empty());
        assert_eq!(fx.snapshot(), before);
    }
}

/// 殘留 `add` 的 image 本機沒有：照 engine/add 的恢復不 pull，VK0055；什麼都不寫。
#[test]
fn residual_add_whose_image_is_missing_is_vk0055() {
    let fx = Fx::new();
    fx.recoverable(ADD_VERB, "fresh", FRESH, false);
    let before = fx.snapshot();
    let out = dev(&fx, "tool", "dev/tool");
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        format!(
            "vendor_kit: error[VK0055]: Cannot access {FRESH} for fresh: docker inspect exited with 1. The requested operation did not complete.\n"
        )
    );
    assert_eq!(out.ops, [format!("inspect {FRESH_PINNED}")]);
    assert_eq!(fx.snapshot(), before);
}

/// 還恢復不了的殘留：`add` 要寫 repo 檔、工具 `upgrade` 寫初始檔、引擎 `upgrade`、欄位不齊、`sync`。照舊以
/// VK0056 停下，在任何 docker 動作與寫入之前。
#[test]
fn residuals_that_cannot_be_recovered_yet_are_gaps() {
    type Setup<'a> = &'a dyn Fn(&Fx);
    let cases: [(Setup<'_>, &str); 5] = [
        (
            &|fx| fx.recoverable(ADD_VERB, "fresh", FRESH, true),
            "which writes repo files from init.toml",
        ),
        (
            &|fx| fx.recoverable(progress::upgrade::VERB, "tool", NEW_TOOL, true),
            "which writes init files",
        ),
        (
            &|fx| fx.recoverable(progress::upgrade::VERB, ENGINE_TARGET, ENGINE, false),
            "incomplete engine upgrade",
        ),
        (
            &|fx| fx.residual(ADD_VERB, &["add", "fresh"], &[]),
            "without the [add] fields",
        ),
        (
            &|fx| fx.residual(SYNC_VERB, &["sync"], &[]),
            "incomplete sync operation",
        ),
    ];
    for (write, what) in cases {
        let fx = Fx::new();
        write(&fx);
        let before = fx.snapshot();
        let out = dev(&fx, "tool", "dev/tool");
        assert_eq!(out.code, 2, "{what}");
        assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
        assert!(out.stderr.contains(what), "{what}: {}", out.stderr);
        assert!(out.ops.is_empty(), "{what}: {:?}", out.ops);
        assert_eq!(fx.snapshot(), before);
    }
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
fn dev_of_a_tool_not_in_the_lock_lines_is_vk0046() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let out = dev(&fx, "missing", "dev/tool");
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0046]: Tool missing is not in the lock version lines. The requested operation did not complete.\n"
    );
    assert!(out.ops.is_empty(), "{:?}", out.ops);
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

/// `dev` 的本機開發來源撞到其他工具或保留名（#372 N79）：每個撞到的名字各一則 VK0030，不寫檔。
#[test]
fn dev_namespace_collision_is_vk0030() {
    let fx = Fx::new();
    fs::write(fx.root().join("dev/tool/just/other.just"), "").unwrap();
    fs::write(fx.root().join("dev/tool/just/vendor_kit.just"), "").unwrap();
    let before = fx.snapshot();
    let out = dev(&fx, "tool", "dev/tool");
    assert_eq!(out.code, 2);
    assert_eq!(
        out.stderr,
        "vendor_kit: error[VK0030]: Cannot add tool: namespace other is already used by other.\n\
         vendor_kit: error[VK0030]: Cannot add tool: namespace vendor_kit is already used by vendor_kit.\n"
    );
    assert!(out.events().is_empty());
    assert_eq!(fx.snapshot(), before);
}

// ---- undev 取件 ----

const VK0053_TOOL: &str = "vendor_kit: error[VK0053]: The undev operation for tool is incomplete. Run again: just vendor_kit undev tool\n";

#[test]
fn undev_after_the_lock_line_changed_fetches_after_removing_the_override() {
    let fx = Fx::new();
    assert_eq!(dev(&fx, "tool", "dev/tool").code, 0);
    fx.set_lock_line(NEW_TOOL);
    let lock = fs::read(fx.dir.version_toml()).unwrap();
    fx.registry
        .borrow_mut()
        .images
        .push(Image::new(NEW_PINNED, false, "new:\n    echo new\n"));

    let out = undev(&fx, "tool");
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(
        out.stdout,
        format!(
            "Removed the local override of tool; tool uses v1.3.0 ({NEW_TOOL}).\n\
             Fetched tool v1.3.0 ({NEW_TOOL}).\n\
             Updated .vendor_kit/gen/tools.just.\n"
        )
    );
    // 本機沒有：以帶 digest 的引用 pull 再 inspect，再以 image ID extract。
    assert_eq!(
        out.ops,
        [
            format!("inspect {NEW_PINNED}"),
            format!("pull {NEW_PINNED}"),
            format!("inspect {NEW_PINNED}"),
            format!("extract {IMAGE_ID} tool1"),
        ]
    );
    assert_eq!(fx.cached_text(), "new:\n    echo new\n");
    assert_eq!(fx.stamp_version(), NEW_TOOL);
    assert_eq!(fx.entry(), GEN);
    assert_eq!(fx.local().unwrap().tool("tool"), None);
    assert_eq!(out.events(), LANDED);
    assert!(fx.progress_files().is_empty());
    // 版本鎖定行不動。
    assert_eq!(fs::read(fx.dir.version_toml()).unwrap(), lock);
}

#[test]
fn undev_refetches_a_cache_that_does_not_match_its_stamp_or_has_no_stamp() {
    for what in ["content changed", "stamp missing"] {
        let fx = Fx::new();
        assert_eq!(dev(&fx, "tool", "dev/tool").code, 0, "{what}");
        if what == "content changed" {
            fs::write(
                fx.dir.tool_cache("tool").unwrap().join("just/tool.just"),
                "changed\n",
            )
            .unwrap();
        } else {
            fs::remove_file(stamp::tool_file(&fx.dir, "tool")).unwrap();
        }
        fx.registry
            .borrow_mut()
            .images
            .push(Image::new(PINNED, true, CACHED_TEXT));
        let out = undev(&fx, "tool");
        assert_eq!(out.code, 0, "{what}: {}", out.stderr);
        assert_eq!(
            out.ops,
            [
                format!("inspect {PINNED}"),
                format!("extract {IMAGE_ID} tool1")
            ],
            "{what}"
        );
        assert_eq!(fx.cached_text(), CACHED_TEXT, "{what}");
        assert_eq!(fx.stamp_version(), TOOL, "{what}");
        assert_eq!(fx.entry(), GEN, "{what}");
        assert_eq!(fx.local().unwrap().tool("tool"), None, "{what}");
        assert!(fx.progress_files().is_empty(), "{what}");
    }
}

#[test]
fn undev_whose_fetch_fails_is_vk0053_without_writing() {
    for what in ["docker fails", "digest mismatch"] {
        let fx = Fx::new();
        assert_eq!(dev(&fx, "tool", "dev/tool").code, 0, "{what}");
        fx.set_lock_line(NEW_TOOL);
        if what == "digest mismatch" {
            let mut image = Image::new(NEW_PINNED, true, "new:\n    echo new\n");
            image.repo_digest = PINNED.to_owned();
            fx.registry.borrow_mut().images.push(image);
        }
        let before = fx.snapshot();
        let out = undev(&fx, "tool");
        assert_eq!(out.code, 2, "{what}");
        assert_eq!(out.stderr, VK0053_TOOL, "{what}");
        assert_eq!(out.stdout, "", "{what}");
        // 取件在寫任何檔之前：覆寫照留、沒有進度檔，重跑同一個 undev 就是從頭再做。
        assert_eq!(fx.snapshot(), before, "{what}");
        assert!(out.events().is_empty(), "{what}: {:?}", out.events());
        assert_eq!(fx.local().unwrap().tool("tool"), Some("dev/tool"), "{what}");
    }
}

#[test]
fn undev_whose_fetched_content_does_not_match_the_stamp_is_a_gap() {
    let fx = Fx::new();
    assert_eq!(dev(&fx, "tool", "dev/tool").code, 0);
    fs::write(
        fx.dir.tool_cache("tool").unwrap().join("just/tool.just"),
        "changed\n",
    )
    .unwrap();
    // 同一個版本取到的內容跟既有印記不符：重跑也補不好。
    fx.registry
        .borrow_mut()
        .images
        .push(Image::new(PINNED, true, "other:\n    echo other\n"));
    let before = fx.snapshot();
    let out = undev(&fx, "tool");
    assert_eq!(out.code, 2);
    assert_eq!(diag_codes(&out.stderr), ["VK0056"], "{}", out.stderr);
    assert!(
        out.stderr.contains("does not match its existing stamp"),
        "{}",
        out.stderr
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn undev_interrupted_after_removing_the_override_is_vk0053_and_a_rerun_completes() {
    let fx = Fx::new();
    assert_eq!(dev(&fx, "tool", "dev/tool").code, 0);
    fx.set_lock_line(NEW_TOOL);
    fx.registry
        .borrow_mut()
        .images
        .push(Image::new(NEW_PINNED, true, "new:\n    echo new\n"));
    // 換 cache/ 那一步失敗：txn 先清掉的暫存目錄位置被一般檔占住。
    let blocker = fx.dir.cache_dir().join(".tmp.tool.new");
    fs::write(&blocker, "x").unwrap();

    let out = undev(&fx, "tool");
    assert_eq!(out.code, 2);
    assert_eq!(out.stderr, VK0053_TOOL);
    // 覆寫已解除，cache/、印記、入口檔還沒同步，進度檔留著。
    assert_eq!(fx.local().unwrap().tool("tool"), None);
    assert_eq!(fx.cached_text(), CACHED_TEXT);
    assert_eq!(fx.stamp_version(), TOOL);
    assert_eq!(fx.entry(), DEV_GEN);
    assert_eq!(fx.progress_files(), ["undev.r1"]);

    // 重跑原 undev：併進殘留的那次，取件、換 cache/、指回去。
    fs::remove_file(&blocker).unwrap();
    let out = run_as(
        &fx,
        &Request::UndevTool { repo: "tool" },
        &["undev", "tool"],
        "r2",
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(fx.cached_text(), "new:\n    echo new\n");
    assert_eq!(fx.stamp_version(), NEW_TOOL);
    assert_eq!(fx.entry(), GEN);
    assert!(fx.progress_files().is_empty());
    assert!(
        out.stdout.ends_with(
            "Completed the interrupted undev recorded in .vendor_kit/.tmp.undev.r1.toml.\n"
        ),
        "{}",
        out.stdout
    );
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
fn inspect_output_reads_the_id_and_repo_digests() {
    let json = format!("[{{\"Id\":\"{IMAGE_ID}\",\"RepoDigests\":[\"{PINNED}\"],\"Size\":1}}]");
    let i = parse_inspect(json.as_bytes()).unwrap();
    assert_eq!(i.id, IMAGE_ID);
    assert_eq!(i.repo_digests, [PINNED]);
    let none = parse_inspect(br#"[{"Id":"sha256:1","RepoDigests":null}]"#).unwrap();
    assert!(none.repo_digests.is_empty());
    assert!(parse_inspect(b"[]").is_err());
    assert!(parse_inspect(b"{}").is_err());
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

// ---- 預演（--dry-run，#372 N11） ----

#[test]
fn dev_and_undev_dry_run_print_the_plan_and_write_nothing() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let p = OsString::from("dev/tool");
    let out = run_with(
        &fx,
        &Request::DevTool {
            repo: "tool",
            path: p.as_os_str(),
        },
        &["dev", "tool", "-p", "dev/tool", "--dry-run"],
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    assert_eq!(
        out.stdout,
        "tool would use the local source dev/tool (local override).\n\
         Would update .vendor_kit/gen/tools.just.\n\
         Dry run: no changes were made.\n"
    );
    assert!(out.events().is_empty());
    assert_eq!(fx.snapshot(), before);

    // 開著覆寫、鎖定行換了：預演照樣取件（docker 動作照送）但不換 cache/。
    assert_eq!(dev(&fx, "tool", "dev/tool").code, 0);
    fx.set_lock_line(NEW_TOOL);
    fx.registry
        .borrow_mut()
        .images
        .push(Image::new(NEW_PINNED, false, "new:\n    echo new\n"));
    let before = fx.snapshot();
    let out = run_with(
        &fx,
        &Request::UndevTool { repo: "tool" },
        &["undev", "tool", "--dry-run"],
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        format!(
            "Would remove the local override of tool; tool would use v1.3.0 ({NEW_TOOL}).\n\
             Would fetch tool v1.3.0 ({NEW_TOOL}).\n\
             Would update .vendor_kit/gen/tools.just.\n\
             Dry run: no changes were made.\n"
        )
    );
    assert_eq!(
        out.ops.last().unwrap(),
        &format!("extract {IMAGE_ID} tool1")
    );
    assert!(out.events().is_empty());
    assert_eq!(fx.snapshot(), before);
    assert_eq!(fx.local().unwrap().tool("tool"), Some("dev/tool"));
}

#[test]
fn engine_dev_and_undev_dry_run_write_nothing() {
    let fx = Fx::new();
    fx.registry
        .borrow_mut()
        .images
        .push(Image::engine("vendor_kit:dev", &engine_labels("1", "2")));
    let before = fx.snapshot();
    let out = run_with(
        &fx,
        &Request::DevEngine {
            image: OsStr::new("vendor_kit:dev"),
        },
        &["dev", "--engine", "-i", "vendor_kit:dev", "--dry-run"],
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.ops, ["inspect vendor_kit:dev"]);
    assert_eq!(
        out.stdout,
        "The engine would use the local image vendor_kit:dev (local override).\n\
         Dry run: no changes were made.\n"
    );
    assert!(out.events().is_empty());
    assert_eq!(fx.snapshot(), before);

    // 沒有覆寫：未變更照印，最後一行照樣是預演的。
    let out = run_with(
        &fx,
        &Request::UndevEngine,
        &["undev", "--engine", "--dry-run"],
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "The engine has no local override. No changes were made.\n\
         Dry run: no changes were made.\n"
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn dry_run_keeps_the_residual_progress_file() {
    let fx = Fx::new();
    fx.write_local("");
    fs::write(fx.dir.gen_dir().join(txn::TOOLS_JUST), DEV_GEN).unwrap();
    fx.residual(UNDEV_VERB, &["undev", "tool"], &[(TARGET_KEY, "tool")]);
    let before = fx.snapshot();
    let out = run_with(
        &fx,
        &Request::UndevTool { repo: "tool" },
        &["undev", "tool", "--dry-run"],
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(
        out.stdout.ends_with(
            "Would complete the interrupted undev recorded in .vendor_kit/.tmp.undev.r0.toml.\n\
             Dry run: no changes were made.\n"
        ),
        "{}",
        out.stdout
    );
    assert_eq!(fx.progress_files().len(), 1);
    assert_eq!(fx.snapshot(), before);
}

/// 同一次有對象相同的 `dev` 殘留（併入）與另一個工具的 `add` 殘留（先恢復）：兩份都完成、都刪掉。
#[test]
fn merged_dev_and_recovered_add_are_both_completed() {
    let fx = Fx::new();
    fx.residual(
        DEV_VERB,
        &["dev", "tool", "-p", "dev/tool"],
        &[(TARGET_KEY, "tool"), (PATH_KEY, "dev/tool")],
    );
    fx.fresh_image(&["fresh"]);
    fx.recoverable(ADD_VERB, "fresh", FRESH, false);
    let out = run_as(
        &fx,
        &Request::DevTool {
            repo: "tool",
            path: OsStr::new("dev/tool"),
        },
        &["dev", "tool", "-p", "dev/tool"],
        "r2",
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert!(
        out.stdout
            .starts_with("Completed the interrupted add of fresh v2.0.0"),
        "{}",
        out.stdout
    );
    assert!(
        out.stdout
            .ends_with("Completed the interrupted dev recorded in .vendor_kit/.tmp.dev.r0.toml.\n"),
        "{}",
        out.stdout
    );
    assert_eq!(fx.lock_line("fresh").as_deref(), Some(FRESH));
    assert_eq!(fx.entry(), format!("{FRESH_LINE}{DEV_GEN}"));
    assert!(fx.progress_files().is_empty());
}
