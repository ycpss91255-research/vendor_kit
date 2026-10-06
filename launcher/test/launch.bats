#!/usr/bin/env bats
# 啟動流程（launch.sh）：判定順序、起唯一的引擎、代辦每種 op 的 req→res 位元組、非法 req（VK0056）、
# 救援呼叫辨識、介面版不合（VK0009）、done 與容器結束碼的核對、中斷（N49）、收尾。
# docker 是假的（fixture/fake_docker.bash）：`start -ai` 當引擎，照 $fake/engine 寫 req、等 res。

load helper

setup() {
    common_setup
    A=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    B=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    E=eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
    engine="ghcr.io/acme/vendor_kit@sha256:$A"
    fake="$BATS_TEST_TMPDIR/fake"
    tmpd="$BATS_TEST_TMPDIR/tmp"
    mkdir -p "$fake" "$tmpd" "$work/.git" "$work/sub"
    fake_cmd docker "source '$BATS_TEST_DIRNAME/fixture/fake_docker.bash'"
    printf '1 1 v1.0.0' >"$fake/labels"
    printf '0' >"$fake/runner.rc"
    printf 'finish 0\n' >"$fake/engine"
    vk_env=(VK_FAKE="$fake" TMPDIR="$tmpd")
    sess="$tmpd/vendor_kit.r1"
}

# launch <P> [<recipe> <args>...]：在 $work/sub 下指令，安裝目錄是 $work。
launch() {
    local proto=$1 args='' a
    shift
    for a in "$@"; do
        args+=" $(printf '%q' "$a")"
    done
    vk "vk_log_version=0.0.0; vk_log_invocation_id=r1; vk_launch \"\$PWD\" \"\$PWD/sub\" '$engine' $proto$args; exit \$?"
}

# engine_does <bash>：假引擎的行為。
engine_does() {
    printf '%s\n' "$1" >"$fake/engine"
}

