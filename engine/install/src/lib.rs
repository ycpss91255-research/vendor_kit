//! `install` 指令（04 指令表 `install`、首次導入還是既有安裝目錄、寫入既有檔的例外、成對與無害；
//! 03 輸出）：從參數到落地。`install` 寫的每一樣東西都要讓 `uninstall`（`engine/remove`）收得回去。
//!
//! 呼叫端（入口 `vendor_kit`）已解析好參數、判過安裝目錄（VK0028），並接好執行紀錄。首次導入時
//! 啟動器在起引擎之前已建好 `.vendor_kit/log/` 與這次的紀錄（04 bootstrap 第 4 步），所以引擎看到的
//! `.vendor_kit/` 一定已在；首次導入與既有安裝目錄的差別只看 `version.toml` 在不在。
//!
//! `install` 屬救援路徑（ADR-0007:37、ADR-0008），只准用 `plan::RESCUE_OPS` 的協定動作；這一版完全不碰
//! docker，不送任何 request。
//!
//! # 順序
//!
//! 1. 讀 `.vendor_kit/config.toml`（VK0059），在第一次取鎖之前（04 設定）。
//! 2. 取安裝目錄的排他鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束。
//! 3. 讀 `version.toml` 與 `version.local.toml`（檔案版過高回 VK0008）；`version.toml` 不在就是首次導入，
//!    在就沿用它的引擎版本鎖定行（不換引擎版，換版走 `upgrade --engine`）。
//! 4. 辨識殘留的進度檔（見「恢復」）。
//! 5. 出貨輸入（[`Release`]，薄殼模板從 image 裡的 [`release::SHIPPED_DIR`] 讀）缺哪一項就以 VK0056 停下，
//!    列出缺的項目。首次導入時另讀啟動器放在 `in/` 的
//!    引擎引用檔（[`release::engine_from`]）：不在、不是 pinned 引用、repo 不是 [`release::ENGINE_REPO`]、
//!    tag 不是本引擎版，都以 VK0056 停下並寫明哪裡不一致；既有安裝目錄不讀它。
//! 6. 算這次要寫的東西，只讀不寫：
//!    - `version.toml`：首次導入時只有引擎版本鎖定行。
//!    - 薄殼四檔（`shell`）：以 `compat` 的介面版、本引擎版與模板本文產生，跟現有的逐檔比對，只寫不一致的
//!      （缺檔、被改過、不是這一版的模板）。symlink 或不是一般檔時停下（`shell` 第一版禁止 symlink）。
//!    - 根 `justfile` 的 `import` 行與根 `.dockerignore` 的行：`baseline/.vendor_kit.toml` 已有那個檔的
//!      紀錄就不動；沒有紀錄時以 `initfiles` 的 append 規則判（`add` 用的同一套）：檔在就先問再 append，
//!      檔不在就新建（根 `justfile` 附 `default`）。
//!    - `.vendor_kit/config.toml`：`baseline/.vendor_kit.toml` 已有它的紀錄就不動（換版與合併歸 `upgrade`，
//!      04 使用者的檔與 VK 的檔）；沒有紀錄、檔也不在時，照隨引擎出貨的模板（[`release::CONFIG_TEMPLATE`]）
//!      新建，不問（04 寫入既有檔的例外：目標不存在就新建），並記基準版。路徑上已有東西（含 symlink）就不碰。
//!    - `baseline/.vendor_kit.toml`：根目錄兩個檔的 `appended` 紀錄（插入的行、寫入後的整檔 hash）與
//!      `config.toml` 的 `managed` 紀錄（寫入後的整檔 hash）；其他工具的紀錄檔有同一個檔、寫入前相符的
//!      紀錄，跟著換成寫入後的 hash（ADR-0003）。
//!    - `config.toml` 的基準版副本 `baseline/.vendor_kit/config.toml`（[`layout::InstallDir::config_baseline`]）。
//!    - `gen/.stamp`：產生薄殼的引擎 ref（見「這次自訂的內部細節」），跟現有內容不同才寫。
//! 7. 什麼都不用寫、也沒有殘留的進度檔：stdout 說明未變更，不建進度檔（04 成對與無害）。
//! 8. `prompt` 一次問完（04 共同選項：全部同意才寫入，含恢復舊操作）：只有 append 進使用者既有檔才問；
//!    `-y` 全部同意。答否是正常取消（stdout 說明未變更，以 0 結束）；不能互動回 VK0002，除執行紀錄外
//!    不寫任何檔。
//! 9. 經 `txn` 落地：建進度檔 → repo 檔（根 `justfile`、`.dockerignore`、`.vendor_kit/config.toml`）→
//!    `.vendor_kit/` 下的檔（薄殼、`config.toml` 的基準版副本、`baseline/` 的紀錄、`gen/.stamp`）→
//!    寫引擎版本鎖定行（只有首次導入）→ 刪進度檔；之後才刪殘留的進度檔。
//!    `cache/` 與 `gen/tools.just` 不動。
//! 10. stdout 列出改了什麼。
//!
//! # 恢復
//!
//! 殘留的 `install` 進度檔表示上一次中途停了。`install` 只把安裝目錄對齊這一版，判定時看的是目前的檔，
//! 所以恢復就是照常再做一次：寫到一半的薄殼會被判成不一致而重寫，沒寫的版本鎖定行照樣補上。
//! 根目錄檔與 `config.toml` 另看殘留的進度檔記的寫入後整檔 hash：目前的檔與它相同，表示那次已經寫進去、
//! 只差紀錄，直接補上紀錄（根目錄檔記 `appended`，`config.toml` 記 `managed` 並補存基準版副本；ADR-0003 以
//! 整檔 hash 認定是 VK 寫的）；還沒寫的照常判定，寫了之後又被改過的 `config.toml` 當成已有、沒有紀錄的檔。
//! 基準版副本排在紀錄之前寫，斷在兩者之間時沒有紀錄，下次照上面補上。
//! 殘留的詢問與這次的一起問完、全部同意才寫，答否時殘留的進度檔照留。這次落地完成之後才刪殘留的那幾份。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 進度檔 `.tmp.install.<run-id>.toml` 另記 `[install]` 表的 `repo_files`（這次有沒有要寫 repo 檔）
//!   與 `files`（每個要寫的 repo 檔：`path`、`lines`、寫入後的 `hash`；`config.toml` 的 `lines` 是空的）。
//! - 根目錄檔的紀錄都記成 `appended`，`lines` 是 VK 寫進去的行：新建的根 `justfile` 只記 `import` 那一行
//!   （`default` 建立後按 repo 檔處理，04），新建的 `.dockerignore` 記全部的行。`uninstall` 照 04 收回
//!   這些行，檔本身不刪。
//! - 薄殼標頭的引擎版寫本引擎的版本（`v<X.Y.Z>`，與 `written_by` 相同）。
//! - `config.toml` 的紀錄 `path` 是 repo 相對路徑 `.vendor_kit/config.toml`，跟其他 `[[file]]` 紀錄同一個格式
//!   （`managed`、`hash`，跟 `initfiles` 新建整份初始檔的紀錄相同）；基準版副本照工具的
//!   `baseline/<repo>/<路徑>` 擺法放在 `baseline/` 下同一個相對路徑（N97）。模板的逐字內容 04 的草稿之後照
//!   [`release::CONFIG_TEMPLATE`] 寫。stdout 的「新建」那一行同根目錄檔。`uninstall` 保留 `config.toml`、
//!   連同 `baseline/` 刪掉副本。
//! - `gen/.stamp`（ADR-0007：只記產生薄殼的引擎 ref，供快路徑比對）：一行、LF 結尾，值是這次的引擎版本
//!   鎖定行的值（首次導入是啟動器給的引擎引用，既有安裝目錄沿用 `version.toml` 的那一行）。`gen/` 不進 git，
//!   新 checkout 沒有它，`install` 照常補上；stdout 不另列這一檔。`uninstall` 連同 `gen/` 一起刪。
//! - stdout 的字句與詢問文字（英文）見 [`text`]。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - 殘留的進度檔不是 `install` 的，或殘留的 `install` 要寫 repo 檔卻沒有 `files`。
//! - 殘留的 `install` 記過的根目錄檔，目前的整檔 hash 跟那次寫入後的不同、卻已含要插入的行（寫入後
//!   使用者又改過，分不出是誰插的）：照下一條停下。
//! - 根目錄檔沒有紀錄、卻已含有要插入的行（`initfiles` 的 `LinesAlreadyPresent`，04 只說未收回的內容
//!   不得無條件再 append），以及 `initfiles` 判出的其他缺口。
//! - 中途寫檔失敗沒有代碼（計畫 G4）。
//! - `config.toml` 已在、卻沒有紀錄（使用者在 `install` 之前自己建的，或寫了之後改過才補跑）：04 沒說要不要
//!   記成未納管。這一條不停下（檔是使用者的，不寫也不違反 04）：不碰、不記，之後的換版與合併（`upgrade`）
//!   照沒有紀錄處理。
//! - 巢狀安裝（VK0029）與「在 git repo 內」要看安裝目錄以外的路徑，引擎只看得到掛進來的安裝目錄，
//!   由啟動器在起引擎前判（flow-bootstrap），不在這裡。

