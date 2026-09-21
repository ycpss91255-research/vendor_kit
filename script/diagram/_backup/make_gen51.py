"""gen50 → gen51：第 1 輪雙軌審查（1–10 頁，51 項 must_fix）修正"""
import re
src = open("gen50.py").read()

def rep(old, new, count=1):
    global src
    assert src.count(old) == count, (src.count(old), old[:90])
    src = src.replace(old, new)

# ================= 頁 1 =================
# 三欄加高；proj 右移 80 讓標籤有空間；m_write 加高放 bootstrap 產出；m_stamp/m_tpl 下移
rep('p1.append(v("user", "1", SW(YELLOW), "使用者", 40, VY, 140, 900))', 'p1.append(v("user", "1", SW(YELLOW), "使用者", 40, VY, 140, 940))')
rep('p1.append(v("u_out", "user", LEAF(), "畫面", 26, 850, 88, 40))', 'p1.append(v("u_out", "user", LEAF(), "畫面", 26, 890, 88, 40))')
rep('p1.append(v("vk", "1", PURPLE_SW, "vendor_kit（一個 container）", VX, VY, 600, 900))', 'p1.append(v("vk", "1", PURPLE_SW, "vendor_kit（一個 container）", VX, VY, 600, 940))')
rep('p1.append(v("m_tpl", "vk", SW(RED), "模板", 20, 520, 200, 130))', 'p1.append(v("m_tpl", "vk", SW(RED), "模板", 20, 560, 200, 130))')
rep('p1.append(v("m_diff", "vk", SW(RED), "差異比對", 20, 710, 200, 130))', 'p1.append(v("m_diff", "vk", SW(RED), "差異比對", 20, 750, 200, 130))')
rep('p1.append(v("m_write", "vk", SW(RED), "專案檔案存取", 300, 250, 292, 220))', 'p1.append(v("m_write", "vk", SW(RED), "專案檔案存取", 300, 250, 292, 270))')
rep('p1.append(v("m_stamp", "vk", SW(RED, 16), "印記與比對", 392, 520, 200, 130))', 'p1.append(v("m_stamp", "vk", SW(RED, 16), "印記與比對", 392, 560, 200, 130))')
rep('p1.append(v("m_report", "vk", SW(RED), "回報", 300, 710, 200, 130))', 'p1.append(v("m_report", "vk", SW(RED), "回報", 300, 750, 200, 130))')
rep('p1.append(v("proj", "1", SW(GREEN), "專案 repo 的目錄", 1140, VY, 200, 900))', 'p1.append(v("proj", "1", SW(GREEN), "專案 repo 的目錄", 1220, VY, 200, 940))')
rep('''p1.append(v("p_stamp", "proj", LEAF(), ".<name>/\\n.stamp", 56, 250, 88, 40))
p1.append(v("p_base", "proj", LEAF(), ".<name>/", 56, 296, 88, 40))
p1.append(v("p_user", "proj", LEAF(), "使用者檔案", 56, 342, 88, 40))
p1.append(v("p_bl", "proj", LEAF(), "基準\\n（baseline）", 56, 420, 88, 40))''',
'''p1.append(v("p_stamp", "proj", LEAF(), ".<name>/\\n.stamp", 56, 250, 88, 40))
p1.append(v("p_base", "proj", LEAF(), ".<name>/", 56, 296, 88, 40))
p1.append(v("p_user", "proj", LEAF(), "使用者檔案", 56, 342, 88, 40))
p1.append(v("p_bl", "proj", LEAF(), "基準\\n（baseline）", 56, 400, 88, 40))
p1.append(v("p_boot", "proj", LEAF(), "啟動器\\n（.vendor_kit/）", 56, 460, 88, 40))''')
rep('p1.append(e("a6", "m_list", "m_write", "dist 全部", (1, 0.3), (0, 0.232)))', 'p1.append(e("a6", "m_list", "m_write", "dist 全部（寫入、比對）", (1, 0.3), (0, 0.189)))')
rep('p1.append(e("a9", "m_write", "m_stamp", "兩棵樹的內容\\n（/dist、.<name>/）", (0.5068, 1), (0.28, 0), vert=True))', 'p1.append(e("a9", "m_write", "m_stamp", "兩棵樹的內容\\n（dist、.<name>/）", (0.5068, 1), (0.28, 0), vert=True))')
rep('p1.append(e("a10", "m_write", "p_stamp", "印記檔", (1, 0.0909), (0, 0.5), both=True))', 'p1.append(e("a10", "m_write", "p_stamp", "印記檔", (1, 0.0741), (0, 0.5), both=True))')
rep('p1.append(e("a11", "m_write", "p_base", "dist 全部", (1, 0.3), (0, 0.5), both=True))', 'p1.append(e("a11", "m_write", "p_base", "dist 全部", (1, 0.2444), (0, 0.5), both=True))')
rep('p1.append(e("a12", "m_write", "p_user", "初始檔（init 時）", (1, 0.4636), (0, 0.25)))', 'p1.append(e("a12", "m_write", "p_user", "初始檔（init 時）", (1, 0.3778), (0, 0.25)))')
rep('p1.append(e("a12b", "p_user", "m_write", "現有內容（diff 時）", (0, 0.76), (1, 0.5564), vert="below"))', 'p1.append(e("a12b", "p_user", "m_write", "現有內容（diff 時）", (0, 0.76), (1, 0.4533), vert="below"))')
rep('p1.append(e("a12c", "m_write", "p_bl", "基準", (1, 0.8636), (0, 0.5), both=True))',
    '''p1.append(e("a12c", "m_write", "p_bl", "基準（init/accept 寫、diff 讀）", (1, 0.6296), (0, 0.5), both=True))
p1.append(e("a12d", "m_write", "p_boot", "bootstrap 寫出（.vendor_kit/、justfile、.version）", (1, 0.8519), (0, 0.5)))''')
rep('<mxPoint x="868" y="800"/><mxPoint x="680" y="800"/>', '<mxPoint x="868" y="860"/><mxPoint x="680" y="860"/>')
rep('p1 += legend("p1", 40, 1100,', 'p1 += legend("p1", 40, 1140,')
rep('p1 += terms("p1", 40, 1210, [', 'p1 += terms("p1", 40, 1250, [')
rep(''' ("兩棵樹比對", "verify 的做法：把 image 內的 /dist 跟專案的 .<name>/ 逐檔比（檔案集合、內容指紋、執行位單向、型別），多的少的改的都算失敗"),''',
    ''' ("兩棵樹比對", "verify 的做法：把 image 內的 dist 跟專案的 .<name>/ 逐檔比：少了檔、多了檔（只豁免 .stamp）、內容不同、該可執行的變成不可執行、檔案種類不同（例如變成連結）都算失敗"),
 ("三方分類", "diff 對每個初始檔看三份：基準（上次確認過的模板）、新版模板、你的檔 → 分成沒人改／只有工具改／只有你改／兩邊都改／你已套上相同內容"),''')
