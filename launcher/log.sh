# shellcheck shell=bash
# 執行紀錄的啟動器端寫入（ADR-0005；欄位與正規形照 engine/runlog）。
#
# - 一行一筆、LF 結尾；鍵序、空白、跳脫與 engine/runlog 的正規形逐位元組相同，
#   golden 由 launcher/test/log.bats 直接拿 engine/runlog/src/tests.rs 的 golden 行比對。
# - 啟動器只寫 run_started、diagnostic_emitted、run_finished（內嵌子集，只准少不准多；
#   launcher/test/log.bats 驗它是 engine/runlog/log-events.txt 的子集）。寫之前查子集，
#   不在子集裡是 VK 的 bug，以 VK0056 停下。
# - 紀錄檔名 `<ts>-<verb>-<id>.jsonl`，ts 是固定寬度的 UTC `YYYYMMDDTHHMMSS.ffffffZ`。
#   建檔前先找 log 目錄裡合這個格式的檔名中最大的 ts；新 ts 不大於它就取它加 1µs，
#   所以新檔一定排在最後。不合格式的檔名不算（不是啟動器建的）。建檔用 noclobber 排他建立，
#   撞名或建不出就以 VK0010 停下（這條診斷不寫進紀錄，ADR-0005:7 的例外）。
# - 同時執行不保證先後；最近一筆怎麼判定由讀取端決定（engine/runlog 的 assess）。
#
# 呼叫端先設 vk_log_version（resource."service.version"），可選 vk_log_invocation_id
# （兩端寫同一個值，只用小寫英數與 `-`；空的就產生 16 位小寫十六進位）。

vk_log_events=(run_started diagnostic_emitted run_finished)
vk_log_format=1
vk_log_file=
vk_log_version=${vk_log_version:-}
vk_log_invocation_id=${vk_log_invocation_id:-}

