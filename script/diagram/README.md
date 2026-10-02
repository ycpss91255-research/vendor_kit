# script/diagram — 圖面審查工具

- 舊圖（`discussion.drawio`、`dist_distribution.drawio`、舊 proposal）與產生它們的 `gen57.py`、`gen_disc.py`、`disc_v1_*.py` 已移出 git（#35），副本在 workspace 的 `reference/diagram_legacy/`，舊內容也在 git 歷史與 tag `archive/pr-59`。
- 最新的圖分成兩個檔（#278）：架構圖在 `doc/diagram/architecture.drawio`，流程圖在 `doc/diagram/flow.drawio`；以舊模型畫成，之後依新名詞重畫。
- 這裡留下的工具等 #138（`diagram-edit` workflow）重做時處理：
  - 審查三步（在本目錄跑，輸出目錄放 scratchpad／repo 外）：`python3 extract_pages.py ../../doc/diagram/architecture.drawio <out> [page_id …]`（流程圖把檔名換成 `../../doc/diagram/flow.drawio`） → `python3 lint_pages.py <out>` → `python3 shrink_png.py <pngdir> <outpng> [scale]`；lint 規則寫在 `lint_pages.py` 檔頭。
  - `check_overflow/overlap.py` + `drawio_common.py`：溢字／壓線機械檢查。
  - `STYLE.md`：圖面樣式規範。

## state.py：drawio 頁面 XML 的 HTTP 讀寫與前後比對

透過 drawio MCP server 的 HTTP 端點讀寫頁面，不呼叫 MCP、不開瀏覽器（規則見 [drawio 使用規則](../../doc/agents/drawio.md)）。在 repo 根目錄跑：

- `python3 script/diagram/state.py check`：判斷 session 是否失效（連不上，或 `version == 1` 加上預設空白頁 `<diagram id="blank" name="Page-1">`）。失效就結束碼 1 並說明，不自動開新頁。
- `python3 script/diagram/state.py get <out.drawio>`：讀目前頁面存成檔；session 失效時不寫檔。
- `python3 script/diagram/state.py put <in.drawio>`：把檔載入頁面，回報 `version`。
- `python3 script/diagram/state.py diff <before.drawio> <after.drawio>`：每頁以 `<diagram id>` 對應，列出新增、刪除、改名的頁與每頁 cell 的增刪改；頁 id 消失或新出現另列在 `id_changes`（名字相同、id 不同的列在 `same_name`）。

頁面網址預設從 workspace 的 `reference/drawio_session.txt` 讀（workspace 是主 worktree 根目錄的上一層），也可以用 `--url <網址>` 或 `--session-file <檔>` 指定；`--timeout` 設 HTTP 逾時秒數。輸出一行 JSON；結束碼 0 過、1 有問題、2 用法錯。測試在 `test/`，用假 HTTP server，不依賴 drawio 服務。

## png.py — 匯出 PNG 的白底與縮圖

drawio MCP `export_diagram` 匯出的 PNG 是透明底（#138）。`png.py` 只用 Python 標準函式庫自己解碼／編碼 PNG，不需要另外安裝影像套件。從 repo 根目錄跑：

- `python3 script/diagram/png.py info <png>`：寬高、位元深度、色彩型態，以及是否支援。
- `python3 script/diagram/png.py flatten <in.png> <out.png>`：RGBA 合成到白底，輸出 RGB PNG。
- `python3 script/diagram/png.py resize <in.png> <out.png> [--max-width 1600]`：寬度超過上限才等比縮（最近鄰取樣），色彩型態沿用輸入。
- `python3 script/diagram/png.py clear <file>…`：刪掉存在的檔，輸出 `{"ok", "cmd", "removed"}`；刪完還有任何一個存在就 ok false。
- `python3 script/diagram/png.py finish --ref <drawio 檔> [--max-width 1600] <名.raw.png>…`：檔名都要以 `.raw.png` 結尾（否則結束碼 2）；每頁 `<名>.raw.png` → flatten → `<名>.flat.png` → resize → `<名>.png`，全部做完再比對時間（成功的每頁，raw 與產出的 png 修改時間都不准早於 `--ref`）。輸出 `{"ok", "cmd", "pngs", "stale": [{"file", "mtime"}], "errors": [{"file", "error"}], "ref", "ref_mtime"}`；某頁讀不到或壞掉記進 `errors`、其他頁照做。
- `python3 script/diagram/png.py fresh --ref <檔> <file>…`：只比對時間，每個檔的修改時間都不准早於 `--ref`；檔不存在也算 stale（`mtime` 為 null）。輸出 `{"ok", "cmd", "ref", "ref_mtime", "stale"}`。

