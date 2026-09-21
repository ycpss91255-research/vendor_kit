s = open("gen14.py", encoding="utf-8").read()

# ---- 1) 線上文字 12pt ----
s = s.replace('"strokeWidth=2;align=center;verticalAlign=bottom;spacingBottom=6;fontFamily=Helvetica;fontSize=10;"',
              '"strokeWidth=2;align=center;verticalAlign=bottom;spacingBottom=6;fontFamily=Helvetica;fontSize=12;"')
assert 'fontSize=12;"\n        "fontColor=default' in s

# ---- 2/3) 圖例改為可選項目；紫色 swimlane ----
old = s[s.index("def legend_arch("):s.index("def legend_flow(")]
new = '''PURPLE_SW = (f"swimlane;html=1;rounded=1;startSize=38;fontStyle=1;fontSize=18;container=1;collapsible=1;"
             f"recursiveResize=0;fillColor={PURPLE};swimlaneFillColor=#ffffff;strokeColor=#9673a6;strokeWidth=2;")
LEGEND_ITEMS = {
 "red":    (LEGEND_BOX(RED),    "紅：我們要開發的模組", 200, 60, 0),
 "green":  (LEGEND_BOX(GREEN),  "綠：使用框架的 repo", 200, 60, 0),
 "yellow": (LEGEND_BOX(YELLOW), "黃：外部系統", 160, 60, 0),
 "purple": (PURPLE_SW,          "紫：container（執行形態）", 220, 60, 0),
 "pimg":   (PURPLE_LEAF,        "紫：image / container", 180, 40, 10),
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
    return legend(prefix, x, y, ["red", "green", "yellow", "pimg", "white"], "實線 = 傳輸內容（線上文字 = 傳什麼）\\n虛線 = 基底依賴，或只在特定情況發生")
TERM_K = "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999999;fontSize=12;fontStyle=1;align=left;spacingLeft=6;strokeWidth=1;"
TERM_V = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=12;align=left;spacingLeft=6;strokeWidth=1;"
def terms(prefix, x, y, rows, kw=170, vw=900, rh=30):
    c = [v(f"{prefix}_th", "1", TEXT(13) + "align=left;fontStyle=1;", "本頁名詞", x, y - 24, 200, 20)]
    for i, (k, d) in enumerate(rows):
        c.append(v(f"{prefix}_tk{i}", "1", TERM_K, k, x, y + i * rh, kw, rh))
        c.append(v(f"{prefix}_tv{i}", "1", TERM_V, d, x + kw, y + i * rh, vw, rh))
    return c

'''
s = s.replace(old, new)

