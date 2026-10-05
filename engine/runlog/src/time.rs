//! 時間戳：UTC ISO 8601、固定六位小數、`Z` 結尾（ADR-0012:20、#118），例如
//! `2026-10-05T01:02:03.000004Z`。固定寬度，讀取端可以直接驗形狀。

use std::time::{SystemTime, UNIX_EPOCH};

/// 格式化；早於 1970-01-01 的時間回 `None`（時鐘壞了，不寫出看似正常的時間）。
pub fn format(at: SystemTime) -> Option<String> {
    let d = at.duration_since(UNIX_EPOCH).ok()?;
    let secs = d.as_secs();
    let days = i64::try_from(secs / 86_400).ok()?;
    let rem = secs % 86_400;
    let (y, m, day) = civil_from_days(days);
    if y > 9999 {
        return None;
    }
    Some(format!(
        "{y:04}-{m:02}-{day:02}T{:02}:{:02}:{:02}.{:06}Z",
        rem / 3600,
        rem % 3600 / 60,
        rem % 60,
        d.subsec_micros()
    ))
}

/// 驗證是不是 [`format`] 寫得出來的形狀（日期與時間都要合法）。
pub fn is_valid(text: &str) -> bool {
    let b = text.as_bytes();
    if b.len() != 27 {
        return false;
    }
    let shape = b"dddd-dd-ddTdd:dd:dd.ddddddZ";
    for (c, s) in b.iter().zip(shape) {
        let ok = match s {
            b'd' => c.is_ascii_digit(),
            other => c == other,
        };
        if !ok {
            return false;
        }
    }
    let num = |r: std::ops::Range<usize>| -> u32 {
        b[r].iter().fold(0, |n, d| n * 10 + u32::from(d - b'0'))
    };
    let (y, m, d) = (num(0..4), num(5..7), num(8..10));
    let (hh, mm, ss) = (num(11..13), num(14..16), num(17..19));
    y >= 1970
        && (1..=12).contains(&m)
        && d >= 1
        && d <= days_in_month(y, m)
        && hh < 24
        && mm < 60
        && ss < 60
}

fn is_leap(y: u32) -> bool {
    (y.is_multiple_of(4) && !y.is_multiple_of(100)) || y.is_multiple_of(400)
}

fn days_in_month(y: u32, m: u32) -> u32 {
    match m {
        2 if is_leap(y) => 29,
        2 => 28,
        4 | 6 | 9 | 11 => 30,
        _ => 31,
    }
}

/// 1970-01-01 起算的天數 → (年, 月, 日)，公曆（H. Hinnant 的 civil_from_days）。
fn civil_from_days(z: i64) -> (i64, u32, u32) {
    let z = z + 719_468;
    let era = z.div_euclid(146_097);
    let doe = z.rem_euclid(146_097);
    let yoe = (doe - doe / 1460 + doe / 36_524 - doe / 146_096) / 365;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let d = (doy - (153 * mp + 2) / 5 + 1) as u32;
    let m = (if mp < 10 { mp + 3 } else { mp - 9 }) as u32;
    let y = yoe + era * 400 + i64::from(m <= 2);
    (y, m, d)
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;
    use std::time::Duration;

    fn at(secs: u64, micros: u32) -> String {
        format(UNIX_EPOCH + Duration::new(secs, micros * 1000)).unwrap()
    }

    #[test]
    fn known_instants() {
        assert_eq!(at(0, 0), "1970-01-01T00:00:00.000000Z");
        assert_eq!(at(1_791_162_123, 4), "2026-10-05T01:02:03.000004Z");
        // 閏日、年界、世紀閏年。
        assert_eq!(at(951_782_400, 0), "2000-02-29T00:00:00.000000Z");
        assert_eq!(at(1_709_164_800, 999_999), "2024-02-29T00:00:00.999999Z");
        assert_eq!(at(1_735_689_599, 0), "2024-12-31T23:59:59.000000Z");
        assert_eq!(at(1_735_689_600, 0), "2025-01-01T00:00:00.000000Z");
        assert_eq!(at(4_107_542_400, 0), "2100-03-01T00:00:00.000000Z");
    }

    #[test]
    fn sub_microsecond_is_truncated() {
        let t = UNIX_EPOCH + Duration::new(0, 1999);
        assert_eq!(format(t).unwrap(), "1970-01-01T00:00:00.000001Z");
    }

    #[test]
    fn before_epoch_is_refused() {
        assert_eq!(format(UNIX_EPOCH - Duration::from_secs(1)), None);
    }

    #[test]
    fn every_day_roundtrips_through_the_validator() {
        // 每一天的格式化結果都要過驗證，且日期連續遞增。
        let mut prev = String::new();
        for day in 0..(366 * 140) {
            let s = at(day * 86_400, 0);
            assert!(is_valid(&s), "{s}");
            assert!(s > prev, "{s}");
            prev = s;
        }
    }

    #[test]
    fn validator_rejects_bad_shapes() {
        for s in [
            "2026-10-05T01:02:03.00004Z",
            "2026-10-05T01:02:03.000004",
            "2026-10-05 01:02:03.000004Z",
            "2026-02-29T00:00:00.000000Z",
            "2026-13-01T00:00:00.000000Z",
            "2026-10-05T24:00:00.000000Z",
            "1969-12-31T23:59:59.000000Z",
            "2026-10-05T01:02:03.000004z",
        ] {
            assert!(!is_valid(s), "{s}");
        }
    }
}
