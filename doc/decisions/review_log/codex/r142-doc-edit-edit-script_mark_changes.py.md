已完成，未執行任何 git 寫入、commit 或 push。

- [script/mark_changes.py:32](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/mark_changes.py:32)：補充 `exit_code`、`description` 新增欄位的 CSV 標示與排序規則。
- [script/mark_changes.py:327](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/mark_changes.py:327)：更新 `diff_csv` 說明，明確涵蓋兩個新欄位。

備份已建立：`doc/decisions/_backup/script_mark_changes.pre_r142.md`，並以 SHA-256 確認與修改後檔案不同。

驗證結果：

- `test_mark_changes`：40 項全過。
- CSV 標示腳本驗證：通過，兩個新欄位均標成新增且順序正確。
- `check_terms.py`：通過。
- `check_context.py`：通過。
- `check_review_pages.py`：通過。
- `check_messages.py`：失敗；並行修改的 CSV 有 7 筆英文 `message` 仍含中文占位符。
- `check_typography.py`：通過。
- 全套 unittest：143 項中 1 項失敗；`test_check_terms.CsvTest.test_csv_text_fields_scanned` 仍期待舊欄位集合，屬其他並行檔案。
- `git diff --check -- script/mark_changes.py`：通過。