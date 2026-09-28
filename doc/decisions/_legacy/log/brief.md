# 題目：vendor_kit 的操作紀錄檔（audit／operation log）

## 背景
vendor_kit 是一個 CLI 工具：專案 repo 用 `just vendor_kit <動詞>` 呼叫薄啟動器（POSIX sh），啟動器起一個 docker 容器跑引擎（Python），引擎以 `resolve`（唯讀）→ `apply`（寫入）兩段修改專案裡的 `.vendor_kit/` 與少數使用者檔。動詞：install／uninstall、add／remove、update（只查）／upgrade（套用）、dev／undev、sync、prune、help。每個動詞現在只把進度與診斷印到 stderr（tty），另外有交易恢復用的「進度日誌」（`.vendor_kit/.tmp.<verb>.<id>.toml` 或 metadata `[progress]`，成功後刪）。

## 新需求（使用者 2026-09-20）
除了印到 tty，每個動作還要**寫入檔案**，事後能看到「做了什麼、哪些執行過」：
- 每個動詞每次執行都要留下紀錄（開始、每個寫入／刪除／詢問／同意、結束碼、耗時）。
- log 資料夾要明確被 `.gitignore`／`.dockerignore` 排除。
- log 格式要參考業界推薦；使用者之前整理過的筆記結論：JSON Lines、欄位對齊 OpenTelemetry Logs Data Model（`timestamp` ISO 8601 UTC、`severity_text`、`body` = 事件名（有限集合）、`trace_id`、`attributes{…}`），用 `jq`／`lnav` 查。

## 硬性限制
- 引擎在容器內跑、以主機 uid 執行，只掛專案目錄 `/repo`；log 只能寫在專案目錄底下（例如 `.vendor_kit/log/`）或明確的位置。
- 啟動器是 POSIX sh，不能依賴 jq／python；啟動器自己那段（docker pull、create/cp）也要留紀錄。
- 「never fail silently」；log 寫不進去不能讓動詞靜默失敗，但也不該讓唯讀動詞因為 log 失敗而回非 0？（要討論）
- 不可洩漏憑證（registry token）進 log。
- 不進 git、不進 docker build context。
- 使用者檔四原則（可以建、要改先問、永不刪、永不覆蓋）不適用 log（log 是 vendor_kit 自己的檔），但要有大小／保留策略，不能無限長大。

## 想知道的
1. 類似 CLI 工具（apt／dpkg、pip、npm、cargo、terraform、pre-commit、renovate、git 的 reflog、docker）怎麼留操作紀錄：位置、格式、輪替／保留、一次執行一檔還是追加。
2. JSON Lines + OTel Logs Data Model 欄位用在單機 CLI 工具是否合適；有沒有更輕的慣例（例如 `logfmt`）；業界對「audit log」與「debug log」分開的建議。
3. 一次執行一檔（`<ts>-<verb>-<id>.jsonl`）vs 單檔追加（`vendor_kit.jsonl`）+ 輪替：各自優缺點、保留策略常見數字。
4. 容器內寫檔到掛載目錄的坑（權限、原子寫入、flock）。
5. lnav 的 JSON format file 需要哪些欄位才能用 timeline view。
