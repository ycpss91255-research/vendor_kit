# script/doc — 文件工具

## 審閱頁的改動標示（`mark_changes.py`）

審閱頁（`doc/decisions/review/0N_*.md`）每改一輪，就產一份標示版讓人只看差異：新文字用 `<mark>` 螢光、被取代的舊文字用 `<del>` 刪除線。標示版只在本地 review 用、不進 git（`_marked/` 在 `.gitignore` 裡），所以可以用 GitHub 會濾掉的 `<mark>`；review 完只留最終版。

### 一輪的流程

1. **改之前先備份**。每輪一個後綴，依序遞增：

   ```sh
   cp doc/decisions/review/02_invariants.md \
      doc/decisions/_backup/doc_decisions_review_02_invariants.pre_r65.md
   ```

   備份檔名是**把路徑攤平**（`/` 換成 `_`）加上 `.pre_<後綴>`。同一套命名用在所有檔，不只審閱頁，`doc-apply` workflow 的護欄也是這個規則。

   `doc/decisions/_backup/` 已移出 git，只留在本機、已 gitignore；舊內容在 git 歷史與 tag `archive/pr-59`。

2. **改**（派子代理做，主對話只協調）。

3. **產標示版**：

   ```sh
   python3 script/doc/mark_changes.py pre_r65 01_purpose 02_invariants
   ```

   輸出到 `doc/decisions/review/_marked/<頁名>.v<N>.marked.md`，`<N>` 每跑一次加一（版本號記在 `_marked/.<頁名>.rev`），舊的那份會被刪掉，所以交出去的永遠是最新版、而且看檔名就分得出新舊。後綴就是步驟 1 用的那個，決定「跟哪一版比」。

4. **基準永遠是審閱者上次看過的那一版**，不是最舊的那一版。他看過並回饋之後，下一輪的後綴就換成他讀的那一版 —— 已經討論完的段落不該再標成新改動，紅綠色只留給他還沒看過的。

5. **只把標示版交給審閱者**。定案之後才給完整檔。

6. **定案就 commit**。commit 之後下一輪的比較基準改成 git：

   ```sh
   git show HEAD:doc/decisions/review/02_invariants.md \
     > doc/decisions/_backup/doc_decisions_review_02_invariants.pre_r66.md
   ```

### 標示規則

- 表格列在儲存格內標記，不把整列包起來。整列包住會讓那一列不再是合法的表格列，GitHub 與 VS Code 都會把表格切斷。
- 標題、清單、引言的行首記號留在標籤外（`## <ins>目錄</ins>`），否則標題會變成普通文字。
- 粗體留給結構標籤、底線留給名詞標記、螢光與刪除線留給改動，三者互不衝突。

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
