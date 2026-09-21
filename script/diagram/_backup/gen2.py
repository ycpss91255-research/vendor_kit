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
    c.append(v(f"{prefix}_lg6", "1", TEXT(12) + "align=left;", "實線 = 資料傳輸（標籤為資料）\n虛線 = 依賴（FROM）或僅特定情況", x + 3 * 240 + 440, y, 260, 60))
    return c

def legend_flow(prefix, x, y):
    c = []
    c.append(v(f"{prefix}_lg0", "1", LEGEND_BOX(NEUTRAL), "淺灰：情境分組（無狀態意義）", x, y, 220, 60))
    c.append(v(f"{prefix}_lg1", "1", ELLIPSE(GREEN), "綠：起點／終點", x + 240, y + 10, 130, 40))
    c.append(v(f"{prefix}_lg2", "1", RHOMBUS, "黃：判斷", x + 390, y, 110, 60))
    c.append(v(f"{prefix}_lg3", "1", ELLIPSE(RED), "紅：錯誤終止", x + 520, y + 10, 130, 40))
    c.append(v(f"{prefix}_lg4", "1", PURPLE_LEAF, "紫：container 內執行", x + 670, y + 10, 160, 40))
    c.append(v(f"{prefix}_lg5", "1", LEAF(), "白：步驟", x + 850, y + 10, 88, 40))
    c.append(v(f"{prefix}_lg6", "1", TEXT(12) + "align=left;", "實線 = 控制流；虛線 = 跨頁參照", x + 960, y, 260, 60))
    return c

# ================= Page 1: 架構圖 =================
p1 = [v("title", "1", TITLE, "架構圖：dist 分發（模組 → 最小單元；線段 = 傳輸的資料）", 40, 20, 1000, 30)]

# vendor_kit（新建模組）
p1.append(v("vk", "1", SW(RED), "vendor_kit（落地引擎）", 40, 80, 320, 320))
p1.append(v("vk_t", "vk", TEXT(), "通用引擎；打包成 vendor_kit:vN image，各工具的 dist image 以它為基底", 10, 40, 300, 36))
p1.append(v("vk_land", "vk", LEAF(), "CLI land\n依 manifest 寫 tool-owned", 20, 78, 135, 46))
p1.append(v("vk_init", "vk", LEAF(), "CLI init\n渲染 seed-once 模板", 165, 78, 135, 46))
p1.append(v("vk_verify", "vk", LEAF(), "CLI verify\nhash 比對印記", 20, 132, 135, 46))
p1.append(v("vk_diff", "vk", LEAF(), "CLI diff\nseed-once 變更 patch", 165, 132, 135, 46))
p1.append(v("vk_manifest", "vk", LEAF(), "manifest 規格\n（檔案類別）", 20, 186, 135, 46))
p1.append(v("vk_stamp", "vk", LEAF(), "印記格式\n（版本 + hash）", 165, 186, 135, 46))
p1.append(v("vk_docker", "vk", LEAF(), "Dockerfile\n（引擎 image）", 20, 240, 135, 46))
p1.append(v("vk_ci", "vk", LEAF(), "CI release", 165, 240, 135, 46))

# base（現有模組）
p1.append(v("base", "1", SW(GREEN), "base（本體不變）", 40, 440, 320, 360))
p1.append(v("base_t", "base", TEXT(), "本體不變；新增 manifest、Dockerfile.dist、release workflow", 10, 40, 300, 36))
p1.append(v("b_wrapper", "base", LEAF(GREY), "dist/wrapper\nbuild / run / exec / stop", 20, 78, 135, 46))
p1.append(v("b_lib", "base", LEAF(GREY), "dist/lib", 165, 78, 135, 46))
p1.append(v("b_runtime", "base", LEAF(GREY), "dist/runtime 腳本", 20, 132, 135, 46))
p1.append(v("b_tpl_df", "base", LEAF(GREY), "模板 Dockerfile", 165, 132, 135, 46))
p1.append(v("b_tpl_ep", "base", LEAF(GREY), "模板 entrypoint", 20, 186, 135, 46))
p1.append(v("b_tpl_conf", "base", LEAF(GREY), "模板 .setup.conf", 165, 186, 135, 46))
p1.append(v("b_tpl_main", "base", LEAF(GREY), "模板 main.yaml", 20, 240, 135, 46))
p1.append(v("b_manifest", "base", LEAF(), "manifest\n（宣告每檔類別）", 165, 240, 135, 46))
p1.append(v("b_dockerfile", "base", LEAF(), "Dockerfile.dist\nFROM vendor_kit:vN", 20, 294, 135, 46))
p1.append(v("base_ci", "base", LEAF(), "CI release\n（tag 觸發）", 165, 294, 135, 46))

