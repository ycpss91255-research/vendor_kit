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
        "strokeWidth=2;align=center;verticalAlign=bottom;spacingBottom=6;fontFamily=Helvetica;fontSize=10;"
        "fontColor=default;labelBorderColor=none;labelBackgroundColor=none;endArrow=block;endFill=1;")

def esc(s): return html.escape(s, quote=True).replace("\n", "&lt;br&gt;")

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
    elif vert: st += "align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;"
    xa = "" if pos is None else f' x="{pos}"'
    inner = "" if offset is None else f'<mxPoint x="{offset[0]}" y="{offset[1]}" as="offset"/>'
    geo = f'<mxGeometry{xa} relative="1" as="geometry">{inner}</mxGeometry>'
    return (f'<mxCell id="{id}" value="{esc(label)}" style="{st}" edge="1" parent="1" source="{src}" target="{tgt}">'
            f'{geo}</mxCell>')

def page(id, name, cells, w=1600, h=1100):
    return (f'<diagram id="{id}" name="{esc(name)}"><mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" '
            f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{w}" pageHeight="{h}" math="0" shadow="0">'
            f'<root><mxCell id="0" style="strokeWidth=2;"/><mxCell id="1" parent="0" style="strokeWidth=2;"/>{"".join(cells)}</root></mxGraphModel></diagram>')

def legend_arch(prefix, x, y):
    c = []
    for i, (t, f) in enumerate([("紅：新建模組", RED), ("綠：現有模組（本體不變）", GREEN), ("黃：外部系統（不由我們維護）", YELLOW)]):
        c.append(v(f"{prefix}_lg{i}", "1", LEGEND_BOX(f), t, x + i * 240, y, 220, 60))
    c.append(v(f"{prefix}_lg3", "1", LEAF(), "白：新建單元", x + 3 * 240, y + 10, 120, 40))
    c.append(v(f"{prefix}_lg4", "1", LEAF(GREY), "灰：現有單元", x + 3 * 240 + 130, y + 10, 120, 40))
    c.append(v(f"{prefix}_lg5", "1", PURPLE_LEAF, "紫：image / container", x + 3 * 240 + 260, y + 10, 160, 40))
    c.append(v(f"{prefix}_lg6", "1", TEXT(12) + "align=left;", "實線 = 傳輸內容（線上文字說明傳什麼）\n虛線 = 建立在它之上，或只在特定情況發生", x + 3 * 240 + 440, y, 260, 60))
    return c

FILE = LEAF() + "dashed=1;"
def legend_flow(prefix, x, y, purple=True, files=False):
    c = []
    items = [(LEGEND_BOX(NEUTRAL), "淺灰：情境分組（無狀態意義）", 220, 60, 0),
             (ELLIPSE(GREEN), "綠：起點／終點", 130, 40, 10),
             (RHOMBUS, "黃：判斷", 110, 60, 0),
             (ELLIPSE(RED), "紅：錯誤終止", 130, 40, 10)]
    if purple: items.append((PURPLE_LEAF, "紫：子命令（在容器內執行）", 200, 40, 10))
    items.append((LEAF(), "白：步驟", 88, 40, 10))
    if files: items.append((FILE, "虛線框：專案裡的檔案", 160, 40, 10))
    cx = x
    for i, (st, t, w, h, dy) in enumerate(items):
        c.append(v(f"{prefix}_lg{i}", "1", st, t, cx, y + dy, w, h)); cx += w + 20
    c.append(v(f"{prefix}_lgt", "1", TEXT(12) + "align=left;", "實線 = 執行順序", cx, y, 200, 60))
    return c

