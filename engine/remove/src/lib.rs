//! `remove <repo>` 與 `uninstall` 指令（04 指令表、收回插入的行、remove 與 uninstall 的收回範圍）：
//! 從參數到落地。兩個指令共用同一條路：收回插入行的判定（`retract`）、一次問完（`prompt`）、
//! 收回的落地順序（`txn` 的 [`txn::Txn::retract_repo_files`] 起），差別只在收回範圍。
//!
//! 呼叫端（入口 `vendor_kit`）已解析好參數、判過安裝目錄（VK0028），並接好執行紀錄與 `plan` 往返。兩個指令
//! 都不碰 docker；`plan` 往返只用在 `remove` 讀安裝目錄外的本機開發來源（`stage-dir`，見「本機覆寫」）。
//!
//! # `remove <repo>`
//!
//! 1. 讀 `.vendor_kit/config.toml`（VK0059），在第一次取鎖之前（04 設定）。
//! 2. 取安裝目錄的排他鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束。
//! 3. 讀 `version.toml` 與 `version.local.toml`（檔案版過高回 VK0008）。
//! 4. 辨識殘留的進度檔（見「恢復」），再判對象：版本鎖定行沒有 `<repo>`、殘留的 `remove` 也沒有它，
//!    回 VK0046（訊息表：先辨識未完成進度，再判斷對象不存在）。對象以外的工具開著覆寫時讀它的本機開發
//!    來源，讀不到回 VK0052（見「本機覆寫」），在詢問之前停下。
//! 5. 這次的對象是 `<repo>` 加上殘留 `remove` 記的工具。每個對象的逐檔紀錄（`baseline/<repo>.toml`，
//!    沒有就是沒有初始檔）交給 `retract`，收齊這次全部的詢問。
//! 6. `prompt` 一次問完（04 共同選項：全部同意才寫入，含恢復舊操作）：答否是正常取消（stdout 說明未變更，
//!    以 0 結束）；不能互動回 VK0002，除執行紀錄外不寫任何檔。
//! 7. 經 `txn` 的收回順序落地：收回插入行後的 repo 檔 → 重產 `gen/tools.just`（拿掉對象的 `<ns>`，
//!    其他工具的 `<ns>` 讀 `cache/<repo>/`，開著覆寫的讀本機開發來源）→ 仍保留的紀錄檔（其他工具與 `baseline/.vendor_kit.toml`
//!    裡同一個檔的紀錄跟著換成寫入後的 hash，ADR-0003；對象開著本機覆寫時，拿掉 `version.local.toml`
//!    裡對象那一行）→ 刪 `cache/<repo>/`、印記、基準版副本、`baseline/<repo>.toml` → 拿掉版本鎖定行 →
//!    刪進度檔；之後才刪殘留的進度檔。
//! 8. stdout 列出改了什麼與保留清單（04：初始檔保留，保留清單印到 stdout）；用了哪個覆寫、解除了哪個覆寫、
//!    保留的本機開發來源也列出來（04 本機覆寫：報告用了哪個覆寫，不加診斷前綴）；只列不刪的每一行在落地後
//!    印一則 VK0061（warn，結束碼 1）。
//!
//! # 本機覆寫
//!
//! 對象開著本機覆寫時比照 `uninstall`：先解除覆寫紀錄再收回，不要求先 `undev`（04：`test` 以外的一般
//! recipe 照常執行；02：覆寫只能覆蓋已存在的版本鎖定行，鎖定行收回後覆寫只能一起解除）。只拿掉那一行，
//! 不讀覆寫來源，所以來源失效也不擋；本機開發來源不動，其他工具與引擎的覆寫照留。
//!
//! 對象以外的工具開著覆寫時，重產 `gen/tools.just` 的做法跟 engine/sync、engine/upgrade 一致：
//!
//! - 它的 `<ns>` 從本機開發來源讀（`fetch::local`，值照 engine/dev 以安裝目錄為準正規化），不讀它的
//!   `cache/<repo>/`；入口檔裡它那幾行指向本機開發來源（`tools_just::render_with`）。安裝目錄外的（`dev` 收的
//!   絕對路徑，或開頭是 `..` 的相對路徑）引擎看不到，照 engine/dev 請啟動器 `stage-dir` 複製進 session 目錄的
//!   `in/<slot>`，再讀那份複本。
//! - 讀不到回 VK0052（04 本機覆寫：覆寫來源失效只擋需讀它的動作；重產入口檔要讀它），列出每個讀不到的覆寫，
//!   在詢問與任何寫入之前停下。
//! - 以 0 結束時（收回完成、答否取消）在 stdout 報告用了哪個覆寫，排在那條路徑的字句前面；停下時只印診斷。
//! - `uninstall` 刪掉 `gen/tools.just` 與 `version.local.toml`、不重產入口檔，不讀任何覆寫來源。
//!
//! # `uninstall`
//!
//! 照 04「remove 與 uninstall 的收回範圍」的目前介面（收回範圍與紀錄保存政策仍待 #47 確認）：
//!
//! 1. 同 `remove` 的 1–3。
//! 2. 殘留的 `uninstall` 與 `remove` 進度檔併進這次（`uninstall` 收回的範圍涵蓋它們）。
//! 3. `baseline/` 下每一份逐檔紀錄（各工具的與 `.vendor_kit.toml`：根 `justfile` 的 `import`、根
//!    `.dockerignore` 的四行也在這裡）一起交給 `retract`，一次問完；答否與不能互動同 `remove`。
//! 4. 落地：收回插入行 → 刪 `gen/tools.just` → 刪 `cache/`、`baseline/`、`gen/`、`version.local.toml`
//!    （解除覆寫紀錄，本機開發來源不動）、薄殼四檔 → 刪 `version.toml`（全部版本鎖定行）→ 刪進度檔。
//!    `config.toml`、`log/`、`.vendor_kit/` 目錄與 `.vendor_kit/` 下其他的項目都不碰。
//! 5. stdout 列出改了什麼與留下的內容：初始檔、本機開發來源，與 `.vendor_kit/` 裡還在的每一項（`install`
//!    建的 `config.toml` 記在 `baseline/.vendor_kit.toml`，已在初始檔那段列過的不重複列）。
//!
//! # 恢復
//!
//! 殘留的 `remove`（`uninstall` 時另含 `uninstall`）進度檔表示上一次中途停了。這次把它記的工具併進
//! 對象一起收回：收回的每一步都可重做（刪不在的路徑不算錯，版本鎖定行沒有就不動），所以恢復就是照常再做
//! 一次。殘留的詢問與這次的詢問一起問完、全部同意才寫，答否時殘留的進度檔照留。這次落地完成之後才刪殘留
//! 的那幾份，中途再斷也還認得出來。
//!
//! 覆寫紀錄的解除也一樣可重做，兩種半套都照常再做一次就補完：覆寫已解除、版本鎖定行還在（落地停在紀錄檔
//! 之後、鎖定行之前），重跑時覆寫已不在、照常收回鎖定行；鎖定行已拿掉、覆寫還在，殘留 `remove` 記的對象
//! 一樣會解除覆寫。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 進度檔 `.tmp.<verb>.<run-id>.toml` 另記 `[<verb>]` 表的 `repos`（這次收回的工具）與
//!   `repo_files`（這次有沒有要寫 repo 檔）。
//! - 覆寫的解除排在紀錄檔那一步（寫回拿掉對象那一行的 `version.local.toml`），在版本鎖定行之前；進度檔不另記
//!   覆寫，恢復時照 `repos` 重算。上一次已解除的覆寫，恢復時不再報告（原來的來源已經不在檔裡）。
//! - 覆寫全部解除後 `version.local.toml` 照留（只剩檔案版與寫入者），跟 `dev` 相同。
//! - 保留清單列逐檔紀錄裡 state 是 `managed` 或 `appended` 的檔（VK 建立或插入過的初始檔）。
//! - `uninstall` 把 `cache/`、`baseline/`、`gen/` 整個目錄當成 VK 的工作狀態刪掉（含未鎖定工具的
//!   `cache/` 目錄與沒有對應版本鎖定行的紀錄），不逐項比對。
//! - `uninstall` 刪掉整份 `version.toml`；執行紀錄的鎖定行事件記成引擎的（`target = engine`）。
//! - stdout 的字句與詢問文字（英文）見 [`text`]；用了哪個覆寫的報告字句跟 engine/sync 相同
//!   （[`text::local_override`]）。
//! - 本機開發來源的正規化與檢查跟 engine/dev、engine/sync、engine/upgrade 共用 `fetch::local`；`stage-dir` 的
//!   slot 名是 `fetch::local::STAGE_SLOT_PREFIX` 加這次執行裡的序號（`dev1`、`dev2`…）。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - 版本鎖定行沒有 `<repo>`、也沒有殘留的 `remove` 記它，`version.local.toml` 卻還有它的覆寫（孤兒覆寫）：
//!   照 VK0046 停下；孤兒覆寫訊息表還沒有代碼（`version_file::OrphanOverrides`）。對象以外的孤兒覆寫同樣
//!   沒有代碼，停下。
//! - 對象以外開著覆寫的工具交付保留名 `vendor_kit`：沒有代碼（同 engine/upgrade）。
//! - `-y`：兩個指令都還不收（#47，`args` 照 #489）；VK0002 的下一步指令照訊息表插入 `-y`。
//! - 殘留的進度檔不是可以併入的 verb（`add`、`install` 等），或殘留的操作要寫 repo 檔：那次寫了哪些
//!   repo 檔沒有記錄，重新判定會把 VK 自己剛收回的結果當成使用者改過（假的 VK0061）。
//! - `retract` 判成契約沒寫到的紀錄組合（非 `appended` 卻有 `lines` 等）。
//! - 其他已裝、沒開覆寫的工具的 `cache/<repo>/` 讀不到（例如全新 checkout 還沒 `sync`）：重產入口檔要它。
//! - 工具名不是 just 名稱。
//! - 中途寫檔失敗沒有代碼（計畫 G4）。
//! - `uninstall` 收回根 `justfile` 的 `import` 與薄殼之後 `just vendor_kit` 就跑不起來；在那之後中斷，
//!   重跑的入口與診斷沒定（04：殘留與真正中斷的結果見訊息表，訊息表還沒有對應的碼）。
//! - 04:261 `remove` 後再 `add` 的重新詢問：`remove` 刪掉了該工具的逐檔紀錄，`add` 照既有檔處理。

