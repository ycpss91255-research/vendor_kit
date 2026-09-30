已完成，未執行 commit、push 或任何 git 寫入指令。

驗證全部通過：

- `check_terms.py`：OK，掃描 31 個 Markdown、1 個 CSV
- `check_context.py`：OK，分群 9、名詞 69
- `check_review_pages.py`：OK，掃描 5 個對外文件
- `check_messages.py`：OK
- `check_typography.py`：OK，檢查 8 個檔
- 單元測試：151 項全部通過

變更：

- `doc/decisions/_backup/README.pre_r144.md`：建立修改前備份。
- `README.md:3`：首次出現的 VK、工具、repo、初始檔、安裝目錄連到名詞表對應分群。
- `README.md:23`：啟動器連到「VK 組件」。
- `README.md:35`：失敗連到「執行與結果」。
- `README.md:44`：引擎連到「VK 組件」。
- `README.md:61`：結束碼連到「執行與結果」。
- `README.md:68`：使用者連到「角色與情境」。