pub mod release;
pub mod text;

#[cfg(test)]
mod tests;

use std::fs;
use std::io::{self, BufRead, Write};
use std::path::{Path, PathBuf};

use config::{Config, ConfigError};
use diagnostics::{Diagnostic, Diagnostics, Message, Sink};
use filelock::{Lock, Mode};
use imageref::ImageRef;
use initfiles::{Gap, InitFile, Strategy, Verdict};
use layout::InstallDir;
use metadata::{FileHash, FileRecord, Metadata, State};
use progress::Progress;
use prompt::{Consent, PromptError, TtyState};
use runlog::Target;
use shell::Shell;
use txn::{Disk, RecordFile, RepoFile, Txn};
use version_file::{LocalFile, LockFile};

pub use release::Release;

/// `install` 的進度檔 `<verb>`，也是它在進度檔裡自己的表名。
pub const INSTALL_VERB: &str = "install";
/// 進度檔記這次有沒有要寫 repo 檔的欄位。
pub const REPO_FILES_KEY: &str = "repo_files";
/// 進度檔記這次要寫的每個 repo 檔的欄位：inline table 的陣列，每個有 [`PATH_KEY`]、[`LINES_KEY`]、
/// [`HASH_KEY`]。
pub const FILES_KEY: &str = "files";
/// repo 相對路徑。
pub const PATH_KEY: &str = "path";
/// VK 寫進去的行。
pub const LINES_KEY: &str = "lines";
/// 寫入後的整檔 hash（`metadata::FileHash`）。
pub const HASH_KEY: &str = "hash";
/// 根 `justfile`。
pub const JUSTFILE: &str = "justfile";
/// 根 `.dockerignore`。
pub const DOCKERIGNORE: &str = ".dockerignore";
/// `.vendor_kit/config.toml` 的 repo 相對路徑（`baseline/.vendor_kit.toml` 裡紀錄的 `path`）。
pub const CONFIG_TOML: &str = ".vendor_kit/config.toml";

