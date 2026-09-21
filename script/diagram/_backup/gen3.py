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
NOTE = "shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#ffffff;strokeColor=#999999;align=left;spacingLeft=6;fontSize=12;"
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
    c.append(v(f"{prefix}_lg6", "1", TEXT(12) + "align=left;", "實線 = 資料傳輸（線上文字 = 資料）\n虛線 = 基底依賴，或只在特定情況發生", x + 3 * 240 + 440, y, 260, 60))
    return c

def legend_flow(prefix, x, y):
    c = []
    c.append(v(f"{prefix}_lg0", "1", LEGEND_BOX(NEUTRAL), "淺灰：情境分組（無狀態意義）", x, y, 220, 60))
    c.append(v(f"{prefix}_lg1", "1", ELLIPSE(GREEN), "綠：起點／終點", x + 240, y + 10, 130, 40))
    c.append(v(f"{prefix}_lg2", "1", RHOMBUS, "黃：判斷", x + 390, y, 110, 60))
    c.append(v(f"{prefix}_lg3", "1", ELLIPSE(RED), "紅：錯誤終止", x + 520, y + 10, 130, 40))
    c.append(v(f"{prefix}_lg4", "1", PURPLE_LEAF, "紫：container 內執行", x + 670, y + 10, 160, 40))
    c.append(v(f"{prefix}_lg5", "1", LEAF(), "白：步驟", x + 850, y + 10, 88, 40))
    c.append(v(f"{prefix}_lg6", "1", TEXT(12) + "align=left;", "實線 = 執行順序", x + 960, y, 260, 60))
    return c

# ================= Page 1: 架構圖 =================
p1 = [v("title", "1", TITLE, "架構圖：dist 分發（模組 → 最小單元；線上的文字 = 傳輸的資料）", 40, 20, 1000, 30)]

# vendor_kit（新建模組）
p1.append(v("vk", "1", SW(RED), "vendor_kit（安裝引擎）", 40, 80, 320, 320))
p1.append(v("vk_t", "vk", TEXT(), "負責把 image 裡的 dist 寫進 downstream repo；打包成 vendor_kit:vN image，各工具的 dist image 都以它為基底", 10, 40, 300, 36))
p1.append(v("vk_land", "vk", LEAF(), "子命令 land\n依清單把工具檔案寫進 .base/", 20, 78, 135, 46))
p1.append(v("vk_init", "vk", LEAF(), "子命令 init\n首次建立使用者檔案", 165, 78, 135, 46))
p1.append(v("vk_verify", "vk", LEAF(), "子命令 verify\n檢查 .base/ 是否被手改", 20, 132, 135, 46))
p1.append(v("vk_diff", "vk", LEAF(), "子命令 diff\n升級時產生使用者檔案的建議修改", 165, 132, 135, 46))
p1.append(v("vk_manifest", "vk", LEAF(), "manifest 格式定義\n（每個檔案屬於哪一類）", 20, 186, 135, 46))
p1.append(v("vk_stamp", "vk", LEAF(), "印記檔格式\n（安裝版本 + 每檔 hash）", 165, 186, 135, 46))
p1.append(v("vk_docker", "vk", LEAF(), "Dockerfile\n（把引擎打包成 image）", 20, 240, 135, 46))
p1.append(v("vk_ci", "vk", LEAF(), "CI：發佈流程\n（build image → push）", 165, 240, 135, 46))

