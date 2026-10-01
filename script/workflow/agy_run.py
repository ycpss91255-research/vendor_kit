"""執行 agy 做一次調查：選模型、沿用既有輸出、先寫 .part 成功才改名、整理 stderr。

用法：python3 script/workflow/agy_run.py --cd <dir> --brief <brief 檔> --out <輸出檔>
                                         [--err <stderr 檔>] [--model <名>] [--timeout 0]

- --out 已存在且非空：不執行 agy，回報 reused=true。
- 沒給 --model：跑 `agy models`，取第一欄符合 `^gemini-[0-9.]+-flash-high$` 的名稱，
  依版本號取最新；找不到就失敗。
- 執行 `agy --model <M> -p <brief 全文>`（工作目錄＝--cd）。stdout 先寫到 <out>.part，
  agy 結束碼 0 且輸出非空才改名成 <out>；其他情況（失敗、輸出空、逾時、被中斷）刪掉 .part，
  所以不會留下會被下次當成「已存在且非空」沿用的半成品。
- stderr 寫到 --err（預設 <out 去副檔名>.err），結束時是空的就刪掉。
- --timeout 秒數，0（預設）表示不設上限。相對路徑以目前目錄為準，不是 --cd。
- agy 執行檔預設 `agy`，環境變數 AGY_BIN 可換（測試用）。

輸出一行 JSON：{"ok", "exit", "model", "reused", "out", "out_bytes", "timed_out", "err_tail", "error"}。
exit 是 agy 的結束碼（沒跑到 agy 時為 null，沿用時為 0）；err_tail 是 stderr 最後 20 行。
結束碼：0 成功或沿用；1 agy 結束碼非 0；2 輸出空；3 逾時；4 用法錯或 brief 不存在；5 找不到模型。
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

MODEL_RE = re.compile(r"^gemini-([0-9.]+)-flash-high$")
TAIL = 20


class UsageError(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def agy_bin() -> str:
    return os.environ.get("AGY_BIN", "agy")


def version_key(v: str) -> tuple:
    return tuple(int(x) for x in v.split(".") if x.isdigit())


def pick_model(timeout) -> tuple[str | None, str]:
    """回傳 (模型名, 錯誤訊息)；找不到時模型名為 None。"""
    try:
        r = subprocess.run([agy_bin(), "models"], capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        return None, f"找不到 agy 執行檔：{agy_bin()}"
    except subprocess.TimeoutExpired:
        return None, "agy models 逾時"
    found = []
    for line in r.stdout.splitlines():
        cols = line.split()
        if cols:
            m = MODEL_RE.match(cols[0])
            if m:
                found.append((version_key(m.group(1)), cols[0]))
    if not found:
        detail = f"（agy models 結束碼 {r.returncode}：{r.stderr.strip()[-200:]}）" if r.returncode else ""
        return None, f"找不到 gemini flash-high 模型{detail}"
    return max(found)[1], ""


def tail(path: Path) -> str:
    try:
        return "\n".join(path.read_text(errors="replace").splitlines()[-TAIL:])
    except OSError:
        return ""


def run(a) -> tuple[dict, int]:
    out = Path(a.out)
    err = Path(a.err) if a.err else out.with_suffix(".err")
    res = {"ok": False, "exit": None, "model": a.model or "", "reused": False, "out": str(out),
           "out_bytes": 0, "timed_out": False, "err_tail": "", "error": ""}

    if out.is_file() and out.stat().st_size > 0:
        res.update(ok=True, exit=0, reused=True, out_bytes=out.stat().st_size)
        return res, 0

    brief = Path(a.brief)
    if not brief.is_file():
        res["error"] = f"brief 不存在：{brief}"
        return res, 4
    if not Path(a.cd).is_dir():
        res["error"] = f"--cd 不是目錄：{a.cd}"
        return res, 4
    if a.timeout < 0:
        res["error"] = "--timeout 不能是負數"
        return res, 4
    timeout = a.timeout or None

    model = a.model
    if not model:
        model, msg = pick_model(timeout)
        if not model:
            res["error"] = msg
            return res, 5
        res["model"] = model

    part = out.with_name(out.name + ".part")
    out.parent.mkdir(parents=True, exist_ok=True)
    err.parent.mkdir(parents=True, exist_ok=True)
    code = None
    try:
        with open(part, "wb") as fo, open(err, "wb") as fe:
            try:
                p = subprocess.run([agy_bin(), "--model", model, "-p", brief.read_text()],
                                   cwd=a.cd, stdout=fo, stderr=fe, timeout=timeout)
                res["exit"] = p.returncode
            except FileNotFoundError:
                res["error"] = f"找不到 agy 執行檔：{agy_bin()}"
                code = 1
            except subprocess.TimeoutExpired:
                res["timed_out"] = True
                res["error"] = f"agy 超過 {a.timeout:g} 秒"
                code = 3
        size = part.stat().st_size
        if code is None:
            if res["exit"] != 0:
                code = 1
                res["error"] = f"agy 結束碼 {res['exit']}"
            elif size == 0:
                code = 2
                res["error"] = "agy 輸出是空的"
            else:
                os.replace(part, out)
                res.update(ok=True, out_bytes=size)
                code = 0
    finally:
        part.unlink(missing_ok=True)
        res["err_tail"] = tail(err)
        if err.is_file() and err.stat().st_size == 0:
            err.unlink()
    return res, code


def main(argv=None) -> int:
    p = Parser(description="執行 agy 做一次調查")
    p.add_argument("--cd", required=True)
    p.add_argument("--brief", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--err")
    p.add_argument("--model", default="")
    p.add_argument("--timeout", type=float, default=0)
    try:
        a = p.parse_args(argv)
    except UsageError as e:
        print(json.dumps({"ok": False, "exit": None, "model": "", "reused": False, "out": "",
                          "out_bytes": 0, "timed_out": False, "err_tail": "", "error": str(e)},
                         ensure_ascii=False))
        return 4
    a.model = a.model.strip()
    res, code = run(a)
    print(json.dumps(res, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
