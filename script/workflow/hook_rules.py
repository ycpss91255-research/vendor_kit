"""共用 .claude/hooks/ 的規則，給 script/workflow/ 等腳本 import；也讓腳本的 gh／git 寫入先過同一批 hook。

用途：
  1. 規則共用：本文自檢（body.py）、留言檔準備（prepare_comment.py）要跟 hook 用同一套規則
     （本機絕對路徑樣式、留言標記、[codex]／[agy] 原文的註記行）；merge 前的署名檢查（merge_pr.py）
     要跟 attribution_guard.py 用同一組 BANNED。規則只寫在 hook 裡，
     這裡直接載入 hook 模組再匯出，不另抄一份；hook 改了，這些腳本自動跟著變。
  2. 寫入前的關卡：腳本內部執行的 gh／git 指令，Claude 的 PreToolUse hook 看不到
     （hook 只看到 `python3 <腳本>` 這一行），所以腳本在寫入前用 precheck 把即將執行的
     同一個 argv 交給 .claude/settings.json 註冊的每支 Bash hook，用 hook 自己的入口跑；
     guarded_run 過了 precheck 才執行。被擋、hook 報錯、逾時、輸出看不懂都不放行（fail closed）。

用法（模組）：
  import hook_rules
  hook_rules.LOCAL_PATHS            # ((compiled re, 標籤), ...)
  hook_rules.tagged(text)           # 第一行是否以 [claude]／[codex]／[agy] 開頭
  hook_rules.local_path_problem(text, src, raw_ok)
  hook_rules.BANNED                 # attribution_guard.py 的 Claude 署名樣式（compiled re）
  hook_rules.load(path, names)      # 從指定路徑載入 hook 模組（測試用）
  hook_rules.bash_hooks(settings=None)          # PreToolUse 裡 matcher 對得上 Bash 的 hook 指令
  hook_rules.precheck(argv, cwd)                # 用全部 Bash hook 檢查 argv，回傳 dict
  hook_rules.guarded_run(argv, cwd, bin_env=…)  # precheck 過了才執行 argv，回傳 dict

用法（命令列，給主對話與除錯用）：
  python3 script/workflow/hook_rules.py precheck [--cwd <dir>] -- <argv…>
  例：python3 script/workflow/hook_rules.py precheck -- gh issue comment 1 --body-file x.md

匯出：LOCAL_PATHS、TAGS、RAW_TAGS、NOTE_PREFIXES、tagged、local_path_problem（comment_tag_guard）；
BANNED（attribution_guard）；bash_hooks、precheck、guarded_run。

bash_hooks：讀這支腳本所在 repo 的 .claude/settings.json（或 settings 給的路徑／dict），
  取 PreToolUse 裡 matcher 用 re.fullmatch 對得上 "Bash" 的每個 hook 的 command 字串，
  順序照檔案；matcher 空或沒給算全部對得上。不寫死清單，之後新增的 Bash hook 自動涵蓋。

precheck 回傳 {"ok", "command", "denied": [{"hook", "decision", "reason"}], "errors": [{"hook", "error"}]}：
  command＝shlex.join(argv)，argv[0] 取檔名（字面的 gh 或 git，hook 才認得）。每支 hook 用 shell
  執行它的 command 字串，CLAUDE_PROJECT_DIR＝project_dir（不給沿用環境變數，再沒有用這個 repo 的根目錄），
  cwd＝cwd，stdin 是 Claude Code 給 PreToolUse hook 的同一種 JSON。判讀：
  stdout 空且結束碼 0＝放行；stdout 是 JSON 且 permissionDecision 是 allow＝放行；
  deny 或 ask＝擋（ask 也算擋：腳本裡沒有人可以回答）；結束碼 2＝擋（理由取 stderr）；
  其他非 0 結束碼、逾時、stdout 不是 JSON、JSON 裡沒有 permissionDecision＝錯誤，同樣不放行。
  ok＝denied 與 errors 都是空的。

guarded_run 回傳：被擋 {"ok": false, "ran": false, "precheck"}；執行了
  {"ok": returncode == 0, "ran": true, "returncode", "stdout", "stderr", "precheck"}；
  執行檔找不到 {"ok": false, "ran": false, "error", "precheck"}。不經 shell 執行；
  有給 bin_env 且該環境變數有值時 argv[0] 換成它（測試用來換假 gh），precheck 仍用字面的 argv[0]。
  其他寫入腳本一律經 guarded_run，不自己呼叫 subprocess 做寫入。

命令列輸出一行 precheck 的 JSON（ensure_ascii=False）；用法錯時 {"ok": false, "error"}。
結束碼：ok 0；被擋或錯誤 1；用法錯 2。

錯誤：hook 檔不存在或載入失敗時 raise HookRulesError，訊息寫明找不到哪個檔；
不會退回自己的副本。settings.json 讀不到或格式不對時 bash_hooks 也 raise HookRulesError；
precheck 把它記進 errors，不放行。
"""
import importlib.util
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".claude/hooks/comment_tag_guard.py"
SETTINGS = ROOT / ".claude/settings.json"
NAMES = ("LOCAL_PATHS", "TAGS", "RAW_TAGS", "NOTE_PREFIXES", "tagged", "local_path_problem")
ATTRIBUTION_HOOK = HOOK.with_name("attribution_guard.py")
ATTRIBUTION_NAMES = ("BANNED",)


