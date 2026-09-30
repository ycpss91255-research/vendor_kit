已完成，未執行 commit、push 或任何 git 寫入指令。

備份：
`doc/decisions/_backup/doc_decisions_scope_roadmap.pre_r116.md`

驗證輸出：

- `check_terms.py`：OK，exit 0
- `check_context.py`：OK，exit 0
- `check_review_pages.py`：OK，exit 0
- `M` 加數字檢查：PASS
- 本地連結目標檢查：PASS
- 備份與修改前 HEAD 相同：PASS

改動：

- `doc/decisions/scope_roadmap.md:35`：把 `M1` 引用改為連結至結束碼 `2`，並以具名連結指向訊息總表。