rep(''' ("啟動器", "專案 repo 裡的 justfile：使用者打 just 指令時，它起 vendor_kit 容器並把結果告訴使用者"),''',
    ''' ("啟動器", "專案 repo 裡的 .vendor_kit/：vendor_kit 寫出的標準 just 指令，使用者打 just 時由它起容器；justfile 只是引用入口"),''')

# ================= 頁 2 =================
rep('p1b.append(e("f7c", "p_vl", "p_vk", "有就優先", (0.5, 1), (0.506, 0), dashed=True, vert=True))', 'p1b.append(e("f7c", "p_vl", "p_vk", "有就優先", (0.5, 1), (0.506, 0), vert=True))')
rep('"啟動器與版本檔（進 git）", 20, 80, 340, 205))', '"啟動器與版本檔", 20, 80, 340, 205))')
rep('".version 一行 = 一個工具 = 一個 .<name>/；.version.local 有同名那行就優先（本機開發用，第 4 頁）", 12, 40, 316, 30))', '"都進 git，只有 .version.local 不進；.version 一行 = 一個工具 = 一個 .<name>/；.version.local 有同名那行就優先（本機開發用，第 4 頁）", 12, 40, 316, 30))')
rep('p1b += legend("p1b", 40, 800, ["red", "green", "yellow", "pimg", "neutral", "white", "grey"], "實線 = 傳輸內容\\n虛線箭頭 = 基底 image → 以它為底的 image")',
    'p1b += legend("p1b", 40, 800, ["red", "green", "yellow", "pimg", "neutral", "white", "grey", "filebox"], "實線 = 傳輸內容\\n虛線箭頭 = 基底 image → 以它為底的 image；虛線框 = 可有可無的檔")')
rep(''' ("PR / merge", "GitHub 上的合併請求／接受它，修改才進 repo"),''',
    ''' ("PR / merge", "GitHub 上的合併請求／接受它，修改才進 repo"),
 ("上鎖", "安裝容器先對專案目錄上鎖：避免兩個 just 同時改同一個 .<name>/，後到的等前一個裝完（第 5 頁）"),
 ("init.toml", "工具 repo 給的清單：dist/ 裡哪個檔（src）在 init 時要複製到專案的哪裡（dest）；之後那些檔歸使用者"),''')
rep('p1b.append(e("f10", "p_eng", "pb", "初始檔（只在 init 時）", (1, 0.7), (0.5, 0)))', 'p1b.append(e("f10", "p_eng", "pb", "初始檔（只在 init 時）", (1, 0.7), (0.5, 0), pos=0.5))')

# ================= 頁 3 =================
rep('("啟動器（justfile，在主機）", 380, 360)', '("啟動器（.vendor_kit/，在主機）", 380, 360)')
rep(''' ("啟動器", "專案裡的 justfile：使用者打 just 指令時，它讀 .version、起安裝容器、再執行工具的腳本"),''',
    ''' ("啟動器", "專案裡的 .vendor_kit/（vendor_kit 寫出的標準 just 指令；justfile 只是引用它）：使用者打 just 時，它讀版本檔、起安裝容器、再執行工具的腳本"),
 ("上鎖", "容器先對專案目錄上鎖：兩個 just 同時跑時，後到的等前一個裝完再檢查，避免同時改同一個 .<name>/（第 5 頁）"),''')
rep('每一行各跑一次右邊的流程\\n「否則」= 不同、尚未安裝、或印記讀不到", 40, 130, 290, 112))',
    '每一行各跑一次右邊的流程；「否則」= 不同、尚未安裝、印記讀不到\\n例外：右邊是 path:（.version.local）→ 走第 4 頁本機開發模式；\\nvendor_kit 那行 → 換 .vendor_kit/ 程式檔（第 11 頁 C）", 40, 130, 290, 124))')
rep('''p2.append('<mxCell id="ce4b" value="讀" style="' + EDGE + 'align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;exitX=0;exitY=0.2;exitDx=0;exitDy=0;entryX=1;entryY=0.8;entryDx=0;entryDy=0;" edge="1" parent="bC" source="c_p3" target="c_c2"><mxGeometry x="0.3" relative="1" as="geometry"><Array as="points"><mxPoint x="1190" y="320"/><mxPoint x="1190" y="203"/></Array></mxGeometry></mxCell>')''',
    '''p2.append('<mxCell id="ce4b" value="讀" style="' + EDGE + 'align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;exitX=0;exitY=0.2;exitDx=0;exitDy=0;entryX=1;entryY=0.8;entryDx=0;entryDy=0;" edge="1" parent="bC" source="c_p3" target="c_c2"><mxGeometry x="0.3" relative="1" as="geometry"><Array as="points"><mxPoint x="1215" y="320"/><mxPoint x="1215" y="203"/></Array></mxGeometry></mxCell>')''')
rep('p2.append(e("ce7", "c_c3", "c_p3", "寫入", (1, 0.5), (0, 0.5)))', 'p2.append(e("ce7", "c_c3", "c_p3", "寫入", (1, 0.5), (0, 0.5), pos=-0.7))')
rep('p2.append(e("ce6", "c_u4", "c_c3", "", (1, 0.5), (0, 0.5)))', 'p2.append(e("ce6", "c_u4", "c_c3", "", (1, 0.5), (0, 0.5)))\np2.append(e("ce8", "c_u3", "c_u4", "", (0.5, 1), (0.5, 0)))')

# ================= 頁 4 =================
rep(''' ("模板 / dist", "dist = 工具要出貨的檔案，整批放進 .<name>/；模板 = dist 裡給初始檔用的樣板，diff 拿新版模板跟你的檔案比"),''',
    ''' ("模板 / dist", "dist = 工具要出貨的檔案，整批放進 .<name>/；模板 = dist 裡給初始檔用的樣板，diff 拿新版模板跟你的檔案比"),
 ("掛進來 / 完整性檢查", "掛進來 = 把本機的 dist 資料夾直接接進容器當作 image 內的 dist（改了馬上生效）／完整性檢查 = verify 比對 .<name>/ 有沒有被改，本機模式下跳過只印警告"),''')
rep(''' (".version / 啟動器", "專案裡記工具版本的檔／專案裡的 justfile，打 just 時它負責安裝與執行"),''',
    ''' (".version / 啟動器", "專案裡記工具版本的檔／專案裡的 .vendor_kit/（vendor_kit 寫出的標準 just 指令），打 just 時它負責安裝與執行"),''')
rep('"just undev <name> → 刪那行 → 下次 just 回到 .version 的正式 image 重裝", 20, 245, 380, 50)', '"just undev <name> → 刪那行、立即用 .version 的正式 image 重裝", 20, 245, 380, 50)')

