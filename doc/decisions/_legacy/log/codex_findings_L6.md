# codex 審 L6 事件集合 — 整理版（只整理 codex 結論，不加整理者意見）

- 來源：`decisions/log/codex_out_L6.md`（codex exec，model gpt-5.6-sol，reasoning effort low，sandbox read-only，31,485 tokens）；brief：`decisions/log/codex_brief_L6.txt`。
- 附件備註：`decisions/log/base/` 下無 `log-events.txt`，附件 D-1 改用 `scratchpad/base_repo/dist/script/docker/lib/log-events.txt`（290 行）；D-2 為 `decisions/log/base/log.sh` 前 60 行。
- codex 標「不確定」之處在本文以 **[不確定]** 標示。

## 0. codex 總結摘要（六項主要問題）

1. 命名慣例混合：`launcher_start`／`resolve_finish`／`lock_acquired`／`file_created`／`registry_query` 並存 → 統一為「名詞（對象）＋過去式結果」。
2. 只有開始、沒有結果的事件：`engine_spawn`、`docker_extract`、`registry_query` 無法可靠表示失敗；`lock_acquired` 無法表示等待逾時。
3. 缺失敗事件：registry 查詢失敗、pull 逾時明確結果、lock 等待逾時、journal 恢復失敗、fingerprint 不符、引擎啟動失敗、prune 刪除失敗。
4. `config_read` 無法精確表示 fallback：應分正常載入／缺檔缺鍵預設／非法值預設／讀取或解析失敗。
5. 「完整原始 argv」與「憑證永不記」互相衝突：argv 可含 URL userinfo、token、使用者名稱；兩者不能同時保證。
6. 缺 invocation-level 模式欄位：`dry_run`、`assume_yes`、`lock_disabled`、`ci` 應放 start 事件共通 attributes，不必各自創事件；CI 只記布林判定、不記 `CI` 原值。

codex 建議保留：一次執行一檔、launcher/engine 共用 trace、註冊表 fail-fast、每個 resolve/apply 容器各自有開始／結束事件。

## 1. 現有事件逐條判定

### 1.1 launcher

| 現有 | 判定 | codex 建議與理由 |
|---|---|---|
| `launcher_start` | 改名 | → `launcher_started`（過去式一致） |
| `config_read` | 拆分 | → `config_loaded`（有效檔）／`config_defaulted`（缺檔或缺鍵）／`config_invalid`（非法或重複值）／`config_read_failed`（存在但無法讀或解析且終止）；理由：`source=file|default` 答不了「為何 default」 |
| `docker_pull_start` | 改名 | → `docker_pull_started` |
| `docker_pull_finish` | 拆分 | → `docker_pull_completed`／`docker_pull_failed`；逾時另立 `docker_pull_timed_out`；理由：成功失敗混在 `reason` 不利以 event_name 篩選與配 severity |
| `docker_extract` | 改名＋新增 | → `docker_extract_completed`；新增 `docker_extract_failed` |
| `engine_spawn` | 改名＋新增 | 「run 前」尚未 spawn → `engine_spawn_started`；另加 `engine_spawned`、`engine_spawn_failed` |
| `sync_fast_path` | 拆分（或保留） | 拆 `sync_fast_path_selected`／`sync_fast_path_skipped`；或保留單一事件＋`result`，但前者較易查詢 |
| `log_prune` | 改名＋新增 | → `log_pruned`；新增 `log_prune_failed`（best-effort 失敗） |
| `launcher_exit` | 拆分（或改名） | → `launcher_completed`／`launcher_failed`；若 trap 分流不便，可合併為 `launcher_exited`（依 exit_code 給 INFO/ERROR），但不要再用 `launcher_exit` |

### 1.2 engine

