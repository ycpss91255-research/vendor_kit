#!/usr/bin/env bats
# 執行紀錄的啟動器端寫入（ADR-0005）：與 engine/runlog 的 golden 逐位元組相同、事件子集、
# 檔名排序（加 1µs、進位）、noclobber 排他建立與 VK0010。

load helper

setup() {
    common_setup
    log_dir="$work/.vendor_kit/log"
}

# 2026-10-05T01:02:03.000004Z，與 engine/runlog/src/tests.rs 的 fixed_time 相同。
fixed='vk_now_us() { REPLY=1791162123000004; }; vk_log_version=0.0.0; vk_log_invocation_id=inv-1;'

only_log_file() {
    local -a files=("$log_dir"/*)
    [ "${#files[@]}" -eq 1 ]
    [ -f "${files[0]}" ]
    REPLY=${files[0]}
}

# ---- golden：與 engine/runlog/src/tests.rs 的同名測試逐位元組相同 ----

@test "run_started matches golden_run_started" {
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" bootstrap initial_import -y "a b" '\''q"\'\'''
    [ "$status" -eq 0 ]
    [ "$stderr" = "" ]
    only_log_file
    local file=$REPLY content
    rust_golden golden_run_started
    # 整份檔恰好是 golden 那一行加 LF
    content=$(cat "$file" && printf x)
    [ "$content" = "$REPLY"$'\n'x ]
}

@test "run_finished matches golden_run_finished and golden_run_finished_without_engine" {
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" install recipe && vk_log_finish 2 2 VK0002 && vk_log_finish 0 "" none'
    [ "$status" -eq 0 ]
    only_log_file
    local -a lines
    mapfile -t lines <"$REPLY"
    [ "${#lines[@]}" -eq 3 ]
    rust_golden golden_run_finished
    [ "${lines[1]}" = "$REPLY" ]
    rust_golden golden_run_finished_without_engine
    [ "${lines[2]}" = "$REPLY" ]
}

@test "diagnostic_emitted matches golden_diagnostic_emitted, written by the launcher" {
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" bootstrap initial_import && vk_diag VK0002 command_with_y "./bootstrap.sh -y"'
    [ "$status" -eq 2 ]
    [ "$stderr" = 'vendor_kit: error[VK0002]: Confirmation is required, but no terminal is available for interaction. No files were modified except the run log. Run from a terminal, or rerun with -y: ./bootstrap.sh -y' ]
    only_log_file
    local -a lines
    mapfile -t lines <"$REPLY"
    [ "${#lines[@]}" -eq 2 ]
    rust_golden golden_diagnostic_emitted
    local want=${REPLY/'"vendor_kit.component":"engine"'/'"vendor_kit.component":"launcher"'}
    [ "${lines[1]}" = "$want" ]
}

@test "one diagnostic is one diagnostic_emitted line with placeholders in argument order" {
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" bootstrap check && vk_diag VK0034 download_url "u" install_command "i"; vk_diag VK0033'
    [ "$status" -eq 2 ]
    only_log_file
    local -a lines
    mapfile -t lines <"$REPLY"
    [ "${#lines[@]}" -eq 3 ]
    [[ ${lines[1]} == *'"body":"just was not found on the host. Use the GitHub release.\nDownload: u\nInstall: i"'* ]]
    [[ ${lines[1]} == *'"vendor_kit.reason_code":"VK0034","vendor_kit.placeholder.download_url":"u","vendor_kit.placeholder.install_command":"i"}}' ]]
    [[ ${lines[2]} == *'"severity_text":"error","severity_number":17,"event_name":"diagnostic_emitted"'* ]]
    [[ ${lines[2]} == *'"vendor_kit.reason_code":"VK0033"}}' ]]
}

@test "fatal diagnostics are severity 21" {
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" bootstrap check && vk_diag VK0040 bootstrap_X 1 engine_X 2'
    [ "$status" -eq 3 ]
    only_log_file
    local -a lines
    mapfile -t lines <"$REPLY"
    [[ ${lines[1]} == *'"severity_text":"fatal","severity_number":21,'* ]]
}

# ---- JSON 正規形的跳脫 ----

@test "strings use the canonical escapes of engine/runlog json::escape" {
    for locale in C C.UTF-8; do
        vk "LC_ALL=$locale; "'vk_json_str "$(printf "q\"b\\\\ n\nr\rt\t\001\037\177 中文 é")"; printf "%s" "$REPLY"'
        [ "$status" -eq 0 ]
        [ "$output" = '"q\"b\\ n\nr\rt\t\u0001\u001f\u007f 中文 é"' ]
    done
    vk 'vk_json_str plain; printf "%s" "$REPLY"'
    [ "$output" = '"plain"' ]
}

# ---- 事件子集 ----

@test "the embedded event subset is a subset of engine/runlog/log-events.txt" {
    local -A registry=()
    local line
    while IFS= read -r line; do
        line=${line%%#*}
        line=${line//[[:space:]]/}
        [[ -n $line ]] && registry[$line]=1
    done <"$repo_root/engine/runlog/log-events.txt"
    vk 'printf "%s\n" "${vk_log_events[@]}"'
    [ "${#lines[@]}" -eq 3 ]
    local e
    for e in "${lines[@]}"; do
        [ -n "${registry[$e]:-}" ]
    done
}

@test "every literal event name in launcher sources is in the embedded subset" {
    vk 'printf "%s\n" "${vk_log_events[@]}"'
    local -A subset=()
    local e
    for e in "${lines[@]}"; do subset[$e]=1; done
    local file src
    for file in "$launcher_dir"/*.sh; do
        src=$(<"$file")
        while [[ $src =~ vk_log_event\ ([a-z_]+) ]]; do
            [ -n "${subset[${BASH_REMATCH[1]}]:-}" ]
            src=${src#*"${BASH_REMATCH[0]}"}
        done
    done
}

@test "an unregistered event name stops with VK0056" {
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" bootstrap check && vk_log_event file_written info 9 "x"'
    [ "$status" -eq 2 ]
    [[ $stderr == 'vendor_kit: error[VK0056]: Internal vendor_kit error: event name file_written is not in the event registry.'* ]]
    only_log_file
    local -a lines
    mapfile -t lines <"$REPLY"
    [ "${#lines[@]}" -eq 2 ]
    [[ ${lines[1]} == *'"event_name":"diagnostic_emitted"'*'"vendor_kit.reason_code":"VK0056"'* ]]
}

# ---- 檔名與排序 ----

@test "the file name is <ts>-<verb>-<id>.jsonl with a fixed-width UTC ts" {
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" install recipe'
    [ "$status" -eq 0 ]
    [ -f "$log_dir/20261005T010203.000004Z-install-inv-1.jsonl" ]
}

@test "a generated invocation id is 16 lowercase hex digits" {
    vk 'vk_log_version=0.0.0; vk_log_start "$PWD/.vendor_kit/log" install recipe && printf "%s" "$vk_log_invocation_id"'
    [ "$status" -eq 0 ]
    [[ $output =~ ^[0-9a-f]{16}$ ]]
    only_log_file
    [[ ${REPLY##*/} =~ ^[0-9]{8}T[0-9]{6}\.[0-9]{6}Z-install-${output}\.jsonl$ ]]
}

