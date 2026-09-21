src = open("gen54.py", encoding="utf-8").read()
def rep(a, b, n=1):
    global src
    assert src.count(a) == n, (a[:80], src.count(a))
    src = src.replace(a, b)

# ---------- page 1 ----------
rep('p1.append(v("vk", "1", PURPLE_SW, "vendor_kit（一個 container）", VX, VY, 600, 940))',
    'p1.append(v("vk", "1", PURPLE_SW, "vendor_kit（一個 container）", VX, VY, 660, 940))')
rep('"upgrade\\n（待議）", 196, 92, 88, 40))', '"upgrade", 196, 92, 88, 40))')
rep('p1.append(v("proj", "1", SW(GREEN), "專案 repo 的目錄", 1220, VY, 200, 940))',
    'p1.append(v("proj", "1", SW(GREEN), "專案 repo 的目錄", 1320, VY, 200, 940))')
rep('p1.append(v("p_bl", "proj", LEAF(), "基準\\n（baseline）", 56, 400, 88, 40))',
    'p1.append(v("p_bl", "proj", LEAF(), "基準\\n（baseline）", 56, 420, 88, 40))')
rep('p1.append(v("p_boot", "proj", LEAF(), "啟動器\\n（.vendor_kit/）", 56, 460, 88, 40))',
    'p1.append(v("p_boot", "proj", LEAF(), "啟動器 .vendor_kit/\\n＋ 根目錄的 justfile、.version", 10, 490, 180, 44).replace("fontSize=14", "fontSize=12"))')
rep('"基準（init/accept 寫、diff 讀）", (1, 0.6296), (0, 0.5), both=True))', '"基準（寫／讀）", (1, 0.7037), (0, 0.5), both=True))')
rep('"bootstrap 寫出（.vendor_kit/、justfile、.version）", (1, 0.8519), (0, 0.5)))', '"bootstrap 寫出", (1, 0.9704), (0, 0.5)))')
rep('("upgrade（升級）", "改 .version 換新版本。兩條路：機器人開 PR（人 merge 後，下次 just 才換新）；或 just vendor_kit upgrade（改完立即 install → diff）"),',
    '("upgrade（升級）", "改 .version 換新版本。兩條路：機器人開 PR（人 merge）；或 just vendor_kit upgrade <name>（只改 .version 那行就停）。之後下次 just 才裝新版，再打 just vendor_kit diff 看差異（第 11 頁）"),')
rep('("install / init / verify / diff / accept / bootstrap", "子命令：安裝 dist 到 .<name>/／第一次建立使用者檔／檢查 .<name>/ 沒被改／升級後三方比對／把新版模板存成基準／第一次寫出啟動器（第 10 頁）"),',
    '("install / init / verify / diff / accept / bootstrap / upgrade", "子命令：安裝 dist 到 .<name>/／第一次建立使用者檔／檢查 .<name>/ 沒被改／升級後三方比對／把新版模板存成基準／寫出啟動器（第 10 頁）／查最新版改 .version（第 11 頁）"),')

# ---------- page 2 ----------
rep('p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器與版本檔", 20, 80, 340, 245))',
    'p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器與版本檔", 20, 80, 700, 205))')
rep('（本機開發用，第 4 頁）", 12, 40, 316, 30))', '（本機開發用，第 4 頁）", 12, 34, 676, 36))')
rep('工具 recipe 開頭先呼叫 just vendor_kit ensure 做自動檢查", 12, 198, 316, 36))',
    '工具 recipe 開頭先呼叫 just vendor_kit ensure 做自動檢查", 350, 74, 336, 118))')
rep('justfile = 專案自己的指令清單，第一行 import .vendor_kit/"),',
    'justfile = 專案自己的指令清單，第一行 mod? vendor_kit \'.vendor_kit/vendor.just\' 把它掛進來"),\n ("recipe / 命名空間 / mod? / ensure", "recipe = justfile 裡的一條指令；命名空間 = 指令前的分組名（just vendor_kit …、just <模組> …）；mod? = justfile 把另一個檔掛成命名空間的寫法；ensure = 每個工具指令開頭自動跑的檢查／安裝（第 3 頁）"),')
rep('("upgrade（升級）", "改 .version 換新版本。兩條路：機器人提出合併請求（PR，人 merge 後下次 just 才換新）；或 just vendor_kit upgrade（改完立即 install → diff）"),',
    '("upgrade（升級）", "改 .version 換新版本。兩條路：機器人提出合併請求（PR，人 merge）；或 just vendor_kit upgrade <name>（只改 .version 那行就停）。之後下次 just 才裝新版，再打 just vendor_kit diff（第 11 頁）"),')
rep('p1b += legend("p1b", 40, 820, ["red", "green", "yellow", "pimg", "neutral", "white", "grey", "filebox"], "實線 = 傳輸內容\\n虛線箭頭 = 基底 image → 以它為底的 image；虛線框 = 可有可無的檔")',
    'p1b += [c.replace("虛線框：檔案", "虛線框：可有可無的檔") for c in legend("p1b", 40, 820, ["red", "green", "yellow", "pimg", "neutral", "white", "grey", "filebox"], "實線 = 傳輸內容\\n虛線箭頭 = 基底 image → 以它為底的 image；虛線框 = 可有可無的檔")]')

