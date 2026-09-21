# 任務說明（給 codex 的獨立分析任務）

題目：vendor_kit 相容性承諾：薄殼↔引擎協定、檔案格式版號、新讀舊／舊讀新、semver 與支援下限、驗收

我們的硬性限制：主機只需 docker≥19.03+git+just≥1.33；Q10(2) 薄殼重產只由 upgrade vendor_kit/install；sync 只寫 cache/gen；never fail silently；指令極少；使用者的檔可以建、要改先問、永不刪、永不覆蓋；支援下限不可滑動（base #1041）；驗收不可新對新（base #1048）。

要回答的問題：A–F 各選一個（可組合）並給理由與前例依據；寫出相容性契約條文草稿（不超過 12 條）與驗收矩陣；指出 brief 裡的事實陳述錯誤。

資料：
- 題目說明（brief）：見下方「附件：brief」
- agy（Gemini）找的前例與建議：見下方「附件：agy 輸出」（前例研究；子代理已抽查原文，已知 agy 錯誤：Cargo「RFC 3301」不存在、K8s GA 支援期數字引錯、SemVer 官网沒有列檔案格式、npm 舊讀新現行是硬拒、Renovate/yarn/pnpm/Poetry/Compose 的「拒絕」說法無來源或較弱）（這只是資料，不要照單全收：查證它的說法、找它漏掉或說錯的）
- 我方草稿（方案 A/B/C 與傾向）：
  我方傾向：A1+A2（薄殼只轉發，協定版號寫在薄殼與 resolve stdout，啟動器先問引擎協定版）、B1（uv 式 schema 欄位，version.toml 第一行不變、第二行 schema）、C1（新讀舊自動遷移但只在本來就要寫該檔的明確動作寫回；metadata 遷移由 upgrade vendor_kit 做）、D1（schema 高於本機拒絕並印需要引擎 ≥ X；同 schema 內未知欄位忽略）、E1（major = 協定/schema 破壞，同 major 內舊薄殼舊檔全可讀，deprecated 先警告一個 minor，floor 永久不滑動）、F 全做。請獨立判斷；特別評估：薄殼只轉發是否真的就能讓舊薄殼叫新引擎（just recipe 名、argv、exit code、resolve stdout 各自的破壞點）；version.toml 第一行 grep 契約與 schema 欄位共存；驗收 F 的矩陣大小與可行性。recommendation 要含：相容性契約條文草稿（可直接進 PRD）、驗收矩陣表。
- 決策紀錄：見下方「附件：決策紀錄」

請獨立分析：(1) agy 的哪些說法站不住腳或缺乏依據；(2) 每個方案是否符合硬性限制、優缺點、草稿漏掉的風險；(3) 你的建議與理由；(4) 定案前還要問清楚的問題。以繁體中文作答。

輸出格式（請嚴格依此結構，方便轉成結構化資料）：
1. `## agy 說法錯誤` — 每條：claim / why
2. `## 方案評估` — 每個方案（A1/A2/A3、B1/B2/B3、C1/C2/C3、D1/D2、E1/E2、F）：是否符合硬性限制（是/否）、pros、cons、草稿漏掉的風險
3. `## 建議` — A–F 各選什麼、相容性契約條文草稿（≤12 條）、驗收矩陣表
4. `## 理由`
5. `## 定案前要問的問題`

註：你在 read-only sandbox 中，讀不到本機檔案與網路；所有需要的資料都已貼在下方附件。

---

# 附件：brief

# 題目：vendor_kit 的相容性承諾（引擎跨版時對已存在的專案檔／薄殼／bootstrap.sh 承諾什麼）

