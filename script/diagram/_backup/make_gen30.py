src = open("gen29.py").read()
def rep(a, b):
    global src; assert src.count(a) == 1, a[:70]; src = src.replace(a, b)
# ===== 第 2 頁：專案 repo 必要條件加 .vendor_kit/ =====
rep('"必要條件只有 .version 與 justfile；.version 可列多個工具，各自安裝到自己的 .<name>/"',
    '"必要條件：.version、justfile、.vendor_kit/（啟動器，由 vendor_kit 寫出）；.version 可列多個工具，各自安裝到自己的 .<name>/"')
rep('p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器（進 git）", 20, 80, 300, 125))',
    'p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器（進 git）", 20, 80, 300, 175))\np1b.append(v("p_vk", "pa", LEAF(), ".vendor_kit/\\n（標準指令，justfile import 它）", 12, 122, 180, 44).replace("fontSize=14", "fontSize=12"))')
# ===== 第 7 頁 =====
rep('(1, "justfile", True, "進 git｜啟動器：使用者打 just 時執行的指令清單（第 9 頁）"),',
    '(1, "justfile", True, "進 git｜使用者的指令清單：第一行 import .vendor_kit/，其餘自己加（第 9 頁）"),\n (1, ".vendor_kit/", False, "進 git｜啟動器：vendor_kit 寫出的標準 just 指令，人不改，升級整個換新（第 10 頁）"),')
rep('(1, "dist/", False, "要出貨的全部：腳本（script/…）、Dockerfile 範本、模板、hooks 空殼；整包寫進專案的 .<name>/"),',
    '(1, "dist/", False, "要出貨的全部：腳本、Dockerfile 範本、模板、hooks 空殼；整包寫進專案 .<name>/"),')
rep('(1, "test/", False, "所有測試與檢查（只進測試用的 stage，不進出貨 image）；先分測試工具、再分層級"),',
    '(1, "test/", False, "所有測試與檢查；smoke／lint／unit／integration 只進測試用的 stage，system／acceptance 在 CI 主機跑；都不進出貨 image"),')
rep(''' ("image", "打包好可執行的檔案包；vendor_kit repo 只有 src/ 會進最終出貨的 image，測試只進測試用的 stage"),''',
    ''' ("image", "打包好可執行的檔案包；vendor_kit repo 只有 src/ 會進最終出貨的 image，測試只進測試用的 stage 或在 CI 主機跑"),
 ("TOML / tomllib / VERSION / pytest", "設定檔格式（.version、init.toml）／Python 讀 TOML 的內建程式庫／image 內的識別字串，install 抄到印記第一行（跟專案的 .version 不同檔）／Python 測試框架"),''')
# ===== 第 8 頁 =====
rep(''' ("fixture / 假專案", "測試用的假資料：假的 dist/、init.toml，以及一個只有 .version 與 justfile 的假專案"),''',
    ''' ("fixture / 假專案", "測試用的假資料：假的 dist/（工具要出貨的檔案）、init.toml（init 要複製哪些初始檔的清單），以及一個只有 .version 與 justfile 的假專案"),
 ("image / 容器 / Docker / Dockerfile", "打包好的環境／image 開起來的實例／跑它們的軟體／怎麼做 image 的食譜（每個 stage 是食譜的一段）"),''')
# ===== 第 9 頁 =====
rep('p9.append(v("gA", "1", SW(RED), "vendor_kit 提供的指令（每個用這套框架的專案都一樣）", 40, 70, TBW + 40, 320))',
    'p9.append(v("gA", "1", SW(RED), "vendor_kit 提供的指令（每個用這套框架的專案都一樣）", 40, 70, TBW + 40, 368))')
rep(''' ("just init", "第一次把工具接進專案", "安裝 .<name>/，再照 init.toml 建立初始檔''',
    ''' ("bootstrap.sh\\n（release 附）", "第一次把 vendor_kit 接進專案", "展開 .vendor_kit/、justfile、.version；問要不要接工具並跑 init；然後刪掉自己（第 10 頁）", "docker run … vendor_kit bootstrap", ".vendor_kit/、justfile、.version（新建）"),
 ("just init", "第一次把工具接進專案", "安裝 .<name>/，再照 init.toml 建立初始檔''')
rep('"verify 不開放給使用者單獨打：它是每個指令前的守門，不是一個要記的指令。"', '"verify 不開放給使用者單獨打：它是每個指令前的守門（檢查 .<name>/ 有沒有被手改，被改就中止），不是一個要記的指令。"')
rep('p9.append(v("gB", "1", SW(GREEN), "工具 <name> 提供的指令（由工具的 dist/ 決定，每個工具可以不同；下面以「容器工作流」工具為例）", 40, 420,',
    'p9.append(v("gB", "1", SW(GREEN), "工具 <name> 提供的指令（由工具的 dist/ 決定，每個工具可以不同；下面以「容器工作流」工具為例）", 40, 470,')
