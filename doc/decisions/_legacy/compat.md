# 相容性承諾 —— 雙軌分析（2026-09-19）

狀態：**草案，待使用者拍板**。

## 一致
- 整體方向一致：A1（薄殼只轉發）＋修訂後的 A2、B1＋B2 合併（每檔各自 schema、同 schema 內只加不改）、C1（新讀舊、只在本來要寫該檔的明確動作寫回、metadata 遷移交給 upgrade vendor_kit）、D1（schema 高於本機→寫入前拒絕）、E1 的 semver 語意＋E2 的固定 floor 常數、F 全做但矩陣線性成長（每個已釋出版各一條→候選，加連升／格式轉換邊），不做全版本兩兩相乘。
- A3、B3、C2、C3、D2 都否決，理由相同：A3 雞生蛋（upgrade 本身要靠舊入口）、B3 舊引擎無從辨識新檔、C2 多一個動詞、C3 是滑動窗口違反永久 floor、D2 只警告會退化成靜默丟棄再改寫（pnpm/yarn 就是實證）。
- 「薄殼只轉發」不等於沒有相容面：兩邊都指出 vendor.just 內仍有 recipe 名、argv、docker run 那行、exit code、resolve stdout 解析這幾段已出貨的協定，這些才是真正要凍結的東西。
- E1 的「floor = 上一個 major 最後一版、永久不滑動」自相矛盾：每次 major 重算就是以 major 為單位的滑動窗口，違反 #1041。floor 必須是一個明示的固定 release 常數，只能經 ADR 提高。
- Q10(2) 的 hash 放在 gen/.stamp 是硬缺口：gen/ 不進 git，fresh clone 沒有 stamp，第一次 upgrade vendor_kit 在「拒絕」與「盲寫」之間無解。兩邊都要求另一種不依賴本機狀態的原產物證據。
- D1 的「同 schema 未知欄位忽略」不夠，必須「讀時忽略、寫時保留」（npm arborist「must not drop」），否則 dev -i 舊 image 跑一次 upgrade 就刷掉新欄位。
- 「印需要引擎 ≥ X」要能成立，檔內從 floor 起就得有寫入者版本／min_reader 欄位（Terraform terraform_version 式）；沒有的歷史檔只能誠實印「未知格式＋救援指令」。
- 跨多版遷移一律「讀任一舊 schema → 直接寫當前 schema」，不能靠逐版鏈式（Copier 鏈式的失敗模式：遷移碼放在使用者永遠不會跑的版本裡）。
- 降版不能一概承諾成功：只有同 schema／可無損轉換才要求成功，其餘必須在修改任何檔之前乾淨拒絕（Terraform 明文不保證降版、K8s 只保證 N-1 rollback）。
- 驗收要用真實已釋出物驅動候選，fixture 由對應歷史引擎產生並固定 digest，不能用候選模擬舊格式（#1048）；#1057 收斂比對要有明列的排除清單（時間戳、digest、絕對路徑），但薄殼內容、ref、所有權紀錄不能排除。
- 舊 bootstrap.sh 在已升級的 repo 再跑是草稿漏掉的反向情境，要列入驗收。
- agy 的多項前例引用有誤（Cargo RFC 3301 不存在、K8s 12 個月／3 release 是 Beta 數字、SemVer FAQ 沒有列舉檔案格式、just set minimum-version 在 1.33 會直接 error、Gradle wrapper 並未「消除」問題、Yarn/pnpm 舊讀新不是硬拒絕、Poetry 範圍內只 warning、Renovate 沒有固定支援期、模式 5 自動建 commit 違反 Q5）。

## 分歧與取捨
### A2 要不要保留「先問引擎」的握手？
- Claude：A2 不符限制：每次 just 呼叫多起一個容器、破壞 v2.2 的快路徑；contract.md 已定案為宣告式（薄殼每次送 --protocol P，引擎依 P 輸出），Docker Engine API 同型，零成本且能讓引擎知道呼叫方多舊。
- codex：A2 符合限制但要修訂：探測入口需穩定、不依賴 gen 或業務 schema，且不相容時不能只「拒絕並要求 upgrade」，要有獨立救援路徑，否則死路。
- 取捨：採 Claude 的宣告式，這才是真正的 A2 修訂版：把「先問」改成「每次呼叫附帶 P」，成本歸零、引擎能依 P 回應，又滿足 codex 的要求（探測不依賴 gen、救援路徑獨立單段）。但要注意：我在本工作區找不到 Claude 引用的 decisions/contract.md（notes 第 5 項只寫「image LABEL 帶契約版本號、啟動器用 docker image inspect 比對」），「--protocol P 已定案」這句要請使用者確認；若尚未定案，這次就一起定。

### 薄殼自描述首行（# vendor_kit-shell/P engine=vX sha256=…）能否解決 fresh clone 的 Q10(2) 缺口？
- Claude：可以：把本體 hash 寫進 tracked 薄殼首行，任何引擎重算即驗，不依賴 gen/。
- codex：只提出需求：缺 stamp 時必須取得「可信的歷史原產物或等效持久證據」，無法證明就不得覆寫；沒指定機制，並警告「註解裡的版號本身沒有協商能力」。
- 取捨：Claude 的首行自描述是最省的落地做法，且能同時解決 codex 要的「fresh clone 不盲寫」，建議採用。但要補兩點：(1) 它證明的是「檔案內容等於寫入時的內容」，不是「等於 vendor_kit 某 release 的正式產物」——被竄改後重算 hash 也能自洽，所以引擎端還要能用 release 產物（image 內含的薄殼模板）二次比對；(2) 首行 hash 只是 Q10 的判定依據，協定協商仍靠 --protocol P，兩者別混。

