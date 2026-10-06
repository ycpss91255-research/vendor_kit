//! `sync` 指令（04 指令表 `sync`、04 sync 節、04 本機覆寫）：依版本鎖定行同步全部已導入工具的 `cache/` 與
//! `gen/`；開著本機覆寫的工具改用本機開發來源。
//!
//! 呼叫端（入口 `vendor_kit`）已解析好參數、判過安裝目錄（VK0028），並接好執行紀錄與 `plan` 往返。
//! 這裡依序做：
//!
//! 1. 讀 `.vendor_kit/config.toml`（VK0059），在第一次取鎖之前（04 設定）。
//! 2. 取安裝目錄的排他鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束：會取件的 `sync`
//!    屬寫入端（04 鎖與逾時）。`sync` 仍是唯讀 recipe（名詞表、ADR-0007）：不動追蹤檔，也不動進度檔。
//! 3. 讀 `version.toml`（檔案版過高回 VK0008）。
//! 4. 逐工具處理前先判（04 sync 第 2 步；02 不變量 4：動到任何工具之前判定有工具不能做，就一個都不動，
//!    並列出每個原因）。這一段只讀、不取件、不寫（安裝目錄外的本機開發來源經 `stage-dir` 複製進 session
//!    目錄，不寫安裝目錄，見「本機覆寫」）：
//!    - 薄殼：以 `compat` 的介面版、本引擎版與隨 image 出貨的模板本文（呼叫端給，跟 `install` 寫薄殼用的
//!      是同一份）產生這一版的薄殼，跑 `shell::Shell::check`；任一檔不符回 VK0006，`<files>` 逐檔標出是哪一種。
//!      `sync` 不重產薄殼（ADR-0007：只有 `install`、`upgrade --engine`、`bootstrap.sh --repair` 重產）。
//!      模板沒有（image 沒出貨）或薄殼檔是 symlink、不是一般檔：VK0056。版本組合的介面版（VK0009）由啟動器
//!      在起引擎前判，不在引擎。
//!    - 每個讀到的 VK 檔（`version.local.toml`、進度檔、每個工具的印記）檔案版過高：VK0008。
//!    - 殘留的進度檔（04 成對與無害：唯讀 recipe 只偵測，不恢復、不刪；見「殘留的進度檔」）：`add` 的回
//!      VK0004；工具 `upgrade` 的回 VK0041；`undev` 的回 VK0053（見「本機覆寫」）；其他可寫 recipe 的回
//!      VK0054；引擎 `upgrade` 的見「缺口」。
//!    - `version.local.toml` 的工具覆寫：讀本機開發來源（見「本機覆寫」），讀不到回 VK0052。
//!    - 沒有覆寫的工具的印記：不在（首次取件，不算損壞）、損壞（VK0044）或讀得到。
//! 5. 沒有覆寫的工具逐一判定要不要重取（04 sync 表）：
//!    - 印記不在：取件，不警告。
//!    - 印記損壞：重新取件並重建印記，警告 VK0044。
//!    - 印記的版本與版本鎖定行不同（例如 `git pull` 換了鎖定行）：取件，不警告；VK0015 的情況只講檔案集合
//!      與逐檔指紋不符。
//!    - 版本相同：以印記比對 `cache/<repo>/` 的檔案集合與逐檔指紋，包括多出的檔與整個目錄不在；不一致就
//!      重新取件，警告 VK0015。一致就不動，`<ns>` 從 `cache/<repo>/` 讀。
//!    - 未列在版本鎖定行的工具目錄不看，留給 `prune`；初始檔不動（基準版落後見「缺口」）。
//! 6. 要取件的工具，經 `plan` 協定請啟動器 `inspect` 帶 digest 的引用 `<registry>/<路徑>@<digest>`；本機沒有
//!    就 `pull` 同一個引用再 `inspect`，再以 image ID `extract`。docker 動作失敗回 VK0055。取件只用
//!    [`plan::RESCUE_OPS`] 裡的 op：`sync` 是救援路徑（ADR-0007、ADR-0008 凍結子集）。本機覆寫的
//!    `stage-dir` 不在這個子集裡，救援路徑送不出（見「本機覆寫」）。
//! 7. `fetch::verify`：inspect 回來的 RepoDigests 要有版本鎖定行的 digest，不符回 VK0043（不報 VK0015）；
//!    dist 格式、逐檔指紋。一個工具失敗時其他工具照樣取件驗證，列出每個原因，但一個都不落地。
//! 8. 用 `tools_just::render_with` 依這次的全部工具（重取的用暫存內容的 `<ns>`，沒重取的讀 `cache/<repo>/`，
//!    開著覆寫的讀本機開發來源）重產 `gen/tools.just`，與現有內容逐位元組比對。開著覆寫的工具那幾行指向
//!    本機開發來源。
//! 9. 沒有要重取的工具、入口檔也不變：什麼都不寫，stdout 只報告用了哪個覆寫（沒有覆寫就不印，[`text`]）。
//! 10. 否則重驗暫存內容（ADR-0006 第三層），經 [`txn::refresh`] 依序落地：`cache/<repo>/` 與印記、
//!     `gen/tools.just`；不建進度檔、不改版本鎖定行（04 成對與無害：`sync` 不改追蹤檔）。
//! 11. stdout 先報告用了哪個覆寫，再列出改了什麼；VK0015、VK0044 在落地之後才印（本文是「已重新取件」）。
//!
//! # 本機覆寫
//!
//! `version.local.toml` 有工具的覆寫（`dev <repo> -p <dir>`）時，那個工具在覆寫期間的內容由本機開發來源決定
//! （02 不變量 2 的本機覆寫例外；名詞表的本機覆寫、本機開發來源），跟 engine/dev 的做法一致：
//!
//! - 不取件，不看也不寫那個工具的 `cache/<repo>/` 與印記（`cache/<repo>/` 留著鎖定版本，`undev` 才能不讀
//!   原來源就回到鎖定版本）。開著覆寫時版本鎖定行換了版（`cache/<repo>/` 跟鎖定行對不上），`sync` 也不對齊
//!   它；`undev` 解除覆寫時才依鎖定行取件（engine/dev）。
//! - `<ns>` 從本機開發來源讀：值照 engine/dev 以安裝目錄為準正規化，要存在、是目錄、每一段都不是
//!   symlink、符合交付格式、交付 `<repo>.just`（`fetch::local`）。安裝目錄外的（`dev` 收的絕對路徑，或開頭
//!   是 `..` 的相對路徑）引擎看不到，照 engine/dev 請啟動器 `stage-dir` 複製進 session 目錄的 `in/<slot>`，
//!   再讀那份複本：只複製進 session 目錄，不寫安裝目錄，`sync` 照樣唯讀於追蹤檔。救援路徑（介面版不在區間內）
//!   送不出 `stage-dir`，照讀不到處理。讀不到回 VK0052（04 本機覆寫：覆寫來源失效只擋需讀它的動作；`sync`
//!   重產入口檔要讀它），跟其他停下原因一起列出，什麼都不寫。
//! - `gen/tools.just` 那個工具的行指向本機開發來源（`tools_just::local_line`）。
//! - 每次報告用了哪個覆寫（04 本機覆寫：不加診斷前綴，`update` 以外到 stdout），沒有變更時也印。
//! - 其他工具照常依版本鎖定行判定、取件、落地。引擎的覆寫與工具同步無關，不看。
//! - 殘留的 `undev` 進度檔：04 本機覆寫說 `undev` 同步未完成時覆寫已解除、須重跑原 `undev`，`sync` 不代替
//!   完成或清掉它；訊息表 VK0053 寫的就是這件事（「sync 不代替 undev 清掉進度檔」），所以回 VK0053，
//!   `<target>` 讀進度檔 `[undev] target`、`<undev_command>` 由進度檔的 `command` 重組（engine/dev 寫的格式），
//!   在逐工具處理前停下，進度檔留著。照常同步會把入口檔指回 `cache/`，等於代替 `undev` 完成。
//!
//! # 中斷
//!
//! `sync` 不寫進度檔，中途停了也不留下要恢復的東西：`sync` 本身就是「把 `cache/`、`gen/` 對齊版本鎖定行」，
//! 再跑一次就是恢復。`txn::refresh` 先換 `cache/` 與印記、最後才寫入口檔：換到一半的 `cache/<repo>/` 會在
//! 第 5 步被印記判成不一致而重取；入口檔與 `cache/` 一新一舊時，第 8 步重產的入口檔與現有內容不同而重寫
//! （02 不變量 4：混合狀態可辨識）。
//!
//! # 殘留的進度檔
//!
//! 進度檔是可寫 recipe 未完成的操作。`sync` 不代替完成、也不清掉，在逐工具處理前停下，依訊息表報出下一步，
//! 進度檔留著（跟 engine/update 的判法一致）：
//!
//! - `add`：VK0004，`<repo>` 讀進度檔 `[add] repo`（`sync` 不代替完成導入）。
//! - 工具 `upgrade`：VK0041，`<repo>` 讀進度檔 `[upgrade] target`（格式見 `progress::upgrade`），
//!   `<original_command>` 由進度檔的 `command` 重組。
//! - `undev`：VK0053，見「本機覆寫」。
//! - 其他可寫 recipe（`remove`、`install`、`uninstall`、`dev`、`prune` 等）：VK0054，`<operation>` 是進度檔的
//!   `<verb>`，`<original_command>` 由進度檔的 `command` 重組。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 印記的位置與 `add` 共用 [`stamp::tool_file`]（`.vendor_kit/cache/<repo>.stamp.toml`）。
//! - 覆寫的報告字句與排在最前面（[`text::local_override`]）；`sync` 停下時只印診斷，不報告覆寫。
//! - 本機開發來源的正規化與檢查跟 engine/dev、engine/upgrade 共用 `fetch::local`。`<undev_command>`、
//!   `<original_command>` 的重組從 engine/update 照抄（[`full_command`]；指令之間互不依賴）。
//! - VK0006 的 `<files>` 寫成 `.vendor_kit/<檔名> (<哪一種>)`，以 `, ` 分隔，順序同 `layout::SHELL_FILES`。
//! - 取件的 slot 名是 [`SLOT_PREFIX`] 加這次執行裡的序號（`tool1`、`tool2`…）；`stage-dir` 的另外編號
//!   （`fetch::local::STAGE_SLOT_PREFIX`，`dev1`、`dev2`…）。
//! - docker `image inspect` 的輸出只讀 `Id` 與 `RepoDigests`（[`parse_inspect`]）。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - 覆寫指到不在版本鎖定行的工具（例如開著覆寫時 `git pull` 拿掉了那一行）：ADR-0002 說覆寫只覆蓋已存在
//!   的鎖定行，訊息表沒有代碼（`version_file::OrphanOverrides`），停下。
//! - 開著覆寫的工具交付保留名 `vendor_kit`，或跟其他工具撞名：沒有代碼，停下（同 engine/dev）。
//! - 殘留的引擎 `upgrade` 進度檔：VK0023 要填新引擎的 `<vY>`，`progress::upgrade` 還沒記引擎 upgrade 的
//!   欄位（`upgrade --engine` 還沒實作），停下時說明裡帶進度檔與原指令（同 engine/update）。
//! - 殘留的 `sync` 進度檔：`sync` 不寫進度檔，正常的引擎不會留下；報 VK0054 會叫使用者重跑 `sync`、
//!   而 `sync` 又清不掉它，所以停下時寫明是哪一份。
//! - 基準版落後（VK0014）：`metadata` 沒有記基準版是哪一版，判不出來；工具有 metadata 時停下。目前
//!   `add` 只在有初始檔時才寫 metadata，而 `init.toml` 格式未定，所以實際上碰不到。
//! - 取到的內容與同一版本的既有印記不符（計畫 G1：印記被改過，或同一 digest 取出不同內容），沒有代碼。
//! - dist 格式不符（G2）、工具交付保留名 `vendor_kit`、兩個工具交付同一個 `<ns>`，`sync` 都沒有代碼。
//! - 中途寫檔失敗沒有代碼（G4）。
//! - 工具 recipe 前的自動 `sync`：引擎分不出這次是不是自動觸發，警告後本體跑不跑、整次回碼見 #120。
//!
//! 這裡不直接碰 docker：docker 動作與 `stage-dir` 一律是 `plan` 協定的 op，由啟動器代做。