# ---------- page 3 ----------
rep('照 init.toml 複製初始檔（已存在：warn、不覆蓋）', '照 init.toml 複製初始檔（已存在：警告、不覆蓋）')
rep('p2.append(v("b_note", "bB", NOTE, ".version 一行 = 一個工具：\\n<name> = \\"…-dist:vX@sha256:…\\"\\n等號左邊 = 工具名 → 目錄 .<name>/\\n等號右邊 = image → 跟 .<name>/.stamp 第一行比\\n每一行各跑一次右邊的流程；「否則」= 不同、尚未安裝、印記讀不到\\n例外：右邊是 path:（.version.local）→ 走第 4 頁本機開發模式；\\nvendor_kit 那行 → 換 .vendor_kit/ 程式檔（第 11 頁 C）", 40, 130, 290, 124))',
    'p2.append(v("b_note", "bB", NOTE, ".version 一行 = 一個工具：<name> = \\"…-dist:vX@sha256:…\\"\\n左邊 = 工具名 → 目錄 .<name>/；右邊 = image → 跟 .<name>/.stamp 第一行比\\n每一行各跑一次右邊流程；「否則」= 不同、尚未安裝、印記讀不到\\n例外：右邊是 path:（.version.local）→ 第 4 頁本機開發模式；\\nvendor_kit 那行 → 換 .vendor_kit/ 程式檔（第 11 頁 C）", 30, 130, 300, 150))')
rep("""<mxGeometry relative="1" as="geometry">', '<mxGeometry x="0.7" relative="1" as="geometry">'))""",
    """<mxGeometry relative="1" as="geometry">', '<mxGeometry x="0.5" relative="1" as="geometry">'))""")
rep('p2.append(v("c_u3", "bC", ELLIPSE(GREEN), "看差異，自己決定\\n要不要改", 60, 230, 180, 55))',
    'p2.append(v("c_u3", "bC", LEAF(), "看差異，自己決定\\n要不要改", 60, 230, 180, 55))')
rep('"跟進完\\n→ just vendor_kit accept <name>", 30, 308, 240, 56))', '"跟進完 → just vendor_kit\\naccept <name>", 30, 308, 240, 56))')
rep('沒有 Renovate 時用 just vendor_kit upgrade 手動：改 .version → 立即 install → diff（細節待議）。',
    '沒有 Renovate 時用 just vendor_kit upgrade <name> 手動：只改 .version 那行就停；下次 just 才 install，再自己打 just vendor_kit diff（第 11 頁 B）。')
rep('("just vendor_kit upgrade", "手動升級指令：改 .version → 立即 install → diff（細節待議）"),',
    '("just vendor_kit upgrade", "手動升級指令：只把 .version 那行改成新版就停（不裝、不 diff）；下次 just 才裝，再打 just vendor_kit diff（第 11 頁 B）"),')

# ---------- page 4 ----------
rep('看完跟進 → just vendor_kit accept 存新基準（第 5 頁）', '看完跟進 → just vendor_kit accept <name> 存新基準（第 5 頁）')
rep(' ("印記", ".<name>/.stamp：第一行 = 裝的是哪個 image；本機開發時寫 dev:<路徑>"),',
    ' ("印記", ".<name>/.stamp：第一行 = 裝的是哪個 image；本機開發時寫 dev:<路徑>"),\n ("dev / undev", "just vendor_kit dev <name> <路徑> = 把工具指到本機原始碼（寫 .version.local）；just vendor_kit undev <name> = 移除那行、回正式版；兩者的形式待回覆（第 9 頁）"),')

# ---------- page 5 ----------
rep('照原本讀到的版本裝完？", 1260, 10, 800, 64))', '照原本讀到的版本裝完？", 1260, 4, 800, 50))')
rep('p4.append(v("l4", "install", LEAF(), "清掉殘留的 .<name>.tmp.*", 230, 520, 200, 40))',
    'p4.append(v("l4", "install", LEAF(), "清殘留：刪 .<name>.tmp.*；\\n改到旁邊的舊目錄先改回來", 220, 516, 220, 46).replace("fontSize=14", "fontSize=12"))')
rep('p4.append(v("l7", "install", LEAF(), "舊 .<name>/ 先改名到旁邊 → 暫存目錄\\n改名為 .<name>/ → 刪舊；失敗就改回", 230, 730, 200, 60).replace("fontSize=14", "fontSize=12"))',
    'p4.append(v("l7", "install", LEAF(), "舊 .<name>/ 改名到旁邊 →\\n暫存目錄改名為 .<name>/ → 刪舊", 210, 725, 240, 70).replace("fontSize=14", "fontSize=12"))')
rep('p4.append(v("ln", "install", NOTE, "任一步失敗即中止，舊 .<name>/ 保留；啟動器不會執行 .<name>/ 內的腳本。\\n支援平台：Linux（含 WSL2）amd64／arm64。", 30, 950, 400, 60))',
    'p4.append(v("ln", "install", NOTE, "任一步失敗即中止：改名前失敗 → 舊 .<name>/ 原封不動；兩次改名之間中斷 → 下次 install「清殘留」那步先把旁邊的舊目錄改回來再重裝。失敗時啟動器不會執行 .<name>/ 內的腳本。\\n支援平台：Linux（含 WSL2）amd64／arm64。", 30, 950, 400, 90))')
rep('p4.append(v("install", "1", SW(NEUTRAL), "install（核心：把 dist/ 放進 .<name>/）", 20, 60, 460, 1060))',
    'p4.append(v("install", "1", SW(NEUTRAL), "install（核心：把 dist/ 放進 .<name>/）", 20, 60, 460, 1070))')
