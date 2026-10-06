//! 參數分派。
//!
//! 兩種呼叫：
//!
//! - 經啟動器（第一個參數是 `--protocol`）：照 `plan` 的入口 argv 取上下文，接上執行紀錄與往返通道，
//!   判介面版、用法與安裝目錄，再分派到指令；結束前寫 `engine_finished` 與 `done`。
//! - 直接呼叫（其他）：沒有執行紀錄與往返，只處理不帶指令的用法；其餘一律以 VK0026 回報並附簡短用法
//!   （#372 N108）。契約沒定直接呼叫，這是引擎自訂的行為。
//!
//! 介面版（ADR-0008:26、#372 N61、N19）：救援路徑的入口 argv、`hdr`、`done` 與救援 op 跨介面版不變，
//! 所以呼叫方的 P 不論在不在 [`compat::Compat`] 的區間內，引擎都以那個 P 回應、照常寫 `done`。
//! 參數解析完先判介面版（[`gate`]）：P 在區間內照常往下；不在區間內時，救援呼叫（`args::Invocation::is_rescue`
//! 與不帶指令的用法）照常執行、往返只准救援 op，其餘一律先報版本、不報用法錯誤，所以救援候選解析失敗
//! （例如 `upgrade --engine --bogus`）也先報版本。P 低於 floor 是 VK0009（fatal 3）；P 高於上限還沒有專屬
//! 代碼（計畫缺口 G6），跟啟動器一樣暫以 VK0056 停下。兩者都停在任何寫入之前（執行紀錄除外）。
//!
//! `bootstrap.sh` 的只檢查與 `--repair` 經 `--` 之後的保留入口（`plan::entry`，[`reserved_entry`]）進來：`--` 之後
//! 剛好只有那一個參數才算，在 `args` 之前認出來，交給 `shell_check`；其餘一律照 `args` 解析，所以保留入口帶了
//! 其他參數就是 VK0026。保留入口屬救援路徑，介面版不在區間內也照常執行（[`gate`]），執行位置照樣檢查（VK0028）。
//!
//! 目前只實作 `add`、`sync`、`install`、`remove`、`uninstall`、`update`、`upgrade <repo>`、`dev`、`undev`、`prune`
//! 與不帶 path 的 `test`（安裝檢查，engine/check）。04 說明與用法錯誤：不認得的名稱由 just 擋下、到不了引擎；
//! 還沒實作的 `upgrade --engine`、`test <path>`、`test dist` 以 VK0056 停下（#372 N62）。
//! `-h`／`--help` 把 [`output::Help`] 的用法印到 stdout、以 0 結束（03 輸出），不看執行位置；救援呼叫的 `-h`
//! 在介面版不合時也照印，其餘的 `-h` 跟一般呼叫一樣先報版本（[`gate`]）。

use std::ffi::OsString;
use std::fs::File;
use std::io::{BufRead, Write};
use std::path::{Path, PathBuf};
use std::time::Duration;

use diagnostics::{Diagnostic, Diagnostics, Sink};
use output::{Output, SHORT_USAGE};

/// 引擎版本；版本行印 `vendor_kit v<X.Y.Z>`，與 tag 的寫法一致。
pub const VERSION: &str = concat!("v", env!("CARGO_PKG_VERSION"));

/// 等啟動器回 result 時多久看一次。
const POLL: Duration = Duration::from_millis(20);

/// 測試用：設了這個環境變數，三個掛載點改到 `<值>/vk/root` 等（`plan::mount` 前面加上這個目錄）。
/// 啟動器起引擎容器時不帶任何環境變數，正式執行時一定不設；e2e 在主機上直接跑執行檔時用它。
pub const MOUNT_PREFIX_ENV: &str = "VK_TEST_MOUNT_PREFIX";

/// 測試用：設了這個環境變數，`install` 與 `sync` 的薄殼模板改從這個目錄讀（`install::Release::from_dir`），
/// 不讀 image 裡的 `install::release::SHIPPED_DIR`（`install::Release::shipped`）。正式執行時一定不設（啟動器
/// 起引擎容器時不帶任何環境變數）；e2e 在主機上直接跑執行檔，沒有 image 裡的模板，用它給 fixture 模板。
pub const RELEASE_DIR_ENV: &str = "VK_TEST_RELEASE_DIR";

/// 引擎容器內的三個掛載點（`plan::mount`）。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Mounts {
    pub root: PathBuf,
    pub ctl: PathBuf,
    pub inbox: PathBuf,
}

impl Mounts {
    /// `plan::mount` 的掛載點，前面接上 `prefix`（沒有就是原樣）。
    pub fn with_prefix(prefix: Option<&Path>) -> Mounts {
        let at = |p: &str| match prefix {
            Some(base) => base.join(p.trim_start_matches('/')),
            None => PathBuf::from(p),
        };
        Mounts {
            root: at(plan::mount::ROOT),
            ctl: at(plan::mount::CTL),
            inbox: at(plan::mount::IN),
        }
    }

    /// 依 [`MOUNT_PREFIX_ENV`] 決定掛載點。
    pub fn from_env() -> Mounts {
        let prefix = std::env::var_os(MOUNT_PREFIX_ENV).map(PathBuf::from);
        Mounts::with_prefix(prefix.as_deref())
    }
}

/// 跑一次引擎，回傳結束碼。寫入 stdout／stderr 失敗時無處可報，仍回同一個結束碼。
pub fn run<O, E>(
    args: &[OsString],
    mounts: &Mounts,
    stdin: &mut dyn BufRead,
    stdout: O,
    stderr: E,
) -> u8
where
    O: Write + Clone,
    E: Write + Clone,
{
    run_with(&compat::THIS, args, mounts, stdin, stdout, stderr)
}

