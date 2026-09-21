# vendor_kit — 產品需求（PRD）

> 本檔是 vendor_kit 的北極星：每個決議都拿來對照的固定參考點。
> 它只放三層，其他一律不放：**核心不變量**（永遠為真、任何 ADR 不得違反的性質）、**設計原則**（兩個選項都可行時，用來取捨的判準）、**衝突優先序**（兩個正當性質不能兼得時，誰讓步）。
> 它只在**產品目標**或背後的判準改變時才改，機制換了不改。個別決議放 [`doc/adr/`](adr/README.md)；領域名詞放 [`CONTEXT.md`](../CONTEXT.md)；工作契約放 [`AGENTS.md`](../AGENTS.md)。
> 每條不變量寫「性質」與「為什麼固定」；「機制」另列並標明可換——機制的細節與理由屬於 ADR，本檔不重述。
> 標「> ⚠ 待拍板」的段落是尚未定案的項目，不得當成已定引用。

## 目的

vendor_kit 解決一個問題：**工具 repo（例：base）要把 `dist/` 送進很多下游專案，而 `git subtree` 與 symlink 把工具內容塞進下游 git、把升級變成人工作業、把使用者的檔與工具的檔混在一起。**

vendor_kit 產出的是一條**散播管線**：工具 repo 把 `dist/` 打包成純資料 image 推上 registry；下游專案用一份宣告（`.vendor_kit/version.toml`）鎖定要哪些工具、哪個版本、哪個引擎；每次打 `just`，工具內容從宣告決定性重建；初始檔建立後歸使用者，升級時三方合併；想改工具本身，一個動詞把它指向本機。

三個角色只對前兩個承諾：**工具 repo 開發者**（供應側，照契約出貨）、**使用者**（下游專案，每天打 `just` 的人與處理升級的人）、**vendor_kit 開發者**（我們，契約不對自己承諾）。

## 範圍

### 納入

- 工具 `dist/` 的**打包**（`Dockerfile.dist`、純資料 image）與**散播**（registry、tag@digest）。
- **鎖版**：專案對「用哪些工具、哪個版本、哪個引擎」的唯一宣告，與從宣告決定性重建快取。
- **初始檔管理**：`init.toml` 宣告的檔在專案裡建立一次、之後歸使用者、升級時三方合併、永不刪。
- **本機開發模式**：把某個工具（含 vendor_kit 自身）指向本機目錄或本機 image。
- **下游 CI 契約檢查腳本**：下游 CI 只呼叫它；它以結束狀態回報「宣告、快取、初始檔是否一致」。

**母體用推導，不列清單（P6）。** 初始檔要支援哪些類型（純文字、二進位、symlink、目錄），看工具實際在 `init.toml` 用了什麼；一個類型進入支援範圍，是因為有工具在用，不是因為它存在。

### 刻意排除

- **工具本身的功能**：`docker build`、compose 產生、部署等由工具的 just 模組提供；vendor_kit 只負責把模組送到專案並掛進命名空間。
- 多 registry 雙推、簽章／驗簽（第一版）、範本變數渲染。
- macOS、Windows 原生（WSL2 視同 Linux，在範圍內）。
- 下游專案的業務邏輯；工具 repo 之間的相容矩陣。

## 核心不變量

每條都是 vendor_kit 全域必須成立的性質，**任何未來的 ADR 不得違反**。「機制」是目前實現它的方式，可以被新 ADR 換掉；性質不行。列在各條下的 ADR 是建立或服務它的決議——它們記錄「怎麼做」與「為什麼這樣做」，本檔只記「它必須永遠成立」。

### 1. 使用者的檔歸使用者：可以建、要改先問、永不刪、永不覆蓋

**性質：** vendor_kit 對使用者的檔（根 `justfile`、初始檔、任何進下游 git 且不在 `.vendor_kit/` 薄殼內的東西）只有四種行為：**可以建**（但要明確印出建立或修改了什麼）；**要改先問**（`-y` 免問，仍印出改了什麼；非互動且無 `-y` = 不改並以 1 結束印出該打的指令，EOF 不算同意）；**永不刪**（含新版工具不再提供的初始檔，只 warn 並列清單）；**永不覆蓋**。

