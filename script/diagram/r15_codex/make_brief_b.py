import re, pathlib
S = pathlib.Path('.')
task = """你是 draw.io 產生器 `disc_v1_b.py` 的修改者。它是 Python 腳本，每頁用 helper（`Flow`／`_Band`：box／free／files／H／D／U／R／LD／UL／LL／P 等）產生 cells，末尾 `addpage(pid, name, cells)`。附件 H 是 helper 與頁內共用段（不可改）；頁內容段從 `# ================= P5：bootstrap.sh` 起，只改那之後。
規則：只改指定頁；每格一件事；例子只用 `<repo>`；線上字級 12；顏色只用圖例（藍＝引擎做、白＝啟動器做、綠＝0、橙＝需人處理、紅＝失敗、白虛線橢圓＝跨頁出入口）；頁高 ≤ 2400、頁寬 ≤ 1660；不可讓線交叉（check_cross_v1b）或壓框（check_overlap）；名詞表每頁 ≤ 8 條且不含第 0 頁的詞；事件名只准 launcher_start／launcher_exit／engine_start／engine_exit。
要做的：附件 R 的 v2.17 全部 11 條；附件 F 的必修＋選修逐條；附件 L 的 lint warn 全清。**改不了的**（會造成交叉、頁高超、頁序固有）不要硬改：在該頁右下角加一個黃底便條（style 同 `pend`，標題「待處理問題」），條列「元件 id：一句說明」。
做法：先 `python3 run_v1_b.py` 確認能跑；改完再跑，並跑 `python3 check_overflow.py v1_b.drawio`、`check_overlap.py`、`check_cross_v1b.py`、`check_self_v1b.py`、`check_jog_r7.py`、`check_align_v1b.py`（都要「共 0 筆」）與 `python3 extract_pages.py v1_b.drawio r15_b_out && python3 lint_pages.py r15_b_out`（非 termcov 的 warn 要 0）。最後輸出：改了哪些頁（id）與每頁改了什麼，加了哪些「待處理問題」便條，檢查結果。
注意：本檔的頁 id 只有 v1p5*／v1p6*／v1p7*／v1p8*（共 38 頁）。其他頁（v1p0…v1p4、v1p9 以後）在別的檔，由別人同時處理，不要碰 `disc_v1_a.py`、`disc_v1_c.py`、`gen_disc.py`、`drawio_common.py`、任何 check_*.py／lint_pages.py／extract_pages.py。附件 L、R 中屬於別的檔的頁（如 v1p1b／v1p2b／v1p3／v1p9c／v1p16*／v1p10）忽略；跨頁 term-diff 條目若本檔頁是其中一方，把本檔頁的名詞文字改成與較長版本一致（或直接刪掉那條名詞，只要不是本頁流程必需）。
"""
# R
prop = S.joinpath('decisions/_legacy/proposal_v2.md').read_text().splitlines()
def sect(lines, start_pat, stop_pat=None):
    out=[]; on=False
    for l in lines:
        if re.match(start_pat, l): on=True
        elif on and re.match(r'^# ', l) and (stop_pat is None or re.match(stop_pat, l)): break
        if on: out.append(l)
    return '\n'.join(out)
r16 = sect(prop, r'^# v2\.16'); r17 = sect(prop, r'^# v2\.17')
# F
claude = S.joinpath('review_v2r14_claude.md').read_text()
parts = re.split(r'(?m)^(?=## )', claude)
F = [p for p in parts if re.search(r'\((v1p[5-8][a-z]*)\)', p)]
F_ids = [re.search(r'\((v1p[5-8][a-z]*)\)', p).group(1) for p in F]
# L
L = [l for l in S.joinpath('review_v2r14_lint.md').read_text().splitlines() if re.search(r'\bv1p[5-8][a-z]*\b', l) or l.startswith('#')]
# include term-diff multi-line blocks that mention our pages
lintlines = S.joinpath('review_v2r14_lint.md').read_text().splitlines()
Lout=[]; i=0
while i < len(lintlines):
    l = lintlines[i]
    if l.startswith('- [term-diff]'):
        block=[l]; j=i+1
        while j < len(lintlines) and lintlines[j].startswith('  '): block.append(lintlines[j]); j+=1
        if re.search(r'\bv1p[5-8][a-z]*\b', '\n'.join(block)): Lout += block
        i=j; continue
    if l.startswith('#') or re.search(r'\bv1p[5-8][a-z]*\b', l): Lout.append(l)
    i+=1
H = '\n'.join(S.joinpath('disc_v1_b.py').read_text().splitlines()[:560])
K = S.joinpath('review_v2_README.md').read_text()
brief = f"""{task}

==================== 附件 R：decisions/_legacy/proposal_v2.md 的 v2.16 與 v2.17 ====================
{r16}

{r17}

==================== 附件 F：review_v2r14_claude.md 中屬本檔的頁（{len(F)} 頁）====================
{''.join(F)}

==================== 附件 L：review_v2r14_lint.md 屬本檔頁的行 ====================
{chr(10).join(Lout)}

==================== 附件 H：disc_v1_b.py 前 560 行（helper 與頁內共用；不可改）====================
{H}

==================== 附件 K：review_v2_README.md（lint 規則）====================
{K}
"""
S.joinpath('r15_codex/brief_b.txt').write_text(brief)
print(len(F), F_ids); print(len(brief))
