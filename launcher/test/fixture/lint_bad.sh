# shellcheck shell=bash
# 白名單 lint 的違規樣本：每個標了 bad 的命令都要被 lint 列出來。

f_plain() {
    git status # bad: git
}

f_subst() {
    local x
    x=$(curl -s https://example.invalid) # bad: curl
    printf '%s\n' "$(sed -n 1p /dev/null)" # bad: sed
}

f_ops() {
    [[ -n ${1:-} ]] && awk 1 # bad: awk
    true || grep x # bad: grep
    printf x | tr x y # bad: tr
}

f_compound() {
    if cat /dev/null; then # bad: cat
        :
    fi
    while sleep 1; do # bad: sleep
        break
    done
    (rm -f /tmp/none) # bad: rm
    local line
    while read -r line; do :; done < <(ls /) # bad: ls
    case ${1:-} in
    a | b) head -n1 /dev/null ;; # bad: head
    *) ;;
    esac
}

f_wrappers() {
    command git log # bad: git
    exec env # bad: env
    FOO=1 date # bad: date
    2>/dev/null uname # bad: uname
}

f_dynamic() {
    local cmd=docker
    "$cmd" ps # bad: dynamic
    eval "docker ps" # bad: eval
}
