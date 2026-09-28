> 對照新設計（GHCR image + `.version` + `.vendor_kit/` 啟動器；見 `dist_distribution_notes.md` 與 #20、#21）盤點舊 issue 後關閉。

新設計沒有 exit 8 也沒有回退（notes §4、§7）：install 失敗只是刪掉暫存目錄、`.<name>/` 保持原樣，錯誤印在 stderr，補救一律是再打一次 `just`；verify 失敗的訊息在原型裡已直接寫出要跑什麼（刪掉 `.<name>/` 重跑 `just`，或重跑 bootstrap）。沒有「回退後該重跑哪個命令」這個問題了。
