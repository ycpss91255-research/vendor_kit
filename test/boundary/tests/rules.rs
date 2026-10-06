//! 模組邊界：讀架構圖 `doc/diagram/architecture.drawio`（ADR-0014），
//! 再用 cargo metadata 讀 workspace 的依賴圖，對照圖上的元件檢查 repo 結構與依賴邊。
//!
//! 目前圖上只有系統層（`arch-components` 頁），引擎是一格 `e_eng`，沒有內部模組；
//! 引擎內部 crate 的邊界規則暫時寫死，待新增 arch-engine 頁後改讀圖（見各測試的 TODO）。
#![allow(clippy::unwrap_used, clippy::expect_used)]

mod drawio;

use std::collections::{BTreeMap, BTreeSet};
use std::path::{Path, PathBuf};

use cargo_metadata::{Metadata, MetadataCommand, Package};

/// 架構圖檔（repo 相對路徑）。image/Dockerfile 的 source stage 要把 doc/diagram 複製進去。
const ARCH_FILE: &str = "doc/diagram/architecture.drawio";
/// 系統層架構頁的 `<diagram id>`。
const ARCH_PAGE: &str = "arch-components";
/// 引擎在系統層的格。
const ENGINE_CELL: &str = "e_eng";

/// 元件的 repo 路徑現況（記錄用；存在與否不在 test stage 檢查，見 R1）。
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
enum Status {
    /// 路徑已存在。
    Built,
    /// 還沒建；路徑不存在。建好後改成 Built。
    Pending,
}

/// 元件 → repo 路徑：鍵是 `arch-components` 頁紅框（VK 開發的）的 cell id。
const COMPONENT_PATHS: &[(&str, &str, Status)] = &[
    ("e_eng", "engine/", Status::Built),
    ("i_eng", "image/Dockerfile", Status::Built),
    ("h_launch", "launcher/", Status::Pending),
    ("h_shell", "launcher/", Status::Pending),
    ("h_boot", "launcher/", Status::Pending),
];

fn repo_root() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR")).join("../..")
}

fn arch_page() -> drawio::Page {
    let path = repo_root().join(ARCH_FILE);
    let xml = std::fs::read_to_string(&path)
        .unwrap_or_else(|e| panic!("讀不到 {ARCH_FILE}（{}）：{e}", path.display()));
    let pages = drawio::parse(&xml).unwrap_or_else(|e| panic!("{ARCH_FILE}：{e}"));
    pages
        .into_iter()
        .find(|p| p.id == ARCH_PAGE)
        .unwrap_or_else(|| panic!("{ARCH_FILE} 沒有 <diagram id=\"{ARCH_PAGE}\"> 頁"))
}

/// 圖例格的 id（`script/diagram/STYLE.md` 3.1）：`<前綴>_lg<n>`、`<前綴>_lgt`、`<前綴>_lgx_<鍵>`。
fn is_legend_id(id: &str) -> bool {
    if id.ends_with("_lgt") || id.contains("_lgx_") {
        return true;
    }
    id.rfind("_lg").is_some_and(|i| {
        let n = &id[i + 3..];
        !n.is_empty() && n.bytes().all(|b| b.is_ascii_digit())
    })
}

