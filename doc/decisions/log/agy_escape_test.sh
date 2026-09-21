#!/bin/sh
# agy 版 json_escape（原樣照抄）
json_escape() {
  _TAB=$(printf '\t'); _CR=$(printf '\r'); _BS=$(printf '\b'); _FF=$(printf '\f')
  _clean_input=$(printf '%s\n' "$1" | tr -d '[\001-\007\013\016-\037]')
  _escaped=$(printf '%s' "$_clean_input" | sed \
    -e ':join' -e '$!{' -e 'N' -e 'bjoin' -e '}' \
    -e 's/\\/\\\\\\\\/g' \
    -e 's/"/\\"/g' \
    -e "s/$_TAB/\\\\t/g" \
    -e "s/$_CR/\\\\r/g" \
    -e "s/$_BS/\\\\b/g" \
    -e "s/$_FF/\\\\f/g" \
    -e 's/\n/\\n/g'
    printf 'x'
  )
  _escaped="${_escaped%x}"
  _escaped="${_escaped%\\n}"
  printf '%s' "$_escaped"
}
t() { printf '%s\t' "$1"; printf '{"v":"%s"}\n' "$(json_escape "$2")"; }
t backslash 'a\b'
t quote 'a"b'
t newline "$(printf 'a\nb')"
t tab "$(printf 'a\tb')"
t cr "$(printf 'a\rb')"
t ctrl1 "$(printf 'a\001b')"
t brackets 'a[b]c'
t utf8 '中文é😀'
t trailnl "$(printf 'a\n\n')"
t empty ''
t endslash 'a\'