# ================= 頁 5 =================
rep('"對專案目錄上鎖（排他）\\n拿不到：1 秒後印訊息，最多等 60 秒", 205, 130, 250, 50)', '"對專案目錄上鎖（排他）\\n拿不到：等最多 60 秒（可調；設 0 = 立即失敗）", 205, 130, 250, 50)')
rep('"逾時或鎖不支援：\\n中止，不動任何檔", 15, 330, 190, 60)', '"逾時或鎖不支援：中止，\\n不動任何檔（可用環境變數\\n強制不鎖，風險自負）", 15, 325, 190, 70)')
rep('"跳過複製\\n（別人剛裝好）", 15, 520, 190, 50)', '"跳過複製（別人剛裝好）\\n仍做一次 verify 比對", 15, 520, 190, 50)')
rep('"刪舊 .<name>/、暫存目錄改名\\n（整批覆蓋；空窗由鎖遮住）", 230, 730, 200, 60)', '"舊 .<name>/ 先改名到旁邊 → 暫存目錄\\n改名為 .<name>/ → 刪舊；失敗就改回", 230, 730, 200, 60)')
rep('p4.append(v("ln", "install", NOTE, "任一步失敗即中止，舊 .<name>/ 不動；啟動器不會執行 .<name>/ 內的腳本。\\n支援平台：Linux（含 WSL2）amd64／arm64；鎖不支援的檔案系統（NFS 等）直接中止。", 30, 950, 400, 84))',
    'p4.append(v("ln", "install", NOTE, "任一步失敗即中止，舊 .<name>/ 保留；啟動器不會執行 .<name>/ 內的腳本。\\n支援平台：Linux（含 WSL2）amd64／arm64。", 30, 950, 400, 60))')
rep('"對專案目錄上鎖（共享）\\n讀印記第一行（已裝版本）", 130, 130, 200, 40)', '"對專案目錄上鎖（共享；逾時規則同 install）\\n讀印記第一行（已裝版本）", 130, 130, 200, 40)')
rep('"比對兩棵樹：image 內 /dist vs .<name>/\\n檔案集合、sha256、型別、\\n執行位（單向：該 +x 的仍 +x）", 110, 320, 240, 76)', '"比對兩棵樹：image 內 dist vs .<name>/\\n檔案集合（只豁免 .stamp）、內容指紋、\\n檔案種類、執行位（該可執行的仍可執行）", 110, 320, 240, 76)')
rep('p4.append(v("v_bad1", "verify", ELLIPSE(RED), "版本不符：回報\\n啟動器改跑 install", 15, 560, 140, 50).replace("fontSize=14", "fontSize=11"))', 'p4.append(v("v_bad1", "verify", LEAF(), "結束：版本不符，\\n回報啟動器改跑 install", 15, 560, 140, 50).replace("fontSize=14", "fontSize=11"))')
rep('p4.append(v("d1", "diff", RHOMBUS, "有基準？\\n（baseline/<name>/）", 60, 130, 200, 80).replace("fontSize=14", "fontSize=12"))', 'p4.append(v("d1", "diff", RHOMBUS, "有基準？（baseline/<name>/，\\n且沒被手改：verify 也檢查它）", 60, 130, 200, 80).replace("fontSize=14", "fontSize=11"))')
rep('"二方：新版模板 vs 你的檔\\n並提示「無基準」", 320, 250, 220, 60)', '"二方：新版模板 vs 你的檔，提示「無基準」\\n結束狀態 0 沒差異／1 有差異（分不出誰改）", 320, 250, 220, 60)')
rep('"印兩份：基準→新版（工具改了）、\\n基準→你的（你改了）；重疊處標「可能重疊」", 20, 340, 280, 60)', '"印兩份：基準→新版（工具改了）、基準→你的（你改了）\\n同一檔兩邊都有改 → 標「可能重疊」（不判定是否同一行）", 20, 340, 280, 60)')
rep('"結束（不改任何檔）\\n結束狀態 0 沒差異／1 工具有改／2 可能重疊", 10, 440, 300, 60)', '"結束（不改任何檔）結束狀態：0 = 沒人改／只有你改／已套上；\\n1 = 有「只有工具改」；2 = 有「兩邊都改」", 10, 440, 300, 60)')
rep('p4.append(e("de2", "d1", "d_two", "沒有", (1, 0.5), (0.5, 0), vert=True))', 'p4.append(e("de2", "d1", "d_two", "沒有", (1, 0.5), (0.5, 0)))')
rep('p4.append(v("dn", "diff", NOTE, "第一版只做檔案層級分類；行級精確判定（自寫 diff3）第二版。", 20, 520, 520, 40))', 'p4.append(v("dn", "diff", NOTE, "第一版只做「哪個檔誰改了」；「同一行有沒有衝突」的精確判定第二版再做。", 20, 520, 520, 40))')
rep('p4.append(v("in", "init", NOTE, "dest 已被另一個工具的 init.toml 用到 → 報錯中止（兩個工具不能搶同一個檔）。基準 = .vendor_kit/baseline/<name>/", 30, 725, 420, 44))', 'p4.append(v("in", "init", NOTE, "dest 已被另一個工具的 init.toml 用到 → 報錯中止（兩個工具不能搶同一個檔）\\n基準 = .vendor_kit/baseline/<name>/", 30, 725, 420, 44))')
rep('p4.append(v("a1", "accept", LEAF(), "對專案目錄上鎖（排他）", 110, 130, 200, 40))', 'p4.append(v("a1", "accept", LEAF(), "對專案目錄上鎖（排他；\\n逾時規則同 install）", 110, 130, 200, 40).replace("fontSize=14", "fontSize=12"))')
rep('"寫進 .vendor_kit/baseline/<name>/\\n＋ metadata（image、每檔指紋）", 100, 280, 220, 60)', '"寫進 .vendor_kit/baseline/<name>/\\n＋ 記下是哪個 image、每檔指紋", 100, 280, 220, 60)')
rep('p4.append(v("an", "accept", NOTE, "語意：「這版我全看過了」。寫的是新版模板，不是你的檔；diff 結尾只提示、不會問你。", 20, 520, 380, 50))', 'p4.append(v("an", "accept", NOTE, "語意：「這版我全看過了」。寫的是新版模板，不是你的檔；\\ndiff 結尾只提示、不會問你。", 20, 520, 380, 50))')
rep('p4.append(v("p4n", "1", NOTE, "已定案：verify 比 image 內的 /dist 而不是印記（issue #23）；diff 三方（#22）；install／verify／accept 對專案目錄上鎖（#24）。本機開發模式見第 4 頁（#21）。", 20, 1090, 1500, 40))',
    'p4.append(v("p4n", "1", NOTE, "已定案：verify 比 image 內的 dist 而不是印記（issue #23）；diff 三方（#22）；install／verify／accept 對專案目錄上鎖（#24）。本機開發模式見第 4 頁（#21）。", 20, 1150, 1500, 40))')
