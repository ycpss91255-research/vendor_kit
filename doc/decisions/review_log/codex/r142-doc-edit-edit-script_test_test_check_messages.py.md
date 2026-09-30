已完成，未 commit、未 push，也未執行任何 git 寫入指令。

驗證結果：

- 單檔測試：41 tests，OK
- 完整測試：143 tests，OK
- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_typography.py`：OK
- `check_messages.py`：FAIL；並行中的 `03_messages.csv` 仍是舊表頭，缺少 `exit_code`、`description`
- 備份經腳本確認逐位元等於修改前版本
- `git diff --check`：通過

異動：

- [script/test/test_check_messages.py:21](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/test/test_check_messages.py:21)：fixture 改為 9 欄，加入 `exit_code`、中文 `description` 與英文 `message`。
- [script/test/test_check_messages.py:124](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/test/test_check_messages.py:124)：欄數與嚴格 CSV 解析案例改為新表頭結構。
- [script/test/test_check_messages.py:137](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/test/test_check_messages.py:137)：多行訊息案例改用英文。
- [script/test/test_check_messages.py:189](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/test/test_check_messages.py:189)：新增 `description` 必填、message 禁止中文字元、exit code 對應與必填測試。
- `doc/decisions/_backup/script_test_test_check_messages.pre_r142.md`：建立修改前備份。