| 現有 | 判定 | codex 建議與理由 |
|---|---|---|
| `engine_start` | 改名 | → `engine_started` |
| `journal_detected` | 保留＋補欄位 | 記 journal 所屬原始 verb／id（`journal_verb`、`journal_id`、`journal_state`），不只記本次 verb |
| `journal_recovered` | 保留＋新增 | 新增 `journal_recovery_started`、`journal_recovery_failed`（完整生命週期） |
| `resolve_finish` | 改名＋新增 | → `resolve_completed`；新增 `resolve_failed` |
| `lock_acquired` | 保留＋新增 | 新增 `lock_wait_started`（DEBUG）、`lock_wait_timed_out`（ERROR）；另加 `lock_disabled`（WARN，`VENDOR_KIT_NO_LOCK` 生效時每個 apply 最多一次） |
| `fingerprint_verified` | 保留＋新增 | 新增 `fingerprint_mismatched`（或 `fingerprint_verification_failed`） |
| `journal_created` | 保留＋新增 | 新增 `journal_create_failed` |
| `journal_deleted` | 保留＋新增 | 新增 `journal_delete_failed`；是否改整體 exit code **[不確定]**，由交易規格定 |
| `prompt_asked` | 保留 | — |
| `prompt_answered` | 保留 | — |
| `file_created` | 保留 | 刪重複的 `action` 欄位 |
| `file_modified` | 保留 | 同上 |
| `file_appended` | 保留＋補欄位 | 只記 `lines` 不足（可能 append 零行但有 bytes、末行有無 LF 影響行數、同檔多次 append）→ 必填 `bytes_written`、`lines_added`、`newline_added`、`strategy`、`content_kind`；選填 `before_digest`／`after_digest`（只用於非敏感專案管理檔）；不記實際內容 |
| `file_deleted` | 保留 | 刪重複的 `action` |
| `merge_conflict` | 改名 | → `merge_conflict_detected` |
| `declined` | 改名 | 太含糊 → `file_change_declined`（或 `merge_declined`，依實際語意）；註：現文「declined_hash」與 attributes 表不一致 |
| `version_written` | 保留 | — |
| `registry_query` | 拆分 | → `registry_query_started`／`registry_query_completed`／`registry_query_failed`；若有硬 timeout 再加 `registry_query_timed_out`（是否有 timeout 機制 **[不確定]**）；`not_found` 屬 INFO 或 ERROR 視語境（查存在性 = INFO；規格要求必存在 = ERROR） |
| `prune_candidate` | 改名＋降級 | → `prune_candidate_identified`，DEBUG |
| `prune_removed` | 保留＋新增 | 新增 `prune_remove_failed`（WARN 或 ERROR，取決於 prune 是否允許部分成功）；dry-run 用 `prune_removal_simulated`，不得寫成 `prune_removed` |
| `engine_exit` | 拆分（或改名） | → `engine_completed`／`engine_failed`；或固定最後一筆用 `engine_exited` |

### 1.3 缺口對應（brief 點名的情境）

| 情境 | codex 答 |
|---|---|
| registry 查詢失敗 | 獨立 `registry_query_failed`（＋`_timed_out` 視實作） |
| pull 逾時 | 獨立 `docker_pull_timed_out`，ERROR；必填 `ref`、`timeout_ms`、`duration_ms`、`exit_code`（可靠取得時）、`message_id`（6-24／6-31）、`attempt`；是否有 retry **[不確定]** |
| 鎖等待逾時 | `lock_wait_started`／`lock_acquired`／`lock_wait_timed_out`／`lock_disabled`；環境變數原值不記，只記布林＋`source="environment"` |
| config 退回預設 | 拆四事件（見 1.1）；新增 `default_reason` ∈ `file_missing|key_missing|invalid_value|duplicate_key|parse_error`、`invalid_keys`；不記原始非法值 |
| 進度檔恢復 | `journal_detected` → `journal_recovery_started` → `journal_recovered`／`journal_recovery_failed`；唯讀動詞只需 `journal_detected`（WARN）＋ `engine_failed`（6-33）；help 回 0 → 最後 `engine_completed`，`journal_detected` 仍 WARN |
| dry-run | 不設獨立 start 事件；`launcher_started.dry_run`、`engine_started.dry_run`；prune 候選 `prune_candidate_identified`，「本來會刪」用 `prune_removal_simulated` |
| 每檔 append 行細節 | 見 1.2 `file_appended` |
| CI 模式旗標 | 不設事件；start 事件記 `ci: true/false`（布林）；「CI 真值」若指原始字串會洩漏且不利查詢；`CI=""`／`"false"` 判定 **[不確定]**，由 CI 模組規格唯一化 |