/// [`run`]，介面版區間由 `compat` 給（測試注入用；正式執行是 [`compat::THIS`]）。
fn run_with<O, E>(
    compat: &compat::Compat,
    args: &[OsString],
    mounts: &Mounts,
    stdin: &mut dyn BufRead,
    stdout: O,
    stderr: E,
) -> u8
where
    O: Write + Clone,
    E: Write + Clone,
{
    if args.first().map(OsString::as_os_str) == Some(plan::argv::PROTOCOL.as_ref()) {
        return launched(compat, args, mounts, stdin, stdout, stderr);
    }
    let mut out = Output::new(stdout, stderr.clone());
    let mut diags = Diagnostics::new(stderr);
    let Some(first) = args.first() else {
        no_command(&mut out, &mut diags);
        return diags.exit_code();
    };
    // 直接呼叫引擎時沒有契約定的診斷：以 VK0026（不認得的參數）回報並附用法（#372 N108）。
    let _ = diags.emit(&Diagnostic::new(&messages::VK0026).arg("value", first.to_string_lossy()));
    let _ = out.stderr_line(SHORT_USAGE);
    let _ = out.flush();
    diags.exit_code()
}

/// 03 輸出：只打 `just vendor_kit` 時，stderr 依序印版本行、VK0024、簡短用法，以 2 結束。
fn no_command<O: Write, E: Write, W: Write, S: Sink>(
    out: &mut Output<O, E>,
    diags: &mut Diagnostics<W, S>,
) {
    let _ = out.stderr_line(&output::version_line(VERSION));
    let _ = diags.emit(&Diagnostic::new(&messages::VK0024));
    let _ = out.stderr_line(SHORT_USAGE);
    let _ = out.flush();
}

/// `--` 之後剛好只有 `bootstrap.sh` 的保留入口（`plan::entry`）時回它的模式；其餘回 `None`，照 `args` 解析。
fn reserved_entry(rest: &[OsString]) -> Option<shell_check::Mode> {
    match rest {
        [only] if *only == *plan::entry::SHELL_CHECK => Some(shell_check::Mode::Check),
        [only] if *only == *plan::entry::SHELL_REPAIR => Some(shell_check::Mode::Repair),
        _ => None,
    }
}

/// 介面版判定：P 在區間內回 `Ok(false)`；不在區間內而且是救援呼叫（含 `reserved`：`bootstrap.sh` 的保留入口）
/// 回 `Ok(true)`（照常回應那個 P，往返只准救援 op）；其餘回 `Err`。解析失敗的呼叫（不帶指令的用法除外）
/// 都不算救援呼叫，所以先報版本。
fn gate(
    compat: &compat::Compat,
    protocol: u32,
    parsed: &Result<args::Invocation, args::UsageError>,
    reserved: bool,
) -> Result<bool, compat::ProtocolError> {
    match compat.accept_protocol(protocol) {
        Ok(_) => Ok(false),
        Err(_) if reserved => Ok(true),
        Err(e) => match parsed {
            Ok(inv) if inv.is_rescue() => Ok(true),
            Err(args::UsageError::NoCommand) => Ok(true),
            _ => Err(e),
        },
    }
}

/// 介面版不合的診斷：P 低於 floor 是 VK0009；高於上限還沒有專屬代碼（G6），暫以 VK0056。
fn protocol_mismatch(e: &compat::ProtocolError, host_log: &str) -> Diagnostic {
    if e.given < e.floor {
        Diagnostic::new(&messages::VK0009)
            .arg("P_shell", e.given.to_string())
            .arg("vY", VERSION)
    } else {
        Diagnostic::new(&messages::VK0056)
            .arg("reason", format!("{e}; reason code pending (G6)"))
            .arg("path", host_log)
    }
}

/// 經啟動器的呼叫。
fn launched<O, E>(
    compat: &compat::Compat,
    args: &[OsString],
    mounts: &Mounts,
    stdin: &mut dyn BufRead,
    stdout: O,
    stderr: E,
) -> u8
where
    O: Write + Clone,
    E: Write + Clone,
{
    let internal = |stderr: E, reason: String, path: &str| {
        let mut diags = Diagnostics::new(stderr);
        let d = Diagnostic::new(&messages::VK0056)
            .arg("reason", reason)
            .arg("path", path);
        let _ = diags.emit(&d);
        diags.exit_code()
    };
    // 入口 argv 不合時連 header 都沒有，寫不了 done：只印診斷，由啟動器核對結束碼。
    let inv = match plan::Invocation::parse(args) {
        Ok(inv) => inv,
        Err(e) => return internal(stderr, e.to_string(), "none"),
    };
    let host_log = inv.host_root.join(&inv.run_log).display().to_string();
    // 介面版不在區間內也以呼叫方的 P 回應：hdr 與 done 屬救援路徑，跨介面版不變（[`gate`] 判要不要往下）。
    let Some(header) = plan::Header::new(inv.protocol, inv.run_id.clone()) else {
        let reason = format!("engine does not accept protocol {}", inv.protocol);
        return internal(stderr, reason, &host_log);
    };
    let mut channel = plan::Channel::new(&mounts.ctl, header);

    let code = match runlog::open_append(&mounts.root.join(&inv.run_log)) {
        Ok(file) => with_log(
            compat,
            &inv,
            mounts,
            &file,
            &host_log,
            &mut channel,
            stdin,
            stdout,
            stderr,
        ),
        Err(e) => {
            let mut diags = Diagnostics::new(stderr);
            let d = Diagnostic::new(&messages::VK0010)
                .arg("path", host_log.as_str())
                .arg("reason", e.to_string());
            let _ = diags.emit(&d);
            diags.exit_code()
        }
    };
    // 結束碼一定是 0–3（取自診斷的嚴重度）。done 寫不進去時啟動器會以 VK0056 收尾；這裡已無處可報。
    if let Some(exit) = plan::Exit::new(code) {
        let _ = channel.finish(exit);
    }
    code
}

