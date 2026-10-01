# script/doc — 文件工具

## 對外文件的改動標示（`mark_changes.py`）

對外文件（審閱頁 `doc/contract/0N_*.md` 與根目錄 `README.md`）每改一輪，就產一份標示版讓人只看差異：新增用綠底 `<mark>`，刪除（被取代或拿掉的舊文字）用紅底 `<mark>`。標示版放在送審資料夾 `doc/review/<鍵>/`，只給審閱用，所以可以用 GitHub 會濾掉的 `<mark>` 內嵌樣式；定案後送審資料夾不再保留那一頁，只留正式檔。整套審閱流程（討論分支、定案才 merge、送審給哪兩個檔）見[審閱頁說明](../../doc/contract/README.md)「版本怎麼迭代」，這裡只講工具。內部文件（本檔、`AGENTS.md`、各目錄的 README、ADR 規則等）改完不產標示版、不送審。

### 一輪的流程

1. **改之前先備份**。改動一律走 doc-edit workflow，由 workflow 在第一次修改前自動備份，不手動建 `*.pre_rNN.md`：手動建的檔會被當成已用掉的 round，也可能蓋掉 workflow 保證為「修改前原檔」的那份備份。`_backup/` 已移出 git（#128），只留在本機、已 gitignore。workflow 中途失敗就換下一個 round 重跑，不手動補備份。每輪一個 round，寫成 `rNN`：取本機 `doc/decisions/_backup/` 裡最大的 `pre_rNN` 與 git log 裡 `Doc-Edit: rNN` footer 兩者的最大編號再加一，不能重用；doc-edit workflow 開跑時會檢查 round 的格式是不是 `rNN`、編號是不是這個最大值加一，重用或跳號就直接停。這一輪的基準後綴（也就是備份尾碼）是 `pre_<round>`，例如 round `r65` 的基準後綴是 `pre_r65`。

   備份檔名是 `<鍵>.pre_<round>.md`，鍵是**把路徑攤平**（去掉 `.md`、`/` 換成 `_`、去掉開頭的點）。所有檔都用這套命名，不限審閱頁。審閱頁 `doc/contract/01_purpose.md` 的備份是 `doc_contract_01_purpose.pre_<round>.md`；`docs/` 併進 `doc/` 之前的備份是舊鍵 `docs_contract_…`（歷史），`mark_changes.py` 兩種都認。

2. **改**：由 [doc-edit workflow](../../.claude/workflows/doc-edit.js) 的改寫階段派子代理修改（各 workflow 的說明見 [workflow 說明](../../.claude/workflows/README.md)）；本工具不改內容，只在修改完成後產生標示版。

