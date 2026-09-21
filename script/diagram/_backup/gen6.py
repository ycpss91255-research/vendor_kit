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

def e(id, src, tgt, label="", exit=None, entry=None, dashed=False, both=False):
    st = EDGE
    if exit:  st += f"exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;"
    if entry: st += f"entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
    if dashed: st += "dashed=1;"
    if both: st += "startArrow=block;startFill=1;"
    return (f'<mxCell id="{id}" value="{esc(label)}" style="{st}" edge="1" parent="1" source="{src}" target="{tgt}">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>')

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

def legend_flow(prefix, x, y):
    c = []
    c.append(v(f"{prefix}_lg0", "1", LEGEND_BOX(NEUTRAL), "淺灰：情境分組（無狀態意義）", x, y, 220, 60))
    c.append(v(f"{prefix}_lg1", "1", ELLIPSE(GREEN), "綠：起點／終點", x + 240, y + 10, 130, 40))
    c.append(v(f"{prefix}_lg2", "1", RHOMBUS, "黃：判斷", x + 390, y, 110, 60))
    c.append(v(f"{prefix}_lg3", "1", ELLIPSE(RED), "紅：錯誤終止", x + 520, y + 10, 130, 40))
    c.append(v(f"{prefix}_lg4", "1", PURPLE_LEAF, "紫：在容器內執行", x + 670, y + 10, 160, 40))
    c.append(v(f"{prefix}_lg5", "1", LEAF(), "白：步驟", x + 850, y + 10, 88, 40))
    c.append(v(f"{prefix}_lg6", "1", TEXT(12) + "align=left;", "實線 = 執行順序", x + 960, y, 260, 60))
    return c