rep('p4 += legend_flow("p4", 40, 1150, purple=False, note=True)', 'p4 += legend_flow("p4", 40, 1210, purple=False, note=True)')
rep('p4 += terms("p4", 40, 1260, [', 'p4 += terms("p4", 40, 1320, [')
rep(''' ("三方 / 二方", "三方 = 基準、新版模板、你的檔三份一起比，能分出誰改了什麼；二方 = 只比新版模板跟你的檔（沒基準時的退路）"),''',
    ''' ("三方 / 二方", "三方 = 基準、新版模板、你的檔三份一起比，能分出誰改了什麼；二方 = 只比新版模板跟你的檔（沒基準時的退路）"),
 ("可執行 / 檔案種類 / 記下是哪個 image", "可執行 = 檔案有「可以直接執行」的標記（腳本要有）／種類 = 一般檔、資料夾、連結（symlink，第一版不准）／基準旁邊記的來源 image 與每檔指紋"),
 ("環境變數", "跑指令前設定的名稱=值，用來改預設行為：例如鎖的等待秒數、強制不鎖"),''')

# ================= 頁 7 =================
rep('IND, RH = 26, 34', 'IND, RH = 26, 42')
rep(''' (2, "template.py  stamp.py  diff.py  report.py", True, "純函式（只算結果、不碰檔案）：模板、印記（指紋）、差異比對、回報"),''',
    ''' (2, "template.py  stamp.py  diff.py  report.py", True, "純函式（只算結果、不碰檔案）：模板、印記（指紋）、差異比對（三方分類）、回報"),''')
rep(''' (2, "treediff.py", True, "規劃：兩棵樹比對（image 內 /dist vs .<name>/），install、verify、release-test 共用"),''',
    ''' (2, "treediff.py", True, "規劃中（尚未寫，也還沒算進模組數與鏡射測試）：兩棵樹比對（image 內 dist vs .<name>/），install、verify、release-test 共用"),''')
rep(''' ("進 git／不進 git", "進 git = 這個檔會被版本管理、跟著 repo 走；不進 git = 只在本機產生''', ''' ("進 git／不進 git", "進 git = 這個檔會被版本管理、跟著 repo 走；不進 git = 不由 git 保存、只在這台機器''')
rep(''' ("TOML / tomllib / VERSION / pytest", "設定檔格式（.version、init.toml）／Python 讀 TOML 的內建程式庫／image 內的識別字串，install 抄到印記第一行（跟專案的 .version 不同檔）／Python 測試框架"),''',
    ''' ("TOML / tomllib / VERSION / pytest", "設定檔格式（.version、init.toml）／Python 讀 TOML 的內建程式庫／image 內給人看的識別字串（印記第一行改由啟動器用 --self 傳入的 .version 字串，issue #23）／Python 測試框架"),
 ("ruff / import-linter / 鏡射 / 黑箱 / 記下是哪個 image", "Python 寫法檢查／檢查模組之間誰能引用誰／每個模組必有對應測試檔／system、acceptance 測試不准引用 vendor_kit 程式／基準旁邊記的來源 image 與每檔指紋"),''')
rep(''' (2, "baseline/<name>/", False, "進 git｜三方比對的基準：init／accept 存的模板副本＋metadata；人不改（納入檢查）；升級不動"),''',
    ''' (2, "baseline/<name>/", False, "進 git｜三方比對的基準：init／accept 存的模板副本＋記下是哪個 image；人不改（納入檢查）；升級不動"),''')

# ================= 頁 8 =================
rep('".github/workflows/ ＋ test/ci/check.sh（給下游的契約檢查，第 12 頁）\\nbake validate → system/acceptance → bake release（amd64 + arm64 都 build）", 20, 1036, 380, 44)',
    '".github/workflows/ ＋ test/ci/check.sh（給下游，第 12 頁）\\nbake validate → system/acceptance → release（兩種架構）", 20, 1036, 380, 44)')
rep('y = gate_group("gi", "integration 層 = 一個子命令走到底（四個 *-test stage）", y, [', 'y = gate_group("gi", "integration 層 = 一個子命令走到底（一個子命令一個 stage）", y, [')
rep('    ("g6", "一個子命令一個 stage\\n各自只 COPY 自己的測試檔；哪個 stage 紅 = 第 5 頁哪條泳道壞"),', '    ("g6", "一個子命令一個 stage\\n各自只 COPY 自己的測試檔；哪個 stage 紅 = 第 5 頁哪條泳道壞（accept-test 待補）"),')
rep('    ("g7", "時間預算\\nverify 200 個檔必須 < 0.5 秒（已安裝且版本一致時，每次 just 都會跑它）")])', '    ("g7", "時間預算\\nverify 200 個檔必須 < 0.5 秒（量容器內的函式，不含起容器；每次 just 都會跑它）")])')
rep(''' ("VERSION vs .version", "VERSION = image 內 /dist/VERSION：出貨時寫入的 image 識別字串，install 抄到印記第一行，就是拿來跟 .version 比的值（fixtures 裡是假的）；.version = 專案 repo 記工具版本的檔"),''',
    ''' ("VERSION vs .version", "VERSION = image 內 /dist/VERSION：出貨時寫入、給人看的識別字串（印記第一行改由啟動器 --self 傳入的 .version 字串，issue #23）；.version = 專案 repo 記工具版本的檔"),
 ("amd64 / arm64 / multi-arch", "兩種處理器架構（一般電腦／Jetson 等 ARM 板子）；multi-arch = 同一個 image 名稱同時提供兩種版本，Docker 依主機自動選"),''')
rep(''' ("install / init / verify / diff / just", "四個子命令：把 dist 裝進 .<name>/ 並寫印記／建立初始檔／檢查 .<name>/ 沒被手改／比對新版模板；just = 使用者在主機打的指令跑器（第 3、9 頁）"),''',
    ''' ("install / init / verify / diff / accept / just", "子命令：把 dist 裝進 .<name>/ 並寫印記／建立初始檔＋存基準／拿 .<name>/ 跟 image 內的 dist 比／三方比對新版模板／存新基準（accept 的測試 stage 待補）；just = 使用者在主機打的指令跑器（第 3、9 頁）"),''')
rep(''' ("fixture / 假專案", "測試用的假資料：假的 dist/（工具要出貨的檔案）、init.toml（init 要複製哪些初始檔的清單），以及一個只有 .version 與 justfile 的假專案"),''',
    ''' ("fixture / 假專案", "測試用的假資料：假的 dist/（工具要出貨的檔案）、init.toml（init 要複製哪些初始檔的清單），以及一個假專案（acceptance 測試先用 bootstrap.sh 產生 .vendor_kit/、justfile、.version）"),''')
rep('p8.append(v("s_bake", "stages", TEXT(11), "docker-bake.hcl：group validate = [env-test, lint, unit-test, install-test,\\ninit-test, verify-test, diff-test]；group release = [release, release-test]", 20, 965, 440, 40))',
    'p8.append(v("s_bake", "stages", TEXT(11), "docker-bake.hcl：group validate = [env-test, lint, unit-test, install-test,\\ninit-test, verify-test, diff-test（accept-test 待補）]；group release = [release, release-test]", 20, 965, 440, 40))')

