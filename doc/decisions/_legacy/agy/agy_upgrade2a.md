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
