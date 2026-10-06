# shellcheck shell=bash
# bootstrap.sh 的入口（#372 的 N39 前半、N41、N93）：參數、模式判定與主機檢查（04 bootstrap.sh）。
#
# - 成品 bootstrap.sh 之後組裝：訊息片段，接著 launcher/ 的 diag、host、log、wire、launch 與這個檔，
#   前面再放內嵌引擎的引用 vk_bootstrap_engine（pinned 引用，tag 是 vX.Y.Z）。
# - 判定順序照 04 bootstrap.sh 的判定順序：
#   1. 看目前目錄的 `.vendor_kit/` 與有效鎖定行；讀不出有效鎖定行時，依最近一筆執行紀錄判定是不是
#      未完成的首次導入（vk_bootstrap_incomplete），以決定收不收 -y。
#   2. 判用法、檢查主機：三種模式都查 Docker，just 只在首次導入（含未完成的首次導入）查。
#   3. 建紀錄前判：跨 vX（VK0040）→ 往上找不到 .git（VK0035）→ 首次導入的巢狀安裝（VK0029）→
#      非安裝目錄帶 --repair（VK0039）→ 不適用例外的無效鎖定行（VK0037）。
#   被拒絕時都不建紀錄、不寫檔，只在 stderr 印診斷。單獨 -h／--help 只印用法，不做主機檢查。
# - 這一版停在「建紀錄並起引擎」之前，以 VK0056 停下（下一個 PR 接手）。
# - 參數的細節跟 engine/args 取同樣的嚴格寫法（之後放寬不破壞相容）：同一個選項給兩次（含 -y 與 --yes）
#   第二個算不允許；帶值的選項只收以空白分開的 `-i <image>`、`--image <image>`，把下一個參數原樣當值；
#   短選項不合併；單獨的 `--` 是選項結束標記，之後的參數都算多出的參數。錯誤先 VK0026（取最前面的那個），
#   再 VK0025。
# - 有效鎖定行：host.sh 的 vk_lock_engine_ref 讀得出 pinned 引用，而且 tag 是 vX.Y.Z（跨 vX 要讀 X）。
#
# 這個檔只定義函式；直接以 bash 執行組好的 bootstrap.sh 時，最後才呼叫 vk_bootstrap_main。被 source 時不執行。
# vk_wire_re_* 由 wire.sh 定義、vk_log_max_* 由 log.sh 定義。
# shellcheck disable=SC2154,SC2034 # vk_bs_image 等由下一個 PR 的建紀錄與起引擎使用

# 內嵌引擎的 pinned 引用：組裝時寫在這個檔前面；沒有就是 VK 的 bug（VK0056）。
vk_bootstrap_engine=${vk_bootstrap_engine:-}

# VK0034、VK0005 的 <download_url> 與 <install_command>（04 主機需求：用 just 的 GitHub release）。
# install_command 用 just 官方的安裝腳本裝到 ~/.local/bin；目的地已有 just 時它不覆蓋。
vk_bootstrap_just_url='https://github.com/casey/just/releases/latest'
vk_bootstrap_just_install="curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin"

# 單獨 -h／--help 印在 stdout 的用法；用法錯誤後在 stderr 附第一行。
vk_bootstrap_usage='Usage: bootstrap.sh [-i <image>] [-y] | --repair [-i <image>] | -h
  (no option)        initial import, or check the shell files of an existing install directory
  -y, --yes          initial import without prompting
  -i, --image <image>  use a local image or image tar
  --repair           regenerate mismatched shell files of an existing install directory
  -h, --help         print this usage'

# 這一版做到哪裡：通過全部檢查後的 VK0056 reason。
vk_bootstrap_pending='creating the run log and starting the engine are not implemented yet (next PR, #372)'

# ---- 參數 ----

