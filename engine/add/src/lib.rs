//! `add` 指令（04 指令表 `add <repo>`、`add <repo>@<tag>`、`add <repo> -i <image>`）：從參數到落地。
//!
//! 呼叫端（入口 `vendor_kit`）已解析好參數、判過安裝目錄（VK0028），並接好執行紀錄與 `plan` 往返。
//! 這裡依序做：
//!
//! 1. `add vendor_kit` 看參數字面就擋（VK0057），不取件。
//! 2. 讀 `.vendor_kit/config.toml`（VK0059），在第一次取鎖之前（04 設定）。
//! 3. 取安裝目錄的排他鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束。
//! 4. 讀 `version.toml` 與 `version.local.toml`（檔案版過高回 VK0008）；有工具的覆寫就讀它的本機開發來源，
//!    讀不到回 VK0052（見「本機覆寫」）。
//! 5. 備好殘留進度檔的恢復（04 成對與無害：可寫 recipe 先恢復再判是否重複）：重新取件、驗證，算好恢復
//!    之後的版本鎖定行與入口檔，只讀不寫；之後的判定都看恢復之後的樣子。恢復跟這次的詢問一起問完（04
//!    共同選項：全部同意才寫入，含恢復舊操作），恢復本身不寫 repo 檔、沒有要問的事。恢復只在這次以 0
//!    結束、要寫入時才落地（導入完成或未變更），排在這次自己的落地之前；答否、不能互動或停下時恢復也
//!    不寫，殘留的進度檔照留。做法見 `Add::recover`、`Add::land_recoveries`。
//! 6. 判來源：`-i <本機 image 引用>`、`-i <path>.tar`（見「image tar」），或不帶 `-i` 的線上 `add`（見「線上解析」）。
//! 7. 已在版本鎖定行：tag 不同回 VK0045；完全相同 stdout 說明未變更，以 0 結束。線上 `add` 已在版本鎖定行
//!    而不帶 tag 也是未變更（已完整導入，04 成對與無害），不連 registry、不送 docker 動作。
//! 8. `-i <本機 image 引用>`：經 `plan` 協定請啟動器 `inspect`（讀 Id 與 RepoDigests；沒有對應的 digest 回
//!    VK0031）。`-i <path>.tar`：`stage` 旁檔、`load`、`inspect`（見「image tar」）。線上：解析 tag 與 digest，
//!    必要時 `pull`（見「線上解析」）。之後以 image ID `extract`；docker 動作失敗回 VK0055。
//! 9. `fetch::verify`：digest、dist 格式、逐檔指紋、`<ns>` 撞名（VK0030，對象是已裝工具、根
//!    `justfile` 的 recipe 與 module、保留名 `vendor_kit`）。
//! 10. `initfiles` 算出每個初始檔的動作與問題，`prompt` 一次問完：答否是正常取消（stdout 說明未變更，
//!     以 0 結束）；不能互動回 VK0002，除執行紀錄外不寫任何檔。帶 `-y` 時其他詢問都同意、不問，但 `-y`
//!     不擴大授權（04 寫入既有檔的例外）：
//!     - append 進已存在、尚未納管的檔那幾題照樣要問（`-y` 不能把它改成 append 納管）；有終端就只問
//!       這幾題，答否同樣是正常取消。不能互動時，VK0002 的下一步會是同一個指令，所以改以 VK0056 停下，
//!       `<reason>` 列出這些檔、結尾是 [`DRAFT_YES_APPEND`]（見缺口）。
//!     - 已存在、不適用 append 的檔照樣不納管、不覆蓋（VK0018），已記成未納管的檔照樣不處理（VK0019）。
//! 11. 重驗暫存內容（ADR-0006 第三層），再經 `txn` 依序落地：`cache/<repo>/` 與印記、repo 檔、
//!     紀錄檔（metadata、基準版副本）、`gen/tools.just`、版本鎖定行，最後刪進度檔。
//! 12. stdout 列出改了什麼；初始檔的警告（VK0018 等）照印。
//!
//! # 預演（`--dry-run`，#372 N11）
//!
//! 語意是這一版自訂的（契約沒寫，列給維護者確認）：照上面的順序算出完整計畫，到第 10 步為止都一樣，
//! 差別只在：
//!
//! - 取安裝目錄的共享鎖，不取排他鎖（只讀）。
//! - 不問（第 10 步整段跳過，不能互動也不報 VK0002），不重驗暫存內容，不落地（第 11 步），不建進度檔；
//!   除執行紀錄外不寫安裝目錄裡的任何檔。
//! - 恢復殘留的 `add` 只印會完成哪一份（[`text::would_recover`]），殘留的進度檔照留。
//! - stdout 照實際執行的順序印會改的內容（覆寫報告、[`text::would_add`]、每個初始檔的
//!   [`text::would_file_line`]；未變更時照樣印未變更），最後一行是 `prompt::DRY_RUN_DONE`，以 0 結束。
//!   初始檔的警告（VK0018 等）照印。
//! - 跟 `-y` 並用時 `-y` 沒有作用（反正不問）。
//! - 算計畫要用的 docker 動作照送：`inspect`、`pull`、`load`、`stage`、`stage-dir`、`extract`。它們動到的是
//!   主機的 image store 與 session 目錄，不是安裝目錄。
//! - 算計畫時遇到的停下（VK0045、VK0030、VK0057、缺口等）照樣以各自的結束碼停下。
//!
//! # 本機覆寫
//!
//! `version.local.toml` 有其他工具的覆寫（`dev <repo> -p <dir>`）時照常導入（04 本機覆寫：除 `test` 外的一般
//! recipe 照常執行），重產 `gen/tools.just` 的做法跟 engine/sync、engine/upgrade 一致：
//!
//! - 每個覆寫的 `<ns>` 從本機開發來源讀（`fetch::local`，值照 engine/dev 以安裝目錄為準正規化），不讀那個
//!   工具的 `cache/<repo>/`。安裝目錄外的（`dev` 收的絕對路徑，或開頭是 `..` 的相對路徑）引擎看不到，照
//!   engine/dev 請啟動器 `stage-dir` 複製進 session 目錄的 `in/<slot>`，再讀那份複本。讀不到回 VK0052（04 本機
//!   覆寫：覆寫來源失效只擋需讀它的動作；重產 `gen/tools.just` 要讀它），列出每個讀不到的覆寫，在恢復、
//!   任何 docker 動作與寫入之前停下。
//! - `gen/tools.just` 裡開著覆寫的工具那幾行指向本機開發來源（`tools_just::render_with`，恢復殘留 `add` 的
//!   重產也一樣）；撞名判定裡開著覆寫的工具也以本機開發來源的 `<ns>` 為準（入口檔裡生效的是它）。
//! - 每次以 0 結束時（導入完成、已導入同一版、答否取消）都在 stdout 報告用了哪個覆寫，排在那條路徑的字句
//!   前面（04 本機覆寫：不加診斷前綴，`update` 以外到 stdout）；停下時只印診斷。恢復殘留 `add` 的字句在恢復
//!   落地時印，排在覆寫報告前面。
//! - 覆寫指到不在版本鎖定行的工具（孤兒覆寫）見「缺口」；引擎的覆寫與導入工具無關，不看。
//!
//! # 線上解析（N2、N53）
//!
//! 不帶 `-i` 時，工具 image 的 `<registry>/<路徑>`：
//!
//! - 已有版本鎖定行：一律讀鎖定行的路徑，`--image-path` 不看（第 7 步：這時不會走到 registry）。
//! - 沒有版本鎖定行：取 `--image-path`（`args` 已驗過是 `ghcr.io/<路徑>`、不帶 tag 或 digest，不合是 VK0026）；
//!   沒給就回 VK0025，`<argument>` 是 [`IMAGE_PATH_ARGUMENT`]。`<repo>` 怎麼對到 GHCR 路徑契約沒定（N2b），
//!   選項名稱也是暫定。
//!
//! 之後跟 engine/upgrade 同一套做法，registry 只經 `registry` crate，不用任何查詢快取：
//!
//! - 不帶 tag：列 tag（帶 token 時用它）→ 取最新版（[`imageref::Tag::latest`]）→ inspect 本機
//!   `<registry>/<路徑>:<最新版>`。本機有：再以同一個查詢（沿用換到的 bearer）取 registry 上這個 tag 的 digest，
//!   跟本機的比對；本機沒有：取 digest 後 pull。
//! - `@<tag>`：先 inspect 本機，本機有就用它、不連 registry（指定 tag 不查清單，也不讀 token 檔；離線照樣
//!   能用）。本機沒有才匿名取 registry 上這個 tag 的 digest，再 pull。
//! - pull 一律用帶 digest、不帶 tag 的引用 `<registry>/<路徑>@<digest>`，之後也以同一個引用 inspect：
//!   以 digest pull 的 image 不會帶上 tag，拿 `<路徑>:<tag>` 去 inspect 會找不到。
//! - 版本鎖定行的值是 `<registry>/<路徑>:<tag>@<digest>`；之後的取件、驗證、詢問、落地跟 `-i` 相同。
//!
//! 無法唯一判定 digest 就停下（02 不變量 12），在任何寫入之前：
//!
//! - 本機 image 的 RepoDigests 沒有這個 `<registry>/<路徑>` 的 digest（例如本機建置、從 tar 載入）：VK0031，
//!   `<image>` 是 `<registry>/<路徑>:<tag>`，`<reason>` 是 [`text::DIGEST_MISSING`]。
//! - 同一個 tag 指向不同 digest（本機 RepoDigests 有兩個以上不同的 digest，或本機的跟 registry 的不同）：
//!   拒絕。草稿碼 VK0078 還沒登錄，先以 VK0056 停下，`<reason>` 寫明各個 digest，結尾是 [`DRAFT_TAG_DIGESTS`]。
//!
//! # image tar（ADR-0009、N43）
//!
//! `-i` 的值以 [`TAR_SUFFIX`] 結尾就當 image tar，其他當 image 引用（同 `launcher/bootstrap_main.sh`）。相對路徑
//! 以安裝目錄為準（`add` 只在安裝目錄執行，VK0028），換成主機上的絕對路徑交給啟動器。依序：
//!
//! 1. 同名旁檔 `<path>.digest`（`foo.tar` → `foo.digest`，[`digest_sidecar`]）以 `stage` 複製進
//!    `in/`[`DIGEST_SLOT`] 再讀。旁檔要是一行多架構 index digest（[`parse_digest`]，規則同 bootstrap.sh）；
//!    `stage` 失敗（含旁檔不存在）或格式不合回 VK0031，`<image>` 是使用者給的值，`<reason>` 是
//!    [`text::DIGEST_MISSING`]。這一步在 `load` 之前，旁檔缺就不載入、不寫任何檔（ADR-0009 驗收）。
//! 2. `load` 載入；失敗回 VK0055。從 `res.<seq>.out`（`docker load -q` 的 stdout）拿 image：要剛好一行
//!    `Loaded image ID: <id>` 或 `Loaded image: <ref>`（[`parse_load`]）。
//! 3. inspect 那個 ID 或引用，取 Id；`<registry>/<路徑>:<tag>` 取自 load 報告的引用，報告的是 ID 時取自
//!    inspect 的 RepoTags（[`tar_tags`]：`-i <本機 image 引用>` 收得下的、不重複的要剛好一個）。
//! 4. 版本鎖定行的值是 `<registry>/<路徑>:<tag>@<旁檔的 digest>`。digest 只取自旁檔、不跟 RepoDigests 比對：
//!    單一平台的 tar 本來就沒有 index digest（ADR-0009）。之後的 VK0045、未變更判定、取件、驗證、詢問、落地
//!    跟 `-i <本機 image 引用>` 相同。
//!
//! # registry token 檔（04 registry token 檔案）
//!
//! `--registry-token-file <path>` 只在線上、不帶 tag、真的要列 tag 時才讀，一次執行只讀一次；`@<tag>`、`-i`
//! 都不讀、不送 `stage`。路徑判定照抄 engine/update（[`locate`]）：落在安裝目錄裡就直接讀；在外面就請啟動器
//! `stage` 複製進 `in/`[`TOKEN_SLOT`] 再讀那份複本。讀不到或去掉前後空白後是空的：VK0055，`<source>` 是使用者
//! 給的路徑，在連 registry 之前停下。往返本身出錯是 VK 的錯，以 VK0056 停下。
//!
//! # 查詢失敗（訊息表 VK0001、VK0055、VK0058）
//!
//! `registry` 的錯誤類別照它的模組說明對應，`<target>` 是 `<repo>`：
//!
//! - 列 tag 時沒帶 token、registry 要求認證：VK0001，`<cmd>` 印 [`VK0001_CMD`]。
//! - 列 tag 的其他錯誤（token 被拒、網路或逾時、404、回應不合協定）：VK0055，`<source>` 是查的
//!   `<registry>/<路徑>`。被拒後不改走匿名重試。
//! - 列得到 tag、但沒有一個是合法的 `vX.Y.Z`：VK0058（情境寫的是 update，同一種情況擴到 add，契約文字待補）。
//! - 取 tag 的 digest 失敗（含要求認證）：VK0055，`<source>` 是 `<registry>/<路徑>:<tag>`。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 印記放在 `.vendor_kit/cache/<repo>.stamp.toml`（[`stamp_file`]）：在 `cache/` 底下所以不進 git，
//!   又不在 `cache/<repo>/` 裡，換 `cache/<repo>/` 時不會被帶走。
//! - 基準版副本放在 `.vendor_kit/baseline/<repo>/<初始檔的 repo 相對路徑>`（[`baseline_file`]）。
//! - 進度檔 `.tmp.add.<run-id>.toml` 另記 `[add]` 表的 `repo`、`image`（版本鎖定行的值）與
//!   `repo_files`（這次有沒有要寫 repo 檔），以及這次要寫的每個 repo 檔（`[[repo_file]]` 的路徑、動作、
//!   寫入前後內容的 hash；格式定在 `progress::repo_files`）。
//! - 取件的 slot 名是 [`SLOT_PREFIX`] 加這次執行裡的序號（`tool1`、`tool2`…）：啟動器不收已存在的
//!   slot，恢復好幾份殘留時每次取件都要一個新的。token 檔 `stage` 的 slot 是 [`TOKEN_SLOT`]，image tar 的
//!   `.digest` 旁檔是 [`DIGEST_SLOT`]。
//! - 同一個 tag 指向不同 digest 的 `<reason>` 字句（[`text::tag_digests`]）。
//! - stdout 的字句與詢問文字（英文）見 [`text`]；覆寫的報告字句跟 engine/sync 相同（[`text::local_override`]）。
//! - 本機開發來源的正規化與檢查跟 engine/dev、engine/sync、engine/upgrade 共用 `fetch::local`；`stage-dir` 的
//!   slot 另外編號（`fetch::local::STAGE_SLOT_PREFIX`，`dev1`、`dev2`…）。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - `<repo>` 對應到哪個 GHCR 路徑沒定（N2b）：沒有版本鎖定行時要使用者給 `--image-path`（名稱暫定）。
//! - registry 列得到、但一個 tag 都沒有：照 engine/update 當查詢失敗，報 VK0055，`<reason>` 寫 [`text::NO_TAGS`]。
//! - 取 digest 時不檢查 manifest 的 media type 是不是多架構 index（`registry` 把判斷交給呼叫端，契約沒定）。
//! - `@<tag>` 而本機沒有、package 又是私有的：04 規定指定 tag 不讀 token 檔，匿名取 digest 會被拒，報 VK0055；
//!   pull 本身用的是主機的 Docker 認證。帶 token 的流程還沒對私有 package 手動測過（`registry` 的缺口）。
//! - `-i` 的引用沒有 tag、tag 不是 `vX.Y.Z`、已帶 digest、不在 ghcr.io，或 `-i` 與 `@<tag>` 並用。
//! - image tar：`docker load` 沒報告剛好一個 image；載入的 image 沒有、或有好幾個 `ghcr.io/<路徑>:vX.Y.Z`
//!   的名稱（無名 tar 的 RepoTags 只剩本機原有的名稱，可能對不到）。
//! - image tar 導入之後（同 bootstrap.sh 首次導入的已知缺口）：classic image store 載入 tar 後沒有 RepoDigests，
//!   之後的 recipe 以版本鎖定行的 `<路徑>@<digest>` 找不到 image、改去 pull，離線時失敗；恢復中斷的 `add`
//!   也以同一個引用 inspect，找不到回 VK0055。containerd image store 載入保留 index 的 tar 時才找得到。
//! - 工具交付 `init.toml`：初始檔的清單與 `strategy` 寫在哪裡、什麼格式都沒定（ADR-0003 只提到
//!   `strategy = "append"`），所以讀不出初始檔；沒有 `init.toml` 的工具就沒有初始檔、沒有詢問。
//! - 根 `justfile` 的 recipe 與 module 只做保守的逐行掃描（引擎 image 沒有 just），限制見 `justfile` 模組。
//! - 其他已裝、沒開覆寫的工具的 `cache/<repo>/` 讀不到（N4）：撞名判定與入口檔都要它的 `<ns>`。
//!   只在真的要導入（或恢復殘留的 `add`）、要讀其他工具時才讀，在落地之前收齊全部讀不到的工具
//!   一起報（`fetch::CacheCheck`）：
//!   不在的合成一則、下一步 `run just vendor_kit sync first`；讀不到或損壞的各一則、保留實際原因。
//!   兩種的草稿碼登錄前以 VK0056 停下，`<reason>` 結尾寫明草稿碼（`fetch::DRAFT_CACHE_MISSING`、
//!   `fetch::DRAFT_CACHE_UNREADABLE`）。
//! - 覆寫指到不在版本鎖定行的工具（孤兒覆寫）：訊息表沒有代碼（`version_file::OrphanOverrides`）；開著覆寫的
//!   工具交付保留名 `vendor_kit`：沒有代碼（同 engine/upgrade）。
//! - 同一個 tag 的版本鎖定行指向別的 digest；`<repo>` 不是 just 名稱；`initfiles` 判成缺口的檔。
//! - 殘留的進度檔不是 `add` 的（04 說可寫 recipe 先恢復，`add` 怎麼恢復別的指令沒定），或殘留的 `add` 要寫
//!   repo 檔：寫了哪些已記在進度檔，但重新落地要讀 `init.toml`，格式沒定（見上）。
//! - 中途寫檔失敗沒有代碼（計畫 G4）；dist 格式不符（G2）、指紋不符（G1）沒有代碼。
//! - `-y` 照「可能詢問才接受」收（#372 N14），04 的已定組合還沒列進 `add`，待維護者確認。帶 `-y` 又不能
//!   互動、卻有 append 進既有檔的詢問：訊息表沒有代碼（草稿碼 VK0084），沒帶 `-y` 時 VK0002 的下一步
//!   照著跑會停在這裡。
//!
//! 這裡不直接碰 docker：docker 動作與 `stage`、`stage-dir` 一律是 `plan` 協定的 op，由啟動器代做。

