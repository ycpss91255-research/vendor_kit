# 三階段 draw.io 審查工具鏈（review v2）

目的：把「機械可查」的東西先用腳本跑掉（抽取、lint、縮圖），代理只做需要判斷的部分
（內容與連接、排版、一格一事），最後每條逐一驗證。輸入只讀，不寫回 `.drawio`／PNG。

檔案（都在 `script/diagram/`）：

| 檔 | 作用 |
|---|---|
| `extract_pages.py <drawio> <outdir> [page_id …]` | 每頁 → `<outdir>/<id>.json` + `<id>.md`；另寫 `pages.json`（頁序＋頁名） |
| `lint_pages.py <outdir>` | 讀上面的 JSON → `<outdir>/lint.md`（依頁分組）+ `lint.json` |
| `shrink_png.py <pngdir> <outdir> [scale] [page_id …]` | PIL 縮圖（預設 50%，白底）→ `<outdir>/*.png` + `pngs.json` |
| `<repo>/../reference/_legacy/workflows/diagram-review-v2.js`（repo 外，只在維護者本機） | 已停用的 workflow（只吃上面三個的產物）。圖面審查要重啟時以它為範本，改寫成命名 workflow 放 `.claude/workflows/` |

## 主對話要先跑的三個指令

```sh
cd <repo>/script/diagram   # 輸出目錄（review_v2_out、review_v2_png、png_v2）請放 scratchpad 或 repo 外
python3 extract_pages.py ../../discussion.drawio review_v2_out          # 1. 抽取（47 頁 → review_v2_out/<id>.json|md, pages.json）
python3 lint_pages.py    review_v2_out                          # 2. lint（→ review_v2_out/lint.md, lint.json）
python3 shrink_png.py    png_v2 review_v2_png                   # 3. 縮圖（→ review_v2_png/*.png, pngs.json）
```

只審部分頁：三個指令都可在最後加頁 id（`extract_pages.py v2_only.drawio out v1p5c v1p5cc`）；
lint 的跨頁名詞比對只會比有抽出的頁。

## workflow args 範例

```json
{
  "extracted": "<scratchpad>/review_v2_out",
  "lint":      "<scratchpad>/review_v2_out/lint.md",
  "pngs":      [ {"page": "v1p5c", "path": ".../review_v2_png/v1p5c.png"}, ... ],
  "notes":     "<scratchpad>/decisions/_legacy/proposal_v2.md",
  "changes":   "第十一輪：…",
  "focus":     "E(c) 兩頁的續跑入口",
  "pages":     ["v1p7bcc", "v1p7bccc"],
  "lint_items": [ ...lint.json 的內容（可選）... ]
}
```

- `pngs`：直接貼 `review_v2_png/pngs.json` 的內容（`page` = 頁 id，與 `<id>.md` 同名）。
- `pages`：可選白名單（頁 id）；不給就審 `pngs` 裡所有頁。
- `lint_items`：可選，貼 `lint.json` 內容；有給，結果的 `lint_mechanical` 直接列 warn 級條目（不經代理）；沒給就只留 lint.md 路徑。

流程：
1. 抽取（無 shell）：分組。內容與連接 = 4 組；排版 = 每 10 頁一個代理（47 頁 → 5 個）；一格一事 = 1 個代理。
2. 三種找問題的代理平行，各自找到的 findings **立刻**進驗證（pipeline，無 barrier）；驗證代理 effort low，對照 `<id>.md`／縮圖。
3. 回傳 `{ verdicts, confirmed(byPage), must_fix_count, rejected, lint_mechanical }`。findings 的 `page` 一律是頁 id。

## extract_pages.py 的判定規則（摸索結果）

- 一頁 = `<diagram id=… name=…>`；cell 用 regex 掃 `<mxCell id=… >`，未壓縮 XML。
- 文字：XML 解跳脫一次 → HTML；`<br>`／`<div>`→`⏎`；去標籤；再解一次實體（所以 `&amp;lt;repo&amp;gt;` 會變回 `<repo>`，
  不像 `pagetext.py` 那樣把 `<repo>` 當標籤吃掉）。