rep('p4.append(v("init", "1", SW(NEUTRAL), "init（第一次：建立使用者檔＋存基準）", IX, 60, 480, 780))',
    'p4.append(v("init", "1", SW(NEUTRAL), "init（第一次：建立使用者檔＋存基準）", IX, 60, 480, 810))')
rep('"warn：已存在，不覆蓋\\n（仍把這版模板存成基準）"', '"警告：已存在，不覆蓋\\n（仍把這版模板存成基準）"')
rep('基準 = .vendor_kit/baseline/<name>/", 30, 725, 420, 44))', '基準 = .vendor_kit/baseline/<name>/", 30, 725, 420, 64))')
rep('p4.append(v("v1", "verify", LEAF(), "對專案目錄上鎖（共享；逾時規則同 install）\\n讀印記第一行（已裝版本）", 130, 130, 200, 40).replace("fontSize=14", "fontSize=12"))',
    'p4.append(v("v1", "verify", LEAF(), "對專案目錄上鎖（共享；逾時同 install）\\n讀印記第一行（已裝版本）", 90, 125, 280, 50).replace("fontSize=14", "fontSize=12"))')
rep('p4.append(v("diff", "1", SW(NEUTRAL), "diff（升級後：三方比對，只印不改）", DX, 60, 560, 600))',
    'p4.append(v("diff", "1", SW(NEUTRAL), "diff（升級後：三方比對，只印不改）", DX, 60, 560, 650))')
rep('"有基準？（baseline/<name>/，\\n且沒被手改：verify 也檢查它）", 60, 130, 200, 80).replace("fontSize=14", "fontSize=11"))',
    '"有基準？（baseline/<name>/\\n存在且指紋相符）", 60, 130, 200, 80).replace("fontSize=14", "fontSize=12"))')
rep('p4.append(v("d_two", "diff", LEAF(), "二方：新版模板 vs 你的檔，提示「無基準」\\n結束狀態 0 沒差異／1 有差異（分不出誰改）", 320, 250, 220, 60).replace("fontSize=14", "fontSize=12"))',
    'p4.append(v("d_two", "diff", LEAF(), "二方：新版模板 vs 你的檔\\n提示「無基準或基準被改」\\n結束狀態 0 沒差異／1 有差異（分不出誰改）", 320, 250, 220, 76).replace("fontSize=14", "fontSize=12"))')
rep('p4.append(v("d3", "diff", LEAF(), "印兩份：基準→新版（工具改了）、基準→你的（你改了）\\n同一檔兩邊都有改 → 標「可能重疊」（不判定是否同一行）", 20, 340, 280, 60).replace("fontSize=14", "fontSize=12"))',
    'p4.append(v("d3", "diff", LEAF(), "印兩份：基準→新版（工具改了）、基準→你的（你改了）\\n同一檔兩邊都有改 → 標「可能重疊」（不判定是否同一行）", 20, 345, 280, 76).replace("fontSize=14", "fontSize=12"))\np4.append(v("d_code", "diff", LEAF(), "算結束狀態：0 = 沒人改／只有你改／已套上；\\n1 = 有「只有工具改」；2 = 有「兩邊都改」", 20, 445, 280, 50).replace("fontSize=14", "fontSize=12"))')
rep('p4.append(v("d4", "diff", ELLIPSE(GREEN), "結束（不改任何檔）結束狀態：0 = 沒人改／只有你改／已套上；\\n1 = 有「只有工具改」；2 = 有「兩邊都改」", 10, 440, 300, 60).replace("fontSize=14", "fontSize=12"))',
    'p4.append(v("d4", "diff", ELLIPSE(GREEN), "結束（不改任何檔）", 80, 520, 160, 50))')
rep('第二版再做。", 20, 520, 520, 40))', '第二版再做。", 20, 595, 520, 40))')
rep('p4.append(e("de2", "d1", "d_two", "沒有", (1, 0.5), (0.5, 0)))', 'p4.append(e("de2", "d1", "d_two", "沒有／被改", (1, 0.5), (0.5, 0)))')
rep('p4.append(e("de3", "d2", "d3")); p4.append(e("de4", "d3", "d4"))', 'p4.append(e("de3", "d2", "d3")); p4.append(e("de4", "d3", "d_code")); p4.append(e("de4b", "d_code", "d4"))')
rep('<mxPoint x="430" y="470"/></Array></mxGeometry></mxCell>\')\n# accept', '<mxPoint x="430" y="545"/></Array></mxGeometry></mxCell>\')\n# accept')
rep('上次確認過的模板副本＋metadata；accept = 把新版模板寫成基準的子命令"),', '上次確認過的模板副本＋來源版本與每檔指紋；accept = 把新版模板寫成基準的子命令"),')

