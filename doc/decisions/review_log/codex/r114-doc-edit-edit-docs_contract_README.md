已完成，未執行任何 git 寫入、commit 或 push。

備份：
`doc/decisions/_backup/docs_contract_README.pre_r114.md`

驗證輸出：

```text
OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆
OK: 分群 9、名詞 67、_Avoid_ 詞 21
OK: 掃 5 個對外文件
EXIT check_terms.py=0 check_context.py=0 check_review_pages.py=0
```

- `docs/contract/README.md`「寫法規則」：以指定正則腳本將範例連結文字 `訊息 6-23` 改為 `訊息 M7`。

另以腳本確認：沒有殘留的 `6-數字` 訊息編號，且正文只有上述一處變更。