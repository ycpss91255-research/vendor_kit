> 對照新設計（GHCR image + `.version` + `.vendor_kit/` 啟動器；見 `dist_distribution_notes.md` 與 #20、#21）盤點舊 issue 後關閉。

這題列的八個操作屬舊設計（凍結 shell 進入點），多數已不存在。新設計的流程已畫在 `dist_distribution.drawio` 第 3、5、8 頁，並用 ADR-0001 的測試分層與強制閘門（notes §10）把「每個分支要有測試」變成 CI 規則而非文件約定；acceptance 測試對應第 3 頁三條泳道。若新設計某條路徑缺圖或缺測試，請對新頁面重開。
