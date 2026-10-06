//! `update` 指令（04 指令表 `update`、`update <repo>`；04 update 節）：查已導入工具與引擎有沒有新版。
//!
//! `update` 是唯讀 recipe（GLOSSARY：不動追蹤檔、也不動進度檔）。04 成對與無害第 1 點「`update` 只查；
//! 真正換版本用 `upgrade`」、GLOSSARY「`update` 只查有沒有新版」、ADR-0004「`update` 不動追蹤檔、也不動
//! 進度檔」：取件、基準版合併、詢問與落地都屬 `upgrade <repo>`，不在這裡。
//!
//! 呼叫端（入口 `vendor_kit`）已解析好參數、判過安裝目錄（VK0028），並接好執行紀錄。這裡依序做：
//!
//! 1. 讀 `.vendor_kit/config.toml`（VK0059），在取鎖之前（04 設定）。
//! 2. 取安裝目錄的共享鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束：04 鎖與逾時「讀取持
//!    共享鎖」。
//! 3. 讀 `version.toml`（檔案版過高回 VK0008）。
//! 4. 查詢前先判，只讀、有任何一項不能做就把每一項都印出來再停下：
//!    - `version.local.toml` 檔案版過高：VK0008。
//!    - 殘留的進度檔（04 成對與無害：唯讀 recipe 只偵測，不恢復、不刪）：`add` 的回 VK0004；`undev` 的回
//!      VK0053，`<target>` 讀進度檔 `[undev]` 表的 `target`（engine/dev 寫的），`<undev_command>` 由進度檔
//!      的 `command` 重組；工具 `upgrade` 的回 VK0041，`<repo>` 讀進度檔 `[upgrade]` 表的 `target`（格式見
//!      `progress::upgrade`），`<original_command>` 由進度檔的 `command` 重組；引擎 `upgrade` 的見「缺口」；
//!      其他可寫 recipe（`remove`、`install`、
//!      `uninstall`、`dev` 等）回 VK0054，`<original_command>` 由進度檔的 `command` 重組、各參數依 POSIX
//!      shell 規則加引號。
//! 5. 判查詢對象：不帶工具參數是版本鎖定行裡的全部工具與引擎；`update <repo>` 只查那個工具，不在版本
//!    鎖定行回 VK0046（訊息表：先辨識未完成進度，再判斷對象不存在，所以排在第 4 步之後）。
//! 6. 查詢對象有本機覆寫時，stderr 印一行提醒、不加診斷前綴（04 本機覆寫、03 輸出）；仍照版本鎖定行查，
//!    覆寫來源失效也不擋（VK0052 不適用於 `update`）。
//! 7. 每個對象即時列 registry 的 tag、依 04 指定版本算最新版（[`imageref::Tag::latest`]），stdout 每個
//!    對象印一行 [`text::result_line`]。列 tag 還做不了，見「缺口」。
//!
//! 不送任何 docker 動作、不建進度檔、不經 `txn`。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 本機覆寫提醒的字句（[`text::override_notice`]）。
//! - `add` 的進度檔記 `<repo>` 的表（engine/add 的 `PROGRESS_TABLE`；指令之間互不依賴，照抄）。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - 列 tag：`<repo>` 對應到哪個 GHCR 路徑、列 tag 要 registry client（計畫 D8），`plan` 協定也沒有列 tag
//!   的 op。第 7 步一律以 VK0056 停下，stdout 不印結果行：`latest: none` 是查詢失敗的顯示值，不拿來表示
//!   還沒實作。所以 `--registry-token-file`（04：只有真的要查版本清單時才讀）這一版不讀，VK0001、VK0055、
//!   VK0058 也還碰不到。
//! - 殘留的引擎 `upgrade` 進度檔（`[upgrade] target` 是引擎）：VK0023 的 `<vY>` 要從進度檔讀，
//!   `upgrade --engine` 還沒實作、它的欄位沒定。
//! - 殘留的 `add` 進度檔沒有 `[add]` 的 `repo` 欄位；殘留的 `undev` 進度檔沒有 `[undev]` 的 `target` 欄位；
//!   殘留的 `upgrade` 進度檔沒有 `[upgrade]` 的 `target` 欄位。

pub mod text;

#[cfg(test)]
mod tests;

use std::io::Write;
use std::path::Path;

use config::{Config, ConfigError};
use diagnostics::{Diagnostic, Diagnostics, Sink};
use filelock::{Lock, Mode};
use imageref::Tag;
use layout::InstallDir;
use version_file::{LocalFile, LockFile};

