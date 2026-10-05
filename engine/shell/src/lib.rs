//! 薄殼：VK 放進安裝目錄、由使用者 commit 的四檔（GLOSSARY 的薄殼、自描述標頭）。
//!
//! - 薄殼四檔是 `.vendor_kit/` 下的 `entry.just`、`vendor.just`、`log.sh`、`.gitignore`（ADR-0007、
//!   04 寫入範圍與其他指令的關係）。檔名與順序只寫在 `layout`（[`layout::SHELL_FILES`]），這裡照用。
//! - 每檔開頭是自描述標頭：介面版、引擎版、其餘內容的 sha256，固定三行、固定順序：
//!
//!   ```text
//!   # vendor_kit-shell interface <介面版>
//!   # vendor_kit-shell engine <引擎版>
//!   # vendor_kit-shell sha256 <其餘內容的 sha256>
//!   ```
//!
//!   四檔都以 `#` 起頭的行為註解，所以標頭不改變各檔的意義。標頭固定放在第一行起，`log.sh` 由
//!   啟動器以 `bash` 執行或載入，不靠 shebang。每行都是 `<前綴><鍵> <值>\n`，啟動器（bash）不用解析器、
//!   以字串比對就讀得出介面版（不變量 6：啟動器只做不需要知道規則內容的事）。
//! - 產生（[`Shell::render`]）只依呼叫端給的介面版、引擎版與四檔模板本文，同樣的輸入每次得到位元組
//!   相同的內容，不放時間等會變的值；`--repair`「一致則不重產」靠這一點。介面版不寫死在這裡，由呼叫端
//!   傳入（ADR-0008 的介面版由引擎決定）；模板本文也由呼叫端給（模板隨 image 出貨，內容不在這個 crate）。
//! - 檢查（[`Shell::check`]）逐檔分兩段（ADR-0007 內部機制）：
//!   1. 用標頭重算比對：其餘內容的 sha256（原樣位元組，不做 CRLF 正規化，[`files::fingerprint`]）跟標頭
//!      記的不同，或標頭缺了、格式不對，就是被改過（[`Status::Modified`]）。
//!   2. 與這一版模板產生的內容整檔比對（含標頭）：自洽但位元組不同，就是不是這一版引擎的模板
//!      （[`Status::OtherTemplate`]）。標頭的 sha256 只涵蓋其餘內容，只改標頭裡引擎版的檔會過第一段，
//!      由這一段抓出來。
//!
//!   缺檔另列（[`Status::Missing`]）。任何一檔不是 [`Status::Match`]，對應 VK0006，`<files>` 逐檔標出
//!   是哪一種（[`Report::message`]、[`Status::as_str`]）。
//! - 寫入經 `files::write_atomic`：[`Shell::write`] 寫四檔（`install`、`upgrade --engine`），
//!   [`Shell::write_mismatched`] 只重產比對不符的檔（`bootstrap.sh --repair`）。`.vendor_kit/` 要已經在。
//! - 第一版禁止 symlink：薄殼檔是 symlink 或不是一般檔時，檢查回錯誤，不跟隨、不當成哪一種不符。
//!
//! 這裡只做產生、比對、寫檔，不決定何時檢查或重產（薄殼重產只由 `install`、`upgrade --engine` 與
//! `bootstrap.sh --repair` 做，ADR-0007），也不印診斷；要怎麼印由呼叫端經 `diagnostics` 決定。
//! 版本組合不合（VK0009）由啟動器在起引擎前判定，引擎升級未完成（VK0023）由呼叫端先看進度檔，都不在這裡。

use std::fmt;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

use layout::{InstallDir, SHELL_FILES};
use messages::Message;

/// 標頭每一行的前綴（含結尾空白）。
pub const HEADER_PREFIX: &str = "# vendor_kit-shell ";
/// 介面版的鍵。
pub const INTERFACE_KEY: &str = "interface";
/// 引擎版的鍵。
pub const ENGINE_KEY: &str = "engine";
/// 其餘內容 sha256 的鍵。
pub const SHA256_KEY: &str = "sha256";

