OpenAI Codex v0.153.4
--------
workdir: <scratchpad>/decisions
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 01a0b585-f717-7bc3-8ddb-99efd73b543d
--------
user
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

warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
codex
我會把前例的證據強度與方案可行性分開判斷，特別檢查舊薄殼的救援路徑、永久支援下限，以及驗收矩陣的成本。附件未提供足夠證據的說法，我會明列為未證實。


codex
## agy 說法錯誤

以下依附件與所附原文抽查紀錄判斷，未另行查閱網路。「未證實」不代表必然錯誤，但不能拿來支撐永久相容承諾。

1. **claim：Cargo RFC 3301 定義 lockfile v4。**  
   **why：**附件已確認該引用不存在；可用的證據是 Cargo PR #12852、changelog 與解析／編碼實作。應刪除虛構 RFC 引用。

2. **claim：Cargo 1.78 起，依賴異動就會把舊 lockfile 升成 v4。**  
   **why：**混淆「能讀 v4」「預設產生 v4」與「既有檔是否升格式」。附件指出 1.78 穩定支援、1.83 才預設 v4，實作還考量 MSRV。可借鑑的是保守寫回策略，不能推論所有依賴變動都升格式。

3. **claim：Cargo 永久支援所有舊格式，舊版對新格式完全沒有前向相容。**  
   **why：**目前實作支援 V1–V4，不等於官方永久承諾；不同 Cargo 發行版也可能共用格式。相容性應按「讀者支援的格式集合」判斷，不能直接按引擎新舊二分。

4. **claim：npm 舊讀新會降級解析或覆蓋，支援窗口是 1–2 個 major。**  
   **why：**歷史上的 npm 6／lockfile v2 過渡行為，不代表現行未知格式處理。附件抽查的 Arborist 對超出 `maxLockfileVersion` 的版本有硬拒絕；也沒有足夠證據支持固定 1–2 major 的窗口。必須標明 client 版本與 lockfile 版本。

5. **claim：Yarn、pnpm、Poetry 遇到較新的格式都直接拒絕。**  
   **why：**Yarn 附件只證明格式欄位與 refresh 邏輯；pnpm 引用不足以證明所有模式都硬拒。Poetry 抽查明確有可讀範圍與 warning／raise 分支，且欄位位置應為 `[metadata]`，不是 `[package.metadata]`。

6. **claim：Renovate 舊版必然因未知欄位退出，舊設定至少維持 1–2 major。**  
   **why：**設定驗證、strict 模式與一般執行的行為不能混用；附件也沒有固定支援期的依據。能保留的前例是「執行時遷移」與「選擇性提出設定遷移 PR」。

7. **claim：pre-commit 永久、無條件向後相容。**  
   **why：**最低版本檢查只證明「可宣告讀者需求」，不能證明舊設定永久可用，更不能代表任意新 schema 的辨識機制。

8. **claim：just 1.x 完全向後相容，可以直接採用 `set minimum-version`。**  
   **why：**決策紀錄已列 just 行為變更與回歸；該 setting 要到 1.55 才有，放入要求支援 1.33 的薄殼會先解析失敗。只能借鑑版本自檢概念，不能照搬語法。

9. **claim：Gradle Wrapper 從架構上消除了相容問題。**  
   **why：**固定引擎版本只減少版本選擇差異；舊 wrapper 仍須成功啟動新 distribution。附件引用也不足以支持「一次 wrapper 指令必然更新所有 wrapper 檔案」及「只保證相鄰 major」等一概而論的描述。

10. **claim：Compose v1 遇到 3.9 或沒有 version 就必然拒絕。**  
    **why：**不同 v1 發行版的行為不能合併描述；附件抽查不足以支持這個全面結論。Compose V2 忽略 obsolete `version`，也不代表它可安全忽略所有未知語義。

11. **claim：Git 不放全域版號，只靠每檔版號與忽略未知資料。**  
    **why：**Git 本身就有 repository format version；format 1 的未知 extension 可導致拒絕。真正可借鑑的是：**可忽略的擴充與理解後才能操作的擴充必須分開。**「所有操作都拒絕」則超出附件證據。

12. **claim：Kubernetes GA API 廢棄後保留 12 個月或 3 releases。**  
    **why：**附件已指出引錯；GA 的同 major 不移除規則不能替換成這個數字。另 `no matches for kind` 不能不分層次地描述為 API Server 的固定錯誤回應。

13. **claim：SemVer FAQ 明列 CLI、wire protocol、檔案格式與 schema。**  
    **why：**附件已确认沒有這段明列。正確論證是：**vendor_kit 自行把這些介面列入 public API，再對其套用 SemVer。**SemVer 也不替專案制定永久 floor。

14. **claim：Terraform 1.x 相容承諾涵蓋所有舊 state，讀舊就自動寫回。**  
    **why：**格式可讀、何時持久化、特定歷史升級路徑是不同問題；附件指出 binary v0 仍被拒絕。不能把某些 state 遷移實作擴張為全歷史格式的永久保證。

15. **claim：uv 較高 revision 可忽略，所以未知欄位都可安全忽略；Copier migration 保證任意跨版。**  
    **why：**前者需要新增資料具有可忽略語義，不能由「解析成功」推得安全；後者取決於模板作者提供的遷移與其可組合性。兩者都不能直接證明 vendor_kit 的跨版承諾。

16. **claim：固定 image tag 能保證同一 commit 執行同一 image；加入 `min_engine_version` 就能讓所有舊引擎安全拒絕。**  
    **why：**tag 是否不可變、local override 與本機 tag 都會影響結果；精確內容識別需 digest。最低版本欄位也只有在舊引擎原本就會檢查時才有效，不能追溯修復已出貨的讀者。

17. **claim：vendor_kit 升級應自動 commit；stamp 只需檢查引擎版號。**  
    **why：**前者違反 Q5「不 commit、不開 PR」。後者不足以驗證輸入、薄殼與生成結果，也忽略已定案的薄殼 hash；版號相同不是內容正確的證明。

**brief 本身另有以下問題：**

18. **claim：引擎與它寫的檔在同一 commit 內永遠一致，不一致只發生在三個介面。**  
    **why：**Renovate 只改第一行，本身就能形成「新引擎宣告＋舊 metadata／薄殼」。`gen`、cache 不受 commit 固定，local override、切分支及中途失敗也會形成混合狀態。「三個介面」可作分類，不能作窮盡性事實。

19. **claim：沒 pull 的人使用舊引擎讀新檔，實際上不會發生。**  
    **why：**正常隔離 checkout 下通常不會；但未追蹤的 `gen/cache` 可跨 checkout 留存，`dev -i` 更是明確入口。應描述成立條件，不能全面排除。

