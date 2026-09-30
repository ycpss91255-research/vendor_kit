已完成，未 commit、未 push，也未執行 git 寫入指令。

備份：`doc/decisions/_backup/script_test_test_mark_changes.pre_r142.md`

驗證：

- `python3 -m unittest script.test.test_mark_changes`：40 tests，OK
- 完整 unittest：143 tests，OK
- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_typography.py`：OK
- `check_messages.py`：FAIL；`03_messages.csv` 尚有 7 筆中文 `message`（VK0001、VK0002、VK0005、VK0010、VK0025、VK0026、VK0032），依規則未修改該檔

修改：

- [script/test/test_mark_changes.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/test/test_mark_changes.py:275)：CSV 測試資料改為九欄表頭，加入 `exit_code`、`description`，診斷本文與下一步改用英文。
- [script/test/test_mark_changes.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/test/test_mark_changes.py:334)：補上 `exit_code`、`description`、英文多行本文及移除列的標示斷言。
- [script/test/test_mark_changes.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/test/test_mark_changes.py:455)：已送審版本測試改用完整九欄 CSV，並驗證英文 `message` 差異。