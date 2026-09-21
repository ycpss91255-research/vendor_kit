"""gen33 → gen34：整合 #20/#21/#22/#23/#24 定案（baseline 三方 diff、verify 比 /dist、flock、.version.local、.vendor_kit/ 線）"""
src = open("gen33.py").read()

def rep(old, new, count=1):
    global src
    assert src.count(old) == count, (src.count(old), old[:90])
    src = src.replace(old, new)

S12 = '.replace("fontSize=14", "fontSize=12")'
S11 = '.replace("fontSize=14", "fontSize=11")'

# ================= 頁 1 =================
rep('p1.append(v("user", "1", SW(YELLOW), "使用者", 40, VY, 140, 860))', 'p1.append(v("user", "1", SW(YELLOW), "使用者", 40, VY, 140, 900))')
rep('p1.append(v("u_out", "user", LEAF(), "畫面", 26, 810, 88, 40))', 'p1.append(v("u_out", "user", LEAF(), "畫面", 26, 850, 88, 40))')
rep('p1.append(v("vk", "1", PURPLE_SW, "vendor_kit（一個 container）", VX, VY, 570, 860))', 'p1.append(v("vk", "1", PURPLE_SW, "vendor_kit（一個 container）", VX, VY, 600, 900))')
rep('''p1.append(v("m_cli", "vk", SW(RED), "命令介面", 20, 50, 200, 140))
p1.append(v("cli_land", "m_cli", LEAF(), "install", 12, 45, 88, 40))
p1.append(v("cli_init", "m_cli", LEAF(), "init", 104, 45, 88, 40))
p1.append(v("cli_verify", "m_cli", LEAF(), "verify", 12, 92, 88, 40))
p1.append(v("cli_diff", "m_cli", LEAF(), "diff", 104, 92, 88, 40))''',
'''p1.append(v("m_cli", "vk", SW(RED), "命令介面", 20, 50, 292, 140))
p1.append(v("cli_land", "m_cli", LEAF(), "install", 12, 45, 88, 40))
p1.append(v("cli_init", "m_cli", LEAF(), "init", 104, 45, 88, 40))
p1.append(v("cli_verify", "m_cli", LEAF(), "verify", 196, 45, 88, 40))
p1.append(v("cli_diff", "m_cli", LEAF(), "diff", 12, 92, 88, 40))
p1.append(v("cli_accept", "m_cli", LEAF(), "accept", 104, 92, 88, 40))
p1.append(v("cli_boot", "m_cli", LEAF(), "bootstrap", 196, 92, 88, 40))''')
rep('p1.append(v("m_tpl", "vk", SW(RED), "模板", 20, 480, 200, 130))', 'p1.append(v("m_tpl", "vk", SW(RED), "模板", 20, 520, 200, 130))')
rep('p1.append(v("m_diff", "vk", SW(RED), "差異比對", 20, 670, 200, 130))', 'p1.append(v("m_diff", "vk", SW(RED), "差異比對", 20, 710, 200, 130))')
rep('''p1.append(v("df_cmp", "m_diff", LEAF(), "比對", 12, 45, 88, 40))
p1.append(v("df_patch", "m_diff", LEAF(), "產生差異", 104, 45, 88, 40))''',
'''p1.append(v("df_cmp", "m_diff", LEAF(), "三方分類", 12, 45, 88, 40))
p1.append(v("df_patch", "m_diff", LEAF(), "產生差異", 104, 45, 88, 40))''')
rep('''p1.append(v("m_write", "vk", SW(RED), "專案檔案存取", 300, 250, 200, 170))
p1.append(v("wr_copy", "m_write", LEAF(), "寫入", 12, 45, 88, 40))
p1.append(v("wr_read", "m_write", LEAF(), "讀回", 104, 45, 88, 40))
p1.append(v("wr_perm", "m_write", LEAF(), "權限設定", 12, 92, 88, 40))
p1.append(v("wr_atomic", "m_write", LEAF(), "整批替換", 104, 92, 88, 40))
p1.append(v("m_stamp", "vk", SW(RED, 16), "印記", 390, 480, 110, 130))
p1.append(v("st_hash", "m_stamp", LEAF(), "指紋計算", 11, 45, 88, 40))
p1.append(v("st_cmp", "m_stamp", LEAF(), "比對", 11, 85, 88, 40))
p1.append(v("m_report", "vk", SW(RED), "回報", 300, 670, 200, 130))''',
'''p1.append(v("m_write", "vk", SW(RED), "專案檔案存取", 300, 250, 292, 220))
p1.append(v("wr_copy", "m_write", LEAF(), "寫入", 12, 45, 88, 40))
p1.append(v("wr_read", "m_write", LEAF(), "讀回", 104, 45, 88, 40))
p1.append(v("wr_perm", "m_write", LEAF(), "權限設定", 196, 45, 88, 40))
p1.append(v("wr_atomic", "m_write", LEAF(), "整批替換", 12, 92, 88, 40))
p1.append(v("wr_base", "m_write", LEAF(), "讀寫基準", 104, 92, 88, 40))
p1.append(v("m_stamp", "vk", SW(RED, 16), "印記與比對", 392, 520, 200, 130))
p1.append(v("st_tree", "m_stamp", LEAF(), "兩棵樹比對", 12, 45, 88, 40))
p1.append(v("st_hash", "m_stamp", LEAF(), "產生印記", 104, 45, 88, 40))
p1.append(v("st_cmp", "m_stamp", LEAF(), "讀已裝版本", 12, 85, 88, 40))
p1.append(v("m_report", "vk", SW(RED), "回報", 300, 710, 200, 130))''')
rep('p1.append(v("proj", "1", SW(GREEN), "專案 repo 的目錄", 1140, VY, 200, 860))', 'p1.append(v("proj", "1", SW(GREEN), "專案 repo 的目錄", 1140, VY, 200, 900))')
rep('''p1.append(v("p_stamp", "proj", LEAF(), ".<name>/\\n.stamp", 56, 250, 88, 40))
p1.append(v("p_base", "proj", LEAF(), ".<name>/", 56, 306, 88, 40))
p1.append(v("p_user", "proj", LEAF(), "使用者檔案", 56, 376, 88, 40))''',
'''p1.append(v("p_stamp", "proj", LEAF(), ".<name>/\\n.stamp", 56, 250, 88, 40))
p1.append(v("p_base", "proj", LEAF(), ".<name>/", 56, 300, 88, 40))
p1.append(v("p_user", "proj", LEAF(), "使用者檔案", 56, 350, 88, 40))
p1.append(v("p_bl", "proj", LEAF(), "基準\\n（baseline）", 56, 400, 88, 40))''')
rep('p1.append(e("a6", "m_list", "m_write", "dist 全部", (1, 0.3), (0, 0.3)))', 'p1.append(e("a6", "m_list", "m_write", "dist 全部（安裝寫入、verify 比對）", (1, 0.3), (0, 0.232)))')
rep('p1.append(e("a9", "m_write", "m_stamp", "檔案內容、\\n舊印記", (0.55, 1), (0.1818, 0), vert=True))',
    'p1.append(e("a9", "m_write", "m_stamp", "兩棵樹的內容\\n（/dist、.<name>/）", (0.438, 1), (0.28, 0), vert=True))')
rep('p1.append(e("a9b", "m_stamp", "m_write", "新指紋、\\n比對結果", (0.9, 0), (0.945, 1), vert=True))',
    'p1.append(e("a9b", "m_stamp", "m_write", "印記、\\n已裝版本", (0.9, 0), (0.9315, 1), vert=True))')
