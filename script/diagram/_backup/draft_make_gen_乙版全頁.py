"""gen56 → gen57：全面改乙版（引擎與工具 image 分離、薄殼 + gen/、命名空間 vendor_kit、bootstrap 詢問式、四角色、契約）。"""
import re
src = open("gen56.py").read()

def rep(old, new, cnt=1):
    global src
    assert src.count(old) == cnt, (src.count(old), old[:90])
    src = src.replace(old, new)

def block(start_marker, end_marker):
    """回傳 (start, end) index，end 為 end_marker 的起點。"""
    s = src.index(start_marker); e = src.index(end_marker, s)
    return s, e

# ===================== 第 1 頁 =====================
rep('p1 = [v("title", "1", TITLE, "vendor_kit 架構圖（模組 → 最小單元；線上文字 = 傳的資料）", 40, 20, 900, 30)]',
    'p1 = [v("title", "1", TITLE, "vendor_kit 架構圖（乙版：引擎容器 = .version 的 vendor_kit 那一版；工具 image 只放檔案）", 40, 20, 900, 30)]')
rep('"⚠ 待你回覆：命令介面的子命令清單是否就是 install / init / verify / diff / accept / bootstrap / upgrade 七個？", 960, 15, 560, 60))',
    '"⚠ 待你回覆：命令介面的子命令清單是否就是 install / init / verify / diff / accept / bootstrap / upgrade / add 八個？（ensure 是啟動器的，不是子命令）", 960, 15, 560, 60))')
rep('p1.append(v("img", "1", PURPLE_SW, "image 內容", 200, 300, 180, 280))',
    'p1.append(v("img", "1", PURPLE_SW, "工具 image 的檔案（/dist）", 200, 230, 180, 350))\np1.append(v("img_t", "img", TEXT(11), "工具 image 只放檔案、沒有程式；\n啟動器先用 docker cp 抓到暫存目錄，\n再掛進引擎容器當 /dist（第 3 頁）", 6, 40, 168, 66))')
rep('p1.append(v("i_list", "img", LEAF(), "init.toml", 46, 121, 88, 40))', 'p1.append(v("i_list", "img", LEAF(), "init.toml", 46, 191, 88, 40))')
rep('p1.append(v("i_dist", "img", LEAF(), "dist/（全部）", 46, 172, 88, 40))', 'p1.append(v("i_dist", "img", LEAF(), "dist/（全部）", 46, 242, 88, 40))')
rep('p1.append(v("i_tpl", "img", LEAF(), "模板", 46, 223, 88, 40))', 'p1.append(v("i_tpl", "img", LEAF(), "模板", 46, 293, 88, 40))')
rep('p1.append(v("vk", "1", PURPLE_SW, "vendor_kit（一個 container）", VX, VY, 660, 940))',
    'p1.append(v("vk", "1", PURPLE_SW, "vendor_kit 引擎（一個 container，版本 = .version 的 vendor_kit 行）", VX, VY, 660, 940))')
rep('p1.append(v("cli_upg", "m_cli", LEAF(), "upgrade", 196, 92, 88, 40))',
    'p1.append(v("cli_upg", "m_cli", LEAF(), "upgrade", 196, 92, 88, 40))\np1.append(v("cli_add", "m_cli", LEAF(), "add", 288, 92, 88, 40))')
rep('p1.append(v("p_boot", "proj", LEAF(), "啟動器 .vendor_kit/\\n＋ 根目錄的 justfile、.version", 10, 490, 180, 44).replace("fontSize=14", "fontSize=12"))',
    'p1.append(v("p_boot", "proj", LEAF(), "啟動器 .vendor_kit/（薄殼＋gen/）\\n＋ 根目錄的 justfile、.version、renovate.json", 10, 490, 180, 44).replace("fontSize=14", "fontSize=11"))')
rep(''' ("vendor_kit", "通用安裝工具；只以 container 形態執行（開發、使用皆是），主機不需安裝"),''',
    ''' ("vendor_kit（引擎）", "通用安裝工具；只以 container 形態執行，主機不需安裝；一個專案只用一版（.version 的 vendor_kit 行），工具 image 裡沒有它"),
 ("工具 image / 抓檔案", "工具出貨的 image 只放檔案（dist/、init.toml、VERSION），沒有程式；啟動器用 docker create + docker cp 把檔案抓到暫存目錄，掛進引擎容器當 /dist"),''')
rep(''' ("install / init / verify / diff / accept / bootstrap / upgrade", "子命令：安裝 dist 到 .<repo>/／第一次建立使用者檔／檢查 .<repo>/ 沒被改／升級後三方比對／把新版模板存成基準／寫出啟動器（第 10 頁）／查最新版改 .version（第 11 頁）"),''',
    ''' ("install / init / verify / diff / accept / bootstrap / upgrade / add", "子命令：安裝 dist 到 .<repo>/／第一次建立使用者檔／檢查 .<repo>/ 沒被改／升級後三方比對／把新版模板存成基準／寫出啟動器（第 10 頁）／查最新版改 .version（第 11 頁）／接新工具：查最新版寫進 .version 並 install + init"),''')
rep(''' ("兩棵樹比對", "verify 的做法：把 image 內的 dist 跟專案的 .<repo>/ 逐檔比：''',
    ''' ("兩棵樹比對", "verify 的做法：把抓出來的 dist（/dist）跟專案的 .<repo>/ 逐檔比：''')
rep(''' ("啟動器", "專案 repo 裡的 .vendor_kit/：vendor_kit 寫出的標準 just 指令，使用者打 just 時由它起容器；justfile 只是引用入口"),''',
    ''' ("啟動器", "專案 repo 裡的 .vendor_kit/：薄殼（進 git：entry.just、vendor.just 只有 ensure + 一行 docker run、ci/check.sh、baseline/）＋ gen/（不進 git，由引擎產生的其餘指令）；justfile 只有一行 import"),''')
rep(''' ("印記檔", ".<repo>/.stamp：第一行 = 裝的 image（啟動器傳進來的 .version 字串），之後每檔指紋（給人追溯用）；verify 只用第一行判斷要不要重裝，內容以 image 為準"),''',
    ''' ("印記檔", ".<repo>/.stamp：第一行 = 裝的 image（啟動器用 --self 傳進來的 .version 字串），之後每檔指紋（給人追溯用）；verify 只用第一行判斷要不要重裝，內容以抓出來的 dist 為準"),''')

