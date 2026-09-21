import html

RED, GREEN, YELLOW, PURPLE, GREY = "#f8cecc", "#d5e8d4", "#FFF4C3", "#e1d5e7", "#CCCCCC"

def SW(fill, stroke="#000000"):
    return (f"swimlane;html=1;rounded=1;startSize=38;fontStyle=1;fontSize=18;container=1;"
            f"collapsible=1;recursiveResize=0;fillColor={fill};swimlaneFillColor=#ffffff;"
            f"strokeColor={stroke};strokeWidth=2;")
def LEAF(fill="#ffffff", stroke="light-dark(#000000,#9577A3)", sw=1):
    return f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize=14;strokeWidth={sw};"
PURPLE_LEAF = LEAF(PURPLE, "#9673a6", 2)
def TEXT(size=12):
    return f"text;html=1;whiteSpace=wrap;align=center;verticalAlign=middle;fontSize={size};strokeColor=none;fillColor=none;"
TITLE = "text;html=1;fontSize=18;fontStyle=1;align=left;verticalAlign=middle;"
def RHOMBUS():
    return f"rhombus;whiteSpace=wrap;html=1;fillColor={YELLOW};strokeColor=#000000;strokeWidth=2;fontSize=14;"
def ELLIPSE(fill):
    return f"ellipse;whiteSpace=wrap;html=1;fillColor={fill};strokeColor=#000000;strokeWidth=2;fontSize=14;"
NOTE = "shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#ffffff;strokeColor=#999999;align=left;spacingLeft=6;fontSize=12;"
LEGEND = lambda fill: (f"swimlane;html=1;rounded=1;startSize=34;fontStyle=1;fontSize=14;container=0;collapsible=0;"
                       f"fillColor={fill};swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=2;")
EDGE = ("edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=default;"
        "strokeWidth=2;align=center;verticalAlign=bottom;spacingBottom=6;fontFamily=Helvetica;fontSize=10;"
        "fontColor=default;labelBorderColor=none;labelBackgroundColor=none;endArrow=block;endFill=1;")

def esc(s): return html.escape(s, quote=True).replace("\n", "&lt;br&gt;")

def v(id, parent, style, value, x, y, w, h):
    return (f'<mxCell id="{id}" value="{esc(value)}" style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

def e(id, src, tgt, label="", exit=None, entry=None, dashed=False, parent="1"):
    st = EDGE
    if exit:  st += f"exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;"
    if entry: st += f"entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
    if dashed: st += "dashed=1;"
    return (f'<mxCell id="{id}" value="{esc(label)}" style="{st}" edge="1" parent="{parent}" source="{src}" target="{tgt}">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>')

def page(id, name, cells, w=1600, h=1000):
    body = "".join(cells)
    return (f'<diagram id="{id}" name="{esc(name)}"><mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" '
            f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{w}" pageHeight="{h}" math="0" shadow="0">'
            f'<root><mxCell id="0" style="strokeWidth=2;"/><mxCell id="1" parent="0" style="strokeWidth=2;"/>{body}</root></mxGraphModel></diagram>')

def legend(prefix, x, y, extra_text):
    c = []
    items = [("未完成（新建）", RED), ("已完成（現有不變）", GREEN), ("特殊／分類", YELLOW)]
    for i, (t, f) in enumerate(items):
        c.append(v(f"{prefix}_lg{i}", "1", LEGEND(f), t, x + i * 185, y, 165, 60))
    c.append(v(f"{prefix}_lg3", "1", PURPLE_LEAF, "image / container", x + 3 * 185, y + 10, 165, 40))
    c.append(v(f"{prefix}_lg4", "1", LEAF(), "新增元件", x + 4 * 185, y + 10, 88, 40))
    c.append(v(f"{prefix}_lg5", "1", LEAF(GREY), "現有元件", x + 4 * 185 + 100, y + 10, 88, 40))
    c.append(v(f"{prefix}_lg6", "1", TEXT(12) + "align=left;", extra_text, x + 5 * 185 + 20, y, 300, 60))
    return c

# ---------------- Page 1: 架構圖 ----------------
p1 = []
p1.append(v("title", "1", TITLE, "dist 分發架構：以 GHCR image 取代 git subtree + symlink", 40, 20, 900, 30))

# vendor_kit repo
p1.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 80, 300, 250))
p1.append(v("vk_t", "vk", TEXT(), "通用落地引擎 + manifest 規格，打包成 vendor_kit:vN image", 10, 40, 280, 36))
p1.append(v("vk_engine", "vk", LEAF(), "落地引擎（land / init / verify）", 20, 85, 260, 40))
p1.append(v("vk_manifest", "vk", LEAF(), "manifest 規格\n（tool-owned / seed-once / opt-in）", 20, 135, 260, 50))
p1.append(v("vk_ci", "vk", LEAF(), "CI release（build + push）", 20, 195, 260, 40))

