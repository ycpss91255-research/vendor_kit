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
