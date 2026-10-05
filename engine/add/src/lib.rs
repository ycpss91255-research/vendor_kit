//! `add` 指令（04 指令表 `add <repo>`、`add <repo>@<tag>`、`add <repo> -i <image>`）：從參數到落地。
//!
//! 呼叫端（入口 `vendor_kit`）已解析好參數、判過安裝目錄（VK0028），並接好執行紀錄與 `plan` 往返。
//! 這裡依序做：
//!
//! 1. `add vendor_kit` 看參數字面就擋（VK0057），不取件。
//! 2. 讀 `.vendor_kit/config.toml`（VK0059），在第一次取鎖之前（04 設定）。
//! 3. 取安裝目錄的排他鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束。
//! 4. 讀 `version.toml`。
//! 5. 恢復殘留的進度檔（04 成對與無害：可寫 recipe 先恢復再判是否重複）。恢復本身不寫 repo 檔，
//!    沒有要問的事；做法見 `Add::recover`。
//! 6. 判來源：目前只有 `-i <本機 image 引用>`（見「缺口」）。
//! 7. 已在版本鎖定行：tag 不同回 VK0045；完全相同 stdout 說明未變更，以 0 結束。
//! 8. 經 `plan` 協定請啟動器 `inspect`（讀 Id 與 RepoDigests；沒有對應的 digest 回 VK0031）
//!    再以 image ID `extract`；docker 動作失敗回 VK0055。
//! 9. `fetch::verify`：digest、dist 格式、逐檔指紋、`<ns>` 撞名（VK0030，對象是已裝工具、根
//!    `justfile` 的 recipe 與 module、保留名 `vendor_kit`）。
//! 10. `initfiles` 算出每個初始檔的動作與問題，`prompt` 一次問完：答否是正常取消（stdout 說明未變更，
//!     以 0 結束）；不能互動回 VK0002，除執行紀錄外不寫任何檔。
//! 11. 重驗暫存內容（ADR-0006 第三層），再經 `txn` 依序落地：`cache/<repo>/` 與印記、repo 檔、
//!     紀錄檔（metadata、基準版副本）、`gen/tools.just`、版本鎖定行，最後刪進度檔。
//! 12. stdout 列出改了什麼；初始檔的警告（VK0018 等）照印。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 印記放在 `.vendor_kit/cache/<repo>.stamp.toml`（[`stamp_file`]）：在 `cache/` 底下所以不進 git，
//!   又不在 `cache/<repo>/` 裡，換 `cache/<repo>/` 時不會被帶走。
//! - 基準版副本放在 `.vendor_kit/baseline/<repo>/<初始檔的 repo 相對路徑>`（[`baseline_file`]）。
//! - 進度檔 `.tmp.add.<run-id>.toml` 另記 `[add]` 表的 `repo`、`image`（版本鎖定行的值）與
//!   `repo_files`（這次有沒有要寫 repo 檔）。
//! - 取件的 slot 名固定是 [`SLOT`]；一次執行只取一個工具，恢復時另用 [`RECOVER_SLOT`]。
//! - stdout 的字句與詢問文字（英文）見 [`text`]。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - 不帶 `-i`：`<repo>` 對應到哪個 GHCR 路徑沒定，列版本與 tag→digest 要 registry client（計畫 D8），
//!   `plan` 的 `pull` 只收帶 digest 的引用。所以線上 `add` 還做不了，`pull` 也還用不到。
//! - `-i` 給 image tar：啟動器丟掉 `docker load` 的輸出，引擎不知道載入了哪個 image；`.digest` 檔的格式也沒定。
//! - `-i` 的引用沒有 tag、tag 不是 `vX.Y.Z`、已帶 digest、不在 ghcr.io，或 `-i` 與 `@<tag>` 並用。
//! - 工具交付 `init.toml`：初始檔的清單與 `strategy` 寫在哪裡、什麼格式都沒定（ADR-0003 只提到
//!   `strategy = "append"`），所以讀不出初始檔；沒有 `init.toml` 的工具就沒有初始檔、沒有詢問。
//! - 根 `justfile` 的 recipe 與 module 只做保守的逐行掃描（引擎 image 沒有 just），限制見 `justfile` 模組。
//! - 其他已裝工具的 `cache/<repo>/` 讀不到（例如全新 checkout 還沒 `sync`）：撞名判定與入口檔都要它。
//! - 同一個 tag 的版本鎖定行指向別的 digest；`<repo>` 不是 just 名稱；`initfiles` 判成缺口的檔。
//! - 殘留的進度檔不是 `add` 的（其他可寫 recipe 還沒實作），或殘留的 `add` 要寫 repo 檔。
//! - 中途寫檔失敗沒有代碼（計畫 G4）；dist 格式不符（G2）、指紋不符（G1）沒有代碼。
//! - `add` 不收 `-y`（#47），但 VK0002 的下一步指令照訊息表插入 `-y`。
//!
//! 這裡不直接碰 docker：docker 動作一律是 `plan` 協定的 op，由啟動器代做。

