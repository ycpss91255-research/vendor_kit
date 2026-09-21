> 對照新設計（GHCR image + `.version` + `.vendor_kit/` 啟動器；見 `dist_distribution_notes.md` 與 #20、#21）盤點舊 issue 後關閉。

新設計（notes §11、#20）下使用者只接觸 `just` recipe，`just --list` 與 recipe 註解就是操作者看到的說明；凍結 shell 進入點與其 `--help` 已整個廢除。vendor_kit 本身的 CLI 只由 `.vendor_kit/vendor.just` 在容器內呼叫，不是使用者面，所以「引擎要不要自我說明」已無對象。若日後要為 just 指令表另寫 README，請對新設計重開。
