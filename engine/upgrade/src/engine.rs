//! `upgrade --engine` 的第一段（04 指令表 `upgrade --engine`、`upgrade --engine=<tag>`；04 upgrade --engine、
//! 指定版本；訊息表 VK0007、VK0023）：換上目標引擎的版本鎖定行，以 VK0023 停下，請使用者重跑原指令，由新引擎
//! 做第二段（重產薄殼、VK 檔格式升級、寫 `gen/.stamp`、刪進度檔）。第二段不在這一版。
//!
//! `upgrade --engine` 是救援路徑（ADR-0007:37、ADR-0008:26）：往返只用 [`plan::RESCUE_OPS`] 的 op（這裡只送
//! `inspect` 與 `pull`），呼叫方的介面版不在本引擎區間內時也照常執行（入口 `vendor_kit` 的 `gate`）。
//! 呼叫端已解析好參數、判過安裝目錄（VK0028），並接好執行紀錄與 `plan` 往返。這裡依序做：
//!
//! 1. 讀 `.vendor_kit/config.toml`（VK0059），在取鎖之前（同 `upgrade <repo>`）。
//! 2. 取安裝目錄的排他鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束。
//! 3. 讀 `version.toml`（檔案版過高回 VK0008）。
//! 4. 有殘留的進度檔就停下（見「缺口」），在任何 docker 動作與寫入之前。
//! 5. 判目標版本：`--engine=<tag>` 就是那個 tag；不帶 tag 就匿名列 [`ENGINE_REPO`] 的 tag，依 04 指定版本取最新版
//!    （[`imageref::Tag::latest`]）。不讀 `--registry-token-file`（04：不適用引擎升版，`args` 也不收）。
//!    目標 tag 等於版本鎖定行的 tag、或最新版比鎖定行舊：見「缺口」。
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
//! `-y` 這一段用不到（第一段不詢問），只是原樣留在原指令裡給第二段。
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
//! 不是 TOML。檔不在就跳過；讀不到或不是合法的 VK TOML 是 VK 的錯，以 VK0056 停下。檔案版高於本引擎上限的檔
//! 照樣算進去（讀時不套本引擎的門檻）。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 進度檔沿用 `progress::upgrade` 的 `[upgrade]` 表：`target` 是 `progress::upgrade::ENGINE_TARGET`、`image` 是
//!   目標的版本鎖定行值；不記 `init_files`（引擎升級不碰初始檔）。
//! - 目標 image 的 [`LABEL_VERSION`] 必須等於目標 tag，否則以 VK0056 停下：鎖定行的 tag 要描述的就是那個 image。
//! - [`ENGINE_REPO`] 照抄 engine/install 的同名常數（指令之間互不依賴），兩邊相等由入口 crate 的測試檢查。
//!
//! # 缺口（契約或其他 crate 沒定，或屬第二段；遇到就以 VK0056 停下並寫明原因）
//!
//! - 第二段（新引擎讀到引擎升級的進度檔後重產薄殼、升級 VK 檔格式、寫 `gen/.stamp`、刪進度檔）還沒做：殘留的
//!   引擎升級進度檔一律停下，重跑原指令目前停在這裡。
//! - 殘留其他可寫 recipe 的進度檔：可寫 recipe 要先恢復（04 成對與無害），引擎升級怎麼恢復別的指令沒定。
//! - 目標 tag 等於版本鎖定行的 tag：04 要求鎖定行已是目標版、但薄殼或 VK 檔還是舊版時直接做第二段，不能回「已是
//!   最新」（N21 草稿點），第二段還沒做，所以停下。
//! - 不帶 tag 而 registry 的最新版比鎖定行舊：04 只說最新版不限目前的 vX，沒說要不要因此降版（同 `upgrade <repo>`）。
//! - 目標 image 缺 LABEL 或值不合（例如公告檔案版上限的 LABEL 之前出的 image）：判不了降版。
//! - 引擎開著本機覆寫（`dev --engine`）時照樣只換鎖定行，覆寫不動；第二段由哪一版引擎做沒定。
//! - registry 列得到、但一個 tag 都沒有：照 `upgrade <repo>` 報 VK0055（[`crate::text::NO_TAGS`]）。
//! - 中途寫檔失敗沒有代碼（計畫 G4）。

use std::fs;
use std::io::{self, Write};
use std::path::{Path, PathBuf};

use compat::Compat;
use diagnostics::{Diagnostic, Sink};
use imageref::Tag;
use progress::Progress;
use progress::upgrade as table;
use runlog::Target;
use txn::{Disk, Txn};
use version_file::LockFile;

