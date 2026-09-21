# vendor_kit 升級（upgrade）流程設計前例研究 Brief

本報告針對 `vendor_kit` 的架構需求（自訂 `.version` TOML 檔、記錄 `ghcr.io/<org>/<name>:<tag>@sha256:<digest>`、主機僅有 Docker/git/just、更新即改檔且下次執行 lazy 安裝、原則為不自動更動使用者檔案僅顯示 diff），進行自動化機器人支援度與業界既有工具升級指令的查證與比較。

---

## 1. Renovate 對「自訂 TOML 檔 + GHCR tag@digest」的支援

### (1) Manager 類型與設定方式
Renovate 原生提供自訂管理器功能，針對非標準檔案可使用 **Regex Manager**（設定陣列 `customManagers`，指定 `customType: "regex"`），並搭配 `datasourceTemplate: "docker"` 來查詢 GHCR（GitHub Container Registry）等 OCI 相容 Registry（[Renovate Custom Manager Regex 文件](https://docs.renovatebot.com/modules/custom-manager/regex/)、[Renovate Docker Datasource 文件](https://docs.renovatebot.com/modules/datasource/docker/)）。

在 `renovate.json` 中，必須透過 Named Capture Group 擷取相應欄位：
- `depName`：識別該工具的名稱（例如 TOML 的 key，如 `vendor_kit`）。
- `packageName`：實際向 Docker Registry 查詢的完整 Image 路徑（如 `ghcr.io/org/vendor_kit`）。
- `currentValue`：當前的版本 Tag（如 `0.2.0`）。
- `currentDigest`：當前鎖定的 SHA256 雜湊（如 `sha256:9c1a...`）。

#### `renovate.json` 完整設定範例
```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "customManagers": [
    {
      "customType": "regex",
      "managerFilePatterns": ["(^|/)\\.version$"],
      "matchStrings": [
        "(?<depName>[a-zA-Z0-9_-]+)\\s*=\\s*\"(?<packageName>ghcr\\.io/[^:]+):(?<currentValue>[^@\"]+)@(?<currentDigest>sha256:[a-f0-9]+)\""
      ],
      "datasourceTemplate": "docker",
      "versioningTemplate": "docker",
      "autoReplaceStringTemplate": "{{{depName}}} = \"{{{packageName}}}:{{{newValue}}}@{{{newDigest}}}\""
    }
  ]
}
```
（[Renovate Regex Manager Templates 說明](https://docs.renovatebot.com/modules/custom-manager/regex/)）

---

### (2) 產生的 PR 行為（Tag 與 Digest 是否分開）
- **新版本釋出（Tag 改變）**：Renovate 會在同一個 PR 內**同時更新 Tag 與 Digest**，不會拆成兩個 PR。因為當 Regex 同時捕獲 `currentValue` 與 `currentDigest`，Renovate 在比對到新 Tag（`newValue`）時，會一併向 Registry 解析該 Tag 最新對應的 Image SHA256（`newDigest`），並透過 `autoReplaceStringTemplate` 完成整行替換（[Renovate pinDigests 配置文件](https://docs.renovatebot.com/configuration-options/#pindigests)）。
- **Tag 不變但 Image 重建（Digest 改變）**：若上游更新了相同 Tag 的 Image 內容，Renovate 的更新類型為 `digest`，此時會開立單獨的 PR 只更新 Digest（[Renovate Update Types 說明](https://docs.renovatebot.com/configuration-options/#matchupdatetypes)）。

---

### (3) Digest Pinning 與同步更新之關鍵設定
- **`currentDigest` 與 `currentDigestTemplate`**：在 Regex Manager 中，正規表達式必須包含 `(?<currentDigest>sha256:[a-f0-9]+)`。若沒有抓取 currentDigest，Renovate 會誤以為此相依性未固定 Digest，而無法計算出 `newDigest`（[Renovate Regex 命名群組指南](https://docs.renovatebot.com/modules/custom-manager/regex/)）。
- **`autoReplaceStringTemplate`**：Regex Manager 預設僅替換 `currentValue`。當需要將整行改寫為新 Tag 伴隨新 Digest 時，必須明確定義此模板（例如 `{{{depName}}} = "{{{packageName}}}:{{{newValue}}}@{{{newDigest}}}"`），利用 Handlebars 語法（三重大括號避免跳脫）產生更新字串（[Renovate autoReplaceStringTemplate 文件](https://docs.renovatebot.com/modules/custom-manager/regex/)）。
- **`pinDigests`**：若原本檔案中的字串「沒有」`@sha256:...`，開啟 `"pinDigests": true`（或套用 `docker:pinDigests` 預設集）會促使 Renovate 主動開 PR 補上 Digest；若原本已寫入 Digest，Renovate 會自動維持 digest pinning 行為（[Renovate pinDigests 配置文件](https://docs.renovatebot.com/configuration-options/#pindigests)）。

---

## 2. Dependabot 的支援評估與限制

- **生態系限制**：Dependabot 目前**完全無法**支援自訂 TOML 檔案中的 Docker Image 更新。在官方規格中，`package-ecosystem: "docker"` 僅支援掃描 `Dockerfile` 以及 Docker Compose 檔（如 `docker-compose.yml` 或 `compose.yaml`）（[GitHub Docs: dependabot.yml 設定選項](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file#package-ecosystem)）。
- **自訂檔案支援相關 Issue**：
  - 核心倉庫長期存在的 Issue **#1290**（*Support for dependency updates in arbitrary configuration files*）曾廣泛討論是否能如 Renovate 般支援任意自訂檔案或自訂 Regex，官方最終以維護成本高、Regex 解析脆弱且架構為固定套件解析器為由關閉該需求（[GitHub Issue dependabot-core#1290](https://github.com/dependabot/dependabot-core/issues/1290)）。
  - 使用者在 Issue **#7885** 中討論版本過濾與非標準格式規則時，官方維護者亦多次重申 Dependabot 傾向維持強型別的語言 AST / 官方 Manifest 解析，不開放通用 Regex 管理器（[GitHub Issue dependabot-core#7885](https://github.com/dependabot/dependabot-core/issues/7885)）。
- **結論**：若專案需使用外部 Bot 自動更新 `.version`，**Renovate 是唯一具備原生 Regex Manager 支援的成熟選擇**。

---

## 3. 「手動升級指令」七大工具前例對照

各工具在 (a) 查最新版方式、(b) 改版本檔後是否立即安裝、(c) 是否有 dry-run 或只改檔不裝選項、(d) 能否指定單一工具或全部的對照如下：

### 1. Gradle (`gradle wrapper --gradle-version X` / `latest`)
- **(a) 查最新版方式**：當使用 `--gradle-version latest` 時，Gradle Client 會向官方 REST API 端點 `https://services.gradle.org/versions/current` 發送 HTTP GET 請求，解析 JSON 回傳之 `version` 與 `downloadUrl`（[Gradle Wrapper 使用指南](https://docs.gradle.org/current/userguide/gradle_wrapper.html)、[Gradle Services API 端點](https://services.gradle.org/versions/current)）。
- **(b) 改版本檔後是否立即安裝**：**否**。執行 `wrapper` 任務只會改寫專案內的 `gradle/wrapper/gradle-wrapper.properties`（修改 `distributionUrl`）與更新 `gradlew`、`gradle-wrapper.jar`。新版 Gradle 的完整二進位發行包（zip）是在**下一次執行 `./gradlew` 時才會觸發下載與解壓縮**（[Gradle Wrapper 官方文件](https://docs.gradle.org/current/userguide/gradle_wrapper.html)）。
- **(c) Dry-run / 只改檔不裝**：Gradle Wrapper 本質即為「**只改版本檔與啟動腳本，不下載完整執行檔**」。它沒有專門預覽版本文字差異的 `--dry-run` 參數（雖然 Gradle 有全域 `-m / --dry-run` 略過 Task 執行，但此時 wrapper 檔不會被寫入）（[Gradle CLI 參數手冊](https://docs.gradle.org/current/userguide/command_line_interface.html)）。
- **(d) 指定單一工具或全部**：僅限 Gradle 本身單一工具（[Gradle Wrapper 使用指南](https://docs.gradle.org/current/userguide/gradle_wrapper.html)）。

---

### 2. Batect (`./batect --upgrade`)
- **(a) 查最新版方式**：Batect 在啟動與執行升級時，會向 GitHub Releases API（`https://api.github.com/repos/batect/batect/releases/latest`）查詢最新 release 標籤（[Batect CLI 說明文件](https://batect.dev/docs/reference/cli)、[Batect GitHub Repository](https://github.com/batect/batect)）。
- **(b) 改版本檔後是否立即安裝**：**否（改檔後延遲安裝）**。`./batect --upgrade` 會從 GitHub Release 下載最新的 `batect` 與 `batect.cmd` 啟動腳本並直接替換本地專案中的 wrapper 檔案。新版對應的 Batect JAR 檔並不會在升級當下預載，而是**在下一次執行 `./batect <task>` 時由 wrapper 腳本自動下載到 `~/.batect/cache/`**（[Batect 官方文件：升級機制](https://batect.dev/docs/reference/cli)）。
- **(c) Dry-run / 只改檔不裝**：**無 `--dry-run` 選項**。執行即直接改寫本地 wrapper 腳本（[Batect CLI 說明文件](https://batect.dev/docs/reference/cli)）。
- **(d) 指定單一工具或全部**：僅限 Batect 本身單一工具（註：Batect 目前已停止維護）（[Batect 官方儲存庫公告](https://github.com/batect/batect)）。

---

### 3. mise (`mise use` / `mise upgrade` 含 `--dry-run`, `--bump`)
- **(a) 查最新版方式**：依據工具的後端外掛類型查詢：core/ubi/aqua 外掛查詢 GitHub Releases API、asdf 外掛執行 `git ls-remote --tags`、npm/cargo 查詢各語言 Registry API（[mise Core Plugins 文件](https://mise.jdx.dev/plugins/)）。
- **(b) 改版本檔後是否立即安裝**：
  - `mise use <tool>`：會改寫 `mise.toml` 並且**立即下載安裝**該工具（[mise use CLI 文件](https://mise.jdx.dev/cli/use.html)）。
  - `mise upgrade`：預設在符合設定檔的 semver 範圍內升級工具，**會立即下載安裝**，但預設**不改寫** `mise.toml`（[mise upgrade CLI 文件](https://mise.jdx.dev/cli/upgrade.html)）。
  - `mise upgrade --bump`：會將 `mise.toml` 內的版本號改寫為最新版，並**同時立即下載安裝**（[mise upgrade CLI 文件](https://mise.jdx.dev/cli/upgrade.html)）。
- **(c) Dry-run / 只改檔不裝**：
  - 有 `--dry-run`：執行 `mise upgrade --bump --dry-run` 會印出可升級的工具與新舊版本比對，**完全不改動檔案、亦不安裝二進位檔**（[mise upgrade CLI 文件](https://mise.jdx.dev/cli/upgrade.html)）。
  - 只改檔不裝：mise 無直接原生指令做到「改寫 `mise.toml` 但抑制安裝」，因為其設計理念為 `use` / `upgrade` 必須確保執行檔在本地可用（[mise use CLI 文件](https://mise.jdx.dev/cli/use.html)）。
- **(d) 指定單一工具或全部**：皆可。可指定個別工具（如 `mise upgrade node`、`mise use go@latest`），若省略參數則針對設定檔內的所有工具批次升級（[mise upgrade CLI 文件](https://mise.jdx.dev/cli/upgrade.html)）。

---

### 4. pre-commit (`pre-commit autoupdate` 含 `--repo`, `--freeze`)
- **(a) 查最新版方式**：使用 Git 協定直接向各 Hook 儲存庫遠端執行 `git ls-remote --tags <repo>` 查詢最新的 Git Tag；若使用 `--bleeding-edge` 則查詢預設分支之 HEAD Commit（[pre-commit autoupdate 官方文件](https://pre-commit.com/#pre-commit-autoupdate)）。
- **(b) 改版本檔後是否立即安裝**：**否**。`pre-commit autoupdate` **只會改寫 `.pre-commit-config.yaml`** 中的 `rev:` 欄位。各 Hook 的虛擬環境（Python venv / Node / Go 等）**完全不會在 autoupdate 時建立**，而是在**下次執行 `pre-commit run` 時才被惰性安裝**（[pre-commit autoupdate 官方文件](https://pre-commit.com/#pre-commit-autoupdate)）。
- **(c) Dry-run / 只改檔不裝**：
  - 官方 `pre-commit` **未提供 `--dry-run` 選項**（社群因而開發了第三方外掛 `pre-commit-update` 補充 `--dry-run` 功能）（[PyPI: pre-commit-update](https://pypi.org/project/pre-commit-update/)）。
  - 由於原生指令**預設就是「只改設定檔不裝環境」**，官方推薦透過 `git diff .pre-commit-config.yaml` 檢視更新內容，不需要的改動以 `git restore` 還原（[pre-commit 官方文件](https://pre-commit.com/)）。
- **(d) 指定單一工具或全部**：皆可。透過 `--repo <REPO_URL>` 參數可指定特定儲存庫（可重複傳入多次）；省略時則全數升級。若帶入 `--freeze`，會將 Tag 名稱轉換並鎖定為具體的 Commit SHA（[pre-commit autoupdate 官方文件](https://pre-commit.com/#pre-commit-autoupdate)）。

---

### 5. Terraform (`terraform init -upgrade` 與 Lock File)
- **(a) 查最新版方式**：依據 Terraform Provider Network Protocol 向 Terraform Registry API（`https://registry.terraform.io/v1/providers/...`）發送 HTTP 請求取得版本清單、雜湊值及各平台 Binary 下載資訊（[Terraform Provider Registry Protocol 文件](https://developer.hashicorp.com/terraform/internals/provider-registry-protocol)）。
- **(b) 改版本檔後是否立即安裝**：
  - `terraform init -upgrade`：**是**。會解析最新版本，將 Provider 二進位檔下載解壓至 `.terraform/providers/`，同時覆寫 `.terraform.lock.hcl` 鎖定檔（[Terraform init 指令說明](https://developer.hashicorp.com/terraform/cli/commands/init#upgrade)）。
- **(c) Dry-run / 只改檔不裝**：
  - `terraform init -upgrade` 本身**無 dry-run 選項**。
  - **前例解法：`terraform providers lock`**：Terraform 專門提供了另一個指令 `terraform providers lock`，此指令會查詢 Registry 並**只改寫 `.terraform.lock.hcl` 鎖定檔與雜湊值，完全不下載 Provider Binary 至本地目錄**（[Terraform providers lock 指令文件](https://developer.hashicorp.com/terraform/cli/commands/providers/lock)）。
- **(d) 指定單一工具或全部**：
  - `terraform init -upgrade`：**無法指定單一 Provider**，會強制更新專案內所有 Provider 與 Module（[Terraform 官方文件：鎖定檔管理](https://developer.hashicorp.com/terraform/language/files/dependency-lock)）。
  - `terraform providers lock [providers...]`：**可以指定單一 Provider**（如 `terraform providers lock hashicorp/aws`），亦可省略參數更新全部（[Terraform providers lock 指令文件](https://developer.hashicorp.com/terraform/cli/commands/providers/lock)）。

---

### 6. npm (`npm update` 與 `npm-check-updates`)
- **(a) 查最新版方式**：向 npm Registry（`https://registry.npmjs.org/<pkg>`）查詢 Packument JSON 元資料，比對 `dist-tags.latest` 或符合範圍的最新版本（[npm Registry API 規格](https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md)）。
- **(b) 改版本檔後是否立即安裝**：
  - `npm update`：**是**。會同時更新 `node_modules`（立即安裝）並改寫 `package-lock.json`（[npm update CLI 文件](https://docs.npmjs.com/cli/commands/npm-update)）。
  - `npm-check-updates` (`ncu`)：**否**。執行 `ncu -u` **只會改寫 `package.json`，完全不會更動 `node_modules` 與 `package-lock.json`**；使用者必須手動執行 `npm install` 才會安裝（[npm-check-updates 儲存庫文件](https://github.com/raineorshine/npm-check-updates)）。
- **(c) Dry-run / 只改檔不裝**：
  - `npm update --dry-run`：提供預覽模式，不改檔亦不安裝（[npm update CLI 文件](https://docs.npmjs.com/cli/commands/npm-update)）。
  - `ncu`：**預設行為即為 Dry-run**。不加參數執行 `ncu` 時只會在終端機輸出彩色 diff 報告（顯示當前版本與最新版本差距），只有加上 `-u / --upgrade` 才會真正寫入檔案（[npm-check-updates 儲存庫文件](https://github.com/raineorshine/npm-check-updates)）。
- **(d) 指定單一工具或全部**：
  - `npm update [pkg...]`：可指定單一或多個套件，省略則全部更新（[npm update CLI 文件](https://docs.npmjs.com/cli/commands/npm-update)）。
  - `ncu [filter...]`：可指定套件名稱或傳入正則字串過濾（例如 `ncu lodash` 或 `ncu -f "/^react/"`），省略則處理全部（[npm-check-updates 儲存庫文件](https://github.com/raineorshine/npm-check-updates)）。

---

### 7. Bazelisk (`.bazelversion` 的 `latest` 語法)
- **(a) 查最新版方式**：當 `.bazelversion` 填入 `latest`（或 `latest-1`、`last_green` 等）時，Bazelisk 會依序向 GitHub Releases API（`https://api.github.com/repos/bazelbuild/bazel/releases`）查詢；若遭遇 Rate limit 則 Fallback 至 GCS Bucket（`https://www.googleapis.com/storage/v1/b/bazel/o`）（[Bazelisk 官方儲存庫文件](https://github.com/bazelbuild/bazelisk)）。
- **(b) 改版本檔後是否立即安裝**：**否**。Bazelisk 本身是透明啟動器（Launcher），沒有升級專用的改檔指令。當 `.bazelversion` 被修改或設為 `latest` 時，**任何下載動作都不會在編輯檔案時發生，而是在下一次執行 `bazel <command>` 時，Bazelisk 才會檢查快取並自動下載解壓**（[Bazelisk 運作機制說明](https://github.com/bazelbuild/bazelisk)）。
- **(c) Dry-run / 只改檔不裝**：Bazelisk 無升級 CLI，改寫 `.bazelversion` 本質就是純文字改檔，不會引發任何安裝副作用（[Bazelisk 官方儲存庫文件](https://github.com/bazelbuild/bazelisk)）。
- **(d) 指定單一工具或全部**：僅限 Bazel 本身單一工具（[Bazelisk 官方儲存庫文件](https://github.com/bazelbuild/bazelisk)）。

---

## 4. 前例橫向對照矩陣與架構歸納

### (1) 綜合特性比較表

| 工具 / 流程 | (a) 最新版查詢方式 | (b) 改版本檔後是否立即安裝 | (c) Dry-run / 只改檔不裝選項 | (d) 範圍控制 |
| :--- | :--- | :--- | :--- | :--- |
| **Gradle Wrapper** | REST API (`services.gradle.org`) | **否**（下一次 `./gradlew` 才裝） | 本質即只改檔不裝；無預覽 diff 的 `--dry-run` | 僅 Gradle 本身 |
| **Batect** | GitHub Releases API | **否**（下一次 `./batect` 才裝） | 無 `--dry-run`；覆寫 wrapper 檔 | 僅 Batect 本身 |
| **mise** | 各外掛對應（GitHub/Git/API） | **是**（`use` / `--bump` 均立即裝） | `--dry-run` 僅預覽；無只改檔不裝指令 | 單一工具 / 全部 |
| **pre-commit** | `git ls-remote --tags` | **否**（下一次 `run` 惰性安裝） | 本質即只改檔不裝；無原生 `--dry-run` | 單一 repo / 全部 |
| **Terraform** | Registry HTTP API | `init -upgrade`: **是**<br>`providers lock`: **否** | `providers lock` 為專用「只改檔不裝」指令 | `init`: 全部<br>`lock`: 單一或全部 |
| **npm / ncu** | npm Registry API | `npm update`: **是**<br>`ncu -u`: **否** | `npm update --dry-run`: 預覽<br>`ncu`: 預設即 Dry-run | 單一套件 / 全部 |
| **Bazelisk** | GitHub API / GCS Bucket | **否**（下一次 `bazel` 惰性安裝） | 無升級 CLI；手動改檔天然不觸發安裝 | 僅 Bazel 本身 |

---

### (2) 業界架構典範歸納
1. **Launcher + 惰性安裝（Lazy Extraction）典範**：
   Gradle、Batect、pre-commit 與 Bazelisk 均證明了一致的設計思維——**升級指令的職責僅限於「解析最新版本並寫入鎖定檔/設定檔」**。二進位檔的下載、解壓與環境建置應推遲到「使用者下一次真正呼叫工具時」進行。這能保持升級指令極速完成，避免網路或編譯中斷破壞檔案系統一致性。
2. **安全與審查典範（Dry-run as Default vs Explicit Write）**：
   - `npm-check-updates` 的典範最符合「工具不自動改使用者檔案，只顯示 diff」原則：**預設執行不帶參數時純粹輸出比對報表（Dry-run）**，必須加上 `-u / --upgrade` 或是 `--interactive` 才會真正覆寫檔案。
   - `pre-commit` 與 `terraform providers lock` 則將版本變更與實體安裝嚴格脫鉤，讓使用者能單純利用 `git diff` 審查純文字設定檔的變更。

---

## 5. 對 vendor_kit 升級流程的架構設計建議

綜合上述真實前例，針對 `vendor_kit` 的升級流程給出具體落地建議：

### (1) 自動化升級管道：導入 Renovate Regex Manager
- 配置前述第 1 節的 `customManagers`，利用 `managerFilePatterns: ["(^|/)\\.version$"]` 與 Handlebars 替換模板（[Renovate Custom Manager Regex 文件](https://docs.renovatebot.com/modules/custom-manager/regex/)）。
- 由 Renovate 自動開 PR，PR 的 diff 會乾淨呈現單行的 `tag` 與 `@sha256:digest` 同步遞增，符合 GitHub 團隊 code review 的標準實踐。

### (2) 本機手動升級指令：`just upgrade [tool]` 設計
建議在 `justfile` / launcher recipe 中提供 `upgrade` 指令，借鏡 `ncu` 與 `pre-commit autoupdate` 的介面設計：

1. **版本查詢與 Digest 取得方式**：
   - 主機僅有 Docker + git + just，因此查版本可藉由 Docker CLI 或輕量網路請求進行：
     - 若為公開 GHCR，直接使用 `curl` 呼叫 GitHub Container Registry 的 OCI / Docker Registry v2 API（`https://ghcr.io/v2/<org>/<name>/tags/list`）取得 Tag 清單，並透過 `manifests/<tag>`（帶 Accept header 為 `application/vnd.oci.image.index.v1+json`）取得精確的 `sha256` Digest。
     - 或在背景執行容器指令（例如 `docker buildx imagetools inspect ghcr.io/...:<tag>`）直接解析 Digest，無須將整個 Image pull 回本地。
2. **執行互動與 Diff 呈現（符合「不自動改檔案」原則）**：
   - **預設行為（`just upgrade` 或 `just upgrade <tool>`）**：
     - **純檢測與顯示 Diff（參照 `ncu` 預設行為）**。比對 `.version` 與 Registry 最新版本，於終端機印出表格：
       ```text
       tool          current                                    latest
       vendor_kit    0.2.0@sha256:9c1a...                      0.3.0@sha256:4f2c...
       mytool        1.0.0@sha256:3b5f...                      1.1.0@sha256:7a8e...
       ```
     - 提示使用者：「若要套用變更，請加上 `--apply` 或 `-u`」。
   - **寫入行為（`just upgrade --apply [tool]` 或 `just upgrade -u [tool]`）**：
     - 支援選擇性指定升級單一工具（如 `just upgrade -u mytool`）或全數升級（參照 `pre-commit --repo` 與 `ncu [filter]`）。
     - **只改寫 `.version` 檔案**，直接產生 git diff，**不要立即執行 `docker pull` 或解壓縮 `.<name>/`**（參照 Gradle / pre-commit 做法）。
3. **執行時生效（Lazy Installation）**：
   - 使用者透過 `git diff .version` 審查變更。
   - 下次使用者執行 `just <task>` 時，launcher 檢查 `.<name>/` 內部記錄之 digest 與 `.version` 不符，自動從 GHCR 抽出新版 dist 並更新，完成零負擔的無縫切換。

---

## 來源清單

1. https://docs.renovatebot.com/modules/custom-manager/regex/
2. https://docs.renovatebot.com/modules/datasource/docker/
3. https://docs.renovatebot.com/configuration-options/#pindigests
4. https://docs.renovatebot.com/configuration-options/#matchupdatetypes
5. https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file
6. https://github.com/dependabot/dependabot-core/issues/1290
7. https://github.com/dependabot/dependabot-core/issues/7885
8. https://docs.gradle.org/current/userguide/gradle_wrapper.html
9. https://docs.gradle.org/current/userguide/command_line_interface.html
10. https://services.gradle.org/versions/current
11. https://batect.dev/docs/reference/cli
12. https://github.com/batect/batect
13. https://mise.jdx.dev/cli/use.html
14. https://mise.jdx.dev/cli/upgrade.html
15. https://mise.jdx.dev/plugins/
16. https://pre-commit.com/#pre-commit-autoupdate
17. https://pre-commit.com/
18. https://pypi.org/project/pre-commit-update/
19. https://developer.hashicorp.com/terraform/cli/commands/init
20. https://developer.hashicorp.com/terraform/cli/commands/providers/lock
21. https://developer.hashicorp.com/terraform/language/files/dependency-lock
22. https://developer.hashicorp.com/terraform/internals/provider-registry-protocol
23. https://docs.npmjs.com/cli/commands/npm-update
24. https://github.com/raineorshine/npm-check-updates
25. https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md
26. https://github.com/bazelbuild/bazelisk
exit=0