20. **claim：floor＝上一個 major 最後一版，且永久不滑動。**  
    **why：**若每次 major 都重新計算「上一個 major」，就是滑動窗口。若指某次定案時的固定 release，必須寫出不可變的具體版本與產物識別。

21. **claim：`gen/.stamp` 足以判定薄殼是否被使用者修改。**  
    **why：**fresh clone 沒有該檔，跨版執行還可能覆寫它；它不能單獨作為歷史原產物的權威證據。這是 Q10 機制目前最重要的缺口之一。

22. **claim：驗收不可新對新，所以新引擎＋乾淨 fixture 結構上不可能失敗。**  
    **why：**這類測試仍能抓新安裝及一般功能錯誤，只是無法證明歷史相容性。另 bootstrap 的已定交付位置是 GitHub Releases，不能籠統寫成全部從 GHCR 取得。

## 方案評估

「是」表示可在硬性限制內採用，仍須補足列出的契約；明確相衝突的原案標為「否」。

| 方案 | 是否符合硬性限制 | pros | cons | 草稿漏掉的風險 |
|---|---|---|---|---|
| **A1** | **是** | 減少薄殼邏輯；引擎可集中維護舊入口 | 薄殼再薄仍有不可遠端更新的解析與啟動邏輯 | public recipe 名、just 解析、argv 分詞、Docker 啟動參數、退出碼、stdout 格式都可能破壞；註解版號本身沒有協商能力 |
| **A2** | **是，但只能採概念** | 不相容時可在寫入前停止，給出明確診斷 | 額外啟動成本；探測入口本身也需要相容承諾 | 不能使用 just 1.55 setting；舊引擎可能沒有探測命令；不相容就要求執行同樣被阻擋的 upgrade，會形成死路 |
| **A3** | **否** | 幾乎沒有相容維護成本 | 把風險全部轉嫁給使用者 | upgrade 依賴舊入口，無法保證救援；違反永久 floor |
| **B1** | **是** | 檔案可自我描述；能分離格式與引擎版本 | 每種檔案都要定義解析及遷移規則 | 「uv 式」不代表一定要 revision；尚未涵蓋非 TOML stamp、無 schema 舊檔、第一行 byte-level 規則 |
| **B2** | **是** | 各檔可獨立演進，減少不必要同步升版 | 多檔一致性與格式組合更複雜 | 若 B1 也是每檔 schema，兩者其實可合併；不可把必要的新語義一律視為可忽略 |
| **B3** | **否** | 欄位少 | 無法可靠辨識混合世代及 local override 產物 | 除非另加等效、可機器辨識的格式識別，否則不能保證未知格式安全拒絕；第一行是目標引擎，不是各檔 writer 身分 |
| **C1** | **是** | 日常操作不改 tracked 檔；沿用既有動詞 | 必須長期維護舊格式解碼與遷移 | sync 是「tracked 資料只讀」，仍可寫 cache/gen；遷移可能缺少舊版未記錄的所有權資訊；多檔寫回可能部分完成 |
| **C2** | **否，作為必要的新公開動詞** | 遷移時機非常明確 | 增加指令與操作步驟 | 仍靠舊薄殼提供入口；可改為 upgrade 的內部階段，沒有必要另開 migrate |
| **C3** | **否** | 維護與測試量可控 | 長期未升級專案被排除 | N−1 是滑動窗口，直接違反固定 floor；不能用「請逐版升」掩蓋已承諾的直接跨版能力 |
| **D1** | **是** | 未知破壞性格式可明確拒絕；阻止錯誤寫回 | 降版不一定能成功 | 舊引擎如何知道未來的 X？未知欄位忽略後寫回可能遺失資料；schema 與最低 reader 不宜只用一個全域數字 |
| **D2** | **否，作為未知 schema 的通則** | 操作阻力小 | 警告後繼續可能產生錯誤結果 | warning 並不等於安全；僅適用已證明可忽略的擴充，此情況可併入 D1 |
| **E1** | **否，按原文** | SemVer 與棄用政策容易溝通 | 「上一 major」floor 自相矛盾；major 破壞範圍不清楚 | major 不能自動取消永久救援義務；格式升版不必然要求手動操作；只承諾同 major 與 v3→v7 目標不一致 |
| **E2** | **是** | 固定常數可直接驗收，不會自動滑動 | 不用 major 後，發行版號較難表達破壞程度 | 單一數字不足以描述薄殼、bootstrap、格式及救援支援集合；可以和修訂後的 E1 並用 |
| **F** | **是，但須定義範圍** | 真實歷史產物能暴露舊 driver 問題；連升可抓救援入口被移除 | 永久 floor 會讓測試量持續成長 | 全版本×全版本×全環境可能平方成長；降版成功不能一概要求；產物比較需排除合法差異；舊 bootstrap 預設只會叫舊引擎 |

A1 的關鍵是：**薄殼只轉發，能減少破壞點，不能消除破壞點。**

| 介面 | 具體破壞例子 | 必須承諾的內容 |
|---|---|---|
| just recipe | 刪除 `upgrade` 入口；gen 缺席導致整份 justfile 無法載入 | 歷史公開入口或相容別名可用；救援入口不依賴 gen |
| argv | 引數重新分詞；選項改位置；`--` 語義改變 | 原始引數邊界、順序與既有參數含義 |
| exit code | 成功升級需重跑的 `1` 被當成普通失敗而回滾；merge `2` 被吞成 `0` | `0/1/2` 的既有語義與錯誤傳遞 |
| resolve stdout | 加入提示文字；欄位換序；新 header 被舊 parser 當資料 | `vk-resolve/1` 的完整文法、錯誤處理及 stderr 分流 |
| 啟動環境 | 新增主機 Python、jq、Compose 或新版 Docker 選項 | 只使用既定主機依賴及其最低版本能力 |

## 建議

**選擇：A1＋修訂 A2；B1＋B2；C1；D1；修訂 E1＋E2；F 全部類型納入，但不做不必要的全版本兩兩乘積。**

其中最重要的修訂是：

- A2 增加**穩定探測入口與獨立救援路徑**，不能只「拒絕並要求 upgrade」。
- B1/B2 定義為**每種檔案獨立 schema**，不建立所有檔案必須同步升版的全域 schema。
- E2 用固定 release `R0` 定義永久 floor；E1 保留 SemVer，但 major 不能撤銷既有 floor 的救援及資料遷移義務。
- F 區分「必須成功」與「必須安全拒絕」。未知格式的降版拒絕本身是合格結果。

### 相容性契約條文草稿（12 條）

1. **主機與公開介面。**vendor_kit 僅要求既定平台上的 Docker ≥19.03、Git、just ≥1.33.0 及既定平台基本執行環境；不得新增額外主機工具需求。公開 recipe、CLI argv、退出碼、薄殼啟動協定、resolve stdout 與持久化檔案格式均列入相容性契約。

