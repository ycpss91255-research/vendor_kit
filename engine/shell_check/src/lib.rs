//! `bootstrap.sh` 只檢查與 `--repair` 的引擎端（04 bootstrap.sh、ADR-0007）：比對薄殼，修復時只重產不符的檔。
//!
//! 入口是 `plan::entry` 的兩個保留入口（`@shell-check`、`@shell-repair`），只有 `bootstrap.sh` 會送；
//! 經 just 打不到（薄殼的每個 recipe 都把指令名寫死在第一個參數），`args` 一般路徑也不收。呼叫端（入口
//! `vendor_kit`）已接好執行紀錄、判過安裝目錄（VK0028）。這裡依序做：
//!
//! 1. 讀 `.vendor_kit/config.toml`（VK0059），在第一次取鎖之前（04 設定）。
//! 2. 取安裝目錄的鎖（VK0042；`lock_enabled = false` 印 VK0060），持到結束（04 鎖與逾時：bootstrap 啟動的
//!    引擎也用同一設定）：只檢查是讀取，持共享鎖；修復會寫薄殼，持排他鎖。
//! 3. 04 bootstrap.sh 判定順序第 5 步：先看引擎升級未完成的進度檔（`[upgrade] target` 是
//!    [`progress::upgrade::ENGINE_TARGET`]），有就回 VK0023，不比對、不重產薄殼。其他殘留的進度檔不擋
//!    （VK0054：bootstrap.sh 只依 VK0037 與 VK0023 判定）。讀進度檔時檔案版過高回 VK0008。
//! 4. 以 `compat` 的介面版、本引擎版與隨 image 出貨的模板本文（呼叫端給，跟 `install`、`sync` 用的是同一份）
//!    產生這一版的薄殼，跑 `shell::Shell::check`。模板沒有（image 沒出貨）或薄殼檔是 symlink、不是一般檔：
//!    VK0056。
//! 5. 只檢查：一致就在 stdout 報一致、回 0；不符回 VK0006，`<files>` 逐檔標出是哪一種。不寫檔。
//! 6. 修復：一致就在 stdout 報一致、不重產、回 0；不符時不詢問，先在 stdout 逐檔列出差異，再
//!    `shell::Shell::write_mismatched` 只重產不符的檔，最後報告重產了哪些檔、回 0。只寫 `.vendor_kit/` 下的
//!    薄殼四檔（04 寫入範圍）：不建進度檔，不寫鎖定行、`gen/.stamp`、設定、根目錄檔或其他狀態。
//!
//! # 這次自訂的內部細節（契約沒寫，使用者看不到格式以外的差別）
//!
//! - 兩個保留入口的名稱（`plan::entry`）：以 `@` 起頭，just 的 recipe 名不能以 `@` 起頭，也不會跟 VK recipe
//!   的指令名撞。這是 D2 協定的新增項，跟救援路徑一起永久不變（`plan` 的測試釘住）。
//! - VK0006 的 `<files>` 與修復時列的差異都寫成 `.vendor_kit/<檔名> (<哪一種>)`，順序同 `layout::SHELL_FILES`
//!   （跟 engine/sync 的寫法一致）；stdout 的字句見 [`text`]。
//! - VK0023 的 `<vY>` 填本引擎版：`bootstrap.sh` 用版本鎖定行那一版引擎檢查，`upgrade --engine` 換好鎖定行
//!   之後留下的進度檔，由新引擎讀到（見「缺口」）。`<original_command>` 由進度檔的 `command` 重組
//!   （[`original_command`]，從 engine/update 照抄；指令之間互不依賴）。
//!
//! # 缺口（契約或其他 crate 沒定，不自己補規則；遇到就以 VK0056 停下並寫明原因）
//!
//! - `progress::upgrade` 還沒記引擎 upgrade 的目標版（`upgrade --engine` 還沒實作）。進度檔寫好、鎖定行還沒
//!   換的那一段中斷時，鎖定行仍是舊引擎，VK0023 的 `<vY>` 會填舊引擎版；要重跑的原指令照樣正確。
//!   進度檔記了目標版之後改從進度檔讀。
//! - 未完成的 `uninstall`（鎖定行還在時）還不辨識，照常比對薄殼。
//! - 重產到一半寫檔失敗沒有代碼（計畫 G4），已重產的檔不還原。

pub mod text;

#[cfg(test)]
mod tests;

use std::io::Write;
use std::path::Path;

use config::{Config, ConfigError};
use diagnostics::{Diagnostic, Diagnostics, Sink};
use filelock::{Lock, Mode as LockMode};
use layout::InstallDir;
use shell::Shell;

/// 重組 `<original_command>` 時接在參數前面的字（engine/update 的 `COMMAND_PREFIX`）。
pub const COMMAND_PREFIX: [&str; 2] = ["just", "vendor_kit"];

/// 只檢查或修復。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Mode {
    /// `bootstrap.sh` 不帶選項：只檢查，不寫檔。
    Check,
    /// `bootstrap.sh --repair`：只重產不符的薄殼檔。
    Repair,
}

