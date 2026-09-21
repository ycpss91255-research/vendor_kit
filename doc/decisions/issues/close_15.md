> 對照新設計（GHCR image + `.version` + `.vendor_kit/` 啟動器；見 `dist_distribution_notes.md` 與 #20、#21）盤點舊 issue 後關閉。

新設計下「下一版需要哪個 image」不再需要問引擎：它就是 `.version` 裡即將 merge 的那一行（tag@digest），Renovate PR 或手改都會先出現在 git diff 裡（notes §3 自動提醒、§8 #1、#20）。連網機器對那一行 `docker save`、離線機器 `docker load` 即可（notes §6）；因為鎖 digest，同 tag 重發不會悄悄改變內容。沒有「發布悄悄換 pin」這個路徑了。