pub mod text;

#[cfg(test)]
mod tests;

use std::collections::BTreeMap;
use std::ffi::OsStr;
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
use plan::{Channel, ChannelError, Field, ImageId, Op, Outcome, Slot};
use shell::Shell;
use stamp::Stamp;
use txn::{Disk, ToolContent};
use version_file::{LocalFile, LockFile, Versions};

/// 這個指令的名稱；`sync` 不寫進度檔，殘留的 `sync` 進度檔見模組說明「缺口」。
pub const VERB: &str = "sync";
/// `add` 的進度檔 `<verb>` 與它記 `<repo>` 的表（engine/add 的 `VERB`、`PROGRESS_TABLE`；指令之間互不依賴，照抄）。
pub const ADD_VERB: &str = "add";
/// `undev` 的進度檔 `<verb>` 與它記 `<target>` 的鍵（engine/dev 的 `UNDEV_VERB`、`TARGET_KEY`；照抄）。
pub const UNDEV_VERB: &str = "undev";
pub const UNDEV_TARGET_KEY: &str = "target";
/// `upgrade` 的進度檔 `<verb>`（格式見 `progress::upgrade`）。
pub const UPGRADE_VERB: &str = progress::upgrade::VERB;
/// 重組指令時接在參數前面的字。
pub const COMMAND_PREFIX: [&str; 2] = ["just", "vendor_kit"];
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
    /// 蓋在 VK 檔上的寫入者，也是判薄殼時這一版薄殼標頭的引擎版。
    pub written_by: &'a str,
    /// 隨 image 出貨的薄殼四檔模板本文，順序同 [`layout::SHELL_FILES`]；`None` 是這個引擎沒有。
    pub shell_templates: Option<&'a [Vec<u8>; layout::SHELL_FILES.len()]>,
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
        stages: 0,
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

