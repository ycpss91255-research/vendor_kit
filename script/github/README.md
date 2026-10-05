# script/github — GitHub 相關工具

盯這個 repo 在 GitHub 上的動靜、檢查 PR 規則，以及開 issue。檢查與唯讀工具，以及經 hook 檢查的寫入工具：會寫入 GitHub 的腳本在每個寫入之前，都經 `script/workflow/hook_rules.py` 的 `guarded_run` 把即將執行的同一個指令交給 `.claude/settings.json` 註冊的 Bash hook 檢查，被擋就不執行。

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
- 一個邏輯目的：每個改動檔照範圍表 [scope.json](scope.json) 對到一個範圍，扣掉附屬檔（測試、README 段、docs.yml 步驟、AGENTS 一句、hook 在 `.claude/settings.json` 的註冊與 `test_settings_hooks.py` 的白名單）後只准一個範圍；表上沒列到的檔算違規，要先補表。
- 規則 B（大題與 sub-issue）只是指引，不檢查。

範圍表只寫在 `scope.json` 一處：本機 hook `.claude/hooks/pr_rules_guard.py`（攔 `gh pr create`）與之後的 CI 都呼叫這支。

跑法（在 repo 根目錄，推薦讓腳本自己取改動檔）：

```sh
python3 script/github/check_pr_rules.py --body-file <本文檔> --git-diff
python3 script/github/check_pr_rules.py --pr <N> --git-diff
```

- `--git-diff [<base>]`：腳本自己跑 `git diff --name-only <base>...HEAD` 取改動檔，`<base>` 預設 `origin/main`。
- `--pr <N>`：本文用 `gh pr view <N>` 取（預設 repo `ycpss91255-research/vendor_kit`，可用 `--repo` 換），取代 `--body-file`。

一定要三點（`<base>...HEAD`）：三點從分支與 main 的分岔點算起，只列分支自己的改動。兩點（`<base>..HEAD` 或 `git diff <base>`）比的是兩端快照，main 在分支開出之後又往前時，main 上別人的改動也會被列進來，誤判成改到多個範圍。用 `--git-diff` 就不用每個呼叫端自己記得三點。

原本自己傳清單的用法照舊可用：

```sh
git diff --name-only origin/main...HEAD | python3 script/github/check_pr_rules.py --body-file <本文檔> --files-from -
```

輸出一行 JSON：`{"ok", "issues", "scopes", "problems"}`；全過結束碼 0，有違規 1。測試：`python3 -m unittest discover -s script/github/test`。

## issue_open.py

[issue_open.py](issue_open.py) 開 issue 並掛成 sub-issue，取代「本文寫檔 → `body.py check` → `gh issue create` → `gh api` 取 id → `POST sub_issues`」逐一下指令。

跑法：

```sh
python3 script/github/issue_open.py create (--title <標題> | --title-file <檔>) --label <標籤> --body-file <檔> [--parent <N>] [--keep-body]
python3 script/github/issue_open.py attach --parent <P> --issue <N>
```

- `create`：
  1. 自檢：有 `--parent` 用 `script/workflow/body.py` 的規則（第一行要是 `Part of #N`、不含本機絕對路徑）；沒有 `--parent` 只查本機絕對路徑。有問題就停，不寫入。
  2. 經 `guarded_run` 跑 `gh issue create -R ycpss91255-research/vendor_kit --title … --label … --body-file <絕對路徑>`，從輸出的網址取編號。
  3. 有 `--parent`：唯讀查 issue 的 database id（`gh api repos/<repo>/issues/<N> --jq .id`，不經 hook），再經 `guarded_run` 跑 `gh api -X POST repos/<repo>/issues/<P>/sub_issues -F sub_issue_id=<id>`。
  - issue 開成功就刪掉本文檔，`--keep-body` 保留；開之前失敗不刪。
- `attach`：只做掛 sub-issue，給 `create` 開了 issue 但掛失敗時重試。

寫入前的 precheck：`gh issue create` 與 `POST sub_issues` 都先用 `.claude/settings.json` 裡每支 Bash hook 檢查同一個指令（例如 `comment_tag_guard.py` 要 `--body-file`、`--label`、本文不准有本機絕對路徑；`attribution_guard.py` 擋 Claude 署名）。任何一支擋下、出錯或逾時都不執行；這支腳本不另抄 hook 的規則。

輸出一行 JSON：`{"ok", "step", "issue", "url", "parent", "attached", "sub_issue_id", "problems", "denied", "error"}`；`step` 是停下或完成的步驟（`check`／`create`／`attach`／`done`），`problems` 是自檢的問題，`denied` 是 hook 擋下的明細。

結束碼：

- 0：成功。
- 1：自檢不過、hook 擋下或 `gh issue create` 失敗，什麼都沒寫。
- 2：用法錯。
- 3：issue 已開但掛 sub-issue 失敗；JSON 帶 issue 編號，用 `attach` 重試，不要再 `create`。

測試：`python3 -m unittest discover -s script/github/test`（假 gh 用環境變數 `ISSUE_OPEN_GH` 換掉，hook 用 repo 真的設定）。

## post_comments.py

[post_comments.py](post_comments.py) 依序把留言檔貼到 issue 或 PR，可選貼完關閉 issue，取代「逐則 `gh issue comment --body-file` → 記網址 → 遇錯停 →（可選）`gh issue close`」逐一下指令。

跑法：