mod justfile;
mod source;
pub mod text;

#[cfg(test)]
mod tests;

use std::collections::BTreeMap;
use std::ffi::OsStr;
use std::fs;
use std::io::{self, BufRead, Write};
use std::path::{Path, PathBuf};
use std::time::Duration;

use config::{Config, ConfigError};
use diagnostics::{Diagnostic, Diagnostics, Message, Sink};
use fetch::{Candidate, Staged, Taken};
use filelock::{Lock, Mode};
use imageref::{ImageRef, Tag};
use initfiles::{FilePlan, InitFile, Strategy};
use layout::InstallDir;
use metadata::Metadata;
use plan::{Channel, ImageId, Op, Outcome, Slot, Tty};
use progress::Progress;
use prompt::{Consent, PromptError, TtyState};
use runlog::Target;
use txn::{Disk, RecordFile, RepoFile, ToolContent, Txn};
use version_file::LockFile;

pub use source::{Inspected, LocalRef, digest_for, parse_inspect, parse_local};

/// 進度檔的 `<verb>`。
pub const VERB: &str = "add";
/// 進度檔裡 `add` 自己的表。
pub const PROGRESS_TABLE: &str = "add";
/// 取件的 slot。
pub const SLOT: &str = "tool";
/// 恢復殘留 `add` 時取件的 slot。
pub const RECOVER_SLOT: &str = "recover";
/// 工具交付初始檔清單的檔名（格式未定，見模組說明的缺口）。
pub const INIT_TOML: &str = "init.toml";

/// 一次 `add` 的參數（`args::Command::Add`）。`--registry-token-file` 只在查版本清單時才讀，
/// 線上 `add` 還沒做，所以這裡不收。
#[derive(Debug, Clone, Copy)]
pub struct Request<'a> {
    pub repo: &'a str,
    pub tag: Option<Tag>,
    pub image: Option<&'a OsStr>,
}

/// 這次執行的環境：容器內的路徑、往返通道、終端狀態與輸出。
pub struct Env<'a, W: Write, S: Sink, L: Write> {
    /// 容器內的安裝目錄（`plan::mount::ROOT`）。
    pub dir: &'a InstallDir,
    /// 主機上的安裝目錄，填 `<install_dir>`。
    pub host_root: &'a str,
    /// 主機上的執行紀錄路徑，填 VK0056 的 `<path>`。
    pub run_log: &'a str,
    /// 容器內的收件目錄（`plan::mount::IN`）。
    pub inbox: &'a Path,
    pub channel: &'a mut Channel,
    /// 等 result 時多久看一次。
    pub poll: Duration,
    pub tty: Tty,
    /// `just vendor_kit` 之後的參數原樣（第一個是 `add`）。
    pub argv: &'a [String],
    /// 這次執行的 run-id，也是進度檔的 `<id>`。
    pub run_id: &'a str,
    /// 蓋在 VK 檔上的寫入者。
    pub written_by: &'a str,
    pub stdin: &'a mut dyn BufRead,
    pub stdout: &'a mut dyn Write,
    /// 詢問文字（印到 stderr）。
    pub prompt: &'a mut dyn Write,
    pub diags: &'a mut Diagnostics<W, S>,
    /// 執行紀錄（`txn` 寫里程碑事件）。
    pub log: &'a mut runlog::Writer<L>,
}

/// 工具交付的一個初始檔（[`InitFile`] 的自有版本）。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OwnedInit {
    pub path: String,
    pub strategy: Strategy,
    pub contents: Vec<u8>,
}

/// 印記檔：`.vendor_kit/cache/<repo>.stamp.toml`。
pub fn stamp_file(dir: &InstallDir, repo: &str) -> PathBuf {
    dir.cache_dir().join(format!("{repo}.stamp.toml"))
}

/// 基準版副本相對於 `.vendor_kit/` 的路徑：`baseline/<repo>/<path>`。
pub fn baseline_file(repo: &str, path: &str) -> PathBuf {
    Path::new("baseline").join(repo).join(path)
}

