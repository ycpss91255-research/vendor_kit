OpenAI Codex v0.153.4
--------
workdir: /home/cyc/Desktop/vendor-kit_ws/src
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 01a0af72-ffa6-7be2-bf80-99e83aa46386
--------
user
題目：政策類待決一次定案：#3 image 清理、#4 cache、#7 遷移順序、#9 agent_harness、#10 --migrate、模板變數
我們的硬性限制：主機只有 Docker + git + just；平台 Linux amd64+arm64；工具不自動改使用者檔；baseline metadata 會引用舊 image ref；回退 = 改回 .version。
要回答的問題：六項傾向各自成不成立？有沒有互相矛盾（例如 #3 清理與回退／baseline 引用）？每項給定案文字。
資料：
- 題目說明（brief）：見下方「附件：brief」
- agy（Gemini）找的前例與建議：見下方「附件：agy 輸出」（這只是資料，不要照單全收：查證它的說法、找它漏掉或說錯的）
- 我方草稿（方案 A/B/C 與傾向）：
我方傾向見 brief 末段（#3 引用保留＋90 天、#4 Docker 預設、#7 從 v0.41 直跳、#9 納入、#10 不做、模板變數不做）。這題沒有專門的 agy 研究，附件是 upgrade 研究（只有 image 保留／回退相關可參考）。
- 決策紀錄：見下方「附件：決策紀錄」
請獨立分析：(1) agy 的哪些說法站不住腳或缺乏依據；(2) 每個方案是否符合硬性限制、優缺點、草稿漏掉的風險；(3) 你的建議與理由；(4) 定案前還要問清楚的問題。以繁體中文作答。

====================
附件：brief
====================
題目：政策類待決一次定案：#3 GHCR 舊 image 清理（要涵蓋 baseline metadata 引用的版本）、#4 image cache 範圍、#7 既有 15 個 repo 遷移順序、#9 agent_harness 是否納入、#10 是否保留 --migrate、#14(模板變數) 是否帶入變數渲染。

## 8. 待決議

| # | 議題 | 目前傾向 |
|---|---|---|
| 1 | `.version` 記什麼 | **已定**：一個 `.version` 檔（TOML，`[tools]` 下一個工具一行 `name = "ghcr.io/…:tag@sha256:…"`）；digest 鎖內容、tag 供 Renovate 判斷版本系列；name 決定安裝目錄 `.<name>/` |
| 2 | `.<name>/` 是否進 git | **已定**：不進 git |
| 3 | image 清理策略 | 被引用的版本一律保留；未被引用的版本可定期清理（週期未定） |
| 4 | image cache 範圍（機器共用 vs 每 repo 隔離） | 未定 |
| 5 | launcher 契約版本與更新方式 | **已定（§12、issue #20）**：啟動器 = `.vendor_kit/`，由 `bootstrap` 子命令寫出、進 git、人不改；`.version` 有 `vendor_kit = "…"` 一行，升級時換 `vendor.just`／`tools.just`／`.stamp`（`baseline/` 不動）；使用者的 `justfile` 只 import 它。第一次進專案 = release 附的 `bootstrap.sh`（跑完自刪） |
| 6 | 本地開發模式的切換方式 | **已定（issue #21，第 4 頁）**：`.version.local` 覆蓋檔（同格式、不進 git，bootstrap 寫進 .gitignore），`<name> = "path:../tool"` 那行優先；用 vendor_kit image 掛本機 dist 安裝，印記第一行 `dev:<路徑>`，verify 跳過只印警告、每次重新複製；`just dev <name> <path>`／`just undev <name>`。不用環境變數（出問題要能從檔案追） |
| 7 | 既有 15 個 repo 的遷移順序 | 建議從 v0.41 直接跳新機制，不先走 v0.42/v0.43 subtree 遷移；試點 urg_node_humble（簡單）+ isaac（複雜） |
| 8 | vendor_kit 既有 issue 的處置 | #7、#13 等 rollback 相關議題可能失效，需逐一重審 |
| 9 | agent_harness 是否納入同一機制 | 其內容（AGENTS.md、skills）屬 init.toml 類；先做只服務 base 的最小版本，再驗證通用性 |
| 10 | 是否保留自動遷移 `just upgrade --migrate` | 預設不動；等 dist 路徑契約穩定後再評估 |
| 11 | `diff` 是否做三方比對 | **已定（issue #22，第 5 頁）**：三方、只顯示不寫回；基準 = `.vendor_kit/baseline/<name>/`（每工具一份，進 git，人不改、納入檢查）；init 從第一版就寫基準（碰到已存在的檔 → warn、不覆蓋、仍存基準）；`just accept <name>` 更新基準；結束狀態 0 沒差異／1 工具有改／2 可能重疊；兩個工具 init 到同一 dest → 報錯；第一版檔案層級五分類＋兩份 diff，第二版自寫 diff3 |
| 12 | `verify` 的基準 | **已定（issue #23，第 5 頁）**：基準 = `.version` 鎖定的 image 內 `/dist`（verify 本來就在該工具容器內跑，不多起容器、不上網）；兩棵樹比對：檔案集合（缺、多都失敗，只豁免 .stamp）＋ sha256 ＋ 執行位（單向）＋ 型別（第一版禁 symlink）；不比 mtime／owner；印記降為「已裝版本」快取鍵（第一行 = `--self`），不簽章；失敗中止不自動重裝；第一版不做 stat 快取 |
| 13 | 並行安裝的 lock | **已定（issue #24，第 5 頁）**：flock 鎖專案目錄本身（不建鎖檔；install／accept 排他、verify 共享）；拿到鎖後重讀 .version 與印記，已是目標版本就跳過複製仍 verify；逾時預設 60 秒（環境變數可改，0 = 立即失敗）；鎖不支援 → 直接失敗，`VENDOR_KIT_NO_LOCK=1` 才放行，不退回 mkdir 鎖；暫存目錄亂數名並清殘留；`docker run --init`；平台 = Linux amd64／arm64（含 WSL2） |
| 14 | 模板是否帶入變數（專案名等）渲染 | 目前只複製；圖上標「待定」 |



我方傾向：#3 被任何 .version（含歷史 commit 與 baseline metadata）引用就保留、其餘 90 天清、先不自動化；#4 用 Docker 預設機器共用；#7 從 v0.41 直接跳新機制、先試 urg_node_humble + isaac；#9 納入（第二個工具 repo）；#10 不做；#14 模板變數先不做（純複製，變數用工具自己的 setup.toml 在執行期讀）。
====================
附件：agy 輸出
====================
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

====================
附件：決策紀錄
====================
# base dist 分發機制調整：討論紀錄

> 日期：2026-09-16
> 範圍：取代 base 目前以 `git subtree` + symlink 分發 dist 的方式。**base 本體（Dockerfile 模板、wrapper、lib 等）不變**，只調整「dist 怎麼送進 downstream repo」。
> 配套圖：`dist_distribution.drawio`（1 vendor_kit 架構圖、2 框架定義、3 流程：使用者指令、4 流程：版本生命週期、5 流程：vendor_kit 內部、6 原型對照、7 資料夾架構、8 測試分層與強制閘門、9 使用者介面：just 指令表、10 流程：bootstrap、11 流程：升級與回退（初版，待決處以便條標示）、12 對外契約與 CI 隔離（初版）；名詞表在各頁底部）
> 圖面審查：每輪改完跑 `.claude/workflows/diagram-review.js`（Claude 子代理 + codex 雙軌審查）
> 可執行原型：`../proto/`（vendor_kit / tool / project 三個資料夾，見 §9）

---

## 1. 現況問題（實際掃描 ycpss91255-docker org）

