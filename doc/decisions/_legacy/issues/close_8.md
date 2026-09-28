> 對照新設計（GHCR image + `.version` + `.vendor_kit/` 啟動器；見 `dist_distribution_notes.md` 與 #20、#21）盤點舊 issue 後關閉。

新設計下 `.version` 就是明確讓人（或 Renovate）改的檔，降版只是改回舊值再打 `just`（notes §3、§4），沒有拒絕降版這個分支，兩種補救之爭不存在。verify 也不再是使用者面的報告，而是每個指令前的守門，只比 `.<name>/` 與印記（notes §11）；「verify 到底保證什麼」已改列為 notes §8 #12 待決。