2. **永久支援集合。**首個承諾版本記為固定 release `R0`，並記錄其不可變產物識別；`R0` 起的正式發行薄殼、bootstrap 與正式產出格式持續納入支援集合，不因新 major 發布而移除。新引擎須提供從這些版本直接升級的路徑，不得要求使用者手動逐版執行。

3. **一般執行與救援分層。**同 major 內保留所有已承諾薄殼的一般呼叫能力；跨 major 至少保留歷史入口所需的探測、解析目標與 `upgrade vendor_kit` 救援能力，以及舊資料讀取／遷移能力。一般命令可因需重產薄殼而回 `1`，但不得因此封鎖救援路徑。

4. **協定與退出碼。**薄殼標記協定世代，候選引擎宣告可接受的協定集合；探測必須不依赖 gen 或當前業務 schema。保留 `vk-resolve/1` 的完整機器可讀文法，診斷只寫 stderr；未知協定、輸出不完整或解析失敗不得繼續操作。保留既有 `0` 成功、`1` 錯誤或需使用者處理／重跑、`2` 合併衝突語義；自身升級完成須停下並回 `1` 提示重跑。

5. **各檔格式。**`version.toml` 第一個實體行固定為 `vendor_kit = "<ref>"`，第二行為 `schema = N`；禁止 BOM、前置空白行、重複鍵及同名旁路解析。其他持久化 TOML 各自具有 schema；stamp 另定格式識別，不改變其引擎 ref＋薄殼 hash 的既定用途。只有明列的歷史格式可將缺少 schema 視為 legacy 格式。

6. **新讀舊與遷移。**新引擎須讀取支援集合內的舊格式，必要時在記憶體轉換；只有原本授權寫入該檔的明確動作才能持久化。既有 metadata 的格式遷移由 `upgrade vendor_kit` 執行；缺失且無法可靠還原的所有權或來源資訊不得猜測，須停止受影響操作並提供處理方式。

7. **未知格式與擴充。**讀者不支援的 schema 必須在修改專案持久化資料前非零退出，說明檔案、現有格式與支援範圍。同 schema 的未知欄位僅可在其語義確實可忽略時略過；寫回須保留未知資料，不能保留則拒絕。需要讀者理解的新語義必須升 schema，或使用事先定義、未知即拒絕的必要能力欄位。

8. **最低讀者提示。**若要保證輸出「需要引擎 ≥X」，須從 `R0` 起提供舊讀者可辨識的固定需求封套，例如每檔 `min_reader`，並驗證其與 schema 一致；它是必要条件，不取代 schema 支援檢查。對沒有這項資訊的歷史檔，只能誠實輸出未知格式及可用救援指令，不得猜測 X。

9. **sync 與重產。**sync 只寫 cache/gen；薄殼不符時回 `1` 提示 `upgrade vendor_kit`。薄殼僅由 install／`upgrade vendor_kit` 重產，且須證明現內容等於原產物。`gen/.stamp` 只能作快取證據；缺失時須取得可信的歷史原產物或等效持久證據，無法證明時不得覆寫。

10. **使用者檔與失敗恢復。**使用者檔可建立並列明；修改須先取得同意，`-y` 只省略詢問，不授權覆蓋既有未納管檔；不刪檔、不盲目覆蓋。遷移與升降版須先完成可行性檢查，失敗不得留下無法辨識的混合狀態，重跑須可安全恢復；明定的合併衝突狀態另依回 `2` 契約處理。

11. **SemVer 與降版。**對已宣告介面的不相容變更使用 major；minor 增加相容功能，patch 修正相容缺陷。可移除介面須至少先於一個 minor 發布棄用通知，但不得移除第 2、3 條的永久義務。降版只有在目標可讀或可無損轉換時成功；否則在修改 ref、metadata、薄殼及使用者檔前拒絕。

12. **發行驗收。**候選版本必須由支援集合內真正已釋出的薄殼與 bootstrap 驅動驗收，涵蓋直接跨版、連續升級、降版、local override、無 gen 的 fresh clone、使用者修改及中斷恢复。新安裝測試另保留；任何必要歷史案例未通過或未執行，不得宣告相容驗收完成。

### 驗收矩陣表

符號：

- `Rᵢ`：支援集合中的歷史正式版本。
- `C`：候選版本。
- `Rⱼ`：另一個已釋出版本。
- 歷史 fixture 必須由對應歷史引擎產生，連同產物 digest 固定保存；不能用 C 模擬生成「舊格式」。

| 案例 | 驅動者／起始狀態 | 目標與流程 | 合格結果 | 覆蓋 |
|---|---|---|---|---|
| 歷史薄殼完整流程 | 每個 `Rᵢ` 真實薄殼＋其 fixture | ref 指向 C；sync → 明確 upgrade → 重新呼叫 → 完整流程 | sync 不改 tracked 檔；舊入口可救援；重跑後正常 | 每個薄殼發行版本 |
| 舊 bootstrap 固定引擎 | 每個已釋出 bootstrap | 不覆寫其內嵌 ref，首次 install／再跑修復 | 使用其所屬引擎；修復不破壞既有檔 | 每個 bootstrap 版本 |
| 舊 bootstrap 呼叫候選 | 每個歷史 bootstrap 的既有 image override 入口 | 指向 C，首次 install／修復 | 舊參數與呼叫協定可用 | 每個具有該入口的版本 |
| 第一行單獨升版 | 真實舊專案，只修改 engine ref | 執行決策紀錄的 frozen sync、verify、dry-run 等流程 | 不因只改一行就誤判通過；需要升級時回 `1` 並給可執行指令 | 每個介面／格式世代 |
| fresh clone | 歷史 tracked 檔，無 cache/gen/stamp | 直接啟動救援並升至 C | just 可載入；缺 stamp 不導致盲目重產 | 每個薄殼世代 |
| 連續升級 | `Rᵢ` 專案 | `Rᵢ → Rⱼ → C`，各階段重新呼叫 | 第二次升級入口仍存在且有效 | 相鄰發行邊及每個協定／schema 轉換邊 |
| 固定 floor 跳升 | `R0` 原始專案 | 不經使用者逐版操作，直接升 C | 跨所有中間世代成功，或依既定使用者檔規則明確待處理 | 每次發行必跑 |
| 可相容降版 | C 升級後的專案 | `upgrade vendor_kit -t Rᵢ` | 能安全轉換者成功；重跑目標引擎可用 | 每個受測目標格式世代 |
| 不可相容降版 | 含較新必要語義的專案 | 降至不支援的 `Rᵢ` | 修改前拒絕；不先改 ref 留下壞狀態 | 每個格式破壞邊界 |
| 舊引擎讀新檔 | 新專案＋`dev -i` 舊 image | 普通命令與會寫檔命令 | 未知 schema 安全拒絕；已宣告可忽略擴充不遺失 | 每個讀者／格式能力世代 |
| 第一行與解析一致性 | 真實舊啟動器＋合法／異常 TOML | BOM、空白、重複鍵、第二行 schema、local override | 合法格式取到相同 ref；異常格式明確失敗 | 每個啟動器 parser 世代 |
| 使用者保護 | 修改薄殼、既有未納管檔、append 零／多命中 | upgrade／install，含 `-y` 與非互動模式 | 不覆蓋、不刪檔；詢問、警告、退出碼符合契約 | C 完整分支＋歷史資料世代 |
| 中斷與重跑 | 遷移前、中、後的故障注入 | 再次執行既有指令 | 保持原狀或可辨識恢復；不把半完成視為成功 | 每個寫入階段 |
| 升級／全新一致 | 歷史專案升 C；另以 C 全新 install | 相同工具、ref 與選項 | 自有確定性產物一致；受保護的使用者差異明列 | 每個歷史產物世代 |
| 主機下限 | 上述歷史驅動案例 | Docker 19.03、just 1.33.0；另跑目前支援端點及架構 | 不依赖新版主機功能；兩平台 image 可執行且內容符合契約 | 明定的環境組合 |

