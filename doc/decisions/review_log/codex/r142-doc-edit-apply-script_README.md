已建立修改前備份：`doc/decisions/_backup/script_README.pre_r142.2.md`。未執行任何 git 寫入、commit 或 push。

- 已改：`script/README.md:98`，檢查項只保留 `message` 不含中文；前綴與 `description` 語言移至欄位約定，明註目前不檢查。
- 已改：`script/README.md:135`，CSV 掃描欄位改列 `situation`、`message`、`description`、`next_step`，刪除不正確的 `check_messages.py` 管理說法。

驗證：

- `check_terms.py`：通過
- `check_context.py`：通過
- `check_review_pages.py`：通過
- `check_messages.py`：失敗，15 項皆來自並行修改中的 03/04 文件，沒有指向 `script/README.md`；依限制未修改其他檔案。