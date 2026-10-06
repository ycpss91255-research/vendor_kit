//! `upgrade --engine` 的兩段（04 指令表 `upgrade --engine`、`upgrade --engine=<tag>`；04 upgrade --engine、
//! 指定版本；訊息表 VK0007、VK0023；flow-engine-upgrade）。第一段由舊引擎換上目標引擎的版本鎖定行，以 VK0023
//! 停下，請使用者重跑原指令；第二段由新引擎做：重產薄殼、VK 檔格式升級、寫 `gen/.stamp` 與介面版列表、刪進度檔。
//!
//! `upgrade --engine` 是救援路徑（ADR-0007:37、ADR-0008:26）：往返只用 [`plan::RESCUE_OPS`] 的 op（這裡只送
//! `inspect` 與 `pull`，第二段不送任何 op），呼叫方的介面版不在本引擎區間內時也照常執行（入口 `vendor_kit` 的
//! `gate`）。呼叫端已解析好參數、判過安裝目錄（VK0028），並接好執行紀錄與 `plan` 往返。這裡依序做：
//!
//! 1. 讀 `.vendor_kit/config.toml`（VK0059），在取鎖之前（同 `upgrade <repo>`）。
//! 2. 取安裝目錄的排他鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束。
//! 3. 讀 `version.toml`（檔案版過高回 VK0008）。
//! 4. 看殘留的進度檔，在任何 docker 動作與寫入之前：都是引擎升級的（`[upgrade] target = "vendor_kit"`），
//!    而且記的目標就是版本鎖定行，表示第一段做完了，直接做第二段（見「第二段」），不連 registry。都記著同一個
//!    目標、但不是版本鎖定行：第一段建好進度檔、還沒換鎖定行就停下了，照記的目標重做第一段（見「第一段中斷」）。
//!    帶的 `--engine=<tag>` 跟要續作的目標不同、或有別的殘留，見「缺口」。
//! 5. 判目標版本：`--engine=<tag>` 就是那個 tag；不帶 tag 就匿名列 [`ENGINE_REPO`] 的 tag，依 04 指定版本取最新版
//!    （[`imageref::Tag::latest`]）。不讀 `--registry-token-file`（04：不適用引擎升版，`args` 也不收）。
//!    目標 tag 等於版本鎖定行的 tag：沒有第一段可做，照第二段判薄殼與 VK 檔（N21 草稿點：鎖定行已是目標版、
//!    但薄殼或 VK 檔還是舊版時直接做第二段，不能回「已是最新」）。最新版比鎖定行舊：見「缺口」。
//! 6. 解析目標的版本鎖定行值，做法同 `upgrade <repo>` 的「線上解析」，image 一律是 [`ENGINE_REPO`]（不看鎖定行
//!    記的路徑；engine/install 寫鎖定行時已檢查兩者相等）：先 `inspect` 本機 `<ENGINE_REPO>:<tag>`；本機沒有就向
//!    registry 取 tag 的 digest，`pull <ENGINE_REPO>@<digest>` 再以同一個引用 `inspect`。缺 RepoDigest 回 VK0031；
//!    同一個 tag 指向不同 digest 照 `upgrade <repo>` 以 VK0056 停下（草稿碼見 [`crate::DRAFT_TAG_DIGESTS`]）。
//! 7. 讀目標 image 的 LABEL（[`LABEL_FLOOR`]、[`LABEL_CURRENT`]、[`LABEL_SCHEMA_MAX`]、[`LABEL_VERSION`]；
//!    engine/compat 的 `image_build_args` 與 image/Dockerfile 寫的那幾個），組成目標引擎的 [`Compat`]。
//! 8. 判降版（[`Compat::check_downgrade`]）：現有 VK 檔的最高檔案版（見「現有檔案版」）高於目標引擎的檔案版上限，
//!    回 VK0007（`<vY>` 是目標 tag，`<P>`、`<M>` 取自目標 LABEL，`<N>` 是現有檔案版；`<tag>` 依訊息表原樣印出），
//!    除執行紀錄外不寫任何檔。升版一樣判，目標上限不比現有低就一定過。
//! 9. 經 `txn` 落地：執行紀錄 `writes_started` → 建進度檔（`[upgrade] target = "vendor_kit"`、`image` 是目標的
//!    版本鎖定行值，原指令在共同欄位 `command`）→ `lock_line_write_started` → 換引擎鎖定行與介面版列表
//!    （`vendor_kit_protocols` 改成目標引擎的區間）→ `lock_line_written`。不換 `cache/`、不寫 repo 檔、紀錄檔與
//!    `gen/tools.just`，也不刪進度檔：留著進度檔讓第二段與唯讀 recipe 認得出引擎升級還沒做完（02 不變量第 4 條
//!    的例外：鎖定行先於完成點寫入）。
//! 10. 報 VK0023 停下（結束碼 2）：`<vY>` 是目標 tag，`<original_command>` 是 `just vendor_kit` 接上原指令的每一段
//!     （保留原 tag 與 `-y`，依 POSIX shell 規則加引號，[`original_command`]）。
//!
//! `-y` 第一段用不到（第一段不詢問），只是原樣留在原指令裡給第二段。
//!
//! # 第一段中斷
//!
//! 第一段在建好進度檔、還沒換版本鎖定行時停下（第 9 步的 `writes_started` 到 `lock_line_written` 之間），重跑時
//! 鎖定行仍是舊引擎，啟動器起的也還是舊引擎，讀到的進度檔記的目標不是鎖定行。這時照進度檔記的目標重做第一段：
//!
//! 1. 目標 tag 取進度檔 `[upgrade] image` 的 tag；不帶 tag 也不列 registry 的 tag（不換成重跑當下的最新版）。
//! 2. 照第 6～8 步解析並檢查目標；解析出的 digest 跟進度檔記的不同，照第 6 步的同一個 tag 指向不同 digest
//!    以 VK0056 停下（草稿碼見 [`crate::DRAFT_TAG_DIGESTS`]）。
//! 3. 照第 9 步建這次的進度檔、換鎖定行，再刪殘留的進度檔，照第 10 步報 VK0023。
//!
//! 鎖定行在第一段之後被手改過，看起來跟這個狀態一樣，也照同樣做法換回進度檔記的目標。
//!
//! # 第二段
//!
//! 由版本鎖定行記的那一版引擎做（重跑原指令時啟動器照新的鎖定行起引擎）。只讀不寫地算完下面幾項，再一次問完、
//! 一次落地：
//!
//! 1. 先確認在跑的就是版本鎖定行那一版：本引擎版本（`written_by`）不等於鎖定行的 tag 就以 VK0056 停下；引擎開著
//!    本機覆寫（`dev --engine`）見「缺口」（flow-engine-upgrade：比薄殼舊的本機引擎不准重產進 git 的薄殼）。
//! 2. 薄殼四檔：以本引擎的介面版、本引擎版與隨 image 出貨的模板產生（同 `install`），逐檔比對，只寫不一致的
//!    （缺檔、被改過、不是這一版的模板）。symlink 或不是一般檔時停下。沒有模板見「缺口」。
//! 3. `gen/.stamp`：版本鎖定行的引擎值（同 `install`），跟現有內容不同才寫。
//! 4. VK 檔格式升級（[`crate::migrate`]）：「現有檔案版」列的每個檔，檔案版低於本引擎上限就直接升到上限
//!    （不鏈式）。`version.toml` 升級後交給版本鎖定行那一步寫。
//! 5. `config.toml` 的換版與合併（見「config.toml」）：算出判定、要問的那一題與要寫的內容。
//! 6. 介面版列表：`vendor_kit_protocols` 寫成本引擎的區間。
//! 7. 沒有殘留的進度檔、而上面全都已是這一版（`config.toml` 沒有要寫的）：stdout 說明未變更，以 0 結束，
//!    不建進度檔。
//! 8. 一次問完（帶 `-y` 全部同意）：答否是正常取消，stdout 說明未變更、以 0 結束，什麼都不寫，第一段換好的
//!    鎖定行與進度檔都不動（04：第二次呼叫答否，不撤回第一次已完成的換引擎），所以引擎升級仍未做完，唯讀
//!    recipe 照樣報 VK0023；不能互動回 VK0002，同樣不寫。要問的只有 `config.toml` 的那一題。
//! 9. 經 `txn` 落地：建這次的進度檔（同第一段的 `[upgrade]` 表，`image` 是版本鎖定行的值）→ `config.toml`
//!    （repo 檔那一步）→ 薄殼、升級後的 VK 檔、`config.toml` 的基準版副本與 `baseline/.vendor_kit.toml`、
//!    `gen/.stamp`（紀錄檔那一步，依序）→ 版本鎖定行（介面版列表）→ 刪這次的進度檔；之後才刪殘留的進度檔。
//! 10. stdout 列出寫了哪些薄殼、升級了哪些 VK 檔、`config.toml` 怎麼了（同 `upgrade <repo>` 的初始檔字句），
//!     最後一行說明引擎升級完成；合併留下衝突時再印 VK0021（warn，結束碼 1）。
//!
//! 中途停下時這次與第一段的進度檔都還在，鎖定行已是新版；重跑原指令照上面再做一次（薄殼與 `gen/.stamp` 只寫
//! 不一致的，升過的 VK 檔已是上限，`config.toml` 見下一節），落地後一起刪掉。
//!
//! # 預演（`--dry-run`，#372 N11）
//!
//! 語意是這一版自訂的（契約沒寫，列給維護者確認）。`upgrade --engine --dry-run`（含 `=<tag>`、`-y`）屬救援路徑，
//! 文法跨介面版永久不變（`args` 的 crate 文件，待維護者確認）。兩段都照上面的順序算到落地之前，差別只在：
//!
//! - 取安裝目錄的共享鎖，不取排他鎖（只讀）。
//! - 第一段：解析目標（`inspect`、`pull` 照送，動到的是主機的 image store）、判降版（VK0007 照樣停下），之後
//!   不建進度檔、不換鎖定行、不刪殘留的進度檔，也不報 VK0023；stdout 印會換上的鎖定行
//!   （[`crate::text::would_lock_engine`]）與一行說明第二段要等重跑時由新的引擎做
//!   （[`crate::text::would_finish_on`]）：第二段的薄殼模板與 VK 檔格式由目標引擎決定，這一版算不出來。
//! - 第二段：不問（`config.toml` 那一題也跳過，不能互動不報 VK0002）、不落地、不刪殘留的進度檔；stdout 照
//!   第 10 步的順序印「Would …」的寫法，合併留下衝突時照樣印 VK0021。
//! - 兩段的最後一行都是 `prompt::DRY_RUN_DONE`，除了警告以外以 0 結束；除執行紀錄外不寫任何檔。跟 `-y` 並用時
//!   `-y` 沒有作用。算計畫時遇到的停下（VK0008、VK0031、VK0055、缺口等）照樣以各自的結束碼停下。
//!
//! # config.toml
//!
//! 04 使用者的檔與 VK 的檔：`config.toml` 是使用者維護的檔，不是初始檔，換版與合併沿用初始檔的保護規則
//! （04 寫入既有檔的例外：未改過也先問是否換版；雙方都改過先問是否合併，衝突留標記）。做法跟 `upgrade <repo>`
//! 的初始檔一樣經 `initfiles`（`Command::Upgrade`，整份型），三份輸入是：
//!
//! - 新版：隨本引擎出貨的模板（[`Request::config_template`]，engine/install 的 `release::CONFIG_TEMPLATE`）。
//! - 基準版：`baseline/.vendor_kit/config.toml`（[`layout::InstallDir::config_baseline`]，engine/install 存的）。
//! - 目前檔：`.vendor_kit/config.toml`。
//!
//! 紀錄是 `baseline/.vendor_kit.toml` 裡 `path` 為 [`CONFIG_TOML`] 的那一筆；判定只拿這一筆（同一份紀錄檔裡
//! 根目錄檔的紀錄不是引擎升級的新版）。依 `initfiles` 的判定：
//!
//! - 新版跟基準版相同：不動、不問（大多數引擎升級都是這樣）。
//! - 使用者沒改過：問「是否換成新版」；同意就換，基準版副本推到新版，紀錄的 hash 換成寫入後的。
//! - 雙方都改過：問「是否合併」；同意就寫入合併結果，基準版推到新版。`config.toml` 是 TOML，留下衝突標記的
//!   結果一定解析不過，所以照 scope_roadmap:32 的例外處理：留原檔、不問、基準版不推，記入
//!   `baseline/.vendor_kit.toml` 的 `conflicts`，stdout 說明留了原檔（同 `upgrade <repo>`）；之後換版或合併
//!   寫入成功就從 `conflicts` 拿掉。VK0021 只在合併結果仍是合法 TOML 時才可能出現，實際上碰不到。
//! - 使用者刪掉了：不重建，紀錄記 `deleted`，stdout 列出來。
//! - `initfiles` 判成缺口的情況：以 VK0056 停下（見「缺口」）。
//!
//! 中斷後恢復：repo 檔先於紀錄檔寫入，所以換版寫進 `config.toml` 之後、推基準版之前停下，重跑時目前檔等於新版
//! 卻不等於基準版（`initfiles` 的 `Gap::CurrentIsNew`）。有殘留的進度檔時這就是上一次寫的：基準版副本推到新版、
//! 紀錄的 hash 換成目前檔的、從 `conflicts` 拿掉，repo 檔不再寫，stdout 不再列。合併寫到一半停下的，重跑時
//! 照「雙方都改過」再問一次，合併結果不變。
//!
//! # 查詢失敗
//!
//! 照 `upgrade <repo>` 的「查詢失敗」，`<target>` 與 VK0058 的 `<repo>` 是 [`ENGINE_NAME`]、`<source>` 是查的
//! [`ENGINE_REPO`]（取 digest 時是 `<ENGINE_REPO>:<tag>`）。差別：列 tag 時 registry 要求認證也報 VK0055，不報
//! VK0001（VK0001 的下一步是帶 `--registry-token-file`，引擎升版不收這個選項）。
//!
//! # 現有檔案版
//!
//! 只看 VK 寫的 TOML：`version.toml`、`version.local.toml`、`baseline/.vendor_kit.toml`、版本鎖定行裡每個工具的
//! metadata 與印記（`cache/<repo>.stamp.toml`）。不掃整個 `.vendor_kit/`：`cache/<repo>/` 是工具交付的檔、
//! `baseline/<repo>/` 是初始檔的副本，都不是 VK 檔；`config.toml` 是使用者的檔，沒有檔案版；`log/`、`gen/.stamp`
//! 不是 TOML；進度檔由各自的 recipe 讀寫。檔不在就跳過；讀不到或不是合法的 VK TOML 是 VK 的錯，以 VK0056 停下。
//! 判降版時檔案版高於本引擎上限的檔照樣算進去（讀時不套本引擎的門檻）；第二段遇到這種檔以 VK0056 停下。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 進度檔沿用 `progress::upgrade` 的 `[upgrade]` 表：`target` 是 `progress::upgrade::ENGINE_TARGET`、`image` 是
//!   目標的版本鎖定行值；不記 `init_files`（引擎升級不碰初始檔）。第二段的進度檔也一樣，所以唯讀 recipe 讀到哪一份
//!   都報 VK0023。
//! - 目標 image 的 [`LABEL_VERSION`] 必須等於目標 tag，否則以 VK0056 停下：鎖定行的 tag 要描述的就是那個 image。
//! - [`ENGINE_REPO`] 照抄 engine/install 的同名常數（指令之間互不依賴），兩邊相等由入口 crate 的測試檢查。
//! - stdout 的字句（英文）見 [`crate::text`]；未變更的字句同 `upgrade <repo>`（[`crate::text::unchanged`]）。
//!   `config.toml` 的詢問與字句用 `upgrade <repo>` 的初始檔字句（[`crate::text::question`]、
//!   [`crate::text::file_line`]、[`crate::text::listed_line`]），`<repo>` 是 [`ENGINE_NAME`]。
//! - `baseline/.vendor_kit.toml` 沒有 `config.toml` 的紀錄（例如 engine/install 記紀錄之前裝的，或使用者在
//!   `install` 之前自己建了檔）：不碰 `config.toml`。04 的換版與合併規則說的是已納管的檔；沒有紀錄就沒有
//!   基準版，新建或納管是 `install` 的事。
//!
//! # 缺口（契約或其他 crate 沒定；遇到就以 VK0056 停下並寫明原因）
//!
//! - 殘留其他可寫 recipe 的進度檔：可寫 recipe 要先恢復（04 成對與無害），引擎升級怎麼恢復別的指令沒定。殘留的
//!   引擎升級進度檔記著不同的目標（有的是版本鎖定行、有的不是，或彼此不同），或帶的 `--engine=<tag>` 跟要續作
//!   的目標（版本鎖定行，或「第一段中斷」時進度檔記的目標）不同：04 沒說要續作哪一個。
//! - 不帶 tag 而 registry 的最新版比鎖定行舊：04 只說最新版不限目前的 vX，沒說要不要因此降版（同 `upgrade <repo>`）。
//! - 目標 image 缺 LABEL 或值不合（例如公告檔案版上限的 LABEL 之前出的 image）：判不了降版。
//! - 引擎開著本機覆寫（`dev --engine`）：第一段照樣只換鎖定行、覆寫不動；第二段由哪一版引擎做沒定，停下。
//! - 第二段時這一版 image 沒有薄殼模板（出貨輸入缺項，同 `install`）。
//! - `config.toml` 遇到 `initfiles` 判成缺口的情況（例如紀錄記 `deleted` 而檔又出現了；目前檔等於新版卻不等於
//!   基準版、又沒有殘留的進度檔）。
//! - `config.toml` 合併結果解析不過、留了原檔：同 `upgrade <repo>`，沒有訊息表代碼，照常以 0 結束。
//! - registry 列得到、但一個 tag 都沒有：照 `upgrade <repo>` 報 VK0055（[`crate::text::NO_TAGS`]）。
//! - 中途寫檔失敗沒有代碼（計畫 G4）。

