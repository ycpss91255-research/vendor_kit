已完成，未執行 commit、push 或任何 git 寫入指令。

備份：

- `doc/decisions/_backup/GLOSSARY.pre_r142.md`，SHA-256 與修改前原檔一致。

檢查結果：

```text
check_terms.py: OK: 掃 30 個 .md 檔、1 個 CSV、21 個 _Avoid_ 詞、白名單 0 筆
check_context.py: OK: 分群 9、名詞 70、_Avoid_ 詞 21
check_review_pages.py: OK: 掃 5 個對外文件
check_messages.py: OK: 檢查 doc/contract/03_messages.csv
```

改動：

- `GLOSSARY.md`「診斷」：將訊息格式中的 `<中文本文>` 改為 `<英文本文>`。