//! `upgrade` 指令的工具那一半（04 指令表 `upgrade <repo>`、`upgrade <repo>@<tag>`；04 成對與無害的工具升版
//! 流程、指定版本、本機覆寫）：換工具版本，做基準版合併。`upgrade --engine` 的兩段在 [`engine`]（VK 檔格式升級
//! 在 [`migrate`]），跟這裡共用讀設定、取鎖、線上解析與 `plan` 往返。
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
//!    - 不帶 tag：工具有逐檔紀錄時先停下（判不出基準版落後，見「缺口」；04 規定基準版落後時不再查最新版，
//!      所以在連 registry 之前停）；否則這時才讀 `--registry-token-file`，向 registry 列鎖定行
//!      `<registry>/<路徑>` 的 tag，依 04 指定版本取最新版（[`imageref::Tag::latest`]）當目標（見「線上解析」）。
//!    - 目標 tag 與版本鎖定行的 tag 相同：stdout 說明未變更，以 0 結束，不送 docker 動作（04 指定版本：
//!      同一 tag 改指別的 digest 不算新版）。
//! 6. 解析目標的版本鎖定行值（見「線上解析」）：經 `plan` 協定請啟動器 `inspect` 本機 image
//!    `<registry>/<路徑>:<tag>`（registry 與路徑取自版本鎖定行），從 RepoDigests 讀 digest；本機沒有就向
//!    registry 查 tag 指向的 digest、`pull <registry>/<路徑>@<digest>` 再以同一個引用 inspect。組成新的版本
//!    鎖定行值 `<registry>/<路徑>:<tag>@<digest>`，再以 image ID `extract`；docker 動作失敗回 VK0055。
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
//! # 線上解析（N2、N53）
//!
//! registry 只經 `registry` crate（列 tag、HEAD manifest 取 `Docker-Content-Digest`），不用任何查詢快取：
//!
//! - 不帶 tag：列 tag（帶 token 時用它）→ 取最新版 → inspect 本機 `<registry>/<路徑>:<最新版>`。本機有：
//!   再以同一個查詢（沿用換到的 bearer）取 registry 上這個 tag 的 digest，跟本機的比對；本機沒有：取 digest
//!   後 pull。
//! - `@<tag>`：先 inspect 本機，本機有就用它、不連 registry（指定 tag 不查清單，也不讀 token 檔；離線照樣
//!   能用）。本機沒有才匿名取 registry 上這個 tag 的 digest，再 pull。
//! - pull 一律用帶 digest、不帶 tag 的引用 `<registry>/<路徑>@<digest>`，之後也以同一個引用 inspect：
//!   以 digest pull 的 image 不會帶上 tag，拿 `<路徑>:<tag>` 去 inspect 會找不到。
//!
//! 無法唯一判定 digest 就停下（02 不變量 12），在任何寫入之前：
//!
//! - 本機 image 的 RepoDigests 沒有這個 `<registry>/<路徑>` 的 digest（例如本機建置、從 tar 載入）：VK0031，
//!   `<image>` 是 `<registry>/<路徑>:<tag>`，`<reason>` 是 [`text::DIGEST_MISSING`]（VK0031 的情境擴到
//!   upgrade，契約文字待補）。
//! - 同一個 tag 指向不同 digest（本機 RepoDigests 有兩個以上不同的 digest，或本機的跟 registry 的不同）：
//!   拒絕。草稿碼 VK0078 還沒登錄，先以 VK0056 停下，`<reason>` 寫明各個 digest，結尾是 [`DRAFT_TAG_DIGESTS`]。
//!
//! # registry token 檔（04 registry token 檔案）
//!
//! `--registry-token-file <path>` 只在不帶 tag、真的要列 tag 時才讀，一次執行只讀一次；`@<tag>` 不讀、
//! 不送 `stage`。路徑判定照抄 engine/update（[`locate`]，只看字面正規化，相對路徑以安裝目錄為準）：
//! 落在安裝目錄裡就直接讀；在外面就請啟動器 `stage` 複製進 `in/`[`TOKEN_SLOT`] 再讀那份複本。讀不到（不存在、
//! 主機路徑放不進往返欄位、`stage` 失敗、不是 UTF-8）或去掉前後空白後是空的：VK0055，`<source>` 是使用者
//! 給的路徑，在連 registry 之前停下。往返本身出錯（寫不了 request、協定不對）是 VK 的錯，以 VK0056 停下。
//!
//! # 查詢失敗（訊息表 VK0001、VK0055、VK0058）
//!
//! `registry` 的錯誤類別照它的模組說明對應，`<target>` 是 `<repo>`：
//!
//! - 列 tag 時沒帶 token、registry 要求認證（`AuthRequired`）：VK0001，`<cmd>` 印 [`VK0001_CMD`]。
//! - 列 tag 的其他錯誤（token 被拒、網路或逾時、404、回應不合協定）：VK0055，`<source>` 是查的
//!   `<registry>/<路徑>`、`<reason>` 是 `registry` 的錯誤說明（不含 token）。被拒後不改走匿名重試。
//! - 列得到 tag、但沒有一個是合法的 `vX.Y.Z`：VK0058（情境寫的是 update，同一種情況擴到 upgrade，契約文字
//!   待補）。一個 tag 都沒有：見「缺口」。
//! - 取 tag 的 digest 失敗（含要求認證）：VK0055，`<source>` 是 `<registry>/<路徑>:<tag>`。VK0001 的下一步是
//!   「帶 token 或指定版本」，不適用於已經指定版本、或已經列過 tag 的這一步。
//!
//! # 本機覆寫
//!
//! `version.local.toml` 有工具的覆寫（`dev <repo> -p <dir>`）時照常換版（04 本機覆寫：除 `test` 外的一般
//! recipe 照常執行；ADR-0013），做法跟 engine/sync 一致：
//!
//! - 對象工具開著覆寫也照常取件、換 `cache/<repo>/`、印記與版本鎖定行：覆寫期間的內容由本機開發來源決定，
//!   `cache/<repo>/` 與鎖定行記的是鎖定版本，`undev` 之後回到換好的新版。
//! - 每個覆寫的 `<ns>` 從本機開發來源讀（`fetch::local`，值照 engine/dev 以安裝目錄為準正規化）。安裝目錄外
//!   的（`dev` 收的絕對路徑，或開頭是 `..` 的相對路徑）引擎看不到，照 engine/dev 請啟動器 `stage-dir` 複製
//!   進 session 目錄的 `in/<slot>`，再讀那份複本。讀不到回 VK0052（04 本機覆寫：覆寫來源失效只擋需讀它的
//!   動作；重產 `gen/tools.just` 要讀它），列出每個讀不到的覆寫，在任何 docker 動作與寫入之前停下。
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
//! - 取件的 slot 名是 [`SLOT_PREFIX`] 加這次執行裡的序號（`tool1`、`tool2`…）；`stage-dir` 的另外編號
//!   （`fetch::local::STAGE_SLOT_PREFIX`，`dev1`、`dev2`…）；token 檔 `stage` 的 slot 是 [`TOKEN_SLOT`]。
//! - 同一個 tag 指向不同 digest 的 `<reason>` 字句（[`text::tag_digests`]）。
//! - stdout 的字句與詢問文字（英文）見 [`text`]；覆寫的報告字句跟 engine/sync 相同（[`text::local_override`]）。
//! - 本機開發來源的正規化與檢查跟 engine/dev、engine/sync 共用 `fetch::local`。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - registry 列得到、但一個 tag 都沒有（200、清單是空的）：VK0058 只寫「有 tag 卻沒有合法 vX.Y.Z」。照
//!   engine/update 當查詢失敗，報 VK0055，`<reason>` 寫 [`text::NO_TAGS`]；之後訊息表定了再改。
//! - 不帶 tag 而 registry 的最新版比版本鎖定行舊（例如較新的 tag 被刪了）：04 只說最新版不限目前的 vX，
//!   沒說要不要因此降版，停下。
//! - 取 digest 時不檢查 manifest 的 media type 是不是多架構 index（`registry` 把判斷交給呼叫端，契約沒定）。
//! - `@<tag>` 而本機沒有、package 又是私有的：04 規定指定 tag 不讀 token 檔，匿名取 digest 會被拒，報 VK0055；
//!   pull 本身用的是主機的 Docker 認證。
//! - 帶 token 的流程還沒對私有 package 手動測過（`registry` 的缺口）。
//! - 工具不在版本鎖定行：VK0046 只寫 remove、undev、update（計畫 G5）。
//! - `<ns>` 撞名：VK0030 只寫 `add`。
//! - 判基準版落後（04：鎖定行比基準版新時，不帶 tag 的 `upgrade` 只完成鎖定行那一版的合併）：`metadata`
//!   沒有記基準版是哪一版。所以不帶 tag、或 `@<tag>` 與鎖定行同 tag，而工具有逐檔紀錄時停下；沒有紀錄的
//!   工具沒有基準版，不帶 tag 就查最新版，同 tag 就是未變更。
//! - 工具交付 `init.toml`：初始檔清單的格式沒定（同 engine/add），讀不出初始檔；沒有 `init.toml` 的工具
//!   就沒有新版初始檔。`initfiles` 判成缺口的檔（新版不再提供的除外）。
//! - 覆寫指到不在版本鎖定行的工具：ADR-0002 說覆寫只覆蓋已存在的鎖定行，訊息表沒有代碼
//!   （`version_file::OrphanOverrides`），停下（同 engine/sync）。
//! - 開著覆寫的工具的本機開發來源交付保留名 `vendor_kit`：沒有代碼，停下（同 engine/sync）。
//! - 其他已裝、沒開覆寫的工具的 `cache/<repo>/` 讀不到（N4）：撞名判定與入口檔都要它的 `<ns>`。
//!   只在真的要換版（或恢復殘留的 `upgrade`）、要讀其他工具時才讀，在落地之前收齊全部讀不到的工具
//!   一起報（`fetch::CacheCheck`）：
//!   不在的合成一則、下一步 `run just vendor_kit sync first`；讀不到或損壞的各一則、保留實際原因。
//!   兩種的草稿碼登錄前以 VK0056 停下，`<reason>` 結尾寫明草稿碼（`fetch::DRAFT_CACHE_MISSING`、
//!   `fetch::DRAFT_CACHE_UNREADABLE`）。
//! - 殘留的進度檔不是 `upgrade` 的；殘留的是引擎 upgrade；或殘留的工具 upgrade 寫過初始檔相關的檔（那次
//!   寫了哪些沒有記錄，重新判定會把它自己寫的內容當成使用者改的）。
//! - 已知偏離：恢復殘留 `upgrade` 的寫入排在這次的詢問之前，04 共同選項要先問完再寫（含恢復）。能恢復
//!   的只有沒寫初始檔的那種，恢復本身沒有要問的事；同 engine/add。
//! - 中途寫檔失敗沒有代碼（計畫 G4）；dist 格式不符（G2）、指紋不符（G1）沒有代碼。
//! - 合併結果解析不過、留了原檔的初始檔沒有訊息表代碼，對外結束碼也沒定（VK0021 說檔裡含有衝突，
//!   不能借用）：這一版只在 stdout 說明，照常以 0 結束（ADR-0003 的補寫待定）。
//!
//! 這裡不直接碰 docker：docker 動作與 `stage`、`stage-dir` 一律是 `plan` 協定的 op，由啟動器代做。