3. **產標示版與正文副本**：

   ```sh
   python3 script/doc/mark_changes.py 01_purpose 02_invariants
   ```

   要在 repo 根目錄執行。審閱頁傳頁名（不含 `.md`）；根目錄 README 傳相對 repo 根目錄的路徑 `README.md`：

   ```sh
   python3 script/doc/mark_changes.py README.md
   ```

   不帶後綴時，基準是這個鍵在 `doc/review/versions.json` 最後一筆 `replied: true` 的紀錄，也就是維護者最後回覆過的那一版（用 `git show` 從紀錄的 commit 取檔）；沒有這樣的紀錄就整份標新增，`versions.json` 還不存在時也一樣，而且不會建立這個檔。鍵已標成定案而且正式檔仍與定案 commit 相同時，不產生送審檔；若送審資料夾還存在就刪掉並印出。正式檔在定案後又有改動時，改用定案版為基準重新產生，並印出「定案後又有改動，回到待審」。要拿本機的改前快照當基準，在頁名前加後綴，例如 `python3 script/doc/mark_changes.py pre_r65 01_purpose`，讀本機 `doc/decisions/_backup/` 裡照步驟 1 命名的備份（例如 `doc_contract_01_purpose.pre_r65.md`）；本機沒有 `_backup/`（換電腦、新 clone）就報錯。新建的頁沒有舊版，後綴寫 `new`，整份標新增。

   輸出到送審資料夾 `doc/review/<鍵>/`，檔名固定、不帶版本號，每次產生就覆蓋：

   - 標示版 `<鍵>.marked.md`。
   - 正文副本 `<鍵>.md`，內容跟正式檔一樣，只差相對連結。

   版本號不在 repo 的檔名裡、也不寫進檔內，只出現在送審 zip 裡的檔名（`<鍵>.v<N>.…`）。`doc/review/versions.json` 記每次送審的版號與 commit，進 git，所以換電腦或新 clone 之後版號不會從 v1 重來。每筆紀錄有 `v`、`commit`、`replied`（維護者回覆過沒有），選填 `path`／`csv_path`：有這欄時基準改從 `git show <commit>:<path>` 取，用於舊的 `_marked/` 副本，從副本取時相對連結會先改寫回正式檔位置再比對；副本的連結沒改寫過（照正式檔位置寫）時帶 `raw_links: true`。沒寫 `replied` 的紀錄當成還沒回覆。正式檔改過名時（`mark_changes.py` 的 `RENAMED`：`03_messages` 改名為 `03_output`，#137），鍵跟著改名，舊紀錄不補 `path`：沒寫 `path`／`csv_path` 而紀錄的 commit 裡還沒有新路徑時，基準改取改名前的路徑；所有基準（含其他頁、本機備份）裡連到改名前路徑的連結也先換成新路徑再比對，只因改名而不同的行不標成改動。`versions.json` 頂層另有 `finalized` 物件，`finalized.<鍵>` 是 `{"v": N, "commit": "<sha>"}`，那一版的送審紀錄有 `path`、`csv_path`、`raw_links` 時一併照抄；沒有任何鍵定案時沒有這個欄位。`mark_changes.py` 只讀 `versions.json`、不寫、不取號，也不改正式檔。

   標示版裡的相對連結會改寫成從送審資料夾出發（正文副本也一樣）：以原檔所在目錄解析成 repo 內的實際路徑，再換成從 `doc/review/<鍵>/` 出發的相對路徑，錨點照留；指到其他審閱頁的連結指正式檔 `doc/contract/<頁>.md`，不指副本。外部網址、純錨點、行內程式碼與程式碼區塊裡的字樣不改，正式檔也不動。

   正式檔名不帶版本號、不改名，其他文件的連結才不會斷。鍵對審閱頁是頁名（例如 `04_interface`），對其他檔是攤平後的路徑（`/` 換成 `_`、去掉 `.md` 與開頭的點，所以 `README.md` 的鍵是 `README`）。鍵 `README` 一律對到根目錄的 `README.md`；`doc/contract/README.md` 要傳路徑，鍵是 `doc_contract_README`。

   基準選擇、輸出檔名與連結改寫這些行為由 [mark_changes 測試](test/test_mark_changes.py) 涵蓋，在 repo 根目錄跑 `python3 -m unittest discover -s script/doc/test`。

4. **基準是維護者最後回覆過的那一版；定案後又有改動時是定案版**，不是最舊的那一版，也不是最後送出、還沒回覆的那一版。不帶後綴時自動選擇；要指定別的送審版本，用 `--base-version` 指定版號（不看 `replied`）：

   ```sh
   python3 script/doc/mark_changes.py --base-version 03_output=13 04_interface=18 GLOSSARY=6
   ```

   基準是 `versions.json` 裡這個鍵版本 `<N>` 記的 commit，用 `git show` 取當時的正式檔，有附屬 CSV 時也一起取；那個 commit 裡沒有那份 CSV 時視為新建、整份標新增。左邊寫頁名、路徑或鍵都行（`GLOSSARY`、`README` 對到根目錄的檔；`doc/contract/README.md` 要寫路徑）。任何一個指定版號在 `versions.json` 裡找不到就停下報錯，整批都不產。已經討論完的段落不該再標成新改動，紅綠色只留給他還沒看過的。

5. **草稿 commit 在討論分支，定案才 merge 進 `main`**。定案版就是正式檔，之後隨 PR merge 進 `main`。下一輪從 `main` 開新的討論分支，再跑 doc-edit workflow，由它自動備份當時的正式檔，不手動從 `main` 取檔建備份。

