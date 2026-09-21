# 題目：類似專案的對外介面前例，以及「能不能用現成工具取代 vendor_kit」

## 背景（同 interface_brief.md，乙版架構）
- 工具 repo 把 dist/ 打包成 OCI image（FROM scratch 純檔案，amd64+arm64）推 GHCR；下游專案用 `.version`（TOML，一行一工具 `image:tag@sha256`，含引擎自己的版本）宣告。
- 每次打 just，薄啟動器確認 `.<repo>/` 與 .version 一致，不一致就用 docker 把檔案抓下來（不進 git、使用者不可改）。
- 工具帶初始檔（init.toml）：第一次複製給使用者，升級時三方合併（baseline／現在的檔／新版範本）。
- 本機開發模式：`.<repo>/` 改指向本機 checkout。
- 主機只需 docker + git + just；Linux amd64/arm64（含 Jetson）、WSL2；macOS 不在範圍。
- 使用者希望指令極少。上一輪雙軌分析（decisions/interface.md）已建議：不開 init；常用 add/upgrade/dev + 進階 remove/undev/update/ensure/uninstall；ensure 只寫 gitignore 路徑。
- 當初要做 vendor_kit 的原因：base 目前用 git subtree 進下游，base 迭代與下游綁死、base 自己升級要改下游。

## 要回答的問題
(B) 有沒有現成工具（或兩個工具 + 少量膠水）能直接取代 vendor_kit，讓我們不用自己寫 repo？請逐一對「拉 OCI 純檔案 image 展開到目錄／lock 檔鎖 digest／使用者初始檔三方合併／本機路徑覆寫／主機只需 docker+git+just／arm64」六項打勾，並評估「把現成工具放進引擎容器內用（例如引擎 image 內含 vendir 或 copier，主機仍只需 docker）」這種折衷，能省掉我們多少自寫程式、會多綁什麼。
(C) 前例的動詞命名對我們介面表的影響：前例壓倒性用 `update` = 套用新版（Copier/Cruft/Nix/Helm dependency/git-vendor），而 base 用 apt 語意（update = 只查、upgrade = 套用）。vendor_kit 要跟 base（下游同時會用 `just base …`，一致性）還是跟生態系多數？只查不套用叫 check／diff／--dry-run／outdated 哪個？link↔unlink 是否比 dev↔undev 更通用？
(D) agy 的哪些說法站不住腳（子代理已列 12 條疑點，請查證關鍵的：Copier 是否真的沒有 OCI 來源；vendir 是否真的無三方合併；vendir/imgpkg 在 arm64 的 release；Renovate 對 vendir/devcontainer/mise 的支援是否為原生 manager）。