fn metadata() -> Metadata {
    MetadataCommand::new()
        .manifest_path(repo_root().join("Cargo.toml"))
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

/// R1：圖上紅框（圖例除外）的 id 集合，和元件 → repo 路徑對照表的鍵完全相等。
/// 路徑是否存在不在這裡檢查：image 的 source stage 只複製 repo 的一部分（image/Dockerfile 的 test stage 裡沒有 image/、launcher/）。
#[test]
fn red_frames_match_component_paths() {
    let page = arch_page();
    let red: BTreeMap<&str, String> = page
        .cells
        .iter()
        .filter(|c| c.is_red_frame() && !is_legend_id(&c.id))
        .map(|c| (c.id.as_str(), c.label()))
        .collect();
    let table: BTreeSet<&str> = COMPONENT_PATHS.iter().map(|(id, _, _)| *id).collect();

    let missing_in_table: Vec<String> = red
        .iter()
        .filter(|(id, _)| !table.contains(*id))
        .map(|(id, label)| format!("{id}（{label}）"))
        .collect();
    let missing_on_diagram: Vec<&str> = table
        .iter()
        .filter(|id| !red.contains_key(*id))
        .copied()
        .collect();
    assert!(
        missing_in_table.is_empty() && missing_on_diagram.is_empty(),
        "{ARCH_FILE} 頁 {ARCH_PAGE} 的紅框與 COMPONENT_PATHS 不一致：\
         圖上有、表裡沒有 {missing_in_table:?}；表裡有、圖上沒有紅框 {missing_on_diagram:?}"
    );
}

/// R2：每個 workspace 成員都在 engine/ 或 test/ 底下。
#[test]
fn members_live_under_engine_or_test() {
    let meta = metadata();
    let engine_dir = meta.workspace_root.join("engine");
    let test_dir = meta.workspace_root.join("test");
    let stray: Vec<String> = meta
        .workspace_packages()
        .into_iter()
        .filter(|p| {
            !p.manifest_path.starts_with(&engine_dir) && !p.manifest_path.starts_with(&test_dir)
        })
        .map(|p| format!("{}（{}）", p.name, p.manifest_path))
        .collect();
    assert!(
        stray.is_empty(),
        "workspace 成員要在 engine/ 或 test/ 底下：{stray:?}"
    );
}

/// R3：系統層的引擎是單一格，沒有內部模組。圖上一旦畫了引擎內部，
/// 就該改到 arch-engine 頁畫，並讓這裡的邊界檢查改讀那一頁。
#[test]
fn engine_is_a_single_cell_on_the_system_page() {
    let page = arch_page();
    let todo = "引擎內部模組要畫在待新增的 arch-engine 頁，並讓 test/boundary 改讀那一頁";
    let engines: Vec<&drawio::Cell> = page.cells_with_id(ENGINE_CELL).collect();
    assert_eq!(
        engines.len(),
        1,
        "頁 {ARCH_PAGE} 要剛好一格 {ENGINE_CELL}，實際 {} 格",
        engines.len()
    );
    let engine = engines[0];
    assert!(
        !engine.style_has("container=1") && !engine.style_has("swimlane"),
        "{ENGINE_CELL}（{}）在頁 {ARCH_PAGE} 是容器；{todo}",
        engine.label()
    );
    let inner: Vec<String> = page
        .cells
        .iter()
        .filter(|c| c.parent.as_deref() == Some(ENGINE_CELL))
        .map(|c| format!("{}（{}）", c.id, c.label()))
        .collect();
    assert!(
        inner.is_empty(),
        "{ENGINE_CELL} 在頁 {ARCH_PAGE} 有內部格 {inner:?}；{todo}"
    );
}

// TODO(#372)：改讀 arch-engine 頁，由圖上的引擎模組產生成員清單。
#[test]
fn expected_members_exist() {
    let m = members(&metadata());
    for name in [
        "vendor_kit",
        "diagnostics",
        "output",
        "message_types",
        "messages",
        "files",
        "imageref",
        "compat",
        "schema",
        "layout",
        "config",
        "filelock",
        "prompt",
        "metadata",
        "stamp",
        "merge",
        "args",
        "version_file",
        "progress",
        "shell",
        "retract",
        "runlog",
        "plan",
        "msggen",
        "txn",
        "fetch",
        "initfiles",
        "tools_just",
        "add",
        "sync",
        "remove",
        "install",
        "update",
        "upgrade",
        "dev",
        "prune",
        "shell_check",
        "registry",
        "check",
    ] {
        assert!(
            m.get(name).is_some_and(|(e, _)| *e),
            "{name} must be under engine/"
        );
    }
    for name in ["e2e", "boundary", "reason_lint"] {
        assert!(
            m.get(name).is_some_and(|(e, _)| !*e),
            "{name} must be under test/"
        );
    }
}

/// 只有入口 crate 能往下依賴；下層不得反向依賴入口。
// TODO(#372)：改讀 arch-engine 頁，由圖上的模組邊產生允許的依賴。
#[test]
fn lower_layers_do_not_depend_on_the_entry_crate() {
    let m = members(&metadata());
    for name in [
        "diagnostics",
        "output",
        "message_types",
        "messages",
        "files",
        "imageref",
        "compat",
        "schema",
        "layout",
        "config",
        "filelock",
        "prompt",
        "metadata",
        "stamp",
        "merge",
        "args",
        "version_file",
        "progress",
        "shell",
        "retract",
        "runlog",
        "plan",
        "msggen",
        "txn",
        "fetch",
        "initfiles",
        "tools_just",
        "add",
        "sync",
        "remove",
        "install",
        "update",
        "upgrade",
        "dev",
        "prune",
        "shell_check",
        "registry",
        "check",
    ] {
        let (_, pkg) = &m[name];
        assert!(
            !workspace_deps(pkg, &m).contains(&"vendor_kit".to_owned()),
            "{name} must not depend on vendor_kit"
        );
    }
}

/// test/ 下的 crate 只經執行檔與 cargo metadata 看引擎，不依賴任何 engine/ crate。
/// 這條永久保留、不從圖產生：依據是 ADR-0010（驗收只經公開入口）與 ADR-0011（測試讀不到引擎內部）。
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
