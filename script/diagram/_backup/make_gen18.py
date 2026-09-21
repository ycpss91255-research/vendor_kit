s = open("gen17.py", encoding="utf-8").read()
R = {
 # ===== 頁 1：雙向箭頭拆線 =====
 'p1.append(e("a9", "m_write", "m_stamp", "↓ 檔案內容、舊印記\\n↑ 新指紋、比對結果", (0.8, 1), (0.64, 0), both=True, vert="left"))':
 'p1.append(e("a9", "m_write", "m_stamp", "檔案內容、舊印記", (0.67, 1), (0.4, 0), vert="left"))\np1.append(e("a9b", "m_stamp", "m_write", "新指紋、比對結果", (0.8, 0), (0.89, 1), vert=True))',
 'p1.append(e("a12", "m_write", "p_user", "初始檔／現有內容", (1, 0.9), (0, 0.5), both=True))':
 'p1.append(e("a12", "m_write", "p_user", "初始檔（init 時）", (1, 0.85), (0, 0.3)))\np1.append(e("a12b", "p_user", "m_write", "現有內容（diff 時）", (0, 0.7), (1, 0.95)))',
 # ===== 頁 3 =====
 'band("bC", "升級：Renovate 開的 PR 被 merge", 730, 300)': 'band("bC", "升級：Renovate 開的 PR 被 merge", 830, 300)',
 '("專案目錄（安裝目錄 .<name>/）", 1240, 380)]': '("專案目錄", 1240, 380)]',
 'p2.append(v("b_l3", "bB", LEAF(), "執行 .<name>/ 內的 build 腳本", 380, 260, 340, 50))': 'p2.append(v("b_l3", "bB", LEAF(), "執行 .<name>/ 內的 build 腳本", 380, 290, 340, 50))',
 'p2.append(v("b_p1", "bB", LEAF(), "docker compose build", 1240, 265, 200, 40))': 'p2.append(v("b_p1", "bB", LEAF(), "docker compose build", 1240, 295, 200, 40))',
 'p2.append(v("b_err", "bB", ELLIPSE(RED), "中止：.<name>/ 被改過\\n刪除 .<name>/ 再 build 即自動重裝", 40, 255, 260, 60))': 'p2.append(v("b_err", "bB", ELLIPSE(RED), "中止：.<name>/ 被改過\\n刪除 .<name>/ 再 build 即自動重裝", 40, 285, 260, 60))',
 'p2.append(e("be3", "b_l2", "b_c0", "否則", (1, 0.5), (0, 0.5), pos=-0.4))': 'p2.append(e("be3", "b_l2", "b_c0", "否則（image 沒有就先下載）", (1, 0.5), (0, 0.5)))',
 'p2.append(e("be4", "b_l2", "b_c1", "相同", (0.5, 1), (0.5, 0)))': 'p2.append(e("be4", "b_l2", "b_c1", "相同", (0.5, 1), (0, 0.5), vert=True))',
 '<Array as="points"><mxPoint x="1340" y="245"/><mxPoint x="638" y="245"/></Array></mxGeometry></mxCell>\'.replace(\'<mxGeometry relative="1" as="geometry">\', \'<mxGeometry x="-0.8" relative="1" as="geometry">\'))': '<Array as="points"><mxPoint x="1340" y="250"/><mxPoint x="638" y="250"/></Array></mxGeometry></mxCell>\'.replace(\'<mxGeometry relative="1" as="geometry">\', \'<mxGeometry x="-0.8" relative="1" as="geometry">\'))',
 'p2.append(e("be7", "b_c1", "b_l3", "通過", (0, 0.85), (0.5, 0), vert=True, pos=0.8))': 'p2.append(\'<mxCell id="be7" value="通過" style="\' + EDGE + \'align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;exitX=0.15;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="bB" source="b_c1" target="b_l3"><mxGeometry x="0.7" relative="1" as="geometry"><Array as="points"><mxPoint x="851" y="270"/><mxPoint x="550" y="270"/></Array></mxGeometry></mxCell>\')',
 '<mxCell id="be8" value="失敗" style="\' + EDGE + \'exitX=0;exitY=0.25;': '<mxCell id="be8" value="失敗" style="\' + EDGE + \'exitX=0;exitY=0.9;',
 '<Array as="points"><mxPoint x="340" y="185"/><mxPoint x="340" y="285"/></Array></mxGeometry></mxCell>\'.replace(\'<mxGeometry relative="1" as="geometry">\', \'<mxGeometry x="-0.6" relative="1" as="geometry">\'))': '<Array as="points"><mxPoint x="340" y="224"/><mxPoint x="340" y="315"/></Array></mxGeometry></mxCell>\'.replace(\'<mxGeometry relative="1" as="geometry">\', \'<mxGeometry x="-0.6" relative="1" as="geometry">\'))',
 'p2.append(e("be9", "b_l3", "b_p1", "", (1, 0.5), (0, 0.5)))': 'p2.append(e("be9", "b_l3", "b_p1", "", (1, 0.5), (0, 0.5)))',
 'p2.append(v("c_l1", "bC", LEAF(), "下次 just build 走上面\\n「不同」分支 → install 新版", 380, 65, 340, 50))': 'p2.append(v("c_l1", "bC", LEAF(), "下次 just build 走上面\\n「否則」分支 → install 新版", 380, 65, 340, 50))',
 '"紫框 = 子命令：install（第一次、版本改變時）、init（只有第一次）、verify（每次日常）、diff（升級後由使用者呼叫）。\\n沒有 Renovate 時用 just upgrade 手動：改 .version → 立即 install → diff（細節待議）。"': '"紫框 = 子命令：install（第一次、版本改變時）、init（只有第一次）、verify（已安裝且版本一致時）、diff（升級後由使用者呼叫）。\\n沒有 Renovate 時用 just upgrade 手動：改 .version → 立即 install → diff（細節待議）。"',
 ' ("entrypoint / hooks", "初始檔的例子：容器啟動腳本／各指令前後可掛的自訂腳本"),\n])': ' ("entrypoint / hooks", "初始檔的例子：容器啟動腳本／各指令前後可掛的自訂腳本"),\n ("<name> / 指紋", "<name> = .version 裡的工具名，安裝目錄就叫 .<name>/；指紋 = 由檔案內容算出的識別碼，內容一改就不同"),\n ("vendor_kit / Dockerfile / TOML", "安裝工具本身（在容器內跑）／打包 image 的食譜、也是專案自己的 image 食譜／設定檔格式"),\n ("just upgrade", "手動升級指令：改 .version → 立即 install → diff（細節待議）"),\n])',
 # ===== 頁 5：回線改經合流框 =====
 'p4.append(v("i7", "init", ELLIPSE(GREEN), "成功結束", 140, 640, 160, 40))': 'p4.append(v("i8", "init", LEAF(), "繼續下一項", 120, 590, 200, 36))\np4.append(v("i7", "init", ELLIPSE(GREEN), "成功結束", 140, 660, 160, 40))',
 'p4.append(\'<mxCell id="ib1" value="" style="\' + EDGE + \'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i5" target="i2"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="110" y="580"/><mxPoint x="10" y="580"/><mxPoint x="10" y="240"/></Array></mxGeometry></mxCell>\')': 'p4.append(e("ib1", "i5", "i8", "", (0.5, 1), (0.25, 0)))',
 'p4.append(\'<mxCell id="ib2" value="" style="\' + EDGE + \'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i6" target="i2"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="330" y="580"/><mxPoint x="10" y="580"/><mxPoint x="10" y="240"/></Array></mxGeometry></mxCell>\')': 'p4.append(e("ib2", "i6", "i8", "", (0.5, 1), (0.75, 0)))\np4.append(\'<mxCell id="ib3" value="" style="\' + EDGE + \'exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i8" target="i2"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="30" y="608"/><mxPoint x="30" y="240"/></Array></mxGeometry></mxCell>\')',
 '<mxPoint x="440" y="240"/><mxPoint x="440" y="610"/><mxPoint x="220" y="610"/>': '<mxPoint x="440" y="240"/><mxPoint x="440" y="680"/><mxPoint x="300" y="680"/>',
 'p4.append(v("i3", "init", LEAF(), "取下一項\\n（image 的 dist/src → 專案的 dest）", 100, 315, 240, 50))': 'p4.append(v("i3", "init", LEAF(), "取下一項\\n（image 內由 src 指定的檔 → 專案內的 dest）", 100, 315, 240, 50))',
 ' ("src → dest", "init.toml 每一項：src 是 image 內 dist/ 的相對路徑，dest 是專案內的相對路徑"),': ' ("src → dest", "init.toml 每一項：src 指 image 的 dist/ 裡哪個檔，dest 指要放到專案的哪裡"),',
 ' ("init.toml / 啟動器", "init 要建立哪些檔的清單／專案裡的 justfile"),\n])': ' ("init.toml / 啟動器", "init 要建立哪些檔的清單／專案裡的 justfile（使用者打 just 時執行的指令清單）"),\n ("容器 / <name>", "容器 = image 執行起來的實例；<name> = .version 裡的工具名，安裝目錄就叫 .<name>/"),\n])',
 # ===== 頁 6 =====
 'p7 = [v("title", "1", TITLE, "原型對照：proto/ 三個資料夾 ↔ 框架裡的三種角色（原型的範例工具名是 tool，正式版對應 <name>）", 40, 20, 1300, 30)]': 'p7 = [v("title", "1", TITLE, "原型對照：proto/ 三個資料夾 ↔ 框架裡的三種角色", 40, 20, 900, 30)]',
 'p7.append(v("r_tool_t", "r_tool", TEXT(11), "= proto/tool/（工具名 tool）", 10, 40, 280, 18))': 'p7.append(v("r_tool_t", "r_tool", TEXT(11), "= proto/tool/（原型裡 <name> 的實際值是 tool）", 10, 40, 280, 18))',
 'p7.append(v("ghcr", "1", SW(YELLOW), "image（原型：本機；正式版：GHCR）", 640, 100, 300, 490))': 'p7.append(v("ghcr", "1", SW(YELLOW), "image 存放處", 640, 100, 300, 490))',
 'p7.append(v("g_tool", "ghcr", PURPLE_LEAF, "tool-dist:v0.1.0", 40, 370, 220, 50))': 'p7.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:v0.1.0", 40, 370, 220, 50))',
 'p7.append(v("g_n", "ghcr", TEXT(11), "原型只 build 到本機；正式版由 CI 在打 tag 時 push 到 GHCR", 10, 450, 280, 40))': 'p7.append(v("g_n", "ghcr", TEXT(11), "原型：本機 Docker 快取；正式版：CI 在打 tag 時 push 到 GHCR", 10, 450, 280, 40))',
 'p7.append(v("f_land", "r_proj", LEAF(), ".tool/（含 .stamp 印記檔）\\n（不進 git，install 寫出）", 20, 370, 300, 50))': 'p7.append(v("f_land", "r_proj", LEAF(), ".<name>/（含 .stamp 印記檔）\\n（不進 git，install 寫出）", 20, 370, 300, 50))',
 'p7.append(v("r_proj_n", "r_proj", TEXT(11), "這個 repo 不知道 vendor_kit 存在，\\n只認 .version 裡的 tool-dist image", 10, 450, 320, 36))': 'p7.append(v("r_proj_n", "r_proj", TEXT(11), "這個 repo 不知道 vendor_kit 存在，\\n只認 .version 裡的 <name>-dist image", 10, 450, 320, 36))',
 ' ("tool", "原型裡那個範例工具的名字；所以它的 image 叫 tool-dist、安裝目錄叫 .tool/"),': ' ("<name>", "工具名；原型裡的實際值是 tool，所以 image 叫 tool-dist、安裝目錄叫 .tool/"),',
 ' (".version / justfile / init.toml", "專案記工具版本的檔／專案的指令入口（啟動器）／工具給的初始檔清單"),\n])': ' (".version / justfile / init.toml", "專案記工具版本的檔／專案的指令入口（啟動器）／工具給的初始檔清單"),\n ("Dockerfile / Dockerfile.dist / FROM", "打包 image 的食譜／工具 repo 出貨用的食譜／食譜第一行，指定以哪個 image 為底"),\n ("dist / 模板 / tag", "工具要出貨的檔案／dist 裡給初始檔用的樣板／image 的版本名稱"),\n ("build / push / 指紋 / TOML", "把食譜做成 image／上傳 image 到倉庫／由檔案內容算出的識別碼／設定檔格式"),\n])',
}
for k, val in R.items():
    assert s.count(k) == 1, (k[:80], s.count(k))
    s = s.replace(k, val)

