#!/usr/bin/env bats
# bootstrap.sh 在既有安裝目錄的只檢查與 --repair（bootstrap_main.sh 的 vk_bootstrap_check；04 bootstrap.sh
# 判定 4、用哪一版引擎，ADR-0007 的驗收清單）：比對之前先建紀錄（mode check 或 repair），用鎖定行那一版引擎
# （不用內嵌版本、不套用覆寫），`--` 之後只放保留入口 `@shell-check` 或 `@shell-repair`。
# 引擎來源三種：鎖定行（本機沒有才 pull）、`-i <path>.tar`（.digest 旁檔要符合鎖定行）、`-i <ref>`（本機 image，
# digest 要符合鎖定行、完整引用也要相同）。
# docker 是假的（fixture/fake_docker.bash）：`start -ai` 當引擎，照 $fake/engine 跑。比對與修復的本體在引擎
# （engine/shell_check，e2e 在 test/e2e/tests/shell_check.rs）；這裡驗啟動器那一側：起對引擎、不碰薄殼。

load helper

setup() {
    common_setup
    A=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    B=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
    C=cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
    D=dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
    L=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    name=ghcr.io/acme/vendor_kit
    embedded="$name:v1.0.0@sha256:$A"
    # 鎖定行跟內嵌引用的 tag 與 digest 都不同：用到哪一個一看就知道。
    lock="$name:v1.2.0@sha256:$D"
    fake="$BATS_TEST_TMPDIR/fake"
    tmpd="$BATS_TEST_TMPDIR/tmp"
    offline="$BATS_TEST_TMPDIR/offline"
    mkdir -p "$fake" "$tmpd" "$offline" "$work/.git" "$work/.vendor_kit"
    fake_cmd docker "source '$BATS_TEST_DIRNAME/fixture/fake_docker.bash'"
    # 只檢查與 --repair 不查 just：放一個太舊的 just，查了就會停。
    fake_version just 'just 1.0.0'
    printf '1 1' >"$fake/labels"
    # 鎖定行只有引擎那一行，沒有介面版列表：走一般路徑的介面版判定就會停（保留入口屬救援路徑，不判）。
    printf 'vendor_kit = "%s"\nschema = 1\n' "$lock" >"$work/.vendor_kit/version.toml"
    # 本機覆寫不套用（04 用哪一版引擎）。
    printf 'vendor_kit = "%s:v9.9.9@sha256:%s"\n' "$name" "$C" >"$work/.vendor_kit/version.local.toml"
    # 引擎：記下 in/engine 與起引擎時紀錄在不在，以 0 結束。
    printf '%s\n' \
        'cp "${engine_ctl%/ctl}/in/engine" "$fake/in_engine"' \
        'logs=("$fake"/../work/.vendor_kit/log/*-bootstrap-r1.jsonl); [[ -f ${logs[0]} ]] && : >"$fake/log_seen"' \
        'finish 0' >"$fake/engine"
    vk_env=(VK_FAKE="$fake" TMPDIR="$tmpd")
    log_dir="$work/.vendor_kit/log"
}

# bsc <args>...：在 $work 跑 vk_bootstrap_main（不換替身），內嵌引擎是 $embedded、介面版 1、invocation id r1。
bsc() {
    local q='' a x
    for a in "$@"; do
        printf -v x ' %q' "$a"
        q+=$x
    done
    printf -v x '%q' "$embedded"
    vk "vk_bootstrap_engine=$x; vk_bootstrap_proto=1; vk_log_invocation_id=r1; vk_bootstrap_main$q; exit \$?"
}

