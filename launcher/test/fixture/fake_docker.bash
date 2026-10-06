# shellcheck shell=bash
# launch.bats 的假 docker（由 shim 目錄的 docker 以 source 載入，"$@" 是 docker 的參數）。
#
# 狀態都在 $VK_FAKE 目錄：
#   calls              每次呼叫一行，參數以 %q 接起來
#   labels             引擎 image 的 LABEL 查詢輸出；不存在表示本機沒有 image
#   labels_after_pull  pull 之後才有的 LABEL 輸出
#   rc.<名>            該動作的結束碼（pull、load、cp、rm、inspect、ps、info、create-engine、create-extract、
#                      create-runner、start-runner）；不存在是 0。非 0 時跟真的 docker 一樣在 stderr 印一行原文
#                      （`fake docker: <名> failed`），用來驗啟動器有沒有把 docker 的原文攔下（N20）
#   info               docker info 的 SecurityOptions 輸出
#   ps                 docker ps 的輸出
#   containers         主機上 VK 建的容器，一行一個 `<id> <vendor_kit.root> <vendor_kit.run>`：
#                      以 `{{.Label "vendor_kit.run"}}` 為格式的 ps 照 root 的 label 篩選、印 run；rm 刪掉那一行。
#                      不存在表示沒有容器
#   engine             引擎的行為（bash，以 source 執行；可用下面的 send、raw、await、hang、interrupt、finish）
#   engine.init        引擎容器帶 --init 建立時才有：tini 會把轉來的訊號交給引擎
#   engine.ignores     有這個檔時引擎收到轉來的訊號也不停（等的 docker wait 被再次中斷），kill 才停
#   engine.pending     訊號已轉給引擎、容器還沒停時引擎之後的結束碼（docker wait 取走）
#   runner.notstarted  有這個檔時 runner 的 StartedAt 是零值
#   runner.rc          runner 的結束碼
#   got/               引擎收到的 res.<seq> 與 res.<seq>.out
#   killed、engine.running、engine.exit：引擎容器的狀態

fake=$VK_FAKE
engine_cid=eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
extract_cid=cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
runner_cid=dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd

{
    printf '%q' "$1"
    shift_args=("${@:2}")
    for a in "${shift_args[@]}"; do
        printf ' %q' "$a"
    done
    printf '\n'
} >>"$fake/calls"

rc_of() {
    local rc=0
    if [[ -f $fake/rc.$1 ]]; then
        rc=$(<"$fake/rc.$1")
    fi
    if ((rc != 0)); then
        printf 'fake docker: %s failed\n' "$1" >&2
    fi
    return "$rc"
}

