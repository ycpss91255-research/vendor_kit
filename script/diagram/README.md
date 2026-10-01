# script/diagram — 圖面審查工具

- 舊圖（`discussion.drawio`、`dist_distribution.drawio`、舊 proposal）與產生它們的 `gen57.py`、`gen_disc.py`、`disc_v1_*.py` 已移出 git（#35），副本在 workspace 的 `reference/diagram_legacy/`，舊內容也在 git 歷史與 tag `archive/pr-59`。
- 最新的架構圖在 `doc/diagram/architecture.drawio`，以舊模型畫成，之後依新名詞重畫。
- 這裡留下的工具等 #138（`diagram-edit` workflow）重做時處理：
  - 審查三步（在本目錄跑，輸出目錄放 scratchpad／repo 外）：`python3 extract_pages.py ../../doc/diagram/architecture.drawio <out> [page_id …]` → `python3 lint_pages.py <out>` → `python3 shrink_png.py <pngdir> <outpng> [scale]`；lint 規則寫在 `lint_pages.py` 檔頭。
  - `check_overflow/overlap.py` + `drawio_common.py`：溢字／壓線機械檢查。
  - `STYLE.md`：圖面樣式規範。