# ================= 頁 9 =================
rep('p9.append(v("gA", "1", SW(RED), "vendor_kit 提供的指令（每個用這套框架的專案都一樣）", 40, 70, TBW + 40, 470))', 'p9.append(v("gA", "1", SW(RED), "vendor_kit 提供的指令（每個用這套框架的專案都一樣）", 40, 70, TBW + 40, 518))')
rep(''' ("just diff", "升級之後", "三方比對：印出「工具改了什麼」「你改了什麼」，不改任何檔；結束狀態 0 沒差異／1 工具有改／2 可能重疊", "vendor_kit 容器：diff", "不動（只印到畫面）"),''',
    ''' ("just diff", "升級之後", "三方比對：印出「工具改了什麼」「你改了什麼」，不改任何檔；結束狀態 0 沒差異／1 工具有改／2 可能重疊", "vendor_kit 容器：diff", "diff 本身不動任何檔（前面的自動檢查可能先更新 .<name>/）"),''')
rep(''' ("just dev / undev\\n<name> [<路徑>]", "開發工具本身時", "dev：把工具指到本機原始碼（寫 .version.local，不進 git；之後不做完整性檢查、只警告）；undev：移除並重裝正式版", "vendor_kit 容器：--dev install", ".version.local、.<name>/"),''',
    ''' ("just dev <name> <路徑>", "開發工具本身時", "把工具指到本機原始碼：寫 .version.local（不進 git）並安裝；之後不做完整性檢查、只印警告", "vendor_kit 容器：--dev install", ".version.local、.<name>/"),
 ("just undev <name>", "改完、要回正式版時", "刪掉 .version.local 那行，立即用 .version 的正式 image 重裝", "vendor_kit 容器：install", ".version.local、.<name>/"),''')
rep(''' ("（自動）", "每個 just 指令執行前", "第 3 頁的檢查：先對專案目錄上鎖 → 印記第一行 ≠ .version → install；相同 → verify（.<name>/ 跟 image 內的 dist 逐檔比）；失敗就中止", "vendor_kit 容器：install 或 verify", ".<name>/（可能重裝）"),''',
    ''' ("（自動）", "每個 just 指令執行前", "第 3 頁的檢查：先對專案目錄上鎖 → 印記第一行 ≠ 有效版本（.version.local 優先於 .version）→ install；相同 → verify（.<name>/ 跟 image 內的 dist 逐檔比）；失敗就中止；本機路徑 → 只印警告", "vendor_kit 容器：install 或 verify", ".<name>/（可能重裝）"),''')
rep('p9.append(v("gB", "1", SW(GREEN), "工具 <name> 提供的指令（由工具的 dist/ 決定，每個工具可以不同；下面以「容器工作流」工具為例）", 40, 570, TBW + 40, 360))', 'p9.append(v("gB", "1", SW(GREEN), "工具 <name> 提供的指令（由工具的 dist/ 決定，每個工具可以不同；下面以「容器工作流」工具為例）", 40, 620, TBW + 40, 360))')
rep('p9.append(v("gC", "1", SW(NEUTRAL), "任何一個 just 指令的完整路徑", 40, 960, TBW + 40, 205))', 'p9.append(v("gC", "1", SW(NEUTRAL), "任何一個 just 指令的完整路徑", 40, 1010, TBW + 40, 205))')
rep('"起 vendor_kit 容器跑子命令\\n（init / diff / accept / dev；upgrade 待議）", 660, 55, 300, 50))', '"起 vendor_kit 容器跑子命令\\n（init / diff / accept；dev = --dev install；upgrade 待議）", 660, 55, 300, 50))')
rep('p9 += legend("p9", 40, 1190,', 'p9 += legend("p9", 40, 1240,')
rep('p9 += terms("p9", 40, 1300, [', 'p9 += terms("p9", 40, 1350, [')
rep(''' ("印記 / .version", ".<name>/.stamp：第一行記裝了哪個 image（之後每檔指紋，追溯用）／專案記工具版本的檔；兩者不同就重裝，相同就拿 .<name>/ 跟 image 內的 dist 比"),''',
    ''' ("印記 / .version", ".<name>/.stamp：第一行記裝了哪個 image（之後每檔指紋，追溯用）／專案記工具版本的檔；兩者不同就重裝，相同就拿 .<name>/ 跟 image 內的 dist 比"),
 ("上鎖 / 結束狀態", "上鎖 = 容器先對專案目錄上鎖，兩個 just 同時跑時後到的等前一個裝完（第 5 頁）／結束狀態 = 指令結束時回報的數字，0 成功、非 0 失敗；diff 用 0／1／2 分別表示沒差異／工具有改／可能撞到"),''')

# ================= 頁 10 =================
rep(''' ("bootstrap", "第一次把工具接進專案的動作；這裡 = release 附的一個腳本，跑完自己刪掉"),''',
    ''' ("bootstrap.sh / bootstrap 子命令", "bootstrap.sh = release 附、在主機跑的腳本（檢查軟體、起容器、問問題、自刪）；bootstrap 子命令 = 容器內真正寫出 .vendor_kit/、justfile、.version 的動作"),
 ("accept", "升級後看完 diff、跟進完，打 just accept <name> 把新版模板存成下次比較的基準（第 5 頁）"),''')
rep('vendor.just：標準指令（init / diff / accept / upgrade 與每個指令前的自動檢查）', 'vendor.just：標準指令（init / diff / accept / dev / undev / upgrade 與每個指令前的自動檢查）')

# ================= 使用者新要求 =================
# (2) 第 1 頁命令介面列全部七個子命令（4 欄）
rep('''p1.append(v("m_cli", "vk", SW(RED), "命令介面", 20, 50, 292, 140))
p1.append(v("cli_land", "m_cli", LEAF(), "install", 12, 45, 88, 40))
p1.append(v("cli_init", "m_cli", LEAF(), "init", 104, 45, 88, 40))
p1.append(v("cli_verify", "m_cli", LEAF(), "verify", 196, 45, 88, 40))
p1.append(v("cli_diff", "m_cli", LEAF(), "diff", 12, 92, 88, 40))
p1.append(v("cli_accept", "m_cli", LEAF(), "accept", 104, 92, 88, 40))
p1.append(v("cli_boot", "m_cli", LEAF(), "bootstrap", 196, 92, 88, 40))''',
'''p1.append(v("m_cli", "vk", SW(RED), "命令介面（子命令，對應第 9 頁指令表）", 20, 50, 384, 140))
p1.append(v("cli_land", "m_cli", LEAF(), "install", 12, 45, 88, 40))
p1.append(v("cli_init", "m_cli", LEAF(), "init", 104, 45, 88, 40))
p1.append(v("cli_verify", "m_cli", LEAF(), "verify", 196, 45, 88, 40))
p1.append(v("cli_diff", "m_cli", LEAF(), "diff", 288, 45, 88, 40))
p1.append(v("cli_accept", "m_cli", LEAF(), "accept", 12, 92, 88, 40))
p1.append(v("cli_boot", "m_cli", LEAF(), "bootstrap", 104, 92, 88, 40))
p1.append(v("cli_upg", "m_cli", LEAF(), "upgrade\\n（待議）", 196, 92, 88, 40))''')
rep('p1.append(e("a2", "m_cli", "m_list", "命令、參數（解析後）", (0.342, 1), (0.5, 0), vert=True))', 'p1.append(e("a2", "m_cli", "m_list", "命令、參數（解析後）", (0.26, 1), (0.5, 0), vert=True))')
# (1) 待回覆便條
PEND = "shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#fff2cc;strokeColor=#d6b656;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;fontSize=12;"
rep('p1 = [v("title", "1", TITLE, "vendor_kit 架構圖（模組 → 最小單元；線上文字 = 傳的資料）", 40, 20, 900, 30)]',
    'p1 = [v("title", "1", TITLE, "vendor_kit 架構圖（模組 → 最小單元；線上文字 = 傳的資料）", 40, 20, 900, 30)]\np1.append(v("p1_pend", "1", PEND, "<b>⚠ 待你回覆</b>\\n命令介面的子命令清單是否就是 install / init / verify / diff / accept / bootstrap / upgrade 七個？", 960, 15, 560, 60))')