# base（現有模組）
p1.append(v("base", "1", SW(GREEN), "base（本體不變）", 40, 440, 320, 360))
p1.append(v("base_t", "base", TEXT(), "本體不變；只新增右下三個白色單元", 10, 40, 300, 36))
p1.append(v("b_wrapper", "base", LEAF(GREY), "dist/wrapper\n（build、run、exec、stop 指令腳本）", 20, 78, 135, 46))
p1.append(v("b_lib", "base", LEAF(GREY), "dist/lib\n（共用函式庫）", 165, 78, 135, 46))
p1.append(v("b_runtime", "base", LEAF(GREY), "dist/runtime\n（container 內執行的腳本）", 20, 132, 135, 46))
p1.append(v("b_tpl_df", "base", LEAF(GREY), "模板：Dockerfile", 165, 132, 135, 46))
p1.append(v("b_tpl_ep", "base", LEAF(GREY), "模板：entrypoint", 20, 186, 135, 46))
p1.append(v("b_tpl_conf", "base", LEAF(GREY), "模板：.setup.conf", 165, 186, 135, 46))
p1.append(v("b_tpl_main", "base", LEAF(GREY), "模板：main.yaml", 20, 240, 135, 46))
p1.append(v("b_manifest", "base", LEAF(), "manifest\n（宣告 dist 每個檔案的類別）", 165, 240, 135, 46))
p1.append(v("b_dockerfile", "base", LEAF(), "Dockerfile.dist\n（以引擎 image 為基底打包 dist）", 20, 294, 135, 46))
p1.append(v("base_ci", "base", LEAF(), "CI：打 tag 時\n發佈 base-dist image", 165, 294, 135, 46))

# 其他工具（新建模組）
p1.append(v("other", "1", SW(RED), "其他工具（agent_harness …）", 40, 840, 320, 100))
p1.append(v("other_ci", "other", LEAF(), "CI：同樣以引擎 image 為基底，發佈自己的 dist image", 20, 45, 280, 40))

# GHCR（外部）
p1.append(v("ghcr", "1", SW(YELLOW), "GHCR", 420, 80, 300, 860))
p1.append(v("g_t", "ghcr", TEXT(), "規則：舊版本不刪、tag 不覆蓋", 10, 40, 280, 30))
p1.append(v("g_vk", "ghcr", PURPLE_LEAF, "引擎 image\nvendor_kit:vN", 20, 258, 220, 60))
p1.append(v("g_base", "ghcr", PURPLE_LEAF, "base-dist:vX image\n內容：引擎 + dist + 模板 + manifest\n標籤：base 的 commit SHA、版本號", 20, 636, 220, 80))
p1.append(v("g_other", "ghcr", PURPLE_LEAF, "其他工具的 dist image\nagent_harness-dist:vY …", 20, 815, 220, 40))

# downstream（新建模組）
DX, DY = 800, 80
p1.append(v("ds", "1", SW(RED), "downstream repo", DX, DY, 800, 460))
p1.append(v("sa", "ds", SW(RED), "啟動器（進 git）", 20, 70, 250, 250))
p1.append(v("c_ref", "sa", LEAF(), ".base-ref\n（記錄要用的版本）", 15, 60, 105, 50))
p1.append(v("c_just", "sa", LEAF(), "justfile\n（使用者唯一入口）", 130, 60, 105, 50))
p1.append(v("sa_t", "sa", TEXT(), "justfile 極少變動；\n.base-ref 由使用者或 Renovate 機器人改版本", 10, 125, 115, 100))
p1.append(v("sb", "ds", SW(RED), "使用者檔案（進 git）", 290, 70, 230, 250))
p1.append(v("c_dockerfile", "sb", LEAF(), "Dockerfile", 15, 50, 95, 40))
p1.append(v("c_entry", "sb", LEAF(), "entrypoint", 120, 50, 95, 40))
p1.append(v("c_main", "sb", LEAF(), "main.yaml", 15, 100, 95, 40))
p1.append(v("c_conf", "sb", LEAF(), ".setup.conf", 120, 100, 95, 40))
p1.append(v("c_hooks", "sb", LEAF(), "hooks（需要才建立）", 15, 150, 200, 40))
p1.append(v("sb_t", "sb", TEXT(), "首次安裝時由引擎建立，之後由使用者維護，工具不再覆寫", 10, 195, 210, 50))
p1.append(v("sc", "ds", SW(RED), "工具安裝區（不進 git）", 540, 70, 240, 250))
p1.append(v("c_wrapper", "sc", LEAF(GREY), ".base/wrapper", 15, 50, 100, 40))
p1.append(v("c_lib", "sc", LEAF(GREY), ".base/lib", 125, 50, 100, 40))
p1.append(v("c_runtime", "sc", LEAF(GREY), ".base/runtime", 15, 100, 100, 40))
p1.append(v("c_stamp", "sc", LEAF(), "印記檔\n（版本 + hash）", 125, 100, 100, 40))
p1.append(v("c_compose", "sc", LEAF(), "compose.yaml", 15, 150, 100, 40))
p1.append(v("c_env", "sc", LEAF(), ".env.generated", 125, 150, 100, 40))
p1.append(v("sc_t", "sc", TEXT(), "每次安裝整批覆寫；手改會被 verify 擋下", 10, 195, 220, 50))
p1.append(v("ds_engine", "ds", PURPLE_LEAF, "引擎 container（跑 base-dist:vX）\n以主機使用者身分執行、只掛載 repo、跑完即刪", 20, 370, 250, 70))

