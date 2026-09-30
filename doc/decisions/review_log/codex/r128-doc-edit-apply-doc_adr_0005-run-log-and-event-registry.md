已完成，未 commit、未 push，也未執行任何 git 寫入指令。備份已建立為 `.pre_r128.2.md`，原 `.pre_r128.md` 保留不動。

- 已改：Considered Options 第 9 行；移除「警告會被吞掉」，改為說明無法提供符合不變量 4 的對象與下一步，且未知事件名會破壞讀取端。
- 已改：內部機制第 21 行；移除 FATAL，改為實作錯誤立即停止並以 error、結束碼 `2` 結束。

三支驗證腳本均通過：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK