OpenAI Codex v0.155.1
--------
workdir: <scratchpad>
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: danger-full-access
reasoning effort: low
reasoning summaries: none
session id: 01a0bf78-cfd1-7ae2-a192-17e0807839c4
--------
user
你是 draw.io 產生器 `disc_v1_b.py` 的修改者（補漏輪，時間預算約 6 分鐘）。前幾輪已把 v1p5*～v1p8* 大部分頁改完，目前六項幾何檢查與 lint（非 termcov）全為 0，改完必須維持。這一輪**只處理三頁**：v1p8b、v1p7bcc、v1p7bccd（附件 F）；其他頁與其他檔一律不碰。附件 H 是 helper 與頁內共用段（不可改）。
規則：每格一件事；線上字級 12；不可讓線交叉（check_cross_v1b）／壓框（check_overlap）／標籤寬 ≥ 線長（check_self_v1b）／折線 dx < 40（check_jog_r7）；頁高 ≤ 2400；菱形出邊只能 2。
要做的：附件 F 三頁的必修與選修逐條處理。每一條都要有交代：要嘛改掉，要嘛在該頁右下角加一個黃底便條（`pend(cells, "待處理問題\n• 元件 id：一句說明")`，放在 foot() 之前，並把 foot 的排除集合中 "pend" 拿掉），不可以既不改也不寫便條。v1p8b 的 me8ax「逾時」標籤壓框：參考 v1p5c／v1p8cc／v1p8bc 這幾頁已處理過的做法（看目前檔案裡它們怎麼寫）。
做法：先 `python3 run_v1_b.py`；改完跑 `python3 check_overflow.py v1_b.drawio`、`check_overlap.py`、`check_cross_v1b.py`、`check_self_v1b.py`、`check_jog_r7.py`、`check_align_v1b.py`（都要「共 0 筆」／全「無」）與 `python3 extract_pages.py v1_b.drawio r15_b_out && python3 lint_pages.py r15_b_out`（非 termcov warn 要 0）。解不掉就回退那個改動並寫便條。最後輸出：每頁改了什麼（對應附件 F 哪條）、加了哪些便條、檢查結果。

==================== 附件 F ====================
## 51 流程 v2：remove（1）resolve → apply 前置 (v1p8b): must_fix 1 / optional 1
- [排版] me8ax: 「逾時」標籤（apply flock 格 → 1 + 6-26 橢圓）間距僅 30px，標籤壓在藍格右邊框上（與 v1p8cc、v1p8bc 同一問題）
  (opt) [內容一致性] m3: 「0：未接入（提示）」直接從引擎判斷 m2 終止，啟動器三叉（m8q0／m8q1）沒有 apply|no → 0 的出路；spec §3.3 未接入時 resolve 回 0 + apply|no、由啟動器驗完文法後 exit 0，圖上此 0 終點在啟動器側不可達。同型：v1p8c u3、v1p8cc w3

## 41 流程 v2：upgrade ── E(c) upgrade vendor_kit（1） (v1p7bcc): must_fix 0 / optional 2
  (opt) [排版] se12f: 「指定 @<tag>？」的「否」線在 x≈590 垂直下行，距「是：目標 = @<tag>」框左緣只約 10px，縮圖上貼著框走；且「否」標籤放在終點（CI 模式菱形旁）而不是出發的菱形旁
  (opt) [排版] se11y: inspect「有」線的回繞在 vendor_kit:vN 紫框右側與下側都只離約 15px，把紫框框住一半；回繞線外移

## 45 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′） (v1p7bccd): must_fix 0 / optional 1
  (opt) [內容一致性] s13h: 菱形「啟動器：apply 後 grep 第一行 == apply 前（未變）？」把 grep 動作與比對判斷合在一格；E(a′) 頁（v1p7bca）同一件事拆成 s2h 白框 + 「第一行變了？」菱形，兩頁不一致



==================== 附件 H：disc_v1_b.py 前 560 行（helper；不可改）====================
"""提案 v2 流程頁（v1p5…v1p8b，拆格後超高的頁再拆成 …c 頁）。
依據：decisions/proposal_v2.md（§2 表格、§5 初始檔規則、§6 啟動器、§7 CI）＋ v2.1 A–F ＋ v2.2 ＋ v2.3 ＋ v2.4 ＋ v2.5（最新優先），
＋ v2.6（2026-09-19 規格審查 16 條必修 + Q22–Q27，最高優先；decisions/interface_spec.md v2 為動詞行為／選項／結束碼／訊息逐字來源），
第十二輪（review_v2r11_findings.md 必修＋選修）：頁尾統一為「log_prune」→「launcher_exit」兩格 + 終點列（footer()/footer_edges()：所有終點的唯一前驅是 launcher_exit 格；各分支從左側匯流排 x=30 匯入，成功路徑直下）；每個 docker run 之後緊接 engine_start（EST_R／EST_A／EST_1）；啟動器 image 段統一 pullseg()（inspect／pull／image 同中心直下，本機有 → 頁面右側 bypass()，pull 失敗紅出口）；拆頁：bootstrap.sh（1′）v1p5i、install（1′）v1p5cw、D. 回退 v1p7bd、E(c)（1′）v1p7bcx；sync(1) 的 docker run 移到 sync(1′) 頁首；E(a) 的 (b) 段改成引用 sync(1)；C′ 出口改文字；內容：bootstrap 先驗 git／just 才建 log；install 的 git／巢狀檢查移到主機側；add 已接入且完成先於查 registry、--local 拆格；B(1) 6-3 橙出口；E(a) 新引擎 pull 移到 apply 前；E(c)(2) 建日誌＋config.toml 拆三格；remove(2) 逐行比對迴圈；undev u6x 措辭；名詞表逐頁裁剪（頁高 ≤ 2400）。備份：.v13（第十二輪前）。
第十一輪（v2.13 + v2.14 + review_v2r10_findings.md）：主路徑補線（B(1) b1q→b2→b2c、uninstall(1) x2→x2b…x2e）；每頁 resolve／apply 段各一格 engine_start、頁尾一格 log_prune／launcher_exit；
藍 = 引擎、白 = 啟動器全檔核對；gen/.stamp 只記引擎 ref、log.sh 帶自描述首行；sync(1′) 6-33 菱形；工具 image pull 失敗紅出口；uninstall(2) 不刪 log/、config.toml 依 v2.13 P6；
E(c)(2) config.toml 三方合併；install(2) igq 拆兩菱形；B(2) 逐檔改「情況菱形 → 同意？」兩層（每菱形兩出邊）；共用名詞改常數；備份：.v12（第十一輪前）。
以及 review_v2r4_findings.md 十六頁段落的必修＋選修（第五輪）。
只定義 pages_v1_b = [(pid, name, cells), ...]；不寫檔（run_v1_b.py 負責組 mxfile）。備份：.v1（v1）、.v2（拆頁前）、.v4（第三輪前）、.v5（第四輪前）、.v6（第五輪前）、.v7（第六輪前）、.v8（第七輪前）、.v9（第八輪前）、.v10（第九輪前）、.v11（第十輪前）。
第十輪（v2.11 + v2.12 + review_v2r9_findings.md）：upgrade vendor_kit 改回建進度日誌 .tmp.upgrade.<id>.toml（E(a) s2d／s2df、E(c)(1) s12j、E(c)(2) s13d 由新引擎刪；撤回 v2.10-4）；
操作紀錄檔：啟動器起點後「建 log 檔並寫 launcher_start」一格（bootstrap(1) a0l、install(1) i0l、add(1) c0l、sync(1) n0l、B(1) b0l、E(c)(1) s10l、dev d0l、remove(1) m0l、uninstall(1) x0l），引擎 append engine_start 一格（i1e／c1e／b1e／d1e／m1e／x1e）或入口文字帶過；
sync(1) 快路徑寫 sync_fast_path／launcher_exit（nql）；install(2) .dockerignore 四行（＋.vendor_kit/log/）；install(1) 建 config.toml（i4_5）；名詞表加操作紀錄檔／config.toml／6-38；
--local 名詞：bootstrap tag 形 digest = 既有 version.toml 或內嵌引擎 ref、add --local 只收存在的 .tar；bootstrap(2) 本次 add 失敗即中止（a10x）；E(a) se6vr／E(c)(1) se11vr 補「否」線；s12hz 改續跑入口樣式；E(c)(1) @tag／frozen 拆開；dev vendor_kit v9 橙；uninstall(2) x5d 拆 gen/／baseline/ 兩格。
第九輪（v2.10 + review_v2r8_findings.md）：需人動作的 1 結束一律橙（B(1′) b10dx／b10nx、dev d3a／d1x／d3c）；upgrade vendor_kit 不建進度日誌（E(c) 兩頁）；6-2b 只給第一行已改（E(a) s2lx、E(c)(2) s13x 拆兩個結束）；
迴圈菱形（bootstrap(2)「還有下一個 -t？」、sync(1′)「還有工具？」）；install(1) 第一次直接建檔；install(2) 刪日誌獨立格；sync(2) 驗證／重裝拆格；失敗線不 T 接（各自進紅橢圓不同入口）；ae11b 不交叉；ce28n／ce28y 標籤離框。
第八輪（v2.9 + review_v2r7_findings.md）：bootstrap tag 形不讀 .digest（a8q 否 → a8i）；dev 起點與菱形距 ≥ 40；add 私有 image 分支、dest／撞名改橙；sync 逐檔驗加「版本變動那次」（sync(2) 補一格）；
B(2) 解析檢查移到替換前、B(2′) 解析失敗檔不推 baseline；uninstall append 行逐行比對；be7 RD、be17 對齊、te14 頂點。
第七輪（v2.8 + review_v2r6_findings.md）：uninstall(2) 刪除集合補 baseline/ 根檔＋rmdir、xe16f/xe16w 不交叉；E(c) 薄殼比對移到拿鎖重驗後、改第一行前；bootstrap --local 三分支；
install 第一次不建日誌／修復型建 .tmp.install；add(2) 逐檔迴圈（LL 線型）；dev vendor_kit inspect 移到啟動器；菱形入口一律頂點（D/U 對齊不動菱形入口）；files(cols=2／cw) 兩欄檔案框；PRE 框走 <pre>+&#9; 真 tab。
第六輪（v2.7 + review_v2r5_findings.md）：一格一件事再細（inspect／pull 分格、建檔／印出分格、append／記 metadata 分格、materialize／原子替換分格、計畫／指紋分格、
判斷格只放一個問句）；declined 語意（已納管檔拒絕 → state 不變只記 declined_hash；新檔被拒才 state=declined）；E(c) 查 registry 三種結果；undev vendor_kit 走 resolve→apply + .tmp.undev 日誌；
bootstrap Q18 分支；逐字範例框 whiteSpace=pre + &nbsp; 縮排；頁名 <repo> 單次跳脫；線標籤不壓線（菱形只從底端中央／側邊出線；RD／LD／R 標籤放在線旁）。
第五輪規則：不用 --pull never（啟動器 docker image inspect 驗本機 image ID，有就直接 run）；CI 一律寫「CI 為真（frozen）」；tools.just 一律 mod?；
橙 = 需要人動作（請先 undev／add／git init／重跑／upgrade vendor_kit／解衝突），紅 = 失敗；跨頁出入口標頁名，入口用白底虛線橢圓「來自 <頁名>」（ENTRY）。
泳道歸屬：所有判斷／合併／衝突處理畫在「引擎容器」；啟動器只有 grep 引擎 ref／gen/.stamp 比對／docker pull・create・cp・run・rm／轉發。
動詞兩段：引擎 resolve（不寫）→ 啟動器 docker → 引擎 apply（v2.5 §3：flock → 重驗指紋 → dry-run 分支 → 建進度日誌 → 寫入們 → 最後刪日誌）。
每格一件事；橢圓／菱形用 check_overflow.shape_spacing 補 spacing（v2.5 §15），高度以內接矩形估；檔案框一格一檔（多檔用 files() 標題容器）。"""
import glob, re, math
_latest = sorted(glob.glob("gen[0-9]*.py"), key=lambda p: int(re.findall(r"\d+", p)[0]))[-1]
exec(open(_latest).read().split("# ================= Page 1")[0])   # helper：v/e/page/legend_flow/terms/SW/LEAF/FILE/NOTE/PEND/ELLIPSE/PURPLE_LEAF/TITLE/EDGE/顏色
from check_overflow import wrap as _wrap, shape_spacing
if not getattr(page, "_single_esc", False):                                          # 頁名 <repo> 不雙重跳脫（v2.7 §12）
    import html as _html
    _page_raw = page
    def page(id, name, cells, **kw):
        out = _page_raw(id, name, cells, **kw)
        return out.replace(f'name="{esc(name)}"', f'name="{_html.escape(name, quote=True)}"', 1)
    page._single_esc = True

# ---------- 12pt 樣式 ----------
def _12(st): return st.replace("fontSize=14", "fontSize=12")
ORANGE = "#ffe6cc"
PAD = "spacingLeft=6;spacingRight=6;"                                                # 長方形文字不貼框（折行寬 = w−16，與估算一致）
W12 = _12(LEAF()) + PAD; F12 = _12(FILE) + PAD; G12 = _12(ELLIPSE(GREEN)); R12 = _12(ELLIPSE(RED)); D12 = _12(RHOMBUS)
O12 = _12(ELLIPSE(ORANGE))                                                           # 橙橢圓 = 需要人動作（1／3 且印指令；2 解衝突也橙；v2.6 §15）
ENTRY = _12(ELLIPSE("#ffffff")) + "dashed=1;"                                        # 白底虛線橢圓 = 來自其他頁的入口（v2.6 §15）
IMG = _12(PURPLE_LEAF) + PAD                                                         # 紫 = image（與主圖 legend 一致）
SUB = "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;strokeWidth=2;" + PAD   # 藍 = 引擎子命令（容器內）
FTREE = _12(FILE) + "align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;"     # 前／後目錄差異
PRE = ("rounded=1;whiteSpace=pre;html=1;fillColor=#ffffff;strokeColor=#666666;dashed=1;strokeWidth=2;fontSize=12;fontFamily=Courier New;"
       "align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;")                  # 逐字範例檔案框：等寬、不置中、不 wrap；縮排用 &nbsp;（v2.7 §9）
NB4 = "&nbsp;&nbsp;&nbsp;&nbsp;"                                                    # 逐字框的 4 格縮排（html 不吃）
FGRP = _12(FILE) + "align=left;verticalAlign=top;spacingLeft=8;spacingTop=2;fontStyle=1;container=1;collapsible=0;"   # 檔案標題容器（內排小框）
RULE = ("rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;strokeWidth=2;fontSize=12;fontStyle=1;"
        "align=left;verticalAlign=middle;spacingLeft=8;")                           # 橘框 = 規則（已定）
INV = ("rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#b85450;strokeWidth=3;fontSize=12;fontStyle=1;"
       "align=left;verticalAlign=middle;spacingLeft=8;")                            # 紅粗框（白底）= 不變量
PENDR = PEND + "fontStyle=1;"                                                       # 黃便條 = 待拍板
HDR = "rounded=0;whiteSpace=wrap;html=1;fillColor=#e6e6e6;strokeColor=#999999;strokeWidth=1;fontSize=12;fontStyle=1;align=center;"
BAND = SW(NEUTRAL, 12).replace("startSize=38", "startSize=30")
LBL = TEXT(12) + "align=left;fontStyle=1;"
V2G = "#00b050"
TAG = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={V2G};strokeColor=none;fontColor=#ffffff;fontSize=9;fontStyle=1;"
       "align=center;verticalAlign=middle;spacing=0;spacingLeft=0;spacingRight=0;spacingTop=0;spacingBottom=0;")
def v2(st):
    """v2 改：不改框色，只在格子右上角加綠色小標籤「v2」（close() 時把 v2=1 記號換成標籤格）。"""
    return st + "v2=1;"


def fl(text):
    """把手動換行拿掉，交給 whiteSpace=wrap 自動折行（高度估算與畫面一致，行數最少）。英數之間補空白。"""
    out = []
    for i, ch in enumerate(text):
        if ch == "\n":
            a = text[i - 1] if i else ""; b = text[i + 1] if i + 1 < len(text) else ""
            out.append(" " if (a.isascii() and a.isalnum()) or (b.isascii() and b.isalnum()) else "")
        else: out.append(ch)
    return "".join(out)

def shape_f(st):
    """內接矩形係數：橢圓 0.707、菱形 0.5、其餘 1（spacing 補上後折行寬 = 內接矩形寬，與 check_overflow 同一套）。"""
    return 0.707 if st.startswith("ellipse") else (0.5 if st.startswith("rhombus") else 1.0)

def fit_w(text, w, st=""):
    """最寬的英數字（不能斷）塞不進內接矩形 → 自動加寬。"""
    f = shape_f(st); need = max((_wrap(ln, 12, 1e9)[1] for ln in text.split("\n")), default=0) + 16
    return w if w * f >= need else math.ceil(need / f)

def fit_h(text, w, minh=40, extra=0, st=""):
    """文字塞得進的高度（與 check_overflow 同一套估法；橢圓／菱形換算內接矩形）。"""
    f = shape_f(st)
    return max(minh, math.ceil((need_h(text, 12, w * f) + extra) / f) + 2)

