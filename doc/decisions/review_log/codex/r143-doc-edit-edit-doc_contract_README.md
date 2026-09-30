已完成，未執行 commit、push 或任何 git 寫入指令。

驗證全部通過：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：OK
- `check_typography.py`：OK
- unittest：151 tests，OK
- `git diff --check`：通過

修改如下：

- `doc/contract/README.md`「這個目錄放什麼」：移除一般用語「選項」的名詞底線。
- `doc/contract/README.md`「版本怎麼迭代」步驟 3：說明產生器會刪除同鍵舊版，只保留最新版，並要求每輪將刪除與新檔一起 commit。
- `doc/contract/README.md`「版本怎麼迭代」末段：更正 `_marked/` 為進 git；補充每輪 commit，以及定稿時在同一個 commit 刪除舊版並產生最終版。
- `doc/decisions/_backup/doc_contract_README.pre_r143.md`：建立修改前備份，已用 `cmp` 驗證與原檔一致。