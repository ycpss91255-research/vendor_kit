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
PEND = "shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#fff2cc;strokeColor=#d6b656;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;fontSize=12;"
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
 "folder": (LEAF(),             "實線框：資料夾", 120, 40, 10),
 "filebox":(FILE,               "虛線框：檔案", 120, 40, 10),
 "rhomb":  (RHOMBUS,            "黃：判斷", 110, 60, 0),
 "startend":(ELLIPSE(GREEN),    "綠橢圓：起點／終點", 160, 40, 10),
 "notebox":(NOTE,               "便條：補充說明", 130, 40, 10),
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
    return legend(prefix, x, y, ["red", "green", "yellow", "pimg", "white"], "實線 = 傳輸內容（線上文字 = 傳什麼）\n虛線 = 只在特定情況發生")
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
p1.append(v("p1_pend", "1", PEND, "⚠ 待你回覆：命令介面的子命令清單是否就是 install / init / verify / diff / accept / bootstrap / upgrade 七個？", 960, 15, 560, 60))
VX, VY = 480, 140
p1.append(v("user", "1", SW(YELLOW), "使用者", 40, VY, 140, 940))
p1.append(v("u_cmd", "user", LEAF(), "指令", 26, 100, 88, 40))
p1.append(v("u_out", "user", LEAF(), "畫面", 26, 890, 88, 40))
p1.append(v("img", "1", PURPLE_SW, "image 內容", 200, 300, 180, 280))
p1.append(v("i_list", "img", LEAF(), "init.toml", 46, 121, 88, 40))
p1.append(v("i_dist", "img", LEAF(), "dist/（全部）", 46, 172, 88, 40))
p1.append(v("i_tpl", "img", LEAF(), "模板", 46, 223, 88, 40))
p1.append(v("vk", "1", PURPLE_SW, "vendor_kit（一個 container）", VX, VY, 660, 940))
p1.append(v("m_cli", "vk", SW(RED), "命令介面（子命令，對應第 9 頁指令表）", 20, 50, 384, 140))
p1.append(v("cli_land", "m_cli", LEAF(), "install", 12, 45, 88, 40))
p1.append(v("cli_init", "m_cli", LEAF(), "init", 104, 45, 88, 40))
p1.append(v("cli_verify", "m_cli", LEAF(), "verify", 196, 45, 88, 40))
p1.append(v("cli_diff", "m_cli", LEAF(), "diff", 288, 45, 88, 40))
p1.append(v("cli_accept", "m_cli", LEAF(), "accept", 12, 92, 88, 40))
p1.append(v("cli_boot", "m_cli", LEAF(), "bootstrap", 104, 92, 88, 40))
p1.append(v("cli_upg", "m_cli", LEAF(), "upgrade", 196, 92, 88, 40))
p1.append(v("m_list", "vk", SW(RED), "出貨內容讀取", 20, 250, 200, 170))
p1.append(v("ls_read", "m_list", LEAF(), "讀 dist/", 12, 45, 88, 40))
p1.append(v("ls_check", "m_list", LEAF(), "讀 init.toml", 104, 45, 88, 40))
p1.append(v("ls_class", "m_list", LEAF(), "檢查清單\n格式", 12, 92, 88, 40))
p1.append(v("m_tpl", "vk", SW(RED), "模板", 20, 560, 200, 130))
p1.append(v("tp_render", "m_tpl", LEAF(), "複製", 12, 45, 88, 40))
p1.append(v("tp_vars", "m_tpl", LEAF(), "渲染／帶入\n變數（待定）", 104, 45, 88, 40))
p1.append(v("m_diff", "vk", SW(RED), "差異比對", 20, 750, 200, 130))
p1.append(v("df_cmp", "m_diff", LEAF(), "三方分類", 12, 45, 88, 40))
p1.append(v("df_patch", "m_diff", LEAF(), "產生差異", 104, 45, 88, 40))
p1.append(v("m_write", "vk", SW(RED), "專案檔案存取", 300, 250, 292, 270))
p1.append(v("wr_copy", "m_write", LEAF(), "寫入", 12, 45, 88, 40))
p1.append(v("wr_read", "m_write", LEAF(), "讀回", 104, 45, 88, 40))
p1.append(v("wr_perm", "m_write", LEAF(), "權限設定", 196, 45, 88, 40))
p1.append(v("wr_atomic", "m_write", LEAF(), "整批替換", 12, 92, 88, 40))
p1.append(v("wr_lock", "m_write", LEAF(), "鎖（專案\n目錄）", 104, 92, 88, 40))
p1.append(v("wr_base", "m_write", LEAF(), "讀寫基準", 196, 92, 88, 40))
p1.append(v("m_stamp", "vk", SW(RED, 16), "印記與比對", 392, 560, 200, 130))
p1.append(v("st_tree", "m_stamp", LEAF(), "兩棵樹比對", 12, 45, 88, 40))
p1.append(v("st_hash", "m_stamp", LEAF(), "產生印記", 104, 45, 88, 40))
p1.append(v("st_cmp", "m_stamp", LEAF(), "讀已裝版本", 12, 85, 88, 40))
p1.append(v("m_report", "vk", SW(RED), "回報", 300, 750, 200, 130))
p1.append(v("rp_msg", "m_report", LEAF(), "訊息", 12, 45, 88, 40))
p1.append(v("rp_code", "m_report", LEAF(), "結束狀態", 104, 45, 88, 40))
p1.append(v("proj", "1", SW(GREEN), "專案 repo 的目錄", 1320, VY, 200, 940))
p1.append(v("p_stamp", "proj", LEAF(), ".<repo>/\n.stamp", 56, 250, 88, 40))
p1.append(v("p_base", "proj", LEAF(), ".<repo>/", 56, 296, 88, 40))
p1.append(v("p_user", "proj", LEAF(), "使用者檔案", 56, 342, 88, 40))
p1.append(v("p_bl", "proj", LEAF(), "基準\n（baseline）", 56, 420, 88, 40))
p1.append(v("p_boot", "proj", LEAF(), "啟動器 .vendor_kit/\n＋ 根目錄的 justfile、.version", 10, 490, 180, 44).replace("fontSize=14", "fontSize=12"))
p1.append(e("a1", "u_cmd", "m_cli", "工具名、命令、參數", (1, 0.5), (0, 0.5)))
p1.append(e("a2", "m_cli", "m_list", "命令、參數（解析後）", (0.26, 1), (0.5, 0), vert=True))
p1.append(e("a3", "i_list", "m_list", "init 清單", (1, 0.5), (0, 0.3)))
p1.append(e("a4", "i_dist", "m_list", "dist 內容", (1, 0.5), (0, 0.6)))
p1.append(e("a5", "i_tpl", "m_list", "模板", (1, 0.5), (0, 0.9)))
p1.append(e("a6", "m_list", "m_write", "dist 全部", (1, 0.3), (0, 0.189)))
p1.append(e("a7", "m_list", "m_tpl", "init 清單\n＋模板", (0.5, 1), (0.5, 0), vert="left"))
p1.append(e("a8", "m_tpl", "m_write", "初始檔內容", (0.8, 0), (0.1, 1)))
p1.append(e("a9", "m_write", "m_stamp", "兩棵樹的內容\n（dist、.<repo>/）", (0.5068, 1), (0.28, 0), vert=True))
p1.append(e("a9b", "m_stamp", "m_write", "印記、\n已裝版本", (0.9, 0), (0.9315, 1), vert=True))
p1.append(e("a10", "m_write", "p_stamp", "印記檔", (1, 0.0741), (0, 0.5), both=True))
p1.append(e("a11", "m_write", "p_base", "dist 全部", (1, 0.2444), (0, 0.5), both=True))
p1.append(e("a12", "m_write", "p_user", "初始檔（init 時）", (1, 0.3778), (0, 0.25)))
p1.append(e("a12b", "p_user", "m_write", "現有內容（diff 時）", (0, 0.76), (1, 0.4533), vert="below"))
p1.append(e("a12c", "m_write", "p_bl", "基準（寫／讀）", (1, 0.7037), (0, 0.5), both=True))
p1.append(e("a12d", "m_write", "p_boot", "bootstrap 寫出", (1, 0.9704), (0, 0.5)))
p1.append('<mxCell id="a13" value="使用者檔案、基準" style="' + EDGE + 'exitX=0.3014;exitY=1;exitDx=0;exitDy=0;entryX=0.9;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="m_write" target="m_diff"><mxGeometry x="0.55" relative="1" as="geometry"><Array as="points"><mxPoint x="868" y="860"/><mxPoint x="680" y="860"/></Array></mxGeometry></mxCell>')
p1.append(e("a14", "m_tpl", "m_diff", "新版模板", (0.5, 1), (0.5, 0), vert=True))
p1.append(e("a15", "m_stamp", "m_report", "比對結果", (0.265, 1), (0.725, 0), vert=True))
p1.append(e("a16", "m_diff", "m_report", "差異、\n結束狀態", (1, 0.5), (0, 0.5)))
p1.append(e("a17", "m_report", "u_out", "訊息、結束狀態", (0.5, 1), (1, 0.5), pos=0.6))
p1 += legend("p1", 40, 1140, ["purple", "red", "green", "yellow", "white"], "實線 = 傳輸內容（線上文字 = 傳什麼）")
p1 += terms("p1", 40, 1250, [
 ("vendor_kit", "通用安裝工具；只以 container 形態執行（開發、使用皆是），主機不需安裝"),
 ("image / container", "image = 打包好的程式與檔案；container = image 執行起來的實例，跑完可刪"),
 ("<repo>", "工具名，由專案的 .version 指定；安裝目錄就叫 .<repo>/"),
 ("install / init / verify / diff / accept / bootstrap / upgrade", "子命令：安裝 dist 到 .<repo>/／第一次建立使用者檔／檢查 .<repo>/ 沒被改／升級後三方比對／把新版模板存成基準／寫出啟動器（第 10 頁）／查最新版改 .version（第 11 頁）"),
 ("結束狀態", "程式結束時回報的數字：0 成功、非 0 失敗；diff 另有 0 沒差異／1 工具有改／2 可能重疊；啟動器據此決定要不要繼續"),
 ("兩棵樹比對", "verify 的做法：把 image 內的 dist 跟專案的 .<repo>/ 逐檔比：少了檔、多了檔（只豁免 .stamp）、內容不同、該可執行的變成不可執行、檔案種類不同（例如變成連結）都算失敗"),
 ("三方分類", "diff 對每個初始檔看三份：基準（上次確認過的模板）、新版模板、你的檔 → 分成沒人改／只有工具改／只有你改／兩邊都改／你已套上相同內容"),
 ("基準（baseline）", ".vendor_kit/baseline/<repo>/：你上次確認過的那版模板副本；diff 用它分出「工具改了什麼」「你改了什麼」；init／accept 寫、人不改"),
 ("鎖（專案目錄）", "同一專案同時只有一個 install 在跑：對專案目錄上鎖（flock），後到的等前一個裝完；verify 拿共享鎖；程序被殺系統自動解鎖"),
 ("模組", "vendor_kit 內部的功能分塊；同一個 container 裡，不是各自的 container"),
 ("dist/", "工具 repo 裡要出貨的那批檔案，全部寫進專案的 .<repo>/"),
 ("init.toml", "工具 repo 提供的清單：init 時要複製到專案的初始檔有哪些、放哪（dist/ 本身每次 upgrade 都整包覆蓋）"),
 ("印記檔", ".<repo>/.stamp：第一行 = 裝的 image（啟動器傳進來的 .version 字串），之後每檔指紋（給人追溯用）；verify 只用第一行判斷要不要重裝，內容以 image 為準"),
 ("指紋", "由檔案內容算出的一串碼（sha256）；內容一改就不同"),
 ("模板", "工具 dist/ 裡給初始檔用的樣板（例如 Dockerfile 範本）；目前只複製；渲染 = 帶入變數（專案名等）產生實際檔案，待定"),
 ("repo", "一個 git 管理的專案資料夾；工具 repo = 工具的原始碼，專案 repo = 使用工具的專案"),
 (".version", "專案 repo 裡的版本清單（TOML）：一個工具一行，記工具名與 image 版本"),
 ("啟動器", "專案 repo 裡的 .vendor_kit/：vendor_kit 寫出的標準 just 指令，使用者打 just 時由它起容器；justfile 只是引用入口"),
 ("Dockerfile", "打包 image 的食譜；專案自己的 Dockerfile 是由模板建立的使用者檔案"),
 ("upgrade（升級）", "改 .version 換新版本。兩條路：機器人開 PR（人 merge）；或 just vendor_kit upgrade <repo>（只改 .version 那行就停）。之後下次 just 才裝新版，再打 just vendor_kit diff 看差異（第 11 頁）"),
 ("TOML / just / PR", "設定檔格式（key = \"value\"）／主機上的指令跑器，使用者打 just <指令>／GitHub 上的合併請求，merge = 接受修改"),
])

