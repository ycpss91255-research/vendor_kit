"""準備要貼到 GitHub issue 的留言檔：標記、註記行、本機路徑替換、切分，並用 hook 的規則自檢。

用途：
  research 這類 workflow 要把 agy、codex 的原文與 Claude 的整合結論貼到 issue。
  留言檔的準備是固定規則，寫在這裡；會寫入 GitHub 的 `gh issue comment` 不在這裡下，
  由子代理逐則下（hook 要看得到指令）。標記、註記行與本機路徑的規則一律經
  hook_rules.py 取自 .claude/hooks/comment_tag_guard.py，不另抄一份。

用法：
  python3 script/workflow/prepare_comment.py prepare --out-dir <dir> --workspace <ws> \
      [--max 60000] --item <tag> <來源檔> <標題> [--item <tag> <來源檔> <標題> ...]
  python3 script/workflow/prepare_comment.py clean --out-dir <dir>

prepare：
- tag 只能是 hook 認得的標記去掉括號（claude、codex、agy）。
- 先刪掉 <dir> 裡舊的 post_*.md，再依 --item 的順序產生 <dir>/post_<NN>_<tag>.md；
  NN 兩位數、跨所有項目連號，檔名排序就是貼出順序。
- 每則第一行 `[<tag>] <標題>`，切成多則時標題後加「（k/n）」。
  原文標記（hook 的 RAW_TAGS，即 agy、codex）第二行固定加註記行
  「（註：以下是 <來源檔相對 workspace 的路徑> 的原文，未改寫。…）」，有換路徑時同一行寫明；
  claude 不加註記行。標頭之後空一行接本文。
- 本機路徑：`<ws>/` 換成相對 workspace 的寫法；其他符合 hook_rules.LOCAL_PATHS 的依 REPLACE
  （家目錄換成 `~/`、Claude scratchpad 換成 `<scratchpad>/`、Windows 使用者目錄換成 `~\\`），
  依 LOCAL_PATHS 的順序套用；其他字一個都不動。LOCAL_PATHS 有 REPLACE 沒涵蓋的樣式就算失敗。
- 切分：每則（含標頭）不超過 --max 字元；在行邊界切、優先切在空行；不在 ``` 程式碼區塊中間切，
  非切不可時在該則結尾補關閉、下一則開頭補開啟；單行超長才硬切。
- 自檢：每個產出檔用 hook_rules.tagged 與 hook_rules.local_path_problem(raw_ok=True) 檢查
  （hook 放行的條件）；另外整份不准再有任何 LOCAL_PATHS（替換後應該一個都不剩）。

clean：刪掉 <dir> 裡的 post_*.md。

輸出一行 JSON（ensure_ascii=False）：
  prepare：{"ok", "files": [{"path", "tag", "source", "part", "parts", "chars"}],
            "replaced": [{"source", "from", "to", "count"}], "problems": [...]}
  clean：{"ok", "removed": [...]}
結束碼：成功 0；有問題（來源檔讀不到、自檢不過）1；用法錯 2。
"""
import argparse
import json
import re
import sys
from pathlib import Path

import hook_rules

