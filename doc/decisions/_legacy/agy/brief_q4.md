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
**限制：請勿執行任何 shell 指令（不要用 terminal/command 工具），只用 web search 與 read_url 查資料。若 8 分鐘內查不完，請先輸出已查到的部分。**

### 4. 回退（rollback）
- 只要把版本檔改回去（git revert）就好的前例：Bazelisk `.bazelversion`、Nix `flake.lock`、Terraform `.terraform.lock.hcl`、Gradle `gradle-wrapper.properties`。它們為什麼可以？（內容可重現、cache by version）
- 需要額外 rollback 紀錄/指令的前例（例如 rustup `toolchain` 切換、`mise` 本地 state、Docker 的 image gc、Helm rollback、Terraform state 版本不可降級）。各自理由。

## 輸出格式
- 繁體中文
- 依 1~5 分節，每個結論後面括號附 URL
- 最後「來源清單」