pub mod engine;
mod justfile;
pub mod migrate;
mod source;
pub mod text;
mod token;

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
use plan::{Channel, Field, ImageId, Op, Outcome, Slot, Tty};
use progress::Progress;
use progress::upgrade as table;
use prompt::{Consent, PromptError, TtyState};
use registry::{Client, ErrorKind, Repository, Token};
use runlog::Target;
use txn::{Disk, RecordFile, RepoFile, ToolContent, Txn};
use version_file::{LocalFile, LockFile, Versions};

pub use source::{Inspected, RepoDigest, digest_for, parse_inspect, repo_digest};
pub use token::{TokenPath, locate};

/// 進度檔的 `<verb>`。
pub const VERB: &str = table::VERB;
/// 取件的 slot 名前綴，後面接這次執行裡的序號（從 1 起）。
pub const SLOT_PREFIX: &str = "tool";
/// 工具交付初始檔清單的檔名（格式未定，見模組說明的缺口）。
pub const INIT_TOML: &str = "init.toml";
/// token 檔在安裝目錄外時，`stage` 放進 `in/` 的 slot 名（同 engine/update）。
pub const TOKEN_SLOT: &str = "token";
/// VK0001 的 `<cmd>`（訊息表：upgrade 時印 upgrade）。
pub const VK0001_CMD: &str = "upgrade";
/// 同一個 tag 指向不同 digest：草稿碼 VK0078（N53）登錄前，以 VK0056 停下時 `<reason>` 的結尾。
pub const DRAFT_TAG_DIGESTS: &str = "reason code pending (draft VK0078, N53)";

