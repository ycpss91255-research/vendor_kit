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
