//! `prune` 指令（04 指令表 `prune`、04 成對與無害、名詞表 `prune`）：清除 VK 產生、但這個安裝目錄已不再
//! 使用的本機資源。不詢問，stdout 列出清理內容（[`text`]）；不改追蹤檔。
//!
//! 清理範圍以 04 成對與無害為準，只有三類，不自己擴大：
//!
//! - 本安裝目錄 `cache/` 中未鎖定的工具目錄：`cache/<repo>/` 是目錄、`<repo>` 是工具名，而且版本鎖定行沒有
//!   `<repo>`（04 sync 表與 remove 表：「未列在鎖定行的工具目錄 | 留給 `prune`」）。同一個工具的印記
//!   `cache/<repo>.stamp.toml` 只記那個目錄的內容（[`stamp::tool_file`]），一起刪。
//! - VK 暫存：ADR-0002 的 `.vendor_kit/.gitignore` 涵蓋 `.tmp.*`；VK 寫檔留下的是 `files::write_atomic` 的
//!   `.tmp.<檔名>.<pid>.<序號>` 與 `txn` 換 `cache/` 的 `cache/.tmp.<repo>.new`、`.old`。這裡只看
//!   `.vendor_kit/`、`cache/`、`gen/`、`baseline/` 這幾層目錄本身（VK 在這幾層寫檔），不往下走：`cache/<repo>/`
//!   底下是工具交付的內容，名字叫 `.tmp.*` 的檔也是工具的。進度檔 `.tmp.<verb>.<id>.toml` 不是暫存，是未完成
//!   操作的恢復狀態（ADR-0004），由 `progress::find` 認出來，不算在內。
//! - VK 建立且可證明不再使用的已停止容器：經 `plan` 協定請啟動器 `ps`，再對列出的每一個 `rm-container`。
//!   啟動器的 `ps` 只列帶本安裝目錄 label 的已停止容器（launcher/launch.sh；label 是啟動器建容器時加的，
//!   所以是 VK 建立的），`rm-container` 只收本次 `ps` 列出的 ID、不加 `-f`。「不再使用」的依據是這次持著
//!   安裝目錄的排他鎖：同一個安裝目錄的其他 VK 執行都要持鎖，所以此刻沒有別的執行還會讀那些容器的結果。
//!   `lock_enabled = false`（VK0060）時沒有鎖，證明不了，就不 `ps`、不刪容器。
//!
//! image 不刪：04 說 image 無法證明無人使用就不刪；主機上的 image 由多個 repo 共用，引擎看不到其他 repo 的
//! 版本鎖定行，證明不了。這是正常行為，不是停下原因（見「缺口」）。
//!
//! 呼叫端（入口 `vendor_kit`）已解析好參數、判過安裝目錄（VK0028），並接好執行紀錄與 `plan` 往返。
//! 這裡依序做：
//!
//! 1. 讀 `.vendor_kit/config.toml`（VK0059），在第一次取鎖之前（04 設定）。
//! 2. 取安裝目錄的排他鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束：`prune` 會刪檔，屬寫入端。
//! 3. 讀 `version.toml`（檔案版過高回 VK0008）。
//! 4. 刪任何東西之前先判（02 不變量 4：判定有不能做的，就一個都不動，並列出每個原因）。這一段只讀：
//!    - 殘留的進度檔：`prune` 自己的留到這次一起完成（見「恢復」）；其他 verb 的見「缺口」。進度檔檔案版
//!      過高回 VK0008。
//!    - 依上面的範圍列出要刪的路徑。
//!    - 要刪的工具目錄仍被 `gen/tools.just` 引用（例如 `git pull` 拿掉了鎖定行、還沒 `sync`）：刪了 just
//!      就載入不了入口檔，見「缺口」。
//! 5. 持著鎖時請啟動器 `ps`，讀回已停止的 VK 容器。
//! 6. 沒有要刪的路徑、沒有殘留的 `prune` 進度檔、也沒有容器：什麼都不寫，stdout 不印。
//! 7. 否則經 `txn` 的收回順序刪路徑：不寫 repo 檔、入口檔不變、只刪 `.vendor_kit/` 下的路徑、不改版本鎖定行
//!    （04 成對與無害：`prune` 不改追蹤檔），最後刪進度檔；再刪殘留的 `prune` 進度檔。
//! 8. stdout 依序列出刪掉的路徑與完成的殘留，再逐一請啟動器 `rm-container`，刪掉一個印一行。
//!
//! # 恢復
//!
//! 殘留的 `prune` 進度檔表示上一次 `prune` 中途停了。`prune` 只刪不寫，恢復就是照常再做一次：刪到一半的
//! 路徑這次還會被列出來。這次的刪除完成之後才刪殘留的那幾份；有殘留時即使沒有要刪的路徑，也走一次 `txn`，
//! 讓刪除排在 `writes_started` 之後（同 engine/dev）。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 進度檔 `.tmp.prune.<run-id>.toml` 只有 `progress` 的共同欄位：恢復不需要別的。
//! - stdout 的字句（[`text`]）；路徑相對於安裝目錄，目錄以 `/` 結尾，依 `.vendor_kit/` 下的相對路徑排序。
//! - `ps` 的輸出（`res.<seq>.out`）是一行一個 64 位小寫 hex 的容器 ID（launcher/launch.sh 的
//!   `docker ps --no-trunc --format '{{.ID}}'`）；重複的只刪一次。
//! - 刪容器排在刪路徑之後：路徑的刪除有進度檔保護，容器在主機上、不在進度檔裡。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - 殘留的進度檔是其他 verb 的（`add`、`upgrade`、`remove` 等）：04 說可寫 recipe 先恢復未完成操作，但
//!   `prune` 不代替完成別的指令；VK0004、VK0041 的情況只寫 `sync` 與唯讀 recipe，訊息表沒有 `prune` 的碼。
//!   照常刪也不行：中斷的 `add` 最後才寫鎖定行，它的 `cache/<repo>/` 看起來就是未鎖定的工具目錄，`txn` 換
//!   `cache/` 的 `.tmp.<repo>.old` 也可能是恢復要用的。所以在刪任何東西之前停下。
//! - 未鎖定的工具目錄仍被 `gen/tools.just` 引用：重產入口檔是 `sync` 的事，`prune` 不代做；04 沒說這時
//!   怎麼辦，訊息表也沒有碼。
//! - 啟動器代做的 `ps`、`rm-container` 失敗：VK0055 只寫取工具 image 的 docker 動作，`prune` 沒有碼。`ps`
//!   失敗時在刪任何東西之前停下；`rm-container` 失敗時其他容器照刪，每個失敗各報一次。
//! - 刪 image：D2（#372 留言 issuecomment-5997655839）定協定不提供刪 image 的 op，這一版不刪，也不停下。
//! - 主機上殘留的 session 目錄（`${TMPDIR:-/tmp}/vendor_kit.<run-id>/`）：在 repo 外、由啟動器擁有
//!   （ADR-0006、ADR-0007），引擎看不到，協定也沒有對應的 op；這一版不清，也不停下。
//! - 中途刪檔失敗沒有代碼（G4）。
//!
//! 這裡不直接碰 docker：docker 動作一律是 `plan` 協定的 op，由啟動器代做。

