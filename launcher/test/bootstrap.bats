#!/usr/bin/env bats
# bootstrap.sh 的參數、模式判定與主機檢查（bootstrap_main.sh；04 bootstrap.sh、ADR-0007 的驗收清單）。
#
# - 判定順序：-h → 判定 1（.vendor_kit/、有效鎖定行、未完成的首次導入）→ 用法 → 主機 → 判定 3
#   （VK0040 → VK0035 → VK0029 → VK0039 → VK0037）。被拒絕時都只印 stderr，不建執行紀錄、不寫檔、不呼叫 git。
# - 未完成首次導入的判定（vk_bootstrap_assess）鏡射 engine/runlog 的 assess：紀錄行取自
#   engine/runlog/src/tests.rs 的 golden，案例對照該檔「判定未完成首次導入」一節。
# - 通過全部檢查時，這一版停在建紀錄之前，以 VK0056 停下（下一個 PR 接）。

load helper

setup() {
    common_setup
    A=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    engine_v1="ghcr.io/acme/vendor_kit:v1.0.0@sha256:$A"
    engine_v2="ghcr.io/acme/vendor_kit:v2.3.4@sha256:$A"
    embedded=$engine_v1
    usage_line='Usage: bootstrap.sh [-i <image>] [-y] | --repair [-i <image>] | -h'
    pending='vendor_kit: error[VK0056]: Internal vendor_kit error: creating the run log and starting the engine are not implemented yet (next PR, #372). This is a VK bug. Report it at https://github.com/ycpss91255-research/vendor_kit/issues and attach run log none.'
    no_git='vendor_kit: error[VK0035]: Cannot find .git in the current directory or any parent directory. Run bootstrap.sh from within a Git repository.'
    bad_lock='vendor_kit: error[VK0037]: Cannot read exactly one valid engine lock version line from .vendor_kit/version.toml. Initial import was not attempted.'
    repair_outside='vendor_kit: error[VK0039]: Cannot repair shell files outside an install directory. Initial import was not attempted.'
    no_docker='vendor_kit: error[VK0033]: Docker was not found on the host. Install Docker and retry.'
    podman='vendor_kit: error[VK0011]: Detected Podman (docker --version). vendor_kit supports only Docker. Switch to Docker (rootful or rootless) and retry.'
    log_dir="$work/.vendor_kit/log"
    rust_golden golden_run_started && RS=$REPLY
    rust_golden golden_engine_started && ES=$REPLY
    rust_golden golden_diagnostic_emitted && DG=$REPLY
    rust_golden golden_writes_started && WS=$REPLY
    rust_golden golden_lock_line_write_started && LWS_E=$REPLY
    LWS_T=${LWS_E/'"vendor_kit.target":"engine"'/'"vendor_kit.target":"tool"'}
    rust_golden golden_lock_line_written && LW_T=$REPLY
    LW_E=${LW_T/'"vendor_kit.target":"tool"'/'"vendor_kit.target":"engine"'}
    rust_golden golden_progress_removed && PR=$REPLY
    rust_golden golden_engine_finished && EF=$REPLY
    rust_golden golden_run_finished && RF=$REPLY
    rust_golden golden_run_finished_without_engine && RF_NONE=$REPLY
    EF0=${EF/'"vendor_kit.exit_code":2'/'"vendor_kit.exit_code":0'}
}

ok_docker() { fake_version docker 'Docker version 24.0.7, build afdd53b'; }
ok_just() { fake_version just 'just 1.33.0'; }
ok_host() {
    ok_docker
    ok_just
}

# bs <args>...：在 vk_cwd（預設 $work）跑 vk_bootstrap_main，內嵌引擎是 $embedded。
bs() {
    local q='' a x
    for a in "$@"; do
        printf -v x ' %q' "$a"
        q+=$x
    done
    printf -v x '%q' "$embedded"
    vk "vk_bootstrap_engine=$x; vk_bootstrap_main$q"
}

repo() { mkdir -p "$work/.git"; }