**矩陣成本與執行方式：**

- `S` 個歷史版本各自跑向 C，是 `S` 條邊；不是 `S²`。
- 連升採「歷史相鄰邊／格式轉換邊＋C」，仍可維持線性成長；沒有必要測所有 `Rᵢ→Rⱼ→C`。
- 跨版直接路徑不能只測 `R0→C` 代替所有歷史版本：中間版可能有特殊 bug 或不同產物。
- Linux 若完整交叉兩個 Docker 端點、兩個 just 端點、兩個架構，為 `8S` 個歷史版本／環境組合；WSL2 另列實际承諾組合。
- 建議每個歷史版本在最低環境跑完整流程；其他環境對協定、格式與產物世代做覆蓋。發行文件必須公開這個覆蓋規則，不能稱為「所有版本×所有環境完整流程」。
- 若不同 releases 的相關歷史產物與呼叫協定完全相同，可依 digest 證明後共用執行結果，但保留每個 release 的對應關係。
- 時間戳、絕對路徑、允許的 legacy 編碼等可正規化；薄殼內容、語義必要欄位、ref、所有權紀錄不能為了通過而忽略。

## 理由

**第一，真正需要永久保留的是可達的升級路徑。**  
A1 把邏輯移到引擎，是有幫助的架構選擇；但舊 recipe、Docker 呼叫方式與 stdout parser 已經出貨，不能靠新版文件修正。A2 若只加入拒絕檢查，反而可能把唯一的 upgrade 入口鎖住。應先證明 `R0` 的實際 argv 能抵達 C 的救援處理，再設計一般命令的阻擋。

**第二，格式可讀、寫回安全、行為相容必須分別承諾。**  
Cargo／Git 的前例支持保守持久化；uv 支持區分破壞格式與相容擴充；附件中的 npm 拒絕邏輯提醒我們不能丟棄未知資料。這些前例共同支持 C1＋D1，但不支持「同 schema 解析成功就可以重新序列化」。

尤其 metadata 若記錄「哪些 append 行是工具實際加入的」，舊格式沒保存這件事，新引擎不能從目前檔案反推所有權。這種遷移不是補一個 schema 欄位就完成；無證據時只能保留內容並明確報告。

**第三，version.toml 第一行可以和 schema 共存，但這是一個雙層契約。**  
舊啟動器先用既有文字規則選引擎，新引擎再解析完整 TOML。因此 schema 不能要求啟動器先理解新格式，也不能准許 TOML 合法但舊 parser 取到不同 ref 的表示法。真正要驗的是每一代已釋出的 parser，不是新寫的範例 grep。

**第四，永久 floor 比 SemVer 更強。**  
SemVer 告訴使用者哪個版本可能改變介面，不能授權撤销已承諾的永久支援。可以在 major 停止舊薄殼的一般工作流程，但必須留下能將它帶到新狀態的救援能力。若不願長期維護這個相容層，就不能同時承諾固定 floor 與直接跨版。

**第五，驗收必須保留歷史輸入，但不必把所有維度盲目相乘。**  
歷史 driver、歷史資料與真實入口是不可省略的部分；全版本兩兩組合則未必增加對承諾的有效覆蓋。從已釋出版本各自指向候選、補上連升與破壞邊界，才能把成本控制在線性成長，同時保留 #1048 要求的歷史證據。

另有一個必須先修正的設計缺口：**放在 gen 的 hash 不能單獨承擔「這份 tracked 薄殼從未被改過」的判定。**若這點未解，fresh clone 的第一次 upgrade 就可能在安全性與可用性之間無解。

## 定案前要問的問題

1. **固定 floor 究竟是哪個實際 release？**  
   要記錄其薄殼、bootstrap、引擎及 fixture digest；若尚無正式版，應從第一個具備完整相容封套的版本開始承諾。

2. **跨 major 承諾到哪一層？**  
   建議明定：舊薄殼至少可救援升級，舊資料可直接遷移；是否還要求所有舊薄殼直接執行新 major 的一般命令，需要另外決定。

3. **fresh clone 缺少 `gen/.stamp` 時，用什麼證據辨識原始薄殼？**  
   候選是可重建的歷史 release 產物，或受追蹤的來源／產物紀錄；不能把「stamp 不存在」視為可覆寫。

4. **歷史 bootstrap 真正支援哪個 override 介面？**  
   brief 的 `--local` 與紀錄待定的 `--image`／`--image-tar` 不一致；必須以實際交付介面決定驗收及救援方式。

5. **是否要求未知 schema 一定印出精確的最低引擎 X？**  
   若是，從 floor 起就須固定 `min_reader` 或等效封套；否則只能保證明確拒絕，不能保證知道未來版本號。

6. **降版的承諾是安全拒絕，還是保證轉換成功？**  
   建議只保證可無損轉換者成功，其餘修改前拒絕；不可承諾任意 major 降版。

7. **哪些檔案屬於自有、哪些即使在 `.vendor_kit/` 內也屬於使用者可編輯內容？**  
   需要逐檔列明，尤其 version 宣告、metadata、baseline 與被修改的薄殼；目錄位置本身不能代表覆寫授權。

8. **「永不覆蓋」是否沿用既有決策的意義：不盲目覆蓋，但允許同意後替換／合併？**  
   這也要和「不刪檔，但可經同意移除工具曾插入的精確行」分開寫，避免不變量與既有 upgrade／uninstall 規則互相矛盾。

