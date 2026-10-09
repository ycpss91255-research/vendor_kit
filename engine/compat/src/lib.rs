//! 介面版、最低介面版與檔案版的判定（ADR-0008）。
//!
//! - 介面版 P：薄殼與引擎之間公開介面的整數版號。引擎接受 `[floor, current]` 區間內的呼叫，
//!   並以呼叫方那個 P 回應。
//! - 檔案版：VK 寫的每個 TOML 的 `schema` 欄。讀取門檻只看它；`written_by` 只供回報。
//!   檔案版高於本引擎上限就拒絕（VK0008）。
//! - 引擎降版：目標引擎的檔案版上限讀不了現有檔時拒絕（VK0007）。
//!
//! 新舊一律以整數比，不比 release 版本字串。這裡只做判定，不讀檔、不印診斷；
//! 要不要印、怎麼印由呼叫端經 `diagnostics` 決定。

use std::fmt;

use messages::Message;

/// 一個引擎版本的相容範圍：接受的介面版區間與讀得了的檔案版上限。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Compat {
    /// 最低介面版 floor；只能經 ADR 提高（ADR-0008）。
    pub floor_protocol: u32,
    /// 目前介面版 P。
    pub current_protocol: u32,
    /// 讀得了的最高檔案版，也是這個引擎寫入時記的檔案版。
    pub max_schema: u32,
}

/// 本引擎的相容範圍。
pub const THIS: Compat = Compat {
    floor_protocol: 1,
    current_protocol: 2,
    max_schema: 1,
};

// 本引擎的常數在編譯期就得自洽：版號從 1 起算，floor 不高於目前介面版。
const _: () = {
    assert!(THIS.floor_protocol >= 1);
    assert!(THIS.floor_protocol <= THIS.current_protocol);
    assert!(THIS.max_schema >= 1);
};

/// 引擎版本 `v<X.Y.Z>`，取自 Cargo workspace version；與版本行、tag 的寫法一致。
pub const ENGINE_VERSION: &str = concat!("v", env!("CARGO_PKG_VERSION"));

/// 建引擎 image 時帶給 `image/Dockerfile` 的 build-arg，一行一個 `NAME=value`，順序固定。
///
/// 最終 stage 把它們寫成 LABEL（`vendor_kit.protocol.floor`、`vendor_kit.protocol.current`、
/// `vendor_kit.schema.max`、`org.opencontainers.image.version`）。啟動器讀介面版區間判介面版
/// （ADR-0008:27）；檔案版上限只公告，供判引擎降版（VK0007）與比對兩平台的 LABEL。
/// 值只從 [`THIS`] 與 [`ENGINE_VERSION`] 來，Dockerfile 不另寫數字。
pub fn image_build_args() -> String {
    format!(
        "VK_PROTOCOL_FLOOR={}\nVK_PROTOCOL_CURRENT={}\nVK_SCHEMA_MAX={}\nVK_VERSION={}\n",
        THIS.floor_protocol, THIS.current_protocol, THIS.max_schema, ENGINE_VERSION
    )
}

impl Compat {
    /// 接受的介面版列表：`[floor, current]` 逐一展開、由小到大、以一個空白分隔（例如 `"2 3 4"`）。
    /// `version.toml` 的引擎鎖定行旁記這一串，啟動器離線逐項做字串相等比對（N13）。
    pub fn protocol_list(&self) -> String {
        (self.floor_protocol..=self.current_protocol)
            .map(|p| p.to_string())
            .collect::<Vec<_>>()
            .join(" ")
    }

    /// 呼叫方的 P 落在 `[floor, current]` 內就接受，回傳引擎回應時用的 P（就是呼叫方的 P）。
    pub fn accept_protocol(&self, protocol: u32) -> Result<u32, ProtocolError> {
        if (self.floor_protocol..=self.current_protocol).contains(&protocol) {
            Ok(protocol)
        } else {
            Err(ProtocolError {
                given: protocol,
                floor: self.floor_protocol,
                current: self.current_protocol,
            })
        }
    }

    /// 讀取門檻：檔案版不高於上限就讀得了；高於上限回 [`SchemaTooNew`]（VK0008）。
    pub fn check_schema(&self, schema: u32) -> Result<(), SchemaTooNew> {
        if schema <= self.max_schema {
            Ok(())
        } else {
            Err(SchemaTooNew {
                found: schema,
                max: self.max_schema,
            })
        }
    }

    /// 引擎降版前的判定（VK0007）：`self` 是目標引擎，`existing_schema` 是現有 VK 檔中最高的檔案版。
    /// 目標引擎讀得了才回 `Ok`；同一個 X 之內新增欄位不提高檔案版，未知欄位讀時忽略、寫時保留，
    /// 所以檔案版不高於目標上限就能無損讀取。
    pub fn check_downgrade(&self, existing_schema: u32) -> Result<(), DowngradeBlocked> {
        if existing_schema <= self.max_schema {
            Ok(())
        } else {
            Err(DowngradeBlocked {
                target_protocol: self.current_protocol,
                target_max_schema: self.max_schema,
                existing_schema,
            })
        }
    }
}

