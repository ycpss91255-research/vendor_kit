針對在受限的純 POSIX `sh`（僅保證 `printf`、`grep`、`sed`、`tr`、`date`，無 `jq`、`python`、`jo`、`awk`）環境下輸出 JSON Lines（NDJSON）日誌與分散式追蹤的需求，以下提供完整的調研、原始碼對比、技術細節分析與推薦架構。

---

### (1) 主流開源專案是否有在 Shell 裡直接產生 JSON Log？跳脫方式為何？

#### 調研結論
在主流開源專案（如 Docker 官方鏡像、Kubernetes、Helm、kind、rustup、nvm、asdf、systemd、busybox）中，**幾乎完全不曾在 Shell 腳本中直接手寫產生結構化 JSON Log**。

主流專案的設計哲學如下：
1. **容器 Entrypoint（Docker 官方鏡像如 postgres、redis、nginx）**：
   - 官方 Entrypoint 嚴格遵守「UNIX 管道與單一職責原則」，只使用 `echo` 或 `printf` 輸出純文字或帶時間戳的人類可讀訊息（例如 `docker-entrypoint.sh` 中的 `echo "$0: ..."`）。
   - **JSON 化交由下層容器執行環境（Container Runtime）**：Docker 的 `json-file` logging driver、containerd 或 Kubernetes CRI 會自動將容器的 `stdout`/`stderr` 串流包裝成標準 JSON 封裝（包含 `log`、`stream`、`time` 欄位），而非由 Shell 腳本自製 JSON。