| 問題 | 觀察 |
|---|---|
| 版本漂移 | 14 個 repo 停在 v0.41.0；jetson_sdk_manager v0.39.0；isaac v0.42.0；base 已到 v0.43.0-rc2 |
| 卡在 layout 遷移前 | v0.42 的 `dist/` 重構與 `.setup.conf` 搬遷，只有 isaac 完成 |
| workflow pin 混用 | ros_distro / ros2_distro 的 `main.yaml` 同時有 `@v0.41.0` 與 `@v0.20.0` |
| 複製過量 | urg_node_humble 160 個檔案中 119 個在 `.base/`（約 74%）；isaac 的 `.base/` 含 base 自己的 115 個 test 檔與 37 個 doc 檔 |
| hook stub 雜訊 | 每 repo 14 個 stub，全 org 只有 4 個有實際內容（isaac ×2、realsense_ros1/2 ×1） |
| 分發機制各自發明 | base（subtree）、agent_harness（自有 init/upgrade）、multi_run（`.template_version`） |
| 自我升級缺陷 | agent_harness 註解記錄：base 曾因升級搬走 upgrade.sh，導致下一次升級失敗 |

## 2. 核心約束

- Host 只安裝 **Docker + Git + just**（不可要求 Python 等）
- 允許使用網路（可從 GHCR pull image）
- **平台範圍**（2026-09-17 定）：Ubuntu／Linux，**amd64 與 arm64 都要**（含 Jetson，對齊 base）；Windows 只在 WSL2 裡用（等同 Linux）；macOS 不在範圍。程式不可依賴架構專屬的東西（例如系統呼叫號），image 一律 multi-arch

## 3. 決策：以 GHCR image 分發 dist

**一句話：base 發佈時把 dist 打包成 image 推上 GHCR；downstream 執行 image，由它把 dist 寫進 repo，跑完 container 即刪除。**

### 角色分工

| 元件 | 職責 |
|---|---|
| vendor_kit | 通用安裝工具（`install / init / verify / diff`，第一次另有 `bootstrap` 寫出啟動器，§12），打包成 `vendor_kit:vN` image；本身以 Python 實作、只在容器內執行。安裝目錄 `.<name>/`，name = `.version` 裡的工具名（由啟動器以 `--name` 傳入） |
| base | 本體不變；release 時 `FROM vendor_kit:vN` 加入 `dist/` 與 `init.toml`，推出 `base-dist:vX` |
| 其他工具（agent_harness …） | 同樣 `FROM vendor_kit`，打包自己的 dist |
| downstream repo | 只記錄使用的版本 + 一個極薄的 launcher（justfile） |

### 出貨規則（只有兩條）

1. **`dist/` 底下全部出貨**，寫進下游的 `.<name>/`（name = 工具名；base 就是 `.base/`）；每次 upgrade 整批覆蓋（原子替換），下游不可改。base 今天的 `upgrade.sh` 第 1 步 `git subtree pull` 就是這個行為，只是範圍從整個 repo 縮到 `dist/`。
2. **`init.toml` 列的檔案**，`init` 時再複製一份到指定路徑；已存在則跳過，之後歸下游所有，upgrade 不碰。

```toml
# init.toml（放在工具 repo 根目錄，跟 dist/ 一起進 image）
[[file]]
src  = "dockerfile/Dockerfile"     # 相對 dist/
dest = "Dockerfile"                # 相對下游 repo 根目錄

[[file]]
src  = "template/hooks/"           # 目錄整個複製
dest = "script/hooks/"
```

| 類別 | 例子 | 行為 | 進 git |
|---|---|---|---|
| `dist/` 全部 | wrapper、lib、runtime、模板、config、smoke 測試 | 每次 upgrade 整批覆蓋 | 否（`.base/`） |
| `init.toml` 列的 | Dockerfile、entrypoint、setup.toml、main.yaml、hooks、.gitignore | init 建立一次，之後屬於使用者；upgrade 時 `diff` 顯示差異、不自動改 | 是 |
| 版本記錄 | `.version` | 由 Renovate 或 `just upgrade` 改；使用者只 merge | 是 |
| 產生物 | `compose.yaml`、`.env`、印記檔 | 由工具產生 | 否 |

hooks 由 init 明確生成（對齊 `init.sh` 現況），不設 opt-in 類別。

**與 base 今天 `upgrade.sh` 的差異（刻意改變）**：今天第 3～5 步會自動改寫使用者的 `Dockerfile`、`script/entrypoint.sh`（`dockerfile_migrate.sh` 的 16 個遷移）、`main.yaml`（`@tag` sed）、`.gitignore`。新架構下工具不改使用者檔：
- `main.yaml` 的 `@tag` → Renovate github-actions manager 更新
- `Dockerfile` 遷移 → `just diff` 顯示，使用者自己改。**前提是 base 遵守 ADR-0006 的 `dist/` 路徑契約不亂搬**；那 16 個遷移的根因幾乎全是 base 內部搬路徑
- `.gitignore` → 列入 `init.toml`，init 建一次
- 若日後仍需自動遷移，加明確的 `just upgrade --migrate`，預設不動（待決議）

### init

`init` 是獨立命令（`just init`），只在專案第一次接上工具時執行一次；`install` 永不建立或修改使用者檔案（使用者刻意刪除的檔案不會復活）。`init` 對已存在的檔案一律跳過，所以新舊 repo 用同一個指令。

### 自動提醒（升級）

- **Renovate**（主要）：`customManagers` 用 regex 追蹤 `.version` 中 `ghcr.io/…:tag@sha256:…`（`datasourceTemplate: docker`；tag 為 `currentValue`、digest 為 `currentDigest`），上游有新版就開 PR；15 個 repo 共用一份 preset。PR 的 CI 跑 install + wrapper smoke test。
- **`just upgrade`**（手動備援）：查 GHCR 最新版 → 改 `.version` → install → diff。細節待議。
- base 端 release 時可加 `repository_dispatch` 推播給 downstream 當即時通知（選配）。

### 前例與定位

方案沒有完整前例；各部分對應：Gradle Wrapper（薄啟動器 + 版本檔 + 自動下載）、Dev Container Features / Homebrew bottles（GHCR 當檔案倉庫、digest 鎖版本）、Copier（初始檔歸使用者 + 升級 diff）、Carvel vendir（宣告式目錄同步的 manifest/lock 設計）、OpenAPI Generator docker CLI（以 image 出貨、bind mount 寫回專案）。

## 4. 流程

**執行 `just <verb>`**
1. 讀 `.version`
2. image 不在本地 → `docker pull`
3. `.<name>/` 印記與 `.version` 不一致、尚未安裝、或印記不可讀 → `docker run --rm`（host UID/GID）執行 `install`；剛安裝成功即直接進入第 5 步，不再 verify
4. 印記一致時 → 執行 `verify` 比對 `.<name>/` 每檔 hash，被手改則報錯中止
5. 執行 `.<name>/` 內 wrapper → `docker compose …`

**升級**：改 `.version` → just → 新版 image 落地。升級邏輯在新版 image 內，不會有「舊工具升級自己」的問題。

**回退**：`git revert` `.version` 的變更 → just → 舊版 image 重新落地。不需額外 rollback 紀錄。

## 5. 可追溯性（出 bug 時）

```
downstream commit → .version（版本）→ image label（base commit SHA）→ base 原始碼
```

必要條件：
- image 加 label：base commit SHA、版本、source repo
- `.base/` 內寫印記檔：寫入的版本 + 各檔案 hash
- GHCR tag 不覆蓋；仍被任何 downstream `.version` 引用的版本不可刪（寫成 CI 規則；未被引用版本的清理策略見 §8 第 3 項）
- `git bisect` 在 `.version` 上即可定位是哪次升級引入問題

## 6. 可行性注意事項

