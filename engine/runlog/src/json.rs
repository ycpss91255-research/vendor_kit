//! 執行紀錄用的 JSON 子集：字串、非負與負整數、`null`、陣列、物件，沒有浮點數與布林。
//!
//! 語法的解析與字串的跳脫交給 serde_json，這裡只定子集與正規形：
//! - [`Value::write`] 產生唯一的正規形：不留空白、鍵依插入順序、字串照 [`escape`] 的固定跳脫。
//! - [`parse`] 照 JSON 語法讀進一個值：浮點數、布林、重複鍵、超出 i64 的整數一律不收，物件保留鍵序。
//!   它照語法接受空白與各種跳脫寫法，所以讀取端讀進來後要重新序列化，跟原行逐位元組相等才算合格；
//!   空白、跳脫寫法、整數寫法只要跟正規形不同，就讀不進來（ADR-0007:30 的讀取端只做字串比對）。

use std::fmt;
use std::io;

use serde::de::{self, Deserialize, Deserializer, MapAccess, SeqAccess, Visitor};
use serde::ser::Serializer as _;
use serde_json::ser::{CharEscape, Formatter, Serializer};

/// 一個 JSON 值；物件保留鍵的順序。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Value {
    Null,
    Int(i64),
    Str(String),
    Array(Vec<Value>),
    Object(Vec<(String, Value)>),
}

impl Value {
    pub fn str(s: impl Into<String>) -> Value {
        Value::Str(s.into())
    }

    /// 正規形：不留空白，字串的跳脫規則見 [`escape`]。
    pub fn write(&self, out: &mut String) {
        match self {
            Value::Null => out.push_str("null"),
            Value::Int(n) => out.push_str(&n.to_string()),
            Value::Str(s) => escape(s, out),
            Value::Array(items) => {
                out.push('[');
                for (i, item) in items.iter().enumerate() {
                    if i > 0 {
                        out.push(',');
                    }
                    item.write(out);
                }
                out.push(']');
            }
            Value::Object(members) => {
                out.push('{');
                for (i, (key, value)) in members.iter().enumerate() {
                    if i > 0 {
                        out.push(',');
                    }
                    escape(key, out);
                    out.push(':');
                    value.write(out);
                }
                out.push('}');
            }
        }
    }

    pub fn to_line(&self) -> String {
        let mut out = String::new();
        self.write(&mut out);
        out
    }
}

/// 字串的正規跳脫（ADR-0012:22 逐項 JSON 跳脫）：`"`、`\`、`\n`、`\r`、`\t` 用短寫，
/// 其他 U+0000–U+001F 與 U+007F 寫成 `\u00xx`（小寫十六進位），其餘字元照 UTF-8 原樣寫。
///
/// 要跳脫哪些字元由 serde_json 判定，寫法由 [`Canonical`] 定；跟 serde_json 預設不同的是
/// U+0008、U+000C 不用短寫，以及 U+007F 也要跳脫（啟動器的 `launcher/log.sh` 寫同一種正規形）。
pub fn escape(s: &str, out: &mut String) {
    let mut buf = Vec::with_capacity(s.len() + 2);
    let mut ser = Serializer::with_formatter(&mut buf, Canonical);
    match (&mut ser).serialize_str(s) {
        Ok(()) => {}
        Err(_) => unreachable!("writing into a Vec does not fail"),
    }
    match String::from_utf8(buf) {
        Ok(text) => out.push_str(&text),
        Err(_) => unreachable!("serde_json writes valid UTF-8"),
    }
}

/// [`escape`] 的寫法：其他方法沿用 serde_json 的緊湊格式（不留空白）。
struct Canonical;

impl Formatter for Canonical {
    fn write_string_fragment<W>(&mut self, writer: &mut W, fragment: &str) -> io::Result<()>
    where
        W: ?Sized + io::Write,
    {
        // serde_json 不跳脫 U+007F，這裡補上；U+007F 是單一位元組，切開不會切斷 UTF-8。
        for (i, part) in fragment.split('\u{7f}').enumerate() {
            if i > 0 {
                writer.write_all(b"\\u007f")?;
            }
            writer.write_all(part.as_bytes())?;
        }
        Ok(())
    }

    fn write_char_escape<W>(&mut self, writer: &mut W, char_escape: CharEscape) -> io::Result<()>
    where
        W: ?Sized + io::Write,
    {
        let short: &[u8] = match char_escape {
            CharEscape::Quote => b"\\\"",
            CharEscape::ReverseSolidus => b"\\\\",
            CharEscape::LineFeed => b"\\n",
            CharEscape::CarriageReturn => b"\\r",
            CharEscape::Tab => b"\\t",
            // serde_json 寫出時不跳脫 `/`，這個分支用不到；照正規形原樣寫。
            CharEscape::Solidus => b"/",
            CharEscape::Backspace => return write!(writer, "\\u0008"),
            CharEscape::FormFeed => return write!(writer, "\\u000c"),
            CharEscape::AsciiControl(byte) => return write!(writer, "\\u{byte:04x}"),
        };
        writer.write_all(short)
    }
}

/// 讀一個值；整串都要用完（結尾只容許空白），物件不准有重複鍵。正規形另由呼叫端比對。
pub fn parse(text: &str) -> Option<Value> {
    serde_json::from_str(text).ok()
}

