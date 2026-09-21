> 對照新設計（GHCR image + `.version` + `.vendor_kit/` 啟動器；見 `dist_distribution_notes.md` 與 #20、#21）盤點舊 issue 後關閉。

新設計裡「這個 repo 用哪個引擎／哪個版本」的答案就是 `.version`（notes §8 #1、§9、#20）：`vendor_kit = "…:vN@sha256:…"` 一行鎖啟動器版本，每個工具一行鎖其 dist image；`.<name>/.stamp` 第一行抄同一字串。從 checkout 直接讀檔即可，不需 daemon、不需 `--version`，稽核與 `docker save` 都拿這一行。
