//! `dev` 與 `undev` 指令（04 指令表、成對與無害、本機覆寫；GLOSSARY 本機覆寫、本機開發來源）：
//! 開啟與解除本機覆寫。兩個指令改的是同一份 `version.local.toml`、同一份 `gen/tools.just`，判定與恢復也
//! 共用，所以放在同一個 crate。
//!
//! 呼叫端（入口 `vendor_kit`）已解析好參數、判過安裝目錄（VK0028），並接好執行紀錄。這裡依序做：
//!
//! 1. 讀 `.vendor_kit/config.toml`（VK0059），在取鎖之前（04 設定）。
//! 2. 取安裝目錄的排他鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束：兩者都是可寫 recipe。
//! 3. 讀 `version.toml` 與 `version.local.toml`（檔案版過高回 VK0008）。
//! 4. 辨識殘留的進度檔（見「恢復」）；不能併入的有任何一份就把每一份都印出來再停下。
//! 5. 判對象：`undev <repo>` 的工具不在版本鎖定行回 VK0046（訊息表：先辨識未完成進度，再判斷對象不存在，
//!    所以排在第 4 步之後）。
//! 6. 判要做什麼：
//!    - `dev <repo> -p <dir>`：已有同來源的覆寫、也沒有殘留，stdout 說明未變更；已有不同來源的覆寫回
//!      VK0050，不取代。`<dir>` 相對於安裝目錄（見「本機目錄」），要存在、是目錄、符合交付格式（`dist/`
//!      的形狀：`just/<ns>.just`，`<repo>.just` 必須存在，ADR-0004），否則回 VK0051。
//!    - `undev <repo>`、`undev --engine`：沒有覆寫、也沒有殘留，stdout 說明未變更。`undev` 不讀原來源
//!      （04 本機覆寫）。
//! 7. 算出新的 `gen/tools.just`（`tools_just::render_with`）：開著覆寫的工具指向本機目錄，其他工具指向
//!    `cache/<repo>/`。`<ns>` 從各自的來源讀：其他開著覆寫的工具要讀它的本機目錄，讀不到回 VK0052（04：
//!    覆寫來源失效只擋需讀它的動作）。`undev <repo>` 的對象回到鎖定版本，要 `cache/<repo>/` 與印記、版本
//!    鎖定行一致才能直接指回去（見「缺口」）。`undev --engine` 不動入口檔。
//! 8. 經 `txn` 落地：建進度檔 → 寫 `version.local.toml`（記錄檔那一步）→ 寫 `gen/tools.just` → 刪進度檔；
//!    不改版本鎖定行（`keep_lock_line`），不動 `cache/`（`swap_cache(&[])`）。覆寫的增減排在入口檔之前：
//!    04 本機覆寫「`undev` 同步未完成時，覆寫已解除，須重跑原 `undev`」。之後才刪併入的殘留進度檔。
//!    `undev` 在覆寫已寫好、入口檔還沒寫好時失敗，回 VK0053（訊息表：undev 解除覆寫後同步失敗）。
//! 9. stdout 列出改了什麼與用了哪個覆寫（04 本機覆寫：每次報告用了哪個覆寫，不加診斷前綴）。
//!
//! 這裡不碰 docker，不用 `plan` 往返。
//!
//! # 本機目錄
//!
//! 引擎容器只看得到安裝目錄（`plan::mount::ROOT`）與這次呼叫的往返目錄，所以 `-p <dir>` 只收落在安裝
//! 目錄裡、引擎讀得到的目錄：以安裝目錄為準逐段正規化（`.` 略過，`..` 往上一層），結果寫成 `/` 分隔的
//! 相對路徑（整個是安裝目錄本身時寫 `.`），存進 `version.local.toml`，入口檔照同一個值指過去。重複 `dev`
//! 是不是同來源，比的是正規化後的值。絕對路徑、跑出安裝目錄、路徑上有 symlink（容器裡解不出主機上的
//! 目標）、含放不進 just 單引號字串的字元，都見「缺口」。
//!
//! # 恢復
//!
//! 殘留的 `dev`、`undev` 進度檔記了對象（`[<verb>] target`；`dev` 另記正規化後的 `path`）。對象跟這次相同
//! 的併進這次：先照殘留的那次把覆寫在記憶體裡補成做完的樣子（`dev` 設成它的 `path`，`undev` 拿掉），再照
//! 這次的參數判定，落地時一起寫，這次落地完成之後才刪殘留的那幾份，中途再斷也還認得出來。有殘留時即使沒有
//! 要改的，也走一次 `txn`，讓刪除排在 `writes_started` 之後。殘留的對象不同、或是其他 verb 的，見「缺口」。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 進度檔 `.tmp.<verb>.<run-id>.toml` 另記 `[<verb>]` 表的 `target`（工具名，引擎是 [`ENGINE_TARGET`]）與
//!   `dev` 的 `path`。`update` 偵測到殘留的 `undev` 時，VK0053 的 `<target>` 讀這個欄位。
//! - VK0050、VK0052、VK0053 的 `<target>`：工具填 `<repo>`，引擎填 [`ENGINE_TARGET`]。
//! - 覆寫全部解除後 `version.local.toml` 照留（只剩檔案版與寫入者），不刪。
//! - stdout 的字句見 [`text`]。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - `dev --engine -i <image>`：本機 image 怎麼驗、舊引擎不得重產薄殼的禁令（ADR-0010；計畫 G6）、
//!   啟動器怎麼套用引擎覆寫都沒接上。
//! - `dev <repo>` 的工具不在版本鎖定行：VK0046 只寫 remove、undev、update（計畫 G5）。
//! - `-p` 指到安裝目錄外（絕對路徑或 `..` 跑出去）：引擎讀不到，`plan` 協定也沒有把本機開發來源掛進
//!   引擎的 op，驗不了「存在且符合交付格式」。路徑上有 symlink、或路徑不是 UTF-8、含 `'`、反斜線、
//!   控制字元，也停下。
//! - `dev` 的 `<ns>` 撞名：VK0030 只寫 `add`。工具之間撞名、或交付保留名 `vendor_kit` 時停下；根
//!   `justfile` 的 recipe 與 module 這一版不比對。
//! - `undev <repo>` 時 `cache/<repo>/` 跟版本鎖定行對不上（印記不在、損壞、版本不同或內容不符，例如開著
//!   覆寫時 `git pull` 換了鎖定行）：要在解除覆寫之後取件，但 `txn` 的順序是先換 `cache/` 再寫記錄檔，
//!   跟「覆寫先解除」相反，要另加 `txn` 的順序；這一版在寫任何檔之前停下。
//! - 其他工具的 `cache/<repo>/` 讀不到（例如還沒 `sync`）：重產入口檔要用到它的 `<ns>`。
//! - 殘留的進度檔是其他 verb 的，或 `dev`、`undev` 但對象不同：怎麼併入沒定。
//! - 中途寫檔失敗沒有代碼（G4），`undev` 解除覆寫後的那一段除外（VK0053）。

