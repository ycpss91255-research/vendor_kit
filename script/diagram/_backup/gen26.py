import html

RED, GREEN, YELLOW, PURPLE, GREY, NEUTRAL = "#f8cecc", "#d5e8d4", "#FFF4C3", "#e1d5e7", "#CCCCCC", "#f5f5f5"

def SW(fill, size=18):
    return (f"swimlane;html=1;rounded=1;startSize=38;fontStyle=1;fontSize={size};container=1;"
            f"collapsible=1;recursiveResize=0;fillColor={fill};swimlaneFillColor=#ffffff;"
            f"strokeColor=#000000;strokeWidth=2;")
def LEAF(fill="#ffffff"):
    return f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor=light-dark(#000000,#9577A3);fontSize=14;strokeWidth=1;"
PURPLE_LEAF = f"rounded=1;whiteSpace=wrap;html=1;fillColor={PURPLE};strokeColor=#9673a6;fontSize=14;strokeWidth=2;"
def TEXT(size=12):
    return f"text;html=1;whiteSpace=wrap;align=center;verticalAlign=middle;fontSize={size};strokeColor=none;fillColor=none;"
TITLE = "text;html=1;fontSize=18;fontStyle=1;align=left;verticalAlign=middle;"
RHOMBUS = f"rhombus;whiteSpace=wrap;html=1;fillColor={YELLOW};strokeColor=#000000;strokeWidth=2;fontSize=14;"
def ELLIPSE(fill):
    return f"ellipse;whiteSpace=wrap;html=1;fillColor={fill};strokeColor=#000000;strokeWidth=2;fontSize=14;"
NOTE = "shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#ffffff;strokeColor=#999999;align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;fontSize=12;"
def LEGEND_BOX(fill):
    return (f"swimlane;html=1;rounded=1;startSize=34;fontStyle=1;fontSize=14;container=0;collapsible=0;"
            f"fillColor={fill};swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=2;")
EDGE = ("edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=default;"
        "strokeWidth=2;align=center;verticalAlign=bottom;spacingBottom=6;fontFamily=Helvetica;fontSize=12;"
        "fontColor=default;labelBorderColor=none;labelBackgroundColor=none;endArrow=block;endFill=1;")

def esc(s): return html.escape(s.replace("<", "&lt;").replace(">", "&gt;"), quote=True).replace("\n", "&lt;br&gt;")

def v(id, parent, style, value, x, y, w, h):
    return (f'<mxCell id="{id}" value="{esc(value)}" style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

def e(id, src, tgt, label="", exit=None, entry=None, dashed=False, both=False, vert=False, pos=None, offset=None):
    st = EDGE
    if exit:  st += f"exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;"
    if entry: st += f"entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
    if dashed: st += "dashed=1;"
    if both: st += "startArrow=block;startFill=1;"
    if vert == "left": st += "align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;"
    elif vert == "below": st += "verticalAlign=top;spacingTop=6;spacingBottom=0;"
    elif vert: st += "align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;"
    xa = "" if pos is None else f' x="{pos}"'
    inner = "" if offset is None else f'<mxPoint x="{offset[0]}" y="{offset[1]}" as="offset"/>'
    geo = f'<mxGeometry{xa} relative="1" as="geometry">{inner}</mxGeometry>'
    return (f'<mxCell id="{id}" value="{esc(label)}" style="{st}" edge="1" parent="1" source="{src}" target="{tgt}">'
            f'{geo}</mxCell>')

def page(id, name, cells, w=1600, h=1100):
    import re as _re
    body = "".join(cells)
    # 自動裁紙張：以頂層 vertex 的邊界 + 邊距 40
    mx = my = 0
    for m in _re.finditer(r'vertex="1" parent="1"><mxGeometry x="([\d.-]+)" y="([\d.-]+)" width="([\d.-]+)" height="([\d.-]+)"', body):
        x0, y0, w0, h0 = map(float, m.groups()); mx = max(mx, x0 + w0); my = max(my, y0 + h0)
    w, h = int(mx + 40), int(my + 40)
    return (f'<diagram id="{id}" name="{esc(name)}"><mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" '
            f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{w}" pageHeight="{h}" math="0" shadow="0">'
            f'<root><mxCell id="0" style="strokeWidth=2;"/><mxCell id="1" parent="0" style="strokeWidth=2;"/>{body}</root></mxGraphModel></diagram>')

FILE = LEAF() + "dashed=1;"
PURPLE_SW = (f"swimlane;html=1;rounded=1;startSize=38;fontStyle=1;fontSize=18;container=1;collapsible=1;"
             f"recursiveResize=0;fillColor={PURPLE};swimlaneFillColor=#ffffff;strokeColor=#9673a6;strokeWidth=2;")
LEGEND_ITEMS = {
 "red":    (LEGEND_BOX(RED),    "紅：我們要開發的模組", 200, 60, 0),
 "green":  (LEGEND_BOX(GREEN),  "綠：使用框架的 repo", 200, 60, 0),
 "yellow": (LEGEND_BOX(YELLOW), "黃：外部（使用者、外部系統）", 220, 60, 0),
 "purple": (f"swimlane;html=1;rounded=1;startSize=34;fontStyle=1;fontSize=14;container=0;collapsible=0;fillColor={PURPLE};swimlaneFillColor=#ffffff;strokeColor=#9673a6;strokeWidth=2;", "紫：image / container", 200, 60, 0),
 "neutral":(LEGEND_BOX(NEUTRAL), "淺灰：分組（無狀態意義）", 200, 60, 0),
 "note":   (NOTE,               "便條：補充說明", 130, 40, 10),
 "pimg":   (PURPLE_LEAF,        "紫：image / container", 180, 40, 10),
 "pstage": (PURPLE_LEAF,        "紫：image（每個 stage 都是一個 image）", 270, 40, 10),
 "white":  (LEAF(),             "白：最小單元", 120, 40, 10),
 "grey":   (LEAF(GREY),         "灰：主機上既有的軟體", 170, 40, 10),
 "file":   (FILE,               "虛線框：專案裡的檔案", 170, 40, 10),
}
def legend(prefix, x, y, keys, note):
    c = []; cx = x
    for i, k in enumerate(keys):
        st, t, w, h, dy = LEGEND_ITEMS[k]
        c.append(v(f"{prefix}_lg{i}", "1", st, t, cx, y + dy, w, h)); cx += w + 20
    c.append(v(f"{prefix}_lgt", "1", TEXT(12) + "align=left;", note, cx, y, 300, 60))
    return c
def legend_arch(prefix, x, y):
    return legend(prefix, x, y, ["red", "green", "yellow", "pimg", "white"], "實線 = 傳輸內容（線上文字 = 傳什麼）\n虛線 = 基底依賴，或只在特定情況發生")
TERM_K = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=12;fontStyle=1;align=left;spacingLeft=6;strokeWidth=1;"
TERM_V = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=12;align=left;spacingLeft=6;strokeWidth=1;"
def terms(prefix, x, y, rows, kw=170, vw=900, rh=30):
    c = [v(f"{prefix}_th", "1", TEXT(13) + "align=left;fontStyle=1;", "本頁名詞", x, y - 24, 200, 20)]
    for i, (k, d) in enumerate(rows):
        c.append(v(f"{prefix}_tk{i}", "1", TERM_K, k, x, y + i * rh, kw, rh))
        c.append(v(f"{prefix}_tv{i}", "1", TERM_V, d, x + kw, y + i * rh, vw, rh))
    return c

def legend_flow(prefix, x, y, purple=True, files=False, note=False, dashed=False, startend=True, err=True):
    c = []
    items = [(LEGEND_BOX(NEUTRAL), "淺灰：情境分組（無狀態意義）", 220, 60, 0), (RHOMBUS, "黃：判斷", 110, 60, 0)]
    if startend: items.append((ELLIPSE(GREEN), "綠：起點／終點", 130, 40, 10))
    if err: items.append((ELLIPSE(RED), "紅：錯誤終止", 130, 40, 10))
    if purple: items.append((PURPLE_LEAF, "紫：子命令（在容器內執行）", 200, 40, 10))
    items.append((LEAF(), "白：步驟", 88, 40, 10))
    if files: items.append((FILE, "虛線框：專案裡的檔案", 170, 40, 10))
    if note: items.append((NOTE, "便條：補充說明", 130, 40, 10))
    cx = x
    for i, (st, t, w, h, dy) in enumerate(items):
        c.append(v(f"{prefix}_lg{i}", "1", st, t, cx, y + dy, w, h)); cx += w + 20
    txt = "實線 = 執行順序（指向檔案時 = 寫入／讀取）" + ("\n虛線 = 之後才會發生" if dashed else "")
    c.append(v(f"{prefix}_lgt", "1", TEXT(12) + "align=left;", txt, cx, y, 300, 60))
    return c

# ================= Page 1: vendor_kit 架構圖 =================
p1 = [v("title", "1", TITLE, "vendor_kit 架構圖（模組 → 最小單元；線上文字 = 傳的資料）", 40, 20, 900, 30)]
VX, VY = 480, 140
p1.append(v("user", "1", SW(YELLOW), "使用者", 40, VY, 140, 860))
p1.append(v("u_cmd", "user", LEAF(), "指令", 26, 100, 88, 40))
p1.append(v("u_out", "user", LEAF(), "畫面", 26, 810, 88, 40))
p1.append(v("img", "1", PURPLE_SW, "image 內容", 200, 300, 180, 280))
p1.append(v("i_list", "img", LEAF(), "init.toml", 46, 121, 88, 40))
p1.append(v("i_dist", "img", LEAF(), "dist/（全部）", 46, 172, 88, 40))
p1.append(v("i_tpl", "img", LEAF(), "模板", 46, 223, 88, 40))
p1.append(v("vk", "1", PURPLE_SW, "vendor_kit（一個 container）", VX, VY, 570, 860))
p1.append(v("m_cli", "vk", SW(RED), "命令介面", 20, 50, 200, 140))
p1.append(v("cli_land", "m_cli", LEAF(), "install", 12, 45, 88, 40))
p1.append(v("cli_init", "m_cli", LEAF(), "init", 104, 45, 88, 40))
p1.append(v("cli_verify", "m_cli", LEAF(), "verify", 12, 92, 88, 40))
p1.append(v("cli_diff", "m_cli", LEAF(), "diff", 104, 92, 88, 40))
p1.append(v("m_list", "vk", SW(RED), "出貨內容讀取", 20, 250, 200, 170))
p1.append(v("ls_read", "m_list", LEAF(), "讀 dist/", 12, 45, 88, 40))
p1.append(v("ls_check", "m_list", LEAF(), "讀 init.toml", 104, 45, 88, 40))
p1.append(v("ls_class", "m_list", LEAF(), "檢查清單\n格式", 12, 92, 88, 40))
p1.append(v("m_tpl", "vk", SW(RED), "模板", 20, 480, 200, 130))
p1.append(v("tp_render", "m_tpl", LEAF(), "複製", 12, 45, 88, 40))
p1.append(v("tp_vars", "m_tpl", LEAF(), "渲染／帶入\n變數（待定）", 104, 45, 88, 40))
p1.append(v("m_diff", "vk", SW(RED), "差異比對", 20, 670, 200, 130))
p1.append(v("df_cmp", "m_diff", LEAF(), "比對", 12, 45, 88, 40))
p1.append(v("df_patch", "m_diff", LEAF(), "產生差異", 104, 45, 88, 40))
p1.append(v("m_write", "vk", SW(RED), "專案檔案存取", 300, 250, 200, 170))
p1.append(v("wr_copy", "m_write", LEAF(), "寫入", 12, 45, 88, 40))
p1.append(v("wr_read", "m_write", LEAF(), "讀回", 104, 45, 88, 40))
p1.append(v("wr_perm", "m_write", LEAF(), "權限設定", 12, 92, 88, 40))
p1.append(v("wr_atomic", "m_write", LEAF(), "整批替換", 104, 92, 88, 40))
p1.append(v("m_stamp", "vk", SW(RED, 16), "印記", 390, 480, 110, 130))
p1.append(v("st_hash", "m_stamp", LEAF(), "指紋計算", 11, 45, 88, 40))
p1.append(v("st_cmp", "m_stamp", LEAF(), "比對", 11, 85, 88, 40))
p1.append(v("m_report", "vk", SW(RED), "回報", 300, 670, 200, 130))
p1.append(v("rp_msg", "m_report", LEAF(), "訊息", 12, 45, 88, 40))
p1.append(v("rp_code", "m_report", LEAF(), "結束狀態", 104, 45, 88, 40))
p1.append(v("proj", "1", SW(GREEN), "專案 repo 的目錄", 1140, VY, 200, 860))
p1.append(v("p_stamp", "proj", LEAF(), ".<name>/\n.stamp", 56, 250, 88, 40))
p1.append(v("p_base", "proj", LEAF(), ".<name>/", 56, 306, 88, 40))
p1.append(v("p_user", "proj", LEAF(), "使用者檔案", 56, 376, 88, 40))
p1.append(e("a1", "u_cmd", "m_cli", "工具名、命令、參數", (1, 0.5), (0, 0.5)))
p1.append(e("a2", "m_cli", "m_list", "命令、參數（解析後）", (0.5, 1), (0.5, 0), vert=True))
p1.append(e("a3", "i_list", "m_list", "init 清單", (1, 0.5), (0, 0.3)))
p1.append(e("a4", "i_dist", "m_list", "dist 內容", (1, 0.5), (0, 0.6)))
p1.append(e("a5", "i_tpl", "m_list", "模板", (1, 0.5), (0, 0.9)))
p1.append(e("a6", "m_list", "m_write", "dist 全部", (1, 0.3), (0, 0.3)))
p1.append(e("a7", "m_list", "m_tpl", "init 清單\n＋模板", (0.5, 1), (0.5, 0), vert="left"))
p1.append(e("a8", "m_tpl", "m_write", "初始檔內容", (0.8, 0), (0.1, 1)))
p1.append(e("a9", "m_write", "m_stamp", "檔案內容、\n舊印記", (0.55, 1), (0.1818, 0), vert=True))
p1.append(e("a9b", "m_stamp", "m_write", "新指紋、\n比對結果", (0.9, 0), (0.945, 1), vert=True))
p1.append(e("a10", "m_write", "p_stamp", "印記檔", (1, 0.1176), (0, 0.5), both=True))
p1.append(e("a11", "m_write", "p_base", "dist 全部", (1, 0.4471), (0, 0.5), both=True))
p1.append(e("a12", "m_write", "p_user", "初始檔（init 時）", (1, 0.8), (0, 0.25)))
p1.append(e("a12b", "p_user", "m_write", "現有內容（diff 時）", (0, 0.76), (1, 0.92), vert="below"))
p1.append('<mxCell id="a13" value="使用者檔案" style="' + EDGE + 'exitX=0.3;exitY=1;exitDx=0;exitDy=0;entryX=0.9;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="m_write" target="m_diff"><mxGeometry x="0.55" relative="1" as="geometry"><Array as="points"><mxPoint x="840" y="780"/><mxPoint x="680" y="780"/></Array></mxGeometry></mxCell>')
p1.append(e("a14", "m_tpl", "m_diff", "新版模板", (0.5, 1), (0.5, 0), vert=True))
p1.append(e("a15", "m_stamp", "m_report", "檢查結果", (0.5, 1), (0.725, 0), vert=True))
p1.append(e("a16", "m_diff", "m_report", "差異", (1, 0.5), (0, 0.5)))
p1.append(e("a17", "m_report", "u_out", "訊息、結束狀態", (0.5, 1), (1, 0.5), pos=0.6))
p1 += legend("p1", 40, 1060, ["purple", "red", "green", "yellow", "white"], "實線 = 傳輸內容（線上文字 = 傳什麼）")
p1 += terms("p1", 40, 1170, [
 ("vendor_kit", "通用安裝工具；只以 container 形態執行（開發、使用皆是），主機不需安裝"),
 ("image / container", "image = 打包好的程式與檔案；container = image 執行起來的實例，跑完可刪"),
 ("<name>", "工具名，由專案的 .version 指定；安裝目錄就叫 .<name>/"),
 ("install / init / verify / diff", "四個子命令：安裝 dist 到 .<name>/／第一次建立使用者檔／檢查 .<name>/ 沒被改／升級後比對模板差異"),
 ("結束狀態", "程式結束時回報成功或失敗，啟動器據此決定要不要繼續執行"),
 ("模組", "vendor_kit 內部的功能分塊；同一個 container 裡，不是各自的 container"),
 ("dist/", "工具 repo 裡要出貨的那批檔案，全部寫進專案的 .<name>/"),
 ("init.toml", "工具 repo 提供的清單：init 時要複製到專案的初始檔有哪些、放哪（dist/ 本身每次 upgrade 都整包覆蓋）"),
 ("印記檔", ".<name>/.stamp：版本 + 每個檔案的指紋；verify 用它判斷有沒有被手改"),
 ("指紋", "由檔案內容算出的一串碼（sha256）；內容一改就不同"),
 ("模板", "工具 dist/ 裡給初始檔用的樣板（例如 Dockerfile 範本）；目前只複製；渲染 = 帶入變數（專案名等）產生實際檔案，待定"),
 ("repo", "一個 git 管理的專案資料夾；工具 repo = 工具的原始碼，專案 repo = 使用工具的專案"),
 (".version", "專案 repo 裡的版本清單（TOML）：一個工具一行，記工具名與 image 版本"),
 ("啟動器", "專案 repo 裡的 justfile：使用者打 just 指令時，它起 vendor_kit 容器並把結果告訴使用者"),
 ("Dockerfile", "打包 image 的食譜；專案自己的 Dockerfile 是由模板建立的使用者檔案"),
 ("upgrade（升級）", "改 .version 換新版本。兩條路：機器人開 PR（人 merge 後，下次 just 才換新）；或 just upgrade（改完立即 install → diff）"),
 ("TOML / just / PR", "設定檔格式（key = \"value\"）／主機上的指令跑器，使用者打 just <指令>／GitHub 上的合併請求，merge = 接受修改"),
])

# ================= Page 2: 框架定義 =================
p1b = [v("title", "1", TITLE, "框架定義：兩種 repo 各自必須有什麼，以及工具怎麼送到專案", 40, 20, 1000, 30)]
p1b.append(v("tool", "1", SW(GREEN), "工具 repo（每個要出貨的工具一個）", 40, 210, 320, 260))
p1b.append(v("t_t", "tool", TEXT(11), "工具名 = <name>；下面四樣是接上 vendor_kit 的必要條件", 10, 40, 300, 30))
p1b.append(v("t_dist", "tool", LEAF(), "dist/\n（要出貨的全部）", 20, 80, 135, 50))
p1b.append(v("t_init", "tool", LEAF(), "init.toml\n（初始檔清單）", 165, 80, 135, 50))
p1b.append(v("t_df", "tool", LEAF(), "Dockerfile.dist\n（FROM vendor_kit）", 20, 145, 135, 50))
p1b.append(v("t_ci", "tool", LEAF(), "CI：打 tag →\n建置＋上傳 image", 165, 145, 135, 50))
p1b.append(v("t_n", "tool", TEXT(11), "其他內容（doc、test、CI 腳本…）不在 dist/ 裡，不會出貨", 10, 205, 300, 40))
p1b.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 490, 320, 130))
p1b.append(v("vk_prog", "vk", LEAF(), "vendor_kit 程式", 20, 50, 135, 40))
p1b.append(v("vk_df", "vk", LEAF(), "Dockerfile", 165, 50, 135, 40))
p1b.append(v("tool2", "1", SW(GREEN), "另一個工具 repo（<name2>，同型）", 40, 640, 320, 60))
p1b.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 420, 80, 260, 640))
p1b.append(v("g_t", "ghcr", TEXT(11), "tag 不覆蓋；被引用的版本不刪；\nimage 附註：版本、來源 repo 與 commit", 10, 40, 240, 40))
p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 280, 200, 40))
p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 460, 200, 40))
p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 570, 200, 40))
p1b.append(v("proj", "1", SW(GREEN), "專案 repo（使用工具的專案）", 740, 80, 770, 640))
p1b.append(v("p_t", "proj", TEXT(11), "必要條件只有 .version 與 justfile；.version 可列多個工具，各自安裝到自己的 .<name>/", 10, 40, 750, 30))
p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器（進 git）", 20, 80, 300, 125))
p1b.append(v("pa_t", "pa", TEXT(11) + "align=left;", ".version 一行 = 一個工具 = 一個 .<name>/", 12, 42, 276, 24))
p1b.append(v("p_ver", "pa", LEAF(), ".version", 12, 72, 90, 40))
p1b.append(v("p_just", "pa", LEAF(), "justfile", 200, 72, 80, 40))
p1b.append(v("p_eng", "proj", PURPLE_LEAF, "安裝容器（<name>-dist:vX）", 20, 270, 300, 60))
p1b.append(v("p_eng_t", "proj", TEXT(11) + "align=left;", "以使用者身分執行，跑完即刪", 20, 332, 200, 20))
p1b.append(v("pb", "proj", SW(NEUTRAL), "使用者檔案（進 git）", 300, 380, 220, 125))
p1b.append(v("p_u1", "pb", LEAF(), "Dockerfile\n（專案自己的）", 12, 45, 100, 50))
p1b.append(v("p_u2", "pb", LEAF(), "設定檔…", 122, 45, 86, 50))
p1b.append(v("pb_t", "pb", TEXT(11), "init 建立；之後由使用者維護", 12, 98, 200, 18))
p1b.append(v("pc", "proj", SW(NEUTRAL), ".<name>/（不進 git）", 540, 380, 220, 125))
p1b.append(v("p_c1", "pc", LEAF(), "dist 全部", 12, 45, 90, 40))
p1b.append(v("p_c2", "pc", LEAF(), "印記檔", 118, 45, 90, 40))
p1b.append(v("pc_t", "pc", TEXT(11), "每次 upgrade 整批覆蓋\n印記檔 = 版本 + 每檔指紋", 6, 88, 210, 32))
p1b.append(v("pc2", "proj", SW(NEUTRAL, 14), ".<name2>/（另一個工具）", 540, 565, 220, 50))
p1b.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1600, 80, 160, 640))
p1b.append(v("h_t", "host", TEXT(11), "需預先安裝這三個", 10, 40, 140, 20))
p1b.append(v("h_just", "host", LEAF(GREY), "just\n（執行 justfile）", 20, 70, 120, 50))
p1b.append(v("h_git", "host", LEAF(GREY), "git\n（管理專案 repo）", 20, 130, 120, 50))
p1b.append(v("h_docker", "host", LEAF(GREY), "Docker\n（跑所有容器）", 20, 418, 120, 50))
p1b.append(e("f1", "t_ci", "g_tool", "image", (1, 0.5), (0, 0.5), pos=-0.5))
p1b.append(e("f2", "tool2", "g_tool2", "image", (1, 0.5), (0, 0.5), pos=-0.5))
p1b.append(e("f3", "vk_df", "g_vk", "image", (1, 0.5), (0, 0.5), pos=0))
p1b.append(e("f4", "g_vk", "g_tool", "基底 image", (0.5, 0), (0.5, 1), dashed=True, vert=True))
p1b.append(e("f5", "g_vk", "g_tool2", "基底 image", (0.5, 1), (0.5, 0), dashed=True, vert=True))
p1b.append(e("f6", "g_tool", "p_eng", "image", (1, 0.5), (0, 0.5)))
p1b.append(e("f12", "g_tool2", "pc2", "dist、印記檔（同樣經安裝容器寫入）", (1, 0.5), (0, 0.5)))
p1b.append(e("f7", "p_ver", "p_just", "工具名、版本", (1, 0.5), (0, 0.5)))
p1b.append(e("f8", "p_just", "p_eng", "工具名、版本、使用者身分、專案路徑", (0.5, 1), (0.8, 0), vert=True))
p1b.append(e("f9", "p_eng", "pc", "寫入 dist、印記檔", (1, 0.3), (0.5, 0)))
p1b.append(e("f10", "p_eng", "pb", "初始檔（只在 init 時）", (1, 0.7), (0.5, 0)))
p1b.append(e("f11", "pc", "h_docker", "compose 指令", (1, 0.5), (0, 0.5), offset=(0, -4)))
p1b += legend("p1b", 40, 730, ["red", "green", "yellow", "pimg", "neutral", "white", "grey"], "實線 = 傳輸內容\n虛線箭頭 = 基底 image → 以它為底的 image")
p1b += terms("p1b", 40, 840, [
 ("工具 repo", "任何想透過 vendor_kit 出貨的工具的原始碼 repo；必須有 dist/、init.toml、Dockerfile.dist、CI"),
 ("專案 repo", "使用工具的專案；必須有 .version、justfile；可同時用多個工具"),
 ("vendor_kit repo", "我們要開發的：安裝工具的原始碼，打包成 vendor_kit image"),
 ("image / 容器", "image = 打包好的程式與檔案；容器 = image 執行起來的實例，跑完可刪"),
 ("GHCR", "GitHub 提供的 image 倉庫；每個工具一個 <name>-dist image，以 vendor_kit image 為底"),
 (".version", "專案裡的 TOML 檔，一個工具一行 name = \"image:tag@sha256:…\"；name 決定安裝目錄 .<name>/"),
 ("CI", "放在 GitHub 上的自動化流程：打 tag 時建置 image 並上傳 GHCR"),
 ("建置 / 上傳", "建置 = 照 Dockerfile 做出 image（docker build）；上傳 = 把 image 放到 GHCR（docker push）"),
 ("upgrade（升級）", "改 .version 換新版本。兩條路：機器人提出合併請求（PR，人 merge 後下次 just 才換新）；或 just upgrade（改完立即 install → diff）"),
 ("PR / merge", "GitHub 上的合併請求／接受它，修改才進 repo"),
 ("just / justfile", "just 是主機上的指令跑器；justfile 是專案裡給它讀的指令清單，也就是啟動器"),
 ("印記檔", ".<name>/.stamp：安裝時寫下「版本 + 每檔指紋」，之後用來檢查有沒有被手改"),
 ("tag / digest", "image 的版本名稱（v0.43.0）／內容指紋（sha256:…）；.version 兩者都記，工具只認 digest"),
 ("Dockerfile / Dockerfile.dist / FROM", "Dockerfile = 打包 image 的食譜；Dockerfile.dist = 工具 repo 出貨用的食譜；FROM = 食譜第一行，指定以哪個 image 為底"),
 ("commit", "git 的一次版本紀錄"),
 ("compose 指令", "docker compose：依設定檔啟動專案容器的指令"),
 ("TOML", "一種設定檔格式（key = \"value\"）；.version、init.toml 都用它"),
])

