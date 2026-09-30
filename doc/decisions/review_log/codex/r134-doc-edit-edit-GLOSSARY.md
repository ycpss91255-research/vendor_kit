已完成，未 commit、push 或執行任何 git 寫入指令。

備份：`doc/decisions/_backup/GLOSSARY.pre_r134.md`，確認與修改前原檔一致。

驗證結果：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：OK
- unittest：88 tests passed
- `git diff --check`：通過

改動：

- [GLOSSARY.md](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/GLOSSARY.md:204)：修改「失敗」定義，改為不承諾可直接執行的修法，但可以附一般建議。