rep('p1.append(e("a10", "m_write", "p_stamp", "印記檔", (1, 0.1176), (0, 0.5), both=True))', 'p1.append(e("a10", "m_write", "p_stamp", "印記檔", (1, 0.0909), (0, 0.5), both=True))')
rep('p1.append(e("a11", "m_write", "p_base", "dist 全部", (1, 0.4471), (0, 0.5), both=True))', 'p1.append(e("a11", "m_write", "p_base", "dist 全部", (1, 0.318), (0, 0.5), both=True))')
rep('p1.append(e("a12", "m_write", "p_user", "初始檔（init 時）", (1, 0.8), (0, 0.25)))', 'p1.append(e("a12", "m_write", "p_user", "初始檔（init 時）", (1, 0.5), (0, 0.25)))')
rep('p1.append(e("a12b", "p_user", "m_write", "現有內容（diff 時）", (0, 0.76), (1, 0.92), vert="below"))',
    '''p1.append(e("a12b", "p_user", "m_write", "現有內容（diff 時）", (0, 0.76), (1, 0.5927), vert="below"))
p1.append(e("a12c", "m_write", "p_bl", "基準（init／accept 寫，diff 讀）", (1, 0.7727), (0, 0.5), both=True))''')
rep('''exitX=0.3;exitY=1;exitDx=0;exitDy=0;entryX=0.9;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="m_write" target="m_diff"><mxGeometry x="0.55" relative="1" as="geometry"><Array as="points"><mxPoint x="840" y="780"/><mxPoint x="680" y="780"/>''',
    '''exitX=0.3014;exitY=1;exitDx=0;exitDy=0;entryX=0.9;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="m_write" target="m_diff"><mxGeometry x="0.55" relative="1" as="geometry"><Array as="points"><mxPoint x="868" y="800"/><mxPoint x="680" y="800"/>''')
rep('<mxCell id="a13" value="使用者檔案" style="', '<mxCell id="a13" value="使用者檔案、基準" style="')
rep('p1.append(e("a15", "m_stamp", "m_report", "檢查結果", (0.5, 1), (0.725, 0), vert=True))', 'p1.append(e("a15", "m_stamp", "m_report", "比對結果", (0.265, 1), (0.725, 0), vert=True))')
rep('p1.append(e("a16", "m_diff", "m_report", "差異", (1, 0.5), (0, 0.5)))', 'p1.append(e("a16", "m_diff", "m_report", "差異、結束狀態", (1, 0.5), (0, 0.5)))')
rep('p1 += legend("p1", 40, 1060,', 'p1 += legend("p1", 40, 1100,')
rep('p1 += terms("p1", 40, 1170, [', 'p1 += terms("p1", 40, 1210, [')
rep(''' ("install / init / verify / diff", "四個子命令：安裝 dist 到 .<name>/／第一次建立使用者檔／檢查 .<name>/ 沒被改／升級後比對模板差異"),
 ("結束狀態", "程式結束時回報成功或失敗，啟動器據此決定要不要繼續執行"),''',
''' ("install / init / verify / diff / accept / bootstrap", "子命令：安裝 dist 到 .<name>/／第一次建立使用者檔／檢查 .<name>/ 沒被改／升級後三方比對／把新版模板存成基準／第一次寫出啟動器（第 10 頁）"),
 ("結束狀態", "程式結束時回報的數字：0 成功、非 0 失敗；diff 另有 0 沒差異／1 工具有改／2 可能重疊；啟動器據此決定要不要繼續"),
 ("兩棵樹比對", "verify 的做法：把 image 內的 /dist 跟專案的 .<name>/ 逐檔比（檔案集合、內容指紋、執行位單向、型別），多的少的改的都算失敗"),
 ("基準（baseline）", ".vendor_kit/baseline/<name>/：你上次確認過的那版模板副本；diff 用它分出「工具改了什麼」「你改了什麼」；init／accept 寫、人不改"),''')
rep(''' ("印記檔", ".<name>/.stamp：版本 + 每個檔案的指紋；verify 用它判斷有沒有被手改"),''',
    ''' ("印記檔", ".<name>/.stamp：第一行 = 裝的 image（啟動器傳進來的 .version 字串），之後每檔指紋（給人追溯用）；verify 只用第一行判斷要不要重裝，內容以 image 為準"),''')

# ================= 頁 2 =================
rep('''p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器與版本檔（進 git）", 20, 80, 300, 175))
p1b.append(v("p_vk", "pa", LEAF(), ".vendor_kit/\\n（標準指令，justfile import 它）", 12, 122, 180, 44).replace("fontSize=14", "fontSize=12"))
p1b.append(v("pa_t", "pa", TEXT(11) + "align=left;", ".version 一行 = 一個工具 = 一個 .<name>/", 12, 42, 276, 24))
p1b.append(v("p_ver", "pa", LEAF(), ".version", 12, 72, 90, 40))
p1b.append(v("p_just", "pa", LEAF(), "justfile", 200, 72, 80, 40))
p1b.append(v("p_eng", "proj", PURPLE_LEAF, "安裝容器（<name>-dist:vX）", 20, 300, 300, 60))
p1b.append(v("p_eng_t", "proj", TEXT(11) + "align=left;", "以使用者身分執行，跑完即刪", 20, 362, 200, 20))''',
'''p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器與版本檔（進 git，.version.local 除外）", 20, 80, 340, 205))
p1b.append(v("pa_t", "pa", TEXT(11) + "align=left;", ".version 一行 = 一個工具 = 一個 .<name>/；.version.local 有同名那行就優先（本機開發用，第 4 頁）", 12, 40, 316, 30))
p1b.append(v("p_ver", "pa", LEAF(), ".version", 12, 74, 90, 40))
p1b.append(v("p_vl", "pa", FILE, ".version.local\\n（可選，不進 git）", 112, 74, 120, 40).replace("fontSize=14", "fontSize=11"))
p1b.append(v("p_just", "pa", LEAF(), "justfile", 250, 74, 78, 40))
p1b.append(v("p_vk", "pa", LEAF(), ".vendor_kit/（啟動器本體）\\nvendor.just、tools.just、.stamp、baseline/<name>/", 12, 142, 316, 50).replace("fontSize=14", "fontSize=12"))
p1b.append(v("p_eng", "proj", PURPLE_LEAF, "安裝容器（<name>-dist:vX）", 20, 330, 300, 60))
p1b.append(v("p_eng_t", "proj", TEXT(11) + "align=left;", "以使用者身分執行，跑完即刪", 20, 392, 300, 20))''')
rep('p1b.append(v("pc_t", "pc", TEXT(11), "每次 upgrade 整批覆蓋\\n印記檔 = 版本 + 每檔指紋", 6, 88, 210, 32))',
    'p1b.append(v("pc_t", "pc", TEXT(11), "每次 upgrade 整批覆蓋；verify 拿它跟 image 內\\n的 dist 比；印記檔 = 裝的 image + 每檔指紋", 6, 88, 210, 32))')