# vk_bootstrap_parse <args>...：逐一讀參數，結果放進 vk_bs_*：
#   vk_bs_help（-- 之前 -h／--help 的個數）、vk_bs_yes／vk_bs_yes_at（-y／--yes 的原字與位置，從 0 起算）、
#   vk_bs_repair、vk_bs_image（-i 的值）、vk_bs_bad_at／vk_bs_bad（第一個不認得、多出或重複的參數）、
#   vk_bs_missing（帶值選項沒有值時 VK0025 的 <argument>）。
vk_bootstrap_parse() {
    local -a args=("$@")
    local n=$# i=0 a ended=0
    vk_bs_help=0
    vk_bs_yes=
    vk_bs_yes_at=-1
    vk_bs_repair=0
    vk_bs_image=
    vk_bs_image_set=0
    vk_bs_bad=
    vk_bs_bad_at=-1
    vk_bs_missing=
    while ((i < n)); do
        a=${args[i]}
        if ((ended)); then
            vk_bootstrap_reject "$i" "$a"
        else
            case $a in
            -h | --help) vk_bs_help=$((vk_bs_help + 1)) ;;
            -y | --yes)
                if [[ -n $vk_bs_yes ]]; then
                    vk_bootstrap_reject "$i" "$a"
                else
                    vk_bs_yes=$a
                    vk_bs_yes_at=$i
                fi
                ;;
            --repair)
                if ((vk_bs_repair)); then
                    vk_bootstrap_reject "$i" "$a"
                else
                    vk_bs_repair=1
                fi
                ;;
            -i | --image)
                if ((i + 1 >= n)); then
                    vk_bs_missing="$a <image>"
                elif ((vk_bs_image_set)); then
                    vk_bootstrap_reject "$i" "$a"
                    i=$((i + 1))
                else
                    i=$((i + 1))
                    vk_bs_image=${args[i]}
                    vk_bs_image_set=1
                fi
                ;;
            --) ended=1 ;;
            *) vk_bootstrap_reject "$i" "$a" ;;
            esac
        fi
        i=$((i + 1))
    done
}

# vk_bootstrap_reject <位置> <參數>：記下 VK0026 的候選，只留最前面的那個。
vk_bootstrap_reject() {
    if ((vk_bs_bad_at < 0 || $1 < vk_bs_bad_at)); then
        vk_bs_bad_at=$1
        vk_bs_bad=$2
    fi
}

# vk_bootstrap_help_value <args>...：-h／--help 與其他參數並用時 VK0026 的 <value>：第一個不是 -h／--help
# 的參數；全部都是 -h／--help 時是第二個參數（訊息表 VK0026）。
vk_bootstrap_help_value() {
    local a
    for a in "$@"; do
        if [[ $a != -h && $a != --help ]]; then
            REPLY=$a
            return 0
        fi
    done
    REPLY=$2
}

# vk_bootstrap_usage_error <code> <name> <value>：印用法錯誤的診斷，stderr 再附一行用法。
vk_bootstrap_usage_error() {
    vk_diag "$1" "$2" "$3"
    printf '%s\n' "${vk_bootstrap_usage%%$'\n'*}" >&2
}

# ---- 版本 ----

# vk_bootstrap_major <pinned 引用>：tag（vX.Y.Z，數值不收前導零）的 X 放進 REPLY；不合回 1。
vk_bootstrap_major() {
    local n='(0|[1-9][0-9]{0,18})'
    if [[ $1 =~ $vk_wire_re_pinned && $1 =~ ^[^@]*:v$n\.$n\.$n@sha256:[0-9a-f]{64}$ ]]; then
        REPLY=${BASH_REMATCH[1]}
        return 0
    fi
    return 1
}

# ---- 判定 1：.vendor_kit/、有效鎖定行與未完成的首次導入 ----

