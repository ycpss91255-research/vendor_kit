# script — 審閱與圖面工具

## 對外文件的改動標示（`mark_changes.py`）

對外文件（審閱頁 `doc/decisions/review/0N_*.md` 與根目錄 `README.md`）每改一輪，就產一份標示版讓人只看差異：新增文字用綠底 `<mark>`；刪除或被取代的舊文字用紅底 `<mark>`。標示版只在本機審閱用、不進 git（`doc/decisions/_marked/` 在 `.gitignore` 裡），所以可以用 GitHub 會濾掉的 `<mark>` 內嵌樣式；審完只留最終版。整套審閱流程（討論分支、定案才 merge、送審給哪兩個檔）見[審閱頁說明](../doc/decisions/review/README.md)「版本怎麼迭代」，這裡只講工具。內部文件（本檔、`AGENTS.md`、各目錄的 README、ADR 規則等）改完不產標示版、不送審。

### 一輪的流程

1. **改之前先備份**。改動一律走 doc-edit workflow，由 workflow 在第一次修改前自動備份，不手動建 `*.pre_rNN.md`：手動建的檔會被當成已用掉的 round，也可能蓋掉 workflow 保證為「修改前原檔」的那份備份。workflow 中途失敗就換下一個 round 重跑，不手動補備份。每輪一個 round，寫成 `rNN`：取 `doc/decisions/_backup/` 裡最大的 `pre_rNN` 的編號再加一，不能重用；doc-edit workflow 開跑時會檢查 round 的格式是不是 `rNN`、編號是不是最大編號加一，重用或跳號就直接停。這一輪的基準後綴（也就是備份尾碼）是 `pre_<round>`，例如 round `r65` 的基準後綴是 `pre_r65`。

   備份檔名是 `<鍵>.pre_<round>.md`，鍵是**把路徑攤平**（去掉 `.md`、`/` 換成 `_`、去掉開頭的點）。所有檔都用這套命名，不限審閱頁；`doc-apply` workflow 的護欄也照這個規則。

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
   - 輸出同一版的正文副本 `doc/decisions/_marked/<鍵>.v<N>.md`，內容跟正式檔一樣。

   同一個鍵的舊版標示版與舊版副本會被刪掉，所以交出去的永遠是最新版，而且看檔名就知道是哪一版。正式檔名不帶版本號、不改名，其他文件的連結才不會斷。鍵對審閱頁是頁名（例如 `04_interface`），對其他檔是攤平後的路徑（`/` 換成 `_`、去掉 `.md` 與開頭的點，所以 `README.md` 的鍵是 `README`）。後綴就是步驟 1 用的那個，決定「跟哪一版比」。

   取號與輸出檔名這些行為由 [mark_changes 測試](test/test_mark_changes.py) 涵蓋，在 repo 根目錄跑 `python3 -m unittest discover -s script/test`。

4. **基準永遠是審閱者上次看過的那一版**，不是最舊的那一版。他看過並回饋之後，下一輪的後綴就換成他讀的那一版。已經討論完的段落不該再標成新改動，紅綠色只留給他還沒看過的。

5. **把兩個帶版本號的檔一起交給審閱者**：`<鍵>.v<N>.md` 與 `<鍵>.v<N>.marked.md`。不交沒帶版本號的正式檔。

6. **草稿 commit 在討論分支，定案才 merge 進 `main`**。定案之後，下一輪從 `main` 開新的討論分支，再跑 doc-edit workflow，由它自動備份當時的正式檔當基準，不手動從 `main` 取檔建備份。

### 標示規則

- 表格列在儲存格內標記，不把整列包起來。整列包住會讓那一列不再是合法的表格列，GitHub 與 VS Code 都會把表格切斷。
- 標題、清單、引言的行首記號留在標籤外（`## <mark style="background:#c8f7c5">目錄</mark>`），否則標題會變成普通文字。
- 粗體留給結構標籤、底線留給名詞標記、綠底與紅底的 `<mark>` 留給改動，三者互不衝突。

## 名詞表自檢（`check_context.py`）

