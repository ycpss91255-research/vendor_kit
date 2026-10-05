//! 模組邊界：用 cargo metadata 讀 workspace 的依賴圖，檢查不准有的依賴邊。
//!
//! TODO(#372)：規則目前寫死在這裡；架構圖（PR #442）進 main 後，
//! 改成讀 `doc/diagram/` 的 .drawio，由圖上的模組邊界與泳道產生規則，
//! 讓圖成為唯一來源。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::collections::BTreeMap;
use std::path::Path;

use cargo_metadata::{Metadata, MetadataCommand, Package};

fn metadata() -> Metadata {
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
    MetadataCommand::new()
        .manifest_path(root.join("Cargo.toml"))
        .no_deps()
        .exec()
        .unwrap()
}

/// workspace 成員：名稱 → (是否在 engine/ 下, 套件)。
fn members(meta: &Metadata) -> BTreeMap<String, (bool, Package)> {
    let engine_dir = meta.workspace_root.join("engine");
    meta.workspace_packages()
        .into_iter()
        .map(|p| {
            let in_engine = p.manifest_path.starts_with(&engine_dir);
            (p.name.to_string(), (in_engine, p.clone()))
        })
        .collect()
}

/// 套件直接依賴的 workspace 成員（normal、dev、build 都算）。
fn workspace_deps(pkg: &Package, members: &BTreeMap<String, (bool, Package)>) -> Vec<String> {
    let mut deps: Vec<String> = pkg
        .dependencies
        .iter()
        .map(|d| d.name.clone())
        .filter(|n| members.contains_key(n))
        .collect();
    deps.sort();
    deps
}

#[test]
fn expected_members_exist() {
    let m = members(&metadata());
    for name in ["vendor_kit", "diagnostics", "output", "messages", "msggen"] {
        assert!(
            m.get(name).is_some_and(|(e, _)| *e),
            "{name} must be under engine/"
        );
    }
    for name in ["e2e", "boundary"] {
        assert!(
            m.get(name).is_some_and(|(e, _)| !*e),
            "{name} must be under test/"
        );
    }
}

/// 只有入口 crate 能往下依賴；下層不得反向依賴入口。
#[test]
fn lower_layers_do_not_depend_on_the_entry_crate() {
    let m = members(&metadata());
    for name in ["diagnostics", "output", "messages", "msggen"] {
        let (_, pkg) = &m[name];
        assert!(
            !workspace_deps(pkg, &m).contains(&"vendor_kit".to_owned()),
            "{name} must not depend on vendor_kit"
        );
    }
}

/// test/ 下的 crate 只經執行檔與 cargo metadata 看引擎，不依賴任何 engine/ crate（ADR-0010、ADR-0011）。
#[test]
fn tests_do_not_depend_on_engine_crates() {
    let m = members(&metadata());
    for (name, (in_engine, pkg)) in &m {
        if *in_engine {
            continue;
        }
        let bad: Vec<String> = workspace_deps(pkg, &m)
            .into_iter()
            .filter(|d| m[d].0)
            .collect();
        assert!(
            bad.is_empty(),
            "{name} must not depend on engine crates: {bad:?}"
        );
    }
}
