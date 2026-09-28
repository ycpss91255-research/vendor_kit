> 對照新設計（GHCR image + `.version` + `.vendor_kit/` 啟動器；見 `dist_distribution_notes.md` 與 #20、#21）盤點舊 issue 後關閉。

這題的前提——凍結面只有 bash 與 git、不能安全輸出 JSON——在新設計下不成立：vendor_kit 以 Python 在容器內執行（notes §3 角色表），原本的解除條件等於已達成。同時 `--json`／`--porcelain` 兩個旗標也隨舊進入點廢除，目前啟動器只讀結束狀態與 `.stamp`，沒有機器可讀輸出的消費者。若日後 Renovate PR 或 CI 需要結構化輸出，請對新 CLI 重開。
