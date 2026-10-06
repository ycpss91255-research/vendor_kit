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
//!    而且記的目標就是版本鎖定行，表示第一段做完了，直接做第二段（見「第二段」），不連 registry。帶的
//!    `--engine=<tag>` 跟版本鎖定行不同、或有別的殘留，見「缺口」。
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
//! 5. 介面版列表：`vendor_kit_protocols` 寫成本引擎的區間。
//! 6. 沒有殘留的進度檔、而上面全都已是這一版：stdout 說明未變更，以 0 結束，不建進度檔。
//! 7. 一次問完（帶 `-y` 全部同意）：答否是正常取消，stdout 說明未變更、以 0 結束，第一段換好的鎖定行與進度檔
//!    都不動（04：第二次呼叫答否，不撤回第一次已完成的換引擎）；不能互動回 VK0002。這一版第二段沒有要問的事
//!    （`config.toml` 的換版與合併還沒做），所以這一步一律通過。
//! 8. 經 `txn` 落地：建這次的進度檔（同第一段的 `[upgrade]` 表，`image` 是版本鎖定行的值）→ 薄殼、升級後的 VK
//!    檔、`gen/.stamp`（紀錄檔那一步，依序）→ 版本鎖定行（介面版列表）→ 刪這次的進度檔；之後才刪殘留的進度檔。
//! 9. stdout 列出寫了哪些薄殼、升級了哪些 VK 檔，最後一行說明引擎升級完成。
//!
//! 中途停下時這次與第一段的進度檔都還在，鎖定行已是新版；重跑原指令照上面再做一次（薄殼與 `gen/.stamp` 只寫
//! 不一致的，升過的 VK 檔已是上限），落地後一起刪掉。
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
//!
//! # 缺口（契約或其他 crate 沒定；遇到就以 VK0056 停下並寫明原因）
//!
//! - 殘留其他可寫 recipe 的進度檔：可寫 recipe 要先恢復（04 成對與無害），引擎升級怎麼恢復別的指令沒定。殘留的
//!   引擎升級進度檔記的目標不是版本鎖定行（鎖定行之後又被手改過），或帶的 `--engine=<tag>` 跟版本鎖定行不同：
//!   04 沒說要續作哪一個。
//! - 不帶 tag 而 registry 的最新版比鎖定行舊：04 只說最新版不限目前的 vX，沒說要不要因此降版（同 `upgrade <repo>`）。
//! - 目標 image 缺 LABEL 或值不合（例如公告檔案版上限的 LABEL 之前出的 image）：判不了降版。
//! - 引擎開著本機覆寫（`dev --engine`）：第一段照樣只換鎖定行、覆寫不動；第二段由哪一版引擎做沒定，停下。
//! - 第二段時這一版 image 沒有薄殼模板（出貨輸入缺項，同 `install`）。
//! - registry 列得到、但一個 tag 都沒有：照 `upgrade <repo>` 報 VK0055（[`crate::text::NO_TAGS`]）。
//! - 中途寫檔失敗沒有代碼（計畫 G4）。

use std::fs;
use std::io::{self, Write};
use std::path::{Path, PathBuf};

use compat::Compat;
use diagnostics::{Diagnostic, Sink};
use imageref::{ImageRef, Tag};
use progress::Progress;
use progress::upgrade as table;
use prompt::{Consent, PromptError, TtyState};
use runlog::Target;
use shell::Shell;
use txn::{Disk, RecordFile, Txn};
use version_file::{LocalFile, LockFile};

use super::{Env, Step, Upgrade, VERB, discover_init_files, migrate, text};

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
/// 重組 `<original_command>` 時接在參數前面的字。
pub const COMMAND_PREFIX: [&str; 2] = ["just", "vendor_kit"];

/// 隨 image 出貨的薄殼四檔模板本文，順序同 `layout::SHELL_FILES`。
pub type ShellTemplates = [Vec<u8>; layout::SHELL_FILES.len()];

/// 一次 `upgrade --engine[=<tag>] [-y]` 的參數（`args::Command::UpgradeEngine`）與第二段要的出貨輸入。
#[derive(Debug, Clone, Copy)]
pub struct Request<'a> {
    pub tag: Option<Tag>,
    /// `-y`：第一段不詢問，只留在原指令裡；第二段預先同意全部詢問。
    pub yes: bool,
    /// 薄殼模板（入口讀 image 裡的出貨輸入）；四檔不齊是 `None`，第二段遇到就停下（模組說明「缺口」）。
    pub shell_templates: Option<&'a ShellTemplates>,
}