# ================= Page 1: vendor_kit 架構圖 =================
p1 = [v("title", "1", TITLE, "vendor_kit 架構圖（模組 → 最小單元；線上文字 = 傳的資料）", 40, 20, 900, 30)]
VX, VY = 480, 140
p1.append(v("user", "1", SW(YELLOW), "使用者", 40, VY, 140, 740))
p1.append(v("u_cmd", "user", LEAF(GREY), "指令", 26, 90, 88, 40))
p1.append(v("u_out", "user", LEAF(GREY), "畫面", 26, 640, 88, 40))
p1.append(v("img", "1", SW(YELLOW), "image 內容", 200, 300, 180, 240))
p1.append(v("i_list", "img", LEAF(), "檔案清單", 46, 50, 88, 40))
p1.append(v("i_dist", "img", LEAF(GREY), "工具檔案", 46, 110, 88, 40))
p1.append(v("i_tpl", "img", LEAF(GREY), "模板", 46, 170, 88, 40))
p1.append(v("vk", "1", SW(RED), "vendor_kit", VX, VY, 480, 740))
p1.append(v("m_cli", "vk", SW(RED), "命令介面", 20, 50, 200, 140))
p1.append(v("cli_land", "m_cli", LEAF(), "land", 12, 45, 88, 40))
p1.append(v("cli_init", "m_cli", LEAF(), "init", 104, 45, 88, 40))
p1.append(v("cli_verify", "m_cli", LEAF(), "verify", 12, 92, 88, 40))
p1.append(v("cli_diff", "m_cli", LEAF(), "diff", 104, 92, 88, 40))
p1.append(v("m_list", "vk", SW(RED), "清單處理", 20, 210, 200, 170))
p1.append(v("ls_read", "m_list", LEAF(), "讀取", 12, 45, 88, 40))
p1.append(v("ls_check", "m_list", LEAF(), "驗證", 104, 45, 88, 40))
p1.append(v("ls_class", "m_list", LEAF(), "分類", 12, 92, 88, 40))
p1.append(v("ls_t", "m_list", TEXT(11), "工具檔／初始檔／選用檔", 104, 92, 92, 40))
p1.append(v("m_tpl", "vk", SW(RED), "模板", 20, 400, 200, 140))
p1.append(v("tp_render", "m_tpl", LEAF(), "渲染", 12, 45, 88, 40))
p1.append(v("tp_vars", "m_tpl", LEAF(), "變數", 104, 45, 88, 40))
p1.append(v("m_diff", "vk", SW(RED), "差異比對", 20, 560, 200, 140))
p1.append(v("df_cmp", "m_diff", LEAF(), "比對", 12, 45, 88, 40))
p1.append(v("df_patch", "m_diff", LEAF(), "產生差異", 104, 45, 88, 40))
p1.append(v("m_write", "vk", SW(RED), "檔案寫入", 260, 210, 200, 170))
p1.append(v("wr_copy", "m_write", LEAF(), "寫入", 12, 45, 88, 40))
p1.append(v("wr_read", "m_write", LEAF(), "讀回", 104, 45, 88, 40))
p1.append(v("wr_perm", "m_write", LEAF(), "權限設定", 12, 92, 88, 40))
p1.append(v("wr_atomic", "m_write", LEAF(), "整批替換", 104, 92, 88, 40))
p1.append(v("m_stamp", "vk", SW(RED, 16), "印記", 350, 400, 110, 140))
p1.append(v("st_hash", "m_stamp", LEAF(), "指紋計算", 11, 45, 88, 40))
p1.append(v("st_cmp", "m_stamp", LEAF(), "比對", 11, 92, 88, 40))
p1.append(v("m_report", "vk", SW(RED), "回報", 260, 560, 200, 140))
p1.append(v("rp_msg", "m_report", LEAF(), "訊息", 12, 45, 88, 40))
p1.append(v("rp_code", "m_report", LEAF(), "結束狀態", 104, 45, 88, 40))
p1.append(v("proj", "1", SW(YELLOW), "專案目錄", 1000, VY, 200, 740))
p1.append(v("p_stamp", "proj", LEAF(), "印記檔", 56, 241, 88, 40))
p1.append(v("p_base", "proj", LEAF(), ".base/", 56, 292, 88, 40))
p1.append(v("p_user", "proj", LEAF(GREY), "使用者檔案", 56, 343, 88, 40))
p1.append(e("a1", "u_cmd", "m_cli", "命令、參數", (1, 0.5), (0, 0.5)))
p1.append(e("a2", "m_cli", "m_list", "命令參數", (0.5, 1), (0.5, 0)))
p1.append(e("a3", "i_list", "m_list", "檔案清單", (1, 0.5), (0, 0.3)))
p1.append(e("a4", "i_dist", "m_list", "檔案內容", (1, 0.5), (0, 0.6)))
p1.append(e("a5", "i_tpl", "m_list", "模板", (1, 0.5), (0, 0.9)))
p1.append(e("a6", "m_list", "m_write", "工具檔", (1, 0.3), (0, 0.3)))
p1.append(e("a7", "m_list", "m_tpl", "初始檔清單", (0.5, 1), (0.5, 0)))
p1.append(e("a8", "m_tpl", "m_write", "初始檔內容", (0.8, 0), (0.1, 1)))
p1.append(e("a9", "m_write", "m_stamp", "指紋、印記", (0.8, 1), (0.64, 0), both=True))
p1.append(e("a10", "m_write", "p_stamp", "印記檔", (1, 0.3), (0, 0.5), both=True))
p1.append(e("a11", "m_write", "p_base", "工具檔", (1, 0.6), (0, 0.5), both=True))
p1.append(e("a12", "m_write", "p_user", "初始檔", (1, 0.9), (0, 0.5), dashed=True))
p1.append('<mxCell id="a13" value="使用者檔案" style="' + EDGE + 'exitX=0.35;exitY=1;exitDx=0;exitDy=0;entryX=0.9;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="m_write" target="m_diff"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="810" y="690"/><mxPoint x="680" y="690"/></Array></mxGeometry></mxCell>')
p1.append(e("a14", "m_tpl", "m_diff", "新版模板", (0.5, 1), (0.5, 0)))
p1.append(e("a15", "m_stamp", "m_report", "檢查結果", (0.5, 1), (0.77, 0)))
p1.append(e("a16", "m_diff", "m_report", "差異", (1, 0.5), (0, 0.5)))
p1.append(e("a17", "m_report", "u_out", "訊息、結束狀態", (0.5, 1), (1, 0.5)))
p1 += legend_arch("p1", 40, 960)