## 2. attributes 欄位建議

### 2.1 每筆共通
- `component` ∈ launcher／engine；`verb`（正規化頂層動詞，bootstrap 為 `bootstrap`）；`phase`（launcher 用 `launch`；engine 用 resolve／apply／single）。
- `verb` 已是共通欄位，不必在各事件「主要 attributes」再重複列。
- 不設 `invocation_id`（與頂層 `trace_id` 重複）。
- `dry_run`、`ci`、`assume_yes` 只在 start 事件必填；`lock_disabled` 在 `engine_started` 必填。

### 2.2 時間與結果
- 所有 completed／failed／timed_out 事件：`duration_ms` 必填。
- 所有 failed 事件：`error_kind`（有限 enum）必填；`message_id` 有對應 6-xx 則必填；`exit_code` 來自外部程序且可靠時必填；`error_detail` 選填且必去敏。
- 自由文字 `reason` 不當唯一機器欄位 → 改 enum `reason_code`，人讀內容放 `body`。

### 2.3 路徑
- 專案內檔案一律 repo-relative；容器內暫存路徑正規化為 repo-relative；不記 `$HOME` 展開後絕對路徑。
- `cwd` 改 `repo_root="."` 或省略；範例中 `"cwd":"/home/me/<專案根>"` 不建議保留。

### 2.4 argv（codex 認為是重大衝突）
- 撤回「不論合法與否，完整原始 argv」；改 `argv_redacted`（逐項保留結構，遮蔽敏感參數值與 URL userinfo）、`argv_count`、`argv_redacted_fields`（只列被遮蔽的類型）；非法 argv 也記但同樣 redaction。
- 即使 CLI 保證不接受秘密參數，也擋不了 URL userinfo，故 URL 至少必須先清洗。

### 2.5 明確禁記（任何欄位含 body／summary／error_detail／argv）
`VENDOR_KIT_REGISTRY_TOKEN`、`_USER`、`_TOKEN_FILE` 內容、token file 內容或可辨識摘要、URL userinfo、`Authorization`／Cookie／credential helper 回覆、`docker login` 輸出、完整環境變數表、registry HTTP headers、subprocess 原始 stderr（除非結構化清洗）、journal 內容、被寫入檔案的完整內容。`summary` 須為結構化 object 或固定模板產生。

### 2.6 建議刪除的重複欄位
`file_*.action`、start 事件表內特列的 `verb`、`journal_created.id`（若只是 trace_id 重複 → 改 `journal_id` 且只在可能指向舊交易時記）、`prompt`（若與 body 重複 → 改 `prompt_kind`）、`log_prune.error`（→ 獨立 `log_prune_failed`＋`error_kind`）、`launcher_exit.reason`（→ `reason_code`）。

## 3. 與 base 命名慣例的對齊

- codex 觀察 base `log-events.txt`：snake_case；名詞／領域對象在前、結果／狀態在後；已發生事件多用過去式或結果詞（`build_started`、`upgrade_completed`、`env_regenerated`、`conf_invalid_value`、`deploy_failed`、`reclaim_orphan_removed`、`transcript_file_unwritable`）。
- base 並非嚴格單一規則（有 `reclaim_scan`、`summary_line`、`dry_run_cmd` 等現在式），但生命週期／稽核事件以「名詞＋過去式結果」最接近 base 主流。
- 建議規則：`<object>_<past-tense-result>`；`finish` 一律改 `completed`；不用動詞在前（`resolve_finish`）、非過去式（`launcher_start`）、單一事件同含開始與結果（`registry_query`）；不把異常塞進正常事件的 `result`／`reason`。
- `prompt_asked`、`prompt_answered`、`file_created` 等現有名稱已符合。
- dry-run 可沿用 base `dry_run_cmd` 精神，但 `prune_removal_simulated` 領域語意更精確。

## 4. severity 原則

