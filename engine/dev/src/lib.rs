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
//! 5. 判對象：`dev <repo>`、`undev <repo>` 的工具不在版本鎖定行回 VK0046（訊息表：先辨識未完成進度，再判斷
//!    對象不存在，所以排在第 4 步之後；`dev` 是 #372 N80 擴的情境，契約文字待補）。工具名不是合法的 just
//!    名稱已在 `args` 回 VK0026。
//! 6. 判要做什麼：
//!    - `dev <repo> -p <dir>`：已有同來源的覆寫、也沒有殘留，stdout 說明未變更；已有不同來源的覆寫回
//!      VK0050，不取代。相對路徑以安裝目錄為準（見「本機目錄」），要存在、是目錄、符合交付格式（`dist/`
//!      的形狀：`just/<ns>.just`，`<repo>.just` 必須存在，ADR-0004），否則回 VK0051。安裝目錄外的目錄
//!      先請啟動器 `stage-dir` 複製進來再驗。
//!    - `dev --engine -i <image>`：已有同一個 image 的覆寫、也沒有殘留，stdout 說明未變更；已有不同 image 的
//!      覆寫回 VK0050，不取代。否則請啟動器 `inspect` 那個 image，讀 LABEL 的介面版區間，要含薄殼的介面版
//!      才寫（見「本機引擎」）。
//!    - `undev <repo>`、`undev --engine`：沒有覆寫、也沒有殘留，stdout 說明未變更。`undev` 不讀原來源
//!      （04 本機覆寫）。
//! 7. 算出新的 `gen/tools.just`（`tools_just::render_with`）：開著覆寫的工具指向本機目錄，其他工具指向
//!    `cache/<repo>/`。`<ns>` 從各自的來源讀：其他開著覆寫的工具要讀它的本機目錄（安裝目錄外的同樣經
//!    `stage-dir`），讀不到回 VK0052（04：
//!    覆寫來源失效只擋需讀它的動作）。`dev <repo>` 的本機開發來源交付的 `<ns>` 撞到保留名 `vendor_kit` 或其他
//!    工具（開著覆寫的以本機開發來源為準）的，每個撞到的名字各回一則 VK0030（#372 N79 擴的情境，契約文字
//!    待補），在任何寫入之前停下。`undev <repo>` 的對象回到鎖定版本：`cache/<repo>/` 與印記、版本
//!    鎖定行一致就直接指回去；對不上就取件（見「取件」），入口檔照取到的內容算。`dev --engine`、
//!    `undev --engine` 不動入口檔。
//! 8. 經 `txn` 的本機覆寫順序落地：建進度檔 → 寫 `version.local.toml`（記錄檔那一步）→ 換 `cache/<repo>/` 與
//!    印記（`undev` 要取件時；其他情況是空的）→ 寫 `gen/tools.just` → 刪進度檔；不改版本鎖定行
//!    （`keep_lock_line`）。覆寫的增減排在 `cache/` 與入口檔之前：04 本機覆寫「`undev` 解除覆寫，隨即同步到
//!    當下鎖定版本」「`undev` 同步未完成時，覆寫已解除，須重跑原 `undev`」。之後才刪併入的殘留進度檔。
//!    `undev` 在覆寫已寫好、`cache/` 或入口檔還沒寫好時失敗，回 VK0053（訊息表：undev 解除覆寫後同步失敗）。
//! 9. stdout 列出改了什麼與用了哪個覆寫（04 本機覆寫：每次報告用了哪個覆寫，不加診斷前綴）。
//!
//! 這裡不直接碰 docker：往返只有安裝目錄外的本機開發來源的 `stage-dir`（不在 `plan::RESCUE_OPS`
//! 裡；`dev` 不是救援路徑）、`dev --engine` 的 `inspect`，與 `undev` 取件的 `inspect`、`pull`、`extract`。
//!
//! # 本機引擎
//!
//! `dev --engine -i <image>` 的 `<image>` 要是啟動器收的 image 引用（`plan::ImageRef`：小寫字母或數字開頭，
//! 之後是小寫字母、數字與 `._/:@-`，例如 `vendor_kit:dev` 或 image ID），否則以 VK0056 停下，不送任何 op。
//! 本機 image 不 `pull`：請啟動器 `inspect` 原樣的引用，失敗（本機沒有或 docker 出錯）以 VK0056 停下。
//! 讀 LABEL 的 [`LABEL_FLOOR`]、[`LABEL_CURRENT`]（[`protocol_range`]），缺或值不合以 VK0056 停下。
//! 區間要含這次呼叫的薄殼介面版（`plan` header 的 P，就是啟動器轉來的薄殼的 P）：
//!
//! - 區間上限低於薄殼的 P：比薄殼舊的引擎，不得用它重產進 git 的薄殼（ADR-0010），草稿碼 VK0076 登錄前以
//!   VK0056 停下，`<reason>` 結尾是 [`DRAFT_ENGINE_TOO_OLD`]。區間含薄殼的 P 的較舊引擎照樣接受（ADR-0010：
//!   允許跑，退得回）；重產薄殼的 `upgrade --engine` 第二段開著引擎覆寫時停下（engine/upgrade）。
//! - 區間下限高於薄殼的 P：見「缺口」。
//!
//! 通過才把原樣的引用寫進 `version.local.toml` 的引擎行，stdout 報告用了哪個覆寫。
//!
//! # 取件
//!
//! `undev <repo>` 時 `cache/<repo>/` 跟版本鎖定行對不上（印記不在、損壞、版本不同，或版本相同而內容不符，
//! 例如開著覆寫時 `git pull` 換了鎖定行），不叫使用者先 `sync`，解除覆寫後一起同步（04 本機覆寫）。取件照
//! engine/sync 的做法（指令之間互不依賴，照抄）：請啟動器 `inspect` 帶 digest 的引用
//! `<registry>/<路徑>@<digest>`，本機沒有就 `pull` 同一個引用再 `inspect`，再以 image ID `extract` 進
//! `in/<slot>`；`fetch::verify` 驗 RepoDigests、交付格式，版本相同時另比對既有印記的逐檔指紋。取件在寫任何檔
//! 之前做，取到 repo 外的暫存處（#372 取件時機），落地前重驗（ADR-0006 第三層），`txn` 在解除覆寫之後才換
//! `cache/` 與印記、再寫入口檔。
//!
//! 取件失敗也回 VK0053：docker 動作失敗或下載的內容與鎖定的 digest 不符時，訊息表的 VK0055、VK0043 只寫
//! update、add、upgrade、sync，`undev` 的同步失敗只有 VK0053（「請再執行一次」）。這時還沒寫任何檔，覆寫
//! 照留、沒有進度檔，重跑同一個 `undev` 就是從頭再做。重跑也補不好的（取到的內容與同一版本的既有印記不符、
//! 交付格式不符、交付保留名 `vendor_kit`）見「缺口」。
//!
//! # 本機目錄
//!
//! `-p <dir>` 只看字面逐段正規化（[`normalize`]；`.` 略過，`..` 往上一層），正規化後的值存進
//! `version.local.toml`，入口檔照同一個值指過去（`tools_just::local_line`）。重複 `dev` 是不是同來源，比的是
//! 正規化後的值。正規化與檢查跟 engine/sync、engine/upgrade 共用 `fetch::local`。三種結果（[`Source`]）：
//!
//! - 落在安裝目錄裡：相對路徑沒跑出安裝目錄，或絕對路徑在 `--host-root` 底下。寫成 `/` 分隔的相對路徑
//!   （整個是安裝目錄本身時寫 `.`）。引擎直接讀 `plan::mount::ROOT` 底下那個目錄；路徑上有 symlink（容器裡
//!   解不出主機上的目標）見「缺口」。
//! - 相對路徑以 `..` 跑出安裝目錄：寫成開頭是 `..` 的相對路徑（例如 `../tool`），照使用者給的形式留相對
//!   路徑，安裝目錄跟它一起搬時仍指得到。
//! - 絕對路徑、不在 `--host-root` 底下：寫成正規化後的絕對路徑。
//!
//! 後兩種引擎容器看不到，請啟動器 `stage-dir` 把目錄複製進 `in/<slot>`（slot 是 `dev1`、`dev2`…，每次執行
//! 各自編號），在那份複本上驗交付格式、讀 `<ns>`。送給啟動器的主機路徑：絕對路徑原樣；相對路徑是
//! `<--host-root>/<值>`，開頭的 `..` 不在引擎這邊消掉，跟 just 從 `.vendor_kit/gen/` 解析入口檔那一行一樣，
//! 都由主機照實際目錄解析，驗的跟載入的是同一個目錄。啟動器回 `failed` 時分不出是不存在、不是目錄還是讀
//! 不到，VK0051 的 `<reason>` 照實寫三者之一。
//!
//! 值不是 UTF-8，或含 `'`、`"`、反斜線、控制字元（放不進 just 單引號字串或 `version.local.toml` 的無跳脫
//! 字串），或正規化後是主機的根目錄 `/`：不猜跳脫（02 不變量 12），見「缺口」。
//!
//! # 恢復
//!
//! 殘留的 `dev`、`undev` 進度檔記了對象（`[<verb>] target`；工具的 `dev` 另記正規化後的 `path`，引擎的
//! `dev` 另記 `image`）。對象跟這次相同的併進這次：先照殘留的那次把覆寫在記憶體裡補成做完的樣子（`dev`
//! 設成它的 `path` 或 `image`，`undev` 拿掉），再照
//! 這次的參數判定，落地時一起寫，這次落地完成之後才刪殘留的那幾份，中途再斷也還認得出來。有殘留時即使沒有
//! 要改的，也走一次 `txn`，讓刪除排在 `writes_started` 之後。
//!
//! 不能併入的殘留不恢復、不刪，依訊息表報出下一步（#372 N81 擴的情境，契約文字待補）：
//!
//! - 對象不同的 `undev`：VK0053，`<target>` 讀進度檔 `[undev] target`，`<undev_command>` 由進度檔的
//!   `command` 重組。
//! - 對象不同的 `dev`，或其他可寫 recipe（`remove`、`install`、`uninstall`、`prune` 等）：VK0054，
//!   `<operation>` 是進度檔的 `<verb>`，`<original_command>` 由進度檔的 `command` 重組。
//! - `add`、`upgrade`、`sync`：見「缺口」。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 進度檔 `.tmp.<verb>.<run-id>.toml` 另記 `[<verb>]` 表的 `target`（工具名，引擎是 [`ENGINE_TARGET`]）、
//!   工具 `dev` 的 `path` 與引擎 `dev` 的 [`IMAGE_KEY`]。`update` 偵測到殘留的 `undev` 時，VK0053 的 `<target>` 讀這個欄位。
//! - VK0050、VK0052、VK0053 的 `<target>`：工具填 `<repo>`，引擎填 [`ENGINE_TARGET`]。
//! - 覆寫全部解除後 `version.local.toml` 照留（只剩檔案版與寫入者），不刪。
//! - stdout 的字句見 [`text`]。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - `dev --engine -i <image>`：引用不合法、`inspect` 失敗、LABEL 缺或值不合都沒有代碼；本機 image 的介面版
//!   區間下限高於薄殼的 P（比薄殼新一個 X 的引擎）沒定要怎麼報，訊息表 VK0009 的下一步與 `<vY>` 不適用。
//!   比薄殼舊的引擎見「本機引擎」。啟動器套用引擎覆寫（讀 `version.local.toml` 的引擎行）不在這裡。
//! - `-p` 指到安裝目錄裡、路徑上有 symlink；或路徑不是 UTF-8、含 `'`、`"`、反斜線、控制字元，或是根目錄
//!   `/`：見「本機目錄」，停下。
//! - `dev` 的 `<ns>` 撞名不比對根 `justfile` 的 recipe 與 module。其他工具之間本來就撞名（跟這次開覆寫的
//!   工具無關）沒有代碼，停下。
//! - `undev <repo>` 取到的內容與同一版本的既有印記不符（計畫 G1）、交付格式不符（G2），或交付保留名
//!   `vendor_kit`：重跑也補不好，VK0053 的「請再執行一次」不適用，在寫任何檔之前停下（同 engine/sync）。
//! - 其他沒開覆寫的工具的 `cache/<repo>/` 讀不到（N4）：重產入口檔要用到它的 `<ns>`。
//!   只在要重產入口檔時讀，在任何寫入之前收齊全部讀不到的工具一起報（`fetch::CacheCheck`）：
//!   不在的合成一則、下一步 `run just vendor_kit sync first`；讀不到或損壞的各一則、保留實際原因。
//!   兩種的草稿碼登錄前以 VK0056 停下，`<reason>` 結尾寫明草稿碼（`fetch::DRAFT_CACHE_MISSING`、
//!   `fetch::DRAFT_CACHE_UNREADABLE`）。
//!   `undev` 不另加檢查；它要重產入口檔時讀不到同樣停下，訊息相同。
//! - 殘留的進度檔是 `add`、`upgrade`（工具或引擎）或 `sync` 的：VK0054 的情境排除未完成導入與 `upgrade`，
//!   而 VK0004、VK0041、VK0023 只寫唯讀 recipe；`sync` 不寫進度檔。
//! - 中途寫檔失敗沒有代碼（G4），`undev` 解除覆寫後的那一段（換 `cache/`、寫入口檔、刪進度檔）除外
//!   （VK0053）。