「永不覆蓋」的定義：**不用工具版本取代使用者的客製內容**。只有兩個明定例外，且都不是取代：(a) 根 `justfile` 加一行 `import`（無檔則建、有檔則詢問後 append）；(b) 已納管初始檔的三方合併（沒改 → 詢問是否換新版；雙方都改 → 詢問是否合併，衝突留標記由使用者解）。`add` 遇到已存在的檔：不納管、不覆蓋、只 warn。`remove`／`uninstall`：不刪初始檔，只印清單。

**為什麼固定：** 初始檔建立後就是使用者的程式碼；base 時代 `init.sh` 的 `rm -f` 與 symlink 接管，正是使用者無法信任「跑一次 just 不會弄壞我的檔」的原因。一個會刪或覆蓋使用者檔的散播工具，使用者只會在每次升級前先備份、然後不升級。

**機制（可換）：** baseline 全文 + `git merge-file --diff3` 逐檔狀態機；`adopted` 旗標；metadata 記錄「檔／行由我們建立」作為 uninstall 唯一刪除依據。

**建立／服務它的 ADR：** 待寫 ADR-xxxx（初始檔合併）、待寫 ADR-xxxx（檔案佈局）。

### 2. 一個來源：`.vendor_kit/version.toml` 是專案的唯一宣告

**性質：** 專案對「用哪些工具、哪個版本（tag@digest）、哪個引擎」只有一份宣告，進 git。工具內容是**快取**（不進下游 git），任何時候都能由宣告決定性重建；Renovate、`upgrade`、人手改的都是同一個檔。本機覆寫（`version.local.toml`）只覆蓋宣告中已存在的工具，不進 git，不是第二份真相。

**為什麼固定：** 兩份版本真相（例如 image tag 與另一個 lock 檔）會漂移，漂移是靜默的；digest 才鎖內容，tag 只給人與 Renovate 看。

**機制（可換）：** TOML；引擎行固定第一行讓啟動器用 `grep` 讀；Renovate 一條 regex manager 追 docker datasource。

> ⚠ 待拍板：檔名 `version.toml` vs `lock.toml`；工具 image 公開／私有（私有時主機 docker credential helper 是否為唯一認證路徑）。

**建立／服務它的 ADR：** ADR-0002（引擎與工具分離，在 proto）、待寫 ADR-xxxx（檔案佈局）。

### 3. 自動化只碰不進 git 的東西

**性質：** 每次 `just` 自動跑的前置（`sync`）只重建 `.vendor_kit/cache/` 與 `.vendor_kit/gen/`；任何要進 git 的寫入（宣告、初始檔、baseline、薄殼）都必須是使用者明確打的動詞。CI 下若判斷需要 tracked 寫入，以 1 結束並印出該打的指令，不偷補。

**為什麼固定：** 自動寫 tracked 檔的工具（npm 寫 lock、terraform 寫 lock）能成立，是因為那些檔「機器擁有、可由 tracked 輸入決定性重生、CI 有 frozen 模式」三條同時滿足；初始檔第一條就不過（建立後歸使用者）。一個在 `git pull` 後靜默建出未提交檔的工具，會讓 CI 測到跟開發者不同的內容。

**機制（可換）：** `sync` 只寫 `.vendor_kit/.gitignore` 涵蓋的路徑；`CI=1` 自動 frozen。

**建立／服務它的 ADR：** 待寫 ADR-xxxx（介面動詞）。

### 4. 永不靜默失敗

**性質：** 結束狀態 `0`／`1`／`2` 是契約（0 成功；1 失敗且不留半成品、宣告不動；2 完成但有衝突待人處理）。`sync` 發現「未完成接入」→ 1 提示 `add`；「baseline 落後宣告」→ 本機 warn 提示 `upgrade`、CI 下 1；`verify` 失敗 → 重裝並 warn，不靜默通過。任何 warn 都要說出是哪個檔、該打什麼。

