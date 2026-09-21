> 對照新設計（GHCR image + `.version` + `.vendor_kit/` 啟動器；見 `dist_distribution_notes.md` 與 #20、#21）盤點舊 issue 後關閉。

新設計沒有 rollback 機制、也沒有 recovery record 或使用者檔快照（notes §4、§7）：install 只把 dist 寫進 repo 內的暫存目錄再改名，失敗就刪暫存，使用者檔案永不被 install/upgrade 動到，回退就是把 `.version` 改回去。所以目錄、命名、`tmpfs`、record 格式這些問題都沒有對象了。兩個 run 同時跑的殘留問題已收進 notes §8 #13（並行安裝的 lock）。
