//! `upgrade` 指令的工具那一半（04 指令表 `upgrade <repo>`、`upgrade <repo>@<tag>`；04 成對與無害的工具升版
//! 流程、指定版本、本機覆寫）：換工具版本，做基準版合併。`upgrade --engine` 不在這裡。
//!
//! `update` 只查（engine/update）；真正換版本在這裡。呼叫端（入口 `vendor_kit`）已解析好參數、判過安裝
//! 目錄（VK0028），並接好執行紀錄與 `plan` 往返。這裡依序做：
//!
//! 1. 讀 `.vendor_kit/config.toml`（VK0059），在第一次取鎖之前（04 設定）。
//! 2. 取安裝目錄的排他鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束。
//! 3. 讀 `version.toml` 與 `version.local.toml`（檔案版過高回 VK0008）；有工具的覆寫就讀它的本機開發來源，
//!    讀不到回 VK0052（見「本機覆寫」）。
//! 4. 恢復殘留的進度檔（04 成對與無害：可寫 recipe 先恢復再判是否重複）；做法見 `Upgrade::recover`。
//! 5. 判對象與目標版本：
//!    - 工具不在版本鎖定行：見「缺口」。
//!    - 不帶 tag：見「缺口」。
//!    - `@<tag>` 與版本鎖定行的 tag 相同：stdout 說明未變更，以 0 結束，不送 docker 動作（04 指定版本：
//!      同一 tag 改指別的 digest 不算新版）。
//! 6. 經 `plan` 協定請啟動器 `inspect` 本機 image `<registry>/<路徑>:<tag>`（registry 與路徑取自版本鎖定行），
//!    從 RepoDigests 讀 digest，組成新的版本鎖定行值，再以 image ID `extract`；docker 動作失敗回 VK0055。
//! 7. `fetch::verify`：digest、dist 格式、逐檔指紋、`<ns>` 撞名（對象是其他已裝工具、根 `justfile` 的
//!    recipe 與 module、保留名 `vendor_kit`；這個工具自己的舊 `<ns>` 不算）。
//! 8. `initfiles`（`Command::Upgrade`）以基準版副本、目前檔、新版算出每個初始檔的動作與問題，`prompt`
//!    一次問完（帶 `-y` 全部同意、不問）：答否是正常取消（stdout 說明未變更，以 0 結束）；不能互動回
//!    VK0002；兩者除執行紀錄外都不寫任何檔。
//! 9. 重驗暫存內容（ADR-0006 第三層），再經 `txn` 依序落地：`cache/<repo>/` 與印記、repo 檔、紀錄檔
//!    （這個工具的 metadata、基準版副本、其他紀錄檔裡同一個路徑的 hash）、`gen/tools.just`（開著覆寫的工具
//!    那幾行指向本機開發來源），最後才寫版本鎖定行（04 成對與無害第 3 點），再刪進度檔。
//! 10. stdout 先報告用了哪個覆寫，再列出改了什麼，以及不刪、不重建的初始檔清單（04 寫入既有檔的例外）；
//!     初始檔的警告（VK0019、VK0020、VK0021）照印。合併結果是 TOML／just 而解析不過的檔
//!     （`initfiles` 的 `Verdict::Unparsable`，scope_roadmap:32）留原檔、基準版不推、記進這個工具 metadata
//!     的 `conflicts`，stdout 說明留了原檔；合併寫入成功的檔從 `conflicts` 拿掉。
//!
//! # 本機覆寫
//!
//! `version.local.toml` 有工具的覆寫（`dev <repo> -p <dir>`）時照常換版（04 本機覆寫：除 `test` 外的一般
//! recipe 照常執行；ADR-0013），做法跟 engine/sync 一致：
//!
//! - 對象工具開著覆寫也照常取件、換 `cache/<repo>/`、印記與版本鎖定行：覆寫期間的內容由本機開發來源決定，
//!   `cache/<repo>/` 與鎖定行記的是鎖定版本，`undev` 之後回到換好的新版。
//! - 每個覆寫的 `<ns>` 從本機開發來源讀（[`local`]，值照 engine/dev 以安裝目錄為準正規化，只收安裝目錄裡的
//!   值，見「缺口」）；讀不到回 VK0052
//!   （04 本機覆寫：覆寫來源失效只擋需讀它的動作；重產 `gen/tools.just` 要讀它），列出每個讀不到的覆寫，
//!   在任何 docker 動作與寫入之前停下。
//! - `gen/tools.just` 裡開著覆寫的工具（對象或其他工具）那幾行指向本機開發來源（`tools_just::render_with`）；
//!   撞名判定裡開著覆寫的其他工具也以本機開發來源的 `<ns>` 為準（入口檔裡生效的是它）。
//! - 每次以 0 結束時（換好、已是該版、答否取消）都在 stdout 報告用了哪個覆寫，排在那條路徑的字句前面
//!   （04 本機覆寫：不加診斷前綴，`update` 以外到 stdout）；停下時只印診斷。恢復殘留 `upgrade` 的字句在恢復
//!   當下就印，所以排在覆寫報告前面。
//! - 引擎的覆寫與工具換版無關，不看。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 印記、基準版副本的位置與 `add` 相同：`.vendor_kit/cache/<repo>.stamp.toml`（[`stamp::tool_file`]）、
//!   `.vendor_kit/baseline/<repo>/<初始檔的 repo 相對路徑>`（[`baseline_file`]，照抄 engine/add）。
//! - 進度檔 `.tmp.upgrade.<run-id>.toml` 的 `[upgrade]` 表：格式定在 `progress::upgrade`，讓 `update`
//!   等唯讀 recipe 也讀得到（VK0041 的 `<repo>`）。
//! - 新版不再提供的初始檔：`initfiles` 判成缺口（紀錄記成什麼 state 契約沒寫），但 04 只要求不刪、只列
//!   清單，所以這裡照列、不改它的紀錄，不因此停下。
//! - 取件的 slot 名是 [`SLOT_PREFIX`] 加這次執行裡的序號（`tool1`、`tool2`…）。
//! - stdout 的字句與詢問文字（英文）見 [`text`]；覆寫的報告字句跟 engine/sync 相同（[`text::local_override`]）。
//! - 本機開發來源的正規化與檢查從 engine/dev 照抄（[`local`]，engine/sync 也照抄同一份）。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - 不帶 tag 的 `upgrade <repo>`：要列 registry 的 tag 算最新版（registry client，計畫 D8；`plan` 沒有列
//!   tag 的 op）。`--registry-token-file` 只在真的列清單時才讀，所以這一版不讀，VK0001 也還碰不到。
//! - `@<tag>` 的 image 不在本機：線上把 tag 解析成 digest 要 registry client，`plan` 的 `pull` 只收帶 digest
//!   的引用。本機 image 沒有這個 registry 與路徑的 RepoDigest 也停下（VK0031 只寫離線導入）。
//! - 工具不在版本鎖定行：VK0046 只寫 remove、undev、update（計畫 G5）。
//! - `<ns>` 撞名：VK0030 只寫 `add`。
//! - 判基準版落後（04：鎖定行比基準版新時，不帶 tag 的 `upgrade` 只完成鎖定行那一版的合併）：`metadata`
//!   沒有記基準版是哪一版。所以 `@<tag>` 與鎖定行同 tag、而工具有逐檔紀錄時停下；沒有紀錄的工具沒有
//!   基準版，同 tag 就是未變更。
//! - 工具交付 `init.toml`：初始檔清單的格式沒定（同 engine/add），讀不出初始檔；沒有 `init.toml` 的工具
//!   就沒有新版初始檔。`initfiles` 判成缺口的檔（新版不再提供的除外）。
//! - 覆寫指到不在版本鎖定行的工具：ADR-0002 說覆寫只覆蓋已存在的鎖定行，訊息表沒有代碼
//!   （`version_file::OrphanOverrides`），停下（同 engine/sync）。
//! - 開著覆寫的工具的本機開發來源交付保留名 `vendor_kit`：沒有代碼，停下（同 engine/sync）。
//! - 覆寫的本機開發來源在安裝目錄外（`dev` 經 `stage-dir` 收的絕對路徑，或開頭是 `..` 的相對路徑）：
//!   這一版不經 `stage-dir` 取，引擎看不到那個目錄，照讀不到回 VK0052，要先 `undev`（同 engine/sync）。
//! - 其他已裝工具的 `cache/<repo>/` 讀不到（例如全新 checkout 還沒 `sync`）：撞名判定與入口檔都要它。
//! - 殘留的進度檔不是 `upgrade` 的；殘留的是引擎 upgrade；或殘留的工具 upgrade 寫過初始檔相關的檔（那次
//!   寫了哪些沒有記錄，重新判定會把它自己寫的內容當成使用者改的）。
//! - 已知偏離：恢復殘留 `upgrade` 的寫入排在這次的詢問之前，04 共同選項要先問完再寫（含恢復）。能恢復
//!   的只有沒寫初始檔的那種，恢復本身沒有要問的事；同 engine/add。
//! - 中途寫檔失敗沒有代碼（計畫 G4）；dist 格式不符（G2）、指紋不符（G1）沒有代碼。
//! - 合併結果解析不過、留了原檔的初始檔沒有訊息表代碼，對外結束碼也沒定（VK0021 說檔裡含有衝突，
//!   不能借用）：這一版只在 stdout 說明，照常以 0 結束（ADR-0003 的補寫待定）。
//!
//! 這裡不直接碰 docker：docker 動作一律是 `plan` 協定的 op，由啟動器代做。

