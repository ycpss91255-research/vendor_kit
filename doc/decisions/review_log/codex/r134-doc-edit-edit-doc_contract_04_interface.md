已完成，未 commit、未 push，也未執行任何 git 寫入指令。

- 備份：`doc/decisions/_backup/doc_contract_04_interface.pre_r134.md`，已用腳本確認與修改前原檔逐位元組相同。
- 四支 lint 全數通過：`check_terms.py`、`check_context.py`、`check_review_pages.py`、`check_messages.py`。
- unittest：88 項全數通過。
- 範圍腳本確認只有指定的一行正文變更。

修改清單：

- [doc/contract/04_interface.md:98](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/04_interface.md:98)：把 `repository name` 連結改為中文「名詞表」，`<repo>` 保留在連結文字外。