# ---------- page 7 (p10) ----------
rep('"我們要開發的安裝工具的 repo；只有 src/ 會進最終出貨的 image，其餘都是開發用"', '"我們要開發的安裝工具的 repo；只有 src/ 與 test/ci/check.sh 會進最終出貨的 image，其餘都是開發用"')
rep('"命令介面：讀參數、分派 install / init / verify / diff / accept（第一次另有 bootstrap，第 10 頁）"', '"命令介面：讀參數、分派 install / init / verify / diff / accept / upgrade（另有 bootstrap，第 10、11 頁）"')
rep('system／acceptance 在 CI 主機跑；都不進出貨 image"),', 'system／acceptance 在 CI 主機跑；除 ci/check.sh 外都不進出貨 image"),')
rep('"給下游專案用的契約檢查腳本（第 12 頁）：bootstrap 寫出到專案，GitHub／GitLab 的 CI 只呼叫它"', '"給下游專案用的契約檢查腳本（第 12 頁）：唯一會 COPY 進出貨 image 的測試檔，bootstrap 寫到專案的 test/ci/check.sh，GitHub／GitLab 的 CI 只呼叫它"')
rep('"設計決策紀錄：一個決策一個 Markdown 檔（例：測試分層與閘門）"', '"設計決策紀錄：一個決策一個文字文件（例：測試分層與閘門）"')
rep('人不改（納入檢查）；升級不動"),', '人不改（diff 前檢查指紋）；升級不動"),')
rep(' (1, "script/hooks/", False, "進 git｜使用者的掛勾腳本：每個工具指令前後自動執行（init 建立的空殼）"),',
    ' (1, "script/hooks/", False, "進 git｜使用者的掛勾腳本：每個工具指令前後自動執行（init 建立的空殼）"),\n (1, "test/ci/check.sh", True, "進 git｜契約檢查腳本（bootstrap 寫出，之後歸專案）：GitHub／GitLab 的 CI 只呼叫它（第 12 頁）"),\n (1, "renovate.json", True, "進 git｜Renovate 設定（bootstrap 寫出）：只含 extends，指向 vendor_kit 的共用 preset（第 11 頁 A）"),')
rep('不進 git = 不由 git 保存、只在這台機器，隨時可刪掉重裝"),', '不進 git = 不由 git 保存、只在這台機器（.<name>/ 隨時可刪掉重裝；.version.local 是你自己的本機設定）"),')
rep('vendor_kit repo 只有 src/ 會進最終出貨的 image，測試只進測試用的 stage 或在 CI 主機跑"),', 'vendor_kit repo 只有 src/ 與 test/ci/check.sh 會進最終出貨的 image，其他測試只進測試用的 stage 或在 CI 主機跑"),')
rep(' ("TOML / tomllib / VERSION / pytest", "設定檔格式（.version、init.toml）／Python 讀 TOML 的內建程式庫／image 內給人看的識別字串（印記第一行改由啟動器用 --self 傳入的 .version 字串，issue #23）／Python 測試框架"),\n ("ruff / import-linter / 鏡射 / 黑箱 / 記下是哪個 image", "Python 寫法檢查／檢查模組之間誰能引用誰／每個模組必有對應測試檔／system、acceptance 測試不准引用 vendor_kit 程式／基準旁邊記的來源 image 與每檔指紋"),',
    ' ("TOML / tomllib / pytest", "設定檔格式（.version、init.toml）／Python 讀 TOML 的內建程式庫／Python 測試框架"),\n ("VERSION", "image 內給人看的識別字串（印記第一行改由啟動器用 --self 傳入的 .version 字串，issue #23）"),\n ("ruff / import-linter", "Python 寫法檢查／檢查模組之間誰能引用誰"),\n ("鏡射 / 黑箱 / 記下是哪個 image", "每個模組必有對應測試檔／system、acceptance 測試不准引用 vendor_kit 程式／基準旁邊記的來源 image 與每檔指紋"),')
rep('p10 += terms("p10", 40, 70 + 50 + len(VK) * RH + 20 + 150, [', 'p10 += terms("p10", 40, 70 + 50 + len(VK) * RH + 20 + 150, rh=36, rows=[')

# ---------- page 8 (p8) ----------
rep('COLH = 1130', 'COLH = 1150')
rep('p8.append(v("d_note", "repo", TEXT(11), "完整資料夾架構見第 7 頁", 20, 1090, 380, 18))', 'p8.append(v("d_note", "repo", TEXT(11), "完整資料夾架構見第 7 頁", 20, 1122, 380, 18))')
rep('p8.append(v("d_ci", "repo", LEAF(), ".github/workflows/ ＋ test/ci/check.sh（給下游，第 12 頁）\\nbake validate → system/acceptance → release（兩種架構）", 20, 1036, 380, 44).replace("fontSize=14", "fontSize=12"))',
    'p8.append(v("d_ci", "repo", LEAF(), ".github/workflows/（vendor_kit 自己的 CI）\\nbake validate → system/acceptance → release（兩種架構）", 20, 1030, 380, 40).replace("fontSize=14", "fontSize=12"))\np8.append(v("d_ci2", "repo", LEAF(), "test/ci/check.sh：給下游專案的契約檢查腳本（第 12 頁）\\n不在自己的 CI 序列裡；COPY 進 image 供 bootstrap 寫出", 20, 1076, 380, 40).replace("fontSize=14", "fontSize=12"))')
rep('("g5", "integration conftest\\n只給臨時目錄；禁 Docker、網路；只能走 cli.main()（程式的正門）"),', '("g5", "integration conftest\\n只給臨時目錄；禁 Docker、網路、啟動其他程序（subprocess／socket 全禁）；只能走 cli.main()（程式的正門）"),')
rep('（量容器內的函式，不含起容器；每次 just 都會跑它）")])', '（量容器內的函式，不含起容器；除剛 install 完與本機模式外每次 just 都跑它）")])')

# ---------- page 9 ----------
rep('"⚠ 待你回覆：dev／undev 要改成選項式（例如 just vendor_kit upgrade --local <name>）而不是給路徑嗎？本機路徑從哪來？", 40, 55, 1260, 48))',
    '"⚠ 待你回覆：1. dev／undev 要改成選項式（例如 just vendor_kit upgrade --local <name>）而不是給路徑嗎？本機路徑從哪來？\\n2. 審查者建議（未改，等你決定）：A 表的 run／stop 與 B 表三欄完全相同，是否只留 B 表並標「使用者也用」？diff（B）與 accept（C）是同一人連續做的兩步，要不要放同一角色？「什麼時候打」與「使用情景」兩欄重疊，要不要合併？", 40, 55, 1460, 64))')