# 其他工具（新建模組）
p1.append(v("other", "1", SW(RED), "其他工具（agent_harness …）", 40, 840, 320, 100))
p1.append(v("other_ci", "other", LEAF(), "CI release（Dockerfile.dist FROM vendor_kit:vN）", 20, 45, 280, 40))

# GHCR（外部）
p1.append(v("ghcr", "1", SW(YELLOW), "GHCR", 420, 80, 300, 860))
p1.append(v("g_t", "ghcr", TEXT(), "舊版本不刪、tag 不覆蓋（CI 規則）", 10, 40, 280, 30))
p1.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN\n（引擎 image）", 20, 258, 220, 60))
p1.append(v("g_base", "ghcr", PURPLE_LEAF, "base-dist:vX\n引擎 + dist + 模板 + manifest\nlabel：base commit SHA、版本", 20, 636, 220, 80))
p1.append(v("g_other", "ghcr", PURPLE_LEAF, "agent_harness-dist:vY …", 20, 815, 220, 40))

# downstream（新建模組）
DX, DY = 800, 80
p1.append(v("ds", "1", SW(RED), "downstream repo", DX, DY, 800, 460))
p1.append(v("sa", "ds", SW(RED), "launcher（進 git）", 20, 70, 250, 250))
p1.append(v("c_ref", "sa", LEAF(), ".base-ref\n（image tag）", 15, 60, 105, 50))
p1.append(v("c_just", "sa", LEAF(), "justfile\n（mod base）", 130, 60, 105, 50))
p1.append(v("sa_t", "sa", TEXT(), "極薄、帶契約版本號；.base-ref 由使用者或 Renovate 修改", 10, 125, 115, 100))
p1.append(v("sb", "ds", SW(RED), "使用者檔案（進 git）", 290, 70, 230, 250))
p1.append(v("c_dockerfile", "sb", LEAF(), "Dockerfile", 15, 50, 95, 40))
p1.append(v("c_entry", "sb", LEAF(), "entrypoint", 120, 50, 95, 40))
p1.append(v("c_main", "sb", LEAF(), "main.yaml", 15, 100, 95, 40))
p1.append(v("c_conf", "sb", LEAF(), ".setup.conf", 120, 100, 95, 40))
p1.append(v("c_hooks", "sb", LEAF(), "hooks（opt-in）", 15, 150, 200, 40))
p1.append(v("sb_t", "sb", TEXT(), "seed-once：init 建立一次，之後屬於使用者", 10, 195, 210, 50))
p1.append(v("sc", "ds", SW(RED), ".base/ ＋ 產生物（不進 git）", 540, 70, 240, 250))
p1.append(v("c_wrapper", "sc", LEAF(GREY), ".base/wrapper", 15, 50, 100, 40))
p1.append(v("c_lib", "sc", LEAF(GREY), ".base/lib", 125, 50, 100, 40))
p1.append(v("c_runtime", "sc", LEAF(GREY), ".base/runtime", 15, 100, 100, 40))
p1.append(v("c_stamp", "sc", LEAF(), "印記檔", 125, 100, 100, 40))
p1.append(v("c_compose", "sc", LEAF(), "compose.yaml", 15, 150, 100, 40))
p1.append(v("c_env", "sc", LEAF(), ".env.generated", 125, 150, 100, 40))
p1.append(v("sc_t", "sc", TEXT(), "dist 副本 + 產生物；不可手改", 10, 195, 220, 50))
p1.append(v("ds_engine", "ds", PURPLE_LEAF, "base-dist:vX container\n--rm、host UID/GID、只 mount repo", 20, 370, 250, 70))

# Host（外部）
p1.append(v("host", "1", SW(YELLOW), "Host", 1640, 80, 200, 460))
p1.append(v("h_t", "host", TEXT(), "只安裝這三個", 10, 40, 180, 30))
p1.append(v("h_docker", "host", LEAF(GREY), "Docker daemon", 20, 80, 160, 40))
p1.append(v("h_just", "host", LEAF(GREY), "just", 20, 140, 160, 40))
p1.append(v("h_git", "host", LEAF(GREY), "git", 20, 200, 160, 40))

