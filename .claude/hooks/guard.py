#!/usr/bin/env python3
"""PreToolUse hook：擋三類反覆發生的問題

檢查 A：Workflow inline 腳本放行但提醒改用命名 workflow；meta／resume 會壞的硬錯照擋
檢查 B：`codex exec` 一定要接 stdin 重導（否則無限卡住）
檢查 C：`git push` 的目標是 main 就擋掉（一律推分支，進 main 走 merge）
"""

import json
import sys
import re
import os
import shlex
import subprocess
from pathlib import Path


def strip_literals(script):
    """移除字串與註解內容（程式碼用）"""
    result = list(script)
    i = 0
    
    while i < len(result):
        ch = result[i]
        if ch == "'":
            result[i] = ' '
            i += 1
            while i < len(result):
                if result[i] == '\\' and i + 1 < len(result):
                    result[i] = ' '
                    result[i + 1] = ' '
                    i += 2
                elif result[i] == "'":
                    result[i] = ' '
                    i += 1
                    break
                elif result[i] == '\n':
                    i += 1
                else:
                    result[i] = ' '
                    i += 1
            continue
        elif ch == '"':
            result[i] = ' '
            i += 1
            while i < len(result):
                if result[i] == '\\' and i + 1 < len(result):
                    result[i] = ' '
                    result[i + 1] = ' '
                    i += 2
                elif result[i] == '"':
                    result[i] = ' '
                    i += 1
                    break
                elif result[i] == '\n':
                    i += 1
                else:
                    result[i] = ' '
                    i += 1
            continue
        elif ch == '`':
            result[i] = ' '
            i += 1
            while i < len(result):
                if result[i] == '\\' and i + 1 < len(result):
                    result[i] = ' '
                    result[i + 1] = ' '
                    i += 2
                elif result[i] == '`':
                    result[i] = ' '
                    i += 1
                    break
                elif result[i] == '\n':
                    i += 1
                else:
                    result[i] = ' '
                    i += 1
            continue
        elif ch == '/' and i + 1 < len(result) and result[i + 1] == '/':
            while i < len(result) and result[i] != '\n':
                result[i] = ' '
                i += 1
            continue
        elif ch == '/' and i + 1 < len(result) and result[i + 1] == '*':
            result[i] = ' '
            result[i + 1] = ' '
            i += 2
            while i < len(result) - 1:
                if result[i] == '*' and result[i + 1] == '/':
                    result[i] = ' '
                    result[i + 1] = ' '
                    i += 2
                    break
                elif result[i] == '\n':
                    i += 1
                else:
                    result[i] = ' '
                    i += 1
            continue
        else:
            i += 1
    
    return ''.join(result)


def strip_shell_data(command):
    """移除 shell 指令中的資料區段（heredoc 和字串內容，保留重導符號）"""
    result = list(command)
    i = 0
    
    while i < len(result):
        ch = result[i]
        
        if ch == "'":
            result[i] = ' '
            i += 1
            while i < len(result):
                if result[i] == "'":
                    result[i] = ' '
                    i += 1
                    break
                elif result[i] == '\n':
                    i += 1
                else:
                    result[i] = ' '
                    i += 1
            continue
        
        elif ch == '"':
            result[i] = ' '
            i += 1
            while i < len(result):
                if result[i] == '\\' and i + 1 < len(result) and result[i + 1] == '"':
                    result[i] = ' '
                    result[i + 1] = ' '
                    i += 2
                elif result[i] == '"':
                    result[i] = ' '
                    i += 1
                    break
                elif result[i] == '\n':
                    i += 1
                else:
                    result[i] = ' '
                    i += 1
            continue
        
        elif ch == '<' and i + 1 < len(result) and result[i + 1] == '<':
            j = i + 2
            
            if j < len(result) and result[j] == '-':
                j += 1
            while j < len(result) and result[j] in ' \t':
                j += 1
            
            delim_start = j
            delim_text = ''
            
            if j < len(result) and result[j] in '\'"':
                quote = result[j]
                j += 1
                while j < len(result) and result[j] != quote:
                    delim_text += result[j]
                    j += 1
                if j < len(result) and result[j] == quote:
                    j += 1
            else:
                while j < len(result) and result[j] not in ' \t\n':
                    delim_text += result[j]
                    j += 1
            
            if delim_text:
                eol = j
                while eol < len(result) and result[eol] != '\n':
                    eol += 1
                
                for k in range(i + 2, eol):
                    result[k] = ' '
                
                if eol < len(result):
                    i = eol + 1
                    while i < len(result):
                        line_start = i
                        line_end = i
                        while line_end < len(result) and result[line_end] != '\n':
                            line_end += 1
                        
                        line_text = command[line_start:line_end].strip()
                        if line_text == delim_text:
                            for k in range(line_start, line_end):
                                result[k] = ' '
                            i = line_end + 1 if line_end < len(result) else line_end
                            break
                        else:
                            for k in range(line_start, line_end):
                                result[k] = ' '
                            i = line_end + 1 if line_end < len(result) else line_end
                else:
                    i = eol
                continue
        
        else:
            i += 1
    
    return ''.join(result)