/// 一次 `upgrade <repo>[@<tag>] [-y] [--registry-token-file <path>]` 的參數（`args::Command::UpgradeTool`）。
#[derive(Debug, Clone, Copy)]
pub struct Request<'a> {
    pub repo: &'a str,
    pub tag: Option<Tag>,
    /// `-y`：預先同意全部詢問。
    pub yes: bool,
    /// `--registry-token-file` 的值，原樣；只在不帶 tag、要列 tag 時才讀（模組說明「registry token 檔」）。
    pub registry_token_file: Option<&'a OsStr>,
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
    /// 列 tag 與取 digest 用的 registry client（模組說明「線上解析」）。
    pub registry: &'a Client,
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
        stages: 0,
        local: BTreeMap::new(),
        engine: false,
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

/// 一個工具（或引擎）這次要換上的版本：版本鎖定行的值、image ID 與 inspect 讀到的 LABEL。
struct Resolved {
    locked: ImageRef,
    id: ImageId,
    repo_digests: Vec<String>,
    labels: BTreeMap<String, String>,
}

struct Upgrade<'r, 'a, W: Write, S: Sink, L: Write> {
    env: &'r mut Env<'a, W, S, L>,
    init: InitSource<'r>,
    code: u8,
    /// 這次執行已用掉的取件 slot 數。
    extracts: u32,
    /// 這次執行已用掉的 `stage-dir` slot 數。
    stages: u32,
    /// 開著覆寫的工具（模組說明「本機覆寫」）。
    local: BTreeMap<String, Local>,
    /// 這次是 `upgrade --engine`（[`engine`]）：列 tag 要求認證時不報 VK0001（見 [`engine`] 的「查詢失敗」）。
    engine: bool,
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