use std::fs;
use std::io::{self, Write};
use std::path::{Path, PathBuf};

use compat::Compat;
use diagnostics::{Diagnostic, Sink};
use imageref::{ImageRef, Tag};
use initfiles::{Ask, FilePlan, Gap, InitFile, Strategy, Verdict};
use metadata::{FileHash, Metadata};
use progress::Progress;
use progress::upgrade as table;
use prompt::{Consent, PromptError, TtyState};
use runlog::Target;
use shell::Shell;
use txn::{Disk, RecordFile, RepoFile, Txn};
use version_file::{LocalFile, LockFile};

use super::{Env, Step, Upgrade, VERB, discover_init_files, migrate, read_optional, text};

/// 引擎 image 的 `<registry>/<路徑>`（engine/install 的 `release::ENGINE_REPO`；指令之間互不依賴，照抄）。
pub const ENGINE_REPO: &str = "ghcr.io/ycpss91255-research/vendor_kit";
/// VK0055 的 `<target>`、VK0058 的 `<repo>`：引擎的名字（保留名，同 `progress::upgrade::ENGINE_TARGET`）。
pub const ENGINE_NAME: &str = table::ENGINE_TARGET;
/// 引擎 image 公告最低介面版的 LABEL（engine/compat 的 `image_build_args`、image/Dockerfile）。
pub const LABEL_FLOOR: &str = "vendor_kit.protocol.floor";
/// 引擎 image 公告目前介面版的 LABEL。
pub const LABEL_CURRENT: &str = "vendor_kit.protocol.current";
/// 引擎 image 公告檔案版上限的 LABEL。
pub const LABEL_SCHEMA_MAX: &str = "vendor_kit.schema.max";
/// 引擎 image 公告引擎版本（`v<X.Y.Z>`）的 LABEL。
pub const LABEL_VERSION: &str = "org.opencontainers.image.version";
/// `.vendor_kit/config.toml` 的 repo 相對路徑（`baseline/.vendor_kit.toml` 裡紀錄的 `path`；engine/install 的
/// `CONFIG_TOML`，照抄，兩邊相等由入口 crate 的測試檢查）。
pub const CONFIG_TOML: &str = ".vendor_kit/config.toml";
/// 重組 `<original_command>` 時接在參數前面的字。
pub const COMMAND_PREFIX: [&str; 2] = ["just", "vendor_kit"];