# Host（外部）
p1.append(v("host", "1", SW(YELLOW), "主機", 1640, 80, 200, 460))
p1.append(v("h_t", "host", TEXT(), "主機只需安裝這三個", 10, 40, 180, 30))
p1.append(v("h_docker", "host", LEAF(GREY), "Docker daemon", 20, 80, 160, 40))
p1.append(v("h_just", "host", LEAF(GREY), "just", 20, 140, 160, 40))
p1.append(v("h_git", "host", LEAF(GREY), "git", 20, 200, 160, 40))

# edges（資料）
p1.append(e("e_vk_push", "vk_ci", "g_vk", "引擎 image（push）", (1, 0.5), (0, 0.5)))
p1.append(e("e_base_push", "base_ci", "g_base", "base-dist image（push）", (1, 0.5), (0, 0.5)))
p1.append(e("e_other_push", "other_ci", "g_other", "其他工具 dist image（push）", (1, 0.5), (0, 0.5)))
p1.append(e("e_from_base", "g_vk", "g_base", "以引擎 image 為基底", (0.5, 1), (0.5, 0), dashed=True))
p1.append(e("e_from_other", "g_vk", "g_other", "以引擎 image 為基底", (1, 0.5), (1, 0.5), dashed=True))
p1.append(e("e_pull", "g_base", "ds_engine", "下載 image（pull）", (1, 0.5), (0, 0.5)))
p1.append(e("e_ref", "c_ref", "c_just", "要用的版本", (1, 0.5), (0, 0.5)))
p1.append(e("e_run", "c_just", "ds_engine", "docker run 參數：版本、使用者 UID/GID、repo 路徑", (0.5, 1), (0.73, 0)))
p1.append(e("e_verb", "c_just", "sc", "使用者下的指令（build / run …）", (0.5, 0), (0.5, 0)))
p1.append(e("e_conf", "c_conf", "sc", "使用者設定（stage、掛載、port …）", (1, 0.5), (0, 0.48)))
p1.append(e("e_land", "ds_engine", "sc", "寫入：工具檔案 + 印記檔 ／ 讀回：印記檔（驗證用）", (1, 0.7), (0.75, 1), both=True))
p1.append(e("e_seed", "ds_engine", "sb", "首次安裝才建立的使用者檔案", (1, 0.3), (0.5, 1), dashed=True))
p1.append(e("e_compose", "sc", "h_docker", "docker compose 指令 + 產生的 compose.yaml", (1, 0.5), (0, 0.5)))
p1.append(v("p1_note", "1", NOTE, "名詞：「安裝」= 引擎把 image 內的 dist 寫進 downstream repo 的 .base/；\n「印記檔」= 安裝時寫下的紀錄（版本 + 每個檔案的 hash），用來偵測手改與判斷是否需重新安裝。", 800, 560, 800, 60))
p1 += legend_arch("p1", 40, 1000)

