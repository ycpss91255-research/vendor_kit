已完成，未 commit、未 push，也未執行 git 寫入指令。

- 已改：[script/mark_changes.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/mark_changes.py:327) 將 docstring 改為不綁定特定欄位的通則；新增欄有值時只標綠底「本欄新增」，只增加 ins、不增加 dele。
- 未改：`script/test/test_mark_changes.py` 與 `script/README.md` 屬於別的檔，交給跨檔一致性。

備份建立於 `script_mark_changes.pre_r142.2.md`；因無序號備份已存在，依規則使用 `.2`。

腳本驗證：

- 實際 CSV：`ins=103`、`dele=39`；新增欄的 64 個非空值不再計入刪除。
- 合成案例：`ins=2`、`dele=0`。
- `check_terms.py`：通過
- `check_context.py`：通過
- `check_review_pages.py`：通過
- `check_messages.py`：通過
- 語法與 `git diff --check`：通過