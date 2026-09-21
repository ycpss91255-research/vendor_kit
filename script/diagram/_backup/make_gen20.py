src = open("gen19.py").read()

def rep(old, new, count=1):
    global src
    assert src.count(old) == count, (src.count(old), old[:90])
    src = src.replace(old, new)

# ---- legend_flow：實線也可指向檔案 ----
rep('''    txt = "實線 = 執行順序" + ("\\n虛線 = 之後才會發生" if dashed else "")''',
    '''    txt = "實線 = 執行順序（指向檔案時 = 寫入／讀取）" + ("\\n虛線 = 之後才會發生" if dashed else "")''')
rep('''    c.append(v(f"{prefix}_lgt", "1", TEXT(12) + "align=left;", txt, cx, y, 200, 60))
    return c

# ================= Page 1''', '''    c.append(v(f"{prefix}_lgt", "1", TEXT(12) + "align=left;", txt, cx, y, 300, 60))
    return c

# ================= Page 1''')
rep(''' "pimg":   (PURPLE_LEAF,        "紫：image / container", 180, 40, 10),''',
    ''' "pimg":   (PURPLE_LEAF,        "紫：image / container", 180, 40, 10),
 "pstage": (PURPLE_LEAF,        "紫：image（每個 stage 都是一個 image）", 270, 40, 10),''')

# ================= 頁 1 =================
rep('p1.append(v("p_stamp", "proj", LEAF(), ".stamp\\n（印記檔）", 56, 250, 88, 40))',
    'p1.append(v("p_stamp", "proj", LEAF(), ".<name>/\\n.stamp", 56, 250, 88, 40))')
rep('p1.append(v("tp_render", "m_tpl", LEAF(), "渲染", 12, 45, 88, 40))',
    'p1.append(v("tp_render", "m_tpl", LEAF(), "複製", 12, 45, 88, 40))')
rep('p1.append(v("tp_vars", "m_tpl", LEAF(), "帶入變數\\n（待定）", 104, 45, 88, 40))',
    'p1.append(v("tp_vars", "m_tpl", LEAF(), "渲染／帶入\\n變數（待定）", 104, 45, 88, 40))')
rep('p1.append(e("a9", "m_write", "m_stamp", "檔案內容、舊印記", (0.67, 1), (0.4, 0), vert="left"))',
    'p1.append(e("a9", "m_write", "m_stamp", "檔案內容、\\n舊印記", (0.55, 1), (0.1818, 0), vert=True))')
rep('p1.append(e("a9b", "m_stamp", "m_write", "新指紋、比對結果", (0.8, 0), (0.89, 1), vert=True))',
    'p1.append(e("a9b", "m_stamp", "m_write", "新指紋、比對結果", (0.9, 0), (0.945, 1), vert=True))')
rep(''' ("模板", "工具 dist/ 裡給初始檔用的樣板（例如 Dockerfile 範本）；渲染 = 帶入變數（專案名等）產生實際檔案"),
])''', ''' ("模板", "工具 dist/ 裡給初始檔用的樣板（例如 Dockerfile 範本）；目前只複製；渲染 = 帶入變數（專案名等）產生實際檔案，待定"),
 ("repo", "一個 git 管理的專案資料夾；工具 repo = 工具的原始碼，專案 repo = 使用工具的專案"),
 (".version", "專案 repo 裡的版本清單（TOML）：一個工具一行，記工具名與 image 版本"),
 ("啟動器", "專案 repo 裡的 justfile：使用者打 just 指令時，它起 vendor_kit 容器並把結果告訴使用者"),
 ("Dockerfile", "打包 image 的食譜；專案自己的 Dockerfile 是由模板建立的使用者檔案"),
 ("upgrade（升級）", "改 .version 換新版本：由機器人開 PR 或 just upgrade；下次 just 時 dist/ 整包換新"),
])''')

# ================= 頁 2 =================
rep('p1b.append(v("t_ci", "tool", LEAF(), "CI：打 tag →\\nbuild + push", 165, 145, 135, 50))',
    'p1b.append(v("t_ci", "tool", LEAF(), "CI：打 tag →\\n建置＋上傳 image", 165, 145, 135, 50))')
rep('p1b.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 420, 80, 260, 620))',
    'p1b.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 420, 80, 260, 640))')
rep('p1b.append(v("proj", "1", SW(GREEN), "專案 repo（使用工具的專案）", 740, 80, 770, 620))',
    'p1b.append(v("proj", "1", SW(GREEN), "專案 repo（使用工具的專案）", 740, 80, 770, 640))')
rep('p1b.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1600, 80, 160, 620))',
    'p1b.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1600, 80, 160, 640))')