**為什麼固定：** vendor_kit 站在每個下游 `just` 指令的最前面；它靜默失敗，錯誤就傳到每個下游而沒人知道。可信任是這個產品本身。

**機制（可換）：** 引擎統一映射結束碼（`git merge-file` 的原生狀態不直接當產品狀態）；`--porcelain` 給機器讀；metadata 記中間狀態讓重跑可續作。

**建立／服務它的 ADR：** 待寫 ADR-xxxx（介面動詞）、待寫 ADR-xxxx（初始檔合併）。

### 5. 主機只需 docker + git + just；正確性不綁單一平台

**性質：** 使用者的主機只需要 `docker`、`git`、`just`（最低版本待定）。支援 Linux amd64 與 arm64（含 Jetson）；WSL2 視同 Linux。不引進第三方 binary：只借主機已有的 docker 與引擎容器內的 `git merge-file`。任何被當作正確性依據的機制（鎖、路徑、symlink、行尾）都不得只在一個平台成立。

**為什麼固定：** 這是把安裝程式從 base 抽離的初衷：base 的下游有 Jetson、有 WSL2、有共用工作站，任何「主機要先裝 X」都會在其中一台失敗。

**機制（可換）：** 引擎 image 多架構（amd64 + arm64）；主機薄啟動器用 `docker create`／`docker cp` 抓 image 內容，享 daemon 快取與同一條認證路徑。

> ⚠ 待拍板：`just` 最低版本（ADR-0002 寫 1.33；需在 CI 用該版本重跑所有 just 實測後定案）；工具 dist image 是否單架構 `linux/amd64` 固定 `--platform` 拉（一份內容一個 digest）。

**建立／服務它的 ADR：** ADR-0002（在 proto）。

### 6. 引擎版本由專案鎖定；啟動器是不含邏輯的薄殼

**性質：** 一個專案只用宣告第一行指定的那一版引擎；引擎在容器內跑。專案裡進 git 的啟動器（`.vendor_kit/entry.just`、`vendor.just`、`ci/check.sh`）只做轉發：讀那一行、拉 image、起容器、原樣傳參數（`"$@"`）。規則只有一個擁有者——引擎；啟動器與 `check.sh` 不判斷、不修補。

**為什麼固定：** 啟動器一旦有邏輯，它跟引擎就是兩個要對齊的實作，而啟動器進了下游 git、由下游決定何時升級；漂移是必然的。薄殼可以永久凍結，引擎可以隨時升級。

**機制（可換）：** POSIX sh + `docker` + `grep`／`sed`；`gen/.stamp` 記錄薄殼對應的引擎 digest，不符就換薄殼並要求重跑。

**建立／服務它的 ADR：** ADR-0002（在 proto）、待寫 ADR-xxxx（bootstrap 薄層）。

### 7. 工具 image 純資料；引擎與工具分離

**性質：** 工具 image 是 `FROM scratch` 只放檔案的純資料，不含程式、不會被執行；引擎只有一份（`vendor_kit:vN`）。工具 repo 永遠不必因為 vendor_kit 升級而重發版；vendor_kit 升級也不必等工具重發版。

**為什麼固定：** 甲版（工具 image `FROM vendor_kit`）把升級工具的程式綁回工具本身，需要一整套協定號與相容矩陣才撐得住——這正是當初把安裝程式抽離 base 要擺脫的東西。

**機制（可換）：** `Dockerfile.dist` = `FROM scratch` + `COPY dist/`；主機 `docker create` → `docker cp` → 唯讀掛進引擎容器。

**建立／服務它的 ADR：** ADR-0002（在 proto）。

### 8. 使用者介面極少；動詞語意跟 base

