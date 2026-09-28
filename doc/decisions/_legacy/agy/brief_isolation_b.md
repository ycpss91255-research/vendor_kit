只准用 search_web 與 read_url_content 兩個工具，不要用 run_command。不要執行任何 shell 指令，不要讀寫本機檔案。這是純網路資料調查任務。

# 任務：vendor_kit 如何把「自己的檔」與「使用者的檔」明確切割

## 背景
vendor_kit 讓工具 repo（例如 base）把 dist/ 打包成 OCI image；下游專案用一個版本檔宣告要哪些工具；專案裡一個薄啟動器（just recipe）每次打 just 都先讓快取目錄與版本檔一致。工具帶「初始檔」（例如 compose.yaml、.github/workflows/ci.yml、Dockerfile），第一次接工具時複製到專案指定路徑給使用者、升級時三方合併。原則：vendor_kit 永不刪、永不覆蓋使用者的檔；碰到使用者的東西只有三處：根 justfile 的一行 import、初始檔、.git/info/exclude。使用者希望這三處也盡量切乾淨。主機只有 docker + git + just（just ≥ 1.33）。

## 請回答（每點都要真實案例與可點的連結；沒找到就寫「沒找到」）

### B. 版本檔與工具目錄的命名／位置慣例
4. 工具自己的狀態檔放專案根還是專屬目錄：`.terraform/` + `.terraform.lock.hcl`、`.copier-answers.yml`、`.cruft.json`、`.projen/` + `.projenrc`、`.devcontainer/`、`.mise.toml`／`mise.toml`、`.pre-commit-config.yaml`、`.tool-versions`、`.nvmrc`、`Chart.lock`、`vendir.lock.yml`、`flake.lock`、`.gitmodules`、`.base/`（base subtree）。歸納：什麼情況用「點目錄集中放」、什麼情況「根目錄單檔」；檔名帶工具名（`.copier-answers`）還是通用名（`.version`）的利弊；Renovate custom regex manager（managerFilePatterns / fileMatch）對檔名有沒有限制、對隱藏檔或點目錄下的檔案能否比對。
5. 具體評估三個候選：(a) 現狀 `.version` + `.version.local` + `.vendor_kit/` + `.<repo>/`；(b) 全部收進 `.vendor_kit/`（`.vendor_kit/version.toml`、`.vendor_kit/cache/<repo>/`）；(c) 根檔改名 `.vendor_kit_version`。各自對「一眼看出是 vendor_kit 的」「Renovate regex」「啟動器 grep」「工具 just 模組路徑長度」的影響。列事實與前例即可，不下結論。

輸出：全中文，每點列事實 + 來源 URL（每個前例都要可點的連結）；最後一張表（做法｜前例｜優點｜缺點｜對我們的適用性只列事實不下結論）。請精簡，總長度控制在 200 行內。
