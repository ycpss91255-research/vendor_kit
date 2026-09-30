已完成，未 commit、未 push，也未執行任何 git 寫入指令。

驗證結果：

- 自訂 CSV 結構檢查：PASS（32 列、UTF-8 BOM、LF、9 欄、description、exit_code、next_step、占位符均符合）
- `check_terms.py`：PASS
- `check_context.py`：PASS
- `check_review_pages.py`：PASS
- `check_messages.py`：FAIL（7 項；檢查器將需求明定保留原名的中文占位符誤判為中文本文，如 `<指令>`、`<原因>`；未修改其他代理負責的檢查器）

備份已建立：`doc/decisions/_backup/doc_contract_03_messages.pre_r142.csv`，與修改前原檔逐位元相同。

修改清單：

- `doc/contract/03_messages.csv` 表頭：調整為指定的九欄順序，新增 `exit_code`、`description`。
- `doc/contract/03_messages.csv` 全部 active 列：依 level 填入 warn→1、error→2、fatal→3。
- `doc/contract/03_messages.csv` `message`：32 筆診斷改為英文，保留原占位符及逐字 `next_step`。
- `doc/contract/03_messages.csv` `description`：逐筆保留原中文訊息內容。
- `doc/contract/03_messages.csv` 檔案格式：維持 UTF-8 BOM、LF 與合法 CSV 引號跳脫。