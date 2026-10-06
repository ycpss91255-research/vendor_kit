//! 工具來源：`-i <image>` 的本機 image 引用、image tar 的 `.digest` 旁檔與 `docker load -q` 輸出、啟動器回的
//! `docker image inspect` 輸出，與 RepoDigests 的判讀。

use std::ffi::OsStr;
use std::os::unix::ffi::OsStrExt;

use imageref::{ImageRef, Tag};

/// `-i` 的值以這個結尾就當 image tar（同 `launcher/bootstrap_main.sh`）。
pub const TAR_SUFFIX: &str = ".tar";
/// image tar 的同名旁檔副檔名：`foo.tar` → `foo.digest`（ADR-0009）。
pub const DIGEST_SUFFIX: &str = ".digest";

/// `-i` 的值是不是 image tar：以 [`TAR_SUFFIX`] 結尾。
pub fn is_tar(given: &OsStr) -> bool {
    given.as_bytes().ends_with(TAR_SUFFIX.as_bytes())
}

/// image tar 主機路徑的同名旁檔：去掉結尾的 [`TAR_SUFFIX`]，接上 [`DIGEST_SUFFIX`]。
pub fn digest_sidecar(tar: &[u8]) -> Vec<u8> {
    let stem = tar.strip_suffix(TAR_SUFFIX.as_bytes()).unwrap_or(tar);
    let mut out = stem.to_vec();
    out.extend_from_slice(DIGEST_SUFFIX.as_bytes());
    out
}

/// 讀 `.digest` 旁檔的內容：一行多架構 index digest `sha256:<64 位小寫 hex>`。跟 `launcher/bootstrap_main.sh`
/// 的 `vk_bootstrap_digest` 同一套規則：含 NUL 不收；去掉結尾一個 LF，再去掉結尾一個 CR；剩下的要整串合格。
pub fn parse_digest(bytes: &[u8]) -> Option<String> {
    if bytes.contains(&0) {
        return None;
    }
    let s = bytes.strip_suffix(b"\n").unwrap_or(bytes);
    let s = s.strip_suffix(b"\r").unwrap_or(s);
    let hex = s.strip_prefix(b"sha256:")?;
    let ok = hex.len() == 64
        && hex
            .iter()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(b));
    ok.then(|| String::from_utf8_lossy(s).into_owned())
}

/// `docker load -q` 報告載入的那一個 image。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Loaded {
    /// `Loaded image ID: <id>`：tar 裡的 image 沒有名稱。
    Id(String),
    /// `Loaded image: <ref>`：tar 裡帶名稱的 image。
    Ref(String),
}

/// 解析 `docker load -q` 的 stdout：要剛好一行非空行，是 `Loaded image ID: <id>` 或 `Loaded image: <ref>`
/// （同 `launcher/bootstrap_main.sh` 的 `vk_bootstrap_load`）；其他都回 `None`。
pub fn parse_load(bytes: &[u8]) -> Option<Loaded> {
    let text = std::str::from_utf8(bytes).ok()?;
    let mut lines = text.lines().filter(|l| !l.is_empty());
    let line = lines.next()?;
    if lines.next().is_some() {
        return None;
    }
    if let Some(id) = line.strip_prefix("Loaded image ID: ") {
        return Some(Loaded::Id(id.to_owned()));
    }
    line.strip_prefix("Loaded image: ")
        .map(|r| Loaded::Ref(r.to_owned()))
}

/// image tar 載入的 image 的 `<registry>/<路徑>:<tag>`：`candidates`（load 報告的引用，或 inspect 的 RepoTags）
/// 裡 [`parse_local`] 收得下的、不重複的那些。
pub fn tar_tags(candidates: &[String]) -> Vec<LocalRef> {
    let mut found: Vec<LocalRef> = Vec::new();
    for c in candidates {
        if let Ok(r) = parse_local(c)
            && !found.iter().any(|f| f.given == r.given)
        {
            found.push(r);
        }
    }
    found
}