/// 這次執行的環境：容器內的路徑、終端狀態與輸出。
pub struct Env<'a, W: Write, S: Sink, L: Write> {
    /// 容器內的安裝目錄（`plan::mount::ROOT`）。
    pub dir: &'a InstallDir,
    /// 容器內的收件目錄（`plan::mount::IN`）：首次導入時讀其中的引擎引用檔。
    pub inbox: &'a Path,
    /// 主機上的安裝目錄，填 `<install_dir>`。
    pub host_root: &'a str,
    /// 主機上的執行紀錄路徑，填 VK0056 的 `<path>`。
    pub run_log: &'a str,
    /// stdin、stderr 是不是終端（啟動器傳進來的值）。
    pub tty: TtyState,
    /// `just vendor_kit` 之後的參數原樣（第一個是指令名）。
    pub argv: &'a [String],
    /// 這次執行的 run-id，也是進度檔的 `<id>`。
    pub run_id: &'a str,
    /// 蓋在 VK 檔上的寫入者，也是薄殼標頭的引擎版。
    pub written_by: &'a str,
    pub stdin: &'a mut dyn BufRead,
    pub stdout: &'a mut dyn Write,
    /// 詢問文字（印到 stderr）。
    pub prompt: &'a mut dyn Write,
    pub diags: &'a mut Diagnostics<W, S>,
    /// 執行紀錄（`txn` 寫里程碑事件）。
    pub log: &'a mut runlog::Writer<L>,
}

