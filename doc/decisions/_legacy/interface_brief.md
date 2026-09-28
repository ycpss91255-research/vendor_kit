# 題目：vendor_kit 對使用者的 just 介面 —— (a) init 被 bootstrap.sh 取代會不會有問題？以及安裝／解除安裝要成對

## 背景（乙版架構，已定案）
- vendor_kit 讓「工具 repo」（例如 base）把 dist/ 打包成 GHCR image `<repo>-dist:<tag>`（FROM scratch 只放檔案，amd64+arm64）。
- 下游「專案」（使用者 = 下游專案裡每天打 just 的人）靠 vendor_kit 拿到工具檔案、跟上新版、在本機開發工具本身。
- 引擎 = `vendor_kit:vN` image（容器內程式，子命令 install/init/verify/upgrade/bootstrap）。
- 啟動器 = 專案裡 `.vendor_kit/`（進 git 的薄殼：entry.just、vendor.just、ci/check.sh、baseline/<repo>/；不進 git 的 gen/ 由引擎產生：vendor_kit.just、tools.just、.stamp）。根 justfile 一行 `import '.vendor_kit/entry.just'`。
- `.version`（TOML，`[tools]` 一行一工具 `<repo> = "image:tag@sha256"`，含 vendor_kit 行）是唯一來源；`.version.local` 為 dev 模式覆寫（不進 git）；`.<repo>/` 是 install 寫出的快取（不進 git，使用者不可改）。
- ensure：每次打 just 都跑；印記 ≠ .version → install；verify 失敗 → 重裝（待拍板）。
- init：把工具 init.toml 列的初始檔複製到專案（已存在只 warn 不覆蓋），並把範本副本存進 `.vendor_kit/baseline/<repo>/`（進 git）供 upgrade 三方合併。
- just 命名空間 `just vendor_kit <verb>`（對齊 base 的 layered just entry：`just base init|update|upgrade`、`just docker build`；工具自己的指令由工具的 just 模組提供，vendor_kit 不定義）。
- 使用者的期望（產品方向）：使用者只想知道極少數指令（原話：init、upgrade、dev），其他能自動就自動，真的不行才開指令。
- 平台：Ubuntu/Linux amd64+arm64（含 Jetson）、WSL2 視同 Linux；需要 docker + git + just(≥1.33, release 下載版)。

## 目前草案（討論圖第 1 頁「對外契約」，待拍板）
使用者介面 = bootstrap.sh + 2 個指令：
| 介面 | 做什麼 |
|---|---|
| bootstrap.sh（release 附的一次性腳本） | 問「要接哪個工具、哪個版本」→ 寫 .version、根 justfile 一行、.vendor_kit/ 薄殼 → install + init → 自刪。之後想再接第二個工具：再跑一次 bootstrap.sh（會問並加一行到 .version），或手動加一行 |
| `just vendor_kit upgrade [<repo>]` | 查 GHCR 最新 → 改 .version → install → 三方合併初始檔（git merge-file；衝突留標記、回 2）→ baseline 自動推到新版 |
| `just vendor_kit dev <repo> -p/--path <dir>` | .version.local 指向本機目錄；不帶 -p = 解除 |
ensure 自動：clone 後 .<repo>/ 不存在 → install；.version 被 pull/revert 改了 → install；**.version 有工具但 baseline/<repo>/ 不存在 = 第一次 → 自動 install + init**；vendor_kit 行變了 → 自動換啟動器並 re-exec。

## 使用者的新疑慮（要回答的）
(a1) `init` 被 bootstrap.sh 取代（第一次由 bootstrap.sh 做、之後由 ensure 自動 init）會不會有什麼問題？沒有問題就不要 init。
(a2) `add` 以及任何「安裝」類動作，都應該有對應的「解除安裝」介面；請列一張建議的 just 介面表（動詞、參數、成對關係、什麼時候用、結束狀態），可參考 base 的 `just base init|update|upgrade[--tag]`、`completions install|uninstall`、apt 對齊（update = 只查、upgrade = 套用）、`--option` 收窄不用位置參數承載語意、每層 `--help`。

## 我方先想到的疑點（請查證、補充、反駁）
1. ensure 在「第一次」自動 init 會在不相干的指令（例如 `just docker build`）時把使用者可見的檔案寫進專案；在 CI 更糟：PR 只加了 .version 一行，CI 的 ensure 會生出初始檔與 baseline 但沒 commit，測試結果與 repo 內容不一致。是不是代表「接工具」必須是明確動作（add），ensure 只能碰不進 git 的東西？
2. bootstrap.sh 第二次執行要從哪拿？再 curl 一次 release → 版本可能跟 .version 裡的 vendor_kit 不同；要嘛它偵測到已有 .version 就改用該版引擎跑，要嘛拒絕。
3. bootstrap.sh 是詢問式 → CI／腳本化需要非互動參數（--repo/--tag/--yes）。
4. bootstrap.sh 不在 just 命名空間：沒有 --help、completions、--list 可發現性；base 的原則是「每個動作都是命名空間，沒有頂層特例」。但它第一次跑時 just 入口還不存在，這一步無法避免。
5. 成對：add ↔ remove（刪 .version 行、.<repo>/、baseline/<repo>/；初始檔已是使用者的檔，--purge 才刪且只刪跟 baseline 相同、沒改過的）；dev ↔ undev（base 慣例是成對動詞，不是「不帶 -p 就解除」）；bootstrap ↔ 把 vendor_kit 從專案拔掉（uninstall/remove --self）；upgrade ↔ 回退（git revert 就夠？還是 `upgrade <repo> --tag <舊版>`）；update（只查）↔ upgrade（套用）。
6. `init` 在 base 的語意是「(re-)wire symlinks + .gitignore」（修復），不是「接工具」。vendor_kit 需不需要一個「修復／同步到 .version 狀態」的明確動詞（例如 `just vendor_kit init` 或 `sync`），還是 ensure 完全涵蓋？
7. 指令數 vs 產品方向：使用者原本只要三個；成對之後可能變 6–8 個。哪些可以用「常用／進階」分組（`just vendor_kit` 列表分兩段）而不是砍掉？

## 硬性限制
- Linux amd64+arm64 通用，不綁單一平台機制；工具 image 純資料；引擎只有 .version 那一版。
- 使用者不可改 .<repo>/；.version 是唯一來源；初始檔屬於使用者（工具不碰、只三方合併）。
- 對齊 base 的 just 慣例（命名空間、--option 收窄、update/upgrade apt 語意、--help）。
- 少指令：能自動就自動；但自動化不可以把「使用者可見、要進 git 的檔」在非明確動作時寫出來（這條是我方假設，請一併評估是否成立）。
