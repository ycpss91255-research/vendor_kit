//! 啟動器回的 `docker image inspect` 輸出。照抄 engine/add 的 `source` 模組裡同名的兩個函式：
//! 指令之間互不依賴。`upgrade --engine` 另讀 `Config.Labels`（engine/add 沒有）。

use std::collections::BTreeMap;

/// `docker image inspect` 輸出裡用得到的欄位。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Inspected {
    /// `Id`：`sha256:<64hex>`。
    pub id: String,
    /// `RepoDigests`：每筆 `<registry>/<路徑>@sha256:<digest>`。
    pub repo_digests: Vec<String>,
    /// `Config.Labels`：沒有（或是 `null`）就是空的。`upgrade --engine` 從這裡讀目標引擎的介面版區間與
    /// 檔案版上限。
    pub labels: BTreeMap<String, String>,
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
    let labels = match item.get("Config").and_then(|c| c.get("Labels")) {
        None | Some(serde_json::Value::Null) => BTreeMap::new(),
        Some(v) => v
            .as_object()
            .ok_or("image inspect Config.Labels is not an object")?
            .iter()
            .map(|(k, v)| {
                v.as_str()
                    .map(|s| (k.clone(), s.to_owned()))
                    .ok_or("image inspect Config.Labels has a non-string value")
            })
            .collect::<Result<_, _>>()?,
    };
    Ok(Inspected {
        id,
        repo_digests,
        labels,
    })
}

/// RepoDigests 裡屬於 `name`（`<registry>/<路徑>`）的那一筆的 digest（`sha256:<hex>`）。
/// 沒有，或有兩筆不同的，回 `None`。
pub fn digest_for(name: &str, repo_digests: &[String]) -> Option<String> {
    match repo_digest(name, repo_digests) {
        RepoDigest::One(d) => Some(d),
        RepoDigest::Missing | RepoDigest::Conflicting(_) => None,
    }
}

/// 本機 image 的 RepoDigests 裡屬於某個 `<registry>/<路徑>` 的 digest。
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
    fn inspect_output() {
        let json = format!(
            "[\n  {{\n    \"Id\": \"sha256:{}\",\n    \"RepoDigests\": [\"ghcr.io/acme/tool@{D}\"]\n  }}\n]\n",
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
        assert!(parse_inspect(b"not json").is_err());
    }

    #[test]
    fn labels_come_from_config() {
        let i = parse_inspect(
            br#"[{"Id":"sha256:1","Config":{"Labels":{"vendor_kit.schema.max":"1","a":"b"}}}]"#,
        )
        .unwrap();
        assert_eq!(
            i.labels.get("vendor_kit.schema.max").map(String::as_str),
            Some("1")
        );
        assert_eq!(i.labels.len(), 2);
        for json in [
            &br#"[{"Id":"sha256:1"}]"#[..],
            br#"[{"Id":"sha256:1","Config":{}}]"#,
            br#"[{"Id":"sha256:1","Config":{"Labels":null}}]"#,
        ] {
            assert!(parse_inspect(json).unwrap().labels.is_empty());
        }
        assert!(parse_inspect(br#"[{"Id":"sha256:1","Config":{"Labels":[]}}]"#).is_err());
        assert!(parse_inspect(br#"[{"Id":"sha256:1","Config":{"Labels":{"a":1}}}]"#).is_err());
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
