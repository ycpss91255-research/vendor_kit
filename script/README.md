# script — 審閱與圖面工具

## 對外文件的改動標示（`mark_changes.py`）

對外文件（審閱頁 `doc/contract/0N_*.md` 與根目錄 `README.md`）每改一輪，就產一份標示版讓人只看差異：新增用綠底 `<mark>`，刪除（被取代或拿掉的舊文字）用紅底 `<mark>`。標示版只在本機審閱用、不進 git（`doc/decisions/_marked/` 在 `.gitignore` 裡），所以可以用 GitHub 會濾掉的 `<mark>` 內嵌樣式；審完只留最終版。整套審閱流程（討論分支、定案才 merge、送審給哪兩個檔）見[審閱頁說明](../doc/contract/README.md)「版本怎麼迭代」，這裡只講工具。內部文件（本檔、`AGENTS.md`、各目錄的 README、ADR 規則等）改完不產標示版、不送審。

### 一輪的流程

1. **改之前先備份**。改動一律走 doc-edit workflow，由 workflow 在第一次修改前自動備份，不手動建 `*.pre_rNN.md`：手動建的檔會被當成已用掉的 round，也可能蓋掉 workflow 保證為「修改前原檔」的那份備份。workflow 中途失敗就換下一個 round 重跑，不手動補備份。每輪一個 round，寫成 `rNN`：取 `doc/decisions/_backup/` 裡最大的 `pre_rNN` 的編號再加一，不能重用；doc-edit workflow 開跑時會檢查 round 的格式是不是 `rNN`、編號是不是最大編號加一，重用或跳號就直接停。這一輪的基準後綴（也就是備份尾碼）是 `pre_<round>`，例如 round `r65` 的基準後綴是 `pre_r65`。

   備份檔名是 `<鍵>.pre_<round>.md`，鍵是**把路徑攤平**（去掉 `.md`、`/` 換成 `_`、去掉開頭的點）。所有檔都用這套命名，不限審閱頁；`doc-apply` workflow 的護欄也照這個規則。審閱頁 `doc/contract/01_purpose.md` 的備份是 `doc_contract_01_purpose.pre_<round>.md`；`docs/` 併進 `doc/` 之前的備份是舊鍵 `docs_contract_…`（歷史），`mark_changes.py` 兩種都認。

2. **改**：由 [doc-edit workflow](../.claude/workflows/doc-edit.js) 的改寫階段派子代理修改（各 workflow 的說明見 [workflow 說明](../.claude/workflows/README.md)）；本工具不改內容，只在修改完成後產生標示版。

3. **產標示版與帶版本號的副本**：

   ```sh
   python3 script/mark_changes.py pre_r65 01_purpose 02_invariants
   ```

   要在 repo 根目錄執行。審閱頁傳頁名（不含 `.md`）；根目錄 README 傳相對 repo 根目錄的路徑 `README.md`：

   ```sh
   python3 script/mark_changes.py pre_r91 README.md
   ```

   新建的頁沒有舊版，基準後綴寫 `new`，整份標成新增。

   版本號 `<N>` 取 `doc/decisions/review_log/versions.json` 裡這個鍵記的數字加一並寫回，沒有記錄就從 1 起算。`versions.json` 進 git（`_marked/` 不進 git），所以換電腦、新 clone 或清掉 `_marked/` 之後不會從 v1 重來。版本號只在 `_marked/` 的檔名：正式檔與正文副本內都不寫版本號，本工具也不改正式檔。每跑一次做兩件事：

   - 輸出標示版 `doc/decisions/_marked/<鍵>.v<N>.marked.md`。
   - 輸出同一版的正文副本 `doc/decisions/_marked/<鍵>.v<N>.md`，內容跟正式檔一樣，只差相對連結。

   標示版裡的相對連結會改寫成從 `_marked/` 出發（正文副本也一樣）：以原檔所在目錄解析成 repo 內的實際路徑，再換成從 `doc/decisions/_marked/` 出發的相對路徑，錨點照留；指到其他審閱頁的連結指正式檔 `doc/contract/<頁>.md`，不指版本副本。外部網址、純錨點、行內程式碼與程式碼區塊裡的字樣不改，正式檔也不動。

   同一個鍵的舊版標示版與舊版副本會被刪掉，所以交出去的永遠是最新版，而且看檔名就知道是哪一版。正式檔名不帶版本號、不改名，其他文件的連結才不會斷。鍵對審閱頁是頁名（例如 `04_interface`），對其他檔是攤平後的路徑（`/` 換成 `_`、去掉 `.md` 與開頭的點，所以 `README.md` 的鍵是 `README`）。後綴就是步驟 1 用的那個，決定「跟哪一版比」。

   取號、輸出檔名與連結改寫這些行為由 [mark_changes 測試](test/test_mark_changes.py) 涵蓋，在 repo 根目錄跑 `python3 -m unittest discover -s script/test`。