rep('''p1b.append(e("f7", "p_ver", "p_just", "工具名、版本", (1, 0.5), (0, 0.5)))
p1b.append(e("f8", "p_just", "p_eng", "工具名、版本、使用者身分、專案路徑", (0.5, 1), (0.8, 0), vert=True, pos=0.6))''',
'''p1b.append(e("f7", "p_ver", "p_vk", "工具名、版本", (0.5, 1), (0.142, 0), vert=True))
p1b.append(e("f7c", "p_vl", "p_vk", "有就優先", (0.5, 1), (0.506, 0), dashed=True, vert=True))
p1b.append(e("f7b", "p_just", "p_vk", "import", (0.5, 1), (0.877, 0), vert=True))
p1b.append(e("f8", "p_vk", "p_eng", "工具名、版本、使用者身分、專案路徑", (0.5, 1), (0.5667, 0), vert=True))''')
rep(''' (".version", "專案裡的 TOML 檔，一個工具一行 name = \\"image:tag@sha256:…\\"；name 決定安裝目錄 .<name>/"),''',
    ''' (".version", "專案裡的 TOML 檔，一個工具一行 name = \\"image:tag@sha256:…\\"；name 決定安裝目錄 .<name>/"),
 (".version.local", "跟 .version 同格式的覆蓋檔，不進 git；開發工具本身時用它把某個工具指到本機路徑（第 4 頁）"),
 ("baseline（基準）", ".vendor_kit/baseline/<name>/：上次確認過的模板副本，just diff 用它分出工具改了什麼、你改了什麼；vendor_kit 寫，人不改"),''')
rep(''' ("just / justfile / .vendor_kit/", "just = 主機的指令跑器；.vendor_kit/ = 啟動器本體（vendor_kit 寫出，人不改）；justfile = 專案自己的指令清單，第一行 import .vendor_kit/"),''',
    ''' ("just / justfile / .vendor_kit/", "just = 主機的指令跑器；.vendor_kit/ = 啟動器本體（vendor_kit 寫出，人不改；升級只換 vendor.just／tools.just／.stamp，baseline/ 不動）；justfile = 專案自己的指令清單，第一行 import .vendor_kit/"),''')
rep(''' ("install / init / verify / diff", "安裝容器的四個子命令：把 dist 裝進 .<name>/ 並寫印記檔／第一次建立初始檔／檢查 .<name>/ 沒被手改／升級後比對新版模板"),
])''', ''' ("install / init / verify / diff / accept", "安裝容器的子命令：把 dist 裝進 .<name>/ 並寫印記檔／第一次建立初始檔／拿 .<name>/ 跟 image 內的 dist 比／升級後三方比對／把新版模板存成基準"),
])''')

# ================= 頁 3 =================
rep('p2.append(v("a_l1", "bA", LEAF(), "讀 .version\\n（一行一個工具，逐行做）", 380, 75, 140, 40).replace("fontSize=14", "fontSize=12"))',
    'p2.append(v("a_l1", "bA", LEAF(), "讀版本檔（.version.local 優先，\\n否則 .version）一行一個工具", 380, 75, 140, 40).replace("fontSize=14", "fontSize=11"))')
rep('p2.append(v("a_c2", "bA", PURPLE_LEAF, "init\\n照 init.toml 複製初始檔（已存在則跳過）", 800, 165, 340, 60))',
    'p2.append(v("a_c2", "bA", PURPLE_LEAF, "init\\n照 init.toml 複製初始檔（已存在：warn、不覆蓋）\\n並把這版模板存成基準", 800, 165, 340, 60).replace("fontSize=14", "fontSize=13"))')
rep('p2.append(v("a_p2", "bA", FILE, "Dockerfile / entrypoint / hooks…\\n（新；之後由你維護）", 1240, 165, 200, 60))',
    'p2.append(v("a_p2", "bA", FILE, "Dockerfile / entrypoint / hooks…\\n（新；之後由你維護）\\n＋ .vendor_kit/baseline/<name>/", 1240, 165, 200, 60).replace("fontSize=14", "fontSize=12"))')
rep('p2.append(v("b_l1", "bB", LEAF(), "讀 .version\\n（一行一個工具，逐行做）", 360, 75, 140, 40).replace("fontSize=14", "fontSize=12"))',
    'p2.append(v("b_l1", "bB", LEAF(), "讀版本檔（.version.local 優先，\\n否則 .version）一行一個工具", 360, 75, 140, 40).replace("fontSize=14", "fontSize=11"))')
rep('p2.append(v("b_c1", "bB", PURPLE_LEAF, "verify\\n.<name>/ 每檔指紋是否仍等於印記", 800, 170, 340, 60))',
    'p2.append(v("b_c1", "bB", PURPLE_LEAF, "verify\\n.<name>/ 跟 image 內的 dist 逐檔比（缺、多、改都算）", 800, 170, 340, 60).replace("fontSize=14", "fontSize=13"))')
rep('p2.append(v("b_err", "bB", ELLIPSE(RED), "中止：.<name>/ 被改過\\n刪除 .<name>/ 再 build 即自動重裝", 40, 285, 260, 60))',
    'p2.append(v("b_err", "bB", ELLIPSE(RED), "中止：.<name>/ 被改過（列出哪些檔）\\n刪除 .<name>/ 再 build 即自動重裝", 40, 285, 260, 60).replace("fontSize=14", "fontSize=12"))')
rep('band("bC", "升級：Renovate 開的 PR 被 merge", 830, 300)', 'band("bC", "升級：Renovate 開的 PR 被 merge", 830, 390)')
rep('p2.append(v("c_c2", "bC", PURPLE_LEAF, "diff\\nimage 內的新版模板 vs 你的初始檔", 800, 155, 340, 60))',
    'p2.append(v("c_c2", "bC", PURPLE_LEAF, "diff（三方）\\n基準 vs image 內的新版模板 vs 你的初始檔\\n只印出「工具改了什麼」「你改了什麼」，不改檔", 800, 155, 340, 60).replace("fontSize=14", "fontSize=12"))')
