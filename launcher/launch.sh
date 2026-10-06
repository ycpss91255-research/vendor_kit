# shellcheck shell=bash
# 啟動器的 VK recipe 流程：起唯一的引擎容器，在旁邊代辦 docker 動作（#372 的 D2；ADR-0007:30–31、ADR-0012:22）。
#
# 判定順序（#372 實作前討論 q-engine-impl-1：用法只有引擎判得出，04 說明與用法錯誤的順序隨之改）：
#   1. 主機前置檢查（host.sh）：沒有副作用，失敗不建執行紀錄。
#   2. 辨識救援呼叫（vk_launch_is_rescue）：只看 recipe 名與 `--` 之前有沒有 `--engine`，純字串比對。
#   3. 建執行紀錄（log.sh）。之後的診斷都寫進紀錄。
#   4. 介面版判定（vk_launch_interface，N13）：離線做，不上網、不起容器。讀 version.toml 引擎鎖定行旁記的
#      介面版列表（host.sh 的 vk_lock_protocols），拿薄殼的 P 逐項做字串相等比對；P 低於列表最小值回
#      VK0009（fatal 3），除執行紀錄外零寫入（ADR-0008）。救援呼叫不判、不讀列表。
#   5. 取得引擎 image（vk_launch_obtain，N40）：本機沒有才 pull 鎖定的 pinned 引用（有逾時，N59），
#      取不到回 VK0036。救援呼叫也一樣。一般路徑接著讀 image 的 LABEL 跟列表核對，不一致就不起容器。
#   6. 起引擎：用法、安裝目錄（VK0028）與檔案版（VK0008）都由引擎判。
#   第 6 步（建 session 目錄、寫 in/engine、起引擎、收尾）是 vk_launch_session，bootstrap.sh 的首次導入也用它。
#
# 引擎與往返（文法見 wire.sh 與 engine/plan）：
# - repo 外的 session 目錄 `${TMPDIR:-/tmp}/vendor_kit.<run-id>/`，以 mkdir -m 700 排他建立；
#   底下 ctl/ 可寫掛在 /vk/ctl、in/ 唯讀掛在 /vk/in，安裝目錄掛在 /vk/root。
# - 起引擎之前先把這次用的 pinned 引用寫成 in/engine（wire.sh 的 vk_wire_in_engine；先 .tmp 再 mv），
#   救援呼叫也寫。之後 stage、stage-dir、extract 到同名 slot 都會被拒，整次只寫這一次。
# - `docker create -i --init` 先拿到容器 ID，再以前景 `docker start -ai` 起引擎（stdin 接通、不帶 -t，
#   stdout 與 stderr 分開）；代辦迴圈（vk_launch_serve）在背景跑，結果寫 res.<seq>（先 .tmp 再 mv）。
# - docker 子程序的輸出一律攔下（N20，03:45–46）：啟動器呼叫的 docker（pull、load、inspect、ps、create、cp、
#   rm）與 stage、stage-dir 的 cp，stderr 都附加到 session 目錄的 docker.err（vk_launch_errlog；在 ctl/、in/
#   之外，引擎看不到），不繼承；stdout 不是要交給引擎的資料就丟掉。docker 的原文不解析、不決定結果（03:26），
#   失敗時印的是 VK 自己的診斷。docker.err 跟 session 目錄一起刪，不寫進執行紀錄（摘錄要不要進紀錄是 N20b，
#   還沒定）。session 目錄建好之前的 pull（vk_launch_obtain）沒有地方放，stderr 直接丟掉。
#   照舊繼承的只有兩個：引擎的 `docker start -ai`（引擎自己的 VK 輸出）與 test runner 的 `docker start -a`
#   （04 test 承諾 runner 的輸出原樣給使用者）。
# - 中斷（N49）：引擎不當 PID 1，由 --init 的 tini 把 docker CLI 轉來的 SIGINT、SIGTERM 交給引擎
#   （PID 1 沒裝處理時兩者都被忽略）。docker start -ai 轉完訊號就返回、不等容器停（docker 29 實測），
#   所以收到中斷後先 docker wait 等引擎停下，再停代辦迴圈；等的時候再中斷一次就照下面停不下來的路徑 kill。
#   代辦迴圈忽略 SIGINT、SIGTERM，只在 done、stop 或協定不合時結束。
#   中斷不是 VK 的 bug：沒有 done 時不印診斷，run_finished 記引擎容器的結束碼，
#   整次以 128＋訊號編號結束（SIGINT 130、SIGTERM 143；04 說外層中斷的碼不承諾是 VK 結束碼）。
#   引擎被訊號停下時不寫 engine_finished，run_finished 由啟動器補。
# - 協定不合（VK0056）時迴圈停掉引擎容器，原因寫在 session 目錄的 fault（不在 ctl/，引擎寫不到）。
# - 引擎結束後核對 done 與容器結束碼，寫 run_finished，刪容器（不加 -f）與 session 目錄。
#   容器停不下來時保留 session 目錄與容器，不刪現場。
# - 殘留的現場（N58）：`prune` 會刪本安裝目錄已停止的容器，但 session 目錄在 repo 外、引擎看不到。
#   所以 `prune` 起引擎之前先記下帶本安裝目錄 label 的容器屬於哪些 run-id，`prune` 成功（結束碼 0）之後
#   再查一次：先前有、現在一個容器都不剩的 run-id，它留下的 `vendor_kit.<run-id>/` 由啟動器刪掉。
#   session 目錄本身不記安裝目錄，只有容器的 label 記，所以只清這次執行期間容器被刪掉的；更早就沒了
#   容器的目錄不清。stdout 不列刪了什麼（要列得由引擎印，協定還沒有對應的 op）。
#
# 呼叫端（薄殼）先載入 msggen 的訊息片段與 diag.sh、host.sh、log.sh、wire.sh，設好 vk_log_version。
# 那些檔定義的變數（vk_wire_*、vk_log_*、vk_diag_exit、vk_req_*）在這裡直接用。
# shellcheck disable=SC2154

