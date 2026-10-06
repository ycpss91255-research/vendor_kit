# 驗收案例共用的函式（test/acceptance/*.bats 以 load 載入）。
#
# 執行環境由 inside.sh 準備：DOCKER_HOST 指向 dind、TMPDIR 在跟 dind 共用的 /acc 底下（fixture repo 放 bats 的暫存
# 目錄，引擎與 test runner 的 bind mount 才找得到），以及
#   VK_ACC_REF：受測引擎的 pinned 引用（內嵌在 bootstrap.sh，也是首次導入後鎖定行該有的值）；
#   VK_ACC_TAR：引擎的 OCI tar，旁邊有同名 .digest；
#   VK_ACC_BOOTSTRAP：內嵌 VK_ACC_REF 的 bootstrap.sh。

bats_require_minimum_version 1.5.0

vk_acc_require_env() {
    local name
    for name in VK_ACC_REF VK_ACC_TAR VK_ACC_BOOTSTRAP DOCKER_HOST; do
        if [[ -z ${!name:-} ]]; then
            echo "$name is not set; run the acceptance tests with test/acceptance/run.sh" >&2
            return 1
        fi
    done
}

# vk_acc_git_repo <dir>：建一個空的 git repo（fixture repo 的起始狀態，ADR-0010：不帶前一次留下的東西）。
vk_acc_git_repo() {
    mkdir -p "$1"
    git -C "$1" init -q
}

# vk_acc_drop_engine：刪掉 dind 裡的受測引擎 image，讓接下來的首次導入只能從 tar 載入。
vk_acc_drop_engine() {
    docker image rm -f "${VK_ACC_REF%@*}" >/dev/null 2>&1 || true
    if docker image inspect "$VK_ACC_REF" >/dev/null 2>&1; then
        echo "the engine image is still present in dind: $VK_ACC_REF" >&2
        return 1
    fi
}

# vk_acc_bootstrap <args>...：在目前目錄以 bash 執行 bootstrap.sh，stdout、stderr 分開收（bats 的 run）。
# 結果也印出來：bats 只在案例失敗時顯示，方便看 CI 日誌。
vk_acc_bootstrap() {
    run --separate-stderr bash "$VK_ACC_BOOTSTRAP" "$@"
    vk_acc_show
}

# vk_acc_just <args>...：在目前目錄跑 just（經薄殼走一般路徑），結果同樣印出來。
vk_acc_just() {
    run --separate-stderr just "$@"
    vk_acc_show
}

# vk_acc_lock_line：目前目錄 .vendor_kit/version.toml 的引擎鎖定行的值。
vk_acc_lock_line() {
    sed -n 's/^vendor_kit = "\(.*\)"$/\1/p' .vendor_kit/version.toml
}

# vk_acc_snapshot <dir>：dir 底下（不含 .git）的路徑清單與每個檔的 sha256，用來驗「沒建紀錄、沒寫檔」。
vk_acc_snapshot() {
    (
        cd -- "$1" || exit 1
        find . -path ./.git -prune -o -print | LC_ALL=C sort
        find . -path ./.git -prune -o -type f -exec sha256sum {} + | LC_ALL=C sort
    )
}

# vk_acc_show：印出上一個 run 的結果（status、output、stderr 由 bats 的 run 設定）。
# shellcheck disable=SC2154
vk_acc_show() {
    printf 'status: %s\n--- stdout\n%s\n--- stderr\n%s\n' "$status" "$output" "$stderr"
}
