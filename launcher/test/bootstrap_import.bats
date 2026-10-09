#!/usr/bin/env bats
# bootstrap.sh 的首次導入（bootstrap_main.sh 的 vk_bootstrap_import；04 bootstrap.sh 判定 4、離線導入）：
# 先建 .vendor_kit/log/ 與這次的紀錄（mode initial_import），再取得引擎，以 `install [-y]` 起引擎。
# 引擎來源三種：內嵌引用（本機沒有才 pull）、`-i <path>.tar`（同名 .digest 旁檔加 docker load）、
# `-i <ref>`（本機 image 的 RepoDigest，不 pull）。
# docker 是假的（fixture/fake_docker.bash）：`start -ai` 當引擎，照 $fake/engine 跑。

load helper

setup() {
    common_setup
    A=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    B=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
    C=cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
    L=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    name=ghcr.io/acme/vendor_kit
    embedded="$name:v1.0.0@sha256:$A"
    fake="$BATS_TEST_TMPDIR/fake"
    tmpd="$BATS_TEST_TMPDIR/tmp"
    offline="$BATS_TEST_TMPDIR/offline"
    mkdir -p "$fake" "$tmpd" "$offline" "$work/.git"
    fake_cmd docker "source '$BATS_TEST_DIRNAME/fixture/fake_docker.bash'"
    fake_version just 'just 1.33.0'
    printf '1 1' >"$fake/labels"
    # 引擎：記下 in/engine，以 0 結束。
    printf '%s\n' 'cp "${engine_ctl%/ctl}/in/engine" "$fake/in_engine"; finish 0' >"$fake/engine"
    vk_env=(VK_FAKE="$fake" TMPDIR="$tmpd")
    log_dir="$work/.vendor_kit/log"
}