9. **發行驗收要承諾哪些環境交叉組合與執行成本？**  
   包含 Docker 上界、Git 下限或測試基準、WSL2 架構，以及是否接受「每個歷史版本在下限完整跑、其他環境按世代覆蓋」。這是 F 能否永久履行的實際預算。
tokens used
27,738
## agy 說法錯誤

以下依附件與所附原文抽查紀錄判斷，未另行查閱網路。「未證實」不代表必然錯誤，但不能拿來支撐永久相容承諾。

1. **claim：Cargo RFC 3301 定義 lockfile v4。**  
   **why：**附件已確認該引用不存在；可用的證據是 Cargo PR #12852、changelog 與解析／編碼實作。應刪除虛構 RFC 引用。

2. **claim：Cargo 1.78 起，依賴異動就會把舊 lockfile 升成 v4。**  
   **why：**混淆「能讀 v4」「預設產生 v4」與「既有檔是否升格式」。附件指出 1.78 穩定支援、1.83 才預設 v4，實作還考量 MSRV。可借鑑的是保守寫回策略，不能推論所有依賴變動都升格式。

3. **claim：Cargo 永久支援所有舊格式，舊版對新格式完全沒有前向相容。**  
   **why：**目前實作支援 V1–V4，不等於官方永久承諾；不同 Cargo 發行版也可能共用格式。相容性應按「讀者支援的格式集合」判斷，不能直接按引擎新舊二分。

4. **claim：npm 舊讀新會降級解析或覆蓋，支援窗口是 1–2 個 major。**  
   **why：**歷史上的 npm 6／lockfile v2 過渡行為，不代表現行未知格式處理。附件抽查的 Arborist 對超出 `maxLockfileVersion` 的版本有硬拒絕；也沒有足夠證據支持固定 1–2 major 的窗口。必須標明 client 版本與 lockfile 版本。

5. **claim：Yarn、pnpm、Poetry 遇到較新的格式都直接拒絕。**  
   **why：**Yarn 附件只證明格式欄位與 refresh 邏輯；pnpm 引用不足以證明所有模式都硬拒。Poetry 抽查明確有可讀範圍與 warning／raise 分支，且欄位位置應為 `[metadata]`，不是 `[package.metadata]`。

6. **claim：Renovate 舊版必然因未知欄位退出，舊設定至少維持 1–2 major。**  
   **why：**設定驗證、strict 模式與一般執行的行為不能混用；附件也沒有固定支援期的依據。能保留的前例是「執行時遷移」與「選擇性提出設定遷移 PR」。

7. **claim：pre-commit 永久、無條件向後相容。**  
   **why：**最低版本檢查只證明「可宣告讀者需求」，不能證明舊設定永久可用，更不能代表任意新 schema 的辨識機制。

8. **claim：just 1.x 完全向後相容，可以直接採用 `set minimum-version`。**  
   **why：**決策紀錄已列 just 行為變更與回歸；該 setting 要到 1.55 才有，放入要求支援 1.33 的薄殼會先解析失敗。只能借鑑版本自檢概念，不能照搬語法。

9. **claim：Gradle Wrapper 從架構上消除了相容問題。**  
   **why：**固定引擎版本只減少版本選擇差異；舊 wrapper 仍須成功啟動新 distribution。附件引用也不足以支持「一次 wrapper 指令必然更新所有 wrapper 檔案」及「只保證相鄰 major」等一概而論的描述。

10. **claim：Compose v1 遇到 3.9 或沒有 version 就必然拒絕。**  
    **why：**不同 v1 發行版的行為不能合併描述；附件抽查不足以支持這個全面結論。Compose V2 忽略 obsolete `version`，也不代表它可安全忽略所有未知語義。

11. **claim：Git 不放全域版號，只靠每檔版號與忽略未知資料。**  
    **why：**Git 本身就有 repository format version；format 1 的未知 extension 可導致拒絕。真正可借鑑的是：**可忽略的擴充與理解後才能操作的擴充必須分開。**「所有操作都拒絕」則超出附件證據。

12. **claim：Kubernetes GA API 廢棄後保留 12 個月或 3 releases。**  
    **why：**附件已指出引錯；GA 的同 major 不移除規則不能替換成這個數字。另 `no matches for kind` 不能不分層次地描述為 API Server 的固定錯誤回應。

13. **claim：SemVer FAQ 明列 CLI、wire protocol、檔案格式與 schema。**  
    **why：**附件已确认沒有這段明列。正確論證是：**vendor_kit 自行把這些介面列入 public API，再對其套用 SemVer。**SemVer 也不替專案制定永久 floor。

14. **claim：Terraform 1.x 相容承諾涵蓋所有舊 state，讀舊就自動寫回。**  
    **why：**格式可讀、何時持久化、特定歷史升級路徑是不同問題；附件指出 binary v0 仍被拒絕。不能把某些 state 遷移實作擴張為全歷史格式的永久保證。

15. **claim：uv 較高 revision 可忽略，所以未知欄位都可安全忽略；Copier migration 保證任意跨版。**  
    **why：**前者需要新增資料具有可忽略語義，不能由「解析成功」推得安全；後者取決於模板作者提供的遷移與其可組合性。兩者都不能直接證明 vendor_kit 的跨版承諾。

16. **claim：固定 image tag 能保證同一 commit 執行同一 image；加入 `min_engine_version` 就能讓所有舊引擎安全拒絕。**  
    **why：**tag 是否不可變、local override 與本機 tag 都會影響結果；精確內容識別需 digest。最低版本欄位也只有在舊引擎原本就會檢查時才有效，不能追溯修復已出貨的讀者。

17. **claim：vendor_kit 升級應自動 commit；stamp 只需檢查引擎版號。**  
    **why：**前者違反 Q5「不 commit、不開 PR」。後者不足以驗證輸入、薄殼與生成結果，也忽略已定案的薄殼 hash；版號相同不是內容正確的證明。

**brief 本身另有以下問題：**

18. **claim：引擎與它寫的檔在同一 commit 內永遠一致，不一致只發生在三個介面。**  
    **why：**Renovate 只改第一行，本身就能形成「新引擎宣告＋舊 metadata／薄殼」。`gen`、cache 不受 commit 固定，local override、切分支及中途失敗也會形成混合狀態。「三個介面」可作分類，不能作窮盡性事實。

19. **claim：沒 pull 的人使用舊引擎讀新檔，實際上不會發生。**  
    **why：**正常隔離 checkout 下通常不會；但未追蹤的 `gen/cache` 可跨 checkout 留存，`dev -i` 更是明確入口。應描述成立條件，不能全面排除。

20. **claim：floor＝上一個 major 最後一版，且永久不滑動。**  
    **why：**若每次 major 都重新計算「上一個 major」，就是滑動窗口。若指某次定案時的固定 release，必須寫出不可變的具體版本與產物識別。