/// 這次執行的環境。不詢問，所以沒有 stdin 與終端狀態。
pub struct Env<'a, W: Write, S: Sink> {
    /// 容器內的安裝目錄（`plan::mount::ROOT`）。
    pub dir: &'a InstallDir,
    /// 主機上的安裝目錄，填 `<install_dir>`。
    pub host_root: &'a str,
    /// 主機上的執行紀錄路徑，填 VK0056 的 `<path>`。
    pub run_log: &'a str,
    /// 本引擎版：寫進薄殼標頭，也填 VK0023 的 `<vY>`。
    pub written_by: &'a str,
    /// 隨 image 出貨的薄殼四檔模板本文（`install::Release::shell`）；image 沒出貨時是 `None`。
    pub shell_templates: Option<&'a [Vec<u8>; layout::SHELL_FILES.len()]>,
    /// 檢查結果與重產報告（03 輸出：成功時改了什麼、檢查結果印到 stdout）。
    pub stdout: &'a mut dyn Write,
    pub diags: &'a mut Diagnostics<W, S>,
}

/// 跑一次只檢查或修復，回傳結束碼。
pub fn run<W: Write, S: Sink>(mode: Mode, env: &mut Env<'_, W, S>) -> u8 {
    let mut check = ShellCheck { env, code: 0 };
    let _ = check.run(mode);
    let _ = check.env.stdout.flush();
    check.code
}

/// POSIX shell 引號：只含安全字元的字原樣留下；其他（含空字串）包單引號，`'` 換成 `'\''`
/// （engine/update 的 `shell_quote`）。
pub fn shell_quote(s: &str) -> String {
    let safe = |c: char| c.is_ascii_alphanumeric() || "_@%+=:,./-".contains(c);
    if !s.is_empty() && s.chars().all(safe) {
        return s.to_owned();
    }
    format!("'{}'", s.replace('\'', r"'\''"))
}

/// 由進度檔的 `command`（`just vendor_kit` 之後的參數）重組完整指令（engine/update 的 `original_command`）。
pub fn original_command<S: AsRef<str>>(command: &[S]) -> String {
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

struct ShellCheck<'r, 'a, W: Write, S: Sink> {
    env: &'r mut Env<'a, W, S>,
    code: u8,
}

impl<W: Write, S: Sink> ShellCheck<'_, '_, W, S> {
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

    fn line(&mut self, s: &str) {
        let _ = writeln!(self.env.stdout, "{s}");
    }

    // ---- 流程 ----

    fn run(&mut self, mode: Mode) -> Step<()> {
        let config = self.config()?;
        let _lock = self.lock(&config, mode)?;
        self.engine_upgrade()?;
        let shell = self.shell()?;
        let report = match shell.check(self.env.dir) {
            Ok(r) => r,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        if report.is_consistent() {
            self.line(text::CONSISTENT);
            return Ok(());
        }
        let files: Vec<String> = report
            .mismatches()
            .map(|f| text::file(f.name, f.status))
            .collect();
        match mode {
            Mode::Check => {
                let d = Diagnostic::new(&messages::VK0006).arg("files", files.join(", "));
                Err(self.stop(d))
            }
            Mode::Repair => {
                // 先逐檔列出差異，寫入前就讓使用者看到（ADR-0007：寫入前列出逐檔差異、完成後報告）。
                self.line(text::DIFFERENCES);
                for f in &files {
                    self.line(&format!("  {f}"));
                }
                let _ = self.env.stdout.flush();
                let written = match shell.write_mismatched(self.env.dir, &report) {
                    Ok(w) => w,
                    Err(e) => {
                        return Err(self.internal(format!("{e}; reason code pending (G4)")));
                    }
                };
                for name in written {
                    self.line(&text::regenerated(name));
                }
                Ok(())
            }
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

    fn lock(&mut self, config: &Config, mode: Mode) -> Step<Lock> {
        let lock_mode = match mode {
            Mode::Check => LockMode::Shared,
            Mode::Repair => LockMode::Exclusive,
        };
        match Lock::acquire(self.env.dir, lock_mode, config) {
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

    /// 第 3 步：引擎升級未完成的進度檔回 VK0023（每一份各一條），其他殘留的進度檔不看。
    fn engine_upgrade(&mut self) -> Step<()> {
        let entries = match progress::find(self.env.dir) {
            Ok(e) => e,
            Err(e) => return Err(self.internal(e.to_string())),
        };
        let mut found = Vec::new();
        for entry in entries.iter().filter(|e| e.verb == progress::upgrade::VERB) {
            let loaded = match entry.load() {
                Ok(p) => p,
                Err(progress::Error::Parse {
                    file,
                    source: progress::ParseError::Read(schema::ReadError::TooNew(t)),
                }) => return Err(self.too_new(&file, &t)),
                Err(e) => return Err(self.internal(e.to_string())),
            };
            if progress::upgrade::field(&loaded, progress::upgrade::TARGET)
                == Some(progress::upgrade::ENGINE_TARGET)
            {
                found.push(original_command(loaded.command()));
            }
        }
        if found.is_empty() {
            return Ok(());
        }
        for command in found {
            let d = Diagnostic::new(&messages::VK0023)
                .arg("vY", self.env.written_by)
                .arg("original_command", command);
            self.emit(d);
        }
        Err(Stop)
    }

    /// 第 4 步：這一版引擎的薄殼。
    fn shell(&mut self) -> Step<Shell> {
        let Some(t) = self.env.shell_templates else {
            return Err(self.internal(
                "checking the shell without the shell templates, which this engine image does not ship, is not supported yet",
            ));
        };
        let bodies = [&t[0][..], &t[1][..], &t[2][..], &t[3][..]];
        match Shell::render(compat::THIS.current_protocol, self.env.written_by, bodies) {
            Ok(s) => Ok(s),
            Err(e) => Err(self.internal(e.to_string())),
        }
    }
}
