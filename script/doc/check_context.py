#!/usr/bin/env python3
"""檢查根 CONTEXT.md：目錄／錨點／名詞三者一致，且 _Avoid_ 詞沒出現在正文。

用法：python3 script/doc/check_context.py [CONTEXT.md]
成功印 OK 並回 0；有問題逐條印出並回 1。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        lang = next(i for i, ln in enumerate(lines) if ln.strip() == "## Language")
    except StopIteration:
        print("找不到 '## Language'")
        return 1

    toc, body = lines[:lang], lines[lang:]
    errs = []

    # 目錄：群組標題（**X**）與條目（- [label](#anchor)）
    toc_groups, toc_items = [], []  # toc_items: (group, label, anchor)
    cur = None
    for ln in toc:
        m = re.fullmatch(r"\*\*(.+)\*\*", ln.strip())
        if m:
            cur = m.group(1)
            toc_groups.append(cur)
            continue
        m = re.fullmatch(r"- \[(.+)\]\(#([a-z0-9-]+)\)", ln.strip())
        if m:
            toc_items.append((cur, m.group(1), m.group(2)))

    # 正文：### 群組、<a id=...>、緊接的 **名詞** 行
    body_groups, body_terms = [], []  # body_terms: (group, anchor, label)
    cur = None
    for i, ln in enumerate(body):
        m = re.fullmatch(r"### (.+)", ln.strip())
        if m:
            cur = m.group(1)
            body_groups.append(cur)
            continue
        m = re.fullmatch(r'<a id="([a-z0-9-]+)"></a>', ln.strip())
        if not m:
            continue
        anchor = m.group(1)
        nxt = body[i + 1].strip() if i + 1 < len(body) else ""
        mt = re.match(r"^(\*\*.+?\*\*.*?)：\s*$", nxt)
        if not mt:
            errs.append(f"錨點 {anchor} 下一行不是名詞定義起頭：{nxt!r}")
            label = nxt
        else:
            label = mt.group(1)
        body_terms.append((cur, anchor, label))

    # 錨點唯一
    for coll, what in ((toc_items, "目錄"), (body_terms, "正文")):
        seen = set()
        for row in coll:
            a = row[2] if what == "目錄" else row[1]
            if a in seen:
                errs.append(f"{what}錨點重複：{a}")
            seen.add(a)

    # 群組一致
    if toc_groups != body_groups:
        errs.append(f"分群不一致：目錄 {toc_groups} / 正文 {body_groups}")

    # 條目 ↔ 錨點，順序與分群都要對上
    t = [(g, a) for g, _, a in toc_items]
    b = [(g, a) for g, a, _ in body_terms]
    if t != b:
        ts, bs = set(t), set(b)
        for x in [x for x in t if x not in bs]:
            errs.append(f"目錄有、正文沒有：{x}")
        for x in [x for x in b if x not in ts]:
            errs.append(f"正文有、目錄沒有：{x}")
        if ts == bs:
            errs.append("目錄與正文順序不一致")

    # 目錄 label 要和正文名詞對得上（去掉 markdown 與英文括號後比較）
    def norm(text: str) -> str:
        text = re.sub(r"[*`]", "", text)
        text = re.sub(r"（.*?）", "", text)
        return text.strip()

    for (g1, lab, a1), (g2, a2, lab2) in zip(toc_items, body_terms):
        if a1 == a2 and norm(lab) != norm(lab2):
            errs.append(f"{a1}：目錄寫 {norm(lab)!r}，正文寫 {norm(lab2)!r}")

    # _Avoid_ 詞不得出現在正文（_Avoid_ 行本身除外）
    avoid = set()
    for ln in body:
        if ln.startswith("_Avoid_:"):
            for w in ln[len("_Avoid_:"):].split("、"):
                w = w.strip().strip("`")
                if w:
                    avoid.add(w)
    for i, ln in enumerate(body):
        if ln.startswith("_Avoid_:"):
            continue
        for w in avoid:
            if w in ln:
                errs.append(f"正文第 {lang + i + 1} 行出現 _Avoid_ 詞 {w!r}：{ln.strip()}")

    for e in errs:
        print(e)
    print(
        f"{'OK' if not errs else 'FAIL'}: 分群 {len(body_groups)}、名詞 {len(body_terms)}、"
        f"目錄條目 {len(toc_items)}、_Avoid_ 詞 {len(avoid)}"
    )
    return 1 if errs else 0


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "CONTEXT.md"
    sys.exit(main(target))