rep('p2.append(v("c_p2", "bC", FILE, "Dockerfile 等（你的）", 1240, 165, 200, 40))', 'p2.append(v("c_p2", "bC", FILE, "Dockerfile 等（你的）", 1240, 150, 200, 40))')
rep('p2.append(v("c_u3", "bC", ELLIPSE(GREEN), "看差異，自己決定\\n要不要改", 60, 230, 180, 55))',
    '''p2.append(v("c_u3", "bC", ELLIPSE(GREEN), "看差異，自己決定\\n要不要改", 60, 230, 180, 55))
p2.append(v("c_u4", "bC", ELLIPSE(GREEN), "跟進完 → just accept <name>", 60, 310, 200, 50))
p2.append(v("c_c3", "bC", PURPLE_LEAF, "accept\\n把 image 內的新版模板存成基準", 800, 305, 340, 60))
p2.append(v("c_p3", "bC", FILE, ".vendor_kit/baseline/<name>/\\n（進 git，人不改）", 1240, 310, 200, 50))''')
rep('p2.append(e("ce4", "c_p2", "c_c2", "讀", (0, 0.5), (1, 0.5)))',
    '''p2.append(e("ce4", "c_p2", "c_c2", "讀", (0, 0.5), (1, 0.25)))
p2.append('<mxCell id="ce4b" value="讀" style="' + EDGE + 'exitX=0;exitY=0.2;exitDx=0;exitDy=0;entryX=1;entryY=0.8;entryDx=0;entryDy=0;" edge="1" parent="bC" source="c_p3" target="c_c2"><mxGeometry x="0.3" relative="1" as="geometry"><Array as="points"><mxPoint x="1190" y="320"/><mxPoint x="1190" y="203"/></Array></mxGeometry></mxCell>')
p2.append(e("ce6", "c_u4", "c_c3", "", (1, 0.5), (0, 0.5)))
p2.append(e("ce7", "c_c3", "c_p3", "寫入", (1, 0.5), (0, 0.5)))''')
rep('''p2.append(v("p2n", "1", NOTE, "紫框 = 子命令：install（第一次、版本改變時）、init（只有第一次）、verify（已安裝且版本一致時）、diff（升級後由使用者呼叫）。\\n沒有 Renovate 時用 just upgrade 手動：改 .version → 立即 install → diff（細節待議）。", 20, 1150, 1620, 50))
p2 += legend_flow("p2", 40, 1220, files=True, note=True, dashed=True)
p2 += terms("p2", 40, 1330, [''',
'''p2.append(v("p2n", "1", NOTE, "紫框 = 子命令：install（第一次、版本改變時）、init（只有第一次）、verify（已安裝且版本一致時）、diff／accept（升級後由使用者呼叫）。\\n沒有 Renovate 時用 just upgrade 手動：改 .version → 立即 install → diff（細節待議）。\\n同一專案兩個 just 同時跑怎麼互斥：方案審中（issue #24），第 5 頁先留一格。", 20, 1240, 1620, 60))
p2 += legend_flow("p2", 40, 1320, files=True, note=True, dashed=True)
p2 += terms("p2", 40, 1430, [''')
rep(''' ("印記", ".<name>/.stamp：install 寫下的「第一行 = 裝的 image，之後每行 = 一個檔的指紋」；日常每次 just 都拿它比對"),''',
    ''' ("印記", ".<name>/.stamp：install 寫下的「第一行 = 裝的 image，之後每行 = 一個檔的指紋」；啟動器只拿第一行判斷要不要重裝，內容以 image 內的 dist 為準"),
 ("基準 / accept", ".vendor_kit/baseline/<name>/ = 上次確認過的模板副本；diff 靠它分出工具改了什麼、你改了什麼；just accept <name> 把新版模板存成基準"),
 (".version.local", "跟 .version 同格式、不進 git 的覆蓋檔；開發工具本身時用（第 4 頁），平常沒有這個檔"),''')
rep(''' ("install / init / verify / diff", "四個子命令：安裝 dist 到 .<name>/ 並寫印記／第一次建立初始檔／檢查 .<name>/ 沒被手改／升級後比對模板差異"),
 ("sha256 / 容器"''', ''' ("install / init / verify / diff / accept", "子命令：安裝 dist 到 .<name>/ 並寫印記／第一次建立初始檔／拿 .<name>/ 跟 image 內的 dist 比／升級後三方比對／存新基準"),
 ("sha256 / 容器"''')

# ================= 頁 4 =================
rep('p3.append(v("c8", "up", RHOMBUS, "使用者執行 just diff：\\n新版模板 vs 你的初始檔有差異？", 70, 240, 280, 100))',
    'p3.append(v("c8", "up", RHOMBUS, "使用者執行 just diff（三方）：\\n工具改了什麼？你改了什麼？\\n有差異？", 70, 240, 280, 100).replace("fontSize=14", "fontSize=12"))')
rep('p3.append(v("c9", "up", LEAF(), "顯示差異，使用者自行決定是否修改\\n（工具不碰使用者檔案）", 20, 370, 380, 60))',
    'p3.append(v("c9", "up", LEAF(), "顯示差異，使用者自行決定是否跟進（工具不碰使用者檔案）\\n跟進完打 just accept <name>：新版模板存成基準", 20, 370, 380, 60).replace("fontSize=14", "fontSize=12"))')
rep('''p3.append(v("dev", "1", SW(NEUTRAL), "本機開發模式（改工具本身時；待設計）", 800, 510, 420, 150))
p3.append(v("c31", "dev", LEAF(), "候選做法：.version 暫時指向本機的工具原始碼（而非 GHCR image）\\n改工具不必每次發佈 image 就能在專案裡測", 20, 50, 380, 80))
p3 += legend_flow("p3", 40, 720, purple=False, startend=False, err=False, note=True)
p3 += terms("p3", 40, 830, [''',
'''p3.append(v("dev", "1", SW(NEUTRAL), "本機開發模式（改工具本身時，不必每改一行就出 image）", 800, 510, 420, 330))
p3.append(v("c31", "dev", LEAF(), "just dev <name> ../tool\\n→ 寫 .version.local（不進 git）：<name> = \\"path:../tool\\"", 20, 50, 380, 50).replace("fontSize=14", "fontSize=12"))
p3.append(v("c32", "dev", LEAF(), "之後每次 just：用 vendor_kit image 把 ../tool/dist 掛進來當 dist 安裝\\n印記第一行寫 dev:../tool", 20, 115, 380, 50).replace("fontSize=14", "fontSize=12"))
p3.append(v("c33", "dev", LEAF(), "看到 dev: 就不做完整性檢查，只印醒目警告、重新複製 dist", 20, 180, 380, 50).replace("fontSize=14", "fontSize=12"))
p3.append(v("c34", "dev", LEAF(), "just undev <name> → 刪那行 → 下次 just 回到 .version 的正式 image 重裝", 20, 245, 380, 50).replace("fontSize=14", "fontSize=12"))
p3.append(e("c35", "c31", "c32")); p3.append(e("c36", "c32", "c33")); p3.append(e("c37", "c33", "c34"))
p3 += legend_flow("p3", 40, 880, purple=False, startend=False, err=False, note=True)
p3 += terms("p3", 40, 990, [''')
rep(''' ("<name> / just", "<name> = .version 裡的工具名，安裝目錄就叫 .<name>/；just = 主機上的指令跑器，使用者打 just <指令>"),
])''', ''' ("<name> / just", "<name> = .version 裡的工具名，安裝目錄就叫 .<name>/；just = 主機上的指令跑器，使用者打 just <指令>"),
 (".version.local / dev:", "跟 .version 同格式、不進 git 的覆蓋檔，有它那行就優先；印記第一行的 dev: 前綴 = 這個 .<name>/ 來自本機路徑，不是正式 image"),
 ("基準 / accept", "基準 = .vendor_kit/baseline/<name>/ 裡上次確認過的模板副本；just accept <name> = 看完差異後把新版模板存成基準"),
])''')

