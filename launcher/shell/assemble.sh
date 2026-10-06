#!/usr/bin/env bash
# 薄殼模板的組裝（#372 的 N38）：把 msggen 的訊息片段與啟動器各檔組成薄殼 log.sh 的本文，連同其餘三份模板
# 放進 outdir。
#
# 用法：assemble.sh <messages fragment> <outdir>
#   outdir 裡寫出 entry.just、vendor.just、log.sh、.gitignore（檔名同 engine/layout 的 SHELL_FILES），
#   都是不含自描述標頭的模板本文；標頭由引擎寫進安裝目錄時加（engine/shell）。outdir 不在就建。
#
# - log.sh 的本文依 vk_assemble_shell_parts 的固定順序串起：訊息片段，接著 launcher/ 的 diag、host、log、
#   wire、launch、main。後面的檔用到前面定義的函式與變數；main.sh 放最後，以 bash 執行時才呼叫 vk_main。
# - 其餘三檔照原樣：launcher/shell/ 的 entry.just、vendor.just，gitignore 寫成 .gitignore。
# - 輸出逐位元組決定（ADR-0012）：只把輸入原樣接起來，不加分隔、時間或路徑。每份輸入都要是一般檔、
#   不是空檔、不含 NUL、以 LF 結尾；任何一份不合就不寫那個檔、在 stderr 說明、以 1 結束。
# - vk_assemble 是通用的組裝函式：source 這個檔後呼叫（bootstrap.sh 的組裝共用），source 時不執行。
#
# 只用 bash 的 builtin 與 mkdir、mv（啟動器命令白名單內的命令）。

# log.sh 本文在訊息片段之後的各檔，依串接順序（launcher/ 下的檔名，不含 .sh）。
vk_assemble_shell_parts=(diag host log wire launch main)

# vk_assemble <out> <part>...：依參數順序把各檔原樣串起，寫成 out（先寫 out.tmp 再 mv）。不合回 1。
vk_assemble() {
    local out=$1 part content body=
    shift
    if (($# == 0)); then
        printf 'assemble: no input for %s\n' "$out" >&2
        return 1
    fi
    for part in "$@"; do
        if [[ ! -f $part || ! -r $part ]]; then
            printf 'assemble: cannot read %s\n' "$part" >&2
            return 1
        fi
        # read -d '' 讀到 NUL 才回 0；沒有 NUL 時讀完整檔（含結尾的換行）、回 1。
        if IFS= read -r -d '' content <"$part"; then
            printf 'assemble: %s has a NUL byte\n' "$part" >&2
            return 1
        fi
        if [[ $content != *$'\n' ]]; then
            printf 'assemble: %s is empty or does not end with LF\n' "$part" >&2
            return 1
        fi
        body+=$content
    done
    if ! { printf '%s' "$body" >"$out.tmp" && mv -f -- "$out.tmp" "$out"; } 2>/dev/null; then
        printf 'assemble: cannot write %s\n' "$out" >&2
        return 1
    fi
    return 0
}

# vk_assemble_shell <messages fragment> <outdir>：組出薄殼四檔的模板本文。
vk_assemble_shell() {
    if (($# != 2)); then
        printf 'usage: assemble.sh <messages fragment> <outdir>\n' >&2
        return 1
    fi
    local fragment=$1 outdir=$2 here
    here=${BASH_SOURCE[0]%/*}
    if [[ $here == "${BASH_SOURCE[0]}" ]]; then
        here=.
    fi
    local launcher=$here/.. name
    local -a parts=("$fragment")
    for name in "${vk_assemble_shell_parts[@]}"; do
        parts+=("$launcher/$name.sh")
    done
    if ! mkdir -p -- "$outdir" 2>/dev/null; then
        printf 'assemble: cannot create %s\n' "$outdir" >&2
        return 1
    fi
    vk_assemble "$outdir/log.sh" "${parts[@]}" || return 1
    vk_assemble "$outdir/entry.just" "$here/entry.just" || return 1
    vk_assemble "$outdir/vendor.just" "$here/vendor.just" || return 1
    vk_assemble "$outdir/.gitignore" "$here/gitignore" || return 1
    return 0
}

if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
    vk_assemble_shell "$@"
    exit "$?"
fi