def load_workflow_meta(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'export\s+const\s+meta\s*=\s*\{([^}]*?(?:{[^}]*}[^}]*?)*)\}', content, re.DOTALL)
        if not match:
            return None
        meta_content = match.group(1)
        name_match = re.search(r"name:\s*['\"]([^'\"]+)['\"]", meta_content)
        desc_match = re.search(r"description:\s*['\"]([^'\"]+)['\"]", meta_content)
        name = name_match.group(1) if name_match else None
        desc = desc_match.group(1) if desc_match else None
        if name:
            return {"name": name, "description": desc}
        return None
    except Exception:
        return None


def list_workflows(workflows_dir):
    result = []
    try:
        workflows_path = Path(workflows_dir)
        if not workflows_path.exists():
            return result
        for js_file in sorted(workflows_path.glob('*.js')):
            meta = load_workflow_meta(str(js_file))
            if meta and meta['name']:
                result.append((meta['name'], meta['description']))
    except Exception:
        pass
    return result


def find_meta_range(script):
    match = re.search(r'export\s+const\s+meta\s*=\s*\{', script)
    if not match:
        return None
    start = match.end() - 1
    depth = 1
    i = start + 1
    while i < len(script) and depth > 0:
        if script[i] == '{':
            depth += 1
        elif script[i] == '}':
            depth -= 1
        i += 1
    return (start, i) if depth == 0 else None


def check_workflow(tool_input):
    if 'name' in tool_input or 'scriptPath' in tool_input:
        return None
    if 'script' not in tool_input:
        return None
    
    script = tool_input['script']
    
    masked_for_first = strip_literals(script)
    first_nonblank = 0
    for idx, ch in enumerate(masked_for_first):
        if ch not in ' \t\n':
            first_nonblank = idx
            break
    remainder = masked_for_first[first_nonblank:]
    if not re.match(r'export\s+const\s+meta\s*=', remainder):
        return ('deny', '第一個語句必須是 `export const meta`（容許前面有空行與註解）')
    
    meta_range = find_meta_range(script)
    if meta_range:
        meta_text = script[meta_range[0]:meta_range[1]]
        if '`' in meta_text:
            line_num = script[:meta_range[0]].count('\n') + 1
            return ('deny', f'meta 物件裡有 template literal（反引號，第 {line_num} 行起）；meta 必須是純字面值')
        if '${' in meta_text:
            line_num = script[:meta_range[0]].count('\n') + 1
            return ('deny', f'meta 物件裡有模板字串插值（第 {line_num} 行起）；meta 必須是純字面值')
    
    masked = strip_literals(script)
    
    forbidden_patterns = [
        (r'\bDate\.now\s*\(', 'Date.now('),
        (r'\bMath\.random\s*\(', 'Math.random('),
        (r'\bnew\s+Date\s*\(\s*\)', 'new Date()'),
    ]
    for pattern, name in forbidden_patterns:
        match = re.search(pattern, masked)
        if match:
            line_num = script[:match.start()].count('\n') + 1
            return ('deny', f'第 {line_num} 行有 `{name}`；這三個在 workflow 腳本會讓 resume 壞掉')
    
    ts_patterns = [
        (r'\binterface\s+\w+\s*\{', 'interface'),
        (r':\s*string\[\]', ': string[]'),
        (r'\bas\s+const\b', 'as const'),
    ]
    for pattern, name in ts_patterns:
        match = re.search(pattern, masked)
        if match:
            line_num = script[:match.start()].count('\n') + 1
            return ('deny', f'第 {line_num} 行有 TypeScript 語法 `{name}`；workflow 腳本必須是純 JavaScript')
    
    workflows_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.')) / '.claude' / 'workflows'
    existing = list_workflows(str(workflows_dir))
    
    # 使用者定案：inline 腳本不跳確認打擾人，改成放行、把提醒塞給 Claude 自己看。
    # 硬錯（上面那幾條 deny）照擋，只有這個「是不是該用命名 workflow」的提醒改成不擋。
    reason = '這是 inline 腳本，如果這個形狀會重複，請改用命名 workflow。\n'
    if existing:
        reason += '現有命名 workflow：'
        for name, desc in existing:
            reason += f'\n  • {name}'
            if desc:
                reason += f' — {desc}'
    reason += '\n真的是新形狀就照原樣跑，跑完把腳本存進 `.claude/workflows/<name>.js` 並在 `.claude/workflows/README.md` 補一列。'
    
    return ('remind', reason)


