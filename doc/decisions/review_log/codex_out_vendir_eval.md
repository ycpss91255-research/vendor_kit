# A. 能取代與不能取代的範圍

## 能取代的部分

vendir 可以取代「從 registry 取得工具 image，並將指定內容展開到 `cache/`」這個狹窄步驟，具體包括：

- 直接透過 registry API 拉取 `FROM scratch` 工具 image，不需要建立暫存 container。
- 驗證並回報實際解析出的 image digest。
- 展開 image layers。
- 用 `includePaths`、`excludePaths`、`newRootPath` 選取 `dist/` 內需要的部分。
- 以 staging directory 後整體替換目標目錄；這適合 `.vendor_kit/cache/<repo>/` 這種由 VK 完全擁有、可隨時重建的快取。
- 用 `-d 'dir=local-dir'` 將某個 vendir directory 改成本機來源，作為「填充 cache」層級的開發覆寫。

這些能力正是 vendir 的定位：宣告某個目錄最後應該長什麼樣，並由它完全管理該目錄。[vendir 官方說明](https://carvel.dev/vendir/)、[v0.46.2 sync 實作](https://github.com/carvel-dev/vendir/blob/v0.46.2/pkg/vendir/cmd/sync.go)

## 完全不能取代的部分

vendir 不能取代以下 VK 核心功能：

1. **初始檔的基準版合併**

   vendir 沒有共同祖先、目前 repo 檔、新版初始檔三方合併的模型，也不保存「上次套用的原版」。它會先移除目標目錄，再把 staging directory 換上去。[目錄替換實作](https://github.com/carvel-dev/vendir/blob/v0.46.2/pkg/vendir/directory/staging_dir.go)

   `manual`、`ignorePaths` 類能力只是讓部分路徑不由 vendir 管，不是三方合併，不能滿足初始檔升版需求。

2. **「不刪、不覆蓋 repo 檔」的政策**

   vendir 適合管理 `.vendor_kit/cache/`，但不能直接管理初始檔所在的 repo 路徑；否則會刪除使用者新增內容並還原使用者修改。

3. **VK 的版本宣告與升退版語意**

   vendir 自己以 `vendir.yml` 加 `vendir.lock.yml` 建模。它不知道 VK 的版本鎖定行、本機覆寫、`upgrade`／`undev`、Renovate 規則或「宣告唯一」不變量。

4. **完整的開發模式**

   `-d dir=local-dir` 只能取代「這次從哪裡複製目錄」。VK 仍須自行負責：

   - `version.local.toml` 或等價本機覆寫；
   - 覆寫只套用到已宣告工具；
   - `dev`／`undev` 的生命週期；
   - 本機來源與正式版本的切換；
   - 對 tracked 檔、cache 與初始檔的不同處理。

5. **離線 image 匯入**

   依實測，vendir `image` 沒有從本機 OCI／Docker tar 讀取的介面。它不能取代 `docker load` 後從 daemon 取出 image 的離線流程。

6. **多架構 index 的平台選擇**

   v0.46.2 內嵌的 imgpkg 對 image index 會要求提供具體 image manifest digest，而不是自行依主機平台選 manifest。[imgpkg pull 實作](https://github.com/carvel-dev/imgpkg/blob/v0.48.1/pkg/imgpkg/v1/pull.go#L184-L192)

   因此若版本鎖定行鎖的是 amd64/arm64 共用的 OCI index digest，vendir 不能直接使用。必須：

   - 發布單一、架構無關的 manifest；或
   - 每個平台鎖不同 manifest digest。

   後者會直接碰撞「同一行在任何機器得到同一份內容」的設計。

# B. 只把 vendir 當主機端下載後端

## 實際得到什麼

它可以把：

```text
docker pull
docker create
docker cp
docker rm
```

縮成由 vendir 負責的：

```text
registry pull → layer extraction → path filtering → cache directory replacement
```

實際收益是：

- 不產生暫存 container。
- 不經 Docker daemon 下載與展開工具 image。
- `includePaths`／`newRootPath` 可直接只取 `dist/files/`。
- vendir 會回報解析後 digest，可用來檢查輸出確實來自版本鎖定行指定的 digest。
- 目標 cache 整體替換，失敗時比逐檔複製更容易維持完整目錄。

但 VK 本來就需要 Docker 啟動引擎 image，因此「不經 daemon」並沒有移除 Docker 依賴，只是另闢第二條下載路徑。

## 付出的第三方 binary 成本

vendir 會成為一個新的正式執行期依賴，VK 至少必須負責：

- 固定 vendir 版本。
- 分發 Linux amd64 與 Linux arm64 binary。
- 下載失敗與版本不相容處理。
- 驗證 `checksums.txt`。
- 若要求來源真實性，還要處理 release checksum 的 Cosign signature／certificate，而不只是 sha256。
- 鏡像或保存 binary，避免 GitHub release 不可達。
- 離線包內攜帶正確架構的 binary。
- 升版、CVE、行為變更及回歸測試。
- 測試 Jetson、WSL2、CI、一般 Linux 上的權限與路徑行為。

v0.46.2 有 Linux amd64/arm64、Darwin amd64/arm64、Windows amd64 發行資產，但「上游有 binary」不等於 VK 已具備可靠的離線分發與驗證鏈。[v0.46.2 release](https://github.com/carvel-dev/vendir/releases/tag/v0.46.2)、[發行與驗證設定](https://github.com/carvel-dev/vendir/blob/v0.46.2/.goreleaser.yml)

此外，vendir 建立 parent directory 為 `0700` 是可觀察差異。VK 必須接受這項契約，或在同步後自行校正權限；後者又增加一層平台與錯誤處理邏輯。

## 認證不是完全分離的 credential store，但確實是兩條路徑

「Docker credential helper 與 vendir keychain 完全是兩套儲存」不完全精確：

- Docker CLI／daemon 會讀 Docker config 並使用其中的 credential helper。
- vendir 不透過 daemon，但 imgpkg 的 default keychain 也能讀 `~/.docker/config.json`；若其中引用 helper，vendir process 必須找得到並能執行該 helper。
- vendir/imgpkg 另有環境變數及 IaaS／GitHub keychain，其解析順序和 daemon 不同。[imgpkg 認證文件](https://carvel.dev/imgpkg/docs/develop/auth/)、[keychain 實作](https://github.com/carvel-dev/imgpkg/blob/v0.48.1/pkg/imgpkg/registry/keychain.go)

所以真正的風險是：

> `docker pull ghcr.io/...` 成功，不保證 `vendir sync` 在相同環境必然成功。

常見差異包括 `$HOME`、`DOCKER_CONFIG`、helper 是否在 `PATH`、WSL2 與 Docker Desktop 的整合，以及環境變數優先序。

私有 GHCR 可以選擇以下任一路徑：

- 讓 vendir process 讀到同一份 Docker config，且相關 credential helper 可執行。
- 提供 `DOCKER_AUTH_CONFIG`，內容含 `ghcr.io` 的 inline credentials。
- 設定：

  ```sh
  IMGPKG_ACTIVE_KEYCHAINS=github
  GITHUB_TOKEN=<可讀取該 GHCR package 的 token>
  ```

- 或直接提供：

  ```sh
  IMGPKG_REGISTRY_HOSTNAME=ghcr.io
  IMGPKG_REGISTRY_USERNAME=<github-user>
  IMGPKG_REGISTRY_PASSWORD=<PAT>
  ```

對 VK 而言，最可控的是明定其中一條並做端到端測試；不能籠統承諾「先 `docker login` 就全部會工作」。

## lock 檔不能真正關掉

v0.46.2 沒有 `--no-lock`。完整的 remote sync 最後會無條件建立 lock config、印到 stdout，再呼叫 `WriteToFile`。只有使用 local-directory override 時才會跳過寫檔。[sync 實作](https://github.com/carvel-dev/vendir/blob/v0.46.2/pkg/vendir/cmd/sync.go)、[lock 寫入實作](https://github.com/carvel-dev/vendir/blob/v0.46.2/pkg/vendir/config/lock_config.go)

因此：

- **能避免留下持久 lock 檔。**
- **不能讓 vendir 完全不生成 lock 資料。**
- lock 內容仍會出現在 stdout。

### `--lock-file /dev/null`

不應視為受支援的 no-lock 模式，原因明確：

- 這只是利用 Unix character device 丟棄寫入，不是 vendir 契約。
- 不跨平台。
- `--locked` 讀取 `/dev/null` 會得到無效／空 lock。
- partial directory sync 會因 `/dev/null` 已存在而嘗試讀取、合併舊 lock，可能失敗。
- 未來若寫檔實作改成 temporary file 加 rename，行為可能改變。

結論：**不值得依賴。**

### `--lock-file <暫存檔>`

這是比較可控的旁路，但必須：

- 使用安全建立的唯一暫存路徑。
- 不使用 `--locked`。
- 輸入只接受完整 `tag@sha256:digest`，禁止只有 tag。
- 同步後解析 lock，驗證回報 digest 與版本鎖定行完全相同。
- 無論成功失敗都清除暫存檔。
- 不讓暫存檔位於 repo，也不允許 commit。
- 防止 crash 後殘留被下次執行誤用。

暫存 lock 在物理上仍存在過，但只要它是由版本鎖定行生成、只用來反向驗證、從不作為下次輸入，就不是語意上的第二份版本真相。

## 是否破壞「唯一版本真相」

結論分兩種：

- **若 `vendir.yml` 或 `vendir.lock.yml` 被持久保存、手改、commit，或後續用 `--locked` 消費：會破壞。**
- **若 vendir config 與 lock 都由版本鎖定行即時生成，lock 只在暫存目錄中驗證後刪除，且永不使用 `--locked`：不會在語意上破壞。**

不過後者需要一套嚴格 wrapper 才能維持。也就是說，vendir 沒有直接服務這條不變量；VK 必須持續防止 vendir 的正常工作模式變成第二份版本真相。

# C. 主機依賴承諾應如何改寫

若 vendir 在主機執行，誠實的說法應是：

> 主機需要 Docker、Git、just，以及 VK 指定版本、符合主機架構的 vendir；vendir 可由使用者預先安裝，或由 VK 下載、校驗並管理。

如果 VK 自動下載 vendir，可以說：

> 使用者預先只需安裝 Docker、Git、just；VK 另會在主機下載並執行 vendir。

但不能再說「不引進第三方 binary」或「主機只需要這三項」，因為 vendir 仍是主機原生可執行檔。

承諾退化程度：

| 環境 | 影響 |
|---|---|
| 一般 Linux amd64 | 中等：安裝通常容易，但多一條下載、校驗、認證及升級故障路徑。 |
| Jetson/Linux arm64 | 中等至高：上游有 arm64 binary，但 VK 必須確保每版都有資產、校驗與實機測試。 |
| WSL2 | 中等至高：Linux binary 可用，但 Docker Desktop credential helper、Windows credential store、WSL `$HOME`／`PATH` 可能不一致。 |
| CI | 中等：要另外 pin/cache vendir，並注入 vendir 能讀到的 GHCR credential。 |
| 離線環境 | 高：必須預先攜帶正確架構的 vendir binary；而 vendir 本身又不能從本機 image tar 匯入。 |
| 共用工作站 | 中等至高：binary 安裝位置、版本漂移、helper 可見性及 cache 權限都要管理。 |

這不是文字上的小修正，而是直接撤銷目前「主機不裝別的東西」的不變量。

# D. 折衷方案

## 1. 預設 Docker，偵測到 vendir 就改用 vendir

**不值得。**

只因 `PATH` 裡多了一個 binary 就切換後端，會使同一個版本鎖定行在不同機器走不同語意：

- 認證解析不同。
- Docker daemon cache 與 vendir 下載行為不同。
- 權限不同。
- OCI index/platform 行為不同。
- 錯誤訊息與重試方式不同。
- 目錄 staging／替換細節不同。

結果是問題難以重現，測試矩陣也翻倍。

若未來真的要雙後端，至少應採明確選項，例如 `VK_FETCH_BACKEND=vendir`，而不是自動偵測；並要求兩個後端通過相同 golden-content、permissions、private-auth、failure-atomicity conformance tests。

## 2. 在引擎容器內使用 vendir

**目前不值得。**

優點是主機表面上仍只安裝 Docker、Git、just；vendir binary 被包在多架構引擎 image 裡。

但代價仍存在，只是移入引擎：

- 引擎 image 要攜帶、更新、掃描 vendir。
- vendir 必須透過 bind mount 寫主機 cache。
- 要處理 UID、GID、`0700` 與檔案 ownership。
- 私有 GHCR credential 必須傳進容器。
- Docker config 引用的主機 credential helper 通常不在容器裡。
- 下載不使用 daemon 的既有 image cache。
- OCI index 限制不會消失。

既然主機已經有 Docker，而且 Docker 正是啟動引擎的必要依賴，用 vendir 再建立另一個 registry client 沒有取得目前缺少的核心能力。

## 3. 只有離線包情境使用 vendir

**不值得，而且方向相反。**

vendir `image` 沒有本機 tar／OCI archive 輸入。離線時仍需要可連線 registry，或預先把內容展開；這不能解決 air-gap 問題。

離線情境應沿用或設計：

```text
docker save → 搬運 → docker load → docker create/cp
```

或另定正式的離線包格式。若引入 imgpkg 的 air-gap bundle，那又是另一個 binary、另一種格式與另一套產品決策，不能算 vendir 下載後端的小延伸。

# E. 最終結論

> 以目前需求，vendir 不該進入 vendor_kit：它只能替換一段已能由 Docker 完成的下載／展開流程，卻引入主機 binary 供應鏈、第二條認證路徑、無法關閉的 lock 流程、權限差異、離線能力倒退，以及 OCI multi-arch index 限制；同時完全不能處理 VK 最關鍵的基準版合併。

未來只有在以下可驗證門檻全部成立時才值得重評：

1. 出現一項 Docker 後端確實無法滿足的硬需求，例如正式要求 daemonless fetch，而不是單純少三行指令。
2. vendir 提供官方 `--no-lock`，保證不寫、不讀、不輸出可被誤用為版本真相的 lock。
3. vendir 能直接接受 VK 的完整 `tag@digest` 輸入，不需要持久的第二份 config／lock。
4. 私有 GHCR 在 Jetson、WSL2、Linux amd64/arm64 與 CI 上通過端到端認證測試。
5. Linux amd64/arm64 binary 有固定版本、sha256／簽章驗證、鏡像保存及離線分發方案。
6. 若版本鎖定行使用 OCI index digest，vendir 能可靠依平台解析；否則工具 image 發布契約已明確改成單一 manifest digest。
7. vendir 與 Docker 後端通過相同的內容、權限、symlink、失敗原子性及重跑 golden tests。
8. 團隊已明確接受修改「主機只需 Docker、Git、just」這項承諾。

即使這些門檻全過，vendir 也仍只適合作下載後端；基準版合併與完整開發模式仍必須由 vendor_kit 自己實作。