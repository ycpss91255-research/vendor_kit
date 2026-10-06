//! 訊息表（`doc/contract/reason_codes.csv`）在引擎內的樣子。
//!
//! 一列的型別 [`Message`] 寫在這裡，各欄的型別（[`Level`]、[`Disposition`]、[`Source`]）
//! 跟 `msggen` 共用，定義在 `message_types`，這裡 re-export；每個使用中代碼的常數由 `msggen`
//! 產生在 `generated.rs`，不要手改那個檔，改 CSV 後重跑 `msggen`。

#[rustfmt::skip]
mod generated;

pub use generated::*;
pub use message_types::{Disposition, Level, Source};

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