# ================= 頁 5：整段重寫 =================
start = src.index("# ================= Page 5: 流程：安裝工具 =================")
end = src.index("# ================= Page 7: 原型對照 =================")
p5 = r'''# ================= Page 5: 流程：vendor_kit 內部 =================
p4 = [v("title", "1", TITLE, "流程：vendor_kit 內部——五個子命令（install 是核心）；全部在容器內執行；bootstrap 見第 10 頁", 40, 20, 1200, 30)]
# install
p4.append(v("install", "1", SW(NEUTRAL), "install（核心：把 dist/ 放進 .<name>/）", 20, 60, 460, 1010))
p4.append(v("l0", "install", ELLIPSE(GREEN), "開始 install", 150, 50, 160, 50))
p4.append(v("l1", "install", NOTE, "取得安裝權（同一專案同時只能一個 install；\n怎麼互斥方案審中，issue #24）", 90, 130, 280, 50))
p4.append(v("l2", "install", LEAF(), "重讀版本檔與印記第一行", 130, 330, 200, 40))
p4.append(v("l3", "install", RHOMBUS, "印記已是\n目標版本？", 140, 400, 180, 80))
p4.append(v("l_skip", "install", LEAF(), "跳過複製\n（別人剛裝好）", 15, 520, 190, 50).replace("fontSize=14", "fontSize=12"))
p4.append(v("l4", "install", LEAF(), "清掉殘留的 .<name>.tmp.*", 130, 520, 200, 40))
p4.append(v("l5", "install", LEAF(), "複製 dist/ 到亂數名暫存目錄", 130, 590, 200, 40))
p4.append(v("l6", "install", LEAF(), "寫印記（--self 的版本＋每檔指紋）", 130, 660, 200, 40).replace("fontSize=14", "fontSize=12"))
p4.append(v("l7", "install", LEAF(), "刪舊 .<name>/、暫存目錄改名\n（整批覆蓋）", 130, 730, 200, 60).replace("fontSize=14", "fontSize=12"))
p4.append(v("l8", "install", LEAF(), "釋放安裝權", 130, 820, 200, 40))
p4.append(v("l9", "install", ELLIPSE(GREEN), "成功結束", 150, 890, 160, 40))
p4.append(v("ln", "install", NOTE, "任一步失敗即中止，舊 .<name>/ 不動；啟動器不會執行 .<name>/ 內的腳本。\n主機要能用在 Linux、macOS Docker Desktop、Windows WSL2（notes §2）。", 30, 950, 400, 50))
p4.append(e("le0", "l0", "l1")); p4.append(e("le1", "l1", "l2"))
p4.append(e("le3", "l2", "l3"))
p4.append('<mxCell id="le_skip" value="是" style="' + EDGE + 'align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="install" source="l3" target="l_skip"><mxGeometry x="0.4" relative="1" as="geometry"><Array as="points"><mxPoint x="110" y="440"/></Array></mxGeometry></mxCell>')
p4.append(e("le4", "l3", "l4", "否", (0.5, 1), (0.5, 0), vert=True))
p4.append(e("le5", "l4", "l5")); p4.append(e("le6", "l5", "l6")); p4.append(e("le7", "l6", "l7")); p4.append(e("le8", "l7", "l8")); p4.append(e("le9", "l8", "l9"))
p4.append('<mxCell id="le_skip2" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="install" source="l_skip" target="l8"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="110" y="840"/></Array></mxGeometry></mxCell>')
# init
IX = 500
p4.append(v("init", "1", SW(NEUTRAL), "init（第一次：建立使用者檔＋存基準）", IX, 60, 480, 780))
p4.append(v("i0", "init", ELLIPSE(GREEN), "開始 init", 160, 50, 160, 50))
p4.append(v("i1", "init", LEAF(), "讀 init.toml", 140, 130, 200, 40))
p4.append(v("i2", "init", RHOMBUS, "還有項目？", 150, 200, 180, 80))
p4.append(v("i3", "init", LEAF(), "取下一項\n（image 內由 src 指定的檔 → 專案內的 dest）", 80, 312, 320, 56))
p4.append(v("i4", "init", RHOMBUS, "dest 已存在？", 150, 390, 180, 80))
p4.append(v("i5", "init", LEAF(), "warn：已存在，不覆蓋\n（仍把這版模板存成基準）", 40, 510, 180, 50).replace("fontSize=14", "fontSize=12"))
p4.append(v("i6", "init", LEAF(), "從 dist/ 複製建立\n＋ 存一份到基準", 260, 510, 180, 50).replace("fontSize=14", "fontSize=12"))
p4.append(v("i8", "init", LEAF(), "繼續下一項", 140, 600, 200, 36))
p4.append(v("i7", "init", ELLIPSE(GREEN), "成功結束", 160, 670, 160, 40))
p4.append(v("in", "init", NOTE, "dest 已被另一個工具的 init.toml 用到 → 報錯中止（兩個工具不能搶同一個檔）。基準 = .vendor_kit/baseline/<name>/", 30, 725, 420, 44))
p4.append(e("ie0", "i0", "i1")); p4.append(e("ie1", "i1", "i2"))
p4.append(e("ie2", "i2", "i3", "有", (0.5, 1), (0.5, 0), vert=True))
p4.append(e("ie3", "i3", "i4"))
p4.append(e("ie4", "i4", "i5", "已有", (0, 0.5), (0.5, 0), vert=True))
p4.append(e("ie5", "i4", "i6", "沒有", (1, 0.5), (0.5, 0), vert=True))
p4.append('<mxCell id="ie6" value="沒有了" style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i2" target="i7"><mxGeometry x="-0.85" relative="1" as="geometry"><Array as="points"><mxPoint x="460" y="240"/><mxPoint x="460" y="690"/></Array></mxGeometry></mxCell>')
p4.append(e("ib1", "i5", "i8", "", (0.5, 1), (0.25, 0)))
p4.append(e("ib2", "i6", "i8", "", (0.5, 1), (0.75, 0)))
p4.append('<mxCell id="ib3" value="" style="' + EDGE + 'exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="init" source="i8" target="i2"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="15" y="618"/><mxPoint x="15" y="240"/></Array></mxGeometry></mxCell>')
# verify
VX2 = 1000
p4.append(v("verify", "1", SW(NEUTRAL), "verify（每次 just 前的守門：.<name>/ 跟 image 內的 dist 一致？）", VX2, 60, 460, 720))
p4.append(v("v0", "verify", ELLIPSE(GREEN), "開始 verify", 150, 50, 160, 50))
p4.append(v("v1", "verify", LEAF(), "讀印記第一行（已裝版本）", 130, 130, 200, 40))
p4.append(v("v2", "verify", RHOMBUS, "印記第一行 = 啟動器\n給的 .version 字串？", 130, 200, 200, 80).replace("fontSize=14", "fontSize=12"))
p4.append(v("v3", "verify", LEAF(), "比對兩棵樹：image 內 /dist vs .<name>/\n檔案集合、sha256、執行位（單向：該 +x 的仍 +x）、型別", 130, 320, 200, 60).replace("fontSize=14", "fontSize=12"))
p4.append(v("v4", "verify", RHOMBUS, "完全一致？", 140, 420, 180, 80))
p4.append(v("v_bad1", "verify", ELLIPSE(RED), "版本不符：回報\n啟動器改跑 install", 15, 560, 140, 50).replace("fontSize=14", "fontSize=11"))
p4.append(v("v_ok", "verify", ELLIPSE(GREEN), "通過", 160, 560, 140, 50))
p4.append(v("v_bad2", "verify", ELLIPSE(RED), "失敗：列出缺／多／\n被改的檔，中止", 325, 560, 130, 60).replace("fontSize=14", "fontSize=11"))
p4.append(v("vn", "verify", NOTE, "多餘的檔也算失敗：.<name>/ 是整批替換的目錄，不該有別的東西。失敗不自動重裝（會無聲毀掉手改），提示刪掉重跑 just。", 20, 640, 420, 50))
p4.append(e("ve0", "v0", "v1")); p4.append(e("ve1", "v1", "v2"))
p4.append('<mxCell id="ve_b1" value="否" style="' + EDGE + 'exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="verify" source="v2" target="v_bad1"><mxGeometry x="-0.8" relative="1" as="geometry"><Array as="points"><mxPoint x="85" y="240"/></Array></mxGeometry></mxCell>')
p4.append(e("ve2", "v2", "v3", "是", (0.5, 1), (0.5, 0), vert=True))
p4.append(e("ve3", "v3", "v4"))
p4.append(e("ve4", "v4", "v_ok", "是", (0.5, 1), (0.5, 0), vert=True))
p4.append('<mxCell id="ve_b2" value="否" style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="verify" source="v4" target="v_bad2"><mxGeometry x="-0.6" relative="1" as="geometry"><Array as="points"><mxPoint x="390" y="460"/></Array></mxGeometry></mxCell>')
# diff
DX = 1480
p4.append(v("diff", "1", SW(NEUTRAL), "diff（升級後：三方比對，只印不改）", DX, 60, 560, 600))
p4.append(v("d0", "diff", ELLIPSE(GREEN), "開始 diff", 80, 50, 160, 50))
p4.append(v("d1", "diff", RHOMBUS, "有基準？\n（baseline/<name>/）", 60, 130, 200, 80).replace("fontSize=14", "fontSize=12"))
p4.append(v("d2", "diff", LEAF(), "對每個初始檔分類：沒人改／只有工具改／\n只有你改／兩邊都改／你已套上相同內容", 20, 250, 280, 60).replace("fontSize=14", "fontSize=12"))
p4.append(v("d_two", "diff", LEAF(), "二方：新版模板 vs 你的檔\n並提示「無基準」", 320, 250, 220, 60).replace("fontSize=14", "fontSize=12"))
p4.append(v("d3", "diff", LEAF(), "印兩份：基準→新版（工具改了）、\n基準→你的（你改了）；重疊處標「可能重疊」", 20, 340, 280, 60).replace("fontSize=14", "fontSize=12"))
p4.append(v("d4", "diff", ELLIPSE(GREEN), "結束（不改任何檔）\n結束狀態 0 沒差異／1 工具有改／2 可能重疊", 10, 440, 300, 60).replace("fontSize=14", "fontSize=12"))
p4.append(v("dn", "diff", NOTE, "第一版只做檔案層級分類；行級精確判定（自寫 diff3）第二版。", 20, 520, 520, 40))
p4.append(e("de0", "d0", "d1"))
p4.append(e("de1", "d1", "d2", "有", (0.5, 1), (0.5, 0), vert=True))
p4.append(e("de2", "d1", "d_two", "沒有", (1, 0.5), (0.5, 0), vert=True))
p4.append(e("de3", "d2", "d3")); p4.append(e("de4", "d3", "d4"))
p4.append('<mxCell id="de5" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="diff" source="d_two" target="d4"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="430" y="470"/></Array></mxGeometry></mxCell>')
# accept
AX = 2060
p4.append(v("accept", "1", SW(NEUTRAL), "accept（看完 diff 後：新版模板存成基準）", AX, 60, 420, 600))
p4.append(v("a0", "accept", ELLIPSE(GREEN), "開始 accept", 130, 50, 160, 50))
p4.append(v("a1", "accept", NOTE, "取得安裝權（跟 install 同一套，審中）", 110, 130, 200, 40))
p4.append(v("a2", "accept", LEAF(), "取 image 內的新版模板\n（init.toml 列的檔）", 110, 200, 200, 50))
p4.append(v("a3", "accept", LEAF(), "寫進 .vendor_kit/baseline/<name>/\n＋ metadata（image、每檔指紋）", 100, 280, 220, 60).replace("fontSize=14", "fontSize=12"))
p4.append(v("a4", "accept", LEAF(), "釋放安裝權", 110, 370, 200, 40))
p4.append(v("a5", "accept", ELLIPSE(GREEN), "結束（基準 = 這版）", 110, 440, 200, 50))
p4.append(v("an", "accept", NOTE, "語意：「這版我全看過了」。寫的是新版模板，不是你的檔；diff 結尾只提示、不會問你。", 20, 520, 380, 50))
p4.append(e("ae0", "a0", "a1")); p4.append(e("ae1", "a1", "a2")); p4.append(e("ae2", "a2", "a3")); p4.append(e("ae3", "a3", "a4")); p4.append(e("ae4", "a4", "a5"))
p4.append(v("p4n", "1", NOTE, "已定案：verify 比 image 內的 /dist 而不是印記（issue #23）；diff 三方（#22）。安裝權怎麼互斥審中（#24，要同時能用在 Linux／macOS／WSL2）。本機開發模式見第 4 頁（#21）。", 20, 1090, 1500, 40))
p4 += legend_flow("p4", 40, 1150, purple=False, note=True)
p4 += terms("p4", 40, 1260, [
 ("暫存目錄", "先把整個 dist/ 寫到 .<name>.tmp.<亂數>/，最後一步才改名成 .<name>/；中途失敗舊目錄不受影響"),
 ("安裝權", "同一專案同時只能有一個 install／accept 在寫 .<name>/ 或基準；怎麼做到互斥（鎖）還在審（issue #24）"),
 ("兩棵樹比對", "把 image 內的 /dist 跟 .<name>/ 逐檔比：檔案集合（缺、多）、內容指紋 sha256、執行位（單向：該可執行的仍可執行，Windows 掛載才不誤報）、型別（symlink 第一版禁止）"),
 ("印記 / --self", "印記 = .<name>/.stamp，第一行 = 啟動器用 --self 傳進來的 .version 字串，之後每檔指紋（追溯用）；verify 只用第一行判斷要不要重裝"),
 ("基準 / accept", "基準 = .vendor_kit/baseline/<name>/：上次確認過的模板副本＋metadata；accept = 把新版模板寫成基準的子命令"),
 ("三方 / 二方", "三方 = 基準、新版模板、你的檔三份一起比，能分出誰改了什麼；二方 = 只比新版模板跟你的檔（沒基準時的退路）"),
 ("結束狀態", "程式結束時回報的數字；diff 用 0 沒差異／1 工具有改／2 可能重疊，給 CI 判斷"),
 ("src → dest", "init.toml 每一項：src 指 image 的 dist/ 裡哪個檔，dest 指要放到專案的哪裡"),
 ("vendor_kit / image / dist", "安裝工具本身／打包好可執行的檔案包／工具要出貨的檔案"),
 ("init.toml / 啟動器", "init 要建立哪些檔的清單／專案裡的 .vendor_kit/ 標準指令（使用者打 just 時執行）"),
 ("容器 / <name>", "容器 = image 執行起來的實例；<name> = .version 裡的工具名，安裝目錄就叫 .<name>/"),
])

'''
src = src[:start] + p5 + src[end:]
rep('       + page("p4", "5. 流程：vendor_kit 內部", p4, w=1920, h=1160)', '       + page("p4", "5. 流程：vendor_kit 內部", p4)')

