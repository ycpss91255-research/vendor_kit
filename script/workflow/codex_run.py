"""呼叫 codex 執行一份 brief，讀出結束碼與輸出檔狀態，結果寫成一行 JSON。

用法：python3 script/workflow/codex_run.py --cd <dir> --brief <brief 檔> --out <輸出檔> [--timeout 570] [--delete-brief] [--reuse]

執行 `codex exec --skip-git-repo-check -C <dir> -o <out> <brief 全文>`：
- stdin 一律接 /dev/null（不接的話 codex 會停在等 stdin）。
- 不帶任何 --sandbox 旗標（沙箱由 repo 的 .codex/config.toml 決定）。
- 執行前先建 <out> 的上層目錄。
- codex 執行檔預設 `codex`，可用環境變數 CODEX_BIN 換掉（測試用）。
- 結束碼由這支腳本直接讀，呼叫端的 shell 是 bash 還是 fish 都一樣。

--timeout 秒數（預設 570，讓前景 Bash 的 600000 毫秒上限內一定回得來）到了就砍掉 codex 的整個行程群組。
--delete-brief：結束後刪掉 brief 檔，不論成敗（含沿用）。
--reuse：<out> 已存在且非空就不執行 codex，回報 reused=true、ok=true、結束碼 0（brief 檔不必存在）。

輸出一行 JSON：{"ok", "exit", "out", "out_bytes", "timed_out", "elapsed_s", "stderr_tail",
"reused", "capacity", "error"}；
exit 是 codex 的結束碼（沒跑起來、逾時或沿用是 null），stderr_tail 是 codex stderr 的最後 2000 字元；
reused 表示沿用了既有輸出、沒執行 codex；capacity 表示 codex 的 stderr 含 `at capacity`（不分大小寫），
呼叫端可據此決定是否重試。
結束碼：0 成功（codex 結束碼 0 且輸出檔存在、非空）或沿用；1 codex 結束碼非 0 或跑不起來；
2 輸出檔不存在或是空的；3 逾時；4 brief 檔不存在或用法錯。
"""
import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_TIMEOUT = 570
TAIL = 2000


class UsageError(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def parse(argv):
    p = Parser(prog="codex_run.py", description="呼叫 codex 並回報結束碼")
    p.add_argument("--cd", required=True, help="codex 的工作目錄（-C）")
    p.add_argument("--brief", required=True, help="brief 檔，全文當成 codex 的 prompt")
    p.add_argument("--out", required=True, help="codex 的輸出檔（-o）")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="逾時秒數，預設 570")
    p.add_argument("--delete-brief", action="store_true", help="結束後刪掉 brief 檔")
    p.add_argument("--reuse", action="store_true", help="輸出檔已存在且非空就不執行 codex")
    return p.parse_args(argv)


def result(out=None, **kw):
    res = {"ok": False, "exit": None, "out": out, "out_bytes": 0, "timed_out": False,
           "elapsed_s": 0.0, "stderr_tail": "", "reused": False, "capacity": False,
           "error": None}
    res.update(kw)
    return res


def kill_group(proc):
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        proc.kill()


def has_output(out):
    path = Path(out)
    return path.is_file() and path.stat().st_size > 0


def run_codex(cd, brief_text, out, timeout):
    """跑 codex，回傳 (結果 dict, 結束碼)。"""
    out_path = Path(out)
    codex = os.environ.get("CODEX_BIN", "codex")
    cmd = [codex, "exec", "--skip-git-repo-check", "-C", cd, "-o", out, brief_text]
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return result(out, error=f"建不了輸出目錄：{e}"), 2
    start = time.monotonic()
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                stderr=subprocess.PIPE, start_new_session=True)
    except OSError as e:
        return result(out, error=f"codex 跑不起來：{e}"), 1
    timed_out = False
    try:
        _, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        kill_group(proc)
        _, err = proc.communicate()
    elapsed = round(time.monotonic() - start, 2)
    err_text = err.decode("utf-8", errors="replace")
    size = out_path.stat().st_size if out_path.is_file() else 0
    res = result(out, out_bytes=size, elapsed_s=elapsed, stderr_tail=err_text[-TAIL:],
                 timed_out=timed_out, capacity="at capacity" in err_text.lower())
    if timed_out:
        res["error"] = f"codex 超過 {timeout:g} 秒沒結束，已砍掉"
        return res, 3
    res["exit"] = proc.returncode
    if proc.returncode != 0:
        res["error"] = f"codex 結束碼 {proc.returncode}"
        return res, 1
    if size == 0:
        res["error"] = "輸出檔不存在" if not out_path.is_file() else "輸出檔是空的"
        return res, 2
    res["ok"] = True
    return res, 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        args = parse(argv)
        if args.timeout <= 0:
            raise UsageError("--timeout 要大於 0")
    except UsageError as e:
        res, code = result(error=f"用法錯：{e}"), 4
    else:
        brief = Path(args.brief)
        try:
            if args.reuse and has_output(args.out):
                res = result(args.out, ok=True, reused=True,
                             out_bytes=Path(args.out).stat().st_size)
                code = 0
            elif not brief.is_file():
                res, code = result(args.out, error=f"brief 檔不存在：{args.brief}"), 4
            else:
                text = brief.read_text(encoding="utf-8")
                res, code = run_codex(args.cd, text, args.out, args.timeout)
        finally:
            if args.delete_brief:
                try:
                    brief.unlink()
                except FileNotFoundError:
                    pass
    print(json.dumps(res, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