DEFAULT_MAX = 60000
FENCE = "```"
# hook_rules.LOCAL_PATHS 的標籤 → [(替換用的樣式, 換成)]，同一標籤內依序套用。
# 偵測樣式只認前綴，替換要吃掉整段目錄（例如 scratchpad 的 session 目錄），所以另寫替換樣式。
REPLACE = {
    "/home/<user>/": [(re.compile(r"/home/[^/\s]+/"), "~/")],
    "/Users/<user>/": [(re.compile(r"/Users/[^/\s]+/"), "~/")],
    "/tmp/claude-": [
        (re.compile(r"/tmp/claude-[^\s]*?/scratchpad/"), "<scratchpad>/"),
        (re.compile(r"/tmp/claude-[^/\s]*/?"), "<scratchpad>/"),
    ],
    "C:\\Users\\": [(re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\", re.IGNORECASE), "~\\")],
}


class UsageError(Exception):
    pass


def tag_names() -> list[str]:
    return [t.strip("[]") for t in hook_rules.TAGS]


def raw_tag_names() -> set[str]:
    return {t.strip("[]") for t in hook_rules.RAW_TAGS}


def replace_paths(text: str, workspace: str) -> tuple[str, list[dict], list[str]]:
    """回傳（替換後文字, [{from, to, count}], problems）。"""
    out, counts, problems = text, {}, []
    ws = workspace.rstrip("/\\") + "/"
    n = out.count(ws)
    if n:
        out = out.replace(ws, "")
        counts[(ws, "")] = n
    for _pat, label in hook_rules.LOCAL_PATHS:
        rules = REPLACE.get(label)
        if rules is None:
            problems.append(f"替換表沒有涵蓋 hook 的本機路徑樣式 {label}")
            continue
        for pat, to in rules:
            def sub(m, to=to):
                counts[(m.group(0), to)] = counts.get((m.group(0), to), 0) + 1
                return to
            out = pat.sub(sub, out)
    return out, [{"from": f, "to": t, "count": c} for (f, t), c in counts.items()], problems


def display_path(source: str, workspace: str) -> str:
    """來源檔相對 workspace 的寫法；不在 workspace 裡就套用同一張替換表。"""
    p, ws = Path(source).resolve(), Path(workspace).resolve()
    try:
        return p.relative_to(ws).as_posix()
    except ValueError:
        return replace_paths(str(p), workspace)[0]


def note_line(shown: str, replaced: list[dict]) -> str:
    extra = ""
    if replaced:
        extra = "原文的本機路徑已換成 workspace 相對路徑"
        if any(r["to"] for r in replaced):
            extra += "（workspace 外的換成 ~/、<scratchpad>/ 這類寫法）"
        extra += "。"
    return f"（註：以下是 {shown} 的原文，未改寫。{extra}）"


def is_fence(line: str) -> bool:
    return line.lstrip().startswith(FENCE)


def split_body(body: str, budget: int) -> list[str]:
    """把本文切成每段不超過 budget 字元；規則見檔頭。"""
    if len(body) <= budget:
        return [body]
    piece = max(1, budget // 3)
    lines = []
    for line in body.splitlines(keepends=True):
        while len(line) > piece:  # 單行超長才硬切
            lines.append(line[:piece])
            line = line[piece:]
        lines.append(line)
    chunks, i, opener = [], 0, None  # opener：上一段結尾還在程式碼區塊裡時的開啟行
    while i < len(lines):
        prefix = opener + "\n" if opener is not None else ""
        length, fence, cur_open = len(prefix), opener is not None, opener
        cands = []  # (下一行索引, 結尾是否在區塊內, 該處的開啟行, 是否空行之後, 長度)
        j = i
        while j < len(lines):
            line = lines[j]
            nf, no = fence, cur_open
            if is_fence(line):
                nf = not fence
                no = line.rstrip("\n") if nf else None
            close = len("\n" + FENCE + "\n") if nf else 0
            if length + len(line) + close > budget:
                break
            length += len(line)
            fence, cur_open = nf, no
            j += 1
            cands.append((j, fence, cur_open, line.strip() == "", length))
        if j == len(lines):
            chunks.append(prefix + "".join(lines[i:j]))
            break
        if not cands:
            raise UsageError(f"--max 太小，放不下一行（每則可用 {budget} 字元）")
        outside = [c for c in cands if not c[1]]
        blank = [c for c in outside if c[3] and c[4] >= budget // 2]
        cut = (blank or outside or cands)[-1]
        k, in_fence, open_line = cut[0], cut[1], cut[2]
        text = prefix + "".join(lines[i:k])
        if in_fence:
            text += ("" if text.endswith("\n") else "\n") + FENCE + "\n"
        chunks.append(text)
        i, opener = k, (open_line if in_fence else None)
    return chunks


def header(tag: str, title: str, note: str | None, k: int, n: int) -> str:
    suffix = f"（{k}/{n}）" if n > 1 else ""
    head = f"[{tag}] {title}{suffix}\n"
    if note:
        head += note + "\n"
    return head + "\n"


def render(tag: str, title: str, note: str | None, body: str, limit: int) -> list[str]:
    # 標頭長度隨則數的位數變；用假設的則數 n 算預算，直到實際則數的位數不超過 n 的位數，
    # 且「要不要加（k/n）」跟假設一致。這時每則的實際標頭都不比預算用的長。
    n = 1
    while True:
        budget = limit - len(header(tag, title, note, n, n))
        if budget <= 0:
            raise UsageError(f"--max {limit} 放不下標頭")
        parts = split_body(body, budget)
        if len(str(len(parts))) <= len(str(n)) and (len(parts) > 1) == (n > 1):
            break
        n = max(len(parts), n + 1)
    return [header(tag, title, note, k, len(parts)) + p for k, p in enumerate(parts, 1)]


def self_check(text: str, src: str) -> list[str]:
    out = []
    if not hook_rules.tagged(text):
        out.append(f"{src} 第一行沒有標記")
    p = hook_rules.local_path_problem(text, src, raw_ok=True)
    if p:
        out.append(p)
    elif hook_rules.local_path_problem(text, src, raw_ok=False):
        out.append(f"{src} 替換後仍含本機絕對路徑")
    return out


def clean(out_dir: Path) -> list[str]:
    removed = []
    if out_dir.is_dir():
        for f in sorted(out_dir.glob("post_*.md")):
            f.unlink()
            removed.append(str(f))
    return removed


def prepare(out_dir: Path, workspace: str, limit: int, items: list[list[str]]) -> dict:
    files, replaced, problems = [], [], []
    raw = raw_tag_names()
    rendered = []
    for tag, source, title in items:
        try:
            text = Path(source).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            problems.append(f"讀不到來源檔 {source}：{e}")
            continue
        if not text.strip():
            problems.append(f"來源檔是空的：{source}")
            continue
        body, reps, probs = replace_paths(text, workspace)
        problems += probs
        replaced += [{"source": source, **r} for r in reps]
        note = note_line(display_path(source, workspace), reps) if tag in raw else None
        rendered.append((tag, source, render(tag, title, note, body, limit)))
    out_dir.mkdir(parents=True, exist_ok=True)
    clean(out_dir)
    no = 0
    for tag, source, parts in rendered:
        for k, text in enumerate(parts, 1):
            no += 1
            path = out_dir / f"post_{no:02d}_{tag}.md"
            path.write_text(text, encoding="utf-8")
            problems += self_check(text, path.name)
            files.append({"path": str(path), "tag": tag, "source": source,
                          "part": k, "parts": len(parts), "chars": len(text)})
    return {"ok": not problems, "files": files, "replaced": replaced, "problems": problems}


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageError(message)


def parse(argv: list[str]) -> argparse.Namespace:
    ap = Parser(prog="prepare_comment.py")
    sub = ap.add_subparsers(dest="cmd", required=True, parser_class=Parser)
    p = sub.add_parser("prepare")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--workspace", required=True)
    p.add_argument("--max", type=int, default=DEFAULT_MAX)
    p.add_argument("--item", nargs=3, action="append", required=True,
                   metavar=("TAG", "SOURCE", "TITLE"))
    c = sub.add_parser("clean")
    c.add_argument("--out-dir", required=True)
    args = ap.parse_args(argv)
    if args.cmd == "prepare":
        for tag, _src, _title in args.item:
            if tag not in tag_names():
                raise UsageError(f"tag 只能是 {'、'.join(tag_names())}，收到 {tag!r}")
        if args.max < 1:
            raise UsageError("--max 要是正整數")
    return args


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse(sys.argv[1:] if argv is None else argv)
        if args.cmd == "clean":
            out = {"ok": True, "removed": clean(Path(args.out_dir))}
        else:
            out = prepare(Path(args.out_dir), args.workspace, args.max, args.item)
    except UsageError as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 2
    print(json.dumps(out, ensure_ascii=False))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
