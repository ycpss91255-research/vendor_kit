#!/usr/bin/env bats
# 主機檢查清單（ADR-0007 的驗收案例）：找不到 docker、低版本 docker、`docker --version` 含 podman 在首次導入、
# 只檢查與 --repair 三種模式各一條；首次導入找不到 just、低版本 just 各一條；往上找不到 .git 一條。
# 被拒絕時都不建執行紀錄、不寫檔（比對執行前後的檔案清單與內容）。
#
# 跑的是組好的 bootstrap.sh；PATH 只放啟動器命令白名單（launcher/lint/commands.txt）上的命令，docker 與 just
# 依案例接 dind 的真 docker、真 just、換成假的或拿掉。舊薄殼跑新 major 的一般 recipe、同一個不合組合下救援路徑
# 仍可用，要兩個不同 major 的引擎，這裡還沒有。

# status、output、stderr 由 bats 的 run 設定。
# shellcheck disable=SC2154
load helper

setup_file() {
    vk_acc_require_env
    # 只檢查與 --repair 用的安裝目錄：用真 docker 走一次首次導入。
    export VK_ACC_INSTALLED="$BATS_FILE_TMPDIR/installed"
    vk_acc_git_repo "$VK_ACC_INSTALLED"
    (cd "$VK_ACC_INSTALLED" && bash "$VK_ACC_BOOTSTRAP" -i "$VK_ACC_TAR" -y >/dev/null)
}

setup() {
    vk_acc_require_env
    shim="$BATS_TEST_TMPDIR/bin"
    mkdir -p "$shim"
    local cmd
    while IFS= read -r cmd; do
        cmd=${cmd%%#*}
        cmd=${cmd//[[:space:]]/}
        if [[ -n $cmd && $cmd != docker && $cmd != just ]]; then
            ln -s "$(command -v "$cmd")" "$shim/$cmd"
        fi
    done </src/launcher/lint/commands.txt
}

# real <cmd>：shim 目錄的 cmd 接真的命令。
real() {
    ln -s "$(command -v "$1")" "$shim/$1"
}

# fake <cmd> <version output>：shim 目錄的 cmd 換成只印一行版本的假命令。
fake() {
    printf '#!%s\nprintf "%%s\\n" %q\n' "$BASH" "$2" >"$shim/$1"
    chmod +x "$shim/$1"
}

# rejected <dir> <code> <args>...：在 dir 以只有 shim 的 PATH 跑 bootstrap.sh，要以結束碼 2 與 code 的診斷拒絕，
# 而且 dir 底下沒有任何改動（沒建執行紀錄、沒寫檔）。
rejected() {
    local dir=$1 code=$2 before
    shift 2
    before=$(vk_acc_snapshot "$dir")
    cd "$dir" || return 1
    run --separate-stderr env PATH="$shim" "$BASH" "$VK_ACC_BOOTSTRAP" "$@"
    vk_acc_show
    [ "$status" -eq 2 ]
    [[ $stderr == *"error[$code]"* ]]
    [ "$(vk_acc_snapshot "$dir")" = "$before" ]
}

fresh() {
    vk_acc_git_repo "$BATS_TEST_TMPDIR/repo"
    echo "$BATS_TEST_TMPDIR/repo"
}

@test "initial import: no docker is VK0033" {
    real just
    rejected "$(fresh)" VK0033 -i "$VK_ACC_TAR" -y
}

@test "initial import: podman is VK0011" {
    fake docker 'podman version 5.0.0'
    real just
    rejected "$(fresh)" VK0011 -i "$VK_ACC_TAR" -y
}

@test "initial import: docker older than 19.03 is VK0012" {
    fake docker 'Docker version 18.09.9, build 039a7df'
    real just
    rejected "$(fresh)" VK0012 -i "$VK_ACC_TAR" -y
}

@test "initial import: no just is VK0034" {
    real docker
    rejected "$(fresh)" VK0034 -i "$VK_ACC_TAR" -y
}

@test "initial import: just older than 1.33.0 is VK0005" {
    real docker
    fake just 'just 1.32.0'
    rejected "$(fresh)" VK0005 -i "$VK_ACC_TAR" -y
}

@test "initial import: no .git above the current directory is VK0035" {
    real docker
    real just
    mkdir -p "$BATS_TEST_TMPDIR/plain"
    rejected "$BATS_TEST_TMPDIR/plain" VK0035 -i "$VK_ACC_TAR" -y
}

@test "check: no docker is VK0033" {
    real just
    rejected "$VK_ACC_INSTALLED" VK0033
}

@test "check: podman is VK0011" {
    fake docker 'podman version 5.0.0'
    rejected "$VK_ACC_INSTALLED" VK0011
}

@test "check: docker older than 19.03 is VK0012" {
    fake docker 'Docker version 18.09.9, build 039a7df'
    rejected "$VK_ACC_INSTALLED" VK0012
}

@test "repair: no docker is VK0033" {
    real just
    rejected "$VK_ACC_INSTALLED" VK0033 --repair
}

@test "repair: podman is VK0011" {
    fake docker 'podman version 5.0.0'
    rejected "$VK_ACC_INSTALLED" VK0011 --repair
}

@test "repair: docker older than 19.03 is VK0012" {
    fake docker 'Docker version 18.09.9, build 039a7df'
    rejected "$VK_ACC_INSTALLED" VK0012 --repair
}

@test "check does not look for just" {
    real docker
    cd "$VK_ACC_INSTALLED"
    run --separate-stderr env PATH="$shim" "$BASH" "$VK_ACC_BOOTSTRAP"
    vk_acc_show
    [ "$status" -eq 0 ]
}
