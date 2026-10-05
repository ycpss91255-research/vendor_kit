//! `.vendor_kit/config.toml` 的設定（04 設定）。
//!
//! - 檔是使用者維護的（04 使用者的檔與 VK 的檔），不是 VK 寫的 TOML，所以沒有 `schema` 與
//!   `written_by`，也不經 `schema` crate 的檔案版門檻（ADR-0008 只管 VK 寫的檔）。這裡只讀不寫。
//! - 頂層 `lock_timeout_seconds`、`lock_enabled` 與 `[test]` 的 `image`、`command` 是已知欄位；
//!   其他欄位一律忽略。檔不存在時全用預設值。
//! - 任一已知欄位的值無效就回 [`ConfigError::Invalid`]（VK0059），不以預設值繼續；所有入口
//!   都該停下。多個欄位無效時依上面的欄位順序回報第一個，結果固定。
//! - `[test]` 缺 `image` 或 `command` 不算無效：只有 `test <path>` 要 runner 時才報，見
//!   [`Config::runner`]。
//! - `lock_enabled = false` 時每次執行都要警告（VK0060），見 [`Config::lock_warning`]。
//!
//! 這裡不印診斷；要怎麼印由呼叫端經 `diagnostics` 決定，`<install_dir>` 也由呼叫端填。

use std::fmt;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

use layout::InstallDir;
use messages::Message;
use toml_edit::{DocumentMut, Item, TableLike, Value};

/// 等鎖期限的鍵。
pub const LOCK_TIMEOUT_KEY: &str = "lock_timeout_seconds";
/// 鎖開關的鍵。
pub const LOCK_ENABLED_KEY: &str = "lock_enabled";
/// test runner 的表名。
pub const TEST_KEY: &str = "test";
/// `[test]` 裡 runner image 的鍵。
pub const TEST_IMAGE_KEY: &str = "image";
/// `[test]` 裡 runner 指令的鍵。
pub const TEST_COMMAND_KEY: &str = "command";

/// 未設定時的等鎖秒數（04 設定）。
pub const DEFAULT_LOCK_TIMEOUT_SECONDS: u64 = 60;

/// 等鎖期限（`lock_timeout_seconds`）。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LockTimeout {
    /// `0`：取不到就不等。
    NoWait,
    /// `-1`：一直等。
    Forever,
    /// 正數：最多等這麼多秒。
    Seconds(u64),
}

impl Default for LockTimeout {
    fn default() -> Self {
        LockTimeout::Seconds(DEFAULT_LOCK_TIMEOUT_SECONDS)
    }
}

/// `test <path>` 用的 runner：兩個欄位都有，且都合法。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Runner {
    /// 跑測試的 image。
    pub image: String,
    /// 在 image 裡執行的指令與參數，至少一個元素。
    pub command: Vec<String>,
}

/// 讀進來的設定。已知欄位都已通過檢查；`[test]` 的欄位可能缺。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Config {
    lock_timeout: LockTimeout,
    lock_enabled: bool,
    /// `[test]` 不在時是 `None`。
    test: Option<TestSection>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct TestSection {
    image: Option<String>,
    command: Option<Vec<String>>,
}

impl Default for Config {
    /// 檔不存在或已知欄位都沒設時的設定。
    fn default() -> Self {
        Config {
            lock_timeout: LockTimeout::default(),
            lock_enabled: true,
            test: None,
        }
    }
}

impl Config {
    /// 讀安裝目錄的 `.vendor_kit/config.toml`；檔不存在時回預設值。
    pub fn load(dir: &InstallDir) -> Result<Config, ConfigError> {
        Config::load_path(&dir.config_toml())
    }

    /// 讀指定路徑的設定檔；檔不存在時回預設值。
    pub fn load_path(path: &Path) -> Result<Config, ConfigError> {
        match fs::read_to_string(path) {
            Ok(text) => Config::parse(&text),
            Err(e) if e.kind() == io::ErrorKind::NotFound => Ok(Config::default()),
            Err(source) => Err(ConfigError::Io {
                path: path.to_path_buf(),
                source,
            }),
        }
    }

