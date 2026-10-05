# Docker 內的四個部分統一使用 Rust

> Status: accepted
>
> Serves: [P7：交付物依執行位置選語言](../decisions/design_principles.md#p7-交付物依執行位置選語言容器內看穩定性執行效率與測試清晰程度主機上看原生)、[不變量 4：永不靜默失敗](../contract/02_invariants.md#4-永不靜默失敗)、[不變量 9：對外承諾必須黑箱可驗；本機開發與正式啟動走同一個入口](../contract/02_invariants.md#9-對外承諾必須黑箱可驗本機開發與正式啟動走同一個入口)

維護者於 2026-10-05 在 [#372](https://github.com/ycpss91255-research/vendor_kit/issues/372) 定案：VK 在 Docker 內執行的引擎本體、build stage 的訊息產生器、整支 VK 的端到端測試（只經公開入口 `just vendor_kit …` 與 `bootstrap.sh`）與模組邊界檢查全部使用 Rust，放在同一個 Cargo workspace。依 P7，只以穩定性、執行效率與測試清晰程度比較候選；學習成本、開發成本與 image 大小不列入判準。主機端的啟動器、薄殼內的 VK recipe 與 `log.sh` 依 P7 使用主機原生的 bash 與 just，其實作不在本 ADR 範圍內。

## Considered Options

- **Rust（採用）**：強型別、以 `Result` 讓錯誤路徑出現在型別上，未處理的 `Result` 由 lint 升為錯誤擋下、沒有 null，safe Rust 提供記憶體安全與資料競爭的編譯期保證，[toml_edit](https://docs.rs/toml_edit/latest/toml_edit/) 的文件樹編輯可保留未知欄位與格式，滿足 [ADR-0008](0008-protocol-and-file-schema-versions.md) 的未知欄位保留硬條件，trait 與獨立 crate 也讓測試清晰程度高。
- **C#**：Tomlyn 有保留格式的語法樹，xUnit 的測試分組最完整，但 nullable 只是可升為錯誤的警告，沒有資料競爭的編譯期保證。
- **Go**：Go 1 相容承諾強、標準庫完整，但忽略 `error`、nil 與不窮舉的 switch 不由編譯器擋下，go-toml 的格式保留編輯 API 也不在該函式庫的相容保證內。
- **Kotlin/JVM**：null 安全與 JUnit 分組強，但 Java platform types 有逃出口，目前比較材料對 TOML 往返保真的證據不足。
- **Python**：tomlkit 成熟、pytest 清楚，但型別與錯誤邊界不強制。
- **C++**：測試框架成熟，但語言沒有記憶體安全保證。
- **shell**：TOML、CSV 與結構化診斷都要另外解析，字串與程序狀態難以提供同等的型別及錯誤邊界。

端到端測試的比較中 Rust 排第一，但與 C#／Kotlin 分數接近（三項等權時打平，測試清晰程度權重再高就會翻轉）；選 Rust 是為了同一套工具鏈與較高的穩定性，測試只經公開入口，日後改用別的語言不需改引擎。

## Consequences

- `unused_must_use` 必須升為錯誤；非測試程式禁用 `unwrap`／`expect`／`panic!` 處理預期失敗；寫回要明確處理關檔錯誤，不靠 `Drop`。
- 四個部分放在同一個 Cargo workspace：引擎本體依模組拆成 crate；訊息產生器是獨立的 generator bin；端到端測試與模組邊界檢查各自是獨立 crate。
- 訊息產生器在 build stage 明確執行，從[訊息表](../contract/reason_codes.csv)同時產出引擎訊息表與 `bootstrap.sh` 使用的 bash 片段，並與引擎共用 schema 型別；不用 `build.rs`。產生器的輸出納入 build，lint 依 [#136](https://github.com/ycpss91255-research/vendor_kit/issues/136) 檢查原因代碼的登錄、使用與退役。
- 整支 VK 的端到端測試 crate 不依賴引擎 crate，只經公開入口，以 snapbox 加 assert_cmd 比對 stdout、stderr、結束碼與檔案樹；驗收依 [ADR-0010](0010-dev-self-and-acceptance.md) 經 just、啟動器與 Docker，不直接呼叫引擎 binary 來代替整條路徑。
- 模組邊界採一個模組一個 crate，由 Rust 檢查器用 cargo_metadata 讀依賴圖，比對[架構圖目錄](../diagram/)中 `.drawio` 的邊，取代 import-linter；Cargo 的依賴宣告不能單獨代替圖面比對，新增可編譯的依賴仍須通過邊界檢查。[代理指引](../../AGENTS.md) 中的 import-linter 約定須另行改成本 ADR 的邊界檢查。
- 引擎 image 的 build stage 用 Rust 工具鏈編譯，最終 stage 仍須帶 git，以執行 [ADR-0003](0003-baseline-merge-and-line-records.md) 的 `git merge-file`。
- 確定性輸出不能依賴 `HashMap` 的走訪順序，須依 [ADR-0012](0012-deterministic-behavior-and-escaping.md) 的規則排序或使用有序容器。
- `flock` 與 SIGTERM 以 Linux API 實作；設定以 [04 使用者介面的設定](../contract/04_interface.md#設定)所定的 `.vendor_kit/config.toml` 為準。
- TOML 修改走 toml_edit 的文件樹，不能先解成只含已知欄位的 struct 再重建整份檔；未知欄位保留不了就依 ADR-0008 拒絕寫入，保留註解與空白不另升為硬條件。
- 這項決議取代 #372 先前的 Python 與 Go 結論。
