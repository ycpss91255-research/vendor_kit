只准用 search_web 與 read_url_content 兩個工具，不要用 run_command。不要執行任何 shell 指令，不要讀寫本機檔案。這是純網路資料調查任務。

# 任務：為 vendor_kit 框架的「upgrade 流程」做前例研究

## 背景

vendor_kit 框架：
- 各工具的 dist/ 打包成 GHCR image（`<name>-dist:vX`，FROM vendor_kit image）。
- 專案 repo 有：
  - `.version`（TOML，一行一工具 `<name> = "ghcr.io/…:tag@sha256:…"`，另一行 `vendor_kit = "…"` 鎖啟動器版本）
  - `justfile`（使用者自己的，只有一行 import）
  - `.vendor_kit/`（vendor_kit 寫出的啟動器 recipe + `baseline/<name>/` 舊版範本副本，進 git）
  - `.<name>/`（不進 git，每次執行 just 時自動依 .version 安裝）
- 主機只有 Docker + git + just。
- 升級 = 改 .version 那一行；下次 just 自動換新；升級後使用者 `just diff`（三方 diff）看範本差異、`just accept` 更新基準。
- 原則：工具不自動改使用者檔。
- 回退 = 把 .version 改回去。

## 要查並回答的題目（每一點都要附真實案例的 URL 連結；查不到就寫「未查到」，不要編造）

1. **Renovate 對「GHCR image 以 tag@digest 記在自訂 TOML 檔」的支援**：
   - 該用哪種 manager（custom regex manager / docker datasource）？
   - PR 長什麼樣（標題、body、改動）？找真實 PR 範例連結。
   - digest pinning 與 tag 同時更新（tag@sha256 一起換）需要什麼設定（例如 `pinDigests`、`currentDigestTemplate`、`versioningTemplate`、`autoReplaceStringTemplate`）？
   - Dependabot 做不做得到（自訂檔案的 docker digest 更新）？附官方文件或 issue 連結。


2. **「手動升級指令」前例對照**：Gradle `wrapper --gradle-version`、Batect `--upgrade`、mise `upgrade`、pre-commit `autoupdate`、Terraform `init -upgrade`。針對每一個查：
   - 查最新版的方式（打哪個 API / registry / 什麼 lockfile）
   - 改版本檔後是否立即安裝（還是只改檔、下次執行才裝）
   - 有沒有「只改檔不裝」或 dry-run 選項
   - 能否指定單一工具/單一 repo 升級（例如 `pre-commit autoupdate --repo`、`mise upgrade <tool>`）
   附官方文件連結。


## 輸出格式

用繁體中文，Markdown，章節依題目 1–2 排列。每個結論都附來源 URL（完整 https:// 連結）。不要憑印象補內容；查不到就標「未查到」。
