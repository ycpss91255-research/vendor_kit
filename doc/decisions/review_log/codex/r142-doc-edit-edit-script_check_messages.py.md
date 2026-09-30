已完成，未 commit、push 或執行任何 git 寫入指令。

備份：`doc/decisions/_backup/script_check_messages.pre_r142.md`

驗證結果：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：FAIL 1 項；目前並行修改中的 CSV 仍是舊 7 欄表頭，尚未更新成新 9 欄表頭
- `git diff --check`：通過

變更：

- [script/check_messages.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/check_messages.py:11)：更新規則說明，納入 `exit_code`、`description` 與英文訊息限制。
- [script/check_messages.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/check_messages.py:35)：表頭改為指定的 9 欄順序。
- [script/check_messages.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/check_messages.py:40)：新增 level 對結束碼映射。
- [script/check_messages.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/check_messages.py:62)：新增中文字元偵測。
- [script/check_messages.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/check_messages.py:174)：active 列檢查結束碼一致性、`description` 必填及 `message` 不含中文字元。