pub mod text;

#[cfg(test)]
mod tests;

use std::collections::BTreeMap;
use std::ffi::OsStr;
use std::fs;
use std::io::{self, Write};
use std::path::{Component, Path};

use config::{Config, ConfigError};
use diagnostics::{Diagnostic, Diagnostics, Message, Sink};
use filelock::{Lock, Mode};
use imageref::ImageRef;
use layout::InstallDir;
use progress::Progress;
use txn::{Disk, RecordFile, Txn};
use version_file::{LocalFile, LockFile};

/// `dev` 的進度檔 `<verb>`。
pub const DEV_VERB: &str = "dev";
/// `undev` 的進度檔 `<verb>`。
pub const UNDEV_VERB: &str = "undev";
/// 進度檔 `[<verb>]` 表裡記對象的鍵。
pub const TARGET_KEY: &str = "target";
/// `dev` 的進度檔 `[dev]` 表裡記正規化後本機目錄的鍵。
pub const PATH_KEY: &str = "path";
/// 引擎當對象時的 `<target>`（與 `update` 結果行的引擎名欄相同）。
pub const ENGINE_TARGET: &str = "vendor_kit";
/// 重組指令時接在參數前面的字。
pub const COMMAND_PREFIX: [&str; 2] = ["just", "vendor_kit"];
/// `version.local.toml` 相對於 `.vendor_kit/` 的路徑（`txn` 記錄檔那一步收這種路徑）。
const LOCAL_FILE: &str = "version.local.toml";

