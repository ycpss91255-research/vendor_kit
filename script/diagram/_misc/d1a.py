# ================= 討論 D1a：架構圖（乙版重畫，待定型） =================
d1a = [v("title", "1", TITLE, "架構圖（乙版重畫，待定型）：模組 → 最小單元；線上文字 = 傳的資料", 40, 20, 900, 34)]
d1a.append(v("d1a_pend", "1", PEND, "⚠ 待你回覆：1. 七個模組與最小單元的清單是否定型？ 2. ensure 每次檢查全部工具，還是只檢查被叫到的？\n3. 啟動器（在主機跑）要不要算成第 8 個模組？ 4. add 子命令要不要（bootstrap 詢問式接工具用它）？", 960, 12, 560, 72))
VX, VY = 520, 140
# 使用者
d1a.append(v("user", "1", SW(YELLOW), "使用者", 40, VY, 140, 940))
d1a.append(v("u_cmd", "user", LEAF(), "指令", 26, 100, 88, 40))
d1a.append(v("u_out", "user", LEAF(), "畫面", 26, 890, 88, 40))
# 啟動器（主機）
d1a.append(v("launch", "1", SW(RED, 14), "啟動器（主機上的 just）", 200, VY, 220, 140))
d1a.append(v("l_ver", "launch", LEAF(), "讀版本", 12, 45, 88, 40))
d1a.append(v("l_fetch", "launch", LEAF(), "抓工具檔", 108, 45, 88, 40))
d1a.append(v("l_run", "launch", LEAF(), "起引擎容器", 12, 91, 88, 40))
# 工具 image（只有檔案）→ 暫存目錄
d1a.append(v("timg", "1", PURPLE_SW, "工具 image（只有檔案）", 220, 300, 180, 190).replace("fontSize=18", "fontSize=14"))
d1a.append(v("i_dist", "timg", LEAF().replace("fontSize=14", "fontSize=12"), "dist/（全部）", 46, 45, 88, 40))
d1a.append(v("i_list", "timg", LEAF().replace("fontSize=14", "fontSize=12"), "init.toml", 46, 91, 88, 40))
d1a.append(v("i_ver", "timg", LEAF(), "VERSION", 46, 137, 88, 40))
d1a.append(v("tmp", "1", LEAF(), "暫存目錄（主機）\n工具的檔案", 220, 490, 180, 50))
# 引擎容器
d1a.append(v("vk", "1", PURPLE_SW, "引擎容器 vendor_kit:vN（一個專案只用一版）", VX, VY, 660, 940))
d1a.append(v("m_cli", "vk", SW(RED), "命令介面（子命令）", 20, 50, 384, 186))
for i, name in enumerate(["install", "init", "verify", "diff", "accept", "bootstrap", "upgrade", "add（待定）", "dev"]):
    d1a.append(v(f"cli_{i}", "m_cli", LEAF().replace("fontSize=14", "fontSize=12") if ("（" in name or len(name) > 8) else LEAF(), name, 12 + (i % 4) * 92, 45 + (i // 4) * 47, 88, 40))
d1a.append(v("m_list", "vk", SW(RED), "出貨內容讀取", 20, 250, 200, 170))
d1a.append(v("ls_read", "m_list", LEAF(), "讀 /dist", 12, 45, 88, 40))
d1a.append(v("ls_check", "m_list", LEAF().replace("fontSize=14", "fontSize=12"), "讀 init.toml", 104, 45, 88, 40))
d1a.append(v("ls_class", "m_list", LEAF().replace("fontSize=14", "fontSize=12"), "檢查清單\n格式", 12, 92, 88, 40))
d1a.append(v("m_tpl", "vk", SW(RED), "模板", 20, 560, 200, 130))
d1a.append(v("tp_copy", "m_tpl", LEAF(), "複製", 12, 45, 88, 40))
d1a.append(v("tp_vars", "m_tpl", LEAF().replace("fontSize=14", "fontSize=12"), "渲染／帶入\n變數（待定）", 104, 45, 88, 40))
d1a.append(v("m_diff", "vk", SW(RED), "差異比對", 20, 750, 200, 130))
d1a.append(v("df_cmp", "m_diff", LEAF(), "三方分類", 12, 45, 88, 40))
d1a.append(v("df_patch", "m_diff", LEAF(), "產生差異", 104, 45, 88, 40))
d1a.append(v("m_write", "vk", SW(RED), "專案檔案存取", 300, 250, 292, 300))
d1a.append(v("wr_copy", "m_write", LEAF(), "寫入", 12, 45, 88, 40))
d1a.append(v("wr_read", "m_write", LEAF(), "讀回", 104, 45, 88, 40))
d1a.append(v("wr_perm", "m_write", LEAF(), "權限設定", 196, 45, 88, 40))
d1a.append(v("wr_atomic", "m_write", LEAF(), "整批替換", 12, 92, 88, 40))
d1a.append(v("wr_lock", "m_write", LEAF().replace("fontSize=14", "fontSize=12"), "鎖（專案\n目錄）", 104, 92, 88, 40))
d1a.append(v("wr_base", "m_write", LEAF(), "讀寫基準", 196, 92, 88, 40))
d1a.append(v("wr_gen", "m_write", LEAF(), "寫啟動器檔", 12, 139, 88, 40))
d1a.append(v("m_stamp", "vk", SW(RED, 16), "印記與比對", 392, 560, 200, 130))
d1a.append(v("st_tree", "m_stamp", LEAF(), "兩棵樹比對", 12, 45, 88, 40))
d1a.append(v("st_hash", "m_stamp", LEAF(), "產生印記", 104, 45, 88, 40))
d1a.append(v("st_cmp", "m_stamp", LEAF(), "讀已裝版本", 12, 85, 88, 40))
d1a.append(v("m_report", "vk", SW(RED), "回報", 300, 750, 200, 130))
d1a.append(v("rp_msg", "m_report", LEAF(), "訊息", 12, 45, 88, 40))
d1a.append(v("rp_code", "m_report", LEAF(), "結束狀態", 104, 45, 88, 40))
# 專案 repo 目錄
d1a.append(v("proj", "1", SW(GREEN), "專案 repo 目錄", 1300, VY, 220, 940))
F12 = FILE.replace("fontSize=14", "fontSize=12")
d1a.append(v("p_ver", "proj", F12, ".version（進 git）\n引擎一行 + 每個工具一行", 10, 100, 200, 44))
d1a.append(v("p_just", "proj", F12, "justfile（你的，進 git）\n一行 import", 10, 156, 200, 44))
d1a.append(v("p_shell", "proj", F12, ".vendor_kit/ 薄殼（進 git）\nentry.just、vendor.just、\nci/check.sh、baseline/<repo>/", 10, 250, 200, 72))
d1a.append(v("p_gen", "proj", F12, ".vendor_kit/gen/（不進 git）\n引擎產生的其餘指令", 10, 332, 200, 56))
d1a.append(v("p_base", "proj", F12, ".<repo>/（不進 git）\n工具檔全部 + .stamp 印記", 10, 400, 200, 44))
d1a.append(v("p_user", "proj", F12, "初始檔（你的，進 git）\nDockerfile、setup.toml…", 10, 456, 200, 44))
d1a.append(v("p_bl", "proj", F12, "基準 baseline/<repo>/\n（在 .vendor_kit/ 裡，進 git）", 10, 512, 200, 56))
d1a.append(v("p_vl", "proj", F12, ".version.local（可選，不進 git）\n本機開發用的覆蓋", 10, 580, 200, 56))
# ---- 線 ----
d1a.append(e("b1", "u_cmd", "launch", "指令", (1, 0.5), (0, 0.857)))
d1a.append('<mxCell id="b2" value="引擎版本、工具版本" style="' + EDGE + 'exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="p_ver" target="launch"><mxGeometry x="0.7" relative="1" as="geometry"><Array as="points"><mxPoint x="1410" y="110"/><mxPoint x="310" y="110"/></Array></mxGeometry></mxCell>')
d1a.append(e("b3", "launch", "timg", "docker create／cp", (0.5, 1), (0.5, 0), vert=True))
d1a.append(e("b4", "timg", "tmp", "dist 檔案", (0.5, 1), (0.5, 0), vert=True))
d1a.append(e("b5", "tmp", "m_list", "/dist（唯讀）", (1, 0.5), (0, 0.735)))
d1a.append(e("b6", "launch", "m_cli", "工具名、子命令\n--self", (1, 0.786), (0, 0.3226)))
d1a.append(e("a2", "m_cli", "m_list", "命令、參數（解析後）", (0.26, 1), (0.5, 0), vert=True))
d1a.append(e("a6", "m_list", "m_write", "dist 全部", (1, 0.3), (0, 0.17)))
d1a.append(e("a7", "m_list", "m_tpl", "init 清單\n＋模板", (0.5, 1), (0.5, 0), vert="left"))
d1a.append(e("a8", "m_tpl", "m_write", "初始檔內容", (0.8, 0), (0.1, 1)))
d1a.append(e("a9", "m_write", "m_stamp", "兩棵樹的內容\n（dist、.<repo>/）", (0.5068, 1), (0.28, 0), vert=True))
d1a.append(e("a9b", "m_stamp", "m_write", "印記、\n已裝版本", (0.9, 0), (0.9315, 1), vert=True))
d1a.append(e("a10", "m_write", "p_shell", "bootstrap／ensure 寫出", (1, 0.12), (0, 0.5)))
d1a.append(e("a10b", "m_write", "p_gen", "ensure 每次重產", (1, 0.3667), (0, 0.5)))
d1a.append(e("a11", "m_write", "p_base", "dist 全部、印記", (1, 0.5733), (0, 0.5), both=True))
d1a.append(e("a12", "m_write", "p_user", "初始檔（init 時）", (1, 0.7233), (0, 0.25)))
d1a.append(e("a12b", "p_user", "m_write", "現有內容（diff 時）", (0, 0.75), (1, 0.7967), vert="below"))
d1a.append(e("a12c", "m_write", "p_bl", "基準（diff 讀／accept 寫）", (1, 0.9667), (0, 0.5), both=True))
d1a.append('<mxCell id="a13" value="使用者檔案、基準" style="' + EDGE + 'exitX=0.3014;exitY=1;exitDx=0;exitDy=0;entryX=0.9;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="m_write" target="m_diff"><mxGeometry x="0.55" relative="1" as="geometry"><Array as="points"><mxPoint x="908" y="860"/><mxPoint x="720" y="860"/></Array></mxGeometry></mxCell>')
d1a.append(e("a14", "m_tpl", "m_diff", "新版模板", (0.5, 1), (0.5, 0), vert=True))
d1a.append(e("a15", "m_stamp", "m_report", "比對結果", (0.265, 1), (0.725, 0), vert=True))
d1a.append(e("a16", "m_diff", "m_report", "差異、\n結束狀態", (1, 0.5), (0, 0.5)))
d1a.append(e("a17", "m_report", "u_out", "訊息、結束狀態", (0.5, 1), (1, 0.5), pos=0.6))
d1a += legend("d1a", 40, 1120, ["purple", "red", "green", "yellow", "white", "file"], "實線 = 傳輸內容（線上文字 = 傳什麼）\n雙向箭頭 = 同一份資料讀與寫")
d1a += terms("d1a", 40, 1230, [
 ("引擎", "vendor_kit 的程式本體：只以 image 存在、只在容器內跑；一個專案只用 .version 指定的那一版"),
 ("啟動器", ".vendor_kit/ 裡的 just recipe，在主機跑：讀 .version、用 docker cp 抓工具檔、起引擎容器"),
 ("工具 image", "工具 repo 出貨的 image，只有檔案（dist/、init.toml、VERSION），沒有程式，不會被執行"),
 ("暫存目錄", "啟動器把工具 image 的檔案抓到主機的暫存資料夾，再唯讀掛進引擎容器當 /dist"),
 ("薄殼 / gen/", "進 git 的最小啟動器（entry.just、vendor.just）／引擎每次 ensure 產生的其餘指令，不進 git"),
 ("兩棵樹比對", "verify 的做法：/dist（來源）與 .<repo>/（裝好的）逐檔比檔案集合、內容、執行位、型別"),
 ("基準（baseline）", "上次確認過的範本副本；diff 三方比對用，accept 更新"),
 ("印記 .stamp", ".<repo>/.stamp：第一行 = 裝的是哪個 image（判斷要不要重裝），其餘給人追溯"),
 ("<repo>", "工具 repo 名（例：base）；.<repo>/ = 專案裡裝好的工具檔"),
 ("--self", "啟動器傳給引擎的字串 = .version 裡那一行的 image，寫進印記第一行"),
])
pages.insert(1, ("d1a", "架構圖（乙版重畫，待定型）", d1a))