# ================= Page 3: 流程：使用者指令 =================
p2 = [v("title", "1", TITLE, "流程：使用者下的每個指令 → 啟動器叫哪個子命令 → 專案裡發生什麼", 40, 20, 1200, 30)]
for name, x, w in [("使用者", 40, 300), ("啟動器（justfile，在主機）", 380, 360), ("安裝容器（vendor_kit）", 800, 360), ("專案目錄", 1240, 380)]:
    p2.append(v(f"h_{x}", "1", "text;html=1;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;", name, x, 60, w, 24))
def band(bid, title, y, h):
    p2.append(v(bid, "1", SW(NEUTRAL), title, 20, y, 1620, h))
# ---- A 第一次 ----
band("bA", "第一次接上工具：just init", 100, 280)
p2.append(v("a_u", "bA", ELLIPSE(GREEN), "just init", 60, 70, 180, 50))
p2.append(v("a_l1", "bA", LEAF(), "讀 .version\n（一行一個工具，逐行做）", 380, 75, 140, 40).replace("fontSize=14", "fontSize=12"))
p2.append(v("a_l2", "bA", LEAF(), ".<name>/ 不存在\n→ 要安裝", 560, 70, 160, 50))
p2.append(v("a_c1", "bA", PURPLE_LEAF, "install\ndist/ 全部 → .<name>/\n並寫印記（.<name>/.stamp：裝的 image + 每檔指紋）", 800, 60, 340, 70).replace("fontSize=14", "fontSize=13"))
p2.append(v("a_p1", "bA", FILE, ".<name>/（新）", 1240, 75, 200, 40))
p2.append(v("a_c2", "bA", PURPLE_LEAF, "init\n照 init.toml 複製初始檔（已存在則跳過）", 800, 165, 340, 60))
p2.append(v("a_p2", "bA", FILE, "Dockerfile / entrypoint / hooks…\n（新；之後由你維護）", 1240, 165, 200, 60))
p2.append(e("ae1", "a_u", "a_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae2", "a_l1", "a_l2", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae3", "a_l2", "a_c1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae4", "a_c1", "a_p1", "寫入", (1, 0.5), (0, 0.5)))
p2.append(e("ae5", "a_c1", "a_c2", "", (0.5, 1), (0.5, 0)))
p2.append(e("ae6", "a_c2", "a_p2", "建立", (1, 0.5), (0, 0.5)))
# ---- B 日常 ----
band("bB", "日常：just build（建置）；run（啟動）／exec（進入）／stop（停止）流程相同", 410, 390)
p2.append(v("b_u", "bB", ELLIPSE(GREEN), "just build", 60, 70, 180, 50))
p2.append(v("b_l1", "bB", LEAF(), "讀 .version\n（一行一個工具，逐行做）", 360, 75, 140, 40).replace("fontSize=14", "fontSize=12"))
p2.append(v("b_note", "bB", NOTE, ".version 一行 = 一個工具：\n<name> = \"…-dist:vX@sha256:…\"\n等號左邊 = 工具名 → 目錄 .<name>/\n等號右邊 = image → 跟 .<name>/.stamp 第一行比\n每一行各跑一次右邊的流程\n「否則」= 不同、尚未安裝、或印記讀不到", 40, 130, 290, 112))
p2.append(v("b_l2", "bB", RHOMBUS, ".<name>/.stamp 第一行\n= .version 那行的 image？", 530, 55, 220, 80).replace("fontSize=14", "fontSize=12"))
p2.append(v("b_c0", "bB", PURPLE_LEAF, "install\n換成 .version 指定的版本", 800, 65, 340, 60))
p2.append(v("b_l1n", "bB", TEXT(11), "（image 不在本機時，Docker 會先下載）", 340, 118, 220, 24))
p2.append(v("b_p0", "bB", FILE, ".<name>/（換新）", 1240, 75, 200, 40))
p2.append(v("b_c1", "bB", PURPLE_LEAF, "verify\n.<name>/ 每檔指紋是否仍等於印記", 800, 170, 340, 60))
p2.append(v("b_l3", "bB", LEAF(), "執行 .<name>/ 內的 build（建置）腳本", 380, 290, 340, 50))
p2.append(v("b_p1", "bB", LEAF(), "docker compose build", 1240, 295, 200, 40))
p2.append(v("b_err", "bB", ELLIPSE(RED), "中止：.<name>/ 被改過\n刪除 .<name>/ 再 build 即自動重裝", 40, 285, 260, 60))
p2.append(e("be1", "b_u", "b_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("be2", "b_l1", "b_l2", "", (1, 0.5), (0, 0.5)))
p2.append(e("be3", "b_l2", "b_c0", "否則", (1, 0.5), (0, 0.5)))
p2.append(e("be4", "b_l2", "b_c1", "相同", (0.5, 1), (0, 0.5), vert=True, pos=-0.7))
p2.append(e("be5", "b_c0", "b_p0", "覆蓋", (1, 0.5), (0, 0.5)))
p2.append('<mxCell id="be6" value="用換新後的目錄" style="' + EDGE + 'align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.76;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="bB" source="b_p0" target="b_l3"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="1340" y="270"/><mxPoint x="638" y="270"/></Array></mxGeometry></mxCell>'.replace('<mxGeometry relative="1" as="geometry">', '<mxGeometry x="-0.8" relative="1" as="geometry">'))
p2.append('<mxCell id="be7" value="通過" style="' + EDGE + 'align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;exitX=0.15;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="bB" source="b_c1" target="b_l3"><mxGeometry x="-0.9" relative="1" as="geometry"><Array as="points"><mxPoint x="851" y="250"/><mxPoint x="550" y="250"/></Array></mxGeometry></mxCell>')
p2.append('<mxCell id="be8" value="失敗" style="' + EDGE + 'align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;exitX=0;exitY=0.9;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="bB" source="b_c1" target="b_err"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="340" y="224"/><mxPoint x="340" y="315"/></Array></mxGeometry></mxCell>'.replace('<mxGeometry relative="1" as="geometry">', '<mxGeometry x="0.7" relative="1" as="geometry">'))
p2.append(e("be9", "b_l3", "b_p1", "", (1, 0.5), (0, 0.5)))
# ---- C 升級 ----
band("bC", "升級：Renovate 開的 PR 被 merge", 830, 300)
p2.append(v("c_u", "bC", ELLIPSE(GREEN), "merge PR\n（.version 改了）", 60, 60, 180, 60))
p2.append(v("c_l1", "bC", LEAF(), "下次 just build 走上面\n「否則」分支 → install 新版", 380, 65, 340, 50))
p2.append(v("c_p1", "bC", FILE, ".<name>/（新版）", 1240, 70, 200, 40))
p2.append(v("c_u2", "bC", ELLIPSE(GREEN), "just diff", 60, 160, 180, 50))
p2.append(v("c_c2", "bC", PURPLE_LEAF, "diff\nimage 內的新版模板 vs 你的初始檔", 800, 155, 340, 60))
p2.append(v("c_p2", "bC", FILE, "Dockerfile 等（你的）", 1240, 165, 200, 40))
p2.append(v("c_u3", "bC", ELLIPSE(GREEN), "看差異，自己決定\n要不要改", 60, 230, 180, 55))
p2.append(e("ce1", "c_u", "c_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ce2", "c_l1", "c_p1", "下次 build 時才發生", (1, 0.5), (0, 0.5), dashed=True))
p2.append(e("ce3", "c_u2", "c_c2", "", (1, 0.5), (0, 0.5)))
p2.append(e("ce4", "c_p2", "c_c2", "讀", (0, 0.5), (1, 0.5)))
p2.append('<mxCell id="ce5" value="印出差異" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="bC" source="c_c2" target="c_u3"><mxGeometry x="0.4" relative="1" as="geometry"><Array as="points"><mxPoint x="970" y="258"/><mxPoint x="300" y="258"/></Array></mxGeometry></mxCell>')
p2.append(v("p2n", "1", NOTE, "紫框 = 子命令：install（第一次、版本改變時）、init（只有第一次）、verify（已安裝且版本一致時）、diff（升級後由使用者呼叫）。\n沒有 Renovate 時用 just upgrade 手動：改 .version → 立即 install → diff（細節待議）。", 20, 1150, 1620, 50))
p2 += legend_flow("p2", 40, 1220, files=True, note=True, dashed=True)
p2 += terms("p2", 40, 1330, [
 ("啟動器", "專案裡的 justfile：使用者打 just 指令時，它讀 .version、起安裝容器、再執行工具的腳本"),
 ("印記", ".<name>/.stamp：install 寫下的「第一行 = 裝的 image，之後每行 = 一個檔的指紋」；日常每次 just 都拿它比對"),
 ("Renovate", "GitHub 上的機器人：GHCR 有新版就自動開 PR 改 .version；沒有它時用 just upgrade 手動"),
 ("docker compose", "工具腳本最後真正拿來建置／啟動／進入／停止專案容器的指令"),
 ("build / run / exec / stop", "四個日常指令：建置 image／啟動容器／進入容器／停止容器；都先經過同樣的檢查再執行 .<name>/ 內的腳本"),
 (".version", "專案裡的版本清單（TOML）：一個工具一行 <name> = \"image\"；<name> 決定安裝目錄 .<name>/ 和要比對哪個印記"),
 ("install / init / verify / diff", "四個子命令：安裝 dist 到 .<name>/ 並寫印記／第一次建立初始檔／檢查 .<name>/ 沒被手改／升級後比對模板差異"),
 ("sha256 / 容器", "image 的內容指紋（跟在 @ 後面，鎖定內容）／容器 = image 執行起來的實例，跑完可刪"),
 ("PR / merge", "GitHub 上的合併請求／接受它"),
 ("GHCR", "GitHub 的 image 倉庫"),
 ("dist / image / 模板", "dist = 工具要出貨的檔案；image = 打包好可執行的檔案包；模板 = dist 裡給初始檔用的樣板"),
 ("just", "主機上的指令跑器；使用者打 just <指令>，它照 justfile 執行"),
 ("init.toml", "工具提供的清單：init 時要複製到專案的初始檔有哪些、放哪"),
 ("entrypoint / hooks", "初始檔的例子：容器啟動腳本／各指令前後可掛的自訂腳本"),
 ("<name> / 指紋", "<name> = .version 裡的工具名，安裝目錄就叫 .<name>/；指紋 = 由檔案內容算出的識別碼，內容一改就不同"),
 ("vendor_kit / Dockerfile / TOML", "安裝工具本身（在容器內跑）／打包 image 的食譜、也是專案自己的 image 食譜／設定檔格式"),
 ("just upgrade", "手動升級指令：改 .version → 立即 install → diff（細節待議）"),
])

# ================= Page 3: 流程：版本生命週期 =================
p3 = [v("title", "1", TITLE, "流程：版本生命週期", 40, 20, 700, 30)]
p3.append(v("up", "1", SW(NEUTRAL), "升級", 20, 60, 440, 560))
p3.append(v("c5", "up", LEAF(), "指定新版本（改 .version；手動或機器人 PR）", 20, 50, 380, 40))
p3.append(v("c6", "up", LEAF(), "執行 just → 啟動器自動 install 新版", 20, 110, 380, 40))
p3.append(v("c7", "up", LEAF(), ".<name>/ 整批換成新版（含模板）", 20, 170, 380, 50))
p3.append(v("c8", "up", RHOMBUS, "使用者執行 just diff：\n新版模板 vs 你的初始檔有差異？", 70, 240, 280, 100))
p3.append(v("c9", "up", LEAF(), "顯示差異，使用者自行決定是否修改\n（工具不碰使用者檔案）", 20, 370, 380, 60))
p3.append(v("c10", "up", LEAF(), "提交變更（有改才提交）\n（just upgrade 那條路連 .version 一起提交；機器人 PR 那條路 .version 已在 merge 時提交）", 20, 455, 380, 56).replace("fontSize=14", "fontSize=12"))
p3.append(e("c11", "c5", "c6"))
p3.append(e("c12", "c6", "c7"))
p3.append(e("c13", "c7", "c8"))
p3.append(e("c14", "c8", "c9", "有", (0.5, 1), (0.5, 0), vert=True))
p3.append('<mxCell id="c14b" value="無" style="' + EDGE + 'align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="c8" target="c10"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="440" y="350"/><mxPoint x="440" y="540"/></Array></mxGeometry></mxCell>')
p3.append(e("c15", "c9", "c10"))
p3.append(v("c16", "1", NOTE, "升級程式在新版 image 裡，不在專案的舊腳本裡，\n所以不會有「舊工具幫自己升級」的問題。", 490, 100, 290, 60))
p3.append(v("rb", "1", SW(NEUTRAL), "回退", 490, 230, 290, 190))
p3.append(v("c18", "rb", LEAF(), "把 .version 改回舊版本", 20, 50, 260, 40))
p3.append(v("c19", "rb", LEAF(), "執行 just → 用舊版 image 重新安裝\n（使用者檔案不會自動回復）", 20, 110, 260, 50))
p3.append(e("c20", "c18", "c19"))
p3.append(v("bug", "1", SW(NEUTRAL), "追查問題", 800, 60, 420, 420))
p3.append(v("c22", "bug", LEAF(), "出問題的專案 commit", 20, 50, 380, 50))
p3.append(v("c23", "bug", LEAF(), "該 commit 的 .version → 用的 digest", 20, 130, 380, 50))
p3.append(v("c24", "bug", LEAF(), "image 記錄的來源 commit（工具 repo）", 20, 210, 380, 50))
p3.append(v("c25", "bug", LEAF(), "工具 repo 該 commit 的原始碼", 20, 290, 380, 50))
p3.append(v("c29", "bug", NOTE, "對 .version 做 git bisect 即可找出出問題的升級", 20, 355, 380, 50))
p3.append(e("c26", "c22", "c23"))
p3.append(e("c27", "c23", "c24"))
p3.append(e("c28", "c24", "c25"))
p3.append(v("dev", "1", SW(NEUTRAL), "本機開發模式（改工具本身時；待設計）", 800, 510, 420, 150))
p3.append(v("c31", "dev", LEAF(), "候選做法：.version 暫時指向本機的工具原始碼（而非 GHCR image）\n改工具不必每次發佈 image 就能在專案裡測", 20, 50, 380, 80))
p3 += legend_flow("p3", 40, 720, purple=False, startend=False, err=False, note=True)
p3 += terms("p3", 40, 830, [
 ("模板 / dist", "dist = 工具要出貨的檔案，整批放進 .<name>/；模板 = dist 裡給初始檔用的樣板，diff 拿新版模板跟你的檔案比"),
 ("commit", "git 的一次版本紀錄"),
 ("PR", "GitHub 上的合併請求；merge 就是接受這次修改"),
 ("git bisect", "git 的二分搜尋：在 .version 的修改紀錄中找出哪次升級引入問題"),
 ("image 附註", "image 上的標籤（label）：記錄它來自工具 repo 的哪個 commit、什麼版本"),
 ("digest", "image 的內容指紋（sha256:…）；同一個 digest 永遠是同一份內容"),
 (".version / 啟動器", "專案裡記工具版本的檔／專案裡的 justfile，打 just 時它負責安裝與執行"),
 ("install / diff / init.toml", "安裝子命令／升級後比對子命令／init 要建立哪些檔的清單"),
 ("工具 repo / GHCR / image", "工具的原始碼 repo／GitHub 的 image 倉庫／打包好可執行的檔案包"),
 ("<name> / just", "<name> = .version 裡的工具名，安裝目錄就叫 .<name>/；just = 主機上的指令跑器，使用者打 just <指令>"),
])

# ================= Page 5: 流程：安裝工具 =================
p4 = [v("title", "1", TITLE, "流程：vendor_kit 內部——四個子命令（install 是核心，其餘三個圍繞它）；全部在容器內執行", 40, 20, 1000, 30)]
# land
p4.append(v("install", "1", SW(NEUTRAL), "install（核心：把 dist/ 放進 .<name>/）", 20, 60, 380, 560))
p4.append(v("l0", "install", ELLIPSE(GREEN), "開始 install", 110, 50, 160, 50))
p4.append(v("l1", "install", LEAF(), "讀取 image 內的 dist/", 90, 130, 200, 40))
p4.append(v("l2", "install", LEAF(), "複製 dist/ 全部到暫存目錄", 90, 200, 200, 40))
p4.append(v("l3", "install", LEAF(), "寫入印記（版本 + 每檔指紋）", 90, 270, 200, 40))
p4.append(v("l4", "install", LEAF(), "暫存目錄換名為 .<name>/\n（整批覆蓋、原子替換）", 90, 340, 200, 50))
p4.append(v("l5", "install", ELLIPSE(GREEN), "成功結束", 110, 430, 160, 40))
p4.append(v("ln", "install", NOTE, "任一步失敗即中止，舊 .<name>/ 不動；\n啟動器不會執行 .<name>/ 內的腳本", 60, 490, 260, 50))
p4.append(e("le0", "l0", "l1")); p4.append(e("le1", "l1", "l2")); p4.append(e("le2", "l2", "l3")); p4.append(e("le3", "l3", "l4")); p4.append(e("le4", "l4", "l5"))
# init
p4.append(v("init", "1", SW(NEUTRAL), "init（第一次：建立使用者檔）", 440, 60, 480, 720))
p4.append(v("i0", "init", ELLIPSE(GREEN), "開始 init", 160, 50, 160, 50))
p4.append(v("i1", "init", LEAF(), "讀 init.toml", 140, 130, 200, 40))
p4.append(v("i2", "init", RHOMBUS, "還有項目？", 150, 200, 180, 80))
p4.append(v("i3", "init", LEAF(), "取下一項\n（image 內由 src 指定的檔 → 專案內的 dest）", 80, 312, 320, 56))
p4.append(v("i4", "init", RHOMBUS, "dest 已存在？", 150, 390, 180, 80))
p4.append(v("i5", "init", LEAF(), "略過（保留使用者版本）", 40, 510, 180, 40))
p4.append(v("i6", "init", LEAF(), "從 dist/ 複製建立", 260, 510, 180, 40))
p4.append(v("i8", "init", LEAF(), "繼續下一項", 140, 590, 200, 36))
p4.append(v("i7", "init", ELLIPSE(GREEN), "成功結束", 160, 660, 160, 40))
p4.append(e("ie0", "i0", "i1")); p4.append(e("ie1", "i1", "i2"))
p4.append(e("ie2", "i2", "i3", "有", (0.5, 1), (0.5, 0), vert=True))
p4.append(e("ie3", "i3", "i4"))
p4.append(e("ie4", "i4", "i5", "已有", (0, 0.5), (0.5, 0), vert=True))
p4.append(e("ie5", "i4", "i6", "沒有", (1, 0.5), (0.5, 0), vert=True))
p4.append('<mxCell id="ie6" value="沒有了" style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i2" target="i7"><mxGeometry x="-0.85" relative="1" as="geometry"><Array as="points"><mxPoint x="460" y="240"/><mxPoint x="460" y="680"/></Array></mxGeometry></mxCell>')
p4.append(e("ib1", "i5", "i8", "", (0.5, 1), (0.25, 0)))
p4.append(e("ib2", "i6", "i8", "", (0.5, 1), (0.75, 0)))
p4.append('<mxCell id="ib3" value="" style="' + EDGE + 'exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i8" target="i2"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="15" y="608"/><mxPoint x="15" y="240"/></Array></mxGeometry></mxCell>')
# verify
p4.append(v("verify", "1", SW(NEUTRAL), "verify（檢查 install 的產物沒被改）", 960, 60, 440, 480))
p4.append(v("v0", "verify", ELLIPSE(GREEN), "開始 verify", 140, 50, 160, 50))
p4.append(v("v1", "verify", LEAF(), "讀取印記", 120, 130, 200, 40))
p4.append(v("v2", "verify", LEAF(), "重新計算 .<name>/ 每檔指紋", 120, 200, 200, 40))
p4.append(v("v3", "verify", RHOMBUS, "全部相符？", 130, 270, 180, 80))
p4.append(v("v4", "verify", ELLIPSE(GREEN), "通過", 20, 390, 160, 50))
p4.append(v("v5", "verify", ELLIPSE(RED), "失敗：列出被改的檔案", 240, 390, 180, 50))
p4.append(e("ve0", "v0", "v1")); p4.append(e("ve1", "v1", "v2")); p4.append(e("ve2", "v2", "v3"))
p4.append(e("ve3", "v3", "v4", "是", (0, 0.5), (0.5, 0), vert=True))
p4.append(e("ve4", "v3", "v5", "否", (1, 0.5), (0.5, 0), vert=True))
# diff
p4.append(v("diff", "1", SW(NEUTRAL), "diff（升級後：新模板 vs 使用者檔）", 1440, 60, 440, 480))
p4.append(v("d0", "diff", ELLIPSE(GREEN), "開始 diff", 140, 50, 160, 50))
p4.append(v("d1", "diff", LEAF(), "對 init.toml 的每一項：\nimage 內的新版 src vs 專案內的 dest", 100, 130, 240, 50))
p4.append(v("d3", "diff", RHOMBUS, "有差異？", 130, 220, 180, 80))
p4.append(v("d4", "diff", LEAF(), "無差異", 20, 340, 180, 50))
p4.append(v("d5", "diff", LEAF(), "顯示差異", 240, 340, 180, 50))
p4.append(v("d6", "diff", ELLIPSE(GREEN), "結束（不改使用者檔案）", 230, 420, 200, 40))
p4.append(e("de5", "d5", "d6"))
p4.append(e("de6", "d4", "d6", "", (0.5, 1), (0, 0.5)))
p4.append(e("de0", "d0", "d1")); p4.append(e("de2", "d1", "d3"))
p4.append(e("de3", "d3", "d4", "否", (0, 0.5), (0.5, 0), vert=True))
p4.append(e("de4", "d3", "d5", "是", (1, 0.5), (0.5, 0), vert=True))
p4.append(v("p4n", "1", NOTE, "仍待決：verify 要跟印記比、還是重新從 image 拿來比；diff 要不要連舊版模板一起比（三方比對）；兩個 just 同時安裝時怎麼互斥（lock）。", 960, 560, 920, 40))
p4 += legend_flow("p4", 40, 900, purple=False, note=True)
p4 += terms("p4", 40, 1010, [
 ("暫存目錄", "先把整個 dist/ 寫到 .<name>.tmp/，最後一步才改名成 .<name>/；中途失敗舊目錄不受影響"),
 ("src → dest", "init.toml 每一項：src 指 image 的 dist/ 裡哪個檔，dest 指要放到專案的哪裡"),
 ("原子替換", "先在暫存目錄準備好全部新檔，最後用一次改名換掉舊目錄；任何時刻看到的都是完整的舊版或完整的新版"),
 ("印記 / 指紋", "印記 = .<name>/.stamp（版本 + 每檔指紋）；指紋 = 由檔案內容算出的識別碼，內容一改就不同"),
 ("vendor_kit / image / dist", "安裝工具本身／打包好可執行的檔案包／工具要出貨的檔案"),
 ("init.toml / 啟動器", "init 要建立哪些檔的清單／專案裡的 justfile（使用者打 just 時執行的指令清單）"),
 ("容器 / <name>", "容器 = image 執行起來的實例；<name> = .version 裡的工具名，安裝目錄就叫 .<name>/"),
])

# ================= Page 7: 原型對照 =================
p7 = [v("title", "1", TITLE, "原型對照：proto/ 三個資料夾 ↔ 框架裡的三種角色", 40, 20, 900, 30)]
p7.append(v("row_t", "1", TEXT(12) + "align=left;", "原始碼（進 git，人維護）", 40, 70, 300, 20))
p7.append(v("row_g", "1", TEXT(12) + "align=left;", "產物（不進 git；原型在本機建置，正式版由 CI 建置＋上傳）", 640, 70, 420, 20))
p7.append(v("row_d", "1", TEXT(12) + "align=left;", "使用端（前三樣進 git）", 1080, 70, 300, 20))
p7.append(v("r_vk", "1", SW(RED), "vendor_kit repo", 40, 100, 300, 200))
p7.append(v("r_vk_t", "r_vk", TEXT(11), "= proto/vendor_kit/", 10, 40, 280, 18))
p7.append(v("f_vk", "r_vk", LEAF(), "vendor_kit\n（安裝工具程式）", 20, 70, 120, 50))
p7.append(v("f_vkdf", "r_vk", LEAF(), "Dockerfile\n（打包食譜）", 160, 70, 120, 50))
p7.append(v("r_vk_n", "r_vk", TEXT(11), "vendor_kit 是產品本體；Dockerfile 只說明怎麼把它裝進 image", 10, 135, 280, 50))
p7.append(v("r_tool", "1", SW(GREEN), "工具 repo", 40, 340, 300, 250))
p7.append(v("r_tool_t", "r_tool", TEXT(11), "= proto/tool/", 10, 40, 280, 18))
p7.append(v("f_dist", "r_tool", LEAF(), "dist/\n（全部出貨，含模板）", 20, 70, 260, 50))
p7.append(v("f_init", "r_tool", LEAF(), "init.toml\n（init 清單）", 20, 130, 120, 50))
p7.append(v("f_tdf", "r_tool", LEAF(), "Dockerfile.dist\n（出貨食譜）", 160, 130, 120, 50))
p7.append(v("r_tool_n", "r_tool", TEXT(11), "Dockerfile.dist：FROM vendor_kit:v1，再疊上 dist/ 與 init.toml", 10, 190, 280, 50))
p7.append(v("ghcr", "1", SW(YELLOW), "image 存放處", 640, 100, 300, 490))
p7.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:v1", 40, 70, 220, 50))
p7.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:v0.1.0", 40, 370, 220, 50))
p7.append(v("g_n", "ghcr", TEXT(11), "原型：本機 Docker 快取；正式版：CI 在打 tag 時 push 到 GHCR", 10, 450, 280, 40))
p7.append(v("r_proj", "1", SW(GREEN), "專案 repo", 1080, 100, 340, 490))
p7.append(v("r_proj_t", "r_proj", TEXT(11), "= proto/project/", 10, 40, 320, 18))
p7.append(v("f_ver", "r_proj", LEAF(), ".version", 20, 70, 140, 40))
p7.append(v("f_just", "r_proj", LEAF(), "justfile", 180, 70, 140, 40))
p7.append(v("f_user", "r_proj", LEAF(), "Dockerfile、設定檔（setup.toml）…\n（init 建立後歸使用者）", 20, 120, 300, 50))
p7.append(v("f_land", "r_proj", LEAF(), ".<name>/（含 .stamp 印記檔）\n（不進 git，install 寫出）", 20, 370, 300, 50))
p7.append(v("r_proj_n", "r_proj", TEXT(11), "專案只在 .version 指定工具的 image，\n不必另外指定 vendor_kit", 10, 450, 320, 36))
p7.append(e("x1", "f_vkdf", "g_vk", "建置成 image", (1, 0.5), (0, 0.5), offset=(0, -4)))
p7.append(e("x2", "f_tdf", "g_tool", "建置成 image", (1, 0.5), (0, 0.5), offset=(0, -4)))
p7.append(e("x3", "g_vk", "g_tool", "FROM（基底）", (0.5, 1), (0.5, 0), dashed=True, vert=True))
p7.append(e("x4", "g_tool", "f_land", "dist（install 寫出）", (1, 0.75), (0, 0.75), pos=0.2))
p7.append(e("x5", "f_ver", "g_tool", "指定用哪個 image", (0, 0.5), (1, 0.15), pos=-0.6))
p7 += legend("p7", 40, 640, ["red", "green", "yellow", "pimg", "white"], "實線 = 傳輸內容\n虛線箭頭 = 基底 → 以它為底的 image")
p7 += terms("p7", 40, 750, [
 ("proto/", "可執行的原型：三個資料夾各對應框架裡的一個角色；image 只 build 到本機，沒有 push"),
 ("<name>", "工具名的占位符。原型不是真實工具，直接用 tool 當占位值：image 叫 tool-dist、目錄叫 .tool/"),
 (".stamp", "印記檔：install 寫下的「版本 + 每檔指紋」"),
 ("setup.toml", "範例工具給專案的設定檔（TOML）"),
 ("GHCR / image / CI", "GitHub 的 image 倉庫／打包好可執行的檔案包／打 tag 時自動 build 並 push 的流程"),
 (".version / justfile / init.toml", "專案記工具版本的檔／專案的指令入口（啟動器）／工具給的初始檔清單"),
 ("Dockerfile / Dockerfile.dist / FROM", "打包 image 的食譜／工具 repo 出貨用的食譜／食譜第一行，指定以哪個 image 為底"),
 ("dist / 模板 / tag", "工具要出貨的檔案／dist 裡給初始檔用的樣板／image 的版本名稱"),
 ("建置 / 上傳 / 指紋 / TOML", "把食譜做成 image（docker build）／把 image 放到倉庫（docker push）／由檔案內容算出的識別碼／設定檔格式"),
])


# ================= Page 7: repo 結構與測試分層 =================
p8 = [v("title", "1", TITLE, "vendor_kit repo：資料夾結構 → Dockerfile stage → 每一層的強制閘門（環境檢查先於一切）", 40, 20, 1300, 30)]
COLH = 1080
# 欄 1：repo 目錄
p8.append(v("repo", "1", SW(RED), "vendor_kit repo", 40, 70, 420, COLH))
p8.append(v("d_src", "repo", SW(RED, 16), "src/vendor_kit/（第 1 頁的 7 個模組）", 20, 50, 380, 140))
MODS = [("cli", "命令介面"), ("dist_reader", "出貨內容讀取"), ("repo_fs", "專案檔案存取"), ("template", "模板"),
        ("stamp", "印記"), ("diff", "差異比對"), ("report", "回報")]
for i, (m, zh) in enumerate(MODS):
    p8.append(v(f"m_{m}", "d_src", LEAF().replace("fontSize=14", "fontSize=11"), f"{m}.py\n{zh}", 12 + (i % 4) * 92, 45 + (i // 4) * 46, 86, 40))
p8.append(v("d_test", "repo", SW(NEUTRAL), "test/（先分測試工具、再分層級）", 20, 200, 380, 681))
TW = 356
S12 = '.replace("fontSize=14", "fontSize=12")'
p8.append(v("t_env", "d_test", LEAF(), "env/check.sh\n環境檢查：image 內 python3、tomllib、vendor_kit 進入點、toml-bridge", 12, 45, TW, 44).replace("fontSize=14", "fontSize=12"))
p8.append(v("t_fix", "d_test", LEAF(), "fixtures/\n假的 dist/、init.toml、VERSION、假專案", 12, 100, TW, 44))
p8.append(v("t_lint", "d_test", LEAF(), "lint/{ruff, import-linter}/ + mirror_check.py + blackbox_check.py\n寫法檢查、import 分層契約、鏡射檢查、黑箱檢查", 12, 185, TW, 44).replace("fontSize=14", "fontSize=12"))
p8.append(v("t_unit", "d_test", LEAF(), "pytest/unit/\ntest_<模組>.py ×7（一個模組一個檔）", 12, 240, TW, 44))
p8.append(v("t_inst", "d_test", LEAF(), "pytest/integration/test_install.py", 12, 295, TW, 44))
p8.append(v("t_init", "d_test", LEAF(), "pytest/integration/test_init.py", 12, 350, TW, 44))
p8.append(v("t_ver", "d_test", LEAF(), "pytest/integration/test_verify.py\n＋ test_perf_verify.py（時間預算）", 12, 405, TW, 44))
p8.append(v("t_diff", "d_test", LEAF(), "pytest/integration/test_diff.py", 12, 460, TW, 44))
p8.append(v("t_sys", "d_test", LEAF(), "pytest/system/\n整個 image：docker run 每個子命令", 12, 515, TW, 44))
p8.append(v("t_acc", "d_test", LEAF(), "pytest/acceptance/\n第 3 頁三條泳道：在假專案裡真的打 just", 12, 570, TW, 44))
p8.append(v("t_conf", "d_test", LEAF(), "pytest/<層級>/conftest.py\n每層的限制寫在這（見右欄）", 12, 625, TW, 44))
p8.append(v("d_df", "repo", LEAF(), "Dockerfile（中欄的 stage）", 20, 900, 180, 40))
p8.append(v("d_bake", "repo", LEAF(), "docker-bake.hcl（group）", 220, 900, 180, 40))
p8.append(v("d_adr", "repo", LEAF(), "doc/adr/\n測試分層與閘門（本頁的決策）", 20, 960, 380, 44))
p8.append(v("d_ci", "repo", LEAF(), ".github/workflows/\nbake validate → system/acceptance → bake release", 20, 1016, 380, 44))
# 欄 2：Dockerfile stage（紫：每個 stage 都是 image）
SX, SW_ = 520, 480
LX, LW = 40, 230
p8.append(v("stages", "1", SW(NEUTRAL), "Dockerfile stage（BuildKit）", SX, 70, SW_ + 20, COLH))
p8.append(v("s_rt", "stages", PURPLE_LEAF, "runtime\nFROM toml-bridge + src/", LX, 50, LW, 50))
p8.append(v("s_env", "stages", PURPLE_LEAF, "env-test（環境檢查，smoke）", LX, 247, LW, 40))
p8.append(v("s_tb", "stages", PURPLE_LEAF, "test-base = env-test + pytest + fixtures", LX, 302, LW, 40).replace("fontSize=14", "fontSize=12"))
GRP = ("swimlane;html=1;rounded=1;startSize=30;fontStyle=1;fontSize=14;container=1;collapsible=0;recursiveResize=0;"
       f"fillColor={NEUTRAL};swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=2;")
GY = 350
p8.append(v("s_grp", "stages", GRP, "六個測試 stage（都 FROM test-base）", 20, GY, 440, 364))
LX = LX - 20
for k, (sid, t) in enumerate([("s_lint", "lint"), ("s_unit", "unit-test"), ("s_inst", "install-test"), ("s_init", "init-test"), ("s_ver", "verify-test"), ("s_diff", "diff-test")]):
    p8.append(v(sid, "s_grp", PURPLE_LEAF, t, LX, 37 + 55 * k, LW, 40))
p8.append(v("s_rel", "stages", PURPLE_LEAF, "release\n= runtime（最終產物）", LX + 20, 740, LW, 50))
p8.append(v("s_rtest", "stages", PURPLE_LEAF, "release-test\nFROM release；真的 install + verify 一次", LX + 20, 830, LW, 60))
p8.append(v("s_host", "stages", TEXT(11), "system / acceptance 不在 Dockerfile 裡：\n它們要 docker run，所以在 CI 主機上跑", 20, 905, 440, 40))
p8.append(v("s_bake", "stages", TEXT(11), "docker-bake.hcl：group validate = [env-test, lint, unit-test, install-test,\ninit-test, verify-test, diff-test]；group release = [release, release-test]", 20, 950, 440, 40))
p8.append(e("s1", "s_rt", "s_env", "FROM", (0.5, 1), (0.5, 0), vert=True))
p8.append(e("s1b", "s_env", "s_tb", "FROM（環境不對就到此為止）", (0.5, 1), (0.5, 0), vert=True))
p8.append(e("s2", "s_tb", "s_grp", "FROM", (0.5, 1), (0.3068, 0), vert=True))
p8.append('<mxCell id="s8" value="FROM\n（不經任何 test stage）" style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="stages" source="s_rt" target="s_rel"><mxGeometry x="0.785" relative="1" as="geometry"><Array as="points"><mxPoint x="475" y="75"/><mxPoint x="475" y="765"/></Array></mxGeometry></mxCell>')
p8.append(e("s9", "s_rel", "s_rtest", "FROM", (0.5, 1), (0.5, 0), vert=True))
# 欄 1 → 欄 2 的 COPY（同高直線）
for a, b in [("t_env", "s_env"), ("t_fix", "s_tb"), ("t_lint", "s_lint"), ("t_unit", "s_unit"), ("t_inst", "s_inst"), ("t_init", "s_init"), ("t_ver", "s_ver"), ("t_diff", "s_diff")]:
    p8.append(e(f"c_{b}", a, b, "COPY", (1, 0.5), (0, 0.5)))
# 欄 3：強制閘門，依層分組
GX = SX + SW_ + 80
p8.append(v("gates", "1", SW(NEUTRAL), "強制閘門（不靠提醒；違反就 CI 紅，依層分組）", GX, 70, 460, COLH))
GSW = ("swimlane;html=1;rounded=1;startSize=30;fontStyle=1;fontSize=14;container=1;collapsible=0;recursiveResize=0;"
       f"fillColor={NEUTRAL};swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=2;")
def gate_group(gid, title, y, gates):
    h = 30 + len(gates) * 60 + 10
    p8.append(v(gid, "gates", GSW, title, 20, y, 420, h))
    for i, (k, t) in enumerate(gates):
        p8.append(v(k, gid, LEAF().replace("fontSize=14", "fontSize=12"), t, 10, 40 + i * 60, 400, 50))
    return y + h + 10
y = 50
y = gate_group("ge", "smoke = 先確認環境能跑，再談測試（env-test stage）", y, [
    ("g0", "環境檢查先於一切\ntest-base FROM env-test：python3、tomllib、vendor_kit 進入點、toml-bridge 任一不對，六個測試 stage 都不會跑")])
y = gate_group("gl", "lint 層 = 不執行程式的檢查（lint stage）", y, [
    ("g_ruff", "ruff\n程式碼寫法檢查"),
    ("g2", "import-linter 分層契約\n只能由上層 import 下層（命令介面 → 讀取／存取 → 純函式）；只有 repo_fs、dist_reader 能碰檔案"),
    ("g3", "鏡射檢查\n每個 src 模組必有 test_<模組>.py，缺一個就失敗")])
y = gate_group("gu", "unit 層 = 一次測一個模組（unit-test stage）", y, [
    ("g4", "unit conftest\n測試中一碰檔案、網路、Docker 就直接失敗")])
y = gate_group("gi", "integration 層 = 一個子命令走到底（四個 *-test stage）", y, [
    ("g5", "integration conftest\n只給臨時目錄；禁 Docker、網路；只能走 cli.main()（程式的正門）"),
    ("g6", "一個子命令一個 stage\n各自只 COPY 自己的測試檔；哪個 stage 紅 = 第 5 頁哪條泳道壞"),
    ("g7", "時間預算\nverify 200 個檔必須 < 0.5 秒（已安裝且版本一致時，每次 just 都會跑它）")])
y = gate_group("gs", "system = 整個 image；acceptance = 真的打 just（CI 主機）", y, [
    ("g8", "黑箱檢查（lint stage）＋ conftest\n測試檔不准 import vendor_kit；只准 docker run／just 與檔案系統")])
y = gate_group("gr", "release = 出貨（release / release-test stage）", y, [
    ("g1", "BuildKit stage 依賴\nrelease 只 FROM runtime → 測試碼、pytest 進不了產品 image"),
    ("g9", "release 必過 release-test\nrelease image 真的 install + verify 一次，失敗就不上傳")])
p8.append(v("g_map", "gates", TEXT(11) + "align=left;", "對應：unit ↔ 第 1 頁模組；integration ↔ 第 5 頁泳道；acceptance ↔ 第 3 頁泳道。\n層級名稱依 ISTQB：unit / integration / system / acceptance；smoke 是測試類型（先於其他測試），不是層級", 20, y, 420, 50))
p8 += legend("p8", 40, 70 + COLH + 40, ["red", "pstage", "neutral", "white"], "實線 = 依賴／複製方向")
p8 += terms("p8", 40, 70 + COLH + 150, [
 ("stage", "Dockerfile 裡的一個階段（FROM … AS 名稱）；docker build --target <名稱> 只做到那一階"),
 ("FROM / COPY", "Dockerfile 的兩個指令：FROM = 以哪個 stage／image 為底；COPY = 把 repo 裡的檔案放進 stage"),
 ("BuildKit", "Docker 的建置引擎：只會建最終目標依賴到的 stage，沒被依賴的測試 stage 不會執行、也不會進 image"),
 ("bake", "docker buildx bake：用一個檔定義多個 stage 目標與群組，CI 一次平行跑"),
 ("smoke / env-test", "smoke = 正式測試前先確認東西能開機的最小檢查；env-test 就是它：確認 runtime image 的環境（Python、tomllib、進入點、toml-bridge）"),
 ("runtime / release / release-test", "runtime = 能執行 vendor_kit 的最小 image；release = 最終出貨的 image；release-test = 出貨前拿 release 真的裝一次"),
 ("toml-bridge", "vendor_kit image 的基底 image（另一個 repo 提供，內含 Python 與 TOML 工具）"),
 ("pytest / conftest.py", "Python 的測試框架／每個測試目錄的共用設定；這裡用它對該層測試強制限制"),
 ("ruff / import-linter", "Python 寫法檢查／檢查模組之間誰可以 import 誰（契約寫在設定檔）"),
 ("import / 純函式", "import = 一個模組引用另一個模組；純函式 = 只算結果、不碰檔案與網路的函式（template、diff、stamp、report）"),
 ("VERSION vs .version", "VERSION = fixtures 裡假 dist 的版本字串（image 內 /dist/VERSION，install 寫進印記）；.version = 專案 repo 記工具版本的檔"),
 ("鏡射", "test/ 的檔名跟 src/ 一一對應：src 有 cli.py，test 就必須有 test_cli.py"),
 ("黑箱", "只從外面用、不看裡面：system / acceptance 測試不准 import vendor_kit，只能像使用者一樣 docker run 或打 just"),
 ("install / verify / just", "install = 把 dist 裝進 .<name>/ 並寫印記；verify = 檢查 .<name>/ 沒被手改；just = 使用者在主機打的指令跑器（第 3、8 頁）"),
 ("fixture / 假專案", "測試用的假資料：假的 dist/、init.toml，以及一個只有 .version 與 justfile 的假專案"),
 ("cli.main()", "vendor_kit 程式的正門（命令介面的進入點）；integration 測試只准從這裡進"),
 ("docker run / CI", "把 image 跑成容器的指令／GitHub 上的自動化流程（每次推送都跑 bake validate）"),
 ("ADR / ISTQB", "設計決策紀錄（doc/adr/ 裡一個決策一個檔）／國際軟體測試標準，本頁的層級名稱來自它"),
 ("泳道", "流程圖裡的一條直欄，代表一個子命令或情境的完整流程"),
])

# ================= Page 8: 使用者介面：just 指令表 =================
p9 = [v("title", "1", TITLE, "使用者介面：just 指令表（使用者只會碰這些；每個指令前都先自動檢查／安裝）", 40, 20, 1300, 30)]
TH = "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999999;fontSize=12;fontStyle=1;align=center;strokeWidth=1;"
TC = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=12;align=left;spacingLeft=6;strokeWidth=1;"
TCB = TC + "fontStyle=1;fontFamily=Courier New;"
COLS = [("指令", 130), ("什麼時候打", 200), ("做什麼", 330), ("背後跑什麼", 300), ("動到專案裡的什麼", 260)]
def table(prefix, parent, x, y, rows, rh=48):
    cx = x
    for i, (h, w) in enumerate(COLS):
        p9.append(v(f"{prefix}_h{i}", parent, TH, h, cx, y, w, 30)); cx += w
    for r, row in enumerate(rows):
        cx = x
        for i, (cell, (h, w)) in enumerate(zip(row, COLS)):
            p9.append(v(f"{prefix}_r{r}c{i}", parent, TCB if i == 0 else TC, cell, cx, y + 30 + r * rh, w, rh)); cx += w
    return y + 30 + len(rows) * rh
TBW = sum(w for _, w in COLS)
# A：vendor_kit 提供
p9.append(v("gA", "1", SW(RED), "vendor_kit 提供的指令（每個用這套框架的專案都一樣）", 40, 70, TBW + 40, 320))
yA = table("ta", "gA", 20, 50, [
 ("just init", "第一次把工具接進專案", "安裝 .<name>/，再照 init.toml 建立初始檔（Dockerfile、設定檔、hooks…）；已存在的不動", "vendor_kit 容器：install → init", ".<name>/（新建）、初始檔（新建）"),
 ("just diff", "升級之後", "顯示新版模板 vs 你的初始檔差在哪；不改任何檔", "vendor_kit 容器：diff", "不動（只印到畫面）"),
 ("just upgrade", "沒有 Renovate 機器人時，想手動升級", "把 .version 改成最新版 → 重新安裝 → 顯示差異（細節待議）", "查 GHCR → 改 .version → install → diff", ".version、.<name>/"),
 ("（自動）", "每個 just 指令執行前", "第 3 頁的檢查：.<name>/.stamp 第一行 ≠ .version → install；相同 → verify；verify 失敗就中止", "vendor_kit 容器：install 或 verify", ".<name>/（可能重裝）"),
])
p9.append(v("gA_n", "gA", TEXT(11) + "align=left;", "verify 不開放給使用者單獨打：它是每個指令前的守門，不是一個要記的指令。", 20, yA + 6, TBW, 20))
# B：工具提供
p9.append(v("gB", "1", SW(GREEN), "工具 <name> 提供的指令（由工具的 dist/ 決定，每個工具可以不同；下面以「容器工作流」工具為例）", 40, 420, TBW + 40, 360))
yB = table("tb", "gB", 20, 50, [
 ("just build", "第一次、或改了 Dockerfile 之後", "建置專案自己的 image", ".<name>/ 的 build 腳本 → docker compose build", "本機 image（不在 repo 裡）"),
 ("just run", "要開始工作時", "啟動專案容器（在背景常駐）", ".<name>/ 的 run 腳本 → docker compose up", "容器（不在 repo 裡）"),
 ("just exec", "容器跑著的時候", "進到容器裡下指令", ".<name>/ 的 exec 腳本 → docker compose exec", "無"),
 ("just stop", "收工", "停掉並移除容器", ".<name>/ 的 stop 腳本 → docker compose down", "容器（移除）"),
])
p9.append(v("gB_n", "gB", NOTE, "為什麼是這四個：它們是「一個容器的一生」— 做出來（build）→ 開起來（run）→ 進去用（exec）→ 關掉（stop），一個階段一個指令。\n這四個是工具定義的，vendor_kit 只負責把工具裝好；換一個工具，這一區的指令就換一套。\n每個工具指令前後都可以掛你自己的腳本：script/hooks/pre/<指令>.sh、post/<指令>.sh（init 建立的空殼）。", 20, yB + 10, TBW, 66))
# C：一個指令的完整路徑
p9.append(v("gC", "1", SW(NEUTRAL), "任何一個 just 指令的完整路徑", 40, 810, TBW + 40, 205))
p9.append(v("c0", "gC", ELLIPSE(GREEN), "使用者打 just X", 20, 95, 160, 50))
p9.append(v("c1", "gC", LEAF(), "自動檢查／安裝\n（第 3 頁「日常」）", 220, 95, 180, 50))
p9.append(v("c2", "gC", RHOMBUS, "X 是誰的？", 440, 80, 160, 80))
p9.append(v("c3", "gC", PURPLE_LEAF, "起 vendor_kit 容器跑子命令\n（init / diff / upgrade）", 660, 55, 260, 50))
p9.append(v("c4", "gC", LEAF(), "執行 .<name>/ 裡的腳本\n（build / run / exec / stop…）", 660, 135, 260, 50))
p9.append(v("c5", "gC", ELLIPSE(GREEN), "畫面顯示結果", 980, 70, 160, 100))
p9.append(e("ce0", "c0", "c1", "", (1, 0.5), (0, 0.5)))
p9.append(e("ce1", "c1", "c2", "通過", (1, 0.5), (0, 0.5)))
p9.append(e("ce2", "c2", "c3", "vendor_kit 的", (0.5, 0), (0, 0.5)))
p9.append(e("ce3", "c2", "c4", "工具的", (0.5, 1), (0, 0.5)))
p9.append(e("ce4", "c3", "c5", "", (1, 0.5), (0, 0.1)))
p9.append(e("ce5", "c4", "c5", "", (1, 0.5), (0, 0.9)))
p9 += legend("p9", 40, 1040, ["red", "green", "neutral", "white", "pimg"], "表格：一列一個指令\n流程：實線 = 執行順序")
p9 += terms("p9", 40, 1150, [
 ("just / justfile", "just = 主機上的指令跑器；justfile = 專案裡給它讀的指令清單（啟動器）。使用者只需要記這一頁的指令"),
 ("<name>", "工具名（= .version 裡的 key）；工具裝在 .<name>/"),
 ("init.toml / 初始檔", "工具給的清單：第一次要複製到專案的檔案（Dockerfile、設定檔、hooks…）；建立後歸使用者，升級不會動"),
 ("印記 / .version", ".<name>/.stamp：記錄裝了哪個 image + 每檔指紋／專案記工具版本的檔；兩者不同就重裝"),
 ("Renovate / GHCR", "GitHub 上的機器人：有新版就自動開 PR 改 .version／GitHub 的 image 倉庫"),
 ("docker compose", "Docker 內建的多容器管理指令：build 建置、up 啟動、exec 進入、down 停止"),
 ("hooks", "掛勾腳本：每個工具指令前（pre）後（post）自動執行的你的腳本，預設是空殼"),
 ("容器工作流", "用容器當開發環境的工作方式：建置 image → 啟動容器 → 進去工作 → 停掉；本頁 B 區的四個指令就是它"),
])

doc = ('<mxfile host="app.diagrams.net">'
       + page("p1", "1. vendor_kit 架構圖", p1, w=1700, h=1430)
       + page("p1b", "2. 框架定義", p1b, w=1800, h=1160)
       + page("p2", "3. 流程：使用者指令", p2, w=1700, h=1580)
       + page("p3", "4. 流程：版本生命週期", p3, h=1030)
       + page("p4", "5. 流程：vendor_kit 內部", p4, w=1920, h=1160)
       + page("p7", "6. 原型對照", p7, h=920)
       + page("p8", "7. repo 結構與測試分層", p8)
       + page("p9", "8. 使用者介面：just 指令表", p9)
       + "</mxfile>")
open("/home/cyc/Desktop/vendor-kit_ws/src/dist_distribution.drawio", "w").write(doc)
print(len(doc))