/// 一次 `dev` 或 `undev` 的參數（`args::Command` 的四種）。
#[derive(Debug, Clone, Copy)]
pub enum Request<'a> {
    /// `dev <repo> -p <dir>`
    DevTool { repo: &'a str, path: &'a OsStr },
    /// `dev --engine -i <image>`
    DevEngine { image: &'a OsStr },
    /// `undev <repo>`
    UndevTool { repo: &'a str },
    /// `undev --engine`
    UndevEngine,
}

impl Request<'_> {
    fn verb(&self) -> &'static str {
        match self {
            Request::DevTool { .. } | Request::DevEngine { .. } => DEV_VERB,
            Request::UndevTool { .. } | Request::UndevEngine => UNDEV_VERB,
        }
    }

    fn target(&self) -> &str {
        match self {
            Request::DevTool { repo, .. } | Request::UndevTool { repo } => repo,
            Request::DevEngine { .. } | Request::UndevEngine => ENGINE_TARGET,
        }
    }
}

/// 這次執行的環境。`dev`、`undev` 不詢問、不碰 docker，所以沒有 stdin、終端狀態與往返通道。
pub struct Env<'a, W: Write, S: Sink, L: Write> {
    /// 容器內的安裝目錄（`plan::mount::ROOT`）。
    pub dir: &'a InstallDir,
    /// 主機上的安裝目錄，填 `<install_dir>`。
    pub host_root: &'a str,
    /// 主機上的執行紀錄路徑，填 VK0056 的 `<path>`。
    pub run_log: &'a str,
    /// `just vendor_kit` 之後的參數原樣（第一個是 `dev` 或 `undev`）。
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

/// 跑一次 `dev` 或 `undev`，回傳結束碼。
pub fn run<W: Write, S: Sink, L: Write>(req: &Request<'_>, env: &mut Env<'_, W, S, L>) -> u8 {
    let mut dev = Dev { env, code: 0 };
    let _ = dev.run(req);
    dev.code
}

/// POSIX shell 引號：只含安全字元的字原樣留下；其他（含空字串）包單引號，`'` 換成 `'\''`
/// （與 engine/prompt 的 VK0002 `<command_with_y>` 同一條規則；指令之間互不依賴，照抄 engine/update）。
pub fn shell_quote(s: &str) -> String {
    let safe = |c: char| c.is_ascii_alphanumeric() || "_@%+=:,./-".contains(c);
    if !s.is_empty() && s.chars().all(safe) {
        return s.to_owned();
    }
    format!("'{}'", s.replace('\'', r"'\''"))
}

/// 由 `just vendor_kit` 之後的參數重組完整指令。
pub fn full_command<S: AsRef<str>>(command: &[S]) -> String {
    COMMAND_PREFIX
        .iter()
        .map(|w| (*w).to_owned())
        .chain(command.iter().map(|w| shell_quote(w.as_ref())))
        .collect::<Vec<_>>()
        .join(" ")
}

/// 解除某個對象覆寫的指令（VK0050、VK0052 的 `<undev_command>`）。
pub fn undev_command(target: &str) -> String {
    if target == ENGINE_TARGET {
        full_command(&["undev", "--engine"])
    } else {
        full_command(&["undev", target])
    }
}

/// `-p <dir>` 為什麼不能用。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PathProblem {
    /// 不存在、不是目錄或不符合交付格式（VK0051 的 `<reason>`）。
    Unusable(String),
    /// 契約或協定沒定的情況（見模組說明的缺口），值是 VK0056 的說明。
    Gap(String),
}

