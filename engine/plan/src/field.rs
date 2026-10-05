//! 自由文字欄 `fld`：`e:` 前綴加八進位跳脫（文法見 crate 文件）。

use std::fmt;

/// 文法裡的前綴；單獨的 `e:` 是空字串。
pub(crate) const PREFIX: &str = "e:";

/// 一個自由文字欄的值：任意位元組，不含 NUL。
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Field(Vec<u8>);

/// 自由文字欄寫不出來或讀不懂。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FieldError {
    /// 值含 NUL，寫不進 `fld`。
    Nul,
    /// 不是合法的 `fld`；帶原字串。
    Syntax(String),
}

impl fmt::Display for FieldError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            FieldError::Nul => f.write_str("free-text field contains NUL"),
            FieldError::Syntax(s) => write!(f, "invalid free-text field: {s:?}"),
        }
    }
}

impl std::error::Error for FieldError {}

/// 照原樣寫的位元組：0x21–0x7E，反斜線 0x5C 除外。
fn is_plain(b: u8) -> bool {
    (0x21..=0x7E).contains(&b) && b != b'\\'
}

impl Field {
    /// 收任意位元組；含 NUL 就回 [`FieldError::Nul`]。
    pub fn new(bytes: impl Into<Vec<u8>>) -> Result<Field, FieldError> {
        let bytes = bytes.into();
        if bytes.contains(&0) {
            return Err(FieldError::Nul);
        }
        Ok(Field(bytes))
    }

    /// 值的位元組。
    pub fn as_bytes(&self) -> &[u8] {
        &self.0
    }

    /// 寫成 `fld`：可讀 ASCII 照寫，其餘（含反斜線、空白）寫成 `\ooo`。同一個值只有這一種寫法。
    pub fn encode(&self) -> String {
        let mut out = String::with_capacity(PREFIX.len() + self.0.len());
        out.push_str(PREFIX);
        for &b in &self.0 {
            if is_plain(b) {
                out.push(char::from(b));
            } else {
                out.push('\\');
                for shift in [6u8, 3, 0] {
                    out.push(char::from(b'0' + ((b >> shift) & 0o7)));
                }
            }
        }
        out
    }

    /// 讀 `fld`：必須以 `e:` 開頭，跳脫只收三位八進位 001–377，反斜線必須跳脫。
    pub fn decode(s: &str) -> Result<Field, FieldError> {
        let err = || FieldError::Syntax(s.to_owned());
        let body = s.strip_prefix(PREFIX).ok_or_else(err)?.as_bytes();
        let mut out = Vec::with_capacity(body.len());
        let mut i = 0;
        while i < body.len() {
            let b = body[i];
            if is_plain(b) {
                out.push(b);
                i += 1;
                continue;
            }
            if b != b'\\' {
                return Err(err());
            }
            let digits = body.get(i + 1..i + 4).ok_or_else(err)?;
            let mut value: u16 = 0;
            for &d in digits {
                if !(b'0'..=b'7').contains(&d) {
                    return Err(err());
                }
                value = value * 8 + u16::from(d - b'0');
            }
            let byte = u8::try_from(value).map_err(|_| err())?;
            if byte == 0 {
                return Err(err());
            }
            out.push(byte);
            i += 4;
        }
        Ok(Field(out))
    }
}
