已完成，未執行 commit、push 或任何 git 寫入指令。

備份：

- `doc/decisions/_backup/doc_contract_01_purpose.pre_r144.md`：已建立，並驗證與修改前原檔一致。

驗證結果：

- `check_terms.py`：FAIL；僅剩 02、04 頁共 4 處並行修改問題，本頁零錯誤。
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：OK
- `check_typography.py`：OK
- unittest：157 tests，全部通過。
- `git diff --check`：通過。

修改清單：

- `doc/contract/01_purpose.md` 開頭：移除名詞底線說明，將 `VK` 首次正文出現連至「角色與情境」。
- `doc/contract/01_purpose.md`「要解決的痛點」：連結 `工具`、`初始檔`、`repo`、`工具內容`、`使用者`。
- `doc/contract/01_purpose.md`「VK 做的事」：連結 `registry`、`版本鎖定行`、`引擎`、`基準版合併`，移除 `<ins>`。
- `doc/contract/01_purpose.md`「承諾關係」：連結 `導入`、`出貨`、`薄殼`，移除其餘 `<ins>`。
- `doc/contract/01_purpose.md`「VK 對導入／出貨的承諾」：連結 `digest`、`repo 檔`、`VK 檔`、`基準版`、`納管`、`需人處理`、`警告`。
- `doc/contract/01_purpose.md`「VK 對相容性的承諾」：連結 `契約`。