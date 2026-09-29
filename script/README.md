# script — 審閱與圖面工具

## 對外文件的改動標示（`mark_changes.py`）

對外文件（審閱頁 `doc/decisions/review/0N_*.md` 與根目錄 `README.md`）每改一輪，就產一份標示版讓人只看差異：新增文字用綠底 `<mark>`；刪除或被取代的舊文字用紅底 `<mark>`。標示版只在本機審閱用、不進 git（`doc/decisions/_marked/` 在 `.gitignore` 裡），所以可以用 GitHub 會濾掉的 `<mark>` 內嵌樣式；審完只留最終版。內部文件（本檔、`AGENTS.md`、各目錄的 README、ADR 規則等）改完不產標示版、不送審。

### 一輪的流程

1. **改之前先備份**。每輪一個後綴，依序遞增：

   ```sh
   cp doc/decisions/review/02_invariants.md \
      doc/decisions/_backup/doc_decisions_review_02_invariants.pre_r65.md
   ```

   備份檔名是**把路徑攤平**（`/` 換成 `_`、去掉開頭的點）加上 `.pre_<後綴>`。所有檔都用這套命名，不限審閱頁；`doc-apply` workflow 的護欄也照這個規則。

2. **改**（派子代理做，主對話只協調）。

3. **產標示版**：

   ```sh
   python3 script/mark_changes.py pre_r65 01_purpose 02_invariants
   ```

   要在 repo 根目錄執行。審閱頁傳頁名（不含 `.md`）；根目錄 README 傳相對 repo 根目錄的路徑 `README.md`：

   ```sh
   python3 script/mark_changes.py pre_r91 README.md
   ```

   新建的頁沒有舊版，基準後綴寫 `new`，整份標成新增。

   所有對外文件的標示版都輸出到 `doc/decisions/_marked/<鍵>.v<N>.marked.md`。鍵對審閱頁是頁名（例如 `03_interface`），對其他檔是攤平後的路徑（`/` 換成 `_`、去掉 `.md` 與開頭的點，所以 `README.md` 的鍵是 `README`）。`<N>` 每跑一次加一（版本號記在 `doc/decisions/_marked/.<鍵>.rev`），舊的那份會被刪掉，所以交出去的永遠是最新版、而且看檔名就分得出新舊。後綴就是步驟 1 用的那個，決定「跟哪一版比」。

4. **基準永遠是審閱者上次看過的那一版**，不是最舊的那一版。他看過並回饋之後，下一輪的後綴就換成他讀的那一版。已經討論完的段落不該再標成新改動，紅綠色只留給他還沒看過的。

5. **只把標示版交給審閱者**。定案之後才給完整檔。

6. **定案就 commit**。commit 之後下一輪的比較基準改成 git：

   ```sh
   git show HEAD:doc/decisions/review/02_invariants.md \
     > doc/decisions/_backup/doc_decisions_review_02_invariants.pre_r66.md
   ```

### 標示規則

- 表格列在儲存格內標記，不把整列包起來。整列包住會讓那一列不再是合法的表格列，GitHub 與 VS Code 都會把表格切斷。
- 標題、清單、引言的行首記號留在標籤外（`## <mark style="background:#c8f7c5">目錄</mark>`），否則標題會變成普通文字。
- 粗體留給結構標籤、底線留給名詞標記、綠底與紅底的 `<mark>` 留給改動，三者互不衝突。

## 名詞表自檢（`check_context.py`）

根 `CONTEXT.md` 每改一次就跑，不要目視：

```sh
python3 script/check_context.py
```

查四件事，全過印 `OK` 回 0，任一不過逐條印出回 1：

- `## 目錄` 的分群與 `## Language` 下的 `###` 分群一字不差、順序一致。
- 每個目錄條目的 `#term-xxx` 對得上一個 `<a id="term-xxx"></a>`，兩邊數量、分群歸屬與順序都一致，錨點不重複。
- 每個錨點的下一行是 `**名詞**（english）：` 格式，且目錄寫的名詞與正文一致。
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
- **目前的兩筆**：`doc/decisions/review/01_purpose.md` 的 `# 01 專案目的與承諾` 與 `doc/decisions/README.md` 裡引用這個標題的那一列。使用者定案：標題保留這個舊名，因為那裡指的是 VK 這個專案本身，不是名詞表裡指使用者 repo 的那個詞；`README.md` 那一列是在引用頁標題，同一個道理。（這一行自己帶「舊名」標記，靠上面的引述規則過關，不再多開一筆白名單。）
- **「數位簽章」例外**：「簽章」是名詞「印記」的舊名，但「數位簽章」是密碼學的標準術語（digital signature），跟印記無關；講 registry 或 image 的簽章時本來就該這樣寫。所以用負向前瞻 `(?<!數位)簽章` 只抓單獨的「簽章」，否則這支腳本會逼著大家把正確的詞改掉。

## 圖面工具

見[圖面工具說明](diagram/README.md)。
