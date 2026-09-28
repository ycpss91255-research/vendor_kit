> 對照新設計（GHCR image + `.version` + `.vendor_kit/` 啟動器；見 `dist_distribution_notes.md` 與 #20、#21）盤點舊 issue 後關閉。

新設計下 vendor_kit 不再對專案 repo 做任何 commit（notes §3、§4）：`.<name>/` 不進 git，`.version` 由 Renovate PR 或人改，`.vendor_kit/` 由 bootstrap 寫出後由使用者自己提交。沒有引擎產生的 commit，就沒有訊息／作者／trailer 要規定。唯一可能相關的是 `just upgrade` 要不要順手 commit，那屬於 upgrade 待議（notes §8 #5、#20 待辦）。
