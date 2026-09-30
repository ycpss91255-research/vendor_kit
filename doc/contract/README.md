# 審閱頁

這個目錄放 <ins>VK</ins> 對外<ins>契約</ins>的審閱頁。給第一次來看的人，也給要改這幾頁的 agent。

## 這個目錄放什麼

一頁一個主題，依序讀：

1. [01 目的與承諾](01_purpose.md)：為什麼做 VK、對<ins>使用者</ins>承諾什麼。
2. [02 不變量](02_invariants.md)：任何版本都必須成立的性質。
3. [03 訊息與錯誤碼總表](03_messages.md)：每個<ins>結束碼</ins>的意思，與 VK 印出、要使用者動手處理的訊息。
4. [04 使用者介面](04_interface.md)：全部 <ins>VK recipe</ins> 與<ins>選項</ins>。

契約放在這裡，不放 issue：issue 不好追蹤改動，也做不了逐頁審與標示版差異。出處：[工作約定](../../AGENTS.md)「決議與文件流程」。

## 寫法規則

- 只能向前依賴：頁 N 只能引用前面的頁與[名詞表](../../GLOSSARY.md)，不引用後面的頁，也不用後面頁才出現的名詞。
- 對外頁不寫「出處」。沿用前面頁的規則時，在正文寫「`依 [頁名](連結#錨點) 第 N 條`」，連到那一條的標題錨點；不引用 ADR 或 issue。
- 名詞第一次出現時用 `<ins>` 標底線。不要用 HTML 的 u 標籤：GitHub 會把它刪掉。出處：[issue #60](https://github.com/ycpss91255-research/vendor_kit/issues/60)。
- HTML 只准 `<ins>`，不寫 `<a id>`、`<br>` 之類的其他標籤。錨點一律由標題產生：要連到表格裡的某一列或名詞表裡的某個名詞，就連到它所在的標題，連結文字寫出是哪一條，例如「以[結束碼 `2`](03_messages.md#結束碼)結束，訊息見[訊息總表](03_messages.md#訊息)」、`[工具](../../GLOSSARY.md#工具與出貨)`。
- 規則只寫一次。其他頁要用到，照上面「對外頁不寫出處」那條寫「依 … 第 N 條」，或連到章節，不重述。
- 連結用有名字的超連結，例如 `[不變量](02_invariants.md)`，不要把路徑當連結文字。

## 版本怎麼迭代

這一節是對外文件審閱的固定流程，新接手的 agent 照這個順序做。出處：維護者 2026-09-30 定案；[issue #64](https://github.com/ycpss91255-research/vendor_kit/issues/64)。

1. **草稿只改在討論分支。** 對外文件是根目錄 [README](../../README.md) 與本目錄的審閱頁（目前 01～04）。草稿一律改在討論分支並開 PR，`main` 上只放定案版。定案之後才 merge 進 `main`，定案的條件見下一節。
2. **改動一律跑 [doc-edit workflow](../../.claude/workflows/doc-edit.js)**。workflow 在第一次修改前自行把原內容備份到 `doc/decisions/_backup/<鍵>.pre_<round>.md`，不用另外手動備份。round 名稱是 `rNN`：取 `doc/decisions/_backup/` 裡最大的 `pre_rNN` 的編號再加一（例如最大是 `pre_r100`，round 就是 `r101`），用過的不能重用。doc-edit workflow 開跑時會檢查 round 的格式是不是 `rNN`、編號是不是最大編號加一，重用或跳號就直接停。目前最大的編號這樣查：

   ```sh
   ls doc/decisions/_backup | grep -oE 'pre_r[0-9]+' | sed 's/^pre_r//' | sort -n | tail -1
   ```

3. **產生標示版與帶版本號的副本。** 改完在 repo 根目錄跑 `python3 script/mark_changes.py <基準後綴> <頁>`（[標示版產生器](../../script/mark_changes.py)），基準後綴是這一輪的備份後綴，例如 `pre_r101`。審閱頁傳頁名，例如 `02_invariants`；根目錄 README 傳 `README.md`。每跑一次：
   - 在 `doc/decisions/_marked/` 產出兩個檔名帶版本號的檔：`<鍵>.vN.marked.md` 是標示版，綠底是新增，紅底是刪除或被取代的舊文字；`<鍵>.vN.md` 是同一版的正文副本。同一個鍵的舊版會被刪掉，只留最新一版。
   - 版本號只在 `_marked/` 的檔名：正式檔與正文副本內都不寫版本號。正式檔名不帶版本號，也不改名，其他文件的連結才不會斷。
   - 版本號 N 取 [版本號紀錄](../decisions/review_log/versions.json)（`doc/decisions/review_log/versions.json`，進 git）裡這個鍵的數字加一並寫回，沒有記錄就是 v1。它跟著 git 走，所以換電腦、新 clone 或清掉 `_marked/` 之後不會從 v1 重來。

   鍵對審閱頁是頁名，對其他檔是攤平後的路徑，規則見[工具說明](../../script/README.md)。
4. **送審。** 用 SendUserFile 把 `<鍵>.vN.md` 與 `<鍵>.vN.marked.md` 兩個檔一起傳給維護者。不傳沒帶版本號的正式檔：看檔名就要知道是哪一版，不用打開才知道。

內部文件（本檔、[工作約定](../../AGENTS.md)、[工具說明](../../script/README.md)、[ADR 規則](../adr/README.md) 等，也就是對外文件以外的所有文件）改完照樣走步驟 2（doc-edit），但不產標示版、不送審；也不准留過時的資訊。

`doc/decisions/_marked/` 與 `doc/decisions/_backup/` 只在本機，不進 git（見[忽略清單](../../.gitignore)），所以標示版與帶版本號的副本要在本機看。正式的改動紀錄是 git 的 commit 歷史。

## 怎樣才算定案

只有維護者針對那一頁明確回覆「定案」才算定案，定案之後才 merge 進 `main`。對其他頁的回覆不算，沒有意見也不算。
