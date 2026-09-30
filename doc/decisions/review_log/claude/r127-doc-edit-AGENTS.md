# r127 doc-edit 審查：AGENTS.md

## 必改

（無）

- 已定案：對照 #78 Decisions so far，沒有衝突。
- 對外承諾：只改了內部規則，01～04 都沒動。
- 做完沒：ask 對 AGENTS.md 要求的兩項（擴充括號範圍、條末補 hook 句）都做了（AGENTS.md:20）。
- 連結：diff 裡唯一的連結 `doc/agents/issue-tracker.md` 存在，也沒有錨點。

## 建議

1. 位置：AGENTS.md:20「會被 `.claude/hooks/` 的 hook 擋下」。問題：這句用現在式寫成已經生效，可是這個 worktree 的 `.claude/hooks/` 只有 guard.py 和 test_guard.py，沒有 issue_body_guard.py；PR #67 目前還是 OPEN。依 CLAUDE.md，內部文件不能留跟現況不符的資訊。建議：這個 PR 等 #67 merge 之後再 merge；不然就先寫成「預定由 hook 擋下（PR #67）」。證據：`ls .claude/hooks`；`gh pr view 67` state=OPEN。
2. 位置：AGENTS.md:20。問題：同一句話裡「新定案改在 map 留言記錄」和「Decisions so far…等節的更新也一律留言」重複講了 Decisions so far。建議：兩句合成「map 本文各節（Decisions so far、Not yet specified、Out of scope 等）的更新一律在 map 留言記錄」。證據：AGENTS.md:20。
