#!/usr/bin/env bats
# 薄殼模板的組裝（launcher/shell/assemble.sh）：輸出逐位元組決定、串接順序固定、組好的 log.sh 過 shellcheck
# 與命令白名單 lint、三份模板的內容，以及輸入不合時不寫檔。
# 用真 just 解析模板的測試不在這裡（test stage 還沒有 just）。

load helper

setup() {
    common_setup
    shell_dir=$launcher_dir/shell
    out=$BATS_TEST_TMPDIR/out
}

assemble() {
    run --separate-stderr "$BASH" "$shell_dir/assemble.sh" "$@"
}

@test "assemble writes the four shell files named as in engine/layout" {
    assemble "$VK_MESSAGES" "$out"
    [ "$status" -eq 0 ]
    [ "$stderr" = "" ]
    local -a names=("$out"/* "$out"/.[!.]*)
    [ "${names[*]##*/}" = "entry.just log.sh vendor.just .gitignore" ]
    local src
    src=$(<"$repo_root/engine/layout/src/lib.rs")
    [[ $src == *'pub const SHELL_FILES: [&str; 4] = ["entry.just", "vendor.just", "log.sh", ".gitignore"];'* ]]
}

@test "log.sh is the fragment then diag, host, log, wire, launch, main, byte for byte" {
    assemble "$VK_MESSAGES" "$out"
    [ "$status" -eq 0 ]
    local want=$BATS_TEST_TMPDIR/want
    cat "$VK_MESSAGES" "$launcher_dir"/{diag,host,log,wire,launch,main}.sh >"$want"
    cmp "$want" "$out/log.sh"
    cmp "$shell_dir/entry.just" "$out/entry.just"
    cmp "$shell_dir/vendor.just" "$out/vendor.just"
    cmp "$shell_dir/gitignore" "$out/.gitignore"
}

@test "assembling twice gives the same bytes and overwrites the old output" {
    assemble "$VK_MESSAGES" "$out"
    [ "$status" -eq 0 ]
    cp -R "$out" "$BATS_TEST_TMPDIR/first"
    printf 'stale\n' >"$out/log.sh"
    assemble "$VK_MESSAGES" "$out"
    [ "$status" -eq 0 ]
    diff -r "$BATS_TEST_TMPDIR/first" "$out"
    [ ! -e "$out/log.sh.tmp" ]
}

@test "the assembled log.sh passes shellcheck and the command whitelist lint" {
    assemble "$VK_MESSAGES" "$out"
    [ "$status" -eq 0 ]
    # 訊息片段的 vk_msg_* 由 diag.sh 以 ${!var} 間接讀取，shellcheck 看不出有用到（SC2034）。
    run shellcheck -s bash -e SC2034 "$out/log.sh"
    [ "$status" -eq 0 ]
    run "$BASH" "$launcher_dir/lint/check_commands.sh" "$out/log.sh"
    [ "$status" -eq 0 ]
    [ "$output" = "" ]
}

@test "assemble.sh itself passes shellcheck and the command whitelist lint" {
    run shellcheck "$shell_dir/assemble.sh"
    [ "$status" -eq 0 ]
    run "$BASH" "$launcher_dir/lint/check_commands.sh" "$shell_dir/assemble.sh"
    [ "$status" -eq 0 ]
    [ "$output" = "" ]
}

@test "an input that is missing, has a NUL or does not end with LF writes nothing" {
    local bad=$BATS_TEST_TMPDIR/bad
    assemble "$BATS_TEST_TMPDIR/none" "$out"
    [ "$status" -eq 1 ]
    [ "$stderr" = "assemble: cannot read $BATS_TEST_TMPDIR/none" ]
    [ ! -e "$out/log.sh" ]
    printf 'a\0b\n' >"$bad"
    assemble "$bad" "$out"
    [ "$status" -eq 1 ]
    [ "$stderr" = "assemble: $bad has a NUL byte" ]
    [ ! -e "$out/log.sh" ]
    printf 'x=1' >"$bad"
    assemble "$bad" "$out"
    [ "$status" -eq 1 ]
    [ "$stderr" = "assemble: $bad is empty or does not end with LF" ]
    : >"$bad"
    assemble "$bad" "$out"
    [ "$status" -eq 1 ]
    [ ! -e "$out/log.sh" ]
    assemble "$VK_MESSAGES"
    [ "$status" -eq 1 ]
    [ "$stderr" = "usage: assemble.sh <messages fragment> <outdir>" ]
}

