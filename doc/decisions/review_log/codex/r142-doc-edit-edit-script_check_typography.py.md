已完成，未 commit、未 push，也未執行任何 git 寫入指令。

- `script/check_typography.py:14`：將 `exit_code` 列為不掃描的 CSV 固定欄。
- `script/check_typography.py:40`：CSV 欄位結構更新為 9 欄，加入 `exit_code`、`description`。
- `script/check_typography.py:43`：文字掃描欄加入 `description`；保留 `message`、`next_step` 掃描。
- `doc/decisions/_backup/script_check_typography.pre_r142.md`：已保存修改前原檔。

驗證結果：

- 本檔 35 項測試：通過
- `check_typography.py`：通過，檢查 7 個檔
- `check_terms.py`：通過
- `check_context.py`：通過
- `check_messages.py`：通過，但因 `03_messages.csv` 尚不存在而跳過
- `check_review_pages.py`：失敗；同一個尚不存在的 `03_messages.csv` 造成 26 個失效連結
- 完整測試：143 項中 1 項失敗；`test_check_terms.py` 的 CSV 欄位期待仍是舊結構，屬其他並行修改範圍
- `py_compile`、`git diff --check`、欄位宣告與備份腳本驗證：全部通過