OpenAI Codex v0.155.0
--------
workdir: <scratchpad>
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: low
reasoning summaries: none
session id: 01a0b9e0-4e1f-79a3-adb2-6c847a0d70e4
--------
user
# 任務：審查 vendor_kit 執行紀錄（run log）的事件清單（L6）

vendor_kit 的執行紀錄（run log）：每個動詞每次執行寫一檔 JSONL（`.vendor_kit/log/<verb>/<ts>-<id8>.jsonl`），欄位 timestamp／severity_text／event_name／body／trace_id／attributes（OTel Logs Data Model 對齊，事件名放 event_name）。啟動器（POSIX sh，移植自附件 D 的 log.sh）寫 launcher_* 與 docker_* 事件，引擎（Python）寫其餘。事件註冊表 log-events.txt 真本在引擎 image，啟動器內嵌白名單，未註冊即 FATAL。

請審附件 A v2.12 L6 的事件集合（附件 B §4.10 的事件表是同一集合的展開版，含 attributes）：
(1) 每個事件是否必要、命名是否一致（動詞_名詞 vs 名詞_動詞；start/finish vs started/finished）、有沒有重複或缺口（例如 registry 查詢失敗、pull 逾時、鎖等待逾時、config 讀取退回預設、進度檔恢復、dry-run 標記、每檔 append 行的細節、CI 模式旗標）；
(2) attributes 欄位建議（哪些必填、哪些敏感不可記）；
(3) 與附件 D base 的事件命名慣例對齊（base 用 snake_case、名詞_動詞過去式？請看實際檔案 log-events.txt 與 log.sh）；
(4) 每個事件的 severity 建議；
(5) 給最終建議清單（表：event_name｜寫者 launcher/engine｜severity｜必填 attributes｜何時）。

輸出：繁體中文；不確定的地方要標明「不確定」。請直接輸出 Markdown 報告，不要問問題。

背景知識（來自 spec 其他節，供判斷）：
- 動詞：install／add／remove／sync／update／upgrade（`upgrade <repo>`、`upgrade vendor_kit`）／dev／undev／prune／uninstall／help；bootstrap.sh 為第一次接入的啟動器（log 在 `log/bootstrap/`）。
- 引擎分 resolve 容器（唯讀、產計畫）與 apply 容器（寫入，先拿 flock 並重驗 fingerprint）；部分動詞單段。
- 進度檔（journal）`.vendor_kit/.tmp.<verb>.<id>.toml`：可寫動詞第一個寫入前建、成功後刪；偵測到未完成交易 → 可寫動詞先恢復、sync／update 印 6-33 結束 1、help 印 6-33 仍 0。
- 結束碼：0 成功、1 錯誤、3 版本不合（零寫入）。訊息編號 6-xx（如 6-38 = 執行紀錄寫不了、6-33 = 有未完成交易、6-24／6-31 = pull 失敗、6-20／6-21／6-22／6-32／6-34 = 問句）。
- CI 模式：環境變數 `CI` 照原值轉發；CI 模式下 sync 不走快路徑、不互動。
- `--dry-run` 只 prune 有；`-y` = 自動回答 yes。
- 敏感值：`VENDOR_KIT_REGISTRY_TOKEN`／`_USER`／`_TOKEN_FILE`、URL userinfo、docker login 輸出。
- 啟動器可用命令白名單：sh 內建、grep、sed、id、mktemp、mkdir、date、rm、sleep、od、tr、git rev-parse、docker {pull, create, cp, run, rm, inspect, image inspect, image ls, image rm, container ls, network ls, network rm, volume ls, volume rm, load, info}。
- `VENDOR_KIT_PULL_TIMEOUT` 由啟動器自讀（pull 逾時）；`VENDOR_KIT_NO_LOCK` 轉發引擎。