/// 把 `-p <dir>` 以安裝目錄為準逐段正規化成 `/` 分隔的相對路徑（安裝目錄本身是 `.`）。只看字面，不碰檔案系統。
pub fn normalize(given: &OsStr) -> Result<String, PathProblem> {
    let Some(text) = given.to_str() else {
        return Err(PathProblem::Gap(format!(
            "a local source path that is not UTF-8 ({})",
            given.to_string_lossy()
        )));
    };
    if text.is_empty() {
        return Err(PathProblem::Unusable("the path is empty".to_owned()));
    }
    let path = Path::new(text);
    let outside = || {
        PathProblem::Gap(format!(
            "a local source outside the install directory ({text})"
        ))
    };
    let mut parts: Vec<&str> = Vec::new();
    for c in path.components() {
        match c {
            Component::CurDir => {}
            Component::ParentDir => {
                parts.pop().ok_or_else(outside)?;
            }
            Component::Normal(seg) => parts.push(seg.to_str().ok_or_else(outside)?),
            Component::RootDir | Component::Prefix(_) => return Err(outside()),
        }
    }
    let joined = if parts.is_empty() {
        ".".to_owned()
    } else {
        parts.join("/")
    };
    if tools_just::is_local_dir(&joined) {
        Ok(joined)
    } else {
        Err(PathProblem::Gap(format!(
            "a local source path containing a quote, a backslash, or a control character ({text})"
        )))
    }
}

/// 檢查正規化後的本機目錄 `rel`（相對於 `root`）：每一段都不是 symlink、存在、最後是目錄，而且符合交付
/// 格式、交付了 `<repo>.just`。回傳它交付的全部 `<ns>`。
pub fn check_dir(root: &Path, rel: &str, repo: &str) -> Result<Vec<String>, PathProblem> {
    let mut at = root.to_path_buf();
    if rel != "." {
        for seg in rel.split('/') {
            at.push(seg);
            match fs::symlink_metadata(&at) {
                Ok(m) if m.file_type().is_symlink() => {
                    return Err(PathProblem::Gap(format!(
                        "a local source path through a symlink ({})",
                        at.strip_prefix(root).unwrap_or(&at).display()
                    )));
                }
                Ok(_) => {}
                Err(e) if e.kind() == io::ErrorKind::NotFound => {
                    return Err(PathProblem::Unusable(
                        "the directory does not exist".to_owned(),
                    ));
                }
                Err(e) => return Err(PathProblem::Unusable(e.to_string())),
            }
        }
    }
    if !at.is_dir() {
        return Err(PathProblem::Unusable("it is not a directory".to_owned()));
    }
    let ns = fetch::namespaces(&at).map_err(|e| PathProblem::Unusable(e.to_string()))?;
    if !ns.iter().any(|n| n == repo) {
        return Err(PathProblem::Unusable(format!(
            "{}/{repo}{} is missing",
            fetch::JUST_DIR,
            fetch::JUST_EXT
        )));
    }
    Ok(ns)
}

/// 診斷已印、這次執行停下。
struct Stop;

type Step<T> = Result<T, Stop>;

/// 併進這次的一份殘留進度檔。
struct Residual {
    entry: progress::Entry,
    /// `dev` 記的正規化後本機目錄；`undev` 是 `None`。
    path: Option<String>,
}

/// 判定後要落地的內容。
struct Plan {
    /// 新的 `version.local.toml`；`None` 表示覆寫不變。
    local: Option<LocalFile>,
    /// 新的 `gen/tools.just`；`None` 表示入口檔不變。
    entry: Option<String>,
    /// 落地後要印的字句（不含入口檔與恢復）。
    said: Vec<String>,
}

struct Dev<'r, 'a, W: Write, S: Sink, L: Write> {
    env: &'r mut Env<'a, W, S, L>,
    code: u8,
}

impl<W: Write, S: Sink, L: Write> Dev<'_, '_, W, S, L> {
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