# ===================== 第 2 頁 =====================
rep('p1b.append(v("t_t", "tool", TEXT(11), "工具名 = <repo>；下面四樣是接上 vendor_kit 的必要條件", 10, 40, 300, 30))',
    'p1b.append(v("t_t", "tool", TEXT(11), "工具名 = <repo>；下面四樣是接上 vendor_kit 的必要條件；image 裡沒有程式", 10, 40, 300, 30))')
rep('"Dockerfile.dist\\n（只放檔案，沒有程式）", 20, 145, 135, 50))', '"Dockerfile.dist\\n（FROM scratch：只放檔案）", 20, 145, 135, 50))')
rep('"必要條件：.version、justfile、.vendor_kit/（啟動器本體，第 10 頁 bootstrap 寫出；justfile 只用 mod? 掛它）；每個工具各自裝到 .<repo>/", 10, 40, 750, 30))',
    '"必要條件：.version、justfile（一行 import）、.vendor_kit/（薄殼＋baseline/ 進 git；gen/ 不進 git，ensure 自動長）；第 10 頁 bootstrap 寫出；每個工具各自裝到 .<repo>/", 10, 40, 750, 30))')
rep('p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器與版本檔", 20, 80, 700, 205))', 'p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器與版本檔", 20, 80, 700, 225))')
rep('p1b.append(v("p_vk", "pa", LEAF(), ".vendor_kit/（啟動器本體）\\nvendor.just、tools.just、.stamp、baseline/<repo>/", 12, 142, 316, 50).replace("fontSize=14", "fontSize=12"))',
    'p1b.append(v("p_vk", "pa", LEAF(), ".vendor_kit/（啟動器）\\n進 git：entry.just、vendor.just（薄殼：ensure＋一行 docker run）、ci/check.sh、baseline/<repo>/\\n不進 git：gen/（其餘指令、tools.just、.stamp，引擎產生）", 12, 142, 316, 70).replace("fontSize=14", "fontSize=11"))')
rep('"根 justfile 只有一行 mod? vendor_kit \'.vendor_kit/vendor.just\' → 指令都是 just vendor_kit <動作>；工具的 tool.just 也用自己的命名空間（mod? <模組> → just <模組> build）；工具 recipe 開頭先呼叫 just vendor_kit ensure 做自動檢查", 350, 74, 336, 118))',
    '"根 justfile 只有一行 import \'.vendor_kit/entry.just\' → 引擎指令都是 just vendor_kit <動作>；工具的指令由 gen/tools.just 用工具自己的命名空間接進來（mod docker → just docker build）；每個工具 recipe 開頭先 just vendor_kit ensure；主機 just ≥ 1.33（下載版）", 350, 74, 336, 138))')
rep('p1b.append(v("p_eng", "proj", PURPLE_LEAF, "引擎容器（vendor_kit:vN）\\n一個專案只有這一版引擎", 20, 350, 300, 60))',
    'p1b.append(v("p_eng", "proj", PURPLE_LEAF, "引擎容器（vendor_kit:vN）\\n一個專案只有這一版引擎", 20, 360, 300, 60))')
rep('p1b.append(v("p_eng_t", "proj", TEXT(11) + "align=left;", "以使用者身分執行，跑完即刪；先對專案目錄上鎖", 20, 412, 300, 20))',
    'p1b.append(v("p_eng_t", "proj", TEXT(11) + "align=left;", "以使用者身分執行，跑完即刪；先對專案目錄上鎖；工具檔案由啟動器抓到暫存目錄後掛成 /dist", 20, 422, 300, 30))')
rep('p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<repo>-dist:vX", 30, 360, 200, 40))', 'p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<repo>-dist:vX（只有檔案）", 30, 370, 200, 40))')
rep('"每次 upgrade 整批覆蓋；verify 拿它跟 image 比\\n印記檔 = 裝的 image + 每檔指紋", 6, 88, 210, 32))', '"每次升級整批覆蓋；verify 拿它跟抓出的 dist 比\\n印記檔 = 裝的 image + 每檔指紋", 6, 88, 210, 32))')
rep('p1b.append(e("f7b", "p_just", "p_vk", "mod?", (0.5, 1), (0.877, 0), vert=True))', 'p1b.append(e("f7b", "p_just", "p_vk", "import", (0.5, 1), (0.877, 0), vert=True))')
rep('p1b.append(e("f8", "p_vk", "p_eng", "工具名、版本、使用者身分、專案路徑", (0.5, 1), (0.5667, 0), vert=True))',
    'p1b.append(e("f8", "p_vk", "p_eng", "工具名、image 字串、使用者身分、專案路徑、抓出的 dist", (0.5, 1), (0.5667, 0), vert=True))')
rep('"實線 = 傳輸內容\\n虛線箭頭 = 基底 image → 以它為底的 image；虛線框 = 可有可無的檔")]', '"實線 = 傳輸內容\\n虛線框 = 可有可無的檔")]')
rep(''' ("GHCR", "GitHub 提供的 image 倉庫；每個工具一個 <repo>-dist image，以 vendor_kit image 為底"),''',
    ''' ("GHCR", "GitHub 提供的 image 倉庫；每個工具一個 <repo>-dist image（只放檔案）；引擎 vendor_kit image 另外一個"),''')
rep(''' ("just / justfile / .vendor_kit/", "just = 主機的指令跑器；.vendor_kit/ = 啟動器本體（vendor_kit 寫出，人不改；升級只換 vendor.just／tools.just／.stamp，baseline/ 不動）；justfile = 專案自己的指令清單，第一行 mod? vendor_kit '.vendor_kit/vendor.just' 把它掛進來"),
 ("recipe / 命名空間 / mod? / ensure", "recipe = justfile 裡的一條指令；命名空間 = 指令前的分組名（just vendor_kit …、just <模組> …）；mod? = justfile 把另一個檔掛成命名空間的寫法；ensure = 每個工具指令開頭自動跑的檢查／安裝（第 3 頁）"),''',
    ''' ("just / justfile / .vendor_kit/", "just = 主機的指令跑器（≥ 1.33，用下載版）；.vendor_kit/ = 啟動器：薄殼進 git（人不改；引擎升級時整個換新）、gen/ 不進 git（引擎產生）、baseline/ 持久不動；justfile = 專案自己的指令清單，第一行 import '.vendor_kit/entry.just'"),
 ("recipe / 命名空間 / import / ensure", "recipe = justfile 裡的一條指令；命名空間 = 指令前的分組名（just vendor_kit …、just docker …）；import = justfile 把另一個檔接進來的寫法；ensure = 每個工具指令開頭自動跑的檢查／安裝（第 3 頁）"),''')
