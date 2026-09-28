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
