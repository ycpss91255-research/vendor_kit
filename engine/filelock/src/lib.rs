//! 安裝目錄的檔案鎖（04 鎖與逾時）。
//!
//! - 鎖的是安裝目錄本身：以 `O_DIRECTORY` 開目錄後 `flock(2)`，不用 `lockf`／`fcntl` 記錄鎖。
//!   `flock` 跟著開檔描述走，同一個 process 開兩次也互斥；fd 帶 `O_CLOEXEC`，子程序不會把鎖帶走。
//! - 寫入持排他鎖（[`Mode::Exclusive`]），讀取持共享鎖（[`Mode::Shared`]）。鎖在 [`Lock`] 被丟掉時放開。
//! - 等鎖期限用 `config` crate 讀出的 [`LockTimeout`]（`lock_timeout_seconds`）：`-1` 一直等、
//!   `0` 不等、正數最多等那麼多秒。`flock` 本身沒有逾時，有期限時以不阻塞的嘗試輪詢到期限為止。
//!   首次導入沒有設定可讀，固定等 [`FIRST_INSTALL_TIMEOUT`]。
//! - 期限內取不到鎖回 [`LockError::Timeout`]（VK0042）。
//! - `lock_enabled = false` 時不取鎖，[`Lock::warning`] 回 VK0060，呼叫端每次執行都要印。
//!
//! 這裡不印診斷；要怎麼印由呼叫端經 `diagnostics` 決定，`<install_dir>` 也由呼叫端填。

use std::fmt;
use std::fs::{File, OpenOptions};
use std::io;
use std::os::unix::fs::OpenOptionsExt;
use std::path::{Path, PathBuf};
use std::thread;
use std::time::{Duration, Instant};

pub use config::LockTimeout;
use config::{Config, DEFAULT_LOCK_TIMEOUT_SECONDS};
use layout::InstallDir;
use messages::Message;
use nix::errno::Errno;
use nix::fcntl::{Flock, FlockArg, OFlag};

/// 首次導入的等鎖期限：固定 60 秒，不讀設定（04 鎖與逾時）。
pub const FIRST_INSTALL_TIMEOUT: LockTimeout = LockTimeout::Seconds(DEFAULT_LOCK_TIMEOUT_SECONDS);

/// 有期限時兩次嘗試之間的間隔。
const POLL_INTERVAL: Duration = Duration::from_millis(50);

/// 鎖的種類。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Mode {
    /// 讀取：可以跟其他共享鎖同時持有。
    Shared,
    /// 寫入：同時只有一個，也擋共享鎖。
    Exclusive,
}

impl Mode {
    fn arg(self, wait: bool) -> FlockArg {
        match (self, wait) {
            (Mode::Shared, true) => FlockArg::LockShared,
            (Mode::Shared, false) => FlockArg::LockSharedNonblock,
            (Mode::Exclusive, true) => FlockArg::LockExclusive,
            (Mode::Exclusive, false) => FlockArg::LockExclusiveNonblock,
        }
    }

    /// 訊息與除錯用的名字。
    pub const fn as_str(self) -> &'static str {
        match self {
            Mode::Shared => "shared",
            Mode::Exclusive => "exclusive",
        }
    }
}

impl fmt::Display for Mode {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

/// 一把取得的鎖，或設定關掉鎖時的空鎖。丟掉時放開。
#[derive(Debug)]
pub struct Lock {
    mode: Mode,
    /// `lock_enabled = false` 時是 `None`。
    held: Option<Flock<File>>,
}

impl Lock {
    /// 依設定取安裝目錄的鎖：`lock_enabled = false` 時不取鎖、回空鎖；否則照 `lock_timeout_seconds` 等。
    pub fn acquire(dir: &InstallDir, mode: Mode, config: &Config) -> Result<Lock, LockError> {
        if !config.lock_enabled() {
            return Ok(Lock { mode, held: None });
        }
        Lock::acquire_with(dir, mode, config.lock_timeout())
    }