# edges（資料）
p1.append(e("e_vk_push", "vk_ci", "g_vk", "vendor_kit image", (1, 0.5), (0, 0.5)))
p1.append(e("e_base_push", "base_ci", "g_base", "base-dist image", (1, 0.5), (0, 0.5)))
p1.append(e("e_other_push", "other_ci", "g_other", "agent_harness-dist image", (1, 0.5), (0, 0.5)))
p1.append(e("e_from_base", "g_vk", "g_base", "FROM（引擎層）", (0.5, 1), (0.5, 0), dashed=True))
p1.append(e("e_from_other", "g_vk", "g_other", "FROM", (1, 0.5), (1, 0.5), dashed=True))
p1.append(e("e_pull", "g_base", "ds_engine", "image layers（pull）", (1, 0.5), (0, 0.5)))
p1.append(e("e_ref", "c_ref", "c_just", "image tag", (1, 0.5), (0, 0.5)))
p1.append(e("e_run", "c_just", "ds_engine", "image tag、UID/GID、repo 路徑（docker run）", (0.5, 1), (0.73, 0)))
p1.append(e("e_verb", "c_just", "sc", "verb ＋ 參數", (0.5, 0), (0.5, 0)))
p1.append(e("e_conf", "c_conf", "sc", "設定值（stage、mount、port …）", (1, 0.5), (0, 0.48)))
p1.append(e("e_land", "ds_engine", "sc", "tool-owned 檔案 ＋ 印記檔（寫）／ hash（讀回驗證）", (1, 0.7), (0.75, 1), both=True))
p1.append(e("e_seed", "ds_engine", "sb", "模板渲染結果（僅首次）", (1, 0.3), (0.5, 1), dashed=True))
p1.append(e("e_compose", "sc", "h_docker", "compose 命令 ＋ compose.yaml", (1, 0.5), (0, 0.5)))
p1 += legend_arch("p1", 40, 1000)

# ================= Page 2: 流程：launcher =================
p2 = [v("title", "1", TITLE, "流程：launcher（justfile）— 每次執行 just <verb>", 40, 20, 900, 30)]
p2.append(v("c4", "1", ELLIPSE(GREEN), "just <verb>", 300, 60, 160, 50))
p2.append(v("c5", "1", LEAF(), "讀 .base-ref", 280, 140, 200, 40))
p2.append(v("c6", "1", RHOMBUS, "image 在本地？", 290, 210, 180, 90))
p2.append(v("c7", "1", LEAF(), "docker pull", 40, 230, 160, 50))
p2.append(v("c8", "1", RHOMBUS, ".base/ 印記\n與 .base-ref 一致？", 270, 340, 220, 100))
p2.append(v("c9", "1", PURPLE_LEAF, "docker run --rm 引擎 land\n（host UID/GID；含首次 init）", 560, 360, 240, 60))
p2.append(v("c9n", "1", NOTE, "引擎內部流程見第 4 頁", 560, 440, 240, 40))
p2.append(v("c13", "1", RHOMBUS, "引擎 verify：\n.base/ hash 與印記相符？", 270, 480, 220, 100))
p2.append(v("c14", "1", ELLIPSE(RED), "報錯：.base/ 被手改\n請重新落地", 20, 500, 180, 60))
p2.append(v("c15", "1", LEAF(), "執行 .base/ 內 wrapper", 280, 640, 200, 50))
p2.append(v("c16", "1", ELLIPSE(GREEN), "docker compose …", 300, 730, 160, 50))
p2.append(e("c17", "c4", "c5"))
p2.append(e("c18", "c5", "c6"))
p2.append(e("c19", "c6", "c7", "否", (0, 0.5), (1, 0.5)))
p2.append(e("c20", "c6", "c8", "是", (0.5, 1), (0.5, 0)))
p2.append(e("c21", "c7", "c8", "", (0.5, 1), (0, 0.5)))
p2.append(e("c22", "c8", "c9", "否（需落地）", (1, 0.5), (0, 0.5)))
p2.append(e("c23", "c8", "c13", "是", (0.5, 1), (0.5, 0)))
p2.append(e("c24", "c9", "c15", "落地完成", (0.5, 1), (1, 0.5)))
p2.append(e("c29", "c13", "c14", "否", (0, 0.5), (1, 0.5)))
p2.append(e("c30", "c13", "c15", "是", (0.5, 1), (0.5, 0)))
p2.append(e("c31", "c15", "c16"))
p2 += legend_flow("p2", 40, 1000)

