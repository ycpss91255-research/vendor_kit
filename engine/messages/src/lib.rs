//! 訊息表（`doc/contract/reason_codes.csv`）在引擎內的樣子。
//!
//! 型別寫在這裡；每個使用中代碼的常數由 `msggen` 產生在 `generated.rs`，
//! 不要手改那個檔，改 CSV 後重跑 `msggen`。

#[rustfmt::skip]
mod generated;

pub use generated::*;

/// 診斷的嚴重度；`info` 不印成 stderr 的診斷，所以不在這裡（03 訊息）。
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Level {
    Warn,
    Error,
    Fatal,
}

impl Level {
    /// 嚴重度固定對應的結束碼（03 結束碼）。
    pub const fn exit_code(self) -> u8 {
        match self {
            Level::Warn => 1,
            Level::Error => 2,
            Level::Fatal => 3,
        }
    }

    /// 印在診斷第一行 `vendor_kit: <level>[VKnnnn]:` 裡的字。
    pub const fn as_str(self) -> &'static str {
        match self {
            Level::Warn => "warn",
            Level::Error => "error",
            Level::Fatal => "fatal",
        }
    }
}

/// 處置；warn 的列與用法錯誤留空，對應 `None`。
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Disposition {
    Pending,
    Failed,
}

/// 發出診斷的入口（訊息表 `source` 欄）。
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Source {
    Bootstrap,
    Engine,
    Launcher,
    Test,
}

/// 訊息表裡一列使用中的代碼。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Message {
    /// 原因代碼，例如 `VK0024`。
    pub code: &'static str,
    pub level: Level,
    pub disposition: Option<Disposition>,
    pub sources: &'static [Source],
    /// `message.en` 欄，逐字照印；多行時以 `\n` 分隔，占位符為 `<name>`。
    pub text: &'static str,
}

impl Message {
    pub const fn exit_code(&self) -> u8 {
        self.level.exit_code()
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    #[test]
    fn codes_are_unique_and_ascending() {
        let codes: Vec<&str> = ALL.iter().map(|m| m.code).collect();
        let mut sorted = codes.clone();
        sorted.sort_unstable();
        sorted.dedup();
        assert_eq!(codes, sorted);
    }

    #[test]
    fn no_command_message_matches_contract() {
        assert_eq!(VK0024.level, Level::Error);
        assert_eq!(VK0024.exit_code(), 2);
        assert_eq!(VK0024.disposition, None);
        assert_eq!(VK0024.text, "No command was specified.");
    }
}