# ================= Page 2: 出貨路徑 =================
p1b = [v("title", "1", TITLE, "出貨路徑：vendor_kit 與 base 如何送到各專案", 40, 20, 900, 30)]
p1b.append(v("vk", "1", SW(RED), "vendor_kit", 40, 80, 240, 130))
p1b.append(v("vk_ci", "vk", LEAF(), "自動發佈", 76, 60, 88, 40))
p1b.append(v("base", "1", SW(GREEN), "base", 40, 250, 240, 250))
p1b.append(v("b_dist", "base", LEAF(GREY), "dist", 22, 50, 88, 40))
p1b.append(v("b_tpl", "base", LEAF(GREY), "模板", 130, 50, 88, 40))
p1b.append(v("b_list", "base", LEAF(), "檔案清單", 22, 110, 88, 40))
p1b.append(v("b_df", "base", LEAF(), "Dockerfile", 130, 110, 88, 40))
p1b.append(v("base_ci", "base", LEAF(), "自動發佈", 76, 180, 88, 40))
p1b.append(v("other", "1", SW(RED), "其他工具", 40, 540, 240, 130))
p1b.append(v("other_ci", "other", LEAF(), "自動發佈", 76, 60, 88, 40))
p1b.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 360, 80, 260, 590))
p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 60, 200, 40))
p1b.append(v("g_base", "ghcr", PURPLE_LEAF, "base-dist:vX", 30, 350, 200, 40))
p1b.append(v("g_other", "ghcr", PURPLE_LEAF, "其他工具-dist:vY", 30, 520, 200, 40))
p1b.append(v("ds", "1", SW(RED), "使用 base 的專案", 700, 80, 720, 420))
p1b.append(v("sa", "ds", SW(RED), "啟動器", 20, 50, 200, 150))
p1b.append(v("c_ref", "sa", LEAF(), ".base-ref", 12, 50, 88, 40))
p1b.append(v("c_just", "sa", LEAF(), "justfile", 104, 50, 88, 40))
p1b.append(v("sa_t", "sa", TEXT(11), "進 git", 12, 100, 180, 30))
p1b.append(v("sb", "ds", SW(RED), "使用者檔案", 260, 50, 200, 150))
p1b.append(v("c_df", "sb", LEAF(), "Dockerfile", 12, 50, 88, 40))
p1b.append(v("c_conf", "sb", LEAF(), ".setup.conf", 104, 50, 88, 40))
p1b.append(v("sb_t", "sb", TEXT(11), "進 git；第一次安裝時建立", 12, 100, 180, 30))
p1b.append(v("sc", "ds", SW(RED), ".base/", 500, 50, 200, 150))
p1b.append(v("c_tools", "sc", LEAF(), "工具檔", 12, 50, 88, 40))
p1b.append(v("c_stamp", "sc", LEAF(), "印記檔", 104, 50, 88, 40))
p1b.append(v("sc_t", "sc", TEXT(11), "不進 git；每次安裝整批替換", 12, 100, 180, 30))
p1b.append(v("ds_engine", "ds", PURPLE_LEAF, "安裝容器（base-dist:vX）", 20, 300, 200, 60))
p1b.append(v("ds_t", "ds", TEXT(11), "以使用者身分執行，跑完即刪", 20, 365, 200, 30))
p1b.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1460, 80, 160, 420))
p1b.append(v("h_docker", "host", LEAF(GREY), "Docker", 36, 60, 88, 40))
p1b.append(v("h_just", "host", LEAF(GREY), "just", 36, 120, 88, 40))
p1b.append(v("h_git", "host", LEAF(GREY), "git", 36, 180, 88, 40))
p1b.append(e("b1", "vk_ci", "g_vk", "image", (1, 0.5), (0, 0.5)))
p1b.append(e("b2", "base_ci", "g_base", "image", (1, 0.5), (0, 0.5)))
p1b.append(e("b3", "other_ci", "g_other", "image", (1, 0.5), (0, 0.5)))
p1b.append(e("b4", "g_vk", "g_base", "基底 image", (0.5, 1), (0.5, 0), dashed=True))
p1b.append(e("b5", "g_vk", "g_other", "基底 image", (1, 0.5), (1, 0.5), dashed=True))
p1b.append(e("b6", "g_base", "ds_engine", "image", (1, 0.5), (0, 0.5)))
p1b.append(e("b7", "c_ref", "c_just", "版本", (1, 0.5), (0, 0.5)))
p1b.append(e("b8", "c_just", "ds_engine", "版本、身分、路徑", (0.5, 1), (0.74, 0)))
p1b.append(e("b9", "ds_engine", "sc", "工具檔、印記檔", (1, 0.5), (0.5, 1), both=True))
p1b.append(e("b10", "ds_engine", "sb", "初始檔", (1, 0.2), (0.5, 1), dashed=True))
p1b.append(e("b11", "sc", "h_docker", "compose 指令", (1, 0.3), (0, 0.5)))
p1b += legend_arch("p1b", 40, 900)