rep(''' ("Dockerfile / Dockerfile.dist / FROM", "Dockerfile = 打包 image 的食譜；Dockerfile.dist = 工具 repo 出貨用的食譜；FROM = 食譜第一行，指定以哪個 image 為底"),''',
    ''' ("Dockerfile / Dockerfile.dist / FROM scratch", "Dockerfile = 打包 image 的食譜；Dockerfile.dist = 工具 repo 出貨用的食譜，FROM scratch = 從空白開始只放檔案（工具 image 不含任何程式）"),''')
rep(''' ("install / init / verify / diff / accept", "安裝容器的子命令：把 dist 裝進 .<repo>/ 並寫印記檔／第一次建立初始檔／拿 .<repo>/ 跟 image 內的 dist 比／升級後三方比對／把新版模板存成基準"),
])''', ''' ("install / init / verify / diff / accept / add", "引擎的子命令：把 dist 裝進 .<repo>/ 並寫印記檔／第一次建立初始檔／拿 .<repo>/ 跟抓出的 dist 比／升級後三方比對／把新版模板存成基準／接新工具（查最新版寫進 .version 並 install + init）"),
 ("docker create / cp", "不啟動容器、只把 image 裡的檔案複製出來的兩個 docker 指令；啟動器用它從工具 image 取 dist"),
])''')
# 第 2 頁「工具 repo」內容補 docker.just
rep('p1b.append(v("t_n", "tool", TEXT(11), "其他內容（doc、test、CI 腳本…）不在 dist/ 裡，不會出貨", 10, 205, 300, 40))',
    'p1b.append(v("t_n", "tool", TEXT(11), "dist/just/docker.just = 工具自己的 just 指令；其他內容（doc、test…）不在 dist/ 裡，不會出貨", 10, 205, 300, 40))')

# ===================== 第 3 頁 =====================
rep('("安裝容器（vendor_kit）", 800, 360)', '("引擎容器（vendor_kit:vN）", 800, 360)')
s, e_ = block('# ---- A 第一次 ----', '# ---- B 日常 ----')
src = src[:s] + '''# ---- A 第一次 ----
band("bA", "第一次接上工具：bootstrap 問答（第 10 頁）或 just vendor_kit add <repo>", 100, 400)
p2.append(v("a_u", "bA", ELLIPSE(GREEN), "bootstrap 問答 或\\njust vendor_kit add <repo>", 60, 65, 200, 60).replace("fontSize=14", "fontSize=13"))
p2.append(v("a_c0", "bA", PURPLE_LEAF, "add\\n查 registry 最新 tag + digest → 寫 <repo> = \\"image\\" 進 .version（有就報錯）", 800, 60, 340, 70).replace("fontSize=14", "fontSize=12"))
p2.append(v("a_p0", "bA", FILE, ".version（多一行）", 1240, 75, 200, 40))
p2.append(v("a_l1", "bA", LEAF(), "讀版本檔（.version.local 優先）\\n抓工具 image 的檔案：docker create\\n＋ docker cp → 暫存目錄，掛成 /dist", 360, 158, 180, 66).replace("fontSize=14", "fontSize=11"))
p2.append(v("a_l2", "bA", LEAF(), ".<repo>/ 不存在\\n→ 要安裝", 570, 166, 150, 50))
p2.append(v("a_c1", "bA", PURPLE_LEAF, "install\\n/dist 全部 → .<repo>/\\n並寫印記（.<repo>/.stamp：裝的 image + 每檔指紋）", 800, 156, 340, 70).replace("fontSize=14", "fontSize=13"))
p2.append(v("a_p1", "bA", FILE, ".<repo>/（新）", 1240, 171, 200, 40))
p2.append(v("a_c2", "bA", PURPLE_LEAF, "init\\n照 init.toml 複製初始檔（已存在：警告、不覆蓋）\\n並把這版模板存成基準", 800, 270, 340, 60).replace("fontSize=14", "fontSize=13"))
p2.append(v("a_p2", "bA", FILE, "Dockerfile / entrypoint / hooks…\\n（新；之後由你維護）\\n＋ .vendor_kit/baseline/<repo>/", 1240, 270, 200, 60).replace("fontSize=14", "fontSize=12"))
p2.append(v("a_n", "bA", NOTE, "bootstrap.sh 問「要接哪個工具？版本？」→ 對每個答案跑一次 add；之後再接工具用 just vendor_kit add；.version 不必手改", 40, 150, 300, 60))
p2.append(e("ae1", "a_u", "a_c0", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae1b", "a_c0", "a_p0", "寫入", (1, 0.5), (0, 0.5)))
p2.append('<mxCell id="ae1c" value="接著 ensure" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="bA" source="a_c0" target="a_l1"><mxGeometry x="-0.4" relative="1" as="geometry"><Array as="points"><mxPoint x="970" y="143"/><mxPoint x="450" y="143"/></Array></mxGeometry></mxCell>')
p2.append(e("ae2", "a_l1", "a_l2", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae3", "a_l2", "a_c1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae4", "a_c1", "a_p1", "寫入", (1, 0.5), (0, 0.5)))
p2.append(e("ae5", "a_c1", "a_c2", "", (0.5, 1), (0.5, 0)))
p2.append(e("ae6", "a_c2", "a_p2", "建立", (1, 0.5), (0, 0.5)))
''' + src[e_:]
rep('band("bB", "日常：just <模組> build（建置）；run（啟動）／exec（進入）／stop（停止）流程相同", 410, 390)',
    'band("bB", "日常：just docker build（工具自己的指令；run／exec／stop 流程相同）— 開頭自動 just vendor_kit ensure", 530, 390)')
rep('p2.append(v("b_u", "bB", ELLIPSE(GREEN), "just <模組> build", 60, 70, 180, 50))', 'p2.append(v("b_u", "bB", ELLIPSE(GREEN), "just docker build", 60, 70, 180, 50))')
rep('p2.append(v("b_l1", "bB", LEAF(), "讀版本檔（.version.local 優先，\\n否則 .version）一行一個工具", 355, 67, 150, 56).replace("fontSize=14", "fontSize=11"))',
    'p2.append(v("b_l1", "bB", LEAF(), "ensure：讀版本檔（.version.local 優先）\\n抓工具 image 檔案（docker create/cp）\\n→ 暫存目錄，掛成 /dist", 345, 62, 170, 66).replace("fontSize=14", "fontSize=11"))')
