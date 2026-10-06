//! `test` 的完整安裝檢查（04 檢查 (test)、04 指令表 `test`）：檢查版本、快取與薄殼的一致性；`test <path>`
//! 通過檢查後跑使用者測試的部分在 [`user_test`]；`test dist` 檢查工具交付內容的部分在 [`dist`]。
//!
//! `test` 是唯讀 recipe：不準備或修復 `cache/`、`gen/`、進度檔，不寫追蹤檔；除執行紀錄外零寫入（04 檢查、
//! 02 不變量 4）。呼叫端（入口 `vendor_kit`）已解析好參數、判過安裝目錄（VK0028），並接好執行紀錄。
//! 不帶 path 時不送任何 docker 動作，所以不需要 `plan` 往返（`test <path>` 只送一個 `runner` op）。依序做：
//!
//! 1. 讀 `.vendor_kit/config.toml`（VK0059），在取鎖之前（04 設定）。
//! 2. 取安裝目錄的共享鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束（04 鎖與逾時「讀取持共享鎖」）。
//! 3. 逐項檢查，每一項都只讀；有任何一項不過就把每一項都印出來再停下（02 不變量 4：列出每個原因）：
//!    - 薄殼：以 `compat` 的介面版、本引擎版與隨 image 出貨的模板本文（呼叫端給，跟 `install`、`sync` 用的是
//!      同一份）產生這一版的薄殼，跑 `shell::Shell::check`；不符回 VK0006，`<files>` 逐檔標出是哪一種。
//!      模板沒有（image 沒出貨）或薄殼檔是 symlink、不是一般檔：VK0056。
//!    - 引擎與工具的版本鎖定行 `version.toml`：檔案版過高回 VK0008；不合正規形回 VK0056（過渡做法，見「缺口」）。
//!    - 本機覆寫 `version.local.toml`：檔案版過高回 VK0008；有任何覆寫（工具或引擎）就各回一條 VK0032
//!      （04 檢查：本機覆寫仍會擋下），`<undev_command>` 依對象印成 `just vendor_kit undev <repo>` 或
//!      `just vendor_kit undev --engine`。
//!    - 殘留的進度檔（04 成對與無害：唯讀 recipe 只偵測，不恢復、不刪）：見「殘留的進度檔」。
//!    - 版本鎖定行裡每個沒有覆寫的工具（見「快取的一致性」）：缺件或不一致回 VK0047，每個工具一條。
//!    - `gen/tools.just`：缺件或跟 `cache/` 不一致回 VK0047（見「快取的一致性」）。
//! 4. 全部通過：stdout 印一行通過（[`text::PASSED`]），回 0（有 VK0060 時回 1）。
//!
//! 沒有工具時照樣檢查薄殼、引擎的版本鎖定行、本機覆寫與殘留的進度檔（04 檢查：沒有工具也檢查薄殼與引擎）。
//!
//! # 快取的一致性
//!
//! `test` 不取件，只比對 `sync` 會對齊的東西；任何一項不一致的下一步都是 `just vendor_kit sync`（VK0047）。
//! 全新 checkout 還沒取件也算缺件（#372 N12：CI 先跑 `sync`）。每個工具：
//!
//! - 印記（`stamp::tool_file`）不在：缺件，`cache/<repo>/` 不在也一起列。
//! - 印記損壞、或印記的版本跟版本鎖定行不同（例如 `git pull` 換了鎖定行）：不一致。
//! - 印記的版本相同：以印記比對 `cache/<repo>/` 的檔案集合與逐檔指紋（#372 N87）；整個目錄不在、少檔、多檔、
//!   指紋不同都是不一致，`<files>` 逐檔列出。
//!
//! `gen/tools.just`：工具全都一致時，以 `tools_just::render` 依 `cache/` 交付的 `<ns>` 產生應有的內容，與現有
//! 內容逐位元組比對；有工具缺件時只看它在不在。沒有工具時應有內容是空的，檔不在也算一致（`install` 不寫
//! 這個檔，薄殼以 `import?` 引入）。有工具開著覆寫時入口檔指向本機開發來源，已由 VK0032 擋下，不比內容。
//!
//! # 殘留的進度檔
//!
//! 跟 engine/sync、engine/update 的判法一致（指令之間互不依賴，照抄）：
//!
//! - `add`：VK0004，`<repo>` 讀進度檔 `[add] repo`。
//! - 工具 `upgrade`：VK0041，`<repo>` 讀進度檔 `[upgrade] target`，`<original_command>` 由進度檔的 `command` 重組。
//! - 引擎 `upgrade`：VK0023，`<vY>` 填本引擎版（同 engine/shell_check，見「缺口」）。
//! - `undev`：VK0053，`<target>` 讀進度檔 `[undev] target`，`<undev_command>` 由進度檔的 `command` 重組。
//! - 其他可寫 recipe（`remove`、`install`、`uninstall`、`dev`、`prune` 等）：VK0054，`<operation>` 是進度檔的
//!   `<verb>`。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 通過時 stdout 的字句（[`text`]）。
//! - VK0047 的 `<target>`：工具填 `<repo>`；`gen/tools.just` 是全部工具共用的檔，填主機上的安裝目錄。
//!   `<files>` 寫成 `.vendor_kit/<相對路徑> (<哪一種>)`，以 `, ` 分隔（跟 VK0006 同一種寫法）。
//! - VK0032 的 `<target>`：工具填 `<repo>`，引擎填 [`ENGINE_TARGET`]（同 engine/dev）。
//! - `<original_command>`、`<undev_command>` 的重組從 engine/update 照抄（[`full_command`]）。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - `version.toml`、`version.local.toml` 不合正規形：訊息表還沒有代碼（草稿 [`DRAFT_NOT_CANONICAL`]，N76）。
//! - 本機覆寫指到不在版本鎖定行的工具：訊息表還沒有代碼（草稿 [`DRAFT_ORPHAN_OVERRIDE`]，N76）。
//! - 基準版落後（VK0014）：`metadata` 沒有記基準版是哪一版（等 N3、N52），判不出來；工具有 metadata 時停下
//!   （同 engine/sync）。目前 `add` 只在有初始檔時才寫 metadata，實際上碰不到。
//! - 殘留的引擎 `upgrade` 進度檔：`progress::upgrade` 還沒記引擎 upgrade 的目標版，VK0023 的 `<vY>` 暫填本引擎版。
//! - 殘留的 `sync` 進度檔：`sync` 不寫進度檔，正常的引擎不會留下（同 engine/sync）。
//! - 工具名不是合法的 just 名稱、兩個工具交付同一個 `<ns>`：沒有代碼。
//! - 訊息表 VK0047 的 situation 還寫著「全新 checkout 是否算缺件待確認」、只講缺件；04 檢查也還寫「待確認」。
//!   這裡照 #372 N12、N87 的結論（缺件或不一致都報 VK0047），契約文字另案更新。