### E1 的 major 語意：major 能否破壞協定／撤銷舊薄殼的一般呼叫？
- Claude：major = 提高 floor 或需要手動步驟；協定版號 P 獨立；引擎永遠接受 [floor_P, current_P]。「major = 協定破壞」與「必須接受上一個 major 的薄殼」互斥，所以 major 不等於協定破壞。
- codex：允許 major 停止舊薄殼的「一般工作流程」，但必須保留探測、解析目標、upgrade vendor_kit 救援與舊資料遷移能力（一般執行與救援分層）。
- 取捨：兩者其實可以合併，codex 的分層更務實：永久義務只需涵蓋「救援路徑（install／upgrade vendor_kit／sync 的不符提示）＋舊資料可讀可遷」；舊薄殼直接跑新 major 的一般 verb 可以只回 1 並提示升級，不必永久保證。Claude 的「P 與 release 版號分開、引擎接受區間」是機制，codex 的「一般 vs 救援分層」是承諾範圍，兩個都寫進契約。

### version.toml 的「第一行」到底是不是契約？
- Claude：不能以行號當契約，應以 key regex（^vendor_kit\s*=）為契約，與 Renovate preset 共用單一來源；第一行只是 install 寫出時的慣例。
- codex：第一個實體行固定為 vendor_kit = "<ref>"，第二行 schema；並禁止 BOM、前置空白、重複鍵、同名旁路解析，且要驗每一代已釋出 parser。
- 取捨：以 regex 為契約較耐 formatter 與人手註解，採 Claude；但 codex 的 byte-level 規則（禁 BOM、禁重複鍵、禁 [vendor_kit] 表旁路等 TOML 合法但舊 grep 讀錯的寫法）是 regex 方案必須補的限制，兩邊合併：契約 = 「唯一一行符合 regex，且不得有任何 TOML 合法但 regex 讀不到／讀錯的等價寫法」，驗收矩陣加「歷史啟動器 parser × 合法／異常 TOML」那一列（codex 表第 11 列）。

### 驗收矩陣的環境交叉範圍與成本上限
- Claude：≈ |R| + 10 個 job，just 兩端點與 arm64 只對 floor 與 N 跑；訂 wall ≤ 30 分或 |R| ≤ 40，超過才以 ADR＋major 談提高 floor，不能讓成本反過來決定 floor。
- codex：完整交叉是 8S（Docker 兩端點 × just 兩端點 × 兩架構）；建議每個歷史版本在最低環境跑完整流程，其他環境按協定／格式／產物世代覆蓋，並公開覆蓋規則；多列 Docker 上界、WSL2、中斷恢復、使用者保護等案例。
- 取捨：採 codex 的「每個歷史版本在最低環境跑完整，其他環境按世代覆蓋」作規則，並用 Claude 的成本上限當觸發條件。Claude 的矩陣漏掉 codex 的中斷／重跑、使用者修改薄殼、只改第一行（模擬 Renovate 後 frozen sync）這三列，要補；codex 的矩陣沒有明訂數字上限，要補。

### agy 對 Gradle Wrapper 前例的用法
- Claude：agy 把最有用的前例歸到「不存在此問題」：Gradle 官方明寫「舊 wrapper 可跑新 Gradle、跑第二次 wrapper task 重產」，這正是 A1 ＋ upgrade vendor_kit 重產薄殼的同構前例。
- codex：只指出 agy 的「架構消除」「一次指令更新所有 wrapper 檔」「相鄰 major」都證據不足，沒有把它當正面前例。
- 取捨：Claude 對：Gradle 是本題最貼切的正面前例（舊啟動器啟動新引擎→引擎重寫啟動器→第二次執行完成），應寫進 ADR 引用，但引用時照 codex 的提醒，不宣稱「消除問題」或「相鄰 major 保證」。

### bootstrap.sh 的來源與 override 介面
- Claude：驗收要用「GHCR 上真實的 bootstrap.sh(r)＋引擎 image r」。
- codex：bootstrap 已定交付位置是 GitHub Releases，不是 GHCR；且 brief 的 --local 與紀錄待定的 --image／--image-tar 不一致，要以實際交付介面決定驗收與救援。
- 取捨：codex 對。本工作區 CONTEXT.md 與 notes 都寫 bootstrap.sh 是「release 附」，image 才在 GHCR；契約第 10 條的「永不刪除」要分開寫成「GitHub Release 資產永不刪除＋GHCR image 永不刪除」。override 旗標名要請使用者定。