# ================= Page 1: vendor_kit 架構圖 =================
p1 = [v("title", "1", TITLE, "vendor_kit 架構圖（模組 → 最小單元；線上文字 = 傳的資料）", 40, 20, 900, 30)]
VX, VY = 480, 140
p1.append(v("user", "1", SW(YELLOW), "使用者", 40, VY, 140, 860))
p1.append(v("u_cmd", "user", LEAF(GREY), "指令", 26, 90, 88, 40))
p1.append(v("u_out", "user", LEAF(GREY), "畫面", 26, 760, 88, 40))
p1.append(v("img", "1", SW(YELLOW), "image 內容", 200, 300, 180, 280))
p1.append(v("i_list", "img", LEAF(), "init.toml", 46, 121, 88, 40))
p1.append(v("i_dist", "img", LEAF(GREY), "dist/（全部）", 46, 172, 88, 40))
p1.append(v("i_tpl", "img", LEAF(GREY), "模板", 46, 223, 88, 40))
p1.append(v("vk", "1", SW(RED), "vendor_kit", VX, VY, 520, 860))
p1.append(v("m_cli", "vk", SW(RED), "命令介面", 20, 50, 200, 140))
p1.append(v("cli_land", "m_cli", LEAF(), "install", 12, 45, 88, 40))
p1.append(v("cli_init", "m_cli", LEAF(), "init", 104, 45, 88, 40))
p1.append(v("cli_verify", "m_cli", LEAF(), "verify", 12, 92, 88, 40))
p1.append(v("cli_diff", "m_cli", LEAF(), "diff", 104, 92, 88, 40))
p1.append(v("m_list", "vk", SW(RED), "出貨內容讀取", 20, 250, 200, 170))
p1.append(v("ls_read", "m_list", LEAF(), "讀 dist/", 12, 45, 88, 40))
p1.append(v("ls_check", "m_list", LEAF(), "讀 init.toml", 104, 45, 88, 40))
p1.append(v("ls_class", "m_list", LEAF(), "驗證", 12, 92, 88, 40))
p1.append(v("m_tpl", "vk", SW(RED), "模板", 20, 480, 200, 130))
p1.append(v("tp_render", "m_tpl", LEAF(), "渲染", 12, 45, 88, 40))
p1.append(v("tp_vars", "m_tpl", LEAF(), "帶入變數", 104, 45, 88, 40))
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
p1.append(v("proj", "1", SW(YELLOW), "專案目錄", 1140, VY, 200, 860))
p1.append(v("p_stamp", "proj", LEAF(), "印記檔", 56, 281, 88, 40))
p1.append(v("p_base", "proj", LEAF(), ".<name>/\n（例：.base/）", 46, 327, 108, 50))
p1.append(v("p_user", "proj", LEAF(GREY), "使用者檔案", 56, 383, 88, 40))
p1.append(e("a1", "u_cmd", "m_cli", "工具名、命令、參數", (1, 0.5), (0, 0.5)))
p1.append(e("a2", "m_cli", "m_list", "命令參數", (0.5, 1), (0.5, 0), vert=True))
p1.append(e("a3", "i_list", "m_list", "init 清單", (1, 0.5), (0, 0.3)))
p1.append(e("a4", "i_dist", "m_list", "dist 內容", (1, 0.5), (0, 0.6)))
p1.append(e("a5", "i_tpl", "m_list", "模板", (1, 0.5), (0, 0.9)))
p1.append(e("a6", "m_list", "m_write", "dist 全部", (1, 0.3), (0, 0.3)))
p1.append(e("a7", "m_list", "m_tpl", "init 清單\n＋模板", (0.5, 1), (0.5, 0), vert="left"))
p1.append(e("a8", "m_tpl", "m_write", "初始檔內容", (0.8, 0), (0.1, 1)))
p1.append(e("a9", "m_write", "m_stamp", "內容、既有印記\n⇄ 新指紋", (0.8, 1), (0.64, 0), both=True, vert="left"))
p1.append(e("a10", "m_write", "p_stamp", "印記檔", (1, 0.3), (0, 0.5), both=True))
p1.append(e("a11", "m_write", "p_base", "dist 全部", (1, 0.6), (0, 0.5), both=True))
p1.append(e("a12", "m_write", "p_user", "初始檔／現有內容", (1, 0.9), (0, 0.5), both=True))
p1.append('<mxCell id="a13" value="使用者檔案" style="' + EDGE + 'exitX=0.35;exitY=1;exitDx=0;exitDy=0;entryX=0.9;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="m_write" target="m_diff"><mxGeometry x="0.55" relative="1" as="geometry"><Array as="points"><mxPoint x="850" y="780"/><mxPoint x="680" y="780"/></Array></mxGeometry></mxCell>')
p1.append(e("a14", "m_tpl", "m_diff", "新版模板", (0.5, 1), (0.5, 0), vert=True))
p1.append(e("a15", "m_stamp", "m_report", "檢查結果", (0.5, 1), (0.77, 0), vert=True))
p1.append(e("a16", "m_diff", "m_report", "差異", (1, 0.5), (0, 0.5)))
p1.append(e("a17", "m_report", "u_out", "訊息、結束狀態", (0.5, 1), (1, 0.5), pos=0.6))
p1 += legend_arch("p1", 40, 1060)