/// 這次的參數與出貨輸入。
pub struct Request<'a> {
    /// 帶了 `-y`。
    pub yes: bool,
    pub release: &'a Release,
}

/// 跑一次 `install`，回傳結束碼。
pub fn run<W: Write, S: Sink, L: Write>(req: &Request<'_>, env: &mut Env<'_, W, S, L>) -> u8 {
    let mut run = Run { env, code: 0 };
    let _ = run.install(req);
    run.code
}

/// 診斷已印、這次執行停下。
struct Stop;

type Step<T> = Result<T, Stop>;

/// 這次要寫的一個 repo 檔：根目錄檔，或新建的 `.vendor_kit/config.toml`。
struct RootEdit {
    path: &'static str,
    /// 寫入前的內容；新建時是 `None`。
    before: Option<Vec<u8>>,
    after: Vec<u8>,
    /// 要先問（append 進既有檔）。
    ask: bool,
    /// VK 寫進去的行；`config.toml` 是整份新建的，沒有行。
    lines: Vec<String>,
}

/// 殘留的進度檔記的一個 repo 檔：那次要寫進去的行與寫入後的整檔 hash。
#[derive(Debug, Clone, PartialEq, Eq)]
struct Written {
    path: String,
    lines: Vec<String>,
    hash: FileHash,
}

/// 一份可以併進這次的殘留進度檔。
struct Residual {
    entry: progress::Entry,
    files: Vec<Written>,
}

/// 出貨輸入都齊了之後的借用。
struct Inputs<'r> {
    /// 首次導入時寫的引擎版本鎖定行；既有安裝目錄是 `None`。
    engine: Option<ImageRef>,
    shell: [&'r [u8]; layout::SHELL_FILES.len()],
    import: &'r str,
    default: &'r str,
    dockerignore: &'r [String],
    config: &'r str,
}

struct Run<'r, 'a, W: Write, S: Sink, L: Write> {
    env: &'r mut Env<'a, W, S, L>,
    code: u8,
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

    /// `.vendor_kit/` 下的路徑換成相對於 `.vendor_kit/` 的寫法（`txn` 的紀錄檔）。
    fn vk_rel(&mut self, path: &Path) -> Step<PathBuf> {
        match path.strip_prefix(self.env.dir.vk_dir()) {
            Ok(p) => Ok(p.to_path_buf()),
            Err(_) => Err(self.internal(format!("{} is not under .vendor_kit", path.display()))),
        }
    }

    fn say(&mut self, line: &str) {
        let _ = writeln!(self.env.stdout, "{line}");
    }

    // ---- 前段 ----

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