rep('"例外：右邊是 path:（.version.local）→ 第 4 頁本機開發模式；\\nvendor_kit 那行 → 換 .vendor_kit/ 程式檔（第 11 頁 C）", 30, 130, 300, 150))',
    '"例外：右邊是 path:（.version.local）→ 第 4 頁本機開發模式；\\nvendor_kit 那行 = 引擎版本 → 不同就用新引擎重產 .vendor_kit/（第 11 頁 C）\\n每個工具指令開頭都自動跑 ensure；引擎 = .version 的 vendor_kit 行那一版", 30, 130, 300, 150))')
rep('p2.append(v("b_c0", "bB", PURPLE_LEAF, "install\\n換成 .version 指定的版本", 800, 65, 340, 60))', 'p2.append(v("b_c0", "bB", PURPLE_LEAF, "install\\n用抓出的 /dist 換成 .version 指定的版本", 800, 65, 340, 60))')
rep('p2.append(v("b_l1n", "bB", TEXT(11), "（image 不在本機時，Docker 會先下載）", 340, 126, 220, 24))', 'p2.append(v("b_l1n", "bB", TEXT(11), "（image 不在本機時，Docker 會先下載）", 340, 132, 220, 24))')
rep('p2.append(v("b_c1", "bB", PURPLE_LEAF, "verify\\n.<repo>/ 跟 image 內的 dist 逐檔比（缺、多、改都算）", 800, 170, 340, 60).replace("fontSize=14", "fontSize=13"))',
    'p2.append(v("b_c1", "bB", PURPLE_LEAF, "verify\\n.<repo>/ 跟抓出的 /dist 逐檔比（缺、多、改都算）", 800, 170, 340, 60).replace("fontSize=14", "fontSize=13"))')
rep('p2.append(v("b_err", "bB", ELLIPSE(RED), "中止：.<repo>/ 被改過（列出哪些檔）\\n刪除 .<repo>/ 再 build 即自動重裝", 40, 285, 260, 60).replace("fontSize=14", "fontSize=12"))',
    'p2.append(v("b_err", "bB", ELLIPSE(RED), "中止：.<repo>/ 被改過（列出哪些檔）\\n刪除 .<repo>/ 再 just vendor_kit ensure 即重裝", 40, 285, 260, 60).replace("fontSize=14", "fontSize=12"))')
rep('band("bC", "升級：Renovate 開的 PR 被 merge", 830, 390)', 'band("bC", "升級：Renovate 開的 PR 被 merge", 950, 390)')
rep('p2.append(v("c_l1", "bC", LEAF(), "下次 just <模組> build 走上面\\n「否則」分支 → install 新版", 380, 65, 340, 50))', 'p2.append(v("c_l1", "bC", LEAF(), "下次工具指令的 ensure 走上面\\n「否則」分支 → install 新版", 380, 65, 340, 50))')
rep('"diff（三方）\\n基準 vs image 內的新版模板 vs 你的初始檔\\n只印出「工具改了什麼」「你改了什麼」，不改檔"', '"diff（三方）\\n基準 vs 抓出的新版模板 vs 你的初始檔\\n只印出「工具改了什麼」「你改了什麼」，不改檔"')
rep('p2.append(v("c_c3", "bC", PURPLE_LEAF, "accept\\n把 image 內的新版模板存成基準", 800, 305, 340, 60))', 'p2.append(v("c_c3", "bC", PURPLE_LEAF, "accept\\n把抓出的新版模板存成基準", 800, 305, 340, 60))')
rep('p2.append(v("p2n", "1", NOTE, "紫框 = 子命令：install（第一次、版本改變時）、init（只有第一次）、verify（已安裝且版本一致時）、diff／accept（升級後由使用者呼叫）。\\n沒有 Renovate 時用 just vendor_kit upgrade <repo> 手動：只改 .version 那行就停；下次 just 才 install，再自己打 just vendor_kit diff（第 11 頁 B）。\\n同一專案兩個 just 同時跑：容器先對專案目錄上鎖，後到的等前一個裝完再檢查（第 5 頁）。", 20, 1240, 1620, 60))',
    'p2.append(v("p2n", "1", NOTE, "紫框 = 引擎子命令：add（接工具）、install（第一次、版本改變時）、init（只有第一次）、verify（已安裝且版本一致時）、diff／accept（升級後由使用者呼叫）。引擎容器每次都是 .version 的 vendor_kit 那一版；工具 image 裡沒有程式，只是檔案來源。\\n沒有 Renovate 時用 just vendor_kit upgrade <repo> 手動：只改 .version 那行就停；下次 just 才 install，再自己打 just vendor_kit diff（第 11 頁 B）。\\n同一專案兩個 just 同時跑：引擎先對專案目錄上鎖，後到的等前一個裝完再檢查（第 5 頁）。刪掉 .<repo>/ 後工具指令也消失，復原入口 = just vendor_kit ensure。", 20, 1360, 1620, 76))')
rep('p2 += legend_flow("p2", 40, 1320, files=True, note=True, dashed=True)', 'p2 += legend_flow("p2", 40, 1456, files=True, note=True, dashed=True)')
rep('p2 += terms("p2", 40, 1430, [', 'p2 += terms("p2", 40, 1566, [')
rep(''' ("啟動器", "專案裡的 .vendor_kit/（vendor_kit 寫出的標準 just 指令；justfile 只是引用它）：使用者打 just 時，它讀版本檔、起安裝容器、再執行工具的腳本"),''',
    ''' ("啟動器 / ensure", "專案裡的 .vendor_kit/（薄殼進 git、gen/ 由引擎產生）：每個工具指令開頭自動跑 ensure — 讀版本檔、抓工具檔案、起引擎容器 install／verify、再執行工具的腳本；復原入口 just vendor_kit ensure"),
 ("docker create / cp", "不啟動容器、只把 image 裡的檔案複製出來；工具 image 只放檔案，靠這兩步抓到暫存目錄再掛給引擎當 /dist"),
 ("add", "接新工具的子命令：查 registry 最新 tag + digest，寫一行進 .version，接著 install + init；bootstrap 問答與 just vendor_kit add <repo> 都走它"),''')
rep(''' ("build / run / exec / stop", "四個日常指令：建置 image／啟動容器／進入容器／停止容器；都先經過同樣的檢查再執行 .<repo>/ 內的腳本"),''',
    ''' ("build / run / exec / stop", "工具（例：base）自己提供的四個日常指令（just docker …，vendor_kit 不定義）：建置 image／啟動容器／進入容器／停止容器；開頭都先 ensure 再執行 .<repo>/ 內的腳本"),''')