    /// 解析設定檔內容：先過 TOML 語法，再依固定順序檢查已知欄位。
    pub fn parse(text: &str) -> Result<Config, ConfigError> {
        let doc: DocumentMut = text
            .parse()
            .map_err(|e: toml_edit::TomlError| ConfigError::Syntax(e.message().to_owned()))?;
        let root = doc.as_table();
        let lock_timeout = match present(root.get(LOCK_TIMEOUT_KEY)) {
            None => LockTimeout::default(),
            Some(item) => lock_timeout(item)?,
        };
        let lock_enabled = match present(root.get(LOCK_ENABLED_KEY)) {
            None => true,
            Some(item) => item
                .as_bool()
                .ok_or_else(|| Invalid::new(Field::LockEnabled, repr(item)))?,
        };
        let test = match present(root.get(TEST_KEY)) {
            None => None,
            Some(item) => Some(test_section(item)?),
        };
        Ok(Config {
            lock_timeout,
            lock_enabled,
            test,
        })
    }

    /// 等鎖期限；未設定時 60 秒。
    pub fn lock_timeout(&self) -> LockTimeout {
        self.lock_timeout
    }

    /// 要不要取鎖；未設定時 `true`。
    pub fn lock_enabled(&self) -> bool {
        self.lock_enabled
    }

    /// 鎖關掉時每次執行都要印的警告（VK0060）；鎖開著時是 `None`。
    pub fn lock_warning(&self) -> Option<&'static Message> {
        (!self.lock_enabled).then_some(&messages::VK0060)
    }

    /// `test <path>` 的 runner。缺 `[test]` 或其中必要欄位時回 VK0059，`<value>` 是 `missing`。
    /// 不帶 path 的 `test` 與其他入口不呼叫這個。
    pub fn runner(&self) -> Result<Runner, Invalid> {
        let test = self
            .test
            .as_ref()
            .ok_or_else(|| Invalid::missing(Field::Test))?;
        let image = test
            .image
            .clone()
            .ok_or_else(|| Invalid::missing(Field::TestImage))?;
        let command = test
            .command
            .clone()
            .ok_or_else(|| Invalid::missing(Field::TestCommand))?;
        Ok(Runner { image, command })
    }
}

/// `Item::None` 跟不在一樣。
fn present(item: Option<&Item>) -> Option<&Item> {
    item.filter(|i| !i.is_none())
}

fn lock_timeout(item: &Item) -> Result<LockTimeout, Invalid> {
    let bad = || Invalid::new(Field::LockTimeoutSeconds, repr(item));
    match item.as_integer().ok_or_else(bad)? {
        -1 => Ok(LockTimeout::Forever),
        0 => Ok(LockTimeout::NoWait),
        n if n > 0 => u64::try_from(n)
            .map(LockTimeout::Seconds)
            .map_err(|_| bad()),
        _ => Err(bad()),
    }
}

fn test_section(item: &Item) -> Result<TestSection, Invalid> {
    let table: &dyn TableLike = item
        .as_table_like()
        .ok_or_else(|| Invalid::new(Field::Test, repr(item)))?;
    let image = match present(table.get(TEST_IMAGE_KEY)) {
        None => None,
        Some(item) => Some(
            item.as_str()
                .filter(|s| !s.is_empty())
                .map(str::to_owned)
                .ok_or_else(|| Invalid::new(Field::TestImage, repr(item)))?,
        ),
    };
    let command = match present(table.get(TEST_COMMAND_KEY)) {
        None => None,
        Some(item) => {
            Some(command(item).ok_or_else(|| Invalid::new(Field::TestCommand, repr(item)))?)
        }
    };
    Ok(TestSection { image, command })
}