rep('p9.append(v("gU", "1", SW(YELLOW), "A. 使用者（拿專案成果來用的人）：只有「跑起來、停掉」，不 build、不 exec；工具有提供才有", 40, 130, TBW + 40, 240))',
    'p9.append(v("gU", "1", SW(NEUTRAL), "A. 使用者（拿專案成果來用的人）：只有「跑起來、停掉」，不 build、不 exec；工具有提供才有", 40, 140, TBW + 40, 290))')
rep('p9.append(v("gB", "1", SW(GREEN), "B. 開發者（天天在專案裡寫程式的人）：工具命名空間的四個指令 ＋ 升級後看差異", 40, 400, TBW + 40, 540))',
    'p9.append(v("gU_n", "gU", NOTE, "跟 B 表一樣，每個工具指令開頭都先自動檢查／安裝（just vendor_kit ensure），所以 .<name>/、印記、tools.just 可能在指令前被更新；「動到專案裡的什麼」欄只寫指令本身動的。", 20, yU + 10, TBW, 40))\np9.append(v("gB", "1", SW(NEUTRAL), "B. 開發者（天天在專案裡寫程式的人）：工具命名空間的四個指令 ＋ 升級後看差異", 40, 460, TBW + 40, 540))')
rep('".<name>/ 的 exec 腳本 → docker compose exec", "無",', '".<name>/ 的 exec 腳本 → docker compose exec", "無（前置檢查除外，見下方便條）",')
rep('由工具定義（以「容器工作流」工具的 docker 模組為例），換工具就換一套', '由工具定義（以「容器工作流」類的工具為例），換工具就換一套')
rep('相同 → verify；失敗就中止）——人不會直接打。", 20, yB + 10, TBW, 66))', '相同 → verify；失敗就中止）——人不會直接打，所以 .<name>/、印記、tools.just 可能在指令前被更新。", 20, yB + 10, TBW, 66))')
rep('p9.append(v("gM", "1", SW(RED), "C. 專案維護者（把工具接進專案、處理升級的人）", 40, 970, TBW + 40, 390))',
    'p9.append(v("gM", "1", SW(NEUTRAL), "C. 專案維護者（把工具接進專案、處理升級的人）", 40, 1030, TBW + 40, 390))')
rep('"docker run … vendor_kit bootstrap", ".vendor_kit/、justfile、.version（新建）"', '"docker run … vendor_kit bootstrap", ".vendor_kit/、justfile、.version、test/ci/check.sh、renovate.json（新建）"')
rep('("just vendor_kit init", "第一次把工具接進專案", "安裝 .<name>/，再照 init.toml 建立初始檔（Dockerfile、設定檔、hooks…）；已存在的 warn、不覆蓋；並把這版模板存成基準", "vendor_kit 容器：install → init", ".<name>/、初始檔（都新建）、基準 baseline/<name>/",',
    '("just vendor_kit init", "第一次把工具接進專案（先在 .version 加一行 <name> = \\"image\\"）", "安裝 .<name>/，再照 init.toml 建立初始檔（Dockerfile、設定檔、hooks…）；已存在的警告、不覆蓋；並把這版模板存成基準", "vendor_kit 容器：install → init", ".<name>/（新建）、初始檔（已存在的不動）、基準 baseline/<name>/",')
rep('"沒有 Renovate 時唯一改 .version 的方式；有 Renovate 就幾乎用不到"', '"自動查最新版與 digest 改 .version，不用手填；有 Renovate 就幾乎用不到"')
rep('p9.append(v("gD", "1", SW(RED), "D. 工具開發者（改工具本身的人；一般專案用不到）", 40, 1390, TBW + 40, 250))',
    'p9.append(v("gD", "1", SW(NEUTRAL), "D. 工具開發者（改工具本身的人；一般專案用不到）", 40, 1450, TBW + 40, 250))')
rep('p9.append(v("gC", "1", SW(NEUTRAL), "任何一個 just 指令的完整路徑", 40, 1670, TBW + 40, 205))', 'p9.append(v("gC", "1", SW(NEUTRAL), "任何一個 just 指令的完整路徑", 40, 1730, TBW + 40, 205))')
rep('p9.append(v("c1", "gC", LEAF(), "自動檢查／安裝\\n（第 3 頁「日常」）", 220, 95, 180, 50))', 'p9.append(v("c1", "gC", LEAF(), "自動檢查／安裝 ensure\\n（第 3 頁「日常」）", 440, 135, 180, 50))')
rep('p9.append(v("c2", "gC", RHOMBUS, "X 是誰的？", 440, 80, 160, 80))', 'p9.append(v("c2", "gC", RHOMBUS, "X 是誰的？", 220, 80, 160, 80))')
rep('p9.append(e("ce0", "c0", "c1", "", (1, 0.5), (0, 0.5)))\np9.append(e("ce1", "c1", "c2", "通過", (1, 0.5), (0, 0.5)))\np9.append(e("ce2", "c2", "c3", "vendor_kit 的", (0.5, 0), (0, 0.5)).replace(\'endFill=1;\', \'endFill=1;jettySize=0;\', 1))\np9.append(e("ce3", "c2", "c4", "工具的", (0.5, 1), (0, 0.5)).replace(\'endFill=1;\', \'endFill=1;jettySize=0;\', 1))',
    'p9.append(e("ce0", "c0", "c2", "", (1, 0.5), (0, 0.5)))\np9.append(e("ce1", "c1", "c4", "通過", (1, 0.5), (0, 0.5)))\np9.append(e("ce2", "c2", "c3", "vendor_kit 的", (0.5, 0), (0, 0.5)).replace(\'endFill=1;\', \'endFill=1;jettySize=0;\', 1))\np9.append(e("ce3", "c2", "c1", "工具的", (0.5, 1), (0, 0.5)).replace(\'endFill=1;\', \'endFill=1;jettySize=0;\', 1))')