# ================= 頁 7 =================
rep(''' (1, "src/vendor_kit/", False, "產品程式碼：7 個 Python 模組（= 第 1 頁的 7 個模組，一個模組一個檔）＋ 進入點"),''',
    ''' (1, "src/vendor_kit/", False, "產品程式碼：第 1 頁的模組，一個模組一個檔＋ 進入點"),''')
rep(''' (2, "cli.py", True, "命令介面：讀參數、分派 install / init / verify / diff（第一次另有 bootstrap，第 10 頁）"),''',
    ''' (2, "cli.py", True, "命令介面：讀參數、分派 install / init / verify / diff / accept（第一次另有 bootstrap，第 10 頁）"),''')
rep(''' (2, "repo_fs.py", True, "專案檔案存取：唯一能寫專案目錄的模組；整批替換（原子替換）在這"),''',
    ''' (2, "repo_fs.py", True, "專案檔案存取：唯一能寫專案目錄的模組；整批替換、讀寫基準都在這（安裝權互斥方案審中）"),
 (2, "treediff.py", True, "規劃：兩棵樹比對（image 內 /dist vs .<name>/），install、verify、release-test 共用"),''')
rep(''' (1, ".vendor_kit/", False, "進 git｜啟動器本體：vendor_kit 寫出的標準 just 指令＋它自己的印記，人不改，升級整個換新（第 10 頁）"),''',
    ''' (1, ".vendor_kit/", False, "進 git｜啟動器本體：vendor.just、tools.just、.stamp（vendor_kit 寫出，人不改，升級只換這三個）"),
 (2, "baseline/<name>/", False, "進 git｜三方比對的基準：init／accept 存的模板副本＋metadata；人不改（納入檢查）；升級不動"),
 (1, ".version.local", True, "不進 git｜本機開發用的覆蓋檔：<name> = \\"path:../tool\\"，有它那行就優先（第 4 頁）；平常沒有這個檔"),''')