# ================= Page 6: 名詞說明 =================
p6 = [v("title", "1", TITLE, "名詞說明", 40, 20, 600, 30)]
terms = [
 ("image", "打包好的程式與檔案，下載後可直接執行"),
 ("容器", "image 執行起來的實例；跑完可以刪掉，image 保留"),
 ("GHCR", "GitHub 提供的 image 倉庫"),
 ("dist", "base 要送給各專案用的那批工具檔案"),
 ("檔案清單（manifest）", "列出每個檔案，以及它屬於「工具擁有／第一次建立／可選」哪一類"),
 ("指紋（hash）", "由檔案內容算出的一串碼；內容一改就不同"),
 ("印記檔", "安裝時寫下的紀錄：版本 + 每個檔案的指紋"),
 (".base-ref", "專案裡的一行文字，寫著要用 base 的哪個版本"),
 ("justfile", "使用者的唯一入口；打 just 指令就會執行"),
 ("自動發佈（CI）", "放在 GitHub 上的自動化流程：打包 image 並上傳"),
 ("commit", "git 的一次版本紀錄"),
]
for i, (k, d) in enumerate(terms):
    p6.append(v(f"t{i}k", "1", LEAF(), k, 40, 70 + i * 56, 200, 44))
    p6.append(v(f"t{i}d", "1", TEXT(14) + "align=left;", d, 260, 70 + i * 56, 900, 44))
