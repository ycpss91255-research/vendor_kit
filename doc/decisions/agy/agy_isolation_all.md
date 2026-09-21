### A. 根 justfile 怎麼不碰使用者的

#### 2. 工具「擁有」根檔 vs. 使用者擴充放另一個檔

* **pre-commit**
  * **誰擁有根檔**：專案/使用者擁有根目錄，工具只擁有並讀取 [`.pre-commit-config.yaml`](https://pre-commit.com/#pre-commit-configyaml---top-level)；它完全不擁有也不碰專案的 `Makefile` / `justfile`。
  * **使用者擴充放哪**：自訂 hook 寫在 `.pre-commit-config.yaml` 內的 `repo: local` 區塊，或透過引用本機 script 執行。
  * **升級時根檔怎麼換**：透過 [`pre-commit autoupdate`](https://pre-commit.com/#pre-commit-autoupdate) 凍結/更新各 hook 的 `rev` 版本號，工具本體永不改寫或覆蓋該 YAML 骨架。

* **devcontainer**
  * **誰擁有根檔**：工具規範擁有專屬目錄 [`.devcontainer/`](https://containers.dev/implementors/json_reference/) 及其下的 `devcontainer.json`。
  * **使用者擴充放哪**：使用者透過 `customizations` 宣告編輯器外掛、用 [Features](https://containers.dev/implementors/features/) 混入通用工具，或透過 VS Code [Dotfiles 機制](https://code.visualstudio.com/docs/devcontainers/containers#_personalizing-with-dotfile-repositories) 注入個人 shell/git 設定。
  * **升級時根檔怎麼換**：Features 宣告語意版本由 runtime 自動抓取；範本檔（Templates）透過 CLI 更新時若遇到使用者既有檔案，依賴 Git 追蹤或由使用者手動 review，不強制靜默覆蓋。

* **Nix flake / devenv**
  * **誰擁有根檔**：團隊/專案擁有根目錄的 [`flake.nix`](https://nixos.wiki/wiki/Flakes) 或 [`devenv.nix`](https://devenv.sh/basics/)。
  * **使用者擴充放哪**：devenv 原生支援 [`devenv.local.nix`](https://devenv.sh/guides/devenv-local-nix/)（或 `devenv.local.yaml`），若存在會自動載入並與主設定合併，官方建議加入 `.gitignore`。
  * **升級時根檔怎麼換**：執行 `nix flake update` 或 `devenv update` 僅更新 `flake.lock`，完全不修改使用者的 `.nix` 原始檔。

* **Bazel `WORKSPACE` + `.bazelrc` + `user.bazelrc`**
  * **誰擁有根檔**：專案團隊擁有 `WORKSPACE`（或 `MODULE.bazel`）以及入庫的 [`.bazelrc`](https://bazel.build/run/bazelrc)。
  * **使用者擴充放哪**：官方標準作法是在 `.bazelrc` 寫入 [`try-import %workspace%/user.bazelrc`](https://bazel.build/run/bazelrc#imports)；使用者個人設定寫入 `user.bazelrc`（已在 `.gitignore` 內），檔案不存在時會靜默略過。
  * **升級時根檔怎麼換**：Bazel 版本由 `.bazelversion` (Bazelisk) 管理；`.bazelrc` 隨團隊 git commit 演進，不破壞個人的 `user.bazelrc`。

* **git config 的 `include.path` / `includeIf`**
  * **誰擁有根檔**：Git 擁有設定檔結構（`.git/config` 或 `~/.gitconfig`）。
  * **使用者擴充放哪**：在主設定檔以 [`[include] path = <path>`](https://git-scm.com/docs/git-config#_includes) 或 `[includeIf "gitdir:..."] path = <path>` 載入外部檔案，設定由後者疊加覆蓋前者。
  * **升級時根檔怎麼換**：Git 升級或 `git config` 命令不會抹除既有 include 區塊，設定純粹為字典合併。

* **just 社群慣例與討論（根 justfile 由工具產生、使用者放 justfile.local）**
  * **社群慣例**：**沒找到**「just 官方由工具擁有根檔、自動隱式載入 justfile.local」的官方慣例。
  * **討論事實**：just 支援語法 [`import? 'justfile.local'`](https://just.systems/man/en/imports.html)（可選導入，若檔案不存在不報錯）；社群在 [casey/just#1787](https://github.com/casey/just/issues/1787) 討論過多檔 import 順序與食譜覆蓋優先級（shallow 覆蓋 deep）。若工具直接覆寫專案根 `justfile`，使用者無法在根檔寫 recipe，必須強制拆檔。

---

### A. 根 justfile 怎麼不碰使用者的

#### 3. 工具在使用者檔「加一行」的反感點、改進與 `.git/info/exclude` 前例

* **使用者反感的點（社群討論事實）**：
  * **污染 Git 與破壞 Dotfiles**：`rustup`、`nvm`、`conda init` 自動修改 `~/.bashrc` / `~/.zshrc`，導致使用者用 Git 管理的 dotfiles 被破壞、工作區變 dirty（如 [rustup#2040](https://github.com/rust-lang/rustup/issues/2040) 在唯讀 HOME 會報錯；[conda#8836](https://github.com/conda/conda/issues/8836) 被批評寫入大量 shell block 且拖慢啟動效能；[HN 討論](https://news.ycombinator.com/item?id=23746684)）。
  * **格式破壞與重複行**：`cargo init` 會自動在既有 `.gitignore` 追加 `/target`，多次執行可能產生重複行或破壞排版（[cargo#1877](https://github.com/rust-lang/cargo/issues/1877)）。
  * **協作衝突與隱式行為**：`git-lfs track` 自動寫入 `.gitattributes`，在多人分支合併時頻繁造成屬性衝突，甚至因換行符號問題損壞 pointer 狀態（[git-lfs#4174](https://github.com/git-lfs/git-lfs/issues/4174)）。`direnv` 生成的 `.direnv/` 快取未忽略會弄髒 `git status`；`.envrc` 若誤 commit 易洩漏機密。

* **後來改掉／退讓提供開關的工具**：
  * **Husky**：v4 原先在 `postinstall` 劫持所有 hooks 並依賴 `package.json` 的 `"husky"` 欄位；[Husky v5+](https://blog.typicode.com/husky-v5/) 改用 Git 2.9+ 原生 `core.hooksPath = .husky`，鉤子回歸為 `.husky/` 內的獨立 shell script，並改用 npm 標準生命週期 `"prepare": "husky"`。
  * **Rustup**：新增 [`--no-modify-path`](https://github.com/rust-lang/rustup/issues/2040) 旗標，允許 CI/自動化腳本安裝時不觸碰任何 shell rc。
  * **Conda**：提供 `conda config --set auto_activate_base false`，避免自動劫持環境與 PATH。
  * **uv**：`uv init` 預設產生 `.gitignore`，但提供 [`--no-gitignore`](https://docs.astral.sh/uv/reference/cli/#uv-init) 旗標，且遇到既有 `.gitignore` 時不強制覆蓋。
  * **pre-commit**：[`pre-commit install`](https://pre-commit.com/) 偵測到既有 hook 時不直接覆蓋，而是先備份為 `pre-commit.legacy` 並在末尾串接調用。

* **工具寫入 `.git/info/exclude` 而非 `.gitignore` 的前例**：
  * [**`git-extras` (`git-ignore -p`)**](https://github.com/tj/git-extras/blob/master/man/git-ignore.md)：提供 `-p` / `--private` 參數，明確將忽略規則寫入本機專屬的 `.git/info/exclude` 而非共享的 `.gitignore`。
  * [**Emacs `Magit` (`magit-gitignore`)**](https://magit.vc/manual/magit/Ignoring-Files.html)：內建功能提供 `magit-gitignore-in-gitdir`（快速鍵 `i` -> `p`），將忽略模式寫入 `$GIT_DIR/info/exclude`，作為使用者本機私有忽略的第一等操作。
  * [**`portool` (Git worktree 管理工具)**](https://github.com/t09tanaka/portool)：在 `portool init` 時，會自動將內部生成的本地狀態檔追加寫入 `.git/info/exclude`，避免污染專案共用的 `.gitignore`。

---

### 對比總結表

| 做法 | 前例 | 優點 | 缺點 | 對我們的適用性（事實陳述） |
| :--- | :--- | :--- | :--- | :--- |
| **工具完全擁有根檔，使用者放擴充檔** | Bazel (`.bazelrc` + `try-import user.bazelrc`)、devenv (`devenv.local.nix`) | 工具升級時可無痛整檔更新根檔；入口路徑標準化。 | 使用者無法隨意在根檔新增食譜；若使用者誤改根檔，升級會產生衝突或需手動合併。 | just 需在根 justfile 頂部寫 `import? "justfile.local"`（just ≥ 1.33 支援 `import?`）；根 justfile 每次升級可整檔替換。 |
| **使用者擁有根檔，工具放在子目錄／獨立檔** | pre-commit (`.pre-commit-config.yaml`)、devcontainer (`.devcontainer/`) | 根 Makefile / justfile 100% 歸使用者掌控；工具零侵入使用者原有建置腳本。 | 工具無法直接成為 `just <recipe>` 的頂層入口；使用者需要多打一層命名空間或手動 delegate。 | 下游專案使用者可自由寫根 justfile，但若要直接 `just <tool-recipe>`，根 justfile 必須宣告 `mod` 或 `import` 指向 vendor 快取。 |
| **工具在使用者檔中「加一行」** | cargo init (.gitignore)、Husky (`package.json` prepare)、nvm/conda (.bashrc) | 使用者不需改變原本指令與檔案結構即可獲得整合。 | 破壞版本控制乾淨度、多次執行易產生重複行或合併衝突，在社群中常引發抗議。 | vendor_kit 原則為「根 justfile 加一行 import」。若使用者檔被改，升級時需依賴三方合併，無法直接靜默覆寫。 |
| **本機忽略寫入 `.git/info/exclude`** | `git-extras (git-ignore -p)`、`Magit (gitdir)`、`portool` | 完全不觸碰需要 git commit 的 `.gitignore`，保證專案 git status 與 commit 歷史零污染。 | 僅存在於當前本地 clone，跨機器、新 clone 或 CI 環境不會自動繼承，需每次重新寫入。 | vendor_kit 僅在本機執行薄啟動器，每次 `just` 執行時若檢查並補上 `.git/info/exclude`，可做到完全不改動團隊共用 `.gitignore`。 |
### B. 版本檔與工具目錄的命名／位置慣例

#### 4. 工具狀態檔放專案根還是專屬目錄之案例與歸納

##### (1) 工業界真實前例
* **[.terraform/](https://developer.hashicorp.com/terraform/language/files/dependency-lock) + [.terraform.lock.hcl](https://developer.hashicorp.com/terraform/language/files/dependency-lock)**：運行下載的 Provider 二進位檔放 `.terraform/`（快取目錄，列入 `.gitignore`）；依賴校驗鎖定狀態放根目錄 `.terraform.lock.hcl`（單檔，提交至版本控制）。
* **[.copier-answers.yml](https://copier.readthedocs.io/en/stable/updating/)**：Copier 專案根單檔，記錄模板來源與各答案變數，供後續 `copier update` 進行 Git 三方合併比對，需 commit。
* **[.cruft.json](https://cruft.github.io/cruft/)**：Cruft 根單檔，記錄 Cookiecutter 模板 Git commit hash 與 Context，用於 `cruft check` 與漂移更新，需 commit。
* **[.projen/](https://projen.io/docs/concepts/overview/) + [.projenrc.js](https://projen.io/docs/concepts/overview/)**：內部合成狀態（如 tasks.json）集中於 `.projen/`（自動生成目錄，部分 gitignore）；使用者規格定義入口置於根目錄單檔 `.projenrc`。
* **[.devcontainer/](https://containers.dev/implementors/spec/)**：多檔時集中於 `.devcontainer/`（包含 `devcontainer.json`、Dockerfile、啟動腳本）；極簡單檔時亦允許根目錄 `.devcontainer.json`。
* **[.mise.toml / mise.toml](https://mise.jdx.dev/configuration/)**：版本宣告兼設定檔，支援根目錄單檔，亦支援集中放於 `.config/mise/config.toml`。
* **[.pre-commit-config.yaml](https://pre-commit.com/)**：根目錄單檔，直接供使用者閱讀、修改與宣告 hook repo 版本。
* **[.tool-versions](https://asdf-vm.com/manage/configuration.html)**：asdf 根目錄單檔，多語言版本通用宣告檔，被眾多工具通用解析。
* **[.nvmrc](https://github.com/nvm-sh/nvm#nvmrc)**：Node.js 版本宣告單檔，極簡字串，專案根目錄標準。
* **[Chart.lock](https://helm.sh/docs/topics/charts/#the-chartlock-file)**：Helm 依賴鎖定檔，平級置於 `Chart.yaml` 旁（根目錄或 Chart 目錄）。
* **[vendir.lock.yml](https://carvel.dev/vendir/docs/latest/vendir-spec/)**：Carvel vendir 鎖定檔，記錄 vendored 資源精確 digest，與 `vendir.yml` 平級放根目錄。
* **[flake.lock](https://nix.dev/manual/nix/latest/command-ref/new-cli/nix3-flake#lock-files)**：Nix Flake 鎖定檔，記錄 inputs 的 git hash，與 `flake.nix` 平級放根目錄。
* **[.gitmodules](https://git-scm.com/docs/gitmodules)**：Git 子模組宣告單檔放根目錄（commit），實際 checkout 快取放 `.git/modules/`。
* **`.base/`（base subtree）**：Git subtree 模式常將外部共用工具直接拉入專案根下的專屬隱藏目錄（如 `.base/`），與業務代碼物理隔離。

##### (2) 歸納：什麼情況用「點目錄集中放」 vs 「根目錄單檔」
* **點目錄集中放（`.<tool>/`）**：
  * 當工具產出多個檔案、包含二進位/暫存/下載快取（如 `.terraform/`、`.projen/`、`.devcontainer/`）。
  * 檔案屬於機器維護之黑箱實體，非供使用者直接閱讀修改，且多數須加入 `.gitignore`。
* **根目錄單檔**：
  * 需要團隊協作共識、納入版本控制（Git commit）的規格宣告或鎖定檔（如 `flake.lock`、`.copier-answers.yml`、`.terraform.lock.hcl`）。
  * 作為通用入口以便外部工具、IDE 或 CI 直觀偵測。

##### (3) 檔名帶工具名 vs 通用名的利弊
* **帶工具名（如 `.copier-answers.yml`、`.pre-commit-config.yaml`）**：
  * *利*：命名空間完全隔離，不會與專案自身代碼或其他工具碰撞；在 Monorepo 或跨工具檢索時特徵明確。
  * *弊*：檔名較長。
* **通用名（如 `.version`）**：
  * *利*：路徑簡短、外觀乾淨。
  * *弊*：極易語意衝突（許多專案會以 `.version` 記錄專案本身的 Release 版本）；缺乏自解釋性，未接觸過 vendor_kit 的人無法識別其擁有者。

##### (4) Renovate custom regex manager 的支援度與限制
* **檔名限制**：Renovate 的 [customManagers (Regex Manager)](https://docs.renovatebot.com/modules/manager/regex/) 採用 RE2 引擎，以 [`managerFilePatterns`](https://docs.renovatebot.com/configuration-options/#managerfilepatterns)（舊稱 `fileMatch`）比對 Git 倉庫檔案清單，對檔名格式無特殊限制。
* **隱藏檔與點目錄比對**：完全支援。比對正則需正確跳脫點字元（例如 `/(^|/)\\.version$/` 或 `/(^|/)\\.vendor_kit/version\\.toml$/`）。Renovate 預設僅忽略 `node_modules` 與 `vendor` 等特定目錄，不會阻擋 `.github/`、`.tool-versions` 或自訂點目錄內的檔案，除非自訂配置的 `ignorePaths` 明確予以排除。

---

#### 5. 三個候選架構事實評估

* **候選 (a)**：現狀 `.version` + `.version.local` + `.vendor_kit/` + `.<repo>/`
* **候選 (b)**：全部收進 `.vendor_kit/`（`.vendor_kit/version.toml`、`.vendor_kit/cache/<repo>/`）
* **候選 (c)**：根檔改名 `.vendor_kit_version`（或 `.vendor_kit.toml`），快取維持根目錄 `.<repo>/`

| 評估維度 | 候選 (a)：現狀 `.version` + 根目錄快取 | 候選 (b)：全收進 `.vendor_kit/` | 候選 (c)：根檔 `.vendor_kit_version` |
| :--- | :--- | :--- | :--- |
| **一眼看出是 vendor_kit** | 根檔 `.version` 無工具識別度，容易誤會為專案自身版本；各工具快取（如 `.base/`）散落根目錄。 | 根目錄無散落設定檔；所有檔案集中於 `.vendor_kit/`，目錄名稱即工具名，歸屬完全自解釋。 | 根檔案名稱直觀帶有 `vendor_kit`，用途明確；但若各工具快取（`.<repo>/`）仍放根目錄則局部發散。 |
| **Renovate regex** | 規則為 `/(^|/)\\.version$/`；若倉庫存在其他用途之 `.version`，存在非預期誤判匹配風險。 | 規則為 `/(^|/)\\.vendor_kit/version\\.toml$/`；路徑特徵全域唯一，無誤傷其他檔案之可能。 | 規則為 `/(^|/)\\.vendor_kit_version$/`；檔名全域唯一，同樣無誤傷風險。 |
| **啟動器 grep** | 目標為 `./.version`，路徑最簡短；若疊加 local 需額外判斷 `./.version.local`。 | 目標為 `.vendor_kit/version.toml`；路徑增加一層子目錄，grep / awk 語法與 (a) 完全相同。 | 目標為 `./.vendor_kit_version`；路徑位於專案根，比 (a) 僅檔名略長，語法一致。 |
| **工具 just 模組路徑** | 模組路徑短，例如：<br>`mod base '.base/justfile'` | 模組路徑加深，例如：<br>`mod base '.vendor_kit/cache/base/justfile'` | 同 (a)，快取若維持在根目錄，模組路徑最短：<br>`mod base '.base/justfile'` |

---

#### 總結對比表

| 做法 | 前例 | 優點 | 缺點 | 對 vendor_kit 的適用性（事實陳述） |
| :--- | :--- | :--- | :--- | :--- |
| **1. 根目錄通用單檔 + 根目錄點快取** | [.tool-versions](https://asdf-vm.com/manage/configuration.html)、[.nvmrc](https://github.com/nvm-sh/nvm#nvmrc) | 檔名最短；啟動器與 `just mod` 引用路徑皆為最短字元數。 | 易與專案本身的專案版本號語意衝突；快取散落在專案根目錄；Renovate regex 需嚴格過濾避免誤匹配。 | 啟動器單行 grep 最短；但使用者無法單看根目錄檔名得知此檔屬 vendor_kit。 |
| **2. 工具專屬點目錄全收納** | [.devcontainer/](https://containers.dev/implementors/spec/)、[.projen/](https://projen.io/docs/concepts/overview/) | 專案根目錄零污染；工具邊界清晰；Renovate 匹配路徑具唯一性。 | 檔案在子目錄內，需要點進目錄才看得到；根 `justfile` 的 `mod` 引用路徑長度增加。 | 符合「把自己的檔切乾淨」原則，但根 `justfile` 需改寫為 `mod base '.vendor_kit/cache/base/justfile'`。 |
| **3. 根目錄專屬單檔 + 集中或分散快取** | [.copier-answers.yml](https://copier.readthedocs.io/en/stable/updating/)、[.cruft.json](https://cruft.github.io/cruft/)、[.terraform.lock.hcl](https://developer.hashicorp.com/terraform/language/files/dependency-lock) | 既保留根目錄能見度，又以名稱前綴避免衝突；Renovate 設定直觀。 | 根目錄多一個以特定工具為前綴的點檔案；若快取未收攏仍有目錄散落。 | 兼顧啟動器路徑長度與工具專屬辨識度，且徹底消除通用檔名被 Renovate 誤傷的可能。 |
### C. 初始檔怎麼明確隔離

#### 6. 前例：生成／範本工具怎麼標示「這個檔是工具給的」

*   **[projen](https://projen.io/)**
    *   **區分機制**：在產生檔案的檔頭插入 `~ Generated by projen` 註解，並於檔案系統直接設為唯讀權限（`chmod 0444`），同時於專案根寫入清單檔 [`.projen/files.json`](https://projen.io/) 記錄所有受管路徑。不區分使用者可改或別改，其哲學為「受管檔禁止手動修改，所有變更必須透過 `.projenrc` 程式碼配置；若要自己管必須呼叫 `eject`」。
    *   **升級處理**：重新執行 `npx projen` 時，依據 `.projen/files.json` 的紀錄比對，重新計算並直接全量覆寫檔案；若舊檔案自配置中消失則由合成器自動自磁碟刪除。
*   **[Copier](https://copier.readthedocs.io/en/latest/updating/)**
    *   **區分機制**：
        *   使用者可改：預設所有範本檔案使用者皆可修改，升級時以三方合併（3-way merge）整合上游。
        *   使用者別改／初始化後不追蹤：提供 [`_skip_if_exists`](https://copier.readthedocs.io/en/latest/configuring/#skip_if_exists) 設定清單。若目標路徑已存在，Copier 便完全凍結該檔，後續升級不再套用任何更新，亦不參與三方合併。
    *   **升級處理**：透過 `.copier-answers.yml` 記錄使用的版號與變數，升級時重新 render 出舊版與新版暫存檔，調用 `git merge-file` 與使用者工作目錄進行三方合併；衝突時留下標準 git 衝突標記（`--conflict inline`）或產生 `.rej` 檔。
*   **[Cruft](https://cruft.github.io/cruft/)**
    *   **區分機制**：在專案根產生 [`.cruft.json`](https://cruft.github.io/cruft/) 記錄 template 來源與 commit hash。透過 `.cruft.json` 中的 `skip` 陣列定義「使用者自訂、工具不再更動」的檔案或 glob 路徑。
    *   **升級處理**：執行 `cruft update` 時計算 template 舊 commit 到新 commit 的 git diff，跳過 `skip` 列表中的檔案，其餘檔案以 `git apply` 將 patch 套用至本地專案；遇衝突時產生 `.rej` 檔案。
*   **[Yeoman](https://yeoman.io/authoring/file-system.html)**
    *   **區分機制**：不預先標記可改或別改，透過內建模組 [`@yeoman/conflicter`](https://yeoman.io/authoring/file-system.html) 與記憶體檔案系統（`mem-fs`）在寫入前比較磁碟既有內容。若完全一致（identical）直接略過。
    *   **升級處理**：若內容衝突，在終端機彈出互動詢問選單（`y` 覆蓋、`n` 保留/跳過、`d` 檢視 diff、`a` 全部覆蓋、`x` 終止）。亦可由 CLI 參數 `--force` 或 `--skip` 批次指定覆蓋或保留。
*   **[Rails Generators](https://guides.rubyonrails.org/generators.html)**
    *   **區分機制**：底層使用 Thor::Actions，不限制使用者修改。執行時狀態分為 `identical`（相同）、`create`（全新建立）、`conflict`（衝突）。
    *   **升級處理**：遇到衝突時停在 TTY Prompt，提供互動選單：`Y`（覆寫）、`n`（跳過保留）、`d`（印出 diff）、`q`（退出）；支援傳入 `-f`（force）或 `-s`（skip）。
*   **Git 屬性：[`linguist-generated`](https://git-scm.com/docs/gitattributes) 與 [`merge=` driver](https://git-scm.com/docs/gitattributes)**
    *   **區分機制**：在 `.gitattributes` 中配置 `path/** linguist-generated=true` 標記檔案為自動產生，使 GitHub PR 預設摺疊 diff 並排除在語言統計之外；透過 `path/** merge=binary` 或 `merge=ours` 標註該檔案在 git 合併時的策略。
    *   **升級處理**：`linguist-generated` 僅影響 GitHub UI 呈現；`merge=` driver 則在 `git merge` 時生效（如設為 `ours` 則自動保留本地版本，放棄上游變更）。
*   **標頭註解：[Ansible `ansible_managed`](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_templating.html) / Puppet / [chezmoi](https://www.chezmoi.io/user-guide/frequently-asked-questions/usage/#how-do-i-use-chezmoi-merge-to-resolve-conflicts)**
    *   **區分機制**：在範本開頭注入 `# Ansible managed` 等字串作為警語，標記此檔案受集中控管，無強制鎖定。chezmoi 透過 [`.chezmoiignore`](https://www.chezmoi.io/) 排除不管理的路徑。
    *   **升級處理**：Ansible/Puppet 採收斂模式，執行時依範本直接覆寫目標檔案（除非手動加 `backup: yes` 產生備份檔）；chezmoi 則在偵測到外部變更時可透過 `chezmoi merge` 呼叫三方比對工具手動合併。
*   **[Helm `helm.sh/resource-policy: keep`](https://helm.sh/docs/howto/charts_tips_and_tricks/#tell-helm-not-to-uninstall-a-resource)**
    *   **區分機制**：在 Kubernetes resource 的 annotations 中加上 `helm.sh/resource-policy: keep`。標記該資源在 release 解除安裝或模板刪除時不予刪除，脫離 Helm 生命週期。
    *   **升級處理**：升級時使用 K8s Three-way Strategic Merge Patch，若新版本移除了該資源，Helm 會因該 annotation 放棄刪除動作，使其成為叢集中的孤立受管資源（orphaned）。

---

#### 7. 三方合併的前例怎麼記「上次給你的版本」（baseline）

*   **[Copier](https://copier.readthedocs.io/en/latest/updating/)**：在專案內的 `.copier-answers.yml` 記錄上次套用的 `_commit` hash 與輸入問卷答案。升級時以該 commit 動態 render 出舊版文字作為 baseline，交由 `git merge-file` 進行三方合併。
*   **[Git merge-base](https://git-scm.com/docs/git-merge-base)**：利用 Git commit graph，以圖論演算法（Lowest Common Ancestor）動態算出兩個 commit 分支的共同祖先 commit 物件作為 baseline。
*   **[Debian conffile](https://www.debian.org/doc/debian-policy/ch-files.html#configuration-files)**：在 `/var/lib/dpkg/status` 中針對每個 conffile 記錄上次安裝時的 MD5 雜湊值（$H_{old}$）。
    *   **dpkg 狀態規則**：
        1. 本地當前雜湊 $H_{disk} == H_{old}$ 且 $H_{old} \ne H_{new}$：使用者未修改、套件更新 $\rightarrow$ 自動靜默以新版覆寫。
        2. $H_{disk} \ne H_{old}$ 且 $H_{old} == H_{new}$：使用者修改過、套件未變 $\rightarrow$ 自動靜默保留使用者版本。
        3. $H_{disk} == H_{old} == H_{new}$ 或 $H_{disk} == H_{new}$ $\rightarrow$ 無動作。
        4. $H_{disk} \ne H_{old}$ 且 $H_{old} \ne H_{new}$（雙方皆修改）$\rightarrow$ 彈出 conffile prompt（`[Y/I/N/O/D/Z]`）由使用者選擇保留、替換或查看二方 diff。
*   **[RPM `.rpmnew` / `.rpmsave`](https://rpm-packaging-guide.github.io/)**：依據 RPM DB 內原始檔案的 MD5 記錄。在 `%config(noreplace)` 下，若本地被改過且上游有新版，本地檔案維持不變，將新版寫入 `.rpmnew`；若為普通 `%config`，則將本地改過的檔案更名為 `.rpmsave`，新版寫入原檔路徑。
*   **[chezmoi state](https://www.chezmoi.io/reference/commands/state/)**：本地維護嵌入式資料庫 `chezmoistate.boltdb`，在 `entryState` bucket 中記錄每個受管檔案最後套用時的 SHA-256 雜湊與狀態，供 `chezmoi diff` 與 `apply` 判定外部變更。
*   **dpkg 規則對 vendor_kit 是否直接可用？事實分析**：
    1. **直接可用部分（三種短路路徑）**：dpkg 的三方 hash 比對邏輯在「本地未改 $\rightarrow$ 直接快進更新」與「上游未改 $\rightarrow$ 靜默保留使用者檔」的預檢完全可用，可省去不必要的 merge 計算。
    2. **不能直接沿用部分（三方文字合併）**：dpkg 只記錄 MD5 雜湊，未保存原始檔案內容，因此雙方皆改時無法執行文字級 3-way merge（無法呼叫 `git merge-file`），只能做二方 diff 與二選一覆寫。vendor_kit 若要自動合併非衝突行，必須持有 baseline 原始完整文字或 git blob。
    3. **非互動環境限制**：dpkg 在雙方皆改時依賴 TTY 終端交互輸入；在 CI 或非 TTY 的 `just` 呼叫下會卡住，vendor_kit 若採自動化模式，衝突時必須退回產生標記或分離檔。

---

#### 8. 「初始檔放到工具專屬子目錄、專案根只留 symlink 或 include」的做法與檔案支援事實

*   **既有前例**：
    *   **Docker Compose**：[Compose Specification `include:`](https://docs.docker.com/compose/compose-file/14-include/)（Compose v2.20+），根目錄 `compose.yaml` 僅需宣告 `include: [ .vendor/base/compose.yaml ]` 即可引入子目錄配置並疊加本地設定。
    *   **Justfile**：[Just `import` 指令](https://just.systems/man/en/chapter_44.html)（`just >= 1.33` 原生支援），根 `justfile` 撰寫 `import '.vendor/base/justfile'` 即可引入 recipe，支援 `set allow-duplicate-recipes` 允許根檔案複寫子檔案。
    *   **GitLab CI**：[GitLab CI `include:local`](https://docs.gitlab.com/ee/ci/yaml/includes.html)，根目錄 `.gitlab-ci.yml` 透過 `include: { local: '.vendor/base/ci.yml' }` 載入子路徑檔案。
    *   **GitHub Actions Reusable Workflows**：[Reusable Workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows)，薄 caller 工作流使用 `uses:` 調用被引用者。
*   **哪些檔案類型做得到**：
    *   `compose.yaml`：**做得到**。原生支援 `include:` 關鍵字載入子路徑；在同一 repo context 內亦支援 symlink。
    *   `justfile`：**做得到**。`just >= 1.33` 原生支援 `import 'path'` 與 `mod` 模組語法，無需建立 symlink。
    *   `pre-commit config (.pre-commit-config.yaml)`：**部分做得到**。pre-commit [官方明確拒絕支援 include 語法](https://github.com/pre-commit/pre-commit)，但 Linux/macOS 上支援將 `.pre-commit-config.yaml` 建立為指向 `.vendor/base/.pre-commit-config.yaml` 的軟連結（symlink）。
*   **哪些檔案類型做不到（必須在固定路徑且不能 include / 不能外部 symlink）**：
    *   **GitHub Actions 工作流**：**做不到完全放子目錄**。
        *   GitHub Actions runner [官方不支援 `.github/workflows/` 內的 symlink](https://docs.github.com/en/actions/sharing-automations/reusing-workflows)，放置 symlink 會被忽略或報錯。
        *   本地 Reusable Workflow（`uses: ./.github/workflows/...`）[強制規範](https://docs.github.com/en/actions/sharing-automations/reusing-workflows)目標檔案必須實體位於 `.github/workflows/` 內，不能指向外部專屬目錄（如 `.vendor/base/ci.yml`）。因此 caller 薄檔案本身必須落在 `.github/workflows/` 下。
    *   **Dockerfile**：**做不到原生 include**。
        *   Dockerfile 語法本身無 `include` 指令。
        *   若根目錄 `Dockerfile` 設為指向子目錄的 symlink，在 Docker CLI 建置時若 context 範圍或平台（如 Windows）限制，容易出現 `unable to prepare context` 或 symlink 穿越失效錯誤；一般須依賴 `docker build -f .vendor/base/Dockerfile .` 指定路徑。
    *   **.gitignore / .gitattributes / .editorconfig**：**做不到 include**。
        *   Git 與 EditorConfig 規範皆無 `include` 語法，必須實體存在於根目錄或特定目錄（Git 的 `.git/info/exclude` 為單機設定，無法隨 repo 簽入版控；若用 symlink，在跨平台或未啟用 symlink 支援的 Git for Windows 簽出時會變成純文字損壞）。

---

### 做法與前例比較表

| 做法 | 前例 | 優點 | 缺點 | 對 vendor_kit 的適用性（事實陳述） |
| :--- | :--- | :--- | :--- | :--- |
| **唯讀保護 + 清單比對** | [projen](https://projen.io/) (`.projen/files.json`) | 根目錄完全一致；強迫使用者不手動修改，避免更新被踩死 | 失去彈性；使用者要自訂必須另闢 escape hatch，與「初始檔給使用者改」原則牴觸 | projen 預設覆寫且不作三方合併，與 vendor_kit「初始檔複製給使用者自訂」模式不相符。 |
| **記錄 Baseline Commit + 三方文字合併** | [Copier](https://copier.readthedocs.io/en/latest/updating/) (`.copier-answers.yml`)、[Cruft](https://cruft.github.io/cruft/) | 能保留使用者既有客製化，自動將上游改動無縫合入；遇衝突打上標準 git 標記 | 必須保存舊 commit 或能在本地動態重現舊版檔案文字；非純文字檔無法合併 | vendor_kit 只要在版本宣告檔或狀態檔記錄上次套用的 image/commit，即可取得舊版完整文字執行 `git merge-file`。 |
| **記錄 Hash + 短路判定狀態機** | [Debian dpkg conffile](https://www.debian.org/doc/debian-policy/ch-files.html#configuration-files)、[chezmoi](https://www.chezmoi.io/reference/commands/state/) | 狀態檢測成本極低（比對三方 MD5/SHA256）；未修改情況下直接快進或跳過，零衝突干擾 | 雙方皆改時只憑 hash 無法生成 3-way merge 文字基底；預設依賴終端 TTY 交互提示 | 短路比對規則可直接引入作為 merge 前的快速路徑，但遭遇「雙方皆改」時仍需退回完整 baseline 文字檔處理。 |
| **衝突分離備份（不覆蓋使用者）** | [RPM `%config(noreplace)`](https://rpm-packaging-guide.github.io/) (`.rpmnew` / `.rpmsave`) | 永不覆蓋使用者檔案；全自動無人值守運作，不需終端 TTY 交互操作 | 專案根目錄留下殘留檔案；需使用者手動 diff 比對並手動搬移整合 | 符合 vendor_kit「永不覆蓋使用者檔案」原則；在三方合併無法自動解衝突時可作為替代落地手段。 |
| **薄封裝 Include** | [Compose `include`](https://docs.docker.com/compose/compose-file/14-include/)、[Just `import`](https://just.systems/man/en/chapter_44.html)、[GitLab CI `include`](https://docs.gitlab.com/ee/ci/yaml/includes.html) | 專案根檔案極薄（1 行）；工具本體檔案完全隔離在專屬子目錄，升級直接換子目錄不碰根檔 | 依賴工具生態語法原生支援；各工具語法不統一 | `compose.yaml` 與 `justfile` 原生支援良好；GitHub Actions、Dockerfile、.gitignore 無法透過此法達成根目錄隔離。 |
| **Symlink 指向工具子目錄** | [pre-commit symlink](https://github.com/pre-commit/pre-commit)、傳統 hook 管理 | 保持根目錄乾淨，實體檔案集中在子目錄 | 跨平台相容性差（Windows git 預設不開 symlink）；GitHub Actions 明確不支援 workflow symlink | 僅適用於 Linux/macOS 本機開發檔案，無法作為 GitHub Actions 與跨平台通用方案。 |