4. **基準永遠是審閱者上次看過的那一版**，不是最舊的那一版。送審的基準是這一頁上一次送審、維護者已回覆的那一版，用 `--base-version` 指定版號：

   ```sh
   python3 script/mark_changes.py --base-version 03_messages=13 04_interface=18 GLOSSARY=6
   ```

   基準讀 `doc/decisions/_marked/<鍵>.v<N>.md`，有附屬 CSV 時也讀 `<鍵>.v<N>.csv`；版本號照舊取 `versions.json` 加一。左邊寫頁名、路徑或鍵都行（`GLOSSARY`、`README` 對到根目錄的檔）。基準副本的連結已改寫成從 `_marked/` 出發，正式檔先用同一套改寫再比，所以內容沒變就是 0 處標記。任何一個指定版號的副本不存在就停下報錯，整批都不產、不取號。基準版的副本保留不刪，維護者回覆之前還能再當基準；其他舊版照舊刪掉。已經討論完的段落不該再標成新改動，紅綠色只留給他還沒看過的。

5. **把兩個帶版本號的檔一起交給審閱者**：`<鍵>.v<N>.md` 與 `<鍵>.v<N>.marked.md`。不交沒帶版本號的正式檔。

6. **草稿 commit 在討論分支，定案才 merge 進 `main`**。定案之後，下一輪從 `main` 開新的討論分支，再跑 doc-edit workflow，由它自動備份當時的正式檔當基準，不手動從 `main` 取檔建備份。

### 標示規則

- 表格列在儲存格內標記，不把整列包起來。整列包住會讓那一列不再是合法的表格列，GitHub 與 VS Code 都會把表格切斷。
- 標題行（`#` 開頭）保持原樣、不加任何標籤：檢視器用標題文字產生錨點，標籤混進去錨點就變了，目錄連結跳不過去。新增的標題在下一行註記綠底「（本節新增）」；改過的標題在下一行標紅底「舊標題：<舊文字>」，再接一行綠底「（標題已修改）」；刪掉的標題去掉 `#`，以紅底呈現在普通文字行，不產生錨點。
- 清單、引言的行首記號留在標籤外，否則會變成普通文字。
- 粗體留給結構標籤、名詞第一次出現於正文時連到 `GLOSSARY.md` 的所屬分群、綠底與紅底的 `<mark>` 留給改動，三者互不衝突。

### 審閱頁旁的 CSV（`03_messages`）

審閱頁旁邊有同名的 CSV（`doc/contract/03_messages.csv`）時，傳頁名 `03_messages`（或路徑 `doc/contract/03_messages.csv`，效果相同）會一起處理 `.md` 與 `.csv`，兩個檔共用 `versions.json` 裡同一個鍵 `03_messages`，一次只加一號。輸出三個檔：

- `03_messages.v<N>.md`：03 頁的正文副本（03 頁這一輪沒改也照樣輸出）。
- `03_messages.v<N>.csv`：CSV 的副本，逐位元組照抄（BOM、LF 都保留）。
- `03_messages.v<N>.marked.md`：合併的標示版。前半是 03 頁的逐行差異，規則同上；後半是「03_messages.csv 的逐碼差異」。

CSV 的逐碼差異：新舊兩版依 `code` 對齊、逐欄比較，每個有改動的代碼寫成一段 `#### VKnnnn`，依新表頭的欄位順序列出這個代碼的各欄。改過的欄寫成紅底舊值 → 綠底新值，沒改的欄照原樣列出、不加標記。新增的代碼在標題下一行註記綠底「（本碼新增）」、各欄標綠；改成 `retired` 的註記紅底「（本碼停用）」；從 CSV 拿掉的列註記紅底「（本列刪除）」、各欄標紅。表頭改了（例如刪掉欄）時，逐碼差異開頭先標出新舊表頭，並逐欄註記紅底「（本欄刪除）」或綠底「（本欄新增）」；新增的欄照新表頭的位置列出，各碼標綠新值並註記綠底「（本欄新增）」，新值是空的不算改動；刪掉的欄排在新表頭各欄之後，列出舊值並標紅，所以只刪欄的代碼也算有改動。沒改動的代碼不成段，最後用一行列出有幾個、是哪些。欄位值裡的 `<`、`>` 會跳脫，占位符照原樣看得到；格內換行改成 `<br>`。

