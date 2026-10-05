//! 可寫 recipe 的落地順序（ADR-0004 可寫 recipe 的時序、`cache/` 與 `gen/` 的寫入順序；04 共同選項
//! 「全部同意才寫入」；#372 取件時機定案：先取到 repo 外暫存，全部同意才寫 cache／印記／gen）。
//!
//! 呼叫端問完所有問題、全部同意之後，才用 [`Txn`] 依序落地。順序固定：
//!
//! 1. 執行紀錄記 `writes_started`（第一筆非紀錄檔寫入之前）。
//! 2. 建進度檔（早於第一個 repo 檔或 VK 檔的寫入）。
//! 3. 換 `cache/<repo>/` 與印記，一個工具接一個工具。
//! 4. 寫 repo 檔。
//! 5. 寫 `.vendor_kit/` 下的紀錄檔：初始檔的逐檔紀錄（metadata）與基準版副本。紀錄記的是 repo 檔
//!    寫入後的 hash，所以排在 repo 檔之後。
//! 6. 寫入口檔 `gen/tools.just`（`cache/` 換好之後才寫）。
//! 7. 執行紀錄記 `lock_line_write_started`。
//! 8. 改版本鎖定行（最後才改：中途失敗時版本鎖定行不動）。
//! 9. 執行紀錄記 `lock_line_written`。
//! 10. 刪進度檔：這次操作唯一的完成點。
//! 11. 執行紀錄記 `progress_removed`。
//!
//! 每一步是一個消耗 `self` 的方法，回傳下一個狀態的 [`Txn`]，所以順序寫錯編譯不過；失敗回 [`Failed`]，
//! 這次操作就此結束，不能接著寫。第 3–5 步一次收齊全部項目（可以是空的），第 6 步可以不寫，第 7–9 步
//! 可以整段略過（[`Txn::keep_lock_line`]），但不能換順序。
//!
//! 下面是正確的順序：
//!
//! ```no_run
//! # fn demo<E: txn::Effects>(fx: &mut E, p: progress::Progress, lock: &mut version_file::LockFile)
//! # -> Result<(), txn::Failed> {
//! txn::Txn::begin(fx, p)?
//!     .swap_cache(&[])?
//!     .write_repo_files(&[])?
//!     .write_records(&[])?
//!     .write_tools_just(Some(b"mod x '../cache/x/just/x.just'\n"))?
//!     .write_lock_line(lock, runlog::Target::Tool)?
//!     .complete()?;
//! # Ok(()) }
//! ```
//!
//! 版本鎖定行排在入口檔之前，編譯不過：
//!
//! ```compile_fail
//! # fn demo<E: txn::Effects>(fx: &mut E, p: progress::Progress, lock: &mut version_file::LockFile)
//! # -> Result<(), txn::Failed> {
//! txn::Txn::begin(fx, p)?
//!     .swap_cache(&[])?
//!     .write_repo_files(&[])?
//!     .write_records(&[])?
//!     .write_lock_line(lock, runlog::Target::Tool)?
//!     .complete()?;
//! # Ok(()) }
//! ```
//!
//! 沒刪進度檔就沒有完成點；略過換 `cache/` 直接寫 repo 檔，同樣編譯不過：
//!
//! ```compile_fail
//! # fn demo<E: txn::Effects>(fx: &mut E, p: progress::Progress) -> Result<(), txn::Failed> {
//! txn::Txn::begin(fx, p)?.write_repo_files(&[])?;
//! # Ok(()) }
//! ```
//!
//! 實際的寫入經 [`Effects`] 做：[`Disk`] 呼叫既有的 `progress`、`runlog`、`files`、`stamp`、
//! `version_file`；測試換成會在第 N 步失敗的實作，驗每一步中斷後的殘留狀態。殘留怎麼辨識：
//!
//! - 第 1 步失敗：沒有任何非紀錄檔寫入。
//! - 第 2 步失敗：紀錄有 `writes_started`、沒有 `progress_removed`，進度檔不在
//!   （`files::write_atomic` 不留半份，暫存檔名不以 `.toml` 結尾，`progress::find` 不認），也沒有其他寫入。
//! - 第 3–10 步失敗：進度檔還在，可寫 recipe 先恢復、唯讀 recipe 報出未完成（ADR-0004）。第 8 步失敗時
//!   紀錄另有 `lock_line_write_started` 而沒有對應的 `lock_line_written`（`runlog::assess` 的規則 6）。
//! - 第 11 步失敗：進度檔已刪，操作已完成，只是紀錄少了 `progress_removed`（[`Step::completed`]）。
//!
//! 中途寫檔失敗目前訊息表沒有代碼（引擎實作計畫缺口 G4）：[`Failed::message`] 對寫檔失敗回 `None`，
//! 只轉出底層 crate 已有的代碼（例如紀錄事件未登錄的 VK0056、進度檔版本過高的 VK0008）。
//! 這裡不印診斷；要怎麼印由呼叫端經 `diagnostics` 決定。
//!
//! 進度檔要放哪些恢復用的欄位、恢復怎麼做、殘留要報哪個代碼，都由 recipe 決定，不在這裡。
//! 呼叫端要先持安裝目錄的排他鎖（`filelock`）。印記的檔名與位置文件還沒定，由呼叫端給路徑
//! （[`ToolContent::stamp_file`]）。

