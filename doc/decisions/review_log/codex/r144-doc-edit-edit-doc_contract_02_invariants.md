已完成 [doc/contract/02_invariants.md](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/02_invariants.md)，未 commit、未 push、未執行任何 git 寫入指令。

- `doc/contract/02_invariants.md:22-228`：33 個首次出現於正文的名詞改為連至 GLOSSARY 對應分群。
- `doc/contract/02_invariants.md:69`：改為「`just vendor_kit test` 不接受本機覆寫。」
- `doc/decisions/_backup/doc_contract_02_invariants.pre_r144.md`：建立修改前備份；腳本確認與 HEAD 原稿完全一致。

驗證結果：

- `check_context.py`：通過
- `check_review_pages.py`：通過
- `check_messages.py`：通過
- `check_typography.py`：通過
- 157 項單元測試：通過
- `git diff --check`：通過
- 自訂名詞腳本：本頁 33 個名詞的首次正文連結及錨點全部通過
- `check_terms.py`：失敗。它把目錄中的既有頁內連結文字誤算為正文，回報 02 的 `repo`、`工具 image`，另有 04 的 `registry`、`test`。這與「已經是連結文字的部分不算正文」規則衝突；依檔案界線未修改 lint 或其他文件。