rep('p4 = [v("title", "1", TITLE, "流程：vendor_kit 內部——五個子命令（install 是核心）；全部在容器內執行；bootstrap 見第 10 頁", 40, 20, 1200, 30)]',
    'p4 = [v("title", "1", TITLE, "流程：vendor_kit 內部——五個子命令（install 是核心）；全部在容器內執行；bootstrap 見第 10 頁", 40, 20, 1200, 30)]\np4.append(v("p4_pend", "1", PEND, "<b>⚠ 待你回覆</b>\\n1. 主機腳本執行到一半時 .<name>/ 被另一個 just 換掉：第一版不防、寫進限制？\\n2. install 進行中 .version 被改（另一邊 git checkout）：照原本讀到的版本裝完？", 1260, 10, 800, 64))')
rep('p9 = [v("title", "1", TITLE, "使用者介面：指令表（bootstrap.sh 只在第一次；之後全是 just 指令，每個 just 指令前都先自動檢查／安裝）", 40, 20, 1300, 30)]',
    'p9 = [v("title", "1", TITLE, "使用者介面：指令表（bootstrap.sh 只在第一次；之後全是 just 指令，每個 just 指令前都先自動檢查／安裝）", 40, 20, 1300, 30)]\np9.append(v("p9_pend", "1", PEND, "<b>⚠ 待你回覆</b>\\n1. recipe 要不要放命名空間（just kit init／just kit diff…，像既有工具的 just <模組> <動作>，沒有頂層動詞）？\\n2. dev／undev 改成選項式（例如 just kit upgrade --local <name>）而不是給路徑？路徑從哪來？", 40, 55, 1260, 64))')
rep('p12 = [v("title", "1", TITLE, "流程：升級與回退 ── 四條路徑（初版，待決處以便條標示）", 40, 20, 1300, 30)]',
    'p12 = [v("title", "1", TITLE, "流程：升級與回退 ── 四條路徑（初版，待決處以便條標示）", 40, 20, 1000, 30)]\np12.append(v("p12_pend", "1", PEND, "<b>⚠ 待你回覆</b>\\nB：just upgrade 只改 .version 就停？要不要 --dry-run？　C：vendor_kit 要先換自己再換工具嗎？　D：accept 是否強制與 .version 同一個 commit？", 1060, 10, 520, 64))')
rep('p13 = [v("title", "1", TITLE, "對外契約 ── vendor_kit 對外承諾的每一個介面，以及 CI 怎麼隔離（GitHub / GitLab 都只呼叫我們的腳本）", 40, 20, 1500, 30)]',
    'p13 = [v("title", "1", TITLE, "對外契約 ── vendor_kit 對外承諾的每一個介面，以及 CI 怎麼隔離（GitHub / GitLab 都只呼叫我們的腳本）", 40, 20, 1500, 30)]\np13.append(v("p13_pend", "1", PEND, "<b>⚠ 待你回覆</b>\\nGitLab 拉 GHCR 私有 image 的 token 放哪？要不要推兩個 registry？契約檢查腳本用 sh 還是 just？", 1560, 10, 440, 64))')
# (4) 第 2 頁啟動器分組加說明
rep('p1b.append(v("p_vk", "pa", LEAF(), ".vendor_kit/（啟動器本體）\\nvendor.just、tools.just、.stamp、baseline/<name>/", 12, 142, 316, 50).replace("fontSize=14", "fontSize=12"))',
    'p1b.append(v("p_vk", "pa", LEAF(), ".vendor_kit/（啟動器本體）\\nvendor.just、tools.just、.stamp、baseline/<name>/", 12, 142, 316, 50).replace("fontSize=14", "fontSize=12"))\np1b.append(v("pa_t2", "pa", TEXT(11) + "align=left;", "根 justfile 只有一行 import .vendor_kit/vendor.just；工具自己的 tool.just 可用 just 的 mod? 命名空間（just <工具> <動作>，對齊既有工具的分層 just 入口）", 12, 198, 316, 36))')