log_file() {
    local -a files=("$work/.vendor_kit/log"/*.jsonl)
    [ "${#files[@]}" -eq 1 ]
    REPLY=${files[0]}
}

internal() {
    log_file
    REPLY="vendor_kit: error[VK0056]: Internal vendor_kit error: $1. This is a VK bug. Report it at https://github.com/ycpss91255-research/vendor_kit/issues and attach run log $REPLY."
}

# res <seq> <result>：res.<seq> 的期待位元組與收到的相同。
assert_res() {
    local got
    got=$(cat "$fake/got/res.$1" && printf x)
    [ "$got" = "vk-resolve/1 r1 $1"$'\n'"$2"$'\n'x ] || {
        echo "res.$1: got ${got%x}" >&2
        return 1
    }
}

assert_called() {
    grep -qxF -- "$1" "$fake/calls" || {
        echo "not called: $1" >&2
        cat "$fake/calls" >&2
        return 1
    }
}

assert_not_called() {
    ! grep -q -- "$1" "$fake/calls"
}

last_finished() {
    log_file
    local -a lines
    mapfile -t lines <"$REPLY"
    REPLY=${lines[${#lines[@]} - 1]}
}

# ---- 起引擎 ----

@test "a recipe starts one engine with the frozen argv and cleans up" {
    launch 1 add foo -- '-x y'
    [ "$status" -eq 0 ]
    [ "$stderr" = "" ]
    log_file
    local rel=${REPLY#"$work/"}
    local -a want=(
        -i --init --user "$(id -u):$(id -g)" --label "vendor_kit.root=$work" --label vendor_kit.run=r1
        --mount "type=bind,\"source=$work\",target=/vk/root"
        --mount "type=bind,\"source=$sess/ctl\",target=/vk/ctl"
        --mount "type=bind,\"source=$sess/in\",target=/vk/in,readonly"
        -w /vk/root "$engine"
        --protocol 1 --run-id r1 --host-root "$work" --host-cwd "$work/sub" --run-log "$rel"
        --tty 000 --no-color 0 -- add foo -- '-x y'
    )
    mapfile -t got <"$fake/engine.argv"
    [ "${got[*]}" = "${want[*]}" ]
    [ "${#got[@]}" -eq "${#want[@]}" ]
    [[ $rel == .vendor_kit/log/*-add-r1.jsonl ]]
    # 同一個容器 create 一次、start 一次，收尾刪容器與 session
    [ "$(grep -c '^create' "$fake/calls")" -eq 1 ]
    assert_called "start -ai $E"
    assert_called "rm $E"
    [ ! -e "$sess" ]
    last_finished
    [[ $REPLY == *'"vendor_kit.exit_code":0,"vendor_kit.engine.exit_code":0,"vendor_kit.stop_reason_code":"none"}}' ]]
    assert_git_not_called
}

@test "the bare usage call passes nothing after -- and NO_COLOR is forwarded" {
    vk_env+=(NO_COLOR=1)
    launch 1
    [ "$status" -eq 0 ]
    mapfile -t got <"$fake/engine.argv"
    [ "${got[${#got[@]} - 1]}" = -- ]
    [ "${got[${#got[@]} - 2]}" = 1 ]
    [ "${got[${#got[@]} - 3]}" = --no-color ]
    log_file
    [[ $REPLY == *-vendor_kit-r1.jsonl ]]
}

@test "rootless docker gets no --user" {
    printf '["name=seccomp,profile=builtin","name=rootless"]' >"$fake/info"
    launch 1 sync
    [ "$status" -eq 0 ]
    mapfile -t got <"$fake/engine.argv"
    [ "${got[1]}" = --init ]
    [ "${got[2]}" = --label ]
}

@test "the engine exit code (done = container) is the run's exit code" {
    engine_does 'finish 3'
    launch 1 sync
    [ "$status" -eq 3 ]
    last_finished
    [[ $REPLY == *'"vendor_kit.exit_code":3,"vendor_kit.engine.exit_code":3,"vendor_kit.stop_reason_code":"none"}}' ]]
}

# ---- in/engine：這次用的 pinned 引用 ----

# 假引擎：起來時記下 in/ 的檔名與 in/engine，再試著 stage／extract 到 engine 這個 slot。
engine_reads_ref() {
    local src="$BATS_TEST_TMPDIR/other"
    printf 'other\n' >"$src"
    engine_does "
in=\$engine_ctl/../in
names=(\"\$in\"/*)
printf '%s\n' \"\${names[@]##*/}\" >\"\$VK_FAKE/in.names\"
cp \"\$in/engine\" \"\$VK_FAKE/ref\"
send 'stage e:$src engine'
send 'extract sha256:$B engine'
cp \"\$in/engine\" \"\$VK_FAKE/ref.after\"
finish 0
"
}

# assert_ref <file>：內容剛好是 pinned 引用加一個 LF。
assert_ref() {
    local got
    got=$(cat "$1" && printf x)
    [ "$got" = "$engine"$'\n'x ] || {
        echo "in/engine: got ${got%x}" >&2
        return 1
    }
}

@test "the pinned engine reference is written once to in/engine before the engine starts" {
    engine_reads_ref
    launch 1 add foo
    [ "$status" -eq 0 ] || {
        echo "$stderr" >&2
        return 1
    }
    # 一行、LF 結尾；.tmp 不留
    assert_ref "$fake/ref"
    [ "$(<"$fake/in.names")" = engine ]
    # 同名 slot 的 stage、extract 都被拒，內容不變
    assert_res 1 'failed 1'
    assert_res 2 'failed 1'
    assert_ref "$fake/ref.after"
    assert_not_called '^create --label'
    [ ! -e "$sess" ]
}

@test "rescue calls also get in/engine" {
    printf '2 3 v2.0.0' >"$fake/labels"
    local c
    for c in sync 'install' 'upgrade --engine' ''; do
        rm -rf "$work/.vendor_kit" "$fake/ref"
        engine_reads_ref
        # shellcheck disable=SC2086
        launch 1 $c
        [ "$status" -eq 0 ] || {
            echo "$c: $stderr" >&2
            return 1
        }
        assert_ref "$fake/ref" || {
            echo "$c" >&2
            return 1
        }
    done
}

