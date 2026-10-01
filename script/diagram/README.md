# script/diagram — 圖產生器與審查工具

- `python3 script/diagram/gen_disc.py`：產生 repo 根 `discussion.drawio`（77 頁：68 頁 v1p* 提案圖 + 9 頁討論）；任何 cwd 都可跑（腳本自己 chdir 到本目錄，helper 取自最新 `gen[0-9]*.py`，頁面來自 `disc_v1_a/b/c.py`）。
- `python3 script/diagram/gen57.py`：產生 repo 根 `dist_distribution.drawio`（正式圖）；同樣任何 cwd 都可跑。
- 審查三步（在本目錄跑，輸出目錄放 scratchpad／repo 外）：`python3 extract_pages.py ../../discussion.drawio <out> [page_id …]` → `python3 lint_pages.py <out>` → `python3 shrink_png.py <pngdir> <outpng> [scale]`；lint 規則寫在 `lint_pages.py` 檔頭。
- `check_overflow/overlap.py` + `drawio_common.py`：溢字／壓線機械檢查。
- 一次性產物（`_backup/`、`_misc/`、`r12_codex/`、`r13_codex/`、`r15_codex/`、`push_*.py`、`verify_r15/16.py`、`finish_r15.py`、`review_v2_README.md`）已刪（#144），舊內容在 git 歷史與 tag `archive/pr-59`。
- 路徑已全部由 scratchpad 絕對路徑改為相對 repo（輸出寫 `../../*.drawio`）；`grep -rn /tmp/claude script/ doc/` 為 0。