/// 跑一次 `add`，回傳結束碼。
pub fn run<W: Write, S: Sink, L: Write>(req: &Request, env: &mut Env<'_, W, S, L>) -> u8 {
    run_with(req, env, &discover_init_files)
}

/// 讀出暫存內容交付的初始檔。`init.toml` 的格式還沒定：有這個檔就停下，沒有就是沒有初始檔。
fn discover_init_files(root: &Path) -> Result<Vec<OwnedInit>, String> {
    match fs::symlink_metadata(root.join(INIT_TOML)) {
        Ok(_) => Err(format!(
            "the tool delivers {INIT_TOML}, but its format is not specified yet"
        )),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(Vec::new()),
        Err(e) => Err(format!("cannot read {INIT_TOML}: {e}")),
    }
}

/// 讀初始檔清單的函式；測試換成直接給清單。
pub(crate) type InitSource<'f> = &'f dyn Fn(&Path) -> Result<Vec<OwnedInit>, String>;

pub(crate) fn run_with<W: Write, S: Sink, L: Write>(
    req: &Request,
    env: &mut Env<'_, W, S, L>,
    init: InitSource,
) -> u8 {
    let mut add = Add { env, init, code: 0 };
    let _ = add.run(req);
    add.code
}

/// 診斷已印、這次執行停下。
struct Stop;

type Step<T> = Result<T, Stop>;

/// 撞名判定與入口檔要用的已裝工具資訊。
struct Installed {
    taken: Taken,
    /// 其他已裝工具的 `<ns>`。
    namespaces: BTreeMap<String, Vec<String>>,
}

struct Add<'r, 'a, W: Write, S: Sink, L: Write> {
    env: &'r mut Env<'a, W, S, L>,
    init: InitSource<'r>,
    code: u8,
}

impl<W: Write, S: Sink, L: Write> Add<'_, '_, W, S, L> {
    // ---- 診斷 ----

    fn emit(&mut self, d: Diagnostic) {
        self.code = self.code.max(d.message().exit_code());
        let _ = self.env.diags.emit(&d);
    }

    fn stop(&mut self, d: Diagnostic) -> Stop {
        self.emit(d);
        Stop
    }

    /// VK0056：契約還沒定的情況，或 VK 自己的錯。
    fn internal(&mut self, reason: impl Into<String>) -> Stop {
        let d = Diagnostic::new(&messages::VK0056)
            .arg("reason", reason)
            .arg("path", self.env.run_log);
        self.stop(d)
    }

    fn gap(&mut self, what: impl std::fmt::Display) -> Stop {
        self.internal(format!("{what} is not supported yet"))
    }

    /// 底層 crate 回的錯：有代碼就照代碼印（只有一個 `<file>` 占位符的代碼），否則當內部錯誤。
    fn failed(&mut self, file: &Path, message: Option<&'static Message>, detail: String) -> Stop {
        match message {
            Some(m) if m.code == messages::VK0013.code => {
                let d = Diagnostic::new(&messages::VK0013)
                    .arg("file", self.rel(file))
                    .arg("path", self.env.run_log);
                self.stop(d)
            }
            _ => self.internal(detail),
        }
    }

    /// VK0008：檔案版過高。
    fn too_new(&mut self, file: &Path, t: &schema::TooNew) -> Stop {
        let d = Diagnostic::new(&messages::VK0008)
            .arg("file", self.rel(file))
            .arg("N", t.found().to_string())
            .arg("M", t.max().to_string())
            .arg("written_by", t.written_by().unwrap_or("unknown"));
        self.stop(d)
    }

    /// 容器內路徑換成相對於安裝目錄的寫法，填 `<file>`。
    fn rel(&self, path: &Path) -> String {
        path.strip_prefix(self.env.dir.root())
            .unwrap_or(path)
            .display()
            .to_string()
    }

    fn say(&mut self, line: &str) {
        let _ = writeln!(self.env.stdout, "{line}");
    }

    // ---- 流程 ----