log_file() {
    local -a files=("$log_dir"/*-bootstrap-r1.jsonl)
    [ "${#files[@]}" -eq 1 ] && [ -f "${files[0]}" ]
    REPLY=${files[0]}
}

# 引擎容器用的 image（docker create 的參數裡 --protocol 前一個）與 `--` 之後的參數。
created() {
    mapfile -t argv <"$fake/engine.argv"
    local i
    created_image=
    created_args=()
    for ((i = 0; i < ${#argv[@]}; i++)); do
        if [[ ${argv[i]} == --protocol && -z $created_image ]]; then
            created_image=${argv[i - 1]}
            [ "${argv[i + 1]}" = 1 ]
        fi
        if [[ ${argv[i]} == -- ]]; then
            created_args=("${argv[@]:i+1}")
            break
        fi
    done
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

# assert_ran <mode> <image> <保留入口>：起了鎖定行那一版引擎、起之前紀錄已建好、紀錄完整、session 目錄已刪。
assert_ran() {
    local mode=$1 image=$2 entry=$3
    [ "$status" -eq 0 ]
    [ "$stderr" = "" ]
    [ "$(<"$fake/in_engine")" = "$lock" ]
    [ -e "$fake/log_seen" ]
    created
    [ "$created_image" = "$image" ]
    [ "${#created_args[@]}" -eq 1 ]
    [ "${created_args[0]}" = "$entry" ]
    log_file
    local -a lines
    mapfile -t lines <"$REPLY"
    [ "${#lines[@]}" -eq 2 ]
    [[ ${lines[0]} == *'"event_name":"run_started"'*'"service.version":"v1.2.0"'*"\"vendor_kit.mode\":\"$mode\""* ]]
    [[ ${lines[1]} == *'"vendor_kit.exit_code":0,"vendor_kit.engine.exit_code":0,"vendor_kit.stop_reason_code":"none"'* ]]
    [ ! -e "$tmpd/vendor_kit.r1" ]
    assert_git_not_called
}

# assert_failed <mode> <code> <stderr>：沒起引擎；紀錄有那條診斷與 run_finished。之後清掉紀錄與呼叫記錄。
assert_failed() {
    [ "$status" -eq 2 ]
    [ "$output" = "" ]
    [ "$stderr" = "$3" ]
    [ ! -e "$fake/engine.argv" ]
    log_file
    local -a lines
    mapfile -t lines <"$REPLY"
    [ "${#lines[@]}" -eq 3 ]
    [[ ${lines[0]} == *'"service.version":"v1.2.0"'*"\"vendor_kit.mode\":\"$1\""* ]]
    [[ ${lines[1]} == *'"event_name":"diagnostic_emitted"'*"\"vendor_kit.reason_code\":\"$2\""* ]]
    [[ ${lines[2]} == *"\"vendor_kit.exit_code\":2,\"vendor_kit.engine.exit_code\":null,\"vendor_kit.stop_reason_code\":\"$2\""* ]]
    rm -rf "$log_dir"
    rm -f "$fake/calls"
}

no_digest() {
    REPLY="vendor_kit: error[VK0031]: Cannot use image $1: required digest information is missing. The supplied image was not used."
}

bad_digest() {
    REPLY="vendor_kit: error[VK0031]: Cannot use image $1: the digest does not match the engine lock version line. The supplied image was not used."
}

not_exact() {
    REPLY="vendor_kit: error[VK0038]: Image $1 does not exactly match the engine lock version line $lock. The supplied image was not used."
}

not_obtained() {
    REPLY="vendor_kit: error[VK0036]: Cannot obtain engine image $1: $2. No alternative engine version was used."
}

# ---- 鎖定行那一版引擎 ----

@test "check runs the locked engine with @shell-check after the run log, not the embedded one or the override" {
    bsc
    assert_ran check "$lock" @shell-check
    assert_not_called '^pull'
    assert_not_called "$embedded"
    assert_not_called 'v9\.9\.9'
    log_file
    [[ $(head -n 1 "$REPLY") == *'"vendor_kit.argv":[]}}' ]]
}

@test "--repair runs the locked engine with @shell-repair, and the run log keeps the arguments as is" {
    bsc --repair
    assert_ran repair "$lock" @shell-repair
    log_file
    [[ $(head -n 1 "$REPLY") == *'"vendor_kit.argv":["--repair"]}}' ]]
}

@test "the engine exit code is the exit code of bootstrap.sh" {
    printf '%s\n' 'finish 2' >"$fake/engine"
    bsc
    [ "$status" -eq 2 ]
    log_file
    [[ $(tail -n 1 "$REPLY") == *'"vendor_kit.exit_code":2,"vendor_kit.engine.exit_code":2,"vendor_kit.stop_reason_code":"none"'* ]]
}

@test "a missing locked engine is pulled; a failed pull is VK0036 after the run log" {
    rm "$fake/labels"
    printf '1 1' >"$fake/labels_after_pull"
    bsc --repair
    assert_ran repair "$lock" @shell-repair
    assert_called "pull -q $lock"
    rm -rf "$log_dir" "$fake/labels" "$fake/labels_after_pull" "$fake/engine.argv" "$fake/calls"
    printf '1' >"$fake/rc.pull"
    bsc
    not_obtained "$lock" 'docker pull exited with 1'
    assert_failed check VK0036 "$REPLY"
}

# ---- -i <path>.tar ----

@test "-i <tar> whose .digest matches the lock line loads the tar and starts the loaded image ID" {
    : >"$offline/engine.tar"
    printf 'sha256:%s\n' "$D" >"$offline/engine.digest"
    bsc -i "$offline/engine.tar"
    assert_ran check "sha256:$L" @shell-check
    assert_called "load -q -i $offline/engine.tar"
    assert_not_called '^pull'
}

@test "-i <tar> without a valid .digest, or with another digest, is VK0031 and loads nothing" {
    : >"$offline/engine.tar"
    no_digest "$offline/engine.tar"
    local want=$REPLY
    bsc --repair -i "$offline/engine.tar"
    assert_not_called '^load'
    assert_failed repair VK0031 "$want"
    printf 'sha256:x\n' >"$offline/engine.digest"
    bsc -i "$offline/engine.tar"
    assert_not_called '^load'
    assert_failed check VK0031 "$want"
    bad_digest "$offline/engine.tar"
    want=$REPLY
    local d
    for d in "$A" "$B"; do
        printf 'sha256:%s\n' "$d" >"$offline/engine.digest"
        bsc --image "$offline/engine.tar"
        assert_not_called '^load'
        assert_failed check VK0031 "$want"
    done
}

@test "-i <tar> that docker cannot load is VK0036" {
    : >"$offline/engine.tar"
    printf 'sha256:%s\n' "$D" >"$offline/engine.digest"
    printf '1' >"$fake/rc.load"
    bsc --repair -i "$offline/engine.tar"
    not_obtained "$offline/engine.tar" 'docker load exited with 1'
    assert_failed repair VK0036 "$REPLY"
}

# ---- -i <ref> ----

@test "-i <ref> equal to the lock line uses the local image ID, never pulling" {
    printf '%s sha256:%s %s@sha256:%s\n' "$lock" "$C" "$name" "$D" >"$fake/local"
    bsc -i "$lock"
    assert_ran check "sha256:$C" @shell-check
    assert_not_called '^pull'
    assert_not_called '^load'
    rm -rf "$log_dir" "$fake/engine.argv"
    # 不帶 digest 的 tag 解出來的完整引用跟鎖定行相同
    printf '%s:v1.2.0 sha256:%s %s@sha256:%s\n' "$name" "$C" "$name" "$D" >"$fake/local"
    bsc --repair -i "$name:v1.2.0"
    assert_ran repair "sha256:$C" @shell-repair
}

@test "-i <ref> whose digest differs from the lock line is VK0031" {
    # ref 自帶的 digest 不符：不查本機
    bad_digest "$name:v1.2.0@sha256:$B"
    bsc -i "$name:v1.2.0@sha256:$B"
    assert_not_called '^image'
    assert_failed check VK0031 "$REPLY"
    # 本機 image 的 RepoDigest 不符
    printf '%s:v1.2.0 sha256:%s %s@sha256:%s\n' "$name" "$C" "$name" "$B" >"$fake/local"
    bad_digest "$name:v1.2.0"
    bsc --repair -i "$name:v1.2.0"
    assert_failed repair VK0031 "$REPLY"
}

@test "-i <ref> without exactly one RepoDigest of the same name is VK0031 (missing)" {
    printf '%s:v1.2.0 sha256:%s\n' "$name" "$C" >"$fake/local"
    no_digest "$name:v1.2.0"
    bsc -i "$name:v1.2.0"
    assert_failed check VK0031 "$REPLY"
}

@test "-i <ref> with the locked digest but another full reference is VK0038" {
    local r
    printf '%s@sha256:%s sha256:%s %s@sha256:%s\n' "$name" "$D" "$C" "$name" "$D" >"$fake/local"
    printf '%s:v1.0.0 sha256:%s %s@sha256:%s\n' "$name" "$C" "$name" "$D" >>"$fake/local"
    printf 'docker.io/acme/vendor_kit:v1.2.0@sha256:%s sha256:%s docker.io/acme/vendor_kit@sha256:%s\n' "$D" "$C" "$D" >>"$fake/local"
    for r in "$name@sha256:$D" "$name:v1.0.0" "docker.io/acme/vendor_kit:v1.2.0@sha256:$D"; do
        not_exact "$r"
        bsc -i "$r"
        assert_failed check VK0038 "$REPLY"
    done
    not_exact "$name:v1.0.0"
    bsc --repair -i "$name:v1.0.0"
    assert_failed repair VK0038 "$REPLY"
}

@test "-i <ref> that is not a local image is VK0036 without pulling" {
    not_obtained "$lock" 'the image is not available locally'
    bsc -i "$lock"
    assert_not_called '^pull'
    assert_failed check VK0036 "$REPLY"
}

# ---- ADR-0007 的驗收清單 ----

# shell_files：.vendor_kit/ 下的薄殼四檔。log.sh 被執行就會留下記號。
shell_files() {
    printf 'mod vendor_kit\n' >"$work/.vendor_kit/entry.just"
    printf 'default:\n' >"$work/.vendor_kit/vendor.just"
    printf 'printf ran >"%s/shell_ran"\n' "$BATS_TEST_TMPDIR" >"$work/.vendor_kit/log.sh"
    printf 'log/\n' >"$work/.vendor_kit/.gitignore"
    mkdir -p "$fake/templates"
    cp "$work/.vendor_kit/entry.just" "$work/.vendor_kit/vendor.just" "$work/.vendor_kit/log.sh" \
        "$work/.vendor_kit/.gitignore" "$fake/templates/"
    # 引擎：跟模板逐檔比對（只檢查與修復都不在一致時寫檔），不符時像 VK0006 那樣報、以 2 結束。
    cat >"$fake/engine" <<'EOF'
vk_dir="$fake/../work/.vendor_kit"
bad=
for f in entry.just vendor.just log.sh .gitignore; do
    if [[ "$(<"$vk_dir/$f")" != "$(<"$fake/templates/$f")" ]]; then
        bad+=" .vendor_kit/$f"
    fi
done
if [[ -n $bad ]]; then
    printf 'vendor_kit: error[VK0006]:%s\n' "$bad" >&2
    finish 2
fi
printf "Shell files match this engine version's templates.\n"
finish 0
EOF
}

# 安裝目錄下除了執行紀錄以外每個檔的內容與修改時間。
shell_snap() {
    (cd "$work" && find . -path ./.vendor_kit/log -prune -o -type f -print | LC_ALL=C sort | while IFS= read -r f; do
        printf '%s %s %s\n' "$f" "$(sha256sum <"$f")" "$(stat -c %Y.%y "$f")"
    done)
}

@test "check with one byte changed in a shell file exits 2 with the engine's diagnostic and touches nothing" {
    shell_files
    printf 'mod vendor_kiT\n' >"$work/.vendor_kit/entry.just"
    local before
    before=$(shell_snap)
    bsc
    [ "$status" -eq 2 ]
    [ "$output" = "" ]
    [ "$stderr" = 'vendor_kit: error[VK0006]: .vendor_kit/entry.just' ]
    [ "$(shell_snap)" = "$before" ]
    [ ! -e "$BATS_TEST_TMPDIR/shell_ran" ]
    created
    [ "${created_args[*]}" = @shell-check ]
    log_file
    [[ $(tail -n 1 "$REPLY") == *'"vendor_kit.exit_code":2,"vendor_kit.engine.exit_code":2,"vendor_kit.stop_reason_code":"none"'* ]]
}

@test "--repair with consistent shell files exits 0 and the launcher regenerates nothing" {
    shell_files
    local before
    before=$(shell_snap)
    bsc --repair
    [ "$status" -eq 0 ]
    [ "$stderr" = "" ]
    [ "$output" = "Shell files match this engine version's templates." ]
    [ "$(shell_snap)" = "$before" ]
    [ ! -e "$BATS_TEST_TMPDIR/shell_ran" ]
    created
    [ "${created_args[*]}" = @shell-repair ]
    assert_git_not_called
}
