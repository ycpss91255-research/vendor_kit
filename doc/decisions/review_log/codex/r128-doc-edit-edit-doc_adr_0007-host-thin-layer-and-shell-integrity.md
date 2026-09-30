已完成，未執行 commit、push 或任何 git 寫入指令。

驗證結果：

- `check_terms.py`：`OK: 掃 29 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆`
- `check_context.py`：`OK: 分群 9、名詞 68、_Avoid_ 詞 21`
- `check_review_pages.py`：`FAIL: 40 個問題`；原因是並行修改中的 `doc/contract/03_messages.md` 當下不存在，導致 README、04 與本 ADR 的既有連結失效，未跨檔修正。
- `git diff --check`：通過。
- 備份：[pre_r128 備份](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/decisions/_backup/doc_adr_0007-host-thin-layer-and-shell-integrity.pre_r128.md)，SHA-256：`3d554fa7ffd7f0666aee0ee9b3badc1001c15a9efefb7d26dafa84b9b1807336`

修改清單：

- [ADR-0007 第 19 行](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/adr/0007-host-thin-layer-and-shell-integrity.md:19)：把 `sync` 的「提示」改為在診斷中列出下一步。
- [ADR-0007 第 29 行](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/adr/0007-host-thin-layer-and-shell-integrity.md:29)：把「提示 `upgrade --engine`」改為在診斷中列出下一步指令。
- [ADR-0007 第 30 行](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/adr/0007-host-thin-layer-and-shell-integrity.md:30)：引擎升級第一段由結束碼 `2` 改為 `warn`／`1`，並同步更新中途狀態的結束碼。