rep(''' ("install / init / verify / diff / bootstrap", "vendor_kit 的子命令：把 dist 裝進 .<name>/ 並寫印記／建立初始檔／檢查 .<name>/ 沒被手改／比對新版模板／第一次寫出啟動器（第 10 頁）"),
])''', ''' ("install / init / verify / diff / accept / bootstrap", "vendor_kit 的子命令：把 dist 裝進 .<name>/ 並寫印記／建立初始檔＋存基準／拿 .<name>/ 跟 image 內的 dist 比／三方比對新版模板／存新基準／第一次寫出啟動器（第 10 頁）"),
 ("基準（baseline）", "上次確認過的模板副本，diff 用它分出誰改了什麼"),
])''')

# ================= 頁 9 =================
rep('p9.append(v("gA", "1", SW(RED), "vendor_kit 提供的指令（每個用這套框架的專案都一樣）", 40, 70, TBW + 40, 368))',
    'p9.append(v("gA", "1", SW(RED), "vendor_kit 提供的指令（每個用這套框架的專案都一樣）", 40, 70, TBW + 40, 470))')
rep(''' ("just init", "第一次把工具接進專案", "安裝 .<name>/，再照 init.toml 建立初始檔（Dockerfile、設定檔、hooks…）；已存在的不動", "vendor_kit 容器：install → init", ".<name>/（新建）、初始檔（新建）"),
 ("just diff", "升級之後", "顯示新版模板 vs 你的初始檔差在哪；不改任何檔", "vendor_kit 容器：diff", "不動（只印到畫面）"),''',
''' ("just init", "第一次把工具接進專案", "安裝 .<name>/，再照 init.toml 建立初始檔（Dockerfile、設定檔、hooks…）；已存在的 warn、不覆蓋；並把這版模板存成基準", "vendor_kit 容器：install → init", ".<name>/（新建）、初始檔（新建）、.vendor_kit/baseline/<name>/"),
 ("just diff", "升級之後", "三方比對：印出「工具改了什麼」「你改了什麼」，不改任何檔；結束狀態 0 沒差異／1 工具有改／2 可能重疊", "vendor_kit 容器：diff", "不動（只印到畫面）"),
 ("just accept <name>", "看完 diff、跟進完之後", "把新版模板存成基準，下次 diff 以它為舊版", "vendor_kit 容器：accept", ".vendor_kit/baseline/<name>/"),
 ("just dev <name> <路徑>\\njust undev <name>", "開發工具本身時", "dev：把工具指到本機原始碼（寫 .version.local，不進 git；之後不做完整性檢查、只警告）；undev：移除並重裝正式版", "vendor_kit 容器：--dev install", ".version.local、.<name>/"),''')
rep(''' ("（自動）", "每個 just 指令執行前", "第 3 頁的檢查：.<name>/.stamp 第一行 ≠ .version → install；相同 → verify；verify 失敗就中止", "vendor_kit 容器：install 或 verify", ".<name>/（可能重裝）"),''',
    ''' ("（自動）", "每個 just 指令執行前", "第 3 頁的檢查：印記第一行 ≠ .version → install；相同 → verify（.<name>/ 跟 image 內的 dist 逐檔比）；失敗就中止", "vendor_kit 容器：install 或 verify", ".<name>/（可能重裝）"),''')
rep('p9.append(v("gB", "1", SW(GREEN), "工具 <name> 提供的指令（由工具的 dist/ 決定，每個工具可以不同；下面以「容器工作流」工具為例）", 40, 470, TBW + 40, 360))',
    'p9.append(v("gB", "1", SW(GREEN), "工具 <name> 提供的指令（由工具的 dist/ 決定，每個工具可以不同；下面以「容器工作流」工具為例）", 40, 570, TBW + 40, 360))')
rep('p9.append(v("gC", "1", SW(NEUTRAL), "任何一個 just 指令的完整路徑", 40, 860, TBW + 40, 205))', 'p9.append(v("gC", "1", SW(NEUTRAL), "任何一個 just 指令的完整路徑", 40, 960, TBW + 40, 205))')
rep('p9.append(v("c3", "gC", PURPLE_LEAF, "起 vendor_kit 容器跑子命令\\n（init / diff；upgrade = 改 .version → install → diff）", 660, 55, 300, 50))',
    'p9.append(v("c3", "gC", PURPLE_LEAF, "起 vendor_kit 容器跑子命令\\n（init / diff / accept / dev；upgrade 待議）", 660, 55, 300, 50))')
rep('p9 += legend("p9", 40, 1090,', 'p9 += legend("p9", 40, 1190,')
rep('p9 += terms("p9", 40, 1200, [', 'p9 += terms("p9", 40, 1300, [')
rep(''' ("子命令 / dist/", "子命令 = vendor_kit 容器裡的動作：install 把 dist 裝進 .<name>/ 並寫印記、init 建初始檔、verify 檢查 .<name>/ 有沒有被手改、diff 比模板；bootstrap 只在第一次寫出啟動器（第 10 頁）；dist/ = 工具要出貨的檔案"),''',
    ''' ("子命令 / dist/", "子命令 = vendor_kit 容器裡的動作：install 把 dist 裝進 .<name>/ 並寫印記、init 建初始檔＋存基準、verify 拿 .<name>/ 跟 image 內的 dist 比、diff 三方比模板、accept 存新基準；bootstrap 只在第一次寫出啟動器（第 10 頁）；dist/ = 工具要出貨的檔案"),
 ("基準（baseline）", ".vendor_kit/baseline/<name>/：上次確認過的模板副本；diff 靠它分出「工具改了什麼」「你改了什麼」；init 第一次存、accept 更新"),
 (".version.local / dev", "跟 .version 同格式、不進 git 的覆蓋檔；just dev 寫它把工具指到本機路徑，undev 移除；有它的工具不做完整性檢查、只印警告"),''')
rep(''' ("印記 / .version", ".<name>/.stamp：記錄裝了哪個 image + 每檔指紋／專案記工具版本的檔；兩者不同就重裝"),''',
    ''' ("印記 / .version", ".<name>/.stamp：第一行記裝了哪個 image（之後每檔指紋，追溯用）／專案記工具版本的檔；兩者不同就重裝，相同就拿 .<name>/ 跟 image 內的 dist 比"),''')