## 前例／brief 查證
- Cargo：RFC 3301 不存在，v4 由 cargo PR #12852 穩定化；正確前例是 encode.rs 的「讀先出貨、等一段時間讓 stable 與前一兩版都能讀，才切預設寫出」，且 1.83 起寫出版本依 rust-version（MSRV）決定；[metadata] 表 Cargo 自己註明是壞主意，不能當「舊版保留未知資料」的正面前例；「目前支援 V1–V4」不等於官方永久承諾。
- Gradle Wrapper：官方文件明寫「舊 wrapper 可跑新 Gradle、需跑第二次 wrapper task 才更新 jar」，這是承認問題並解決的同構前例，不是「架構消除」；文件中沒有「相鄰 major 保證相容」這句。
- pnpm：舊版讀到不相容 lockfile 只印 WARN Ignoring not compatible lockfile 然後重解析改寫，只有 --frozen-lockfile 才報 ERR_PNPM_LOCKFILE_BREAKING_CHANGE；是 D2 的反例，不是「拒絕」前例。
- Yarn Berry：Project.ts 只有 lockfileVersion < LOCKFILE_VERSION → needsRefresh，沒有「高於本機就拋錯」；高版 lockfile 會被照讀並可能被降版改寫。
- Poetry：locker.py _READ_VERSION_RANGE = ">=1,<3"，範圍內但高於本機只 logger.warning 並繼續，超出範圍才 raise；欄位在 [metadata] 不是 [package.metadata]。
- npm：Arborist 對超過 maxLockfileVersion 硬拒絕（ELOCKFILEVERSION），不是「降級解析或覆蓋」；沒有證據支持固定 1–2 major 支援窗口；引用時要標 client 版本與 lockfile 版本。
- git：gitrepository-layout 對 extensions.* 明寫「MUST NOT proceed」，未知 extension 是硬停；git 也有全域的 core.repositoryformatversion；不能概括成「新資料全能被舊 client 優雅忽略」。
- Kubernetes：GA 是「同一 major 內不得移除」，「9 個月或 3 個 minor」是 Beta；漏掉最相關的 Rule #4b（storage version 要等到有一版同時支援新舊格式之後才能推進，保證 upgrade 後可 rollback）。
- Terraform：1.x 承諾只涵蓋升級方向，官方明寫降版不保證（新 state 格式可能無法被舊版讀）；抽查 read.go 顯示 binary v0 state 仍被拒絕，不是全歷史格式永久可讀。
- SemVer：官網只要求「宣告 public API」與 deprecation 先出 minor，沒有列舉 CLI／wire protocol／檔案格式；正確論證是 vendor_kit 自行把這些列入 public API；SemVer 也不替專案訂永久 floor。
- just：set minimum-version 是 1.55 才有，實測 1.33.0 回 error: Unknown setting 並 exit 1；floor 是 just ≥ 1.33 且 entry.just/tools.just 零 set，這個機制不能落地，只能借概念。另 just 1.x 有多次行為回歸（1.40、1.42.x、1.52、1.53），不是「完全向後相容」。
- Renovate：設定驗證、strict 模式與一般執行行為不能混用；引用的 validator 頁面 404，沒有固定 1–2 major 支援期依據；能保留的只有「執行時遷移＋選擇性提設定遷移 PR」。
- pre-commit：minimum_pre_commit_version 只證明「可宣告讀者需求」，不證明永久無條件向後相容。
- Compose：v1 各發行版行為不同，不能合併描述為「必然拒絕」；Compose 拿掉 version 是因為它是使用者手寫宣告檔，vendor_kit 的檔全是機器寫的，B3 不適用。
- uv：uv_lock.rs 來源 404，官方只說 uv.lock schema 是 public API、只在 minor 破壞性提升，沒有 revision 行為描述；「高於本機安全忽略」未經查證，要標未查證。
- Copier：跨版 migration 取決於模板作者是否提供每一步且可組合，不能直接證明任意跨版；鏈式遷移的失敗模式（遷移碼在使用者永遠不會跑的版本）反而是要避開的。
- agy 模式 1（min_engine_version 擋本機舊引擎）：vendor_kit 的引擎由 version.toml 指定、啟動器 docker pull 來跑，同 commit 必同引擎；「本機舊引擎讀新專案」只發生在 dev -i 舊 image 或 -t 降版；真正主題是「舊薄殼叫新引擎」，agy 完全沒分析。另外 image tag 是否不可變、local override 都影響「同 commit 同 image」的結論，精確識別要靠 digest。
- agy §三.4「CI 校驗 gen/.stamp 版本」不成立：gen/ 是 gitignored，CI 看不到；要擋舊引擎寫的 tracked 檔只能靠檔案自身的 schema／寫入者版本欄位。
- agy 模式 5「just vendor-kit-upgrade 自動建獨立 commit」違反 Q5（vendor_kit 不 commit、不開 PR），指令名也不是既定介面，不能採。
- brief 本身的三處：(a)「引擎與它寫的檔在同一 commit 永遠一致」不是窮盡事實——Renovate 只改第一行就形成新引擎宣告＋舊薄殼／metadata，gen/cache 也不受 commit 固定；(b)「沒 pull 的人用舊引擎讀新檔不會發生」要寫成成立條件，dev -i 是明確入口；(c) bootstrap.sh 交付位置是 GitHub Releases，不是 GHCR。

