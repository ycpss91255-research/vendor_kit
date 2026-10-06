#!/usr/bin/env bats
# 薄殼 log.sh 的入口（main.sh）：版本鎖定行的引擎行（命中數、引號、縮排、CRLF）、自描述標頭的介面版與引擎版，
# 以及組好的 log.sh 加上標頭後，用假 docker 從 vendor.just 的呼叫形狀跑完整一趟。

load helper

setup() {
    common_setup
    A=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    E=eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
    engine="ghcr.io/acme/vendor_kit:v1.0.0@sha256:$A"
    pending='reason code pending (draft VK0070, N76)'
}

# internal <reason>：沒有執行紀錄時的 VK0056 整行。
internal() {
    REPLY="vendor_kit: error[VK0056]: Internal vendor_kit error: $1. This is a VK bug. Report it at https://github.com/ycpss91255-research/vendor_kit/issues and attach run log none."
}

# lock <內容（printf %b）>：寫 $work/v.toml，再跑 vk_main_recipe，成功時印出引用。
lock() {
    printf '%b' "$1" >"$work/v.toml"
    vk 'vk_main_recipe "$PWD/v.toml" || exit "$vk_diag_exit"; printf "%s\n" "$REPLY"'
}

# header <內容（printf %b）>：寫 $work/h，再跑 vk_main_header，成功時印出介面版與引擎版。
header() {
    printf '%b' "$1" >"$work/h"
    vk 'vk_main_header "$PWD/h" || exit "$vk_diag_exit"; printf "%s %s\n" "$vk_main_proto" "$vk_main_version"'
}

# ---- 版本鎖定行的引擎行 ----

@test "the single engine line gives the pinned reference" {
    lock "vendor_kit = \"$engine\"\nschema = 1\nwritten_by = \"v1.0.0\"\n\n[tools]\ntool = \"x\"\n"
    [ "$status" -eq 0 ]
    [ "$output" = "$engine" ]
    [ "$stderr" = "" ]
}

@test "the engine line is found anywhere, with any spacing, a comment, CRLF or no final LF" {
    local text
    for text in \
        "# lock\nschema = 1\nvendor_kit\t=   \"$engine\" # pinned\n" \
        "vendor_kit=\"$engine\"\n" \
        "vendor_kit = \"$engine\"\r\nschema = 1\r\n" \
        "schema = 1\nvendor_kit = \"$engine\""; do
        lock "$text"
        [ "$status" -eq 0 ]
        [ "$output" = "$engine" ]
    done
}

@test "zero engine lines (no file, indented or quoted key) is VK0056" {
    vk 'vk_main_recipe "$PWD/v.toml"'
    [ "$status" -eq 2 ]
    internal "$work/v.toml has 0 engine lock lines, exactly 1 is required; $pending"
    [ "$stderr" = "$REPLY" ]
    [ "$output" = "" ]
    local text
    for text in \
        "schema = 1\n" \
        "  vendor_kit = \"$engine\"\n" \
        "\"vendor_kit\" = \"$engine\"\n" \
        "vendor_kit_engine = \"$engine\"\n"; do
        lock "$text"
        [ "$status" -eq 2 ]
        [ "$stderr" = "$REPLY" ]
    done
}

@test "two engine lines (one under [tools]) is VK0056" {
    lock "vendor_kit = \"$engine\"\n[tools]\nvendor_kit = \"$engine\"\n"
    [ "$status" -eq 2 ]
    internal "$work/v.toml has 2 engine lock lines, exactly 1 is required; $pending"
    [ "$stderr" = "$REPLY" ]
    [ "$output" = "" ]
}

@test "an engine line that is not a double-quoted pinned reference is VK0056" {
    local text
    for text in "vendor_kit = '$engine'\n" "vendor_kit = $engine\n" "vendor_kit = \"$engine\n"; do
        lock "$text"
        [ "$status" -eq 2 ]
        internal "the engine lock line in $work/v.toml is not a double-quoted string; $pending"
        [ "$stderr" = "$REPLY" ]
    done
    for text in "vendor_kit = \"ghcr.io/acme/vendor_kit:v1.0.0\"\n" "vendor_kit = \"\"\n"; do
        lock "$text"
        [ "$status" -eq 2 ]
        internal "the engine lock line in $work/v.toml is not a pinned image reference; $pending"
        [ "$stderr" = "$REPLY" ]
    done
}