mod justfile;
mod source;
pub mod text;
mod token;

#[cfg(test)]
mod tests;

use std::collections::BTreeMap;
use std::ffi::OsStr;
use std::fs;
use std::io::{self, BufRead, Write};
use std::os::unix::ffi::OsStrExt;
use std::path::{Path, PathBuf};
use std::time::Duration;

use config::{Config, ConfigError};
use diagnostics::{Diagnostic, Diagnostics, Message, Sink};
use fetch::{Candidate, Staged, Taken};
use filelock::{Lock, Mode};
use imageref::{ImageRef, Tag};
use initfiles::{Ask, FilePlan, InitFile, Strategy};
use layout::InstallDir;
use metadata::Metadata;
use plan::{Channel, Field, ImageId, Op, Outcome, Slot, Tty};
use progress::Progress;
use progress::repo_files::{self, RepoFile as WrittenFile};
use prompt::{Consent, PromptError, TtyState};
use registry::{Client, ErrorKind, Repository, Token};
use runlog::Target;
use txn::{Disk, RecordFile, RepoFile, ToolContent, Txn};
use version_file::{LocalFile, LockFile, Versions};

pub use source::{
    DIGEST_SUFFIX, Inspected, Loaded, LocalRef, RepoDigest, TAR_SUFFIX, digest_for, digest_sidecar,
    is_tar, parse_digest, parse_inspect, parse_load, parse_local, repo_digest, tar_tags,
};
pub use token::{TokenPath, locate};