/// 薄殼的檔數。
pub const FILE_COUNT: usize = SHELL_FILES.len();

// ---------------------------------------------------------------------------
// 標頭

/// 一個薄殼檔的自描述標頭。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Header {
    /// 介面版。
    pub interface: u32,
    /// 引擎版（原文，不解析）。
    pub engine: String,
    /// 其餘內容的 sha256，小寫十六進位 64 字元。
    pub sha256: String,
}

/// 由介面版、引擎版與其餘內容產生一個薄殼檔：標頭三行接著原樣的 `body`。
pub fn render(interface: u32, engine: &str, body: &[u8]) -> Result<Vec<u8>, InvalidEngine> {
    check_engine(engine)?;
    let sha256 = files::fingerprint(body).to_hex();
    let mut out = format!(
        "{HEADER_PREFIX}{INTERFACE_KEY} {interface}\n\
         {HEADER_PREFIX}{ENGINE_KEY} {engine}\n\
         {HEADER_PREFIX}{SHA256_KEY} {sha256}\n"
    )
    .into_bytes();
    out.extend_from_slice(body);
    Ok(out)
}

/// 拆出標頭與其餘內容；標頭缺了或格式不對回 `None`。不驗 sha256，驗用 [`is_intact`]。
pub fn parse(contents: &[u8]) -> Option<(Header, &[u8])> {
    let (interface, rest) = header_line(contents, INTERFACE_KEY)?;
    let (engine, rest) = header_line(rest, ENGINE_KEY)?;
    let (sha256, body) = header_line(rest, SHA256_KEY)?;
    let parsed: u32 = interface.parse().ok()?;
    if parsed.to_string() != interface {
        return None;
    }
    check_engine(engine).ok()?;
    if sha256.len() != 64
        || !sha256
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    {
        return None;
    }
    Some((
        Header {
            interface: parsed,
            engine: engine.to_owned(),
            sha256: sha256.to_owned(),
        },
        body,
    ))
}

/// 第一段：標頭在、格式對，而且其餘內容的 sha256 跟標頭記的相同。
pub fn is_intact(contents: &[u8]) -> bool {
    parse(contents).is_some_and(|(header, body)| files::fingerprint(body).to_hex() == header.sha256)
}

/// 讀一行 `<前綴><鍵> <值>\n`，回傳值與之後的內容。
fn header_line<'a>(contents: &'a [u8], key: &str) -> Option<(&'a str, &'a [u8])> {
    let end = contents.iter().position(|&b| b == b'\n')?;
    let line = std::str::from_utf8(&contents[..end]).ok()?;
    let value = line
        .strip_prefix(HEADER_PREFIX)?
        .strip_prefix(key)?
        .strip_prefix(' ')?;
    Some((value, &contents[end + 1..]))
}

/// 引擎版要能原樣放進標頭的一行：非空，沒有空白與控制字元。
fn check_engine(engine: &str) -> Result<(), InvalidEngine> {
    if engine.is_empty() || engine.chars().any(|c| c.is_whitespace() || c.is_control()) {
        return Err(InvalidEngine {
            engine: engine.to_owned(),
        });
    }
    Ok(())
}

// ---------------------------------------------------------------------------
// 薄殼四檔

/// 這一版引擎的薄殼四檔內容，順序同 [`layout::SHELL_FILES`]。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Shell {
    files: [Vec<u8>; FILE_COUNT],
}

impl Shell {
    /// 由介面版、引擎版與四檔模板本文（順序同 [`layout::SHELL_FILES`]）產生薄殼四檔的內容。
    pub fn render(
        interface: u32,
        engine: &str,
        bodies: [&[u8]; FILE_COUNT],
    ) -> Result<Shell, InvalidEngine> {
        check_engine(engine)?;
        let mut files: [Vec<u8>; FILE_COUNT] = Default::default();
        for (slot, body) in files.iter_mut().zip(bodies) {
            *slot = render(interface, engine, body)?;
        }
        Ok(Shell { files })
    }

