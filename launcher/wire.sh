# shellcheck shell=bash
# 啟動器端的 vk-resolve/<P> 文法（#372 的 D2）：驗證並解碼引擎寫的 req.<seq> 與 done，寫出 res.<seq> 的位元組。
#
# 規範是 engine/plan 的 crate 文件（engine/plan/src/lib.rs 的 ABNF）；這裡逐欄鏡射同一份規則，
# launcher/test/wire.bats 用 engine/plan/src/tests.rs 的 golden 與拒絕清單比對。
#
# 讀檔的順序固定（ADR-0012:22）：先查 NUL（bash 變數存不了 NUL，讀進來就看不到了），再以 `IFS= read -r`
# 逐行讀、逐欄比對該型別的正規式，全部合格後才解碼自由文字欄。解碼用 `printf -v` 的 `%b`，
# 不用 eval、source 或 command substitution（command substitution 會吃掉尾端換行）。
#
# 這裡的變數由 launch.sh 使用。
# shellcheck disable=SC2034
#
# 救援路徑用到的部分（掛載點、控制檔名、hdr、done、fld、ok／failed 與 pull、load、inspect、extract、stage）
# 跨介面版永久不變（#372 維護者 10/05 定救援路徑協定選 A）；改了就破壞救援，P+1 也不能改。

vk_wire_grammar=vk-resolve
# op 的封閉集合，依文法的順序（engine/plan 的 OPS）。
vk_wire_ops=(pull load inspect extract stage ps rm-container runner)
# 引擎入口的具名選項，依傳的順序（engine/plan 的 argv::ORDER），之後接 `--`。
vk_wire_argv=(--protocol --run-id --host-root --host-cwd --run-log --tty --no-color)
# 引擎容器內的掛載點（engine/plan 的 mount）。
vk_wire_mount_root=/vk/root
vk_wire_mount_ctl=/vk/ctl
vk_wire_mount_in=/vk/in

# 各欄的型別（engine/plan 的 ABNF）。fld 的 0x21–0x7E 不含反斜線 0x5C；八進位只收 001–377。
vk_wire_re_proto='^[1-9][0-9]{0,9}$'
vk_wire_re_run_id='^[a-z0-9-]{1,64}$'
vk_wire_re_seq='^[1-9][0-9]{0,3}$'
vk_wire_re_exit='^[0-3]$'
vk_wire_re_ref='^[a-z0-9][a-z0-9._/:@-]*$'
vk_wire_re_pinned='^[^@]+@sha256:[0-9a-f]{64}$'
vk_wire_re_imgid='^sha256:[0-9a-f]{64}$'
vk_wire_re_cid='^[0-9a-f]{64}$'
vk_wire_re_slot='^[a-z0-9]{1,16}$'
vk_wire_re_rc='^(0|[1-9][0-9]?|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
vk_wire_re_fld='^e:([!-[]|[]-~]|\\(00[1-7]|0[1-7][0-7]|[1-3][0-7][0-7]))*$'
# 一行：可見 ASCII 以單一空白分欄，開頭、結尾與連續的空白都不收（也就擋掉 CR、TAB 與非 ASCII）。
vk_wire_re_line='^[!-~]+( [!-~]+)*$'