mod justfile;
pub mod local;
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
use initfiles::{Gap, InitFile, Strategy};
use layout::InstallDir;
use metadata::Metadata;
use plan::{Channel, ImageId, Op, Outcome, Slot, Tty};
use progress::Progress;
use progress::upgrade as table;
use prompt::{Consent, PromptError, TtyState};
use runlog::Target;
use txn::{Disk, RecordFile, RepoFile, ToolContent, Txn};
use version_file::{LocalFile, LockFile, Versions};

pub use source::{Inspected, digest_for, parse_inspect};

/// 進度檔的 `<verb>`。
pub const VERB: &str = table::VERB;
/// 取件的 slot 名前綴，後面接這次執行裡的序號（從 1 起）。
pub const SLOT_PREFIX: &str = "tool";
/// 工具交付初始檔清單的檔名（格式未定，見模組說明的缺口）。
pub const INIT_TOML: &str = "init.toml";

/// 一次 `upgrade <repo>[@<tag>] [-y]` 的參數（`args::Command::UpgradeTool`）。
/// `--registry-token-file` 只在查版本清單時才讀，列 tag 還沒做，所以這裡不收。
#[derive(Debug, Clone, Copy)]
pub struct Request<'a> {
    pub repo: &'a str,
    pub tag: Option<Tag>,
    /// `-y`：預先同意全部詢問。
    pub yes: bool,
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
    /// `just vendor_kit` 之後的參數原樣（第一個是 `upgrade`）。
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

