import re
src = open("gen18.py").read()

def rep(old, new, count=1):
    global src
    assert src.count(old) == count, (src.count(old), old[:80])
    src = src.replace(old, new)

# ---- e(): 新增 below（標籤放線下）----
rep('''    if vert == "left": st += "align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;"
    elif vert: st += "align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;"''',
'''    if vert == "left": st += "align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;"
    elif vert == "below": st += "verticalAlign=top;spacingTop=6;spacingBottom=0;"
    elif vert: st += "align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;"''')

# ================= 頁 1 =================
# 專案 repo 的目錄：三個最小單元統一 88×40、間距 ≥16；線的出入口對齊各自中心
rep('p1.append(v("p_stamp", "proj", LEAF(), ".<name>/.stamp\\n（印記檔）", 46, 276, 108, 50))',
    'p1.append(v("p_stamp", "proj", LEAF(), ".stamp\\n（印記檔）", 56, 250, 88, 40))')
rep('p1.append(v("p_base", "proj", LEAF(), ".<name>/", 46, 327, 108, 50))',
    'p1.append(v("p_base", "proj", LEAF(), ".<name>/", 56, 306, 88, 40))')
rep('p1.append(v("p_user", "proj", LEAF(), "使用者檔案", 56, 383, 88, 40))',
    'p1.append(v("p_user", "proj", LEAF(), "使用者檔案", 56, 376, 88, 40))')
rep('p1.append(e("a10", "m_write", "p_stamp", "印記檔", (1, 0.3), (0, 0.5), both=True))',
    'p1.append(e("a10", "m_write", "p_stamp", "印記檔", (1, 0.1176), (0, 0.5), both=True))')
rep('p1.append(e("a11", "m_write", "p_base", "dist 全部", (1, 0.6), (0, 0.5), both=True))',
    'p1.append(e("a11", "m_write", "p_base", "dist 全部", (1, 0.4471), (0, 0.5), both=True))')
rep('p1.append(e("a12", "m_write", "p_user", "初始檔（init 時）", (1, 0.85), (0, 0.3)))',
    'p1.append(e("a12", "m_write", "p_user", "初始檔（init 時）", (1, 0.8), (0, 0.25)))')
rep('p1.append(e("a12b", "p_user", "m_write", "現有內容（diff 時）", (0, 0.7), (1, 0.95)))',
    'p1.append(e("a12b", "p_user", "m_write", "現有內容（diff 時）", (0, 0.76), (1, 0.92), vert="below"))')
# a13：與 a8 拉開距離
rep("exitX=0.15;exitY=1;exitDx=0;exitDy=0;entryX=0.9;entryY=0;entryDx=0;entryDy=0;\" edge=\"1\" parent=\"1\" source=\"m_write\" target=\"m_diff\"><mxGeometry x=\"0.55\" relative=\"1\" as=\"geometry\"><Array as=\"points\"><mxPoint x=\"810\" y=\"780\"/>",
    "exitX=0.3;exitY=1;exitDx=0;exitDy=0;entryX=0.9;entryY=0;entryDx=0;entryDy=0;\" edge=\"1\" parent=\"1\" source=\"m_write\" target=\"m_diff\"><mxGeometry x=\"0.55\" relative=\"1\" as=\"geometry\"><Array as=\"points\"><mxPoint x=\"840\" y=\"780\"/>")

# ================= 頁 2 =================
rep('p1b.append(v("tool", "1", SW(GREEN), "工具 repo（每個要出貨的工具一個）", 40, 190, 320, 260))',
    'p1b.append(v("tool", "1", SW(GREEN), "工具 repo（每個要出貨的工具一個）", 40, 210, 320, 260))')
rep('p1b.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 470, 320, 130))',
    'p1b.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 490, 320, 130))')
rep('p1b.append(v("tool2", "1", SW(GREEN), "另一個工具 repo（<name2>，同型）", 40, 620, 320, 60))',
    'p1b.append(v("tool2", "1", SW(GREEN), "另一個工具 repo（<name2>，同型）", 40, 640, 320, 60))')