## 最終建議
採 A1 ＋ 宣告式協定（薄殼每次呼叫附 --protocol P，引擎依 P 輸出，取代查詢式 A2）；B1＋B2 合併（每檔各自 schema = N 與寫入者版本，同 schema 只加不改、讀忽略寫保留，version.toml 以 key regex 為契約並禁止 TOML 旁路寫法）；C1（新讀舊在記憶體轉換、只在本來要寫該檔的明確動作寫回、跨版直遷不鏈式、metadata 遷移由 upgrade vendor_kit 做並在 dry-run 明列、遷移在拿鎖與進度日誌內完成）；D1（schema 高於本機→任何寫入前退出，有 min_reader 才印精確 X，否則印未知格式＋救援指令；dev -i 舊 image 禁止重產 tracked 薄殼）；E：保留 semver 語意但 major 只允許「提高 floor 或需手動步驟」，floor 是 PRD 明示的固定 release R0（含產物 digest），只能經 ADR 提高；永久義務分兩層——救援路徑（install／upgrade vendor_kit／sync 不符提示、單段轉發、不依賴 resolve/apply 與 gen）與舊資料可讀可遷是永久，舊薄殼跑新 major 一般 verb 可只回 1 提示升級；補「讀先出貨、寫延後」原則（同 major 內 N-1 必能讀 N 寫的檔）。Q10(2) 改為 tracked 薄殼首行自描述（# vendor_kit-shell/P engine=vX sha256=…），並由引擎再對 release 內模板二次比對，不依賴 gen/.stamp。F：以 floor 以來每個真實已釋出 bootstrap.sh（GitHub Releases）＋ image（GHCR）驅動候選，每版一條臂＋連升／格式轉換邊，線性成長；每個歷史版本在最低環境（Docker 19.03、just 1.33.0）跑完整，其他環境按世代覆蓋並公開規則；矩陣以 Claude 的 F1–F10 為骨幹，補 codex 的「只改第一行後 frozen sync」「fresh clone 無 gen」「使用者修改薄殼／未納管檔」「中斷與重跑」「歷史 parser × 合法／異常 TOML」五列；降版只對可無損轉換要求成功，其餘乾淨拒絕並指引 git revert；「< floor 太舊」是唯一可用 synthetic 的格；訂成本上限（例如 wall ≤ 30 分或 |R| ≤ 40）當作觸發討論的條件而非決定 floor 的依據；已釋出 image、bootstrap.sh 與 fixture 永不刪除。契約條文以 Claude 的 12 條為底，併入 codex 的第 1（主機依賴不得新增）、5（byte-level 規則）、6（無法還原的所有權資訊不得猜）、8（min_reader 封套）、10（-y 不授權覆蓋、失敗不留混合狀態）。ADR 引用前例時只留已查證者：Gradle wrapper、Cargo encode.rs／resolve.rs、git repository-layout、K8s Rule #4b、Terraform version/terraform_version、npm arborist、Docker Engine API 版本協商；pnpm／yarn 當 D2 反例；uv、Renovate 支援期、agy 的 RFC 3301 一律刪除或標未查證。

## 要問使用者
- 「薄殼每次呼叫送 --protocol P、引擎依 P 輸出」Claude 說 decisions/contract.md 已定案，但本工作區找不到該檔（notes 第 5 項只寫 image LABEL＋docker image inspect 比對）。這條是已定還是要在這次一起定？
- 固定 floor R0 是哪個實際 release？是否就是第一個正式版 v1.0.0／P=1／schema=1？提高 floor 的程序（ADR＋major＋提前一個 minor 公告）可以接受嗎？
- 跨 major 的永久義務要到哪一層：只保證救援路徑（install／upgrade vendor_kit／sync 提示）與舊資料可讀可遷，還是也要求舊薄殼能直接跑新 major 的一般 verb？
- tracked 的 entry.just／vendor.just／ci/check.sh 首行寫入 # vendor_kit-shell/P engine=vX sha256=… 自描述，可以接受嗎？若不接受，fresh clone 無 gen/.stamp 時 upgrade vendor_kit 要拒絕還是用什麼證據？
- 舊 bootstrap.sh 在已裝有較新 version.toml 的 repo 再跑：defer 到 version.toml 指定的引擎，還是直接拒絕並印「請用 upgrade vendor_kit」？
- 歷史 bootstrap.sh 的 image override 介面到底是哪個（brief 的 --local，或紀錄待定的 --image／--image-tar）？這決定驗收能否用舊 bootstrap 驅動候選。
- 降版承諾：(a) 同 schema／可無損轉換時 upgrade vendor_kit -t 舊版必須成功、其餘乾淨拒絕（兩位一致建議），還是 (b) 一律只保證 git revert？
- 協定不合／太舊要不要專用 exit code（例如 3），讓 CI 能與一般失敗 1、衝突 2 區分？
- upgrade vendor_kit 一次改寫所有 baseline/<repo>/.vendor_kit.toml 是否接受？同一專案短暫混合 schema 是否列為合法狀態？舊格式沒記錄的所有權（append 行歸屬）無法還原時，停下報告可以嗎？
- #1057 升級／全新一致比對的排除清單要哪些欄位（digest、時間戳、最後合併版本、絕對路徑）？baseline/ 納不納入？
- dev vendor_kit -i <舊 image> 的舊引擎是否禁止跑 upgrade vendor_kit 重產（降版）tracked 薄殼？建議禁止或必問。
- 驗收預算：每次 release 可接受的 wall time 與 |R| 上限各多少？是否接受「每個歷史版本在最低環境跑完整、其他環境（Docker 上界、just 最新、arm64、WSL2）按世代覆蓋」的規則？
- Renovate：是否出 preset 建議 major 分開 PR（matchUpdateTypes），並與 version.toml 的 key regex 共用單一來源？
- 已釋出的 GHCR image、GitHub Release 的 bootstrap.sh 與 fixture image「永不刪除」要不要寫成契約？