/// 進度檔的 `<verb>`。
pub const VERB: &str = "add";
/// 進度檔裡 `add` 自己的表。
pub const PROGRESS_TABLE: &str = "add";
/// 取件的 slot 名前綴，後面接這次執行裡的序號（從 1 起）。
pub const SLOT_PREFIX: &str = "tool";
/// 工具交付初始檔清單的檔名（格式未定，見模組說明的缺口）。
pub const INIT_TOML: &str = "init.toml";
/// token 檔在安裝目錄外時，`stage` 放進 `in/` 的 slot 名（同 engine/update）。
pub const TOKEN_SLOT: &str = "token";
/// image tar 的 `.digest` 旁檔 `stage` 放進 `in/` 的 slot 名（模組說明「image tar」）。
pub const DIGEST_SLOT: &str = "digest";
/// VK0001 的 `<cmd>`（訊息表：add 時印 add）。
pub const VK0001_CMD: &str = "add";
/// 線上 `add` 沒有版本鎖定行又沒給 `--image-path`：VK0025 的 `<argument>`（選項名稱暫定，N2b）。
pub const IMAGE_PATH_ARGUMENT: &str = "--image-path";
/// 同一個 tag 指向不同 digest：草稿碼 VK0078（N53）登錄前，以 VK0056 停下時 `<reason>` 的結尾。
pub const DRAFT_TAG_DIGESTS: &str = "reason code pending (draft VK0078, N53)";
/// 帶 `-y` 又不能互動、卻有要 append 進既有檔的詢問：草稿碼 VK0084（N14）登錄前，以 VK0056 停下時
/// `<reason>` 的結尾。
pub const DRAFT_YES_APPEND: &str = "reason code pending (draft VK0084, N14)";

