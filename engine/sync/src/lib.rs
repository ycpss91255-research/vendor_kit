//! `sync` 指令（04 指令表 `sync`、04 sync 節）：依版本鎖定行同步全部已導入工具的 `cache/` 與 `gen/`。
//!
//! 呼叫端（入口 `vendor_kit`）已解析好參數、判過安裝目錄（VK0028），並接好執行紀錄與 `plan` 往返。
//! 這裡依序做：
//!
//! 1. 讀 `.vendor_kit/config.toml`（VK0059），在第一次取鎖之前（04 設定）。
//! 2. 取安裝目錄的排他鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束：會取件的 `sync`
//!    屬寫入端（04 鎖與逾時）。
//! 3. 讀 `version.toml`（檔案版過高回 VK0008）。
//! 4. 逐工具處理前先判（04 sync 第 2 步；02 不變量 4：動到任何工具之前判定有工具不能做，就一個都不動，
//!    並列出每個原因）。這一段只讀、不取件、不寫：
//!    - 每個讀到的 VK 檔（`version.local.toml`、進度檔、每個工具的印記）檔案版過高：VK0008。
//!    - 殘留的進度檔：`sync` 自己的留到這次一起完成（見下面「恢復」）；`add` 的回 VK0004（`sync` 不代替
//!      完成導入）；其他的見「缺口」。
//!    - 每個工具的印記：不在（首次取件，不算損壞）、損壞（VK0044）或讀得到。
//! 5. 逐工具判定要不要重取（04 sync 表）：
//!    - 印記不在：取件，不警告。
//!    - 印記損壞：重新取件並重建印記，警告 VK0044。
//!    - 印記的版本與版本鎖定行不同（例如 `git pull` 換了鎖定行）：取件，不警告；VK0015 的情況只講檔案集合
//!      與逐檔指紋不符。
//!    - 版本相同：以印記比對 `cache/<repo>/` 的檔案集合與逐檔指紋，包括多出的檔與整個目錄不在；不一致就
//!      重新取件，警告 VK0015。一致就不動，`<ns>` 從 `cache/<repo>/` 讀。
//!    - 未列在版本鎖定行的工具目錄不看，留給 `prune`；初始檔不動（基準版落後見「缺口」）。
//! 6. 要取件的工具，經 `plan` 協定請啟動器 `inspect` 帶 digest 的引用 `<registry>/<路徑>@<digest>`；本機沒有
//!    就 `pull` 同一個引用再 `inspect`，再以 image ID `extract`。docker 動作失敗回 VK0055。只用
//!    [`plan::RESCUE_OPS`] 裡的 op：`sync` 是救援路徑（ADR-0007、ADR-0008 凍結子集）。
//! 7. `fetch::verify`：inspect 回來的 RepoDigests 要有版本鎖定行的 digest，不符回 VK0043（不報 VK0015）；
//!    dist 格式、逐檔指紋。一個工具失敗時其他工具照樣取件驗證，列出每個原因，但一個都不落地。
//! 8. 用 `tools_just` 依這次的全部工具（重取的用暫存內容的 `<ns>`，沒重取的讀 `cache/<repo>/`）重產
//!    `gen/tools.just`，與現有內容逐位元組比對。
//! 9. 沒有要重取的工具、入口檔不變、也沒有殘留的 `sync` 進度檔：什麼都不寫，stdout 不印（[`text`]）。
//! 10. 否則重驗暫存內容（ADR-0006 第三層），經 `txn` 依序落地：`cache/<repo>/` 與印記、`gen/tools.just`；
//!     不改版本鎖定行（04 成對與無害：`sync` 不改追蹤檔），最後刪進度檔。
//! 11. stdout 列出改了什麼；VK0015、VK0044 在落地之後才印（本文是「已重新取件」）。
//!
//! # 恢復
//!
//! 殘留的 `sync` 進度檔表示上一次 `sync` 中途停了。`sync` 本身就是「把 `cache/`、`gen/` 對齊版本鎖定行」，
//! 所以恢復就是照常做一次：換到一半的 `cache/<repo>/` 會在第 5 步被判成不一致而重取。這次的落地完成之後
//! 才刪殘留的那幾份，中途再斷也還認得出來；有殘留時即使沒有要重取的工具，也走一次 `txn`，讓刪除排在
//! `writes_started` 之後。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 印記的位置與 `add` 共用 [`stamp::tool_file`]（`.vendor_kit/cache/<repo>.stamp.toml`）。
//! - 進度檔 `.tmp.sync.<run-id>.toml` 只有 `progress` 的共同欄位，沒有 `sync` 自己的表：恢復不需要。
//! - 取件的 slot 名是 [`SLOT_PREFIX`] 加這次執行裡的序號（`tool1`、`tool2`…）。
//! - docker `image inspect` 的輸出只讀 `Id` 與 `RepoDigests`（[`parse_inspect`]）。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - 已知偏離：04 sync 第 2 步要在逐工具處理前判薄殼（VK0006），但薄殼模板還沒隨 image 出貨、沒有任何
//!   crate 產得出這一版的模板（`shell::Shell::render` 要呼叫端給模板本文），所以這裡還不判薄殼。版本組合的
//!   介面版（VK0009）由啟動器在起引擎前判，不在引擎。
//! - 本機覆寫：`version.local.toml` 有工具的覆寫（`dev <repo> -p <dir>`）時停下。`dev` 讓 `gen/tools.just`
//!   改指本機目錄、`cache/<repo>/` 不動（engine/dev），但 `sync` 遇到覆寫時要不要照常對齊那個工具的
//!   `cache/`、本機目錄失效時報不報 VK0052，以及「每次報告用了哪個覆寫」（stdout）跟沒有變更時 stdout 不印
//!   （#119）怎麼並存，都沒定。所以 `dev` 之後工具 recipe 前的自動 `sync` 也會停下。引擎的覆寫與工具同步
//!   無關，不看。
//! - 殘留的進度檔不是 `sync` 或 `add` 的。`undev` 的：04 本機覆寫說 `sync` 不代替完成或清掉它，VK0053 只寫
//!   `undev` 自己同步失敗與唯讀 recipe 偵測到，`sync` 遇到時怎麼報沒定。
//! - 基準版落後（VK0014）：`metadata` 沒有記基準版是哪一版，判不出來；工具有 metadata 時停下。目前
//!   `add` 只在有初始檔時才寫 metadata，而 `init.toml` 格式未定，所以實際上碰不到。
//! - 取到的內容與同一版本的既有印記不符（計畫 G1：印記被改過，或同一 digest 取出不同內容），沒有代碼。
//! - dist 格式不符（G2）、工具交付保留名 `vendor_kit`、兩個工具交付同一個 `<ns>`，`sync` 都沒有代碼。
//! - 中途寫檔失敗沒有代碼（G4）。
//! - 工具 recipe 前的自動 `sync`：引擎分不出這次是不是自動觸發，警告後本體跑不跑、整次回碼見 #120。
//!
//! 這裡不直接碰 docker：docker 動作一律是 `plan` 協定的 op，由啟動器代做。