R = {
 # ---------- 頁 1 ----------
 'p1.append(v("u_cmd", "user", LEAF(GREY), "指令", 26, 90, 88, 40))': 'p1.append(v("u_cmd", "user", LEAF(), "指令", 26, 100, 88, 40))',
 'p1.append(v("u_out", "user", LEAF(GREY), "畫面", 26, 760, 88, 40))': 'p1.append(v("u_out", "user", LEAF(), "畫面", 26, 760, 88, 40))',
 'p1.append(v("i_dist", "img", LEAF(GREY), "dist/（全部）", 46, 172, 88, 40))': 'p1.append(v("i_dist", "img", LEAF(), "dist/（全部）", 46, 172, 88, 40))',
 'p1.append(v("i_tpl", "img", LEAF(GREY), "模板", 46, 223, 88, 40))': 'p1.append(v("i_tpl", "img", LEAF(), "模板", 46, 223, 88, 40))',
 'p1.append(v("vk", "1", SW(RED), "vendor_kit", VX, VY, 520, 860))': 'p1.append(v("vk", "1", PURPLE_SW, "vendor_kit（一個 container）", VX, VY, 520, 860))',
 'p1.append(v("p_user", "proj", LEAF(GREY), "使用者檔案", 56, 383, 88, 40))': 'p1.append(v("p_user", "proj", LEAF(), "使用者檔案", 56, 383, 88, 40))',
 'p1.append(e("a15", "m_stamp", "m_report", "檢查結果", (0.5, 1), (0.77, 0), vert=True))': 'p1.append(e("a15", "m_stamp", "m_report", "檢查結果", (0.5, 1), (0.725, 0), vert=True))',
 'p1 += legend_arch("p1", 40, 1060)': '''p1 += legend("p1", 40, 1060, ["purple", "red", "yellow", "white"], "實線 = 傳輸內容（線上文字 = 傳什麼）\\n虛線 = 只在特定情況發生")
p1 += terms("p1", 40, 1170, [
 ("vendor_kit", "通用安裝工具；只以 container 形態執行（開發、使用皆是），主機不需安裝"),
 ("模組", "vendor_kit 內部的功能分塊；同一個 container 裡，不是各自的 container"),
 ("dist/", "工具 repo 裡要出貨的那批檔案，全部寫進專案的 .<name>/"),
 ("init.toml", "工具 repo 提供的清單：init 時要複製到專案的初始檔；不在清單上的每次 upgrade 都覆蓋"),
 ("印記檔", ".<name>/.stamp：版本 + 每個檔案的指紋；verify 用它判斷有沒有被手改"),
 ("指紋", "由檔案內容算出的一串碼（sha256）；內容一改就不同"),
])''',
 'page("p1", "1. vendor_kit 架構圖", p1, w=1700, h=1150)': 'page("p1", "1. vendor_kit 架構圖", p1, w=1700, h=1400)',
 # ---------- 頁 2 ----------
 'p1b.append(v("t_dist", "tool", LEAF(GREY), "dist/\\n（要出貨的全部）", 20, 80, 135, 50))': 'p1b.append(v("t_dist", "tool", LEAF(), "dist/\\n（要出貨的全部）", 20, 80, 135, 50))',
 'p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 190, 200, 40))': 'p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 150, 200, 40))',
 'p1b.append(v("pc2", "proj", SW(RED), ".<name2>/（另一個工具）", 540, 480, 220, 50))': 'p1b.append(v("pc2", "proj", SW(RED), ".<name2>/（另一個工具）", 540, 465, 220, 50))',
 'p1b.append(v("p_just", "pa", LEAF(), "justfile", 158, 52, 90, 40))': 'p1b.append(v("p_just", "pa", LEAF(), "justfile", 158, 50, 90, 40))',
 'p1b.append(v("h_docker", "host", LEAF(GREY), "Docker\\n（跑所有容器）", 20, 390, 120, 50))': 'p1b.append(v("h_docker", "host", LEAF(GREY), "Docker\\n（跑所有容器）", 20, 378, 120, 50))',
 'p1b += legend_arch("p1b", 40, 900)': '''p1b += legend("p1b", 40, 700, ["red", "green", "yellow", "pimg", "white", "grey"], "實線 = 傳輸內容\\n虛線 = 基底依賴，或只在特定情況發生")
p1b += terms("p1b", 40, 810, [
 ("工具 repo", "任何想透過 vendor_kit 出貨的工具的原始碼 repo；必須有 dist/、init.toml、Dockerfile.dist、CI"),
 ("專案 repo", "使用工具的專案；必須有 .version、justfile；可同時用多個工具"),
 ("vendor_kit repo", "我們要開發的：安裝工具的原始碼，打包成 vendor_kit image"),
 ("image / 容器", "image = 打包好的程式與檔案；容器 = image 執行起來的實例，跑完可刪"),
 ("GHCR", "GitHub 提供的 image 倉庫；每個工具一個 <name>-dist image，以 vendor_kit image 為底"),
 (".version", "專案裡的 TOML 檔，一個工具一行 name = \\"image:tag@sha256:…\\"；name 決定安裝目錄 .<name>/"),
 ("CI", "放在 GitHub 上的自動化流程：打 tag 時 build image 並上傳 GHCR"),
])''',
 'page("p1b", "2. 框架定義", p1b, w=1800)': 'page("p1b", "2. 框架定義", p1b, w=1800, h=1080)',
 # ---------- 頁 3 ----------
 'p2.append(v("a_p1", "bA", FILE, ".<name>/（新）", 1240, 70, 200, 40))': 'p2.append(v("a_p1", "bA", FILE, ".<name>/（新）", 1240, 75, 200, 40))',
 'p2 += legend_flow("p2", 40, 1220, files=True)': '''p2 += legend_flow("p2", 40, 1220, files=True)
p2 += terms("p2", 40, 1330, [
 ("啟動器", "專案裡的 justfile：使用者打 just 指令時，它讀 .version、起安裝容器、再執行工具的腳本"),
 ("印記", ".<name>/.stamp：install 寫下的「版本 + 每檔指紋」；日常每次 just 都拿它比對"),
 ("Renovate", "GitHub 上的機器人：GHCR 有新版就自動開 PR 改 .version；沒有它時用 just upgrade 手動"),
 ("docker compose", "工具腳本最後真正用來啟動專案容器的指令"),
])''',
 'page("p2", "3. 流程：使用者指令", p2, w=1700, h=1320)': 'page("p2", "3. 流程：使用者指令", p2, w=1700, h=1480)',
 # ---------- 頁 4 ----------
 'p3 += legend_flow("p3", 40, 1000)': '''p3 += legend_flow("p3", 40, 720)
p3 += terms("p3", 40, 830, [
 ("commit", "git 的一次版本紀錄"),
 ("PR", "GitHub 上的合併請求；merge 就是接受這次修改"),
 ("git bisect", "git 的二分搜尋：在 .version 的修改紀錄中找出哪次升級引入問題"),
 ("image 附註", "image 上的標籤（label）：記錄它來自工具 repo 的哪個 commit、什麼版本"),
])''',
 'page("p3", "4. 流程：版本生命週期", p3)': 'page("p3", "4. 流程：版本生命週期", p3, h=1000)',
 # ---------- 頁 5 ----------
 'p4.append(v("d6", "diff", ELLIPSE(GREEN), "結束（不改使用者檔案）", 220, 420, 200, 40))': 'p4.append(v("d6", "diff", ELLIPSE(GREEN), "結束（不改使用者檔案）", 230, 420, 200, 40))',
 'p4 += legend_flow("p4", 40, 900, purple=False)': '''p4 += legend_flow("p4", 40, 900, purple=False)
p4 += terms("p4", 40, 1010, [
 ("暫存目錄", "先把整個 dist/ 寫到 .<name>.tmp/，最後一步才改名成 .<name>/；中途失敗舊目錄不受影響"),
 ("src → dest", "init.toml 每一項：src 是 image 內 dist/ 的相對路徑，dest 是專案內的相對路徑"),
])''',
 'page("p4", "5. 流程：vendor_kit 內部", p4, w=1920, h=1000)': 'page("p4", "5. 流程：vendor_kit 內部", p4, w=1920, h=1100)',
 # ---------- 頁 7 ----------
 'p7.append(v("f_dist", "r_tool", LEAF(GREY), "dist/\\n（全部出貨，含模板）", 20, 70, 260, 50))': 'p7.append(v("f_dist", "r_tool", LEAF(), "dist/\\n（全部出貨，含模板）", 20, 70, 260, 50))',
 'p7.append(v("f_user", "r_proj", LEAF(GREY), "Dockerfile、setup.toml…\\n（init 建立後歸使用者）", 20, 120, 300, 50))': 'p7.append(v("f_user", "r_proj", LEAF(), "Dockerfile、setup.toml…\\n（init 建立後歸使用者）", 20, 120, 300, 50))',
 'p7.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:v1", 40, 90, 220, 50))': 'p7.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:v1", 40, 70, 220, 50))',
 'p7.append(v("g_tool", "ghcr", PURPLE_LEAF, "tool-dist:v0.1.0", 40, 390, 220, 50))': 'p7.append(v("g_tool", "ghcr", PURPLE_LEAF, "tool-dist:v0.1.0", 40, 370, 220, 50))',
 'p7.append(v("f_land", "r_proj", LEAF(), ".tool/ ＋ .stamp\\n（不進 git，install 寫出）", 20, 390, 300, 50))': 'p7.append(v("f_land", "r_proj", LEAF(), ".tool/ ＋ .stamp\\n（不進 git，install 寫出）", 20, 370, 300, 50))',
 'p7 += legend_arch("p7", 40, 640)': '''p7 += legend("p7", 40, 640, ["red", "green", "yellow", "pimg", "white"], "實線 = 傳輸內容\\n虛線 = 基底依賴")
p7 += terms("p7", 40, 750, [
 ("proto/", "可執行的原型：三個資料夾各對應框架裡的一個角色；image 只 build 到本機，沒有 push"),
 ("tool", "原型裡那個範例工具的名字；所以它的 image 叫 tool-dist、安裝目錄叫 .tool/"),
])''',
 '+ page("p7", "7. 原型對照", p7, h=760)': '+ page("p7", "7. 原型對照", p7, h=860)',
}
for k, val in R.items():
    assert s.count(k) == 1, (k[:70], s.count(k))
    s = s.replace(k, val)

# ---- 5) 移除第 6 頁 ----
a6 = s.index("# ================= Page 6: 名詞說明 =================")
b6 = s.index("# ================= Page 7: 原型對照 =================")
s = s[:a6] + s[b6:]
s = s.replace('       + page("p6", "6. 名詞說明", p6)\n', '')
s = s.replace('page("p7", "7. 原型對照"', 'page("p7", "6. 原型對照"')
open("gen15.py", "w", encoding="utf-8").write(s)
print("ok")
