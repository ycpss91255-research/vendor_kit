# 測試分層用 Docker multi-stage，兩個平台都跑

測試讀得到引擎內部就可能對外已壞、紅燈卻不亮（[不變量 9](../contract/02_invariants.md#9-對外承諾必須黑箱可驗本機開發與正式啟動走同一個入口)）；只在一個平台成立的鎖、行尾比對、指紋則在別的平台靜默給錯答案（[不變量 11](../contract/02_invariants.md#11-正確性不綁單一平台)）。所以測試分層寫成 Docker multi-stage，後一層以前一層為 base，順序靠 build 相依強制、本機與 CI 走同一條鏈；支援平台是一份明列清單（Linux amd64 與 arm64），CI 在兩個平台都跑，並用 just 的下限版與最新版各跑一格。

## Considered Options

- **CI 只跑 amd64，arm64 等使用者回報**：省一半 CI 資源，但不變量 11 要防的正是不報錯、只給錯答案的那類錯誤。
- **每個平台各發單架構 image、版本鎖定行各鎖一個 digest**：同一行在不同機器會裝到不同內容，打破鎖定行的意義（同樣的理由讓 [ADR-0001](0001-why-not-existing-tools.md) 不採 vendir 的多架構處理）。
- **引擎 image 也驗兩平台位元組一致**：兩個架構編出來的產物本來就不同，這個檢查永遠紅。
- **分層交給 CI job 串接，不用 multi-stage**：順序只存在於 CI，本機跑不到同一條鏈，分層變成兩份真相。
- **CI 只鎖 just `1.33.0` 一格**：上游 just 改了行為要等使用者撞到才知道，而使用者裝的通常是最新版。

## Consequences

- 本機 `just test` 與 CI 走同一條路，不會有「CI 才有的順序」；代價是前面任一層失敗就停，改一行 lint 也要重跑 build 鏈。
- arm64 不是事後補測的平台；代價是 CI 要有 arm64 執行環境（runner 或 emulation），buildx 成本比單架構高。
- Jetson、RPi、WSL2 的驗證進不了一般 CI，得靠實機驗收；[ADR-0001](0001-why-not-existing-tools.md) 重評門檻第 3 項也倚賴同一批實機。
- 平台清單增加時改本檔，不動不變量頁；armv7 或 SELinux 要改成支援是新的決議。
- 內部機制（之後搬到實作 issue）：
  - 分層順序：smoke → lint 與 unit → integration → system → acceptance。每一層是一個 build stage；lint 與 unit 同屬第二層、彼此沒有先後。acceptance 只走公開入口，流程與驗收矩陣見 [ADR-0010](0010-dev-self-and-acceptance.md)。
  - 支援平台：Linux amd64 與 arm64（含 Jetson、RPi 64 位元），WSL2 視同 Linux；armv7、SELinux 不支援。清單以外的平台不承諾、不驗。
  - 不得只在一個平台成立的機制：鎖、路徑、symlink、行尾、時間戳、指紋計算。失效的例子：鎖沒鎖到，兩個 `just` 同時寫 `cache/`；行尾比對不等價，冒出假的合併衝突或漏認自己寫過的行。
  - 工具 image 是多架構 amd64 + arm64，同一次 buildx 產出、COPY-only（形狀見 [ADR-0006](0006-tool-image-as-data-only.md)）；CI 驗兩平台 image 內展開的交付資料逐檔位元組一致。image tar、layer 與 digest 含平台資訊，本來就不同，不拿來比。
  - 引擎 image 同為多架構，只驗兩平台的 `protocol` 與 `schema` 兩個 LABEL 一致。
  - CI 的 just 矩陣：`1.33.0`（required，對應主機需求的下限，見 [ADR-0007](0007-host-thin-layer-and-shell-integrity.md) 與 [04 使用者介面](../contract/04_interface.md#主機需求)）與 latest（非 required，是提早看見上游變動的哨兵，紅了就進 issue 討論，不擋合併）。
