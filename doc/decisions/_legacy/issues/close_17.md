> 對照新設計（GHCR image + `.version` + `.vendor_kit/` 啟動器；見 `dist_distribution_notes.md` 與 #20、#21）盤點舊 issue 後關閉。

這張圖的主題——supervisor 與 child 兩個程序、recovery record、trap 的時間重疊——在新設計裡結構上不存在（notes §4「升級邏輯在新版 image 內」、§7 第 3 列）。`init` 也只剩一條路徑：已存在就跳過。沒有東西可畫。
