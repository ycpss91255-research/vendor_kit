# ADR-0001：為什麼不用現成工具（vendir／Copier／subtree／submodule／套件管理器）

> Serves: 設計原則 P2（借主機已有的，不養第三方）——這份 ADR 記錄 P2 在「要不要引進現成的搬檔、範本、套件工具」這個問題上的應用，並固定將來重評的門檻。也服務不變量 5（主機只需 docker + git + just）。機制決議，不建立不變量。

- **Status:** Accepted
- **Date:** 2026-09-25
- **Related:** `doc/decisions/design_principles.md` P2、`doc/decisions/review/02_invariants.md` 第 5 條、`doc/decisions/review/01_purpose.md`（第 01 頁只留結論一句，完整比較在本檔）、`doc/decisions/review_log/codex_out_vendir_eval.md`（2026-09-25 vendir 實測與獨立評估）

## Context

vendor_kit 要同時做到四件事：搬檔、鎖版、初始檔升版不蓋掉使用者改的、工具作者能在本機邊改邊測。第 01 頁原本在正文裡逐條比較現有工具，審閱時判定那是決議內容、不是目的陳述，移進本檔；第 01 頁只留一句結論。

硬性限制：

- 設計原則 P2「借主機已有的，不養第三方」（`doc/decisions/design_principles.md`）：拉與展開交給 docker（`create`／`cp`），文字基準版合併交給引擎內的 `git merge-file`，版本追蹤交給 Renovate 一條 regex；vendir、crane、Copier 都不進引擎。
- 不變量 5「主機只需 docker + git + just；正確性不綁單一平台」（`doc/decisions/review/02_invariants.md` 第 5 條）：任何「主機要先裝 X」都會在 Jetson、WSL2、共用工作站其中一台失敗。

已定案的事實：2026-09-18 定案「自寫 + 主機 docker（拉 image）+ 引擎內 git merge-file；第一版不放 vendir/Copier」。

## Decision

不引進 vendir、crane、Copier、cookiecutter，也不用 `git subtree`、`git submodule` 或語言套件管理器當搬檔機制。理由逐項如下。

| 方案 | 工具內容放哪 | 使用者的 git 歷史 | 鎖什麼版本 | 初始檔升版合併 | 本機邊改邊測 | 主機要裝什麼 |
| --- | --- | --- | --- | --- | --- | --- |
| `git subtree` | 複製進 repo | 工具的 commit 混進來 | 無（複製當下） | 不做 | 改完要再合一次 | git |
| `git submodule`（註 1） | 另一個 repo，本地只有 gitlink 指標 | 只有指標進歷史 | 一個 commit | 不做 | 可改 submodule 工作樹，要另外 commit 推上游 | git |
| vendir | 依宣告同步到指定目錄，該目錄整份由它管 | 不進（可 gitignore） | tag 或 digest（多架構 index 要給具體 manifest digest） | 不做（先刪目標目錄再整份換上） | 不做 | vendir |
| Copier | 從範本產生檔案到 repo | 不進 | 範本的 git tag | 做（它的核心功能） | 不做 | Copier（Python） |
| cookiecutter | 從範本產生檔案 | 不進 | 無 | 不做（只產生一次） | 不做 | cookiecutter（Python） |
| 語言套件管理器（npm、pip、cargo）（註 2） | 語言自己的目錄 | 不進 | 版本與 lock 檔 | 不做 | 不做（link／editable 只限該語言產物） | 該語言工具鏈 |
| **vendor_kit** | **搬進 repo，但不進 git** | **只有一行版本鎖定行** | **image tag 加 digest** | **做（基準版合併）** | **做（工具可指到本機目錄）** | **Git、Docker、just** |

註 1：`git submodule` 還要 `clone --recursive` 或額外的初始化步驟，忘了就是空目錄，而且沒有錯誤訊息。
註 2：語言套件管理器只處理該語言的產物，`justfile`、`Dockerfile` 這類純檔案不在它們的範圍內。

### 1. `git subtree`、`git submodule`

把工具的 git 歷史綁進使用者的 repo：工具的 commit 與使用者的 commit 混在一起，正是 vendor_kit 要解的第一個痛點。`submodule` 另外還要求使用者自己記得初始化與更新，漏掉就拿到空目錄或舊版，而且是靜默的。

### 2. vendir

方向與 vendor_kit 最接近，所以單獨實測過：2026-09-25，vendir v0.46.2 linux-amd64、本機 `registry:2`、`FROM scratch` 測試 image，另有一份獨立評估（`doc/decisions/review_log/codex_out_vendir_eval.md`）。