---
## 附：Claude 原文
選擇：A1＋修訂 A2；B1＋B2（每檔獨立 schema，不建全域同步升版的 schema）；C1；D1；修訂 E1＋E2（固定 release R0 定義永久 floor，SemVer 保留但 major 不撤銷 floor 的救援與遷移義務）；F 全部類型納入但不做不必要的全版本兩兩乘積。

關鍵修訂：A2 要有穩定探測入口與獨立救援路徑，不能只「拒絕並要求 upgrade」；F 區分「必須成功」與「必須安全拒絕」。

另一個必須先修的設計缺口：放在 gen 的 hash 不能單獨承擔「這份 tracked 薄殼從未被改過」的判定；fresh clone 第一次 upgrade 會在安全與可用之間無解。

=== 相容性契約條文草稿（12 條，可直接進 PRD）===
1. 主機與公開介面。vendor_kit 僅要求既定平台上的 Docker ≥19.03、Git、just ≥1.33.0；不得新增額外主機工具需求。公開 recipe、CLI argv、退出碼、薄殼啟動協定、resolve stdout 與持久化檔案格式均列入相容性契約。
2. 永久支援集合。首個承諾版本記為固定 release R0 並記錄其不可變產物識別（digest）；R0 起的正式發行薄殼、bootstrap 與正式產出格式持續納入支援集合，不因新 major 發布而移除。新引擎須提供從這些版本直接升級的路徑，不得要求使用者手動逐版執行。
3. 一般執行與救援分層。同 major 內保留所有已承諾薄殼的一般呼叫能力；跨 major 至少保留歷史入口所需的探測、解析目標與 upgrade vendor_kit 救援能力，以及舊資料讀取／遷移能力。一般命令可因需重產薄殼而回 1，但不得因此封鎖救援路徑。
4. 協定與退出碼。薄殼標記協定世代，候選引擎宣告可接受的協定集合；探測不得依賴 gen 或當前業務 schema。保留 vk-resolve/1 的完整機器可讀文法，診斷只寫 stderr；未知協定、輸出不完整或解析失敗不得繼續操作。保留 0 成功、1 錯誤或需使用者處理／重跑、2 合併衝突的語義；自身升級完成須停下並回 1 提示重跑。
5. 各檔格式。version.toml 第一個實體行固定為 vendor_kit = "<ref>"，第二行為 schema = N；禁止 BOM、前置空白行、重複鍵及同名旁路解析。其他持久化 TOML 各自具有 schema；stamp 另定格式識別，不改變其引擎 ref＋薄殼 hash 的既定用途。只有明列的歷史格式可將缺少 schema 視為 legacy 格式。
6. 新讀舊與遷移。新引擎須讀取支援集合內的舊格式，必要時在記憶體轉換；只有原本授權寫入該檔的明確動作才能持久化。既有 metadata 的格式遷移由 upgrade vendor_kit 執行；缺失且無法可靠還原的所有權或來源資訊不得猜測，須停止受影響操作並提供處理方式。
7. 未知格式與擴充。讀者不支援的 schema 必須在修改專案持久化資料前非零退出，說明檔案、現有格式與支援範圍。同 schema 的未知欄位僅可在其語義確實可忽略時略過；寫回須保留未知資料，不能保留則拒絕。需要讀者理解的新語義必須升 schema，或使用事先定義、未知即拒絕的必要能力欄位。
8. 最低讀者提示。若要保證輸出「需要引擎 ≥X」，須從 R0 起提供舊讀者可辨識的固定需求封套（例如每檔 min_reader）並驗證其與 schema 一致；它是必要條件，不取代 schema 支援檢查。對沒有這項資訊的歷史檔，只能誠實輸出未知格式及可用救援指令，不得猜測 X。
9. sync 與重產。sync 只寫 cache/gen；薄殼不符時回 1 提示 upgrade vendor_kit。薄殼僅由 install／upgrade vendor_kit 重產，且須證明現內容等於原產物。gen/.stamp 只能作快取證據；缺失時須取得可信的歷史原產物或等效持久證據，無法證明時不得覆寫。
10. 使用者檔與失敗恢復。使用者檔可建立並列明；修改須先取得同意，-y 只省略詢問，不授權覆蓋既有未納管檔；不刪檔、不盲目覆蓋。遷移與升降版須先完成可行性檢查，失敗不得留下無法辨識的混合狀態，重跑須可安全恢復；合併衝突狀態另依回 2 契約處理。
11. SemVer 與降版。對已宣告介面的不相容變更使用 major；minor 增加相容功能，patch 修正相容缺陷。可移除介面須至少先於一個 minor 發布棄用通知，但不得移除第 2、3 條的永久義務。降版只有在目標可讀或可無損轉換時成功；否則在修改 ref、metadata、薄殼及使用者檔前拒絕。
12. 發行驗收。候選版本必須由支援集合內真正已釋出的薄殼與 bootstrap 驅動驗收，涵蓋直接跨版、連續升級、降版、local override、無 gen 的 fresh clone、使用者修改及中斷恢復。新安裝測試另保留；任何必要歷史案例未通過或未執行，不得宣告相容驗收完成。