/// 隨 image 出貨的薄殼四檔模板本文，順序同 `layout::SHELL_FILES`。
pub type ShellTemplates = [Vec<u8>; layout::SHELL_FILES.len()];

/// 一次 `upgrade --engine[=<tag>] [-y] [--dry-run]` 的參數（`args::Command::UpgradeEngine`）與第二段要的出貨輸入。
#[derive(Debug, Clone, Copy)]
pub struct Request<'a> {
    pub tag: Option<Tag>,
    /// `-y`：第一段不詢問，只留在原指令裡；第二段預先同意全部詢問。
    pub yes: bool,
    /// `--dry-run`：算出這一段的計畫後只印、不問、不寫（模組說明「預演」）。
    pub dry_run: bool,
    /// 薄殼模板（入口讀 image 裡的出貨輸入）；四檔不齊是 `None`，第二段遇到就停下（模組說明「缺口」）。
    pub shell_templates: Option<&'a ShellTemplates>,
    /// 隨本引擎出貨的 `config.toml` 模板（engine/install 的 `release::CONFIG_TEMPLATE`），第二段拿它當新版。
    pub config_template: &'a str,
}

/// 跑一次 `upgrade --engine`，回傳結束碼。`env` 跟 `upgrade <repo>` 共用（`argv` 第一個是 `upgrade`）。
pub fn run<W: Write, S: Sink, L: Write>(req: &Request<'_>, env: &mut Env<'_, W, S, L>) -> u8 {
    let mut upgrade = Upgrade {
        env,
        init: &discover_init_files,
        dry_run: req.dry_run,
        code: 0,
        extracts: 0,
        stages: 0,
        local: Default::default(),
        pending: Vec::new(),
        engine: true,
    };
    let _ = upgrade.engine_run(req);
    upgrade.code
}

