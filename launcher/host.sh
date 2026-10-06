# shellcheck shell=bash
# 主機前置檢查（ADR-0007:17–20、29–30；04 主機需求）。
#
# - 這些檢查沒有副作用，排在建執行紀錄之前：失敗時只在 stderr 印診斷（diag.sh），回非零，
#   呼叫端以 vk_diag_exit（2）結束，不建執行紀錄、不寫檔。
# - VK recipe 的主機前置檢查排在用法之前（用法只有引擎判得出，#497）；bootstrap.sh 自己的判定順序
#   （04 bootstrap.sh 的判定順序、單獨 -h 不做主機檢查）由 bootstrap.sh 決定什麼時候呼叫這裡。
# - 只呼叫 docker 與 just 本身；主機不呼叫 git，「在 git repo 裡」以往上找 `.git` 判斷。
# - 讀版本鎖定行的引擎行（vk_lock_engine_ref）也在這裡：同樣沒有副作用、排在建紀錄之前，
#   薄殼的 log.sh（main.sh）與 bootstrap.sh 共用，各自決定讀不出時報哪一條診斷。
#   本機覆寫的引擎行（vk_local_engine_ref，讀 version.local.toml）用同一套讀法，只有薄殼的 log.sh 讀；
#   bootstrap.sh 不讀（04 用哪一版引擎：檢查、修復不套用本機覆寫）。
#   引擎行旁記的介面版列表（vk_lock_protocols）同樣只讀不寫，由 launch.sh 的介面版判定在建紀錄之後讀：
#   救援呼叫不讀它，列表缺漏或格式錯時救援路徑仍可用（N13）。
#
# 模式名與 engine/runlog 的 Mode 相同：initial_import、check、repair、recipe。

vk_docker_min=19.03
vk_just_min=1.33.0