rep('p1b.append(v("pc2", "proj", SW(NEUTRAL), ".<name2>/（另一個工具）", 540, 565, 220, 50))',
    'p1b.append(v("pc2", "proj", SW(NEUTRAL, 14), ".<name2>/（另一個工具）", 540, 565, 220, 50))')
rep(''' ("CI", "放在 GitHub 上的自動化流程：打 tag 時 build image 並上傳 GHCR"),''',
    ''' ("CI", "放在 GitHub 上的自動化流程：打 tag 時建置 image 並上傳 GHCR"),
 ("建置 / 上傳", "建置 = 照 Dockerfile 做出 image（docker build）；上傳 = 把 image 放到 GHCR（docker push）"),
 ("upgrade（升級）", "改 .version 換新版本：由機器人開 PR 或 just upgrade；下次 just 時 .<name>/ 整批換新"),''')
rep(''' ("tag / digest", "image 的版本名稱（v0.43.0）／內容指紋（sha256:…，鎖多架構 index）；.version 兩者都記，工具只認 digest"),''',
    ''' ("tag / digest", "image 的版本名稱（v0.43.0）／內容指紋（sha256:…）；.version 兩者都記，工具只認 digest"),''')

# ================= 頁 3 =================
rep('band("bB", "日常：just build（run / exec / stop 同）", 410, 390)',
    'band("bB", "日常：just build（建置）；run（啟動）／exec（進入）／stop（停止）流程相同", 410, 390)')
rep('p2.append(v("b_l3", "bB", LEAF(), "執行 .<name>/ 內的 build 腳本", 380, 290, 340, 50))',
    'p2.append(v("b_l3", "bB", LEAF(), "執行 .<name>/ 內的 build（建置）腳本", 380, 290, 340, 50))')
rep('p2.append(v("b_c0", "bB", PURPLE_LEAF, "install\\n換成 .version 指定的版本（image 沒有就先下載）", 800, 65, 340, 60))',
    '''p2.append(v("b_c0", "bB", PURPLE_LEAF, "install\\n換成 .version 指定的版本", 800, 65, 340, 60))
p2.append(v("b_l1n", "bB", TEXT(11), "（image 不在本機時，Docker 會先下載）", 360, 118, 180, 30))''')
rep('''<mxPoint x="340" y="224"/><mxPoint x="340" y="315"/></Array></mxGeometry></mxCell>'.replace('<mxGeometry relative="1" as="geometry">', '<mxGeometry x="0.6" relative="1" as="geometry">'))''',
    '''<mxPoint x="340" y="224"/><mxPoint x="340" y="315"/></Array></mxGeometry></mxCell>'.replace('<mxGeometry relative="1" as="geometry">', '<mxGeometry x="0.7" relative="1" as="geometry">').replace(EDGE + 'exitX=0;exitY=0.9', EDGE + 'align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;exitX=0;exitY=0.9'))''')
rep(''' ("docker compose", "工具腳本最後真正拿來 build／啟動／進入／停止專案容器的指令"),''',
    ''' ("docker compose", "工具腳本最後真正拿來建置／啟動／進入／停止專案容器的指令"),
 ("build / run / exec / stop", "四個日常指令：建置 image／啟動容器／進入容器／停止容器；都先經過同樣的檢查再執行 .<name>/ 內的腳本"),''')

# ================= 頁 4 =================
rep('p3.append(v("c8", "up", RHOMBUS, "執行 diff：init.toml 列的檔案\\n新版模板有差異？", 70, 240, 280, 100))',
    'p3.append(v("c8", "up", RHOMBUS, "執行 diff：init.toml 列的檔案\\n新版模板 vs 你的檔案有差異？", 70, 240, 280, 100))')
rep(''' ("工具 repo / GHCR / image", "工具的原始碼 repo／GitHub 的 image 倉庫／打包好可執行的檔案包"),
])''', ''' ("工具 repo / GHCR / image", "工具的原始碼 repo／GitHub 的 image 倉庫／打包好可執行的檔案包"),
 ("<name> / just", "<name> = .version 裡的工具名，安裝目錄就叫 .<name>/；just = 主機上的指令跑器，使用者打 just <指令>"),
])''')

# ================= 頁 5 =================
rep('''p4 += legend_flow("p4", 40, 900, purple=False, note=True)''',
    '''p4.append(v("p4n", "1", NOTE, "仍待決（notes §8 #11–13）：verify 的驗證基準（印記 vs 從 image 重取）、diff 是否三方比對、並行安裝的 lock。", 960, 560, 920, 40))
p4 += legend_flow("p4", 40, 900, purple=False, note=True)''')