/// 基準版副本相對於 `.vendor_kit/` 的路徑：`baseline/<repo>/<path>`（照抄 engine/add）。
pub fn baseline_file(repo: &str, path: &str) -> PathBuf {
    Path::new("baseline").join(repo).join(path)
}

/// 跑一次 `upgrade <repo>`，回傳結束碼。
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
    let mut upgrade = Upgrade {
        env,
        init,
        code: 0,
        extracts: 0,
        local: BTreeMap::new(),
    };
    let _ = upgrade.run(req);
    upgrade.code
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

/// 開著本機覆寫的一個工具：正規化後的本機開發來源與它交付的 `<ns>`。
struct Local {
    dir: String,
    namespaces: Vec<String>,
}

/// 一個工具這次要換上的版本：版本鎖定行的值與 image ID。
struct Resolved {
    locked: ImageRef,
    id: ImageId,
    repo_digests: Vec<String>,
}

struct Upgrade<'r, 'a, W: Write, S: Sink, L: Write> {
    env: &'r mut Env<'a, W, S, L>,
    init: InitSource<'r>,
    code: u8,
    /// 這次執行已用掉的 slot 數。
    extracts: u32,
    /// 開著覆寫的工具（模組說明「本機覆寫」）。
    local: BTreeMap<String, Local>,
}

impl<W: Write, S: Sink, L: Write> Upgrade<'_, '_, W, S, L> {
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