@test "vk_assemble can be sourced and concatenates any parts in the given order" {
    printf 'b\n' >"$BATS_TEST_TMPDIR/b"
    printf 'a\n\n' >"$BATS_TEST_TMPDIR/a"
    run "$BASH" -c "source '$shell_dir/assemble.sh' && vk_assemble '$BATS_TEST_TMPDIR/ab' '$BATS_TEST_TMPDIR/b' '$BATS_TEST_TMPDIR/a'"
    [ "$status" -eq 0 ]
    [ "$output" = "" ]
    [ "$(cat "$BATS_TEST_TMPDIR/ab" && printf x)" = $'b\na\n\nx' ]
}

# ---- 模板內容 ----

@test "entry.just imports the VK module and the optional tool entry, relative to .vendor_kit/" {
    # 開頭的空行讓引擎加的標頭不會變成 mod 的說明（just --list 會印出來）。
    [ "$(cat "$shell_dir/entry.just" && printf x)" = $'\nmod vendor_kit \'vendor.just\'\nimport? \'gen/tools.just\'\nx' ]
}

@test "gitignore lists the paths of ADR-0002" {
    [ "$(cat "$shell_dir/gitignore" && printf x)" = $'cache/\ngen/\nlog/\nversion.local.toml\n.tmp.*\nx' ]
}

# vendor.just 的轉發行（不含 recipe 名與 "$@"）。
forward='    @exec bash {{quote(source_directory() / "log.sh")}} {{quote(parent_directory(source_directory()))}} {{quote(invocation_directory())}}'

@test "vendor.just has one forwarding recipe per VK recipe of engine/args, after the default" {
    local -a lines
    mapfile -t lines <"$shell_dir/vendor.just"
    # 第一個 recipe 是 `just vendor_kit` 的預設：不收參數、不帶 recipe 名。
    [ "${lines[0]}" = "" ]
    [ "${lines[1]}" = "[no-exit-message]" ]
    [ "${lines[2]}" = "[private]" ]
    [ "${lines[3]}" = "_usage:" ]
    [ "${lines[4]}" = "$forward" ]
    local -a names=()
    local i
    for ((i = 5; i < ${#lines[@]}; i += 6)); do
        [ "${lines[i]}" = "" ]
        [[ ${lines[i + 1]} =~ ^\[group\(\'(常用|進階)\'\)\]$ ]]
        [ "${lines[i + 2]}" = "[no-exit-message]" ]
        [ "${lines[i + 3]}" = "[positional-arguments]" ]
        [[ ${lines[i + 4]} =~ ^([a-z]+)\ \*args:$ ]]
        local name=${BASH_REMATCH[1]}
        [ "${lines[i + 5]}" = "$forward $name \"\$@\"" ]
        names+=("$name")
    done
    [ "$i" -eq "${#lines[@]}" ]
    # 跟引擎認得的指令名（engine/args 的 Name::from_command）是同一組。
    local src want=()
    src=$(<"$repo_root/engine/args/src/lib.rs")
    src=${src#*'fn from_command(s: &str) -> Option<Name> {'}
    src=${src%%'_ => return None'*}
    while [[ $src =~ \"([a-z]+)\"\ =\>\ Name:: ]]; do
        want+=("${BASH_REMATCH[1]}")
        src=${src#*"${BASH_REMATCH[0]}"}
    done
    [ "${#want[@]}" -eq 11 ]
    local -a sorted_names sorted_want
    mapfile -t sorted_names < <(printf '%s\n' "${names[@]}" | sort)
    mapfile -t sorted_want < <(printf '%s\n' "${want[@]}" | sort)
    [ "${sorted_names[*]}" = "${sorted_want[*]}" ]
}