# --mount 的 source（CSV：整欄雙引號、欄內雙引號兩個）。
mount_source() {
    local v=$1
    v=${v#*\"source=}
    v=${v%%\",target=*}
    REPLY=${v//\"\"/\"}
}

# ---- 引擎（start -ai）用的動作 ----

engine_proto=
engine_id=
engine_ctl=
next_seq=1

# raw <檔名> <內容（printf %b）>：直接寫一個控制檔（先 .tmp 再 mv）。
raw() {
    printf '%b' "$2" >"$engine_ctl/$1.tmp"
    mv -f "$engine_ctl/$1.tmp" "$engine_ctl/$1"
}

# send <op 那一行>：寫 req.<下一個 seq>，等 res。
send() {
    local n=$next_seq
    printf 'vk-resolve/%s %s %s\n%s\n' "$engine_proto" "$engine_id" "$n" "$1" >"$engine_ctl/req.$n.tmp"
    mv -f "$engine_ctl/req.$n.tmp" "$engine_ctl/req.$n"
    next_seq=$((n + 1))
    await "$n"
}

# await <seq>：等 res.<seq>（最多約 10 秒），收到後複製到 got/；被 kill 就以 137 結束。
await() {
    local i
    for ((i = 0; i < 400; i++)); do
        if [[ -e $fake/killed ]]; then
            printf '137' >"$fake/engine.exit"
            exit 137
        fi
        if [[ -e $engine_ctl/res.$1 ]]; then
            mkdir -p "$fake/got"
            cp "$engine_ctl/res.$1" "$fake/got/"
            if [[ -e $engine_ctl/res.$1.out ]]; then
                cp "$engine_ctl/res.$1.out" "$fake/got/"
            fi
            return 0
        fi
        sleep 0.025
    done
    printf '124' >"$fake/engine.exit"
    exit 124
}

# hang：等到被 kill 為止（最多約 10 秒）。
hang() {
    local i
    for ((i = 0; i < 400; i++)); do
        if [[ -e $fake/killed ]]; then
            printf '137' >"$fake/engine.exit"
            exit 137
        fi
        sleep 0.025
    done
    printf '124' >"$fake/engine.exit"
    exit 124
}

# interrupt <INT|TERM>：像在終端按 Ctrl-C（或外層送 SIGTERM 給整個 process group）：訊號同時送到
# 啟動器與 `docker start -ai`，再等著被停。
interrupt() {
    kill -s "$1" "$PPID" "$$"
    hang
}

# start_signaled <128＋訊號編號>：`docker start -ai` 收到訊號。跟真的 docker CLI 一樣，把訊號轉給容器後
# 馬上返回、不等容器停（docker 29 實測）。沒有 --init 時引擎是 PID 1，訊號被忽略，容器一直跑。
start_signaled() {
    : >"$fake/engine.running"
    if [[ -e $fake/engine.init && ! -e $fake/engine.ignores ]]; then
        printf '%s' "$1" >"$fake/engine.pending"
    fi
    exit 0
}

# finish <done 的碼> [<容器結束碼>]：寫 done，以容器結束碼結束。
finish() {
    raw done "vk-resolve/$engine_proto $engine_id done $1\n"
    printf '%s' "${2:-$1}" >"$fake/engine.exit"
    exit "${2:-$1}"
}

case $1 in
--version)
    printf 'Docker version 24.0.7, build afdd53b\n'
    ;;
info)
    rc_of info || exit
    if [[ -f $fake/info ]]; then
        printf '%s\n' "$(<"$fake/info")"
    else
        printf '["name=seccomp,profile=builtin"]\n'
    fi
    ;;
image)
    # image inspect [--format F] <ref>
    if [[ $3 == --format && $4 == *vendor_kit.protocol* ]]; then
        [[ -f $fake/labels ]] || exit 1
        printf '%s\n' "$(<"$fake/labels")"
    else
        rc_of inspect || exit
        printf '[{"Id":"sha256:%s"}]\n' 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    fi
    ;;
pull)
    rc_of pull || exit
    printf '%s\n' "${*: -1}"
    if [[ -f $fake/labels_after_pull ]]; then
        cp "$fake/labels_after_pull" "$fake/labels"
    fi
    ;;
load)
    rc_of load || exit
    # load -q 的 stdout：image ID（N43）
    printf 'Loaded image ID: sha256:%s\n' 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    ;;
