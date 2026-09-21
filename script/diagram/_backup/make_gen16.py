s = open("gen15.py", encoding="utf-8").read()

# ---- 圖例系統：可控項目 ----
old = s[s.index("def legend_flow("):s.index("# ================= Page 1: vendor_kit 架構圖")]
new = '''def legend_flow(prefix, x, y, purple=True, files=False, note=False, dashed=False, startend=True, err=True):
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
    txt = "實線 = 執行順序" + ("\\n虛線 = 之後才會發生" if dashed else "")
    c.append(v(f"{prefix}_lgt", "1", TEXT(12) + "align=left;", txt, cx, y, 200, 60))
    return c

'''
s = s.replace(old, new)
# 紫色圖例改成小字版；黃色語意；新增淺灰、便條
s = s.replace(''' "purple": (PURPLE_SW,          "紫：container（執行形態）", 220, 60, 0),''',
 ''' "purple": (f"swimlane;html=1;rounded=1;startSize=34;fontStyle=1;fontSize=14;container=0;collapsible=0;fillColor={PURPLE};swimlaneFillColor=#ffffff;strokeColor=#9673a6;strokeWidth=2;", "紫：container（執行形態）", 220, 60, 0),
 "neutral":(LEGEND_BOX(NEUTRAL), "淺灰：分組（無狀態意義）", 200, 60, 0),
 "note":   (NOTE,               "便條：補充說明", 130, 40, 10),''')
s = s.replace(''' "yellow": (LEGEND_BOX(YELLOW), "黃：外部系統", 160, 60, 0),''', ''' "yellow": (LEGEND_BOX(YELLOW), "黃：外部（使用者、外部系統）", 220, 60, 0),''')