# vk_bootstrap_state <dir>：dir 是不是安裝目錄、有沒有有效鎖定行，結果放進 vk_bs_kind：
#   fresh（沒有 .vendor_kit/）、installed（有效鎖定行，引用放進 vk_bs_lock）、
#   incomplete（讀不出有效鎖定行，但依最近一筆執行紀錄是未完成的首次導入）、broken（其他）。
# 沒有副作用、不印診斷。
vk_bootstrap_state() {
    local dir=$1
    vk_bs_lock=
    if [[ ! -e $dir/.vendor_kit && ! -L $dir/.vendor_kit ]]; then
        vk_bs_kind=fresh
        return 0
    fi
    if vk_lock_engine_ref "$dir/.vendor_kit/version.toml"; then
        local ref=$REPLY
        if vk_bootstrap_major "$ref"; then
            vk_bs_kind=installed
            vk_bs_lock=$ref
            return 0
        fi
    fi
    if vk_bootstrap_incomplete "$dir/.vendor_kit/log"; then
        vk_bs_kind=incomplete
    else
        vk_bs_kind=broken
    fi
    return 0
}

# vk_bootstrap_incomplete <log_dir>：最近一筆執行紀錄是可唯一判定的未完成首次導入時回 0。
# 最近一筆是合格式的檔名中 ts 最大的檔（log.sh 建檔時新 ts 一定大於既有的最大值，所以時鐘回調也排在最後）；
# 沒有紀錄、最大的 ts 不只一個檔（同時執行撞名）都不套用，也不往回找更舊的紀錄。
vk_bootstrap_incomplete() {
    vk_log_max_ts "$1"
    if ((REPLY < 0 || vk_log_max_count != 1)); then
        return 1
    fi
    vk_bootstrap_assess "$vk_log_max_path"
}

# 紀錄行正規形（engine/runlog 的 json::escape）的片段：JSON 字串的一個字元、一個字串、0–255 的結束碼。
vk_bs_re_c='([^"\[:cntrl:]]|\\["\nrt]|\\u00(0[0-8bcef]|1[0-9a-f]|7f))'
vk_bs_re_s="\"$vk_bs_re_c*\""
vk_bs_re_rc='(0|[1-9][0-9]?|1[0-9]{2}|2[0-4][0-9]|25[0-5])'