=== 驗收矩陣 ===
符號：Rᵢ = 支援集合中的歷史正式版本；C = 候選；Rⱼ = 另一已釋出版本。歷史 fixture 必須由對應歷史引擎產生並固定 digest；不能用 C 模擬舊格式。

| 案例 | 驅動者／起始狀態 | 目標與流程 | 合格結果 | 覆蓋 |
|---|---|---|---|---|
| 歷史薄殼完整流程 | 每個 Rᵢ 真實薄殼＋其 fixture | ref 指向 C；sync → 明確 upgrade → 重新呼叫 → 完整流程 | sync 不改 tracked 檔；舊入口可救援；重跑後正常 | 每個薄殼發行版本 |
| 舊 bootstrap 固定引擎 | 每個已釋出 bootstrap | 不覆寫內嵌 ref，首次 install／再跑修復 | 使用其所屬引擎；修復不破壞既有檔 | 每個 bootstrap 版本 |
| 舊 bootstrap 呼叫候選 | 每個歷史 bootstrap 的 image override 入口 | 指向 C，首次 install／修復 | 舊參數與呼叫協定可用 | 每個具有該入口的版本 |
| 第一行單獨升版 | 真實舊專案，只改 engine ref | frozen sync、verify、upgrade --dry-run 等流程 | 不因只改一行就誤判通過；需要升級時回 1 並給可執行指令 | 每個介面／格式世代 |
| fresh clone | 歷史 tracked 檔，無 cache/gen/stamp | 直接啟動救援並升至 C | just 可載入；缺 stamp 不導致盲目重產 | 每個薄殼世代 |
| 連續升級 | Rᵢ 專案 | Rᵢ → Rⱼ → C，各階段重新呼叫 | 第二次升級入口仍存在且有效 | 相鄰發行邊及每個協定／schema 轉換邊 |
| 固定 floor 跳升 | R0 原始專案 | 不逐版，直接升 C | 跨所有中間世代成功，或依使用者檔規則明確待處理 | 每次發行必跑 |
| 可相容降版 | C 升級後的專案 | upgrade vendor_kit -t Rᵢ | 能安全轉換者成功；重跑目標引擎可用 | 每個受測目標格式世代 |
| 不可相容降版 | 含較新必要語義的專案 | 降至不支援的 Rᵢ | 修改前拒絕；不先改 ref 留下壞狀態 | 每個格式破壞邊界 |
| 舊引擎讀新檔 | 新專案＋dev -i 舊 image | 普通命令與會寫檔命令 | 未知 schema 安全拒絕；已宣告可忽略擴充不遺失 | 每個讀者／格式能力世代 |
| 第一行與解析一致性 | 真實舊啟動器＋合法／異常 TOML | BOM、空白、重複鍵、第二行 schema、local override | 合法格式取到相同 ref；異常格式明確失敗 | 每個啟動器 parser 世代 |
| 使用者保護 | 修改薄殼、既有未納管檔、append 零／多命中 | upgrade／install，含 -y 與非互動 | 不覆蓋、不刪檔；詢問、警告、退出碼符合契約 | C 完整分支＋歷史資料世代 |
| 中斷與重跑 | 遷移前、中、後的故障注入 | 再次執行既有指令 | 保持原狀或可辨識恢復；不把半完成視為成功 | 每個寫入階段 |
| 升級／全新一致 | 歷史專案升 C；另以 C 全新 install | 相同工具、ref 與選項 | 自有確定性產物一致；受保護的使用者差異明列 | 每個歷史產物世代 |
| 主機下限 | 上述歷史驅動案例 | Docker 19.03、just 1.33.0；另跑目前支援端點及架構 | 不依賴新版主機功能；兩平台 image 可執行且內容符合契約 | 明定的環境組合 |

矩陣成本與執行方式：S 個歷史版本各自跑向 C 是 S 條邊、不是 S²；連升採「相鄰邊／格式轉換邊＋C」維持線性；跨版直接路徑不能只測 R0→C 代替所有歷史版本；Linux 完整交叉兩個 Docker 端點×兩個 just 端點×兩架構為 8S，WSL2 另列；建議每個歷史版本在最低環境跑完整流程、其他環境按協定／格式／產物世代覆蓋，並公開這個覆蓋規則；相同產物與協定可依 digest 證明後共用結果但保留對應關係；時間戳、絕對路徑可正規化，薄殼內容、語義必要欄位、ref、所有權紀錄不能為了通過而忽略。

## 附：codex 原文
## 選擇
**A1 + 宣告式協定（取代 A2 的查詢式）**、**B1（含 B2 的「同 schema 只加不改」與「讀先出貨、寫延後」）**、**C1（跨版直遷、以檔為單位、只在明確動作寫回）**、**D1（加寫入者版本、讀忽略寫保留）**、**E1 的 semver 語意 + E2 的明示 floor 常數 + contract.md 的協定整數 P**、**F 全做但矩陣 O(|R|)**。