============================================================
## 附件 A：decisions/proposal_v2.md 的 v2.12、v2.13、v2.14 三節全文
============================================================
# v2.12 操作紀錄檔（2026-09-20 使用者逐題定案 L1–L5；L6 依建議先行、**待 codex 審過才最後定案**）
- L1 位置與切割：`.vendor_kit/log/<verb>/<UTC-ts>-<id8>.jsonl`，一次執行一檔（前例 npm `_logs/`；base `log/<verb>/<ts>-<traceid8>.log`）。`.gitignore`／`.dockerignore` 由 install 加 `.vendor_kit/log/`；目錄內自帶 `.gitignore`（`*`／`!.gitignore`）。不做 latest symlink。
- L2 格式：JSON Lines；欄位 `timestamp`（ISO 8601 UTC 微秒）、`severity_text`、`event_name`（有限集合，對齊現行 OTel Logs Data Model 的 EventName）、`body`（人讀一句話，選填；凡印到 tty 的訊息一律同句進 body）、`trace_id`（32 hex）、`attributes{component: launcher|engine, verb, …}`。使用者 Notion 筆記已同步改為 event_name。
- L3 保留：每個動詞目錄各自「最近 30 天且最多 50 檔」（stricter wins；base 為 20／14）；年齡用檔名時間戳、計數用檔名排序；啟動器結束時 prune、best-effort。
- L3′ 設定：新檔 `.vendor_kit/config.toml`（進 git；install 建立含註解與預設值；缺檔或缺鍵 = 預設）`schema = 1`、`[log] keep = 50`、`days = 30`；非正整數 → 預設 + 警告。upgrade 對它 = 三方合併初始檔。引擎用 TOML parser 讀（**parser 以 stage 明確帶進引擎 image**：`COPY --from=ghcr.io/ycpss91255-docker/toml-bridge:<tag>@sha256:…`，不依賴基底 Python 的 tomllib）；啟動器 grep 正規行 `^keep *= *[0-9]+ *$`（**待議**：config 鍵變多時改由引擎產啟動器專用平面檔或其他方式）。
- L4 寫失敗：**先確認能寫才開始**——啟動器 mkdir + 建檔 + 寫 `launcher_start` 失敗 → 1 + 6-38、零寫入；引擎 append `engine_start` 失敗 → 1 + 6-38、不進 resolve。所有動詞一致（含 help／prune），無 `--no-log`。磁碟滿連 prune 也擋：6-38 附清空間提示；紀錄以備追責。
- L5 實作：移植 base `dist/script/docker/lib/log.sh`（API `_log_<level> <event> [k=v]…`、事件註冊表 `log-events.txt` 未註冊即 FATAL、lnav format、bats）到 POSIX sh：跳脫改 `decisions/log/json_escape_fixed.sh`（dash＋busybox 實測）、`body`→`event_name`、`service.name`→`component`＋`verb`。啟動器 `launcher_start` 記**完整原始 argv**（逐項跳脫，不論合法與否）；引擎 `engine_start` 再記一次收到的 argv；引擎 Python `logging` + JSON formatter（`json.dumps`）append 同一檔，不引 OTel SDK。trace_id 由啟動器產（`/proc/sys/kernel/random/uuid` 去 `-`，缺則 `od -An -N16 -tx1 /dev/urandom`；啟動器工具清單加 `od`、`tr`），同值 = 進度日誌交易 id，`TRACEPARENT` 傳給引擎。驗收：每個 log 檔逐行 `json.loads`；bats 餵 `"`、`\`、換行、`[`、非 ASCII argv。開 issue：base 反向採用 vendor_kit 的 POSIX log.sh（單一 owner）。
- L6 事件集合（先依建議；待 codex）：啟動器 `launcher_start`（argv、verb、engine_ref、cwd、launcher 版本、CI 真值）、`config_read`、`docker_pull_start/finish`、`docker_extract`、`engine_spawn`、`sync_fast_path`、`log_prune`、`launcher_exit`（exit_code、duration_ms、reason）；引擎 `engine_start`、`journal_recovered`／`journal_detected`、`resolve_finish`、`lock_acquired`、`fingerprint_verified`、`journal_created/deleted`、`prompt_asked/answered`（auto:true 表 -y）、`file_created/modified/appended/deleted`、`merge_conflict`、`declined`、`version_written`、`registry_query`、`prune_candidate/removed`、`engine_exit`（exit_code、message_id、duration_ms、summary）。通用：6-xx 訊息同句進 body + `message_id`；憑證永不記、URL 去 userinfo。
- 架構：log 與 ci 為輔助模組，核心只透過 `log_event()` 一個介面呼叫（不是 sidecar 容器）；sync 快路徑維持不起引擎（實測 grep 0.00 s vs 引擎容器 0.42 s，且不依賴 daemon）。
- 新訊息 6-38；新檔 config.toml、log/ 進目錄樹、schema 表、動詞×檔案矩陣；架構圖加 log 模組。

# v2.13 spec v3 待議 P4–P13 的取捨（2026-09-20 主對話依既定原則決定；使用者可否決）
- P4 bootstrap.sh：它就是第一次接入的啟動器。順序：驗 git repo／just → `mkdir -p .vendor_kit/log/bootstrap/` → 產 trace_id → 寫 `launcher_start`（失敗 → 1 + 6-38）→ 之後才 pull／install。install 失敗「不留半成品」的例外：**`.vendor_kit/log/` 保留**（使用者 L4：紀錄以備追責）；訊息明說「已清除半成品，紀錄在 .vendor_kit/log/bootstrap/<檔>」。
- P5 第一次 install 也建 `.tmp.install.<id>.toml`（統一規則、無例外，v2.11 精神）；該日誌同時是「不留半成品」的清除清單，成功後刪。
- P6 uninstall：`config.toml` 比照初始檔保護模式——hash == baseline 副本 → 刪；被使用者改過 → 留下並列出（永不刪使用者改過的檔）。`log/` 一律保留（uninstall 自己也在寫），結束訊息說明 `.vendor_kit/log/` 留存、可手動刪。
- P7 啟動器白名單加 `mkdir`、`date`（連同 `od`、`tr`）。啟動器 timestamp：試 `date -u +%Y-%m-%dT%H:%M:%S.%NZ`，輸出含字面 `N`（busybox）→ 退回秒級；引擎一律微秒。
- P8 引擎定位檔：`-e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔>`（進 `-e` 白名單與 §5），與 `TRACEPARENT` 並用。
- P9 事件註冊表：真本 `log-events.txt` 在引擎 image；啟動器端 `log.sh` 內嵌一份啟動器事件白名單（case），release CI 驗「內嵌清單 ⊆ 真本」；未註冊事件 = 程式錯誤 → FATAL 結束 1（同 base）。薄殼由四檔改**五檔**：`entry.just`、`vendor.just`、`log.sh`、`ci/check.sh`（+ version.toml）；`log.sh` 從 base log.sh 移植（POSIX），由引擎重產、hash 記在 gen/.stamp。
- P10 config.toml 的 baseline 副本：`baseline/vendor_kit/config.toml`，metadata 記在 `baseline/.vendor_kit.toml`（與根 .dockerignore 同表）；config.toml **不寫 `written_by`／`schema` 以外的機器欄位**（使用者可編輯、含註解），`schema = 1` 保留。
- P11 6-38／6-24 文案先採草擬，待 codex／使用者審。
- P12「零寫入」= 不寫任何專案檔，**操作紀錄檔例外**（launcher_start／engine_start 已寫屬預期）。
- P13 根 `.dockerignore` 四行（加 `.vendor_kit/log/`），與 Q22 cache 同理。
- 低風險推論照子代理所寫（upgrade vendor_kit 對 config.toml 走狀態機＋6-22；grep 命中 0 → 預設不警告、重複／非正整數 → 預設＋警告；log prune 不刪本次檔與 .gitignore；啟動器一律自產 TRACEPARENT）。

# v2.14（2026-09-20 第十輪後；圖面落實與兩個小定案）
1. `log.sh` 與其他薄殼檔同規則：**帶自描述首行** `# vendor_kit-shell/<P> engine=<vX> sha256=…`；`gen/.stamp` 維持只記引擎 ref（§4.4 不變）。撤回第十版「gen/.stamp 記 log.sh hash」的畫法。
2. 引擎每個子命令（resolve 容器、apply 容器）啟動都先 append `engine_start`，結束寫 `engine_exit`；啟動器結束寫 `log_prune`、`launcher_exit`。圖上表現法統一：每頁 resolve 段與 apply 段各一格「append engine_start（失敗 → 1 + 6-38）」，頁尾一格「launcher_exit／log_prune」（可與結束橢圓相鄰、一格）。
3. 步驟格顏色規則統一：**藍 = 引擎（容器內）做的**、白 = 啟動器（主機）做的；同一動作各頁一致（install(2) 的建 justfile／append／刪日誌都是引擎 → 藍）。
4. sync resolve 加「偵測未完成交易？→ 是：印 6-33 結束 1」菱形（與 update 同）。
5. 工具 image `docker pull` 失敗（6-24／6-31）一律畫紅色出口（add(1)、B(1)、sync(2)、回退、undev）；bootstrap(1) 引擎 pull 失敗與 tag 形 inspect 失敗加紅出口。
6. uninstall(2)：不 rmdir `log/`，`.vendor_kit/` 保留（只剩 log/），訊息說明；config.toml 依 v2.13 P6。
7. E(c)(2) 加「config.toml：缺則建／有則三方合併（6-22 問）」一格與檔案框。
8. VENDOR_KIT_LOG_FILE 已定（v2.13 P8）→ spec §3.1／§5 白名單同步；契約④ 白名單加 od、tr、mkdir、date；快路徑前提加 log/。
9. 驗收矩陣頁（v1p3c）同步到 35 條。

============================================================
## 附件 B：decisions/interface_spec.md §4.10 執行紀錄（全文）
============================================================
### 4.10 執行紀錄（`.vendor_kit/log/`）

| 項目 | 規格 |
|---|---|
| 位置與切割 | `.vendor_kit/log/<verb>/<UTC-ts>-<id8>.jsonl`；`<verb>` = vendor_kit 動詞名（`upgrade vendor_kit`、不帶 repo 的 `upgrade` 皆在 `upgrade/`；bootstrap.sh 自身那段在 `bootstrap/`，由 bootstrap.sh 自己建目錄、產 trace_id、寫 `launcher_start`，install 失敗清半成品時 `log/` 保留；v2.13 P4）；`<UTC-ts>` = `YYYYMMDDTHHMMSSZ`；`<id8>` = trace_id 前 8 碼。**一次執行一檔**：同一次啟動器呼叫（含 §3.4 接手的第二個引擎、resolve 與 apply 兩個容器）append 同一檔，同一時間只有一個寫者；不做 latest symlink（Windows／CIFS 上 symlink 不可靠，檔名排序即可）。目錄內自帶 `.gitignore`（`*`／`!.gitignore`；由啟動器第一次建 `log/` 時一起建）；`.vendor_kit/.gitignore` 列 `log/`；根 `.dockerignore` 由 install append `.vendor_kit/log/`（三行改**四行**，與 Q22 cache 同理；v2.13 P13）。<sub>[v2.12 L1；agy_summary 前例 npm `_logs/`；出處：base `log/<verb>/<ts>-<traceid8>.log`]</sub> |
| 格式 | JSON Lines：UTF-8、每行一個 JSON object、LF 結尾、無空行；欄位名對齊現行 OTel Logs Data Model（`EventName` 為頂層欄位，`Body` 留給人讀訊息），**不引 OTel SDK**；捨棄 `observed_timestamp`、`span_id`、`trace_flags`、`severity_number`、`resource`、`instrumentation_scope`。欄位表見下。<sub>[v2.12 L2；agy_summary「JSONL+OTel 適用性」]</sub> |
| 保留 | 每個 `log/<verb>/` 目錄各自「最近 `days`（預設 30）天**且**最多 `keep`（預設 50）檔」，較嚴者勝；年齡用檔名時間戳（不用 mtime）、計數用檔名排序；由**啟動器**在每次呼叫結束時（trap 內、`launcher_exit` 前）prune，**best-effort**：失敗只 warn、不改結束碼；只刪 `*.jsonl`，不刪 `.gitignore`、不刪本次的檔；記 `log_prune` 事件。值來自 config.toml（§4.9）。不屬 `prune` 動詞。<sub>[v2.12 L3；出處：base 為 20／14]</sub> |
| 寫失敗（fail-closed） | **先確認能寫才開始**：啟動器 mkdir + 建檔 + 寫 `launcher_start` 任一失敗 → 1 + 6-38、零寫入（不進引擎 ref 取得、最低介面版檢查、docker）；引擎 append `engine_start` 失敗 → 1 + 6-38、不進 resolve／apply。所有動詞一致（含 help、prune、sync 快路徑、`--dry-run`）；無 `--no-log`。磁碟滿連 `prune` 也擋：6-38 附清空間提示。理由：紀錄以備追責；never fail silently。<sub>[v2.12 L4（取代 draft「不改結束碼」與 agy「唯讀動詞放行」）]</sub> |
| 憑證與敏感值 | `VENDOR_KIT_REGISTRY_TOKEN`／`_USER`／`_TOKEN_FILE` 內容永不記；`attributes` 不收環境變數；URL 一律去 userinfo；不記 `docker login` 相關輸出。驗收：所有 log 檔 grep 不到 token（§7.4-18）。<sub>[v2.12 L6；#28]</sub> |
| 6-xx 訊息 | 凡印到 tty 的訊息（含 §6 全部）一律**同句**進 `body`，並在 `attributes.message_id` 記 `6-xx`；問句記 `prompt_asked`、回答記 `prompt_answered`（`auto: true` 表 `-y`）。<sub>[v2.12 L2、L6]</sub> |
| trace_id | 32 hex，由啟動器產：`/proc/sys/kernel/random/uuid` 去 `-`；缺則 `od -An -N16 -tx1 /dev/urandom` 去空白（白名單加 `od`、`tr`）；同值 = 進度檔交易 id `<id>`（§4.6）；以 `TRACEPARENT`（W3C Trace Context `00-<trace_id>-<span_id>-<flags>`；span_id／flags 為實作細節，引擎只取 trace_id）傳給每個引擎容器（含 §3.4 接手的第二次，同值）；啟動器一律自產，不採用環境中既有的 `TRACEPARENT`。<sub>[v2.12 L5；agy_summary2「trace_id 傳遞前例」（`TRACEPARENT` 為 otel-cli／Thoth 事實標準）]</sub> |
| 啟動器 argv | `launcher_start` 記**完整原始 argv**（`"$@"` 逐項、array of string，不論合法與否、不做任何正規化）；引擎 `engine_start` 再記一次收到的 argv。逐項 JSON 跳脫（採 `decisions/log/json_escape_fixed.sh`，dash 與 busybox sh 實測 15 案例通過）：順序 `\` → `\\`、`"` → `\"`、U+0008／0009／000C／000D → `\b`／`\t`／`\f`／`\r`、其餘 U+0001–001F → `\u00XX`、換行 → `\n`；全程 `printf '%s'`、不用 `echo`、只跑一次 sed。已知限制：NUL 進不了 shell 變數；無效 UTF-8 位元組原樣輸出。<sub>[v2.12 L5；agy_summary2 修正版]</sub> |
| 引擎寫法 | 以 `-e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<verb>/<檔>` 定位（§5；v2.13 P8）；每個子命令容器各自 `engine_start`／`engine_exit`（v2.14-2）；Python `logging` + JSON formatter（`json.dumps`）append 同一檔（`open(path, 'a')` + 每筆 flush），不引 OTel SDK；核心模組只透過單一介面 `log_event()` 呼叫，log 與 ci 為輔助模組（不是 sidecar 容器）；引擎不做保留清理。<sub>[v2.12 L5、架構]</sub> |
| 啟動器寫法 | 薄殼第五檔 `log.sh`（§4.5；由引擎重產、帶自描述首行）：移植外部 repo 的 `dist/script/docker/lib/log.sh` 到 POSIX sh（出處見註記），API `_log_<level> <event> [k=v]…`；`body` → `event_name`、`service.name` → `component` + `verb`；bats 測試隨附。sync 快路徑不起引擎，由啟動器自己寫 `sync_fast_path`（實測 grep 0.00 s vs 引擎容器 0.42 s，且不依賴 daemon）。<sub>[v2.12 L5、架構；出處：base log.sh]</sub> |
| 事件註冊表落點 | 真本 `log-events.txt` 在引擎 image；啟動器端 `log.sh` 內嵌一份啟動器事件白名單（`case`）；release CI 驗「內嵌清單 ⊆ 真本」；未註冊事件 = 程式錯誤 → FATAL 結束 1（同 base）。<sub>[v2.13 P9]</sub> |
| 零寫入例外 | 「零寫入」= 不寫任何專案檔，執行紀錄例外：`launcher_start`／`engine_start` 已寫屬預期（結束碼 3、6-12、6-30、6-37 等情境皆同）。<sub>[v2.13 P12]</sub> |
| lnav | Release 資產附 lnav format 檔：`json: true`、`timestamp-field: timestamp`、`level-field: severity_text`、`opid-field: trace_id`（timeline 用；須含在 line-format）、`body-field: body`、`file-pattern` 對 `.vendor_kit/log/*/*.jsonl`；`attributes/duration_ms` 供 timeline duration。<sub>[v2.12 L5；agy_summary「lnav timeline 需要的欄位」]</sub> |

欄位表（每行）：

| 欄位 | 型別 | 必填 | 說明 |
|---|---|---|---|
| `timestamp` | string | 是 | ISO 8601 UTC，微秒：`YYYY-MM-DDTHH:MM:SS.ffffffZ`；啟動器端試 `date -u +%Y-%m-%dT%H:%M:%S.%NZ`，輸出含字面 `N`（busybox）→ 退回秒級補零；引擎一律微秒（v2.13 P7） |
| `severity_text` | string | 是 | `DEBUG`／`INFO`／`WARN`／`ERROR`／`FATAL`（對齊 OTel SeverityText；warn 與 error 事件對應印到 stderr 的 warn／錯誤） |
| `event_name` | string | 是 | 事件註冊表內的名稱（下表）；未註冊 → FATAL |
| `body` | string | 否 | 人讀一句話；凡印到 tty 的訊息一律同句進此欄 |
| `trace_id` | string | 是 | 32 hex；= 進度檔交易 id |
| `attributes` | object | 是 | 必有 `component` ∈ `launcher`／`engine`、`verb`；其餘依事件：`phase` ∈ resolve／apply／single、`path`、`action` ∈ create／modify／append／delete、`exit_code`、`duration_ms`、`message_id`、`prompt`、`answer`、`auto`、`argv`（array of string）、`engine_ref`、`cwd`、`launcher_version`、`ci`、`ref`、`digest`、`reason`、`keep`、`days`… |

事件集合（**L6：依建議先行，待 codex 審過才最後定案**；審後只准增刪事件名與屬性，不改欄位表）：

| component | event_name | 時機 | 主要 attributes |
|---|---|---|---|
| launcher | `launcher_start` | 建檔後第一筆 | `argv`（完整原始）、`verb`、`engine_ref`、`cwd`、`launcher_version`（薄殼首行 `engine=<vX>`）、`ci`（CI 模式真值） |
| launcher | `config_read` | 讀 config.toml 後 | `keep`、`days`、`source` ∈ file／default、警告（非正整數時，body 同句） |
| launcher | `docker_pull_start`／`docker_pull_finish` | 每筆 `pull` 記錄 | `name`、`ref`、`exit_code`、`duration_ms`、`reason`（逾時／網路／認證／不存在／主機錯誤） |
| launcher | `docker_extract` | 每筆 `extract` 記錄 | `repo`、`ref`、`path`（`.tmp.dist.<id>/<repo>/`） |
| launcher | `engine_spawn` | 每次 docker run 引擎前 | `engine_ref`、`subcommand`（resolve／apply／單段 verb）、`interactive` |
| launcher | `sync_fast_path` | sync 快路徑判定 | `result` ∈ hit／miss、`reason` |
| launcher | `log_prune` | trap 內保留清理後 | `deleted`（數）、`keep`、`days`、`error`（best-effort 失敗時） |
| launcher | `launcher_exit` | 最後一筆 | `exit_code`、`duration_ms`、`reason` |
| engine | `engine_start` | 子命令第一筆 | `argv`（收到的）、`verb`、`subcommand`、`engine_version`、`protocol` |
| engine | `journal_detected`／`journal_recovered` | 偵測到／恢復未完成交易 | `verb`、`id`、`path`、`result`（唯讀動詞只有 detected） |
| engine | `resolve_finish` | resolve 結束 | 計畫摘要（pull／extract／mount／engine 筆數、`apply` yes／no）、`fingerprint` |
| engine | `lock_acquired` | apply 拿到 flock | `wait_ms` |
| engine | `fingerprint_verified` | apply 重驗指紋 | `result` |
| engine | `journal_created`／`journal_deleted` | 進度檔建／刪 | `path`、`verb`、`id` |
| engine | `prompt_asked`／`prompt_answered` | 每個詢問 | `prompt`（6-20／6-21／6-22／6-32／6-34）、`path`、`answer` ∈ yes／no／eof、`auto`（true = `-y`） |
| engine | `file_created`／`file_modified`／`file_appended`／`file_deleted` | 每個實際寫入 | `path`、`action`、`strategy`、`lines`（appended 時） |
| engine | `merge_conflict` | 三方合併衝突 | `path` |
| engine | `declined` | 拒絕（記 `declined_hash`） | `path`、`state` |
| engine | `version_written` | version.toml 寫入 | `path`、`changed`（鍵清單） |
| engine | `registry_query` | 每次查 registry | `host`、`repo`、`result`、`duration_ms`（URL 去 userinfo；不記 token） |
| engine | `prune_candidate`／`prune_removed` | prune 候選／已刪 | `kind` ∈ container／image／network／volume／tmp、`id` |
| engine | `engine_exit` | 最後一筆 | `exit_code`、`message_id`、`duration_ms`、`summary` |

<sub>[v2.12 L6；draft 方案 A 事件集合]</sub>

範例（`sync` 快路徑，一檔三行；`…` 省略）：
```
{"timestamp":"2026-09-20T01:02:03.000000Z","severity_text":"INFO","event_name":"launcher_start","trace_id":"0123456789abcdef0123456789abcdef","attributes":{"component":"launcher","verb":"sync","argv":["sync"],"engine_ref":"ghcr.io/<org>/vendor_kit:v1.0.0@sha256:…","cwd":"/home/me/<專案根>","launcher_version":"v1.0.0","ci":false}}
{"timestamp":"2026-09-20T01:02:03.004000Z","severity_text":"INFO","event_name":"sync_fast_path","body":"快路徑：stamp 與 version.toml 全相符","trace_id":"0123456789abcdef0123456789abcdef","attributes":{"component":"launcher","verb":"sync","result":"hit"}}
{"timestamp":"2026-09-20T01:02:03.006000Z","severity_text":"INFO","event_name":"launcher_exit","trace_id":"0123456789abcdef0123456789abcdef","attributes":{"component":"launcher","verb":"sync","exit_code":0,"duration_ms":6}}
```


============================================================
## 附件 C-1：decisions/log/agy_summary.md 全文
============================================================
# agy 前例研究摘要：vendor_kit 操作紀錄檔（audit／operation log）

- 來源：`decisions/log/agy_out.md`（agy / Antigravity CLI，Gemini 3.8，`--sandbox -p`，一次成功，29 KB）
- 整理者：Claude 子代理。agy 的說法我另外用 WebFetch 對官方文件／原始碼逐一抽查；抽查結果標在各節與最後一節。
- 標記：✅ = 我已對到官方來源；⚠️ = agy 有講但我查到不一致或來源對不上；❓ = agy 無來源／我沒查。

## 前例對照表（工具｜位置｜格式｜一檔／追加｜輪替／保留｜來源）

| 工具 | 位置 | 格式 | 一檔／追加 | 輪替／保留 | 來源 | 抽查 |
|---|---|---|---|---|---|---|
| dpkg | `/var/log/dpkg.log` | 單行純文字 `YYYY-MM-DD HH:MM:SS <action> <pkg> <ver> <ver>` | 追加 | 系統 logrotate：monthly、rotate 12、compress、delaycompress | agy: [dpkg(1)](https://manpages.debian.org/unstable/dpkg/dpkg.1.en.html)；我：本機 Ubuntu 24.04 `/etc/logrotate.d/dpkg` | ✅ |
| apt | `/var/log/apt/history.log`（交易）、`term.log`（終端輸出）、`eipp.log.xz` | history.log 為 RFC 822 式 stanza（`Start-Date:`／`Commandline:`／`Install:`／`Upgrade:`／`End-Date:`），一次交易一個區塊 | 追加 | logrotate：monthly、rotate 12、compress（history 與 term 皆同） | agy: [apt.conf(5)](https://manpages.debian.org/unstable/apt/apt.conf.5.en.html)；我：本機 `/etc/logrotate.d/apt` | ⚠️ agy 說 history.log「rotate 1 或依發行版」，本機實查是 rotate 12 |
| pip | 預設**不寫檔**；`--log <path>`（`PIP_LOG`）才寫 | 純文字 verbose | 追加（「Path to a verbose appending log」） | 無 | [pip --log](https://pip.pypa.io/en/stable/cli/pip/#cmdoption-log) | ✅ |
| npm | `<cache>/_logs/`（`logs-dir`） | 純文字逐行 debug log | **一次執行一檔** `<ISO-ts>-debug-<n>.log` | `logs-max` 預設 **10**，超過刪最舊；0 = 不寫 | [config logs-max](https://docs.npmjs.com/cli/v10/using-npm/config#logs-max)、[npm logging](https://docs.npmjs.com/cli/v10/using-npm/logging) | ✅ |
| cargo | 無操作紀錄檔；`CARGO_LOG` 只控制 stderr 除錯等級（tracing） | — | — | — | agy 給的是 Cargo Book 首頁；我：[environment-variables](https://doc.rust-lang.org/cargo/reference/environment-variables.html) | ✅（agy 來源太籠統，已換） |
| terraform | 預設 stderr；`TF_LOG_PATH` 導向檔案（需同時設 `TF_LOG`） | 純文字；`TF_LOG=JSON` 為 JSON（官方註明格式不穩定、非支援介面） | 追加（「always be appended to a specific file」） | 無 | [Debugging Terraform](https://developer.hashicorp.com/terraform/internals/debugging) | ✅（agy 說 `TF_LOG_CORE=JSON`，文件是 `TF_LOG=JSON`；`TF_LOG_CORE/PROVIDER` 是子集開關） |
| pre-commit | `<store>/pre-commit.log`（預設 `~/.cache/pre-commit/`） | 純文字：版本、環境、traceback | **只有崩潰才寫**，`open(..., 'wb')` = **覆寫**上一次 | 無（永遠只有最後一次崩潰） | agy 只給 repo 首頁；我：[error_handler.py](https://github.com/pre-commit/pre-commit/blob/main/pre_commit/error_handler.py) | ⚠️ agy 寫「覆寫/附加」，實際只有覆寫 |
| renovate | `LOG_FILE=<path>`（v38 移除 `logFile` config；`RENOVATE_LOG_FILE` 是舊 config 的 env 映射，後續才討論兩者並存） | bunyan JSON 一行一筆（NDJSON）；`LOG_FILE_FORMAT=pretty` 可改；`LOG_FILE_LEVEL` 預設 debug | 追加（`fs.openSync(path,'a')`） | 無（CI 當 artifact） | 我：[lib/logger/bunyan.ts](https://github.com/renovatebot/renovate/blob/main/lib/logger/bunyan.ts)、[discussion #30635](https://github.com/renovatebot/renovate/discussions/30635) | ⚠️ agy 把新舊變數名講反；agy 引的 troubleshooting 頁沒有這些內容 |
| git reflog | `.git/logs/HEAD`、`.git/logs/refs/heads/<b>` | 單行 `<old> <new> <ident> <ts> <tz>\t<msg>` | 追加 | `git gc`／`reflog expire`：可達 90 天（`gc.reflogExpire`）、不可達 30 天（`gc.reflogExpireUnreachable`） | [git-reflog](https://git-scm.com/docs/git-reflog)、[git-config](https://git-scm.com/docs/git-config) | ✅ |
| docker | CLI 本身無本機操作紀錄（要靠 auditd）；容器輸出走 logging driver | `json-file`：`{"log","stream","time"}` JSONL | 追加 | driver 選項 `max-size`／`max-file` | [logging drivers](https://docs.docker.com/engine/logging/configure/)、[json-file](https://docs.docker.com/engine/logging/drivers/json-file/) | ❓ 未逐字抽查，但與我所知一致 |

觀察：**沒有一個前例用 OTel 欄位**；結構化 JSONL 的只有 renovate（bunyan）、docker json-file、terraform（選配）。「一次執行一檔＋計數保留」只有 npm；其餘幾乎都是單檔追加＋外部 logrotate 或時間到期。

## JSONL+OTel 在單機 CLI 的適用性（含 logfmt 比較、audit vs debug 分開的建議、來源）

agy 結論：**借用 OTel 的欄位名與語意，不引入 OTel SDK，自寫輕量 JSONL 序列化。**

- 保留：`timestamp`、`severity_text`、`body`、`trace_id`、`attributes{}`。
- 捨棄：`observed_timestamp`、`span_id`、`trace_flags`、`severity_number`、`resource`、`instrumentation_scope`（單機無意義）。
- 來源：[OTel Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) ✅。
- ⚠️ 我補充：目前 Data Model 的頂層欄位共 12 個，**含 `EventName`**（「Name that identifies the class / type of the Event」），而 `Body` 定義為自由文字或結構化資料。brief 裡「`body` = 事件名（有限集合）」是舊 Event API 時代的作法；agy 引的 [Event API 頁](https://opentelemetry.io/docs/specs/otel/logs/event-api/) 已 **404**，事件語意已併入 [Logs API](https://opentelemetry.io/docs/specs/otel/logs/api/)（emit 參數含 optional Event Name）。若要「對齊 OTel」，事件名應放 `event_name`，`body` 留給人讀訊息。另：OTel 的 `Timestamp` 是 uint64 奈秒，ISO 8601 字串是我們自己的 JSON 表示法，不是 OTLP/JSON 編碼。
- ❓ agy 說「OTel SDK 動輒增加數十 MB」——無來源。

logfmt 比較（來源 [brandur.org/logfmt](https://brandur.org/logfmt)、[go-logfmt](https://pkg.go.dev/github.com/go-logfmt/logfmt)）：
- 優點：人眼可讀、POSIX sh 用 `printf` 就能拼，不需 JSON 跳脫。
- 缺點：無正式規範（各解析器對引號／換行處理不一）、無巢狀／陣列、lnav 對 JSON 的支援遠比 logfmt 好。
- agy 判定：vendor_kit 需要記「多個檔案路徑」「詢問選項」等結構，JSONL 較合適。

audit vs debug 分開（agy 引 [NIST SP 800-92](https://csrc.nist.gov/publications/detail/sp/800-92/final)、[OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)）：
- audit：讀者是使用者／維護者；低雜訊（一次執行數筆～數十筆）；嚴禁憑證；保留較長（agy 說 30～90 天）。
- debug：讀者是開發者；高雜訊；易誤含 token；短期（最近 N 次或崩潰才產生）。
- 混在一檔會讓 `jq`／`lnav` 查 audit 時被 debug 淹沒。
- ❓ 兩份來源我未逐字核對；OWASP 那頁我記得確實建議 security event log 與 debug 分流，NIST 800-92 是泛論 log 管理，屬「泛引」。

## 一次一檔 vs 追加+輪替（優缺點、常見數字、來源）

| 面向 | 一次執行一檔 `<ts>-<verb>-<id>.jsonl` | 單檔追加 `vendor_kit.jsonl` + 輪替 |
|---|---|---|
| 並行／鎖 | 零衝突，不需 flock | 多終端同時跑要靠 O_APPEND 原子性或 flock |
| 輪替 | 只需列目錄刪最舊，無競態 | 無 daemon 的 CLI 誰來 rotate？rename／copytruncate 有遺失風險 |
| 崩潰隔離 | 壞行只污染該次檔 | 半截 JSON 行污染全檔後續解析 |
| 回報 issue | 附一個檔即可 | 要按 `trace_id` 節錄 |
| 跨次檢視 | 要 `cat *.jsonl` 或 lnav 開整個目錄 | `tail -f` 直覺 |
| inode | 保留策略失效會堆小檔 | 檔數固定 |

常見數字：
- 計數：npm `logs-max=10` ✅；agy 說 audit 常見 50～100 次 ❓（無來源）。
- 時間：git reflog 90／30 天 ✅；dpkg／apt monthly × 12 ✅（本機實查）。
- 容量：agy 說單檔 5～10 MB × 3～5 份、總量 < 50 MB ❓（無來源；docker json-file 的 `max-size`／`max-file` 是類似模式但無預設數字）。

## 容器內寫掛載目錄的坑（來源）

1. **掛載點由 daemon 建立會是 root 擁有**：`-v` 對不存在的主機路徑會自動建目錄（[bind-mounts](https://docs.docker.com/engine/storage/bind-mounts/) ✅ 有「automatically creates the directory」；`--mount` 預設報錯，除非 `bind-create-src`）。文件**沒有**明說 owner 是 root（agy 加的，實務上確實如此，但 ❓ 該頁無此句）。
   ⚠️ 對 vendor_kit 的適用性：我們只掛已存在的專案目錄 `/repo`，`.vendor_kit/log/` 是掛載**內部**的子目錄，由容器內以主機 uid 的行程 `mkdir` 建立，擁有者就是主機使用者——這個坑**不會**發生。agy 建議「啟動器先 `mkdir -p`」仍合理（啟動器自己那段要先寫 log），但理由不是 root 陷阱。
2. **umask**：容器與主機 umask 可能不同，agy 建議明確設 0644／0755 ❓（常識，無來源）。
3. **EXDEV**：`os.replace` 底層是 `rename(2)`，跨檔案系統會 `EXDEV`；`tempfile.NamedTemporaryFile()` 不指定 `dir` 會落在容器 `/tmp`（overlay/tmpfs）→ 搬到 `/repo` 失敗。對策：`dir=` 指到目標同目錄。來源 [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html)、[os.replace](https://docs.python.org/3/library/os.html#os.replace) ✅（這是既有進度檔 `.tmp.<verb>.<id>.toml` 也要注意的點）。
4. **flock**：Linux 原生 bind mount 與主機共用核心，`flock(2)`／`fcntl` 跨容器有效；但 NFS／CIFS／macOS／Windows Docker Desktop（VirtioFS、gRPC-FUSE、9P）鎖語意脆弱（[flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html) 有 NFS 註記 ✅；Docker Desktop 部分 ❓ agy 無來源）。agy 建議：乾脆用一次一檔避免鎖。
5. 追加寫入 JSONL 本身不需要暫存檔：`open(path,'a')` + 每筆 `flush()` 即可。

## lnav timeline 需要的欄位（來源）

來源：[lnav formats](https://docs.lnav.org/en/latest/formats.html)、[lnav ui](https://docs.lnav.org/en/latest/ui.html)、[NEWS.md](https://github.com/tstack/lnav/blob/master/NEWS.md)。

- `json: true`、`timestamp-field`（預設 `timestamp`，ISO 8601 UTC 開箱可解）✅
- `opid-field`（例如 `trace_id`）：timeline 用它把多行聚成一個 span；**文件明寫「MUST be included in the line-format for the o hotkeys to work」** ✅
- `level-field`（`severity_text`）：預設名是 `level`，要指定 ✅
- `duration-field` + `timestamp-point-of-reference`（`start`／`end`）：**v0.14.0 新增** ✅；`start-timestamp-field` 也是 0.14.0（agy 沒提）。
- ❓ `duration-divisor`：agy 有寫，我在 formats 頁摘要沒看到，未查證。
- Span 計算：「earliest and latest timestamps of messages associated with the item；若有 duration 也納入」✅。
- ⚠️ 開 timeline 的按鍵：agy 說 `t` 或 `Shift+A`。hotkeys 頁沒列 timeline 專屬鍵；ui 頁說可從 breadcrumb（`` ` ``）或 `:switch-to-view timeline` 進入，`Shift+A` 是「離開後回到 timeline 並同步時間」。`Shift+T` 是 time-offset 顯示，不是 timeline。
- 歷史：gantt view 在 v0.12.0 加入，v0.12.3 改名 timeline ✅。

agy 給的範例 format（`opid-field: trace_id`、`level-field: severity_text`、line-format 含 `trace_id`、`value` 裡標 `identifier`）結構合理；`attributes/duration_ms` 用 `/` 取巢狀欄位是 lnav JSON 格式的慣例（❓ 未逐字查）。

## agy 的推薦方案與理由

1. **位置**：`.vendor_kit/log/`；根 `.gitignore`／`.dockerignore` 加 `.vendor_kit/log/`，目錄內再放 `.gitignore`（`*` + `!.gitignore`）雙保險。
2. **一次執行一檔**：`<YYYYMMDDTHHMMSSZ>-<verb>-<trace_id前8碼>.jsonl`；結束後 `ln -sf` 一個 `latest.jsonl`。理由：免鎖、崩潰隔離、回報只附一檔；前例 npm `_logs/`。
3. **欄位**：`timestamp`（ISO 8601 UTC，微秒）、`severity_text`、`body`（有限事件集合：`launcher_start/exit`、`docker_pull_start/finish`、`engine_start/exit`、`resolve_start/finish`、`prompt_ask/answer`、`file_write/delete`、`apply_start/finish`）、`trace_id`（32 hex）、`attributes{verb, phase, path, bytes_written, component, exit_code, duration_s…}`。URL 遮蔽 token；`attributes` 禁收含 TOKEN／PASSWORD／SECRET 的 env。
4. **保留**：計數制，保留最近 **50** 檔；啟動器 `trap … EXIT` 時 `find | sort -r | sed '1,50d' | xargs rm -f`。
5. **啟動器（POSIX sh）**：先 `mkdir -p .vendor_kit/log`；產 `trace_id`（`/proc/sys/kernel/random/uuid` 或 `od /dev/urandom`）；自己用 `printf … >> $LOG_FILE` 寫 `launcher_start`／`launcher_exit`；把 `VENDOR_KIT_TRACE_ID`、`VENDOR_KIT_LOG_FILE=/repo/…` 用 `-e` 傳進容器，引擎追加寫**同一檔**。
6. **never fail silently 的分級**：
   - 唯讀動詞（help／update／resolve 階段）：log 寫失敗 → stderr 大聲警告、無 log 模式繼續、回 0。理由：磁碟滿時使用者還要能 `help`／`update` 排查。
   - 寫入動詞（install／upgrade／apply 階段／prune／remove）：進 apply 前先寫 `apply_start` 測試；寫不進 → 中止、非 0，除非 `--no-audit`。理由：狀態變更必須可追溯。
7. **容器內**：log 直接 `open('a')` + `flush()`；需原子替換的檔（進度檔）`NamedTemporaryFile(dir=目標同目錄)` 避 EXDEV。

## 我（子代理）認為 agy 說法可疑或無來源的地方

1. **apt history.log 輪替**：agy 說「rotate 1 或依發行版」；本機 Ubuntu 24.04 `/etc/logrotate.d/apt` 是 history 與 term 都 `monthly rotate 12`。
2. **Renovate 變數名講反**：v38 移除的是 `logFile` config（`RENOVATE_LOG_FILE` 就是它的 env 映射），現行是 `LOG_FILE`／`LOG_FILE_LEVEL`／`LOG_FILE_FORMAT`；agy 引的 troubleshooting 頁完全沒提檔案 log。正確來源是 `lib/logger/bunyan.ts`。
3. **pre-commit** 寫「覆寫/附加」，原始碼是 `open(log_path,'wb')` 純覆寫；agy 只引 repo 首頁。
4. **OTel Event API 連結 404**；現行 Data Model 有頂層 `EventName`，「`body` = 事件名」與現行規範不一致。**這點影響 brief 的欄位設計，建議主對話決定要不要改成 `event_name`。**
5. **Docker root 目錄陷阱套錯情境**：只對「掛載點本身不存在」成立；vendor_kit 的 log 目錄在既有掛載內部，以主機 uid 建立即可。文件也沒有明寫 owner 是 root。
6. **lnav 開 timeline 的按鍵**（`t`／`Shift+A`）與文件不符（見上節）；`duration-divisor` 未查證。
7. **無來源的數字**：audit 保留 50～100 次、單檔 5～10 MB × 3～5、OTel SDK 數十 MB、「audit 保留 30～90 天」。
8. **NIST 800-92／OWASP** 屬泛引，agy 沒有引用具體段落。
9. **Terraform**：JSON 開關是 `TF_LOG=JSON`（且官方說不穩定），不是 agy 寫的 `TF_LOG_CORE=JSON`。
10. **範例啟動器腳本有 bug／缺陷**（若主對話要採用要重寫）：
    - `date -u +"%Y%m%m%dT%H%M%SZ"` 的 `%m%m` 是筆誤。
    - `write_log` 沒做 JSON 跳脫，`$VERB` 來自 argv，含 `"` 或 `\` 會產生壞 JSON（正是「never fail silently」要避免的靜默壞檔）。
    - 註解說「依修改時間排序」，實際 `sort -r` 是依檔名；靠時間戳前綴才成立（可接受但要明講）。
    - `date +%s`、`id -u` 在 POSIX 嚴格意義下非必然，但主流 sh 都有。
    - trap 裡 `write_log "launcher_exit"` 在容器結束之後才寫，順序 OK；但 `latest.jsonl` 是 symlink，`find -type f` 不會誤刪，OK。
    - 用 `-v "$PWD:/repo"` 而非 `--mount`；文件建議 `--mount`（更明確、不自動建目錄）。
11. **fail-closed（寫入動詞 log 寫不進就中止）是 agy 的設計意見**，沒有任何前例這樣做（apt／dpkg／npm 都不因 log 失敗而拒絕動作）；這題 brief 標「要討論」，應交由 decision-review 雙軌再審。

============================================================
## 附件 C-2：decisions/log/agy_summary2.md 全文
============================================================
# agy 前例研究摘要 #2：POSIX sh 產生 JSON Lines 操作紀錄

- 原始題目：`decisions/log/agy_brief2.txt`；agy 原文：`decisions/log/agy_out2.md`（一次成功，約 22 KB）。
- 抽查方式：WebFetch 原始碼／官方文件 8 處；另在本機用 `dash` 與 `busybox sh`（含 busybox sed/tr/printf）實測 agy 給的跳脫函式與修正版（`decisions/log/agy_escape_test.sh`、`decisions/log/json_escape_fixed.sh`，輸出 `*.out`，並以 python `json.loads` 與 `jq` 驗證）。

## 主流專案 shell 內產 JSON 的前例（專案｜檔案連結｜跳脫方式｜bash 或 POSIX｜抽查結果）

agy 結論：主流專案（docker-library entrypoint、k8s/helm/kind hack、rustup/nvm/asdf/sdkman、Actions runner、systemd、busybox）**都不在 shell 裡手寫 JSON log**；JSON 化交給容器 runtime（docker json-file driver）、Go 端 klog、或 Actions 的 `::error::` workflow commands。

| 專案 | 檔案 | 跳脫方式 | bash／POSIX | 抽查結果 |
|---|---|---|---|---|
| kubernetes | https://github.com/kubernetes/kubernetes/blob/master/hack/lib/logging.sh | 無（純文字＋ANSI 顏色） | bash | 已抽查：12 個 `kube::log::*` 函式，無 JSON 輸出，agy 說法正確 |
| acme.sh | https://github.com/acmesh-official/acme.sh/blob/master/acme.sh `_json_encode` | `sed 's/"/\\"/g'` + `sed "s/\r/\\r/g"`，接著 **hex dump 把 `0a`→`5c 6e`（即換行→`\n`）** 再轉回 | POSIX sh | 已抽查：**agy 貼的片段不完整**（漏了 hex-dump 那行），因此「漏掉換行跳脫」的指控**不成立**；「漏掉 `\` 跳脫」與「其他控制字元未處理」**成立**。另 `sed "s/\r/..."` 依賴 GNU sed 對 `\r` 的擴充，非 POSIX |
| AWS Lambda custom runtime bootstrap 範例 | （agy 未附連結） | 硬編碼字串 | bash | 未抽查，無來源 |

補充（agy 未提，我自查）：docker-library 的 entrypoint 確實只用 `echo`/`printf` 純文字；沒有找到任何主流專案在 POSIX sh 內做完整 RFC 8259 跳脫的前例。

## 現成 logger 函式庫（名稱｜依賴｜跳脫完整度｜來源）

| 名稱 | 依賴 | 跳脫完整度（`"`、`\`、U+0000–001F） | 來源／抽查 |
|---|---|---|---|
| jo | C 二進位 | 完整 | https://github.com/jpmens/jo（未抽查，常識） |
| `jq -n --arg` | C 二進位 | 完整 | https://github.com/jqlang/jq（未抽查，常識） |
| Zordrak/bashlog | bash、`echo -e` | **零跳脫**：`printf '{"timestamp":"%s","level":"%s","message":"%s"}' ... ; echo -e "$json_line"` | https://github.com/Zordrak/bashlog/blob/master/log.sh — 已抽查，agy 片段屬實 |
| kward/log4sh | POSIX sh | 無 JSON 模式 | https://github.com/kward/log4sh（未抽查） |
| jsware/shlog | **bash**（README 自述 written in Bash；agy 說 POSIX sh，存疑） | 無 JSON 模式 | https://github.com/jsware/shlog — 已抽查 |
| plengauer/Thoth（前 opentelemetry-shell） | sh/dash/bash/busybox 皆支援，但需其 agent 套件 | 走 OTLP，非自製 JSON logger | https://github.com/plengauer/Thoth — 已抽查存在，README 明載 `TRACEPARENT` 「Extracted once at startup. Rewritten whenever a span is activated.」 |
| **kunitsucom/log.sh**（agy 漏掉，我自查） | 純 POSIX：printf/sed/tr | **不完整**：跳脫 `"`、`\r`、`\t`，用 `tr -d "[:cntrl:]"` 刪除其他控制字元，**不跳脫 `\`** | https://github.com/kunitsucom/log.sh — 已抽查：`_logshEscape() { printf %s "${1:-}" \| sed "s/\"/\\\"/g; s/\r/\\\r/g; s/\t/\\\t/g; s/$/\\\n/g" \| tr -d "[:cntrl:]" \| sed "s/\\\n$/\n/"; }` |
| stegard.net 作法 | jq coprocess | 完整（交給 jq） | https://stegard.net/2021/07/how-to-make-a-shell-script-log-json-messages/（自查，未細讀） |

結論：**沒有任何一個「純 POSIX、零依賴」的現成 logger 做到 RFC 8259 完整跳脫**；最接近的 log.sh 與 acme.sh 都漏 `\`。

## POSIX sh 最小跳脫的正確寫法（含 sed／tr 指令、常見錯誤、來源）

### agy 版實測結果（dash；`decisions/log/agy_escape_test.out`）
- `"`、`\n`、`\t`、`\r`、UTF-8、空字串：正確。
- **`\` 錯誤**：輸入 `a\b` 得到 `"a\\\\b"`（解碼成兩個反斜線）。原因：`s/\\/\\\\\\\\/g` 替換段 8 個反斜線 = 4 個字面反斜線。agy 在「常見錯誤 #2」聲稱 `s/\\/\\\\/g` 是 no-op，**這是錯的**：`s/\\/\\\\/g` 才是正確寫法（實測正確）。
- **`tr -d '[\001-\007\013\016-\037]'` 錯誤**：GNU/busybox tr 把 `[`、`]` 當字面字元，輸入 `a[b]c` 變成 `abc`（**資料遺失**）。
- 控制字元被靜默刪除而非 `\u00XX`（合法但有損）。

### 修正版（`decisions/log/json_escape_fixed.sh`，dash 與 busybox sh 15 個案例全部通過 python `json.loads` 與 `jq`）
```sh
_json_sed_script() {
  printf '%s\n' 's/\\/\\\\/g' 's/"/\\"/g'          # 反斜線必須第一個
  _i=1
  while [ "$_i" -le 31 ]; do
    case "$_i" in
      10) ;;                                          # \n 最後統一處理
      8)  _rep='\\b' ;; 9) _rep='\\t' ;; 12) _rep='\\f' ;; 13) _rep='\\r' ;;
      *)  _rep=$(printf '\\\\u%04x' "$_i") ;;         # 其餘 → \u00XX
    esac
    if [ "$_i" -ne 10 ]; then
      _byte=$(printf "\\$(printf '%03o' "$_i")")      # 用 printf 造出真實位元組
      printf 's/%s/%s/g\n' "$_byte" "$_rep"
    fi
    _i=$((_i + 1))
  done
  printf '%s\n' 's/\n/\\n/g'
}
JSON_SED_SCRIPT=$(_json_sed_script)   # 只算一次

json_escape() {
  _e=$(printf '%s\n' "$1" | sed -e ':a' -e '$!{' -e 'N' -e 'ba' -e '}' -e "$JSON_SED_SCRIPT"; printf x)
  _e=${_e%x}        # 哨兵保住結尾
  _e=${_e%\\n}      # 剝掉 printf '%s\n' 人為補的換行
  printf '%s' "$_e"
}
# 用法：printf '{"k":"%s"}\n' "$(json_escape "$v")"
```
要點：
1. `printf '%s\n'` 餵 sed（避免 incomplete last line 的未定義行為）；`:a; $!{N; ba}` 併行（BSD sed 需要分開 `-e`）。
2. 順序：`\` → `"` → 控制字元 → `\n`。
3. 全程 `printf '%s'`，不用 `echo`（`-n`、`\c` 問題）；實測 `-n foo` 正確。
4. 已知硬限制（agy 說法正確）：NUL 進不了 shell 變數；`$(...)` 吃掉結尾換行；BRE 沒有 `\xNN`。
5. 未處理：無效 UTF-8 位元組會原樣輸出（產生非法 JSON）；U+007F 與 U+2028/2029 依 RFC 8259 不必跳脫。

### 常見錯誤（agy 列的，已核對）
- 先跳脫 `"` 再跳脫 `\`（順序反）— 正確。
- 「`s/\\/\\\\/g` 是 no-op」— **錯**，見上。
- 用 `echo` 傳值 — 正確。
- 未併行導致 NDJSON 破行 — 正確。
- BSD sed 標籤語法 — 正確（未實測 BSD）。
- `$(...)` 吃結尾換行 — 正確。

來源：POSIX sed／tr／printf 規範 agy 未附 URL（可查 https://pubs.opengroup.org/onlinepubs/9699919799/utilities/sed.html 等）；RFC 8259 §7 https://www.rfc-editor.org/rfc/rfc8259#section-7（agy 未附）。

## 事件名註冊表前例

| 前例 | agy 說法 | 抽查 |
|---|---|---|
| Linux ftrace `available_events` | 純文字列舉合法事件名，寫入未註冊即錯 | 未抽查；與我認知相符，但這是 runtime 檢查非 CI |
| GitLab Internal Events | `config/events/*.yml`，CI 跑 `scripts/lint-events` | 已抽查文件：定義存於 `config/events`、`ee/config/events`，須符合 JSON Schema（https://docs.gitlab.com/development/internal_analytics/internal_event_instrumentation/event_definition_guide/）；runtime 對未定義事件 raise `UnknownEventError "Unknown event: #{event_name}"`（https://gitlab.com/gitlab-org/gitlab/-/issues/499632、/499826）。**`scripts/lint-events` 這個檔名未查到，存疑** |
| Mozilla Glean `metrics.yaml` + `glean_parser` | 未列舉即無法編譯 | 未抽查；glean_parser 產生型別安全 API 是事實，「純文字檔＋CI 驗證」概念相符 |
| Segment Typewriter／Avo | tracking plan + CI | 未抽查，無 URL |

agy 給的 CI 腳本（`grep -v '#' events.txt \| sort -u` vs `git grep -o 'log_event "..."' \| comm -23`）與 runtime `grep -Fqx -- "$event" events.txt` 都是合理的純 POSIX 作法（注意 `comm` 不在題目的可用工具清單內，CI 端可放寬）。

## trace_id 傳遞前例

| 前例 | 抽查 |
|---|---|
| OTel 規範「Environment Variables as Context Propagation Carriers」 | agy 給的 URL（api-propagators 頁面錨點）**不存在該節**。正確頁面是 https://opentelemetry.io/docs/specs/otel/context/env-carriers/ （狀態 Release Candidate）。該頁**沒有指定 `TRACEPARENT` 等變數名**，只規定鍵名正規化（大寫、非字母數字→`_`）並禁止實作自行 spawn 子行程；變數名由各 propagator 決定。`TRACEPARENT` 是 otel-cli／Thoth 的**事實標準**，不是規範定義 |
| equinix-labs/otel-cli `exec` | 已抽查 README：「propagates context via envvars so you can chain it to create child spans」、「if a traceparent envvar is set it will be automatically picked up and used by span and exec」；另有 `--tp-carrier` 檔案載體 |
| plengauer/Thoth | 已抽查：`TRACEPARENT` 啟動時擷取、span 啟用時改寫 |
| W3C traceparent 格式 `00-<32hex>-<16hex>-<2hex>` | https://www.w3.org/TR/trace-context/（agy 未附 URL） |

agy 的 POSIX 範例（`tr -dc '0-9a-f' </dev/urandom \| head -c 32`）注意：`head` 不在題目工具清單；可改 `dd bs=16 count=1 \| od`（但 od 也不在清單）——**trace_id 生成需要額外工具或由外層注入**，這點 agy 未指出。

## agy 推薦作法與理由

三層：(1) 校驗層——`grep -Fqx` 對 `events.txt` 白名單、讀取或生成 `TRACEPARENT`；(2) 跳脫層——tr 刪控制字元 + sed 跳脫；(3) 輸出層——單一 `printf` 寫一行 NDJSON。長期建議：若環境允許，改輸出 logfmt 交給 Vector/Fluent Bit 轉 JSON；CI 靜態擋未註冊事件名。

理由：主流專案都不在 shell 手寫 JSON，因為邊界條件多；但純 POSIX 下可行，前提是跳脫函式正確且只跑一次 sed。

我的評價：架構方向合理，但**其跳脫函式有兩個實測 bug**（反斜線變四個、`[]` 被刪），應採用上面的修正版；「先 tr 刪控制字元」改為 `\u00XX` 較無損。

## 我認為 agy 說法可疑或無來源的地方

1. **`s/\\/\\\\/g` 是 no-op、必須寫 8 個反斜線** — 錯誤，實測相反；agy 自己的函式因此輸出錯誤的雙反斜線。
2. **`tr -d '[\001-\007...]'`** — 方括號會被當字面字元刪掉，實測 `a[b]c`→`abc`。
3. **acme.sh 片段被截斷**：實際有 hex-dump 把換行轉 `\n`，agy「漏掉換行跳脫」的指控不成立（漏 `\` 成立）。
4. **OTel 規範連結錯**：api-propagators 頁沒有 env carrier 一節；正確頁 env-carriers 也**沒有定義 `TRACEPARENT` 變數名**。
5. **jsware/shlog 標為 POSIX sh** — README 自述 Bash。
6. **漏掉 kunitsucom/log.sh**（唯一自稱「零依賴 POSIX JSON logger」的現成品，且它也漏 `\`）。
7. 無來源／未驗證：AWS Lambda bootstrap 範例、GitLab `scripts/lint-events` 檔名、Glean、Segment/Avo、Linux available_events、log4sh、jo、jq（後三者屬常識）。
8. agy 推薦腳本用了 `head`、`cut`、`comm`、`/dev/urandom`，超出題目「只有 printf/grep/sed/tr/date」的限制，未標明。
9. Thoth 的「跳脫部分完整」評語無依據（agy 未讀其原始碼）。

============================================================
## 附件 D-1：base 的 log-events.txt 全文（來源：base repo `dist/script/docker/lib/log-events.txt`；decisions/log/base/ 下無此檔，改取 base_repo 副本）
============================================================
# log-events.txt - Registered body enum for _log_* (#423, #438).
#
# One event name per line. _log_* with an unregistered body is a fatal
# error (strict enforcement, #438). Adding a new event requires a
# same-PR addition here.

# setup.sh
env_regenerated
env_drift_detected
env_migrated_to_local
env_local_migration_conflict
setup_conf_migrated_to_root
setup_conf_migration_conflict
conf_parsed
conf_set
conf_added
conf_removed
conf_reset
conf_invalid_value
conf_key_not_found
conf_section_not_found
conf_unknown_subcmd
conf_unknown_arg
conf_upsert_file_missing
conf_local_created
conf_write_shadowed
config_components_provisioned
config_components_absent
config_files_unprovisioned
config_preset_selected
config_preset_dangling
deploy_local_override_refused
deploy_local_override_accepted
conf_upsert_newline_rejected
conf_upsert_mv_failed
conf_upsert_tmp_failed
conf_write_mv_failed
conf_write_tmp_failed
stage_baseline_collision
stage_reserved_tag
stage_invalid_format
stage_override_key_not_allowed
stage_unknown_referenced
gui_override_invalid
ssh_x11_no_xauth
ssh_x11_network_mismatch
xauth_rewrite_failed
xauth_empty_cookie
conf_image_name_default
conf_image_name_unknown
conf_runtime_key_deprecated
conf_no_repo_conf
conf_empty_repo_conf
conf_template_missing
conf_reset_aborted
conf_reset_needs_yes
conf_mount_stale_path
network_ports_inert
stage_devel_reserved
env_drift_detail
deploy_no_dockerfile
deploy_stage_not_deployable
deploy_needs_yes
deploy_aborted
deploy_failed
deploy_done
deploy_manifest_malformed
deploy_manifest_dup_basename
deploy_manifest_no_baked_default
deploy_stage_absent

# build.sh
build_started
build_bootstrap
build_drift_regen
build_prune_displaced
build_prune_skip_tagged
build_no_env
build_rerun_setup
build_test_tools_version_missing
build_verify_capture_failed
build_verify_step_unresolved
build_verify_no_steps
build_verify_all_cached
build_verify_partly_cached
build_verify_all_ran

# run.sh
run_started
run_bootstrap
run_drift_regen
run_already_running
run_no_env
run_build_image_missing
run_build_delegating
run_rerun_setup
run_build_invoking
run_detach_cmd_rejected

# exec.sh
exec_not_running

# stop.sh
stop_teardown
stop_no_containers
stop_prune_images
stop_prune_networks

# prune.sh
prune_buildx
prune_images
prune_networks
prune_volumes
prune_worktree_scan
prune_worktree_candidates
prune_worktree_none
prune_skip_bare
prune_skip_other_owner
prune_nothing_selected
prune_aborted
prune_volume_aborted
prune_no_workspace
prune_unknown_flag
prune_reclaim_failed

# lib/project_reclaim.sh - the scoped reclaim
reclaim_artifacts_unreadable
reclaim_containers_unreadable
reclaim_bad_grace
reclaim_bad_keep
reclaim_scan
reclaim_orphan_dry_run
reclaim_orphan_removed
reclaim_network_rm_failed
reclaim_image_scan
reclaim_image_dry_run
reclaim_image_removed
reclaim_image_rm_failed
reclaim_tool_tags_scan
reclaim_tool_tags_dry_run
reclaim_tool_tag_retired
reclaim_tool_tag_rm_failed
stop_reclaim_failed
ci_reclaim_failed

# script/test/test.sh - the previous run's residue on this project
ci_project_bad_wait
ci_project_wait_unreadable
ci_project_wait
ci_project_ready
ci_project_wedged

# hook.sh
hook_not_executable

# upgrade.sh
upgrade_started
upgrade_completed
upgrade_subtree_pull_failed
upgrade_version_bumped
upgrade_version_mismatch
upgrade_rollback
upgrade_rollback_failed

# init.sh
init_started
init_completed
init_missing_required_arg
init_progress
init_just_missing
init_bootstrap_just
init_failed
init_rollback
init_rollback_failed

# smoke_migrate.sh (repo-owned smoke tree layout; emitted under the init
# service because init.sh is the only caller)
smoke_tree_migrated
smoke_tree_migration_conflict

# gitignore.sh (managed .gitignore blocks; emitted under the init service
# because init.sh / upgrade.sh are the only callers)
gitignore_managed_block_invalid
gitignore_managed_block_migrated
gitignore_managed_block_orphans

# template_guard.sh (init/upgrade self-run guard)
base_self_run_refused

# test.sh
ci_apt_update_failed
ci_apt_install_failed
ci_bats_mock_clone_failed
ci_invalid_shard
ci_empty_shard
ci_no_docker_socket
ci_no_docker_cli
ci_unknown_option
ci_bats_path_not_found
ci_bats_path_system
ci_bats_path_coverage
ci_coverage_path_conflict
ci_coverage_evidence_not_erased
ci_coverage_local_conflict
ci_jobs_without_coverage_local
ci_invalid_coverage_jobs
ci_coverage_parallel_empty_slice
ci_coverage_slice_no_report
ci_coverage_merge_failed
ci_coverage_clean_absent
ci_coverage_cleaned
ci_coverage_not_reclaimed
ci_mixed_test_layout
ci_issueref_in_comment
ci_adr_numbering
ci_adr_structure
ci_stale_setup_conf_path
ci_readme_sync
ci_doc_counts
ci_catalog_description
ci_spec_repo_root
ci_home_literal
ci_arch_literal
ci_bash_source_guard
ci_early_close_reader
ci_errexit_bang
ci_derived_figures
ci_i18n_orphan
ci_self_hosted_guard
ci_tool_provenance
ci_changelog_entry
ci_changelog_layout
ci_pin_coverage
ci_action_ref_agreement
ci_generated_workflow_actions
ci_just_provenance
ci_shell_metrics
ci_nesting_depth
ci_function_length
ci_positional_params
ci_lint_bad_root
ci_no_hadolint
ci_lint_tool_without_lint
ci_unknown_lint_tool
ci_bad_lint_group
ci_lint_driver_failed
ci_lint_phase_failed
ci_lint_errexit_suppressed
ci_test_tools_dockerfile_missing
ci_project_name_digest_failed
ci_host_id_not_numeric
ci_handback_failed
ci_prev_release_progress
ci_prev_release_unavailable
ci_live_tree_residue

# transcript.sh (#606)
# Only genuine setup FAILURES are emitted via the logger (to stderr,
# pre-tee). Success meta-events (started / trace / complete / pruned) are
# written directly into the transcript file, never the terminal, so a run
# produces no extra on-screen output.
transcript_dir_create_failed
transcript_file_unwritable
transcript_tee_missing
transcript_env_invalid

# compose.sh (project-name resolution)
project_name_missing_from_env
project_name_unrecorded
project_name_reconfigured

# wrapper.sh (shared wrapper runtime). Emitted under the CALLING verb's
# tag (build / run), so the names carry no verb prefix of their own.
service_probe_failed
project_renamed
project_rename_write_failed
project_rename_deferred
project_rename_deferred_volumes
project_rename_probe_failed

# setup_tui.sh (the interactive editor). The list editors' screen labels
# are a table keyed by (section, prefix); a list with no complete row is
# a defect, not a default.
tui_list_labels_missing

# general
dry_run_cmd
summary_line
section_header
divider

============================================================
## 附件 D-2：base 的 log.sh 前 60 行（decisions/log/base/log.sh）
============================================================
#!/usr/bin/env bash
#
# log.sh - OTel-aligned 5-level logger.
#
# 5 functions: _log_debug, _log_info, _log_warn, _log_err, _log_fatal.
# API: _log_<level> <service> <body> [attr=val]...
#
# Single-sink tty-detect dispatch: text when fd is a TTY, JSON when
# piped/redirected. Override with LOG_FORMAT=auto|text|json.
# TTY-ness is resolved once at startup via _LOG_IS_TTY (0 = tty,
# non-zero = not) so a later transcript tee on fd1 cannot flip
# the format/color decision; when _LOG_IS_TTY is unset (standalone
# sourcing, e.g. test.sh) it falls back to live `test -t <fd>` and behaves
# exactly as before (ADR-00000007).
# Unregistered body (not in log-events.txt) is a fatal error.
#
# Stream routing (matches OTel severity mapping):
#   _log_debug / _log_info -> stdout
#   _log_warn / _log_err / _log_fatal -> stderr
#
# TRACEPARENT env (W3C Trace Context) propagation:
#   When set, trace_id and span_id are extracted and included in JSON.
#   Scoped wrappers: _log_with_trace / _log_with_span.
#
# Refs:    ADR-00000007, OTel Logs Data Model,
# W3C Trace Context.

if [[ -n "${_DOCKER_LIB_LOG_SOURCED:-}" ]]; then
  return 0
fi
_DOCKER_LIB_LOG_SOURCED=1

_LOG_LIB_DIR="$(dirname -- "${BASH_SOURCE[0]:-$0}")"
readonly _LOG_LIB_DIR
readonly _LOG_EVENTS_FILE="${_LOG_LIB_DIR}/log-events.txt"

# ── Event registry ─────────────────────────────────────────────────

_log_is_registered() {
  [[ -n "${1}" ]] && [[ "${1}" != \#* ]] && [[ -f "${_LOG_EVENTS_FILE}" ]] && \
    grep -Fxq "${1}" "${_LOG_EVENTS_FILE}" 2>/dev/null
}

# ── JSON helpers ───────────────────────────────────────────────────

_log_json_escape() {
  local s="${1}"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\t'/\\t}"
  s="${s//$'\r'/\\r}"
  printf '%s' "${s}"
}

_log_emit_json() {
  local severity_text="${1}"
  local severity_number="${2}"
  local service="${3}"
  local body="${4}"

warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
codex
# vendor_kit 執行紀錄事件集合 L6 審查報告

## 一、結論摘要

目前 L6 的方向可行，但不宜原樣定案。主要問題有六項：

1. **命名慣例混合**：同時出現 `launcher_start`、`resolve_finish`、`lock_acquired`、`file_created`、`registry_query`。建議統一為「名詞／對象＋過去式狀態」，例如 `launcher_started`、`resolve_completed`、`registry_query_failed`。
2. **只有開始、沒有結果的事件**：`engine_spawn`、`docker_extract`、`registry_query` 無法可靠表示失敗；`lock_acquired` 無法表示等待逾時。
3. **缺少重要失敗事件**：至少缺 registry 查詢失敗、pull 逾時的明確結果、lock 等待逾時、journal 恢復失敗、fingerprint 不符、引擎啟動失敗、prune 刪除失敗。
4. **`config_read` 無法精確表示 fallback**：應區分正常載入、缺檔／缺鍵使用預設、非法值退回預設、讀取或解析失敗。
5. **「完整原始 argv」與敏感值禁記互相衝突**：argv 可能含 URL userinfo、token、使用者名稱或未來新增的敏感參數。不能同時保證「逐字完整」及「憑證永不記」。
6. **缺少 invocation-level 模式欄位**：`dry_run`、`assume_yes`、`lock_disabled`、`ci` 應放在 `launcher_started`／`engine_started` 的共通 attributes；不必各自創事件。CI 只能記布林判定，不應記 `CI` 原值。

建議保留一次執行一檔、launcher/engine 共用 trace、事件註冊表 fail-fast，以及每個 resolve/apply 容器各自有開始與結束事件的設計。

---

## 二、與附件 D base 命名慣例的對照

### 實際觀察

附件 D 並不是完全一致的單一規則，但主流形式是：

- snake_case；
- 名詞或領域對象在前；
- 結果／狀態在後；
- 已發生事件常用過去式或結果詞：
  - `build_started`
  - `upgrade_completed`
  - `env_regenerated`
  - `conf_invalid_value`
  - `deploy_failed`
  - `reclaim_orphan_removed`
  - `transcript_file_unwritable`

base 也有現在式名詞或動作縮寫，如 `reclaim_scan`、`summary_line`、`dry_run_cmd`，因此不能說它嚴格限定「名詞＋過去式」。但對生命週期與稽核結果而言，**名詞／對象＋過去式結果**確實是最清楚、也最接近 base 主流的形式。

### 建議規則

採用：

```text
<object>_<past-tense-result>
```

例如：

- `launcher_started`
- `docker_pull_completed`
- `docker_pull_failed`
- `lock_wait_timed_out`
- `journal_recovered`
- `file_appended`
- `engine_failed`

不建議：

- 動詞在前的 `resolve_finish`
- 非過去式的 `launcher_start`
- 語意同時包含開始與結果的單一 `registry_query`
- `finish`；建議一律用 `completed`
- 把所有異常塞進正常事件的 `result`／`reason`

`prompt_asked`、`prompt_answered`、`file_created` 等現有名稱已符合建議規則。

---

## 三、現有事件逐項審查

### Launcher 事件

| 現有事件 | 判定 | 建議 |
|---|---|---|
| `launcher_start` | 必要，但命名不一致 | 改 `launcher_started` |
| `config_read` | 必要，但語意過寬 | 拆成 `config_loaded`、`config_defaulted`、`config_invalid`；真正無法讀／解析則 `config_read_failed` |
| `docker_pull_start` | 必要 | 改 `docker_pull_started` |
| `docker_pull_finish` | 必要，但成功與失敗混在一起 | 拆成 `docker_pull_completed`、`docker_pull_failed`；逾時另用 `docker_pull_timed_out` |
| `docker_extract` | 必要，但沒有結果語意 | 改 `docker_extract_completed`，增加 `docker_extract_failed` |
| `engine_spawn` | 必要，但「run 前」其實尚未 spawn | 若記呼叫前，叫 `engine_spawn_started`；另加 `engine_spawned`／`engine_spawn_failed` |
| `sync_fast_path` | 必要 | 建議拆為 `sync_fast_path_selected`／`sync_fast_path_skipped`；或保留單一事件加 `result`，但前者較易查詢 |
| `log_prune` | 必要 | 改 `log_pruned`，另加 `log_prune_failed` |
| `launcher_exit` | 必要 | 建議拆 `launcher_completed`／`launcher_failed`；若重視固定最後一筆，也可保留單一 `launcher_exited` |

### Engine 事件

| 現有事件 | 判定 | 建議 |
|---|---|---|
| `engine_start` | 必要 | 改 `engine_started` |
| `journal_detected` | 必要 | 保留；增加 journal 所屬原始 verb/trace，不要只記本次 verb |
| `journal_recovered` | 必要 | 保留；增加 `journal_recovery_started`、`journal_recovery_failed` |
| `resolve_finish` | 必要 | 改 `resolve_completed`；增加 `resolve_failed` |
| `lock_acquired` | 必要 | 保留；增加 `lock_wait_started`、`lock_wait_timed_out`，或至少增加 timeout 事件 |
| `fingerprint_verified` | 必要 | 保留；增加 `fingerprint_mismatched` 或 `fingerprint_verification_failed` |
| `journal_created` | 必要 | 保留；寫失敗通常會終止，仍建議 `journal_create_failed` |
| `journal_deleted` | 必要 | 保留；刪除失敗應有 `journal_delete_failed` |
| `prompt_asked` | 必要 | 保留 |
| `prompt_answered` | 必要 | 保留 |
| `file_created` | 必要 | 保留 |
| `file_modified` | 必要 | 保留 |
| `file_appended` | 必要 | 保留，但不能只記 `lines` |
| `file_deleted` | 必要 | 保留 |
| `merge_conflict` | 必要 | 改 `merge_conflict_detected` |
| `declined` | 太含糊 | 改 `file_change_declined` 或 `merge_declined`，依實際語意；目前「declined_hash」文字與 attributes 表也不一致 |
| `version_written` | 必要 | 保留 |
| `registry_query` | 必要，但缺開始／失敗語意 | 拆成 `registry_query_started`、`registry_query_completed`、`registry_query_failed`；若有硬 timeout，再加 `registry_query_timed_out` |
| `prune_candidate` | 可用，但屬細節 | 改 `prune_candidate_identified`，建議 DEBUG |
| `prune_removed` | 必要 | 保留；增加 `prune_remove_failed` |
| `engine_exit` | 必要 | 建議 `engine_completed`／`engine_failed`；或固定最後一筆用 `engine_exited` |

---

## 四、缺口與特殊情境

### 1. Registry 查詢失敗

現有 `registry_query(result=...)` technically 可以承載，但不利於：

- 用 event_name 篩選錯誤；
- 直接依事件配置 severity；
- 分辨 registry 回覆「不存在」和網路／認證／timeout；
- 確認查詢是否根本沒有完成。

建議至少有：

- `registry_query_started`
- `registry_query_completed`
- `registry_query_failed`
- `registry_query_timed_out`：只有實作確有獨立 timeout 才需要；不確定目前 registry query 是否有 timeout 設定。

`not_found` 是否為 ERROR 取決於語境：若查詢的目的就是判斷 tag 是否存在，not found 可能是正常結果，應為 INFO；若規格要求該 artifact 必須存在，則為 ERROR。

### 2. Docker pull 逾時

不能只靠：

```json
{"event_name":"docker_pull_finish","reason":"timeout"}
```

建議獨立成 `docker_pull_timed_out`，severity 為 ERROR，必填：

- `ref`
- `timeout_ms`
- `duration_ms`
- `exit_code`，若 wrapper 有可靠取得
- `message_id`：6-24 或 6-31
- `attempt`

若有 retry，再加 `attempt`／`max_attempts`；不確定目前是否會 retry。

### 3. Lock 等待逾時及關閉鎖

增加：

- `lock_wait_started`：INFO 或 DEBUG
- `lock_acquired`：INFO
- `lock_wait_timed_out`：ERROR
- `lock_disabled`：WARN

`VENDOR_KIT_NO_LOCK` 不應只默默放在 `engine_started.lock_disabled=true`；它會削弱一致性保證，建議另寫一次 WARN `lock_disabled`。但環境變數的原始值不可記，只記解析後布林值及來源 `source="environment"`。

### 4. Config 退回預設

建議區分：

- 缺檔、缺鍵：`config_defaulted`，INFO；
- 重複鍵、非正整數、格式非法：`config_invalid`，WARN；
- 檔案存在但權限／I/O／TOML parser 錯誤，且操作不可安全繼續：`config_read_failed`，ERROR。

`source=file|default` 不足以回答「為何 default」。增加：

- `default_reason`: `file_missing|key_missing|invalid_value|duplicate_key|parse_error`
- `invalid_keys`
- `keep`
- `days`

不應把原始非法值完整記錄；它現在是整數欄位，風險低，但採通用規則仍建議只記欄位名及錯誤類別。

### 5. Journal 恢復

建議完整生命週期：

- `journal_detected`
- `journal_recovery_started`
- `journal_recovered`
- `journal_recovery_failed`

唯讀動詞偵測後依規格結束的情況，只需：

- `journal_detected`，WARN；
- `engine_failed`，ERROR，`message_id=6-33`。

`help` 仍回 0，故最後應是 `engine_completed`，但 `journal_detected` 仍可 WARN。

### 6. Dry-run

不必為 invocation 增設一般性的 `dry_run_started`。建議：

- `launcher_started.dry_run=true`
- `engine_started.dry_run=true`
- prune 每個候選用 `prune_candidate_identified`
- 若要清楚表明「本來會刪但因 dry-run 未刪」，增加 `prune_removal_simulated`

後者比把 `prune_removed` 加 `dry_run=true` 更安全，避免被誤認為已刪除。可沿用 base 的 `dry_run_cmd` 命名精神，但 `prune_removal_simulated` 的領域語意更精確。

### 7. 每檔 append 行細節

`file_appended.lines` 不足，因為：

- 可能 append 零行但若干 bytes；
- 最後一行有無 LF 會影響實際行數；
- 同一檔可能多次 append；
- 敏感內容不可記。

建議必填：

- `path`
- `bytes_written`
- `lines_added`
- `newline_added`
- `strategy`
- `content_kind`，例如 `gitignore_entry|dockerignore_entry|config_block`

選填：

- `before_digest`
- `after_digest`

digest 建議只用於非敏感專案管理檔；不得對 token file 或可能含秘密的任意檔案計算並記錄可離線比對的 digest。不可記實際 appended content。

`action` 在 `file_appended` 內是重複資訊，應刪除；event_name 已表達 action。

### 8. CI 模式

不需要獨立事件。記：

```json
"ci": true
```

即可，而且只記解析後布林值：

- `CI` 未設定或被規格判為 false → `false`
- 其他判定為 CI → `true`

附件寫「CI 真值」仍有歧義：如果指原始環境字串，就可能洩漏資訊，也不利於穩定查詢。建議規格明訂為 boolean。如何把 `CI=""`、`CI="false"` 判定為真假目前不確定，需由 CI 模組規格唯一化，但不能在 log 中保留原始值。

---

## 五、Attributes 共通規則

### 每筆必填

所有事件均應包含：

| attribute | 規則 |
|---|---|
| `component` | `launcher` 或 `engine` |
| `verb` | 正規化後的頂層動詞；bootstrap 為 `bootstrap` |
| `phase` | launcher 可用 `launch`；engine 為 `resolve`／`apply`／`single` |
| `invocation_id` | 可省略，因已由頂層 `trace_id` 表達；不應重複 |
| `dry_run` | 建議只在 start 事件必填，其餘事件透過同 trace 關聯 |
| `ci` | 建議只在 start 事件必填 |
| `assume_yes` | 建議只在 start 事件必填 |
| `lock_disabled` | engine start 必填 |

`verb` 已經是全事件共通 attribute，不需要在各事件的「主要 attributes」再重複列為事件專屬要求。

### 時間與結果

- 所有完成、失敗、timeout 事件：`duration_ms` 必填。
- 所有失敗事件：
  - `error_kind` 必填，使用有限 enum；
  - `message_id` 若有對應 6-xx，必填；
  - `exit_code` 若來自外部程序且可靠取得，必填；
  - `error_detail` 選填且必須去敏。
- 不建議自由文字 `reason` 作為唯一機器欄位；改用 enum `reason_code`，人讀內容放 `body`。

### 路徑

`cwd`、`path` 可能洩漏：

- 使用者名稱；
- 客戶／專案名稱；
- 主機目錄布局。

建議：

- 專案內檔案一律記 repo-relative path；
- `cwd` 改為 `repo_root="."` 或省略；
- 若確實需要辨識 repo，可記不具可逆性的 repo identifier，但未必必要；
- container 內暫存路徑應正規化為 repo-relative；
- 不記 `$HOME` 展開後的絕對路徑。

因此附件範例中的：

```json
"cwd":"/home/me/<專案根>"
```

不建議保留。

### argv 的重大衝突

建議撤銷「不論合法與否，完整原始 argv」要求，改成：

- `argv_redacted`：逐項保留結構，但對敏感參數值與 URL userinfo 做遮蔽；
- `argv_count`；
- `argv_redacted_fields`：只列被遮蔽的參數類型，不列原值；
- 非法 argv 也照記，但仍經相同 redaction。

例如：

```json
{
  "argv_redacted": [
    "add",
    "https://***@registry.example/repo",
    "--token",
    "[REDACTED]"
  ],
  "argv_redacted_fields": ["url_userinfo", "token_argument"]
}
```

如果 vendor_kit 可形式化保證 CLI 永遠不接受秘密參數，仍無法阻止 URL userinfo，因此至少 URL 必須先清洗。

### 明確禁止記錄

禁止出現在任何欄位，包括 `body`、`summary`、`error_detail`、`argv`：

- `VENDOR_KIT_REGISTRY_TOKEN`
- `VENDOR_KIT_REGISTRY_USER`
- `VENDOR_KIT_REGISTRY_TOKEN_FILE` 的內容
- token file 內容或可辨識摘要
- URL userinfo
- `Authorization`、Cookie、Docker credential helper 回覆
- `docker login` stdout/stderr
- 完整環境變數表
- registry HTTP request/response headers
- subprocess 原始 stderr，除非經明確結構化清洗
- journal 內容
- 被寫入檔案的完整內容

`summary` 也必須是結構化 object 或由固定模板產生；任意拼接 subprocess output 風險太高。

---

## 六、Severity 建議

### 原則

| 情況 | Severity |
|---|---|
| 正常生命週期、已完成動作 | `INFO` |
| 高頻診斷資訊、候選清單 | `DEBUG` |
| 可恢復異常、fallback、使用者拒絕、best-effort 失敗 | `WARN` |
| 本階段／本次操作失敗 | `ERROR` |
| 程式不變量破壞、未註冊事件、logger 本身不可用 | `FATAL` |

`FATAL` 不應用於普通 pull、registry、merge 或使用者輸入失敗。未註冊 event_name 是程式缺陷，使用 FATAL 合理。

log 檔本身無法寫時，`6-38` 只能輸出到 stderr；不能期待把這個 FATAL 記進同一個不可寫的 log。若是「後續 append 失敗」，現有檔案也可能只留下最後一個成功事件。

---

## 七、最終建議事件清單

下表採較嚴格、可查詢的結果型事件。`component`、`verb`、engine 的 `phase` 視為所有事件共同必填，表內不重複列出。

### Launcher

| event_name | 寫者 | severity | 必填 attributes | 何時 |
|---|---|---:|---|---|
| `launcher_started` | launcher | INFO | `argv_redacted`, `launcher_version`, `engine_ref`, `ci`, `dry_run`, `assume_yes` | log 建立成功後第一筆 |
| `config_loaded` | launcher | INFO | `keep`, `days`, `source="file"` | 成功讀取有效 config |
| `config_defaulted` | launcher | INFO | `keep`, `days`, `default_reason` | 缺檔或缺鍵，採預設 |
| `config_invalid` | launcher | WARN | `invalid_keys`, `defaulted_keys`, `keep`, `days`, `message_id`（若有） | 非法／重複值，對相關鍵採預設 |
| `config_read_failed` | launcher | ERROR | `error_kind`, `message_id`, `path` | config 存在但無法讀取或解析，且操作終止 |
| `docker_pull_started` | launcher | INFO | `ref`, `attempt`, `timeout_ms` | 每次 docker pull 前 |
| `docker_pull_completed` | launcher | INFO | `ref`, `digest`, `duration_ms`, `attempt` | pull 成功 |
| `docker_pull_failed` | launcher | ERROR | `ref`, `duration_ms`, `attempt`, `error_kind`, `exit_code`, `message_id` | pull 非 timeout 失敗 |
| `docker_pull_timed_out` | launcher | ERROR | `ref`, `duration_ms`, `timeout_ms`, `attempt`, `message_id` | pull 超過 `VENDOR_KIT_PULL_TIMEOUT` |
| `docker_extract_completed` | launcher | INFO | `repo`, `ref`, `path`, `duration_ms` | create/cp/rm 組成的 extract 全部成功 |
| `docker_extract_failed` | launcher | ERROR | `repo`, `ref`, `path`, `operation`, `error_kind`, `duration_ms`, `message_id` | extract 任一步失敗 |
| `engine_spawn_started` | launcher | INFO | `engine_ref`, `subcommand`, `interactive` | 執行 docker run 前 |
| `engine_spawned` | launcher | INFO | `engine_ref`, `subcommand`, `duration_ms` | 容器已成功開始執行；精確判定點不確定，需依 docker run 封裝方式定義 |
| `engine_spawn_failed` | launcher | ERROR | `engine_ref`, `subcommand`, `error_kind`, `exit_code`, `duration_ms`, `message_id` | docker 未能啟動引擎 |
| `sync_fast_path_selected` | launcher | INFO | `reason_code` | sync 命中快路徑 |
| `sync_fast_path_skipped` | launcher | DEBUG | `reason_code` | 快路徑不適用，包括 CI 模式 |
| `log_pruned` | launcher | INFO | `deleted_count`, `keep`, `days`, `duration_ms` | 保留清理成功；即使刪除零檔也可記 |
| `log_prune_failed` | launcher | WARN | `deleted_count`, `keep`, `days`, `error_kind`, `duration_ms` | best-effort 清理未完整成功 |
| `launcher_completed` | launcher | INFO | `exit_code=0`, `duration_ms` | 啟動器成功結束，最後一筆 |
| `launcher_failed` | launcher | ERROR | `exit_code`, `duration_ms`, `reason_code`, `message_id`（若有） | 啟動器非零結束，最後一筆 |

`launcher_completed`／`launcher_failed` 若因 trap 實作複雜而不方便分流，可合併為 `launcher_exited`，依 `exit_code` 動態給 INFO/ERROR；但不要再使用 `launcher_exit`。

### Engine

| event_name | 寫者 | severity | 必填 attributes | 何時 |
|---|---|---:|---|---|
| `engine_started` | engine | INFO | `argv_redacted`, `subcommand`, `engine_version`, `protocol`, `ci`, `dry_run`, `assume_yes`, `lock_disabled` | 每個 resolve/apply/single 容器第一筆 |
| `journal_detected` | engine | WARN | `path`, `journal_id`, `journal_verb`, `journal_state` | 發現未完成交易 |
| `journal_recovery_started` | engine | INFO | `path`, `journal_id`, `journal_verb`, `operation_count` | 可寫動詞開始恢復 |
| `journal_recovered` | engine | INFO | `path`, `journal_id`, `actions_reverted`, `duration_ms` | 恢復成功 |
| `journal_recovery_failed` | engine | ERROR | `path`, `journal_id`, `failed_action`, `error_kind`, `duration_ms`, `message_id` | 恢復失敗 |
| `resolve_completed` | engine | INFO | `plan_summary`, `apply_required`, `fingerprint`, `duration_ms` | resolve 成功完成 |
| `resolve_failed` | engine | ERROR | `error_kind`, `duration_ms`, `message_id` | resolve 失敗 |
| `lock_wait_started` | engine | DEBUG | `lock_path`, `timeout_ms` | apply 開始等待 flock |
| `lock_acquired` | engine | INFO | `lock_path`, `wait_ms` | 成功取得 flock |
| `lock_wait_timed_out` | engine | ERROR | `lock_path`, `wait_ms`, `timeout_ms`, `message_id` | 等待鎖逾時 |
| `lock_disabled` | engine | WARN | `source="environment"` | `VENDOR_KIT_NO_LOCK` 生效；每個 apply 最多一次 |
| `fingerprint_verified` | engine | INFO | `fingerprint` | apply 重驗與 resolve 相符 |
| `fingerprint_mismatched` | engine | ERROR | `expected_fingerprint`, `actual_fingerprint`, `message_id` | apply 重驗不符而停止 |
| `journal_created` | engine | INFO | `path`, `journal_id`, `operation_count` | 第一個實際寫入前建 journal |
| `journal_create_failed` | engine | ERROR | `path`, `error_kind`, `message_id` | journal 無法建立，禁止進入寫入 |
| `journal_deleted` | engine | INFO | `path`, `journal_id` | 成功完成後刪除 journal |
| `journal_delete_failed` | engine | ERROR | `path`, `journal_id`, `error_kind`, `message_id` | 成功操作後無法刪 journal；是否改整體 exit code 需由交易規格定義，不確定 |
| `prompt_asked` | engine | INFO | `message_id`, `prompt_kind`, `path`（適用時） | 印出 6-20/21/22/32/34 問句 |
| `prompt_answered` | engine | INFO | `message_id`, `answer`, `auto` | 得到 yes/no/eof；`auto=true` 表 `-y` |
| `file_created` | engine | INFO | `path`, `strategy`, `bytes_written` | 實際建立專案檔 |
| `file_modified` | engine | INFO | `path`, `strategy`, `bytes_written` | 實際修改或原子替換專案檔 |
| `file_appended` | engine | INFO | `path`, `strategy`, `bytes_written`, `lines_added`, `newline_added`, `content_kind` | 每個檔案每次實際 append 完成 |
| `file_deleted` | engine | INFO | `path`, `strategy` | 實際刪除專案檔 |
| `merge_conflict_detected` | engine | WARN | `path`, `merge_kind`, `message_id`（若有） | 三方合併產生需使用者決定的衝突 |
| `file_change_declined` | engine | INFO | `path`, `change_kind`, `state` | 使用者拒絕提議的檔案變更 |
| `version_written` | engine | INFO | `path`, `changed_keys`, `engine_ref` | 寫入 version.toml |
| `registry_query_started` | engine | DEBUG | `host`, `repo`, `query_kind` | 發出 registry 查詢前 |
| `registry_query_completed` | engine | INFO | `host`, `repo`, `query_kind`, `result`, `duration_ms`, `digest`（適用時） | 查詢正常完成，含正常的 not-found |
| `registry_query_failed` | engine | ERROR | `host`, `repo`, `query_kind`, `error_kind`, `duration_ms`, `message_id` | 認證、網路、協定或主機錯誤 |
| `registry_query_timed_out` | engine | ERROR | `host`, `repo`, `query_kind`, `timeout_ms`, `duration_ms`, `message_id` | registry 查詢有明確 timeout 且逾時；目前是否需要此機制不確定 |
| `prune_candidate_identified` | engine | DEBUG | `kind`, `object_id`, `reason_code` | 判定為 prune 候選 |
| `prune_removal_simulated` | engine | INFO | `kind`, `object_id`, `reason_code` | `--dry-run` 下本來會刪除 |
| `prune_removed` | engine | INFO | `kind`, `object_id`, `duration_ms` | 成功刪除候選 |
| `prune_remove_failed` | engine | WARN 或 ERROR | `kind`, `object_id`, `error_kind`, `duration_ms` | 單一候選刪除失敗；是否 ERROR 取決於 prune 是否允許部分成功 |
| `engine_completed` | engine | INFO | `exit_code=0`, `duration_ms`, `summary` | 子命令成功，該容器最後一筆 |
| `engine_failed` | engine | ERROR | `exit_code`, `duration_ms`, `reason_code`, `message_id`, `summary` | 子命令失敗，該容器最後一筆 |

---

## 八、可刪除或合併的重複資訊

建議刪除以下重複 attributes：

- `file_created.action=create`
- `file_modified.action=modify`
- `file_appended.action=append`
- `file_deleted.action=delete`
- `launcher_started.verb`／`engine_started.verb` 在表中特別列出，因其本來就是所有事件共通欄位
- `journal_created.id` 若只是頂層 `trace_id` 的重複值；改名 `journal_id`，並只在可能指向舊交易時記錄
- `prompt` 若內容就是 `body` 的重複文字；attributes 改記穩定的 `prompt_kind`，實際本地化句子留在 `body`
- `log_prune.error` 自由文字；改成獨立 `log_prune_failed` 加有限 enum `error_kind`
- `launcher_exit.reason` 自由文字；改成 `reason_code`

---

## 九、最終定案建議

1. 採用 snake_case、`object_past_tense`。
2. 全面改：
   - `*_start` → `*_started`
   - `*_finish` → `*_completed`
   - `*_exit` → `*_completed`／`*_failed`，或退而求其次用 `*_exited`
3. 外部操作至少應有 completed/failed；有硬 timeout 者另有 timed_out。
4. `config_read` 拆分正常、預設、非法及讀取失敗。
5. 增加 lock timeout、journal recovery failure、fingerprint mismatch、engine spawn failure、prune removal failure。
6. `dry_run`、`ci`、`assume_yes`、`lock_disabled` 納入 start 事件；其中 `lock_disabled` 再發 WARN。
7. dry-run 不得寫成 `prune_removed`；使用 `prune_removal_simulated`。
8. per-file append 記 bytes/lines/newline/content_kind，不記實際內容。
9. argv 必須改為 redacted argv；「完整原始 argv」要求應撤回。
10. 所有路徑盡量 repo-relative；不記完整 cwd。
11. `FATAL` 僅保留給未註冊事件、logger 不變量破壞及無法建立必要 audit log；業務失敗使用 ERROR。
12. release CI 除驗證 launcher 白名單是 registry 子集，還應驗證：
    - 所有程式碼中的靜態 event_name 都已註冊；
    - registry 無重複名稱；
    - event_name 符合 `^[a-z][a-z0-9_]*$`；
    - 不再使用 `_start`、`_finish`、`_exit` 等舊後綴；
    - launcher 只能發出其內嵌子集中的事件。

整體而言，L6 不需要追求每一個內部步驟都有事件；應優先確保「每個外部副作用、決策、等待、fallback 與失敗都有可機器查詢的結果事件」。這會比把大量不同結果塞進單一 `result` 或 `reason` attribute 更適合 audit、lnav 與後續相容性。
tokens used
31,485
# vendor_kit 執行紀錄事件集合 L6 審查報告

## 一、結論摘要

目前 L6 的方向可行，但不宜原樣定案。主要問題有六項：

1. **命名慣例混合**：同時出現 `launcher_start`、`resolve_finish`、`lock_acquired`、`file_created`、`registry_query`。建議統一為「名詞／對象＋過去式狀態」，例如 `launcher_started`、`resolve_completed`、`registry_query_failed`。
2. **只有開始、沒有結果的事件**：`engine_spawn`、`docker_extract`、`registry_query` 無法可靠表示失敗；`lock_acquired` 無法表示等待逾時。
3. **缺少重要失敗事件**：至少缺 registry 查詢失敗、pull 逾時的明確結果、lock 等待逾時、journal 恢復失敗、fingerprint 不符、引擎啟動失敗、prune 刪除失敗。
4. **`config_read` 無法精確表示 fallback**：應區分正常載入、缺檔／缺鍵使用預設、非法值退回預設、讀取或解析失敗。
5. **「完整原始 argv」與敏感值禁記互相衝突**：argv 可能含 URL userinfo、token、使用者名稱或未來新增的敏感參數。不能同時保證「逐字完整」及「憑證永不記」。
6. **缺少 invocation-level 模式欄位**：`dry_run`、`assume_yes`、`lock_disabled`、`ci` 應放在 `launcher_started`／`engine_started` 的共通 attributes；不必各自創事件。CI 只能記布林判定，不應記 `CI` 原值。

建議保留一次執行一檔、launcher/engine 共用 trace、事件註冊表 fail-fast，以及每個 resolve/apply 容器各自有開始與結束事件的設計。

---

## 二、與附件 D base 命名慣例的對照

### 實際觀察

附件 D 並不是完全一致的單一規則，但主流形式是：

- snake_case；
- 名詞或領域對象在前；
- 結果／狀態在後；
- 已發生事件常用過去式或結果詞：
  - `build_started`
  - `upgrade_completed`
  - `env_regenerated`
  - `conf_invalid_value`
  - `deploy_failed`
  - `reclaim_orphan_removed`
  - `transcript_file_unwritable`

base 也有現在式名詞或動作縮寫，如 `reclaim_scan`、`summary_line`、`dry_run_cmd`，因此不能說它嚴格限定「名詞＋過去式」。但對生命週期與稽核結果而言，**名詞／對象＋過去式結果**確實是最清楚、也最接近 base 主流的形式。

### 建議規則

採用：

```text
<object>_<past-tense-result>
```

例如：

- `launcher_started`
- `docker_pull_completed`
- `docker_pull_failed`
- `lock_wait_timed_out`
- `journal_recovered`
- `file_appended`
- `engine_failed`

不建議：

- 動詞在前的 `resolve_finish`
- 非過去式的 `launcher_start`
- 語意同時包含開始與結果的單一 `registry_query`
- `finish`；建議一律用 `completed`
- 把所有異常塞進正常事件的 `result`／`reason`

`prompt_asked`、`prompt_answered`、`file_created` 等現有名稱已符合建議規則。

---

## 三、現有事件逐項審查

### Launcher 事件

| 現有事件 | 判定 | 建議 |
|---|---|---|
| `launcher_start` | 必要，但命名不一致 | 改 `launcher_started` |
| `config_read` | 必要，但語意過寬 | 拆成 `config_loaded`、`config_defaulted`、`config_invalid`；真正無法讀／解析則 `config_read_failed` |
| `docker_pull_start` | 必要 | 改 `docker_pull_started` |
| `docker_pull_finish` | 必要，但成功與失敗混在一起 | 拆成 `docker_pull_completed`、`docker_pull_failed`；逾時另用 `docker_pull_timed_out` |
| `docker_extract` | 必要，但沒有結果語意 | 改 `docker_extract_completed`，增加 `docker_extract_failed` |
| `engine_spawn` | 必要，但「run 前」其實尚未 spawn | 若記呼叫前，叫 `engine_spawn_started`；另加 `engine_spawned`／`engine_spawn_failed` |
| `sync_fast_path` | 必要 | 建議拆為 `sync_fast_path_selected`／`sync_fast_path_skipped`；或保留單一事件加 `result`，但前者較易查詢 |
| `log_prune` | 必要 | 改 `log_pruned`，另加 `log_prune_failed` |
| `launcher_exit` | 必要 | 建議拆 `launcher_completed`／`launcher_failed`；若重視固定最後一筆，也可保留單一 `launcher_exited` |

### Engine 事件

| 現有事件 | 判定 | 建議 |
|---|---|---|
| `engine_start` | 必要 | 改 `engine_started` |
| `journal_detected` | 必要 | 保留；增加 journal 所屬原始 verb/trace，不要只記本次 verb |
| `journal_recovered` | 必要 | 保留；增加 `journal_recovery_started`、`journal_recovery_failed` |
| `resolve_finish` | 必要 | 改 `resolve_completed`；增加 `resolve_failed` |
| `lock_acquired` | 必要 | 保留；增加 `lock_wait_started`、`lock_wait_timed_out`，或至少增加 timeout 事件 |
| `fingerprint_verified` | 必要 | 保留；增加 `fingerprint_mismatched` 或 `fingerprint_verification_failed` |
| `journal_created` | 必要 | 保留；寫失敗通常會終止，仍建議 `journal_create_failed` |
| `journal_deleted` | 必要 | 保留；刪除失敗應有 `journal_delete_failed` |
| `prompt_asked` | 必要 | 保留 |
| `prompt_answered` | 必要 | 保留 |
| `file_created` | 必要 | 保留 |
| `file_modified` | 必要 | 保留 |
| `file_appended` | 必要 | 保留，但不能只記 `lines` |
| `file_deleted` | 必要 | 保留 |
| `merge_conflict` | 必要 | 改 `merge_conflict_detected` |
| `declined` | 太含糊 | 改 `file_change_declined` 或 `merge_declined`，依實際語意；目前「declined_hash」文字與 attributes 表也不一致 |
| `version_written` | 必要 | 保留 |
| `registry_query` | 必要，但缺開始／失敗語意 | 拆成 `registry_query_started`、`registry_query_completed`、`registry_query_failed`；若有硬 timeout，再加 `registry_query_timed_out` |
| `prune_candidate` | 可用，但屬細節 | 改 `prune_candidate_identified`，建議 DEBUG |
| `prune_removed` | 必要 | 保留；增加 `prune_remove_failed` |
| `engine_exit` | 必要 | 建議 `engine_completed`／`engine_failed`；或固定最後一筆用 `engine_exited` |

---

## 四、缺口與特殊情境

### 1. Registry 查詢失敗

現有 `registry_query(result=...)` technically 可以承載，但不利於：

- 用 event_name 篩選錯誤；
- 直接依事件配置 severity；
- 分辨 registry 回覆「不存在」和網路／認證／timeout；
- 確認查詢是否根本沒有完成。

建議至少有：

- `registry_query_started`
- `registry_query_completed`
- `registry_query_failed`
- `registry_query_timed_out`：只有實作確有獨立 timeout 才需要；不確定目前 registry query 是否有 timeout 設定。

`not_found` 是否為 ERROR 取決於語境：若查詢的目的就是判斷 tag 是否存在，not found 可能是正常結果，應為 INFO；若規格要求該 artifact 必須存在，則為 ERROR。

### 2. Docker pull 逾時

不能只靠：

```json
{"event_name":"docker_pull_finish","reason":"timeout"}
```

建議獨立成 `docker_pull_timed_out`，severity 為 ERROR，必填：

- `ref`
- `timeout_ms`
- `duration_ms`
- `exit_code`，若 wrapper 有可靠取得
- `message_id`：6-24 或 6-31
- `attempt`

若有 retry，再加 `attempt`／`max_attempts`；不確定目前是否會 retry。

### 3. Lock 等待逾時及關閉鎖

增加：

- `lock_wait_started`：INFO 或 DEBUG
- `lock_acquired`：INFO
- `lock_wait_timed_out`：ERROR
- `lock_disabled`：WARN

`VENDOR_KIT_NO_LOCK` 不應只默默放在 `engine_started.lock_disabled=true`；它會削弱一致性保證，建議另寫一次 WARN `lock_disabled`。但環境變數的原始值不可記，只記解析後布林值及來源 `source="environment"`。

### 4. Config 退回預設

建議區分：

- 缺檔、缺鍵：`config_defaulted`，INFO；
- 重複鍵、非正整數、格式非法：`config_invalid`，WARN；
- 檔案存在但權限／I/O／TOML parser 錯誤，且操作不可安全繼續：`config_read_failed`，ERROR。

`source=file|default` 不足以回答「為何 default」。增加：

- `default_reason`: `file_missing|key_missing|invalid_value|duplicate_key|parse_error`
- `invalid_keys`
- `keep`
- `days`

不應把原始非法值完整記錄；它現在是整數欄位，風險低，但採通用規則仍建議只記欄位名及錯誤類別。

### 5. Journal 恢復

建議完整生命週期：

- `journal_detected`
- `journal_recovery_started`
- `journal_recovered`
- `journal_recovery_failed`

唯讀動詞偵測後依規格結束的情況，只需：

- `journal_detected`，WARN；
- `engine_failed`，ERROR，`message_id=6-33`。

`help` 仍回 0，故最後應是 `engine_completed`，但 `journal_detected` 仍可 WARN。

### 6. Dry-run

不必為 invocation 增設一般性的 `dry_run_started`。建議：

- `launcher_started.dry_run=true`
- `engine_started.dry_run=true`
- prune 每個候選用 `prune_candidate_identified`
- 若要清楚表明「本來會刪但因 dry-run 未刪」，增加 `prune_removal_simulated`

後者比把 `prune_removed` 加 `dry_run=true` 更安全，避免被誤認為已刪除。可沿用 base 的 `dry_run_cmd` 命名精神，但 `prune_removal_simulated` 的領域語意更精確。

### 7. 每檔 append 行細節

`file_appended.lines` 不足，因為：

- 可能 append 零行但若干 bytes；
- 最後一行有無 LF 會影響實際行數；
- 同一檔可能多次 append；
- 敏感內容不可記。

建議必填：

- `path`
- `bytes_written`
- `lines_added`
- `newline_added`
- `strategy`
- `content_kind`，例如 `gitignore_entry|dockerignore_entry|config_block`

選填：

- `before_digest`
- `after_digest`

digest 建議只用於非敏感專案管理檔；不得對 token file 或可能含秘密的任意檔案計算並記錄可離線比對的 digest。不可記實際 appended content。

`action` 在 `file_appended` 內是重複資訊，應刪除；event_name 已表達 action。

### 8. CI 模式

不需要獨立事件。記：

```json
"ci": true
```

即可，而且只記解析後布林值：

- `CI` 未設定或被規格判為 false → `false`
- 其他判定為 CI → `true`

附件寫「CI 真值」仍有歧義：如果指原始環境字串，就可能洩漏資訊，也不利於穩定查詢。建議規格明訂為 boolean。如何把 `CI=""`、`CI="false"` 判定為真假目前不確定，需由 CI 模組規格唯一化，但不能在 log 中保留原始值。

---

## 五、Attributes 共通規則

### 每筆必填

所有事件均應包含：

| attribute | 規則 |
|---|---|
| `component` | `launcher` 或 `engine` |
| `verb` | 正規化後的頂層動詞；bootstrap 為 `bootstrap` |
| `phase` | launcher 可用 `launch`；engine 為 `resolve`／`apply`／`single` |
| `invocation_id` | 可省略，因已由頂層 `trace_id` 表達；不應重複 |
| `dry_run` | 建議只在 start 事件必填，其餘事件透過同 trace 關聯 |
| `ci` | 建議只在 start 事件必填 |
| `assume_yes` | 建議只在 start 事件必填 |
| `lock_disabled` | engine start 必填 |

`verb` 已經是全事件共通 attribute，不需要在各事件的「主要 attributes」再重複列為事件專屬要求。

### 時間與結果

- 所有完成、失敗、timeout 事件：`duration_ms` 必填。
- 所有失敗事件：
  - `error_kind` 必填，使用有限 enum；
  - `message_id` 若有對應 6-xx，必填；
  - `exit_code` 若來自外部程序且可靠取得，必填；
  - `error_detail` 選填且必須去敏。
- 不建議自由文字 `reason` 作為唯一機器欄位；改用 enum `reason_code`，人讀內容放 `body`。

### 路徑

`cwd`、`path` 可能洩漏：

- 使用者名稱；
- 客戶／專案名稱；
- 主機目錄布局。

建議：

- 專案內檔案一律記 repo-relative path；
- `cwd` 改為 `repo_root="."` 或省略；
- 若確實需要辨識 repo，可記不具可逆性的 repo identifier，但未必必要；
- container 內暫存路徑應正規化為 repo-relative；
- 不記 `$HOME` 展開後的絕對路徑。

因此附件範例中的：

```json
"cwd":"/home/me/<專案根>"
```

不建議保留。

### argv 的重大衝突

建議撤銷「不論合法與否，完整原始 argv」要求，改成：

- `argv_redacted`：逐項保留結構，但對敏感參數值與 URL userinfo 做遮蔽；
- `argv_count`；
- `argv_redacted_fields`：只列被遮蔽的參數類型，不列原值；
- 非法 argv 也照記，但仍經相同 redaction。

例如：

```json
{
  "argv_redacted": [
    "add",
    "https://***@registry.example/repo",
    "--token",
    "[REDACTED]"
  ],
  "argv_redacted_fields": ["url_userinfo", "token_argument"]
}
```

如果 vendor_kit 可形式化保證 CLI 永遠不接受秘密參數，仍無法阻止 URL userinfo，因此至少 URL 必須先清洗。

### 明確禁止記錄

禁止出現在任何欄位，包括 `body`、`summary`、`error_detail`、`argv`：

- `VENDOR_KIT_REGISTRY_TOKEN`
- `VENDOR_KIT_REGISTRY_USER`
- `VENDOR_KIT_REGISTRY_TOKEN_FILE` 的內容
- token file 內容或可辨識摘要
- URL userinfo
- `Authorization`、Cookie、Docker credential helper 回覆
- `docker login` stdout/stderr
- 完整環境變數表
- registry HTTP request/response headers
- subprocess 原始 stderr，除非經明確結構化清洗
- journal 內容
- 被寫入檔案的完整內容

`summary` 也必須是結構化 object 或由固定模板產生；任意拼接 subprocess output 風險太高。

---

## 六、Severity 建議

### 原則

| 情況 | Severity |
|---|---|
| 正常生命週期、已完成動作 | `INFO` |
| 高頻診斷資訊、候選清單 | `DEBUG` |
| 可恢復異常、fallback、使用者拒絕、best-effort 失敗 | `WARN` |
| 本階段／本次操作失敗 | `ERROR` |
| 程式不變量破壞、未註冊事件、logger 本身不可用 | `FATAL` |

`FATAL` 不應用於普通 pull、registry、merge 或使用者輸入失敗。未註冊 event_name 是程式缺陷，使用 FATAL 合理。

log 檔本身無法寫時，`6-38` 只能輸出到 stderr；不能期待把這個 FATAL 記進同一個不可寫的 log。若是「後續 append 失敗」，現有檔案也可能只留下最後一個成功事件。

---

## 七、最終建議事件清單

下表採較嚴格、可查詢的結果型事件。`component`、`verb`、engine 的 `phase` 視為所有事件共同必填，表內不重複列出。

### Launcher

| event_name | 寫者 | severity | 必填 attributes | 何時 |
|---|---|---:|---|---|
| `launcher_started` | launcher | INFO | `argv_redacted`, `launcher_version`, `engine_ref`, `ci`, `dry_run`, `assume_yes` | log 建立成功後第一筆 |
| `config_loaded` | launcher | INFO | `keep`, `days`, `source="file"` | 成功讀取有效 config |
| `config_defaulted` | launcher | INFO | `keep`, `days`, `default_reason` | 缺檔或缺鍵，採預設 |
| `config_invalid` | launcher | WARN | `invalid_keys`, `defaulted_keys`, `keep`, `days`, `message_id`（若有） | 非法／重複值，對相關鍵採預設 |
| `config_read_failed` | launcher | ERROR | `error_kind`, `message_id`, `path` | config 存在但無法讀取或解析，且操作終止 |
| `docker_pull_started` | launcher | INFO | `ref`, `attempt`, `timeout_ms` | 每次 docker pull 前 |
| `docker_pull_completed` | launcher | INFO | `ref`, `digest`, `duration_ms`, `attempt` | pull 成功 |
| `docker_pull_failed` | launcher | ERROR | `ref`, `duration_ms`, `attempt`, `error_kind`, `exit_code`, `message_id` | pull 非 timeout 失敗 |
| `docker_pull_timed_out` | launcher | ERROR | `ref`, `duration_ms`, `timeout_ms`, `attempt`, `message_id` | pull 超過 `VENDOR_KIT_PULL_TIMEOUT` |
| `docker_extract_completed` | launcher | INFO | `repo`, `ref`, `path`, `duration_ms` | create/cp/rm 組成的 extract 全部成功 |
| `docker_extract_failed` | launcher | ERROR | `repo`, `ref`, `path`, `operation`, `error_kind`, `duration_ms`, `message_id` | extract 任一步失敗 |
| `engine_spawn_started` | launcher | INFO | `engine_ref`, `subcommand`, `interactive` | 執行 docker run 前 |
| `engine_spawned` | launcher | INFO | `engine_ref`, `subcommand`, `duration_ms` | 容器已成功開始執行；精確判定點不確定，需依 docker run 封裝方式定義 |
| `engine_spawn_failed` | launcher | ERROR | `engine_ref`, `subcommand`, `error_kind`, `exit_code`, `duration_ms`, `message_id` | docker 未能啟動引擎 |
| `sync_fast_path_selected` | launcher | INFO | `reason_code` | sync 命中快路徑 |
| `sync_fast_path_skipped` | launcher | DEBUG | `reason_code` | 快路徑不適用，包括 CI 模式 |
| `log_pruned` | launcher | INFO | `deleted_count`, `keep`, `days`, `duration_ms` | 保留清理成功；即使刪除零檔也可記 |
| `log_prune_failed` | launcher | WARN | `deleted_count`, `keep`, `days`, `error_kind`, `duration_ms` | best-effort 清理未完整成功 |
| `launcher_completed` | launcher | INFO | `exit_code=0`, `duration_ms` | 啟動器成功結束，最後一筆 |
| `launcher_failed` | launcher | ERROR | `exit_code`, `duration_ms`, `reason_code`, `message_id`（若有） | 啟動器非零結束，最後一筆 |

`launcher_completed`／`launcher_failed` 若因 trap 實作複雜而不方便分流，可合併為 `launcher_exited`，依 `exit_code` 動態給 INFO/ERROR；但不要再使用 `launcher_exit`。

### Engine

| event_name | 寫者 | severity | 必填 attributes | 何時 |
|---|---|---:|---|---|
| `engine_started` | engine | INFO | `argv_redacted`, `subcommand`, `engine_version`, `protocol`, `ci`, `dry_run`, `assume_yes`, `lock_disabled` | 每個 resolve/apply/single 容器第一筆 |
| `journal_detected` | engine | WARN | `path`, `journal_id`, `journal_verb`, `journal_state` | 發現未完成交易 |
| `journal_recovery_started` | engine | INFO | `path`, `journal_id`, `journal_verb`, `operation_count` | 可寫動詞開始恢復 |
| `journal_recovered` | engine | INFO | `path`, `journal_id`, `actions_reverted`, `duration_ms` | 恢復成功 |
| `journal_recovery_failed` | engine | ERROR | `path`, `journal_id`, `failed_action`, `error_kind`, `duration_ms`, `message_id` | 恢復失敗 |
| `resolve_completed` | engine | INFO | `plan_summary`, `apply_required`, `fingerprint`, `duration_ms` | resolve 成功完成 |
| `resolve_failed` | engine | ERROR | `error_kind`, `duration_ms`, `message_id` | resolve 失敗 |
| `lock_wait_started` | engine | DEBUG | `lock_path`, `timeout_ms` | apply 開始等待 flock |
| `lock_acquired` | engine | INFO | `lock_path`, `wait_ms` | 成功取得 flock |
| `lock_wait_timed_out` | engine | ERROR | `lock_path`, `wait_ms`, `timeout_ms`, `message_id` | 等待鎖逾時 |
| `lock_disabled` | engine | WARN | `source="environment"` | `VENDOR_KIT_NO_LOCK` 生效；每個 apply 最多一次 |
| `fingerprint_verified` | engine | INFO | `fingerprint` | apply 重驗與 resolve 相符 |
| `fingerprint_mismatched` | engine | ERROR | `expected_fingerprint`, `actual_fingerprint`, `message_id` | apply 重驗不符而停止 |
| `journal_created` | engine | INFO | `path`, `journal_id`, `operation_count` | 第一個實際寫入前建 journal |
| `journal_create_failed` | engine | ERROR | `path`, `error_kind`, `message_id` | journal 無法建立，禁止進入寫入 |
| `journal_deleted` | engine | INFO | `path`, `journal_id` | 成功完成後刪除 journal |
| `journal_delete_failed` | engine | ERROR | `path`, `journal_id`, `error_kind`, `message_id` | 成功操作後無法刪 journal；是否改整體 exit code 需由交易規格定義，不確定 |
| `prompt_asked` | engine | INFO | `message_id`, `prompt_kind`, `path`（適用時） | 印出 6-20/21/22/32/34 問句 |
| `prompt_answered` | engine | INFO | `message_id`, `answer`, `auto` | 得到 yes/no/eof；`auto=true` 表 `-y` |
| `file_created` | engine | INFO | `path`, `strategy`, `bytes_written` | 實際建立專案檔 |
| `file_modified` | engine | INFO | `path`, `strategy`, `bytes_written` | 實際修改或原子替換專案檔 |
| `file_appended` | engine | INFO | `path`, `strategy`, `bytes_written`, `lines_added`, `newline_added`, `content_kind` | 每個檔案每次實際 append 完成 |
| `file_deleted` | engine | INFO | `path`, `strategy` | 實際刪除專案檔 |
| `merge_conflict_detected` | engine | WARN | `path`, `merge_kind`, `message_id`（若有） | 三方合併產生需使用者決定的衝突 |
| `file_change_declined` | engine | INFO | `path`, `change_kind`, `state` | 使用者拒絕提議的檔案變更 |
| `version_written` | engine | INFO | `path`, `changed_keys`, `engine_ref` | 寫入 version.toml |
| `registry_query_started` | engine | DEBUG | `host`, `repo`, `query_kind` | 發出 registry 查詢前 |
| `registry_query_completed` | engine | INFO | `host`, `repo`, `query_kind`, `result`, `duration_ms`, `digest`（適用時） | 查詢正常完成，含正常的 not-found |
| `registry_query_failed` | engine | ERROR | `host`, `repo`, `query_kind`, `error_kind`, `duration_ms`, `message_id` | 認證、網路、協定或主機錯誤 |
| `registry_query_timed_out` | engine | ERROR | `host`, `repo`, `query_kind`, `timeout_ms`, `duration_ms`, `message_id` | registry 查詢有明確 timeout 且逾時；目前是否需要此機制不確定 |
| `prune_candidate_identified` | engine | DEBUG | `kind`, `object_id`, `reason_code` | 判定為 prune 候選 |
| `prune_removal_simulated` | engine | INFO | `kind`, `object_id`, `reason_code` | `--dry-run` 下本來會刪除 |
| `prune_removed` | engine | INFO | `kind`, `object_id`, `duration_ms` | 成功刪除候選 |
| `prune_remove_failed` | engine | WARN 或 ERROR | `kind`, `object_id`, `error_kind`, `duration_ms` | 單一候選刪除失敗；是否 ERROR 取決於 prune 是否允許部分成功 |
| `engine_completed` | engine | INFO | `exit_code=0`, `duration_ms`, `summary` | 子命令成功，該容器最後一筆 |
| `engine_failed` | engine | ERROR | `exit_code`, `duration_ms`, `reason_code`, `message_id`, `summary` | 子命令失敗，該容器最後一筆 |

---

## 八、可刪除或合併的重複資訊

建議刪除以下重複 attributes：

- `file_created.action=create`
- `file_modified.action=modify`
- `file_appended.action=append`
- `file_deleted.action=delete`
- `launcher_started.verb`／`engine_started.verb` 在表中特別列出，因其本來就是所有事件共通欄位
- `journal_created.id` 若只是頂層 `trace_id` 的重複值；改名 `journal_id`，並只在可能指向舊交易時記錄
- `prompt` 若內容就是 `body` 的重複文字；attributes 改記穩定的 `prompt_kind`，實際本地化句子留在 `body`
- `log_prune.error` 自由文字；改成獨立 `log_prune_failed` 加有限 enum `error_kind`
- `launcher_exit.reason` 自由文字；改成 `reason_code`

---

## 九、最終定案建議

1. 採用 snake_case、`object_past_tense`。
2. 全面改：
   - `*_start` → `*_started`
   - `*_finish` → `*_completed`
   - `*_exit` → `*_completed`／`*_failed`，或退而求其次用 `*_exited`
3. 外部操作至少應有 completed/failed；有硬 timeout 者另有 timed_out。
4. `config_read` 拆分正常、預設、非法及讀取失敗。
5. 增加 lock timeout、journal recovery failure、fingerprint mismatch、engine spawn failure、prune removal failure。
6. `dry_run`、`ci`、`assume_yes`、`lock_disabled` 納入 start 事件；其中 `lock_disabled` 再發 WARN。
7. dry-run 不得寫成 `prune_removed`；使用 `prune_removal_simulated`。
8. per-file append 記 bytes/lines/newline/content_kind，不記實際內容。
9. argv 必須改為 redacted argv；「完整原始 argv」要求應撤回。
10. 所有路徑盡量 repo-relative；不記完整 cwd。
11. `FATAL` 僅保留給未註冊事件、logger 不變量破壞及無法建立必要 audit log；業務失敗使用 ERROR。
12. release CI 除驗證 launcher 白名單是 registry 子集，還應驗證：
    - 所有程式碼中的靜態 event_name 都已註冊；
    - registry 無重複名稱；
    - event_name 符合 `^[a-z][a-z0-9_]*$`；
    - 不再使用 `_start`、`_finish`、`_exit` 等舊後綴；
    - launcher 只能發出其內嵌子集中的事件。

整體而言，L6 不需要追求每一個內部步驟都有事件；應優先確保「每個外部副作用、決策、等待、fallback 與失敗都有可機器查詢的結果事件」。這會比把大量不同結果塞進單一 `result` 或 `reason` attribute 更適合 audit、lnav 與後續相容性。
