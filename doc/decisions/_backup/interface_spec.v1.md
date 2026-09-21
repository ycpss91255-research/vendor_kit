# vendor_kit 介面規格（interface reference）草稿 v0.1（2026-09-19）

用途：後續每張票唯一可引用的 input／output 定義。來源優先序：`grilling.md` 最晚條目 > `proposal_v2.md` v2.4 → v2.3 → v2.2 → v2.1 → 正文 > 其他 decisions／issue。每條規格後以 <sub>[來源]</sub> 標注；`[待定]` 集中於 §9；矛盾處理於 §10。占位符：`<repo>` 工具 repo 名、`<ns>` just 命名空間、`<dir>` 目錄、`<tag>`、`<digest>`、`vX`／`vY` 引擎版本、`P` 協定整數、`<專案根>` = 含 `.vendor_kit/` 的目錄。

## 0. 共通前提（所有動詞）

| 項目 | 規格 |
|---|---|
| 專案根 | = 含 `.vendor_kit/` 的目錄（monorepo 子專案各自一套）；不是 git toplevel。<sub>[grilling Q20 定案（改）]</sub> |
| 執行位置 | vendor_kit 動詞只准在專案根執行：recipe 檢查 `invocation_directory() == justfile_directory()`，否則 1 印「請到 <dir> 執行」。工具自己的 recipe 是否擋由工具決定。<sub>[grilling Q20 修正]</sub> |
| git | 專案根須在某 git repo 內（主機側檢查）；引擎不讀 `.git`、不碰 index；不做 `git init`。禁止巢狀：install 時上層已有 `.vendor_kit/` → 1。<sub>[grilling Q20、19條-1；proposal §2 install]</sub> |
| 主機需求 | docker ≥ 19.03、just ≥ 1.33.0（GitHub release 下載版）、POSIX sh；Linux amd64／arm64、WSL2；armv7、SELinux 不支援。<sub>[grilling Q4、Q8、19條-13]</sub> |
| 不變量 | 對使用者的檔：可以建（明說建了什麼）、要改先問（`-y` 免問）、永不刪、永不覆蓋（= 不用工具版本取代客製內容；例外只有根 justfile 一行、已納管初始檔的三方合併）。自動化（sync）只碰不進 git 的東西（cache/、gen/）。never fail silently。<sub>[grilling 隔離題；proposal §1；isolation 最終建議]</sub> |
| 詢問通則 | 需詢問但無 tty／EOF 且無 `-y` → 1 印「加 -y 或在終端執行」；EOF／Ctrl-C 視為拒絕、不套用。`-y` 只省略詢問，不授權覆蓋既有未納管檔、不硬加 append 行。<sub>[grilling 19條-6、Q13；base_pitfalls 2-15；compat 條 10]</sub> |
| frozen（`CI=1`） | 不寫任何 tracked 檔、警告變失敗（薄殼不符、baseline 落後、未完成接入、任何 local 覆寫）、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/。<sub>[v2.1 A；v2.2 A]</sub> |
| 進度日誌 | add／upgrade 記 metadata `state=in-progress`；remove／uninstall 放 `.vendor_kit/.tmp.*`；任何動詞開始前有未完成 → 先恢復再繼續，失敗明列。<sub>[grilling 進度日誌條；v2.2 C]</sub> |
| 引擎環境 | `LC_ALL=C.UTF-8`、`TZ=UTC`，時間戳 UTC ISO 8601；容器以 host uid:gid 跑，HOME 指容器內暫存（實作細節）。<sub>[grilling 19條-3、-4]</sub> |
| 路徑 | 啟動器一律引號（含空白路徑）。<sub>[grilling 19條-8]</sub> |

## 1. 使用者動詞

語法：`just vendor_kit <verb> [args]`；所有動詞 recipe 一律 `verb *args` 一行轉發（`set positional-arguments` 只在 vendor.just），各動詞 `--help` 由引擎印。分組 `[group('常用')]`：add、upgrade、dev；`[group('進階')]`：其餘。<sub>[proposal §2]</sub> 不開：init、ensure、diff、accept、rollback、`--repair`、`--purge`、`--porcelain`。<sub>[proposal §2；v2.1 E]</sub>

