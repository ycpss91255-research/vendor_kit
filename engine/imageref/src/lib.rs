//! tag、digest 與 image 引用。
//!
//! - tag：只收 `vX.Y.Z`，三個數值不收前導零，不帶 pre-release 或 build 後綴（04 指定版本）。
//! - 版本比較：X、Y、Z 當非負整數逐欄比數值；[`Tag`] 的 `Ord` 就是這個順序，
//!   不看字串順序（04 指定版本）。
//! - image 引用：`<registry>/<路徑>:<tag>@sha256:<digest>`（GLOSSARY 的 image 引用），
//!   registry 只收 GHCR（04 registry 與認證）。
//!
//! 錯誤一律回傳，這裡不印診斷。tag 格式錯誤是用法錯誤，[`TagError::message`] 對應 VK0027；
//! 要不要印、怎麼印由呼叫端經 `diagnostics` 決定。

use std::fmt;
use std::str::FromStr;

use messages::Message;

/// 唯一支援的 registry 主機（04 registry 與認證）。
pub const GHCR: &str = "ghcr.io";

/// 合法的 `vX.Y.Z` tag；欄位依宣告順序比較，所以 `Ord` 就是逐欄數值比較。
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Tag {
    pub major: u64,
    pub minor: u64,
    pub patch: u64,
}

/// tag 不是合法的 `vX.Y.Z`；帶著原本的輸入，給 VK0027 的 `<tag>`。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TagError {
    input: String,
}

impl TagError {
    /// 使用者給的原字串。
    pub fn input(&self) -> &str {
        &self.input
    }

    /// 對應的訊息表條目（VK0027，用法錯誤：tag 格式不合）。
    pub fn message(&self) -> &'static Message {
        &messages::VK0027
    }

    /// 訊息文字裡要填的佔位名稱，值是 [`TagError::input`]。
    pub const PLACEHOLDER: &'static str = "tag";
}

impl fmt::Display for TagError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "invalid tag format: {}", self.input)
    }
}

impl std::error::Error for TagError {}

impl Tag {
    /// 解析 `vX.Y.Z`；不合就回 [`TagError`]。
    pub fn parse(s: &str) -> Result<Tag, TagError> {
        let err = || TagError {
            input: s.to_owned(),
        };
        let rest = s.strip_prefix('v').ok_or_else(err)?;
        let mut fields = rest.split('.');
        let (Some(x), Some(y), Some(z), None) =
            (fields.next(), fields.next(), fields.next(), fields.next())
        else {
            return Err(err());
        };
        Ok(Tag {
            major: number(x).ok_or_else(err)?,
            minor: number(y).ok_or_else(err)?,
            patch: number(z).ok_or_else(err)?,
        })
    }

    /// 從一串 tag 取最新版；不合法的 tag 略過，一個合法的都沒有就回 `None`（04 `latest: none`）。
    pub fn latest<'a, I>(tags: I) -> Option<Tag>
    where
        I: IntoIterator<Item = &'a str>,
    {
        tags.into_iter().filter_map(|t| Tag::parse(t).ok()).max()
    }
}

/// 一個欄位：只有 ASCII 數字、非空、沒有前導零（`0` 本身可以），放得進 `u64`。
fn number(s: &str) -> Option<u64> {
    if s.is_empty() || !s.bytes().all(|b| b.is_ascii_digit()) {
        return None;
    }
    if s.len() > 1 && s.starts_with('0') {
        return None;
    }
    s.parse().ok()
}

impl FromStr for Tag {
    type Err = TagError;

    fn from_str(s: &str) -> Result<Tag, TagError> {
        Tag::parse(s)
    }
}

impl fmt::Display for Tag {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "v{}.{}.{}", self.major, self.minor, self.patch)
    }
}

/// image 內容的 sha256：64 個小寫十六進位字元，不含 `sha256:` 前綴。
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Digest(String);

impl Digest {
    /// 解析 `sha256:<64 個小寫十六進位>`。
    pub fn parse(s: &str) -> Option<Digest> {
        let hex = s.strip_prefix("sha256:")?;
        let ok = hex.len() == 64 && hex.bytes().all(|b| matches!(b, b'0'..=b'9' | b'a'..=b'f'));
        ok.then(|| Digest(hex.to_owned()))
    }

    /// 不含 `sha256:` 的十六進位字串。
    pub fn hex(&self) -> &str {
        &self.0
    }
}

impl fmt::Display for Digest {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "sha256:{}", self.0)
    }
}