@test "an unreadable version.toml is VK0056" {
    mkdir "$work/v.toml"
    vk 'vk_main_recipe "$PWD/v.toml"'
    [ "$status" -eq 2 ]
    internal "cannot read $work/v.toml; $pending"
    [ "$stderr" = "$REPLY" ]
}

# ---- 自描述標頭 ----

@test "the header gives the interface version and the engine version" {
    header "# vendor_kit-shell interface 1\n# vendor_kit-shell engine v1.2.3\n# vendor_kit-shell sha256 x\nbody\n"
    [ "$status" -eq 0 ]
    [ "$output" = "1 v1.2.3" ]
    header "# vendor_kit-shell interface 12\r\n# vendor_kit-shell engine v1.2.3\r\n"
    [ "$status" -eq 0 ]
    [ "$output" = "12 v1.2.3" ]
}

@test "a missing or malformed interface version is VK0056" {
    local text
    for text in \
        "" \
        "# shellcheck shell=bash\n" \
        "# vendor_kit-shell interface 01\n# vendor_kit-shell engine v1\n" \
        "# vendor_kit-shell interface x\n# vendor_kit-shell engine v1\n" \
        "# vendor_kit-shell interface  1\n# vendor_kit-shell engine v1\n" \
        "# vendor_kit-shell engine v1\n# vendor_kit-shell interface 1\n"; do
        header "$text"
        [ "$status" -eq 2 ]
        internal "cannot read the interface version from the self-describing header of $work/h"
        [ "$stderr" = "$REPLY" ]
    done
    vk 'vk_main_header "$PWD/none"'
    [ "$status" -eq 2 ]
    internal "cannot read the interface version from the self-describing header of $work/none"
    [ "$stderr" = "$REPLY" ]
}

@test "a missing or malformed engine version is VK0056" {
    local text
    for text in \
        "# vendor_kit-shell interface 1\n" \
        "# vendor_kit-shell interface 1\n# vendor_kit-shell engine \n" \
        "# vendor_kit-shell interface 1\n# vendor_kit-shell engine v1 x\n" \
        "# vendor_kit-shell interface 1\n# vendor_kit-shell sha256 x\n"; do
        header "$text"
        [ "$status" -eq 2 ]
        internal "cannot read the engine version from the self-describing header of $work/h"
        [ "$stderr" = "$REPLY" ]
    done
}

# ---- 組好的 log.sh 跑完整一趟（假 docker） ----

# install_shell：組好的 log.sh 加上標頭放進 $work/.vendor_kit/，假 docker 與版本鎖定行就位。
install_shell() {
    fake="$BATS_TEST_TMPDIR/fake"
    tmpd="$BATS_TEST_TMPDIR/tmp"
    mkdir -p "$fake" "$tmpd" "$work/.git" "$work/sub" "$work/.vendor_kit"
    fake_cmd docker "source '$BATS_TEST_DIRNAME/fixture/fake_docker.bash'"
    printf '1 1 v1.0.0' >"$fake/labels"
    printf 'finish 0\n' >"$fake/engine"
    "$BASH" "$launcher_dir/shell/assemble.sh" "$VK_MESSAGES" "$BATS_TEST_TMPDIR/shell"
    {
        printf '# vendor_kit-shell interface 1\n# vendor_kit-shell engine v9.9.9\n# vendor_kit-shell sha256 %s\n' "$A"
        cat "$BATS_TEST_TMPDIR/shell/log.sh"
    } >"$work/.vendor_kit/log.sh"
    printf 'vendor_kit = "%s"\nvendor_kit_protocols = "1"\nschema = 1\n' "$engine" >"$work/.vendor_kit/version.toml"
    vk_env=(VK_FAKE="$fake" TMPDIR="$tmpd" vk_log_invocation_id=r1)
}

