已完成，未 commit、push 或執行任何 git 寫入指令。

驗證結果：

- 完整測試：`Ran 144 tests`，`OK`
- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_typography.py`：OK
- `check_messages.py`：FAIL，並行修改中的 `03_messages.csv` 尚有 7 筆中文 `message`；依指示未跨檔修正
- `_Avoid_` 詞掃描：0 筆
- 備份內容雜湊與修改前原檔一致

改動：

- [script/test/test_check_typography.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/test/test_check_typography.py:22)：fixture 表頭加入 `exit_code`、`description`，訊息與下一步改成英文。
- [script/test/test_check_typography.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/test/test_check_typography.py:253)：將 `exit_code` 納入固定欄不修改測試。
- [script/test/test_check_typography.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/test/test_check_typography.py:269)：改測 `situation`、`description` 中文排版，新增英文 `message`／`next_step` 不誤報案例。
- [script/test/test_check_typography.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/test/test_check_typography.py:286)：CSV 格式修正案例改由 `description` 承載中文。
- [備份](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/decisions/_backup/script_test_test_check_typography.pre_r142.md)：保存本輪修改前原檔。