### 標示規則

- 表格列在儲存格內標記，不把整列包起來。整列包住會讓那一列不再是合法的表格列，GitHub 與 VS Code 都會把表格切斷。
- 標題行（`#` 開頭）保持原樣、不加任何標籤：檢視器用標題文字產生錨點，標籤混進去錨點就變了，目錄連結跳不過去。新增的標題在下一行註記綠底「（本節新增）」；改過的標題在下一行標紅底「舊標題：<舊文字>」，再接一行綠底「（標題已修改）」；刪掉的標題去掉 `#`，以紅底呈現在普通文字行，不產生錨點。
- 清單、引言的行首記號留在標籤外，否則會變成普通文字。
- 粗體留給結構標籤、名詞第一次出現於正文時連到 `GLOSSARY.md` 的所屬分群、綠底與紅底的 `<mark>` 留給改動，三者互不衝突。

### 審閱頁旁的 CSV（`03_output`）

審閱頁旁邊有同名的 CSV（`doc/contract/03_output.csv`）時，傳頁名 `03_output`（或路徑 `doc/contract/03_output.csv`，效果相同）會一起處理 `.md` 與 `.csv`，兩個檔共用 `versions.json` 裡同一個鍵 `03_output`，送審時一次只加一號。在 `doc/review/03_output/` 輸出三個檔：

- `03_output.md`：03 頁的正文副本（03 頁這一輪沒改也照樣輸出）。
- `03_output.csv`：CSV 的副本，逐位元組照抄（BOM、LF 都保留）。
- `03_output.marked.md`：合併的標示版。前半是 03 頁的逐行差異，規則同上；後半是「03_output.csv 的逐碼差異」。

CSV 的逐碼差異：新舊兩版依 `code` 對齊、逐欄比較，每個有改動的代碼寫成一段 `#### VKnnnn`，依新表頭的欄位順序列出這個代碼的各欄。改過的欄寫成紅底舊值 → 綠底新值，沒改的欄照原樣列出、不加標記。新增的代碼在標題下一行註記綠底「（本碼新增）」、各欄標綠；改成 `retired` 的註記紅底「（本碼停用）」；從 CSV 拿掉的列註記紅底「（本列刪除）」、各欄標紅。表頭改了（例如刪掉欄）時，逐碼差異開頭先標出新舊表頭，並逐欄註記紅底「（本欄刪除）」或綠底「（本欄新增）」；新增的欄照新表頭的位置列出，各碼標綠新值並註記綠底「（本欄新增）」，新值是空的不算改動；刪掉的欄排在新表頭各欄之後，列出舊值並標紅，所以只刪欄的代碼也算有改動。沒改動的代碼不成段，最後用一行列出有幾個、是哪些。欄位值裡的 `<`、`>` 會跳脫，占位符照原樣看得到；格內換行改成 `<br>`。

不帶後綴或用 `--base-version` 時，CSV 的基準跟 `.md` 一樣從送審紀錄的 commit 取（紀錄有 `csv_path` 就取那個路徑）。帶後綴時，CSV 的基準版是本機 `doc/decisions/_backup/doc_contract_03_output.<後綴>.csv`，攤平規則跟 `.md` 相同，只差副檔名；以下是後綴模式的規則。兩個檔只有一個有基準版時，另一個視為這一輪沒改；CSV 沒有基準版、也不在 git 的 `HEAD` 裡時，視為新建、整份標新增。這兩種情況都會印在輸出，也寫在標示版開頭。兩個都沒有基準版就停下。基準後綴寫 `new` 時，兩個檔都整份標新增。

## 名詞表自檢（`check_context.py`）

根 `CONTEXT.md` 每改一次就跑，不要目視：

```sh
python3 script/doc/check_context.py
```

查四件事，全過印 `OK` 回 0，任一不過逐條印出回 1：