use std::fmt;
use std::fs;
use std::io::{self, Write};
use std::marker::PhantomData;
use std::os::unix::fs::PermissionsExt;
use std::path::{Component, Path, PathBuf};

use layout::{InstallDir, InvalidName};
use messages::Message;
use progress::Progress;
use runlog::{Event, Target};
use stamp::Stamp;
use version_file::LockFile;

/// 入口檔在 `gen/` 底下的檔名。
pub const TOOLS_JUST: &str = "tools.just";

// ---------------------------------------------------------------------------
// 輸入

/// 一個工具要換進 `cache/<repo>/` 的內容。
#[derive(Debug, Clone, Copy)]
pub struct ToolContent<'a> {
    /// 工具名，`cache/` 底下的一段目錄名。
    pub repo: &'a str,
    /// 取件時放在 repo 外的暫存目錄，裡面是工具內容根目錄。
    pub staged: &'a Path,
    /// 取件所依據的版本鎖定行的值，寫進印記。
    pub version: &'a str,
    /// 印記檔的路徑。
    pub stamp_file: &'a Path,
}

/// 一個要寫的 repo 檔。
#[derive(Debug, Clone, Copy)]
pub struct RepoFile<'a> {
    /// 相對於 repo 根目錄的路徑，只能由一般路徑段組成（不准絕對路徑、`.`、`..`）。
    pub path: &'a Path,
    /// 整檔的新內容。
    pub contents: &'a [u8],
}

/// 一個要寫的 VK 紀錄檔：metadata（`baseline/<repo>.toml`）或基準版副本。
#[derive(Debug, Clone, Copy)]
pub struct RecordFile<'a> {
    /// 相對於 `.vendor_kit/` 的路徑，只能由一般路徑段組成。
    pub path: &'a Path,
    /// 整檔的新內容。
    pub contents: &'a [u8],
}

// ---------------------------------------------------------------------------
// 步驟與錯誤

/// 落地順序的每一步，依序排列。
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Step {
    /// 記 `writes_started`。
    WritesStarted,
    /// 建進度檔。
    CreateProgress,
    /// 換 `cache/<repo>/` 與印記。
    SwapCache,
    /// 寫 repo 檔。
    RepoFile,
    /// 寫 metadata 與基準版副本。
    Records,
    /// 寫 `gen/tools.just`。
    ToolsJust,
    /// 記 `lock_line_write_started`。
    LockLineWriteStarted,
    /// 改版本鎖定行。
    LockLine,
    /// 記 `lock_line_written`。
    LockLineWritten,
    /// 刪進度檔（完成點）。
    DeleteProgress,
    /// 記 `progress_removed`。
    ProgressRemoved,
}

impl Step {
    pub const ALL: [Step; 11] = [
        Step::WritesStarted,
        Step::CreateProgress,
        Step::SwapCache,
        Step::RepoFile,
        Step::Records,
        Step::ToolsJust,
        Step::LockLineWriteStarted,
        Step::LockLine,
        Step::LockLineWritten,
        Step::DeleteProgress,
        Step::ProgressRemoved,
    ];