pub mod text;

#[cfg(test)]
mod tests;

use std::collections::BTreeMap;
use std::ffi::OsStr;
use std::fs;
use std::io::{self, Write};
use std::path::Path;
use std::time::Duration;

use config::{Config, ConfigError};
use diagnostics::{Diagnostic, Diagnostics, Message, Sink};
use fetch::{Candidate, Staged, Taken};
use filelock::{Lock, Mode};
use imageref::ImageRef;
use layout::InstallDir;
use plan::{Channel, Field, ImageId, Op, Outcome, Slot};
use progress::Progress;
use stamp::Stamp;
use txn::{Disk, RecordFile, ToolContent, Txn};
use version_file::{LocalFile, LockFile};

/// `dev` 的進度檔 `<verb>`。
pub const DEV_VERB: &str = "dev";
/// `undev` 的進度檔 `<verb>`。
pub const UNDEV_VERB: &str = "undev";
/// 進度檔 `[<verb>]` 表裡記對象的鍵。
pub const TARGET_KEY: &str = "target";
/// `dev` 的進度檔 `[dev]` 表裡記正規化後本機目錄的鍵。
pub const PATH_KEY: &str = "path";
/// `dev --engine` 的進度檔 `[dev]` 表裡記本機 image 的鍵。
pub const IMAGE_KEY: &str = "image";
/// 引擎 image 公告最低介面版的 LABEL（engine/compat 的 `image_build_args`、image/Dockerfile；照抄
/// engine/upgrade 的同名常數，指令之間互不依賴）。
pub const LABEL_FLOOR: &str = "vendor_kit.protocol.floor";
/// 引擎 image 公告目前介面版的 LABEL。
pub const LABEL_CURRENT: &str = "vendor_kit.protocol.current";
/// 本機 image 的介面版區間上限低於薄殼的介面版（比薄殼舊的引擎，ADR-0010）時 VK0056 的 `<reason>` 結尾：
/// 訊息表草稿 VK0076（薄殼介面版比引擎新）登錄前的過渡做法。
pub const DRAFT_ENGINE_TOO_OLD: &str = "reason code pending (draft VK0076, N55)";
/// 引擎當對象時的 `<target>`（與 `update` 結果行的引擎名欄相同）。
pub const ENGINE_TARGET: &str = "vendor_kit";
/// 重組指令時接在參數前面的字。
pub const COMMAND_PREFIX: [&str; 2] = ["just", "vendor_kit"];
/// `undev` 取件 `extract` 進 `in/` 的 slot 名前綴，後接這次執行裡的序號（`tool1`…；同 engine/sync）。
pub const FETCH_SLOT_PREFIX: &str = "tool";
/// 殘留時不報 VK0054 的 `<verb>`（訊息表 VK0054 排除未完成導入與工具、引擎 `upgrade`；`sync` 不寫進度檔），
/// 見模組說明的缺口。
const NOT_VK0054: [&str; 3] = ["add", "upgrade", "sync"];
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