pub mod dist;
pub mod text;
pub mod user_test;

#[cfg(test)]
mod tests;

use std::collections::BTreeMap;
use std::fs;
use std::io::{self, Write};
use std::path::Path;

use config::{Config, ConfigError};
use diagnostics::{Diagnostic, Diagnostics, Sink};
use filelock::{Lock, Mode};
use layout::InstallDir;
use shell::Shell;
use stamp::Stamp;
use version_file::{LocalFile, LockFile, Versions};

/// `add` 的進度檔 `<verb>` 與它記 `<repo>` 的表（engine/add 的 `VERB`、`PROGRESS_TABLE`；指令之間互不依賴，照抄）。
pub const ADD_VERB: &str = "add";
/// `undev` 的進度檔 `<verb>` 與它記 `<target>` 的鍵（engine/dev 的 `UNDEV_VERB`、`TARGET_KEY`；照抄）。
pub const UNDEV_VERB: &str = "undev";
pub const UNDEV_TARGET_KEY: &str = "target";
/// `upgrade` 的進度檔 `<verb>`（格式見 `progress::upgrade`）。
pub const UPGRADE_VERB: &str = progress::upgrade::VERB;
/// `sync` 的進度檔 `<verb>`：`sync` 不寫進度檔，見模組說明「缺口」。
pub const SYNC_VERB: &str = "sync";
/// VK0032 的 `<target>` 填引擎時用的名字（engine/dev 的 `ENGINE_TARGET`；照抄）。
pub const ENGINE_TARGET: &str = "vendor_kit";
/// `gen/` 下的入口檔名（engine/txn 的 `TOOLS_JUST`；照抄）。
pub const TOOLS_JUST: &str = "tools.just";
/// 重組指令時接在參數前面的字。
pub const COMMAND_PREFIX: [&str; 2] = ["just", "vendor_kit"];

