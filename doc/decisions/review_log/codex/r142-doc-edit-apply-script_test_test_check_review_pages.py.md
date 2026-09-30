已完成，未 commit、未 push，也未執行 git 寫入指令。

備份：`doc/decisions/_backup/script_test_test_check_review_pages.pre_r142.2.md`（無序號版本已存在）。

驗證結果：

- `check_terms.py`：通過
- `check_context.py`：通過
- `check_review_pages.py`：通過
- `check_messages.py`：通過
- 指定單測仍因並行修改的 `script/check_review_pages.py` 輸出格式變化而失敗；不屬於本次必改位置，未越界修改 assertion。
- 腳本比對確認只做了兩個指定 replacement。

已改：`test_messages_csv_commands_must_be_defined_earlier` fixture，VK0001 的 disposition 由 `needs_human` 改為空白，VK0002 由 `needs_human` 改為 `需人處理`。