rep('p9 += legend("p9", 40, 1905, ["red", "green", "neutral", "white", "pimg", "startend", "rhomb", "notebox"], "表格：一列一個指令\\n流程：實線 = 執行順序")',
    'p9 += legend("p9", 40, 1965, ["neutral", "white", "pimg", "startend", "rhomb", "notebox"], "表格：一列一個指令\\n流程：實線 = 執行順序")')
rep('p9 += terms("p9", 40, 2015, [\n ("子命令 / dist/", "子命令 = vendor_kit 容器裡的動作：install 把 dist 裝進 .<name>/ 並寫印記、init 建初始檔＋存基準、verify 拿 .<name>/ 跟 image 內的 dist 比、diff 三方比模板、accept 存新基準；bootstrap 只在第一次寫出啟動器（第 10 頁）；dist/ = 工具要出貨的檔案"),',
    'p9 += terms("p9", 40, 2075, rh=36, rows=[\n ("子命令", "vendor_kit 容器裡的動作：install 把 dist 裝進 .<name>/ 並寫印記、init 建初始檔＋存基準、verify 拿 .<name>/ 跟 image 內的 dist 比、diff 三方比模板、accept 存新基準、upgrade 查最新版改 .version；bootstrap 寫出啟動器（第一次，第 10 頁；vendor_kit 自我升級時再跑一次，第 11 頁 C）"),\n ("dist/ / <模組>", "dist/ = 工具要出貨的檔案；<模組> = 工具的 tool.just 掛上的命名空間名（tools.just 裡 mod? <模組>），由工具自己決定，通常就跟 <name> 一樣"),\n ("registry / recipe", "image 倉庫（GHCR 等）／justfile 裡的一條指令"),\n ("有效版本 / 完整性檢查", ".version.local 有同名那行就用它、否則用 .version 的那行／verify：拿 .<name>/ 跟 image 內的 dist 逐檔比"),')

# ---------- page 10 (p11) ----------
rep('p11.append(v("u1", "bs", ELLIPSE(GREEN), "完成：專案裡只剩\\n.vendor_kit/、justfile、.version\\n（＋ .<name>/、初始檔）", 30, 545, 240, 70))',
    'p11.append(v("u1", "bs", ELLIPSE(GREEN), "完成：專案裡多了 .vendor_kit/、justfile、\\n.version、test/ci/check.sh、renovate.json\\n（＋ .<name>/、初始檔）", 20, 545, 260, 80).replace("fontSize=14", "fontSize=12"))')
rep('p11.append(v("c1", "bs", PURPLE_LEAF, "bootstrap 子命令\\n寫出啟動器與版本檔（不碰其他檔）\\n--self = 要寫進 .version 與印記的 vendor_kit 字串", 760, 215, 340, 180).replace("fontSize=14", "fontSize=13"))',
    'p11.append(v("c1", "bs", PURPLE_LEAF, "bootstrap 子命令\\n寫出啟動器、版本檔、契約檢查腳本與 renovate.json（不碰其他檔）；.gitignore 加一行 .version.local\\n--self = 要寫進 .version 與印記的 vendor_kit 字串", 760, 215, 340, 250).replace("fontSize=14", "fontSize=13"))')
rep('tools.just：依 .version 產生的工具指令清單；.stamp：記 vendor_kit 版本', 'tools.just：依 .version 產生的工具指令清單（每次 install 後重寫）；.stamp：記 vendor_kit 版本')
rep('p11.append(v("f2", "bs", FILE, "justfile（一行 mod? vendor_kit \'.vendor_kit/vendor.just\'；之後是\\n使用者自己的指令，進 git；已存在就不動）", 1160, 311, 340, 44))',
    'p11.append(v("f2", "bs", FILE, "justfile（一行 mod? vendor_kit \'.vendor_kit/vendor.just\'；\\n之後是使用者自己的指令，進 git；已存在就不動）", 1160, 311, 340, 56).replace("fontSize=14", "fontSize=12"))')
rep('p11.append(v("f3", "bs", FILE, ".version（先只有 vendor_kit 一行，進 git；已存在就不動）", 1160, 361, 340, 36).replace("fontSize=14", "fontSize=12"))',
    'p11.append(v("f3", "bs", FILE, ".version（先只有 vendor_kit 一行，進 git；已存在就不動）", 1160, 375, 340, 36).replace("fontSize=14", "fontSize=12"))\np11.append(v("f3b", "bs", FILE, "test/ci/check.sh、renovate.json（進 git，之後歸專案；第 11、12 頁）", 1160, 418, 340, 36).replace("fontSize=14", "fontSize=12"))')