    /// 其他已裝工具的 `cache/<repo>/` 讀不到（N4）：收齊的每則 `<reason>` 各印一則 VK0056 再停下（草稿碼
    /// 登錄前的過渡做法，見 `fetch::CacheCheck`）。
    fn unready(&mut self, check: &fetch::CacheCheck) -> Stop {
        for reason in check.reasons() {
            let _ = self.internal(reason);
        }
        Stop
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
        let name = format!("{}/{}", current.registry(), current.path());
        let registry = self.env.registry;
        // 不帶 tag：先判基準版落後（判不出就停），之後才讀 token 檔、列 tag（模組說明第 5 步）。
        if req.tag.is_none() && self.meta_path(req.repo)?.exists() {
            return Err(self.gap(format_args!(
                "judging whether the baseline of {} is behind the lock version line before \
                 upgrading it to the latest version",
                req.repo
            )));
        }
        let token = match (req.tag, req.registry_token_file) {
            (None, Some(given)) => Some(self.token(given, req.repo)?),
            _ => None,
        };
        let mut listed = None;
        let tag = match req.tag {
            Some(tag) => tag,
            None => {
                let mut repo = match registry.repository(&name, token.as_ref()) {
                    Ok(r) => r,
                    Err(e) => return Err(self.list_failed(&e, &name, req.repo)),
                };
                let latest = self.latest(&mut repo, &name, req.repo)?;
                if latest < current.tag() {
                    return Err(self.gap(format_args!(
                        "upgrade {} without @<tag> when the latest version in the registry ({latest}) \
                         is older than the lock version line ({})",
                        req.repo,
                        current.tag()
                    )));
                }
                listed = Some(repo);
                latest
            }
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

        let name = format!("{}/{}", current.registry(), current.path());
        let resolved = self.resolve(&name, tag, listed.as_mut(), req.repo)?;
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
                "upgrade while the local source of {repo} delivers the reserved namespace {} \
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
        let (_, outcome) = self.request(&Op::StageDir(field, slot))?;
        match outcome {
            Outcome::Ok => Ok(fetch::local::check_dir(
                &self.env.inbox.join(&name),
                ".",
                repo,
            )),
            Outcome::Failed(rc) => Ok(Err(fetch::local::copy_failed(rc))),
            Outcome::Runner(_) => Err(self.internal("stage-dir got a runner result")),
        }
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

    /// 目標 tag 換成版本鎖定行的值（模組說明第 6 步、「線上解析」）：先 inspect 本機 image，讀 RepoDigests 的
    /// digest；`listed` 是不帶 tag 時列過 tag 的查詢，有它就再跟 registry 的 digest 比對。本機沒有就向
    /// registry 取 digest（沒有 `listed` 就匿名開一個查詢），pull 之後再 inspect。
    fn resolve(
        &mut self,
        name: &str,
        tag: Tag,
        listed: Option<&mut Repository<'_>>,
        repo: &str,
    ) -> Step<Resolved> {
        let given = format!("{name}:{tag}");
        let Some(wire) = plan::ImageRef::parse(&given) else {
            return Err(self.internal(format!("cannot inspect {given}")));
        };
        let inspected = match self.inspect(&wire)? {
            Ok(i) => i,
            Err(_) => {
                return match listed {
                    Some(online) => self.pull(online, name, tag, repo),
                    None => {
                        let registry = self.env.registry;
                        let mut online = match registry.repository(name, None) {
                            Ok(r) => r,
                            Err(e) => return Err(self.digest_failed(&e, &given, repo)),
                        };
                        self.pull(&mut online, name, tag, repo)
                    }
                };
            }
        };
        let digest = match repo_digest(name, &inspected.repo_digests) {
            RepoDigest::One(d) => d,
            RepoDigest::Missing => {
                let d = Diagnostic::new(&messages::VK0031)
                    .arg("image", given.as_str())
                    .arg("reason", text::DIGEST_MISSING);
                return Err(self.stop(d));
            }
            RepoDigest::Conflicting(found) => return Err(self.tag_digests(&given, &found)),
        };
        if let Some(online) = listed {
            let remote = self.remote_digest(online, tag, &given, repo)?;
            if remote != digest {
                return Err(self.tag_digests(&given, &[digest, remote]));
            }
        }
        self.resolved(&given, &digest, inspected)
    }

    /// 組成 [`Resolved`]：版本鎖定行值 `<given>@<digest>` 與 inspect 到的 image ID。
    fn resolved(&mut self, given: &str, digest: &str, inspected: Inspected) -> Step<Resolved> {
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
            labels: inspected.labels,
        })
    }

