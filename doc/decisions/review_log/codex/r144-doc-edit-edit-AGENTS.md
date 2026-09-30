AGENTS.md 無需修改：檔內沒有 `<ins>`、`<u>` 或名詞底線規則，依指示「沒有就不動」。

驗證結果：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：OK
- unittest：157 tests，全部通過
- `cmp`：AGENTS.md 與修改前備份一致
- 未執行 commit、push 或任何 git 寫入指令

變更清單：

- `doc/decisions/_backup/AGENTS.pre_r144.md`：建立本輪修改前備份。
- `AGENTS.md`：無內容變更。