    fn lockfile(&mut self) -> Step<Option<LockFile>> {
        match LockFile::load_from(self.env.dir) {
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

    fn local(&mut self) -> Step<()> {
        match LocalFile::load_from(self.env.dir) {
            Ok(_) => Ok(()),
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

    /// 辨識殘留的進度檔：`install` 的而且欄位齊全的，回傳讓這次併入；其他的每一份都印出原因再停下。
    fn residuals(&mut self) -> Step<Vec<Residual>> {
        let entries = match progress::find(self.env.dir) {
            Ok(e) => e,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let mut found = Vec::new();
        let mut blocked = Vec::new();
        for entry in entries {
            match self.residual(&entry) {
                Ok(files) => found.push(Residual { entry, files }),
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

    fn residual(&self, entry: &progress::Entry) -> Result<Vec<Written>, Diagnostic> {
        let loaded = match entry.load() {
            Ok(p) => p,
            Err(progress::Error::Parse {
                file,
                source: progress::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => return Err(self.too_new_diag(&file, &t)),
            Err(e) => return Err(self.failed_diag(&entry.path, e.message(), e.to_string())),
        };
        let shown = self.rel(&entry.path);
        if entry.verb != INSTALL_VERB {
            return Err(self.gap_diag(format_args!(
                "install while the incomplete {} operation in {shown} remains",
                entry.verb
            )));
        }
        let doc = loaded.document();
        let repo_files = doc
            .get(&[INSTALL_VERB, REPO_FILES_KEY])
            .and_then(|i| i.as_bool());
        let files = doc
            .get(&[INSTALL_VERB, FILES_KEY])
            .and_then(|i| i.as_array())
            .and_then(|a| a.iter().map(written).collect::<Option<Vec<_>>>());
        match (repo_files, files) {
            (Some(false), _) => Ok(Vec::new()),
            (Some(true), Some(files)) if !files.is_empty() => Ok(files),
            _ => Err(self.gap_diag(format_args!(
                "recovering {shown} without its [{INSTALL_VERB}] fields"
            ))),
        }
    }

    /// 出貨輸入都齊了才繼續，缺的項目一起列在一則 VK0056；`need_engine`（首次導入）時再讀引擎引用檔。
    fn inputs<'r>(&mut self, release: &'r Release, need_engine: bool) -> Step<Inputs<'r>> {
        let Some(shell) = release.shell.as_ref() else {
            return Err(self.gap(format_args!(
                "install without {}, which this engine image does not ship",
                release.missing().join(", ")
            )));
        };
        let engine = if need_engine {
            match release::engine_from(self.env.inbox, self.env.written_by) {
                Ok(e) => Some(e),
                Err(reason) => return Err(self.internal(reason)),
            }
        } else {
            None
        };
        Ok(Inputs {
            engine,
            shell: [&shell[0], &shell[1], &shell[2], &shell[3]],
            import: &release.justfile_import,
            default: &release.justfile_default,
            dockerignore: &release.dockerignore,
            config: &release.config,
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

    // ---- install ----

    fn install(&mut self, req: &Request<'_>) -> Step<()> {
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        let existing = self.lockfile()?;
        self.local()?;
        let residual = self.residuals()?;
        let inputs = self.inputs(req.release, existing.is_none())?;

        let mut new_lock = match (&existing, &inputs.engine) {
            (Some(_), _) => None,
            (None, Some(engine)) => Some(LockFile::new(engine)),
            (None, None) => return Err(self.internal("no engine lock line value")),
        };

        // 薄殼四檔：只寫不一致的。
        let shell = Shell::render(
            compat::THIS.current_protocol,
            self.env.written_by,
            inputs.shell,
        );
        let shell = shell.map_err(|e| self.internal(e.to_string()))?;
        let report = shell.check(self.env.dir);
        let report = report.map_err(|e| self.internal(e.to_string()))?;
        // 順序同 `layout::SHELL_FILES`。
        let shell_names: Vec<&'static str> = report.mismatches().map(|f| f.name).collect();

        // `gen/.stamp`：產生薄殼的引擎 ref（ADR-0007 內部機制），跟現有內容不同才寫。
        let engine_ref = match (&existing, &inputs.engine) {
            (Some(lock), _) => lock.engine().to_string(),
            (None, Some(engine)) => engine.to_string(),
            (None, None) => return Err(self.internal("no engine lock line value")),
        };
        let stamp = format!("{engine_ref}\n").into_bytes();
        let stamp_path = self.env.dir.stamp();
        let current = read_optional(&stamp_path);
        let current =
            current.map_err(|e| self.internal(format!("{}: {e}", self.rel(&stamp_path))))?;
        let stamp_changed = current.as_deref() != Some(stamp.as_slice());

        // 根目錄檔與 `baseline/.vendor_kit.toml`。
        let vk_path = metadata::vk_path(self.env.dir);
        let mut vk_md = self.load_metadata(&vk_path)?.unwrap_or_default();
        let mut edits: Vec<RootEdit> = Vec::new();
        let mut adopted: Vec<&'static str> = Vec::new();
        let import = vec![inputs.import.to_owned()];
        let wanted: [(&'static str, &[String], Option<&str>); 2] = [
            (JUSTFILE, &import, Some(inputs.default)),
            (DOCKERIGNORE, inputs.dockerignore, None),
        ];
        for (path, lines, extra) in wanted {
            if vk_md.get(path).is_some() {
                continue;
            }
            if let Some(record) = self.adopt(path, &residual)? {
                vk_md
                    .put(record)
                    .map_err(|e| self.internal(e.to_string()))?;
                adopted.push(path);
                continue;
            }
            let (edit, record) = self.root_file(path, lines, extra, &vk_md)?;
            vk_md
                .put(record)
                .map_err(|e| self.internal(e.to_string()))?;
            edits.push(edit);
        }

        // `.vendor_kit/config.toml`：沒有紀錄才考慮；殘留的進度檔記過、而且內容還是那次寫的，補上紀錄；
        // 檔不在就照模板新建。兩種都記 `managed` 並存基準版副本。
        let mut config_baseline = false;
        if vk_md.get(CONFIG_TOML).is_none() {
            if let Some(record) = self.adopt(CONFIG_TOML, &residual)? {
                vk_md
                    .put(record)
                    .map_err(|e| self.internal(e.to_string()))?;
                adopted.push(CONFIG_TOML);
                config_baseline = true;
            } else if let Some((edit, record)) = self.config_file(inputs.config)? {
                vk_md
                    .put(record)
                    .map_err(|e| self.internal(e.to_string()))?;
                edits.push(edit);
                config_baseline = true;
            }
        }

        if shell_names.is_empty()
            && !stamp_changed
            && edits.is_empty()
            && new_lock.is_none()
            && residual.is_empty()
        {
            let host_root = self.env.host_root;
            self.say(&text::unchanged(host_root));
            return Ok(());
        }

        let questions: Vec<String> = edits
            .iter()
            .filter(|e| e.ask)
            .map(|e| text::question(e.path, e.lines.len()))
            .collect();
        if !self.ask(&questions, req.yes)? {
            return Ok(());
        }

        // `.vendor_kit/` 下要寫的檔：薄殼、這次的紀錄、其他工具跟著換 hash 的紀錄，最後是 `gen/.stamp`。
        let mut records: Vec<(PathBuf, Vec<u8>)> = shell_names
            .iter()
            .filter_map(|n| shell.file(n).map(|c| (PathBuf::from(n), c.to_vec())))
            .collect();
        if !edits.is_empty() || !adopted.is_empty() {
            // 基準版副本排在紀錄之前：中途斷在兩者之間時沒有紀錄，下次照殘留的進度檔重寫副本。
            if config_baseline {
                let copy = self.env.dir.config_baseline();
                let path = self.vk_rel(&copy)?;
                records.push((path, inputs.config.as_bytes().to_vec()));
            }
            let text = vk_md.render(self.env.written_by);
            let text = text.map_err(|e| self.internal(e.to_string()))?;
            records.push((self.vk_rel(&vk_path)?, text.into_bytes()));
            let tools: Vec<String> = existing
                .as_ref()
                .map(|l| l.tools().keys().cloned().collect())
                .unwrap_or_default();
            records.extend(self.other_records(&tools, &edits)?);
        }
        if stamp_changed {
            records.push((self.vk_rel(&stamp_path)?, stamp));
        }

        let progress = self.progress(&edits)?;
        self.land(progress, &edits, &records, new_lock.as_mut())?;
        for Residual { entry, .. } in &residual {
            if let Err(e) = progress::delete(self.env.dir, &entry.verb, &entry.id) {
                let d = self.failed_diag(&entry.path, e.message(), e.to_string());
                return Err(self.stop(d));
            }
        }

        if let Some(engine) = inputs.engine.as_ref().filter(|_| new_lock.is_some()) {
            self.say(&text::locked(engine));
        }
        for name in &shell_names {
            self.say(&text::wrote_shell(name));
        }
        for e in &edits {
            let line = if e.before.is_some() {
                text::appended(e.path)
            } else {
                text::created(e.path)
            };
            self.say(&line);
        }
        if !residual.is_empty() {
            self.say(text::RECOVERED);
        }
        let (version, host_root) = (self.env.written_by, self.env.host_root);
        self.say(&text::installed(version, host_root));
        Ok(())
    }

    /// 一個根目錄檔要怎麼寫，與它在 `baseline/.vendor_kit.toml` 的新紀錄。
    fn root_file(
        &mut self,
        path: &'static str,
        lines: &[String],
        extra: Option<&str>,
        vk_md: &Metadata,
    ) -> Step<(RootEdit, FileRecord)> {
        let mut contents = String::new();
        for line in lines {
            contents.push_str(line);
            contents.push('\n');
        }
        let init = InitFile {
            path,
            strategy: Strategy::Append,
            contents: contents.as_bytes(),
        };
        let root = self.env.dir.root().to_path_buf();
        let planned = initfiles::plan(
            initfiles::Command::Add,
            &[init],
            vk_md,
            |p| read_optional(&root.join(p)),
            |_| Ok(None),
        );
        let planned = planned.map_err(|e| self.internal(e.to_string()))?;
        let Some(file) = planned.files.into_iter().next() else {
            return Err(self.internal(format!("no plan for {path}")));
        };
        match file.verdict {
            Verdict::Append => {
                let (Some(write), Some(record)) = (file.write, file.record) else {
                    return Err(self.internal(format!("append plan for {path} has no write")));
                };
                let edit = RootEdit {
                    path,
                    before: write.before,
                    after: write.after,
                    ask: true,
                    lines: record.lines.clone(),
                };
                Ok((edit, record))
            }
            Verdict::Gap(Gap::AppendTargetMissing) => {
                // 目標不存在就新建（04 寫入既有檔的例外）；根 `justfile` 附 `default`。
                let mut after = contents;
                if let Some(extra) = extra {
                    after.push('\n');
                    after.push_str(extra);
                    if !after.ends_with('\n') {
                        after.push('\n');
                    }
                }
                let after = after.into_bytes();
                let mut record = FileRecord::new(path, State::Appended);
                record.lines = lines.to_vec();
                record.hash = Some(FileHash::of(&after));
                let edit = RootEdit {
                    path,
                    before: None,
                    after,
                    ask: false,
                    lines: lines.to_vec(),
                };
                Ok((edit, record))
            }
            Verdict::Gap(g) => Err(self.gap(format_args!(
                "installing into {path} without a vendor_kit record ({g:?})"
            ))),
            v => Err(self.internal(format!("unexpected plan for {path}: {v:?}"))),
        }
    }

    /// 沒有紀錄的 `.vendor_kit/config.toml`：不在就照模板新建（04 寫入既有檔的例外：目標不存在就新建），
    /// 記 `managed` 與寫入後的 hash（同 `initfiles` 新建整份初始檔的紀錄）。路徑上已有東西（含 symlink）
    /// 就不碰、不記，回 `None`。
    fn config_file(&mut self, template: &str) -> Step<Option<(RootEdit, FileRecord)>> {
        let path = self.env.dir.config_toml();
        match fs::symlink_metadata(&path) {
            Ok(_) => return Ok(None),
            Err(e) if e.kind() == io::ErrorKind::NotFound => {}
            Err(e) => return Err(self.internal(format!("{CONFIG_TOML}: {e}"))),
        }
        let after = template.as_bytes().to_vec();
        let mut record = FileRecord::new(CONFIG_TOML, State::Managed);
        record.hash = Some(FileHash::of(&after));
        let edit = RootEdit {
            path: CONFIG_TOML,
            before: None,
            after,
            ask: false,
            lines: Vec::new(),
        };
        Ok(Some((edit, record)))
    }

    /// 其他工具的紀錄檔裡同一個路徑的紀錄（ADR-0003）：寫入前內容相符的紀錄跟著換成寫入後的 hash。
    fn other_records(
        &mut self,
        tools: &[String],
        edits: &[RootEdit],
    ) -> Step<Vec<(PathBuf, Vec<u8>)>> {
        let mut out = Vec::new();
        for tool in tools {
            let path = metadata::tool_path(self.env.dir, tool);
            let path = path.map_err(|e| self.internal(e.to_string()))?;
            let Some(mut m) = self.load_metadata(&path)? else {
                continue;
            };
            let mut changed = false;
            for e in edits {
                let Some(before) = &e.before else {
                    continue;
                };
                match m.record_write(e.path, before, &e.after) {
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

    /// 一次問完；全部同意回 `true`，答否印未變更回 `false`，不能互動回 VK0002。
    fn ask(&mut self, questions: &[String], yes: bool) -> Step<bool> {
        let consent = if yes {
            Consent::AssumeYes
        } else {
            Consent::Ask
        };
        let answers = prompt::ask_all(
            questions,
            consent,
            &self.env.tty,
            &mut *self.env.stdin,
            &mut *self.env.prompt,
        );
        match answers {
            Ok(a) if a.all_yes() => Ok(true),
            Ok(_) => {
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

    fn progress(&mut self, edits: &[RootEdit]) -> Step<Progress> {
        let mut p = match Progress::new(INSTALL_VERB, self.env.run_id, self.env.argv) {
            Ok(p) => p,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let files: toml_edit::Array = edits
            .iter()
            .map(|e| {
                let mut t = toml_edit::InlineTable::new();
                t.insert(PATH_KEY, e.path.into());
                let lines: toml_edit::Array = e.lines.iter().map(String::as_str).collect();
                t.insert(LINES_KEY, lines.into());
                t.insert(HASH_KEY, FileHash::of(&e.after).as_str().into());
                toml_edit::Value::from(t)
            })
            .collect();
        let doc = p.document_mut();
        let set = doc
            .set(&[INSTALL_VERB, REPO_FILES_KEY], !edits.is_empty())
            .and_then(|()| doc.set(&[INSTALL_VERB, FILES_KEY], files));
        set.map_err(|e| self.internal(e.to_string()))?;
        Ok(p)
    }

    /// 殘留的 `install` 記過這個檔、而且目前整檔 hash 等於那次寫入後的 hash：那次已經寫進去了
    /// （ADR-0003 以整檔 hash 認定是 VK 寫的），直接補上紀錄，不再問、不再插入。根目錄檔記 `appended`
    /// 與那次的行；`config.toml` 記 `managed`、沒有行。
    fn adopt(&mut self, path: &str, residual: &[Residual]) -> Step<Option<FileRecord>> {
        let Some(w) = residual
            .iter()
            .flat_map(|r| r.files.iter())
            .find(|w| w.path == path)
        else {
            return Ok(None);
        };
        let current = read_optional(&self.env.dir.root().join(path));
        let current = current.map_err(|e| self.internal(format!("{path}: {e}")))?;
        if current.is_none_or(|c| FileHash::of(&c) != w.hash) {
            return Ok(None);
        }
        let mut record = if path == CONFIG_TOML {
            FileRecord::new(path, State::Managed)
        } else {
            let mut r = FileRecord::new(path, State::Appended);
            r.lines = w.lines.clone();
            r
        };
        record.hash = Some(w.hash.clone());
        Ok(Some(record))
    }

    /// 依 `txn` 的順序落地。
    fn land(
        &mut self,
        progress: Progress,
        edits: &[RootEdit],
        records: &[(PathBuf, Vec<u8>)],
        lock: Option<&mut LockFile>,
    ) -> Step<txn::Done> {
        let repo_files: Vec<RepoFile> = edits
            .iter()
            .map(|e| RepoFile {
                path: Path::new(e.path),
                contents: &e.after,
            })
            .collect();
        let record_files: Vec<RecordFile> = records
            .iter()
            .map(|(path, contents)| RecordFile { path, contents })
            .collect();
        let result = {
            let mut fx = Disk::new(self.env.dir, self.env.log, self.env.written_by);
            Txn::begin(&mut fx, progress).and_then(|t| {
                let t = t
                    .swap_cache(&[])?
                    .write_repo_files(&repo_files)?
                    .write_records(&record_files)?
                    .write_tools_just(None)?;
                let t = match lock {
                    Some(lock) => t.write_lock_line(lock, Target::Engine)?,
                    None => t.keep_lock_line(),
                };
                t.complete()
            })
        };
        result.map_err(|f| self.internal(f.to_string()))
    }
}

/// 進度檔 `[install].files` 的一項；格式不對回 `None`。
fn written(v: &toml_edit::Value) -> Option<Written> {
    let t = v.as_inline_table()?;
    let path = t.get(PATH_KEY)?.as_str()?.to_owned();
    let lines = t
        .get(LINES_KEY)?
        .as_array()?
        .iter()
        .map(|l| l.as_str().map(str::to_owned))
        .collect::<Option<Vec<_>>>()?;
    let hash = FileHash::parse(t.get(HASH_KEY)?.as_str()?)?;
    Some(Written { path, lines, hash })
}

/// 讀檔；不在回 `None`。
fn read_optional(path: &Path) -> io::Result<Option<Vec<u8>>> {
    match fs::read(path) {
        Ok(b) => Ok(Some(b)),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(None),
        Err(e) => Err(e),
    }
}