R = {
 # ---------- 頁 1 ----------
 'p1.append(v("img", "1", SW(YELLOW), "image 內容", 200, 300, 180, 280))': 'p1.append(v("img", "1", PURPLE_SW, "image 內容", 200, 300, 180, 280))',
 'p1.append(v("proj", "1", SW(YELLOW), "專案目錄", 1140, VY, 200, 860))': 'p1.append(v("proj", "1", SW(GREEN), "專案 repo 的目錄", 1140, VY, 200, 860))',
 'p1.append(v("u_out", "user", LEAF(), "畫面", 26, 760, 88, 40))': 'p1.append(v("u_out", "user", LEAF(), "畫面", 26, 810, 88, 40))',
 'p1.append(e("a2", "m_cli", "m_list", "命令參數", (0.5, 1), (0.5, 0), vert=True))': 'p1.append(e("a2", "m_cli", "m_list", "命令、參數（解析後）", (0.5, 1), (0.5, 0), vert=True))',
 'p1.append(e("a9", "m_write", "m_stamp", "內容、既有印記\\n⇄ 新指紋", (0.8, 1), (0.64, 0), both=True, vert="left"))': 'p1.append(e("a9", "m_write", "m_stamp", "↓ 檔案內容、舊印記\\n↑ 新指紋、比對結果", (0.8, 1), (0.64, 0), both=True, vert="left"))',
 '<mxCell id="a13" value="使用者檔案" style="\' + EDGE + \'exitX=0.35;exitY=1;exitDx=0;exitDy=0;entryX=0.9;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="m_write" target="m_diff"><mxGeometry x="0.55" relative="1" as="geometry"><Array as="points"><mxPoint x="850" y="780"/>':
 '<mxCell id="a13" value="使用者檔案" style="\' + EDGE + \'exitX=0.15;exitY=1;exitDx=0;exitDy=0;entryX=0.9;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="m_write" target="m_diff"><mxGeometry x="0.55" relative="1" as="geometry"><Array as="points"><mxPoint x="810" y="780"/>',
 'p1 += legend("p1", 40, 1060, ["purple", "red", "yellow", "white"], "實線 = 傳輸內容（線上文字 = 傳什麼）\\n虛線 = 只在特定情況發生")': 'p1 += legend("p1", 40, 1060, ["purple", "red", "green", "yellow", "white"], "實線 = 傳輸內容（線上文字 = 傳什麼）")',
 ' ("指紋", "由檔案內容算出的一串碼（sha256）；內容一改就不同"),\n])': ' ("指紋", "由檔案內容算出的一串碼（sha256）；內容一改就不同"),\n ("模板", "工具 dist/ 裡給初始檔用的樣板（例如 Dockerfile 範本）；渲染 = 帶入變數（專案名等）產生實際檔案"),\n])',
 'page("p1", "1. vendor_kit 架構圖", p1, w=1700, h=1400)': 'page("p1", "1. vendor_kit 架構圖", p1, w=1700, h=1430)',
 # ---------- 頁 2 ----------
 'p1b.append(v("pa", "proj", SW(RED), "啟動器（進 git）", 20, 80, 260, 135))': 'p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器（進 git）", 20, 80, 260, 145))',
 'p1b.append(v("p_ver", "pa", LEAF(), ".version", 12, 50, 100, 40))': 'p1b.append(v("p_ver", "pa", LEAF(), ".version", 12, 70, 100, 40))',
 'p1b.append(v("pa_t", "pa", TEXT(11) + "align=left;", ".version 一行 = 一個工具 = 一個 .<name>/", 12, 96, 240, 24))': 'p1b.append(v("pa_t", "pa", TEXT(11) + "align=left;", ".version 一行 = 一個工具 = 一個 .<name>/", 12, 116, 240, 24))',
 'p1b.append(v("p_just", "pa", LEAF(), "justfile", 158, 50, 90, 40))': 'p1b.append(v("p_just", "pa", LEAF(), "justfile", 158, 70, 90, 40))',
 'p1b.append(v("p_eng", "proj", PURPLE_LEAF, "安裝容器（<name>-dist:vX）", 20, 260, 260, 60))': 'p1b.append(v("p_eng", "proj", PURPLE_LEAF, "安裝容器（<name>-dist:vX）", 340, 140, 260, 60))',
 'p1b.append(v("p_eng_t", "proj", TEXT(11) + "align=left;", "以使用者身分執行，跑完即刪", 20, 322, 150, 20))': 'p1b.append(v("p_eng_t", "proj", TEXT(11) + "align=left;", "以使用者身分執行，跑完即刪", 340, 202, 200, 20))',
 'p1b.append(v("pb", "proj", SW(RED), "使用者檔案（進 git）", 300, 360, 220, 125))': 'p1b.append(v("pb", "proj", SW(NEUTRAL), "使用者檔案（進 git）", 300, 360, 220, 125))',
 'p1b.append(v("pc", "proj", SW(RED), ".<name>/（不進 git）", 540, 340, 220, 125))': 'p1b.append(v("pc", "proj", SW(NEUTRAL), ".<name>/（不進 git）", 540, 340, 220, 125))',
 'p1b.append(v("pc2", "proj", SW(RED), ".<name2>/（另一個工具）", 540, 465, 220, 50))': 'p1b.append(v("pc2", "proj", SW(NEUTRAL), ".<name2>/（另一個工具）", 540, 480, 220, 50))',
 'p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 470, 200, 40))': 'p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 485, 200, 40))',
 'p1b.append(v("tool2", "1", SW(GREEN), "另一個工具 repo（<name2>，同型）", 40, 540, 320, 60))': 'p1b.append(v("tool2", "1", SW(GREEN), "另一個工具 repo（<name2>，同型）", 40, 555, 320, 60))',
 'p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 150, 200, 40))': 'p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 150, 200, 40))',
 'p1b.append(e("f6", "g_tool", "p_eng", "image", (1, 0.5), (0, 0.5)))': 'p1b.append(e("f6", "g_tool", "p_eng", "image", (1, 0.5), (0, 0.5), pos=-0.4))',
 'p1b.append(e("f7", "p_ver", "p_just", "", (1, 0.5), (0, 0.5)))': 'p1b.append(e("f7", "p_ver", "p_just", "讀取", (1, 0.5), (0, 0.5)))',
 'p1b.append(e("f8", "p_just", "p_eng", "工具名、版本、使用者 UID/GID、專案路徑", (0.5, 1), (0.78, 0), vert=True, pos=0.2))': 'p1b.append(e("f8", "p_just", "p_eng", "工具名、版本、使用者身分（讓寫出的檔案歸使用者）、專案路徑", (1, 0.5), (0, 0.5)))',
 'p1b.append(e("f9", "p_eng", "pc", "寫入 dist、印記檔", (1, 0.5), (0.5, 0)))': 'p1b.append(e("f9", "p_eng", "pc", "寫入 dist、印記檔", (1, 0.5), (0.5, 0)))',
 'p1b.append(e("f10", "p_eng", "pb", "初始檔（init 時）", (0.85, 1), (0, 0.5), dashed=True, vert="left", pos=-0.6))': 'p1b.append(e("f10", "p_eng", "pb", "初始檔（init 時）", (0.27, 1), (0.5, 0), dashed=True, vert=True))',
 'p1b += legend("p1b", 40, 700, ["red", "green", "yellow", "pimg", "white", "grey"], "實線 = 傳輸內容\\n虛線 = 基底依賴，或只在特定情況發生")': 'p1b += legend("p1b", 40, 700, ["red", "green", "yellow", "pimg", "neutral", "white", "grey"], "實線 = 傳輸內容\\n虛線箭頭 = 基底 → 以它為底的 image；或只在特定情況發生")',
 ' ("CI", "放在 GitHub 上的自動化流程：打 tag 時 build image 並上傳 GHCR"),\n])': ' ("CI", "放在 GitHub 上的自動化流程：打 tag 時 build image 並上傳 GHCR"),\n ("just / justfile", "just 是主機上的指令跑器；justfile 是專案裡給它讀的指令清單，也就是啟動器"),\n ("印記檔", ".<name>/.stamp：安裝時寫下「版本 + 每檔指紋」，之後用來檢查有沒有被手改"),\n ("tag / digest", "image 的版本名稱（v0.43.0）／內容指紋（sha256:…）；.version 兩者都記，工具只認 digest"),\n])',
 'page("p1b", "2. 框架定義", p1b, w=1800, h=1080)': 'page("p1b", "2. 框架定義", p1b, w=1800, h=1160)',
 # ---------- 頁 3 ----------
 'p2.append(e("be3", "b_l2", "b_c0", "不同或不存在", (1, 0.5), (0, 0.5)))': 'p2.append(e("be3", "b_l2", "b_c0", "不同或不存在", (1, 0.5), (0, 0.5), pos=-0.4))',
 'p2.append(e("be7", "b_c1", "b_l3", "通過", (0, 0.75), (0.5, 0)))': 'p2.append(e("be7", "b_c1", "b_l3", "通過", (0, 0.85), (0.5, 0), vert=True, pos=0.6))',
 '<mxCell id="be8" value="失敗" style="\' + EDGE + \'align=left;verticalAlign=middle;spacingLeft=8;spacingBottom=0;exitX=0;exitY=0.35;': '<mxCell id="be8" value="失敗" style="\' + EDGE + \'exitX=0;exitY=0.25;',
 '<Array as="points"><mxPoint x="340" y="191"/><mxPoint x="340" y="285"/></Array></mxGeometry></mxCell>\'.replace(\'<mxGeometry relative="1" as="geometry">\', \'<mxGeometry x="0.5" relative="1" as="geometry">\'))': '<Array as="points"><mxPoint x="340" y="185"/><mxPoint x="340" y="285"/></Array></mxGeometry></mxCell>\'.replace(\'<mxGeometry relative="1" as="geometry">\', \'<mxGeometry x="-0.6" relative="1" as="geometry">\'))',
 'p2 += legend_flow("p2", 40, 1220, files=True)': 'p2 += legend_flow("p2", 40, 1220, files=True, note=True, dashed=True)',
 ' ("docker compose", "工具腳本最後真正用來啟動專案容器的指令"),\n])': ' ("docker compose", "工具腳本最後真正用來啟動專案容器的指令"),\n ("just", "主機上的指令跑器；使用者打 just <指令>，它照 justfile 執行"),\n ("init.toml", "工具提供的清單：init 時要複製到專案的初始檔有哪些、放哪"),\n ("entrypoint / hooks", "初始檔的例子：容器啟動腳本／各指令前後可掛的自訂腳本"),\n])',
 'page("p2", "3. 流程：使用者指令", p2, w=1700, h=1480)': 'page("p2", "3. 流程：使用者指令", p2, w=1700, h=1580)',
 # ---------- 頁 4 ----------
 'p3 += legend_flow("p3", 40, 720)': 'p3 += legend_flow("p3", 40, 720, purple=False, startend=False, err=False, note=True)',
 ' ("image 附註", "image 上的標籤（label）：記錄它來自工具 repo 的哪個 commit、什麼版本"),\n])': ' ("image 附註", "image 上的標籤（label）：記錄它來自工具 repo 的哪個 commit、什麼版本"),\n ("digest", "image 的內容指紋（sha256:…）；同一個 digest 永遠是同一份內容"),\n])',
 '"來源暫時指向本機的工具原始碼\\n改工具不必每次發佈 image 就能在專案裡測"': '".version 暫時指向本機的工具原始碼（而非 GHCR image）\\n改工具不必每次發佈 image 就能在專案裡測"',
 'page("p3", "4. 流程：版本生命週期", p3, h=1000)': 'page("p3", "4. 流程：版本生命週期", p3, h=1030)',
 # ---------- 頁 5 ----------
 'p4 += legend_flow("p4", 40, 900, purple=False)': 'p4 += legend_flow("p4", 40, 900, purple=False, note=True)',
 ' ("src → dest", "init.toml 每一項：src 是 image 內 dist/ 的相對路徑，dest 是專案內的相對路徑"),\n])': ' ("src → dest", "init.toml 每一項：src 是 image 內 dist/ 的相對路徑，dest 是專案內的相對路徑"),\n ("原子替換", "改名是一步完成的動作，不會出現「一半新一半舊」的目錄"),\n ("印記 / 指紋", "印記 = .<name>/.stamp（版本 + 每檔指紋）；指紋 = 檔案內容算出的 sha256"),\n])',
 'page("p4", "5. 流程：vendor_kit 內部", p4, w=1920, h=1100)': 'page("p4", "5. 流程：vendor_kit 內部", p4, w=1920, h=1160)',
 # ---------- 頁 6（原型對照） ----------
 'p7.append(e("x4", "g_tool", "f_land", "docker run\\n… install", (1, 0.75), (0, 0.75), pos=0.15))': 'p7.append(e("x4", "g_tool", "f_land", "docker run\\n… install", (1, 0.75), (0, 0.75), pos=0.5))',
 'p7.append(v("f_user", "r_proj", LEAF(), "Dockerfile、setup.toml…\\n（init 建立後歸使用者）", 20, 120, 300, 50))': 'p7.append(v("f_user", "r_proj", LEAF(), "Dockerfile、設定檔（setup.toml）…\\n（init 建立後歸使用者）", 20, 120, 300, 50))',
 'p7 += legend("p7", 40, 640, ["red", "green", "yellow", "pimg", "white"], "實線 = 傳輸內容\\n虛線 = 基底依賴")': 'p7 += legend("p7", 40, 640, ["red", "green", "yellow", "pimg", "white"], "實線 = 傳輸內容\\n虛線箭頭 = 基底 → 以它為底的 image")',
 ' ("tool", "原型裡那個範例工具的名字；所以它的 image 叫 tool-dist、安裝目錄叫 .tool/"),\n])': ' ("tool", "原型裡那個範例工具的名字；所以它的 image 叫 tool-dist、安裝目錄叫 .tool/"),\n (".stamp", "印記檔：install 寫下的「版本 + 每檔指紋」"),\n ("setup.toml", "範例工具給專案的設定檔（TOML）"),\n])',
 '+ page("p7", "6. 原型對照", p7, h=860)': '+ page("p7", "6. 原型對照", p7, h=920)',
}
for k, val in R.items():
    assert s.count(k) == 1, (k[:80], s.count(k))
    s = s.replace(k, val)
open("gen16.py", "w", encoding="utf-8").write(s)
print("ok")
