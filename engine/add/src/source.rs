//! 工具來源：`-i <image>` 的本機 image 引用、啟動器回的 `docker image inspect` 輸出，與 RepoDigests 的判讀。

use imageref::{ImageRef, Tag};

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
        Err(_) => Err("add -i with an image tar or an image outside ghcr.io".to_owned()),
    }
}

/// `docker image inspect` 輸出裡用得到的兩個欄位。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Inspected {
    /// `Id`：`sha256:<64hex>`。
    pub id: String,
    /// `RepoDigests`：每筆 `<registry>/<路徑>@sha256:<digest>`。
    pub repo_digests: Vec<String>,
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
    let repo_digests = match item.get("RepoDigests") {
        None | Some(serde_json::Value::Null) => Vec::new(),
        Some(v) => v
            .as_array()
            .ok_or("image inspect RepoDigests is not an array")?
            .iter()
            .map(|d| {
                d.as_str()
                    .map(str::to_owned)
                    .ok_or("image inspect RepoDigests has a non-string entry")
            })
            .collect::<Result<_, _>>()?,
    };
    Ok(Inspected { id, repo_digests })
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
        assert!(parse_local("./tool.tar").unwrap_err().contains("tar"));
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

        let none = parse_inspect(br#"[{"Id":"sha256:1","RepoDigests":null}]"#).unwrap();
        assert!(none.repo_digests.is_empty());
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
}