# installed [<引用>]：有效鎖定行的安裝目錄。
installed() {
    mkdir -p "$work/.vendor_kit"
    printf 'vendor_kit = "%s"\nschema = 1\n' "${1:-$engine_v1}" >"$work/.vendor_kit/version.toml"
}

# write_log <檔名的 ts> <行>...：在 $log_dir 寫一份紀錄（每行加 LF）。
write_log() {
    local ts=$1
    shift
    mkdir -p "$log_dir"
    printf '%s\n' "$@" >"$log_dir/$ts-bootstrap-inv-1.jsonl"
}

# 停在 VK0002、沒寫任何檔的首次導入（tests.rs 的 stopped_at_prompt）。
stopped_at_prompt() {
    write_log 20261005T010203.000004Z "$RS" "$ES" "$DG" "$EF" "$RF"
}

snap() {
    (cd "$work" && find . | LC_ALL=C sort)
}

# assert_stopped <status> <stderr> <snap 之前>：只印 stderr、沒有 stdout、檔案沒變、沒呼叫 git。
assert_stopped() {
    [ "$status" -eq "$1" ]
    [ "$output" = "" ]
    [ "$stderr" = "$2" ]
    [ "$(snap)" = "$3" ]
    assert_git_not_called
}

usage_bad() {
    REPLY="vendor_kit: error[VK0026]: Unknown, extra, or disallowed argument: $1."$'\n'"$usage_line"
}

# ---- -h／--help ----

@test "-h and --help alone print usage only, without host checks or writes" {
    mkdir -p "$work/.vendor_kit"
    local before
    before=$(snap)
    for h in -h --help; do
        bs "$h"
        [ "$status" -eq 0 ]
        [ "$stderr" = "" ]
        [[ ${lines[0]} == "$usage_line" ]]
        [[ $output != *"$A"* && $output != *v1.0.0* ]]
        [ "$(snap)" = "$before" ]
    done
    assert_git_not_called
}

