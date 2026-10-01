# script/git — git 相關工具

檢查 commit 訊息這類 git 本身的東西。

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

## 測試

測試在 [test/test_check_commit_msg.py](test/test_check_commit_msg.py)，跑法：

```sh
python3 -m unittest discover -s script/git/test
```