## 誰跟誰之間有相容問題（先釐清，這決定題目範圍）
引擎版本寫在 `version.toml` 第一行，所以「引擎」與「它寫的檔」在同一個 commit 內永遠一致；不一致只發生在三個介面：
1. **薄殼 ↔ 引擎**：`.vendor_kit/entry.just`、`vendor.just`、`ci/check.sh` 是舊引擎產的（tracked），Renovate／人把第一行升到新引擎後、`upgrade vendor_kit` 重產薄殼之前，**舊薄殼要能叫新引擎**（至少要能跑 `upgrade vendor_kit` 這條救援路徑）。base 的教訓（#915/#1077/#1110，ADR-6 修六次）：升級由使用者手上已出貨的舊 driver 驅動，新版才知道的路徑／行為它不知道；「the upgrade REMOVED THE COMMAND THAT PERFORMED IT」。
2. **bootstrap.sh ↔ 引擎**：使用者可能拿到很久以前的 bootstrap.sh（它內嵌自己那版的引擎 ref，所以正常不會叫到新引擎）；但 `--local` 給的 image 可能任意版本。
3. **新引擎 ↔ 舊引擎寫的檔**：`version.toml`、`baseline/<repo>/.vendor_kit.toml`（metadata）、`gen/<repo>.stamp`、`gen/.stamp`——新引擎讀舊格式（隔很久才升：v3 → v7）；以及 `dev vendor_kit -i` 用舊 image 讀新格式（舊引擎讀新格式）。
另外「同一專案多人用不同引擎」：因為引擎 ref 在 version.toml 裡，pull 到同一 commit 的人用同一引擎；差異只在誰還沒 pull。

## 前例（已查證，見 agy/agy_compat.md 與子代理報告）
- 格式版號放檔案裡：Terraform state `version:4`、Cargo.lock `version = N`、npm `lockfileVersion`、uv `version`+`revision`、Poetry `lock-version`、git `core.repositoryformatversion`+extensions。
- 新讀舊：Terraform/Cargo/npm 自動讀，Cargo「找到舊格式就保留，只有本來要寫的操作才改寫」（encode.rs）。Copier 的 `_migrations` 依版本範圍在 update 時跑。
- 舊讀新：Terraform/Cargo/npm(arborist maxLockfileVersion)/uv/pre-commit 全部**拒絕並印升級指示**；Poetry 範圍內只 warning。npm 原始碼註解：舊 client「must not drop」讀不懂的資料。
- 宣告最低版本：pre-commit `minimum_pre_commit_version`、Copier `_min_copier_version`、just `set minimum-version`、uv `required-version`。
- 破壞定義：uv「schema version 是 public API 的一部分，只在 minor（uv 的 breaking 單位）bump」；SemVer FAQ「先 minor 標 deprecated，下個 major 移除」；K8s GA「同一 major 內不得移除」；Terraform 1.x「升級不需額外指令」。
- git 策略：盡量不 bump 整庫版本，個別檔案各自版號 + 新資料要能被舊 client 優雅忽略。
- base 的教訓（#1041 open）：「A compatibility obligation is permanent; a sliding window expires」——支援下限（floor）要明定且只往前不往後滑；（#1048）驗收若用「剛 build 的引擎 + 乾淨 fixture」就是新對新、結構上不可能失敗，必須用**已釋出的薄殼／bootstrap.sh** 驅動候選引擎、連升兩次、跨多版、降版。

## 已定案的相關限制
Q10(2)：薄殼重產只由 `upgrade vendor_kit`／install 做，先比對 hash；sync 只回 1 提示。v2.2 C：resolve 的 stdout 協定版本化（第一行 `vk-resolve/1`）。v2.3：`gen/.stamp` = 引擎 ref + 薄殼 hash。動詞語意跟 base。never fail silently。指令極少。

