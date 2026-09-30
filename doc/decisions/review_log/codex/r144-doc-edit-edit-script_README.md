已完成，未執行 commit、push 或任何 git 寫入指令。

備份已建立：`doc/decisions/_backup/script_README.pre_r144.md`，並確認與修改前原檔逐位元組相同。

驗證結果：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：OK
- `check_typography.py`：OK
- unittest：157 項全數通過
- `git diff --check`：通過

改動：

- [script/README.md:57](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/README.md:57)：將「名詞底線」規則改為首次正文出現時連到 `GLOSSARY.md` 所屬分群。
- [script/README.md:128](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/README.md:128)：將 `check_terms.py` 章節擴充為名詞連結與舊名殘留檢查。
- [script/README.md:139](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/README.md:139)：補充首次連結、分群與錨點驗證、正文排除範圍，以及禁止 HTML `u`／`ins` 標籤的規則。