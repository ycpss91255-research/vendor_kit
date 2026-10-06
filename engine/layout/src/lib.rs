//! 安裝目錄判定與 `.vendor_kit/` 下各檔的路徑。
//!
//! - 安裝目錄是 `.vendor_kit/` 的直接父目錄（GLOSSARY）。判定只看「這個目錄底下有沒有真的
//!   `.vendor_kit/` 目錄」，不看裡面有哪些檔（ADR-0007）；`.vendor_kit` 是一般檔或 symlink 都不算。
//! - VK recipe 只准在安裝目錄執行，檢查的是使用者打指令時的所在目錄，子目錄也不算（04 執行位置）。
//!   不在安裝目錄時回 [`LayoutError::NotInstallDir`]（VK0028）。
//! - 安裝目錄彼此不互相包含（02 第 2 條）。首次導入前用 [`check_nested`] 找上層或下層已有的
//!   安裝目錄，找到就回 [`LayoutError::Nested`]（VK0029）。
//! - `.vendor_kit/` 下各檔的名字只寫在這裡（ADR-0002、ADR-0003、ADR-0004、ADR-0007），契約沒定名、
//!   由引擎自訂的檔也是：
//!   - 工具的印記 `cache/<repo>.stamp.toml`（[`InstallDir::tool_stamp`]）：第一行是 schema，
//!     印記第一行的語意變了要升介面版（ADR-0008）。
//!   - 初始檔的逐檔紀錄（metadata）`baseline/<repo>.toml`（[`InstallDir::tool_metadata`]）與
//!     `baseline/.vendor_kit.toml`（[`InstallDir::baseline_vk`]）。
//!   - 執行紀錄檔 `log/<ts>-<verb>-<id>.jsonl`（[`InstallDir::log_dir`] 底下）：檔名由啟動器取
//!     （`launcher/log.sh`），經入口 argv 把路徑傳進引擎，引擎只照傳進來的路徑寫，不自己組檔名。
//!
//! 這裡只做判定與組路徑，不寫檔、不印診斷；要不要印、怎麼印由呼叫端經 `diagnostics` 決定。

use std::ffi::OsString;
use std::fmt;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

use messages::Message;

/// VK 在安裝目錄下的目錄名。
pub const VK_DIR: &str = ".vendor_kit";

/// 薄殼四檔，都在 `.vendor_kit/` 下（ADR-0007）。
pub const SHELL_FILES: [&str; 4] = ["entry.just", "vendor.just", "log.sh", ".gitignore"];

/// 工具印記的檔名後綴：`cache/<repo>.stamp.toml`（[`InstallDir::tool_stamp`]）。
pub const STAMP_SUFFIX: &str = ".stamp.toml";

/// 逐檔紀錄（metadata）的檔名後綴：`baseline/<repo>.toml`（[`InstallDir::tool_metadata`]）。
pub const METADATA_SUFFIX: &str = ".toml";

/// 往下找巢狀安裝時不進去的目錄名：git 的內部目錄不是使用者的目錄樹。
const SKIP_DIRS: [&str; 1] = [".git"];

/// 一個安裝目錄，以及它 `.vendor_kit/` 下各檔的路徑。
///
/// 只記根目錄；各檔路徑都由根目錄組出來，不碰檔案系統。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InstallDir {
    root: PathBuf,
}

impl InstallDir {
    /// 以 `root` 為安裝目錄，不檢查檔案系統。
    ///
    /// 用在已經判定過的根目錄（例如啟動器傳進來、掛進容器的安裝目錄），或首次導入時
    /// 還沒有 `.vendor_kit/` 的目錄。要從使用者所在目錄判定，用 [`probe`] 或 [`require`]。
    pub fn new(root: impl Into<PathBuf>) -> Self {
        Self { root: root.into() }
    }

    /// 安裝目錄本身。
    pub fn root(&self) -> &Path {
        &self.root
    }

    /// `.vendor_kit/`。
    pub fn vk_dir(&self) -> PathBuf {
        self.root.join(VK_DIR)
    }

    /// `.vendor_kit/version.toml`：全部版本鎖定行，進 git（ADR-0002）。
    pub fn version_toml(&self) -> PathBuf {
        self.vk_dir().join("version.toml")
    }