/// 執行紀錄接好之後的部分。
#[allow(clippy::too_many_arguments)]
fn with_log<O, E>(
    compat: &compat::Compat,
    inv: &plan::Invocation,
    mounts: &Mounts,
    file: &File,
    host_log: &str,
    channel: &mut plan::Channel,
    stdin: &mut dyn BufRead,
    stdout: O,
    stderr: E,
) -> u8
where
    O: Write + Clone,
    E: Write + Clone,
{
    let header = runlog::Header {
        version: VERSION.to_owned(),
        component: runlog::Component::Engine,
        invocation_id: inv.run_id.as_str().to_owned(),
    };
    let mut log = runlog::Writer::new(file, header.clone());
    let mut diags = Diagnostics::with_sink(stderr.clone(), runlog::Writer::new(file, header));
    let mut out = Output::new(stdout.clone(), stderr.clone());
    if let Err(e) = log.write(&runlog::Event::EngineStarted) {
        let d = Diagnostic::new(&messages::VK0010)
            .arg("path", host_log)
            .arg("reason", e.to_string());
        let mut bare = Diagnostics::new(stderr);
        let _ = bare.emit(&d);
        return bare.exit_code();
    }

    let reserved = reserved_entry(&inv.rest);
    let parsed = args::parse(&inv.rest);
    let rescue_only = match gate(compat, inv.protocol, &parsed, reserved.is_some()) {
        Ok(rescue_only) => rescue_only,
        Err(e) => {
            let _ = diags.emit(&protocol_mismatch(&e, host_log));
            return finish_log(&mut out, &mut log, host_log, stderr, diags.exit_code());
        }
    };
    if rescue_only {
        channel.restrict_to_rescue();
    }
    let code = match (reserved, parsed) {
        (Some(mode), _) => {
            if at_install_root(inv, mounts, &mut diags) {
                run_shell_check(mode, inv, mounts, host_log, stdout, &mut diags)
            } else {
                2
            }
        }
        (None, Err(args::UsageError::NoCommand)) => {
            no_command(&mut out, &mut diags);
            2
        }
        (None, Err(e)) => {
            let mut d = Diagnostic::new(e.message());
            if let Some((name, value)) = e.placeholder() {
                d = d.arg(name, value);
            }
            let _ = diags.emit(&d);
            let _ = out.stderr_line(SHORT_USAGE);
            2
        }
        (None, Ok(args::Invocation::Help { name, engine })) => {
            let _ = out.help(help_for(name, engine));
            0
        }
        (None, Ok(args::Invocation::Run(command))) => {
            if at_install_root(inv, mounts, &mut diags) {
                dispatch(
                    &command, inv, mounts, host_log, channel, stdin, stdout, &stderr, &mut diags,
                    &mut log,
                )
            } else {
                2
            }
        }
    };
    let code = code.max(diags.exit_code());
    finish_log(&mut out, &mut log, host_log, stderr, code)
}

/// 04 執行位置：檢查使用者打指令時所在的目錄（啟動器已解掉 symlink，這裡只比字串）。不在安裝目錄印 VK0028、
/// 回 `false`。
fn at_install_root<W: Write, S: diagnostics::Sink>(
    inv: &plan::Invocation,
    mounts: &Mounts,
    diags: &mut Diagnostics<W, S>,
) -> bool {
    let in_root = layout::is_install_dir(&mounts.root).unwrap_or(false);
    if inv.host_cwd == inv.host_root && in_root {
        return true;
    }
    let d =
        Diagnostic::new(&messages::VK0028).arg("install_dir", inv.host_root.display().to_string());
    let _ = diags.emit(&d);
    false
}

/// `bootstrap.sh` 的只檢查與 `--repair`（`plan::entry` 的保留入口）。
fn run_shell_check<O, E>(
    mode: shell_check::Mode,
    inv: &plan::Invocation,
    mounts: &Mounts,
    host_log: &str,
    stdout: O,
    diags: &mut Diagnostics<E, runlog::Writer<&File>>,
) -> u8
where
    O: Write,
    E: Write,
{
    let release = match release(host_log, diags) {
        Ok(r) => r,
        Err(code) => return code,
    };
    let dir = layout::InstallDir::new(&mounts.root);
    let host_root = inv.host_root.display().to_string();
    let mut stdout = stdout;
    let mut env = shell_check::Env {
        dir: &dir,
        host_root: &host_root,
        run_log: host_log,
        written_by: VERSION,
        shell_templates: release.shell.as_ref(),
        stdout: &mut stdout,
        diags,
    };
    shell_check::run(mode, &mut env)
}

/// `-h`／`--help` 要印哪一份用法。`engine` 只有 `upgrade`、`dev`、`undev` 會是真（`args` 擋掉其餘）。
fn help_for(name: args::Name, engine: bool) -> output::Help {
    use args::Name;
    use output::Help;
    match (name, engine) {
        (Name::Add, _) => Help::Add,
        (Name::Upgrade, false) => Help::UpgradeTool,
        (Name::Upgrade, true) => Help::UpgradeEngine,
        (Name::Dev, false) => Help::DevTool,
        (Name::Dev, true) => Help::DevEngine,
        (Name::Undev, false) => Help::UndevTool,
        (Name::Undev, true) => Help::UndevEngine,
        (Name::Remove, _) => Help::Remove,
        (Name::Update, _) => Help::Update,
        (Name::Sync, _) => Help::Sync,
        (Name::Install, _) => Help::Install,
        (Name::Uninstall, _) => Help::Uninstall,
        (Name::Prune, _) => Help::Prune,
        (Name::Test, _) => Help::Test,
        (Name::TestDist, _) => Help::TestDist,
    }
}

/// flush 輸出、寫 `engine_finished`，回傳整次的結束碼。
fn finish_log<O, E>(
    out: &mut Output<O, E>,
    log: &mut runlog::Writer<&File>,
    host_log: &str,
    stderr: E,
    code: u8,
) -> u8
where
    O: Write,
    E: Write,
{
    let _ = out.flush();
    if let Err(e) = log.write(&runlog::Event::EngineFinished { exit_code: code }) {
        // 紀錄寫不進去：診斷照印（不再寫紀錄），整次以錯誤結束。
        let mut bare = Diagnostics::new(stderr);
        let d = Diagnostic::new(&messages::VK0010)
            .arg("path", host_log)
            .arg("reason", e.to_string());
        let _ = bare.emit(&d);
        return code.max(bare.exit_code());
    }
    code
}

