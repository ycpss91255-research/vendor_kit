已完成，未 commit、未 push，也未執行任何 git 寫入指令。

備份已建立：
`doc/decisions/_backup/doc_contract_03_messages.pre_r144.md`

驗證結果：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：OK
- `check_typography.py`：OK
- 單元測試：151 tests，OK

修改明細：

- [doc/contract/03_messages.md:3](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.md:3)：將 VK、結束碼、診斷、契約的首次正文出現改為名詞表分群連結。
- [doc/contract/03_messages.md:17](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.md:17)：替 level、警告、需人處理、失敗、薄殼、VK 檔、引擎、repo 檔、執行紀錄加入首次出現連結。
- [doc/contract/03_messages.md:27](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.md:27)：替合併衝突與工具加入首次出現連結。
- [doc/contract/03_messages.md:49](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.md:49)：替詢問、初始檔、使用者加入首次出現連結。
- [doc/contract/03_messages.md:61](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.md:61)：移除執行紀錄後續出現處的 `<ins>`。
- [doc/contract/03_messages.md:66](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.md:66)：替正常輸出與原因代碼加入首次出現連結。