# 引擎 image 公告介面版區間的 LABEL（ADR-0008:27）。
vk_label_floor=vendor_kit.protocol.floor
vk_label_current=vendor_kit.protocol.current
# 啟動器建的每個容器都帶這兩個 label：所屬安裝目錄與這次執行（ps 只列本安裝目錄的）。
vk_label_root=vendor_kit.root
vk_label_run=vendor_kit.run
# extract 建容器時的入口：不存在的檔，容器永遠不會被 run（ADR-0006）。
vk_never_run=/__vk_never_run__
# 代辦迴圈看控制檔的間隔（秒）。
vk_poll=0.05
# session 目錄裡收 docker 子程序 stderr 的檔名（N20）。
vk_launch_errfile=docker.err
# 本機沒有引擎 image 時 pull 的逾時（秒，N59）；逾時跟 pull 失敗一樣回 VK0036。
vk_pull_timeout=600
# 還沒有專屬原因代碼的介面版情況，以 VK0056 停下時 reason 後面附的說明（過渡做法）。
vk_pending_list='reason code pending (draft VK0070, N13)'
vk_pending_newer='reason code pending (draft VK0076, N82)'
vk_pending_label='reason code pending (draft VK0080, N13)'

vk_launch_stop=none

# vk_launch_is_rescue [<recipe> <args>...]：救援呼叫回 0（ADR-0007:37、04 說明與用法錯誤）。
# 救援呼叫：不帶指令（用法）、install、sync、upgrade 在 `--` 之前帶 `--engine` 或 `--engine=<tag>`；
# 這些的 -h／--help 也算。其他 recipe 即使帶 -h 也不是。
vk_launch_is_rescue() {
    if (($# == 0)); then
        return 0
    fi
    local recipe=$1
    shift
    case $recipe in
    install | sync) return 0 ;;
    upgrade) ;;
    *) return 1 ;;
    esac
    local a
    for a in "$@"; do
        if [[ $a == -- ]]; then
            return 1
        fi
        if [[ $a == --engine || $a == --engine=* ]]; then
            return 0
        fi
    done
    return 1
}

# vk_launch_fail <code> [<name> <value>]...：印一條診斷並記成這次的停下原因。
vk_launch_fail() {
    vk_launch_stop=$1
    vk_diag "$@"
}

# vk_launch_internal <reason>：VK0056（VK 的 bug）。
vk_launch_internal() {
    vk_launch_fail VK0056 reason "$1" path "${vk_log_file:-none}"
}

