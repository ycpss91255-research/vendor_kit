已完成，未 commit、未 push，未執行 git 寫入指令。

- 已改：[script/check_terms.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/check_terms.py:112)；掃描欄位改為 `situation`、`message`、`description`、`next_step`，並修正固定值域註解。
- 未改：`script/test/test_check_terms.py` 屬於別的檔，交給跨檔一致性。
- 未改：`script/README.md` 屬於別的檔，交給跨檔一致性。

原有未編號備份未覆寫；修改前版本另存為 `script_check_terms.pre_r142.2.md`，並以 SHA-256 確認內容相同。

指定的四項驗證全部通過：

- `check_terms.py`
- `check_context.py`
- `check_review_pages.py`
- `check_messages.py`