    /// 本機沒有目標 image：向 registry 取 tag 的 digest，`pull <name>@<digest>`，再以同一個引用 inspect
    /// （以 digest pull 的 image 不帶 tag）。
    fn pull(
        &mut self,
        online: &mut Repository<'_>,
        name: &str,
        tag: Tag,
        repo: &str,
    ) -> Step<Resolved> {
        let given = format!("{name}:{tag}");
        let digest = self.remote_digest(online, tag, &given, repo)?;
        let shown = format!("{given}@{digest}");
        let pinned = format!("{name}@{digest}");
        let Some(wire) = plan::ImageRef::parse(&pinned).filter(plan::ImageRef::is_pinned) else {
            return Err(self.internal(format!("cannot request {pinned}")));
        };
        let (_, outcome) = self.request(&Op::Pull(wire.clone()))?;
        match outcome {
            Outcome::Ok => {}
            Outcome::Failed(rc) => {
                return Err(self.access_failed(&shown, repo, text::docker_failed("pull", rc)));
            }
            Outcome::Runner(_) => return Err(self.internal("pull returned a runner result")),
        }
        let inspected = match self.inspect(&wire)? {
            Ok(i) => i,
            Err(rc) => {
                return Err(self.access_failed(&shown, repo, text::docker_failed("inspect", rc)));
            }
        };
        self.resolved(&given, &digest, inspected)
    }

    /// registry 上 `tag` 指向的 digest（`sha256:<hex>`）；失敗回 VK0055（模組說明「查詢失敗」）。
    fn remote_digest(
        &mut self,
        online: &mut Repository<'_>,
        tag: Tag,
        given: &str,
        repo: &str,
    ) -> Step<String> {
        match online.manifest(&tag) {
            Ok(m) => Ok(m.digest.to_string()),
            Err(e) => Err(self.digest_failed(&e, given, repo)),
        }
    }

    /// 同一個 tag 指向不同 digest：拒絕（草稿碼 VK0078 登錄前以 VK0056 停下）。
    fn tag_digests(&mut self, given: &str, digests: &[String]) -> Stop {
        let reason = format!("{}; {DRAFT_TAG_DIGESTS}", text::tag_digests(given, digests));
        self.internal(reason)
    }