    /// 不看設定，以指定期限取安裝目錄的鎖；首次導入用 [`FIRST_INSTALL_TIMEOUT`]。
    pub fn acquire_with(
        dir: &InstallDir,
        mode: Mode,
        timeout: LockTimeout,
    ) -> Result<Lock, LockError> {
        let root = dir.root();
        let file = open_dir(root)?;
        let held = lock(file, mode, timeout).map_err(|e| match e {
            Failure::Busy => LockError::Timeout {
                dir: root.to_path_buf(),
                mode,
                timeout,
            },
            Failure::Errno(errno) => LockError::Io {
                path: root.to_path_buf(),
                op: Op::Lock,
                source: io::Error::from(errno),
            },
        })?;
        Ok(Lock {
            mode,
            held: Some(held),
        })
    }

    /// 鎖的種類。
    pub fn mode(&self) -> Mode {
        self.mode
    }

    /// 是否真的持有鎖；設定關掉鎖時是 `false`。
    pub fn is_held(&self) -> bool {
        self.held.is_some()
    }

    /// 鎖被設定關掉時每次執行都要印的警告（VK0060）；有持鎖時是 `None`。
    pub fn warning(&self) -> Option<&'static Message> {
        self.held.is_none().then_some(&messages::VK0060)
    }
}

/// 以唯讀、`O_DIRECTORY` 開目錄；不是目錄就失敗，不會誤鎖到一般檔。std 預設帶 `O_CLOEXEC`。
fn open_dir(root: &Path) -> Result<File, LockError> {
    OpenOptions::new()
        .read(true)
        .custom_flags(OFlag::O_DIRECTORY.bits())
        .open(root)
        .map_err(|source| LockError::Io {
            path: root.to_path_buf(),
            op: Op::Open,
            source,
        })
}

enum Failure {
    /// 期限內一直被別人持有。
    Busy,
    /// 其他錯誤，例如檔案系統不支援檔案鎖。
    Errno(Errno),
}

fn lock(file: File, mode: Mode, timeout: LockTimeout) -> Result<Flock<File>, Failure> {
    let deadline = match timeout {
        LockTimeout::Forever => return lock_blocking(file, mode),
        LockTimeout::NoWait => Some(Instant::now()),
        // 大到加不上去的期限跟一直等一樣。
        LockTimeout::Seconds(n) => match Instant::now().checked_add(Duration::from_secs(n)) {
            Some(d) => Some(d),
            None => return lock_blocking(file, mode),
        },
    };
    let mut file = file;
    loop {
        match Flock::lock(file, mode.arg(false)) {
            Ok(held) => return Ok(held),
            Err((f, Errno::EINTR)) => file = f,
            Err((f, Errno::EWOULDBLOCK)) => {
                let now = Instant::now();
                let left = match deadline {
                    Some(d) if d > now => d - now,
                    _ => return Err(Failure::Busy),
                };
                thread::sleep(left.min(POLL_INTERVAL));
                file = f;
            }
            Err((_, errno)) => return Err(Failure::Errno(errno)),
        }
    }
}

fn lock_blocking(file: File, mode: Mode) -> Result<Flock<File>, Failure> {
    let mut file = file;
    loop {
        match Flock::lock(file, mode.arg(true)) {
            Ok(held) => return Ok(held),
            Err((f, Errno::EINTR)) => file = f,
            Err((_, errno)) => return Err(Failure::Errno(errno)),
        }
    }
}

/// 失敗時正在做的動作。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Op {
    /// 開安裝目錄。
    Open,
    /// `flock(2)`。
    Lock,
}

