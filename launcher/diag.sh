# shellcheck shell=bash
# 啟動器的診斷出口（03 輸出的訊息格式）：第一行 `vendor_kit: <level>[VKnnnn]: <message>`，續行原樣，都印到 stderr。
#
# 訊息文字不在這裡寫：呼叫端先載入 msggen 產生的片段（`vk_msg_<code>_level`、`vk_msg_<code>_exit`、
# `vk_msg_<code>_text`，見 engine/msggen 的 --bash-out），這裡只換占位符。
# 已建執行紀錄時（log.sh 的 vk_log_file 有值），每印一條就寫恰好一筆 diagnostic_emitted（ADR-0005:7）。
#
# 整次的結束碼取所有診斷裡最大的那個，沒有診斷時為 0（03 結束碼），存在 vk_diag_exit。

vk_diag_exit=0

# vk_diag_body <code> [<name> <value>]...：把換好占位符的本文放進 REPLY。
# 照引數順序逐一把 `<name>` 全部換成 value，與 engine/diagnostics 的 body 相同（逐項 replace）。
vk_diag_body() {
    local code=$1
    shift
    local var="vk_msg_${code}_text"
    if [[ ! -v $var ]]; then
        return 1
    fi
    local text=${!var} name value token out
    while (($# >= 2)); do
        name=$1
        value=$2
        shift 2
        token="<$name>"
        out=
        while [[ $text == *"$token"* ]]; do
            out+=${text%%"$token"*}$value
            text=${text#*"$token"}
        done
        text=$out$text
    done
    REPLY=$text
}

# vk_diag <code> [<name> <value>]...：印一條診斷並更新 vk_diag_exit。
# 代碼不在載入的片段裡是 VK 的 bug，改報 VK0056。
vk_diag() {
    local code=$1
    shift
    if ! vk_diag_body "$code" "$@"; then
        if [[ $code == VK0056 ]]; then
            printf 'vendor_kit: error[VK0056]: message fragment is not loaded\n' >&2
            vk_diag_exit=2
            return 0
        fi
        vk_diag VK0056 reason "unknown reason code $code" path "${vk_log_file:-none}"
        return 0
    fi
    local body=$REPLY
    local level_var="vk_msg_${code}_level" exit_var="vk_msg_${code}_exit"
    local level=${!level_var} code_exit=${!exit_var}
    printf 'vendor_kit: %s[%s]: %s\n' "$level" "$code" "$body" >&2
    if ((code_exit > vk_diag_exit)); then
        vk_diag_exit=$code_exit
    fi
    if [[ -n ${vk_log_file:-} ]]; then
        vk_log_diagnostic "$code" "$level" "$body" "$@"
    fi
    return 0
}