def pre_v(cid, parent, st, text, x, y, w, h):
    """逐字框（whiteSpace=pre）：值包在 <pre> 內、tab 寫成 &#9;（XML 屬性裡的字面 tab 會被正規化）；同 disc_v1_a 的 code()（v2.7 §9）。"""
    import html as _html
    inner = _html.escape(text, quote=False).replace("\n", "<br>")
    htmlv = '<pre style="margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;">' + inner + '</pre>'
    val = _html.escape(htmlv, quote=True).replace("\t", "&#9;")
    return (f'<mxCell id="{cid}" value="{val}" style="{st}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

def emit(cells, cid, parent, st, text, x, y, w, h):
    """輸出一格；style 帶 v2=1 → 另加右上角綠標籤；橢圓／菱形自動補 spacing（v2.5 §15）；whiteSpace=pre → pre_v。"""
    tag = "v2=1;" in st; st = shape_spacing(st.replace("v2=1;", ""), w, h)
    cells.append((pre_v if "whiteSpace=pre;" in st else v)(cid, parent, st, text, x, y, w, h))
    if tag: cells.append(v(f"{cid}_v2", parent, TAG, "v2", round(x + w - 24), round(y - 10), 30, 20))

# ---------- 泳道流程佈局 ----------
class Flow:
    """cols: [(名稱, x, w)]（絕對座標）。band() 開一個情境分組；box() 放格子（欄, 列）；H/D/U/R/LU/DL/LD/P 拉線；close() 排版並輸出。"""
    def __init__(self, cells, cols, band_x=20, band_w=1600, gap=20):
        self.cells, self.cols, self.bx, self.bw, self.gap = cells, {n: (x, w) for n, x, w in cols}, band_x, band_w, gap
        self.abs = {}; self.y = 0; self.n = 0
    def headers(self, y):
        for i, (n, (x, w)) in enumerate(self.cols.items()):
            self.cells.append(v(f"hdr{i}", "1", HDR, n, x, y, w, 28))
        self.y = y + 44
    def band(self, bid, title, pad=6, v2=False):
        return _Band(self, bid, title, pad, v2)

class _Band:
    def __init__(self, f, bid, title, pad, v2flag):
        self.f, self.bid, self.title, self.pad, self.v2 = f, bid, title, pad, v2flag
        self.boxes, self.edges, self.extra = [], [], []
    def box(self, cid, col, row, style, text, w, h=None, ax="c", minh=40, extra=0):
        """ax: 'c' 置中／'l' 靠欄左／'r' 靠欄右／數字 = 欄左偏移。h 未給就依文字算（給了也至少要塞得下）。"""
        w = fit_w(text, w, style)
        hh = fit_h(text, w, minh, extra + (6 if "v2=1;" in style and shape_f(style) == 1 else 0), style)
        h = hh if h is None else max(h, hh)
        self.boxes.append(dict(id=cid, col=col, row=row, st=style, text=text, w=w, h=h, ax=ax)); return cid
    def files(self, cid, col, row, title, items, w, ax="c", cols=1, cw=None):
        """檔案框一格一檔（v2.5 §14）：虛線標題容器，內排每檔一個小框（id = cid_0, cid_1…）；cols=2 → 兩欄（同列取最高；cw=(w1, w2) 指定各欄寬）。"""
        if cw is None: cw = [(w - 16 - 6 * (cols - 1)) // cols] * cols
        cols = len(cw); assert sum(cw) + 6 * (cols - 1) <= w - 16
        hs = [fit_h(t, cw[i % cols], 26) for i, t in enumerate(items)]
        rows = [max(hs[i:i + cols]) for i in range(0, len(hs), cols)]
        h = 26 + sum(rows) + 6 * len(rows) + 4
        self.boxes.append(dict(id=cid, col=col, row=row, st=FGRP, text=title, w=w, h=h, ax=ax, items=list(zip(items, hs)), cols=cols, cw=cw, rows=rows)); return cid
    def free(self, cid, style, text, x, y, w, h=None, minh=40):
        """不參與排版的格子（band 內相對座標）；h 未給就依文字算（給了也至少要塞得下）。"""
        w = fit_w(text, w, style); hh = fit_h(text, w, minh, 0, style)
        h = hh if h is None else max(h, hh)
        self.extra.append((cid, style, text, x, y, w, h))
    def free_files(self, cid, title, items, x, y, w):
        """free 版的檔案容器（一格一檔）；回傳容器高度。"""
        iw = w - 16; hs = [fit_h(t, iw, 26) for t in items]
        h = 26 + sum(hs) + 6 * len(items) + 4
        self.extra.append((cid, FGRP, title, x, y, w, h)); self.extra_items = getattr(self, "extra_items", {}); self.extra_items[cid] = list(zip(items, hs))
        return h
    def H(self, eid, s, t, label="", sy=0.5): self.edges.append(("H", eid, s, t, label, sy))
    def D(self, eid, s, t, label="", sx=0.5, tx=0.5, dy=0, al=False): self.edges.append(("D", eid, s, t, label, sx, tx, dy, al))
    def U(self, eid, s, t, label="", sx=0.5, tx=0.5, dy=0, al=False): self.edges.append(("U", eid, s, t, label, sx, tx, dy, al))
    def R(self, eid, s, t, label="", busx=0, tx=0.5, dy=0, vert=None):
        """從 s 右側出去，沿 x=busx 的「匯流排」往下，在 t 上方的縫隙轉進 t 頂端（多個右側結果匯到同一格）。vert 給了 → 標籤放在垂直段旁（True=右、'left'=左）。"""
        self.edges.append(("R", eid, s, t, label, busx, tx, dy, vert))
    def LD(self, eid, s, t, label="", busx=0, vert=None):
        """從 s 左側出去，水平到 x=busx，往下直接進 t 頂端（t 在下方、且 busx 落在 t 的寬度內）。vert 給了 → 標籤放在垂直段旁（'left'=線左、True=線右、'below'=水平段下）。"""
        self.edges.append(("LD", eid, s, t, label, busx, vert))
    def UL(self, eid, s, t, label="", busx=0, row=0, dy=0):
        """從 s 頂端往上到第 row 列上方的縫隙（再偏 dy），水平到 x=busx 的左側匯流排，往下到 t 的中線高度，再水平進 t 的左側（繞過中間所有格子的回流線）。"""
        self.edges.append(("UL", eid, s, t, label, busx, row, dy))
    def LL(self, eid, s, t, label="", busx=0):
        """從 s 左側出去，水平到 x=busx 的左側匯流排，往上到 t 的中線高度，再水平進 t 的左側（迴圈回上方的格子；標籤放匯流排左側）。"""
        self.edges.append(("LL", eid, s, t, label, busx))
    def RD(self, eid, s, t, label="", tx=0.5):
        """從 s 右側出去，水平到 t 的 x=tx 處，往下進 t 頂端（t 在右下；菱形的側邊出口，不從底端分兩條）。標籤放在水平段下方。"""
        self.edges.append(("RD", eid, s, t, label, tx))
    def BL(self, eid, s, t, label="", busx=0, sx=0.5):
        """從 s 底端往下到列間縫隙，水平到 x=busx 的左側匯流排，往下到 t 的中線高度，再水平進 t 的右側（t 在左下方；避開右側的寫入線）。"""
        self.edges.append(("BL", eid, s, t, label, busx, sx))
    def LU(self, eid, s, t, label="", tx=0.5):
        """從 s 右側出去，水平到 t 正下方，再往上進 t 底端（t 在上一列）。"""
        self.edges.append(("LU", eid, s, t, label, tx))
    def DL(self, eid, s, t, label="", sx=0.5):
        """從 s 底端往下到 t 的中線高度，再水平進 t 的側邊（t 在下一列的旁邊欄；不走列間縫隙，避免貼到同列的橢圓）。"""
        self.edges.append(("DL", eid, s, t, label, sx))
    def P(self, eid, s, t, label="", exit=None, entry=None, pts=(), pos=None, vert=None):
        self.edges.append(("P", eid, s, t, label, exit, entry, pts, pos, vert))
    def close(self):
        f = self.f; g = f.gap; A = f.abs; RT = f.rt if hasattr(f, "rt") else {}
        f.rt = RT; ST = f.st if hasattr(f, "st") else {}; f.st = ST; RB = f.rb if hasattr(f, "rb") else {}; f.rb = RB
        def rh_off(cid, xr):
            """菱形底部出口的實際周界點比外框底端高 |0.5−xr|×h（標籤要放在外框之外才不壓菱形邊；review r4）。"""
            return abs(0.5 - xr) * A[cid][3] if ST.get(cid, "").startswith("rhombus") else 0.0
        nrows = max([b["row"] for b in self.boxes], default=-1) + 1
        rh = [max([b["h"] for b in self.boxes if b["row"] == r] or [0]) for r in range(nrows)]
        top = [0] * nrows; y = f.y + 30 + self.pad
        for r in range(nrows): top[r] = y; y += rh[r] + g
        bh = 30 + self.pad + sum(rh) + max(nrows - 1, 0) * g + self.pad
        if self.extra: bh = max(bh, max(yy + h for _, _, _, _, yy, _, h in self.extra) + self.pad)
        bx, by = f.bx, f.y
        f.cells.append(v(self.bid, "1", BAND, self.title, bx, by, f.bw, bh))
        if self.v2: f.cells.append(v(f"{self.bid}_v2", self.bid, TAG, "v2", f.bw - 44, 5, 30, 20))
        for b in self.boxes:
            cx, cw = f.cols[b["col"]]
            if b["ax"] == "c": x = cx + (cw - b["w"]) / 2
            elif b["ax"] == "l": x = cx
            elif b["ax"] == "r": x = cx + cw - b["w"]
            else: x = cx + b["ax"]
            yy = top[b["row"]] + (rh[b["row"]] - b["h"]) / 2
            A[b["id"]] = (x, yy, b["w"], b["h"]); RT[b["id"]] = top[b["row"]]; ST[b["id"]] = b["st"]; RB[b["id"]] = top[b["row"]] + rh[b["row"]]
            emit(f.cells, b["id"], self.bid, b["st"], b["text"], round(x - bx), round(yy - by), b["w"], b["h"])
            if "items" in b:                                    # 檔案容器：小框相對容器座標（cols 欄）
                iy = 26; nc = b["cols"]; cw = b["cw"]
                for i, (t, hh) in enumerate(b["items"]):
                    r, c = divmod(i, nc)
                    emit(f.cells, f"{b['id']}_{i}", b["id"], F12, t, 8 + sum(cw[:c]) + 6 * c, iy, cw[c], b["rows"][r])
                    if c == nc - 1 or i == len(b["items"]) - 1: iy += b["rows"][r] + 6
        for cid, st, text, x, yy, w, h in self.extra:
            emit(f.cells, cid, self.bid, st, text, x, yy, w, h); A[cid] = (bx + x, by + yy, w, h); RT[cid] = by + yy; ST[cid] = st
            if cid in getattr(self, "extra_items", {}):
                iy = 26
                for i, (t, hh) in enumerate(self.extra_items[cid]):
                    emit(f.cells, f"{cid}_{i}", cid, F12, t, 8, iy, w - 16, hh); iy += hh + 6
        for ed in self.edges:
            kind, eid, s, t = ed[:4]
            sx0, sy0, sw, sh = A[s]; tx0, ty0, tw, th = A[t]
            if kind == "H":
                _, _, _, _, label, sy = ed
                if tx0 > sx0: f.cells.append(e(eid, s, t, label, (1, sy), (0, sy)))
                else: f.cells.append(e(eid, s, t, label, (0, sy), (1, sy)))
            elif kind in ("D", "U"):
                _, _, _, _, label, sxr, txr, dy, al = ed
                ex, nx = sx0 + sxr * sw, tx0 + txr * tw
                if 1 <= abs(ex - nx) < 40 or (al and abs(ex - nx) >= 1):   # 小折角很醜：把出／入點對齊成一直線（先動目標入口，再動來源出口）
                    r = (ex - tx0) / tw                                      # 目標是菱形 → 入口只用頂點（entryX=0.5），不接斜邊（review r6）
                    if 0.1 <= r <= 0.9 and not ST.get(t, "").startswith("rhombus"): txr, nx = r, ex
                    else:
                        r = (nx - sx0) / sw
                        if 0.1 <= r <= 0.9 and not ST.get(s, "").startswith("rhombus"): sxr, ex = r, nx
                if kind == "D":
                    ey, ny = sy0 + sh, ty0; gy = RT[t] - g / 2 + dy; exit_, entry = (round(sxr, 3), 1), (round(txr, 3), 0)
                else:
                    ey, ny = sy0, ty0; gy = RT[s] - g / 2 + dy; exit_, entry = (round(sxr, 3), 0), (round(txr, 3), 0)
                if abs(ex - nx) < 1:
                    pos = None
                    if label:
                        off = rh_off(s, sxr) if kind == "D" else 0.0; L = off + abs(ny - ey)
                        pos = -0.6 if off < 1 else min(0.5, 2 * ((off + 12) / L) - 1)   # 菱形：標籤放到外框底端之下 12px
                    f.cells.append(e(eid, s, t, label, exit_, entry, vert=True if label else None, pos=pos))
                else:
                    pts = [(ex, gy), (nx, gy)]
                    L1, L2, L3 = abs(gy - ey), abs(nx - ex), abs(ny - gy); tot = L1 + L2 + L3
                    pos = 2 * ((L1 + L2 / 2) / tot) - 1
                    f.cells.append(_edge(eid, s, t, label, exit_, entry, pts, pos))
            elif kind == "R":
                _, _, _, _, label, busx, txr, dy, vert = ed
                ey = sy0 + sh / 2; gy = RT[t] - g / 2 + dy; nx = tx0 + txr * tw
                pos = None
                if label and vert:
                    L1 = abs(busx - (sx0 + sw)); tot = L1 + abs(gy - ey) + abs(nx - busx) + abs(ty0 - gy)
                    pos = 2 * ((L1 + 14) / tot) - 1
                f.cells.append(_edge(eid, s, t, label, (1, 0.5), (round(txr, 3), 0), [(busx, ey), (busx, gy), (nx, gy)], pos, vert if label else None))
            elif kind == "LD":
                _, _, _, _, label, busx, vert = ed
                ey = sy0 + sh / 2; txr = (busx - tx0) / tw
                pos = -0.7 if label else None
                if label and vert:
                    L1 = abs(sx0 - busx); tot = L1 + abs(ty0 - ey)
                    pos = 2 * ((L1 / 2) / tot) - 1 if vert == "below" else 2 * ((L1 + 14) / tot) - 1
                f.cells.append(_edge(eid, s, t, label, (0, 0.5), (round(txr, 3), 0), [(busx, ey)], pos, vert if label else None))
            elif kind == "UL":
                _, _, _, _, label, busx, row, dy = ed
                ex = sx0 + sw / 2; gy = top[row] - g / 2 + dy; ny = ty0 + th / 2
                f.cells.append(_edge(eid, s, t, label, (0.5, 0), (0, 0.5), [(ex, gy), (busx, gy), (busx, ny)], None))
            elif kind == "LL":
                _, _, _, _, label, busx = ed
                ey = sy0 + sh / 2; ny = ty0 + th / 2
                L1 = abs(sx0 - busx); tot = L1 + abs(ey - ny) + abs(tx0 - busx)
                pos = 2 * ((L1 + 14) / tot) - 1 if label else None
                f.cells.append(_edge(eid, s, t, label, (0, 0.5), (0, 0.5), [(busx, ey), (busx, ny)], pos, "left" if label else None))
            elif kind == "RD":
                _, _, _, _, label, txr = ed
                ey = sy0 + sh / 2; nx = tx0 + txr * tw
                L1 = abs(nx - (sx0 + sw)); tot = L1 + abs(ty0 - ey)
                if not label: pos, vert = None, None
                elif L1 >= 24: pos, vert = 2 * ((L1 / 2) / tot) - 1, "below"        # 水平段夠長：標籤放水平段下方
                else: pos, vert = 2 * ((L1 + 12) / tot) - 1, True                   # 水平段太短：標籤放垂直段右側
                f.cells.append(_edge(eid, s, t, label, (1, 0.5), (round(txr, 3), 0), [(nx, ey)], pos, vert))
            elif kind == "BL":
                _, _, _, _, label, busx, sxr = ed
                ex = sx0 + sxr * sw; gy = RB[s] + g / 2; ny = ty0 + th / 2
                f.cells.append(_edge(eid, s, t, label, (round(sxr, 3), 1), (1, 0.5), [(ex, gy), (busx, gy), (busx, ny)], None))
            elif kind == "LU":
                _, _, _, _, label, txr = ed
                ey = sy0 + sh / 2; nx = tx0 + txr * tw
                f.cells.append(_edge(eid, s, t, label, (1, 0.5), (round(txr, 3), 1), [(nx, ey)], -0.3 if label else None))
            elif kind == "DL":
                _, _, _, _, label, sxr = ed
                ex = sx0 + sxr * sw; ny = ty0 + th / 2; entry = (1, 0.5) if tx0 < sx0 else (0, 0.5)
                off = rh_off(s, sxr); L1 = ny - (sy0 + sh); L2 = abs(ex - (tx0 + tw if tx0 < sx0 else tx0))
                pos = 2 * ((off + max(L1 / 2, 12)) / (off + L1 + L2)) - 1   # 菱形：從外框底端再往下量
                f.cells.append(_edge(eid, s, t, label, (round(sxr, 3), 1), entry, [(ex, ny)], pos, vert=True))
            else:
                _, _, _, _, label, exit_, entry, pts, pos, vert = ed
                f.cells.append(_edge(eid, s, t, label, exit_, entry, pts, pos, vert))
        f.y = by + bh + 16
        return self

def _edge(eid, s, t, label, exit_, entry, pts, pos=None, vert=None):
    st = EDGE + f"exitX={exit_[0]};exitY={exit_[1]};exitDx=0;exitDy=0;entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
    if vert == "left": st += "align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;"
    elif vert == "below": st += "align=center;verticalAlign=top;spacingTop=6;spacingBottom=0;"
    elif vert: st += "align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;"
    arr = "".join(f'<mxPoint x="{round(px)}" y="{round(py)}"/>' for px, py in pts)
    xa = "" if pos is None else f' x="{pos:.2f}"'
    return (f'<mxCell id="{eid}" value="{esc(label)}" style="{st}" edge="1" parent="1" source="{s}" target="{t}">'
            f'<mxGeometry{xa} relative="1" as="geometry"><Array as="points">{arr}</Array></mxGeometry></mxCell>')

def pend(cells, text, x=1080, w=520, style=PENDR):
    h = fit_h(text, w, 40, 4)
    cells.append(v("pend", "1", style, text, x, 12, w, h)); return 12 + h

LEG1 = [(LEGEND_BOX(NEUTRAL), "淺灰：情境分組（無狀態意義）", 200, 60, 0), (RHOMBUS, "黃：判斷", 140, 64, 0),
        (ELLIPSE(GREEN), "綠：起點／終點", 140, 44, 8), (ELLIPSE(RED), "紅：失敗終止（拉不到／寫壞）", 190, 56, 2),
        (ELLIPSE(ORANGE), "橙：需要人動作（1／3 印指令；2 解衝突）", 210, 56, 2),
        (LEAF(), "白：步驟", 88, 40, 10), (FILE, "虛線框：專案裡的檔案", 170, 40, 10)]
LEG2 = [("entry", ENTRY, "虛線橢圓：跨頁入口", 200), ("note", NOTE, "便條：補充說明", 120), ("pend", PENDR, "黃便條：待拍板", 130), ("rule", RULE, "橘框：規則（已定）", 150),
        ("inv", INV, "紅粗框：不變量", 130), ("sub", SUB, "藍：引擎子命令（容器內）", 190), ("img", IMG, "紫：image（引擎與工具）", 170),
        ("hdr", HDR, "灰底：泳道／表格表頭", 170), ("v2", v2(W12), "右上綠標 v2：與 v1 不同處", 200), ("tree", FTREE, "虛線樹：目錄差異", 140)]
def terms2(prefix, x, y, rows, kw=150, vw=610, gap=40):
    """名詞表排兩欄（省高度）；id 沿用 {prefix}_tk{i}/_tv{i}。"""
    c = [v(f"{prefix}_th", "1", TEXT(13) + "align=left;fontStyle=1;", "本頁名詞", x, y - 34, 200, 28)]
    hs = [max(28, math.ceil(max(need_h(k, 12, kw), need_h(d, 12, vw)))) for k, d in rows]
    tot = sum(hs); acc = 0; split = len(rows)
    for i, h in enumerate(hs):
        acc += h
        if acc >= tot / 2: split = i + 1; break
    for cx, idx in ((x, range(0, split)), (x + kw + vw + gap, range(split, len(rows)))):
        cy = y
        for i in idx:
            k, d = rows[i]; h = hs[i]
            c.append(v(f"{prefix}_tk{i}", "1", TERM_K, k, cx, cy, kw, h)); c.append(v(f"{prefix}_tv{i}", "1", TERM_V, d, cx + kw, cy, vw, h)); cy += h
    return c
def foot(cells, prefix, y, rows, keys):
    """legend 兩列 + 本頁名詞（兩欄）。keys = 本頁用到的第二列圖例（每頁都有便條 → 一律含 note）。"""
    keys = set(keys) | {"note"}
    x = 40
    for i, (st, t, w, h, dy) in enumerate(LEG1):
        emit(cells, f"{prefix}_lg{i}", "1", _12(st), t, x, y + dy, w, h); x += w + 20
    cells.append(v(f"{prefix}_lgt", "1", TEXT(12) + "align=left;", "實線 = 執行順序（指向檔案時 = 寫入／讀取）", x, y, 300, 60))
    x = 40
    for k, st, t, w in LEG2:
        if k in keys: emit(cells, f"{prefix}_lgx_{k}", "1", st, t, x, y + 68, w, 36); x += w + 20
    cells += terms2(prefix, 40, y + 140, rows)

COLS5 = [("使用者", 40, 220), ("啟動器（主機 sh）", 280, 280), ("引擎容器", 580, 400), ("GHCR", 1000, 220), ("專案目錄", 1240, 360)]
COLS7 = [("使用者", 40, 220), ("Renovate（GitHub 上）", 280, 180), ("啟動器（主機 sh）", 480, 240), ("引擎容器", 740, 360), ("GHCR", 1120, 180), ("專案目錄", 1320, 280)]
COLS5W = [("使用者", 40, 220), ("啟動器（主機 sh）", 280, 320), ("引擎容器", 620, 380), ("GHCR", 1020, 200), ("專案目錄", 1240, 360)]   # 啟動器欄要兩條車道（判斷＋pull）的頁
COLS5B = [("使用者", 40, 220), ("啟動器（主機 sh）", 280, 460), ("引擎容器", 760, 260), ("GHCR", 1040, 180), ("專案目錄", 1240, 360)]   # bootstrap.sh：啟動器兩條車道各 200
COLS5I = [("使用者", 40, 220), ("啟動器（主機 sh）", 280, 140), ("引擎容器", 440, 560), ("GHCR", 1020, 200), ("專案目錄", 1240, 360)]   # install（2）：引擎欄三條車道
U, L, E, G, P, RN = "使用者", "啟動器（主機 sh）", "引擎容器", "GHCR", "專案目錄", "Renovate（GitHub 上）"
ALL = {"note", "pend", "rule", "inv", "sub", "img", "hdr", "v2", "tree"}   # "entry" 只在有跨頁入口的頁加
EXIT3 = ("結束狀態 0／1／2／3", "0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）")
def newpage(cells_title, note, cols, note_style=NOTE):
    cells = [v("title", "1", TITLE, cells_title, 40, 20, 1000, 34)]
    ny = pend(cells, note, style=note_style)
    F = Flow(cells, cols); F.headers(ny + 8)
    return cells, F
pages_v1_b = []

# ================= 第十三輪共用（頁內；helper 段不動；v2.15-1～6、r12_codex/findings1–4）=================
# 1. 名詞換新（v2.15-1、decisions/review/terms.md）：TR() 對照表；用「包住」helper 的方式套到每格文字、線標籤、名詞表、頁名（helper 本體不改；
#    box/free/files 在算高度前先換，v() 再換一次 → 規則一律冪等）。第 0 頁已有的詞不再進各頁名詞表（BM_T／MD_T／SYM_T／FROZEN_T／INIT_T／VL_T／EXIT3… 移除）。
# 2. 執行紀錄改圖例約定（v2.15-2）：不畫 launcher_exit／log_prune 扇出格與各段 engine_start 格；圖例加兩條隱含約定（foot()）；
#    只留啟動器起點「建執行紀錄、寫 launcher_started（失敗 → 1 + 6-38）」一格，其失敗畫紅出口；終點直接接各自分支（footer()/footer_edges() 重寫：無匯流）。
# 3. 跨頁出入口一律白虛線橢圓 ENTRY（v2.15-3）：入口「來自「X」頁」、出口「續「X」頁」。
# 4. vk-resolve/1 只傳協定內容（v2.15-4）：RES_OUT 固定文字；resolve 非 0 → 啟動器不讀 stdout（NZ_T）；apply 多「原 argv 與計畫一致？」一格（ARGV_T）。
# 5. 詢問格三出口（v2.15-6）：共用小圖示 tty()（橙小標「無 tty→1+6-4」貼在問句格右上；圖例 tty）。
import re as _re
_TR = [
 (r"工具 repo", "下游 repo"), (r"工具 image", "下游 image"), (r"使用者的檔", "專案檔"), (r"使用者檔", "專案檔"), (r"你的檔", "專案檔"),
 (r"(?<!下游)使用者", "下游使用者"), (r"下游專案", "專案"),
 (r"正規行", "版本鎖定行"), (r"(?<!版本)鎖定行", "版本鎖定行"),
 (r"(?<![:/A-Za-z_.])baseline(?![/:_.A-Za-z])", "基準版"),
 (r"進度日誌", "進度檔"), (r"操作紀錄檔", "執行紀錄"), (r"建 log 檔並寫", "建執行紀錄、寫"), (r"(?<![A-Za-z_])log 檔", "執行紀錄"),
 (r"CI 為真（frozen）", "CI 模式"), (r"frozen（CI 為真）", "CI 模式"), (r"（frozen）", ""), (r"非 frozen", "非 CI 模式"), (r"frozen", "CI 模式"),
 (r"CI 不為真", "非 CI 模式"), (r"CI 為真", "CI 模式"), (r"需改 tracked 檔", "需改任何進 git 的檔"), (r"tracked 五檔", "進 git 的五檔"),
 (r"tracked 檔", "進 git 的檔"), (r"tracked 薄殼", "進 git 的薄殼"), (r"tracked", "進 git 的"),
 (r"協定號", "介面版"), (r"協定不合", "介面版不合"), (r"schema 號", "檔案版"), (r"(?<![A-Za-z_])floor(?![A-Za-z_])", "最低介面版"),
 (r"materialize", "取件"), (r"需要人動作", "需人處理"), (r"自身升級", "升引擎"),
 (r"薄殼首行自描述", "薄殼自描述首行"), (r"首行自描述", "自描述首行"),
 (r"launcher_started", "launcher_start"), (r"engine_started", "engine_start"),                      # v2.16-3：事件名回歸 spec §4.10 註冊表
 (r"launcher_completed\|failed", "launcher_exit"), (r"engine_completed\|failed", "engine_exit"),
]
_TRC = [(_re.compile(p), r) for p, r in _TR]
def TR(s):
    """名詞對照（冪等）；非字串原樣回傳。"""
    if not isinstance(s, str) or not s: return s
    for p, r in _TRC: s = p.sub(r, s)
    return s

if not globals().get('_TR_WRAPPED'):   # 冪等：同一 namespace 重複 exec（gen_disc 先經 disc_v1_c 再 exec 本檔）時不可重包，否則 v→v 無限遞迴
    _box0, _free0, _files0, _ffiles0 = _Band.box, _Band.free, _Band.files, _Band.free_files
    _v0, _e0, _edge0, _pend0, _newpage0 = v, e, _edge, pend, newpage
    _TR_WRAPPED = True
def _box1(self, cid, col, row, style, text, w, *a, **k): return _box0(self, cid, col, row, style, TR(text), w, *a, **k)
def _free1(self, cid, style, text, x, y, w, *a, **k): return _free0(self, cid, style, TR(text), x, y, w, *a, **k)
def _files1(self, cid, col, row, title, items, w, *a, **k): return _files0(self, cid, col, row, TR(title), [TR(t) for t in items], w, *a, **k)
def _ffiles1(self, cid, title, items, x, y, w): return _ffiles0(self, cid, TR(title), [TR(t) for t in items], x, y, w)
_Band.box, _Band.free, _Band.files, _Band.free_files = _box1, _free1, _files1, _ffiles1
def v(id, parent, style, value, x, y, w, h): return _v0(id, parent, style, TR(value), x, y, w, h)
def e(id, src, tgt, label="", *a, **k): return _e0(id, src, tgt, TR(label), *a, **k)
def _edge(eid, s, t, label, *a, **k): return _edge0(eid, s, t, TR(label), *a, **k)
def pend(cells, text, x=1080, w=520, style=PENDR): return _pend0(cells, TR(text), x, w, style)
def newpage(cells_title, note, cols, note_style=NOTE):
    """第十四輪（v2.16-18）：沿革便條全刪 —— note 參數保留簽名但不畫；表頭直接接在頁標題下。"""
    cells = [v("title", "1", TITLE, cells_title, 40, 20, 1000, 34)]
    F = Flow(cells, cols); F.headers(64)
    return cells, F
def addpage(pid, name, cells): pages_v1_b.append((pid, TR(name), cells))

# ---------- 圖例（第十三輪）：跨頁出入口、tty 小標、兩條隱含約定 ----------
TTY = ("rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=9;fontStyle=1;align=center;verticalAlign=middle;"
       "spacing=0;spacingLeft=0;spacingRight=0;spacingTop=0;spacingBottom=0;")
TTY_TXT = "無tty→6-4"
def tty(F, cells, *ids):
    """問句格（菱形／步驟）左上角加橙小標「無 tty→1+6-4」= 第三出口（v2.15-6 共用小圖示；圖例 tty）。close() 之後呼叫。"""
    for cid in ids:
        x, y, w, h = F.abs[cid]
        cells.append(v(f"{cid}_tty", "1", TTY, TTY_TXT, round(x), round(y - 10), 76, 20))   # 左上角（菱形頂點在中央，右上有 v2 標）
LEG2 = [("entry", ENTRY, "白虛線橢圓：跨頁出入口", 220), ("note", NOTE, "便條：補充說明", 120), ("pend", PENDR, "黃便條：待拍板", 130),
        ("rule", RULE, "橘框：規則（已定）", 130), ("inv", INV, "紅粗框：不變量", 120), ("sub", SUB, "藍：引擎（容器內）做的", 160), ("img", IMG, "紫：image", 100),
        ("hdr", HDR, "灰底：泳道／表頭", 130), ("v2", v2(W12), "右上綠標 v2：與 v1 不同", 180), ("tree", FTREE, "虛線樹：目錄差異", 140),
        ("tty", TTY, "橙小標：問句無 tty／EOF 且無 -y → 1 + 6-4（Ctrl-C 中止、不記拒絕）", 300)]
LEG_IMPL = ("圖例約定（v2.15-2、v2.16-3）：每個終點橢圓隱含 —— 啟動器結束前已寫 log_prune、launcher_exit（結束碼、耗時）；"
            "每個「docker run 引擎」格隱含 —— 容器開始寫 engine_start、結束寫 engine_exit（同一執行紀錄；事件名 = spec §4.10 註冊表）。白 = 啟動器（主機）做的。")
def foot(cells, prefix, y, rows, keys):
    """legend 兩列 + 兩條隱含約定 + 本頁名詞（兩欄；只列第 0 頁沒有的頁內特有詞）。"""
    keys = set(keys) | {"note"}
    x = 40
    for i, (st, t, w, h, dy) in enumerate(LEG1):
        emit(cells, f"{prefix}_lg{i}", "1", _12(st), t, x, y + dy, w, h); x += w + 20
    cells.append(v(f"{prefix}_lgt", "1", TEXT(12) + "align=left;", "實線 = 執行順序（指向檔案時 = 寫入／讀取）", x, y, 300, 60))
    x = 40
    for k, st, t, w in LEG2:
        if k in keys: emit(cells, f"{prefix}_lgx_{k}", "1", st, t, x, y + 68, w, 36); x += w + 20
    cells.append(v(f"{prefix}_lgi", "1", TEXT(12) + "align=left;", LEG_IMPL, 40, y + 108, 1540, 40))
    cells += terms2(prefix, 40, y + 188, [(TR(k), TR(d)) for k, d in rows])

# ---------- 共用名詞（只留第 0 頁沒有的；term-diff：同名各頁同文） ----------
LOGT = [   # 執行紀錄（第 0 頁已有）不再列；只留 config.toml 與 6-38
 ("config.toml（install／uninstall）", ".vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 建（含註解）＋ 基準版副本 baseline/vendor_kit/config.toml；升引擎時三方合併；uninstall 只在 hash == 副本時刪；缺檔或缺鍵 = 預設"),
 ("6-38", "執行紀錄建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log"),
]
RA_T = ("resolve／apply 兩段", "動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1（pull／extract／mount 清單、apply|yes／no、指紋；不寫檔）→ 啟動器 docker 拉到暫存 → apply 拿鎖、重驗指紋、驗原 argv 與計畫一致、建進度檔、寫檔、最後刪進度檔；細節 p3b 契約④")
RAD_T = ("resolve／apply／--dry-run", "resolve 只讀只算（查目標版或讀 metadata、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫；--dry-run = apply 的唯讀預覽（要先拉 image；本機 → 0；CI 模式且需改任何進 git 的檔 → 1）")
FIP_T = ("flock／指紋", "flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest 等（算法見 add（1）頁「輸入指紋」），apply 拿鎖後重驗，不同 → 1 + 6-12「請重跑」（橙）")
GM_T = ("git merge-file --diff3", "git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 結束碼 2（需人處理，橙）；多工具（Q27）兩者皆回 2 時訊息全部列出")
GS_T = ("gen/.stamp", "只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；本機覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 版本鎖定行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行")
BDN_T = ("B／D／N", "B = 基準版（上次合併時的初始檔原版副本，進 git）；D = 現況（專案裡你的那份檔）；N = 新版初始檔 = 啟動器把目標版 image 展開到暫存、掛進引擎的 /dist/<repo>（不是 cache；v2.5 §2）；「D==B」= 你沒改過")
BOOT_T = ("bootstrap.sh 檔名與內嵌 ref", "release 附的 POSIX sh，內嵌所屬引擎的完整 ref（ghcr.io/<org>/vendor_kit:vN@sha256:<index digest>）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local <tar>")
GT_T = ("gen/tools.just／mod?", "不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生，最後寫、與 cache 同一 apply 內原子替換（I17）；裡面沒有 recipe")
E2B_T = ("6-2b", "第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（.tmp.upgrade 進度檔保留）")
PULLX_T = ("6-24／6-31（pull 失敗）", "docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）；docker create／cp／rm 或暫存目錄失敗同樣 → 1 停止")
E22_T = ("6-22（upgrade 逐檔問句）", "「<X> 換成新版？」／「你和新版都改了 <X>，要三方合併嗎？」／「要建 <X> 嗎」／「<X> 是二進位檔，要換成新版嗎？」；config.toml 三方合併也用它；-y 免問")
REN_T = ("Renovate", "GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：有新版就開 PR 改 version.toml 那一行；見「A. Renovate 路徑」頁")
E33_T = ("6-33（未完成交易）", "唯讀動詞偵測到 .tmp.<verb>.*.toml 或 metadata [progress] in-progress → 只印「偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>」，不自動恢復、不寫檔；sync／update 結束 1，help 仍 0")
E4_T = ("6-4（無 tty）", "需詢問但無 tty／EOF 且無 -y → 1：「需要確認但沒有終端可互動。請加 -y，或在終端執行。」；Ctrl-C 中止整個 apply 回 1、不套用、不記拒絕（declined 只記明確回答「否」）")
E12_T = ("6-12（指紋不同）", "apply 拿鎖後重驗指紋不同（中間有人改了）→ 1：「專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit <verb> …」；原 argv 與計畫不一致也 → 1")
MSG_T = ("6-16／6-23／6-28／6-35", "前置檢查訊息：6-16 不在 git repo 內（請先 git init）；6-23 just 版本不足（印安裝指令）；6-28 薄殼被改過，列差異不動；6-35 禁止巢狀（上層或下層已有 .vendor_kit/）")
NZ_T = ("resolve 非 0", "resolve 容器結束碼非 0（1／2／3）→ 啟動器不讀 stdout、不跑任何 docker／apply，原碼傳出；stdout 文法不合 → 1 + 6-30（§3.3）")
ARGV_T = ("原 argv 與計畫一致", "apply 讀 /dist/vk-resolve（啟動器把 resolve 的 stdout 整份存成 .tmp.dist.<id>/vk-resolve 掛入）：重算指紋 ≠ 計畫的 fingerprint → 1 + 6-12；本次 argv 與計畫不一致 → 1；apply 不重新選最新版（§3.2）")
N5I = "已定（v2.4 Q17、v2.5 §8、v2.6、v2.13 P5、v2.15-11）：install 第一次／修復判定用薄殼自描述首行；進度檔在第一個寫入（含暫存檔）之前建；修復型 config.toml 缺才建（含基準版副本與 metadata state=managed）、存在不動；根 justfile／.dockerignore 無則建、有則問後才加、symlink 不寫只印指示；引擎 image 一律先 docker image inspect，本機有就不 pull。"
LS_T = "建執行紀錄、寫 launcher_start（失敗 → 1 + 6-38，零寫入）"     # （第十四輪改用 lstart() 拆兩格；此常數只留給舊引用）
LS1 = "寫 launcher_start（失敗 → 1 + 6-38，零寫入）"                    # 啟動器起點第二格（v2.16-19）
LSX = "1 + 6-38：執行紀錄建不了／寫不進（零寫入）"                    # 其紅出口
E27X = "1 + 6-27：恢復失敗（未恢復：<檔名>，逐檔列出）"                # 共通前置格的紅出口（v2.16-1）
E33X = "1 + 6-33：偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>"   # 唯讀動詞（sync／update）
E26X = "1 + 6-26：專案目錄被鎖定（PID <pid>，自 <time>）；60 秒內未釋放"   # flock 逾時出口（每個 apply 頁都有）
NZX = "1／2／3：resolve 非 0 → 原碼傳出（不讀 stdout、不跑 docker／apply）"   # resolve 三叉（v2.16-2）第一叉
E30X = "1 + 6-30：引擎輸出不完整或不相容，未執行任何動作（stdout 文法不合）"   # 第二叉
RES_OUT = "stdout vk-resolve/1：pull／extract／mount 清單、apply|yes、指紋（只傳協定內容）"   # v2.15-4
NZ_X = "1／2／3：resolve 非 0（啟動器不讀 stdout、不跑 docker／apply）"
ARGV_Q = "原 argv 與計畫一致？"
E64 = "1 + 6-4：無 tty／EOF 且無 -y（Ctrl-C 中止、不記拒絕）"

def footer(b, F, row, ends, spacer=0, sp="r"):
    """終點列（第十三輪：各分支直接接自己的終點，無匯流）。spacer > 0 → 第 row 列放透明佔位格（高 16×spacer+12），給左右匯流排的
    水平段分層用，終點放 row+1；否則終點放 row。sp = 佔位格放哪（不能被水平段穿過）：'r' 專案目錄欄右緣（只有左側來源時）、
    'l' 下游使用者欄左緣（只有右側來源時）、'm' GHCR 與專案目錄欄之間（兩側都有；右側終點須放 P 欄）。
    ends: [(cid, style, text)] 依序放槽位 U、L、E-l、E-r、G、P（欄寬 ≥ 180；E ≥ 360 兩槽），或 (cid, style, text, col, ax) 指定位置。回傳終點所在列。"""
    r0 = row
    if spacer:
        hh = 16 * spacer + 12
        col, ax = {"r": (P, "r"), "l": (U, "l"), "m": (G, F.cols[G][1] + 5)}[sp] if sp != "m" or G in F.cols else (E, F.cols[E][1] + 5)
        b.box("_sp", col, row, "text;html=1;fillColor=none;strokeColor=none;", "", 10, h=hh, minh=hh, ax=ax); r0 = row + 1
    slots = []
    for col in (U, L, E, G, P):
        if col not in F.cols: continue
        cx, cw = F.cols[col]
        if col == E and cw >= 360:
            sw = min(220, (cw - 20) // 2); slots += [(col, "l", sw), (col, "r", sw)]
        elif cw >= 180: slots.append((col, "c", min(220, cw)))
    i = 0
    for en in ends:
        cid, st, text = en[:3]
        if len(en) > 3: b.box(cid, en[3], r0, st, text, 220, ax=en[4])
        else:
            col, ax, sw = slots[i % len(slots)]; b.box(cid, col, r0 + i // len(slots), st, text, sw, ax=ax); i += 1
    return r0

def footer_edges(F, srcs, busl=None, busr=None, dlevel=0):
    """close() 之後畫終點線。srcs: [(eid, src, label, how, end[, sx])]：
      'l'／'lb' 左出（'lb' 從底端 sx 出、經該列底縫隙）→ 左匯流排 → 分層水平段 → 終點頂端；'r'／'rb' 右側同理；'d' 從底端直下（不對齊時在終點上方縫隙折一次）。
    分層：同側依來源由上到下排序，最上面的用最外側匯流排、最低的水平層、最左（右側：最右）的終點 → 不交叉（頁內終點順序須照這規則排）。"""
    A, RT, RB, g = F.abs, F.rt, F.rb, F.gap
    if busl is None: busl = F.cols[U][0] - 10
    if busr is None: busr = F.cols[P][0] + F.cols[P][1] + 10
    def rh_off(cid, xr): return abs(0.5 - xr) * A[cid][3] if F.st.get(cid, "").startswith("rhombus") else 0.0
    ends = {s[4] for s in srcs}; ytop = min(RT[en] for en in ends) if ends else 0
    for side in ("l", "r"):
        grp = sorted([s for s in srcs if s[3] in (side, side + "b")], key=lambda s: (A[s[1]][1], A[s[1]][0]))
        n = len(grp)
        for i, it in enumerate(grp):
            eid, s, label, how, en = it[:5]; sxr = it[5] if len(it) > 5 else 0.5
            sx0, sy0, sw, sh = A[s]; tx0, ty0, tw, th = A[en]; nx = tx0 + tw / 2
            busx = (busl - 14 * (n - 1 - i)) if side == "l" else (busr + 14 * (n - 1 - i))
            lev = ytop - g / 2 - 12 - 16 * i
            if how in ("l", "r"):
                left = side == "l"; ex = sx0 if left else sx0 + sw; ey = sy0 + sh / 2
                pts = [(busx, ey), (busx, lev), (nx, lev)]
                tot = abs(ex - busx) + abs(lev - ey) + abs(nx - busx) + abs(ty0 - lev)
                F.cells.append(_edge(eid, s, en, label, (0 if left else 1, 0.5), (0.5, 0), pts, 2 * (14 / tot) - 1 if label else None, "below" if label else None))
            else:
                ex = sx0 + sxr * sw; gy = RB[s] + g / 2; pts = [(ex, gy), (busx, gy), (busx, lev), (nx, lev)]
                off = rh_off(s, sxr); L1 = gy - (sy0 + sh); tot = off + L1 + abs(ex - busx) + abs(lev - gy) + abs(nx - busx) + abs(ty0 - lev)
                F.cells.append(_edge(eid, s, en, label, (round(sxr, 3), 1), (0.5, 0), pts, 2 * ((off + max(L1 / 2, 12)) / tot) - 1 if label else None, True if label else None))
    for it in srcs:
        eid, s, label, how, en = it[:5]; sxr = it[5] if len(it) > 5 else 0.5
        if how != "d": continue
        sx0, sy0, sw, sh = A[s]; tx0, ty0, tw, th = A[en]; ex = sx0 + sxr * sw; nx = tx0 + tw / 2
        if abs(ex - nx) < 1 or (tx0 + 0.1 * tw <= ex <= tx0 + 0.9 * tw and not F.st.get(en, "").startswith("ellipse")):
            txr = round((ex - tx0) / tw, 3); off = rh_off(s, sxr); L1 = ty0 - (sy0 + sh)
            F.cells.append(_edge(eid, s, en, label, (round(sxr, 3), 1), (txr, 0), [], (2 * ((off + 12) / (off + L1)) - 1) if label else None, True if label else None))
        else:
            gy = RT[en] - g / 2 + dlevel; pts = [(ex, gy), (nx, gy)]; off = rh_off(s, sxr); L1 = gy - (sy0 + sh); tot = off + L1 + abs(nx - ex) + (ty0 - gy)
            F.cells.append(_edge(eid, s, en, label, (round(sxr, 3), 1), (0.5, 0), pts, 2 * ((off + max(L1 / 2, 12)) / tot) - 1 if label else None, True if label else None))

def bypass(F, cells, eid, s, t, label="有", busx=None):
    """close() 後畫：inspect 菱形「本機有」→ 跳過 pull 直接到 t：s 右側出線 → 頁面右側匯流排（預設專案目錄欄左 10px）→ t 上方縫隙 → t 頂端。"""
    A = F.abs; busx = busx or F.cols[P][0] - 10
    sx0, sy0, sw, sh = A[s]; tx0, ty0, tw, th = A[t]
    ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tw / 2
    tot = (busx - (sx0 + sw)) + (gy - ey) + (busx - nx) + (ty0 - gy)
    cells.append(_edge(eid, s, t, label, (1, 0.5), (0.5, 0), [(busx, ey), (busx, gy), (nx, gy)], 2 * (14 / tot) - 1 if label else None, "below" if label else None))

def pullseg(b, row, ids, texts, nxt, w=(260, 200, 280), imgw=180):
    """啟動器 image 段（三格同中心直下，pull 失敗從左側出線）：row inspect 菱形；row+1 pull 白格 + GHCR 欄 image；nxt 放 row+2。
    契約④（v2.15-10）：inspect 本機已有 → 跳過 pull（bypass()）；只有 extract kind 才 create／cp。"""
    qi, pi, gi = ids; qt, pt, gt = texts
    b.box(qi, L, row, v2(D12), qt, w[0]); b.box(pi, L, row + 1, v2(W12), pt, w[1]); b.box(gi, G, row + 1, IMG, gt, imgw)
    b.box(nxt[0], L, row + 2, nxt[1], nxt[2], w[2])
    b.D(f"{qi}_n", qi, pi, "無", al=True); b.H(f"{gi}_p", gi, pi, "拉" if "vendor_kit" in gt else "拉 /dist"); b.D(f"{pi}_x", pi, nxt[0], al=True)

def sidebus(F, cells, eid, s, t, label="", busx=0, side="l", tx=0.5, pos=-0.7, vert="left"):
    """close() 後畫：s 側邊出線 → x=busx 匯流排往下 → t 上方縫隙 → t 頂端 tx 處（菱形用 0.5 = 頂點）。跳過中間幾列的分支線。"""
    A = F.abs; sx0, sy0, sw, sh = A[s]; tx0, ty0, tw, th = A[t]
    ey = sy0 + sh / 2; gy = F.rt[t] - F.gap / 2; nx = tx0 + tx * tw

codex
我會只改 `disc_v1_b.py` 中 v1p8b、v1p7bcc、v1p7bccd 三頁；先依 implement skill 的工作流程確認基線與定位三頁，再逐條修正，最後完整跑你指定的產圖、六項幾何檢查與 lint。
exec
/usr/bin/bash -lc "sed -n '1,240p' /home/cyc/.agents/skills/implement/SKILL.md && python3 run_v1_b.py" in <scratchpad>
 succeeded in 107ms:
v1p5 流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別 page ('1660', '1919')
v1p5x 流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版 page ('1660', '1311')
v1p5i 流程 v2：bootstrap.sh（1′）docker run install page ('1660', '1364')
v1p5ccc 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add page ('1660', '1878')
v1p5c 流程 v2：install（1）主機檢查 → 引擎 image → docker run page ('1660', '1606')
v1p5cm 流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存 page ('1660', '1734')
v1p5cw 流程 v2：install（1″）寫入 page ('1660', '1808')
v1p5cc 流程 v2：install（2）根 justfile 與 .dockerignore page ('1660', '2014')
v1p5b 流程 v2：add（1）resolve → docker page ('1660', '2273')
v1p5bcc 流程 v2：add（1′）apply 前置 page ('1660', '2219')
v1p5bc 流程 v2：add（2）apply 寫入段 page ('1660', '2301')
v1p6 流程 v2：sync（1）啟動器快路徑 page ('1660', '2124')
v1p6cc 流程 v2：sync（1′）引擎 resolve page ('1660', '2395')
v1p6c 流程 v2：sync（2）三叉 → docker → apply 前置 page ('1660', '1636')
v1p6cw 流程 v2：sync（2′）apply 寫入段 page ('1660', '1594')
v1p7 流程 v2：upgrade ── A. Renovate 路徑 page ('1660', '1821')
v1p7c 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker page ('1660', '2363')
v1p7ccc 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置 page ('1660', '2349')
v1p7cc 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併 page ('1660', '2394')
v1p7cccc 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入 page ('1660', '1569')
v1p7b 流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入 page ('1660', '2371')
v1p7bd 流程 v2：upgrade ── D. 回退 page ('1660', '2290')
v1p7bc 流程 v2：upgrade ── E. 升引擎 (a)(b) page ('1660', '2140')
v1p7bca 流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手 page ('1660', '1673')
v1p7bcc 流程 v2：upgrade ── E(c) upgrade vendor_kit（1） page ('1660', '2340')
v1p7bcx 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′） page ('1660', '1639')
v1p7bccc 流程 v2：upgrade ── E(c) upgrade vendor_kit（2） page ('1660', '1537')
v1p7bcce 流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml page ('1660', '2181')
v1p7bccd 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′） page ('1660', '1241')
v1p8 流程 v2：dev <repo> page ('1660', '2094')
v1p8ccc 流程 v2：dev vendor_kit page ('1660', '2121')
v1p8c 流程 v2：undev <repo>（1）resolve → apply 前置 page ('1660', '2178')
v1p8cx 流程 v2：undev <repo>（2）寫入段 page ('1660', '1315')
v1p8cc 流程 v2：undev vendor_kit page ('1660', '2303')
v1p8b 流程 v2：remove（1）resolve → apply 前置 page ('1660', '2322')
v1p8bccc 流程 v2：remove（2）寫入段 page ('1660', '2167')
v1p8bc 流程 v2：uninstall（1）resolve → apply 前置 page ('1660', '2394')
v1p8bcc 流程 v2：uninstall（2）寫入段 page ('1660', '2261')

exec
/usr/bin/bash -lc "git status --short && rg -n '"'^# =+ .*v1p(8b|7bccd?|5c|8cc|8bc)|addpage'"\\(\"v1p(8b|7bccd?)\"|me8ax|se12f|se11y|s13h|m3|u3|w3' disc_v1_b.py" in <scratchpad>
 exited 128 in 0ms:
fatal: not a git repository (or any of the parent directories): .git

exec
/usr/bin/bash -lc "rg -n '"'^# =+ .*v1p(8b|7bccd?|5c|8cc|8bc)|addpage'"\\(\"v1p(8b|7bccd?)\"|me8ax|se12f|se11y|s13h|m3|u3|w3' disc_v1_b.py" in <scratchpad>
 succeeded in 0ms:
1293:b.box("m3e", E, 0, ENTRY, "來自「sync（2）」頁：apply 前置通過（已寫 launcher_start）", 400)
1294:b.box("m3", E, 1, v2(SUB), fl("逐待辦工具：取件 /dist/<repo> 展開到暫存目錄"), 400)
1295:b.box("m3c", E, 2, v2(SUB), fl("暫存 → cache/<repo>/（原子替換）"), 400)
1296:b.box("m3f", P, 2, F12, "cache/<repo>/（重寫，不進 git）", 360)
1297:b.box("m3b", E, 3, v2(SUB), fl("寫印記 gen/<repo>.stamp（第一行 index digest，之後每檔 sha256）"), 400)
1298:b.box("m3bf", P, 3, F12, "gen/<repo>.stamp（重寫，不進 git）", 360)
1299:b.box("m3vd", E, 4, v2(D12), "逐檔驗？（--verify／CI 模式／版本變動的那次）", 400, ax="l")
1300:b.box("m3v", E, 5, v2(SUB), fl("是：逐檔 sha256 驗 cache/<repo>/ ＝ 印記（§3.6）"), 400)
1301:b.box("m3vq", E, 6, v2(D12), "全部相符？", 200, ax="l")
1302:b.box("m3vn", E, 6, v2(SUB), fl("否：重裝該工具一次（並印 cache 被改過的 warn）"), 150, ax="r")
1303:b.box("m3v2", E, 7, v2(SUB), fl("再逐檔驗一次"), 150, ax="r")
1304:b.box("m3x2", G, 8, v2(R12), fl("1：重裝後仍不符（取件／寫入／驗證失敗），不再重裝"), 200)
1305:b.box("m3vq2", E, 8, v2(D12), "相符？", 150, ax="r")
1311:b.D("me3", "m3e", "m3")
1312:b.D("me3c", "m3", "m3c"); b.H("me4", "m3c", "m3f", "寫"); b.D("me4b", "m3c", "m3b"); b.H("me4f", "m3b", "m3bf", "寫"); b.D("me4v", "m3b", "m3vd", al=True)
1313:b.D("me4vy", "m3vd", "m3v", "是", al=True)
1314:b.D("me4q", "m3v", "m3vq", al=True); b.H("me4n", "m3vq", "m3vn", "否"); b.D("me5", "m3vq", "mq", "是", al=True)
1315:b.D("me5n", "m3vn", "m3v2"); b.D("me5v2", "m3v2", "m3vq2", al=True); b.H("me5x2", "m3vq2", "m3x2", "否"); b.D("me5y2", "m3vq2", "mq", "是", 0.5, 0.5)
1316:b.LL("me6y", "mq", "m3", "是：下一個工具", busx=545); b.D("me6n", "mq", "m5q", "否", al=True)
1319:failbus(F, p6cw, ["m3", "m3c", "m3b", "m3vn", "m5"], "m7x")
1321:sidebus(F, p6cw, "me4vn", "m3vd", "mq", "否：跳過逐檔驗", busx=565, tx=0.5, pos=-0.9, vert="below")
1804:b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
1808:bypass(F, p7bcc, "se11y", "s11n", "s11v")
1809:sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
1814:_rb("se12jrv", "s12jr", "s12d1", ""); _rb("se12ttv", "s12tt", "s12d1", ""); _rb("se12fzv", "s12fz", "s12d1", ""); _rb("se12d1n", "s12d1", "s12v", "否")
1816:addpage("v1p7bcc", "流程 v2：upgrade ── E(c) upgrade vendor_kit（1）", p7bcc)
1936:b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
1943:b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
1948:addpage("v1p7bccd", "流程 v2：upgrade ── E(c) upgrade vendor_kit（2′）", p7bce)
2052:b.box("u3", U, 4, G12, "0：未啟用 dev（提示）", 220)
2069:b.H("ue1", "u0", "u0l0"); b.D("ue1l", "u0l", "upq", al=True); b.H("ue1e", "u1", "u1e"); b.D("ue2", "u1e", "u2", al=True); b.H("ue3", "u2", "u3", "否"); b.D("ue4", "u2", "u4b", "是", 0.5, 0.5)
2121:b.box("w3", U, 4, G12, "0：未啟用（提示）", 220)
2144:b.H("we1", "w0", "w0l0"); b.D("we1l", "w0l", "wpq", al=True); b.H("we1e", "w1", "w1e"); b.D("we2", "w1e", "w2q", al=True); b.H("we2n", "w2q", "w3", "否"); b.D("we2y", "w2q", "w2s", "是", 0.5, 0.5); b.D("we2s2", "w2s", "w2s2")
2183:b.box("m3", U, 4, G12, "0：未接入（提示）", 220)
2205:b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
2207:b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
2211:addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)

exec
/usr/bin/bash -lc "sed -n '1725,1825p' disc_v1_b.py; sed -n '1885,1960p' disc_v1_b.py; sed -n '2150,2220p' disc_v1_b.py; rg -n '逾時.*6-26|6-26.*逾時|ax.*6-26' disc_v1_b.py | head -30" in <scratchpad>
 succeeded in 0ms:
b.D("se2so", "s2so", "s2q0", "", 0.5, 0.5)
b.H("se6px", "s2lp", "s2lx", "失敗")
b.D("se6lv", "s2lo", "s2lv", "是", al=True); b.H("se6vx", "s2lv", "s2lvx", "是"); b.D("se6vr", "s2lv", "s2ln", "否", al=True)
b.close()
bypass(F, p7bc, "se6y", "s2ln", "s2r")
sidebus(F, p7bc, "se3", "s2q", "s2so", "是", busx=610, tx=0.15, pos=-0.6, vert="below")
sidebus(F, p7bc, "se6lo", "s2lo", "s2ln", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
pend(p7bc, "待處理問題\n• se6vr：本機 image ID 相符時直接跳過 pull 的新路徑待重新配置")
foot(p7bc, "p7bc", F.y, _k7e("多工具", "docker image inspect", "6-27", "6-30", "resolve 非 0") + [PULLX_T], ALL - {"inv", "tree", "rule"} | {"entry"})
addpage("v1p7bc", "流程 v2：upgrade ── E. 升引擎 (a)(b)", p7bc)

# ================= P7bca：upgrade ── E. 升引擎 (a′) 舊引擎 apply 改第一行 → 啟動器接手 =================
p7bca, F = newpage("流程 v2：upgrade ── E. 升引擎 (a′) 舊引擎 apply 改第一行 → 啟動器 grep 第一行 → 接手新引擎（§3.4）", "", COLS5W)
b = F.band("uEa", "E(a′)（承「E. 升引擎 (a)(b)」頁：新引擎 image 已在本機）：舊引擎 apply：flock（逾時 6-26）→ 重驗指紋 → argv → 建 .tmp.upgrade 進度檔 → 只改第一行 → 啟動器比對正式 version.toml 第一行前後 → 用新引擎跑 upgrade vendor_kit（「E(c)（1）」頁）", v2=True)
b.box("s2e0", L, 0, ENTRY, "來自「E. 升引擎 (a)(b)」頁：新引擎 image 已在本機（已寫 launcher_start；apply 前已 grep 第一行）", 280)
b.box("s2r0", L, 1, v2(W12), "docker run 舊引擎 apply upgrade", 280)
b.box("s2b", E, 1, v2(SUB), "apply（舊引擎）：flock 專案目錄（60 秒）", 300, ax="l")
b.box("s2bx", G, 1, v2(R12), fl(E26X), 180)
b.box("s2cx", U, 2, v2(O12), "1 + 6-12：指紋不同「請重跑」", 220)
b.box("s2c", E, 2, v2(D12), "重驗指紋：相同？", 260, ax="l")
b.box("s2c2x", U, 3, v2(O12), "1：原 argv 與計畫不一致，請重跑", 220)
b.box("s2c2", E, 3, v2(D12), ARGV_Q, 260, ax="l")
b.box("s2d", E, 4, v2(SUB), fl("是 → 建進度檔 .tmp.upgrade.<id>.toml（記舊引擎 ref、目標引擎 ref、計畫 image ID；改第一行之前）"), 360)
b.box("s2df", P, 4, v2(F12), "＋.vendor_kit/.tmp.upgrade.<id>.toml（進度檔，不進 git；新引擎重產薄殼完成後才刪）", 280)
b.box("s2e", E, 5, v2(SUB), fl("只改 version.toml 的 vendor_kit 版本鎖定行 → 新引擎 ref（其餘工具等重跑原指令；進度檔留給新引擎）"), 360)
b.box("s2f", P, 5, F12, "version.toml 的 vendor_kit 版本鎖定行 = 新引擎 ref", 280)
b.box("s2h", L, 6, v2(W12), fl("apply 後再 grep 正式 version.toml 的 vendor_kit 版本鎖定行（不看本機覆寫、不從 stdout 讀）"), 280)
b.box("s2hx", U, 7, v2(R12), fl("1：apply 未改第一行（印 apply 的錯誤）"), 220)
b.box("s2h2", L, 7, v2(D12), fl("第一行變了？"), 280)
b.box("s2h3x", U, 8, v2(O12), fl("1 + 6-2b：第一行變成非計畫值；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 220)
b.box("s2h3", L, 8, v2(D12), fl("是 → == 計畫的 engine？"), 280)
b.box("s2r", L, 9, v2(W12), fl("是：docker run 新引擎 upgrade vendor_kit（本機覆寫有 vendor_kit= 則用該 image、驗 ID；同一 TRACEPARENT、同一執行紀錄）"), 280)
b.box("s4", E, 9, ENTRY, "續「E(c)（1）」頁「docker run 該引擎」格（同一次指令內；接手 §3.4，結束碼原樣傳出）", 360)
footer(b, F, 10, [("s2dx", v2(R12), fl("1：建進度檔失敗則第一行未改；改第一行失敗則進度檔保留。印實際原因，下次可寫動詞自動恢復"), P, "c")], spacer=1, sp="l")
b.D("se3r", "s2e0", "s2r0"); b.H("se3b0", "s2r0", "s2b"); b.H("se3bx", "s2b", "s2bx", "逾時"); b.D("se3c", "s2b", "s2c", al=True); b.H("se3cx", "s2c", "s2cx", "否"); b.D("se3c2", "s2c", "s2c2", "是", al=True); b.H("se3c2x", "s2c2", "s2c2x", "否")
b.D("se3d", "s2c2", "s2d", "是", al=True); b.H("se3df", "s2d", "s2df", "寫"); b.D("se3e", "s2d", "s2e"); b.H("se4", "s2e", "s2f", "寫")
b.D("se5", "s2e", "s2h", "", 0.2, 0.5); b.D("se5h", "s2h", "s2h2", al=True); b.H("se5x", "s2h2", "s2hx", "否"); b.D("se5h3", "s2h2", "s2h3", "是", al=True); b.H("se5h3x", "s2h3", "s2h3x", "否")
b.D("se5l", "s2h3", "s2r", "是", al=True); b.H("se7", "s2r", "s4")
b.close()
failbus(F, p7bca, ["s2d", "s2e"], "s2dx")
foot(p7bca, "p7bca", F.y, _k7e("升引擎進度檔", "6-2b", "6-26", "原 argv", "6-12") + [("接手（§3.4）", "「引擎已變」不從 stdout 讀：啟動器在 apply 前後各 grep 一次正式 version.toml 的 vendor_kit 版本鎖定行；變了且 == 計畫的 engine → 以新 ref 跑 upgrade vendor_kit（同一 TRACEPARENT），其結束碼原樣傳出（預期 1 + 6-2）；本機覆寫只影響實際用哪個 image")], ALL - {"inv", "tree", "pend", "rule"} | {"entry"})
addpage("v1p7bca", "流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手", p7bca)

# ================= P7bcc：upgrade ── E(c) upgrade vendor_kit（1）=================
p7bcc, F = newpage("流程 v2：upgrade ── E(c) upgrade vendor_kit（1）薄殼檢查 → 恢復 → 目標判定（v2.15-7、v2.16-8）", "", COLS5W)
b = F.band("uE2", "E(c)（1）upgrade vendor_kit[@<tag>]（單段、無指紋重驗）：執行紀錄 → inspect／pull 現引擎 → flock → 薄殼 == 上次產物？（6-28）→ 恢復既有 .tmp.upgrade → 目標判定（@<tag>／CI 模式／查 registry 三條分開）→ 降版檢查 → 目標 ≠ 現 ref？", v2=True)
b.box("s10", U, 0, v2(G12), fl("(c) just vendor_kit upgrade vendor_kit[@<tag>]"), 220)
lstart(b, "s10l", "s10x", 0, "upgrade", w=280)
b.box("s11a", L, 2, v2(W12), "grep version.toml 的 vendor_kit 版本鎖定行取引擎 ref（本機覆寫 vendor_kit= 優先；跳過 gen/.stamp 比對）", 280)
pullseg(b, 3, ("s11n", "s11p", "s11g"), ("docker image inspect：本機有？", "無：docker pull 該引擎", "vendor_kit:vN\n（版本鎖定行指到的引擎）"), ("s11v", v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？")), w=(280, 200, 280))
b.box("s11px", U, 4, v2(R12), fl("1 + 6-24／6-31：現引擎拉不到／逾時"), 220)
b.box("s11x", U, 5, v2(R12), fl("1：本機覆寫的 image ID 不符（同 tag 重 build）"), 220)
b.box("s10a", U, 6, ENTRY, fl("來自「E. 升引擎 (a′)」頁：啟動器已改用新引擎 ref（已寫 launcher_start）"), 220)
b.box("s11r", L, 6, v2(W12), "否：docker run 該引擎 upgrade vendor_kit", 280)
b.box("s12a", E, 6, v2(SUB), "flock 專案目錄（60 秒）", 300, ax="l")
b.box("s12ax", G, 6, v2(R12), fl(E26X), 200)
b.box("s12sx", U, 7, v2(O12), fl("1 + 6-28：薄殼被改過，列差異不動（零寫入）"), 220)
b.box("s12s", E, 7, v2(D12), "薄殼 == 上次產物？", 210, ax="l")
b.box("s12sn", P, 7, v2(NOTE), fl("「上次產物」= 薄殼自描述首行的 sha256 與其餘內容相符（Q17；install 頁同）；任何寫入前檢查、恢復進度檔之前，不符 → 1 列差異、零寫入（v2.16-8）"), 360)
b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
b.box("s12d1", E, 13, v2(D12), fl("目標比現版舊（image LABEL 介面版／檔案版）？"), 210, ax="l")
b.box("s12dx", U, 14, v2(O12), fl("3 + 6-10：目標引擎無法無損讀現有檔（零寫入）"), 220)
b.box("s12d2", E, 14, v2(D12), fl("是 → 目標引擎能無損讀現有檔？"), 210, ax="l")
b.box("s12v", E, 15, v2(D12), "目標引擎 ref ≠ 現 ref？", 210, ax="l")
b.box("s12vz", E, 15, ENTRY, "否：續「E(c)（2）」頁：薄殼比對與重產", 140, ax="r")
b.box("s12jz", E, 16, ENTRY, "是：續「E(c)（1′）」頁：建進度檔 → 啟動器 pull 目標引擎 → 新引擎接手", 360)
b.H("se11", "s10", "s10l0"); b.D("se11l", "s10l", "s11a", al=True); b.D("se11q", "s11a", "s11n", al=True)
b.H("se11px", "s11p", "s11px", "失敗"); b.H("se11vx", "s11v", "s11x", "是"); b.D("se11vr", "s11v", "s11r", "否", al=True)
b.H("se11e", "s10a", "s11r")
b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
b.D("se12tt", "s12t", "s12tt", "是", al=True)
b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
b.close()
bypass(F, p7bcc, "se11y", "s11n", "s11v")
sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
_A = F.abs
def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
    sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
    hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
_rb("se12jrv", "s12jr", "s12d1", ""); _rb("se12ttv", "s12tt", "s12d1", ""); _rb("se12fzv", "s12fz", "s12d1", ""); _rb("se12d1n", "s12d1", "s12v", "否")
foot(p7bcc, "p7bcc", F.y, _k7e("升引擎進度檔", "上次產物", "registry", "--protocol", "6-26") + [PULLX_T, ("6-28", "薄殼被改過（自描述首行 hash 與內容不符）→ 1，列差異不動、零寫入；在恢復進度檔之前檢查")], ALL - {"inv", "tree", "pend", "rule"} | {"entry"})
addpage("v1p7bcc", "流程 v2：upgrade ── E(c) upgrade vendor_kit（1）", p7bcc)

# ================= P7bcx：upgrade ── E(c)（1′）建進度檔 → pull 目標引擎 → 接手 =================
p7bcx, F = newpage("流程 v2：upgrade ── E(c) upgrade vendor_kit（1′）pull 目標引擎 → 接手（v2.15-7）", "", COLS5W)
b = F.band("uE2b", "E(c)（1′）目標 ≠ 現 ref（承「E(c)（1）」頁）：建進度檔（記目標 ref）→ 啟動器 grep 目標 ref → inspect／pull 目標引擎（失敗 → 第一行未改）→ 目標引擎跑 upgrade vendor_kit（「E(c)（2）」頁）", v2=True)
b.box("s12j0", E, 0, ENTRY, "來自「E(c)（1）」頁：目標引擎 ref ≠ 現 ref（已拿鎖；已寫 launcher_start）", 360)
b.box("s12j", E, 1, v2(SUB), fl("建進度檔 .tmp.upgrade.<id>.toml（記舊引擎 ref、目標引擎 ref、計畫 image ID、pending；已有 → 沿用；之後引擎結束交回啟動器）"), 360)
b.box("s12jf", P, 1, v2(F12), "＋.vendor_kit/.tmp.upgrade.<id>.toml（進度檔，不進 git；第一行尚未改；新引擎重產薄殼完成後才刪）", 360)
b.box("s12h", L, 2, v2(W12), fl("啟動器：grep 進度檔的目標引擎 ref（不從 stdout 讀）"), 280)
pullseg(b, 3, ("s12hi", "s12hp", "s12hg"), ("docker image inspect 目標引擎：本機有？", "無：docker pull 目標引擎", "vendor_kit:vY\n（目標引擎）"), ("s12ho", v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？")), w=(280, 200, 280))
b.box("s13gm", E, 7, v2(SUB), fl("寫 metadata baseline/.vendor_kit.toml：config.toml 的 state／conflicts／declined_hash"), 360)
b.box("s13gmf", P, 7, v2(F12), "baseline/.vendor_kit.toml（config.toml 紀錄；進 git）", 360)
b.box("s13gz", E, 8, ENTRY, "續「E(c)（2′）」頁：gen/.stamp → tools.just → 刪進度檔 → 終點", 360)
footer(b, F, 9, [("s13qx", ENTRY, "失敗（本頁任一步；共通匯流）→ 續「E(c)（2′）」頁「引擎結束 = 失敗」入口", P, "c")], spacer=1, sp="l")
b.D("se17", "s13g0", "s13gq", al=True); b.D("se17y", "s13gq", "s13gy", "是", al=True)
b.D("se17gpq", "s13gy", "s13gpq", al=True); b.D("se17gaq", "s13gpq", "s13gaq", "否", al=True); b.D("se17aw", "s13gaq", "s13gw", "是", al=True)
b.H("se17f", "s13gw", "s13gf", "寫"); b.D("se17b", "s13gw", "s13gb"); b.H("se17bf", "s13gb", "s13gbf", "寫")
b.D("se17m", "s13gb", "s13gm"); b.H("se17mf", "s13gm", "s13gmf", "寫"); b.D("se17z", "s13gm", "s13gz")
b.close()
tty(F, p7bcg, "s13gaq")
sidebus(F, p7bcg, "se17gpx", "s13gpq", "s13gm", "是：留原檔、不推基準版（記 conflicts）", busx=400, tx=0.15, pos=-0.6, vert="below")
sidebus(F, p7bcg, "se17adn", "s13gaq", "s13gb", "否：不替換；記 declined", busx=420, tx=0.15, pos=-0.5, vert="left")
failbus(F, p7bcg, ["s13gw", "s13gb", "s13gm"], "s13qx")
b = F.band("uE3c", "E(c)（2″）B：config.toml 缺 → 問「要建 config.toml 嗎」→ 是：新版範本原子替換 → 推基準版副本 → metadata state=managed；否：不建、不寫檔，只記 declined → 續「E(c)（2′）」頁", v2=True)
b.box("s13gp0", E, 0, ENTRY, "來自上段「config.toml 存在？」= 否", 360)
b.box("s13gp", E, 1, v2(SUB), fl("問「要建 config.toml 嗎」（-y 免問）"), 360)
b.box("s13gpa", E, 2, v2(D12), "同意？", 300)
b.box("s13gn", E, 3, v2(SUB), fl("是：建 config.toml（新版範本；原子替換）"), 360)
b.box("s13gnf", P, 3, v2(F12), "＋config.toml（進 git；含註解與預設）", 360)
b.box("s13gnb", E, 4, v2(SUB), fl("baseline/vendor_kit/config.toml 副本 = 新版範本"), 360)
b.box("s13gnbf", P, 4, v2(F12), "＋baseline/vendor_kit/config.toml（副本；進 git）", 360)
b.box("s13gnm", E, 5, v2(SUB), fl("寫 metadata baseline/.vendor_kit.toml：config.toml state=managed（拒絕 → state=declined、不建）"), 360)
b.box("s13gnmf", P, 5, v2(F12), "baseline/.vendor_kit.toml（config.toml 紀錄；進 git）", 360)
b.box("s13gz2", E, 6, ENTRY, "續「E(c)（2′）」頁：gen/.stamp → tools.just → 刪進度檔 → 終點", 360)
footer(b, F, 7, [("s13qx2", ENTRY, "失敗（本段任一步；共通匯流）→ 續「E(c)（2′）」頁「引擎結束 = 失敗」入口", P, "c")], spacer=1, sp="l")
b.D("se17p0", "s13gp0", "s13gp"); b.D("se17pa", "s13gp", "s13gpa", al=True); b.D("se17pn", "s13gpa", "s13gn", "是", al=True)
b.H("se17nf", "s13gn", "s13gnf", "寫"); b.D("se17nb", "s13gn", "s13gnb"); b.H("se17nbf", "s13gnb", "s13gnbf", "寫"); b.D("se17nm", "s13gnb", "s13gnm"); b.H("se17nmf", "s13gnm", "s13gnmf", "寫"); b.D("se17z2", "s13gnm", "s13gz2")
b.close()
tty(F, p7bcg, "s13gpa")
sidebus(F, p7bcg, "se17pnn", "s13gpa", "s13gnm", "否：不建（記 declined）", busx=400, tx=0.15, pos=-0.6, vert="below")
failbus(F, p7bcg, ["s13gn", "s13gnb", "s13gnm"], "s13qx2")
_A = F.abs; _sx, _sy, _sw, _sh = _A["s13gq"]; _tx0, _ty0, _tw, _th = _A["s13gp0"]
p7bcg.append(_edge("se17n", "s13gq", "s13gp0", "否", (0, 0.5), (0, 0.5), [(10, _sy + _sh / 2), (10, _ty0 + _th / 2)], -0.95, "below"))
pend(p7bcg, "待處理問題\n• s13gcq／se17same：結果相同分支待重新配置")
foot(p7bcg, "p7bcg", F.y, _k7e("升引擎進度檔") + [LOGT[0], E22_T, E4_T, GM_T, ("解析失敗（config.toml）", "合併結果解析失敗（TOML 不合法）→ 留原檔、不推基準版副本、metadata 記 conflicts → 結束碼 2；有衝突標記 → 仍替換並推基準版（重入時靠標記偵測）→ 2")], ALL - {"inv", "tree", "rule", "note"} | {"entry", "tty"})
addpage("v1p7bcce", "流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml", p7bcg)

# ================= P7bccd：upgrade ── E(c)（2′）gen/.stamp → tools.just → 刪進度檔 → 判定 =================
p7bce, F = newpage("流程 v2：upgrade ── E(c) upgrade vendor_kit（2′）收尾 → 啟動器驗第一行 → 終點（§3.4、v2.15-7）", "", COLS5W)
b = F.band("uE4", "E(c)（2′）（承「E(c)（2″）」頁）：gen/.stamp → tools.just → 刪進度檔（刪前已讀舊引擎 ref）→ config.toml 衝突 → 2；換引擎 → 1 + 6-2；同引擎修復 → 1 + 6-2（文案分開）；失敗 → 啟動器：第一行未變 → 1 印原因；已改 → 1 + 6-2b", v2=True)
b.box("s13z0", E, 0, ENTRY, "來自「E(c)（2″）」頁：薄殼五檔已重產、config.toml 已處理（已寫 launcher_start）", 360)
b.box("s13b", E, 1, v2(SUB), "寫 gen/.stamp（只記本引擎 ref）", 360)
b.box("s13bf", P, 1, F12, "gen/.stamp（不進 git）", 360)
b.box("s13c", E, 2, v2(SUB), "重生 gen/tools.just（用本引擎的規則；mod? 行）", 360)
b.box("s13cf", P, 2, F12, "gen/tools.just（不進 git；mod? 行）", 360)
b.box("s13d", E, 3, v2(SUB), fl("成功：刪進度檔 .tmp.upgrade.<id>.toml（最後一步，由新引擎刪；刪前已讀舊引擎 ref）"), 360)
b.box("s13df", P, 3, v2(F12), "－.vendor_kit/.tmp.upgrade.<id>.toml（E(a′)／E(c)(1′) 或 E(c)(2) 建的進度檔）", 360)
b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
b.close()
lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
foot(p7bce, "p7bce", F.y, _k7e("升引擎進度檔", "6-2b", "gen/.stamp", "gen/tools") + [("接手判定（§3.4）", "啟動器在 apply 前後各 grep 一次正式 version.toml 的 vendor_kit 版本鎖定行；引擎失敗時：未變 → 1 印原因；已改（含變成非計畫值）→ 1 + 6-2b（進度檔保留，重跑 upgrade vendor_kit 續跑）"), ("6-2（升引擎完成）", "「已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」（結束 1，需人處理）；同引擎修復重產另有文案（版本未變）")], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
addpage("v1p7bccd", "流程 v2：upgrade ── E(c) upgrade vendor_kit（2′）", p7bce)

# ================= P8：dev =================
T8 = [
 ("覆寫兩種（v2.1 B）", "工具 path 覆寫 [tools].<repo> = \"path:<dir>\"：cache/<repo>/ 變 symlink，sync 跳過該工具取件／verify 但仍檢查 metadata、基準版；引擎 tag 覆寫 vendor_kit = \"<tag>\"＋vendor_kit_image_id：啟動器改用該本機 image"),
 RA_T, NZ_T,
 ("dev 進度檔", ".tmp.dev.<id>.toml：dev 是可寫動詞，第一個寫入前建，記要寫的覆寫行、symlink 目標、印記第一行；成功後刪；失敗 → 保留、下次可寫動詞先恢復（v2.15-5、新規則 (b)）"),
 ("RepoDigests", "從倉庫拉來才有的 digest，docker load 的 tar 沒有 → dev vendor_kit 只能用 tag（另記 image ID：同 tag 重 build 才會被發現）"),
 ("GHCR／tar／docker load", "GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i <tag> 指定它"),
 ("docker image inspect／掛載 -v", "啟動器每次 docker run 前先 docker image inspect <ref 或 tag>：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；-v <dir>/dist:/dist/<repo>:ro = 把本機目錄唯讀掛進容器；引擎 image LABEL 帶介面版／檔案版"),
 ("統一提示 6-1／gen/.stamp（Q10 (2)）", "gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印 6-1「請 just vendor_kit upgrade vendor_kit」（需人處理，橙）"),
 ("下次 just", "下次執行 vendor_kit 動詞，或帶 _sync 前置的工具 recipe（不是每個任意 just recipe 都會進啟動器）"),
 FIP_T,
b.close()
sidebus(F, p8cc, "we2g", "w2e", "w2g", "是：留著", busx=525, tx=0.15, pos=-0.45, vert="left")
failbus(F, p8cc, ["w2l", "w2", "w2ed", "w2g"], "w2x")
footer_edges(F, [("we2z", "w2g", "", "d", "w2z")])
_A = F.abs; _sx, _sy, _sw, _sh = _A["w2z"]; _tx0, _ty0, _tw, _th = _A["w9"]
p8cc.append(_edge("we9", "w2z", "w9", "", (0, 0.5), (1, 0.5), [], None))
foot(p8cc, "p8cc", F.y, _k8("覆寫兩種", "統一提示", "6-27", "6-26", "6-30", "原 argv", "6-12") + [("undev 進度檔（vendor_kit）", ".tmp.undev.<id>.toml：第一個寫入前建，記要撤的 vendor_kit 行與 vendor_kit_image_id（image ID）；成功後刪；失敗保留、下次可寫動詞先恢復")], ALL - {"inv", "pend", "tree", "rule"} | {"entry"})
addpage("v1p8cc", "流程 v2：undev vendor_kit", p8cc)

# ================= P8b：remove（1）=================
RADN_T = ("resolve／apply／--dry-run（remove／uninstall）", "resolve 只讀只算（讀 metadata、算刪除／詢問清單、輸出指紋與 apply|yes，不寫檔；無 image 要拉）；apply 拿 flock 後重驗指紋才寫；--dry-run = apply 的唯讀預覽（只印會刪什麼、會問什麼；不拉 image、不建進度檔；本機 → 0；CI 模式且需改任何進 git 的檔 → 1）")
T8B = [
 RADN_T, FIP_T, NZ_T, ARGV_T, E12_T,
 ("append 行／CRLF／逐行比對", "add 時（strategy=append）問後加進專案檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問 6-21 後逐行比對（CRLF = Windows 換行 \\r\\n，與 LF 視為相同；其餘精確）：仍與紀錄原文相同的行 → 刪；缺失／被改的行 → 跳過並 warn（不是全有／全無；§4.3、v2.9 §5）；下游使用者拒絕 → 不刪，另記孤兒 append 行（v2.16-9）"),
 ("保護清單／保護模式", "uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過；version.local.toml 直接刪（不看 hash）"),
 ("gen／mod?／import", "gen/tools.just 每個 <ns>.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行，與刪 cache 同一次原子替換（I17）；gen/.stamp 只記引擎 ref，uninstall 一併刪；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問 6-20 後才刪；根 .dockerignore 我們加的行也問後只刪原文相同的"),
 ("刪除順序（v2.15-8）", "remove／uninstall：先 append 行（問後）→ 基準版／metadata → cache 與 gen/tools.just（同一次原子替換）→ 印記 → 版本鎖定行最後刪 → 刪進度檔；回 1 時鎖定行不動（工具仍鎖定），進度檔保留、下次可寫動詞先恢復"),
 ("孤兒 append 行（v2.16-9）", "拒絕刪 append 行 → 仍完成移除（版本鎖定行、cache、印記、基準版都刪），只在 baseline/.vendor_kit.toml 另留一筆「孤兒 append 行」紀錄（dest、行原文；同 .dockerignore append 記錄那張表）；不留 baseline/<repo>/ 孤兒目錄"),
 ("6-27（恢復失敗）", "可寫動詞開始前偵測到既有進度檔 → 先恢復再繼續；恢復失敗 → 1「未恢復：<檔名>」逐檔列出"),
 ("6-26（flock 逾時）", "apply 拿專案目錄鎖 60 秒未釋放 → 1「專案目錄被鎖定（PID <pid>，自 <time>）…重試，或設 VENDOR_KIT_NO_LOCK=1」"),
 ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）"),
 ("6-20／6-21／6-34（問後才刪）", "6-21「要刪我們加在 X 的這幾行嗎」（append 行）；6-20「要刪這一行嗎」（根 justfile import 行）；6-34「要刪這幾行嗎」（根 .dockerignore 記錄的行）；-y 免問；拒絕 → 不動"),
 *LOGT,
]
def _t8b(*keep): return [t for t in T8B if t[0].startswith(keep)]
N8B = ""
p8b, F = newpage("流程 v2：remove（1）執行紀錄 → 偵測進度檔 → resolve → 三叉 → apply 前置（§2、§5、v2.16）", "", COLS5)
b = F.band("vC", "remove <repo> [-y] [--dry-run]（1）：拆掉一個工具（初始檔永不刪）= 執行紀錄 → 偵測進度檔 → resolve（讀 metadata → 算清單 → 指紋 → stdout）→ 三叉 → apply 前置（flock 逾時 6-26）；無 image 要拉；寫入段見「remove（2）」頁", v2=True)
b.box("m0", U, 0, G12, "just vendor_kit remove <repo> [-y] [--dry-run]", 220)
lstart(b, "m0l", "m0x", 0, "remove")
preseg(b, "m", 2, "m1", "remove")
b.box("m1", L, 3, v2(W12), fl("docker run <引擎> resolve remove <repo>（不經 extract）"), 280)
b.box("m1e", E, 3, v2(SUB), "resolve（不寫任何檔）：讀 version.toml、version.local.toml", 400)
b.box("m3", U, 4, G12, "0：未接入（提示）", 220)
b.box("m2", E, 4, D12, "已接入 <repo>？", 280, ax="l")
b.box("m5", U, 5, O12, "1：請先 undev <repo>（本機覆寫中）", 220)
b.box("m4", E, 5, D12, "是 → 有 dev path 覆寫？", 280, ax="l")
b.box("m6", E, 6, v2(SUB), fl("否：讀 metadata（append 過的行、完成標記）"), 400)
b.box("m6b", E, 7, v2(SUB), fl("引擎內算刪除清單：版本鎖定行、cache/<repo>/、gen/<repo>.stamp、baseline/<repo>/、gen/tools.just 的 mod? 行（不經 stdout；apply 重算）"), 400)
b.box("m6c", E, 8, v2(SUB), fl("引擎內算詢問清單：metadata 記的 append 行（有才問；由 apply 執行詢問，不交給啟動器）"), 400)
b.box("m6d", E, 9, v2(SUB), fl("產生輸入指紋（同 add（1）頁「輸入指紋」）"), 400)
b.box("m6d2", E, 10, v2(SUB), fl("stdout vk-resolve/1：指紋、apply|yes（無 pull／extract；只傳協定內容）"), 400)
res3(b, "m8", 11, "m8")
b.box("m8", L, 13, v2(W12), fl("是：docker run … -v（含 vk-resolve）<引擎> apply remove <repo>（--dry-run 原樣轉發）"), 280)
b.box("m9a", E, 13, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("m9ax", G, 13, v2(R12), fl(E26X), 200)
b.box("m9x", U, 14, v2(O12), "1 + 6-12：指紋不同「請重跑」", 220)
b.box("m9b", E, 14, v2(D12), "重驗指紋：相同？", 340, ax="l")
b.box("m9cx", U, 15, v2(O12), "1：原 argv 與計畫不一致，請重跑", 220)
b.box("m9c", E, 15, v2(D12), ARGV_Q, 340, ax="l")
b.box("m7cx", U, 16, v2(O12), fl("1：印需改清單（CI 模式；請在本機執行後 commit 並 push）"), 220)
b.box("m7c", E, 16, v2(D12), "是 → CI 模式且需改任何進 git 的檔？", 340, ax="l")
b.box("m7y", U, 17, v2(G12), "0：只印清單（會刪什麼、會問什麼；不拉 image）", 220)
b.box("m7", E, 17, D12, "否 → --dry-run？", 240, ax="l")
b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
b.close()
foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)

# ================= P8bccc：remove（2）寫入段 =================
p8b2, F = newpage("流程 v2：remove（2）apply 寫入段（§2、§5；v2.5 §3／§11、v2.9 §5、v2.16-9／-10）", "", COLS5)
b = F.band("vC2", "remove <repo>（2）寫入段（承「remove（1）」頁）：建進度檔 → 問 append 行（逐行比對；拒絕 → 記孤兒 append 行、仍完成移除）→ 刪基準版與 metadata → 刪 cache 與重生 tools.just 同次原子替換 → 印記 → 最後刪版本鎖定行 → 刪進度檔；任一寫入失敗 → 共通匯流", v2=True)
b.box("m9e", E, 0, ENTRY, "來自「remove（1）」頁：apply 檢查通過（非 dry-run；已寫 launcher_start）", 300)
b.box("m9l", E, 1, v2(SUB), "建進度檔（.vendor_kit/.tmp.remove.<id>.toml；第一個寫入前）", 400)
b.box("m9lf", P, 1, F12, "＋.vendor_kit/.tmp.remove.<id>.toml（進度檔，不進 git）", 360)
b.box("m9h", E, 2, v2(D12), "metadata 有 append 過的行？", 300, ax=30)
b.box("m9q", E, 3, v2(D12), fl("有 → 問 6-21「要刪我們加在 X 的這幾行嗎」同意？（-y 免問）"), 300, ax=30)
471:E26X = "1 + 6-26：專案目錄被鎖定（PID <pid>，自 <time>）；60 秒內未釋放"   # flock 逾時出口（每個 apply 頁都有）
786: ("6-26（flock 逾時）", "apply 拿專案目錄鎖 60 秒未釋放 → 1「專案目錄被鎖定（PID <pid>，自 <time>）…重試，或設 VENDOR_KIT_NO_LOCK=1」"),
792:b = F.band("bI", "5a′ install（bootstrap.sh 代打或自己打）：主機側檢查 git repo／巢狀 → 執行紀錄 → 偵測既有進度檔 → 引擎 ref → inspect／無才 pull → docker run → flock（逾時 6-26）；薄殼比對與暫存見「install（1′）」頁", v2=True)
979: ("6-26（flock 逾時）", "apply 拿專案目錄鎖 60 秒未釋放 → 1「專案目錄被鎖定（PID <pid>，自 <time>）…重試，或設 VENDOR_KIT_NO_LOCK=1」"),
1040:b = F.band("bB1", "5b′ add <repo> docker 段與 apply 前置（承「add（1）」頁）：resolve 回 0？→ 文法合法？→ inspect → 無才 pull → extract → apply → 拿鎖（逾時 6-26）→ 重驗指紋 → argv 一致 → dest？→ 撞名？→ CI 模式 → dry-run；寫入段見「add（2）」頁", v2=True)
1152: ("6-26（flock 逾時）", "apply 拿專案目錄鎖 60 秒未釋放 → 1「專案目錄被鎖定（PID <pid>，自 <time>）…重試，或設 VENDOR_KIT_NO_LOCK=1」"),
1261:b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
1342: ("6-26（flock 逾時）", "apply 拿專案目錄鎖 60 秒未釋放 → 1「專案目錄被鎖定（PID <pid>，自 <time>）…重試，或設 VENDOR_KIT_NO_LOCK=1」"),
1434:b = F.band("uB1", "B（1′）docker 段與 apply 前置（承「B（1）」頁）：resolve 回 0？→ 文法？→ inspect → 無才 pull → extract → apply → 拿鎖（逾時 6-26）→ 重驗 → argv 一致 → dest／命名空間 → 逐檔狀態機只算會問的項目 → CI 模式 → dry-run；寫入段見「B（2）」頁", v2=True)
1704:T7E += [("6-27（恢復失敗）", "可寫動詞開始前偵測到既有進度檔 → 先恢復再繼續；恢復失敗 → 1「未恢復：<檔名>」逐檔列出"), ("6-26（flock 逾時）", "apply 拿專案目錄鎖 60 秒未釋放 → 1「專案目錄被鎖定（PID <pid>，自 <time>）…重試，或設 VENDOR_KIT_NO_LOCK=1」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")]
1738:b = F.band("uEa", "E(a′)（承「E. 升引擎 (a)(b)」頁：新引擎 image 已在本機）：舊引擎 apply：flock（逾時 6-26）→ 重驗指紋 → argv → 建 .tmp.upgrade 進度檔 → 只改第一行 → 啟動器比對正式 version.toml 第一行前後 → 用新引擎跑 upgrade vendor_kit（「E(c)（1）」頁）", v2=True)
1967:T8 += [("6-27（恢復失敗）", "可寫動詞開始前偵測到既有進度檔 → 先恢復再繼續；恢復失敗 → 1「未恢復：<檔名>」逐檔列出"), ("6-26（flock 逾時）", "apply 拿專案目錄鎖 60 秒未釋放 → 1「專案目錄被鎖定（PID <pid>，自 <time>）…重試，或設 VENDOR_KIT_NO_LOCK=1」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")]
2046:b = F.band("vB", "undev <repo>（1）：回到 version.toml 鎖定版 = 執行紀錄 → 偵測既有進度檔 → resolve（不寫）→ 啟動器三叉 → inspect → 無才 pull → extract → apply：flock（逾時 6-26）→ 重驗指紋 → argv；寫入段見「undev（2）」頁", v2=True)
2115:b = F.band("vB′", "undev vendor_kit = 執行紀錄 → 偵測進度檔 → resolve → 三叉 → apply（無 image 要拉；flock 逾時 6-26）：建進度檔（記 image ID）後才撤 vendor_kit 行；最後一個覆寫撤掉 → 刪整個 version.local.toml；任一寫入失敗 → 匯流；下次 just 見「sync（1）」頁", v2=True)
2169: ("6-26（flock 逾時）", "apply 拿專案目錄鎖 60 秒未釋放 → 1「專案目錄被鎖定（PID <pid>，自 <time>）…重試，或設 VENDOR_KIT_NO_LOCK=1」"),
2177:b = F.band("vC", "remove <repo> [-y] [--dry-run]（1）：拆掉一個工具（初始檔永不刪）= 執行紀錄 → 偵測進度檔 → resolve（讀 metadata → 算清單 → 指紋 → stdout）→ 三叉 → apply 前置（flock 逾時 6-26）；無 image 要拉；寫入段見「remove（2）」頁", v2=True)
2272:b = F.band("vD", "uninstall（1）：全部拆掉 = 執行紀錄 → 偵測進度檔 → resolve（完整預檢 → hash → 保護清單 → 算計畫／詢問清單 → 指紋 → stdout）→ 三叉 → apply 前置（flock 逾時 6-26、重驗、argv、CI、dry-run）；寫入段見「uninstall（2）」頁", v2=True)

exec
/usr/bin/bash -lc "rg -n '"'^def res3|def hseg_edge|me.*ax|se.*ax'"' disc_v1_b.py | head -60; sed -n '620,700p' disc_v1_b.py; sed -n '815,855p' disc_v1_b.py; sed -n '1050,1085p' disc_v1_b.py" in <scratchpad>
 succeeded in 0ms:
126:    def box(self, cid, col, row, style, text, w, h=None, ax="c", minh=40, extra=0):
130:        h = hh if h is None else max(h, hh)
131:        self.boxes.append(dict(id=cid, col=col, row=row, st=style, text=text, w=w, h=h, ax=ax)); return cid
132:    def files(self, cid, col, row, title, items, w, ax="c", cols=1, cw=None):
139:        self.boxes.append(dict(id=cid, col=col, row=row, st=FGRP, text=title, w=w, h=h, ax=ax, items=list(zip(items, hs)), cols=cols, cw=cw, rows=rows)); return cid
143:        h = hh if h is None else max(h, hh)
190:        bh = 30 + self.pad + sum(rh) + max(nrows - 1, 0) * g + self.pad
191:        if self.extra: bh = max(bh, max(yy + h for _, _, _, _, yy, _, h in self.extra) + self.pad)
200:            else: x = cx + b["ax"]
598:def res3(b, pid, row, nxt, w=280, col=L, xcol=U, xw=220):
636:def hseg_edge(cells, eid, s, t, label, exit_, entry, pts, A):
840:b.box("i4_5b", E, 11, v2(SUB), fl("產 baseline/vendor_kit/config.toml 副本到暫存（其基準版）"), 300, ax="l")
865:b.box("i4bb", E, 4, v2(SUB), fl("baseline/vendor_kit/config.toml 副本原子替換"), 300, ax="l")
867:b.box("i4bm", E, 5, v2(SUB), fl("寫 metadata baseline/.vendor_kit.toml：config.toml state=managed"), 300, ax="l")
874:b.box("i4gq", E, 9, v2(D12), "baseline/.gitkeep 缺？", 260, ax="l")
875:b.box("i4g", E, 10, v2(SUB), fl("是：建 baseline/.gitkeep（VK 自產進 git 的空檔）"), 300, ax="l")
922:b.box("igm", E, 12, v2(SUB), fl("只記實際新增的行到 baseline/.vendor_kit.toml（lines）"), 250, ax=SP)
999:b.box("c5", E, 9, D12, "metadata 有完成標記？", 310, ax="l")
1098:b.box("c20", E, 10, SUB, fl("是：append 那幾行到暫存副本（state=appended；實際插入的行之後記進 metadata）"), 200, ax=180)
1202:b.box("n1be", E, 1, v2(SUB), "resolve sync（不寫任何檔）：讀 version.toml、各 metadata、印記", 360, ax="l")
1207:b.box("t0s", E, 3, v2(SUB), fl("是：跳過取件／verify（仍查 metadata、基準版）↓"), 180, ax=LR)
1216:b.box("t3m", E, 7, v2(D12), "metadata 存在且可解析？", 360, ax="l")
1218:b.box("t3", E, 8, D12, "是 → metadata 有完成標記？", 360, ax="l")
1228:b.box("z1", E, 15, v2(SUB), fl("產生輸入指紋（version.toml、metadata、印記 hash…）"), 360, ax="l")
1280:b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "否"); b.D("me2c", "m2b", "m2c", "是", al=True); b.H("me2cx", "m2c", "m2cx", "否")
1402:b.box("b4", E, 6, D12, "否 → 有 baseline/<repo>/？", 340, ax=10)
1479:b.box("b10fq", E, 2, v2(D12), fl("(0) metadata 有衝突狀態（resolve 已判定已解）？"), 300, ax="l")
1499:b.box("b14a3", E, 13, v2(SUB), fl("是：git merge-file --diff3（暫存）"), 140, ax="r")
1505:b.box("b14pc2", E, 18, v2(SUB), fl("記 conflicts（metadata；該檔基準版不推）"), 140, ax="l")
1589:b.box("q1", E, 1, v2(D12), "metadata 無此 dest（新版新增）且 dest 已存在？", 460, ax=LM)
1597:b.box("q3b", E, 5, v2(D12), "否 → metadata 記有 declined_hash 且 == N 的 hash？（已納管檔拒絕過或 state=declined）", 460, ax=LM)
1800:b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
1837:b.H("se12hpx", "s12hp", "s12hpx", "失敗"); b.H("se12hox", "s12ho", "s12hox", "是"); b.D("se12hr", "s12ho", "s12hr", "否", al=True); b.H("se12ha", "s12hr", "s12ha"); b.H("se12hax", "s12ha", "s12hax", "逾時"); b.D("se12hs", "s12ha", "s12hs", al=True); b.H("se12hsx", "s12hs", "s12hsx", "否"); b.D("se12hz", "s12hs", "s12hz", "是", al=True)
2207:b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
2219:b.box("m9h", E, 2, v2(D12), "metadata 有 append 過的行？", 300, ax=30)
2228:b.box("m10a", E, 8, v2(SUB), "否：刪 baseline/<repo>/ 內範本副本", 400, ax=-60)
2279:b.box("x2", E, 4, v2(D12), fl("完整預檢全部工具通過？（每個工具：本機覆寫中？未完成接入？metadata 可解析？任一不過整體不動）"), 400, ax="l")
        lw = sum(12 if ord(c) > 255 else 7 for c in (lab or ""))
        pos = 2 * ((stub + (gy - ey) + 6 + lw / 2) / tot) - 1 if lab else None       # 標籤放縫隙水平段起點上方
        st_ = _edge(f"fb_{s}", s, end, lab, (1, round(syy, 3)), (round(tx, 3), 0), pts, pos, "below" if lab else None)
        cells.append(st_.replace("verticalAlign=top;spacingTop=6;", "verticalAlign=bottom;spacingBottom=4;"))

def lbus(F, cells, srcs, end, busx, label="失敗", sy=0.85, stub=16, tx=0.5):
    """failbus 的左側版：寫入格左側短線 → 該列下方縫隙 → x=busx（在該欄左側）→ 終點上方縫隙 → 終點頂端（終點在左側欄）。"""
    A, RB, RT, g = F.abs, F.rb, F.rt, F.gap
    tx0, ty0, tw, th = A[end]; nx = tx0 + tx * tw; lev = RT[end] - g / 2
    for s in srcs:
        sx0, sy0, sw, sh = A[s]; ex, ey = sx0, sy0 + sy * sh; hx = ex - stub; gy = RB[s] + g / 2
        if abs(hx - busx) < 40: pts = [(busx, ey), (busx, lev), (nx, lev)]                 # 匯流排就在旁邊：短線直接接上，不折
        else: pts = [(hx, ey), (hx, gy), (busx, gy), (busx, lev), (nx, lev)]
        tot = abs(ex - busx) + (lev - ey) + abs(nx - busx) + (ty0 - lev)
        cells.append(_edge(f"lb_{s}", s, end, label, (0, round(sy, 3)), (round(tx, 3), 0), pts, 2 * ((abs(ex - busx) + 8) / tot) - 1 if label else None, "left" if label else None))

def hseg_edge(cells, eid, s, t, label, exit_, entry, pts, A):
    """自訂路徑，標籤放第一段水平段中央下方（避免壓在轉角或垂直匯流線上）。"""
    sx0, sy0, sw, sh = A[s]; tx0, ty0, tw, th = A[t]
    p0 = (sx0 + exit_[0] * sw, sy0 + exit_[1] * sh); pn = (tx0 + entry[0] * tw, ty0 + entry[1] * th)
    allp = [p0] + list(pts) + [pn]; segs = [abs(b_[0] - a_[0]) + abs(b_[1] - a_[1]) for a_, b_ in zip(allp, allp[1:])]; tot = sum(segs) or 1
    i = next((k for k, (a_, b_) in enumerate(zip(allp, allp[1:])) if abs(a_[1] - b_[1]) < 1 and segs[k] >= 24), 0)
    pos = 2 * ((sum(segs[:i]) + segs[i] / 2) / tot) - 1
    cells.append(_edge(eid, s, t, label, exit_, entry, pts, pos if label else None, "below" if label else None))

# ================= P5：bootstrap.sh（1）=================
T5 = [
 BOOT_T,
 ("release／tar／.digest／docker load", "release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker"),
 ("--local <image tag 或 tar>（B1，依序互斥）", "以 .tar 結尾 → 檔案路徑（必須存在，否則 1）；否則值含 / 且存在同名檔 → 1 + 6-37 消歧；否則 → image tag（含 / 但無同名檔的完整 ref 也是 tag 形）。tar 形：docker load 後由同名 .digest 旁檔取 index digest；tag 形：不讀 .digest、只 docker image inspect 本機 image ID；version.toml 仍寫正式 ref@digest（tag 形 = 專案已有那行或內嵌引擎 ref）；version.local.toml 在 install 成功後才寫"),
 ("6-37", "「--local 的值 <v> 既是存在的檔案也可解讀為 image tag。要指定檔案請用以 .tar 結尾的路徑；要指定 image 請先移走或改名同名檔 <v>。」（結束 1、零寫入；需人處理）"),
 ("GHCR／引擎 ref", "GHCR = GitHub 的容器倉庫；引擎 ref = version.toml 的 vendor_kit 版本鎖定行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）；已有 version.toml → 用該行、拉不到即失敗、不退回內嵌"),
 ("docker image inspect／pull（啟動器）", "每次 docker run 前先 docker image inspect <ref>：本機有 → 不 pull（離線可用）；無 → docker pull；tag 形 --local 本機無此 image = 失敗、不得 pull；LABEL 帶介面版／最低介面版"),
 ("6-18（最低介面版）", "引擎 image LABEL 的最低介面版高於 bootstrap.sh 的介面版 → 3 + 6-18「目前薄殼或引擎低於最低介面版 <floor>。請以 bootstrap.sh 重建。」（零寫入；本機有 image → inspect LABEL 即檢查，沒有 → pull 後立即檢查，仍在任何寫入之前）"),
 MSG_T,
]
def _t5(*drop): return [t for t in T5 if not t[0].startswith(drop)]
N5 = ""   # 沿革便條已刪（v2.16-18）
p5, F = newpage("流程 v2：bootstrap.sh（1）檢查 → 執行紀錄 → 引擎 ref → --local 判別（§1.1 B1、§2）", "", COLS5B)
b = F.band("bA", "5a bootstrap.sh 前半：檢查 git／just → 執行紀錄 → 引擎 ref（Q18）→ --local 依序判別：.tar 結尾？／含 / 且存在同名檔？（6-37）→ tar 形 docker load、讀 .digest；image 段見「bootstrap.sh（1″）」頁", v2=True)
b.box("a0", U, 0, G12, "執行 bootstrap.sh -t <repo>[@<tag>]…", 220)
b.box("a2", U, 1, O12, fl("1 + 6-16：請先 git init（執行紀錄未建）"), 220)
b.box("a1", L, 1, D12, "是 git repo？（主機側）", 240)
b.box("a4", U, 2, O12, fl("1 + 6-23：印 just 安裝指令（執行紀錄未建）"), 220)
b.box("a3", L, 2, D12, "just ≥ 1.33.0？", 300)
lstart(b, "a0l", "a0lx", 3, "bootstrap", w=300, xcol=U, xw=220, pre="是：")
b.box("a1v", L, 5, v2(D12), "專案已有 version.toml？", 240)
b.box("a1r", P, 5, v2(RULE), fl("Q18（v2.4 §5）：已裝過的 repo 再跑舊 bootstrap.sh → 用 version.toml 的 vendor_kit 版本鎖定行的引擎跑 install（不降版）；拉不到 → 1，不得退回內嵌；只有第一次接入才用內嵌 ref"), 360)
b.box("a1vy", L, 6, v2(W12), fl("是：引擎 ref = version.toml 的版本鎖定行（拉不到 → 1，不退回內嵌）"), 200, ax="l")
b.box("a1vn", L, 6, v2(W12), fl("否：引擎 ref = 內嵌引擎 ref（第一次接入）"), 200, ax="r")
b.box("a5", L, 7, D12, "--local？", 160)
b.box("a8z2", E, 8, ENTRY, "否：續「bootstrap.sh（1″）」頁 B：非 --local（引擎 ref 已定）", 240)
b.box("a8q", L, 8, v2(D12), fl("是：值以 .tar 結尾？"), 210, ax=40)
b.box("a8t", L, 8, v2(D12), fl("否 → 值含 / 且存在同名檔？"), 180, ax="r")
b.box("a8ex", U, 9, v2(O12), "1：--local 檔案不存在（請檢查路徑）", 220)
b.box("a8e", L, 9, v2(D12), "是：該檔案存在？", 210, ax=40)
b.box("a8tx", E, 9, v2(O12), fl("1 + 6-37：--local 的值 <v> 既是存在的檔案也可解讀為 image tag。要指定檔案請用以 .tar 結尾的路徑；要指定 image 請先移走或改名同名檔 <v>。"), 260)
b.box("a8lx", U, 10, v2(R12), fl("1：docker load 失敗（印原文）"), 220)
b.box("a8l", L, 10, v2(W12), "是：docker load <tar>", 210, ax=40)
b.box("a8dx", U, 11, v2(R12), fl("1：.digest 旁檔缺（tar 形需要）"), 220)
b.box("a8dq", L, 11, v2(D12), fl("有同名 .digest 旁檔？"), 210, ax=40)
b.box("a8d", L, 12, v2(W12), fl("是：讀旁檔 = 正式 index digest（tar 形才讀）"), 210, ax=40)
b.box("a8z", L, 13, ENTRY, "續「bootstrap.sh（1″）」頁 A：--local，image 在本機（tar 形已 load；tag 形 = 值即本機 tag，不讀 .digest）", 440, ax="l")
b.D("ae1", "a0", "a1", "", 0.5, 0.5); b.H("ae2", "a1", "a2", "否"); b.D("ae3", "a1", "a3", "是", al=True)
b.H("ae4", "a3", "a4", "否"); b.D("ae5", "a3", "a0l0", "是", al=True); b.D("ae5l", "a0l", "a1v", al=True)
b.D("ae5y", "a1v", "a1vy", "是"); b.D("ae5n", "a1v", "a1vn", "否")
b.D("ae5a", "a1vy", "a5"); b.D("ae5b", "a1vn", "a5")
b.D("ae6", "a5", "a8q", "是", 0.5, 0.5); b.RD("ae7", "a5", "a8z2", "否")
b.H("ae8t", "a8q", "a8t", "否"); b.D("ae8", "a8q", "a8e", "是", al=True)
b.H("ae8tx", "a8t", "a8tx", ""); b.D("ae8tn", "a8t", "a8z", "", 0.5, 0.9)
b.H("ae8e", "a8e", "a8ex", "否"); b.D("ae8ey", "a8e", "a8l", "是", al=True); b.H("ae8lx", "a8l", "a8lx", "失敗")
b.D("ae9", "a8l", "a8dq", al=True); b.H("ae9x", "a8dq", "a8dx", "否"); b.D("ae9d", "a8dq", "a8d", "是", al=True); b.D("ae9z", "a8d", "a8z", "", 0.5, 0.3)
b.close()
foot(p5, "p5", F.y, _t5("docker image inspect", "6-18"), ALL - {"inv", "tree", "pend"} | {"entry"})
addpage("v1p5", "流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別", p5)

# ================= P5x：bootstrap.sh（1″）inspect → pull → LABEL =================
p5x, F = newpage("流程 v2：bootstrap.sh（1″）引擎 image：inspect → 無才 pull → LABEL 最低介面版（§2）", "", COLS5B)
b = F.band("bAx", "5a′ bootstrap.sh 引擎 image 段（承「bootstrap.sh（1）」頁）：A --local → inspect 取 image ID（不 pull）；B → inspect → 無才 pull → LABEL 最低介面版檢查（任何寫入之前；否 → 3 零寫入）→ 續「bootstrap.sh（1′）」頁", v2=True)
b.box("a8a", L, 0, ENTRY, "來自「bootstrap.sh（1）」頁 A：--local（image 在本機）", 220, ax="l")
b.box("a8b", L, 0, ENTRY, "來自「bootstrap.sh（1）」頁 B：非 --local（引擎 ref = 版本鎖定行或內嵌）", 220, ax="r")
b.H("ie1e", "i1", "i4a"); b.H("ie4ax", "i4a", "i4ax", ""); b.D("ie4a", "i4a", "ipq", al=True)
b.H("ipe_y", "ipq", "ipr", "是"); b.H("ipe_x", "ipr", "ipx", "失敗"); b.D("ipe_r", "ipr", "i4z0", "", 0.5, 0.75); b.D("ipe_n", "ipq", "i4z0", "否", al=True)
b.close()
bypass(F, p5c, "ie1y", "i1i", "i1")
foot(p5c, "p5c", F.y, [t for t in T5I if not t[0].startswith(("install 進度檔", "上次產物", "暫存目錄"))], ALL - {"inv", "tree", "pend"} | {"entry"})
addpage("v1p5c", "流程 v2：install（1）主機檢查 → 引擎 image → docker run", p5c)

# ================= P5cm：install（1′）比對薄殼 → 進度檔 → 產薄殼到暫存 =================
p5cm, F = newpage("流程 v2：install（1′）比對薄殼 → 進度檔 → 產薄殼五檔到暫存（§2、Q17、v2.15-11）", "", COLS5)
b = F.band("bIm", "5a″ install 引擎前半（承「install（1）」頁：已拿鎖）：薄殼已存在？→ hash 比對上次產物（6-28）→ 建進度檔（第一個寫入前）→ 產薄殼五檔到暫存 → config.toml 缺才產（含基準版副本）；寫入見「install（1″）」頁", v2=True)
b.box("i4ze0", E, 0, ENTRY, "來自「install（1）」頁：引擎已拿鎖（已寫 launcher_start）", 400)
b.box("i4e", E, 1, v2(D12), "薄殼已存在？", 250, ax="l")
b.box("i4en", E, 1, v2(SUB), "否：第一次 = 全新建", 120, ax="r")
b.box("i4x", U, 2, v2(O12), fl("1 + 6-28：薄殼被改過，列差異不動（零寫入）"), 220)
b.box("i4q", E, 2, v2(D12), "是 → 薄殼 == 上次產物？（自描述首行 hash）", 250, ax="l")
b.box("i4qn", P, 2, v2(NOTE), fl("自描述首行（Q17）：薄殼每檔（含 log.sh）# vendor_kit-shell/<介面版> engine=<vX> sha256=<其餘內容 LF 正規化 hash>；引擎重算 + 對 image 內模板二次比對；不用 gen/.stamp（不進 git）"), 360)
b.box("i4l", E, 3, v2(SUB), fl("是：建進度檔 .tmp.install.<id>.toml（第一次也建；第一個寫入（含暫存檔）之前）"), 300, ax="l")
b.box("i4lf", P, 3, v2(F12), "＋.vendor_kit/.tmp.install.<id>.toml（進度檔，不進 git；第一次 = 不留半成品的清除清單；install（2）頁最後刪）", 360)
b.box("i4", E, 4, v2(SUB), fl("產 .gitignore 到暫存（自描述首行；排除 cache/、gen/、log/、version.local.toml、.tmp.*）"), 300, ax="l")
b.box("i4_2", E, 5, v2(SUB), fl("產 entry.just 到暫存（自描述首行）"), 300, ax="l")
b.box("i4_3", E, 6, v2(SUB), fl("產 vendor.just 到暫存（自描述首行；source log.sh）"), 300, ax="l")
b.box("i4_3b", E, 7, v2(SUB), fl("產 log.sh 到暫存（自描述首行；POSIX；內嵌啟動器事件白名單）"), 300, ax="l")
b.box("i4_4", E, 8, v2(SUB), fl("產 ci/check.sh 到暫存（自描述在第二行）"), 300, ax="l")
b.box("i4_5q", E, 9, v2(D12), "config.toml 存在？（存在 → 不動）", 250, ax="l")
b.box("i4_5", E, 10, v2(SUB), fl("否：產 config.toml 到暫存（含註解與預設 schema=1、[log] keep=50、days=30）"), 300, ax="l")
b.box("i4_5b", E, 11, v2(SUB), fl("產 baseline/vendor_kit/config.toml 副本到暫存（其基準版）"), 300, ax="l")
b.box("i4z", E, 12, ENTRY, "續「install（1″）」頁：逐檔原子替換 → version.toml、gen/.stamp、基準版根檔", 400)
footer(b, F, 13, [("i4tx", v2(R12), fl("1：進度檔或暫存寫入失敗（任一步，共通匯流）→ 第一次：依進度檔清半成品；修復型：列已完成／未完成"), P, "c")], spacer=1, sp="l")
b.D("ie4a", "i4ze0", "i4e", "", 0.5, 0.5)
b.H("ie5n", "i4e", "i4en", "否"); b.D("ie5y", "i4e", "i4q", "是", al=True); b.H("ie5x", "i4q", "i4x", "否")
b.D("ie6", "i4q", "i4l", "是", al=True); b.D("ie6n", "i4en", "i4l", "", 0.5, 0.9)
b.H("ie6lf", "i4l", "i4lf", "寫"); b.D("ie6ln", "i4l", "i4", al=True)
b.D("ie4c", "i4", "i4_2"); b.D("ie4d", "i4_2", "i4_3"); b.D("ie4e", "i4_3", "i4_3b"); b.D("ie4e2", "i4_3b", "i4_4"); b.D("ie4f", "i4_4", "i4_5q", al=True)
b.D("ie4g", "i4_5q", "i4_5", "否", al=True); b.D("ie4h", "i4_5", "i4_5b"); b.D("ie5", "i4_5b", "i4z", "", 0.5, 0.5)
b.close()
sidebus(F, p5cm, "ie4gy", "i4_5q", "i4z", "是", busx=565, tx=0.15, pos=-0.85, vert="below")
failbus(F, p5cm, ["i4l", "i4", "i4_2", "i4_3", "i4_3b", "i4_4", "i4_5", "i4_5b"], "i4tx")
foot(p5cm, "p5cm", F.y, [t for t in T5I if t[0].startswith(("install 進度檔", "上次產物", "暫存目錄", "config.toml"))] + [("薄殼五檔", ".vendor_kit/ 內進 git 的 .gitignore、entry.just、vendor.just、log.sh、ci/check.sh；每檔帶自描述首行；只由 install／升引擎產生或重產")], ALL - {"inv", "tree", "pend", "rule"} | {"entry"})
addpage("v1p5cm", "流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存", p5cm)


b.box("c11cx", U, 8, v2(O12), fl("1：原 argv 與計畫不一致，請重跑"), 220)
b.box("c11c", E, 8, v2(D12), ARGV_Q, 400, ax="l")
b.box("c12x", U, 9, v2(O12), fl("1：dest 不合法（請修 init.toml／dest）"), 220)
b.box("c12", E, 9, v2(D12), fl("是 → init.toml 的 dest 全部合法？（任何寫入前檢查）"), 400, ax="l")
b.box("c12r", P, 9, v2(RULE), fl("dest 規則（v2.2 E）：兩工具 copy/copy、copy/append 同 dest → 拒絕；append/append 允許（各工具的行分開記；重疊或歸屬不明 → 拒絕）；正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；src 不得越出 dist；dist 含 symlink → 拒絕"), 360)
b.box("c12bx", U, 10, v2(O12), fl("1：命名空間撞名（請改名／移除撞名者）"), 220)
b.box("c12b", E, 10, v2(D12), fl("just/<ns>.just 的 <ns> 撞名？（其他工具／根 justfile recipe／module／alias／保留名 vendor_kit）"), 400, ax="l")
b.box("c12br", P, 10, v2(RULE), fl("命名空間撞名（v2.5 §5）：<ns> 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module／alias（just --dump --dump-format json）(c) 保留名 vendor_kit 相同 → 1 拒絕（撞名整個 just 會掛）"), 360)
b.box("c14x", U, 11, v2(O12), fl("1：印需改清單（CI 模式；請在本機執行後 commit 並 push）"), 220)
b.box("c14", E, 11, v2(D12), "CI 模式且需改任何進 git 的檔？", 340, ax=30)
b.box("c13y", U, 12, v2(G12), "0：唯讀預覽（印會建／會問哪些檔；讀 /dist/<repo>）", 220)
b.box("c13", E, 12, D12, "--dry-run？", 240, ax=80)
b.box("c13z", E, 13, ENTRY, "續「add（2）」頁：apply 寫入段（非 dry-run）", 300, ax="l")
footer(b, F, 14, [("c11x", v2(O12), fl("1 + 6-12：指紋不同「請重跑」（中間有人改了）"))], spacer=1, sp="r")
b.D("ce13e", "c9e", "c9q0", "", 0.5, 0.5)
b.H("ce12px", "c9p", "c9px", "失敗"); b.H("ce12bx", "c9b", "c9bx", "失敗")
b.D("ce13d", "c9b", "c10")
b.H("ce14", "c10", "c11a"); b.H("ce14ax", "c11a", "c11ax", ""); b.D("ce14b", "c11a", "c11b")
b.D("ce14c", "c11b", "c11c", al=True); b.H("ce14cx", "c11c", "c11cx", "否")
b.D("ce16", "c11c", "c12", "是", al=True); b.H("ce17", "c12", "c12x", "否"); b.D("ce18", "c12", "c12b", "是", al=True)
b.H("ce18x", "c12b", "c12bx", "是"); b.D("ce18b", "c12b", "c14", "否", al=True)
b.H("ce19", "c14", "c14x", "是"); b.D("ce20", "c14", "c13", "否", al=True)
b.H("ce21", "c13", "c13y", "是"); b.D("ce22", "c13", "c13z", "否", al=True)
b.close()
bypass(F, p5bp, "ce12y", "c9a", "c9b")
footer_edges(F, [("ce15", "c11b", "不同", "l", "c11x")])
foot(p5bp, "p5bp", F.y, _t5b("stdout", "/dist/<repo>", "dest 撞名", "命名空間", "6-26", "6-12", "resolve 非 0") + [PULLX_T], ALL - {"inv", "pend", "tree"} | {"entry"})
addpage("v1p5bcc", "流程 v2：add（1′）apply 前置", p5bp)

# ================= P5bc：add（2）apply 寫入段 =================
p5bc, F = newpage("流程 v2：add <repo>（2）apply 寫入段（§5、v2.2 C／E、v2.3 §1／§6、v2.5 §2～§4、v2.16-10）", "", COLS5)
b = F.band("bB2", "5b″ add <repo> apply 寫入段（承「add（1′）」頁：檢查通過、非 dry-run）：進度檔 → 取件 → 印記 → 初始檔逐檔到暫存 → 原子替換 → 基準版 → metadata → tools.just → version.toml → 刪進度檔；任一寫入失敗 → 共通匯流 → 1", v2=True)
b.box("c13c", E, 0, ENTRY, "來自「add（1′）」頁：apply 檢查通過（非 dry-run；已寫 launcher_start）", 300)
b.box("c15a", E, 1, v2(SUB), fl("建進度檔：metadata [progress]（state=in-progress、started、verb、id、done／pending；第一個寫入前）"), 400)
b.box("c15af", P, 1, F12, "＋baseline/<repo>/.vendor_kit.toml（[progress] state=in-progress、started、verb、id=trace_id、done、pending）", 360)
b.box("c15", E, 2, v2(SUB), fl("取件（fetch）：/dist/<repo> 複製到暫存目錄"), 400)

exec
/usr/bin/bash -lc "sed -n '590,620p' disc_v1_b.py; sed -n '1255,1290p' disc_v1_b.py; sed -n '2038,2080p' disc_v1_b.py" in <scratchpad>
 succeeded in 0ms:
    else:
        b.box(f"{pid}pr", rcol, row, v2(SUB), fl("是：先恢復（依進度檔 done／pending 續跑上次未完成的交易）"), 300, ax="l")
        b.box(f"{pid}px", xcol, row, v2(R12), fl(E27X), 200)
        b.H(f"{pid}pe_y", f"{pid}pq", f"{pid}pr", "是"); b.H(f"{pid}pe_x", f"{pid}pr", f"{pid}px", "失敗")
        b.D(f"{pid}pe_r", f"{pid}pr", nxt, "", 0.5, nxt_tx)   # nxt 是菱形 → nxt_tx=0.5（頂點）
    b.D(f"{pid}pe_n", f"{pid}pq", nxt, "否", al=True)
    return row + 1

def res3(b, pid, row, nxt, w=280, col=L, xcol=U, xw=220):
    """resolve 結果三叉（v2.16-2）：{pid}q0「resolve 回 0？」否 → {pid}q0x 橙原碼傳出；{pid}q1「vk-resolve/1 文法合法？」否 → {pid}q1x 紅 6-30；是 → nxt。回傳 row+2。"""
    b.box(f"{pid}q0", col, row, v2(D12), "resolve 回 0？", w)
    b.box(f"{pid}q0x", xcol, row, v2(O12), fl(NZX), xw)
    b.box(f"{pid}q1", col, row + 1, v2(D12), fl("是 → vk-resolve/1 文法合法？"), w)
    b.box(f"{pid}q1x", xcol, row + 1, v2(R12), fl(E30X), xw)
    b.H(f"{pid}qe_0x", f"{pid}q0", f"{pid}q0x", "否"); b.D(f"{pid}qe_01", f"{pid}q0", f"{pid}q1", "是", al=True)
    b.H(f"{pid}qe_1x", f"{pid}q1", f"{pid}q1x", "否"); b.D(f"{pid}qe_1n", f"{pid}q1", nxt, "是", al=True)
    return row + 2

def failbus(F, cells, srcs, end, busx=1610, sy=0.85, stub=16, label="失敗", tx=0.5):
    """共通失敗匯流（v2.16-10）：每個寫入格右側短線（y=sy）→ 該列下方縫隙 → x=busx 匯流排 → 終點上方一層 → 終點頂端（多條線在匯流排上重疊 = 一條匯流排）。
    close() 之後呼叫；終點列前放一列 spacer（footer(spacer=1)）給水平層用。"""
    A, RB, RT, g = F.abs, F.rb, F.rt, F.gap
    tx0, ty0, tw, th = A[end]; nx = tx0 + tx * tw; lev = RT[end] - g / 2 - 12
    for s in srcs:
        lab = label
        if isinstance(s, tuple): s, lab = s
        syy = 0.5 if F.st.get(s, "").startswith("rhombus") else sy                  # 菱形：從右頂點出
        sx0, sy0, sw, sh = A[s]; ex, ey = sx0 + sw, sy0 + syy * sh; hx = ex + stub; gy = RB[s] + g / 2
        pts = [(hx, ey), (hx, gy), (busx, gy), (busx, lev), (nx, lev)]
        tot = stub + (gy - ey) + (busx - hx) + (lev - gy) + (busx - nx) + (ty0 - lev)
        lw = sum(12 if ord(c) > 255 else 7 for c in (lab or ""))
p6r.append(_edge("te15y", "tq", "t0", "是：下一個工具", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈：走頁面最右側（x=1610）回 t0 頂點
foot(p6r, "p6r", F.y - 60, _t6("待辦清單", "verify", "完成標記", "覆寫兩種", "gen/ 三種") + [("6-5／6-13（CI 模式升為失敗）", "6-5 基準版落後（最後合併版本 ≠ version.toml；CI 模式 → 1，本機 warn 繼續）；6-13 metadata 無完成標記 = add 沒做完 → 1「請先 add <repo>」"), ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend"} | {"entry"})
addpage("v1p6cc", "流程 v2：sync（1′）引擎 resolve", p6r)

# ================= P6c：sync（2）第 2 段 apply =================
p6c, F = newpage("流程 v2：sync（2）三叉 → docker（多 extract 迴圈）→ apply 前置（§6、v2.16-2／-11）", "", COLS5)
b = F.band("eB", "sync 第 2 段（承「sync（1′）」頁：三叉已通過）：每個 extract：inspect → 無才 pull → extract → 還有下一個？→ docker run apply sync → flock（逾時 6-26）→ 重驗指紋 → argv 一致；寫入段見「sync（2′）」頁", v2=True)
b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（apply|yes；已寫 launcher_start）", 280)
b.box("m0q0", L, 1, v2(W12), "啟動器已驗完 resolve 三叉（回 0、文法合法、apply|yes）", 280)
b.box("m0m", L, 2, v2(W12), fl("處理 mount 記錄：驗 <dir>/dist/init.toml；記 -v <dir>/dist:/dist/<repo>:ro"), 280)
pullseg(b, 3, ("m0a", "m0p", "m0g"), ("是 → 對每個 extract：docker image inspect 本機有？", "無：docker pull", "<repo>-dist@digest\n（鎖定版；多架構 index）"), ("m0b", v2(W12), fl("extract /dist 到暫存（create／cp／rm 見契約④）")), w=(260, 200, 260))
b.box("m0px", U, 4, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
b.box("m0bx", U, 5, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
b.box("m0lq", L, 6, v2(D12), "還有下一個 extract？", 240)
b.box("m1", L, 7, v2(W12), fl("否：docker run … -v <tmp>:/dist:ro（含 vk-resolve）<引擎> apply sync"), 280)
b.box("m2a", E, 7, v2(SUB), fl("apply：flock 專案目錄（60 秒；VENDOR_KIT_NO_LOCK=1 可關）"), 400)
b.box("m2ax", G, 7, v2(R12), fl(E26X), 200)
b.box("m2b", E, 8, v2(D12), "重驗 resolve 的輸入指紋：相同？", 400)
b.box("m2x", U, 8, v2(O12), fl("1 + 6-12：指紋不同「請重跑」"), 220)
b.box("m2cx", U, 9, v2(O12), fl("1：原 argv 與計畫不一致，請重跑"), 220)
b.box("m2c", E, 9, v2(D12), ARGV_Q, 300, ax="l")
b.box("m2z", E, 10, ENTRY, "是：續「sync（2′）」頁：逐工具取件 → 印記 → 驗 → tools.just", 400)
b.D("me0", "m00", "m0q0", "", 0.5, 0.5)
b.D("me0m", "m0q0", "m0m", al=True); b.D("me0q", "m0m", "m0a", al=True); b.H("me0px", "m0p", "m0px", "失敗"); b.H("me0bx", "m0b", "m0bx", "失敗")
b.D("me0lq", "m0b", "m0lq", al=True); b.D("me1", "m0lq", "m1", "否", al=True)
b.H("me2", "m1", "m2a"); b.H("me2ax", "m2a", "m2ax", "逾時"); b.D("me2b", "m2a", "m2b"); b.H("me2x", "m2b", "m2x", "否"); b.D("me2c", "m2b", "m2c", "是", al=True); b.H("me2cx", "m2c", "m2cx", "否")
b.D("me3", "m2c", "m2z", "是", al=True)
b.close()
bypass(F, p6c, "me0y", "m0a", "m0b")
_A = F.abs; _sx, _sy, _sw, _sh = _A["m0lq"]; _tx, _ty, _tw, _th = _A["m0a"]; _ey = _sy + _sh / 2; _gy = F.rt["m0a"] - F.gap / 2; _nx = _tx + _tw / 2; _bx = 1250
_tot = (_bx - (_sx + _sw)) + (_ey - _gy) + (_bx - _nx) + 10
p6c.append(_edge("me0ly", "m0lq", "m0a", "是：下一個 extract", (1, 0.5), (0.5, 0), [(_bx, _ey), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))   # 迴圈走右側（避開左側失敗線）
foot(p6c, "p6c", F.y, _t6("待辦清單", "6-26", "extract", "原 argv", "6-12", "resolve 非 0") + [PULLX_T, ("6-30", "啟動器驗 vk-resolve/1 文法不合 →「引擎輸出不完整或不相容（<原因>），未執行任何動作。」（結束 1）")], ALL - {"tree", "pend", "rule", "inv"} | {"entry"})
addpage("v1p6c", "流程 v2：sync（2）三叉 → docker → apply 前置", p6c)

# ================= P6cw：sync（2′）apply 寫入段 =================
failbus(F, p8v, ["v2p", "v2b", "v2d"], "v2bx")
footer_edges(F, [("ve5z", "v2d", "", "d", "v2z")])
p8v.append(_edge("ve12", "v2z", "v10", "", (0, 0.5), (1, 0.5), [], None))
foot(p8v, "p8v", F.y, _k8("覆寫兩種", "dev 進度檔", "RepoDigests", "docker image inspect", "統一提示", "6-27", "6-26"), ALL - {"inv", "pend", "tree", "rule"} | {"entry"})
addpage("v1p8ccc", "流程 v2：dev vendor_kit", p8v)

# ================= P8c：undev（1）resolve → 三叉 → docker → apply 前置 =================
p8c, F = newpage("流程 v2：undev <repo>（1）執行紀錄 → resolve → 三叉 → docker → apply 前置（v2.5 §10）", "", COLS5)
b = F.band("vB", "undev <repo>（1）：回到 version.toml 鎖定版 = 執行紀錄 → 偵測既有進度檔 → resolve（不寫）→ 啟動器三叉 → inspect → 無才 pull → extract → apply：flock（逾時 6-26）→ 重驗指紋 → argv；寫入段見「undev（2）」頁", v2=True)
b.box("u0", U, 0, G12, "just vendor_kit undev <repo>", 220)
lstart(b, "u0l", "u0x", 0, "undev")
preseg(b, "u", 2, "u1", "undev")
b.box("u1", L, 3, v2(W12), "docker run 引擎 resolve undev <repo>", 280)
b.box("u1e", E, 3, v2(SUB), "resolve（不寫任何檔）：讀 version.toml、version.local.toml", 400)
b.box("u3", U, 4, G12, "0：未啟用 dev（提示）", 220)
b.box("u2", E, 4, D12, "有 path 覆寫？", 220, ax="l")
b.box("u4b", E, 5, v2(SUB), fl("是：算執行計畫（extract 鎖定版；只有 extract 一項）"), 400)
b.box("u4c", E, 6, v2(SUB), fl("產生輸入指紋（同 add（1）頁「輸入指紋」）"), 400)
b.box("u4d", E, 7, v2(SUB), fl("stdout vk-resolve/1：extract 清單、apply|yes、指紋（只傳協定內容）"), 400)
res3(b, "u4", 8, "u5a")
pullseg(b, 10, ("u5a", "u5p", "u5g"), ("是 → docker image inspect：本機有？", "無：docker pull", "<repo>-dist@digest（鎖定版）"), ("u5b", v2(W12), fl("extract /dist 到暫存（見契約④）")), w=(260, 200, 260))
b.box("u5px", U, 11, v2(R12), fl("1 + 6-24／6-31：pull 失敗／逾時"), 220)
b.box("u5bx", U, 12, v2(R12), fl("1：extract 失敗（create／cp／rm 或暫存目錄）"), 220)
b.box("u5r", L, 13, v2(W12), fl("docker run … -v <tmp>:/dist:ro（含 vk-resolve）引擎 apply undev <repo>"), 280)
b.box("u6a", E, 13, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("u6ax", G, 13, v2(R12), fl(E26X), 200)
b.box("u6bx", U, 14, v2(O12), "1 + 6-12：指紋不同「請重跑」", 220)
b.box("u6b", E, 14, v2(D12), "重驗指紋：相同？", 300, ax="l")
b.box("u6b2x", U, 15, v2(O12), "1：原 argv 與計畫不一致，請重跑", 220)
b.box("u6b2", E, 15, v2(D12), ARGV_Q, 300, ax="l")
b.box("u6z", E, 16, ENTRY, "是：續「undev（2）」頁：建進度檔 → 撤覆寫行 → 拆 symlink → 取件鎖定版 → 印記 → 刪進度檔", 400)
b.H("ue1", "u0", "u0l0"); b.D("ue1l", "u0l", "upq", al=True); b.H("ue1e", "u1", "u1e"); b.D("ue2", "u1e", "u2", al=True); b.H("ue3", "u2", "u3", "否"); b.D("ue4", "u2", "u4b", "是", 0.5, 0.5)
b.D("ue4c", "u4b", "u4c"); b.D("ue4d", "u4c", "u4d"); b.D("ue5", "u4d", "u4q0", "", 0.5, 0.5)
b.H("ue5px", "u5p", "u5px", "失敗"); b.H("ue5bx", "u5b", "u5bx", "失敗")
b.D("ue7", "u5b", "u5r")
b.H("ue8", "u5r", "u6a"); b.H("ue8ax", "u6a", "u6ax", "逾時"); b.D("ue8b", "u6a", "u6b", al=True); b.H("ue8x", "u6b", "u6bx", "否"); b.D("ue8c", "u6b", "u6b2", "是", al=True); b.H("ue8cx", "u6b2", "u6b2x", "否")
b.D("ue9", "u6b2", "u6z", "是", al=True)
b.close()
bypass(F, p8c, "ue5y", "u5a", "u5b")
foot(p8c, "p8c", F.y, _k8("覆寫兩種", "docker image inspect", "6-27", "6-26", "6-30", "原 argv", "6-12") + [PULLX_T], ALL - {"inv", "pend", "tree", "rule"} | {"entry"})
addpage("v1p8c", "流程 v2：undev <repo>（1）resolve → apply 前置", p8c)

# ================= P8cx：undev（2）寫入段 =================

codex
基線產圖成功。三頁的處理方向已確認：`me8ax` 依既有頁做法移除線上「逾時」字（紅色 6-26 終點本身已完整表意）；v1p7bcc 會把 `se12f` 的「否」改成從來源旁直下，並把 `se11y` 回繞外移；v1p7bccd 會把 grep 與判斷拆成兩格。v1p8b 的未接入語意牽涉三叉結構，為避免在本輪硬改協定流程，我會按規則留下該頁黃便條。
apply patch
patch: completed
<scratchpad>/disc_v1_b.py
diff --git a/disc_v1_b.py b/disc_v1_b.py
index 263512664407ca4bc04b3449a1d0add6e332ef95..2014c76c15d6f0fee27d6267e24bc97cf6f1542a
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -1784,7 +1784,7 @@
 b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
 b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
 b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
-b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
+b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
 b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
 b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
 b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
@@ -1800,14 +1800,18 @@
 b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
 b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
 b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
-b.D("se12tt", "s12t", "s12tt", "是", al=True)
+b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
 b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
 b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
 b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
 b.close()
-bypass(F, p7bcc, "se11y", "s11n", "s11v")
-sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
 _A = F.abs
+_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
+_bx, _gy, _nx = 1250, _ty, _tx + _tw / 2
+_tot = (_bx - (_sx + _sw)) + (_gy - (_sy + _sh / 2)) + (_bx - _nx)
+p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (1, 0.5), (0.5, 0),
+                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
+_A = F.abs
 def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
     sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
     hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
@@ -1932,15 +1936,16 @@
 b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
 b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
 b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
-b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
-b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
+b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
 b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
 b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
-b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
-b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
+b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
+b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
+b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
+b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
 b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
 b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
-b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
+b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
 b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
 b.close()
 lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
@@ -2204,10 +2209,11 @@
 b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
 b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
 b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
-b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
+b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
 b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
 b.close()
-foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
+pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
+foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
 addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
 
 # ================= P8bccc：remove（2）寫入段 =================

diff --git a/disc_v1_b.py b/disc_v1_b.py
index 263512664407ca4bc04b3449a1d0add6e332ef95..2014c76c15d6f0fee27d6267e24bc97cf6f1542a
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -1784,7 +1784,7 @@
 b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
 b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
 b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
-b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
+b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
 b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
 b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
 b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
@@ -1800,14 +1800,18 @@
 b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
 b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
 b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
-b.D("se12tt", "s12t", "s12tt", "是", al=True)
+b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
 b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
 b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
 b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
 b.close()
-bypass(F, p7bcc, "se11y", "s11n", "s11v")
-sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
 _A = F.abs
+_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
+_bx, _gy, _nx = 1250, _ty, _tx + _tw / 2
+_tot = (_bx - (_sx + _sw)) + (_gy - (_sy + _sh / 2)) + (_bx - _nx)
+p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (1, 0.5), (0.5, 0),
+                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
+_A = F.abs
 def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
     sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
     hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
@@ -1932,15 +1936,16 @@
 b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
 b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
 b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
-b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
-b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
+b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
 b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
 b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
-b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
-b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
+b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
+b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
+b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
+b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
 b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
 b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
-b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
+b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
 b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
 b.close()
 lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
@@ -2204,10 +2209,11 @@
 b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
 b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
 b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
-b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
+b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
 b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
 b.close()
-foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
+pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
+foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
 addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
 
 # ================= P8bccc：remove（2）寫入段 =================

exec
/usr/bin/bash -lc 'python3 run_v1_b.py && python3 check_overflow.py v1_b.drawio && python3 check_overlap.py v1_b.drawio && python3 check_cross_v1b.py v1_b.drawio && python3 check_self_v1b.py v1_b.drawio && python3 check_jog_r7.py v1_b.drawio && python3 check_align_v1b.py v1_b.drawio' in <scratchpad>
 exited 1 in 901ms:
v1p5 流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別 page ('1660', '1919')
v1p5x 流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版 page ('1660', '1311')
v1p5i 流程 v2：bootstrap.sh（1′）docker run install page ('1660', '1364')
v1p5ccc 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add page ('1660', '1878')
v1p5c 流程 v2：install（1）主機檢查 → 引擎 image → docker run page ('1660', '1606')
v1p5cm 流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存 page ('1660', '1734')
v1p5cw 流程 v2：install（1″）寫入 page ('1660', '1808')
v1p5cc 流程 v2：install（2）根 justfile 與 .dockerignore page ('1660', '2014')
v1p5b 流程 v2：add（1）resolve → docker page ('1660', '2273')
v1p5bcc 流程 v2：add（1′）apply 前置 page ('1660', '2219')
v1p5bc 流程 v2：add（2）apply 寫入段 page ('1660', '2301')
v1p6 流程 v2：sync（1）啟動器快路徑 page ('1660', '2124')
v1p6cc 流程 v2：sync（1′）引擎 resolve page ('1660', '2395')
v1p6c 流程 v2：sync（2）三叉 → docker → apply 前置 page ('1660', '1636')
v1p6cw 流程 v2：sync（2′）apply 寫入段 page ('1660', '1594')
v1p7 流程 v2：upgrade ── A. Renovate 路徑 page ('1660', '1821')
v1p7c 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker page ('1660', '2363')
v1p7ccc 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置 page ('1660', '2349')
v1p7cc 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併 page ('1660', '2394')
v1p7cccc 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入 page ('1660', '1569')
v1p7b 流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入 page ('1660', '2371')
v1p7bd 流程 v2：upgrade ── D. 回退 page ('1660', '2290')
v1p7bc 流程 v2：upgrade ── E. 升引擎 (a)(b) page ('1660', '2140')
v1p7bca 流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手 page ('1660', '1673')
v1p7bcc 流程 v2：upgrade ── E(c) upgrade vendor_kit（1） page ('1660', '2340')
v1p7bcx 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′） page ('1660', '1639')
v1p7bccc 流程 v2：upgrade ── E(c) upgrade vendor_kit（2） page ('1660', '1537')
v1p7bcce 流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml page ('1660', '2181')
v1p7bccd 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′） page ('1660', '1342')
v1p8 流程 v2：dev <repo> page ('1660', '2094')
v1p8ccc 流程 v2：dev vendor_kit page ('1660', '2121')
v1p8c 流程 v2：undev <repo>（1）resolve → apply 前置 page ('1660', '2178')
v1p8cx 流程 v2：undev <repo>（2）寫入段 page ('1660', '1315')
v1p8cc 流程 v2：undev vendor_kit page ('1660', '2303')
v1p8b 流程 v2：remove（1）resolve → apply 前置 page ('1660', '2322')
v1p8bccc 流程 v2：remove（2）寫入段 page ('1660', '2167')
v1p8bc 流程 v2：uninstall（1）resolve → apply 前置 page ('1660', '2394')
v1p8bcc 流程 v2：uninstall（2）寫入段 page ('1660', '2261')
== v1p5 流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別
   無
== v1p5x 流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版
   無
== v1p5i 流程 v2：bootstrap.sh（1′）docker run install
   無
== v1p5ccc 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add
   無
== v1p5c 流程 v2：install（1）主機檢查 → 引擎 image → docker run
   無
== v1p5cm 流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存
   無
== v1p5cw 流程 v2：install（1″）寫入
   無
== v1p5cc 流程 v2：install（2）根 justfile 與 .dockerignore
   無
== v1p5b 流程 v2：add（1）resolve → docker
   無
== v1p5bcc 流程 v2：add（1′）apply 前置
   無
== v1p5bc 流程 v2：add（2）apply 寫入段
   無
== v1p6 流程 v2：sync（1）啟動器快路徑
   無
== v1p6cc 流程 v2：sync（1′）引擎 resolve
   無
== v1p6c 流程 v2：sync（2）三叉 → docker → apply 前置
   無
== v1p6cw 流程 v2：sync（2′）apply 寫入段
   無
== v1p7 流程 v2：upgrade ── A. Renovate 路徑
   無
== v1p7c 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker
   無
== v1p7ccc 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置
   無
== v1p7cc 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併
   無
== v1p7cccc 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入
   無
== v1p7b 流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入
   無
== v1p7bd 流程 v2：upgrade ── D. 回退
   無
== v1p7bc 流程 v2：upgrade ── E. 升引擎 (a)(b)
   無
== v1p7bca 流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手
   無
== v1p7bcc 流程 v2：upgrade ── E(c) upgrade vendor_kit（1）
   無
== v1p7bcx 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′）
   無
== v1p7bccc 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）
   無
== v1p7bcce 流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml
   無
== v1p7bccd 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′）
   無
== v1p8 流程 v2：dev <repo>
   無
== v1p8ccc 流程 v2：dev vendor_kit
   無
== v1p8c 流程 v2：undev <repo>（1）resolve → apply 前置
   無
== v1p8cx 流程 v2：undev <repo>（2）寫入段
   無
== v1p8cc 流程 v2：undev vendor_kit
   無
== v1p8b 流程 v2：remove（1）resolve → apply 前置
   無
== v1p8bccc 流程 v2：remove（2）寫入段
   無
== v1p8bc 流程 v2：uninstall（1）resolve → apply 前置
   無
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
== v1p5 流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別
   無
== v1p5x 流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版
   無
== v1p5i 流程 v2：bootstrap.sh（1′）docker run install
   無
== v1p5ccc 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add
   無
== v1p5c 流程 v2：install（1）主機檢查 → 引擎 image → docker run
   無
== v1p5cm 流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存
   無
== v1p5cw 流程 v2：install（1″）寫入
   無
== v1p5cc 流程 v2：install（2）根 justfile 與 .dockerignore
   無
== v1p5b 流程 v2：add（1）resolve → docker
   無
== v1p5bcc 流程 v2：add（1′）apply 前置
   無
== v1p5bc 流程 v2：add（2）apply 寫入段
   無
== v1p6 流程 v2：sync（1）啟動器快路徑
   無
== v1p6cc 流程 v2：sync（1′）引擎 resolve
   無
== v1p6c 流程 v2：sync（2）三叉 → docker → apply 前置
   無
== v1p6cw 流程 v2：sync（2′）apply 寫入段
   無
== v1p7 流程 v2：upgrade ── A. Renovate 路徑
   無
== v1p7c 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker
   無
== v1p7ccc 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置
   無
== v1p7cc 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併
   無
== v1p7cccc 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入
   無
== v1p7b 流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入
   無
== v1p7bd 流程 v2：upgrade ── D. 回退
   無
== v1p7bc 流程 v2：upgrade ── E. 升引擎 (a)(b)
   無
== v1p7bca 流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手
   無
== v1p7bcc 流程 v2：upgrade ── E(c) upgrade vendor_kit（1）
   se11y (s11n→s11v) 壓到 s11v_v2「v2」 ['']
== v1p7bcx 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′）
   無
== v1p7bccc 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）
   無
== v1p7bcce 流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml
   無
== v1p7bccd 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′）
   無
== v1p8 流程 v2：dev <repo>
   無
== v1p8ccc 流程 v2：dev vendor_kit
   無
== v1p8c 流程 v2：undev <repo>（1）resolve → apply 前置
   無
== v1p8cx 流程 v2：undev <repo>（2）寫入段
   無
== v1p8cc 流程 v2：undev vendor_kit
   無
== v1p8b 流程 v2：remove（1）resolve → apply 前置
   無
== v1p8bccc 流程 v2：remove（2）寫入段
   無
== v1p8bc 流程 v2：uninstall（1）resolve → apply 前置
   無
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 1 筆

diff --git a/disc_v1_b.py b/disc_v1_b.py
index 263512664407ca4bc04b3449a1d0add6e332ef95..2014c76c15d6f0fee27d6267e24bc97cf6f1542a
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -1784,7 +1784,7 @@
 b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
 b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
 b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
-b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
+b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
 b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
 b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
 b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
@@ -1800,14 +1800,18 @@
 b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
 b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
 b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
-b.D("se12tt", "s12t", "s12tt", "是", al=True)
+b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
 b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
 b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
 b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
 b.close()
-bypass(F, p7bcc, "se11y", "s11n", "s11v")
-sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
 _A = F.abs
+_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
+_bx, _gy, _nx = 1250, _ty, _tx + _tw / 2
+_tot = (_bx - (_sx + _sw)) + (_gy - (_sy + _sh / 2)) + (_bx - _nx)
+p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (1, 0.5), (0.5, 0),
+                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
+_A = F.abs
 def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
     sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
     hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
@@ -1932,15 +1936,16 @@
 b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
 b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
 b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
-b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
-b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
+b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
 b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
 b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
-b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
-b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
+b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
+b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
+b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
+b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
 b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
 b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
-b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
+b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
 b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
 b.close()
 lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
@@ -2204,10 +2209,11 @@
 b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
 b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
 b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
-b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
+b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
 b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
 b.close()
-foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
+pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
+foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
 addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
 
 # ================= P8bccc：remove（2）寫入段 =================

codex
第一輪檢查抓到 1 筆：外移後的 `se11y` 在進入 `s11v` 頂點前碰到它的 v2 小標。這正是檢查器要攔的情況；我會把這條「本機有」旁路改走左側空白匯流排，不再包住紫框，也避開 v2 標，再重跑全套。
apply patch
patch: completed
<scratchpad>/disc_v1_b.py
diff --git a/disc_v1_b.py b/disc_v1_b.py
index 263512664407ca4bc04b3449a1d0add6e332ef95..972a8c246538666a11d80305134af695d820e8a2
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -1784,7 +1784,7 @@
 b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
 b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
 b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
-b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
+b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
 b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
 b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
 b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
@@ -1800,14 +1800,18 @@
 b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
 b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
 b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
-b.D("se12tt", "s12t", "s12tt", "是", al=True)
+b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
 b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
 b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
 b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
 b.close()
-bypass(F, p7bcc, "se11y", "s11n", "s11v")
-sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
 _A = F.abs
+_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
+_bx, _gy, _nx = 270, F.rt["s11v"] - F.gap / 2, _tx + _tw / 2
+_tot = (_sx - _bx) + (_gy - (_sy + _sh / 2)) + (_nx - _bx)
+p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (0, 0.5), (0.5, 0),
+                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
+_A = F.abs
 def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
     sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
     hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
@@ -1932,15 +1936,16 @@
 b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
 b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
 b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
-b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
-b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
+b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
 b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
 b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
-b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
-b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
+b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
+b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
+b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
+b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
 b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
 b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
-b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
+b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
 b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
 b.close()
 lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
@@ -2204,10 +2209,11 @@
 b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
 b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
 b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
-b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
+b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
 b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
 b.close()
-foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
+pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
+foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
 addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
 
 # ================= P8bccc：remove（2）寫入段 =================

diff --git a/disc_v1_b.py b/disc_v1_b.py
index 263512664407ca4bc04b3449a1d0add6e332ef95..972a8c246538666a11d80305134af695d820e8a2
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -1784,7 +1784,7 @@
 b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
 b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
 b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
-b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
+b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
 b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
 b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
 b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
@@ -1800,14 +1800,18 @@
 b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
 b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
 b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
-b.D("se12tt", "s12t", "s12tt", "是", al=True)
+b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
 b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
 b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
 b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
 b.close()
-bypass(F, p7bcc, "se11y", "s11n", "s11v")
-sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
 _A = F.abs
+_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
+_bx, _gy, _nx = 270, F.rt["s11v"] - F.gap / 2, _tx + _tw / 2
+_tot = (_sx - _bx) + (_gy - (_sy + _sh / 2)) + (_nx - _bx)
+p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (0, 0.5), (0.5, 0),
+                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
+_A = F.abs
 def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
     sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
     hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
@@ -1932,15 +1936,16 @@
 b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
 b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
 b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
-b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
-b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
+b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
 b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
 b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
-b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
-b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
+b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
+b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
+b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
+b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
 b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
 b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
-b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
+b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
 b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
 b.close()
 lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
@@ -2204,10 +2209,11 @@
 b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
 b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
 b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
-b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
+b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
 b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
 b.close()
-foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
+pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
+foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
 addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
 
 # ================= P8bccc：remove（2）寫入段 =================

exec
/usr/bin/bash -lc 'python3 run_v1_b.py >/tmp/run_v1_b.log && for c in check_overflow.py check_overlap.py check_cross_v1b.py check_self_v1b.py check_jog_r7.py check_align_v1b.py; do echo "== $c =="; python3 "$c" v1_b.drawio | tail -n 5; done' in <scratchpad>
 succeeded in 1636ms:
== check_overflow.py ==
== v1p8bc 流程 v2：uninstall（1）resolve → apply 前置
   無
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
== check_overlap.py ==
== v1p8bc 流程 v2：uninstall（1）resolve → apply 前置
   無
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
== check_cross_v1b.py ==
== v1p8bc 流程 v2：uninstall（1）resolve → apply 前置
   無
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 1 筆
== check_self_v1b.py ==
== v1p8bc 流程 v2：uninstall（1）resolve → apply 前置
   無
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
== check_jog_r7.py ==
共 0 筆
== check_align_v1b.py ==
   無
== 流程 v2：uninstall（1）resolve → apply 前置
   無
== 流程 v2：uninstall（2）寫入段
   無

diff --git a/disc_v1_b.py b/disc_v1_b.py
index 263512664407ca4bc04b3449a1d0add6e332ef95..972a8c246538666a11d80305134af695d820e8a2
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -1784,7 +1784,7 @@
 b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
 b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
 b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
-b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
+b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
 b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
 b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
 b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
@@ -1800,14 +1800,18 @@
 b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
 b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
 b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
-b.D("se12tt", "s12t", "s12tt", "是", al=True)
+b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
 b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
 b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
 b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
 b.close()
-bypass(F, p7bcc, "se11y", "s11n", "s11v")
-sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
 _A = F.abs
+_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
+_bx, _gy, _nx = 270, F.rt["s11v"] - F.gap / 2, _tx + _tw / 2
+_tot = (_sx - _bx) + (_gy - (_sy + _sh / 2)) + (_nx - _bx)
+p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (0, 0.5), (0.5, 0),
+                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
+_A = F.abs
 def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
     sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
     hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
@@ -1932,15 +1936,16 @@
 b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
 b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
 b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
-b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
-b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
+b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
 b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
 b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
-b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
-b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
+b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
+b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
+b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
+b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
 b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
 b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
-b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
+b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
 b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
 b.close()
 lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
@@ -2204,10 +2209,11 @@
 b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
 b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
 b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
-b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
+b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
 b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
 b.close()
-foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
+pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
+foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
 addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
 
 # ================= P8bccc：remove（2）寫入段 =================

exec
/usr/bin/bash -lc "python3 check_cross_v1b.py v1_b.drawio | rg -C 2 'v1p7bcc|se11y|共'" in <scratchpad>
 succeeded in 117ms:
== v1p7bca 流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手
   無
== v1p7bcc 流程 v2：upgrade ── E(c) upgrade vendor_kit（1）
   se11px × se11y at ((340.0, 557.0),(260.0, 557.0)) / ((270.0, 468.0),(270.0, 596.0))
== v1p7bcx 流程 v2：upgrade ── E(c) upgrade vendor_kit（1′）
   無
== v1p7bccc 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）
   無
== v1p7bcce 流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml
   無
== v1p7bccd 流程 v2：upgrade ── E(c) upgrade vendor_kit（2′）
   無
== v1p8 流程 v2：dev <repo>
--
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 1 筆

diff --git a/disc_v1_b.py b/disc_v1_b.py
index 263512664407ca4bc04b3449a1d0add6e332ef95..972a8c246538666a11d80305134af695d820e8a2
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -1784,7 +1784,7 @@
 b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
 b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
 b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
-b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
+b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
 b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
 b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
 b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
@@ -1800,14 +1800,18 @@
 b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
 b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
 b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
-b.D("se12tt", "s12t", "s12tt", "是", al=True)
+b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
 b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
 b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
 b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
 b.close()
-bypass(F, p7bcc, "se11y", "s11n", "s11v")
-sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
 _A = F.abs
+_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
+_bx, _gy, _nx = 270, F.rt["s11v"] - F.gap / 2, _tx + _tw / 2
+_tot = (_sx - _bx) + (_gy - (_sy + _sh / 2)) + (_nx - _bx)
+p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (0, 0.5), (0.5, 0),
+                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
+_A = F.abs
 def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
     sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
     hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
@@ -1932,15 +1936,16 @@
 b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
 b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
 b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
-b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
-b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
+b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
 b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
 b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
-b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
-b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
+b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
+b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
+b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
+b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
 b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
 b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
-b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
+b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
 b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
 b.close()
 lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
@@ -2204,10 +2209,11 @@
 b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
 b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
 b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
-b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
+b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
 b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
 b.close()
-foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
+pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
+foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
 addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
 
 # ================= P8bccc：remove（2）寫入段 =================

apply patch
patch: completed
<scratchpad>/disc_v1_b.py
diff --git a/disc_v1_b.py b/disc_v1_b.py
index 263512664407ca4bc04b3449a1d0add6e332ef95..b9e4e3be3dded92229cb5d9c5697157fc0488f4a
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -1784,7 +1784,7 @@
 b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
 b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
 b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
-b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
+b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
 b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
 b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
 b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
@@ -1800,14 +1800,18 @@
 b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
 b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
 b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
-b.D("se12tt", "s12t", "s12tt", "是", al=True)
+b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
 b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
 b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
 b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
 b.close()
-bypass(F, p7bcc, "se11y", "s11n", "s11v")
-sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
 _A = F.abs
+_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
+_bx, _gy, _nx = 30, F.rt["s11v"] - F.gap / 2, _tx + _tw / 2
+_tot = (_sx - _bx) + (_gy - (_sy + _sh / 2)) + (_nx - _bx)
+p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (0, 0.5), (0.5, 0),
+                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
+_A = F.abs
 def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
     sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
     hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
@@ -1932,15 +1936,16 @@
 b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
 b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
 b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
-b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
-b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
+b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
 b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
 b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
-b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
-b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
+b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
+b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
+b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
+b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
 b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
 b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
-b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
+b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
 b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
 b.close()
 lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
@@ -2204,10 +2209,11 @@
 b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
 b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
 b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
-b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
+b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
 b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
 b.close()
-foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
+pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
+foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
 addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
 
 # ================= P8bccc：remove（2）寫入段 =================

diff --git a/disc_v1_b.py b/disc_v1_b.py
index 263512664407ca4bc04b3449a1d0add6e332ef95..b9e4e3be3dded92229cb5d9c5697157fc0488f4a
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -1784,7 +1784,7 @@
 b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
 b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
 b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
-b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
+b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
 b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
 b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
 b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
@@ -1800,14 +1800,18 @@
 b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
 b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
 b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
-b.D("se12tt", "s12t", "s12tt", "是", al=True)
+b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
 b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
 b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
 b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
 b.close()
-bypass(F, p7bcc, "se11y", "s11n", "s11v")
-sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
 _A = F.abs
+_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
+_bx, _gy, _nx = 30, F.rt["s11v"] - F.gap / 2, _tx + _tw / 2
+_tot = (_sx - _bx) + (_gy - (_sy + _sh / 2)) + (_nx - _bx)
+p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (0, 0.5), (0.5, 0),
+                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
+_A = F.abs
 def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
     sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
     hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
@@ -1932,15 +1936,16 @@
 b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
 b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
 b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
-b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
-b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
+b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
 b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
 b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
-b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
-b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
+b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
+b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
+b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
+b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
 b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
 b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
-b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
+b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
 b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
 b.close()
 lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
@@ -2204,10 +2209,11 @@
 b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
 b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
 b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
-b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
+b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
 b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
 b.close()
-foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
+pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
+foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
 addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
 
 # ================= P8bccc：remove（2）寫入段 =================

2026-09-20T15:42:07.414930Z ERROR codex_core::tools::router: error=exec_command failed: CreateProcess { message: "Rejected(\"`/usr/bin/bash -lc 'python3 run_v1_b.py >/tmp/run_v1_b.log && for c in check_overflow.py check_overlap.py check_cross_v1b.py check_self_v1b.py check_jog_r7.py check_align_v1b.py; do echo \\\"== $c ==\\\"; python3 \\\"$c\\\" v1_b.drawio | tail -n 3; done && rm -rf r15_b_out && python3 extract_pages.py v1_b.drawio r15_b_out && python3 lint_pages.py r15_b_out'` rejected: rm -f style commands are not permitted. Use a safer approach\")" }
diff --git a/disc_v1_b.py b/disc_v1_b.py
index 263512664407ca4bc04b3449a1d0add6e332ef95..b9e4e3be3dded92229cb5d9c5697157fc0488f4a
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -1784,7 +1784,7 @@
 b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
 b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
 b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
-b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
+b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
 b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
 b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
 b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
@@ -1800,14 +1800,18 @@
 b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
 b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
 b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
-b.D("se12tt", "s12t", "s12tt", "是", al=True)
+b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
 b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
 b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
 b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
 b.close()
-bypass(F, p7bcc, "se11y", "s11n", "s11v")
-sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
 _A = F.abs
+_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
+_bx, _gy, _nx = 30, F.rt["s11v"] - F.gap / 2, _tx + _tw / 2
+_tot = (_sx - _bx) + (_gy - (_sy + _sh / 2)) + (_nx - _bx)
+p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (0, 0.5), (0.5, 0),
+                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
+_A = F.abs
 def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
     sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
     hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
@@ -1932,15 +1936,16 @@
 b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
 b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
 b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
-b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
-b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
+b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
 b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
 b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
-b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
-b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
+b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
+b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
+b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
+b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
 b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
 b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
-b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
+b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
 b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
 b.close()
 lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
@@ -2204,10 +2209,11 @@
 b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
 b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
 b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
-b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
+b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
 b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
 b.close()
-foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
+pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
+foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
 addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
 
 # ================= P8bccc：remove（2）寫入段 =================

exec
/usr/bin/bash -lc 'python3 run_v1_b.py >/tmp/run_v1_b.log && for c in check_overflow.py check_overlap.py check_cross_v1b.py check_self_v1b.py check_jog_r7.py check_align_v1b.py; do echo "== $c =="; python3 "$c" v1_b.drawio | tail -n 3; done && python3 extract_pages.py v1_b.drawio r15_b_out && python3 lint_pages.py r15_b_out' in <scratchpad>
 succeeded in 2139ms:
== check_overflow.py ==
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
== check_overlap.py ==
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
== check_cross_v1b.py ==
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
== check_self_v1b.py ==
== v1p8bcc 流程 v2：uninstall（2）寫入段
   無
共 0 筆
== check_jog_r7.py ==
共 0 筆
== check_align_v1b.py ==
   無
== 流程 v2：uninstall（2）寫入段
   無
v1p5       nodes=  61 edges= 25 terms= 6 xrefs= 3  流程 v2：bootstrap.sh（1）檢查 → 引擎 ref → --local 判別
v1p5x      nodes=  48 edges= 13 terms= 6 xrefs= 5  流程 v2：bootstrap.sh（1″）引擎 image → LABEL 最低介面版
v1p5i      nodes=  54 edges= 11 terms= 5 xrefs= 4  流程 v2：bootstrap.sh（1′）docker run install
v1p5ccc    nodes=  62 edges= 23 terms= 7 xrefs= 6  流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add
v1p5c      nodes=  58 edges= 24 terms= 5 xrefs= 2  流程 v2：install（1）主機檢查 → 引擎 image → docker run
v1p5cm     nodes=  52 edges= 25 terms= 5 xrefs= 4  流程 v2：install（1′）比對薄殼 → 進度檔 → 暫存
v1p5cw     nodes=  61 edges= 30 terms= 5 xrefs= 4  流程 v2：install（1″）寫入
v1p5cc     nodes=  67 edges= 41 terms= 6 xrefs= 2  流程 v2：install（2）根 justfile 與 .dockerignore
v1p5b      nodes=  90 edges= 36 terms= 8 xrefs= 2  流程 v2：add（1）resolve → docker
v1p5bcc    nodes=  70 edges= 27 terms= 8 xrefs= 4  流程 v2：add（1′）apply 前置
v1p5bc     nodes=  83 edges= 53 terms= 8 xrefs= 2  流程 v2：add（2）apply 寫入段
v1p6       nodes=  69 edges= 23 terms= 8 xrefs= 2  流程 v2：sync（1）啟動器快路徑
v1p6cc     nodes=  75 edges= 40 terms= 7 xrefs= 4  流程 v2：sync（1′）引擎 resolve
v1p6c      nodes=  57 edges= 19 terms= 8 xrefs= 4  流程 v2：sync（2）三叉 → docker → apply 前置
v1p6cw     nodes=  51 edges= 26 terms= 4 xrefs= 2  流程 v2：sync（2′）apply 寫入段
v1p7       nodes=  61 edges= 24 terms= 6 xrefs= 2  流程 v2：upgrade ── A. Renovate 路徑
v1p7c      nodes=  66 edges= 32 terms= 5 xrefs= 3  流程 v2：upgrade ── B. 手動路徑（1）resolve → docker
v1p7ccc    nodes=  70 edges= 30 terms= 8 xrefs= 7  流程 v2：upgrade ── B. 手動路徑（1′）apply 前置
v1p7cc     nodes=  74 edges= 44 terms= 6 xrefs= 8  流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併
v1p7cccc   nodes=  59 edges= 26 terms= 6 xrefs= 2  流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入
v1p7b      nodes=  70 edges= 41 terms= 6 xrefs= 9  流程 v2：upgrade ── C. 逐檔判斷狀態機、衝突重入
v1p7bd     nodes=  76 edges= 37 terms= 7 xrefs= 2  流程 v2：upgrade ── D. 回退
v1p7bc     nodes=  64 edges= 28 terms= 6 xrefs= 5  流程 v2：upgrade ── E. 升引擎 (a)(b)
v1p7bca    nodes=  56 edges= 20 terms= 6 xrefs= 4  流程 v2：upgrade ── E. 升引擎 (a′) apply 改第一行 → 接手
v1p7bcc    nodes=  68 edges= 34 terms= 7 xrefs= 3  流程 v2：upgrade ── E(c) upgrade vendor_kit（1）
v1p7bcx    nodes=  49 edges= 17 terms= 4 xrefs= 4  流程 v2：upgrade ── E(c) upgrade vendor_kit（1′）
v1p7bccc   nodes=  51 edges= 16 terms= 4 xrefs= 8  流程 v2：upgrade ── E(c) upgrade vendor_kit（2）
v1p7bcce   nodes=  67 edges= 30 terms= 6 xrefs= 7  流程 v2：upgrade ── E(c) upgrade vendor_kit（2″）config.toml
v1p7bccd   nodes=  52 edges= 18 terms= 6 xrefs= 3  流程 v2：upgrade ── E(c) upgrade vendor_kit（2′）
v1p8       nodes=  70 edges= 35 terms= 7 xrefs= 0  流程 v2：dev <repo>
v1p8ccc    nodes=  65 edges= 29 terms= 7 xrefs= 1  流程 v2：dev vendor_kit
v1p8c      nodes=  71 edges= 33 terms= 8 xrefs= 2  流程 v2：undev <repo>（1）resolve → apply 前置
v1p8cx     nodes=  51 edges= 26 terms= 4 xrefs= 2  流程 v2：undev <repo>（2）寫入段
v1p8cc     nodes=  76 edges= 40 terms= 8 xrefs= 2  流程 v2：undev vendor_kit
v1p8b      nodes=  75 edges= 34 terms= 8 xrefs= 2  流程 v2：remove（1）resolve → apply 前置
v1p8bccc   nodes=  73 edges= 46 terms= 7 xrefs= 2  流程 v2：remove（2）寫入段
v1p8bc     nodes=  71 edges= 35 terms= 6 xrefs= 3  流程 v2：uninstall（1）resolve → apply 前置
v1p8bcc    nodes=  91 edges= 51 terms= 7 xrefs= 3  流程 v2：uninstall（2）寫入段
共 38 頁 → r15_b_out/
頁數 38；條目 338（warn 122、info 216）
| 規則 | warn | info |
|---|---|---|
| dangling | 0 | 0 |
| decision | 0 | 38 |
| endcolor | 0 | 6 |
| xref | 0 | 50 |
| term-diff | 0 | 0 |
| base | 0 | 0 |
| color | 0 | 0 |
| termcov | 122 | 37 |
| onething | 0 | 85 |
| event-name | 0 | 0 |
→ r15_b_out/lint.md, lint.json

diff --git a/disc_v1_b.py b/disc_v1_b.py
index 263512664407ca4bc04b3449a1d0add6e332ef95..b9e4e3be3dded92229cb5d9c5697157fc0488f4a
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -1784,7 +1784,7 @@
 b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
 b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
 b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
-b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
+b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
 b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
 b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
 b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
@@ -1800,14 +1800,18 @@
 b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
 b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
 b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
-b.D("se12tt", "s12t", "s12tt", "是", al=True)
+b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
 b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
 b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
 b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
 b.close()
-bypass(F, p7bcc, "se11y", "s11n", "s11v")
-sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
 _A = F.abs
+_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
+_bx, _gy, _nx = 30, F.rt["s11v"] - F.gap / 2, _tx + _tw / 2
+_tot = (_sx - _bx) + (_gy - (_sy + _sh / 2)) + (_nx - _bx)
+p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (0, 0.5), (0.5, 0),
+                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
+_A = F.abs
 def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
     sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
     hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
@@ -1932,15 +1936,16 @@
 b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
 b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
 b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
-b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
-b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
+b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
 b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
 b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
-b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
-b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
+b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
+b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
+b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
+b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
 b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
 b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
-b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
+b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
 b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
 b.close()
 lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
@@ -2204,10 +2209,11 @@
 b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
 b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
 b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
-b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
+b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
 b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
 b.close()
-foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
+pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
+foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
 addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
 
 # ================= P8bccc：remove（2）寫入段 =================

exec
/usr/bin/bash -lc "nl -ba disc_v1_b.py | sed -n '1775,1820p;1928,1955p;2198,2218p'" in <scratchpad>
 succeeded in 0ms:
  1775	b.box("s11px", U, 4, v2(R12), fl("1 + 6-24／6-31：現引擎拉不到／逾時"), 220)
  1776	b.box("s11x", U, 5, v2(R12), fl("1：本機覆寫的 image ID 不符（同 tag 重 build）"), 220)
  1777	b.box("s10a", U, 6, ENTRY, fl("來自「E. 升引擎 (a′)」頁：啟動器已改用新引擎 ref（已寫 launcher_start）"), 220)
  1778	b.box("s11r", L, 6, v2(W12), "否：docker run 該引擎 upgrade vendor_kit", 280)
  1779	b.box("s12a", E, 6, v2(SUB), "flock 專案目錄（60 秒）", 300, ax="l")
  1780	b.box("s12ax", G, 6, v2(R12), fl(E26X), 200)
  1781	b.box("s12sx", U, 7, v2(O12), fl("1 + 6-28：薄殼被改過，列差異不動（零寫入）"), 220)
  1782	b.box("s12s", E, 7, v2(D12), "薄殼 == 上次產物？", 210, ax="l")
  1783	b.box("s12sn", P, 7, v2(NOTE), fl("「上次產物」= 薄殼自描述首行的 sha256 與其餘內容相符（Q17；install 頁同）；任何寫入前檢查、恢復進度檔之前，不符 → 1 列差異、零寫入（v2.16-8）"), 360)
  1784	b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
  1785	b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
  1786	b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
  1787	b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
  1788	b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
  1789	b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
  1790	b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
  1791	b.box("s12d1", E, 13, v2(D12), fl("目標比現版舊（image LABEL 介面版／檔案版）？"), 210, ax="l")
  1792	b.box("s12dx", U, 14, v2(O12), fl("3 + 6-10：目標引擎無法無損讀現有檔（零寫入）"), 220)
  1793	b.box("s12d2", E, 14, v2(D12), fl("是 → 目標引擎能無損讀現有檔？"), 210, ax="l")
  1794	b.box("s12v", E, 15, v2(D12), "目標引擎 ref ≠ 現 ref？", 210, ax="l")
  1795	b.box("s12vz", E, 15, ENTRY, "否：續「E(c)（2）」頁：薄殼比對與重產", 140, ax="r")
  1796	b.box("s12jz", E, 16, ENTRY, "是：續「E(c)（1′）」頁：建進度檔 → 啟動器 pull 目標引擎 → 新引擎接手", 360)
  1797	b.H("se11", "s10", "s10l0"); b.D("se11l", "s10l", "s11a", al=True); b.D("se11q", "s11a", "s11n", al=True)
  1798	b.H("se11px", "s11p", "s11px", "失敗"); b.H("se11vx", "s11v", "s11x", "是"); b.D("se11vr", "s11v", "s11r", "否", al=True)
  1799	b.H("se11e", "s10a", "s11r")
  1800	b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
  1801	b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
  1802	b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
  1803	b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
  1804	b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
  1805	b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
  1806	b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
  1807	b.close()
  1808	_A = F.abs
  1809	_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
  1810	_bx, _gy, _nx = 30, F.rt["s11v"] - F.gap / 2, _tx + _tw / 2
  1811	_tot = (_sx - _bx) + (_gy - (_sy + _sh / 2)) + (_nx - _bx)
  1812	p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (0, 0.5), (0.5, 0),
  1813	                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
  1814	_A = F.abs
  1815	def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
  1816	    sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
  1817	    hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
  1818	_rb("se12jrv", "s12jr", "s12d1", ""); _rb("se12ttv", "s12tt", "s12d1", ""); _rb("se12fzv", "s12fz", "s12d1", ""); _rb("se12d1n", "s12d1", "s12v", "否")
  1819	foot(p7bcc, "p7bcc", F.y, _k7e("升引擎進度檔", "上次產物", "registry", "--protocol", "6-26") + [PULLX_T, ("6-28", "薄殼被改過（自描述首行 hash 與內容不符）→ 1，列差異不動、零寫入；在恢復進度檔之前檢查")], ALL - {"inv", "tree", "pend", "rule"} | {"entry"})
  1820	addpage("v1p7bcc", "流程 v2：upgrade ── E(c) upgrade vendor_kit（1）", p7bcc)
  1928	b = F.band("uE4", "E(c)（2′）（承「E(c)（2″）」頁）：gen/.stamp → tools.just → 刪進度檔（刪前已讀舊引擎 ref）→ config.toml 衝突 → 2；換引擎 → 1 + 6-2；同引擎修復 → 1 + 6-2（文案分開）；失敗 → 啟動器：第一行未變 → 1 印原因；已改 → 1 + 6-2b", v2=True)
  1929	b.box("s13z0", E, 0, ENTRY, "來自「E(c)（2″）」頁：薄殼五檔已重產、config.toml 已處理（已寫 launcher_start）", 360)
  1930	b.box("s13b", E, 1, v2(SUB), "寫 gen/.stamp（只記本引擎 ref）", 360)
  1931	b.box("s13bf", P, 1, F12, "gen/.stamp（不進 git）", 360)
  1932	b.box("s13c", E, 2, v2(SUB), "重生 gen/tools.just（用本引擎的規則；mod? 行）", 360)
  1933	b.box("s13cf", P, 2, F12, "gen/tools.just（不進 git；mod? 行）", 360)
  1934	b.box("s13d", E, 3, v2(SUB), fl("成功：刪進度檔 .tmp.upgrade.<id>.toml（最後一步，由新引擎刪；刪前已讀舊引擎 ref）"), 360)
  1935	b.box("s13df", P, 3, v2(F12), "－.vendor_kit/.tmp.upgrade.<id>.toml（E(a′)／E(c)(1′) 或 E(c)(2) 建的進度檔）", 360)
  1936	b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
  1937	b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
  1938	b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
  1939	b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
  1940	b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
  1941	b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
  1942	b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
  1943	b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
  1944	b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
  1945	b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
  1946	b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
  1947	b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
  1948	b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
  1949	b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
  1950	b.close()
  1951	lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
  1952	foot(p7bce, "p7bce", F.y, _k7e("升引擎進度檔", "6-2b", "gen/.stamp", "gen/tools") + [("接手判定（§3.4）", "啟動器在 apply 前後各 grep 一次正式 version.toml 的 vendor_kit 版本鎖定行；引擎失敗時：未變 → 1 印原因；已改（含變成非計畫值）→ 1 + 6-2b（進度檔保留，重跑 upgrade vendor_kit 續跑）"), ("6-2（升引擎完成）", "「已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」（結束 1，需人處理）；同引擎修復重產另有文案（版本未變）")], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
  1953	addpage("v1p7bccd", "流程 v2：upgrade ── E(c) upgrade vendor_kit（2′）", p7bce)
  1954	
  1955	# ================= P8：dev =================
  2198	b.box("m8", L, 13, v2(W12), fl("是：docker run … -v（含 vk-resolve）<引擎> apply remove <repo>（--dry-run 原樣轉發）"), 280)
  2199	b.box("m9a", E, 13, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
  2200	b.box("m9ax", G, 13, v2(R12), fl(E26X), 200)
  2201	b.box("m9x", U, 14, v2(O12), "1 + 6-12：指紋不同「請重跑」", 220)
  2202	b.box("m9b", E, 14, v2(D12), "重驗指紋：相同？", 340, ax="l")
  2203	b.box("m9cx", U, 15, v2(O12), "1：原 argv 與計畫不一致，請重跑", 220)
  2204	b.box("m9c", E, 15, v2(D12), ARGV_Q, 340, ax="l")
  2205	b.box("m7cx", U, 16, v2(O12), fl("1：印需改清單（CI 模式；請在本機執行後 commit 並 push）"), 220)
  2206	b.box("m7c", E, 16, v2(D12), "是 → CI 模式且需改任何進 git 的檔？", 340, ax="l")
  2207	b.box("m7y", U, 17, v2(G12), "0：只印清單（會刪什麼、會問什麼；不拉 image）", 220)
  2208	b.box("m7", E, 17, D12, "否 → --dry-run？", 240, ax="l")
  2209	b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
  2210	b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
  2211	b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
  2212	b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
  2213	b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
  2214	b.close()
  2215	pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
  2216	foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
  2217	addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
  2218	

diff --git a/disc_v1_b.py b/disc_v1_b.py
index 263512664407ca4bc04b3449a1d0add6e332ef95..b9e4e3be3dded92229cb5d9c5697157fc0488f4a
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -1784,7 +1784,7 @@
 b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
 b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
 b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
-b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
+b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
 b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
 b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
 b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
@@ -1800,14 +1800,18 @@
 b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
 b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
 b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
-b.D("se12tt", "s12t", "s12tt", "是", al=True)
+b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
 b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
 b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
 b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
 b.close()
-bypass(F, p7bcc, "se11y", "s11n", "s11v")
-sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
 _A = F.abs
+_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
+_bx, _gy, _nx = 30, F.rt["s11v"] - F.gap / 2, _tx + _tw / 2
+_tot = (_sx - _bx) + (_gy - (_sy + _sh / 2)) + (_nx - _bx)
+p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (0, 0.5), (0.5, 0),
+                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
+_A = F.abs
 def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
     sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
     hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
@@ -1932,15 +1936,16 @@
 b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
 b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
 b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
-b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
-b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
+b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
 b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
 b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
-b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
-b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
+b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
+b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
+b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
+b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
 b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
 b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
-b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
+b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
 b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
 b.close()
 lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
@@ -2204,10 +2209,11 @@
 b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
 b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
 b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
-b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
+b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
 b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
 b.close()
-foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
+pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
+foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
 addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
 
 # ================= P8bccc：remove（2）寫入段 =================

codex
已只修改 [disc_v1_b.py](<scratchpad>/disc_v1_b.py)。

- v1p8b
  - `me8ax`：移除線上「逾時」標籤，避免壓框；6-26 紅框仍完整表意。
  - `m3`：未直接重構流程，新增黃底待處理便條，並讓頁尾圖例包含 `pend`。

- v1p7bcc
  - `se12f`：「否」改由來源菱形直下，標籤靠近來源；`@<tag>` 是分支移至右車道。
  - `se11y`：「有」回繞改走頁面左側空白匯流排，不再緊貼或半包圍紫框。

- v1p7bccd
  - `s13h` 拆成白框 grep 動作與 `s13h2`「第一行未變？」菱形，與 v1p7bca 一致。

檢查結果：

- overflow：共 0 筆
- overlap：共 0 筆
- cross：共 0 筆
- self：共 0 筆
- jog：共 0 筆
- align：全頁「無」
- lint：非 termcov warn 全為 0
- 三頁高度：v1p7bcc 2340、v1p7bccd 1342、v1p8b 2322，皆 ≤ 2400。
diff --git a/disc_v1_b.py b/disc_v1_b.py
index 263512664407ca4bc04b3449a1d0add6e332ef95..b9e4e3be3dded92229cb5d9c5697157fc0488f4a
--- a/disc_v1_b.py
+++ b/disc_v1_b.py
@@ -1784,7 +1784,7 @@
 b.box("s12j", E, 8, v2(D12), "是 → 有未完成的 .tmp.upgrade 進度檔？", 210, ax="l")
 b.box("s12jr", E, 8, v2(SUB), fl("是：恢復：目標 = 進度檔記的目標引擎 ref"), 140, ax="r")
 b.box("s12t", E, 9, v2(D12), fl("否 → 指定 @<tag>？"), 210, ax="l")
-b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="l")
+b.box("s12tt", E, 10, v2(SUB), fl("是：目標 = @<tag>（不查 registry）"), 210, ax="r")
 b.box("s12f", E, 11, v2(D12), fl("否 → CI 模式？"), 210, ax="l")
 b.box("s12fz", E, 11, v2(SUB), fl("是：不查 registry；目標 = 現 ref"), 140, ax="r")
 b.box("s12u", E, 12, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 210, ax="l")
@@ -1800,14 +1800,18 @@
 b.H("se12", "s11r", "s12a"); b.H("se12ax", "s12a", "s12ax", "逾時"); b.D("se12s", "s12a", "s12s", "", 0.5, 0.5)
 b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12j", "s12s", "s12j", "是", al=True)
 b.H("se12jr", "s12j", "s12jr", "是"); b.D("se12t", "s12j", "s12t", "否", al=True)
-b.D("se12tt", "s12t", "s12tt", "是", al=True)
+b.D("se12tt", "s12t", "s12tt", "是", al=True); b.D("se12f", "s12t", "s12f", "否", al=True)
 b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12u", "s12f", "s12u", "否", al=True); b.D("se12ud", "s12u", "s12d1", al=True)
 b.D("se12d2", "s12d1", "s12d2", "是", al=True); b.H("se12dx", "s12d2", "s12dx", "否"); b.D("se12d2v", "s12d2", "s12v", "是", al=True)
 b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12jz", "s12v", "s12jz", "是", 0.5, 0.5)
 b.close()
-bypass(F, p7bcc, "se11y", "s11n", "s11v")
-sidebus(F, p7bcc, "se12f", "s12t", "s12f", "否", busx=610, tx=0.5, pos=-0.6, vert="below")
 _A = F.abs
+_sx, _sy, _sw, _sh = _A["s11n"]; _tx, _ty, _tw, _th = _A["s11v"]
+_bx, _gy, _nx = 30, F.rt["s11v"] - F.gap / 2, _tx + _tw / 2
+_tot = (_sx - _bx) + (_gy - (_sy + _sh / 2)) + (_nx - _bx)
+p7bcc.append(_edge("se11y", "s11n", "s11v", "有", (0, 0.5), (0.5, 0),
+                     [(_bx, _sy + _sh / 2), (_bx, _gy), (_nx, _gy)], 2 * (14 / _tot) - 1, "below"))
+_A = F.abs
 def _rb(eid, s_, t_, label):   # 右車道／格 → x=1010 右匯流排 → 目標菱形頂點；標籤放第一段水平段中央下方
     sx0, sy0, sw, sh = _A[s_]; tx0, ty0, tw, th = _A[t_]; gy = F.rt[t_] - F.gap / 2; nx = tx0 + tw / 2
     hseg_edge(p7bcc, eid, s_, t_, label, (1, 0.5), (0.5, 0), [(1010, sy0 + sh / 2), (1010, gy), (nx, gy)], _A)
@@ -1932,15 +1936,16 @@
 b.box("s13qe", L, 4, ENTRY, "來自「E(c)（2）」「E(c)（2″）」頁或本頁：任一步失敗（引擎結束非 0）", 280)
 b.box("s14c", G, 4, v2(O12), fl("2：config.toml 三方合併有衝突（留標記）＋ 已重產薄殼；解完衝突再跑原指令"), 200)
 b.box("s13cq", E, 4, v2(D12), "config.toml conflicts 非空？", 260, ax="l")
-b.box("s13xn", U, 5, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
-b.box("s13h", L, 5, v2(D12), fl("啟動器：apply 後 grep 第一行 == apply 前（未變）？"), 280)
+b.box("s13h", L, 5, v2(W12), fl("啟動器：apply 後 grep 正式 version.toml 的 vendor_kit 版本鎖定行"), 280)
 b.box("s14", G, 5, v2(O12), fl("1 + 6-2：已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令"), 200)
 b.box("s13k", E, 5, v2(D12), "否 → 本次換了引擎（進度檔的舊引擎 ref ≠ 本引擎；刪前已讀）？", 260, ax="l")
-b.box("s13x", L, 6, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
-b.box("s14b", E, 6, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
+b.box("s13xn", U, 6, v2(R12), fl("1：第一行未變、重產失敗（印原因；引擎未鎖定新版，不是 6-2b）"), 220)
+b.box("s13h2", L, 6, v2(D12), fl("第一行 == apply 前（未變）？"), 280)
+b.box("s13x", L, 7, v2(O12), fl("否 → 1 + 6-2b：第一行已改（== 計畫）或又變，但重產失敗；請排除錯誤後執行 just vendor_kit upgrade vendor_kit（進度檔保留）"), 280)
+b.box("s14b", E, 7, v2(O12), fl("否 → 1 + 6-2：同引擎修復重產薄殼（版本未變），請 commit .vendor_kit/ 並再跑原指令"), 220, ax="l")
 b.D("se18z", "s13z0", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
 b.D("se18cd", "s13c", "s13d"); b.H("se18df", "s13d", "s13df", "刪"); b.D("se18cq", "s13d", "s13cq", al=True)
-b.D("se19e", "s13qe", "s13h", al=True); b.H("se19xn", "s13h", "s13xn", "是"); b.D("se19x", "s13h", "s13x", "否", al=True)
+b.D("se19e", "s13qe", "s13h", al=True); b.D("se19h", "s13h", "s13h2", al=True); b.H("se19xn", "s13h2", "s13xn", "是"); b.D("se19x", "s13h2", "s13x", "否", al=True)
 b.H("se19c", "s13cq", "s14c", "是"); b.D("se19k", "s13cq", "s13k", "否", al=True); b.H("se19ky", "s13k", "s14", "是"); b.D("se19kn", "s13k", "s14b", "否", al=True)
 b.close()
 lbus(F, p7bce, ["s13b", "s13c", "s13d"], "s13qe", busx=610)
@@ -2204,10 +2209,11 @@
 b.box("m7z", E, 18, ENTRY, "續「remove（2）」頁：建進度檔 → 問 append 行 → 刪檔 → 刪進度檔", 400, ax="l")
 b.H("me1", "m0", "m0l0"); b.D("me1l", "m0l", "mpq", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)
 b.H("me5", "m4", "m5", "是"); b.D("me6", "m4", "m6", "否", 0.5, 0.5); b.D("me6b", "m6", "m6b"); b.D("me6c", "m6b", "m6c"); b.D("me6d", "m6c", "m6d"); b.D("me6d2", "m6d", "m6d2"); b.D("me7", "m6d2", "m8q0", "", 0.5, 0.5)
-b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax", "逾時"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
+b.H("me8e", "m8", "m9a"); b.H("me8ax", "m9a", "m9ax"); b.D("me8b", "m9a", "m9b", al=True); b.H("me8x", "m9b", "m9x", "否"); b.D("me9", "m9b", "m9c", "是", al=True); b.H("me9cx", "m9c", "m9cx", "否")
 b.D("me9c", "m9c", "m7c", "是", al=True); b.H("me9x", "m7c", "m7cx", "是"); b.D("me9d", "m7c", "m7", "否", al=True); b.H("me10", "m7", "m7y", "是"); b.D("me11", "m7", "m7z", "否", al=True)
 b.close()
-foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "pend", "rule", "note"} | {"entry"})
+pend(p8b, "待處理問題\n• m3：未接入時 resolve 應回 0 + apply|no，現圖仍由引擎判斷直接終止，啟動器三叉缺少 apply|no → 0 出路")
+foot(p8b, "p8b", F.y, _t8b("resolve／apply", "flock", "原 argv", "6-12", "6-27", "6-26", "6-30") + [LOGT[0]], ALL - {"inv", "tree", "rule", "note"} | {"entry"})
 addpage("v1p8b", "流程 v2：remove（1）resolve → apply 前置", p8b)
 
 # ================= P8bccc：remove（2）寫入段 =================

tokens used
85,593
已只修改 [disc_v1_b.py](<scratchpad>/disc_v1_b.py)。

- v1p8b
  - `me8ax`：移除線上「逾時」標籤，避免壓框；6-26 紅框仍完整表意。
  - `m3`：未直接重構流程，新增黃底待處理便條，並讓頁尾圖例包含 `pend`。

- v1p7bcc
  - `se12f`：「否」改由來源菱形直下，標籤靠近來源；`@<tag>` 是分支移至右車道。
  - `se11y`：「有」回繞改走頁面左側空白匯流排，不再緊貼或半包圍紫框。

- v1p7bccd
  - `s13h` 拆成白框 grep 動作與 `s13h2`「第一行未變？」菱形，與 v1p7bca 一致。

檢查結果：

- overflow：共 0 筆
- overlap：共 0 筆
- cross：共 0 筆
- self：共 0 筆
- jog：共 0 筆
- align：全頁「無」
- lint：非 termcov warn 全為 0
- 三頁高度：v1p7bcc 2340、v1p7bccd 1342、v1p8b 2322，皆 ≤ 2400。
