"""等 PR 的 CI 跑完並讀出結果（唯讀，只呼叫 `gh pr checks` 與 `gh run view`）。

用法：python3 script/workflow/wait_ci.py <pr> [--timeout 600] [--interval 15] [--repo ycpss91255-research/vendor_kit]
                                         [--failed-logs [--log-lines 80]]

每隔 interval 秒跑一次 `gh pr checks <pr> -R <repo> --json name,state,bucket,link`，直到每個 check 都結束
（bucket 不是 pending）或逾時。剛開 PR、還沒有任何 check 時算「還在跑」。

輸出一行 JSON：{"pr", "all_pass", "timed_out", "checks": [{"name", "state"}]}。
給 --failed-logs 時多一個 "failed_logs": [{"name", "run_id", "tail", "error"}]：每個失敗（fail／cancel）的
check 一筆；run id 從 check 的 link（`/actions/runs/<id>/`）取，每個 run 只跑一次
`gh run view <id> -R <repo> --log-failed`，tail 是最後 --log-lines 行（預設 80）。取不到 run id 或
gh run view 失敗時 run_id／tail 為 null，error 寫原因；成功時 error 為 null。沒有失敗時是空陣列。
沒給 --failed-logs 時輸出不變，也不呼叫 gh run view。
結束碼：全過 0；有失敗（fail／cancel）1；逾時 2；gh 本身出錯 3。skipping 算通過。取日誌失敗不改結束碼。
gh 的位置可用環境變數 WAIT_CI_GH 換掉（測試用）。
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

REPO = "ycpss91255-research/vendor_kit"
PASS = {"pass", "skipping"}
FAIL = {"fail", "cancel"}
NO_CHECKS = "no checks reported"
RUN_ID = re.compile(r"/actions/runs/(\d+)(?:/|$|\?|#)")


class GhError(Exception):
    pass


def gh_bin() -> str:
    return os.environ.get("WAIT_CI_GH", "gh")


def fetch(pr: str, repo: str) -> list[dict]:
    r = subprocess.run([gh_bin(), "pr", "checks", str(pr), "-R", repo, "--json", "name,state,bucket,link"],
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


def poll(pr, repo, timeout, interval, fetch_fn=fetch, sleep=time.sleep, clock=time.monotonic) -> tuple[list[dict], bool]:
    """輪詢到每個 check 都結束或逾時；回傳 (最後一次的 checks 原始資料, 是否逾時)。"""
    start = clock()
    while True:
        checks = fetch_fn(pr, repo)
        if done(checks):
            return checks, False
        if clock() - start >= timeout:
            return checks, True
        sleep(interval)


def wait(pr, repo, timeout, interval, fetch_fn=fetch, sleep=time.sleep, clock=time.monotonic) -> tuple[dict, int]:
    checks, timed_out = poll(pr, repo, timeout, interval, fetch_fn, sleep, clock)
    return finish(pr, checks, timed_out)


def finish(pr, checks, timed_out) -> tuple[dict, int]:
    res = result(pr, checks, timed_out)
    if timed_out:
        return res, 2
    return res, 0 if res["all_pass"] else 1


def result(pr, checks, timed_out) -> dict:
    all_pass = (not timed_out) and bool(checks) and all(c.get("bucket") in PASS for c in checks)
    return {"pr": int(pr), "all_pass": all_pass, "timed_out": timed_out,
            "checks": [{"name": c.get("name"), "state": c.get("state")} for c in checks]}


def run_log(run_id: str, repo: str) -> str:
    """跑 `gh run view <id> -R <repo> --log-failed`（唯讀）；失敗時 raise GhError。"""
    r = subprocess.run([gh_bin(), "run", "view", run_id, "-R", repo, "--log-failed"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise GhError(f"gh run view {run_id} 失敗（{r.returncode}）：{(r.stderr or r.stdout).strip()}")
    return r.stdout


def failed_logs(checks: list[dict], repo: str, lines: int, log_fn=run_log) -> list[dict]:
    """每個失敗的 check 一筆 {name, run_id, tail, error}；同一個 run 只取一次日誌。"""
    cache: dict[str, tuple[str | None, str | None]] = {}
    out = []
    for ch in checks:
        if ch.get("bucket") not in FAIL:
            continue
        m = RUN_ID.search(ch.get("link") or "")
        if not m:
            out.append({"name": ch.get("name"), "run_id": None, "tail": None,
                        "error": f"link 裡找不到 run id：{ch.get('link')!r}"})
            continue
        rid = m.group(1)
        if rid not in cache:
            try:
                text = log_fn(rid, repo)
                cache[rid] = ("\n".join(text.splitlines()[-lines:]), None)
            except GhError as e:
                cache[rid] = (None, str(e))
        tail, err = cache[rid]
        out.append({"name": ch.get("name"), "run_id": int(rid), "tail": tail, "error": err})
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="等 PR 的 CI 跑完")
    p.add_argument("pr")
    p.add_argument("--timeout", type=float, default=600)
    p.add_argument("--interval", type=float, default=15)
    p.add_argument("--repo", default=REPO)
    p.add_argument("--failed-logs", action="store_true", help="有失敗的 check 時附上 gh run view --log-failed 的尾段")
    p.add_argument("--log-lines", type=int, default=80, help="failed_logs 每個 run 留最後幾行（預設 80）")
    a = p.parse_args(argv)
    if not a.pr.isdigit():
        print(json.dumps({"error": f"PR 編號要是數字：{a.pr!r}"}, ensure_ascii=False))
        return 3
    if a.log_lines < 1:
        print(json.dumps({"error": f"--log-lines 要是正整數：{a.log_lines}"}, ensure_ascii=False))
        return 3
    try:
        checks, timed_out = poll(a.pr, a.repo, a.timeout, a.interval)
        res, code = finish(a.pr, checks, timed_out)
        if a.failed_logs:
            res["failed_logs"] = failed_logs(checks, a.repo, a.log_lines)
    except GhError as e:
        print(json.dumps({"pr": int(a.pr), "error": str(e)}, ensure_ascii=False))
        return 3
    print(json.dumps(res, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