/// 這次執行的環境。`dev`、`undev` 不詢問，所以沒有 stdin 與終端狀態；往返只用來 `stage-dir` 與 `undev`
/// 的取件。
pub struct Env<'a, W: Write, S: Sink, L: Write> {
    /// 容器內的安裝目錄（`plan::mount::ROOT`）。
    pub dir: &'a InstallDir,
    /// 主機上的安裝目錄，填 `<install_dir>`；也是相對路徑的基準。
    pub host_root: &'a str,
    /// 容器內的收件目錄（`plan::mount::IN`）。
    pub inbox: &'a Path,
    pub channel: &'a mut Channel,
    /// 等 result 時多久看一次。
    pub poll: Duration,
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
    let mut dev = Dev {
        env,
        code: 0,
        slots: 0,
        extracts: 0,
    };
    let _ = dev.run(req);
    dev.code
}

/// `docker image inspect` 輸出裡用得到的兩個欄位。
#[derive(Debug, Clone, PartialEq, Eq)]
struct Inspected {
    /// `Id`：`sha256:<64hex>`。
    id: String,
    /// `RepoDigests`：每筆 `<registry>/<路徑>@sha256:<digest>`。
    repo_digests: Vec<String>,
    /// `Config.Labels`；沒有或是 `null` 時是空的。
    labels: BTreeMap<String, String>,
}

