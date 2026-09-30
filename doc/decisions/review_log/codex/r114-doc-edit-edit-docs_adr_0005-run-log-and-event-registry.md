已完成，未 commit、未 push、未執行任何 git 寫入指令。

驗證輸出：

- `check_terms.py`：`OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆`
- `check_context.py`：`OK: 分群 9、名詞 67、_Avoid_ 詞 21`
- `check_review_pages.py`：`OK: 掃 5 個對外文件`
- 腳本確認舊 `6-N` 殘留：0
- 腳本確認 6 個本機連結目標均存在

備份：

- `doc/decisions/_backup/docs_adr_0005-run-log-and-event-registry.pre_r114.md`：已確認與改前原檔逐位元相同。

改動：

- [docs/adr/0005-run-log-and-event-registry.md](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0005-run-log-and-event-registry.md:23)：將訊息引用 `6-23、6-39、6-40` 改為 `M7、M11、M12`。