pub mod text;

#[cfg(test)]
mod tests;

use std::collections::BTreeMap;
use std::fs;
use std::io::{self, Write};
use std::path::{Path, PathBuf};
use std::time::Duration;

use config::{Config, ConfigError};
use diagnostics::{Diagnostic, Diagnostics, Message, Sink};
use fetch::{Candidate, Staged, Taken};
use filelock::{Lock, Mode};
use imageref::ImageRef;
use layout::InstallDir;
use plan::{Channel, ImageId, Op, Outcome, Slot};
use progress::Progress;
use stamp::Stamp;
use txn::{Disk, ToolContent, Txn};
use version_file::{LocalFile, LockFile};

/// 進度檔的 `<verb>`。
pub const VERB: &str = "sync";
/// `add` 的進度檔 `<verb>` 與它記 `<repo>` 的表（engine/add 的 `VERB`、`PROGRESS_TABLE`；指令之間互不依賴，照抄）。
pub const ADD_VERB: &str = "add";
/// 取件的 slot 名前綴，後面接這次執行裡的序號（從 1 起）。
pub const SLOT_PREFIX: &str = "tool";

/// 這次執行的環境：容器內的路徑、往返通道與輸出。`sync` 不詢問，所以沒有 stdin 與終端狀態。
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
    /// `just vendor_kit` 之後的參數原樣（第一個是 `sync`）。
    pub argv: &'a [String],
    /// 這次執行的 run-id，也是進度檔的 `<id>`。
    pub run_id: &'a str,
    /// 蓋在 VK 檔上的寫入者。
    pub written_by: &'a str,
    pub stdout: &'a mut dyn Write,
    pub diags: &'a mut Diagnostics<W, S>,
    /// 執行紀錄（`txn` 寫里程碑事件）。
    pub log: &'a mut runlog::Writer<L>,
}

