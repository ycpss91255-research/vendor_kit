#!/usr/bin/env bats
# vk-resolve/<P> 文法的啟動器端（wire.sh）：與 engine/plan 同一份規則。
# 期待的位元組與拒絕清單照 engine/plan/src/tests.rs 的同名測試逐條抄過來（P=1、run-id r1）。

load helper

setup() {
    common_setup
    A=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    B=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    pinned="ghcr.io/acme/ros_tools@sha256:$A"
}

# put <檔名> <內容（printf %b）>：在 $work 寫一個控制檔。
put() {
    printf '%b' "$2" >"$work/$1"
}

# vk 片段的結束碼是 vk_diag_exit，要看函式的結束碼就自己 `|| exit 1`。
# 解析 req 後印出 op 名與每個運算元（%q），一行一個。
show_req='vk_wire_parse_req "$PWD/req" 1 r1 3 || { printf "rejected: %s\n" "$REPLY"; exit 1; }; printf "%s\n" "$vk_req_op"; for a in "${vk_req_args[@]}"; do printf "%q\n" "$a"; done'

@test "rust golden strings are still in engine/plan/src/tests.rs" {
    local src
    src=$(<"$repo_root/engine/plan/src/tests.rs")
    [[ $src == *'"vk-resolve/1 r1 3\nload e:/srv/u/my\\040proj/my\\040tools.tar\n"'* ]]
    [[ $src == *'"vk-resolve/1 r1 3\nstage e:/srv/u/.ghcr\\040token t1\n"'* ]]
    [[ $src == *'"vk-resolve/1 r1 3\nrunner ghcr.io/u/test:1 e:pytest e:-q e: e:tests/a\\134b.py\n"'* ]]
    [[ $src == *'(Outcome::Runner(RunnerOutcome::Stopped(None)),'*'"runner stopped unavailable"'* ]] ||
        [[ $src == *'"runner stopped unavailable"'* ]]
    [[ $src == *'["/vk/root", "/vk/ctl", "/vk/in"]'* ]]
    [[ $src == *'["req.", "res.", ".out", "done", ".tmp"]'* ]]
}