/// 版本檔不合正規形的草稿碼（#372 B 清單；定案登錄前以 VK0056 停下，原因寫明草稿碼）。
pub const DRAFT_NOT_CANONICAL: &str = "reason code pending (draft VK0070, N76)";
/// 本機覆寫指到不存在的鎖定行的草稿碼。
pub const DRAFT_ORPHAN_OVERRIDE: &str = "reason code pending (draft VK0071, N76)";

/// 這次執行的環境：容器內的安裝目錄與輸出。`test` 不詢問，所以沒有 stdin；`test <path>` 的往返通道另外給
/// （[`user_test::Runner`]），不帶 path 時不送 docker 動作。
pub struct Env<'a, W: Write, S: Sink> {
    /// 容器內的安裝目錄（`plan::mount::ROOT`）。
    pub dir: &'a InstallDir,
    /// 主機上的安裝目錄，填 `<install_dir>`。
    pub host_root: &'a str,
    /// 主機上的執行紀錄路徑，填 VK0056 的 `<path>`。
    pub run_log: &'a str,
    /// 本引擎版：判薄殼時這一版薄殼標頭的引擎版，也填 VK0023 的 `<vY>`。
    pub written_by: &'a str,
    /// 隨 image 出貨的薄殼四檔模板本文，順序同 [`layout::SHELL_FILES`]；`None` 是這個引擎沒有。
    pub shell_templates: Option<&'a [Vec<u8>; layout::SHELL_FILES.len()]>,
    pub stdout: &'a mut dyn Write,
    pub diags: &'a mut Diagnostics<W, S>,
}

/// 跑一次安裝檢查，回傳結束碼。
pub fn run<W: Write, S: Sink>(env: &mut Env<'_, W, S>) -> u8 {
    let mut check = Check { env, code: 0 };
    if check.run().is_ok() {
        check.say(text::PASSED);
    }
    check.code
}

/// POSIX shell 引號：只含安全字元的字原樣留下；其他（含空字串）包單引號，`'` 換成 `'\''`
/// （engine/update 的 `shell_quote`；指令之間互不依賴，照抄）。
pub fn shell_quote(s: &str) -> String {
    let safe = |c: char| c.is_ascii_alphanumeric() || "_@%+=:,./-".contains(c);
    if !s.is_empty() && s.chars().all(safe) {
        return s.to_owned();
    }
    format!("'{}'", s.replace('\'', r"'\''"))
}

/// 由進度檔的 `command`（`just vendor_kit` 之後的參數）重組完整指令。
pub fn full_command<S: AsRef<str>>(command: &[S]) -> String {
    COMMAND_PREFIX
        .iter()
        .map(|w| (*w).to_owned())
        .chain(command.iter().map(|w| shell_quote(w.as_ref())))
        .collect::<Vec<_>>()
        .join(" ")
}

/// 診斷已印、這次執行停下。
struct Stop;

type Step<T> = Result<T, Stop>;

struct Check<'r, 'a, W: Write, S: Sink> {
    env: &'r mut Env<'a, W, S>,
    code: u8,
}

impl<W: Write, S: Sink> Check<'_, '_, W, S> {
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

    /// VK0008：檔案版過高。
    fn too_new_diag(&self, file: &Path, t: &schema::TooNew) -> Diagnostic {
        Diagnostic::new(&messages::VK0008)
            .arg("file", self.rel(file))
            .arg("N", t.found().to_string())
            .arg("M", t.max().to_string())
            .arg("written_by", t.written_by().unwrap_or("unknown"))
    }

    /// 版本檔讀不進來：檔案版過高是 VK0008，其他（語法、不合正規形）以 VK0056 帶草稿碼。
    fn version_file_diag(&self, e: &version_file::Error) -> Diagnostic {
        match e {
            version_file::Error::Parse {
                file,
                source: version_file::ParseError::Read(schema::ReadError::TooNew(t)),
            } => self.too_new_diag(file, t),
            version_file::Error::Parse { file, source } => self.internal_diag(format!(
                "{}: {source}; {DRAFT_NOT_CANONICAL}",
                self.rel(file)
            )),
            e => self.internal_diag(e.to_string()),
        }
    }

