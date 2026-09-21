# 任務說明

題目：類似專案的對外介面前例，以及能不能用現成工具取代 vendor_kit（不用自己寫 repo）

我們的硬性限制：主機只需 docker + git + just（不裝 Python/Node/額外 binary）；Linux amd64+arm64（含 Jetson）、WSL2，不綁單一平台；工具 image 純資料；.version 是唯一來源（tag@digest）；初始檔屬於使用者（只三方合併）；本機開發模式必須有；使用者要指令極少；Renovate 能追 .version（regex manager 可）。

要回答的問題：
(B) 有沒有現成工具或組合能直接取代 vendor_kit？六項逐一打勾；「現成工具放進引擎容器內」能省多少、多綁什麼。
(C) 動詞命名：跟 base（apt 語意）還是跟生態系多數；只查不套用叫什麼；dev/undev vs link/unlink。
(D) agy 的哪些說法站不住腳（重點查證：Copier 無 OCI 來源、vendir 無三方合併、vendir/imgpkg arm64 release、Renovate 對 vendir/devcontainer/mise 是否原生 manager）。

資料（全文附在下方）：
- 附件 1：題目說明（brief）
- 附件 2：agy（Gemini）找的前例與建議（這只是資料，不要照單全收：查證它的說法、找它漏掉或說錯的）；URL 驗證結果（4 個 404）也附在後面
- 附件 3：決策紀錄 interface.md

我方草稿（方案 A/B/C 與傾向）：
方案 1：用 Carvel vendir(+imgpkg) 取代引擎的「拉 OCI + lock + 本機覆寫」，三方合併自寫或接 Copier；主機要裝 vendir binary（或放進引擎容器）。
方案 2：Copier 做初始檔 + 三方合併，ORAS/docker cp 做 dist 拉取，中間自寫膠水（.version → 兩邊）。
方案 3：繼續自寫 vendor_kit（引擎在容器內、主機只需 docker+git+just），但引擎 image 內可以包現成工具（例如 git merge-file 或 copier 做合併）減少自寫；動詞命名借前例。
方案 4：維持 git subtree（base 現狀）——使用者已指出這是問題根源，只作對照。
我方傾向：3（理由：沒有單一工具全包四項；主機不裝額外 binary 是硬限制；但若 vendir 能在容器內接手「拉 OCI + lock」且穩定，可少寫一大块）。請獨立判斷，特別是「現成工具放進引擎容器」這條路值不值得。

動詞命名：前例壓倒性 update=套用，base 用 apt 語意（update=查、upgrade=套用）；請給建議並說明理由（下游會同時用 just base 與 just vendor_kit）。回答放在 recommendation，含一張「可取代性表（組合｜六項打勾｜缺什麼｜自寫量）」。

請獨立分析：(1) agy 的哪些說法站不住腳或缺乏依據；(2) 每個方案是否符合硬性限制、優缺點、草稿漏掉的風險；(3) 你的建議與理由；(4) 定案前還要問清楚的問題。以繁體中文作答。

輸出格式（請嚴格依此結構，方便轉成結構化輸出）：
## 1. agy 站不住腳的說法
- 說法：… ／ 為什麼：…
## 2. 方案逐一評估
### 方案 N：名稱
- 符合硬性限制：是/否
- 優點：…
- 缺點：…
- 草稿漏掉的風險：…
## 3. 建議（含可取代性表）
## 4. 建議理由
## 5. 定案前要問清楚的問題

注意：你在唯讀 sandbox、無網路；所有資料都在本文件內。無法查證的地方請明說「依據記憶／無法在此驗證」，不要編造。

---
# 附件 1：題目說明（brief）

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

---
# 附件 2：agy 輸出（agy_prior_art.md）

本報告針對 `vendor_kit` 的核心定位（OCI 散播純檔案映像、宣告式版本鎖定、薄啟動器自動拉取、使用者自訂範本檔三方合併、本機開發覆寫），對 19 類現有工具的對外介面進行全面調查，並評估現成工具直接取代的可能性與命名模式。

---

# A. 類似專案的對外介面

