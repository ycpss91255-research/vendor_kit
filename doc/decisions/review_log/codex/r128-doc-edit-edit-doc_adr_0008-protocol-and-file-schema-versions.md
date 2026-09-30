已完成，未執行 commit、push 或任何 git 寫入指令。

備份：

- `doc/decisions/_backup/doc_adr_0008-protocol-and-file-schema-versions.pre_r128.md`
- 腳本確認與修改前原檔逐位元相同，SHA-256：`e412054f...23b92c2`

改動：

- `doc/adr/0008-protocol-and-file-schema-versions.md:1`：標題明定版本組合不合是 `fatal`，結束碼為 `3`。
- `doc/adr/0008-protocol-and-file-schema-versions.md:3`：首段明定版本組合不合以 `fatal`（結束碼 `3`）結束，維持零寫入規則。

驗證輸出：

- `check_terms.py`：`OK: 掃 29 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆`
- `check_context.py`：`OK: 分群 9、名詞 68、_Avoid_ 詞 21`
- `check_review_pages.py`：`FAIL: 40 個問題`
  - 全部因並行修改期間 `doc/contract/03_messages.md` 不存在。
  - 其中 ADR-0008 的兩個「訊息總表」連結也因此暫時找不到目標；依規則未修改其他檔案。