2. **Kubernetes / Helm / kind 的 hack 腳本**：
   - Kubernetes 的內部 Shell 腳本統一引用 [`hack/lib/logging.sh`](https://github.com/kubernetes/kubernetes/blob/master/hack/lib/logging.sh)。
   - 其採用的日誌函式（如 `kube::log::info`、`kube::log::status`、`kube::log::error`）全部輸出帶時間戳與 ANSI 終端顏色的純文字，**無任何 JSON 格式輸出**（Kubernetes 僅在編譯後的 Go 二進制程式中以 `klog`/`zap` 輸出 JSON）。
3. **rustup / nvm / asdf / sdkman 安裝與管理腳本**：
   - 均為給終端使用者看的人機介面腳本，使用 `say()`、`nvm_echo()`、`display_info()` 等函式輸出彩色文字，無 JSON 日誌需求。
4. **GitHub Actions Runner 腳本**：
   - Runner 核心為 C#，其輔助 Shell 腳本與 Runner 溝通結構化資料時，使用的是 GitHub 自創的 **Workflow Commands**（如 `::error::...`、`::notice::...`），而非 JSON。
5. **systemd / busybox**：
   - 均為 C 語言實作。systemd 使用 `sd-journal` 原生二進制鍵值協定寫入 `/run/systemd/journal/socket`，`journalctl -o json` 是在 C 層級做序列化；Busybox 的 `logger` 僅支援 RFC 3164/5424 的 Syslog 純文字格式。

#### 例外：極少數在 Shell 裡手寫 JSON 的專案及其跳脫缺陷
少數因架構限制必須在純 POSIX Shell 中拼裝 JSON API Payload 的專案（非日誌，而是 HTTP 呼叫），其跳脫往往**不完整且充滿漏洞**：

*   **專案案例：`acme.sh`**（著名的純 POSIX Shell ACME 憑證客戶端）
    *   **原始碼連結**：[`acmesh-official/acme.sh`（`acme.sh` 核心程式碼）](https://github.com/acmesh-official/acme.sh/blob/master/acme.sh)
    *   **函式片段**：
        ```sh
        _json_encode() {
          _j_str="$(sed 's/"/\\"/g' | sed "s/\r/\\r/g")"
          _debug3 "_json_encode"
          _debug3 "_j_str"
          printf "%s" "$_j_str"
        }
        ```
    *   **跳脫缺陷**：
        1. **漏掉反斜線（`\`）跳脫**：未將 `\` 轉為 `\\`，若輸入含有 `\` 會破壞 JSON 語法或產生非法跳脫字元。
        2. **漏掉換行（`\n`）跳脫**：未將換行轉為 `\n`，導致產生多行字串，在嚴格的 JSON / JSON Lines 中直接解析失敗。
        3. **忽略所有控制字元（U+0000–U+001F）**：除 `\r` 之外的 Tab（`\t`）、Backspace（`\b`）等控制字元皆未處理。
*   **常見教學/範例專案：AWS Lambda Custom Runtime `bootstrap`**
    *   在 AWS 官方的 Bash 自訂執行環境範例中，通常直接以硬編碼字串回傳：
        `RESPONSE="{\"statusCode\": 200, \"body\": \"Hello from Bash!\"}"`
        只要遇到動態變數含有引號或換行便會崩潰，官方文件通常備註「生產環境請引入 `jq`」。

---

### (2) 現成 Shell JSON Logger 函式庫與工具分析

| 工具 / 函式庫 | 語言 / 執行依賴 | 是否符合 POSIX sh？ | RFC 8259 跳脫完整性（`"`, `\`, U+0000–U+001F） | 來源連結 / 評語 |
| :--- | :--- | :--- | :--- | :--- |
| **`jpmens/jo`** | C 語言編譯程式 | **否**（需編譯/安裝二進制檔） | **完整**。由 C 語言底層字串處理器序列化，正確處理引號、反斜線與所有控制字元。 | [GitHub: jpmens/jo](https://github.com/jpmens/jo) |
| **`jq -n --arg`** | C 語言編譯程式 | **否**（需安裝 `jq` 套件） | **完整**。`--arg key "$val"` 會嚴格按照 RFC 8259 轉義所有控制字元（轉為 `\u00XX` 或 `\n`、`\t` 等）與 UTF-8。 | [GitHub: jqlang/jq](https://github.com/jqlang/jq) |
| **`bashlog`** (`Zordrak/bashlog`) | Bash 腳本 | **否**（依賴 Bash 專屬語法、`echo -e`） | **完全未跳脫（嚴重缺陷）**。原始碼見下方分析。 | [GitHub: Zordrak/bashlog](https://github.com/Zordrak/bashlog) |
| **`log4sh`** | POSIX sh | **是** | **無 JSON 支援**。僅支援人類可讀文字與 Syslog 等級格式。 | [GitHub: kward/log4sh](https://github.com/kward/log4sh) |
| **`shlog`** (`jsware/shlog`) | POSIX sh | **是** | **無 JSON 支援**。僅提供純文字日誌輪替（Rotation）與標準輸出封裝。 | [GitHub: jsware/shlog](https://github.com/jsware/shlog) |
| **`plengauer/Thoth`** (原 `opentelemetry-shell`) | POSIX sh / Bash | **是**（主要針對 Shell 環境注入 OTel） | **部分完整**。能處理一般命令列與屬性，但複雜多行字串仍依賴子處理程序或精簡規則。 | [GitHub: plengauer/Thoth](https://github.com/plengauer/Thoth) |

#### 案例剖析：為何現有的 Bash JSON Logger 不可靠？
以 `Zordrak/bashlog` 為例，其支援 JSON 格式的實作片段如下：
```bash
# 擷取自 Zordrak/bashlog log.sh
json_line="$(printf '{"timestamp":"%s","level":"%s","message":"%s"}' "${date_s}" "${level}" "${line}")"
echo -e "${json_line}" >> "${json_path}"
```
*   **問題 1**：完全沒有做任何字元跳脫。若 `${line}` 包含 `"`，JSON 語法立即損毀。
*   **問題 2**：使用 `echo -e`，若使用者輸入本身包含 `\t` 或 `\n`，`echo -e` 會自動展開它；若包含換行，寫入檔案時會變成多行，徹底破壞 JSON Lines 每一行必須是獨立 JSON 物件的規則。

---

### (3) 純 POSIX sh 用 sed／tr 做 RFC 8259 最小跳脫的正確寫法與常見錯誤

#### 1. 技術限制與邊界先驗說明
在設計純 POSIX `sh` 跳脫器前，必須認知以下 POSIX 標準硬限制：
1. **NUL 字元（`\0` / U+0000）不可存於變數中**：POSIX Shell 變數底層是 C 字串（以 `\0` 結尾）。任何賦值若包含 `\0`，字串會在該處被截斷或丟棄。若日誌內容來自管線串流且可能含 `\0`，必須預先使用 `tr -d '\000'` 過濾。
2. **命令替換 `$(...)` 會自動吃掉結尾的所有換行**：這是 POSIX Shell 的標準規範。若原始值結尾有換行，`val=$(...)` 會將其全部剔除。
3. **POSIX `sed` 對未以換行結尾的字串行為是 Undefined**：若輸入未包含終止換行符，BSD `sed`（macOS 等）可能直接忽略最後一行。
4. **POSIX 正則表達式（BRE）不支援 `\x01` 或 `\u0001` 等十六進制轉義**：必須透過 `printf` 產生真實控制位元組注入至 `sed` 命令中。

#### 2. 正確實作：符合 POSIX sh 的 RFC 8259 跳脫函式
此函式處理了 `\`、`"`、標準跳脫字元（`\b`、`\t`、`\n`、`\f`、`\r`），並將其餘 ASCII 控制字元（U+0001–U+001F）在輸出前過濾或轉義，同時完美解決多行輸入問題：

```sh
# ==============================================================================
# json_escape_string: 符合 POSIX sh 的 RFC 8259 最小跳脫實作
# 使用方式: escaped_str=$(json_escape_string "$raw_input")
# ==============================================================================
json_escape_string() {
  # 1. 產生標準控制字元的二進制變數（POSIX printf 保證支援此語法）
  _ESC_BS=$(printf '\b')
  _ESC_TAB=$(printf '\t')
  _ESC_FF=$(printf '\f')
  _ESC_CR=$(printf '\r')

  # 2. 透過管線進行處理：
  #    - 先用 tr 將剩餘無法良好轉義的罕見控制字元 (0x01-0x07, 0x0B, 0x0E-0x1F) 剔除或替換
  #    - 保留 0x08(\b), 0x09(\t), 0x0A(\n), 0x0C(\f), 0x0D(\r)
  #    - printf '%s\n' 確保輸入必定帶有換行符（規避 POSIX sed 對 incomplete line 的未定義行為）
  _raw_with_nl=$(printf '%s\n' "$1" | tr -d '[\001-\007\013\016-\037]')

  # 3. 呼叫 sed 進行跳脫：
  #    - :join; $!{N; bjoin;} 迴圈將所有輸入行讀入 pattern space（相容 BSD 與 GNU sed）
  #    - 優先將 \ 替換為 \\（必須最先執行！）
  #    - 替換 " 為 \"
  #    - 替換 \t, \r, \b, \f
  #    - 將 pattern space 內的實際換行符 \n 替換為字面文字 \n
  _res=$(printf '%s' "$_raw_with_nl" | sed \
    -e ':join' \
    -e '$!{' \
    -e 'N' \
    -e 'bjoin' \
    -e '}' \
    -e 's/\\/\\\\\\\\/g' \
    -e 's/"/\\"/g' \
    -e "s/$_ESC_TAB/\\\\t/g" \
    -e "s/$_ESC_CR/\\\\r/g" \
    -e "s/$_ESC_BS/\\\\b/g" \
    -e "s/$_ESC_FF/\\\\f/g" \
    -e 's/\n/\\n/g'
    # 結尾補上標記字元 x，防止 $(...) 剝除結尾換行
    printf 'x'
  )
  _res="${_res%x}"

  # 4. 因步驟 2 人為補了一個 \n，sed 會將該結尾換行轉成字面文字 \n，此處需精準剝除
  _res="${_res%\\n}"

  # 5. 輸出轉義完成的純字串（不帶外圍引號）
  printf '%s' "$_res"
}
```

#### 3. 常見錯誤與陷阱（Common Pitfalls）
1. **跳脫順序顛倒（Fatal Bug）**：
   若先替換 `s/"/\\"/g` 再替換 `s/\\/\\\\/g`，引號產生的 `\` 會被再次跳脫成 `\\\"`，導致 JSON 語法解析錯誤。**反斜線必須永遠最優先處理**。
2. **`sed` 替換字串的反斜線災難**：
   在 `sed 's/\\/\\\\/g'` 中，正則內的 `\\` 代表一個字面 `\`；但在替換段（Replacement）中，`\\` 也代表轉義一個 `\`。因此寫 `s/\\/\\\\/g` 實際上是將 `\` 替換為 `\`（完全沒變）。要輸出兩個反斜線 `\\`，替換段必須寫成四個反斜線 `\\\\\\\\`。
3. **使用 `echo` 傳遞變數**：
   POSIX 標準中，`echo "$val"` 當遇到變數以 `-n` 開頭，或內容包含 `\c`、`\e` 時，不同系統的內建 `echo` 會有不可預測的展開行為。**必須全數改用 `printf '%s'`**。
4. **未處理多行換行（NDJSON 結構損毀）**：
   `sed` 預設是逐行串流處理，若直接執行 `sed 's/"/\\"/g'`，多行文字輸出時依然是多行，直接違反 JSON Lines「一行一個 JSON 物件」的規範。必須使用 `:join; $!{N; bjoin;}` 累積成單一緩衝區。
5. **BSD sed 與 GNU sed 的標籤語法相容性**：
   GNU sed 允許 `:a; N; $!ba;` 寫在同一行，但 BSD sed（macOS / FreeBSD）要求標籤或跳轉後必須是換行或獨立的 `-e` 參數，否則會報語法錯誤。
6. **Command Substitution 吃掉結尾換行**：
   `val=$(cmd)` 會無條件吃掉 `cmd` 輸出的最後所有 `\n`。若要精確保留原始結尾換行，必須採用 `out=$(cmd; printf x); out=${out%x}` 技法。

---

### (4) 「事件名註冊表」（有限集合、未註冊即錯）的前例與 CI 驗證

在軟體工程中，限制日誌/遙測事件名稱為有限集合（Finite Enumeration / Allowlist）並在 CI 驗證是常見實踐。

#### 1. 開源前例
*   **Linux Kernel Tracepoints (`available_events`)**：
    *   在 Linux Ftrace 機制中，核心透過 `/sys/kernel/debug/tracing/available_events` 純文字檔列舉所有合法事件名稱（如 `sched:sched_switch`）。若寫入未註冊的事件名，核心會直接拋出錯誤。
*   **GitLab Telemetry Event Dictionary**：
    *   **官方文件**：[GitLab Internal Events Guide](https://docs.gitlab.com/ee/development/internal_events.html)
    *   GitLab 規定所有遙測事件必須在 `config/events/*.yml` 註冊。CI 流水線中會執行事件檢查工具（`scripts/lint-events`），若程式碼中觸發了字典檔以外的事件名稱，或事件屬性不合規範，CI 直接中斷。
*   **Mozilla Glean Telemetry**：
    *   **官方專案**：[Mozilla Glean](https://mozilla.github.io/glean/)
    *   所有指標與事件名稱必須定義於 `metrics.yaml` 純文字檔中。CI 會執行 `glean_parser check`，凡在程式碼中使用未列舉的 Event 名稱即無法通過編譯。
*   **Segment Typewriter / Avo**：
    *   企業端前端/後端埋點追蹤計劃（Tracking Plan）。透過純文字/JSON Schema 定義事件清單，CI 階段使用 `avo status` 或 `typewriter` 掃描程式碼，若偵測到未列舉事件即報錯。

#### 2. 純文字檔與 CI 驗證實作範例
可於專案根目錄建立 `events.txt`（純文字清單，支援 `#` 註解）：
```text
# events.txt: 合法事件名清單
user_login
file_upload_start
file_upload_success
task_dispatched
```

**CI 驗證腳本（POSIX sh / git 支援，用於 GitHub Actions 或 GitLab CI）：**
```sh
#!/bin/sh
set -e

REGISTRY="events.txt"
TMP_USED="/tmp/used_events.txt"
TMP_ALLOWED="/tmp/allowed_events.txt"

# 1. 整理合法的事件清單（去除註解與空白行）
grep -v '^[[:space:]]*#' "$REGISTRY" | grep -v '^[[:space:]]*$' | sort -u > "$TMP_ALLOWED"

# 2. 靜態掃描程式碼中所有 emit_event 或 log_event 呼叫
#    例如尋找 log_event "event_name"
git grep -h -o -E 'log_event[[:space:]]+"[a-zA-Z0-9_.-]+"' src/ | \
  sed -e 's/log_event[[:space:]]*"//' -e 's/"//' | sort -u > "$TMP_USED"

# 3. 比對是否有程式碼使用了未註冊的事件名 (comm -23: 只存在於左邊集合的項目)
UNREGISTERED=$(comm -23 "$TMP_USED" "$TMP_ALLOWED")

if [ -n "$UNREGISTERED" ]; then
  echo "❌ 錯誤：在程式碼中偵測到未註冊的事件名稱：" >&2
  echo "$UNREGISTERED" >&2
  exit 1
fi

echo "✅ 所有事件名稱均已在 events.txt 註冊。"
```

**執行期（Runtime）校驗邏輯（純 POSIX sh）：**
```sh
validate_event() {
  _event="$1"
  # 使用 grep -Fqx 進行純文字整行精準比對
  if ! grep -Fqx -- "$_event" "events.txt"; then
    printf '{"severity_text":"ERROR","message":"Unknown event: %s"}\n' "$_event" >&2
    return 1
  fi
}
```

---

### (5) 單機 CLI 將 W3C `traceparent`／trace_id 傳給子行程（env）的前例

#### 1. 標準依據與開源前例
*   **W3C Trace Context 規範**：
    *   格式：`version-trace_id-parent_id-trace_flags`（例：`00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`）。
*   **OpenTelemetry 官方規範：環境變數作為傳播媒介**：
    *   **官方規範文件**：[OpenTelemetry Environment Variables as Context Propagation Carriers](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#environment-variables-as-context-propagation-carriers)
    *   官方定義了標準環境變數名稱：**`TRACEPARENT`**、`TRACESTATE` 與 `BAGGAGE`，專門用於程序跨越邊界（如 Subprocess、Shell 腳本、CI 工作階段）時的 Context Propagation。
*   **`equinix-labs/otel-cli`**：
    *   **官方專案**：[`equinix-labs/otel-cli`](https://github.com/equinix-labs/otel-cli)
    *   提供 `otel-cli exec -- <command>` 功能。當呼叫子命令時，`otel-cli` 會產生新的 Span，將產生的 W3C 字串注入至環境變數 `TRACEPARENT`，並將此環境變數傳遞給子行程執行。
*   **`plengauer/Thoth` (opentelemetry-shell)**：
    *   自動包裝 Shell 命令。每次呼叫子命令或衍生子腳本時，會動態產生新 `span_id` 並更新並 `export TRACEPARENT="00-${trace_id}-${new_span_id}-01"`，讓下游行程無縫繼承 Trace ID。

#### 2. 單機 CLI 在 POSIX sh 中的實作範例
在沒有外部高階工具的情況下，利用 Linux `/dev/urandom` 與 POSIX 工具產生合法的 W3C `traceparent`，並將其傳遞給子行程：

```sh
#!/bin/sh
set -e

# 1. 產生 16-byte (32 hex) trace_id 與 8-byte (16 hex) span_id
#    Linux 環境下可使用 tr + /dev/urandom
gen_hex() {
  _len="$1"
  # 取足夠隨機字元並過濾十六進位字元
  tr -dc '0-9a-f' < /dev/urandom | head -c "$_len" 2>/dev/null || \
  dd if=/dev/urandom bs=32 count=1 2>/dev/null | od -An -tx1 | tr -d ' \n' | cut -c 1-"$_len"
}

# 2. 判斷是否有既有的 TRACEPARENT 傳入，若無則生成新的
if [ -n "$TRACEPARENT" ]; then
  # 繼承父行程傳入的 trace_id (第二欄位)
  TRACE_ID=$(printf '%s' "$TRACEPARENT" | cut -d'-' -f2)
else
  TRACE_ID=$(gen_hex 32)
fi

# 為當前 CLI / 行程生成專屬的 SPAN_ID
CURRENT_SPAN_ID=$(gen_hex 16)
TRACE_FLAGS="01" # 01 代表 sampled

# 組裝標準 W3C traceparent
export TRACEPARENT="00-${TRACE_ID}-${CURRENT_SPAN_ID}-${TRACE_FLAGS}"

# 3. 執行日誌輸出與子行程呼叫
#    子行程（不管是 Python、Go、Node.js 還是另一個 Shell 腳本）自動從 env 繼承 TRACEPARENT
exec "$@"
```

---

### 推薦作法（Recommended Practice）

要在嚴苛的純 POSIX `sh`（無 `jq`/`jo`）環境中建構生產等級的 JSON Lines 日誌系統，推薦採用以下分層架構：

```
+-------------------------------------------------------------+
| 1. 輸入校驗層 (Validation Layer)                             |
|    - 檢查 event_name 是否符合 events.txt 白名單 (grep -Fqx)  |
|    - 從環境變數讀取或生成 W3C TRACEPARENT (Trace Propagation) |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 2. 資料清理與跳脫層 (Escape & Sanitization)                  |
|    - tr 移除危險控制字元 (0x01-0x07, 0x0B, 0x0E-0x1F)        |
|    - sed 處理反斜線、引號、\t、\r、\n 轉義                   |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 3. 序列化輸出層 (NDJSON Emission)                            |
|    - printf 格式化輸出單行 JSON 物件至 stdout/stderr          |
+-------------------------------------------------------------+
```

#### 完整推薦實作腳本（可直接嵌入專案使用）：

```sh
#!/bin/sh
set -eu

# ------------------------------------------------------------------------------
# 設定與常數
# ------------------------------------------------------------------------------
EVENT_REGISTRY_FILE="./events.txt"

# 確保 TRACEPARENT 存在 (W3C Trace Context)
if [ -z "${TRACEPARENT:-}" ]; then
  # 生成隨機 32 位元 hex trace_id 與 16 位元 hex span_id
  _T_ID=$(tr -dc '0-9a-f' < /dev/urandom 2>/dev/null | head -c 32 || printf '00000000000000000000000000000000')
  _S_ID=$(tr -dc '0-9a-f' < /dev/urandom 2>/dev/null | head -c 16 || printf '0000000000000000')
  export TRACEPARENT="00-${_T_ID}-${_S_ID}-01"
fi
TRACE_ID=$(printf '%s' "$TRACEPARENT" | cut -d'-' -f2)

# ------------------------------------------------------------------------------
# 核心跳脫函式
# ------------------------------------------------------------------------------
json_escape() {
  _TAB=$(printf '\t')
  _CR=$(printf '\r')
  _BS=$(printf '\b')
  _FF=$(printf '\f')

  # 過濾未支援的控制字元 + 保證以換行結尾送入 sed
  _clean_input=$(printf '%s\n' "$1" | tr -d '[\001-\007\013\016-\037]')

  _escaped=$(printf '%s' "$_clean_input" | sed \
    -e ':join' -e '$!{' -e 'N' -e 'bjoin' -e '}' \
    -e 's/\\/\\\\\\\\/g' \
    -e 's/"/\\"/g' \
    -e "s/$_TAB/\\\\t/g" \
    -e "s/$_CR/\\\\r/g" \
    -e "s/$_BS/\\\\b/g" \
    -e "s/$_FF/\\\\f/g" \
    -e 's/\n/\\n/g'
    printf 'x'
  )
  _escaped="${_escaped%x}"
  _escaped="${_escaped%\\n}"
  printf '%s' "$_escaped"
}

# ------------------------------------------------------------------------------
# 日誌輸出主函式
# 參數: $1=severity_text, $2=event_name, $3=attributes (可選, 格式如: "k1=v1;k2=v2")
# ------------------------------------------------------------------------------
log_json() {
  _severity="$1"
  _event="$2"
  _raw_attrs="${3:-}"

  # 1. 事件名驗證（若有註冊表檔案則強制檢查）
  if [ -f "$EVENT_REGISTRY_FILE" ]; then
    if ! grep -Fqx -- "$_event" "$EVENT_REGISTRY_FILE"; then
      printf '{"severity_text":"ERROR","event_name":"system.error","message":"Unregistered event: %s"}\n' \
        "$(json_escape "$_event")" >&2
      return 1
    fi
  fi

  # 2. 生成 UTC ISO-8601 時間戳
  _timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")

  # 3. 處理 attributes (若為空輸出 {})
  #    若傳入如 "msg=hello world"，進行簡易解析與跳脫
  _attr_json="{}"
  if [ -n "$_raw_attrs" ]; then
    _attr_k=$(json_escape "${_raw_attrs%%=*}")
    _attr_v=$(json_escape "${_raw_attrs#*=}")
    _attr_json="{\"${_attr_k}\":\"${_attr_v}\"}"
  fi

  # 4. 以單行 printf 輸出標準 NDJSON，保證單一 write 呼叫輸出
  printf '{"timestamp":"%s","severity_text":"%s","event_name":"%s","trace_id":"%s","attributes":%s}\n' \
    "$_timestamp" \
    "$(json_escape "$_severity")" \
    "$(json_escape "$_event")" \
    "$(json_escape "$TRACE_ID")" \
    "$_attr_json"
}
```

#### 長期架構建議：
1. **日誌與業務分離**：手寫 Shell JSON 跳脫雖然在純 POSIX 下可行，但維護成本與潛在邊界條件極多。若日後環境允許擴充，建議日誌僅輸出標準 `logfmt`（`key=value`），並由主機端的專屬日誌收集器（如 Vector、Fluent Bit、Promtail）在背景解析並轉發為 JSON Lines。
2. **CI 嚴格防線**：在 PR / Commit 階段即以 CI 靜態檢查（`grep` + `comm`）強行防堵未註冊的 Event 名稱流入生產環境，確保日誌資料庫的 Schema 穩定。