    /// `.vendor_kit/version.local.toml`：本機覆寫，不進 git（ADR-0002）。
    pub fn version_local_toml(&self) -> PathBuf {
        self.vk_dir().join("version.local.toml")
    }

    /// `.vendor_kit/config.toml`：使用者維護的設定（04 使用者的檔與 VK 的檔）。
    pub fn config_toml(&self) -> PathBuf {
        self.vk_dir().join("config.toml")
    }

    /// `.vendor_kit/cache/`：已展開的工具內容，不進 git（ADR-0002）。
    pub fn cache_dir(&self) -> PathBuf {
        self.vk_dir().join("cache")
    }

    /// `.vendor_kit/cache/<repo>/`。`<repo>` 必須是單一路徑段，跳不出 `cache/`。
    pub fn tool_cache(&self, repo: &str) -> Result<PathBuf, InvalidName> {
        check_segment(repo, NameKind::Repo)?;
        Ok(self.cache_dir().join(repo))
    }

    /// `.vendor_kit/cache/<repo>.stamp.toml`：工具 `<repo>` 的印記。
    ///
    /// 在 `cache/` 底下所以不進 git，又不在 `cache/<repo>/` 裡，換 `cache/<repo>/` 時不會被帶走。
    /// 與 [`InstallDir::stamp`]（`gen/.stamp`，薄殼的引擎 ref）是不同的檔。`<repo>` 由呼叫端先驗過是
    /// 單一路徑段，這裡不再檢查。
    pub fn tool_stamp(&self, repo: &str) -> PathBuf {
        self.cache_dir().join(format!("{repo}{STAMP_SUFFIX}"))
    }

    /// `.vendor_kit/gen/`：供 just 載入的產生檔，不進 git。
    pub fn gen_dir(&self) -> PathBuf {
        self.vk_dir().join("gen")
    }

    /// `.vendor_kit/gen/.stamp`：產生薄殼的引擎 ref，供快路徑比對（ADR-0007）。
    pub fn stamp(&self) -> PathBuf {
        self.gen_dir().join(".stamp")
    }

    /// `.vendor_kit/log/`：執行紀錄，不進 git（ADR-0002、ADR-0005）。
    pub fn log_dir(&self) -> PathBuf {
        self.vk_dir().join("log")
    }

    /// `.vendor_kit/baseline/`：初始檔的基準版（ADR-0003）。
    pub fn baseline_dir(&self) -> PathBuf {
        self.vk_dir().join("baseline")
    }

    /// `.vendor_kit/baseline/.vendor_kit.toml`：不屬於任何工具的根 `.dockerignore` 行（ADR-0003）。
    pub fn baseline_vk(&self) -> PathBuf {
        self.baseline_dir().join(".vendor_kit.toml")
    }

    /// `.vendor_kit/baseline/<repo>.toml`：工具 `<repo>` 的逐檔紀錄（metadata，ADR-0003）。
    ///
    /// `<repo>` 必須是單一路徑段，且不以 `.` 開頭，才不會跟 [`InstallDir::baseline_vk`] 撞名。
    pub fn tool_metadata(&self, repo: &str) -> Result<PathBuf, InvalidName> {
        check_segment(repo, NameKind::Repo)?;
        if repo.starts_with('.') {
            return Err(InvalidName::new(NameKind::Repo, repo));
        }
        Ok(self.baseline_dir().join(format!("{repo}{METADATA_SUFFIX}")))
    }

    /// `.vendor_kit/baseline/.vendor_kit/config.toml`：`config.toml` 的基準版副本（ADR-0003）。
    ///
    /// 紀錄在 [`InstallDir::baseline_vk`]；副本放在 `baseline/` 下照 `config.toml` 的 repo 相對路徑
    /// （`.vendor_kit/config.toml`）擺，跟工具的 `baseline/<repo>/<路徑>` 同一個擺法，只是不分工具。
    pub fn config_baseline(&self) -> PathBuf {
        self.baseline_dir().join(VK_DIR).join("config.toml")
    }

    /// `.vendor_kit/.gitignore`：薄殼四檔之一，也是自動化可以自己寫的界線（ADR-0002）。
    pub fn gitignore(&self) -> PathBuf {
        self.vk_dir().join(".gitignore")
    }

    /// 薄殼四檔，順序同 [`SHELL_FILES`]。
    pub fn shell_files(&self) -> [PathBuf; 4] {
        SHELL_FILES.map(|name| self.vk_dir().join(name))
    }

