import re, pathlib
S = pathlib.Path('.')
A_PAGES = ["v1p2","v1p3","v1p3b","v1p3bb","v1p3c","v1p3d","v1p4"]
C_PAGES = ["v1p9","v1p9c","v1p10","v1p11","v1p12","v1p15","v1p15c","v1p16","v1p16i","v1p16c","v1p16cb","v1p16cc","v1p16ccb","v1p16ccc"]
OUR = set(A_PAGES + C_PAGES)
task = """你是 draw.io 產生器 `disc_v1_a.py`、`disc_v1_c.py` 的修改者（Python；a 檔用 tbl／rtitle／emit 等 helper 畫表格與架構圖，c 檔 exec `disc_v1_b.py` 的 helper 段後用 Flow／_Band 畫流程）。附件 H 是 helper 段（不可改）。只改指定頁：a 檔 v1p2、v1p3、v1p3b、v1p3bb、v1p3c、v1p3d、v1p4；c 檔 v1p9、v1p9c、v1p10、v1p11、v1p12、v1p15、v1p15c、v1p16、v1p16i、v1p16c、v1p16cb、v1p16cc、v1p16ccb、v1p16ccc。**a 檔的 v1p0、v1p0c、v1p0b、v1p1、v1p1i、v1p1b、v1p1c、v1p2b、v1p2c 絕對不可改。**
規則：每格一件事；例子只用 `<repo>`；線上字級 12；顏色只用圖例；頁高 ≤ 2400、頁寬 ≤ 1660；不可交叉／壓框；名詞表每頁 ≤ 8 條且不含第 0 頁的詞；事件名只准 launcher_start／launcher_exit／engine_start／engine_exit。
要做的：附件 R 的 v2.17（含第 2 條契約④、第 10 條 lint、第 11 條便條規則）；附件 F 的必修＋選修逐條；附件 L 全清。改不了的在該頁右下角加黃底便條「待處理問題」（style 同 `pend`／NOTE），條列「元件 id：一句說明」。
做法：先 `python3 run_v1_a.py && python3 run_v1_c.py` 確認能跑；改完再跑，並對 `v1_a.drawio`、`v1_c.drawio` 各跑 `check_overflow.py`、`check_overlap.py`、`check_cross_v1b.py`、`check_self_v1b.py`、`check_jog_r7.py`、`check_align_v1b.py`、`check_margin_label.py`（都要「共 0 筆」）與 `extract_pages.py <drawio> <out> && lint_pages.py <out>`（非 termcov warn 要 0）。最後輸出：改了哪些頁與每頁改了什麼、便條清單、檢查結果。
注意：`disc_v1_b.py` 由別人同時修改，**不要碰**；`disc_v1_c.py` 第 10 行 exec 它的 helper 段，若 b 檔暫時語法壞導致 run_v1_c.py 跑不了，等 60 秒再試（最多 10 次）。不改 `gen_disc.py`、`drawio_common.py`、任何 check_*.py／lint_pages.py／extract_pages.py。附件 F／L／R 中屬別的檔的頁（v1p5*～v1p8*、v1p1b／v1p2b 等）忽略；跨頁 term-diff 兩條以**較長版本為準**、較長版本都在本檔頁（baseline/.gitkeep 的 v1 在 v1p2／v1p2c／v1p16i；6-33 的 v2 在 v1p10）：這些名詞文字**不要改**，b 檔那方會對齊過來（v1p2c 不可改，所以 v1p2／v1p16i 也不能動這條文字）。lint 的 write-fail-edge 條目屬 v1p9c／v1p16cb／v1p16ccc，要補失敗出邊或匯流；end-color-text 屬 v1p16 o3tx；term-count 屬 v1p3。
"""
prop = S.joinpath('decisions/_legacy/proposal_v2.md').read_text().splitlines()
def sect(lines, start_pat):
    out=[]; on=False
    for l in lines:
        if re.match(start_pat, l): on=True
        elif on and re.match(r'^# ', l): break
        if on: out.append(l)
    return '\n'.join(out)
r16 = sect(prop, r'^# v2\.16'); r17 = sect(prop, r'^# v2\.17')
claude = S.joinpath('review_v2r14_claude.md').read_text()
parts = re.split(r'(?m)^(?=## )', claude)
F=[]; F_ids=[]
for p in parts:
    m = re.search(r'\((v1p\d+[a-z]*)\)', p)
    if m and m.group(1) in OUR: F.append(p); F_ids.append(m.group(1))
lintlines = S.joinpath('review_v2r14_lint.md').read_text().splitlines()
def ours(text): return any(re.search(r'\b'+re.escape(p)+r'\b', text) for p in OUR)
Lout=[]; i=0
while i < len(lintlines):
    l = lintlines[i]
    if l.startswith('- [term-diff]'):
        block=[l]; j=i+1
        while j < len(lintlines) and lintlines[j].startswith('  '): block.append(lintlines[j]); j+=1
        if ours('\n'.join(block)): Lout += block
        i=j; continue
    if l.startswith('#') or ours(l): Lout.append(l)
    i+=1
Ha = '\n'.join(S.joinpath('disc_v1_a.py').read_text().splitlines()[:450])
Hc = '\n'.join(S.joinpath('disc_v1_c.py').read_text().splitlines()[:120])
K = S.joinpath('review_v2_README.md').read_text()
brief = f"""{task}

==================== 附件 R：decisions/_legacy/proposal_v2.md 的 v2.16 與 v2.17 ====================
{r16}

{r17}

==================== 附件 F：review_v2r14_claude.md 中屬 a／c 檔的頁（{len(F)} 頁：{' '.join(F_ids)}）====================
{''.join(F)}

==================== 附件 L：review_v2r14_lint.md 屬 a／c 檔頁的行 ====================
{chr(10).join(Lout)}

==================== 附件 H-a：disc_v1_a.py 前 450 行（helper：tbl／rtitle／emit／LEGEND 等；不可改）====================
{Ha}

==================== 附件 H-c：disc_v1_c.py 前 120 行（exec b 的 helper、_TRC 覆寫、foot()、LST1/LST2/LSX；不可改）====================
{Hc}

==================== 附件 K：review_v2_README.md（lint 規則）====================
{K}
"""
S.joinpath('r15_codex/brief_ac.txt').write_text(brief)
print(len(F), F_ids); print(len(Lout)); print(len(brief))