    /// 在這一步失敗時，完成點（刪進度檔）是否已經過了：只有記 `progress_removed` 失敗是。
    pub fn completed(self) -> bool {
        self == Step::ProgressRemoved
    }

    pub const fn as_str(self) -> &'static str {
        match self {
            Step::WritesStarted => "writes_started",
            Step::CreateProgress => "create progress file",
            Step::SwapCache => "swap cache",
            Step::RepoFile => "write repo file",
            Step::Records => "write records",
            Step::ToolsJust => "write gen/tools.just",
            Step::LockLineWriteStarted => "lock_line_write_started",
            Step::LockLine => "write lock line",
            Step::LockLineWritten => "lock_line_written",
            Step::DeleteProgress => "delete progress file",
            Step::ProgressRemoved => "progress_removed",
        }
    }
}

impl fmt::Display for Step {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

/// 一步寫入失敗的原因。
#[derive(Debug)]
pub enum Error {
    /// 寫執行紀錄失敗。
    Log(runlog::Error),
    /// 建或刪進度檔失敗。
    Progress(progress::Error),
    /// `<repo>` 不是合法的 `cache/` 目錄名。
    Name(InvalidName),
    /// repo 檔或紀錄檔的路徑不是相對路徑或含 `.`、`..`。
    BadPath(PathBuf),
    /// 讀暫存目錄、建目錄、搬目錄、刪目錄的系統呼叫失敗。
    Io { path: PathBuf, source: io::Error },
    /// 原子寫入失敗。
    Write(files::Error),
    /// 算印記失敗。
    StampCompute(stamp::ComputeError),
    /// 寫印記失敗。
    Stamp(stamp::Error),
    /// 寫版本鎖定行失敗。
    Lock(version_file::Error),
}

impl Error {
    fn io(path: &Path, source: io::Error) -> Error {
        Error::Io {
            path: path.to_path_buf(),
            source,
        }
    }

    /// 對應的訊息表條目。寫檔失敗沒有代碼（G4），回 `None`；只轉出底層 crate 已有的代碼。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            Error::Log(e) => e.message(),
            Error::Progress(e) => e.message(),
            Error::Stamp(e) => e.message(),
            Error::Lock(e) => e.message(),
            Error::Name(_)
            | Error::BadPath(_)
            | Error::Io { .. }
            | Error::Write(_)
            | Error::StampCompute(_) => None,
        }
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Log(e) => e.fmt(f),
            Error::Progress(e) => e.fmt(f),
            Error::Name(e) => e.fmt(f),
            Error::BadPath(p) => write!(f, "not a plain relative path: {}", p.display()),
            Error::Io { path, source } => write!(f, "{}: {source}", path.display()),
            Error::Write(e) => e.fmt(f),
            Error::StampCompute(e) => e.fmt(f),
            Error::Stamp(e) => e.fmt(f),
            Error::Lock(e) => e.fmt(f),
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Error::Log(e) => Some(e),
            Error::Progress(e) => Some(e),
            Error::Name(e) => Some(e),
            Error::Io { source, .. } => Some(source),
            Error::Write(e) => Some(e),
            Error::StampCompute(e) => Some(e),
            Error::Stamp(e) => Some(e),
            Error::Lock(e) => Some(e),
            Error::BadPath(_) => None,
        }
    }
}

/// 在哪一步、為什麼失敗。這次操作就此結束。
#[derive(Debug)]
pub struct Failed {
    pub step: Step,
    pub error: Error,
}

impl Failed {
    /// 見 [`Error::message`]：中途寫檔失敗回 `None`（G4）。
    pub fn message(&self) -> Option<&'static Message> {
        self.error.message()
    }
}

impl fmt::Display for Failed {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}: {}", self.step, self.error)
    }
}

impl std::error::Error for Failed {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        Some(&self.error)
    }
}

// ---------------------------------------------------------------------------
// 寫入