/// 開著本機覆寫的一個工具：正規化後的本機開發來源與它交付的 `<ns>`。
struct Local {
    dir: String,
    namespaces: Vec<String>,
}

/// 逐工具處理前判定的結果。
struct Judged {
    /// 沒有覆寫的工具的印記。
    stamps: BTreeMap<String, StampState>,
    /// 開著覆寫的工具。
    local: BTreeMap<String, Local>,
}

/// 取到、驗過的一個工具。
struct Fetched {
    candidate: Candidate,
    warn: Option<&'static Message>,
}

struct Sync<'r, 'a, W: Write, S: Sink, L: Write> {
    env: &'r mut Env<'a, W, S, L>,
    code: u8,
    /// 這次執行已用掉的取件 slot 數。
    extracts: u32,
    /// 這次執行已用掉的 `stage-dir` slot 數。
    stages: u32,
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
        let Judged { mut stamps, local } = self.judge(&lockfile)?;

        let mut keep: BTreeMap<String, Vec<String>> = BTreeMap::new();
        let mut fetched: Vec<Fetched> = Vec::new();
        let mut failed = false;
        for (repo, locked) in lockfile.tools() {
            if local.contains_key(repo) {
                // 開著覆寫：不取件，不看也不寫 `cache/<repo>/` 與印記（模組說明「本機覆寫」）。
                continue;
            }
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

        let entry = self.render_entry(&keep, &fetched, &local)?;
        let path = self.env.dir.gen_dir().join(txn::TOOLS_JUST);
        let current = match fs::read(&path) {
            Ok(b) => Some(b),
            Err(e) if e.kind() == io::ErrorKind::NotFound => None,
            Err(e) => return Err(self.internal(format!("{}: {e}", path.display()))),
        };
        let entry_changed = current.as_deref() != Some(entry.as_bytes());
        if fetched.is_empty() && !entry_changed {
            self.report_overrides(&local);
            return Ok(());
        }

        for f in &fetched {
            if let Err(e) = f.candidate.recheck() {
                let repo = f.candidate.repo().to_owned();
                return Err(self.internal(format!("staged content of {repo} changed: {e}")));
            }
        }
        self.land(&fetched, entry_changed.then_some(entry.as_bytes()))?;

        self.report_overrides(&local);
        for f in &fetched {
            self.say(&text::fetched(f.candidate.repo(), f.candidate.locked()));
        }
        if entry_changed {
            self.say(text::TOOLS_JUST_UPDATED);
        }
        for f in &fetched {
            if let Some(m) = f.warn {
                let d = Diagnostic::new(m).arg("repo", f.candidate.repo());
                self.emit(d);
            }
        }
        Ok(())
    }