/// 一次 `add` 的參數（`args::Command::Add`）。
#[derive(Debug, Clone, Copy)]
pub struct Request<'a> {
    pub repo: &'a str,
    pub tag: Option<Tag>,
    pub image: Option<&'a OsStr>,
    /// 有沒有帶 `-y`：全部詢問都同意（模組說明第 10 步）。
    pub yes: bool,
    /// 有沒有帶 `--dry-run`：算出完整計畫後只印、不問、不寫（模組說明「預演」）。
    pub dry_run: bool,
    /// `--image-path` 的值（`args` 已驗過是 `ghcr.io/<路徑>`）；只在線上、沒有版本鎖定行時用。
    pub image_path: Option<&'a str>,
    /// `--registry-token-file` 的值，原樣；只在線上、不帶 tag、要列 tag 時才讀（模組說明「registry token 檔」）。
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
    /// 線上 `add` 列 tag 與取 digest 用的 registry client（模組說明「線上解析」）。
    pub registry: &'a Client,
    pub tty: Tty,
    /// `just vendor_kit` 之後的參數原樣（第一個是 `add`）。
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

/// 印記檔：`.vendor_kit/cache/<repo>.stamp.toml`（[`stamp::tool_file`]，與 `sync` 共用）。
pub fn stamp_file(dir: &InstallDir, repo: &str) -> PathBuf {
    stamp::tool_file(dir, repo)
}

/// 基準版副本相對於 `.vendor_kit/` 的路徑：`baseline/<repo>/<path>`。
pub fn baseline_file(repo: &str, path: &str) -> PathBuf {
    Path::new("baseline").join(repo).join(path)
}

/// 跑一次 `add`，回傳結束碼。
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
    let mut add = Add {
        env,
        init,
        yes: req.yes,
        dry_run: req.dry_run,
        code: 0,
        extracts: 0,
        stages: 0,
        local: BTreeMap::new(),
        pending: Vec::new(),
    };
    let _ = add.run(req);
    add.code
}

/// 診斷已印、這次執行停下。
struct Stop;

type Step<T> = Result<T, Stop>;

/// 開著本機覆寫的一個工具：正規化後的本機開發來源與它交付的 `<ns>`。
struct Local {
    dir: String,
    namespaces: Vec<String>,
}

/// 照殘留進度檔備好、還沒落地的恢復（模組說明第 5 步）：取件、驗證過，入口檔與版本鎖定行也算好了。
struct Recovery {
    /// 殘留的進度檔，這次落地完成之後才刪。
    entry: progress::Entry,
    repo: String,
    locked: ImageRef,
    candidate: Candidate,
    /// 恢復當下的 `gen/tools.just`。
    tools_just: String,
    /// 恢復之後的版本鎖定行。
    lockfile: LockFile,
}

/// 撞名判定與入口檔要用的已裝工具資訊。
struct Installed {
    taken: Taken,
    /// 其他已裝工具的 `<ns>`。
    namespaces: BTreeMap<String, Vec<String>>,
}

struct Add<'r, 'a, W: Write, S: Sink, L: Write> {
    env: &'r mut Env<'a, W, S, L>,
    init: InitSource<'r>,
    /// 有沒有帶 `-y`（[`Request::yes`]）。
    yes: bool,
    /// 預演（[`Request::dry_run`]）。
    dry_run: bool,
    code: u8,
    /// 這次執行已用掉的 slot 數。
    extracts: u32,
    /// 這次執行已用掉的 `stage-dir` slot 數。
    stages: u32,
    /// 開著覆寫的工具（模組說明「本機覆寫」）。
    local: BTreeMap<String, Local>,
    /// 備好、等這次的詢問全部同意才落地的恢復，依進度檔的順序。
    pending: Vec<Recovery>,
}

impl<W: Write, S: Sink, L: Write> Add<'_, '_, W, S, L> {
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