rep('"任何一個 just 指令的完整路徑", 40, 810, TBW + 40, 205))', '"任何一個 just 指令的完整路徑", 40, 860, TBW + 40, 205))')
rep('p9.append(e("ce2", "c2", "c3", "vendor_kit 的", (0.5, 0), (0, 0.5)))', 'p9.append(e("ce2", "c2", "c3", "vendor_kit 的", (0.5, 0), (0, 0.5)).replace(\'endFill=1;\', \'endFill=1;jettySize=0;\', 1))')
rep('p9.append(e("ce3", "c2", "c4", "工具的", (0.5, 1), (0, 0.5)))', 'p9.append(e("ce3", "c2", "c4", "工具的", (0.5, 1), (0, 0.5)).replace(\'endFill=1;\', \'endFill=1;jettySize=0;\', 1))')
rep('p9 += legend("p9", 40, 1040,', 'p9 += legend("p9", 40, 1090,')
rep('p9 += terms("p9", 40, 1150, [', 'p9 += terms("p9", 40, 1200, [\n ("子命令 / dist/", "子命令 = vendor_kit 容器裡的四個動作：install 把 dist 裝進 .<name>/ 並寫印記、init 建初始檔、verify 檢查 .<name>/ 有沒有被手改、diff 比模板；dist/ = 工具要出貨的檔案"),')
rep('("容器工作流", "用容器當開發環境的工作方式：建置 image → 啟動容器 → 進去工作 → 停掉；本頁 B 區的四個指令就是它"),',
    '("容器工作流", "用容器當開發環境的工作方式：建置 image → 啟動容器 → 進去工作 → 停掉；「工具 <name> 提供的指令」表的四個指令就是它"),')
rep('("just / justfile", "just = 主機上的指令跑器；justfile = 專案裡給它讀的指令清單（啟動器）。使用者只需要記這一頁的指令"),',
    '("just / justfile", "just = 主機上的指令跑器；justfile = 專案裡給它讀的指令清單，第一行 import .vendor_kit/ 的標準指令（啟動器）。使用者只需要記這一頁的指令"),')
# ===== 第 10 頁 =====
i = src.index("doc = ('<mxfile host=")
src = src[:i] + open("page_bootstrap.py").read() + "\n" + src[i:]
rep('''       + page("p9", "9. 使用者介面：just 指令表", p9)
       + "</mxfile>")''', '''       + page("p9", "9. 使用者介面：just 指令表", p9)
       + page("p11", "10. 流程：bootstrap", p11)
       + "</mxfile>")''')
open("gen30.py", "w").write(src); print("ok")

# ---- 第 10 頁排版、第 9 頁 c3 文字 ----
src = open("gen30.py").read()
rep('"起 vendor_kit 容器跑子命令\\n（init / diff；upgrade = 改 .version 再 install + diff）", 660', '"起 vendor_kit 容器跑子命令\\n（init / diff；upgrade 是它們的組合）", 660')
rep('''exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="bs" source="s1" target="s2"><mxGeometry x="-0.6" relative="1" as="geometry"><Array as="points"><mxPoint x="690" y="90"/><mxPoint x="690" y="285"/></Array>''',
    '''exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="bs" source="s1" target="s2"><mxGeometry x="-0.5" relative="1" as="geometry"><Array as="points"><mxPoint x="690" y="90"/><mxPoint x="690" y="230"/><mxPoint x="500" y="230"/></Array>''')
rep('指令 ＋ 印記（vendor_kit 擁有，人不改，進 git）", 1160, 215, 340, 60))', '指令 ＋ 印記（vendor_kit 擁有，人不改，進 git）", 1160, 215, 340, 64))')
rep('之後是使用者自己的指令，進 git）", 1160, 275, 340, 50))', '之後是使用者自己的指令，進 git）", 1160, 283, 340, 44))')
rep('".version（先只有 vendor_kit = \\"…\\" 一行，進 git）", 1160, 325, 340, 40))', '".version（先只有 vendor_kit = \\"…\\" 一行，進 git）", 1160, 331, 340, 36))')
rep('p11.append(e("be5", "c1", "f1", "寫出", (1, 0.2143), (0, 0.5)))', 'p11.append(e("be5", "c1", "f1", "寫出", (1, 0.2286), (0, 0.5)))')
rep('p11.append(e("be6", "c1", "f2", "寫出", (1, 0.6071), (0, 0.5)))', 'p11.append(e("be6", "c1", "f2", "寫出", (1, 0.6429), (0, 0.5)))')
rep('p11.append(e("be7", "c1", "f3", "寫出", (1, 0.9286), (0, 0.5)))', 'p11.append(e("be7", "c1", "f3", "寫出", (1, 0.9571), (0, 0.5)))')
open("gen30.py", "w").write(src); print("ok2")
