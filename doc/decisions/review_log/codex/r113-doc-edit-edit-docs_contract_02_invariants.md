已完成，未執行 commit、push 或任何 git 寫入指令。

備份：`doc/decisions/_backup/docs_contract_02_invariants.pre_r113.md`，SHA-256 與改前原檔一致。

驗證輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
exit_codes: check_terms=0 check_context=0 check_review_pages=0
```

變更：

- [docs/contract/02_invariants.md:190](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:190)：在不變量 10 的「零寫入」承諾補充「執行紀錄不算在內」，並具名連結至第 4 條。