# ================= 頁 10 =================
rep('p11.append(v("s2", "bs", LEAF(), "docker run … vendor_kit:vN bootstrap\\n（以使用者身分，掛載專案目錄）", 340, 260, 320, 50))',
    'p11.append(v("s2", "bs", LEAF(), "docker run … vendor_kit:vN --self <image> bootstrap\\n（以使用者身分，掛載專案目錄）", 340, 270, 320, 50).replace("fontSize=14", "fontSize=12"))')
rep('<mxPoint x="690" y="90"/><mxPoint x="690" y="230"/><mxPoint x="500" y="230"/>', '<mxPoint x="690" y="90"/><mxPoint x="690" y="240"/><mxPoint x="500" y="240"/>')
rep('p11.append(v("c1", "bs", PURPLE_LEAF, "bootstrap 子命令\\n寫出啟動器與版本檔（不碰其他檔）", 760, 215, 340, 140))',
    'p11.append(v("c1", "bs", PURPLE_LEAF, "bootstrap 子命令\\n寫出啟動器與版本檔（不碰其他檔）\\n--self = 要寫進 .version 與印記的 vendor_kit 字串", 760, 215, 340, 160).replace("fontSize=14", "fontSize=13"))')
rep('p11.append(v("f1", "bs", FILE, ".vendor_kit/\\n啟動器本體：標準 just 指令（init / diff / upgrade 與每個指令前的自動檢查）\\n＋ 自己的印記 .stamp（記 vendor_kit 版本）；進 git，人不改", 1160, 215, 340, 64).replace("fontSize=14", "fontSize=12"))',
    'p11.append(v("f1", "bs", FILE, ".vendor_kit/（進 git，人不改）\\nvendor.just：標準指令（init / diff / accept / upgrade 與每個指令前的自動檢查）\\ntools.just：依 .version 產生的工具指令清單；.stamp：記 vendor_kit 版本\\nbaseline/<name>/ 之後由 init／accept 寫", 1160, 215, 340, 80).replace("fontSize=14", "fontSize=11"))')
rep('p11.append(v("f2", "bs", FILE, "justfile（一行 import .vendor_kit/…；之後是\\n使用者自己的指令，進 git；已存在就不動）", 1160, 283, 340, 44))',
    'p11.append(v("f2", "bs", FILE, "justfile（一行 import .vendor_kit/…；之後是\\n使用者自己的指令，進 git；已存在就不動）", 1160, 301, 340, 44))')
rep('p11.append(v("f3", "bs", FILE, ".version（先只有 vendor_kit 一行，進 git；已存在就不動）", 1160, 331, 340, 36).replace("fontSize=14", "fontSize=12"))',
    'p11.append(v("f3", "bs", FILE, ".version（先只有 vendor_kit 一行，進 git；已存在就不動）", 1160, 349, 340, 36).replace("fontSize=14", "fontSize=12"))')
rep('''p11.append(e("be5", "c1", "f1", "寫出", (1, 0.2286), (0, 0.5)))
p11.append(e("be6", "c1", "f2", "沒有才寫", (1, 0.6429), (0, 0.5)))
p11.append(e("be7", "c1", "f3", "沒有才寫", (1, 0.9571), (0, 0.5)))''',
'''p11.append(e("be5", "c1", "f1", "寫出", (1, 0.25), (0, 0.5)))
p11.append(e("be6", "c1", "f2", "沒有才寫", (1, 0.675), (0, 0.5)))
p11.append(e("be7", "c1", "f3", "沒有才寫", (1, 0.95), (0, 0.5)))''')
rep('p11.append(v("bn", "1", NOTE, "之後：vendor_kit 出新版 → .version 的 vendor_kit 那行改掉（Renovate 或 just upgrade）→ .vendor_kit/ 整個換新，跟 .<name>/ 一樣；使用者的 justfile 永遠不會被動到。',
    'p11.append(v("bn", "1", NOTE, "之後：vendor_kit 出新版 → .version 的 vendor_kit 那行改掉（Renovate 或 just upgrade）→ .vendor_kit/ 的 vendor.just、tools.just、.stamp 換新（baseline/ 不動）；使用者的 justfile 永遠不會被動到。')
rep(''' ("啟動器 / .vendor_kit/", "just 要用的標準指令集，由 vendor_kit 寫出並擁有；使用者不改，升級整個換新"),''',
    ''' ("啟動器 / .vendor_kit/", "just 要用的標準指令集，由 vendor_kit 寫出並擁有；使用者不改，升級換新程式檔（baseline/ 是持久資料不動）"),
 ("--self / tools.just / baseline/", "--self = 啟動器傳給容器的 vendor_kit image 字串／依 .version 產生的工具指令 import 清單／三方比對的基準副本（第 5 頁）"),''')

# 對齊：a2（m_cli 加寬）、a9、f6（安裝容器下移 30 → GHCR 的 <name>-dist 也下移）
rep('p1.append(e("a2", "m_cli", "m_list", "命令、參數（解析後）", (0.5, 1), (0.5, 0), vert=True))', 'p1.append(e("a2", "m_cli", "m_list", "命令、參數（解析後）", (0.342, 1), (0.5, 0), vert=True))')
rep('p1.append(e("a9", "m_write", "m_stamp", "兩棵樹的內容\\n（/dist、.<name>/）", (0.438, 1), (0.28, 0), vert=True))',
    'p1.append(e("a9", "m_write", "m_stamp", "兩棵樹的內容\\n（/dist、.<name>/）", (0.5068, 1), (0.28, 0), vert=True))')
rep('p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 310, 200, 40))', 'p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 340, 200, 40))')
rep('p1b.append(v("tool", "1", SW(GREEN), "工具 repo（每個要出貨的工具一個）", 40, 240, 320, 260))', 'p1b.append(v("tool", "1", SW(GREEN), "工具 repo（每個要出貨的工具一個）", 40, 270, 320, 260))')
rep('p1b.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 520, 320, 130))', 'p1b.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 550, 320, 130))')
rep('p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 490, 200, 40))', 'p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 520, 200, 40))')
rep('p1b.append(v("tool2", "1", SW(GREEN), "另一個工具 repo（<name2>，同型）", 40, 670, 320, 60))', 'p1b.append(v("tool2", "1", SW(GREEN), "另一個工具 repo（<name2>，同型）", 40, 700, 320, 60))')
rep('p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 600, 200, 40))', 'p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 630, 200, 40))')
rep('p1b.append(v("pc2", "proj", SW(NEUTRAL, 14), ".<name2>/（另一個工具）", 540, 595, 220, 50))', 'p1b.append(v("pc2", "proj", SW(NEUTRAL, 14), ".<name2>/（另一個工具）", 540, 625, 220, 50))')
rep('p1b.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 420, 80, 260, 660))', 'p1b.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 420, 80, 260, 690))')
rep('p1b.append(v("proj", "1", SW(GREEN), "專案 repo（使用工具的專案）", 740, 80, 770, 660))', 'p1b.append(v("proj", "1", SW(GREEN), "專案 repo（使用工具的專案）", 740, 80, 770, 690))')
rep('p1b.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1600, 80, 160, 660))', 'p1b.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1600, 80, 160, 690))')
rep('p1b += legend("p1b", 40, 770,', 'p1b += legend("p1b", 40, 800,')
rep('p1b += terms("p1b", 40, 880, [', 'p1b += terms("p1b", 40, 910, [')
open("gen34.py", "w").write(src)
print("ok")