@test "every op in the rust golden parses to its operands" {
    local -a cases=(
        "pull $pinned" "pull\n$pinned"
        'load e:/srv/u/my\\040proj/my\\040tools.tar' "load\n/srv/u/my\\\\ proj/my\\\\ tools.tar"
        "inspect $pinned" "inspect\n$pinned"
        "extract sha256:$B x1" "extract\nsha256:$B\nx1"
        'stage e:/srv/u/.ghcr\\040token t1' "stage\n/srv/u/.ghcr\\\\ token\nt1"
        'stage-dir e:/srv/u/my\\040src d1' "stage-dir\n/srv/u/my\\\\ src\nd1"
        "ps" "ps"
        "rm-container $B" "rm-container\n$B"
        'runner ghcr.io/u/test:1 e:pytest e:-q e: e:tests/a\\134b.py' "runner\nghcr.io/u/test:1\npytest\n-q\n''\ntests/a\\\\\\\\b.py"
    )
    local i want
    for ((i = 0; i < ${#cases[@]}; i += 2)); do
        put req "vk-resolve/1 r1 3\n${cases[i]}\n"
        vk "$show_req"
        printf -v want '%b' "${cases[i + 1]}"
        [ "$status" -eq 0 ] || {
            echo "${cases[i]}: $output" >&2
            return 1
        }
        [ "$output" = "$want" ] || {
            echo "${cases[i]}: got $output want $want" >&2
            return 1
        }
    done
}

@test "op names are the closed set of engine/plan" {
    vk 'printf "%s\n" "${vk_wire_ops[*]}" "${vk_wire_argv[*]}" "$vk_wire_mount_root $vk_wire_mount_ctl $vk_wire_mount_in" "$vk_wire_in_engine" "$vk_wire_in_bootstrap" "${vk_wire_since_v2[*]}"'
    [ "${lines[0]}" = "pull load inspect extract stage stage-dir ps rm-container runner pull-tag rm-sessions" ]
    [ "${lines[1]}" = "--protocol --run-id --host-root --host-cwd --run-log --tty --no-color" ]
    [ "${lines[2]}" = "/vk/root /vk/ctl /vk/in" ]
    # 救援協定的一部分，跟引擎端讀的檔名一致
    [ "${lines[3]}" = engine ]
    # bootstrap.sh 首次導入的來源檔（B2）與介面版 2 起才收的 op
    [ "${lines[4]}" = bootstrap ]
    [ "${lines[5]}" = "pull-tag rm-sessions" ]
}

@test "the launcher ops equal the OPS of engine/plan in order, or add only the pending version-2 ops" {
    # 兩邊各自寫一份；這裡從 engine/plan/src/lib.rs 讀 OPS，逐項依序比對。
    # 啟動器先 merge、引擎後加 op（#724 先、#723 後；前例 stage-dir）時，兩邊有一段時間不相等：
    # 這時啟動器的清單只准是 engine/plan 的 OPS 後面接上還沒落地的 pull-tag rm-sessions。
    local src re='pub const OPS: \[&str; [0-9]+\] = \[([^]]*)\]'
    src=$(<"$repo_root/engine/plan/src/lib.rs")
    [[ $src =~ $re ]]
    local -a engine_ops
    read -r -a engine_ops <<<"$(printf '%s' "${BASH_REMATCH[1]}" | tr '\n,"' '   ')"
    [ "${#engine_ops[@]}" -gt 0 ]
    vk 'printf "%s\n" "${vk_wire_ops[@]}"'
    [ "$status" -eq 0 ]
    [ "${lines[*]}" = "${engine_ops[*]}" ] || [ "${lines[*]}" = "${engine_ops[*]} pull-tag rm-sessions" ] || {
        echo "launcher ops: ${lines[*]}; engine/plan OPS: ${engine_ops[*]}" >&2
        return 1
    }
}

@test "interface version 2 adds pull-tag, rm-sessions and a free-text runner image" {
    local -a cases=(
        'pull-tag ghcr.io/acme/ros_tools:v1.2.0' "pull-tag\nghcr.io/acme/ros_tools:v1.2.0"
        'pull-tag localhost:5000/acme/ros_tools:v1.2.0' "pull-tag\nlocalhost:5000/acme/ros_tools:v1.2.0"
        'rm-sessions' 'rm-sessions'
        'runner e:ghcr.io/u/test:Nightly_1 e:pytest e:-q' "runner\nghcr.io/u/test:Nightly_1\npytest\n-q"
        'runner e:sha256:0123 e:pytest' "runner\nsha256:0123\npytest"
    )
    local i want
    for ((i = 0; i < ${#cases[@]}; i += 2)); do
        put req "vk-resolve/2 r1 3\n${cases[i]}\n"
        vk 'vk_wire_parse_req "$PWD/req" 2 r1 3 || { printf "rejected: %s\n" "$REPLY"; exit 1; }; printf "%s\n" "$vk_req_op"; for a in "${vk_req_args[@]}"; do printf "%q\n" "$a"; done'
        printf -v want '%b' "${cases[i + 1]}"
        [ "$status" -eq 0 ] || {
            echo "${cases[i]}: $output" >&2
            return 1
        }
        [ "$output" = "$want" ] || {
            echo "${cases[i]}: got $output want $want" >&2
            return 1
        }
    done
    local -a bad=(
        "pull-tag $pinned"
        'pull-tag ghcr.io/acme/ros_tools'
        'pull-tag ghcr.io/acme/ros_tools:'
        'pull-tag localhost:5000/acme/ros_tools'
        'pull-tag ghcr.io/acme/ros_tools:V1.2.0'
        'pull-tag ghcr.io/acme/ros_tools:.v1'
        'pull-tag ghcr.io/acme/ros_tools:v1.2.0 x'
        'pull-tag'
        'rm-sessions r1'
        'runner ghcr.io/u/test:1 e:pytest'
        'runner e: e:pytest'
        'runner e:--privileged e:pytest'
        'runner e:ghcr.io/u/test:1'
    )
    for i in "${!bad[@]}"; do
        put "bad.$i" "vk-resolve/2 r1 1\n${bad[i]}\n"
    done
    vk 'for f in bad.*; do if vk_wire_parse_req "$PWD/$f" 2 r1 1; then echo "accepted $(<"$f")"; fi; done'
    [ "$status" -eq 0 ]
    [ "$output" = "" ]
}

@test "the version-2 ops and the free-text runner image are not accepted at interface version 1" {
    local req
    # e:ghcr.io/u/test:1 這種字串本身也合 ref，所以 P = 1 用 ref 收不下的大寫 tag 驗。
    for req in 'pull-tag ghcr.io/acme/ros_tools:v1.2.0' 'rm-sessions' 'runner e:ghcr.io/u/test:Nightly e:pytest'; do
        put req "vk-resolve/1 r1 1\n$req\n"
        vk 'vk_wire_parse_req "$PWD/req" 1 r1 1 && echo accepted; true'
        [ "$output" = "" ] || {
            echo "$req: $output" >&2
            return 1
        }
    done
    # P = 1 的 runner 照舊收 ref
    put req 'vk-resolve/1 r1 1\nrunner ghcr.io/u/test:1 e:pytest\n'
    vk 'vk_wire_parse_req "$PWD/req" 1 r1 1 || exit 1; printf "%s\n" "${vk_req_args[@]}"'
    [ "$status" -eq 0 ]
    [ "${lines[0]}" = ghcr.io/u/test:1 ]
}

@test "the free-text encoder writes the one byte form that the decoder reads back" {
    local -a cases=(
        '' 'e:'
        'abc' 'e:abc'
        'a\b' 'e:a\134b'
        'a b' 'e:a\040b'
        $'\t\n' 'e:\011\012'
        $'\001\177\377' 'e:\001\177\377'
        'e:' 'e:e:'
        './bootstrap.sh' 'e:./bootstrap.sh'
    )
    local i
    for ((i = 0; i < ${#cases[@]}; i += 2)); do
        vk "vk_wire_encode $(printf '%q' "${cases[i]}") && printf '%s' \"\$REPLY\""
        [ "$status" -eq 0 ]
        [ "$output" = "${cases[i + 1]}" ] || {
            echo "${cases[i]}: got $output" >&2
            return 1
        }
    done
    # 每個非 NUL 位元組編了再解，回到原值
    vk 'for ((b = 1; b < 256; b++)); do printf -v w "%b" "\\0$(printf %03o "$b")"; vk_wire_encode "x${w}y"; e=$REPLY; vk_wire_field "$e" || echo "rejected $e"; [[ $REPLY == "x${w}y" ]] || echo "wrong $b"; done'
    [ "$status" -eq 0 ]
    [ "$output" = "" ]
}

@test "free-text fields decode exactly like field_encoding_is_exact" {
    # 編碼 → 解碼後的值（%q）
    local -a cases=(
        'e:' "''"
        'e:abc' 'abc'
        'e:a\134b' 'a\\b'
        'e:\134' '\\'
        'e:a\040b' 'a\ b'
        'e:\011\012\015' "\$'\\t\\n\\r'"
        'e:\001\177\377' "\$'\\001\\177\\377'"
        'e:e:' 'e:'
        'e:\101' 'A'
    )
    local i
    for ((i = 0; i < ${#cases[@]}; i += 2)); do
        vk "vk_wire_field '${cases[i]}' && printf '%q' \"\$REPLY\""
        [ "$status" -eq 0 ]
        [ "$output" = "${cases[i + 1]}" ] || {
            echo "${cases[i]}: got $output" >&2
            return 1
        }
    done
    # 每個非可見或反斜線的位元組都只收三位八進位
    vk 'for ((b = 1; b < 256; b++)); do printf -v o "e:\\%03o" "$b"; vk_wire_field "$o" || echo "rejected $o"; printf -v w "%b" "\\0$(printf %03o "$b")"; [[ $REPLY == "$w" ]] || echo "wrong $o"; done'
    [ "$status" -eq 0 ]
    [ "$output" = "" ]
}

@test "free-text fields reject what field_rejects_nul_and_bad_syntax rejects" {
    local bad
    for bad in '' 'abc' 'E:abc' 'e:a\b' 'e:\' 'e:\12' 'e:\000' 'e:\400' 'e:\777' 'e:\08a' 'e:a b' $'e:\t' $'e:\x7f' 'e:é'; do
        vk "vk_wire_field $(printf '%q' "$bad") || exit 1"
        [ "$status" -ne 0 ] || {
            echo "accepted $bad" >&2
            return 1
        }
    done
}

@test "requests are rejected like request_rejects_malformed_bytes" {
    local pull="pull $pinned"
    local -a bad=(
        ''
        "vk-resolve/1 r1 1\n$pull"
        "vk-resolve/1 r1 1\r\n$pull\r\n"
        "vk-resolve/1 r1 1\n$pull\n\n"
        "vk-resolve/1 r1 1\n\n"
        "vk-resolve/1 r1 1\n$pull\nps\n"
        "vk-resolve/1 r1 1\n $pull\n"
        "vk-resolve/1 r1 1\n$pull \n"
        "vk-resolve/1  r1 1\n$pull\n"
        "vk-resolve/1 r1 1\npull\t$pinned\n"
        "vk-resolve/1 r1 1\n$pull\0\n"
        "vk-resolve/2 r1 1\n$pull\n"
        "vk-resolve/01 r1 1\n$pull\n"
        "VK-RESOLVE/1 r1 1\n$pull\n"
        "vk-resolve/1 r2 1\n$pull\n"
        "vk-resolve/1 r1\n$pull\n"
        "vk-resolve/1 r1 0\n$pull\n"
        "vk-resolve/1 r1 01\n$pull\n"
        "vk-resolve/1 r1 10000\n$pull\n"
        "vk-resolve/1 r1 1 2\n$pull\n"
        "vk-resolve/1 r1 done 0\n$pull\n"
        "vk-resolve/1 r1 1\nrm-image x\n"
        "vk-resolve/1 r1 1\nPS\n"
        "vk-resolve/1 r1 1\nps x\n"
        "vk-resolve/1 r1 1\npull ghcr.io/acme/ros_tools:v1.2.0\n"
        "vk-resolve/1 r1 1\npull ghcr.io/a@b@sha256:$A\n"
        "vk-resolve/1 r1 1\npull ghcr.io/acme/ros_tools@sha256:${A:1}\n"
        "vk-resolve/1 r1 1\npull ghcr.io/acme/ros_tools@sha256:${A^^}\n"
        "vk-resolve/1 r1 1\npull GHCR.io/acme/ros_tools@sha256:$A\n"
        "vk-resolve/1 r1 1\npull $pinned $pinned\n"
        "vk-resolve/1 r1 1\nextract ghcr.io/acme/ros_tools:v1.2.0 x1\n"
        "vk-resolve/1 r1 1\nextract $pinned x1\n"
        "vk-resolve/1 r1 1\nextract $B x1\n"
        "vk-resolve/1 r1 1\nextract sha256:${B^^} x1\n"
        "vk-resolve/1 r1 1\nextract sha256:$B\n"
        "vk-resolve/1 r1 1\nextract sha256:$B X1\n"
        "vk-resolve/1 r1 1\nextract sha256:$B abcdefghijklmnopq\n"
        'vk-resolve/1 r1 1\nload e:my\\040tools.tar\n'
        'vk-resolve/1 r1 1\nload e:\n'
        'vk-resolve/1 r1 1\nload /srv/u/a.tar\n'
        'vk-resolve/1 r1 1\nstage e:token t1\n'
        'vk-resolve/1 r1 1\nstage-dir e:src d1\n'
        'vk-resolve/1 r1 1\nstage-dir e:\n'
        'vk-resolve/1 r1 1\nstage-dir /srv/u/src d1\n'
        'vk-resolve/1 r1 1\nstage-dir e:/srv/u/src\n'
        'vk-resolve/1 r1 1\nstage-dir e:/srv/u/src D1\n'
        'vk-resolve/1 r1 1\nstage-dir e:/srv/u/src d1 d2\n'
        'vk-resolve/1 r1 1\nstage_dir e:/srv/u/src d1\n'
        "vk-resolve/1 r1 1\nrm-container ${B:0:12}\n"
        'vk-resolve/1 r1 1\nrunner ghcr.io/u/test:1\n'
        'vk-resolve/1 r1 1\nrunner ghcr.io/u/test:1 pytest\n'
    )
    local i
    for i in "${!bad[@]}"; do
        put "bad.$i" "${bad[i]}"
    done
    # 拒絕清單之外：一份合格的 req 要收（確認上面不是因為別的原因被拒）。
    put good "vk-resolve/1 r1 1\n$pull\n"
    vk 'vk_wire_parse_req "$PWD/good" 1 r1 1 || echo "good rejected: $REPLY"; for f in bad.*; do if vk_wire_parse_req "$PWD/$f" 1 r1 1; then echo "accepted $f"; fi; done'
    [ "$status" -eq 0 ]
    [ "$output" = "" ]
}

@test "a NUL byte is reported before anything else" {
    put req "vk-resolve/1 r1 1\nps\0\n"
    vk 'vk_wire_parse_req "$PWD/req" 1 r1 1; echo "$?:$REPLY"'
    [ "$output" = "1:control file req has a NUL byte" ]
}

@test "result lines are exact and only fit their op" {
    local line
    for line in ok 'failed 1' 'failed 0' 'failed 255'; do
        vk "vk_wire_result_ok pull '$line' && vk_wire_res 1 r1 7 '$line' && printf %s \"\$REPLY\""
        [ "$status" -eq 0 ]
        [ "$output" = "vk-resolve/1 r1 7"$'\n'"$line" ]
    done
    for line in 'runner notstarted' 'runner exited 0' 'runner exited 130' 'runner stopped 137' 'runner stopped unavailable'; do
        vk "vk_wire_result_ok runner '$line' || exit 1"
        [ "$status" -eq 0 ]
    done
    for line in OK 'ok 0' failed 'failed 256' 'failed 01' 'failed -1' 'failed unavailable' 'runner exited 1'; do
        vk "vk_wire_result_ok pull '$line' || exit 1"
        [ "$status" -ne 0 ] || {
            echo "accepted $line for pull" >&2
            return 1
        }
    done
    for line in ok 'failed 125' 'runner stopped' 'runner exited unavailable' 'runner notstarted 1' 'runner'; do
        vk "vk_wire_result_ok runner '$line' || exit 1"
        [ "$status" -ne 0 ] || {
            echo "accepted $line for runner" >&2
            return 1
        }
    done
}

@test "done is parsed like done_has_exact_bytes_and_rejects_malformed" {
    local code
    for code in 0 1 2 3; do
        put done "vk-resolve/1 r1 done $code\n"
        vk 'vk_wire_parse_done "$PWD/done" 1 r1 && printf %s "$REPLY"'
        [ "$status" -eq 0 ]
        [ "$output" = "$code" ]
    done
    local -a bad=(
        'vk-resolve/1 r1 done 4\n' 'vk-resolve/1 r1 done 00\n' 'vk-resolve/1 r1 done\n' 'vk-resolve/1 r1 done 0'
        'vk-resolve/1 r1 done 0\n\n' 'vk-resolve/1 r1 1 0\n' 'vk-resolve/1 r2 done 0\n'
    )
    local b
    for b in "${bad[@]}"; do
        put done "$b"
        vk 'vk_wire_parse_done "$PWD/done" 1 r1 || exit 1'
        [ "$status" -ne 0 ] || {
            echo "accepted $b" >&2
            return 1
        }
    done
}

@test "mount fields use the docker CSV quoting" {
    vk 'vk_wire_mount_source "/srv/a,b \"c\"/d" && printf "%s\n" "$REPLY"; vk_wire_mount_target "/vk/repo/x y" && printf "%s\n" "$REPLY"'
    [ "${lines[0]}" = '"source=/srv/a,b ""c""/d"' ]
    [ "${lines[1]}" = '"target=/vk/repo/x y"' ]
}