| 情況 | severity |
|---|---|
| 正常生命週期、已完成動作 | INFO |
| 高頻診斷、候選清單 | DEBUG |
| 可恢復異常、fallback、使用者拒絕、best-effort 失敗 | WARN |
| 本階段／本次操作失敗 | ERROR |
| 程式不變量破壞、未註冊事件、logger 本身不可用 | FATAL |

- FATAL 不用於普通 pull／registry／merge／使用者輸入失敗。
- log 檔不可寫時 6-38 只能到 stderr，不能期待記進同一不可寫的 log；「後續 append 失敗」時檔案可能只留最後一個成功事件。

## 5. 最終建議清單（codex）

共通必填 `component`、`verb`、engine 的 `phase`，表內不重複。

### 5.1 launcher

| event_name | 寫者 | severity | 必填 attributes | 何時 |
|---|---|---|---|---|
| `launcher_started` | launcher | INFO | `argv_redacted`, `launcher_version`, `engine_ref`, `ci`, `dry_run`, `assume_yes` | log 建立成功後第一筆 |
| `config_loaded` | launcher | INFO | `keep`, `days`, `source="file"` | 成功讀取有效 config |
| `config_defaulted` | launcher | INFO | `keep`, `days`, `default_reason` | 缺檔或缺鍵採預設 |
| `config_invalid` | launcher | WARN | `invalid_keys`, `defaulted_keys`, `keep`, `days`, `message_id`（若有） | 非法／重複值，相關鍵採預設 |
| `config_read_failed` | launcher | ERROR | `error_kind`, `message_id`, `path` | config 存在但無法讀或解析且終止 |
| `docker_pull_started` | launcher | INFO | `ref`, `attempt`, `timeout_ms` | 每次 pull 前 |
| `docker_pull_completed` | launcher | INFO | `ref`, `digest`, `duration_ms`, `attempt` | pull 成功 |
| `docker_pull_failed` | launcher | ERROR | `ref`, `duration_ms`, `attempt`, `error_kind`, `exit_code`, `message_id` | pull 非逾時失敗 |
| `docker_pull_timed_out` | launcher | ERROR | `ref`, `duration_ms`, `timeout_ms`, `attempt`, `message_id` | 超過 `VENDOR_KIT_PULL_TIMEOUT` |
| `docker_extract_completed` | launcher | INFO | `repo`, `ref`, `path`, `duration_ms` | create/cp/rm 全部成功 |
| `docker_extract_failed` | launcher | ERROR | `repo`, `ref`, `path`, `operation`, `error_kind`, `duration_ms`, `message_id` | extract 任一步失敗 |
| `engine_spawn_started` | launcher | INFO | `engine_ref`, `subcommand`, `interactive` | docker run 前 |
| `engine_spawned` | launcher | INFO | `engine_ref`, `subcommand`, `duration_ms` | 容器已開始執行；判定點 **[不確定]**，依 docker run 封裝定義 |
| `engine_spawn_failed` | launcher | ERROR | `engine_ref`, `subcommand`, `error_kind`, `exit_code`, `duration_ms`, `message_id` | docker 未能啟動引擎 |
| `sync_fast_path_selected` | launcher | INFO | `reason_code` | sync 命中快路徑 |
| `sync_fast_path_skipped` | launcher | DEBUG | `reason_code` | 快路徑不適用（含 CI 模式） |
| `log_pruned` | launcher | INFO | `deleted_count`, `keep`, `days`, `duration_ms` | 保留清理成功（刪零檔也記） |
| `log_prune_failed` | launcher | WARN | `deleted_count`, `keep`, `days`, `error_kind`, `duration_ms` | best-effort 清理未完整成功 |
| `launcher_completed` | launcher | INFO | `exit_code=0`, `duration_ms` | 成功結束，最後一筆 |
| `launcher_failed` | launcher | ERROR | `exit_code`, `duration_ms`, `reason_code`, `message_id`（若有） | 非零結束，最後一筆 |

（`launcher_completed`／`launcher_failed` 可退而合併為 `launcher_exited`，依 exit_code 給 INFO/ERROR。）

### 5.2 engine