/// 由非空字串組成的非空陣列；不合就是 `None`。
fn command(item: &Item) -> Option<Vec<String>> {
    let array = item.as_array()?;
    if array.is_empty() {
        return None;
    }
    array
        .iter()
        .map(|v| v.as_str().filter(|s| !s.is_empty()).map(str::to_owned))
        .collect()
}

/// 填 `<value>` 用的原值：TOML 寫法，不含前後空白與註解。
fn repr(item: &Item) -> String {
    match item {
        Item::None => MISSING.to_owned(),
        Item::Value(v) => {
            let mut v: Value = v.clone();
            v.decor_mut().clear();
            v.to_string()
        }
        Item::Table(_) => "a table".to_owned(),
        Item::ArrayOfTables(_) => "an array of tables".to_owned(),
    }
}

/// 欄位不在時 `<value>` 印的字（VK0059）。
pub const MISSING: &str = "missing";

/// 設定檔裡的已知欄位，順序就是檢查與回報的順序。
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Field {
    LockTimeoutSeconds,
    LockEnabled,
    /// `[test]` 本身：不是表，或 `test <path>` 時不在。
    Test,
    TestImage,
    TestCommand,
}

impl Field {
    /// 填 `<field>` 的欄位名，寫法同訊息表。
    pub const fn name(self) -> &'static str {
        match self {
            Field::LockTimeoutSeconds => "lock_timeout_seconds",
            Field::LockEnabled => "lock_enabled",
            Field::Test => "[test]",
            Field::TestImage => "[test].image",
            Field::TestCommand => "[test].command",
        }
    }

    /// 填 `<fix>` 的修法；訊息輸出一律英文（04 輸出）。
    pub const fn fix(self) -> &'static str {
        match self {
            Field::LockTimeoutSeconds => {
                "use an integer greater than or equal to -1 (seconds to wait; 0 does not wait; -1 waits forever)"
            }
            Field::LockEnabled => "use a boolean (true or false)",
            Field::Test => "add a [test] table with image and command",
            Field::TestImage => "use a nonempty string",
            Field::TestCommand => "use a nonempty array of nonempty strings",
        }
    }
}

impl fmt::Display for Field {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.name())
    }
}

/// 一個無效的設定值（VK0059），帶著填訊息用的值。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Invalid {
    field: Field,
    value: String,
}

impl Invalid {
    fn new(field: Field, value: String) -> Self {
        Invalid { field, value }
    }

    fn missing(field: Field) -> Self {
        Invalid::new(field, MISSING.to_owned())
    }

    /// 對應的訊息表條目（VK0059）。
    pub fn message(&self) -> &'static Message {
        &messages::VK0059
    }

    /// 無效的欄位。
    pub fn field(&self) -> Field {
        self.field
    }

    /// 填 `<value>`：原值的 TOML 寫法，欄位不在時是 `missing`。
    pub fn value(&self) -> &str {
        &self.value
    }

    /// 填 `<fix>`。
    pub fn fix(&self) -> &'static str {
        self.field.fix()
    }
}

impl fmt::Display for Invalid {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} = {}: {}", self.field, self.value, self.fix())
    }
}

impl std::error::Error for Invalid {}

/// 讀設定失敗。
#[derive(Debug)]
pub enum ConfigError {
    /// 已知欄位的值無效（VK0059）。
    Invalid(Invalid),
    /// 不是合法的 TOML。訊息表還沒有對應代碼，先回 `None`。
    Syntax(String),
    /// 檔在但讀不到。訊息表沒有對應代碼，由呼叫端當內部錯誤處理。
    Io { path: PathBuf, source: io::Error },
}

impl ConfigError {
    /// 對應的訊息表條目；語法錯與讀檔失敗沒有代碼，回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            ConfigError::Invalid(e) => Some(e.message()),
            ConfigError::Syntax(_) | ConfigError::Io { .. } => None,
        }
    }
}

impl From<Invalid> for ConfigError {
    fn from(e: Invalid) -> Self {
        ConfigError::Invalid(e)
    }
}

