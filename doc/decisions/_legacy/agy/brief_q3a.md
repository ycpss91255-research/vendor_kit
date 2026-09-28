# 前例研究 brief：vendor_kit 的 upgrade 流程設計

你是研究員。請用網路搜尋（web search / fetch）查證真實前例，**每一點都要附真實來源連結（官方文件、GitHub issue/PR、changelog）**。不確定或查不到的請明確標「未查到」，不要憑印象編造。輸出用繁體中文，最後附「來源清單」（每條一個 URL）。

## 背景：vendor_kit 框架

- 工具（tool）的 `dist/` 打包成 GHCR container image（`ghcr.io/<org>/<name>:<tag>@sha256:<digest>`）。
- 專案 repo 內有：
  - `.version`：TOML，一行一個工具：`<name> = "ghcr.io/…:tag@sha256:…"`；另有一行 `vendor_kit = "…"` 鎖定啟動器（launcher）本身的版本。
  - `justfile`：使用者自己的，第一行 `import` 啟動器 recipe。
  - `.vendor_kit/`：vendor_kit 寫出的啟動器 recipe，進 git，人不改。
  - `.<name>/`：不進 git，每次 `just` 執行時自動依 `.version` 安裝（從 image 抽出 dist）。
- 主機只有 Docker + git + just。
- 升級 = 改 `.version` 那一行；下次 `just` 自動換新。
- 原則：工具不自動改使用者檔案，只顯示 diff。

## 題目：upgrade 流程要怎麼設計
**限制：請勿執行任何 shell 指令，只用 web search 與 read_url。時間有限（8 分鐘），每個小題最多查 2~3 個來源即輸出，先求有再求全。**

### 3a. 「啟動器自我升級」的做法（Batect、Gradle wrapper）
舊版啟動器去升級新版工具時，新版可能需要新的參數／掛載，怎麼辦？請查：
- Batect：`./batect --upgrade` 如何換自己（wrapper script vs. jar）；是否先換 wrapper 再換 jar；wrapper 與 jar 版本如何綁定。
- Gradle wrapper：`gradle wrapper` 任務由「當前版本」跑，會產生新的 wrapper script+jar+properties，順序如何；官方是否建議「用新版本再跑一次 wrapper」（double-run）；wrapper jar 何時更新。
## 輸出格式
- 繁體中文
- 依 1~5 分節，每個結論後面括號附 URL
- 最後「來源清單」
