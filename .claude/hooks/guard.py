#!/usr/bin/env python3
"""PreToolUse hook：擋三類反覆發生的問題

檢查 A：Workflow 腳本必須走命名 workflow（避免 inline script 重複寫）
檢查 B：`codex exec` 一定要接 stdin 重導（否則無限卡住）
檢查 C：`git push` 的目標是 main 就擋掉（一律推分支，進 main 走 merge）
"""

import json
import sys
import re
import os
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
    
    reason = '這是 inline 腳本，如果這個形狀會重複，請改用命名 workflow。\n'
    if existing:
        reason += '現有命名 workflow：'
        for name, desc in existing:
            reason += f'\n  • {name}'
            if desc:
                reason += f' — {desc}'
    reason += '\n真的是新形狀就照原樣跑，跑完把腳本存進 `.claude/workflows/<name>.js` 並在 `.claude/workflows/README.md` 補一列。'
    
    return ('ask', reason)


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
    # 列出來給人看的只取「真的要審的檔」：備份、審查紀錄、標示版、歸檔都是產生物或
    # 歷史快照，列進去會把前 10 個名額吃光、把該看的檔擠掉。計數仍然含它們。
    NOISE = (
        'doc/decisions/_backup/',
        'doc/decisions/review_log/',
        'doc/decisions/review/_marked/',
        'doc/decisions/_legacy/',
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

def check_git(tool_input):
    """檢查 git push 的目標分支。

    規則（使用者定案）：commit 與 push 本身不需要詢問，但**一律不准 push 到 main**，
    force push 到 main 更不行。進 main 只能走 merge。所以這裡只擋目標是 main 的 push。

    判定用 strip_shell_data 遮罩後的指令，所以文件裡寫到 git push 不算。
    """
    command = tool_input.get('command', '')
    masked = strip_shell_data(command)

    m = re.search(r'\bgit\s+push\b', masked)
    if not m:
        return None

    after = masked[m.end():]
    forced = bool(re.search(r'(^|\s)(-f|--force|--force-with-lease\S*)(\s|$)', after))

    # 明寫 main 當目標：git push origin main / HEAD:main / main:main / +main / refs/heads/main
    targets_main = bool(re.search(r'(^|[\s:+])(main|refs/heads/main)(\s|$|:)', after))

    # 沒給 refspec 時推的是當前分支：當前分支是 main 就等於 push to main
    no_refspec = not re.search(r'(^|\s)[\w./+-]*:?[\w./+-]+(\s|$)',
                               re.sub(r'(^|\s)-{1,2}[\w-]+(=\S*)?', ' ', after).strip())
    on_main = False
    if no_refspec or not targets_main:
        try:
            r = subprocess.run(
                ['git', '-C', str(get_repo_dir()), 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True, text=True, timeout=5,
            )
            on_main = r.returncode == 0 and r.stdout.strip() == 'main'
        except Exception:
            on_main = False

    if targets_main or (no_refspec and on_main):
        why = 'force push 到 main' if forced else 'push 到 main'
        return ('deny', '不准 ' + why + '。這個 repo 的規則是一律 push 到分支，'
                        '進 main 只能走 merge。\n'
                        '先開分支：git switch -c <branch>，再 git push -u origin <branch>。'
                        + ('\n目前在 main 上，沒給 refspec 的 push 等於推 main。' if (no_refspec and on_main) else ''))

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
