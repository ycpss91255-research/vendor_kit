#!/usr/bin/env python3
"""檢查對外文件（根目錄 README.md 與 docs/contract/0N_*.md）的寫法規則。

規則見 docs/contract/README.md「寫法規則」與「版本怎麼迭代」：
1. 不寫「出處：」行：沿用規則時在正文寫「依 [頁名](連結#錨點) 第 N 條」。
2. 不寫「> 版本 vN」：版本只在 doc/decisions/_marked/ 的檔名。
3. 每頁有「## 目錄」。
3a. HTML 只准 <ins>：<a id>、<br> 這類只有部分環境顯示得出來；錨點一律用標題產生。
4. 相對連結的檔案與錨點都存在（錨點照 GitHub 的標題轉換規則算）。
5. 只能向前依賴：審閱頁 N 不能連到編號比它大的審閱頁。
6. 03 總表的指令寫法只能用前面頁定義過的：反引號裡 `just vendor_kit …` 的每個選項（-x、--xxx）
   與 @<tag> 寫法，都要在 GLOSSARY.md、01、02 出現過。

用法：python3 script/check_review_pages.py（在 repo 根目錄跑；有問題以 1 結束）
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(".")
REVIEW = ROOT / "docs/contract"
PAGE = re.compile(r"^(\d\d)_.+\.md$")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")


def pages() -> list[pathlib.Path]:
    return [ROOT / "README.md"] + sorted(p for p in REVIEW.glob("*.md") if PAGE.match(p.name))


def slug(text: str) -> str:
    """GitHub 的標題錨點：小寫、去掉標點（保留文字、數字、_、-、空白），空白換成 -。"""
    text = re.sub(r"<[^>]+>", "", text)          # <ins> 之類的標籤
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # 連結只留文字
    text = text.replace("`", "").lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(path: pathlib.Path) -> set[str]:
    seen: dict[str, int] = {}
    out = set()
    fenced = False
    for line in path.read_text().splitlines():
        if FENCE.match(line):
            fenced = not fenced
            continue
        m = None if fenced else HEADING.match(line)
        if not m:
            continue
        s = slug(m.group(2))
        n = seen.get(s, 0)
        out.add(s if n == 0 else f"{s}-{n}")
        seen[s] = n + 1
    return out


def body_lines(path: pathlib.Path):
    fenced = False
    for i, line in enumerate(path.read_text().splitlines(), 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            yield i, line


def page_no(path: pathlib.Path) -> int | None:
    m = PAGE.match(path.name)
    return int(m.group(1)) if m and path.parent.resolve() == REVIEW.resolve() else None


def check_page(path: pathlib.Path, errors: list[str]) -> None:
    text = path.read_text()
    if "## 目錄" not in text:
        errors.append(f"{path}: 沒有「## 目錄」")
    me = page_no(path)
    for i, line in body_lines(path):
        where = f"{path}:{i}"
        if re.match(r"^\s*(?:[-*]\s*)?出處[:：]", line):
            errors.append(f"{where}: 對外頁不寫「出處」行；沿用規則時在正文寫「依 [頁名](連結#錨點) 第 N 條」")
        tags = sorted({t for t in re.findall(r"</?([a-zA-Z][\w-]*)[^>]*>", re.sub(r"`[^`]*`", "", line)) if t != "ins"})
        if tags:
            errors.append(f"{where}: 用了 HTML {tags}：對外頁只准 <ins>（GitHub 與 GitLab 都顯示）；錨點用標題產生")
        if re.match(r"^>\s*版本\s*v\d+\s*$", line):
            errors.append(f"{where}: 正式檔不寫版本號；版本只在 _marked/ 的檔名")
        for target in LINK.findall(line):
            if re.match(r"^[a-z]+:", target):
                continue
            file_part, _, frag = target.partition("#")
            dest = path if not file_part else (path.parent / file_part)
            if file_part.startswith("/"):
                errors.append(f"{where}: 連結 {target} 以 / 開頭，改成相對路徑")
                continue
            if not dest.exists():
                errors.append(f"{where}: 連結目標不存在：{target}")
                continue
            if frag and dest.suffix == ".md" and frag not in anchors(dest):
                errors.append(f"{where}: 錨點不存在：{target}")
            other = page_no(dest) if dest.suffix == ".md" else None
            if me is not None and other is not None and other > me:
                errors.append(f"{where}: 審閱頁 {me:02d} 連到後面的頁 {dest.name}；只能向前依賴")


def check_commands(errors: list[str]) -> None:
    msgs = sorted(REVIEW.glob("03_*.md"))
    if not msgs:
        return
    defined = "\n".join(
        p.read_text() for p in [ROOT / "GLOSSARY.md", *sorted(REVIEW.glob("0[12]_*.md"))] if p.exists()
    )
    for i, line in body_lines(msgs[0]):
        for cmd in re.findall(r"`(just vendor_kit [^`]+)`", line):
            for tok in re.findall(r"(?<![\w<])(--?[a-z][\w-]*|@<[^>]+>)", cmd):
                if tok not in defined:
                    errors.append(
                        f"{msgs[0]}:{i}: 指令 `{cmd}` 用了 {tok}，但 GLOSSARY.md、01、02 都沒出現過；先補進前面的頁"
                    )


def main() -> int:
    errors: list[str] = []
    ps = pages()
    for p in ps:
        check_page(p, errors)
    check_commands(errors)
    for e in errors:
        print(e)
    if errors:
        print(f"FAIL: {len(errors)} 個問題")
        return 1
    print(f"OK: 掃 {len(ps)} 個對外文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