impl<'de> Deserialize<'de> for Value {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Value, D::Error> {
        deserializer.deserialize_any(ValueVisitor)
    }
}

/// 只收子集裡的型別；沒實作的 visit（布林、浮點數）由 serde 回型別錯誤。
struct ValueVisitor;

impl<'de> Visitor<'de> for ValueVisitor {
    type Value = Value;

    fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result {
        f.write_str("null, an integer, a string, an array or an object")
    }

    fn visit_unit<E: de::Error>(self) -> Result<Value, E> {
        Ok(Value::Null)
    }

    fn visit_i64<E: de::Error>(self, n: i64) -> Result<Value, E> {
        Ok(Value::Int(n))
    }

    fn visit_u64<E: de::Error>(self, n: u64) -> Result<Value, E> {
        i64::try_from(n)
            .map(Value::Int)
            .map_err(|_| E::custom("integer out of range"))
    }

    fn visit_str<E: de::Error>(self, s: &str) -> Result<Value, E> {
        Ok(Value::str(s))
    }

    fn visit_string<E: de::Error>(self, s: String) -> Result<Value, E> {
        Ok(Value::Str(s))
    }

    fn visit_seq<A: SeqAccess<'de>>(self, mut seq: A) -> Result<Value, A::Error> {
        let mut items = Vec::new();
        while let Some(item) = seq.next_element()? {
            items.push(item);
        }
        Ok(Value::Array(items))
    }

    fn visit_map<A: MapAccess<'de>>(self, mut map: A) -> Result<Value, A::Error> {
        let mut members: Vec<(String, Value)> = Vec::new();
        while let Some(key) = map.next_key::<String>()? {
            if members.iter().any(|(k, _)| *k == key) {
                return Err(de::Error::custom("duplicate key"));
            }
            let value = map.next_value()?;
            members.push((key, value));
        }
        Ok(Value::Object(members))
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    fn line(v: &Value) -> String {
        v.to_line()
    }

    /// 讀進來且重新序列化跟原文相等，才算正規形（讀取端的判定）。
    fn canonical(text: &str) -> bool {
        parse(text).is_some_and(|v| line(&v) == text)
    }

    #[test]
    fn escapes_are_fixed() {
        let v = Value::str("a\"b\\c\nd\re\tf\u{1}g\u{7f}h中\u{8}\u{c}\u{1f}/\u{7f}\u{7f}");
        assert_eq!(
            line(&v),
            r#""a\"b\\c\nd\re\tf\u0001g\u007fh中\u0008\u000c\u001f/\u007f\u007f""#
        );
    }

    /// 與 `launcher/test/log.bats` 的跳脫測試用同一個字串、同一個結果。
    #[test]
    fn escapes_match_the_launcher() {
        let v = Value::str("q\"b\\ n\nr\rt\t\u{1}\u{1f}\u{7f} 中文 é");
        assert_eq!(line(&v), r#""q\"b\\ n\nr\rt\t\u0001\u001f\u007f 中文 é""#);
    }

    #[test]
    fn roundtrip_keeps_order() {
        let v = Value::Object(vec![
            ("b".into(), Value::Int(-3)),
            ("a".into(), Value::Array(vec![Value::Null, Value::str("x")])),
            ("c".into(), Value::Object(vec![])),
            ("d".into(), Value::Array(vec![])),
        ]);
        let text = line(&v);
        assert_eq!(text, r#"{"b":-3,"a":[null,"x"],"c":{},"d":[]}"#);
        assert_eq!(parse(&text), Some(v));
    }

    #[test]
    fn rejects_duplicates_types_and_trailing_text() {
        assert_eq!(parse(r#"{"a":1,"a":2}"#), None);
        assert_eq!(parse(r#"{"a":1}x"#), None);
        assert_eq!(parse(r#"{"a":1"#), None);
        assert_eq!(parse("\"a\u{1}\""), None);
        assert_eq!(parse("true"), None);
        assert_eq!(parse("1.5"), None);
        assert_eq!(parse("1.0"), None);
        assert_eq!(parse("9223372036854775808"), None);
        assert_eq!(parse(r#""\ud83d""#), None);
    }

    #[test]
    fn whitespace_is_not_canonical() {
        assert!(canonical(r#"{"a":1}"#));
        for text in [r#"{"a": 1}"#, r#" {"a":1}"#, "{\"a\":1}\n", "[1, 2]"] {
            assert!(parse(text).is_some(), "{text}");
            assert!(!canonical(text), "{text}");
        }
    }

    #[test]
    fn non_canonical_escapes_parse_but_do_not_roundtrip() {
        for (text, s) in [
            (r#""A\/""#, "A/"),
            (r#""\u0041""#, "A"),
            (r#""\b\f""#, "\u{8}\u{c}"),
            ("\"\u{7f}\"", "\u{7f}"),
            (r#""\u001F""#, "\u{1f}"),
        ] {
            assert_eq!(parse(text), Some(Value::str(s)), "{text}");
            assert!(!canonical(text), "{text}");
        }
        assert!(canonical(r#""😀""#));
        assert!(canonical(r#""\u0008\u000c\u007f""#));
    }

    #[test]
    fn non_canonical_ints_are_rejected() {
        for text in ["007", "-0", "1e2", "-"] {
            assert!(!canonical(text), "{text}");
        }
        assert!(canonical("-3"));
        assert!(canonical("0"));
    }
}
