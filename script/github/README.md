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
