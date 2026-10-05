#!/usr/bin/env bats
# 命令白名單 lint（ADR-0007:26、30）：launcher/*.sh 要過，違規樣本要被擋。

load helper

lint() {
    run --separate-stderr "$BASH" "$launcher_dir/lint/check_commands.sh" "$@"
}

@test "launcher sources only call allowed commands" {
    lint
    [ "$status" -eq 0 ]
    [ "$output" = "" ]
}

@test "the whitelist does not contain git" {
    local line
    while IFS= read -r line; do
        line=${line%%#*}
        line=${line//[[:space:]]/}
        [ "$line" != git ]
    done <"$launcher_dir/lint/commands.txt"
}

@test "a sample using only builtins, own functions and allowed commands passes" {
    lint "$BATS_TEST_DIRNAME/fixture/lint_good.sh"
    [ "$status" -eq 0 ]
    [ "$output" = "" ]
}

@test "every command outside the whitelist is reported" {
    local f=$BATS_TEST_DIRNAME/fixture/lint_bad.sh
    lint "$f"
    [ "$status" -eq 1 ]
    local want=(git curl sed awk grep tr cat sleep rm ls head git env date uname)
    local i=0 w
    for w in "${want[@]}"; do
        [ "${lines[i]}" = "$f: command not in commands.txt: $w" ]
        i=$((i + 1))
    done
    [[ ${lines[i]} == "$f: dynamic command word: "* ]]
    [ "${lines[i + 1]}" = "$f: eval is not allowed" ]
    [ "${#lines[@]}" -eq $((i + 2)) ]
}

@test "a command allowed only by another whitelist is reported" {
    local allow=$BATS_TEST_TMPDIR/allow.txt
    printf 'just\n' >"$allow"
    lint --allow "$allow" "$BATS_TEST_DIRNAME/fixture/lint_good.sh"
    [ "$status" -eq 1 ]
    [[ $output == *'command not in allow.txt: docker'* ]]
    [[ $output == *'command not in allow.txt: mkdir'* ]]
}

@test "backticks and heredocs are reported" {
    local f=$BATS_TEST_TMPDIR/tick.sh
    printf '%s\n' 'f() {' '    x=`date`' '    read -r y <<EOF' 'hi' 'EOF' '}' >"$f"
    lint "$f"
    [ "$status" -eq 1 ]
    [[ $output == *'backticks are not allowed'* ]]
    [[ $output == *'heredocs are not allowed'* ]]
}

@test "a syntax error is reported" {
    local f=$BATS_TEST_TMPDIR/broken.sh
    printf 'f() { if true; }\n' >"$f"
    lint "$f"
    [ "$status" -eq 1 ]
    [[ $output == *'syntax error'* ]]
}