rep('"啟動器與版本檔", 20, 80, 340, 205))', '"啟動器與版本檔", 20, 80, 340, 245))')
rep('p1b.append(v("p_eng", "proj", PURPLE_LEAF, "安裝容器（<name>-dist:vX）", 20, 330, 300, 60))', 'p1b.append(v("p_eng", "proj", PURPLE_LEAF, "安裝容器（<name>-dist:vX）", 20, 350, 300, 60))')
rep('"以使用者身分執行，跑完即刪；先對專案目錄上鎖", 20, 392, 300, 20))', '"以使用者身分執行，跑完即刪；先對專案目錄上鎖", 20, 412, 300, 20))')
rep('p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 340, 200, 40))', 'p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 360, 200, 40))')
rep('p1b.append(v("tool", "1", SW(GREEN), "工具 repo（每個要出貨的工具一個）", 40, 270, 320, 260))', 'p1b.append(v("tool", "1", SW(GREEN), "工具 repo（每個要出貨的工具一個）", 40, 290, 320, 260))')
rep('p1b.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 550, 320, 130))', 'p1b.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 570, 320, 130))')
rep('p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 520, 200, 40))', 'p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 540, 200, 40))')
rep('p1b.append(v("tool2", "1", SW(GREEN), "另一個工具 repo（<name2>，同型）", 40, 700, 320, 60))', 'p1b.append(v("tool2", "1", SW(GREEN), "另一個工具 repo（<name2>，同型）", 40, 720, 320, 60))')
rep('p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 630, 200, 40))', 'p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 650, 200, 40))')
rep('p1b.append(v("pc2", "proj", SW(NEUTRAL, 14), ".<name2>/（另一個工具）", 540, 625, 220, 50))', 'p1b.append(v("pc2", "proj", SW(NEUTRAL, 14), ".<name2>/（另一個工具）", 540, 645, 220, 50))')
rep('p1b.append(v("pb", "proj", SW(NEUTRAL), "使用者檔案（進 git）", 300, 400, 220, 125))', 'p1b.append(v("pb", "proj", SW(NEUTRAL), "使用者檔案（進 git）", 300, 440, 220, 125))')
rep('p1b.append(v("pc", "proj", SW(NEUTRAL), ".<name>/（不進 git）", 540, 400, 220, 125))', 'p1b.append(v("pc", "proj", SW(NEUTRAL), ".<name>/（不進 git）", 540, 440, 220, 125))')
rep('p1b.append(v("h_docker", "host", LEAF(GREY), "Docker\\n（跑所有容器）", 20, 437.5, 120, 50))', 'p1b.append(v("h_docker", "host", LEAF(GREY), "Docker\\n（跑所有容器）", 20, 477.5, 120, 50))')
for a, b in [('"GHCR（image 倉庫）", 420, 80, 260, 690))', '"GHCR（image 倉庫）", 420, 80, 260, 710))'),
             ('"專案 repo（使用工具的專案）", 740, 80, 770, 690))', '"專案 repo（使用工具的專案）", 740, 80, 770, 710))'),
             ('"使用者的電腦", 1600, 80, 160, 690))', '"使用者的電腦", 1600, 80, 160, 710))'),
             ('p1b += legend("p1b", 40, 800,', 'p1b += legend("p1b", 40, 820,'),
             ('p1b += terms("p1b", 40, 910, [', 'p1b += terms("p1b", 40, 930, [')]:
    rep(a, b)
# (3) 第 9 頁：常用／不常用兩區
start = src.index('# A：vendor_kit 提供')
end = src.index('# C：一個指令的完整路徑')
src = src[:start] + '''# 常用（日常）：工具提供 + 自動檢查
p9.append(v("gB", "1", SW(GREEN), "常用（日常）：工具 <name> 提供的指令（由工具的 dist/ 決定，每個工具可以不同；以「容器工作流」工具為例）＋ 每次的自動檢查", 40, 130, TBW + 40, 420))
yB = table("tb", "gB", 20, 50, [
 ("just build", "第一次、或改了 Dockerfile 之後", "建置專案自己的 image", ".<name>/ 的 build 腳本 → docker compose build", "本機 image（不在 repo 裡）"),
 ("just run", "要開始工作時", "啟動專案容器（在背景常駐）", ".<name>/ 的 run 腳本 → docker compose up", "容器（不在 repo 裡）"),
 ("just exec", "容器跑著的時候", "進到容器裡下指令", ".<name>/ 的 exec 腳本 → docker compose exec", "無"),
 ("just stop", "收工", "停掉並移除容器", ".<name>/ 的 stop 腳本 → docker compose down", "容器（移除）"),
 ("（自動）", "每個 just 指令執行前", "第 3 頁的檢查：先對專案目錄上鎖 → 印記第一行 ≠ 有效版本（.version.local 優先於 .version）→ install；相同 → verify（.<name>/ 跟 image 內的 dist 逐檔比）；失敗就中止；本機路徑 → 只印警告", "vendor_kit 容器：install 或 verify", ".<name>/（可能重裝）"),
])
p9.append(v("gB_n", "gB", NOTE, "為什麼是這四個：它們是「一個容器的一生」— 做出來（build）→ 開起來（run）→ 進去用（exec）→ 關掉（stop），一個階段一個指令。這四個是工具定義的，vendor_kit 只負責把工具裝好；換一個工具，這一區的指令就換一套。\\n每個工具指令前後都可以掛你自己的腳本：script/hooks/pre/<指令>.sh、post/<指令>.sh（init 建立的空殼）。verify 不開放單獨打：它是每個指令前的守門。", 20, yB + 10, TBW, 66))
# 不常用：第一次／升級／開發工具本身（vendor_kit 提供）
p9.append(v("gA", "1", SW(RED), "不常用（第一次／升級／開發工具本身）：vendor_kit 提供的指令，每個用這套框架的專案都一樣", 40, 580, TBW + 40, 440))
yA = table("ta", "gA", 20, 50, [
 ("bootstrap.sh\\n（release 附）", "第一次把 vendor_kit 接進專案", "展開 .vendor_kit/、justfile、.version；問要不要接工具並跑 init；然後刪掉自己（第 10 頁）", "docker run … vendor_kit bootstrap", ".vendor_kit/、justfile、.version（新建）"),
 ("just init", "第一次把工具接進專案", "安裝 .<name>/，再照 init.toml 建立初始檔（Dockerfile、設定檔、hooks…）；已存在的 warn、不覆蓋；並把這版模板存成基準", "vendor_kit 容器：install → init", ".<name>/（新建）、初始檔（新建）、.vendor_kit/baseline/<name>/"),
 ("just diff", "升級之後", "三方比對：印出「工具改了什麼」「你改了什麼」，不改任何檔；結束狀態 0 沒差異／1 工具有改／2 可能重疊", "vendor_kit 容器：diff", "diff 本身不動任何檔（前面的自動檢查可能先更新 .<name>/）"),
 ("just accept <name>", "看完 diff、跟進完之後", "把新版模板存成基準，下次 diff 以它為舊版", "vendor_kit 容器：accept", ".vendor_kit/baseline/<name>/"),
 ("just upgrade", "沒有 Renovate 機器人時，想手動升級", "把 .version 改成最新版 → 重新安裝 → 顯示差異（細節待議，第 11 頁）", "查 GHCR → 改 .version → install → diff", ".version、.<name>/"),
 ("just dev <name> <路徑>\\n（形式待回覆）", "開發工具本身時", "把工具指到本機原始碼：寫 .version.local（不進 git）並安裝；之後不做完整性檢查、只印警告", "vendor_kit 容器：--dev install", ".version.local、.<name>/"),
 ("just undev <name>\\n（形式待回覆）", "改完、要回正式版時", "刪掉 .version.local 那行，立即用 .version 的正式 image 重裝", "vendor_kit 容器：install", ".version.local、.<name>/"),
])
''' + src[end:]
rep('p9.append(v("gC", "1", SW(NEUTRAL), "任何一個 just 指令的完整路徑", 40, 1010, TBW + 40, 205))', 'p9.append(v("gC", "1", SW(NEUTRAL), "任何一個 just 指令的完整路徑", 40, 1050, TBW + 40, 205))')
rep('p9 += legend("p9", 40, 1240,', 'p9 += legend("p9", 40, 1280,')
rep('p9 += terms("p9", 40, 1350, [', 'p9 += terms("p9", 40, 1390, [')

