# r122 doc-edit 審查：doc/adr/0004-vk-recipe-interface-and-write-boundary.md

範圍：`diff -u doc/decisions/_backup/doc_adr_0004-vk-recipe-interface-and-write-boundary.pre_r122.md doc/adr/0004-vk-recipe-interface-and-write-boundary.md`，只改第 21、22 行兩處。

核對結果：
- 已定案：第 32 條要求「薄殼少掉 `ci/check.sh`」「CI 入口 `just vendor_kit test`」「CI 模式照舊由 `CI` 判斷」。第 21 行「薄殼四檔」、第 22 行「`just vendor_kit test` 自己開啟 CI 模式」都符合，與 ADR-0007 第 28 行「薄殼四檔」一致。
- 對外承諾：沒有動 01／02；訊息、結束碼不變。
- 做完沒：全檔 grep `check.sh`、`CI 檢查腳本`、`ci/` 都沒有殘留。
- 連結：diff 裡的連結 `02_invariants.md#6-引擎版本由安裝目錄鎖定啟動器不判斷-repo-內容的意義` 用腳本算 slug 核對過，錨點存在。

## 必改

（無）

## 建議

1. 位置：第 22 行。問題：只寫「`just vendor_kit test` 自己開啟 CI 模式」，沒說 `test dist` 會不會開；ask 的寫法是「`test` 自己開啟 CI 模式」，泛指整個 `test` 指令。建議改成「`test`（含 `test dist`）自己開啟 CI 模式」，或寫成 ask 原句「`test` 自己開啟 CI 模式」。證據：ADR-0004 第 22 行；04_interface.md 第 252–253 行列了兩種用法。
2. 位置：第 22 行。問題：04「## CI 模式」只寫 CI 模式由環境變數 `CI` 判斷，沒提 `test` 會自己開 CI 模式。讀者看了 04 會以為本機跑 `just vendor_kit test` 會照本機行為走。建議在跨檔一致性那一步確認 04 要不要補一句（或在 ADR 寫明做法是 `test` 自己設 `CI=1`，跟 04 的判斷規則對得上）。這件事改名前就存在，不算這一輪造成的。證據：ADR-0004 第 22 行；04_interface.md 第 257–259 行。