# ================= 頁 6 =================
rep('p7.append(v("row_g", "1", TEXT(12) + "align=left;", "產物（不進 git，CI 產生）", 640, 70, 300, 20))',
    'p7.append(v("row_g", "1", TEXT(12) + "align=left;", "產物（不進 git；原型在本機建置，正式版由 CI 建置＋上傳）", 640, 70, 420, 20))')
rep('"這個 repo 不知道 vendor_kit 存在，\\n只認 .version 裡的 <name>-dist image"',
    '"專案只在 .version 指定工具的 image，\\n不必另外指定 vendor_kit"')
rep('p7.append(e("x1", "f_vkdf", "g_vk", "image（build 後 push）", (1, 0.5), (0, 0.5), offset=(0, -4)))',
    'p7.append(e("x1", "f_vkdf", "g_vk", "建置成 image", (1, 0.5), (0, 0.5), offset=(0, -4)))')
rep('p7.append(e("x2", "f_tdf", "g_tool", "image（build 後 push）", (1, 0.5), (0, 0.5), offset=(0, -4)))',
    'p7.append(e("x2", "f_tdf", "g_tool", "建置成 image", (1, 0.5), (0, 0.5), offset=(0, -4)))')
rep(''' ("<name>", "工具名；原型裡的實際值是 tool，所以 image 叫 tool-dist、安裝目錄叫 .tool/"),''',
    ''' ("<name>", "工具名的占位符。原型不是真實工具，直接用 tool 當占位值：image 叫 tool-dist、目錄叫 .tool/"),''')
rep(''' ("build / push / 指紋 / TOML", "把食譜做成 image／上傳 image 到倉庫／由檔案內容算出的識別碼／設定檔格式"),''',
    ''' ("建置 / 上傳 / 指紋 / TOML", "把食譜做成 image（docker build）／把 image 放到倉庫（docker push）／由檔案內容算出的識別碼／設定檔格式"),''')

# ================= 頁 7 =================
rep('p8.append(v("d_test", "repo", SW(NEUTRAL), "test/（tool-first：test/<工具>/<層級>/）", 20, 200, 380, 596))',
    'p8.append(v("d_test", "repo", SW(NEUTRAL), "test/（先分測試工具、再分層級）", 20, 200, 380, 596))')
rep('p8.append(v("t_lint", "d_test", LEAF(), "lint/{ruff, hadolint, import-linter}/\\n寫法檢查＋架構契約", 12, 45, TW, 44))',
    'p8.append(v("t_lint", "d_test", LEAF(), "lint/{ruff, import-linter}/ + mirror_check.py + blackbox_check.py\\n寫法、架構契約、鏡射、黑箱", 12, 45, TW, 44).replace("fontSize=14", "fontSize=12"))')
rep('p8.append(v("t_fix", "d_test", LEAF(), "fixtures/\\n假的 dist/、init.toml、假專案（test-base 帶進去）", 12, 485, TW, 44))',
    'p8.append(v("t_fix", "d_test", LEAF(), "fixtures/\\n假的 dist/、init.toml、VERSION、假專案", 12, 485, TW, 44))')
# stage 欄：runtime / test-base 上移，六個測試 stage 收進一個分組
rep('p8.append(v("s_rt", "stages", PURPLE_LEAF, "runtime\\nFROM toml-bridge + src/", LX, 60, LW, 50))',
    'p8.append(v("s_rt", "stages", PURPLE_LEAF, "runtime\\nFROM toml-bridge + src/", LX, 50, LW, 50))')
rep('p8.append(v("s_tb", "stages", PURPLE_LEAF, "test-base\\n= runtime + pytest + fixtures", LX, 160, LW, 50))',
    '''p8.append(v("s_tb", "stages", PURPLE_LEAF, "test-base\\n= runtime + pytest + fixtures", LX, 130, LW, 50))
GRP = ("swimlane;html=1;rounded=1;startSize=30;fontStyle=1;fontSize=14;container=1;collapsible=0;recursiveResize=0;"
       f"fillColor={NEUTRAL};swimlaneFillColor=#ffffff;strokeColor=#000000;strokeWidth=2;")
GY = 205
p8.append(v("s_grp", "stages", GRP, "六個測試 stage（都 FROM test-base）", 20, GY, 440, 372))
LX = LX - 20''')
for sid, y in [("s_lint", 247), ("s_unit", 302), ("s_inst", 357), ("s_init", 412), ("s_ver", 467), ("s_diff", 522)]:
    rep(f'p8.append(v("{sid}", "stages", PURPLE_LEAF, ', f'p8.append(v("{sid}", "s_grp", PURPLE_LEAF, ')
    rep(f'（FROM test-base）", LX, {y}, LW, 40))', f'", LX, {y - 205}, LW, 40))')
