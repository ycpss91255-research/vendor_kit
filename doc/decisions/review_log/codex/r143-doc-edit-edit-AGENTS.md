完成，未執行 commit、push 或任何 git 寫入指令。

- [AGENTS.md](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/AGENTS.md:24)：補充 `_marked/` 每輪進 git，以及定稿時同一 commit 刪除舊版並產生最終版。
- 已建立修改前備份：`doc/decisions/_backup/AGENTS.pre_r143.md`。

驗證結果：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：OK
- `check_typography.py`：OK
- 單元測試：151 項全部通過。