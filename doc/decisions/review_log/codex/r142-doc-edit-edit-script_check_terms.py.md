已完成，未 commit、未 push，也未執行任何 git 寫入指令。

驗證結果：

- `check_terms.py`：通過
- `check_context.py`：通過
- `check_review_pages.py`：通過
- `check_typography.py`：通過
- `check_messages.py`：失敗 29 項，皆來自並行編修中的 `03_messages.csv`
- 完整 unittest：143 項中 1 項失敗；`test_check_terms.py` 仍期待舊欄位，屬另一代理負責更新的檔
- 暫存 CSV 行為測試、`py_compile`、`git diff --check`：通過
- 備份經腳本確認等同修改前內容

改動：

- `script/check_terms.py:112`：CSV `_Avoid_` 詞掃描欄位由舊四欄改為 `situation`、`description`。
- `script/check_terms.py:112`：同步更新註解，說明其餘欄位的值域與語言由 `check_messages.py` 管理。
- `doc/decisions/_backup/script_check_terms.pre_r142.md`：建立修改前備份。