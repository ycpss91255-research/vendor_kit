已完成，未 commit、未 push，也未執行任何 git 寫入指令。

備份：`doc/decisions/_backup/docs_contract_README.pre_r116.md`，腳本確認與修改前原檔完全一致。

驗證結果：

- `check_terms.py`：OK，掃 30 個 `.md` 檔
- `check_context.py`：OK
- `check_review_pages.py`：OK，掃 5 個對外文件
- 訊息編號掃描：`M` 加數字殘留 0 處
- 新增連結掃描：2 個目標皆存在
- `git diff --check`：通過

改動清單：

- [docs/contract/README.md 第 11 行](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/README.md:11)：移除 03 訊息「每條有固定編號」的說明。
- [docs/contract/README.md 第 21 行](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/README.md:21)：把 M7 範例改為結束碼 `6-23`，並連到結束碼及訊息總表。