    /// 各檔的檔名與內容，順序同 [`layout::SHELL_FILES`]。
    pub fn files(&self) -> impl Iterator<Item = (&'static str, &[u8])> {
        SHELL_FILES
            .into_iter()
            .zip(self.files.iter().map(Vec::as_slice))
    }

    /// 某一檔的內容；不是薄殼檔名回 `None`。
    pub fn file(&self, name: &str) -> Option<&[u8]> {
        self.files().find(|(n, _)| *n == name).map(|(_, c)| c)
    }

    /// 逐檔比對安裝目錄裡的薄殼與這一版的內容，不寫檔。
    pub fn check(&self, dir: &InstallDir) -> Result<Report, Error> {
        let mut findings = Vec::with_capacity(FILE_COUNT);
        for ((name, expected), path) in self.files().zip(dir.shell_files()) {
            let status = match read_regular(&path)? {
                None => Status::Missing,
                Some(actual) => classify(&actual, expected),
            };
            findings.push(Finding { name, status });
        }
        Ok(Report { findings })
    }

    /// 寫出四檔。
    pub fn write(&self, dir: &InstallDir) -> Result<(), Error> {
        for ((_, contents), path) in self.files().zip(dir.shell_files()) {
            files::write_atomic(&path, contents)?;
        }
        Ok(())
    }

    /// 只重產 `report` 裡不是 [`Status::Match`] 的檔，回傳重產了哪些檔名；全部一致時不寫檔。
    ///
    /// `report` 要是同一個 [`Shell`] 對同一個安裝目錄、剛做完的 [`Shell::check`]。
    pub fn write_mismatched(
        &self,
        dir: &InstallDir,
        report: &Report,
    ) -> Result<Vec<&'static str>, Error> {
        let mut written = Vec::new();
        for ((name, contents), path) in self.files().zip(dir.shell_files()) {
            let mismatched = report
                .findings
                .iter()
                .any(|f| f.name == name && f.status != Status::Match);
            if mismatched {
                files::write_atomic(&path, contents)?;
                written.push(name);
            }
        }
        Ok(written)
    }
}

/// 兩段比對一個在場的檔。
fn classify(actual: &[u8], expected: &[u8]) -> Status {
    if !is_intact(actual) {
        Status::Modified
    } else if actual != expected {
        Status::OtherTemplate
    } else {
        Status::Match
    }
}

/// 讀一般檔；不在回 `None`，symlink 或不是一般檔回錯誤。
fn read_regular(path: &Path) -> Result<Option<Vec<u8>>, Error> {
    let meta = match fs::symlink_metadata(path) {
        Ok(meta) => meta,
        Err(e) if e.kind() == io::ErrorKind::NotFound => return Ok(None),
        Err(source) => {
            return Err(Error::Io {
                file: path.to_path_buf(),
                source,
            });
        }
    };
    let ty = meta.file_type();
    if ty.is_symlink() {
        return Err(Error::Symlink {
            file: path.to_path_buf(),
        });
    }
    if !ty.is_file() {
        return Err(Error::NotRegular {
            file: path.to_path_buf(),
        });
    }
    match fs::read(path) {
        Ok(contents) => Ok(Some(contents)),
        Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(None),
        Err(source) => Err(Error::Io {
            file: path.to_path_buf(),
            source,
        }),
    }
}

// ---------------------------------------------------------------------------
// 比對結果

/// 一個薄殼檔的比對結果。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Status {
    /// 與這一版的內容位元組相同。
    Match,
    /// 檔不在。
    Missing,
    /// 被改過：標頭缺了、格式不對，或其餘內容跟標頭的 sha256 不符。
    Modified,
    /// 自洽，但不是這一版引擎的模板。
    OtherTemplate,
}

impl Status {
    /// 放進 VK0006 `<files>` 標出是哪一種時用的字。
    pub const fn as_str(self) -> &'static str {
        match self {
            Status::Match => "match",
            Status::Missing => "missing",
            Status::Modified => "modified",
            Status::OtherTemplate => "not this engine version's template",
        }
    }
}