impl fmt::Display for ConfigError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ConfigError::Invalid(e) => write!(f, "invalid configuration: {e}"),
            ConfigError::Syntax(m) => write!(f, "invalid TOML: {m}"),
            ConfigError::Io { path, source } => write!(f, "{}: {source}", path.display()),
        }
    }
}

impl std::error::Error for ConfigError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            ConfigError::Invalid(e) => Some(e),
            ConfigError::Syntax(_) => None,
            ConfigError::Io { source, .. } => Some(source),
        }
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    fn invalid(text: &str) -> Invalid {
        match Config::parse(text) {
            Err(ConfigError::Invalid(e)) => e,
            other => panic!("{text:?}: expected Invalid, got {other:?}"),
        }
    }

    #[test]
    fn empty_file_uses_defaults() {
        let c = Config::parse("").unwrap();
        assert_eq!(c, Config::default());
        assert_eq!(c.lock_timeout(), LockTimeout::Seconds(60));
        assert!(c.lock_enabled());
        assert_eq!(c.lock_warning(), None);
    }

    #[test]
    fn missing_file_uses_defaults() {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        assert_eq!(Config::load(&dir).unwrap(), Config::default());
    }

    #[test]
    fn load_reads_config_toml_under_vendor_kit() {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        fs::create_dir(dir.vk_dir()).unwrap();
        fs::write(dir.config_toml(), "lock_timeout_seconds = 5\n").unwrap();
        let c = Config::load(&dir).unwrap();
        assert_eq!(c.lock_timeout(), LockTimeout::Seconds(5));
    }

    #[test]
    fn unreadable_file_is_io_error_without_code() {
        let tmp = tempfile::tempdir().unwrap();
        let dir = InstallDir::new(tmp.path());
        fs::create_dir_all(dir.config_toml()).unwrap();
        let err = Config::load(&dir).unwrap_err();
        assert!(matches!(err, ConfigError::Io { .. }), "{err:?}");
        assert_eq!(err.message(), None);
    }

    #[test]
    fn lock_timeout_values() {
        for (text, want) in [
            ("lock_timeout_seconds = -1", LockTimeout::Forever),
            ("lock_timeout_seconds = 0", LockTimeout::NoWait),
            ("lock_timeout_seconds = 1", LockTimeout::Seconds(1)),
            ("lock_timeout_seconds = 3600", LockTimeout::Seconds(3600)),
        ] {
            assert_eq!(Config::parse(text).unwrap().lock_timeout(), want, "{text}");
        }
    }

    #[test]
    fn lock_timeout_must_be_integer_at_least_minus_one() {
        for (text, value) in [
            ("lock_timeout_seconds = -2", "-2"),
            ("lock_timeout_seconds = 60.0", "60.0"),
            ("lock_timeout_seconds = \"60\"", "\"60\""),
            ("lock_timeout_seconds = true", "true"),
            ("lock_timeout_seconds = [60]  # comment", "[60]"),
        ] {
            let e = invalid(text);
            assert_eq!(e.field(), Field::LockTimeoutSeconds, "{text}");
            assert_eq!(e.value(), value, "{text}");
        }
    }

    #[test]
    fn lock_disabled_warns_with_vk0060() {
        let c = Config::parse("lock_enabled = false").unwrap();
        assert!(!c.lock_enabled());
        let m = c.lock_warning().unwrap();
        assert_eq!(m.code, "VK0060");
        assert_eq!(m.exit_code(), 1);
        assert_eq!(
            Config::parse("lock_enabled = true").unwrap().lock_warning(),
            None
        );
    }

    #[test]
    fn lock_enabled_must_be_boolean() {
        for (text, value) in [
            ("lock_enabled = \"false\"", "\"false\""),
            ("lock_enabled = 0", "0"),
        ] {
            let e = invalid(text);
            assert_eq!(e.field(), Field::LockEnabled);
            assert_eq!(e.value(), value);
        }
    }

    #[test]
    fn test_runner_from_table_and_inline_table() {
        let want = Runner {
            image: "ghcr.io/o/r:v1".to_owned(),
            command: vec!["bats".to_owned(), "test".to_owned()],
        };
        for text in [
            "[test]\nimage = \"ghcr.io/o/r:v1\"\ncommand = [\"bats\", \"test\"]\n",
            "test = { image = \"ghcr.io/o/r:v1\", command = [\"bats\", \"test\"] }\n",
            "test.image = \"ghcr.io/o/r:v1\"\ntest.command = [\"bats\", \"test\"]\n",
        ] {
            assert_eq!(
                Config::parse(text).unwrap().runner().unwrap(),
                want,
                "{text}"
            );
        }
    }

    #[test]
    fn missing_runner_fields_fail_only_when_runner_is_asked() {
        let c = Config::parse("").unwrap();
        let e = c.runner().unwrap_err();
        assert_eq!((e.field(), e.value()), (Field::Test, MISSING));

        let c = Config::parse("[test]\ncommand = [\"x\"]\n").unwrap();
        let e = c.runner().unwrap_err();
        assert_eq!((e.field(), e.value()), (Field::TestImage, MISSING));

        let c = Config::parse("[test]\nimage = \"x\"\n").unwrap();
        let e = c.runner().unwrap_err();
        assert_eq!((e.field(), e.value()), (Field::TestCommand, MISSING));
        assert_eq!(e.message().code, "VK0059");
    }

    #[test]
    fn invalid_test_values_fail_on_load() {
        for (text, field, value) in [
            ("test = 1", Field::Test, "1"),
            ("[[test]]\nimage = \"x\"", Field::Test, "an array of tables"),
            ("[test]\nimage = \"\"", Field::TestImage, "\"\""),
            ("[test]\nimage = 1", Field::TestImage, "1"),
            ("[test]\ncommand = []", Field::TestCommand, "[]"),
            ("[test]\ncommand = \"bats\"", Field::TestCommand, "\"bats\""),
            (
                "[test]\ncommand = [\"bats\", \"\"]",
                Field::TestCommand,
                "[\"bats\", \"\"]",
            ),
            (
                "[test]\ncommand = [\"bats\", 1]",
                Field::TestCommand,
                "[\"bats\", 1]",
            ),
            ("[test.command]\nx = 1", Field::TestCommand, "a table"),
        ] {
            let e = invalid(text);
            assert_eq!((e.field(), e.value()), (field, value), "{text}");
        }
    }

    #[test]
    fn first_invalid_field_in_fixed_order_is_reported() {
        let e = invalid("[test]\nimage = 1\n");
        assert_eq!(e.field(), Field::TestImage);
        let text = "lock_enabled = 1\nlock_timeout_seconds = -5\n[test]\nimage = 1\n";
        assert_eq!(invalid(text).field(), Field::LockTimeoutSeconds);
    }

    #[test]
    fn unknown_fields_are_ignored() {
        let text = "schema = 9\nfuture = \"x\"\nlock_enabled = true\n[test]\nimage = \"i\"\ncommand = [\"c\"]\nenv = { A = \"1\" }\n[other]\nk = 1\n";
        let c = Config::parse(text).unwrap();
        assert!(c.lock_enabled());
        assert_eq!(c.runner().unwrap().image, "i");
    }

    #[test]
    fn invalid_message_fill_values() {
        let e = invalid("lock_enabled = \"no\"");
        assert_eq!(e.message().code, "VK0059");
        assert_eq!(e.message().exit_code(), 2);
        assert_eq!(e.field().name(), "lock_enabled");
        assert_eq!(e.value(), "\"no\"");
        assert_eq!(e.fix(), "use a boolean (true or false)");
        let err = ConfigError::from(e);
        assert_eq!(err.message().map(|m| m.code), Some("VK0059"));
    }

    #[test]
    fn syntax_error_has_no_code() {
        let err = Config::parse("lock_enabled = ").unwrap_err();
        assert!(matches!(err, ConfigError::Syntax(_)), "{err:?}");
        assert_eq!(err.message(), None);
    }
}