    /// 底層 crate 回的錯：有代碼就照代碼印（只有一個 `<file>` 占位符的 VK0013），否則當內部錯誤。
    fn failed_diag(
        &self,
        file: &Path,
        message: Option<&'static diagnostics::Message>,
        detail: String,
    ) -> Diagnostic {
        match message {
            Some(m) if m.code == messages::VK0013.code => Diagnostic::new(&messages::VK0013)
                .arg("file", self.rel(file))
                .arg("path", self.env.run_log),
            _ => self.internal_diag(detail),
        }
    }

    /// 容器內路徑換成相對於安裝目錄的寫法，填 `<file>`、`<files>`。
    fn rel(&self, path: &Path) -> String {
        path.strip_prefix(self.env.dir.root())
            .unwrap_or(path)
            .display()
            .to_string()
    }

    fn say(&mut self, line: &str) {
        let _ = writeln!(self.env.stdout, "{line}");
        let _ = self.env.stdout.flush();
    }

    // ---- 流程 ----

    fn run(&mut self) -> Step<()> {
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        self.inspect()
    }

    /// 逐項檢查（模組說明第 3 步）；呼叫端已讀好設定、持共享鎖。有任何一項不過就全部印出、回 `Err`。
    fn inspect(&mut self) -> Step<()> {
        let mut blocked: Vec<Diagnostic> = Vec::new();
        if let Some(d) = self.shell() {
            blocked.push(d);
        }
        let lockfile = match LockFile::load_from(self.env.dir) {
            Ok(Some(l)) => Some(l),
            Ok(None) => {
                blocked.push(self.internal_diag(".vendor_kit/version.toml does not exist"));
                None
            }
            Err(e) => {
                blocked.push(self.version_file_diag(&e));
                None
            }
        };
        let overridden = self.overrides(lockfile.as_ref(), &mut blocked);
        self.residuals(&mut blocked);
        if let Some(lockfile) = &lockfile {
            self.tools(lockfile, &overridden, &mut blocked);
        }

        if blocked.is_empty() {
            return Ok(());
        }
        for d in blocked {
            self.emit(d);
        }
        Err(Stop)
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
        match Lock::acquire(self.env.dir, Mode::Shared, config) {
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

    /// 薄殼：跟這一版的模板不符回 VK0006，判不了回 VK0056，一致回 `None`。
    fn shell(&self) -> Option<Diagnostic> {
        let Some(t) = self.env.shell_templates else {
            return Some(self.gap_diag(
                "test without the shell templates, which this engine image does not ship",
            ));
        };
        let bodies = [&t[0][..], &t[1][..], &t[2][..], &t[3][..]];
        let shell = match Shell::render(compat::THIS.current_protocol, self.env.written_by, bodies)
        {
            Ok(s) => s,
            Err(e) => return Some(self.internal_diag(e.to_string())),
        };
        let report = match shell.check(self.env.dir) {
            Ok(r) => r,
            Err(e) => return Some(self.internal_diag(e.to_string())),
        };
        let message = report.message()?;
        let files: Vec<String> = report
            .mismatches()
            .map(|f| text::file(&format!("{}/{}", layout::VK_DIR, f.name), f.status))
            .collect();
        Some(Diagnostic::new(message).arg("files", files.join(", ")))
    }

    /// 本機覆寫：每個覆寫一條 VK0032。回開著覆寫的工具。
    fn overrides(&self, lockfile: Option<&LockFile>, blocked: &mut Vec<Diagnostic>) -> Vec<String> {
        let file = match LocalFile::load_from(self.env.dir) {
            Ok(Some(f)) => f,
            Ok(None) => return Vec::new(),
            Err(e) => {
                blocked.push(self.version_file_diag(&e));
                return Vec::new();
            }
        };
        if let Some(lockfile) = lockfile
            && let Err(orphan) = Versions::new(lockfile, Some(&file))
        {
            blocked.push(self.internal_diag(format!("{orphan}; {DRAFT_ORPHAN_OVERRIDE}")));
        }
        if file.engine().is_some() {
            blocked.push(
                Diagnostic::new(&messages::VK0032)
                    .arg("target", ENGINE_TARGET)
                    .arg("undev_command", full_command(&["undev", "--engine"])),
            );
        }
        for repo in file.tools().keys() {
            blocked.push(
                Diagnostic::new(&messages::VK0032)
                    .arg("target", repo.as_str())
                    .arg("undev_command", full_command(&["undev", repo.as_str()])),
            );
        }
        file.tools().keys().cloned().collect()
    }

    /// 殘留的進度檔（模組說明「殘留的進度檔」）：只偵測，不恢復、不刪。
    fn residuals(&self, blocked: &mut Vec<Diagnostic>) {
        match progress::find(self.env.dir) {
            Ok(entries) => {
                for entry in entries {
                    blocked.push(self.residual(&entry));
                }
            }
            Err(e) => blocked.push(self.internal_diag(e.to_string())),
        }
    }

    fn residual(&self, entry: &progress::Entry) -> Diagnostic {
        let loaded = match entry.load() {
            Ok(p) => p,
            Err(progress::Error::Parse {
                file,
                source: progress::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => return self.too_new_diag(&file, &t),
            Err(e) => return self.failed_diag(&entry.path, e.message(), e.to_string()),
        };
        let field = |table: &str, key: &str| {
            loaded
                .document()
                .get(&[table, key])
                .and_then(|i| i.as_str())
                .map(str::to_owned)
        };
        let missing_field = |what: &str, table: &str, key: &str| {
            self.gap_diag(format_args!(
                "reporting the incomplete {what} in {} without its [{table}] {key} field",
                self.rel(&entry.path)
            ))
        };
        match entry.verb.as_str() {
            ADD_VERB => match field(ADD_VERB, "repo") {
                Some(repo) => Diagnostic::new(&messages::VK0004).arg("repo", repo),
                None => missing_field(ADD_VERB, ADD_VERB, "repo"),
            },
            UNDEV_VERB => match field(UNDEV_VERB, UNDEV_TARGET_KEY) {
                Some(target) => Diagnostic::new(&messages::VK0053)
                    .arg("target", target)
                    .arg("undev_command", full_command(loaded.command())),
                None => missing_field(UNDEV_VERB, UNDEV_VERB, UNDEV_TARGET_KEY),
            },
            UPGRADE_VERB => match progress::upgrade::field(&loaded, progress::upgrade::TARGET) {
                Some(progress::upgrade::ENGINE_TARGET) => Diagnostic::new(&messages::VK0023)
                    .arg("vY", self.env.written_by)
                    .arg("original_command", full_command(loaded.command())),
                Some(repo) => Diagnostic::new(&messages::VK0041)
                    .arg("repo", repo)
                    .arg("original_command", full_command(loaded.command())),
                None => missing_field(UPGRADE_VERB, UPGRADE_VERB, progress::upgrade::TARGET),
            },
            SYNC_VERB => self.gap_diag(format_args!(
                "test while {} remains; sync no longer writes progress files",
                self.rel(&entry.path)
            )),
            other => Diagnostic::new(&messages::VK0054)
                .arg("install_dir", self.env.host_root)
                .arg("operation", other)
                .arg("original_command", full_command(loaded.command())),
        }
    }

    /// 每個工具的快取與 `gen/tools.just`（模組說明「快取的一致性」）。
    fn tools(&self, lockfile: &LockFile, overridden: &[String], blocked: &mut Vec<Diagnostic>) {
        let mut namespaces: BTreeMap<&str, Vec<String>> = BTreeMap::new();
        let mut complete = overridden.is_empty();
        for (repo, locked) in lockfile.tools() {
            if !fetch::is_namespace(repo) {
                blocked.push(self.gap_diag(format_args!("tool name {repo:?} (not a just name)")));
                complete = false;
                continue;
            }
            match metadata::tool_path(self.env.dir, repo) {
                Ok(p) if p.exists() => blocked.push(self.gap_diag(format_args!(
                    "judging whether the baseline of {repo} is behind the lock version line \
                     (VK0014 waits for N3 and N52)"
                ))),
                Ok(_) => {}
                Err(e) => blocked.push(self.internal_diag(e.to_string())),
            }
            if overridden.iter().any(|r| r == repo) {
                continue;
            }
            match self.cache(repo, &locked.to_string()) {
                Ok(ns) => {
                    namespaces.insert(repo, ns);
                }
                Err(d) => {
                    blocked.push(d);
                    complete = false;
                }
            }
        }
        if let Some(d) = self.entry(lockfile, &namespaces, complete) {
            blocked.push(d);
        }
    }

    /// 一個工具的 `cache/<repo>/` 與印記：一致回交付的 `<ns>`，缺件或不一致回 VK0047（判不了回 VK0056）。
    fn cache(&self, repo: &str, version: &str) -> Result<Vec<String>, Diagnostic> {
        let cache = self
            .env
            .dir
            .tool_cache(repo)
            .map_err(|e| self.internal_diag(e.to_string()))?;
        let stamp_file = stamp::tool_file(self.env.dir, repo);
        let cache_exists = match fs::symlink_metadata(&cache) {
            Ok(_) => true,
            Err(e) if e.kind() == io::ErrorKind::NotFound => false,
            Err(e) => return Err(self.internal_diag(format!("{}: {e}", cache.display()))),
        };
        let cache_dir = format!("{}/", self.rel(&cache));
        let mut files: Vec<String> = Vec::new();
        match Stamp::load(&stamp_file) {
            Ok(None) => {
                files.push(text::file(&self.rel(&stamp_file), text::MISSING));
                if !cache_exists {
                    files.push(text::file(&cache_dir, text::MISSING));
                }
            }
            Err(stamp::Error::Corrupt { .. }) => {
                files.push(text::file(&self.rel(&stamp_file), text::CORRUPT));
            }
            Err(stamp::Error::TooNew { file, too_new }) => {
                return Err(self.too_new_diag(&file, &too_new));
            }
            Err(e) => return Err(self.internal_diag(e.to_string())),
            Ok(Some(s)) if s.version() != version => {
                files.push(text::file(&self.rel(&stamp_file), text::OTHER_VERSION));
            }
            Ok(Some(_)) if !cache_exists => {
                files.push(text::file(&cache_dir, text::MISSING));
            }
            Ok(Some(s)) => {
                let diff = s
                    .verify(&cache)
                    .map_err(|e| self.internal_diag(format!("cache of {repo}: {e}")))?;
                let under = |p: &String, kind: &str| text::file(&format!("{cache_dir}{p}"), kind);
                files.extend(diff.missing.iter().map(|p| under(p, text::MISSING)));
                files.extend(diff.extra.iter().map(|p| under(p, text::EXTRA)));
                files.extend(diff.changed.iter().map(|p| under(p, text::CHANGED)));
            }
        }
        if !files.is_empty() {
            return Err(self.cache_diag(repo, &files));
        }
        fetch::namespaces(&cache).map_err(|e| {
            self.internal_diag(format!(
                "cache of {repo} matches its stamp, but its tool content is invalid: {e}"
            ))
        })
    }

    /// VK0047：缺件或不一致，下一步是 `sync`。
    fn cache_diag(&self, target: &str, files: &[String]) -> Diagnostic {
        Diagnostic::new(&messages::VK0047)
            .arg("target", target)
            .arg("files", files.join(", "))
    }

    /// `gen/tools.just`：`complete`（每個工具都一致、沒有覆寫）時比內容，否則只看在不在。
    fn entry(
        &self,
        lockfile: &LockFile,
        namespaces: &BTreeMap<&str, Vec<String>>,
        complete: bool,
    ) -> Option<Diagnostic> {
        let path = self.env.dir.gen_dir().join(TOOLS_JUST);
        let shown = self.rel(&path);
        let current = match fs::read(&path) {
            Ok(b) => Some(b),
            Err(e) if e.kind() == io::ErrorKind::NotFound => None,
            Err(e) => return Some(self.internal_diag(format!("{shown}: {e}"))),
        };
        if !complete {
            return (current.is_none() && !lockfile.tools().is_empty()).then(|| {
                self.cache_diag(self.env.host_root, &[text::file(&shown, text::MISSING)])
            });
        }
        let tools: Vec<tools_just::Tool> = namespaces
            .iter()
            .map(|(repo, namespaces)| tools_just::Tool { repo, namespaces })
            .collect();
        let expected = match tools_just::render(&tools) {
            Ok(t) => t,
            Err(e @ tools_just::Error::Duplicate { .. }) => {
                return Some(
                    self.gap_diag(format_args!("test of tools whose namespaces collide ({e})")),
                );
            }
            Err(e) => return Some(self.internal_diag(e.to_string())),
        };
        let kind = match current {
            None if expected.is_empty() => return None,
            None => text::MISSING,
            Some(b) if b == expected.as_bytes() => return None,
            Some(_) => text::CHANGED,
        };
        Some(self.cache_diag(self.env.host_root, &[text::file(&shown, kind)]))
    }
}