## 候選（請獨立裁定、可組合）
A. **薄殼 ↔ 引擎協定**：(A1) 薄殼只含「呼叫引擎 + 轉發 argv」，協定 = 引擎 CLI 的 argv 與 exit code + resolve stdout 版號；引擎承諾在同一 major 內接受所有舊薄殼；薄殼裡寫 `# vendor_kit-shell/1`。(A2) 薄殼也帶 `set minimum-version` 式的自檢：啟動器先問引擎 `--shell-protocol`，不合就印「請 upgrade vendor_kit」。(A3) 不承諾：每次引擎升級都先 `upgrade vendor_kit`（但這條路徑本身就靠舊薄殼叫新引擎——雞生蛋）。
B. **檔案格式版號**：(B1) uv 式：每個 vendor_kit 寫的 TOML 有 `schema = N`（破壞性）；version.toml 第一行維持 `vendor_kit = "…"`（啟動器 grep 契約）、第二行 `schema = 1`。(B2) git 式：不放全域版號，每檔各自 `schema`，新增欄位設計成舊引擎可忽略。(B3) 只靠引擎 semver，不放格式版號。
C. **新引擎讀舊檔**：(C1) 自動遷移但只在「本來就要寫該檔的明確動作」時寫回（Cargo 式；配合 Q10：`upgrade vendor_kit` 負責 metadata 遷移，sync 只讀不寫）。(C2) 要求手動 `migrate` 指令（多一個動詞）。(C3) 拒絕跨太多版（例如只保證 N-1 major）。
D. **舊引擎讀新檔**（`dev vendor_kit -i` 舊 image、或未 pull 的人…實際上後者不會發生）：(D1) schema 高於本機 → 拒絕並印「需要引擎 ≥ X」；未知欄位在同 schema 內忽略（uv revision 精神）。(D2) 只 warning。
E. **支援下限與 semver**：(E1) 引擎 major = 協定或 schema 破壞（需手動步驟）、minor = 功能、patch = 修；承諾：同 major 內舊薄殼／舊檔全部可讀；deprecated 先在 minor 警告一個 minor 以上才在下個 major 移除；floor = 上一個 major 的最後一版薄殼（永久，不滑動）。(E2) 不用 major，改 floor 版號常數寫在 PRD。
F. **驗收**：用 GHCR 上**已釋出**的每一個受支援薄殼／bootstrap.sh 版本驅動候選引擎跑完整流程；連升兩次；跨多版（floor → 候選）；降版（`upgrade vendor_kit -t` 舊版）；「就地升級後的專案 == 全新 install 的專案」比對 vendor_kit 自有產物（base #1057）。
我方傾向：A1+A2、B1、C1、D1、E1、F 全做。

---

# 附件：agy 輸出

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

## 附註：子代理對 agy 引用來源的 URL 檢查與原文抽查紀錄（urlcheck_compat.txt）