@test "a call that fails validation creates no in/engine" {
    # 介面版不合（VK0009）與啟動器參數不合（VK0056）都停在建 session 之前
    printf '2 3 v2.0.0' >"$fake/labels"
    launch 1 add foo
    [ "$status" -eq 3 ]
    [ ! -e "$sess" ]
    rm -rf "$work/.vendor_kit"
    printf '1 1 v1.0.0' >"$fake/labels"
    vk "vk_log_version=0.0.0; vk_log_invocation_id=r1; vk_launch \"\$PWD\" \"\$PWD/sub\" ghcr.io/acme/vendor_kit:v1 1 sync; exit \$?"
    [ "$status" -eq 2 ]
    [ ! -e "$sess" ]
    assert_not_called '^create'
}

@test "an unwritable in/ stops with VK0056 before docker create and removes the session" {
    # in/engine.tmp 先放成目錄，寫入失敗
    engine_does 'finish 0'
    vk "vk_log_version=0.0.0; vk_log_invocation_id=r1; mkdir() { command mkdir \"\$@\" && if [[ \$* == *'$sess/ctl'* ]]; then command mkdir '$sess/in/engine.tmp'; fi; }; vk_launch \"\$PWD\" \"\$PWD/sub\" '$engine' 1 sync; exit \$?"
    [ "$status" -eq 2 ]
    internal "cannot write the engine reference to the session directory $sess"
    [ "$stderr" = "$REPLY" ]
    assert_not_called '^create'
    [ ! -e "$sess" ]
    last_finished
    [[ $REPLY == *'"vendor_kit.exit_code":2,"vendor_kit.engine.exit_code":null,"vendor_kit.stop_reason_code":"VK0056"}}' ]]
}

# ---- 每種 op 的 req→res ----

