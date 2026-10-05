#!/usr/bin/env bats
# 主機前置檢查（ADR-0007:17–20、27、29；04 主機需求）。每條失敗都只印 stderr、回 2，
# 不建執行紀錄、不寫檔，也不呼叫 git。

load helper

setup() {
    common_setup
}

ok_docker() { fake_version docker 'Docker version 24.0.7, build afdd53b'; }
ok_just() { fake_version just 'just 1.33.0'; }

precheck() {
    vk "vk_host_precheck $1 https://example.invalid/just 'install-just --to ~/bin'"
}

assert_stopped() {
    [ "$status" -eq 2 ]
    [ "$output" = "" ]
    [ "$stderr" = "$1" ]
    assert_work_empty
    assert_git_not_called
}

no_docker='vendor_kit: error[VK0033]: Docker was not found on the host. Install Docker and retry.'
podman='vendor_kit: error[VK0011]: Detected Podman (docker --version). vendor_kit supports only Docker. Switch to Docker (rootful or rootless) and retry.'

low_docker() {
    REPLY="vendor_kit: error[VK0012]: Docker 19.03 or later is required; the current version is $1. Upgrade Docker and retry."
}

# ---- docker：首次導入、只檢查、修復（與 VK recipe）都檢查 ----

@test "docker missing stops every mode with VK0033" {
    ok_just
    for mode in initial_import check repair recipe; do
        precheck "$mode"
        assert_stopped "$no_docker"
    done
}

@test "docker --version containing podman stops every mode with VK0011" {
    ok_just
    fake_version docker 'podman version 4.9.3'
    for mode in initial_import check repair recipe; do
        precheck "$mode"
        assert_stopped "$podman"
    done
    fake_version docker 'Emulate Docker CLI using Podman. Create /etc/containers/nodocker to quiet msg.
Docker version 4.9.3'
    precheck check
    assert_stopped "$podman"
}

@test "docker older than 19.03 stops every mode with VK0012" {
    ok_just
    fake_version docker 'Docker version 18.09.7, build 2d0083d'
    low_docker 18.09.7
    for mode in initial_import check repair recipe; do
        precheck "$mode"
        assert_stopped "$REPLY"
    done
    fake_version docker 'Docker version 17.03.1-ce, build c6d412e'
    low_docker 17.03.1
    precheck repair
    assert_stopped "$REPLY"
}

@test "an unreadable docker version counts as too old" {
    fake_version docker 'something else'
    low_docker unknown
    precheck check
    assert_stopped "$REPLY"
}

@test "docker 19.03 and newer pass" {
    ok_just
    for v in 'Docker version 19.03.0, build aeac949' 'Docker version 20.10.24+dfsg1, build 297e128' \
        'Docker version 27.3.1, build ce12230'; do
        fake_version docker "$v"
        for mode in initial_import check repair recipe; do
            precheck "$mode"
            [ "$status" -eq 0 ]
            [ "$stderr" = "" ]
        done
    done
    assert_work_empty
    assert_git_not_called
}

# ---- just：只有首次導入檢查 ----

no_just='vendor_kit: error[VK0034]: just was not found on the host. Use the GitHub release.
Download: https://example.invalid/just
Install: install-just --to ~/bin'

low_just() {
    REPLY="vendor_kit: error[VK0005]: just 1.33.0 or later is required; the current version is $1. Use the GitHub release.
Download: https://example.invalid/just
Install: install-just --to ~/bin"
}

@test "initial import without just stops with VK0034" {
    ok_docker
    precheck initial_import
    assert_stopped "$no_just"
}

@test "initial import with just older than 1.33.0 stops with VK0005" {
    ok_docker
    for v in 1.32.9 1.9.0 0.99.99; do
        fake_version just "just $v"
        low_just "$v"
        precheck initial_import
        assert_stopped "$REPLY"
    done
}

@test "just 1.33.0 and newer pass initial import" {
    ok_docker
    for v in 1.33.0 1.33.1 1.40.0 2.0.0; do
        fake_version just "just $v"
        precheck initial_import
        [ "$status" -eq 0 ]
        [ "$stderr" = "" ]
    done
}

@test "check, repair and recipes do not look at just" {
    ok_docker
    for mode in check repair recipe; do
        precheck "$mode"
        [ "$status" -eq 0 ]
        [ "$stderr" = "" ]
    done
    fake_version just 'just 1.0.0'
    precheck check
    [ "$status" -eq 0 ]
}

@test "docker is checked before just" {
    precheck initial_import
    assert_stopped "$no_docker"
}

@test "an unknown mode is a VK bug" {
    ok_docker
    precheck bogus
    [ "$status" -eq 2 ]
    [[ $stderr == 'vendor_kit: error[VK0056]: Internal vendor_kit error: unknown launcher mode bogus.'* ]]
}

# ---- 往上找 .git ----

@test "a .git directory in a parent is found without calling git" {
    mkdir -p "$work/repo/.git" "$work/repo/a/b"
    vk "vk_find_git '$work/repo/a/b' && printf '%s\n' \"\$REPLY\""
    [ "$status" -eq 0 ]
    [ "$output" = "$work/repo" ]
    assert_git_not_called
}

@test "a .git file (worktree or submodule) counts" {
    mkdir -p "$work/wt/sub"
    printf 'gitdir: /elsewhere\n' >"$work/wt/.git"
    vk "vk_find_git '$work/wt/sub' && printf '%s\n' \"\$REPLY\""
    [ "$status" -eq 0 ]
    [ "$output" = "$work/wt" ]
}

@test "the current directory is the default start" {
    mkdir -p "$work/.git"
    vk 'vk_find_git && printf "%s\n" "$REPLY"'
    [ "$status" -eq 0 ]
    [ "$output" = "$work" ]
}

@test "no .git up to / stops with VK0035 and writes nothing" {
    if [[ -e /.git ]]; then
        skip "/.git exists on this machine"
    fi
    local outside
    outside=$(mktemp -d /tmp/vk-nogit.XXXXXX)
    local p=$outside
    while [[ -n $p ]]; do
        if [[ -e $p/.git ]]; then
            rm -rf "$outside"
            skip "a parent of $outside has .git"
        fi
        p=${p%/*}
    done
    vk "vk_find_git '$outside'"
    rm -rf "$outside"
    assert_stopped 'vendor_kit: error[VK0035]: Cannot find .git in the current directory or any parent directory. Run bootstrap.sh from within a Git repository.'
}

# ---- 版本比較 ----

@test "versions compare numerically, segment by segment" {
    vk 'for p in "19.03 19.03" "19.03.0 19.03" "20.10 19.03" "1.33.0 1.33.0" "1.100.0 1.33.0" "2 1.33.0"; do
            set -- $p; vk_version_ge "$1" "$2" || { echo "not ge: $p"; exit 1; }
        done
        for p in "18.09 19.03" "1.9.0 1.33.0" "1.32.99 1.33.0" "0.200 1.33.0"; do
            set -- $p; vk_version_ge "$1" "$2" && { echo "ge: $p"; exit 1; }
        done
        exit 0'
    [ "$status" -eq 0 ]
}
