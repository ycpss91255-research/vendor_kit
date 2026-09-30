# 不用現成的搬檔、範本與套件工具

vendor_kit 要同時做到搬檔、鎖版、初始檔升版不蓋掉使用者改的、工具作者能在本機邊改邊測，而主機只能假設 Docker、Git、just（[不變量 5](../contract/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)）。所以不引進 vendir、crane、Copier、cookiecutter，也不用 `git subtree`、`git submodule` 或語言套件管理器當搬檔機制：拉與展開交給主機的 docker（`create`／`cp`），基準版合併交給引擎內的 `git merge-file`，版本追蹤交給 Renovate 一條 regex（[設計原則 P2](../../doc/decisions/design_principles.md)）。現成工具各自只涵蓋四件事的一部分，換掉的程式很少，卻要多養一個第三方依賴。

## Considered Options

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

- **`git subtree`**：把工具的 commit 合進使用者的 repo，工具的 commit 與使用者的 commit 混在一起，正是 vendor_kit 要解的第一個痛點。
- **`git submodule`**：工具的 commit 不進使用者的 repo，歷史裡只有 gitlink 指標；代價是多一個 repo，也多出初始化與更新的狀態要使用者自己記得，漏掉就拿到空目錄或舊版，而且是靜默的。用 submodule 搬工具、再自寫升級腳本，可以鎖版，但多出來的 repo 與初始化狀態都還在。
- **vendir**：方向最接近，所以單獨實測過（vendir v0.46.2 linux-amd64、本機 `registry:2`、`FROM scratch` 測試 image，另有[獨立評估](../../doc/decisions/review_log/codex_out_vendir_eval.md)）。它的 `image` 來源可以直接展開 `FROM scratch` 純資料 image，不需要 `.imgpkg/` bundle、不經 docker daemon，還能用 `includePaths`／`newRootPath` 只取 `dist/` 的一部分。不採用的理由：
  1. `sync` 的模型是「這個目錄整份由我管」：實測時目標目錄裡使用者新增的檔被刪、改過的檔被還原。它先移除目標目錄再整份換上，沒有基準版合併，也沒有「改過就不覆蓋」；`ignorePaths`／`manual` 只是讓某些路徑不歸它管，不是合併。它只適合 `.vendor_kit/cache/<repo>/` 這種 VK 完全擁有、可隨時重建的目錄。
  2. 多架構 index 挑不了平台：內嵌的 imgpkg 要求給具體的 manifest digest，不會依主機平台挑（[imgpkg pull 實作](https://github.com/carvel-dev/imgpkg/blob/v0.48.1/pkg/imgpkg/v1/pull.go#L184-L192)）。改成每個平台各鎖一個 digest，就打破「同一行在任何機器裝到同一份內容」。
  3. 離線接不上：`vendir sync` 沒有從本機 tar／OCI archive 匯入的介面，接不上 `docker save`／`docker load` 的離線路徑；要走 imgpkg 的 air-gap bundle，是另一個 binary、另一種格式。
  4. 認證是第二條路徑：它走 imgpkg 的 keychain 與 `DOCKER_AUTH_CONFIG`（[imgpkg 認證文件](https://carvel.dev/imgpkg/docs/develop/auth/)），解析順序與主機 docker 的 credential helper 不同。`docker pull ghcr.io/...` 成功，不保證同一台機器上 `vendir sync` 成功。
  5. 它建的上層目錄是 `0700`，與 repo 內其他目錄的權限預期不一致，要嘛接受、要嘛同步後自己校正。
  6. 收益很小：換掉的只是 `docker create` + `docker cp` + `docker rm` 那幾行。VK 本來就要 docker 才能啟動引擎，「不經 daemon」沒有移除任何依賴。
  7. 多一個第三方 binary：要固定版本、分發 amd64 與 arm64、驗 `checksums.txt` 與 release 的數位簽章、鏡像保存、離線包帶對架構的 binary、跟升版與 CVE，再測 Jetson／WSL2／CI。與不變量 5 直接相衝。
  8. lock 檔是第二份版本真相：v0.46.2 沒有 `--no-lock`，完整的 remote sync 最後一定建立 lock、印到 stdout 再寫檔（[sync 實作](https://github.com/carvel-dev/vendir/blob/v0.46.2/pkg/vendir/cmd/sync.go)）。`--lock-file <path>` 或 `-d 'dir=local-dir'` 只能壓制持久檔，`--lock-file /dev/null` 不是受支援的用法；要維持「宣告唯一」就得靠一層 wrapper 一直防著它。
- **在引擎容器內跑 vendir**：主機表面仍只裝三個工具，但代價沒有消失，只是搬進引擎：引擎 image 要帶、更新、掃 vendir，要 bind mount 寫主機 cache 並處理 UID／GID 與 `0700`，私有 GHCR 憑證要傳進容器，用不到 daemon 既有的 image 快取，多架構 index 的限制也沒消失。
- **Copier、cookiecutter**：能做範本與升版合併，但要求範本是帶 tag 的 git repo，而 VK 的工具以純資料 image 出貨；它們也只在建立時產生一次檔案，不管後續的內容同步。用 Copier 管初始檔、image 只管搬檔，工具就得同時以 image 與 git repo 兩種形式出貨，違反[設計原則 P5](../../doc/decisions/design_principles.md#p5-一條規則一個擁有者)（一條規則一個擁有者）。
- **語言套件管理器（npm、pip、cargo）**：只裝自己語言的產物。`justfile`、`Dockerfile`、`.gitignore` 這類純檔案不在範圍內，而那正是 VK 要搬的東西。

## Consequences

- 主機只需要 Docker、Git、just；沒有第三方 binary 的安裝、版本、平台支援要跟。代價是拉與展開、鎖版、基準版合併、本機開發這幾塊由 VK 自己維護。
- [01 目的與承諾](../contract/01_purpose.md)留對外結論，本 ADR 留完整取捨；承諾改變時，先依對外契約的審閱流程改 01，再同步本檔。
- 重評門檻（[設計原則 P2](../../doc/decisions/design_principles.md) 與[範圍與路線圖](../../doc/decisions/scope_roadmap.md)所說的「十項門檻」就是這份清單）：將來要把上列任何第三方工具放進引擎或主機，每一項都要能用一次可重跑的測試、或一份已拍板的文件回答「過了沒有」；「應該可以」「上游有支援」不算過。第 1～4 項是 P2 原本的四項，第 5 項起是 vendir 實測與獨立評估補上的。
  1. 能展開現有的 `FROM scratch` 純資料 image，不要求額外的 bundle 格式（vendir 已通過這一項）。
  2. 完全服從宣告：餵 `tag@sha256:<digest>`，工具只裝那一份內容，不自作主張改版本或內容，且能回報實際解析出的 digest 供逐字比對。
  3. 私有 registry、多架構、Jetson、WSL2 各有一條端到端驗收並通過，一般 linux amd64／arm64 與 CI 同樣通過；私有 GHCR 的認證路徑明定為其中一條，並在上列每個環境測過。
  4. 引進後確實刪掉一整塊自維護程式，而不是在既有程式旁邊再加一層：能指名被刪掉的檔案或函式。
  5. 有一項 docker 後端確實做不到的硬需求（例如正式要求 daemonless fetch），且已寫成需求條目；「少三行指令」不算。
  6. 不產生第二份版本真相：工具有官方選項保證不寫、不讀、不輸出可被當成版本真相的 lock；或能直接吃 VK 的完整 `tag@digest`，不需要持久的第二份 config／lock。
  7. 多架構 digest 可解析：工具能依主機平台可靠解析 OCI index digest；否則工具 image 的發布契約已明文改成單一、架構無關的 manifest digest，且該改動已記入 ADR。
  8. binary 供應鏈有人負責：版本固定、有 sha256 與數位簽章驗證、有鏡像保存、離線包能帶對架構的 binary，並有升版與 CVE 的處理流程。
  9. 新後端與現有 docker 後端跑同一組 golden test 且全過：展開內容逐檔相同、檔案與目錄權限相同、symlink 處理相同、失敗時的原子性相同、重跑結果相同。
  10. 若該工具會改動「主機只需 Docker、Git、just」這條承諾，不變量 5 已先修訂並經維護者拍板。
- 門檻第 3 項的私有 registry、多架構、Jetson、WSL2 由驗收層涵蓋（[ADR-0011](0011-test-layers-and-ci-matrix.md)）。