    /// 每次報告用了哪個覆寫（04 本機覆寫）。
    fn report_overrides(&mut self) {
        let lines: Vec<String> = self
            .local
            .iter()
            .map(|(repo, l)| text::local_override(repo, &l.dir))
            .collect();
        for line in lines {
            self.say(&line);
        }
    }

    // ---- 流程 ----

    fn run(&mut self, req: &Request) -> Step<()> {
        if !fetch::is_namespace(req.repo) {
            return Err(self.gap(format_args!("tool name {:?} (not a just name)", req.repo)));
        }
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        let mut lockfile = self.lockfile()?;
        self.local = self.local(&lockfile)?;
        if self.recover_all(&lockfile)? {
            lockfile = self.lockfile()?;
        }

        let Some(current) = lockfile.tool(req.repo).cloned() else {
            return Err(self.gap(format_args!(
                "upgrade of {}, which is not in the lock version lines",
                req.repo
            )));
        };
        let Some(tag) = req.tag else {
            return Err(self.gap(format_args!(
                "upgrade {} without @<tag> (listing tags from the registry to find the latest \
                 version; currently {})",
                req.repo,
                current.tag()
            )));
        };
        if tag == current.tag() {
            let meta_path = self.meta_path(req.repo)?;
            if meta_path.exists() {
                return Err(self.gap(format_args!(
                    "judging whether the baseline of {} is behind the lock version line",
                    req.repo
                )));
            }
            self.report_overrides();
            self.say(&text::unchanged(req.repo, tag));
            return Ok(());
        }

        let resolved = self.resolve(&current, tag)?;
        let fetched = self.fetch(req.repo, &resolved, &lockfile)?;
        self.apply(req, &current, &resolved.locked, fetched, lockfile)
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

    /// `version.local.toml`：檔案版過高回 VK0008；工具的覆寫讀本機開發來源（模組說明「本機覆寫」），
    /// 讀不到的每一個都印 VK0052 再停下。
    fn local(&mut self, lockfile: &LockFile) -> Step<BTreeMap<String, Local>> {
        match LocalFile::load_from(self.env.dir) {
            Ok(Some(file)) => {
                if let Err(orphan) = Versions::new(lockfile, Some(&file)) {
                    return Err(self.gap(format_args!("{orphan} (no reason code)")));
                }
                let mut local = BTreeMap::new();
                let mut blocked: Vec<Diagnostic> = Vec::new();
                for (repo, source) in file.tools() {
                    match self.local_source(repo, source) {
                        Ok(Ok(l)) => {
                            local.insert(repo.clone(), l);
                        }
                        Ok(Err(d)) => blocked.push(d),
                        Err(stop) => return Err(stop),
                    }
                }
                if blocked.is_empty() {
                    Ok(local)
                } else {
                    for d in blocked {
                        self.emit(d);
                    }
                    Err(Stop)
                }
            }
            Ok(None) => Ok(BTreeMap::new()),
            Err(version_file::Error::Parse {
                file,
                source: version_file::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => Err(self.too_new(&file, &t)),
            Err(e) => Err(self.internal(e.to_string())),
        }
    }

    /// 一個工具的本機開發來源：讀不到回 `Ok(Err(VK0052))`；交付保留名是缺口（模組說明）。
    fn local_source(&mut self, repo: &str, source: &str) -> Step<Result<Local, Diagnostic>> {
        let unreadable = |reason: String| {
            Diagnostic::new(&messages::VK0052)
                .arg("target", repo)
                .arg("source", source)
                .arg("reason", reason)
                .arg("undev_command", format!("just vendor_kit undev {repo}"))
        };
        let dir = match local::normalize(OsStr::new(source)) {
            Ok(d) => d,
            Err(reason) => return Ok(Err(unreadable(reason))),
        };
        let namespaces = match local::check_dir(self.env.dir.root(), &dir, repo) {
            Ok(ns) => ns,
            Err(reason) => return Ok(Err(unreadable(reason))),
        };
        if namespaces.iter().any(|n| n == fetch::RESERVED) {
            return Err(self.gap(format_args!(
                "upgrade while the local source of {repo} delivers the reserved namespace {} \
                 (no reason code)",
                fetch::RESERVED
            )));
        }
        Ok(Ok(Local { dir, namespaces }))
    }

    fn meta_path(&mut self, repo: &str) -> Step<PathBuf> {
        metadata::tool_path(self.env.dir, repo).map_err(|e| self.internal(e.to_string()))
    }

    /// 請啟動器做一個 docker 動作，等結果。
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

    /// inspect 一個引用；docker 失敗回 `Ok(Err(rc))`。
    fn inspect(&mut self, wire: &plan::ImageRef) -> Step<Result<Inspected, u8>> {
        let (seq, outcome) = self.request(&Op::Inspect(wire.clone()))?;
        match outcome {
            Outcome::Ok => {}
            Outcome::Failed(rc) => return Ok(Err(rc)),
            Outcome::Runner(_) => return Err(self.internal("inspect returned a runner result")),
        }
        let out = self.env.channel.output_path(seq);
        let bytes = fs::read(&out).map_err(|e| self.internal(format!("{}: {e}", out.display())))?;
        parse_inspect(&bytes).map(Ok).map_err(|e| self.internal(e))
    }

    /// `@<tag>` 換成版本鎖定行的值（模組說明第 6 步）：inspect 本機 image，讀 RepoDigests 的 digest。
    fn resolve(&mut self, current: &ImageRef, tag: Tag) -> Step<Resolved> {
        let name = format!("{}/{}", current.registry(), current.path());
        let given = format!("{name}:{tag}");
        let Some(wire) = plan::ImageRef::parse(&given) else {
            return Err(self.internal(format!("cannot inspect {given}")));
        };
        let inspected = match self.inspect(&wire)? {
            Ok(i) => i,
            Err(_) => {
                return Err(self.gap(format_args!(
                    "upgrade to {given}, which is not a local image (resolving a tag to a digest \
                     from the registry)"
                )));
            }
        };
        let Some(digest) = digest_for(&name, &inspected.repo_digests) else {
            return Err(self.gap(format_args!(
                "upgrade to the local image {given} without a repository digest for {name}"
            )));
        };
        let Ok(locked) = ImageRef::parse(&format!("{given}@{digest}")) else {
            return Err(self.internal(format!("cannot pin {given} to {digest}")));
        };
        let Some(id) = ImageId::parse(&inspected.id) else {
            return Err(self.internal(format!("image inspect returned Id {:?}", inspected.id)));
        };
        Ok(Resolved {
            locked,
            id,
            repo_digests: inspected.repo_digests,
        })
    }

    /// 取件並驗證：extract 到這次執行的下一個 slot，再 `fetch::verify`（含撞名）。
    fn fetch(
        &mut self,
        repo: &str,
        resolved: &Resolved,
        lockfile: &LockFile,
    ) -> Step<(Candidate, Installed)> {
        self.extracts += 1;
        let slot = format!("{SLOT_PREFIX}{}", self.extracts);
        let Some(slot_v) = Slot::parse(&slot) else {
            return Err(self.internal(format!("invalid slot {slot}")));
        };
        let (_, outcome) = self.request(&Op::Extract(resolved.id.clone(), slot_v))?;
        let shown = resolved.locked.to_string();
        match outcome {
            Outcome::Ok => {}
            Outcome::Failed(rc) => {
                return Err(self.access_failed(&shown, repo, text::docker_failed("extract", rc)));
            }
            Outcome::Runner(_) => return Err(self.internal("extract returned a runner result")),
        }
        let root = self.env.inbox.join(&slot);
        let installed = self.installed(repo, lockfile)?;
        let staged = Staged {
            repo,
            locked: &resolved.locked,
            root: &root,
            repo_digests: &resolved.repo_digests,
        };
        match fetch::verify(&staged, &installed.taken, None) {
            Ok(c) => Ok((c, installed)),
            Err(fetch::Error::Collision { collisions, .. }) => {
                let list: Vec<String> = collisions
                    .iter()
                    .map(|c| format!("{} (used by {})", c.ns, c.owner))
                    .collect();
                Err(self.gap(format_args!(
                    "upgrade of {repo} whose new version delivers colliding namespaces: {}",
                    list.join(", ")
                )))
            }
            Err(e) => Err(self.internal(format!("tool content of {repo}: {e}"))),
        }
    }

    /// 已裝工具（不含 `repo` 自己）的 `<ns>` 與根 `justfile` 的名字。開著覆寫的工具取本機開發來源的 `<ns>`。
    fn installed(&mut self, repo: &str, lockfile: &LockFile) -> Step<Installed> {
        let mut taken = Taken::new();
        let mut namespaces = BTreeMap::new();
        for other in lockfile.tools().keys().filter(|r| r.as_str() != repo) {
            if let Some(l) = self.local.get(other) {
                taken.tool(other, l.namespaces.iter().cloned());
                namespaces.insert(other.clone(), l.namespaces.clone());
                continue;
            }
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
                        "upgrade while the cache of installed tool {other} is unreadable ({e}); \
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

    /// 算初始檔、一次問完、全部同意才落地（模組說明第 8–10 步）。
    fn apply(
        &mut self,
        req: &Request,
        current: &ImageRef,
        locked: &ImageRef,
        (candidate, installed): (Candidate, Installed),
        mut lockfile: LockFile,
    ) -> Step<()> {
        let repo = req.repo;
        let init = (self.init)(candidate.root()).map_err(|reason| self.gap(reason))?;
        let meta_path = self.meta_path(repo)?;
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
            initfiles::Command::Upgrade,
            &files,
            &meta,
            |p| read_optional(&root.join(p)),
            |p| read_optional(&vk.join(baseline_file(repo, p))),
        );
        let planned = planned.map_err(|e| self.internal(e.to_string()))?;
        // 新版不再提供的初始檔照列、不停下（模組說明「這次自訂的內部細節」）。
        if let Some((path, gap)) = planned.gaps().find(|(_, g)| *g != Gap::NoLongerProvided) {
            return Err(self.gap(format_args!("init file {path} on upgrade ({gap:?})")));
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
        let consent = if req.yes {
            Consent::AssumeYes
        } else {
            Consent::Ask
        };
        let answers = prompt::ask_all(
            &questions,
            consent,
            &tty,
            &mut *self.env.stdin,
            &mut *self.env.prompt,
        );
        match answers {
            Ok(a) if a.all_yes() => {}
            Ok(_) => {
                self.report_overrides();
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

        let mut repo_writes: Vec<(PathBuf, Vec<u8>)> = Vec::new();
        let mut records: Vec<(PathBuf, Vec<u8>)> = Vec::new();
        let mut meta_changed = false;
        for f in &planned.files {
            if let Some(w) = &f.write {
                repo_writes.push((PathBuf::from(&f.path), w.after.clone()));
            }
            if let Some(b) = &f.baseline {
                records.push((baseline_file(repo, &f.path), b.clone()));
            }
            if let Some(r) = &f.record {
                if let Err(e) = meta.put(r.clone()) {
                    return Err(self.internal(e.to_string()));
                }
                meta_changed = true;
            }
            // 合併結果解析不過的檔記入 `conflicts`，合併寫入成功的拿掉（scope_roadmap:32）。
            if let Some(conflicted) = f.conflict {
                match meta.set_conflict(&f.path, conflicted) {
                    Ok(changed) => meta_changed |= changed,
                    Err(e) => return Err(self.internal(e.to_string())),
                }
            }
        }
        // 換版、合併不換紀錄（`FilePlan::record` 是 `None`）：每一份含這個路徑的紀錄檔都以同一份
        // 寫入前內容更新 hash，這個工具自己的也一樣（initfiles 模組說明）。
        let writes: Vec<(&str, &[u8], &[u8])> = planned
            .files
            .iter()
            .filter_map(|f| {
                let w = f.write.as_ref()?;
                Some((f.path.as_str(), w.before.as_deref()?, w.after.as_slice()))
            })
            .collect();
        for (p, before, after) in &writes {
            match meta.record_write(p, before, after) {
                Ok(metadata::WriteOutcome::Updated) => meta_changed = true,
                Ok(_) => {}
                Err(e) => return Err(self.internal(e.to_string())),
            }
        }
        if meta_changed {
            let rendered = meta.render(self.env.written_by);
            let rendered = rendered.map_err(|e| self.internal(e.to_string()))?;
            let rel = meta_path
                .strip_prefix(&vk)
                .map(Path::to_path_buf)
                .unwrap_or_else(|_| meta_path.clone());
            records.push((rel, rendered.into_bytes()));
        }
        self.other_records(repo, &writes, &lockfile, &mut records)?;

        if let Err(e) = lockfile.set_tool(repo, locked) {
            return Err(self.internal(e.to_string()));
        }
        let entry = self.entry(installed.namespaces, &candidate)?;
        let init_files = !repo_writes.is_empty() || !records.is_empty();
        let argv = self.env.argv;
        let progress = self.progress(argv, repo, locked, init_files)?;
        self.land(
            &candidate,
            progress,
            &repo_writes,
            &records,
            &entry,
            &mut lockfile,
        )?;

        self.report_overrides();
        self.say(&text::upgraded(repo, current, locked));
        for f in &planned.files {
            if let Some(line) = text::file_line(f) {
                self.say(&line);
            }
        }
        for f in &planned.files {
            if let Some(line) = text::listed_line(repo, locked.tag(), f) {
                self.say(&line);
            }
        }
        for f in &planned.files {
            if let Some(m) = f.message() {
                let d = Diagnostic::new(m)
                    .arg("file", f.path.as_str())
                    .arg("repo", repo)
                    .arg("tag", locked.tag().to_string());
                self.emit(d);
            }
        }
        Ok(())
    }

    /// 其他紀錄檔（其他工具的、`baseline/.vendor_kit.toml`）裡同一個路徑的紀錄（ADR-0003）：寫入前內容
    /// 相符的紀錄跟著換成寫入後的 hash。
    fn other_records(
        &mut self,
        repo: &str,
        writes: &[(&str, &[u8], &[u8])],
        lockfile: &LockFile,
        records: &mut Vec<(PathBuf, Vec<u8>)>,
    ) -> Step<()> {
        if writes.is_empty() {
            return Ok(());
        }
        let vk = self.env.dir.vk_dir();
        let mut paths = vec![metadata::vk_path(self.env.dir)];
        for other in lockfile.tools().keys().filter(|r| r.as_str() != repo) {
            paths.push(self.meta_path(other)?);
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
            for (p, before, after) in writes {
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

    /// 這次全部工具的 `gen/tools.just`：其他工具的 `<ns>` 加上換版後的這個工具；開著覆寫的工具（這個工具
    /// 也算）用本機開發來源的 `<ns>`，那幾行指向本機開發來源。
    fn entry(
        &mut self,
        mut all: BTreeMap<String, Vec<String>>,
        candidate: &Candidate,
    ) -> Step<String> {
        let repo = candidate.repo();
        let namespaces = match self.local.get(repo) {
            Some(l) => l.namespaces.clone(),
            None => candidate.namespaces().to_vec(),
        };
        all.insert(repo.to_owned(), namespaces);
        let dirs: BTreeMap<String, String> = self
            .local
            .iter()
            .map(|(r, l)| (r.clone(), l.dir.clone()))
            .collect();
        let tools: Vec<tools_just::Tool> = all
            .iter()
            .map(|(r, ns)| tools_just::Tool {
                repo: r,
                namespaces: ns,
            })
            .collect();
        tools_just::render_with(&tools, &dirs).map_err(|e| self.internal(e.to_string()))
    }

    /// 這次的進度檔：共同欄位之外記 `[upgrade]` 表（`progress::upgrade`）。
    fn progress<A: AsRef<str>>(
        &mut self,
        command: &[A],
        repo: &str,
        locked: &ImageRef,
        init_files: bool,
    ) -> Step<Progress> {
        let mut p = match Progress::new(VERB, self.env.run_id, command) {
            Ok(p) => p,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let doc = p.document_mut();
        let set = doc
            .set(&[table::TABLE, table::TARGET], repo)
            .and_then(|()| doc.set(&[table::TABLE, table::IMAGE], locked.to_string()))
            .and_then(|()| doc.set(&[table::TABLE, table::INIT_FILES], init_files));
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
        let stamp = stamp::tool_file(self.env.dir, candidate.repo());
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
    fn recover_all(&mut self, lockfile: &LockFile) -> Step<bool> {
        let entries = match progress::find(self.env.dir) {
            Ok(e) => e,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let mut lockfile = lockfile.clone();
        let mut any = false;
        for entry in entries {
            if entry.verb != VERB {
                return Err(self.gap(format_args!(
                    "upgrade while the incomplete {} operation in {} remains",
                    entry.verb,
                    self.rel(&entry.path)
                )));
            }
            self.recover(&entry, &lockfile)?;
            lockfile = self.lockfile()?;
            any = true;
        }
        Ok(any)
    }

    /// 恢復一份殘留的工具 `upgrade`：依進度檔記的版本鎖定行值，以帶 digest 的引用 inspect（本機沒有就
    /// `pull` 再 inspect），重新取件、驗證，再走一次同樣的落地順序；新的進度檔完成之後才刪舊的那一份，
    /// 中途再斷也還認得出來。只在那次沒寫初始檔相關的檔時做（見模組說明的缺口）。
    fn recover(&mut self, entry: &progress::Entry, lockfile: &LockFile) -> Step<()> {
        let old = match entry.load() {
            Ok(p) => p,
            Err(progress::Error::Parse {
                file,
                source: progress::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => return Err(self.too_new(&file, &t)),
            Err(e) => return Err(self.failed(&entry.path, e.message(), e.to_string())),
        };
        let target = table::field(&old, table::TARGET).map(str::to_owned);
        let image = table::field(&old, table::IMAGE).map(str::to_owned);
        let init_files = table::flag(&old, table::INIT_FILES);
        let file = self.rel(&entry.path);
        if target.as_deref() == Some(table::ENGINE_TARGET) {
            return Err(self.gap(format_args!(
                "recovering the incomplete engine upgrade in {file}"
            )));
        }
        let (Some(repo), Some(image), Some(init_files)) = (target, image, init_files) else {
            return Err(self.gap(format_args!(
                "recovering {file} without the [upgrade] fields"
            )));
        };
        if init_files {
            return Err(self.gap(format_args!("recovering {file}, which writes init files")));
        }
        let Ok(locked) = ImageRef::parse(&image) else {
            return Err(self.internal(format!("{file} records image {image:?}")));
        };
        let pinned = format!(
            "{}/{}@{}",
            locked.registry(),
            locked.path(),
            locked.digest()
        );
        let Some(wire) = plan::ImageRef::parse(&pinned).filter(plan::ImageRef::is_pinned) else {
            return Err(self.internal(format!("cannot request {pinned}")));
        };
        let inspected = match self.inspect(&wire)? {
            Ok(i) => i,
            Err(_) => {
                let (_, outcome) = self.request(&Op::Pull(wire.clone()))?;
                match outcome {
                    Outcome::Ok => {}
                    Outcome::Failed(rc) => {
                        return Err(self.access_failed(
                            &image,
                            &repo,
                            text::docker_failed("pull", rc),
                        ));
                    }
                    Outcome::Runner(_) => {
                        return Err(self.internal("pull returned a runner result"));
                    }
                }
                match self.inspect(&wire)? {
                    Ok(i) => i,
                    Err(rc) => {
                        return Err(self.access_failed(
                            &image,
                            &repo,
                            text::docker_failed("inspect", rc),
                        ));
                    }
                }
            }
        };
        let Some(id) = ImageId::parse(&inspected.id) else {
            return Err(self.internal(format!("image inspect returned Id {:?}", inspected.id)));
        };
        let resolved = Resolved {
            locked,
            id,
            repo_digests: inspected.repo_digests,
        };
        let (candidate, installed) = self.fetch(&repo, &resolved, lockfile)?;
        if let Err(e) = candidate.recheck() {
            return Err(self.internal(format!("staged content of {repo} changed: {e}")));
        }
        let mut lockfile = lockfile.clone();
        if let Err(e) = lockfile.set_tool(&repo, &resolved.locked) {
            return Err(self.internal(e.to_string()));
        }
        let entry_text = self.entry(installed.namespaces, &candidate)?;
        let progress = self.progress(old.command(), &repo, &resolved.locked, false)?;
        self.land(&candidate, progress, &[], &[], &entry_text, &mut lockfile)?;
        if let Err(e) = progress::delete(self.env.dir, &entry.verb, &entry.id) {
            return Err(self.failed(&entry.path, e.message(), e.to_string()));
        }
        self.say(&text::recovered(&repo, &resolved.locked));
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