rep('p11.append(e("be5", "c1", "f1", "寫出", (1, 0.25), (0, 0.5)))\np11.append(e("be6", "c1", "f2", "沒有才寫", (1, 0.6556), (0, 0.5)))\np11.append(e("be7", "c1", "f3", "沒有才寫", (1, 0.9111), (0, 0.5)))',
    'p11.append(e("be5", "c1", "f1", "寫出", (1, 0.18), (0, 0.5)))\np11.append(e("be6", "c1", "f2", "沒有才寫", (1, 0.496), (0, 0.5)))\np11.append(e("be7", "c1", "f3", "沒有才寫", (1, 0.712), (0, 0.5)))\np11.append(e("be7b", "c1", "f3b", "寫出", (1, 0.884), (0, 0.5)))')
rep('("--self / tools.just / baseline/", "--self = 啟動器傳給容器的 vendor_kit image 字串／依 .version 產生的工具指令 import 清單／三方比對的基準副本（第 5 頁）"),',
    '("--self / tools.just / baseline/", "--self = 啟動器傳給容器的 vendor_kit image 字串／依 .version 產生、每次 install 後重寫的工具指令清單（用 mod? 掛進 just）／三方比對的基準副本（第 5 頁）"),')
rep('("以使用者身分", "docker run -u UID:GID：容器寫出的檔案擁有者是你，不是 root"),', '("以使用者身分", "docker run -u UID:GID（你在主機的使用者與群組編號）：容器寫出的檔案擁有者是你，不是 root（系統管理者帳號）"),\n ("契約檢查腳本 / renovate.json", "test/ci/check.sh：下游 CI 只呼叫它（第 12 頁）／Renovate 的設定檔，只含 extends 指向 vendor_kit 的共用設定（第 11 頁 A）"),')

# ---------- page 11 (p12) ----------
rep('p12 = [v("title", "1", TITLE, "流程：升級與回退 ── 四條路徑（初版，待決處以便條標示）", 40, 20, 1000, 30)]', 'p12 = [v("title", "1", TITLE, "流程：升級與回退 ── 四條路徑（初版，待決處以便條標示）", 40, 20, 580, 30)]')
rep('由誰 commit（人手，CI 紅燈提醒）？", 1060, 10, 520, 90))', '由誰 commit（人手，CI 紅燈提醒）？", 640, 6, 940, 50))')
rep('p12.append(v("a2", "uA", LEAF(), "CI 在 PR 上自動跑 just\\n（install + verify + 工具的煙霧測試）", 320, 205, 240, 50).replace("fontSize=14", "fontSize=12"))',
    'p12.append(v("a2", "uA", LEAF(), "CI 在 PR 上跑契約檢查腳本 test/ci/check.sh\\n（範例；深淺由專案決定）", 310, 205, 260, 50).replace("fontSize=14", "fontSize=12"))')
rep('p12.append(v("a7", "uA", LEAF(), "just vendor_kit diff → 跟進 → just vendor_kit accept\\n（第 5 頁 diff／accept 泳道）", 60, 375, 220, 60).replace("fontSize=14", "fontSize=12"))',
    'p12.append(v("a7", "uA", LEAF(), "just vendor_kit diff <name> → 跟進 →\\njust vendor_kit accept <name>\\n（第 5 頁 diff／accept 泳道）", 50, 375, 240, 60).replace("fontSize=14", "fontSize=12"))')
rep('p12.append(v("b2", "uB", PURPLE_LEAF, "查 registry（OCI API）：<name>-dist 最新 tag + digest\\n（要網路；只查不裝）", 940, 60, 280, 50))',
    'p12.append(v("b2", "uB", PURPLE_LEAF, "查 registry（OCI API）：\\n<name>-dist 最新 tag + digest（要網路；只查不裝）", 940, 55, 280, 60).replace("fontSize=14", "fontSize=12"))')
rep('p12.append(v("b4", "uB", LEAF(), "停：印「尚未安裝，下一步 just vendor_kit diff」\\n之後每個人下次打 just 才 install（同 A）", 600, 170, 280, 50).replace("fontSize=14", "fontSize=12"))',
    'p12.append(v("b4", "uB", LEAF(), "upgrade 結束：印「尚未安裝，下一步 just vendor_kit diff <name>」\\n之後每個人下次打 just 才 install（同 A）", 600, 165, 280, 60).replace("fontSize=14", "fontSize=12"))')
rep('p12.append(v("b5", "uB", ELLIPSE(GREEN), "just vendor_kit diff → 跟進 → accept\\n→ commit .version 與修改", 60, 165, 220, 60))',
    'p12.append(v("b5", "uB", LEAF(), "just vendor_kit diff <name> → 跟進 →\\njust vendor_kit accept <name>（同 A）", 40, 155, 240, 46).replace("fontSize=14", "fontSize=12"))\np12.append(v("b6", "uB", ELLIPSE(GREEN), "結束：commit .version 與你的修改", 40, 215, 240, 40).replace("fontSize=14", "fontSize=12"))')
rep("""p12.append('<mxCell id="be4" value="下次 just 讀到" style="' + EDGE + 'verticalAlign=top;spacingTop=6;spacingBottom=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="uB" source="b3" target="b4"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="1410" y="140"/><mxPoint x="740" y="140"/></Array></mxGeometry></mxCell>')""",
    """p12.append('<mxCell id="be4" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="uB" source="b3" target="b4"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="1410" y="132"/><mxPoint x="740" y="132"/></Array></mxGeometry></mxCell>')""")
