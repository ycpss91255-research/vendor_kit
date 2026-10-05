//! 執行紀錄用的 JSON 子集：字串、非負與負整數、`null`、陣列、物件，沒有浮點數與布林。
//!
//! 寫與讀共用同一份序列化：[`Value::write`] 產生唯一的正規形（不留空白、鍵依插入順序、
//! 跳脫規則固定），讀取端先 [`parse`] 再重新序列化，跟原行逐位元組相等才算合格。
//! 所以空白、跳脫寫法、整數寫法只要跟正規形不同，就讀不進來（ADR-0007:30 的讀取端只做字串比對）。

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

    /// 正規形：不留空白，跳脫規則見 [`escape`]。
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
pub fn escape(s: &str, out: &mut String) {
    out.push('"');
    for c in s.chars() {
        match c {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c if (c as u32) < 0x20 || c as u32 == 0x7f => {
                out.push_str(&format!("\\u{:04x}", c as u32));
            }
            c => out.push(c),
        }
    }
    out.push('"');
}

/// 讀一個值；整串都要用完，物件不准有重複鍵。不接受空白（正規形沒有空白）。
pub fn parse(text: &str) -> Option<Value> {
    let mut p = Parser {
        s: text.as_bytes(),
        i: 0,
    };
    let v = p.value()?;
    (p.i == p.s.len()).then_some(v)
}

struct Parser<'a> {
    s: &'a [u8],
    i: usize,
}

impl Parser<'_> {
    fn peek(&self) -> Option<u8> {
        self.s.get(self.i).copied()
    }

    fn eat(&mut self, b: u8) -> Option<()> {
        (self.peek()? == b).then(|| self.i += 1)
    }

    fn value(&mut self) -> Option<Value> {
        match self.peek()? {
            b'n' => {
                let rest = self.s.get(self.i..self.i + 4)?;
                (rest == b"null").then(|| {
                    self.i += 4;
                    Value::Null
                })
            }
            b'"' => self.string().map(Value::Str),
            b'[' => {
                self.i += 1;
                let mut items = Vec::new();
                if self.eat(b']').is_some() {
                    return Some(Value::Array(items));
                }
                loop {
                    items.push(self.value()?);
                    if self.eat(b']').is_some() {
                        return Some(Value::Array(items));
                    }
                    self.eat(b',')?;
                }
            }
            b'{' => {
                self.i += 1;
                let mut members: Vec<(String, Value)> = Vec::new();
                if self.eat(b'}').is_some() {
                    return Some(Value::Object(members));
                }
                loop {
                    let key = self.string()?;
                    if members.iter().any(|(k, _)| *k == key) {
                        return None;
                    }
                    self.eat(b':')?;
                    let value = self.value()?;
                    members.push((key, value));
                    if self.eat(b'}').is_some() {
                        return Some(Value::Object(members));
                    }
                    self.eat(b',')?;
                }
            }
            b'-' | b'0'..=b'9' => self.int(),
            _ => None,
        }
    }

    fn int(&mut self) -> Option<Value> {
        let start = self.i;
        if self.peek() == Some(b'-') {
            self.i += 1;
        }
        while self.peek().is_some_and(|b| b.is_ascii_digit()) {
            self.i += 1;
        }
        let text = std::str::from_utf8(&self.s[start..self.i]).ok()?;
        text.parse().ok().map(Value::Int)
    }

    fn hex4(&mut self) -> Option<u32> {
        let digits = self.s.get(self.i..self.i + 4)?;
        let text = std::str::from_utf8(digits).ok()?;
        let n = u32::from_str_radix(text, 16).ok()?;
        self.i += 4;
        Some(n)
    }

    fn string(&mut self) -> Option<String> {
        self.eat(b'"')?;
        let mut out = String::new();
        loop {
            // 一次吃一段沒有跳脫的 UTF-8。
            let start = self.i;
            while self
                .peek()
                .is_some_and(|b| b != b'"' && b != b'\\' && b >= 0x20)
            {
                self.i += 1;
            }
            out.push_str(std::str::from_utf8(&self.s[start..self.i]).ok()?);
            match self.peek()? {
                b'"' => {
                    self.i += 1;
                    return Some(out);
                }
                b'\\' => {
                    self.i += 1;
                    let b = self.peek()?;
                    self.i += 1;
                    let c = match b {
                        b'"' => '"',
                        b'\\' => '\\',
                        b'/' => '/',
                        b'b' => '\u{8}',
                        b'f' => '\u{c}',
                        b'n' => '\n',
                        b'r' => '\r',
                        b't' => '\t',
                        b'u' => {
                            let hi = self.hex4()?;
                            let code = if (0xd800..0xdc00).contains(&hi) {
                                self.eat(b'\\')?;
                                self.eat(b'u')?;
                                let lo = self.hex4()?;
                                if !(0xdc00..0xe000).contains(&lo) {
                                    return None;
                                }
                                0x10000 + ((hi - 0xd800) << 10) + (lo - 0xdc00)
                            } else {
                                hi
                            };
                            char::from_u32(code)?
                        }
                        _ => return None,
                    };
                    out.push(c);
                }
                // 字串裡的控制字元一定要跳脫。
                _ => return None,
            }
        }
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    fn line(v: &Value) -> String {
        v.to_line()
    }

    #[test]
    fn escapes_are_fixed() {
        let v = Value::str("a\"b\\c\nd\re\tf\u{1}g\u{7f}h中");
        assert_eq!(line(&v), r#""a\"b\\c\nd\re\tf\u0001g\u007fh中""#);
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
    fn rejects_whitespace_duplicates_and_trailing_text() {
        assert_eq!(parse(r#"{"a": 1}"#), None);
        assert_eq!(parse(r#"{"a":1,"a":2}"#), None);
        assert_eq!(parse(r#"{"a":1}x"#), None);
        assert_eq!(parse(r#"{"a":1"#), None);
        assert_eq!(parse("\"a\u{1}\""), None);
        assert_eq!(parse("true"), None);
        assert_eq!(parse("1.5"), None);
    }

    #[test]
    fn non_canonical_escapes_parse_but_do_not_roundtrip() {
        let v = parse(r#""A\/""#).unwrap();
        assert_eq!(v, Value::str("A/"));
        assert_ne!(line(&v), r#""A\/""#);
        assert_eq!(parse(r#""😀""#), Some(Value::str("😀")));
        assert_eq!(parse(r#""\ud83d""#), None);
    }

    #[test]
    fn non_canonical_ints_do_not_roundtrip() {
        for text in ["007", "-0"] {
            let v = parse(text).unwrap();
            assert_ne!(line(&v), text);
        }
        assert_eq!(parse("-"), None);
    }
}