```sh
python3 script/github/post_comments.py --kind issue|pr --number <N> (--body-file <檔> [<檔> …] | --dir <目錄>) [--close] [--delete]
```

- 留言檔：`--body-file` 依給的順序；`--dir` 取目錄裡的 `post_*.md`，依檔名排序。一則都沒有、檔案不存在都算用法錯。
- 先全部 precheck：每一則都先用 `.claude/settings.json` 裡每支 Bash hook 檢查 `gh <kind> comment <N> -R ycpss91255-research/vendor_kit --body-file <絕對路徑>`（例如 `comment_tag_guard.py` 查第一行的 `[claude]`／`[codex]`／`[agy]` 標記與本機絕對路徑，`attribution_guard.py` 擋 Claude 署名）。任何一則被擋就一則都不貼。
- 再依序經 `guarded_run` 貼，從輸出取留言網址；某一則失敗就停，不貼後面的。
- `--close`（只限 `--kind issue`）：全部貼完才經 `guarded_run` 跑 `gh issue close <N> -R <repo>`，不帶 `--comment`。
- `--delete`：全部貼成功後刪掉留言檔。

跟 `script/workflow/prepare_comment.py` 搭配（例如 research 把 agy、codex 原文與 Claude 結論貼到 issue）：

```sh
python3 script/workflow/prepare_comment.py prepare --out-dir <目錄> --workspace <ws> --item <tag> <來源檔> <標題> …
python3 script/github/post_comments.py --kind issue --number <N> --dir <目錄>
python3 script/workflow/prepare_comment.py clean --out-dir <目錄>
```

先留言再關 issue：`python3 script/github/post_comments.py --kind issue --number <N> --body-file <檔> --close`。

輸出一行 JSON：`{"ok", "planned", "urls", "failed_at", "closed", "denied", "error"}`；`planned` 是要貼的留言檔（依貼出順序），`urls` 是已貼出的留言網址，`failed_at` 是失敗那一則的路徑，`denied` 是 hook 擋下的明細（每筆帶 `path`）。

結束碼：

- 0：全部成功。
- 1：precheck 擋下，什麼都沒貼。
- 2：用法錯，什麼都沒貼。
- 3：貼到一半失敗（`urls` 是已貼的，`failed_at` 是失敗那一則），或留言全部貼完但關閉失敗（`failed_at` 是 null，只需重跑關閉）。不要整批重貼。

測試：`python3 -m unittest discover -s script/github/test`（假 gh 用環境變數 `POST_COMMENTS_GH` 換掉，hook 用 repo 真的設定）。

## pr_open.py

[pr_open.py](pr_open.py) 開 PR，取代「本文寫檔 → `body.py check` → `check_pr_rules.py --git-diff` → `gh pr create` → 刪本文」逐一下指令。

跑法：

```sh
python3 script/github/pr_open.py --repo <worktree> --branch <分支> --issue <N> --body-file <檔> (--title <標題> | --title-from-commit) [--base main] [--keep-body]
```

`--repo` 是分支所在的 worktree，git 指令與 hook 都在那裡跑；GitHub 上的 repo 固定是 `ycpss91255-research/vendor_kit`。依序：

1. `push`：worktree 的 HEAD 要等於 `origin/<分支>`（不 fetch，只用已有的 ref）。沒 push 或沒推齊就停，先 push 再跑。
2. `existing`：唯讀查 `gh pr list -R <repo> --head <分支> --state open --json number,url`，這個分支已有 open PR 就停，`existing` 帶那個 PR。
3. `check`：
   - 標題用 `script/git/check_commit_msg.py` 的 `check_title`（`--title-from-commit` 取 HEAD 的 subject）。
   - 本文用 `script/workflow/body.py` 的規則（第一行 `[claude] `、有一行 `Closes #N`、不含本機絕對路徑）。
   - PR 規則用 `check_pr_rules.py` 的 `check`，改動檔取 `git diff --name-only origin/<base>...origin/<分支>`（三點）；沒有改動檔也算問題。
   - 問題原樣放進 `problems`，有任何一條就停，不寫入。
4. `create`：經 `guarded_run` 跑 `gh pr create -R <repo> --base <base> --head <分支> --title … --body-file <絕對路徑>`，從輸出的網址取 PR 編號。成功就刪掉本文檔，`--keep-body` 保留；失敗不刪。

寫入前的 precheck：`gh pr create` 先用 `.claude/settings.json` 裡每支 Bash hook 檢查同一個指令（例如 `pr_rules_guard.py` 用 `--head` 的遠端分支取改動檔再查一次範圍，`comment_tag_guard.py` 查本文的本機絕對路徑，`attribution_guard.py` 擋 Claude 署名）。任何一支擋下、出錯或逾時都不執行；這支腳本不另抄 hook 的規則。

輸出一行 JSON：`{"ok", "step", "pr", "url", "existing", "problems", "denied", "error"}`；`step` 是停下或完成的步驟（`push`／`existing`／`check`／`create`／`done`），`existing` 是已存在的 open PR（`{"number", "url"}`，沒有是 null），`denied` 是 hook 擋下的明細。

結束碼：

- 0：成功。
- 1：沒推齊、已有 PR、檢查不過、hook 擋下或 `gh pr create` 失敗，沒開 PR。
- 2：用法錯。

測試：`python3 -m unittest discover -s script/github/test`（暫存 bare remote 加 clone；假 gh 用環境變數 `PR_OPEN_GH` 換掉，hook 用 repo 真的設定）。