# vk_bootstrap_line <line>：讀一行紀錄（不含 LF），合格時把事件名、invocation_id（JSON 原字）與事件的值
# 放進 vk_bs_ev、vk_bs_inv、vk_bs_val（mode、reason_code、target、stop_reason_code；其他事件是空字串），回 0。
# 照 engine/runlog 的 read.rs 逐欄比對正規形：鍵序固定、沒有多的鍵或空白、跳脫寫法唯一。
# 跟 read.rs 不同、這裡只看形狀的地方：訊息片段只有主機端的代碼，不在片段裡的代碼只查 VKnnnn 的形狀，
# 診斷的嚴重度只查成對（在片段裡的才跟 level 比）；不檢查 UTF-8。
vk_bootstrap_line() {
    local LC_ALL=C line=$1 s=$vk_bs_re_s c=$vk_bs_re_c rc=$vk_bs_re_rc
    local head='^\{"timestamp":"([^"]*)","severity_text":"(info|warn|error|fatal)","severity_number":(9|13|17|21),'
    head+='"event_name":"([a-z_]+)","body":('"$s"'),"resource":\{"service\.name":"vendor_kit","service\.version":('"$s"')\},'
    head+='"attributes":\{"vendor_kit\.log_format":"1","vendor_kit\.component":"(launcher|engine)","vendor_kit\.invocation_id":('"$s"')(.*)\}\}$'
    [[ $line =~ $head ]] || return 1
    local ts=${BASH_REMATCH[1]} sev=${BASH_REMATCH[2]}:${BASH_REMATCH[3]} ev=${BASH_REMATCH[4]}
    # 每個字串（$s）自己帶兩組括號，所以 body、version、invocation_id 各佔三組。
    local body=${BASH_REMATCH[5]} version=${BASH_REMATCH[8]} component=${BASH_REMATCH[11]}
    local inv=${BASH_REMATCH[12]} rest=${BASH_REMATCH[15]}
    case $sev in
    info:9 | warn:13 | error:17 | fatal:21) ;;
    *) return 1 ;;
    esac
    if [[ ! $ts =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})\.([0-9]{6})Z$ ]] ||
        ! vk_ts_name_parse "${BASH_REMATCH[1]}${BASH_REMATCH[2]}${BASH_REMATCH[3]}T${BASH_REMATCH[4]}${BASH_REMATCH[5]}${BASH_REMATCH[6]}.${BASH_REMATCH[7]}Z"; then
        return 1
    fi
    if [[ $version == '""' || $inv == '""' ]]; then
        return 1
    fi
    local want_body='' want_component=engine
    vk_bs_val=
    case $ev in
    run_started)
        want_body='Run started.'
        want_component=launcher
        [[ $rest =~ ^,\"vendor_kit\.mode\":\"(initial_import|check|repair|recipe)\",\"vendor_kit\.argv\":\[($s(,$s)*)?\]$ ]] || return 1
        vk_bs_val=${BASH_REMATCH[1]}
        ;;
    engine_started)
        want_body='Engine started.'
        [[ -z $rest ]] || return 1
        ;;
    diagnostic_emitted)
        want_component=
        [[ $rest =~ ^,\"vendor_kit\.reason_code\":\"(VK[0-9]{4})\"(,\"vendor_kit\.placeholder\.$c+\":$s)*$ ]] || return 1
        vk_bs_val=${BASH_REMATCH[1]}
        local level_var="vk_msg_${vk_bs_val}_level"
        if [[ -v $level_var ]]; then
            [[ ${sev%%:*} == "${!level_var}" ]] || return 1
        elif [[ $sev == info:9 ]]; then
            return 1
        fi
        ;;
    writes_started)
        want_body='Writes started.'
        [[ -z $rest ]] || return 1
        ;;
    lock_line_write_started | lock_line_written)
        if [[ $ev == lock_line_written ]]; then
            want_body='Lock line written.'
        else
            want_body='Lock line write started.'
        fi
        [[ $rest =~ ^,\"vendor_kit\.target\":\"(engine|tool)\"$ ]] || return 1
        vk_bs_val=${BASH_REMATCH[1]}
        ;;
    progress_removed)
        want_body='Progress file removed.'
        [[ $rest =~ ^,\"vendor_kit\.progress_file\":\"$c+\"$ ]] || return 1
        ;;
    engine_finished)
        want_body='Engine finished.'
        [[ $rest =~ ^,\"vendor_kit\.exit_code\":$rc$ ]] || return 1
        ;;
    run_finished)
        want_body='Run finished.'
        want_component=launcher
        [[ $rest =~ ^,\"vendor_kit\.exit_code\":$rc,\"vendor_kit\.engine\.exit_code\":($rc|null),\"vendor_kit\.stop_reason_code\":\"(none|VK[0-9]{4})\"$ ]] || return 1
        vk_bs_val=${BASH_REMATCH[4]}
        ;;
    *) return 1 ;;
    esac
    if [[ -n $want_body ]]; then
        [[ $body == "\"$want_body\"" && $sev == info:9 ]] || return 1
    fi
    if [[ -n $want_component && $component != "$want_component" ]]; then
        return 1
    fi
    vk_bs_ev=$ev
    vk_bs_inv=$inv
    return 0
}

# vk_bootstrap_assess <file>：engine/runlog 的 assess（讀不出有效鎖定行時）在啟動器端的鏡射：
# 紀錄是可唯一判定的未完成首次導入（條件 (a) 停在 VK0002 且沒有 writes_started，或 (b) 沒有引擎的
# lock_line_write_started）時回 0；任何一行不合、順序不合理、還沒結束都回 1。只用字串比對。
vk_bootstrap_assess() {
    local LC_ALL=C file=$1 content line first=1 inv=
    if [[ ! -f $file || ! -r $file ]]; then
        return 1
    fi
    # read -d '' 讀到 NUL 才回 0；沒有 NUL 時讀完整檔（含結尾的換行）、回 1。
    if IFS= read -r -d '' content <"$file"; then
        return 1
    fi
    if [[ -z $content || $content != *$'\n' ]]; then
        return 1
    fi
    local finished=0 writes=0 engine_lock=0 pend_engine=0 pend_tool=0 stop='' diagnosed=' '
    while IFS= read -r line; do
        vk_bootstrap_line "$line" || return 1
        if ((first)); then
            [[ $vk_bs_ev == run_started && $vk_bs_val == initial_import ]] || return 1
            inv=$vk_bs_inv
            first=0
            continue
        fi
        [[ $vk_bs_inv == "$inv" ]] || return 1
        case $vk_bs_ev in
        run_started) return 1 ;;
        engine_started) ;;
        diagnostic_emitted) diagnosed+="$vk_bs_val " ;;
        writes_started) writes=1 ;;
        progress_removed) ((writes)) || return 1 ;;
        lock_line_write_started)
            ((writes)) || return 1
            if [[ $vk_bs_val == engine ]]; then
                pend_engine=$((pend_engine + 1))
                engine_lock=1
            else
                pend_tool=$((pend_tool + 1))
            fi
            ;;
        lock_line_written)
            if [[ $vk_bs_val == engine ]]; then
                ((pend_engine > 0)) || return 1
                pend_engine=$((pend_engine - 1))
            else
                ((pend_tool > 0)) || return 1
                pend_tool=$((pend_tool - 1))
            fi
            ;;
        engine_finished) finished=1 ;;
        run_finished)
            [[ -z $stop ]] || return 1
            finished=1
            stop=$vk_bs_val
            ;;
        esac
    done <<<"${content%$'\n'}"
    if ((!finished || pend_engine > 0 || pend_tool > 0)); then
        return 1
    fi
    if [[ -n $stop && $stop != none && $diagnosed != *" $stop "* ]]; then
        return 1
    fi
    if ((!writes)) && [[ $stop == VK0002 ]]; then
        return 0
    fi
    ((!engine_lock))
}