## 針對「薄殼只轉發是否真的能讓舊薄殼叫新引擎」
只轉發是必要不充分。舊 vendor.just 裡仍有五段真正的協定：(1) `version.toml` 引擎 ref 那行的 grep；(2) `gen/.stamp` 第一行比對；(3) 那一條 `docker run`（/repo、/dist/<repo> mount、-u、env 轉發、tty）；(4) `vk-resolve/N` stdout 解析；(5) exit code 對應。各自的破壞點與對策：
- just recipe 名／命名空間／`upgrade vendor_kit` 這個 argv：凍結（條 1），新增 verb 對舊薄殼不可見是可接受的（just 會說 unknown recipe，使用者先 `upgrade vendor_kit`）。
- argv：舊薄殼無法補新必要參數 → 引擎對舊 P 一律有預設；新能力走旗標，由協定閘門擋（contract.md）。
- exit code：0/1/2 語意凍結；新碼只對宣告 P ≥ 新版的薄殼發出；舊薄殼對未知碼原樣傳出、不吞。
- resolve stdout：**薄殼每次呼叫送 `--protocol P`，引擎以 P 輸出**（Docker Engine API 版本協商同型）；舊薄殼永遠不會看到不認識的行別。這一條讓 A2 的「先問」不必要且省掉一個容器。
- gen/.stamp hash（Q10(2)）：gen/ 不進 git，fresh clone 沒有 hash → 改為薄殼自描述首行 `# vendor_kit-shell/P engine=vX sha256=<本體 hash>`，任何引擎重算即驗。
- bootstrap.sh：舊 bootstrap 在已升級的 repo 再跑會用舊引擎 `install` 降版重寫 → bootstrap 必須先讀既有 version.toml 並 defer/拒絕。
- 降版救援（新薄殼 → 舊引擎 `upgrade vendor_kit -t`）：只要 `install`／`upgrade vendor_kit` 是**單段轉發**（不經 resolve/apply 兩段協定），新薄殼就能叫任何 ≥ floor 的舊引擎重產薄殼。

