# 本機開發與驗收共用同一條「用指定 image 當引擎」的路

驗收若能伸手進引擎內部，改內部就能讓測試繼續綠，而使用者唯一看得到的那一面早就壞了；開發與驗收若各有一條換引擎的路，驗收測的就不是開發者實際跑的東西（[不變量 9](../contract/02_invariants.md#9-對外承諾必須黑箱可驗本機開發與正式啟動走同一個入口)）。所以驗收只走公開入口、只看可觀察的結果，並用剛 build 出來的引擎 image 在乾淨 fixture repo 上跑完整流程；「指定用哪個 image 當引擎」只有一個機制，就是 `version.local.toml` 的本機覆寫，`dev --engine -i <image>` 與驗收寫的都是這一行。為了驗「退得回」（[不變量 10](../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)），介面版區間包含薄殼介面版 P 的較舊引擎仍可跑；比薄殼舊到不支援 P 的引擎，不得用來重產薄殼，`dev --engine -i` 在寫入本機覆寫前就拒絕。

## Considered Options

- **驗收直接呼叫引擎內部模組，跳過 `just` 與容器**：快得多，但內部重構可以讓測試全綠而對外行為已經壞掉，不變量 9 直接排除。
- **開發用專用旗標或環境變數指引擎，正式啟動只讀 `version.toml`**：引擎來源有兩個入口，差異只會在使用者機器上第一次出現。
- **驗收沿用前一次跑剩下的 repo**：「第一次導入」與「在既有狀態上修復」混成同一種情形，而兩者的正確行為不同。
- **每項驗收獨立、不固定流程順序**：每一步的前置狀態得另外造，造出來的是不是真實流程產生的那一份，本身又要驗。
- **舊引擎一律拒絕啟動**：不必管重產薄殼，但同時廢掉了退得回：沒辦法用舊引擎取回舊內容。

## Consequences

- 開發者手上那條路就是出貨閘門走的那條路：`dev --engine -i` 壞了，驗收會一起壞。
- 驗收只碰公開入口，引擎內部隨時重寫都不用改驗收；反過來，任何對外行為的改動都要先在矩陣裡有一項。
- 代價是驗收慢：每一項都要起容器、建 fixture repo、跑完整流程。
- 驗收矩陣的 13 項還沒逐項寫成文件；落地時照 [名詞表](../../GLOSSARY.md) 的名詞寫，並與下面的流程順序一致。
- 目前驗收以 `bootstrap.sh -i <tar>` 離線導入剛 build 的引擎、鎖在 tar 的 digest，沒有經過 `version.local.toml`；跟本 ADR 的單一機制與不變量 9 不一致，列為缺口。
- maintainer_questions（待維護者決定）：驗收的 tar 離線導入與本機開發的 `version.local.toml` 如何符合單一指定引擎機制及不變量 9？本輪只記錄缺口，不另定機制。
- 內部機制：
  - 本機覆寫是 `version.local.toml` 的 `vendor_kit = "<image>"`；沒有第二個環境變數、旗標或入口能改引擎來源。`dev --engine -i <image>` 只用本機 image、不 pull，由引擎在寫入前讀 LABEL 的介面版區間 `[floor, current]`，確認包含薄殼的 P（[ADR-0008](0008-protocol-and-file-schema-versions.md)）；不含時不寫覆寫，以 VK0085 停下（error，結束碼 2），下一步是換一個 image。區間包含 P 的較舊引擎照收，不能只憑引擎版本較舊就拒絕。這一步不重產薄殼，避免把不支援 P 的引擎設成日常入口，之後重產薄殼時把 repo 的入口降級。
  - 啟動器套用引擎本機覆寫時，也只用本機 image、不 pull，不讀 `version.toml` 旁記的介面版列表；一般呼叫以覆寫 image 的 LABEL 區間驗 P，不含時以 VK0086 結束（fatal，結束碼 3），下一步是 `just vendor_kit undev --engine` 或換 image。救援呼叫仍用覆寫的 image，但不判介面版，開發者要能用自己的引擎驗 `sync`、`install` 這些救援路徑。`undev --engine` 改用鎖定的引擎，覆寫 image 失效也能解除；`bootstrap.sh` 不套用本機覆寫。救援呼叫使用覆寫 image 的唯一例外是 `upgrade --engine` 第二段（含按診斷重跑）：由引擎判斷後，以版本鎖定行那一版引擎重新啟動，不套用引擎本機覆寫；覆寫照留，輸出要說明這一段用的是鎖定行引擎、沒有套用覆寫。
  - 禁止不支援薄殼 P 的舊引擎重產薄殼，採用兩道保護：`dev --engine -i` 在寫入本機覆寫前以 VK0085 拒絕；`upgrade --engine` 第二段一律由版本鎖定行那一版引擎重產薄殼、升 VK 檔與處理 `config.toml` 換版，開著引擎本機覆寫時也不套用覆寫。仍有缺口：開著覆寫的救援呼叫（`install`）不判介面版，既有安裝目錄的 `install` 也不核對在跑的引擎，會按本引擎模板重產薄殼四檔，目前擋不住用覆寫的舊引擎重產薄殼。
  - 驗收跑剛 build、已通過前面各層的引擎 image（[ADR-0011](0011-test-layers-and-ci-matrix.md)），不是 registry 上的某個 tag，也不是上一次 build 的殘留。
  - 乾淨 fixture repo：起始狀態由 fixture 自己定義，不帶前一次留下的 `.vendor_kit/`、快取或未提交的改動。fixture 屬於永不刪的資產（[ADR-0009](0009-release-assets-and-offline-import.md)）。
  - 驗收矩陣是出貨閘門，第 1～13 項缺任一不得出貨，流程順序固定：`install → add → upgrade → dev/undev → remove → uninstall`。`sync`、`update`、`prune` 要有納管狀態才驗得出東西，排在 `add` 與 `upgrade` 之後。順序固定是因為每一步的前置狀態由前一步產生。驗收矩陣與流程順序由測試層擁有，不進引擎程式。