/// `-i` 給的本機 image 引用 `<registry>/<路徑>:<tag>`（還沒有 digest）。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LocalRef {
    /// 使用者給的原字串，原樣交給 inspect 與診斷。
    pub given: String,
    pub registry: String,
    pub path: String,
    pub tag: Tag,
}

impl LocalRef {
    /// `<registry>/<路徑>`：RepoDigests 每一筆的 `@` 之前。
    pub fn name(&self) -> String {
        format!("{}/{}", self.registry, self.path)
    }

    /// 加上 inspect 讀到的 digest，成為版本鎖定行的值。
    pub fn pin(&self, digest: &str) -> Option<ImageRef> {
        ImageRef::parse(&format!("{}:{}@{digest}", self.name(), self.tag)).ok()
    }
}

/// 解析 `-i` 的值；不支援的形式回原因（英文，填進診斷）。
pub fn parse_local(given: &str) -> Result<LocalRef, String> {
    if given.contains('@') {
        return Err("add -i with an image reference that includes a digest".to_owned());
    }
    // 借完整 image 引用的規則檢查 registry、路徑與 tag：補一個占位 digest 再解析。
    let probe = format!("{given}@sha256:{}", "0".repeat(64));
    match ImageRef::parse(&probe) {
        Ok(r) => Ok(LocalRef {
            given: given.to_owned(),
            registry: r.registry().to_owned(),
            path: r.path().to_owned(),
            tag: r.tag(),
        }),
        Err(imageref::ImageRefError::MissingTag) => {
            Err("add -i with an image reference without a :vX.Y.Z tag".to_owned())
        }
        Err(imageref::ImageRefError::Tag(_)) => {
            Err("add -i with an image reference whose tag is not vX.Y.Z".to_owned())
        }
        Err(_) => Err("add -i with an image outside ghcr.io".to_owned()),
    }
}

/// `docker image inspect` 輸出裡用得到的兩個欄位。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Inspected {
    /// `Id`：`sha256:<64hex>`。
    pub id: String,
    /// `RepoDigests`：每筆 `<registry>/<路徑>@sha256:<digest>`。
    pub repo_digests: Vec<String>,
    /// `RepoTags`：每筆 `<registry>/<路徑>:<tag>`；沒有或 `null` 是空的。
    pub repo_tags: Vec<String>,
}

/// 解析 `docker image inspect <ref>` 的 JSON：一個陣列，剛好一個物件。
pub fn parse_inspect(bytes: &[u8]) -> Result<Inspected, String> {
    let value: serde_json::Value = serde_json::from_slice(bytes)
        .map_err(|e| format!("image inspect output is not JSON: {e}"))?;
    let items = value
        .as_array()
        .ok_or("image inspect output is not a JSON array")?;
    let [item] = items.as_slice() else {
        return Err(format!(
            "image inspect output has {} entries, expected 1",
            items.len()
        ));
    };
    let id = item
        .get("Id")
        .and_then(serde_json::Value::as_str)
        .ok_or("image inspect output has no Id")?
        .to_owned();
    let repo_digests = strings(item, "RepoDigests")?;
    let repo_tags = strings(item, "RepoTags")?;
    Ok(Inspected {
        id,
        repo_digests,
        repo_tags,
    })
}

/// inspect 物件裡的字串陣列欄位；沒有或 `null` 是空的。
fn strings(item: &serde_json::Value, key: &str) -> Result<Vec<String>, String> {
    match item.get(key) {
        None | Some(serde_json::Value::Null) => Ok(Vec::new()),
        Some(v) => v
            .as_array()
            .ok_or_else(|| format!("image inspect {key} is not an array"))?
            .iter()
            .map(|d| {
                d.as_str()
                    .map(str::to_owned)
                    .ok_or_else(|| format!("image inspect {key} has a non-string entry"))
            })
            .collect(),
    }
}