    fn run(&mut self, req: &Request<'_>) -> Step<()> {
        if let Request::DevEngine { image } = req {
            let image = image.to_string_lossy().into_owned();
            return Err(self.gap(format_args!(
                "dev --engine -i {image} (validating the local engine image and applying the engine override)"
            )));
        }
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        let lockfile = self.lockfile()?;
        let disk = self.local_file()?;
        let residual = self.residuals(req)?;

        let mut local = disk.clone().unwrap_or_default();
        for r in &residual {
            let applied = match (&r.path, req.target()) {
                (Some(path), target) => local.set_tool(target, path),
                (None, ENGINE_TARGET) => local.remove_engine().map(|_| ()),
                (None, target) => local.remove_tool(target).map(|_| ()),
            };
            if let Err(e) = applied {
                return Err(self.internal(e.to_string()));
            }
        }

        let recovering = !residual.is_empty();
        let plan = match req {
            Request::DevTool { repo, path } => {
                self.dev_tool(&lockfile, &mut local, repo, path, recovering)?
            }
            Request::UndevTool { repo } => {
                self.undev_tool(&lockfile, &mut local, repo, recovering)?
            }
            Request::UndevEngine => {
                let had = local.engine().is_some() || recovering;
                if let Err(e) = local.remove_engine() {
                    return Err(self.internal(e.to_string()));
                }
                let said = if had {
                    vec![text::undev_engine(lockfile.engine())]
                } else {
                    vec![text::UNDEV_ENGINE_UNCHANGED.to_owned()]
                };
                Plan {
                    local: Some(local),
                    entry: None,
                    said,
                }
            }
            Request::DevEngine { .. } => return Err(self.internal("dev --engine reached planning")),
        };

        // 覆寫的實際內容跟檔上一樣就不寫（殘留併進來時，記憶體裡的可能已經跟檔上不同）。
        let local = plan.local.filter(|l| !same_overrides(l, disk.as_ref()));
        if local.is_none() && plan.entry.is_none() && residual.is_empty() {
            for line in &plan.said {
                self.say(line);
            }
            return Ok(());
        }

        self.land(req, local, plan.entry.as_deref())?;
        for r in &residual {
            if let Err(err) = progress::delete(self.env.dir, &r.entry.verb, &r.entry.id) {
                let d = self.failed_diag(&r.entry.path, err.message(), err.to_string());
                return Err(self.stop(d));
            }
        }

        for line in &plan.said {
            self.say(line);
        }
        if plan.entry.is_some() {
            self.say(text::TOOLS_JUST_UPDATED);
        }
        for r in &residual {
            let shown = self.rel(&r.entry.path);
            self.say(&text::recovered(&r.entry.verb, &shown));
        }
        Ok(())
    }

    /// `dev <repo> -p <dir>` 的判定（模組說明第 5–7 步）。
    fn dev_tool(
        &mut self,
        lockfile: &LockFile,
        local: &mut LocalFile,
        repo: &str,
        path: &OsStr,
        recovering: bool,
    ) -> Step<Plan> {
        if lockfile.tool(repo).is_none() {
            return Err(self.gap(format_args!(
                "dev for {repo}, which is not in the lock version lines (no reason code)"
            )));
        }
        let shown = path.to_string_lossy().into_owned();
        let unusable = |reason: String| {
            Diagnostic::new(&messages::VK0051)
                .arg("path", shown.as_str())
                .arg("repo", repo)
                .arg("reason", reason)
        };
        let dir = match normalize(path) {
            Ok(d) => d,
            Err(PathProblem::Unusable(reason)) => return Err(self.stop(unusable(reason))),
            Err(PathProblem::Gap(what)) => return Err(self.gap(what)),
        };
        if let Some(current) = local.tool(repo) {
            let current_norm = normalize(OsStr::new(current)).ok();
            if current_norm.as_deref() == Some(dir.as_str()) {
                // 重複 `dev` 同來源：04 只要求 stdout 說明未變更，入口檔不另修。併進殘留的 `dev` 時
                // 覆寫可能還沒寫進檔、入口檔也可能還沒指過去，照常算。
                if !recovering {
                    return Ok(Plan {
                        local: None,
                        entry: None,
                        said: vec![text::dev_unchanged(repo, &dir)],
                    });
                }
                let entry = self.entry_if_changed(lockfile, local, None)?;
                return Ok(Plan {
                    local: Some(local.clone()),
                    entry,
                    said: vec![text::dev_enabled(repo, &dir)],
                });
            }
            let d = Diagnostic::new(&messages::VK0050)
                .arg("target", repo)
                .arg("undev_command", undev_command(repo));
            return Err(self.stop(d));
        }
        let ns = match check_dir(self.env.dir.root(), &dir, repo) {
            Ok(ns) => ns,
            Err(PathProblem::Unusable(reason)) => return Err(self.stop(unusable(reason))),
            Err(PathProblem::Gap(what)) => return Err(self.gap(what)),
        };
        if ns.iter().any(|n| n == ENGINE_TARGET) {
            return Err(self.gap(format_args!(
                "dev for {repo} whose local source delivers the reserved namespace {ENGINE_TARGET} (no reason code)"
            )));
        }
        if let Err(e) = local.set_tool(repo, &dir) {
            return Err(self.internal(e.to_string()));
        }
        let mut known = BTreeMap::new();
        known.insert(repo.to_owned(), ns);
        let entry = self.entry_if_changed(lockfile, local, Some(known))?;
        Ok(Plan {
            local: Some(local.clone()),
            entry,
            said: vec![text::dev_enabled(repo, &dir)],
        })
    }