rep(''' ("install / init / verify / diff / accept", "子命令：安裝 dist 到 .<repo>/ 並寫印記／第一次建立初始檔／拿 .<repo>/ 跟 image 內的 dist 比／升級後三方比對／存新基準"),''',
    ''' ("install / init / verify / diff / accept", "引擎子命令：安裝 /dist 到 .<repo>/ 並寫印記／第一次建立初始檔／拿 .<repo>/ 跟抓出的 /dist 比／升級後三方比對／存新基準"),''')
rep('p2.append(v("h_1240", "1", "text;html=1;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;", "專案目錄", 1240, 60, 380, 24))', 'p2.append(v("h_1240", "1", "text;html=1;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;", "專案目錄", 1240, 60, 380, 24))', 0) if False else None

# ===================== 第 4 頁 =====================
rep('p3.append(v("c6", "up", LEAF(), "執行 just → 啟動器自動 install 新版", 20, 110, 380, 40))', 'p3.append(v("c6", "up", LEAF(), "執行工具指令 → ensure 抓新版檔案、自動 install", 20, 110, 380, 40).replace("fontSize=14", "fontSize=13"))')
rep('p3.append(v("c16", "1", NOTE, "升級程式在新版 image 裡，不在專案的舊腳本裡，\\n所以不會有「舊工具幫自己升級」的問題。", 490, 100, 290, 60))',
    'p3.append(v("c16", "1", NOTE, "升級程式在引擎 image 裡；工具 image 只有檔案、沒有程式，\\n所以不會有「舊工具幫自己升級」的問題。", 490, 100, 290, 60))')
rep('"just vendor_kit dev <repo> ../tool\\n→ 寫 .version.local（不進 git）：<repo> = \\"path:../tool\\""', '"just vendor_kit dev <repo> -p ../tool（--path）\\n→ 寫 .version.local（不進 git）：<repo> = \\"path:../tool\\""')
rep('"之後每次 just：用 vendor_kit image 把 ../tool/dist 掛進來當 dist 安裝\\n印記第一行寫 dev:../tool"', '"之後每次 just：用 .version 那版引擎，把 ../tool/dist 掛進來當 /dist 安裝\\n印記第一行寫 path:../tool"')
rep('"看到 dev: 就不做完整性檢查，只印醒目警告、重新複製 dist"', '"看到 path: 就不做完整性檢查，只印醒目警告、重新複製 dist"')
rep(''' ("印記", ".<repo>/.stamp：第一行 = 裝的是哪個 image；本機開發時寫 dev:<路徑>"),
 ("dev / undev", "just vendor_kit dev <repo> <路徑> = 把工具指到本機原始碼（寫 .version.local）；just vendor_kit undev <repo> = 移除那行、回正式版；兩者的形式待回覆（第 9 頁）"),''',
    ''' ("印記", ".<repo>/.stamp：第一行 = 裝的是哪個 image；本機開發時寫 path:<路徑>"),
 ("dev / undev", "just vendor_kit dev <repo> -p/--path <目錄> = 把工具指到本機原始碼（寫 .version.local）；just vendor_kit undev <repo> = 移除那行、回正式版；帶值選項都有短選項（對齊 base 的 -t/--target）"),''')
rep(''' (".version.local / dev:", "跟 .version 同格式、不進 git 的覆蓋檔，有它那行就優先；印記第一行的 dev: 前綴 = 這個 .<repo>/ 來自本機路徑，不是正式 image"),''',
    ''' (".version.local / path:", "跟 .version 同格式、不進 git 的覆蓋檔，有它那行就優先；印記第一行的 path: 前綴 = 這個 .<repo>/ 來自本機路徑，不是正式 image"),''')

# ===================== 第 5 頁 =====================
rep('p4 = [v("title", "1", TITLE, "流程：vendor_kit 內部——五個子命令（install 是核心）；全部在容器內執行；bootstrap 見第 10 頁", 40, 20, 1200, 30)]',
    'p4 = [v("title", "1", TITLE, "流程：vendor_kit 引擎內部——五個子命令（install 是核心）；工具檔案由啟動器先抓到 /dist；bootstrap／add 見第 10 頁", 40, 20, 1200, 30)]')
rep('"⚠ 待你回覆：1. 主機腳本執行到一半時 .<repo>/ 被另一個 just 換掉：第一版不防、寫進限制？\\n2. install 進行中 .version 被改（另一邊 git checkout）：照原本讀到的版本裝完？", 1260, 4, 800, 50))',
    '"⚠ 待你回覆：1. 主機腳本執行到一半時 .<repo>/ 被另一個 just 換掉：第一版不防、寫進限制？\\n2. install 進行中 .version 被改（另一邊 git checkout）：照原本讀到的版本裝完？\\n3. ensure 範圍：每個工具指令前檢查 .version 全部工具（N 個 = N 次抓檔＋N 次容器），還是只檢查被叫到的工具？", 1260, 4, 800, 64))')
# install 泳道：前面加「抓工具檔」一格，其餘下移 70
s, e_ = block('p4.append(v("install", "1", SW(NEUTRAL), "install（核心：把 dist/ 放進 .<repo>/）", 20, 60, 460, 1070))', '# init\n')
blk = src[s:e_]
blk = blk.replace('p4.append(v("install", "1", SW(NEUTRAL), "install（核心：把 dist/ 放進 .<repo>/）", 20, 60, 460, 1070))',
                  'p4.append(v("install", "1", SW(NEUTRAL), "install（核心：把 /dist 放進 .<repo>/）", 20, 60, 460, 1140))\np4.append(v("l_pre", "install", LEAF(), "啟動器（容器外）：docker create + docker cp\\n把工具 image 的檔案抓到暫存目錄，掛成 /dist", 200, 45, 260, 50).replace("fontSize=14", "fontSize=11"))')
def shift_y(m):
    return f'{m.group(1)}{int(m.group(2)) + 70}{m.group(3)}'
# vertex 的 y（第 6 個參數）：v("id", "install", STYLE, "text", x, y, w, h)
blk = re.sub(r'(p4\.append\(v\("(?!install"|l_pre")[^"]*", "install", [^\n]*?, \d+, )(\d+)(, \d+, \d+\))', shift_y, blk)
for old, new in [('y="250"', 'y="320"'), ('y="440"', 'y="510"'), ('y="840"', 'y="910"')]:
    blk = blk.replace(old, new)