| event_name | 寫者 | severity | 必填 attributes | 何時 |
|---|---|---|---|---|
| `engine_started` | engine | INFO | `argv_redacted`, `subcommand`, `engine_version`, `protocol`, `ci`, `dry_run`, `assume_yes`, `lock_disabled` | 每個 resolve/apply/single 容器第一筆 |
| `journal_detected` | engine | WARN | `path`, `journal_id`, `journal_verb`, `journal_state` | 發現未完成交易 |
| `journal_recovery_started` | engine | INFO | `path`, `journal_id`, `journal_verb`, `operation_count` | 可寫動詞開始恢復 |
| `journal_recovered` | engine | INFO | `path`, `journal_id`, `actions_reverted`, `duration_ms` | 恢復成功 |
| `journal_recovery_failed` | engine | ERROR | `path`, `journal_id`, `failed_action`, `error_kind`, `duration_ms`, `message_id` | 恢復失敗 |
| `resolve_completed` | engine | INFO | `plan_summary`, `apply_required`, `fingerprint`, `duration_ms` | resolve 成功 |
| `resolve_failed` | engine | ERROR | `error_kind`, `duration_ms`, `message_id` | resolve 失敗 |
| `lock_wait_started` | engine | DEBUG | `lock_path`, `timeout_ms` | apply 開始等 flock |
| `lock_acquired` | engine | INFO | `lock_path`, `wait_ms` | 取得 flock |
| `lock_wait_timed_out` | engine | ERROR | `lock_path`, `wait_ms`, `timeout_ms`, `message_id` | 等鎖逾時 |
| `lock_disabled` | engine | WARN | `source="environment"` | `VENDOR_KIT_NO_LOCK` 生效；每 apply 最多一次 |
| `fingerprint_verified` | engine | INFO | `fingerprint` | apply 重驗相符 |
| `fingerprint_mismatched` | engine | ERROR | `expected_fingerprint`, `actual_fingerprint`, `message_id` | apply 重驗不符而停止 |
| `journal_created` | engine | INFO | `path`, `journal_id`, `operation_count` | 第一個寫入前建 journal |
| `journal_create_failed` | engine | ERROR | `path`, `error_kind`, `message_id` | journal 無法建立，禁止進寫入 |
| `journal_deleted` | engine | INFO | `path`, `journal_id` | 成功後刪 journal |
| `journal_delete_failed` | engine | ERROR | `path`, `journal_id`, `error_kind`, `message_id` | 成功後無法刪 journal；是否改 exit code **[不確定]** |
| `prompt_asked` | engine | INFO | `message_id`, `prompt_kind`, `path`（適用時） | 印 6-20/21/22/32/34 問句 |
| `prompt_answered` | engine | INFO | `message_id`, `answer`, `auto` | yes/no/eof；`auto=true` = `-y` |
| `file_created` | engine | INFO | `path`, `strategy`, `bytes_written` | 建立專案檔 |
| `file_modified` | engine | INFO | `path`, `strategy`, `bytes_written` | 修改或原子替換 |
| `file_appended` | engine | INFO | `path`, `strategy`, `bytes_written`, `lines_added`, `newline_added`, `content_kind` | 每檔每次 append 完成 |
| `file_deleted` | engine | INFO | `path`, `strategy` | 刪除專案檔 |
| `merge_conflict_detected` | engine | WARN | `path`, `merge_kind`, `message_id`（若有） | 三方合併需使用者決定 |
| `file_change_declined` | engine | INFO | `path`, `change_kind`, `state` | 使用者拒絕提議變更 |
| `version_written` | engine | INFO | `path`, `changed_keys`, `engine_ref` | 寫 version.toml |
| `registry_query_started` | engine | DEBUG | `host`, `repo`, `query_kind` | 發查詢前 |
| `registry_query_completed` | engine | INFO | `host`, `repo`, `query_kind`, `result`, `duration_ms`, `digest`（適用時） | 正常完成（含正常 not-found） |
| `registry_query_failed` | engine | ERROR | `host`, `repo`, `query_kind`, `error_kind`, `duration_ms`, `message_id` | 認證／網路／協定／主機錯誤 |
| `registry_query_timed_out` | engine | ERROR | `host`, `repo`, `query_kind`, `timeout_ms`, `duration_ms`, `message_id` | 有明確 timeout 且逾時；是否需要 **[不確定]** |
| `prune_candidate_identified` | engine | DEBUG | `kind`, `object_id`, `reason_code` | 判定為候選 |
| `prune_removal_simulated` | engine | INFO | `kind`, `object_id`, `reason_code` | `--dry-run` 下本來會刪 |
| `prune_removed` | engine | INFO | `kind`, `object_id`, `duration_ms` | 刪除成功 |
| `prune_remove_failed` | engine | WARN 或 ERROR | `kind`, `object_id`, `error_kind`, `duration_ms` | 單一候選刪除失敗；等級取決於是否允許部分成功 |
| `engine_completed` | engine | INFO | `exit_code=0`, `duration_ms`, `summary` | 子命令成功，該容器最後一筆 |
| `engine_failed` | engine | ERROR | `exit_code`, `duration_ms`, `reason_code`, `message_id`, `summary` | 子命令失敗，該容器最後一筆 |

