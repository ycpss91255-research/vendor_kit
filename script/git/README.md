# script/git — git 相關工具

檢查 commit 訊息這類 git 本身的東西、呼叫它的本機 hook（`.githooks/`），以及 commit、push 的包裝。

## check_commit_msg.py

[check_commit_msg.py](check_commit_msg.py) 檢查 commit 訊息格式，規格是 vendor_kit#110 的「維護者決議與定案」：

1. 標題 `<type>(<scope>)[!]: <繁中描述>`；type 九種 `feat fix docs refactor test perf build ci chore`；scope 只准用 `SCOPES` 常數列的，可省略；句尾不加標點。
2. 標題顯示寬度（中文算 2 欄）上限 72，超過 50 只提示。
3. 標題跟內文之間空一行；footer 放最後一段，只認 `Refs: #N`、`Closes #N`、`BREAKING CHANGE: …`、`Doc-Edit: rNN`；標題有 `!` 就要有 `BREAKING CHANGE:`，反之亦然。
4. 不准有 Claude 署名或 session 連結。這組 pattern 直接從 `.claude/hooks/attribution_guard.py` 的 `BANNED` 載入，不另抄一份；hook 檔不在或缺 `BANNED` 時直接報錯，不退回副本。
5. 豁免 `Revert "…"` 與 git merge 的預設標題；把 main 併進分支的 merge commit 要擋，改用 rebase。

新增 scope 要開 PR 改 `SCOPES`，跟一般 PR 一起審。

跑法（在 repo 根目錄）：

```sh
python3 script/git/check_commit_msg.py <訊息檔>      # commit-msg hook 用；會去掉 # 註解行
python3 script/git/check_commit_msg.py -             # 從 stdin 讀整則訊息
python3 script/git/check_commit_msg.py --title -     # 只檢查一行標題（PR 標題）
python3 script/git/check_commit_msg.py --range A..B  # 逐一檢查 A..B 的每個 commit
```

全部合格回 0；有不合格逐條印出回 1；用法錯誤或 `--range` 給錯回 2。

## 本機 commit-msg hook

[.githooks/commit-msg](../../.githooks/commit-msg) 在每次 commit 時呼叫 `check_commit_msg.py` 檢查訊息，不合格就擋下這次 commit。git 不會自動啟用 repo 裡的 hook，clone 之後要在 repo 根目錄設一次：

```sh
git config core.hooksPath .githooks
```

這是本機設定，每份 clone 設一次；同一份 clone 開出的 worktree 共用這個設定。CI 另外檢查 PR 標題與 PR 內每個 commit，沒設 hook 也擋得到，只是比較晚才發現。

## commit_push.py

[commit_push.py](commit_push.py) 檢查 commit 訊息後 commit，並 push 到自己的分支，取代 pr、pr-fix workflow 裡照文字做的「寫訊息檔 → `git commit -F` → `git push -u`」：

1. 檢查 `--repo` 是 git worktree 的根目錄、目前分支等於 `--branch`、`--branch` 不是 main、有改動。
2. `--message-file` 只寫標題（可加空行與內文），不含 footer。腳本在最後空一行加 `Refs: #<refs>`（已經有同一行就不重複加），寫到同目錄的 `<檔名>.final`，再用 `check_commit_msg.check_message` 檢查；有錯誤就停、不 stage。
3. stage `--add` 給的路徑，或 `--all`（`git add -A`）。
4. commit 與 push 都經 `script/workflow/hook_rules.py` 的 `guarded_run`：把即將執行的同一個 argv 交給 `.claude/settings.json` 註冊的 Bash hook，被擋就不執行。`--no-push` 時只 commit。

跑法：

```sh
python3 script/git/commit_push.py --repo <worktree> --branch <分支> --message-file <檔> --refs <issue> (--add <路徑>… | --all) [--no-push]
```

輸出一行 JSON：`{"ok", "step", "branch", "commit", "files", "pushed", "problems", "denied", "error"}`。`step` 成功時是 `done`，失敗時是停下的那一步（usage、repo、message、stage、commit、push）；`files` 是這個 commit 的檔案清單；`problems` 是訊息檢查的錯誤；`denied` 是擋下的 hook。結束碼：成功 0；檢查、hook 或 git 失敗 1；用法錯 2。

## 測試

測試在 [test/test_check_commit_msg.py](test/test_check_commit_msg.py)（檢查器）、[test/test_commit_msg_hook.py](test/test_commit_msg_hook.py)（用暫存 git repo 設 `core.hooksPath` 實際跑 hook）與 [test/test_commit_push.py](test/test_commit_push.py)（暫存 git repo 加暫存 bare remote，經真的 Bash hook commit、push），跑法：

```sh
python3 -m unittest discover -s script/git/test
```