blk = blk.replace('p4.append(e("le0", "l0", "l1"))', 'p4.append(e("le_pre", "l_pre", "l0", "", (0.5, 1), (0.5, 0)))\np4.append(e("le0", "l0", "l1"))')
blk = blk.replace('"複製 dist/ 到亂數名暫存目錄"', '"複製 /dist 到亂數名暫存目錄"')
src = src[:s] + blk + src[e_:]
rep('"比對兩棵樹：image 內 dist vs .<repo>/\\n檔案集合（只豁免 .stamp）、內容指紋、\\n檔案種類、執行位（該可執行的仍可執行）"', '"比對兩棵樹：抓出的 /dist vs .<repo>/\\n檔案集合（只豁免 .stamp）、內容指紋、\\n檔案種類、執行位（該可執行的仍可執行）"')
rep('"多餘的檔也算失敗：.<repo>/ 是整批替換的目錄，不該有別的東西。失敗不自動重裝（會無聲毀掉手改），提示刪掉重跑 just。"', '"多餘的檔也算失敗：.<repo>/ 是整批替換的目錄，不該有別的東西。失敗不自動重裝（會無聲毀掉手改），提示刪掉 .<repo>/ 再 just vendor_kit ensure。"')
rep('p4.append(v("a2", "accept", LEAF(), "取 image 內的新版模板\\n（init.toml 列的檔）", 110, 200, 200, 50))', 'p4.append(v("a2", "accept", LEAF(), "取抓出的 /dist 裡的新版模板\\n（init.toml 列的檔）", 110, 200, 200, 50).replace("fontSize=14", "fontSize=12"))')
rep('p4.append(v("p4n", "1", NOTE, "已定案：verify 比 image 內的 dist 而不是印記（issue #23）；diff 三方（#22）；install／verify／accept 對專案目錄上鎖（#24）。本機開發模式見第 4 頁（#21）。", 20, 1150, 1500, 40))',
    'p4.append(v("p4n", "1", NOTE, "已定案：乙版——工具 image 只放檔案，引擎只有 .version 那一版（一個專案永遠一個引擎版本，不會有新啟動器叫舊引擎的問題）；verify 比抓出的 /dist 而不是印記（issue #23）；diff 三方（#22）；install／verify／accept 對專案目錄上鎖（#24）。本機開發模式見第 4 頁（#21）。", 20, 1220, 1500, 50))')
rep('p4 += legend_flow("p4", 40, 1210, purple=False, note=True)', 'p4 += legend_flow("p4", 40, 1290, purple=False, note=True)')
rep('p4 += terms("p4", 40, 1320, [', 'p4 += terms("p4", 40, 1400, [')
rep(''' ("兩棵樹比對", "把 image 內的 /dist 跟 .<repo>/ 逐檔比：''', ''' ("/dist / 兩棵樹比對", "/dist = 啟動器從工具 image 抓出、掛進引擎容器的檔案（工具 image 只放檔案）；兩棵樹比對 = 把 /dist 跟 .<repo>/ 逐檔比：''')

# ===================== 第 6 頁（已改，補一句）=====================
rep('p7.append(v("r_vk_n", "r_vk", TEXT(11), "vendor_kit 是產品本體；Dockerfile 只說明怎麼把它裝進 image", 10, 135, 280, 50))',
    'p7.append(v("r_vk_n", "r_vk", TEXT(11), "vendor_kit 是引擎本體；Dockerfile 把它裝進 image；啟動器（.vendor_kit/）由它寫出", 10, 135, 280, 50))')
rep('p7.append(v("f_just", "r_proj", LEAF(), "justfile", 180, 70, 140, 40))', 'p7.append(v("f_just", "r_proj", LEAF(), "justfile ＋ .vendor_kit/", 180, 70, 140, 40).replace("fontSize=14", "fontSize=12"))')

# ===================== 第 7 頁（資料夾）=====================
rep(''' (2, "cli.py", True, "命令介面：讀參數、分派 install / init / verify / diff / accept / upgrade（另有 bootstrap，第 10、11 頁）"),''',
    ''' (2, "cli.py", True, "命令介面：讀參數、分派 install / init / verify / diff / accept / upgrade / add / bootstrap"),
 (2, "launcher.py", True, "啟動器內容（純函式）：產生 entry.just、薄殼 vendor.just、gen/ 裡的指令、tools.just、ci/check.sh 的文字，bootstrap 與 ensure 寫進專案"),''')
rep(''' (2, "ci/check.sh", True, "給下游專案用的契約檢查腳本（第 12 頁）：唯一會 COPY 進出貨 image 的測試檔，bootstrap 寫到專案的 test/ci/check.sh，GitHub／GitLab 的 CI 只呼叫它"),''',
    ''' (2, "ci/check.sh", True, "給下游專案用的契約檢查腳本（第 12 頁）：唯一會 COPY 進出貨 image 的測試檔，bootstrap 寫到專案的 .vendor_kit/ci/check.sh，GitHub／GitLab 的 CI 只呼叫它"),''')
rep(''' (1, "Dockerfile.dist", True, "出貨食譜：FROM vendor_kit，疊上 dist/ 與 init.toml → <repo>-dist image"),''',
    ''' (1, "dist/just/docker.just", True, "工具自己的 just 指令（mod docker：build / run / exec / stop），每條 recipe 開頭先 just vendor_kit ensure；由 gen/tools.just 接進專案"),
 (1, "Dockerfile.dist", True, "出貨食譜：FROM scratch（空白），只 COPY dist/、init.toml、VERSION → <repo>-dist image（純檔案，沒有程式；multi-arch 但內容與架構無關）"),''')
