# 測試分層用 Docker multi-stage，兩個平台都跑

測試讀得到引擎內部就可能對外已壞、紅燈卻不亮（[不變量 9](../contract/02_invariants.md#9-對外承諾必須黑箱可驗本機開發與正式啟動走同一個入口)）；只在一個平台成立的鎖、行尾比對、指紋則在別的平台靜默給錯答案（[不變量 11](../contract/02_invariants.md#11-正確性不綁單一平台)）。所以測試分層寫成 Docker multi-stage，後一層以前一層為 base，順序靠 build 相依強制，本機與 CI 走同一條鏈。支援平台明列為 Linux amd64 與 arm64，CI 在兩個平台都跑，並用 just 的下限版與最新版各跑一格。PR 的 CI 目前只跑 amd64；arm64 在 `just release-image` 以 QEMU 跑完整 test stage，出貨前一定驗過兩平台。驗收需要 Docker daemon，目前由共用腳本另起 DinD，尚未覆蓋兩平台；這個驗收層安排標為待確認（A1）。

## Considered Options

- **CI 只跑 amd64，arm64 等使用者回報**：省一半 CI 資源，但不變量 11 要防的正是不報錯、只給錯答案的那類錯誤。
- **每個平台各發單架構 image、版本鎖定行各鎖一個 digest**：同一行在不同機器會裝到不同內容，打破鎖定行的意義（同樣的理由讓 [ADR-0001](0001-why-not-existing-tools.md) 不採 vendir 的多架構處理）。
- **引擎 image 也驗兩平台位元組一致**：兩個架構編出來的產物本來就不同，這個檢查永遠紅。
- **分層交給 CI job 串接，不用 multi-stage**：順序只存在於 CI，本機跑不到同一條鏈，分層變成兩份真相。
- **CI 只鎖 just `1.33.0` 一格**：上游 just 改了行為要等使用者撞到才知道，而使用者裝的通常是最新版。

## Consequences

- 本機 `just test` 與 CI 走同一條路，不會有「CI 才有的順序」；代價是前面任一層失敗就停，改動 lint 也受 build 相依順序約束。
- arm64 的完整 test stage 由 `just release-image` 建置時跑；非本機架構以 QEMU 執行，不要求原生 runner，代價是 buildx 與 emulation 成本比單架構高。PR 的 CI 目前只跑 amd64，且尚無 release workflow；每個 PR 未驗 arm64，是 PR 與發版之間的已知缺口。這不代表驗收層已覆蓋兩平台，驗收覆蓋的缺口仍待確認（A1）。
- Jetson、RPi 與 WSL2 的環境差異得靠實機驗收；WSL2 上用 Docker Desktop 當 daemon 時列為候選，實機驗收過才算支援，在此之前跟清單外的形態一樣處理。[ADR-0001](0001-why-not-existing-tools.md) 重評門檻第 3 項也倚賴同一批實機。
- 平台清單增加時改本檔，不動不變量頁；armv7 或 SELinux 要改成支援是新的決議。
- 內部機制：
  - 分層順序：smoke → lint 與 unit → integration → system → acceptance。每一層是一個 build stage；lint 與 unit 同屬第二層、彼此沒有先後。目前實作把 acceptance 以前的檢查併在單一 test stage；acceptance 需要 daemon，不在 stage 鏈裡，改由驗收腳本另起 DinD。分層是否照實作改寫，待確認（A1）。
  - 建置內檢查集中在 [引擎 Dockerfile](../../image/Dockerfile) 的 test stage：訊息產物一致性、fmt、clippy、引擎編譯與工作區測試、啟動器 lint 與 bats、薄殼入口 e2e、bootstrap.sh 檢查與 smoke。test stage 安裝 just，入口 e2e 用真正的 just 解析薄殼。引擎 image 依賴 test stage 的產物，檢查沒過就建不出來。
  - 驗收層需要獨立 daemon，由[驗收腳本](../../test/acceptance/run.sh) 自己起 `docker:29.8.0-dind`，網路設為 `--internal`；測試端 image 以 test stage 為 base，順序仍接在前面的檢查之後。[測試 workflow](../../.github/workflows/test.yml) 的 acceptance job 只呼叫同一支腳本，本機 `just acceptance` 也走這條路，不另寫 workflow 的 DinD service。驗收只走公開入口，流程見 [ADR-0010](0010-dev-self-and-acceptance.md)。目前只驗 containerd image store、單一平台；[ADR-0009](0009-release-assets-and-offline-import.md) 要求的 classic image store 一格尚未覆蓋。這個安排與覆蓋範圍待確認（A1）。
  - 支援平台：Linux amd64 與 arm64（含 Jetson、RPi 64 位元），WSL2 視同 Linux；armv7、SELinux 不支援。WSL2 上用 Docker Desktop 當 daemon 時列為候選，實機驗收過才算支援，在此之前跟清單外的形態一樣處理。清單以外的平台不承諾。
  - 不得只在一個平台成立的機制：鎖、路徑、symlink、行尾、時間戳、指紋計算。失效的例子：鎖沒鎖到，兩個 `just` 同時寫 `cache/`；行尾比對不等價，冒出假的合併衝突或漏認自己寫過的行。
  - 工具 image 是多架構 amd64 + arm64，同一次 buildx 產出、COPY-only（形狀見 [ADR-0006](0006-tool-image-as-data-only.md)）；CI 驗兩平台 image 內展開的交付資料逐檔位元組一致。image tar、layer 與 digest 含平台資訊，本來就不同，不拿來比。
  - 引擎 image 同為多架構，[release recipes](../../justfile) 的 `just release-image` 一次 buildx 建 amd64 與 arm64，非本機架構在 QEMU 下跑完整 test stage。`just release-verify` 確認 index 恰含這兩平台，且每個平台都有 `vendor_kit.protocol.floor`、`vendor_kit.protocol.current`、`vendor_kit.schema.max` 三個 LABEL、值跨平台一致；不比引擎產物位元組。
  - CI 的 just 矩陣：`1.33.0`（required，對應主機需求的下限，見 [ADR-0007](0007-host-thin-layer-and-shell-integrity.md) 與 [04 使用者介面](../contract/04_interface.md#主機需求)）與 latest（以 `continue-on-error` 設為非 required，是提早看見上游變動的哨兵，紅了就進 issue 討論，不擋合併）。

## 驗收的 daemon 形態清單

下列 daemon 形態的支援範圍已定案；本機 rootful（不開 userns-remap）與同一使用者的本機 rootless 都必須在驗收矩陣實際覆蓋。目前的 DinD 驗收不等於已逐項驗過這份清單，驗收安排與覆蓋缺口仍待確認（A1）。清單外的形態與尚未通過實機驗收的 WSL2 Docker Desktop，由啟動器在建立執行紀錄之前以另行登錄的原因代碼擋下，結束碼 `2`，不建執行紀錄、不動任何 VK 檔。這項檢查排在建執行紀錄之前，要等 PR #684 的 03 輸出把 daemon 形態併進主機前置檢查並定案後才生效；在那之前，契約的主機前置檢查還不含這一項，也不在 ADR-0005 承認的建紀錄前例外裡。

| daemon 形態 | 支援範圍 |
|---|---|
| 本機 rootful，不開 userns-remap | 支援；驗收矩陣需覆蓋 |
| 同一使用者的本機 rootless | 支援；驗收矩陣需覆蓋 |
| WSL2 Docker Desktop | 候選，實機驗收過才算支援；在此之前跟清單外的形態一樣處理 |
| snap、遠端 daemon、DinD、userns-remap | 不支援；DinD 在此只用作驗收的隔離環境 |
