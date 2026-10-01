# script/diagram — 圖面審查工具

- 舊圖（`discussion.drawio`、`dist_distribution.drawio`、舊 proposal）與產生它們的 `gen57.py`、`gen_disc.py`、`disc_v1_*.py` 已移出 git（#35），副本在 workspace 的 `reference/diagram_legacy/`，舊內容也在 git 歷史與 tag `archive/pr-59`。
- 最新的架構圖在 `doc/diagram/architecture.drawio`，以舊模型畫成，之後依新名詞重畫。
- 這裡留下的工具等 #138（`diagram-edit` workflow）重做時處理：
  - 審查三步（在本目錄跑，輸出目錄放 scratchpad／repo 外）：`python3 extract_pages.py ../../doc/diagram/architecture.drawio <out> [page_id …]` → `python3 lint_pages.py <out>` → `python3 shrink_png.py <pngdir> <outpng> [scale]`；lint 規則寫在 `lint_pages.py` 檔頭。
  - `check_overflow/overlap.py` + `drawio_common.py`：溢字／壓線機械檢查。
  - `STYLE.md`：圖面樣式規範。

## state.py：drawio 頁面 XML 的 HTTP 讀寫與前後比對

透過 drawio MCP server 的 HTTP 端點讀寫頁面，不呼叫 MCP、不開瀏覽器（規則見 [drawio 使用規則](../../doc/agents/drawio.md)）。在 repo 根目錄跑：

- `python3 script/diagram/state.py check`：判斷 session 是否失效（連不上，或 `version == 1` 加上預設空白頁 `<diagram id="blank" name="Page-1">`）。失效就結束碼 1 並說明，不自動開新頁。
- `python3 script/diagram/state.py get <out.drawio>`：讀目前頁面存成檔；session 失效時不寫檔。
- `python3 script/diagram/state.py put <in.drawio>`：把檔載入頁面，回報 `version`。
- `python3 script/diagram/state.py diff <before.drawio> <after.drawio>`：每頁以 `<diagram id>` 對應，列出新增、刪除、改名的頁與每頁 cell 的增刪改；頁 id 消失或新出現另列在 `id_changes`（名字相同、id 不同的列在 `same_name`）。

頁面網址預設從 workspace 的 `reference/drawio_session.txt` 讀（workspace 是主 worktree 根目錄的上一層），也可以用 `--url <網址>` 或 `--session-file <檔>` 指定；`--timeout` 設 HTTP 逾時秒數。輸出一行 JSON；結束碼 0 過、1 有問題、2 用法錯。測試在 `test/`，用假 HTTP server，不依賴 drawio 服務。