# ================= Page 2: 流程：launcher =================
p2 = [v("title", "1", TITLE, "流程：啟動器（justfile）— 每次執行 just 指令", 40, 20, 900, 30)]
p2.append(v("c4", "1", ELLIPSE(GREEN), "執行 just 指令", 300, 60, 160, 50))
p2.append(v("c5", "1", LEAF(), "讀取版本（.base-ref）", 280, 140, 200, 40))
p2.append(v("c6", "1", RHOMBUS, "image 已下載？", 290, 210, 180, 90))
p2.append(v("c7", "1", LEAF(), "下載 image", 40, 230, 160, 50))
p2.append(v("c8", "1", RHOMBUS, ".base/ 版本\n與 .base-ref 一致？", 270, 340, 220, 100))
p2.append(v("c9", "1", PURPLE_LEAF, "啟動安裝容器，執行 land\n（安裝工具檔到 .base/）", 560, 360, 240, 60))
p2.append(v("c9n", "1", NOTE, "land 內部步驟見第 5 頁", 820, 370, 180, 40))
p2.append(v("c13", "1", RHOMBUS, "執行 verify：\n工具檔完整？", 270, 480, 220, 100))
p2.append(v("c14", "1", ELLIPSE(RED), "中止：.base/ 被改過\n請重新安裝", 20, 500, 180, 60))
p2.append(v("c15", "1", LEAF(), "執行 .base/ 內對應指令", 280, 640, 200, 50))
p2.append(v("c16", "1", ELLIPSE(GREEN), "啟動專案容器", 300, 730, 160, 50))
p2.append(e("c17", "c4", "c5"))
p2.append(e("c18", "c5", "c6"))
p2.append(e("c19", "c6", "c7", "還沒", (0, 0.5), (1, 0.5)))
p2.append(e("c20", "c6", "c8", "已下載", (0.5, 1), (0.5, 0)))
p2.append(e("c21", "c7", "c8", "", (0.5, 1), (0, 0.5)))
p2.append(e("c22", "c8", "c9", "不一致", (1, 0.5), (0, 0.5)))
p2.append(e("c23", "c8", "c13", "一致", (0.5, 1), (0.5, 0)))
p2.append(e("c24", "c9", "c15", "安裝完成", (0.5, 1), (1, 0.5)))
p2.append(e("c29", "c13", "c14", "被改過", (0, 0.5), (1, 0.5)))
p2.append(e("c30", "c13", "c15", "完整", (0.5, 1), (0.5, 0)))
p2.append(e("c31", "c15", "c16"))
p2 += legend_flow("p2", 40, 1000)

# ================= Page 3: 流程：版本生命週期 =================
p3 = [v("title", "1", TITLE, "流程：版本生命週期", 40, 20, 700, 30)]
p3.append(v("up", "1", SW(NEUTRAL), "升級", 20, 60, 440, 560))
p3.append(v("c5", "up", LEAF(), "指定新版本（改 .base-ref；手動或機器人 PR）", 20, 50, 380, 40))
p3.append(v("c6", "up", LEAF(), "執行 just → 啟動器用新版 image 重新安裝", 20, 110, 380, 40))
p3.append(v("c7", "up", LEAF(), ".base/ 工具檔：整批替換", 20, 170, 380, 50))
p3.append(v("c8", "up", RHOMBUS, "執行 diff：\n新版模板與使用者檔案有差異？", 70, 240, 280, 100))
p3.append(v("c9", "up", LEAF(), "顯示差異，使用者自行決定是否修改\n（工具不碰使用者檔案）", 20, 370, 380, 60))
p3.append(v("c10", "up", LEAF(), "提交變更（.base-ref + 使用者的修改）", 20, 460, 380, 40))
p3.append(e("c11", "c5", "c6"))
p3.append(e("c12", "c6", "c7"))
p3.append(e("c13", "c7", "c8"))
p3.append(e("c14", "c8", "c9", "是", (0.5, 1), (0.5, 0)))
p3.append('<mxCell id="c14b" value="否" style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="c8" target="c10"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="440" y="350"/><mxPoint x="440" y="540"/></Array></mxGeometry></mxCell>')
p3.append(e("c15", "c9", "c10"))
p3.append(v("c16", "1", NOTE, "升級程式在新版 image 裡，不在專案的舊腳本裡，\n所以不會有「舊工具幫自己升級」的問題。", 490, 100, 290, 60))
p3.append(v("rb", "1", SW(NEUTRAL), "回退", 490, 230, 290, 190))
p3.append(v("c18", "rb", LEAF(), "把 .base-ref 改回舊版本", 20, 50, 260, 40))
p3.append(v("c19", "rb", LEAF(), "執行 just → 用舊版 image 重新安裝\n（使用者檔案不會自動回復）", 20, 110, 260, 50))
p3.append(e("c20", "c18", "c19"))
p3.append(v("bug", "1", SW(NEUTRAL), "追查問題", 800, 60, 420, 420))
p3.append(v("c22", "bug", LEAF(), "出問題的專案 commit", 20, 50, 380, 50))
p3.append(v("c23", "bug", LEAF(), "該 commit 的 .base-ref → 用的版本", 20, 130, 380, 50))
p3.append(v("c24", "bug", LEAF(), "該版本 image 的附註 → base 的 commit", 20, 210, 380, 50))
p3.append(v("c25", "bug", LEAF(), "base 該 commit 的原始碼", 20, 290, 380, 50))
p3.append(v("c29", "bug", NOTE, "對 .base-ref 做 git bisect 即可找出出問題的升級", 20, 355, 380, 50))
p3.append(e("c26", "c22", "c23"))
p3.append(e("c27", "c23", "c24"))
p3.append(e("c28", "c24", "c25"))
p3.append(v("dev", "1", SW(NEUTRAL), "本機開發模式（待設計）", 800, 510, 420, 150))
p3.append(v("c31", "dev", LEAF(), "來源暫時指向本機的 base 原始碼\n改 base 不必每次發佈 image 就能在專案裡測", 20, 50, 380, 80))
p3 += legend_flow("p3", 40, 1000)

