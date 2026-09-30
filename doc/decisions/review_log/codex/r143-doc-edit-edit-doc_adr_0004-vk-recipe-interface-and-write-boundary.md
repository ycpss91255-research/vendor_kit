已完成，未 commit、未 push，也未執行任何 git 寫入指令。

變更：

- [ADR-0004](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:3)：標明 CI 模式及依環境分流的部分已由 ADR-0013 取代。
- [ADR-0004 Considered Options](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:11)：將三項 CI 相關選項標成歷史選項。
- [ADR-0004 Consequences](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:22)：將 CI 偵測、附加規則及環境相依結束碼改成歷史記錄，現行規則改指向 ADR-0013 與訊息總表。
- [pre_r143 備份](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/decisions/_backup/doc_adr_0004-vk-recipe-interface-and-write-boundary.pre_r143.md)：已建立；腳本比對確認與修改前 HEAD 內容一致。

驗證結果：

- `check_terms.py`：通過
- `check_context.py`：通過
- `check_review_pages.py`：失敗；`doc/contract/04_interface.md:20` 的 `#追蹤新版` 錨點尚不存在
- `check_messages.py`：失敗；`doc/contract/04_interface.md:308` 仍引用已退役的 VK0003
- `check_typography.py`：通過，檢查 8 個檔
- `python3 -m unittest discover -s script/test`：151 項通過

兩項失敗均來自並行修改的 `doc/contract/04_interface.md`，未越界修正。