@test "-h with other arguments is VK0026 with the documented value" {
    local before
    before=$(snap)
    local -a cases=(
        '-h -y|-y' '-y -h|-y' '-h --help|--help' '-h -h|-h' '--help -h|-h'
        '-h --repair|--repair' '-h -i x|-i' '-h --|--' '-h -- -h|--'
    )
    local c args want
    for c in "${cases[@]}"; do
        args=${c%|*}
        want=${c#*|}
        # shellcheck disable=SC2086
        bs $args
        usage_bad "$want"
        assert_stopped 2 "$REPLY" "$before"
    done
}

# ---- 參數 ----

@test "unknown options, positional arguments and anything after -- are VK0026, first one wins" {
    ok_host
    repo
    local before
    before=$(snap)
    local -a cases=(
        '-x|-x' '-x -z|-x' 'foo|foo' '-y foo|foo' '--version|--version' '-yi|-yi'
        '--image=x|--image=x' '--repair=1|--repair=1' '-- -y|-y' '-- foo bar|foo' '-x -i|-x'
    )
    local c args want
    for c in "${cases[@]}"; do
        args=${c%|*}
        want=${c#*|}
        # shellcheck disable=SC2086
        bs $args
        usage_bad "$want"
        assert_stopped 2 "$REPLY" "$before"
    done
}

@test "an option given twice is VK0026 on the second one" {
    ok_host
    repo
    local before
    before=$(snap)
    bs -y --yes
    usage_bad --yes
    assert_stopped 2 "$REPLY" "$before"
    bs -i a --image b
    usage_bad --image
    assert_stopped 2 "$REPLY" "$before"
    installed
    before=$(snap)
    bs --repair --repair
    usage_bad --repair
    assert_stopped 2 "$REPLY" "$before"
}

@test "-i or --image without an image is VK0025" {
    ok_host
    repo
    local before
    before=$(snap)
    bs -i
    assert_stopped 2 "vendor_kit: error[VK0025]: Required argument is missing: -i <image>."$'\n'"$usage_line" "$before"
    bs -y --image
    assert_stopped 2 "vendor_kit: error[VK0025]: Required argument is missing: --image <image>."$'\n'"$usage_line" "$before"
}

@test "short and long options are synonyms in any order; -i takes the next argument as is" {
    ok_host
    repo
    local before
    before=$(snap)
    for args in '-y' '--yes' '-i img -y' '-y --image img' '--image -y' '-i -- -y' '-y --'; do
        # shellcheck disable=SC2086
        bs $args
        assert_stopped 2 "$pending" "$before"
    done
}

@test "--repair -y is VK0026 everywhere" {
    ok_host
    repo
    local before
    before=$(snap)
    bs --repair -y
    usage_bad -y
    assert_stopped 2 "$REPLY" "$before"
    installed
    before=$(snap)
    bs --yes --repair
    usage_bad --yes
    assert_stopped 2 "$REPLY" "$before"
    # 未完成的首次導入也不收 --repair -y
    rm "$work/.vendor_kit/version.toml"
    stopped_at_prompt
    before=$(snap)
    bs --repair -y
    usage_bad -y
    assert_stopped 2 "$REPLY" "$before"
}

@test "-y in an existing install directory is VK0026, also without a valid lock line" {
    ok_host
    repo
    installed
    local before
    before=$(snap)
    bs -y
    usage_bad -y
    assert_stopped 2 "$REPLY" "$before"
    # 讀不出有效鎖定行、又不是未完成的首次導入：用法先判，不是 VK0037
    rm "$work/.vendor_kit/version.toml"
    before=$(snap)
    bs -i img --yes
    usage_bad --yes
    assert_stopped 2 "$REPLY" "$before"
}

@test "usage is judged before host checks" {
    repo
    local before
    before=$(snap)
    bs -x
    usage_bad -x
    assert_stopped 2 "$REPLY" "$before"
}

# ---- 主機檢查（ADR-0007 驗收：三種模式的 docker、首次導入的 just） ----

# each_mode <stderr>：首次導入、只檢查、修復各跑一次，都要以 stderr 停下、不寫檔。
each_mode() {
    local want=$1 before
    rm -rf "$work/.vendor_kit"
    before=$(snap)
    bs
    assert_stopped 2 "$want" "$before"
    installed
    before=$(snap)
    bs
    assert_stopped 2 "$want" "$before"
    bs --repair
    assert_stopped 2 "$want" "$before"
}

@test "docker missing stops initial import, check and repair with VK0033" {
    ok_just
    repo
    each_mode "$no_docker"
}

@test "docker --version containing podman stops every mode with VK0011" {
    ok_just
    repo
    fake_version docker 'podman version 4.9.3'
    each_mode "$podman"
}

@test "docker older than 19.03 stops every mode with VK0012" {
    ok_just
    repo
    fake_version docker 'Docker version 18.09.7, build 2d0083d'
    each_mode 'vendor_kit: error[VK0012]: Docker 19.03 or later is required; the current version is 18.09.7. Upgrade Docker and retry.'
}

@test "just missing or older than 1.33.0 stops initial import with VK0034 or VK0005" {
    ok_docker
    repo
    local before
    before=$(snap)
    bs
    [ "$status" -eq 2 ]
    [[ $stderr == 'vendor_kit: error[VK0034]: just was not found on the host. Use the GitHub release.'$'\n''Download: https://github.com/casey/just/releases/latest'$'\n''Install: '* ]]
    [ "$(snap)" = "$before" ]
    fake_version just 'just 1.32.0'
    bs -y
    [ "$status" -eq 2 ]
    [[ $stderr == 'vendor_kit: error[VK0005]: just 1.33.0 or later is required; the current version is 1.32.0. Use the GitHub release.'$'\n''Download: https://github.com/casey/just/releases/latest'$'\n''Install: '* ]]
    [ "$(snap)" = "$before" ]
    assert_git_not_called
}

@test "an incomplete initial import checks just too" {
    ok_docker
    repo
    mkdir -p "$work/.vendor_kit"
    stopped_at_prompt
    local before
    before=$(snap)
    bs -y
    [ "$status" -eq 2 ]
    [[ $stderr == 'vendor_kit: error[VK0034]: '* ]]
    [ "$(snap)" = "$before" ]
}

@test "check and repair do not check just" {
    ok_docker
    repo
    installed
    local before
    before=$(snap)
    bs
    assert_stopped 2 "$pending" "$before"
    bs --repair -i img
    assert_stopped 2 "$pending" "$before"
}

@test "host checks come before the checks before the run log" {
    local before
    before=$(snap)
    bs
    assert_stopped 2 "$no_docker" "$before"
}

# ---- 建紀錄前的拒絕 ----

@test "no .git upward stops every mode with VK0035, without writes or calling git" {
    ok_host
    each_mode "$no_git"
    # 非安裝目錄的 --repair 也先判 git 位置
    rm -rf "$work/.vendor_kit"
    local before
    before=$(snap)
    bs --repair
    assert_stopped 2 "$no_git" "$before"
}

@test ".git as a file (worktree, submodule) counts" {
    ok_host
    printf 'gitdir: /elsewhere\n' >"$work/.git"
    local before
    before=$(snap)
    bs
    assert_stopped 2 "$pending" "$before"
}

@test "a lock line of another X stops check and repair with VK0040 (exit 3) before the git check" {
    ok_host
    installed "$engine_v2"
    local want='vendor_kit: fatal[VK0040]: This bootstrap.sh is for major version 1, but the locked engine requires major version 2. No files were modified. Download bootstrap.sh for major version 2 from the Release and retry.'
    local before
    before=$(snap)
    bs
    assert_stopped 3 "$want" "$before"
    bs --repair
    assert_stopped 3 "$want" "$before"
    # 同一個 X 的其他版本照常
    installed "ghcr.io/acme/vendor_kit:v1.9.0@sha256:$A"
    repo
    before=$(snap)
    bs
    assert_stopped 2 "$pending" "$before"
}

@test "--repair outside an install directory is VK0039" {
    ok_host
    repo
    local before
    before=$(snap)
    bs --repair
    assert_stopped 2 "$repair_outside" "$before"
    bs -i img --repair
    assert_stopped 2 "$repair_outside" "$before"
}

@test "an invalid lock line without the exception is VK0037, in check and repair" {
    ok_host
    repo
    mkdir -p "$work/.vendor_kit"
    local before
    before=$(snap)
    bs
    assert_stopped 2 "$bad_lock" "$before"
    bs --repair
    assert_stopped 2 "$bad_lock" "$before"
    bs -i img
    assert_stopped 2 "$bad_lock" "$before"
    local v
    for v in \
        'vendor_kit = "ghcr.io/acme/vendor_kit:v1.0.0"\n' \
        'vendor_kit = "ghcr.io/acme/vendor_kit:latest@sha256:'"$A"'"\n' \
        'vendor_kit = "ghcr.io/acme/vendor_kit:v01.0.0@sha256:'"$A"'"\n' \
        'vendor_kit = "ghcr.io/acme/vendor_kit:v1.0.0@sha256:'"$A"'"\nvendor_kit = "x"\n'; do
        # shellcheck disable=SC2059
        printf "$v" >"$work/.vendor_kit/version.toml"
        before=$(snap)
        bs
        assert_stopped 2 "$bad_lock" "$before"
    done
}

@test ".vendor_kit as a file is not a fresh directory either" {
    ok_host
    repo
    : >"$work/.vendor_kit"
    local before
    before=$(snap)
    bs
    assert_stopped 2 "$bad_lock" "$before"
}

@test "--repair in an incomplete initial import is still VK0037" {
    ok_host
    repo
    mkdir -p "$work/.vendor_kit"
    stopped_at_prompt
    local before
    before=$(snap)
    bs --repair
    assert_stopped 2 "$bad_lock" "$before"
}

@test "an embedded engine reference that is not pinned vX.Y.Z is a VK bug" {
    ok_host
    repo
    local before
    before=$(snap)
    for embedded in '' "ghcr.io/acme/vendor_kit:v1.0.0" "ghcr.io/acme/vendor_kit:latest@sha256:$A"; do
        bs
        assert_stopped 2 'vendor_kit: error[VK0056]: Internal vendor_kit error: the embedded engine reference is not a pinned vX.Y.Z image reference. This is a VK bug. Report it at https://github.com/ycpss91255-research/vendor_kit/issues and attach run log none.' "$before"
    done
}

@test "every mode that passes stops before creating the run log with VK0056" {
    ok_host
    repo
    local before
    before=$(snap)
    bs
    assert_stopped 2 "$pending" "$before"
    installed
    before=$(snap)
    bs
    assert_stopped 2 "$pending" "$before"
    bs --repair
    assert_stopped 2 "$pending" "$before"
    [ ! -e "$log_dir" ]
}

# ---- 首次導入的巢狀安裝（VK0029；鏡射 engine/layout 的 check_nested） ----

nested() {
    REPLY="vendor_kit: error[VK0029]: Cannot create a nested install directory: $1 is already an install directory."
}

@test "an install directory above, nearest first, up to and including the repo root" {
    ok_host
    repo
    mkdir -p "$work/.vendor_kit" "$work/a/.vendor_kit" "$work/a/b/c" "$work/x/y"
    local before
    before=$(snap)
    vk_cwd=$work/a/b/c bs
    nested "$work/a"
    assert_stopped 2 "$REPLY" "$before"
    vk_cwd=$work/x/y bs -y
    nested "$work"
    assert_stopped 2 "$REPLY" "$before"
}

@test "nothing above the repo root is looked at" {
    ok_host
    mkdir -p "$work/.vendor_kit" "$work/repo/.git" "$work/repo/app"
    local before
    before=$(snap)
    vk_cwd=$work/repo/app bs
    assert_stopped 2 "$pending" "$before"
    vk_cwd=$work/repo bs
    assert_stopped 2 "$pending" "$before"
}

@test "an install directory below, the first in byte-sorted preorder" {
    ok_host
    repo
    mkdir -p "$work/z/.vendor_kit" "$work/b/deep/.vendor_kit" "$work/b/deep/inner/.vendor_kit" "$work/a/plain" "$work/B/.vendor_kit"
    local before
    before=$(snap)
    bs
    nested "$work/B"
    assert_stopped 2 "$REPLY" "$before"
    rm -r "$work/B"
    before=$(snap)
    bs
    nested "$work/b/deep"
    assert_stopped 2 "$REPLY" "$before"
}

@test ".git internals, symlinks and .vendor_kit files or symlinks below are not install directories" {
    ok_host
    repo
    mkdir -p "$work/.git/modules/x/.vendor_kit" "$BATS_TEST_TMPDIR/elsewhere/.vendor_kit" "$work/src" "$work/f" "$work/l"
    ln -s "$BATS_TEST_TMPDIR/elsewhere" "$work/src/linked"
    : >"$work/f/.vendor_kit"
    ln -s "$BATS_TEST_TMPDIR/elsewhere/.vendor_kit" "$work/l/.vendor_kit"
    local before
    before=$(snap)
    bs
    assert_stopped 2 "$pending" "$before"
}

@test "the own .vendor_kit/ of an incomplete initial import is not looked into" {
    ok_host
    repo
    mkdir -p "$work/.vendor_kit/cache/tool/.vendor_kit"
    stopped_at_prompt
    local before
    before=$(snap)
    bs -y
    assert_stopped 2 "$pending" "$before"
}

@test "check and repair do not look for nested install directories" {
    ok_host
    repo
    installed
    mkdir -p "$work/sub/.vendor_kit"
    local before
    before=$(snap)
    bs
    assert_stopped 2 "$pending" "$before"
}

@test "the nested search restores dotglob and nullglob" {
    mkdir -p "$work/a"
    vk 'vk_bootstrap_nested "$PWD" "$PWD"; shopt -q dotglob && exit 9; shopt -q nullglob && exit 8; exit 0'
    [ "$status" -eq 0 ]
    vk 'shopt -s dotglob; vk_bootstrap_nested "$PWD" "$PWD"; shopt -q dotglob || exit 9; exit 0'
    [ "$status" -eq 0 ]
}

# ---- 未完成首次導入的判定（鏡射 engine/runlog 的 assess；案例對照 tests.rs） ----

# assess <行>...：把這些行（各加 LF）寫成一份紀錄，跑 vk_bootstrap_assess；套用是 0、不套用是 1。
assess() {
    printf '%s\n' "$@" >"$work/l.jsonl"
    vk 'vk_bootstrap_assess "$PWD/l.jsonl"; exit $?'
}

# assess_raw <printf %s 的內容>
assess_raw() {
    printf '%s' "$1" >"$work/l.jsonl"
    vk 'vk_bootstrap_assess "$PWD/l.jsonl"; exit $?'
}

@test "assess: condition (a) stopped at VK0002 without writes" {
    assess "$RS" "$ES" "$DG" "$EF" "$RF"
    [ "$status" -eq 0 ]
}

@test "assess: condition (b) ended before the engine lock line" {
    local dg=${DG/'"VK0002"'/'"VK0036"'}
    dg=${dg/'"vendor_kit.placeholder.command_with_y":"./bootstrap.sh -y"'/'"vendor_kit.placeholder.image":"i","vendor_kit.placeholder.reason":"r"'}
    local rf=${RF/'"VK0002"'/'"VK0036"'}
    assess "$RS" "$ES" "$WS" "$LWS_T" "$LW_T" "$dg" "$EF" "$rf"
    [ "$status" -eq 0 ]
}

@test "assess: condition (b) when only the launcher saw the end" {
    local rf=${RF/'"vendor_kit.exit_code":2,"vendor_kit.engine.exit_code":2,"vendor_kit.stop_reason_code":"VK0002"'/'"vendor_kit.exit_code":3,"vendor_kit.engine.exit_code":137,"vendor_kit.stop_reason_code":"none"'}
    assess "$RS" "$ES" "$WS" "$rf"
    [ "$status" -eq 0 ]
}

@test "assess: a prompt stop after writes falls back to condition (b)" {
    assess "$RS" "$WS" "$DG" "$RF"
    [ "$status" -eq 0 ]
}

@test "assess: every golden line reads back" {
    assess "$RS" "$ES" "$DG" "$WS" "$LWS_T" "$LW_T" "$PR" "$EF" "$RF"
    [ "$status" -eq 0 ]
    assess "$RS" "$RF_NONE"
    [ "$status" -eq 0 ]
}

@test "assess: not applicable cases" {
    # 引擎版本鎖定行已經寫過
    assess "$RS" "$WS" "$LWS_E" "$LW_E" "$EF0"
    [ "$status" -eq 1 ]
    # 有 started 沒有 written
    assess "$RS" "$WS" "$LWS_E" "$EF"
    [ "$status" -eq 1 ]
    assess "$RS" "$WS" "$LWS_T" "$EF"
    [ "$status" -eq 1 ]
    # writes_started 之前改檔
    assess "$RS" "$LWS_E" "$LW_E" "$DG" "$RF"
    [ "$status" -eq 1 ]
    assess "$RS" "$PR" "$DG" "$RF"
    [ "$status" -eq 1 ]
    # written 之前沒有 started
    assess "$RS" "$LW_E" "$EF0"
    [ "$status" -eq 1 ]
    # 沒有 run_started、run_started 兩筆或不在第一行
    assess "$ES" "$DG" "$EF" "$RF"
    [ "$status" -eq 1 ]
    assess "$RS" "$RS" "$EF0"
    [ "$status" -eq 1 ]
    assess "$ES" "$RS" "$EF0"
    [ "$status" -eq 1 ]
    # 一份紀錄裡兩個 invocation_id
    assess "$RS" "$ES" "$DG" "${EF/'"inv-1"'/'"inv-2"'}" "$RF"
    [ "$status" -eq 1 ]
    # 不是首次導入
    for mode in check repair recipe; do
        assess "${RS/initial_import/$mode}" "$EF0"
        [ "$status" -eq 1 ]
    done
    # 沒有結束事件
    assess "$RS" "$ES" "$WS"
    [ "$status" -eq 1 ]
    # 停下原因沒有對應的診斷
    assess "$RS" "$EF" "$RF"
    [ "$status" -eq 1 ]
    # run_finished 兩筆
    assess "$RS" "$WS" "$RF_NONE" "$RF_NONE"
    [ "$status" -eq 1 ]
}

@test "assess: empty, truncated or NUL logs are not applicable" {
    assess_raw ''
    [ "$status" -eq 1 ]
    local text
    text=$(printf '%s\n' "$RS" "$ES" "$DG" "$EF" "$RF")
    assess_raw "${text:0:${#text}-10}"
    [ "$status" -eq 1 ]
    # 只少了最後的 LF
    assess_raw "$text"
    [ "$status" -eq 1 ]
    printf '%s\n%s\n' "$RS" "$ES" >"$work/l.jsonl"
    printf '\0\n' >>"$work/l.jsonl"
    printf '%s\n%s\n' "$EF0" "$RF_NONE" >>"$work/l.jsonl"
    vk 'vk_bootstrap_assess "$PWD/l.jsonl"; exit $?'
    [ "$status" -eq 1 ]
}

@test "assess: an unsupported log format is not applicable" {
    assess "$RS" "${ES/'"vendor_kit.log_format":"1"'/'"vendor_kit.log_format":"2"'}" "$DG" "$EF" "$RF"
    [ "$status" -eq 1 ]
}

@test "assess: malformed lines are not applicable (tests.rs malformed_lines_are_invalid)" {
    local -a base=("$RS" "$ES" "$DG" "$EF" "$RF")
    # 非正規的跳脫：把 "." 寫成反斜線加 u002e
    local bsl='\' escaped
    escaped=${ES/Engine started./Engine started${bsl}u002e}
    [[ $escaped == *"Engine started${bsl}u002e"* ]]
    local -a cases=(
        "1|$RS"$'\r'
        "2|${ES/'":"'/'": "'}"
        "2|${ES/'"severity_text":"info","severity_number":9'/'"severity_number":9,"severity_text":"info"'}"
        "2|$escaped"
        "1|${RS/initial_import/initial-import}"
        "5|${RF/'"VK0002"'/'"VK9999"'}"
        "2|${ES/engine_started/engine_begun}"
        "1|${RS/'"launcher"'/'"engine"'}"
        "3|${DG/'"error","severity_number":17'/'"warn","severity_number":13'}"
        "2|${ES/.000004Z/.0004Z}"
        "4|not json"
        "4|${EF/'"vendor_kit.exit_code":2'/'"vendor_kit.exit_code":2,"x":1'}"
        "3|${DG/'"error","severity_number":17'/'"error","severity_number":9'}"
        "2|${ES/T01:02:03/T25:02:03}"
        "5|${RF/'"vendor_kit.exit_code":2,'/'"vendor_kit.exit_code":256,'}"
        "5|${RF/'"Run finished."'/'"Run done."'}"
        "2|${ES/'"service.version":"0.0.0"'/'"service.version":""'}"
    )
    local c n line
    for c in "${cases[@]}"; do
        n=${c%%|*}
        line=${c#*|}
        local -a l=("${base[@]}")
        l[n - 1]=$line
        assess "${l[@]}"
        [ "$status" -eq 1 ]
    done
    # 原樣的紀錄是套用的（上面每一條都只改一個地方）
    assess "${base[@]}"
    [ "$status" -eq 0 ]
}

@test "assess: a misspelled target is not applicable" {
    assess "$RS" "$WS" "${LWS_E/'"target":"engine"'/'"target":"Engine"'}" "$LW_E" "$EF0"
    [ "$status" -eq 1 ]
}

# ---- 最近一筆紀錄的挑選（N93：檔名的 ts、撞名、時鐘回調） ----

@test "the incomplete initial import exception allows -y and initial import" {
    ok_host
    repo
    mkdir -p "$work/.vendor_kit"
    stopped_at_prompt
    local before
    before=$(snap)
    bs -y
    assert_stopped 2 "$pending" "$before"
    bs -i img
    assert_stopped 2 "$pending" "$before"
}

@test "only the newest log counts, never an older one" {
    ok_host
    repo
    mkdir -p "$work/.vendor_kit"
    stopped_at_prompt
    write_log 20261005T010203.000005Z "${RS/initial_import/check}" "$EF0"
    local before
    before=$(snap)
    bs -y
    usage_bad -y
    assert_stopped 2 "$REPLY" "$before"
    bs
    assert_stopped 2 "$bad_lock" "$before"
}

@test "names not in the launcher format are not logs" {
    ok_host
    repo
    mkdir -p "$work/.vendor_kit"
    stopped_at_prompt
    printf '%s\n' "${RS/initial_import/check}" >"$log_dir/zzz.jsonl"
    printf '%s\n' "${RS/initial_import/check}" >"$log_dir/20261005T010203.000009Z-bootstrap-INV.jsonl"
    printf '%s\n' "${RS/initial_import/check}" >"$log_dir/20261305T010203.000009Z-bootstrap-inv-1.jsonl"
    local before
    before=$(snap)
    bs -y
    assert_stopped 2 "$pending" "$before"
}

@test "two logs with the same newest ts cannot be told apart" {
    ok_host
    repo
    mkdir -p "$work/.vendor_kit"
    stopped_at_prompt
    printf '%s\n' "$RS" "$ES" "$DG" "$EF" "$RF" >"$log_dir/20261005T010203.000004Z-bootstrap-inv-2.jsonl"
    local before
    before=$(snap)
    bs -y
    usage_bad -y
    assert_stopped 2 "$REPLY" "$before"
}

@test "no log at all is not an incomplete initial import" {
    ok_host
    repo
    mkdir -p "$log_dir"
    local before
    before=$(snap)
    bs -y
    usage_bad -y
    assert_stopped 2 "$REPLY" "$before"
}

# run_logged <us> <bash 片段> [<status>]：時鐘固定在 us，以啟動器的 vk_log_start 建一份新紀錄。
run_logged() {
    vk "vk_now_us() { REPLY=$1; }; vk_log_version=0.0.0; vk_log_invocation_id=inv-3; $2"
    [ "$status" -eq "${3:-0}" ]
}

@test "after the clock goes back, the log written last is still the newest" {
    ok_host
    repo
    mkdir -p "$work/.vendor_kit"
    stopped_at_prompt
    # 時鐘比既有紀錄早一天：新紀錄的檔名仍排在既有的最大 ts 之後，所以它才是最近一筆
    run_logged 1791075723000004 'vk_log_start "$PWD/.vendor_kit/log" bootstrap check && vk_log_finish 0 "" none'
    [ -e "$log_dir/20261005T010203.000005Z-bootstrap-inv-3.jsonl" ]
    local before
    before=$(snap)
    bs -y
    usage_bad -y
    assert_stopped 2 "$REPLY" "$before"
}

@test "an initial import that stopped at VK0002 after the clock went back is still recognized" {
    ok_host
    repo
    mkdir -p "$work/.vendor_kit"
    write_log 20261005T010203.000004Z "${RS/initial_import/check}" "$RF_NONE"
    run_logged 1791075723000004 'vk_log_start "$PWD/.vendor_kit/log" bootstrap initial_import -y && vk_diag VK0002 command_with_y "./bootstrap.sh -y"; vk_log_finish 2 "" VK0002' 2
    local before
    before=$(snap)
    bs -y
    assert_stopped 2 "$pending" "$before"
}
