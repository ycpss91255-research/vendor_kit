//! 啟動器與引擎的往返協定 `vk-resolve/<P>`（#372 的 D2）的引擎端。
//!
//! 一次指令只起一個引擎容器，引擎全程活著、全程持鎖；要在主機上做的 docker 動作（取件、test runner、
//! prune 的容器刪除）由引擎寫一份 request，啟動器照做後寫回 result，逐項往返；最後引擎寫 `done` 結束。
//! 使用者下指令時的上下文（所在目錄、執行紀錄、TTY、NO_COLOR）由啟動器以具名 argv 傳入（[`argv`]）。
//! 定案見 #372 留言（issuecomment-5997655839）。bash 啟動器端照這裡的文法驗證與分派，不在這個 crate。
//!
//! # 掛載與控制檔
//!
//! 安裝目錄掛在 [`mount::ROOT`]；repo 外的 session 目錄（`${TMPDIR:-/tmp}/vendor_kit.<run-id>/`）的 `ctl/`
//! 可寫掛在 [`mount::CTL`]，`in/` 唯讀掛在 [`mount::IN`]（啟動器 `docker cp` 進 `in/<slot>` 的檔，與起引擎前
//! 寫好的引擎引用檔 [`files::IN_ENGINE`]）。控制檔都在 `ctl/`（[`files`]）：
//!
//! - 引擎寫 `req.<seq>`：先寫 `req.<seq>.tmp` 再 rename，啟動器只讀 rename 完的檔。
//! - 啟動器寫 `res.<seq>`（同樣先寫暫存再 rename）；有原始輸出（inspect、ps）時另存 `res.<seq>.out`。
//! - 同一時間只有一個未完成的 request；seq 從 1 起連續。
//! - 引擎最後寫 `done`（同樣先寫暫存再 rename），帶自己的結束碼。
//!
//! # 文法 vk-resolve/1（ABNF，RFC 5234）
//!
//! 這一節是規範：bash 端照它逐欄驗證，與這裡的解析器同一份規則。字串一律區分大小寫，只用 ASCII，
//! 不准 CR、NUL 與多餘的空白或行。
//!
//! ```text
//! req     = hdr SP seq LF op LF
//! res     = hdr SP seq LF result LF
//! done    = hdr SP "done" SP exit LF
//! hdr     = "vk-resolve/" proto SP run-id     ; 兩者必須等於 argv 的 --protocol、--run-id
//! proto   = %x31-39 *9DIGIT                   ; 不補零
//! run-id  = 1*64( %x61-7A / DIGIT / "-" )
//! seq     = %x31-39 *3DIGIT                   ; 1–9999，不補零（檔名 req.<seq> 要逐字相等）
//! exit    = "0" / "1" / "2" / "3"
//! op      = "pull" SP pinned                  ; 只收帶 digest 的引用，不收純 tag
//!         / "load" SP fld                     ; 主機絕對路徑
//!         / "inspect" SP ref                  ; image inspect，輸出寫 res.<seq>.out（ID、RepoDigests）
//!         / "extract" SP imgid SP slot        ; create（入口設成不存在的檔）→ cp /dist/. 進 in/<slot> → rm
//!         / "stage" SP fld SP slot            ; 安裝目錄外的主機檔（例如 token 檔）複製進 in/<slot>
//!         / "ps"                              ; 本安裝目錄 label 的已停止容器，輸出寫 res.<seq>.out
//!         / "rm-container" SP cid             ; 只收本次 ps 列出的 cid；不加 -f
//!         / "runner" SP ref 1*( SP fld )      ; command 加 path，不經 shell
//! result  = "ok" / "failed" SP rc             ; runner 以外的 op
//!         / "runner" SP runout                ; 只回給 runner
//! runout  = "notstarted" / "exited" SP rc / "stopped" SP ( rc / "unavailable" )
//! fld     = "e:" *( %x21-5B / %x5D-7E / "\" oct )   ; 單獨的 "e:" 是空字串
//! oct     = "00" %x31-37 / "0" %x31-37 %x30-37 / %x31-33 %x30-37 %x30-37   ; 001–377，不收 \000
//! ref     = ( %x61-7A / DIGIT ) *( %x61-7A / DIGIT / "." / "_" / "/" / ":" / "@" / "-" )
//! pinned  = ref                               ; 而且以 "@sha256:" 64hexl 結尾，全串只有這一個 "@"
//! imgid   = "sha256:" 64hexl
//! cid     = 64hexl
//! hexl    = DIGIT / %x61-66
//! slot    = 1*16( %x61-7A / DIGIT )
//! rc      = "0" / %x31-39 [DIGIT] / "1" 2DIGIT / "2" %x30-34 DIGIT / "25" %x30-35   ; 0–255，不補零
//! ```
//!
//! 自由文字欄 `fld` 的寫法（ADR-0012:22，前例 getmntent(3) 的 `\040`、`\134`）：0x21–0x7E 照原樣寫，
//! 只有反斜線 0x5C 例外；反斜線、空白、控制字元與 0x7F 以上的位元組一律寫成三位八進位。編碼端
//! （[`Field::encode`]）只用這一種寫法，所以同一個值只有一種位元組。NUL 寫不進去（argv 與路徑本來就不含）。
//!
//! runner 的結果帶三件事（[`RunnerOutcome`]）：起來沒（started）、runner 自己的結束碼（process-rc）、
//! 是不是被 VK 停掉（stopped-by-vk）。起不來或被 VK 停掉報 VK0066，自己結束且非 0 報 VK0067；
//! 不從結束碼大於 128 猜是不是被中斷。
//!
//! # 救援路徑
//!
//! 救援路徑（install、upgrade --engine、sync 判定與四種用法呼叫）用到的協定動作與文法跨介面版永久不變
//! （#372 維護者 10/05 定救援路徑協定選 A，issuecomment-5995675088；ADR-0007:37、ADR-0008）。
//! 範圍是：入口 argv（[`argv`]）、掛載點（[`mount`]）、控制檔名（[`files`]）、`hdr`、`done`、`fld`、
//! `result` 的 `ok`／`failed`，以及 [`RESCUE_OPS`] 的五個 op。這些都集中成常數並由測試釘住；
//! 改了就破壞救援，P+1 也不能改。其餘 op 依 ADR-0008:25 隨 P 演進。
//! 呼叫方的 P 不在引擎接受的區間內時，引擎仍照救援路徑回應那個 P，往返限定只送這五個 op
//! （[`Channel::restrict_to_rescue`]）。
//!
//! 協定不合（文法、seq、header、op 與 result 不配對）一律是 VK 的 bug，對應 VK0056（[`ProtocolError::message`]）。