/// 跑一次 `sync`，回傳結束碼。
pub fn run<W: Write, S: Sink, L: Write>(env: &mut Env<'_, W, S, L>) -> u8 {
    let mut sync = Sync {
        env,
        code: 0,
        extracts: 0,
    };
    let _ = sync.run();
    sync.code
}

/// `docker image inspect` 輸出裡用得到的兩個欄位。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Inspected {
    /// `Id`：`sha256:<64hex>`。
    pub id: String,
    /// `RepoDigests`：每筆 `<registry>/<路徑>@sha256:<digest>`。
    pub repo_digests: Vec<String>,
}

/// 解析 `docker image inspect <ref>` 的 JSON：一個陣列，剛好一個物件。
pub fn parse_inspect(bytes: &[u8]) -> Result<Inspected, String> {
    let value: serde_json::Value = serde_json::from_slice(bytes)
        .map_err(|e| format!("image inspect output is not JSON: {e}"))?;
    let items = value
        .as_array()
        .ok_or("image inspect output is not a JSON array")?;
    let [item] = items.as_slice() else {
        return Err(format!(
            "image inspect output has {} entries, expected 1",
            items.len()
        ));
    };
    let id = item
        .get("Id")
        .and_then(serde_json::Value::as_str)
        .ok_or("image inspect output has no Id")?
        .to_owned();
    let repo_digests = match item.get("RepoDigests") {
        None | Some(serde_json::Value::Null) => Vec::new(),
        Some(v) => v
            .as_array()
            .ok_or("image inspect RepoDigests is not an array")?
            .iter()
            .map(|d| {
                d.as_str()
                    .map(str::to_owned)
                    .ok_or("image inspect RepoDigests has a non-string entry")
            })
            .collect::<Result<_, _>>()?,
    };
    Ok(Inspected { id, repo_digests })
}

/// 診斷已印、這次執行停下。
struct Stop;

type Step<T> = Result<T, Stop>;

/// 一個工具的印記讀出來的樣子。
enum StampState {
    /// 不在：首次取件，不算損壞。
    Absent,
    /// 損壞（VK0044）。
    Corrupt,
    Present(Box<Stamp>),
}

/// 一個工具要怎麼處理。
enum Need {
    /// `cache/<repo>/` 與印記一致，不動；帶著讀出的 `<ns>`。
    Keep(Vec<String>),
    /// 要取件；`warn` 是落地後要印的警告，`previous` 是同一個版本的既有印記。
    Fetch {
        warn: Option<&'static Message>,
        previous: Option<Box<Stamp>>,
    },
}

/// 取到、驗過的一個工具。
struct Fetched {
    candidate: Candidate,
    warn: Option<&'static Message>,
}

struct Sync<'r, 'a, W: Write, S: Sink, L: Write> {
    env: &'r mut Env<'a, W, S, L>,
    code: u8,
    /// 這次執行已用掉的 slot 數。
    extracts: u32,
}

impl<W: Write, S: Sink, L: Write> Sync<'_, '_, W, S, L> {
    // ---- 診斷 ----

    fn emit(&mut self, d: Diagnostic) {
        self.code = self.code.max(d.message().exit_code());
        let _ = self.env.diags.emit(&d);
    }

    fn stop(&mut self, d: Diagnostic) -> Stop {
        self.emit(d);
        Stop
    }

    /// VK0056 的診斷：契約還沒定的情況，或 VK 自己的錯。
    fn internal_diag(&self, reason: impl Into<String>) -> Diagnostic {
        Diagnostic::new(&messages::VK0056)
            .arg("reason", reason)
            .arg("path", self.env.run_log)
    }

    fn internal(&mut self, reason: impl Into<String>) -> Stop {
        let d = self.internal_diag(reason);
        self.stop(d)
    }

    fn gap_diag(&self, what: impl std::fmt::Display) -> Diagnostic {
        self.internal_diag(format!("{what} is not supported yet"))
    }

    fn gap(&mut self, what: impl std::fmt::Display) -> Stop {
        let d = self.gap_diag(what);
        self.stop(d)
    }

    /// VK0008：檔案版過高。
    fn too_new_diag(&self, file: &Path, t: &schema::TooNew) -> Diagnostic {
        Diagnostic::new(&messages::VK0008)
            .arg("file", self.rel(file))
            .arg("N", t.found().to_string())
            .arg("M", t.max().to_string())
            .arg("written_by", t.written_by().unwrap_or("unknown"))
    }

