已完成，未 commit、未 push，也未執行 git 寫入指令。

備份：`doc/decisions/_backup/doc_contract_03_messages.pre_r143.csv`

檢查結果：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_typography.py`：OK
- 單元測試：151 項全數通過
- `check_messages.py`：CSV 本身通過；因並行修改中的 `doc/contract/04_interface.md` 仍有 3 處引用已退役的 `VK0003` 而失敗，位置為第 204、212、310 行

修改明細：

- `doc/contract/03_messages.csv`／`VK0003`：改為 `retired`，依規則清空 level、exit code、處置與訊息欄位。
- `doc/contract/03_messages.csv`／`VK0014`：情況改為 `test` 發現基準版落後版本鎖定行。
- `doc/contract/03_messages.csv`／`VK0032`：情況、英文訊息與中文說明改為由 `test` 阻擋本機覆寫，不再提 CI 模式。