/// 取鎖失敗。
#[derive(Debug)]
pub enum LockError {
    /// 等鎖期限內取不到鎖（VK0042）。`dir` 填 `<install_dir>`。
    Timeout {
        dir: PathBuf,
        mode: Mode,
        timeout: LockTimeout,
    },
    /// 開不了目錄，或 `flock` 回了等不到以外的錯（例如檔案系統不支援檔案鎖）。
    /// 訊息表沒有對應代碼，由呼叫端當內部錯誤處理。
    Io {
        path: PathBuf,
        op: Op,
        source: io::Error,
    },
}

impl LockError {
    /// 對應的訊息表條目；`Io` 沒有代碼，回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            LockError::Timeout { .. } => Some(&messages::VK0042),
            LockError::Io { .. } => None,
        }
    }
}

impl fmt::Display for LockError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            LockError::Timeout { dir, mode, timeout } => {
                let wait = match timeout {
                    LockTimeout::NoWait => "without waiting".to_owned(),
                    LockTimeout::Forever => "while waiting forever".to_owned(),
                    LockTimeout::Seconds(n) => format!("within {n} s"),
                };
                write!(
                    f,
                    "could not acquire the {mode} lock on {} {wait}",
                    dir.display()
                )
            }
            LockError::Io { path, op, source } => {
                let op = match op {
                    Op::Open => "open",
                    Op::Lock => "lock",
                };
                write!(f, "{op} {}: {source}", path.display())
            }
        }
    }
}

