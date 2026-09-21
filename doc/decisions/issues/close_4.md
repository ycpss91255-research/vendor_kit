> 對照新設計（GHCR image + `.version` + `.vendor_kit/` 啟動器；見 `dist_distribution_notes.md` 與 #20、#21）盤點舊 issue 後關閉。

舊的三張 exit code 表隨凍結 shell 進入點一起廢除（notes §3、§11）：`outdated` 由 Renovate 追 `.version` 取代，delivery-set 查詢不存在，`--help` 不是使用者面。新設計裡 CLI 的結束狀態只有啟動器 `_ensure` 在讀（非 0 就中止），原型 `report.py` 用 0/1/2 已足夠。若日後需要更細的碼，請對新 CLI 重開。