# base repo
p1.append(v("base", "1", SW(GREEN), "base repo（本體不變）", 40, 370, 300, 300))
p1.append(v("base_t", "base", TEXT(), "release 時 FROM vendor_kit:vN，加入 dist、init 模板、manifest", 10, 40, 280, 36))
p1.append(v("base_dist", "base", LEAF(GREY), "dist/（wrapper、lib）", 20, 85, 125, 40))
p1.append(v("base_tpl", "base", LEAF(GREY), "init 模板（Dockerfile …）", 155, 85, 125, 40))
p1.append(v("base_manifest", "base", LEAF(), "manifest（宣告每個檔案類別）", 20, 135, 260, 40))
p1.append(v("base_ci", "base", LEAF(), "CI release（tag 觸發）\n只打包 dist，不含 test / ADR / 翻譯", 20, 195, 260, 50))

# other tools
p1.append(v("other", "1", SW(RED), "其他工具（agent_harness …）", 40, 710, 300, 110))
p1.append(v("other_ci", "other", LEAF(), "CI release（同樣 FROM vendor_kit:vN）", 20, 50, 260, 40))

# GHCR
p1.append(v("ghcr", "1", SW(YELLOW), "GHCR", 420, 80, 300, 760))
p1.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN\n（引擎 image）", 20, 185, 220, 60))
p1.append(v("g_base", "ghcr", PURPLE_LEAF, "base-dist:vX\nFROM vendor_kit:vN\n+ dist + 模板 + manifest\nlabel：base commit SHA", 20, 475, 220, 70))
p1.append(v("g_other", "ghcr", PURPLE_LEAF, "agent_harness-dist:vY …\n（共用同一引擎）", 20, 670, 220, 60))
p1.append(v("g_t", "ghcr", TEXT(), "舊版本不刪、tag 不覆蓋（CI 規則）", 10, 740, 280, 30))

# downstream repo
p1.append(v("ds", "1", SW(RED), "downstream repo（Host 只有 Docker + Git + just）", 800, 80, 740, 560))
p1.append(v("col1", "ds", SW(YELLOW), "進 git", 20, 50, 220, 290))
p1.append(v("c_ref", "col1", LEAF(), ".base-ref（base 版本）", 20, 50, 180, 40))
p1.append(v("c_just", "col1", LEAF(), "justfile（launcher）\n極薄、很少變動", 20, 110, 180, 50))
p1.append(v("c1_t", "col1", TEXT(), "版本由使用者或 Renovate 修改；launcher 帶契約版本號", 10, 180, 200, 60))
p1.append(v("col2", "ds", SW(YELLOW), "進 git・使用者檔案", 260, 50, 220, 290))
p1.append(v("c2_t", "col2", TEXT(), "seed-once：init 建立一次，之後屬於使用者", 10, 40, 200, 40))
p1.append(v("c_dockerfile", "col2", LEAF(), "Dockerfile", 16, 90, 88, 40))
p1.append(v("c_entry", "col2", LEAF(), "entrypoint", 116, 90, 88, 40))
p1.append(v("c_conf", "col2", LEAF(), ".setup.conf", 16, 140, 88, 40))
p1.append(v("c_main", "col2", LEAF(), "main.yaml", 116, 140, 88, 40))
p1.append(v("c_hooks", "col2", LEAF(), "hooks（opt-in，需要才建立）", 16, 190, 188, 40))
p1.append(v("col3", "ds", SW(YELLOW), "不進 git", 500, 50, 220, 290))
p1.append(v("c_basedir", "col3", LEAF(), ".base/（dist 落地處）", 20, 50, 180, 40))
p1.append(v("c_stamp", "col3", LEAF(), "印記檔（版本 + 各檔 hash）", 20, 100, 180, 40))
p1.append(v("c_compose", "col3", LEAF(), "compose.yaml / .env.generated", 20, 150, 180, 40))
p1.append(v("c3_t", "col3", TEXT(), "由工具產生；不可手改，被改會報錯", 10, 200, 200, 50))
p1.append(v("ds_engine", "ds", PURPLE_LEAF, "docker run --rm base-dist:vX\nhost UID/GID、只 mount repo\n跑完 container 即刪除，image 保留", 20, 475, 440, 70))
p1.append(v("ds_compose", "ds", LEAF(), "docker compose\nbuild / up / exec / down\n（.base/ 內 wrapper）", 500, 475, 220, 70))

