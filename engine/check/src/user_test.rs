//! `test <path>`：先選測試，再做完整安裝檢查，通過才請啟動器跑使用者的 runner（04 test 路徑與 runner）。
//!
//! 跟不帶 path 的檢查共用同一份設定與共享鎖，鎖持到 runner 結束才放（引擎全程持鎖，`plan` 的說明），
//! 所以 runner 跑的期間別的指令改不了 `cache/`、`gen/`。依序做：
//!
//! 1. 讀 `.vendor_kit/config.toml`（VK0059 無效值）、取共享鎖（VK0042；VK0060），同不帶 path 的檢查。
//! 2. 選測試（見「這次自訂的內部細節」）：path 不合回 VK0063。
//! 3. 依 `.vendor_kit/baseline/<repo>.toml` 的紀錄判定選取範圍含不含工具交付的測試：含就每個工具一條 VK0064。
//! 4. 沒選到測試回 VK0065；`[test]` 或其中的 `image`、`command` 缺回 VK0059（`<value>` 是 `missing`）。
//! 5. 完整安裝檢查（跟不帶 path 的 `test` 同一份）：不過就照常印出每一項，再印 VK0062，整次以
//!    `max(檢查碼, 2)` 結束，不啟動 runner。通過時 stdout 照樣印通過那一行。
//! 6. 送 `runner` op：image 是 `[test].image`，command 是 `[test].command` 的第一個元素，其餘元素後面加上
//!    使用者打的 path（原樣）。啟動器回的 runner result 照 [`plan::RunnerOutcome::failure`] 發碼：起不來或被 VK
//!    停掉是 VK0066，自己結束且非 0 是 VK0067，兩者的續行都印 runner 的原始結束碼（沒有就是 `unavailable`）；
//!    source 維持 `test`（#372 N71：由引擎依啟動器回的 result 發碼）。runner 回 0 時不印任何字。
//!
//! # 這次自訂的內部細節（契約沒寫）
//!
//! - path 的寫法：第一段必須是 `test`，不准絕對路徑、`.`、`..` 開頭或含 `..`；單獨的 `test` 選整個 `test/`。
//! - 符號連結：path 本身與資料夾裡找到的每一項都先解析，必須仍在安裝目錄的 `test/`（不解析 `test` 本身）
//!   底下，否則是 VK0063。資料夾裡指到資料夾的符號連結只檢查指到哪裡，不往下走（避免迴圈）。
//! - 「選到的測試」是選取範圍裡的一般檔（含指到一般檔的符號連結）；空資料夾是 VK0065。一般檔與資料夾以外的
//!   檔（FIFO、socket 等）算無效的選取檔（VK0063）。
//! - VK0064 的「工具交付」：版本鎖定行裡每個工具的紀錄中，`managed`（整份初始檔）與 `appended`（插入行）
//!   兩種狀態的檔；比對解析符號連結後的實際路徑。`declined`、`unmanaged` 不是工具交付的內容，`deleted` 的檔
//!   不在。
//! - VK0060（`lock_enabled = false`）是取鎖時每次執行都印的警告，不算安裝檢查的結果：鎖關著時檢查通過照樣
//!   啟動 runner，整次結束碼仍取 1 與 runner 結果的較大者。否則鎖關著的安裝目錄永遠跑不了測試。
//! - runner 的 image 欄（D16）：介面版 2 起寫成自由文字欄，`[test].image` 只要非空、不以 `-` 開頭就照原樣交給
//!   主機 Docker（04 只要求非空字串；以 `-` 開頭的會被 docker create 當成選項）。呼叫方的介面版是 1 時照舊文法
//!   `ref`（tag 有大寫字母等就送不出）。送不出時回 VK0066，`<reason>` 寫明，續行印 `unavailable`。
//!
//! # 缺口
//!
//! - VK0064 要靠初始檔的紀錄，`add`、`upgrade` 讀 `init.toml` 的地方還在等 #372 N3，實際走不到；判法先照
//!   上面寫好並有單元測試。

use std::collections::BTreeSet;
use std::ffi::OsStr;
use std::fs;
use std::io::{self, Write};
use std::os::unix::ffi::OsStrExt;
use std::path::{Component, Path, PathBuf};
use std::time::Duration;