CSV 的基準版是 `doc/decisions/_backup/doc_contract_03_messages.<後綴>.csv`，攤平規則跟 `.md` 相同，只差副檔名。兩個檔只有一個有基準版時，另一個視為這一輪沒改；CSV 沒有基準版、也不在 git 的 `HEAD` 裡時，視為新建、整份標新增。這兩種情況都會印在輸出，也寫在標示版開頭。兩個都沒有基準版就停下。基準後綴寫 `new` 時，兩個檔都整份標新增。

## 送審打包（`pack_review.py`）

把要送審的標示版打包成一個 zip，檔名一律是 `review_v<N>.zip`：

```sh
python3 script/pack_review.py --note <審閱說明.md> --out <目錄> 03_messages 04_interface GLOSSARY.md
```

在 repo 根目錄執行，頁鍵的寫法跟 `mark_changes.py` 相同。每個鍵取 `doc/decisions/_marked/` 裡 `versions.json` 記的那一版：`<鍵>.v<N>.marked.md`、`<鍵>.v<N>.md`，有 `<鍵>.v<N>.csv` 也一起放。缺檔或 `versions.json` 沒有這個鍵就停下報錯，不取號。zip 的 N 是 `versions.json` 的 `review_zip` 加一並寫回；zip 內檔名不帶目錄，有 `--note` 時審閱說明排第一個。沒給 `--out` 就放在系統暫存目錄，不寫進 repo。跑完印出 zip 路徑與內容清單。本工具只打包，標示版照舊由 `mark_changes.py` 產生。

版號遞增、內容與缺檔報錯由 [pack_review 測試](test/test_pack_review.py) 涵蓋。

## 訊息表自檢（`check_messages.py`）

`doc/contract/03_messages.csv` 是每個原因代碼的唯一出處（#122）。改了 CSV，或其他頁引用代碼的地方就跑：

```sh
python3 script/check_messages.py
```

在 repo 根目錄執行。全過印 `OK` 回 0，任一不過逐條印出回 1。CSV 還不存在時印 `OK` 並跳過。錯誤位置報 `<檔>:<代碼>:<欄名>`，例如 `doc/contract/03_messages.csv:VK0003:next_step`，不報實體行號。查這幾件事：

- 格式：UTF-8 開頭恰好一個 BOM、只准 LF、檔尾恰好一個換行；表頭逐字等於 `code,status,level,exit_code,disposition,situation,message,description,next_step`；用 `csv` 模組以 strict 照 RFC 4180 解析，每列欄數相同。格內換行（雙引號包住的 LF）解析得過。欄位頭尾不准空白，不准以 `=`、`+`、`-`、`@`、Tab、CR 開頭（Excel 會當成公式）。
- 代碼：`VK` 加四位數字，從 `VK0001` 起逐列加一，所以唯一、遞增、不缺列；停用的代碼留列。
- `status` 只准 `active`、`retired`。`retired` 列只留 `code`、`status`、`situation`，其餘欄要空白。
- `active` 列：`level` 只准 `warn`、`error`、`fatal`；`exit_code` 必須依序對應 `1`、`2`、`3`；`situation`、`message`、`description` 必填。
- `disposition` 只准「需人處理」「失敗」或空白；`warn` 一律空白；「需人處理」必有 `next_step`；「失敗」的 `next_step` 必須空白。
- `message` 不准含中文字元（中文說明放 `description`）。
- `next_step` 有值時，必須逐字出現在 `message` 裡。
- 欄位不准 HTML（有屬性的標籤、結束標籤、`<ins>`、`<br>` 這類常見標籤名、`<!--`）與 Markdown（反引號、粗體、刪除線、連結、行首的標題、清單或引言記號）；不帶屬性的 `<…>`（例如 `<repo>`、`<P>`）算占位符。`<`、`>` 要成對、不巢狀。
- 引用：`README.md`、`doc/contract/*.md`、`GLOSSARY.md` 裡出現的每個 `VKnnnn` 都要在 CSV 裡、而且是 `active`；`doc/adr/*.md` 只要求在 CSV 裡，可以是 `retired`。連到 `03_messages.csv` 不准帶 `#`；連結文字是代碼時不准連 `03_messages.md`（03 頁不放逐碼內容），一律連 CSV。01、02 不准連 CSV。
- 診斷範例：`README.md`、`doc/contract/*.md`、`GLOSSARY.md` 裡的 `vendor_kit: <level>[VKnnnn]: <本文>`，level 要等於 CSV，本文要符合 message 第一行，`<…>` 占位符可以對應任意文字。
- `active` 列的 `message` 句首要大寫，或以占位符、小寫指令名 `just` 開頭；結尾要是句點，或以 `next_step`、`just vendor_kit` 指令結尾。

