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

# ================= Page 1: 架構圖 =================
p1 = [v("title", "1", TITLE, "架構圖：base 工具怎麼送到各專案（模組 → 最小單元；線上的文字 = 傳輸的內容）", 40, 20, 1000, 30)]

# vendor_kit（新建模組）
p1.append(v("vk", "1", SW(RED), "vendor_kit（安裝工具）", 40, 80, 320, 320))
p1.append(v("vk_t", "vk", TEXT(), "負責把 base 的工具檔案寫進各專案；本身也打包成 image，其他工具的 image 都以它為基底", 10, 40, 300, 36))
p1.append(v("vk_land", "vk", LEAF(), "子命令 land（安裝）\n依清單把工具檔案寫進專案的 .base/", 20, 78, 135, 46))
p1.append(v("vk_init", "vk", LEAF(), "子命令 init（初始化）\n第一次安裝時建立使用者要改的檔案", 165, 78, 135, 46))
p1.append(v("vk_verify", "vk", LEAF(), "子命令 verify（檢查）\n確認 .base/ 沒有被人手動改過", 20, 132, 135, 46))
p1.append(v("vk_diff", "vk", LEAF(), "子命令 diff（比對）\n升級時列出使用者檔案建議怎麼改", 165, 132, 135, 46))
p1.append(v("vk_manifest", "vk", LEAF(), "檔案清單（manifest）格式\n定義每個檔案屬於哪一類", 20, 186, 135, 46))
p1.append(v("vk_stamp", "vk", LEAF(), "印記檔格式\n記錄安裝的版本 + 每個檔案的指紋", 165, 186, 135, 46))
p1.append(v("vk_docker", "vk", LEAF(), "Dockerfile\n（把安裝工具打包成 image）", 20, 240, 135, 46))
p1.append(v("vk_ci", "vk", LEAF(), "自動發佈流程（CI）\n打包 image → 上傳到倉庫", 165, 240, 135, 46))

# base（現有模組）
p1.append(v("base", "1", SW(GREEN), "base（現有工具，本體不變）", 40, 440, 320, 360))
p1.append(v("base_t", "base", TEXT(), "現有內容都不動；只新增右下三個白色的部分", 10, 40, 300, 36))
p1.append(v("b_wrapper", "base", LEAF(GREY), "dist/wrapper\n（build、run、exec、stop 這些指令）", 20, 78, 135, 46))
p1.append(v("b_lib", "base", LEAF(GREY), "dist/lib\n（共用函式庫）", 165, 78, 135, 46))
p1.append(v("b_runtime", "base", LEAF(GREY), "dist/runtime\n（在容器裡面跑的腳本）", 20, 132, 135, 46))
p1.append(v("b_tpl_df", "base", LEAF(GREY), "模板：Dockerfile", 165, 132, 135, 46))
p1.append(v("b_tpl_ep", "base", LEAF(GREY), "模板：entrypoint", 20, 186, 135, 46))
p1.append(v("b_tpl_conf", "base", LEAF(GREY), "模板：.setup.conf", 165, 186, 135, 46))
p1.append(v("b_tpl_main", "base", LEAF(GREY), "模板：main.yaml", 20, 240, 135, 46))
p1.append(v("b_manifest", "base", LEAF(), "檔案清單（manifest）\n宣告 dist 每個檔案的類別", 165, 240, 135, 46))
p1.append(v("b_dockerfile", "base", LEAF(), "Dockerfile.dist\n（把 dist 疊在安裝工具 image 上）", 20, 294, 135, 46))
p1.append(v("base_ci", "base", LEAF(), "自動發佈流程（CI）\n標記版本時上傳 base-dist image", 165, 294, 135, 46))

# 其他工具（新建模組）
p1.append(v("other", "1", SW(RED), "其他工具（agent_harness …）", 40, 840, 320, 100))
p1.append(v("other_ci", "other", LEAF(), "自動發佈流程：同樣疊在安裝工具 image 上，上傳自己的 image", 20, 45, 280, 40))

