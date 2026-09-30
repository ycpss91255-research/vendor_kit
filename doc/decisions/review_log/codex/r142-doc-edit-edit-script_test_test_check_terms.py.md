已完成，未 commit、未 push，也未執行任何 git 寫入指令。

驗證結果：

- `python3 -m unittest discover -s script/test`：143 tests，全部通過
- `python3 script/check_terms.py`：通過
- `python3 script/check_context.py`：通過
- `python3 script/check_review_pages.py`：通過
- `python3 script/check_typography.py`：通過
- `python3 script/check_messages.py`：失敗；`03_messages.csv` 尚有 7 筆中文 `message`，屬其他並行代理範圍，未修改

修改：

- `script/test/test_check_terms.py:36`：CSV fixture 更新為九欄表頭，加入 `exit_code`、`description`
- `script/test/test_check_terms.py:43`：預期名詞掃描欄改為 `situation`、`description`
- `doc/decisions/_backup/script_test_test_check_terms.pre_r142.md`：保存本輪修改前原檔备份