class HookRulesError(ImportError):
    """載不到 hook 檔的規則。"""


def load(path: Path = HOOK, names: tuple = NAMES):
    """載入 path 指到的 hook 模組並回傳；缺檔或缺 names 裡的名稱就 raise HookRulesError。"""
    path = Path(path)
    if not path.is_file():
        raise HookRulesError(f"找不到 hook 檔：{path}")
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise HookRulesError(f"無法載入 hook 檔：{path}")
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:  # noqa: BLE001 — 任何載入錯誤都換成同一種例外
        raise HookRulesError(f"載入 hook 檔失敗：{path}：{e}") from e
    missing = [n for n in names if not hasattr(mod, n)]
    if missing:
        raise HookRulesError(f"hook 檔 {path} 缺少：{'、'.join(missing)}")
    return mod


hook = load()
LOCAL_PATHS = hook.LOCAL_PATHS
TAGS = hook.TAGS
RAW_TAGS = hook.RAW_TAGS
NOTE_PREFIXES = hook.NOTE_PREFIXES
tagged = hook.tagged
local_path_problem = hook.local_path_problem

attribution = load(ATTRIBUTION_HOOK, ATTRIBUTION_NAMES)
BANNED = attribution.BANNED


def bash_hooks(settings=None) -> list[str]:
    """PreToolUse 裡 matcher 對得上 "Bash" 的每個 hook 的 command 字串，順序照檔案。

    settings 可以是 settings.json 的路徑或已讀好的 dict；不給用這個 repo 的 .claude/settings.json。
    """
    if settings is None or isinstance(settings, (str, Path)):
        path = Path(settings) if settings is not None else SETTINGS
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            raise HookRulesError(f"讀不到 settings：{path}：{e}") from e
    else:
        data = settings
    if not isinstance(data, dict):
        raise HookRulesError("settings 不是 JSON 物件")
    groups = (data.get("hooks") or {}).get("PreToolUse") or []
    commands = []
    for group in groups:
        matcher = group.get("matcher") or ""
        try:
            hit = matcher in ("", "*") or re.fullmatch(matcher, "Bash")
        except re.error as e:
            raise HookRulesError(f"matcher 不是合法的正規表示式：{matcher!r}：{e}") from e
        if not hit:
            continue
        for h in group.get("hooks") or []:
            if h.get("type", "command") == "command" and h.get("command"):
                commands.append(h["command"])
    return commands


def hook_name(command: str) -> str:
    """hook 指令字串的簡稱：最後一個參數的檔名（例如 guard.py）；拆不開就回原字串。"""
    try:
        toks = shlex.split(command)
    except ValueError:
        return command
    return Path(toks[-1]).name if toks else command


def judge(returncode: int, stdout: str, stderr: str):
    """回傳 ("allow", None)、("deny"/"ask", 理由) 或 ("error", 說明)。"""
    if returncode == 2:
        return "deny", stderr.strip() or "hook 以結束碼 2 擋下"
    if returncode != 0:
        return "error", f"hook 結束碼 {returncode}：{stderr.strip()}"
    out = stdout.strip()
    if not out:
        return "allow", None
    try:
        data = json.loads(out)
    except ValueError:
        return "error", f"hook 輸出不是 JSON：{out[:200]}"
    if not isinstance(data, dict):
        return "error", f"hook 輸出不是 JSON 物件：{out[:200]}"
    spec = data.get("hookSpecificOutput") or {}
    decision = spec.get("permissionDecision") if isinstance(spec, dict) else None
    if decision == "allow":
        return "allow", None
    if decision in ("deny", "ask"):
        return decision, spec.get("permissionDecisionReason") or ""
    if decision is None:
        return "error", f"hook 輸出的 JSON 沒有 permissionDecision：{out[:200]}"
    return "error", f"看不懂的 permissionDecision：{decision!r}"