impl fmt::Display for Status {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

/// 一檔的比對結果。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Finding {
    /// `.vendor_kit/` 下的檔名。
    pub name: &'static str,
    pub status: Status,
}

/// [`Shell::check`] 的結果，順序同 [`layout::SHELL_FILES`]。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Report {
    findings: Vec<Finding>,
}

impl Report {
    /// 每一檔的結果。
    pub fn findings(&self) -> &[Finding] {
        &self.findings
    }

    /// 不一致的檔。
    pub fn mismatches(&self) -> impl Iterator<Item = &Finding> {
        self.findings.iter().filter(|f| f.status != Status::Match)
    }

    /// 四檔都與這一版相同。
    pub fn is_consistent(&self) -> bool {
        self.mismatches().next().is_none()
    }

    /// 有不一致時對應 VK0006；全部一致回 `None`。`--repair` 不報這個診斷，由呼叫端決定。
    pub fn message(&self) -> Option<&'static Message> {
        if self.is_consistent() {
            None
        } else {
            Some(&messages::VK0006)
        }
    }
}

// ---------------------------------------------------------------------------
// 錯誤

/// 引擎版放不進標頭的一行（空字串，或含空白、控制字元）。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InvalidEngine {
    pub engine: String,
}

impl fmt::Display for InvalidEngine {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "engine version must be non-empty without whitespace or control characters: {:?}",
            self.engine
        )
    }
}

impl std::error::Error for InvalidEngine {}

/// 讀寫薄殼檔失敗。
#[derive(Debug)]
pub enum Error {
    /// 讀檔失敗。
    Io { file: PathBuf, source: io::Error },
    /// 薄殼檔是 symlink（第一版禁止）。
    Symlink { file: PathBuf },
    /// 薄殼檔不是一般檔。
    NotRegular { file: PathBuf },
    /// 寫檔失敗。
    Write(files::Error),
}

impl From<files::Error> for Error {
    fn from(e: files::Error) -> Self {
        Error::Write(e)
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Io { file, source } => write!(f, "read {}: {source}", file.display()),
            Error::Symlink { file } => write!(f, "symlink not allowed: {}", file.display()),
            Error::NotRegular { file } => write!(f, "not a regular file: {}", file.display()),
            Error::Write(e) => e.fmt(f),
        }
    }
}

impl std::error::Error for Error {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Error::Io { source, .. } => Some(source),
            Error::Write(e) => Some(e),
            Error::Symlink { .. } | Error::NotRegular { .. } => None,
        }
    }
}