# ================= Page 2: 出貨路徑 =================
p1b = [v("title", "1", TITLE, "出貨路徑（以 base 為例）：工具透過 vendor_kit 送到各專案；其他工具（agent_harness…）同型", 40, 20, 900, 30)]
p1b.append(v("base", "1", SW(GREEN), "base", 40, 105, 240, 250))
p1b.append(v("b_dist", "base", LEAF(GREY), "dist", 22, 50, 88, 40))
p1b.append(v("b_tpl", "base", LEAF(GREY), "模板", 130, 50, 88, 40))
p1b.append(v("b_list", "base", LEAF(), "init.toml", 22, 110, 88, 40))
p1b.append(v("b_df", "base", LEAF(), "Dockerfile", 130, 110, 88, 40))
p1b.append(v("base_ci", "base", LEAF(), "自動發佈", 76, 180, 88, 40))
p1b.append(v("vk", "1", SW(RED), "vendor_kit", 40, 385, 240, 130))
p1b.append(v("vk_ci", "vk", LEAF(), "自動發佈", 76, 60, 88, 40))
p1b.append(v("other", "1", SW(GREEN), "其他工具", 40, 555, 240, 130))
p1b.append(v("other_ci", "other", LEAF(), "自動發佈", 76, 60, 88, 40))
p1b.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 360, 80, 260, 610))
p1b.append(v("g_base", "ghcr", PURPLE_LEAF, "base-dist:vX", 30, 205, 200, 40))
p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 365, 200, 40))
p1b.append(v("g_other", "ghcr", PURPLE_LEAF, "其他工具-dist:vY", 30, 535, 200, 40))
p1b.append(v("g_t", "ghcr", TEXT(11), "tag 不覆蓋；被引用的版本不刪；\nimage 附註版本與來源 commit", 10, 40, 240, 40))
p1b.append(v("ds", "1", SW(GREEN), "使用 base 的專案", 700, 80, 760, 400))
p1b.append(v("ds_engine", "ds", PURPLE_LEAF, "安裝容器（base-dist:vX）", 20, 195, 200, 60))
p1b.append(v("ds_t", "ds", TEXT(11), "以使用者身分執行，跑完即刪", 20, 257, 200, 20))
p1b.append(v("sa", "ds", SW(RED), "啟動器", 20, 50, 240, 125))
p1b.append(v("sa_t", "sa", TEXT(11), "契約版本與更新\n方式：待設計", 6, 90, 100, 26))
p1b.append(v("c_ref", "sa", LEAF(), ".version", 12, 48, 88, 40))
p1b.append(v("c_just", "sa", LEAF(), "justfile", 140, 48, 88, 40))
p1b.append(v("sb", "ds", SW(RED), "使用者檔案", 300, 265, 200, 110))
p1b.append(v("c_df", "sb", LEAF(), "Dockerfile", 12, 45, 88, 40))
p1b.append(v("c_conf", "sb", LEAF(), ".setup.conf", 104, 45, 88, 40))
p1b.append(v("sb_t", "sb", TEXT(11), "進 git；init 建立", 12, 88, 180, 18))
p1b.append(v("sc", "ds", SW(RED), ".<name>/（例 .base/）", 540, 265, 200, 110))
p1b.append(v("c_tools", "sc", LEAF(), "dist 全部", 12, 45, 88, 40))
p1b.append(v("c_stamp", "sc", LEAF(), "印記檔", 104, 45, 88, 40))
p1b.append(v("sc_t", "sc", TEXT(11), "不進 git；每次 upgrade 整批覆蓋", 12, 88, 180, 18))
p1b.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1540, 80, 150, 400))
p1b.append(v("h_docker", "host", LEAF(GREY), "Docker", 31, 300, 88, 40))
p1b.append(v("h_just", "host", LEAF(GREY), "just", 31, 60, 88, 40))
p1b.append(v("h_git", "host", LEAF(GREY), "git", 31, 120, 88, 40))
p1b.append(e("b1", "vk_ci", "g_vk", "image", (1, 0.5), (0, 0.5)))
p1b.append(e("b2", "base_ci", "g_base", "image", (1, 0.5), (0, 0.5)))
p1b.append(e("b3", "other_ci", "g_other", "image", (1, 0.5), (0, 0.5)))
p1b.append(e("b4", "g_vk", "g_base", "基底 image", (0.5, 0), (0.5, 1), dashed=True, vert=True))
p1b.append(e("b5", "g_vk", "g_other", "基底 image", (0.5, 1), (0.5, 0), dashed=True, vert=True))
p1b.append(e("b6", "g_base", "ds_engine", "image", (1, 0.5), (0, 0.5)))
p1b.append(e("b7", "c_ref", "c_just", "版本", (1, 0.5), (0, 0.5)))
p1b.append(e("b8", "c_just", "ds_engine", "版本、使用者身分、專案路徑", (0.5, 1), (0.74, 0), vert=True, pos=0.85))
p1b.append(e("b9", "ds_engine", "sc", "dist、印記檔", (1, 0.3), (0.5, 0), both=True))
p1b.append(e("b10", "ds_engine", "sb", "初始檔", (1, 0.7), (0.5, 0), dashed=True))
p1b.append(e("b11", "sc", "h_docker", "compose 指令", (1, 0.5), (0, 0.5)))
p1b += legend_arch("p1b", 40, 900)