## version.toml 第一行 grep 與 schema 共存
可以共存，但契約不能是「第一行」而是 **key regex**（`^vendor_kit\s*=\s*"…"`，與 Renovate preset、引擎共用同一來源；contract.md 已定「啟動器忽略不認得的行」）。「第一行」降為 install 寫出時的慣例。`schema = 1` 放第二行；啟動器不讀它，只有引擎讀；實際上只有 `dev -i 舊 image`／`-t 降版` 兩條路會讓舊引擎讀到高 schema。gen/*.stamp 同樣只凍結第一行，第二行 `schema`。

## 相容性契約條文草稿（12 條，可直接進 PRD）
1. **凍結介面（永久）**：根 justfile 那一行 `import '.vendor_kit/entry.just'`、`.vendor_kit/entry.just`、`vendor.just`、`ci/check.sh`、`version.toml` 與其中引擎 ref 行的 regex、`gen/.stamp` 第一行語意、命名空間 `vendor_kit`、救援動詞 `install`／`upgrade vendor_kit` 的名稱與 argv。只准新增，不准改名或搬移；若必須換名，舊名保留轉發器，且轉發器本身受本條保護。
2. **薄殼↔引擎協定 P**：單一整數，與 release 版號分開。薄殼每次呼叫都送 `--protocol P`（第一版即有）。引擎接受 [floor_P, current_P]，並**以呼叫方的 P** 輸出 `vk-resolve/P` 行別與 exit code 語意；對 P ≥ floor 的薄殼不得輸出其不認識的行別、不得要求其未提供的 mount／環境變數（缺少時明確拒絕）。新增 verb／旗標／行別／exit code 語意／印記第一行語意 → P+1。
3. **救援路徑單段化**：`install`、`upgrade vendor_kit`，以及 `sync` 的「薄殼不符→1 提示」判定，只用第 1 條的凍結介面（ref grep、一條 docker run、exit code），不依賴 resolve/apply 兩段協定；任何 ≥ floor 的薄殼都能經此路徑叫任何引擎重產薄殼，反向（新薄殼叫舊引擎降版）亦然。
4. **自有 tracked 檔自描述**：引擎產生的 `entry.just`／`vendor.just`／`ci/check.sh` 首行 `# vendor_kit-shell/P engine=vX sha256=<本體 hash>`（LF 正規化後計算）。「未被改過」以重算本體 hash 判定，不依賴 gen/；被改過 → 1 列差異不動（Q10）。
5. **檔案格式版號**：每個 vendor_kit 寫的檔各自 `schema = N`（`version.toml` 第二行、`baseline/<repo>/.vendor_kit.toml`、`gen/*.stamp` 第二行）並記寫入者引擎版本。同 schema 內只准新增欄位；讀方忽略未知欄位、寫方保留未知欄位（不得丟棄）。schema bump 只在 major。
6. **新讀舊**：引擎必須讀 floor 以來所有 schema，讀取不寫回；寫回只在本來就會寫該檔的明確動作（`install`／`add`／`remove`／`upgrade`），以該動作原本要寫的檔為單位，不順手遷移別的檔；跨多版一律「讀任一舊 schema → 直接寫當前 schema」，不得依賴逐版鏈。`upgrade vendor_kit` 負責把 `.vendor_kit/` 自有檔（含全部 baseline metadata）遷到本版 schema，並在摘要與 `--dry-run` 明列；同一專案短暫混合 schema 為合法狀態。
7. **舊讀新**：schema 高於本機 → 任何寫入前退出，訊息含「此檔由 vendor_kit vX 寫入，需要引擎 ≥ vX；請 `upgrade vendor_kit` 或使用 version.toml 指定的引擎」。不得降級改寫、不得忽略後重寫。
8. **讀先出貨、寫延後**：新 schema／新 P 的「讀」支援先釋出；只有當 floor 已涵蓋能讀它的版本後，才允許把它當預設寫出（Cargo encode.rs、git repository-layout、K8s Rule #4b）。因此同 major 內 N-1 版引擎必須能讀 N 版寫出的所有檔。
9. **SemVer**：major = 提高 floor（floor_P 或 schema floor）或需要使用者手動步驟；minor = 新功能（含 P+1、新增欄位）；patch = 修正。任何 ≥ floor 薄殼會呼叫的 verb／旗標／路徑，在 floor 未越過它之前不得移除；移除前至少一個 minor 印 deprecated 警告（警告是禮貌，floor 才是保證）。
10. **支援下限 floor**：PRD 常數，初值 = 第一個正式版（v1.0.0、P=1、schema 1）。只能經 ADR + major 明示提高，不得由「最近 N 版」或「上一個 major」推導。低於 floor 的薄殼／檔遇到新引擎 → 退出並印「太舊：請用 bootstrap.sh vY 重建」（不是協定錯誤）。已釋出的引擎 image、bootstrap.sh、fixture image 永不刪除（floor 義務與驗收需要）。
11. **降版**：同 schema 內 `upgrade vendor_kit -t <舊版>` 必須成功（第 3 條保證新薄殼可叫舊引擎）；跨 schema 降版不承諾，但必須乾淨拒絕並指出「git revert 整個升級 commit」。
12. **驗收**：每次 release 前對 floor 以來每個已釋出版本 r，用 GHCR 上真實的 `bootstrap.sh(r)` + 引擎 image r 建 fixture，再對候選引擎跑下表；任何從候選樹複製、stub、synthetic tag 替代已釋出物的測試不算驗收（唯一例外：第 10 條的「< floor 太舊」案例）。缺任一格不得出貨。

## 驗收矩陣（R = floor 以來所有已釋出版；N = 最新已釋出；C = 候選）
| # | 驅動者（真實已釋出物） | 被測 | 步驟 | 期望 | 對應 |
|---|---|---|---|---|---|
| F1 舊殼→新引擎 | bootstrap.sh(r)+引擎 r，∀r∈R | C | 建 fixture、add 一工具 → 第一行改為 C（模擬 Renovate）→ `just vendor_kit sync` → `just vendor_kit upgrade vendor_kit` → `sync` → 任一工具 recipe → `upgrade`（全） | sync：1 + 提示、不寫 tracked；upgrade vendor_kit：1 + 提示、薄殼重產；之後 0；第二次 upgrade 0 無變更 | #915/#1077/#1084 |
| F2 收斂 | F1 產物 | C | `.vendor_kit/` tracked 內容 vs bootstrap.sh(C) 全新 install + add 的 repo | 相同（排除清單明列：digest、時間、最後合併版本） | #1057 |
| F3 鏈式跨版 | bootstrap.sh(floor) | floor→r1→…→N→C | 逐版改第一行 + upgrade vendor_kit | 每步同 F1；終態同 F2 | 跨多版 |
| F4 降版 | bootstrap.sh(C) | 引擎 N | `upgrade vendor_kit -t vN` → sync → 工具 recipe → `upgrade vendor_kit`（回 C） | 同 schema：全部成功；跨 schema：乾淨拒絕 + revert 指引 | 條 11 |
| F5 太舊 | synthetic P/schema = floor−1（唯一 synthetic） | C | 任一動詞 | 退出、訊息「太舊請用 bootstrap.sh 重建」、零寫入 | #1049 |
| F6 舊 bootstrap 重跑 | bootstrap.sh(r)，r∈{floor,N} | 已在 C 的 repo | 再跑 bootstrap.sh(r) | 不降版：defer 到 version.toml 或明確拒絕 | 新 |
| F7 舊引擎讀新檔 | 引擎 r∈{floor,N} 經 `dev vendor_kit -i` | C 寫的 fixture | sync／upgrade | 寫入前拒絕、訊息含需要版本、不改 tracked | 條 7 |
| F8 CI frozen | F1 r∈{floor,N}，CI=1 | C | 同 F1 前半 | 1 列「薄殼不符」、零 tracked 寫入 | Q5 |
| F9 just 矩陣 | F1 r∈{floor,N} × just {1.33.0, latest} | C | 同 F1 | 同 F1 | Q8 |
| F10 arm64 | F1 r=N | C | 同 F1 | 同 F1 | Q4 |

規模：不同 job ≈ |R| + 10（F2/F8 可搭 F1 同 job），每臂 3–5 分鐘、可平行；|R| 每月一版兩年 = 24，可行。訂上限（例如 wall ≤ 30 分鐘或 |R| ≤ 40），超過才討論以 ADR + major 提高 floor，不能讓成本反過來決定 floor。