已完成，未執行 commit、push 或任何 git 寫入指令。

備份：[docs_adr_0008-protocol-and-file-schema-versions.pre_r116.md](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_backup/docs_adr_0008-protocol-and-file-schema-versions.pre_r116.md)，SHA-256 與修改前原檔一致。

驗證輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
M-number check: PASS
local link target check: PASS
exit codes: check_terms=0 check_context=0 check_review_pages=0 extra=0
```

改動：

- [docs/adr/0008-protocol-and-file-schema-versions.md:29](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:29)：將「訊息 M6」改成具名的「訊息總表」連結，保留既有結束碼 `3`。
- [docs/adr/0008-protocol-and-file-schema-versions.md:31](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:31)：將「訊息 M4」改成具名的「訊息總表」連結，保留既有結束碼 `3`。