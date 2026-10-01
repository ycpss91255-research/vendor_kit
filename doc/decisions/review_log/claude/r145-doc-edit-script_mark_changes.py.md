# r145 審查：script/mark_changes.py

範圍：`git diff HEAD -- script/mark_changes.py`（備份 pre_r145 不存在）。

## 必改

無。ask 第 1 點三處（第 4、448、521 行）都改了；第 57、65 行的「不進 git」也一併改成現況。檔內已沒有「名詞標記」「不進 git」「<ins>」字樣（grep 驗證）。不碰 01／02／03／04 的對外介面；map #78 的定案裡沒有跟 _marked 或底線有關的條目（grep 驗證）；diff 沒有新增連結。test_mark_changes 通過。

## 建議

無。
