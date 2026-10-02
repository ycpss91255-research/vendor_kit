# script/workflow — workflow 的機械步驟

命名 workflow（`.claude/workflows/`）裡固定、不需要判斷的步驟寫成這裡的腳本，子代理只負責呼叫並讀 JSON 結果。目前給 [`pr`](../../.claude/workflows/pr.js) 與 [`pr-fix`](../../.claude/workflows/pr-fix.js) 用。

會寫入 GitHub 的動作（`gh issue create`、sub_issues API、`gh issue`／`gh pr comment`、`gh issue close`、`gh pr create`、`gh pr merge`）與 `git commit`／`push` 可以寫進腳本，但**一律經 [`hook_rules.py`](#hook_rulespy) 的 `guarded_run`**：腳本內部的指令 Claude 的 hook 看不到，所以寫入前先把即將執行的同一個 argv 交給 `.claude/settings.json` 註冊的每支 Bash hook 檢查，被擋、hook 出錯或逾時都不執行（fail closed）。不准在腳本裡另抄一份 hook 的規則，也不自己呼叫 `subprocess` 做寫入。

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

等 PR 的 CI 跑完並讀出結果，只呼叫唯讀的 `gh pr checks` 與 `gh run view`。

```sh
python3 script/workflow/wait_ci.py <pr> [--timeout 600] [--interval 15] [--failed-logs [--log-lines 80]]
```

- 每隔 `--interval` 秒查一次，直到每個 check 都結束或過了 `--timeout` 秒（預設 600）。還沒有任何 check 時算還在跑。
- 輸出一行 JSON：`{"pr", "all_pass", "timed_out", "checks": [{"name", "state"}]}`。
- `--failed-logs`：多一個 `failed_logs: [{"name", "run_id", "tail", "error"}]`，每個失敗或取消的 check 一筆，沒有失敗時是空陣列。run id 從 check 的 link（`/actions/runs/<id>/`）取，每個 run 只跑一次 `gh run view <id> --log-failed`，`tail` 是最後 `--log-lines` 行（預設 80）。取不到 run id 或 `gh run view` 失敗時 `run_id`／`tail` 為 null、`error` 寫原因。沒給這個旗標時輸出不變，`merge_pr.py` 就是這樣呼叫。
- 結束碼：全過 0；有失敗或取消 1；逾時 2；`gh` 本身出錯 3。skipping 算通過。取日誌失敗不改結束碼。

## body.py

issue 與 PR 本文檔送出前的自檢，只讀檔，不呼叫 `gh`。

```sh
python3 script/workflow/body.py check <file> --kind issue --parent <父題編號>
python3 script/workflow/body.py check <file> --kind pr --issue <issue 編號>
```

- issue：第一行要是 `Part of #<父題>`。
- PR：第一行以 `[claude] ` 開頭，且有一行 `Closes #<issue>`。
- 兩者都不准含本機絕對路徑；規則經 [`hook_rules.py`](#hook_rulespy) 直接 import `.claude/hooks/comment_tag_guard.py`。
- 輸出一行 JSON：`{"ok", "file", "kind", "problems"}`；全過 0，有問題 1。

## hook_rules.py

給其他腳本 import 的模組，另有一個除錯用的命令列。從 `.claude/hooks/comment_tag_guard.py` 載入 hook 模組，匯出 `LOCAL_PATHS`、`TAGS`、`RAW_TAGS`、`NOTE_PREFIXES`、`tagged`、`local_path_problem`；從 `.claude/hooks/attribution_guard.py` 匯出 `BANNED`（Claude 署名樣式）。

- 給誰用：`body.py`（本機絕對路徑樣式）、[`prepare_comment.py`](#prepare_commentpy)（標記、`[codex]`／`[agy]` 原文的註記行、本機路徑樣式），以及 [`merge_pr.py`](#merge_prpy)（merge 前查 PR 標題與本文的署名）。
- 為什麼不另抄一份：送出前的自檢跟 hook 用兩份規則，改一邊另一邊不會跟著變，自檢過了 hook 還是會擋（或反過來）。直接 import，規則只寫在 hook 一處。
- hook 檔不存在或缺上面的名稱時 raise `HookRulesError`，訊息寫明哪個檔；不退回自己的副本。

寫入前的關卡：腳本內部執行的 `gh`、`git` 指令，Claude 的 PreToolUse hook 看不到（hook 只看到 `python3 <腳本>` 這一行），所以腳本要自己 precheck。做法是用每支 hook 自己的入口跑，不 import hook 的函式、也不改 hook：判斷路徑跟 Claude 直接下指令時一樣，之後新增的 Bash hook 自動涵蓋。

```sh
python3 script/workflow/hook_rules.py precheck [--cwd <dir>] -- <argv…>   # 臨時確認某個指令會不會被擋
```

- `bash_hooks(settings=None)`：讀這個 repo 的 `.claude/settings.json`，取 PreToolUse 裡 matcher 用 `re.fullmatch` 對得上 `Bash` 的每個 hook 指令（`Workflow|Bash` 算，`Edit|Write` 不算；matcher 空的算），順序照檔案，不寫死清單。
- `precheck(argv, cwd, *, settings=None, project_dir=None, timeout=60)`：指令字串是 `shlex.join(argv)`，`argv[0]` 取檔名（字面的 `gh`、`git`）。每支 hook 用 shell 執行，`CLAUDE_PROJECT_DIR` 取 `project_dir`，不給沿用環境變數，再沒有用這個 repo 的根目錄；stdin 是 Claude Code 給 hook 的同一種 JSON（`hook_event_name`、`tool_name: "Bash"`、`tool_input.command`、`cwd`）。
  - 放行：stdout 空且結束碼 0，或 `permissionDecision` 是 `allow`。
  - 擋：`deny`、`ask`（腳本裡沒有人可以回答），以及結束碼 2（理由取 stderr）。
  - 錯誤，同樣不放行：其他非 0 結束碼、逾時、stdout 不是 JSON、JSON 裡沒有 `permissionDecision`、settings 讀不到或沒有任何 Bash hook。
  - 回傳 `{"ok", "command", "denied": [{"hook", "decision", "reason"}], "errors": [{"hook", "error"}]}`，`denied` 與 `errors` 都空才 `ok`。
- `guarded_run(argv, cwd, *, bin_env=None, settings=None, project_dir=None)`：先 `precheck`，不 ok 就不執行，回傳 `{"ok": false, "ran": false, "precheck"}`；過了才不經 shell 執行同一個 argv，回傳 `{"ok", "ran": true, "returncode", "stdout", "stderr", "precheck"}`。有給 `bin_env` 且該環境變數有值時執行檔換成它（測試用來換假 `gh`），precheck 仍用字面的 `argv[0]`。
- 命令列輸出一行 precheck 的 JSON；結束碼 ok 0、被擋或錯誤 1、用法錯 2。例如 `precheck -- git push origin main` 會印 `ok: false`，`denied` 含 `guard.py`。

## prepare_comment.py

準備要貼到 issue 的留言檔（標記、註記行、本機路徑替換、切分），並用 hook 的同一套規則自檢。只寫本機檔，不呼叫 `gh`；`gh issue comment` 由子代理依產出順序逐則下。

```sh
python3 script/workflow/prepare_comment.py prepare --out-dir <dir> --workspace <ws> [--max 60000] \
    --item <tag> <來源檔> <標題> [--item <tag> <來源檔> <標題> ...]
python3 script/workflow/prepare_comment.py clean --out-dir <dir>
```

- `tag` 只能是 `claude`、`codex`、`agy`（取自 hook 的 `TAGS`）。先刪掉 `<dir>` 裡舊的 `post_*.md`，再依 `--item` 順序產生 `<dir>/post_<NN>_<tag>.md`，`NN` 兩位數、跨所有項目連號，檔名排序就是貼出順序。
- 每則第一行 `[<tag>] <標題>`，切成多則時標題後加「（k/n）」。`agy`、`codex`（hook 的 `RAW_TAGS`）第二行加註記行「（註：以下是 <來源檔相對 workspace 的路徑> 的原文，未改寫。…）」，有換路徑時同一行寫明；`claude` 不加。
- 本機路徑：`<ws>/` 開頭的換成 workspace 相對路徑；其他符合 `LOCAL_PATHS` 的依腳本裡的替換表換（家目錄 `~/`、Claude scratchpad `<scratchpad>/`、Windows 使用者目錄 `~\`），順序照 `LOCAL_PATHS`，其他字不動。hook 新增了替換表沒涵蓋的樣式就算失敗，不會漏換。
- 切分：每則（含標頭）不超過 `--max` 字元；在行邊界切、優先切在空行；不在 ```` ``` ```` 程式碼區塊中間切，非切不可時該則結尾補關閉、下一則開頭補開啟；單行超長才硬切。
- 自檢：每個產出檔過 `hook_rules.tagged` 與 `hook_rules.local_path_problem(raw_ok=True)`（hook 放行的條件），且替換後不准再有任何本機絕對路徑。
- 輸出一行 JSON：`prepare` 是 `{"ok", "files": [{"path", "tag", "source", "part", "parts", "chars"}], "replaced": [{"source", "from", "to", "count"}], "problems"}`；`clean` 是 `{"ok", "removed"}`。結束碼：成功 0；來源檔讀不到或自檢不過 1；用法錯 2。
- 呼叫端用 `files` 的則數當「預計則數」，跟實際貼出的網址數對照，沒貼齊就報錯。

## pr_target.py

找出已開 PR 的修改目標，並把 worktree 準備好。只呼叫唯讀的 `gh pr view`，git 動作只在本機，不 push。

```sh
python3 script/workflow/pr_target.py <pr> [--repo <主 repo>]
```

- 分支取 PR 的 headRefName；issue 取 PR 本文第一個 `Closes #N`／`Refs #N`（也認 `Refs: #N`、Fixes、Resolves），找不到就報錯。PR 不是 OPEN 也報錯。
- worktree 位置跟 `worktree.py` 相同（`worktree/branch/<分支>`）。先 `git fetch origin`，不存在就從 `origin/<分支>` 建（本機分支已存在就直接掛上），存在就沿用。
- 檢查：worktree 在 PR 分支、沒有未提交或未追蹤的改動、沒有還沒推的 commit；落後 `origin/<分支>` 就 fast-forward，跟遠端分岔就報錯。
- 輸出一行 JSON：成功 `{"ok": true, "pr", "branch", "issue", "repo", "path", "url", "created", "head", "fast_forwarded", "behind_main"}`，失敗 `{"ok": false, "error"}` 並以 1 結束。

## merge_pr.py

等 CI、merge、收尾一次做完：等 CI 全過、確認可 merge 且沒有署名、`gh pr merge --merge`，再 pull 主 repo、移除 worktree 與本機分支、刪這個 PR 的暫存目錄。PR 已經 merge 過時用 `--no-merge`，只做收尾。

```sh
python3 script/workflow/merge_pr.py <pr> [--no-merge] [--repo <主 repo>] [--scratch <scratchpad 根>] [--item <父題>-<no> ...]
```

- 主 repo（`--repo` 不給時同 `worktree.py`，由 git common dir 推）要在 main、沒有未提交的改動（未追蹤檔不算），否則停下報錯，不 stash、不 checkout；要 merge 時這項最先查，不過就不 merge。
- 等 CI：跑同目錄的 [`wait_ci.py`](#wait_cipy) `<pr>`；不是全過（有失敗或逾時）就以 1 結束，不 merge。
- 查 mergeable：`gh pr view <pr> --json mergeable,...`，`UNKNOWN` 時每 5 秒重查，最多 6 次；`CONFLICTING` 就以 1 結束，錯誤寫明要先 rebase。PR 不是 OPEN 也停下（已經 merge 過就提示改用 `--no-merge`）。
- 查署名：PR 標題與本文經 [`hook_rules.py`](#hook_rulespy) 的 `BANNED`（`attribution_guard.py` 的規則）確認沒有 Claude 署名或 session 連結。
- merge：`gh pr merge <pr> -R ycpss91255-research/vendor_kit --merge`，只用 merge，不 squash、不 rebase（照 ruleset）；之後再查一次確認 `state=MERGED` 且有 `mergedAt`。`--no-merge` 時跳過上面三項，直接確認已 merge，沒 merge 就以 1 結束，什麼都不動。
- 主 repo `git pull --ff-only`。
- 用 `worktree.py` 的 remove 移除 `headRefName` 的 worktree 與本機分支；兩者都不存在就跳過（`worktree_skipped`），算成功。worktree 有未提交的改動或分支有沒推的 commit 時照 `worktree.py` 的規則拒絕。
- 有給 `--scratch` 才刪暫存目錄，只刪慣例路徑：`pr-fix/<pr>/`（`pr-fix` workflow），以及每個 `--item` 的 `pr/<父題>-<no>/`（`pr` workflow，`/`、空白、`:` 換成 `_`，同 `pr.js`）。不做萬用刪除；`--item` 格式不對時什麼都不動。
- 輸出一行 JSON：`{"ok", "pr", "branch", "ci", "mergeable", "merge", "merged", "pulled", "worktree_removed", "worktree_skipped", "scratch_removed", "error"}`。`ci` 是 `wait_ci.py` 的 JSON 加上它的結束碼 `code`（`--no-merge` 時 `null`），`mergeable` 是最後查到的值，`merge` 是這次有沒有執行 `gh pr merge`，`pulled` 是 pull 後的 HEAD。成功 0；任何一步失敗 1，失敗的那一步之後都不做。

## verify.py

送 PR 前的全部驗證，在 worktree 根目錄跑。

```sh
python3 script/workflow/verify.py [--root <worktree 根目錄>]
```

- 依序跑：`.github/workflows/docs.yml` 每個 `run:`（原樣用 shell 跑）、每個 `script/*/test` 的 unittest（docs.yml 已跑的不重跑）、`script/repo/check_script_layout.py`、hooks 的守門測試（舊位置 `.claude/hooks/test_guard.py` 還在才跑，不在就標 `skipped`；hooks 的測試由 `.claude/hooks/test` 跑）。
- 每個 `script/*/test` 都要出現在 docs.yml 裡，沒出現的列在 `not_in_ci`，算失敗：新類別的測試 CI 要跑得到。
- 輸出一行 JSON：`{"ok", "root", "steps": [{"source", "cmd", "code", "ok", "output"}], "not_in_ci"}`，`output` 只留最後 40 行。全過 0，有失敗 1，找不到根目錄或 docs.yml 2。

## codex_run.py

呼叫 codex 執行一份 brief，結束碼由腳本直接讀，呼叫端的 shell 是 bash 還是 fish 都一樣。

```sh
python3 script/workflow/codex_run.py --cd <dir> --brief <brief 檔> --out <輸出檔> [--timeout 570] [--delete-brief] [--reuse]
```

- `--reuse`：`--out` 已存在且非空就不執行 codex，回報 `reused=true`、`ok=true`、結束碼 0；有 `--delete-brief` 時照樣刪 brief。
- 執行 `codex exec --skip-git-repo-check -C <dir> -o <out> <brief 全文>`：stdin 固定接 /dev/null（不接 codex 會停在等 stdin），不帶任何 `--sandbox` 旗標；先建 `<out>` 的上層目錄。brief 用 Write 工具寫檔即可，不必用 heredoc。
- `--timeout` 預設 570 秒，前景 Bash 的 600000 毫秒上限內一定回得來；到了就砍掉 codex。`--delete-brief`：結束後刪掉 brief 檔，不論成敗。
- 輸出一行 JSON：`{"ok", "exit", "out", "out_bytes", "timed_out", "elapsed_s", "stderr_tail", "reused", "capacity", "error"}`；`exit` 是 codex 的結束碼（沒跑起來、逾時或沿用是 null），`stderr_tail` 是 codex stderr 的最後 2000 字元，`reused` 表示沿用既有輸出、沒執行 codex，`capacity` 表示 codex 的 stderr 含 `at capacity`（不分大小寫），呼叫端據此決定要不要重試。
- 結束碼：成功（codex 結束碼 0 且輸出檔存在、非空）或沿用 0；codex 結束碼非 0 或跑不起來 1；輸出檔不存在或是空的 2；逾時 3；brief 檔不存在或用法錯 4。
- codex 執行檔可用環境變數 `CODEX_BIN` 換掉（測試用）。

## agy_run.py

執行 agy 做一次調查：選模型、沿用既有輸出、先寫 `.part` 成功才改名、整理 stderr。只在本機跑 agy，不碰 GitHub。

```sh
python3 script/workflow/agy_run.py --cd <dir> --brief <brief 檔> --out <輸出檔> [--err <stderr 檔>] [--model <名>] [--timeout 0]
```

- `--out` 已存在且非空：不執行 agy，回報 `reused=true`。
- 沒給 `--model`：跑 `agy models`，取第一欄符合 `^gemini-[0-9.]+-flash-high$` 的名稱，依版本號取最新；找不到就失敗。
- 執行 `agy --model <M> -p <brief 全文>`（工作目錄＝`--cd`）。stdout 先寫 `<out>.part`，結束碼 0 且非空才改名成 `<out>`；失敗、輸出空、逾時或被中斷都刪掉 `.part`，不會留下被下次沿用的半成品。
- stderr 寫到 `--err`（預設 `<out 去副檔名>.err`），結束時是空的就刪掉。
- `--timeout` 秒數，0（預設）表示不設上限。相對路徑以目前目錄為準，不是 `--cd`。
- 輸出一行 JSON：`{"ok", "exit", "model", "reused", "out", "out_bytes", "timed_out", "err_tail", "error"}`；`err_tail` 是 stderr 最後 20 行。
- 結束碼：成功或沿用 0；agy 結束碼非 0 為 1；輸出空 2；逾時 3；用法錯或 brief 不存在 4；找不到模型 5。

## 測試

測試在 [test/](test/)，用暫存的 git repo、暫存的根目錄與假的 `gh`、`codex`、`agy`（環境變數 `WAIT_CI_GH`、`PR_TARGET_GH`、`MERGE_PR_GH`、`MERGE_PR_WAIT_CI`、`CODEX_BIN`、`AGY_BIN`），不打 GitHub。跑法：

```sh
python3 -m unittest discover -s script/workflow/test
```