/// 殘留的進度檔怎麼續作（模組說明第 4 步）。
enum Residuals {
    None,
    /// 第一段做完：記的目標就是版本鎖定行，做第二段。
    FirstStageDone(Vec<progress::Entry>),
    /// 第一段建好進度檔、還沒換鎖定行就停下：照記的目標重做第一段（模組說明「第一段中斷」）。
    FirstStageInterrupted(Vec<progress::Entry>, ImageRef),
}

/// 重做第一段時要對照的進度檔（模組說明「第一段中斷」）。
#[derive(Clone, Copy)]
struct Resume<'a> {
    /// 進度檔記的版本鎖定行值。
    recorded: &'a ImageRef,
    residuals: &'a [progress::Entry],
}

/// 第二段對 `config.toml` 要做的事（模組說明「config.toml」）。
struct ConfigChange {
    /// `initfiles` 對 `config.toml` 的判定；中斷後恢復時改過的見 [`ConfigChange::adopted`]。
    plan: FilePlan,
    /// 恢復時補上紀錄（`Gap::CurrentIsNew` 且有殘留的進度檔）。
    adopted: bool,
    /// 要一起問的那一題。
    question: Option<String>,
    /// 換過的 `baseline/.vendor_kit.toml` 全文；紀錄沒變是 `None`。
    metadata: Option<Vec<u8>>,
}

/// POSIX shell 的單引號引用：只含安全字元就原樣（同 engine/update 的 `shell_quote`；指令之間互不依賴，照抄）。
pub fn shell_quote(s: &str) -> String {
    let safe = |c: char| c.is_ascii_alphanumeric() || "_@%+=:,./-".contains(c);
    if !s.is_empty() && s.chars().all(safe) {
        return s.to_owned();
    }
    format!("'{}'", s.replace('\'', r"'\''"))
}

/// 由原指令（`just vendor_kit` 之後的參數）重組 VK0023 的 `<original_command>`。
pub fn original_command<S: AsRef<str>>(command: &[S]) -> String {
    COMMAND_PREFIX
        .iter()
        .map(|w| (*w).to_owned())
        .chain(command.iter().map(|w| shell_quote(w.as_ref())))
        .collect::<Vec<_>>()
        .join(" ")
}

/// 目標 image 的 LABEL 組成的相容範圍；缺 LABEL 或值不合回說明。
pub fn target_compat(
    labels: &std::collections::BTreeMap<String, String>,
    tag: Tag,
) -> Result<Compat, String> {
    let number = |key: &str| -> Result<u32, String> {
        let value = labels
            .get(key)
            .ok_or_else(|| format!("the target engine image has no {key} label"))?;
        let ok = !value.is_empty()
            && value.bytes().all(|b| b.is_ascii_digit())
            && !value.starts_with('0');
        let n = ok.then(|| value.parse::<u32>().ok()).flatten();
        n.ok_or_else(|| format!("the target engine image has {key}={value:?}"))
    };
    let compat = Compat {
        floor_protocol: number(LABEL_FLOOR)?,
        current_protocol: number(LABEL_CURRENT)?,
        max_schema: number(LABEL_SCHEMA_MAX)?,
    };
    if compat.floor_protocol > compat.current_protocol {
        return Err(format!(
            "the target engine image has {LABEL_FLOOR}={} above {LABEL_CURRENT}={}",
            compat.floor_protocol, compat.current_protocol
        ));
    }
    match labels.get(LABEL_VERSION) {
        Some(v) if *v == tag.to_string() => Ok(compat),
        Some(v) => Err(format!(
            "the target engine image announces {LABEL_VERSION}={v:?}, not {tag}"
        )),
        None => Err(format!(
            "the target engine image has no {LABEL_VERSION} label"
        )),
    }
}

