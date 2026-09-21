s = open("gen16.py", encoding="utf-8").read()

# ---- 名詞表底色改白（避免未列於圖例的顏色）；紫色圖例文字 ----
s = s.replace('TERM_K = "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;', 'TERM_K = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;')
s = s.replace('"紫：container（執行形態）", 220, 60, 0)', '"紫：image / container", 200, 60, 0)')

# ---- page(): 依內容自動裁紙張大小 ----
s = s.replace('def page(id, name, cells, w=1600, h=1100):\n    body = "".join(cells)',
'''def page(id, name, cells, w=1600, h=1100):
    body = "".join(cells)
    # 自動裁切：只看頂層（parent="1"）vertex 的邊界
    import re as _re
    mx = my = 0
    for m in _re.finditer(r'<mxCell id="[^"]+" value="[^"]*" style="[^"]*" vertex="1" parent="1"><mxGeometry x="([\\d.-]+)" y="([\\d.-]+)" width="([\\d.-]+)" height="([\\d.-]+)"', body):
        x0, y0, w0, h0 = map(float, m.groups()); mx = max(mx, x0 + w0); my = max(my, y0 + h0)
    w, h = int(mx + 40), int(my + 40)''')

R = {
 # ================= 頁 1 =================
 'p1.append(v("p_stamp", "proj", LEAF(), "印記檔", 56, 281, 88, 40))': 'p1.append(v("p_stamp", "proj", LEAF(), ".<name>/.stamp\\n（印記檔）", 46, 276, 108, 50))',
 'p1.append(v("tp_vars", "m_tpl", LEAF(), "帶入變數", 104, 45, 88, 40))': 'p1.append(v("tp_vars", "m_tpl", LEAF(), "帶入變數\\n（待定）", 104, 45, 88, 40))',
 ' ("vendor_kit", "通用安裝工具；只以 container 形態執行（開發、使用皆是），主機不需安裝"),': ' ("vendor_kit", "通用安裝工具；只以 container 形態執行（開發、使用皆是），主機不需安裝"),\n ("image / container", "image = 打包好的程式與檔案；container = image 執行起來的實例，跑完可刪"),\n ("<name>", "工具名，由專案的 .version 指定；安裝目錄就叫 .<name>/"),\n ("install / init / verify / diff", "四個子命令：安裝 dist 到 .<name>/／第一次建立使用者檔／檢查 .<name>/ 沒被改／升級後比對模板差異"),\n ("結束狀態", "程式結束時回報成功或失敗，啟動器據此決定要不要繼續執行"),',
 ' ("init.toml", "工具 repo 提供的清單：init 時要複製到專案的初始檔；不在清單上的每次 upgrade 都覆蓋"),': ' ("init.toml", "工具 repo 提供的清單：init 時要複製到專案的初始檔有哪些、放哪（dist/ 本身每次 upgrade 都整包覆蓋）"),',
 # ================= 頁 2：重排（安裝容器回到啟動器下方，整欄下移對齊） =================
 'p1b.append(v("tool", "1", SW(GREEN), "工具 repo（每個要出貨的工具一個）", 40, 80, 320, 260))': 'p1b.append(v("tool", "1", SW(GREEN), "工具 repo（每個要出貨的工具一個）", 40, 190, 320, 260))',
 'p1b.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 360, 320, 130))': 'p1b.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 470, 320, 130))',
 'p1b.append(v("tool2", "1", SW(GREEN), "另一個工具 repo（<name2>，同型）", 40, 555, 320, 60))': 'p1b.append(v("tool2", "1", SW(GREEN), "另一個工具 repo（<name2>，同型）", 40, 620, 320, 60))',
 'p1b.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 420, 80, 260, 550))': 'p1b.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 420, 80, 260, 620))',
 'p1b.append(v("g_t", "ghcr", TEXT(11), "tag 不覆蓋；被引用的版本不刪；\\nimage 附註版本與來源 commit", 10, 40, 240, 40))': 'p1b.append(v("g_t", "ghcr", TEXT(11), "tag 不覆蓋；被引用的版本不刪；\\nimage 附註：版本、來源 repo 與 commit", 10, 40, 240, 40))',
 'p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 150, 200, 40))': 'p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 260, 200, 40))',
 'p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 330, 200, 40))': 'p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 440, 200, 40))',
 'p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 485, 200, 40))': 'p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 550, 200, 40))',
 'p1b.append(v("proj", "1", SW(GREEN), "專案 repo（使用工具的專案）", 740, 80, 770, 550))': 'p1b.append(v("proj", "1", SW(GREEN), "專案 repo（使用工具的專案）", 740, 80, 770, 620))',
 'p1b.append(v("p_eng", "proj", PURPLE_LEAF, "安裝容器（<name>-dist:vX）", 340, 140, 260, 60))': 'p1b.append(v("p_eng", "proj", PURPLE_LEAF, "安裝容器（<name>-dist:vX）", 20, 250, 260, 60))',
 'p1b.append(v("p_eng_t", "proj", TEXT(11) + "align=left;", "以使用者身分執行，跑完即刪", 340, 202, 200, 20))': 'p1b.append(v("p_eng_t", "proj", TEXT(11) + "align=left;", "以使用者身分執行，跑完即刪", 20, 312, 200, 20))',
 'p1b.append(v("pb", "proj", SW(NEUTRAL), "使用者檔案（進 git）", 300, 360, 220, 125))': 'p1b.append(v("pb", "proj", SW(NEUTRAL), "使用者檔案（進 git）", 300, 380, 220, 125))',
 'p1b.append(v("pc", "proj", SW(NEUTRAL), ".<name>/（不進 git）", 540, 340, 220, 125))': 'p1b.append(v("pc", "proj", SW(NEUTRAL), ".<name>/（不進 git）", 540, 380, 220, 125))',
 'p1b.append(v("pc2", "proj", SW(NEUTRAL), ".<name2>/（另一個工具）", 540, 480, 220, 50))': 'p1b.append(v("pc2", "proj", SW(NEUTRAL), ".<name2>/（另一個工具）", 540, 545, 220, 50))',
 'p1b.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1600, 80, 160, 550))': 'p1b.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1600, 80, 160, 620))',
 'p1b.append(v("h_docker", "host", LEAF(GREY), "Docker\\n（跑所有容器）", 20, 378, 120, 50))': 'p1b.append(v("h_docker", "host", LEAF(GREY), "Docker\\n（跑所有容器）", 20, 418, 120, 50))',
 'p1b.append(e("f6", "g_tool", "p_eng", "image", (1, 0.5), (0, 0.5), pos=-0.4))': 'p1b.append(e("f6", "g_tool", "p_eng", "image", (1, 0.5), (0, 0.5)))',
 'p1b.append(e("f7", "p_ver", "p_just", "讀取", (1, 0.5), (0, 0.5)))': 'p1b.append(e("f7", "p_ver", "p_just", "工具名、版本", (1, 0.5), (0, 0.5)))',
 'p1b.append(e("f8", "p_just", "p_eng", "工具名、版本、使用者身分（讓寫出的檔案歸使用者）、專案路徑", (1, 0.5), (0, 0.5)))': 'p1b.append(e("f8", "p_just", "p_eng", "工具名、版本、使用者身分、專案路徑", (0.5, 1), (0.78, 0), vert=True))',
 'p1b.append(e("f9", "p_eng", "pc", "寫入 dist、印記檔", (1, 0.5), (0.5, 0)))': 'p1b.append(e("f9", "p_eng", "pc", "寫入 dist、印記檔", (1, 0.3), (0.5, 0)))',
 'p1b.append(e("f10", "p_eng", "pb", "初始檔（init 時）", (0.27, 1), (0.5, 0), dashed=True, vert=True))': 'p1b.append(e("f10", "p_eng", "pb", "初始檔（只在 init 時）", (1, 0.7), (0.5, 0)))',
 'p1b.append(e("f12", "g_tool2", "pc2", "image（同樣經安裝容器）", (1, 0.5), (0, 0.5)))': 'p1b.append(e("f12", "g_tool2", "pc2", "dist、印記檔（同樣經安裝容器寫入）", (1, 0.5), (0, 0.5)))',
 'p1b += legend("p1b", 40, 700, ["red", "green", "yellow", "pimg", "neutral", "white", "grey"], "實線 = 傳輸內容\\n虛線箭頭 = 基底 → 以它為底的 image；或只在特定情況發生")': 'p1b += legend("p1b", 40, 730, ["red", "green", "yellow", "pimg", "neutral", "white", "grey"], "實線 = 傳輸內容\\n虛線箭頭 = 基底 image → 以它為底的 image")',
 'p1b += terms("p1b", 40, 810, [': 'p1b += terms("p1b", 40, 840, [',
 ' ("tag / digest", "image 的版本名稱（v0.43.0）／內容指紋（sha256:…）；.version 兩者都記，工具只認 digest"),\n])': ' ("tag / digest", "image 的版本名稱（v0.43.0）／內容指紋（sha256:…，鎖多架構 index）；.version 兩者都記，工具只認 digest"),\n ("Dockerfile / Dockerfile.dist / FROM", "Dockerfile = 打包 image 的食譜；Dockerfile.dist = 工具 repo 出貨用的食譜；FROM = 食譜第一行，指定以哪個 image 為底"),\n ("commit", "git 的一次版本紀錄"),\n ("compose 指令", "docker compose：依設定檔啟動專案容器的指令"),\n ("TOML", "一種設定檔格式（key = \\"value\\"）；.version、init.toml 都用它"),\n])',
 # ================= 頁 3 =================
 '("專案目錄（安裝目錄 .<name>/，下以 .<name>/ 示意）", 1240, 380)]': '("專案目錄（安裝目錄 .<name>/）", 1240, 380)]',
 'p2.append(v("b_l2", "bB", RHOMBUS, "印記存在且版本\\n= .version？", 550, 55, 180, 80))': 'p2.append(v("b_l2", "bB", RHOMBUS, "印記可讀且版本\\n= .version？", 550, 55, 180, 80))',
 'p2.append(e("be3", "b_l2", "b_c0", "不同或不存在", (1, 0.5), (0, 0.5), pos=-0.4))': 'p2.append(e("be3", "b_l2", "b_c0", "否則", (1, 0.5), (0, 0.5), pos=-0.4))',
 'p2.append(v("b_p1", "bB", FILE, "docker compose build", 1240, 265, 200, 40))': 'p2.append(v("b_p1", "bB", LEAF(), "docker compose build", 1240, 265, 200, 40))',
 'p2.append(e("be7", "b_c1", "b_l3", "通過", (0, 0.85), (0.5, 0), vert=True, pos=0.6))': 'p2.append(e("be7", "b_c1", "b_l3", "通過", (0, 0.85), (0.5, 0), vert=True, pos=0.8))',
 'band("bC", "升級：Renovate 開的 PR 被 merge（或 just upgrade）", 830, 300)': 'band("bC", "升級：Renovate 開的 PR 被 merge", 730, 300)',
 '"四個紫框 = 四個子命令：install（第一次、版本改變時）、init（只有第一次）、verify（每次日常）、diff（升級後由使用者呼叫）。\\nRenovate：GitHub 上的機器人，GHCR 有新版就自動開 PR 改 .version；沒有它時用 just upgrade 手動改。"': '"紫框 = 子命令：install（第一次、版本改變時）、init（只有第一次）、verify（每次日常）、diff（升級後由使用者呼叫）。\\n沒有 Renovate 時用 just upgrade 手動：改 .version → 立即 install → diff（細節待議）。"',
 ' ("docker compose", "工具腳本最後真正用來啟動專案容器的指令"),': ' ("docker compose", "工具腳本最後真正拿來 build／啟動／進入／停止專案容器的指令"),\n (".version", "專案裡的版本清單（TOML）：一個工具一行，記工具名與 image 版本"),\n ("PR / merge", "GitHub 上的合併請求／接受它"),\n ("GHCR", "GitHub 的 image 倉庫"),\n ("dist / image / 模板", "dist = 工具要出貨的檔案；image = 打包好可執行的檔案包；模板 = dist 裡給初始檔用的樣板"),',
 # ================= 頁 4 =================
 '".<name>/ 整批覆蓋（非 init 的東西全部換新）"': '".<name>/ 整批換成新版（含模板）"',
 '".version 暫時指向本機的工具原始碼（而非 GHCR image）\\n改工具不必每次發佈 image 就能在專案裡測"': '"候選做法：.version 暫時指向本機的工具原始碼（而非 GHCR image）\\n改工具不必每次發佈 image 就能在專案裡測"',
 '<mxCell id="c14b" value="無" style="\' + EDGE + \'align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;exitX=1;': '<mxCell id="c14b" value="無" style="\' + EDGE + \'align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;exitX=1;',
 ' ("digest", "image 的內容指紋（sha256:…）；同一個 digest 永遠是同一份內容"),\n])': ' ("digest", "image 的內容指紋（sha256:…）；同一個 digest 永遠是同一份內容"),\n (".version / 啟動器", "專案裡記工具版本的檔／專案裡的 justfile，打 just 時它負責安裝與執行"),\n ("install / diff / init.toml", "安裝子命令／升級後比對子命令／init 要建立哪些檔的清單"),\n ("工具 repo / GHCR / image", "工具的原始碼 repo／GitHub 的 image 倉庫／打包好可執行的檔案包"),\n])',
 # ================= 頁 5 =================
 ' ("原子替換", "改名是一步完成的動作，不會出現「一半新一半舊」的目錄"),': ' ("原子替換", "先在暫存目錄準備好全部新檔，最後用一次改名換掉舊目錄；任何時刻看到的都是完整的舊版或完整的新版"),',
 ' ("印記 / 指紋", "印記 = .<name>/.stamp（版本 + 每檔指紋）；指紋 = 檔案內容算出的 sha256"),\n])': ' ("印記 / 指紋", "印記 = .<name>/.stamp（版本 + 每檔指紋）；指紋 = 由檔案內容算出的識別碼，內容一改就不同"),\n ("vendor_kit / image / dist", "安裝工具本身／打包好可執行的檔案包／工具要出貨的檔案"),\n ("init.toml / 啟動器", "init 要建立哪些檔的清單／專案裡的 justfile"),\n])',
 # ================= 頁 6 =================
 'p7 = [v("title", "1", TITLE, "原型對照：proto/ 三個資料夾 ↔ 框架裡的三種角色 ↔ GHCR", 40, 20, 900, 30)]': 'p7 = [v("title", "1", TITLE, "原型對照：proto/ 三個資料夾 ↔ 框架裡的三種角色（原型的範例工具名是 tool，正式版對應 <name>）", 40, 20, 1300, 30)]',
 'p7.append(v("row_d", "1", TEXT(12) + "align=left;", "使用端（進 git 的只有前兩個）", 1080, 70, 300, 20))': 'p7.append(v("row_d", "1", TEXT(12) + "align=left;", "使用端（前三樣進 git）", 1080, 70, 300, 20))',
 'p7.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 640, 100, 300, 490))': 'p7.append(v("ghcr", "1", SW(YELLOW), "image（原型：本機；正式版：GHCR）", 640, 100, 300, 490))',
 'p7.append(v("g_n", "ghcr", TEXT(11), "原型只 build 到本機，沒有 push；\\n正式版由 CI 在打 tag 時 push", 10, 450, 280, 40))': 'p7.append(v("g_n", "ghcr", TEXT(11), "原型只 build 到本機；正式版由 CI 在打 tag 時 push 到 GHCR", 10, 450, 280, 40))',
 'p7.append(v("f_land", "r_proj", LEAF(), ".tool/ ＋ .stamp\\n（不進 git，install 寫出）", 20, 370, 300, 50))': 'p7.append(v("f_land", "r_proj", LEAF(), ".tool/（含 .stamp 印記檔）\\n（不進 git，install 寫出）", 20, 370, 300, 50))',
 'p7.append(e("x1", "f_vkdf", "g_vk", "docker build → push", (1, 0.5), (0, 0.5), offset=(0, -4)))': 'p7.append(e("x1", "f_vkdf", "g_vk", "image（build 後 push）", (1, 0.5), (0, 0.5), offset=(0, -4)))',
 'p7.append(e("x2", "f_tdf", "g_tool", "docker build → push", (1, 0.5), (0, 0.5), offset=(0, -4)))': 'p7.append(e("x2", "f_tdf", "g_tool", "image（build 後 push）", (1, 0.5), (0, 0.5), offset=(0, -4)))',
 'p7.append(e("x4", "g_tool", "f_land", "docker run\\n… install", (1, 0.75), (0, 0.75), pos=0.5))': 'p7.append(e("x4", "g_tool", "f_land", "dist（install 寫出）", (1, 0.75), (0, 0.75), pos=0.2))',
 ' ("setup.toml", "範例工具給專案的設定檔（TOML）"),\n])': ' ("setup.toml", "範例工具給專案的設定檔（TOML）"),\n ("GHCR / image / CI", "GitHub 的 image 倉庫／打包好可執行的檔案包／打 tag 時自動 build 並 push 的流程"),\n (".version / justfile / init.toml", "專案記工具版本的檔／專案的指令入口（啟動器）／工具給的初始檔清單"),\n])',
}
for k, val in R.items():
    assert s.count(k) == 1, (k[:80], s.count(k))
    s = s.replace(k, val)
open("gen17.py", "w", encoding="utf-8").write(s)
print("ok")