# vk_launch_engine_version <engine_ref>：引擎版本（pinned 引用的 tag）放進 REPLY；引用沒有 tag 時是 unknown。
# 介面版判定是離線做的，VK0009 的 <vY> 不讀 image 的 LABEL。
vk_launch_engine_version() {
    local name=${1%%@*}
    local last=${name##*/}
    REPLY=unknown
    if [[ $last == *:* ]]; then
        REPLY=${last##*:}
    fi
}

# vk_launch_labels <engine_ref>：讀本機 image 公告介面版區間的 LABEL，放進 vk_image_floor、vk_image_current。
# 本機沒有那個 image 回 1。不上網。
vk_launch_labels() {
    local out _
    local fmt="{{index .Config.Labels \"$vk_label_floor\"}} {{index .Config.Labels \"$vk_label_current\"}}"
    vk_image_floor=
    vk_image_current=
    if ! out=$(docker image inspect --format "$fmt" "$1" 2>/dev/null); then
        return 1
    fi
    read -r vk_image_floor vk_image_current _ <<<"$out"
    return 0
}

# vk_launch_obtain <engine_ref>：確保本機有引擎 image（N40）。有就不 pull；沒有才以 vk_pull_timeout 秒的逾時
# pull 這個 pinned 引用，失敗或逾時回 VK0036，不改用其他版本。成功時 image 的 LABEL 已讀進 vk_image_*。
# 這時還沒有 session 目錄，docker pull 的 stdout、stderr 都丟掉（N20）。
vk_launch_obtain() {
    local engine=$1 rc
    if vk_launch_labels "$engine"; then
        return 0
    fi
    timeout "$vk_pull_timeout" docker pull -q "$engine" >/dev/null 2>&1
    rc=$?
    if ((rc == 124)); then
        vk_launch_fail VK0036 image "$engine" reason "docker pull timed out after $vk_pull_timeout seconds"
        return 1
    fi
    if ((rc != 0)); then
        vk_launch_fail VK0036 image "$engine" reason "docker pull exited with $rc"
        return 1
    fi
    if ! vk_launch_labels "$engine"; then
        vk_launch_fail VK0036 image "$engine" reason "the image is not available locally after docker pull"
        return 1
    fi
    return 0
}

# vk_launch_interface <host_root> <engine_ref> <P_shell>：一般路徑的介面版判定與取得引擎 image。合回 0；不合印診斷回 1。
# 1. 離線判（N13，ADR-0008:3、27）：讀 <host_root>/.vendor_kit/version.toml 的介面版列表，P 跟列表逐項做字串
#    相等比對（ADR-0007:31）。列表缺漏或格式錯、P 高於列表最大值都還沒有專屬代碼，以 VK0056 停下；
#    P 低於列表最小值回 VK0009。這一步不上網、不碰 docker。
# 2. 比對通過才取得 image（vk_launch_obtain）：本機沒有才 pull。
# 3. 起容器之前讀 image 的 LABEL 跟列表核對：區間 [floor, current] 要剛好是列表的頭尾（列表已驗過是連續遞增），
#    不一致以 VK0056 停下。
vk_launch_interface() {
    local root=$1 engine=$2 proto=$3
    if ! vk_lock_protocols "$root/.vendor_kit/version.toml"; then
        vk_launch_internal "$REPLY; $vk_pending_list"
        return 1
    fi
    local list=$REPLY item found=0
    local -a items
    read -r -a items <<<"$list"
    for item in "${items[@]}"; do
        if [[ $item == "$proto" ]]; then
            found=1
        fi
    done
    local first=${items[0]} last=${items[${#items[@]} - 1]}
    if ((!found)); then
        if ((proto < first)); then
            vk_launch_engine_version "$engine"
            vk_launch_fail VK0009 P_shell "$proto" vY "$REPLY"
        else
            vk_launch_internal "shell interface version $proto is newer than the interface versions $list accepted by the locked engine; $vk_pending_newer"
        fi
        return 1
    fi
    vk_launch_obtain "$engine" || return 1
    local floor=$vk_image_floor current=$vk_image_current
    if [[ ! $floor =~ $vk_wire_re_proto || ! $current =~ $vk_wire_re_proto ]] || ((floor > current)); then
        vk_launch_internal "the engine image $engine does not announce a valid interface version range"
        return 1
    fi
    if [[ $floor != "$first" || $current != "$last" ]]; then
        vk_launch_internal "the engine image $engine announces interface versions $floor-$current, but version.toml records $list; $vk_pending_label"
        return 1
    fi
    return 0
}

# vk_launch_user：引擎與 runner 以誰的身分跑，放進陣列 vk_user_args。
# rootless Docker 已把容器的 root 對到主機使用者，不另指定；其他情況用主機的 uid:gid，寫出的檔才是使用者的。
vk_launch_user() {
    vk_user_args=()
    local opts
    opts=$(docker info --format '{{json .SecurityOptions}}' 2>/dev/null)
    if [[ $opts == *rootless* ]]; then
        return 0
    fi
    local gid
    gid=$(id -g)
    vk_user_args=(--user "$UID:$gid")
}

# vk_launch_finish <engine_exit|""> → 寫 run_finished，整次的結束碼放進 REPLY。
# 結束碼取引擎與啟動器診斷之中最大的；沒起引擎或引擎的結束碼不可信時只看啟動器的。
vk_launch_finish() {
    local engine=$1 code=$vk_diag_exit
    if [[ $engine =~ ^[0-3]$ && $vk_launch_stop == none ]] && ((engine > code)); then
        code=$engine
    fi
    vk_log_finish "$code" "$engine" "$vk_launch_stop"
    REPLY=$code
}

# vk_launch <host_root> <host_cwd> <engine_ref> <P_shell> [<recipe> <args>...]：跑一次 VK recipe，
# 結束碼放進 REPLY 並回傳。host_cwd 是使用者下指令時的目錄（just 的 invocation_directory()）；
# recipe 與參數原樣轉給引擎，不帶 recipe 是 `just vendor_kit` 的用法呼叫。
vk_launch() {
    local root=$1 cwd=$2 engine=$3 proto=$4
    shift 4
    vk_launch_stop=none
    if ! vk_host_precheck recipe; then
        REPLY=$vk_diag_exit
        return "$REPLY"
    fi
    if [[ $root != /* || $cwd != /* ]] || ! vk_wire_ref "$engine" pinned || [[ ! $proto =~ $vk_wire_re_proto ]]; then
        vk_launch_internal "invalid launcher arguments"
        REPLY=$vk_diag_exit
        return "$REPLY"
    fi
    # 主機的 symlink 在容器裡解不了，先解成實體路徑。
    if ! root=$(cd -- "$root" 2>/dev/null && pwd -P) || ! cwd=$(cd -- "$cwd" 2>/dev/null && pwd -P); then
        vk_launch_internal "cannot resolve the install or working directory"
        REPLY=$vk_diag_exit
        return "$REPLY"
    fi

    local rescue=0
    if vk_launch_is_rescue "$@"; then
        rescue=1
    fi

    local verb=${1:-vendor_kit}
    if [[ ! $verb =~ ^[a-z0-9_]+$ ]]; then
        verb=unknown
    fi
    if ! vk_log_start "$root/.vendor_kit/log" "$verb" recipe "$@"; then
        REPLY=$vk_diag_exit
        return "$REPLY"
    fi
    local run_id=$vk_log_invocation_id run_log=${vk_log_file#"$root/"}
    if [[ ! $run_id =~ $vk_wire_re_run_id ]]; then
        vk_launch_internal "invocation id $run_id does not fit the protocol"
        vk_launch_finish ""
        return "$REPLY"
    fi

    # 救援呼叫不判介面版、不讀列表，但本機沒有 image 時一樣要 pull（N40）。
    if ((rescue)); then
        if ! vk_launch_obtain "$engine"; then
            vk_launch_finish ""
            return "$REPLY"
        fi
    elif ! vk_launch_interface "$root" "$engine" "$proto"; then
        vk_launch_finish ""
        return "$REPLY"
    fi

    vk_launch_session "$root" "$cwd" "$engine" "$engine" "$proto" "$run_id" "$run_log" "$@"
}

# vk_launch_session <host_root> <host_cwd> <image> <engine_ref> <P> <run-id> <run-log> [<recipe> <args>...]：
# 執行紀錄已建好、引擎 image 已在本機之後的共同段（VK recipe 與 bootstrap.sh 首次導入共用）：建 session 目錄、
# 把 engine_ref 寫成 in/engine、以 image 建引擎容器並起引擎，收尾。image 是 docker create 用的 image
# （VK recipe 是 engine_ref 本身；bootstrap.sh 的 -i 是載入後的 image ID），engine_ref 是寫進 in/engine 的 pinned 引用。
# 結束碼放進 REPLY 並回傳。
vk_launch_session() {
    local root=$1 cwd=$2 image=$3 engine=$4 proto=$5 run_id=$6 run_log=$7
    shift 7
    local tmp=${TMPDIR:-/tmp}
    tmp=${tmp%/}
    local sess="${tmp:-/tmp}/vendor_kit.$run_id"
    if ! mkdir -m 700 -- "$sess" 2>/dev/null || ! mkdir -- "$sess/ctl" "$sess/in" 2>/dev/null; then
        vk_launch_internal "cannot create the session directory $sess"
        vk_launch_finish ""
        return "$REPLY"
    fi
    local ref=$sess/in/$vk_wire_in_engine
    if ! { printf '%s\n' "$engine" >"$ref.tmp" && mv -f -- "$ref.tmp" "$ref"; } 2>/dev/null; then
        rm -rf -- "$sess"
        vk_launch_internal "cannot write the engine reference to the session directory $sess"
        vk_launch_finish ""
        return "$REPLY"
    fi

    # prune 起引擎之前記下本安裝目錄的容器所屬的 run-id；查不到就不清殘留的現場。
    local prune=0
    local -a before=()
    if [[ ${1:-} == prune ]] && vk_launch_runs "$root"; then
        prune=1
        before=("${vk_runs[@]}")
    fi

    vk_launch_engine "$sess" "$root" "$cwd" "$image" "$proto" "$run_id" "$run_log" "$@"
    local code=$REPLY
    if ((prune && code == 0)); then
        vk_launch_prune_sessions "${tmp:-/tmp}" "$root" "$run_id" "${before[@]}"
    fi
    REPLY=$code
    return "$REPLY"
}

# vk_launch_runs <root>：帶本安裝目錄 label 的容器（不論狀態）所屬的 run-id，一個容器一個，放進陣列 vk_runs。
# docker 失敗回 1。
vk_launch_runs() {
    vk_runs=()
    local out line
    if ! out=$(docker ps -a --no-trunc --filter "label=$vk_label_root=$1" --format "{{.Label \"$vk_label_run\"}}" 2>/dev/null); then
        return 1
    fi
    while IFS= read -r line; do
        if [[ -n $line ]]; then
            vk_runs+=("$line")
        fi
    done <<<"$out"
    return 0
}

# vk_launch_prune_sessions <tmp> <root> <run-id> [<prune 之前的 run-id>...]：prune 成功之後清殘留的現場（N58）。
# 只刪這樣的 <tmp>/vendor_kit.<id>/：<id> 在 prune 之前帶本安裝目錄 label 的容器裡、現在一個都不剩、
# 不是這次執行，而且是自己的實體目錄（不是 symlink）。label 值來自 docker，先照 run-id 文法驗過才拼路徑。
# 查不到現在的容器就一個都不刪。不印、不影響結束碼。
vk_launch_prune_sessions() {
    local tmp=$1 root=$2 self=$3
    shift 3
    if (($# == 0)) || ! vk_launch_runs "$root"; then
        return 0
    fi
    local id now dir left
    for id in "$@"; do
        if [[ ! $id =~ $vk_wire_re_run_id || $id == "$self" ]]; then
            continue
        fi
        left=0
        for now in "${vk_runs[@]}"; do
            if [[ $now == "$id" ]]; then
                left=1
            fi
        done
        dir=$tmp/vendor_kit.$id
        if ((!left)) && [[ -d $dir && ! -L $dir && -O $dir ]]; then
            rm -rf -- "$dir" 2>/dev/null
        fi
    done
    return 0
}

# vk_launch_engine <sess> <root> <cwd> <image> <P> <run-id> <run-log> [<recipe> <args>...]：
# 以 image 建、起引擎與代辦迴圈，收尾。結束碼放進 REPLY。
vk_launch_engine() {
    local sess=$1 root=$2 cwd=$3 image=$4 proto=$5 run_id=$6 run_log=$7
    shift 7
    local tty='' nocolor=0 fd
    for fd in 0 1 2; do
        if [[ -t $fd ]]; then
            tty="${tty}1"
        else
            tty="${tty}0"
        fi
    done
    if [[ -n ${NO_COLOR:-} ]]; then
        nocolor=1
    fi
    vk_launch_user
    # 之後啟動器呼叫的 docker 子程序（含背景的代辦迴圈）stderr 都附加到這裡（N20）。
    vk_launch_errlog=$sess/$vk_launch_errfile
    local m_root m_ctl m_in
    vk_wire_mount_source "$root"
    m_root="type=bind,$REPLY,target=$vk_wire_mount_root"
    vk_wire_mount_source "$sess/ctl"
    m_ctl="type=bind,$REPLY,target=$vk_wire_mount_ctl"
    vk_wire_mount_source "$sess/in"
    m_in="type=bind,$REPLY,target=$vk_wire_mount_in,readonly"

    local cid rc
    cid=$(docker create -i --init "${vk_user_args[@]}" \
        --label "$vk_label_root=$root" --label "$vk_label_run=$run_id" \
        --mount "$m_root" --mount "$m_ctl" --mount "$m_in" -w "$vk_wire_mount_root" \
        "$image" \
        "${vk_wire_argv[0]}" "$proto" "${vk_wire_argv[1]}" "$run_id" "${vk_wire_argv[2]}" "$root" \
        "${vk_wire_argv[3]}" "$cwd" "${vk_wire_argv[4]}" "$run_log" "${vk_wire_argv[5]}" "$tty" \
        "${vk_wire_argv[6]}" "$nocolor" -- "$@" 2>>"$vk_launch_errlog")
    rc=$?
    if ((rc != 0)) || [[ ! $cid =~ $vk_wire_re_cid ]]; then
        rm -rf -- "$sess"
        vk_launch_internal "docker create for the engine exited with $rc"
        vk_launch_finish ""
        return "$REPLY"
    fi

    trap 'vk_launch_interrupted "$sess" INT' INT
    trap 'vk_launch_interrupted "$sess" TERM' TERM
    vk_launch_serve "$sess" "$cid" "$root" "$proto" "$run_id" &
    local loop=$!
    docker start -ai "$cid"
    if [[ -e $sess/interrupted ]]; then
        docker wait "$cid" >/dev/null 2>&1
    fi
    : >"$sess/stop"
    # 等代辦迴圈的 wait 會被收到的訊號打斷，迴圈真的結束才往下。
    while kill -0 "$loop" 2>/dev/null; do
        wait "$loop"
    done
    trap - INT TERM

    # 引擎容器真的停了才收尾；停不下來就保留現場。
    local state running exit
    state=$(docker container inspect --format '{{.State.Running}} {{.State.ExitCode}}' "$cid" 2>/dev/null)
    read -r running exit <<<"$state"
    if [[ $running != false ]]; then
        docker kill "$cid" >/dev/null 2>&1
        state=$(docker container inspect --format '{{.State.Running}} {{.State.ExitCode}}' "$cid" 2>/dev/null)
        read -r running exit <<<"$state"
    fi
    if [[ $running != false || ! $exit =~ ^[0-9]+$ ]]; then
        vk_launch_internal "the engine container $cid did not stop; kept $sess"
        vk_launch_finish ""
        return "$REPLY"
    fi

    local reason='' sig=''
    if [[ -e $sess/fault ]]; then
        IFS= read -r reason <"$sess/fault"
        vk_launch_internal "${reason:-the request loop failed}"
    elif [[ -e $sess/interrupted && ! -e $sess/ctl/done ]]; then
        IFS= read -r sig <"$sess/interrupted"
        docker rm "$cid" >/dev/null 2>>"$vk_launch_errlog"
        rm -rf -- "$sess"
        local code=130
        if [[ $sig == TERM ]]; then
            code=143
        fi
        vk_log_finish "$code" "$exit" none
        REPLY=$code
        return "$REPLY"
    elif ! vk_wire_parse_done "$sess/ctl/done" "$proto" "$run_id"; then
        vk_launch_internal "$REPLY (engine exit code $exit)"
    elif [[ $REPLY != "$exit" ]]; then
        vk_launch_internal "done exit code $REPLY does not match the engine container exit code $exit"
    fi
    docker rm "$cid" >/dev/null 2>>"$vk_launch_errlog"
    rm -rf -- "$sess"
    vk_launch_finish "$exit"
    return "$REPLY"
}

# vk_launch_interrupted <sess> <INT|TERM>：收到中斷時記下第一個訊號（runner 的結果與收尾都看這個檔）。
vk_launch_interrupted() {
    if [[ ! -e $1/interrupted ]]; then
        { printf '%s\n' "$2" >"$1/interrupted"; } 2>/dev/null
    fi
}

# vk_launch_serve <sess> <engine_cid> <root> <P> <run-id>：代辦迴圈（在背景跑）。
# 依序等 req.<seq>，驗文法、做 op、寫 res.<seq>；看到 done 或 stop 就結束。
# 協定不合時把原因寫進 <sess>/fault、停掉引擎容器，以 1 結束。
# 忽略 SIGINT、SIGTERM：中斷後引擎還在收尾時照樣代辦，由 vk_launch_engine 決定什麼時候停。
vk_launch_serve() {
    local sess=$1 engine_cid=$2 root=$3 proto=$4 run_id=$5
    trap '' INT TERM
    local ctl=$sess/ctl seq=1 f name
    vk_serve_ps=()
    while :; do
        if [[ -e $ctl/req.$seq ]]; then
            if ((seq > 9999)); then
                vk_launch_fault "request sequence exhausted"
            fi
            if ! vk_wire_parse_req "$ctl/req.$seq" "$proto" "$run_id" "$seq"; then
                vk_launch_fault "$REPLY"
            fi
            vk_launch_dispatch "$sess" "$root" "$run_id" "$seq"
            local result=$REPLY
            if ! vk_wire_result_ok "$vk_req_op" "$result"; then
                vk_launch_fault "launcher produced an invalid result for op $vk_req_op"
            fi
            vk_wire_res "$proto" "$run_id" "$seq" "$result"
            if ! { printf '%s' "$REPLY" >"$ctl/res.$seq.tmp" && mv -f -- "$ctl/res.$seq.tmp" "$ctl/res.$seq"; } 2>/dev/null; then
                vk_launch_fault "cannot write res.$seq"
            fi
            seq=$((seq + 1))
            continue
        fi
        # 等的是 req.<seq>；出現別的 req 檔就是跳號或檔名不合。
        for f in "$ctl"/req.*; do
            name=${f##*/req.}
            if [[ ! -e $f || $name == *.tmp ]]; then
                continue
            fi
            if [[ ! $name =~ $vk_wire_re_seq ]] || ((name > seq)); then
                vk_launch_fault "unexpected request file ${f##*/} while waiting for req.$seq"
            fi
        done
        if [[ -e $ctl/done || -e $sess/stop ]]; then
            return 0
        fi
        sleep "$vk_poll"
    done
}

# vk_launch_fault <reason>：代辦迴圈裡的協定不合。
vk_launch_fault() {
    { printf '%s\n' "$1" >"$sess/fault"; } 2>/dev/null
    docker kill "$engine_cid" >/dev/null 2>&1
    exit 1
}

# vk_launch_result <rc>：runner 以外的 op 的結果：0 是 ok，其他是 failed <rc>。
vk_launch_result() {
    if (($1 == 0)); then
        REPLY=ok
    else
        REPLY="failed $1"
    fi
}

# vk_launch_dispatch <sess> <root> <run-id> <seq>：照 vk_req_op 與 vk_req_args 做固定的 docker 動作，
# result 那一行放進 REPLY。只在這裡呼叫 docker；op 不在封閉清單的已在 wire.sh 擋掉。
# 交給引擎的原始輸出寫 res.<seq>.out：inspect、ps，以及 load -q 的 stdout（引擎從裡面拿 image ID，N43）。
# stderr 一律附加到 vk_launch_errlog（N20）。
vk_launch_dispatch() {
    local sess=$1 root=$2 run_id=$3 seq=$4
    local ctl=$sess/ctl in=$sess/in rc=0
    local out=$ctl/res.$seq.out
    local -a a=("${vk_req_args[@]}")
    local -a labels=(--label "$vk_label_root=$root" --label "$vk_label_run=$run_id")
    case $vk_req_op in
    pull)
        docker pull -q "${a[0]}" >/dev/null 2>>"$vk_launch_errlog"
        rc=$?
        ;;
    load)
        docker load -q -i "${a[0]}" >"$out" 2>>"$vk_launch_errlog"
        rc=$?
        ;;
    inspect)
        docker image inspect "${a[0]}" >"$out" 2>>"$vk_launch_errlog"
        rc=$?
        ;;
    extract)
        vk_launch_extract "${a[0]}" "$in/${a[1]}" "${labels[@]}"
        rc=$REPLY
        ;;
    stage)
        if [[ -e $in/${a[1]} ]]; then
            rc=1
        else
            cp -- "${a[0]}" "$in/${a[1]}" 2>>"$vk_launch_errlog"
            rc=$?
        fi
        ;;
    stage-dir)
        vk_launch_stage_dir "${a[0]}" "$in/${a[1]}"
        rc=$REPLY
        ;;
    ps)
        docker ps -a --no-trunc --filter "label=$vk_label_root=$root" --filter status=exited --format '{{.ID}}' >"$out" 2>>"$vk_launch_errlog"
        rc=$?
        vk_serve_ps=()
        if ((rc == 0)); then
            local line
            while IFS= read -r line; do
                vk_serve_ps+=("$line")
            done <"$out"
        fi
        ;;
    rm-container)
        local id listed=0
        for id in "${vk_serve_ps[@]}"; do
            if [[ $id == "${a[0]}" ]]; then
                listed=1
            fi
        done
        if ((!listed)); then
            vk_launch_fault "rm-container ${a[0]} was not listed by ps"
        fi
        docker rm "${a[0]}" >/dev/null 2>>"$vk_launch_errlog"
        rc=$?
        ;;
    runner)
        vk_launch_runner "$sess" "$root" "${a[@]}"
        return 0
        ;;
    esac
    vk_launch_result "$rc"
}