/// 分派到指令。
#[allow(clippy::too_many_arguments)]
fn dispatch<O, E>(
    command: &args::Command,
    inv: &plan::Invocation,
    mounts: &Mounts,
    host_log: &str,
    channel: &mut plan::Channel,
    stdin: &mut dyn BufRead,
    stdout: O,
    stderr: &E,
    diags: &mut Diagnostics<E, runlog::Writer<&File>>,
    log: &mut runlog::Writer<&File>,
) -> u8
where
    O: Write + Clone,
    E: Write + Clone,
{
    match command {
        args::Command::Add {
            repo, tag, image, ..
        } => {
            let dir = layout::InstallDir::new(&mounts.root);
            let argv: Vec<String> = inv
                .rest
                .iter()
                .map(|a| a.to_string_lossy().into_owned())
                .collect();
            let host_root = inv.host_root.display().to_string();
            let mut stdout = stdout;
            let mut prompt = stderr.clone();
            let mut env = add::Env {
                dir: &dir,
                host_root: &host_root,
                run_log: host_log,
                inbox: &mounts.inbox,
                channel,
                poll: POLL,
                tty: inv.tty,
                argv: &argv,
                run_id: inv.run_id.as_str(),
                written_by: VERSION,
                stdin,
                stdout: &mut stdout,
                prompt: &mut prompt,
                diags,
                log,
            };
            let req = add::Request {
                repo,
                tag: *tag,
                image: image.as_deref(),
            };
            let code = add::run(&req, &mut env);
            let _ = stdout.flush();
            code
        }
        args::Command::Sync => {
            let release = match release(host_log, diags) {
                Ok(r) => r,
                Err(code) => return code,
            };
            let dir = layout::InstallDir::new(&mounts.root);
            let host_root = inv.host_root.display().to_string();
            let mut stdout = stdout;
            let mut env = sync::Env {
                dir: &dir,
                host_root: &host_root,
                run_log: host_log,
                inbox: &mounts.inbox,
                channel,
                poll: POLL,
                written_by: VERSION,
                shell_templates: release.shell.as_ref(),
                stdout: &mut stdout,
                diags,
                log,
            };
            let code = sync::run(&mut env);
            let _ = stdout.flush();
            code
        }
        args::Command::Prune => {
            let dir = layout::InstallDir::new(&mounts.root);
            let argv: Vec<String> = inv
                .rest
                .iter()
                .map(|a| a.to_string_lossy().into_owned())
                .collect();
            let host_root = inv.host_root.display().to_string();
            let mut stdout = stdout;
            let mut env = prune::Env {
                dir: &dir,
                host_root: &host_root,
                run_log: host_log,
                channel,
                poll: POLL,
                argv: &argv,
                run_id: inv.run_id.as_str(),
                written_by: VERSION,
                stdout: &mut stdout,
                diags,
                log,
            };
            let code = prune::run(&mut env);
            let _ = stdout.flush();
            code
        }
        args::Command::Update { repo, .. } => {
            let dir = layout::InstallDir::new(&mounts.root);
            let host_root = inv.host_root.display().to_string();
            let mut stdout = stdout;
            let mut plain = stderr.clone();
            let mut env = update::Env {
                dir: &dir,
                host_root: &host_root,
                run_log: host_log,
                stdout: &mut stdout,
                stderr: &mut plain,
                diags,
            };
            let req = update::Request {
                repo: repo.as_deref(),
            };
            let code = update::run(&req, &mut env);
            let _ = stdout.flush();
            code
        }
        args::Command::UpgradeTool { repo, tag, yes, .. } => {
            let dir = layout::InstallDir::new(&mounts.root);
            let argv: Vec<String> = inv
                .rest
                .iter()
                .map(|a| a.to_string_lossy().into_owned())
                .collect();
            let host_root = inv.host_root.display().to_string();
            let mut stdout = stdout;
            let mut prompt = stderr.clone();
            let mut env = upgrade::Env {
                dir: &dir,
                host_root: &host_root,
                run_log: host_log,
                inbox: &mounts.inbox,
                channel,
                poll: POLL,
                tty: inv.tty,
                argv: &argv,
                run_id: inv.run_id.as_str(),
                written_by: VERSION,
                stdin,
                stdout: &mut stdout,
                prompt: &mut prompt,
                diags,
                log,
            };
            let req = upgrade::Request {
                repo,
                tag: *tag,
                yes: *yes,
            };
            let code = upgrade::run(&req, &mut env);
            let _ = stdout.flush();
            code
        }
        args::Command::DevTool { repo, path } => run_dev(
            &dev::Request::DevTool { repo, path },
            inv,
            mounts,
            host_log,
            channel,
            stdout,
            diags,
            log,
        ),
        args::Command::DevEngine { image } => run_dev(
            &dev::Request::DevEngine { image },
            inv,
            mounts,
            host_log,
            channel,
            stdout,
            diags,
            log,
        ),
        args::Command::UndevTool { repo } => run_dev(
            &dev::Request::UndevTool { repo },
            inv,
            mounts,
            host_log,
            channel,
            stdout,
            diags,
            log,
        ),
        args::Command::UndevEngine => run_dev(
            &dev::Request::UndevEngine,
            inv,
            mounts,
            host_log,
            channel,
            stdout,
            diags,
            log,
        ),
        args::Command::Install { yes } => run_install(
            *yes, inv, mounts, host_log, stdin, stdout, stderr, diags, log,
        ),
        args::Command::Remove { repo } => run_remove(
            Some(repo),
            inv,
            mounts,
            host_log,
            stdin,
            stdout,
            stderr,
            diags,
            log,
        ),
        args::Command::Uninstall => run_remove(
            None, inv, mounts, host_log, stdin, stdout, stderr, diags, log,
        ),
        args::Command::UpgradeEngine { .. } => not_implemented("upgrade --engine", host_log, diags),
        args::Command::Test { path: None } => run_check(inv, mounts, host_log, stdout, diags),
        args::Command::Test { path: Some(_) } => {
            not_implemented("test with a path", host_log, diags)
        }
        args::Command::TestDist => not_implemented("test dist", host_log, diags),
    }
}

/// 還沒實作的指令（#372 N62）：是 VK 自己的缺，不是使用者打錯，以 VK0056 停下、不印用法。
fn not_implemented<E: Write>(
    what: &str,
    host_log: &str,
    diags: &mut Diagnostics<E, runlog::Writer<&File>>,
) -> u8 {
    let d = Diagnostic::new(&messages::VK0056)
        .arg("reason", format!("{what} is not implemented yet"))
        .arg("path", host_log);
    let _ = diags.emit(&d);
    2
}

