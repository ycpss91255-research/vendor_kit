import re, pathlib, sys
S = pathlib.Path('.')
half = sys.argv[1]  # '56' or '78'
pat = r'\((v1p[56][a-z]*)\)' if half=='56' else r'\((v1p[78][a-z]*)\)'
rng = 'v1p5*／v1p6*（v1p5、v1p5x、v1p5i、v1p5ccc、v1p5c、v1p5cm、v1p5cw、v1p5cc、v1p5b、v1p5bcc、v1p5bc、v1p6、v1p6cc、v1p6c、v1p6cw）' if half=='56' else 'v1p7*／v1p8*（v1p7、v1p7c、v1p7ccc、v1p7cc、v1p7cccc、v1p7b、v1p7bd、v1p7bc、v1p7bca、v1p7bcc、v1p7bcx、v1p7bccc、v1p7bcce、v1p7bccd、v1p8、v1p8ccc、v1p8c、v1p8cx、v1p8cc、v1p8b、v1p8bccc、v1p8bc、v1p8bcc）'
task = f"""你是 draw.io 產生器 `disc_v1_b.py` 的修改者（第二輪）。它是 Python 腳本，每頁用 helper（`Flow`／`_Band`：box／free／files／H／D／U／R／LD／UL／LL／P 等）產生 cells，末尾 `addpage(pid, name, cells)`。附件 H 是 helper 與頁內共用段（不可改）；頁內容段從 `# ================= P5：bootstrap.sh` 起，只改那之後。
規則：只改指定頁；每格一件事；例子只用 `<repo>`；線上字級 12；顏色只用圖例（藍＝引擎做、白＝啟動器做、綠＝0、橙＝需人處理、紅＝失敗、白虛線橢圓＝跨頁出入口）；頁高 ≤ 2400、頁寬 ≤ 1660；不可讓線交叉（check_cross_v1b）或壓框（check_overlap）；名詞表每頁 ≤ 8 條且不含第 0 頁的詞；事件名只准 launcher_start／launcher_exit／engine_start／engine_exit。

**第一輪已做**（別重做；只驗證是否還有殘留）：v1p5i 移三個前引；v1p5ccc docker 段改單一子流程；v1p5c 補 grep 命中 ≠ 1 紅出口；v1p5cc 補寫入／刪進度檔失敗匯流、移 symlink 名詞；v1p5bc 改刪進度檔失敗敘述；v1p6cc resolve 三叉／apply|no 順序；v1p6c 入口改承接前頁三叉；v1p7 補「⓪ 納管 → 1 停」出口；v1p7cccc 6-14 改提醒；v1p8bccc 改後段失敗終點敘述。目前六項幾何檢查與 lint（非 termcov）都是 0，改完必須維持。

**這一輪只處理本檔中 {rng} 這些頁**；其他頁（含本檔另一半與其他檔）一律不碰。也不要碰 `disc_v1_a.py`、`disc_v1_c.py`、`gen_disc.py`、`drawio_common.py`、任何 check_*.py／lint_pages.py／extract_pages.py。
要做的：**附件 F 中這些頁的每一條必修（「- [」開頭）與選修（「(opt)」）逐條處理**；附件 R v2.17 的 11 條凡落在這些頁的也要落實（例如第 1 條共通前置格位置＝docker run 之後、flock 之後、寫入之前；第 5 條 install `install <repo>` 誤用 6-17 出口與 flock 逾時標籤；第 6 條 sync(1) 本機覆寫判斷在 inspect／pull 之前；第 7 條 sync(2) mount 記錄、指紋重驗菱形「相同？」、sync(2′) 失敗線進匯流；第 8 條 B(1) 目標==現版判斷順序、長折線不貼綠終點；第 9 條標籤不壓線；第 3 條失敗終點文字不得不實）。
**每一條都要有交代**：要嘛改掉，要嘛（會造成交叉、頁高超 2400、頁序固有、或與其他規則衝突）在該頁右下角加一個黃底便條（style 同 `pend`，標題「待處理問題」），條列「元件 id：一句說明為何不改」。不可以既不改也不寫便條。便條也要通過 check_overlap（放在空白處，寬 ≤ 360，必要時放在最下方列的右側）。
做法：先 `python3 run_v1_b.py` 確認能跑；每改幾頁就跑一次，最後跑 `python3 check_overflow.py v1_b.drawio`、`check_overlap.py`、`check_cross_v1b.py`、`check_self_v1b.py`、`check_jog_r7.py`、`check_align_v1b.py`（都要「共 0 筆」／全「無」）與 `python3 extract_pages.py v1_b.drawio r15_b_out && python3 lint_pages.py r15_b_out`（非 termcov 的 warn 要 0）。若某個改動造成交叉或壓框且無法在幾次嘗試內解掉，就回退那一個改動並寫進便條。最後輸出：改了哪些頁（id）與每頁改了什麼（對應附件 F 的哪條）、加了哪些「待處理問題」便條（頁 id ＋ 內容）、檢查結果。
"""
prop = S.joinpath('decisions/proposal_v2.md').read_text().splitlines()
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
F = [p for p in parts if re.search(pat, p)]
H = '\n'.join(S.joinpath('disc_v1_b.py').read_text().splitlines()[:560])
K = S.joinpath('review_v2_README.md').read_text()
brief = f"""{task}

==================== 附件 R：decisions/proposal_v2.md 的 v2.16 與 v2.17 ====================
{r16}

{r17}

==================== 附件 F：review_v2r14_claude.md 中屬本輪的頁（{len(F)} 頁）====================
{''.join(F)}

==================== 附件 H：disc_v1_b.py 前 560 行（helper 與頁內共用；不可改）====================
{H}

==================== 附件 K：review_v2_README.md（lint 規則）====================
{K}
"""
S.joinpath(f'r15_codex/brief_b{half}.txt').write_text(brief)
print(half, len(F), len(brief))
