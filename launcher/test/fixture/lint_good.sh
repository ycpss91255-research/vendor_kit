# shellcheck shell=bash
# 白名單 lint 的合格樣本：只用 builtin、keyword、自己的函式與白名單命令，lint 要回 0。

g_helper() {
    REPLY=ok
}

g_all() {
    local -a arr=(git curl "sed x")
    local s="git $(g_helper) curl" n=0
    [[ $s =~ ^(git|curl)\ (x|y)$ && -n ${arr[0]} ]] || n=$((n + 1))
    ((n > 0)) && printf '%s\n' "${s//git/curl}" >&2
    for ((n = 0; n < 2; n++)); do
        g_helper
    done
    for s in git curl; do :; done
    case $s in
    git | curl)
        docker --version 2>/dev/null
        ;;
    *) just --version ;;
    esac
    command -v docker >/dev/null 2>&1
    mkdir -p -- "${TMPDIR:-/tmp}/x" 2>/dev/null
    printf '%s' "a 'git' b" "$'\x01'" $'\'git'
    IFS=. read -r -a arr <<<"1.2.3"
    { printf x; } 2>/dev/null
    trap 'git status' EXIT
}
