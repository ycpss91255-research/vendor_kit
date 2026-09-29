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

照順序做：

1. **改動。** 一律跑 [doc-edit workflow](/.claude/workflows/doc-edit.js)：改寫 → lint → codex 審查 → 套用必改 → 潤稿。workflow 在第一次修改前自行把原內容備份到 `doc/decisions/_backup/doc_decisions_review_<頁>.pre_<輪次>.md`，不用另外手動備份。
2. **產生標示版。** 在 repo 根目錄跑 `python3 script/mark_changes.py <舊版後綴> <頁>`（[標示版產生器](/script/mark_changes.py)），輸出 `doc/decisions/_marked/<頁>.v<N>.marked.md`：綠底是新增，紅底是刪除或被取代的舊文字。版本號 N 記在 `doc/decisions/_marked/.<頁>.rev`，每產一次加一。
3. **送審。** 把標示版送給維護者審。

審閱頁以外，只有根目錄 [README](/README.md) 是對外文件，也照同一套產生標示版與版本號：產生時傳相對 repo 根目錄的路徑，例如 `python3 script/mark_changes.py pre_r91 README.md`，輸出 `doc/decisions/_marked/README.v<N>.marked.md`，用法見[工具說明](/script/README.md)。

內部文件（本檔、[工作約定](/AGENTS.md)、[工具說明](/script/README.md)、[ADR 規則](/doc/adr/README.md) 等）改完照樣走步驟 1（doc-edit），但不產標示版、不送審；也不准留過時的資訊。

`doc/decisions/_marked/` 與 `doc/decisions/_backup/` 只在本機，不進 git（見[忽略清單](/.gitignore)），所以版本號與標示版要在本機看。正式的改動紀錄是 git 的 commit 歷史。

## 怎樣才算定案

只有維護者針對那一頁的明確回覆才算定案。對其他頁的回覆不算，「看起來沒意見」也不算。