/// 呼叫方的 P 不在引擎接受的區間內。
///
/// 低於 floor 是 VK0009（舊薄殼）；高於上限還沒有對應的代碼（計畫缺口 G6），所以這裡沒有 `message()`，
/// 由呼叫端依方向選診斷（engine/vendor_kit 的 cli）；補上代碼後再接。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ProtocolError {
    pub given: u32,
    pub floor: u32,
    pub current: u32,
}

impl fmt::Display for ProtocolError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "interface version {} is outside the supported range [{}, {}]",
            self.given, self.floor, self.current
        )
    }
}

impl std::error::Error for ProtocolError {}

/// 檔案版高於本引擎上限（VK0008）。`<file>` 與 `<written_by>` 由讀檔的一方填。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SchemaTooNew {
    /// 檔裡的檔案版，填 `<N>`。
    pub found: u32,
    /// 本引擎的上限，填 `<M>`。
    pub max: u32,
}

impl SchemaTooNew {
    /// 對應的訊息表條目（VK0008）。
    pub fn message(&self) -> &'static Message {
        &messages::VK0008
    }
}

impl fmt::Display for SchemaTooNew {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "schema version {} is newer than the maximum supported version {}",
            self.found, self.max
        )
    }
}

impl std::error::Error for SchemaTooNew {}

/// 降版的目標引擎讀不了現有檔（VK0007）。`<vY>` 由呼叫端填目標 tag。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct DowngradeBlocked {
    /// 目標引擎的介面版，填 `<P>`。
    pub target_protocol: u32,
    /// 目標引擎的檔案版上限，填 `<M>`。
    pub target_max_schema: u32,
    /// 現有檔的檔案版，填 `<N>`。
    pub existing_schema: u32,
}

impl DowngradeBlocked {
    /// 對應的訊息表條目（VK0007）。
    pub fn message(&self) -> &'static Message {
        &messages::VK0007
    }
}

impl fmt::Display for DowngradeBlocked {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "target engine (interface version {}, schema version {}) cannot read schema version {}",
            self.target_protocol, self.target_max_schema, self.existing_schema
        )
    }
}

impl std::error::Error for DowngradeBlocked {}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    const ENGINE: Compat = Compat {
        floor_protocol: 2,
        current_protocol: 4,
        max_schema: 3,
    };

    #[test]
    fn image_build_args_come_from_this_engine() {
        assert_eq!(
            image_build_args(),
            format!(
                "VK_PROTOCOL_FLOOR={}\nVK_PROTOCOL_CURRENT={}\nVK_SCHEMA_MAX={}\nVK_VERSION=v{}\n",
                THIS.floor_protocol,
                THIS.current_protocol,
                THIS.max_schema,
                env!("CARGO_PKG_VERSION")
            )
        );
    }

    #[test]
    fn protocol_list_expands_the_range() {
        assert_eq!(ENGINE.protocol_list(), "2 3 4");
        let one = Compat {
            floor_protocol: 1,
            current_protocol: 1,
            max_schema: 1,
        };
        assert_eq!(one.protocol_list(), "1");
    }

    #[test]
    fn this_engine_accepts_its_current_protocol() {
        assert_eq!(
            THIS.accept_protocol(THIS.current_protocol),
            Ok(THIS.current_protocol)
        );
    }

    #[test]
    fn protocol_inside_range_is_answered_with_callers_protocol() {
        for p in 2..=4 {
            assert_eq!(ENGINE.accept_protocol(p), Ok(p));
        }
    }

    #[test]
    fn protocol_outside_range_is_rejected() {
        for p in [0, 1, 5, u32::MAX] {
            let e = ENGINE.accept_protocol(p).unwrap_err();
            assert_eq!(
                e,
                ProtocolError {
                    given: p,
                    floor: 2,
                    current: 4
                }
            );
        }
    }

    #[test]
    fn schema_up_to_max_is_readable() {
        for n in 1..=3 {
            assert_eq!(ENGINE.check_schema(n), Ok(()));
        }
    }

    #[test]
    fn schema_above_max_maps_to_vk0008() {
        let e = ENGINE.check_schema(4).unwrap_err();
        assert_eq!(e, SchemaTooNew { found: 4, max: 3 });
        assert_eq!(e.message().code, "VK0008");
        assert_eq!(e.message().exit_code(), 3);
    }

    #[test]
    fn downgrade_allowed_when_target_reads_existing_files() {
        assert_eq!(ENGINE.check_downgrade(1), Ok(()));
        assert_eq!(ENGINE.check_downgrade(3), Ok(()));
    }

    #[test]
    fn downgrade_blocked_maps_to_vk0007() {
        let e = ENGINE.check_downgrade(5).unwrap_err();
        assert_eq!(
            e,
            DowngradeBlocked {
                target_protocol: 4,
                target_max_schema: 3,
                existing_schema: 5
            }
        );
        assert_eq!(e.message().code, "VK0007");
        assert_eq!(e.message().exit_code(), 3);
    }
}
