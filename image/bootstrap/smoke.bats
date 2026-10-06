#!/usr/bin/env bats
# 組好的 bootstrap.sh 的 smoke 測試（#372 的 N1）：組裝結果的開頭與決定性、以 bash 直接執行時入口照常、
# 內嵌引用真的被讀到，以及 image/bootstrap/assemble.sh 接受帶 port 的 registry、擋下不合格式的引用與介面版。
# 各判定的完整測試在 launcher/test/bootstrap*.bats（那裡 source 各檔，這裡跑組好的單一檔）。
#
# 執行前設：
#   VK_BOOTSTRAP：用固定的假引用組好的 bootstrap.sh（image/Dockerfile 的 test stage 產出）；
#   VK_MESSAGES：同一次組裝用的 msggen 訊息片段。

bats_require_minimum_version 1.5.0

image_dir=$(cd -- "$BATS_TEST_DIRNAME/.." && pwd)
repo_root=$(cd -- "$image_dir/.." && pwd)
assemble=$image_dir/bootstrap/assemble.sh

setup() {
    if [[ -z ${VK_BOOTSTRAP:-} || ! -r $VK_BOOTSTRAP || -z ${VK_MESSAGES:-} || ! -r $VK_MESSAGES ]]; then
        echo "VK_BOOTSTRAP and VK_MESSAGES must point to the assembled bootstrap.sh and its message fragment" >&2
        return 1
    fi
    # 組裝時的引用與介面版：從組好的檔的開頭讀回來（第 2、3 行）。
    local line
    line=$(sed -n 2p "$VK_BOOTSTRAP")
    ref=${line#vk_bootstrap_engine=\'}
    ref=${ref%\'}
    line=$(sed -n 3p "$VK_BOOTSTRAP")
    proto=${line#vk_bootstrap_proto=\'}
    proto=${proto%\'}
    usage_line='Usage: bootstrap.sh [-i <image>] [-y] | --repair [-i <image>] | -h'
    shim="$BATS_TEST_TMPDIR/bin"
    work="$BATS_TEST_TMPDIR/work"
    mkdir -p "$shim" "$work"
    # PATH 只有 shim 目錄：啟動器命令白名單上的基礎命令接真的，docker、just 換成假的，git 留下記號。
    local cmd
    while IFS= read -r cmd; do
        cmd=${cmd%%#*}
        cmd=${cmd//[[:space:]]/}
        if [[ -n $cmd && $cmd != docker && $cmd != just ]]; then
            ln -s "$(command -v "$cmd")" "$shim/$cmd"
        fi
    done <"$repo_root/launcher/lint/commands.txt"
    fake_cmd git 'printf called >"'"$BATS_TEST_TMPDIR"'/git_called"'
    fake_cmd docker "printf '%s\\n' 'Docker version 24.0.7, build afdd53b'"
    fake_cmd just "printf '%s\\n' 'just 1.33.0'"
}

fake_cmd() {
    printf '#!%s\n%s\n' "$BASH" "$2" >"$shim/$1"
    chmod +x "$shim/$1"
}

# bs <args>...：在 $work 以 bash 直接執行組好的 bootstrap.sh，PATH 只有 shim 目錄。
bs() {
    cd "$work" || return 1
    run --separate-stderr env -i PATH="$shim" HOME="$work" "$BASH" "$VK_BOOTSTRAP" "$@"
    cd - >/dev/null || return 1
}

@test "the assembled file starts with the shebang and the embedded reference" {
    [ "$(sed -n 1p "$VK_BOOTSTRAP")" = '#!/usr/bin/env bash' ]
    [[ $ref =~ ^[a-z0-9][a-z0-9._/-]*:v[0-9]+\.[0-9]+\.[0-9]+@sha256:[0-9a-f]{64}$ ]]
    [[ $proto =~ ^[1-9][0-9]*$ ]]
}

@test "assembling again with the same inputs gives the same bytes" {
    run bash "$assemble" "$ref" "$proto" "$VK_MESSAGES" "$BATS_TEST_TMPDIR/again.sh"
    [ "$status" -eq 0 ]
    cmp "$VK_BOOTSTRAP" "$BATS_TEST_TMPDIR/again.sh"
    [ ! -e "$BATS_TEST_TMPDIR/again.sh.head" ]
}

@test "-h prints the usage on stdout" {
    bs -h
    [ "$status" -eq 0 ]
    [ "${lines[0]}" = "$usage_line" ]
    [ "$stderr" = "" ]
}

@test "an unknown option is a usage error (VK0026) before the host check" {
    rm "$shim/docker"
    bs --bogus
    [ "$status" -eq 2 ]
    [ "$output" = "" ]
    [ "$stderr" = "vendor_kit: error[VK0026]: Unknown, extra, or disallowed argument: --bogus."$'\n'"$usage_line" ]
}

@test "outside a Git repository the initial import stops with VK0035" {
    bs -y
    [ "$status" -eq 2 ]
    [ "$output" = "" ]
    [ "$stderr" = 'vendor_kit: error[VK0035]: Cannot find .git in the current directory or any parent directory. Run bootstrap.sh from within a Git repository.' ]
    [ ! -e "$BATS_TEST_TMPDIR/git_called" ]
    [ -z "$(ls -A "$work")" ]
}

@test "the embedded reference decides the major version (VK0040)" {
    local x=${ref#*:v}
    x=${x%%.*}
    local other=$((x + 1))
    mkdir -p "$work/.vendor_kit"
    printf 'vendor_kit = "%s"\nschema = 1\n' "${ref%%:*}:v$other.0.0@${ref#*@}" >"$work/.vendor_kit/version.toml"
    bs
    [ "$status" -eq 3 ]
    [ "$stderr" = "vendor_kit: fatal[VK0040]: This bootstrap.sh is for major version $x, but the locked engine requires major version $other. No files were modified. Download bootstrap.sh for major version $other from the Release and retry." ]
}

@test "assemble.sh rejects a reference that is not pinned vX.Y.Z and an invalid interface version" {
    local d=sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa out=$BATS_TEST_TMPDIR/bad.sh bad
    for bad in "ghcr.io/acme/vendor_kit:v1.0.0" "ghcr.io/acme/vendor_kit@$d" "ghcr.io/acme/vendor_kit:latest@$d" \
        "ghcr.io/acme/vendor_kit:v1.0@$d" "ghcr.io/acme/vendor_kit:v01.0.0@$d" "ghcr.io/acme/vendor_kit:v1.0.0@$d'" \
        "localhost:5000:v1.0.0@$d" "localhost:/acme/vendor_kit:v1.0.0@$d" "localhost:50x0/acme/vendor_kit:v1.0.0@$d" \
        "localhost:5000/acme/vendor_kit@$d" "localhost:5000/acme/vendor_kit:v1.0.0"; do
        run bash "$assemble" "$bad" 1 "$VK_MESSAGES" "$out"
        [ "$status" -eq 1 ]
        [[ $output == *"is not a pinned"* ]]
        [ ! -e "$out" ]
    done
    for bad in 0 01 x ''; do
        run bash "$assemble" "$ref" "$bad" "$VK_MESSAGES" "$out"
        [ "$status" -eq 1 ]
        [[ $output == *"interface version"* ]]
        [ ! -e "$out" ]
    done
    run bash "$assemble" "$ref" 1 "$BATS_TEST_TMPDIR/missing" "$out"
    [ "$status" -eq 1 ]
    [ ! -e "$out" ]
    [ ! -e "$out.head" ]
}

@test "assemble.sh accepts a registry with a port and embeds the reference as given" {
    local d=sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb out=$BATS_TEST_TMPDIR/port.sh good
    for good in "localhost:5000/acme/vendor_kit:v1.2.3@$d" "registry.example.com:443/vendor_kit:v0.0.1@$d"; do
        run bash "$assemble" "$good" "$proto" "$VK_MESSAGES" "$out"
        [ "$status" -eq 0 ]
        [ "$(sed -n 2p "$out")" = "vk_bootstrap_engine='$good'" ]
        # 除了內嵌引用那一行，其餘逐位元組跟用假引用組的那份相同。
        cmp <(sed 2d "$VK_BOOTSTRAP") <(sed 2d "$out")
        [ ! -e "$out.head" ]
        rm -f -- "$out"
    done
}