**性質：** 常用三個：`add`／`upgrade`／`dev`；進階六個：`remove`／`undev`／`update`／`sync`／`install`／`uninstall`；一支薄腳本 `bootstrap.sh`（下載引擎 + 呼叫 `install`，再跑 = 修復）。全部在 `just vendor_kit` 命名空間，不佔頂層。動詞語意與 base 一致：`update` 只查不改任何檔、`upgrade` 套用（含安裝、三方合併、推 baseline）。成對動詞成對出現（`add`↔`remove`、`dev`↔`undev`、`install`↔`uninstall`）。不加 `init`／`diff`／`accept`／`rollback`／`check` 等別名——各自由既有動詞的選項或 git 接手。

**為什麼固定：** 同一批使用者在同一個 `justfile` 裡同時打 `just base …` 與 `just vendor_kit …`；兩個命名空間語意相反，比偏離生態系更糟。動詞少，每個動詞就能有完整的 `--help`、成對的反向、明確的結束狀態。

**機制（可換）：** 動詞 recipe 一行 `verb *args` 轉發、放 tracked 的 `vendor.just`；`[group('常用')]`／`[group('進階')]` 分段；`help` recipe 補命名空間層說明。

> ⚠ 待拍板：一個工具可否輸出多個 just 命名空間（base 現有 `docker`／`base`／`template`）；`.gitignore` 這類幾乎必已存在的初始檔（base 的 ignore 條目永遠進不去）只 warn 還是另立「標記區塊 append」動詞。

**建立／服務它的 ADR：** 待寫 ADR-xxxx（介面動詞）。

### 9. 驗收 = 真引擎、乾淨下游、完整流程；dev 自身與驗收用同一機制

**性質：** vendor_kit 的驗收測試用**剛 build 出來、已通過前面所有測試層**的引擎 image，在一個乾淨的下游 fixture repo 跑完整流程：`install` → `add` → `upgrade` → `dev`／`undev` → `remove` → `uninstall`，並以結束狀態與檔案系統為斷言，不 import vendor_kit。在本機開發 vendor_kit 自身（`dev vendor_kit -i <image>`）與驗收走的是同一條「用指定 image 當引擎」的路。

**為什麼固定：** 引擎在容器內、使用者只看得到 `just` 與檔案；只有黑箱驗收能證明「使用者看到的」是對的。dev 自身若另闢機制，驗收測的就不是開發者實際跑的東西。

**機制（可換）：** `version.local.toml` 的 `vendor_kit = "<本機 image tag>"` 覆寫；Docker multi-stage 測試分層（smoke → lint／unit → integration → system → acceptance）。

**建立／服務它的 ADR：** ADR-0001（測試分層，在 proto）、待寫 ADR-xxxx（dev 自身與驗收）。

### 10. 決議記 issue，定案寫 ADR，ADR 回連本檔；架構圖是測試依據

**性質：** 每個設計決議先在 issue 討論（中文）；定案後寫成 ADR，ADR 檔頭一行 `> Serves:` 回連本檔的不變量／原則／範圍項目；ADR 記機制與理由，本檔記性質。架構圖（`.drawio`）不是插圖，是測試的依據：圖上畫的模組邊界與泳道由 lint（import-linter、鏡射、黑箱）強制。

**為什麼固定：** 沒有回連的 ADR 會在幾次修改後與產品目標脫鉤；沒有被測試強制的圖，會在幾次修改後跟程式脫鉤。兩者都是靜默的。

**機制（可換）：** `doc/adr/NNNN-<slug>.md` 檔案系統即登錄；必要段落由 lint 管（見 [`doc/adr/README.md`](adr/README.md)）。

**建立／服務它的 ADR：** ADR-0001（在 proto）；本檔與 `doc/adr/README.md` 的規則本身。

## 設計原則

在不變量之下、個別決議之上。不變量是任何 ADR 不得違反的**性質**；設計原則是**判準**——兩個看起來都對的選項並存時，vendor_kit 怎麼選。原則刻意比不變量弱：一個 ADR 可以在說明理由後偏離原則，那份 ADR 就是紀錄；不變量不能被偏離。每條附「寫在哪裡」與「服務哪條不變量」。

### P1. 對齊 base 的 just 慣例；base 反過來對齊 vendor_kit 的檔案佈局