@test "every op is done on the host and answered with the exact result bytes" {
    printf 'token\n' >"$BATS_TEST_TMPDIR/my token"
    printf '%s' "$B" >"$fake/ps"
    printf '3' >"$fake/runner.rc"
    local tok
    tok="$BATS_TEST_TMPDIR/my token"
    tok=${tok// /\\040}
    engine_does "
send 'pull $engine'
send 'load e:/srv/u/my\\040proj/my\\040tools.tar'
send 'inspect $engine'
send 'extract sha256:$B x1'
[[ -f \$engine_ctl/../in/x1/from_image ]] && : >\"\$VK_FAKE/extract_seen\"
send 'stage e:$tok t1'
cp \"\$engine_ctl/../in/t1\" \"\$VK_FAKE/staged\"
send ps
send 'rm-container $B'
send 'runner ghcr.io/u/test:1 e:pytest e:-q e: e:a\\134b.py'
finish 0
"
    launch 1 sync
    [ "$status" -eq 0 ] || {
        echo "$stderr" >&2
        return 1
    }
    assert_res 1 ok
    assert_res 2 ok
    assert_res 3 ok
    assert_res 4 ok
    assert_res 5 ok
    assert_res 6 ok
    assert_res 7 ok
    assert_res 8 'runner exited 3'
    [ "$(<"$fake/got/res.3.out")" = '[{"Id":"sha256:'"$B"'"}]' ]
    [ "$(<"$fake/got/res.6.out")" = "$B" ]
    [ -e "$fake/extract_seen" ]
    [ "$(<"$fake/staged")" = token ]
    [ "$output" = "runner output" ]
    assert_called "pull -q $engine"
    assert_called 'load -q -i /srv/u/my\ proj/my\ tools.tar'
    assert_called "image inspect $engine"
    assert_called "create --label vendor_kit.root=$(printf '%q' "$work") --label vendor_kit.run=r1 --entrypoint /__vk_never_run__ sha256:$B"
    assert_called "cp ${C:=cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc}:/dist/. $(printf '%q' "$sess/in/x1")"
    assert_called "rm $C"
    assert_called "ps -a --no-trunc --filter label=vendor_kit.root=$(printf '%q' "$work") --filter status=exited --format \{\{.ID\}\}"
    assert_called "rm $B"
    # runner：repo 唯讀、.vendor_kit/ 遮住、command 不經 shell
    mapfile -t got <"$fake/runner.argv"
    local -a want=(
        --user "$(id -u):$(id -g)" --label "vendor_kit.root=$work" --label vendor_kit.run=r1
        --mount "type=bind,\"source=$work\",target=/vk/repo,readonly"
        --mount 'type=tmpfs,"target=/vk/repo/.vendor_kit"' --mount type=tmpfs,target=/tmp -w /vk/repo
        --entrypoint=pytest ghcr.io/u/test:1 -q '' 'a\b.py'
    )
    [ "${got[*]}" = "${want[*]}" ]
    [ "${#got[@]}" -eq "${#want[@]}" ]
    [ ! -e "$sess" ]
}

@test "failed docker actions are reported as failed <rc> or runner notstarted" {
    printf '1' >"$fake/rc.pull"
    printf '2' >"$fake/rc.cp"
    printf '125' >"$fake/rc.create-runner"
    printf '/srv/x' >"$BATS_TEST_TMPDIR/tok"
    engine_does "
send 'pull $engine'
send 'extract sha256:$B x1'
send 'stage e:/nonexistent/file t1'
send 'runner ghcr.io/u/test:1 e:pytest'
rm -f \"\$VK_FAKE/rc.create-runner\"
: >\"\$VK_FAKE/runner.notstarted\"
send 'runner ghcr.io/u/test:1 e:pytest'
send 'runner ghcr.io/u/test:1 e:'
finish 2
"
    launch 1 sync
    [ "$status" -eq 2 ]
    [ "$stderr" != "" ] # cp 的錯誤訊息原樣
    assert_res 1 'failed 1'
    assert_res 2 'failed 2'
    assert_res 3 'failed 1'
    assert_res 4 'runner notstarted'
    assert_res 5 'runner notstarted'
    assert_res 6 'runner notstarted'
    # cp 失敗也刪 extract 的容器
    assert_called "rm cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
}

# ---- 非法 req ----

@test "an invalid request stops the engine with VK0056" {
    local -a cases=(
        "raw req.1 'vk-resolve/1 r1 1\nrm-image x\n'" 'unknown op rm-image'
        "raw req.1 'vk-resolve/1 r2 1\nps\n'" 'request header does not match vk-resolve/1 r1'
        "raw req.1 'vk-resolve/1 r1 1\nps\0\n'" 'control file req.1 has a NUL byte'
        "raw req.1 'vk-resolve/1 r1 1\nps\r\n'" 'control file req.1 has a malformed line'
        "raw req.1 'vk-resolve/1 r1 1\npull ghcr.io/a:v1\n'" 'invalid operands for op pull'
        "raw req.2 'vk-resolve/1 r1 2\nps\n'" 'unexpected request file req.2 while waiting for req.1'
        "send 'rm-container $B'" "rm-container $B was not listed by ps"
    )
    local i
    for ((i = 0; i < ${#cases[@]}; i += 2)); do
        rm -rf "$work/.vendor_kit" "$fake/killed" "$fake/got" "$fake/calls"
        engine_does "${cases[i]}"$'\nawait 1\nfinish 0'
        launch 1 sync
        internal "${cases[i + 1]}"
        [ "$status" -eq 2 ] || {
            echo "${cases[i]}: status $status $stderr" >&2
            return 1
        }
        [ "$stderr" = "$REPLY" ] || {
            echo "${cases[i]}: $stderr" >&2
            return 1
        }
        [ ! -e "$fake/got/res.1" ]
        assert_called "kill $E"
        assert_called "rm $E"
        [ ! -e "$sess" ]
        last_finished
        [[ $REPLY == *'"vendor_kit.exit_code":2,"vendor_kit.engine.exit_code":137,"vendor_kit.stop_reason_code":"VK0056"}}' ]]
    done
}

@test "done must exist and match the engine container exit code" {
    engine_does 'finish 0 3'
    launch 1 sync
    [ "$status" -eq 2 ]
    internal 'done exit code 0 does not match the engine container exit code 3'
    [ "$stderr" = "$REPLY" ]
    last_finished
    [[ $REPLY == *'"vendor_kit.exit_code":2,"vendor_kit.engine.exit_code":3,"vendor_kit.stop_reason_code":"VK0056"}}' ]]

    rm -rf "$work/.vendor_kit"
    engine_does 'printf 1 >"$VK_FAKE/engine.exit"'
    launch 1 sync
    [ "$status" -eq 2 ]
    internal 'cannot read control file done (engine exit code 1)'
    [ "$stderr" = "$REPLY" ]
    [ ! -e "$sess" ]
}

@test "an engine container that does not stop is killed, and kept when it still runs" {
    : >"$fake/engine.running"
    launch 1 sync
    [ "$status" -eq 2 ]
    internal "the engine container $E did not stop; kept $sess"
    [ "$stderr" = "$REPLY" ]
    assert_called "kill $E"
    assert_not_called "^rm $E"
    [ -d "$sess" ]
}

# ---- 中斷（N49） ----

@test "an interrupt reaches the engine through --init; the launcher waits for it and finishes the run" {
    local sig code
    for sig in INT TERM; do
        code=130
        if [[ $sig == TERM ]]; then
            code=143
        fi
        rm -rf "$work/.vendor_kit" "$fake/calls" "$fake/engine.running" "$fake/engine.init"
        # 詢問中被中斷：引擎沒寫任何東西就停下，沒有 done
        engine_does "interrupt $sig"
        launch 1 add foo
        [ "$status" -eq "$code" ] || {
            echo "$sig: status $status $stderr" >&2
            return 1
        }
        # 不是 VK 的 bug，不印診斷
        [ "$stderr" = "" ]
        # docker start -ai 先返回；等引擎容器停下才收尾，不 kill
        assert_called "wait $E"
        assert_not_called "^kill"
        assert_called "rm $E"
        [ ! -e "$sess" ]
        last_finished
        [[ $REPLY == *"\"vendor_kit.exit_code\":$code,\"vendor_kit.engine.exit_code\":$code,\"vendor_kit.stop_reason_code\":\"none\"}}" ]] || {
            echo "$sig: $REPLY" >&2
            return 1
        }
    done
}

@test "an engine that keeps running after the interrupt is killed when the wait is interrupted again" {
    : >"$fake/engine.ignores"
    engine_does 'interrupt INT'
    launch 1 sync
    [ "$status" -eq 130 ]
    [ "$stderr" = "" ]
    assert_called "wait $E"
    assert_called "kill $E"
    assert_called "rm $E"
    [ ! -e "$sess" ]
    last_finished
    [[ $REPLY == *'"vendor_kit.exit_code":130,"vendor_kit.engine.exit_code":137,"vendor_kit.stop_reason_code":"none"}}' ]]
}

@test "an engine that writes done before stopping is checked as usual after an interrupt" {
    engine_does 'kill -s INT "$PPID"; finish 1'
    launch 1 sync
    [ "$status" -eq 1 ]
    [ "$stderr" = "" ]
    last_finished
    [[ $REPLY == *'"vendor_kit.exit_code":1,"vendor_kit.engine.exit_code":1,"vendor_kit.stop_reason_code":"none"}}' ]]
}

# ---- 救援呼叫 ----

@test "rescue calls are recognised by recipe name and --engine before --" {
    local -a yes=('' 'install' 'install -h' 'install -y' 'sync' 'sync --help' 'upgrade --engine'
        'upgrade --engine=v1.2.0' 'upgrade --engine -h' 'upgrade -h --engine' 'upgrade --help --engine=v1.0.0')
    local -a no=('add' 'add -h' 'upgrade' 'upgrade foo' 'upgrade -h' 'upgrade -- --engine' 'upgrade --engines'
        'remove --engine' 'test' 'dev --engine -i x' 'undev --engine' 'prune' 'update')
    local c
    for c in "${yes[@]}"; do
        vk "vk_launch_is_rescue $c || exit 1"
        [ "$status" -eq 0 ] || {
            echo "not rescue: $c" >&2
            return 1
        }
    done
    for c in "${no[@]}"; do
        vk "vk_launch_is_rescue $c || exit 1"
        [ "$status" -eq 1 ] || {
            echo "rescue: $c" >&2
            return 1
        }
    done
}

# ---- 介面版 ----

@test "an old shell running a general recipe stops with VK0009 before any container" {
    printf '2 3 v2.0.0' >"$fake/labels"
    launch 1 add foo
    [ "$status" -eq 3 ]
    [ "$output" = "" ]
    [ "$stderr" = 'vendor_kit: fatal[VK0009]: Shell interface version 1 is older than required for general recipes in engine v2.0.0. Run first: just vendor_kit upgrade --engine' ]
    assert_not_called '^create'
    assert_not_called '^pull'
    [ ! -e "$sess" ]
    log_file
    local -a lines
    mapfile -t lines <"$REPLY"
    [ "${#lines[@]}" -eq 3 ]
    [[ ${lines[1]} == *'"event_name":"diagnostic_emitted"'*'"vendor_kit.reason_code":"VK0009"'* ]]
    [[ ${lines[2]} == *'"vendor_kit.exit_code":3,"vendor_kit.engine.exit_code":null,"vendor_kit.stop_reason_code":"VK0009"}}' ]]
    # -h 也一樣
    rm -rf "$work/.vendor_kit"
    launch 1 add -h
    [ "$status" -eq 3 ]
}

@test "rescue calls skip the interface check and start the engine" {
    printf '2 3 v2.0.0' >"$fake/labels"
    local c
    for c in sync 'install' 'upgrade --engine' 'upgrade --engine -h' ''; do
        rm -rf "$work/.vendor_kit"
        # shellcheck disable=SC2086
        launch 1 $c
        [ "$status" -eq 0 ] || {
            echo "$c: $stderr" >&2
            return 1
        }
    done
    assert_not_called 'image inspect --format'
}

@test "interface versions inside the range pass; a shell newer than the engine is an internal error" {
    printf '1 3 v2.0.0' >"$fake/labels"
    launch 3 add foo
    [ "$status" -eq 0 ]
    rm -rf "$work/.vendor_kit" "$fake/calls"
    launch 4 add foo
    [ "$status" -eq 2 ]
    internal 'shell interface version 4 is newer than the engine range 1-3'
    [ "$stderr" = "$REPLY" ]
    assert_not_called '^create'
}

@test "a missing or malformed LABEL is an internal error" {
    local l
    for l in '  ' '0 1 v' '2 1 v' 'x 1 v' '01 1 v'; do
        rm -rf "$work/.vendor_kit"
        printf '%s' "$l" >"$fake/labels"
        launch 1 add foo
        [ "$status" -eq 2 ]
        internal "the engine image $engine does not announce a valid interface version range"
        [ "$stderr" = "$REPLY" ]
    done
    assert_not_called '^create'
}

@test "without a local engine image the call stops before pulling or creating anything (#42)" {
    rm "$fake/labels"
    launch 1 add foo
    [ "$status" -eq 2 ]
    internal "engine image $engine is not available locally; the interface version cannot be checked offline (#42)"
    [ "$stderr" = "$REPLY" ]
    assert_not_called '^pull'
    assert_not_called '^create'
    [ ! -e "$sess" ]
    last_finished
    [[ $REPLY == *'"vendor_kit.exit_code":2,"vendor_kit.engine.exit_code":null,"vendor_kit.stop_reason_code":"VK0056"}}' ]]
}

# ---- 主機前置檢查在建執行紀錄之前 ----

@test "a failed host precheck stops before the run log" {
    fake_version docker 'podman version 4.9.3'
    launch 1 sync
    [ "$status" -eq 2 ]
    [[ $stderr == *'[VK0011]'* ]]
    [ ! -e "$work/.vendor_kit" ]
}
