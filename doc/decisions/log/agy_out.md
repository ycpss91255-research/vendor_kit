本篇報告針對 `vendor_kit` 的操作紀錄檔（audit / operation log）需求與硬性限制，逐題深入分析業界實踐、日誌標準、容器檔案系統特性與 `lnav` 視覺化規範，並於文末提供專為 `vendor_kit` 量身定制的推薦方案。

---

## 1. 類似 CLI 工具的操作紀錄留存方式

各主流 CLI 工具依據其定位（套件管理、版本控制、基礎架構編排、診斷輔助），在日誌的位置、格式、保留策略與寫入模式上有不同的設計：

### (1) `dpkg` 與 `apt`
* **存放位置**：
  * `/var/log/dpkg.log`（底層套件安裝/狀態變更紀錄）
  * `/var/log/apt/history.log`（高層交易紀錄）
  * `/var/log/apt/term.log`（終端機輸出複製）
* **格式**：
  * `dpkg.log` 為單行純文字追加：`YYYY-MM-DD HH:MM:SS <action> <pkg> <installed-version> <available-version>`。
  * `history.log` 採用類似 RFC 822 / Debian control file 的鍵值區塊（Stanza）格式，以區塊記錄每次執行，包含 `Start-Date:`、`Commandline:`、`Install:`、`Upgrade:`、`Remove:`、`End-Date:` 等欄位。