# vk_launch_extract <image_id> <dest> <label 參數>...：建容器（不 run）、cp /dist/. 進 dest、刪容器。
# 結束碼放進 REPLY：第一個失敗的 docker 動作的碼；容器一律刪掉。
vk_launch_extract() {
    local image=$1 dest=$2 c rc
    shift 2
    if [[ -e $dest ]] || ! mkdir -- "$dest" 2>/dev/null; then
        REPLY=1
        return 0
    fi
    c=$(docker create "$@" --entrypoint "$vk_never_run" "$image" 2>>"$vk_launch_errlog")
    rc=$?
    if ((rc != 0)) || [[ ! $c =~ $vk_wire_re_cid ]]; then
        REPLY=$((rc == 0 ? 1 : rc))
        return 0
    fi
    docker cp "$c:/dist/." "$dest" >/dev/null 2>>"$vk_launch_errlog"
    rc=$?
    docker rm "$c" >/dev/null 2>>"$vk_launch_errlog"
    local rm_rc=$?
    if ((rc == 0)); then
        rc=$rm_rc
    fi
    REPLY=$rc
}

# vk_launch_stage_dir <host dir> <dest>：把主機上的目錄整個複製進 dest（in/<slot>，唯讀掛進引擎；N48 的開發來源）。
# 結束碼放進 REPLY：來源不是目錄、dest 已存在或建不出來是 1，其他是 cp 的碼。
# 複製的是 "<host dir>/." 而不是 <host dir> 本身：來源是 symlink 時 cp -R 不跟隨命令列上的連結，
# dest 會變成指向容器外路徑的連結；先建 dest 再複製內容就沒有這個問題。
vk_launch_stage_dir() {
    local src=$1 dest=$2
    if [[ ! -d $src || -e $dest ]] || ! mkdir -- "$dest" 2>/dev/null; then
        REPLY=1
        return 0
    fi
    cp -R -- "$src/." "$dest" 2>>"$vk_launch_errlog"
    REPLY=$?
}