rep('p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 260, 200, 40))',
    'p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 280, 200, 40))')
rep('p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 440, 200, 40))',
    'p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 460, 200, 40))')
rep('p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 550, 200, 40))',
    'p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 570, 200, 40))')
# 啟動器：說明字移到上方、justfile 右移讓 f7 標籤有空間、f8 標籤不壓框
rep('''p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器（進 git）", 20, 80, 260, 145))
p1b.append(v("p_ver", "pa", LEAF(), ".version", 12, 70, 100, 40))
p1b.append(v("pa_t", "pa", TEXT(11) + "align=left;", ".version 一行 = 一個工具 = 一個 .<name>/", 12, 116, 240, 24))
p1b.append(v("p_just", "pa", LEAF(), "justfile", 158, 70, 90, 40))
p1b.append(v("p_eng", "proj", PURPLE_LEAF, "安裝容器（<name>-dist:vX）", 20, 250, 260, 60))
p1b.append(v("p_eng_t", "proj", TEXT(11) + "align=left;", "以使用者身分執行，跑完即刪", 20, 312, 200, 20))''',
'''p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器（進 git）", 20, 80, 300, 125))
p1b.append(v("pa_t", "pa", TEXT(11) + "align=left;", ".version 一行 = 一個工具 = 一個 .<name>/", 12, 42, 276, 24))
p1b.append(v("p_ver", "pa", LEAF(), ".version", 12, 72, 90, 40))
p1b.append(v("p_just", "pa", LEAF(), "justfile", 200, 72, 80, 40))
p1b.append(v("p_eng", "proj", PURPLE_LEAF, "安裝容器（<name>-dist:vX）", 20, 270, 300, 60))
p1b.append(v("p_eng_t", "proj", TEXT(11) + "align=left;", "以使用者身分執行，跑完即刪", 20, 332, 200, 20))''')
rep('p1b.append(v("pc2", "proj", SW(NEUTRAL), ".<name2>/（另一個工具）", 540, 545, 220, 50))',
    'p1b.append(v("pc2", "proj", SW(NEUTRAL), ".<name2>/（另一個工具）", 540, 565, 220, 50))')
rep('p1b.append(e("f8", "p_just", "p_eng", "工具名、版本、使用者身分、專案路徑", (0.5, 1), (0.78, 0), vert=True))',
    'p1b.append(e("f8", "p_just", "p_eng", "工具名、版本、使用者身分、專案路徑", (0.5, 1), (0.8, 0), vert=True))')

# ================= 頁 3 =================
rep('p2.append(v("b_c0", "bB", PURPLE_LEAF, "install\\n換成 .version 指定的版本", 800, 65, 340, 60))',
    'p2.append(v("b_c0", "bB", PURPLE_LEAF, "install\\n換成 .version 指定的版本（image 沒有就先下載）", 800, 65, 340, 60))')
rep('p2.append(e("be3", "b_l2", "b_c0", "否則（image 沒有就先下載）", (1, 0.5), (0, 0.5)))',
    'p2.append(e("be3", "b_l2", "b_c0", "否則", (1, 0.5), (0, 0.5)))')
rep('p2.append(e("be4", "b_l2", "b_c1", "相同", (0.5, 1), (0, 0.5), vert=True))',
    'p2.append(e("be4", "b_l2", "b_c1", "相同", (0.5, 1), (0, 0.5), vert=True, pos=-0.7))')
# be6 / be7 交換高度：be6 走 y=270、be7 走 y=250，不再交叉；「通過」放垂直段
rep('<mxPoint x="1340" y="250"/><mxPoint x="638" y="250"/>', '<mxPoint x="1340" y="270"/><mxPoint x="638" y="270"/>')
rep('edge="1" parent="bB" source="b_c1" target="b_l3"><mxGeometry x="0.7" relative="1" as="geometry"><Array as="points"><mxPoint x="851" y="270"/><mxPoint x="550" y="270"/>',
    'edge="1" parent="bB" source="b_c1" target="b_l3"><mxGeometry x="-0.9" relative="1" as="geometry"><Array as="points"><mxPoint x="851" y="250"/><mxPoint x="550" y="250"/>')
