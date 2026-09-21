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
### 5. 建議流程
根據以上前例，給出 vendor_kit upgrade 的建議流程，分四條路徑：
- (A) Renovate 路徑：機器人開 PR 改 `.version`（tag+digest）；CI 跑 `just`；人 merge。
- (B) `just upgrade <name>` 路徑：啟動器查 registry 最新 tag+digest（查法？用 `docker manifest inspect`/`crane`/`skopeo`/GHCR API？主機只有 Docker），只改 `.version` 或同時安裝？顯示 diff？
- (C) vendor_kit 自身升級路徑：先換 `.vendor_kit/` recipe 再換工具？舊 recipe 如何 bootstrap 新 recipe？
- (D) 回退：改回 `.version` 即可？`.<name>/` 快取要不要按 digest 分目錄？
每一步標明誰做（機器人／使用者／啟動器／容器）。並指出每條路徑的前例依據（連結）。

## 輸出格式
- 繁體中文
- 依 1~5 分節，每個結論後面括號附 URL
- 最後「來源清單」
