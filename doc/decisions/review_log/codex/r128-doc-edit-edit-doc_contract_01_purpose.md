已完成，未執行任何 git 寫入、commit 或 push。

備份：
`doc/decisions/_backup/doc_contract_01_purpose.pre_r128.md`

驗證輸出：

```text
DIFF_CHECK: PASS（只新增「有警告也不算成功。」一行）
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 68、_Avoid_ 詞 21
OK: 掃 5 個對外文件
EXIT_CODES check_terms=0 check_context=0 check_review_pages=0
```

- `doc/contract/01_purpose.md`：「VK 對導入的承諾」新增「有警告也不算成功。」