# be8「失敗」移到垂直段（x=340）
rep('''<mxPoint x="340" y="224"/><mxPoint x="340" y="315"/></Array></mxGeometry></mxCell>'.replace('<mxGeometry relative="1" as="geometry">', '<mxGeometry x="-0.6" relative="1" as="geometry">'))''',
    '''<mxPoint x="340" y="224"/><mxPoint x="340" y="315"/></Array></mxGeometry></mxCell>'.replace('<mxGeometry relative="1" as="geometry">', '<mxGeometry x="0.6" relative="1" as="geometry">'))''')

# ================= 頁 5 =================
# init 泳道整體右移 20、加寬；回線走 x=15；「沒有了」從右側進成功結束
rep('p4.append(v("init", "1", SW(NEUTRAL), "init（第一次：建立使用者檔）", 440, 60, 460, 720))',
    'p4.append(v("init", "1", SW(NEUTRAL), "init（第一次：建立使用者檔）", 440, 60, 480, 720))')
for old, new in [
    ('"i0", "init", ELLIPSE(GREEN), "開始 init", 140,', '"i0", "init", ELLIPSE(GREEN), "開始 init", 160,'),
    ('"i1", "init", LEAF(), "讀 init.toml", 120,', '"i1", "init", LEAF(), "讀 init.toml", 140,'),
    ('"i2", "init", RHOMBUS, "還有項目？", 130,', '"i2", "init", RHOMBUS, "還有項目？", 150,'),
    ('（image 內由 src 指定的檔 → 專案內的 dest）", 100,', '（image 內由 src 指定的檔 → 專案內的 dest）", 120,'),
    ('"i4", "init", RHOMBUS, "dest 已存在？", 130,', '"i4", "init", RHOMBUS, "dest 已存在？", 150,'),
    ('"i5", "init", LEAF(), "略過（保留使用者版本）", 20,', '"i5", "init", LEAF(), "略過（保留使用者版本）", 40,'),
    ('"i6", "init", LEAF(), "從 dist/ 複製建立", 240,', '"i6", "init", LEAF(), "從 dist/ 複製建立", 260,'),
    ('"i8", "init", LEAF(), "繼續下一項", 120,', '"i8", "init", LEAF(), "繼續下一項", 140,'),
    ('"i7", "init", ELLIPSE(GREEN), "成功結束", 140,', '"i7", "init", ELLIPSE(GREEN), "成功結束", 160,'),
]:
    rep(old, new)
rep('''exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="init" source="i2" target="i7"><mxGeometry x="-0.85" relative="1" as="geometry"><Array as="points"><mxPoint x="440" y="240"/><mxPoint x="440" y="680"/><mxPoint x="300" y="680"/></Array>''',
    '''exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i2" target="i7"><mxGeometry x="-0.85" relative="1" as="geometry"><Array as="points"><mxPoint x="460" y="240"/><mxPoint x="460" y="680"/></Array>''')
rep('<mxPoint x="30" y="608"/><mxPoint x="30" y="240"/>', '<mxPoint x="15" y="608"/><mxPoint x="15" y="240"/>')
rep('p4.append(v("verify", "1", SW(NEUTRAL), "verify（檢查 install 的產物沒被改）", 940, 60, 440, 480))',
    'p4.append(v("verify", "1", SW(NEUTRAL), "verify（檢查 install 的產物沒被改）", 960, 60, 440, 480))')
rep('p4.append(v("diff", "1", SW(NEUTRAL), "diff（升級後：新模板 vs 使用者檔）", 1420, 60, 440, 480))',
    'p4.append(v("diff", "1", SW(NEUTRAL), "diff（升級後：新模板 vs 使用者檔）", 1440, 60, 440, 480))')

# ================= 頁 6 =================
rep('"= proto/tool/（原型裡 <name> 的實際值是 tool）"', '"= proto/tool/"')