# ================= Page 2: 流程：launcher =================
p2 = [v("title", "1", TITLE, "流程：啟動器（justfile）— 使用者每次執行 just 指令", 40, 20, 900, 30)]
p2.append(v("c4", "1", ELLIPSE(GREEN), "使用者執行 just 指令", 300, 60, 160, 50))
p2.append(v("c5", "1", LEAF(), "讀 .base-ref，取得要用的版本", 280, 140, 200, 40))
p2.append(v("c6", "1", RHOMBUS, "該版本 image\n已在本機？", 290, 210, 180, 90))
p2.append(v("c7", "1", LEAF(), "從 GHCR 下載 image", 40, 230, 160, 50))
p2.append(v("c8", "1", RHOMBUS, ".base/ 已安裝的版本\n= .base-ref 的版本？", 270, 340, 220, 100))
p2.append(v("c9", "1", PURPLE_LEAF, "起 container 執行引擎 land\n把 dist 寫進 .base/（首次同時建立使用者檔案）", 560, 360, 240, 60))
p2.append(v("c9n", "1", NOTE, "引擎內部怎麼做，見第 4 頁", 560, 440, 240, 40))
p2.append(v("c13", "1", RHOMBUS, "執行引擎 verify：\n.base/ 沒被手改？", 270, 480, 220, 100))
p2.append(v("c14", "1", ELLIPSE(RED), "中止：.base/ 被手改\n提示使用者重新安裝", 20, 500, 180, 60))
p2.append(v("c15", "1", LEAF(), "呼叫 .base/ 內的 wrapper 腳本", 280, 640, 200, 50))
p2.append(v("c16", "1", ELLIPSE(GREEN), "交給 docker compose 執行", 300, 730, 160, 50))
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
p3.append(v("c5", "up", LEAF(), "修改 .base-ref 到新版本（手動或 Renovate PR）", 20, 50, 380, 40))
p3.append(v("c6", "up", LEAF(), "執行 just：啟動器發現版本不同，用新版 image 重新安裝", 20, 110, 380, 40))
p3.append(v("c7", "up", LEAF(), ".base/ 內的工具檔案：整批覆寫", 20, 170, 380, 50))
p3.append(v("c8", "up", RHOMBUS, "新版是否要求使用者檔案\n（Dockerfile 等）配合修改？", 70, 240, 280, 100))
p3.append(v("c9", "up", LEAF(), "執行引擎 diff 產生建議修改（patch）\n使用者自行決定是否套用；工具不碰使用者檔案、不自動 commit", 20, 370, 380, 60))
p3.append(v("c10", "up", LEAF(), "commit .base-ref + 使用者自己的修改", 20, 460, 380, 40))
p3.append(e("c11", "c5", "c6"))
p3.append(e("c12", "c6", "c7"))
p3.append(e("c13", "c7", "c8"))
p3.append(e("c14", "c8", "c9", "是", (0.5, 1), (0.5, 0)))
p3.append(e("c14b", "c8", "c10", "否", (1, 0.5), (1, 0.5)))
p3.append(e("c15", "c9", "c10"))
p3.append(v("c16", "1", NOTE, "重點：升級的程式在「新版 image」裡，\n不在 repo 內的舊腳本裡，\n所以不會發生「舊工具升級自己」失敗的問題。", 460, 100, 300, 90))
p3.append(v("rb", "1", SW(NEUTRAL), "回退", 460, 230, 300, 190))
p3.append(v("c18", "rb", LEAF(), "用 git 把 .base-ref 改回舊版本", 20, 50, 260, 40))
p3.append(v("c19", "rb", LEAF(), "執行 just：用舊版 image 重新安裝\n（.base/ 不進 git，所以不需要額外的回退紀錄）", 20, 110, 260, 50))
p3.append(e("c20", "c18", "c19"))
p3.append(v("bug", "1", SW(NEUTRAL), "追查問題（從 commit 追到原始碼）", 800, 60, 420, 420))
p3.append(v("c22", "bug", LEAF(), "出問題的 downstream commit", 20, 50, 380, 50))
p3.append(v("c23", "bug", LEAF(), "看該 commit 的 .base-ref → 得知用的版本\n（記 tag 還是 digest，待決）", 20, 130, 380, 50))
p3.append(v("c24", "bug", PURPLE_LEAF, "看該版本 image 的標籤 → 得知 base 的 commit SHA", 20, 210, 380, 50))
p3.append(v("c25", "bug", LEAF(), "base repo 該 commit 的原始碼", 20, 290, 380, 50))
p3.append(v("c29", "bug", NOTE, "對 .base-ref 做 git bisect，就能找出是哪次升級引入問題", 20, 355, 380, 50))
p3.append(e("c26", "c22", "c23"))
p3.append(e("c27", "c23", "c24"))
p3.append(e("c28", "c24", "c25"))
p3.append(v("dev", "1", SW(NEUTRAL), "本機開發模式（改 base 的時候）", 800, 510, 420, 150))
p3.append(v("c31", "dev", LEAF(), "把來源暫時改成本機的 base 原始碼目錄\n改 base 時不必每次發佈 image 就能在 downstream 測\n（設計初期就要預留這個開關）", 20, 50, 380, 80))
p3 += legend_flow("p3", 40, 1000)