    /// 進度檔 `.vendor_kit/.tmp.<verb>.<id>.toml`（ADR-0004）。
    ///
    /// `<verb>` 與 `<id>` 各是一段不含 `.` 的名字，檔名才拆得回去。
    pub fn progress_file(&self, verb: &str, id: &str) -> Result<PathBuf, InvalidName> {
        check_segment(verb, NameKind::Verb)?;
        check_segment(id, NameKind::Id)?;
        if verb.contains('.') {
            return Err(InvalidName::new(NameKind::Verb, verb));
        }
        if id.contains('.') {
            return Err(InvalidName::new(NameKind::Id, id));
        }
        Ok(self.vk_dir().join(format!(".tmp.{verb}.{id}.toml")))
    }
}

/// `dir` 底下有沒有真的 `.vendor_kit/` 目錄（不跟 symlink）。
pub fn is_install_dir(dir: &Path) -> io::Result<bool> {
    match fs::symlink_metadata(dir.join(VK_DIR)) {
        Ok(meta) => Ok(meta.file_type().is_dir()),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(false),
        Err(e) => Err(e),
    }
}

/// [`probe`] 的結果。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Probe {
    /// 已經是安裝目錄（有 `.vendor_kit/`）。
    Existing(InstallDir),
    /// 還沒有 `.vendor_kit/`：`install` 當首次導入處理（04 首次導入還是既有安裝目錄）。
    Fresh(InstallDir),
}

impl Probe {
    /// 不論哪一種，都是以使用者所在目錄為根的安裝目錄。
    pub fn dir(&self) -> &InstallDir {
        match self {
            Probe::Existing(d) | Probe::Fresh(d) => d,
        }
    }
}

/// `install` 用：使用者所在目錄是既有安裝目錄，還是首次導入。兩種都不算錯。
pub fn probe(cwd: &Path) -> Result<Probe, LayoutError> {
    let dir = InstallDir::new(cwd);
    if is_install_dir(cwd).map_err(|e| LayoutError::io(cwd, e))? {
        Ok(Probe::Existing(dir))
    } else {
        Ok(Probe::Fresh(dir))
    }
}

/// `install` 以外的 VK recipe 用：使用者所在目錄必須就是安裝目錄（VK0028）。
///
/// 不往上找替使用者換目錄；最近的上層安裝目錄只放進錯誤裡當 `cd` 的提示，找不到就沒有提示。
pub fn require(cwd: &Path) -> Result<InstallDir, LayoutError> {
    if is_install_dir(cwd).map_err(|e| LayoutError::io(cwd, e))? {
        return Ok(InstallDir::new(cwd));
    }
    let nearest = cwd
        .ancestors()
        .skip(1)
        .find(|a| is_install_dir(a).unwrap_or(false))
        .map(Path::to_path_buf);
    Err(LayoutError::NotInstallDir {
        cwd: cwd.to_path_buf(),
        nearest,
    })
}

/// 首次導入前的巢狀判定（VK0029）：`target` 的上層（到 `repo_root` 為止，含 `repo_root`）
/// 或下層已有安裝目錄就拒絕。
///
/// - 上層由近到遠找，不出 `repo_root`；`target` 不在 `repo_root` 底下時不找上層。
/// - 下層依名字排序、先序走訪，回報第一個找到的，結果固定。不跟 symlink、不進 `.git`。
/// - `target` 自己的 `.vendor_kit/` 不算：未完成的首次導入可能已經留下它。
pub fn check_nested(target: &Path, repo_root: &Path) -> Result<(), LayoutError> {
    for ancestor in target.ancestors().skip(1) {
        if !ancestor.starts_with(repo_root) {
            break;
        }
        if is_install_dir(ancestor).map_err(|e| LayoutError::io(ancestor, e))? {
            return Err(LayoutError::Nested {
                existing: ancestor.to_path_buf(),
            });
        }
    }
    match find_below(target, true)? {
        Some(existing) => Err(LayoutError::Nested { existing }),
        None => Ok(()),
    }
}