# ================= Page 2: 框架定義 =================
p1b = [v("title", "1", TITLE, "框架定義：兩種 repo 各自必須有什麼，以及工具怎麼送到專案", 40, 20, 1000, 30)]
p1b.append(v("tool", "1", SW(GREEN), "工具 repo（每個要出貨的工具一個）", 40, 290, 320, 260))
p1b.append(v("t_t", "tool", TEXT(11), "工具名 = <repo>；下面四樣是接上 vendor_kit 的必要條件", 10, 40, 300, 30))
p1b.append(v("t_dist", "tool", LEAF(), "dist/\n（要出貨的全部）", 20, 80, 135, 50))
p1b.append(v("t_init", "tool", LEAF(), "init.toml\n（初始檔清單）", 165, 80, 135, 50))
p1b.append(v("t_df", "tool", LEAF(), "Dockerfile.dist\n（只放檔案，沒有程式）", 20, 145, 135, 50))
p1b.append(v("t_ci", "tool", LEAF(), "CI：打 tag →\n建置＋上傳 image", 165, 145, 135, 50))
p1b.append(v("t_n", "tool", TEXT(11), "其他內容（doc、test、CI 腳本…）不在 dist/ 裡，不會出貨", 10, 205, 300, 40))
p1b.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 570, 320, 130))
p1b.append(v("vk_prog", "vk", LEAF(), "vendor_kit 程式", 20, 50, 135, 40))
p1b.append(v("vk_df", "vk", LEAF(), "Dockerfile", 165, 50, 135, 40))
p1b.append(v("tool2", "1", SW(GREEN), "另一個工具 repo（<repo2>，同型）", 40, 720, 320, 60))
p1b.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 420, 80, 260, 710))
p1b.append(v("g_t", "ghcr", TEXT(11), "tag 不覆蓋；被引用的版本不刪\nmulti-arch（amd64 + arm64）；附註來源 commit", 10, 40, 240, 40))
p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<repo>-dist:vX", 30, 360, 200, 40))
p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 540, 200, 40))
p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<repo2>-dist:vY", 30, 650, 200, 40))
p1b.append(v("proj", "1", SW(GREEN), "專案 repo（使用工具的專案）", 740, 80, 770, 710))
p1b.append(v("p_t", "proj", TEXT(11), "必要條件：.version、justfile、.vendor_kit/（啟動器本體，第 10 頁 bootstrap 寫出；justfile 只用 mod? 掛它）；每個工具各自裝到 .<repo>/", 10, 40, 750, 30))
p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器與版本檔", 20, 80, 700, 205))
p1b.append(v("pa_t", "pa", TEXT(11) + "align=left;", "都進 git，只有 .version.local 不進；.version 一行 = 一個工具 = 一個 .<repo>/；.version.local 有同名那行就優先（本機開發用，第 4 頁）", 12, 34, 676, 36))
p1b.append(v("p_ver", "pa", LEAF(), ".version", 12, 74, 90, 40))
p1b.append(v("p_vl", "pa", FILE, ".version.local\n（可選，不進 git）", 112, 74, 120, 40).replace("fontSize=14", "fontSize=11"))
p1b.append(v("p_just", "pa", LEAF(), "justfile", 250, 74, 78, 40))
p1b.append(v("p_vk", "pa", LEAF(), ".vendor_kit/（啟動器本體）\nvendor.just、tools.just、.stamp、baseline/<repo>/", 12, 142, 316, 50).replace("fontSize=14", "fontSize=12"))
p1b.append(v("pa_t2", "pa", TEXT(11) + "align=left;", "根 justfile 只有一行 mod? vendor_kit '.vendor_kit/vendor.just' → 指令都是 just vendor_kit <動作>；工具的 tool.just 也用自己的命名空間（mod? <模組> → just <模組> build）；工具 recipe 開頭先呼叫 just vendor_kit ensure 做自動檢查", 350, 74, 336, 118))
p1b.append(v("p_eng", "proj", PURPLE_LEAF, "引擎容器（vendor_kit:vN）\n一個專案只有這一版引擎", 20, 350, 300, 60))
p1b.append(v("p_eng_t", "proj", TEXT(11) + "align=left;", "以使用者身分執行，跑完即刪；先對專案目錄上鎖", 20, 412, 300, 20))
p1b.append(v("pb", "proj", SW(NEUTRAL), "使用者檔案（進 git）", 300, 440, 220, 125))
p1b.append(v("p_u1", "pb", LEAF(), "Dockerfile\n（專案自己的）", 12, 45, 100, 50))
p1b.append(v("p_u2", "pb", LEAF(), "設定檔…", 122, 45, 86, 50))
p1b.append(v("pb_t", "pb", TEXT(11), "init 建立；之後由使用者維護", 12, 98, 200, 18))
p1b.append(v("pc", "proj", SW(NEUTRAL), ".<repo>/（不進 git）", 540, 440, 220, 125))
p1b.append(v("p_c1", "pc", LEAF(), "dist 全部", 12, 45, 90, 40))
p1b.append(v("p_c2", "pc", LEAF(), "印記檔", 118, 45, 90, 40))
p1b.append(v("pc_t", "pc", TEXT(11), "每次 upgrade 整批覆蓋；verify 拿它跟 image 比\n印記檔 = 裝的 image + 每檔指紋", 6, 88, 210, 32))
p1b.append(v("pc2", "proj", SW(NEUTRAL, 14), ".<repo2>/（另一個工具）", 540, 645, 220, 50))
p1b.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1600, 80, 160, 710))
p1b.append(v("h_t", "host", TEXT(11), "需預先安裝這三個", 10, 40, 140, 20))
p1b.append(v("h_just", "host", LEAF(GREY), "just\n（執行 justfile）", 20, 70, 120, 50))
p1b.append(v("h_git", "host", LEAF(GREY), "git\n（管理專案 repo）", 20, 130, 120, 50))
p1b.append(v("h_docker", "host", LEAF(GREY), "Docker\n（跑所有容器）", 20, 477.5, 120, 50))
p1b.append(e("f1", "t_ci", "g_tool", "image", (1, 0.5), (0, 0.5), pos=-0.5))
p1b.append(e("f2", "tool2", "g_tool2", "image", (1, 0.5), (0, 0.5), pos=-0.5))
p1b.append(e("f3", "vk_df", "g_vk", "image", (1, 0.5), (0, 0.5), pos=0))
p1b.append(e("f6", "g_tool", "p_eng", "docker cp 抓出檔案", (1, 0.5), (0, 0.5)))
p1b.append(e("f6b", "g_vk", "p_eng", "引擎 image", (1, 0.5), (0, 0.85)))
p1b.append(e("f12", "g_tool2", "pc2", "檔案（同樣抓出後由引擎寫入）", (1, 0.5), (0, 0.5)))
p1b.append(e("f7", "p_ver", "p_vk", "工具名、版本", (0.5, 1), (0.142, 0), vert=True))
p1b.append(e("f7c", "p_vl", "p_vk", "有就優先", (0.5, 1), (0.506, 0), vert=True))
p1b.append(e("f7b", "p_just", "p_vk", "mod?", (0.5, 1), (0.877, 0), vert=True))
p1b.append(e("f8", "p_vk", "p_eng", "工具名、版本、使用者身分、專案路徑", (0.5, 1), (0.5667, 0), vert=True))
p1b.append(e("f9", "p_eng", "pc", "寫入 dist、印記檔", (1, 0.3), (0.5, 0)))
p1b.append(e("f10", "p_eng", "pb", "初始檔（只在 init 時）", (1, 0.7), (0.5, 0), pos=0.5))
p1b.append(e("f11", "pc", "h_docker", "compose 指令", (1, 0.5), (0, 0.5), offset=(0, -4)))
p1b += [c.replace("虛線框：檔案", "虛線框：可有可無的檔") for c in legend("p1b", 40, 820, ["red", "green", "yellow", "pimg", "neutral", "white", "grey", "filebox"], "實線 = 傳輸內容\n虛線箭頭 = 基底 image → 以它為底的 image；虛線框 = 可有可無的檔")]
p1b += terms("p1b", 40, 930, [
 ("工具 repo", "任何想透過 vendor_kit 出貨的工具的原始碼 repo；必須有 dist/、init.toml、Dockerfile.dist、CI"),
 ("專案 repo", "使用工具的專案；必須有 .version、justfile、.vendor_kit/；可同時用多個工具"),
 ("vendor_kit repo", "我們要開發的：安裝工具的原始碼，打包成 vendor_kit image"),
 ("image / 容器", "image = 打包好的程式與檔案；容器 = image 執行起來的實例，跑完可刪"),
 ("GHCR", "GitHub 提供的 image 倉庫；每個工具一個 <repo>-dist image，以 vendor_kit image 為底"),
 (".version", "專案裡的 TOML 檔，一個工具一行 name = \"image:tag@sha256:…\"；name 決定安裝目錄 .<repo>/"),
 (".version.local", "跟 .version 同格式的覆蓋檔，不進 git；開發工具本身時用它把某個工具指到本機路徑（第 4 頁）"),
 ("baseline（基準）", ".vendor_kit/baseline/<repo>/：上次確認過的模板副本，just vendor_kit diff 用它分出工具改了什麼、你改了什麼；vendor_kit 寫，人不改"),
 ("CI", "放在 GitHub 上的自動化流程：打 tag 時建置 image 並上傳 GHCR"),
 ("建置 / 上傳", "建置 = 照 Dockerfile 做出 image（docker build）；上傳 = 把 image 放到 GHCR（docker push）"),
 ("upgrade（升級）", "改 .version 換新版本。兩條路：機器人提出合併請求（PR，人 merge）；或 just vendor_kit upgrade <repo>（只改 .version 那行就停）。之後下次 just 才裝新版，再打 just vendor_kit diff（第 11 頁）"),
 ("PR / merge", "GitHub 上的合併請求／接受它，修改才進 repo"),
 ("上鎖", "安裝容器先對專案目錄上鎖：避免兩個 just 同時改同一個 .<repo>/，後到的等前一個裝完（第 5 頁）"),
 ("init.toml", "工具 repo 給的清單：dist/ 裡哪個檔（src）在 init 時要複製到專案的哪裡（dest）；之後那些檔歸使用者"),
 ("just / justfile / .vendor_kit/", "just = 主機的指令跑器；.vendor_kit/ = 啟動器本體（vendor_kit 寫出，人不改；升級只換 vendor.just／tools.just／.stamp，baseline/ 不動）；justfile = 專案自己的指令清單，第一行 mod? vendor_kit '.vendor_kit/vendor.just' 把它掛進來"),
 ("recipe / 命名空間 / mod? / ensure", "recipe = justfile 裡的一條指令；命名空間 = 指令前的分組名（just vendor_kit …、just <模組> …）；mod? = justfile 把另一個檔掛成命名空間的寫法；ensure = 每個工具指令開頭自動跑的檢查／安裝（第 3 頁）"),
 ("印記檔", ".<repo>/.stamp：安裝時寫下「裝的 image + 每檔指紋」；啟動器只看第一行決定要不要重裝，內容以 image 內的 dist 為準"),
 ("tag / digest", "image 的版本名稱（v0.43.0）／內容指紋（sha256:…）；.version 兩者都記，工具只認 digest"),
 ("multi-arch", "同一個 image 名稱同時提供 amd64 與 arm64 兩種處理器版本，Docker 依主機自動選；支援平台 = Linux（含 WSL2）amd64／arm64"),
 ("Dockerfile / Dockerfile.dist / FROM", "Dockerfile = 打包 image 的食譜；Dockerfile.dist = 工具 repo 出貨用的食譜；FROM = 食譜第一行，指定以哪個 image 為底"),
 ("commit", "git 的一次版本紀錄"),
 ("compose 指令", "docker compose：依設定檔啟動專案容器的指令"),
 ("TOML", "一種設定檔格式（key = \"value\"）；.version、init.toml 都用它"),
 ("install / init / verify / diff / accept", "安裝容器的子命令：把 dist 裝進 .<repo>/ 並寫印記檔／第一次建立初始檔／拿 .<repo>/ 跟 image 內的 dist 比／升級後三方比對／把新版模板存成基準"),
])

# ================= Page 3: 流程：使用者指令 =================
p2 = [v("title", "1", TITLE, "流程：使用者下的每個指令 → 啟動器叫哪個子命令 → 專案裡發生什麼", 40, 20, 1200, 30)]
for name, x, w in [("使用者", 40, 300), ("啟動器（.vendor_kit/，在主機）", 380, 360), ("安裝容器（vendor_kit）", 800, 360), ("專案目錄", 1240, 380)]:
    p2.append(v(f"h_{x}", "1", "text;html=1;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;", name, x, 60, w, 24))
def band(bid, title, y, h):
    p2.append(v(bid, "1", SW(NEUTRAL), title, 20, y, 1620, h))