- container 必須以 host UID/GID 執行，否則落地檔案為 root 擁有
- gitignore 路線下，`docker build` 前必須先落地（launcher 保證順序）；進 image 的 runtime 腳本亦可考慮改為 `COPY --from=base-dist:vX`
- launcher 無法由 dist 分發自己，需極薄、帶契約版本號，過舊時由引擎提示更新
- image 保留、只刪 container；每次重 pull 會變慢、受 rate limit 影響、離線失效
- 離線機器：`docker save` / `docker load` 預載 image
- 需預留**本地開發模式**：來源暫時指向本機 base checkout，開發 base 時不必每次發佈
- **rootless Docker / userns-remap / 遠端 daemon**：`-u UID:GID` 不通吃、bind mount 掛不到遠端；要偵測並明寫支援範圍
- **多架構**：Apple Silicon、Jetson 需各自的 vendor_kit image；`.version` 鎖 image **index** digest
- **私有 GHCR**：使用者與 Renovate 各自需要 token
- **替換原子性**：並行 `just`、安裝中斷 → 先寫暫存目錄再換名，並加 lock
- **驗證邊界**：印記可被寫，驗證基準應來自鎖定的 image；比對檔案集合、執行權限、symlink，不只內容 hash
- **`diff` 需三方比對**（舊模板→新模板 vs 使用者檔→新模板），否則使用者修改會淹沒真正的升級需求

## 7. 已排除的方向

| 方向 | 排除原因 |
|---|---|
| 以 binary 取代 base 本體 | 誤解範圍；base 本體必須繼續提供 Dockerfile 等內容 |
| 整套工具在 container 內執行並透過 docker.sock 操作 daemon | host 偵測（GPU/X11/DRI/Jetson）靠 mount 拼湊，漏一項即安靜出錯；bind mount 路徑由 daemon 以 host 路徑解析 |
| 自行開發完整 vendoring engine（含獨立 rollback 紀錄等） | 版本由 image 決定、`.base/` 不進 git 後，rollback 與自我升級問題結構上消失 |

## 8. 待決議

| # | 議題 | 目前傾向 |
|---|---|---|
| 1 | `.version` 記什麼 | **已定**：一個 `.version` 檔（TOML，`[tools]` 下一個工具一行 `name = "ghcr.io/…:tag@sha256:…"`）；digest 鎖內容、tag 供 Renovate 判斷版本系列；name 決定安裝目錄 `.<name>/` |
| 2 | `.<name>/` 是否進 git | **已定**：不進 git |
| 3 | image 清理策略 | 被引用的版本一律保留；未被引用的版本可定期清理（週期未定） |
| 4 | image cache 範圍（機器共用 vs 每 repo 隔離） | 未定 |
| 5 | launcher 契約版本與更新方式 | **已定（§12、issue #20）**：啟動器 = `.vendor_kit/`，由 `bootstrap` 子命令寫出、進 git、人不改；`.version` 有 `vendor_kit = "…"` 一行，升級時換 `vendor.just`／`tools.just`／`.stamp`（`baseline/` 不動）；使用者的 `justfile` 只 import 它。第一次進專案 = release 附的 `bootstrap.sh`（跑完自刪） |
| 6 | 本地開發模式的切換方式 | **已定（issue #21，第 4 頁）**：`.version.local` 覆蓋檔（同格式、不進 git，bootstrap 寫進 .gitignore），`<name> = "path:../tool"` 那行優先；用 vendor_kit image 掛本機 dist 安裝，印記第一行 `dev:<路徑>`，verify 跳過只印警告、每次重新複製；`just dev <name> <path>`／`just undev <name>`。不用環境變數（出問題要能從檔案追） |
| 7 | 既有 15 個 repo 的遷移順序 | 建議從 v0.41 直接跳新機制，不先走 v0.42/v0.43 subtree 遷移；試點 urg_node_humble（簡單）+ isaac（複雜） |
| 8 | vendor_kit 既有 issue 的處置 | #7、#13 等 rollback 相關議題可能失效，需逐一重審 |
| 9 | agent_harness 是否納入同一機制 | 其內容（AGENTS.md、skills）屬 init.toml 類；先做只服務 base 的最小版本，再驗證通用性 |
| 10 | 是否保留自動遷移 `just upgrade --migrate` | 預設不動；等 dist 路徑契約穩定後再評估 |
| 11 | `diff` 是否做三方比對 | **已定（issue #22，第 5 頁）**：三方、只顯示不寫回；基準 = `.vendor_kit/baseline/<name>/`（每工具一份，進 git，人不改、納入檢查）；init 從第一版就寫基準（碰到已存在的檔 → warn、不覆蓋、仍存基準）；`just accept <name>` 更新基準；結束狀態 0 沒差異／1 工具有改／2 可能重疊；兩個工具 init 到同一 dest → 報錯；第一版檔案層級五分類＋兩份 diff，第二版自寫 diff3 |
| 12 | `verify` 的基準 | **已定（issue #23，第 5 頁）**：基準 = `.version` 鎖定的 image 內 `/dist`（verify 本來就在該工具容器內跑，不多起容器、不上網）；兩棵樹比對：檔案集合（缺、多都失敗，只豁免 .stamp）＋ sha256 ＋ 執行位（單向）＋ 型別（第一版禁 symlink）；不比 mtime／owner；印記降為「已裝版本」快取鍵（第一行 = `--self`），不簽章；失敗中止不自動重裝；第一版不做 stat 快取 |
| 13 | 並行安裝的 lock | **已定（issue #24，第 5 頁）**：flock 鎖專案目錄本身（不建鎖檔；install／accept 排他、verify 共享）；拿到鎖後重讀 .version 與印記，已是目標版本就跳過複製仍 verify；逾時預設 60 秒（環境變數可改，0 = 立即失敗）；鎖不支援 → 直接失敗，`VENDOR_KIT_NO_LOCK=1` 才放行，不退回 mkdir 鎖；暫存目錄亂數名並清殘留；`docker run --init`；平台 = Linux amd64／arm64（含 WSL2） |
| 14 | 模板是否帶入變數（專案名等）渲染 | 目前只複製；圖上標「待定」 |

## 9. 出貨物清單（安裝後 downstream repo 的實際樣貌）

image 只是運送容器，不會出現在 repo；repo 裡看到的是安裝工具從 image 寫出來的檔案。以同時使用 base 與 agent_harness 的專案為例：

```
my_robot_project/
├── .version                ← 進 git   Renovate／just upgrade 改；一行一個工具（tag@digest）
├── justfile                ← 進 git   使用者自己的指令清單；第一行 import .vendor_kit/（bootstrap 建立，之後歸使用者）
├── .vendor_kit/            ← 進 git   啟動器本體：vendor.just（標準指令）、tools.just（由 .version 衍生）、.stamp（vendor_kit 版本）；bootstrap 寫出，人不改，升級只換這三個
│   └── baseline/<name>/    ← 進 git   三方比對的基準：init／accept 存的模板副本＋metadata；人不改
├── .version.local          ← 不進 git  本機開發用的覆蓋檔（平常沒有）
├── Dockerfile              ← 進 git   使用者檔案：第一次安裝時從 base 模板建立，之後歸使用者
├── entrypoint.sh           ← 進 git
├── setup.toml              ← 進 git
├── .github/workflows/main.yaml ← 進 git
├── script/hooks/           ← 進 git   init 建立的 stub
├── AGENTS.md               ← 進 git   使用者檔案：來自 agent_harness 模板
├── .base/                  ← 不進 git  base 的工具檔，每次安裝整批重寫，不可手改
│   ├── wrapper/ lib/ runtime/
│   └── .stamp              ←            印記檔：安裝版本 + 每個檔案的指紋
├── .harness/               ← 不進 git  agent_harness 的工具檔，同上
├── compose.yaml            ← 不進 git  wrapper 執行時產生
└── .env.generated          ← 不進 git
```