# GHCR（外部）
p1.append(v("ghcr", "1", SW(YELLOW), "GHCR（GitHub 的 image 倉庫）", 420, 80, 300, 860))
p1.append(v("g_t", "ghcr", TEXT(), "規則：舊版本永遠保留、版本名稱不重複使用", 10, 40, 280, 30))
p1.append(v("g_vk", "ghcr", PURPLE_LEAF, "安裝工具 image\nvendor_kit:vN", 20, 258, 220, 60))
p1.append(v("g_base", "ghcr", PURPLE_LEAF, "base-dist:vX image\n內容：安裝工具 + dist + 模板 + 檔案清單\n附註：來自 base 的哪個 commit、版本號", 20, 636, 220, 80))
p1.append(v("g_other", "ghcr", PURPLE_LEAF, "其他工具的 dist image\nagent_harness-dist:vY …", 20, 815, 220, 40))

# downstream（新建模組）
DX, DY = 800, 80
p1.append(v("ds", "1", SW(RED), "使用 base 的專案（downstream repo）", DX, DY, 800, 460))
p1.append(v("sa", "ds", SW(RED), "啟動器（進 git）", 20, 70, 250, 250))
p1.append(v("c_ref", "sa", LEAF(), ".base-ref\n（一行文字：要用哪個版本）", 15, 60, 105, 50))
p1.append(v("c_just", "sa", LEAF(), "justfile\n（使用者只需要記這個入口）", 130, 60, 105, 50))
p1.append(v("sa_t", "sa", TEXT(), "justfile 幾乎不用改；\n.base-ref 由使用者手動改，或由機器人自動開升級 PR", 10, 125, 115, 100))
p1.append(v("sb", "ds", SW(RED), "使用者檔案（進 git）", 290, 70, 230, 250))
p1.append(v("c_dockerfile", "sb", LEAF(), "Dockerfile", 15, 50, 95, 40))
p1.append(v("c_entry", "sb", LEAF(), "entrypoint", 120, 50, 95, 40))
p1.append(v("c_main", "sb", LEAF(), "main.yaml", 15, 100, 95, 40))
p1.append(v("c_conf", "sb", LEAF(), ".setup.conf", 120, 100, 95, 40))
p1.append(v("c_hooks", "sb", LEAF(), "hooks（需要才建立）", 15, 150, 200, 40))
p1.append(v("sb_t", "sb", TEXT(), "第一次安裝時建立，之後屬於使用者，工具不會再覆蓋", 10, 195, 210, 50))
p1.append(v("sc", "ds", SW(RED), "工具安裝區（不進 git）", 540, 70, 240, 250))
p1.append(v("c_wrapper", "sc", LEAF(GREY), ".base/wrapper", 15, 50, 100, 40))
p1.append(v("c_lib", "sc", LEAF(GREY), ".base/lib", 125, 50, 100, 40))
p1.append(v("c_runtime", "sc", LEAF(GREY), ".base/runtime", 15, 100, 100, 40))
p1.append(v("c_stamp", "sc", LEAF(), "印記檔\n（版本 + 指紋）", 125, 100, 100, 40))
p1.append(v("c_compose", "sc", LEAF(), "compose.yaml", 15, 150, 100, 40))
p1.append(v("c_env", "sc", LEAF(), ".env.generated", 125, 150, 100, 40))
p1.append(v("sc_t", "sc", TEXT(), "每次安裝整批覆蓋；手動改了會被 verify 擋下", 10, 195, 220, 50))
p1.append(v("ds_engine", "ds", PURPLE_LEAF, "安裝工具的容器（執行 base-dist:vX）\n以使用者本人身分執行、只能碰這個專案、跑完就刪", 20, 370, 250, 70))

# Host（外部）
p1.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1640, 80, 200, 460))
p1.append(v("h_t", "host", TEXT(), "只需要裝這三個軟體", 10, 40, 180, 30))
p1.append(v("h_docker", "host", LEAF(GREY), "Docker daemon", 20, 80, 160, 40))
p1.append(v("h_just", "host", LEAF(GREY), "just", 20, 140, 160, 40))
p1.append(v("h_git", "host", LEAF(GREY), "git", 20, 200, 160, 40))

