//! 對整個 repo 跑原因代碼使用檢查（規則見 crate 文件）。
//! image/Dockerfile 的 source stage 已複製 engine/、test/ 與訊息表，test stage 跑得到這個檢查。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::path::{Path, PathBuf};

use reason_lint::{Allow, check, parse_table, scan_tree};

/// 訊息表（repo 相對路徑）。
const CSV: &str = "doc/contract/reason_codes.csv";
/// 要掃的目錄。
const DIRS: &[&str] = &["engine", "test"];
/// 不掃的路徑：msggen 由訊息表產生的檔（逐列列出全部使用中代碼），與本 crate 自己（測試用假代碼）。
const SKIP: &[&str] = &["engine/messages/src/generated.rs", "test/reason_lint"];

/// 可以出現未登錄或已退役代碼的地方。
const ALLOWS: &[Allow] = &[
    Allow {
        path: "engine/runlog/src/tests.rs",
        code: "VK9999",
        reason: "測試執行紀錄讀到未登錄代碼時的處理，故意用不存在的代碼",
    },
    Allow {
        path: "engine/version_file/src/lib.rs",
        code: "VK0070",
        reason: "介面版列表缺少或格式錯的草稿碼（N13），定案登錄前原因先寫明草稿碼、以 VK0056 停下",
    },
    Allow {
        path: "engine/check/src/lib.rs",
        code: "VK0070",
        reason: "test 讀到不合正規形的版本檔的草稿碼（N76），定案登錄前原因先寫明草稿碼、以 VK0056 停下",
    },
    Allow {
        path: "engine/check/src/lib.rs",
        code: "VK0071",
        reason: "test 讀到指向不存在鎖定行的本機覆寫的草稿碼（N76），定案登錄前原因先寫明草稿碼、以 VK0056 停下",
    },
    Allow {
        path: "engine/upgrade/src/lib.rs",
        code: "VK0078",
        reason: "upgrade 遇到同一個 tag 指向不同 digest 的草稿碼（N53），定案登錄前原因先寫明草稿碼、以 VK0056 停下",
    },
    Allow {
        path: "test/e2e/tests/upgrade.rs",
        code: "VK0078",
        reason: "驗 upgrade 同一個 tag 指向不同 digest 時原因寫明草稿碼（N53）；e2e 不能依賴 engine crate 的常數",
    },
    Allow {
        path: "engine/add/src/lib.rs",
        code: "VK0078",
        reason: "線上 add 遇到同一個 tag 指向不同 digest 的草稿碼（N53），定案登錄前原因先寫明草稿碼、以 VK0056 停下",
    },
    Allow {
        path: "test/e2e/tests/add.rs",
        code: "VK0078",
        reason: "驗線上 add 同一個 tag 指向不同 digest 時原因寫明草稿碼（N53）；e2e 不能依賴 engine crate 的常數",
    },
    Allow {
        path: "engine/add/src/lib.rs",
        code: "VK0084",
        reason: "add 帶 -y 又不能互動、卻要 append 進既有未納管檔的草稿碼（N14），定案登錄前原因先寫明草稿碼、以 VK0056 停下",
    },
    Allow {
        path: "engine/check/src/dist.rs",
        code: "VK0075",
        reason: "test dist 交付內容不合格式、文字檔含 CR 的草稿碼（N78、N24），定案登錄前原因先寫明草稿碼、以 VK0056 停下",
    },
    Allow {
        path: "test/e2e/tests/test_dist.rs",
        code: "VK0075",
        reason: "e2e 比對 test dist 以 VK0056 停下時原因裡寫的草稿碼（N78、N24）",
    },
    Allow {
        path: "engine/fetch/src/lib.rs",
        code: "VK0068",
        reason: "其他工具的 cache/<repo>/ 不在、下一步 sync 的草稿碼（N4），定案登錄前原因先寫明草稿碼、以 VK0056 停下",
    },
    Allow {
        path: "engine/fetch/src/lib.rs",
        code: "VK0073",
        reason: "其他工具的 cache/<repo>/ 讀不到或損壞的草稿碼（N4），定案登錄前原因先寫明草稿碼、以 VK0056 停下",
    },
    Allow {
        path: "test/e2e/tests/add.rs",
        code: "VK0068",
        reason: "驗 add 遇到其他工具 cache 不在時原因寫明草稿碼（N4）；e2e 不能依賴 engine crate 的常數",
    },
    Allow {
        path: "test/e2e/tests/upgrade.rs",
        code: "VK0068",
        reason: "驗 upgrade 遇到其他工具 cache 不在時原因寫明草稿碼（N4）；e2e 不能依賴 engine crate 的常數",
    },
    Allow {
        path: "test/e2e/tests/upgrade.rs",
        code: "VK0073",
        reason: "驗 upgrade 遇到其他工具 cache 損壞時原因寫明草稿碼（N4）；e2e 不能依賴 engine crate 的常數",
    },
    Allow {
        path: "test/e2e/tests/remove.rs",
        code: "VK0068",
        reason: "驗 remove 遇到其他工具 cache 不在時原因寫明草稿碼（N4）；e2e 不能依賴 engine crate 的常數",
    },
    Allow {
        path: "test/e2e/tests/remove.rs",
        code: "VK0073",
        reason: "驗 remove 遇到其他工具 cache 損壞時原因寫明草稿碼（N4）；e2e 不能依賴 engine crate 的常數",
    },
    Allow {
        path: "test/e2e/tests/dev.rs",
        code: "VK0068",
        reason: "驗 dev 遇到其他工具 cache 不在時原因寫明草稿碼（N4）；e2e 不能依賴 engine crate 的常數",
    },
    Allow {
        path: "test/e2e/tests/dev.rs",
        code: "VK0073",
        reason: "驗 dev 遇到其他工具 cache 損壞時原因寫明草稿碼（N4）；e2e 不能依賴 engine crate 的常數",
    },
];

fn repo_root() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR")).join("../..")
}

#[test]
fn reason_codes_in_source_are_registered_and_active() {
    let root = repo_root();
    let bytes = std::fs::read(root.join(CSV)).unwrap_or_else(|e| panic!("讀不到 {CSV}：{e}"));
    let table = parse_table(&bytes).unwrap_or_else(|e| panic!("{CSV}：{e}"));
    let found = scan_tree(&root, DIRS, SKIP).unwrap();
    assert!(
        !found.is_empty(),
        "在 {DIRS:?} 裡一個代碼都沒找到，掃描路徑可能錯了"
    );

    let report = check(&table, &found, ALLOWS);
    if !report.unused.is_empty() {
        eprintln!(
            "訊息表登錄、source 含 engine，但 engine/ 還沒以 messages::VKnnnn 用到（只列不擋，{} 個）：{}",
            report.unused.len(),
            report.unused.join(" ")
        );
    }
    let problems = report.problems();
    assert!(
        problems.is_empty(),
        "原因代碼使用不合 {CSV}：\n{}",
        problems.join("\n")
    );
}
