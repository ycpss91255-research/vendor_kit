# Release 資產附 digest 旁檔，已釋出的永不刪

版本鎖定行鎖了 digest，但 digest 指到的東西得由提供端一直留著，否則決定性重建會在提供端靜默失效（[不變量 2](../contract/02_invariants.md#2-一個來源版本鎖定行只有一份進-git)），退版也退不回（[不變量 10](../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)）。離線導入也必須寫出 digest，而從一份 image tar 算得到的只是那個平台的雜湊，不是版本鎖定行要鎖的多架構 index digest。所以每個支援平台的 image tar 旁附一個同名 `.digest` 檔，由出貨端交出正式的 index digest，讓離線與線上寫出同一行；已釋出的 image 與 Release 資產永不刪。

## Considered Options

- **不要旁檔，離線導入自己算 tar 的 sha256 當 digest**：算出來的是那個平台的雜湊，離線與線上會寫出不同的鎖定行，兩邊都不報錯。
- **離線時只寫 tag**：tag 不鎖內容，離線裝到的不保證與線上同一份。
- **digest 塞進 `SHA256SUMS`，不另設旁檔**：要先解析再挑出對應平台那一行；同名旁檔一次讀取就到手，缺哪個平台也直接看得出來。
- **舊資產設保留窗口，過期清掉**：資產一清，退得回的承諾在某個時間點之後就作廢，而且沒有訊號。
- **用 imgpkg air-gap bundle 取代 tar 加旁檔**：見 [ADR-0001](0001-why-not-existing-tools.md)。
- **(A) 把離線導入後不能續用列為已知限制**：導入成功後隔天就得連網，違反 [01 目的與承諾](../contract/01_purpose.md#vk-對導入的承諾)的離線承諾。
- **(B) 離線導入只保證 containerd image store**：與本 ADR 採 `docker save` 格式「讓 classic image store 也能載入」的既定目的衝突。

## Consequences

- 退版不需要額外機制，還原鎖定行就夠，因為指到的資產還在。
- 代價落在出貨端：每次 release 多交每個平台的 `.digest` 與一份 `SHA256SUMS`，支援平台增加時跟著長。永不刪是永久成本：儲存與用過的版本號只會累積，發錯的版本只能另發一版蓋過去。
- 驗收落在黑箱層：乾淨 fixture 裡拿掉旁檔跑 `add <repo> -i <image>`，要得到[結束碼 `2`](../contract/03_output.md#結束碼)，且版本鎖定行不動。
- `docker load` 在 classic image store 不留 RepoDigests，用版本鎖定行的引用找不到剛載入的 image；containerd store 也只在 tar 的名稱與鎖定行相同、而且保留多架構 index 時才找得到。離線導入時，在安裝目錄的 `.vendor_kit/` 下另設一個新路徑記錄版本鎖定行的完整 image 引用與載入的 image ID，並依 [ADR-0002](0002-vendor-kit-dir-layout-and-lock-line-form.md) 把它加進 `.vendor_kit/.gitignore`；不進 git，也不放進 `cache/`、`gen/`、`log/`，它們各有用途。之後以鎖定引用找不到 image 時，先查這筆紀錄；完整引用相同且 image 仍在本機，就直接用、不 pull，否則才嘗試 pull，失敗仍以 VK0036（引擎）或 VK0055（工具）停下。這筆紀錄只回答同一份內容在本機 Docker 裡如何取得，不改版本鎖定行，也不按 tag、版本名或最後載入的 image 挑選。這個機制涵蓋 `bootstrap.sh -i <tar>` 首次導入後的日常指令、`add <repo> -i <tar>` 後的重新取件，以及中斷 `add` 的恢復；classic 與 containerd 兩種 image store 都要驗收。

## 內部機制

- Release 資產：每個支援平台交付 `vendor_kit-vX.Y.Z-linux-<arch>.tar`，採 `docker save` 格式、含 `manifest.json`，讓 classic image store 也能載入；每份旁邊一個同名 `.digest`，記正式的多架構 index digest，不是那份 tar 的雜湊。另交付內嵌引擎 image 引用 `<registry>/<路徑>:vX.Y.Z@<index digest>` 的 `bootstrap.sh` 與一份 `SHA256SUMS`；後者管其餘資產的完整性，不承擔版本鎖定行的 digest。不發布 `vN` 或 `latest` 浮動 tag，版本只用完整的 `vX.Y.Z`。
- `.digest` 內容是一行 `sha256:<64 位小寫 hex>`；不收 NUL，解析時依序去掉結尾的一個 LF 與一個 CR，再檢查格式。旁檔名是把 `.tar` 換成 `.digest`，例如 `engine.tar` 對應 `engine.digest`。
- `-i` 的值只有以 `.tar` 結尾才當 tar。離線導入（`add <repo> -i <image>`）寫入版本鎖定行的 digest 只取自旁檔，不從 tar 或 RepoDigests 推算；旁檔缺少或格式不合，以 VK0031、結束碼 `2` 停下，版本鎖定行不動，不退化成只寫 tag。
- tar 交付格式只允許一個 image，且名稱恰好一個 `ghcr.io/<路徑>:vX.Y.Z`。不合時以另行登錄的原因代碼、結束碼 `2` 停下，版本鎖定行不動；診斷指名 tar、違反的規則與實際看到的內容。此時 `docker load` 已成功，image 會留在本機，訊息不得宣稱沒有載入或沒有副作用。採用專屬原因代碼，因為這是交付格式不合，不是 VK 的 bug，也不是 docker 操作失敗。
- 啟動器把引擎的鎖定 image 引用寫進 `in/engine`，內容是一行引用加 LF，透過唯讀掛載的 `in/` 交給引擎。引擎 image 無法內含自身的多架構 index digest，因此首次導入由這個檔取得要寫入的引用。
- 永不刪涵蓋已釋出的 image（含多架構 index 的子 digest）、Release 資產，以及驗收用的 fixture。