pub mod text;

#[cfg(test)]
mod tests;

use std::collections::BTreeMap;
use std::fs;
use std::io::{self, Write};
use std::path::{Path, PathBuf};
use std::time::Duration;

use config::{Config, ConfigError};
use diagnostics::{Diagnostic, Diagnostics, Message, Sink};
use filelock::{Lock, Mode};
use layout::InstallDir;
use plan::{Channel, Container, Op, Outcome};
use progress::Progress;
use txn::{Disk, Txn};
use version_file::LockFile;

/// 進度檔的 `<verb>`。
pub const VERB: &str = "prune";
/// VK 暫存的檔名前綴（ADR-0002 `.gitignore` 的 `.tmp.*`）。
pub const TEMP_PREFIX: &str = ".tmp.";
/// 工具印記的檔名後綴（[`stamp::tool_file`]：`cache/<repo>.stamp.toml`）。
pub const STAMP_SUFFIX: &str = ".stamp.toml";

/// 這次執行的環境：容器內的路徑、往返通道與輸出。`prune` 不詢問，所以沒有 stdin 與終端狀態。
pub struct Env<'a, W: Write, S: Sink, L: Write> {
    /// 容器內的安裝目錄（`plan::mount::ROOT`）。
    pub dir: &'a InstallDir,
    /// 主機上的安裝目錄，填 `<install_dir>`。
    pub host_root: &'a str,
    /// 主機上的執行紀錄路徑，填 VK0056 的 `<path>`。
    pub run_log: &'a str,
    pub channel: &'a mut Channel,
    /// 等 result 時多久看一次。
    pub poll: Duration,
    /// `just vendor_kit` 之後的參數原樣（第一個是 `prune`）。
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