use super::{Env, Resolved, Step, Upgrade, VERB, discover_init_files};

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

/// 一次 `upgrade --engine[=<tag>] [-y]` 的參數（`args::Command::UpgradeEngine`）。
#[derive(Debug, Clone, Copy)]
pub struct Request {
    pub tag: Option<Tag>,
    /// `-y`：第一段不詢問，只留在原指令裡。
    pub yes: bool,
}

/// 跑一次 `upgrade --engine` 的第一段，回傳結束碼。`env` 跟 `upgrade <repo>` 共用（`argv` 第一個是 `upgrade`）。
pub fn run<W: Write, S: Sink, L: Write>(req: &Request, env: &mut Env<'_, W, S, L>) -> u8 {
    let mut upgrade = Upgrade {
        env,
        init: &discover_init_files,
        code: 0,
        extracts: 0,
        stages: 0,
        local: Default::default(),
        engine: true,
    };
    let _ = upgrade.engine_stage1(req);
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
    fn engine_stage1(&mut self, req: &Request) -> Step<()> {
        let config = self.config()?;
        let _lock = self.lock(&config)?;
        let mut lockfile = self.lockfile()?;
        self.engine_residuals()?;
        let current = lockfile.engine().tag();
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
            return Err(self.gap(format_args!(
                "upgrade --engine to {tag}, which the engine lock version line already names \
                 (the second stage of the engine upgrade)"
            )));
        }

        let resolved = self.resolve(ENGINE_REPO, tag, listed.as_mut(), ENGINE_NAME)?;
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
        let progress = self.engine_progress(&resolved)?;
        self.switch(progress, &mut lockfile)?;

        let d = Diagnostic::new(&messages::VK0023)
            .arg("vY", tag.to_string())
            .arg("original_command", original_command(self.env.argv));
        Err(self.stop(d))
    }

    /// 殘留的進度檔一律停下（模組說明「缺口」）。
    fn engine_residuals(&mut self) -> Step<()> {
        let entries = match progress::find(self.env.dir) {
            Ok(e) => e,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let Some(entry) = entries.first() else {
            return Ok(());
        };
        let file = self.rel(&entry.path);
        if entry.verb == VERB {
            let loaded = match entry.load() {
                Ok(p) => p,
                Err(progress::Error::Parse {
                    file,
                    source: progress::ParseError::Read(schema::ReadError::TooNew(t)),
                }) => return Err(self.too_new(&file, &t)),
                Err(e) => return Err(self.failed(&entry.path, e.message(), e.to_string())),
            };
            if table::field(&loaded, table::TARGET) == Some(table::ENGINE_TARGET) {
                return Err(self.gap(format_args!(
                    "completing the engine upgrade recorded in {file} (the second stage)"
                )));
            }
        }
        Err(self.gap(format_args!(
            "upgrade --engine while the incomplete {} operation in {file} remains",
            entry.verb
        )))
    }

    /// 現有 VK 檔的最高檔案版（模組說明「現有檔案版」）。
    fn existing_schema(&mut self, lockfile: &LockFile) -> Step<u32> {
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
        let mut max = 0;
        for path in paths {
            if let Some(n) = self.schema_of(&path)? {
                max = max.max(n);
            }
        }
        Ok(max)
    }

    /// 一個 VK 檔的檔案版；檔不在回 `None`。
    fn schema_of(&mut self, path: &Path) -> Step<Option<u32>> {
        let text = match fs::read_to_string(path) {
            Ok(t) => t,
            Err(e) if e.kind() == io::ErrorKind::NotFound => return Ok(None),
            Err(e) => return Err(self.internal(format!("{}: {e}", self.rel(path)))),
        };
        match schema::Document::parse_with(&text, &ANY_SCHEMA) {
            Ok(doc) => Ok(Some(doc.schema())),
            Err(e) => Err(self.internal(format!("{}: {e}", self.rel(path)))),
        }
    }

    /// 引擎升級的進度檔：共同欄位之外記 `[upgrade]` 表的 `target` 與 `image`。
    fn engine_progress(&mut self, resolved: &Resolved) -> Step<Progress> {
        let mut p = match Progress::new(VERB, self.env.run_id, self.env.argv) {
            Ok(p) => p,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let doc = p.document_mut();
        let set = doc
            .set(&[table::TABLE, table::TARGET], table::ENGINE_TARGET)
            .and_then(|()| doc.set(&[table::TABLE, table::IMAGE], resolved.locked.to_string()));
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