# ================= Page 3: 流程：使用者指令 =================
p2 = [v("title", "1", TITLE, "流程：使用者下的每個指令 → 啟動器叫哪個子命令 → 專案裡發生什麼", 40, 20, 1200, 30)]
for name, x, w in [("使用者", 40, 300), ("啟動器（justfile，在主機）", 380, 360), ("安裝容器（vendor_kit）", 800, 360), ("專案目錄（安裝目錄 .<name>/，下以 .base/ 示意）", 1240, 380)]:
    p2.append(v(f"h_{x}", "1", "text;html=1;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;", name, x, 60, w, 24))
def band(bid, title, y, h):
    p2.append(v(bid, "1", SW(NEUTRAL), title, 20, y, 1620, h))
# ---- A 第一次 ----
band("bA", "第一次接上工具：just init", 100, 280)
p2.append(v("a_u", "bA", ELLIPSE(GREEN), "just init", 60, 70, 180, 50))
p2.append(v("a_l1", "bA", LEAF(), "讀 .version", 380, 75, 140, 40))
p2.append(v("a_l2", "bA", LEAF(), ".base/ 不存在\n→ 要安裝", 560, 70, 160, 50))
p2.append(v("a_c1", "bA", PURPLE_LEAF, "install\ndist/ 全部 → .base/\n並寫印記（.base/.stamp：版本 + 每檔指紋）", 800, 60, 340, 70))
p2.append(v("a_p1", "bA", FILE, ".base/（新）", 1240, 70, 200, 40))
p2.append(v("a_c2", "bA", PURPLE_LEAF, "init\n照 init.toml 複製初始檔（已存在則跳過）", 800, 165, 340, 60))
p2.append(v("a_p2", "bA", FILE, "Dockerfile / entrypoint / hooks…\n（新；之後由你維護）", 1240, 165, 200, 60))
p2.append(e("ae1", "a_u", "a_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae2", "a_l1", "a_l2", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae3", "a_l2", "a_c1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae4", "a_c1", "a_p1", "寫入", (1, 0.5), (0, 0.5)))
p2.append(e("ae5", "a_c1", "a_c2", "", (0.5, 1), (0.5, 0)))
p2.append(e("ae6", "a_c2", "a_p2", "建立", (1, 0.5), (0, 0.5)))
# ---- B 日常 ----
band("bB", "日常：just build（run / exec / stop 同）", 410, 390)
p2.append(v("b_u", "bB", ELLIPSE(GREEN), "just build", 60, 70, 180, 50))
p2.append(v("b_l1", "bB", LEAF(), "讀 .version", 380, 75, 140, 40))
p2.append(v("b_l2", "bB", RHOMBUS, "印記存在且版本\n= .version？", 550, 55, 180, 80))
p2.append(v("b_c0", "bB", PURPLE_LEAF, "install\n換成 .version 指定的版本", 800, 65, 340, 60))
p2.append(v("b_p0", "bB", FILE, ".base/（換新）", 1240, 75, 200, 40))
p2.append(v("b_c1", "bB", PURPLE_LEAF, "verify\n.base/ 每檔指紋是否仍等於印記", 800, 170, 340, 60))
p2.append(v("b_l3", "bB", LEAF(), "執行 .base/ 內的 build 腳本", 380, 260, 340, 50))
p2.append(v("b_p1", "bB", FILE, "docker compose build", 1240, 265, 200, 40))
p2.append(v("b_err", "bB", ELLIPSE(RED), "中止：.base/ 被改過\n刪除 .base/ 再 build 即自動重裝", 40, 255, 260, 60))
p2.append(e("be1", "b_u", "b_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("be2", "b_l1", "b_l2", "", (1, 0.5), (0, 0.5)))
p2.append(e("be3", "b_l2", "b_c0", "不同或不存在", (1, 0.5), (0, 0.5)))
p2.append(e("be4", "b_l2", "b_c1", "相同", (0.5, 1), (0, 0.25), pos=0.5))
p2.append(e("be5", "b_c0", "b_p0", "覆蓋", (1, 0.5), (0, 0.5)))
p2.append('<mxCell id="be6" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.76;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="bB" source="b_p0" target="b_l3"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="1340" y="245"/><mxPoint x="638" y="245"/></Array></mxGeometry></mxCell>')
p2.append(e("be7", "b_c1", "b_l3", "通過", (0, 0.75), (0.5, 0)))
p2.append(e("be8", "b_c1", "b_err", "失敗", (0.5, 1), (0.5, 1), vert=True, pos=-0.85))
p2.append(e("be9", "b_l3", "b_p1", "", (1, 0.5), (0, 0.5)))
# ---- C 升級 ----
band("bC", "升級：Renovate 開的 PR 被 merge（或 just upgrade）", 830, 300)
p2.append(v("c_u", "bC", ELLIPSE(GREEN), "merge PR\n（.version 改了）", 60, 60, 180, 60))
p2.append(v("c_l1", "bC", LEAF(), "下次 just build 走上面\n「不同」分支 → install 新版", 380, 65, 340, 50))
p2.append(v("c_p1", "bC", FILE, ".base/（新版）", 1240, 70, 200, 40))
p2.append(v("c_u2", "bC", ELLIPSE(GREEN), "just diff", 60, 160, 180, 50))
p2.append(v("c_c2", "bC", PURPLE_LEAF, "diff\nimage 內的新版模板 vs 你的初始檔", 800, 155, 340, 60))
p2.append(v("c_p2", "bC", FILE, "Dockerfile 等（你的）", 1240, 165, 200, 40))
p2.append(v("c_u3", "bC", ELLIPSE(GREEN), "看差異，自己決定\n要不要改", 60, 230, 180, 55))
p2.append(e("ce1", "c_u", "c_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ce2", "c_l1", "c_p1", "下次 build 時", (1, 0.5), (0, 0.5), dashed=True))
p2.append(e("ce3", "c_u2", "c_c2", "", (1, 0.5), (0, 0.5)))
p2.append(e("ce4", "c_p2", "c_c2", "讀", (0, 0.5), (1, 0.5)))
p2.append('<mxCell id="ce5" value="印出差異" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="bC" source="c_c2" target="c_u3"><mxGeometry x="0.4" relative="1" as="geometry"><Array as="points"><mxPoint x="970" y="258"/><mxPoint x="300" y="258"/></Array></mxGeometry></mxCell>')
p2.append(v("p2n", "1", NOTE, "四個紫框 = 四個子命令：install（第一次、版本改變時）、init（只有第一次）、verify（每次日常）、diff（升級後由使用者呼叫）。\nRenovate：GitHub 上的機器人，GHCR 有新版就自動開 PR 改 .version；沒有它時用 just upgrade 手動改。", 20, 1150, 1620, 50))
p2 += legend_flow("p2", 40, 1220, files=True)

# ================= Page 3: 流程：版本生命週期 =================
p3 = [v("title", "1", TITLE, "流程：版本生命週期", 40, 20, 700, 30)]
p3.append(v("up", "1", SW(NEUTRAL), "升級", 20, 60, 440, 560))
p3.append(v("c5", "up", LEAF(), "指定新版本（改 .version；手動或機器人 PR）", 20, 50, 380, 40))
p3.append(v("c6", "up", LEAF(), "執行 just → 啟動器自動 install 新版", 20, 110, 380, 40))
p3.append(v("c7", "up", LEAF(), ".<name>/ 整批覆蓋（非 init 的東西全部換新）", 20, 170, 380, 50))
p3.append(v("c8", "up", RHOMBUS, "執行 diff：init.toml 列的檔案\n新版模板有差異？", 70, 240, 280, 100))
p3.append(v("c9", "up", LEAF(), "顯示差異，使用者自行決定是否修改\n（工具不碰使用者檔案）", 20, 370, 380, 60))
p3.append(v("c10", "up", LEAF(), "提交變更（.version + 使用者的修改）", 20, 460, 380, 40))
p3.append(e("c11", "c5", "c6"))
p3.append(e("c12", "c6", "c7"))
p3.append(e("c13", "c7", "c8"))
p3.append(e("c14", "c8", "c9", "有", (0.5, 1), (0.5, 0), vert=True))
p3.append('<mxCell id="c14b" value="無" style="' + EDGE + 'align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="c8" target="c10"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="440" y="350"/><mxPoint x="440" y="540"/></Array></mxGeometry></mxCell>')
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
p3.append(v("c31", "dev", LEAF(), "來源暫時指向本機的工具原始碼\n改工具不必每次發佈 image 就能在專案裡測", 20, 50, 380, 80))
p3 += legend_flow("p3", 40, 1000)

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
p4.append(v("init", "1", SW(NEUTRAL), "init（第一次：建立使用者檔）", 440, 60, 460, 720))
p4.append(v("i0", "init", ELLIPSE(GREEN), "開始 init", 140, 50, 160, 50))
p4.append(v("i1", "init", LEAF(), "讀 init.toml", 120, 130, 200, 40))
p4.append(v("i2", "init", RHOMBUS, "還有項目？", 130, 200, 180, 80))
p4.append(v("i3", "init", LEAF(), "取下一項\n（image 的 dist/src → 專案的 dest）", 100, 315, 240, 50))
p4.append(v("i4", "init", RHOMBUS, "dest 已存在？", 130, 390, 180, 80))
p4.append(v("i5", "init", LEAF(), "略過（保留使用者版本）", 20, 510, 180, 40))
p4.append(v("i6", "init", LEAF(), "從 dist/ 複製建立", 240, 510, 180, 40))
p4.append(v("i7", "init", ELLIPSE(GREEN), "成功結束", 140, 640, 160, 40))
p4.append(e("ie0", "i0", "i1")); p4.append(e("ie1", "i1", "i2"))
p4.append(e("ie2", "i2", "i3", "有", (0.5, 1), (0.5, 0), vert=True))
p4.append(e("ie3", "i3", "i4"))
p4.append(e("ie4", "i4", "i5", "已有", (0, 0.5), (0.5, 0), vert=True))
p4.append(e("ie5", "i4", "i6", "沒有", (1, 0.5), (0.5, 0), vert=True))
p4.append('<mxCell id="ie6" value="沒有了" style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="init" source="i2" target="i7"><mxGeometry x="-0.85" relative="1" as="geometry"><Array as="points"><mxPoint x="440" y="240"/><mxPoint x="440" y="610"/><mxPoint x="220" y="610"/></Array></mxGeometry></mxCell>')
p4.append('<mxCell id="ib1" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i5" target="i2"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="110" y="580"/><mxPoint x="10" y="580"/><mxPoint x="10" y="240"/></Array></mxGeometry></mxCell>')
p4.append('<mxCell id="ib2" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i6" target="i2"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="330" y="580"/><mxPoint x="10" y="580"/><mxPoint x="10" y="240"/></Array></mxGeometry></mxCell>')
# verify
p4.append(v("verify", "1", SW(NEUTRAL), "verify（檢查 install 的產物沒被改）", 940, 60, 440, 480))
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
p4.append(v("diff", "1", SW(NEUTRAL), "diff（升級後：新模板 vs 使用者檔）", 1420, 60, 440, 480))
p4.append(v("d0", "diff", ELLIPSE(GREEN), "開始 diff", 140, 50, 160, 50))
p4.append(v("d1", "diff", LEAF(), "對 init.toml 的每一項：\nimage 內的新版 src vs 專案內的 dest", 100, 130, 240, 50))
p4.append(v("d3", "diff", RHOMBUS, "有差異？", 130, 220, 180, 80))
p4.append(v("d4", "diff", LEAF(), "無差異", 20, 340, 180, 50))
p4.append(v("d5", "diff", LEAF(), "顯示差異", 240, 340, 180, 50))
p4.append(v("d6", "diff", ELLIPSE(GREEN), "結束（不改使用者檔案）", 220, 420, 200, 40))
p4.append(e("de5", "d5", "d6"))
p4.append(e("de6", "d4", "d6", "", (0.5, 1), (0, 0.5)))
p4.append(e("de0", "d0", "d1")); p4.append(e("de2", "d1", "d3"))
p4.append(e("de3", "d3", "d4", "否", (0, 0.5), (0.5, 0), vert=True))
p4.append(e("de4", "d3", "d5", "是", (1, 0.5), (0.5, 0), vert=True))
p4 += legend_flow("p4", 40, 900, purple=False)

# ================= Page 6: 名詞說明 =================
p6 = [v("title", "1", TITLE, "名詞說明", 40, 20, 600, 30)]
terms = [
 ("image", "打包好的程式與檔案，下載後可直接執行"),
 ("容器", "image 執行起來的實例；跑完可以刪掉，image 保留"),
 ("GHCR", "GitHub 提供的 image 倉庫"),
 ("dist", "工具要出貨的那批檔案，全部寫進下游的 .<name>/"),
 ("init.toml", "init 清單：列出 init 時要複製到專案的初始檔；不在清單上的每次 upgrade 都覆蓋"),
 ("指紋（hash）", "由檔案內容算出的一串碼；內容一改就不同"),
 ("印記檔", "安裝時寫下的紀錄（.<name>/.stamp）：版本 + 每個檔案的指紋"),
 (".version", "專案裡的版本清單：一個工具一行 `name = image`；name 決定安裝目錄 .<name>/"),
 (".<name>/", "工具的安裝目錄，例如 base → .base/、harness → .harness/；不進 git，每次 upgrade 整批覆蓋"),
 ("justfile", "使用者的唯一入口；打 just 指令就會執行"),
 ("自動發佈（CI）", "放在 GitHub 上的自動化流程：打包 image 並上傳"),
 ("commit", "git 的一次版本紀錄"),
]
for i, (k, d) in enumerate(terms):
    p6.append(v(f"t{i}k", "1", LEAF(), k, 40, 70 + i * 56, 200, 44))
    p6.append(v(f"t{i}d", "1", TEXT(14) + "align=left;", d, 260, 70 + i * 56, 900, 44))


# ================= Page 7: 原型對照 =================
p7 = [v("title", "1", TITLE, "原型對照（以 base 為例）：proto/ 三個資料夾 ↔ 真實 repo ↔ GHCR", 40, 20, 900, 30)]
p7.append(v("row_t", "1", TEXT(12) + "align=left;", "原始碼（進 git，人維護）", 40, 70, 300, 20))
p7.append(v("row_g", "1", TEXT(12) + "align=left;", "產物（不進 git，CI 產生）", 640, 70, 300, 20))
p7.append(v("row_d", "1", TEXT(12) + "align=left;", "使用端（進 git 的只有前三個）", 1000, 70, 300, 20))

p7.append(v("r_vk", "1", SW(RED), "vendor_kit repo", 40, 100, 300, 200))
p7.append(v("r_vk_t", "r_vk", TEXT(11), "= proto/vendor_kit/", 10, 40, 280, 18))
p7.append(v("f_vk", "r_vk", LEAF(), "vendor_kit\n（安裝工具程式）", 20, 70, 120, 50))
p7.append(v("f_vkdf", "r_vk", LEAF(), "Dockerfile\n（打包食譜）", 160, 70, 120, 50))
p7.append(v("r_vk_n", "r_vk", TEXT(11), "vendor_kit 是產品本體；Dockerfile 只說明怎麼把它裝進 image", 10, 135, 280, 50))

p7.append(v("r_base", "1", SW(GREEN), "base repo", 40, 340, 300, 250))
p7.append(v("r_base_t", "r_base", TEXT(11), "= proto/base/（只放出貨相關的檔）", 10, 40, 280, 18))
p7.append(v("f_dist", "r_base", LEAF(GREY), "dist/\n（全部出貨，含模板）", 20, 70, 260, 50))

p7.append(v("f_man", "r_base", LEAF(), "init.toml\n（init 清單）", 20, 130, 120, 50))
p7.append(v("f_bdf", "r_base", LEAF(), "Dockerfile.dist\n（出貨食譜）", 160, 130, 120, 50))
p7.append(v("r_base_n", "r_base", TEXT(11), "Dockerfile.dist：FROM vendor_kit:v1，再疊上 dist/ 與 init.toml", 10, 190, 280, 50))

p7.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 640, 100, 300, 490))
p7.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:v1", 40, 90, 220, 50))
p7.append(v("g_base", "ghcr", PURPLE_LEAF, "base-dist:v0.1.0", 40, 390, 220, 50))
p7.append(v("g_n", "ghcr", TEXT(11), "原型只 build 到本機，沒有 push；\n正式版由 CI 在打 tag 時 push", 10, 450, 280, 40))

p7.append(v("r_ds", "1", SW(GREEN), "downstream repo", 1080, 100, 340, 490))
p7.append(v("r_ds_t", "r_ds", TEXT(11), "= proto/downstream/（如 urg_node_humble）", 10, 40, 320, 18))
p7.append(v("f_ver", "r_ds", LEAF(), ".version", 20, 70, 140, 40))
p7.append(v("f_just", "r_ds", LEAF(), "justfile", 180, 70, 140, 40))
p7.append(v("f_user", "r_ds", LEAF(GREY), "Dockerfile、.setup.conf…\n（init 建立後歸使用者）", 20, 120, 300, 50))
p7.append(v("f_base", "r_ds", LEAF(), ".base/ ＋ .stamp\n（不進 git，install 寫出）", 20, 390, 300, 50))
p7.append(v("r_ds_n", "r_ds", TEXT(11), "這個 repo 不知道 vendor_kit 存在，\n只認 .version 裡的 base-dist image", 10, 450, 320, 36))

p7.append(e("x1", "f_vkdf", "g_vk", "docker build → push", (1, 0.5), (0, 0.5), offset=(0, -4)))
p7.append(e("x2", "f_bdf", "g_base", "docker build → push", (1, 0.5), (0, 0.5), offset=(0, -4)))
p7.append(e("x3", "g_vk", "g_base", "FROM（基底）", (0.5, 1), (0.5, 0), dashed=True, vert=True))
p7.append(e("x4", "g_base", "f_base", "docker run\n… install", (1, 0.75), (0, 0.75), pos=0.15))
p7.append(e("x5", "f_ver", "g_base", "指定用哪個 image", (0, 0.5), (1, 0.15), pos=-0.6))
p7 += legend_arch("p7", 40, 640)

doc = ('<mxfile host="app.diagrams.net">'
       + page("p1", "1. vendor_kit 架構圖", p1, w=1700, h=1150)
       + page("p1b", "2. 出貨路徑（以 base 為例）", p1b, w=1700)
       + page("p2", "3. 流程：使用者指令", p2, w=1700, h=1320)
       + page("p3", "4. 流程：版本生命週期", p3)
       + page("p4", "5. 流程：vendor_kit 內部", p4, w=1920, h=1000)
       + page("p6", "6. 名詞說明", p6)
       + page("p7", "7. 原型對照（以 base 為例）", p7, h=760)
       + "</mxfile>")
open("/home/cyc/Desktop/vendor-kit_ws/src/dist_distribution.drawio", "w").write(doc)
print(len(doc))