`.version` 範例：

```toml
[tools]
vendor_kit = "ghcr.io/ycpss91255-research/vendor_kit:v1.0.0@sha256:…"     # 啟動器自己的版本
base    = "ghcr.io/ycpss91255-docker/base-dist:v0.43.0@sha256:3f2a9c…"
harness = "ghcr.io/ycpss91255-research/agent_harness-dist:v0.5.2@sha256:8b1d…"
```

`git ls-files` 只會看到 `.version`、`justfile`、`.vendor_kit/`、使用者檔案；`.base/`、`.harness/` 是第一次跑 `just` 才長出來的。

## 10. vendor_kit repo 結構與測試分層（第 7、8 頁；決策日期 2026-09-17）

**決策：單一 container、單一 Python package（7 個模組），但測試分層與隔離全部用「強制閘門」實現，不靠提醒或紀錄。**

### 目錄（tool-first：`test/<工具>/<層級>/`）

```
vendor_kit/
├── src/vendor_kit/        cli.py dist_reader.py repo_fs.py template.py stamp.py diff.py report.py（= 第 1 頁 7 個模組）
├── test/
│   ├── env/check.sh            環境檢查（smoke）：python3 ≥ 3.11、tomllib、vendor_kit 進入點、toml-bridge、WORKDIR
│   ├── lint/{ruff,import-linter}/ + mirror_check.py + blackbox_check.py
│   ├── pytest/unit/            test_<模組>.py ×7（鏡射 src）
│   ├── pytest/integration/     test_install.py test_init.py test_verify.py test_perf_verify.py test_diff.py
│   ├── pytest/system/          docker run 整個 image（CI 主機）
│   ├── pytest/acceptance/      第 3 頁三條泳道：假專案裡真的打 just（CI 主機）
│   ├── fixtures/               假 dist/、init.toml、VERSION、project/（假專案：justfile）、tool_image/（假工具 image 的 Dockerfile）
│   └── (system / acceptance 各有 conftest.py：sys.modules["vendor_kit"] = None)
├── Dockerfile                  runtime 的基底 = toml-bridge image（ghcr.io/ycpss91255-docker/toml-bridge@sha256:0a01f9…，提供 Python 與 TOML 工具）
│                               stage：runtime → env-test → test-base → lint / unit-test / install-test / init-test / verify-test / diff-test；runtime → release → release-test
├── docker-bake.hcl             group validate（env-test + 六個測試 stage）、group release（release + release-test）
└── doc/adr/
```

### 強制閘門（違反就 CI 紅）

| 層 | 閘門 | 實作 |
|---|---|---|
| smoke（環境檢查） | `env-test` stage 跑 `test/env/check.sh`；`test-base FROM env-test`，所以環境不對就沒有任何測試會跑（環境檢查先於一切） | `env-test` stage |
| lint | ruff；黑箱檢查；import-linter 契約（cli → dist_reader\|repo_fs → template\|diff\|stamp\|report；cli/template/diff/stamp/report 不准直接 import pathlib/shutil/os/io）；鏡射檢查（每個 src 模組必有 test_<模組>.py） | `lint` stage |
| unit | conftest 把 open()/Path.read_*/write_*/socket 換成 `pytest.fail` | `unit-test` stage |
| integration | conftest 禁 subprocess/socket；只給 tmp 目錄；只走 `cli.main()`；一個子命令一個 stage、各自只 COPY 自己的檔；`verify` 200 檔 < 0.5s | 四個 `*-test` stage |
| system / acceptance | lint 的 `blackbox_check.py`：測試檔不准 import vendor_kit；conftest 再把 `sys.modules["vendor_kit"]` 設為 None；只准 docker run／just + 檔案系統 | CI 主機（`.github/workflows/ci.yaml`） |
| release | `release` 只 FROM `runtime`（BuildKit 不會執行、也不會打包任何 test stage）；`release-test` FROM release 真的跑一次 install + verify，失敗就不 push | `release`、`release-test` stage |

前例：Docker multi-stage test stage、Google Small/Medium/Large、pytest src layout、import-linter；ROS 2 `system_tests`／REP-2004、Linux KUnit（in-tree）vs kselftest（out-of-tree）。層級名稱依 ISTQB（unit / integration / system / acceptance）；smoke 是類型不是層級：這裡指 env-test，先於所有測試。

印記第一行的來源（issue #23 改定）：啟動器把 `.version` 該行的字串用 `--self` 傳進容器，`install` 寫進 `.<name>/.stamp` 第一行，啟動器就拿這行跟 `.version` 比；image 內的 `/dist/VERSION` 只是給人看的識別字串（也解掉 `Dockerfile.dist` 要把自己的 digest 寫進自身的循環）。fixtures 裡的 `VERSION` 是假的（`fixture-dist:v0.1.0`）。

原型狀態（2026-09-17）：`docker buildx bake validate` 六個 stage 全綠；`bake release` 含 release-test（install + verify）通過；system 4 個、acceptance 4 個測試在主機 pytest 通過；`proto/project` 的 `just init / build / diff` 走完整流程；ADR-0001「測試分層與強制閘門」已寫（`proto/vendor_kit/doc/adr/`）。

## 11. 使用者介面：just 指令表（第 9 頁）

使用者只會碰 justfile 提供的指令。**命名空間定案（2026-09-17）**：vendor_kit 的 recipe 全部放在 `vendor_kit` 命名空間，不佔頂層——`just vendor_kit init / diff / accept / upgrade / dev / undev`；bootstrap 寫出的根 justfile 只有一行 `mod? vendor_kit '.vendor_kit/vendor.just'`；工具的 tool.just 用自己的命名空間（例 `mod? docker` → `just docker build`）。每個工具指令前的自動檢查由工具的 recipe 呼叫 `just vendor_kit ensure`（對專案目錄上鎖 → 印記第一行 ≠ 有效版本（`.version.local` 優先）→ install；相同 → verify（`.<name>/` 跟 image 內 dist 逐檔比）；失敗就中止；本機路徑 → 只印警告）。指令表分「常用（日常）」與「不常用（第一次／升級／開發工具本身）」兩區；dev／undev 的形式（給路徑 vs 選項式）仍待使用者回覆。

**vendor_kit 提供（每個專案都一樣）**

| 指令 | 什麼時候 | 做什麼 | 背後 |
|---|---|---|---|
| `just vendor_kit init` | 第一次接上工具 | 安裝 `.<name>/`，照 init.toml 建立初始檔（已存在：warn、不覆蓋），並把這版模板存成基準 `.vendor_kit/baseline/<name>/` | 容器：install → init |
| `just vendor_kit diff` | 升級之後 | 三方比對：印出「工具改了什麼」「你改了什麼」，不改檔；結束狀態 0／1／2 | 容器：diff |
| `just vendor_kit accept <name>` | 看完 diff、跟進完 | 把新版模板存成基準 | 容器：accept |
| `just vendor_kit dev <name> <path>` / `just vendor_kit undev <name>`（形式待回覆） | 開發工具本身時 | 寫／刪 `.version.local`，把工具指到本機路徑（不驗證只警告） | 容器：--dev install |
| `just vendor_kit upgrade` | 沒有 Renovate 時手動升級 | 改 .version 為最新 → 重裝 → 顯示差異（細節待議，§8 #5） | 查 GHCR → 改 .version → install → diff |
| （自動）`just vendor_kit ensure` | 每個工具指令前 | 檢查／安裝／驗證 | 容器：install 或 verify |

verify 不開放給使用者單獨打：它是每個指令前的守門。