# ---- 判定 3：建紀錄前的拒絕 ----

# vk_bootstrap_is_install_dir <dir>：dir 底下有真的 .vendor_kit/ 目錄（一般檔或 symlink 都不算，engine/layout）。
vk_bootstrap_is_install_dir() {
    [[ -d $1/.vendor_kit && ! -L $1/.vendor_kit ]]
}

# vk_bootstrap_nested <target> <repo_root>：首次導入前的巢狀判定，鏡射 engine/layout 的 check_nested。
# target 的上層（由近到遠、到 repo_root 為止、含 repo_root）或下層已有安裝目錄時，把它放進 REPLY、回 0。
# 下層依名字的位元組順序先序走訪、回報第一個；不跟 symlink、不進 .git、不算 target 自己的 .vendor_kit/。
vk_bootstrap_nested() {
    local target=$1 root=$2 dir=$1
    local prefix=${root%/}/
    if [[ $target == "$root" || $target == "$prefix"* ]]; then
        while [[ $dir != "$root" ]]; do
            dir=${dir%/*}
            dir=${dir:-/}
            if vk_bootstrap_is_install_dir "$dir"; then
                REPLY=$dir
                return 0
            fi
        done
    fi
    local had_dotglob=0 had_nullglob=0 found=1
    shopt -q dotglob && had_dotglob=1
    shopt -q nullglob && had_nullglob=1
    shopt -s dotglob nullglob
    vk_bootstrap_below "$target" 1 && found=0
    ((had_dotglob)) || shopt -u dotglob
    ((had_nullglob)) || shopt -u nullglob
    return "$found"
}

# vk_bootstrap_below <dir> <is_target>：dir 之下（is_target=1 時不含 dir 本身）先序找第一個安裝目錄。
vk_bootstrap_below() {
    local LC_ALL=C dir=$1 sub name
    if (($2 == 0)) && vk_bootstrap_is_install_dir "$dir"; then
        REPLY=$dir
        return 0
    fi
    for sub in "${dir%/}"/*/; do
        sub=${sub%/}
        name=${sub##*/}
        if [[ -L $sub || $name == .git ]] || { (($2 == 1)) && [[ $name == .vendor_kit ]]; }; then
            continue
        fi
        vk_bootstrap_below "$sub" 0 && return 0
    done
    return 1
}

# vk_bootstrap_gate <dir> <mode>：判定 3，依 04 列的順序；被拒絕時印診斷、回 1。
vk_bootstrap_gate() {
    local dir=$1 mode=$2
    if ! vk_bootstrap_major "$vk_bootstrap_engine"; then
        vk_diag VK0056 reason "the embedded engine reference is not a pinned vX.Y.Z image reference" path none
        return 1
    fi
    local bootstrap_x=$REPLY
    if [[ $vk_bs_kind == installed ]]; then
        vk_bootstrap_major "$vk_bs_lock"
        if [[ $REPLY != "$bootstrap_x" ]]; then
            vk_diag VK0040 bootstrap_X "$bootstrap_x" engine_X "$REPLY"
            return 1
        fi
    fi
    vk_find_git "$dir" || return 1
    local repo_root=$REPLY
    if [[ $mode == initial_import ]] && vk_bootstrap_nested "$dir" "$repo_root"; then
        vk_diag VK0029 existing_install_dir "$REPLY"
        return 1
    fi
    if [[ $mode == repair && $vk_bs_kind == fresh ]]; then
        vk_diag VK0039
        return 1
    fi
    if [[ $vk_bs_kind == broken || ($mode == repair && $vk_bs_kind == incomplete) ]]; then
        vk_diag VK0037
        return 1
    fi
    return 0
}

# ---- 入口 ----

# vk_bootstrap_main [<args>...]：bootstrap.sh 本體。目前目錄是要導入或已有 VK 的目錄。回傳整次的結束碼。
vk_bootstrap_main() {
    local dir=$PWD
    vk_bootstrap_parse "$@"
    if ((vk_bs_help > 0)); then
        if (($# == 1)); then
            printf '%s\n' "$vk_bootstrap_usage"
            return 0
        fi
        vk_bootstrap_help_value "$@"
        vk_bootstrap_usage_error VK0026 value "$REPLY"
        return "$vk_diag_exit"
    fi
    vk_bootstrap_state "$dir"
    # -y 只在首次導入（含未完成的首次導入）收；--repair 一律不收。
    if [[ -n $vk_bs_yes ]] && ((vk_bs_repair)) ||
        [[ -n $vk_bs_yes && $vk_bs_kind != fresh && $vk_bs_kind != incomplete ]]; then
        vk_bootstrap_reject "$vk_bs_yes_at" "$vk_bs_yes"
    fi
    if ((vk_bs_bad_at >= 0)); then
        vk_bootstrap_usage_error VK0026 value "$vk_bs_bad"
        return "$vk_diag_exit"
    fi
    if [[ -n $vk_bs_missing ]]; then
        vk_bootstrap_usage_error VK0025 argument "$vk_bs_missing"
        return "$vk_diag_exit"
    fi
    local mode
    if ((vk_bs_repair)); then
        mode=repair
    elif [[ $vk_bs_kind == fresh || $vk_bs_kind == incomplete ]]; then
        mode=initial_import
    else
        mode=check
    fi
    vk_host_precheck "$mode" "$vk_bootstrap_just_url" "$vk_bootstrap_just_install" || return "$vk_diag_exit"
    vk_bootstrap_gate "$dir" "$mode" || return "$vk_diag_exit"
    vk_diag VK0056 reason "$vk_bootstrap_pending" path none
    return "$vk_diag_exit"
}

if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
    vk_bootstrap_main "$@"
    exit "$?"
fi