/// 第二段要問的事；這一版沒有（模組說明「第二段」第 7 步），測試換成直接給。
pub(crate) type Questions<'f> = &'f dyn Fn() -> Vec<String>;

/// 跑一次 `upgrade --engine`，回傳結束碼。`env` 跟 `upgrade <repo>` 共用（`argv` 第一個是 `upgrade`）。
pub fn run<W: Write, S: Sink, L: Write>(req: &Request<'_>, env: &mut Env<'_, W, S, L>) -> u8 {
    run_with(req, env, &Vec::<String>::new)
}

pub(crate) fn run_with<W: Write, S: Sink, L: Write>(
    req: &Request<'_>,
    env: &mut Env<'_, W, S, L>,
    questions: Questions,
) -> u8 {
    let mut upgrade = Upgrade {
        env,
        init: &discover_init_files,
        code: 0,
        extracts: 0,
        stages: 0,
        local: Default::default(),
        engine: true,
    };
    let _ = upgrade.engine_run(req, questions);
    upgrade.code
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
    fn engine_run(&mut self, req: &Request<'_>, questions: Questions) -> Step<()> {
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        let lockfile = self.lockfile()?;
        let residuals = self.engine_residuals(&lockfile)?;
        let current = lockfile.engine().tag();
        if let Some(first) = residuals.first() {
            if let Some(tag) = req.tag.filter(|t| *t != current) {
                let file = self.rel(&first.path);
                return Err(self.gap(format_args!(
                    "upgrade --engine={tag} while the engine upgrade to {current} recorded in \
                     {file} is incomplete"
                )));
            }
            return self.engine_stage2(req, questions, lockfile, &residuals);
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
            return self.engine_stage2(req, questions, lockfile, &[]);
        }
        self.engine_stage1(tag, listed.as_mut(), lockfile)
    }

    fn engine_stage1(
        &mut self,
        tag: Tag,
        listed: Option<&mut registry::Repository<'_>>,
        mut lockfile: LockFile,
    ) -> Step<()> {
        let resolved = self.resolve(ENGINE_REPO, tag, listed, ENGINE_NAME)?;
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
        let progress = self.engine_progress(&resolved.locked)?;
        self.switch(progress, &mut lockfile)?;

        let d = Diagnostic::new(&messages::VK0023)
            .arg("vY", tag.to_string())
            .arg("original_command", original_command(self.env.argv));
        Err(self.stop(d))
    }

    /// 殘留的進度檔：全是記著版本鎖定行那個目標的引擎升級，回傳它們（第一段做完，接著做第二段）；有別的就停下
    /// （模組說明「缺口」）。
    fn engine_residuals(&mut self, lockfile: &LockFile) -> Step<Vec<progress::Entry>> {
        let entries = match progress::find(self.env.dir) {
            Ok(e) => e,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let locked = lockfile.engine().to_string();
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
            if table::field(&loaded, table::IMAGE) != Some(locked.as_str()) {
                return Err(self.gap(format_args!(
                    "completing the engine upgrade recorded in {file}, whose target is not the \
                     engine lock version line ({locked})"
                )));
            }
        }
        Ok(entries)
    }

    /// 第二段（模組說明「第二段」）；`residuals` 是第一段（或中斷的第二段）留下的進度檔。
    fn engine_stage2(
        &mut self,
        req: &Request<'_>,
        questions: Questions,
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

        if residuals.is_empty() && records.is_empty() && migrated.is_empty() && !protocols_changed {
            self.say(&text::unchanged(ENGINE_NAME, tag));
            return Ok(());
        }

        if !self.engine_ask(&questions(), req.yes)? {
            self.say(text::NO_CHANGES);
            return Ok(());
        }

        let progress = self.engine_progress(&engine)?;
        let record_files: Vec<RecordFile> = records
            .iter()
            .map(|(path, contents)| RecordFile { path, contents })
            .collect();
        let result = {
            let mut fx = Disk::new(self.env.dir, self.env.log, self.env.written_by);
            Txn::begin(&mut fx, progress).and_then(|t| {
                t.swap_cache(&[])?
                    .write_repo_files(&[])?
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

        for name in &shell_names {
            self.say(&text::wrote_shell(name));
        }
        for (file, from) in &migrated {
            self.say(&text::migrated(file, *from, compat::THIS.max_schema));
        }
        self.say(&text::engine_upgraded(&engine));
        Ok(())
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