命名空間、`--option` 收窄（帶值選項皆有短選項、不用複合值 positional）、`update` 只查／`upgrade` 套用——這些借 base。反方向：檔案佈局（`.vendor_kit/`、根 `justfile` 一行 import）由 vendor_kit 定，base 遷移時對齊，所以「與 base 共存」不是 vendor_kit 要解的問題。只借慣例不抄行為：base 的 `update` 吞結束碼、`upgrade` 自己 commit，都不繼承。
*寫在哪裡：* 待寫 ADR-xxxx（介面動詞）；base ADR-00000011。*服務：* 不變量 8。

### P2. 借主機已有的，不養第三方

拉與展開交給 docker（`create`／`cp`），文字三方合併交給引擎內的 `git merge-file`，版本追蹤交給 Renovate 一條 regex。vendir、crane、Copier 都不進引擎；要進，須通過四項門檻（能展開現有 scratch image、完全服從宣告、通過私有 registry／多架構／Jetson／WSL2 驗收、確實刪掉一整塊自維護程式）。
*寫在哪裡：* 前例研究定案（待寫 ADR-xxxx，bootstrap 薄層）。*服務：* 不變量 5、6。

### P3. 每個逃生口顯式、有名字、印出它做了什麼

`-y`（免詢問）、`--no-justfile`（不碰根檔只印指示）、`VENDOR_KIT_NO_LOCK`（鎖不支援的檔案系統）、`--dry-run`（只印會動哪些檔）。取逃生口是可見的動作；沒有靜默的逃生口，也沒有「偵測到就自動放寬」。
*寫在哪裡：* 待寫 ADR-xxxx（介面動詞）、待寫 ADR-xxxx（初始檔合併）。*服務：* 不變量 1、4。

### P4. 先加後退

會破壞使用者的改動拆成兩步：新路徑先與舊路徑並存，退場是另一個可獨立排程、公告、回退的決議。升級契約（宣告格式、`init.toml` 格式、結束狀態）只加不改；動詞改名走別名期。
*寫在哪裡：* 待寫 ADR-xxxx（介面動詞）。*服務：* 不變量 4、8——下游在 vendor_kit 不決定的時間點升級，一步到位的「加+刪」是它們走不到一半的一步。

### P5. 一條規則一個擁有者

規則在引擎實作一次；啟動器、`check.sh`、工具 just 模組只轉發。兩個必須一致的實作是延遲發作的漂移。
*寫在哪裡：* ADR-0002（在 proto）§3；待寫 ADR-xxxx（bootstrap 薄層）。*服務：* 不變量 6、4。

### P6. 母體用推導，不列清單

要支援哪些初始檔類型，看工具實際用了什麼；要驗哪些平台，看下游實際跑在哪；哪些 ADR 存在，看檔案系統。手寫清單從第一個在別處新增的項目起就是錯的，而且錯得靜默。
*寫在哪裡：* 本檔「範圍」；`doc/adr/README.md`。*服務：* 不變量 4、10。

## 衝突優先序

這個順序**只用於**：兩個 vendor_kit 都持有的正當性質，在某個決議裡不能兼得，順序說誰讓步。它**不是**把「這很難做」排在任何東西之上的許可：**難做不是理由**——難度不在下列性質之中、永遠不進比較；一個難以安全實作的改動是程式碼的發現，不是一個競爭的主張。引用這個順序的決議必須點名兩個相衝的性質，並證明在此處確實不能兩全；做不到，衝突就是想像的，順序不適用。

高者勝。

**① 使用者的檔與下游跑的東西正確。** 使用者的檔只在使用者同意下改變；下游 `just` 跑到的工具內容與宣告一致。*立於不變量 1、2、5。*

**② 缺陷大聲且早。** 有錯，在第一個有人在場的時間點說出來，而不是繼續跑然後回報綠燈。*立於不變量 4。*

**③ 一個來源、一個擁有者。** 宣告一份、規則在引擎一份、其餘轉發。*立於不變量 2、6；這是 P5 作為性質而非判準。*

**④ 使用便利。** 少打幾個字、少問一次、少知道一件事。*不立於任何不變量——這是它排最後的原因，不是它不重要。*

