//! 訊息表（`doc/contract/reason_codes.csv`）各欄的型別：嚴重度、處置、發出來源。
//!
//! 產生器 `msggen` 讀表時用它，引擎的 `messages` 也用它（`generated.rs` 的常數經 `messages`
//! re-export 取用）；兩邊共用同一份定義，表的欄位值改了只改這裡（ADR-0014）。
//! 這裡只放型別，不讀表、不放代碼常數。

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

    /// 印在診斷第一行 `vendor_kit: <level>[VKnnnn]:` 裡的字，也是訊息表 `level` 欄的值。
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

/// 發出診斷的入口（訊息表 `source` 欄）；宣告順序就是該欄規定的固定順序。
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Source {
    Bootstrap,
    Engine,
    Launcher,
    Test,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn level_maps_to_exit_code_and_word() {
        assert_eq!(
            [Level::Warn, Level::Error, Level::Fatal].map(|l| (l.exit_code(), l.as_str())),
            [(1, "warn"), (2, "error"), (3, "fatal")]
        );
    }

    #[test]
    fn source_order_is_the_fixed_column_order() {
        assert!(Source::Bootstrap < Source::Engine);
        assert!(Source::Engine < Source::Launcher);
        assert!(Source::Launcher < Source::Test);
    }
}
