# r122 doc-edit 審查：doc/decisions/scope_roadmap.md

範圍：`diff -u doc/decisions/_backup/doc_decisions_scope_roadmap.pre_r122.md doc/decisions/scope_roadmap.md`（3 處改動：第 12、22、36 行）。

## 必改

無。

- 已定案：三處改動與 discussion_queue.md 第 32 條一致（`test` 跑全部、`test dist` 只檢查交付內容、本機與 CI 同一個），沒有碰其他定案條。
- 對外承諾：只改內部決議頁的寫法，01／02 的承諾與 03／04 的介面沒被改動。
- 做完沒：`grep -n "check.sh\|CI 檢查腳本" doc/decisions/scope_roadmap.md` 零命中；原本的 `check.sh`、`check.sh --dist` 都已換成新寫法。
- 連結：diff 裡沒有新增或改動連結。

## 建議

1. 位置：第 10 行「命名空間下的 recipe…」條目。問題：寫「`just vendor_kit add`、`upgrade`、`dev` 是使用者需要知道的全部」，這一輪第 12、22 行把 `just vendor_kit test` 寫成使用者本機也會用的入口，兩條放在一起前後矛盾（第 10 行不在 diff 裡，但被這一輪的改動弄成過時資訊，內部文件不准留過時資訊）。建議：改成「`add`、`upgrade`、`dev`、`test` 是使用者需要知道的全部」，或第 10 行明寫 `test` 另列在 CI 契約那條。證據：scope_roadmap.md 第 10、12 行；discussion_queue.md 第 58 行（第 32 條「本機與 CI 用同一個」）。