    /// 列 tag 取最新版（模組說明「查詢失敗」）。
    fn latest(&mut self, online: &mut Repository<'_>, name: &str, repo: &str) -> Step<Tag> {
        match online.tags() {
            Ok(tags) if tags.is_empty() => {
                Err(self.access_failed(name, repo, text::NO_TAGS.to_owned()))
            }
            Ok(tags) => match Tag::latest(tags.iter().map(String::as_str)) {
                Some(latest) => Ok(latest),
                None => {
                    let d = Diagnostic::new(&messages::VK0058).arg("repo", repo);
                    Err(self.stop(d))
                }
            },
            Err(e) => Err(self.list_failed(&e, name, repo)),
        }
    }

    /// 列 tag 失敗：要求認證而沒帶 token 是 VK0001，其他是 VK0055。`upgrade --engine` 不收 token 檔，
    /// VK0001 的下一步用不上，要求認證也報 VK0055（[`engine`] 的「查詢失敗」）。
    fn list_failed(&mut self, e: &registry::Error, name: &str, repo: &str) -> Stop {
        match e.kind() {
            ErrorKind::AuthRequired if !self.engine => {
                let d = Diagnostic::new(&messages::VK0001)
                    .arg("repo", repo)
                    .arg("cmd", VK0001_CMD);
                self.stop(d)
            }
            ErrorKind::AuthRequired
            | ErrorKind::TokenRejected
            | ErrorKind::Network
            | ErrorKind::NotFound
            | ErrorKind::Protocol => self.access_failed(name, repo, e.detail().to_owned()),
        }
    }

    /// 取 digest 失敗：一律 VK0055（模組說明「查詢失敗」）。
    fn digest_failed(&mut self, e: &registry::Error, given: &str, repo: &str) -> Stop {
        self.access_failed(given, repo, e.detail().to_owned())
    }

    /// 讀 token 檔（模組說明「registry token 檔」）。讀不到印 VK0055 停下；往返本身失敗是 VK 的錯。
    fn token(&mut self, given: &OsStr, repo: &str) -> Step<Token> {
        let read = match locate(given, self.env.host_root) {
            TokenPath::Inside(rel) => Ok(self.env.dir.root().join(rel)),
            TokenPath::Outside(host) => self.stage_token(host)?,
        };
        let read = read.and_then(|path| match fs::read(&path) {
            Ok(bytes) => String::from_utf8(bytes).map_err(|_| text::TOKEN_NOT_UTF8.to_owned()),
            Err(e) => Err(text::token_unreadable(&e.to_string())),
        });
        let token = read.and_then(|s| Token::new(&s).ok_or_else(|| text::TOKEN_EMPTY.to_owned()));
        token.map_err(|reason| self.access_failed(&given.to_string_lossy(), repo, reason))
    }

    /// 請啟動器把安裝目錄外的 token 檔複製進 `in/`[`TOKEN_SLOT`]，回那份複本的路徑。
    fn stage_token(&mut self, host: Vec<u8>) -> Step<Result<PathBuf, String>> {
        let Some(slot) = Slot::parse(TOKEN_SLOT) else {
            return Err(self.internal(format!("stage slot {TOKEN_SLOT} is not a valid slot")));
        };
        let field = match Field::new(host) {
            Ok(f) => f,
            Err(e) => return Ok(Err(text::token_unpassable(&e.to_string()))),
        };
        let (_, outcome) = self.request(&Op::Stage(field, slot))?;
        match outcome {
            Outcome::Ok => Ok(Ok(self.env.inbox.join(TOKEN_SLOT))),
            Outcome::Failed(rc) => Ok(Err(text::token_copy_failed(rc))),
            Outcome::Runner(_) => Err(self.internal("stage got a runner result")),
        }
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
        let mut check = fetch::CacheCheck::default();
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
            match fetch::cached_namespaces(&cache) {
                Ok(ns) => {
                    taken.tool(other, ns.iter().cloned());
                    namespaces.insert(other.clone(), ns);
                }
                Err(e) => check.push(other, e),
            }
        }
        if !check.is_empty() {
            return Err(self.unready(&check));
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
            labels: inspected.labels,
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
