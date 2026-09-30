已完成，未 commit、未 push，也未執行任何 git 寫入指令。

- [ADR-0005 第 3 行](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/adr/0005-run-log-and-event-registry.md:3)：新增每條帶原因代碼的 stderr 診斷，須寫入一筆 `diagnostic_emitted` 紀錄及 `vendor_kit.reason_code`，並註明兩種建立紀錄前的例外。
- [ADR-0005 第 16 行](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/adr/0005-run-log-and-event-registry.md:16)：補充 stderr 與結構化紀錄共用診斷資料、原因代碼一致，以及反向並非一對一。
- [pre_r128 備份](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/decisions/_backup/doc_adr_0005-run-log-and-event-registry.pre_r128.md)：已建立；雜湊與改前原檔相同。

驗證結果：

- `check_terms.py`：通過，`OK: 掃 29 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆`
- `check_context.py`：失敗，40 個問題，皆因並行中的 `doc/contract/03_messages.md` 暫時被刪除而導致連結目標不存在。
- `check_review_pages.py`：同樣因上述檔案暫時不存在，回報相同 40 個問題。
- `<u>` 檢查：無 `<u>` 標籤。
- 備份與 `HEAD` 原檔比較：完全相同。