# ADR-0011：測試分層與強制閘門——multi-stage 的固定順序、兩個平台、CI 的 just 矩陣

> Serves: 機制（服務不變量 9、11），不建立不變量——本檔記錄 Docker multi-stage 的測試分層順序、支援平台清單、多架構 image 的建置與兩平台驗證方式，以及 CI 的 just 版本矩陣，是[不變量 9「對外承諾必須黑箱可驗；本機開發與正式啟動走同一個入口」](../contract/02_invariants.md#9-對外承諾必須黑箱可驗本機開發與正式啟動走同一個入口)與[不變量 11「正確性不綁單一平台」](../contract/02_invariants.md#11-正確性不綁單一平台)的驗證機制。

- **Status:** Accepted

## Context

引擎跑在容器裡，使用者從外面只看得到 `just`、檔案系統、結束碼與印出的訊息。測試若讀得到引擎內部模組或內部狀態，改內部就能讓測試繼續綠：對外行為已經壞了，紅燈不會亮。所以「驗得到」這件事得先決定在哪裡驗、以什麼順序驗。

平台那一側的失敗方式更難發現。鎖只在一個平台鎖得住、行尾比對只在一個平台等價、指紋只在一個平台算得一樣——這些在別的平台上不會報錯，只會靜默給錯答案，而且通常被當成那台機器的個別狀況。同一批使用者手上同時有 Jetson、WSL2 與共用工作站，出錯的那一台不會自己回報。要接住這類錯誤，支援平台得先是一份明列的清單，清單上的每個平台都要真的跑過。

主機那三個工具裡，`just` 是唯一會因版本差異改變 recipe 行為的一個；下限 `just >= 1.33.0` 記在 [ADR-0007 第 1 節](0007-host-thin-layer-and-shell-integrity.md#1-主機依賴的版本下限)與 [04 使用者介面的主機需求](../contract/04_interface.md#主機需求)。下限只寫在文件裡不等於驗過，也不保證上游後來的版本還照舊行為。

## Decision

不變量 9 與 11 的條文不在本檔重述，只連結。以下是實現它們的驗證機制。

### 1. 測試分層：Docker multi-stage，順序固定

- Docker multi-stage 測試分層（smoke → lint 與 unit → integration → system → acceptance）

每一層是一個 build stage，後一層以前一層為 base。所以順序不是慣例而是相依：前面那層沒過，後面那層根本不會開始跑。`lint 與 unit` 同屬第二層，彼此沒有先後。

最後一層 acceptance 只走公開入口，跑不變量 9 的完整流程；那條流程與驗收矩陣由「dev 自身與驗收」ADR 擁有，本檔只固定它是分層的最後一層。

### 2. 支援平台清單

- 平台：Linux amd64 與 arm64（含 Jetson、RPi 64 位元），WSL2 視同 Linux；armv7 不支援，SELinux 不支援

清單以外的平台不承諾、不驗；清單本身會增加，增加時這一節改，不變量 11 的條文不動。

### 3. 多架構 image 與兩平台驗證

- 工具 image 為多架構 amd64 + arm64，同一次 buildx 出、COPY-only，CI 驗兩平台 image 內展開的交付資料逐檔位元組一致；引擎 image 同為多架構，只驗兩平台 LABEL（protocol 與 schema）一致

工具 image 只裝資料，同一份 `dist/` 進去，兩個平台展開出來的每個檔就該一個位元組都不差，所以驗的是交付資料逐檔的位元組。比的是展開後的檔。image tar、layer 與 digest 含平台資訊，兩個平台本來就不同，不拿來比。工具 image 三行 `Dockerfile.dist` 的 COPY-only 形狀由 [ADR-0006](0006-tool-image-as-data-only.md) 擁有，本檔擁有的是驗證那一側。

引擎 image 兩個平台各有自己的編譯產物，位元組本來就不同，能比也該比的是對外契約：`protocol` 與 `schema` 兩個 LABEL 在兩個平台一致。

### 4. CI 的 just 版本矩陣

- CI 矩陣 just 1.33.0 + latest（latest 非 required）

`1.33.0` 是 required，對應不變量 5 記的下限；`latest` 不是 required，它是提早看見上游變動的哨兵，紅了就進 issue 討論，不擋合併。

### 修訂（2026-09-30）

- **Amendment status:** Accepted
- 不變量頁改成只寫概念（維護者 2026-09-30），原本寫在那裡的機制細節移到本檔。決定不變，只補記。
- 被當作正確性依據、因此不得只在一個平台成立的機制，例如鎖、路徑、symlink、行尾、時間戳、指紋計算。
- 失效的例子：鎖沒鎖到，兩個 `just` 就同時寫 `cache/`；行尾比對不等價，就會冒出假的合併衝突，或漏認自己寫過的行。

## Consequences

- 得到：分層順序靠 build 相依強制，本機 `just test` 與 CI 走同一條路，不會有「CI 才有的順序」。
- 得到：arm64 不是事後補測的平台。工具 image 的位元組差異、引擎 image 的契約 LABEL 差異都會在 CI 亮紅燈。
- 得到：`just` 的下限有測試撐著，上游改行為時 `latest` 那一格先紅。
- 付出：CI 時間。前面任一層失敗就停，改一行 lint 也要重跑一次 build 鏈。
- 付出：CI 要有 arm64 的執行環境（runner 或 emulation），出貨端跑 buildx 的成本比單架構高。
- 付出：Jetson、RPi、WSL2 這幾個平台的驗證進不了一般 CI，得靠實機驗收；[ADR-0001 §5](0001-why-not-existing-tools.md) 重評門檻第 3 項也倚賴同一批實機。
- 平台清單增加時改本檔第 2 節，不動不變量頁。`armv7` 或 SELinux 要改成支援，是新的決議。

## Alternatives

- **CI 只跑 amd64，arm64 等使用者回報。** 省一半 CI 資源，但不變量 11 要防的正是「不會報錯、只給錯答案」的那類錯誤，靠回報等於沒驗。
- **每個平台各發一個單架構 image、版本鎖定行各鎖一個 digest。** 建置最簡單，但同一行在不同機器就會裝到不同內容，打破鎖定行的意義（同樣的理由讓 [ADR-0001](0001-why-not-existing-tools.md) 不採 vendir 的多架構處理）。（歷史：`doc/decisions/scope_roadmap.md` 曾把「dist image 單架構 amd64」列為待拍板，那一項已定案為多架構。）
- **引擎 image 也驗兩平台位元組一致。** 標準更嚴，但引擎在兩個架構上編出來的產物本來就不同，這個檢查永遠紅，測不到任何東西。
- **分層交給 CI job 串接，不用 multi-stage。** CI 設定寫得出同樣的順序，代價是順序只存在於 CI：本機跑不到同一條鏈，分層與閘門變成兩份真相。
- **CI 只鎖 `1.33.0` 一格。** 綠燈最穩定，但上游 `just` 改了行為要等使用者撞到才知道，而使用者裝的通常就是 latest。