// ---------------------------------------------------------------------------

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    const INTERFACE: u32 = 1;
    const ENGINE: &str = "ghcr.io/example/vendor_kit:v1.0.0";
    const BODIES: [&[u8]; FILE_COUNT] = [
        b"# entry\nimport? 'vendor.just'\n",
        b"# vendor\nmod vendor_kit\n",
        b"# log\nlog() { :; }\n",
        b"cache/\ngen/\nlog/\n",
    ];

    fn shell() -> Shell {
        Shell::render(INTERFACE, ENGINE, BODIES).unwrap()
    }

    fn install() -> (tempfile::TempDir, InstallDir) {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        fs::create_dir(dir.vk_dir()).unwrap();
        (tmp, dir)
    }

    fn statuses(report: &Report) -> Vec<(&'static str, Status)> {
        report
            .findings()
            .iter()
            .map(|f| (f.name, f.status))
            .collect()
    }

    fn only(report: &Report, name: &str, status: Status) {
        for f in report.findings() {
            let want = if f.name == name {
                status
            } else {
                Status::Match
            };
            assert_eq!(f.status, want, "{}", f.name);
        }
    }

    #[test]
    fn render_writes_header_then_body() {
        let out = render(INTERFACE, ENGINE, b"body\n").unwrap();
        let text = String::from_utf8(out).unwrap();
        let sha = files::fingerprint(b"body\n").to_hex();
        assert_eq!(
            text,
            format!(
                "# vendor_kit-shell interface 1\n\
                 # vendor_kit-shell engine {ENGINE}\n\
                 # vendor_kit-shell sha256 {sha}\n\
                 body\n"
            )
        );
    }

    #[test]
    fn render_is_deterministic() {
        assert_eq!(shell(), shell());
    }

    #[test]
    fn parse_reads_back_header() {
        let out = render(7, ENGINE, b"x").unwrap();
        let (header, body) = parse(&out).unwrap();
        assert_eq!(header.interface, 7);
        assert_eq!(header.engine, ENGINE);
        assert_eq!(header.sha256, files::fingerprint(b"x").to_hex());
        assert_eq!(body, b"x");
        assert!(is_intact(&out));
    }

    #[test]
    fn parse_rejects_malformed_headers() {
        let sha = files::fingerprint(b"").to_hex();
        for bad in [
            String::new(),
            "no header\n".to_owned(),
            format!("# vendor_kit-shell interface 01\n# vendor_kit-shell engine e\n# vendor_kit-shell sha256 {sha}\n"),
            format!("# vendor_kit-shell interface x\n# vendor_kit-shell engine e\n# vendor_kit-shell sha256 {sha}\n"),
            format!("# vendor_kit-shell engine e\n# vendor_kit-shell interface 1\n# vendor_kit-shell sha256 {sha}\n"),
            format!("# vendor_kit-shell interface 1\r\n# vendor_kit-shell engine e\n# vendor_kit-shell sha256 {sha}\n"),
            format!("# vendor_kit-shell interface 1\n# vendor_kit-shell engine e\n# vendor_kit-shell sha256 {}\n", sha.to_uppercase()),
            "# vendor_kit-shell interface 1\n# vendor_kit-shell engine e\n# vendor_kit-shell sha256 abc\n".to_owned(),
            format!("# vendor_kit-shell interface 1\n# vendor_kit-shell engine e\n# vendor_kit-shell sha256 {sha}"),
        ] {
            assert!(parse(bad.as_bytes()).is_none(), "{bad:?}");
        }
    }

    #[test]
    fn invalid_engine_is_rejected() {
        for bad in ["", "a b", "a\nb", "a\rb", "a\tb"] {
            assert!(render(INTERFACE, bad, b"").is_err(), "{bad:?}");
            assert!(Shell::render(INTERFACE, bad, BODIES).is_err(), "{bad:?}");
        }
    }

    #[test]
    fn untouched_shell_matches() {
        let (_tmp, dir) = install();
        let shell = shell();
        shell.write(&dir).unwrap();
        let report = shell.check(&dir).unwrap();
        assert!(report.is_consistent());
        assert_eq!(report.message(), None);
        assert_eq!(
            statuses(&report),
            SHELL_FILES.map(|n| (n, Status::Match)).to_vec()
        );
        for ((name, contents), path) in shell.files().zip(dir.shell_files()) {
            assert_eq!(fs::read(&path).unwrap(), contents, "{name}");
        }
    }

    #[test]
    fn one_changed_byte_in_body_is_modified() {
        let (_tmp, dir) = install();
        let shell = shell();
        shell.write(&dir).unwrap();
        let path = dir.vk_dir().join("vendor.just");
        let mut contents = fs::read(&path).unwrap();
        let last = contents.len() - 2;
        contents[last] ^= 1;
        fs::write(&path, contents).unwrap();
        let report = shell.check(&dir).unwrap();
        only(&report, "vendor.just", Status::Modified);
        assert_eq!(report.message().map(|m| m.code), Some("VK0006"));
    }

    #[test]
    fn crlf_only_change_is_modified() {
        let (_tmp, dir) = install();
        let shell = shell();
        shell.write(&dir).unwrap();
        let path = dir.gitignore();
        let text = String::from_utf8(fs::read(&path).unwrap()).unwrap();
        let (head, body) = text.split_at(text.len() - BODIES[3].len());
        fs::write(&path, format!("{head}{}", body.replace('\n', "\r\n"))).unwrap();
        only(&shell.check(&dir).unwrap(), ".gitignore", Status::Modified);
    }

    #[test]
    fn broken_header_is_modified() {
        let (_tmp, dir) = install();
        let shell = shell();
        shell.write(&dir).unwrap();
        fs::write(dir.vk_dir().join("log.sh"), BODIES[2]).unwrap();
        only(&shell.check(&dir).unwrap(), "log.sh", Status::Modified);
    }

    #[test]
    fn edited_engine_in_header_is_other_template() {
        let (_tmp, dir) = install();
        let shell = shell();
        shell.write(&dir).unwrap();
        let path = dir.vk_dir().join("entry.just");
        let text = String::from_utf8(fs::read(&path).unwrap()).unwrap();
        fs::write(&path, text.replace(":v1.0.0", ":v1.0.1")).unwrap();
        only(
            &shell.check(&dir).unwrap(),
            "entry.just",
            Status::OtherTemplate,
        );
    }

    #[test]
    fn shell_of_another_engine_is_other_template() {
        let (_tmp, dir) = install();
        Shell::render(INTERFACE, "ghcr.io/example/vendor_kit:v0.9.0", BODIES)
            .unwrap()
            .write(&dir)
            .unwrap();
        let report = shell().check(&dir).unwrap();
        assert_eq!(
            statuses(&report),
            SHELL_FILES.map(|n| (n, Status::OtherTemplate)).to_vec()
        );
    }

    #[test]
    fn other_interface_or_body_is_other_template() {
        let (_tmp, dir) = install();
        let mut bodies = BODIES;
        bodies[1] = b"# older vendor template\n";
        Shell::render(INTERFACE, ENGINE, bodies)
            .unwrap()
            .write(&dir)
            .unwrap();
        only(
            &shell().check(&dir).unwrap(),
            "vendor.just",
            Status::OtherTemplate,
        );

        Shell::render(INTERFACE + 1, ENGINE, BODIES)
            .unwrap()
            .write(&dir)
            .unwrap();
        let report = shell().check(&dir).unwrap();
        assert!(
            report
                .mismatches()
                .all(|f| f.status == Status::OtherTemplate)
        );
        assert_eq!(report.mismatches().count(), FILE_COUNT);
    }

    #[test]
    fn missing_file_is_missing() {
        let (_tmp, dir) = install();
        let shell = shell();
        shell.write(&dir).unwrap();
        fs::remove_file(dir.vk_dir().join("log.sh")).unwrap();
        only(&shell.check(&dir).unwrap(), "log.sh", Status::Missing);
    }

    #[test]
    fn symlink_or_directory_is_an_error() {
        let (_tmp, dir) = install();
        let shell = shell();
        shell.write(&dir).unwrap();
        let entry = dir.vk_dir().join("entry.just");
        fs::remove_file(&entry).unwrap();
        std::os::unix::fs::symlink(dir.vk_dir().join("vendor.just"), &entry).unwrap();
        assert!(matches!(shell.check(&dir), Err(Error::Symlink { .. })));

        fs::remove_file(&entry).unwrap();
        fs::create_dir(&entry).unwrap();
        assert!(matches!(shell.check(&dir), Err(Error::NotRegular { .. })));
    }

    #[test]
    fn write_mismatched_rewrites_only_mismatches() {
        let (_tmp, dir) = install();
        let shell = shell();
        shell.write(&dir).unwrap();
        let report = shell.check(&dir).unwrap();
        assert!(shell.write_mismatched(&dir, &report).unwrap().is_empty());

        fs::write(dir.vk_dir().join("vendor.just"), b"changed\n").unwrap();
        fs::remove_file(dir.gitignore()).unwrap();
        let report = shell.check(&dir).unwrap();
        let written = shell.write_mismatched(&dir, &report).unwrap();
        assert_eq!(written, vec!["vendor.just", ".gitignore"]);
        assert!(shell.check(&dir).unwrap().is_consistent());
    }

    #[test]
    fn file_looks_up_by_name() {
        let shell = shell();
        assert_eq!(
            shell.file("log.sh"),
            Some(render(INTERFACE, ENGINE, BODIES[2]).unwrap().as_slice())
        );
        assert_eq!(shell.file("other"), None);
    }
}