pub mod text;

#[cfg(test)]
mod tests;

use std::collections::{BTreeMap, BTreeSet};
use std::ffi::OsStr;
use std::fs;
use std::io::{self, BufRead, Write};
use std::path::{Path, PathBuf};
use std::time::Duration;

use config::{Config, ConfigError};
use diagnostics::{Diagnostic, Diagnostics, Message, Sink};
use filelock::{Lock, Mode};
use layout::InstallDir;
use metadata::{Metadata, State};
use plan::{Channel, Field, Op, Outcome, Slot};
use progress::Progress;
use prompt::{Consent, PromptError, TtyState};
use retract::{Owner, Plan, Source, Verdict};
use runlog::Target;
use txn::{Disk, Entry, RecordFile, RepoFile, Txn};
use version_file::{LocalFile, LockFile};

/// `remove` 的進度檔 `<verb>`，也是它在進度檔裡自己的表名。
pub const REMOVE_VERB: &str = "remove";
/// `uninstall` 的進度檔 `<verb>`，也是它在進度檔裡自己的表名。
pub const UNINSTALL_VERB: &str = "uninstall";
/// 進度檔記這次收回哪些工具的欄位。
pub const REPOS_KEY: &str = "repos";
/// 進度檔記這次有沒有要寫 repo 檔的欄位。
pub const REPO_FILES_KEY: &str = "repo_files";

