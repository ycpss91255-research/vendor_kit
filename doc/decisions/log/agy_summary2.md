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