# shell_run [<recipe> <args>...]：照 vendor.just 的形狀在 $work/sub 下呼叫 log.sh。
shell_run() {
    cd "$work/sub" || return 1
    run --separate-stderr env -i PATH="$shim" HOME="$work" "${vk_env[@]}" \
        "$BASH" "$work/.vendor_kit/log.sh" "$work" "$work/sub" "$@"
    cd - >/dev/null || return 1
}

# engine_tail：引擎 argv 的 --protocol 值與 `--` 之後的部分，以空白接起放進 REPLY。
engine_tail() {
    local -a got
    mapfile -t got <"$fake/engine.argv"
    local i proto=
    for ((i = 0; i < ${#got[@]}; i++)); do
        if [[ ${got[i]} == --protocol ]]; then
            proto=${got[i + 1]}
        fi
        if [[ ${got[i]} == -- ]]; then
            break
        fi
    done
    REPLY="$proto ${got[*]:i}"
}

@test "the assembled log.sh with a header runs a recipe end to end" {
    install_shell
    shell_run add foo -- '-x y'
    [ "$status" -eq 0 ]
    [ "$stderr" = "" ]
    local -a want=(--mount "type=bind,\"source=$work\",target=/vk/root")
    mapfile -t got <"$fake/engine.argv"
    [[ " ${got[*]} " == *" ${want[*]} "* ]]
    [[ " ${got[*]} " == *" $engine "* ]]
    [[ " ${got[*]} " == *" --host-cwd $work/sub "* ]]
    engine_tail
    [ "$REPLY" = "1 -- add foo -- -x y" ]
    [ "${got[${#got[@]} - 1]}" = '-x y' ]
    local -a logs=("$work/.vendor_kit/log"/*-add-r1.jsonl)
    [ -f "${logs[0]}" ]
    grep -qF '"service.version":"v9.9.9"' "${logs[0]}"
    assert_git_not_called
}

@test "the assembled log.sh without a recipe is the usage call" {
    install_shell
    shell_run
    [ "$status" -eq 0 ]
    engine_tail
    [ "$REPLY" = "1 --" ]
    local -a logs=("$work/.vendor_kit/log"/*-vendor_kit-r1.jsonl)
    [ -f "${logs[0]}" ]
}

@test "the engine exit code is the exit code of log.sh" {
    install_shell
    printf 'finish 1\n' >"$fake/engine"
    shell_run sync
    [ "$status" -eq 1 ]
}

@test "a bad lock line stops log.sh before the run log and docker" {
    install_shell
    printf 'schema = 1\n' >"$work/.vendor_kit/version.toml"
    shell_run sync
    [ "$status" -eq 2 ]
    internal "$work/.vendor_kit/version.toml has 0 engine lock lines, exactly 1 is required; $pending"
    [ "$stderr" = "$REPLY" ]
    [ ! -e "$work/.vendor_kit/log" ]
    [ ! -e "$fake/calls" ]
}

@test "log.sh without the self-describing header stops before docker" {
    install_shell
    cp "$BATS_TEST_TMPDIR/shell/log.sh" "$work/.vendor_kit/log.sh"
    shell_run sync
    [ "$status" -eq 2 ]
    internal "cannot read the interface version from the self-describing header of $work/.vendor_kit/log.sh"
    [ "$stderr" = "$REPLY" ]
    [ ! -e "$fake/calls" ]
}

@test "log.sh called without the two directories is VK0056" {
    install_shell
    cd "$work" || return 1
    run --separate-stderr env -i PATH="$shim" HOME="$work" "$BASH" "$work/.vendor_kit/log.sh" "$work"
    cd - >/dev/null || return 1
    [ "$status" -eq 2 ]
    internal "log.sh needs the install directory and the working directory"
    [ "$stderr" = "$REPLY" ]
}

@test "sourcing log.sh defines the functions without running vk_main" {
    install_shell
    vk "source '$work/.vendor_kit/log.sh'; declare -F vk_main >/dev/null || exit 9"
    [ "$status" -eq 0 ]
    [ "$stderr" = "" ]
    [ ! -e "$fake/calls" ]
}
