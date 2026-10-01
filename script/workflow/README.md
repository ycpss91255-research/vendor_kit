# script/workflow — workflow 的機械步驟

命名 workflow（`.claude/workflows/`）裡固定、不需要判斷的步驟寫成這裡的腳本，子代理只負責呼叫並讀 JSON 結果。目前給 [`pr`](../../.claude/workflows/pr.js) 與 [`pr-fix`](../../.claude/workflows/pr-fix.js) 用。

會寫入 GitHub 的動作（`gh issue create`、sub_issues API、`gh pr create`、`gh pr merge`、留言）**不包進腳本**：hook 要看得到這些 `gh` 指令才擋得了，所以由子代理逐一下指令。這裡的腳本只做本機的事、唯讀的查詢，以及送出前的本文自檢。

## worktree.py

開與收 PR 用的 worktree。位置固定在主 repo 上一層的 `worktree/branch/<分支名>`，跟 `.claude/hooks/worktree_guard.py` 的規則一致。

```sh
python3 script/workflow/worktree.py add <branch>       # git fetch origin，從 origin/main 開新分支與 worktree
python3 script/workflow/worktree.py remove <branch>    # 移除 worktree 與本機分支，不刪遠端
```

- `add`：worktree 目錄或本機分支已存在就報錯。`--base` 可換起點（預設 `origin/main`）。
- `remove`：分支有還沒推上遠端的 commit，或 worktree 有未提交的改動時拒絕；確定要丟掉才加 `--force`。
- `--repo` 不給時用這支腳本所在 repo 的主 worktree，所以從任何 worktree 裡跑都會開在同一個位置。
- 輸出一行 JSON：成功 `{"ok": true, "action", "branch", "path", ...}`，失敗 `{"ok": false, "error"}` 並以 1 結束。

## wait_ci.py

等 PR 的 CI 跑完並讀出結果，只呼叫唯讀的 `gh pr checks`。

```sh
python3 script/workflow/wait_ci.py <pr> [--timeout 600] [--interval 15]
```

- 每隔 `--interval` 秒查一次，直到每個 check 都結束或過了 `--timeout` 秒（預設 600）。還沒有任何 check 時算還在跑。
- 輸出一行 JSON：`{"pr", "all_pass", "timed_out", "checks": [{"name", "state"}]}`。
- 結束碼：全過 0；有失敗或取消 1；逾時 2；`gh` 本身出錯 3。skipping 算通過。

## body.py

issue 與 PR 本文檔送出前的自檢，只讀檔，不呼叫 `gh`。

```sh
python3 script/workflow/body.py check <file> --kind issue --parent <父題編號>
python3 script/workflow/body.py check <file> --kind pr --issue <issue 編號>
```

- issue：第一行要是 `Part of #<父題>`。
- PR：第一行以 `[claude] ` 開頭，且有一行 `Closes #<issue>`。
- 兩者都不准含本機絕對路徑；樣式跟 `.claude/hooks/comment_tag_guard.py` 的 `LOCAL_PATHS` 相同。
- 輸出一行 JSON：`{"ok", "file", "kind", "problems"}`；全過 0，有問題 1。

## pr_target.py

找出已開 PR 的修改目標，並把 worktree 準備好。只呼叫唯讀的 `gh pr view`，git 動作只在本機，不 push。

```sh
python3 script/workflow/pr_target.py <pr> [--repo <主 repo>]
```

- 分支取 PR 的 headRefName；issue 取 PR 本文第一個 `Closes #N`／`Refs #N`（也認 `Refs: #N`、Fixes、Resolves），找不到就報錯。PR 不是 OPEN 也報錯。
- worktree 位置跟 `worktree.py` 相同（`worktree/branch/<分支>`）。先 `git fetch origin`，不存在就從 `origin/<分支>` 建（本機分支已存在就直接掛上），存在就沿用。
- 檢查：worktree 在 PR 分支、沒有未提交或未追蹤的改動、沒有還沒推的 commit；落後 `origin/<分支>` 就 fast-forward，跟遠端分岔就報錯。
- 輸出一行 JSON：成功 `{"ok": true, "pr", "branch", "issue", "repo", "path", "url", "created", "head", "fast_forwarded", "behind_main"}`，失敗 `{"ok": false, "error"}` 並以 1 結束。

## verify.py

送 PR 前的全部驗證，在 worktree 根目錄跑。

```sh
python3 script/workflow/verify.py [--root <worktree 根目錄>]
```

- 依序跑：`.github/workflows/docs.yml` 每個 `run:`（原樣用 shell 跑）、每個 `script/*/test` 的 unittest（docs.yml 已跑的不重跑）、`script/repo/check_script_layout.py`、`.claude/hooks/test_guard.py`。
- 每個 `script/*/test` 都要出現在 docs.yml 裡，沒出現的列在 `not_in_ci`，算失敗：新類別的測試 CI 要跑得到。
- 輸出一行 JSON：`{"ok", "root", "steps": [{"source", "cmd", "code", "ok", "output"}], "not_in_ci"}`，`output` 只留最後 40 行。全過 0，有失敗 1，找不到根目錄或 docs.yml 2。

## 測試

測試在 [test/](test/)，用暫存的 git repo、暫存的根目錄與假的 `gh`（環境變數 `WAIT_CI_GH`、`PR_TARGET_GH`），不打 GitHub。跑法：

```sh
python3 -m unittest discover -s script/workflow/test
```
