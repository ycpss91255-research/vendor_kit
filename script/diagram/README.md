# script/diagram — 圖產生器與審查工具

- `python3 script/diagram/gen_disc.py`：產生 repo 根 `discussion.drawio`（77 頁：68 頁 v1p* 提案圖 + 9 頁討論）；任何 cwd 都可跑（腳本自己 chdir 到本目錄，helper 取自最新 `gen[0-9]*.py`，頁面來自 `disc_v1_a/b/c.py`）。
- `python3 script/diagram/gen57.py`：產生 repo 根 `dist_distribution.drawio`（正式圖）；同樣任何 cwd 都可跑。
- 審查三步（在本目錄跑，輸出目錄放 scratchpad／repo 外）：`python3 extract_pages.py ../../discussion.drawio <out> [page_id …]` → `python3 lint_pages.py <out>` → `python3 shrink_png.py <pngdir> <outpng> [scale]`；細節與 lint 規則見 `review_v2_README.md`。
- `push_*.py`：把 v1p* 頁推到 draw.io MCP session（127.0.0.1:6002）；`verify_r15/16.py`、`finish_r15.py`：審閱頁逐字比對與 PNG 白底化；`check_overflow/overlap.py` + `drawio_common.py`：溢字／壓線機械檢查。
- `_backup/`：歷代版本痕跡（gen2–56、make_gen*、disc_v1_*.py.v*／.pre_r16、lint_pages.py.v1 …），不維護。`_misc/`：一次性 patch／診斷腳本（patch_r*、finish_r5–14、check_*、cellfind …），多數假設 cwd 有 `v2_only.drawio` 或 `disc_v1_b.py`，用前自行調整。
- 路徑已全部由 scratchpad 絕對路徑改為相對 repo（輸出寫 `../../*.drawio`）；`grep -rn /tmp/claude script/ doc/` 為 0。