    /// `undev <repo>` 的判定（模組說明第 5–7 步）。
    fn undev_tool(
        &mut self,
        lockfile: &LockFile,
        local: &mut LocalFile,
        repo: &str,
        recovering: bool,
    ) -> Step<Plan> {
        let Some(locked) = lockfile.tool(repo) else {
            let d = Diagnostic::new(&messages::VK0046).arg("repo", repo);
            return Err(self.stop(d));
        };
        // 併進殘留的 `undev` 時覆寫可能已經解除、入口檔還沒指回去，照常算。
        if local.tool(repo).is_none() && !recovering {
            return Ok(Plan {
                local: None,
                entry: None,
                said: vec![text::undev_tool_unchanged(repo)],
            });
        }
        let ns = self.locked_cache(repo, locked)?;
        if let Err(e) = local.remove_tool(repo) {
            return Err(self.internal(e.to_string()));
        }
        let mut known = BTreeMap::new();
        known.insert(repo.to_owned(), ns);
        let entry = self.entry_if_changed(lockfile, local, Some(known))?;
        Ok(Plan {
            local: Some(local.clone()),
            entry,
            said: vec![text::undev_tool(repo, locked)],
        })
    }

    /// `undev <repo>` 的對象回到鎖定版本：`cache/<repo>/` 要與印記一致，印記的版本要是版本鎖定行的值。
    /// 回傳 `cache/<repo>/` 交付的 `<ns>`。
    fn locked_cache(&mut self, repo: &str, locked: &ImageRef) -> Step<Vec<String>> {
        let refetch = || {
            format!(
                "undev {repo} while cache/{repo}/ does not match the lock version line \
                 (fetching the locked version after removing the override)"
            )
        };
        let stamp = match stamp::Stamp::load(&stamp::tool_file(self.env.dir, repo)) {
            Ok(Some(s)) if s.version() == locked.to_string() => s,
            Ok(_) | Err(stamp::Error::Corrupt { .. }) => return Err(self.gap(refetch())),
            Err(stamp::Error::TooNew { file, too_new }) => {
                let d = self.too_new_diag(&file, &too_new);
                return Err(self.stop(d));
            }
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let cache = match self.env.dir.tool_cache(repo) {
            Ok(c) => c,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        match stamp.verify(&cache) {
            Ok(diff) if diff.is_match() => {}
            Ok(_) => return Err(self.gap(refetch())),
            Err(e) => return Err(self.internal(format!("cache of {repo}: {e}"))),
        }
        fetch::namespaces(&cache).map_err(|e| {
            self.internal(format!(
                "cache of {repo} matches its stamp, but its tool content is invalid: {e}"
            ))
        })
    }

    /// 依覆寫算出新的 `gen/tools.just`（模組說明第 7 步），跟現有內容一樣回 `None`。`known` 是這次已經讀過
    /// `<ns>` 的工具。
    fn entry_if_changed(
        &mut self,
        lockfile: &LockFile,
        local: &LocalFile,
        known: Option<BTreeMap<String, Vec<String>>>,
    ) -> Step<Option<String>> {
        let mut known = known.unwrap_or_default();
        let mut dirs: BTreeMap<String, String> = BTreeMap::new();
        let mut blocked: Vec<Diagnostic> = Vec::new();
        for repo in lockfile.tools().keys() {
            let source = local.tool(repo);
            if let Some(source) = source {
                match normalize(OsStr::new(source)) {
                    Ok(dir) => {
                        dirs.insert(repo.clone(), dir);
                    }
                    Err(PathProblem::Unusable(reason) | PathProblem::Gap(reason)) => {
                        blocked.push(self.unreadable(repo, source, reason));
                        continue;
                    }
                }
            }
            if known.contains_key(repo) {
                continue;
            }
            let ns = match dirs.get(repo) {
                Some(dir) => match check_dir(self.env.dir.root(), dir, repo) {
                    Ok(ns) => ns,
                    Err(PathProblem::Unusable(reason) | PathProblem::Gap(reason)) => {
                        let source = source.unwrap_or(dir).to_owned();
                        blocked.push(self.unreadable(repo, &source, reason));
                        continue;
                    }
                },
                None => {
                    let cache = match self.env.dir.tool_cache(repo) {
                        Ok(c) => c,
                        Err(e) => return Err(self.internal(e.to_string())),
                    };
                    match fetch::namespaces(&cache) {
                        Ok(ns) => ns,
                        Err(e) => {
                            blocked.push(self.gap_diag(format_args!(
                                "regenerating gen/tools.just while cache/{repo}/ cannot be read ({e})"
                            )));
                            continue;
                        }
                    }
                }
            };
            known.insert(repo.clone(), ns);
        }
        if !blocked.is_empty() {
            for d in blocked {
                self.emit(d);
            }
            return Err(Stop);
        }
        let tools: Vec<tools_just::Tool> = known
            .iter()
            .filter(|(repo, _)| lockfile.tool(repo).is_some())
            .map(|(repo, ns)| tools_just::Tool {
                repo,
                namespaces: ns,
            })
            .collect();
        let entry = match tools_just::render_with(&tools, &dirs) {
            Ok(e) => e,
            Err(e @ tools_just::Error::Duplicate { .. }) => {
                return Err(self.gap(format_args!(
                    "{e} after the local override (no reason code)"
                )));
            }
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let path = self.env.dir.gen_dir().join(txn::TOOLS_JUST);
        match fs::read(&path) {
            Ok(b) if b == entry.as_bytes() => Ok(None),
            Ok(_) => Ok(Some(entry)),
            Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(Some(entry)),
            Err(e) => Err(self.internal(format!("{}: {e}", path.display()))),
        }
    }

    /// VK0052：需要讀其他工具的本機開發來源，卻讀不到。
    fn unreadable(&self, repo: &str, source: &str, reason: String) -> Diagnostic {
        Diagnostic::new(&messages::VK0052)
            .arg("target", repo)
            .arg("source", source)
            .arg("reason", reason)
            .arg("undev_command", undev_command(repo))
    }

    /// 經 `txn` 落地（模組說明第 8 步）。
    fn land(
        &mut self,
        req: &Request<'_>,
        local: Option<LocalFile>,
        entry: Option<&str>,
    ) -> Step<()> {
        let mut progress = match Progress::new(req.verb(), self.env.run_id, self.env.argv) {
            Ok(p) => p,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let mut fields: Vec<(&str, String)> = vec![(TARGET_KEY, req.target().to_owned())];
        if let Request::DevTool { repo, .. } = req
            && let Some(dir) = local.as_ref().and_then(|l| l.tool(repo))
        {
            fields.push((PATH_KEY, dir.to_owned()));
        }
        for (key, value) in fields {
            if let Err(e) = progress.document_mut().set(&[req.verb(), key], value) {
                return Err(self.internal(e.to_string()));
            }
        }
        let rendered = match local {
            Some(mut l) => match l.render(self.env.written_by) {
                Ok(text) => Some(text),
                Err(e) => return Err(self.internal(e.to_string())),
            },
            None => None,
        };
        let records: Vec<RecordFile> = rendered
            .iter()
            .map(|text| RecordFile {
                path: Path::new(LOCAL_FILE),
                contents: text.as_bytes(),
            })
            .collect();
        let result = {
            let mut fx = Disk::new(self.env.dir, self.env.log, self.env.written_by);
            Txn::begin(&mut fx, progress).and_then(|t| {
                t.swap_cache(&[])?
                    .write_repo_files(&[])?
                    .write_records(&records)?
                    .write_tools_just(entry.map(str::as_bytes))?
                    .keep_lock_line()
                    .complete()
            })
        };
        match result {
            Ok(_) => Ok(()),
            // 覆寫已經解除、入口檔或完成點沒寫好：訊息表的「undev 解除覆寫後同步失敗」。
            Err(f)
                if req.verb() == UNDEV_VERB
                    && f.step > txn::Step::Records
                    && !f.step.completed() =>
            {
                let d = Diagnostic::new(&messages::VK0053)
                    .arg("target", req.target())
                    .arg("undev_command", full_command(self.env.argv));
                Err(self.stop(d))
            }
            Err(f) => Err(self.internal(f.to_string())),
        }
    }

    /// 殘留的進度檔（模組說明「恢復」）：對象相同的 `dev`、`undev` 併進這次，其他的把每一份都印出來再停下。
    fn residuals(&mut self, req: &Request<'_>) -> Step<Vec<Residual>> {
        let entries = match progress::find(self.env.dir) {
            Ok(e) => e,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let mut merged = Vec::new();
        let mut blocked = Vec::new();
        for entry in entries {
            match self.residual(req, entry) {
                Ok(r) => merged.push(r),
                Err(d) => blocked.push(d),
            }
        }
        if blocked.is_empty() {
            Ok(merged)
        } else {
            for d in blocked {
                self.emit(d);
            }
            Err(Stop)
        }
    }

    fn residual(&self, req: &Request<'_>, entry: progress::Entry) -> Result<Residual, Diagnostic> {
        let loaded = match entry.load() {
            Ok(p) => p,
            Err(progress::Error::Parse {
                file,
                source: progress::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => return Err(self.too_new_diag(&file, &t)),
            Err(e) => return Err(self.failed_diag(&entry.path, e.message(), e.to_string())),
        };
        let shown = self.rel(&entry.path);
        let verb = entry.verb.as_str();
        if verb != DEV_VERB && verb != UNDEV_VERB {
            return Err(self.gap_diag(format_args!(
                "{} while the incomplete {verb} operation in {shown} remains",
                req.verb()
            )));
        }
        let field = |key: &str| {
            loaded
                .document()
                .get(&[verb, key])
                .and_then(|i| i.as_str())
                .map(str::to_owned)
        };
        let Some(target) = field(TARGET_KEY) else {
            return Err(self.gap_diag(format_args!(
                "recovering the incomplete {verb} in {shown} without its [{verb}] {TARGET_KEY} field"
            )));
        };
        if target != req.target() {
            return Err(self.gap_diag(format_args!(
                "{} {} while the incomplete {verb} of {target} in {shown} remains",
                req.verb(),
                req.target()
            )));
        }
        let path = if verb == DEV_VERB {
            match field(PATH_KEY) {
                Some(p) if target != ENGINE_TARGET => Some(p),
                _ => {
                    return Err(self.gap_diag(format_args!(
                        "recovering the incomplete dev in {shown} without its [dev] {PATH_KEY} field"
                    )));
                }
            }
        } else {
            None
        };
        Ok(Residual { entry, path })
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

    fn local_file(&mut self) -> Step<Option<LocalFile>> {
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
}

/// 兩份覆寫的內容（引擎與每個工具的來源）一樣；檔不在等於沒有任何覆寫。
fn same_overrides(a: &LocalFile, b: Option<&LocalFile>) -> bool {
    let empty = LocalFile::new();
    let b = b.unwrap_or(&empty);
    a.engine() == b.engine() && a.tools() == b.tools()
}
