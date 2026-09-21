> 對照新設計（GHCR image + `.version` + `.vendor_kit/` 啟動器；見 `dist_distribution_notes.md` 與 #20、#21）盤點舊 issue 後關閉。

新設計沒有 delivery-set／signals 查詢這個面：出貨清單就是工具 image 內的 `init.toml` 與落地後的 `.<name>/.stamp`（notes §3 出貨規則、§9），外部稽核直接讀 checkout 的 `.version`。舊設計裡需要分類「既有 repo 訊號」的 init path B 也不存在了——init 對已存在的檔一律跳過。「第五個凍結檔 vs 稽核面」的二選一因此沒有對象。
