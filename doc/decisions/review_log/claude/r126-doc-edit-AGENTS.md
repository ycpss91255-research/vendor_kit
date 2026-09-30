# r126 doc-edit 審查：AGENTS.md

## 必改

無。改動只有 AGENTS.md:20 一條，符合 ask；沒有違反 #78 Decisions so far 任何一條；沒有碰 01～04 對外承諾；連結 `doc/agents/issue-tracker.md` 存在（無錨點）。

## 建議

- 位置：AGENTS.md:20
  問題：wayfinder 除了「Decisions so far」，也會改 map 本文的「Not yet specified」「Out of scope」（.agents/skills/wayfinder/SKILL.md:93、:101、:113）。新規則禁止改本文，這兩節的更新同樣要改成留言，但這條只點名 Decisions so far，agent 可能以為其他節照舊可改。
  建議：括號改成「wayfinder 會改 map 本文的『Decisions so far』『Not yet specified』『Out of scope』」，或補一句「其他節的更新也一律留言」；同步在 doc/agents/issue-tracker.md 講清楚。
  證據：.agents/skills/wayfinder/SKILL.md:93、:101、:113
- 位置：AGENTS.md:20
  問題：ask 說 hook `issue_body_guard.py` 會擋，但這條沒提，且 worktree 的 .claude/hooks/ 裡找不到此檔；其他偏離條目（AGENTS.md:18）有寫由哪個工具擋。
  建議：hook 落地後補「改本文會被 `.claude/hooks/issue_body_guard.py` 擋下」。
  證據：AGENTS.md:18；`ls .claude/hooks | grep issue` 無結果
