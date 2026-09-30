`script/check_review_pages.py` 已符合需求：指令掃描欄位為 `situation、message、next_step`，因此未製造額外修改。

驗證結果：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK，掃描 5 個對外文件
- `check_messages.py`：FAIL，29 個問題，皆來自並行修改中的 `03_messages.csv`
- `check_typography.py`：OK
- 完整單元測試：143 項中 1 項失敗，為並行修改中的 `test_check_terms.CsvTest.test_csv_text_fields_scanned`

檔案異動：

- `doc/decisions/_backup/script_check_review_pages.pre_r142.md`：建立修改前備份，已用 `cmp` 驗證與原檔完全相同。
- `script/check_review_pages.py`：無內容異動；現有實作已符合本輪要求。

未執行 commit、push 或任何 git 寫入指令。