mod argv_parse;
mod channel;
mod field;
mod wire;

pub use argv_parse::{ArgvError, Invocation, Tty};
pub use channel::{Channel, ChannelError};
pub use field::{Field, FieldError};
pub use wire::{
    Container, Exit, Header, ImageId, ImageRef, Op, OpKind, Outcome, ProtocolError, Reply, RunId,
    RunnerOutcome, Seq, Slot,
};

/// 文法名；控制檔第一行的開頭是 `vk-resolve/<P>`。
pub const GRAMMAR: &str = "vk-resolve";

/// op 的封閉集合，依文法的順序。
pub const OPS: [&str; 8] = [
    "pull",
    "load",
    "inspect",
    "extract",
    "stage",
    "ps",
    "rm-container",
    "runner",
];

/// 救援路徑用到的 op；文法跨介面版永久不變（見 crate 文件「救援路徑」）。
pub const RESCUE_OPS: [&str; 5] = ["pull", "load", "inspect", "extract", "stage"];

/// 引擎入口的具名選項，依啟動器傳的順序；`--` 之後是 recipe 與使用者參數原樣。救援路徑也走這一行，永久不變。
pub mod argv {
    pub const PROTOCOL: &str = "--protocol";
    pub const RUN_ID: &str = "--run-id";
    pub const HOST_ROOT: &str = "--host-root";
    pub const HOST_CWD: &str = "--host-cwd";
    pub const RUN_LOG: &str = "--run-log";
    pub const TTY: &str = "--tty";
    pub const NO_COLOR: &str = "--no-color";
    /// 具名選項結束、recipe 與使用者參數開始。
    pub const END: &str = "--";
    /// 具名選項的順序，每個剛好一次、各帶一個值。
    pub const ORDER: [&str; 7] = [
        PROTOCOL, RUN_ID, HOST_ROOT, HOST_CWD, RUN_LOG, TTY, NO_COLOR,
    ];
}

/// 引擎容器內的掛載點；救援路徑也用，永久不變。
pub mod mount {
    /// 安裝目錄（可寫，引擎的工作目錄）。
    pub const ROOT: &str = "/vk/root";
    /// session 的 `ctl/`（可寫）：控制檔。
    pub const CTL: &str = "/vk/ctl";
    /// session 的 `in/`（唯讀）：啟動器取件放進來的檔。
    pub const IN: &str = "/vk/in";
}

/// `ctl/` 裡的控制檔名與 `in/` 裡啟動器放的引擎引用檔名；救援路徑也用，永久不變。
pub mod files {
    /// 引擎寫的 request：`req.<seq>`。
    pub const REQ_PREFIX: &str = "req.";
    /// 啟動器寫的 result：`res.<seq>`。
    pub const RES_PREFIX: &str = "res.";
    /// result 的原始輸出：`res.<seq>.out`。
    pub const OUT_SUFFIX: &str = ".out";
    /// 引擎最後寫的結束檔。
    pub const DONE: &str = "done";
    /// 寫到一半的檔：`<名>.tmp`，寫完才 rename 成正式檔名。
    pub const TMP_SUFFIX: &str = ".tmp";
    /// `in/` 裡啟動器起引擎前寫好的檔：這次起的引擎 image 的 pinned 引用，一行、LF 結尾（N37）。
    /// 引擎 image 不可能含有自己的 index digest，救援 argv 又凍結，所以經這個檔交給引擎。
    /// 不會跟 `tool<N>` 的 slot 撞名（stage、extract 遇到已存在的 slot 一律拒絕）。
    pub const IN_ENGINE: &str = "engine";
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests;
