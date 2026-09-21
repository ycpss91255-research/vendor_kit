s = open("gen12.py", encoding="utf-8").read()

# ---------- 頁 2 重寫：框架定義 ----------
a = s.index("# ================= Page 2: 出貨路徑 =================")
b = s.index("# ================= Page 6: 名詞說明 =================")
p2 = r'''# ================= Page 2: 框架定義 =================
p1b = [v("title", "1", TITLE, "框架定義：兩種 repo 各自必須有什麼，以及工具怎麼送到專案", 40, 20, 1000, 30)]
# 工具 repo
p1b.append(v("tool", "1", SW(GREEN), "工具 repo（每個要出貨的工具一個）", 40, 80, 300, 300))
p1b.append(v("t_t", "tool", TEXT(11), "工具名 = <name>；下面四樣是接上 vendor_kit 的必要條件", 10, 40, 280, 30))
p1b.append(v("t_dist", "tool", LEAF(GREY), "dist/\n（要出貨的全部檔案）", 20, 80, 125, 50))
p1b.append(v("t_init", "tool", LEAF(), "init.toml\n（初始檔清單）", 155, 80, 125, 50))
p1b.append(v("t_df", "tool", LEAF(), "Dockerfile.dist\n（FROM vendor_kit）", 20, 145, 125, 50))
p1b.append(v("t_ci", "tool", LEAF(), "CI：打 tag →\nbuild + push image", 155, 145, 125, 50))
p1b.append(v("t_n", "tool", TEXT(11), "其他內容（doc、test、CI 腳本…）不在 dist/ 裡，不會出貨", 10, 210, 280, 40))
p1b.append(v("tool2", "1", SW(GREEN), "另一個工具 repo（同型）", 40, 400, 300, 60))
# vendor_kit repo
p1b.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 500, 300, 130))
p1b.append(v("vk_prog", "vk", LEAF(), "vendor_kit 程式", 20, 50, 125, 40))
p1b.append(v("vk_df", "vk", LEAF(), "Dockerfile", 155, 50, 125, 40))
# GHCR
p1b.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 400, 80, 260, 550))
p1b.append(v("g_t", "ghcr", TEXT(11), "tag 不覆蓋；被引用的版本不刪；\nimage 附註版本與來源 commit", 10, 40, 240, 40))
p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 190, 200, 40))
p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 330, 200, 40))
p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 490, 200, 40))
# 專案 repo
p1b.append(v("proj", "1", SW(GREEN), "專案 repo（使用工具的專案）", 720, 80, 780, 550))
p1b.append(v("p_t", "proj", TEXT(11), "進 git 的只有前兩樣；.version 可以列多個工具，每個安裝到自己的 .<name>/", 10, 40, 760, 30))
p1b.append(v("pa", "proj", SW(RED), "啟動器（進 git）", 20, 80, 240, 125))
p1b.append(v("p_ver", "pa", LEAF(), ".version", 12, 48, 100, 40))
p1b.append(v("p_just", "pa", LEAF(), "justfile", 128, 48, 100, 40))
p1b.append(v("pa_t", "pa", TEXT(11), "契約版本與更新\n方式：待設計", 6, 90, 110, 26))
p1b.append(v("p_eng", "proj", PURPLE_LEAF, "安裝容器（<name>-dist:vX）", 20, 230, 240, 60))
p1b.append(v("p_eng_t", "proj", TEXT(11), "以使用者身分執行，跑完即刪", 20, 292, 240, 20))
p1b.append(v("pb", "proj", SW(RED), "使用者檔案（進 git）", 300, 330, 220, 110))
p1b.append(v("p_u1", "pb", LEAF(), "Dockerfile", 12, 45, 90, 40))
p1b.append(v("p_u2", "pb", LEAF(), "設定檔…", 118, 45, 90, 40))
p1b.append(v("pb_t", "pb", TEXT(11), "init 建立；之後由使用者維護", 12, 88, 200, 18))
p1b.append(v("pc", "proj", SW(RED), ".<name>/（不進 git）", 540, 330, 220, 110))
p1b.append(v("p_c1", "pc", LEAF(), "dist 全部", 12, 45, 90, 40))
p1b.append(v("p_c2", "pc", LEAF(), "印記檔", 118, 45, 90, 40))
p1b.append(v("pc_t", "pc", TEXT(11), "每次 upgrade 整批覆蓋", 12, 88, 200, 18))
# 使用者的電腦
p1b.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1540, 80, 150, 550))
p1b.append(v("h_just", "host", LEAF(GREY), "just", 31, 60, 88, 40))
p1b.append(v("h_git", "host", LEAF(GREY), "git", 31, 120, 88, 40))
p1b.append(v("h_docker", "host", LEAF(GREY), "Docker", 31, 365, 88, 40))
# 線
p1b.append(e("f1", "t_ci", "g_tool", "image", (1, 0.5), (0, 0.5)))
p1b.append(e("f2", "tool2", "g_tool2", "image", (1, 0.5), (0, 0.5)))
p1b.append(e("f3", "vk_df", "g_vk", "image", (1, 0.5), (0, 0.5)))
p1b.append(e("f4", "g_vk", "g_tool2", "基底 image", (0.5, 0), (0.5, 1), dashed=True, vert=True))
p1b.append(e("f5", "g_tool2", "g_tool", "基底 image", (0.5, 0), (0.5, 1), dashed=True, vert=True))
p1b.append(e("f6", "g_tool", "p_eng", "image", (1, 0.5), (0, 0.5)))
p1b.append(e("f7", "p_ver", "p_just", "工具名、版本", (1, 0.5), (0, 0.5)))
p1b.append(e("f8", "p_just", "p_eng", "工具名、版本、身分、路徑", (0.5, 1), (0.74, 0), vert=True, pos=0.85))
p1b.append(e("f9", "p_eng", "pc", "dist、印記檔", (1, 0.3), (0.5, 0), both=True))
p1b.append(e("f10", "p_eng", "pb", "初始檔", (1, 0.7), (0.5, 0), dashed=True))
p1b.append(e("f11", "pc", "h_docker", "compose 指令", (1, 0.5), (0, 0.5)))
p1b += legend_arch("p1b", 40, 900)

# ================= Page 3: 流程：使用者指令 =================
'''
# 頁 3 沿用（從原檔取出）
p3_start = s.index("# ================= Page 3: 流程：使用者指令 =================")
p3_end = s.index("# ================= Page 3: 流程：版本生命週期 =================")
p3_body = s[p3_start + len("# ================= Page 3: 流程：使用者指令 =================\n"):p3_end]
p3_body = p3_body.replace(".base/", ".<name>/").replace("專案目錄（安裝目錄 .<name>/，下以 .base/ 示意）", "專案目錄")
s = s[:a] + p2 + p3_body + s[p3_end:]