# ===== 新增頁 7：repo 結構、測試分層、閘門 =====
p8 = r'''
# ================= Page 7: repo 結構與測試分層 =================
p8 = [v("title", "1", TITLE, "vendor_kit repo：資料夾結構 → 測試分層 → Dockerfile stage，每一層一個強制閘門", 40, 20, 1300, 30)]
# 欄 1：repo 目錄
p8.append(v("repo", "1", SW(RED), "vendor_kit repo", 40, 70, 420, 900))
p8.append(v("d_src", "repo", SW(RED), "src/vendor_kit/（產品，= 第 1 頁的 7 個模組）", 20, 50, 380, 130))
for i, m in enumerate(["cli", "dist_reader", "repo_fs", "template", "stamp", "diff", "report"]):
    p8.append(v(f"m_{m}", "d_src", LEAF(), m + ".py", 12 + (i % 4) * 92, 45 + (i // 4) * 40, 86, 32))
p8.append(v("d_test", "repo", SW(NEUTRAL), "test/（tool-first：test/<工具>/<層級>/）", 20, 200, 380, 500))
p8.append(v("t_unit", "d_test", LEAF(), "pytest/unit/\ntest_<模組>.py ×7（鏡射 src）", 12, 45, 356, 44))
p8.append(v("t_int", "d_test", LEAF(), "pytest/integration/\ntest_install / init / verify / diff.py", 12, 100, 356, 44))
p8.append(v("t_sys", "d_test", LEAF(), "pytest/system/\n整個 image：docker run 每個子命令", 12, 155, 356, 44))
p8.append(v("t_acc", "d_test", LEAF(), "pytest/acceptance/\n第 3 頁三條泳道：fixture 專案裡真的打 just", 12, 210, 356, 44))
p8.append(v("t_nf", "d_test", LEAF(), "pytest/integration/test_perf_verify.py\n非功能：verify 時間預算", 12, 265, 356, 44))
p8.append(v("t_lint", "d_test", LEAF(), "lint/{ruff, hadolint, import-linter}/\n靜態分析＋架構契約", 12, 320, 356, 44))
p8.append(v("t_fix", "d_test", LEAF(), "fixtures/\n假的 dist/、init.toml、專案", 12, 375, 356, 44))
p8.append(v("t_conf", "d_test", LEAF(), "pytest/<層級>/conftest.py\n每層的資源限制（見右欄）", 12, 430, 356, 44))
p8.append(v("d_df", "repo", LEAF(), "Dockerfile（下面的 stage）", 20, 720, 180, 40))
p8.append(v("d_bake", "repo", LEAF(), "docker-bake.hcl（group）", 220, 720, 180, 40))
p8.append(v("d_adr", "repo", LEAF(), "doc/adr/\n測試分層與閘門（沿用 base ADR-12/15/18）", 20, 780, 380, 44))
p8.append(v("d_ci", "repo", LEAF(), ".github/workflows/\nbake validate test → system/acceptance → bake release", 20, 836, 380, 44))
# 欄 2：Dockerfile stage
p8.append(v("stages", "1", SW(YELLOW), "Dockerfile stage（BuildKit）", 520, 70, 380, 900))
p8.append(v("s_rt", "stages", PURPLE_LEAF, "runtime\nFROM toml-bridge + src/", 90, 60, 200, 50))
p8.append(v("s_tb", "stages", PURPLE_LEAF, "test-base\n= runtime + pytest + fixtures", 90, 160, 200, 50))
p8.append(v("s_lint", "stages", PURPLE_LEAF, "lint", 20, 270, 160, 40))
p8.append(v("s_unit", "stages", PURPLE_LEAF, "unit-test", 200, 270, 160, 40))
p8.append(v("s_inst", "stages", PURPLE_LEAF, "install-test", 20, 330, 160, 40))
p8.append(v("s_init", "stages", PURPLE_LEAF, "init-test", 200, 330, 160, 40))
p8.append(v("s_ver", "stages", PURPLE_LEAF, "verify-test", 20, 390, 160, 40))
p8.append(v("s_diff", "stages", PURPLE_LEAF, "diff-test", 200, 390, 160, 40))
p8.append(v("s_rel", "stages", PURPLE_LEAF, "release\n= runtime（最終產物）", 90, 520, 200, 50))
p8.append(v("s_smoke", "stages", PURPLE_LEAF, "smoke\nFROM release；跑一次最小安裝", 90, 620, 200, 50))
p8.append(v("s_host", "stages", TEXT(11), "system / acceptance 不在 Dockerfile 裡：\n要 docker run，所以在 CI 主機上跑", 20, 720, 340, 40))
p8.append(v("s_bake", "stages", TEXT(11), "docker-bake.hcl：group validate = [lint, unit-test, install-test, init-test, verify-test, diff-test]；\ngroup release = [release, smoke]；CI 平行跑", 20, 790, 340, 60))
p8.append(e("s1", "s_rt", "s_tb", "FROM", (0.5, 1), (0.5, 0), vert=True))
p8.append(e("s2", "s_tb", "s_lint", "", (0.3, 1), (0.5, 0)))
p8.append(e("s3", "s_tb", "s_unit", "", (0.7, 1), (0.5, 0)))
p8.append(e("s4", "s_lint", "s_inst", "", (0.5, 1), (0.5, 0)))
p8.append(e("s5", "s_unit", "s_init", "", (0.5, 1), (0.5, 0)))
p8.append(e("s6", "s_inst", "s_ver", "", (0.5, 1), (0.5, 0)))
p8.append(e("s7", "s_init", "s_diff", "", (0.5, 1), (0.5, 0)))
p8.append('<mxCell id="s8" value="FROM（不經過任何 test stage）" style="' + EDGE + 'align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="stages" source="s_rt" target="s_rel"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="365" y="85"/><mxPoint x="365" y="545"/></Array></mxGeometry></mxCell>')
p8.append(e("s9", "s_rel", "s_smoke", "FROM", (0.5, 1), (0.5, 0), vert=True))
# 欄 3：強制閘門
p8.append(v("gates", "1", SW(RED), "強制閘門（不靠提醒，違反就 CI 紅）", 960, 70, 460, 900))
p8.append(v("g1", "gates", LEAF(), "BuildKit stage 依賴\nrelease 只 FROM runtime → 測試碼、pytest 進不了產品 image", 20, 50, 420, 50))
p8.append(v("g2", "gates", LEAF(), "import-linter 契約（lint stage）\n模組只能沿第 1 頁的線 import；只有 repo_fs 能 import 檔案系統", 20, 120, 420, 50))
p8.append(v("g3", "gates", LEAF(), "鏡射檢查（lint stage）\n每個 src 模組必有 test_<模組>.py，缺一個就失敗", 20, 190, 420, 50))
p8.append(v("g4", "gates", LEAF(), "unit conftest\nopen()/socket 被換成會炸的假物件：unit 不准碰檔案、網路、Docker", 20, 260, 420, 50))
p8.append(v("g5", "gates", LEAF(), "integration conftest\n只給 tmp 目錄；禁 Docker、網路；只能呼叫 cli.main()（公開介面）", 20, 330, 420, 50))
p8.append(v("g6", "gates", LEAF(), "每個子命令一個 test stage\n各自只 COPY 自己的測試檔，互不可見；哪個 stage 紅 = 哪條泳道壞", 20, 400, 420, 50))
p8.append(v("g7", "gates", LEAF(), "時間預算（integration）\nverify 在 fixture 上超過預算即失敗（每次 just 都會跑它）", 20, 470, 420, 50))
p8.append(v("g8", "gates", LEAF(), "system / acceptance 只能碰公開介面\n只准 docker run 與檔案系統，不准 import vendor_kit", 20, 540, 420, 50))
p8.append(v("g9", "gates", LEAF(), "release 必過 smoke\nrelease image 跑一次最小安裝失敗就不 push", 20, 610, 420, 50))
p8.append(v("g_map", "gates", TEXT(11) + "align=left;", "對應：unit ↔ 第 1 頁模組；integration ↔ 第 5 頁泳道；acceptance ↔ 第 3 頁泳道；\n層級名稱沿用 base ADR-18（ISTQB）：unit / integration / system / acceptance；smoke 為類型", 20, 690, 420, 60))
# 欄 1 → 欄 2 的 COPY 關係（直線，同高）
p8.append(e("c1", "t_unit", "s_unit", "COPY", (1, 0.5), (0, 0.5)))
p8.append(e("c2", "t_lint", "s_lint", "COPY", (1, 0.5), (0, 0.5)))
p8 += legend("p8", 40, 1010, ["red", "yellow", "pimg", "neutral", "white"], "實線 = 依賴／複製方向")
p8 += terms("p8", 40, 1120, [
 ("stage", "Dockerfile 裡的一個階段（FROM … AS 名稱）；docker build --target <名稱> 只做到那一階"),
 ("BuildKit", "Docker 的建置引擎：只會建最終目標依賴到的 stage，沒被依賴的測試 stage 不會執行、也不會進 image"),
 ("bake", "docker buildx bake：用一個檔定義多個 stage 目標與群組，CI 一次平行跑"),
 ("conftest.py", "pytest 每個目錄的共用設定；這裡用來對該層測試強制資源限制"),
 ("import-linter", "檢查 Python 模組之間誰可以 import 誰的工具；契約寫在設定檔，違反就失敗"),
 ("fixture", "測試用的假資料（假的 dist/、假的專案）"),
])
'''
s = s.replace("doc = ('<mxfile", p8 + "\ndoc = ('<mxfile", 1)
s = s.replace('+ page("p7", "6. 原型對照", p7, h=920)', '+ page("p7", "6. 原型對照", p7, h=920)\n       + page("p8", "7. repo 結構與測試分層", p8)')
open("gen18.py", "w", encoding="utf-8").write(s)
print("ok")
