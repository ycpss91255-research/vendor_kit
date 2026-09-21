src = open("gen28.py").read()
def rep(a, b):
    global src; assert src.count(a) == 1, a[:70]; src = src.replace(a, b)
# 圖例新項目
rep(''' "pstage": (PURPLE_LEAF,        "紫：image（每個 stage 都是一個 image）", 270, 40, 10),''',
''' "pstage": (PURPLE_LEAF,        "紫：image（每個 stage 都是一個 image）", 270, 40, 10),
 "folder": (LEAF(),             "實線框：資料夾", 120, 40, 10),
 "filebox":(FILE,               "虛線框：檔案", 120, 40, 10),
 "rhomb":  (RHOMBUS,            "黃：判斷", 110, 60, 0),
 "startend":(ELLIPSE(GREEN),    "綠橢圓：起點／終點", 160, 40, 10),
 "notebox":(NOTE,               "便條：補充說明", 130, 40, 10),''')
# ---- 第 7 頁 ----
rep('(0, "vendor_kit/", False, "我們要開發的安裝工具；只有 src/ 會進 image，其餘都是開發用"),',
    '(0, "vendor_kit/", False, "我們要開發的安裝工具的 repo；只有 src/ 會進最終出貨的 image，其餘都是開發用"),')
rep('(1, "src/vendor_kit/", False, "產品程式碼：7 個 Python 模組（= 第 1 頁的 7 個模組），一個模組一個檔"),',
    '(1, "src/vendor_kit/", False, "產品程式碼：7 個 Python 模組（= 第 1 頁的 7 個模組，一個模組一個檔）＋ 進入點"),')
rep('(1, "test/", False, "所有測試與檢查（不進 image）；先分測試工具、再分層級"),',
    '(1, "test/", False, "所有測試與檢查（只進測試用的 stage，不進出貨 image）；先分測試工具、再分層級"),')
rep('"自寫的檢查腳本：鏡射（每模組必有測試）、黑箱（system/acceptance 不准 import）"', '"自寫的檢查腳本：鏡射（每模組必有測試）、黑箱（system/acceptance 測試不准引用 vendor_kit 程式）"')
rep('(2, "repo_fs.py", True, "專案檔案存取：唯一能寫專案目錄的模組；原子替換在這"),', '(2, "repo_fs.py", True, "專案檔案存取：唯一能寫專案目錄的模組；整批替換（原子替換）在這"),')
rep('(2, "template.py  stamp.py  diff.py  report.py", True, "純函式：模板、印記（指紋）、差異比對、回報"),',
    '(2, "template.py  stamp.py  diff.py  report.py", True, "純函式（只算結果、不碰檔案）：模板、印記（指紋）、差異比對、回報"),')
rep('(1, "Dockerfile  setup.toml  script/hooks/…", True, "進 git｜使用者檔案：init 從模板建立，之後歸使用者維護"),',
    '''(1, "Dockerfile  setup.toml  …", True, "進 git｜使用者檔案：init 從模板建立，之後歸使用者維護"),
 (1, "script/hooks/", False, "進 git｜使用者的掛勾腳本：每個工具指令前後自動執行（init 建立的空殼）"),''')
rep('p10 += legend("p10", 40, 70 + 50 + len(VK) * RH + 20 + 40, ["red", "green", "white", "file"], "實線框 = 資料夾；虛線框 = 檔案\\n右欄 = 用途／放什麼類型的東西")',
    'p10 += legend("p10", 40, 70 + 50 + len(VK) * RH + 20 + 40, ["red", "green", "folder", "filebox"], "右欄 = 用途／放什麼類型的東西")')
rep(''' ("image", "打包好可執行的檔案包；vendor_kit repo 只有 src/ 會被放進去"),''',
''' ("repo", "一個 git 管理的專案資料夾；這頁的三種：我們開發的、工具的、使用工具的專案"),
 ("進 git／不進 git", "進 git = 這個檔會被版本管理、跟著 repo 走；不進 git = 只在本機產生，隨時可刪掉重裝"),
 ("image", "打包好可執行的檔案包；vendor_kit repo 只有 src/ 會進最終出貨的 image，測試只進測試用的 stage"),
 ("tag / GHCR", "tag = 給 repo 打的版本記號（v1.2.0），CI 看到就出貨／GHCR = GitHub 的 image 倉庫"),
 ("hooks", "掛勾腳本：每個工具指令前（pre）後（post）自動執行的使用者腳本，init 建立空殼"),
 ("原子替換 / 純函式 / 引用", "整批一次換掉，不會出現半新半舊／只算結果、不碰檔案與網路的程式／一個程式 import（引用）另一個程式"),''')
# ---- 第 8 頁 ----
rep(''' ("VERSION vs .version", "VERSION = fixtures 裡假 dist 的版本字串（image 內 /dist/VERSION，install 寫進印記）；.version = 專案 repo 記工具版本的檔"),''',
''' ("VERSION vs .version", "VERSION = image 內 /dist/VERSION：出貨時寫入的 image 識別字串，install 抄到印記第一行，就是拿來跟 .version 比的值（fixtures 裡是假的）；.version = 專案 repo 記工具版本的檔"),
 ("TOML / tomllib", "TOML = 設定檔格式（.version、init.toml 都用它）；tomllib = Python 3.11 起內建的讀 TOML 程式庫，環境檢查要確認它在"),''')
# ---- 第 9 頁 ----
rep('"起 vendor_kit 容器跑子命令\\n（init / diff / upgrade）", 660', '"起 vendor_kit 容器跑子命令\\n（init / diff；upgrade = 改 .version 再 install + diff）", 660')
rep('p9 += legend("p9", 40, 1040, ["red", "green", "neutral", "white", "pimg"], "表格：一列一個指令\\n流程：實線 = 執行順序")',
    'p9 += legend("p9", 40, 1040, ["red", "green", "neutral", "white", "pimg", "startend", "rhomb", "notebox"], "表格：一列一個指令\\n流程：實線 = 執行順序")')
rep(''' ("docker compose", "Docker 內建的多容器管理指令：build 建置、up 啟動、exec 進入、down 停止"),''',
''' ("docker compose", "Docker 內建的多容器管理指令：build 建置、up 啟動、exec 進入、down 停止"),
 ("image / 容器 / Dockerfile", "image = 打包好的環境（做一次）；容器 = image 開起來的實例（可開可關）；Dockerfile = 怎麼做 image 的食譜。build 做 image，run 開容器"),''')
open("gen29.py", "w").write(src); print("ok")
