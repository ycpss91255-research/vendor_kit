#!/usr/bin/env bash
# 啟動器命令白名單 lint（ADR-0007:26、30）：launcher/*.sh 呼叫的每個命令，只能是 bash 的 builtin 或 keyword、
# 受檢檔自己定義的函式，或 commands.txt 列的命令；不合就列出並以 1 結束。
#
# 用法：check_commands.sh [--allow <commands.txt>] [<script>...]
#   不給 script 時檢查 launcher/*.sh；不給 --allow 時用同目錄的 commands.txt。
#
# 做法：不執行受檢檔。把整份檔包進一個函式定義（eval 只定義、不執行），再讀 `declare -f` 印出的
# 正規化原始碼，逐字元掃出每個簡單命令的第一個字。正規化後註解已去掉、每個命令一行，掃描只要處理
# 引號、`$(…)`、`<(…)`、`((…))`、`[[ … ]]`、case 的樣式行、指派與重導。
# 為了讓檢查判得出來，以下寫法直接算違規：命令位置是變數或含引號（動態命令）、反引號、heredoc、eval。
# 已知不看的地方：trap 與 `bash -c` 的字串內容（字串不是命令；要呼叫的命令照樣得寫在命令位置）。

set -u

lint_dir=$(cd -- "${BASH_SOURCE[0]%/*}" && pwd)
allow_file=$lint_dir/commands.txt
if [[ ${1:-} == --allow ]]; then
    allow_file=$2
    shift 2
fi
if (($# == 0)); then
    set -- "$lint_dir"/../*.sh
fi

declare -A allowed=() functions=()
while IFS= read -r line || [[ -n $line ]]; do
    line=${line%%#*}
    line=${line//[[:space:]]/}
    if [[ -n $line ]]; then
        allowed[$line]=1
    fi
done <"$allow_file"

problems=0
report() {
    printf '%s: %s\n' "$current" "$1"
    problems=$((problems + 1))
}

# 把檔讀成 declare -f 的正規化文字；語法錯也算違規。
normalized=()
for file in "$@"; do
    body=$(<"$file")
    if ! eval "__vk_lint_body() {
$body
}" 2>/dev/null; then
        current=$file
        report "syntax error (bash -n $file)"
        normalized+=("")
        continue
    fi
    text=$(declare -f __vk_lint_body)
    unset -f __vk_lint_body
    normalized+=("$text")
    while IFS= read -r line; do
        if [[ $line =~ ^[[:space:]]*(function\ )?([A-Za-z_][A-Za-z0-9_]*)\ \(\)\ *$ ]]; then
            functions[${BASH_REMATCH[2]}]=1
        fi
    done <<<"$text"
done

# 一個命令字的判定。
check_word() {
    local w=$1
    if [[ $w == *[\$\"\'\`\\*?]* ]]; then
        report "dynamic command word: $w"
        return
    fi
    if [[ $w == eval ]]; then
        report "eval is not allowed"
        return
    fi
    if [[ -n ${functions[$w]:-} || -n ${allowed[$w]:-} ]]; then
        return
    fi
    local t
    t=$(builtin type -t -- "$w" 2>/dev/null)
    if [[ $t == builtin || $t == keyword ]]; then
        return
    fi
    report "command not in ${allow_file##*/}: $w"
}