/// 跑一次 `prune`，回傳結束碼。
pub fn run<W: Write, S: Sink, L: Write>(env: &mut Env<'_, W, S, L>) -> u8 {
    let mut prune = Prune { env, code: 0 };
    let _ = prune.run();
    prune.code
}

/// 要刪的一個路徑。
#[derive(Debug, Clone, PartialEq, Eq)]
struct Removal {
    /// 相對於 `.vendor_kit/`。
    rel: PathBuf,
    /// 是目錄（印的時候以 `/` 結尾）。
    dir: bool,
}

/// 刪任何東西之前判定的結果。
struct Judged {
    /// 殘留的 `prune` 進度檔。
    residual: Vec<progress::Entry>,
    /// 要刪的路徑，依相對路徑排序。
    removes: Vec<Removal>,
}

/// 診斷已印、這次執行停下。
struct Stop;

type Step<T> = Result<T, Stop>;

struct Prune<'r, 'a, W: Write, S: Sink, L: Write> {
    env: &'r mut Env<'a, W, S, L>,
    code: u8,
}

impl<W: Write, S: Sink, L: Write> Prune<'_, '_, W, S, L> {
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

    /// 容器內路徑換成相對於安裝目錄的寫法。
    fn rel(&self, path: &Path) -> String {
        path.strip_prefix(self.env.dir.root())
            .unwrap_or(path)
            .display()
            .to_string()
    }

    /// 要刪的路徑印出來的樣子：相對於安裝目錄，目錄以 `/` 結尾。
    fn shown(&self, r: &Removal) -> String {
        let mut s = self.rel(&self.env.dir.vk_dir().join(&r.rel));
        if r.dir {
            s.push('/');
        }
        s
    }

    fn say(&mut self, line: &str) {
        let _ = writeln!(self.env.stdout, "{line}");
    }

    // ---- 流程 ----

