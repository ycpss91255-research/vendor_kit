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
