"""第十四輪：把 disc_v1_b.py 某頁區塊內 row >= k 的列號全部 +d。
用法: python3 r14_shift.py "<頁區塊起始標記子字串>" k d
區塊 = 從含該子字串的 '# ================= ' 行起，到下一個 '# ================= ' 行前。
改寫：b.box("id", COL, N, …)、b.files("id", COL, N, …)、footer(b, F, N, …)、pullseg(b, N, …)、lstart(b, …, N, …)、preseg(b, …, N, …)、res3(b, …, N, …)。"""
import re, sys
path = "disc_v1_b.py"; src = open(path, encoding="utf-8").read().split("\n")
mark, k, d = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
starts = [i for i, l in enumerate(src) if l.startswith("# ================= ")]
s = next(i for i in starts if mark in src[i]); e = next((i for i in starts if i > s), len(src))
def bump(m):
    n = int(m.group("n")); return m.group("pre") + str(n + d if n >= k else n) + m.group("post")
pats = [re.compile(r'(?P<pre>\bb\.(?:box|files)\("[^"]+", (?:[A-Z]+|RN), )(?P<n>\d+)(?P<post>,)'),
        re.compile(r'(?P<pre>\bfooter\(b, F, )(?P<n>\d+)(?P<post>,)'),
        re.compile(r'(?P<pre>\bpullseg\(b, )(?P<n>\d+)(?P<post>,)'),
        re.compile(r'(?P<pre>\b(?:lstart|preseg|res3)\(b, [^,]+, [^,]+, )(?P<n>\d+)(?P<post>[,)])')]
cnt = 0
for i in range(s, e):
    l = src[i]
    for p in pats:
        l, c = p.subn(bump, l); cnt += c
    src[i] = l
open(path, "w", encoding="utf-8").write("\n".join(src))
print(f"block {s+1}-{e}: {cnt} substitutions (rows >= {k} += {d})")