/// image 引用解析失敗的原因。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ImageRefError {
    /// 缺 `@sha256:<digest>`，或 digest 不是 64 個小寫十六進位字元。
    Digest,
    /// 缺 `:<tag>`。
    MissingTag,
    /// tag 不是合法的 `vX.Y.Z`。
    Tag(TagError),
    /// registry 不是 GHCR（含沒寫 registry 的情形）；帶著讀到的 registry。
    UnsupportedRegistry(String),
    /// 路徑是空的，或某一段不合 registry 的路徑規則。
    Path,
}

impl fmt::Display for ImageRefError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ImageRefError::Digest => f.write_str("missing or invalid @sha256:<digest>"),
            ImageRefError::MissingTag => f.write_str("missing :<tag>"),
            ImageRefError::Tag(e) => e.fmt(f),
            ImageRefError::UnsupportedRegistry(r) => write!(f, "unsupported registry: {r}"),
            ImageRefError::Path => f.write_str("invalid image path"),
        }
    }
}

impl std::error::Error for ImageRefError {}

/// `<registry>/<路徑>:<tag>@sha256:<digest>`。
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct ImageRef {
    registry: String,
    path: String,
    tag: Tag,
    digest: Digest,
}

impl ImageRef {
    /// 解析完整的 image 引用；tag 與 digest 都必須有。
    pub fn parse(s: &str) -> Result<ImageRef, ImageRefError> {
        let (name_tag, digest) = s.split_once('@').ok_or(ImageRefError::Digest)?;
        let digest = Digest::parse(digest).ok_or(ImageRefError::Digest)?;
        let (registry, path_tag) = name_tag
            .split_once('/')
            .ok_or_else(|| ImageRefError::UnsupportedRegistry(String::new()))?;
        if registry != GHCR {
            return Err(ImageRefError::UnsupportedRegistry(registry.to_owned()));
        }
        let (path, tag) = path_tag.rsplit_once(':').ok_or(ImageRefError::MissingTag)?;
        if !path.split('/').all(path_component) {
            return Err(ImageRefError::Path);
        }
        let tag = Tag::parse(tag).map_err(ImageRefError::Tag)?;
        Ok(ImageRef {
            registry: registry.to_owned(),
            path: path.to_owned(),
            tag,
            digest,
        })
    }

    pub fn registry(&self) -> &str {
        &self.registry
    }

    pub fn path(&self) -> &str {
        &self.path
    }

    pub fn tag(&self) -> Tag {
        self.tag
    }

    pub fn digest(&self) -> &Digest {
        &self.digest
    }
}

impl FromStr for ImageRef {
    type Err = ImageRefError;

    fn from_str(s: &str) -> Result<ImageRef, ImageRefError> {
        ImageRef::parse(s)
    }
}

impl fmt::Display for ImageRef {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{}/{}:{}@{}",
            self.registry, self.path, self.tag, self.digest
        )
    }
}

