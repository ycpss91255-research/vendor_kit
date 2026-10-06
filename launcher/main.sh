# shellcheck shell=bash
# 薄殼 log.sh 的入口（#372 的 N38）：vendor.just 的每個 VK recipe 以
# `bash .vendor_kit/log.sh <安裝目錄> <下指令的目錄> [<recipe> <args>...]` 呼叫這裡，參數原樣轉給 vk_launch。
#
# - 薄殼的 log.sh 是 launcher/shell/assemble.sh 組出的本文（訊息片段，接著 diag、host、log、wire、launch、
#   這個檔），安裝時引擎再在檔頭加自描述標頭（engine/shell）。這裡只讀標頭的介面版與引擎版：
#   介面版是傳給引擎的 P，引擎版是執行紀錄的 resource."service.version"（log.sh 的 vk_log_version）。
# - 引擎引用取自 `.vendor_kit/version.toml` 裡唯一符合 `^vendor_kit[[:space:]]*=` 的行（ADR-0002），
#   讀法見 host.sh 的 vk_lock_engine_ref。命中數不是 1、值不是雙引號裡的 pinned 引用，都以 VK0056 停下
#   （專屬的原因代碼還沒定：草稿 VK0070，N76）。
# - 不套用 version.local.toml 的本機覆寫（之後另做）。
# - 讀標頭與版本鎖定行都沒有副作用：失敗時只在 stderr 印診斷，不建執行紀錄（同 host.sh 的前置檢查）。
# - 標頭行尾的 CR 先去掉再比對（ADR-0012：CRLF 與 LF 等價）。
#
# 這個檔只定義函式；直接以 bash 執行組好的 log.sh 時，最後才呼叫 vk_main。被 source 時不執行。
# vk_wire_re_* 由 wire.sh 定義。
# shellcheck disable=SC2154

# 自描述標頭每一行的前綴（engine/shell 的 HEADER_PREFIX）。
vk_main_header_prefix='# vendor_kit-shell '
# vk_main_reason_pending：還沒有專屬原因代碼的情況，reason 後面附的說明。
vk_main_reason_pending='reason code pending (draft VK0070, N76)'

# vk_main_header <file>：讀 file 開頭的自描述標頭，介面版放進 vk_main_proto、引擎版放進 vk_main_version。
# 讀不出就印 VK0056、回 1。
vk_main_header() {
    local file=$1 line1='' line2=''
    vk_main_proto=
    vk_main_version=
    {
        IFS= read -r line1
        IFS= read -r line2
    } 2>/dev/null <"$file"
    line1=${line1%$'\r'}
    line2=${line2%$'\r'}
    local proto=${line1#"${vk_main_header_prefix}interface "}
    local version=${line2#"${vk_main_header_prefix}engine "}
    if [[ $proto == "$line1" || ! $proto =~ $vk_wire_re_proto ]]; then
        vk_diag VK0056 reason "cannot read the interface version from the self-describing header of $file" path none
        return 1
    fi
    if [[ $version == "$line2" || ! $version =~ ^[!-~]+$ ]]; then
        vk_diag VK0056 reason "cannot read the engine version from the self-describing header of $file" path none
        return 1
    fi
    vk_main_proto=$proto
    vk_main_version=$version
    return 0
}

# vk_main_recipe <version.toml>：版本鎖定行裡引擎那一行的值（pinned 引用）放進 REPLY。
# 讀法在 host.sh 的 vk_lock_engine_ref（bootstrap.sh 共用）；讀不出時印 VK0056、回 1。
vk_main_recipe() {
    if ! vk_lock_engine_ref "$1"; then
        vk_diag VK0056 reason "$REPLY; $vk_main_reason_pending" path none
        return 1
    fi
    return 0
}

# vk_main <host_root> <host_cwd> [<recipe> <args>...]：薄殼的 VK recipe。標頭從這個函式所在的檔
# （組好的 log.sh）讀，引擎引用從 <host_root>/.vendor_kit/version.toml 讀，再交給 vk_launch。
# 回傳整次的結束碼。
vk_main() {
    if (($# < 2)); then
        vk_diag VK0056 reason "log.sh needs the install directory and the working directory" path none
        return "$vk_diag_exit"
    fi
    local root=$1 cwd=$2
    shift 2
    vk_main_header "${BASH_SOURCE[0]}" || return "$vk_diag_exit"
    vk_main_recipe "$root/.vendor_kit/version.toml" || return "$vk_diag_exit"
    local engine=$REPLY
    # shellcheck disable=SC2034 # log.sh 的 vk_log_line 讀它
    vk_log_version=$vk_main_version
    vk_launch "$root" "$cwd" "$engine" "$vk_main_proto" "$@"
}

if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
    vk_main "$@"
    exit "$?"
fi