# vk_version_ge <have> <want>：以點分開的數字逐段比，have >= want 回 0。缺的段當 0。
vk_version_ge() {
    local -a have want
    IFS=. read -r -a have <<<"$1"
    IFS=. read -r -a want <<<"$2"
    local i n=${#want[@]}
    if ((${#have[@]} > n)); then
        n=${#have[@]}
    fi
    for ((i = 0; i < n; i++)); do
        local h=$((10#${have[i]:-0})) w=$((10#${want[i]:-0}))
        if ((h != w)); then
            ((h > w))
            return
        fi
    done
    return 0
}

# vk_parse_version <text>：取 text 裡第一個 `數字.數字[.數字]` 放進 REPLY，沒有就回 1。
vk_parse_version() {
    if [[ $1 =~ ([0-9]+)\.([0-9]+)(\.([0-9]+))? ]]; then
        REPLY=${BASH_REMATCH[0]}
        return 0
    fi
    return 1
}

# vk_check_docker：找不到 docker（VK0033）→ 輸出含 podman（VK0011，不分大小寫）→ 低於 19.03（VK0012）。
# 讀不出版本時當成版本不足，<version> 印 unknown。
vk_check_docker() {
    if ! command -v docker >/dev/null 2>&1; then
        vk_diag VK0033
        return 1
    fi
    local out
    out=$(docker --version 2>&1)
    if [[ ${out,,} == *podman* ]]; then
        vk_diag VK0011
        return 1
    fi
    local version=unknown
    if vk_parse_version "$out"; then
        version=$REPLY
    fi
    if [[ $version == unknown ]] || ! vk_version_ge "$version" "$vk_docker_min"; then
        vk_diag VK0012 version "$version"
        return 1
    fi
    return 0
}

# vk_check_just <download_url> <install_command>：找不到 just（VK0034）→ 低於 1.33.0（VK0005）。
# 兩個占位符由呼叫端（bootstrap.sh）填好；讀不出版本時當成版本不足，<version> 印 unknown。
vk_check_just() {
    local download_url=$1 install_command=$2
    if ! command -v just >/dev/null 2>&1; then
        vk_diag VK0034 download_url "$download_url" install_command "$install_command"
        return 1
    fi
    local out version=unknown
    out=$(just --version 2>&1)
    if vk_parse_version "$out"; then
        version=$REPLY
    fi
    if [[ $version == unknown ]] || ! vk_version_ge "$version" "$vk_just_min"; then
        vk_diag VK0005 version "$version" download_url "$download_url" install_command "$install_command"
        return 1
    fi
    return 0
}

# vk_host_precheck <mode> [<download_url> <install_command>]：三種 bootstrap 模式與 VK recipe 都檢查 docker；
# just 只在首次導入檢查（已有安裝目錄時由 just 解析 justfile 時自己拒絕，ADR-0007:19）。
vk_host_precheck() {
    local mode=$1
    case $mode in
    initial_import | check | repair | recipe) ;;
    *)
        vk_diag VK0056 reason "unknown launcher mode $mode" path none
        return 1
        ;;
    esac
    vk_check_docker || return 1
    if [[ $mode == initial_import ]]; then
        vk_check_just "$2" "$3" || return 1
    fi
    return 0
}

# vk_find_git [<dir>]：從 dir（預設目前目錄）往上找 `.git`（目錄或檔都算，適用 worktree 與 submodule）。
# 找到就把那一層目錄放進 REPLY；找不到印 VK0035 回 1。不呼叫 git，也不建 repo。
vk_find_git() {
    local dir=${1:-$PWD}
    while :; do
        if [[ -e $dir/.git ]]; then
            REPLY=${dir:-/}
            return 0
        fi
        if [[ -z $dir || $dir == / ]]; then
            break
        fi
        dir=${dir%/*}
    done
    vk_diag VK0035
    return 1
}

# vk_engine_line <file> <what> <pinned|any>：讀 file 裡的引擎行，值放進 REPLY，回 0。
# 引擎行是符合 `^vendor_kit[[:space:]]*=` 的行（ADR-0002；`vendor_kit_protocols` 不算），以 `while read` 加字串
# 比對，不用 grep；行尾的 CR 先去掉（ADR-0012：CRLF 與 LF 等價）。只讀到雙引號為止，其餘的形狀由引擎檢查。
# 檔不存在算命中 0 行。pinned（版本鎖定行）要命中恰好 1 行、值是 pinned 引用；any（本機覆寫）命中 0 或 1 行，
# 0 行時 REPLY 是空字串，值只要是 image 引用（wire.sh 的 vk_wire_ref；例如 `vendor_kit:dev` 或 image ID）。
# what 是原因裡的名稱（`engine lock`、`engine override`）。讀不出（命中數不合、值不是雙引號裡的引用、檔讀不到）
# 時不印診斷，把原因（英文、不含結尾句點）放進 REPLY、回 1。
vk_engine_line() {
    local file=$1 what=$2 kind=$3 line hit='' n=0
    if [[ -e $file ]]; then
        if [[ ! -f $file || ! -r $file ]]; then
            REPLY="cannot read $file"
            return 1
        fi
        while IFS= read -r line || [[ -n $line ]]; do
            line=${line%$'\r'}
            if [[ $line =~ ^vendor_kit[[:space:]]*= ]]; then
                n=$((n + 1))
                hit=$line
            fi
        done <"$file"
    fi
    if [[ $kind == pinned ]] && ((n != 1)); then
        REPLY="$file has $n $what lines, exactly 1 is required"
        return 1
    fi
    if ((n > 1)); then
        REPLY="$file has $n $what lines, at most 1 is allowed"
        return 1
    fi
    if ((n == 0)); then
        REPLY=
        return 0
    fi
    local value=${hit#*=}
    value=${value#"${value%%[![:space:]]*}"}
    if [[ $value != \"*\"* ]]; then
        REPLY="the $what line in $file is not a double-quoted string"
        return 1
    fi
    value=${value#\"}
    value=${value%%\"*}
    if ! vk_wire_ref "$value" "$kind"; then
        if [[ $kind == pinned ]]; then
            REPLY="the $what line in $file is not a pinned image reference"
        else
            REPLY="the $what line in $file is not an image reference"
        fi
        return 1
    fi
    REPLY=$value
    return 0
}

# vk_lock_engine_ref <version.toml>：版本鎖定行裡引擎那一行的值（pinned 引用）放進 REPLY，回 0。
# 命中數要恰好 1；讀不出時同 vk_engine_line，不印診斷，原因放進 REPLY、回 1。
vk_lock_engine_ref() {
    vk_engine_line "$1" 'engine lock' pinned
}

# vk_local_engine_ref <version.local.toml>：本機覆寫的引擎行（`dev --engine -i` 寫的 image 引用，ADR-0010）
# 放進 REPLY，回 0；沒有覆寫（檔不存在或命中 0 行）時 REPLY 是空字串。讀不出時同 vk_engine_line、回 1。
vk_local_engine_ref() {
    vk_engine_line "$1" 'engine override' any
}

# vk_lock_protocols <version.toml>：引擎鎖定行旁記的介面版列表（`vendor_kit_protocols = "<列表>"`，N13）
# 放進 REPLY，回 0。列表是鎖定的引擎接受的介面版，由小到大、以一個空白分隔（例如 `1`、`2 3 4`）。
# 跟引擎（engine/version_file 的 parse_protocols）拒絕一樣的形狀：命中 `^vendor_kit_protocols[[:space:]]*=`
# 的行數不是 1、值不是雙引號字串、項目是 0 或有前導零、超過 32 位元無號整數、不是一個空白分隔、
# 不是連續遞增。行尾的 CR 先去掉（ADR-0012）。讀不出時不印診斷，把原因（英文、不含結尾句點）放進 REPLY、回 1。
vk_lock_protocols() {
    local LC_ALL=C file=$1 line hit='' n=0
    if [[ ! -f $file || ! -r $file ]]; then
        REPLY="cannot read $file"
        return 1
    fi
    while IFS= read -r line || [[ -n $line ]]; do
        line=${line%$'\r'}
        if [[ $line =~ ^vendor_kit_protocols[[:space:]]*= ]]; then
            n=$((n + 1))
            hit=$line
        fi
    done <"$file"
    if ((n == 0)); then
        REPLY="$file has no vendor_kit_protocols line"
        return 1
    fi
    if ((n != 1)); then
        REPLY="$file has $n vendor_kit_protocols lines, exactly 1 is required"
        return 1
    fi
    local value=${hit#*=}
    value=${value#"${value%%[![:space:]]*}"}
    if [[ $value != \"*\"* ]]; then
        REPLY="the vendor_kit_protocols line in $file is not a double-quoted string"
        return 1
    fi
    value=${value#\"}
    value=${value%%\"*}
    local -a items
    local item prev=''
    IFS=' ' read -r -a items <<<"$value"
    local joined="${items[*]}"
    if [[ -z $value ]]; then
        REPLY="the vendor_kit_protocols list in $file is empty"
        return 1
    fi
    if [[ $joined != "$value" ]]; then
        REPLY="the vendor_kit_protocols list in $file is not single-space separated"
        return 1
    fi
    for item in "${items[@]}"; do
        if [[ ! $item =~ ^[1-9][0-9]{0,9}$ ]] || ((item > 4294967295)); then
            REPLY="the vendor_kit_protocols list in $file has an invalid interface version"
            return 1
        fi
        if [[ -n $prev ]] && ((item != prev + 1)); then
            REPLY="the vendor_kit_protocols list in $file is not consecutive and ascending"
            return 1
        fi
        prev=$item
    done
    REPLY=$value
    return 0
}