/// 路徑的一段：`[a-z0-9]+((\.|_|__|-+)[a-z0-9]+)*`（OCI distribution 的 path-component）。
fn path_component(s: &str) -> bool {
    let b = s.as_bytes();
    let alnum = |c: u8| c.is_ascii_lowercase() || c.is_ascii_digit();
    let (Some(&first), Some(&last)) = (b.first(), b.last()) else {
        return false;
    };
    if !alnum(first) || !alnum(last) {
        return false;
    }
    let mut i = 0;
    while i < b.len() {
        if alnum(b[i]) {
            i += 1;
            continue;
        }
        // 分隔符：`.`、`_`、`__` 或一個以上的 `-`，後面必須接英數字。
        let start = i;
        match b[i] {
            b'.' => i += 1,
            b'_' => {
                i += 1;
                if b.get(i) == Some(&b'_') {
                    i += 1;
                }
            }
            b'-' => {
                while b.get(i) == Some(&b'-') {
                    i += 1;
                }
            }
            _ => return false,
        }
        if i == start || !b.get(i).is_some_and(|&c| alnum(c)) {
            return false;
        }
    }
    true
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    const D: &str = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef";

    #[test]
    fn valid_tags() {
        let cases = [
            ("v0.0.0", (0, 0, 0)),
            ("v1.2.3", (1, 2, 3)),
            ("v10.20.30", (10, 20, 30)),
            ("v1.0.10", (1, 0, 10)),
            (
                "v18446744073709551615.0.0",
                (18_446_744_073_709_551_615, 0, 0),
            ),
        ];
        for (input, (x, y, z)) in cases {
            let t = Tag::parse(input).unwrap_or_else(|e| panic!("{input}: {e}"));
            assert_eq!((t.major, t.minor, t.patch), (x, y, z), "{input}");
            assert_eq!(t.to_string(), input, "round trip {input}");
        }
    }

    #[test]
    fn invalid_tags() {
        let cases = [
            "",
            "v",
            "1.2.3",
            "V1.2.3",
            "vv1.2.3",
            "v1.2",
            "v1",
            "v1.2.3.4",
            "v01.2.3",
            "v1.02.3",
            "v1.2.03",
            "v00.0.0",
            "v1.2.3-rc.1",
            "v1.2.3+build",
            "v1.2.3-",
            "v1..3",
            "v.1.2",
            "v1.2.",
            "v+1.2.3",
            "v-1.2.3",
            "v1.2.x",
            " v1.2.3",
            "v1.2.3 ",
            "v1.2.3\n",
            "v１.2.3",
            "v18446744073709551616.0.0",
            "latest",
        ];
        for input in cases {
            let e = Tag::parse(input).expect_err(input);
            assert_eq!(e.input(), input);
            assert_eq!(e.message().code, "VK0027");
            assert!(
                e.message()
                    .text
                    .contains(&format!("<{}>", TagError::PLACEHOLDER)),
                "VK0027 must have <tag>"
            );
        }
    }

    #[test]
    fn versions_compare_field_by_field_numerically() {
        let ordered = [
            ("v0.0.0", "v0.0.1"),
            ("v0.0.9", "v0.0.10"),
            ("v0.9.0", "v0.10.0"),
            ("v1.2.3", "v1.10.0"),
            ("v1.99.99", "v2.0.0"),
            ("v9.0.0", "v10.0.0"),
            ("v2.0.0", "v10.0.0"),
        ];
        for (lo, hi) in ordered {
            let (lo_t, hi_t) = (Tag::parse(lo).unwrap(), Tag::parse(hi).unwrap());
            assert!(lo_t < hi_t, "{lo} < {hi}");
            assert!(hi_t > lo_t, "{hi} > {lo}");
        }
        assert_eq!(Tag::parse("v1.2.3").unwrap(), Tag::parse("v1.2.3").unwrap());
    }

    #[test]
    fn latest_skips_invalid_and_ignores_order() {
        let cases: [(&[&str], Option<&str>); 6] = [
            (&[], None),
            (&["latest", "v1.2", "v01.0.0"], None),
            (&["v1.0.0"], Some("v1.0.0")),
            (&["v10.0.0", "v9.0.0", "v2.0.0"], Some("v10.0.0")),
            (&["v1.2.3", "v1.10.0", "v1.9.9"], Some("v1.10.0")),
            (&["v3.0.0-rc.1", "v2.0.0", "main"], Some("v2.0.0")),
        ];
        for (tags, want) in cases {
            let got = Tag::latest(tags.iter().copied());
            assert_eq!(got.map(|t| t.to_string()).as_deref(), want, "{tags:?}");
        }
    }

    #[test]
    fn valid_image_refs() {
        let cases = [
            ("ghcr.io/owner/tool", "v1.2.3"),
            ("ghcr.io/my-org/my_tool", "v0.0.0"),
            ("ghcr.io/org/team/tool.name", "v10.0.1"),
            ("ghcr.io/a/b__c", "v1.0.0"),
            ("ghcr.io/a/b---c", "v1.0.0"),
            ("ghcr.io/tool", "v1.0.0"),
        ];
        for (name, tag) in cases {
            let input = format!("{name}:{tag}@sha256:{D}");
            let r = ImageRef::parse(&input).unwrap_or_else(|e| panic!("{input}: {e}"));
            assert_eq!(r.registry(), GHCR);
            assert_eq!(format!("{}/{}", r.registry(), r.path()), name);
            assert_eq!(r.tag().to_string(), tag);
            assert_eq!(r.digest().hex(), D);
            assert_eq!(r.to_string(), input, "round trip");
        }
    }

    #[test]
    fn invalid_image_refs() {
        let upper = D.to_uppercase();
        let short = &D[..63];
        let long = format!("{D}0");
        let cases: Vec<(String, ImageRefError)> = vec![
            // digest
            ("ghcr.io/o/t:v1.2.3".into(), ImageRefError::Digest),
            ("ghcr.io/o/t:v1.2.3@".into(), ImageRefError::Digest),
            (format!("ghcr.io/o/t:v1.2.3@{D}"), ImageRefError::Digest),
            (
                format!("ghcr.io/o/t:v1.2.3@sha512:{D}"),
                ImageRefError::Digest,
            ),
            (
                format!("ghcr.io/o/t:v1.2.3@sha256:{upper}"),
                ImageRefError::Digest,
            ),
            (
                format!("ghcr.io/o/t:v1.2.3@sha256:{short}"),
                ImageRefError::Digest,
            ),
            (
                format!("ghcr.io/o/t:v1.2.3@sha256:{long}"),
                ImageRefError::Digest,
            ),
            (
                format!("ghcr.io/o/t:v1.2.3@sha256:{D}@sha256:{D}"),
                ImageRefError::Digest,
            ),
            // tag
            (format!("ghcr.io/o/t@sha256:{D}"), ImageRefError::MissingTag),
            (
                format!("ghcr.io/o/t:1.2.3@sha256:{D}"),
                ImageRefError::Tag(Tag::parse("1.2.3").unwrap_err()),
            ),
            (
                format!("ghcr.io/o/t:v1.2.3-rc.1@sha256:{D}"),
                ImageRefError::Tag(Tag::parse("v1.2.3-rc.1").unwrap_err()),
            ),
            (
                format!("ghcr.io/o/t:@sha256:{D}"),
                ImageRefError::Tag(Tag::parse("").unwrap_err()),
            ),
            // registry
            (
                format!("docker.io/o/t:v1.2.3@sha256:{D}"),
                ImageRefError::UnsupportedRegistry("docker.io".into()),
            ),
            (
                format!("GHCR.IO/o/t:v1.2.3@sha256:{D}"),
                ImageRefError::UnsupportedRegistry("GHCR.IO".into()),
            ),
            (
                format!("ghcr.io:443/o/t:v1.2.3@sha256:{D}"),
                ImageRefError::UnsupportedRegistry("ghcr.io:443".into()),
            ),
            (
                format!("t:v1.2.3@sha256:{D}"),
                ImageRefError::UnsupportedRegistry(String::new()),
            ),
            (
                format!("o/t:v1.2.3@sha256:{D}"),
                ImageRefError::UnsupportedRegistry("o".into()),
            ),
            // 路徑
            (format!("ghcr.io/:v1.2.3@sha256:{D}"), ImageRefError::Path),
            (
                format!("ghcr.io/O/t:v1.2.3@sha256:{D}"),
                ImageRefError::Path,
            ),
            (
                format!("ghcr.io/o//t:v1.2.3@sha256:{D}"),
                ImageRefError::Path,
            ),
            (
                format!("ghcr.io/o/t/:v1.2.3@sha256:{D}"),
                ImageRefError::Path,
            ),
            (
                format!("ghcr.io/o/-t:v1.2.3@sha256:{D}"),
                ImageRefError::Path,
            ),
            (
                format!("ghcr.io/o/t.:v1.2.3@sha256:{D}"),
                ImageRefError::Path,
            ),
            (
                format!("ghcr.io/o/a..b:v1.2.3@sha256:{D}"),
                ImageRefError::Path,
            ),
            (
                format!("ghcr.io/o/a___b:v1.2.3@sha256:{D}"),
                ImageRefError::Path,
            ),
            (
                format!("ghcr.io/o/a._b:v1.2.3@sha256:{D}"),
                ImageRefError::Path,
            ),
            (
                format!("ghcr.io/o/a b:v1.2.3@sha256:{D}"),
                ImageRefError::Path,
            ),
            (
                format!("ghcr.io/o:x/t:v1.2.3@sha256:{D}"),
                ImageRefError::Path,
            ),
        ];
        for (input, want) in cases {
            assert_eq!(ImageRef::parse(&input), Err(want), "{input}");
        }
    }

    #[test]
    fn tag_error_inside_image_ref_still_maps_to_vk0027() {
        let Err(ImageRefError::Tag(e)) =
            ImageRef::parse(&format!("ghcr.io/o/t:v01.0.0@sha256:{D}"))
        else {
            panic!("expected tag error");
        };
        assert_eq!(e.input(), "v01.0.0");
        assert_eq!(e.message().code, "VK0027");
    }

    #[test]
    fn digest_parse() {
        assert_eq!(Digest::parse(&format!("sha256:{D}")).unwrap().hex(), D);
        for bad in [
            "",
            "sha256:",
            D,
            &format!("sha256:{}", &D[1..]),
            &format!("sha256:g{}", &D[1..]),
        ] {
            assert_eq!(Digest::parse(bad), None, "{bad}");
        }
    }
}