rep(''' (1, "justfile", True, "進 git｜使用者的指令清單：第一行 mod? vendor_kit '.vendor_kit/vendor.just'，其餘自己加（第 9 頁）"),
 (1, ".vendor_kit/", False, "進 git｜啟動器本體：vendor.just、tools.just、.stamp（vendor_kit 寫出，人不改，升級只換這三個）"),
 (2, "baseline/<repo>/", False, "進 git｜三方比對的基準：init／accept 存的模板副本＋記下是哪個 image；人不改（diff 前檢查指紋）；升級不動"),''',
    ''' (1, "justfile", True, "進 git｜使用者的指令清單：第一行 import '.vendor_kit/entry.just'，其餘自己加（第 9 頁）"),
 (1, ".vendor_kit/", False, "進 git｜啟動器：vendor_kit 寫出，人不改；引擎升級時整個換新（baseline/ 除外）"),
 (2, "entry.just  vendor.just", True, "進 git｜入口（mod vendor_kit + import? gen/tools.just）／薄殼：只有 ensure 與一行 docker run bootstrap（永久凍結的契約）"),
 (2, "ci/check.sh", True, "進 git｜契約檢查腳本：GitHub／GitLab 的 CI 只呼叫它（第 12 頁）"),
 (2, "baseline/<repo>/", False, "進 git｜三方比對的基準：init／accept 存的模板副本＋記下是哪個 image；人不改（diff 前檢查指紋）；升級不動"),
 (2, "gen/", False, "不進 git（.git/info/exclude）｜引擎產生：vendor_kit.just（其餘指令）、tools.just（依 .version 接工具命名空間）、.stamp（記產生它的引擎版本）；ensure 發現引擎版本變了就重產"),''')
rep(''' (1, "test/ci/check.sh", True, "進 git｜契約檢查腳本（bootstrap 寫出，之後歸專案）：GitHub／GitLab 的 CI 只呼叫它（第 12 頁）"),
 (1, "renovate.json", True, "進 git｜Renovate 設定（bootstrap 寫出）：只含 extends，指向 vendor_kit 的共用 preset（第 11 頁 A）"),''',
    ''' (1, "renovate.json", True, "進 git｜Renovate 設定（bootstrap 寫出，只含 extends 指向 vendor_kit 的共用 preset）；放置位置待 ci_bridge 定案（issue #25）"),''')
rep(''' ("install / init / verify / diff / accept / bootstrap", "vendor_kit 的子命令：把 dist 裝進 .<repo>/ 並寫印記／建立初始檔＋存基準／拿 .<repo>/ 跟 image 內的 dist 比／三方比對新版模板／存新基準／第一次寫出啟動器（第 10 頁）"),''',
    ''' ("install / init / verify / diff / accept / bootstrap / add", "引擎的子命令：把 /dist 裝進 .<repo>/ 並寫印記／建立初始檔＋存基準／拿 .<repo>/ 跟抓出的 /dist 比／三方比對新版模板／存新基準／第一次寫出啟動器（第 10 頁）／接新工具"),
 ("薄殼 / gen/ / docker create+cp", "進 git 的最小啟動器（只讀 .version、跑一行 docker run）／引擎產生的其餘指令（不進 git）／不啟動容器、只把工具 image 的檔案複製出來的兩個指令"),''')

# ===================== 第 8 頁（測試）=====================
rep('p8.append(v("d_src", "repo", SW(RED, 16), "src/vendor_kit/（第 1 頁的 7 個模組）", 20, 50, 380, 140))', 'p8.append(v("d_src", "repo", SW(RED, 16), "src/vendor_kit/（第 1 頁的模組＋啟動器內容）", 20, 50, 380, 140))')
rep('''MODS = [("cli", "命令介面"), ("dist_reader", "出貨內容讀取"), ("repo_fs", "專案檔案存取"), ("template", "模板"),
        ("stamp", "印記"), ("diff", "差異比對"), ("report", "回報")]''',
    '''MODS = [("cli", "命令介面"), ("dist_reader", "出貨內容讀取"), ("repo_fs", "專案檔案存取"), ("template", "模板"),
        ("stamp", "印記"), ("diff", "差異比對"), ("report", "回報"), ("launcher", "啟動器內容")]''')
rep('p8.append(v("t_fix", "d_test", LEAF(), "fixtures/\\n假的 dist/、init.toml、VERSION、假專案", 12, 110, TW, 44))', 'p8.append(v("t_fix", "d_test", LEAF(), "fixtures/\\n假 dist/、init.toml、VERSION、假專案、假工具 image（FROM scratch）", 12, 110, TW, 44).replace("fontSize=14", "fontSize=12"))')
rep('p8.append(v("t_unit", "d_test", LEAF(), "pytest/unit/\\ntest_<模組>.py ×7（一個模組一個檔）", 12, 262, TW, 44))', 'p8.append(v("t_unit", "d_test", LEAF(), "pytest/unit/\\ntest_<模組>.py ×8（一個模組一個檔）", 12, 262, TW, 44))')
rep('"pytest/acceptance/\\n第 3 頁三條泳道：在假專案裡真的打 just"', '"pytest/acceptance/\\n空目錄 bootstrap.sh → add → just docker build（第 3 頁三情境）"')
rep('".github/workflows/（vendor_kit 自己的 CI）\\nbake validate → system/acceptance → release（兩種架構）"', '".github/workflows/（vendor_kit 自己的 CI）\\nbake validate → system/acceptance → release（amd64、arm64 各自 build 再合併）"')
rep('"test/ci/check.sh：給下游專案的契約檢查腳本（第 12 頁）\\n不在自己的 CI 序列裡；COPY 進 image 供 bootstrap 寫出"', '"test/ci/check.sh：給下游專案的契約檢查腳本（第 12 頁）\\n不在自己的 CI 序列裡；COPY 進 image，bootstrap 寫到專案 .vendor_kit/ci/"')
rep('p8.append(v("s_rtest", "stages", PURPLE_LEAF, "release-test\\nFROM release；真的 install + verify 一次", LX + 20, 850, LW, 60))', 'p8.append(v("s_rtest", "stages", PURPLE_LEAF, "release-test\\nFROM release；用純資料的假工具 image\\n真的 install + verify 一次", LX + 20, 850, LW, 60).replace("fontSize=14", "fontSize=12"))')
rep('("g1", "BuildKit stage 依賴\\nrelease 只 FROM runtime → 測試碼、pytest 進不了產品 image；release 同時 build amd64 + arm64（multi-arch）"),',
    '("g1", "BuildKit stage 依賴\\nrelease 只 FROM runtime → 測試碼、pytest 進不了產品 image；amd64、arm64 各在原生 runner build 並過 release-test 才合併成 multi-arch index"),')
rep(''' ("runtime / release / release-test", "runtime = 能執行 vendor_kit 的最小 image；release = 最終出貨的 image；release-test = 出貨前拿 release 真的裝一次"),''',
    ''' ("runtime / release / release-test", "runtime = 能執行 vendor_kit 的最小 image；release = 最終出貨的引擎 image；release-test = 出貨前拿 release 配純資料的假工具 image 真的裝一次"),''')
