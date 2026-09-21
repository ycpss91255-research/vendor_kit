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
