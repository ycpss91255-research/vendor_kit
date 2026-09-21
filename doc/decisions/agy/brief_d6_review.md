題目：#6 本地開發模式的指令形式（使用者已定：用 .version.local 覆蓋檔、不用環境變數；現在要定指令形式，要對齊 base 的用法：base 的 just 全部是命名空間 + flag 選項，例如 just base upgrade --check、just docker build --no-cache；使用者說 dev/undev 應該「用 opt，不要直接給路徑」）

決議 D6：本地開發模式用 .version.local 覆蓋檔，不用環境變數
> 討論紀錄：`dist_distribution_notes.md` §8 #6；草圖：`discussion.drawio`「討論 #6」（定案後搬進正式圖第 4 頁）。

## 決議（2026-09-17）

本地開發模式用 **`.version.local` 覆蓋檔**（與 `.version` 同格式、不進 git、bootstrap 寫進 `.gitignore`）。**不用環境變數**：出問題時要能從檔案追到原因，環境變數留不下紀錄。

- `.version.local` 有 `<name> = "path:../tool"` 那行 → 啟動器改跑 `docker run … -v <path>/dist:/dist:ro <vendor_kit image> --name <name> --dev install`（用 vendor_kit image，dist 用 bind mount）。
- 印記第一行寫 `dev:<路徑>`；verify 看到 `dev:` 前綴 → 不比指紋、每次印醒目警告、重新同步 dist（複製，行為與正式版一致）。
- 指令：`just dev <name> <path>` 寫入並安裝；`just undev <name>` 移除那行並重裝正式版。檔案不存在 = 沒人在用本地版。

## 理由

前例（agy，14 個工具）一致把本地路徑放在「不進 git 的覆蓋檔」：Go 的 `go.work`（提案明寫不應 check in）、docker compose 的 `compose.override.yaml`、`mise.local.toml`、Cargo `.cargo/config.toml [patch]`、Terraform `dev_overrides`（放 CLI 設定檔不放 .tf）。本地路徑一律不做 checksum（go.sum、Cargo.lock、pnpm lockfile 都不記），改印警告（Terraform「Provider development overrides are in effect」）。

## 已排除

- `.version` 直接寫 `path:`：污染 git diff、易誤 commit、CI 要另外擋。
- 環境變數／CLI 旗標（含 agy 建議的 B+C 混合）：無法追蹤。

## 待辦

- [ ] 正式圖第 4 頁「本機開發模式（待設計）」那格改成流程；第 3 頁啟動器讀版本順序加 `.version.local`
- [ ] 原型：`--dev` 參數、`dev:` 印記、`just dev / undev`



要回答：just vendor_kit dev/undev 的指令形式（例如 just vendor_kit dev <name> --path ../tool？just vendor_kit upgrade --local <name>？還是路徑只寫在 .version.local、指令只切開關？）；dev 模式下的 verify/印記/warning；與 base 現有 justfile.base（init/upgrade/update/completions）的對齊。