/// 讀檔案版時不套任何上限：檔案版高於本引擎上限的檔也要算進「現有檔案版」。
const ANY_SCHEMA: Compat = Compat {
    floor_protocol: 1,
    current_protocol: 1,
    max_schema: u32::MAX,
};

impl<W: Write, S: Sink, L: Write> Upgrade<'_, '_, W, S, L> {
    fn engine_run(&mut self, req: &Request<'_>) -> Step<()> {
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        let lockfile = self.lockfile()?;
        let current = lockfile.engine().tag();
        match self.engine_residuals(&lockfile)? {
            Residuals::None => {}
            Residuals::FirstStageDone(residuals) => {
                self.same_tag(req, current, &residuals[0])?;
                return self.engine_stage2(req, lockfile, &residuals);
            }
            Residuals::FirstStageInterrupted(residuals, recorded) => {
                self.same_tag(req, recorded.tag(), &residuals[0])?;
                let resume = Resume {
                    recorded: &recorded,
                    residuals: &residuals,
                };
                return self.engine_stage1(recorded.tag(), None, lockfile, Some(resume));
            }
        }
        let registry = self.env.registry;

        let mut listed = None;
        let tag = match req.tag {
            Some(tag) => tag,
            None => {
                let mut repo = match registry.repository(ENGINE_REPO, None) {
                    Ok(r) => r,
                    Err(e) => return Err(self.list_failed(&e, ENGINE_REPO, ENGINE_NAME)),
                };
                let latest = self.latest(&mut repo, ENGINE_REPO, ENGINE_NAME)?;
                if latest < current {
                    return Err(self.gap(format_args!(
                        "upgrade --engine when the latest engine version in the registry ({latest}) \
                         is older than the engine lock version line ({current})"
                    )));
                }
                listed = Some(repo);
                latest
            }
        };
        if tag == current {
            return self.engine_stage2(req, lockfile, &[]);
        }
        self.engine_stage1(tag, listed.as_mut(), lockfile, None)
    }

    fn engine_stage1(
        &mut self,
        tag: Tag,
        listed: Option<&mut registry::Repository<'_>>,
        mut lockfile: LockFile,
        resume: Option<Resume<'_>>,
    ) -> Step<()> {
        if let Some(entry) =
            resume.and_then(|r| r.residuals.iter().find(|e| e.id == self.env.run_id))
        {
            let file = self.rel(&entry.path);
            return Err(self.internal(format!("{file} has this run's id {}", entry.id)));
        }
        if let Some(r) = resume {
            let name = format!("{}/{}", r.recorded.registry(), r.recorded.path());
            if name != ENGINE_REPO {
                let file = self.rel(&r.residuals[0].path);
                return Err(self.internal(format!(
                    "{file} records the engine upgrade to {}, which is not a {ENGINE_REPO} image",
                    r.recorded
                )));
            }
        }
        let resolved = self.resolve(ENGINE_REPO, tag, listed, ENGINE_NAME)?;
        if let Some(r) = resume.filter(|r| *r.recorded != resolved.locked) {
            let given = format!("{ENGINE_REPO}:{tag}");
            let digests = [
                r.recorded.digest().to_string(),
                resolved.locked.digest().to_string(),
            ];
            return Err(self.tag_digests(&given, &digests));
        }
        let target = target_compat(&resolved.labels, tag).map_err(|r| self.internal(r))?;
        let existing = self.existing_schema(&lockfile)?;
        if let Err(e) = target.check_downgrade(existing) {
            let d = Diagnostic::new(e.message())
                .arg("vY", tag.to_string())
                .arg("P", e.target_protocol.to_string())
                .arg("M", e.target_max_schema.to_string())
                .arg("N", e.existing_schema.to_string());
            return Err(self.stop(d));
        }

        let set = lockfile
            .set_engine(&resolved.locked)
            .and_then(|()| lockfile.set_protocols(&target));
        set.map_err(|e| self.internal(e.to_string()))?;
        if self.dry_run {
            // 預演：不換鎖定行、不建進度檔、殘留的照留，也不報 VK0023（模組說明「預演」）。
            self.say(&text::would_lock_engine(&resolved.locked));
            self.say(&text::would_finish_on(tag));
            self.dry_run_done();
            return Ok(());
        }
        let progress = self.engine_progress(&resolved.locked)?;
        self.switch(progress, &mut lockfile)?;
        // 「第一段中斷」：這次的進度檔已記著同一個目標，殘留的那份不再需要。
        for entry in resume.map_or(&[][..], |r| r.residuals) {
            if let Err(e) = progress::delete(self.env.dir, &entry.verb, &entry.id) {
                return Err(self.failed(&entry.path, e.message(), e.to_string()));
            }
        }

        let d = Diagnostic::new(&messages::VK0023)
            .arg("vY", tag.to_string())
            .arg("original_command", original_command(self.env.argv));
        Err(self.stop(d))
    }

    /// 帶的 `--engine=<tag>` 跟要續作的目標 `target` 不同就停下（模組說明「缺口」）；`first` 是殘留的進度檔之一。
    fn same_tag(&mut self, req: &Request<'_>, target: Tag, first: &progress::Entry) -> Step<()> {
        match req.tag.filter(|t| *t != target) {
            Some(tag) => {
                let file = self.rel(&first.path);
                Err(self.gap(format_args!(
                    "upgrade --engine={tag} while the engine upgrade to {target} recorded in \
                     {file} is incomplete"
                )))
            }
            None => Ok(()),
        }
    }

