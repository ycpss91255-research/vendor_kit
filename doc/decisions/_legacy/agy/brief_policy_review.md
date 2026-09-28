題目：政策類待決一次定案：#3 GHCR 舊 image 清理（要涵蓋 baseline metadata 引用的版本）、#4 image cache 範圍、#7 既有 15 個 repo 遷移順序、#9 agent_harness 是否納入、#10 是否保留 --migrate、#14(模板變數) 是否帶入變數渲染。

## 8. 待決議

| # | 議題 | 目前傾向 |
|---|---|---|
| 1 | `.version` 記什麼 | **已定**：一個 `.version` 檔（TOML，`[tools]` 下一個工具一行 `name = "ghcr.io/…:tag@sha256:…"`）；digest 鎖內容、tag 供 Renovate 判斷版本系列；name 決定安裝目錄 `.<name>/` |
| 2 | `.<name>/` 是否進 git | **已定**：不進 git |
| 3 | image 清理策略 | 被引用的版本一律保留；未被引用的版本可定期清理（週期未定） |
| 4 | image cache 範圍（機器共用 vs 每 repo 隔離） | 未定 |
| 5 | launcher 契約版本與更新方式 | **已定（§12、issue #20）**：啟動器 = `.vendor_kit/`，由 `bootstrap` 子命令寫出、進 git、人不改；`.version` 有 `vendor_kit = "…"` 一行，升級時換 `vendor.just`／`tools.just`／`.stamp`（`baseline/` 不動）；使用者的 `justfile` 只 import 它。第一次進專案 = release 附的 `bootstrap.sh`（跑完自刪） |
| 6 | 本地開發模式的切換方式 | **已定（issue #21，第 4 頁）**：`.version.local` 覆蓋檔（同格式、不進 git，bootstrap 寫進 .gitignore），`<name> = "path:../tool"` 那行優先；用 vendor_kit image 掛本機 dist 安裝，印記第一行 `dev:<路徑>`，verify 跳過只印警告、每次重新複製；`just dev <name> <path>`／`just undev <name>`。不用環境變數（出問題要能從檔案追） |
| 7 | 既有 15 個 repo 的遷移順序 | 建議從 v0.41 直接跳新機制，不先走 v0.42/v0.43 subtree 遷移；試點 urg_node_humble（簡單）+ isaac（複雜） |
| 8 | vendor_kit 既有 issue 的處置 | #7、#13 等 rollback 相關議題可能失效，需逐一重審 |
| 9 | agent_harness 是否納入同一機制 | 其內容（AGENTS.md、skills）屬 init.toml 類；先做只服務 base 的最小版本，再驗證通用性 |
| 10 | 是否保留自動遷移 `just upgrade --migrate` | 預設不動；等 dist 路徑契約穩定後再評估 |
| 11 | `diff` 是否做三方比對 | **已定（issue #22，第 5 頁）**：三方、只顯示不寫回；基準 = `.vendor_kit/baseline/<name>/`（每工具一份，進 git，人不改、納入檢查）；init 從第一版就寫基準（碰到已存在的檔 → warn、不覆蓋、仍存基準）；`just accept <name>` 更新基準；結束狀態 0 沒差異／1 工具有改／2 可能重疊；兩個工具 init 到同一 dest → 報錯；第一版檔案層級五分類＋兩份 diff，第二版自寫 diff3 |
| 12 | `verify` 的基準 | **已定（issue #23，第 5 頁）**：基準 = `.version` 鎖定的 image 內 `/dist`（verify 本來就在該工具容器內跑，不多起容器、不上網）；兩棵樹比對：檔案集合（缺、多都失敗，只豁免 .stamp）＋ sha256 ＋ 執行位（單向）＋ 型別（第一版禁 symlink）；不比 mtime／owner；印記降為「已裝版本」快取鍵（第一行 = `--self`），不簽章；失敗中止不自動重裝；第一版不做 stat 快取 |
| 13 | 並行安裝的 lock | **已定（issue #24，第 5 頁）**：flock 鎖專案目錄本身（不建鎖檔；install／accept 排他、verify 共享）；拿到鎖後重讀 .version 與印記，已是目標版本就跳過複製仍 verify；逾時預設 60 秒（環境變數可改，0 = 立即失敗）；鎖不支援 → 直接失敗，`VENDOR_KIT_NO_LOCK=1` 才放行，不退回 mkdir 鎖；暫存目錄亂數名並清殘留；`docker run --init`；平台 = Linux amd64／arm64（含 WSL2） |
| 14 | 模板是否帶入變數（專案名等）渲染 | 目前只複製；圖上標「待定」 |



我方傾向：#3 被任何 .version（含歷史 commit 與 baseline metadata）引用就保留、其餘 90 天清、先不自動化；#4 用 Docker 預設機器共用；#7 從 v0.41 直接跳新機制、先試 urg_node_humble + isaac；#9 納入（第二個工具 repo）；#10 不做；#14 模板變數先不做（純複製，變數用工具自己的 setup.toml 在執行期讀）。