# vk_wire_read <file> <N>：讀成剛好 N 行放進陣列 vk_wire_lines；不合時把原因放進 REPLY、回 1。
vk_wire_read() {
    local LC_ALL=C file=$1 n=$2 line=
    vk_wire_lines=()
    if [[ ! -f $file || ! -r $file ]]; then
        REPLY="cannot read control file ${file##*/}"
        return 1
    fi
    # read -d '' 讀到 NUL 才回 0；沒有 NUL 時讀到檔尾回 1。
    if IFS= read -r -d '' line <"$file"; then
        REPLY="control file ${file##*/} has a NUL byte"
        return 1
    fi
    line=
    {
        while IFS= read -r line; do
            vk_wire_lines+=("$line")
            line=
        done
    } <"$file"
    if [[ -n $line ]]; then
        REPLY="control file ${file##*/} does not end with LF"
        return 1
    fi
    if ((${#vk_wire_lines[@]} != n)); then
        REPLY="control file ${file##*/} must have exactly $n line(s)"
        return 1
    fi
    for line in "${vk_wire_lines[@]}"; do
        if [[ ! $line =~ $vk_wire_re_line ]]; then
            REPLY="control file ${file##*/} has a malformed line"
            return 1
        fi
    done
    return 0
}

# vk_wire_header <P> <run-id> <第一欄> <第二欄>：前兩欄是不是 `vk-resolve/<P> <run-id>`。
vk_wire_header() {
    [[ $3 == "$vk_wire_grammar/$1" && $4 == "$2" ]]
}

# vk_wire_field <token>：驗證並解碼自由文字欄，值放進 REPLY；不合回 1。
vk_wire_field() {
    local LC_ALL=C tok=$1
    if [[ ! $tok =~ $vk_wire_re_fld ]]; then
        return 1
    fi
    tok=${tok#e:}
    # 驗過之後每個反斜線後面都是三位八進位；改寫成 %b 的 \0nnn。
    printf -v REPLY '%b' "${tok//\\/\\0}"
}

# vk_wire_ref <token> [pinned]：image 引用；給 pinned 時還要以 @sha256:<64 位小寫 hex> 結尾、全串只有一個 @。
vk_wire_ref() {
    local LC_ALL=C
    [[ $1 =~ $vk_wire_re_ref ]] || return 1
    if [[ ${2:-} == pinned ]]; then
        [[ $1 =~ $vk_wire_re_pinned ]] || return 1
    fi
    return 0
}

# vk_wire_parse_req <file> <P> <run-id> <seq>：讀 req.<seq>。成功時 op 名放進 vk_req_op，
# 運算元（自由文字欄已解碼）放進陣列 vk_req_args；不合時把原因放進 REPLY、回 1。
vk_wire_parse_req() {
    local LC_ALL=C file=$1 proto=$2 run_id=$3 seq=$4
    vk_req_op=
    vk_req_args=()
    vk_wire_read "$file" 2 || return 1
    local -a hdr op
    read -r -a hdr <<<"${vk_wire_lines[0]}"
    read -r -a op <<<"${vk_wire_lines[1]}"
    if ((${#hdr[@]} != 3)) || ! vk_wire_header "$proto" "$run_id" "${hdr[0]}" "${hdr[1]}"; then
        REPLY="request header does not match $vk_wire_grammar/$proto $run_id"
        return 1
    fi
    if [[ ! ${hdr[2]} =~ $vk_wire_re_seq || ${hdr[2]} != "$seq" ]]; then
        REPLY="request seq ${hdr[2]} does not match the expected seq $seq"
        return 1
    fi
    local name=${op[0]} n=$((${#op[@]} - 1)) known=0 o
    for o in "${vk_wire_ops[@]}"; do
        if [[ $o == "$name" ]]; then
            known=1
        fi
    done
    if ((!known)); then
        REPLY="unknown op $name"
        return 1
    fi
    if ! vk_wire_operands "$name" "$n" "${op[@]:1}"; then
        REPLY="invalid operands for op $name"
        return 1
    fi
    vk_req_op=$name
    return 0
}

# vk_wire_operands <op> <個數> <運算元>...：逐欄驗證，合格的值（自由文字欄已解碼）放進 vk_req_args；不合回 1。
vk_wire_operands() {
    local LC_ALL=C name=$1 n=$2
    shift 2
    vk_req_args=()
    case $name in
    pull | inspect)
        local want=
        if [[ $name == pull ]]; then
            want=pinned
        fi
        if ((n != 1)) || ! vk_wire_ref "$1" "$want"; then
            return 1
        fi
        vk_req_args=("$1")
        ;;
    load)
        if ((n != 1)) || ! vk_wire_field "$1" || [[ $REPLY != /* ]]; then
            return 1
        fi
        vk_req_args=("$REPLY")
        ;;
    extract)
        if ((n != 2)) || [[ ! $1 =~ $vk_wire_re_imgid || ! $2 =~ $vk_wire_re_slot ]]; then
            return 1
        fi
        vk_req_args=("$1" "$2")
        ;;
    stage)
        if ((n != 2)) || [[ ! $2 =~ $vk_wire_re_slot ]] || ! vk_wire_field "$1" || [[ $REPLY != /* ]]; then
            return 1
        fi
        vk_req_args=("$REPLY" "$2")
        ;;
    ps)
        ((n == 0)) || return 1
        ;;
    rm-container)
        if ((n != 1)) || [[ ! $1 =~ $vk_wire_re_cid ]]; then
            return 1
        fi
        vk_req_args=("$1")
        ;;
    runner)
        if ((n < 2)) || ! vk_wire_ref "$1"; then
            return 1
        fi
        vk_req_args=("$1")
        shift
        local a
        for a in "$@"; do
            vk_wire_field "$a" || return 1
            vk_req_args+=("$REPLY")
        done
        ;;
    *) return 1 ;;
    esac
    return 0
}

# vk_wire_result_ok <op> <result>：result 這一行能不能回給 op（runner 只回 runner …，其他只回 ok／failed rc）。
vk_wire_result_ok() {
    local LC_ALL=C kind=$1 line=$2
    local -a w
    read -r -a w <<<"$line"
    if [[ $kind != runner ]]; then
        [[ $line == ok ]] || [[ ${#w[@]} -eq 2 && ${w[0]} == failed && ${w[1]} =~ $vk_wire_re_rc ]]
        return
    fi
    if [[ ${w[0]:-} != runner ]]; then
        return 1
    fi
    if ((${#w[@]} == 2)); then
        [[ ${w[1]} == notstarted ]]
    elif ((${#w[@]} == 3)); then
        [[ (${w[1]} == exited && ${w[2]} =~ $vk_wire_re_rc) ||
            (${w[1]} == stopped && (${w[2]} == unavailable || ${w[2]} =~ $vk_wire_re_rc)) ]]
    else
        return 1
    fi
}

# vk_wire_res <P> <run-id> <seq> <result>：res.<seq> 的確切位元組放進 REPLY（尾端有 LF）。
vk_wire_res() {
    REPLY="$vk_wire_grammar/$1 $2 $3"$'\n'"$4"$'\n'
}

# vk_wire_parse_done <file> <P> <run-id>：讀 done，引擎的結束碼（0–3）放進 REPLY；不合時原因放進 REPLY、回 1。
vk_wire_parse_done() {
    local LC_ALL=C file=$1 proto=$2 run_id=$3
    vk_wire_read "$file" 1 || return 1
    local -a t
    read -r -a t <<<"${vk_wire_lines[0]}"
    if ((${#t[@]} != 4)) || ! vk_wire_header "$proto" "$run_id" "${t[0]}" "${t[1]}" || [[ ${t[2]} != "done" || ! ${t[3]} =~ $vk_wire_re_exit ]]; then
        REPLY="invalid done line"
        return 1
    fi
    REPLY=${t[3]}
}

# vk_wire_mount_source <path>：--mount 的 source 欄（docker/cli 的 CSV 規則：整欄加雙引號、欄內雙引號寫兩次）。
# 這一層與 shell 引號分開；呼叫端照樣把整個 --mount 值加引號傳。
vk_wire_mount_source() {
    REPLY="\"source=${1//\"/\"\"}\""
}

# vk_wire_mount_target <path>：--mount 的 target 欄，寫法同 source。
vk_wire_mount_target() {
    REPLY="\"target=${1//\"/\"\"}\""
}