    fn run(&mut self, req: &Request) -> Step<()> {
        if req.repo == fetch::RESERVED {
            return Err(self.stop(Diagnostic::new(&messages::VK0057)));
        }
        if !fetch::is_namespace(req.repo) {
            return Err(self.gap(format_args!("tool name {:?} (not a just name)", req.repo)));
        }
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        let mut lockfile = self.lockfile()?;
        if self.recover_all(&mut lockfile)? {
            lockfile = self.lockfile()?;
        }

        let local = match (req.image, req.tag) {
            (None, _) => {
                return Err(self.gap(
                    "add without -i (resolving <repo> to an image and querying the registry)",
                ));
            }
            (Some(_), Some(_)) => return Err(self.gap("add -i together with <repo>@<tag>")),
            (Some(image), None) => {
                let given = image.to_string_lossy();
                parse_local(&given).map_err(|reason| self.gap(reason))?
            }
        };

        if let Some(current) = lockfile.tool(req.repo).cloned()
            && current.tag() != local.tag
        {
            let upgrade = format!("{}@{}", req.repo, local.tag);
            let command = prompt::command_with_y(&["just", "vendor_kit", "upgrade", &upgrade]);
            // VK0045 的下一步不帶 -y：去掉 command_with_y 補在最後的那一個（沒有 `--`，所以一定在最後）。
            let command = command.strip_suffix(" -y").unwrap_or(&command).to_owned();
            let d = Diagnostic::new(&messages::VK0045)
                .arg("repo", req.repo)
                .arg("tag", local.tag.to_string())
                .arg("current_tag", current.tag().to_string())
                .arg("upgrade_command", command);
            return Err(self.stop(d));
        }

        let pinned = self.inspect(req.repo, &local)?;
        if let Some(current) = lockfile.tool(req.repo) {
            if *current == pinned.0 {
                self.say(&text::unchanged(req.repo, &pinned.0));
                return Ok(());
            }
            return Err(self.gap(format_args!(
                "add with tag {} whose digest differs from the lock version line",
                local.tag
            )));
        }
        let candidate = self.fetch(req.repo, &pinned.1, &pinned.0, SLOT, &lockfile)?;
        self.import(req.repo, &pinned.0, candidate, lockfile)
    }

    fn config(&mut self) -> Step<Config> {
        match Config::load(self.env.dir) {
            Ok(c) => Ok(c),
            Err(ConfigError::Invalid(e)) => {
                let d = Diagnostic::new(e.message())
                    .arg("field", e.field().name())
                    .arg("value", e.value())
                    .arg("fix", e.fix());
                Err(self.stop(d))
            }
            Err(e) => Err(self.internal(e.to_string())),
        }
    }

    fn lock(&mut self, config: &Config) -> Step<Lock> {
        match Lock::acquire(self.env.dir, Mode::Exclusive, config) {
            Ok(lock) => {
                if let Some(m) = lock.warning() {
                    let d = Diagnostic::new(m).arg("install_dir", self.env.host_root);
                    self.emit(d);
                }
                Ok(lock)
            }
            Err(e) => match e.message() {
                Some(m) => {
                    let d = Diagnostic::new(m).arg("install_dir", self.env.host_root);
                    Err(self.stop(d))
                }
                None => Err(self.internal(e.to_string())),
            },
        }
    }