use config::Config;
use diagnostics::{Diagnostic, Sink};
use metadata::{Metadata, State};
use plan::{Channel, Field, Op, Outcome, RunnerOutcome};
use version_file::LockFile;

use super::{Check, Env, Step, Stop, text};

/// 安裝目錄底下放使用者測試的資料夾名，也是 path 必須的第一段（04：寫成 `test/...`）。
pub const TEST_DIR: &str = "test";

/// VK0066、VK0067 的續行在沒有 runner 結束碼時印的字（訊息表 VK0066）。
pub const UNAVAILABLE: &str = "unavailable";

/// `test <path>` 的往返通道。
pub struct Runner<'a> {
    pub channel: &'a mut Channel,
    /// 等啟動器回 result 時多久看一次。
    pub poll: Duration,
}

/// 跑一次 `test <path>`，回傳結束碼。`path` 是使用者打的原樣。
pub fn run<W: Write, S: Sink>(
    path: &OsStr,
    runner: &mut Runner<'_>,
    env: &mut Env<'_, W, S>,
) -> u8 {
    let mut check = Check { env, code: 0 };
    let _ = check.user_test(path, runner);
    check.code
}

/// 選到的測試：選取範圍裡每個一般檔解析符號連結後的實際路徑。
#[derive(Debug, Default)]
struct Selection {
    files: BTreeSet<PathBuf>,
}

/// path 不合（VK0063）或讀檔失敗（VK0056）。
enum SelectError {
    Invalid(String),
    Io(String),
}

impl SelectError {
    fn io(path: &Path, e: &io::Error) -> SelectError {
        SelectError::Io(format!("{}: {e}", path.display()))
    }
}

/// path 的寫法：第一段是 `test`，之後只有一般的段。
fn lexical(path: &Path) -> Result<(), String> {
    let mut parts = path.components();
    match parts.next() {
        Some(Component::Normal(first)) if first == TEST_DIR => {}
        _ => return Err(format!("it is not written as {TEST_DIR}/...")),
    }
    if parts.any(|c| !matches!(c, Component::Normal(_))) {
        return Err("it contains a .. component".to_owned());
    }
    Ok(())
}

/// 選測試（模組說明「這次自訂的內部細節」）：每一項解析後都要在 `<安裝目錄解析後>/test` 底下。
fn select(root: &Path, path: &Path) -> Result<Selection, SelectError> {
    lexical(path).map_err(SelectError::Invalid)?;
    let canonical_root = fs::canonicalize(root).map_err(|e| SelectError::io(root, &e))?;
    let base = canonical_root.join(TEST_DIR);
    let full = root.join(path);
    let meta = match fs::symlink_metadata(&full) {
        Ok(m) => m,
        Err(e) if e.kind() == io::ErrorKind::NotFound => {
            return Err(SelectError::Invalid("it does not exist".to_owned()));
        }
        Err(e) => return Err(SelectError::io(&full, &e)),
    };
    let mut sel = Selection::default();
    if meta.is_dir() {
        resolve(&full, path, &base)?;
        walk(&full, path, &base, &mut sel)?;
    } else {
        add_entry(&full, path, &base, &mut sel, true)?;
    }
    Ok(sel)
}

/// 解析符號連結後的實際路徑，必須在 `base` 底下。
fn resolve(full: &Path, shown: &Path, base: &Path) -> Result<PathBuf, SelectError> {
    let real = match fs::canonicalize(full) {
        Ok(p) => p,
        Err(e) if e.kind() == io::ErrorKind::NotFound => {
            return Err(SelectError::Invalid(format!(
                "{} is a broken symbolic link",
                shown.display()
            )));
        }
        Err(e) => return Err(SelectError::io(full, &e)),
    };
    if !real.starts_with(base) {
        return Err(SelectError::Invalid(format!(
            "{} resolves outside {TEST_DIR}/ of the install directory",
            shown.display()
        )));
    }
    Ok(real)
}

/// 一個不是真資料夾的項目：一般檔（或指到一般檔的符號連結）算選到；指到資料夾的符號連結在資料夾裡
/// 只檢查位置（`top` 是 path 本身時照樣往下走）；其他種類的檔無效。
fn add_entry(
    full: &Path,
    shown: &Path,
    base: &Path,
    sel: &mut Selection,
    top: bool,
) -> Result<(), SelectError> {
    let real = resolve(full, shown, base)?;
    let meta = fs::metadata(&real).map_err(|e| SelectError::io(&real, &e))?;
    if meta.is_file() {
        sel.files.insert(real);
        Ok(())
    } else if meta.is_dir() {
        if top {
            walk(full, shown, base, sel)
        } else {
            Ok(())
        }
    } else {
        Err(SelectError::Invalid(format!(
            "{} is not a regular file or directory",
            shown.display()
        )))
    }
}

