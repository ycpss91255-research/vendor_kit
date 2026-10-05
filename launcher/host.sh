# shellcheck shell=bash
# 主機前置檢查（ADR-0007:17–20、29–30；04 主機需求）。
#
# - 這些檢查沒有副作用，排在建執行紀錄之前：失敗時只在 stderr 印診斷（diag.sh），回非零，
#   呼叫端以 vk_diag_exit（2）結束，不建執行紀錄、不寫檔。
# - VK recipe 的主機前置檢查排在用法之前（用法只有引擎判得出，#497）；bootstrap.sh 自己的判定順序
#   （04 bootstrap.sh 的判定順序、單獨 -h 不做主機檢查）由 bootstrap.sh 決定什麼時候呼叫這裡。
# - 只呼叫 docker 與 just 本身；主機不呼叫 git，「在 git repo 裡」以往上找 `.git` 判斷。
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