200 https://compose-spec.io/
200 https://copier.readthedocs.io/en/stable/configuring/#min_copier_version
200 https://copier.readthedocs.io/en/stable/updating/
200 https://developer.hashicorp.com/terraform/language/state
200 https://developer.hashicorp.com/terraform/language/v1-compatibility-promises
200 https://doc.rust-lang.org/cargo/commands/cargo-update.html
200 https://docs.astral.sh/uv/concepts/projects/sync/#lockfile-format
200 https://docs.docker.com/compose/compose-file/04-version-and-name/
200 https://docs.gradle.org/current/userguide/feature_lifecycle.html
200 https://docs.gradle.org/current/userguide/gradle_wrapper.html
200 https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json
200 https://docs.renovatebot.com/config-overview/#config-migration
404 https://docs.renovatebot.com/renovate-config-validator/
200 https://git-scm.com/docs/git-config#Documentation/git-config.txt-corerepositoryFormatVersion
200 https://git-scm.com/docs/gitrepository-layout
404 https://just.systems/man/en/settings/minimum-version.html
200 https://kubernetes.io/docs/reference/using-api/deprecation-policy/
200 https://pnpm.io/git#lockfiles
200 https://pre-commit.com/#pre-commit-configyaml---top-level
200 https://python-poetry.org/docs/cli/#lock
404 https://rust-lang.github.io/rfcs/3301-cargo-lockfile-v4.html
200 https://semver.org/#semantic-versioning-specification-semverorg
200 https://yarnpkg.com/configuration/yarnrc
200 https://docs.renovatebot.com/config-validation/
200 https://just.systems/man/en/settings.html
200 https://rust-lang.github.io/rfcs/
200 https://github.com/rust-lang/cargo/pull/12852
200 https://helm.sh/docs/topics/charts/
200 https://docs.docker.com/reference/compose-file/version-and-name/
200 https://docs.astral.sh/uv/concepts/projects/layout/
200 https://pre-commit.com/
200 https://pnpm.io/settings
200 https://python-poetry.org/docs/basic-usage/
404 https://yarnpkg.com/features/lockfile
404 https://docs.gradle.org/current/userguide/upgrading_major_version_8.html
uv versioning 200
200 https://docs.astral.sh/uv/concepts/resolution/#lockfile-versioning
200 https://docs.gradle.org/current/userguide/upgrading_version_8.html
200 https://docs.gradle.org/current/userguide/upgrading_version_7.html
200 https://docs.docker.com/reference/compose-file/legacy-versions/
# --- 原文抽查（gh api / curl 取得的來源，存於 compat_src/）---
verified hashicorp/terraform internal/states/statefile/read.go  (format version guard, legacy v1-3 upgraded, v0 binary rejected)
verified rust-lang/cargo src/resolver/encode.rs + resolve.rs   (V1..V4 + with_rust_version MSRV table; error "does not understand this lock file")
verified doc.rust-lang.org/nightly/cargo/CHANGELOG.html         (1.78 stabilize v4 #12852; 1.83 default v4 #14595)
verified npm/cli workspaces/arborist/lib/shrinkwrap.js           (maxLockfileVersion=4, ELOCKFILEVERSION refusal; parse-conflict-json)
verified yarnpkg/berry packages/yarnpkg-core/sources/Project.ts  (LOCKFILE_VERSION=10; __metadata.version; lockfileNeedsRefresh)
verified python-poetry/poetry src/poetry/packages/locker.py      (_VERSION 2.1, _READ_VERSION_RANGE ">=1,<3", warn/raise)
verified pre-commit/pre-commit pre_commit/clientlib.py           (check_min_version error text)
verified casey/just src/compile_error.rs + CHANGELOG 1.55.0     ("justfile requires just {minimum} or later")
verified docker/compose 1.29.2 compose/config/config.py          (version regex ^[1-3]+(\.\d+)?$, v1 rejected)

---

# 附件：決策紀錄

# 討論紀錄（grilling，2026-09-18）
- Q1 定案：自寫 + 主機 docker（拉 image）+ 引擎內 git merge-file；第一版不放 vendir/Copier。
- 第 1 頁討論：
  - base 的 update/upgrade 確認對齊 apt（ADR-00000011 §2）；我們跟 base。
  - 專案層動詞 `install`（第一次建立、再跑 = 修復、要求已是 git repo、不做 git init）↔ `uninstall`；bootstrap.sh = 下載引擎 + 呼叫 install；`--repair` 取消。引擎內部「拉 image 展開」改名 fetch。—— 使用者 OK。
  - `ensure` → `sync`：使用者 OK，待 codex 批判確認。
  - codex 批判（agy/codex_verbs.md）：同意 install/uninstall、同意 sync；附帶條件：`install <repo>` 誤用要導向 `add`；help 明寫「已接入的專案跑 sync，不是 install」；sync help =「依 .version 重建本機工具快取與產生的模組；不修改鎖定版本或需提交的檔案」；fresh clone 的 sync 入口在 gen/ 不存在時也要能跑（recipe 放 tracked vendor.just 已解）；frozen 模式要明寫多禁止什麼；uninstall 要交代初始檔處理（保留並印清單）。內部展開步驟名：codex 建議 materialize（非 fetch）——內部名，不對外。
- 第 1 頁便條 (3)(4)(6)(11) 回覆：
  - add = 正式使用（GHCR、進 git、共享）；dev = 開發用（本機目錄、.version.local、只在本機）；**dev 要求工具已在 .version**。使用者 OK，要記 issue/ADR。
  - update/upgrade 語意 OK；upgrade 含 install+合併+推 baseline OK。
  - remove 不開 --purge OK；bootstrap 第二次拒絕 → 作廢（bootstrap = 下載 + install，再跑 = 修復）。
  - 「vendor_kit 會碰使用者的東西」只有三處：根 justfile 一行、初始檔（add 建立不覆蓋；upgrade 合併；**永不刪**——新版刪除的檔改為只 warn 不刪）、.git/info/exclude 我們的區塊（不碰 .gitignore）。使用者要求再研究：根 justfile 能否不碰（base 式 symlink？）、.version 改名或收進 .vendor_kit/、初始檔隔離方式 → agy + Claude/codex 雙軌（進行中）。
  - (11) dev 自身：**要支援**（使用者定案）。機制 = .version.local `vendor_kit = "<本機 image tag>"`，`dev vendor_kit -i/--image <tag>`；驗收測試 = 用剛 build 的引擎 image 在乾淨下游 fixture repo 跑完整流程，放 test 分層最後一關。
- 隔離題定案（2026-09-18）：
  - **不變量**：vendor_kit 對使用者的檔——可以建（要明確說明建立或修改了什麼）、要改先問（`-y` 免問）、永不刪、永不覆蓋。
  - A 根 justfile：無 → 建（import 一行 + default: @just --list）；有 → 詢問加一行，`-y` 直接加並印出；uninstall 對稱詢問，只刪與我們寫的完全相同的行。不接管根檔（base 會對齊我們，共存問題消失）。
  - B 全收進 `.vendor_kit/`：version.toml、version.local.toml、cache/<repo>/、.gitignore（自有）；不碰 .git/info/exclude 與使用者 .gitignore；工具 recipe 用 `cd "{{justfile_directory()}}"` 回專案根。
  - C 初始檔：add 建（已存在不納管、不覆蓋）；upgrade 逐檔判斷後**詢問**（沒改→換新版？；都改→三方合併？），`-y` 免問，衝突留標記回 2，baseline 推到新版；remove/uninstall 不刪只印清單；CI 無 -y 需改檔 → 1 印清單。
  - PRD/ADR 一律中文；PRD 結構學 base（不變量／原則／衝突優先序；機制放 ADR）。
- Q3 定案：vendor_kit 只輸出一個命名空間 `vendor_kit`；工具 `dist/just/<ns>.just` 每檔一個頂層命名空間，數量工具自己決定；add 時跨工具撞名報錯拒絕。（proto ADR-0002 §4 與此一致）
- Q4 進行中：工具 image 單架構 amd64 + arm64 CI 驗收守門 vs 多架構 index。實測：amd64 主機（無 qemu）docker create --platform linux/arm64 + docker cp 展開 arm64-only 純資料 image 成功（scratchpad/archtest）。
- PRD 草稿已寫（src/doc/PRD.md 234 行、doc/adr/README.md、TEMPLATE.md）；子代理列出 10 處來源矛盾，除 Q4／just 最低版本／多命名空間（已定）外，一律以 grilling.md 為準；CONTEXT.md 待同步。
- Q4 定案：工具 image **多架構 amd64+arm64**（同一次 buildx、COPY-only、CI 驗兩平台內容一致）；引擎 image 同；平台 Linux amd64 + arm64（Jetson、RPi 64 位元）、WSL2；armv7 不支援；docker 最低 19.03；印記記 index digest（與 version.toml 一致）。多架構測試開 issue 追蹤，做完才關。
- Q5 定案（Renovate）：vendor_kit 本身無 bot、不 commit、不開 PR；Renovate 是下游自選；PR 只改 version.toml 一行，初始檔合併由維護者本機 `upgrade <repo> -y` → commit → push（Renovate 預設不動有人推過的分支，PR body 警告勿勾 rebase）。**PR 的 CI 必須以新版跑完整流程（sync frozen → verify → upgrade --dry-run → 工具測試 → 專案測試），一行改動本身不可能出錯，不構成通過依據；需合併 → 1 印指令；人補完 push 後全部再跑一次。** bot commit／postUpgradeTasks 不採（附註）。
- Q7 定案（雙軌一致）：引擎 image 公開、工具自決、認證是主機的事；公開不可逆要提醒。
- Q8：維持 just ≥ 1.33（來源：[group] 放 mod 上需 1.33 #2263）；CI 用 1.33.0 跑完整 fixture 才定案。
- Q9 定案：自身升級後停下、退出 1、要求重跑；契約「同一次 just 呼叫內不會看到新 recipe」。
- Q6 雙軌一致：只 warn + 明列條目；工具契約禁止初始檔以根 .gitignore/.dockerignore/.editorconfig 為目標（lint）；required/optional 待使用者。
- Q6 定案（使用者：對齊不變量）：init.toml `mode = "append"` 的初始檔——無檔則建；已有則**問**後 append（-y 免問，印出加了什麼）；upgrade 用原文完全比對找上次加的行（記在 baseline），找到→問後替換，找不到→不動只印新內容；remove/uninstall 問後只刪原文相同的行。不用標記區塊；required/optional 不需要。
- Q7 定案：(c) 引擎 image 公開；工具 image 由各工具 repo 自決；認證是主機／CI／Renovate 各自的事，vendor_kit 契約只承諾「主機 docker 拉得到就能用」；文件提醒公開不可逆、denied 分不出不存在／無權限。
- Q8 定案：just ≥ 1.33.0（來源：[group] 放 mod 上 #2263；ADR-0002 理由要改）；一律 GitHub release 下載版；bootstrap.sh 低於即印下載＋安裝指令；CI 矩陣 1.33.0 + latest（不跑中間版）；禁用比 1.33 新的功能由 lint 擋；定案前用 1.33.0 跑完整 fixture。
- Q9 定案：引擎升級後 sync 一次重寫完薄殼＋gen、退出 1、統一印「vendor_kit 已更新 vX → vY，請再跑一次剛才的指令」；不自動續跑（just 一開始即載入定義，續跑會用舊定義）。契約：「同一次 just 呼叫內不會看到新 recipe」。
- Q8 補充：lint 現在擋比 1.33 新的功能；just 有重大功能時允許提高下限（agy 查 1.33 後變更中）。
- Q8 補充（just 1.33→1.58 調查，scratchpad/agy/ 子代理以 gh api + 實測完成，agy 逾時無輸出）：無值得提高下限的功能；候選 1.51 `[working-directory: justfile_directory()]`、1.55 `set minimum-version`。ADR 記破壞性變更：1.53 which() 需 set lists；1.40 --list-submodules 必配 --list；1.42.0–1.42.2 submodule cwd 回歸（提高下限時跳過）；1.52 缺席 mod? 相依 recipe 改 disabled；settings 永遠 per-module（entry.just/tools.just 零 set 規則永久）。
- bootstrap.sh 交付定案：README 連 `releases/latest/download/bootstrap.sh`（GitHub 內建，不需 latest tag，實測 302）；每版 `releases/download/vN/bootstrap.sh`；腳本內嵌所屬引擎 ref；檔名固定。
- 待確認：bootstrap.sh `--image <本機 image>` / `--image-tar <tar>`（version.toml 寫正式 ref、version.local.toml 寫本機覆寫；release 附各平台 docker save tar）。
- 2026-09-19 codex 審三小題（agy/codex_small3.md）：
  - 私有 image 查最新：預設「未提供 registry 憑證時不支援需認證的版本列舉」，update 對該工具回 1 印「可設 VENDOR_KIT_REGISTRY_TOKEN（PAT classic read:packages）或用 upgrade <repo> -t <tag>」；多工具照查其他再彙總；不掛 ~/.docker/config.json。
  - init.toml 欄位：`strategy = "copy" | "append"`（預設 copy；mode 在 Ansible 是權限）；規格明寫 append 首次加入並記錄、重跑不重複、upgrade 只對可辨識的上次插入內容提修改；copy 已存在就跳過，-y 也不覆蓋。
  - append 行比對：CRLF/LF 等價、其餘精確；記錄實際插入片段（原先就存在的相同行不認領）；零命中或多處 → 保留並 warn。
- Q10 待使用者：傾向 (2) 只報 1 提示 `upgrade vendor_kit`（升級者多一個指令；pull 的人 hash 相符無事）。
- **Q10 定案 (2)**：sync 發現薄殼與引擎不符只回 1 提示 `just vendor_kit upgrade vendor_kit`；重產薄殼只由明確動作（upgrade vendor_kit／install）做，做之前比對現內容 == 上次產物（hash 在 gen/.stamp），被改過 → 1 列差異不動。sync 只寫 cache/、gen/（不變量回到「自動化只碰不進 git 的東西」，不需精確化為「不碰使用者的檔」）。
- **Q11 定案 (b)**：未提供 registry 憑證時不支援需認證的版本列舉；update 對該工具回 1 印「可設 VENDOR_KIT_REGISTRY_TOKEN（+ _USER；或 _TOKEN_FILE）或用 upgrade <repo> -t <tag>」；只在 update/upgrade 的 resolve 階段以 -e 傳入引擎；不寫 log/檔、不傳給工具。「查最新」= registry tags/list 取 SemVer 最大正式版。引擎實作 Docker Registry 標準協定（WWW-Authenticate 換 token → /v2/<name>/tags/list 分頁）；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」。PAT 種類／權限細節實作時手動測再定。README 要有「私有 image」一節；測試：unit（token 交換、分頁、SemVer）、integration（無 token→1 逐字訊息、錯 token→1、對 token→列出、TOKEN_FILE）、洩漏 grep、驗收 fixture 私有工具案例。
- **Q12 定案**：init.toml 欄位 `strategy = "copy" | "append"`（預設 copy）；規格明寫 append 首次確認後加入並記錄、重跑不重複、upgrade 只對可辨識的上次插入內容提修改；copy 已存在跳過、-y 不覆蓋。
- **Q13 定案 (2)**：append 行比對 CRLF/LF 等價、其餘精確；metadata 記實際插入的行（原本就存在的相同行不認領）；零命中或多處 → 保留只 warn，-y 不硬加。行尾政策（repo 預設 LF、.gitattributes、dist lint）開 issue #29；使用者確認預設 LF。