    /// 殘留的進度檔（模組說明第 4 步）：全是引擎升級、記著同一個目標時回傳怎麼續作；有別的就停下（模組說明「缺口」）。
    fn engine_residuals(&mut self, lockfile: &LockFile) -> Step<Residuals> {
        let entries = match progress::find(self.env.dir) {
            Ok(e) => e,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let mut targets: Vec<(String, ImageRef)> = Vec::new();
        for entry in &entries {
            let file = self.rel(&entry.path);
            if entry.verb != VERB {
                return Err(self.gap(format_args!(
                    "upgrade --engine while the incomplete {} operation in {file} remains",
                    entry.verb
                )));
            }
            let loaded = match entry.load() {
                Ok(p) => p,
                Err(progress::Error::Parse {
                    file,
                    source: progress::ParseError::Read(schema::ReadError::TooNew(t)),
                }) => return Err(self.too_new(&file, &t)),
                Err(e) => return Err(self.failed(&entry.path, e.message(), e.to_string())),
            };
            if table::field(&loaded, table::TARGET) != Some(table::ENGINE_TARGET) {
                return Err(self.gap(format_args!(
                    "upgrade --engine while the incomplete upgrade operation in {file} remains"
                )));
            }
            let image = table::field(&loaded, table::IMAGE).map(ImageRef::parse);
            let Some(Ok(image)) = image else {
                return Err(self.internal(format!(
                    "{file} has no valid [{}] {} field",
                    table::TABLE,
                    table::IMAGE
                )));
            };
            targets.push((file, image));
        }
        let Some((first, recorded)) = targets.first().cloned() else {
            return Ok(Residuals::None);
        };
        if let Some((file, other)) = targets.iter().find(|(_, t)| *t != recorded) {
            return Err(self.gap(format_args!(
                "completing the engine upgrades recorded in {first} ({recorded}) and {file} \
                 ({other}), which name different targets,"
            )));
        }
        if recorded == *lockfile.engine() {
            Ok(Residuals::FirstStageDone(entries))
        } else {
            Ok(Residuals::FirstStageInterrupted(entries, recorded))
        }
    }

    /// 第二段（模組說明「第二段」）；`residuals` 是第一段（或中斷的第二段）留下的進度檔。
    fn engine_stage2(
        &mut self,
        req: &Request<'_>,
        mut lockfile: LockFile,
        residuals: &[progress::Entry],
    ) -> Step<()> {
        let engine = lockfile.engine().clone();
        let tag = engine.tag();
        if tag.to_string() != self.env.written_by {
            return Err(self.internal(format!(
                "this engine is {}, but the engine lock version line names {tag}; the second stage \
                 of the engine upgrade runs on the engine that line names",
                self.env.written_by
            )));
        }
        self.no_engine_override()?;
        if let Some(entry) = residuals.iter().find(|e| e.id == self.env.run_id) {
            let file = self.rel(&entry.path);
            return Err(self.internal(format!("{file} has this run's id {}", entry.id)));
        }
        let Some(templates) = req.shell_templates else {
            return Err(self.gap(
                "the second stage of the engine upgrade without the shell templates, which this \
                 engine image does not ship",
            ));
        };

        // 薄殼四檔：只寫不一致的。
        let bodies = [
            templates[0].as_slice(),
            templates[1].as_slice(),
            templates[2].as_slice(),
            templates[3].as_slice(),
        ];
        let shell = Shell::render(compat::THIS.current_protocol, self.env.written_by, bodies);
        let shell = shell.map_err(|e| self.internal(e.to_string()))?;
        let report = shell.check(self.env.dir);
        let report = report.map_err(|e| self.internal(e.to_string()))?;
        let shell_names: Vec<&'static str> = report.mismatches().map(|f| f.name).collect();
        let mut records: Vec<(PathBuf, Vec<u8>)> = shell_names
            .iter()
            .filter_map(|n| shell.file(n).map(|c| (PathBuf::from(n), c.to_vec())))
            .collect();

        // VK 檔格式升級；`version.toml` 交給版本鎖定行那一步。
        let mut migrated: Vec<(String, u32)> = Vec::new();
        let version_toml = self.env.dir.version_toml();
        for path in self.vk_files(&lockfile)? {
            let Some((from, text)) = self.migrate_file(&path)? else {
                continue;
            };
            migrated.push((self.rel(&path), from));
            if path == version_toml {
                lockfile = LockFile::parse(&text)
                    .map_err(|e| self.internal(format!("{}: {e}", self.rel(&path))))?;
            } else {
                let rel = self.vk_rel(&path)?;
                records.push((rel, text.into_bytes()));
            }
        }

        // `config.toml`：新版是本引擎出貨的模板；`baseline/.vendor_kit.toml` 升級過就接著改升級後的內容。
        let md_rel = self.vk_rel(&metadata::vk_path(self.env.dir))?;
        let md_index = records.iter().position(|(p, _)| *p == md_rel);
        let migrated_md = md_index.map(|i| records[i].1.clone());
        let config = self.config_change(req.config_template, !residuals.is_empty(), migrated_md)?;
        let mut repo_writes: Vec<(PathBuf, Vec<u8>)> = Vec::new();
        let mut questions: Vec<String> = Vec::new();
        if let Some(c) = &config {
            if let Some(w) = &c.plan.write {
                repo_writes.push((PathBuf::from(CONFIG_TOML), w.after.clone()));
            }
            if let Some(b) = &c.plan.baseline {
                records.push((self.vk_rel(&self.env.dir.config_baseline())?, b.clone()));
            }
            if let Some(m) = &c.metadata {
                match md_index {
                    Some(i) => records[i].1 = m.clone(),
                    None => records.push((md_rel, m.clone())),
                }
            }
            questions.extend(c.question.clone());
        }

        // `gen/.stamp`：產生薄殼的引擎 ref，跟現有內容不同才寫。
        let stamp = format!("{engine}\n").into_bytes();
        let stamp_path = self.env.dir.stamp();
        let now = match fs::read(&stamp_path) {
            Ok(b) => Some(b),
            Err(e) if e.kind() == io::ErrorKind::NotFound => None,
            Err(e) => return Err(self.internal(format!("{}: {e}", self.rel(&stamp_path)))),
        };
        let stamp_changed = now.as_deref() != Some(stamp.as_slice());
        if stamp_changed {
            records.push((self.vk_rel(&stamp_path)?, stamp));
        }

        // 介面版列表寫成本引擎的區間。
        let protocols: Vec<u32> =
            (compat::THIS.floor_protocol..=compat::THIS.current_protocol).collect();
        let protocols_changed = lockfile.protocols() != protocols.as_slice();
        lockfile
            .set_protocols(&compat::THIS)
            .map_err(|e| self.internal(e.to_string()))?;

        if residuals.is_empty()
            && records.is_empty()
            && repo_writes.is_empty()
            && migrated.is_empty()
            && !protocols_changed
        {
            self.config_lines(config.as_ref(), tag);
            self.say(&text::unchanged(ENGINE_NAME, tag));
            self.dry_run_done();
            return Ok(());
        }

        let dry = self.dry_run;
        if dry {
            // 預演不問、不落地，殘留的進度檔照留（模組說明「預演」）。
            self.engine_report(&shell_names, &migrated, config.as_ref(), &engine);
            self.dry_run_done();
            return Ok(());
        }
        if !self.engine_ask(&questions, req.yes)? {
            self.say(text::NO_CHANGES);
            return Ok(());
        }

        let progress = self.engine_progress(&engine)?;
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
                t.swap_cache(&[])?
                    .write_repo_files(&repo_files)?
                    .write_records(&record_files)?
                    .write_tools_just(None)?
                    .write_lock_line(&mut lockfile, Target::Engine)?
                    .complete()
            })
        };
        result.map_err(|f| self.internal(f.to_string()))?;
        for entry in residuals {
            if let Err(e) = progress::delete(self.env.dir, &entry.verb, &entry.id) {
                return Err(self.failed(&entry.path, e.message(), e.to_string()));
            }
        }

        self.engine_report(&shell_names, &migrated, config.as_ref(), &engine);
        Ok(())
    }

    /// 第二段的 stdout 字句與 `config.toml` 的警告（模組說明「第二段」第 10 步）；預演時是「Would …」的寫法。
    fn engine_report(
        &mut self,
        shell_names: &[&str],
        migrated: &[(String, u32)],
        config: Option<&ConfigChange>,
        engine: &ImageRef,
    ) {
        let dry = self.dry_run;
        let tag = engine.tag();
        for name in shell_names {
            self.say(&text::wrote_shell(name, dry));
        }
        for (file, from) in migrated {
            self.say(&text::migrated(file, *from, compat::THIS.max_schema, dry));
        }
        self.config_lines(config, tag);
        self.say(&text::engine_upgraded(engine, dry));
        if let Some(m) = config.and_then(|c| c.plan.message()) {
            let d = Diagnostic::new(m)
                .arg("file", CONFIG_TOML)
                .arg("repo", ENGINE_NAME)
                .arg("tag", tag.to_string());
            self.emit(d);
        }
    }

    /// `config.toml` 的換版與合併（模組說明「config.toml」）：只讀不寫地算出判定、要問的那一題與寫入內容。
    /// `baseline/.vendor_kit.toml` 沒有它的紀錄回 `None`（不碰）。`resuming` 是有殘留的進度檔；`migrated_md`
    /// 是這次升級過的 `baseline/.vendor_kit.toml` 全文。
    fn config_change(
        &mut self,
        template: &str,
        resuming: bool,
        migrated_md: Option<Vec<u8>>,
    ) -> Step<Option<ConfigChange>> {
        let md_path = metadata::vk_path(self.env.dir);
        let mut meta = match migrated_md {
            Some(bytes) => {
                let parsed = String::from_utf8(bytes)
                    .map_err(|e| e.to_string())
                    .and_then(|t| Metadata::parse(&t).map_err(|e| e.to_string()));
                parsed.map_err(|e| self.internal(format!("{}: {e}", self.rel(&md_path))))?
            }
            None => match Metadata::load(&md_path) {
                Ok(m) => m,
                Err(metadata::Error::Missing { .. }) => return Ok(None),
                Err(metadata::Error::TooNew { file, too_new }) => {
                    return Err(self.too_new(&file, &too_new));
                }
                Err(e) => return Err(self.failed(&md_path, e.message(), e.to_string())),
            },
        };
        let Some(record) = meta.get(CONFIG_TOML).cloned() else {
            return Ok(None);
        };
        // 只拿 `config.toml` 的紀錄去判：同一份紀錄檔裡根目錄檔的紀錄不是這次的新版。
        let mut only = Metadata::new();
        only.put(record.clone())
            .map_err(|e| self.internal(e.to_string()))?;
        let root = self.env.dir.root().to_path_buf();
        let copy = self.env.dir.config_baseline();
        let file = InitFile {
            path: CONFIG_TOML,
            strategy: Strategy::Whole,
            contents: template.as_bytes(),
        };
        let planned = initfiles::plan(
            initfiles::Command::Upgrade,
            &[file],
            &only,
            |p| read_optional(&root.join(p)),
            |_| read_optional(&copy),
        );
        let mut planned = planned.map_err(|e| self.internal(e.to_string()))?;
        let Some(mut plan) = planned.files.drain(..).find(|f| f.path == CONFIG_TOML) else {
            return Err(self.internal(format!("no plan for {CONFIG_TOML}")));
        };

        // 中斷後恢復：上一次已把模板寫進 `config.toml`、還沒推基準版與紀錄，補上（模組說明「config.toml」）。
        let mut adopted = false;
        if resuming && plan.verdict == Verdict::Gap(Gap::CurrentIsNew) {
            let now = read_optional(&self.env.dir.config_toml());
            let now = now.map_err(|e| self.internal(format!("{CONFIG_TOML}: {e}")))?;
            let now = now.ok_or_else(|| self.internal(format!("{CONFIG_TOML} disappeared")))?;
            let mut r = record.clone();
            r.hash = Some(FileHash::of(&now));
            plan.baseline = Some(template.as_bytes().to_vec());
            plan.record = Some(r);
            plan.conflict = Some(false);
            adopted = true;
        }
        if let (Verdict::Gap(gap), false) = (plan.verdict, adopted) {
            return Err(self.gap(format_args!(
                "{CONFIG_TOML} in the second stage of the engine upgrade ({gap:?})"
            )));
        }

        let mut changed = false;
        if let Some(r) = &plan.record {
            meta.put(r.clone())
                .map_err(|e| self.internal(e.to_string()))?;
            changed = true;
        }
        if let Some(c) = plan.conflict {
            let set = meta.set_conflict(CONFIG_TOML, c);
            changed |= set.map_err(|e| self.internal(e.to_string()))?;
        }
        if let Some((before, after)) = plan
            .write
            .as_ref()
            .and_then(|w| Some((w.before.as_deref()?, w.after.as_slice())))
        {
            match meta.record_write(CONFIG_TOML, before, after) {
                Ok(metadata::WriteOutcome::Updated) => changed = true,
                Ok(_) => {}
                Err(e) => return Err(self.internal(e.to_string())),
            }
        }
        let metadata = if changed {
            let text = meta.render(self.env.written_by);
            Some(text.map_err(|e| self.internal(e.to_string()))?.into_bytes())
        } else {
            None
        };
        let question = plan
            .ask
            .map(|a: Ask| text::question(ENGINE_NAME, CONFIG_TOML, a));
        Ok(Some(ConfigChange {
            plan,
            adopted,
            question,
            metadata,
        }))
    }

    /// `config.toml` 這次的 stdout 字句（同 `upgrade <repo>` 的初始檔字句）。
    fn config_lines(&mut self, config: Option<&ConfigChange>, tag: Tag) {
        let Some(c) = config.filter(|c| !c.adopted) else {
            return;
        };
        let dry = self.dry_run;
        if let Some(line) = text::file_line(&c.plan, dry) {
            self.say(&line);
        }
        if let Some(line) = text::listed_line(ENGINE_NAME, tag, &c.plan, dry) {
            self.say(&line);
        }
    }

    /// 引擎開著本機覆寫時停下（模組說明「缺口」）。
    fn no_engine_override(&mut self) -> Step<()> {
        match LocalFile::load_from(self.env.dir) {
            Ok(Some(local)) if local.engine().is_some() => Err(self.gap(
                "the second stage of the engine upgrade while the engine has a local override \
                 (dev --engine)",
            )),
            Ok(_) => Ok(()),
            Err(version_file::Error::Parse {
                file,
                source: version_file::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => Err(self.too_new(&file, &t)),
            Err(e) => Err(self.internal(e.to_string())),
        }
    }

    /// 第二段一次問完（帶 `-y` 全部同意）；全部同意回真，答否回假，不能互動回 VK0002。
    fn engine_ask(&mut self, questions: &[String], yes: bool) -> Step<bool> {
        let tty = TtyState {
            stdin: self.env.tty.stdin,
            stderr: self.env.tty.stderr,
        };
        let consent = if yes {
            Consent::AssumeYes
        } else {
            Consent::Ask
        };
        let answers = prompt::ask_all(
            questions,
            consent,
            &tty,
            &mut *self.env.stdin,
            &mut *self.env.prompt,
        );
        match answers {
            Ok(a) => Ok(a.all_yes()),
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

    /// 「現有檔案版」列的 VK 檔，`version.toml` 排第一。
    fn vk_files(&mut self, lockfile: &LockFile) -> Step<Vec<PathBuf>> {
        let dir = self.env.dir;
        let mut paths: Vec<PathBuf> = vec![
            dir.version_toml(),
            dir.version_local_toml(),
            metadata::vk_path(dir),
        ];
        for repo in lockfile.tools().keys() {
            paths.push(self.meta_path(repo)?);
            paths.push(stamp::tool_file(dir, repo));
        }
        Ok(paths)
    }

    /// 現有 VK 檔的最高檔案版（模組說明「現有檔案版」）。
    fn existing_schema(&mut self, lockfile: &LockFile) -> Step<u32> {
        let mut max = 0;
        for path in self.vk_files(lockfile)? {
            if let Some(n) = self.schema_of(&path)? {
                max = max.max(n);
            }
        }
        Ok(max)
    }

    /// 一個 VK 檔的內容；檔不在回 `None`。
    fn read_vk(&mut self, path: &Path) -> Step<Option<String>> {
        match fs::read_to_string(path) {
            Ok(t) => Ok(Some(t)),
            Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(None),
            Err(e) => Err(self.internal(format!("{}: {e}", self.rel(path)))),
        }
    }

    /// 一個 VK 檔的檔案版；檔不在回 `None`。
    fn schema_of(&mut self, path: &Path) -> Step<Option<u32>> {
        let Some(text) = self.read_vk(path)? else {
            return Ok(None);
        };
        match schema::Document::parse_with(&text, &ANY_SCHEMA) {
            Ok(doc) => Ok(Some(doc.schema())),
            Err(e) => Err(self.internal(format!("{}: {e}", self.rel(path)))),
        }
    }

    /// 一個 VK 檔升到本引擎的檔案版上限；檔不在或已是上限回 `None`，升了回原檔案版與新內容。
    fn migrate_file(&mut self, path: &Path) -> Step<Option<(u32, String)>> {
        let Some(text) = self.read_vk(path)? else {
            return Ok(None);
        };
        let written_by = self.env.written_by;
        match migrate::migrate(&text, &compat::THIS, migrate::MIGRATIONS, written_by) {
            Ok(migrate::Outcome::Current) => Ok(None),
            Ok(migrate::Outcome::Migrated { from, text }) => Ok(Some((from, text))),
            Err(r) => Err(self.internal(format!("{}: {r}", self.rel(path)))),
        }
    }

    /// 容器內路徑換成相對於 `.vendor_kit/` 的寫法（`txn` 的紀錄檔路徑）。
    fn vk_rel(&mut self, path: &Path) -> Step<PathBuf> {
        match path.strip_prefix(self.env.dir.vk_dir()) {
            Ok(p) => Ok(p.to_path_buf()),
            Err(_) => Err(self.internal(format!("{} is not under .vendor_kit", path.display()))),
        }
    }

    /// 引擎升級的進度檔：共同欄位之外記 `[upgrade]` 表的 `target` 與 `image`。
    fn engine_progress(&mut self, image: &ImageRef) -> Step<Progress> {
        let mut p = match Progress::new(VERB, self.env.run_id, self.env.argv) {
            Ok(p) => p,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let doc = p.document_mut();
        let set = doc
            .set(&[table::TABLE, table::TARGET], table::ENGINE_TARGET)
            .and_then(|()| doc.set(&[table::TABLE, table::IMAGE], image.to_string()));
        set.map_err(|e| self.internal(e.to_string()))?;
        Ok(p)
    }

    /// 建進度檔、換引擎鎖定行；不刪進度檔（模組說明第 9 步）。
    fn switch(&mut self, progress: Progress, lockfile: &mut LockFile) -> Step<()> {
        let result = {
            let mut fx = Disk::new(self.env.dir, self.env.log, self.env.written_by);
            Txn::begin(&mut fx, progress).and_then(|t| {
                t.swap_cache(&[])?
                    .write_repo_files(&[])?
                    .write_records(&[])?
                    .write_tools_just(None)?
                    .write_lock_line(lockfile, Target::Engine)
                    .map(|_| ())
            })
        };
        result.map_err(|f| self.internal(f.to_string()))
    }
}