21. **claim：`gen/.stamp` 足以判定薄殼是否被使用者修改。**  
    **why：**fresh clone 沒有該檔，跨版執行還可能覆寫它；它不能單獨作為歷史原產物的權威證據。這是 Q10 機制目前最重要的缺口之一。

22. **claim：驗收不可新對新，所以新引擎＋乾淨 fixture 結構上不可能失敗。**  
    **why：**這類測試仍能抓新安裝及一般功能錯誤，只是無法證明歷史相容性。另 bootstrap 的已定交付位置是 GitHub Releases，不能籠統寫成全部從 GHCR 取得。

## 方案評估

「是」表示可在硬性限制內採用，仍須補足列出的契約；明確相衝突的原案標為「否」。

| 方案 | 是否符合硬性限制 | pros | cons | 草稿漏掉的風險 |
|---|---|---|---|---|
| **A1** | **是** | 減少薄殼邏輯；引擎可集中維護舊入口 | 薄殼再薄仍有不可遠端更新的解析與啟動邏輯 | public recipe 名、just 解析、argv 分詞、Docker 啟動參數、退出碼、stdout 格式都可能破壞；註解版號本身沒有協商能力 |
| **A2** | **是，但只能採概念** | 不相容時可在寫入前停止，給出明確診斷 | 額外啟動成本；探測入口本身也需要相容承諾 | 不能使用 just 1.55 setting；舊引擎可能沒有探測命令；不相容就要求執行同樣被阻擋的 upgrade，會形成死路 |
| **A3** | **否** | 幾乎沒有相容維護成本 | 把風險全部轉嫁給使用者 | upgrade 依賴舊入口，無法保證救援；違反永久 floor |
| **B1** | **是** | 檔案可自我描述；能分離格式與引擎版本 | 每種檔案都要定義解析及遷移規則 | 「uv 式」不代表一定要 revision；尚未涵蓋非 TOML stamp、無 schema 舊檔、第一行 byte-level 規則 |
| **B2** | **是** | 各檔可獨立演進，減少不必要同步升版 | 多檔一致性與格式組合更複雜 | 若 B1 也是每檔 schema，兩者其實可合併；不可把必要的新語義一律視為可忽略 |
| **B3** | **否** | 欄位少 | 無法可靠辨識混合世代及 local override 產物 | 除非另加等效、可機器辨識的格式識別，否則不能保證未知格式安全拒絕；第一行是目標引擎，不是各檔 writer 身分 |
| **C1** | **是** | 日常操作不改 tracked 檔；沿用既有動詞 | 必須長期維護舊格式解碼與遷移 | sync 是「tracked 資料只讀」，仍可寫 cache/gen；遷移可能缺少舊版未記錄的所有權資訊；多檔寫回可能部分完成 |
| **C2** | **否，作為必要的新公開動詞** | 遷移時機非常明確 | 增加指令與操作步驟 | 仍靠舊薄殼提供入口；可改為 upgrade 的內部階段，沒有必要另開 migrate |
| **C3** | **否** | 維護與測試量可控 | 長期未升級專案被排除 | N−1 是滑動窗口，直接違反固定 floor；不能用「請逐版升」掩蓋已承諾的直接跨版能力 |
| **D1** | **是** | 未知破壞性格式可明確拒絕；阻止錯誤寫回 | 降版不一定能成功 | 舊引擎如何知道未來的 X？未知欄位忽略後寫回可能遺失資料；schema 與最低 reader 不宜只用一個全域數字 |
| **D2** | **否，作為未知 schema 的通則** | 操作阻力小 | 警告後繼續可能產生錯誤結果 | warning 並不等於安全；僅適用已證明可忽略的擴充，此情況可併入 D1 |
| **E1** | **否，按原文** | SemVer 與棄用政策容易溝通 | 「上一 major」floor 自相矛盾；major 破壞範圍不清楚 | major 不能自動取消永久救援義務；格式升版不必然要求手動操作；只承諾同 major 與 v3→v7 目標不一致 |
| **E2** | **是** | 固定常數可直接驗收，不會自動滑動 | 不用 major 後，發行版號較難表達破壞程度 | 單一數字不足以描述薄殼、bootstrap、格式及救援支援集合；可以和修訂後的 E1 並用 |
| **F** | **是，但須定義範圍** | 真實歷史產物能暴露舊 driver 問題；連升可抓救援入口被移除 | 永久 floor 會讓測試量持續成長 | 全版本×全版本×全環境可能平方成長；降版成功不能一概要求；產物比較需排除合法差異；舊 bootstrap 預設只會叫舊引擎 |

A1 的關鍵是：**薄殼只轉發，能減少破壞點，不能消除破壞點。**

| 介面 | 具體破壞例子 | 必須承諾的內容 |
|---|---|---|
| just recipe | 刪除 `upgrade` 入口；gen 缺席導致整份 justfile 無法載入 | 歷史公開入口或相容別名可用；救援入口不依賴 gen |
| argv | 引數重新分詞；選項改位置；`--` 語義改變 | 原始引數邊界、順序與既有參數含義 |
| exit code | 成功升級需重跑的 `1` 被當成普通失敗而回滾；merge `2` 被吞成 `0` | `0/1/2` 的既有語義與錯誤傳遞 |
| resolve stdout | 加入提示文字；欄位換序；新 header 被舊 parser 當資料 | `vk-resolve/1` 的完整文法、錯誤處理及 stderr 分流 |
| 啟動環境 | 新增主機 Python、jq、Compose 或新版 Docker 選項 | 只使用既定主機依賴及其最低版本能力 |

## 建議

**選擇：A1＋修訂 A2；B1＋B2；C1；D1；修訂 E1＋E2；F 全部類型納入，但不做不必要的全版本兩兩乘積。**

其中最重要的修訂是：

- A2 增加**穩定探測入口與獨立救援路徑**，不能只「拒絕並要求 upgrade」。
- B1/B2 定義為**每種檔案獨立 schema**，不建立所有檔案必須同步升版的全域 schema。
- E2 用固定 release `R0` 定義永久 floor；E1 保留 SemVer，但 major 不能撤銷既有 floor 的救援及資料遷移義務。
- F 區分「必須成功」與「必須安全拒絕」。未知格式的降版拒絕本身是合格結果。

### 相容性契約條文草稿（12 條）

1. **主機與公開介面。**vendor_kit 僅要求既定平台上的 Docker ≥19.03、Git、just ≥1.33.0 及既定平台基本執行環境；不得新增額外主機工具需求。公開 recipe、CLI argv、退出碼、薄殼啟動協定、resolve stdout 與持久化檔案格式均列入相容性契約。

