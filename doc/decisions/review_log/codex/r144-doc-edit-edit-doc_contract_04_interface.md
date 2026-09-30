已完成，未 commit、未 push，也未執行任何 git 寫入指令。

- `doc/contract/04_interface.md:3-301`：移除全部 `<ins>`，將正文首次出現的 GLOSSARY 名詞改為正確分群連結；程式碼型名詞採 B 式連結文字。
- `doc/decisions/_backup/doc_contract_04_interface.pre_r144.md`：保存修改前原檔；`cmp` 驗證與 HEAD 原檔一致。
- 連結驗證：所有本機連結路徑均存在。
- `git diff --check`：通過。

檢查輸出：

```text
OK: 掃 31 個 .md 檔、1 個 CSV、21 個 _Avoid_ 詞、72 個名詞、白名單 0 筆
OK: 分群 9、名詞 69、_Avoid_ 詞 21
OK: 掃 5 個對外文件
OK: 檢查 doc/contract/03_messages.csv
Ran 157 tests in 14.369s
OK
EXIT check_terms=0 check_context=0 check_review_pages=0 check_messages=0 unittest=0
```