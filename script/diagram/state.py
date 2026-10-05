#!/usr/bin/env python3
"""透過 drawio MCP server 的 HTTP 端點讀寫頁面 XML，並比對前後兩份 .drawio（#138）。

用法：
  python3 script/diagram/state.py get   <out.drawio> [--url URL | --session-file FILE] [--timeout 秒]
  python3 script/diagram/state.py put   <in.drawio>  [--url URL | --session-file FILE] [--timeout 秒]
  python3 script/diagram/state.py check              [--url URL | --session-file FILE] [--timeout 秒]
  python3 script/diagram/state.py diff  <before.drawio> <after.drawio>

- get：GET /api/state?sessionId=<id>，把回傳的 xml 存成檔。session 失效時不寫檔。
- put：POST /api/state，body {"sessionId", "xml"}，回報 version。分頁會自己重新載入。
- check：判斷 session 是否失效：連不上，或 version == 1 加上預設空白頁
  <diagram id="blank" name="Page-1">。失效就結束碼 1 並說明，不自動開新頁。
- diff：每頁以 <diagram id> 對應，列出新增／刪除／改名的頁與每頁 cell 的增刪改；
  頁 id 消失或新出現另列在 id_changes，供「id 不准變」檢查用。

頁面網址（格式 http://localhost:<port>/?mcp=<session id>）來源，先到先用：
  --url；--session-file；預設是 workspace 的 reference/drawio_session.txt
  （workspace = 主 worktree 根目錄的上一層，從 linked worktree 跑也找得到）。

輸出一行 JSON 到 stdout。結束碼：0 過、1 有問題（連不上、session 失效、XML 壞掉）、2 用法錯（含找不到網址）。
只用 Python 標準函式庫，不呼叫 MCP、不開瀏覽器。
"""
import argparse
import base64
import json
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path

BLANK_ID = "blank"
BLANK_NAME = "Page-1"


class Fail(Exception):
    """結束碼 1：有問題。"""

    def __init__(self, reason, message, **extra):
        super().__init__(message)
        self.reason, self.message, self.extra = reason, message, extra


class Usage(Exception):
    """結束碼 2：用法錯。"""


# ---------- 頁面網址 ----------

