# script/github — 盯 GitHub 的工具

查這個 repo 在 GitHub 上的動靜。只讀：只呼叫 `gh api` 的 GET，不改 GitHub 上任何東西。

## watch_github.sh

[watch_github.sh](watch_github.sh) 盯 `ycpss91255-research/vendor_kit` 的 issue 與 PR，每隔一段時間查一次，有事件就每件印一行：新開的 issue／PR、新留言、被關閉或 merge 的 issue／PR。

跑法（在 repo 根目錄）：

```sh
sh script/github/watch_github.sh [間隔秒數，預設 60] [--once]
```

- 不帶 `--once`：一直跑，有事件就印。
- 帶 `--once`：查到第一批事件就印出來並結束。給 Bash `run_in_background` 用，結束時才通知一次；處理完再用同一行重開，就能一直盯著。這個 repo 不用 Monitor（最長 30 分鐘，見 issue #70），`.claude/hooks/monitor_guard.py` 擋下 Monitor 時就指向這一行。

需要已登入的 `gh`。