/// 資料夾含子資料夾；依名稱排序，結果與讀取順序無關。
fn walk(dir: &Path, shown: &Path, base: &Path, sel: &mut Selection) -> Result<(), SelectError> {
    let mut names: Vec<_> = fs::read_dir(dir)
        .map_err(|e| SelectError::io(dir, &e))?
        .map(|e| e.map(|e| e.file_name()))
        .collect::<Result<_, _>>()
        .map_err(|e| SelectError::io(dir, &e))?;
    names.sort();
    for name in names {
        let full = dir.join(&name);
        let shown = shown.join(&name);
        let meta = fs::symlink_metadata(&full).map_err(|e| SelectError::io(&full, &e))?;
        if meta.is_dir() {
            resolve(&full, &shown, base)?;
            walk(&full, &shown, base, sel)?;
        } else {
            add_entry(&full, &shown, base, sel, false)?;
        }
    }
    Ok(())
}

impl<W: Write, S: Sink> Check<'_, '_, W, S> {
    fn user_test(&mut self, path: &OsStr, runner: &mut Runner<'_>) -> Step<()> {
        let shown = path.to_string_lossy().into_owned();
        let config = self.config()?;
        let _lock = self.lock(&config)?;

        let sel = self.selection(path, &shown)?;
        self.delivered(&sel, &shown)?;
        if sel.files.is_empty() {
            let d = Diagnostic::new(&messages::VK0065).arg("path", shown.as_str());
            return Err(self.stop(d));
        }
        let test = self.test_config(&config)?;

        // VK0060 不算安裝檢查的結果（模組說明）：先記下，檢查碼只看檢查本身。
        let warned = std::mem::replace(&mut self.code, 0);
        let checked = self.inspect();
        let check_code = self.code;
        self.code = self.code.max(warned);
        if checked.is_err() || check_code != 0 {
            let d = Diagnostic::new(&messages::VK0062)
                .arg("check_exit_code", check_code.to_string())
                .arg("path", shown.as_str());
            return Err(self.stop(d));
        }
        self.say(text::PASSED);

        let protocol = runner.channel.header().protocol();
        let op = self.runner_op(&test, path, &shown, protocol)?;
        let outcome = self.request(runner, &op)?;
        self.report(outcome, &shown);
        Ok(())
    }

    fn selection(&mut self, path: &OsStr, shown: &str) -> Step<Selection> {
        match select(self.env.dir.root(), Path::new(path)) {
            Ok(sel) => Ok(sel),
            Err(SelectError::Invalid(reason)) => {
                let d = Diagnostic::new(&messages::VK0063)
                    .arg("path", shown)
                    .arg("reason", reason);
                Err(self.stop(d))
            }
            Err(SelectError::Io(e)) => Err(self.internal(e)),
        }
    }

    /// 選取範圍含工具交付的測試：每個工具一條 VK0064（模組說明「這次自訂的內部細節」）。
    /// 版本鎖定行讀不進來時不判，交給安裝檢查報。
    fn delivered(&mut self, sel: &Selection, shown: &str) -> Step<()> {
        let Ok(Some(lockfile)) = LockFile::load_from(self.env.dir) else {
            return Ok(());
        };
        let mut found: Vec<Diagnostic> = Vec::new();
        for repo in lockfile.tools().keys() {
            let file = match metadata::tool_path(self.env.dir, repo) {
                Ok(p) => p,
                Err(e) => return Err(self.internal(e.to_string())),
            };
            if !file.exists() {
                continue;
            }
            let records = match Metadata::load(&file) {
                Ok(m) => m,
                Err(metadata::Error::TooNew { file, too_new }) => {
                    let d = self.too_new_diag(&file, &too_new);
                    return Err(self.stop(d));
                }
                Err(e) => {
                    let d = self.failed_diag(e.file(), e.message(), e.to_string());
                    return Err(self.stop(d));
                }
            };
            let hit = records.files().iter().any(|r| {
                matches!(r.state, State::Managed | State::Appended)
                    && fs::canonicalize(self.env.dir.root().join(&r.path))
                        .is_ok_and(|real| sel.files.contains(&real))
            });
            if hit {
                found.push(
                    Diagnostic::new(&messages::VK0064)
                        .arg("path", shown)
                        .arg("repo", repo.as_str()),
                );
            }
        }
        if found.is_empty() {
            return Ok(());
        }
        for d in found {
            self.emit(d);
        }
        Err(Stop)
    }