/// 解析 `docker image inspect <ref>` 的 JSON：一個陣列，剛好一個物件（engine/sync 的 `parse_inspect`；
/// 指令之間互不依賴，照抄）。
fn parse_inspect(bytes: &[u8]) -> Result<Inspected, String> {
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
    let labels = match item.get("Config").and_then(|c| c.get("Labels")) {
        None | Some(serde_json::Value::Null) => BTreeMap::new(),
        Some(v) => v
            .as_object()
            .ok_or("image inspect Config.Labels is not an object")?
            .iter()
            .map(|(k, v)| {
                v.as_str()
                    .map(|v| (k.clone(), v.to_owned()))
                    .ok_or("image inspect Config.Labels has a non-string value")
            })
            .collect::<Result<_, _>>()?,
    };
    Ok(Inspected {
        id,
        repo_digests,
        labels,
    })
}

/// 本機引擎 image 的 LABEL 公告的介面版區間 `(floor, current)`；缺 LABEL 或值不合回說明（判法照抄
/// engine/upgrade 的 `target_compat`：十進位、不帶前導零、floor 不高於 current）。不看
/// `org.opencontainers.image.version`：本機 build 的 image 沒有對應的 tag。
pub fn protocol_range(
    image: &str,
    labels: &BTreeMap<String, String>,
) -> Result<(u32, u32), String> {
    let number = |key: &str| -> Result<u32, String> {
        let value = labels
            .get(key)
            .ok_or_else(|| format!("the local engine image {image} has no {key} label"))?;
        let ok = !value.is_empty()
            && value.bytes().all(|b| b.is_ascii_digit())
            && !value.starts_with('0');
        let n = ok.then(|| value.parse::<u32>().ok()).flatten();
        n.ok_or_else(|| format!("the local engine image {image} has {key}={value:?}"))
    };
    let floor = number(LABEL_FLOOR)?;
    let current = number(LABEL_CURRENT)?;
    if floor > current {
        return Err(format!(
            "the local engine image {image} has {LABEL_FLOOR}={floor} above {LABEL_CURRENT}={current}"
        ));
    }
    Ok((floor, current))
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

pub use fetch::local::{PathProblem, STAGE_SLOT_PREFIX, Source, check_dir, normalize};

/// 診斷已印、這次執行停下。
struct Stop;

type Step<T> = Result<T, Stop>;

/// 併進這次的一份殘留進度檔。
struct Residual {
    entry: progress::Entry,
    /// `dev` 記的值：工具是正規化後的本機目錄，引擎是本機 image；`undev` 是 `None`。
    value: Option<String>,
}

/// `undev <repo>` 的對象 `cache/<repo>/` 跟版本鎖定行比的結果。
enum Cached {
    /// 一致：`cache/<repo>/` 交付的 `<ns>`。
    Keep(Vec<String>),
    /// 對不上，要取件；`previous` 是同一個版本的既有印記（內容不符時），取到的要跟它一致。
    Fetch { previous: Option<Box<Stamp>> },
}

/// 判定後要落地的內容。
struct Plan {
    /// 新的 `version.local.toml`；`None` 表示覆寫不變。
    local: Option<LocalFile>,
    /// 新的 `gen/tools.just`；`None` 表示入口檔不變。
    entry: Option<String>,
    /// `undev <repo>` 取到、要換進 `cache/<repo>/` 的內容。
    fetched: Option<Candidate>,
    /// 落地後要印的字句（不含入口檔與恢復）。
    said: Vec<String>,
}

struct Dev<'r, 'a, W: Write, S: Sink, L: Write> {
    env: &'r mut Env<'a, W, S, L>,
    code: u8,
    /// 這次執行已用掉的 `stage-dir` slot 數。
    slots: usize,
    /// 這次執行已用掉的取件 slot 數。
    extracts: usize,
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
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        let lockfile = self.lockfile()?;
        let disk = self.local_file()?;
        let residual = self.residuals(req)?;

        let mut local = disk.clone().unwrap_or_default();
        for r in &residual {
            let applied = match (&r.value, req.target()) {
                (Some(image), ENGINE_TARGET) => local.set_engine(image),
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
                    fetched: None,
                    said,
                }
            }
            Request::DevEngine { image } => self.dev_engine(&mut local, image, recovering)?,
        };

        // 覆寫的實際內容跟檔上一樣就不寫（殘留併進來時，記憶體裡的可能已經跟檔上不同）。
        let local = plan.local.filter(|l| !same_overrides(l, disk.as_ref()));
        if local.is_none() && plan.entry.is_none() && plan.fetched.is_none() && residual.is_empty()
        {
            for line in &plan.said {
                self.say(line);
            }
            return Ok(());
        }

        if let Some(c) = &plan.fetched
            && let Err(e) = c.recheck()
        {
            let repo = c.repo().to_owned();
            return Err(self.internal(format!("staged content of {repo} changed: {e}")));
        }
        self.land(req, local, plan.entry.as_deref(), plan.fetched.as_ref())?;
        for r in &residual {
            if let Err(err) = progress::delete(self.env.dir, &r.entry.verb, &r.entry.id) {
                let d = self.failed_diag(&r.entry.path, err.message(), err.to_string());
                return Err(self.stop(d));
            }
        }

        for line in &plan.said {
            self.say(line);
        }
        if let Some(c) = &plan.fetched {
            self.say(&text::fetched(c.repo(), c.locked()));
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
            let d = Diagnostic::new(&messages::VK0046).arg("repo", repo);
            return Err(self.stop(d));
        }
        let shown = path.to_string_lossy().into_owned();
        let unusable = |reason: String| {
            Diagnostic::new(&messages::VK0051)
                .arg("path", shown.as_str())
                .arg("repo", repo)
                .arg("reason", reason)
        };
        let source = match normalize(path, self.env.host_root) {
            Ok(d) => d,
            Err(PathProblem::Unusable(reason)) => return Err(self.stop(unusable(reason))),
            Err(PathProblem::Gap(what)) => return Err(self.gap(what)),
        };
        let dir = source.as_str().to_owned();
        if let Some(current) = local.tool(repo) {
            let current_norm = normalize(OsStr::new(current), self.env.host_root).ok();
            if current_norm.as_ref().map(Source::as_str) == Some(dir.as_str()) {
                // 重複 `dev` 同來源：04 只要求 stdout 說明未變更，入口檔不另修。併進殘留的 `dev` 時
                // 覆寫可能還沒寫進檔、入口檔也可能還沒指過去，照常算。
                if !recovering {
                    return Ok(Plan {
                        local: None,
                        entry: None,
                        fetched: None,
                        said: vec![text::dev_unchanged(repo, &dir)],
                    });
                }
                let entry = self.entry_if_changed(lockfile, local, None, None)?;
                return Ok(Plan {
                    local: Some(local.clone()),
                    entry,
                    fetched: None,
                    said: vec![text::dev_enabled(repo, &dir)],
                });
            }
            let d = Diagnostic::new(&messages::VK0050)
                .arg("target", repo)
                .arg("undev_command", undev_command(repo));
            return Err(self.stop(d));
        }
        let ns = match self.read_source(&source, repo)? {
            Ok(ns) => ns,
            Err(PathProblem::Unusable(reason)) => return Err(self.stop(unusable(reason))),
            Err(PathProblem::Gap(what)) => return Err(self.gap(what)),
        };
        if let Err(e) = local.set_tool(repo, &dir) {
            return Err(self.internal(e.to_string()));
        }
        let mut known = BTreeMap::new();
        known.insert(repo.to_owned(), ns);
        let entry = self.entry_if_changed(lockfile, local, Some(known), Some(repo))?;
        Ok(Plan {
            local: Some(local.clone()),
            entry,
            fetched: None,
            said: vec![text::dev_enabled(repo, &dir)],
        })
    }

    /// `dev --engine -i <image>` 的判定（模組說明第 6 步與「本機引擎」）。
    fn dev_engine(&mut self, local: &mut LocalFile, image: &OsStr, recovering: bool) -> Step<Plan> {
        let Some(wire) = image.to_str().and_then(plan::ImageRef::parse) else {
            let shown = image.to_string_lossy().into_owned();
            return Err(self.internal(format!(
                "the local engine image {shown:?} is not a valid image reference"
            )));
        };
        let image = wire.as_str().to_owned();
        if let Some(current) = local.engine() {
            if current == image {
                if !recovering {
                    return Ok(Plan {
                        local: None,
                        entry: None,
                        fetched: None,
                        said: vec![text::dev_engine_unchanged(&image)],
                    });
                }
                return Ok(Plan {
                    local: Some(local.clone()),
                    entry: None,
                    fetched: None,
                    said: vec![text::dev_engine_enabled(&image)],
                });
            }
            let d = Diagnostic::new(&messages::VK0050)
                .arg("target", ENGINE_TARGET)
                .arg("undev_command", undev_command(ENGINE_TARGET));
            return Err(self.stop(d));
        }
        let inspected = match self.inspect(&wire)? {
            Ok(i) => i,
            Err(rc) => {
                return Err(self.internal(format!(
                    "the launcher could not inspect the local engine image {image} (exit {rc}): \
                     it does not exist locally or docker failed"
                )));
            }
        };
        let (floor, current) =
            protocol_range(&image, &inspected.labels).map_err(|r| self.internal(r))?;
        let shell = self.env.channel.header().protocol();
        if shell > current {
            return Err(self.internal(format!(
                "the local engine image {image} accepts interface versions [{floor}, {current}], \
                 older than the shell interface version {shell}, and must not regenerate the shell; \
                 {DRAFT_ENGINE_TOO_OLD}"
            )));
        }
        if shell < floor {
            return Err(self.gap(format_args!(
                "dev --engine with the local engine image {image} whose interface versions \
                 [{floor}, {current}] are all newer than the shell interface version {shell}"
            )));
        }
        if let Err(e) = local.set_engine(&image) {
            return Err(self.internal(e.to_string()));
        }
        Ok(Plan {
            local: Some(local.clone()),
            entry: None,
            fetched: None,
            said: vec![text::dev_engine_enabled(&image)],
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
                fetched: None,
                said: vec![text::undev_tool_unchanged(repo)],
            });
        }
        let (ns, fetched) = match self.locked_cache(repo, locked)? {
            Cached::Keep(ns) => (ns, None),
            Cached::Fetch { previous } => {
                let c = self.fetch(repo, locked, previous.as_deref())?;
                (c.namespaces().to_vec(), Some(c))
            }
        };
        if let Err(e) = local.remove_tool(repo) {
            return Err(self.internal(e.to_string()));
        }
        let mut known = BTreeMap::new();
        known.insert(repo.to_owned(), ns);
        let entry = self.entry_if_changed(lockfile, local, Some(known), None)?;
        Ok(Plan {
            local: Some(local.clone()),
            entry,
            fetched,
            said: vec![text::undev_tool(repo, locked)],
        })
    }

    /// `undev <repo>` 的對象回到鎖定版本：`cache/<repo>/` 要與印記一致，印記的版本要是版本鎖定行的值，
    /// 否則要取件（模組說明「取件」；判法同 engine/sync）。
    fn locked_cache(&mut self, repo: &str, locked: &ImageRef) -> Step<Cached> {
        let fetch = Cached::Fetch { previous: None };
        let stamp = match Stamp::load(&stamp::tool_file(self.env.dir, repo)) {
            Ok(Some(s)) if s.version() == locked.to_string() => s,
            Ok(_) | Err(stamp::Error::Corrupt { .. }) => return Ok(fetch),
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
            Ok(_) => {
                return Ok(Cached::Fetch {
                    previous: Some(Box::new(stamp)),
                });
            }
            Err(e) => return Err(self.internal(format!("cache of {repo}: {e}"))),
        }
        fetch::namespaces(&cache).map(Cached::Keep).map_err(|e| {
            self.internal(format!(
                "cache of {repo} matches its stamp, but its tool content is invalid: {e}"
            ))
        })
    }

    /// 請啟動器做一個 docker 動作，等結果。
    fn request(&mut self, op: &Op) -> Step<(plan::Seq, Outcome)> {
        let sent = self.env.channel.send(op);
        let seq = sent.map_err(|e| self.internal(e.to_string()))?;
        let reply = self.env.channel.receive(self.env.poll);
        let reply = reply.map_err(|e| self.internal(e.to_string()))?;
        Ok((seq, reply.outcome))
    }

    /// VK0053：`undev` 的同步沒完成（模組說明「取件」），請再執行一次原指令。
    fn incomplete(&mut self, target: &str) -> Stop {
        let d = Diagnostic::new(&messages::VK0053)
            .arg("target", target)
            .arg("undev_command", full_command(self.env.argv));
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

    /// 依版本鎖定行取件並驗證（模組說明「取件」）：docker 動作失敗與 digest 不符回 VK0053。
    fn fetch(
        &mut self,
        repo: &str,
        locked: &ImageRef,
        previous: Option<&Stamp>,
    ) -> Step<Candidate> {
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
                    Outcome::Failed(_) => return Err(self.incomplete(repo)),
                    Outcome::Runner(_) => {
                        return Err(self.internal("pull returned a runner result"));
                    }
                }
                match self.inspect(&wire)? {
                    Ok(i) => i,
                    Err(_) => return Err(self.incomplete(repo)),
                }
            }
        };
        let Some(id) = ImageId::parse(&inspected.id) else {
            return Err(self.internal(format!("image inspect returned Id {:?}", inspected.id)));
        };

        self.extracts += 1;
        let slot = format!("{FETCH_SLOT_PREFIX}{}", self.extracts);
        let Some(slot_v) = Slot::parse(&slot) else {
            return Err(self.internal(format!("invalid slot {slot}")));
        };
        let (_, outcome) = self.request(&Op::Extract(id, slot_v))?;
        match outcome {
            Outcome::Ok => {}
            Outcome::Failed(_) => return Err(self.incomplete(repo)),
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
            Err(fetch::Error::DigestMismatch { .. }) => Err(self.incomplete(repo)),
            Err(fetch::Error::Collision { .. }) => Err(self.gap(format_args!(
                "undev of {repo}, whose locked version delivers the reserved namespace {}",
                fetch::RESERVED
            ))),
            Err(fetch::Error::Fingerprint(_)) => Err(self.gap(format_args!(
                "undev of {repo} whose fetched content does not match its existing stamp \
                 for the same lock version line"
            ))),
            Err(e) => Err(self.gap(format_args!(
                "undev of {repo} whose fetched tool content is invalid ({e})"
            ))),
        }
    }

    /// 依覆寫算出新的 `gen/tools.just`（模組說明第 7 步），跟現有內容一樣回 `None`。`known` 是這次已經讀過
    /// `<ns>` 的工具。`collide` 是這次開覆寫的工具：它的 `<ns>` 撞到保留名或其他工具的，每個各印一則 VK0030
    /// 再停下。
    fn entry_if_changed(
        &mut self,
        lockfile: &LockFile,
        local: &LocalFile,
        known: Option<BTreeMap<String, Vec<String>>>,
        collide: Option<&str>,
    ) -> Step<Option<String>> {
        let mut known = known.unwrap_or_default();
        let mut dirs: BTreeMap<String, Source> = BTreeMap::new();
        let mut blocked: Vec<Diagnostic> = Vec::new();
        let mut check = fetch::CacheCheck::default();
        for repo in lockfile.tools().keys() {
            let source = local.tool(repo);
            if let Some(source) = source {
                match normalize(OsStr::new(source), self.env.host_root) {
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
            let ns = match dirs.get(repo).cloned() {
                Some(dir) => match self.read_source(&dir, repo)? {
                    Ok(ns) => ns,
                    Err(PathProblem::Unusable(reason) | PathProblem::Gap(reason)) => {
                        let source = source.unwrap_or(dir.as_str()).to_owned();
                        blocked.push(self.unreadable(repo, &source, reason));
                        continue;
                    }
                },
                None => {
                    let cache = match self.env.dir.tool_cache(repo) {
                        Ok(c) => c,
                        Err(e) => return Err(self.internal(e.to_string())),
                    };
                    match fetch::cached_namespaces(&cache) {
                        Ok(ns) => ns,
                        Err(e) => {
                            check.push(repo, e);
                            continue;
                        }
                    }
                }
            };
            known.insert(repo.clone(), ns);
        }
        for reason in check.reasons() {
            blocked.push(self.internal_diag(reason));
        }
        if !blocked.is_empty() {
            for d in blocked {
                self.emit(d);
            }
            return Err(Stop);
        }
        if let Some(target) = collide
            && let Some(wanted) = known.get(target)
        {
            let mut taken = Taken::new();
            for (other, ns) in known.iter().filter(|(r, _)| r.as_str() != target) {
                taken.tool(other, ns.iter().cloned());
            }
            let collisions = taken.collisions(target, wanted);
            if !collisions.is_empty() {
                for c in collisions {
                    let d = Diagnostic::new(&messages::VK0030)
                        .arg("repo", target)
                        .arg("ns", c.ns)
                        .arg("owner", c.owner.to_string());
                    self.emit(d);
                }
                return Err(Stop);
            }
        }
        let tools: Vec<tools_just::Tool> = known
            .iter()
            .filter(|(repo, _)| lockfile.tool(repo).is_some())
            .map(|(repo, ns)| tools_just::Tool {
                repo,
                namespaces: ns,
            })
            .collect();
        let dirs: BTreeMap<String, String> = dirs
            .into_iter()
            .map(|(repo, dir)| (repo, dir.as_str().to_owned()))
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

    /// 讀本機開發來源交付的 `<ns>`（`check_dir`）：安裝目錄裡的直接讀；安裝目錄外的先請啟動器
    /// `stage-dir` 複製進 `in/<slot>`，再讀那份複本。往返本身失敗是 VK 的錯，停下。
    fn read_source(
        &mut self,
        source: &Source,
        repo: &str,
    ) -> Step<Result<Vec<String>, PathProblem>> {
        let Some(host) = source.host_path(self.env.host_root) else {
            return Ok(check_dir(self.env.dir.root(), source.as_str(), repo));
        };
        self.slots += 1;
        let name = format!("{STAGE_SLOT_PREFIX}{}", self.slots);
        let Some(slot) = Slot::parse(&name) else {
            return Err(self.internal(format!("stage-dir slot {name} is not a valid slot")));
        };
        let field = match Field::new(host.into_bytes()) {
            Ok(f) => f,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let sent = self.env.channel.send(&Op::StageDir(field, slot));
        if let Err(e) = sent {
            return Err(self.internal(e.to_string()));
        }
        let reply = match self.env.channel.receive(self.env.poll) {
            Ok(r) => r,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        match reply.outcome {
            Outcome::Ok => Ok(check_dir(&self.env.inbox.join(&name), ".", repo)),
            Outcome::Failed(rc) => Ok(Err(fetch::local::copy_failed(rc))),
            Outcome::Runner(_) => Err(self.internal("stage-dir got a runner result")),
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

    /// 經 `txn` 的本機覆寫順序落地（模組說明第 8 步）。
    fn land(
        &mut self,
        req: &Request<'_>,
        local: Option<LocalFile>,
        entry: Option<&str>,
        fetched: Option<&Candidate>,
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
        if let Request::DevEngine { .. } = req
            && let Some(image) = local.as_ref().and_then(LocalFile::engine)
        {
            fields.push((IMAGE_KEY, image.to_owned()));
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
        let stamp_file = fetched.map(|c| stamp::tool_file(self.env.dir, c.repo()));
        let tools: Vec<ToolContent> = fetched
            .zip(stamp_file.as_deref())
            .map(|(c, stamp_file)| ToolContent {
                repo: c.repo(),
                staged: c.root(),
                version: c.version(),
                stamp_file,
            })
            .into_iter()
            .collect();
        let result = {
            let mut fx = Disk::new(self.env.dir, self.env.log, self.env.written_by);
            Txn::begin(&mut fx, progress).and_then(|t| {
                t.write_overrides(&records)?
                    .swap_cache(&tools)?
                    .write_tools_just(entry.map(str::as_bytes))?
                    .keep_lock_line()
                    .complete()
            })
        };
        let order = &txn::Step::OVERRIDE;
        let records_at = txn::Step::Records.position(order);
        match result {
            Ok(_) => Ok(()),
            // 覆寫已經解除、`cache/`、入口檔或完成點沒寫好：訊息表的「undev 解除覆寫後同步失敗」。
            Err(f)
                if req.verb() == UNDEV_VERB
                    && f.step.position(order) > records_at
                    && !f.step.completed() =>
            {
                Err(self.incomplete(req.target()))
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
        if NOT_VK0054.contains(&verb) {
            return Err(self.gap_diag(format_args!(
                "{} while the incomplete {verb} operation in {shown} remains",
                req.verb()
            )));
        }
        if verb != DEV_VERB && verb != UNDEV_VERB {
            return Err(self.other_operation(verb, &loaded));
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
            if verb == UNDEV_VERB {
                return Err(Diagnostic::new(&messages::VK0053)
                    .arg("target", target)
                    .arg("undev_command", full_command(loaded.command())));
            }
            return Err(self.other_operation(verb, &loaded));
        }
        let value = if verb == DEV_VERB {
            let key = if target == ENGINE_TARGET {
                IMAGE_KEY
            } else {
                PATH_KEY
            };
            match field(key) {
                Some(v) => Some(v),
                None => {
                    return Err(self.gap_diag(format_args!(
                        "recovering the incomplete dev in {shown} without its [dev] {key} field"
                    )));
                }
            }
        } else {
            None
        };
        Ok(Residual { entry, value })
    }

    /// VK0054：不能併進這次的殘留（其他可寫 recipe 的，或對象不同的 `dev`），下一步是重跑原指令。
    fn other_operation(&self, verb: &str, loaded: &Progress) -> Diagnostic {
        Diagnostic::new(&messages::VK0054)
            .arg("install_dir", self.env.host_root)
            .arg("operation", verb)
            .arg("original_command", full_command(loaded.command()))
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