/// 在 `dir` 之下（不含 `dir` 本身）先序找第一個安裝目錄。
fn find_below(dir: &Path, is_target: bool) -> Result<Option<PathBuf>, LayoutError> {
    if !is_target && is_install_dir(dir).map_err(|e| LayoutError::io(dir, e))? {
        return Ok(Some(dir.to_path_buf()));
    }
    for name in sorted_subdirs(dir)? {
        if SKIP_DIRS.iter().any(|s| name == *s) || (is_target && name == VK_DIR) {
            continue;
        }
        if let Some(found) = find_below(&dir.join(&name), false)? {
            return Ok(Some(found));
        }
    }
    Ok(None)
}

/// `dir` 底下真的子目錄（不含 symlink）的名字，依位元組排序。
fn sorted_subdirs(dir: &Path) -> Result<Vec<OsString>, LayoutError> {
    let mut names = Vec::new();
    for entry in fs::read_dir(dir).map_err(|e| LayoutError::io(dir, e))? {
        let entry = entry.map_err(|e| LayoutError::io(dir, e))?;
        let file_type = entry.file_type().map_err(|e| LayoutError::io(dir, e))?;
        if file_type.is_dir() {
            names.push(entry.file_name());
        }
    }
    names.sort();
    Ok(names)
}

/// 安裝目錄判定的錯誤。
#[derive(Debug)]
pub enum LayoutError {
    /// 使用者所在目錄不是安裝目錄（VK0028）。`nearest` 是最近的上層安裝目錄，填 `<install_dir>`。
    NotInstallDir {
        cwd: PathBuf,
        nearest: Option<PathBuf>,
    },
    /// 上層或下層已有安裝目錄（VK0029），填 `<existing_install_dir>`。
    Nested { existing: PathBuf },
    /// 讀目錄失敗。訊息表沒有對應代碼，由呼叫端當內部錯誤處理。
    Io { path: PathBuf, source: io::Error },
}

impl LayoutError {
    fn io(path: &Path, source: io::Error) -> Self {
        LayoutError::Io {
            path: path.to_path_buf(),
            source,
        }
    }

    /// 對應的訊息表條目；讀目錄失敗沒有對應代碼，回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            LayoutError::NotInstallDir { .. } => Some(&messages::VK0028),
            LayoutError::Nested { .. } => Some(&messages::VK0029),
            LayoutError::Io { .. } => None,
        }
    }
}

impl fmt::Display for LayoutError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            LayoutError::NotInstallDir { cwd, .. } => {
                write!(f, "{} is not an install directory", cwd.display())
            }
            LayoutError::Nested { existing } => {
                write!(f, "{} is already an install directory", existing.display())
            }
            LayoutError::Io { path, source } => write!(f, "{}: {source}", path.display()),
        }
    }
}

impl std::error::Error for LayoutError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            LayoutError::Io { source, .. } => Some(source),
            _ => None,
        }
    }
}

/// 組路徑時名字不合法的是哪一段。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum NameKind {
    /// 工具名 `<repo>`。
    Repo,
    /// 進度檔的 `<verb>`。
    Verb,
    /// 進度檔的 `<id>`。
    Id,
}

/// 名字不是單一路徑段（空字串、`.`、`..`、含 `/` 或 NUL），或進度檔的名字含 `.`。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InvalidName {
    pub kind: NameKind,
    pub name: String,
}

impl InvalidName {
    fn new(kind: NameKind, name: &str) -> Self {
        Self {
            kind,
            name: name.to_owned(),
        }
    }
}

impl fmt::Display for InvalidName {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "invalid {:?} name {:?}", self.kind, self.name)
    }
}

impl std::error::Error for InvalidName {}

