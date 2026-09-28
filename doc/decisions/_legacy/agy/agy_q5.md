這是一份針對「**薄啟動器（`justfile`）的出貨、更新與 bootstrap 策略**」的業界前例研究與方案評估報告。

---

# 前例研究：薄啟動器（`justfile`）的出貨、更新與 Bootstrap

## 一、「薄啟動器 + 版本檔」的業界前例分析

我們針對業界 10 個具代表性的啟動器/版本管理工具進行梳理，重點檢視：
- **(a) 啟動器進不進 git？**
- **(b) 誰負責更新啟動器？**
- **(c) 啟動器與被啟動工具的版本是分開還是綁定？**

---

### 1. Gradle Wrapper
- **架構**：專案根目錄存放啟動腳本 `gradlew` / `gradlew.bat`、二進位啟動器 `gradle/wrapper/gradle-wrapper.jar`，以及版本宣告檔 `gradle/wrapper/gradle-wrapper.properties`。
- **(a) 進不進 git**：**進 git**。官方強烈建議完整 commit，確保協作者與 CI 無須預裝 Gradle 即可直接執行。
- **(b) 誰負責更新啟動器**：開發者手動執行 `./gradlew wrapper --gradle-version X.Y.Z`（或由 Renovate/Dependabot 提 PR）。執行時 Gradle 會直接覆寫 `gradlew` 腳本、jar 與 properties 檔。
- **(c) 版本關係**：**高度綁定**。Wrapper 腳本與 jar 的實作會隨 Gradle 發行版同步演進（官方建議執行兩次 wrapper task 確保腳本與 runtime 版本完全對齊）。
- **來源**：[Gradle User Manual: Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)

---