    /// 底層 crate 回的錯：有代碼就照代碼印（只有一個 `<file>` 占位符的 VK0013），否則當內部錯誤。
    fn failed_diag(
        &self,
        file: &Path,
        message: Option<&'static Message>,
        detail: String,
    ) -> Diagnostic {
        match message {
            Some(m) if m.code == messages::VK0013.code => Diagnostic::new(&messages::VK0013)
                .arg("file", self.rel(file))
                .arg("path", self.env.run_log),
            _ => self.internal_diag(detail),
        }
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

    fn run(&mut self) -> Step<()> {
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        let lockfile = self.lockfile()?;
        let (residual, mut stamps) = self.judge(&lockfile)?;

        let mut keep: BTreeMap<String, Vec<String>> = BTreeMap::new();
        let mut fetched: Vec<Fetched> = Vec::new();
        let mut failed = false;
        for (repo, locked) in lockfile.tools() {
            let state = stamps.remove(repo).unwrap_or(StampState::Absent);
            match self.need(repo, locked, state)? {
                Need::Keep(ns) => {
                    keep.insert(repo.clone(), ns);
                }
                Need::Fetch { warn, previous } => {
                    match self.fetch(repo, locked, previous.as_deref()) {
                        Ok(candidate) => fetched.push(Fetched { candidate, warn }),
                        Err(Stop) => failed = true,
                    }
                }
            }
        }
        if failed {
            return Err(Stop);
        }

        let entry = self.render_entry(&keep, &fetched)?;
        let path = self.env.dir.gen_dir().join(txn::TOOLS_JUST);
        let current = match fs::read(&path) {
            Ok(b) => Some(b),
            Err(e) if e.kind() == io::ErrorKind::NotFound => None,
            Err(e) => return Err(self.internal(format!("{}: {e}", path.display()))),
        };
        let entry_changed = current.as_deref() != Some(entry.as_bytes());
        if fetched.is_empty() && !entry_changed && residual.is_empty() {
            return Ok(());
        }

        for f in &fetched {
            if let Err(e) = f.candidate.recheck() {
                let repo = f.candidate.repo().to_owned();
                return Err(self.internal(format!("staged content of {repo} changed: {e}")));
            }
        }
        self.land(&fetched, entry_changed.then_some(entry.as_bytes()))?;
        for e in &residual {
            if let Err(err) = progress::delete(self.env.dir, &e.verb, &e.id) {
                let d = self.failed_diag(&e.path, err.message(), err.to_string());
                return Err(self.stop(d));
            }
        }

        for f in &fetched {
            self.say(&text::fetched(f.candidate.repo(), f.candidate.locked()));
        }
        if entry_changed {
            self.say(text::TOOLS_JUST_UPDATED);
        }
        for e in &residual {
            let shown = self.rel(&e.path);
            self.say(&text::recovered(&shown));
        }
        for f in &fetched {
            if let Some(m) = f.warn {
                let d = Diagnostic::new(m).arg("repo", f.candidate.repo());
                self.emit(d);
            }
        }
        Ok(())
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
            }) => {
                let d = self.too_new_diag(&file, &t);
                Err(self.stop(d))
            }
            Err(e) => Err(self.internal(e.to_string())),
        }
    }

    /// 逐工具處理前的判定（模組說明第 4 步）：只讀。有任何一項不能做就把每一項都印出來再停下。
    /// 回傳殘留的 `sync` 進度檔與每個工具的印記。
    #[allow(clippy::type_complexity)]
    fn judge(
        &mut self,
        lockfile: &LockFile,
    ) -> Step<(Vec<progress::Entry>, BTreeMap<String, StampState>)> {
        let mut blocked: Vec<Diagnostic> = Vec::new();

        match LocalFile::load_from(self.env.dir) {
            Ok(Some(local)) => {
                if let Some(repo) = local.tools().keys().next() {
                    blocked.push(self.gap_diag(format_args!(
                        "sync while {repo} has a local override in .vendor_kit/version.local.toml"
                    )));
                }
            }
            Ok(None) => {}
            Err(version_file::Error::Parse {
                file,
                source: version_file::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => blocked.push(self.too_new_diag(&file, &t)),
            Err(e) => blocked.push(self.internal_diag(e.to_string())),
        }

        let mut residual = Vec::new();
        match progress::find(self.env.dir) {
            Ok(entries) => {
                for entry in entries {
                    match self.residual(&entry) {
                        Ok(()) => residual.push(entry),
                        Err(d) => blocked.push(d),
                    }
                }
            }
            Err(e) => blocked.push(self.internal_diag(e.to_string())),
        }

        let mut stamps = BTreeMap::new();
        for repo in lockfile.tools().keys() {
            if !fetch::is_namespace(repo) {
                blocked.push(self.gap_diag(format_args!("tool name {repo:?} (not a just name)")));
                continue;
            }
            let file = stamp::tool_file(self.env.dir, repo);
            match Stamp::load(&file) {
                Ok(None) => {
                    stamps.insert(repo.clone(), StampState::Absent);
                }
                Ok(Some(s)) => {
                    stamps.insert(repo.clone(), StampState::Present(Box::new(s)));
                }
                Err(stamp::Error::Corrupt { .. }) => {
                    stamps.insert(repo.clone(), StampState::Corrupt);
                }
                Err(stamp::Error::TooNew { file, too_new }) => {
                    blocked.push(self.too_new_diag(&file, &too_new));
                }
                Err(e) => blocked.push(self.internal_diag(e.to_string())),
            }
            match metadata::tool_path(self.env.dir, repo) {
                Ok(p) if p.exists() => blocked.push(self.gap_diag(format_args!(
                    "judging whether the baseline of {repo} is behind the lock version line"
                ))),
                Ok(_) => {}
                Err(e) => blocked.push(self.internal_diag(e.to_string())),
            }
        }

        if blocked.is_empty() {
            Ok((residual, stamps))
        } else {
            for d in blocked {
                self.emit(d);
            }
            Err(Stop)
        }
    }

    /// 一份殘留的進度檔：`sync` 的回 `Ok`（這次一起完成），其他的回要印的診斷。
    fn residual(&self, entry: &progress::Entry) -> Result<(), Diagnostic> {
        let loaded = match entry.load() {
            Ok(p) => p,
            Err(progress::Error::Parse {
                file,
                source: progress::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => return Err(self.too_new_diag(&file, &t)),
            Err(e) => return Err(self.failed_diag(&entry.path, e.message(), e.to_string())),
        };
        match entry.verb.as_str() {
            VERB => Ok(()),
            ADD_VERB => {
                let repo = loaded
                    .document()
                    .get(&[ADD_VERB, "repo"])
                    .and_then(|i| i.as_str())
                    .map(str::to_owned);
                match repo {
                    Some(repo) => Err(Diagnostic::new(&messages::VK0004).arg("repo", repo)),
                    None => Err(self.gap_diag(format_args!(
                        "reporting the incomplete add in {} without its [add] repo field",
                        self.rel(&entry.path)
                    ))),
                }
            }
            other => Err(self.gap_diag(format_args!(
                "sync while the incomplete {other} operation in {} remains",
                self.rel(&entry.path)
            ))),
        }
    }

    /// 一個工具要不要重取（模組說明第 5 步）。
    fn need(&mut self, repo: &str, locked: &ImageRef, state: StampState) -> Step<Need> {
        let version = locked.to_string();
        let stamp = match state {
            StampState::Absent => {
                return Ok(Need::Fetch {
                    warn: None,
                    previous: None,
                });
            }
            StampState::Corrupt => {
                return Ok(Need::Fetch {
                    warn: Some(&messages::VK0044),
                    previous: None,
                });
            }
            StampState::Present(s) if s.version() != version => {
                return Ok(Need::Fetch {
                    warn: None,
                    previous: None,
                });
            }
            StampState::Present(s) => s,
        };
        let cache = match self.env.dir.tool_cache(repo) {
            Ok(c) => c,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let diff = match stamp.verify(&cache) {
            Ok(d) => d,
            Err(e) => return Err(self.internal(format!("cache of {repo}: {e}"))),
        };
        if !diff.is_match() {
            return Ok(Need::Fetch {
                warn: diff.message(),
                previous: Some(stamp),
            });
        }
        match fetch::namespaces(&cache) {
            Ok(ns) => Ok(Need::Keep(ns)),
            Err(e) => Err(self.internal(format!(
                "cache of {repo} matches its stamp, but its tool content is invalid: {e}"
            ))),
        }
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

    /// 依版本鎖定行取件並驗證（模組說明第 6、7 步）。
    fn fetch(
        &mut self,
        repo: &str,
        locked: &ImageRef,
        previous: Option<&Stamp>,
    ) -> Step<Candidate> {
        let shown = locked.to_string();
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
                // 本機沒有這個 image：以同一個帶 digest 的引用 pull，再 inspect。
                let (_, outcome) = self.request(&Op::Pull(wire.clone()))?;
                match outcome {
                    Outcome::Ok => {}
                    Outcome::Failed(rc) => {
                        return Err(self.access_failed(
                            &shown,
                            repo,
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
                            &shown,
                            repo,
                            text::docker_failed("inspect", rc),
                        ));
                    }
                }
            }
        };
        let Some(id) = ImageId::parse(&inspected.id) else {
            return Err(self.internal(format!("image inspect returned Id {:?}", inspected.id)));
        };

        self.extracts += 1;
        let slot = format!("{SLOT_PREFIX}{}", self.extracts);
        let Some(slot_v) = Slot::parse(&slot) else {
            return Err(self.internal(format!("invalid slot {slot}")));
        };
        let (_, outcome) = self.request(&Op::Extract(id, slot_v))?;
        match outcome {
            Outcome::Ok => {}
            Outcome::Failed(rc) => {
                return Err(self.access_failed(&shown, repo, text::docker_failed("extract", rc)));
            }
            Outcome::Runner(_) => return Err(self.internal("extract returned a runner result")),
        }
        let root = self.env.inbox.join(&slot);
        let staged = Staged {
            repo,
            locked,
            root: &root,
            repo_digests: &inspected.repo_digests,
        };
        match fetch::verify(&staged, &Taken::new(), previous) {
            Ok(c) => Ok(c),
            Err(fetch::Error::DigestMismatch { .. }) => {
                let d = Diagnostic::new(&messages::VK0043)
                    .arg("repo", repo)
                    .arg("image", shown.as_str())
                    .arg("digest", locked.digest().to_string());
                Err(self.stop(d))
            }
            Err(fetch::Error::Collision { .. }) => Err(self.gap(format_args!(
                "sync of {repo}, which delivers the reserved namespace {}",
                fetch::RESERVED
            ))),
            Err(fetch::Error::Fingerprint(_)) => Err(self.gap(format_args!(
                "sync of {repo} whose fetched content does not match its existing stamp \
                 for the same lock version line"
            ))),
            Err(e) => Err(self.internal(format!("tool content of {repo}: {e}"))),
        }
    }

    /// 這次全部工具的 `gen/tools.just`。
    fn render_entry(
        &mut self,
        keep: &BTreeMap<String, Vec<String>>,
        fetched: &[Fetched],
    ) -> Step<String> {
        let mut all: BTreeMap<&str, &[String]> = BTreeMap::new();
        for (repo, ns) in keep {
            all.insert(repo, ns);
        }
        for f in fetched {
            all.insert(f.candidate.repo(), f.candidate.namespaces());
        }
        let tools: Vec<tools_just::Tool> = all
            .iter()
            .map(|(repo, namespaces)| tools_just::Tool { repo, namespaces })
            .collect();
        match tools_just::render(&tools) {
            Ok(t) => Ok(t),
            Err(e @ tools_just::Error::Duplicate { .. }) => {
                Err(self.gap(format_args!("sync of tools whose namespaces collide ({e})")))
            }
            Err(e) => Err(self.internal(e.to_string())),
        }
    }

    /// 依序落地（`txn`）：`cache/` 與印記、入口檔；版本鎖定行不動。
    fn land(&mut self, fetched: &[Fetched], entry: Option<&[u8]>) -> Step<txn::Done> {
        let progress = match Progress::new(VERB, self.env.run_id, self.env.argv) {
            Ok(p) => p,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let stamps: Vec<PathBuf> = fetched
            .iter()
            .map(|f| stamp::tool_file(self.env.dir, f.candidate.repo()))
            .collect();
        let tools: Vec<ToolContent> = fetched
            .iter()
            .zip(&stamps)
            .map(|(f, stamp_file)| ToolContent {
                repo: f.candidate.repo(),
                staged: f.candidate.root(),
                version: f.candidate.version(),
                stamp_file,
            })
            .collect();
        let result = {
            let mut fx = Disk::new(self.env.dir, self.env.log, self.env.written_by);
            Txn::begin(&mut fx, progress).and_then(|t| {
                t.swap_cache(&tools)?
                    .write_repo_files(&[])?
                    .write_records(&[])?
                    .write_tools_just(entry)?
                    .keep_lock_line()
                    .complete()
            })
        };
        result.map_err(|f| self.internal(f.to_string()))
    }
}