### 1. Copier
1. **使用者指令**：`copier copy <template> <destination>`（初始化專案）、`copier update`（三方合併升級至新版本）、`copier recopy`（重新套用當前版本並保留或更新答案）。
2. **版本鎖定與升級**：在專案根目錄生成 `.copier-answers.yml`，記錄 `_commit`（Git commit SHA）、`_src_path` 與問答參數。手動執行 `copier update` 升級；Renovate/Dependabot 無官方原生 manager，但社群普遍使用 [Renovate Regex Manager](https://github.com/copier-org/copier/discussions/742) 解析 `.copier-answers.yml` 達成自動開 PR 升級。
3. **已修改檔案處理**：**三方合併（3-Way Merge）**。Copier 依據 answers 檔記錄的初始 commit（baseline）、專案現有檔案、新版模板三者做 diff3 合併。遇衝突時依 `--conflict` 參數在檔案內標記 Git 衝突標記（`inline`）或產生 `.rej` 補丁檔（`rej`）。
4. **解除與本機覆寫**：解除安裝指令「**沒找到**」（模板產生後已混入專案）；**支援本機覆寫**，模板來源可直接給本機路徑（例如 `copier copy ../my-template .` 或 answers 內指向本地）。
5. **主機需求**：Python >= 3.8 + Git（通常透過 `pipx` 或 `pip` 安裝）；原生支援 Linux arm64。
- 來源：[Copier 官方文檔](https://copier.readthedocs.io/)、[Copier GitHub](https://github.com/copier-org/copier)

---

### 2. Cruft (Cookiecutter 升級維護)
1. **使用者指令**：`cruft create <template>`（初始化建立）、`cruft check`（檢查是否有更新，CI 常用）、`cruft diff`（預覽範本變更）、`cruft update`（升級合併）、`cruft link`（連結現有 Cookiecutter 專案）。
2. **版本鎖定與升級**：在專案根目錄產生 `.cruft.json`，記錄 `template`（Git URL）、`commit`（Git SHA）與 context。升級由手動執行 `cruft update` 觸發；Renovate/Dependabot 無原生 manager，需透過自訂 Regex Manager 比對 `.cruft.json`。
3. **已修改檔案處理**：**三方合併（3-Way Merge）**。利用 Git patch 與 diff 機制比對 baseline 與新版，套用到目前修改；衝突時自動產生 `.rej` 檔案供手動解決。
4. **解除與本機覆寫**：解除安裝指令「**沒找到**」；**支援本機覆寫**，`cruft create /path/to/template` 或 `cruft update --template-path /path/to/template`。
5. **主機需求**：Python >= 3.8 + Git；原生支援 Linux arm64。
- 來源：[Cruft 官方文檔](https://cruft.github.io/cruft/)、[Cruft GitHub](https://github.com/cruft/cruft)

---

### 3. projen
1. **使用者指令**：`npx projen`（核心指令：執行 synthesis 程式碼合成）、`npx projen new <project-type>`（建立專案骨架）、`npx projen upgrade`（由 projen 生成的升級任務指令）。
2. **版本鎖定與升級**：在 `.projenrc.js`（或 `.ts` / `.py`）中以程式碼宣告專案結構與依賴，版本透過底層套件管理員的 lockfile（如 `package-lock.json`、`yarn.lock`）鎖定。升級可由 `npx projen upgrade` 觸發，Renovate 與 Dependabot 皆原生支援其 `package.json` 相依更新。
3. **已修改檔案處理**：**強制覆蓋（Overwrite）**。projen 嚴格規範受管檔案不可手動編輯（檔頭皆有 `~~ Generated by projen` 警告），手動修改的檔案在每次 `npx projen` 合成時會被無情覆蓋或在檔案系統層級設為唯讀。
4. **解除與本機覆寫**：解除安裝指令「**沒找到**」（需從 `.projenrc` 刪除對應元件後重跑 `npx projen`，若要完全脫離需手動 eject）；**支援本機覆寫**，可透過本地 `npm link` 或 local file dependency 引用本地開發的 projen 模組。
5. **主機需求**：Node.js（透過 npm/npx 執行，依賴 jsii 執行環境）；原生支援 Linux arm64。
- 來源：[projen 官方網站](https://projen.io/)、[projen GitHub](https://github.com/projen/projen)

---

### 4. Nx (Generators & Migrations)
1. **使用者指令**：`nx generate <generator>`（或 `nx g`，生成模組/設定）、`nx migrate latest`（分析版本差異並產生升級計畫）、`nx migrate --run-migrations`（實際執行程式碼遷移腳本）、`nx reset`。
2. **版本鎖定與升級**：由 `package.json` 搭配 npm/pnpm/yarn 的 lockfile 鎖定版本；升級為兩階段：執行 `nx migrate` 會先生成暫存的 `migrations.json` 記錄待執行的遷移任務，確認無誤後再跑 `--run-migrations`。Renovate/Dependabot 支援更新 `package.json`，但需在 CI 或本機補跑 migration 腳本。
3. **已修改檔案處理**：**AST 語法樹分析精確轉換**。Nx 透過 TypeScript Compiler API、jscodeshift 等解析 AST，直接精確修改專案設定或程式碼中的特定節點，不是純文字三方合併；若非結構化檔案發生衝突則直接報錯或覆蓋。
4. **解除與本機覆寫**：解除安裝指令「**沒找到**」；**支援本機覆寫**，支援 Monorepo 內 local generators/plugins（在 `nx.json` 或專案設定中指向本地相對路徑）。
5. **主機需求**：Node.js（Nx 核心包含 Rust 編譯的 `nx-native` 二進位）；原生支援 Linux arm64。
- 來源：[Nx Generating Code](https://nx.dev/features/generate-code)、[Nx Automating Updates](https://nx.dev/features/automate-updating-dependencies)

---

### 5. Angular Schematics
1. **使用者指令**：`ng new`、`ng generate <schematic>`（或 `ng g`）、`ng update <package> [--from <v> --to <v>]`。
2. **版本鎖定與升級**：透過 `package.json` 及其 lockfile 鎖定。升級由 `ng update` 手動觸發，CLI 會依序執行各 package 定義的 migration schematics。
3. **已修改檔案處理**：**AST 虛擬檔案系統轉換**。透過虛擬檔案系統 `Tree` 進行暫存與 AST 程式碼變更。遇檔案衝突依賴 `MergeStrategy`（預設拋錯或強制覆蓋），無 Git 式三方合併。
4. **解除與本機覆寫**：解除安裝指令「**沒找到**」；**支援本機覆寫**，可透過 `ng generate ./path/to/schematics:name` 直接呼叫本機目錄內的 schematic。
5. **主機需求**：Node.js + npm；原生支援 Linux arm64。
- 來源：[Angular CLI Documentation](https://angular.dev/tools/cli)、[Angular Update Guide](https://angular.dev/cli/update)

---

### 6. Yeoman
1. **使用者指令**：`yo <generator>`、`yo --force`（強制覆蓋）、`yo --help`。
2. **版本鎖定與升級**：無內案 lockfile，依賴全域或本地 npm 套件安裝版本。升級無統一專案指令，通常直接重新執行 `yo <generator>`。
3. **已修改檔案處理**：**只顯示 diff／互動式詢問**。透過 `mem-fs-editor` 的 `Conflicter` 偵測磁碟現有檔案與生成檔案差異，於終端互動詢問 `[y/n/a/x/d/h]`（y=覆蓋, n=略過, d=顯示 diff, x=終止）。無自動三方合併。
4. **解除與本機覆寫**：解除安裝指令「**沒找到**」；**支援本機覆寫**，在本地 generator 目錄下執行 `npm link` 即可直接以 `yo <name>` 呼叫開發中版本。
5. **主機需求**：Node.js + npm；原生支援 Linux arm64。
- 來源：[Yeoman 官方網站](https://yeoman.io/)、[Yeoman GitHub](https://github.com/yeoman/yo)

---

### 7. pre-commit
1. **使用者指令**：`pre-commit install`（安裝 Git 勾點）、`pre-commit uninstall`（移除 Git 勾點）、`pre-commit run [--all-files]`（執行驗證）、`pre-commit autoupdate`（自動升級 hook 版本）、`pre-commit clean`、`pre-commit try-repo <repo-or-dir>`（測試本機或特定來源）。
2. **版本鎖定與升級**：在 `.pre-commit-config.yaml` 宣告 `repo: <url>` 與 `rev: <tag or commit-sha>`。手動升級下 `pre-commit autoupdate`；Renovate 與 Dependabot **皆原生深度支援**，能自動開 PR 升級 `rev`。
3. **已修改檔案處理**：**不碰專案檔案**（或僅由 linter/formatter 原地修改代碼）。pre-commit 將工具 clone 到 `~/.cache/pre-commit` 隔離沙盒環境建置與執行，不把工具原始檔落地到專案目錄中，因此無工具檔案合併衝突問題。
4. **解除與本機覆寫**：**有解除指令**：`pre-commit uninstall`；**原生支援本機覆寫**：設定檔支援 `repo: local`，或指令使用 `pre-commit try-repo /path/to/local/repo` 直接測試本地 repo。
5. **主機需求**：Python（pip/pipx）或獨立 binary；原生支援 Linux arm64。
- 來源：[pre-commit 官方網站](https://pre-commit.com/)、[pre-commit GitHub](https://github.com/pre-commit/pre-commit)

---

### 8. Carvel vendir
1. **使用者指令**：`vendir sync`（依據配置拉取同步）、`vendir sync -l`（或 `--locked`，嚴格使用 lock 檔同步）、`vendir diff`（比對本地目錄與宣告來源的差異）。
2. **版本鎖定與升級**：宣告檔 `vendir.yml` 搭配自動生成的 `vendir.lock.yml`，鎖定 OCI image digest（`@sha256:...`）、Git commit SHA 等。手動下 `vendir sync` 升級並重新計算 lockfile。Renovate 可透過 Custom Regex Manager 維護。
3. **已修改檔案處理**：**完全覆蓋（Overwrite）**。vendir 將受管目標目錄視為其專屬擁有的產物目錄（"owned directory"），每次 `vendir sync` 都會清空並直接覆蓋，手動變更會被抹除。
4. **解除與本機覆寫**：專用解除指令「**沒找到**」（手動自 `vendir.yml` 刪除該 directory 區塊）；**原生支援本機覆寫**：支援 `directory` 來源類型（`directory: {path: /local/path}`）。
5. **主機需求**：單一 Go 二進位檔（`vendir`）；官方提供 Linux amd64 與 arm64 binary。
- 來源：[Carvel vendir 官方文檔](https://carvel.dev/vendir/)、[Carvel vendir GitHub](https://github.com/carvel-dev/vendir)

---

### 9. Carvel imgpkg
1. **使用者指令**：`imgpkg push -b <image> -f <dir>`（將目錄打包推送為 OCI bundle）、`imgpkg pull -b <image> -o <dir>`（拉取 OCI bundle 並解壓至目錄）、`imgpkg copy -b <src> --to-repo <dst>`（映像複製/air-gapped 遷移）、`imgpkg tag list`。
2. **版本鎖定與升級**：OCI image tag 或 `@sha256:...` digest。升級由手動 pull 新 tag/digest 觸發。
3. **已修改檔案處理**：**完全覆蓋（Overwrite）**。pull 時直接解開 OCI 檔案層至目標目錄。
4. **解除與本機覆寫**：解除安裝指令「**沒找到**」；本機開發覆寫指令「**沒找到**」（純 CLI 工具，本地開發需手動本機複製目錄）。
5. **主機需求**：單一 Go 二進位檔（`imgpkg`）；支援 Linux amd64 與 arm64。
- 來源：[Carvel imgpkg 官方文檔](https://carvel.dev/imgpkg/)、[Carvel imgpkg GitHub](https://github.com/carvel-dev/imgpkg)

---

### 10. ORAS (OCI Registry As Storage)
1. **使用者指令**：`oras push <ref> <files...>`、`oras pull <ref> -o <dir>`、`oras attach`（附加 artifact 參照）、`oras discover`、`oras cp`、`oras manifest delete`。
2. **版本鎖定與升級**：支援 OCI tag 或 `@sha256:...` digest。ORAS 本身為底層傳輸工具，**無專案級 lockfile 概念**。升級由手動指定新 tag 或 digest pull 觸發。
3. **已修改檔案處理**：**完全覆蓋（Overwrite）**。pull 直接將 blob 解開或寫入本地目錄。
4. **解除與本機覆寫**：解除本地安裝指令「**沒找到**」（`oras manifest delete` 是刪除遠端 Registry 的 manifest）；本機覆寫模式「**沒找到**」。
5. **主機需求**：單一 Go 二進位檔（`oras`）；支援 Linux amd64 與 arm64。
- 來源：[ORAS 官方網站](https://oras.land/)、[ORAS GitHub](https://github.com/oras-project/oras)

---

### 11. devcontainer Features
1. **使用者指令**：由 Dev Container CLI 提供：`devcontainer up`、`devcontainer build`、`devcontainer features test`（作者測試 feature）、`devcontainer features package`、`devcontainer features publish`。
2. **版本鎖定與升級**：在 `devcontainer.json` 的 `features` 鍵宣告 OCI 參照（例如 `ghcr.io/devcontainers/features/go:1` 或具體 tag/sha）。Renovate **原生支援** `devcontainer` manager 自動偵測升級 tag；手動改版本觸發。
3. **已修改檔案處理**：**不碰專案檔案**。Features 是在容器建置期間下載 tarball 於 container 內部執行 `install.sh` 安裝工具，不產出任何檔案至宿主機專案目錄中。
4. **解除與本機覆寫**：解除只需在 `devcontainer.json` 移除該 feature key；**原生支援本機覆寫**，可在 `devcontainer.json` 中宣告本機相對路徑（例如 `"./local-features/my-feature": {}`）。
5. **主機需求**：Node.js（`@devcontainers/cli`）+ Docker / Podman；原生支援 Linux amd64 與 arm64。
- 來源：[Dev Container Features 規範](https://containers.dev/implementors/features/)、[Dev Container CLI GitHub](https://github.com/devcontainers/cli)

---

### 12. Helm Chart (OCI 散播模式)
1. **使用者指令**：`helm package`、`helm push <chart.tgz> oci://...`、`helm pull oci://...`、`helm install <release> oci://...`、`helm dependency update`、`helm dependency build`、`helm uninstall <release>`。
2. **版本鎖定與升級**：`Chart.yaml` 宣告相依性，`Chart.lock` 記錄 exact version 與 digest。手動執行 `helm dependency update`；Renovate 與 Dependabot **皆原生支援** Helm Chart.lock。
3. **已修改檔案處理**：**不碰使用者檔案**。依賴僅下載為 `charts/` 壓縮包或子目錄；在叢集部屬時由 Helm 對 Kubernetes 資源做 3-way strategic merge patch，但不對本機檔案原始碼做三方合併。
4. **解除與本機覆寫**：**有解除指令**：`helm uninstall`；**原生支援本機覆寫**：在 `Chart.yaml` dependencies 宣告 `repository: "file://../local-chart"`。
5. **主機需求**：單一 Go 二進位檔（`helm`）；支援 Linux amd64 與 arm64。
- 來源：[Helm Registries 指南](https://helm.sh/docs/topics/registries/)、[Helm GitHub](https://github.com/helm/helm)

---

### 13. Kustomize Remote Bases
1. **使用者指令**：`kustomize build <dir>`（或 `kubectl kustomize <dir>`）。
2. **版本鎖定與升級**：在 `kustomization.yaml` 的 `resources` 填寫 Git URL（如 `?ref=v1.0.0` 或 commit SHA）或 OCI URL（`oci://ghcr.io/...:tag@sha256:...`）。**無原生 lockfile 機制**。Renovate 原生支援更新其 Git ref 與 OCI tag。
3. **已修改檔案處理**：**不碰使用者檔案**。Kustomize 在記憶體中解析遠端 base 並疊加本地 overlay/patch，不將檔案落地或覆寫到專案中。
4. **解除與本機覆寫**：解除指令「**沒找到**」（直接編輯 YAML 刪除 resource）；**原生支援本機覆寫**：直接將遠端 URL 替換為本地相對目錄路徑（如 `../local-base`）。
5. **主機需求**：單一 Go 二進位檔（`kustomize`，或 kubectl 內建）；支援 Linux amd64 與 arm64。
- 來源：[Kustomize Remote Bases](https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/remote/)、[Kustomize GitHub](https://github.com/kubernetes-sigs/kustomize)

---

### 14. Git Subtree / Git-Subrepo / Git-Vendor / Vendorpull / Peru
1. **使用者指令**：
   - `git subtree`：`git subtree add --prefix=<dir> <repo> <ref>`、`git subtree pull`、`git subtree push`。
   - `git-subrepo`：`git subrepo clone <repo> <path>`、`git subrepo pull <path>`、`git subrepo push <path>`、`git subrepo status`、`git subrepo clean`。
   - `git-vendor`：`git vendor add <name> <repo> [<ref>]`、`git vendor update <name>`、`git vendor list`。
   - `vendorpull`：`vendorpull add <url> <path>`、`vendorpull update <path>`。
   - `peru`：`peru sync`、`peru reup`、`peru clean`。
2. **版本鎖定與升級**：
   - subtree/git-vendor：無獨立 lockfile，commit 資訊記錄在 Git commit message（squash merge commit）。
   - git-subrepo：子目錄內的 `.gitrepo` 鎖定 upstream commit。
   - peru：`peru.yaml` 直接鎖定 `rev: <commit-sha>`，手動執行 `peru reup` 升級。
3. **已修改檔案處理**：
   - **git subtree / git-subrepo / git-vendor**：**三方合併（3-Way Merge）**。由 Git 歷史紀錄處理 merge，修改過之檔案遇衝突產生標準 Git conflict markers。
   - **vendorpull / peru**：**完全覆蓋（Overwrite）**。peru 直接清空並重新提取目錄內容。
4. **解除與本機覆寫**：
   - 解除指令：git-subrepo 有 `git subrepo clean`；其餘「**沒找到**」專屬指令（需 `git rm` 或刪除設定檔）。
   - 本機覆寫：subtree / subrepo / vendor 可直接 clone 本地 Git 目錄；peru 支援 `type: rsync` 或 `type: copy` 指向本機目錄。
5. **主機需求**：git-subrepo / git-vendor / vendorpull 為 Bash/POSIX sh 腳本 + Git；peru 為 Python 套件；全數支援 Linux amd64 與 arm64。
- 來源：[git-subtree 官方手冊](https://github.com/git/git/blob/master/contrib/subtree/git-subtree.txt)、[git-subrepo GitHub](https://github.com/ingydotnet/git-subrepo)、[git-vendor GitHub](https://github.com/brettlangdon/git-vendor)、[vendorpull GitHub](https://github.com/sourcemeta/vendorpull)、[peru GitHub](https://github.com/buildperu/peru)

---

### 15. GitHub actions-template-sync 與 repo-file-sync-action
1. **使用者指令**：無本地 CLI 指令，屬於 GitHub Actions 雲端工作流程（透過 schedule cron 或 push event 觸發）。
2. **版本鎖定與升級**：actions-template-sync 記錄 template 的 upstream Git commit/tag；repo-file-sync-action 透過中央 repo 的 `.github/sync.yml` 宣告同步檔案與目標 repo。由 Action 自動開 Pull Request 觸發升級。
3. **已修改檔案處理**：**三方合併（3-Way Merge via PR）**。以 Git commit/PR 方式合併；下游檔案若有修改，會在 PR 內顯示 diff 或標示 Git merge 衝突，由審查者在 PR 解決。
4. **解除與本機覆寫**：解除指令「**沒找到**」（直接移除 workflow 或從 `sync.yml` 刪除目標 repo）；本機覆寫開發模式「**沒找到**」（純雲端 CI 執行）。
5. **主機需求**：本機無需安裝（GitHub Actions runner 執行）。
- 來源：[actions-template-sync GitHub](https://github.com/AndreasAugustin/actions-template-sync)、[repo-file-sync-action GitHub](https://github.com/BetaHuhn/repo-file-sync-action)

---

### 16. 薄啟動器與版本檔（Gradle Wrapper / Bazelisk / mise）
1. **使用者指令**：
   - Gradle Wrapper：`./gradlew <task>`、`./gradlew wrapper --gradle-version <v>`。
   - Bazelisk：`bazel <task>`（Bazelisk 透明代跑）。
   - mise：`mise install`、`mise upgrade`、`mise use <tool>@<ver>`、`mise run`、`mise prune`。
2. **版本鎖定與升級**：
   - Gradle：`gradle/wrapper/gradle-wrapper.properties` 中的 `distributionUrl` 與 sha256。
   - Bazelisk：`.bazelversion`（如 `7.1.0` 或 commit）。
   - mise：`mise.toml` 或 `.tool-versions`，支援 `mise.lock`。
   - 升級與機器人：手動指令升級；Renovate **原生支援** Gradle Wrapper、Bazelisk、mise；Dependabot 原生支援 Gradle Wrapper。
3. **已修改檔案處理**：**不碰專案檔案**。薄啟動器僅在背景下載並快取二進位引擎至使用者家目錄（`~/.gradle`、`~/.cache/bazelisk`、`~/.local/share/mise`），完全不寫入或修改專案內的程式代碼。
4. **解除與本機覆寫**：
   - 解除指令：「**沒找到**」（直接刪除 wrapper 腳本或版本檔）。
   - 本機覆寫：Gradle Wrapper 可設定 `distributionUrl=file:///path/to/local.zip`；Bazelisk 支援環境變數 `USE_BAZEL_VERSION=/path/to/local/bazel`；mise 支援 `mise.local.toml` 覆寫指向本地 build 出的 binary。
5. **主機需求**：
   - Gradle Wrapper：Bash/sh + Java (JRE)。
   - Bazelisk：單一 Go 二進位檔。
   - mise：單一 Rust 二進位檔。
   - 全數原生支援 Linux amd64 與 arm64。
- 來源：[Gradle Wrapper 指南](https://docs.gradle.org/current/userguide/gradle_wrapper.html)、[Bazelisk GitHub](https://github.com/bazelbuild/bazelisk)、[mise 官方文檔](https://mise.jdx.dev/)

---

### 17. Nix flakes
1. **使用者指令**：`nix flake init`、`nix flake update`、`nix flake lock`、`nix flake check`、`nix flake metadata`、`nix develop`、`nix run`。
2. **版本鎖定與升級**：`flake.nix`（宣告 inputs）搭配自動生成的 `flake.lock`（JSON 格式，鎖定 git revision、narHash 等）。手動執行 `nix flake update`；Renovate **原生支援** Nix flakes 自動升級。
3. **已修改檔案處理**：**不碰專案檔案**。純函數式環境管理，所有產物置於唯讀的 `/nix/store` 中，透過環境變數或 symlink 注入開發 shell，不碰專案程式碼。
4. **解除與本機覆寫**：解除只需在 `flake.nix` 移除 input 並執行 `nix flake update`；**原生支援本機覆寫**：命令列支援 `--override-input <name> path:/local/path`，或在 `flake.nix` 宣告 `inputs.foo.url = "path:/local/path"`。
5. **主機需求**：Nix 套件管理器（需 root 安裝 daemon 與 `/nix` 檔案目錄）；原生支援 Linux x86_64 與 aarch64 (arm64)。
- 來源：[Nix Flakes 手冊](https://nixos.wiki/wiki/Flakes)、[Nix Flakes 概念指南](https://nix.dev/concepts/flakes.html)

---

### 18. Dagger Modules
1. **使用者指令**：`dagger init`、`dagger install <module>`、`dagger develop`、`dagger call <function>`、`dagger run`。
2. **版本鎖定與升級**：`dagger.json`（宣告模組與來源 ref）搭配 `dagger.lock`（鎖定 commit SHA）。手動改版本或透過 Renovate 更新。
3. **已修改檔案處理**：**不碰專案檔案**（除 `dagger develop` 會在模組目錄下生成對應語言的 SDK 型別定義代碼外）。
4. **解除與本機覆寫**：**有解除指令**：`dagger uninstall <module>`（或手動自 `dagger.json` 移除）；**原生支援本機覆寫**：`dagger install ./path/to/local/module`。
5. **主機需求**：Dagger CLI（單一 Go 二進位）+ Docker / Podman（背景需要 container engine 運行 Dagger Engine）；支援 Linux amd64 與 arm64。
- 來源：[Dagger Module Dependencies](https://docs.dagger.io/manuals/developer/dependencies/)、[Dagger GitHub](https://github.com/dagger/dagger)

---

### 19. Earthly
1. **使用者指令**：`earthly +<target>`、`earthly init`、`earthly prune`。
2. **版本鎖定與升級**：`Earthfile` 檔頭宣告語法版本 `VERSION 0.8`。相依外部模組使用 `IMPORT github.com/org/repo:tag AS alias`。**無獨立 lockfile**，需在 IMPORT 後面手動指定 tag 或 commit。Renovate 支援更新 Earthfile 內的 Docker image 與 Git tags。
3. **已修改檔案處理**：**不碰專案檔案**。在隔離的 BuildKit container 內執行，僅將指定 artifact 導出至本地。
4. **解除與本機覆寫**：解除指令「**沒找到**」（自 `Earthfile` 移除 `IMPORT` 行）；**原生支援本機覆寫**：`IMPORT ./local/path AS alias`。
5. **主機需求**：Earthly CLI（單一 Go 二進位）+ Docker / BuildKit daemon；支援 Linux amd64 與 arm64。
- 來源：[Earthly 官方文檔](https://docs.earthly.dev/)、[Earthly GitHub](https://github.com/earthly/earthly)

---

# B. 有沒有現成工具可以直接取代 vendor_kit

### 1. 候選組合逐一評估

1. **Carvel vendir + imgpkg**
   - **能做到**：
     - 原生支援從 OCI Registry 拉取純檔案 image 並展開到目錄（`vendir.yml` 支援 `image: {url: ...}` 來源）。
     - 原生產出 `vendir.lock.yml` 鎖定 OCI image 的 digest（`sha256`）。
     - 原生支援本機覆寫（`directory: {path: ...}` 來源）。
     - 跨平台支援 Linux amd64 / arm64（單一 Go binary）。
   - **做不到（缺點）**：
     - **完全不支援三方合併（3-way merge）**：vendir 的核心設計哲學是「受管目錄為 tool-owned」，每次 `vendir sync` 都直接清空覆蓋，手動變更會被全部抹除。無法滿足「初始範本檔複製給使用者自訂、升級時三方合併」的需求。
     - 需要額外安裝二進位檔（vendir / imgpkg），不符合「主機只要 docker + git + just」的極簡要求。
   - 來源：[carvel.dev/vendir](https://carvel.dev/vendir/)

2. **ORAS + 一段 just recipe**
   - **能做到**：
     - 拉取 OCI artifact 展開至目錄（`oras pull` 或 `docker run` 直接從 scratch image 拷貝）。
     - 本機覆寫可藉由 just recipe 裡的條件判斷或符號連結（symlink）實現。
     - 只要有 docker，甚至不需額外裝 oras binary。
   - **做不到（缺點）**：
     - **ORAS 是純傳輸客戶端，完全沒有三方合併邏輯**。
     - **ORAS 沒有專案層級 lockfile 概念**。
     - 結論：這本質上就是 vendor_kit 正在寫的引擎本身，不算「現成可直接取代的工具」。
   - 來源：[oras.land](https://oras.land/)

3. **Copier 單獨，或搭配 1 / 2**
   - **能做到**：
     - **三方合併是 Copier 的最強項**：`copier update` 原生利用 Git baseline 與 answers 檔執行完備的 3-way merge。
     - 具備答案記錄與版本追蹤（`.copier-answers.yml`）。
     - 原生支援本地目錄作為模板來源。
   - **做不到（缺點）**：
     - **完全不支援 OCI Registry / Docker image**：Copier 只接受 Git repo 或本地目錄/tarball。
     - 主機需要安裝 Python (>=3.8) 及 Git，無法僅靠 docker + git + just。
     - 若搭配 vendir 或 ORAS：由外部工具拉 OCI 到暫存目錄，再叫 Copier 執行 `copier update`，理論可行但需要自己寫封裝膠水層，並非單一工具原生全包。
   - 來源：[copier.readthedocs.io](https://copier.readthedocs.io/)

4. **git subtree / git-subrepo 直接 vendoring**
   - **能做到**：
     - 三方合併：Git 原生的 3-way merge。
     - 鎖定版本：記錄在 Git 歷史（subtree）或 `.gitrepo`（subrepo）。
     - 本機覆寫：直接 pull 本機 Git repo。
     - 主機環境只需要 Git。
   - **做不到（缺點）**：
     - **完全無法解耦 Git 歷史，無法以 OCI 映像發布**：工具的 Git 歷程會污染下游專案；工具 repo 改動會直接卡死下游專案。這正是發問者欲擺脫現狀的根本原因。
   - 來源：[git-subtree manual](https://github.com/git/git/blob/master/contrib/subtree/git-subtree.txt)

5. **devcontainer Features 的 OCI 散播模型**
   - **能做到**：
     - 規範成熟的 OCI 散播模型（以 tarball 推送至 GHCR，支援多架構）。
     - `devcontainer.json` 支援本地相對路徑覆寫（`./local-features/...`）。
   - **做不到（缺點）**：
     - **完全不支援落地到專案目錄與三方合併**：Features 是在 Container 建置時跑 `install.sh` 安裝套件到容器 OS，設計目的不是為了管理專案原始碼或範本檔案。
   - 來源：[containers.dev Features specification](https://containers.dev/implementors/features/)

6. **pre-commit 的 repo 散播模型**
   - **能做到**：
     - 優秀的 CLI 介面（`autoupdate`、`try-repo` 本機測試）。
     - Renovate/Dependabot 完美支援。
   - **做不到（缺點）**：
     - 不支援 OCI image（只吃 Git repo）。
     - 不落地範本檔案至專案，亦無三方合併功能。
   - 來源：[pre-commit.com](https://pre-commit.com/)

---

### 2. 「全包四項」檢驗與最接近的工具

> **檢驗標準**：原生支援「**① 從 OCI Registry 拉純檔案 image 展開到目錄** + **② lock 檔** + **③ 三方合併使用者修改檔** + **④ 本機路徑覆寫**」全部四項。

- **檢驗結論**：**目前開源生態中「沒有任何單一現成工具」全部支援這四項。**
- **最接近的兩個工具是**：
  1. **Carvel vendir**：具備 ①（拉 OCI 檔案）、②（`vendir.lock.yml`）、④（`directory` 來源）。
     - **缺哪一項**：**缺少 ③（三方合併）**。vendir 會強制抹除覆蓋目錄，無法處理給使用者自訂的設定檔，且主機需額外裝 binary。
  2. **Copier**：具備 ②（answers 鎖定）、③（完美的 3-way merge）、④（本地目錄模板）。
     - **缺哪一項**：**缺少 ①（無法拉取 OCI image，只吃 Git）**，且需要 Python 環境。

因此，**vendor_kit 所定義的「OCI 純檔案散播 + lock 檔 + 區分唯讀工具目錄與可修改範本檔之三方合併 + Docker 零相依薄啟動器」，目前在開源界確實處於獨特的空白交集點，無法被單一現成工具無痛取代。**

---

### 3. 現成組合能力綜合評估表

| 組合 | 拉 OCI 檔案 | lock 檔 | 三方合併 | 本機覆寫 | arm64 支援 | 主機需求 | 缺什麼（為何無法直接取代） |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Carvel vendir (+ imgpkg)** | ✅ 原生 | ✅ 原生 | ❌ 無（直接強制覆蓋） | ✅ 原生 | ✅ 支援 | vendir (+ imgpkg) 單一 Go binary | **缺三方合併**；目標目錄視為唯讀產物，每次 sync 會抹除使用者修改的檔案；需額外安裝工具 |
| **ORAS + just recipe** | ✅ 原生 | ❌ 需自製 | ❌ 無（需自製） | ⚠️ 需自刻 | ✅ 支援 | docker 或 oras binary + just | **缺三方合併與 lock 邏輯**；ORAS 僅負責傳輸，三方合併與 lock 仍需自己寫，實質上就是 vendor_kit 自身 |
| **Copier (單獨)** | ❌ 不支援 | ✅ 原生 | ✅ 原生（強項） | ✅ 原生 | ✅ 支援 | Python >= 3.8 + Git | **缺 OCI 映像支援**；只吃 Git 或本地目錄；且主機需安裝 Python 與 Git，違反極簡依賴限制 |
| **git subtree / git-subrepo** | ❌ 不支援 | ✅ 原生 | ✅ 原生 | ✅ 原生 | ✅ 支援 | Git (+ bash) | **缺 OCI 映像支援**；下游專案與工具 repo 歷史深度綁定，下游 repo 肥大且版本升級污染專案歷程 |
| **devcontainer Features** | ✅ 原生 | ⚠️ 需釘 digest | ❌ 無 | ✅ 原生 | ✅ 支援 | Node.js + Docker | **缺專案檔案落地與三方合併**；本質是容器建置期安裝環境，不是管理與合併專案內檔案 |
| **pre-commit 模型** | ❌ 不支援 | ✅ 原生 | ❌ 無 | ✅ 原生 | ✅ 支援 | Python (pip/pipx) | **缺 OCI 映像支援與範本三方合併**；僅快取執行 hook，不處理專案內的範本檔案維護 |

---

# C. 對「介面命名」的觀察

在調查上述 19 個專案後，整理出業界最常見的動詞、成對解除命名與預覽查詢慣例：

### 1. 最常見的動詞模式
- **專案／宣告初始化**：
  - 首選為 **`init`**（Dagger、Nix Flakes、Earthly、pre-commit）。
  - 模板生成類偏好 **`create`**（Cruft）或 **`new`**（projen、Angular）。
- **加入外部依賴**：
  - 加入單元偏好 **`add`**（Git subtree、git-vendor、vendorpull）。
  - 具備完整環境或模組安裝概念偏好 **`install`**（Dagger、pre-commit、mise）。
  - 宣告式檔案同步首選 **`sync`**（Carvel vendir、peru）。這非常適合 vendor_kit 宣告在 `.version`、由 `just` 自動檢查並確保一致的行為。
- **更新版本**：
  - **`update`**（Copier、Cruft、Angular、Nix、Helm、vendorpull）：業界壓倒性多數，語意為「檢查新版、拉取並刷新 lockfile／套用升級」。
  - **`upgrade`**（projen、mise）：通常用於主要大版本（Major upgrade）或整套執行環境升級。
  - **`autoupdate`**（pre-commit）：特指由工具主動查詢遠端最新標籤並改寫設定檔的動作。

### 2. 成對的解除動作（Detachment / Removal）命名
- **`add` ↔ `remove`**：最標準的宣告式條目增刪（例如套件管理員、`dagger install` ↔ `dagger uninstall` / `remove`）。
- **`install` ↔ `uninstall`**：若該動作涉及在系統或專案中安裝勾點/常駐檔案，必定成對使用（如 `pre-commit install` ↔ `pre-commit uninstall`）。
- **`link` ↔ `unlink`**：**本機開發覆寫的業界黃金標準命名**（npm、yarn、pnpm、Cruft 皆如此）。若 vendor_kit 提供切換本機目錄覆寫，`link <repo> <path>` 與 `unlink <repo>` 是認知負擔最低的命名。
- **`clean` / `prune`**：用於退回狀態、刪除快取或抹除本機殘留檔案（`git subrepo clean`、`peru clean`、`mise prune`）。

### 3. 「只查不套用」的命名慣例
- **`check`**：最適合 CI 檢查（例如 `cruft check`、`nix flake check`），語意是「檢查是否最新/是否漂移，若非最新則退出碼非 0」，適合自動化流程。
- **`diff`**：最適合人眼預覽變更（例如 `cruft diff`、`vendir diff`），只印出即將套用的範本 diff，不寫入任何檔案。
- **`--dry-run`**：最標準的命令列安全旗標（例如 `copier --dry-run`、`helm --dry-run`），在既有動作指令後加上，印出模擬結果而不改變磁碟狀態。
- **`outdated`**：套件管理員常見指令（`npm outdated`、`pip list --outdated`），只條列出有新版本可升級的清單。

### 4. 對 vendor_kit 介面設計的具體建議
若希望維持「極少指令 + 自動化」，建議的最小對外動詞集合為：
- 接工具：`just vendor add <tool> [version]` 或直接寫 `.version` 由薄啟動器自動 **`sync`**。
- 升級：`just vendor update [tool]`（自動三方合併使用者修改過的範本檔）。
- 預覽：`just vendor diff [tool]` 或 `just vendor check`。
- 本機開發覆寫：`just vendor link <tool> <path>` ↔ `just vendor unlink <tool>`。
- 解除工具：`just vendor remove <tool>`。

---
# 附件 2b：agy URL 驗證結果（urlcheck_prior_art.txt）

200 https://angular.dev/cli/update
200 https://angular.dev/tools/cli
200 https://carvel.dev/imgpkg/
200 https://carvel.dev/vendir/
200 https://containers.dev/implementors/features/
200 https://copier.readthedocs.io/en/stable/
200 https://cruft.github.io/cruft/
200 https://docs.dagger.io/reference/sdks/
200 https://docs.earthly.dev/
200 https://docs.gradle.org/current/userguide/gradle_wrapper.html
200 https://github.com/AndreasAugustin/actions-template-sync
200 https://github.com/bazelbuild/bazelisk
200 https://github.com/BetaHuhn/repo-file-sync-action
200 https://github.com/brettlangdon/git-vendor
404 https://github.com/buildperu/peru
200 https://github.com/carvel-dev/imgpkg
200 https://github.com/carvel-dev/vendir
200 https://github.com/copier-org/copier
404 https://github.com/copier-org/copier/discussions/742
200 https://github.com/cruft/cruft
200 https://github.com/dagger/dagger
200 https://github.com/devcontainers/cli
200 https://github.com/earthly/earthly
404 https://github.com/git/git/blob/master/contrib/subtree/git-subtree.txt
200 https://github.com/helm/helm
200 https://github.com/ingydotnet/git-subrepo
200 https://github.com/kubernetes-sigs/kustomize
200 https://github.com/oras-project/oras
200 https://github.com/pre-commit/pre-commit
200 https://github.com/projen/projen
200 https://github.com/sourcemeta/vendorpull
200 https://github.com/yeoman/yo
200 https://helm.sh/docs/topics/registries/
404 https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/remote/
200 https://mise.jdx.dev/
200 https://nix.dev/concepts/flakes.html
403 https://nixos.wiki/wiki/Flakes
200 https://nx.dev/docs/features/automate-updating-dependencies
200 https://nx.dev/docs/features/generate-code
200 https://oras.land/
200 https://pre-commit.com/
200 https://projen.io/
200 https://yeoman.io/
200 https://github.com/buildinspace/peru
200 https://github.com/git/git/blob/master/contrib/subtree/git-subtree.adoc
200 https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/resource/
200 https://docs.dagger.io/reference/sdks/
200 https://wiki.nixos.org/wiki/Flakes

# 註記
# buildperu/peru 404 -> 正確為 buildinspace/peru
# git-subtree.txt 404 -> 已改名 git-subtree.adoc
# kustomize .../remote/ 404 -> 頁面已不存在，resource/ 頁可連
# docs.dagger.io/manuals/developer/dependencies/ 被轉址到 /reference/sdks/（原頁已移走）
# nixos.wiki 403 為反爬蟲阻擋，非失效；新站 wiki.nixos.org 可連
# copier discussions/742 404

---
# 附件 3：決策紀錄（interface.md）

# 介面題 (a)：init 是否可拿掉、安裝／解除安裝成對介面表 —— 雙軌分析（2026-09-17）

狀態：**草案，待使用者拍板**；另等 agy 前例研究（brief_prior_art.md）回來後再與本題合併。

## 交叉比對：一致
- 兩位都判定方案 A 不符硬性限制：ensure 在非明確動作時寫出初始檔與 baseline（要進 git 的檔），違反「初始檔屬於使用者」；CI 會用另一套內容測試。Claude 補了實測後果（git pull 被 untracked 檔擋住、git 不追蹤空目錄導致「第一次」永遠為真、.gitignore 是初始檔會被靜默改）。
- 兩位都採「修正版 C」：不開 init；保留 add/remove、update/upgrade、dev/undev、uninstall；ensure 只寫 ignored 內容（.<repo>/、gen/），缺 baseline 時報錯或警告，不偷補。
- (a1) 答案一致：bootstrap.sh 取代「第一次 init」沒問題；有問題的是「之後由 ensure 自動 init」，必須改成明確 `add`。
- 修復分三處接手：快取/gen 缺 → ensure；未完成接入/缺初始檔 → add；薄殼或 tracked 入口壞 → git 還原或主機腳本逃生口，不是 just recipe（just 進不了命名空間）。
- 「dev 不帶 -p = 解除」不可採，以 devmode.md 已定的 `undev` 為準。
- 我方假設「自動化不可在非明確動作時寫出要進 git 的檔」方向對但要收窄：Claude 用「ensure 只寫 gitignore 路徑；CI/frozen 下需 tracked 寫入即失敗提示」，codex 用「非明確動作不得隱含修改應提交的宣告、設定、初始檔或合併歷史」——兩者互補，可合寫成一條規則。
- bootstrap.sh 第二次跑不得使用 curl 來的新引擎覆蓋 .version 鎖定的版本；非互動模式 EOF 不算同意；不自刪。
- base 可借的只有命名空間、--option 收窄、update=查/upgrade=套用 的動詞語意；base 自身文件與實作不一致（positional VERSION、update 吞 exit 1、upgrade 自己 git commit、`--help` 每層做不到），不能照抄行為。
- `just vendor_kit --help` 在 just 做不到，只能靠 `help`/`h` recipe 補，且要另行驗收；help/list 不可觸發安裝或網路。
- upgrade 衝突時不推進 baseline、不宣告完成；回退用 git revert 整組 commit（.version + 初始檔 + baseline 同一 commit），不另開 rollback。
- fresh clone 問題：動詞 recipe 若放 gen/，clone 後 `add` 不存在；Claude 建議一行轉發 recipe 放 tracked vendor.just，codex 要求至少明訂先跑 `ensure`——兩者都指出 bootstrap.md 決議 1 需修訂或補條件。
- remove/undev/dev 必填 repo（裸跑顯示用法並失敗）；upgrade/update/ensure 可不帶 repo 表示全部。

## 交叉比對：分歧與取捨
### add 對已接入工具的冪等語意
- Claude：add 冪等 = 補缺的初始檔（已存在只 warn）與缺的 baseline，只建立不合併
- codex：通用補缺檔會復活使用者刻意刪的初始檔、且缺 baseline 時用當下 image 捏造合併祖先；add 應收窄為「已完成接入→不變更；可辨識的未完成接入→續作；無法判定歷史→停下給恢復指示」
- 取捨：採 codex。關鍵是「接入是否已完成」要可辨識，這靠 upgrade.md D-2 的 metadata 檔（記錄來源 ref/digest + 完成標記）即可判定；同時它也解掉 Claude 提的「git 不追蹤空目錄」問題。已完成接入後缺初始檔 = 使用者刪除，保留。

### bootstrap.sh 第二次執行
- Claude：偵測到 .version 就拒絕並提示 `just vendor_kit add`；只留 `--repair` 重寫薄殼
- codex：讀既有 .version，委派給鎖定版引擎跑 add；讀不到/ABI 不相容/拉不到 image 就失敗，不得退回腳本內建引擎
- 取捨：採 Claude 的「拒絕 + 提示」為主：兩個入口 + flag 同步是長期負擔。但 codex 的失敗條件仍要寫進 `--repair`：repair 用 .version 鎖定的引擎，拉不到就失敗，不得用腳本內建引擎。差異只剩「第二次要不要幫使用者做 add」，建議不做。

### remove --purge
- Claude：提供 --purge，只刪與 baseline 位元組相同、使用者沒改過的檔；目錄型內使用者新增檔與二進位不刪
- codex：第一版不提供；內容沒變不代表專案不需要；改列出曾提供的檔讓使用者用 git 刪
- 取捨：採 codex，第一版不開 --purge，remove 印出清單。理由：判準複雜（共享路徑、symlink、目錄型），而 git 已能完成同樣事情。將來有需求再加。

### upgrade 是否冪等同步（目標版 = 現版時仍合併）
- Claude：是。Renovate 只改 .version，merge 後沒人做初始檔合併，upgrade 必須在目標 = 現版時仍做合併 + 推 baseline，取代 sync
- codex：upgrade 應「優先完成 .version 已到 B 但 baseline 仍是 A 的待處理狀態」（先 A→B，不順便追到 C）；未直接談冪等
- 取捨：兩者其實是同一件事的兩種描述，合併採用：upgrade 先比對「.version 版本」與「baseline 最後合併版本」（metadata 記錄），不一致就先補到 .version 版本；一致且無新版才是 no-op。這推翻 upgrade.md 甲案「只改 .version 就停」，需重新拍板。

### update ↔ upgrade 是否算成對
- Claude：列為「upgrade 的只查半邊」，表中當成對
- codex：是前後階段，不是反向動作；不該列為成對
- 取捨：採 codex 措辭：介面表分「成對反向」與「前後階段」兩欄，update 屬後者。這不影響指令設計，只影響文件表述。

### update 結束狀態
- Claude：預設 0；`--exit-code` 且有新版回 2；查詢失敗 1
- codex：只說不改任何檔、拒絕未知參數，未定結束碼
- 取捨：採 Claude 的 0/1/2 契約（與 vendor_kit 既有契約一致），並加 codex 的「拒絕未知參數」。

### 參數形式
- Claude：`add <repo>` positional + `-t/--tag`；bootstrap `-T/--tool <repo>[=<tag>]`
- codex：一律 `-r/--repo <name>`、`-s/--source <image>`、`-t/--tag`，不用 positional
- 取捨：repo 名作 positional 可接受（git remote add、cargo add 都如此，且不承載「語意」只承載對象），但複合值 `<repo>[=<tag>]` 違反 --option 收窄，改成 `--tool base --tag v1`。image 覆寫用 `-s/--source`（比 `-i/--image` 更通用）。

### 動詞 recipe 放哪
- Claude：一行 `verb *args` 轉發放 tracked vendor.just，clone 後命名空間即完整；等於修訂 bootstrap.md 決議 1
- codex：若照現結構，第一版明確要求 fresh clone 先跑 `just vendor_kit ensure`；否則要做解析前派送設計
- 取捨：採 Claude：vendor_kit 自身動詞放 tracked vendor.just（它們不依賴 gen/，只轉發引擎）；工具 recipe（gen/tools.just）仍需先 ensure，codex 的「fresh clone 第一次 `just docker build` 找不到 recipe」在第一版接受，文件註明。

### ensure 缺 baseline 的行為
- Claude：非 CI 本機只 warn 繼續；CI/frozen 下失敗
- codex：整合歷史不完整就報錯不補（未區分 CI）
- 取捨：折衷：區分「從未完成接入」（兩邊都報錯，提示 add）與「已有 baseline 但落後 .version」（本機 warn 提示 upgrade、CI 可設為失敗）。

### `{{args}}` 轉發可靠性
- Claude：實測 `verb *args` 轉發可讓引擎收到 `--help`
- codex：節錄不足以證明含空白路徑與特殊字元能保留
- 取捨：codex 的疑慮有效但可解：recipe 內用 `"$@"` 形式（just 的 positional-arguments 設定或 `set positional-arguments`），並把「含空白 path 的 `dev -p`」列入驗收案例。

## base 慣例不可照搬之處
- base ADR 寫 `just base upgrade --tag`，但實作 upgrade.sh 解析的是 positional VERSION，usage 也寫 `[VERSION]`；ADR 清單還留有 `template new <name>`。base 沒有全面做到「--option 收窄」，只能借原則不能當已驗證規範；順帶修掉我方 upgrade.md 的 `just upgrade <name> [version]` positional 寫法。
- base 的 update recipe 用 `|| [ $? -eq 1 ]` 把「有新版」吞成 0，且忽略未知參數；不能抄，vendor_kit 自定 0/1/2 並拒絕未知參數。
- base 的 upgrade.sh 會重跑 init.sh 改 symlink/.gitignore 並自己 git add + commit，直接違反 vendor_kit「工具不碰 git、初始檔屬於使用者」限制；只借動詞語意。
- base 的 init 不是純修復：init.sh 自動判斷第一次 scaffold 或重建 symlink，是「第一次與修復同一冪等動詞」；且它管的是 symlink，跟 vendor_kit 的初始檔/baseline 所有權完全不同，名稱不必沿用。
- base 沒有把 .base 從 repo 拔掉的指令；成對只落實在 `completions install|uninstall`（host-side 檔）。remove/uninstall 語意應參考 apt remove/purge、cargo/git-remote add↔remove，不是 base。
- 「每層 --help」在 base 也未成立（justfile 註解自承 `just base --help` 攔不到）；just 1.53 實測 `just vendor_kit --help` 報錯，動詞 `--help` 只在 `*args` 全轉發時才到引擎。
- base 的 `mod?`/`import?` 可選匯入不可套到 tracked 啟動器（bootstrap.md 已定為反模式），只用於 gen/tools.just。
- `--lang`、completions 是 base 產品功能，不在 vendor_kit 範圍；ADR「every level: --help, --lang」不該整句繼承。
- `set working-directory := '../..'` 是 base 模組位於 `<repo>/script/base/` 的結果；vendor_kit 的 vendor.just 在 `.vendor_kit/` 要用 `'..'`。
- 「裸指令最大範圍」不能套到破壞性動詞：remove、undev、dev 必填 repo。
- agy/決策紀錄內部矛盾待修：.version 的 vendor_kit 是頂層 key（bootstrap.md 第一行 grep）還是 `[tools]` 成員（brief）？兩者在 TOML 是不同位置，shell 與引擎必須讀同一 schema。
- 決策紀錄「子程序 ensure + exec just 重跑」未解決兩題：gen/ 不存在時工具 recipe 根本不會被發現；子程序 re-exec 不會替換父程序，第一版應以非 0 狀態阻止父流程並提示重跑。
- 「逐檔 tmp+rename 原子寫入」不等於整次操作原子；.version、初始檔、baseline、gen 可能停在不同階段，需要 flock + metadata 標記可辨識中間狀態 + 重跑續作。

## 最終建議
採「修正版 C」，兩位共識為底，分歧處取較保守的一邊：

1. **(a1)** bootstrap.sh 取代第一次 init 沒問題；「ensure 自動 init」有問題，改成明確 `add`。不開 `init`：快取缺 → `ensure`；未完成接入 → `add` 安全續作；薄殼/根 justfile 那行壞 → `bootstrap.sh --repair`（用 .version 鎖的引擎，拉不到就失敗，不得用腳本內建引擎）或 git 還原。

2. **ensure 規則（假設收窄後）**：ensure 只寫 gitignore 路徑（.<repo>/、gen/）；任何 tracked 寫入都必須是使用者明確打的動詞；「從未完成接入」報錯提示 add，「baseline 落後 .version」本機 warn 提示 upgrade、CI 失敗。

3. **成對介面表**（常用 3 + 進階 5 + bootstrap.sh；所有動詞 `verb *args` 一行轉發、放 tracked vendor.just；`[group('common')]`/`[group('advanced')]` 分段；`help`/`h` recipe 補命名空間層 help）：

| 動詞 | 參數 | 反向 | 用途 | 結束狀態 | 組 |
|---|---|---|---|---|---|
| bootstrap.sh | `--tool <repo>`（可重複）、`-t/--tag`、`-s/--source <image>`、`-y/--yes`、`--repair` | `uninstall` | 第一次接入；`--repair` 重寫薄殼不動 .version/初始檔/baseline | 0；1 不留半成品；偵測到 .version 且無 --repair → 1 提示 `add` | 一次性 |
| `add <repo>` | `-t/--tag`、`-s/--source`、`-n/--dry-run` | `remove` | 接工具；已完成接入→不變更；可辨識未完成→續作；無法判定歷史→1 給指示；指定版本與鎖定不同→要求 upgrade | 0 / 1（不動 .version） | 常用 |
| `remove <repo>` | `-n/--dry-run`（第一版無 --purge） | `add`（不保證還原合併歷史） | 停用工具；移宣告、override、快取、baseline、gen；保留初始檔並列清單 | 0（未接 = 0+提示）；1（.version.local 有覆寫→先 undev）；裸跑 → 用法+1 | 進階 |
| `update [<repo>]` | `--exit-code` | 無（upgrade 是後續階段） | 只查不動檔；拒絕未知參數 | 0；--exit-code 有新版 2；查詢失敗 1 | 進階 |
| `upgrade [<repo>]` | `-t/--tag`（限單一 repo）、`-n/--dry-run` | git revert 整組 commit | 套用新版；**先補「.version 已到 B、baseline 仍 A」的待合併**（不順便追 C）；目標=現版且無待合併 = no-op；不帶 repo 含自身，自身變了先換自己、停下要求重跑 | 0；1 不動 .version；2 衝突不推 baseline；無 baseline → 1 提示 add | 常用 |
| `dev <repo>` | `-p/--path`（必填） | `undev` | 本機改工具；不污染 upgrade 合併來源；第一版不支援 vendor_kit 自身 | 0；1（缺 dist/init.toml；CI 拒絕） | 常用 |
| `undev <repo>` | 無 | `dev -p` | 回正式版（先移 entry 再重裝） | 0（未啟用 = 0+提示）；1 | 進階 |
| `ensure [<repo>]` | 無（CI 自動 frozen） | 無（快取可丟） | 自動前置；fresh clone 後工具 recipe 出現前必跑一次 | 0；1（frozen 需 tracked 寫入 / 從未完成接入） | 進階 |
| `uninstall` | `-y/--yes`、`-n/--dry-run` | bootstrap.sh | 逐工具 remove → 刪 .vendor_kit/、.version、.version.local、gen；根 justfile 那行只在與 bootstrap 寫入完全相同時刪，否則印指示 | 0 / 1 | 進階 |

不開：init、sync（=upgrade 補待合併）、diff（=upgrade --dry-run）、accept（衝突解完重跑 upgrade）、rollback（git revert）、clean（git clean -fdX）、completions、install/verify（引擎內部）。

4. **必須一起改的先前決議**：upgrade.md 甲案「只改 .version 就停」→ 改為 upgrade 含合併 + 推 baseline；upgrade.md 的 positional `[version]` → `-t/--tag`；bootstrap.md 決議 1 → vendor_kit 自身動詞放 tracked vendor.just，只有工具 recipe 放 gen/；D-2 metadata 檔明訂記錄「來源 ref/digest、最後合併版本、接入完成標記」並兼作空目錄佔位。

5. **驗收案例**：`just vendor_kit add --help` 到引擎；`dev -p "含 空白/路徑"` 正確傳遞；fresh clone 裸 `just vendor_kit` 列出完整命名空間且不觸網。

## 要問使用者的問題
- 接受把 install + 三方合併 + baseline 推進併進 `upgrade`（推翻 upgrade.md 甲案「只改 .version 就停」），且 upgrade 先補「.version 已變、baseline 未合併」的待處理狀態？
- .version 正式 schema：vendor_kit 是頂層 key（bootstrap.md 第一行 grep）還是 `[tools]` 成員（brief）？只能選一個。
- `<repo>` 如何對映 image？固定 `ghcr.io/<org>/<repo>-dist`（org 從哪來）、還是 add/bootstrap 一律可用 `-s/--source` 覆寫並在 .version 記下來源？
- 第一版 `remove` 不提供 `--purge`、一律保留初始檔並印清單——接受嗎？
- add 的「已完成接入」判定靠 metadata 標記檔（兼作 baseline 空目錄佔位）：接受 upgrade.md D-2 的 metadata 兼任嗎？檔名與欄位（來源 ref/digest、最後合併版本、完成標記）？
- bootstrap.sh 第二次跑：拒絕 + 提示 `add`（建議）還是委派鎖定引擎跑 add？`--repair` 第一版要做嗎？
- vendor_kit 自身動詞 recipe 放 tracked vendor.just（修訂 bootstrap.md 決議 1），工具 recipe 仍放 gen/，fresh clone 第一次 `just docker build` 前要先 `ensure`——第一版接受嗎？
- `uninstall` 刪根 justfile 的 import 行：只在該行與 bootstrap 寫入完全相同時才刪、否則印指示——這個唯一動使用者檔的例外可以嗎？
- CI/frozen 偵測用 `CI=1` 自動還是 ensure 加 `--frozen`？本機遇到「baseline 落後 .version」只 warn 提示 upgrade 可接受嗎？
- `upgrade` 不帶 repo 含 vendor_kit 自身時，「停下要求重跑」（upgrade.md C-4）與討論圖 (c)「自動 re-exec」何者為準？子程序無法替換父程序，建議前者。
- repo 名用 positional（`add base`）還是一律 `-r/--repo`？bootstrap 的 `--tool base --tag v1`（拆開）可接受嗎？
- 分組名稱用英文 common/advanced 還是中文？

---
## 附：Claude 分析原文（recommendation）
**codex 建議：採「修正版 C」——不設 `init`，保留 `add/remove`、`dev/undev`、`update/upgrade`、`uninstall`，並把 `ensure` 限定為「重建本機執行環境（只寫 ignored 內容）」。** 但草稿的「第一次 bootstrap、之後 ensure 自動 init」不能原樣採用：接工具、建立初始檔與建立 baseline 仍須由明確的 `bootstrap`/`add` 完成。我方傾向 C 站得住，但 C 的優勢理由要改：不是「add 冪等 = 通用補檔」，而是「add 只做安全續作，無法判定歷史時停下來」。

**(a1) init 拿掉會不會有問題？** bootstrap.sh 取代「第一次 init」沒問題；ensure 取代「之後的初始檔管理」有問題（CI 補出未提交的初始檔與 baseline、捏造合併祖先、復活使用者刪的檔）。結論：不開 `init`，把修復分配給三處——快取/gen 缺失 → `ensure`；tracked 入口或 baseline 遺失 → git 還原（或逃生口）；未完成接入 → `add` 安全續作。

**bootstrap.sh 契約：** 第一次建立專案整合並委派接入工具；再次執行時先讀既有 `.version`，只呼叫該版引擎的 `add`；若讀不到、ABI 不相容或鎖定 image 無法取得就失敗，**不得退回腳本內建的新引擎**。不自刪，非互動模式缺參數就失敗，EOF 不代表同意。

**假設修訂：** 「自動化不可在非明確動作時寫出要進 git 的檔」改為「**非明確的專案維護動作，不得隱含修改應提交的工具宣告、整合設定、初始檔或合併歷史**」。明確執行 add/upgrade 時寫 tracked 檔是需要的功能。

### 建議的 just 介面表（recipe 均在 `just vendor_kit`；每個動作提供 `-h/--help`；帶值選項均有短選項；`--repo` 指登錄名稱、`--source` 指工具 image 來源）

| 動詞 | 參數 | 成對的反向動作 | 什麼時候用 | 結束狀態 | 常用/進階 |
|---|---|---|---|---|---|
| `add` | `-r/--repo <name>`；新來源用 `-s/--source <image>`；可選 `-t/--tag <tag>` | `remove --repo <name>` | 接入工具；安全續作未完成的接入 | 寫入含 digest 的鎖定宣告、建立快取與初始 baseline；新初始檔建立，既有檔保留並報告碰撞；完成接入後重跑不補回使用者刪檔；指定版本與既有鎖定不同 → 要求改用 upgrade | 常用 |
| `remove` | 必填 `-r/--repo <name>`（裸跑 = 顯示用法並失敗） | `add`，但不保證還原原合併歷史 | 專案停止使用某工具 | 移除宣告、該工具 local override、快取、baseline 與產生入口；**保留使用者初始檔**（第一版不提供 `--purge`，改列出曾提供的檔讓使用者用 git 刪）；禁止以此移除 vendor_kit | 進階 |
| `update` | 可選 `-r/--repo <name>` | 無反向；後續為 `upgrade`（前後階段，非成對） | 查詢可用新版 | 報告目前與候選版本；不改鎖定、baseline 或使用者檔；拒絕未知參數 | 進階 |
| `upgrade` | 可選 `-r/--repo <name>`；`-t/--tag <tag>` 僅能搭配單一 repo | 以 git 還原整組升級變更；指定舊 tag 是另一次合併，不是 rollback | 套用新版或指定版本；**優先完成 `.version` 已變更但 baseline 未合併的待處理狀態**（A→B，不順便追到 C） | 鎖定版本、快取與範本合併結果一致；衝突回非成功狀態、保留可恢復資訊、不推進 baseline、不宣告完成 | 常用 |
| `dev` | 必填 `-r/--repo <name>`、`-p/--path <dir>` | `undev --repo <name>` | 在本機開發工具 | 建立 ignored override；不改 `.version`、初始檔或 baseline；不污染 upgrade 的合併來源；第一版不接受 vendor_kit 自身 | 常用 |
| `undev` | 必填 `-r/--repo <name>` | `dev --repo … --path …` | 回到發布版本 | 移除指定 override，恢復使用 `.version` 的工具；重跑無副作用 | 進階 |
| `ensure` | 可選 `-r/--repo <name>`，省略為全部 | 不另設 uninstall（快取可丟棄，接入關係由 remove 解除） | fresh clone、快取修復、日常自動前置檢查 | 本機快取與 gen 符合鎖定版本及允許的 dev override；**不改 tracked 檔**；整合歷史不完整（缺 baseline）則報錯不補 | 進階；fresh clone 第一版可能必跑 |
| `uninstall` | 可選 `-y/--yes` | 重新 `bootstrap.sh`；精確恢復用 git | 整個專案退出 vendor_kit | 移除工具登錄、vendor_kit 自有入口、baseline、local override 與專案內快取；僅移除可辨識的根 import／管理區塊；保留使用者檔、根 justfile、混有其他設定的 `.version`/`.gitignore` 內容、全域 Docker image | 進階 |
| `bootstrap.sh`（just 外，release 附） | `-r/--repo <name>`、`-s/--source <image>`、可選 `-t/--tag <tag>`、`-y/--yes` | `uninstall` | 第一次接入；入口故障時的有限逃生路徑 | 首次建立鎖定引擎與穩定入口，接入指定工具；既有專案只委派 `.version` 鎖定的引擎跑 add，不隱含升級；不自刪 | 首次操作 |

裸 `just vendor_kit` 列出「常用：add、upgrade、dev」與其餘進階操作。

### 不另外開指令的動作
- **`init`：不開。** 初次接入由 bootstrap/add；本機重建由 ensure；tracked 損壞用 git 恢復。
- **`install`/`uninstall <tool>`：不開另一組。** 對外生命週期就是 add/remove；引擎內部 install 只是快取實作。
- **`repair`/`sync`：暫不開。** 沒有比上述三種恢復手段更清楚的獨立契約。
- **`rollback`/`downgrade`：不另開。** 精確回退須一起還原 .version、baseline 與初始檔（git revert 整組 commit）；只 revert .version 不夠；指定舊 tag 是另一個版本變更。
- **`clean`：暫不開。** ignored 快取可直接刪掉由 ensure 重建。
- **`verify`：先作為 ensure 內部檢查。** 只在需要「只檢查不修復」的 CI 契約時再公開。
- **`completions install/uninstall`：第一版不新增。** 未來真的安裝到使用者環境再成對提供。

### 兩項不能靠命名解決的實作門檻
1. fresh clone 依現有結構需先跑 `just vendor_kit ensure`（gen/ 不存在時工具 recipe 找不到）；若要第一次直接 `just docker build`，須先完成解析前派送設計。
2. `just vendor_kit --help` 必須另行驗收，照貼 base 的 help recipe 不足；help／列表本身不應觸發安裝或網路查詢。

## 附：codex 分析原文（recommendation）
## 結論

**採 C 的修正版（C′）**：拿掉 `init`，成對動詞照 B；但 (1) bootstrap.sh 第二次跑不是 add，而是「拒絕並提示 `just vendor_kit add`」，只有 `--repair` 才做第二次用途（重寫薄殼）；(2) `upgrade` 定義為冪等同步，接住 Renovate 之後的初始檔合併；(3) 動詞 recipe 全部是一行轉發、放 tracked 的 vendor.just；(4) ensure 絕不寫 tracked 檔，CI 下遇到需要寫就失敗提示。

**(a1) 答案**：把 `init` 動詞拿掉沒問題（需要它的三種情境都有人接手），但「由 ensure 第一次自動 init」有問題，必須改成明確動作 `add`。我方假設「自動化不可在非明確動作時寫出要進 git 的檔」**成立，但要收窄成可執行的規則**：生態系裡確實有隱式寫 tracked 檔的例子（npm install 寫 package-lock、terraform init 寫 .terraform.lock.hcl），它們能成立是因為同時滿足「機器擁有、可從 tracked 輸入決定性重生、CI 有 frozen 模式改為失敗（`npm ci`、`-lockfile=readonly`）」三條；初始檔第一條就不過（建立後歸使用者、之一是 .gitignore），所以 vendor_kit 的規則寫成：**ensure 只能寫 gitignore 的路徑；任何 tracked 寫入都必須是使用者明確打的動詞；CI（`CI=1` 或 `--frozen`）下 ensure 若判斷需要 tracked 寫入就以 1 結束並印出該打的指令。**

## 建議的 just 介面表

| 動詞 | 參數（--option；帶值皆有短選項） | 反向動作 | 什麼時候用 | 結束狀態 | 分組 |
|---|---|---|---|---|---|
| `bootstrap.sh`（release 附，主機跑） | `-T/--tool <repo>[=<tag>]`（可重複，不給 tag = 最新）、`-y/--yes`（非互動；EOF 不算同意）、`--repair`、`-h/--help` | `just vendor_kit uninstall` | 專案第一次接 vendor_kit；`--repair`：薄殼／根 justfile 那行壞掉時用 .version 鎖的引擎重寫薄殼（不動 .version、初始檔、baseline） | 0；1 失敗不留半成品；偵測到 .version 且無 `--repair` → 1 並提示 `just vendor_kit add` | 一次性 |
| `add <repo>` | `-t/--tag <tag>`（預設最新）、`-i/--image <ref>`（image 路徑不符 `<org>/<repo>-dist` 慣例時）、`-n/--dry-run` | `remove <repo>` | 接第二個以後的工具；對已在 .version 的工具 = 冪等修復：補缺的初始檔（已存在只 warn 不覆蓋）、補缺的 baseline。**只建立、不合併** | 0（含 warn）；1 失敗不動 .version | 常用 |
| `remove <repo>` | `--purge`（連初始檔一起刪，只刪與 baseline 位元組相同、使用者沒改過的）、`-n/--dry-run` | `add <repo>` | 不再用某工具 | 0（未接 = 0 + 提示，apt 語意）；1（該工具在 .version.local 有覆寫 → 提示先 `undev`） | 進階 |
| `update [<repo>]` | `--exit-code` | `upgrade` 的「只查」半邊 | 只想知道有沒有新版，不動任何檔；CI 定期檢查 | 0 已列出；`--exit-code` 且有新版 → 2；1 查詢失敗 | 進階 |
| `upgrade [<repo>]` | `-t/--tag <tag>`（指定版本；比現版舊時警告仍執行）、`-n/--dry-run`（= 舊 diff，只印會動哪些檔） | 回退 = `git revert` 該 commit（Renovate merge 用 `-m 1`）；明確降版 = `upgrade <repo> -t <舊>` | 追新版；**Renovate merge 後補做初始檔三方合併**（目標版 = 現版時跳過改 .version，仍做合併 + 推 baseline）。不帶 repo = 全部含 vendor_kit 自身：自身有變先換自己、停下要求重跑 | 0；1 失敗不動 .version；2 有衝突（列檔名，解掉後再跑一次 upgrade 收尾）；沒有 baseline 的工具 → 1 提示先 `add` | 常用 |
| `dev <repo>` | `-p/--path <dir>`（必填） | `undev <repo>` | 本機改工具本身 | 0；1（dir 缺 dist/ 或 init.toml；CI 環境拒絕） | 常用 |
| `undev <repo>` | （無） | `dev <repo> -p` | 改完工具回到 .version 正式版（先移 entry 再重裝，不跑一般 ensure） | 0（未啟用 = 0 + 提示）；1 | 進階 |
| `ensure [<repo>]` | （無；CI 自動 frozen） | 無反向（純冪等快取同步）；清快取 = `git clean -fdX` 或 `rm -rf .<repo>/ .vendor_kit/gen/` | 自動（每個工具 recipe 前）；人只在復原時打。逃生口 `just --justfile .vendor_kit/vendor.just ensure` | 0；1（frozen 下需 tracked 寫入 → 1 + 該打的指令；非 frozen 下缺 baseline 只 warn） | 進階 |
| `uninstall` | `--purge`（同 remove）、`-n/--dry-run` | `bootstrap.sh` | 把 vendor_kit 從專案拔掉：逐工具 remove → 刪 .vendor_kit/、.version、.version.local、gen | 0；根 justfile 那行只在與 bootstrap 寫入的完全相同時才刪，否則印指示 | 進階 |
| `help`（alias `h`） | 各動詞 `--help` 由引擎印 | — | `just vendor_kit` 裸打 = `--list`（用 `source_file()` 釘住模組）；`just vendor_kit --help` 在 just 做不到，`help` recipe 補 | 0 | — |

**實作備註**：所有動詞 recipe 一律 `verb *args:` 一行轉發給引擎（`--list` 簽名寫在 doc 註解），否則 `just vendor_kit add --help` 會把 `--help` 吃成 repo（實測）；用 `[group('常用')]`/`[group('進階')]` 屬性分段；`upgrade`/`add`/`remove` 寫 .version 前在 flock 內重讀。

## 不開指令的動作（自動或 git 就夠）

| 不開 | 由誰接 |
|---|---|
| `init` | 第一次 = `add`；缺初始檔／baseline = `add` 冪等；薄殼壞 = `bootstrap.sh --repair` |
| `diff` | `upgrade --dry-run` |
| `accept` | `upgrade` 合併成功自動推 baseline；衝突解完再跑一次 `upgrade` |
| `sync` | `upgrade <repo>`（目標 = 現版）|
| `install` / `verify` | 引擎內部，ensure 呼叫 |
| 回退 | `git revert`（.version + 初始檔 + baseline 同一個 commit 時一次退乾淨） |
| Renovate 升級 | 自動：merge → 下次 `just` ensure 裝；初始檔用 `upgrade <repo>` 補 |
| `clean` | `git clean -fdX`（會連 .version.local 一起清，文件要提） |
| `completions` | 工具（base）自帶，vendor_kit 不管 |

指令數：常用 3（add、upgrade、dev）＋ 進階 5（remove、undev、update、ensure、uninstall）＋ bootstrap.sh。使用者原話的三個「init、upgrade、dev」對映為 `add`、`upgrade`、`dev`。