# bsi <args>...：在 $work 跑 vk_bootstrap_main（不換替身），內嵌引擎是 $embedded、介面版 1、invocation id r1。
bsi() {
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

# assert_imported <in/engine> <image> <install 的參數>...：起了引擎、紀錄完整、session 目錄已刪。
assert_imported() {
    local ref=$1 image=$2
    shift 2
    [ "$status" -eq 0 ]
    [ "$stderr" = "" ]
    [ "$(<"$fake/in_engine")" = "$ref" ]
    created
    [ "$created_image" = "$image" ]
    [ "${created_args[*]}" = "$*" ]
    log_file
    local -a lines
    mapfile -t lines <"$REPLY"
    [ "${#lines[@]}" -eq 2 ]
    [[ ${lines[0]} == *'"event_name":"run_started"'*'"service.version":"v1.0.0"'*'"vendor_kit.mode":"initial_import"'* ]]
    [[ ${lines[1]} == *'"vendor_kit.exit_code":0,"vendor_kit.engine.exit_code":0,"vendor_kit.stop_reason_code":"none"'* ]]
    [ ! -e "$tmpd/vendor_kit.r1" ]
    assert_git_not_called
}

# assert_failed <code> <stderr>：沒起引擎；紀錄有那條診斷與 run_finished，而且算未完成的首次導入（可帶 -y 重跑）。
assert_failed() {
    [ "$status" -eq 2 ]
    [ "$output" = "" ]
    [ "$stderr" = "$2" ]
    [ ! -e "$fake/engine.argv" ]
    log_file
    local file=$REPLY
    local -a lines
    mapfile -t lines <"$file"
    [ "${#lines[@]}" -eq 3 ]
    [[ ${lines[1]} == *'"event_name":"diagnostic_emitted"'*"\"vendor_kit.reason_code\":\"$1\""* ]]
    [[ ${lines[2]} == *"\"vendor_kit.exit_code\":2,\"vendor_kit.engine.exit_code\":null,\"vendor_kit.stop_reason_code\":\"$1\""* ]]
    vk "vk_bootstrap_incomplete '$log_dir'; exit \$?"
    [ "$status" -eq 0 ]
    rm -rf "$work/.vendor_kit"
    rm -f "$fake/calls"
}

no_digest() {
    REPLY="vendor_kit: error[VK0031]: Cannot use image $1: required digest information is missing. The supplied image was not used."
}

not_obtained() {
    REPLY="vendor_kit: error[VK0036]: Cannot obtain engine image $1: $2. No alternative engine version was used."
}

# ---- 內嵌引用 ----

@test "without -i the embedded engine runs install, after the run log is created" {
    bsi
    assert_imported "$embedded" "$embedded" install
    assert_not_called '^pull'
    log_file
    [[ $(head -n 1 "$REPLY") == *'"vendor_kit.argv":[]}}' ]]
}

@test "-y and --yes are passed to install as -y and kept as is in the run log" {
    bsi -y
    assert_imported "$embedded" "$embedded" install -y
    log_file
    [[ $(head -n 1 "$REPLY") == *'"vendor_kit.argv":["-y"]}}' ]]
    rm -rf "$work/.vendor_kit"
    bsi --yes
    assert_imported "$embedded" "$embedded" install -y
    log_file
    [[ $(head -n 1 "$REPLY") == *'"vendor_kit.argv":["--yes"]}}' ]]
}

@test "the bootstrap source (\$0 and every original argument) is written to in/bootstrap for VK0002" {
    # 入口 argv 凍結（救援），所以 bootstrap.sh 怎麼被叫的經 in/bootstrap 交給引擎（B2）：一行、每個字一個自由文字欄。
    printf '%s\n' 'cp "${engine_ctl%/ctl}/in/bootstrap" "$fake/in_bootstrap"; finish 0' >"$fake/engine"
    bsi --yes
    [ "$status" -eq 0 ]
    local line
    line=$(<"$fake/in_bootstrap")
    local -a words
    read -r -a words <<<"$line"
    [ "${#words[@]}" -eq 2 ]
    [[ ${words[0]} == e:?* ]]
    [ "${words[1]}" = e:--yes ]
    # 位元組跟 wire.sh 的 vk_wire_encode 一致，解得回來：第一個字是 bash 的 $0
    vk "vk_wire_field '${words[0]}' && printf '%s' \"\$REPLY\""
    [ "$output" = "$BASH" ]
    [ "$(tail -c 1 "$fake/in_bootstrap" | od -An -c | tr -d ' ')" = '\n' ]
}

@test "the engine exit code is the exit code of bootstrap.sh" {
    printf '%s\n' 'finish 1' >"$fake/engine"
    bsi
    [ "$status" -eq 1 ]
    log_file
    [[ $(tail -n 1 "$REPLY") == *'"vendor_kit.exit_code":1,"vendor_kit.engine.exit_code":1,"vendor_kit.stop_reason_code":"none"'* ]]
}

@test "a missing embedded engine is pulled; a failed pull is VK0036 and leaves an incomplete initial import" {
    rm "$fake/labels"
    printf '1 1' >"$fake/labels_after_pull"
    bsi
    assert_imported "$embedded" "$embedded" install
    assert_called "pull -q $embedded"
    rm -rf "$work/.vendor_kit" "$fake/labels" "$fake/labels_after_pull" "$fake/engine.argv"
    printf '1' >"$fake/rc.pull"
    bsi
    not_obtained "$embedded" 'docker pull exited with 1'
    assert_failed VK0036 "$REPLY"
}

# ---- -i <path>.tar ----

@test "-i <tar> reads the .digest sidecar, loads the tar and starts the loaded image ID" {
    : >"$offline/engine.tar"
    printf 'sha256:%s\n' "$B" >"$offline/engine.digest"
    bsi -i "$offline/engine.tar" -y
    assert_imported "$name:v1.0.0@sha256:$B" "sha256:$L" install -y
    assert_called "load -q -i $offline/engine.tar"
    assert_not_called '^pull'
}

@test "-i <tar> with a tagged load output inspects that tag for the image ID" {
    : >"$offline/engine.tar"
    printf 'sha256:%s\r\n' "$B" >"$offline/engine.digest"
    printf 'Loaded image: %s:v1.0.0' "$name" >"$fake/load_out"
    printf '%s:v1.0.0 sha256:%s\n' "$name" "$C" >"$fake/tags"
    bsi --image "$offline/engine.tar"
    assert_imported "$name:v1.0.0@sha256:$B" "sha256:$C" install
}

@test "-i <tar> without a valid .digest sidecar is VK0031 and loads nothing" {
    : >"$offline/engine.tar"
    no_digest "$offline/engine.tar"
    local want=$REPLY
    bsi -i "$offline/engine.tar"
    assert_failed VK0031 "$want"
    local c
    for c in '' 'sha256:%s\nsha256:%s\n' 'SHA256:%s\n' 'sha256:%sa\n' ' sha256:%s\n' 'sha256:x\n' 'sha256:%s\n\n'; do
        # shellcheck disable=SC2059
        printf "$c" "$B" "$B" >"$offline/engine.digest"
        bsi -i "$offline/engine.tar"
        assert_not_called '^load'
        assert_failed VK0031 "$want"
    done
    # 名字是 tar 去掉 .tar 再加 .digest；engine.tar.digest 不算
    rm "$offline/engine.digest"
    printf 'sha256:%s\n' "$B" >"$offline/engine.tar.digest"
    bsi -i "$offline/engine.tar"
    assert_not_called '^load'
    assert_failed VK0031 "$want"
}

@test "-i <tar> that docker cannot load, or that holds not exactly one image, is VK0036" {
    : >"$offline/engine.tar"
    printf 'sha256:%s\n' "$B" >"$offline/engine.digest"
    printf '1' >"$fake/rc.load"
    bsi -i "$offline/engine.tar"
    # load 的原文摘錄跟著 VK0036 寫進紀錄（N20b），收 stderr 的暫存檔讀完就刪；這份紀錄照樣算未完成的首次導入
    log_file
    [[ $(sed -n 2p "$REPLY") == *',"vendor_kit.docker.stderr":"fake docker: load failed\n","vendor_kit.docker.stderr_truncated":0}}' ]]
    [ ! -e "$tmpd/vendor_kit.r1.load.err" ]
    not_obtained "$offline/engine.tar" 'docker load exited with 1'
    assert_failed VK0036 "$REPLY"
    rm "$fake/rc.load"
    not_obtained "$offline/engine.tar" 'docker load did not report exactly one image'
    local want=$REPLY
    local c
    for c in "Loaded image ID: sha256:$L"$'\n'"Loaded image ID: sha256:$C" '' 'Loaded image ID: sha256:x' "Loaded image: $name:v9.9.9"; do
        printf '%s' "$c" >"$fake/load_out"
        bsi -i "$offline/engine.tar"
        assert_failed VK0036 "$want"
    done
}

# ---- -i <ref> ----

@test "-i <ref> uses the local image ID and the RepoDigest of the same name, never pulling" {
    printf '%s:v1.0.0 sha256:%s docker.io/other/vendor_kit@sha256:%s %s@sha256:%s\n' "$name" "$C" "$A" "$name" "$B" >"$fake/local"
    bsi -i "$name:v1.0.0" -y
    assert_imported "$name:v1.0.0@sha256:$B" "sha256:$C" install -y
    assert_not_called '^pull'
    assert_not_called '^load'
}

@test "-i <ref> with a digest needs that digest among the RepoDigests" {
    printf '%s:v1.0.0@sha256:%s sha256:%s %s@sha256:%s\n' "$name" "$A" "$C" "$name" "$B" >"$fake/local"
    no_digest "$name:v1.0.0@sha256:$A"
    bsi -i "$name:v1.0.0@sha256:$A"
    assert_failed VK0031 "$REPLY"
    printf '%s:v1.0.0@sha256:%s sha256:%s %s@sha256:%s %s@sha256:%s\n' "$name" "$A" "$C" "$name" "$B" "$name" "$A" >"$fake/local"
    bsi -i "$name:v1.0.0@sha256:$A"
    assert_imported "$name:v1.0.0@sha256:$A" "sha256:$C" install
}

@test "-i <ref> without exactly one RepoDigest of the same name is VK0031" {
    no_digest "$name:v1.0.0"
    local want=$REPLY
    local c
    for c in "sha256:$C" "sha256:$C other/vendor_kit@sha256:$B" "sha256:$C $name@sha256:$A $name@sha256:$B"; do
        printf '%s:v1.0.0 %s\n' "$name" "$c" >"$fake/local"
        bsi -i "$name:v1.0.0"
        assert_failed VK0031 "$want"
    done
}

@test "-i <ref> that is not a local image is VK0036 without pulling" {
    bsi -i "$name:v1.0.0"
    not_obtained "$name:v1.0.0" 'the image is not available locally'
    assert_failed VK0036 "$REPLY"
    bsi -i "$name:v1.0.0"
    assert_not_called '^pull'
}

# ---- 內嵌值 ----

@test "an embedded interface version that is not valid is a VK bug, before the run log" {
    local p x
    printf -v x '%q' "$embedded"
    for p in '' 0 01 x; do
        vk "vk_bootstrap_engine=$x; vk_bootstrap_proto='$p'; vk_bootstrap_main; exit \$?"
        [ "$status" -eq 2 ]
        [ "$stderr" = 'vendor_kit: error[VK0056]: Internal vendor_kit error: the embedded interface version is not valid. This is a VK bug. Report it at https://github.com/ycpss91255-research/vendor_kit/issues and attach run log none.' ]
        [ ! -e "$work/.vendor_kit" ]
        [ ! -e "$fake/calls" ] || ! grep -qv -- '^--version' "$fake/calls"
    done
}