/// 這次執行的環境：容器內的路徑、終端狀態與輸出。
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
    /// stdin、stderr 是不是終端（啟動器傳進來的值）。
    pub tty: TtyState,
    /// `just vendor_kit` 之後的參數原樣（第一個是指令名）。
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

/// 跑一次 `remove <repo>`，回傳結束碼。
pub fn remove<W: Write, S: Sink, L: Write>(repo: &str, env: &mut Env<'_, W, S, L>) -> u8 {
    let mut run = Run::new(env);
    let _ = run.remove(repo);
    run.code
}

/// 跑一次 `uninstall`，回傳結束碼。
pub fn uninstall<W: Write, S: Sink, L: Write>(env: &mut Env<'_, W, S, L>) -> u8 {
    let mut run = Run::new(env);
    let _ = run.uninstall();
    run.code
}

/// 診斷已印、這次執行停下。
struct Stop;

type Step<T> = Result<T, Stop>;

/// 一份可以併進這次的殘留進度檔。
struct Residual {
    entry: progress::Entry,
    repos: Vec<String>,
}

/// 版本鎖定行怎麼處理。
enum LockAction<'l> {
    /// 不動（殘留的 `remove` 已經拿掉了）。
    Keep,
    /// 寫回已拿掉工具的版本鎖定行。
    Write(&'l mut LockFile),
    /// 整份刪掉 `version.toml`（`uninstall`）。
    RemoveFile,
}

/// 一份逐檔紀錄檔與它屬於誰。
struct Record {
    owner: Owner,
    metadata: Metadata,
}

/// 開著本機覆寫的一個工具（對象以外）：正規化後的本機開發來源與它交付的 `<ns>`。
struct Local {
    dir: String,
    namespaces: Vec<String>,
}

struct Run<'r, 'a, W: Write, S: Sink, L: Write> {
    env: &'r mut Env<'a, W, S, L>,
    code: u8,
    /// 這次執行已用掉的 `stage-dir` slot 數。
    stages: u32,
    /// 對象以外開著覆寫的工具（模組說明「本機覆寫」）。
    local: BTreeMap<String, Local>,
}

impl<'r, 'a, W: Write, S: Sink, L: Write> Run<'r, 'a, W, S, L> {
    fn new(env: &'r mut Env<'a, W, S, L>) -> Self {
        Run {
            env,
            code: 0,
            stages: 0,
            local: BTreeMap::new(),
        }
    }
}

impl<W: Write, S: Sink, L: Write> Run<'_, '_, W, S, L> {
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