/// RepoDigests 裡屬於 `name`（`<registry>/<路徑>`）的那一筆的 digest（`sha256:<hex>`）。
/// 沒有，或有兩筆不同的，回 `None`。
pub fn digest_for(name: &str, repo_digests: &[String]) -> Option<String> {
    match repo_digest(name, repo_digests) {
        RepoDigest::One(d) => Some(d),
        RepoDigest::Missing | RepoDigest::Conflicting(_) => None,
    }
}

/// 本機 image 的 RepoDigests 裡屬於某個 `<registry>/<路徑>` 的 digest（同 engine/upgrade）。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RepoDigest {
    /// 一筆都沒有（例如本機建置或從 tar 載入的 image）。
    Missing,
    /// 剛好一個 digest（同一個 digest 出現多次也算一個）。
    One(String),
    /// 兩個以上不同的 digest，依出現順序、不重複：無法唯一判定。
    Conflicting(Vec<String>),
}

/// 分出 RepoDigests 裡屬於 `name`（`<registry>/<路徑>`）的 digest：沒有、一個、或互相衝突。
pub fn repo_digest(name: &str, repo_digests: &[String]) -> RepoDigest {
    let prefix = format!("{name}@");
    let mut found: Vec<String> = Vec::new();
    for d in repo_digests {
        if let Some(digest) = d.strip_prefix(&prefix)
            && !found.iter().any(|f| f == digest)
        {
            found.push(digest.to_owned());
        }
    }
    match found.len() {
        0 => RepoDigest::Missing,
        1 => RepoDigest::One(found.remove(0)),
        _ => RepoDigest::Conflicting(found),
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    const D: &str = "sha256:2222222222222222222222222222222222222222222222222222222222222222";

    #[test]
    fn local_ref_forms() {
        let r = parse_local("ghcr.io/acme/tool:v1.2.0").unwrap();
        assert_eq!(r.name(), "ghcr.io/acme/tool");
        assert_eq!(r.tag.to_string(), "v1.2.0");
        assert_eq!(
            r.pin(D).unwrap().to_string(),
            format!("ghcr.io/acme/tool:v1.2.0@{D}")
        );
        assert!(
            parse_local("ghcr.io/acme/tool")
                .unwrap_err()
                .contains("without")
        );
        assert!(
            parse_local("ghcr.io/acme/tool:latest")
                .unwrap_err()
                .contains("tag")
        );
        assert!(
            parse_local("./tool.tar")
                .unwrap_err()
                .contains("outside ghcr.io")
        );
        assert!(
            parse_local("docker.io/acme/tool:v1.0.0")
                .unwrap_err()
                .contains("ghcr.io")
        );
        assert!(
            parse_local(&format!("ghcr.io/acme/tool@{D}"))
                .unwrap_err()
                .contains("digest")
        );
    }

    #[test]
    fn inspect_output() {
        let json = format!(
            "[\n  {{\n    \"Id\": \"sha256:{}\",\n    \"RepoTags\": [\"x\"],\n    \"RepoDigests\": [\"ghcr.io/acme/tool@{D}\"],\n    \"Size\": 12.5,\n    \"Config\": {{\"Labels\": null}}\n  }}\n]\n",
            "a".repeat(64)
        );
        let i = parse_inspect(json.as_bytes()).unwrap();
        assert_eq!(i.id, format!("sha256:{}", "a".repeat(64)));
        assert_eq!(
            digest_for("ghcr.io/acme/tool", &i.repo_digests),
            Some(D.to_owned())
        );
        assert_eq!(digest_for("ghcr.io/acme/other", &i.repo_digests), None);

        assert_eq!(i.repo_tags, ["x"]);
        let none = parse_inspect(br#"[{"Id":"sha256:1","RepoDigests":null}]"#).unwrap();
        assert!(none.repo_digests.is_empty());
        assert!(none.repo_tags.is_empty());
        assert!(parse_inspect(br#"[{"Id":"sha256:1","RepoTags":"x"}]"#).is_err());
        assert!(parse_inspect(b"[]").is_err());
        assert!(parse_inspect(b"{}").is_err());
        assert!(parse_inspect(b"not json").is_err());
    }

    #[test]
    fn two_different_digests_for_one_name_are_ambiguous() {
        let other = "sha256:3333333333333333333333333333333333333333333333333333333333333333";
        let ds = vec![format!("ghcr.io/a/t@{D}"), format!("ghcr.io/a/t@{other}")];
        assert_eq!(digest_for("ghcr.io/a/t", &ds), None);
        assert_eq!(
            repo_digest("ghcr.io/a/t", &ds),
            RepoDigest::Conflicting(vec![D.to_owned(), other.to_owned()])
        );
        let same = vec![format!("ghcr.io/a/t@{D}"), format!("ghcr.io/a/t@{D}")];
        assert_eq!(
            repo_digest("ghcr.io/a/t", &same),
            RepoDigest::One(D.to_owned())
        );
        assert_eq!(repo_digest("ghcr.io/a/x", &same), RepoDigest::Missing);
    }

    #[test]
    fn tar_values_and_digest_sidecars() {
        assert!(is_tar(OsStr::new("./tool.tar")));
        assert!(is_tar(OsStr::new("/a b/tool.tar")));
        assert!(!is_tar(OsStr::new("ghcr.io/acme/tool:v1.2.0")));
        assert!(!is_tar(OsStr::new("tool.tar.gz")));
        assert_eq!(digest_sidecar(b"/h/p/foo.tar"), b"/h/p/foo.digest");
        assert_eq!(digest_sidecar(b"/h/p/x.y.tar"), b"/h/p/x.y.digest");
    }

    #[test]
    fn digest_file_is_one_index_digest() {
        let ok = Some(D.to_owned());
        assert_eq!(parse_digest(D.as_bytes()), ok);
        assert_eq!(parse_digest(format!("{D}\n").as_bytes()), ok);
        assert_eq!(parse_digest(format!("{D}\r\n").as_bytes()), ok);
        assert_eq!(parse_digest(format!("{D}\r").as_bytes()), ok);
        for bad in [
            String::new(),
            "\n".to_owned(),
            format!("{D}\n\n"),
            format!("{D}\n{D}\n"),
            format!(" {D}"),
            format!("{D} "),
            format!("sha256:{}", "A".repeat(64)),
            format!("{D}0"),
            "sha512:00".to_owned(),
            format!("{D}\0"),
        ] {
            assert_eq!(parse_digest(bad.as_bytes()), None, "{bad:?}");
        }
    }

    #[test]
    fn load_output_names_exactly_one_image() {
        let id = format!("sha256:{}", "a".repeat(64));
        assert_eq!(
            parse_load(format!("Loaded image ID: {id}\n").as_bytes()),
            Some(Loaded::Id(id.clone()))
        );
        assert_eq!(
            parse_load(b"\nLoaded image: ghcr.io/acme/tool:v1.2.0\n\n"),
            Some(Loaded::Ref("ghcr.io/acme/tool:v1.2.0".to_owned()))
        );
        for bad in [
            &b""[..],
            b"\n",
            b"Loaded image: a:v1\nLoaded image: b:v1\n",
            b"something else\n",
        ] {
            assert_eq!(parse_load(bad), None);
        }
    }

    #[test]
    fn tar_tags_keep_usable_distinct_tags() {
        let c = |v: &[&str]| -> Vec<String> {
            tar_tags(&v.iter().map(|s| (*s).to_owned()).collect::<Vec<_>>())
                .into_iter()
                .map(|r| r.given)
                .collect()
        };
        assert_eq!(
            c(&[
                "ghcr.io/acme/tool:v1.2.0",
                "tool:latest",
                "ghcr.io/acme/tool:v1.2.0"
            ]),
            ["ghcr.io/acme/tool:v1.2.0"]
        );
        assert_eq!(
            c(&["ghcr.io/acme/tool:v1.2.0", "ghcr.io/acme/tool:v1.3.0"]),
            ["ghcr.io/acme/tool:v1.2.0", "ghcr.io/acme/tool:v1.3.0"]
        );
        assert!(c(&["tool:latest"]).is_empty());
    }
}