# ================= Page 3: 流程：版本生命週期 =================
p3 = [v("title", "1", TITLE, "流程：版本生命週期（launcher ＋ 引擎）", 40, 20, 700, 30)]
p3.append(v("up", "1", SW(NEUTRAL), "升級", 20, 60, 420, 560))
p3.append(v("c5", "up", LEAF(), "修改 .base-ref 到新版本（手動或 Renovate PR）", 20, 50, 380, 40))
p3.append(v("c6", "up", LEAF(), "just → 用「新版 image」落地", 20, 110, 380, 40))
p3.append(v("c7", "up", LEAF(), "tool-owned 檔案：直接覆蓋", 20, 170, 380, 50))
p3.append(v("c8", "up", RHOMBUS, "seed-once 檔案（Dockerfile 等）\n需要配合變更？", 70, 240, 280, 100))
p3.append(v("c9", "up", LEAF(), "引擎 diff 輸出 patch，由使用者決定是否套用\n（工具不自動 commit 使用者檔案）", 20, 370, 380, 60))
p3.append(v("c10", "up", LEAF(), "commit .base-ref + 使用者自己的修改", 20, 460, 380, 40))
p3.append(e("c11", "c5", "c6"))
p3.append(e("c12", "c6", "c7"))
p3.append(e("c13", "c7", "c8"))
p3.append(e("c14", "c8", "c9", "是", (0.5, 1), (0.5, 0)))
p3.append(e("c14b", "c8", "c10", "否", (1, 0.5), (1, 0.5)))
p3.append(e("c15", "c9", "c10"))
p3.append(v("c16", "1", NOTE, "重點：升級邏輯在「新版 image」裡，\n不在 repo 的舊腳本裡，\n不會發生「舊工具升級自己」的問題。", 460, 100, 300, 90))
p3.append(v("rb", "1", SW(NEUTRAL), "回退", 460, 230, 300, 190))
p3.append(v("c18", "rb", LEAF(), "git revert .base-ref 的變更", 20, 50, 260, 40))
p3.append(v("c19", "rb", LEAF(), "just → 用舊版 image 重新落地\n（.base/ 不進 git，無需額外紀錄）", 20, 110, 260, 50))
p3.append(e("c20", "c18", "c19"))
p3.append(v("bug", "1", SW(NEUTRAL), "追 bug（可追溯鏈）", 800, 60, 420, 420))
p3.append(v("c22", "bug", LEAF(), "downstream 的某個 commit", 20, 50, 380, 50))
p3.append(v("c23", "bug", LEAF(), ".base-ref\n版本 tag（tag / digest 待決議）", 20, 130, 380, 50))
p3.append(v("c24", "bug", PURPLE_LEAF, "image label\nbase commit SHA、版本、source repo", 20, 210, 380, 50))
p3.append(v("c25", "bug", LEAF(), "base repo 對應 commit 的原始碼", 20, 290, 380, 50))
p3.append(v("c29", "bug", NOTE, "git bisect 在 .base-ref 上即可找出哪次升級引入問題", 20, 355, 380, 50))
p3.append(e("c26", "c22", "c23"))
p3.append(e("c27", "c23", "c24"))
p3.append(e("c28", "c24", "c25"))
p3.append(v("dev", "1", SW(NEUTRAL), "本地開發模式（開發 base 時）", 800, 510, 420, 150))
p3.append(v("c31", "dev", LEAF(), "來源暫時改指向本機 base checkout\n不需每次發佈 image 即可在 downstream 測試\n（需在設計初期就預留）", 20, 50, 380, 80))
p3 += legend_flow("p3", 40, 1000)