- `kind`（依 disc_v1_b.py／gen57.py 的樣式常數）：
  - 菱形 → `decision`（D12）
  - 橢圓：`#d5e8d4` → `end_ok`（G12；**綠橢圓同時是起點**，lint 懸空規則只在「無進邊也無出邊」才報）、`#f8cecc` → `end_red`（R12）、
    `#ffe6cc` → `end_orange`（O12）、白底 `dashed=1` → `entry`（ENTRY）
  - 長方形：`#dae8fc`/`#6c8ebf` → `step`（SUB 藍）、白底 `light-dark(…)` 邊 → `step`（W12）；同邊但 `dashed=1` → `file`（F12；粗體 = FGRP 檔案容器）；
    `#666666` 邊 → `file`（PRE 逐字框）；`#ffe6cc`/`#d79b00` → `rule`（RULE）；白底 `#b85450` 粗邊 → `rule`（INV）；
    `#e6e6e6` → `header`（HDR）；`#e1d5e7` → `other`/IMG（紫 image）
  - `shape=note` → `note`（`#fff2cc` = PEND 黃便條）
  - id 形如 `<prefix>_tk<i>`／`_tv<i>` → `term`（名詞／說明；`_th` = 「本頁名詞」表頭）
  - id 含 `_lg<n>`／`_lgt`／`_lgx_` → 圖例（`legend=true`，`cls=LEGEND`）；swimlane → BAND；`text` → TEXT／TITLE；其餘白底 `#999999` 邊 → CELL（表格格）
  - `#00b050` 小綠標「v2」不列入 nodes，改記在本體 `v2=true`
- `terms`：`_tk<i>` 與 `_tv<i>` 依 prefix＋序號配對（47 頁全部都是這個形式，表頭 `_th`）。
- `xrefs`：regex `(來自|續|見|回|→)?「X」頁`，node 文字與線標籤都掃。
- `edges[].fontSize`：style 的 fontSize 字串（沒有 = null）；lint `edge-font` 用。
- `fills`／`legend_fills`：非圖例格 vs 圖例格的 fillColor 集合（lint 的 color 規則用）。

## lint_pages.py 規則與可調參數

檔頭 docstring 列了全部規則的代號（v1 的 9 條＋v2 的 12 條；v1 原檔備份在 `lint_pages.py.v1`）；可調參數在檔案頂端：`FLOW_PAGE_RE`（哪些頁算流程頁，懸空規則只查這些）、
`KEYWORDS`（名詞覆蓋的關鍵字 regex）、`BASE_ALLOW`（不算 base 實例的片語）、`COLOR_WHITELIST`、`ONETHING_TOKENS`／`ONETHING_MIN`、`NEEDS_HUMAN`。
v2 規則每條可在 `ENABLED` 字典關閉，門檻／關鍵字都是頂端常數。

### v2 新增規則（全部 warn；目標 = 把反覆發生的圖面問題機械化擋掉）

