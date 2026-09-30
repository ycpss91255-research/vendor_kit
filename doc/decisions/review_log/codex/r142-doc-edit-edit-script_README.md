已完成，未 commit、未 push，也未執行任何 git 寫入指令。

備份：`doc/decisions/_backup/script_README.pre_r142.md`，已用 `cmp` 驗證與修改前原檔逐位元組一致。

檢查輸出：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：FAIL；其他代理負責的 `03_messages.csv` 尚有 7 筆 `message` 含中文字元（VK0001、VK0002、VK0005、VK0010、VK0025、VK0026、VK0032）
- `git diff --check -- script/README.md`：通過

改動如下：

- `script/README.md`「訊息表自檢」：更新九欄表頭，加入 `exit_code`、`description`、中英文內容及 level 對應規則。
- `script/README.md`「訊息表自檢」：將指令掃描欄位更新為 `situation`、`message`、`next_step`。
- `script/README.md`「舊名殘留自檢」：CSV 中文名詞掃描欄位更新為 `situation`、`description`。
- `script/README.md`「中英排版自檢」：加入 `description`、`exit_code`，並說明英文欄位仍掃描但不得誤報。