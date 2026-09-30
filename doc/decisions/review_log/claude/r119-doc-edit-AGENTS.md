# r119 doc-edit 審查：AGENTS.md

## 必改

（無）

- 已定案：新增條與定案「repo 一律用 doc/」一致，沒有違反 discussion_queue.md 已定案區。
- 對外承諾：只動內部文件 AGENTS.md，沒碰 01～04。
- 做完沒：AGENTS.md 第 18 行逐字等於 ask，位置緊接在「對外契約放 `doc/contract/`」那條後；diff 只有這一行新增。
- 連結：`script/check_terms.py` 存在（沒有 #錨點）；第 9、113–118 行確實在根目錄有 `docs/` 時失敗，跟新增條「根目錄出現 `docs/` 時會擋下來」相符。

## 建議

- 位置：AGENTS.md 第 18 行。問題：只寫了 `docs/adr/`、`docs/agents/`「等」。`.agents/skills/` 的 `docs/` 路徑只有這兩種（docs/adr 17 處、docs/agents 12 處，`grep -rhoE "docs/[a-z_-]+" .agents/skills`），而且 `doc/adr/`、`doc/agents/` 都已存在，所以這樣寫夠了。不用改。