| 動詞 | 語法 | 位置參數 | 選項（長／短／型別／預設／互斥） | 前置檢查 | 副作用（寫哪些檔，見 §4） | 詢問點（`-y`／無 tty） | 結束碼 | stdout／stderr 概要 |
|---|---|---|---|---|---|---|---|---|
| `bootstrap.sh` | `sh bootstrap.sh [--tool <repo>]… [-t <tag>] [-y] [--local <image tag 或 tar>]` | 無 | `--tool <repo>` string 可重複；`-t/--tag <tag>` string 預設最新；`-y/--yes` bool；`--local <image tag 或 tar>` string（tar 先 `docker load`）；`-h` <sub>[proposal §2；#27]</sub> | 在 git repo 內；just ≥ 1.33.0（不足印下載＋安裝指令）；專案已有 version.toml → 用該行引擎跑 install（不用內嵌，拉不到即失敗）；只有第一次接入才用內嵌引擎 ref <sub>[grilling Q8、Q18]</sub> | `docker pull` 內嵌引擎 ref → 引擎 `install` → 每個 `--tool` 呼叫 `add`；`--local` 時 version.toml 仍寫正式 ref、version.local.toml 寫 `vendor_kit = "<tag>"`；不自刪 <sub>[proposal §2；#27]</sub> | 轉發 `-y` 給 install／add；EOF 不算同意 <sub>[interface 一致]</sub> | 0；1 失敗不留半成品（只對第一次 install 成立）<sub>[proposal §2；v2.2 C]</sub> | 診斷 stderr；不用腳本的替代指令印在 release notes：`docker run --rm -it -u "$(id -u):$(id -g)" -v "$PWD:/repo" <引擎 ref> install` <sub>[#27]</sub> |
| `install` | `install [-y] [--no-justfile]` | 無；`install <repo>` 誤用 → 1 提示 `add` <sub>[codex_verbs]</sub> | `-y` bool；`--no-justfile` bool（跳過根 justfile 步驟只印指示） | 在 git repo 內（否 → 1 提示 `git init`）；上層無 `.vendor_kit/`；不被 gen/.stamp 比對擋 <sub>[proposal §2；grilling Q20；v2.3 §2]</sub> | 建 `.vendor_kit/`：version.toml（第一行引擎 ref）、entry.just、vendor.just、.gitignore、ci/check.sh、baseline/、gen/.stamp；根 justfile 無 → 建（`import '.vendor_kit/entry.just'` + `default: @just --list`）；再跑 = 用引擎重寫薄殼（先比對現內容 == 上次產物；被改過 → 1 列差異不動）；已含那行 → 不再加 <sub>[proposal §2；v2.1 E；grilling Q10、Q17]</sub> | 根 justfile 已存在 → 問「要加這一行嗎」（`-y` 直接加並印出）；根檔是 symlink → 不寫、印一次性遷移指示 <sub>[proposal §2；isolation A1(4)]</sub> | 0／1 | 印建立或修改了什麼（含加進根 justfile 的那一行） |
| `uninstall` | `uninstall [-y] [-n]` | 無 | `-y` bool；`-n/--dry-run` bool（覆蓋所有刪改與詢問） | 先預檢全部工具（hash 相符清單）；任一工具 remove 回 1 → 中止並列出已完成部分 <sub>[v2.2 E；v2.3 §6]</sub> | 逐工具 remove → 只刪確認是自產（hash 相符）的檔（version.toml、version.local.toml、薄殼、gen/、cache/、baseline/）；未知或被改的保留並回報；目錄非空則保留；不 `rm -rf`；初始檔保留並印清單 <sub>[v2.2 E；proposal §2]</sub> | 根 justfile 那行：問「要刪這一行嗎」，只刪與我們寫的完全相同的行；append 行問後只刪原文相同的 <sub>[proposal §2、§5]</sub> | 0／1 | 初始檔清單、保留檔清單 |
| `add <repo>` | `add <repo> [-t <tag>] [-s <image>] [--local <tar>] [-y] [-n]` | `<repo>` 必填 | `-t/--tag <tag>` string 預設最新；`-s/--source <image>` string（image 路徑不符 `<org>/<repo>-dist` 慣例時）；`--local <tar>` string（先 `docker load`）；`-y` bool；`-n/--dry-run` bool | 已接入且完成 → 0 無變更；`-t` 與鎖定不同 → 1 提示 upgrade；dest 撞名／越界／指向 `.vendor_kit/` → 拒絕；跨工具 `<ns>` 撞名 → 拒絕；任何寫入前檢查 <sub>[proposal §2；v2.2 E；grilling Q3]</sub> | resolve → docker → apply：cache/<repo>/、gen/<repo>.stamp、初始檔（無 → 建；有 → 不納管印「已存在，範本在 cache」）、baseline/<repo>/ + metadata（完成標記、append 行、四種狀態）、gen/tools.just 重生；version.toml 最後寫 <sub>[proposal §2、§5；v2.1 C；v2.3 §3]</sub> | `strategy="append"` 且檔已存在 → 問「要在 X 加這幾行嗎」（`-y` 免問，印出加了什麼）；copy 已存在跳過，`-y` 也不覆蓋 <sub>[grilling Q6、Q12]</sub> | 0；1（version.toml 一律未動：dest 不合法、CI 需改 tracked、指紋不同、失敗） | resolve stdout 給啟動器；人看的走 stderr；摘要列建了什麼 |
| `remove <repo>` | `remove <repo> [-y] [-n]` | `<repo>` 必填（裸跑 → 用法 + 1）<sub>[interface]</sub> | `-y` bool；`-n/--dry-run` bool | 有 dev 覆寫 → 1 提示先 `undev`；未接 = 0 + 提示；不經 docker create/cp <sub>[proposal §2；v2.3 §5]</sub> | 刪 version.toml 該行、cache/<repo>/、baseline/<repo>/、gen/<repo>.stamp、gen/tools.just 該工具所有 mod 行；初始檔永不刪，印清單；進度日誌 `.vendor_kit/.tmp.*` <sub>[proposal §2；v2.1 E；grilling 進度日誌]</sub> | append 過的行 → 問「要刪我們加的這幾行嗎」，只刪原文相同的（CRLF/LF 等價） <sub>[proposal §5；grilling Q13]</sub> | 0／1 | 初始檔清單 |
| `update [<repo>]` | `update [<repo>] [--exit-code]` | `<repo>` 可省 = 全部含 vendor_kit | `--exit-code` bool；拒絕未知參數 | 只查 registry（`tags/list` 取 SemVer 最大正式版，預發行排除），不動任何檔；不經 docker create/cp；無 registry 憑證時對需認證的工具回 1 印私有訊息（§6-3），其他工具照查再彙總；不可同時宣稱「已是最新」 <sub>[proposal §2；grilling Q11；#28]</sub> | 無 | 無 | 0 已列出；1 查詢失敗；`--exit-code` 有新版 → 2 <sub>[proposal §2；v2.1 E]</sub> | 末行固定「套用：just vendor_kit upgrade」<sub>[proposal §2]</sub> |
| `upgrade [<repo>]` | `upgrade [<repo>] [-t <tag>] [-y] [-n]` | `<repo>` 可省 = 全部含 vendor_kit 自身；`vendor_kit` 為特殊值 | `-t/--tag <tag>` string，限單一 repo；`-t` 比現版舊 → warn 仍執行；`-y` bool；`-n/--dry-run` bool | 順序：(0) metadata 衝突中檔案仍含 `<<<<<<< vendor_kit:baseline` → 2 停（檔案失蹤不算已解）；(1) 有待合併（version.toml 已 B、baseline 仍 A）→ 只補到 B 然後停，印「另有新版 vX，再跑一次 upgrade 可升」；(2) 沒有待合併才查最新（或 `-t`；frozen 不查）；無 baseline → 1 提示 add；工具在 dev 覆寫中 → 1 提示先 undev；不帶 repo 先完整預檢（含 dev 中工具）再動任何東西 <sub>[v2.2 D；v2.1 B；v2.2 B；proposal §2]</sub> | resolve → docker → apply：cache/、gen/<repo>.stamp、初始檔逐檔（§4.3 狀態機）、baseline 推到新版（有衝突仍推）+ metadata、gen/tools.just；version.toml 最後寫。自身：(a) 不帶 repo 遇引擎新版 → 舊引擎 apply 只改第一行 → 啟動器同次 pull 新引擎 → 新引擎跑 `upgrade vendor_kit`；(b) `upgrade vendor_kit` → 比對薄殼 == 上次產物 → 重產薄殼四檔 + gen/.stamp → 1；`-t <舊版>` 降版：舊引擎能無損讀現有檔才做，否則改檔前拒絕印「請 git revert」 <sub>[v2.3 §2；grilling Q19]</sub> | 逐檔：「X 換成新版？」／「你和新版都改了 X，要三方合併嗎？」／新增檔「要建 X 嗎」（拒絕 → metadata 記 declined）／append 行找到 → 問後替換、找不到 → 不動印新內容；`-y` 全免問；CI 無 `-y` 又需改檔 → 1 印清單 <sub>[proposal §5；grilling Q14、Q6]</sub> | 0；1 工具層不動 version.toml（自身升級已改第一行後回 1 是明列例外）；2 有衝突（留標記、印檔名、baseline 仍推到新版、解完重跑直到乾淨；`git merge-file` 衝突數映射為 2）；3 協定不合／版本太舊 <sub>[proposal §2；v2.3 §2；v2.2 D；grilling Q19]</sub> | `--dry-run`：印會問哪些檔、「X 沒納管，與範本差 N 行」「Y 你拒絕過，vZ 有新版」「有 N 個範本你拒絕過」、metadata 遷移明列；dest 在 CI 路徑時訊息醒目 <sub>[grilling Q14、Q15]</sub> |
| `dev <repo>` | `dev <repo> -p <dir>`／`dev vendor_kit -i <tag>` | `<repo>` 必填 | `-p/--path <dir>` string（工具必填）；`-i/--image <tag>` string（僅 `vendor_kit`，只能 tag 不能 digest）；兩者互斥 | 工具必須已在 version.toml（否 → 1）；`<dir>/dist/init.toml` 存在（缺 → 1）；CI 拒絕；不經 docker create/cp <sub>[proposal §2；v2.2 B；v2.3 §5]</sub> | 工具：version.local.toml `<repo> = "path:<dir>"`，cache/<repo>/ 改唯讀 symlink → `<dir>/dist`，gen/<repo>.stamp 第一行 `path:<dir>`。自身：version.local.toml `vendor_kit = "<tag>"` + 解析後 image ID；之後啟動器 `--pull never`；禁止用舊 image 重產 tracked 薄殼 <sub>[proposal §2；v2.2 B；grilling Q19]</sub> | 無 | 0／1 | — |
| `undev <repo>` | `undev <repo>`／`undev vendor_kit` | `<repo>` 必填 | 無 | 未啟用 = 0 + 提示 | 刪 version.local.toml 該行 → 重新 materialize 鎖定版（經 docker create/cp）；失敗 → 1 保留可恢復狀態。`undev vendor_kit`：下次 just 用 version.toml 引擎，薄殼不符 → 統一提示 <sub>[proposal §2；v2.2 B；v2.3 §5]</sub> | 無 | 0／1 | — |
| `sync [<repo>]` | `sync [<repo>]` | `<repo>` 可省 = 全部 | 無（`CI=1` 自動 frozen） | 每次 just 自動前置；引擎 ref ≠ gen/.stamp 第一行 → 1 印統一提示（§6-1），不重寫；install／upgrade vendor_kit 跳過此關 <sub>[grilling Q10；v2.3 §2]</sub> | 只寫 cache/、gen/tools.just、gen/<repo>.stamp。每工具順序：覆寫 path → 跳過 materialize/verify（仍查完成標記、baseline 落後）；cache 缺或印記第一行 ≠ 鎖定 digest → materialize；否則 verify sha256 → 失敗 → 重裝 + warn。無待辦 → 快路徑 0（不起第二個容器）<sub>[v2.3 §4；v2.2 E]</sub> | 無 | 0；1：薄殼不符、metadata 無完成標記（印「請 just vendor_kit add <repo>」）、CI 下 baseline 落後、CI 下任何 local 覆寫 <sub>[proposal §2；v2.1 A]</sub> | 本機 baseline 落後 → warn 提示 upgrade |
| `prune` | `prune` | 無 | [待定 A1] | 依 label 掃容器／image／network／volume | 刪 version.toml 未引用的舊引擎／工具 image、殘留容器、network／volume、`.vendor_kit/.tmp.*` <sub>[grilling 9 修正、9 補充]</sub> | [待定 A1] | 0／1 | 列出刪了什麼 |
| `help`／`h` | `help` | 無 | 無 | 不觸網、不安裝 | 無 | 無 | 0 | 命名空間層說明；help 明寫「已接入的專案跑 sync，不是 install」；sync 說明 =「依 version.toml 重建本機工具快取與產生的模組；不修改鎖定版本或需提交的檔案」<sub>[codex_verbs]</sub> |

## 2. 結束碼總表

| 碼 | 定義 | 動詞例外／特例 |
|---|---|---|
| 0 | 成功（含 warn）；`add` 已接入完成、`remove` 未接、`undev` 未啟用皆 0 + 提示 <sub>[proposal §2]</sub> | — |
| 1 | 一般失敗、需使用者處理／重跑；工具層動詞回 1 時 version.toml 不動 <sub>[proposal §2；compat 條 4]</sub> | 自身升級：已改 version.toml 第一行後回 1（明列例外）；`upgrade vendor_kit` 重產薄殼後回 1 要求 commit 並重跑；sync 薄殼不符回 1 <sub>[v2.3 §2]</sub> |
| 2 | 合併衝突（留 `<<<<<<< vendor_kit:baseline` 標記、印檔名、baseline 仍推到新版）<sub>[proposal §2；v2.2 D]</sub> | `update --exit-code` 有新版回 2 <sub>[v2.1 E]</sub> |
| 3 | 協定不合／版本太舊（舊薄殼跑新 major 一般動詞；`-t` 降版舊引擎無法無損讀；低於 floor）<sub>[grilling Q19；v2.4 §3]</sub> | 網路失敗不得偽裝成協定不合 <sub>[contract 3]</sub> |

舊薄殼對未知碼原樣傳出、不吞。<sub>[compat codex 原文]</sub>

## 3. 薄殼 ↔ 引擎協定

### 3.1 啟動器（POSIX sh，只用 docker pull／create／cp／run／rm + grep／sed；不解析 TOML、不 eval）<sub>[proposal §6；v2.2 C]</sub>

| 項目 | 規格 |
|---|---|
| 引擎 ref 取得 | `grep -m1 '^vendor_kit *='` 於 version.local.toml（覆寫優先）→ version.toml；找不到 → 1 明確訊息 <sub>[base_pitfalls 1-11；v2.1 B]</sub> |
| docker run 參數 | `docker run --rm -u "$(id -u):$(id -g)" -v "<專案根>:/repo" [-v "<tmp>:/dist:ro"] [-it] [--pull never] [-e …] <引擎 ref> --protocol P <子命令> …`；`-it` 只在互動（CI／`-y` 不加）；`--pull never` 只在 version.local.toml 引擎覆寫時（並驗 image ID）；dev 工具改掛 `-v "<dir>/dist:/dist/<repo>:ro"`；容器與所有資源帶 vendor_kit label；啟動器 `trap` 清容器與暫存 <sub>[proposal §6；v2.2 B、C；#27；grilling Q16、19條-5、9 補充]</sub> |
| `-e` 清單 | `VENDOR_KIT_REGISTRY_TOKEN`／`_USER`／`_TOKEN_FILE`：只在 update／upgrade 的 resolve 階段傳；`CI`：frozen 判定；`HTTP_PROXY`／`HTTPS_PROXY`／`NO_PROXY`：v2；其餘 `VENDOR_KIT_*` 轉發 [待定 B2] <sub>[#28；grilling 19條-2；contract 分歧 3]</sub> |
| 工具 image 展開 | 每工具 `docker pull`（已有則略）→ `docker create <img> /x` → `docker cp c:/dist/. <tmp>/<repo>/` → `docker rm`；不帶 `--platform`（daemon 挑原生）；不執行工具 image <sub>[proposal §6；v2.1 C；#26]</sub> |
| 兩段編排 | 動 image 的動詞 = add／upgrade／sync／undev：`resolve <verb>`（不寫檔）→ 主機 docker → `apply <verb>`。install／remove／uninstall／update／dev 不經 create/cp（單段）。`-n` = `apply --dry-run`（也要先拉 image 展開）<sub>[v2.3 §5；v2.2 C]</sub> |
| 鎖 | 鎖在引擎 version 模組（apply 一開始 flock 專案目錄，60 秒逾時失敗，印持鎖 PID 與時間）；`VENDOR_KIT_NO_LOCK=1` 跳過；啟動器不鎖 <sub>[proposal §6；v2.1 C；base_pitfalls 3-8]</sub> |
| 自身升級編排 | 啟動器讀到 resolve/apply 回報「引擎已變」→ `docker pull` 新引擎 → 用新引擎跑 `upgrade vendor_kit` → 1 <sub>[v2.3 §2]</sub> |
| pull 失敗 | 印原文 + 三分類（網路／認證／不存在）+「離線可用 `--local`」；cache 與印記相符時不 pull <sub>[base_pitfalls 2-9]</sub> |
| 逾時 | `docker pull` 逾時：預設值 + 可調參數，v1.0.0 必做 [待定 B3] <sub>[grilling 19條-14]</sub> |

### 3.2 引擎子命令與 argv

| 子命令 | argv | 說明 |
|---|---|---|
| `install`、`uninstall`、`add`、`remove`、`update`、`upgrade`、`dev`、`undev`、`sync`、`help` | `--protocol P <verb> [verb args]` | 對外動詞，argv 與 §1 相同（`*args` 原樣轉發）<sub>[proposal §6；grilling Q16]</sub> |
| `resolve <verb>` | `--protocol P resolve <verb> [verb args]` | 只讀：讀 version.toml／local、查 registry（frozen 不查）、算「要拉哪些 image@digest、待辦、輸入指紋」，stdout 回啟動器 <sub>[v2.1 C；v2.2 C]</sub> |
| `apply <verb> [--dry-run]` | `--protocol P apply <verb> [--dry-run] [verb args]` | 拿 flock → 重驗指紋（不同 → 1「請重跑」）→ 才寫；`--dry-run` 唯讀預覽 <sub>[v2.3 §6；v2.2 C]</sub> |
| `prune` | [待定 A1] | — |
| 內部（不對外） | `materialize`、`verify`、`merge` | 不列入契約 <sub>[proposal §6]</sub> |

`--protocol P`：單一整數，與 release 版號分開，從第一版就有；引擎接受 `[floor_P, current_P]` 並以呼叫方的 P 輸出行別與結束碼語意；新增 verb／旗標／行別／結束碼語意／印記第一行語意 → P+1。<sub>[grilling Q16；compat codex 2]</sub>

### 3.3 `vk-resolve/1` stdout 格式

| 項目 | 規格 |
|---|---|
| 第一行 | `vk-resolve/1`（P 提高時為 `vk-resolve/<P>`）<sub>[v2.2 C]</sub> |
| 其後 | 一行一項、固定欄位、只含安全字元；啟動器逐行讀、不 eval <sub>[v2.2 C]</sub> |
| 記錄種類 | (a) 要拉的 image：`<repo>` + `<image>@<digest>`；(b) 待辦：要重裝、要重生 gen/tools.just；(c) 輸入指紋：version.toml、metadata、要動的使用者檔 hash、鎖定 digest；(d) 「引擎已變」訊號（upgrade 不帶 repo）。欄位名、分隔符、每種記錄的順序與結尾標記 [待定 B4] <sub>[v2.2 C；v2.3 §2、§6]</sub> |
| 指紋算法 | sha256（內容指紋）；apply 重驗同一組輸入 [待定 B4 覆蓋範圍細節] <sub>[v2.3 §6]</sub> |
| stderr | 診斷（warn、錯誤、問句以外的人看訊息）一律 stderr；未知協定、輸出不完整或解析失敗 → 啟動器不得繼續 <sub>[v2.2 C；compat 條 4]</sub> |
| 對舊 P | 不得輸出呼叫方不認識的行別、不得要求其未提供的 mount／環境變數（缺少時明確拒絕）<sub>[compat codex 2]</sub> |

### 3.4 救援路徑（單段 docker run，不依賴 resolve/apply 與 gen/，永久保證）

`install`、`upgrade vendor_kit`、`sync` 的「薄殼不符 → 1 提示」判定。任何 ≥ floor 的薄殼可經此路徑叫任何引擎重產薄殼，反向（新薄殼叫舊引擎降版）亦然。<sub>[grilling Q16；compat codex 3]</sub>

## 4. 檔案 schema

通則：每個 vendor_kit 寫的 TOML 有 `schema = N` + 寫入者版本欄位；同 schema 只加不改；讀時忽略未知欄位、寫時保留；未知 key／型別錯／重複宣告 → 1；讀任一舊 schema → 直接寫當前 schema（不鏈式）；只在本來要寫該檔的明確動作寫回；引擎寫回固定格式並重讀驗證。<sub>[grilling 相容性其餘採納；base_pitfalls 1-11]</sub> 第一版 `schema = 1`。寫入者版本欄位名 [待定 C1]。

### 4.1 `.vendor_kit/version.toml`

| 項目 | 規格 |
|---|---|
| 進 git | 是；唯一來源。寫入者：install／add／upgrade／remove（apply 最後寫）；使用者、Renovate 可手改；sync 只讀。<sub>[proposal §3；drawio 目錄樹]</sub> |
| 契約 | 唯一一行符合 `^vendor_kit\s*=`（啟動器、引擎、Renovate preset 共用單一來源）；不是行號（第一行只是 install 寫出慣例）。禁止：BOM、重複鍵、`[vendor_kit]` 表旁路等 TOML 合法但 regex 讀不到／讀錯的等價寫法。<sub>[grilling 相容性其餘採納；compat 分歧]</sub> |
| 公開格式 | 工具可讀它寫來源紀錄。<sub>[grilling deploy 定案]</sub> |

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `vendor_kit` | string | 是 | 引擎 ref `ghcr.io/<org>/vendor_kit:vN@sha256:<digest>`（多架構 index digest）<sub>[proposal §3；#26]</sub> |
| `schema` | integer | 是 | 第二行；啟動器不讀、只引擎讀 <sub>[compat codex 5]</sub> |
| [待定 C1] | string | 是 | 寫入者版本 |
| `[tools].<repo>` | string | 每工具 | `ghcr.io/<org>/<repo>-dist:<tag>@sha256:<digest>`（index digest）<sub>[proposal §3]</sub> |

```toml
vendor_kit = "ghcr.io/<org>/vendor_kit:v1.0.0@sha256:<digest>"
schema = 1

[tools]
<repo> = "ghcr.io/<org>/<repo>-dist:v2.3.0@sha256:<digest>"
```

### 4.2 `.vendor_kit/version.local.toml`

不進 git（自有 .gitignore 擋）；寫入者 dev／undev；uninstall 刪；不交 Renovate；`CI=1` 有任何覆寫 → sync 回 1。啟動器先讀它再退回 version.toml。<sub>[proposal §3；v2.1 A；isolation B(b)]</sub>

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `vendor_kit` | string | 否 | 本機引擎 image tag（只能 tag，docker load 後無 RepoDigests）<sub>[proposal §2；#27]</sub> |
| 引擎 image ID 欄位 [待定 C2] | string | 有 `vendor_kit` 時 | 解析後 image ID `sha256:…`，同 tag 重 build 才會被發現 <sub>[v2.2 B]</sub> |
| `<repo>`（位置 [待定 C3]） | string | 否 | `path:<dir>`；cache/<repo>/ 為 symlink → `<dir>/dist` <sub>[proposal §2、§3]</sub> |

```toml
vendor_kit = "vendor_kit:dev"
<image_id 欄位> = "sha256:<image id>"
<repo> = "path:/home/me/<repo>"
```

### 4.3 `baseline/<repo>/.vendor_kit.toml`（metadata）

進 git；寫入者 add／upgrade；兼作 baseline/<repo>/ 空目錄佔位；apply 重驗指紋時一起比；schema 遷移由 `upgrade vendor_kit` 做並在 dry-run 明列。<sub>[proposal §3；drawio p2；grilling 相容性其餘採納]</sub> 欄位名全部 [待定 C4]（下表為語意）。

| 欄位（語意） | 型別 | 必填 | 說明 |
|---|---|---|---|
| `schema`、寫入者版本 | integer、string | 是 | 同通則 |
| 來源 ref@digest | string | 是 | 這份 baseline 來自哪個工具 image（tag@index digest）<sub>[drawio p2]</sub> |
| 最後合併版本 | string | 是 | ≠ version.toml → sync 本機 warn／CI 1；upgrade 先補待合併到該版然後停 <sub>[drawio p2；v2.2 D]</sub> |
| 完成標記 | bool | 是 | add 走完 materialize → 初始檔 → baseline 才寫；缺 → sync 1「請 add」；add 已完成 → 0 無變更 <sub>[interface；proposal §2]</sub> |
| 每個初始檔的狀態 | table | 是 | 四種：已納管（managed）／拒絕過（declined）／本來就有沒納管（unmanaged）／使用者刪了（deleted-by-user）；完成標記列每檔結果（created／skipped-exists／appended／declined）<sub>[grilling Q15；base_pitfalls 3-4]</sub> |
| append 過的行 | table | append 檔 | 每個 `strategy="append"` 檔實際插入的行原文（各工具分開記；原本就存在的相同行不認領）<sub>[grilling Q13]</sub> |
| 衝突中檔案 | array | 否 | upgrade 回 2 時留標記的檔名清單；仍含標籤 → 2 停；解完重跑才清空 <sub>[v2.2 D]</sub> |
| 進度日誌 state | string | 否 | `in-progress` + 已完成／未完成清單；第一個寫入前建立、最後一步刪除 <sub>[v2.2 C；v2.3 §6]</sub> |

upgrade 逐檔狀態機（B=baseline、D=磁碟、N=新版；只對已納管、一般文字檔、無待解衝突）：D 缺 → 維持刪除；D==N → 不動；B==N → 不動；D==B → 問後寫 N；三者皆異 → 問後 `git merge-file --diff3`（標籤 `<<<<<<< vendor_kit:baseline` 等），衝突 → 2；不論結果 baseline 推到 N。N 缺（新版刪檔）→ 不刪只 warn。二進位／symlink 不合併：未改才換、改過保留 + warn。合併後對 TOML／just 類目標重新解析，失敗 → 2 留原檔。<sub>[isolation C；proposal §5；base_pitfalls 2-12]</sub>

### 4.4 `gen/.stamp`、`gen/<repo>.stamp`、`gen/tools.just`（不進 git）

| 檔 | 寫入者 | 內容 |
|---|---|---|
| `gen/.stamp` | 只由 install／upgrade vendor_kit | 第一行 = 產生薄殼的引擎 ref（引擎覆寫時為 `<tag>`），供 sync grep 快速比對；不再承擔薄殼 hash <sub>[grilling Q17]</sub> |
| `gen/<repo>.stamp` | materialize | 第一行 = 多架構 index digest（與 version.toml 一致；dev 時 `path:<dir>` 或 `image:<tag>`）；之後每檔一行 `<sha256>  <相對路徑>`（files/…、init.toml、just/<ns>.just）；verify 逐檔比 <sub>[v2.3 §3；#26]</sub> |
| `gen/tools.just` | sync／add／remove／upgrade 重生；最後寫、與 cache 同一 apply 內原子替換 | 每個 `<ns>.just` 一行 `mod <ns> '../cache/<repo>/just/<ns>.just'`（一工具可多行），每行 mod 上方一行註解；零 set 零 recipe <sub>[v2.1 E；v2.3 §3；base_pitfalls 2-4；grilling 相容性]</sub> |

### 4.5 薄殼（進 git，vendor_kit 擁有，人不改）

| 檔 | 內容 |
|---|---|
| 自描述首行 | entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行（第一行 shebang）：`# vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 LF 正規化後的 sha256>`；引擎重算比對 + 對 image 內薄殼模板二次比對；不符 → 1 列差異不動（使用者 `git checkout` 還原後再跑）；mode 變更只 warn <sub>[grilling Q17；base_pitfalls §5 CRLF]</sub> |
| `entry.just` | `mod vendor_kit 'vendor.just'` + `import? 'gen/tools.just'`；零 set 零 recipe <sub>[proposal §2、§3]</sub> |
| `vendor.just` | 動詞 recipe 一行轉發 + sync 前置；`set positional-arguments` 只放這 <sub>[proposal §2]</sub> |
| `.gitignore` | `cache/`、`gen/`、`version.local.toml`、`.tmp.*` <sub>[proposal §3]</sub> |
| `ci/check.sh` | §7 |
| 根 justfile（使用者的） | install 只加一行 `import '.vendor_kit/entry.just'`（無檔則另加 `default: @just --list`）；uninstall 只刪完全相同行 <sub>[proposal §2]</sub> |

### 4.6 `.vendor_kit/.tmp.*`

remove／uninstall 的進度日誌（metadata 會被刪）；prune 清除；自有 .gitignore 擋。格式 [待定 C5]。<sub>[grilling 進度日誌；9 修正]</sub>

### 4.7 工具側 `dist/`、`dist/init.toml`、`Dockerfile.dist`、image

| 項目 | 規格 |
|---|---|
| `dist/` 佈局 | `dist/files/`（全部出貨，原樣展開到 cache/<repo>/files/）、`dist/init.toml`、`dist/just/<ns>.just`（每檔一個頂層命名空間，數量工具自決，`<repo>.just` 必須存在）；symlink 第一版禁止（check.sh --dist 擋、引擎展開時也驗）；文字檔一律 LF <sub>[proposal §4；v2.2 E；#29]</sub> |
| `Dockerfile.dist` | `FROM scratch` + `COPY dist/ /dist/`；純資料，不承諾可執行、vendor_kit 不檢查 binary <sub>[proposal §4；grilling Q21]</sub> |
| image 命名 | 工具 `ghcr.io/<org>/<repo>-dist:<tag>`；引擎 `ghcr.io/<org>/vendor_kit:vN`；皆多架構 amd64+arm64（同一次 buildx、COPY-only、CI 驗兩平台一致）；引擎 image 公開，工具自決（公開不可逆）；已釋出 image／index 子 digest／Release 資產／fixture 永不刪 <sub>[proposal §4；grilling Q4、Q7、相容性；base_pitfalls 2-17]</sub> |
| label | 所有 vendor_kit 建的 docker 資源（容器／image／network／volume）帶 vendor_kit label；名稱 [待定 B5]；協定 LABEL [待定 B5] <sub>[grilling 9 補充；contract 1]</sub> |
| 工具契約（初始檔） | 只能引用穩定入口 `just <ns> …`、`.vendor_kit/ci/check.sh`、`.vendor_kit/entry.just`、`.vendor_kit/version.toml`；不得寫死 cache 內部路徑；交付物執行期不得依賴 `.vendor_kit/`、version.toml、GHCR；rename／格式變更不得以 copy/append 假裝完成；工具 recipe 用 `cd "{{justfile_directory()}}"` 回專案根，禁止相對 working-directory <sub>[grilling Q14、deploy；base_pitfalls 1-4、2-13；proposal §4]</sub> |

`dist/init.toml`：

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `schema` | integer | 是 | 建置期契約（同 image 內讀寫），不進執行期矩陣 <sub>[contract 4；base_pitfalls 1-11]</sub> |
| `description`（位置 [待定 C6]） | string | 否 | gen/tools.just mod 上方註解，缺則 `<repo> vX` <sub>[base_pitfalls 2-4]</sub> |
| `[[file]].src` | string | 是 | 來源（相對基準 [待定 C6]） |
| `[[file]].dest` | string | 是 | 相對專案根；正規化、不得越出 repo、不得指向 `.vendor_kit/`；copy/copy、copy/append 同 dest 跨工具 → add 拒絕；append/append 允許（各工具行分開記，重疊或歸屬不明 → 拒絕）；引擎與 lint 都驗 <sub>[proposal §4；v2.2 E]</sub> |
| `[[file]].strategy` | string | 否 | `"copy"`（預設）或 `"append"`，只有這兩值；根 `.gitignore`／`.dockerignore`／`.editorconfig` 類必須用 append，用 copy 指向它們 → check.sh --dist 報錯 <sub>[grilling Q12、Q6]</sub> |

```toml
schema = 1

[[file]]
src = "files/Dockerfile"
dest = "Dockerfile"

[[file]]
src = "files/gitignore.snippet"
dest = ".gitignore"
strategy = "append"
```

## 5. 環境變數與參數

| 名稱 | 讀者 | 規格 |
|---|---|---|
| `VENDOR_KIT_REGISTRY_TOKEN` | 引擎 registry 模組 | registry 讀取憑證（GHCR：PAT classic `read:packages`，細節手動測後定）；只在 update／upgrade 的 resolve 階段以 `-e` 傳；不寫 log／檔、不傳給工具、dry-run 不印 <sub>[grilling Q11；#28]</sub> |
| `VENDOR_KIT_REGISTRY_USER` | 同上 | 換 token 的使用者名（GHCR 任意非空）<sub>[#28]</sub> |
| `VENDOR_KIT_REGISTRY_TOKEN_FILE` | 同上 | 從檔案讀 token（CI 掛 secret）<sub>[#28]</sub> |
| `VENDOR_KIT_NO_LOCK` | 引擎 version 模組 | `=1` 跳過 flock <sub>[proposal §6]</sub> |
| `CI` | sync／apply | `=1` → frozen（§0）<sub>[proposal §2；v2.1 A]</sub> |
| `HTTP_PROXY`／`HTTPS_PROXY`／`NO_PROXY` | resolve 階段 | v2（issue）<sub>[grilling 19條-2]</sub> |
| pull 逾時 | 啟動器 | 名稱 [待定 B3]、預設 [待定 B3]；可調 <sub>[grilling 19條-14]</sub> |
| docker label | 啟動器／prune | 名稱 [待定 B5] |
| 暫存目錄 | 啟動器 | `<tmp>`：mktemp 建立、trap EXIT/INT 刪；命名 [待定 B6] <sub>[grilling 19條-5；base_pitfalls 3-6]</sub> |
| 引擎容器內 | 引擎 | `LC_ALL=C.UTF-8`、`TZ=UTC`、`HOME=<容器內暫存>`（實作細節）<sub>[grilling 19條-3、-4]</sub> |

README 一節列出全部 `VENDOR_KIT_*` 與 `CI`，lint 擋未列者。<sub>[base_pitfalls 2-6]</sub>

## 6. 訊息文字清單（逐字；`<…>` 為占位符）

| # | 時機 | 文字 | 來源 |
|---|---|---|---|
| 6-1 | sync 發現 gen/.stamp 第一行 ≠ 引擎 ref | `vendor_kit 已更新 <vX> → <vY>，請 just vendor_kit upgrade vendor_kit`（結束 1）| <sub>[grilling Q9 統一訊息 + Q10 定案；逐字合併版 [待定 D1]]</sub> |
| 6-2 | `upgrade vendor_kit` 重產薄殼後 | `已升級引擎 <vX>→<vY> 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令`（結束 1）| <sub>[v2.3 §2]</sub> |
| 6-3 | update／upgrade 無 registry 憑證 | `無法列舉 \`<repo>\` 的版本：需要 registry 讀取權限。可設定 \`VENDOR_KIT_REGISTRY_TOKEN\`，或使用 \`upgrade <repo> -t <tag>\`（拉取使用主機 docker 認證）` | <sub>[#28]</sub> |
| 6-4 | 需詢問但無 tty／EOF 且無 `-y` | `加 -y 或在終端執行`（結束 1）| <sub>[grilling 19條-6]</sub> |
| 6-5 | CI 下 baseline 落後 version.toml；Renovate PR 需合併 | `請在本機執行 just vendor_kit upgrade <repo> -y 後 commit/push`（結束 1）| <sub>[remaining Q5；proposal §7]</sub> |
| 6-6 | dry-run／check.sh 有拒絕過的範本 | `有 <N> 個範本你拒絕過` | <sub>[grilling Q14]</sub> |
| 6-7 | dry-run／check.sh 未納管檔 | `<X> 沒納管，與範本差 <N> 行` | <sub>[grilling Q15]</sub> |
| 6-8 | dry-run／check.sh 拒絕過且新版有更新 | `<Y> 你拒絕過，<vZ> 有新版` | <sub>[grilling Q15]</sub> |
| 6-9 | 不在專案根執行 | `請到 <dir> 執行`（結束 1）| <sub>[grilling Q20 修正]</sub> |
| 6-10 | `upgrade vendor_kit -t <舊版>` 無法無損讀 | `請 git revert`（改任何檔前拒絕，結束 3）| <sub>[grilling Q19]</sub> |
| 6-11 | add 初始檔已存在（copy） | `已存在，範本在 cache 可自行比對` | <sub>[proposal §2]</sub> |
| 6-12 | apply 重驗指紋不同 | `請重跑`（結束 1）| <sub>[v2.2 C]</sub> |
| 6-13 | sync metadata 無完成標記 | `請 just vendor_kit add <repo>`（結束 1）| <sub>[proposal §2；drawio p2]</sub> |
| 6-14 | upgrade 補完待合併後另有新版 | `另有新版 <vX>，再跑一次 upgrade 可升` | <sub>[v2.2 D]</sub> |
| 6-15 | update 末行 | `套用：just vendor_kit upgrade` | <sub>[proposal §2]</sub> |
| 6-16 | install 非 git repo | 提示 `git init`（不代做；逐字 [待定 D2]）| <sub>[proposal §2]</sub> |
| 6-17 | `install <repo>` 誤用 | 導向 `add <repo>`（逐字 [待定 D2]）| <sub>[proposal §2；codex_verbs]</sub> |
| 6-18 | 薄殼／版本低於 floor | `請以 bootstrap.sh 重建`（結束 3；逐字 [待定 D2]）| <sub>[base_pitfalls 1-1；compat codex 10]</sub> |
| 6-19 | 舊引擎讀到 schema 高於本機 | `此檔由 vendor_kit <vX> 寫入，需要引擎 ≥ <vX>；請 upgrade vendor_kit 或使用 version.toml 指定的引擎`（寫入前退出；逐字 [待定 D2]）| <sub>[compat codex 7；grilling 相容性其餘採納]</sub> |
| 6-20 | 問句：根 justfile | `要加這一行嗎`／`要刪這一行嗎` | <sub>[proposal §2]</sub> |
| 6-21 | 問句：append | `要在 <X> 加這幾行嗎`／`要刪我們加的這幾行嗎` | <sub>[proposal §2、§5]</sub> |
| 6-22 | 問句：upgrade 逐檔 | `<X> 換成新版？`／`你和新版都改了 <X>，要三方合併嗎？`／`要建 <X> 嗎` | <sub>[proposal §5；grilling Q14]</sub> |
| 6-23 | bootstrap just 太舊 | 印下載＋安裝指令（逐字 [待定 D2]）| <sub>[grilling Q8]</sub> |
| 6-24 | docker pull 失敗 | 原文 + 三分類（網路／認證／不存在）+ `離線可用 --local`；認證類：`不存在或無權限（GHCR 未登入一律 denied），私有請先 docker login <host>` | <sub>[base_pitfalls 2-9；remaining Q7]</sub> |
| 6-25 | Renovate PR body（preset `prBodyNotes`） | 6-5 的指令 + `推 commit 後不要勾 rebase/retry` | <sub>[remaining Q5]</sub> |
| 6-26 | flock 逾時 | 印持鎖 PID 與時間 | <sub>[base_pitfalls 3-8]</sub> |
| 6-27 | 進度日誌恢復失敗 | `未恢復：<檔名>` | <sub>[base_pitfalls 3-7]</sub> |
| 6-28 | 薄殼被改（install／upgrade vendor_kit） | 列差異、不動（結束 1）；逐字 [待定 D2] | <sub>[grilling Q10、Q17]</sub> |
| 6-29 | upgrade 新增初始檔 dest 在 CI 路徑（`.github/workflows/`、`.gitlab-ci.yml`） | 醒目行（逐字 [待定 D2]）| <sub>[grilling Q14]</sub> |

## 7. CI 契約

### 7.1 `.vendor_kit/ci/check.sh`（下游 CI 只呼叫它；GitHub／GitLab 一樣；平台無關）

| 步驟 | 內容 | 結束碼 |
|---|---|---|
| ① | `sync`（`CI=1` frozen） | 1：薄殼不符、未完成接入、baseline 落後、任何 local 覆寫 |
| ② | verify（印記 sha256） | 1 |
| ③ | `upgrade --dry-run` | CI=1 且需改 tracked 檔 → 1 印清單（version.toml 不動）；仍有衝突標記 → 2；印 6-6～6-8 但不紅燈 |
| ④ | 工具測試 `just <repo> check`（若有） | 依工具 |
| ⑤ | 專案測試 | 依專案 |

一關過才下一關；全部通過 → 0。check.sh 整體結束碼 = 失敗步驟的碼 [待定 E1]。拒絕 version.local.toml 被 track。<sub>[proposal §7；v2.3 §7；drawio 契約⑤；base_pitfalls 2-7]</sub>

### 7.2 `check.sh --dist`（工具 repo CI）

驗：dist 佈局（files/、init.toml、just/<repo>.just 存在）、init.toml 合法（schema、strategy 只能 copy|append、dest 規則、copy 不得指向根 ignore 類檔）、無 symlink、文字檔 LF（含 CR 即失敗）、以 just 1.33.0 解析每個 `<ns>.just`（並擋比 1.33 新的功能）、image 可展開、amd64／arm64 內容一致、遷移後實際生效值。不檢查 binary 可執行性。<sub>[v2.1 E；#29；base_pitfalls 1-7、2-13；grilling Q21]</sub>

### 7.3 Renovate preset（放 vendor_kit repo，GitHub App 託管版；下游自選）

regex manager 只匹配 `.vendor_kit/version.toml`（`(?m)` 多行，key regex 與 §4.1 契約共用）+ docker datasource，同時擷取 `currentValue`（tag）與 `currentDigest`；PR 只改一行；major 分開 PR（`matchUpdateTypes`）；分組／排程範例；`hostRules` 依 host 不寫死 ghcr.io；`prBodyNotes` = 6-25；不設 `gitIgnoredAuthors`、不改 `rebaseWhen`；postUpgradeTasks 不採（文件附註）。流程：PR CI 以新版跑 §7.1 完整流程；需合併 → 1（6-5）→ 維護者在 PR 分支本機 `upgrade <repo> -y` → commit → push → CI 全部再跑 → 綠了才 merge。<sub>[grilling Q5、CI 平台定案；remaining Q5；v2.1 E；base_pitfalls 2-8；contract 更正]</sub>

### 7.4 驗收矩陣（每條一情境）

1. floor 以來每個已釋出 `bootstrap.sh(r)` + 引擎 image r 建 fixture → 第一行改為候選 C → sync（1 + 6-1、零 tracked 寫入）→ `upgrade vendor_kit`（1 + 6-2、薄殼重產）→ sync 0 → 工具 recipe → `upgrade` 全；第二次 0 無變更；禁止由候選樹複製 fixture、禁 stub 引擎。<sub>[grilling 相容性驗收 F；base_pitfalls 1-2、1-10]</sub>
2. 每個歷史版本在最低環境（docker 19.03、just 1.33.0）跑完整；其他環境（docker 上界、just latest、arm64、WSL2）按世代覆蓋；成本上限當觸發討論條件。<sub>[grilling 相容性]</sub>
3. 升級後 `.vendor_kit/` tracked 內容 == 用 C 全新 install + add（排除清單：時間戳、digest）。<sub>[grilling 19條-18]</sub>
4. 連續升級 r_i → r_j → C；固定 floor 直接跳升 C。<sub>[compat 矩陣]</sub>
5. 降版 `upgrade vendor_kit -t <舊版>`：同 schema 成功；跨 schema 改檔前拒絕 + 6-10。<sub>[grilling Q19]</sub>
6. `< floor` 太舊：唯一可用 synthetic fixture；任一動詞 → 3 + 6-18、零寫入。<sub>[compat]</sub>
7. 舊 bootstrap.sh 在已升級 repo 再跑：用 version.toml 指定引擎，不降版。<sub>[grilling Q18]</sub>
8. 舊引擎（`dev vendor_kit -i`）讀新檔：寫入前拒絕 + 6-19；不重產 tracked 薄殼。<sub>[grilling Q19]</sub>
9. 只改第一行後 `CI=1` sync（模擬 Renovate）→ 1 列薄殼不符、零 tracked 寫入。<sub>[grilling 相容性補列]</sub>
10. fresh clone 無 gen/：`just vendor_kit` 列出完整命名空間不觸網；sync 可跑；缺 stamp 不盲寫。<sub>[interface 驗收；compat]</sub>
11. 使用者改薄殼／未納管檔／append 零／多命中：不覆蓋、不刪、詢問與結束碼符合契約。<sub>[grilling 相容性補列、Q13]</sub>
12. 中斷與重跑：resolve／apply／遷移各階段故障注入；再跑保持原狀或可辨識恢復；disk-full／rename 失敗。<sub>[grilling 相容性；base_pitfalls 3-7]</sub>
13. 歷史啟動器 parser × 合法／異常 TOML（BOM、空白、重複鍵、schema 第二行、local 覆寫）。<sub>[grilling 相容性]</sub>
14. just 矩陣 1.33.0 + latest（latest 非 required）。<sub>[grilling Q8；base_pitfalls 1-7]</sub>
15. amd64 與 arm64 原生 runner 各跑完整流程（install → add → upgrade → dev/undev → remove → uninstall）；兩平台 image 內容一致。<sub>[#26]</sub>
16. 離線包：無法連 GHCR 的機器用 `local_bootstrap.sh` 完成 install → add → sync，amd64／arm64 各一次。<sub>[#27]</sub>
17. 私有工具：`add -t` 可拉；`update` 無 token → 1 + 6-3 逐字；錯 token → 1；對 token → 列出；TOKEN_FILE；所有輸出與 metadata／log grep 不到 token。<sub>[#28]</sub>
18. append：LF／CRLF／混合檔各跑 add → upgrade → remove；Markdown 尾端兩空格不得視為相同。<sub>[#29]</sub>
19. `dev -p "含 空白/路徑"`、含 `$` 的 repo 路徑；`just vendor_kit add --help` 到引擎。<sub>[grilling 19條-8；interface]</sub>
20. git worktree（`.git` 是檔）；submodule（派子代理實測後定）。<sub>[grilling 19條-1、-10]</sub>
21. rootless docker（setup-docker-action `rootless: true`）與 Podman（Ubuntu 24.04 runner 內建）；uid 12345 無 passwd 項。<sub>[grilling 12 修正；base_pitfalls 3-10]</sub>
22. prune：完整流程前後 `docker network/volume ls` 差集為空；故意留一個帶 label 的 network／volume，prune 後必須消失。<sub>[grilling 9 修正、9 補充]</sub>
23. Renovate：實際 repo 驗證人工 commit 後 Renovate 不再動該分支。<sub>[remaining Q5]</sub>
24. 驗收動詞集合由 vendor.just 實際列出推導（含 help、參數轉發、失敗碼）；刪掉受測物必紅。<sub>[base_pitfalls 2-18、1-10]</sub>

## 8. 相容性契約條文（12 條）

1. **公開介面集合**：`vendor_kit` 命名空間內 recipe 名與 argv、結束碼 0/1/2/3、薄殼→引擎 docker run 呼叫方式（子命令、mount、`-u`、`--protocol`）、`vk-resolve/<P>` 文法、§4 各檔格式、根 justfile 那一行、救援動詞 `install`／`upgrade vendor_kit` 名稱與 argv 皆列入契約；主機依賴不得新增（docker ≥ 19.03、git、just ≥ 1.33.0、sh）。<sub>[compat 條 1；grilling Q8]</sub>
2. **協定 P**：單一整數、與 release 版號分開；薄殼每次呼叫附 `--protocol P`（第一版起）；引擎接受 `[floor_P, current_P]` 並以呼叫方 P 回應；新增 verb／旗標／行別／結束碼語意／印記第一行語意 → P+1。<sub>[grilling Q16]</sub>
3. **floor**：固定 release 常數（第一個正式版 v1.0.0、P=1、schema=1）寫在契約，只能經 ADR 提高；低於 floor → 3 + 6-18。<sub>[grilling Q16、Q19]</sub>
4. **永久義務**：任何 ≥ floor 的舊薄殼可呼叫新引擎的救援路徑（§3.4）並得正確提示；舊資料永遠可讀、可遷（讀任一舊 schema → 直接寫當前 schema，不鏈式）。<sub>[grilling Q16]</sub>
5. **非永久義務**：舊薄殼跑新 major 的一般動詞只保證乾淨回 3 提示先 `upgrade vendor_kit`；同 major 內保留所有已承諾薄殼的一般呼叫能力。<sub>[v2.4 §3；grilling Q19]</sub>
6. **薄殼自描述**：§4.5 首行；未被改過以重算 hash + image 內模板二次比對判定，不依賴 gen/；不符 → 1 列差異不動。<sub>[grilling Q17]</sub>
7. **檔案 schema**：每檔 `schema = N` + 寫入者版本；同 schema 只加不改；讀忽略未知欄位、寫保留（不能保留則拒絕）；schema 高於本機 → 任何寫入前退出 + 6-19；version.toml 契約 = 唯一符合 `^vendor_kit\s*=` 的行（禁 BOM／重複鍵／表旁路）。<sub>[grilling 相容性其餘採納]</sub>
8. **新讀舊與遷移**：新引擎在記憶體轉換，只在本來要寫該檔的明確動作寫回；metadata 遷移由 `upgrade vendor_kit` 做並在 dry-run 明列；缺失且無法可靠還原的所有權資訊不得猜，停下報告。<sub>[grilling 相容性其餘採納；compat 條 6]</sub>
9. **讀先出貨、寫延後**：同 major 內 N-1 必能讀 N 寫的檔；tools.just 最後寫且與 cache 同一 apply 內原子替換。<sub>[grilling 相容性其餘採納]</sub>
10. **bootstrap.sh 與降版**：已有 version.toml → 用該行引擎跑 install，拉不到即失敗、不得退回內嵌；`upgrade vendor_kit -t <舊版>` 只在舊引擎能無損讀現有檔時成功，否則改檔前拒絕 + 6-10；`dev vendor_kit -i <舊 image>` 禁止重產 tracked 薄殼。<sub>[grilling Q18、Q19]</sub>
11. **使用者檔與失敗恢復**：§0 不變量；`-y` 不授權覆蓋；遷移與升降版先做可行性檢查，失敗不留無法辨識的混合狀態；衝突（2）與自身升級要求重跑（1）是獨立狀態。<sub>[compat 條 10；v2.2 C]</sub>
12. **發行與驗收**：已釋出 GHCR image（含 index 子 digest）、Release 資產、fixture 永不刪；SemVer：major = 提高 floor 或需手動步驟；Renovate preset 建議 major 分開 PR；驗收 §7.4 條 1–13 缺任一不得出貨；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」。<sub>[grilling 相容性其餘採納、Q11；base_pitfalls 2-17]</sub>

## 9. [待定] 清單

| 編號 | 項目 | 建議值 |
|---|---|---|
| A1 | `prune` 的選項、詢問點、引擎 argv | `prune [-n/--dry-run] [-y]`；列出將刪清單後問「要刪嗎」，`-y` 免問；單段 `docker run <引擎> prune`（需掛 docker socket 或由啟動器執行 docker 指令 — 後者較符合「引擎不碰主機 docker」）|
| B1 | bootstrap.sh 本機 image 參數名（grilling 列 `--image`／`--image-tar` 待確認，proposal／#27 已用 `--local`） | 維持 `--local <tag 或 tar>`（一個旗標、依副檔名／存在性判斷） |
| B2 | 啟動器是否轉發其餘 `VENDOR_KIT_*` 環境變數；`CI` 轉發方式 | 只轉發 `CI` 與 #28 三個；其餘不轉發（contract：環境變數不是相容策略支柱） |
| B3 | pull 逾時參數名與預設 | `VENDOR_KIT_PULL_TIMEOUT`（秒），預設 300 |
| B4 | `vk-resolve/1` 記錄欄位名、分隔符、順序、結尾標記、指紋覆蓋範圍 | 每行 `<kind>\t<k>=<v>…`，kind ∈ {pull, todo, fingerprint, engine-changed}，以 `end` 行結尾；欄位值限 `[A-Za-z0-9._:/@=+-]` |
| B5 | docker label 名；協定 LABEL 名 | `io.vendor_kit.project=<專案根絕對路徑>` + `io.vendor_kit=1`；協定 `io.vendor_kit.protocol=<P>`（contract.md 草案） |
| B6 | 暫存目錄命名 | `mktemp -d "${TMPDIR:-/tmp}/vendor_kit.XXXXXX"` |
| B7 | 容器工作目錄與 `--protocol` 在 argv 的位置 | `-w /repo`；`--protocol P` 置於子命令之前（全域旗標） |
| C1 | 寫入者版本欄位名 | `min_reader = "v1.0.0"`（grilling 用語） |
| C2 | version.local.toml 引擎 image ID 欄位名 | `vendor_kit_image_id`（drawio p2 草案） |
| C3 | version.local.toml 工具覆寫的位置（頂層或 `[tools]`） | 與 version.toml 同結構，放 `[tools]` |
| C4 | metadata 全部欄位名 | `source`、`last_merged`、`complete`、`[files.<dest>] state/result`、`[appended.<dest>] lines`、`conflicts`、`[progress] state/done/pending` |
| C5 | `.vendor_kit/.tmp.*` 格式與命名 | `.tmp.<verb>.<repo>.toml`，欄位同 metadata 進度日誌 |
| C6 | init.toml `description` 位置；`src` 相對基準 | 頂層 `description`；`src` 相對 `dist/` |
| D1 | 6-1 逐字（Q9 與 Q10 兩句合併） | 如 §6 所列 |
| D2 | 6-16、6-17、6-18、6-19、6-23、6-28、6-29 逐字 | 實作票定，須含可直接複製的指令 |
| E1 | check.sh 整體結束碼規則 | 回傳第一個失敗步驟的碼；③ 有衝突標記回 2 |
| E2 | Renovate preset 檔名與路徑 | `renovate/default.json`，下游 `extends: ["github>ycpss91255-research/vendor_kit"]` |
| F1 | `sync` 自動前置的觸發機制（工具 recipe 如何呼叫；兄弟模組不能互相依賴） | 由 gen/tools.just 每個 mod 之前的 recipe 依賴或 vendor.just 內 `_sync` 前置；實作票以 just 1.33.0 實測定 |
| F2 | 6-1 訊息在 `undev vendor_kit` 後的路徑（v2.1 B 說「重寫並統一提示」、Q10 說 sync 不重寫） | 依 Q10：只提示，不重寫 |
| F3 | submodule 支援與否 | 待子代理實測 |
| F4 | `just <ns>` 撞 `vendor_kit` 保留名／使用者根檔既有 recipe 的預檢工具（`--summary`／`--dump`） | 採 base_pitfalls 1-6（ADR 層） |

共 22 條。

## 10. 矛盾處理

| # | 衝突 | 取捨（依優先序） |
|---|---|---|
| 1 | 舊薄殼跑新 major 一般動詞：grilling Q16 回 1 vs v2.4 §3／grilling Q19 回 3 | Q19 較晚且新增碼 3 → 回 3（§2、§8-5） |
| 2 | gen/.stamp 內容：v2.3 §3「引擎 ref + 薄殼各檔 hash」vs grilling Q17「只記引擎 ref」 | Q17 → 只記引擎 ref；hash 移到薄殼首行（§4.4、§4.5） |
| 3 | sync 發現薄殼不符：v2.1 A「本機可重寫」vs grilling Q10「只回 1 提示」 | Q10 → 只提示（§1 sync） |
| 4 | 薄殼被改：isolation「warn 再覆蓋」vs grilling Q10／Q17「1 列差異不動」 | grilling → 1 不動 |
| 5 | 衝突時 baseline：interface.md「不推」vs proposal §5／isolation「推到新版」 | proposal → 推到新版（§4.3） |
| 6 | init.toml required／optional：remaining Q6 建議 vs grilling Q6 定案「不需要」 | grilling → 無此欄位 |
| 7 | uninstall：proposal §2「刪 .vendor_kit/ 全部」vs v2.2 E「不 rm -rf，只刪 hash 相符」 | v2.2 → 只刪自產（§1 uninstall） |
| 8 | 專案根：base_pitfalls 1-15／§6-4「$PWD == toplevel、一 repo 一個」vs grilling Q20 定案（改）monorepo 子專案 | grilling → 含 `.vendor_kit/` 的目錄（§0） |
| 9 | dist binary：base_pitfalls 3-5「check.sh --dist 拒絕 ELF」vs grilling Q21「vendor_kit 不檢查 binary」 | grilling → 不檢查（§7.2） |
| 10 | 自身升級訊息：grilling Q9「請再跑一次剛才的指令」vs Q10「提示 upgrade vendor_kit」vs v2.3 §2「請 commit 並再跑原指令」 | sync 路徑用 Q10（6-1）；`upgrade vendor_kit` 完成用 v2.3（6-2）；Q9 句留給 6-1 的前半 |
| 11 | local 覆寫檔名：base_pitfalls 2-7「version.toml.local」vs grilling／proposal「version.local.toml」 | grilling → `version.local.toml` |
| 12 | bootstrap.sh 第二次跑：interface.md「拒絕 + 提示 add」vs grilling「再跑 = install 修復」＋ Q18 | grilling → 呼叫 install（用既有 version.toml 引擎） |
| 13 | 引擎覆寫記錄：proposal §2「只記 tag」vs v2.2 B「tag + image ID」 | v2.2 → 兩者（§4.2） |
| 14 | 進度日誌：v2.2 C「metadata 進度日誌」vs grilling「remove/uninstall 放 .tmp.*」 | grilling → add/upgrade 用 metadata、remove/uninstall 用 .tmp.*（§0） |
| 15 | Renovate 觸發：remaining「baseline 落後 CI 只警告不紅（notes #15 D）」vs grilling Q5「需合併 → 1 印指令」 | grilling → CI 下 1（§1 sync、§7.1） |
| 16 | pull 逾時：base_pitfalls §5「列 v2」vs grilling 19條-14「v1.0.0 必做」 | grilling → v1.0.0（§3.1） |
| 17 | proxy：base_pitfalls §5「第一版要定 -e HTTP_PROXY」vs grilling 19條-2「issue v2」 | grilling → v2（§5） |
| 18 | rootless／Podman：base_pitfalls §5「明寫未驗證」vs grilling 12 修正「進驗收矩陣」 | grilling → 進矩陣（§7.4-21） |
| 19 | upgrade 的自身升級接手：v2.1 D「apply 改第一行 → 重寫薄殼+gen → 停」vs v2.3 §2「舊引擎只改第一行 → 啟動器 pull 新引擎跑 upgrade vendor_kit」 | v2.3（§1 upgrade） |
| 20 | dry-run 範圍：v2.1 C「resolve 到此為止」vs v2.2 C「也要拉 image，apply --dry-run」 | v2.2（§3.1） |

共 20 條。
