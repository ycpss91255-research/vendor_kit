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
# 救援路徑用到的部分（掛載點、控制檔名、in/ 的引擎引用檔名、hdr、done、fld、ok／failed 與 pull、load、
# inspect、extract、stage）跨介面版永久不變（#372 維護者 10/05 定救援路徑協定選 A）；改了就破壞救援，P+1 也不能改。
#
# 介面版 2 起（ADR-0008:25 的 P+1；#723、#724）：多了 pull-tag、rm-sessions 兩個 op，runner 的 image 欄改用自由文字欄。
# 這三樣只在 header 的 P ≥ 2 時收；P = 1 的 req 照原本的文法（舊薄殼配新引擎時，引擎以 P = 1 回應、不送新 op）。

vk_wire_grammar=vk-resolve
# op 的封閉集合，依文法的順序（engine/plan 的 OPS），兩邊相等；wire.bats 比對兩份清單。
# stage-dir（N48，開發來源的目錄）只給 dev 用，不屬救援路徑。
# pull-tag、rm-sessions 是介面版 2 起才有的 op（vk_wire_since_v2），不屬救援路徑。
vk_wire_ops=(pull load inspect extract stage stage-dir ps rm-container runner pull-tag rm-sessions)
# 介面版 2 起才收的 op；P = 1 的 req 送這些算協定不合。
vk_wire_since_v2=(pull-tag rm-sessions)
# 引擎入口的具名選項，依傳的順序（engine/plan 的 argv::ORDER），之後接 `--`。
vk_wire_argv=(--protocol --run-id --host-root --host-cwd --run-log --tty --no-color)
# 引擎容器內的掛載點（engine/plan 的 mount）。
vk_wire_mount_root=/vk/root
vk_wire_mount_ctl=/vk/ctl
vk_wire_mount_in=/vk/in
# in/ 裡啟動器放的引擎引用檔（容器內 /vk/in/engine）：這次起的引擎 image 的 pinned 引用，一行、LF 結尾。
# 引擎 image 不可能含有自己的 index digest，救援 argv 又凍結，所以由這個檔交給引擎（N37）。
# 不會跟 tool<N> 的 slot 撞名；stage、stage-dir、extract 遇到已存在的 slot 一律拒絕，也蓋不掉這個檔。
vk_wire_in_engine=engine
# in/ 裡 bootstrap.sh 首次導入時放的來源檔（容器內 /vk/in/bootstrap）：`$0` 與 bootstrap.sh 收到的全部參數，
# 每個寫成一個自由文字欄（fld），以一個空白分隔，一行、LF 結尾。引擎用它組 VK0002 的重跑指令（B2）。
# install 是救援呼叫、入口 argv 凍結，所以比照 res.<seq>.out 的前例放進 in/；引擎讀時允許檔不存在。
vk_wire_in_bootstrap=bootstrap

# 各欄的型別（engine/plan 的 ABNF）。fld 的 0x21–0x7E 不含反斜線 0x5C；八進位只收 001–377。
vk_wire_re_proto='^[1-9][0-9]{0,9}$'
vk_wire_re_run_id='^[a-z0-9-]{1,64}$'
vk_wire_re_seq='^[1-9][0-9]{0,3}$'
vk_wire_re_exit='^[0-3]$'
vk_wire_re_ref='^[a-z0-9][a-z0-9._/:@-]*$'
vk_wire_re_pinned='^[^@]+@sha256:[0-9a-f]{64}$'
# pull-tag 的 tag（最後一個 / 之後、: 之後那段）：Docker 的 tag 文法 [\w][\w.-]{0,127} 裡 ref 收得下的子集。
vk_wire_re_tag='^[a-z0-9_][a-z0-9_.-]{0,127}$'
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

# vk_wire_encode <value>：把值編成自由文字欄（engine/plan 的 Field::encode，同一個值只有一種位元組），放進 REPLY。
# 0x21–0x7E 照原樣，反斜線、空白、控制字元與 0x7F 以上一律寫成三位八進位。值不能含 NUL（bash 字串本來就存不了）。
vk_wire_encode() {
    local LC_ALL=C s=$1 c o i
    REPLY=e:
    for ((i = 0; i < ${#s}; i++)); do
        c=${s:i:1}
        printf -v o '%d' "'$c"
        if ((o < 0)); then
            o=$((o + 256))
        fi
        if ((o >= 0x21 && o <= 0x7e && o != 0x5c)); then
            REPLY+=$c
        else
            printf -v c '\\%03o' "$o"
            REPLY+=$c
        fi
    done
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

# vk_wire_tagged <token>：pull-tag 的運算元，不帶 digest 的 `<路徑>:<tag>`：是 ref、不含 @，最後一個 / 之後有 :，
# 那個 : 之後是 tag（vk_wire_re_tag）。
vk_wire_tagged() {
    local LC_ALL=C last
    [[ $1 =~ $vk_wire_re_ref && $1 != *@* ]] || return 1
    last=${1##*/}
    [[ $last == *:* && ${last##*:} =~ $vk_wire_re_tag ]]
}

# vk_wire_runner_image <token> <P>：runner 的 image 欄，合格的值放進 REPLY。P = 1 是 ref（只收小寫）；
# P ≥ 2 是自由文字欄，解碼後非空、不以 - 開頭（不讓 docker create 當成選項），其餘照 Docker 自己的規則判。
vk_wire_runner_image() {
    local LC_ALL=C
    if (($2 < 2)); then
        vk_wire_ref "$1" || return 1
        REPLY=$1
        return 0
    fi
    vk_wire_field "$1" || return 1
    [[ -n $REPLY && $REPLY != -* ]]
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
    if ((proto < 2)); then
        for o in "${vk_wire_since_v2[@]}"; do
            if [[ $o == "$name" ]]; then
                REPLY="op $name needs interface version 2 or later"
                return 1
            fi
        done
    fi
    if ! vk_wire_operands "$name" "$n" "$proto" "${op[@]:1}"; then
        REPLY="invalid operands for op $name"
        return 1
    fi
    vk_req_op=$name
    return 0
}

# vk_wire_operands <op> <個數> <P> <運算元>...：逐欄驗證，合格的值（自由文字欄已解碼）放進 vk_req_args；不合回 1。
vk_wire_operands() {
    local LC_ALL=C name=$1 n=$2 proto=$3
    shift 3
    vk_req_args=()
    case $name in
    pull | inspect)
        local form=
        if [[ $name == pull ]]; then
            form=pinned
        fi
        if ((n != 1)) || ! vk_wire_ref "$1" "$form"; then
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
    stage-dir)
        # 運算元跟 stage 一樣：主機上的絕對路徑（自由文字欄）與 slot；複製的是目錄。不屬救援路徑。
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
    pull-tag)
        # 介面版 2 起：依 tag 下載（D7），由主機 Docker（含它的登入）pull；不屬救援路徑，救援的 pull 文法不動。
        if ((n != 1)) || ! vk_wire_tagged "$1"; then
            return 1
        fi
        vk_req_args=("$1")
        ;;
    rm-sessions)
        # 介面版 2 起：prune 請啟動器清殘留的 session 目錄（D14）；沒有運算元，刪哪些由啟動器證明歸屬後決定。
        ((n == 0)) || return 1
        ;;
    runner)
        if ((n < 2)) || ! vk_wire_runner_image "$1" "$proto"; then
            return 1
        fi
        vk_req_args=("$REPLY")
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