# ================= Page 4: 流程：引擎 =================
p4 = [v("title", "1", TITLE, "流程：引擎（vendor_kit）— 在 container 內執行的三個子命令", 40, 20, 900, 30)]
# land
p4.append(v("land", "1", SW(NEUTRAL), "land：把 dist 寫進 repo（首次同時 init）", 20, 60, 560, 760))
p4.append(v("l0", "land", ELLIPSE(GREEN), "開始 land", 200, 50, 160, 50))
p4.append(v("l1", "land", LEAF(), "讀 image 內的 manifest（檔案清單與類別）", 180, 130, 200, 40))
p4.append(v("l2", "land", LEAF(), "逐一處理清單中的每個檔案", 180, 200, 200, 40))
p4.append(v("l3", "land", RHOMBUS, "這個檔案\n屬於哪一類？", 190, 270, 180, 80))
p4.append(v("l4", "land", LEAF(), "工具擁有：\n寫進 .base/，記下 hash", 20, 380, 160, 50))
p4.append(v("l5", "land", RHOMBUS, "首次建立類：\nrepo 裡已有這個檔案？", 190, 370, 180, 80))
p4.append(v("l6", "land", LEAF(), "可選類：\n不建立", 400, 380, 140, 50))
p4.append(v("l7", "land", LEAF(), "用模板建立（= init）", 100, 480, 170, 40))
p4.append(v("l8", "land", LEAF(), "不動，保留使用者的版本", 290, 480, 170, 40))
p4.append(v("l9", "land", LEAF(), "寫印記檔：本次版本 + 每個檔案的 hash", 180, 570, 200, 50))
p4.append(v("l10", "land", ELLIPSE(GREEN), "完成（exit 0）", 200, 660, 160, 50))
p4.append(e("le0", "l0", "l1"))
p4.append(e("le1", "l1", "l2"))
p4.append(e("le2", "l2", "l3"))
p4.append(e("le3", "l3", "l4", "工具擁有", (0, 0.5), (0.5, 0)))
p4.append(e("le4", "l3", "l5", "首次建立", (0.5, 1), (0.5, 0)))
p4.append(e("le5", "l3", "l6", "可選", (1, 0.5), (0.5, 0)))
p4.append(e("le6", "l5", "l7", "沒有", (0, 0.5), (0.5, 0)))
p4.append(e("le7", "l5", "l8", "已有", (1, 0.5), (0.5, 0)))
p4.append(e("le8", "l4", "l9", "", (0.5, 1), (0, 0.5)))
p4.append(e("le9", "l7", "l9", "", (0.5, 1), (0.25, 0)))
p4.append(e("le10", "l8", "l9", "", (0.5, 1), (0.75, 0)))
p4.append(e("le11", "l6", "l9", "", (0.5, 1), (1, 0.5)))
p4.append(e("le12", "l9", "l10"))
# verify
p4.append(v("verify", "1", SW(NEUTRAL), "verify：檢查 .base/ 有沒有被手改", 620, 60, 440, 480))
p4.append(v("v0", "verify", ELLIPSE(GREEN), "開始 verify", 140, 50, 160, 50))
p4.append(v("v1", "verify", LEAF(), "讀印記檔（安裝時記下的 hash）", 120, 130, 200, 40))
p4.append(v("v2", "verify", LEAF(), "重新計算 .base/ 每個檔案的 hash", 120, 200, 200, 40))
p4.append(v("v3", "verify", RHOMBUS, "全部相符？", 130, 270, 180, 80))
p4.append(v("v4", "verify", ELLIPSE(GREEN), "通過（exit 0）", 20, 390, 160, 50))
p4.append(v("v5", "verify", ELLIPSE(RED), "失敗（exit 非 0）\n列出被改過的檔案", 240, 390, 180, 50))
p4.append(e("ve0", "v0", "v1"))
p4.append(e("ve1", "v1", "v2"))
p4.append(e("ve2", "v2", "v3"))
p4.append(e("ve3", "v3", "v4", "是", (0, 0.5), (0.5, 0)))
p4.append(e("ve4", "v3", "v5", "否", (1, 0.5), (0.5, 0)))
# diff
p4.append(v("diff", "1", SW(NEUTRAL), "diff：升級時產生使用者檔案的建議修改", 1100, 60, 440, 480))
p4.append(v("d0", "diff", ELLIPSE(GREEN), "開始 diff", 140, 50, 160, 50))
p4.append(v("d1", "diff", LEAF(), "用新版模板產生一份\n「新版應有的樣子」", 100, 130, 240, 50))
p4.append(v("d2", "diff", LEAF(), "跟使用者現在的檔案比對", 100, 210, 240, 40))
p4.append(v("d3", "diff", RHOMBUS, "有差異？", 130, 280, 180, 80))
p4.append(v("d4", "diff", ELLIPSE(GREEN), "無需變更（exit 0）", 20, 400, 180, 50))
p4.append(v("d5", "diff", LEAF(), "把建議修改（patch）印到畫面\n（不直接改使用者檔案）", 240, 395, 180, 60))
p4.append(e("de0", "d0", "d1"))
p4.append(e("de1", "d1", "d2"))
p4.append(e("de2", "d2", "d3"))
p4.append(e("de3", "d3", "d4", "否", (0, 0.5), (0.5, 0)))
p4.append(e("de4", "d3", "d5", "是", (1, 0.5), (0.5, 0)))
p4.append(v("p4n", "1", NOTE, "三個子命令共同前提：container 以主機使用者的 UID/GID 執行、只掛載 repo；\n引擎版本由 image tag 決定，不讀 repo 內任何腳本（所以不會有「舊工具升級自己」的問題）。", 620, 570, 920, 60))
p4 += legend_flow("p4", 40, 1000)

doc = ('<mxfile host="app.diagrams.net">'
       + page("p1", "1. 架構圖", p1, w=1900)
       + page("p2", "2. 流程：launcher", p2)
       + page("p3", "3. 流程：版本生命週期", p3)
       + page("p4", "4. 流程：引擎", p4)
       + "</mxfile>")
open("/home/cyc/Desktop/vendor-kit_ws/src/dist_distribution.drawio", "w").write(doc)
print(len(doc))