def precheck(argv, cwd, *, settings=None, project_dir=None, timeout=60) -> dict:
    """把 argv 交給每支 Bash hook 檢查；任何一支擋或出錯就 ok false（fail closed）。"""
    argv = [str(a) for a in argv]
    if argv:
        argv[0] = Path(argv[0]).name
    command = shlex.join(argv)
    cwd = Path(cwd).resolve()
    result = {"ok": False, "command": command, "denied": [], "errors": []}
    if not argv:
        result["errors"].append({"hook": None, "error": "argv 是空的"})
        return result
    try:
        hooks = bash_hooks(settings)
    except HookRulesError as e:
        result["errors"].append({"hook": None, "error": str(e)})
        return result
    if not hooks:
        result["errors"].append({"hook": None, "error": "settings 裡沒有任何 Bash hook，無法確認"})
        return result
    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = str(project_dir or os.environ.get("CLAUDE_PROJECT_DIR") or ROOT)
    stdin = json.dumps({
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": str(cwd),
    }, ensure_ascii=False)
    for hook in hooks:
        name = hook_name(hook)
        try:
            r = subprocess.run(hook, shell=True, cwd=cwd, env=env, input=stdin,
                               capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            result["errors"].append({"hook": name, "error": f"逾時（{timeout} 秒）"})
            continue
        except OSError as e:
            result["errors"].append({"hook": name, "error": f"無法執行：{e}"})
            continue
        decision, detail = judge(r.returncode, r.stdout, r.stderr)
        if decision == "error":
            result["errors"].append({"hook": name, "error": detail})
        elif decision != "allow":
            result["denied"].append({"hook": name, "decision": decision, "reason": detail})
    result["ok"] = not result["denied"] and not result["errors"]
    return result


def guarded_run(argv, cwd, *, bin_env=None, settings=None, project_dir=None) -> dict:
    """precheck 過了才執行 argv（不經 shell）；被擋就不執行。"""
    argv = [str(a) for a in argv]
    check = precheck(argv, cwd, settings=settings, project_dir=project_dir)
    if not check["ok"]:
        return {"ok": False, "ran": False, "precheck": check}
    run = list(argv)
    if bin_env and os.environ.get(bin_env):
        run[0] = os.environ[bin_env]
    try:
        r = subprocess.run(run, cwd=cwd, capture_output=True, text=True)
    except OSError as e:
        return {"ok": False, "ran": False, "error": f"無法執行 {run[0]}：{e}", "precheck": check}
    return {"ok": r.returncode == 0, "ran": True, "returncode": r.returncode,
            "stdout": r.stdout, "stderr": r.stderr, "precheck": check}


USAGE = "用法：hook_rules.py precheck [--cwd <dir>] -- <argv…>"


def main(args=None) -> int:
    args = list(sys.argv[1:] if args is None else args)

    def usage(msg):
        print(json.dumps({"ok": False, "error": f"{msg}。{USAGE}"}, ensure_ascii=False))
        return 2

    if not args or args[0] != "precheck":
        return usage("第一個參數要是 precheck")
    if "--" not in args:
        return usage("要用 -- 隔開要檢查的指令")
    sep = args.index("--")
    opts, argv = args[1:sep], args[sep + 1:]
    if not argv:
        return usage("-- 後面沒有指令")
    cwd = os.getcwd()
    i = 0
    while i < len(opts):
        if opts[i] == "--cwd" and i + 1 < len(opts):
            cwd = opts[i + 1]
            i += 2
        elif opts[i].startswith("--cwd="):
            cwd = opts[i].split("=", 1)[1]
            i += 1
        else:
            return usage(f"看不懂的選項：{opts[i]}")
    if not Path(cwd).is_dir():
        return usage(f"--cwd 不是目錄：{cwd}")
    result = precheck(argv, cwd)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
