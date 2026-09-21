本報告針對 **vendor_kit** 框架設計「升級（upgrade）流程」的技術前例進行調查，包含自動化工具（Renovate、Dependabot）對自訂 TOML 檔內 `tag@digest` 的支援能力，以及現有主流工具的「手動升級指令」行為對照。

---

# 1. Renovate 對「GHCR image 以 tag@digest 記在自訂 TOML 檔」的支援

### 1.1 該用哪種 manager 與 datasource？
* **Manager**：使用 **`customManagers`**（`customType: "regex"`；在舊版本稱為 `regexManagers`）。
* **Datasource**：在 `customManagers` 中宣告 `datasourceTemplate: "docker"`。
* **說明**：Renovate 沒有專門針對 vendor_kit 的原生 manager，但其 custom regex manager 允許開發者自訂正規表達式匹配任意檔案（例如 `.version`），並透過 `datasourceTemplate: "docker"` 調用 Docker Registry API（包括 GitHub Container Registry, `ghcr.io`）來查詢最新的 tags 與 sha256 digests。
* **來源官方文件**：
  - Renovate Custom Manager (Regex): [https://docs.renovatebot.com/modules/manager/regex/](https://docs.renovatebot.com/modules/manager/regex/)
  - Renovate Docker Datasource: [https://docs.renovatebot.com/modules/datasource/docker/](https://docs.renovatebot.com/modules/datasource/docker/)

---

### 1.2 PR 長什麼樣（標題、Body、改動 Diff）？真實 PR 範例
* **PR 標題（Title）**：
  - 若有新版本（Tag 變更）：預設通常為 `Update <depName> to <newValue>` 或遵循 Conventional Commits 格式（例如 `chore(deps): update <depName> to v1.2.3`）。
  - 若 Tag 不變僅 upstream 重建（Digest 變更）：格式為 `chore(deps): update <image> docker digest to <short-sha>`。
* **PR 內容（Body）**：
  - 開頭固定為：`This PR contains the following updates:`
  - 核心為 Markdown 匯總表格：
    ```markdown
    | Package | Type | Update | Change |
    |---|---|---|---|
    | [ghcr.io/org/tool](https://ghcr.io/...) | ... | patch/digest | `v1.0.0@sha256:aaa...` -> `v1.0.1@sha256:bbb...` |
    ```
  - 下方會附帶該版本的 Release Notes、Commit 差異列表或 Renovate 設定檢查狀態。
* **檔案改動（Diff）**：
  - 在目標自訂檔案（例如 `.version`）中，直接將舊的 `tag@sha256:...` 替換為新版本的 `tag@sha256:...`。
* **真實 PR 範例**：
  - Renovate 更新 GHCR Docker 映像檔 digest 範例：[`jdx/mise` PR #6258: `chore(deps): update ghcr.io/jdx/mise:rpm docker digest to 5a96587`](https://github.com/jdx/mise/pull/6258)
  - Renovate 社群針對 regex manager 支援 digest pinning 的討論與測試案例：[Renovate Issue #10993](https://github.com/renovatebot/renovate/issues/10993) 與 [Renovate Issue #24942](https://github.com/renovatebot/renovate/issues/24942)

---

### 1.3 digest pinning 與 tag 同時更新（tag@sha256 一起換）需要什麼設定？
若要讓 Renovate 辨識 `.version` 檔中的 `name = "ghcr.io/...:tag@sha256:digest"` 並在有新 tag 時「同時換新 tag 與新 digest」，需要下列設定組合：

1. **`matchStrings` 捕獲組**：
   - 必須同時擷取 `depName`、`currentValue`（舊 tag）以及 `currentDigest`（舊 digest）。
   - 範例 regex：
     `"^(?<key>[a-zA-Z0-9_-]+)\\s*=\\s*\"(?<depName>ghcr\\.io/[^:]+):(?<currentValue>[^@\"]+)@(?<currentDigest>sha256:[a-f0-9]+)\""`
2. **`datasourceTemplate` 與 `versioningTemplate`**：
   - `"datasourceTemplate": "docker"`：指定查詢 Docker/OCI registry。
   - `"versioningTemplate": "docker"`：明確告知使用 Docker 標籤版本規範（可辨識 semver、alpine 等後綴）。
3. **`pinDigests`**：
   - 設定 `"pinDigests": true`（或全域 extends preset `"docker:pinDigests"`）。這會指示 Renovate 在偵測到 Docker 映像檔有新版本 tag 時，一併查詢並鎖定對應的 SHA256 digest。
4. **`autoReplaceStringTemplate`**：
   - 由於自訂檔案格式不在原生解析器範圍內，必須明確指定替換模板，將 `{{{newValue}}}` 與 `{{{newDigest}}}` 拼接輸出：
     ```json
     "autoReplaceStringTemplate": "{{{key}}} = \"{{{depName}}}:{{{newValue}}}@{{{newDigest}}}\""
     ```
   - 若要考慮 digest 可能是可選欄位，可使用 Handlebars 條件判斷：
     `"{{{depName}}}:{{{newValue}}}{{#if newDigest}}@{{{newDigest}}}{{/if}}"`
* **來源官方文件**：
  - Renovate Configuration: `pinDigests`: [https://docs.renovatebot.com/configuration-options/#pindigests](https://docs.renovatebot.com/configuration-options/#pindigests)
  - Renovate Configuration: `autoReplaceStringTemplate`: [https://docs.renovatebot.com/configuration-options/#autoreplacestringtemplate](https://docs.renovatebot.com/configuration-options/#autoreplacestringtemplate)
  - Renovate Template Fields: [https://docs.renovatebot.com/templates/](https://docs.renovatebot.com/templates/)

---

### 1.4 Dependabot 做不做得到（自訂檔案的 docker digest 更新）？
* **結論**：**做不到**。
* **原因**：
  1. Dependabot 只支援預先定義的套件生態系（`package-ecosystem` 清單）。
  2. 針對 Docker 生態系（`package-ecosystem: "docker"`），Dependabot 僅寫死支援掃描 `Dockerfile` 與 `docker-compose.yml`。
  3. Dependabot **完全沒有**類似 Renovate 的 Custom Regex Manager 機制，不允許使用者定義正規表達式來追蹤或更新任意非標準檔案（如自訂 TOML 檔）。
* **來源官方文件與 Issue**：
  - GitHub 官方 Dependabot 設定檔文件（支援的 package-ecosystem）：[https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file#package-ecosystem](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file#package-ecosystem)
  - Dependabot Core Issue #1290（要求支援非標準檔案的依賴更新，官方關閉並表示暫無支援規劃）：[https://github.com/dependabot/dependabot-core/issues/1290](https://github.com/dependabot/dependabot-core/issues/1290)

---

# 2. 「手動升級指令」前例對照

本節針對 Gradle `wrapper`、Batect `--upgrade`、mise `upgrade`、pre-commit `autoupdate`、Terraform `init -upgrade` 進行深度調查與比較。

### 綜合對照表

| 工具與指令 | 查最新版方式 (API/Registry/Lockfile) | 改版本檔後是否立即安裝？ | 有無「只改檔不裝」或 Dry-run？ | 能否指定單一工具/Repo 升級？ |
|---|---|---|---|---|
| **Gradle**<br>`./gradlew wrapper --gradle-version` | 查詢 Gradle 官方 API (`https://services.gradle.org/versions/...`) | **否**（只改 `gradle-wrapper.properties`，下次執行時才下載） | **本質即為只改檔**（無特定 task dry-run，但可帶全域 `-m`） | **否**（僅管理 Gradle 本身） |
| **Batect**<br>`./batect --upgrade` | 查詢 GitHub Releases API (`api.github.com/repos/batect/batect/releases/latest`) | **否**（改寫 `./batect` wrapper script，下次執行 wrapper 時才下載 jar） | **無**（無 dry-run 選項） | **否**（僅管理 Batect 本身） |
| **mise**<br>`mise upgrade` | 依各工具後端查詢（Mise Registry、Aqua、Core API、asdf plugins 等） | **是**（立即下載並安裝二進制檔；帶 `--bump` 會一併修改 `mise.toml`） | **有 dry-run**（`-n, --dry-run` 預覽，但不支援只改檔不裝） | **能**（`mise upgrade <tool>@<version>`） |
| **pre-commit**<br>`pre-commit autoupdate` | 使用 `git ls-remote` 查詢各 remote git repository 的最新 tag/commit | **否**（只改寫 `.pre-commit-config.yaml`，下次執行 `pre-commit run` 才安裝環境） | **本質即為只改檔**（無預覽的 `--dry-run`，有 issue 討論但未實作） | **能**（`--repo <repo_url>`，可重複指定） |
| **Terraform**<br>`terraform init -upgrade` | 查詢 Terraform Registry API (`registry.terraform.io`) 與 Module Git sources | **是**（立即下載 Provider/Module 至 `.terraform/`，並更新 `.terraform.lock.hcl`） | **無**（`init` 無 dry-run；若要只更新 lock 檔不下載本機執行環境可改用 `providers lock`） | **否**（`init -upgrade` 一律升級全部符合範圍者；手動改配置檔才能限縮） |

---

### 詳細工具分析與官方來源

#### (1) Gradle `wrapper --gradle-version`
* **查最新版方式**：支援傳入標籤（如 `--gradle-version latest`），底層會請求 Gradle 官方 API 端點：`https://services.gradle.org/versions/current` 或 `https://services.gradle.org/versions/all` 獲取發布版本與 distribution URL。
* **是否立即安裝**：**否**。執行 `./gradlew wrapper --gradle-version <version>` 時，是由目前既有的 Gradle daemon 執行 wrapper task，僅負責將新的版本網址與 SHA256 checksum 寫入專案的 `gradle/wrapper/gradle-wrapper.properties`（以及產生 wrapper 腳本）。新版本的 Gradle 實體不會在此時下載，而是在**下次執行 `./gradlew`** 時，由 wrapper 腳本檢查本機快取目錄（`~/.gradle/wrapper/dists/`）缺失後自動下載並解壓縮。
* **只改檔不裝 / Dry-run**：該指令本質就是「只改檔」，安裝被延遲到 runtime。若要檢視任務是否會執行，僅有 Gradle 內建的全域 dry-run 參數（`./gradlew wrapper -m` 或 `--dry-run`）。
* **單一升級**：**否**。Gradle Wrapper 僅專門管理 Gradle 構建工具本體版本。
* **官方文件**：
  - Upgrading the Gradle Wrapper: [https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper)
  - Gradle Versions API 規格與釋出文件: [https://docs.gradle.org/current/release-notes.html](https://docs.gradle.org/current/release-notes.html)

#### (2) Batect `--upgrade`
* **查最新版方式**：Batect 內建更新檢查器會打 GitHub Releases API（`https://api.github.com/repos/batect/batect/releases/latest`）比對最新版本號。
* **是否立即安裝**：**否**。`./batect --upgrade` 的動作是從官方 GitHub Release 下載最新的 wrapper 腳本，覆蓋本機專案根目錄的 `./batect` 與 `./batect.cmd`。實際的 Batect Java 執行檔（JAR）是在使用者**下次執行 `./batect`** 時，由新 wrapper 自動下載至 `~/.batect/cache/`。
* **只改檔不裝 / Dry-run**：**無**。Batect 未提供 `--dry-run` 選項給 `--upgrade` 指令。
* **單一升級**：**否**。Batect 僅管理自身 wrapper 與執行檔。
* **官方文件**：
  - Batect CLI Reference & Upgrading: [https://batect.dev/using-batect/command-line-interface/](https://batect.dev/using-batect/command-line-interface/)
  - Batect Source Repository: [https://github.com/batect/batect](https://github.com/batect/batect)

#### (3) mise `upgrade`
* **查最新版方式**：依據所管理的工具來源不同，向對應的 Registry/Backend 查詢最新版本（例如 Mise Registry API、Aqua Registry、asdf plugin 遠端 repo 的 `list-all`、或 GitHub Releases）。
* **是否立即安裝**：**是**。`mise upgrade` 預設會在背景或前景立即下載安裝符合版本條件的新版本二進制檔至 `~/.local/share/mise/installs/`。若加上 `--bump` 參數，它會升級至絕對最新版並**同步改寫 `mise.toml`**。
* **只改檔不裝 / Dry-run**：
  - 支援 **`-n, --dry-run`**：僅輸出會執行升級的工具與版本差異，不執行實際安裝與寫入。
  - 沒有「只改寫 `mise.toml` 但不安裝二進制檔」的專門開關（執行 `--bump` 即伴隨安裝）。
* **單一升級**：**能**。支援指定工具語法：`mise upgrade <tool>@<version>`（例如 `mise upgrade node@20`）或使用 `--exclude` 排除特定工具。
* **官方文件**：
  - mise upgrade CLI Document: [https://mise.jdx.dev/cli/upgrade.html](https://mise.jdx.dev/cli/upgrade.html)

#### (4) pre-commit `autoupdate`
* **查最新版方式**：透過內部執行 `git ls-remote <repo_url>`，直接向各個 Hook 宣告的遠端 Git Repository 查詢最新的 git tag 或預設分支 commit。
* **是否立即安裝**：**否**。`pre-commit autoupdate` 僅修改專案內的 `.pre-commit-config.yaml` 檔案（更新各 repo 的 `rev:` 欄位）。它**完全不會**在執行當下建立新的 virtualenv 或編譯環境，而是延遲至**下次執行 `pre-commit run` 或 git hook 觸發時**才自動拉取並初始化該環境。
* **只改檔不裝 / Dry-run**：
  - 該指令本身即為「只改檔不裝環境」。
  - 但針對「只看有什麼版本更新，連 `.pre-commit-config.yaml` 都不改」的 Dry-run 預覽功能：**無**（社群 Issue #2785 曾討論過，但尚未實作）。
* **單一升級**：**能**。支援 `--repo REPO` 參數（例如 `pre-commit autoupdate --repo https://github.com/psf/black`），可重複使用以指定升級特定 repo。
* **官方文件**：
  - pre-commit autoupdate Reference: [https://pre-commit.com/#pre-commit-autoupdate](https://pre-commit.com/#pre-commit-autoupdate)
  - Dry-run feature discussion (Issue #2785): [https://github.com/pre-commit/pre-commit/issues/2785](https://github.com/pre-commit/pre-commit/issues/2785)

#### (5) Terraform `init -upgrade`
* **查最新版方式**：
  - Provider：透過 Terraform Registry API（預設 `https://registry.terraform.io/v1/providers/...`）查詢符合配置檔版本約束的最新釋出。
  - Module：查詢 Terraform Registry 或 Git/HTTP 來源。
* **是否立即安裝**：**是**。`terraform init -upgrade` 會立即忽略既有的 `.terraform.lock.hcl` 鎖定版本，下載最新的 provider 外掛程式與 module 原始碼至 `.terraform/` 暫存目錄中，並同步將新的版本與 checksum 寫入 `.terraform.lock.hcl`。
* **只改檔不裝 / Dry-run**：
  - `terraform init` **沒有 dry-run 選項**。
  - **對照指令**：若目的是「只更新版本鎖定檔（`.terraform.lock.hcl`），不安裝本機外掛」，Terraform 另外提供 **`terraform providers lock`** 指令，可在不安裝執行檔的情況下查詢 Registry 並更新 lockfile。
* **單一升級**：
  - `terraform init -upgrade` **否**（無法指定單一 provider，會全面升級所有相容依賴；若要限縮必須手動編輯 `.tf` 檔的 version constraint）。
  - （補充：`terraform providers lock [PROVIDER...]` 則**可以**指定單一 provider 寫入 lockfile）。
* **官方文件**：
  - Command: init (`-upgrade` flag): [https://developer.hashicorp.com/terraform/cli/commands/init#upgrade](https://developer.hashicorp.com/terraform/cli/commands/init#upgrade)
  - Command: providers lock: [https://developer.hashicorp.com/terraform/cli/commands/providers/lock](https://developer.hashicorp.com/terraform/cli/commands/providers/lock)

---

### 對 vendor_kit 設計的借鏡意涵
1. **模式選擇**：
   - **Gradle / Batect / pre-commit** 採用「升級指令只負責改版本檔/Wrapper 宣告，執行時才 Lazy 下載容器/執行檔」的架構。這與 vendor_kit「主機只有 Docker+git+just、升級只改 `.version` 一行、下次執行 `just` 才自動安裝 `.<name>/`」的設計理念完全一致。
2. **單一升級能力**：
   - 像 pre-commit（`--repo`）與 mise（`<tool>`）都支援「單一目標升級」，vendor_kit 在設計 `just upgrade [name]` 時，具備極佳的直覺性與前例支撐。
3. **安全審查流程**：
   - 延遲安裝（只改檔）讓使用者在升級後能透過 `git diff` 審查版本變化，並在正式運行前先跑 `just diff` 檢查範本變更，符合「工具不自動任意改寫使用者程式碼」的原則。
本調查針對 `vendor_kit` 升級與回退流程，調研現行主流工具（Batect、Gradle Wrapper、rustup、uv、Bazelisk、Nix Flakes、Terraform）的架構模式與前例，並提供具體流程建議。

---

# 3. 「啟動器自我升級」前例研究

當「舊版啟動器」負責升級到新版，若新版需要新參數、新設定格式或新通訊協定時，現有工具採用了不同的演進模式：

### (1) Batect：Wrapper 腳本覆寫更新
* **機制**：
  專案根目錄的 `./batect`（或 Windows 下的 `batect.cmd`）是一個被納入 Git 追蹤的 shell 啟動包裝器（wrapper script），內部包含 `VERSION="x.y.z"`。
  當使用者執行 `./batect --upgrade` 時，啟動器會連線至 GitHub Releases 下載最新版的 `./batect` wrapper script 並**直接覆寫本機的 wrapper 腳本**。
* **應對新參數/新格式**：
  若新版本需要新的環境變數、Docker 旗標或 JVM 參數，這些新邏輯會直接包含在被替換下載的新 wrapper 腳本內。下次執行時，新版 wrapper 腳本才會負責下載並啟動對應的新版 Batect 運行檔。
* **來源連結**：
  * [Batect Documentation - Upgrading Batect](https://batect.dev/docs/getting-started/tutorial#upgrading-batect)
  * [GitHub: batect/batect](https://github.com/batect/batect)
  * [Renovate batect-wrapper Manager](https://docs.renovatebot.com/modules/manager/batect-wrapper/)

---

### (2) Gradle Wrapper：兩階段執行（Two-stage execution）
* **機制**：
  升級指令為 `./gradlew wrapper --gradle-version <version>`。官方與社群的最佳實踐均要求**連續執行兩次（run twice）**：
  1. **第一階段（First Run）**：由當前舊版 Gradle 執行 `wrapper` task。這一步只會將新的版本號寫入 `gradle/wrapper/gradle-wrapper.properties`，但此時生成的 `gradle-wrapper.jar` 與 `gradlew` 腳本仍然是由舊版 Gradle 生成的。
  2. **第二階段（Second Run）**：再次執行 `./gradlew wrapper` 時，啟動腳本讀取更新後的屬性檔，自動下載並啟動「新版 Gradle 發行版」。此時由**新版 Gradle** 重新產出並覆寫 `gradle-wrapper.jar` 與 `gradlew` 啟動腳本。
* **應對新參數/新格式**：
  舊版啟動器不需要預先知道新版啟動腳本的所有細節，只需負責把「目標版本」寫入屬性檔；隨後由新版執行引擎接管，重新產出符合新規格的啟動器與二進制 Jar 包。
* **來源連結**：
  * [Gradle User Manual - Upgrading the Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper)
  * [Gradle 1.6 Release Notes: Multi-process safe wrapper upgrading](https://docs.gradle.org/1.6/release-notes.html)

---

### (3) `rustup self update` 與 `rustup update` 的關係與順序
* **關係與預設順序**：
  * `rustup update`：預設會**先同步並升級所有已安裝的 Rust toolchains**（`info: syncing channel updates for ...`），在工具鏈升級完成後，再檢查並執行 `rustup` 本身的自我升級（`info: checking for self-updates`）。可透過 `--no-self-update` 或設定 `RUSTUP_AUTO_SELF_UPDATE=disable` 關閉自我升級。
  * `rustup self update`：獨立只升級 `rustup` 管理器本體，不更動 toolchains。
* **新格式/新參數衝突時的處理**：
  * Rust 的發布清單帶有 `manifest-version`（目前主流為 v2）。若未來的清單格式或新組件（如早期新增 `rust-analyzer` 或支援新 target架構）超出舊版 rustup 的解析能力，舊版 rustup 會直接報錯：`error: manifest version '{0}' is not supported`。
  * 因此在架構改版或遇到解析失敗時，官方與社群的標準修復指引是**「先手動執行 `rustup self update`，換上新版啟動器，再執行 `rustup update`」**。
* **來源連結**：
  * [The Rustup Book - Basics](https://rust-lang.github.io/rustup/basics.html)
  * [GitHub rust-lang/rustup: errors.rs (UnsupportedVersion error)](https://github.com/rust-lang/rustup/blob/master/src/errors.rs)
  * [GitHub rust-lang/rustup: rustup_mode.rs](https://github.com/rust-lang/rustup/blob/master/src/cli/rustup_mode.rs)

---

### (4) `uv self update` 與 `uv tool upgrade` 的關係
* **關係**：
  * `uv self update`：專門更新 `uv` 執行檔本體（重新觸發 installer 並更新 PATH）。
  * `uv tool upgrade <tool>`：專門更新透過 `uv tool install` 安裝於使用者隔離虛擬環境（`~/.local/share/uv/tools/`）中的 Python CLI 工具。
  * 兩者完全**解耦（Decoupled）**，執行 `uv tool upgrade` 不會自動檢查或升級 `uv` 本身。
* **應對新參數/新格式**：
  `uv tool` 仰賴每個 tool 目錄內的 environment receipt 來追蹤元資料。如果新版 tool 需要新的隔離機制或依賴解析格式，是由升級後的 `uv` 二進制來處理相容性轉換。
* **來源連結**：
  * [uv CLI Reference - uv self update](https://docs.astral.sh/uv/reference/cli/#uv-self-update)
  * [uv CLI Reference - uv tool upgrade](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade)
  * [uv Documentation - Tools Guide](https://docs.astral.sh/uv/guides/tools/)

---

### (5) 順序總結：「先換自己再換工具」vs「先換工具再換自己」

| 策略 | 代表工具 | 優勢 | 潛在問題 | 適用情境 |
| :--- | :--- | :--- | :--- | :--- |
| **先換自己再換工具**<br>*(Manager/Launcher First)* | **Batect** (`--upgrade`)<br>**rustup** (遇到 manifest 升級時) | 確保啟動器具備最新參數、協定解析能力與旗標支援，絕不傳遞舊參數給新工具。 | 若新啟動器有 breaking change，尚未升級工具前啟動器可能先行失效。 | 工具依賴啟動器傳入執行參數、或版本宣告檔格式有結構改變時。 |
| **先換工具再換自己**<br>*(Tool First / 兩階段)* | **Gradle Wrapper** | 啟動腳本由新工具負責「自我生成」，專案內不需要維護獨立的啟動器升級邏輯。 | 舊啟動器若遇到無法解析的新格式會卡死，需分兩次執行（第一階段改宣告、第二階段由新工具替換腳本）。 | 啟動腳本本質上就是工具發行版的一個「附屬產物」時。 |

> **對 vendor_kit 的結論**：
> `vendor_kit` 的啟動器（`.vendor_kit/` 內的 recipe）是由 `vendor_kit` 映像檔產出的。因此應採**「先換自己再換工具」**：在更新 `.version` 後，下次執行 `just` 時，啟動器必須先比對 `vendor_kit` 核心版本，若版本更新，先啟動新版 `vendor_kit` 容器刷新 `.vendor_kit/` 中的啟動器 recipe，再由新版 recipe 接管工具的執行與升級。

---

# 4. 回退：只改版本檔就能回退的前例研究

調研當使用者僅透過 Git 或文字編輯器將版本宣告檔改回舊版時，工具是否能立即生效，或是否需要額外指令：

### (1) Bazelisk：`.bazelversion`
* **回退行為**：**不需要任何額外指令即可生效**。
* **機制**：
  Bazelisk 是 Bazel 的啟動器封裝。每次在終端機輸入 `bazel <command>` 時，Bazelisk 都會在執行期讀取專案目錄下的 `.bazelversion` 檔案。若使用者透過 `git revert` 或編輯器將版本改為舊版（例如 `7.0.0` 改回 `6.4.0`），下次執行 `bazel` 時，Bazelisk 就會直接檢查本機快取是否有該舊版；若無則自動下載舊版並執行。
* **來源連結**：
  * [GitHub: bazelbuild/bazelisk README](https://github.com/bazelbuild/bazelisk)
  * [Bazel Documentation: Installing Bazel using Bazelisk](https://bazel.build/install/bazelisk)

---

### (2) Nix Flakes：`flake.lock`
* **回退行為**：**不需要任何額外指令即可生效**。
* **機制**：
  Nix 是宣告式且內容定址（content-addressed）的套件管理系統。當使用者透過 `git checkout -- flake.lock` 或 `git revert` 將 `flake.lock` 還原為舊提交時，下次執行 `nix build` 或 `nix develop` 時，Nix 會直接解析被鎖定的舊版 commit SHA 與 narHash，並直接從本機 `/nix/store`（或遠端 binary cache）還原出舊版環境。除非使用者顯式輸入 `nix flake update`，否則 Nix 嚴格遵守 `flake.lock`，改回即生效。
* **來源連結**：
  * [Nix Reference Manual - nix flake](https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-flake.html)
  * [Nix Documentation - Flakes Guide](https://nix.dev/concepts/flakes.html)

---

### (3) Terraform：`.terraform.lock.hcl`
* **能否降級？**：**可以降級，但不能「只改 lock 檔」就直接使用，必須搭配指令重新初始化**。
* **機制與限制**：
  1. **需要額外指令**：Terraform 執行時（如 `terraform plan` / `apply`）不會自動下載或替換已經下載到本機 `.terraform/providers/` 快取目錄中的二進制外掛。因此若透過 Git 把 `.terraform.lock.hcl` 還原到舊版，**必須顯式執行 `terraform init`** 才會重新驗證並下載舊版 provider。
  2. **降級操作規範**：
     * 若在 `.tf` 檔指定了較低版本約束，只跑 `terraform init` 會噴錯（提示 lock file 與設定約束不一致）。
     * 正確降級指令為：**`terraform init -upgrade`**（官方設計中 `-upgrade` 代表「重新評估約束並更新 lock 檔」，當約束調低時即執行降級）。
     * 另外，若要手動為特定平台重新鎖定 provider 雜湊，官方提供了專門指令：`terraform providers lock`。
* **來源連結**：
  * [HashiCorp Terraform - Dependency Lock File](https://developer.hashicorp.com/terraform/language/files/dependency-lock)
  * [HashiCorp Terraform CLI - terraform init](https://developer.hashicorp.com/terraform/cli/commands/init)
  * [HashiCorp Terraform CLI - terraform providers lock](https://developer.hashicorp.com/terraform/cli/commands/providers/lock)

---

# 5. 建議的 upgrade 流程

基於上述前例（Bazelisk 的「每次執行即時比對版本檔自動就緒」、Gradle 的「新舊版本過渡與兩階段刷新」、Batect 的「不自動更動使用者檔」原則），為 `vendor_kit` 設計以下四條升級與回退路徑。

各步驟的操作者角色定義：
* **機器人 (Renovate)**：自動發 PR 的機器人。
* **使用者 (User)**：開發者本人。
* **啟動器 (Launcher)**：Host 上的 `just` 與 `.vendor_kit/` 生成的 recipe。
* **容器 (Container)**：Docker 運行的工具 dist 容器或 vendor_kit 容器。

---

### 路徑一：Renovate 自動 PR 路徑
1. **機器人 (Renovate)**：
   偵測到 GHCR 上有新版 tool 或 vendor_kit image，向專案發出 PR，修改 `.version` 檔中對應工具的行（包含最新 digest 與 tag）。
2. **使用者 (User)**：
   在本地 checkout 該 PR 分支（或在 GitHub 合併後於本地 `git pull`）。
3. **使用者 (User)**：
   執行日常指令（例如 `just <name>`）或 `just diff <name>`。
4. **啟動器 (Launcher)**：
   讀取 `.version`，比對本機快取目錄 `.<name>/.installed_version`：
   * 發現版本不一致，呼叫 **容器 (Container)** 從新版 image 提取二進制/dist 檔案，原子更新至本機 `.<name>/`。
   * 將最新範本寫入 `.<name>/template/`（暫存區，不進 git）。
5. **使用者 (User)**：
   執行 `just diff <name>`。
6. **啟動器 (Launcher)**：
   調用三方 diff 工具（比對：`.vendor_kit/baseline/<name>/` 舊基準 vs `.<name>/template/` 新範本 vs 使用者目前設定檔）。
7. **使用者 (User)**：
   檢視 diff，手動將需要採納的範本變更合併到自己的專案設定檔中（維持「工具不自動改使用者檔」原則）。
8. **使用者 (User)**：
   執行 `just accept <name>`。
9. **啟動器 (Launcher)**：
   將 `.<name>/template/` 複製覆寫至 `.vendor_kit/baseline/<name>/`，更新基準副本。
10. **使用者 (User)**：
    執行 `git commit`，提交設定檔變更與 `.vendor_kit/baseline/<name>/`。

---

### 路徑二：`just upgrade <name>` 手動升級路徑
1. **使用者 (User)**：
   執行 `just upgrade <name>`（或可選指定版本 `just upgrade <name> v2.0.0`）。
2. **啟動器 (Launcher)**：
   透過 Docker / 遠端 API 查詢 GHCR 上 `<name>-dist` 的最新 digest 與 tag，將其寫入專案根目錄的 `.version`。
3. **啟動器 (Launcher)**：
   呼叫 **容器 (Container)** 拉取新 image，將二進制檔案解壓至 `.<name>/`，並將新版範本置於暫存區。
4. **使用者 (User)**：
   執行 `just diff <name>` 檢視設定檔與新範本差異。
5. **使用者 (User)**：
   手動調整自己的專案設定檔。
6. **使用者 (User)**：
   執行 `just accept <name>`。
7. **啟動器 (Launcher)**：
   將新範本更新至 `.vendor_kit/baseline/<name>/`。
8. **使用者 (User)**：
   執行 `git commit`，提交 `.version`、`.vendor_kit/baseline/<name>/` 與個人設定檔。

---

### 路徑三：vendor_kit 自身升級路徑（`.version` 中的 `vendor_kit = ...`）
*核心原則：採「先換自己再換工具」，由新版 vendor_kit 容器刷新 host 上的 recipe*
1. **使用者 (User)** 或 **機器人 (Renovate)**：
   更新 `.version` 中的 `vendor_kit = "ghcr.io/...:tag@sha256:..."`。
2. **使用者 (User)**：
   執行任何 `just` 指令（例如日常的 `just test` 或 `just update`）。
3. **啟動器 (Launcher, 舊版 recipe)**：
   在執行任務前觸發 self-check hook，比對 `.version` 中的 `vendor_kit` 版本與 `.vendor_kit/.installed_version`：
   * 發現版本變更，啟動器暫停目前任務，調用 **容器 (Container, 新版 vendor_kit image)**。
4. **容器 (Container, 新版 vendor_kit)**：
   執行自我安裝邏輯，將新版的 launcher recipe、共用腳本覆寫至 `.vendor_kit/`，並寫入新的 `.vendor_kit/.installed_version`。
5. **啟動器 (Launcher)**：
   自動使用新載入的 recipe 繼續完成原本使用者呼叫的任務（或提示使用者重新執行一次指令，類似 Gradle 的過渡）。
6. **使用者 (User)**：
   執行 `git commit`，將更新後的 `.vendor_kit/` 啟動器 recipe 提交進 Git。

---

### 路徑四：回退路徑（Rollback）
*核心原則：效法 Bazelisk 與 Nix，宣告式檔案改回即生效，使用者無須記憶複雜 rollback 指令*
1. **使用者 (User)**：
   透過 Git 還原 `.version`（例如 `git checkout HEAD~1 -- .version` 或 `git revert <commit>`）。
2. **使用者 (User)**：
   執行一般的 `just <name>`（無需執行特殊回退指令）。
3. **啟動器 (Launcher)**：
   在啟動前偵測到本機現存的 `.<name>/` 版本高於（或不等於）`.version` 所指定的舊版 image digest：
   * 啟動器調用 **容器 (Container, 舊版 image)**。
   * 自動以舊版 image 重新覆寫解壓 `.<name>/`，還原回舊版工具環境。
4. **啟動器 (Launcher)**：
   以舊版工具完成使用者指令。
5. **使用者 (User)**（可選）：
   若使用者在升級時已經跑過 `just accept`，使用者只需執行 `git checkout HEAD~1 -- .vendor_kit/baseline/<name>/` 與自己的設定檔，即可將基準與設定檔一併還原。