create)
    args=("${@:2}")
    if [[ ${args[0]} == -i ]]; then
        rc_of create-engine || exit
        if [[ ${args[1]} == --init ]]; then
            : >"$fake/engine.init"
        fi
        for ((i = 0; i < ${#args[@]}; i++)); do
            if [[ ${args[i]} == --mount && ${args[i + 1]} == *target=/vk/ctl* ]]; then
                mount_source "${args[i + 1]}"
                printf '%s' "$REPLY" >"$fake/ctl_path"
            fi
        done
        printf '%s\n' "${args[@]}" >"$fake/engine.argv"
        printf '%s\n' "$engine_cid"
    elif [[ " ${args[*]} " == *" --entrypoint /__vk_never_run__ "* ]]; then
        rc_of create-extract || exit
        printf '%s\n' "$extract_cid"
    else
        rc_of create-runner || exit
        printf '%s\n' "${args[@]}" >"$fake/runner.argv"
        printf '%s\n' "$runner_cid"
    fi
    ;;
start)
    if [[ $2 == -ai && $3 == "$engine_cid" ]]; then
        mapfile -t argv <"$fake/engine.argv"
        for ((i = 0; i < ${#argv[@]}; i++)); do
            case ${argv[i]} in
            --protocol) engine_proto=${argv[i + 1]} ;;
            --run-id) engine_id=${argv[i + 1]} ;;
            esac
        done
        engine_ctl=$(<"$fake/ctl_path")
        printf '0' >"$fake/engine.exit"
        trap 'start_signaled 130' INT
        trap 'start_signaled 143' TERM
        # shellcheck source=/dev/null
        source "$fake/engine"
        exit "$(<"$fake/engine.exit")"
    elif [[ $2 == -a && $3 == "$runner_cid" ]]; then
        printf 'runner output\n'
        rc_of start-runner || exit
        exit 0
    fi
    exit 1
    ;;
wait)
    # wait <cid>：引擎有之後的結束碼就停下、印出碼；否則像等的時候又被中斷，以 1 返回。
    if [[ $2 == "$engine_cid" && -f $fake/engine.pending ]]; then
        mv -f "$fake/engine.pending" "$fake/engine.exit"
        rm -f "$fake/engine.running"
        printf '%s\n' "$(<"$fake/engine.exit")"
    else
        exit 1
    fi
    ;;
container)
    # container inspect --format F <cid>
    if [[ $5 == "$engine_cid" ]]; then
        if [[ -e $fake/engine.running ]]; then
            printf 'true 0\n'
        else
            printf 'false %s\n' "$(<"$fake/engine.exit")"
        fi
    elif [[ $5 == "$runner_cid" ]]; then
        if [[ -e $fake/runner.notstarted ]]; then
            printf '0001-01-01T00:00:00Z 0\n'
        else
            printf '2026-10-06T00:00:00.000000000Z %s\n' "$(<"$fake/runner.rc")"
        fi
    else
        exit 1
    fi
    ;;
cp)
    rc_of cp || exit
    # cp <cid>:/dist/. <dest>：放一個檔表示複製過
    printf 'dist\n' >"$3/from_image"
    ;;
rm)
    rc_of rm || exit
    if [[ -f $fake/containers ]]; then
        kept=()
        while read -r c_id c_root c_run; do
            if [[ $c_id != "$2" ]]; then
                kept+=("$c_id $c_root $c_run")
            fi
        done <"$fake/containers"
        printf '%s\n' "${kept[@]}" >"$fake/containers"
    fi
    printf '%s\n' "$2"
    ;;
ps)
    if [[ ${*: -1} == '{{.Label "vendor_kit.run"}}' ]]; then
        # ps -a --no-trunc --filter label=vendor_kit.root=<root> --format '{{.Label "vendor_kit.run"}}'
        rc_of ps-runs || exit
        want=${5#label=vendor_kit.root=}
        if [[ -f $fake/containers ]]; then
            while read -r c_id c_root c_run; do
                if [[ -n $c_id && $c_root == "$want" ]]; then
                    printf '%s\n' "$c_run"
                fi
            done <"$fake/containers"
        fi
        exit 0
    fi
    rc_of ps || exit
    if [[ -f $fake/ps ]]; then
        printf '%s\n' "$(<"$fake/ps")"
    fi
    ;;
kill)
    if [[ $2 == "$engine_cid" ]]; then
        : >"$fake/killed"
        if [[ -e $fake/engine.ignores ]]; then
            rm -f "$fake/engine.running"
            printf '137' >"$fake/engine.exit"
        fi
    fi
    printf '%s\n' "$2"
    ;;
*)
    exit 1
    ;;
esac
exit 0
