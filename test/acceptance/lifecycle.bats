#!/usr/bin/env bats
# 引擎生命週期（#372 的 N22；ADR-0010 的流程順序裡不連外網的部分）：首次導入、sync、test、改一個位元組的薄殼、
# uninstall、重新導入，全部走公開入口（bootstrap.sh 與 `just vendor_kit …`），引擎是剛建好的 image。
# 案例依檔內順序在同一個 fixture repo 上接著跑：每一步的前置狀態由前一步產生。
# 需要 registry 的 add、update、upgrade、remove、dev／undev、prune 等 GHCR 上有驗收 fixture 後另做。

# status、output、stderr 由 bats 的 run 設定。
# shellcheck disable=SC2154
load helper

setup_file() {
    vk_acc_require_env
    export VK_ACC_LIFE="$BATS_FILE_TMPDIR/repo"
    vk_acc_git_repo "$VK_ACC_LIFE"
}

setup() {
    vk_acc_require_env
    cd "$VK_ACC_LIFE" || return 1
}

@test "initial import with -i loads the image tar and locks the engine to the tar's digest" {
    vk_acc_drop_engine
    vk_acc_bootstrap -i "$VK_ACC_TAR" -y
    [ "$status" -eq 0 ]
    [ "$(vk_acc_lock_line)" = "$VK_ACC_REF" ]
    [ "$(cat "${VK_ACC_TAR%.tar}.digest")" = "${VK_ACC_REF#*@}" ]
    # 之後的 recipe 以鎖定行的 pinned 引用找 image：載入後要找得到（不連外網，找不到就只能 pull 而失敗）。
    docker image inspect "$VK_ACC_REF" >/dev/null
    grep -qx "import '.vendor_kit/entry.just'" justfile
    for f in entry.just vendor.just log.sh .gitignore config.toml version.toml; do
        [ -f ".vendor_kit/$f" ]
    done
    compgen -G '.vendor_kit/log/*-bootstrap-*.jsonl' >/dev/null
}

@test "sync regenerates gen/ through the shell entry" {
    vk_acc_just vendor_kit sync
    [ "$status" -eq 0 ]
    [ -f .vendor_kit/gen/tools.just ]
    compgen -G '.vendor_kit/log/*-sync-*.jsonl' >/dev/null
}

@test "test without a path checks the install" {
    vk_acc_just vendor_kit test
    [ "$status" -eq 0 ]
    compgen -G '.vendor_kit/log/*-test-*.jsonl' >/dev/null
}

@test "bootstrap.sh check reports a shell file changed by one byte and --repair restores it" {
    local f=.vendor_kit/vendor.just at=200 byte new
    cp "$f" "$BATS_TEST_TMPDIR/original"
    byte=$(dd if="$f" bs=1 skip="$at" count=1 2>/dev/null)
    new=Z
    if [[ $byte == Z ]]; then
        new=Y
    fi
    printf '%s' "$new" | dd of="$f" bs=1 seek="$at" conv=notrunc 2>/dev/null
    cp "$f" "$BATS_TEST_TMPDIR/changed"
    [ "$(cmp "$BATS_TEST_TMPDIR/original" "$BATS_TEST_TMPDIR/changed" | wc -l)" -eq 1 ]
    [ "$(wc -c <"$f")" -eq "$(wc -c <"$BATS_TEST_TMPDIR/original")" ]

    vk_acc_bootstrap
    [ "$status" -eq 2 ]
    [[ $stderr == *'error[VK0006]'* ]]
    [[ $stderr == *"$f (modified)"* ]]
    # 只檢查不重產。
    cmp -s "$f" "$BATS_TEST_TMPDIR/changed"

    vk_acc_bootstrap --repair
    [ "$status" -eq 0 ]
    cmp -s "$f" "$BATS_TEST_TMPDIR/original"

    vk_acc_bootstrap
    [ "$status" -eq 0 ]
}

@test "uninstall removes the install and keeps config.toml and the run logs" {
    # uninstall 不收 -y，要詢問（收回根 justfile 與 .dockerignore 插入的行）：用 script 給它一個終端並答 y。
    run --separate-stderr script -qec 'just vendor_kit uninstall' /dev/null < <(printf 'y\ny\n')
    vk_acc_show
    [ "$status" -eq 0 ]
    [ ! -e .vendor_kit/version.toml ]
    for f in entry.just vendor.just log.sh; do
        [ ! -e ".vendor_kit/$f" ]
    done
    [ -f .vendor_kit/config.toml ]
    compgen -G '.vendor_kit/log/*-uninstall-*.jsonl' >/dev/null
    run ! grep -q "import '.vendor_kit/entry.just'" justfile
    run ! grep -q '^\.vendor_kit/' .dockerignore
}

@test "re-import after moving .vendor_kit away installs again from the image tar" {
    mv .vendor_kit "$BATS_TEST_TMPDIR/old_vendor_kit"
    vk_acc_drop_engine
    vk_acc_bootstrap -i "$VK_ACC_TAR" -y
    [ "$status" -eq 0 ]
    [ "$(vk_acc_lock_line)" = "$VK_ACC_REF" ]
    grep -qx "import '.vendor_kit/entry.just'" justfile

    vk_acc_just vendor_kit sync
    [ "$status" -eq 0 ]
    vk_acc_bootstrap
    [ "$status" -eq 0 ]
}