# edges
p1.append(e("e_vk_push", "vk_ci", "g_vk", "push", (1, 0.5), (0, 0.5)))
p1.append(e("e_base_push", "base_ci", "g_base", "push", (1, 0.5), (0, 0.5)))
p1.append(e("e_other_push", "other_ci", "g_other", "push", (1, 0.5), (0, 0.5)))
p1.append(e("e_from_base", "g_vk", "g_base", "FROM", (0.5, 1), (0.5, 0), dashed=True))
p1.append(e("e_from_other", "g_vk", "g_other", "FROM", (1, 0.5), (1, 0.5), dashed=True))
p1.append(e("e_pull", "g_base", "ds_engine", "pull", (1, 0.5), (0, 0.5)))
p1.append(e("e_just", "c_just", "ds_engine", "讀 .base-ref → pull → run", (0.5, 1), (0.25, 0)))
p1.append(e("e_seed", "ds_engine", "col2", "僅首次建立（seed-once）", (0.795, 0), (0.5, 1), dashed=True))
p1.append(e("e_land", "ds_engine", "col3", "寫入 tool-owned + 印記檔", (1, 0.5), (0, 0.9)))
p1.append(e("e_wrap", "col3", "ds_compose", "just 執行 .base/ 內 wrapper", (0.5, 1), (0.5, 0)))
p1 += legend("p1", 40, 880, "虛線 = 繼承或僅特定情況發生")

# ---------------- Page 2: 執行流程 ----------------
p2 = []
p2.append(v("title", "1", TITLE, "每次執行 just <verb> 時的流程", 40, 20, 700, 30))
p2.append(v("c4", "1", ELLIPSE(GREEN), "just <verb>", 300, 60, 160, 50))
p2.append(v("c5", "1", LEAF(), "讀 .base-ref", 280, 140, 200, 40))
p2.append(v("c6", "1", RHOMBUS(), "image 在本地？", 290, 210, 180, 90))
p2.append(v("c7", "1", LEAF(), "docker pull", 40, 230, 160, 50))
p2.append(v("c8", "1", RHOMBUS(), ".base/ 印記\n與 .base-ref 一致？", 270, 340, 220, 100))
p2.append(v("c9", "1", PURPLE_LEAF, "docker run --rm\n（host UID/GID）", 560, 360, 220, 60))
p2.append(v("c10", "1", RHOMBUS(), "首次？\n（無使用者檔案）", 580, 460, 180, 90))
p2.append(v("c11", "1", LEAF(), "init：建立 Dockerfile、\nentrypoint、setup.conf …", 840, 475, 200, 60))
p2.append(v("c12", "1", LEAF(), "寫入 .base/ + 印記檔\ncontainer 結束刪除", 560, 600, 220, 60))
p2.append(v("c13", "1", RHOMBUS(), ".base/ 檔案 hash\n與印記相符？", 270, 480, 220, 100))
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
p2.append(e("c24", "c9", "c10"))
p2.append(e("c25", "c10", "c11", "是", (1, 0.5), (0, 0.5)))
p2.append(e("c26", "c10", "c12", "否", (0.5, 1), (0.5, 0)))
p2.append(e("c27", "c11", "c12", "", (0.5, 1), (1, 0.5)))
p2.append(e("c28", "c12", "c13", "", (0, 0.5), (1, 0.5)))
p2.append(e("c29", "c13", "c14", "否", (0, 0.5), (1, 0.5)))
p2.append(e("c30", "c13", "c15", "是", (0.5, 1), (0.5, 0)))
p2.append(e("c31", "c15", "c16"))

