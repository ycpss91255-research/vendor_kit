# Release 資產附 digest 旁檔，已釋出的永不刪

版本鎖定行鎖了 digest，但 digest 指到的東西得由提供端一直留著，否則決定性重建會在提供端靜默失效（[不變量 2](../contract/02_invariants.md#2-一個來源版本鎖定行只有一份進-git)），退版也退不回（[不變量 10](../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)）。離線導入也必須寫出 digest，而從一份 image tar 算得到的只是那個平台的雜湊，不是版本鎖定行要鎖的多架構 index digest。所以每個支援平台的 image tar 旁附一個同名 `.digest` 檔，由出貨端交出正式的 index digest，讓離線與線上寫出同一行；已釋出的 image 與 Release 資產永不刪。

## Considered Options

- **不要旁檔，離線導入自己算 tar 的 sha256 當 digest**：算出來的是那個平台的雜湊，離線與線上會寫出不同的鎖定行，兩邊都不報錯。
- **離線時只寫 tag**：tag 不鎖內容，離線裝到的不保證與線上同一份。
- **digest 塞進 `SHA256SUMS`，不另設旁檔**：要先解析再挑出對應平台那一行；同名旁檔一次讀取就到手，缺哪個平台也直接看得出來。
- **舊資產設保留窗口，過期清掉**：資產一清，退得回的承諾在某個時間點之後就作廢，而且沒有訊號。
- **用 imgpkg air-gap bundle 取代 tar 加旁檔**：見 [ADR-0001](0001-why-not-existing-tools.md)。

## Consequences

- 退版不需要額外機制，還原鎖定行就夠，因為指到的資產還在。
- 代價落在出貨端：每次 release 多交每個平台的 `.digest` 與一份 `SHA256SUMS`，支援平台增加時跟著長。永不刪是永久成本：儲存與用過的版本號只會累積，發錯的版本只能另發一版蓋過去。
- 驗收落在黑箱層：乾淨 fixture 裡拿掉旁檔跑 `add <repo> -i <image>`，要得到[結束碼 `2`](../contract/03_output.md#結束碼)，且版本鎖定行不動。
- 內部機制（之後搬到實作 issue）：
  - Release 資產：每個支援平台一份 image tar（工具 image 是多架構 amd64＋arm64，見 [ADR-0011](0011-test-layers-and-ci-matrix.md)）；每份旁邊一個同名 `.digest`，記正式的多架構 index digest，不是那份 tar 的雜湊；另有一份 `SHA256SUMS` 管其餘資產的完整性，不承擔 digest。
  - 離線導入（`add <repo> -i <image>`）讀 tar 同名的旁檔取得 digest 寫進版本鎖定行；旁檔缺就以 `2` 結束，不退化成只寫 tag。
  - 永不刪涵蓋已釋出的 image（含多架構 index 的子 digest）、Release 資產，以及驗收用的 fixture。
