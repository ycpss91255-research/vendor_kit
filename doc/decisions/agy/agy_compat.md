這份調查針對 **「工具引擎升版時，對既有專案檔案之相容性承諾、格式演進、跨版本衝突處置」** 整理了 14 個業界代表性前例，並在文末針對 `vendor_kit` 這類「多人協作、Docker 引擎版號漂移」的情境提供深入分析與架構解法。

---

### 一、前例調查總覽表

| 工具 | 1. 格式版本號放哪 | 2. 新版工具讀到舊格式（新讀舊） | 3. 舊版工具讀到新格式（舊讀新） | 4. 破壞性變更定義與公告方式 | 5. 支援期（Floor） | 來源 URL |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Terraform** | • State 檔頂層：`"version": 4`（格式）與 `"terraform_version": "1.x.y"`（執行引擎版號）<br>• Lock 檔：`.terraform.lock.hcl`<br>• 配置檔：`terraform { required_version = ">= 1.5.0" }` | **自動升級並寫回**：1.x 系列自動相容舊 State（0.14+）。執行 `apply` 時會將 State 升版並寫回 backend（進 git 或 S3 會產生異動）。0.12/0.13 時代曾強制要求循序升級（0.12→0.13→0.14→1.0）。 | **拒絕執行**：若 State 檔 `version` 高於本機支援，或含未知 feature，立即中斷報錯（`The state file was produced by a newer version of Terraform...`），絕不靜默覆蓋以防毀損。 | 遵循 **Terraform 1.0 Compatibility Promises**。Major 版本才允許破壞性變更；重大升級提供專用升級指南與指令（如 `terraform 0.12upgrade`）。 | **1.x 期間無限期向後相容**；0.x 時代僅承諾相鄰 minor/checkpoint 升級（禁止跨版跳升）。 | [HashiCorp Terraform 1.0 Promises](https://developer.hashicorp.com/terraform/language/v1-compatibility-promises)<br>[Terraform State](https://developer.hashicorp.com/terraform/language/state) |
| **Cargo (Rust)** | • `Cargo.lock` 頂層：`version = 4`（Rust 1.78+）/ `version = 3`<br>• `Cargo.toml`：`[package] rust-version`（MSRV）與 `edition` | **保守讀取，依賴變動才寫回**：新版 Cargo 完全相容 v1~v3，日常建置讀取舊 lockfile 不主動重寫；只有觸發依賴異動（如 `cargo update` 或新增套件）時才會升級為 v4 並寫回（進 git）。 | **拒絕執行**：舊版 Cargo（< 1.78）讀到 `version = 4` 直接報錯中止（`lock file version 4 was found, but this version does not understand this lock file`）。 | 遵循 Rust RFC 流程（如 RFC 3301 定義 Lockfile v4）。以 **Edition 機制**（2015/2018/2021/2024）隔離語言破壞；lockfile 格式變動極少且視為生態系重大變更。 | **新版對舊格式無限期支援**；舊版對新格式 0 向前相容。 | [Cargo Update Docs](https://doc.rust-lang.org/cargo/commands/cargo-update.html)<br>[RFC 3301 Lockfile v4](https://rust-lang.github.io/rfcs/3301-cargo-lockfile-v4.html) |
| **npm** | `package-lock.json` 頂層：`"lockfileVersion": 1`（npm 5-6）、`2`（npm 7-8 雙相容）、`3`（npm 9+） | **自動遷移並寫回**：npm 7+ 執行 `npm install` 時自動將 v1 遷移為 v2/v3，並直接覆寫 `package-lock.json`（進 git）。 | **降級解析或直接覆蓋**：npm 6 遇到 v2 採降級解析（讀取 `dependencies`，忽略 `packages` 並印出 warning）；但遇到純 v3 則可能解析失敗或退回舊版重產。 | 伴隨 npm Major 釋出（v7, v9）。npm v7 採用「雙軌相容格式（v2 同時包含 v1 與 v2 結構）」作為平滑過渡期。 | 跨 1~2 個 Major（npm 7/8 支援 v1 讀取與轉換，npm 9+ 預設全面產出 v3）。 | [npm package-lock.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json) |
| **Yarn (Berry)** | `yarn.lock` 頂層 YAML block：<br>`__metadata:`<br>`  version: 6`（或 8）<br>`  cacheKey: 8` | **自動遷移並寫回**：Berry（v2+）讀到 Classic（`# yarn lockfile v1`）或舊 Berry 格式，於 `yarn install` 時自動轉換結構並寫回 `yarn.lock`。 | **報錯拒絕**：Yarn Classic 無法解析 Berry 的 YAML lockfile；舊 Berry 讀到高於自身的 `__metadata.version` 時報錯退出。 | 伴隨 Major 升級（v1→v2→v3→v4）；透過 `.yarnrc.yml` 與官方 migration guide 引導。 | 跨 1 個 Major 提供平滑轉換支援。 | [Yarn Architecture & Lockfile](https://yarnpkg.com/configuration/yarnrc) |
| **pnpm** | `pnpm-lock.yaml` 頂層：`lockfileVersion: '6.0'`（pnpm 8）、`'9.0'`（pnpm 9） | **自動遷移並寫回**：新版 pnpm 執行 `pnpm install` 時自動將舊版 lockfile 結構升級為最新版並寫回檔案（進 git）。 | **報錯拒絕**：舊版 pnpm 讀到新版 lockfile 因無法滿足嚴格 schema 檢查而直接退出報錯。 | 隨 pnpm Major 升版發布。Changelog 詳細列出 lockfile 結構優化原因與影響。 | 支援前一個 Major 的 lockfile 自動遷移。 | [pnpm Lockfile](https://pnpm.io/git#lockfiles) |
| **Poetry** | `poetry.lock` 頂層或 metadata：`[package.metadata]` 之 `lock-version = "2.0"` / `"2.1"` | **自動遷移並寫回**：Poetry 2.x 讀取 1.x lockfile，在執行 `poetry lock` 時重新寫入新格式與新版號（進 git）。 | **報錯拒絕**：舊版 Poetry 讀到高版 `lock-version` 拋出 validation 或 parse error。 | 伴隨 Poetry Major 升版發布（如 1.x 到 2.0）；Release notes 提供遷移指南。 | 支援前一個 Major 升級。 | [Poetry CLI Lock](https://python-poetry.org/docs/cli/#lock) |
| **uv** | `uv.lock` 頂層 TOML：<br>`version = 1`（Schema Version）<br>`revision = N`（向後相容版次） | **自動相容**：只要 Schema `version` 相同，即使 `revision` 較舊也能完全正常解析並相容運作。 | **雙軌處理**：<br>• `version` 高於本機：**拒絕執行並報錯**。<br>• `revision` 高於本機：**安全相容忽略**。 | **將 lockfile schema 列入 Public API**。承諾只有在破壞性變更時才在 Minor 釋出中 bump `version`；相容性新增只 bump `revision`。 | 相同 `version` 內所有 patch/minor 保證相容。可在 `pyproject.toml` 宣告 `required-version`。 | [uv Lockfile Format](https://docs.astral.sh/uv/concepts/projects/sync/#lockfile-format) |
| **Copier** | • 專案檔：`.copier-answers.yml`（含 `_commit`, `_src_path`）<br>• 模板檔：`copier.yml` 宣告 `_min_copier_version: "9.0.0"` 與 `_migrations` 串列 | **自動按版本鏈遷移並寫回**：`copier update` 比對 answers 檔之 `_commit`，依序執行 `_migrations` 中的 `before`/`after` 腳本，升級完成後覆寫 `.copier-answers.yml`。 | **立即中止**：若本機 Copier 版本 < 模板要求的 `_min_copier_version`，直接報錯中止，強制要求升級。 | 模板採 SemVer 標籤。破壞性變更必須透過 `_migrations` 顯式提供升級腳本（提供 `$VERSION_FROM`, `$VERSION_TO` 環境變數）。 | 依賴模板作者定義的 migration 鏈；理論上支援任意跨版跳升（只要中間各版 migration 連貫）。 | [Copier Updating](https://copier.readthedocs.io/en/stable/updating/)<br>[Copier Min Version](https://copier.readthedocs.io/en/stable/configuring/#min_copier_version) |
| **Renovate** | `renovate.json` / `renovate.json5`（無單一數值版號，各欄位語義版控） | **記憶體自動遷移，PR 寫回**：執行時在記憶體中自動相容舊設定並輸出 deprecation warning。若開啟 `configMigration: true`，會由 Bot 自動向 repo 發起 PR 覆寫舊檔。 | 報錯退出：舊版執行到新版新增的語義欄位會報 unknown option。 | 提供 `renovate-config-validator --strict`，若存在過時需遷移欄位則回傳非 0 exit code 阻擋 CI。變更公告於 Major changelog。 | 廢棄設定通常在記憶體動態轉譯支援維持至少 1~2 個 Major 週期才徹底移除。 | [Renovate Config Validator](https://docs.renovatebot.com/renovate-config-validator/)<br>[Renovate Config Migration](https://docs.renovatebot.com/config-overview/#config-migration) |
| **pre-commit** | `.pre-commit-config.yaml` 頂層：`minimum_pre_commit_version: '3.2.0'` | **完全相容**：新版工具無條件相容舊格式（未設定時預設值為 `'0'`）。 | **立即退出**：若本機版本 < 宣告版本，立即退出（exit code 1）並印出升級指示：`The config requires pre-commit version X but version Y is installed...`。 | 語法重大調整透過 Major/Minor 發布，依賴 `minimum_pre_commit_version` 防護罩避免舊版以未定義行為解析。 | 永久向後相容。 | [pre-commit Configuration](https://pre-commit.com/#pre-commit-configyaml---top-level) |
| **just** | `justfile` 頂部宣告：<br>`set minimum-version := "1.55.0"` | **完全相容**：新版 just 完全支援舊版語法。 | **解析錯誤或阻擋退出**：< 1.55 會因不認識該 setting 出現語法錯誤；>= 1.55 但低於需求時直接報版本過低錯誤並中止。 | SemVer 保證 1.x 語法向下相容；新增特性透過 minimum-version 機制讓 script 作者主動限制舊版。 | 1.x 期間永久向後相容。 | [just Settings (minimum-version)](https://just.systems/man/en/settings/minimum-version.html) |
| **Gradle Wrapper** | `gradle/wrapper/gradle-wrapper.properties` 內之 `distributionUrl` | **相鄰 Major 保證相容**：升級時執行 `./gradlew wrapper --gradle-version X.Y.Z`，會將新版 URL、wrapper jar 與 gradlew 腳本更新並寫回 git。 | **不存在此問題（架構消除）**：專案不依賴全域 Gradle，而是由 `gradlew` 讀取 properties 自動下載指定版號執行。 | API 與設定廢棄至少保留 1 個完整 Major 週期，並透過 `--warning-mode=all` 警告；Major 升版才移除。 | 僅保證相鄰 Major 升級（如 7.x 升至 8.x）；官方提供完整 Migration Guide。 | [Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)<br>[Gradle Feature Lifecycle](https://docs.gradle.org/current/userguide/feature_lifecycle.html) |
| **Docker Compose** | `docker-compose.yml` 頂層欄位：`version: "3.8"`（歷史上） | **廢棄並忽略（Obsolete）**：Compose V2（Compose Spec）統一規格後，**將 `version` 欄位宣告為 obsolete**。新引擎遇到該欄位僅印出警告並直接忽略，統一採用最新 Spec 解析。 | **報錯拒絕**：舊版 Python `docker-compose` v1 讀到不支援的高版本號（如 3.9）或缺少 version 的 Compose Spec 會直接報錯拒絕。 | Compose Spec 獨立成立；宣布 Compose V1 EOL 並提供 `docker compose`（Go plugin）遷移手冊。 | Compose V2 完整容納 v2/v3 大多數設定，打破了嚴格的數字版本閘門。 | [Compose File Version and Name](https://docs.docker.com/compose/compose-file/04-version-and-name/)<br>[Compose Specification](https://compose-spec.io/) |
| **Git** | `.git/config` 內：<br>`core.repositoryformatversion = 0` 或 `1`<br>搭配 `[extensions]` 區塊 | **平滑相容**：新版 Git 完全相容 format 0；日常讀取不會主動將 0 升級為 1，只有在啟用需要 extension 的新特性時才改寫。 | **立即拒絕全部操作**：<br>• format version > 1：拋出 `fatal: Expected git repo version <= 1`。<br>• version = 1 且含未知 extension：拋出 `fatal: unknown repository extension: <name>` 中止所有操作，防毀損。 | 核心倉庫結構變更極其嚴苛，透過 Git mailing list 與 Documentation 規範；引入 `extensions.*` 實現模組化向前相容隔離。 | Format version 0 永久向後相容。 | [Git Repository Layout](https://git-scm.com/docs/gitrepository-layout)<br>[Git Config core.repositoryformatversion](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corerepositoryFormatVersion) |
| **Kubernetes** | YAML 宣告頂層：<br>`apiVersion: <group>/<version>`（如 `apps/v1`, `policy/v1`） | **記憶體自動無損轉換**：若該版本仍受支援，API Server 透過 Internal Hub 在記憶體中轉為 storage version；若已廢棄但未移除，HTTP Response header 附加 `Warning: 299`；若已移除則報 404/422。 | **拒絕執行**：舊叢集 API Server 不認識新 `apiVersion`，回傳 `no matches for kind ... in version ...`。 | 遵守官方 **Deprecation Policy**：<br>• GA API：宣告廢棄後**至少保留 12 個月或 3 個 release**。<br>• Beta API：至少保留 9 個月或 3 個 release。<br>• 提供 `kubectl-convert` 工具進行 YAML 批次升級。 | 嚴格的 12 個月 / 3 個 release 緩衝期。 | [Kubernetes Deprecation Policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/) |
| **Semantic Versioning** | 規格書第 1 條要求宣告 Public API | 升級 Minor/Patch 必須保持向後相容；新版若無法讀取舊格式，或破壞舊格式語義，**視為 Public API 破壞**。 | 舊版若因新格式無法運作，屬於 Forward Incompatibility（前向不相容）。 | **SemVer 官方 FAQ 明確界定**：Public API **包含 CLI 參數、連線協定（Wire Protocols）、檔案格式（File Formats）與 Schema**。任何檔案格式不相容改動必須 bump MAJOR 版號。 | 廢棄任何 Public API / 格式欄位，應在 MINOR 發布 Deprecation Notice，並至少維持一個 MINOR 週期後才能在下個 MAJOR 移除。 | [Semantic Versioning 2.0.0](https://semver.org/#semantic-versioning-specification-semverorg) |

---

### 二、對「同一專案多人用不同引擎版」的情境，前例如何處理？

在多人協作同一專案時，若成員 A 使用新引擎（v7），成員 B 仍停留在舊引擎（v3），最常見的痛點是：
1. **版本踩踏與 Git Diff 噪音（Lockfile Ping-Pong / Churn）**：A 執行指令將 lockfile/宣告檔升級為新格式並 commit；B pull 之後用舊引擎跑指令，舊引擎又把檔案「降級」改寫回舊格式，導致 Git 歷史充斥無意義的格式互踩與 merge conflict。
2. **本機突然爆掉（Broken Local State）**：A 升級了狀態檔或引入新欄位，B 用舊版執行直接 crash（例如 Terraform state 或 Cargo lockfile v4）。
3. **未定義行為（Silent Corruption）**：舊引擎未驗證版本號，靜默忽略未知新欄位，產出不完整的檔案甚至破壞專案 baseline。

針對此問題，業界前例發展出以下 **5 種處置範式**，可作為 `vendor_kit` 架構設計的直接借鑒：

---

#### 模式 1：強阻擋與快速失敗（Hard Guard & Fail Fast）—— 防禦性最徹底
*   **代表案例**：`pre-commit`（`minimum_pre_commit_version`）、`just`（`set minimum-version`）、`Terraform`（`required_version`）、`uv`（`[tool.uv] required-version`）。
*   **機制**：
    專案內的宣告檔（如 `.vendor_kit/version.toml`）強制包含最低引擎版號約束。引擎啟動時的第一步，**在讀寫任何業務檔案前，先校驗當前引擎版號是否滿足宣告值**。
*   **行為效果**：
    *   成員 A 升級引擎至 v7，專案宣告檔被 bump 為 `min_engine_version = "v7"` 並進 git。
    *   成員 B 尚未升級（本機為 v3），執行指令時，v3 引擎在啟動時發現 `v3 < v7`，**立即以非零狀態碼（exit 1）中斷退出**。
    *   印出可操作的提示：`Error: This project requires vendor_kit >= v7 (current engine: v3). Please update your docker image via 'docker pull ...'`。
*   **價值**：
    **舊引擎絕不讀取、絕不改寫、絕不生成任何檔案**，從根本上杜絕了「舊引擎把檔案降級寫回」的 Git 互踩問題。

---

#### 模式 2：自包含包裝器（In-repo Wrapper / Bootstrap）—— 從架構上消滅版本漂移
*   **代表案例**：`Gradle Wrapper`（`gradlew`）、Node.js `Corepack`（配合 `package.json` 的 `packageManager` 欄位）。
*   **機制**：
    專案倉庫中追蹤一個輕量級的啟動薄殼（Wrapper script），開發者**禁止直接調用全域工具**，所有操作皆經由 Wrapper（如 `./gradlew`）。
*   **對應到 `vendor_kit`（Docker 容器引擎）的作法**：
    *   下游專案中的 `entry.just` 或 `vendor.just` 本身就是薄殼。
    *   目前常見的危險寫法是 `docker run vendor_kit:latest ...`（導致有人是昨天 pull 的，有人是半年前 pull 的）。
    *   **Wrapper 最佳實踐**：在 `.vendor_kit/version.toml` 中記錄 `engine_image_tag = "v7.2.0"`。薄殼 `entry.just` 執行時，動態讀取此欄位，直接組裝指令 `docker run ghcr.io/.../vendor_kit:${ENGINE_TAG}`。
*   **價值**：
    不管成員 B 本機原本有什麼版本的 Docker image，只要他 pull 了 repo，薄殼就會自動調用或拉取專案所指定的精確 tag，**全團隊成員與 CI 執行的始終是同一個 Docker image，徹底根除版本漂移**。

---

#### 模式 3：保守讀取，非必要不主動改寫（Non-destructive Read-Only Compatibility）
*   **代表案例**：`Cargo`（Rust 1.78+ 對 `Cargo.lock` v3）、`Git`（對 `core.repositoryformatversion = 0`）。
*   **機制**：
    新版引擎讀到舊版檔案時，在記憶體中內部向上相容解析；**如果當次操作沒有用到「必須升級格式才能儲存的破壞性新功能」，新引擎不會主動把檔案改寫成新格式**。
*   **行為效果**：
    *   成員 A 換了新引擎，但只是執行一般的 check、verify 或不涉及結構變更的日常操作，新引擎讀取舊的 `.vendor_kit.toml` 並保持原樣，不修改檔案。
    *   只有當 A 顯式執行了升級指令（例如 `vendor-kit migrate` 或升級 baseline 定義）時，才觸發格式升級。
*   **價值**：
    避免成員 A 只是開專案看一眼或跑個測試，就把整個 repo 的 metadata 檔案版本 bump 上去，導致其他人被強迫升級。

---

#### 模式 4：過渡期雙相容結構（Bridge / Dual-Format Schema）
*   **代表案例**：`npm 7` 的 `lockfileVersion: 2`。
*   **機制**：
    當格式不得不改版時，新格式在過渡期內同時保留舊版欄位與新版欄位。
*   **對應到 `vendor_kit` 的 metadata**：
    若 `.vendor_kit.toml` 從 v1 演進到 v2，新引擎在寫入時，可同時維護舊引擎看得懂的頂層欄位，並把新版擴展放在新 table 中。舊引擎只讀舊 table（需配合嚴格忽略未知欄位），新引擎讀新 table。當團隊確認全員過渡完成後，再於下個 Major 廢棄舊欄位。

---

#### 模式 5：專用遷移命令與 CI 一票否決（Centralized Migration & CI Gate）
*   **代表案例**：`Renovate`（`renovate-config-validator --strict`）、`npm ci`（vs `npm install`）、`Terraform 0.13upgrade`。
*   **機制**：
    *   **CI 強制檢驗**：在 `ci/check.sh` 中加上版本一致性檢查（例如校驗 `gen/.stamp` 記錄的產生版號與專案宣告的引擎版號是否一致）。如果有成員本機用舊版產生了錯誤檔案並推上 PR，CI 立即報警紅燈，不允許合入主線。
    *   **顯式遷移**：格式遷移（例如 v3 檔案轉 v7）不做為一般日常運行的副產物，而是做成顯式指令（如 `just vendor-kit-upgrade`），且升級會自動建立一個獨立乾淨的 Git commit，方便 code review。

---

### 三、總結：對 `vendor_kit` 各專案檔相容性承諾的建議方針

綜合上述前例，針對 `vendor_kit` 下游專案檔案的設計矩陣建議如下：

1.  **`.vendor_kit/version.toml`（宣告檔，進 git）**：
    *   **承諾**：放 `schema_version = 1` 與 `min_engine_version = "v7"`。
    *   **舊讀新**：舊引擎（v3）讀到宣告檔若發現本機 `< min_engine_version`，**立即 fail-fast 報錯中斷**，禁止往下執行。
2.  **`.vendor_kit/baseline/<repo>/.vendor_kit.toml`（內部 metadata）**：
    *   **承諾**：加上 `format_version = 1`。
    *   **新讀舊**：新引擎保證支援跨版（例如 v3 到 v7）的自動遷移（仿效 Copier 的 sequential migrations 概念）。
    *   **改寫原則**：日常唯讀指令不改寫；變更 metadata 時若升版，一次性更新 `format_version`。
3.  **薄殼 Just 檔（`entry.just`, `vendor.just`）**：
    *   **承諾**：薄殼內寫死引用的 Docker tag（或讀取 `version.toml` 動態決定 tag），**仿效 Gradle Wrapper**，使專案具有自包含鎖定引擎版本的能力，從根源消除本機版本漂移。
4.  **`gen/.stamp` 與 `ci/check.sh`**：
    *   **承諾**：Stamp 內寫入產出該印記的 `engine_version`。CI 執行 `ci/check.sh` 時校驗 Stamp 內的版本是否與主線宣告的引擎版本吻合，若有團隊成員用舊引擎偷跑並 commit，CI 直接擋下。
