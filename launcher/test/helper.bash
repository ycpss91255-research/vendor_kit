# shellcheck shell=bash
# launcher/ 的 bats 共用設定。
#
# 訊息文字一律取自 msggen 產生的片段（engine/msggen --bash-out），不在測試裡另抄一份：
# 執行前設 VK_MESSAGES 指向那個檔（image/Dockerfile 的 test stage 產出 /out/bootstrap_messages.sh）。
# 測試期待的整行診斷寫死在各 .bats 裡，片段跟契約不一致時這裡會紅。

bats_require_minimum_version 1.5.0

launcher_dir=$(cd -- "$BATS_TEST_DIRNAME/.." && pwd)
repo_root=$(cd -- "$launcher_dir/.." && pwd)

common_setup() {
    vk_env=()
    if [[ -z ${VK_MESSAGES:-} || ! -r $VK_MESSAGES ]]; then
        echo "VK_MESSAGES must point to the msggen bash fragment (bootstrap_messages.sh)" >&2
        return 1
    fi
    shim="$BATS_TEST_TMPDIR/bin"
    work="$BATS_TEST_TMPDIR/work"
    mkdir -p "$shim" "$work"
    # 主機不准呼叫 git：放一個會留下記號的假 git，測試最後確認記號不存在。
    fake_cmd git 'printf called >"'"$BATS_TEST_TMPDIR"'/git_called"'
    # 受測程式的 PATH 只有 shim 目錄：白名單上的基礎 userland 才接上真的命令，其他命令一律找不到。
    local cmd
    while IFS= read -r cmd; do
        cmd=${cmd%%#*}
        cmd=${cmd//[[:space:]]/}
        if [[ -n $cmd && $cmd != docker && $cmd != just ]]; then
            ln -s "$(command -v "$cmd")" "$shim/$cmd"
        fi
    done <"$launcher_dir/lint/commands.txt"
}

# fake_cmd <name> <bash 本文>：在 shim 目錄放一個假命令。
fake_cmd() {
    printf '#!%s\n%s\n' "$BASH" "$2" >"$shim/$1"
    chmod +x "$shim/$1"
}

# fake_version <name> <--version 的輸出>
fake_version() {
    local quoted
    printf -v quoted '%q' "$2"
    fake_cmd "$1" "printf '%s\\n' $quoted"
}

# vk <bash 片段>：在乾淨的 bash 裡載入片段與 launcher/*.sh（main.sh、bootstrap_main.sh 被 source 時不執行入口），
# cwd 是 $work（有設 vk_cwd 時改用它），PATH 只有 shim 目錄，跑完以 vk_diag_exit 結束（片段自己 exit 的話照它的）。stdout、stderr 分開收。
# 陣列 vk_env 的 `名=值` 另外傳進環境（預設沒有）。
vk() {
    local script f
    script="source '$VK_MESSAGES';"
    for f in diag host log wire launch main bootstrap_main; do
        script+=" source '$launcher_dir/$f.sh';"
    done
    script+=" $1"$'\n''exit "$vk_diag_exit"'
    cd "${vk_cwd:-$work}" || return 1
    run --separate-stderr env -i PATH="$shim" HOME="$work" "${vk_env[@]}" "$BASH" -c "$script"
    cd - >/dev/null || return 1
}

# work 目錄裡什麼都沒有（沒建執行紀錄、沒寫檔）。
assert_work_empty() {
    local -a left=("$work"/* "$work"/.[!.]*)
    local f
    for f in "${left[@]}"; do
        if [[ -e $f ]]; then
            echo "unexpected file: $f" >&2
            return 1
        fi
    done
}

assert_git_not_called() {
    [[ ! -e $BATS_TEST_TMPDIR/git_called ]]
}

# rust_golden <函式名>：engine/runlog/src/tests.rs 裡該 golden 測試的期待行（r#"…"# 裡的字串）。
rust_golden() {
    local src rest
    src=$(<"$repo_root/engine/runlog/src/tests.rs")
    rest=${src#*"fn $1()"}
    if [[ $rest == "$src" ]]; then
        echo "golden $1 not found in engine/runlog/src/tests.rs" >&2
        return 1
    fi
    rest=${rest#*'r#"'}
    REPLY=${rest%%'"#'*}
}
