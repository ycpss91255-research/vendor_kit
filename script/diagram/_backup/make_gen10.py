s = open("gen9.py", encoding="utf-8").read()
R = {
 # ---------- 頁 1 ----------
 'p1.append(v("user", "1", SW(YELLOW), "使用者", 40, VY, 140, 820))': 'p1.append(v("user", "1", SW(YELLOW), "使用者", 40, VY, 140, 860))',
 'p1.append(v("u_out", "user", LEAF(GREY), "畫面", 26, 720, 88, 40))': 'p1.append(v("u_out", "user", LEAF(GREY), "畫面", 26, 760, 88, 40))',
 'p1.append(v("i_list", "img", LEAF(), "檔案清單", 46, 81, 88, 40))': 'p1.append(v("i_list", "img", LEAF(), "init.toml", 46, 121, 88, 40))',
 'p1.append(v("i_dist", "img", LEAF(GREY), "工具檔案", 46, 132, 88, 40))': 'p1.append(v("i_dist", "img", LEAF(GREY), "dist/（全部）", 46, 172, 88, 40))',
 'p1.append(v("i_tpl", "img", LEAF(GREY), "模板", 46, 183, 88, 40))': 'p1.append(v("i_tpl", "img", LEAF(GREY), "模板", 46, 223, 88, 40))',
 'p1.append(v("img", "1", SW(YELLOW), "image 內容", 200, 300, 180, 240))': 'p1.append(v("img", "1", SW(YELLOW), "image 內容", 200, 300, 180, 280))',
 'p1.append(v("vk", "1", SW(RED), "vendor_kit", VX, VY, 480, 820))': 'p1.append(v("vk", "1", SW(RED), "vendor_kit", VX, VY, 480, 860))',
 'p1.append(v("m_cli", "vk", SW(RED), "命令介面", 20, 50, 200, 100))\np1.append(v("cli_land", "m_cli", LEAF(), "land", 8, 48, 58, 40))\np1.append(v("cli_verify", "m_cli", LEAF(), "verify", 71, 48, 58, 40))\np1.append(v("cli_diff", "m_cli", LEAF(), "diff", 134, 48, 58, 40))':
 'p1.append(v("m_cli", "vk", SW(RED), "命令介面", 20, 50, 200, 140))\np1.append(v("cli_land", "m_cli", LEAF(), "land", 12, 45, 88, 40))\np1.append(v("cli_init", "m_cli", LEAF(), "init", 104, 45, 88, 40))\np1.append(v("cli_verify", "m_cli", LEAF(), "verify", 12, 92, 88, 40))\np1.append(v("cli_diff", "m_cli", LEAF(), "diff", 104, 92, 88, 40))',
 'p1.append(v("m_list", "vk", SW(RED), "清單處理", 20, 210, 200, 170))\np1.append(v("ls_read", "m_list", LEAF(), "讀取", 12, 45, 88, 40))\np1.append(v("ls_check", "m_list", LEAF(), "驗證", 104, 45, 88, 40))\np1.append(v("ls_class", "m_list", LEAF(), "分類：工具檔／初始檔／選用檔", 12, 92, 180, 40))':
 'p1.append(v("m_list", "vk", SW(RED), "出貨內容讀取", 20, 250, 200, 170))\np1.append(v("ls_read", "m_list", LEAF(), "讀 dist/", 12, 45, 88, 40))\np1.append(v("ls_check", "m_list", LEAF(), "讀 init.toml", 104, 45, 88, 40))\np1.append(v("ls_class", "m_list", LEAF(), "驗證", 12, 92, 88, 40))',
 'p1.append(v("m_tpl", "vk", SW(RED), "模板", 20, 440, 200, 130))': 'p1.append(v("m_tpl", "vk", SW(RED), "模板", 20, 480, 200, 130))',
 'p1.append(v("m_diff", "vk", SW(RED), "差異比對", 20, 630, 200, 130))': 'p1.append(v("m_diff", "vk", SW(RED), "差異比對", 20, 670, 200, 130))',
 'p1.append(v("m_write", "vk", SW(RED), "專案檔案存取", 260, 210, 200, 170))': 'p1.append(v("m_write", "vk", SW(RED), "專案檔案存取", 260, 250, 200, 170))',
 'p1.append(v("m_stamp", "vk", SW(RED, 16), "印記", 350, 440, 110, 130))': 'p1.append(v("m_stamp", "vk", SW(RED, 16), "印記", 350, 480, 110, 130))',
 'p1.append(v("m_report", "vk", SW(RED), "回報", 260, 630, 200, 130))': 'p1.append(v("m_report", "vk", SW(RED), "回報", 260, 670, 200, 130))',
 'p1.append(v("proj", "1", SW(YELLOW), "專案目錄", 1000, VY, 200, 820))': 'p1.append(v("proj", "1", SW(YELLOW), "專案目錄", 1000, VY, 200, 860))',
 'p1.append(v("p_stamp", "proj", LEAF(), "印記檔", 56, 241, 88, 40))': 'p1.append(v("p_stamp", "proj", LEAF(), "印記檔", 56, 281, 88, 40))',
 'p1.append(v("p_base", "proj", LEAF(), ".base/", 56, 292, 88, 40))': 'p1.append(v("p_base", "proj", LEAF(), ".base/", 56, 332, 88, 40))',
 'p1.append(v("p_user", "proj", LEAF(GREY), "使用者檔案", 56, 343, 88, 40))': 'p1.append(v("p_user", "proj", LEAF(GREY), "使用者檔案", 56, 383, 88, 40))',
 'p1.append(e("a3", "i_list", "m_list", "檔案清單", (1, 0.5), (0, 0.3)))': 'p1.append(e("a3", "i_list", "m_list", "init 清單", (1, 0.5), (0, 0.3)))',
 'p1.append(e("a4", "i_dist", "m_list", "檔案內容", (1, 0.5), (0, 0.6)))': 'p1.append(e("a4", "i_dist", "m_list", "dist 內容", (1, 0.5), (0, 0.6)))',
 'p1.append(e("a6", "m_list", "m_write", "工具檔", (1, 0.3), (0, 0.3)))': 'p1.append(e("a6", "m_list", "m_write", "dist 全部", (1, 0.3), (0, 0.3)))',
 'p1.append(e("a7", "m_list", "m_tpl", "初始檔／選用檔\\n清單、模板", (0.5, 1), (0.5, 0), vert="left"))': 'p1.append(e("a7", "m_list", "m_tpl", "init 清單\\n＋模板", (0.5, 1), (0.5, 0), vert="left"))',
 'p1.append(e("a11", "m_write", "p_base", "工具檔", (1, 0.6), (0, 0.5), both=True))': 'p1.append(e("a11", "m_write", "p_base", "dist 全部", (1, 0.6), (0, 0.5), both=True))',
 '<mxPoint x="810" y="740"/><mxPoint x="680" y="740"/>': '<mxPoint x="810" y="780"/><mxPoint x="680" y="780"/>',
 'p1 += legend_arch("p1", 40, 1020)': 'p1 += legend_arch("p1", 40, 1060)',
 'page("p1", "1. vendor_kit 架構圖", p1, w=1700)': 'page("p1", "1. vendor_kit 架構圖", p1, w=1700, h=1150)',
 # ---------- 頁 2 ----------
 'p1b.append(v("b_list", "base", LEAF(), "檔案清單", 22, 110, 88, 40))': 'p1b.append(v("b_list", "base", LEAF(), "init.toml", 22, 110, 88, 40))',
 'p1b.append(v("c_tools", "sc", LEAF(), "工具檔", 12, 45, 88, 40))': 'p1b.append(v("c_tools", "sc", LEAF(), "dist 全部", 12, 45, 88, 40))',
 '"進 git；缺少時才建立"': '"進 git；init 建立"',
 '"不進 git；每次安裝整批替換"': '"不進 git；每次 upgrade 整批覆蓋"',
 'p1b.append(e("b9", "ds_engine", "sc", "工具檔、印記檔", (1, 0.3), (0.5, 0), both=True))': 'p1b.append(e("b9", "ds_engine", "sc", "dist、印記檔", (1, 0.3), (0.5, 0), both=True))',
 # ---------- 頁 3 ----------
 '"啟動安裝容器，執行 land\\n（安裝工具檔到 .base/）"': '"啟動安裝容器，執行 land\\n（dist 全部寫進 .base/）"',
 'p2.append(v("c13", "1", RHOMBUS, "工具檔完整？", 290, 560, 180, 90))': 'p2.append(v("c13", "1", RHOMBUS, ".base/ 完整？", 290, 560, 180, 90))',
 # ---------- 頁 4 ----------
 '".base/ 工具檔：整批替換"': '".base/ 整批覆蓋（非 init 的東西全部換新）"',
 '"執行 diff：\\n新版模板與使用者檔案有差異？"': '"執行 diff：init.toml 列的檔案\\n新版模板有差異？"',
 # ---------- 頁 6 ----------
 ' ("檔案清單（manifest）", "列出每個檔案，以及它屬於「工具擁有／第一次建立／可選」哪一類"),': ' ("init.toml", "init 清單：列出 init 時要複製到專案的初始檔；不在清單上的每次 upgrade 都覆蓋"),',
 ' ("dist", "base 要送給各專案用的那批工具檔案"),': ' ("dist", "工具要出貨的那批檔案，全部寫進下游的 .base/"),',
 ' ("印記檔", "安裝時寫下的紀錄：版本 + 每個工具檔的指紋（不含使用者檔案）"),': ' ("印記檔", "安裝時寫下的紀錄：版本 + .base/ 每個檔案的指紋"),',
 # ---------- 頁 7 ----------
 'p7.append(v("f_dist", "r_base", LEAF(GREY), "dist/\\n（wrapper、lib）", 20, 70, 120, 50))': 'p7.append(v("f_dist", "r_base", LEAF(GREY), "dist/\\n（全部出貨，含模板）", 20, 70, 260, 50))',
 'p7.append(v("f_tpl", "r_base", LEAF(GREY), "templates/\\n（Dockerfile…）", 160, 70, 120, 50))': '',
 'p7.append(v("f_man", "r_base", LEAF(), "manifest\\n（檔案清單）", 20, 130, 120, 50))': 'p7.append(v("f_man", "r_base", LEAF(), "init.toml\\n（init 清單）", 20, 130, 120, 50))',
 '"Dockerfile.dist：FROM vendor_kit:v1，再疊上左邊三樣"': '"Dockerfile.dist：FROM vendor_kit:v1，再疊上 dist/ 與 init.toml"',
}
for k, val in R.items():
    assert s.count(k) == 1, (k, s.count(k))
    s = s.replace(k, val)