def default_session_file() -> Path:
    """workspace 的 reference/drawio_session.txt；workspace 是主 worktree 根目錄的上一層。"""
    here = Path(__file__).resolve().parent
    root = here.parents[1]
    try:
        r = subprocess.run(["git", "-C", str(here), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                           capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            root = Path(r.stdout.strip()).parent
    except (OSError, subprocess.SubprocessError):
        pass
    return root.parent / "reference" / "drawio_session.txt"


def parse_page_url(url: str):
    """頁面網址 → (API 基底網址, session id)。localhost 換成 127.0.0.1。"""
    u = urllib.parse.urlsplit(url.strip())
    if u.scheme not in ("http", "https") or not u.hostname or not u.port:
        raise Usage(f"網址要像 http://localhost:<port>/?mcp=<session id>：{url.strip()!r}")
    sid = urllib.parse.parse_qs(u.query).get("mcp", [""])[0]
    if not sid:
        raise Usage(f"網址裡沒有 mcp=<session id>：{url.strip()!r}")
    host = "127.0.0.1" if u.hostname == "localhost" else u.hostname
    return f"{u.scheme}://{host}:{u.port}", sid


def resolve_session(args):
    if args.url:
        return parse_page_url(args.url)
    path = Path(args.session_file) if args.session_file else default_session_file()
    try:
        lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    except OSError:
        raise Usage(f"讀不到頁面網址檔 {path}；用 --url 或 --session-file 指定")
    if len(lines) != 1:
        raise Usage(f"頁面網址檔 {path} 要剛好一行網址，現在有 {len(lines)} 行")
    return parse_page_url(lines[0])


# ---------- HTTP ----------

def http_json(req, timeout):
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        raise Fail("http_error", f"drawio server 回 HTTP {e.code}", status=e.code)
    except (urllib.error.URLError, OSError) as e:
        raise Fail("unreachable", f"連不上 drawio server：{getattr(e, 'reason', e)}；"
                                  "請維護者在既有分頁重新取得網址，更新 reference/drawio_session.txt")
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise Fail("bad_response", "drawio server 回的不是 JSON")
    if not isinstance(data, dict):
        raise Fail("bad_response", "drawio server 回的 JSON 不是物件")
    return data


def fetch_state(base, sid, timeout):
    url = f"{base}/api/state?" + urllib.parse.urlencode({"sessionId": sid})
    data = http_json(urllib.request.Request(url, method="GET"), timeout)
    if not isinstance(data.get("xml"), str):
        raise Fail("bad_response", "drawio server 的回應沒有 xml 字串")
    return data


def post_state(base, sid, xml, timeout):
    body = json.dumps({"sessionId": sid, "xml": xml}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(f"{base}/api/state", data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    data = http_json(req, timeout)
    if data.get("success") is not True:
        raise Fail("rejected", "drawio server 沒有接受這份 XML", response=data)
    return data


# ---------- .drawio 解析 ----------

def _inflate(text):
    """壓縮過的 <diagram> 內容：base64 → raw deflate → URL decode。"""
    raw = zlib.decompress(base64.b64decode(text), -15).decode("utf-8")
    return urllib.parse.unquote(raw)


def parse_pages(xml: str, label: str):
    """回傳 [(page id, page name, {cell id: 正規化後的 XML})]，照檔內順序。"""
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        raise Fail("bad_xml", f"{label} 不是合法的 XML：{e}")
    diagrams = [root] if root.tag == "diagram" else root.findall("diagram")
    if root.tag not in ("mxfile", "diagram"):
        raise Fail("bad_xml", f"{label} 的根元素是 <{root.tag}>，不是 <mxfile>")
    pages, seen = [], set()
    for d in diagrams:
        pid, name = d.get("id"), d.get("name", "")
        if not pid:
            raise Fail("bad_xml", f"{label} 有一頁沒有 id（name={name!r}）")
        if pid in seen:
            raise Fail("bad_xml", f"{label} 的頁 id {pid!r} 重複")
        seen.add(pid)
        model = d.find("mxGraphModel")
        if model is None and (d.text or "").strip():
            try:
                model = ET.fromstring(_inflate(d.text.strip()))
            except (ValueError, zlib.error, UnicodeDecodeError, ET.ParseError):
                raise Fail("bad_xml", f"{label} 的頁 {pid!r} 內容解不開")
        cells = {}
        cell_root = model.find("root") if model is not None else None
        for el in (list(cell_root) if cell_root is not None else []):
            cid = el.get("id")
            if cid is None:
                continue
            if cid in cells:
                raise Fail("bad_xml", f"{label} 的頁 {pid!r} 的 cell id {cid!r} 重複")
            cells[cid] = ET.canonicalize(ET.tostring(el, encoding="unicode"), strip_text=True)
        pages.append((pid, name, cells))
    return pages


def read_drawio(path: str):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError as e:
        raise Usage(f"讀不到 {path}：{e.strerror}")


def is_blank(version, pages):
    return version == 1 and len(pages) == 1 and pages[0][0] == BLANK_ID and pages[0][1] == BLANK_NAME


def page_list(pages):
    return [{"id": pid, "name": name} for pid, name, _ in pages]


# ---------- 子指令 ----------

def live_state(args):
    """取目前頁面狀態；失效（空白頁）就丟 Fail。"""
    base, sid = resolve_session(args)
    data = fetch_state(base, sid, args.timeout)
    pages = parse_pages(data["xml"], "drawio server 回的 XML")
    version = data.get("version")
    if is_blank(version, pages):
        raise Fail("blank", f"session {sid} 是 version 1 的預設空白頁，表示原本的頁面已經不在；"
                            "請維護者在既有分頁重新取得網址，或用 put 重新載入檔案。不自動開新頁",
                   session=sid, version=version)
    return sid, data, pages


def cmd_check(args):
    sid, data, pages = live_state(args)
    return {"session": sid, "version": data.get("version"), "pages": page_list(pages)}


def cmd_get(args):
    sid, data, pages = live_state(args)
    out = Path(args.out)
    try:
        out.write_text(data["xml"], encoding="utf-8")
    except OSError as e:
        raise Fail("write_error", f"寫不進 {args.out}：{e.strerror}")
    return {"session": sid, "version": data.get("version"), "file": args.out, "pages": page_list(pages)}


def cmd_put(args):
    xml = read_drawio(args.file)
    pages = parse_pages(xml, args.file)
    if not pages:
        raise Fail("bad_xml", f"{args.file} 一頁都沒有")
    base, sid = resolve_session(args)
    data = post_state(base, sid, xml, args.timeout)
    return {"session": sid, "version": data.get("version"), "file": args.file, "pages": page_list(pages)}


def diff_pages(before, after):
    b = {pid: (name, cells) for pid, name, cells in before}
    a = {pid: (name, cells) for pid, name, cells in after}
    added = [{"id": pid, "name": a[pid][0]} for pid, _, _ in after if pid not in b]
    removed = [{"id": pid, "name": b[pid][0]} for pid, _, _ in before if pid not in a]
    renamed = [{"id": pid, "from": b[pid][0], "to": a[pid][0]}
               for pid, _, _ in after if pid in b and b[pid][0] != a[pid][0]]
    cells = {}
    for pid, _, _ in after:
        if pid not in b:
            continue
        bc, ac = b[pid][1], a[pid][1]
        ch = {"added": [c for c in ac if c not in bc],
              "removed": [c for c in bc if c not in ac],
              "changed": [c for c in ac if c in bc and ac[c] != bc[c]]}
        if any(ch.values()):
            cells[pid] = ch
    # 名字相同、id 不同：多半是 id 被換掉，另列方便追
    gone = {r["name"]: r["id"] for r in removed}
    same_name = [{"name": x["name"], "from_id": gone[x["name"]], "to_id": x["id"]}
                 for x in added if x["name"] in gone]
    id_changes = {"disappeared": [r["id"] for r in removed], "appeared": [x["id"] for x in added],
                  "same_name": same_name}
    changed = bool(added or removed or renamed or cells)
    return {"changed": changed, "pages": {"added": added, "removed": removed, "renamed": renamed},
            "cells": cells, "id_changes": id_changes}


def cmd_diff(args):
    before = parse_pages(read_drawio(args.before), args.before)
    after = parse_pages(read_drawio(args.after), args.after)
    return {"before": args.before, "after": args.after, **diff_pages(before, after)}


# ---------- 進入點 ----------

class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Usage(message)


def build_parser():
    p = Parser(prog="state.py", description="drawio 頁面 XML 的 HTTP 讀寫與前後比對（#138）")
    sub = p.add_subparsers(dest="cmd", required=True, parser_class=Parser)

    def session_opts(sp):
        g = sp.add_mutually_exclusive_group()
        g.add_argument("--url", help="頁面網址 http://localhost:<port>/?mcp=<session id>")
        g.add_argument("--session-file", help="只有一行頁面網址的檔（預設 workspace 的 reference/drawio_session.txt）")
        sp.add_argument("--timeout", type=float, default=10.0, help="HTTP 逾時秒數（預設 10）")

    sp = sub.add_parser("get", help="讀目前頁面 XML 存成檔")
    sp.add_argument("out")
    session_opts(sp)
    sp.set_defaults(func=cmd_get)
    sp = sub.add_parser("put", help="把 .drawio 檔載入頁面")
    sp.add_argument("file")
    session_opts(sp)
    sp.set_defaults(func=cmd_put)
    sp = sub.add_parser("check", help="判斷 session 是否失效")
    session_opts(sp)
    sp.set_defaults(func=cmd_check)
    sp = sub.add_parser("diff", help="比對兩份 .drawio")
    sp.add_argument("before")
    sp.add_argument("after")
    sp.set_defaults(func=cmd_diff)
    return p


def main(argv=None):
    cmd = None
    try:
        args = build_parser().parse_args(argv)
        cmd = args.cmd
        out, code = {"ok": True, "cmd": cmd, **args.func(args)}, 0
    except Usage as e:
        out, code = {"ok": False, "cmd": cmd, "reason": "usage", "message": str(e)}, 2
    except Fail as e:
        out, code = {"ok": False, "cmd": cmd, "reason": e.reason, "message": e.message, **e.extra}, 1
    print(json.dumps(out, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
