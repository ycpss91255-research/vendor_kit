//! 啟動器回的 `docker image inspect` 輸出。照抄 engine/add 的 `source` 模組裡同名的兩個函式：
//! 指令之間互不依賴。

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
    let prefix = format!("{name}@");
    let mut found: Option<&str> = None;
    for d in repo_digests {
        if let Some(digest) = d.strip_prefix(&prefix) {
            if found.is_some_and(|f| f != digest) {
                return None;
            }
            found = Some(digest);
        }
    }
    found.map(str::to_owned)
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
    fn two_different_digests_for_one_name_are_ambiguous() {
        let other = "sha256:3333333333333333333333333333333333333333333333333333333333333333";
        let ds = vec![format!("ghcr.io/a/t@{D}"), format!("ghcr.io/a/t@{other}")];
        assert_eq!(digest_for("ghcr.io/a/t", &ds), None);
    }
}