    /// `.vendor_kit/` 下的路徑換成相對於 `.vendor_kit/` 的寫法（`txn` 的紀錄檔與要刪的路徑）。
    fn vk_rel(&mut self, path: &Path) -> Step<PathBuf> {
        match path.strip_prefix(self.env.dir.vk_dir()) {
            Ok(p) => Ok(p.to_path_buf()),
            Err(_) => Err(self.internal(format!("{} is not under .vendor_kit", path.display()))),
        }
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

    // ---- 共同的前段 ----

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

    fn local(&mut self) -> Step<Option<LocalFile>> {
        match LocalFile::load_from(self.env.dir) {
            Ok(l) => Ok(l),
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

    /// 辨識殘留的進度檔：`accept` 裡的 verb 而且沒有要寫 repo 檔的，回傳讓這次併入；其他的每一份
    /// 都印出原因再停下。
    fn residuals(&mut self, accept: &[&str]) -> Step<Vec<Residual>> {
        let entries = match progress::find(self.env.dir) {
            Ok(e) => e,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let mut found = Vec::new();
        let mut blocked = Vec::new();
        for entry in entries {
            match self.residual(entry, accept) {
                Ok(r) => found.push(r),
                Err(d) => blocked.push(d),
            }
        }
        if blocked.is_empty() {
            return Ok(found);
        }
        for d in blocked {
            self.emit(d);
        }
        Err(Stop)
    }

    fn residual(&self, entry: progress::Entry, accept: &[&str]) -> Result<Residual, Diagnostic> {
        let loaded = match entry.load() {
            Ok(p) => p,
            Err(progress::Error::Parse {
                file,
                source: progress::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => return Err(self.too_new_diag(&file, &t)),
            Err(e) => return Err(self.failed_diag(&entry.path, e.message(), e.to_string())),
        };
        let shown = self.rel(&entry.path);
        if !accept.contains(&entry.verb.as_str()) {
            return Err(self.gap_diag(format_args!(
                "{} while the incomplete {} operation in {shown} remains",
                accept[0], entry.verb
            )));
        }
        let doc = loaded.document();
        let verb = entry.verb.as_str();
        let repos: Option<Vec<String>> = doc
            .get(&[verb, REPOS_KEY])
            .and_then(|i| i.as_array())
            .and_then(|a| a.iter().map(|v| v.as_str().map(str::to_owned)).collect());
        let repo_files = doc.get(&[verb, REPO_FILES_KEY]).and_then(|i| i.as_bool());
        let (Some(repos), Some(repo_files)) = (repos, repo_files) else {
            return Err(self.gap_diag(format_args!(
                "recovering {shown} without its [{verb}] fields"
            )));
        };
        if repo_files {
            return Err(self.gap_diag(format_args!("recovering {shown}, which writes repo files")));
        }
        Ok(Residual {
            entry,
            repos: repos_vec(repos),
        })
    }

    /// 讀一份逐檔紀錄檔；不在回 `None`。
    fn load_metadata(&mut self, path: &Path) -> Step<Option<Metadata>> {
        match fs::symlink_metadata(path) {
            Ok(_) => {}
            Err(e) if e.kind() == io::ErrorKind::NotFound => return Ok(None),
            Err(e) => return Err(self.internal(format!("{}: {e}", path.display()))),
        }
        match Metadata::load(path) {
            Ok(m) => Ok(Some(m)),
            Err(metadata::Error::TooNew { file, too_new }) => {
                let d = self.too_new_diag(&file, &too_new);
                Err(self.stop(d))
            }
            Err(e) => {
                let d = self.failed_diag(path, e.message(), e.to_string());
                Err(self.stop(d))
            }
        }
    }

    /// `retract` 判定；契約沒寫到的紀錄組合停下。
    fn plan(&mut self, records: &[Record]) -> Step<Plan> {
        let sources: Vec<Source<'_>> = records
            .iter()
            .map(|r| Source {
                owner: &r.owner,
                metadata: &r.metadata,
            })
            .collect();
        let root = self.env.dir.root().to_path_buf();
        let planned = retract::plan(&sources, |p| read_optional(&root.join(p)));
        let planned = planned.map_err(|e| self.internal(e.to_string()))?;
        if let Some(r) = planned
            .records
            .iter()
            .find(|r| matches!(r.verdict, Verdict::Gap(_)))
        {
            let what = format!(
                "retracting the {} record of {} with state {} ({:?})",
                r.owner, r.path, r.state, r.verdict
            );
            return Err(self.gap(what));
        }
        Ok(planned)
    }

    /// 一次問完；全部同意回 `true`，答否印未變更回 `false`，不能互動回 VK0002。
    fn ask(&mut self, plan: &Plan) -> Step<bool> {
        let questions: Vec<String> = plan.questions.iter().map(text::question).collect();
        let answers = prompt::ask_all(
            &questions,
            Consent::Ask,
            &self.env.tty,
            &mut *self.env.stdin,
            &mut *self.env.prompt,
        );
        match answers {
            Ok(a) if a.all_yes() => Ok(true),
            Ok(_) => {
                self.report_overrides();
                self.say(text::NO_CHANGES);
                Ok(false)
            }
            Err(PromptError::NotInteractive(_)) => {
                let mut words = vec!["just".to_owned(), "vendor_kit".to_owned()];
                words.extend(self.env.argv.iter().cloned());
                let d = Diagnostic::new(&messages::VK0002)
                    .arg("command_with_y", prompt::command_with_y(&words));
                Err(self.stop(d))
            }
            Err(e) => Err(self.internal(e.to_string())),
        }
    }

    fn progress(
        &mut self,
        verb: &str,
        repos: &BTreeSet<String>,
        repo_files: bool,
    ) -> Step<Progress> {
        let mut p = match Progress::new(verb, self.env.run_id, self.env.argv) {
            Ok(p) => p,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let list: toml_edit::Array = repos.iter().map(String::as_str).collect();
        let doc = p.document_mut();
        let set = doc
            .set(&[verb, REPOS_KEY], list)
            .and_then(|()| doc.set(&[verb, REPO_FILES_KEY], repo_files));
        set.map_err(|e| self.internal(e.to_string()))?;
        Ok(p)
    }

    /// 這次落地完成之後刪殘留的進度檔。
    fn delete_residuals(&mut self, residual: &[Residual]) -> Step<()> {
        for r in residual {
            if let Err(e) = progress::delete(self.env.dir, &r.entry.verb, &r.entry.id) {
                let d = self.failed_diag(&r.entry.path, e.message(), e.to_string());
                return Err(self.stop(d));
            }
        }
        Ok(())
    }

    /// 收回了哪些檔、保留哪些初始檔。
    /// 收回的檔與保留清單；回傳列過的保留路徑。
    fn report_files(&mut self, plan: &Plan) -> BTreeSet<String> {
        for e in &plan.edits {
            self.say(&text::retracted(&e.path));
        }
        let kept: BTreeSet<String> = plan
            .records
            .iter()
            .filter(|r| matches!(r.state, State::Managed | State::Appended))
            .map(|r| r.path.clone())
            .collect();
        for path in &kept {
            self.say(&text::kept(path));
        }
        kept
    }

    /// 只列不刪的每一行一則 VK0061（落地之後才印）。
    fn report_unretracted(&mut self, plan: &Plan) {
        for u in &plan.unretracted {
            let d = Diagnostic::new(u.message())
                .arg("file", u.path.as_str())
                .arg("text", u.text.as_str())
                .arg("line_numbers", text::line_numbers(&u.matches));
            self.emit(d);
        }
    }

    // ---- remove ----

    fn remove(&mut self, repo: &str) -> Step<()> {
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        let mut lockfile = self.lockfile()?;
        let local = self.local()?;
        let residual = self.residuals(&[REMOVE_VERB])?;

        let mut targets: BTreeSet<String> = residual
            .iter()
            .flat_map(|r| r.repos.iter().cloned())
            .collect();
        if lockfile.tool(repo).is_none() && !targets.contains(repo) {
            return Err(self.stop(Diagnostic::new(&messages::VK0046).arg("repo", repo)));
        }
        targets.insert(repo.to_owned());
        for t in &targets {
            if !fetch::is_namespace(t) {
                return Err(self.gap(format_args!("tool name {t:?} (not a just name)")));
            }
        }
        self.local = self.others_local(local.as_ref(), &targets, &lockfile)?;

        let mut records = Vec::new();
        for t in &targets {
            let path = self.tool_metadata(t)?;
            if let Some(metadata) = self.load_metadata(&path)? {
                records.push(Record {
                    owner: Owner::Tool(t.clone()),
                    metadata,
                });
            }
        }
        let plan = self.plan(&records)?;
        if !self.ask(&plan)? {
            return Ok(());
        }

        let mut writes = self.other_records(&targets, &lockfile, &plan)?;
        let lifted = self.lift_overrides(local, &targets, &mut writes)?;
        let mut removed = Vec::new();
        for t in &targets {
            match lockfile.remove_tool(t) {
                Ok(Some(image)) => removed.push((t.clone(), image)),
                Ok(None) => {}
                Err(e) => return Err(self.internal(e.to_string())),
            }
        }
        let entry_text = self.render_entry(&lockfile)?;
        let current = read_optional(&self.env.dir.gen_dir().join(txn::TOOLS_JUST));
        let current =
            current.map_err(|e| self.internal(format!("gen/{}: {e}", txn::TOOLS_JUST)))?;
        let entry = if current.as_deref() == Some(entry_text.as_bytes()) {
            Entry::Keep
        } else {
            Entry::Write(entry_text.as_bytes())
        };
        let mut removes: Vec<PathBuf> = Vec::new();
        for t in &targets {
            let cache = self.env.dir.tool_cache(t);
            let cache = cache.map_err(|e| self.internal(e.to_string()))?;
            removes.push(self.vk_rel(&cache)?);
            removes.push(self.vk_rel(&stamp::tool_file(self.env.dir, t))?);
            removes.push(Path::new("baseline").join(t));
            let meta = self.tool_metadata(t)?;
            removes.push(self.vk_rel(&meta)?);
        }

        let progress = self.progress(REMOVE_VERB, &targets, !plan.edits.is_empty())?;
        let lock = if removed.is_empty() {
            LockAction::Keep
        } else {
            LockAction::Write(&mut lockfile)
        };
        self.land(progress, &plan, entry, &writes, &removes, lock)?;
        self.delete_residuals(&residual)?;

        self.report_overrides();
        for (t, image) in &removed {
            let shown = image.to_string();
            self.say(&text::removed(t, &image.tag().to_string(), &shown));
        }
        for t in &targets {
            if !removed.iter().any(|(r, _)| r == t) {
                self.say(&text::recovered(t));
            }
        }
        for (t, dir) in &lifted {
            self.say(&text::lifted_override(t, dir));
            self.say(&text::kept_local_source(t, dir));
        }
        self.report_files(&plan);
        self.report_unretracted(&plan);
        Ok(())
    }

    /// 解除對象的覆寫紀錄（`version.local.toml` 裡 `<repo>` 那一行）：有要解除的才把新內容排進紀錄檔那一步，
    /// 本機開發來源不讀也不動。回傳解除了哪些覆寫與它們的來源。
    fn lift_overrides(
        &mut self,
        local: Option<LocalFile>,
        targets: &BTreeSet<String>,
        writes: &mut Vec<(PathBuf, Vec<u8>)>,
    ) -> Step<Vec<(String, String)>> {
        let Some(mut local) = local else {
            return Ok(Vec::new());
        };
        let mut lifted = Vec::new();
        for t in targets {
            match local.remove_tool(t) {
                Ok(Some(dir)) => lifted.push((t.clone(), dir)),
                Ok(None) => {}
                Err(e) => return Err(self.internal(e.to_string())),
            }
        }
        if lifted.is_empty() {
            return Ok(lifted);
        }
        let text = local.render(self.env.written_by);
        let text = text.map_err(|e| self.internal(e.to_string()))?;
        let local_toml = self.env.dir.version_local_toml();
        let path = self.vk_rel(&local_toml)?;
        writes.push((path, text.into_bytes()));
        Ok(lifted)
    }

    fn tool_metadata(&mut self, repo: &str) -> Step<PathBuf> {
        metadata::tool_path(self.env.dir, repo).map_err(|e| self.internal(e.to_string()))
    }

    /// 其他紀錄檔裡同一個路徑的紀錄（ADR-0003）：寫入前內容相符的紀錄跟著換成寫入後的 hash。
    fn other_records(
        &mut self,
        targets: &BTreeSet<String>,
        lockfile: &LockFile,
        plan: &Plan,
    ) -> Step<Vec<(PathBuf, Vec<u8>)>> {
        let mut out = Vec::new();
        if plan.edits.is_empty() {
            return Ok(out);
        }
        let mut paths = vec![metadata::vk_path(self.env.dir)];
        for other in lockfile.tools().keys().filter(|r| !targets.contains(*r)) {
            paths.push(self.tool_metadata(other)?);
        }
        for path in paths {
            let Some(mut m) = self.load_metadata(&path)? else {
                continue;
            };
            let mut changed = false;
            for e in &plan.edits {
                match m.record_write(&e.path, &e.before, &e.after) {
                    Ok(metadata::WriteOutcome::Updated) => changed = true,
                    Ok(_) => {}
                    Err(e) => return Err(self.internal(e.to_string())),
                }
            }
            if changed {
                let text = m.render(self.env.written_by);
                let text = text.map_err(|e| self.internal(e.to_string()))?;
                out.push((self.vk_rel(&path)?, text.into_bytes()));
            }
        }
        Ok(out)
    }

    /// 剩下的工具的入口檔：`<ns>` 讀各自的 `cache/<repo>/`；開著覆寫的用本機開發來源的 `<ns>`，那幾行
    /// 指向本機開發來源。
    fn render_entry(&mut self, lockfile: &LockFile) -> Step<String> {
        let mut all: Vec<(String, Vec<String>)> = Vec::new();
        for other in lockfile.tools().keys() {
            if let Some(l) = self.local.get(other) {
                all.push((other.clone(), l.namespaces.clone()));
                continue;
            }
            let cache = self.env.dir.tool_cache(other);
            let cache = cache.map_err(|e| self.internal(e.to_string()))?;
            match fetch::namespaces(&cache) {
                Ok(ns) => all.push((other.clone(), ns)),
                Err(e) => {
                    return Err(self.gap(format_args!(
                        "remove while the cache of installed tool {other} is unreadable ({e}); \
                         run just vendor_kit sync first"
                    )));
                }
            }
        }
        let tools: Vec<tools_just::Tool> = all
            .iter()
            .map(|(repo, namespaces)| tools_just::Tool { repo, namespaces })
            .collect();
        let dirs: BTreeMap<String, String> = self
            .local
            .iter()
            .map(|(r, l)| (r.clone(), l.dir.clone()))
            .collect();
        tools_just::render_with(&tools, &dirs).map_err(|e| self.internal(e.to_string()))
    }

    /// 對象以外的覆寫讀本機開發來源（模組說明「本機覆寫」）：讀不到的每一個都印 VK0052 再停下。對象的覆寫
    /// 只解除、不讀；對象以外的覆寫指到不在版本鎖定行的工具是缺口。
    fn others_local(
        &mut self,
        file: Option<&LocalFile>,
        targets: &BTreeSet<String>,
        lockfile: &LockFile,
    ) -> Step<BTreeMap<String, Local>> {
        let mut local = BTreeMap::new();
        let Some(file) = file else {
            return Ok(local);
        };
        let others: Vec<(String, String)> = file
            .tools()
            .iter()
            .filter(|(repo, _)| !targets.contains(*repo))
            .map(|(repo, source)| (repo.clone(), source.clone()))
            .collect();
        let orphans: Vec<&str> = others
            .iter()
            .filter(|(repo, _)| lockfile.tool(repo).is_none())
            .map(|(repo, _)| repo.as_str())
            .collect();
        if !orphans.is_empty() {
            return Err(self.gap(format_args!(
                "local overrides of {} without a lock version line (no reason code)",
                orphans.join(", ")
            )));
        }
        let mut blocked: Vec<Diagnostic> = Vec::new();
        for (repo, source) in &others {
            match self.local_source(repo, source)? {
                Ok(l) => {
                    local.insert(repo.clone(), l);
                }
                Err(d) => blocked.push(d),
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

    /// 一個工具的本機開發來源：讀不到回 `Ok(Err(VK0052))`；交付保留名是缺口（模組說明）。
    fn local_source(&mut self, repo: &str, source: &str) -> Step<Result<Local, Diagnostic>> {
        let unreadable = |reason: String| {
            Diagnostic::new(&messages::VK0052)
                .arg("target", repo)
                .arg("source", source)
                .arg("reason", reason)
                .arg("undev_command", format!("just vendor_kit undev {repo}"))
        };
        let dir = match fetch::local::normalize(OsStr::new(source), self.env.host_root) {
            Ok(d) => d,
            Err(p) => return Ok(Err(unreadable(p.reason()))),
        };
        let namespaces = match self.read_source(&dir, repo)? {
            Ok(ns) => ns,
            Err(p) => return Ok(Err(unreadable(p.reason()))),
        };
        if namespaces.iter().any(|n| n == fetch::RESERVED) {
            return Err(self.gap(format_args!(
                "remove while the local source of {repo} delivers the reserved namespace {} \
                 (no reason code)",
                fetch::RESERVED
            )));
        }
        Ok(Ok(Local {
            dir: dir.as_str().to_owned(),
            namespaces,
        }))
    }

    /// 讀本機開發來源交付的 `<ns>`（`fetch::local::check_dir`）：安裝目錄裡的直接讀；安裝目錄外的先請
    /// 啟動器 `stage-dir` 複製進 `in/<slot>`（session 目錄），再讀那份複本。往返本身失敗是 VK 的錯，停下。
    fn read_source(
        &mut self,
        source: &fetch::local::Source,
        repo: &str,
    ) -> Step<Result<Vec<String>, fetch::local::PathProblem>> {
        let Some(host) = source.host_path(self.env.host_root) else {
            return Ok(fetch::local::check_dir(
                self.env.dir.root(),
                source.as_str(),
                repo,
            ));
        };
        self.stages += 1;
        let name = format!("{}{}", fetch::local::STAGE_SLOT_PREFIX, self.stages);
        let Some(slot) = Slot::parse(&name) else {
            return Err(self.internal(format!("stage-dir slot {name} is not a valid slot")));
        };
        let field = match Field::new(host.into_bytes()) {
            Ok(f) => f,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let sent = self.env.channel.send(&Op::StageDir(field, slot));
        sent.map_err(|e| self.internal(e.to_string()))?;
        let reply = self.env.channel.receive(self.env.poll);
        let reply = reply.map_err(|e| self.internal(e.to_string()))?;
        match reply.outcome {
            Outcome::Ok => Ok(fetch::local::check_dir(
                &self.env.inbox.join(&name),
                ".",
                repo,
            )),
            Outcome::Failed(rc) => Ok(Err(fetch::local::copy_failed(rc))),
            Outcome::Runner(_) => Err(self.internal("stage-dir got a runner result")),
        }
    }

    /// 依收回順序落地。
    fn land(
        &mut self,
        progress: Progress,
        plan: &Plan,
        entry: Entry,
        writes: &[(PathBuf, Vec<u8>)],
        removes: &[PathBuf],
        lock: LockAction,
    ) -> Step<txn::Done> {
        let repo_files: Vec<RepoFile> = plan
            .edits
            .iter()
            .map(|e| RepoFile {
                path: Path::new(&e.path),
                contents: &e.after,
            })
            .collect();
        let record_files: Vec<RecordFile> = writes
            .iter()
            .map(|(path, contents)| RecordFile { path, contents })
            .collect();
        let removes: Vec<&Path> = removes.iter().map(PathBuf::as_path).collect();
        let result = {
            let mut fx = Disk::new(self.env.dir, self.env.log, self.env.written_by);
            Txn::begin(&mut fx, progress).and_then(|t| {
                let t = t
                    .retract_repo_files(&repo_files)?
                    .retract_tools_just(entry)?
                    .retract_records(&record_files, &removes)?;
                let t = match lock {
                    LockAction::Keep => t.keep_lock_line(),
                    LockAction::Write(lockfile) => t.write_lock_line(lockfile, Target::Tool)?,
                    LockAction::RemoveFile => t.remove_lock_file(Target::Engine)?,
                };
                t.complete()
            })
        };
        result.map_err(|f| self.internal(f.to_string()))
    }

    // ---- uninstall ----

    fn uninstall(&mut self) -> Step<()> {
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        let lockfile = self.lockfile()?;
        let local = self.local()?;
        let residual = self.residuals(&[UNINSTALL_VERB, REMOVE_VERB])?;

        let mut targets: BTreeSet<String> = lockfile.tools().keys().cloned().collect();
        targets.extend(residual.iter().flat_map(|r| r.repos.iter().cloned()));
        let records = self.all_records()?;
        let plan = self.plan(&records)?;
        if !self.ask(&plan)? {
            return Ok(());
        }

        let mut removes: Vec<PathBuf> = ["cache", "baseline", "gen"]
            .iter()
            .map(PathBuf::from)
            .collect();
        let local_toml = self.env.dir.version_local_toml();
        removes.push(self.vk_rel(&local_toml)?);
        removes.extend(layout::SHELL_FILES.iter().map(PathBuf::from));

        let progress = self.progress(UNINSTALL_VERB, &targets, !plan.edits.is_empty())?;
        self.land(
            progress,
            &plan,
            Entry::Remove,
            &[],
            &removes,
            LockAction::RemoveFile,
        )?;
        self.delete_residuals(&residual)?;

        let host_root = self.env.host_root;
        self.say(&text::uninstalled(host_root));
        let listed = self.report_files(&plan);
        if let Some(local) = &local {
            for (repo, dir) in local.tools() {
                self.say(&text::kept_local_source(repo, dir));
            }
        }
        self.report_left(&listed)?;
        self.report_unretracted(&plan);
        Ok(())
    }

    /// `baseline/` 下每一份逐檔紀錄：各工具的 `<repo>.toml`，與 `.vendor_kit.toml`。
    fn all_records(&mut self) -> Step<Vec<Record>> {
        let dir = self.env.dir.baseline_dir();
        let mut names: Vec<String> = Vec::new();
        match fs::read_dir(&dir) {
            Ok(entries) => {
                for entry in entries {
                    let entry =
                        entry.map_err(|e| self.internal(format!("{}: {e}", dir.display())))?;
                    let name = entry.file_name().to_string_lossy().into_owned();
                    let is_file = entry.file_type().map(|t| t.is_file()).unwrap_or(false);
                    if is_file && name.ends_with(".toml") {
                        names.push(name);
                    }
                }
            }
            Err(e) if e.kind() == io::ErrorKind::NotFound => {}
            Err(e) => return Err(self.internal(format!("{}: {e}", dir.display()))),
        }
        names.sort();
        let vk_name = metadata::vk_path(self.env.dir)
            .file_name()
            .map(|n| n.to_string_lossy().into_owned())
            .unwrap_or_default();
        let mut records = Vec::new();
        for name in names {
            let owner = if name == vk_name {
                Owner::Vk
            } else {
                match name.strip_suffix(".toml") {
                    Some(repo) if !repo.starts_with('.') => Owner::Tool(repo.to_owned()),
                    _ => {
                        let shown = self.rel(&dir.join(&name));
                        return Err(
                            self.gap(format_args!("uninstall with the record file {shown}"))
                        );
                    }
                }
            };
            if let Some(metadata) = self.load_metadata(&dir.join(&name))? {
                records.push(Record { owner, metadata });
            }
        }
        // 不屬於任何工具的紀錄排在最後，問題的順序跟著工具名。
        records.sort_by(|a, b| a.owner.cmp(&b.owner));
        Ok(records)
    }

    /// `.vendor_kit/` 裡還留著的每一項；保留清單已列過的（例如納管的 `config.toml`）不重複列。
    fn report_left(&mut self, listed: &BTreeSet<String>) -> Step<()> {
        let vk = self.env.dir.vk_dir();
        let entries =
            fs::read_dir(&vk).map_err(|e| self.internal(format!("{}: {e}", vk.display())))?;
        let mut left: Vec<String> = Vec::new();
        for entry in entries {
            let entry = entry.map_err(|e| self.internal(format!("{}: {e}", vk.display())))?;
            let mut shown = self.rel(&entry.path());
            if entry.file_type().map(|t| t.is_dir()).unwrap_or(false) {
                shown.push('/');
            }
            if !listed.contains(&shown) {
                left.push(shown);
            }
        }
        left.sort();
        for path in left {
            self.say(&text::kept(&path));
        }
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

fn repos_vec(repos: Vec<String>) -> Vec<String> {
    let mut repos = repos;
    repos.sort();
    repos.dedup();
    repos
}