* **寫入模式**：單檔追加（Append-only）。
* **輪替與保留策略**：依賴系統層級的 `logrotate`（位於 `/etc/logrotate.d/dpkg` 與 `/etc/logrotate.d/apt`）。預設策略通常為 `monthly`，`dpkg.log` 保留 12 個月（`rotate 12`），`history.log` 保留 1 個月（`rotate 1` 或依發行版而異），並啟用 `gzip` 壓縮。
* **來源**：
  * [Debian manpages - dpkg(1)](https://manpages.debian.org/unstable/dpkg/dpkg.1.en.html)
  * [Debian manpages - apt.conf(5)](https://manpages.debian.org/unstable/apt/apt.conf.5.en.html)

### (2) `pip`
* **存放位置**：預設**不自動保留操作紀錄檔**。僅在使用者明確指定 `--log <path>` 時，才會將完整除錯日誌附加寫入指定檔案。
* **格式**：純文字（包含時間戳、日誌等級與詳細 HTTP/解析診斷訊息）。
* **寫入模式**：單檔追加（若檔案已存在則 append）。
* **輪替與保留策略**：無內建輪替機制，由使用者自行管理指定檔案。
* **來源**：
  * [pip Documentation - General Options (--log)](https://pip.pypa.io/en/stable/cli/pip/#cmdoption-log)

### (3) `npm`
* **存放位置**：`~/.npm/_logs/`（可透過 `npm config set logs-dir <path>` 自訂）。
* **格式**：純文字逐行除錯日誌（包含 ISO 8601 UTC 時間戳、記錄序號、模組名稱與診斷資訊）。
* **寫入模式**：**一次執行一檔**。檔名格式為 `<timestamp>-debug-<run_id>.log`（例如 `2026-09-20T03_14_07_123Z-debug-0.log`）。
* **輪替與保留策略**：由配置項 `logs-max` 控制（預設值為 **10**）。每次 `npm` 執行完畢或啟動清理時，若 `_logs/` 內的檔案數超過 `logs-max`，便自動刪除最舊的檔案。若設為 `0` 則不寫入磁碟。
* **來源**：
  * [npm CLI Documentation - Config: logs-max](https://docs.npmjs.com/cli/v10/using-npm/config#logs-max)
  * [npm CLI Documentation - Config: logs-dir](https://docs.npmjs.com/cli/v10/using-npm/config#logs-dir)

### (4) `cargo`
* **存放位置**：Cargo 本身**沒有內建的操作紀錄或審計日誌檔**。其所有進度、警告與錯誤預設直接印到 `stderr`。若設定環境變數 `CARGO_LOG`，除錯訊息同樣直接輸出至終端。
* **說明**：Rust 生態中的「審計」（Audit）通常是指 `cargo-audit` / `cargo-vet` 等第三方工具對依賴套件進行安全弱點掃描，而非記錄 CLI 本身的操作歷程。
* **來源**：
  * [The Cargo Book - Reference](https://doc.rust-lang.org/cargo/)

### (5) `terraform`
* **存放位置**：預設僅輸出到 `stderr`。若設定環境變數 `TF_LOG_PATH=<path>`，則會將日誌導向該檔案路徑。
* **格式**：若設定 `TF_LOG=TRACE` 或其他層級，預設為純文字；若設定 `TF_LOG_CORE=JSON` / `TF_LOG_PROVIDER=JSON` 則輸出結構化 JSON。
* **寫入模式**：單檔追加（若目標檔案存在則自動 append）。
* **輪替與保留策略**：Terraform 不提供日誌輪替或保留上限，由呼叫端或外部腳本維護。
* **來源**：
  * [Terraform Documentation - Debugging Terraform](https://developer.hashicorp.com/terraform/internals/debugging)

### (6) `pre-commit`
* **存放位置**：`~/.cache/pre-commit/pre-commit.log`。
* **格式**：Python 異常 Traceback 與執行環境資訊的純文字。
* **寫入模式**：**崩潰才寫入**（Fail-only crash log）。常態成功執行時不產生日誌檔；僅當發生未捕捉例外或勾點嚴重異常時，才會將崩潰細節覆寫/附加至該日誌檔。
* **來源**：
  * [pre-commit GitHub Repository](https://github.com/pre-commit/pre-commit)

### (7) `renovate`
* **存放位置**：透過環境變數 `RENOVATE_LOG_FILE` 指定路徑（例如 `renovate-log.ndjson`）。早期版本支援 `logFile` 配置項，自 v38 起已廢棄並改由環境變數控制。
* **格式**：NDJSON（Newline Delimited JSON，即 JSON Lines），基於 Pino/Bunyan 格式，包含 `name`, `level`, `msg`, `time`, `pid`, `hostname` 與自訂結構化欄位。
* **寫入模式**：每次任務批次執行時寫入該檔案。
* **輪替與保留策略**：Renovate 多在 CI/CD 中以容器化或排程執行，產生的 NDJSON 通常直接做為 CI Artifact 上傳，工具本身不負責跨日期的滾動輪替。
* **來源**：
  * [Renovate Docs - Troubleshooting (Logging)](https://docs.renovatebot.com/troubleshooting/)

### (8) `git reflog`
* **存放位置**：`.git/logs/HEAD` 以及各參照對應的 `.git/logs/refs/heads/<branch>`。
* **格式**：固定空白分隔欄位的純文字（單行一筆紀錄）：
  `<old-oid> <new-oid> <committer-name-and-email> <timestamp> <timezone-offset> <message>`
* **寫入模式**：單檔追加（每當參照發生移動時，原子附加至對應參照日誌檔末端）。
* **輪替與保留策略**：透過 `git gc` / `git reflog expire` 依據時間到期修剪。預設保留策略：
  * 可達提交（Reachable commits）：預設保留 90 天（由 `gc.reflogExpire` 控制）。
  * 不可達提交（Unreachable commits）：預設保留 30 天（由 `gc.reflogExpireUnreachable` 控制）。
* **來源**：
  * [Git Documentation - git-reflog](https://git-scm.com/docs/git-reflog)
  * [Git Documentation - git-config (gc.reflogExpire)](https://git-scm.com/docs/git-config#Documentation/git-config.txt-gcreflogExpire)

### (9) `docker`
* **主機操作**：Docker CLI 本身是薄客戶端，透過 Unix Socket 呼叫 Docker Daemon。CLI 操作紀錄（誰執行了 `docker run`）在標準 Docker Engine 中並無內建的本機操作日誌，通常需藉助 Linux 系統的 `auditd` 監控 `/usr/bin/dockerd` 或 `/var/run/docker.sock`。
* **容器執行日誌**：由 Engine 端的 Logging Driver（預設 `json-file` 或 `local`）記錄。`json-file` 驅動將容器標準串流包裝成 JSON Lines 格式（`{"log":"...","stream":"stdout","time":"..."}`），支援 `max-size`（如 10m）與 `max-file`（如 3）的輪替策略。
* **來源**：
  * [Docker Documentation - Configure logging drivers](https://docs.docker.com/engine/logging/configure/)
  * [Docker Documentation - JSON File logging driver](https://docs.docker.com/engine/logging/drivers/json-file/)

---

## 2. JSON Lines + OTel Logs Data Model 欄位在單機 CLI 的適用性評估

### (1) OTel Logs Data Model 是否過度設計？
OpenTelemetry (OTel) Logs Data Model 原本是為了分散式微服務追蹤與日誌整合設計，包含 `Timestamp`, `ObservedTimestamp`, `TraceId`, `SpanId`, `TraceFlags`, `SeverityText`, `SeverityNumber`, `Body`, `Resource`, `InstrumentationScope`, `Attributes` 等欄位。

* **適用之處**：
  * **標準欄位命名**：採用 OTel 的頂層命名規範（`timestamp` 以 ISO 8601 UTC 呈現、`severity_text`、`body`、`trace_id`、`attributes`），能直接享有日誌分析工具（如 `lnav`、Elasticsearch、Vector、Datadog）的現成解析支援。
  * **有限集合的 `body` 作為 Event Name**：將 `body` 當作事件類型（例如 `verb_start`、`file_write`、`prompt_ask`、`verb_end`），搭配鍵值結構的 `attributes` 記錄詳細中繼資料，完全符合 OTel 規範中的 **Event API** 語意。
* **應簡化之處（過度設計部分）**：
  * 單機 CLI 無需包含 `ObservedTimestamp`、`SpanId`、`TraceFlags`、`SeverityNumber`（數字代碼）、`Resource` 與 `InstrumentationScope`。
  * 引入完整的 OTel SDK（Python `opentelemetry-sdk`）會帶來龐大的依賴負擔（動輒增加數十 MB 映像檔大小與顯著啟動延遲）。
  * **結論**：**採用 OTel 的欄位名稱與結構語意，但使用自研的輕量級 JSON Lines 序列化輸出，是單機 CLI 工具的最佳實踐**。
* **來源**：
  * [OpenTelemetry Specs - Log Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/)
  * [OpenTelemetry Specs - Event API](https://opentelemetry.io/docs/specs/otel/logs/event-api/)

### (2) 替代方案：`logfmt` 的對比
* **優點**：`logfmt`（如 `timestamp=2026-09-20T03:14:07Z level=INFO event=file_write path=.vendor_kit/manifest.toml`）非常親和人類視覺，且在 POSIX sh 下不依賴 JSON 跳脫函式庫，用 `printf` 即可拼接。
* **致命缺點**：
  * **無法良好表達巢狀與陣列結構**：當事件需要記錄「修改的多個檔案列表」、「使用者提示選項陣列」或「diff 統計」時，`logfmt` 缺乏標準表達方式。
  * **缺乏正式規範**：`logfmt` 沒有官方標準 RFC，各家解析器（Go `logfmt`、Fluent Bit 等）對於空白、引號、換行與跳脫字元的處理常有不相容問題。
  * **與工具相容性**：`lnav` 對 JSON 的開箱即用支援與欄位過濾功能遠強於 `logfmt`。
* **來源**：
  * [Brandur Leach - logfmt](https://brandur.org/logfmt)
  * [Go doc - logfmt package](https://pkg.go.dev/github.com/go-logfmt/logfmt)

### (3) 業界對「Audit Log（審計日誌）」與「Debug Log（除錯日誌）」分開的建議
業界最佳實踐強烈建議將兩者拆分為不同通道或檔案，原因如下：

| 維度 | Audit Log（操作/審計日誌） | Debug Log（除錯/診斷日誌） |
| :--- | :--- | :--- |
| **目標讀者** | 終端使用者、專案維護者、安全審查員 | 工具開發者、深層除錯維護者 |
| **內容本質** | 業務與狀態變更（誰、動詞、改了什麼檔、確認與否、結果碼、耗時） | 程式碼內部流程（堆疊追蹤、網路連線標頭、容器掛載細節、執行緒狀態） |
| **雜訊量** | **極低、高訊噪比**（一次執行僅數筆至數十筆事件） | **極高**（一次執行動輒數千至數萬行） |
| **敏感資訊** | **嚴格禁止憑證與機密**（必須保證符合合規規範） | 可能含有低階通訊封包（容易意外洩漏 token） |
| **保留週期** | 長期保留（如 30～90 天，甚至隨 repo 歷史管理） | 短期暫存（如保留最近 10 次執行或崩潰時才產生） |

* **分離原則**：若將除錯日誌與審計日誌混入同一個檔案，審計日誌的高訊號價值將完全被巨量除錯資訊淹沒，使用者使用 `jq` 或 `lnav` 時將面臨巨大的解析負擔。
* **來源**：
  * [NIST SP 800-92 - Guide to Computer Security Log Management](https://csrc.nist.gov/publications/detail/sp/800-92/final)
  * [OWASP Cheat Sheet - Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)

---

## 3. 一次執行一檔 vs 單檔追加 + 輪替

針對單機 CLI 工具，兩種日誌架構的優缺點與保留策略對比如下：

### (1) 優缺點對比

| 特性 | 一次執行一檔（Per-run: `<ts>-<verb>-<id>.jsonl`） | 單檔追加（Append-only: `vendor_kit.jsonl`）+ 輪替 |
| :--- | :--- | :--- |
| **並行衝突與鎖定** | **完全零衝突**。每次呼叫獨立寫入新檔，無需跨行程鎖定（`flock`）。 | **高風險**。多個終端或後台任務同時執行時，必須搶鎖或依賴 POSIX 原子附加，容易交錯損壞。 |
| **輪替與清理成本** | **極低且安全**。清理僅需列舉目錄檔案並刪除最舊檔案（`unlink`），無競態條件。 | **極高且脆弱**。在無守護行程（Daemonless）架構下，誰負責輪替？容易遇到 `rename` 或 `copytruncate` 過程中的資料遺失或讀寫衝突。 |
| **失敗與交易隔離** | **天生隔離**。若執行途中當機或被 SIGKILL，損壞或不完整的紀錄僅限該次執行的單一檔案。 | **污染全域**。未閉合的 JSON 行或崩潰中斷可能破壞後續行解析。 |
| **單次追蹤便攜性** | **極佳**。回報 Issue 時只需附上該次執行的單一 `.jsonl` 檔即可重現問題。 | 需手動依據時間戳或 `trace_id` 從大檔中節錄相關區間。 |
| **跨次檢視體驗** | 若無專用工具（如 `cat *.jsonl` 或支援 glob 的 `lnav`），單純使用文字編輯器較零散。 | **較直覺**。可直接使用 `tail -f vendor_kit.jsonl` 監控最近動態。 |
| **Inode 與檔案數** | 若保留策略失效，頻繁執行會產生大量小檔案。 | 檔案數量固定（如主檔 + 數個 `.1`、`.2` 備份檔）。 |

### (2) 常見保留策略數字
* **依執行次數（Count-based）**：
  * `npm` 預設：保留 **10** 個檔案（`logs-max=10`）。
  * 適用於高頻互動 CLI 工具的除錯日誌。
  * 對於操作/審計日誌，常見數字為保留最近 **50 到 100 次** 執行。
* **依天數（Time-based）**：
  * `git reflog` 預設：**90 天**（可達提交）與 **30 天**（不可達提交）。
  * 系統管理日誌（如 `dpkg`、`syslog`）：通常保留 **30 天**（月輪替）至 **1 年**（12 個月）。
* **依容量上限（Size-based）**：
  * 單檔輪替常見上限：每個檔案 **5 MB ～ 10 MB**，保留 **3 ～ 5 個** 備份檔，總容量控制在 50 MB 以內。
* **來源**：
  * [npm CLI Documentation - Config: logs-max](https://docs.npmjs.com/cli/v10/using-npm/config#logs-max)
  * [Git Documentation - git-config (gc.reflogExpire)](https://git-scm.com/docs/git-config#Documentation/git-config.txt-gcreflogExpire)

---

## 4. 容器內寫檔到掛載目錄的陷阱

在主機由薄啟動器以 `docker run -v "$PWD":/repo -u $(id -u):$(id -g)` 啟動引擎並寫檔至掛載目錄時，有三個關鍵底層陷阱：

### (1) 權限與使用者識別碼（UID/GID & umask）
* **自動建立目錄歸屬 Root 的陷阱**：
  * 若掛載的子目錄（例如 `.vendor_kit/log/`）在主機上**尚未存在**，且容器以掛載卷的方式直接掛載該路徑（或容器內的程式在容器啟動前由 Docker Daemon 預先建立掛載點），Docker Daemon 會在主機上自動以 `root:root` 建立該目錄！
  * 即使容器執行時指定了 `--user $(id -u):$(id -g)`，由於主機目錄屬於 `root`，非 root 的容器行程將會直接遭遇 `Permission denied`，連日誌檔都無法建立。
  * **防禦對策**：**啟動器（主機端的 POSIX sh）必須在啟動 Docker 前，於主機上先行執行 `mkdir -p .vendor_kit/log`**，確保目錄的所有權直接屬於主機目前使用者。
* **umask 差異**：
  * 容器環境與主機環境的預設 `umask` 可能不同（常見為 `0022` 或 `0002`）。寫入日誌檔時應明確設定檔案權限為 `0644`，目錄為 `0755`，避免群組寫入權限異常。
* **來源**：
  * [Docker Documentation - Understand how UID and GID work in bind mounts](https://docs.docker.com/storage/bind-mounts/)

### (2) 原子寫入與跨裝置連結錯誤（Atomic Write & `EXDEV`）
* **陷阱機制**：
  * 在 Python 中實作安全寫入時，標準慣例是先寫入暫存檔，再透過 `os.replace(src, dst)`（底層呼叫 POSIX `rename(2)` 系統呼叫）進行原子覆蓋。
  * `rename(2)` 的 POSIX 規範明確限制：**來源與目標必須位於同一個掛載檔案系統（Same Filesystem / Mount Point）**。
  * 若 Python 程式碼使用 `tempfile.NamedTemporaryFile()` 且未指定目錄，暫存檔將被建立於容器根檔案系統的 `/tmp`（屬於容器的 OverlayFS 或 tmpfs）。當嘗試將暫存檔 `os.replace` 到掛載目錄 `/repo/.vendor_kit/log/` 時，Linux 核心會直接拋出錯誤：`OSError: [Errno 18] Invalid cross-device link (EXDEV)`。
* **防禦對策**：
  * 任何需要原子替換或寫入的暫存檔案，**其暫存目錄必須明確指定在目標路徑所在的同一目錄或同一掛載點內**（例如：`tempfile.NamedTemporaryFile(dir="/repo/.vendor_kit/log", prefix=".tmp.")`）。
* **來源**：
  * [Linux man-pages - rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html)
  * [Python Documentation - os.replace](https://docs.python.org/3/library/os.html#os.replace)

### (3) 檔案鎖定（`flock`）在掛載卷的行為
* **Linux 原生 Bind Mount**：
  * 在標準 Linux 主機環境下，Docker bind mount 只是核心 VFS 命名空間的掛載呈現，容器與主機共用同一個 Linux 核心與同一個檔案 Inode。
  * 因此，主機端行程與容器端行程針對同一檔案呼叫 `flock(2)` 或 `fcntl(F_SETLK)`，核心**能夠正常維護並感知鎖定狀態**。
* **跨平台與網路檔案系統陷阱**：
  * 若專案目錄位於 **NFS、CIFS/SMB** 或在 macOS / Windows 的 Docker Desktop 環境（透過 VirtioFS、gRPC-FUSE 或 9P 共享），`flock` 的跨行程鎖定語意極度脆弱，甚至可能直接回傳 `ENOSYS`、鎖定無效，或導致呼叫無端掛起（Deadlock）。
  * **異常終止時的死鎖問題**：若容器遭到 `SIGKILL` 或 OOM-Killed，依賴行程常駐維持的鎖（Advisory lock）雖會隨檔案描述符關閉由核心釋放，但若採用檔案標記式（如 `.lock` 檔未刪除）則會造成永久死鎖。
* **防禦對策**：
  * **避免在單機 CLI 跨容器邊界依賴複雜的 `flock`**。採用「一次執行一檔」架構從根本上免除寫入鎖定競爭。
* **來源**：
  * [Linux man-pages - flock(2)](https://man7.org/linux/man-pages/man2/flock.2.html)

---

## 5. `lnav` 的 JSON Format File 啟用 Timeline View 所需欄位與設定

`lnav`（Log File Navigator）是一套強大的終端結構化日誌分析器。要在 `lnav` 中完整啟用 **Timeline View**（時序檢視，按鍵 `t` 或 `Shift+A` 切換），必須在自訂格式定義檔（通常安裝於 `~/.lnav/formats/installed/<format_name>.json`）中設定特定鍵值，且日誌資料必須具備相應欄位。

### (1) 格式定義檔（Format JSON）所需關鍵屬性
* **`json: true`**：宣告此格式為結構化 JSON Lines 日誌。
* **`timestamp-field`**：指定日誌中代表時間戳的 JSON 欄位名稱（預設為 `"timestamp"`）。時間戳值必須為 `lnav` 支援的時間格式（ISO 8601 UTC 如 `2026-09-20T03:14:07.123Z` 開箱即用）。
* **`opid-field`**：**Timeline 顯示操作長度的核心欄位**。
  * 指定代表操作/交易識別碼的欄位名稱（例如 `"trace_id"` 或 `"id"`）。
  * **重大硬性限制**：在 `lnav` 的 JSON 格式定義中，**`opid-field` 所指定的欄位名稱，必須同時存在於 `line-format` 陣列中**（或作為格式輸出的一部分），否則 `lnav` 的操作分組與 `o` / `Shift+O` 操作導覽快捷鍵將無法正確綁定！
* **`duration-field` 與 `timestamp-point-of-reference`**（適用於單行事件包含耗時）：
  * 若某一筆日誌直接代表一個已完成的動作並包含耗時，可宣告 `"duration-field": "attributes/duration_ms"`。
  * `"duration-divisor"`：若單位為毫秒則設為 `1000`（`lnav` 內部以秒為基準）。
  * `"timestamp-point-of-reference"`（v0.14.0+）：指定該行的時間戳代表操作的 `"end"`（預設）還是 `"start"`。
* **`level-field`**：指定記錄日誌等級的欄位（如 `"severity_text"`），讓 Timeline 視圖上能顯示彩色指標（Sparklines）與錯誤狀態。
* **`line-format`**：定義日誌在終端主要檢視畫面的排版。

### (2) Timeline View 運作邏輯
在 Timeline 視圖中，`lnav` 會自動將具有相同 `opid`（`trace_id`）的多條日誌聚合成一個時間橫條（Span），橫條的起始點為該 `opid` 最早出現的日誌時間戳，終點為最後出現的日誌時間戳。若單一行包含 `duration-field`，亦會直接繪製出耗時寬度。

### (3) 範例：符合規範的 `lnav` Format 配置
```json
{
  "$schema": "https://lnav.org/schemas/format-v1.schema.json",
  "vendor_kit_log": {
    "title": "vendor_kit Operation Log",
    "description": "Log format for vendor_kit audit & operation events",
    "json": true,
    "timestamp-field": "timestamp",
    "opid-field": "trace_id",
    "level-field": "severity_text",
    "line-format": [
      { "field": "__timestamp__" },
      " ",
      { "field": "__level__" },
      " [",
      { "field": "trace_id" },
      "] ",
      { "field": "body" },
      ": ",
      { "field": "attributes/verb" }
    ],
    "value": {
      "body": { "kind": "string", "identifier": true },
      "trace_id": { "kind": "string", "identifier": true },
      "attributes/duration_ms": { "kind": "integer" }
    }
  }
}
```
* **來源**：
  * [lnav Documentation - Log Formats](https://docs.lnav.org/en/latest/formats.html)
  * [lnav Documentation - Timeline View](https://docs.lnav.org/en/latest/ui.html#timeline)

---

## 6. vendor_kit 推薦架構方案

綜合上述分析與使用者提供的背景與限制，以下為針對 `vendor_kit` 的完整架構設計方案：

### (1) 儲存位置與命名（一次執行一檔）
* **目錄位置**：專案根目錄下的 `.vendor_kit/log/`。
* **版控排除**：
  * 在專案根目錄的 `.gitignore` 與 `.dockerignore` 中加入：
    ```gitignore
    .vendor_kit/log/
    ```
  * 同時在 `.vendor_kit/log/.gitignore` 中放置 `*` 與 `!.gitignore`，作為雙重保險。
* **檔案命名慣例**：
  `.vendor_kit/log/<YYYYMMDDTHHMMSSZ>-<verb>-<trace_id_prefix>.jsonl`
  例如：`20260920T031407Z-install-a1b2c3d4.jsonl`
* **輔助捷徑**：每次執行完畢後，在該目錄建立或更新軟連結 `latest.jsonl` 指向最近一次的日誌檔，方便使用者快速 `cat` 或 `jq` 檢視。
* **理由與前例**：採用類似 `npm`（`~/.npm/_logs/`）與 CI Runner 的獨立執行檔模式，徹底杜絕跨容器/主機行程的檔案鎖定競態，確保日誌檔案在被強行終止時不污染其他歷史紀錄。

### (2) 欄位規格（對齊 OTel Event Logs）
每筆紀錄為標準 JSON 行，頂層欄位固定如下：
```json
{
  "timestamp": "2026-09-20T03:14:07.123456Z",
  "severity_text": "INFO",
  "body": "file_write",
  "trace_id": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
  "attributes": {
    "verb": "install",
    "phase": "apply",
    "path": ".vendor_kit/vendor.toml",
    "bytes_written": 1420
  }
}
```
* **有限的 `body`（事件集合）**：
  * `launcher_start` / `launcher_exit`
  * `docker_pull_start` / `docker_pull_finish`
  * `engine_start` / `engine_exit`
  * `resolve_start` / `resolve_finish`
  * `prompt_ask` / `prompt_answer`（記錄使用者的互動確認，如同意覆蓋）
  * `file_write` / `file_delete`
  * `apply_start` / `apply_finish`
* **機密防護保證**：
  在 Python 引擎與啟動器中設置過濾機制，所有 URL 必須遮蔽認證資訊（以 `***` 取代 token），`attributes` 中禁止收集任何含有 `TOKEN`、`PASSWORD`、`SECRET` 等關鍵字的環境變數或參數。

### (3) 保留與清理策略（Count-based）
* **策略**：**保留最近 50 個日誌檔**。
* **執行時機**：在啟動器行程即將退出（`trap ... EXIT`）的最後階段執行清理。
* **實作方式**：啟動器為 POSIX sh，使用原生命令排序並刪除超額檔案：
  ```sh
  # 僅保留最新的 50 個 .jsonl 檔案
  cleanup_logs() {
    log_dir="$1"
    [ -d "$log_dir" ] || return 0
    # 列出檔案並依修改時間排序，跳過前 50 個後刪除其餘檔案
    find "$log_dir" -maxdepth 1 -name "*.jsonl" -type f | sort -r | sed -e '1,50d' | xargs rm -f 2>/dev/null || true
  }
  ```

### (4) 啟動器（POSIX sh）與引擎的日誌串聯
啟動器負責生成唯一的 `trace_id`，記錄容器前置動作，並將其透過環境變數傳入容器，使容器內的 Python 引擎將日誌寫入同一個檔案：

```sh
#!/bin/sh
set -eu

VERB="${1:-help}"
LOG_DIR=".vendor_kit/log"

# 1. 主機端預先建立目錄，確保擁有者為當前主機使用者 (避開 Docker root 陷阱)
mkdir -p "$LOG_DIR"

# 2. 生成 Trace ID (32 位元 16 進位字串)
if [ -r /proc/sys/kernel/random/uuid ]; then
  TRACE_ID=$(tr -d '-' < /proc/sys/kernel/random/uuid)
else
  # POSIX 相容隨機降級方案
  TRACE_ID=$(od -vN 16 -An -tx1 /dev/urandom 2>/dev/null | tr -d ' \n' || printf '%016x%016x' "$$" "$(date +%s)")
fi

TRACE_SHORT=$(printf '%.8s' "$TRACE_ID")
TIMESTAMP=$(date -u +"%Y%m%m%dT%H%M%SZ" 2>/dev/null || date +"%Y%m%d%H%M%S")
ISO_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")

LOG_FILE="$LOG_DIR/${TIMESTAMP}-${VERB}-${TRACE_SHORT}.jsonl"

# 輔助：寫入日誌行至檔案
write_log() {
  _severity="$1"
  _body="$2"
  _extra_attrs="${3:-}"
  _now=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")
  printf '{"timestamp":"%s","severity_text":"%s","body":"%s","trace_id":"%s","attributes":{"verb":"%s","component":"launcher"%s}}\n' \
    "$_now" "$_severity" "$_body" "$TRACE_ID" "$VERB" "$_extra_attrs" >> "$LOG_FILE" 2>/dev/null || {
      # Never fail silently: 輸出警告至 stderr
      printf '[vendor_kit WARN] 無法寫入日誌檔: %s\n' "$LOG_FILE" >&2
    }
}

write_log "INFO" "launcher_start" ',"event":"cli_invoked"'

# 退出時的清理與結束紀錄
START_TIME=$(date +%s 2>/dev/null || true)
trap 'exit_code=$?; 
      end_time=$(date +%s 2>/dev/null || true);
      dur=0;
      [ -n "$START_TIME" ] && [ -n "$end_time" ] && dur=$((end_time - START_TIME));
      write_log "INFO" "launcher_exit" ",\"exit_code\":$exit_code,\"duration_s\":$dur";
      ln -sf "$(basename "$LOG_FILE")" "$LOG_DIR/latest.jsonl" 2>/dev/null || true;
      find "$LOG_DIR" -maxdepth 1 -name "*.jsonl" -type f | sort -r | sed -e "1,50d" | xargs rm -f 2>/dev/null || true;
      exit $exit_code' EXIT INT TERM

# 3. 執行 Docker 啟動，掛載 /repo 並注入 Trace ID 與日誌路徑
docker run --rm \
  -u "$(id -u):$(id -g)" \
  -v "$PWD:/repo" \
  -e VENDOR_KIT_TRACE_ID="$TRACE_ID" \
  -e VENDOR_KIT_LOG_FILE="/repo/$LOG_FILE" \
  vendor_kit_engine:latest "$@"
```

### (5) 「Never Fail Silently」與動詞回傳碼之權衡討論
針對使用者提出的矛盾情境：**「日誌寫不進去不能靜默忽略，但唯讀動詞是否應因為日誌失敗而回傳非 0？」**

* **靜默失敗（Fail Silently）的定義**：將錯誤捕捉（`try ... catch: pass`）並不發出任何警告，造成使用者在不知情的情況下遺失紀錄。因此，**在 `stderr` 印出高可見度的警告訊息絕對不是靜默失敗**。
* **動詞分級處理策略**：
  1. **唯讀/診斷動詞（`help`、`update`（僅查詢）、`resolve` 階段）**：
     * **行為**：**降級並發出強烈警告（Loud Warning）**。
     * **規則**：若日誌寫入失敗（例如磁碟滿、唯讀檔案系統、權限異常），立即於 `stderr` 印出：
       `[vendor_kit WARN] 無法寫入審計日誌 (.vendor_kit/log/...)：<詳細原因>。正在以無日誌模式繼續執行。`
     * **結果碼**：動詞主體執行成功即回傳 `0`。
     * **理由**：若使用者系統出問題（例如磁碟滿），執行 `vendor_kit help` 或 `vendor_kit update` 是排查問題的手段；若連說明或查詢都因無法記日誌而回傳非 0 崩潰，將造成嚴重的工具死鎖與糟糕的使用體驗。
  2. **寫入動詞（`install`、`upgrade`、`apply` 階段、`prune`、`remove`）**：
     * **行為**：**嚴格拒絕（Fail-Closed）**。
     * **規則**：在進入 `apply` 寫入任何專案檔案前，引擎先對日誌檔案進行連通性測試（寫入 `apply_start`）。若日誌檔案無法寫入，引擎必須立即中斷退出，並回傳非 0 結束碼，除非使用者明確加上強制跳過旗標（例如 `--no-audit`）。
     * **理由**：狀態變更必須具有審計追溯性。若在無法寫入日誌的情況下擅自變更專案檔案，將違反使用者對於審計追蹤（Audit Log）的安全性承諾。

### (6) 容器內寫檔注意事項（Python 引擎）
1. **直接追加寫入**：日誌採用 JSON Lines 格式，Python 引擎應以標準 `open(os.environ['VENDOR_KIT_LOG_FILE'], 'a', encoding='utf-8')` 開啟檔案，並於每次事件寫入時執行 `flush()`，無須使用暫存檔覆蓋。
2. **暫存檔原子寫入位置（交易進度檔）**：引擎若有 `.tmp.<verb>.<id>.toml` 進度日誌或配置檔需要原子替換，務必使用 `tempfile.NamedTemporaryFile(dir='/repo/.vendor_kit/log', prefix='.tmp.')`，保證暫存檔與專案目錄位於同一 Inode 裝置，防止 Linux 核心噴出 `EXDEV` 錯誤。