## 6. codex 最終定案建議（12 條）

1. snake_case、`object_past_tense`。
2. 全面改：`*_start`→`*_started`；`*_finish`→`*_completed`；`*_exit`→`*_completed`／`*_failed`（退而 `*_exited`）。
3. 外部操作至少 completed/failed；有硬 timeout 者另有 timed_out。
4. `config_read` 拆四。
5. 增 lock timeout、journal recovery failure、fingerprint mismatch、engine spawn failure、prune removal failure。
6. `dry_run`、`ci`、`assume_yes`、`lock_disabled` 納入 start 事件；`lock_disabled` 另發 WARN。
7. dry-run 不得寫 `prune_removed`；用 `prune_removal_simulated`。
8. per-file append 記 bytes/lines/newline/content_kind，不記內容。
9. argv 改 redacted；撤回「完整原始 argv」。
10. 路徑 repo-relative；不記完整 cwd。
11. FATAL 只留給未註冊事件、logger 不變量破壞、無法建立必要 audit log。
12. release CI 除「內嵌白名單 ⊆ 真本」外，再驗：程式碼中靜態 event_name 都已註冊；registry 無重複；符合 `^[a-z][a-z0-9_]*$`；不再用 `_start`／`_finish`／`_exit` 後綴；launcher 只能發內嵌子集事件。

總評（codex 原話大意）：L6 不必追求每個內部步驟都有事件；優先確保「每個外部副作用、決策、等待、fallback 與失敗都有可機器查詢的結果事件」，比把不同結果塞進單一 `result`／`reason` attribute 更適合 audit、lnav 與後續相容。

## 7. codex 標「不確定」的項目彙整
- registry query 是否有 timeout 機制（決定 `registry_query_timed_out` 是否需要）。
- docker pull 是否有 retry（決定 `attempt`／`max_attempts`）。
- `engine_spawned` 的精確判定點。
- `journal_delete_failed` 是否改整體 exit code。
- `prune_remove_failed` 是 WARN 或 ERROR（取決於 prune 是否允許部分成功）。
- `CI=""`／`CI="false"` 如何判真假（由 CI 模組規格唯一化）。
- `registry not_found` 的 severity 視語境。

## 8. 與既定案（v2.12 L1–L5 已由使用者定案）相牴觸的 codex 建議（供主對話判斷，整理者不表態）
- L5「`launcher_start` 記完整原始 argv（不論合法與否）」 ↔ codex 建議撤回、改 `argv_redacted`。
- §4.10 欄位表「審後只准增刪事件名與屬性，不改欄位表」 ↔ codex 的 `phase` 改為所有事件共通必填（含 launcher `launch`）；屬 attributes 層，未動頂層欄位。
- §4.10 範例 `cwd` 絕對路徑 ↔ codex 建議不記完整 cwd。
- v2.12 L6「`launcher_start` 記 CI 真值」 ↔ codex 要求明訂為布林、不記原值。
