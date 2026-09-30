已完成，未 commit、未 push，也未執行任何 git 寫入指令。

驗證結果：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：FAIL，3 項皆來自並行修改中的 `doc/contract/04_interface.md` 仍引用已退役的 VK0003；未代修
- `check_typography.py`：OK
- 單元測試：151 項全部通過
- 範圍與內容斷言：PASS
- 備份與修改前原檔 SHA-256 相同

修改清單：

- [doc/contract/02_invariants.md](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/02_invariants.md:81)：第 3 條改為不分環境；需要寫入進 git 的檔時不得回 `0`，至少印出警告及指令。
- [doc/contract/02_invariants.md](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/02_invariants.md:213)：第 12 條改為任何環境皆採相同且最嚴格行為，列明互動與主機前置條件兩項環境差異，以及具名例外的要求。
- [doc/contract/02_invariants.md](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/02_invariants.md:228)：第 12 條補列 ADR-0013。
- `doc/decisions/_backup/doc_contract_02_invariants.pre_r143.md`：建立修改前備份。

第 7 條沒有 CI 模式或本機覆寫內容，因此未改。實際的本機覆寫段在第 2 條；依「只改第 3、7、12 條」的硬性範圍未跨條修改。