fn check_segment(name: &str, kind: NameKind) -> Result<(), InvalidName> {
    if name.is_empty() || name == "." || name == ".." || name.contains(['/', '\0']) {
        Err(InvalidName::new(kind, name))
    } else {
        Ok(())
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;
    use std::os::unix::fs::symlink;

    /// 在 `root` 底下建出各個相對路徑的目錄。
    fn tree(root: &Path, dirs: &[&str]) {
        for d in dirs {
            fs::create_dir_all(root.join(d)).unwrap();
        }
    }

    #[test]
    fn paths_under_vendor_kit() {
        let d = InstallDir::new("/r/app");
        assert_eq!(d.root(), Path::new("/r/app"));
        assert_eq!(d.vk_dir(), Path::new("/r/app/.vendor_kit"));
        assert_eq!(
            d.version_toml(),
            Path::new("/r/app/.vendor_kit/version.toml")
        );
        assert_eq!(
            d.version_local_toml(),
            Path::new("/r/app/.vendor_kit/version.local.toml")
        );
        assert_eq!(d.config_toml(), Path::new("/r/app/.vendor_kit/config.toml"));
        assert_eq!(d.cache_dir(), Path::new("/r/app/.vendor_kit/cache"));
        assert_eq!(
            d.tool_cache("ros_kit").unwrap(),
            Path::new("/r/app/.vendor_kit/cache/ros_kit")
        );
        assert_eq!(
            d.tool_stamp("ros_kit"),
            Path::new("/r/app/.vendor_kit/cache/ros_kit.stamp.toml")
        );
        assert_eq!(d.gen_dir(), Path::new("/r/app/.vendor_kit/gen"));
        assert_eq!(d.stamp(), Path::new("/r/app/.vendor_kit/gen/.stamp"));
        assert_eq!(d.log_dir(), Path::new("/r/app/.vendor_kit/log"));
        assert_eq!(d.baseline_dir(), Path::new("/r/app/.vendor_kit/baseline"));
        assert_eq!(
            d.baseline_vk(),
            Path::new("/r/app/.vendor_kit/baseline/.vendor_kit.toml")
        );
        assert_eq!(
            d.tool_metadata("docker").unwrap(),
            Path::new("/r/app/.vendor_kit/baseline/docker.toml")
        );
        assert_eq!(
            d.config_baseline(),
            Path::new("/r/app/.vendor_kit/baseline/.vendor_kit/config.toml")
        );
        assert_eq!(d.gitignore(), Path::new("/r/app/.vendor_kit/.gitignore"));
        assert_eq!(
            d.progress_file("add", "42").unwrap(),
            Path::new("/r/app/.vendor_kit/.tmp.add.42.toml")
        );
    }

    #[test]
    fn shell_files_are_the_four_files() {
        let d = InstallDir::new("/r");
        assert_eq!(
            d.shell_files(),
            [
                PathBuf::from("/r/.vendor_kit/entry.just"),
                PathBuf::from("/r/.vendor_kit/vendor.just"),
                PathBuf::from("/r/.vendor_kit/log.sh"),
                PathBuf::from("/r/.vendor_kit/.gitignore"),
            ]
        );
        assert!(d.shell_files().contains(&d.gitignore()));
    }

    #[test]
    fn names_cannot_escape_their_directory() {
        let d = InstallDir::new("/r");
        for bad in ["", ".", "..", "a/b", "../x", "a\0b"] {
            assert_eq!(
                d.tool_cache(bad),
                Err(InvalidName::new(NameKind::Repo, bad)),
                "{bad:?}"
            );
        }
        for bad in ["", ".", "..", ".vendor_kit", "a/b", "a\0b"] {
            assert_eq!(
                d.tool_metadata(bad),
                Err(InvalidName::new(NameKind::Repo, bad)),
                "{bad:?}"
            );
        }
        assert_eq!(
            d.progress_file("a.b", "1"),
            Err(InvalidName::new(NameKind::Verb, "a.b"))
        );
        assert_eq!(
            d.progress_file("add", "1.2"),
            Err(InvalidName::new(NameKind::Id, "1.2"))
        );
        assert_eq!(
            d.progress_file("add", ".."),
            Err(InvalidName::new(NameKind::Id, ".."))
        );
        assert_eq!(
            d.progress_file("", "1"),
            Err(InvalidName::new(NameKind::Verb, ""))
        );
    }

    #[test]
    fn install_dir_needs_a_real_vendor_kit_directory() {
        let t = tempfile::tempdir().unwrap();
        let root = t.path();
        tree(
            root,
            &[
                "yes/.vendor_kit",
                "no",
                "file",
                "link",
                "target/.vendor_kit",
            ],
        );
        fs::write(root.join("file/.vendor_kit"), "").unwrap();
        symlink(
            root.join("target/.vendor_kit"),
            root.join("link/.vendor_kit"),
        )
        .unwrap();

        assert!(is_install_dir(&root.join("yes")).unwrap());
        assert!(!is_install_dir(&root.join("no")).unwrap());
        assert!(!is_install_dir(&root.join("file")).unwrap());
        assert!(!is_install_dir(&root.join("link")).unwrap());
    }

    #[test]
    fn probe_tells_existing_from_fresh() {
        let t = tempfile::tempdir().unwrap();
        let root = t.path();
        tree(root, &["old/.vendor_kit", "new"]);

        let old = root.join("old");
        assert_eq!(probe(&old).unwrap(), Probe::Existing(InstallDir::new(&old)));
        let new = root.join("new");
        let p = probe(&new).unwrap();
        assert_eq!(p, Probe::Fresh(InstallDir::new(&new)));
        assert_eq!(p.dir().root(), new);
    }

    #[test]
    fn require_accepts_only_the_install_dir_itself() {
        let t = tempfile::tempdir().unwrap();
        let root = t.path();
        tree(root, &["app/.vendor_kit", "app/src/deep", "other"]);
        let app = root.join("app");

        assert_eq!(require(&app).unwrap(), InstallDir::new(&app));

        // 子目錄不算安裝目錄；提示指向最近的上層安裝目錄。
        let err = require(&app.join("src/deep")).unwrap_err();
        assert_eq!(err.message().map(|m| m.code), Some("VK0028"));
        match err {
            LayoutError::NotInstallDir { cwd, nearest } => {
                assert_eq!(cwd, app.join("src/deep"));
                assert_eq!(nearest, Some(app.clone()));
            }
            other => panic!("unexpected {other:?}"),
        }

        // 上層也沒有安裝目錄：沒有提示。
        match require(&root.join("other")).unwrap_err() {
            LayoutError::NotInstallDir { nearest, .. } => assert_eq!(nearest, None),
            other => panic!("unexpected {other:?}"),
        }
    }

    fn nested_at(target: &Path, repo: &Path) -> PathBuf {
        let err = check_nested(target, repo).unwrap_err();
        assert_eq!(err.message().map(|m| m.code), Some("VK0029"));
        match err {
            LayoutError::Nested { existing } => existing,
            other => panic!("unexpected {other:?}"),
        }
    }

    #[test]
    fn nested_finds_an_install_dir_above() {
        let t = tempfile::tempdir().unwrap();
        let repo = t.path().join("repo");
        tree(&repo, &[".vendor_kit", "a/.vendor_kit", "a/b/c"]);

        // 最近的上層先報。
        assert_eq!(nested_at(&repo.join("a/b/c"), &repo), repo.join("a"));
        // repo 根本身也算上層。
        tree(&repo, &["x/y"]);
        assert_eq!(nested_at(&repo.join("x/y"), &repo), repo.clone());
    }

    #[test]
    fn nested_does_not_look_above_the_repo_root() {
        let t = tempfile::tempdir().unwrap();
        let outer = t.path();
        tree(outer, &[".vendor_kit", "repo/app"]);
        let repo = outer.join("repo");
        check_nested(&repo.join("app"), &repo).unwrap();
        check_nested(&repo, &repo).unwrap();
    }

    #[test]
    fn nested_finds_an_install_dir_below_in_sorted_order() {
        let t = tempfile::tempdir().unwrap();
        let repo = t.path();
        tree(
            repo,
            &[
                "z/.vendor_kit",
                "b/deep/.vendor_kit",
                "b/deep/inner/.vendor_kit",
                "a/plain",
            ],
        );
        assert_eq!(nested_at(repo, repo), repo.join("b/deep"));
    }

    #[test]
    fn nested_ignores_own_vendor_kit_git_and_symlinks() {
        let t = tempfile::tempdir().unwrap();
        let base = t.path();
        let repo = base.join("repo");
        tree(
            &repo,
            &[
                ".vendor_kit/cache/tool/.vendor_kit",
                ".git/modules/x/.vendor_kit",
                "src",
            ],
        );
        tree(base, &["elsewhere/.vendor_kit"]);
        symlink(base.join("elsewhere"), repo.join("src/linked")).unwrap();

        // 未完成首次導入留下的 .vendor_kit/、.git 內部與 symlink 指到的目錄都不算。
        check_nested(&repo, &repo).unwrap();
    }

    #[test]
    fn unreadable_dir_is_an_io_error_without_a_code() {
        let t = tempfile::tempdir().unwrap();
        let missing = t.path().join("missing");
        let err = check_nested(&missing, t.path()).unwrap_err();
        assert!(matches!(err, LayoutError::Io { .. }), "{err:?}");
        assert!(err.message().is_none());
    }
}