# vk_now_us：現在的 UNIX 時間（微秒）放進 REPLY。測試可以重新定義這個函式換成固定時鐘。
vk_now_us() {
    local t=${EPOCHREALTIME/,/.}
    local sec=${t%.*} frac=${t#*.}
    REPLY=$((sec * 1000000 + 10#$frac))
}

# vk_civil_from_days <days>：1970-01-01 起的天數 → REPLY="Y M D"（Howard Hinnant 的 civil_from_days）。
vk_civil_from_days() {
    local z=$(($1 + 719468))
    local era=$((z / 146097))
    local doe=$((z - era * 146097))
    local yoe=$(((doe - doe / 1460 + doe / 36524 - doe / 146096) / 365))
    local y=$((yoe + era * 400))
    local doy=$((doe - (365 * yoe + yoe / 4 - yoe / 100)))
    local mp=$(((5 * doy + 2) / 153))
    local d=$((doy - (153 * mp + 2) / 5 + 1))
    local m=$((mp < 10 ? mp + 3 : mp - 9))
    if ((m <= 2)); then
        y=$((y + 1))
    fi
    REPLY="$y $m $d"
}

# vk_days_from_civil <Y> <M> <D>：→ REPLY=1970-01-01 起的天數。
vk_days_from_civil() {
    local y=$((10#$1)) m=$((10#$2)) d=$((10#$3))
    if ((m <= 2)); then
        y=$((y - 1))
    fi
    local era=$((y / 400))
    local yoe=$((y - era * 400))
    local doy=$(((153 * (m > 2 ? m - 3 : m + 9) + 2) / 5 + d - 1))
    local doe=$((yoe * 365 + yoe / 4 - yoe / 100 + doy))
    REPLY=$((era * 146097 + doe - 719468))
}

# vk_ts_fields <us>：→ REPLY="YYYY MM DD hh mm ss ffffff"（補零）；早於 1970 或晚於 9999 年回 1。
vk_ts_fields() {
    local us=$1
    if ((us < 0)); then
        return 1
    fi
    local secs=$((us / 1000000)) frac=$((us % 1000000))
    local rem=$((secs % 86400))
    vk_civil_from_days $((secs / 86400))
    local y m d
    read -r y m d <<<"$REPLY"
    if ((y > 9999)); then
        return 1
    fi
    printf -v REPLY '%04d %02d %02d %02d %02d %02d %06d' \
        "$y" "$m" "$d" $((rem / 3600)) $((rem % 3600 / 60)) $((rem % 60)) "$frac"
}

# vk_ts_format <us>：紀錄行的 timestamp，`YYYY-MM-DDTHH:MM:SS.ffffffZ`（engine/runlog 的 time::format）。
vk_ts_format() {
    vk_ts_fields "$1" || return 1
    local -a f
    read -r -a f <<<"$REPLY"
    REPLY="${f[0]}-${f[1]}-${f[2]}T${f[3]}:${f[4]}:${f[5]}.${f[6]}Z"
}

# vk_ts_name <us>：紀錄檔名的 ts，`YYYYMMDDTHHMMSS.ffffffZ`（不含冒號，任何檔案系統都能用）。
vk_ts_name() {
    vk_ts_fields "$1" || return 1
    local -a f
    read -r -a f <<<"$REPLY"
    REPLY="${f[0]}${f[1]}${f[2]}T${f[3]}${f[4]}${f[5]}.${f[6]}Z"
}

# vk_ts_name_parse <ts>：vk_ts_name 的反向；只認 vk_ts_name 寫得出來的形狀（含合法日期），→ REPLY=微秒。
vk_ts_name_parse() {
    local ts=$1
    if [[ ! $ts =~ ^([0-9]{4})([0-9]{2})([0-9]{2})T([0-9]{2})([0-9]{2})([0-9]{2})\.([0-9]{6})Z$ ]]; then
        return 1
    fi
    local -a f=("${BASH_REMATCH[@]:1}")
    vk_days_from_civil "${f[0]}" "${f[1]}" "${f[2]}"
    local us=$(((REPLY * 86400 + 10#${f[3]} * 3600 + 10#${f[4]} * 60 + 10#${f[5]}) * 1000000 + 10#${f[6]}))
    vk_ts_name "$us" || return 1
    if [[ $REPLY != "$ts" ]]; then
        return 1
    fi
    REPLY=$us
}

# vk_json_str <s>：JSON 字串的正規形放進 REPLY（engine/runlog 的 json::escape）：
# `"`、`\`、LF、CR、TAB 用短寫，其他 U+0000–U+001F 與 U+007F 寫成 `\u00xx`（小寫），其餘位元組原樣。
vk_json_str() {
    local LC_ALL=C
    local s=$1
    if [[ $s != *[\"\\[:cntrl:]]* ]]; then
        REPLY="\"$s\""
        return 0
    fi
    local out='' c i
    for ((i = 0; i < ${#s}; i++)); do
        c=${s:i:1}
        if [[ $c == '"' ]]; then
            out+='\"'
        elif [[ $c == "\\" ]]; then
            out+="\\\\"
        elif [[ $c == $'\n' ]]; then
            out+='\n'
        elif [[ $c == $'\r' ]]; then
            out+='\r'
        elif [[ $c == $'\t' ]]; then
            out+='\t'
        elif [[ $c == [[:cntrl:]] ]]; then
            printf -v c '\\u%04x' "'$c"
            out+=$c
        else
            out+=$c
        fi
    done
    REPLY="\"$out\""
}

# vk_log_line <timestamp> <event> <severity_text> <severity_number> <body> [<attrs>]：
# 一行紀錄（不含 LF）放進 REPLY；attrs 是事件自己的 attribute，已是正規形、以 `,` 開頭。
vk_log_line() {
    local ts=$1 event=$2 sev_text=$3 sev_num=$4 body=$5 attrs=${6:-}
    local j_ts j_event j_body j_version j_id
    vk_json_str "$ts" && j_ts=$REPLY
    vk_json_str "$event" && j_event=$REPLY
    vk_json_str "$body" && j_body=$REPLY
    vk_json_str "$vk_log_version" && j_version=$REPLY
    vk_json_str "$vk_log_invocation_id" && j_id=$REPLY
    REPLY="{\"timestamp\":$j_ts,\"severity_text\":\"$sev_text\",\"severity_number\":$sev_num"
    REPLY+=",\"event_name\":$j_event,\"body\":$j_body"
    REPLY+=",\"resource\":{\"service.name\":\"vendor_kit\",\"service.version\":$j_version}"
    REPLY+=",\"attributes\":{\"vendor_kit.log_format\":\"$vk_log_format\",\"vendor_kit.component\":\"launcher\""
    REPLY+=",\"vendor_kit.invocation_id\":$j_id$attrs}}"
}

# vk_log_event <event> <severity_text> <severity_number> <body> [<attrs>]：查子集、取時間、寫一行。
# 不在子集裡以 VK0056 停下；寫檔失敗回 1。
vk_log_event() {
    local event=$1 known=0 e
    for e in "${vk_log_events[@]}"; do
        if [[ $e == "$event" ]]; then
            known=1
        fi
    done
    if ((!known)); then
        vk_diag VK0056 reason "event name $event is not in the event registry" path "${vk_log_file:-none}"
        return 1
    fi
    vk_now_us
    if ! vk_ts_format "$REPLY"; then
        vk_log_file=
        vk_diag VK0056 reason "the system clock is outside the supported range" path "${vk_log_file:-none}"
        return 1
    fi
    vk_log_line "$REPLY" "$@"
    { printf '%s\n' "$REPLY" >>"$vk_log_file"; } 2>/dev/null
}

# vk_log_max_ts <dir>：dir 裡合格式的紀錄檔名中最大的 ts（微秒）放進 REPLY；沒有就是 -1。
vk_log_max_ts() {
    local dir=$1 path name max=-1
    for path in "$dir"/*.jsonl; do
        name=${path##*/}
        if [[ $name =~ ^([0-9]{8}T[0-9]{6}\.[0-9]{6}Z)-[a-z0-9_]+-[0-9a-z-]+\.jsonl$ ]] &&
            vk_ts_name_parse "${BASH_REMATCH[1]}" && ((REPLY > max)); then
            max=$REPLY
        fi
    done
    REPLY=$max
}

# vk_log_start <log_dir> <verb> <mode> [<argv>...]：建紀錄檔、寫 run_started，成功後 vk_log_file 指向它。
# 建不出（含撞名）以 VK0010 停下、回 1；這條診斷不寫進紀錄。
vk_log_start() {
    local dir=$1 verb=$2 mode=$3
    shift 3
    if [[ ! $mode =~ ^(initial_import|check|repair|recipe)$ ]]; then
        vk_diag VK0056 reason "invalid run log mode $mode" path none
        return 1
    fi
    if [[ ! $verb =~ ^[a-z0-9_]+$ ]]; then
        vk_diag VK0056 reason "invalid run log verb $verb" path none
        return 1
    fi
    if [[ -z $vk_log_invocation_id ]]; then
        printf -v vk_log_invocation_id '%04x%04x%04x%04x' "$RANDOM" "$RANDOM" "$RANDOM" "$RANDOM"
    elif [[ ! $vk_log_invocation_id =~ ^[0-9a-z-]+$ ]]; then
        vk_diag VK0056 reason "invalid invocation id $vk_log_invocation_id" path none
        return 1
    fi
    if ! mkdir -p -- "$dir" 2>/dev/null; then
        vk_diag VK0010 path "$dir" reason "cannot create the log directory"
        return 1
    fi
    vk_log_max_ts "$dir"
    local max=$REPLY
    vk_now_us
    local now=$REPLY
    if ((now <= max)); then
        now=$((max + 1))
    fi
    if ! vk_ts_name "$now"; then
        vk_diag VK0056 reason "the system clock is outside the supported range" path none
        return 1
    fi
    local path="$dir/$REPLY-$verb-$vk_log_invocation_id.jsonl"
    if ! (set -C && : >"$path") 2>/dev/null; then
        if [[ -e $path ]]; then
            vk_diag VK0010 path "$path" reason "the file already exists"
        else
            vk_diag VK0010 path "$path" reason "cannot create the file"
        fi
        return 1
    fi
    local argv='' a
    for a in "$@"; do
        vk_json_str "$a"
        argv+=${argv:+,}$REPLY
    done
    vk_log_file=$path
    if ! vk_log_event run_started info 9 "Run started." ",\"vendor_kit.mode\":\"$mode\",\"vendor_kit.argv\":[$argv]"; then
        vk_log_file=
        vk_diag VK0010 path "$path" reason "cannot write to the file"
        return 1
    fi
    return 0
}

# vk_log_diagnostic <code> <level> <body> [<name> <value>]...：diagnostic_emitted（diag.sh 的 vk_diag 呼叫）。
vk_log_diagnostic() {
    local code=$1 level=$2 body=$3 num
    shift 3
    case $level in
    warn) num=13 ;;
    error) num=17 ;;
    fatal) num=21 ;;
    *) num=17 ;;
    esac
    local attrs=",\"vendor_kit.reason_code\":\"$code\"" j_name
    while (($# >= 2)); do
        vk_json_str "vendor_kit.placeholder.$1"
        j_name=$REPLY
        vk_json_str "$2"
        attrs+=",$j_name:$REPLY"
        shift 2
    done
    vk_log_event diagnostic_emitted "$level" "$num" "$body" "$attrs"
}

# vk_log_finish <exit_code> <engine_exit_code|""> <stop_reason_code|none>：run_finished；
# 沒起引擎時 engine_exit_code 給空字串，寫成 null。
vk_log_finish() {
    local engine=${2:-null}
    if [[ ! $1 =~ ^[0-9]+$ || ! $engine =~ ^([0-9]+|null)$ || ! $3 =~ ^(none|VK[0-9]{4})$ ]]; then
        vk_diag VK0056 reason "invalid run_finished fields $1 $engine $3" path "${vk_log_file:-none}"
        return 1
    fi
    vk_log_event run_finished info 9 "Run finished." \
        ",\"vendor_kit.exit_code\":$1,\"vendor_kit.engine.exit_code\":$engine,\"vendor_kit.stop_reason_code\":\"$3\""
}