@test "a clock not after the newest name moves to that name plus 1us" {
    mkdir -p "$log_dir"
    : >"$log_dir/20261005T010203.000009Z-add-aaaa.jsonl"
    : >"$log_dir/20261005T010203.000007Z-add-bbbb.jsonl"
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" add recipe'
    [ "$status" -eq 0 ]
    [ -f "$log_dir/20261005T010203.000010Z-add-inv-1.jsonl" ]
    # 時鐘剛好等於最大檔名也要加 1µs
    rm "$log_dir/20261005T010203.000010Z-add-inv-1.jsonl" "$log_dir"/*9Z-add-aaaa.jsonl
    : >"$log_dir/20261005T010203.000004Z-add-cccc.jsonl"
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" add recipe'
    [ -f "$log_dir/20261005T010203.000007Z-add-bbbb.jsonl" ]
    [ -f "$log_dir/20261005T010203.000008Z-add-inv-1.jsonl" ]
}

@test "adding 1us carries across seconds, days and years" {
    mkdir -p "$log_dir"
    : >"$log_dir/20261231T235959.999999Z-add-aaaa.jsonl"
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" add recipe'
    [ "$status" -eq 0 ]
    [ -f "$log_dir/20270101T000000.000000Z-add-inv-1.jsonl" ]
    rm "$log_dir"/*
    : >"$log_dir/20280228T235959.999999Z-add-aaaa.jsonl"
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" add recipe'
    [ -f "$log_dir/20280229T000000.000000Z-add-inv-1.jsonl" ]
}

@test "a clock after the newest name is used as is" {
    mkdir -p "$log_dir"
    : >"$log_dir/20250101T000000.000000Z-add-aaaa.jsonl"
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" add recipe'
    [ -f "$log_dir/20261005T010203.000004Z-add-inv-1.jsonl" ]
}

@test "names not in the launcher format are ignored" {
    mkdir -p "$log_dir"
    : >"$log_dir/zzzz.jsonl"
    : >"$log_dir/99991399T000000.000000Z-add-aaaa.jsonl"
    : >"$log_dir/2099-01-01T00:00:00.000000Z-add-aaaa.jsonl"
    : >"$log_dir/20990101T000000.000000Z-Add-aaaa.jsonl"
    : >"$log_dir/20990101T000000.000000Z-add-aaaa.txt"
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" add recipe'
    [ "$status" -eq 0 ]
    [ -f "$log_dir/20261005T010203.000004Z-add-inv-1.jsonl" ]
}

@test "the timestamp round-trips through the file name format" {
    vk 'for us in 0 1791162123000004 253402300799999999 951782400000000; do
            vk_ts_name "$us"; n=$REPLY; vk_ts_name_parse "$n" || exit 1; [[ $REPLY == "$us" ]] || exit 1
            vk_ts_format "$us"; printf "%s %s\n" "$n" "$REPLY"
        done
        vk_ts_name 253402300800000000 && exit 1
        vk_ts_name -1 && exit 1
        vk_ts_name_parse 20261005T250000.000000Z && exit 1
        vk_ts_name_parse 20260230T000000.000000Z && exit 1
        exit 0'
    [ "$status" -eq 0 ]
    [ "${lines[0]}" = '19700101T000000.000000Z 1970-01-01T00:00:00.000000Z' ]
    [ "${lines[1]}" = '20261005T010203.000004Z 2026-10-05T01:02:03.000004Z' ]
    [ "${lines[2]}" = '99991231T235959.999999Z 9999-12-31T23:59:59.999999Z' ]
    [ "${lines[3]}" = '20000229T000000.000000Z 2000-02-29T00:00:00.000000Z' ]
}

# ---- 建不出紀錄：VK0010，不寫進紀錄 ----

@test "an existing file at the new name is not overwritten (noclobber) and stops with VK0010" {
    mkdir -p "$log_dir"
    printf 'keep\n' >"$log_dir/20261005T010203.000004Z-add-inv-1.jsonl"
    # 模擬兩個啟動器同時算出同一個名字：讓最大檔名查不到既有的檔。
    vk "$fixed"' vk_log_max_ts() { REPLY=-1; }; vk_log_start "$PWD/.vendor_kit/log" add recipe'
    [ "$status" -eq 2 ]
    [ "$stderr" = "vendor_kit: error[VK0010]: Cannot write run log $log_dir/20261005T010203.000004Z-add-inv-1.jsonl: the file already exists. vendor_kit does not run without a log; no files were modified. Free disk space or fix the permissions and retry." ]
    [ "$(<"$log_dir/20261005T010203.000004Z-add-inv-1.jsonl")" = keep ]
}

@test "an uncreatable log directory stops with VK0010 and writes nothing" {
    printf 'not a dir\n' >"$work/.vendor_kit"
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" add recipe'
    [ "$status" -eq 2 ]
    [ "$stderr" = "vendor_kit: error[VK0010]: Cannot write run log $log_dir: cannot create the log directory. vendor_kit does not run without a log; no files were modified. Free disk space or fix the permissions and retry." ]
    [ "$(<"$work/.vendor_kit")" = 'not a dir' ]
}

@test "VK0010 is not written to any log" {
    printf 'not a dir\n' >"$work/.vendor_kit"
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" add recipe; printf "[%s]" "$vk_log_file"'
    [ "$output" = '[]' ]
}

@test "invalid mode, verb or run_finished fields are VK bugs" {
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" add bogus'
    [ "$status" -eq 2 ]
    [[ $stderr == *'[VK0056]'*'invalid run log mode bogus'* ]]
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" Add-x recipe'
    [[ $stderr == *'[VK0056]'*'invalid run log verb Add-x'* ]]
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" add recipe && vk_log_finish 2 "" VK2'
    [[ $stderr == *'[VK0056]'*'invalid run_finished fields 2 null VK2'* ]]
}

# ---- docker 原文摘錄（N20b）：規則同 engine/diagnostics 的 DockerStderr ----

# excerpt <原文檔>：vk_log_docker_read 讀那個檔，`<旗標>|<摘錄>` 寫進 $BATS_TEST_TMPDIR/got（沒有摘錄時前面加 none）。
excerpt() {
    vk "vk_log_docker_read <'$1'; if [[ -z \$vk_log_docker_stderr ]]; then printf none >'$BATS_TEST_TMPDIR/got'; else : >'$BATS_TEST_TMPDIR/got'; fi; printf '%s|%s' \"\$vk_log_docker_truncated\" \"\$vk_log_docker_stderr\" >>'$BATS_TEST_TMPDIR/got'"
    [ "$status" -eq 0 ]
    [ "$stderr" = "" ]
}

# got_is <期待的位元組（printf 格式）>
got_is() {
    local want got
    want=$(printf "$1" && printf x)
    got=$(cat "$BATS_TEST_TMPDIR/got" && printf x)
    [ "$got" = "$want" ] || {
        echo "got ${#got} bytes: ${got:0:80}" >&2
        return 1
    }
}

@test "a docker stderr excerpt matches golden_diagnostic_emitted_docker_stderr" {
    printf 'Error: "denied"\n' >"$BATS_TEST_TMPDIR/raw"
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" bootstrap initial_import && vk_log_docker_read <'"$BATS_TEST_TMPDIR/raw"' && vk_log_diagnostic VK0024 error "No command was specified."'
    [ "$status" -eq 0 ]
    [ "$stderr" = "" ]
    only_log_file
    local -a lines
    mapfile -t lines <"$REPLY"
    [ "${#lines[@]}" -eq 2 ]
    rust_golden golden_diagnostic_emitted_docker_stderr
    [ "${lines[1]}" = "$REPLY" ]
}

@test "the excerpt keeps short stderr whole and writes nothing for empty stderr" {
    local raw=$BATS_TEST_TMPDIR/raw
    : >"$raw"
    excerpt "$raw"
    got_is 'none0|'
    printf 'line 1\nline 2\n\n' >"$raw"
    excerpt "$raw"
    got_is '0|line 1\nline 2\n\n'
    # 剛好上限不算截斷
    printf 'a%.0s' {1..4096} >"$raw"
    excerpt "$raw"
    [ "$(<"$BATS_TEST_TMPDIR/got")" = "0|$(<"$raw")" ]
}

@test "stderr over the limit keeps the tail and is flagged" {
    local raw=$BATS_TEST_TMPDIR/raw
    printf 'b%.0s' {1..4096} >"$raw"
    printf 'x' >>"$raw"
    excerpt "$raw"
    local want
    want="1|$(printf 'b%.0s' {1..4095})x"
    [ "$(<"$BATS_TEST_TMPDIR/got")" = "$want" ]
}

@test "the cut moves forward to a UTF-8 character boundary" {
    # 「中」是 3 位元組：1366 個加 end 是 4101 位元組，切點落在字元中間（同 engine 的 docker_stderr_keeps_the_tail_on_a_char_boundary）
    local raw=$BATS_TEST_TMPDIR/raw
    printf '中%.0s' {1..1366} >"$raw"
    printf 'end' >>"$raw"
    excerpt "$raw"
    got_is "1|$(printf '中%.0s' {1..1364})end"
}

@test "invalid UTF-8 becomes one U+FFFD per maximal invalid subpart" {
    local raw=$BATS_TEST_TMPDIR/raw
    printf 'bad \xff byte' >"$raw"
    excerpt "$raw"
    got_is '0|bad \xef\xbf\xbd byte'
    # 少了最後一個位元組的「中」：一個 U+FFFD
    printf '\xe4\xb8' >"$raw"
    excerpt "$raw"
    got_is '0|\xef\xbf\xbd'
    # surrogate（ED A0）、overlong（C0 AF）、超出範圍（F4 90）：開頭跟第一個接續位元組就不合，每個位元組各一個
    printf '\xed\xa0\x80|\xc0\xaf|\xf4\x90' >"$raw"
    excerpt "$raw"
    got_is '0|\xef\xbf\xbd\xef\xbf\xbd\xef\xbf\xbd|\xef\xbf\xbd\xef\xbf\xbd|\xef\xbf\xbd\xef\xbf\xbd'
    # 合法的 4 位元組字元原樣
    printf 'ok \xf0\x9f\x98\x80\xf0\x9f.' >"$raw"
    excerpt "$raw"
    got_is '0|ok \xf0\x9f\x98\x80\xef\xbf\xbd.'
}

@test "replacement is measured after conversion, so short invalid stderr can be truncated" {
    # 1366 個 0xFF 換成 4098 位元組：切點落在 U+FFFD 中間，往後挪到下一個字元
    local raw=$BATS_TEST_TMPDIR/raw
    printf '\xff%.0s' {1..1366} >"$raw"
    excerpt "$raw"
    got_is "1|$(printf '\\xef\\xbf\\xbd%.0s' {1..1365})"
}

@test "NUL is written as \\u0000 and an excerpt goes with exactly one diagnostic" {
    printf 'a\0b"\t' >"$BATS_TEST_TMPDIR/raw"
    excerpt "$BATS_TEST_TMPDIR/raw"
    got_is '0|a\xffb"\t'
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" bootstrap check && vk_log_docker_read <'"$BATS_TEST_TMPDIR/raw"' && vk_diag VK0033; vk_diag VK0033'
    [ "$status" -eq 2 ]
    [ "$stderr" = 'vendor_kit: error[VK0033]: Docker was not found on the host. Install Docker and retry.'$'\n''vendor_kit: error[VK0033]: Docker was not found on the host. Install Docker and retry.' ]
    only_log_file
    local -a lines
    mapfile -t lines <"$REPLY"
    [ "${#lines[@]}" -eq 3 ]
    [[ ${lines[1]} == *'"vendor_kit.reason_code":"VK0033","vendor_kit.docker.stderr":"a\u0000b\"\t","vendor_kit.docker.stderr_truncated":0}}' ]]
    [[ ${lines[2]} == *'"vendor_kit.reason_code":"VK0033"}}' ]]
}

@test "an excerpt read before the run log exists is dropped with the diagnostic" {
    printf 'x\n' >"$BATS_TEST_TMPDIR/raw"
    vk "$fixed"' vk_log_docker_read <'"$BATS_TEST_TMPDIR/raw"'; vk_diag VK0033; printf "[%s]" "$vk_log_docker_stderr"'
    [ "$output" = '[]' ]
}

@test "a line with the excerpt that cannot be written falls back to the same diagnostic without it" {
    printf 'x\n' >"$BATS_TEST_TMPDIR/raw"
    # 帶摘錄的那一行寫不進去（例如磁碟滿）：改寫不帶摘錄的同一筆，stderr 與結束碼不變
    vk "$fixed"' vk_log_start "$PWD/.vendor_kit/log" bootstrap check || exit 9
    vk_log_line_real=$(declare -f vk_log_event)
    eval "${vk_log_line_real/vk_log_event/vk_log_event_real}"
    vk_log_event() { [[ ${5:-} != *docker.stderr* ]] || return 1; vk_log_event_real "$@"; }
    vk_log_docker_read <'"$BATS_TEST_TMPDIR/raw"' && vk_diag VK0033'
    [ "$status" -eq 2 ]
    [ "$stderr" = 'vendor_kit: error[VK0033]: Docker was not found on the host. Install Docker and retry.' ]
    only_log_file
    local -a lines
    mapfile -t lines <"$REPLY"
    [ "${#lines[@]}" -eq 2 ]
    [[ ${lines[1]} == *'"vendor_kit.reason_code":"VK0033"}}' ]]
}
