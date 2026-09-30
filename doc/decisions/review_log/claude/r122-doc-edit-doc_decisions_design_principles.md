# r122 doc-edit 審查：doc/decisions/design_principles.md

範圍：`diff -u doc/decisions/_backup/doc_decisions_design_principles.pre_r122.md doc/decisions/design_principles.md`，只有第 32 行（P5）一處改動。

核對結果：
1. 已定案：改動照 discussion_queue.md 定案第 32 條（第 58 行），沒有違反其他條。
2. 對外承諾：這一頁是內部設計原則頁，改動沒碰 01／02／03／04。
3. 做完沒：`grep -n "check.sh\|CI 檢查腳本\|--dist\|ci/"` 在本檔沒有結果，唯一出現的 `check.sh`（P5）已經換掉。
4. 連結：diff 沒有新增或改動連結（第 33 行的兩個 ADR 連結沒動）。

## 必改

（無）

## 建議

### 1. P5 列舉把「命令」跟「實作層」混在一起
- 位置：doc/decisions/design_principles.md 第 32 行（### P5. 一條規則一個擁有者）
- 問題：原句列的三項都是「只轉發的實作物」：啟動器、`check.sh`（薄殼裡的腳本）、工具 just 模組。現在 `check.sh` 不存在了，換上的 `just vendor_kit test` 是使用者打的命令，本身不是一層實作；實際負責轉發的是薄殼的 `entry.just`／`vendor.just` 加上啟動器，而啟動器已經在清單裡。這樣列會讓讀者以為 `test` 是另一個要跟引擎保持一致的實作，跟 P5「兩個實作會漂移」的論點不合。
- 建議：改成「規則在引擎實作一次；啟動器、`just vendor_kit` 的各個指令（含 `test`）、工具 just 模組只轉發。」，或乾脆拿掉這一項，只留「啟動器、工具 just 模組只轉發」（`test` 走啟動器，已經涵蓋）。
- 證據：design_principles.md 第 32 行；discussion_queue.md 第 58 行（薄殼少掉 `ci/check.sh`）；GLOSSARY.md 第 33–34 行（啟動器＝薄殼內的 POSIX sh 片段與 `bootstrap.sh`）。