# edges（資料）
p1.append(e("e_vk_push", "vk_ci", "g_vk", "安裝工具 image（上傳）", (1, 0.5), (0, 0.5)))
p1.append(e("e_base_push", "base_ci", "g_base", "base-dist image（上傳）", (1, 0.5), (0, 0.5)))
p1.append(e("e_other_push", "other_ci", "g_other", "其他工具的 image（上傳）", (1, 0.5), (0, 0.5)))
p1.append(e("e_from_base", "g_vk", "g_base", "以安裝工具 image 為基底", (0.5, 1), (0.5, 0), dashed=True))
p1.append(e("e_from_other", "g_vk", "g_other", "以安裝工具 image 為基底", (1, 0.5), (1, 0.5), dashed=True))
p1.append(e("e_pull", "g_base", "ds_engine", "下載 image", (1, 0.5), (0, 0.5)))
p1.append(e("e_ref", "c_ref", "c_just", "要用的版本", (1, 0.5), (0, 0.5)))
p1.append(e("e_run", "c_just", "ds_engine", "啟動容器的參數：版本、使用者身分、專案路徑", (0.5, 1), (0.73, 0)))
p1.append(e("e_verb", "c_just", "sc", "使用者下的指令（build / run …）", (0.5, 0), (0.5, 0)))
p1.append(e("e_conf", "c_conf", "sc", "使用者的設定（要跑哪個階段、掛哪些資料夾、開哪些 port）", (1, 0.5), (0, 0.48)))
p1.append(e("e_land", "ds_engine", "sc", "寫入：工具檔案 + 印記檔 ／ 讀回：印記檔（用來檢查）", (1, 0.7), (0.75, 1), both=True))
p1.append(e("e_seed", "ds_engine", "sb", "首次安裝才建立的使用者檔案", (1, 0.3), (0.5, 1), dashed=True))
p1.append(e("e_compose", "sc", "h_docker", "啟動專案容器的指令 + 產生的 compose.yaml", (1, 0.5), (0, 0.5)))
p1.append(v("p1_note", "1", NOTE, "名詞說明\n・image：打包好的程式與檔案，下載後可直接執行；容器 = image 執行起來的那個實例\n・dist：base 要送給各專案用的那批工具檔案\n・檔案清單（manifest）：列出每個檔案、以及它屬於「工具擁有／第一次建立／可選」哪一類\n・指紋（hash）：由檔案內容算出的一串碼，內容一改就不同，用來偵測檔案有沒有被動過\n・印記檔：安裝時寫下的紀錄（版本 + 每個檔案的指紋），用來判斷要不要重裝、有沒有被手改\n・CI：放在 GitHub 上的自動化流程；commit：git 的一次版本紀錄", 800, 560, 1040, 130))
p1 += legend_arch("p1", 40, 1000)

