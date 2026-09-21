# ADR 索引

vendor_kit 的架構決議紀錄（Architecture Decision Record）索引，以及每份 ADR 對 [`doc/PRD.md`](../PRD.md)（北極星）的對映。每份 ADR 檔頭有一行 `> Serves:` 回連它所建立或服務的 PRD 不變量（1–10）、設計原則（P1–P6）或範圍項目；下表是彙整的檢視。

## 檔案系統即登錄

沒有資料庫、沒有人工維護的編號總表——**`doc/adr/NNNN-<slug>.md` 這組檔案本身就是登錄**（PRD 設計原則 P6）。規則：

- 檔名 `NNNN-<slug>.md`：四位數遞增編號 + kebab-case slug。編號在檔案落地時取用，不預留、不重用；被 supersede 的 ADR 保留原檔與編號。
- 本檔 `README.md` 與 `TEMPLATE.md` 的檔名刻意不符合 `NNNN-<slug>.md`，所以不是 ADR、不干擾登錄。
- 之後由 lint 管（待寫，掛在 `just test`）：編號重複或檔名格式錯 → **失敗**；編號有缺口 → 只警告。

## 必要段落規則

每份 ADR 必須在**第 0 欄**（行首）恰好出現一次以下六個部分，順序固定：

| 順序 | 部分 | 內容 |
|---|---|---|
| 1 | `> Serves:` | 一行：服務 PRD 哪條不變量／原則／範圍項目，以及怎麼服務。純機制決議寫「機制（服務不變量 N），不建立不變量」。 |
| 2 | `- **Status:**` | `Proposed`／`Accepted`／`Rejected`／`Superseded by ADR-NNNN`。 |
| 3 | `## Context` | 為什麼現在要決定；當時的事實與量測；相關 issue。 |
| 4 | `## Decision` | 決定了什麼。性質與機制分開寫：性質屬 PRD 的只連結不重述；本檔記機制與理由。 |
| 5 | `## Consequences` | 得到什麼、付出什麼、哪些先前決議被修訂。 |
| 6 | `## Alternatives` | 考慮過但沒採的選項，各附一句為什麼不採。 |

之後由 lint 管（待寫）：lint 只看第 0 欄，不認 code fence——所以 ADR 內若要**示例**這些行，示例要縮排；修訂不得再寫第二個 `- **Status:**`，改用 `### 修訂（YYYY-MM-DD）` 標題與 `- **Amendment status:**`。模板見 [`TEMPLATE.md`](TEMPLATE.md)。

語言：繁體中文；識別字、指令、檔名、既有英文段落名（`Context`／`Decision`／`Consequences`／`Alternatives`／`Status`）保留原文。

## 決議流程

1. 討論記在 issue（`ycpss91255-research/vendor_kit`，中文），必要時走 `decision-review`（Claude 子代理 + codex 雙軌）。
2. 定案後寫 ADR：從 `TEMPLATE.md` 起稿，`> Serves:` 指向 PRD；PRD 的對應不變量若列的是「待寫 ADR-xxxx」，把 xxxx 換成新編號。
3. 一份 ADR 若**建立**了新的不變量或原則，PRD 同一個 PR 修訂；ADR 記機制，PRD 記性質。
4. 架構圖（`.drawio`）若因決議改變，同一個 PR 更新；圖是測試依據（PRD 不變量 10）。

## 索引表

| 編號 | 標題 | 狀態 | Serves |
|---|---|---|---|
| 0001 | 測試分層與強制閘門 | Accepted；**在 `../proto/vendor_kit/doc/adr/`，待搬回**；搬回時補 `> Serves:` 行，acceptance 層改為 PRD 不變量 9 的完整流程 | 不變量 9（驗收 = 真引擎、乾淨下游、完整流程）、10（架構圖是測試依據） |
| 0002 | 引擎與工具 image 分離（乙版） | Accepted；**在 proto，待搬回**；搬回時補 `> Serves:`，並修訂 §3（`gen/` 改用 `.vendor_kit/.gitignore`，不碰 `.git/info/exclude`）與 §5（`just` 最低版本待拍板） | 不變量 7（工具 image 純資料；引擎與工具分離）、6（引擎版本由專案鎖定；啟動器薄殼）；也服務 5（主機只需三個工具） |

## 計畫中的 ADR

以下決議已在 grilling／decision-review 定案（來源：`scratchpad/decisions/grilling.md`、`interface.md`、`isolation.md`、`prior_art.md`、`devmode.md`），尚未寫成 ADR。編號在檔案落地時取用；PRD 目前以「待寫 ADR-xxxx（<主題>）」引用。

| 主題 | 決定了什麼（摘要） | Serves |
|---|---|---|
| 介面動詞 | 常用 `add`／`upgrade`／`dev`，進階 `remove`／`undev`／`update`／`sync`／`install`／`uninstall`；`update` 只查／`upgrade` 套用（跟 base）；結束狀態 0/1/2；`sync` 只寫 ignored 路徑、CI 下需 tracked 寫入即失敗；一行 `verb *args` 轉發放 tracked `vendor.just`；不開 `init`／`diff`／`accept`／`rollback` | 不變量 3、4、8；P1、P3、P4 |
| 檔案佈局 | 全收進 `.vendor_kit/`（`version.toml`、`version.local.toml`、`cache/<repo>/`、`gen/`、`baseline/<repo>/`、自有 `.gitignore`）；根 `justfile` 無則建、有則詢問加一行；不碰 `.git/info/exclude` 與使用者 `.gitignore`；工具 recipe 用 `cd "{{justfile_directory()}}"` 回專案根 | 不變量 1、2；P1 |
| 初始檔合併 | `add` 建、已存在不納管（`adopted=false`）只 warn；`upgrade` 逐檔狀態機（`disk==new` 不動 → `old==new` 不動 → `disk==old` 詢問換新版 → 三方 `git merge-file --diff3` 詢問合併，衝突留標記回 2）；`-y` 免問；永不刪（上游刪檔只 warn）；二進位只比對不合併；「永不覆蓋」的正式定義與兩個例外 | 不變量 1、4；P3 |
| bootstrap 薄層 | `bootstrap.sh` = 下載引擎 + 呼叫 `install`，再跑 = 修復、不自刪、EOF 不算同意；`install` 要求已是 git repo、不做 `git init`；啟動器 POSIX sh 只用 `docker` + `grep`／`sed`、只讀宣告第一行；主機 `docker create`／`cp` 拉 dist；不引進 vendir／crane／Copier（四項門檻記入） | 不變量 5、6；P2、P5 |
| dev 自身與驗收 | `dev <repo> -p <dir>`／`undev <repo>`；`dev` 要求工具已在宣告；`dev vendor_kit -i <image>` 用 `version.local.toml` 覆寫引擎；驗收用剛 build 的引擎 image 在乾淨 fixture repo 跑 `install → add → upgrade → dev/undev → remove → uninstall`；CI 下拒絕 dev | 不變量 9；ADR-0001 的 acceptance 層 |

## 待拍板（不寫 ADR，直到定案）

PRD 內標「> ⚠ 待拍板」的項目：宣告檔名（`version.toml` vs `lock.toml`）、`just` 最低版本、dist image 單架構 amd64、衝突時 baseline 是否推到新版、Renovate 路徑由 PR 作者本機補合併、多命名空間工具、image 公開／私有、`.gitignore` 類初始檔。每項定案後併入上表對應主題的 ADR，或獨立成一份。
