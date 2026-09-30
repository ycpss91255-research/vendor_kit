已完成，未 commit、未 push，也未執行 git 寫入指令。

- `script/test/test_check_review_pages.py:74`：CSV fixture 更新為九欄正式表頭，加入 `exit_code`、`description`，並將 `message` 改為英文。
- `script/test/test_check_review_pages.py:87`：更新英文訊息的指令錯誤斷言，並驗證 `description` 不會被當作指令掃描欄位。

備份已建立：

`doc/decisions/_backup/script_test_test_check_review_pages.pre_r142.md`

驗證結果：

- 目標測試：14 tests，OK
- 全套測試：143 tests，OK
- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_typography.py`：OK
- `check_messages.py`：FAIL，並行修改中的 `03_messages.csv` 尚有 7 列中文 `message`；依限制未修改該檔。
- `git diff --check`：通過。