/// 每一步實際的寫入。[`Disk`] 是真的實作；測試以包一層的實作注入故障。
pub trait Effects {
    /// 寫一筆執行紀錄。
    fn log(&mut self, event: &Event) -> Result<(), Error>;
    /// 建進度檔，回傳它的路徑；同名進度檔已在要拒絕。
    fn create_progress(&mut self, progress: &mut Progress) -> Result<PathBuf, Error>;
    /// 把一個工具的暫存內容換進 `cache/<repo>/`，再寫它的印記。
    fn swap_cache(&mut self, tool: &ToolContent) -> Result<(), Error>;
    /// 寫一個 repo 檔。
    fn write_repo_file(&mut self, file: &RepoFile) -> Result<(), Error>;
    /// 寫一個 `.vendor_kit/` 下的紀錄檔。
    fn write_record_file(&mut self, file: &RecordFile) -> Result<(), Error>;
    /// 寫 `gen/tools.just`。
    fn write_tools_just(&mut self, contents: &[u8]) -> Result<(), Error>;
    /// 寫版本鎖定行所在的 `.vendor_kit/version.toml`。
    fn save_lock(&mut self, lock: &mut LockFile) -> Result<(), Error>;
    /// 刪進度檔（完成點）。
    fn delete_progress(&mut self, progress: &Progress) -> Result<(), Error>;
}

/// 寫到安裝目錄與執行紀錄的 [`Effects`]。
pub struct Disk<'a, W: Write> {
    dir: &'a InstallDir,
    log: &'a mut runlog::Writer<W>,
    written_by: &'a str,
}

impl<'a, W: Write> Disk<'a, W> {
    /// `written_by` 蓋在進度檔、印記與 `version.toml` 上。
    pub fn new(dir: &'a InstallDir, log: &'a mut runlog::Writer<W>, written_by: &'a str) -> Self {
        Disk {
            dir,
            log,
            written_by,
        }
    }
}

impl<W: Write> Effects for Disk<'_, W> {
    fn log(&mut self, event: &Event) -> Result<(), Error> {
        self.log.write(event).map_err(Error::Log)
    }

    fn create_progress(&mut self, progress: &mut Progress) -> Result<PathBuf, Error> {
        progress
            .create(self.dir, self.written_by)
            .map_err(Error::Progress)
    }

    fn swap_cache(&mut self, tool: &ToolContent) -> Result<(), Error> {
        let target = self.dir.tool_cache(tool.repo).map_err(Error::Name)?;
        let cache = self.dir.cache_dir();
        let new = cache.join(format!(".tmp.{}.new", tool.repo));
        let old = cache.join(format!(".tmp.{}.old", tool.repo));
        remove_dir_if_present(&new)?;
        remove_dir_if_present(&old)?;
        // 暫存目錄在 repo 外，可能不在同一個檔案系統上，不能直接 rename：先複製到 cache/ 底下。
        copy_tree(tool.staged, &new)?;
        let had_old = present(&target)?;
        if had_old {
            fs::rename(&target, &old).map_err(|e| Error::io(&target, e))?;
        }
        fs::rename(&new, &target).map_err(|e| Error::io(&target, e))?;
        sync_dir(&cache)?;
        if had_old {
            fs::remove_dir_all(&old).map_err(|e| Error::io(&old, e))?;
        }
        // 印記由換好的 cache/<repo>/ 算，記的是實際落地的位元組。
        let mut stamp =
            Stamp::compute_tool(self.dir, tool.repo, tool.version).map_err(Error::StampCompute)?;
        stamp
            .save(tool.stamp_file, self.written_by)
            .map_err(Error::Stamp)
    }

    fn write_repo_file(&mut self, file: &RepoFile) -> Result<(), Error> {
        plain(file.path)?;
        write_file(&self.dir.root().join(file.path), file.contents)
    }

    fn write_record_file(&mut self, file: &RecordFile) -> Result<(), Error> {
        plain(file.path)?;
        write_file(&self.dir.vk_dir().join(file.path), file.contents)
    }

    fn write_tools_just(&mut self, contents: &[u8]) -> Result<(), Error> {
        write_file(&self.dir.gen_dir().join(TOOLS_JUST), contents)
    }

    fn save_lock(&mut self, lock: &mut LockFile) -> Result<(), Error> {
        lock.save_to(self.dir, self.written_by).map_err(Error::Lock)
    }

    fn delete_progress(&mut self, progress: &Progress) -> Result<(), Error> {
        progress::delete(self.dir, progress.verb(), progress.id()).map_err(Error::Progress)
    }
}