# ---- A 第一次 ----
band("bA", "第一次接上工具：just vendor_kit init", 100, 280)
p2.append(v("a_u", "bA", ELLIPSE(GREEN), "just vendor_kit init", 60, 70, 180, 50))
p2.append(v("a_l1", "bA", LEAF(), "讀版本檔（.version.local 優先，\n否則 .version）一行一個工具", 375, 67, 150, 56).replace("fontSize=14", "fontSize=11"))
p2.append(v("a_l2", "bA", LEAF(), ".<repo>/ 不存在\n→ 要安裝", 560, 70, 160, 50))
p2.append(v("a_c1", "bA", PURPLE_LEAF, "install\ndist/ 全部 → .<repo>/\n並寫印記（.<repo>/.stamp：裝的 image + 每檔指紋）", 800, 60, 340, 70).replace("fontSize=14", "fontSize=13"))
p2.append(v("a_p1", "bA", FILE, ".<repo>/（新）", 1240, 75, 200, 40))
p2.append(v("a_c2", "bA", PURPLE_LEAF, "init\n照 init.toml 複製初始檔（已存在：警告、不覆蓋）\n並把這版模板存成基準", 800, 165, 340, 60).replace("fontSize=14", "fontSize=13"))
p2.append(v("a_p2", "bA", FILE, "Dockerfile / entrypoint / hooks…\n（新；之後由你維護）\n＋ .vendor_kit/baseline/<repo>/", 1240, 165, 200, 60).replace("fontSize=14", "fontSize=12"))
p2.append(e("ae1", "a_u", "a_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae2", "a_l1", "a_l2", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae3", "a_l2", "a_c1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae4", "a_c1", "a_p1", "寫入", (1, 0.5), (0, 0.5)))
p2.append(e("ae5", "a_c1", "a_c2", "", (0.5, 1), (0.5, 0)))
p2.append(e("ae6", "a_c2", "a_p2", "建立", (1, 0.5), (0, 0.5)))
# ---- B 日常 ----
band("bB", "日常：just <模組> build（建置）；run（啟動）／exec（進入）／stop（停止）流程相同", 410, 390)
p2.append(v("b_u", "bB", ELLIPSE(GREEN), "just <模組> build", 60, 70, 180, 50))
p2.append(v("b_l1", "bB", LEAF(), "讀版本檔（.version.local 優先，\n否則 .version）一行一個工具", 355, 67, 150, 56).replace("fontSize=14", "fontSize=11"))
p2.append(v("b_note", "bB", NOTE, ".version 一行 = 一個工具：<repo> = \"…-dist:vX@sha256:…\"\n左邊 = 工具名 → 目錄 .<repo>/；右邊 = image → 跟 .<repo>/.stamp 第一行比\n每一行各跑一次右邊流程；「否則」= 不同、尚未安裝、印記讀不到\n例外：右邊是 path:（.version.local）→ 第 4 頁本機開發模式；\nvendor_kit 那行 → 換 .vendor_kit/ 程式檔（第 11 頁 C）", 30, 130, 300, 150))
p2.append(v("b_l2", "bB", RHOMBUS, ".<repo>/.stamp 第一行\n= .version 那行的 image？", 530, 55, 220, 80).replace("fontSize=14", "fontSize=12"))
p2.append(v("b_c0", "bB", PURPLE_LEAF, "install\n換成 .version 指定的版本", 800, 65, 340, 60))
p2.append(v("b_l1n", "bB", TEXT(11), "（image 不在本機時，Docker 會先下載）", 340, 126, 220, 24))
p2.append(v("b_p0", "bB", FILE, ".<repo>/（換新）", 1240, 75, 200, 40))
p2.append(v("b_c1", "bB", PURPLE_LEAF, "verify\n.<repo>/ 跟 image 內的 dist 逐檔比（缺、多、改都算）", 800, 170, 340, 60).replace("fontSize=14", "fontSize=13"))
p2.append(v("b_l3", "bB", LEAF(), "執行 .<repo>/ 內的 build（建置）腳本", 380, 290, 340, 50))
p2.append(v("b_p1", "bB", LEAF(), "docker compose build", 1240, 295, 200, 40))
p2.append(v("b_err", "bB", ELLIPSE(RED), "中止：.<repo>/ 被改過（列出哪些檔）\n刪除 .<repo>/ 再 build 即自動重裝", 40, 285, 260, 60).replace("fontSize=14", "fontSize=12"))
p2.append(e("be1", "b_u", "b_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("be2", "b_l1", "b_l2", "", (1, 0.5), (0, 0.5)))
p2.append(e("be3", "b_l2", "b_c0", "否則", (1, 0.5), (0, 0.5)))
p2.append(e("be4", "b_l2", "b_c1", "相同", (0.5, 1), (0, 0.5), vert=True, pos=-0.7))
p2.append(e("be5", "b_c0", "b_p0", "覆蓋", (1, 0.5), (0, 0.5)))
p2.append('<mxCell id="be6" value="用換新後的目錄" style="' + EDGE + 'align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.76;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="bB" source="b_p0" target="b_l3"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="1340" y="270"/><mxPoint x="638" y="270"/></Array></mxGeometry></mxCell>'.replace('<mxGeometry relative="1" as="geometry">', '<mxGeometry x="-0.8" relative="1" as="geometry">'))
p2.append('<mxCell id="be7" value="通過" style="' + EDGE + 'align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;exitX=0.15;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="bB" source="b_c1" target="b_l3"><mxGeometry x="-0.9" relative="1" as="geometry"><Array as="points"><mxPoint x="851" y="250"/><mxPoint x="550" y="250"/></Array></mxGeometry></mxCell>')
p2.append('<mxCell id="be8" value="失敗" style="' + EDGE + 'align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;exitX=0;exitY=0.9;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="bB" source="b_c1" target="b_err"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="340" y="224"/><mxPoint x="340" y="315"/></Array></mxGeometry></mxCell>'.replace('<mxGeometry relative="1" as="geometry">', '<mxGeometry x="0.5" relative="1" as="geometry">'))
p2.append(e("be9", "b_l3", "b_p1", "", (1, 0.5), (0, 0.5)))
# ---- C 升級 ----
band("bC", "升級：Renovate 開的 PR 被 merge", 830, 390)
p2.append(v("c_u", "bC", ELLIPSE(GREEN), "merge PR\n（.version 改了）", 60, 60, 180, 60))
p2.append(v("c_l1", "bC", LEAF(), "下次 just <模組> build 走上面\n「否則」分支 → install 新版", 380, 65, 340, 50))
p2.append(v("c_p1", "bC", FILE, ".<repo>/（新版）", 1240, 70, 200, 40))
p2.append(v("c_u2", "bC", ELLIPSE(GREEN), "just vendor_kit diff", 60, 160, 180, 50))
p2.append(v("c_c2", "bC", PURPLE_LEAF, "diff（三方）\n基準 vs image 內的新版模板 vs 你的初始檔\n只印出「工具改了什麼」「你改了什麼」，不改檔", 800, 155, 340, 60).replace("fontSize=14", "fontSize=12"))
p2.append(v("c_p2", "bC", FILE, "Dockerfile 等（你的）", 1240, 150, 200, 40))
p2.append(v("c_u3", "bC", LEAF(), "看差異，自己決定\n要不要改", 60, 230, 180, 55))
p2.append(v("c_u4", "bC", ELLIPSE(GREEN), "跟進完 → just vendor_kit\naccept <repo>", 30, 308, 240, 56))
p2.append(v("c_c3", "bC", PURPLE_LEAF, "accept\n把 image 內的新版模板存成基準", 800, 305, 340, 60))
p2.append(v("c_p3", "bC", FILE, ".vendor_kit/baseline/<repo>/\n（進 git，人不改）", 1240, 310, 200, 50))
p2.append(e("ce1", "c_u", "c_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ce2", "c_l1", "c_p1", "下次 build 時才發生", (1, 0.5), (0, 0.5), dashed=True))
p2.append(e("ce3", "c_u2", "c_c2", "", (1, 0.5), (0, 0.5)))
p2.append(e("ce4", "c_p2", "c_c2", "讀", (0, 0.5), (1, 0.25)))
p2.append('<mxCell id="ce4b" value="讀" style="' + EDGE + 'align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;exitX=0;exitY=0.2;exitDx=0;exitDy=0;entryX=1;entryY=0.8;entryDx=0;entryDy=0;" edge="1" parent="bC" source="c_p3" target="c_c2"><mxGeometry x="0.3" relative="1" as="geometry"><Array as="points"><mxPoint x="1215" y="320"/><mxPoint x="1215" y="203"/></Array></mxGeometry></mxCell>')
p2.append(e("ce6", "c_u4", "c_c3", "", (1, 0.5), (0, 0.5)))
p2.append(e("ce8", "c_u3", "c_u4", "", (0.5, 1), (0.5, 0)))
p2.append(e("ce7", "c_c3", "c_p3", "寫入", (1, 0.5), (0, 0.5), pos=-0.7))
p2.append('<mxCell id="ce5" value="印出差異" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="bC" source="c_c2" target="c_u3"><mxGeometry x="0.4" relative="1" as="geometry"><Array as="points"><mxPoint x="970" y="258"/><mxPoint x="300" y="258"/></Array></mxGeometry></mxCell>')
p2.append(v("p2n", "1", NOTE, "紫框 = 子命令：install（第一次、版本改變時）、init（只有第一次）、verify（已安裝且版本一致時）、diff／accept（升級後由使用者呼叫）。\n沒有 Renovate 時用 just vendor_kit upgrade <repo> 手動：只改 .version 那行就停；下次 just 才 install，再自己打 just vendor_kit diff（第 11 頁 B）。\n同一專案兩個 just 同時跑：容器先對專案目錄上鎖，後到的等前一個裝完再檢查（第 5 頁）。", 20, 1240, 1620, 60))
p2 += legend_flow("p2", 40, 1320, files=True, note=True, dashed=True)
p2 += terms("p2", 40, 1430, [
 ("啟動器", "專案裡的 .vendor_kit/（vendor_kit 寫出的標準 just 指令；justfile 只是引用它）：使用者打 just 時，它讀版本檔、起安裝容器、再執行工具的腳本"),
 ("上鎖", "容器先對專案目錄上鎖：兩個 just 同時跑時，後到的等前一個裝完再檢查，避免同時改同一個 .<repo>/（第 5 頁）"),
 ("印記", ".<repo>/.stamp：install 寫下的「第一行 = 裝的 image，之後每行 = 一個檔的指紋」；啟動器只拿第一行判斷要不要重裝，內容以 image 內的 dist 為準"),
 ("基準 / accept", ".vendor_kit/baseline/<repo>/ = 上次確認過的模板副本；diff 靠它分出工具改了什麼、你改了什麼；just vendor_kit accept <repo> 把新版模板存成基準"),
 (".version.local", "跟 .version 同格式、不進 git 的覆蓋檔；開發工具本身時用（第 4 頁），平常沒有這個檔"),
 ("Renovate", "GitHub 上的機器人：GHCR 有新版就自動開 PR 改 .version；沒有它時用 just vendor_kit upgrade 手動"),
 ("docker compose", "工具腳本最後真正拿來建置／啟動／進入／停止專案容器的指令"),
 ("build / run / exec / stop", "四個日常指令：建置 image／啟動容器／進入容器／停止容器；都先經過同樣的檢查再執行 .<repo>/ 內的腳本"),
 (".version", "專案裡的版本清單（TOML）：一個工具一行 <repo> = \"image\"；<repo> 決定安裝目錄 .<repo>/ 和要比對哪個印記"),
 ("install / init / verify / diff / accept", "子命令：安裝 dist 到 .<repo>/ 並寫印記／第一次建立初始檔／拿 .<repo>/ 跟 image 內的 dist 比／升級後三方比對／存新基準"),
 ("sha256 / 容器", "image 的內容指紋（跟在 @ 後面，鎖定內容）／容器 = image 執行起來的實例，跑完可刪"),
 ("PR / merge", "GitHub 上的合併請求／接受它"),
 ("GHCR", "GitHub 的 image 倉庫"),
 ("dist / image / 模板", "dist = 工具要出貨的檔案；image = 打包好可執行的檔案包；模板 = dist 裡給初始檔用的樣板"),
 ("just", "主機上的指令跑器；使用者打 just <指令>，它照 justfile 執行"),
 ("init.toml", "工具提供的清單：init 時要複製到專案的初始檔有哪些、放哪"),
 ("entrypoint / hooks", "初始檔的例子：容器啟動腳本／各指令前後可掛的自訂腳本"),
 ("<repo> / 指紋", "<repo> = .version 裡的工具名，安裝目錄就叫 .<repo>/；指紋 = 由檔案內容算出的識別碼，內容一改就不同"),
 ("vendor_kit / Dockerfile / TOML", "安裝工具本身（在容器內跑）／打包 image 的食譜、也是專案自己的 image 食譜／設定檔格式"),
 ("just vendor_kit upgrade", "手動升級指令：只把 .version 那行改成新版就停（不裝、不 diff）；下次 just 才裝，再打 just vendor_kit diff（第 11 頁 B）"),
])

# ================= Page 3: 流程：版本生命週期 =================
p3 = [v("title", "1", TITLE, "流程：版本生命週期", 40, 20, 700, 30)]
p3.append(v("up", "1", SW(NEUTRAL), "升級（摘要；四條路徑見第 11 頁）", 20, 60, 440, 440))
p3.append(v("c5", "up", LEAF(), "指定新版本（改 .version；Renovate PR 或 just vendor_kit upgrade）", 20, 50, 380, 40).replace("fontSize=14", "fontSize=12"))
p3.append(v("c6", "up", LEAF(), "執行 just → 啟動器自動 install 新版", 20, 110, 380, 40))
p3.append(v("c7", "up", LEAF(), ".<repo>/ 整批換成新版（含模板）", 20, 170, 380, 50))
p3.append(v("c8", "up", LEAF(), "使用者 just vendor_kit diff（三方：基準、新版模板、你的檔）\n看完跟進 → just vendor_kit accept <repo> 存新基準（第 5 頁）", 20, 240, 380, 56).replace("fontSize=14", "fontSize=12"))
p3.append(v("c9", "up", LEAF(), "提交變更（有改才提交）", 20, 320, 380, 40))
p3.append(v("c10n", "up", NOTE, "Renovate 路徑／just vendor_kit upgrade 路徑／vendor_kit 自身升級各自的步驟與待決處：第 11 頁", 20, 380, 380, 40))
p3.append(e("c11", "c5", "c6"))
p3.append(e("c12", "c6", "c7"))
p3.append(e("c13", "c7", "c8"))
p3.append(e("c14", "c8", "c9"))
p3.append(v("c16", "1", NOTE, "升級程式在新版 image 裡，不在專案的舊腳本裡，\n所以不會有「舊工具幫自己升級」的問題。", 490, 100, 290, 60))
p3.append(v("rb", "1", SW(NEUTRAL), "回退（詳見第 11 頁 D）", 490, 230, 290, 190))
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
p3.append(v("dev", "1", SW(NEUTRAL, 15), "本機開發模式（改工具本身時，免出 image）", 800, 510, 420, 330))
p3.append(v("c31", "dev", LEAF(), "just vendor_kit dev <repo> ../tool\n→ 寫 .version.local（不進 git）：<repo> = \"path:../tool\"", 20, 50, 380, 50).replace("fontSize=14", "fontSize=12"))
p3.append(v("c32", "dev", LEAF(), "之後每次 just：用 vendor_kit image 把 ../tool/dist 掛進來當 dist 安裝\n印記第一行寫 dev:../tool", 20, 115, 380, 50).replace("fontSize=14", "fontSize=12"))
p3.append(v("c33", "dev", LEAF(), "看到 dev: 就不做完整性檢查，只印醒目警告、重新複製 dist", 20, 180, 380, 50).replace("fontSize=14", "fontSize=12"))
p3.append(v("c34", "dev", LEAF(), "just vendor_kit undev <repo> → 刪那行、立即用 .version 的正式 image 重裝", 20, 245, 380, 50).replace("fontSize=14", "fontSize=12"))
p3.append(e("c35", "c31", "c32")); p3.append(e("c36", "c32", "c33")); p3.append(e("c37", "c33", "c34"))
p3 += legend_flow("p3", 40, 880, purple=False, startend=False, err=False, note=True)
p3 += terms("p3", 40, 990, [
 ("模板 / dist", "dist = 工具要出貨的檔案，整批放進 .<repo>/；模板 = dist 裡給初始檔用的樣板，diff 拿新版模板跟你的檔案比"),
 ("掛進來 / 完整性檢查", "掛進來 = 把本機的 dist 資料夾直接接進容器當作 image 內的 dist（改了馬上生效）／完整性檢查 = verify 比對 .<repo>/ 有沒有被改，本機模式下跳過只印警告"),
 ("三方", "diff 比的三份：基準（上次確認過的模板）、新版模板、你的檔；才能分出工具改了什麼、你改了什麼"),
 ("印記", ".<repo>/.stamp：第一行 = 裝的是哪個 image；本機開發時寫 dev:<路徑>"),
 ("dev / undev", "just vendor_kit dev <repo> <路徑> = 把工具指到本機原始碼（寫 .version.local）；just vendor_kit undev <repo> = 移除那行、回正式版；兩者的形式待回覆（第 9 頁）"),
 ("Renovate / just vendor_kit upgrade / vendor_kit", "自動開 PR 改 .version 的機器人／手動升級指令／通用安裝工具（容器內跑），第 11 頁"),
 ("commit", "git 的一次版本紀錄"),
 ("PR", "GitHub 上的合併請求；merge 就是接受這次修改"),
 ("git bisect", "git 的二分搜尋：在 .version 的修改紀錄中找出哪次升級引入問題"),
 ("image 附註", "image 上的標籤（label）：記錄它來自工具 repo 的哪個 commit、什麼版本"),
 ("digest", "image 的內容指紋（sha256:…）；同一個 digest 永遠是同一份內容"),
 (".version / 啟動器", "專案裡記工具版本的檔／專案裡的 .vendor_kit/（vendor_kit 寫出的標準 just 指令），打 just 時它負責安裝與執行"),
 ("install / diff / init.toml", "安裝子命令／升級後比對子命令／init 要建立哪些檔的清單"),
 ("工具 repo / GHCR / image", "工具的原始碼 repo／GitHub 的 image 倉庫／打包好可執行的檔案包"),
 ("<repo> / just", "<repo> = .version 裡的工具名，安裝目錄就叫 .<repo>/；just = 主機上的指令跑器，使用者打 just <指令>"),
 (".version.local / dev:", "跟 .version 同格式、不進 git 的覆蓋檔，有它那行就優先；印記第一行的 dev: 前綴 = 這個 .<repo>/ 來自本機路徑，不是正式 image"),
 ("基準 / accept", "基準 = .vendor_kit/baseline/<repo>/ 裡上次確認過的模板副本；just vendor_kit accept <repo> = 看完差異後把新版模板存成基準"),
])

# ================= Page 5: 流程：vendor_kit 內部 =================
p4 = [v("title", "1", TITLE, "流程：vendor_kit 內部——五個子命令（install 是核心）；全部在容器內執行；bootstrap 見第 10 頁", 40, 20, 1200, 30)]
p4.append(v("p4_pend", "1", PEND, "⚠ 待你回覆：1. 主機腳本執行到一半時 .<repo>/ 被另一個 just 換掉：第一版不防、寫進限制？\n2. install 進行中 .version 被改（另一邊 git checkout）：照原本讀到的版本裝完？", 1260, 4, 800, 50))
# install
p4.append(v("install", "1", SW(NEUTRAL), "install（核心：把 dist/ 放進 .<repo>/）", 20, 60, 460, 1070))
p4.append(v("l0", "install", ELLIPSE(GREEN), "開始 install", 250, 50, 160, 50))
p4.append(v("l1", "install", LEAF(), "對專案目錄上鎖（排他）\n拿不到：等最多 60 秒（可調；設 0 = 立即失敗）", 205, 130, 250, 50).replace("fontSize=14", "fontSize=12"))
p4.append(v("l1q", "install", RHOMBUS, "拿到鎖？", 240, 210, 180, 80))
p4.append(v("l_err", "install", ELLIPSE(RED), "逾時或鎖不支援：中止，\n不動任何檔（可用環境變數\n強制不鎖，風險自負）", 15, 325, 190, 70).replace("fontSize=14", "fontSize=12"))
p4.append(v("l2", "install", LEAF(), "重讀版本檔與印記第一行", 230, 330, 200, 40))
p4.append(v("l3", "install", RHOMBUS, "印記已是\n目標版本？", 240, 400, 180, 80))
p4.append(v("l_skip", "install", LEAF(), "跳過複製（別人剛裝好）\n仍做一次 verify 比對", 15, 520, 190, 50).replace("fontSize=14", "fontSize=12"))
p4.append(v("l4", "install", LEAF(), "清殘留：刪 .<repo>.tmp.*；\n改到旁邊的舊目錄先改回來", 220, 516, 220, 46).replace("fontSize=14", "fontSize=12"))
p4.append(v("l5", "install", LEAF(), "複製 dist/ 到亂數名暫存目錄", 230, 590, 200, 40))
p4.append(v("l6", "install", LEAF(), "寫印記（--self 的版本＋每檔指紋）", 230, 660, 200, 40).replace("fontSize=14", "fontSize=12"))
p4.append(v("l7", "install", LEAF(), "舊 .<repo>/ 改名到旁邊 →\n暫存目錄改名為 .<repo>/ → 刪舊", 210, 725, 240, 70).replace("fontSize=14", "fontSize=12"))
p4.append(v("l8", "install", LEAF(), "釋放鎖", 230, 820, 200, 40))
p4.append(v("l9", "install", ELLIPSE(GREEN), "成功結束", 250, 890, 160, 40))
p4.append(v("ln", "install", NOTE, "任一步失敗即中止：改名前失敗 → 舊 .<repo>/ 原封不動；兩次改名之間中斷 → 下次 install「清殘留」那步先把旁邊的舊目錄改回來再重裝。失敗時啟動器不會執行 .<repo>/ 內的腳本。\n支援平台：Linux（含 WSL2）amd64／arm64。", 30, 950, 400, 90))
p4.append(e("le0", "l0", "l1")); p4.append(e("le1", "l1", "l1q"))
p4.append('<mxCell id="le_err" value="否" style="' + EDGE + 'align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="install" source="l1q" target="l_err"><mxGeometry x="0.4" relative="1" as="geometry"><Array as="points"><mxPoint x="110" y="250"/></Array></mxGeometry></mxCell>')
p4.append(e("le2", "l1q", "l2", "是", (0.5, 1), (0.5, 0), vert=True))
p4.append(e("le3", "l2", "l3"))
p4.append('<mxCell id="le_skip" value="是" style="' + EDGE + 'align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="install" source="l3" target="l_skip"><mxGeometry x="0.4" relative="1" as="geometry"><Array as="points"><mxPoint x="110" y="440"/></Array></mxGeometry></mxCell>')
p4.append(e("le4", "l3", "l4", "否", (0.5, 1), (0.5, 0), vert=True))
p4.append(e("le5", "l4", "l5")); p4.append(e("le6", "l5", "l6")); p4.append(e("le7", "l6", "l7")); p4.append(e("le8", "l7", "l8")); p4.append(e("le9", "l8", "l9"))
p4.append('<mxCell id="le_skip2" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="install" source="l_skip" target="l8"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="110" y="840"/></Array></mxGeometry></mxCell>')
# init
IX = 500
p4.append(v("init", "1", SW(NEUTRAL), "init（第一次：建立使用者檔＋存基準）", IX, 60, 480, 810))
p4.append(v("i0", "init", ELLIPSE(GREEN), "開始 init", 160, 50, 160, 50))
p4.append(v("i1", "init", LEAF(), "讀 init.toml", 140, 130, 200, 40))
p4.append(v("i2", "init", RHOMBUS, "還有項目？", 150, 200, 180, 80))
p4.append(v("i3", "init", LEAF(), "取下一項\n（image 內由 src 指定的檔 → 專案內的 dest）", 80, 312, 320, 56))
p4.append(v("i4", "init", RHOMBUS, "dest 已存在？", 150, 390, 180, 80))
p4.append(v("i5", "init", LEAF(), "警告：已存在，不覆蓋\n（仍把這版模板存成基準）", 40, 510, 180, 50).replace("fontSize=14", "fontSize=12"))
p4.append(v("i6", "init", LEAF(), "從 dist/ 複製建立\n＋ 存一份到基準", 260, 510, 180, 50).replace("fontSize=14", "fontSize=12"))
p4.append(v("i8", "init", LEAF(), "繼續下一項", 140, 600, 200, 36))
p4.append(v("i7", "init", ELLIPSE(GREEN), "成功結束", 160, 670, 160, 40))
p4.append(v("in", "init", NOTE, "dest 已被另一個工具的 init.toml 用到 → 報錯中止（兩個工具不能搶同一個檔）\n基準 = .vendor_kit/baseline/<repo>/", 30, 725, 420, 64))
p4.append(e("ie0", "i0", "i1")); p4.append(e("ie1", "i1", "i2"))
p4.append(e("ie2", "i2", "i3", "有", (0.5, 1), (0.5, 0), vert=True))
p4.append(e("ie3", "i3", "i4"))
p4.append(e("ie4", "i4", "i5", "已有", (0, 0.5), (0.5, 0), vert=True))
p4.append(e("ie5", "i4", "i6", "沒有", (1, 0.5), (0.5, 0), vert=True))
p4.append('<mxCell id="ie6" value="沒有了" style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i2" target="i7"><mxGeometry x="-0.85" relative="1" as="geometry"><Array as="points"><mxPoint x="460" y="240"/><mxPoint x="460" y="690"/></Array></mxGeometry></mxCell>')
p4.append(e("ib1", "i5", "i8", "", (0.5, 1), (0.25, 0)))
p4.append(e("ib2", "i6", "i8", "", (0.5, 1), (0.75, 0)))
p4.append('<mxCell id="ib3" value="" style="' + EDGE + 'exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i8" target="i2"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="15" y="618"/><mxPoint x="15" y="240"/></Array></mxGeometry></mxCell>')
# verify
VX2 = 1000
p4.append(v("verify", "1", SW(NEUTRAL), "verify（每次 just 前的守門）", VX2, 60, 460, 720))
p4.append(v("v0", "verify", ELLIPSE(GREEN), "開始 verify", 150, 50, 160, 50))
p4.append(v("v1", "verify", LEAF(), "對專案目錄上鎖（共享；逾時同 install）\n讀印記第一行（已裝版本）", 90, 125, 280, 50).replace("fontSize=14", "fontSize=12"))
p4.append(v("v2", "verify", RHOMBUS, "印記第一行 = 啟動器\n給的 .version 字串？", 130, 200, 200, 80).replace("fontSize=14", "fontSize=12"))
p4.append(v("v3", "verify", LEAF(), "比對兩棵樹：image 內 dist vs .<repo>/\n檔案集合（只豁免 .stamp）、內容指紋、\n檔案種類、執行位（該可執行的仍可執行）", 110, 320, 240, 76).replace("fontSize=14", "fontSize=12"))
p4.append(v("v4", "verify", RHOMBUS, "完全一致？", 140, 425, 180, 80))
p4.append(v("v_bad1", "verify", LEAF(), "結束：版本不符，\n回報啟動器改跑 install", 15, 560, 140, 50).replace("fontSize=14", "fontSize=11"))
p4.append(v("v_ok", "verify", ELLIPSE(GREEN), "通過（釋放鎖）", 160, 560, 140, 50).replace("fontSize=14", "fontSize=12"))
p4.append(v("v_bad2", "verify", ELLIPSE(RED), "失敗：列出缺／多／\n被改的檔，中止", 325, 560, 130, 60).replace("fontSize=14", "fontSize=11"))
p4.append(v("vn", "verify", NOTE, "多餘的檔也算失敗：.<repo>/ 是整批替換的目錄，不該有別的東西。失敗不自動重裝（會無聲毀掉手改），提示刪掉重跑 just。", 20, 640, 420, 50))
p4.append(e("ve0", "v0", "v1")); p4.append(e("ve1", "v1", "v2"))
p4.append('<mxCell id="ve_b1" value="否" style="' + EDGE + 'exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="verify" source="v2" target="v_bad1"><mxGeometry x="-0.8" relative="1" as="geometry"><Array as="points"><mxPoint x="85" y="240"/></Array></mxGeometry></mxCell>')
p4.append(e("ve2", "v2", "v3", "是", (0.5, 1), (0.5, 0), vert=True))
p4.append(e("ve3", "v3", "v4"))
p4.append(e("ve4", "v4", "v_ok", "是", (0.5, 1), (0.5, 0), vert=True))
p4.append('<mxCell id="ve_b2" value="否" style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="verify" source="v4" target="v_bad2"><mxGeometry x="-0.6" relative="1" as="geometry"><Array as="points"><mxPoint x="390" y="465"/></Array></mxGeometry></mxCell>')
# diff
DX = 1480
p4.append(v("diff", "1", SW(NEUTRAL), "diff（升級後：三方比對，只印不改）", DX, 60, 560, 650))
p4.append(v("d0", "diff", ELLIPSE(GREEN), "開始 diff", 80, 50, 160, 50))
p4.append(v("d1", "diff", RHOMBUS, "有基準？（baseline/<repo>/\n存在且指紋相符）", 30, 130, 260, 80).replace("fontSize=14", "fontSize=12"))
p4.append(v("d2", "diff", LEAF(), "對每個初始檔分類：沒人改／只有工具改／\n只有你改／兩邊都改／你已套上相同內容", 20, 250, 280, 60).replace("fontSize=14", "fontSize=12"))
p4.append(v("d_two", "diff", LEAF(), "二方：新版模板 vs 你的檔\n提示「無基準或基準被改」\n結束狀態 0 沒差異／1 有差異（分不出誰改）", 320, 250, 220, 76).replace("fontSize=14", "fontSize=12"))
p4.append(v("d3", "diff", LEAF(), "印兩份：基準→新版（工具改了）、基準→你的（你改了）\n同一檔兩邊都有改 → 標「可能重疊」（不判定是否同一行）", 20, 345, 280, 76).replace("fontSize=14", "fontSize=12"))
p4.append(v("d_code", "diff", LEAF(), "算結束狀態：0 = 沒人改／只有你改／已套上；\n1 = 有「只有工具改」；2 = 有「兩邊都改」", 20, 445, 280, 50).replace("fontSize=14", "fontSize=12"))
p4.append(v("d4", "diff", ELLIPSE(GREEN), "結束（不改任何檔）", 80, 520, 160, 50))
p4.append(v("dn", "diff", NOTE, "第一版只做「哪個檔誰改了」；「同一行有沒有衝突」的精確判定第二版再做。", 20, 595, 520, 40))
p4.append(e("de0", "d0", "d1"))
p4.append(e("de1", "d1", "d2", "有", (0.5, 1), (0.5, 0), vert=True))
p4.append(e("de2", "d1", "d_two", "沒有／被改", (1, 0.5), (0.5, 0)))
p4.append(e("de3", "d2", "d3")); p4.append(e("de4", "d3", "d_code")); p4.append(e("de4b", "d_code", "d4"))
p4.append('<mxCell id="de5" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="diff" source="d_two" target="d4"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="430" y="545"/></Array></mxGeometry></mxCell>')
# accept
AX = 2060
p4.append(v("accept", "1", SW(NEUTRAL), "accept（看完 diff 後：新版模板存成基準）", AX, 60, 420, 600))
p4.append(v("a0", "accept", ELLIPSE(GREEN), "開始 accept", 130, 50, 160, 50))
p4.append(v("a1", "accept", LEAF(), "對專案目錄上鎖（排他；\n逾時規則同 install）", 110, 130, 200, 40).replace("fontSize=14", "fontSize=12"))
p4.append(v("a2", "accept", LEAF(), "取 image 內的新版模板\n（init.toml 列的檔）", 110, 200, 200, 50))
p4.append(v("a3", "accept", LEAF(), "寫進 .vendor_kit/baseline/<repo>/\n＋ 記下是哪個 image、每檔指紋", 100, 280, 220, 60).replace("fontSize=14", "fontSize=12"))
p4.append(v("a4", "accept", LEAF(), "釋放鎖", 110, 370, 200, 40))
p4.append(v("a5", "accept", ELLIPSE(GREEN), "結束（基準 = 這版）", 110, 440, 200, 50))
p4.append(v("an", "accept", NOTE, "語意：「這版我全看過了」。寫的是新版模板，不是你的檔；\ndiff 結尾只提示、不會問你。", 20, 520, 380, 50))
p4.append(e("ae0", "a0", "a1")); p4.append(e("ae1", "a1", "a2")); p4.append(e("ae2", "a2", "a3")); p4.append(e("ae3", "a3", "a4")); p4.append(e("ae4", "a4", "a5"))
p4.append(v("p4n", "1", NOTE, "已定案：verify 比 image 內的 dist 而不是印記（issue #23）；diff 三方（#22）；install／verify／accept 對專案目錄上鎖（#24）。本機開發模式見第 4 頁（#21）。", 20, 1150, 1500, 40))
p4 += legend_flow("p4", 40, 1210, purple=False, note=True)
p4 += terms("p4", 40, 1320, [
 ("暫存目錄", "先把整個 dist/ 寫到 .<repo>.tmp.<亂數>/，最後一步才改名成 .<repo>/；中途失敗舊目錄不受影響"),
 ("鎖（排他／共享）", "對專案目錄上鎖（flock）：排他 = 同時只有一個（install、accept）；共享 = 可多個一起但要等排他的放開（verify）。程序結束或被殺，系統自動解鎖，不會留殘鎖"),
 ("兩棵樹比對", "把 image 內的 /dist 跟 .<repo>/ 逐檔比：檔案集合（缺、多）、內容指紋 sha256、執行位（單向：該可執行的仍可執行，Windows 掛載才不誤報）、型別（symlink 第一版禁止）"),
 ("印記 / --self", "印記 = .<repo>/.stamp，第一行 = 啟動器用 --self 傳進來的 .version 字串，之後每檔指紋（追溯用）；verify 只用第一行判斷要不要重裝"),
 ("基準 / accept", "基準 = .vendor_kit/baseline/<repo>/：上次確認過的模板副本＋來源版本與每檔指紋；accept = 把新版模板寫成基準的子命令"),
 ("三方 / 二方", "三方 = 基準、新版模板、你的檔三份一起比，能分出誰改了什麼；二方 = 只比新版模板跟你的檔（沒基準時的退路）"),
 ("可執行 / 檔案種類 / 記下是哪個 image", "可執行 = 檔案有「可以直接執行」的標記（腳本要有）／種類 = 一般檔、資料夾、連結（symlink，第一版不准）／基準旁邊記的來源 image 與每檔指紋"),
 ("環境變數", "跑指令前設定的名稱=值，用來改預設行為：例如鎖的等待秒數、強制不鎖"),
 ("結束狀態", "程式結束時回報的數字；diff 用 0 沒差異／1 工具有改／2 可能重疊，給 CI 判斷"),
 ("src → dest", "init.toml 每一項：src 指 image 的 dist/ 裡哪個檔，dest 指要放到專案的哪裡"),
 ("vendor_kit / image / dist", "安裝工具本身／打包好可執行的檔案包／工具要出貨的檔案"),
 ("init.toml / 啟動器", "init 要建立哪些檔的清單／專案裡的 .vendor_kit/ 標準指令（使用者打 just 時執行）"),
 ("容器 / <repo>", "容器 = image 執行起來的實例；<repo> = .version 裡的工具名，安裝目錄就叫 .<repo>/"),
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
p7.append(v("r_tool_n", "r_tool", TEXT(11), "Dockerfile.dist：FROM scratch（空白），只放 dist/ 與 init.toml", 10, 190, 280, 50))
p7.append(v("ghcr", "1", SW(YELLOW), "image 存放處", 640, 100, 300, 490))
p7.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:v1", 40, 70, 220, 50))
p7.append(v("g_tool", "ghcr", PURPLE_LEAF, "<repo>-dist:v0.1.0", 40, 370, 220, 50))
p7.append(v("g_n", "ghcr", TEXT(11), "原型：本機 Docker 快取；正式版：CI 在打 tag 時 push 到 GHCR", 10, 450, 280, 40))
p7.append(v("r_proj", "1", SW(GREEN), "專案 repo", 1080, 100, 340, 490))
p7.append(v("r_proj_t", "r_proj", TEXT(11), "= proto/project/", 10, 40, 320, 18))
p7.append(v("f_ver", "r_proj", LEAF(), ".version", 20, 70, 140, 40))
p7.append(v("f_just", "r_proj", LEAF(), "justfile", 180, 70, 140, 40))
p7.append(v("f_user", "r_proj", LEAF(), "Dockerfile、設定檔（setup.toml）…\n（init 建立後歸使用者）", 20, 120, 300, 50))
p7.append(v("f_land", "r_proj", LEAF(), ".<repo>/（含 .stamp 印記檔）\n（不進 git，install 寫出）", 20, 370, 300, 50))
p7.append(v("r_proj_n", "r_proj", TEXT(11), ".version 兩種行：引擎版本一行、每個工具一行；\n工具 image 與引擎 image 各自獨立升級", 10, 450, 320, 36))
p7.append(e("x1", "f_vkdf", "g_vk", "建置成 image", (1, 0.5), (0, 0.5), offset=(0, -4)))
p7.append(e("x2", "f_tdf", "g_tool", "建置成 image", (1, 0.5), (0, 0.5), offset=(0, -4)))
p7.append(e("x4", "g_tool", "f_land", "檔案：docker cp 抓出 → 引擎 install 寫入", (1, 0.75), (0, 0.75), pos=0.2))
p7.append(e("x6", "g_vk", "f_land", "引擎（跑 install / verify）", (1, 0.5), (0, 0.3)))
p7.append(e("x5b", "f_ver", "g_vk", "指定引擎版本", (0, 0.625), (1, 0.5), pos=-0.6))
p7.append(e("x5", "f_ver", "g_tool", "指定用哪個 image", (0, 0.5), (1, 0.15), pos=-0.6))
p7 += legend("p7", 40, 640, ["red", "green", "yellow", "pimg", "white"], "實線 = 傳輸內容")
p7 += terms("p7", 40, 750, [
 ("proto/", "可執行的原型：三個資料夾各對應框架裡的一個角色；image 只 build 到本機，沒有 push"),
 ("<repo>", "工具名的占位符。原型不是真實工具，直接用 tool 當占位值：image 叫 tool-dist、目錄叫 .tool/"),
 (".stamp", "印記檔：install 寫下的「版本 + 每檔指紋」"),
 ("setup.toml", "範例工具給專案的設定檔（TOML）"),
 ("GHCR / image / CI", "GitHub 的 image 倉庫／打包好可執行的檔案包／打 tag 時自動 build 並 push 的流程"),
 (".version / justfile / init.toml", "專案記工具版本的檔／專案的指令入口（啟動器）／工具給的初始檔清單"),
 ("Dockerfile / Dockerfile.dist / FROM scratch", "打包 image 的食譜／工具 repo 出貨用的食譜／從空白開始、只放檔案（工具 image 不含任何程式）"),
 ("dist / 模板 / tag", "工具要出貨的檔案／dist 裡給初始檔用的樣板／image 的版本名稱"),
 ("建置 / 上傳 / 指紋 / TOML", "把食譜做成 image（docker build）／把 image 放到倉庫（docker push）／由檔案內容算出的識別碼／設定檔格式"),
])



# ================= Page 7: 資料夾架構 =================
p10 = [v("title", "1", TITLE, "資料夾架構：三種 repo 裡各有什麼、每個資料夾放什麼類型的東西", 40, 20, 1200, 30)]
FOLDER = LEAF() + "align=left;spacingLeft=8;fontFamily=Courier New;"
FILEB = FILE + "align=left;spacingLeft=8;fontFamily=Courier New;"
DESC = TERM_V
IND, RH = 26, 42
def tree(prefix, parent, x, y, nw, dw, rows):
    """rows: (depth, name, is_file, 用途)。資料夾 = 實線框；檔案 = 虛線框；右欄 = 用途／放什麼類型的東西"""
    for i, (d, name, is_file, desc) in enumerate(rows):
        yy = y + i * RH
        p10.append(v(f"{prefix}_n{i}", parent, (FILEB if is_file else FOLDER).replace("fontSize=14", "fontSize=12"), name, x + d * IND, yy, nw - d * IND, RH - 4))
        p10.append(v(f"{prefix}_d{i}", parent, DESC, desc, x + nw + 10, yy, dw, RH - 4))
    return y + len(rows) * RH
# vendor_kit repo
VK = [
 (0, "vendor_kit/", False, "我們要開發的安裝工具的 repo；只有 src/ 與 test/ci/check.sh 會進最終出貨的 image，其餘都是開發用"),
 (1, "src/vendor_kit/", False, "產品程式碼：第 1 頁的模組，一個模組一個檔＋ 進入點"),
 (2, "__main__.py", True, "進入點：容器啟動時跑 python3 -m vendor_kit → 交給 cli"),
 (2, "cli.py", True, "命令介面：讀參數、分派 install / init / verify / diff / accept / upgrade（另有 bootstrap，第 10、11 頁）"),
 (2, "dist_reader.py", True, "出貨內容讀取：讀 image 內的 /dist 與 init.toml"),
 (2, "repo_fs.py", True, "專案檔案存取：唯一能寫專案目錄的模組；整批替換、專案目錄鎖（flock）、讀寫基準都在這"),
 (2, "treediff.py", True, "規劃中（尚未寫，也還沒算進模組數與鏡射測試）：兩棵樹比對（image 內 dist vs .<repo>/），install、verify、release-test 共用"),
 (2, "template.py  stamp.py  diff.py  report.py", True, "純函式（只算結果、不碰檔案）：模板、印記（指紋）、差異比對（三方分類）、回報"),
 (1, "test/", False, "所有測試與檢查；smoke／lint／unit／integration 只進測試用的 stage，system／acceptance 在 CI 主機跑；除 ci/check.sh 外都不進出貨 image"),
 (2, "env/check.sh", True, "環境檢查（smoke）：shell 腳本，確認 image 內 Python、tomllib、進入點都能跑"),
 (2, "ci/check.sh", True, "給下游專案用的契約檢查腳本（第 12 頁）：唯一會 COPY 進出貨 image 的測試檔，bootstrap 寫到專案的 test/ci/check.sh，GitHub／GitLab 的 CI 只呼叫它"),
 (2, "lint/ruff/  lint/import-linter/", False, "檢查工具的設定檔：Python 寫法規則、模組分層契約"),
 (2, "lint/mirror_check.py  blackbox_check.py", True, "自寫的檢查腳本：鏡射（每模組必有測試）、黑箱（system/acceptance 測試不准引用 vendor_kit 程式）"),
 (2, "pytest/unit/", False, "單元測試：test_<模組>.py ×7 + conftest.py（禁碰檔案、網路）"),
 (2, "pytest/integration/", False, "子命令測試：test_<子命令>.py ×4 + 時間預算 + conftest.py（禁 Docker）"),
 (2, "pytest/system/", False, "整個 image 測試：docker run 每個子命令（CI 主機跑）"),
 (2, "pytest/acceptance/", False, "驗收測試：在假專案裡真的打 just（CI 主機跑）"),
 (2, "fixtures/", False, "測試用假資料：假 dist/、init.toml、VERSION、假專案（project/）、假工具 image 食譜（tool_image/）"),
 (1, "docs/adr/", False, "設計決策紀錄：一個決策一個文字文件（例：測試分層與閘門）"),
 (1, "Dockerfile", True, "打包食譜：runtime → env-test → test-base → 各測試 stage；runtime → release（第 8 頁）"),
 (1, "docker-bake.hcl", True, "一次跑多個 stage 的清單：group validate（測試）、group release（出貨）"),
 (1, ".github/workflows/ci.yaml", True, "CI：推送就跑 bake validate → system/acceptance → bake release"),
]
p10.append(v("r_vk", "1", SW(RED), "vendor_kit repo（我們開發的）", 40, 70, 1000, 50 + len(VK) * RH + 20))
tree("vk", "r_vk", 20, 50, 400, 560, VK)
# 工具 repo
TL = [
 (0, "<repo>/", False, "任何要透過 vendor_kit 出貨的工具的原始碼 repo"),
 (1, "dist/", False, "要出貨的全部（腳本、Dockerfile 範本、模板、hooks 空殼），整包裝進專案的工具目錄"),
 (1, "init.toml", True, "清單：dist/ 裡哪些檔在 init 時要再複製到專案哪裡（TOML）"),
 (1, "Dockerfile.dist", True, "出貨食譜：FROM vendor_kit，疊上 dist/ 與 init.toml → <repo>-dist image"),
 (1, ".github/workflows/", False, "CI：打 tag 時建置 <repo>-dist image 並上傳 GHCR"),
 (1, "doc/  test/  …", False, "工具自己的文件、測試等；不在 dist/ 裡，不會出貨"),
]
p10.append(v("r_tool", "1", SW(GREEN), "工具 repo（每個工具一個）", 1080, 70, 760, 50 + len(TL) * RH + 20))
tree("tl", "r_tool", 20, 50, 300, 420, TL)
# 專案 repo
PJ = [
 (0, "<專案>/", False, "使用工具的專案；使用者天天工作的地方"),
 (1, ".version", True, "進 git｜工具版本清單：一行一個工具 <repo> = \"image\""),
 (1, "justfile", True, "進 git｜使用者的指令清單：第一行 mod? vendor_kit '.vendor_kit/vendor.just'，其餘自己加（第 9 頁）"),
 (1, ".vendor_kit/", False, "進 git｜啟動器本體：vendor.just、tools.just、.stamp（vendor_kit 寫出，人不改，升級只換這三個）"),
 (2, "baseline/<repo>/", False, "進 git｜三方比對的基準：init／accept 存的模板副本＋記下是哪個 image；人不改（diff 前檢查指紋）；升級不動"),
 (1, ".version.local", True, "不進 git｜本機開發用的覆蓋檔：<repo> = \"path:../tool\"，有它那行就優先（第 4 頁）；平常沒有這個檔"),
 (1, "Dockerfile  setup.toml  …", True, "進 git｜使用者檔案：init 從模板建立，之後歸使用者維護"),
 (1, "script/hooks/", False, "進 git｜使用者的掛勾腳本：每個工具指令前後自動執行（init 建立的空殼）"),
 (1, "test/ci/check.sh", True, "進 git｜契約檢查腳本（bootstrap 寫出，之後歸專案）：GitHub／GitLab 的 CI 只呼叫它（第 12 頁）"),
 (1, "renovate.json", True, "進 git｜Renovate 設定（bootstrap 寫出）：只含 extends，指向 vendor_kit 的共用 preset（第 11 頁 A）"),
 (1, ".<repo>/", False, "不進 git｜工具的 dist/ 整包 + .stamp 印記；每次升級整批換新，不可手改"),
 (1, ".<repo2>/", False, "不進 git｜另一個工具的，同上"),
]
ty = 70 + 50 + len(TL) * RH + 20 + 30
p10.append(v("r_proj", "1", SW(GREEN), "專案 repo（使用工具的）", 1080, ty, 760, 50 + len(PJ) * RH + 20))
tree("pj", "r_proj", 20, 50, 300, 420, PJ)
p10 += legend("p10", 40, 70 + 50 + len(VK) * RH + 20 + 40, ["red", "green", "folder", "filebox"], "右欄 = 用途／放什麼類型的東西")
p10 += terms("p10", 40, 70 + 50 + len(VK) * RH + 20 + 150, rh=36, rows=[
 ("repo", "一個 git 管理的專案資料夾；這頁的三種：我們開發的、工具的、使用工具的專案"),
 ("進 git／不進 git", "進 git = 這個檔會被版本管理、跟著 repo 走；不進 git = 不由 git 保存、只在這台機器（.<repo>/ 隨時可刪掉重裝；.version.local 是你自己的本機設定）"),
 ("image", "打包好可執行的檔案包；vendor_kit repo 只有 src/ 與 test/ci/check.sh 會進最終出貨的 image，其他測試只進測試用的 stage 或在 CI 主機跑"),
 ("TOML / tomllib / pytest", "設定檔格式（.version、init.toml）／Python 讀 TOML 的內建程式庫／Python 測試框架"),
 ("VERSION", "image 內給人看的識別字串（印記第一行改由啟動器用 --self 傳入的 .version 字串，issue #23）"),
 ("ruff / import-linter", "Python 寫法檢查／檢查模組之間誰能引用誰"),
 ("鏡射 / 黑箱 / 記下是哪個 image", "每個模組必有對應測試檔／system、acceptance 測試不准引用 vendor_kit 程式／基準旁邊記的來源 image 與每檔指紋"),
 ("tag / GHCR", "tag = 給 repo 打的版本記號（v1.2.0），CI 看到就出貨／GHCR = GitHub 的 image 倉庫"),
 ("hooks", "掛勾腳本：每個工具指令前（pre）後（post）自動執行的使用者腳本，init 建立空殼"),
 ("原子替換 / 純函式 / 引用", "整批一次換掉，不會出現半新半舊／只算結果、不碰檔案與網路的程式／一個程式 import（引用）另一個程式"),
 ("測試層級名稱", "smoke = 環境能跑；lint = 不執行的檢查；unit = 單一模組；integration = 一個子命令走到底；system = 整個 image；acceptance = 真的打 just（第 8 頁）"),
 ("conftest.py / fixtures", "pytest 每個目錄的共用設定（這裡用來強制限制）／測試用的假資料"),
 ("ADR", "設計決策紀錄（Architecture Decision Record）：為什麼這樣決定，一個檔一個決策"),
 ("Dockerfile / stage / bake", "打包 image 的食譜／食譜裡的一個階段／一次建多個階段的清單工具"),
 ("CI", "GitHub 上的自動化流程：推送或打 tag 時自動跑測試、建置、上傳"),
 ("dist/ / init.toml / .stamp", "工具要出貨的檔案／init 要複製哪些初始檔的清單／印記檔（裝了哪個 image + 每檔指紋）"),
 ("<repo> / just", "工具名（= .version 的 key，安裝目錄 .<repo>/）／主機上的指令跑器"),
 ("install / init / verify / diff / accept / bootstrap", "vendor_kit 的子命令：把 dist 裝進 .<repo>/ 並寫印記／建立初始檔＋存基準／拿 .<repo>/ 跟 image 內的 dist 比／三方比對新版模板／存新基準／第一次寫出啟動器（第 10 頁）"),
 ("基準（baseline） / flock", "上次確認過的模板副本，diff 用它分出誰改了什麼／Linux 的檔案鎖，程序結束自動解鎖"),
])

# ================= Page 7: repo 結構與測試分層 =================
p8 = [v("title", "1", TITLE, "測試分層與強制閘門：test/ 的每一層 → Dockerfile stage → 由什麼強制（環境檢查先於一切）", 40, 20, 1300, 30)]
COLH = 1150
# 欄 1：repo 目錄
p8.append(v("repo", "1", SW(RED), "vendor_kit repo（測試相關）", 40, 70, 420, COLH))
p8.append(v("d_note", "repo", TEXT(11), "完整資料夾架構見第 7 頁", 20, 1122, 380, 18))
p8.append(v("d_src", "repo", SW(RED, 16), "src/vendor_kit/（第 1 頁的 7 個模組）", 20, 50, 380, 140))
MODS = [("cli", "命令介面"), ("dist_reader", "出貨內容讀取"), ("repo_fs", "專案檔案存取"), ("template", "模板"),
        ("stamp", "印記"), ("diff", "差異比對"), ("report", "回報")]
for i, (m, zh) in enumerate(MODS):
    p8.append(v(f"m_{m}", "d_src", LEAF().replace("fontSize=14", "fontSize=11"), f"{m}.py\n{zh}", 12 + (i % 4) * 92, 45 + (i // 4) * 46, 86, 40))
p8.append(v("d_test", "repo", SW(NEUTRAL), "test/（先分測試工具、再分層級）", 20, 200, 380, 703))
TW = 356
S12 = '.replace("fontSize=14", "fontSize=12")'
p8.append(v("t_env", "d_test", LEAF(), "env/check.sh\n環境檢查：Python、tomllib、進入點、toml-bridge 都能跑", 12, 45, TW, 44).replace("fontSize=14", "fontSize=12"))
p8.append(v("t_fix", "d_test", LEAF(), "fixtures/\n假的 dist/、init.toml、VERSION、假專案", 12, 110, TW, 44))
p8.append(v("t_lint", "d_test", LEAF(), "lint/{ruff, import-linter}/ + mirror_check.py + blackbox_check.py\n寫法檢查、import 分層契約、鏡射檢查、黑箱檢查", 12, 207, TW, 44).replace("fontSize=14", "fontSize=12"))
p8.append(v("t_unit", "d_test", LEAF(), "pytest/unit/\ntest_<模組>.py ×7（一個模組一個檔）", 12, 262, TW, 44))
p8.append(v("t_inst", "d_test", LEAF(), "pytest/integration/test_install.py", 12, 317, TW, 44))
p8.append(v("t_init", "d_test", LEAF(), "pytest/integration/test_init.py", 12, 372, TW, 44))
p8.append(v("t_ver", "d_test", LEAF(), "pytest/integration/test_verify.py\n＋ test_perf_verify.py（時間預算）", 12, 427, TW, 44))
p8.append(v("t_diff", "d_test", LEAF(), "pytest/integration/test_diff.py", 12, 482, TW, 44))
p8.append(v("t_sys", "d_test", LEAF(), "pytest/system/\n整個 image：docker run 每個子命令", 12, 537, TW, 44))
p8.append(v("t_acc", "d_test", LEAF(), "pytest/acceptance/\n第 3 頁三條泳道：在假專案裡真的打 just", 12, 592, TW, 44))
p8.append(v("t_conf", "d_test", LEAF(), "pytest/<層級>/conftest.py\n每層的限制寫在這（見右欄）", 12, 647, TW, 44))
p8.append(v("d_df", "repo", LEAF(), "Dockerfile（中欄的 stage）", 20, 920, 180, 40))
p8.append(v("d_bake", "repo", LEAF(), "docker-bake.hcl（group）", 220, 920, 180, 40))
p8.append(v("d_adr", "repo", LEAF(), "docs/adr/\n測試分層與閘門（本頁的決策）", 20, 980, 380, 44))
p8.append(v("d_ci", "repo", LEAF(), ".github/workflows/（vendor_kit 自己的 CI）\nbake validate → system/acceptance → release（兩種架構）", 20, 1030, 380, 40).replace("fontSize=14", "fontSize=12"))
p8.append(v("d_ci2", "repo", LEAF(), "test/ci/check.sh：給下游專案的契約檢查腳本（第 12 頁）\n不在自己的 CI 序列裡；COPY 進 image 供 bootstrap 寫出", 20, 1076, 380, 40).replace("fontSize=14", "fontSize=12"))
# 欄 2：Dockerfile stage（紫：每個 stage 都是 image）
SX, SW_ = 520, 480
LX, LW = 40, 230
p8.append(v("stages", "1", SW(NEUTRAL), "Dockerfile stage（BuildKit）", SX, 70, SW_ + 20, COLH))
p8.append(v("s_rt", "stages", PURPLE_LEAF, "runtime\nFROM toml-bridge + src/", LX, 50, LW, 50))
p8.append(v("s_env", "stages", PURPLE_LEAF, "env-test（環境檢查，smoke）", LX, 247, LW, 40))
p8.append(v("s_tb", "stages", PURPLE_LEAF, "test-base = env-test + pytest + fixtures", LX, 312, LW, 40).replace("fontSize=14", "fontSize=12"))
GRP = ("swimlane;html=1;rounded=1;startSize=30;fontStyle=1;fontSize=14;container=1;collapsible=0;recursiveResize=0;"
       f"fillColor={NEUTRAL};swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=2;")
GY = 372
p8.append(v("s_grp", "stages", GRP, "六個測試 stage（都 FROM test-base）", 20, GY, 440, 364))
LX = LX - 20
for k, (sid, t) in enumerate([("s_lint", "lint"), ("s_unit", "unit-test"), ("s_inst", "install-test"), ("s_init", "init-test"), ("s_ver", "verify-test"), ("s_diff", "diff-test")]):
    p8.append(v(sid, "s_grp", PURPLE_LEAF, t, LX, 37 + 55 * k, LW, 40))
p8.append(v("s_rel", "stages", PURPLE_LEAF, "release\n= runtime（最終產物）", LX + 20, 760, LW, 50))
p8.append(v("s_rtest", "stages", PURPLE_LEAF, "release-test\nFROM release；真的 install + verify 一次", LX + 20, 850, LW, 60))
p8.append(v("s_host", "stages", TEXT(11), "system / acceptance 不在 Dockerfile 裡：\n它們要 docker run，所以在 CI 主機上跑", 20, 925, 440, 40))
p8.append(v("s_bake", "stages", TEXT(11), "docker-bake.hcl：group validate = [env-test, lint, unit-test, install-test,\ninit-test, verify-test, diff-test（accept-test 待補）]；group release = [release, release-test]", 20, 965, 440, 40))
p8.append(e("s1", "s_rt", "s_env", "FROM", (0.5, 1), (0.5, 0), vert=True))
p8.append(e("s1b", "s_env", "s_tb", "FROM（環境不對 → 到此為止）", (0.5, 1), (0.5, 0), vert=True))
p8.append(e("s2", "s_tb", "s_grp", "FROM", (0.5, 1), (0.3068, 0), vert=True))
p8.append('<mxCell id="s8" value="FROM\n（不經任何 test stage）" style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="stages" source="s_rt" target="s_rel"><mxGeometry x="0.785" relative="1" as="geometry"><Array as="points"><mxPoint x="475" y="75"/><mxPoint x="475" y="785"/></Array></mxGeometry></mxCell>')
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
    h = 30 + len(gates) * 64 + 10
    p8.append(v(gid, "gates", GSW, title, 20, y, 420, h))
    for i, (k, t) in enumerate(gates):
        p8.append(v(k, gid, LEAF().replace("fontSize=14", "fontSize=12"), t, 10, 40 + i * 64, 400, 56))
    return y + h + 10
y = 50
y = gate_group("ge", "smoke = 先確認環境能跑，再談測試（env-test stage）", y, [
    ("g0", "環境檢查先於一切\ntest-base FROM env-test：Python、tomllib、進入點、toml-bridge 任一不對，六個測試 stage 都不會跑")])
y = gate_group("gl", "lint 層 = 不執行程式的檢查（lint stage）", y, [
    ("g_ruff", "ruff\n程式碼寫法檢查"),
    ("g2", "import-linter 分層契約\n只能由上層 import 下層（命令介面 → 讀取／存取 → 純函式）；只有 repo_fs、dist_reader 能碰檔案"),
    ("g3", "鏡射檢查\n每個 src 模組必有 test_<模組>.py，缺一個就失敗")])
y = gate_group("gu", "unit 層 = 一次測一個模組（unit-test stage）", y, [
    ("g4", "unit conftest\n測試中一碰檔案、網路、Docker 就直接失敗")])
y = gate_group("gi", "integration 層 = 一個子命令走到底（一個子命令一個 stage）", y, [
    ("g5", "integration conftest\n只給臨時目錄；禁 Docker、網路、啟動其他程序（subprocess／socket 全禁）；只能走 cli.main()（程式的正門）"),
    ("g6", "一個子命令一個 stage\n各自只 COPY 自己的測試檔；哪個 stage 紅 = 第 5 頁哪條泳道壞（accept-test 待補）"),
    ("g7", "時間預算\nverify 200 個檔必須 < 0.5 秒（量容器內的函式，不含起容器；除剛 install 完與本機模式外每次 just 都跑它）")])
y = gate_group("gs", "system = 整個 image；acceptance = 真的打 just（CI 主機）", y, [
    ("g8", "黑箱檢查（lint stage）＋ conftest\n測試檔不准 import vendor_kit；只准 docker run／just 與檔案系統")])
y = gate_group("gr", "release = 出貨（release / release-test stage）", y, [
    ("g1", "BuildKit stage 依賴\nrelease 只 FROM runtime → 測試碼、pytest 進不了產品 image；release 同時 build amd64 + arm64（multi-arch）"),
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
 ("VERSION vs .version", "VERSION = image 內 /dist/VERSION：出貨時寫入、給人看的識別字串（印記第一行改由啟動器 --self 傳入的 .version 字串，issue #23）；.version = 專案 repo 記工具版本的檔"),
 ("amd64 / arm64 / multi-arch", "兩種處理器架構（一般電腦／Jetson 等 ARM 板子）；multi-arch = 同一個 image 名稱同時提供兩種版本，Docker 依主機自動選"),
 ("TOML / tomllib", "TOML = 設定檔格式（.version、init.toml 都用它）；tomllib = Python 3.11 起內建的讀 TOML 程式庫，環境檢查要確認它在"),
 ("鏡射", "test/ 的檔名跟 src/ 一一對應：src 有 cli.py，test 就必須有 test_cli.py"),
 ("黑箱", "只從外面用、不看裡面：system / acceptance 測試不准 import vendor_kit，只能像使用者一樣 docker run 或打 just"),
 ("install / init / verify / diff / accept / just", "子命令：把 dist 裝進 .<repo>/ 並寫印記／建立初始檔＋存基準／拿 .<repo>/ 跟 image 內的 dist 比／三方比對新版模板／存新基準（accept 的測試 stage 待補）；just = 使用者在主機打的指令跑器（第 3、9 頁）"),
 ("fixture / 假專案", "測試用的假資料：假的 dist/（工具要出貨的檔案）、init.toml（init 要複製哪些初始檔的清單），以及一個假專案（acceptance 測試先用 bootstrap.sh 產生 .vendor_kit/、justfile、.version）"),
 ("image / 容器 / Docker / Dockerfile", "打包好的環境／image 開起來的實例／跑它們的軟體／怎麼做 image 的食譜（每個 stage 是食譜的一段）"),
 ("cli.main()", "vendor_kit 程式的正門（命令介面的進入點）；integration 測試只准從這裡進"),
 ("docker run / CI", "把 image 跑成容器的指令／GitHub 上的自動化流程（每次推送都跑 bake validate）"),
 ("ADR / ISTQB", "設計決策紀錄（docs/adr/ 裡一個決策一個檔）／國際軟體測試標準，本頁的層級名稱來自它"),
 ("泳道", "流程圖裡的一條直欄，代表一個子命令或情境的完整流程"),
])

# ================= Page 8: 使用者介面：just 指令表 =================
p9 = [v("title", "1", TITLE, "指令表（依角色）：使用者／開發者／專案維護者／工具開發者各自會碰到的指令", 40, 20, 1300, 30)]
p9.append(v("p9_pend", "1", PEND, "⚠ 待你回覆：1. dev／undev 要改成選項式（例如 just vendor_kit upgrade --local <repo>）而不是給路徑嗎？本機路徑從哪來？\n2. 審查者建議（未改，等你決定）：A 表的 run／stop 與 B 表三欄完全相同，是否只留 B 表並標「使用者也用」？diff（B）與 accept（C）是同一人連續做的兩步，要不要放同一角色？「什麼時候打」與「使用情景」兩欄重疊，要不要合併？", 40, 55, 1460, 64))
TH = "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999999;fontSize=12;fontStyle=1;align=center;strokeWidth=1;"
TC = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=12;align=left;spacingLeft=6;strokeWidth=1;"
TCB = TC + "fontStyle=1;fontFamily=Courier New;"
COLS = [("指令", 150), ("什麼時候打", 150), ("做什麼", 245), ("背後跑什麼", 220), ("動到專案裡的什麼", 190), ("為什麼必要（沒有它會怎樣）", 245), ("使用情景（誰、多常）", 230)]
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
# A：使用者
p9.append(v("gU", "1", SW(NEUTRAL), "A. 使用者（拿專案成果來用的人）：只有「跑起來、停掉」，不 build、不 exec；工具有提供才有", 40, 140, TBW + 40, 290))
yU = table("tu", "gU", 20, 50, rh=72, rows=[
 ("just <模組> run", "要用這個專案的成果時", "啟動專案容器（在背景常駐）", ".<repo>/ 的 run 腳本 → docker compose up", "容器（不在 repo 裡）", "不啟動就沒有東西可用；不用懂 docker compose 的參數", "使用者；每次要用時一次"),
 ("just <模組> stop", "用完", "停掉並移除容器", ".<repo>/ 的 stop 腳本 → docker compose down", "容器（移除）", "釋放資源", "使用者；用完一次"),
])
# B：開發者
p9.append(v("gU_n", "gU", NOTE, "跟 B 表一樣，每個工具指令開頭都先自動檢查／安裝（just vendor_kit ensure），所以 .<repo>/、印記、tools.just 可能在指令前被更新；「動到專案裡的什麼」欄只寫指令本身動的。", 20, yU + 10, TBW, 40))
p9.append(v("gB", "1", SW(NEUTRAL), "B. 開發者（天天在專案裡寫程式的人）：工具命名空間的四個指令 ＋ 升級後看差異", 40, 460, TBW + 40, 540))
yB = table("tb", "gB", 20, 50, rh=72, rows=[
 ("just <模組> build", "第一次、或改了 Dockerfile 之後", "建置專案自己的 image", ".<repo>/ 的 build 腳本 → docker compose build", "本機 image（不在 repo 裡）", "沒有它就得自己記 docker compose 的參數與 image 名，每個人打的都不一樣", "開發者；改 Dockerfile 或第一次；每週幾次"),
 ("just <模組> run", "要開始工作時", "啟動專案容器（在背景常駐）", ".<repo>/ 的 run 腳本 → docker compose up", "容器（不在 repo 裡）", "容器不啟動就沒有開發環境", "開發者；每天開工一次"),
 ("just <模組> exec", "容器跑著的時候", "進到容器裡下指令", ".<repo>/ 的 exec 腳本 → docker compose exec", "無（前置檢查除外，見下方便條）", "編譯、測試都要在容器裡做", "開發者；每天多次"),
 ("just <模組> stop", "收工", "停掉並移除容器", ".<repo>/ 的 stop 腳本 → docker compose down", "容器（移除）", "釋放資源、切換專案", "開發者；收工，每天一次"),
 ("just vendor_kit diff", "升級之後（.version 被 merge 後）", "三方比對：印出「工具改了什麼」「你改了什麼」，不改任何檔；結束狀態 0 沒差異／1 工具有改／2 可能重疊", "vendor_kit 容器：diff", "diff 本身不動任何檔（前面的自動檢查可能先更新 .<repo>/）", "升級後不看就不知道工具改了什麼、自己的 Dockerfile 要不要跟進", "開發者；每次升級後一次（幾週一次）"),
])
p9.append(v("gB_n", "gB", NOTE, "工具指令的四個是「一個容器的一生」：做出來（build）→ 開起來（run）→ 進去用（exec）→ 關掉（stop）；由工具定義（以「容器工作流」類的工具為例），換工具就換一套；前後可掛你自己的 hooks（script/hooks/pre|post/<指令>.sh）。\n每個工具指令開頭都先自動呼叫 just vendor_kit ensure（上鎖 → 印記第一行 ≠ 有效版本 → install；相同 → verify；失敗就中止）——人不會直接打，所以 .<repo>/、印記、tools.just 可能在指令前被更新。", 20, yB + 10, TBW, 66))
# C：專案維護者
p9.append(v("gM", "1", SW(NEUTRAL), "C. 專案維護者（把工具接進專案、處理升級的人）", 40, 1030, TBW + 40, 390))
yM = table("tm", "gM", 20, 50, rh=72, rows=[
 ("bootstrap.sh\n（release 附）", "第一次把 vendor_kit 接進專案", "展開 .vendor_kit/、justfile、.version；問要不要接工具並跑 init；然後刪掉自己（第 10 頁）", "docker run … vendor_kit bootstrap", ".vendor_kit/、justfile、.version、test/ci/check.sh、renovate.json（新建）", "專案裡還沒有任何 vendor_kit 的東西，得有第一個入口", "建專案的人；一個專案一次"),
 ("just vendor_kit init", "第一次把工具接進專案（先在 .version 加一行 <repo> = \"image\"）", "安裝 .<repo>/，再照 init.toml 建立初始檔（Dockerfile、設定檔、hooks…）；已存在的警告、不覆蓋；並把這版模板存成基準", "vendor_kit 容器：install → init", ".<repo>/（新建）、初始檔（已存在的不動）、基準 baseline/<repo>/", "初始檔（Dockerfile 等）要有第一份，基準要存下來", "接上工具的人；每個工具一次"),
 ("just vendor_kit upgrade <repo>", "沒有 Renovate 機器人時，想手動升級", "只把 .version 那行改成最新（或指定）版本就停、不裝、不 diff（第 11 頁 B）", "容器查 registry → 改 .version", ".version", "自動查最新版與 digest 改 .version，不用手填；有 Renovate 就幾乎用不到", "維護者；沒機器人或急著升時，很少"),
 ("just vendor_kit accept <repo>", "看完 diff、跟進完之後", "把新版模板存成基準，下次 diff 以它為舊版", "vendor_kit 容器：accept", ".vendor_kit/baseline/<repo>/", "不更新基準，下次 diff 會把舊改動再報一次", "維護者；跟進完，每次升級一次"),
])
# D：工具開發者
p9.append(v("gD", "1", SW(NEUTRAL), "D. 工具開發者（改工具本身的人；一般專案用不到）", 40, 1450, TBW + 40, 250))
yD = table("td", "gD", 20, 50, rh=72, rows=[
 ("just vendor_kit dev <repo> <路徑>\n（形式待回覆）", "開發工具本身時", "把工具指到本機原始碼：寫 .version.local（不進 git）並安裝；之後不做完整性檢查、只印警告", "vendor_kit 容器：--dev install", ".version.local、.<repo>/", "改工具本身時不必每改一行就出 image", "工具開發者（少數人）；開發期間"),
 ("just vendor_kit undev <repo>\n（形式待回覆）", "改完、要回正式版時", "刪掉 .version.local 那行，立即用 .version 的正式 image 重裝", "vendor_kit 容器：install", ".version.local、.<repo>/", "回正式版；同上", "工具開發者；開發結束時"),
])
# C：一個指令的完整路徑
p9.append(v("gC", "1", SW(NEUTRAL), "任何一個 just 指令的完整路徑", 40, 1730, TBW + 40, 205))
p9.append(v("c0", "gC", ELLIPSE(GREEN), "使用者打 just X", 20, 95, 160, 50))
p9.append(v("c1", "gC", LEAF(), "自動檢查／安裝 ensure\n（第 3 頁「日常」）", 440, 135, 180, 50))
p9.append(v("c2", "gC", RHOMBUS, "X 是誰的？", 220, 80, 160, 80))
p9.append(v("c3", "gC", PURPLE_LEAF, "起 vendor_kit 容器跑子命令\n（init / diff / accept / upgrade；dev = --dev install）", 660, 55, 300, 50))
p9.append(v("c4", "gC", LEAF(), "執行 .<repo>/ 裡的腳本\n（build / run / exec / stop…）", 660, 135, 300, 50))
p9.append(v("c5", "gC", ELLIPSE(GREEN), "畫面顯示結果", 1000, 70, 160, 100))
p9.append(e("ce0", "c0", "c2", "", (1, 0.5), (0, 0.5)))
p9.append(e("ce1", "c1", "c4", "通過", (1, 0.5), (0, 0.5)))
p9.append(e("ce2", "c2", "c3", "vendor_kit 的", (0.5, 0), (0, 0.5)).replace('endFill=1;', 'endFill=1;jettySize=0;', 1))
p9.append(e("ce3", "c2", "c1", "工具的", (0.5, 1), (0, 0.5)).replace('endFill=1;', 'endFill=1;jettySize=0;', 1))
p9.append(e("ce4", "c3", "c5", "", (1, 0.5), (0.2, 0.1)).replace('endFill=1;', 'endFill=1;entryPerimeter=0;', 1))
p9.append(e("ce5", "c4", "c5", "", (1, 0.5), (0.2, 0.9)).replace('endFill=1;', 'endFill=1;entryPerimeter=0;', 1))
p9 += legend("p9", 40, 1965, ["neutral", "white", "pimg", "startend", "rhomb", "notebox"], "表格：一列一個指令\n流程：實線 = 執行順序")
p9 += terms("p9", 40, 2075, rh=36, rows=[
 ("子命令", "vendor_kit 容器裡的動作：install 把 dist 裝進 .<repo>/ 並寫印記、init 建初始檔＋存基準、verify 拿 .<repo>/ 跟 image 內的 dist 比、diff 三方比模板、accept 存新基準、upgrade 查最新版改 .version；bootstrap 寫出啟動器（第一次，第 10 頁；vendor_kit 自我升級時再跑一次，第 11 頁 C）"),
 ("dist/ / <模組>", "dist/ = 工具要出貨的檔案；<模組> = 工具的 tool.just 掛上的命名空間名（tools.just 裡 mod? <模組>），由工具自己決定，通常就跟 <repo> 一樣"),
 ("registry / recipe", "image 倉庫（GHCR 等）／justfile 裡的一條指令"),
 ("有效版本 / 完整性檢查", ".version.local 有同名那行就用它、否則用 .version 的那行／verify：拿 .<repo>/ 跟 image 內的 dist 逐檔比"),
 ("基準（baseline）", ".vendor_kit/baseline/<repo>/：上次確認過的模板副本；diff 靠它分出「工具改了什麼」「你改了什麼」；init 第一次存、accept 更新"),
 (".version.local / dev", "跟 .version 同格式、不進 git 的覆蓋檔；just vendor_kit dev 寫它把工具指到本機路徑，undev 移除；有它的工具不做完整性檢查、只印警告"),
 ("bootstrap / release", "bootstrap = 第一次把 vendor_kit 接進專案的腳本，不是 just 指令、也不會先自動檢查（那時啟動器還不存在）；release = vendor_kit 打 tag 發佈的版本，image 上傳 GHCR、bootstrap.sh 附在 GitHub release 頁"),
 ("just / justfile", "just = 主機上的指令跑器；justfile = 專案裡給它讀的指令清單，第一行 mod? vendor_kit 把 .vendor_kit/ 的標準指令掛成 just vendor_kit … 命名空間（啟動器）。使用者只需要記這一頁的指令"),
 ("<repo>", "工具名（= .version 裡的 key）；工具裝在 .<repo>/"),
 ("init.toml / 初始檔", "工具給的清單：第一次要複製到專案的檔案（Dockerfile、設定檔、hooks…）；建立後歸使用者，升級不會動"),
 ("印記 / .version", ".<repo>/.stamp：第一行記裝了哪個 image（之後每檔指紋，追溯用）／專案記工具版本的檔；兩者不同就重裝，相同就拿 .<repo>/ 跟 image 內的 dist 比"),
 ("上鎖 / 結束狀態", "上鎖 = 容器先對專案目錄上鎖，兩個 just 同時跑時後到的等前一個裝完（第 5 頁）／結束狀態 = 指令結束時回報的數字，0 成功、非 0 失敗；diff 用 0／1／2 分別表示沒差異／工具有改／可能撞到"),
 ("Renovate / GHCR", "GitHub 上的機器人：有新版就自動開 PR 改 .version／GitHub 的 image 倉庫"),
 ("PR / tag / docker run", "GitHub 上的合併請求，人 merge 才生效／給 repo 打的版本記號，CI 看到就發佈／把 image 跑成容器的指令"),
 ("docker compose", "Docker 內建的多容器管理指令：build 建置、up 啟動、exec 進入、down 停止"),
 ("image / 容器 / Dockerfile", "image = 打包好的環境（做一次）；容器 = image 開起來的實例（可開可關）；Dockerfile = 怎麼做 image 的食譜。build 做 image，run 開容器"),
 ("hooks", "掛勾腳本：每個工具指令前（pre）後（post）自動執行的你的腳本，預設是空殼"),
 ("容器工作流", "用容器當開發環境的工作方式：建置 image → 啟動容器 → 進去工作 → 停掉；「工具 <repo> 提供的指令」表的四個指令就是它"),
])

# ================= Page 10: 流程：bootstrap（第一次把 vendor_kit 接進專案） =================
# 依使用者描述：release 附一個腳本 → 執行後展開 .vendor_kit/ → 問要不要跑 init → 做完腳本自己刪掉，只留 .vendor_kit/
p11 = [v("title", "1", TITLE, "流程：bootstrap ── 第一次把 vendor_kit 接進專案（release 附的腳本，跑完自己刪掉）", 40, 20, 1300, 30)]
for name, x, w in [("使用者", 40, 260), ("bootstrap.sh（在主機執行）", 340, 380), ("vendor_kit 容器", 760, 360), ("專案目錄", 1160, 360)]:
    p11.append(v(f"bh_{x}", "1", "text;html=1;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;", name, x, 60, w, 24))
p11.append(v("bs", "1", SW(NEUTRAL), "bootstrap：一次做完，之後都靠 just", 20, 100, 1520, 640))
# 使用者
p11.append(v("u0", "bs", ELLIPSE(GREEN), "下載 release 附的\nbootstrap.sh，在專案目錄執行", 30, 60, 240, 60))
p11.append(v("u1", "bs", ELLIPSE(GREEN), "完成：專案裡多了 .vendor_kit/、justfile、\n.version、test/ci/check.sh、renovate.json\n（＋ .<repo>/、初始檔）", 20, 545, 260, 80).replace("fontSize=14", "fontSize=12"))
# 腳本
p11.append(v("s1", "bs", RHOMBUS, "主機有 docker、\ngit、just？", 400, 50, 200, 80))
p11.append(v("s_err", "bs", ELLIPSE(RED), "中止：列出缺的軟體", 400, 160, 200, 50))
p11.append(v("s2", "bs", LEAF(), "docker run … vendor_kit:vN --self <image> bootstrap\n（以使用者身分，掛載專案目錄）", 340, 280, 320, 50).replace("fontSize=14", "fontSize=12"))
p11.append(v("s3", "bs", RHOMBUS, "要現在接一個\n工具嗎？", 400, 360, 200, 80))
p11.append(v("s4", "bs", LEAF(), "把 <repo> = \"image\" 寫進 .version\n再執行 just vendor_kit init（第 3 頁「第一次」）", 340, 470, 320, 50))
p11.append(v("s5", "bs", LEAF(), "刪掉 bootstrap.sh 自己", 380, 560, 240, 40))
# 容器
p11.append(v("c1", "bs", PURPLE_LEAF, "bootstrap 子命令\n寫出啟動器、版本檔、契約檢查腳本與 renovate.json（不碰其他檔）；.gitignore 加一行 .version.local\n--self = 要寫進 .version 與印記的 vendor_kit 字串", 760, 215, 340, 250).replace("fontSize=14", "fontSize=13"))
# 專案目錄（虛線框 = 檔案）
p11.append(v("f1", "bs", FILE, ".vendor_kit/（進 git，人不改）\nvendor.just：標準指令（init / diff / accept / dev / undev / upgrade 與每個指令前的自動檢查）\ntools.just：依 .version 產生的工具指令清單（每次 install 後重寫）；.stamp：記 vendor_kit 版本\nbaseline/<repo>/ 之後由 init／accept 寫", 1160, 205, 340, 100).replace("fontSize=14", "fontSize=11"))
p11.append(v("f2", "bs", FILE, "justfile（一行 mod? vendor_kit '.vendor_kit/vendor.just'；\n之後是使用者自己的指令，進 git；已存在就不動）", 1160, 311, 340, 56).replace("fontSize=14", "fontSize=12"))
p11.append(v("f3", "bs", FILE, ".version（先只有 vendor_kit 一行，進 git；已存在就不動）", 1160, 375, 340, 36).replace("fontSize=14", "fontSize=12"))
p11.append(v("f3b", "bs", FILE, "test/ci/check.sh、renovate.json\n（進 git，之後歸專案；第 11、12 頁）", 1160, 416, 340, 40).replace("fontSize=14", "fontSize=12"))
p11.append(v("f4", "bs", FILE, ".<repo>/（不進 git）＋ 初始檔（進 git）", 1160, 475, 340, 40))
# 線
p11.append(e("be1", "u0", "s1", "", (1, 0.5), (0, 0.5)))
p11.append(e("be2", "s1", "s_err", "缺", (0.5, 1), (0.5, 0), vert="left"))
p11.append('<mxCell id="be3" value="齊全" style="' + EDGE + 'align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="bs" source="s1" target="s2"><mxGeometry x="-0.5" relative="1" as="geometry"><Array as="points"><mxPoint x="690" y="90"/><mxPoint x="690" y="250"/><mxPoint x="500" y="250"/></Array></mxGeometry></mxCell>')
p11.append(e("be4", "s2", "c1", "", (1, 0.5), (0, 0.36)))
p11.append(e("be5", "c1", "f1", "寫出", (1, 0.16), (0, 0.5)))
p11.append(e("be6", "c1", "f2", "沒有才寫", (1, 0.496), (0, 0.5)))
p11.append(e("be7", "c1", "f3", "沒有才寫", (1, 0.712), (0, 0.5)))
p11.append(e("be7b", "c1", "f3b", "寫出", (1, 0.884), (0, 0.5)))
p11.append(e("be8", "s2", "s3", "", (0.5, 1), (0.5, 0)))
p11.append(e("be9", "s3", "s4", "要", (0.5, 1), (0.5, 0), vert=True))
p11.append('<mxCell id="be10" value="先不要" style="' + EDGE + 'align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="bs" source="s3" target="s5"><mxGeometry x="0.2" relative="1" as="geometry"><Array as="points"><mxPoint x="310" y="400"/><mxPoint x="310" y="580"/></Array></mxGeometry></mxCell>')
p11.append(e("be11", "s4", "f4", "install + init 寫出", (1, 0.5), (0, 0.5)))
p11.append(e("be12", "s4", "s5", "", (0.5, 1), (0.5, 0)))
p11.append('<mxCell id="be13" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="bs" source="s5" target="u1"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="500" y="630"/><mxPoint x="150" y="630"/></Array></mxGeometry></mxCell>')
p11.append(v("bn", "1", NOTE, "之後：vendor_kit 出新版 → .version 的 vendor_kit 那行改掉（Renovate 或 just vendor_kit upgrade）→ .vendor_kit/ 的 vendor.just、tools.just、.stamp 換新（baseline/ 不動）；使用者的 justfile 永遠不會被動到。\nbootstrap.sh 的內容其實只有：檢查三個軟體 → 那一行 docker run → 問問題 → 自刪；主機不需要 Python。", 20, 760, 1520, 50))
p11 += legend_flow("p11", 40, 830, files=True, note=True)
p11 += terms("p11", 40, 940, [
 ("bootstrap.sh / bootstrap 子命令", "bootstrap.sh = release 附、在主機跑的腳本（檢查軟體、起容器、問問題、自刪）；bootstrap 子命令 = 容器內真正寫出 .vendor_kit/、justfile、.version 的動作"),
 ("accept", "升級後看完 diff、跟進完，打 just vendor_kit accept <repo> 把新版模板存成下次比較的基準（第 5 頁）"),
 ("啟動器 / .vendor_kit/", "just 要用的標準指令集，由 vendor_kit 寫出並擁有；使用者不改，升級換新程式檔（baseline/ 是持久資料不動）"),
 ("--self / tools.just / baseline/", "--self = 啟動器傳給容器的 vendor_kit image 字串／依 .version 產生、每次 install 後重寫的工具指令清單（用 mod? 掛進 just）／三方比對的基準副本（第 5 頁）"),
 ("印記（.vendor_kit/.stamp）", "跟 .<repo>/.stamp 同一種東西，但這份記的是 vendor_kit 自己的版本 + 標準指令檔（.vendor_kit/vendor.just）的指紋；啟動器拿它跟 .version 的 vendor_kit 那行比"),
 ("docker / git / just", "主機要先裝的三個軟體：跑容器的／管理 repo 的／跑 justfile 指令的；bootstrap 只檢查有沒有，不幫你裝"),
 ("容器 / image / 掛載", "image = 打包好的環境；容器 = image 開起來的實例；掛載 = 把專案目錄接進容器，容器寫的檔就直接出現在專案裡"),
 ("GHCR / Renovate / tag / TOML", "GitHub 的 image 倉庫／自動開 PR 改 .version 的機器人／給 repo 打的版本記號／設定檔格式"),
 ("justfile / mod?", "專案根目錄給 just 讀的指令清單；第一行 mod? vendor_kit 把 .vendor_kit/ 的標準指令掛成命名空間（just vendor_kit …），其餘是使用者自己的"),
 (".version", "工具版本清單（TOML）；bootstrap 後先只有 vendor_kit 一行，接工具時再加一行 <repo> = \"image\""),
 ("release", "vendor_kit 打 tag 發佈的一個版本：含 image（上傳 GHCR）與 bootstrap.sh（附在 GitHub release 頁）"),
 ("just vendor_kit init / install", "just vendor_kit init = 第 3 頁「第一次」流程：先 install（把工具的 dist 裝進 .<repo>/），再 init（建立初始檔）"),
 ("以使用者身分", "docker run -u UID:GID（你在主機的使用者與群組編號）：容器寫出的檔案擁有者是你，不是 root（系統管理者帳號）"),
 ("契約檢查腳本 / renovate.json", "test/ci/check.sh：下游 CI 只呼叫它（第 12 頁）／Renovate 的設定檔，只含 extends 指向 vendor_kit 的共用設定（第 11 頁 A）"),
 ("diff / PR", "diff = 升級後比對新版模板與你的初始檔的子命令（不改檔）／PR = GitHub 上的合併請求，人 merge 才生效"),
])

# ================= Page 11: 流程：升級與回退（初版，供討論） =================
# 四條路徑：A Renovate 自動、B just vendor_kit upgrade 手動、C vendor_kit 自身升級、D 回退。待決處用便條標「待決」。
p12 = [v("title", "1", TITLE, "流程：升級與回退 ── 四條路徑（初版，待決處以便條標示）", 40, 20, 580, 30)]
p12.append(v("p12_pend", "1", PEND, "⚠ 待你回覆：1. image 是公開還是私有？（決定 token 怎麼給）　2. upgrade 不給 name 時要拒絕（要 name 或 --all）？--all 含不含 vendor_kit 自身？　3. C 第一版「更新啟動器後停下來要求重跑」可接受？　4. .vendor_kit/ 程式檔重寫後由誰 commit（人手，CI 紅燈提醒）？", 640, 6, 940, 50))
COLS_U = [("使用者", 40, 260), ("Renovate 機器人與 CI（GitHub 上）", 310, 260), ("啟動器（.vendor_kit/，在主機）", 580, 320), ("vendor_kit 容器", 920, 320), ("專案目錄", 1260, 300)]
for name, x, w in COLS_U:
    p12.append(v(f"uh_{x}", "1", "text;html=1;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;", name, x, 60, w, 24))
def uband(bid, title, y, h):
    p12.append(v(bid, "1", SW(NEUTRAL), title, 20, y, 1560, h))

# ---- A：Renovate 自動 ----
uband("uA", "A. 自動：Renovate 發現 GHCR 有新版（正常情況走這條）", 100, 470)
p12.append(v("a0", "uA", ELLIPSE(GREEN), "起點：GHCR 出現\n<repo>-dist 新 tag", 340, 55, 200, 50))
p12.append(v("a1", "uA", LEAF(), "開 PR：改 .version 那一行\n（tag 與 digest 一起換）", 340, 130, 200, 50))
p12.append(v("a2", "uA", LEAF(), "CI 在 PR 上跑契約檢查腳本 test/ci/check.sh\n（範例；深淺由專案決定）", 310, 205, 260, 50).replace("fontSize=14", "fontSize=12"))
p12.append(v("a3", "uA", LEAF(), "自動檢查通過 → merge PR", 60, 205, 220, 50))
p12.append(v("a4", "uA", LEAF(), "每個人下次打 just：\n印記第一行 ≠ .version → install", 600, 290, 280, 50))
p12.append(v("a5", "uA", PURPLE_LEAF, "install 新版", 940, 290, 280, 50))
p12.append(v("a6", "uA", FILE, ".<repo>/（新版）", 1280, 290, 260, 50))
p12.append(v("a7", "uA", LEAF(), "just vendor_kit diff <repo> → 跟進 →\njust vendor_kit accept <repo>\n（第 5 頁 diff／accept 泳道）", 50, 375, 240, 60).replace("fontSize=14", "fontSize=12"))
p12.append(v("a8", "uA", FILE, ".vendor_kit/baseline/<repo>/（更新）", 1280, 380, 260, 50))
p12.append(e("ae1", "a0", "a1", "", (0.5, 1), (0.5, 0)))
p12.append(e("ae2", "a1", "a2", "PR", (0.5, 1), (0.5, 0), vert=True))
p12.append('<mxCell id="ae3" value="結果" style="' + EDGE + 'exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="uA" source="a2" target="a3"><mxGeometry relative="1" as="geometry"/></mxCell>')
p12.append('<mxCell id="ae4" value="merge 後" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="uA" source="a3" target="a4"><mxGeometry x="0.5" relative="1" as="geometry"><Array as="points"><mxPoint x="170" y="315"/></Array></mxGeometry></mxCell>')
p12.append(e("ae5", "a4", "a5", "", (1, 0.5), (0, 0.5)))
p12.append(e("ae6", "a5", "a6", "寫入", (1, 0.5), (0, 0.5)))
p12.append('<mxCell id="ae7" value="裝完之後" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="uA" source="a4" target="a7"><mxGeometry x="-0.3" relative="1" as="geometry"><Array as="points"><mxPoint x="740" y="405"/></Array></mxGeometry></mxCell>')
p12.append('<mxCell id="ae8" value="accept 寫入" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="uA" source="a7" target="a8"><mxGeometry x="0.5" relative="1" as="geometry"><Array as="points"><mxPoint x="170" y="450"/><mxPoint x="1250" y="450"/><mxPoint x="1250" y="405"/></Array></mxGeometry></mxCell>')
p12.append(v("an", "uA", NOTE, "已定：CI 深淺由專案決定；vendor_kit 出貨完整的契約檢查腳本與 renovate.json（只含 extends，指向 vendor_kit repo 內的共用 preset；GitLab 自架 renovate-runner），bootstrap 寫出，之後歸專案。", 940, 55, 600, 64))

# ---- B：手動 just vendor_kit upgrade ----
uband("uB", "B. 手動：just vendor_kit upgrade <repo>（沒有 Renovate、或想馬上升）", 600, 270)
p12.append(v("b0", "uB", ELLIPSE(GREEN), "just vendor_kit upgrade <repo>", 60, 60, 220, 50))
p12.append(v("b1", "uB", LEAF(), "起 vendor_kit 容器跑 upgrade 子命令", 600, 60, 280, 50))
p12.append(v("b2", "uB", PURPLE_LEAF, "查 registry（OCI API）：\n<repo>-dist 最新 tag + digest（要網路；只查不裝）", 940, 55, 280, 60).replace("fontSize=14", "fontSize=12"))
p12.append(v("b3", "uB", FILE, ".version 那一行改成新版", 1280, 60, 260, 50))
p12.append(v("b4", "uB", LEAF(), "upgrade 結束：印「尚未安裝，下一步 just vendor_kit diff <repo>」\n之後每個人下次打 just 才 install（同 A）", 600, 165, 280, 60).replace("fontSize=14", "fontSize=12"))
p12.append(v("b5", "uB", LEAF(), "just vendor_kit diff <repo> → 跟進 →\njust vendor_kit accept <repo>（同 A）", 40, 172, 240, 46).replace("fontSize=14", "fontSize=12"))
p12.append(v("b6", "uB", ELLIPSE(GREEN), "結束：commit .version 與你的修改", 40, 228, 240, 40).replace("fontSize=14", "fontSize=12"))
p12.append(e("be1", "b0", "b1", "", (1, 0.5), (0, 0.5)))
p12.append(e("be2", "b1", "b2", "", (1, 0.5), (0, 0.5)))
p12.append(e("be3", "b2", "b3", "改一行", (1, 0.5), (0, 0.5)))
p12.append('<mxCell id="be4" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="uB" source="b3" target="b4"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="1410" y="132"/><mxPoint x="740" y="132"/></Array></mxGeometry></mxCell>')
p12.append(e("be5", "b4", "b5", "", (0, 0.5), (1, 0.5)))
p12.append(e("be6", "b5", "b6", "", (0.5, 1), (0.5, 0)))
p12.append(v("bn", "uB", NOTE, "已定（雙軌一致）：just vendor_kit upgrade <repo> [版本] [--dry-run|--check]：只把 .version 那行改成最新（或指定）版本就停、不裝、不 diff，成功訊息寫「尚未安裝，下一步 just vendor_kit diff <repo>」；查 registry 在容器內用 OCI 標準 API（GHCR、GitLab 同一套）；「最新」只認 v主.次.修，預設略過預發行版；digest 取 multi-arch index 並確認含 amd64+arm64；憑證：唯讀掛 ~/.docker/config.json 或環境變數 token。", 940, 150, 600, 100))

# ---- C：vendor_kit 自身升級 ----
uband("uC", "C. vendor_kit 自己升級（啟動器 .vendor_kit/ 換新）", 900, 250)
p12.append(v("c0", "uC", FILE, ".version 的 vendor_kit 那一行改了\n（走 A 或 B，跟工具一樣）", 60, 50, 240, 60).replace("fontSize=14", "fontSize=12"))
p12.append(v("c1", "uC", LEAF(), "下次 just：.vendor_kit/.stamp 第一行\n≠ .version 的 vendor_kit 行", 600, 50, 280, 60).replace("fontSize=14", "fontSize=12"))
p12.append(v("c2", "uC", PURPLE_LEAF, "用新版 vendor_kit image 跑 bootstrap\n只重寫 vendor.just / tools.just / .stamp", 940, 50, 280, 60).replace("fontSize=14", "fontSize=12"))
p12.append(v("c3", "uC", FILE, ".vendor_kit/ 程式檔換新\n（baseline/、justfile、.version 不動）", 1280, 55, 260, 50).replace("fontSize=14", "fontSize=12"))
p12.append(e("ce1", "c0", "c1", "下次 just 讀到", (1, 0.5), (0, 0.5)))
p12.append(e("ce2", "c1", "c2", "", (1, 0.5), (0, 0.5)))
p12.append(e("ce3", "c2", "c3", "寫入", (1, 0.5), (0, 0.5)))
p12.append(v("cn", "uC", NOTE, "已定（雙軌一致）：先換自己：舊啟動器發現 vendor_kit 行變了 → 用新 image 跑 bootstrap（這個呼叫方式凍結為契約）重寫 .vendor_kit/ 程式檔（baseline/ 不動）→ 第一版：停下來、印「請重打一次指令」（just 已把 recipe 讀進記憶體，改了檔本次無效）。相容性（issue #14）：image LABEL 帶契約版本號，啟動器用 docker image inspect 比對。", 60, 130, 800, 84))

# ---- D：回退 ----
uband("uD", "D. 回退（升上去發現壞了）", 1180, 220)
p12.append(v("d0", "uD", ELLIPSE(GREEN), "git revert 那個升級 commit\n（.version 那行改回舊版）", 60, 55, 220, 60))
p12.append(v("d1", "uD", LEAF(), "下次 just：印記 ≠ .version\n→ install 舊版", 600, 60, 280, 50))
p12.append(v("d2", "uD", FILE, ".<repo>/（舊版）", 1280, 60, 260, 50))
p12.append(e("de1", "d0", "d1", "", (1, 0.5), (0, 0.5)))
p12.append(e("de2", "d1", "d2", "寫入", (1, 0.5), (0, 0.5)))
p12.append(v("dn", "uD", NOTE, "已定（雙軌一致）：回退 = git revert 那個 commit（Renovate 的 merge commit 用 -m 1）；不強制 accept 與 .version 同一 commit；baseline 落後或超前 .version 都是合法中間狀態，diff 會印出方向（落後 = 還沒 accept；超前 = 可能是回退），CI 只警告不紅；使用者檔由人決定。", 60, 125, 1480, 70))

p12 += legend_flow("p12", 40, 1430, files=True, note=True)
p12 += terms("p12", 40, 1540, rh=36, rows=[
 ("Renovate", "GitHub 上的機器人：發現 GHCR 有新版就自動開 PR 改 .version；沒有它時用 just vendor_kit upgrade 手動"),
 ("CI / 契約檢查腳本 / renovate.json", "CI = GitHub／GitLab 上的自動檢查，PR 一開就跑／test/ci/check.sh：vendor_kit 出貨、bootstrap 寫到專案的檢查腳本（第 12 頁）／Renovate 的設定檔，只含 extends"),
 ("registry / OCI API", "image 倉庫（GHCR、GitLab 都是）／它們共同遵守的標準查詢介面，所以同一段程式兩邊都能查"),
 ("preset / extends / runner", "Renovate 的共用設定檔（放在 vendor_kit repo）／專案的 renovate.json 用 extends 指向它／GitLab 上自己架的 Renovate 執行器"),
 ("token / multi-arch index", "登入 registry 用的密碼字串／同一 image 同時含 amd64 與 arm64 的索引，digest 鎖的是它"),
 ("LABEL / docker image inspect / --dry-run", "寫在 image 上的標籤（帶契約版本號）／讀 image 標籤的指令／只顯示會改什麼、不真的改（--check 同）"),
 ("recipe", "justfile 裡的一條指令；just 啟動時整份讀進記憶體，跑到一半改檔本次無效"),
 ("GHCR / image / 容器", "GitHub 的 image 倉庫／打包好的程式與檔案／image 執行起來的實例；vendor_kit 與工具都以 image 出貨"),
 (".version / <repo>", "專案裡的工具版本清單（一行一個工具）／工具名，安裝目錄叫 .<repo>/"),
 ("just / just vendor_kit upgrade", "主機上的指令跑器，使用者打 just <指令>／手動升級的指令（B 路徑）"),
 ("install / verify / diff / commit", "裝進 .<repo>/／檢查 .<repo>/ 沒被改／三方比對／git 的一次版本紀錄"),
 ("vendor_kit / 啟動器", "通用安裝工具（容器內跑）／專案裡的 .vendor_kit/：just 用的標準指令，vendor_kit 寫出、人不改"),
 ("justfile / vendor.just / tools.just", "使用者自己的指令清單（第一行 mod? vendor_kit）／vendor_kit 的標準指令檔（just vendor_kit …）／依 .version 產生的工具指令清單；C 只換後兩者與 .stamp"),
 ("TOML / regex manager / init.toml", "設定檔格式／Renovate 用「找字串」的方式改自訂檔案的設定／工具的初始檔清單"),
 ("tag / digest", "image 的版本名稱／內容指紋；.version 兩者都記，一起換"),
 ("PR / merge / revert", "GitHub 上的合併請求／接受它／用 git 把某次修改整個倒回去"),
 ("印記第一行", ".<repo>/.stamp 第一行 = 裝的是哪個 image；跟 .version 那行不同就重裝（第 3 頁）"),
 ("baseline / accept", "上次確認過的範本副本／告訴工具「這版我看完了」（第 5 頁、issue #22）"),
 ("bootstrap（在 C 裡）", "同第 10 頁的子命令，這裡只重寫 .vendor_kit/ 的程式檔"),
 ("issue #14", "相容性承諾這一題的 GitHub 討論串"),
])

# ================= Page 12: 對外契約與 CI 隔離（初版，供討論） =================
p13 = [v("title", "1", TITLE, "對外契約 ── vendor_kit 對外承諾的每一個介面，以及 CI 怎麼隔離（GitHub / GitLab 都只呼叫我們的腳本）", 40, 20, 860, 30)]
p13.append(v("p13_pend", "1", PEND, "⚠ 待你回覆：GitLab 拉 GHCR 私有 image 的 token 放哪？要不要推兩個 registry？契約檢查腳本用 sh 還是 just？", 920, 10, 450, 50))
CT_H = "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999999;fontSize=12;fontStyle=1;align=center;strokeWidth=1;"
CT_C = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=12;align=left;spacingLeft=6;strokeWidth=1;"
CT_K = CT_C + "fontStyle=1;"
CCOLS = [("契約", 190), ("誰對誰", 220), ("內容（承諾不會隨便改的部分）", 620), ("誰用它來測", 300)]
def ctable(prefix, parent, x, y, rows, rh=52):
    cx = x
    for i, (h, w) in enumerate(CCOLS):
        p13.append(v(f"{prefix}_h{i}", parent, CT_H, h, cx, y, w, 30)); cx += w
    for r, row in enumerate(rows):
        cx = x
        for i, (cell, (h, w)) in enumerate(zip(row, CCOLS)):
            p13.append(v(f"{prefix}_r{r}c{i}", parent, CT_K if i == 0 else CT_C, cell, cx, y + 30 + r * rh, w, rh)); cx += w
    return y + 30 + len(rows) * rh
CW = sum(w for _, w in CCOLS)
p13.append(v("ct", "1", SW(NEUTRAL), "對外契約（五個介面；①依角色分四行）", 40, 70, CW + 40, 570))
yc = ctable("ct", "ct", 20, 50, [
 ("①a 使用者介面", "使用者（拿專案成果來用）→ 啟動器", "工具命名空間的 just <模組> run / stop（若工具提供）；結束狀態 0 成功／非 0 失敗（第 9 頁 A 區）", "acceptance 測試（第 8 頁）；下游的 CI"),
 ("①b 開發者介面", "開發者（天天寫程式）→ 啟動器", "just <模組> build / run / exec / stop（由工具定義）＋ just vendor_kit diff（結束狀態 0／1／2）（第 9 頁 B 區）", "acceptance 測試；下游的 CI"),
 ("①c 維護者介面", "專案維護者 → 啟動器", "bootstrap.sh 的用法；just vendor_kit init / upgrade / accept 的名稱、參數與行為（第 9 頁 C 區）", "acceptance 測試；下游的 CI"),
 ("①d 工具開發者介面", "工具開發者 → 啟動器", "just vendor_kit dev / undev（本機開發模式，形式待回覆）；.version.local 格式（第 9 頁 D 區）", "acceptance 測試"),
 ("② 啟動器 ↔ 容器", ".vendor_kit/vendor.just → vendor_kit 容器", "docker run 的參數：-u UID:GID、-v 專案:/repo；argv：--name --self --repo --dist + 子命令 install / init / verify / diff / accept / bootstrap / upgrade；結束狀態 0/1/2；image 內 /dist 的佈局（dist/ 原樣、init.toml、VERSION）", "system 測試（docker run 每個子命令）"),
 ("③ 專案裡的檔", "vendor_kit → 專案 repo", ".version 格式（TOML，[tools] 一行一工具 <repo> = \"image:tag@sha256\"，含 vendor_kit 行）；.version.local；.vendor_kit/ 佈局（vendor.just、tools.just、.stamp、baseline/<repo>/）；.<repo>/.stamp 格式（第一行 image，之後 sha256 路徑）", "integration 測試（bootstrap / install 寫出的檔）"),
 ("④ 工具 repo 要交的", "工具 repo → vendor_kit", "dist/（全部出貨、不含 symlink）；init.toml 格式（[[file]] src/dest）；dist/just/tool.just（工具自己的指令）；Dockerfile.dist（FROM vendor_kit + COPY）；image 命名 <repo>-dist:tag，且支援兩種架構（multi-arch amd64 + arm64）", "release-test 與 system 測試（用 fixtures 假工具）；工具 repo 的 CI"),
 ("⑤ 給下游的 CI 腳本", "vendor_kit → 專案／工具 repo 的 CI", "test/ci/check.sh（平台無關，下方）＋ renovate.json（只含 extends）；腳本內容 = 上面四條契約的檢查；GitHub / GitLab 的 CI 檔只負責呼叫它", "下游 CI（GitHub Actions 或 GitLab CI 皆可）"),
])
p13.append(v("ct_n", "ct", NOTE, "待決（issue #14）：契約版本號寫在哪（.vendor_kit/.stamp？image label？），哪些改動算破壞相容（要升大版）、誰檢查啟動器與容器內 vendor_kit 版本不合。", 20, yc + 10, CW, 44))
# CI 隔離
p13.append(v("ci", "1", SW(NEUTRAL), "CI 隔離：CI 平台檔只呼叫我們的腳本，換平台不用改測試", 40, 670, CW + 40, 270))
p13.append(v("ci_gh", "ci", LEAF(YELLOW), "GitHub Actions\n.github/workflows/*.yaml（薄：只呼叫）", 20, 50, 320, 50))
p13.append(v("ci_gl", "ci", LEAF(YELLOW), "GitLab CI\n.gitlab-ci.yml（薄：只呼叫）", 20, 120, 320, 50))
p13.append(v("ci_sc", "ci", LEAF(), "vendor_kit 出貨的測試腳本（平台無關）\ntest/ci/check.sh：bootstrap 檢查 → install → verify → diff 結束狀態\n（只需要 docker + git + just）", 420, 50, 420, 120))
p13.append(v("ci_bake", "ci", LEAF(), "vendor_kit 自己的 CI（第 8 頁）：\nbake validate → system／acceptance → bake release", 920, 50, 380, 50).replace("fontSize=14", "fontSize=12"))
p13.append(v("ci_reg", "ci", LEAF(YELLOW), "image 倉庫：GHCR 或 GitLab Container Registry\n（.version 記完整位址，docker login 就能拉；Renovate 兩邊都支援）", 920, 120, 380, 60))
p13.append(e("cie1", "ci_gh", "ci_sc", "呼叫", (1, 0.5), (0, 0.2083)))
p13.append(e("cie2", "ci_gl", "ci_sc", "呼叫", (1, 0.5), (0, 0.7917)))
p13.append(e("cie3", "ci_sc", "ci_bake", "vendor_kit\nrepo 內", (1, 0.2083), (0, 0.5)))
p13.append(e("cie4", "ci_sc", "ci_reg", "拉 image", (1, 0.8333), (0, 0.5)))
p13.append(v("ci_n", "ci", NOTE, "待決：GitLab 拉 GHCR 私有 image 要放 token（GitLab CI 變數）；要不要同時推到兩個 registry？測試腳本用 sh 還是 just recipe（just 在 CI runner 也要裝）？", 20, 200, 1300, 44))
p13 += legend("p13", 40, 970, ["yellow", "neutral", "white"], "實線 = 呼叫／依賴方向")
p13 += terms("p13", 40, 1080, rh=36, rows=[
 ("對外契約", "我們承諾「這樣用一定可以、不會隨便改」的介面清單；改了就要升版並公告"),
 ("image / dist / TOML / baseline / 印記", "打包好的程式與檔案／工具要出貨的檔案／設定檔格式／上次確認過的模板副本（.vendor_kit/baseline/<repo>/）／.<repo>/.stamp，記裝了哪個 image"),
 ("symlink / sha256 / digest", "指向別檔的捷徑（第一版禁止）／檔案內容指紋／image 內容指紋"),
 ("FROM / COPY / bake", "Dockerfile 指令：以哪個 image 為底／把檔放進去／docker buildx bake：一次跑多個 stage 的工具"),
 ("測試層級", "acceptance = 在假專案真的打 just；system = docker run 每個子命令；integration = 一個子命令走到底；release-test = 出貨前真的裝一次（第 8 頁）"),
 ("Renovate / renovate.json / 契約檢查腳本", "自動開 PR 改 .version 的機器人／它的設定檔（bootstrap 寫出、只含 extends）／test/ci/check.sh，bootstrap 寫到專案"),
 ("啟動器", ".vendor_kit/ 裡 vendor_kit 寫出的 just 指令（第 2、10 頁）"),
 ("argv / 子命令", "傳給容器內程式的參數／install、init 這些動作名"),
 ("GitHub Actions / GitLab CI", "兩家平台各自的自動化流程；設定檔格式不同，所以我們的測試不寫在裡面，寫在自己的腳本"),
 ("GHCR / GitLab Container Registry", "GitHub 與 GitLab 各自的 image 倉庫；都是標準 Docker registry，位址不同而已"),
 ("multi-arch", "同一個 image 名稱同時有 amd64 與 arm64 版本；.version 鎖的 digest 是這組的索引"),
 ("issue #14", "相容性承諾這一題的 GitHub 討論串"),
])


doc = ('<mxfile host="app.diagrams.net">'
       + page("p1", "1. vendor_kit 架構圖", p1, w=1700, h=1430)
       + page("p1b", "2. 框架定義", p1b, w=1800, h=1160)
       + page("p2", "3. 流程：使用者指令", p2, w=1700, h=1580)
       + page("p3", "4. 流程：版本生命週期", p3, h=1030)
       + page("p4", "5. 流程：vendor_kit 內部", p4)
       + page("p7", "6. 原型對照", p7, h=920)
       + page("p10", "7. 資料夾架構", p10)
       + page("p8", "8. 測試分層與強制閘門", p8)
       + page("p9", "9. 使用者介面：just 指令表", p9)
       + page("p11", "10. 流程：bootstrap", p11)
       + page("p12", "11. 流程：升級與回退", p12)
       + page("p13", "12. 對外契約與 CI 隔離", p13)
       + "</mxfile>")
open("/home/cyc/Desktop/vendor-kit_ws/src/dist_distribution.drawio", "w").write(doc)
print(len(doc))