# ================= Page 4: 流程：引擎 =================
p4 = [v("title", "1", TITLE, "流程：安裝工具（vendor_kit）三個子命令", 40, 20, 900, 30)]
# land
p4.append(v("land", "1", SW(NEUTRAL), "land（安裝）", 20, 60, 640, 820))
p4.append(v("l0", "land", ELLIPSE(GREEN), "開始 land", 200, 50, 160, 50))
p4.append(v("l1", "land", LEAF(), "讀取檔案清單", 180, 130, 200, 40))
p4.append(v("l1b", "land", LEAF(), "清空 .base/（整批替換）", 180, 190, 200, 40))
p4.append(v("l2", "land", LEAF(), "取下一個檔案", 180, 250, 200, 40))
p4.append(v("l3", "land", RHOMBUS, "檔案類別？", 190, 320, 180, 80))
p4.append(v("l4", "land", LEAF(), "工具檔：\n寫入 .base/，記指紋", 20, 430, 160, 50))
p4.append(v("l5", "land", RHOMBUS, "初始檔：\n專案裡已存在？", 190, 420, 180, 80))
p4.append(v("l6", "land", LEAF(), "選用檔：\n有指定才建立", 480, 430, 140, 50))
p4.append(v("l7", "land", LEAF(), "用模板建立（init）", 230, 530, 150, 40))
p4.append(v("l8", "land", LEAF(), "保留使用者版本", 400, 530, 150, 40))
p4.append(v("l9", "land", RHOMBUS, "還有檔案？", 190, 600, 180, 80))
p4.append(v("l10", "land", LEAF(), "寫入印記（版本 + 工具檔指紋）", 180, 710, 200, 40))
p4.append(v("l11", "land", ELLIPSE(GREEN), "成功結束", 200, 770, 160, 40))
p4.append(e("le0", "l0", "l1"))
p4.append(e("le1", "l1", "l1b"))
p4.append(e("le1b", "l1b", "l2"))
p4.append(e("le2", "l2", "l3"))
p4.append(e("le3", "l3", "l4", "工具檔", (0, 0.5), (0.5, 0)))
p4.append(e("le4", "l3", "l5", "初始檔", (0.5, 1), (0.5, 0)))
p4.append(e("le5", "l3", "l6", "選用檔", (1, 0.5), (0.5, 0)))
p4.append(e("le6", "l5", "l7", "沒有", (0, 0.5), (0.5, 0)))
p4.append(e("le7", "l5", "l8", "已有", (1, 0.5), (0.5, 0)))
p4.append(e("le8", "l4", "l9", "", (0.5, 1), (0.15, 0)))
p4.append(e("le9", "l7", "l9", "", (0.5, 1), (0.4, 0)))
p4.append(e("le10", "l8", "l9", "", (0.5, 1), (0.75, 0)))
p4.append(e("le11", "l6", "l9", "", (0.5, 1), (1, 0.5)))
p4.append(e("le12", "l9", "l10", "沒有了", (0.5, 1), (0.5, 0)))
p4.append(e("le13", "l10", "l11"))
p4.append('<mxCell id="le14" value="還有" style="' + EDGE + 'exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="land" source="l9" target="l2"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="10" y="640"/><mxPoint x="10" y="270"/></Array></mxGeometry></mxCell>')
# verify
p4.append(v("verify", "1", SW(NEUTRAL), "verify（檢查）", 700, 60, 440, 480))
p4.append(v("v0", "verify", ELLIPSE(GREEN), "開始 verify", 140, 50, 160, 50))
p4.append(v("v1", "verify", LEAF(), "讀取印記", 120, 130, 200, 40))
p4.append(v("v2", "verify", LEAF(), "重新計算工具檔指紋", 120, 200, 200, 40))
p4.append(v("v3", "verify", RHOMBUS, "全部相符？", 130, 270, 180, 80))
p4.append(v("v4", "verify", ELLIPSE(GREEN), "通過", 20, 390, 160, 50))
p4.append(v("v5", "verify", ELLIPSE(RED), "失敗：列出被改的檔案", 240, 390, 180, 50))
p4.append(e("ve0", "v0", "v1"))
p4.append(e("ve1", "v1", "v2"))
p4.append(e("ve2", "v2", "v3"))
p4.append(e("ve3", "v3", "v4", "是", (0, 0.5), (0.5, 0)))
p4.append(e("ve4", "v3", "v5", "否", (1, 0.5), (0.5, 0)))
# diff
p4.append(v("diff", "1", SW(NEUTRAL), "diff（比對）", 1180, 60, 440, 480))
p4.append(v("d0", "diff", ELLIPSE(GREEN), "開始 diff", 140, 50, 160, 50))
p4.append(v("d1", "diff", LEAF(), "產生新版範本", 100, 130, 240, 50))
p4.append(v("d2", "diff", LEAF(), "與使用者檔案比對", 100, 210, 240, 40))
p4.append(v("d3", "diff", RHOMBUS, "有差異？", 130, 280, 180, 80))
p4.append(v("d4", "diff", ELLIPSE(GREEN), "不需要改", 20, 400, 180, 50))
p4.append(v("d5", "diff", LEAF(), "顯示差異\n（不改使用者檔案）", 240, 395, 180, 60))
p4.append(e("de0", "d0", "d1"))
p4.append(e("de1", "d1", "d2"))
p4.append(e("de2", "d2", "d3"))
p4.append(e("de3", "d3", "d4", "否", (0, 0.5), (0.5, 0)))
p4.append(e("de4", "d3", "d5", "是", (1, 0.5), (0.5, 0)))
#p4.append(v("p4n", "1", NOTE, "三個子命令共同前提：容器以使用者本人的身分執行（寫出來的檔案才會是使用者的，不是 root 的）、只能碰這個專案；\n安裝工具的版本由 image 決定，不讀專案裡的任何腳本（所以不會有「舊工具幫自己升級」的問題）。", 620, 570, 920, 60))
p4 += legend_flow("p4", 40, 1050)

doc = ('<mxfile host="app.diagrams.net">'
       + page("p1", "1. vendor_kit 架構圖", p1, w=1700)
       + page("p1b", "2. 出貨路徑", p1b, w=1700)
       + page("p2", "3. 流程：啟動器", p2)
       + page("p3", "4. 流程：版本生命週期", p3)
       + page("p4", "5. 流程：安裝工具", p4, w=1700, h=1150)
       + page("p6", "6. 名詞說明", p6)
       + "</mxfile>")
open("/home/cyc/Desktop/vendor-kit_ws/src/dist_distribution.drawio", "w").write(doc)
print(len(doc))