**工具 `<name>` 提供（由工具的 dist/ 決定，每個工具可以不同；以「容器工作流」工具為例）**

| 指令 | 做什麼 | 背後 |
|---|---|---|
| `just <模組> build`（例 `just docker build`） | 建置專案自己的 image | `.<name>/` 的 build 腳本 → docker compose build |
| `just <模組> run` | 啟動專案容器 | run 腳本 → docker compose up |
| `just <模組> exec` | 進到容器裡下指令 | exec 腳本 → docker compose exec |
| `just <模組> stop` | 停掉並移除容器 | stop 腳本 → docker compose down |

為什麼是這四個：一個容器的一生 = 做出來 → 開起來 → 進去用 → 關掉，一個階段一個指令；換工具就換一套。每個工具指令前後可掛使用者自己的 hooks（`script/hooks/pre|post/<指令>.sh`，init 建立的空殼）。

## 12. bootstrap：第一次把 vendor_kit 接進專案（第 10 頁；決策日期 2026-09-17）

**決策：啟動器由 vendor_kit 寫出並擁有；第一次靠 release 附的一支腳本，跑完自刪。**

1. 使用者從 vendor_kit 的 GitHub release 頁下載 `bootstrap.sh`，在專案目錄執行。
2. 腳本只做四件事：檢查主機有 docker / git / just → `docker run --rm -u UID:GID -v $PWD:/repo vendor_kit:vN --name vendor_kit --self <image> bootstrap` → 問「要現在接一個工具嗎？」（要就把 `<name> = "image"` 寫進 `.version`，再 `just init`）→ 刪掉自己。主機不需要 Python。
3. `bootstrap` 子命令寫出：
   - `.vendor_kit/vendor.just`（標準指令 install / init / diff / accept / upgrade 與每個指令前的 `_ensure`）、`.vendor_kit/tools.just`（由 `.version` 衍生的每工具 recipe，每次 install 後重寫）、`.vendor_kit/.stamp`（vendor_kit 自己的版本 + vendor.just 指紋）——由 vendor_kit 擁有，人不改，進 git；`.vendor_kit/baseline/<name>/` 之後由 init／accept 寫（持久資料，升級不動）；
   - `justfile`（第一行 `mod? vendor_kit '.vendor_kit/vendor.just'`，其餘歸使用者）、`.version`（先只有 `vendor_kit = "…"` 一行）——已存在就不動。
4. 之後 vendor_kit 出新版：`.version` 的 `vendor_kit` 那行改掉（Renovate 或 `just upgrade`）→ `.vendor_kit/` 的 `vendor.just`、`tools.just`、`.stamp` 換新（`baseline/` 不動）；使用者的 `justfile` 永遠不會被動到。

原型：`proto/vendor_kit/src/vendor_kit/launcher.py` 產生 `.vendor_kit/` 內容；`cli.bootstrap()` 寫出。

warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
codex
我會先查證會影響定案的官方資料，重點是 image 保留、多架構與回退，再逐項整理可直接採用的決議文字及尚需釐清的邊界。

web search: 
web search: https://docs.renovatebot.com/modules/manager/regex/
web search: 
web search: https://docs.renovatebot.com/configuration-options/#autoreplacestringtemplate
web search: 
web search: 'Override how'
web search: 
web search: '### `autoReplaceStringTemplate`'
codex
六項傾向可以採用，但 **#3 必須改成可執行的保留政策，#7 必須區分「跳過中間版本」與「省略相容性修改」，#9 必須限定檔案所有權**。另外，「回退＝改回 `.version`」只能保證工具版本回退；若要求連使用者設定、baseline、產生物都恢復，會與「不自動改使用者檔」衝突。

附件沒有完整列出 A/B/C，以下比較各題的實際替代方向，不替草稿杜撰方案編號。repo 現況採附件描述，未另行掃描 15 個 repo。

**一、agy 哪些說法不能直接採信**