| 規則 | 條件 | 訊息／備註 | 可調常數 |
|---|---|---|---|
| `event-name` | node／edge 文字出現 `launcher_started|launcher_completed|launcher_failed|engine_started|engine_completed|engine_failed|_started\b|_completed\b` | 事件名須用 spec 註冊表：launcher_start/exit、engine_start/exit | `EVENT_NAME_RE` |
| `resolve-3way` | 流程頁上文字「docker run … resolve」（中間無括號；排除 apply 格的「（含 vk-resolve）」）的 step，沿出邊走 ≤ 3 步須同時有 (A) decision 含「回 0／結束碼 0／非 0」與 (B) **另一個** decision／step 含「6-30」或「文法」。步數只算啟動器白 step（藍 SUB、菱形、file、note 不計）；走到「續「X」頁」出口會接到 X 頁的「來自」入口續走（跨頁） | resolve 結果須三叉：非 0 原碼傳出／文法不合 6-30／合法；A 與 B 合在同一格（「回 0 且文法合法？」）也報「缺文法格」 | `RESOLVE_3WAY_DEPTH`、`RESOLVE_3WAY_CROSS_PAGE`、`RESOLVE_STEP_RE`、`RESOLVE_EXIT_RE`、`RESOLVE_GRAMMAR_RE` |
| `precheck-recover` | 頁名含 install|add|remove|upgrade|dev|undev|uninstall|升引擎 的第一頁（頁名含「（1）」或不含全形括號；且頁上有起點綠橢圓、沒有「來自「X」頁」入口）須有 decision 文字含「未完成」「既有進度檔」「恢復」；頁名含 sync|update 的第一頁須有節點文字含「6-33」；prune 頁只要有「只列出」 | 缺 → warn（頁級，id `-`） | `PRECHECK_VERB_RE`、`PRECHECK_SYNC_RE`、`PRECHECK_DECISION_RE`、`PRECHECK_FIRST_RE`、`PRECHECK_SKIP_RE`（預設 None） |
| `end-color-text` | end 節點：文字含「→ 0」或以「0：」開頭 → 須 end_ok；含 `6-24|6-31|6-38|6-30|寫不進|拉不到|寫入失敗|失敗（任一步）` → 須 end_red；含 `請|先 |手動|重跑|→ 3|6-4|6-33` 且無紅關鍵字 → 須 end_orange | 「終點文字應為 X 但是 Y」（舊 `endcolor` 保留不動） | `END_OK_RE`、`END_RED_RE`、`END_ORANGE_RE` |
| `xref-forward` | xrefs 指到的頁序號（頁名前綴數字；沒有前綴就用 pages.json 順序）大於本頁序號。「續「X」頁」出口不算；「來自」「見」「回」、裸「X」頁都算；引用命中多頁時取最小序號 | 前引：頁 N 只能引用序號更小的頁 | — |
| `write-line` | 流程頁 step 文字（去掉「是：」「否 →」等分支前綴）以 寫|建|刪|原子替換|append 開頭或含「→ 檔」，頁內有 file 節點，但該 step 沒有出邊指到 file 節點 | 寫入格缺到檔案框的線 | `WRITE_LINE_EXEMPT`（動詞後緊接：印、印出、印記、執行紀錄、launcher_、engine_、sync_fast_path；「寫印記」仍算 = `WRITE_LINE_FORCE`）、`WRITE_LINE_EXEMPT_ANY`（含「到暫存」「暫存副本」= 寫暫存不算）、`WRITE_PAGE_RE` |
| `write-fail-edge` | 同上寫入 step：沒有出邊到 end_red／end_orange、沒有出邊 label 含「失敗」、頁內也沒有 node／edge 文字含「任一步」「失敗匯流」 | 寫入格缺失敗出邊或失敗匯流 | `WRITE_FAIL_PAGE_RE` |
| `term-count` | 名詞表條數 > 8 | 頁級 | `TERM_MAX` |
| `term-dup-page0` | 名詞 name（去結尾括號）已在第 0 頁出現（第 0 頁 = `PAGE0_IDS` 的 terms ＋ 表格每列第一格 `_r<i>c0`） | 「第 0 頁已有，不必重列」 | `PAGE0_IDS`、`PAGE0_CELL_RE` |
| `page-height` | max(y+h) > 2400 | 列最低的格 | `PAGE_MAX_H` |
| `edge-font` | edge style 有 fontSize 且 ≠ 12（extract_pages.py 現在會把 edge 的 `fontSize` 寫進 JSON；舊 JSON 沒有此欄就略過） | — | `EDGE_FONT` |
| `merge-fanout` | step 出邊 ≥ 3 且 targets 全是 end_* | 終點扇出：分支來源不可辨 | `MERGE_FANOUT_MIN` |

已知會報但要人判斷的：`xref-forward` 的「見」前引（bootstrap 頁見 install 頁、add（1）見 add（2）、B 頁見 C 逐檔判斷）——規則刻意嚴格；
`precheck-recover` 對「upgrade ── D. 回退」（git revert 起點、沒有前置檢查）；`end-color-text` 對狀態機頁的綠格「prune 特例…印 6-33 → 繼續」（關鍵字命中但語意是繼續）；
`write-fail-edge` 對 release 頁（v1p15c，CI 寫 .digest／SHA256SUMS／GitHub Release，沒畫失敗邊）。

- 等級：`warn` = 機械上幾乎確定；`info` = 候選／提示（一格一事候選全是 info，交第 3 階段代理）。
- xref：頁名包含引用 → 過；否則拆 token（英數字串／CJK 連續字）全部包含 → `info`「只靠拆字比對到」；
  「install（1）（2）」「E(a)(b)」這種多括號引用會展開成多個各自比對。
- termcov：關鍵字在名詞 name 或說明文出現就算覆蓋；只在說明文出現的彙總成每頁一行 info；都沒有 → warn。
- term-diff：放在 lint.md 最後「跨頁」段（列各版本出現的頁與前三處差異）。
- lint.md 頁序 = 文件內頁序（pages.json）；規則表會列出 v1 9 條＋v2 12 條的 warn／info 數。

## 已知限制

- 懸空規則只看「kind」：白底結果框（例如 prune 頁「列出帶 label 的四類資源」）會被當 step 報「無出邊」；狀態機頁旁邊的說明框也會。這些交代理判定。
- base 規則只排除 `BASE_ALLOW` 的片語；「log.sh 由 base 移植」這類敘述會被列出（是否算實例由代理／使用者決定）。
- 縮圖 50% 後一頁約 1600×2300、0.9 MB；排版代理一次看 10 頁。
