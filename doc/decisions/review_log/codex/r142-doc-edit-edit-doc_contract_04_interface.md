已完成，未 commit、未 push，也未執行任何 git 寫入指令。

備份已建立並以 `cmp` 驗證一致：

`doc/decisions/_backup/doc_contract_04_interface.pre_r142.md`

檢查結果：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：FAIL；並行修改中的 `03_messages.csv` 表頭尚未加入 `exit_code`、`description`
- 診斷範例數量及英文檢查：OK
- `git diff --check`：OK

改動：

- `doc/contract/04_interface.md:132`：VK0024 診斷改為英文。
- `doc/contract/04_interface.md:145`：VK0025 診斷改為英文。
- `doc/contract/04_interface.md:150`：VK0026 診斷改為英文。
- `doc/contract/04_interface.md:155`：VK0027 診斷改為英文。
- `doc/contract/04_interface.md:232`：VK0022 診斷改為英文，並保留可直接執行的 `next_step`。