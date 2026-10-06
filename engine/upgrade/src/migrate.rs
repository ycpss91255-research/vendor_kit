//! VK 檔的檔案版升級（`upgrade --engine` 第二段；flow-engine-upgrade「檔案版直接遷移、不鏈式」）。
//!
//! 每一項遷移把某一個舊檔案版的檔「直接」升到本引擎的檔案版上限（[`compat::THIS`] 的 `max_schema`），不經過
//! 中間版本：新引擎出貨時，替每一個它還要接手的舊檔案版各寫一項。這一版的上限是 1，沒有更舊的檔案版，所以
//! [`MIGRATIONS`] 是空的，框架先就位（N45）。
//!
//! 這裡只做判定與換內容，不讀寫檔、不印診斷：輸入是檔案內容，輸出是要寫回的內容，寫入交給 `txn`。
//! `version.toml` 遷移後，呼叫端要以遷移後的內容重建 `version_file::LockFile`，交給 `txn` 的版本鎖定行那一步寫，
//! 否則那一步會用舊的內容蓋回去。

use compat::Compat;

/// 一項遷移：把檔案版 `from` 的檔直接升到本引擎的檔案版上限。
#[derive(Debug, Clone, Copy)]
pub struct Migration {
    /// 這一項接手的舊檔案版。
    pub from: u32,
    /// 輸入舊檔的內容與寫入者（`v<X.Y.Z>`），回升級後的完整內容；`schema` 要寫成目標檔案版。
    pub apply: fn(text: &str, written_by: &str) -> Result<String, String>,
}

/// 本引擎出貨的遷移；檔案版上限是 1，沒有更舊的檔案版。
pub const MIGRATIONS: &[Migration] = &[];

/// 一個檔判完的結果。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Outcome {
    /// 已是目標檔案版，不用寫。
    Current,
    /// 升好了：從哪個檔案版升上來，與要寫回的內容。
    Migrated { from: u32, text: String },
}

/// 把一個 VK 檔升到 `target` 的檔案版上限：已是就回 [`Outcome::Current`]；比上限舊就找 `from` 等於它的那一項
/// 直接升，升完的內容要能以 `target` 讀、檔案版正好是上限。讀不了、沒有對應的遷移、比上限新、升完不合，都回說明。
pub fn migrate(
    text: &str,
    target: &Compat,
    table: &[Migration],
    written_by: &str,
) -> Result<Outcome, String> {
    let any = Compat {
        max_schema: u32::MAX,
        ..*target
    };
    let from = schema::Document::parse_with(text, &any)
        .map_err(|e| e.to_string())?
        .schema();
    let to = target.max_schema;
    if from == to {
        return Ok(Outcome::Current);
    }
    if from > to {
        return Err(format!(
            "schema version {from} is newer than this engine's {to}"
        ));
    }
    let Some(m) = table.iter().find(|m| m.from == from) else {
        return Err(format!("no migration from schema version {from} to {to}"));
    };
    let out = (m.apply)(text, written_by)?;
    let doc = schema::Document::parse_with(&out, target)
        .map_err(|e| format!("the migration from schema version {from} wrote {e}"))?;
    if doc.schema() != to {
        return Err(format!(
            "the migration from schema version {from} wrote schema version {}, not {to}",
            doc.schema()
        ));
    }
    Ok(Outcome::Migrated { from, text: out })
}

#[cfg(test)]
mod tests {
    #![allow(clippy::unwrap_used)]

    use super::*;

    const TWO: Compat = Compat {
        floor_protocol: 1,
        current_protocol: 1,
        max_schema: 2,
    };

    /// 測試用：檔案版 1 直接升到 2，把 `old` 改名成 `new`，其餘原樣。
    fn one_to_two(text: &str, written_by: &str) -> Result<String, String> {
        Ok(text
            .replace("schema = 1", "schema = 2")
            .replace("old =", "new =")
            .replace(
                "written_by = \"v0.0.0\"",
                &format!("written_by = \"{written_by}\""),
            ))
    }

    fn broken(text: &str, _: &str) -> Result<String, String> {
        Ok(text.to_owned())
    }

    const TABLE: &[Migration] = &[Migration {
        from: 1,
        apply: one_to_two,
    }];

    #[test]
    fn this_engine_has_a_migration_for_every_older_schema() {
        // 上限是 1 時沒有更舊的檔案版；寫成 `(1..=max).filter` 免得空的區間被 clippy 擋下。
        let max = compat::THIS.max_schema;
        for from in (1..=max).filter(|n| *n < max) {
            assert!(
                MIGRATIONS.iter().any(|m| m.from == from),
                "no migration from schema version {from}"
            );
        }
        assert!(MIGRATIONS.iter().all(|m| m.from >= 1 && m.from < max));
    }

    #[test]
    fn a_current_file_is_left_alone() {
        let text = "schema = 1\nwritten_by = \"v0.0.0\"\n";
        assert_eq!(
            migrate(text, &compat::THIS, MIGRATIONS, "v1.0.0"),
            Ok(Outcome::Current)
        );
    }

    #[test]
    fn an_older_file_is_migrated_directly_and_keeps_unknown_fields() {
        let text = "schema = 1\nwritten_by = \"v0.0.0\"\nold = 1\nunknown = \"kept\"\n";
        assert_eq!(
            migrate(text, &TWO, TABLE, "v2.0.0"),
            Ok(Outcome::Migrated {
                from: 1,
                text: "schema = 2\nwritten_by = \"v2.0.0\"\nnew = 1\nunknown = \"kept\"\n"
                    .to_owned()
            })
        );
    }

    #[test]
    fn a_missing_migration_stops() {
        let text = "schema = 1\nwritten_by = \"v0.0.0\"\n";
        assert_eq!(
            migrate(text, &TWO, &[], "v2.0.0"),
            Err("no migration from schema version 1 to 2".to_owned())
        );
        // 不鏈式：只有 2→3 的時候，1 不會先升到 2 再升到 3。
        let three = Compat {
            max_schema: 3,
            ..TWO
        };
        let table = [Migration {
            from: 2,
            apply: one_to_two,
        }];
        assert_eq!(
            migrate(text, &three, &table, "v3.0.0"),
            Err("no migration from schema version 1 to 3".to_owned())
        );
    }

    #[test]
    fn a_migration_must_write_the_target_schema() {
        let text = "schema = 1\nwritten_by = \"v0.0.0\"\n";
        let table = [Migration {
            from: 1,
            apply: broken,
        }];
        assert_eq!(
            migrate(text, &TWO, &table, "v2.0.0"),
            Err("the migration from schema version 1 wrote schema version 1, not 2".to_owned())
        );
    }

    #[test]
    fn a_newer_or_unreadable_file_stops() {
        assert_eq!(
            migrate("schema = 3\n", &TWO, TABLE, "v2.0.0"),
            Err("schema version 3 is newer than this engine's 2".to_owned())
        );
        assert!(migrate("not toml [", &TWO, TABLE, "v2.0.0").is_err());
        assert!(migrate("written_by = \"v0.0.0\"\n", &TWO, TABLE, "v2.0.0").is_err());
    }
}