impl std::error::Error for LockError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            LockError::Timeout { .. } => None,
            LockError::Io { source, .. } => Some(source),
        }
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;
    use std::io::{BufRead, BufReader};
    use std::process::{Child, ChildStdout, Command, Stdio};
    use std::sync::mpsc;

    /// 設了這個環境變數，[`hold_lock_for_parent`] 才當持鎖 helper；值是 `<mode>:<dir>`。
    const HELPER_ENV: &str = "FILELOCK_TEST_HOLD";
    /// helper 取到鎖後印的一行。
    const HELD_MARKER: &str = "FILELOCK_TEST_HELD";

    /// 另一個 process：重跑這支測試執行檔，只跑 [`hold_lock_for_parent`]。
    /// 取到鎖才回來；丟掉或 [`Holder::release`] 時放鎖並結束 helper。
    struct Holder {
        child: Option<Child>,
        /// 讀到標記後還要留著讀：關掉的話 helper 之後印字會寫進斷掉的 pipe 而失敗。
        stdout: BufReader<ChildStdout>,
    }

    impl Holder {
        fn spawn(dir: &Path, mode: Mode) -> Holder {
            let exe = std::env::current_exe().unwrap();
            let mut child = Command::new(exe)
                .args([
                    "tests::hold_lock_for_parent",
                    "--exact",
                    "--nocapture",
                    "--test-threads=1",
                ])
                .env(HELPER_ENV, format!("{}:{}", mode.as_str(), dir.display()))
                .stdin(Stdio::piped())
                .stdout(Stdio::piped())
                .stderr(Stdio::inherit())
                .spawn()
                .unwrap();
            let stdout = BufReader::new(child.stdout.take().unwrap());
            let mut holder = Holder {
                child: Some(child),
                stdout,
            };
            // libtest 會在同一條 stdout 印自己的字，所以只找含標記的行。
            let held = (&mut holder.stdout)
                .lines()
                .map_while(Result::ok)
                .any(|line| line.contains(HELD_MARKER));
            if !held {
                holder.kill();
                panic!("helper exited before holding the {mode} lock");
            }
            holder
        }

        /// 關掉 helper 的 stdin，等它放鎖結束。
        fn release(mut self) {
            let mut child = self.child.take().unwrap();
            drop(child.stdin.take());
            let mut rest = Vec::new();
            io::Read::read_to_end(&mut self.stdout, &mut rest).unwrap();
            let status = child.wait().unwrap();
            assert!(status.success(), "helper failed: {status}");
        }

        fn kill(&mut self) {
            if let Some(mut child) = self.child.take() {
                let _ = child.kill();
                let _ = child.wait();
            }
        }
    }

    impl Drop for Holder {
        fn drop(&mut self) {
            self.kill();
        }
    }

    /// 持鎖 helper：平常直接通過；由 [`Holder::spawn`] 叫起時取鎖、印標記，等 stdin 關掉才放。
    #[test]
    fn hold_lock_for_parent() {
        let Ok(spec) = std::env::var(HELPER_ENV) else {
            return;
        };
        let (mode, dir) = spec.split_once(':').unwrap();
        let mode = match mode {
            "shared" => Mode::Shared,
            "exclusive" => Mode::Exclusive,
            other => panic!("unknown mode {other}"),
        };
        let lock = Lock::acquire_with(&InstallDir::new(dir), mode, LockTimeout::NoWait).unwrap();
        println!("{HELD_MARKER}");
        let mut rest = String::new();
        let _ = io::Read::read_to_string(&mut io::stdin(), &mut rest);
        drop(lock);
    }

    fn timed_out(r: Result<Lock, LockError>) -> LockError {
        match r {
            Err(e @ LockError::Timeout { .. }) => e,
            other => panic!("expected Timeout, got {other:?}"),
        }
    }

    #[test]
    fn exclusive_without_contention() {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        let lock = Lock::acquire_with(&dir, Mode::Exclusive, LockTimeout::NoWait).unwrap();
        assert!(lock.is_held());
        assert_eq!(lock.mode(), Mode::Exclusive);
        assert_eq!(lock.warning(), None);
        drop(lock);
        // 放開後可以再取。
        Lock::acquire_with(&dir, Mode::Exclusive, LockTimeout::NoWait).unwrap();
    }

    #[test]
    fn exclusive_held_elsewhere_fails_at_once_without_waiting() {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        let holder = Holder::spawn(tmp.path(), Mode::Exclusive);
        let start = Instant::now();
        let e = timed_out(Lock::acquire_with(
            &dir,
            Mode::Exclusive,
            LockTimeout::NoWait,
        ));
        assert!(start.elapsed() < Duration::from_secs(1));
        assert_eq!(e.message(), Some(&messages::VK0042));
        match &e {
            LockError::Timeout { dir: d, mode, .. } => {
                assert_eq!(d, tmp.path());
                assert_eq!(*mode, Mode::Exclusive);
            }
            LockError::Io { .. } => unreachable!(),
        }
        // 共享鎖也被排他鎖擋住。
        timed_out(Lock::acquire_with(&dir, Mode::Shared, LockTimeout::NoWait));
        holder.release();
        Lock::acquire_with(&dir, Mode::Exclusive, LockTimeout::NoWait).unwrap();
    }

    #[test]
    fn positive_timeout_waits_that_long_then_fails() {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        let _holder = Holder::spawn(tmp.path(), Mode::Exclusive);
        let start = Instant::now();
        timed_out(Lock::acquire_with(
            &dir,
            Mode::Exclusive,
            LockTimeout::Seconds(1),
        ));
        let waited = start.elapsed();
        assert!(waited >= Duration::from_secs(1), "waited {waited:?}");
        assert!(waited < Duration::from_secs(5), "waited {waited:?}");
    }

    #[test]
    fn shared_locks_coexist_but_block_exclusive() {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        let holder = Holder::spawn(tmp.path(), Mode::Shared);
        let shared = Lock::acquire_with(&dir, Mode::Shared, LockTimeout::NoWait).unwrap();
        assert!(shared.is_held());
        timed_out(Lock::acquire_with(
            &dir,
            Mode::Exclusive,
            LockTimeout::NoWait,
        ));
        drop(shared);
        // 只剩另一個 process 的共享鎖，排他鎖仍取不到。
        timed_out(Lock::acquire_with(
            &dir,
            Mode::Exclusive,
            LockTimeout::NoWait,
        ));
        holder.release();
        Lock::acquire_with(&dir, Mode::Exclusive, LockTimeout::NoWait).unwrap();
    }

    #[test]
    fn exclusive_held_here_blocks_another_process() {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        let lock = Lock::acquire_with(&dir, Mode::Exclusive, LockTimeout::NoWait).unwrap();
        // helper 以不等的方式取鎖，取不到就失敗結束。
        let output = Command::new(std::env::current_exe().unwrap())
            .args([
                "tests::hold_lock_for_parent",
                "--exact",
                "--nocapture",
                "--test-threads=1",
            ])
            .env(HELPER_ENV, format!("shared:{}", tmp.path().display()))
            .stdin(Stdio::null())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .output()
            .unwrap();
        assert!(!output.status.success());
        assert!(!String::from_utf8_lossy(&output.stdout).contains(HELD_MARKER));
        drop(lock);
    }

    /// 在另一條 thread 取鎖，主 thread 放掉 helper 後應該取得。
    fn acquires_after_release(timeout: LockTimeout) {
        let tmp = tempfile::tempdir().unwrap();
        let holder = Holder::spawn(tmp.path(), Mode::Exclusive);
        let (tx, rx) = mpsc::channel();
        let root = tmp.path().to_path_buf();
        let waiter = thread::spawn(move || {
            let r = Lock::acquire_with(&InstallDir::new(root), Mode::Exclusive, timeout);
            tx.send(()).unwrap();
            r
        });
        // 還沒放鎖前不該取得。
        assert!(rx.recv_timeout(Duration::from_millis(300)).is_err());
        holder.release();
        rx.recv_timeout(Duration::from_secs(5)).unwrap();
        let lock = waiter.join().unwrap().unwrap();
        assert!(lock.is_held());
    }

    #[test]
    fn positive_timeout_acquires_once_released() {
        acquires_after_release(LockTimeout::Seconds(10));
    }

    #[test]
    fn forever_waits_until_released() {
        acquires_after_release(LockTimeout::Forever);
    }

    #[test]
    fn config_decides_timeout_and_enabled() {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        let _holder = Holder::spawn(tmp.path(), Mode::Exclusive);

        let no_wait = Config::parse("lock_timeout_seconds = 0").unwrap();
        let start = Instant::now();
        timed_out(Lock::acquire(&dir, Mode::Exclusive, &no_wait));
        assert!(start.elapsed() < Duration::from_secs(1));

        // 關掉鎖時不取鎖，別人持鎖也不擋，並帶 VK0060 警告。
        let disabled = Config::parse("lock_enabled = false").unwrap();
        let lock = Lock::acquire(&dir, Mode::Exclusive, &disabled).unwrap();
        assert!(!lock.is_held());
        assert_eq!(lock.warning(), Some(&messages::VK0060));
    }

    #[test]
    fn first_install_waits_sixty_seconds() {
        assert_eq!(FIRST_INSTALL_TIMEOUT, LockTimeout::Seconds(60));
    }

    #[test]
    fn missing_dir_is_an_io_error_without_code() {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path().join("missing"));
        match Lock::acquire_with(&dir, Mode::Shared, LockTimeout::NoWait) {
            Err(e @ LockError::Io { op: Op::Open, .. }) => assert_eq!(e.message(), None),
            other => panic!("expected Io, got {other:?}"),
        }
    }

    #[test]
    fn regular_file_is_not_locked() {
        let tmp = tempfile::tempdir().unwrap();
        let file = tmp.path().join("file");
        std::fs::write(&file, "").unwrap();
        match Lock::acquire_with(
            &InstallDir::new(&file),
            Mode::Exclusive,
            LockTimeout::NoWait,
        ) {
            Err(LockError::Io {
                op: Op::Open,
                source,
                ..
            }) => assert_eq!(source.raw_os_error(), Some(Errno::ENOTDIR as i32)),
            other => panic!("expected ENOTDIR, got {other:?}"),
        }
    }
}