`diagram-edit` workflow 匯出 PNG 時這樣用（由 #139 的後續項目改過去）：匯出前 `clear` 刪掉每頁舊的 `.raw.png`／`.flat.png`／`.png`，匯出沒寫出新檔時後面就讀不到檔而失敗，不會把舊圖當成這次的結果；匯出後一次 `finish --ref <最後一次 state.py get 寫的 .drawio>` 做完所有頁的白底、縮圖與時間比對；收尾檢查再用 `fresh` 確認回報的 raw 與 png 都不早於最後一次 `state.py get`。

只支援 drawio 實際會輸出的 8-bit RGBA／RGB、非交錯；其他型態回結束碼 2。輸出一行 JSON；結束碼 0 過、1 有問題（讀不到、不是 PNG、內容壞掉）、2 用法錯；`clear` 沒刪乾淨、`finish`／`fresh` 有 stale 或 errors、`--ref` 讀不到都算有問題（結束碼 1）。測試在 `test/`（`python3 -m unittest discover -s script/diagram/test`）。

## lint.py

[lint.py](lint.py) 一次跑完圖的機械檢查（#138），給 `diagram-edit` workflow 的「lint 歸零」用。壓線與溢字直接沿用 `check_overlap.py`、`check_overflow.py`，格子分類沿用 `extract_pages.py`，不另寫一份。

跑法（在 repo 根目錄）：

```sh
python3 script/diagram/lint.py <file.drawio> [--base <old.drawio>] [--rules a,b]
```

| 規則 | 檢查 |
|---|---|
| `overlap` | 壓線：線穿過不相干的方塊 |
| `overflow` | 溢字：文字超出方塊、橢圓或菱形；字寬估算，全形字 = fontSize，半形字 = 0.6 × fontSize |
| `dangling` | 懸空：流程頁的步驟與判斷沒有進線或出線、終點沒有進線、跨頁出入口少了該有的線 |
| `decision` | 判斷：菱形出線不是兩條，或兩條沒有分別標「是」「否」 |
| `endcolor` | 終點顏色：橢圓底色不是終點色；寫結束碼 0 卻不是綠、寫非 0 卻是綠；紅終點寫了「請」「手動」「重跑」就該用橙 |
| `term` | 名詞：用了名詞表 `_Avoid_` 的說法、本頁名詞表的名詞不在名詞表、同一名詞各頁寫法或定義不一致。名詞表讀根目錄 `GLOSSARY.md`，沒有就讀 `CONTEXT.md`，都沒有就跳過並在 `skipped` 標出 |
| `legend` | 圖例：每頁要有圖例（id 規則見 `STYLE.md` 3.1）、頁上的底色要在圖例裡、圖例的底色要是 `STYLE.md` 定義過的 |
| `page-id` | 頁 id：`<diagram id>` 不准重複或缺；給 `--base` 時，舊檔每頁的 id 在新檔都要還在（改頁名、換頁序不算） |

流程頁 = 頁上有非圖例的菱形或終點、出入口橢圓；`dangling` 只查流程頁。只讀檔，不連 drawio 服務；壓縮與未壓縮的 `<diagram>` 都讀。

輸出一行 JSON：`{"ok", "file", "base", "rules", "skipped", "count", "violations": [{"page", "cell", "rule", "msg"}]}`，`page` 是 `<diagram id>`。結束碼 0 沒有違規、1 有違規、2 用法錯。測試：`python3 -m unittest discover -s script/diagram/test`。