def get_repo_dir():
    """取得 repo 根目錄。優先 CLAUDE_PROJECT_DIR，否則 hook 檔往上兩層。"""
    proj_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', ''))
    if proj_dir.exists():
        return proj_dir
    hook_file = Path(__file__)
    return hook_file.parent.parent.parent


def get_git_status_summary(repo_dir):
    """跑 git status --porcelain，回傳改動摘要。失敗或逾時回傳 None。

    porcelain 的狀態是兩個字元 XY（X = 索引、Y = 工作區），第 3 個字元起是路徑。
    只看 X 會漏掉未 staged 的修改，只看 Y 會漏掉已 staged 的，所以兩個都要看。
    """
    # 列出來給人看的只取「真的要審的檔」：標示版與圖產生器的備份都是產生物或
    # 歷史快照，列進去會把前 10 個名額吃光、把該看的檔擠掉。計數仍然含它們。
    NOISE = (
        'doc/decisions/review/_marked/',
        'script/diagram/_backup/',
    )
    LIMIT = 10

    try:
        result = subprocess.run(
            ['git', '-C', str(repo_dir), 'status', '--porcelain'],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode != 0:
            return None

        lines = [l for l in result.stdout.split('\n') if l.strip()]
        if not lines:
            return '（無改動）'

        counts = {'改': 0, '新增': 0, '刪除': 0, '搬移': 0}
        interesting = []
        for line in lines:
            xy, path = line[:2], line[3:].strip('"')
            if ' -> ' in path:            # 搬移：舊路徑 -> 新路徑，只留新的
                path = path.split(' -> ', 1)[1].strip('"')

            if 'R' in xy:
                counts['搬移'] += 1
                continue                  # 搬移是位置變動，不需要逐檔審
            if 'D' in xy:
                counts['刪除'] += 1
                continue
            if xy == '??':
                counts['新增'] += 1
            elif 'M' in xy or 'A' in xy:
                counts['改'] += 1
            else:
                continue

            if not path.startswith(NOISE):
                interesting.append(path)

        summary = '待 commit 改動摘要：{} 項（{}）'.format(
            len(lines), ' '.join('{}:{}'.format(k, v) for k, v in counts.items() if v),
        )
        if interesting:
            summary += '\n  ' + '\n  '.join(interesting[:LIMIT])
            extra = len(interesting) - LIMIT
            if extra > 0:
                summary += '\n  …另外 {} 個'.format(extra)
        return summary

    except Exception:
        return None

def strip_heredoc_bodies(command):
    """只移除 heredoc（`<<` 到結束標記），引號與其他內容原樣保留，長度與換行不變。

    給拆詞用：引號要留著讓 shlex 正確切出帶空白的路徑，heredoc 本文是資料，不是指令。
    與 strip_shell_data 不同，heredoc 那一行在結束標記之後的指令（例如 `&& git push`）會保留。
    """
    result = list(command)
    n = len(command)
    i = 0
    while i < n:
        ch = command[i]
        if ch in '\'"':
            # 跳過引號內容（引號裡的 << 不是 heredoc）
            j = i + 1
            while j < n and command[j] != ch:
                if ch == '"' and command[j] == '\\':
                    j += 1
                j += 1
            i = j + 1
            continue
        if ch == '<' and command.startswith('<<', i) and not command.startswith('<<<', i):
            j = i + 2
            if j < n and command[j] == '-':
                j += 1
            while j < n and command[j] in ' \t':
                j += 1
            delim = ''
            if j < n and command[j] in '\'"':
                quote = command[j]
                j += 1
                while j < n and command[j] != quote:
                    delim += command[j]
                    j += 1
                j += 1
            else:
                while j < n and command[j] not in ' \t\n;&|<>()':
                    delim += command[j]
                    j += 1
            if not delim:
                i += 2
                continue
            for k in range(i, min(j, n)):
                result[k] = ' '
            # 本文從這一行的下一行開始，到單獨一行的結束標記為止
            eol = command.find('\n', j)
            if eol == -1:
                break
            k = eol + 1
            while k < n:
                line_end = command.find('\n', k)
                if line_end == -1:
                    line_end = n
                done = command[k:line_end].strip() == delim
                for m in range(k, line_end):
                    result[m] = ' '
                k = line_end + 1
                if done:
                    break
            i = k
            continue
        i += 1
    return ''.join(result)


# shell 的控制運算子：分隔出各段簡單指令
_SEPARATOR_CHARS = set(';&|()\n')
# git 自己的全域選項裡，值放在下一個字的那些（--opt=value 形式是單一個字，不在此列）
_GIT_GLOBAL_OPTS_WITH_VALUE = {
    '-C', '-c', '--git-dir', '--work-tree', '--namespace',
    '--config-env', '--super-prefix', '--exec-path',
}
# 放在指令前面、後面才是真正指令的包裝
_COMMAND_WRAPPERS = {'env', 'command', 'exec', 'time', 'nohup', 'sudo', 'builtin'}
# git push 的選項裡，值放在下一個字的那些
_PUSH_OPTS_WITH_VALUE = {'-o', '--push-option', '--repo', '--receive-pack', '--exec'}


def split_simple_commands(command):
    """把 shell 指令拆成各段簡單指令的字詞串列（以 ; && || | & ( ) 換行分段，去掉重導）。

    heredoc 本文先移除；引號內容由 shlex 正確處理，所以字串裡提到的 git push 只是某個字的一部分。
    """
    def tokenize(text):
        lex = shlex.shlex(text, posix=True, punctuation_chars=';&|()<>\n')
        lex.whitespace = ' \t\r'
        lex.whitespace_split = True
        lex.commenters = '#'
        return list(lex)

    text = strip_heredoc_bodies(command)
    try:
        tokens = tokenize(text)
    except ValueError:
        # 引號沒配對（shlex 解不開）：退回遮罩版，至少看得到引號外的指令
        tokens = tokenize(strip_shell_data(command))

    segments, current = [], []
    skip_next = False
    for tok in tokens:
        if skip_next:
            skip_next = False
            continue
        if tok and all(c in ';&|()<>\n' for c in tok):
            if tok[0] in '<>':
                skip_next = True       # 重導運算子與它的目標檔都不是指令參數
                continue
            if any(c in _SEPARATOR_CHARS for c in tok):
                if current:
                    segments.append(current)
                current = []
                continue
        current.append(tok)
    if current:
        segments.append(current)
    return segments


def parse_git_push(words):
    """一段簡單指令若是 git push，回傳 (-C 目錄串列, push 之後的參數)；否則 None。

    跳過前置的環境變數指定與 env／command 之類的包裝，再跳過 git 的全域選項
    （-C <dir>、-c <k=v>、--git-dir、--work-tree、--no-pager、-P …），才看子指令。
    """
    i = 0
    while i < len(words):
        w = words[i]
        if re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', w):
            i += 1
        elif w in _COMMAND_WRAPPERS:
            i += 1
            # 包裝自己的選項（env -i、sudo -u x 之類）不精確處理，只跳過以 - 開頭的字
            while i < len(words) and words[i].startswith('-'):
                i += 1
        else:
            break
    if i >= len(words) or os.path.basename(words[i]) != 'git':
        return None
    i += 1

    dirs = []
    while i < len(words) and words[i].startswith('-'):
        opt = words[i]
        if opt in _GIT_GLOBAL_OPTS_WITH_VALUE:
            if opt == '-C' and i + 1 < len(words):
                dirs.append(words[i + 1])
            i += 2
        else:
            i += 1
    if i >= len(words) or words[i] != 'push':
        return None
    return dirs, words[i + 1:]


def current_branch(dirs):
    """依 -C 目錄（相對於 repo 根目錄，可多個疊加）取當前分支；取不到回傳 None。"""
    base = Path(get_repo_dir())
    for d in dirs:
        base = base / d
    try:
        r = subprocess.run(
            ['git', '-C', str(base), 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True, text=True, timeout=5,
        )
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def push_targets_main(dirs, args):
    """回傳 (是否推到 main, 是否 force, 是否因「推當前分支而當前在 main」)。"""
    forced = False
    positionals = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == '--':
            positionals.extend(args[i + 1:])
            break
        if a.startswith('-'):
            if a in ('-f', '--force') or a.startswith('--force-with-lease'):
                forced = True
            elif re.match(r'^-[A-Za-z]+$', a) and 'f' in a[1:]:
                forced = True          # 合併的短選項，例如 -uf
            if a in _PUSH_OPTS_WITH_VALUE:
                i += 1
            i += 1
            continue
        positionals.append(a)
        i += 1

    refspecs = positionals[1:]          # 第一個位置參數是 remote
    if not refspecs:
        on_main = current_branch(dirs) == 'main'
        return on_main, forced, on_main

    for spec in refspecs:
        if spec.startswith('+'):
            forced = True
            spec = spec[1:]
        dst = spec.split(':', 1)[1] if ':' in spec else spec
        if dst in ('main', 'refs/heads/main'):
            return True, forced, False
        if ':' not in spec and spec == 'HEAD' and current_branch(dirs) == 'main':
            return True, forced, True
    return False, forced, False


def check_git(tool_input):
    """檢查 git push 的目標分支。

    規則（使用者定案）：commit 與 push 本身不需要詢問，但**一律不准 push 到 main**，
    force push 到 main 更不行。進 main 只能走 merge。所以這裡只擋目標是 main 的 push。

    指令先拆成各段簡單指令（管線、&&、; 都會分段），每段用 shlex 拆詞，
    跳過 git 的全域選項後才判斷子指令，所以 `git -C <dir> push origin main` 這類寫法也擋。
    字串與 heredoc 裡寫到 git push 不算。
    """
    command = tool_input.get('command', '')
    if 'git' not in command:
        return None

    for words in split_simple_commands(command):
        parsed = parse_git_push(words)
        if parsed is None:
            continue
        dirs, args = parsed
        targets_main, forced, via_current = push_targets_main(dirs, args)
        if not targets_main:
            continue
        why = 'force push 到 main' if forced else 'push 到 main'
        return ('deny', '不准 ' + why + '。這個 repo 的規則是一律 push 到分支，'
                        '進 main 只能走 merge。\n'
                        '先開分支：git switch -c <branch>，再 git push -u origin <branch>。'
                        + ('\n目前在 main 上，沒給 refspec 的 push 等於推 main。' if via_current else ''))

    return None

def has_pipe_before_codex(command):
    codex_match = re.search(r'\bcodex\s+exec\b', command)
    if not codex_match:
        return False
    codex_pos = codex_match.start()
    before_codex = command[:codex_pos]
    i = len(before_codex) - 1
    while i >= 0:
        if before_codex[i] == '|':
            if i + 1 < len(before_codex) and before_codex[i + 1] == '|':
                return False
            if i > 0 and before_codex[i - 1] == '|':
                return False
            return True
        i -= 1
    return False


def has_stdin_redirect_after_codex(command):
    """檢查 codex 之後有無重導。遮罩後的片段裡只要有 < 就算有重導（shell 語法）。"""
    codex_match = re.search(r'\bcodex\s+exec\b', command)
    if not codex_match:
        return False
    codex_end = codex_match.end()
    after_codex = command[codex_end:]
    masked_after = strip_literals(after_codex)
    return '<' in masked_after


def check_bash(tool_input):
    command = tool_input.get('command', '')
    
    masked_command = strip_shell_data(command)
    
    if 'codex exec' not in masked_command:
        return None
    
    if '--sandbox' in masked_command:
        return ('deny', '本 repo 的 `.codex/config.toml` 已設 `danger-full-access`；帶 `--sandbox` 會讓 bubblewrap 失敗，codex 零修改')
    
    has_pipe = has_pipe_before_codex(masked_command)
    has_redirect = has_stdin_redirect_after_codex(masked_command)
    
    if has_pipe or has_redirect:
        return None
    
    return ('deny', '`codex exec` 少了 stdin 重導會卡在等輸入；正確形狀是 `codex exec --skip-git-repo-check -C <dir> -o <out.md> "<brief>" < /dev/null` 或 `printf "%s" "$brief" | codex exec ...`')


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)
    
    try:
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        decision = None
        reason = None
        
        if tool_name == 'Workflow':
            result = check_workflow(tool_input)
            if result:
                decision, reason = result
        elif tool_name == 'Bash':
            result = check_git(tool_input)
            if result:
                decision, reason = result
            else:
                result = check_bash(tool_input)
                if result:
                    decision, reason = result
        
        if decision is None:
            sys.exit(0)
        
        if decision == 'remind':
            # 放行，但把提醒注入 Claude 的 context，不顯示成確認提示
            output = {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'allow',
                    'additionalContext': reason,
                }
            }
        else:
            output = {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': decision,
                    'permissionDecisionReason': reason,
                }
            }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    except Exception as e:
        sys.stderr.write(f'hook 錯誤（放行此次）：{e}\n')
        sys.exit(0)


if __name__ == '__main__':
    main()