    /// 每次報告用了哪個覆寫（04 本機覆寫）。
    fn report_overrides(&mut self, local: &BTreeMap<String, Local>) {
        for (repo, l) in local {
            self.say(&text::local_override(repo, &l.dir));
        }
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

    /// 判薄殼（模組說明第 4 步）：跟這一版的模板不符回 VK0006，判不了回 VK0056，一致回 `None`。
    fn shell(&self) -> Option<Diagnostic> {
        let Some(t) = self.env.shell_templates else {
            return Some(self.gap_diag(
                "sync without the shell templates, which this engine image does not ship",
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
            .map(|f| format!("{}/{} ({})", layout::VK_DIR, f.name, f.status))
            .collect();
        Some(Diagnostic::new(message).arg("files", files.join(", ")))
    }

    /// 逐工具處理前的判定（模組說明第 4 步）：只讀。有任何一項不能做就把每一項都印出來再停下。
    fn judge(&mut self, lockfile: &LockFile) -> Step<Judged> {
        let mut blocked: Vec<Diagnostic> = Vec::new();

        if let Some(d) = self.shell() {
            blocked.push(d);
        }

        let mut local = BTreeMap::new();
        match LocalFile::load_from(self.env.dir) {
            Ok(Some(file)) => match Versions::new(lockfile, Some(&file)) {
                Ok(_) => {
                    for (repo, source) in file.tools() {
                        match self.local_source(repo, source)? {
                            Ok(l) => {
                                local.insert(repo.clone(), l);
                            }
                            Err(d) => blocked.push(d),
                        }
                    }
                }
                Err(orphan) => {
                    blocked.push(self.gap_diag(format_args!("{orphan} (no reason code)")))
                }
            },
            Ok(None) => {}
            Err(version_file::Error::Parse {
                file,
                source: version_file::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => blocked.push(self.too_new_diag(&file, &t)),
            Err(e) => blocked.push(self.internal_diag(e.to_string())),
        }

        match progress::find(self.env.dir) {
            Ok(entries) => {
                for entry in entries {
                    blocked.push(self.residual(&entry));
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
            if local.contains_key(repo) {
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
            Ok(Judged { stamps, local })
        } else {
            for d in blocked {
                self.emit(d);
            }
            Err(Stop)
        }
    }

    /// 一個工具的本機開發來源（模組說明「本機覆寫」）：讀不到回 `Ok(Err(VK0052))`，交付保留名是缺口。
    fn local_source(&mut self, repo: &str, source: &str) -> Step<Result<Local, Diagnostic>> {
        let unreadable = |reason: String| {
            Diagnostic::new(&messages::VK0052)
                .arg("target", repo)
                .arg("source", source)
                .arg("reason", reason)
                .arg("undev_command", full_command(&["undev", repo]))
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
            return Ok(Err(self.gap_diag(format_args!(
                "sync of {repo} whose local source delivers the reserved namespace {} (no reason code)",
                fetch::RESERVED
            ))));
        }
        Ok(Ok(Local {
            dir: dir.as_str().to_owned(),
            namespaces,
        }))
    }

    /// 讀本機開發來源交付的 `<ns>`（`fetch::local::check_dir`）：安裝目錄裡的直接讀；安裝目錄外的先請
    /// 啟動器 `stage-dir` 複製進 `in/<slot>`（session 目錄，不寫安裝目錄），再讀那份複本。救援路徑送不出
    /// `stage-dir`，照讀不到處理；往返本身失敗是 VK 的錯，停下。
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
        match self.env.channel.send(&Op::StageDir(field, slot)) {
            Ok(_) => {}
            Err(ChannelError::NotRescue(_)) => {
                return Ok(Err(fetch::local::PathProblem::Unusable(
                    "it is outside the install directory, and the launcher cannot copy it on \
                     the rescue path (the interface version is not supported)"
                        .to_owned(),
                )));
            }
            Err(e) => return Err(self.internal(e.to_string())),
        }
        let reply = match self.env.channel.receive(self.env.poll) {
            Ok(r) => r,
            Err(e) => return Err(self.internal(e.to_string())),
        };
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

    /// 一份殘留的進度檔要印的診斷（模組說明「殘留的進度檔」）：一律停下，不恢復、不刪。
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
                        .arg("undev_command", full_command(loaded.command())),
                    None => self.gap_diag(format_args!(
                        "reporting the incomplete undev in {} without its [undev] {UNDEV_TARGET_KEY} field",
                        self.rel(&entry.path)
                    )),
                }
            }
            UPGRADE_VERB => match progress::upgrade::field(&loaded, progress::upgrade::TARGET) {
                Some(progress::upgrade::ENGINE_TARGET) => self.gap_diag(format_args!(
                    "reporting the incomplete engine upgrade in {} (run again: {})",
                    self.rel(&entry.path),
                    full_command(loaded.command())
                )),
                Some(repo) => Diagnostic::new(&messages::VK0041)
                    .arg("repo", repo)
                    .arg("original_command", full_command(loaded.command())),
                None => self.gap_diag(format_args!(
                    "reporting the incomplete upgrade in {} without its [upgrade] target field",
                    self.rel(&entry.path)
                )),
            },
            VERB => self.gap_diag(format_args!(
                "sync while {} remains; sync no longer writes progress files",
                self.rel(&entry.path)
            )),
            other => Diagnostic::new(&messages::VK0054)
                .arg("install_dir", self.env.host_root)
                .arg("operation", other)
                .arg("original_command", full_command(loaded.command())),
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
        local: &BTreeMap<String, Local>,
    ) -> Step<String> {
        let mut all: BTreeMap<&str, &[String]> = BTreeMap::new();
        for (repo, ns) in keep {
            all.insert(repo, ns);
        }
        let mut dirs: BTreeMap<String, String> = BTreeMap::new();
        for (repo, l) in local {
            all.insert(repo, &l.namespaces);
            dirs.insert(repo.clone(), l.dir.clone());
        }
        for f in fetched {
            all.insert(f.candidate.repo(), f.candidate.namespaces());
        }
        let tools: Vec<tools_just::Tool> = all
            .iter()
            .map(|(repo, namespaces)| tools_just::Tool { repo, namespaces })
            .collect();
        match tools_just::render_with(&tools, &dirs) {
            Ok(t) => Ok(t),
            Err(e @ tools_just::Error::Duplicate { .. }) => {
                Err(self.gap(format_args!("sync of tools whose namespaces collide ({e})")))
            }
            Err(e) => Err(self.internal(e.to_string())),
        }
    }

    /// 依序落地（[`txn::refresh`]）：`cache/` 與印記、入口檔；不建進度檔、版本鎖定行不動。
    fn land(&mut self, fetched: &[Fetched], entry: Option<&[u8]>) -> Step<()> {
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
            txn::refresh(&mut fx, &tools, entry)
        };
        result.map_err(|f| self.internal(f.to_string()))
    }
}
