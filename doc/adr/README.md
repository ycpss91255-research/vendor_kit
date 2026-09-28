# ADR 索引

vendor_kit 的架構決議紀錄（Architecture Decision Record）索引，以及每份 ADR 對不變量與設計原則的對映。每份 ADR 檔頭有一行 `> Serves:` 回連它所建立或服務的不變量（1–11，見 [`doc/decisions/review/02_invariants.md`](../decisions/review/02_invariants.md)）、設計原則（P1–P6，見 [`doc/decisions/design_principles.md`](../decisions/design_principles.md)）或範圍項目（見 [`doc/decisions/scope_roadmap.md`](../decisions/scope_roadmap.md)）；下表是彙整的檢視。

## 檔案系統即登錄

沒有資料庫、沒有人工維護的編號總表——**`doc/adr/NNNN-<slug>.md` 這組檔案本身就是登錄**（設計原則 P6）。規則：

- 檔名 `NNNN-<slug>.md`：四位數遞增編號 + kebab-case slug。編號在檔案落地時取用，不預留、不重用；被 supersede 的 ADR 保留原檔與編號。
- 本檔 `README.md` 與 `TEMPLATE.md` 的檔名刻意不符合 `NNNN-<slug>.md`，所以不是 ADR、不干擾登錄。
- 之後由 lint 管（待寫，掛在 `just test`）：編號重複或檔名格式錯 → **失敗**；編號有缺口 → 只警告。

## 必要段落規則

每份 ADR 必須在**第 0 欄**（行首）恰好出現一次以下六個部分，順序固定：

| 順序 | 部分 | 內容 |
|---|---|---|
| 1 | `> Serves:` | 一行：服務哪條不變量／原則／範圍項目，以及怎麼服務。純機制決議寫「機制（服務不變量 N），不建立不變量」。 |
| 2 | `- **Status:**` | `Proposed`／`Accepted`／`Rejected`／`Superseded by ADR-NNNN`。 |
| 3 | `## Context` | 為什麼現在要決定；當時的事實與量測；相關 issue。 |
| 4 | `## Decision` | 決定了什麼。性質與機制分開寫：性質屬不變量的只連結不重述；本檔記機制與理由。 |
| 5 | `## Consequences` | 得到什麼、付出什麼、哪些先前決議被修訂。 |
| 6 | `## Alternatives` | 考慮過但沒採的選項，各附一句為什麼不採。 |

之後由 lint 管（待寫）：lint 只看第 0 欄，不認 code fence——所以 ADR 內若要**示例**這些行，示例要縮排；修訂不得再寫第二個 `- **Status:**`，改用 `### 修訂（YYYY-MM-DD）` 標題與 `- **Amendment status:**`。模板見 [`TEMPLATE.md`](TEMPLATE.md)。

語言：繁體中文；識別字、指令、檔名、既有英文段落名（`Context`／`Decision`／`Consequences`／`Alternatives`／`Status`）保留原文。

## 決議流程

1. 討論記在 issue（`ycpss91255-research/vendor_kit`，中文），必要時走 `decision-review`（Claude 子代理 + codex 雙軌）。
2. 定案後寫 ADR：從 `TEMPLATE.md` 起稿，`> Serves:` 指向不變量或設計原則；不變量頁的對應條目若列的是「待寫 ADR-xxxx」，把 xxxx 換成新編號。
3. 一份 ADR 若**建立**了新的不變量或原則，`doc/decisions/review/02_invariants.md`／`doc/decisions/design_principles.md` 同一個 PR 修訂；ADR 記機制，那兩份記性質與判準。
4. 架構圖（`.drawio`）若因決議改變，同一個 PR 更新；圖是測試依據（工作約定見 `../../AGENTS.md`）。

## 索引表

| 編號 | 標題 | 狀態 | Serves |
|---|---|---|---|
| 0001 | 為什麼不用現成工具（vendir／Copier／subtree／submodule／套件管理器） | Accepted | 設計原則 P2（借主機已有的，不養第三方）；不變量 5（主機只需 docker + git + just，見 `../decisions/review/02_invariants.md` 第 5 條） |
| 0002 | VK 的狀態全收進 `.vendor_kit/`，版本鎖定行只認一種正規形 | Accepted | 機制：不變量 2（一份版本鎖定行、進 git）、1（只動有紀錄的檔）、3（自動化只碰不進 git 的東西） |
| 0003 | 初始檔升級走基準版全文加逐檔狀態機，移除只認紀錄原文恰好一處 | Accepted | 機制：不變量 1（可以建、要改先問、永不刪、永不覆蓋）、4（結束碼不由 `git merge-file` 的原生狀態決定） |
| 0004 | VK recipe 一行轉發、寫入邊界，與 CI 模式的封閉紅燈清單 | Accepted | 機制：不變量 8（使用者介面極少；recipe 語意固定）、3（自動化只碰不進 git 的東西）、4（永不靜默失敗） |
| 0005 | 機器可讀的輸出只走執行紀錄，事件名由註冊表封閉 | Accepted | 機制：不變量 4（永不靜默失敗——執行紀錄不可關閉那一段） |
| 0006 | 工具 image 只搬不跑——取件走 `docker create`／`cp`，位元組相同靠三層 | Accepted | 機制：不變量 7（工具 image 只承載交付資料；引擎與工具不互相綁發版）；也服務 5（取件只借主機已有的 docker）、6（引擎單一實作） |
| 0007 | 主機薄層：依賴下限與命令白名單固定，薄殼以自描述標頭鎖住，引擎升級分兩段 | Accepted | 機制：不變量 5（主機依賴最小）、6（引擎版本由安裝目錄鎖定；啟動器不判斷 repo 內容的意義）；也服務 10（舊薄殼遇新 major 的處置） |
| 0008 | 介面版 P 與檔案版 schema 分開計數；版本組合不合就零寫入回 3 | Accepted | 機制：不變量 10（相容性與演進：同一個 X 內不破壞，X 變動才可能不相容且先公告） |
| 0009 | Release 資產的形狀與離線導入——旁檔給 digest，已釋出的永不刪 | Accepted | 機制：不變量 2（決定性重建在提供端）；也服務 10（退得回） |
| 0010 | dev 自身與驗收共用同一條「用指定 image 當引擎」的路 | Accepted | 機制：不變量 9（對外承諾必須黑箱可驗；本機開發與正式啟動走同一個入口）；也服務 10（退得回） |
| 0011 | 測試分層與強制閘門——multi-stage 的固定順序、兩個平台、CI 的 just 矩陣 | Accepted | 機制：不變量 9（驗收 = 真引擎、乾淨 repo、完整流程）、11（正確性不綁單一平台）；架構圖是測試依據（`../../AGENTS.md`） |
| 0012 | 引擎容器內的語言與時區寫死，行尾與跳脫逐處指定 | Accepted | 機制：不變量 11（同一份輸入在每個支援平台得到相同的對外結果） |

## 待拍板（不寫 ADR，直到定案）

`doc/decisions/review/02_invariants.md` 與 `doc/decisions/scope_roadmap.md` 內標「> ⚠ 待拍板」的項目：宣告檔名（`version.toml` vs `lock.toml`）、`just` 最低版本、dist image 單架構 amd64、衝突時 baseline 是否推到新版、Renovate 路徑由 PR 作者本機補合併、多命名空間工具、image 公開／私有、`.gitignore` 類初始檔。每項定案後併入上表對應主題的 ADR，或獨立成一份。