# PEND 樣式定義進產生器
rep('NOTE = "shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#ffffff;strokeColor=#999999;align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;fontSize=12;"',
    'NOTE = "shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#ffffff;strokeColor=#999999;align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;fontSize=12;"\nPEND = "shape=note;whiteSpace=wrap;html=1;size=14;fillColor=#fff2cc;strokeColor=#d6b656;strokeWidth=2;align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;fontSize=12;"')
# ================= 命名空間定案：just vendor_kit …；根 justfile 用 mod? =================
for a, b in [
 ("just init", "just vendor_kit init"), ("just diff", "just vendor_kit diff"), ("just accept", "just vendor_kit accept"),
 ("just upgrade", "just vendor_kit upgrade"), ("just dev", "just vendor_kit dev"), ("just undev", "just vendor_kit undev"),
 ("just build", "just <模組> build"), ("just run", "just <模組> run"), ("just exec", "just <模組> exec"), ("just stop", "just <模組> stop"),
]:
    src = src.replace(a, b)
src = src.replace("just vendor_kit vendor_kit", "just vendor_kit")
rep('第一行 import .vendor_kit/ 的標準指令（啟動器）', '第一行 mod? vendor_kit 把 .vendor_kit/ 的標準指令掛成 just vendor_kit … 命名空間（啟動器）')
rep('justfile（一行 import .vendor_kit/…；之後是', "justfile（一行 mod? vendor_kit '.vendor_kit/vendor.just'；之後是")
rep('第一行 import .vendor_kit/，其餘自己加（第 9 頁）', "第一行 mod? vendor_kit '.vendor_kit/vendor.just'，其餘自己加（第 9 頁）")
rep('justfile 只 import 它', 'justfile 只用 mod? 掛它')
rep('根 justfile 只有一行 import .vendor_kit/vendor.just；工具自己的 tool.just 可用 just 的 mod? 命名空間（just <工具> <動作>，對齊既有工具的分層 just 入口）',
    "根 justfile 只有一行 mod? vendor_kit '.vendor_kit/vendor.just' → 指令都是 just vendor_kit <動作>；工具的 tool.just 也用自己的命名空間（mod? <模組> → just <模組> build）；工具 recipe 開頭先呼叫 just vendor_kit ensure 做自動檢查")
rep('p1b.append(e("f7b", "p_just", "p_vk", "import", (0.5, 1), (0.877, 0), vert=True))', 'p1b.append(e("f7b", "p_just", "p_vk", "mod?", (0.5, 1), (0.877, 0), vert=True))')
rep('("justfile / import", "專案根目錄給 just 讀的指令清單；第一行 import 把 .vendor_kit/ 的標準指令接進來，其餘是使用者自己的")',
    '("justfile / mod?", "專案根目錄給 just 讀的指令清單；第一行 mod? vendor_kit 把 .vendor_kit/ 的標準指令掛成命名空間（just vendor_kit …），其餘是使用者自己的")')
rep('"使用者自己的指令清單（第一行 import）／vendor_kit 的標準指令檔／依 .version 產生的工具指令清單；C 只換後兩者與 .stamp"',
    '"使用者自己的指令清單（第一行 mod? vendor_kit）／vendor_kit 的標準指令檔（just vendor_kit …）／依 .version 產生的工具指令清單；C 只換後兩者與 .stamp"')
rep('"第 3 頁的檢查：先對專案目錄上鎖 → 印記第一行 ≠ 有效版本（.version.local 優先於 .version）→ install；相同 → verify（.<name>/ 跟 image 內的 dist 逐檔比）；失敗就中止；本機路徑 → 只印警告", "vendor_kit 容器：install 或 verify", ".<name>/（可能重裝）"),',
    '"工具的 recipe 開頭先呼叫 just vendor_kit ensure：先對專案目錄上鎖 → 印記第一行 ≠ 有效版本（.version.local 優先於 .version）→ install；相同 → verify（.<name>/ 跟 image 內的 dist 逐檔比）；失敗就中止；本機路徑 → 只印警告", "vendor_kit 容器：install 或 verify", ".<name>/（可能重裝）"),')
rep('("（自動）", "每個 just 指令執行前",', '("（自動）\\njust vendor_kit ensure", "每個工具指令執行前",')
rep('"<b>⚠ 待你回覆</b>\\n1. recipe 要不要放命名空間（just kit init／just kit diff…，像既有工具的 just <模組> <動作>，沒有頂層動詞）？\\n2. dev／undev 改成選項式（例如 just kit upgrade --local <name>）而不是給路徑？路徑從哪來？", 40, 55, 1260, 64))',
    '"<b>⚠ 待你回覆</b>\\ndev／undev 要改成選項式（例如 just vendor_kit upgrade --local <name>）而不是給路徑嗎？本機路徑從哪來？", 40, 55, 1260, 48))')
rep('"常用（日常）：工具 <name> 提供的指令（由工具的 dist/ 決定，每個工具可以不同；以「容器工作流」工具為例）＋ 每次的自動檢查", 40, 130, TBW + 40, 420))',
    '"常用（日常）：工具提供的指令（各工具自己的命名空間 just <模組> <動作>；以「容器工作流」工具的 docker 模組為例）＋ 每次的自動檢查", 40, 130, TBW + 40, 420))')

rep('"跟進完\\n→ just vendor_kit accept <name>", 40, 308, 240, 56))', '"跟進完\\n→ just vendor_kit accept <name>", 30, 308, 240, 56))')
src = src.replace("<b>⚠ 待你回覆</b>\\n", "⚠ 待你回覆：")
rep('p1.append(e("a6", "m_list", "m_write", "dist 全部（寫入、比對）", (1, 0.3), (0, 0.189)))', 'p1.append(e("a6", "m_list", "m_write", "dist 全部", (1, 0.3), (0, 0.189)))')
rep('＋ 每次的自動檢查", 40, 130, TBW + 40, 420))', '＋ 每次的自動檢查", 40, 130, TBW + 40, 470))')
rep('yB = table("tb", "gB", 20, 50, [', 'yB = table("tb", "gB", 20, 50, rh=60, rows=[')
rep('"不常用（第一次／升級／開發工具本身）：vendor_kit 提供的指令，每個用這套框架的專案都一樣", 40, 580, TBW + 40, 440))', '"不常用（第一次／升級／開發工具本身）：vendor_kit 提供的指令，每個用這套框架的專案都一樣", 40, 620, TBW + 40, 520))')
rep('yA = table("ta", "gA", 20, 50, [', 'yA = table("ta", "gA", 20, 50, rh=60, rows=[')
rep('p9.append(v("gC", "1", SW(NEUTRAL), "任何一個 just 指令的完整路徑", 40, 1050, TBW + 40, 205))', 'p9.append(v("gC", "1", SW(NEUTRAL), "任何一個 just 指令的完整路徑", 40, 1170, TBW + 40, 205))')
rep('p9 += legend("p9", 40, 1280,', 'p9 += legend("p9", 40, 1400,')
rep('p9 += terms("p9", 40, 1390, [', 'p9 += terms("p9", 40, 1510, [')
open("gen51.py", "w").write(src)
print("ok")