### 實例：詢問 vs `-y`

`upgrade` 對某個已納管初始檔判定「使用者沒改、新版有變」。④ 說直接換掉——使用者沒改，換了也不會壞；① 說那是使用者的檔，vendor_kit 不能未經同意寫入。① 勝：預設**詢問**。但 ④ 沒有被丟掉，而是被給了一扇有名字的門（P3）：`-y` 免問，且仍印出改了哪些檔。CI 下沒有人回答問題：無 `-y` 時 ② 勝過 ④——以 1 結束並印出「請在本機執行 `just vendor_kit upgrade base` 後提交」，而不是 EOF 當同意、也不是靜默跳過然後綠燈。三個性質各得其所，是順序讓它成為一個決議而不是三條互相矛盾的規則。

### 第二例：`sync` 發現 baseline 落後

Renovate 的 PR 改了宣告、merge 後有人打 `just docker build`。④ 說 `sync` 順手把初始檔合併掉最省事；③ 說 tracked 寫入只能來自明確動詞（不變量 3）；② 說這個狀態要被說出來。結果：本機 warn 提示 `upgrade`、CI 以 1 結束——③ 與 ② 都在 ④ 之上，而它們彼此不衝突。

### 順序排不出時

同一階的兩個性質不由這份清單決定；不變量與任何東西的衝突也不由它決定——不變量不是可以讓步的性質，這正是它叫不變量的原因。一個決議發現自己在拿一條不變量換另一條，它發現的是不變量的缺陷，產物是本檔的修訂，不是一份挑贏家的 ADR。

## 產品形狀

- **純資料 image 散播、宣告鎖版、快取重建**（不變量 2、7）：工具 repo 推 image；專案一份宣告；內容從宣告重建，不進下游 git。
- **薄啟動器 + 容器內引擎**（不變量 5、6）：主機三個工具；規則在引擎；啟動器凍結。
- **初始檔建一次、歸使用者、三方合併升級**（不變量 1）：baseline 進 git 作合併祖先；衝突用 git 熟悉的標記解。
- **命名空間動詞、成對、跟 base**（不變量 8）：`just vendor_kit add/upgrade/dev` 是使用者需要知道的全部。
- **一份 CI 契約腳本**（不變量 3、4）：下游 CI 只呼叫 `.vendor_kit/ci/check.sh`；GitHub／GitLab 差異不進引擎。

## 路線圖

### 第一版

- 引擎子命令與九個動詞 + `bootstrap.sh`；結束狀態 0/1/2；`--dry-run`、`-y`、`--porcelain`。
- 初始檔逐檔狀態機（純文字三方合併；二進位只比對不合併；symlink 第一版禁止）；baseline + metadata。
- `.vendor_kit/` 佈局、自有 `.gitignore`、根 `justfile` 一行。
- `dev -p <dir>` 與 `dev vendor_kit -i <image>`；驗收 fixture repo 走完整流程；amd64 + arm64 原生 runner。
- Renovate regex preset；`check.sh` 給下游 CI 與工具 repo CI（`--dist`）。
- ADR-0001／0002 搬回本 repo 並補 `> Serves:`；本檔列的「待寫 ADR」全部落地。

> ⚠ 待拍板（彙整）：宣告檔名；`just` 最低版本；dist image 單架構；衝突時 baseline 是否推到新版（避免重跑再衝突）；Renovate 路徑由 PR 作者本機補合併（vs CI bot commit）；多命名空間工具；image 公開／私有；`.gitignore` 類初始檔的處理。

### v2

- `upgrade --adopt <file>`：把 `add` 時已存在、未納管的檔納入合併。
- tracked 的 `.vendor_kit/files/<repo>/`，讓 compose／GitLab CI 這類「快取不進 git 就讀不到」的引用場景可行。
- 簽章／驗簽；多 registry；範本變數渲染——各自先有下游需求證據（P6）再進範圍。
- vendir 類下載後端：只在通過 P2 的四項門檻後重評。