/// 只由一般路徑段組成的相對路徑才收。
fn plain(path: &Path) -> Result<(), Error> {
    let ok = path.components().count() > 0
        && path.components().all(|c| matches!(c, Component::Normal(_)));
    if ok {
        Ok(())
    } else {
        Err(Error::BadPath(path.to_path_buf()))
    }
}

/// 路徑在不在（不跟隨 symlink）。
fn present(path: &Path) -> Result<bool, Error> {
    match fs::symlink_metadata(path) {
        Ok(_) => Ok(true),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(false),
        Err(e) => Err(Error::io(path, e)),
    }
}

fn remove_dir_if_present(path: &Path) -> Result<(), Error> {
    if present(path)? {
        fs::remove_dir_all(path).map_err(|e| Error::io(path, e))?;
    }
    Ok(())
}

/// 把 `from` 底下的一般檔逐一原子寫到 `to` 底下，沿用原檔的權限位元。symlink 等非一般檔回錯。
fn copy_tree(from: &Path, to: &Path) -> Result<(), Error> {
    fs::create_dir_all(to).map_err(|e| Error::io(to, e))?;
    for rel in files::walk_sorted(from).map_err(Error::Write)? {
        let src = from.join(&rel);
        let dst = to.join(&rel);
        let contents = fs::read(&src).map_err(|e| Error::io(&src, e))?;
        write_file(&dst, &contents)?;
        let mode = fs::metadata(&src)
            .map_err(|e| Error::io(&src, e))?
            .permissions()
            .mode();
        fs::set_permissions(&dst, fs::Permissions::from_mode(mode & 0o7777))
            .map_err(|e| Error::io(&dst, e))?;
    }
    Ok(())
}

/// 上層目錄不在時先建，再原子寫入。
fn write_file(path: &Path, contents: &[u8]) -> Result<(), Error> {
    if let Some(parent) = path.parent().filter(|p| !p.as_os_str().is_empty()) {
        fs::create_dir_all(parent).map_err(|e| Error::io(parent, e))?;
    }
    files::write_atomic(path, contents).map_err(Error::Write)
}

fn sync_dir(dir: &Path) -> Result<(), Error> {
    fs::File::open(dir)
        .and_then(|d| d.sync_all())
        .map_err(|e| Error::io(dir, e))
}

// ---------------------------------------------------------------------------
// 型別狀態

/// 已建進度檔，下一步換 `cache/`。
pub struct Begun;
/// `cache/` 與印記已換好，下一步寫 repo 檔。
pub struct CacheSwapped;
/// repo 檔已寫好，下一步寫紀錄檔。
pub struct RepoWritten;
/// 紀錄檔已寫好，下一步寫入口檔。
pub struct RecordsWritten;
/// 入口檔已寫好，下一步改版本鎖定行。
pub struct EntryWritten;
/// 版本鎖定行已處理，下一步刪進度檔。
pub struct LockHandled;

/// 一次可寫 recipe 的落地。`S` 是目前走到哪一步，每一步只在對應的狀態上有方法。
pub struct Txn<'e, E: Effects + ?Sized, S> {
    fx: &'e mut E,
    progress: Progress,
    progress_file: String,
    state: PhantomData<S>,
}

/// 刪掉進度檔、記好 `progress_removed` 之後的結果。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Done {
    /// 刪掉的進度檔檔名。
    pub progress_file: String,
}

fn at(step: Step) -> impl FnOnce(Error) -> Failed {
    move |error| Failed { step, error }
}

impl<'e, E: Effects + ?Sized> Txn<'e, E, Begun> {
    /// 第 1、2 步：記 `writes_started`，再建進度檔。
    pub fn begin(fx: &'e mut E, mut progress: Progress) -> Result<Self, Failed> {
        fx.log(&Event::WritesStarted)
            .map_err(at(Step::WritesStarted))?;
        let path = fx
            .create_progress(&mut progress)
            .map_err(at(Step::CreateProgress))?;
        let progress_file = path
            .file_name()
            .map(|n| n.to_string_lossy().into_owned())
            .unwrap_or_default();
        Ok(Txn {
            fx,
            progress,
            progress_file,
            state: PhantomData,
        })
    }