先修掉一個舊說法。實測結果是 **vendir 的 `image` 來源可以直接展開 `FROM scratch` 純資料 image**：不需要 `.imgpkg/` bundle，也不經 docker daemon——它自帶 registry client，能驗證並回報實際解析出的 digest，還能用 `includePaths`／`newRootPath` 只取 `dist/` 裡要的部分。也就是 §5 門檻的第 1 項（能展開現有的 scratch 純資料 image），vendir 其實通得過。不採用的理由換成下面這些。

1. **`sync` 的模型是「這個目錄整份由我管」。** 實測：目標目錄裡使用者新增的檔被刪掉，改過的檔被還原成 image 內容——vendir 先移除目標目錄，再把 staging directory 整份換上去，沒有任何基準版合併，也沒有「改過就不覆蓋」。這與基準版合併、以及「不刪不覆蓋 repo 檔」直接衝突；`ignorePaths`／`manual` 只是讓某些路徑不由它管，不是合併。它適合 `.vendor_kit/cache/<repo>/` 這種由 vendor_kit 完全擁有、可隨時重建的目錄，不適合初始檔所在的 repo 路徑。
2. **多架構 index 挑不了平台。** v0.46.2 內嵌的 imgpkg 對 image index 要求給具體的 manifest digest，不會按主機平台自行挑 manifest（[imgpkg pull 實作](https://github.com/carvel-dev/imgpkg/blob/v0.48.1/pkg/imgpkg/v1/pull.go#L184-L192)）。版本鎖定行若鎖 amd64／arm64 共用的 index digest，vendir 用不了；改成每個平台各鎖一個 digest，就打破「同一行在任何機器裝到同一份內容」。
3. **離線接不上。** `vendir sync` 沒有從本機 tar／OCI archive 匯入的介面，接不上 `docker save`／搬運／`docker load` 那條離線路徑；離線時它仍需要一個連得到的 registry。要走 imgpkg 的 air-gap bundle，那是另一個 binary、另一種格式、另一個產品決策。
4. **認證是第二條路徑。** vendir 走 imgpkg 的 keychain（aks、ecr、gke、github）與 `DOCKER_AUTH_CONFIG`（[imgpkg 認證文件](https://carvel.dev/imgpkg/docs/develop/auth/)）；它雖然也讀得到 `~/.docker/config.json`，但解析順序與主機 docker credential helper 不同，實質是兩套。風險具體是：`docker pull ghcr.io/...` 成功，不保證同一台機器上 `vendir sync` 成功（`$HOME`、`DOCKER_CONFIG`、helper 是否在 `PATH`、WSL2 加 Docker Desktop 都會造成差異）。私有 GHCR 要另外指定並測試一條憑證路徑。
5. **目錄權限不同。** vendir 建的上層目錄是 `0700`，與 repo 內其他目錄的權限預期不一致：要嘛接受這個契約，要嘛同步後自己校正權限，後者又多一層平台與錯誤處理邏輯。
6. **收益很小。** 換掉的只是「建暫存 container」那幾行：`docker create` + `docker cp` + `docker rm`。vendor_kit 本來就要 docker 才能啟動引擎，所以「不經 daemon」沒有移除任何相依，只是多開第二條下載路徑。
7. **多一個第三方 binary。** vendir 會變成正式的執行期相依：固定版本、分發 linux amd64 與 arm64、驗 `checksums.txt`（要來源真實性還得驗 release 的數位簽章而不只是 sha256）、鏡像保存以防 GitHub release 不可達、離線包內帶對架構的 binary、跟升版與 CVE、再測 Jetson／WSL2／CI 的權限與路徑行為。與不變量 5 直接相衝。
8. **lock 檔是第二份版本真相。** 實測：v0.46.2 沒有 `--no-lock`，完整的 remote sync 最後會無條件建立 lock config、印到 stdout、再寫檔（[sync 實作](https://github.com/carvel-dev/vendir/blob/v0.46.2/pkg/vendir/cmd/sync.go)）。可以壓制持久檔案：`--lock-file <path>` 能把它改道到暫存檔，`-d 'dir=local-dir'` 時 vendir 會印 `Lock config is not saved due to command line overrides` 而不寫檔。但沒有官方的「完全不產生 lock」選項，lock 內容照樣出現在 stdout；`--lock-file /dev/null` 不是受支援的用法（不跨平台、`--locked` 會讀到空 lock、partial sync 會嘗試讀舊 lock）。要維持「宣告唯一」就得靠一層嚴格 wrapper 一直防著它。

### 3. Copier、cookiecutter

能做範本與升版合併，但要求範本是帶 tag 的 git repo——vendor_kit 的工具以純資料 image 出貨，不是 git repo；而且它們只在建立時產生一次檔案，不管後續的內容同步，四件事裡只覆蓋到一件的一半。

### 4. 語言的套件管理器（npm、pip、cargo）

只裝自己語言的產物。`justfile`、`Dockerfile`、`.gitignore` 這類純檔案不在它們的範圍內，而那正是 vendor_kit 要搬的東西。

### 5. 重評門檻

將來要把上列任何一個第三方工具放進引擎或主機，先過下列門檻。每一條都要能用一次可重跑的測試、或一份已拍板的文件回答「過了沒有」；「應該可以」「上游有支援」不算過。第 1–4 項就是 P2 原本的四項門檻，第 5 項起是 2026-09-25 的 vendir 實測與獨立評估補上的。

1. 能展開現有的 `FROM scratch` 純資料 image，不要求額外的 bundle 格式（vendir 已通過這一項）。
2. 完全服從宣告：餵 `tag@sha256:<digest>`，工具只裝那一份內容，不自作主張改版本或內容，且能回報實際解析出的 digest 供逐字比對。
3. 私有 registry、多架構、Jetson、WSL2 各有一條端到端驗收並通過，一般 linux amd64／arm64 與 CI 同樣通過；私有 GHCR 的認證路徑明定為其中一條，並在上列每個環境測過。
4. 引進後確實刪掉一整塊自維護程式，而不是在既有程式旁邊再加一層：能指名被刪掉的檔案或函式。
5. 有一項 docker 後端確實做不到的硬需求（例如正式要求 daemonless fetch），且已寫成需求條目——「少三行指令」不算。
6. 不產生第二份版本真相：工具有官方選項保證不寫、不讀、不輸出可被當成版本真相的 lock；或能直接吃 vendor_kit 的完整 `tag@digest`，不需要持久的第二份 config／lock。
7. 多架構 digest 可解析：工具能依主機平台可靠解析 OCI index digest；否則工具 image 的發布契約已明文改成單一、架構無關的 manifest digest，且該改動已記入 ADR。
8. binary 供應鏈有人負責：版本固定、有 sha256 與數位簽章驗證、有鏡像保存、離線包能帶對架構的 binary，並有升版與 CVE 的處理流程。
9. 新後端與現有 docker 後端跑同一組 golden test 且全過：展開內容逐檔相同、檔案與目錄權限相同、symlink 處理相同、失敗時的原子性相同、重跑結果相同。
10. 若該工具會改動「主機只需 docker + git + just」這條承諾，不變量 5 已先修訂並經維護者拍板。

## Consequences

- 得到：主機只需要 `docker`、`git`、`just`；沒有第三方 binary 的安裝、版本、平台支援問題要跟。
- 付出：拉與展開、鎖版、基準版合併、本機開發這幾塊由 vendor_kit 自己維護，bug 也自己修。
- 第 01 頁不再列這四條比較，只留一句結論並指向本檔；兩邊若要改，改本檔為準。
- 驗收：重評門檻第 3 項的私有 registry、多架構、Jetson、WSL2 由驗收層（見「測試分層與強制閘門」ADR 的 acceptance 層）涵蓋。

## Alternatives

- **用 vendir 當下載後端，其餘自寫。** 會滿足「宣告式同步」這一項，實測也確實展開得了 scratch image，但換掉的只有 `docker create`／`cp`／`rm` 那幾行，代價是主機或引擎多一個第三方 binary、第二條認證路徑、關不掉的 lock 流程、`0700` 權限差異、離線能力倒退，以及多架構 index 的限制；`doc/decisions/scope_roadmap.md` 的路線圖已把它排到 v2，且限定「只在通過 §5 門檻後重評」。
- **在引擎容器內跑 vendir（主機表面仍只裝三個工具）。** 代價只是搬進引擎：引擎 image 要帶、更新、掃 vendir，要 bind mount 寫主機 cache 並處理 UID／GID 與 `0700`，私有 GHCR 憑證要傳進容器（主機的 credential helper 通常不在容器裡），下載也用不到 daemon 既有的 image 快取，多架構 index 的限制一項都沒消失。
- **用 Copier 管初始檔，image 只管搬檔。** 會滿足「初始檔升版合併」，代價是工具必須同時以 image 與帶 tag 的 git repo 兩種形式出貨，出貨端要維護兩份來源——違反一條規則一個擁有者（P5）。
- **用 `git submodule` 搬工具、自寫升級腳本。** 會滿足「鎖版」（submodule 記 commit），但工具歷史仍進使用者的 repo，且使用者要多記兩個 git 指令；痛點第一條沒有解決。