- `## 目錄` 的分群與 `## Language` 下的 `###` 分群一字不差、順序一致。
- 每個目錄條目的 `#term-xxx` 對得上一個 `<a id="term-xxx"></a>`，兩邊數量、分群歸屬與順序都一致，錨點不重複。
- 每個錨點的下一行是 `**名詞**（english）：` 格式，且目錄寫的名詞與正文一致。
- 所有 `_Avoid_` 列出的詞都沒出現在正文（`_Avoid_:` 那行本身除外）——改名沒改乾淨會在這裡被擋下。

## 舊名殘留自檢（`check_terms.py`）

`check_context.py` 只管 `CONTEXT.md` 自己；改名改到一半、舊詞留在某一頁，要靠這支抓：

```sh
python3 script/doc/check_terms.py
```

每筆殘留印 `<檔>:<行號>  <詞>  <該行內容>`，全乾淨印 `OK` 加統計（掃了幾個檔、幾個 `_Avoid_` 詞）。有殘留回 1，乾淨回 0。

- **詞從哪裡來**：每次跑都從根 `CONTEXT.md` 的 `_Avoid_:` 行現抽，不寫死清單。名詞表會長大，寫死的清單幾次改名之後就跟名詞表脫鉤，而且是靜默的。
- **掃哪些檔**：`git ls-files -co --exclude-standard` 取得的現行 `.md` 檔。`doc/decisions/_backup/`、`doc/decisions/review_log/`、`doc/research/` 已移出 git 並 gitignore，本來就不在清單裡。排除 `doc/decisions/research/`（研究素材）、`doc/decisions/review/_marked/`（本地產物）、`.claude/skills/`（vendored 的第三方 skill）、`script/diagram/` 與 `discussion.drawio`（架構圖已凍結，裡面的舊詞是歷史），以及 index 裡還留著但已刪除的檔。
- **不算殘留的行**：`_Avoid_:` 行本身；以及帶「舊名」「已廢止」「已移除」「之名作廢」「舊審閱頁」「改名」這類引述標記的行——講改名史本來就得同時寫出新舊兩個詞。標記清單是 `check_terms.py` 頂端的 `QUOTE_MARKERS` 常數，要放行新的講法就加在那裡。
- **逐行白名單**：已定案要保留舊詞的**個別一行**登記在 `check_terms.py` 頂端的 `WHITELIST`，每筆是 `(檔案路徑, 該行必須包含的字串, 理由)`。三個欄位都要對上才放行，而且只放行「那段字串裡面」的舊詞：把字串從該行挖掉之後還搜得到舊詞，照樣算殘留。所以同一個檔的其他行、同一行的其他位置、別的檔抄同一段字，全都還是會被抓到。只比對詞會讓那個詞全域失效、只比對檔案會讓整個檔失效，白名單就變成漏洞——這是刻意不做的兩種寫法。白名單筆數印在 `OK`／`FAIL` 那行，悄悄長大會看得見。
- **目前的兩筆**：`doc/decisions/review/01_purpose.md` 的 `# 01 專案目的與承諾` 與 `doc/decisions/README.md` 裡引用這個標題的那一列。使用者定案：標題保留這個舊名，因為那裡指的是 VK 這個專案本身，不是名詞表裡指使用者 repo 的那個詞；`README.md` 那一列是在引用頁標題，同一個道理。（這一行自己帶「舊名」標記，靠上面的引述規則過關，不再多開一筆白名單。）
- **「數位簽章」例外**：「簽章」是名詞「印記」的舊名，但「數位簽章」是密碼學的標準術語（digital signature），跟印記無關——講 registry 或 image 的簽章時本來就該這樣寫。所以用負向前瞻 `(?<!數位)簽章` 只抓單獨的「簽章」，否則這支腳本會逼著大家把正確的詞改掉。

## 中英排版自檢（`check_typography.py`）

改了 `README.md`、`doc/contract/*.md`、`doc/contract/*.csv` 或 `GLOSSARY.md` 就跑，CI 的 docs-lint job 也跑這支：

```sh
python3 script/doc/check_typography.py
python3 script/doc/check_typography.py --fix
```

在 repo 根目錄執行。全過印 `OK` 回 0；有違規逐條印 `<檔>:<行>: <問題與建議寫法>` 回 1。加 `--fix` 直接改檔，只動下面三條規則涉及的空白與括號，其他字元不動。規則是維護者定案的：

