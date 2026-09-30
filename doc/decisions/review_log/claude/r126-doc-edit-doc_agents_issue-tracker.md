# r126 審查：doc/agents/issue-tracker.md

## 必改

（無）ask 兩項都做了（第 5–7 行總則、第 52、57 行 Map／Resolve）；沒有違反 #78 Decisions so far；沒碰 01～04 承諾；diff 沒有新增或改動連結。

## 建議

1. 位置：第 53 行 Child ticket、第 54 行 Blocking。問題：sub-issue 或 dependencies 不能用時，退路是「把 child 加進 map 本文的 task list」「在 child 本文最上面寫 `Part of #<map>`／`Blocked by:`」。本文開好後才補這些，就違反第 7 行的總則，`issue_body_guard.py` 也會擋。建議：改成「開 issue 時就寫進本文；開好後才要補的，用留言記」，或另開一輪處理（這一輪 ask 寫明其他條不動）。證據：doc/agents/issue-tracker.md:7、:53、:54。
2. 位置：第 25 行。問題：這行 ask 沒要求改，但舊寫法「定案後回頭更新本文」跟新總則衝突，改了是對的；只是「不是只留在對話裡」加「本文開好後不改」跟第 7 行重複。建議：保留，或縮成「設計決議與定案用留言記錄（見總則）」。證據：doc/agents/issue-tracker.md:7、:25。
3. 位置：第 7 行。問題：總則只說「本文與標題」，沒說標籤、assignee、關閉還是可以用 `gh issue edit`。讀的人可能以為 `gh issue edit` 一律不准，跟第 19、56 行衝突。建議：補一句「標籤、assignee 照常用 `gh issue edit`」。證據：doc/agents/issue-tracker.md:19、:56。