1. **前例支持「依版本宣告選工具」，不保證舊版本永遠可取得。**  
   digest 鎖住內容，不等於保存內容。agy 沒有研究 GHCR 保留政策，不能用 Bazelisk／Nix 的回退前例推導「刪舊 image 也沒問題」。GitHub 明確提醒刪除 package 可能破壞依賴它的專案；刪除後的還原還有 30 天與 namespace 可用等條件，不能當長期回退機制。[GitHub 文件](https://docs.github.com/en/packages/learn-github-packages/deleting-and-restoring-a-package)

2. **Renovate 方向正確，但範例不能直接用。**  
   regex manager 預設按整份檔案匹配，agy 的 `^` 不會逐行匹配；你們第一行是 `[tools]`，其範例因此可能完全抓不到工具。必須處理換行邊界，並限定 `.version`，避免更新 baseline metadata。此外，`autoReplaceStringTemplate` 是覆寫替換方式的選項，並非自訂格式一律必填。[regex 文件](https://docs.renovatebot.com/modules/manager/regex/)、[替換設定](https://docs.renovatebot.com/configuration-options/#custommanagersautoreplacestringtemplate)

3. **Dependabot「只支援 Dockerfile 與 docker-compose.yml」已不正確。**  
   官方也列出 Kubernetes manifests／Helm charts 的 image 更新支援。「不能靠一般設定更新這份自訂 TOML」仍是合理結論，但原本的理由過度概括。[GitHub 文件](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-repositories#docker)

4. **Gradle「升級必須跑兩次」說得太滿。**  
   官方說一次通常足以讓舊 Wrapper 執行新版 Gradle；第二次是為了完整更新 Wrapper 本身。這不能證明 vendor_kit 必須採某個自我升級順序。[Gradle 文件](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper)

5. **「覆寫 recipe 後自動由新 recipe 接管」缺少機制。**  
   agy 沒證明執行中的 `just` 會重新載入已改寫的檔案。應明確安排刷新後重新啟動 `just`，或定義需要再次執行；不能把「檔案換新」當作「目前指令已換新」。降級時同樣要驗證。

6. **報告內部也有口徑不一致。**  
   前面主張升級只改版本、延遲安裝，後面手動 upgrade 卻立即 install；兩者都可以設計，但不是相同流程。它還沿用 `.installed_version`、頂層 `just init`、直接調用三方 diff 工具等說法，已不符合你們的 `.stamp`、命名空間與第一版檔案層級 diff 決策。

**二、六項建議與可直接採用的定案文字**

| 議題 | 判斷 | 替代方向與取捨 |
|---|---|---|
| #3 引用保留＋90 天 | 修正後成立 | 單純按年齡／保留最近 N 版會破壞歷史回退；全部永久保留最簡單，但儲存持續增加 |
| #4 Docker 預設共用 | 成立 | 每 repo 自建 cache 增加空間、清理與同步負擔；獨立 daemon 才能提供更強的隔離 |
| #7 直接遷移 | 有條件成立 | 逐版遷移可以沿用舊程序，但增加過渡狀態與修改次數；直跳需要完整對照與驗收 |
| #9 納入 harness | 有條件成立 | 永久分開維護會重複分發機制；一次全部重構則擴大首版範圍 |
| #10 不做 `--migrate` | 成立 | 自動遷移減少手工，但引入使用者檔改寫、衝突與反向遷移問題 |
| #14 不做變數渲染 | 成立 | 渲染較方便，但 baseline 必須追蹤變數、渲染器及其版本；純複製較容易重現 |

這些選擇本身均不需要增加 host 套件；TOML 解析、registry 查詢與檔案處理應放在容器內。

**#3：引用保留＋90 天，先不自動化**

最大問題是「被任何歷史 commit 引用」無法只靠掃描目前 default branch 判定。未推送的 commit、fork、已刪 branch、封存 repo、沒有權限讀取的 repo，都可能讓掃描漏掉引用。

若堅持字面上的「任何歷史引用」，最容易落實的首版政策是：**公開供下游採用的 release image 永久保留；只清理能確認沒有被採用的候選版本。** 90 天不能凌駕引用保護，也不是儲存上限。

保護對象還必須是完整的 multi-arch image。OCI index 會指向各平台 manifest；只保留 index、刪掉看似「無 tag」的子 manifest，仍可能破壞 arm64 或 amd64 的拉取。[OCI 規格](https://github.com/opencontainers/image-spec/blob/main/image-index.md)、[Docker 多平台文件](https://docs.docker.com/build/building/multi-platform/)

> **定案文字：**  
> 任何受支援 downstream 的 `.version` 或 baseline metadata，包括歷史版本，所引用的 image 均不得清除。保護範圍包含 index digest、amd64／arm64 manifest 與其必要內容；release tag 不覆寫、不移除。第一版永久保留已供下游採用的 release image。其他 image 自首次完整確認未被引用起滿 90 天，且刪除前再次確認仍未被引用，才可人工清理；無法確認者保留。第一版不啟用自動刪除。

補充兩個執行邊界：

- baseline 已保存模板副本，也不代表可以忽略 metadata 裡的舊 image ref；依本次政策，它仍是保留根。
- 若 Dockerfile 等其他檔案也直接引用 dist image，必須一併納入，不能只搜尋 `.version`。首次盤點不能把 image 的發布日期直接當成「已確認無引用 90 天」。

**#4：沿用 Docker 共用 image cache**

精確範圍應寫成 **同一 Docker daemon 的 image store**，不是整台機器必然只有一份；rootless、不同 context 或不同 daemon 可能各有儲存。

共用 image cache 不影響各 repo 用不同 digest；但它也不提供永久保存或 repo 間的安全隔離。尤其你們 container 跑完即刪，`docker image prune -a` 可以清掉沒有 container 關聯的 image，Docker 不會讀 `.version` 判斷是否仍需要。[Docker prune 文件](https://docs.docker.com/reference/cli/docker/image/prune/)

> **定案文字：**  
> image cache 使用目前 Docker daemon 的預設 image store，供連到該 daemon 的專案共用；vendor_kit 不建立每 repo 的 image cache，也不自動執行 prune。各 repo 的 `.<name>/` 安裝目錄仍獨立。精確 image 不在本地時，依鎖定 digest 拉取；離線且缺少 image 時明確失敗，不改用其他版本。GHCR 的保留政策與本地 cache 清理由不同責任範圍管理。

因此 #3 與 #4 不矛盾：**GHCR 負責可再次取得，本地 cache 負責減少下載。** 即使 `.<name>/` 還在，缺少 image 時仍可能無法執行你們的 verify。

**#7：直接進新機制，但不能跳過必要修改**

直跳可以省掉 v0.42／v0.43 的 subtree 過渡流程；不能省掉 `.setup.conf`、Dockerfile 路徑、entrypoint、hooks、workflow 等實際相容性調整。

另有兩個草稿缺口：

- 附件的「14 個 v0.41＋jetson_sdk_manager＋isaac」合計是 **16 個**，與題目的 15 個不符。
- 舊 `.base/` 是 git 追蹤的 subtree，新 `.base/` 是可覆寫安裝目錄；不能直接讓 installer 接管而遺失本地修改。

> **定案文字：**  
> 既有 repo 從目前版本直接遷移至新分發機制，不要求先完成 v0.42／v0.43 subtree 遷移。先以 urg_node_humble 驗證簡單案例，再以 isaac 驗證複雜案例；擴大前必須另完成 arm64／Jetson 實機驗收。其餘 repo 依設定相似度與客製程度分批遷移。所有必要的使用者檔修改透過人工審查的 migration PR 完成，不由 install／upgrade 自動改寫。

每個 migration PR 至少要確認：

- 舊 subtree 的自訂內容與有效 hooks 已保留，才移除追蹤並加入 ignore。
- 在全新 clone、沒有既有 `.base/` 的情況下能 install、verify、build 及完成必要 smoke。
- 首次 init 對既有檔案只存「導入時的新模板基準」；它不是 v0.41 的真實祖先，不能據此宣稱已重建舊版三方比對。
- **跨越舊機制的回退使用 migration commit／PR 的還原；「只改 `.version`」適用於接入新機制之後。**

**#9：納入 agent_harness，作為第二個工具**

納入有助於驗證 vendor_kit 是否真的通用。但不能只因內容是 Markdown，就把所有 skills 都判定為使用者檔；分類依據應是所有權。

> **定案文字：**  
> agent_harness 納入同一分發機制，作為 base 最小流程完成後的第二個工具。需要下游編輯的 AGENTS.md 與 skills，透過 init.toml 初次複製，之後只提供 diff／accept；不可由 upgrade 覆寫。需要隨 image 整批更新的執行工具或共用資源保留在 `.<name>/`。第一版不提供使用者檔的區塊合併或自動同步。

必須提早驗證：

- agent 實際讀取的是哪個路徑；若不會讀 `.harness/`，不能把必要內容只放那裡。
- AGENTS.md 與已複製 skills **不會隨 `.version` 自動回退**。
- dest 衝突除了相同檔案，還要涵蓋目錄展開後重疊，以及檔案／目錄互斥。
- 不以 host Python／Node 腳本補足 harness 安裝，避免違反主機限制。

**#10：不提供 `--migrate`**

「保留旗標但預設不執行」仍會留下另一套修改使用者檔的契約；目前沒有必要承擔。

> **定案文字：**  
> 第一版不提供 `just vendor_kit upgrade --migrate`，不保留空殼旗標。upgrade 僅更新版本宣告、工具管理的安裝內容與啟動器，並顯示差異；既有使用者檔不改寫。必要修改以 migration guide 與 diff 說明，由使用者採用。未來若引入自動遷移，必須另立決策，不視為既定 roadmap。

這與 #7 相容：**人工 migration PR 是專案維護工作，不是工具執行時自動遷移。** `accept` 也只表示更新比較基準，不保證使用者已採納所有變更。

**#14：純複製，專案變數由工具在執行期讀取**

此選擇讓模板與 baseline 保持明確的位元組關係。代價是有些靜態檔案仍須人工修改；例如不能假設所有 GitHub Actions 欄位都能直接讀取 `setup.toml`。

> **定案文字：**  
> vendor_kit 第一版不執行模板變數替換、條件渲染或可變目的路徑；init 依固定映射複製原始內容，baseline 保存同一份來源模板。專案參數由各工具在執行期讀取自己的設定；必要的衍生檔寫至工具明確擁有的產生物路徑。必須固化在使用者檔的值由使用者手動調整，不在 upgrade 時重新生成。

`setup.toml` 的格式也要考慮舊工具能否讀取；否則 image 能降級，實際指令仍可能失敗。

**三、定案時必須一起修正的共同契約**

最重要的是把回退承諾寫準：

> **回退定義：**  
> 在新分發機制與受支援的契約版本範圍內，改回 `.version` 後，下一次工具指令會安裝並使用該版本；不要求額外 rollback 指令。此操作不還原使用者檔、baseline、外部狀態或工具產生物。若使用者檔已改成舊工具不相容的格式，必須另行還原相容設定。

還有三個必須一致的地方：

- **`.version.local` 優先權：** 有本機覆蓋時，改 `.version` 不會切回 image。回退文件必須要求先解除該工具覆蓋，並讓指令清楚顯示有效來源。
- **launcher 與 baseline 格式：** 保留舊 image 不代表新版 launcher 一定能啟動它，也不代表舊 vendor_kit 能讀新版 baseline metadata。需訂出雙向相容範圍，並驗證升級後再降級。
- **使用者檔保護：** 決策紀錄的「bootstrap 寫進既有 `.gitignore`」與「已存在使用者檔不改」衝突。建議既有 `.gitignore`／justfile 只報告缺少的內容，由 migration PR 或使用者補上；不存在時才建立。

**四、定案前真正需要問清楚的問題**

1. **歷史保留承諾有多廣？**  
   是否接受已採用 release 永久保留？若涵蓋外部 fork、未推送 commit，僅靠 org 掃描無法證明無引用。

2. **回退是否接受上述「工具版本回退」定義？**  
   若要求只改 `.version` 就恢復完整可工作的專案，就必須另外要求設定向後相容；不能同時依賴自動還原使用者檔。

3. **遷移清單究竟是 15 還是 16 個，哪些需要 Jetson 驗收？**  
   urg_node_humble＋isaac 的簡單／複雜覆蓋，不等於 amd64＋arm64 與硬體行為覆蓋。

4. **harness 哪些檔案允許下游編輯、agent 必須在哪裡讀到它們？**  
   這決定哪些進 init，哪些能隨 image 更新。

5. **最低執行環境包含哪些 Docker 元件與版本？**  
   明列 Compose、just 最低版本，以及本機 daemon／rootless／userns-remap 支援範圍；CI 的 Buildx 需求另列，不默認成所有 host 都具備。

6. **哪些專案變數必須寫死在靜態檔案？**  
   列出後確認可以接受人工修改，便能正式關閉模板渲染需求。

其中第 1、2 題會改變核心承諾；其餘可作為遷移與第二工具驗收條件，不必因此延後 #4、#10、#14 的政策定案。
tokens used
54,773
六項傾向可以採用，但 **#3 必須改成可執行的保留政策，#7 必須區分「跳過中間版本」與「省略相容性修改」，#9 必須限定檔案所有權**。另外，「回退＝改回 `.version`」只能保證工具版本回退；若要求連使用者設定、baseline、產生物都恢復，會與「不自動改使用者檔」衝突。

附件沒有完整列出 A/B/C，以下比較各題的實際替代方向，不替草稿杜撰方案編號。repo 現況採附件描述，未另行掃描 15 個 repo。

**一、agy 哪些說法不能直接採信**

1. **前例支持「依版本宣告選工具」，不保證舊版本永遠可取得。**  
   digest 鎖住內容，不等於保存內容。agy 沒有研究 GHCR 保留政策，不能用 Bazelisk／Nix 的回退前例推導「刪舊 image 也沒問題」。GitHub 明確提醒刪除 package 可能破壞依賴它的專案；刪除後的還原還有 30 天與 namespace 可用等條件，不能當長期回退機制。[GitHub 文件](https://docs.github.com/en/packages/learn-github-packages/deleting-and-restoring-a-package)

2. **Renovate 方向正確，但範例不能直接用。**  
   regex manager 預設按整份檔案匹配，agy 的 `^` 不會逐行匹配；你們第一行是 `[tools]`，其範例因此可能完全抓不到工具。必須處理換行邊界，並限定 `.version`，避免更新 baseline metadata。此外，`autoReplaceStringTemplate` 是覆寫替換方式的選項，並非自訂格式一律必填。[regex 文件](https://docs.renovatebot.com/modules/manager/regex/)、[替換設定](https://docs.renovatebot.com/configuration-options/#custommanagersautoreplacestringtemplate)

3. **Dependabot「只支援 Dockerfile 與 docker-compose.yml」已不正確。**  
   官方也列出 Kubernetes manifests／Helm charts 的 image 更新支援。「不能靠一般設定更新這份自訂 TOML」仍是合理結論，但原本的理由過度概括。[GitHub 文件](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-repositories#docker)

4. **Gradle「升級必須跑兩次」說得太滿。**  
   官方說一次通常足以讓舊 Wrapper 執行新版 Gradle；第二次是為了完整更新 Wrapper 本身。這不能證明 vendor_kit 必須採某個自我升級順序。[Gradle 文件](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper)

5. **「覆寫 recipe 後自動由新 recipe 接管」缺少機制。**  
   agy 沒證明執行中的 `just` 會重新載入已改寫的檔案。應明確安排刷新後重新啟動 `just`，或定義需要再次執行；不能把「檔案換新」當作「目前指令已換新」。降級時同樣要驗證。

6. **報告內部也有口徑不一致。**  
   前面主張升級只改版本、延遲安裝，後面手動 upgrade 卻立即 install；兩者都可以設計，但不是相同流程。它還沿用 `.installed_version`、頂層 `just init`、直接調用三方 diff 工具等說法，已不符合你們的 `.stamp`、命名空間與第一版檔案層級 diff 決策。

**二、六項建議與可直接採用的定案文字**

| 議題 | 判斷 | 替代方向與取捨 |
|---|---|---|
| #3 引用保留＋90 天 | 修正後成立 | 單純按年齡／保留最近 N 版會破壞歷史回退；全部永久保留最簡單，但儲存持續增加 |
| #4 Docker 預設共用 | 成立 | 每 repo 自建 cache 增加空間、清理與同步負擔；獨立 daemon 才能提供更強的隔離 |
| #7 直接遷移 | 有條件成立 | 逐版遷移可以沿用舊程序，但增加過渡狀態與修改次數；直跳需要完整對照與驗收 |
| #9 納入 harness | 有條件成立 | 永久分開維護會重複分發機制；一次全部重構則擴大首版範圍 |
| #10 不做 `--migrate` | 成立 | 自動遷移減少手工，但引入使用者檔改寫、衝突與反向遷移問題 |
| #14 不做變數渲染 | 成立 | 渲染較方便，但 baseline 必須追蹤變數、渲染器及其版本；純複製較容易重現 |

這些選擇本身均不需要增加 host 套件；TOML 解析、registry 查詢與檔案處理應放在容器內。

**#3：引用保留＋90 天，先不自動化**

最大問題是「被任何歷史 commit 引用」無法只靠掃描目前 default branch 判定。未推送的 commit、fork、已刪 branch、封存 repo、沒有權限讀取的 repo，都可能讓掃描漏掉引用。

若堅持字面上的「任何歷史引用」，最容易落實的首版政策是：**公開供下游採用的 release image 永久保留；只清理能確認沒有被採用的候選版本。** 90 天不能凌駕引用保護，也不是儲存上限。

保護對象還必須是完整的 multi-arch image。OCI index 會指向各平台 manifest；只保留 index、刪掉看似「無 tag」的子 manifest，仍可能破壞 arm64 或 amd64 的拉取。[OCI 規格](https://github.com/opencontainers/image-spec/blob/main/image-index.md)、[Docker 多平台文件](https://docs.docker.com/build/building/multi-platform/)

> **定案文字：**  
> 任何受支援 downstream 的 `.version` 或 baseline metadata，包括歷史版本，所引用的 image 均不得清除。保護範圍包含 index digest、amd64／arm64 manifest 與其必要內容；release tag 不覆寫、不移除。第一版永久保留已供下游採用的 release image。其他 image 自首次完整確認未被引用起滿 90 天，且刪除前再次確認仍未被引用，才可人工清理；無法確認者保留。第一版不啟用自動刪除。

補充兩個執行邊界：

- baseline 已保存模板副本，也不代表可以忽略 metadata 裡的舊 image ref；依本次政策，它仍是保留根。
- 若 Dockerfile 等其他檔案也直接引用 dist image，必須一併納入，不能只搜尋 `.version`。首次盤點不能把 image 的發布日期直接當成「已確認無引用 90 天」。

**#4：沿用 Docker 共用 image cache**

精確範圍應寫成 **同一 Docker daemon 的 image store**，不是整台機器必然只有一份；rootless、不同 context 或不同 daemon 可能各有儲存。

共用 image cache 不影響各 repo 用不同 digest；但它也不提供永久保存或 repo 間的安全隔離。尤其你們 container 跑完即刪，`docker image prune -a` 可以清掉沒有 container 關聯的 image，Docker 不會讀 `.version` 判斷是否仍需要。[Docker prune 文件](https://docs.docker.com/reference/cli/docker/image/prune/)

> **定案文字：**  
> image cache 使用目前 Docker daemon 的預設 image store，供連到該 daemon 的專案共用；vendor_kit 不建立每 repo 的 image cache，也不自動執行 prune。各 repo 的 `.<name>/` 安裝目錄仍獨立。精確 image 不在本地時，依鎖定 digest 拉取；離線且缺少 image 時明確失敗，不改用其他版本。GHCR 的保留政策與本地 cache 清理由不同責任範圍管理。

因此 #3 與 #4 不矛盾：**GHCR 負責可再次取得，本地 cache 負責減少下載。** 即使 `.<name>/` 還在，缺少 image 時仍可能無法執行你們的 verify。

**#7：直接進新機制，但不能跳過必要修改**

直跳可以省掉 v0.42／v0.43 的 subtree 過渡流程；不能省掉 `.setup.conf`、Dockerfile 路徑、entrypoint、hooks、workflow 等實際相容性調整。

另有兩個草稿缺口：

- 附件的「14 個 v0.41＋jetson_sdk_manager＋isaac」合計是 **16 個**，與題目的 15 個不符。
- 舊 `.base/` 是 git 追蹤的 subtree，新 `.base/` 是可覆寫安裝目錄；不能直接讓 installer 接管而遺失本地修改。

> **定案文字：**  
> 既有 repo 從目前版本直接遷移至新分發機制，不要求先完成 v0.42／v0.43 subtree 遷移。先以 urg_node_humble 驗證簡單案例，再以 isaac 驗證複雜案例；擴大前必須另完成 arm64／Jetson 實機驗收。其餘 repo 依設定相似度與客製程度分批遷移。所有必要的使用者檔修改透過人工審查的 migration PR 完成，不由 install／upgrade 自動改寫。

每個 migration PR 至少要確認：

- 舊 subtree 的自訂內容與有效 hooks 已保留，才移除追蹤並加入 ignore。
- 在全新 clone、沒有既有 `.base/` 的情況下能 install、verify、build 及完成必要 smoke。
- 首次 init 對既有檔案只存「導入時的新模板基準」；它不是 v0.41 的真實祖先，不能據此宣稱已重建舊版三方比對。
- **跨越舊機制的回退使用 migration commit／PR 的還原；「只改 `.version`」適用於接入新機制之後。**

**#9：納入 agent_harness，作為第二個工具**

納入有助於驗證 vendor_kit 是否真的通用。但不能只因內容是 Markdown，就把所有 skills 都判定為使用者檔；分類依據應是所有權。

> **定案文字：**  
> agent_harness 納入同一分發機制，作為 base 最小流程完成後的第二個工具。需要下游編輯的 AGENTS.md 與 skills，透過 init.toml 初次複製，之後只提供 diff／accept；不可由 upgrade 覆寫。需要隨 image 整批更新的執行工具或共用資源保留在 `.<name>/`。第一版不提供使用者檔的區塊合併或自動同步。

必須提早驗證：

- agent 實際讀取的是哪個路徑；若不會讀 `.harness/`，不能把必要內容只放那裡。
- AGENTS.md 與已複製 skills **不會隨 `.version` 自動回退**。
- dest 衝突除了相同檔案，還要涵蓋目錄展開後重疊，以及檔案／目錄互斥。
- 不以 host Python／Node 腳本補足 harness 安裝，避免違反主機限制。

**#10：不提供 `--migrate`**

「保留旗標但預設不執行」仍會留下另一套修改使用者檔的契約；目前沒有必要承擔。

> **定案文字：**  
> 第一版不提供 `just vendor_kit upgrade --migrate`，不保留空殼旗標。upgrade 僅更新版本宣告、工具管理的安裝內容與啟動器，並顯示差異；既有使用者檔不改寫。必要修改以 migration guide 與 diff 說明，由使用者採用。未來若引入自動遷移，必須另立決策，不視為既定 roadmap。

這與 #7 相容：**人工 migration PR 是專案維護工作，不是工具執行時自動遷移。** `accept` 也只表示更新比較基準，不保證使用者已採納所有變更。

**#14：純複製，專案變數由工具在執行期讀取**

此選擇讓模板與 baseline 保持明確的位元組關係。代價是有些靜態檔案仍須人工修改；例如不能假設所有 GitHub Actions 欄位都能直接讀取 `setup.toml`。

> **定案文字：**  
> vendor_kit 第一版不執行模板變數替換、條件渲染或可變目的路徑；init 依固定映射複製原始內容，baseline 保存同一份來源模板。專案參數由各工具在執行期讀取自己的設定；必要的衍生檔寫至工具明確擁有的產生物路徑。必須固化在使用者檔的值由使用者手動調整，不在 upgrade 時重新生成。

`setup.toml` 的格式也要考慮舊工具能否讀取；否則 image 能降級，實際指令仍可能失敗。

**三、定案時必須一起修正的共同契約**

最重要的是把回退承諾寫準：

> **回退定義：**  
> 在新分發機制與受支援的契約版本範圍內，改回 `.version` 後，下一次工具指令會安裝並使用該版本；不要求額外 rollback 指令。此操作不還原使用者檔、baseline、外部狀態或工具產生物。若使用者檔已改成舊工具不相容的格式，必須另行還原相容設定。

還有三個必須一致的地方：

- **`.version.local` 優先權：** 有本機覆蓋時，改 `.version` 不會切回 image。回退文件必須要求先解除該工具覆蓋，並讓指令清楚顯示有效來源。
- **launcher 與 baseline 格式：** 保留舊 image 不代表新版 launcher 一定能啟動它，也不代表舊 vendor_kit 能讀新版 baseline metadata。需訂出雙向相容範圍，並驗證升級後再降級。
- **使用者檔保護：** 決策紀錄的「bootstrap 寫進既有 `.gitignore`」與「已存在使用者檔不改」衝突。建議既有 `.gitignore`／justfile 只報告缺少的內容，由 migration PR 或使用者補上；不存在時才建立。

**四、定案前真正需要問清楚的問題**

1. **歷史保留承諾有多廣？**  
   是否接受已採用 release 永久保留？若涵蓋外部 fork、未推送 commit，僅靠 org 掃描無法證明無引用。

2. **回退是否接受上述「工具版本回退」定義？**  
   若要求只改 `.version` 就恢復完整可工作的專案，就必須另外要求設定向後相容；不能同時依賴自動還原使用者檔。

3. **遷移清單究竟是 15 還是 16 個，哪些需要 Jetson 驗收？**  
   urg_node_humble＋isaac 的簡單／複雜覆蓋，不等於 amd64＋arm64 與硬體行為覆蓋。

4. **harness 哪些檔案允許下游編輯、agent 必須在哪裡讀到它們？**  
   這決定哪些進 init，哪些能隨 image 更新。

5. **最低執行環境包含哪些 Docker 元件與版本？**  
   明列 Compose、just 最低版本，以及本機 daemon／rootless／userns-remap 支援範圍；CI 的 Buildx 需求另列，不默認成所有 host 都具備。

6. **哪些專案變數必須寫死在靜態檔案？**  
   列出後確認可以接受人工修改，便能正式關閉模板渲染需求。

其中第 1、2 題會改變核心承諾；其餘可作為遷移與第二工具驗收條件，不必因此延後 #4、#10、#14 的政策定案。