    /// 預演時印收尾的那一行（模組說明「預演」）；不是預演就不印。
    fn dry_run_done(&mut self) {
        if self.dry_run {
            self.say(prompt::DRY_RUN_DONE);
        }
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

    /// 這次全部工具的 `gen/tools.just`：開著覆寫的工具那幾行指向本機開發來源。
    fn entry(&mut self, all: &BTreeMap<String, Vec<String>>) -> Step<String> {
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

    // ---- 流程 ----

    fn run(&mut self, req: &Request) -> Step<()> {
        if req.repo == fetch::RESERVED {
            return Err(self.stop(Diagnostic::new(&messages::VK0057)));
        }
        if !fetch::is_namespace(req.repo) {
            return Err(self.gap(format_args!("tool name {:?} (not a just name)", req.repo)));
        }
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        let mut lockfile = self.lockfile()?;
        self.local = self.local(&lockfile)?;
        self.recover_all(&mut lockfile)?;

        let local = match (req.image, req.tag) {
            (None, _) => return self.online(req, lockfile),
            (Some(_), Some(_)) => return Err(self.gap("add -i together with <repo>@<tag>")),
            (Some(image), None) if is_tar(image) => {
                return self.add_tar(req.repo, image, lockfile);
            }
            (Some(image), None) => {
                let given = image.to_string_lossy();
                parse_local(&given).map_err(|reason| self.gap(reason))?
            }
        };

        if let Some(current) = lockfile.tool(req.repo).cloned()
            && current.tag() != local.tag
        {
            return Err(self.already_at(req.repo, local.tag, &current));
        }

        let pinned = self.inspect(req.repo, &local)?;
        self.settle(req.repo, local.tag, pinned, lockfile)
    }

    /// `-i` 已定出版本鎖定行的值與 image ID：比對版本鎖定行（不同 tag 回 VK0045；完全相同是未變更；同 tag
    /// 不同 digest 是缺口），之後取件與落地。
    fn settle(
        &mut self,
        repo: &str,
        tag: Tag,
        (locked, id): (ImageRef, ImageId),
        lockfile: LockFile,
    ) -> Step<()> {
        if let Some(current) = lockfile.tool(repo).cloned() {
            if current.tag() != tag {
                return Err(self.already_at(repo, tag, &current));
            }
            if current == locked {
                self.land_recoveries()?;
                self.report_overrides();
                self.say(&text::unchanged(repo, &locked));
                self.dry_run_done();
                return Ok(());
            }
            return Err(self.gap(format_args!(
                "add with tag {tag} whose digest differs from the lock version line"
            )));
        }
        let candidate = self.fetch(repo, &id, &locked, &lockfile)?;
        self.import(repo, &locked, candidate, lockfile)
    }

    /// `-i <path>.tar`（模組說明「image tar」）。
    fn add_tar(&mut self, repo: &str, given: &OsStr, lockfile: LockFile) -> Step<()> {
        let shown = given.to_string_lossy().into_owned();
        let host = match locate(given, self.env.host_root) {
            TokenPath::Inside(rel) => {
                let mut h = self.env.host_root.trim_end_matches('/').as_bytes().to_vec();
                if !rel.as_os_str().is_empty() {
                    h.push(b'/');
                    h.extend_from_slice(rel.as_os_str().as_bytes());
                }
                h
            }
            TokenPath::Outside(h) => h,
        };
        let digest = self.tar_digest(&digest_sidecar(&host), &shown)?;
        let loaded = self.load(host, &shown, repo)?;
        let (wire, named) = match &loaded {
            Loaded::Id(id) => (
                ImageId::parse(id).and_then(|i| plan::ImageRef::parse(i.as_str())),
                None,
            ),
            Loaded::Ref(r) => (plan::ImageRef::parse(r), Some(r.clone())),
        };
        let Some(wire) = wire else {
            return Err(self.gap(format_args!(
                "add -i with an image tar whose loaded image is reported as {loaded:?}"
            )));
        };
        let inspected = self.inspect_ref(wire, &shown, repo)?;
        let candidates = named.map_or_else(|| inspected.repo_tags.clone(), |r| vec![r]);
        let local = match tar_tags(&candidates).as_slice() {
            [one] => one.clone(),
            [] => {
                return Err(self.gap(format_args!(
                    "add -i with an image tar whose image has no ghcr.io/<path>:vX.Y.Z name \
                     (names: {candidates:?})"
                )));
            }
            many => {
                let names: Vec<&str> = many.iter().map(|r| r.given.as_str()).collect();
                return Err(self.gap(format_args!(
                    "add -i with an image tar whose image has more than one name ({})",
                    names.join(", ")
                )));
            }
        };
        let Some(locked) = local.pin(&digest) else {
            return Err(self.internal(format!("cannot pin {} to {digest}", local.given)));
        };
        let Some(id) = ImageId::parse(&inspected.id) else {
            return Err(self.internal(format!("image inspect returned Id {:?}", inspected.id)));
        };
        self.settle(repo, local.tag, (locked, id), lockfile)
    }

    /// image tar 的 `.digest` 旁檔：`stage` 進 `in/`[`DIGEST_SLOT`] 再讀。`stage` 失敗或格式不合回 VK0031。
    fn tar_digest(&mut self, sidecar: &[u8], shown: &str) -> Step<String> {
        let Some(slot) = Slot::parse(DIGEST_SLOT) else {
            return Err(self.internal(format!("stage slot {DIGEST_SLOT} is not a valid slot")));
        };
        let field = Field::new(sidecar.to_vec()).map_err(|e| self.internal(e.to_string()))?;
        let (_, outcome) = self.request(&Op::Stage(field, slot))?;
        let staged = match outcome {
            Outcome::Ok => {
                let path = self.env.inbox.join(DIGEST_SLOT);
                let bytes = fs::read(&path);
                bytes.map_err(|e| self.internal(format!("{}: {e}", path.display())))?
            }
            Outcome::Failed(_) => Vec::new(),
            Outcome::Runner(_) => return Err(self.internal("stage returned a runner result")),
        };
        match parse_digest(&staged) {
            Some(d) => Ok(d),
            None => {
                let d = Diagnostic::new(&messages::VK0031)
                    .arg("image", shown)
                    .arg("reason", text::DIGEST_MISSING);
                Err(self.stop(d))
            }
        }
    }

    /// `load` image tar，回 `docker load -q` 報告的 image；失敗回 VK0055。
    fn load(&mut self, host: Vec<u8>, shown: &str, repo: &str) -> Step<Loaded> {
        let field = Field::new(host).map_err(|e| self.internal(e.to_string()))?;
        let (seq, outcome) = self.request(&Op::Load(field))?;
        match outcome {
            Outcome::Ok => {}
            Outcome::Failed(rc) => {
                return Err(self.access_failed(shown, repo, text::docker_failed("load", rc)));
            }
            Outcome::Runner(_) => return Err(self.internal("load returned a runner result")),
        }
        let out = self.env.channel.output_path(seq);
        let bytes = fs::read(&out).map_err(|e| self.internal(format!("{}: {e}", out.display())))?;
        match parse_load(&bytes) {
            Some(l) => Ok(l),
            None => Err(self.gap(format_args!(
                "add -i with an image tar for which docker load did not report exactly one image \
                 ({:?})",
                String::from_utf8_lossy(&bytes).trim_end()
            ))),
        }
    }

    /// VK0045：已以別的 tag 導入，改用 `upgrade`。
    fn already_at(&mut self, repo: &str, tag: Tag, current: &ImageRef) -> Stop {
        let upgrade = format!("{repo}@{tag}");
        let command = prompt::command_with_y(&["just", "vendor_kit", "upgrade", &upgrade]);
        // VK0045 的下一步不帶 -y：去掉 command_with_y 補在最後的那一個（沒有 `--`，所以一定在最後）。
        let command = command.strip_suffix(" -y").unwrap_or(&command).to_owned();
        let d = Diagnostic::new(&messages::VK0045)
            .arg("repo", repo)
            .arg("tag", tag.to_string())
            .arg("current_tag", current.tag().to_string())
            .arg("upgrade_command", command);
        self.stop(d)
    }

    /// 不帶 `-i` 的線上 `add`（模組說明第 7、8 步與「線上解析」）。
    fn online(&mut self, req: &Request, lockfile: LockFile) -> Step<()> {
        if let Some(current) = lockfile.tool(req.repo).cloned() {
            return match req.tag {
                Some(tag) if tag != current.tag() => Err(self.already_at(req.repo, tag, &current)),
                _ => {
                    self.land_recoveries()?;
                    self.report_overrides();
                    self.say(&text::unchanged(req.repo, &current));
                    self.dry_run_done();
                    Ok(())
                }
            };
        }
        let Some(name) = req.image_path else {
            let d = Diagnostic::new(&messages::VK0025).arg("argument", IMAGE_PATH_ARGUMENT);
            return Err(self.stop(d));
        };
        let registry = self.env.registry;
        let token = match (req.tag, req.registry_token_file) {
            (None, Some(given)) => Some(self.token(given, req.repo)?),
            _ => None,
        };
        let mut listed = None;
        let tag = match req.tag {
            Some(tag) => tag,
            None => {
                let mut online = match registry.repository(name, token.as_ref()) {
                    Ok(r) => r,
                    Err(e) => return Err(self.list_failed(&e, name, req.repo)),
                };
                let latest = self.latest(&mut online, name, req.repo)?;
                listed = Some(online);
                latest
            }
        };
        let (locked, id) = self.resolve(name, tag, listed.as_mut(), req.repo)?;
        let candidate = self.fetch(req.repo, &id, &locked, &lockfile)?;
        self.import(req.repo, &locked, candidate, lockfile)
    }

    /// 目標 tag 換成版本鎖定行的值與 image ID（模組說明「線上解析」）：先 inspect 本機 image，讀 RepoDigests
    /// 的 digest；`listed` 是不帶 tag 時列過 tag 的查詢，有它就再跟 registry 的 digest 比對。本機沒有就向
    /// registry 取 digest（沒有 `listed` 就匿名開一個查詢），pull 之後再 inspect。
    fn resolve(
        &mut self,
        name: &str,
        tag: Tag,
        listed: Option<&mut Repository<'_>>,
        repo: &str,
    ) -> Step<(ImageRef, ImageId)> {
        let given = format!("{name}:{tag}");
        let Some(wire) = plan::ImageRef::parse(&given) else {
            return Err(self.internal(format!("cannot inspect {given}")));
        };
        let inspected = match self.inspect_local(&wire)? {
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
        self.resolved(&given, &digest, &inspected)
    }

    /// 版本鎖定行值 `<given>@<digest>` 與 inspect 到的 image ID。
    fn resolved(
        &mut self,
        given: &str,
        digest: &str,
        inspected: &Inspected,
    ) -> Step<(ImageRef, ImageId)> {
        let Ok(locked) = ImageRef::parse(&format!("{given}@{digest}")) else {
            return Err(self.internal(format!("cannot pin {given} to {digest}")));
        };
        let Some(id) = ImageId::parse(&inspected.id) else {
            return Err(self.internal(format!("image inspect returned Id {:?}", inspected.id)));
        };
        Ok((locked, id))
    }

    /// 本機沒有目標 image：向 registry 取 tag 的 digest，`pull <name>@<digest>`，再以同一個引用 inspect
    /// （以 digest pull 的 image 不帶 tag）。
    fn pull(
        &mut self,
        online: &mut Repository<'_>,
        name: &str,
        tag: Tag,
        repo: &str,
    ) -> Step<(ImageRef, ImageId)> {
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
        let inspected = match self.inspect_local(&wire)? {
            Ok(i) => i,
            Err(rc) => {
                return Err(self.access_failed(&shown, repo, text::docker_failed("inspect", rc)));
            }
        };
        self.resolved(&given, &digest, &inspected)
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

    /// 列 tag 失敗：要求認證而沒帶 token 是 VK0001，其他是 VK0055。
    fn list_failed(&mut self, e: &registry::Error, name: &str, repo: &str) -> Stop {
        match e.kind() {
            ErrorKind::AuthRequired => {
                let d = Diagnostic::new(&messages::VK0001)
                    .arg("repo", repo)
                    .arg("cmd", VK0001_CMD);
                self.stop(d)
            }
            ErrorKind::TokenRejected
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
        // 預演只讀，持共享鎖（模組說明「預演」）。
        let mode = if self.dry_run {
            Mode::Shared
        } else {
            Mode::Exclusive
        };
        match Lock::acquire(self.env.dir, mode, config) {
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
                "add while the local source of {repo} delivers the reserved namespace {} \
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

    /// 請啟動器做一個 docker 動作，等結果。`Failed` 回 docker 的結束碼。
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

    /// inspect `-i` 給的 image，回傳版本鎖定行的值與 image ID。
    fn inspect(&mut self, repo: &str, local: &LocalRef) -> Step<(ImageRef, ImageId)> {
        let Some(wire) = plan::ImageRef::parse(&local.given) else {
            return Err(self.gap(format_args!("image reference {:?}", local.given)));
        };
        let inspected = self.inspect_ref(wire, &local.given, repo)?;
        let Some(digest) = digest_for(&local.name(), &inspected.repo_digests) else {
            let d = Diagnostic::new(&messages::VK0031)
                .arg("image", &local.given)
                .arg("reason", text::no_repo_digest(&local.name()));
            return Err(self.stop(d));
        };
        let Some(pinned) = local.pin(&digest) else {
            return Err(self.internal(format!("cannot pin {} to {digest}", local.given)));
        };
        let Some(id) = ImageId::parse(&inspected.id) else {
            return Err(self.internal(format!("image inspect returned Id {:?}", inspected.id)));
        };
        Ok((pinned, id))
    }

    fn inspect_ref(&mut self, wire: plan::ImageRef, shown: &str, target: &str) -> Step<Inspected> {
        match self.inspect_local(&wire)? {
            Ok(i) => Ok(i),
            Err(rc) => Err(self.access_failed(shown, target, text::docker_failed("inspect", rc))),
        }
    }

    /// 請啟動器 inspect；docker 回非零時回 `Err(結束碼)`，交給呼叫端判斷（本機沒有、或真的失敗）。
    fn inspect_local(&mut self, wire: &plan::ImageRef) -> Step<Result<Inspected, u8>> {
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

    /// 取件並驗證：extract 到這次執行的下一個 slot，再 `fetch::verify`（含撞名）。
    fn fetch(
        &mut self,
        repo: &str,
        id: &ImageId,
        locked: &ImageRef,
        lockfile: &LockFile,
    ) -> Step<(Candidate, Installed)> {
        self.extracts += 1;
        let slot = format!("{SLOT_PREFIX}{}", self.extracts);
        let Some(slot_v) = Slot::parse(&slot) else {
            return Err(self.internal(format!("invalid slot {slot}")));
        };
        let (_, outcome) = self.request(&Op::Extract(id.clone(), slot_v))?;
        match outcome {
            Outcome::Ok => {}
            Outcome::Failed(rc) => {
                let shown = locked.to_string();
                return Err(self.access_failed(&shown, repo, text::docker_failed("extract", rc)));
            }
            Outcome::Runner(_) => return Err(self.internal("extract returned a runner result")),
        }
        let root = self.env.inbox.join(&slot);
        let installed = self.installed(repo, lockfile)?;
        let inspected_digests = vec![format!(
            "{}/{}@{}",
            locked.registry(),
            locked.path(),
            locked.digest()
        )];
        let staged = Staged {
            repo,
            locked,
            root: &root,
            repo_digests: &inspected_digests,
        };
        match fetch::verify(&staged, &installed.taken, None) {
            Ok(c) => Ok((c, installed)),
            Err(fetch::Error::Collision { repo, collisions }) => {
                for c in collisions {
                    let d = Diagnostic::new(&messages::VK0030)
                        .arg("repo", repo.as_str())
                        .arg("ns", c.ns)
                        .arg("owner", c.owner.to_string());
                    self.emit(d);
                }
                Err(Stop)
            }
            Err(e) => Err(self.internal(format!("tool content of {repo}: {e}"))),
        }
    }

    /// 已裝工具（不含 `repo` 自己）的 `<ns>` 與根 `justfile` 的名字。開著覆寫的工具取本機開發來源的 `<ns>`，
    /// 備好還沒落地的恢復取它暫存內容的 `<ns>`。
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
            // 備好還沒落地的恢復：`cache/<repo>/` 還沒換，以暫存內容的 `<ns>` 為準。
            if let Some(r) = self.pending.iter().rev().find(|r| &r.repo == other) {
                let ns = r.candidate.namespaces().to_vec();
                taken.tool(other, ns.iter().cloned());
                namespaces.insert(other.clone(), ns);
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

    /// 算初始檔、一次問完、全部同意才落地。
    fn import(
        &mut self,
        repo: &str,
        locked: &ImageRef,
        (candidate, installed): (Candidate, Installed),
        mut lockfile: LockFile,
    ) -> Step<()> {
        let init = (self.init)(candidate.root()).map_err(|reason| self.gap(reason))?;
        let meta_path = match metadata::tool_path(self.env.dir, repo) {
            Ok(p) => p,
            Err(e) => return Err(self.internal(e.to_string())),
        };
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
            initfiles::Command::Add,
            &files,
            &meta,
            |p| read_optional(&root.join(p)),
            |p| read_optional(&vk.join(baseline_file(repo, p))),
        );
        let planned = planned.map_err(|e| self.internal(e.to_string()))?;
        if let Some((path, gap)) = planned.gaps().next() {
            return Err(self.gap(format_args!("init file {path} ({gap:?})")));
        }

        // 預演不問、不重驗暫存內容：之後不落地（模組說明「預演」）。
        if !self.dry_run {
            if !self.consent(repo, &planned.questions)? {
                return Ok(());
            }
            if let Err(e) = candidate.recheck() {
                return Err(self.internal(format!("staged content of {repo} changed: {e}")));
            }
        }

        // 紀錄檔：這個工具的 metadata 與基準版副本。
        let mut repo_writes: Vec<(PathBuf, Vec<u8>)> = Vec::new();
        let mut written: Vec<WrittenFile> = Vec::new();
        let mut records: Vec<(PathBuf, Vec<u8>)> = Vec::new();
        for f in &planned.files {
            if let Some(w) = &f.write {
                repo_writes.push((PathBuf::from(&f.path), w.after.clone()));
                written.push(WrittenFile::new(
                    f.path.as_str(),
                    w.before.as_deref(),
                    &w.after,
                ));
            }
            if let Some(b) = &f.baseline {
                records.push((baseline_file(repo, &f.path), b.clone()));
            }
            if let Some(r) = &f.record
                && let Err(e) = meta.put(r.clone())
            {
                return Err(self.internal(e.to_string()));
            }
        }
        if !planned.files.is_empty() {
            let rendered = meta.render(self.env.written_by);
            let rendered = rendered.map_err(|e| self.internal(e.to_string()))?;
            let rel = meta_path
                .strip_prefix(&vk)
                .map(Path::to_path_buf)
                .unwrap_or_else(|_| meta_path.clone());
            records.push((rel, rendered.into_bytes()));
            self.other_records(repo, &planned.files, &lockfile, &mut records)?;
        }

        if let Err(e) = lockfile.set_tool(repo, locked) {
            return Err(self.internal(e.to_string()));
        }
        let mut all_ns = installed.namespaces;
        all_ns.insert(repo.to_owned(), candidate.namespaces().to_vec());
        let entry = self.entry(&all_ns)?;

        let progress = self.progress(repo, locked, &written)?;
        // 恢復排在這次第一個寫入之前、所有可能停下的判定之後（停下時恢復也不寫）。預演只印、不落地。
        self.land_recoveries()?;
        if !self.dry_run {
            self.land(
                &candidate,
                progress,
                &repo_writes,
                &records,
                &entry,
                &mut lockfile,
            )?;
        }

        self.report_overrides();
        let dry_run = self.dry_run;
        if dry_run {
            self.say(&text::would_add(repo, locked));
        } else {
            self.say(&text::added(repo, locked));
        }
        for f in &planned.files {
            let line = if dry_run {
                text::would_file_line(f)
            } else {
                text::file_line(f)
            };
            if let Some(line) = line {
                self.say(&line);
            }
        }
        for f in &planned.files {
            if let Some(m) = f.message() {
                let d = Diagnostic::new(m).arg("file", f.path.as_str());
                self.emit(d);
            }
        }
        self.dry_run_done();
        Ok(())
    }

    /// 一次問完初始檔的詢問：全部同意回 `true`；答否印未變更回 `false`；不能互動停下（模組說明第 10 步）。
    fn consent(&mut self, repo: &str, questions: &[initfiles::Question]) -> Step<bool> {
        // 帶 `-y` 時其他詢問都同意，只有 append 進既有檔的那幾題照樣要問（04 寫入既有檔的例外：已存在但
        // 尚未納管的檔，`-y` 不能改成 append 納管）。
        let yes = self.yes;
        let asked: Vec<_> = questions
            .iter()
            .filter(|q| !yes || q.ask == Ask::Append)
            .collect();
        let questions: Vec<String> = asked
            .iter()
            .map(|q| text::question(repo, &q.path, q.ask))
            .collect();
        let tty = TtyState {
            stdin: self.env.tty.stdin,
            stderr: self.env.tty.stderr,
        };
        let answers = prompt::ask_all(
            &questions,
            Consent::Ask,
            &tty,
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
            Err(PromptError::NotInteractive(_)) if self.yes => {
                // 已帶 `-y`：VK0002 的下一步會是同一個指令，照著跑還是停在這裡（03 待處理的下一步必須可
                // 直接執行），草稿碼登錄前以 VK0056 停下。
                let files: Vec<&str> = asked.iter().map(|q| q.path.as_str()).collect();
                let reason = format!("{}; {DRAFT_YES_APPEND}", text::yes_append(&files));
                Err(self.internal(reason))
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

    /// 其他紀錄檔裡同一個路徑的紀錄（ADR-0003）：寫入前內容相符的紀錄跟著換成寫入後的 hash。
    fn other_records(
        &mut self,
        repo: &str,
        files: &[FilePlan],
        lockfile: &LockFile,
        records: &mut Vec<(PathBuf, Vec<u8>)>,
    ) -> Step<()> {
        let writes: Vec<(&str, &[u8], &[u8])> = files
            .iter()
            .filter_map(|f| {
                let w = f.write.as_ref()?;
                Some((f.path.as_str(), w.before.as_deref()?, w.after.as_slice()))
            })
            .collect();
        if writes.is_empty() {
            return Ok(());
        }
        let vk = self.env.dir.vk_dir();
        let mut paths = vec![metadata::vk_path(self.env.dir)];
        for other in lockfile.tools().keys().filter(|r| r.as_str() != repo) {
            match metadata::tool_path(self.env.dir, other) {
                Ok(p) => paths.push(p),
                Err(e) => return Err(self.internal(e.to_string())),
            }
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
            for (p, before, after) in &writes {
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

    /// 這次的進度檔：`[add]` 表記對象、版本鎖定行的值與有沒有要寫 repo 檔，`[[repo_file]]` 記這次要寫的
    /// 每個 repo 檔（`progress::repo_files`）。
    fn progress(&mut self, repo: &str, locked: &ImageRef, files: &[WrittenFile]) -> Step<Progress> {
        let mut p = match Progress::new(VERB, self.env.run_id, self.env.argv) {
            Ok(p) => p,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let doc = p.document_mut();
        let set = doc
            .set(&[PROGRESS_TABLE, "repo"], repo)
            .and_then(|()| doc.set(&[PROGRESS_TABLE, "image"], locked.to_string()))
            .and_then(|()| doc.set(&[PROGRESS_TABLE, "repo_files"], !files.is_empty()));
        set.and_then(|()| repo_files::record(&mut p, files))
            .map_err(|e| self.internal(e.to_string()))?;
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
        let stamp = stamp_file(self.env.dir, candidate.repo());
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

    /// 備好全部殘留的進度檔（只讀不寫），`lockfile` 換成恢復之後的版本鎖定行；落地等這次的詢問全部同意
    /// （[`Self::land_recoveries`]）。
    fn recover_all(&mut self, lockfile: &mut LockFile) -> Step<()> {
        let entries = match progress::find(self.env.dir) {
            Ok(e) => e,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        for entry in entries {
            if entry.verb != VERB {
                return Err(self.gap(format_args!(
                    "recovering the incomplete {} operation in {}",
                    entry.verb,
                    self.rel(&entry.path)
                )));
            }
            let recovery = self.recover(entry, lockfile)?;
            *lockfile = recovery.lockfile.clone();
            self.pending.push(recovery);
        }
        Ok(())
    }

    /// 備好一份殘留的 `add`：依進度檔記的版本鎖定行值重新取件、驗證，算好恢復之後的入口檔與版本鎖定行，
    /// 不寫任何檔。只在沒有 repo 檔要寫時做：要寫的已記在進度檔，但重新落地要讀 `init.toml`，格式沒定
    /// （見模組說明的缺口）。
    fn recover(&mut self, entry: progress::Entry, lockfile: &LockFile) -> Step<Recovery> {
        let old = match entry.load() {
            Ok(p) => p,
            Err(e) => return Err(self.failed(&entry.path, e.message(), e.to_string())),
        };
        let field = |key: &str| {
            old.document()
                .get(&[PROGRESS_TABLE, key])
                .and_then(|i| i.as_value())
                .cloned()
        };
        let repo = field("repo").and_then(|v| v.as_str().map(str::to_owned));
        let image = field("image").and_then(|v| v.as_str().map(str::to_owned));
        let repo_files = field("repo_files").and_then(|v| v.as_bool());
        let (Some(repo), Some(image), Some(repo_files)) = (repo, image, repo_files) else {
            return Err(self.gap(format_args!(
                "recovering {} without the [add] fields",
                self.rel(&entry.path)
            )));
        };
        if repo_files {
            return Err(self.gap(format_args!(
                "recovering {}, which writes repo files from init.toml",
                self.rel(&entry.path)
            )));
        }
        let Ok(locked) = ImageRef::parse(&image) else {
            return Err(self.internal(format!("{} records image {image:?}", self.rel(&entry.path))));
        };
        let pinned = format!(
            "{}/{}@{}",
            locked.registry(),
            locked.path(),
            locked.digest()
        );
        let Some(wire) = plan::ImageRef::parse(&pinned) else {
            return Err(self.internal(format!("cannot inspect {pinned}")));
        };
        let inspected = self.inspect_ref(wire, &image, &repo)?;
        if !inspected.repo_digests.contains(&pinned) {
            let d = Diagnostic::new(&messages::VK0031)
                .arg("image", image.as_str())
                .arg("reason", text::no_repo_digest(&pinned));
            return Err(self.stop(d));
        }
        let Some(id) = ImageId::parse(&inspected.id) else {
            return Err(self.internal(format!("image inspect returned Id {:?}", inspected.id)));
        };
        let (candidate, installed) = self.fetch(&repo, &id, &locked, lockfile)?;
        let mut lockfile = lockfile.clone();
        if let Err(e) = lockfile.set_tool(&repo, &locked) {
            return Err(self.internal(e.to_string()));
        }
        let mut all_ns = installed.namespaces;
        all_ns.insert(repo.clone(), candidate.namespaces().to_vec());
        let tools_just = self.entry(&all_ns)?;
        Ok(Recovery {
            entry,
            repo,
            locked,
            candidate,
            tools_just,
            lockfile,
        })
    }

    /// 依序落地備好的恢復（04 共同選項：全部同意才寫入，含恢復舊操作），排在這次自己的落地與輸出之前：
    /// 每一份重驗暫存內容、走一次同樣的落地順序，新的進度檔完成之後才刪舊的那一份，中途再斷也還認得出來。
    fn land_recoveries(&mut self) -> Step<()> {
        if self.dry_run {
            // 預演：只印會完成哪幾份，殘留的進度檔照留（模組說明「預演」）。
            let lines: Vec<String> = self
                .pending
                .iter()
                .map(|r| text::would_recover(&r.repo, &r.locked))
                .collect();
            for line in lines {
                self.say(&line);
            }
            return Ok(());
        }
        for mut r in std::mem::take(&mut self.pending) {
            if let Err(e) = r.candidate.recheck() {
                return Err(self.internal(format!("staged content of {} changed: {e}", r.repo)));
            }
            let progress = self.progress(&r.repo, &r.locked, &[])?;
            self.land(
                &r.candidate,
                progress,
                &[],
                &[],
                &r.tools_just,
                &mut r.lockfile,
            )?;
            if let Err(e) = progress::delete(self.env.dir, &r.entry.verb, &r.entry.id) {
                return Err(self.failed(&r.entry.path, e.message(), e.to_string()));
            }
            self.say(&text::recovered(&r.repo, &r.locked));
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