/// `add` 的進度檔 `<verb>` 與它記 `<repo>` 的表（engine/add 的 `VERB`、`PROGRESS_TABLE`）。
pub const ADD_VERB: &str = "add";
/// `upgrade` 的進度檔 `<verb>`（`progress::upgrade`）。
pub const UPGRADE_VERB: &str = progress::upgrade::VERB;
/// `undev` 的進度檔 `<verb>` 與它記 `<target>` 的鍵（engine/dev 的 `UNDEV_VERB`、`TARGET_KEY`；指令之間互不
/// 依賴，照抄）。
pub const UNDEV_VERB: &str = "undev";
pub const UNDEV_TARGET_KEY: &str = "target";
/// 重組 `<original_command>` 時接在參數前面的字。
pub const COMMAND_PREFIX: [&str; 2] = ["just", "vendor_kit"];

/// 一次 `update` 的參數（`args::Command::Update`）。`--registry-token-file` 只在真的要查版本清單時才讀，
/// 列 tag 還沒做（見模組說明的缺口），所以這裡不收。
#[derive(Debug, Clone, Copy)]
pub struct Request<'a> {
    /// `update <repo>` 的 `<repo>`；不帶是查全部工具與引擎。
    pub repo: Option<&'a str>,
}

/// 這次執行的環境。`update` 不詢問、不寫檔，所以沒有 stdin、終端狀態與執行紀錄的寫入端。
pub struct Env<'a, W: Write, S: Sink> {
    /// 容器內的安裝目錄（`plan::mount::ROOT`）。
    pub dir: &'a InstallDir,
    /// 主機上的安裝目錄，填 `<install_dir>`。
    pub host_root: &'a str,
    /// 主機上的執行紀錄路徑，填 VK0056 的 `<path>`。
    pub run_log: &'a str,
    /// 結果行（04 update：stdout 只有結果行）。
    pub stdout: &'a mut dyn Write,
    /// 不加前綴的 stderr 行（本機覆寫提醒）。
    pub stderr: &'a mut dyn Write,
    pub diags: &'a mut Diagnostics<W, S>,
}

/// 跑一次 `update`，回傳結束碼。
pub fn run<W: Write, S: Sink>(req: &Request<'_>, env: &mut Env<'_, W, S>) -> u8 {
    let mut update = Update { env, code: 0 };
    let _ = update.run(req);
    update.code
}

/// POSIX shell 引號：只含安全字元的字原樣留下；其他（含空字串）包單引號，`'` 換成 `'\''`
/// （與 engine/prompt 的 VK0002 `<command_with_y>` 同一條規則）。
pub fn shell_quote(s: &str) -> String {
    let safe = |c: char| c.is_ascii_alphanumeric() || "_@%+=:,./-".contains(c);
    if !s.is_empty() && s.chars().all(safe) {
        return s.to_owned();
    }
    format!("'{}'", s.replace('\'', r"'\''"))
}

