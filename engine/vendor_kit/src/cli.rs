//! 參數分派。
//!
//! 兩種呼叫：
//!
//! - 經啟動器（第一個參數是 `--protocol`）：照 `plan` 的入口 argv 取上下文，接上執行紀錄與往返通道，
//!   判用法與安裝目錄，再分派到指令；結束前寫 `engine_finished` 與 `done`。
//! - 直接呼叫（其他）：沒有執行紀錄與往返，只處理不帶指令的用法；其餘以 VK0026 回報，待決議（#457）。
//!
//! 目前只實作 `add`、`sync`、`install`、`remove`、`uninstall`、`update`、`upgrade <repo>`、`dev`、`undev` 與 `prune`（`upgrade --engine` 還沒有）。04 說明與用法錯誤：不認得的名稱由 just 擋下、到不了引擎；其他還沒實作的指令
//! 暫以 VK0026（不認得的參數）回報並附用法，`-h`／`--help` 的用法文字還沒定，以 VK0056 停下。

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

/// 測試用：設了這個環境變數，`install` 的出貨輸入改從這個目錄讀（`install::Release::from_dir`）。
/// 這一版引擎沒有出貨那些輸入（`install::Release::shipped`），正式執行時一定不設（啟動器起引擎容器時
/// 不帶任何環境變數）；e2e 用它驗 `install` 其餘的流程。
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
    if args.first().map(OsString::as_os_str) == Some(plan::argv::PROTOCOL.as_ref()) {
        return launched(args, mounts, stdin, stdout, stderr);
    }
    let mut out = Output::new(stdout, stderr.clone());
    let mut diags = Diagnostics::new(stderr);
    let Some(first) = args.first() else {
        no_command(&mut out, &mut diags);
        return diags.exit_code();
    };
    // 直接呼叫引擎時沒有契約定的診斷，暫以 VK0026（不認得的參數）回報並附用法，待決議（#457）。
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

/// 經啟動器的呼叫。
fn launched<O, E>(
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
    let protocol = compat::THIS.accept_protocol(inv.protocol);
    let header = protocol
        .ok()
        .and_then(|p| plan::Header::new(p, inv.run_id.clone()));
    let Some(header) = header else {
        let reason = format!("engine does not accept protocol {}", inv.protocol);
        return internal(stderr, reason, &host_log);
    };
    let mut channel = plan::Channel::new(&mounts.ctl, header);

    let code = match runlog::open_append(&mounts.root.join(&inv.run_log)) {
        Ok(file) => with_log(
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

    let code = match args::parse(&inv.rest) {
        Err(args::UsageError::NoCommand) => {
            no_command(&mut out, &mut diags);
            2
        }
        Err(e) => {
            let mut d = Diagnostic::new(e.message());
            if let Some((name, value)) = e.placeholder() {
                d = d.arg(name, value);
            }
            let _ = diags.emit(&d);
            let _ = out.stderr_line(SHORT_USAGE);
            2
        }
        Ok(args::Invocation::Help { name, .. }) => {
            let d = Diagnostic::new(&messages::VK0056)
                .arg(
                    "reason",
                    format!("help text for {name} is not specified yet"),
                )
                .arg("path", host_log);
            let _ = diags.emit(&d);
            2
        }
        Ok(args::Invocation::Run(command)) => {
            let in_root = layout::is_install_dir(&mounts.root).unwrap_or(false);
            if inv.host_cwd != inv.host_root || !in_root {
                // 04 執行位置：檢查使用者打指令時所在的目錄（啟動器已解掉 symlink，這裡只比字串）。
                let d = Diagnostic::new(&messages::VK0028)
                    .arg("install_dir", inv.host_root.display().to_string());
                let _ = diags.emit(&d);
                2
            } else {
                dispatch(
                    &command, inv, mounts, host_log, channel, stdin, stdout, &stderr, &mut diags,
                    &mut log,
                )
            }
        }
    };
    let _ = out.flush();
    let code = code.max(diags.exit_code());
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
            let dir = layout::InstallDir::new(&mounts.root);
            let argv: Vec<String> = inv
                .rest
                .iter()
                .map(|a| a.to_string_lossy().into_owned())
                .collect();
            let host_root = inv.host_root.display().to_string();
            let mut stdout = stdout;
            let mut env = sync::Env {
                dir: &dir,
                host_root: &host_root,
                run_log: host_log,
                inbox: &mounts.inbox,
                channel,
                poll: POLL,
                argv: &argv,
                run_id: inv.run_id.as_str(),
                written_by: VERSION,
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
            stdout,
            diags,
            log,
        ),
        args::Command::DevEngine { image } => run_dev(
            &dev::Request::DevEngine { image },
            inv,
            mounts,
            host_log,
            stdout,
            diags,
            log,
        ),
        args::Command::UndevTool { repo } => run_dev(
            &dev::Request::UndevTool { repo },
            inv,
            mounts,
            host_log,
            stdout,
            diags,
            log,
        ),
        args::Command::UndevEngine => run_dev(
            &dev::Request::UndevEngine,
            inv,
            mounts,
            host_log,
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
        _ => {
            let name = inv
                .rest
                .first()
                .map(|a| a.to_string_lossy().into_owned())
                .unwrap_or_default();
            let d = Diagnostic::new(&messages::VK0026).arg("value", name);
            let _ = diags.emit(&d);
            let mut out = Output::new(stdout, stderr.clone());
            let _ = out.stderr_line(SHORT_USAGE);
            2
        }
    }
}

/// `dev` 與 `undev`（四種呼叫）。
fn run_dev<O, E>(
    req: &dev::Request<'_>,
    inv: &plan::Invocation,
    mounts: &Mounts,
    host_log: &str,
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
    let release = match std::env::var_os(RELEASE_DIR_ENV) {
        Some(dir) => match install::Release::from_dir(Path::new(&dir)) {
            Ok(r) => r,
            Err(e) => {
                let d = Diagnostic::new(&messages::VK0056)
                    .arg("reason", format!("{RELEASE_DIR_ENV}: {e}"))
                    .arg("path", host_log);
                let _ = diags.emit(&d);
                return 2;
            }
        },
        None => install::Release::shipped(),
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