# vk_launch_runner <sess> <root> <image> <command> [<arg>...]：test runner（04 test）：
# command 加參數、不經 shell；repo（安裝目錄往上第一個有 .git 的目錄，同 host.sh 的 vk_find_git，但不印診斷）唯讀掛在 /vk/repo，安裝目錄的 .vendor_kit/ 以空的 tmpfs 遮住，
# /tmp 是用完即丟的 tmpfs，工作目錄是安裝目錄。runner 的 stdout、stderr（docker start -a）直接繼承；
# 建、刪 runner 容器的 docker create、rm 的 stderr 照 N20 攔下。
# result 那一行放進 REPLY：起不來是 notstarted；被 VK 停掉（收到中斷）是 stopped；其他是 exited。
vk_launch_runner() {
    local sess=$1 root=$2 image=$3 command=$4
    shift 4
    REPLY="runner notstarted"
    if [[ -z $command ]]; then
        return 0
    fi
    local repo=$root
    while [[ ! -e $repo/.git ]]; do
        if [[ -z $repo || $repo == / ]]; then
            return 0
        fi
        repo=${repo%/*}
    done
    local rel=${root#"$repo"}
    local wd="/vk/repo$rel"
    local m_repo m_mask
    vk_wire_mount_source "${repo:-/}"
    m_repo="type=bind,$REPLY,target=/vk/repo,readonly"
    vk_wire_mount_target "$wd/.vendor_kit"
    m_mask="type=tmpfs,$REPLY"
    local c rc
    c=$(docker create "${vk_user_args[@]}" --label "$vk_label_root=$root" --label "$vk_label_run=$run_id" \
        --mount "$m_repo" --mount "$m_mask" --mount type=tmpfs,target=/tmp -w "$wd" \
        --entrypoint="$command" "$image" "$@" 2>>"$vk_launch_errlog")
    rc=$?
    REPLY="runner notstarted"
    if ((rc != 0)) || [[ ! $c =~ $vk_wire_re_cid ]]; then
        return 0
    fi
    docker start -a "$c"
    local state started code
    state=$(docker container inspect --format '{{.State.StartedAt}} {{.State.ExitCode}}' "$c" 2>/dev/null)
    read -r started code <<<"$state"
    if [[ -z $started || $started == 0001-01-01T00:00:00Z ]]; then
        REPLY="runner notstarted"
    elif [[ -e $sess/interrupted ]]; then
        if [[ $code =~ $vk_wire_re_rc ]]; then
            REPLY="runner stopped $code"
        else
            REPLY="runner stopped unavailable"
        fi
    elif [[ $code =~ $vk_wire_re_rc ]]; then
        REPLY="runner exited $code"
    else
        REPLY="runner stopped unavailable"
    fi
    docker rm "$c" >/dev/null 2>>"$vk_launch_errlog"
    return 0
}