    /// `[test]` 的 image 與 command；缺就是 VK0059。
    fn test_config(&mut self, config: &Config) -> Step<config::Runner> {
        match config.runner() {
            Ok(r) => Ok(r),
            Err(e) => {
                let d = Diagnostic::new(e.message())
                    .arg("field", e.field().name())
                    .arg("value", e.value())
                    .arg("fix", e.fix());
                Err(self.stop(d))
            }
        }
    }

    fn not_started(&mut self, shown: &str, reason: impl Into<String>) -> Stop {
        let d = Diagnostic::new(&messages::VK0066)
            .arg("path", shown)
            .arg("reason", reason)
            .arg("runner_exit_code", UNAVAILABLE);
        self.stop(d)
    }

    fn runner_op(
        &mut self,
        test: &config::Runner,
        path: &OsStr,
        shown: &str,
        protocol: u32,
    ) -> Step<Op> {
        let fits = Op::runner_image_fits(test.image.as_bytes(), protocol);
        let image = match Field::new(test.image.as_bytes().to_vec()) {
            Ok(f) if fits => f,
            _ if protocol < plan::SINCE_V2 => {
                return Err(self.not_started(
                    shown,
                    format!(
                        "the image reference {:?} cannot be passed to the launcher \
                         (only lowercase letters, digits and . _ / : @ - are accepted)",
                        test.image
                    ),
                ));
            }
            _ => {
                return Err(self.not_started(
                    shown,
                    format!(
                        "the image reference {:?} cannot be passed to the launcher \
                         (it must not be empty or start with -)",
                        test.image
                    ),
                ));
            }
        };
        let field = |b: &[u8]| Field::new(b.to_vec());
        let mut words = test.command.iter().map(|w| field(w.as_bytes()));
        let fields: Result<Vec<Field>, _> = match words.next() {
            Some(first) => std::iter::once(first)
                .chain(words)
                .chain(std::iter::once(field(path.as_bytes())))
                .collect(),
            None => return Err(self.internal("[test].command is empty")),
        };
        let mut fields = match fields {
            Ok(f) => f,
            Err(e) => {
                return Err(self.not_started(
                    shown,
                    format!("the command or path cannot be passed to the launcher: {e}"),
                ));
            }
        };
        let command = fields.remove(0);
        Ok(Op::Runner {
            image,
            command,
            args: fields,
        })
    }

    /// 請啟動器跑 runner，等結果。
    fn request(&mut self, runner: &mut Runner<'_>, op: &Op) -> Step<RunnerOutcome> {
        if let Err(e) = runner.channel.send(op) {
            return Err(self.internal(e.to_string()));
        }
        let reply = match runner.channel.receive(runner.poll) {
            Ok(r) => r,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        match reply.outcome {
            Outcome::Runner(o) => Ok(o),
            Outcome::Ok | Outcome::Failed(_) => {
                Err(self.internal("the runner op returned a non-runner result"))
            }
        }
    }

    /// 依 runner result 發碼（#372 N71）；回 0 時不印。
    fn report(&mut self, outcome: RunnerOutcome, shown: &str) {
        let Some(message) = outcome.failure() else {
            return;
        };
        let rc = outcome
            .process_rc()
            .map_or_else(|| UNAVAILABLE.to_owned(), |rc| rc.to_string());
        let d = if message.code == messages::VK0066.code {
            let reason = if outcome.stopped_by_vk() {
                "the runner was stopped by vendor_kit"
            } else {
                "the runner did not start"
            };
            Diagnostic::new(message)
                .arg("path", shown)
                .arg("reason", reason)
                .arg("runner_exit_code", rc)
        } else {
            Diagnostic::new(message)
                .arg("path", shown)
                .arg("runner_exit_code", rc)
        };
        self.emit(d);
    }
}