# ================= Page 2: 流程：launcher =================
p2 = [v("title", "1", TITLE, "流程：啟動器（justfile）— 使用者每次打 just 指令時，背後發生什麼", 40, 20, 900, 30)]
p2.append(v("c4", "1", ELLIPSE(GREEN), "使用者執行 just 指令", 300, 60, 160, 50))
p2.append(v("c5", "1", LEAF(), "讀 .base-ref，取得要用的版本", 280, 140, 200, 40))
p2.append(v("c6", "1", RHOMBUS, "該版本 image\n已在本機？", 290, 210, 180, 90))
p2.append(v("c7", "1", LEAF(), "從倉庫下載 image", 40, 230, 160, 50))
p2.append(v("c8", "1", RHOMBUS, ".base/ 已安裝的版本\n= .base-ref 的版本？", 270, 340, 220, 100))
p2.append(v("c9", "1", PURPLE_LEAF, "啟動安裝工具的容器，執行 land\n把工具檔案寫進 .base/（第一次會同時建立使用者檔案）", 560, 360, 240, 60))
p2.append(v("c9n", "1", NOTE, "安裝工具內部怎麼做，見第 4 頁", 560, 440, 240, 40))
p2.append(v("c13", "1", RHOMBUS, "執行 verify：\n.base/ 沒被手動改過？", 270, 480, 220, 100))
p2.append(v("c14", "1", ELLIPSE(RED), "停止並報錯：.base/ 被手動改過\n請使用者重新安裝", 20, 500, 180, 60))
p2.append(v("c15", "1", LEAF(), "執行 .base/ 裡對應的指令腳本", 280, 640, 200, 50))
p2.append(v("c16", "1", ELLIPSE(GREEN), "啟動專案的容器", 300, 730, 160, 50))
p2.append(e("c17", "c4", "c5"))
p2.append(e("c18", "c5", "c6"))
p2.append(e("c19", "c6", "c7", "否", (0, 0.5), (1, 0.5)))
p2.append(e("c20", "c6", "c8", "是", (0.5, 1), (0.5, 0)))
p2.append(e("c21", "c7", "c8", "", (0.5, 1), (0, 0.5)))
p2.append(e("c22", "c8", "c9", "不同（要重新安裝）", (1, 0.5), (0, 0.5)))
p2.append(e("c23", "c8", "c13", "相同", (0.5, 1), (0.5, 0)))
p2.append(e("c24", "c9", "c15", "安裝完成", (0.5, 1), (1, 0.5)))
p2.append(e("c29", "c13", "c14", "否", (0, 0.5), (1, 0.5)))
p2.append(e("c30", "c13", "c15", "是", (0.5, 1), (0.5, 0)))
p2.append(e("c31", "c15", "c16"))
p2 += legend_flow("p2", 40, 1000)

# ================= Page 3: 流程：版本生命週期 =================
p3 = [v("title", "1", TITLE, "流程：版本生命週期（升級／回退／追查問題／本機開發）", 40, 20, 700, 30)]
p3.append(v("up", "1", SW(NEUTRAL), "升級", 20, 60, 420, 560))
p3.append(v("c5", "up", LEAF(), "把 .base-ref 改成新版本（手動改，或機器人自動開 PR）", 20, 50, 380, 40))
p3.append(v("c6", "up", LEAF(), "執行 just：啟動器發現版本不同，自動用新版 image 重新安裝", 20, 110, 380, 40))
p3.append(v("c7", "up", LEAF(), ".base/ 內的工具檔案：整批覆寫", 20, 170, 380, 50))
p3.append(v("c8", "up", RHOMBUS, "新版有沒有要求\n使用者檔案配合修改？", 70, 240, 280, 100))
p3.append(v("c9", "up", LEAF(), "執行 diff 列出建議修改\n使用者自己決定要不要改；工具不碰使用者檔案、不自動 commit", 20, 370, 380, 60))
p3.append(v("c10", "up", LEAF(), "commit .base-ref + 使用者自己的修改", 20, 460, 380, 40))
p3.append(e("c11", "c5", "c6"))
p3.append(e("c12", "c6", "c7"))
p3.append(e("c13", "c7", "c8"))
p3.append(e("c14", "c8", "c9", "是", (0.5, 1), (0.5, 0)))
p3.append(e("c14b", "c8", "c10", "否", (1, 0.5), (1, 0.5)))
p3.append(e("c15", "c9", "c10"))
p3.append(v("c16", "1", NOTE, "重點：負責升級的程式在「新版 image」裡，\n不是專案裡的舊腳本，\n所以不會發生「舊工具幫自己升級」而失敗的問題。", 460, 100, 300, 90))
p3.append(v("rb", "1", SW(NEUTRAL), "回退", 460, 230, 300, 190))
p3.append(v("c18", "rb", LEAF(), "用 git 把 .base-ref 改回舊版本", 20, 50, 260, 40))
p3.append(v("c19", "rb", LEAF(), "執行 just：用舊版 image 重新安裝\n（.base/ 不進 git，所以不需要額外的回退紀錄）", 20, 110, 260, 50))
p3.append(e("c20", "c18", "c19"))
p3.append(v("bug", "1", SW(NEUTRAL), "追查問題（從出事的專案一路追到 base 原始碼）", 800, 60, 420, 420))
p3.append(v("c22", "bug", LEAF(), "出問題的專案 commit", 20, 50, 380, 50))
p3.append(v("c23", "bug", LEAF(), "看那時的 .base-ref → 知道用的是哪個版本\n（記版本名稱還是內容指紋，待決）", 20, 130, 380, 50))
p3.append(v("c24", "bug", PURPLE_LEAF, "看那個版本 image 的附註 → 知道來自 base 的哪個 commit", 20, 210, 380, 50))
p3.append(v("c25", "bug", LEAF(), "base repo 該 commit 的原始碼", 20, 290, 380, 50))
p3.append(v("c29", "bug", NOTE, "對 .base-ref 的修改紀錄做二分搜尋（git bisect），就能找出是哪次升級出問題", 20, 355, 380, 50))
p3.append(e("c26", "c22", "c23"))
p3.append(e("c27", "c23", "c24"))
p3.append(e("c28", "c24", "c25"))
p3.append(v("dev", "1", SW(NEUTRAL), "本機開發模式（自己在改 base 的時候）", 800, 510, 420, 150))
p3.append(v("c31", "dev", LEAF(), "把來源暫時指到自己電腦上的 base 原始碼\n這樣改 base 不用每次都發佈 image，就能直接在專案裡測\n（設計一開始就要預留這個開關）", 20, 50, 380, 80))
p3 += legend_flow("p3", 40, 1000)