# ---------- 頁 1 ----------
s = s.replace('".<name>/\\n（例：.base/）"', '".<name>/"')
# ---------- 頁 6 ----------
s = s.replace(' (".<name>/", "工具的安裝目錄，例如 base → .base/、harness → .harness/；不進 git，每次 upgrade 整批覆蓋"),',
              ' (".<name>/", "工具的安裝目錄，name 是 .version 裡的工具名；不進 git，每次 upgrade 整批覆蓋"),\n (".version", "專案裡的版本清單：一個工具一行 `name = image`；name 決定安裝目錄 .<name>/"),')
s = s.replace(' (".version", "專案裡的版本清單：一個工具一行 `name = image`；name 決定安裝目錄 .<name>/"),\n (".<name>/"', ' (".<name>/"')
s = s.replace(' ("dist", "工具要出貨的那批檔案，全部寫進下游的 .<name>/"),', ' ("dist", "工具 repo 裡要出貨的那批檔案，全部寫進專案的 .<name>/"),')
s = s.replace(' ("justfile", "使用者的唯一入口；打 just 指令就會執行"),', ' ("justfile", "專案 repo 的唯一入口；打 just 指令就會執行"),')

# ---------- 頁 7 ----------
a7 = s.index("# ================= Page 7: 原型對照 =================")
b7 = s.index("doc = ('<mxfile")
p7 = r'''# ================= Page 7: 原型對照 =================
p7 = [v("title", "1", TITLE, "原型對照：proto/ 三個資料夾 ↔ 框架裡的三種角色 ↔ GHCR", 40, 20, 900, 30)]
p7.append(v("row_t", "1", TEXT(12) + "align=left;", "原始碼（進 git，人維護）", 40, 70, 300, 20))
p7.append(v("row_g", "1", TEXT(12) + "align=left;", "產物（不進 git，CI 產生）", 640, 70, 300, 20))
p7.append(v("row_d", "1", TEXT(12) + "align=left;", "使用端（進 git 的只有前兩個）", 1080, 70, 300, 20))
p7.append(v("r_vk", "1", SW(RED), "vendor_kit repo", 40, 100, 300, 200))
p7.append(v("r_vk_t", "r_vk", TEXT(11), "= proto/vendor_kit/", 10, 40, 280, 18))
p7.append(v("f_vk", "r_vk", LEAF(), "vendor_kit\n（安裝工具程式）", 20, 70, 120, 50))
p7.append(v("f_vkdf", "r_vk", LEAF(), "Dockerfile\n（打包食譜）", 160, 70, 120, 50))
p7.append(v("r_vk_n", "r_vk", TEXT(11), "vendor_kit 是產品本體；Dockerfile 只說明怎麼把它裝進 image", 10, 135, 280, 50))
p7.append(v("r_tool", "1", SW(GREEN), "工具 repo", 40, 340, 300, 250))
p7.append(v("r_tool_t", "r_tool", TEXT(11), "= proto/tool/（工具名 tool）", 10, 40, 280, 18))
p7.append(v("f_dist", "r_tool", LEAF(GREY), "dist/\n（全部出貨，含模板）", 20, 70, 260, 50))
p7.append(v("f_init", "r_tool", LEAF(), "init.toml\n（init 清單）", 20, 130, 120, 50))
p7.append(v("f_tdf", "r_tool", LEAF(), "Dockerfile.dist\n（出貨食譜）", 160, 130, 120, 50))
p7.append(v("r_tool_n", "r_tool", TEXT(11), "Dockerfile.dist：FROM vendor_kit:v1，再疊上 dist/ 與 init.toml", 10, 190, 280, 50))
p7.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 640, 100, 300, 490))
p7.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:v1", 40, 90, 220, 50))
p7.append(v("g_tool", "ghcr", PURPLE_LEAF, "tool-dist:v0.1.0", 40, 390, 220, 50))
p7.append(v("g_n", "ghcr", TEXT(11), "原型只 build 到本機，沒有 push；\n正式版由 CI 在打 tag 時 push", 10, 450, 280, 40))
p7.append(v("r_proj", "1", SW(GREEN), "專案 repo", 1080, 100, 340, 490))
p7.append(v("r_proj_t", "r_proj", TEXT(11), "= proto/project/", 10, 40, 320, 18))
p7.append(v("f_ver", "r_proj", LEAF(), ".version", 20, 70, 140, 40))
p7.append(v("f_just", "r_proj", LEAF(), "justfile", 180, 70, 140, 40))
p7.append(v("f_user", "r_proj", LEAF(GREY), "Dockerfile、setup.toml…\n（init 建立後歸使用者）", 20, 120, 300, 50))
p7.append(v("f_land", "r_proj", LEAF(), ".tool/ ＋ .stamp\n（不進 git，install 寫出）", 20, 390, 300, 50))
p7.append(v("r_proj_n", "r_proj", TEXT(11), "這個 repo 不知道 vendor_kit 存在，\n只認 .version 裡的 tool-dist image", 10, 450, 320, 36))
p7.append(e("x1", "f_vkdf", "g_vk", "docker build → push", (1, 0.5), (0, 0.5), offset=(0, -4)))
p7.append(e("x2", "f_tdf", "g_tool", "docker build → push", (1, 0.5), (0, 0.5), offset=(0, -4)))
p7.append(e("x3", "g_vk", "g_tool", "FROM（基底）", (0.5, 1), (0.5, 0), dashed=True, vert=True))
p7.append(e("x4", "g_tool", "f_land", "docker run\n… install", (1, 0.75), (0, 0.75), pos=0.15))
p7.append(e("x5", "f_ver", "g_tool", "指定用哪個 image", (0, 0.5), (1, 0.15), pos=-0.6))
p7 += legend_arch("p7", 40, 640)

'''
s = s[:a7] + p7 + s[b7:]
s = s.replace('page("p1b", "2. 出貨路徑（以 base 為例）", p1b, w=1700)', 'page("p1b", "2. 框架定義", p1b, w=1720)')
s = s.replace('+ page("p7", "7. 原型對照（以 base 為例）", p7, h=760)', '+ page("p7", "7. 原型對照", p7, h=760)')
open("gen13.py", "w", encoding="utf-8").write(s)
print("ok")