- 括號裡全是 ASCII（英文、數字、符號）時用半形括號，半形括號與中文之間空一格：「檢查（test）」寫成「檢查 (test)」。括號裡有中文就維持全形「（…）」。
- 中文與英文字母或阿拉伯數字相鄰時中間空一格：「VK的recipe」寫成「VK 的 recipe」、「第12條」寫成「第 12 條」。全形標點（，。、：；「」（）等）與英數之間不加空白。
- 行內程式碼（反引號包住的）與前後的中文相鄰時也空一格：「`0`結束」寫成「`0` 結束」、「印`VK0024`」寫成「印 `VK0024`」。與全形標點相鄰不加空白；隔著連結的 `[` 或 `](…)` 時照上一條，連結記號不算字元。

不查行內程式碼的內容、程式碼區塊、URL、Markdown 連結目標（括號裡的路徑與錨點）與 HTML 標籤。CSV 只查文字欄（`situation`、`message`、`description`、`next_step`），`code`、`status`、`level`、`exit_code`、`disposition` 是固定值域，不查；英文的 `message` 與 `next_step` 仍會掃描，但不會因英文排版本身誤報。`--fix` 改到 CSV 時，若 `next_step` 不再逐字出現在 `message` 裡，這支照樣報錯，要手動把兩欄對齊；改到標題時 GitHub 產生的錨點跟著變，連到舊錨點的連結不會自動改，要另外改。

各條規則的正反例與排除範圍在 [check_typography 測試](test/test_check_typography.py)。

## 訊息表自檢（`check_messages.py`）

`doc/contract/03_output.csv` 是每個原因代碼的唯一出處（#122）。改了 CSV，或其他頁引用代碼的地方就跑：

```sh
python3 script/doc/check_messages.py
```

在 repo 根目錄執行。全過印 `OK` 回 0，任一不過逐條印出回 1。CSV 還不存在時印 `OK` 並跳過。CSV 與 03 頁的路徑只寫在 `check_messages.py` 頂端的 `CSV_PATH`、`MD_PATH` 兩個常數，之後改名 `reason_codes.csv`（#137）只改那兩行。錯誤位置報 `<檔>:<代碼>:<欄名>`，例如 `doc/contract/03_output.csv:VK0003:next_step`，不報實體行號。查這幾件事：

- 格式：UTF-8 開頭恰好一個 BOM、只准 LF、檔尾恰好一個換行；表頭逐字等於 `code,status,level,exit_code,disposition,situation,message,description,next_step`；用 `csv` 模組以 strict 照 RFC 4180 解析，每列欄數相同。格內換行（雙引號包住的 LF）解析得過。欄位頭尾不准空白，不准以 `=`、`+`、`-`、`@`、Tab、CR 開頭（Excel 會當成公式）。
- 代碼：`VK` 加四位數字，從 `VK0001` 起逐列加一，所以唯一、遞增、不缺列；停用的代碼留列。
- `status` 只准 `active`、`retired`。`retired` 列只留 `code`、`status`、`situation`，其餘欄要空白。
- `active` 列：`level` 只准 `warn`、`error`、`fatal`；`exit_code` 必須依序對應 `1`、`2`、`3`；`situation`、`message`、`description` 必填。
- `disposition` 只准「待處理」「失敗」或空白；`warn` 一律空白，只有 `warn` 與 `situation` 以「用法錯誤：」開頭的列可留空，其他 `error`、`fatal` 的 `active` 列必填；「待處理」必有 `next_step`；「失敗」的 `next_step` 必須空白。
- `message` 不准含中文字元（中文說明放 `description`）。
- `next_step` 有值時，必須逐字出現在 `message` 裡。
- 欄位不准 HTML（有屬性的標籤、結束標籤、`<ins>`、`<br>` 這類常見標籤名、`<!--`）與 Markdown（反引號、粗體、刪除線、連結、行首的標題、清單或引言記號）；不帶屬性的 `<…>`（例如 `<repo>`、`<P>`）算占位符。`<`、`>` 要成對、不巢狀。
- 引用：`README.md`、`doc/contract/*.md`、`GLOSSARY.md` 裡出現的每個 `VKnnnn` 都要在 CSV 裡、而且是 `active`；`doc/adr/*.md` 只要求在 CSV 裡，可以是 `retired`。連到 `03_output.csv` 不准帶 `#`；連結文字是代碼時不准連 `03_output.md`（03 頁不放逐碼內容），一律連 CSV。01、02 不准連 CSV。
- 診斷範例：`README.md`、`doc/contract/*.md`、`GLOSSARY.md` 裡的 `vendor_kit: <level>[VKnnnn]: <本文>`，level 要等於 CSV，本文要符合 message 第一行，`<…>` 占位符可以對應任意文字。
- `active` 列的 `message` 句首要大寫，或以占位符、小寫指令名 `just` 開頭；結尾要是句點，或以 `next_step`、`just vendor_kit` 指令結尾。

