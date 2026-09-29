# 審閱頁

這個目錄放 <ins>VK</ins> 對外<ins>契約</ins>的審閱頁。給第一次來看的人，也給要改這幾頁的 agent。

## 這個目錄放什麼

一頁一個主題，依序讀：

1. [01 目的與承諾](01_purpose.md)：為什麼做 VK、對<ins>使用者</ins>承諾什麼。
2. [02 不變量](02_invariants.md)：任何版本都必須成立的性質。
3. [03 使用者介面](03_interface.md)：全部 <ins>VK recipe</ins>、<ins>選項</ins>、<ins>結束碼</ins>。

契約放在這裡，不放 issue：issue 不好追蹤改動，也做不了逐頁審與標示版差異。出處：[工作約定](/AGENTS.md)「決議與文件流程」。

## 寫法規則

- 每頁只用前面頁與[名詞表](/CONTEXT.md)的名詞，不引用後面頁才出現的名詞。
- 名詞第一次出現時用 `<ins>` 標底線。不要用 HTML 的 u 標籤：GitHub 會把它刪掉。出處：[issue #60](https://github.com/ycpss91255-research/vendor_kit/issues/60)。
- 規則只寫一次。其他頁要用到，標明來源的條號或章節，不重述。
- 連結用有名字的超連結，例如 `[不變量](02_invariants.md)`，不要把路徑當連結文字。

## 版本怎麼迭代

這一節是對外文件審閱的固定流程，新接手的 agent 照這個順序做。出處：維護者 2026-09-30 定案；[issue #64](https://github.com/ycpss91255-research/vendor_kit/issues/64)。

1. **草稿只改在討論分支。** 對外文件是根目錄 [README](/README.md) 與本目錄的審閱頁（目前 01～03）。草稿一律改在討論分支並開 PR，`main` 上只放定案版。定案之後才 merge 進 `main`，定案的條件見下一節。
2. **改動一律跑 [doc-edit workflow](/.claude/workflows/doc-edit.js)**：改寫 → lint → codex 審查 → 套用必改 → 潤稿。workflow 在第一次修改前自行把原內容備份到 `doc/decisions/_backup/<鍵>.pre_<round>.md`，不用另外手動備份。round 名稱是 `rNN`：取 `doc/decisions/_backup/` 裡最大的 `pre_rNN` 的編號再加一（最大是 `pre_r100`，round 就是 `r101`），用過的不能重用。workflow 目前只檢查 round 有填，不檢查編號，也不擋重用（同名備份已存在時會另存成 `.pre_<round>.2.md`），所以開跑前要自己查目前最大的編號：

   ```sh
   ls doc/decisions/_backup | grep -oE 'pre_r[0-9]+' | sed 's/^pre_r//' | sort -n | tail -1
   ```

3. **產生標示版與帶版本號的副本。** 改完在 repo 根目錄跑 `python3 script/mark_changes.py <基準後綴> <頁>`（[標示版產生器](/script/mark_changes.py)），基準後綴是這一輪的備份後綴，例如 `pre_r101`。審閱頁傳頁名，例如 `02_invariants`；根目錄 README 傳 `README.md`。版本號 N 的取號方式見下面最後一條。每跑一次：
   - 正式檔的檔頭自動寫一行 `> 版本 vN`。
   - 在 `doc/decisions/_marked/` 產出兩個檔名帶版本號的檔：`<鍵>.vN.marked.md` 是標示版，綠底是新增，紅底是刪除或被取代的舊文字；`<鍵>.vN.md` 是同一版的正文副本。同一個鍵的舊版會被刪掉，只留最新一版。
   - 正式檔名不帶版本號，也不改名，其他文件的連結才不會斷。
   - 標示版的正文是拿寫入版本號之前的正式檔去比的，所以標示版正文裡的 `> 版本` 行還是前一版（或沒有）；這一版的編號看檔名與標示版開頭的註解。
   - 版本號 N 是 `doc/decisions/_marked/.<鍵>.rev` 記的數字加一，這個檔不存在就從 v1 起算，不讀正式檔檔頭現有的版本號。`.rev` 只在本機，換電腦、新 clone 或清掉 `_marked/` 之後會從 v1 重來，送審前要對照正式檔在 git 裡上一版的檔頭，確認編號沒有倒退。

   鍵對審閱頁是頁名，對其他檔是攤平後的路徑，規則見[工具說明](/script/README.md)。
4. **送審。** 用 SendUserFile 把 `<鍵>.vN.md` 與 `<鍵>.vN.marked.md` 兩個檔一起傳給維護者。不傳沒帶版本號的正式檔：看檔名就要知道是哪一版，不用打開才知道。

內部文件（本檔、[工作約定](/AGENTS.md)、[工具說明](/script/README.md)、[ADR 規則](/doc/adr/README.md) 等，也就是對外文件以外的所有文件）改完照樣走步驟 2（doc-edit），但不產標示版、不送審；也不准留過時的資訊。

`doc/decisions/_marked/` 與 `doc/decisions/_backup/` 只在本機，不進 git（見[忽略清單](/.gitignore)），所以標示版與帶版本號的副本要在本機看。正式的改動紀錄是 git 的 commit 歷史。

## 怎樣才算定案

只有維護者針對那一頁明確回覆「定案」才算定案，定案之後才 merge 進 `main`。對其他頁的回覆不算，沒有意見也不算。
