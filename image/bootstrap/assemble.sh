#!/usr/bin/env bash
# bootstrap.sh 的組裝（#372 的 N1）：把內嵌引用、msggen 的訊息片段與 launcher/ 各檔串成發佈用的 bootstrap.sh。
#
# 用法：assemble.sh <engine ref> <P> <messages fragment> <out>
#   engine ref 是內嵌引擎的 pinned 引用 `<registry>[:port]/<路徑>:vX.Y.Z@sha256:<64 位十六進位>`，P 是介面版（正整數）。
#   兩者格式不合、或任何一份輸入不合，就不寫 out、在 stderr 說明、以 1 結束。
#
# - 串接順序：開頭（shebang 與內嵌引用 vk_bootstrap_engine、vk_bootstrap_proto），接著訊息片段、launcher/ 的
#   diag、host、log、wire、launch、bootstrap_main。bootstrap_main.sh 放最後，以 bash 執行時才呼叫入口；
#   不放 main.sh（那是薄殼 log.sh 的入口）。
# - 串接用 launcher/shell/assemble.sh 的 vk_assemble（跟薄殼模板同一個組裝函式），輸出逐位元組決定（ADR-0012）。
# - 內嵌的訊息與代碼由 msggen --embedded 另外檢查（image/Dockerfile 的 test 與 bootstrap stage）。

set -euo pipefail

here=${BASH_SOURCE[0]%/*}
if [[ $here == "${BASH_SOURCE[0]}" ]]; then
    here=.
fi
launcher=$here/../../launcher
# shellcheck source=launcher/shell/assemble.sh
source "$launcher/shell/assemble.sh"

# bootstrap.sh 在訊息片段之後的各檔，依串接順序（launcher/ 下的檔名，不含 .sh）。
vk_bootstrap_parts=(diag host log wire launch bootstrap_main)

# 內嵌引用的格式（OCI image 引用）：第一段是 registry 的 host，可帶 :port；帶 port 時後面一定接 /路徑，
# 所以 port 的冒號後面是數字與 /，tag 的冒號後面是 vX.Y.Z 與 @，兩者分得開。
vk_bootstrap_re_part='[a-z0-9][a-z0-9._-]*'
vk_bootstrap_re_ref="^$vk_bootstrap_re_part((:[0-9]{1,5})?(/$vk_bootstrap_re_part)+)?"
vk_bootstrap_re_ref+=':v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)@sha256:[0-9a-f]{64}$'
vk_bootstrap_re_proto='^[1-9][0-9]{0,9}$'

main() {
    if (($# != 4)); then
        printf 'usage: assemble.sh <engine ref> <P> <messages fragment> <out>\n' >&2
        return 1
    fi
    local ref=$1 proto=$2 fragment=$3 out=$4 name
    if [[ ! $ref =~ $vk_bootstrap_re_ref ]]; then
        printf 'assemble: engine ref %s is not a pinned <registry>[:port]/<path>:vX.Y.Z@sha256:<digest> reference\n' "$ref" >&2
        return 1
    fi
    if [[ ! $proto =~ $vk_bootstrap_re_proto ]]; then
        printf 'assemble: interface version %s is not a positive integer\n' "$proto" >&2
        return 1
    fi
    # 兩個值的字元都在上面的格式內，不含引號，直接放進單引號。
    local head=$out.head
    if ! printf "#!/usr/bin/env bash\nvk_bootstrap_engine='%s'\nvk_bootstrap_proto='%s'\n" "$ref" "$proto" \
        >"$head" 2>/dev/null; then
        printf 'assemble: cannot write %s\n' "$head" >&2
        return 1
    fi
    local -a parts=("$head" "$fragment")
    for name in "${vk_bootstrap_parts[@]}"; do
        parts+=("$launcher/$name.sh")
    done
    local rc=0
    vk_assemble "$out" "${parts[@]}" || rc=1
    rm -f -- "$head"
    return "$rc"
}

main "$@"