2. **永久支援集合。**首個承諾版本記為固定 release `R0`，並記錄其不可變產物識別；`R0` 起的正式發行薄殼、bootstrap 與正式產出格式持續納入支援集合，不因新 major 發布而移除。新引擎須提供從這些版本直接升級的路徑，不得要求使用者手動逐版執行。

3. **一般執行與救援分層。**同 major 內保留所有已承諾薄殼的一般呼叫能力；跨 major 至少保留歷史入口所需的探測、解析目標與 `upgrade vendor_kit` 救援能力，以及舊資料讀取／遷移能力。一般命令可因需重產薄殼而回 `1`，但不得因此封鎖救援路徑。

4. **協定與退出碼。**薄殼標記協定世代，候選引擎宣告可接受的協定集合；探測必須不依赖 gen 或當前業務 schema。保留 `vk-resolve/1` 的完整機器可讀文法，診斷只寫 stderr；未知協定、輸出不完整或解析失敗不得繼續操作。保留既有 `0` 成功、`1` 錯誤或需使用者處理／重跑、`2` 合併衝突語義；自身升級完成須停下並回 `1` 提示重跑。

5. **各檔格式。**`version.toml` 第一個實體行固定為 `vendor_kit = "<ref>"`，第二行為 `schema = N`；禁止 BOM、前置空白行、重複鍵及同名旁路解析。其他持久化 TOML 各自具有 schema；stamp 另定格式識別，不改變其引擎 ref＋薄殼 hash 的既定用途。只有明列的歷史格式可將缺少 schema 視為 legacy 格式。

6. **新讀舊與遷移。**新引擎須讀取支援集合內的舊格式，必要時在記憶體轉換；只有原本授權寫入該檔的明確動作才能持久化。既有 metadata 的格式遷移由 `upgrade vendor_kit` 執行；缺失且無法可靠還原的所有權或來源資訊不得猜測，須停止受影響操作並提供處理方式。

7. **未知格式與擴充。**讀者不支援的 schema 必須在修改專案持久化資料前非零退出，說明檔案、現有格式與支援範圍。同 schema 的未知欄位僅可在其語義確實可忽略時略過；寫回須保留未知資料，不能保留則拒絕。需要讀者理解的新語義必須升 schema，或使用事先定義、未知即拒絕的必要能力欄位。

8. **最低讀者提示。**若要保證輸出「需要引擎 ≥X」，須從 `R0` 起提供舊讀者可辨識的固定需求封套，例如每檔 `min_reader`，並驗證其與 schema 一致；它是必要条件，不取代 schema 支援檢查。對沒有這項資訊的歷史檔，只能誠實輸出未知格式及可用救援指令，不得猜測 X。

9. **sync 與重產。**sync 只寫 cache/gen；薄殼不符時回 `1` 提示 `upgrade vendor_kit`。薄殼僅由 install／`upgrade vendor_kit` 重產，且須證明現內容等於原產物。`gen/.stamp` 只能作快取證據；缺失時須取得可信的歷史原產物或等效持久證據，無法證明時不得覆寫。

10. **使用者檔與失敗恢復。**使用者檔可建立並列明；修改須先取得同意，`-y` 只省略詢問，不授權覆蓋既有未納管檔；不刪檔、不盲目覆蓋。遷移與升降版須先完成可行性檢查，失敗不得留下無法辨識的混合狀態，重跑須可安全恢復；明定的合併衝突狀態另依回 `2` 契約處理。

11. **SemVer 與降版。**對已宣告介面的不相容變更使用 major；minor 增加相容功能，patch 修正相容缺陷。可移除介面須至少先於一個 minor 發布棄用通知，但不得移除第 2、3 條的永久義務。降版只有在目標可讀或可無損轉換時成功；否則在修改 ref、metadata、薄殼及使用者檔前拒絕。

12. **發行驗收。**候選版本必須由支援集合內真正已釋出的薄殼與 bootstrap 驅動驗收，涵蓋直接跨版、連續升級、降版、local override、無 gen 的 fresh clone、使用者修改及中斷恢复。新安裝測試另保留；任何必要歷史案例未通過或未執行，不得宣告相容驗收完成。

### 驗收矩陣表

符號：

- `Rᵢ`：支援集合中的歷史正式版本。
- `C`：候選版本。
- `Rⱼ`：另一個已釋出版本。
- 歷史 fixture 必須由對應歷史引擎產生，連同產物 digest 固定保存；不能用 C 模擬生成「舊格式」。

| 案例 | 驅動者／起始狀態 | 目標與流程 | 合格結果 | 覆蓋 |
|---|---|---|---|---|
| 歷史薄殼完整流程 | 每個 `Rᵢ` 真實薄殼＋其 fixture | ref 指向 C；sync → 明確 upgrade → 重新呼叫 → 完整流程 | sync 不改 tracked 檔；舊入口可救援；重跑後正常 | 每個薄殼發行版本 |
| 舊 bootstrap 固定引擎 | 每個已釋出 bootstrap | 不覆寫其內嵌 ref，首次 install／再跑修復 | 使用其所屬引擎；修復不破壞既有檔 | 每個 bootstrap 版本 |
| 舊 bootstrap 呼叫候選 | 每個歷史 bootstrap 的既有 image override 入口 | 指向 C，首次 install／修復 | 舊參數與呼叫協定可用 | 每個具有該入口的版本 |
| 第一行單獨升版 | 真實舊專案，只修改 engine ref | 執行決策紀錄的 frozen sync、verify、dry-run 等流程 | 不因只改一行就誤判通過；需要升級時回 `1` 並給可執行指令 | 每個介面／格式世代 |
| fresh clone | 歷史 tracked 檔，無 cache/gen/stamp | 直接啟動救援並升至 C | just 可載入；缺 stamp 不導致盲目重產 | 每個薄殼世代 |
| 連續升級 | `Rᵢ` 專案 | `Rᵢ → Rⱼ → C`，各階段重新呼叫 | 第二次升級入口仍存在且有效 | 相鄰發行邊及每個協定／schema 轉換邊 |
| 固定 floor 跳升 | `R0` 原始專案 | 不經使用者逐版操作，直接升 C | 跨所有中間世代成功，或依既定使用者檔規則明確待處理 | 每次發行必跑 |
| 可相容降版 | C 升級後的專案 | `upgrade vendor_kit -t Rᵢ` | 能安全轉換者成功；重跑目標引擎可用 | 每個受測目標格式世代 |
| 不可相容降版 | 含較新必要語義的專案 | 降至不支援的 `Rᵢ` | 修改前拒絕；不先改 ref 留下壞狀態 | 每個格式破壞邊界 |
| 舊引擎讀新檔 | 新專案＋`dev -i` 舊 image | 普通命令與會寫檔命令 | 未知 schema 安全拒絕；已宣告可忽略擴充不遺失 | 每個讀者／格式能力世代 |
| 第一行與解析一致性 | 真實舊啟動器＋合法／異常 TOML | BOM、空白、重複鍵、第二行 schema、local override | 合法格式取到相同 ref；異常格式明確失敗 | 每個啟動器 parser 世代 |
| 使用者保護 | 修改薄殼、既有未納管檔、append 零／多命中 | upgrade／install，含 `-y` 與非互動模式 | 不覆蓋、不刪檔；詢問、警告、退出碼符合契約 | C 完整分支＋歷史資料世代 |
| 中斷與重跑 | 遷移前、中、後的故障注入 | 再次執行既有指令 | 保持原狀或可辨識恢復；不把半完成視為成功 | 每個寫入階段 |
| 升級／全新一致 | 歷史專案升 C；另以 C 全新 install | 相同工具、ref 與選項 | 自有確定性產物一致；受保護的使用者差異明列 | 每個歷史產物世代 |
| 主機下限 | 上述歷史驅動案例 | Docker 19.03、just 1.33.0；另跑目前支援端點及架構 | 不依赖新版主機功能；兩平台 image 可執行且內容符合契約 | 明定的環境組合 |