# ================= Page 4: 流程：引擎 =================
p4 = [v("title", "1", TITLE, "流程：安裝工具（vendor_kit）— 在容器內執行的三個子命令", 40, 20, 900, 30)]
# land
p4.append(v("land", "1", SW(NEUTRAL), "land（安裝）：把工具檔案寫進專案，第一次會同時初始化", 20, 60, 560, 760))
p4.append(v("l0", "land", ELLIPSE(GREEN), "開始 land", 200, 50, 160, 50))
p4.append(v("l1", "land", LEAF(), "讀 image 內的檔案清單（每個檔案與它的類別）", 180, 130, 200, 40))
p4.append(v("l2", "land", LEAF(), "逐一處理清單中的每個檔案", 180, 200, 200, 40))
p4.append(v("l3", "land", RHOMBUS, "這個檔案\n屬於哪一類？", 190, 270, 180, 80))
p4.append(v("l4", "land", LEAF(), "工具擁有：\n寫進 .base/，記下指紋", 20, 380, 160, 50))
p4.append(v("l5", "land", RHOMBUS, "第一次建立類：\n專案裡已經有這個檔案了？", 190, 370, 180, 80))
p4.append(v("l6", "land", LEAF(), "可選類：\n不建立", 400, 380, 140, 50))
p4.append(v("l7", "land", LEAF(), "用模板建立（= init）", 100, 480, 170, 40))
p4.append(v("l8", "land", LEAF(), "不動，保留使用者的版本", 290, 480, 170, 40))
p4.append(v("l9", "land", LEAF(), "寫印記檔：這次的版本 + 每個檔案的指紋", 180, 570, 200, 50))
p4.append(v("l10", "land", ELLIPSE(GREEN), "成功結束", 200, 660, 160, 50))
p4.append(e("le0", "l0", "l1"))
p4.append(e("le1", "l1", "l2"))
p4.append(e("le2", "l2", "l3"))
p4.append(e("le3", "l3", "l4", "工具擁有", (0, 0.5), (0.5, 0)))
p4.append(e("le4", "l3", "l5", "第一次建立", (0.5, 1), (0.5, 0)))
p4.append(e("le5", "l3", "l6", "可選", (1, 0.5), (0.5, 0)))
p4.append(e("le6", "l5", "l7", "沒有", (0, 0.5), (0.5, 0)))
p4.append(e("le7", "l5", "l8", "已有", (1, 0.5), (0.5, 0)))
p4.append(e("le8", "l4", "l9", "", (0.5, 1), (0, 0.5)))
p4.append(e("le9", "l7", "l9", "", (0.5, 1), (0.25, 0)))
p4.append(e("le10", "l8", "l9", "", (0.5, 1), (0.75, 0)))
p4.append(e("le11", "l6", "l9", "", (0.5, 1), (1, 0.5)))
p4.append(e("le12", "l9", "l10"))
# verify
p4.append(v("verify", "1", SW(NEUTRAL), "verify（檢查）：.base/ 有沒有被手動改過", 620, 60, 440, 480))
p4.append(v("v0", "verify", ELLIPSE(GREEN), "開始 verify", 140, 50, 160, 50))
p4.append(v("v1", "verify", LEAF(), "讀印記檔（安裝時記下的指紋）", 120, 130, 200, 40))
p4.append(v("v2", "verify", LEAF(), "重新算 .base/ 每個檔案現在的指紋", 120, 200, 200, 40))
p4.append(v("v3", "verify", RHOMBUS, "全部相符？", 130, 270, 180, 80))
p4.append(v("v4", "verify", ELLIPSE(GREEN), "通過", 20, 390, 160, 50))
p4.append(v("v5", "verify", ELLIPSE(RED), "失敗：列出被改過的檔案", 240, 390, 180, 50))
p4.append(e("ve0", "v0", "v1"))
p4.append(e("ve1", "v1", "v2"))
p4.append(e("ve2", "v2", "v3"))
p4.append(e("ve3", "v3", "v4", "是", (0, 0.5), (0.5, 0)))
p4.append(e("ve4", "v3", "v5", "否", (1, 0.5), (0.5, 0)))
# diff
p4.append(v("diff", "1", SW(NEUTRAL), "diff（比對）：升級時列出使用者檔案建議怎麼改", 1100, 60, 440, 480))
p4.append(v("d0", "diff", ELLIPSE(GREEN), "開始 diff", 140, 50, 160, 50))
p4.append(v("d1", "diff", LEAF(), "用新版模板產生一份\n「新版應有的樣子」", 100, 130, 240, 50))
p4.append(v("d2", "diff", LEAF(), "跟使用者現在的檔案比對", 100, 210, 240, 40))
p4.append(v("d3", "diff", RHOMBUS, "有差異？", 130, 280, 180, 80))
p4.append(v("d4", "diff", ELLIPSE(GREEN), "不需要改", 20, 400, 180, 50))
p4.append(v("d5", "diff", LEAF(), "把建議的修改印到畫面上\n（不直接動使用者的檔案）", 240, 395, 180, 60))
p4.append(e("de0", "d0", "d1"))
p4.append(e("de1", "d1", "d2"))
p4.append(e("de2", "d2", "d3"))
p4.append(e("de3", "d3", "d4", "否", (0, 0.5), (0.5, 0)))
p4.append(e("de4", "d3", "d5", "是", (1, 0.5), (0.5, 0)))
p4.append(v("p4n", "1", NOTE, "三個子命令共同前提：容器以使用者本人的身分執行（寫出來的檔案才會是使用者的，不是 root 的）、只能碰這個專案；\n安裝工具的版本由 image 決定，不讀專案裡的任何腳本（所以不會有「舊工具幫自己升級」的問題）。", 620, 570, 920, 60))
p4 += legend_flow("p4", 40, 1000)

doc = ('<mxfile host="app.diagrams.net">'
       + page("p1", "1. 架構圖", p1, w=1900)
       + page("p2", "2. 流程：launcher", p2)
       + page("p3", "3. 流程：版本生命週期", p3)
       + page("p4", "4. 流程：引擎", p4)
       + "</mxfile>")
open("/home/cyc/Desktop/vendor-kit_ws/src/dist_distribution.drawio", "w").write(doc)
print(len(doc))
