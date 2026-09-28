#!/bin/sh
# 修正版：純 POSIX sh + sed，RFC 8259 最小跳脫（\ " \b \t \n \f \r，其餘 U+0001–U+001F → \u00XX）
# 注意：NUL 無法存在於 shell 變數；結尾換行會被 $(...) 吃掉（呼叫端自行接受）。
_json_sed_script() {
  # 反斜線必須第一個處理
  printf '%s\n' 's/\\/\\\\/g' 's/"/\\"/g'
  _i=1
  while [ "$_i" -le 31 ]; do
    case "$_i" in
      10) ;;                                  # \n：由 N-loop 之後統一處理
      8)  _rep='\\b' ;; 9) _rep='\\t' ;; 12) _rep='\\f' ;; 13) _rep='\\r' ;;
      *)  _rep=$(printf '\\\\u%04x' "$_i") ;;
    esac
    if [ "$_i" -ne 10 ]; then
      _byte=$(printf "\\$(printf '%03o' "$_i")")
      printf 's/%s/%s/g\n' "$_byte" "$_rep"
    fi
    _i=$((_i + 1))
  done
  printf '%s\n' 's/\n/\\n/g'
}
JSON_SED_SCRIPT=$(_json_sed_script)

json_escape() {
  # 1. printf '%s\n' 保證 sed 拿到完整行；2. N-loop 把多行併成單一 pattern space；
  # 3. 套用跳脫；4. 以 x 哨兵保住結尾，再剝掉人為補上的 \n
  _e=$(printf '%s\n' "$1" | sed -e ':a' -e '$!{' -e 'N' -e 'ba' -e '}' -e "$JSON_SED_SCRIPT"; printf x)
  _e=${_e%x}
  _e=${_e%\\n}
  printf '%s' "$_e"
}

# ---- 測試 ----
t() { printf '%s\t' "$1"; printf '{"v":"%s"}\n' "$(json_escape "$2")"; }
t backslash 'a\b'
t quote 'a"b'
t newline "$(printf 'a\nb')"
t tab "$(printf 'a\tb')"
t cr "$(printf 'a\rb')"
t ctrl1 "$(printf 'a\001b')"
t ctrl1f "$(printf 'a\037b')"
t esc "$(printf 'a\033[0mb')"
t brackets 'a[b]c'
t slashn 'a\nb'
t utf8 '中文é😀'
t empty ''
t endslash 'a\'
t amp 'a&b/c'
t dash '-n foo'