# ================= Page 4: 流程：引擎 =================
p4 = [v("title", "1", TITLE, "流程：引擎（vendor_kit）— 在 base-dist container 內執行", 40, 20, 900, 30)]
# land
p4.append(v("land", "1", SW(NEUTRAL), "land（含首次 init）", 20, 60, 560, 760))
p4.append(v("l0", "land", ELLIPSE(GREEN), "land", 200, 50, 160, 50))
p4.append(v("l1", "land", LEAF(), "讀 image 內的 manifest", 180, 130, 200, 40))
p4.append(v("l2", "land", LEAF(), "逐一處理 manifest 條目", 180, 200, 200, 40))
p4.append(v("l3", "land", RHOMBUS, "檔案類別？", 190, 270, 180, 80))
p4.append(v("l4", "land", LEAF(), "tool-owned：\n寫入 .base/，記錄 hash", 20, 380, 160, 50))
p4.append(v("l5", "land", RHOMBUS, "seed-once：\n目標已存在？", 190, 370, 180, 80))
p4.append(v("l6", "land", LEAF(), "opt-in：跳過", 400, 380, 140, 50))
p4.append(v("l7", "land", LEAF(), "渲染模板寫入（init）", 100, 480, 170, 40))
p4.append(v("l8", "land", LEAF(), "跳過，保留使用者版本", 290, 480, 170, 40))
p4.append(v("l9", "land", LEAF(), "寫印記檔（版本 + 各檔 hash）", 180, 570, 200, 50))
p4.append(v("l10", "land", ELLIPSE(GREEN), "exit 0", 200, 660, 160, 50))
p4.append(e("le0", "l0", "l1"))
p4.append(e("le1", "l1", "l2"))
p4.append(e("le2", "l2", "l3"))
p4.append(e("le3", "l3", "l4", "tool-owned", (0, 0.5), (0.5, 0)))
p4.append(e("le4", "l3", "l5", "seed-once", (0.5, 1), (0.5, 0)))
p4.append(e("le5", "l3", "l6", "opt-in", (1, 0.5), (0.5, 0)))
p4.append(e("le6", "l5", "l7", "否", (0, 0.5), (0.5, 0)))
p4.append(e("le7", "l5", "l8", "是", (1, 0.5), (0.5, 0)))
p4.append(e("le8", "l4", "l9", "", (0.5, 1), (0, 0.5)))
p4.append(e("le9", "l7", "l9", "", (0.5, 1), (0.25, 0)))
p4.append(e("le10", "l8", "l9", "", (0.5, 1), (0.75, 0)))
p4.append(e("le11", "l6", "l9", "", (0.5, 1), (1, 0.5)))
p4.append(e("le12", "l9", "l10"))
# verify
p4.append(v("verify", "1", SW(NEUTRAL), "verify", 620, 60, 440, 480))
p4.append(v("v0", "verify", ELLIPSE(GREEN), "verify", 140, 50, 160, 50))
p4.append(v("v1", "verify", LEAF(), "讀印記檔", 120, 130, 200, 40))
p4.append(v("v2", "verify", LEAF(), "逐檔計算 .base/ hash", 120, 200, 200, 40))
p4.append(v("v3", "verify", RHOMBUS, "全部相符？", 130, 270, 180, 80))
p4.append(v("v4", "verify", ELLIPSE(GREEN), "exit 0", 20, 390, 160, 50))
p4.append(v("v5", "verify", ELLIPSE(RED), "exit 非 0\n列出被改的檔案", 240, 390, 180, 50))
p4.append(e("ve0", "v0", "v1"))
p4.append(e("ve1", "v1", "v2"))
p4.append(e("ve2", "v2", "v3"))
p4.append(e("ve3", "v3", "v4", "是", (0, 0.5), (0.5, 0)))
p4.append(e("ve4", "v3", "v5", "否", (1, 0.5), (0.5, 0)))
# diff
p4.append(v("diff", "1", SW(NEUTRAL), "diff（升級時）", 1100, 60, 440, 480))
p4.append(v("d0", "diff", ELLIPSE(GREEN), "diff", 140, 50, 160, 50))
p4.append(v("d1", "diff", LEAF(), "以目前使用者檔案為基準\n渲染新版 seed-once 模板", 100, 130, 240, 50))
p4.append(v("d2", "diff", LEAF(), "比對使用者檔案 vs 新模板", 100, 210, 240, 40))
p4.append(v("d3", "diff", RHOMBUS, "有差異？", 130, 280, 180, 80))
p4.append(v("d4", "diff", ELLIPSE(GREEN), "exit 0（無需變更）", 20, 400, 180, 50))
p4.append(v("d5", "diff", LEAF(), "輸出 patch 到 stdout\n（不改使用者檔案）", 240, 395, 180, 60))
p4.append(e("de0", "d0", "d1"))
p4.append(e("de1", "d1", "d2"))
p4.append(e("de2", "d2", "d3"))
p4.append(e("de3", "d3", "d4", "否", (0, 0.5), (0.5, 0)))
p4.append(e("de4", "d3", "d5", "是", (1, 0.5), (0.5, 0)))
p4.append(v("p4n", "1", NOTE, "所有 verb 共同前提：container 以 host UID/GID 執行，只 mount repo；\n引擎自身版本由 image tag 決定，不讀 repo 內任何腳本。", 620, 570, 920, 60))
p4 += legend_flow("p4", 40, 1000)

doc = ('<mxfile host="app.diagrams.net">'
       + page("p1", "1. 架構圖", p1, w=1900)
       + page("p2", "2. 流程：launcher", p2)
       + page("p3", "3. 流程：版本生命週期", p3)
       + page("p4", "4. 流程：引擎", p4)
       + "</mxfile>")
open("/home/cyc/Desktop/vendor-kit_ws/src/dist_distribution.drawio", "w").write(doc)
print(len(doc))