rep('p12.append(e("be5", "b4", "b5", "", (0, 0.5), (1, 0.5)))', 'p12.append(e("be5", "b4", "b5", "", (0, 0.5), (1, 0.5)))\np12.append(e("be6", "b5", "b6", "", (0.5, 1), (0.5, 0)))')
rep('或環境變數 token。", 940, 140, 600, 100))', '或環境變數 token。", 940, 150, 600, 100))')
rep(' ("CI / 煙霧測試", "CI = GitHub 上的自動檢查，PR 一開就跑；煙霧測試 = 最小的一次實跑（例如 just <模組> build 能過）"),',
    ' ("CI / 契約檢查腳本 / renovate.json", "CI = GitHub／GitLab 上的自動檢查，PR 一開就跑／test/ci/check.sh：vendor_kit 出貨、bootstrap 寫到專案的檢查腳本（第 12 頁）／Renovate 的設定檔，只含 extends"),\n ("registry / OCI API", "image 倉庫（GHCR、GitLab 都是）／它們共同遵守的標準查詢介面，所以同一段程式兩邊都能查"),\n ("preset / extends / runner", "Renovate 的共用設定檔（放在 vendor_kit repo）／專案的 renovate.json 用 extends 指向它／GitLab 上自己架的 Renovate 執行器"),\n ("token / multi-arch index", "登入 registry 用的密碼字串／同一 image 同時含 amd64 與 arm64 的索引，digest 鎖的是它"),\n ("LABEL / docker image inspect / --dry-run", "寫在 image 上的標籤（帶契約版本號）／讀 image 標籤的指令／只顯示會改什麼、不真的改（--check 同）"),\n ("recipe", "justfile 裡的一條指令；just 啟動時整份讀進記憶體，跑到一半改檔本次無效"),')
rep('p12 += terms("p12", 40, 1540, [', 'p12 += terms("p12", 40, 1540, rh=36, rows=[')

# ---------- page 12 (p13) ----------
rep('p13.append(v("ct", "1", SW(RED), "對外契約（五個介面；①依角色分四行）", 40, 70, CW + 40, 570))', 'p13.append(v("ct", "1", SW(NEUTRAL), "對外契約（五個介面；①依角色分四行）", 40, 70, CW + 40, 570))')
rep('image 內 /dist 的佈局（files/、init.toml、VERSION）', 'image 內 /dist 的佈局（dist/ 原樣、init.toml、VERSION）')
rep('"dist/（全部出貨、與架構無關、不含 symlink）；init.toml 格式（[[file]] src/dest）；dist/just/tool.just（工具自己的指令）；Dockerfile.dist（FROM vendor_kit + COPY）；image 命名 <name>-dist:tag，multi-arch（amd64 + arm64）", "env-test / release-test（用 fixtures 假工具）；工具 repo 的 CI"',
    '"dist/（全部出貨、不含 symlink）；init.toml 格式（[[file]] src/dest）；dist/just/tool.just（工具自己的指令）；Dockerfile.dist（FROM vendor_kit + COPY）；image 命名 <name>-dist:tag，且支援兩種架構（multi-arch amd64 + arm64）", "release-test 與 system 測試（用 fixtures 假工具）；工具 repo 的 CI"')
rep('"一組平台無關的測試腳本（下方），內容 = 上面四條契約的檢查；GitHub / GitLab 的 CI 檔只負責呼叫它"', '"test/ci/check.sh（平台無關，下方）＋ renovate.json（只含 extends）；腳本內容 = 上面四條契約的檢查；GitHub / GitLab 的 CI 檔只負責呼叫它"')
rep('p13.append(v("ci_bake", "ci", PURPLE_LEAF, "docker buildx bake validate / release\\n（vendor_kit 自己的測試，第 8 頁）", 920, 50, 380, 50))',
    'p13.append(v("ci_bake", "ci", LEAF(), "vendor_kit 自己的 CI（第 8 頁）：\\nbake validate → system／acceptance → bake release", 920, 50, 380, 50).replace("fontSize=14", "fontSize=12"))')
rep('p13 += legend("p13", 40, 970, ["red", "yellow", "pimg", "neutral", "white"], "實線 = 呼叫／依賴方向")', 'p13 += legend("p13", 40, 970, ["yellow", "neutral", "white"], "實線 = 呼叫／依賴方向")')
rep('p13 += terms("p13", 40, 1080, [\n ("對外契約", "我們承諾「這樣用一定可以、不會隨便改」的介面清單；改了就要升版並公告"),',
    'p13 += terms("p13", 40, 1080, rh=36, rows=[\n ("對外契約", "我們承諾「這樣用一定可以、不會隨便改」的介面清單；改了就要升版並公告"),\n ("image / dist / TOML / baseline / 印記", "打包好的程式與檔案／工具要出貨的檔案／設定檔格式／上次確認過的模板副本（.vendor_kit/baseline/<name>/）／.<name>/.stamp，記裝了哪個 image"),\n ("symlink / sha256 / digest", "指向別檔的捷徑（第一版禁止）／檔案內容指紋／image 內容指紋"),\n ("FROM / COPY / bake", "Dockerfile 指令：以哪個 image 為底／把檔放進去／docker buildx bake：一次跑多個 stage 的工具"),\n ("測試層級", "acceptance = 在假專案真的打 just；system = docker run 每個子命令；integration = 一個子命令走到底；release-test = 出貨前真的裝一次（第 8 頁）"),\n ("Renovate / renovate.json / 契約檢查腳本", "自動開 PR 改 .version 的機器人／它的設定檔（bootstrap 寫出、只含 extends）／test/ci/check.sh，bootstrap 寫到專案"),')

open("gen55.py", "w", encoding="utf-8").write(src)
print("ok")
