# script/github — GitHub 相關工具

盯這個 repo 在 GitHub 上的動靜，以及檢查 PR 規則。都只讀：不改 GitHub 上任何東西。

## watch_github.sh

[watch_github.sh](watch_github.sh) 盯 `ycpss91255-research/vendor_kit` 的 issue 與 PR，每隔一段時間查一次，有事件就每件印一行：新開的 issue／PR、新留言、被關閉或 merge 的 issue／PR。

跑法（在 repo 根目錄）：

```sh
sh script/github/watch_github.sh [間隔秒數，預設 60] [--once]
```

- 不帶 `--once`：一直跑，有事件就印。
- 帶 `--once`：查到第一批事件就印出來並結束。給 Bash `run_in_background` 用，結束時才通知一次；處理完再用同一行重開，就能一直盯著。這個 repo 不用 Monitor（最長 30 分鐘，見 issue #70），`.claude/hooks/monitor_guard.py` 擋下 Monitor 時就指向這一行。

需要已登入的 `gh`。

## check_pr_rules.py 與 scope.json

[check_pr_rules.py](check_pr_rules.py) 檢查一個 PR 合不合規則（#140）：

- 規則 A：本文至少連一個 issue（`Refs #N`、`Refs: #N`、`Closes`／`Fixes`／`Resolves #N`）。不設豁免，連多個允許。
- 一個邏輯目的：每個改動檔照範圍表 [scope.json](scope.json) 對到一個範圍，扣掉附屬檔（測試、README 段、docs.yml 步驟、AGENTS 一句）後只准一個範圍；表上沒列到的檔算違規，要先補表。
- 規則 B（大題與 sub-issue）只是指引，不檢查。

範圍表只寫在 `scope.json` 一處：本機 hook `.claude/hooks/pr_rules_guard.py`（攔 `gh pr create`）與之後的 CI 都呼叫這支。

跑法（在 repo 根目錄）：

```sh
git diff --name-only origin/main...HEAD | python3 script/github/check_pr_rules.py --body-file <本文檔> --files-from -
```

輸出一行 JSON：`{"ok", "issues", "scopes", "problems"}`；全過結束碼 0，有違規 1。測試：`python3 -m unittest discover -s script/github/test`。