# ================= 頁 7：整段重寫 =================
start = src.index("# ================= Page 7: repo 結構與測試分層 =================")
end = src.index("doc = ('<mxfile host=")
p8 = r'''# ================= Page 7: repo 結構與測試分層 =================
p8 = [v("title", "1", TITLE, "vendor_kit repo：資料夾結構 → Dockerfile stage → 每一層的強制閘門（右欄依層分組）", 40, 20, 1300, 30)]
COLH = 1010
# 欄 1：repo 目錄
p8.append(v("repo", "1", SW(RED), "vendor_kit repo", 40, 70, 420, COLH))
p8.append(v("d_src", "repo", SW(RED, 16), "src/vendor_kit/（第 1 頁的 7 個模組）", 20, 50, 380, 140))
MODS = [("cli", "命令介面"), ("dist_reader", "出貨內容讀取"), ("repo_fs", "專案檔案存取"), ("template", "模板"),
        ("stamp", "印記"), ("diff", "差異比對"), ("report", "回報")]
for i, (m, zh) in enumerate(MODS):
    p8.append(v(f"m_{m}", "d_src", LEAF().replace("fontSize=14", "fontSize=11"), f"{m}.py\n{zh}", 12 + (i % 4) * 92, 45 + (i // 4) * 46, 86, 40))
p8.append(v("d_test", "repo", SW(NEUTRAL), "test/（tool-first：test/<工具>/<層級>/）", 20, 200, 380, 596))
TW = 356
p8.append(v("t_lint", "d_test", LEAF(), "lint/{ruff, hadolint, import-linter}/\n寫法檢查＋架構契約", 12, 45, TW, 44))
p8.append(v("t_unit", "d_test", LEAF(), "pytest/unit/\ntest_<模組>.py ×7（一個模組一個檔）", 12, 100, TW, 44))
p8.append(v("t_inst", "d_test", LEAF(), "pytest/integration/test_install.py", 12, 155, TW, 44))
p8.append(v("t_init", "d_test", LEAF(), "pytest/integration/test_init.py", 12, 210, TW, 44))
p8.append(v("t_ver", "d_test", LEAF(), "pytest/integration/test_verify.py\n＋ test_perf_verify.py（時間預算）", 12, 265, TW, 44))
p8.append(v("t_diff", "d_test", LEAF(), "pytest/integration/test_diff.py", 12, 320, TW, 44))
p8.append(v("t_sys", "d_test", LEAF(), "pytest/system/\n整個 image：docker run 每個子命令", 12, 375, TW, 44))
p8.append(v("t_acc", "d_test", LEAF(), "pytest/acceptance/\n第 3 頁三條泳道：在假專案裡真的打 just", 12, 430, TW, 44))
p8.append(v("t_fix", "d_test", LEAF(), "fixtures/\n假的 dist/、init.toml、假專案（test-base 帶進去）", 12, 485, TW, 44))
p8.append(v("t_conf", "d_test", LEAF(), "pytest/<層級>/conftest.py\n每層的限制寫在這（見右欄）", 12, 540, TW, 44))
p8.append(v("d_df", "repo", LEAF(), "Dockerfile（中欄的 stage）", 20, 816, 180, 40))
p8.append(v("d_bake", "repo", LEAF(), "docker-bake.hcl（group）", 220, 816, 180, 40))
p8.append(v("d_adr", "repo", LEAF(), "doc/adr/\n測試分層與閘門（本頁的決策）", 20, 876, 380, 44))
p8.append(v("d_ci", "repo", LEAF(), ".github/workflows/\nbake validate → system/acceptance → bake release", 20, 932, 380, 44))
# 欄 2：Dockerfile stage（紫：每個 stage 都是 image）
SX, SW_ = 520, 480
LX, LW = 40, 230
p8.append(v("stages", "1", PURPLE_SW, "Dockerfile stage（BuildKit）", SX, 70, SW_, COLH))
p8.append(v("s_rt", "stages", PURPLE_LEAF, "runtime\nFROM toml-bridge + src/", LX, 60, LW, 50))
p8.append(v("s_tb", "stages", PURPLE_LEAF, "test-base\n= runtime + pytest + fixtures", LX, 160, LW, 50))
p8.append(v("s_lint", "stages", PURPLE_LEAF, "lint（FROM test-base）", LX, 247, LW, 40))
p8.append(v("s_unit", "stages", PURPLE_LEAF, "unit-test（FROM test-base）", LX, 302, LW, 40))
p8.append(v("s_inst", "stages", PURPLE_LEAF, "install-test（FROM test-base）", LX, 357, LW, 40))
p8.append(v("s_init", "stages", PURPLE_LEAF, "init-test（FROM test-base）", LX, 412, LW, 40))
p8.append(v("s_ver", "stages", PURPLE_LEAF, "verify-test（FROM test-base）", LX, 467, LW, 40))
p8.append(v("s_diff", "stages", PURPLE_LEAF, "diff-test（FROM test-base）", LX, 522, LW, 40))
p8.append(v("s_rel", "stages", PURPLE_LEAF, "release\n= runtime（最終產物）", LX, 600, LW, 50))
p8.append(v("s_smoke", "stages", PURPLE_LEAF, "smoke\nFROM release；真的跑一次 install", LX, 690, LW, 50))
p8.append(v("s_host", "stages", TEXT(11), "system / acceptance 不在 Dockerfile 裡：\n它們要 docker run，所以在 CI 主機上跑", 20, 780, 440, 40))
p8.append(v("s_bake", "stages", TEXT(11), "docker-bake.hcl：group validate = [lint, unit-test, install-test, init-test,\nverify-test, diff-test]；group release = [release, smoke]；CI 一次平行跑", 20, 830, 440, 40))
p8.append(e("s1", "s_rt", "s_tb", "FROM", (0.5, 1), (0.5, 0), vert=True))
p8.append(e("s2", "s_tb", "s_lint", "FROM（六個測試 stage 都是）", (0.5, 1), (0.5, 0), vert=True))
p8.append('<mxCell id="s8" value="FROM\n（不經任何 test stage）" style="' + EDGE + 'align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="stages" source="s_rt" target="s_rel"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="455" y="85"/><mxPoint x="455" y="625"/></Array></mxGeometry></mxCell>')
p8.append(e("s9", "s_rel", "s_smoke", "FROM", (0.5, 1), (0.5, 0), vert=True))
# 欄 1 → 欄 2 的 COPY（同高直線）
for a, b in [("t_lint", "s_lint"), ("t_unit", "s_unit"), ("t_inst", "s_inst"), ("t_init", "s_init"), ("t_ver", "s_ver"), ("t_diff", "s_diff")]:
    p8.append(e(f"c_{b}", a, b, "COPY", (1, 0.5), (0, 0.5)))
# 欄 3：強制閘門，依層分組
GX = SX + SW_ + 60
p8.append(v("gates", "1", SW(NEUTRAL), "強制閘門（不靠提醒；違反就 CI 紅，依層分組）", GX, 70, 460, COLH))
GSW = ("swimlane;html=1;rounded=1;startSize=30;fontStyle=1;fontSize=14;container=1;collapsible=0;recursiveResize=0;"
       f"fillColor={NEUTRAL};swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=2;")
def gate_group(gid, title, y, gates):
    h = 30 + len(gates) * 60 + 10
    p8.append(v(gid, "gates", GSW, title, 20, y, 420, h))
    for i, (k, t) in enumerate(gates):
        p8.append(v(k, gid, LEAF().replace("fontSize=14", "fontSize=12"), t, 10, 40 + i * 60, 400, 50))
    return y + h + 10
y = 50
y = gate_group("gl", "lint 層（lint stage）", y, [
    ("g_ruff", "ruff / hadolint\n程式碼與 Dockerfile 的寫法檢查"),
    ("g2", "import-linter 契約\n模組只能沿第 1 頁的線 import；只有 repo_fs、dist_reader 能碰檔案"),
    ("g3", "鏡射檢查\n每個 src 模組必有 test_<模組>.py，缺一個就失敗")])
y = gate_group("gu", "unit 層（unit-test stage）", y, [
    ("g4", "unit conftest\n測試中一碰檔案、網路、Docker 就直接失敗")])
y = gate_group("gi", "integration 層（install / init / verify / diff-test stage）", y, [
    ("g5", "integration conftest\n只給臨時目錄；禁 Docker、網路；只能走 cli.main()（程式的正門）"),
    ("g6", "一個子命令一個 stage\n各自只 COPY 自己的測試檔；哪個 stage 紅 = 第 5 頁哪條泳道壞"),
    ("g7", "時間預算\nverify 在假專案上超過預算即失敗（每次 just 都會跑它）")])
y = gate_group("gs", "system / acceptance 層（CI 主機）", y, [
    ("g8", "只能碰公開介面\n只准 docker run 與檔案系統，不准 import vendor_kit")])
y = gate_group("gr", "release（release / smoke stage）", y, [
    ("g1", "BuildKit stage 依賴\nrelease 只 FROM runtime → 測試碼、pytest 進不了產品 image"),
    ("g9", "release 必過 smoke\nrelease image 真的 install 一次，失敗就不 push")])
p8.append(v("g_map", "gates", TEXT(11) + "align=left;", "對應：unit ↔ 第 1 頁模組；integration ↔ 第 5 頁泳道；acceptance ↔ 第 3 頁泳道。\n層級名稱依 ISTQB：unit / integration / system / acceptance；smoke 是測試類型，不是層級", 20, y, 420, 50))
p8 += legend("p8", 40, 70 + COLH + 40, ["red", "pimg", "neutral", "white"], "實線 = 依賴／複製方向")
p8 += terms("p8", 40, 70 + COLH + 150, [
 ("stage", "Dockerfile 裡的一個階段（FROM … AS 名稱）；docker build --target <名稱> 只做到那一階"),
 ("FROM / COPY", "Dockerfile 的兩個指令：FROM = 以哪個 stage／image 為底；COPY = 把 repo 裡的檔案放進 stage"),
 ("BuildKit", "Docker 的建置引擎：只會建最終目標依賴到的 stage，沒被依賴的測試 stage 不會執行、也不會進 image"),
 ("bake", "docker buildx bake：用一個檔定義多個 stage 目標與群組，CI 一次平行跑"),
 ("runtime / release / smoke", "runtime = 能執行 vendor_kit 的最小 image；release = 最終出貨的 image；smoke = 出貨前最小的一次實跑"),
 ("toml-bridge", "vendor_kit image 的基底 image（另一個 repo 提供，內含 Python 與 TOML 工具）"),
 ("pytest / conftest.py", "Python 的測試框架／每個測試目錄的共用設定；這裡用它對該層測試強制限制"),
 ("ruff / hadolint / import-linter", "Python 寫法檢查／Dockerfile 寫法檢查／檢查模組之間誰可以 import 誰（契約寫在設定檔）"),
 ("鏡射", "test/ 的檔名跟 src/ 一一對應：src 有 cli.py，test 就必須有 test_cli.py"),
 ("fixture / 假專案", "測試用的假資料：假的 dist/、init.toml，以及一個只有 .version 與 justfile 的假專案"),
 ("cli.main()", "vendor_kit 程式的正門（命令介面的進入點）；integration 測試只准從這裡進"),
 ("docker run / CI", "把 image 跑成容器的指令／GitHub 上的自動化流程（每次推送都跑 bake validate）"),
 ("ADR / ISTQB", "設計決策紀錄（doc/adr/ 裡一個決策一個檔）／國際軟體測試標準，本頁的層級名稱來自它"),
 ("泳道", "流程圖裡的一條直欄，代表一個子命令或情境的完整流程"),
])

'''
src = src[:start] + p8 + src[end:]
open("gen19.py", "w").write(src)
print("ok")
