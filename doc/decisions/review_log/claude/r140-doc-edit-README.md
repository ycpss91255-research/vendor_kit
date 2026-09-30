# r140 doc-edit 審查：README.md

範圍：`doc/decisions/_backup/README.pre_r140.md` 不存在（這一輪的備份只有 01～04、GLOSSARY、script 那幾個檔）；`git diff HEAD -- README.md` 是空的，`git status` 也沒有列 README.md。README 這一輪沒改。

核對過：
- 做完沒：ask 1 要對 README 跑 --fix。改過的 `script/check_typography.py README.md` 回 `OK: 檢查 1 個檔`（rc=0）。另外用腳本逐一找成對的反引號區段，檢查前後是不是直接貼著漢字，README 一處都沒有。所以不改是對的，不算漏做。ask 2 只動 04，跟 README 無關。
- 已定案（map #78）、對外承諾、連結：README 沒有 diff，沒有新增或改動的連結，這三項都沒有東西要審。

## 必改

無。

## 建議

無。