rep('p8.append(v("s_smoke", "stages", PURPLE_LEAF, "smoke\\nFROM release；真的跑一次 install", LX, 690, LW, 50))',
    'p8.append(v("s_smoke", "stages", PURPLE_LEAF, "smoke\\nFROM release；真的跑一次 install + verify", LX + 20, 690, LW, 50))')
rep('p8.append(v("s_rel", "stages", PURPLE_LEAF, "release\\n= runtime（最終產物）", LX, 600, LW, 50))',
    'p8.append(v("s_rel", "stages", PURPLE_LEAF, "release\\n= runtime（最終產物）", LX + 20, 600, LW, 50))')
rep('p8.append(e("s2", "s_tb", "s_lint", "FROM（六個測試 stage 都是）", (0.5, 1), (0.5, 0), vert=True))',
    'p8.append(e("s2", "s_tb", "s_grp", "FROM", (0.5, 1), (0.3068, 0), vert=True))')
rep('<mxPoint x="455" y="85"/><mxPoint x="455" y="625"/>', '<mxPoint x="475" y="75"/><mxPoint x="475" y="625"/>')
rep('''style="' + EDGE + 'align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="stages" source="s_rt" target="s_rel"><mxGeometry relative="1" as="geometry">''',
    '''style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="stages" source="s_rt" target="s_rel"><mxGeometry x="0.785" relative="1" as="geometry">''')
rep('p8.append(v("stages", "1", PURPLE_SW, "Dockerfile stage（BuildKit）", SX, 70, SW_, COLH))',
    'p8.append(v("stages", "1", PURPLE_SW, "Dockerfile stage（BuildKit）", SX, 70, SW_ + 20, COLH))')
rep('GX = SX + SW_ + 60', 'GX = SX + SW_ + 80')
# 閘門：層的中文定義、強制者
rep('y = gate_group("gl", "lint 層（lint stage）", y, [\n    ("g_ruff", "ruff / hadolint\\n程式碼與 Dockerfile 的寫法檢查"),',
    'y = gate_group("gl", "lint 層 = 不執行程式的檢查（lint stage）", y, [\n    ("g_ruff", "ruff\\n程式碼寫法檢查"),')
rep('("g2", "import-linter 契約\\n模組只能沿第 1 頁的線 import；只有 repo_fs、dist_reader 能碰檔案"),',
    '("g2", "import-linter 分層契約\\n只能由上層 import 下層（命令介面 → 讀取／存取 → 純函式）；只有 repo_fs、dist_reader 能碰檔案"),')
rep('y = gate_group("gu", "unit 層（unit-test stage）", y, [', 'y = gate_group("gu", "unit 層 = 一次測一個模組（unit-test stage）", y, [')
rep('y = gate_group("gi", "integration 層（install / init / verify / diff-test stage）", y, [',
    'y = gate_group("gi", "integration 層 = 一個子命令走到底（四個 *-test stage）", y, [')
rep('("g7", "時間預算\\nverify 在假專案上超過預算即失敗（每次 just 都會跑它）")])',
    '("g7", "時間預算\\nverify 200 個檔必須 < 0.5 秒（每次 just 都會跑它）")])')
rep('''y = gate_group("gs", "system / acceptance 層（CI 主機）", y, [
    ("g8", "只能碰公開介面\\n只准 docker run 與檔案系統，不准 import vendor_kit")])''',
    '''y = gate_group("gs", "system = 整個 image；acceptance = 真的打 just（CI 主機）", y, [
    ("g8", "黑箱檢查（lint stage）＋ conftest\\n測試檔不准 import vendor_kit；只准 docker run／just 與檔案系統")])''')
rep('y = gate_group("gr", "release（release / smoke stage）", y, [', 'y = gate_group("gr", "release = 出貨（release / smoke stage）", y, [')
rep('("g9", "release 必過 smoke\\nrelease image 真的 install 一次，失敗就不 push")])',
    '("g9", "release 必過 smoke\\nrelease image 真的 install + verify 一次，失敗就不上傳")])')
rep('p8 += legend("p8", 40, 70 + COLH + 40, ["red", "pimg", "neutral", "white"], "實線 = 依賴／複製方向")',
    'p8 += legend("p8", 40, 70 + COLH + 40, ["red", "pstage", "neutral", "white"], "實線 = 依賴／複製方向")')

open("gen20.py", "w").write(src)
print("ok")