rep(''' ("install / init / verify / diff / accept / just", "子命令：把 dist 裝進 .<repo>/ 並寫印記／建立初始檔＋存基準／拿 .<repo>/ 跟 image 內的 dist 比／三方比對新版模板／存新基準（accept 的測試 stage 待補）；just = 使用者在主機打的指令跑器（第 3、9 頁）"),''',
    ''' ("install / init / verify / diff / accept / just", "引擎子命令：把 /dist 裝進 .<repo>/ 並寫印記／建立初始檔＋存基準／拿 .<repo>/ 跟抓出的 /dist 比／三方比對新版模板／存新基準（accept 的測試 stage 待補）；just = 使用者在主機打的指令跑器（第 3、9 頁）"),''')

# ===================== 第 9 頁（指令表）=====================
s, e_ = block('# ================= Page 8: 使用者介面：just 指令表 =================', '# ================= Page 10: 流程：bootstrap')
src = src[:s] + open("p9_v57.py").read() + "\n" + src[e_:]

# ===================== 第 10 頁（bootstrap）=====================
s, e_ = block('# ================= Page 10: 流程：bootstrap', '# ================= Page 11: 流程：升級與回退')
src = src[:s] + open("p11_v57.py").read() + "\n" + src[e_:]

# ===================== 第 11 頁（升級）=====================
rep('p12 = [v("title", "1", TITLE, "流程：升級與回退 ── 四條路徑（初版，待決處以便條標示）", 40, 20, 580, 30)]', 'p12 = [v("title", "1", TITLE, "流程：升級與回退 ── 四條路徑（乙版）", 40, 20, 580, 30)]')
rep('"⚠ 待你回覆：1. image 是公開還是私有？（決定 token 怎麼給）　2. upgrade 不給 name 時要拒絕（要 name 或 --all）？--all 含不含 vendor_kit 自身？　3. C 第一版「更新啟動器後停下來要求重跑」可接受？　4. .vendor_kit/ 程式檔重寫後由誰 commit（人手，CI 紅燈提醒）？", 640, 6, 940, 50))',
    '"⚠ 待你回覆：1. image 是公開還是私有？（決定 token 怎麼給）　2. upgrade 不給 <repo> 時要拒絕（要 <repo> 或 --all）？--all 含不含 vendor_kit 自身？　3. C 第一版「重產啟動器後停下來要求重打一次」可接受？　4. 薄殼（進 git 的 entry.just／vendor.just）若被新引擎改寫，由誰 commit（人手，CI 紅燈提醒）？", 640, 6, 940, 50))')
rep('p12.append(v("a4", "uA", LEAF(), "每個人下次打 just：\\n印記第一行 ≠ .version → install", 600, 290, 280, 50))', 'p12.append(v("a4", "uA", LEAF(), "每個人下次打工具指令：ensure 抓新版檔案\\n→ 印記第一行 ≠ .version → install", 600, 290, 280, 50).replace("fontSize=14", "fontSize=12"))')
rep('"已定：CI 深淺由專案決定；vendor_kit 出貨完整的契約檢查腳本與 renovate.json（只含 extends，指向 vendor_kit repo 內的共用 preset；GitLab 自架 renovate-runner），bootstrap 寫出，之後歸專案。"', '"已定：CI 深淺由專案決定；vendor_kit 出貨完整的契約檢查腳本（.vendor_kit/ci/check.sh）與 renovate.json（只含 extends，指向 vendor_kit repo 內的共用 preset；GitHub 裝 Renovate App、GitLab 自架 renovate-runner；檔案放置位置待 ci_bridge，issue #25），bootstrap 寫出，之後歸專案。"')
rep('"下次 just：.vendor_kit/.stamp 第一行\\n≠ .version 的 vendor_kit 行"', '"下次 just（ensure）：gen/.stamp 第一行\\n≠ .version 的 vendor_kit 行"')
rep('"用新版 vendor_kit image 跑 bootstrap\\n只重寫 vendor.just / tools.just / .stamp"', '"用新版引擎 image 跑 bootstrap（凍結的那一行）\\n重產 gen/ 與薄殼（baseline/ 不動）"')
rep('".vendor_kit/ 程式檔換新\\n（baseline/、justfile、.version 不動）"', '".vendor_kit/ 換新（gen/ 不進 git；薄殼進 git）\\nbaseline/、justfile、.version 不動"')
rep('"已定（雙軌一致）：先換自己：舊啟動器發現 vendor_kit 行變了 → 用新 image 跑 bootstrap（這個呼叫方式凍結為契約）重寫 .vendor_kit/ 程式檔（baseline/ 不動）→ 第一版：停下來、印「請重打一次指令」（just 已把 recipe 讀進記憶體，改了檔本次無效）。相容性（issue #14）：image LABEL 帶契約版本號，啟動器用 docker image inspect 比對。"',
    '"已定（雙軌一致）：先換自己：舊薄殼發現 vendor_kit 行變了 → 用新引擎 image 跑 bootstrap（薄殼裡那一行 docker run 永久凍結）重產 gen/ 與薄殼（baseline/ 不動）→ 第一版：停下來、印「請重打一次指令」（just 已把 recipe 讀進記憶體，改了檔本次無效）。乙版下工具 image 沒有引擎，所以不會有「新啟動器叫舊引擎」；相容性（issue #14）只剩「新引擎讀得懂舊 baseline／印記格式」，image LABEL 帶契約版本號。"')
rep(''' ("justfile / vendor.just / tools.just", "使用者自己的指令清單（第一行 mod? vendor_kit）／vendor_kit 的標準指令檔（just vendor_kit …）／依 .version 產生的工具指令清單；C 只換後兩者與 .stamp"),''',
    ''' ("justfile / 薄殼 / gen/", "使用者自己的指令清單（第一行 import '.vendor_kit/entry.just'）／進 git 的最小啟動器（entry.just、vendor.just：ensure＋一行 docker run）／引擎產生、不進 git 的其餘指令與 tools.just、.stamp；C 重產 gen/ 與薄殼"),''')
rep(''' ("bootstrap（在 C 裡）", "同第 10 頁的子命令，這裡只重寫 .vendor_kit/ 的程式檔"),''', ''' ("bootstrap（在 C 裡）", "同第 10 頁的子命令，這裡只重產 .vendor_kit/ 的薄殼與 gen/（不碰 justfile、.version、baseline/）"),''')

# ===================== 第 12 頁（契約）=====================
s, e_ = block('# ================= Page 12: 對外契約與 CI 隔離', '\n\ndoc = (')
src = src[:s] + open("p13_v57.py").read() + src[e_:]

open("gen57.py", "w").write(src)
print("ok")