/// `test` 不帶 path：完整安裝檢查（engine/check）。
fn run_check<O, E>(
    inv: &plan::Invocation,
    mounts: &Mounts,
    host_log: &str,
    stdout: O,
    diags: &mut Diagnostics<E, runlog::Writer<&File>>,
) -> u8
where
    O: Write,
    E: Write,
{
    let release = match release(host_log, diags) {
        Ok(r) => r,
        Err(code) => return code,
    };
    let dir = layout::InstallDir::new(&mounts.root);
    let host_root = inv.host_root.display().to_string();
    let mut stdout = stdout;
    let mut env = check::Env {
        dir: &dir,
        host_root: &host_root,
        run_log: host_log,
        written_by: VERSION,
        shell_templates: release.shell.as_ref(),
        stdout: &mut stdout,
        diags,
    };
    check::run(&mut env)
}

/// `dev` 與 `undev`（四種呼叫）。
#[allow(clippy::too_many_arguments)]
fn run_dev<O, E>(
    req: &dev::Request<'_>,
    inv: &plan::Invocation,
    mounts: &Mounts,
    host_log: &str,
    channel: &mut plan::Channel,
    stdout: O,
    diags: &mut Diagnostics<E, runlog::Writer<&File>>,
    log: &mut runlog::Writer<&File>,
) -> u8
where
    O: Write + Clone,
    E: Write + Clone,
{
    let dir = layout::InstallDir::new(&mounts.root);
    let argv: Vec<String> = inv
        .rest
        .iter()
        .map(|a| a.to_string_lossy().into_owned())
        .collect();
    let host_root = inv.host_root.display().to_string();
    let mut stdout = stdout;
    let mut env = dev::Env {
        dir: &dir,
        host_root: &host_root,
        inbox: &mounts.inbox,
        channel,
        poll: POLL,
        run_log: host_log,
        argv: &argv,
        run_id: inv.run_id.as_str(),
        written_by: VERSION,
        stdout: &mut stdout,
        diags,
        log,
    };
    let code = dev::run(req, &mut env);
    let _ = stdout.flush();
    code
}

/// 出貨輸入：設了 [`RELEASE_DIR_ENV`] 從那個目錄讀，否則讀 image 裡的。讀檔失敗印 VK0056、回 `Err(2)`；
/// 四檔不齊不算失敗（`shell` 是 `None`），由各指令報缺的項目。
fn release<E: Write>(
    host_log: &str,
    diags: &mut Diagnostics<E, runlog::Writer<&File>>,
) -> Result<install::Release, u8> {
    let (read, what) = match std::env::var_os(RELEASE_DIR_ENV) {
        Some(dir) => (
            install::Release::from_dir(Path::new(&dir)),
            RELEASE_DIR_ENV.to_owned(),
        ),
        None => (
            install::Release::shipped(),
            install::release::SHIPPED_DIR.to_owned(),
        ),
    };
    read.map_err(|e| {
        let d = Diagnostic::new(&messages::VK0056)
            .arg("reason", format!("{what}: {e}"))
            .arg("path", host_log);
        let _ = diags.emit(&d);
        2
    })
}

/// `install [-y]`。
#[allow(clippy::too_many_arguments)]
fn run_install<O, E>(
    yes: bool,
    inv: &plan::Invocation,
    mounts: &Mounts,
    host_log: &str,
    stdin: &mut dyn BufRead,
    stdout: O,
    stderr: &E,
    diags: &mut Diagnostics<E, runlog::Writer<&File>>,
    log: &mut runlog::Writer<&File>,
) -> u8
where
    O: Write + Clone,
    E: Write + Clone,
{
    let release = match release(host_log, diags) {
        Ok(r) => r,
        Err(code) => return code,
    };
    let dir = layout::InstallDir::new(&mounts.root);
    let argv: Vec<String> = inv
        .rest
        .iter()
        .map(|a| a.to_string_lossy().into_owned())
        .collect();
    let host_root = inv.host_root.display().to_string();
    let mut stdout = stdout;
    let mut prompt = stderr.clone();
    let mut env = install::Env {
        dir: &dir,
        inbox: &mounts.inbox,
        host_root: &host_root,
        run_log: host_log,
        tty: prompt::TtyState {
            stdin: inv.tty.stdin,
            stderr: inv.tty.stderr,
        },
        argv: &argv,
        run_id: inv.run_id.as_str(),
        written_by: VERSION,
        stdin,
        stdout: &mut stdout,
        prompt: &mut prompt,
        diags,
        log,
    };
    let req = install::Request {
        yes,
        release: &release,
    };
    let code = install::run(&req, &mut env);
    let _ = stdout.flush();
    code
}

