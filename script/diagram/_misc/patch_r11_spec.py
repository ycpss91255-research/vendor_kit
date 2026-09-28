P = "decisions/_legacy/interface_spec.md"; s = open(P, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (c, old[:70])
    s = s.replace(old, new)

# ---- 文首 ----
rep('# vendor_kit 介面規格（interface reference）v3（2026-09-20；併入 proposal_v2 v2.10–v2.12、grilling「2026-09-20 第八～九輪審查後定案」、r9 規格層矛盾，改動見 §10 #58–#95）',
    '# vendor_kit 介面規格（interface reference）v3.1（2026-09-20；v3 併入 proposal_v2 v2.10–v2.12、grilling「2026-09-20 第八～九輪審查後定案」、r9 規格層矛盾，改動見 §10 #58–#95；**v3.1 併入 v2.13（§9.1 P4–P13 結案）與 v2.14（第十輪後圖面落實與小定案），改動見 §10 #96–#115**）')
rep('前版存於 `interface_spec.v1.md`（v2 初稿）、`interface_spec.v2.md`（v2.7 併入前）、`interface_spec.v2.final.md`（v2 定稿 = v2.7 併入後、v3 併入前）。',
    '前版存於 `interface_spec.v1.md`（v2 初稿）、`interface_spec.v2.md`（v2.7 併入前）、`interface_spec.v2.final.md`（v2 定稿 = v2.7 併入後、v3 併入前）、`interface_spec.v3.0.md`（v3 = v2.13／v2.14 併入前）。')
rep('0. 本次（v3）新併入：', '0. v3.1 新併入：`proposal_v2.md` **v2.14 → v2.13**（v2.13 = 主對話依既定原則對 §9.1 P4–P13 的取捨，使用者可否決；v2.14 = 第十輪後圖面落實與兩個小定案）。\n0′. v3 併入：')

# ---- §0 ----
rep('add／`upgrade <repo>` 記 metadata `[progress]`；install（修復型）／remove／uninstall／undev／prune／`upgrade vendor_kit`（含不帶 repo 時 E(a) 的自身那段）放 `.vendor_kit/.tmp.<verb>.<id>.toml`',
    'add／`upgrade <repo>` 記 metadata `[progress]`；install（**第一次也建**，該日誌同時是「不留半成品」的清除清單，成功後刪；v2.13 P5）／remove／uninstall／undev／prune／`upgrade vendor_kit`（含不帶 repo 時 E(a) 的自身那段）放 `.vendor_kit/.tmp.<verb>.<id>.toml`')
rep('`trace_id` 同時是進度日誌交易 id。凡印到 tty 的訊息一律同句進 `body`。bootstrap.sh 自身那段：§9.1 P4。<sub>[v2.11-3；v2.12 L1–L5]</sub> |',
    '`trace_id` 同時是進度日誌交易 id。凡印到 tty 的訊息一律同句進 `body`。bootstrap.sh 就是第一次接入的啟動器：先 `mkdir -p .vendor_kit/log/bootstrap/` → trace_id → `launcher_start`，之後才 pull／install（§1.2 bootstrap.sh）。<sub>[v2.11-3；v2.12 L1–L5；v2.13 P4]</sub> |')
rep('CI 靜態擋原始碼中未註冊的事件名。檔案在薄殼／引擎 image 內的落點：§9.1 P9。<sub>[v2.12 L5、L6；agy_summary2「事件名註冊表前例」]</sub> |',
    'CI 靜態擋原始碼中未註冊的事件名。落點：真本 `log-events.txt` 在引擎 image；啟動器端薄殼 `log.sh` 內嵌一份啟動器事件白名單（`case`），release CI 驗「內嵌清單 ⊆ 真本」；未註冊事件 = 程式錯誤 → FATAL 結束 1（§4.10）。<sub>[v2.12 L5、L6；agy_summary2「事件名註冊表前例」；v2.13 P9]</sub> |')
rep('回 3 時**零寫入**（操作紀錄檔除外：`launcher_start`／`engine_start` 在判定前已寫，§4.10；§9.1 P12）',
    '回 3 時**零寫入**（「零寫入」= 不寫任何專案檔，操作紀錄檔例外：`launcher_start`／`engine_start` 已寫屬預期，§4.10；v2.13 P12 已定）')

# ---- §1.2 通則 ----
rep('通則（每個動詞，含 help；bootstrap.sh 自身那段見 §9.1 P4）：啟動器最先建操作紀錄檔並寫 `launcher_start`（失敗 → 1 + 6-38、零寫入），**再**做下表的前置檢查；引擎子命令啟動時 append `engine_start`（失敗 → 1 + 6-38、不進 resolve）；結束前 `launcher_exit`／`engine_exit` 記結束碼與耗時（§4.10）。下表不逐格重複。<sub>[v2.12 L4]</sub>',
    '通則（每個動詞，含 help 與 bootstrap.sh —— 它就是第一次接入的啟動器，v2.13 P4）：啟動器最先建操作紀錄檔並寫 `launcher_start`（失敗 → 1 + 6-38、零寫入），**再**做下表的前置檢查；**每個**引擎子命令（resolve 容器、apply 容器、單段各一）啟動時先 append `engine_start`（失敗 → 1 + 6-38、不做任何動作）、結束寫 `engine_exit`；啟動器結束前 `log_prune`、`launcher_exit` 記結束碼與耗時（§4.10）。下表不逐格重複；圖面表現法：每頁 resolve 段與 apply 段各一格 `engine_start`、頁尾一格 `launcher_exit`／`log_prune`。<sub>[v2.12 L4；v2.14-2]</sub>')
# ---- §1.2 bootstrap.sh ----
rep('| 無 | 在 git repo 內（否 → 1 + 6-16）；just ≥ 1.33.0（不足 → 1 + 6-23）；專案已有 version.toml → 用該行引擎跑 install',
    '| 無 | **順序**：驗 git repo／just（下列）→ `mkdir -p .vendor_kit/log/bootstrap/`（含目錄內 `.gitignore`）→ 產 trace_id → 寫 `launcher_start`（失敗 → 1 + 6-38）→ 之後才 pull／install（v2.13 P4）。在 git repo 內（否 → 1 + 6-16）；just ≥ 1.33.0（不足 → 1 + 6-23）；專案已有 version.toml → 用該行引擎跑 install')
rep('`docker image inspect` 本機有則不 pull，否則 `docker pull` 引擎 ref → 引擎 `install` → 逐 `-t` **依序**呼叫 `add <repo>[@<tag>]`，**任一 add 回非 0 → 立即中止**、不處理後續 `-t`、整體回 1 並列出已完成／未處理的工具（已完成的 add 保留；「不留半成品」只對第一次 install 成立）；',
    '`docker image inspect` 本機有則不 pull，否則 `docker pull` 引擎 ref（拉不到 → 1 + 6-24／逾時 6-31，**失敗出口**、不退回內嵌；tag 形 `--local` 的 `docker image inspect` 本機無此 image 亦為失敗出口；v2.14-5）→ 引擎 `install`（失敗 → 1：依 `.tmp.install.<id>.toml` 清半成品，**`.vendor_kit/log/` 保留**，訊息明說「已清除半成品，紀錄在 .vendor_kit/log/bootstrap/<檔>」；v2.13 P4、P5）→ 逐 `-t` **依序**呼叫 `add <repo>[@<tag>]`，**任一 add 回非 0 → 立即中止**、不處理後續 `-t`、整體回 1 並列出已完成／未處理的工具（已完成的 add 保留；「不留半成品」只對第一次 install 成立）；')
# ---- §1.2 install ----
rep('gen/.stamp、**log/**（含目錄內 `.gitignore`；§4.10，第一次 install 的建立時機見 §9.1 P4）；根 justfile 無 → 建',
    'gen/.stamp；**log/**（含目錄內 `.gitignore`）由**啟動器**在寫 `launcher_start` 前建（第一次接入 = bootstrap.sh 建 `log/bootstrap/`；§4.10、v2.13 P4），引擎不建；根 justfile 無 → 建')
rep('再跑 = 用引擎重寫薄殼（hash 相符才重寫），修復型先建 `.tmp.install.<id>.toml`（§4.6）<sub>[proposal §2；v2.1 E；grilling Q10、Q17、Q22 補；review 必修 1；v2.9-8；v2.12 L1、L3′]</su',
    '再跑 = 用引擎重寫薄殼（hash 相符才重寫）；**第一次與修復型都**在第一個寫入前建 `.tmp.install.<id>.toml`（統一規則、無例外；第一次時它同時是「不留半成品」的清除清單，失敗依它移除已寫的檔、`log/` 保留，成功後刪；§4.6、v2.13 P5）<sub>[proposal §2；v2.1 E；grilling Q10、Q17、Q22 補；review 必修 1；v2.9-8；v2.12 L1、L3′；v2.13 P4、P5]</su')
# ---- §1.2 uninstall ----
rep('初始檔保留並印清單；config.toml（三方合併初始檔）與 log/（uninstall 自身仍在寫）是否刪除：§9.1 P6；進度日誌 `.tmp.uninstall.<id>.toml`（根 justfile 那行之後才刪日誌）<sub>[v2.2 E；v2.5-3、-10；proposal §2；v2.12]</sub>',
    '初始檔保留並印清單；**config.toml** 比照初始檔保護模式：hash == `baseline/vendor_kit/config.toml` 副本 → 刪，被使用者改過 → 留下並列出（永不刪使用者改過的檔）；**`log/` 一律保留**（uninstall 自己也在寫）、不 rmdir `log/`，`.vendor_kit/` 因此保留（只剩 `log/`），結束訊息說明 `.vendor_kit/log/` 留存、可手動刪；進度日誌 `.tmp.uninstall.<id>.toml`（根 justfile 那行之後才刪日誌）<sub>[v2.2 E；v2.5-3、-10；proposal §2；v2.12；v2.13 P6；v2.14-6]</sub>')
# ---- §1.2 upgrade (b) 五檔 ----
rep('→ 新引擎重產薄殼四檔 + gen/.stamp、config.toml 缺則建／有則三方合併（§4.9）→ 新引擎刪日誌 → **1 + 6-2**',
    '→ 新引擎重產薄殼五檔（含 log.sh）+ gen/.stamp → **config.toml 缺則建／有則三方合併（6-22 問；B = `baseline/vendor_kit/config.toml`；§4.9）** → 新引擎刪日誌 → **1 + 6-2**（E(c)(2) 圖須有此格與檔案框；v2.14-7）')
# ---- §1.2 sync ----
rep('引擎 ref ≠ gen/.stamp 第一行 → 1 + 6-1，不重寫；install／upgrade vendor_kit 跳過此關；未完成交易 → 6-33 結束 1、不恢復 <sub>[grilling Q10、Q22；v2.3 §2；review 必修 9；v2.10-6]</sub>',
    '引擎 ref ≠ gen/.stamp 第一行 → 1 + 6-1，不重寫；install／upgrade vendor_kit 跳過此關；`resolve sync` 一開始偵測未完成交易 → 印 6-33 結束 1、不恢復（與 update 同一菱形；快路徑只把「無 `.tmp.*`」當起引擎條件）；工具 image `docker pull` 失敗 → 1 + 6-24／6-31 失敗出口 <sub>[grilling Q10、Q22；v2.3 §2；review 必修 9；v2.10-6；v2.14-4、-5]</sub>')
# ---- §2c 矩陣 ----
rep('| 動詞 | version.toml | config.toml | 薄殼四檔 + gen/.stamp |', '| 動詞 | version.toml | config.toml | 薄殼五檔 + gen/.stamp |')
rep('`--local`（tar 或 tag 形）：install 成功後寫 `vendor_kit` + `vendor_kit_image_id`、失敗清除 | 經 add | 經 install／add | 經 install／add | §9.1 P4 |',
    '`--local`（tar 或 tag 形）：install 成功後寫 `vendor_kit` + `vendor_kit_image_id`、失敗清除 | 經 add | 經 install／add | 經 install／add | 經 install（`.tmp.install.<id>.toml`；失敗依它清半成品） | 寫 `log/bootstrap/`（自己建目錄、寫 `launcher_start`；失敗仍保留） |')
rep('根 justfile 建或問後加一行；根 .dockerignore 建或問後 append 四行 | §9.1 P5 | 寫 |', '根 justfile 建或問後加一行；根 .dockerignore 建或問後 append 四行 | `.tmp.install.<id>.toml`（兼不留半成品的清除清單） | 寫（目錄由啟動器建） |')
rep('| `uninstall` | 刪（hash 相符） | §9.1 P6 | 刪（hash 相符） | 刪自產 | 刪 | 刪自產 | 問後逐行刪原文相同行；初始檔保留 | `.tmp.uninstall.<id>.toml` | 寫（§9.1 P6） |',
    '| `uninstall` | 刪（hash 相符） | hash == baseline 副本 → 刪；被改 → 留並列出 | 刪（hash 相符） | 刪自產 | 刪 | 刪自產 | 問後逐行刪原文相同行；初始檔保留 | `.tmp.uninstall.<id>.toml` | 寫；一律保留（不 rmdir） |')

# ---- §3.1 ----
rep('`mktemp`、`rm`、`sleep`、`od`、`tr`（後兩者只用於產 trace_id，§4.10）、`git rev-parse`、',
    '`mktemp`、`mkdir`、`date`、`rm`、`sleep`、`od`、`tr`（`mkdir`／`date`／`od`／`tr` 只用於操作紀錄檔：建 `log/<verb>/`、時間戳、trace_id，§4.10）、`git rev-parse`、')
rep('lint 擋清單外的命令。操作紀錄檔還需要的 `mkdir`、`date`（及 `date` 的微秒精度）未在清單：§9.1 P7 <sub>[review 必修 12；grilling Q24；v2.12 L5]</sub>',
    'lint 擋清單外的命令。啟動器 timestamp：試 `date -u +%Y-%m-%dT%H:%M:%S.%NZ`，輸出含字面 `N`（busybox）→ 退回秒級（`.000000Z` 補零）；引擎一律微秒 <sub>[review 必修 12；grilling Q24；v2.12 L5；v2.13 P7]</sub>')
rep('[-e CI] [-e VENDOR_KIT_NO_LOCK] -e TRACEPARENT [-e VENDOR_KIT_REGISTRY_TOKEN -e VENDOR_KIT_REGISTRY_USER] [-it]',
    '[-e CI] [-e VENDOR_KIT_NO_LOCK] -e TRACEPARENT=<…> -e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔> [-e VENDOR_KIT_REGISTRY_TOKEN -e VENDOR_KIT_REGISTRY_USER] [-it]')
rep('| `-e` 白名單 | 轉發：`CI`（照原值）、`VENDOR_KIT_NO_LOCK`、`TRACEPARENT`（每次呼叫，啟動器自產，§4.10、§5）；',
    '| `-e` 白名單 | 轉發：`CI`（照原值）、`VENDOR_KIT_NO_LOCK`、`TRACEPARENT` 與 `VENDOR_KIT_LOG_FILE`（每次呼叫，啟動器自產、必傳；容器內路徑 `/repo/.vendor_kit/log/<verb>/<檔>`，§4.10、§5；v2.13 P8）；')
rep('→ 產 trace_id → `mkdir -p .vendor_kit/log/<verb>/` → 建 `<UTC-ts>-<id8>.jsonl` 並寫 `launcher_start`（完整原始 argv）；任一步失敗 → 1 + 6-38、零寫入。',
    '→ 產 trace_id → `mkdir -p .vendor_kit/log/<verb>/`（第一次建 `log/` 時一起建目錄內 `.gitignore`）→ 建 `<UTC-ts>-<id8>.jsonl` 並寫 `launcher_start`（完整原始 argv）；任一步失敗 → 1 + 6-38、零寫入。')
# ---- §3.2 ----
rep('每個子命令啟動時先 append `engine_start`（記收到的 argv、component=engine）到啟動器建的同一操作紀錄檔，失敗 → 1 + 6-38、不做任何動作（含 resolve）；結束前 append `engine_exit`（exit_code、message_id、duration_ms、summary）。引擎定位該檔的方式：§9.1 P8。<sub>[v2.12 L4、L5、L6]</sub>',
    '**每個**子命令（resolve 容器、apply 容器、單段各自）啟動時先 append `engine_start`（記收到的 argv、component=engine）到啟動器建的同一操作紀錄檔，失敗 → 1 + 6-38、不做任何動作（含 resolve）；結束前 append `engine_exit`（exit_code、message_id、duration_ms、summary）。引擎以 `-e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔>` 定位該檔（與 `TRACEPARENT` 並用；§3.1、§5）。<sub>[v2.12 L4、L5、L6；v2.13 P8；v2.14-2]</sub>')
# ---- §4.4 ----
rep('第一行 = 產生薄殼的引擎 ref（local 覆寫時為 `<tag>`），供 sync grep 快速比對；不承擔薄殼 hash；fresh clone 缺此檔時相容判定改用薄殼自描述首行 <sub>[grilling Q17；review I-15]</sub>',
    '第一行 = 產生薄殼的引擎 ref（local 覆寫時為 `<tag>`），供 sync grep 快速比對；**不承擔薄殼 hash**（含 log.sh：其 hash 在自身自描述首行；第十版「gen/.stamp 記 log.sh hash」畫法撤回）；fresh clone 缺此檔時相容判定改用薄殼自描述首行 <sub>[grilling Q17；review I-15；v2.14-1]</sub>')
# ---- §4.5 ----
rep('| 自描述首行 | entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行（第一行 shebang）：',
    '| 自描述首行 | entry.just／vendor.just／log.sh／.gitignore 第一行、ci/check.sh 第二行（第一行 shebang）：')
rep('| `.gitignore` | `cache/`、`gen/`、`version.local.toml`、`.tmp.*`、`log/` <sub>[proposal §3；grilling Q22；v2.12 L1]</sub> |',
    '| `.gitignore` | `cache/`、`gen/`、`version.local.toml`、`.tmp.*`、`log/` <sub>[proposal §3；grilling Q22；v2.12 L1]</sub> |\n| `log.sh` | 啟動器 log 函式（自 base `dist/script/docker/lib/log.sh` 移植成 POSIX sh，§4.10）；內嵌啟動器事件白名單（`case`）；由引擎 launcher-gen 重產（install／upgrade vendor_kit），**帶自描述首行 `# vendor_kit-shell/<P> engine=<vX> sha256=…`**，hash 不記 gen/.stamp；vendor.just 內啟動器 `. ./log.sh`。薄殼由四檔改**五檔**：entry.just、vendor.just、log.sh、.gitignore、ci/check.sh（+ version.toml）<sub>[v2.13 P9；v2.14-1]</sub> |')
# ---- §4.9 ----
rep('使用者可手改（要改先問、永不覆蓋）。baseline 副本位置與 metadata 記錄：§9.1 P10。<sub>[v2.12 L3′]</sub> |',
    '使用者可手改（要改先問、永不覆蓋）。baseline 副本 = `baseline/vendor_kit/config.toml`（install 建、`upgrade vendor_kit` 推進），metadata 記在 `baseline/.vendor_kit.toml`（與根 `.dockerignore` 同表，`[[file]]` dest=`.vendor_kit/config.toml` state=managed）；uninstall 比照初始檔保護模式（hash == 副本 → 刪，被改 → 留並列出）。**例外於 §4 通則：config.toml 不寫 `written_by`、也不寫 `schema` 以外的任何機器欄位**（使用者可編輯、含註解），只保留 `schema = 1`。<sub>[v2.12 L3′；v2.13 P6、P10]</sub> |')
rep('| `written_by` | string | 是 | — | 同 §4 通則（純資訊；使用者手改後不更新；§9.1 P10） |', '| `written_by` | — | **不寫** | — | 例外於 §4 通則：config.toml 是使用者可編輯的檔，不放機器欄位（v2.13 P10） |')
rep('install 寫出的範本（逐字，`<vX>` 為引擎版本）：\n```toml\n# vendor_kit 設定檔（進 git）。缺檔或缺鍵 = 預設值；非正整數會退回預設並警告。\nschema = 1\nwritten_by = "<vX>"\n',
    'install 寫出的範本（逐字；同一份也放 `baseline/vendor_kit/config.toml`）：\n```toml\n# vendor_kit 設定檔（進 git）。缺檔或缺鍵 = 預設值；非正整數會退回預設並警告。\nschema = 1\n')
# ---- §4.10 ----
rep('`<verb>` = vendor_kit 動詞名（`upgrade vendor_kit`、不帶 repo 的 `upgrade` 皆在 `upgrade/`；bootstrap.sh 自身那段 §9.1 P4）；',
    '`<verb>` = vendor_kit 動詞名（`upgrade vendor_kit`、不帶 repo 的 `upgrade` 皆在 `upgrade/`；bootstrap.sh 自身那段在 `bootstrap/`，由 bootstrap.sh 自己建目錄、產 trace_id、寫 `launcher_start`，install 失敗清半成品時 `log/` 保留；v2.13 P4）；')
rep('目錄內自帶 `.gitignore`（`*`／`!.gitignore`）；`.vendor_kit/.gitignore` 列 `log/`；根 `.dockerignore` 由 install append `.vendor_kit/log/`。',
    '目錄內自帶 `.gitignore`（`*`／`!.gitignore`；由啟動器第一次建 `log/` 時一起建）；`.vendor_kit/.gitignore` 列 `log/`；根 `.dockerignore` 由 install append `.vendor_kit/log/`（三行改**四行**，與 Q22 cache 同理；v2.13 P13）。')
rep('| 引擎寫法 | Python `logging` + JSON formatter（`json.dumps`）append 同一檔（`open(path, \'a\')` + 每筆 flush），不引 OTel SDK；',
    '| 引擎寫法 | 以 `-e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔>` 定位（§5；v2.13 P8）；每個子命令容器各自 `engine_start`／`engine_exit`（v2.14-2）；Python `logging` + JSON formatter（`json.dumps`）append 同一檔（`open(path, \'a\')` + 每筆 flush），不引 OTel SDK；')
rep('| 啟動器寫法 | 移植 base `dist/script/docker/lib/log.sh` 到 POSIX sh：API `_log_<level> <event> [k=v]…`；`body` → `event_name`、`service.name` → `component` + `verb`；事件註冊表 `log-events.txt` 未註冊即 FATAL；bats 測試隨附。',
    '| 啟動器寫法 | 薄殼第五檔 `log.sh`（§4.5；由引擎重產、帶自描述首行）：移植 base `dist/script/docker/lib/log.sh` 到 POSIX sh，API `_log_<level> <event> [k=v]…`；`body` → `event_name`、`service.name` → `component` + `verb`；bats 測試隨附。')
rep('| lnav | Release 資產附 lnav format 檔：',
    '| 事件註冊表落點 | 真本 `log-events.txt` 在引擎 image；啟動器端 `log.sh` 內嵌一份啟動器事件白名單（`case`）；release CI 驗「內嵌清單 ⊆ 真本」；未註冊事件 = 程式錯誤 → FATAL 結束 1（同 base）。<sub>[v2.13 P9]</sub> |\n| 零寫入例外 | 「零寫入」= 不寫任何專案檔，操作紀錄檔例外：`launcher_start`／`engine_start` 已寫屬預期（結束碼 3、6-12、6-30、6-37 等情境皆同）。<sub>[v2.13 P12]</sub> |\n| lnav | Release 資產附 lnav format 檔：')
rep('| `timestamp` | string | 是 | ISO 8601 UTC，微秒：`YYYY-MM-DDTHH:MM:SS.ffffffZ`（啟動器端取得方式與精度：§9.1 P7） |',
    '| `timestamp` | string | 是 | ISO 8601 UTC，微秒：`YYYY-MM-DDTHH:MM:SS.ffffffZ`；啟動器端試 `date -u +%Y-%m-%dT%H:%M:%S.%NZ`，輸出含字面 `N`（busybox）→ 退回秒級補零；引擎一律微秒（v2.13 P7） |')
# ---- §5 ----
rep('引擎只取 trace_id 當操作紀錄檔 `trace_id` 與進度日誌 `<id>`；不採用使用者環境既有值；引擎定位 log 檔是否另需環境變數：§9.1 P8 <sub>[v2.12 L5]</sub> |',
    '引擎只取 trace_id 當操作紀錄檔 `trace_id` 與進度日誌 `<id>`；不採用使用者環境既有值；與 `VENDOR_KIT_LOG_FILE` 並用 <sub>[v2.12 L5；v2.13 P8]</sub> |\n| `VENDOR_KIT_LOG_FILE` | 啟動器產 → 轉發引擎 | 容器內路徑 `/repo/.vendor_kit/log/<verb>/<UTC-ts>-<id8>.jsonl`（啟動器建的那一檔）；每次 docker run 皆傳（含 §3.4 接手，同值）；引擎 append 同一檔、不另開檔；不採用使用者環境既有值；在 `-e` 白名單（§3.1）<sub>[v2.13 P8]</sub> |')
# ---- §6 P11 ----
rep('（結束 1；逐字待審 §9.1 P11）| <sub>[base_pitfalls 2-9；remaining Q7；review I-37、I-38；v2.10-3]</sub> |',
    '（結束 1；文案採草擬，待 codex／使用者審，不擋規格；v2.13 P11）| <sub>[base_pitfalls 2-9；remaining Q7；review I-37、I-38；v2.10-3；v2.13 P11]</sub> |')
rep('無 `--no-log`；逐字待審 §9.1 P11）| <sub>[v2.12 L4]</sub> |', '無 `--no-log`；文案採草擬，待 codex／使用者審，不擋規格；v2.13 P11）| <sub>[v2.12 L4；v2.13 P11]</sub> |')

# ---- §9.1 ----
old_91 = s[s.index('### 9.1 仍待定（13 條）'):s.index('### 9.2 已定值')]
new_91 = '''### 9.1 仍待定（3 條）

B1、F5 已依 grilling 2026-09-19 末條定案（見 §9.2）。v3 併入時發現的 P4–P13 已依 v2.13 結案（見下「已結案」；使用者可否決）。

待議（來源已明列，等時機或第三方）：
- **P1** 啟動器讀 config.toml 的方式：現為 grep 正規行（§4.9）；config 鍵變多時改由引擎產啟動器專用平面檔或其他方式；重評觸發 = 新增第二個表或啟動器要讀的鍵超過兩個。<sub>[v2.12 L3′；grilling 2026-09-20]</sub>
- **P2** base 反向採用 vendor_kit 的 POSIX log.sh（單一 owner）：開 issue；不影響本規格。<sub>[v2.12 L5；grilling 2026-09-20]</sub>
- **P3** L6 事件集合（§4.10 事件表）依建議先行，**待 codex 審過才最後定案**；審後只准增刪事件名與屬性，不改欄位表。<sub>[v2.12 L6]</sub>

已結案（v2.13，主對話依既定原則決定；落點）：
- **P4** bootstrap.sh 就是第一次接入的啟動器：驗 git repo／just → `mkdir -p .vendor_kit/log/bootstrap/` → trace_id → `launcher_start`（失敗 → 1 + 6-38）→ 才 pull／install；install 失敗清半成品但 **`.vendor_kit/log/` 保留**，訊息明說紀錄位置 → §1.2 bootstrap.sh、§2c、§4.10。
- **P5** 第一次 install 也建 `.tmp.install.<id>.toml`（統一規則、無例外），兼「不留半成品」的清除清單，成功後刪 → §0、§1.2 install、§2c、§4.6。
- **P6** uninstall：config.toml 比照初始檔保護模式（hash == baseline 副本 → 刪；被改 → 留並列出）；`log/` 一律保留、不 rmdir、`.vendor_kit/` 只剩 `log/`，訊息說明 → §1.2 uninstall、§2c。
- **P7** 白名單加 `mkdir`、`date`（連同 `od`、`tr`）；啟動器 timestamp 試 `%N`、busybox 退回秒級；引擎一律微秒 → §3.1、§4.10 欄位表。
- **P8** `-e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔>`，與 `TRACEPARENT` 並用 → §3.1 docker run 參數與 `-e` 白名單、§3.2、§5。
- **P9** 真本 `log-events.txt` 在引擎 image；啟動器端 `log.sh` 內嵌啟動器事件白名單，release CI 驗內嵌 ⊆ 真本；未註冊 → FATAL 1；薄殼四檔改五檔（`log.sh` 由引擎重產、帶自描述首行）→ §0、§4.5、§4.10。
- **P10** baseline 副本 `baseline/vendor_kit/config.toml`，metadata 記於 `baseline/.vendor_kit.toml`（與根 `.dockerignore` 同表）；config.toml 不寫 `written_by`／`schema` 以外的機器欄位 → §4.9。
- **P11** 6-38／6-24 文案採草擬，待 codex／使用者審（不擋規格）→ §6。
- **P12** 「零寫入」= 不寫任何專案檔，操作紀錄檔例外 → §0、§4.10。
- **P13** 根 `.dockerignore` 四行（加 `.vendor_kit/log/`），與 Q22 cache 同理 → §4.10（各節已為四行）。
- 低風險推論照子代理所寫：`upgrade vendor_kit` 對 config.toml 走狀態機＋6-22；grep 命中 0 → 預設不警告、重複／非正整數 → 預設＋警告；log prune 不刪本次檔與 `.gitignore`；啟動器一律自產 `TRACEPARENT`。

'''
s = s.replace(old_91, new_91)

# ---- §10 ----
rep('共 95 處（v3 新增 #58–#95）。',
'''| 96 | 文首 | v3 → v3.1；來源優先序加 v2.14 → v2.13；前版另存 `interface_spec.v3.0.md` | 本次 |
| 97 | §0 進度日誌 | install 第一次也建 `.tmp.install.<id>.toml`，兼不留半成品的清除清單 | v2.13 P5 |
| 98 | §0 操作紀錄檔、事件註冊表、結束碼 3 | bootstrap.sh = 第一次接入的啟動器（P4）；註冊表落點（P9）；零寫入例外（P12） | v2.13 P4、P9、P12 |
| 99 | §1.2 通則 | 每個引擎子命令各自 `engine_start`／`engine_exit`；啟動器結束 `log_prune`／`launcher_exit`；圖面表現法 | v2.14-2 |
| 100 | §1.2 bootstrap.sh | 順序：驗 git／just → mkdir log/bootstrap/ → trace_id → launcher_start → pull／install；pull 失敗與 tag 形 inspect 失敗為失敗出口；install 失敗清半成品、`log/` 保留、訊息明說 | v2.13 P4、P5；v2.14-5 |
| 101 | §1.2 install | 第一次與修復型都建 `.tmp.install.<id>.toml`；`log/`（含 `.gitignore`）由啟動器建 | v2.13 P4、P5 |
| 102 | §1.2 uninstall | config.toml 保護模式（hash == baseline 副本 → 刪）；`log/` 一律保留、不 rmdir、`.vendor_kit/` 只剩 `log/`、訊息說明 | v2.13 P6；v2.14-6 |
| 103 | §1.2 upgrade (b) | 重產薄殼五檔（含 log.sh）；config.toml 缺則建／有則三方合併（6-22）獨立一步，B = `baseline/vendor_kit/config.toml` | v2.13 P9、P10；v2.14-7 |
| 104 | §1.2 sync | `resolve sync` 偵測未完成交易 → 6-33 結束 1（與 update 同菱形）；工具 image pull 失敗為失敗出口 | v2.14-4、-5 |
| 105 | §2c | 薄殼五檔；bootstrap.sh／install 第一次／uninstall 三列的 config.toml、`.tmp.*`、`log/` 欄填實（原 §9.1 P4／P5／P6） | v2.13 P4–P6 |
| 106 | §3.1 白名單 | 加 `mkdir`、`date`（與 `od`、`tr` 同為操作紀錄檔用）；啟動器 timestamp 精度規則；`log/` 首次建立含目錄內 `.gitignore` | v2.13 P7；v2.14-8 |
| 107 | §3.1 docker run／`-e` 白名單 | 加 `-e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔>` | v2.13 P8；v2.14-8 |
| 108 | §3.2 | 每個子命令容器各自 `engine_start`／`engine_exit`；定位檔 = `VENDOR_KIT_LOG_FILE` | v2.13 P8；v2.14-2 |
| 109 | §4.4 | gen/.stamp 維持只記引擎 ref，明寫不承擔 log.sh hash（撤回第十版畫法） | v2.14-1 |
| 110 | §4.5 | 自描述首行加 log.sh；新增 `log.sh` 列（薄殼五檔、由引擎重產、內嵌事件白名單） | v2.13 P9；v2.14-1 |
| 111 | §4.9 | baseline 副本 `baseline/vendor_kit/config.toml` + metadata 落點；uninstall 保護模式；不寫 `written_by`（欄位表與範本同步） | v2.13 P6、P10 |
| 112 | §4.10 | bootstrap 那段在 `log/bootstrap/`；目錄內 `.gitignore` 由啟動器建；四行；引擎寫法加定位與每容器 start/exit；啟動器寫法 = 薄殼 log.sh；新增「事件註冊表落點」「零寫入例外」兩列；timestamp 精度 | v2.13 P4、P7–P9、P12、P13；v2.14-2 |
| 113 | §5 | 新增 `VENDOR_KIT_LOG_FILE`；TRACEPARENT 列去掉 P8 指標 | v2.13 P8 |
| 114 | §6 | 6-24、6-38 文案標「採草擬、待審、不擋規格」 | v2.13 P11 |
| 115 | §9.1 | 13 條 → 3 條待議 + P4–P13 已結案清單（含低風險推論） | v2.13 |

共 115 處（v3 新增 #58–#95；v3.1 新增 #96–#115）。''')
open(P, "w", encoding="utf-8").write(s); print("ok")