**矩陣成本與執行方式：**

- `S` 個歷史版本各自跑向 C，是 `S` 條邊；不是 `S²`。
- 連升採「歷史相鄰邊／格式轉換邊＋C」，仍可維持線性成長；沒有必要測所有 `Rᵢ→Rⱼ→C`。
- 跨版直接路徑不能只測 `R0→C` 代替所有歷史版本：中間版可能有特殊 bug 或不同產物。
- Linux 若完整交叉兩個 Docker 端點、兩個 just 端點、兩個架構，為 `8S` 個歷史版本／環境組合；WSL2 另列實际承諾組合。
- 建議每個歷史版本在最低環境跑完整流程；其他環境對協定、格式與產物世代做覆蓋。發行文件必須公開這個覆蓋規則，不能稱為「所有版本×所有環境完整流程」。
- 若不同 releases 的相關歷史產物與呼叫協定完全相同，可依 digest 證明後共用執行結果，但保留每個 release 的對應關係。
- 時間戳、絕對路徑、允許的 legacy 編碼等可正規化；薄殼內容、語義必要欄位、ref、所有權紀錄不能為了通過而忽略。

## 理由

**第一，真正需要永久保留的是可達的升級路徑。**  
A1 把邏輯移到引擎，是有幫助的架構選擇；但舊 recipe、Docker 呼叫方式與 stdout parser 已經出貨，不能靠新版文件修正。A2 若只加入拒絕檢查，反而可能把唯一的 upgrade 入口鎖住。應先證明 `R0` 的實際 argv 能抵達 C 的救援處理，再設計一般命令的阻擋。

**第二，格式可讀、寫回安全、行為相容必須分別承諾。**  
Cargo／Git 的前例支持保守持久化；uv 支持區分破壞格式與相容擴充；附件中的 npm 拒絕邏輯提醒我們不能丟棄未知資料。這些前例共同支持 C1＋D1，但不支持「同 schema 解析成功就可以重新序列化」。

尤其 metadata 若記錄「哪些 append 行是工具實際加入的」，舊格式沒保存這件事，新引擎不能從目前檔案反推所有權。這種遷移不是補一個 schema 欄位就完成；無證據時只能保留內容並明確報告。

**第三，version.toml 第一行可以和 schema 共存，但這是一個雙層契約。**  
舊啟動器先用既有文字規則選引擎，新引擎再解析完整 TOML。因此 schema 不能要求啟動器先理解新格式，也不能准許 TOML 合法但舊 parser 取到不同 ref 的表示法。真正要驗的是每一代已釋出的 parser，不是新寫的範例 grep。

**第四，永久 floor 比 SemVer 更強。**  
SemVer 告訴使用者哪個版本可能改變介面，不能授權撤销已承諾的永久支援。可以在 major 停止舊薄殼的一般工作流程，但必須留下能將它帶到新狀態的救援能力。若不願長期維護這個相容層，就不能同時承諾固定 floor 與直接跨版。

**第五，驗收必須保留歷史輸入，但不必把所有維度盲目相乘。**  
歷史 driver、歷史資料與真實入口是不可省略的部分；全版本兩兩組合則未必增加對承諾的有效覆蓋。從已釋出版本各自指向候選、補上連升與破壞邊界，才能把成本控制在線性成長，同時保留 #1048 要求的歷史證據。

另有一個必須先修正的設計缺口：**放在 gen 的 hash 不能單獨承擔「這份 tracked 薄殼從未被改過」的判定。**若這點未解，fresh clone 的第一次 upgrade 就可能在安全性與可用性之間無解。

## 定案前要問的問題

1. **固定 floor 究竟是哪個實際 release？**  
   要記錄其薄殼、bootstrap、引擎及 fixture digest；若尚無正式版，應從第一個具備完整相容封套的版本開始承諾。

2. **跨 major 承諾到哪一層？**  
   建議明定：舊薄殼至少可救援升級，舊資料可直接遷移；是否還要求所有舊薄殼直接執行新 major 的一般命令，需要另外決定。

3. **fresh clone 缺少 `gen/.stamp` 時，用什麼證據辨識原始薄殼？**  
   候選是可重建的歷史 release 產物，或受追蹤的來源／產物紀錄；不能把「stamp 不存在」視為可覆寫。

4. **歷史 bootstrap 真正支援哪個 override 介面？**  
   brief 的 `--local` 與紀錄待定的 `--image`／`--image-tar` 不一致；必須以實際交付介面決定驗收及救援方式。

5. **是否要求未知 schema 一定印出精確的最低引擎 X？**  
   若是，從 floor 起就須固定 `min_reader` 或等效封套；否則只能保證明確拒絕，不能保證知道未來版本號。

6. **降版的承諾是安全拒絕，還是保證轉換成功？**  
   建議只保證可無損轉換者成功，其餘修改前拒絕；不可承諾任意 major 降版。

7. **哪些檔案屬於自有、哪些即使在 `.vendor_kit/` 內也屬於使用者可編輯內容？**  
   需要逐檔列明，尤其 version 宣告、metadata、baseline 與被修改的薄殼；目錄位置本身不能代表覆寫授權。

8. **「永不覆蓋」是否沿用既有決策的意義：不盲目覆蓋，但允許同意後替換／合併？**  
   這也要和「不刪檔，但可經同意移除工具曾插入的精確行」分開寫，避免不變量與既有 upgrade／uninstall 規則互相矛盾。

9. **發行驗收要承諾哪些環境交叉組合與執行成本？**  
   包含 Docker 上界、Git 下限或測試基準、WSL2 架構，以及是否接受「每個歷史版本在下限完整跑、其他環境按世代覆蓋」。這是 F 能否永久履行的實際預算。