根 `CONTEXT.md` 每改一次就跑，不要目視：

```sh
python3 script/check_context.py
```

`CONTEXT.md` 照 domain-modeling skill 的格式（[CONTEXT 格式說明](../.claude/skills/domain-modeling/CONTEXT-FORMAT.md)）：沒有目錄，`## Language` 底下的 `###` 分群標題本身就是大綱；要連到某個名詞，連到它所在分群標題產生的錨點。

查這幾件事，全過印 `OK` 回 0，任一不過逐條印出回 1：

- HTML 只准 `<ins>`（行內程式碼與程式碼區塊裡的不算）；錨點一律由標題產生，不寫 `<a id>`。
- 沒有 `## 目錄`。
- 每個名詞是 `**名詞**（english）：` 格式、在某個 `###` 分群底下、下一行是定義，名詞不重複。
- 所有 `_Avoid_` 列出的詞都沒出現在正文（`_Avoid_:` 那行本身除外）。改名沒改乾淨，會在這裡擋下。

## 舊名殘留自檢（`check_terms.py`）

`check_context.py` 只管 `CONTEXT.md` 自己；改名改到一半、舊詞留在某一頁，要靠這支抓：

```sh
python3 script/check_terms.py
```

每筆殘留印 `<檔>:<行號>  <詞>  <該行內容>`，全乾淨印 `OK` 加統計（掃了幾個檔、幾個 `_Avoid_` 詞）。有殘留回 1，乾淨回 0。

- **詞從哪裡來**：每次跑都從根 `CONTEXT.md` 的 `_Avoid_:` 行現抽，不寫死清單。名詞表會長大，寫死的清單幾次改名之後就跟名詞表脫鉤，而且是靜默的。
- **掃哪些檔**：`git ls-files -co --exclude-standard` 取得的現行 `.md` 檔。排除 `doc/decisions/_legacy/`、`_backup/`、`review_log/`、`doc/decisions/_marked/`（歷史快照與本地產物）、`.claude/skills/`（vendored 的第三方 skill）、`script/diagram/` 與 `discussion.drawio`（架構圖已凍結，裡面的舊詞是歷史），以及 index 裡還留著但已刪除的檔。
- **不算殘留的行**：`_Avoid_:` 行本身；以及帶「舊名」「已廢止」「已移除」「之名作廢」「舊審閱頁」「改名」這類引述標記的行，因為講改名史本來就得同時寫出新舊兩個詞。標記清單是 `check_terms.py` 頂端的 `QUOTE_MARKERS` 常數，要放行新的講法就加在那裡。
- **逐行白名單**：已定案要保留舊詞的**個別一行**登記在 `check_terms.py` 頂端的 `WHITELIST`，每筆是 `(檔案路徑, 該行必須包含的字串, 理由)`。三個欄位都要對上才放行，而且只放行「那段字串裡面」的舊詞：把字串從該行挖掉之後還搜得到舊詞，照樣算殘留。所以同一個檔的其他行、同一行的其他位置、別的檔抄同一段字，全都還是會被抓到。只比對詞會讓那個詞全域失效、只比對檔案會讓整個檔失效，白名單就成了漏洞，所以這兩種寫法刻意不做。白名單筆數印在 `OK`／`FAIL` 那行，悄悄長大會看得見。
- **目前沒有登記**：`WHITELIST` 是空的。（歷史：過去登記過 01 審閱頁的舊標題與 `doc/decisions/README.md` 引用它的那一列；維護者 2026-09-30 定案把標題改成「01 目的與承諾」後，這兩筆已拿掉。）
- **「數位簽章」例外**：「簽章」是名詞「印記」的舊名，但「數位簽章」是密碼學的標準術語（digital signature），跟印記無關；講 registry 或 image 的簽章時本來就該這樣寫。所以用負向前瞻 `(?<!數位)簽章` 只抓單獨的「簽章」，否則這支腳本會逼著大家把正確的詞改掉。

## 圖面工具

見[圖面工具說明](diagram/README.md)。