欄位約定：`message` 是印出的英文本文，不含 `vendor_kit: <level>[VKnnnn]: ` 前綴、不准含中文（規則 4）；`description` 是給人讀的中文說明。

CSV 的 `situation`、`message`、`next_step` 裡的指令寫法（`just vendor_kit …`）不在這支的範圍，目前沒有工具檢查。

各條規則的正反例在 [check_messages 測試](test/test_check_messages.py)。

## 對外頁寫法自檢（`check_review_pages.py`）

改了根目錄 `README.md`、`doc/contract/0N_*.md` 或 03 的 CSV 就跑，CI 的 docs-lint job 也跑這支：

```sh
python3 script/doc/check_review_pages.py
```

在 repo 根目錄執行。全過印 `OK: 掃 N 個對外文件` 回 0；有違規逐條印 `<檔>:<行>: <問題>` 回 1，CSV 的位置報 `<檔>:<代碼>:<欄名>`。掃描範圍是根目錄 `README.md` 與 `doc/contract/0N_*.md`，另掃 `doc/contract/03_*.csv` 的指令欄。檔案還不存在就少掃那些，不算錯誤。查這幾件事：

- 每頁有 `## 目錄`；不寫「出處：」行，也不寫 `> 版本 vN`。
- 不准任何 HTML 標籤，`<ins>`、`<a id>`、`<br>` 也不行；行內程式碼裡的、反斜線跳脫的 `\<repo\>` 不算。
- 相對連結的檔案與錨點都要存在，錨點照 GitHub 的標題轉換規則算；不准以 `/` 開頭。
- 引用別頁條目寫「依 [頁名第 N 條](連結#錨點)」，不寫舊寫法「[名字](連結) 第 N 條」。
- 連結文字不得含反引號：碼放在連結外，例如「[結束碼](03_output.md#結束碼) `2`」。連結文字裡的 `<…>` 要跳脫成 `\<…\>`。
- **L1**：01、02 不准原因代碼 `VKnnnn`，行內程式碼照掃，程式碼區塊不掃。
- **L2**：01、02 的「結束碼」前後 10 字內不准反引號包住的單位數字，也不准 `exit code <數字>`。
- **L3**：內容只能往前依賴，導覽可以往後指。審閱頁 N 以「依」或「依照」連到後面的頁就擋；README 是入口不是第 0 頁，以「依」連到審閱頁也擋。只是導覽就寫「詳見」。
- **L4**：README 與 03 的行內程式碼、03 CSV 的 `situation`、`message`、`next_step` 欄，以 VK recipe 名或 `just vendor_kit <recipe>` 開頭的片段，用到的選項 token（含單獨的 `--` 與 `@<tag>`）都要先在 `GLOSSARY.md`、01、02 的行內程式碼出現過，逐 token 完整比對。還沒有 `GLOSSARY.md` 時整條跳過。

頂端的 `TEMP_ALLOWLIST` 放暫時豁免的個別錯誤（整行原文完全相同才放行），目前是空的；輸出第一行會印筆數與命中數，悄悄長大看得見。

各條規則的正反例在 [check_review_pages 測試](test/test_check_review_pages.py)。