# ---------------- Page 3: 升級・回退・追 bug ----------------
p3 = []
p3.append(v("title", "1", TITLE, "版本生命週期", 40, 20, 700, 30))
p3.append(v("up", "1", SW(RED), "升級", 20, 60, 420, 560))
p3.append(v("c5", "up", LEAF(), "修改 .base-ref 到新版本（手動或 Renovate PR）", 20, 50, 380, 40))
p3.append(v("c6", "up", LEAF(), "just → 用「新版 image」落地", 20, 110, 380, 40))
p3.append(v("c7", "up", LEAF(), "tool-owned 檔案：直接覆蓋", 20, 170, 380, 50))
p3.append(v("c8", "up", RHOMBUS(), "seed-once 檔案（Dockerfile 等）\n需要配合變更？", 70, 240, 280, 100))
p3.append(v("c9", "up", LEAF(), "輸出 patch / 提示，由使用者決定是否套用\n（工具不自動 commit 使用者檔案）", 20, 370, 380, 60))
p3.append(v("c10", "up", LEAF(), "commit .base-ref + 使用者自己的修改", 20, 460, 380, 40))
p3.append(e("c11", "c5", "c6"))
p3.append(e("c12", "c6", "c7"))
p3.append(e("c13", "c7", "c8"))
p3.append(e("c14", "c8", "c9", "是", (0.5, 1), (0.5, 0)))
p3.append(e("c14b", "c8", "c10", "否", (1, 0.5), (1, 0.5)))
p3.append(e("c15", "c9", "c10"))
p3.append(v("c16", "1", NOTE, "重點：升級邏輯在「新版 image」裡，\n不在 repo 的舊腳本裡，\n不會發生「舊工具升級自己」的問題。", 460, 100, 300, 90))
p3.append(v("rb", "1", SW(RED), "回退", 460, 230, 300, 190))
p3.append(v("c18", "rb", LEAF(), "git revert .base-ref 的變更", 20, 50, 260, 40))
p3.append(v("c19", "rb", LEAF(), "just → 用舊版 image 重新落地\n（.base/ 不進 git，無需額外紀錄）", 20, 110, 260, 50))
p3.append(e("c20", "c18", "c19"))
p3.append(v("bug", "1", SW(YELLOW), "追 bug（可追溯鏈）", 800, 60, 420, 420))
p3.append(v("c22", "bug", LEAF(), "downstream 的某個 commit", 20, 50, 380, 50))
p3.append(v("c23", "bug", LEAF(), ".base-ref\n版本 tag（tag / digest 待決議）", 20, 130, 380, 50))
p3.append(v("c24", "bug", PURPLE_LEAF, "image label\nbase commit SHA、版本、source repo", 20, 210, 380, 50))
p3.append(v("c25", "bug", LEAF(), "base repo 對應 commit 的原始碼", 20, 290, 380, 50))
p3.append(v("c29", "bug", NOTE, "git bisect 在 .base-ref 上即可找出哪次升級引入問題", 20, 355, 380, 50))
p3.append(e("c26", "c22", "c23"))
p3.append(e("c27", "c23", "c24"))
p3.append(e("c28", "c24", "c25"))
p3.append(v("dev", "1", SW(YELLOW), "本地開發模式（開發 base 時）", 800, 510, 420, 150))
p3.append(v("c31", "dev", LEAF(), "來源暫時改指向本機 base checkout\n不需每次發佈 image 即可在 downstream 測試\n（需在設計初期就預留）", 20, 50, 380, 80))

doc = ('<mxfile host="app.diagrams.net">'
       + page("p1", "1. 架構圖", p1)
       + page("p2", "2. 執行流程（just <verb>）", p2)
       + page("p3", "3. 升級・回退・追 bug", p3)
       + "</mxfile>")
open("/home/cyc/Desktop/vendor-kit_ws/src/dist_distribution.drawio", "w").write(doc)
print(len(doc))