# 掃描狀態以深度 d 為索引：ctx（N＝程式碼、D＝雙引號、A＝陣列字面值、B＝程式碼裡的 ${…}）、
# cs（0＝不是命令位置、1＝命令位置、2＝command/builtin/exec 之後、下一個非選項字是命令）、
# wd（累積中的字）、br（在 [[ ]] 裡）、sk（for/case/select 到下一個分隔前不看）、tg（下一個字是重導目標）。
scan() {
    local s=$1
    local n=${#s} i=0 c d=0
    local -a ctx=(N) cs=(1) wd=("") br=(0) sk=(0) tg=(0)
    local case_depth=0 line_start=1

    finish_word() {
        local w=${wd[d]}
        wd[d]=
        if [[ -z $w ]]; then
            return
        fi
        if ((tg[d])); then
            tg[d]=0
            return
        fi
        if ((br[d])); then
            if [[ $w == ']]' ]]; then
                br[d]=0
                cs[d]=0
            fi
            return
        fi
        if ((sk[d])); then
            return
        fi
        if ((cs[d] == 0)); then
            return
        fi
        if ((cs[d] == 2)); then
            if [[ $w == -* ]]; then
                return
            fi
            cs[d]=0
            check_word "$w"
            return
        fi
        if [[ $w =~ ^[A-Za-z_][A-Za-z0-9_]*(\[[^]]*\])?\+?= ]]; then
            return
        fi
        case $w in
        if | then | else | elif | fi | do | done | while | until | '!' | '{' | '}' | time | 'esac')
            if [[ $w == 'esac' ]] && ((case_depth > 0)); then
                case_depth=$((case_depth - 1))
            fi
            return
            ;;
        case)
            case_depth=$((case_depth + 1))
            sk[d]=1
            return
            ;;
        for | select)
            sk[d]=1
            return
            ;;
        '[[')
            br[d]=1
            return
            ;;
        command | builtin | exec)
            cs[d]=2
            return
            ;;
        esac
        cs[d]=0
        check_word "$w"
    }

    separator() {
        finish_word
        cs[d]=1
        sk[d]=0
        tg[d]=0
    }

    push() {
        d=$((d + 1))
        ctx[d]=$1
        cs[d]=$2
        wd[d]=
        br[d]=0
        sk[d]=0
        tg[d]=0
    }

    pop() {
        finish_word
        d=$((d - 1))
    }

    # 從 i（指著第一個 `(`）跳過成對的括號，停在最後一個 `)`。
    skip_parens() {
        local depth=0
        while ((i < n)); do
            case ${s:i:1} in
            '(') depth=$((depth + 1)) ;;
            ')')
                depth=$((depth - 1))
                if ((depth == 0)); then
                    return
                fi
                ;;
            esac
            i=$((i + 1))
        done
    }

    while ((i < n)); do
        c=${s:i:1}
        local top=${ctx[d]}

        if [[ $top == D ]]; then
            case $c in
            "\\") i=$((i + 1)) ;;
            '"') d=$((d - 1)) ;;
            '`') report "backticks are not allowed" ;;
            '$')
                if [[ ${s:i+1:2} == '((' ]]; then
                    i=$((i + 1))
                    skip_parens
                elif [[ ${s:i+1:1} == '(' ]]; then
                    i=$((i + 1))
                    push N 1
                fi
                ;;
            esac
            i=$((i + 1))
            continue
        fi

        if [[ $top == B ]]; then
            case $c in
            '}') d=$((d - 1)) ;;
            '"') push D 0 ;;
            "'")
                i=$((i + 1))
                while ((i < n)) && [[ ${s:i:1} != "'" ]]; do i=$((i + 1)); done
                ;;
            '$')
                if [[ ${s:i+1:1} == '{' ]]; then
                    i=$((i + 1))
                    push B 0
                elif [[ ${s:i+1:1} == '(' ]]; then
                    i=$((i + 1))
                    push N 1
                fi
                ;;
            esac
            i=$((i + 1))
            continue
        fi

        # case 的樣式行：在 case 裡、行首、整行以 `)` 結尾且沒有其他括號。
        if ((line_start && case_depth > 0)) && [[ $c != [[:space:]] ]]; then
            local rest=${s:i}
            rest=${rest%%$'\n'*}
            if [[ $rest =~ ^[^\(\)]*\)[[:space:]]*$ && $rest != ';;'* ]]; then
                i=$((i + ${#rest}))
                continue
            fi
        fi
        if [[ $c != [[:space:]] ]]; then
            line_start=0
        fi

        # [[ ]] 裡只有空白分字，其他運算子都是字的一部分。
        if ((br[d])) && [[ $c != [[:space:]\"\'\$\\] ]]; then
            wd[d]+=$c
            i=$((i + 1))
            continue
        fi

        case $c in
        $'\n')
            if [[ $top == A ]]; then
                finish_word
            else
                separator
            fi
            line_start=1
            ;;
        ' ' | $'\t') finish_word ;;
        "\\")
            wd[d]+=${s:i:2}
            i=$((i + 1))
            ;;
        "'")
            local j=$((i + 1))
            while ((j < n)) && [[ ${s:j:1} != "'" ]]; do j=$((j + 1)); done
            wd[d]+=${s:i:j-i+1}
            i=$j
            ;;
        '"')
            wd[d]+='"'
            push D 0
            ;;
        '`') report "backticks are not allowed" ;;
        '$')
            local next=${s:i+1:1}
            if [[ ${s:i+1:2} == '((' ]]; then
                wd[d]+='$'
                i=$((i + 1))
                skip_parens
            elif [[ $next == '(' ]]; then
                wd[d]+='$'
                i=$((i + 1))
                push N 1
            elif [[ $next == '{' ]]; then
                wd[d]+='$'
                i=$((i + 1))
                push B 0
            elif [[ $next == "'" ]]; then
                local j=$((i + 2))
                while ((j < n)) && [[ ${s:j:1} != "'" ]]; do
                    if [[ ${s:j:1} == "\\" ]]; then j=$((j + 1)); fi
                    j=$((j + 1))
                done
                wd[d]+=${s:i:j-i+1}
                i=$j
            else
                wd[d]+='$'
            fi
            ;;
        ';' | '&' | '|')
            if [[ $c == '&' && ${s:i+1:1} == '>' ]]; then
                finish_word
                i=$((i + 1))
                if [[ ${s:i+1:1} == '>' ]]; then i=$((i + 1)); fi
                tg[d]=1
            else
                if [[ ${s:i+1:1} == "$c" || ($c == ';' && ${s:i+1:1} == '&') || ($c == '|' && ${s:i+1:1} == '&') ]]; then
                    i=$((i + 1))
                fi
                separator
            fi
            ;;
        '<' | '>')
            if [[ ${s:i+1:1} == '(' ]]; then
                finish_word
                tg[d]=0
                i=$((i + 1))
                push N 1
            else
                if [[ ${wd[d]} =~ ^[0-9]+$ ]]; then
                    wd[d]=
                fi
                finish_word
                if [[ $c == '<' && ${s:i+1:1} == '<' && ${s:i+2:1} != '<' ]]; then
                    report "heredocs are not allowed"
                fi
                while [[ ${s:i+1:1} == [\<\>\&\|] ]]; do i=$((i + 1)); done
                tg[d]=1
            fi
            ;;
        '(')
            if [[ ${wd[d]} == *= ]]; then
                push A 0
            elif [[ ${s:i+1:1} == '(' ]]; then
                finish_word
                skip_parens
            else
                finish_word
                push N 1
            fi
            ;;
        ')')
            if ((d > 0)); then
                pop
            else
                finish_word
            fi
            ;;
        *) wd[d]+=$c ;;
        esac
        i=$((i + 1))
    done
    finish_word
}

for idx in "${!normalized[@]}"; do
    current=${*:idx+1:1}
    scan "${normalized[idx]}"
done

if ((problems > 0)); then
    exit 1
fi
exit 0