/// 由進度檔的 `command`（`just vendor_kit` 之後的參數）重組完整指令。
pub fn original_command<S: AsRef<str>>(command: &[S]) -> String {
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

/// 一個查詢對象：結果行的工具名欄、鎖定版本的 tag、本機覆寫來源。
struct Target {
    name: String,
    current: Tag,
    local: Option<String>,
}

struct Update<'r, 'a, W: Write, S: Sink> {
    env: &'r mut Env<'a, W, S>,
    code: u8,
}

impl<W: Write, S: Sink> Update<'_, '_, W, S> {
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
        message: Option<&'static messages::Message>,
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

    // ---- 流程 ----

    fn run(&mut self, req: &Request<'_>) -> Step<()> {
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        let lockfile = self.lockfile()?;
        let local = self.judge()?;
        let targets = self.targets(req, &lockfile, local.as_ref())?;

        for t in &targets {
            if let Some(source) = &t.local {
                let _ = writeln!(
                    self.env.stderr,
                    "{}",
                    text::override_notice(&t.name, source)
                );
            }
        }
        let _ = self.env.stderr.flush();

        // 第 7 步：列 tag 還做不了（模組說明的缺口）。
        let names: Vec<String> = targets
            .iter()
            .map(|t| format!("{} ({})", t.name, t.current))
            .collect();
        Err(self.gap(format_args!(
            "listing tags from the registry for update ({})",
            names.join(", ")
        )))
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

    /// 查詢前的判定（模組說明第 4 步）：只讀。有任何一項不能做就把每一項都印出來再停下。
    /// 回傳讀到的 `version.local.toml`。
    fn judge(&mut self) -> Step<Option<LocalFile>> {
        let mut blocked: Vec<Diagnostic> = Vec::new();

        let local = match LocalFile::load_from(self.env.dir) {
            Ok(local) => local,
            Err(version_file::Error::Parse {
                file,
                source: version_file::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => {
                blocked.push(self.too_new_diag(&file, &t));
                None
            }
            Err(e) => {
                blocked.push(self.internal_diag(e.to_string()));
                None
            }
        };

        match progress::find(self.env.dir) {
            Ok(entries) => {
                for entry in entries {
                    blocked.push(self.residual(&entry));
                }
            }
            Err(e) => blocked.push(self.internal_diag(e.to_string())),
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

    /// 一份殘留的進度檔要印的診斷：唯讀 recipe 只偵測，不恢復、不刪。
    fn residual(&self, entry: &progress::Entry) -> Diagnostic {
        let loaded = match entry.load() {
            Ok(p) => p,
            Err(progress::Error::Parse {
                file,
                source: progress::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => return self.too_new_diag(&file, &t),
            Err(e) => return self.failed_diag(&entry.path, e.message(), e.to_string()),
        };
        match entry.verb.as_str() {
            ADD_VERB => {
                let repo = loaded
                    .document()
                    .get(&[ADD_VERB, "repo"])
                    .and_then(|i| i.as_str())
                    .map(str::to_owned);
                match repo {
                    Some(repo) => Diagnostic::new(&messages::VK0004).arg("repo", repo),
                    None => self.gap_diag(format_args!(
                        "reporting the incomplete add in {} without its [add] repo field",
                        self.rel(&entry.path)
                    )),
                }
            }
            UNDEV_VERB => {
                let target = loaded
                    .document()
                    .get(&[UNDEV_VERB, UNDEV_TARGET_KEY])
                    .and_then(|i| i.as_str())
                    .map(str::to_owned);
                match target {
                    Some(target) => Diagnostic::new(&messages::VK0053)
                        .arg("target", target)
                        .arg("undev_command", original_command(loaded.command())),
                    None => self.gap_diag(format_args!(
                        "reporting the incomplete undev in {} without its [undev] {UNDEV_TARGET_KEY} field",
                        self.rel(&entry.path)
                    )),
                }
            }
            UPGRADE_VERB => match progress::upgrade::field(&loaded, progress::upgrade::TARGET) {
                Some(progress::upgrade::ENGINE_TARGET) => self.gap_diag(format_args!(
                    "reporting the incomplete engine upgrade in {}",
                    self.rel(&entry.path)
                )),
                Some(repo) => Diagnostic::new(&messages::VK0041)
                    .arg("repo", repo)
                    .arg("original_command", original_command(loaded.command())),
                None => self.gap_diag(format_args!(
                    "reporting the incomplete upgrade in {} without its [upgrade] target field",
                    self.rel(&entry.path)
                )),
            },
            other => Diagnostic::new(&messages::VK0054)
                .arg("install_dir", self.env.host_root)
                .arg("operation", other)
                .arg("original_command", original_command(loaded.command())),
        }
    }

    /// 這次的查詢對象（模組說明第 5 步）。
    fn targets(
        &mut self,
        req: &Request<'_>,
        lockfile: &LockFile,
        local: Option<&LocalFile>,
    ) -> Step<Vec<Target>> {
        let tool_local = |repo: &str| local.and_then(|l| l.tool(repo)).map(str::to_owned);
        if let Some(repo) = req.repo {
            let Some(locked) = lockfile.tool(repo) else {
                let d = Diagnostic::new(&messages::VK0046).arg("repo", repo);
                return Err(self.stop(d));
            };
            return Ok(vec![Target {
                name: repo.to_owned(),
                current: locked.tag(),
                local: tool_local(repo),
            }]);
        }
        let mut targets: Vec<Target> = lockfile
            .tools()
            .iter()
            .map(|(repo, locked)| Target {
                name: repo.clone(),
                current: locked.tag(),
                local: tool_local(repo),
            })
            .collect();
        targets.push(Target {
            name: text::ENGINE_NAME.to_owned(),
            current: lockfile.engine().tag(),
            local: local.and_then(LocalFile::engine).map(str::to_owned),
        });
        Ok(targets)
    }
}