    fn lockfile(&mut self) -> Step<LockFile> {
        match LockFile::load_from(self.env.dir) {
            Ok(Some(l)) => Ok(l),
            Ok(None) => Err(self.internal(".vendor_kit/version.toml does not exist")),
            Err(version_file::Error::Parse {
                file,
                source: version_file::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => Err(self.too_new(&file, &t)),
            Err(e) => Err(self.internal(e.to_string())),
        }
    }

    /// 請啟動器做一個 docker 動作，等結果。`Failed` 回 docker 的結束碼。
    fn request(&mut self, op: &Op) -> Step<(plan::Seq, Outcome)> {
        let sent = self.env.channel.send(op);
        let seq = sent.map_err(|e| self.internal(e.to_string()))?;
        let reply = self.env.channel.receive(self.env.poll);
        let reply = reply.map_err(|e| self.internal(e.to_string()))?;
        Ok((seq, reply.outcome))
    }

    /// VK0055：取工具 image 的 docker 動作失敗。
    fn access_failed(&mut self, source: &str, repo: &str, reason: String) -> Stop {
        let d = Diagnostic::new(&messages::VK0055)
            .arg("source", source)
            .arg("target", repo)
            .arg("reason", reason);
        self.stop(d)
    }

    /// inspect `-i` 給的 image，回傳版本鎖定行的值與 image ID。
    fn inspect(&mut self, repo: &str, local: &LocalRef) -> Step<(ImageRef, ImageId)> {
        let Some(wire) = plan::ImageRef::parse(&local.given) else {
            return Err(self.gap(format_args!("image reference {:?}", local.given)));
        };
        let inspected = self.inspect_ref(wire, &local.given, repo)?;
        let Some(digest) = digest_for(&local.name(), &inspected.repo_digests) else {
            let d = Diagnostic::new(&messages::VK0031)
                .arg("image", &local.given)
                .arg("reason", text::no_repo_digest(&local.name()));
            return Err(self.stop(d));
        };
        let Some(pinned) = local.pin(&digest) else {
            return Err(self.internal(format!("cannot pin {} to {digest}", local.given)));
        };
        let Some(id) = ImageId::parse(&inspected.id) else {
            return Err(self.internal(format!("image inspect returned Id {:?}", inspected.id)));
        };
        Ok((pinned, id))
    }

    fn inspect_ref(&mut self, wire: plan::ImageRef, shown: &str, target: &str) -> Step<Inspected> {
        let (seq, outcome) = self.request(&Op::Inspect(wire))?;
        match outcome {
            Outcome::Ok => {}
            Outcome::Failed(rc) => {
                return Err(self.access_failed(shown, target, text::docker_failed("inspect", rc)));
            }
            Outcome::Runner(_) => return Err(self.internal("inspect returned a runner result")),
        }
        let out = self.env.channel.output_path(seq);
        let bytes = fs::read(&out).map_err(|e| self.internal(format!("{}: {e}", out.display())))?;
        parse_inspect(&bytes).map_err(|e| self.internal(e))
    }

    /// 取件並驗證：extract 到 `slot`，再 `fetch::verify`（含撞名）。
    fn fetch(
        &mut self,
        repo: &str,
        id: &ImageId,
        locked: &ImageRef,
        slot: &str,
        lockfile: &LockFile,
    ) -> Step<(Candidate, Installed)> {
        let Some(slot_v) = Slot::parse(slot) else {
            return Err(self.internal(format!("invalid slot {slot}")));
        };
        let (_, outcome) = self.request(&Op::Extract(id.clone(), slot_v))?;
        match outcome {
            Outcome::Ok => {}
            Outcome::Failed(rc) => {
                let shown = locked.to_string();
                return Err(self.access_failed(&shown, repo, text::docker_failed("extract", rc)));
            }
            Outcome::Runner(_) => return Err(self.internal("extract returned a runner result")),
        }
        let root = self.env.inbox.join(slot);
        let installed = self.installed(repo, lockfile)?;
        let inspected_digests = vec![format!(
            "{}/{}@{}",
            locked.registry(),
            locked.path(),
            locked.digest()
        )];
        let staged = Staged {
            repo,
            locked,
            root: &root,
            repo_digests: &inspected_digests,
        };
        match fetch::verify(&staged, &installed.taken, None) {
            Ok(c) => Ok((c, installed)),
            Err(fetch::Error::Collision { repo, collisions }) => {
                for c in collisions {
                    let d = Diagnostic::new(&messages::VK0030)
                        .arg("repo", repo.as_str())
                        .arg("ns", c.ns)
                        .arg("owner", c.owner.to_string());
                    self.emit(d);
                }
                Err(Stop)
            }
            Err(e) => Err(self.internal(format!("tool content of {repo}: {e}"))),
        }
    }

    /// 已裝工具（不含 `repo` 自己）的 `<ns>` 與根 `justfile` 的名字。
    fn installed(&mut self, repo: &str, lockfile: &LockFile) -> Step<Installed> {
        let mut taken = Taken::new();
        let mut namespaces = BTreeMap::new();
        for other in lockfile.tools().keys().filter(|r| r.as_str() != repo) {
            let cache = match self.env.dir.tool_cache(other) {
                Ok(c) => c,
                Err(e) => return Err(self.internal(e.to_string())),
            };
            match fetch::namespaces(&cache) {
                Ok(ns) => {
                    taken.tool(other, ns.iter().cloned());
                    namespaces.insert(other.clone(), ns);
                }
                Err(e) => {
                    return Err(self.gap(format_args!(
                        "add while the cache of installed tool {other} is unreadable ({e}); \
                         run just vendor_kit sync first"
                    )));
                }
            }
        }
        let justfile = self.env.dir.root().join("justfile");
        match fs::read(&justfile) {
            Ok(bytes) => {
                let names = justfile::scan(&String::from_utf8_lossy(&bytes));
                for r in names.recipes {
                    taken.root_recipe(r);
                }
                for m in names.modules {
                    taken.root_module(m);
                }
            }
            Err(e) if e.kind() == io::ErrorKind::NotFound => {}
            Err(e) => return Err(self.internal(format!("{}: {e}", justfile.display()))),
        }
        Ok(Installed { taken, namespaces })
    }

    /// 算初始檔、一次問完、全部同意才落地。
    fn import(
        &mut self,
        repo: &str,
        locked: &ImageRef,
        (candidate, installed): (Candidate, Installed),
        mut lockfile: LockFile,
    ) -> Step<()> {
        let init = (self.init)(candidate.root()).map_err(|reason| self.gap(reason))?;
        let meta_path = match metadata::tool_path(self.env.dir, repo) {
            Ok(p) => p,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let mut meta = if meta_path.exists() {
            match Metadata::load(&meta_path) {
                Ok(m) => m,
                Err(metadata::Error::TooNew { file, too_new }) => {
                    return Err(self.too_new(&file, &too_new));
                }
                Err(e) => return Err(self.failed(&meta_path, e.message(), e.to_string())),
            }
        } else {
            Metadata::new()
        };
        let files: Vec<InitFile> = init
            .iter()
            .map(|f| InitFile {
                path: &f.path,
                strategy: f.strategy,
                contents: &f.contents,
            })
            .collect();
        let root = self.env.dir.root().to_path_buf();
        let vk = self.env.dir.vk_dir();
        let planned = initfiles::plan(
            initfiles::Command::Add,
            &files,
            &meta,
            |p| read_optional(&root.join(p)),
            |p| read_optional(&vk.join(baseline_file(repo, p))),
        );
        let planned = planned.map_err(|e| self.internal(e.to_string()))?;
        if let Some((path, gap)) = planned.gaps().next() {
            return Err(self.gap(format_args!("init file {path} ({gap:?})")));
        }

        let questions: Vec<String> = planned
            .questions
            .iter()
            .map(|q| text::question(repo, &q.path, q.ask))
            .collect();
        let tty = TtyState {
            stdin: self.env.tty.stdin,
            stderr: self.env.tty.stderr,
        };
        let answers = prompt::ask_all(
            &questions,
            Consent::Ask,
            &tty,
            &mut *self.env.stdin,
            &mut *self.env.prompt,
        );
        match answers {
            Ok(a) if a.all_yes() => {}
            Ok(_) => {
                self.say(text::NO_CHANGES);
                return Ok(());
            }
            Err(PromptError::NotInteractive(_)) => {
                let mut words = vec!["just".to_owned(), "vendor_kit".to_owned()];
                words.extend(self.env.argv.iter().cloned());
                let d = Diagnostic::new(&messages::VK0002)
                    .arg("command_with_y", prompt::command_with_y(&words));
                return Err(self.stop(d));
            }
            Err(e) => return Err(self.internal(e.to_string())),
        }

        if let Err(e) = candidate.recheck() {
            return Err(self.internal(format!("staged content of {repo} changed: {e}")));
        }

        // 紀錄檔：這個工具的 metadata 與基準版副本。
        let mut repo_writes: Vec<(PathBuf, Vec<u8>)> = Vec::new();
        let mut records: Vec<(PathBuf, Vec<u8>)> = Vec::new();
        for f in &planned.files {
            if let Some(w) = &f.write {
                repo_writes.push((PathBuf::from(&f.path), w.after.clone()));
            }
            if let Some(b) = &f.baseline {
                records.push((baseline_file(repo, &f.path), b.clone()));
            }
            if let Some(r) = &f.record
                && let Err(e) = meta.put(r.clone())
            {
                return Err(self.internal(e.to_string()));
            }
        }
        if !planned.files.is_empty() {
            let rendered = meta.render(self.env.written_by);
            let rendered = rendered.map_err(|e| self.internal(e.to_string()))?;
            let rel = meta_path
                .strip_prefix(&vk)
                .map(Path::to_path_buf)
                .unwrap_or_else(|_| meta_path.clone());
            records.push((rel, rendered.into_bytes()));
            self.other_records(repo, &planned.files, &lockfile, &mut records)?;
        }

        if let Err(e) = lockfile.set_tool(repo, locked) {
            return Err(self.internal(e.to_string()));
        }
        let mut all_ns = installed.namespaces;
        all_ns.insert(repo.to_owned(), candidate.namespaces().to_vec());
        let tools: Vec<tools_just::Tool> = all_ns
            .iter()
            .map(|(r, ns)| tools_just::Tool {
                repo: r,
                namespaces: ns,
            })
            .collect();
        let entry = tools_just::render(&tools).map_err(|e| self.internal(e.to_string()))?;

        let progress = self.progress(repo, locked, !repo_writes.is_empty())?;
        self.land(
            &candidate,
            progress,
            &repo_writes,
            &records,
            &entry,
            &mut lockfile,
        )?;

        self.say(&text::added(repo, locked));
        for f in &planned.files {
            if let Some(line) = text::file_line(f) {
                self.say(&line);
            }
        }
        for f in &planned.files {
            if let Some(m) = f.message() {
                let d = Diagnostic::new(m).arg("file", f.path.as_str());
                self.emit(d);
            }
        }
        Ok(())
    }

    /// 其他紀錄檔裡同一個路徑的紀錄（ADR-0003）：寫入前內容相符的紀錄跟著換成寫入後的 hash。
    fn other_records(
        &mut self,
        repo: &str,
        files: &[FilePlan],
        lockfile: &LockFile,
        records: &mut Vec<(PathBuf, Vec<u8>)>,
    ) -> Step<()> {
        let writes: Vec<(&str, &[u8], &[u8])> = files
            .iter()
            .filter_map(|f| {
                let w = f.write.as_ref()?;
                Some((f.path.as_str(), w.before.as_deref()?, w.after.as_slice()))
            })
            .collect();
        if writes.is_empty() {
            return Ok(());
        }
        let vk = self.env.dir.vk_dir();
        let mut paths = vec![metadata::vk_path(self.env.dir)];
        for other in lockfile.tools().keys().filter(|r| r.as_str() != repo) {
            match metadata::tool_path(self.env.dir, other) {
                Ok(p) => paths.push(p),
                Err(e) => return Err(self.internal(e.to_string())),
            }
        }
        for path in paths {
            if !path.exists() {
                continue;
            }
            let mut m = match Metadata::load(&path) {
                Ok(m) => m,
                Err(metadata::Error::TooNew { file, too_new }) => {
                    return Err(self.too_new(&file, &too_new));
                }
                Err(e) => return Err(self.failed(&path, e.message(), e.to_string())),
            };
            let mut changed = false;
            for (p, before, after) in &writes {
                match m.record_write(p, before, after) {
                    Ok(metadata::WriteOutcome::Updated) => changed = true,
                    Ok(_) => {}
                    Err(e) => return Err(self.internal(e.to_string())),
                }
            }
            if changed {
                let text = m.render(self.env.written_by);
                let text = text.map_err(|e| self.internal(e.to_string()))?;
                let rel = path.strip_prefix(&vk).map(Path::to_path_buf);
                let rel = rel.map_err(|_| self.internal(format!("{}", path.display())))?;
                records.push((rel, text.into_bytes()));
            }
        }
        Ok(())
    }

    fn progress(&mut self, repo: &str, locked: &ImageRef, repo_files: bool) -> Step<Progress> {
        let mut p = match Progress::new(VERB, self.env.run_id, self.env.argv) {
            Ok(p) => p,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let doc = p.document_mut();
        let set = doc
            .set(&[PROGRESS_TABLE, "repo"], repo)
            .and_then(|()| doc.set(&[PROGRESS_TABLE, "image"], locked.to_string()))
            .and_then(|()| doc.set(&[PROGRESS_TABLE, "repo_files"], repo_files));
        set.map_err(|e| self.internal(e.to_string()))?;
        Ok(p)
    }

    /// 依序落地（`txn`）。
    fn land(
        &mut self,
        candidate: &Candidate,
        progress: Progress,
        repo_writes: &[(PathBuf, Vec<u8>)],
        records: &[(PathBuf, Vec<u8>)],
        entry: &str,
        lockfile: &mut LockFile,
    ) -> Step<txn::Done> {
        let stamp = stamp_file(self.env.dir, candidate.repo());
        let tool = ToolContent {
            repo: candidate.repo(),
            staged: candidate.root(),
            version: candidate.version(),
            stamp_file: &stamp,
        };
        let repo_files: Vec<RepoFile> = repo_writes
            .iter()
            .map(|(path, contents)| RepoFile { path, contents })
            .collect();
        let record_files: Vec<RecordFile> = records
            .iter()
            .map(|(path, contents)| RecordFile { path, contents })
            .collect();
        let result = {
            let mut fx = Disk::new(self.env.dir, self.env.log, self.env.written_by);
            Txn::begin(&mut fx, progress).and_then(|t| {
                t.swap_cache(&[tool])?
                    .write_repo_files(&repo_files)?
                    .write_records(&record_files)?
                    .write_tools_just(Some(entry.as_bytes()))?
                    .write_lock_line(lockfile, Target::Tool)?
                    .complete()
            })
        };
        result.map_err(|f| self.internal(f.to_string()))
    }

    // ---- 恢復 ----

    /// 恢復全部殘留的進度檔；有恢復任何一份回 `true`。
    fn recover_all(&mut self, lockfile: &mut LockFile) -> Step<bool> {
        let entries = match progress::find(self.env.dir) {
            Ok(e) => e,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let mut any = false;
        for entry in entries {
            if entry.verb != VERB {
                return Err(self.gap(format_args!(
                    "recovering the incomplete {} operation in {}",
                    entry.verb,
                    self.rel(&entry.path)
                )));
            }
            self.recover(&entry, lockfile)?;
            *lockfile = self.lockfile()?;
            any = true;
        }
        Ok(any)
    }

    /// 恢復一份殘留的 `add`：依進度檔記的版本鎖定行值重新取件、驗證，再走一次同樣的落地順序；
    /// 新的進度檔完成之後才刪舊的那一份，中途再斷也還認得出來。只在沒有 repo 檔要寫時做：
    /// 那次寫了哪些 repo 檔沒有記錄，重新判定會把它自己建的檔當成使用者的檔。
    fn recover(&mut self, entry: &progress::Entry, lockfile: &LockFile) -> Step<()> {
        let old = match entry.load() {
            Ok(p) => p,
            Err(e) => return Err(self.failed(&entry.path, e.message(), e.to_string())),
        };
        let field = |key: &str| {
            old.document()
                .get(&[PROGRESS_TABLE, key])
                .and_then(|i| i.as_value())
                .cloned()
        };
        let repo = field("repo").and_then(|v| v.as_str().map(str::to_owned));
        let image = field("image").and_then(|v| v.as_str().map(str::to_owned));
        let repo_files = field("repo_files").and_then(|v| v.as_bool());
        let (Some(repo), Some(image), Some(repo_files)) = (repo, image, repo_files) else {
            return Err(self.gap(format_args!(
                "recovering {} without the [add] fields",
                self.rel(&entry.path)
            )));
        };
        if repo_files {
            return Err(self.gap(format_args!(
                "recovering {}, which writes repo files",
                self.rel(&entry.path)
            )));
        }
        let Ok(locked) = ImageRef::parse(&image) else {
            return Err(self.internal(format!("{} records image {image:?}", self.rel(&entry.path))));
        };
        let pinned = format!(
            "{}/{}@{}",
            locked.registry(),
            locked.path(),
            locked.digest()
        );
        let Some(wire) = plan::ImageRef::parse(&pinned) else {
            return Err(self.internal(format!("cannot inspect {pinned}")));
        };
        let inspected = self.inspect_ref(wire, &image, &repo)?;
        if !inspected.repo_digests.contains(&pinned) {
            let d = Diagnostic::new(&messages::VK0031)
                .arg("image", image.as_str())
                .arg("reason", text::no_repo_digest(&pinned));
            return Err(self.stop(d));
        }
        let Some(id) = ImageId::parse(&inspected.id) else {
            return Err(self.internal(format!("image inspect returned Id {:?}", inspected.id)));
        };
        let (candidate, installed) = self.fetch(&repo, &id, &locked, RECOVER_SLOT, lockfile)?;
        if let Err(e) = candidate.recheck() {
            return Err(self.internal(format!("staged content of {repo} changed: {e}")));
        }
        let mut lockfile = lockfile.clone();
        if let Err(e) = lockfile.set_tool(&repo, &locked) {
            return Err(self.internal(e.to_string()));
        }
        let mut all_ns = installed.namespaces;
        all_ns.insert(repo.clone(), candidate.namespaces().to_vec());
        let tools: Vec<tools_just::Tool> = all_ns
            .iter()
            .map(|(r, ns)| tools_just::Tool {
                repo: r,
                namespaces: ns,
            })
            .collect();
        let entry_text = tools_just::render(&tools).map_err(|e| self.internal(e.to_string()))?;
        let progress = self.progress(&repo, &locked, false)?;
        self.land(&candidate, progress, &[], &[], &entry_text, &mut lockfile)?;
        if let Err(e) = progress::delete(self.env.dir, &entry.verb, &entry.id) {
            return Err(self.failed(&entry.path, e.message(), e.to_string()));
        }
        self.say(&text::recovered(&repo, &locked));
        Ok(())
    }
}

/// 讀檔；不在回 `None`。
fn read_optional(path: &Path) -> io::Result<Option<Vec<u8>>> {
    match fs::read(path) {
        Ok(b) => Ok(Some(b)),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(None),
        Err(e) => Err(e),
    }
}