欄位約定：`message` 是印出的英文本文，不含 `vendor_kit: <level>[VKnnnn]: ` 前綴、不准含中文（規則 4）；`description` 是給人讀的中文說明。

CSV 的 `situation`、`message`、`next_step` 裡的 `just vendor_kit …` 指令寫法由 `check_review_pages.py` 檢查，跟 03 頁反引號裡的指令用同一個函式：每個選項與 `@<tag>` 寫法都要在 `GLOSSARY.md`、01、02 出現過。CSV 裡的指令沒有反引號，範圍從 `just vendor_kit` 起，到英文收尾 `and retry.`、`;`、`,`、`(`、句尾句點、第一個非 ASCII 字或欄尾為止。

各條規則的正反例在 [check_messages 測試](test/test_check_messages.py)。

## 名詞表自檢（`check_context.py`）

根 `GLOSSARY.md` 每改一次就跑，不要目視：

```sh
python3 script/check_context.py
```

`GLOSSARY.md` 照 domain-modeling skill 的格式（[CONTEXT 格式說明](../.claude/skills/domain-modeling/CONTEXT-FORMAT.md)）：沒有目錄，`## Language` 底下的 `###` 分群標題本身就是大綱；要連到某個名詞，連到它所在分群標題產生的錨點。

查這幾件事，全過印 `OK` 回 0，任一不過逐條印出回 1：

- HTML 只准 `<ins>`（行內程式碼與程式碼區塊裡的不算）；錨點一律由標題產生，不寫 `<a id>`。
- 沒有 `## 目錄`。
- 每個名詞是 `**名詞**（english）：` 格式、在某個 `###` 分群底下、下一行是定義，名詞不重複。
- 所有 `_Avoid_` 列出的詞都沒出現在正文（`_Avoid_:` 那行本身除外）。改名沒改乾淨，會在這裡擋下。

## 名詞連結與舊名殘留自檢（`check_terms.py`）

`check_context.py` 只管 `GLOSSARY.md` 自己；對外文件的名詞連結，以及改名改到一半、舊詞留在某一頁或 CSV 的某一格，要靠這支抓：

```sh
python3 script/check_terms.py
```

每個問題都報檔名與位置；名詞連結問題會一併報名詞，舊名殘留印 `<檔>:<行號>  <詞>  <該行內容>`（CSV 印 `<檔>:<代碼>:<欄名>  <詞>  <欄位內容>`）。全乾淨印 `OK` 加統計；有警告或錯誤回 1，乾淨回 0。

- **名詞連結**：根目錄 `README.md` 與 `doc/contract/01`～`04` 的 Markdown 頁面中，每個 `GLOSSARY.md` 粗體詞條第一次出現在正文時，都要連到該詞所在的 `###` 分群標題。`A` / `B` 形式的詞條拆成兩個名稱；`_Avoid_` 詞不算名詞。
- **連結目的地**：指向的 `GLOSSARY.md` 錨點必須存在，而且該分群底下確實收錄連結文字所指的名詞；連錯分群或使用不存在的錨點都會失敗。
- **不算正文的位置**：標題、程式碼區塊與行內程式碼不參與第一次出現的判定；已是連結文字的名詞會用該連結驗證。程式碼樣的名詞在正文作為連結文字時不加反引號，例如 `[\<repo\>](…)`、`[dist/](…)`。
- **禁止名詞底線**：上述對外文件不准出現 HTML `u` 或 `ins` 標籤；名詞改用連結，不再用 HTML 底線標記。