# ---------- 頁 5 全部重寫 ----------
s5 = s.index("# ================= Page 4: 流程：引擎 =================")
e5 = s.index("# ================= Page 6: 名詞說明 =================")
p5 = r'''# ================= Page 5: 流程：安裝工具 =================
p4 = [v("title", "1", TITLE, "流程：安裝工具（vendor_kit）四個子命令 — 全部在安裝容器內執行", 40, 20, 1000, 30)]
# land
p4.append(v("land", "1", SW(NEUTRAL), "land（安裝／upgrade）", 20, 60, 380, 560))
p4.append(v("l0", "land", ELLIPSE(GREEN), "開始 land", 110, 50, 160, 50))
p4.append(v("l1", "land", LEAF(), "讀取 image 內的 dist/", 90, 130, 200, 40))
p4.append(v("l2", "land", LEAF(), "複製 dist/ 全部到暫存目錄", 90, 200, 200, 40))
p4.append(v("l3", "land", LEAF(), "寫入印記（版本 + 每檔指紋）", 90, 270, 200, 40))
p4.append(v("l4", "land", LEAF(), "暫存目錄換名為 .base/\n（整批覆蓋、原子替換）", 90, 340, 200, 50))
p4.append(v("l5", "land", ELLIPSE(GREEN), "成功結束", 110, 430, 160, 40))
p4.append(v("ln", "land", NOTE, "任一步失敗即中止，舊 .base/ 不動；\n啟動器不會執行工具檔", 60, 490, 260, 50))
p4.append(e("le0", "l0", "l1")); p4.append(e("le1", "l1", "l2")); p4.append(e("le2", "l2", "l3")); p4.append(e("le3", "l3", "l4")); p4.append(e("le4", "l4", "l5"))
# init
p4.append(v("init", "1", SW(NEUTRAL), "init（第一次）", 440, 60, 440, 760))
p4.append(v("i0", "init", ELLIPSE(GREEN), "開始 init", 140, 50, 160, 50))
p4.append(v("i1", "init", LEAF(), "讀 init.toml", 120, 130, 200, 40))
p4.append(v("i2", "init", RHOMBUS, "還有項目？", 130, 200, 180, 80))
p4.append(v("i3", "init", LEAF(), "取下一項（src → dest）", 120, 320, 200, 40))
p4.append(v("i4", "init", RHOMBUS, "dest 已存在？", 130, 390, 180, 80))
p4.append(v("i5", "init", LEAF(), "略過（保留使用者版本）", 20, 510, 180, 40))
p4.append(v("i6", "init", LEAF(), "從 dist/ 複製建立", 240, 510, 180, 40))
p4.append(v("i7", "init", ELLIPSE(GREEN), "成功結束", 140, 640, 160, 40))
p4.append(e("ie0", "i0", "i1")); p4.append(e("ie1", "i1", "i2"))
p4.append(e("ie2", "i2", "i3", "有", (0.5, 1), (0.5, 0), vert=True))
p4.append(e("ie3", "i3", "i4"))
p4.append(e("ie4", "i4", "i5", "已有", (0, 0.5), (0.5, 0), vert=True))
p4.append(e("ie5", "i4", "i6", "沒有", (1, 0.5), (0.5, 0), vert=True))
p4.append('<mxCell id="ie6" value="沒有了" style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="init" source="i2" target="i7"><mxGeometry x="-0.85" relative="1" as="geometry"><Array as="points"><mxPoint x="425" y="240"/><mxPoint x="425" y="610"/><mxPoint x="220" y="610"/></Array></mxGeometry></mxCell>')
p4.append('<mxCell id="ib1" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i5" target="i2"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="110" y="580"/><mxPoint x="10" y="580"/><mxPoint x="10" y="240"/></Array></mxGeometry></mxCell>')
p4.append('<mxCell id="ib2" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i6" target="i2"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="330" y="580"/><mxPoint x="10" y="580"/><mxPoint x="10" y="240"/></Array></mxGeometry></mxCell>')
# verify
p4.append(v("verify", "1", SW(NEUTRAL), "verify（檢查）", 920, 60, 440, 480))
p4.append(v("v0", "verify", ELLIPSE(GREEN), "開始 verify", 140, 50, 160, 50))
p4.append(v("v1", "verify", LEAF(), "讀取印記", 120, 130, 200, 40))
p4.append(v("v2", "verify", LEAF(), "重新計算 .base/ 每檔指紋", 120, 200, 200, 40))
p4.append(v("v3", "verify", RHOMBUS, "全部相符？", 130, 270, 180, 80))
p4.append(v("v4", "verify", ELLIPSE(GREEN), "通過", 20, 390, 160, 50))
p4.append(v("v5", "verify", ELLIPSE(RED), "失敗：列出被改的檔案", 240, 390, 180, 50))
p4.append(e("ve0", "v0", "v1")); p4.append(e("ve1", "v1", "v2")); p4.append(e("ve2", "v2", "v3"))
p4.append(e("ve3", "v3", "v4", "是", (0, 0.5), (0.5, 0), vert=True))
p4.append(e("ve4", "v3", "v5", "否", (1, 0.5), (0.5, 0), vert=True))
# diff
p4.append(v("diff", "1", SW(NEUTRAL), "diff（比對）", 1400, 60, 440, 480))
p4.append(v("d0", "diff", ELLIPSE(GREEN), "開始 diff", 140, 50, 160, 50))
p4.append(v("d1", "diff", LEAF(), "對 init.toml 的每一項：\n新版 src vs 專案內的 dest", 100, 130, 240, 50))
p4.append(v("d3", "diff", RHOMBUS, "有差異？", 130, 220, 180, 80))
p4.append(v("d4", "diff", ELLIPSE(GREEN), "無差異", 20, 340, 180, 50))
p4.append(v("d5", "diff", LEAF(), "顯示差異\n（不改使用者檔案）", 240, 335, 180, 60))
p4.append(e("de0", "d0", "d1")); p4.append(e("de2", "d1", "d3"))
p4.append(e("de3", "d3", "d4", "否", (0, 0.5), (0.5, 0), vert=True))
p4.append(e("de4", "d3", "d5", "是", (1, 0.5), (0.5, 0), vert=True))
p4 += legend_flow("p4", 40, 900)

'''
s = s[:s5] + p5 + s[e5:]
s = s.replace('page("p4", "5. 流程：安裝工具", p4, w=1700, h=1250)', 'page("p4", "5. 流程：安裝工具", p4, w=1900, h=1000)')
open("gen10.py", "w", encoding="utf-8").write(s)
print("ok")
