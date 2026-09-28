# 題目：契約剩餘五題（每題要獨立裁定並給理由）

## 已定案背景（以 grilling.md 為準）
自寫 + docker + git merge-file；動詞 install/uninstall、add/remove、update/upgrade、dev/undev、sync；不變量「使用者的檔：可以建（明說建了什麼）、要改先問（-y 免問）、永不刪、永不覆蓋」；全收進 `.vendor_kit/`（version.toml、version.local.toml、cache/<repo>/、自有 .gitignore）；初始檔 add 建立、已存在不納管、upgrade 逐檔判斷後詢問（-y 免問）、衝突留標記回 2 且 baseline 推到新版；工具 image 與引擎 image 多架構 amd64+arm64（index digest）；平台 Linux amd64/arm64（Jetson、RPi 64）、WSL2；docker ≥ 19.03；dev 自身 = `.version.local` 指本機 image tag；驗收 = 乾淨 fixture repo 跑完整流程。Renovate 用 custom regex manager 追 `.vendor_kit/version.toml`（docker datasource、currentValue+currentDigest）。

## Q5 Renovate 開的 PR 誰補初始檔合併
Renovate 只改 version.toml 一行；之後初始檔三方合併與 baseline 推進沒人做，CI 的 sync（frozen）會判「baseline 落後」讓 PR 紅。
(1) PR 作者本機 `upgrade <repo> -y` 補合併、commit、push（Renovate 要設定不 rebase 掉人的 commit）。(2) CI 以 bot 身分跑 `upgrade -y` 並 commit 回 PR 分支（GitHub/GitLab 各養一套 bot 推權限；ci_bridge #25 未定）。(3) 只鎖版本不管初始檔，等下次人工 upgrade（version.toml 與 baseline 長期不一致）。(4) 其他：例如 Renovate `postUpgradeTasks` 直接在 Renovate 端跑 upgrade（需 self-hosted Renovate + allowedCommands）。
我方傾向 (1)。請查證：Renovate 對人推 commit 的處理（rebaseWhen、`stopUpdating` label、`ignore` 之類）；GitHub/GitLab 上 (2) 的實際需求；(4) 是否只在 self-hosted 可用。

## Q6 幾乎一定已存在的初始檔（.gitignore、.dockerignore、.editorconfig）
工具（base）想把自己的 ignore 條目送進下游，但 add 時這些檔幾乎都已存在 → 依不變量「已存在不納管」，條目永遠進不去。
(a) 只 warn，工具作者改用不需要碰這些檔的設計（例如 base 的 ignore 需求改由 `.vendor_kit/.gitignore` 或 base 自己的子目錄 .gitignore 解決）。(b) 第四種初始檔模式「標記區塊 append」：`# >>> vendor_kit:<repo> >>>` … `# <<< vendor_kit:<repo> <<<`，add 時詢問後 append、upgrade 只替換區塊內容、remove 詢問後刪區塊（conda init / nvm 的做法）。(c) 工具在 init.toml 宣告 `mode = "append"` 才允許 (b)，預設 (a)。
我方傾向 (c)。請查證 conda init／nvm／oh-my-zsh 標記區塊做法的口碑與問題（使用者反感點：改 rc 檔、區塊被手改後失效、重複區塊）。

## Q7 image 公開／私有
GHCR 上工具 image 與引擎 image 公開還是私有？影響：私有時主機要 `docker login`（credential helper）；GitLab CI 拉 GHCR 私有 image 要 bot PAT；bootstrap.sh 第一次拉引擎前要先 login。
(a) 一律公開（org 是研究用 public repo）。(b) 一律私有。(c) 引擎公開、工具由各工具 repo 自己決定；vendor_kit 契約只保證「主機 docker 能 pull 就能用」，認證是主機的事。
我方傾向 (c)。

## Q8 just 最低版本
proto ADR-0002 定 ≥ 1.33。我們用到：`mod`/`mod?`（1.19+ 穩定於 1.31？）、`import?`、`[group]`（1.27）、`set positional-arguments`、`justfile_directory()`、`[no-cd]`、`--list-submodules`、`set allow-duplicate-recipes`。請查證每個功能的最低版本（just 的 changelog/手冊），並考慮 Ubuntu 22.04/24.04 apt 的 just 版本（我們用 release 下載版，但要知道差距）。建議一個下限並說明；CI 要用該版本重跑全部 just 實測（isolation 題已要求）。

## Q9 vendor_kit 自身升級後：停下要求重跑 vs 自動 re-exec
啟動器發現 version.toml 第一行的引擎 ≠ gen/.stamp → 用新引擎重寫薄殼與 gen/ → 然後？(1) 印「已更新 vendor_kit，請重跑」回 1（interface.md 建議：子程序無法替換父程序、just 已載入舊 recipe）。(2) 啟動器 `exec just <原參數>` 重跑一次（風險：無限迴圈需 guard、just 的 argv 還原、環境變數）。
我方傾向 (1)。請評估 (2) 是否真的做不到或不值得。

## 輸出要求
每題：裁定｜理由｜若與我方傾向不同請明說｜實作時的必要條件。recommendation 放五題的表。