    fn run(&mut self) -> Step<()> {
        let config = self.config()?;
        let lock = self.lock(&config)?;
        let lockfile = self.lockfile()?;
        let Judged { residual, removes } = self.judge(&lockfile)?;
        let containers = if lock.warning().is_none() {
            self.ps()?
        } else {
            // 沒有鎖就證明不了容器不再使用（模組說明）。
            Vec::new()
        };

        if !removes.is_empty() || !residual.is_empty() {
            self.land(&removes)?;
            for e in &residual {
                if let Err(err) = progress::delete(self.env.dir, &e.verb, &e.id) {
                    let d = self.failed_diag(&e.path, err.message(), err.to_string());
                    return Err(self.stop(d));
                }
            }
            for r in &removes {
                let line = text::removed(&self.shown(r));
                self.say(&line);
            }
            for e in &residual {
                let line = text::recovered(&self.rel(&e.path));
                self.say(&line);
            }
        }

        for c in &containers {
            let (_, outcome) = self.request(&Op::RmContainer(c.clone()))?;
            match outcome {
                Outcome::Ok => self.say(&text::removed_container(c.as_str())),
                Outcome::Failed(rc) => {
                    let d = self.gap_diag(format_args!(
                        "reporting that {} for stopped container {} (no reason code for prune)",
                        text::docker_failed("rm", rc),
                        c.as_str()
                    ));
                    self.emit(d);
                }
                Outcome::Runner(_) => {
                    return Err(self.internal("rm-container returned a runner result"));
                }
            }
        }
        Ok(())
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

    /// 刪任何東西之前的判定（模組說明第 4 步）：只讀。有任何一項不能做就把每一項都印出來再停下。
    fn judge(&mut self, lockfile: &LockFile) -> Step<Judged> {
        let mut blocked: Vec<Diagnostic> = Vec::new();

        let mut residual = Vec::new();
        let mut progress_files = Vec::new();
        match progress::find(self.env.dir) {
            Ok(entries) => {
                for entry in entries {
                    progress_files.push(entry.path.clone());
                    match self.residual(&entry) {
                        Ok(()) => residual.push(entry),
                        Err(d) => blocked.push(d),
                    }
                }
            }
            Err(e) => blocked.push(self.internal_diag(e.to_string())),
        }

        // 依 `.vendor_kit/` 下的相對路徑排序、去重。
        let mut removes: BTreeMap<PathBuf, bool> = BTreeMap::new();
        let vk = self.env.dir.vk_dir();
        for sub in ["", "cache", "gen", "baseline"] {
            let rel = PathBuf::from(sub);
            match list(&vk.join(&rel)) {
                Ok(names) => {
                    for (name, is_dir) in names {
                        let path = rel.join(&name);
                        if name.starts_with(TEMP_PREFIX)
                            && !progress_files.contains(&vk.join(&path))
                        {
                            removes.insert(path, is_dir);
                        }
                    }
                }
                Err(e) => blocked.push(self.internal_diag(e)),
            }
        }

        let entry = self.env.dir.gen_dir().join(txn::TOOLS_JUST);
        let entry = match fs::read_to_string(&entry) {
            Ok(t) => t,
            Err(e) if e.kind() == io::ErrorKind::NotFound => String::new(),
            Err(e) => {
                blocked.push(self.internal_diag(format!("{}: {e}", entry.display())));
                String::new()
            }
        };
        match list(&self.env.dir.cache_dir()) {
            Ok(names) => {
                for (name, is_dir) in names {
                    if name.starts_with(TEMP_PREFIX) {
                        continue;
                    }
                    if is_dir {
                        if !fetch::is_namespace(&name) || lockfile.tools().contains_key(&name) {
                            continue;
                        }
                        if entry.contains(&format!("'../cache/{name}/")) {
                            blocked.push(self.gap_diag(format_args!(
                                "pruning .vendor_kit/cache/{name}/, which is not in the lock version \
                                 line but .vendor_kit/gen/tools.just still references \
                                 (no reason code; run sync first)"
                            )));
                            continue;
                        }
                        removes.insert(Path::new("cache").join(&name), true);
                    } else if let Some(repo) = name.strip_suffix(STAMP_SUFFIX) {
                        let is_stamp = fetch::is_namespace(repo)
                            && stamp::tool_file(self.env.dir, repo)
                                == self.env.dir.cache_dir().join(&name);
                        if is_stamp && !lockfile.tools().contains_key(repo) {
                            removes.insert(Path::new("cache").join(&name), false);
                        }
                    }
                }
            }
            Err(e) => blocked.push(self.internal_diag(e)),
        }

        if blocked.is_empty() {
            Ok(Judged {
                residual,
                removes: removes
                    .into_iter()
                    .map(|(rel, dir)| Removal { rel, dir })
                    .collect(),
            })
        } else {
            for d in blocked {
                self.emit(d);
            }
            Err(Stop)
        }
    }

    /// 一份殘留的進度檔：`prune` 的回 `Ok`（這次一起完成），其他的回要印的診斷。
    fn residual(&self, entry: &progress::Entry) -> Result<(), Diagnostic> {
        let loaded = match entry.load() {
            Ok(p) => p,
            Err(progress::Error::Parse {
                file,
                source: progress::ParseError::Read(schema::ReadError::TooNew(t)),
            }) => return Err(self.too_new_diag(&file, &t)),
            Err(e) => return Err(self.failed_diag(&entry.path, e.message(), e.to_string())),
        };
        if entry.verb == VERB {
            return Ok(());
        }
        Err(self.gap_diag(format_args!(
            "prune while the incomplete {} operation in {} remains \
             (no reason code for prune; finish it first: {})",
            entry.verb,
            self.rel(&entry.path),
            full_command(loaded.command())
        )))
    }

    /// 請啟動器做一個 docker 動作，等結果。
    fn request(&mut self, op: &Op) -> Step<(plan::Seq, Outcome)> {
        let sent = self.env.channel.send(op);
        let seq = sent.map_err(|e| self.internal(e.to_string()))?;
        let reply = self.env.channel.receive(self.env.poll);
        let reply = reply.map_err(|e| self.internal(e.to_string()))?;
        Ok((seq, reply.outcome))
    }

    /// 請啟動器列出本安裝目錄已停止的 VK 容器（模組說明第 5 步）。
    fn ps(&mut self) -> Step<Vec<Container>> {
        let (seq, outcome) = self.request(&Op::Ps)?;
        match outcome {
            Outcome::Ok => {}
            Outcome::Failed(rc) => {
                let d = self.gap_diag(format_args!(
                    "reporting that {} (no reason code for prune)",
                    text::docker_failed("ps", rc)
                ));
                return Err(self.stop(d));
            }
            Outcome::Runner(_) => return Err(self.internal("ps returned a runner result")),
        }
        let out = self.env.channel.output_path(seq);
        let text = match fs::read_to_string(&out) {
            Ok(t) => t,
            Err(e) => return Err(self.internal(format!("{}: {e}", out.display()))),
        };
        match parse_ps(&text) {
            Ok(c) => Ok(c),
            Err(e) => Err(self.internal(e)),
        }
    }

    /// 依收回順序刪路徑（模組說明第 7 步）：repo 檔、入口檔、版本鎖定行都不動。
    fn land(&mut self, removes: &[Removal]) -> Step<txn::Done> {
        let progress = match Progress::new(VERB, self.env.run_id, self.env.argv) {
            Ok(p) => p,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let paths: Vec<&Path> = removes.iter().map(|r| r.rel.as_path()).collect();
        let result = {
            let mut fx = Disk::new(self.env.dir, self.env.log, self.env.written_by);
            Txn::begin(&mut fx, progress).and_then(|t| {
                t.retract_repo_files(&[])?
                    .retract_tools_just(txn::Entry::Keep)?
                    .retract_records(&[], &paths)?
                    .keep_lock_line()
                    .complete()
            })
        };
        result.map_err(|f| self.internal(f.to_string()))
    }
}

/// POSIX shell 引號：只含安全字元的字原樣留下；其他（含空字串）包單引號，`'` 換成 `'\''`
/// （engine/sync 的 `shell_quote`；指令之間互不依賴，照抄）。
pub fn shell_quote(s: &str) -> String {
    let safe = |c: char| c.is_ascii_alphanumeric() || "_@%+=:,./-".contains(c);
    if !s.is_empty() && s.chars().all(safe) {
        return s.to_owned();
    }
    format!("'{}'", s.replace('\'', r"'\''"))
}

/// 由進度檔的 `command`（`just vendor_kit` 之後的參數）重組完整指令（engine/sync 的 `full_command`；照抄）。
pub fn full_command<S: AsRef<str>>(command: &[S]) -> String {
    ["just", "vendor_kit"]
        .iter()
        .map(|w| (*w).to_owned())
        .chain(command.iter().map(|w| shell_quote(w.as_ref())))
        .collect::<Vec<_>>()
        .join(" ")
}

/// 一層目錄裡的項目：名字與是不是目錄（不跟隨 symlink）。目錄不在回空清單；名字不是 UTF-8 的略過
/// （不是 VK 寫的）。依名字排序。
fn list(dir: &Path) -> Result<Vec<(String, bool)>, String> {
    let read = match fs::read_dir(dir) {
        Ok(r) => r,
        Err(e) if e.kind() == io::ErrorKind::NotFound => return Ok(Vec::new()),
        Err(e) => return Err(format!("{}: {e}", dir.display())),
    };
    let mut out = Vec::new();
    for entry in read {
        let entry = entry.map_err(|e| format!("{}: {e}", dir.display()))?;
        let Ok(name) = entry.file_name().into_string() else {
            continue;
        };
        let ty = entry
            .file_type()
            .map_err(|e| format!("{}: {e}", entry.path().display()))?;
        out.push((name, ty.is_dir()));
    }
    out.sort();
    Ok(out)
}

/// 解析啟動器 `ps` 的輸出：一行一個容器 ID（64 位小寫 hex），每行以 LF 結尾；空的表示沒有。重複的只留一個。
pub fn parse_ps(text: &str) -> Result<Vec<Container>, String> {
    let mut out: Vec<Container> = Vec::new();
    if text.is_empty() {
        return Ok(out);
    }
    let Some(body) = text.strip_suffix('\n') else {
        return Err("ps output does not end with LF".to_owned());
    };
    for line in body.split('\n') {
        let Some(c) = Container::parse(line) else {
            return Err(format!("ps output has an invalid container ID {line:?}"));
        };
        if !out.contains(&c) {
            out.push(c);
        }
    }
    Ok(out)
}
