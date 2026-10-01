"""等 PR 的 CI 跑完並讀出結果（唯讀，只呼叫 `gh pr checks`）。

用法：python3 script/workflow/wait_ci.py <pr> [--timeout 600] [--interval 15] [--repo ycpss91255-research/vendor_kit]

每隔 interval 秒跑一次 `gh pr checks <pr> -R <repo> --json name,state,bucket`，直到每個 check 都結束
（bucket 不是 pending）或逾時。剛開 PR、還沒有任何 check 時算「還在跑」。

輸出一行 JSON：{"pr", "all_pass", "timed_out", "checks": [{"name", "state"}]}。
結束碼：全過 0；有失敗（fail／cancel）1；逾時 2；gh 本身出錯 3。skipping 算通過。
gh 的位置可用環境變數 WAIT_CI_GH 換掉（測試用）。
"""
import argparse
import json
import os
import subprocess
import sys
import time

REPO = "ycpss91255-research/vendor_kit"
PASS = {"pass", "skipping"}
FAIL = {"fail", "cancel"}
NO_CHECKS = "no checks reported"


class GhError(Exception):
    pass


def fetch(pr: str, repo: str) -> list[dict]:
    gh = os.environ.get("WAIT_CI_GH", "gh")
    r = subprocess.run([gh, "pr", "checks", str(pr), "-R", repo, "--json", "name,state,bucket"],
                       capture_output=True, text=True)
    out = r.stdout.strip()
    if out.startswith("["):
        # gh 在有失敗或還在跑時結束碼不是 0，但 JSON 照樣輸出，以 JSON 為準
        return json.loads(out)
    if NO_CHECKS in (r.stderr + r.stdout):
        return []
    raise GhError(f"gh pr checks 失敗（{r.returncode}）：{(r.stderr or r.stdout).strip()}")


def done(checks: list[dict]) -> bool:
    return bool(checks) and all(c.get("bucket") != "pending" for c in checks)


def wait(pr, repo, timeout, interval, fetch_fn=fetch, sleep=time.sleep, clock=time.monotonic) -> tuple[dict, int]:
    start = clock()
    while True:
        checks = fetch_fn(pr, repo)
        if done(checks):
            break
        if clock() - start >= timeout:
            return result(pr, checks, timed_out=True), 2
        sleep(interval)
    res = result(pr, checks, timed_out=False)
    return res, 0 if res["all_pass"] else 1


def result(pr, checks, timed_out) -> dict:
    all_pass = (not timed_out) and bool(checks) and all(c.get("bucket") in PASS for c in checks)
    return {"pr": int(pr), "all_pass": all_pass, "timed_out": timed_out,
            "checks": [{"name": c.get("name"), "state": c.get("state")} for c in checks]}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="等 PR 的 CI 跑完")
    p.add_argument("pr")
    p.add_argument("--timeout", type=float, default=600)
    p.add_argument("--interval", type=float, default=15)
    p.add_argument("--repo", default=REPO)
    a = p.parse_args(argv)
    if not a.pr.isdigit():
        print(json.dumps({"error": f"PR 編號要是數字：{a.pr!r}"}, ensure_ascii=False))
        return 3
    try:
        res, code = wait(a.pr, a.repo, a.timeout, a.interval)
    except GhError as e:
        print(json.dumps({"pr": int(a.pr), "error": str(e)}, ensure_ascii=False))
        return 3
    print(json.dumps(res, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