- **詞從哪裡來**：每次跑都從根 `GLOSSARY.md` 的 `_Avoid_:` 行現抽，不寫死清單。名詞表會長大，寫死的清單幾次改名之後就跟名詞表脫鉤，而且是靜默的。
- **掃哪些檔**：`git ls-files -co --exclude-standard` 取得的現行 `.md` 檔，加上 `doc/contract/*.csv` 的文字欄（`situation`、`message`、`description`、`next_step`）。排除 `_backup/`、`review_log/`、`doc/decisions/_marked/`（歷史快照與本地產物）、`.claude/skills/`（vendored 的第三方 skill）、`script/diagram/` 與 `discussion.drawio`（架構圖已凍結，裡面的舊詞是歷史），以及 index 裡還留著但已刪除的檔。
- **不算殘留的行**：`_Avoid_:` 行本身；以及帶「舊名」「已廢止」「已移除」「之名作廢」「舊審閱頁」「改名」這類引述標記的行，因為講改名史本來就得同時寫出新舊兩個詞。標記清單是 `check_terms.py` 頂端的 `QUOTE_MARKERS` 常數，要放行新的講法就加在那裡。
- **逐行白名單**：已定案要保留舊詞的**個別一行**登記在 `check_terms.py` 頂端的 `WHITELIST`，每筆是 `(檔案路徑, 該行必須包含的字串, 理由)`。三個欄位都要對上才放行，而且只放行「那段字串裡面」的舊詞：把字串從該行挖掉之後還搜得到舊詞，照樣算殘留。所以同一個檔的其他行、同一行的其他位置、別的檔抄同一段字，全都還是會被抓到。只比對詞會讓那個詞全域失效、只比對檔案會讓整個檔失效，白名單就成了漏洞，所以這兩種寫法刻意不做。白名單筆數印在 `OK`／`FAIL` 那行，悄悄長大會看得見。
- **目前沒有登記**：`WHITELIST` 是空的。（歷史：過去登記過 01 審閱頁的舊標題與 `doc/decisions/README.md` 引用它的那一列；維護者 2026-09-30 定案把標題改成「01 目的與承諾」後，這兩筆已拿掉。）
- **「數位簽章」例外**：「簽章」是名詞「印記」的舊名，但「數位簽章」是密碼學的標準術語（digital signature），跟印記無關；講 registry 或 image 的簽章時本來就該這樣寫。所以用負向前瞻 `(?<!數位)簽章` 只抓單獨的「簽章」，否則這支腳本會逼著大家把正確的詞改掉。

## 中英排版自檢（`check_typography.py`）

改了 `README.md`、`doc/contract/*.md`、`doc/contract/*.csv` 或 `GLOSSARY.md` 就跑，CI 的 docs-lint job 也跑這支：

```sh
python3 script/check_typography.py
python3 script/check_typography.py --fix
```

在 repo 根目錄執行。全過印 `OK` 回 0；有違規逐條印 `<檔>:<行>: <問題與建議寫法>` 回 1。加 `--fix` 直接改檔，只動下面三條規則涉及的空白與括號，其他字元不動。規則是維護者定案的：

- 括號裡全是 ASCII（英文、數字、符號）時用半形括號，半形括號與中文之間空一格：「檢查（test）」寫成「檢查 (test)」。括號裡有中文就維持全形「（…）」。
- 中文與英文字母或阿拉伯數字相鄰時中間空一格：「VK的recipe」寫成「VK 的 recipe」、「第12條」寫成「第 12 條」。全形標點（，。、：；「」（）等）與英數之間不加空白。
- 行內程式碼（反引號包住的）與前後的中文相鄰時也空一格：「`0`結束」寫成「`0` 結束」、「印`VK0024`」寫成「印 `VK0024`」。與全形標點相鄰不加空白；隔著連結的 `[` 或 `](…)` 時照上一條，連結記號不算字元。

不查行內程式碼的內容、程式碼區塊、URL、Markdown 連結目標（括號裡的路徑與錨點）與 HTML 標籤。CSV 只查文字欄（`situation`、`message`、`description`、`next_step`），`code`、`status`、`level`、`exit_code`、`disposition` 是固定值域，不查；英文的 `message` 與 `next_step` 仍會掃描，但不會因英文排版本身誤報。`--fix` 改到 CSV 之後再跑 `check_messages.py`，確認 `next_step` 仍逐字出現在 `message` 裡；改到標題時 GitHub 產生的錨點跟著變，連到舊錨點的連結不會自動改，要另外改。

各條規則的正反例與排除範圍在 [check_typography 測試](test/test_check_typography.py)。

## 圖面工具

見[圖面工具說明](diagram/README.md)。