/// `remove <repo>`（`repo` 是 `Some`）或 `uninstall`（`None`）。
#[allow(clippy::too_many_arguments)]
fn run_remove<O, E>(
    repo: Option<&str>,
    inv: &plan::Invocation,
    mounts: &Mounts,
    host_log: &str,
    stdin: &mut dyn BufRead,
    stdout: O,
    stderr: &E,
    diags: &mut Diagnostics<E, runlog::Writer<&File>>,
    log: &mut runlog::Writer<&File>,
) -> u8
where
    O: Write + Clone,
    E: Write + Clone,
{
    let dir = layout::InstallDir::new(&mounts.root);
    let argv: Vec<String> = inv
        .rest
        .iter()
        .map(|a| a.to_string_lossy().into_owned())
        .collect();
    let host_root = inv.host_root.display().to_string();
    let mut stdout = stdout;
    let mut prompt = stderr.clone();
    let mut env = remove::Env {
        dir: &dir,
        host_root: &host_root,
        run_log: host_log,
        tty: prompt::TtyState {
            stdin: inv.tty.stdin,
            stderr: inv.tty.stderr,
        },
        argv: &argv,
        run_id: inv.run_id.as_str(),
        written_by: VERSION,
        stdin,
        stdout: &mut stdout,
        prompt: &mut prompt,
        diags,
        log,
    };
    let code = match repo {
        Some(repo) => remove::remove(repo, &mut env),
        None => remove::uninstall(&mut env),
    };
    let _ = stdout.flush();
    code
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;
    use std::cell::RefCell;
    use std::io;
    use std::rc::Rc;

    /// stdout、stderr 各一份可共用的緩衝，讓輸出與診斷寫進同一條 stderr。
    #[derive(Clone, Default)]
    struct Buf(Rc<RefCell<Vec<u8>>>);

    impl Write for Buf {
        fn write(&mut self, data: &[u8]) -> io::Result<usize> {
            self.0.borrow_mut().extend_from_slice(data);
            Ok(data.len())
        }
        fn flush(&mut self) -> io::Result<()> {
            Ok(())
        }
    }

    impl Buf {
        fn text(&self) -> String {
            String::from_utf8(self.0.borrow().clone()).unwrap()
        }
    }

    fn call(args: &[&str]) -> (u8, String, String) {
        let (out, err) = (Buf::default(), Buf::default());
        let args: Vec<OsString> = args.iter().map(OsString::from).collect();
        let mounts = Mounts::with_prefix(Some(Path::new("/nonexistent")));
        let code = run(&args, &mounts, &mut io::empty(), out.clone(), err.clone());
        (code, out.text(), err.text())
    }

    #[test]
    fn no_command_prints_version_diagnostic_and_usage() {
        let (code, stdout, stderr) = call(&[]);
        assert_eq!(code, 2);
        assert_eq!(stdout, "");
        assert_eq!(
            stderr,
            format!(
                "vendor_kit {VERSION}\nvendor_kit: error[VK0024]: No command was specified.\nUsage: just vendor_kit <cmd> [arguments] [options]\n"
            )
        );
    }

    #[test]
    fn unregistered_command_is_rejected_without_stdout() {
        let (code, stdout, stderr) = call(&["foo"]);
        assert_eq!(code, 2);
        assert_eq!(stdout, "");
        assert!(stderr.starts_with("vendor_kit: error[VK0026]: "));
    }

    #[test]
    fn mounts_default_to_the_plan_mount_points() {
        let m = Mounts::with_prefix(None);
        assert_eq!(m.root, Path::new("/vk/root"));
        assert_eq!(m.ctl, Path::new("/vk/ctl"));
        assert_eq!(m.inbox, Path::new("/vk/in"));
        let m = Mounts::with_prefix(Some(Path::new("/t")));
        assert_eq!(m.root, Path::new("/t/vk/root"));
    }

    /// 一次經啟動器呼叫用的暫存掛載點：安裝目錄（有 `.vendor_kit/` 與空的執行紀錄）與 `ctl/`、`in/`。
    struct Scratch(PathBuf);

    impl Scratch {
        fn new(name: &str) -> Scratch {
            let base = std::env::temp_dir().join(format!("vk-cli-{}-{name}", std::process::id()));
            let _ = std::fs::remove_dir_all(&base);
            for d in ["vk/root/.vendor_kit/log", "vk/ctl", "vk/in"] {
                std::fs::create_dir_all(base.join(d)).unwrap();
            }
            std::fs::write(base.join("vk/root").join(RUN_LOG), "").unwrap();
            Scratch(base)
        }

        fn mounts(&self) -> Mounts {
            Mounts::with_prefix(Some(&self.0))
        }

        fn done(&self) -> String {
            std::fs::read_to_string(self.0.join("vk/ctl/done")).unwrap()
        }

        /// `.vendor_kit/` 底下除了執行紀錄以外的路徑。
        fn written(&self) -> Vec<PathBuf> {
            let vk = self.0.join("vk/root/.vendor_kit");
            let mut out = Vec::new();
            for e in std::fs::read_dir(&vk).unwrap() {
                let p = e.unwrap().path();
                if p != vk.join("log") {
                    out.push(p);
                }
            }
            out
        }
    }

    impl Drop for Scratch {
        fn drop(&mut self) {
            let _ = std::fs::remove_dir_all(&self.0);
        }
    }

    const RUN_LOG: &str = ".vendor_kit/log/r1.jsonl";

    /// 只接受 P=2、3 的引擎（floor 高於 1，用來測舊薄殼）。
    const NEWER: compat::Compat = compat::Compat {
        floor_protocol: 2,
        current_protocol: 3,
        max_schema: 1,
    };

    /// 經啟動器跑一次：P 是 `protocol`，`rest` 是 `--` 之後的 recipe 與參數。
    fn launch(
        s: &Scratch,
        compat: &compat::Compat,
        protocol: u32,
        rest: &[&str],
    ) -> (u8, String, String) {
        let host_root = "/srv/proj";
        let p = protocol.to_string();
        let mut args: Vec<&str> = vec![
            "--protocol",
            &p,
            "--run-id",
            "r1",
            "--host-root",
            host_root,
            "--host-cwd",
            host_root,
            "--run-log",
            RUN_LOG,
            "--tty",
            "000",
            "--no-color",
            "1",
            "--",
        ];
        args.extend_from_slice(rest);
        let args: Vec<OsString> = args.iter().map(OsString::from).collect();
        let (out, err) = (Buf::default(), Buf::default());
        let code = run_with(
            compat,
            &args,
            &s.mounts(),
            &mut io::empty(),
            out.clone(),
            err.clone(),
        );
        (code, out.text(), err.text())
    }

    #[test]
    fn gate_lets_only_rescue_calls_through_outside_the_range() {
        let p = |a: &[&str]| args::parse(a);
        // 區間內：一律照常往下，不限定救援 op。
        for a in [&["prune"][..], &["upgrade", "--engine", "--bogus"], &[]] {
            assert_eq!(gate(&NEWER, 2, &p(a), false), Ok(false), "{a:?}");
            assert_eq!(gate(&NEWER, 3, &p(a), false), Ok(false), "{a:?}");
        }
        // 區間外（低於 floor 與高於上限）：救援呼叫照常、限定救援 op；其餘先報版本。
        for protocol in [1, 4] {
            for a in [
                &[][..],
                &["install"],
                &["install", "-y"],
                &["sync"],
                &["upgrade", "--engine"],
                &["upgrade", "--engine=v2.0.0", "-y"],
                &["install", "-h"],
                &["sync", "--help"],
                &["upgrade", "--engine", "-h"],
            ] {
                assert_eq!(
                    gate(&NEWER, protocol, &p(a), false),
                    Ok(true),
                    "{protocol} {a:?}"
                );
            }
            for a in [
                &["prune"][..],
                &["add", "lint"],
                &["add", "-h"],
                &["upgrade", "lint"],
                &["upgrade", "--engine", "--bogus"],
                &["install", "--bogus"],
                &["sync", "extra"],
                &["frobnicate"],
            ] {
                assert!(
                    gate(&NEWER, protocol, &p(a), false).is_err(),
                    "{protocol} {a:?}"
                );
            }
        }
    }

    #[test]
    fn reserved_entries_are_recognized_only_alone() {
        let os = |a: &[&str]| a.iter().map(OsString::from).collect::<Vec<_>>();
        assert_eq!(
            reserved_entry(&os(&[plan::entry::SHELL_CHECK])),
            Some(shell_check::Mode::Check)
        );
        assert_eq!(
            reserved_entry(&os(&[plan::entry::SHELL_REPAIR])),
            Some(shell_check::Mode::Repair)
        );
        for a in [
            &[][..],
            &["@shell-check", "-y"],
            &["@shell-repair", "--"],
            &["sync", "@shell-check"],
            &["--", "@shell-check"],
            &["@shell-Check"],
        ] {
            assert_eq!(reserved_entry(&os(a)), None, "{a:?}");
        }
        // 介面版不在區間內也照常執行（救援路徑）。
        let parsed = args::parse(&[plan::entry::SHELL_CHECK]);
        for protocol in [1, 4] {
            assert_eq!(gate(&NEWER, protocol, &parsed, true), Ok(true));
        }
        assert_eq!(gate(&NEWER, 2, &parsed, true), Ok(false));
    }

    #[test]
    fn reserved_entry_outside_the_range_answers_with_the_callers_protocol() {
        // 單元測試沒有出貨的薄殼模板：照常往下到 shell_check，以 VK0056 停下，不先報版本。
        for rest in [plan::entry::SHELL_CHECK, plan::entry::SHELL_REPAIR] {
            let s = Scratch::new("old-shell-check");
            let (code, stdout, stderr) = launch(&s, &NEWER, 1, &[rest]);
            assert_eq!(code, 2, "{rest}");
            assert_eq!(stdout, "");
            assert!(
                stderr.starts_with("vendor_kit: error[VK0056]: Internal vendor_kit error: checking the shell without the shell templates"),
                "{stderr}"
            );
            assert!(s.written().is_empty(), "{:?}", s.written());
            assert_eq!(s.done(), "vk-resolve/1 r1 done 2\n");
        }
    }

    #[test]
    fn reserved_entry_outside_the_install_dir_is_vk0028() {
        let s = Scratch::new("shell-check-cwd");
        let host_root = "/srv/proj";
        let args: Vec<OsString> = [
            "--protocol",
            "1",
            "--run-id",
            "r1",
            "--host-root",
            host_root,
            "--host-cwd",
            "/srv/proj/sub",
            "--run-log",
            RUN_LOG,
            "--tty",
            "000",
            "--no-color",
            "1",
            "--",
            plan::entry::SHELL_REPAIR,
        ]
        .iter()
        .map(OsString::from)
        .collect();
        let (out, err) = (Buf::default(), Buf::default());
        let code = run(
            &args,
            &s.mounts(),
            &mut io::empty(),
            out.clone(),
            err.clone(),
        );
        assert_eq!(code, 2);
        assert!(
            err.text().starts_with("vendor_kit: error[VK0028]: "),
            "{}",
            err.text()
        );
        assert!(s.written().is_empty(), "{:?}", s.written());
    }

    #[test]
    fn rescue_candidate_with_a_usage_error_reports_the_version_first() {
        // 版本合：用法錯誤，回 2。
        let s = Scratch::new("bogus-ok");
        let (code, stdout, stderr) = launch(&s, &NEWER, 2, &["upgrade", "--engine", "--bogus"]);
        assert_eq!(code, 2);
        assert_eq!(stdout, "");
        assert!(
            stderr.starts_with("vendor_kit: error[VK0026]: "),
            "{stderr}"
        );
        assert_eq!(s.done(), "vk-resolve/2 r1 done 2\n");
        // 版本不合（舊薄殼）：先報版本，回 3，不報用法錯誤。
        let s = Scratch::new("bogus-old");
        let (code, stdout, stderr) = launch(&s, &NEWER, 1, &["upgrade", "--engine", "--bogus"]);
        assert_eq!(code, 3);
        assert_eq!(stdout, "");
        assert_eq!(
            stderr,
            format!(
                "vendor_kit: fatal[VK0009]: Shell interface version 1 is older than required for general recipes in engine {VERSION}. Run first: just vendor_kit upgrade --engine\n"
            )
        );
        assert_eq!(s.done(), "vk-resolve/1 r1 done 3\n");
    }

    #[test]
    fn general_recipe_outside_the_range_stops_before_any_write() {
        let s = Scratch::new("old-prune");
        let (code, _, stderr) = launch(&s, &NEWER, 1, &["prune"]);
        assert_eq!(code, 3);
        assert!(
            stderr.starts_with("vendor_kit: fatal[VK0009]: "),
            "{stderr}"
        );
        assert!(s.written().is_empty(), "{:?}", s.written());
        assert_eq!(s.done(), "vk-resolve/1 r1 done 3\n");
        // 薄殼比引擎新：還沒有專屬代碼（G6），暫以 VK0056。
        let s = Scratch::new("new-prune");
        let (code, _, stderr) = launch(&s, &NEWER, 4, &["prune"]);
        assert_eq!(code, 2);
        assert!(
            stderr.starts_with("vendor_kit: error[VK0056]: Internal vendor_kit error: interface version 4 is outside the supported range [2, 3]; reason code pending (G6)."),
            "{stderr}"
        );
        assert!(s.written().is_empty(), "{:?}", s.written());
        assert_eq!(s.done(), "vk-resolve/4 r1 done 2\n");
    }

    #[test]
    fn rescue_calls_outside_the_range_answer_with_the_callers_protocol() {
        // 不帶指令的用法照常。
        let s = Scratch::new("old-usage");
        let (code, _, stderr) = launch(&s, &NEWER, 1, &[]);
        assert_eq!(code, 2);
        assert!(stderr.contains("error[VK0024]"), "{stderr}");
        assert_eq!(s.done(), "vk-resolve/1 r1 done 2\n");
        // 救援呼叫的 -h 照常印用法，不報版本。
        for (rest, help) in [
            (&["sync", "-h"][..], output::Help::Sync),
            (&["install", "--help"], output::Help::Install),
            (&["upgrade", "--engine", "-h"], output::Help::UpgradeEngine),
        ] {
            let s = Scratch::new("old-help");
            let (code, stdout, stderr) = launch(&s, &NEWER, 1, rest);
            assert_eq!(code, 0, "{rest:?}");
            assert_eq!(stdout, help.text(), "{rest:?}");
            assert_eq!(stderr, "", "{rest:?}");
            assert_eq!(s.done(), "vk-resolve/1 r1 done 0\n");
        }
    }

    #[test]
    fn non_rescue_help_outside_the_range_reports_the_version() {
        let s = Scratch::new("old-add-help");
        let (code, stdout, stderr) = launch(&s, &NEWER, 1, &["add", "-h"]);
        assert_eq!(code, 3);
        assert_eq!(stdout, "");
        assert!(
            stderr.starts_with("vendor_kit: fatal[VK0009]: "),
            "{stderr}"
        );
        assert_eq!(s.done(), "vk-resolve/1 r1 done 3\n");
    }

    /// 用法裡列的每個選項（`-h` 除外），`args` 這一版都收：help 是唯一來源，不能列還沒有的選項。
    #[test]
    fn every_option_in_the_help_is_accepted() {
        use output::Help;
        let base: [(Help, &[&str]); 15] = [
            (Help::Add, &["add", "lint"]),
            (Help::UpgradeTool, &["upgrade", "lint"]),
            (Help::UpgradeEngine, &["upgrade", "--engine"]),
            (Help::DevTool, &["dev", "lint"]),
            (Help::DevEngine, &["dev", "--engine"]),
            (Help::UndevTool, &["undev", "lint"]),
            (Help::UndevEngine, &["undev", "--engine"]),
            (Help::Remove, &["remove", "lint"]),
            (Help::Update, &["update"]),
            (Help::Sync, &["sync"]),
            (Help::Install, &["install"]),
            (Help::Uninstall, &["uninstall"]),
            (Help::Prune, &["prune"]),
            (Help::Test, &["test"]),
            (Help::TestDist, &["test", "dist"]),
        ];
        let mut checked = 0;
        for (help, base) in base {
            for line in help
                .text()
                .lines()
                .filter(|l| l.starts_with("  ") && l.trim_start().starts_with('-'))
            {
                let spec = line.trim_start().split("  ").next().unwrap();
                let takes_value = spec.contains('<');
                for opt in spec.split(", ").map(|f| f.split(' ').next().unwrap()) {
                    if opt == "-h" || opt == "--help" {
                        continue;
                    }
                    let mut argv: Vec<&str> = base.to_vec();
                    argv.push(opt);
                    if takes_value {
                        argv.push("x");
                    }
                    assert!(
                        matches!(args::parse(&argv), Ok(args::Invocation::Run(_))),
                        "{help:?}: {argv:?} -> {:?}",
                        args::parse(&argv)
                    );
                    checked += 1;
                }
            }
        }
        // -i／--image 兩處、-y／--yes 三處、--registry-token-file 三處、-p／--path 一處。
        assert_eq!(checked, 4 + 6 + 3 + 2);
    }

    #[test]
    fn help_prints_the_usage_on_stdout_and_exits_0() {
        for (rest, help) in [
            (&["add", "-h"][..], output::Help::Add),
            (&["upgrade", "--help"], output::Help::UpgradeTool),
            (&["upgrade", "--engine", "-h"], output::Help::UpgradeEngine),
            (&["dev", "-h"], output::Help::DevTool),
            (&["dev", "--engine", "-h"], output::Help::DevEngine),
            (&["undev", "-h"], output::Help::UndevTool),
            (&["undev", "--engine", "-h"], output::Help::UndevEngine),
            (&["remove", "-h"], output::Help::Remove),
            (&["update", "-h"], output::Help::Update),
            (&["sync", "-h"], output::Help::Sync),
            (&["install", "-h"], output::Help::Install),
            (&["uninstall", "-h"], output::Help::Uninstall),
            (&["prune", "-h"], output::Help::Prune),
            (&["test", "-h"], output::Help::Test),
            (&["test", "dist", "-h"], output::Help::TestDist),
        ] {
            let s = Scratch::new("help");
            let (code, stdout, stderr) = launch(&s, &compat::THIS, 1, rest);
            assert_eq!(code, 0, "{rest:?}");
            assert_eq!(stdout, help.text(), "{rest:?}");
            assert_eq!(stderr, "", "{rest:?}");
            assert_eq!(s.done(), "vk-resolve/1 r1 done 0\n");
            assert!(s.written().is_empty(), "{:?}", s.written());
        }
    }

    #[test]
    fn unimplemented_commands_are_internal_errors_not_usage_errors() {
        for (rest, what) in [
            (&["upgrade", "--engine"][..], "upgrade --engine"),
            (&["test", "test/unit"], "test with a path"),
            (&["test", "dist"], "test dist"),
        ] {
            let s = Scratch::new("unimplemented");
            let (code, stdout, stderr) = launch(&s, &compat::THIS, 1, rest);
            assert_eq!(code, 2, "{rest:?}");
            assert_eq!(stdout, "");
            assert!(
                stderr.starts_with(&format!(
                    "vendor_kit: error[VK0056]: Internal vendor_kit error: {what} is not implemented yet."
                )),
                "{stderr}"
            );
            assert!(!stderr.contains(SHORT_USAGE), "{stderr}");
        }
    }

    #[test]
    fn launched_with_bad_argv_is_an_internal_error() {
        let (code, stdout, stderr) = call(&["--protocol", "1", "--run-id"]);
        assert_eq!(code, 2);
        assert_eq!(stdout, "");
        assert!(
            stderr.starts_with("vendor_kit: error[VK0056]: "),
            "{stderr}"
        );
    }
}
