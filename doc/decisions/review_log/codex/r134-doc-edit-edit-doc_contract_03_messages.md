已完成，未 commit、未 push，也未執行 git 寫入指令。

備份：

- `doc/decisions/_backup/doc_contract_03_messages.pre_r134.md`
- 腳本比對修改前版本：`backup-check: PASS`

驗證結果：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：OK
- unittest：88 tests，全部通過
- `git diff --check`：通過

修改內容：

- [doc/contract/03_messages.md:31](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.md:31)：補上 A、B、C 各自輸出的示意，使用實際對應的 `VK0022`、`VK0001`，最後以結束碼 `2` 結束。
- [doc/contract/03_messages.md:63](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.md:63)：將「失敗」改定義為不承諾可執行的修法，但可以附一般建議。