### 2. Maven Wrapper
- **架構**：類似 Gradle，專案包含 `mvnw` / `mvnw.cmd`、`.mvn/wrapper/maven-wrapper.jar` 及 `.mvn/wrapper/maven-wrapper.properties`。
- **(a) 進不進 git**：**進 git**。
- **(b) 誰負責更新啟動器**：開發者手動執行 `mvn wrapper:wrapper -DmavenVersion=X.Y.Z`。
- **(c) 版本關係**：**半獨立但通常同步**。Wrapper Plugin 本身有自己的版號（如 3.3.x），但它產出的 `mvnw` 與設定檔會綁定目標 `mavenVersion`。
- **來源**：[Apache Maven Wrapper Documentation](https://maven.apache.org/wrapper/)

---

### 3. Bazelisk
- **架構**：專案根目錄只放 `.bazelversion`（純文字版本字串）；啟動器是名為 `bazel` 的 Go 二進位檔（即 Bazelisk）。
- **(a) 進不進 git**：**不進 git**。標準做法是由開發者在主機全域安裝（或由 CI runner 預裝），專案只追蹤 `.bazelversion`（少數專案會自己放幾行 bash wrapper，但非官方主流）。
- **(b) 誰負責更新啟動器**：主機套件管理器（`brew`、`npm -g`、`apt` 或 GitHub Releases）負責更新 Bazelisk；專案內的 Bazel 版本則由開發者直接改寫 `.bazelversion`。
- **(c) 版本關係**：**完全分開**。Bazelisk 本身是獨立工具，它讀取 `.bazelversion` 去官方儲存庫動態拉取並快取對應版本的 Bazel runtime。
- **來源**：[GitHub: bazelbuild/bazelisk](https://github.com/bazelbuild/bazelisk)

---

### 4. mise / asdf 的 shim
- **架構**：專案根目錄只放 `.tool-versions` 或 `mise.toml`；啟動器（shim 腳本）統一放在使用者家目錄（如 `~/.local/share/mise/shims` 或 `~/.asdf/shims`），掛在主機 `$PATH` 前端。
- **(a) 進不進 git**：**絕對不進 git**。Shim 屬於主機環境資產，專案 repo 只進設定檔。
- **(b) 誰負責更新啟動器**：`mise` / `asdf` 本身（如 `mise self-update` 或套件管理）或執行 `asdf reshim`；專案不參與 shim 更新。
- **(c) 版本關係**：**完全分開**。Shim 只是通用轉發器，在呼叫當下讀取當前工作目錄的 `.tool-versions` / `mise.toml`，再去執行已安裝的特定版本 binary。
- **來源**：[mise Documentation: Shims](https://mise.jdx.dev/dev-tools/shims.html)、[asdf Core Commands: reshim](https://asdf-vm.com/manage/core-commands.html#reshim)

---

### 5. uv / `uvx`
- **架構**：`uvx` 是 Astral 開發的 `uv` 工具之別名（等同 `uv tool run`）。直接以暫存隔離環境執行 CLI（如 `uvx ruff@0.4.0 check .`），或在專案內依據 `pyproject.toml` 執行。
- **(a) 進不進 git**：**不進 git**。`uv` / `uvx` 為本機二進位工具。
- **(b) 誰負責更新啟動器**：本機環境（如 `uv self update`）。
- **(c) 版本關係**：**完全分開**。`uvx` 負責動態建構臨時 virtualenv 並拉取套件，與被啟動的 Python 套件版本無依賴。
- **來源**：[Astral uv Documentation: Tools & uvx](https://docs.astral.sh/uv/concepts/tools/)

---

### 6. Nix Flakes (`nix run`)
- **架構**：專案目錄包含 `flake.nix` 與 `flake.lock`。啟動器為本機安裝的 `nix` CLI。
- **(a) 進不進 git**：`nix` CLI **不進 git**；宣告檔 `flake.nix` 與精確依賴鎖定檔 `flake.lock` **進 git**。
- **(b) 誰負責更新啟動器**：作業系統套件管理更新 `nix`；專案相依則透過 `nix flake update` 刷新 `flake.lock`。
- **(c) 版本關係**：**完全分開**。Nix CLI 作為直譯器，其自身的版本與 Flake 中宣告並建構的 derivation 版本完全解耦。
- **來源**：[Nix Reference Manual: nix run](https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-run.html)

---

### 7. Dagger CLI 與 `dagger.json`
- **架構**：主機安裝 `dagger` CLI；專案根目錄由 `dagger init` 產生 `dagger.json`，其中包含模組設定與 `engineVersion`（現行推薦搭配 workspace modules）。
- **(a) 進不進 git**：CLI **不進 git**；`dagger.json` **進 git**。
- **(b) 誰負責更新啟動器**：主機套件管理器更新 CLI；`dagger.json` 透過 `dagger develop` 或手動修改更新。
- **(c) 版本關係**：**半綁定/自動協商**。`dagger` CLI 預設會啟動相同版號的 Dagger Engine 容器（`registry.dagger.io/engine:<version>`），但 `dagger.json` 限制了模組最低支援的 engine 版本，若 CLI 過舊會直接擋下。
- **來源**：[Dagger Modules & Configuration Documentation](https://docs.dagger.io/manuals/developer/modules)

---

### 8. Earthly (`Earthfile` `VERSION`)
- **架構**：主機安裝 `earthly` CLI；專案目錄放置 `Earthfile`，第一行強制以 `VERSION 0.8` 宣告語法版本。
- **(a) 進不進 git**：CLI **不進 git**；`Earthfile` **進 git**。
- **(b) 誰負責更新啟動器**：主機套件管理更新 CLI；開發者手動修改 `Earthfile`。
- **(c) 版本關係**：**語法向下相容的相依**。CLI 自身版本必須大於等於 `Earthfile` 所宣告的 `VERSION`，否則 CLI 會中止並提示升級。
- **來源**：[Earthly Earthfile: VERSION command](https://docs.earthly.dev/docs/earthfile#version)

---

### 9. Dev Container CLI (`@devcontainers/cli`)
- **架構**：本機安裝 `@devcontainers/cli`（npm 套件或 standalone binary）；專案內簽入 `.devcontainer/devcontainer.json`。
- **(a) 進不進 git**：CLI **不進 git**；`.devcontainer/devcontainer.json` **進 git**。
- **(b) 誰負責更新啟動器**：本機 npm / IDE 插件自動更新；專案設定由使用者手動或 CLI 模板指令更新。
- **(c) 版本關係**：**完全分開**。CLI 只依據 Specification 解析 JSON 並調度 Docker/Podman，不綁定容器內環境版本。
- **來源**：[GitHub: devcontainers/cli](https://github.com/devcontainers/cli)

---

### 10. Batect（最貼近 vendor_kit 的案例）
- **架構**：Batect 是基於 Docker 的建置工具，專案根目錄必須包含 `batect` (bash) / `batect.cmd` (bat) 啟動腳本，以及任務定義檔 `batect.yml`。
- **(a) 進不進 git**：**進 git**。官方設計 philosophy 與 Gradle Wrapper 相同，主打「免預裝任何環境，只要有 Docker 就能跑」。
- **(b) 誰負責更新啟動器**：**啟動器自帶更新機制**。開發者在專案目錄執行 `./batect --upgrade`，它會自動抓取最新版並覆寫專案內的 `batect` 腳本（Renovate 亦內建支援 Batect wrapper 自動發 PR）。
- **(c) 版本關係**：**高度綁定**。`batect` 啟動腳本內有一行寫死版本號（`batect_version=...`），執行時由腳本自動下載該版本的 jar/runtime，更新啟動器即等同更新 batect。
- **來源**：[Batect Documentation: Installation](https://batect.dev/docs/getting-started/installation)、[Batect: Upgrading](https://batect.dev/docs/using-batect/upgrading)

---

### 啟動器分類歸納表

| 模式 | 代表案例 | 啟動器進 Git？ | 更新發起者 | 版本耦合度 | 對 vendor_kit 的借鏡 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **In-Repo Wrapper** | **Gradlew, Batect** | **是** | 自帶 `--upgrade` 覆寫或 CI PR | 高度綁定 | **完全相符**。vendor_kit 限制主機只有 Docker + just，`justfile` 必須進 repo。 |
| **External Shim / CLI** | Bazelisk, mise, asdf, uvx | 否 | 主機套件管理器 | 完全分開 | 不適用。因為專案不可強制要求主機安裝專用 CLI（如 Python/vendor_kit binary）。 |
| **Declarative Spec** | Dagger, Earthly, devcontainer | 否 | 主機套件管理器 | 語法契約約束 | 不適用，理由同上。 |

---

## 二、「用 Container 寫出 Bootstrap 檔」的前例與實務指令

在主機無特定語言環境時，透過 `docker run` 掛載本機目錄並執行 `init` / `new` 輸出初始檔案是行之有年的做法。以下是業界常見案例與真實指令：

### 1. Material for MkDocs (`squidfunk/mkdocs-material`)
- **指令**：
  ```bash
  docker run --rm -it -v ${PWD}:/docs squidfunk/mkdocs-material new .
  ```
- **行為**：掛載宿主目錄到容器內 `/docs`，在當前目錄產生 `mkdocs.yml` 與 `docs/index.md`。
- **來源**：[Material for MkDocs: Getting Started with Docker](https://squidfunk.github.io/mkdocs-material/getting-started/#with-docker)

### 2. Jekyll 官方 Image (`jekyll/jekyll`)
- **指令**：
  ```bash
  docker run --rm -v "$PWD:/srv/jekyll" -it jekyll/jekyll jekyll new .
  ```
- **行為**：掛載當前目錄至 `/srv/jekyll`，在宿主目錄骨架化出 `_config.yml`、`Gemfile` 與目錄結構。
- **來源**：[GitHub: envygeeks/jekyll-docker](https://github.com/envygeeks/jekyll-docker)

### 3. Hugo Container (`klakegg/hugo` / `hugomods/hugo`)
- **指令**：
  ```bash
  docker run --rm -v $(pwd):/src klakegg/hugo:ext-alpine new site . --force
  ```
- **行為**：掛載當前目錄至 `/src`，產生 `hugo.toml` 與結構檔。
- **來源**：[GitHub: klakegg/docker-hugo](https://github.com/klakegg/docker-hugo)

### 4. HashiCorp Terraform (`hashicorp/terraform`)
- **指令**：
  ```bash
  docker run --rm -v "$(pwd):/workspace" -w /workspace hashicorp/terraform:latest init
  ```
- **行為**：首次執行時在宿主機的工作目錄寫出 `.terraform/` 目錄與鎖定檔 `.terraform.lock.hcl`。
- **來源**：[Docker Hub: hashicorp/terraform](https://hub.docker.com/r/hashicorp/terraform)

### 5. Dev Container CLI (`@devcontainers/cli`)
- **指令**：
  ```bash
  docker run --rm -v "$PWD:/work" -w /work ghcr.io/devcontainers/cli:latest \
    templates apply -t ghcr.io/devcontainers/templates/typescript-node -w /work
  ```
- **行為**：從 OCI Registry 下載模板，在掛載的宿主機目錄寫出 `.devcontainer/devcontainer.json`。
- **來源**：[GitHub: devcontainers/cli](https://github.com/devcontainers/cli)

### 6. Renovate (`renovate/renovate`)
- **指令**：
  ```bash
  docker run --rm -v "$(pwd):/usr/src/app" renovate/renovate:latest renovate-config-validator
  ```
- **行為**：掛載工作區驗證 `renovate.json`；若專案無設定檔，Renovate 容器在 headless 執行時會自動產出 onboarding PR（內含初始 `renovate.json`）。
- **來源**：[Renovate Docs: Config Validation](https://docs.renovatebot.com/config-validation/)

---

## 三、風險分析：啟動器（`justfile`）被專案修改後的升級處理

若 `justfile` 進入了專案 git，使用者極有可能在其中加入自訂 recipe（例如 `just test`、`just build`）或修改原有行為。當 vendor_kit 升級時，如何面對「既有修改 vs 上游新版啟動器」？

### 1. 業界前例機制回顧

| 工具 / 框架 | 升級處理機制 | 衝突處置方式 | 優缺點評價 |
| :--- | :--- | :--- | :--- |
| **Gradle Wrapper** (`gradle wrapper`) | **破壞性覆蓋 (Destructive Overwrite)** | 直接覆寫 `gradlew`，不管使用者修改。 | 簡單粗暴，但官方明確禁止使用者修改 wrapper；若使用者有改動則直接遺失。 |
| **Copier** (`copier update`) | **Git 三方合併 (3-Way Merge)** | 以 `.copier-answers.yml` 記錄狀態，升級時對比 `base`、`current`、`new`，執行 `git merge-file`。支援 `--conflict inline`（注入 `<<<<<<<`）或 `--conflict rej`（產出 `.rej` 檔）。 | 強大，但會破壞性汙染使用者檔案或殘留 `.rej` 檔案。 |
| **Cruft** (`cruft diff` / `cruft update`) | **Patch 應用與檢查** | 專案存放 `.cruft.json` 記錄 template commit。`cruft diff` 顯示差異（支援 `--exit-code` 用於 CI）；`cruft update` 嘗試打補丁，衝突時生成 `.rej`。 | 檢查方便，但衝突處置依然具有破壞性。 |
| **Ruby on Rails** (`rails app:update`) | **互動式比對 (Thor Diff & Prompt)** | 比對新範本與本機檔案，若有衝突跳出互動 prompt：`[Y/n/a/q/d/h]`。<br>- `d`：顯示 unified diff。<br>- `Y`：確認覆蓋。<br>- `n`：略過。<br>- 支援 `THOR_MERGE="code -d $1 $2"`。 | **對使用者最友善**，給予完全知情權，預設不強制破壞。 |
| **Angular / Nx** (`ng update`) | **AST 語義化 CodeMod** | 解析 TypeScript/JSON AST 進行精確節點變更，由開發者用 `git diff` 驗證。 | 技術成本極高，適用於語言語法升級，不適用於一般 Makefile/justfile 腳本。 |

- **來源參考**：
  - [Copier: Updating a Project](https://copier.readthedocs.io/en/stable/updating/)
  - [Cruft Documentation](https://cruft.github.io/cruft/)
  - [Ruby on Rails Guides: The Update Task](https://guides.rubyonrails.org/upgrading_ruby_on_rails.html#the-update-task)

### 2. 針對「不自動改使用者檔、只顯示 diff」原則的實務建議

在 vendor_kit 的架構下，若採用傳統的「單一 `justfile` 涵蓋全部邏輯」，會產生死結：**使用者一定會加自己的 recipe，而 vendor_kit 升級又必須改動啟動器語法**。

若堅持「工具不自動改使用者檔、只顯示 diff」，建議採取 **兩層防禦策略**：

1. **架構層解耦（首選解法：利用 `just` 的 `import` 特性）**：
   - `just` 原生支援 `import` 與可選引入 `import?`（見 [just manual: imports](https://just.systems/man/en/#imports)）。
   - **拆分檔案所有權**：
     - `justfile`（專案所有）：只包含 `import? ".vendor_kit/vendor.just"`，其餘空間留給使用者自行撰寫專案 recipe。
     - `.vendor_kit/vendor.just`（vendor_kit 完全所有）：存放 `install`、`verify`、`diff`、`upgrade` 等標準啟動 recipe。
   - **效果**：每次升級時，工具可以**大膽且自動地覆寫 `.vendor_kit/vendor.just`**（因為它是生成物，使用者被明確告知不可修改），而專案根目錄的 `justfile` **永不變動、永無衝突**。
2. **升級指令（`just upgrade`）的比對與警示機制**：
   - 升級時比對 `.version` 與啟動器。若有需要使用者確認的差異（例如根目錄 `justfile` 範本發生重大變更）：
     - 參考 `rails app:update` 與 `cruft diff`，在 terminal 輸出彩色的 Unified Diff。
     - 輸出訊息：「`justfile` has drifted from template. Showing diff below. No files were modified. Run with --write to overwrite.`」
     - 嚴格遵守「只讀比對、非破壞性輸出」原則。

---

## 四、可選方案評估、比較表與最終建議

針對「啟動器由誰出貨、怎麼更新、第一次怎麼放進專案」，提出以下 3 個方案進行深度權衡：

---

### 方案 A：單一 `justfile` 由 vendor_kit 出貨 + Bootstrap 一行寫出 + 升級時 Diff（目前傾向）

- **運作流程**：
  1. **Bootstrap**：使用者執行：
     ```bash
     docker run --rm -u $(id -u):$(id -g) -v "$PWD:/repo" ghcr.io/org/vendor_kit:v1 bootstrap
     ```
     在專案根目錄產生單一 `justfile` 與空的 `.version`。
  2. **專案結構**：只有 2 個檔案：`justfile` 與 `.version`。
  3. **升級流程**：執行 `just upgrade` 時，容器內部比對新版標準 `justfile` 與專案當前 `justfile`。若不同，印出 diff 並提供覆蓋參數（如 `just upgrade --overwrite-justfile`）。
- **優點**：
  - 目錄極度乾淨，嚴格維持「專案只有兩個必要檔」的簡約心智模型。
  - 開發者執行 `just --list` 能直接看見所有可用子命令與說明。
- **缺點**：
  - **衝突頻率高**：一旦開發者在 `justfile` 加上專案自訂的 recipe（如 `just run`、`just test`），未來只要 vendor_kit 調整了底層 docker flags，每次 `upgrade` 都會跳出 diff 衝突，無法一鍵無痛自動化升級。

---

### 方案 B：`justfile` 由專案自己維護，vendor_kit 只提供範本（Copy-Paste）

- **運作流程**：
  1. **Bootstrap**：vendor_kit 只負責產生 `.version`，`justfile` 由開發者從 README 複製，或由 bootstrap 產出一次後即宣告歸專案所有。
  2. **升級流程**：`just upgrade` 只負責更新 `.version`（更新 image tag 與 hash），完全不碰、也不 diff `justfile`。
- **優點**：
  - 邊界清楚，工具絕不干預專案檔案，完全沒有合併衝突問題。
- **缺點**：
  - **版本漂移（Drift）風險**：若 vendor_kit 容器調整了命令列介面（CLI contract，例如環境變數傳遞、掛載路徑調整），舊版 `justfile` 可能無法驅動新版 container，導致專案壞死且難以排查。

---

### 方案 C：雙層分離架構 —— `justfile` (使用者) + `.vendor_kit/vendor.just` (工具全權託管)（★ 強烈推薦）

- **運作流程**：
  1. **Bootstrap**：
     ```bash
     docker run --rm -u $(id -u):$(id -g) -v "$PWD:/repo" ghcr.io/org/vendor_kit:v1 bootstrap
     ```
     輸出：
     - `.version`
     - `.vendor_kit/vendor.just`（內含由 vendor_kit 產生的完整標準 recipes：`install`, `verify`, `diff`, `upgrade` 等）
     - `justfile`（只有極精簡的 2 行）：
       ```just
       # Project recipes can be added below
       import? ".vendor_kit/vendor.just"
       ```
  2. **自訂與覆寫能力**：
     - 開發者在 `justfile` 自由增加自訂 recipe。
     - 若要自訂 vendor 行為，由於 `just` 的 import 規則是「頂層（shallower）定義會覆蓋底層（deeper）定義」，開發者隨時可以在根目錄 `justfile` 覆寫同名 recipe。
  3. **升級流程**：
     - 執行 `just upgrade` 時，直接無痛覆寫 `.vendor_kit/vendor.just` 與更新 `.version`。
     - 根目錄的 `justfile` 永遠不需被工具修改，因此符合「不改使用者檔」且「零升級負擔」。
- **優點**：
  - **徹底解耦**：使用者私有 recipes 與上游啟動器邏輯物理隔離。
  - **自動升級無衝突**：啟動器邏輯有修正時，直接覆寫 `.vendor_kit/vendor.just`，不會引發任何 merge conflict。
  - **體驗無損**：因為 `just` 會遞迴展開 import，終端機執行 `just --list` 或 IDE 補全時，所有 vendor 子命令依然完整呈現。
- **缺點**：
  - 比原先預期的「只有兩個檔」多了一個隱藏目錄/檔案（`.vendor_kit/vendor.just`）。

---

### 三方案綜合比較表

| 評估維度 | 方案 A：單一 `justfile` 由工具出貨 (目前傾向) | 方案 B：`justfile` 由專案自理 (純範本) | 方案 C：雙層 `import` 分離架構 (建議方案) |
| :--- | :--- | :--- | :--- |
| **檔案數量** | 2 個 (`justfile`, `.version`) | 2 個 (`justfile`, `.version`) | 3 個 (`justfile`, `.version`, `.vendor_kit/vendor.just`) |
| **Bootstrap 難易度** | 單行 `docker run ... bootstrap` | 需手動複製貼上或初始生成 | 單行 `docker run ... bootstrap` |
| **使用者能否自訂 Recipe** | 能，但在同一個檔案混寫 | 能，完全自由 | 能，乾淨隔離且支援語法覆寫 |
| **升級維護負擔** | 高（只要有自訂就會有 diff 警示，需手動確認） | 高（介面變更時需手動修復 launcher） | **極低（Vendor 檔自動替換，使用者檔不動）** |
| **違反「不改使用者檔」風險**| 中（若使用者按強制覆寫會洗掉自訂內容） | 無（完全不管） | **無（只更新工具託管目錄下的檔案）** |
| **Shell / IDE 自動補全** | 完整支援 | 完整支援 | 完整支援 |

---

## 五、最終結論與建議

1. **結論**：
   - 業界前例中，凡是需要將啟動腳本進 git 的工具（如 **Gradle** 與 **Batect**），其升級手段都是**直接覆寫啟動器**；然而這兩者之所以可行，是因為它們**嚴格要求使用者不可修改啟動器腳本**。
   - `justfile` 在專案中具有「專案任務入口」的本質，開發者勢必會想在裡面添加專案專屬的 recipes。若走 **方案 A**，勢必陷入「專案改了 `justfile` $\rightarrow$ 升級時產生 diff $\rightarrow$ 使用者每次升級都要人肉審查或手動 merge」的困境，這與現代 DevOps 工具追求的「無感、自動化升級」相違背。

2. **具體建議：採行「方案 C（雙層 `import` 模式）」**：
   - **Bootstrap**：維持目前傾向，使用單行容器指令建立：
     ```bash
     docker run --rm -u $(id -u):$(id -g) -v "$PWD:/repo" ghcr.io/org/vendor_kit:v1 bootstrap
     ```
     自動寫出空 `.version`、`.vendor_kit/vendor.just` 與帶有 `import? ".vendor_kit/vendor.just"` 的 `justfile`。
   - **更新機制**：
     - `just upgrade` 執行時，工具僅負責更新 `.version` 及覆寫 `.vendor_kit/vendor.just`。
     - 專案根目錄的 `justfile` 視為「使用者資產（User-owned file）」，工具永遠不碰。
   - 這樣既保留了「主機只需 Docker + just」的前提，又完美兼顧了「工具不擅改使用者檔案」與「啟動器能夠零衝突無痛升級」兩大核心要求。