    /// 第 3 步：依序換每個工具的 `cache/<repo>/` 與印記；可以是空的。
    pub fn swap_cache(self, tools: &[ToolContent]) -> Result<Txn<'e, E, CacheSwapped>, Failed> {
        for tool in tools {
            self.fx.swap_cache(tool).map_err(at(Step::SwapCache))?;
        }
        Ok(self.next())
    }
}

impl<'e, E: Effects + ?Sized> Txn<'e, E, CacheSwapped> {
    /// 第 4 步：依序寫每個 repo 檔；可以是空的。
    pub fn write_repo_files(self, files: &[RepoFile]) -> Result<Txn<'e, E, RepoWritten>, Failed> {
        for file in files {
            self.fx.write_repo_file(file).map_err(at(Step::RepoFile))?;
        }
        Ok(self.next())
    }
}

impl<'e, E: Effects + ?Sized> Txn<'e, E, RepoWritten> {
    /// 第 5 步：依序寫每個紀錄檔；可以是空的。
    pub fn write_records(self, files: &[RecordFile]) -> Result<Txn<'e, E, RecordsWritten>, Failed> {
        for file in files {
            self.fx.write_record_file(file).map_err(at(Step::Records))?;
        }
        Ok(self.next())
    }
}

impl<'e, E: Effects + ?Sized> Txn<'e, E, RecordsWritten> {
    /// 第 6 步：寫 `gen/tools.just`；`None` 表示入口檔不變。
    pub fn write_tools_just(
        self,
        contents: Option<&[u8]>,
    ) -> Result<Txn<'e, E, EntryWritten>, Failed> {
        if let Some(contents) = contents {
            self.fx
                .write_tools_just(contents)
                .map_err(at(Step::ToolsJust))?;
        }
        Ok(self.next())
    }
}

impl<'e, E: Effects + ?Sized> Txn<'e, E, EntryWritten> {
    /// 第 7–9 步：記 `lock_line_write_started`，寫 `lock`（呼叫端已改好的版本鎖定行），
    /// 再記 `lock_line_written`。`target` 是改的是引擎還是工具的版本鎖定行。
    pub fn write_lock_line(
        self,
        lock: &mut LockFile,
        target: Target,
    ) -> Result<Txn<'e, E, LockHandled>, Failed> {
        self.fx
            .log(&Event::LockLineWriteStarted { target })
            .map_err(at(Step::LockLineWriteStarted))?;
        self.fx.save_lock(lock).map_err(at(Step::LockLine))?;
        self.fx
            .log(&Event::LockLineWritten { target })
            .map_err(at(Step::LockLineWritten))?;
        Ok(self.next())
    }

    /// 這次不改版本鎖定行（例如只重裝 `cache/`）：不寫 `version.toml`，也不記鎖定行的事件。
    pub fn keep_lock_line(self) -> Txn<'e, E, LockHandled> {
        self.next()
    }
}

impl<E: Effects + ?Sized> Txn<'_, E, LockHandled> {
    /// 第 10、11 步：刪進度檔（完成點），再記 `progress_removed`。
    pub fn complete(self) -> Result<Done, Failed> {
        self.fx
            .delete_progress(&self.progress)
            .map_err(at(Step::DeleteProgress))?;
        self.fx
            .log(&Event::ProgressRemoved {
                file: &self.progress_file,
            })
            .map_err(at(Step::ProgressRemoved))?;
        Ok(Done {
            progress_file: self.progress_file,
        })
    }
}

impl<'e, E: Effects + ?Sized, S> Txn<'e, E, S> {
    /// 這次操作的進度內容。
    pub fn progress(&self) -> &Progress {
        &self.progress
    }

    fn next<T>(self) -> Txn<'e, E, T> {
        Txn {
            fx: self.fx,
            progress: self.progress,
            progress_file: self.progress_file,
            state: PhantomData,
        }
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests;
