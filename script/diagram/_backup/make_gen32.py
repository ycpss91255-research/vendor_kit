src = open("gen31.py").read()
def rep(a, b):
    global src; assert src.count(a) == 1, a[:70]; src = src.replace(a, b)
# 第 2 頁
rep('"必要條件：.version、justfile、.vendor_kit/（啟動器本體，第 10 頁 bootstrap 寫出；justfile 只是 import 它）；.version 可列多個工具，各自安裝到自己的 .<name>/"',
    '"必要條件：.version、justfile、.vendor_kit/（啟動器本體，第 10 頁 bootstrap 寫出；justfile 只 import 它）；每個工具各自裝到 .<name>/"')
rep('p1b.append(e("f8", "p_just", "p_eng", "工具名、版本、使用者身分、專案路徑", (0.5, 1), (0.8, 0), vert=True))',
    'p1b.append(e("f8", "p_just", "p_eng", "工具名、版本、使用者身分、專案路徑", (0.5, 1), (0.8, 0), vert="left"))')
# 第 7 頁
rep('(1, "dist/", False, "要出貨的全部：腳本、Dockerfile 範本、模板、hooks 空殼；整包寫進專案 .<name>/"),',
    '(1, "dist/", False, "要出貨的全部（腳本、Dockerfile 範本、模板、hooks 空殼），整包裝進專案的工具目錄"),')
# 第 8 頁
rep('("install / verify / just", "install = 把 dist 裝進 .<name>/ 並寫印記；verify = 檢查 .<name>/ 沒被手改；just = 使用者在主機打的指令跑器（第 3、9 頁）"),',
    '("install / init / verify / diff / just", "四個子命令：把 dist 裝進 .<name>/ 並寫印記／建立初始檔／檢查 .<name>/ 沒被手改／比對新版模板；just = 使用者在主機打的指令跑器（第 3、9 頁）"),')
# 第 9 頁
rep('"起 vendor_kit 容器跑子命令\\n（init / diff；upgrade 是它們的組合）", 660', '"起 vendor_kit 容器跑子命令\\n（init / diff；upgrade = 改 .version → install → diff）", 660')
i = src.index('p9.append(v("c3", "gC"'); j = src.index('\n', i)
src = src[:i] + src[i:j].replace(', 660, 55, 260, 50))', ', 660, 55, 300, 50))') + src[j:]
rep('（build / run / exec / stop…）", 660, 135, 260, 50))', '（build / run / exec / stop…）", 660, 135, 300, 50))')
rep('p9.append(v("c5", "gC", ELLIPSE(GREEN), "畫面顯示結果", 980, 70, 160, 100))', 'p9.append(v("c5", "gC", ELLIPSE(GREEN), "畫面顯示結果", 1000, 70, 160, 100))')
rep('p9.append(e("ce4", "c3", "c5", "", (1, 0.5), (0, 0.1)))', 'p9.append(e("ce4", "c3", "c5", "", (1, 0.5), (0, 0.1)).replace(\'endFill=1;\', \'endFill=1;entryPerimeter=0;\', 1))')
rep('p9.append(e("ce5", "c4", "c5", "", (1, 0.5), (0, 0.9)))', 'p9.append(e("ce5", "c4", "c5", "", (1, 0.5), (0, 0.9)).replace(\'endFill=1;\', \'endFill=1;entryPerimeter=0;\', 1))')
rep(''' ("Renovate / GHCR", "GitHub 上的機器人：有新版就自動開 PR 改 .version／GitHub 的 image 倉庫"),''',
    ''' ("Renovate / GHCR", "GitHub 上的機器人：有新版就自動開 PR 改 .version／GitHub 的 image 倉庫"),
 ("PR / tag / docker run", "GitHub 上的合併請求，人 merge 才生效／給 repo 打的版本記號，CI 看到就發佈／把 image 跑成容器的指令"),''')
# 第 10 頁
rep('"justfile（一行 import .vendor_kit/…；\\n之後是使用者自己的指令，進 git）", 1160, 283, 340, 44))', '"justfile（一行 import .vendor_kit/…；之後是\\n使用者自己的指令，進 git；已存在就不動）", 1160, 283, 340, 44))')
rep('".version（先只有 vendor_kit = \\"…\\" 一行，進 git）", 1160, 331, 340, 36))', '".version（先只有 vendor_kit = \\"…\\" 一行，進 git；已存在就不動）", 1160, 331, 340, 36).replace("fontSize=14", "fontSize=12"))')
rep('p11.append(e("be6", "c1", "f2", "寫出", (1, 0.6429), (0, 0.5)))', 'p11.append(e("be6", "c1", "f2", "沒有才寫", (1, 0.6429), (0, 0.5)))')
rep('p11.append(e("be7", "c1", "f3", "寫出", (1, 0.9571), (0, 0.5)))', 'p11.append(e("be7", "c1", "f3", "沒有才寫", (1, 0.9571), (0, 0.5)))')
rep('啟動器本體：標準 just 指令（install / init / diff / upgrade）\\n＋ 自己的印記', '啟動器本體：標準 just 指令（init / diff / upgrade 與每個指令前的自動檢查）\\n＋ 自己的印記')
rep('("印記（.vendor_kit/.stamp）", "跟 .<name>/.stamp 同一種東西，但這份記的是 vendor_kit 自己的版本 + vendor.just 指紋；啟動器拿它跟 .version 的 vendor_kit 那行比"),',
    '("印記（.vendor_kit/.stamp）", "跟 .<name>/.stamp 同一種東西，但這份記的是 vendor_kit 自己的版本 + 標準指令檔（.vendor_kit/vendor.just）的指紋；啟動器拿它跟 .version 的 vendor_kit 那行比"),')
open("gen32.py", "w").write(src); print("ok")

# ---- 第 2 頁重排：安裝容器下移，f8 標籤落在啟動器框外 ----
src = open("gen32.py").read()
rep('"工具 repo（每個要出貨的工具一個）", 40, 210, 320, 260))', '"工具 repo（每個要出貨的工具一個）", 40, 240, 320, 260))')
rep('p1b.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 490, 320, 130))', 'p1b.append(v("vk", "1", SW(RED), "vendor_kit repo", 40, 520, 320, 130))')
rep('"另一個工具 repo（<name2>，同型）", 40, 640, 320, 60))', '"另一個工具 repo（<name2>，同型）", 40, 670, 320, 60))')
rep('p1b.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 420, 80, 260, 640))', 'p1b.append(v("ghcr", "1", SW(YELLOW), "GHCR（image 倉庫）", 420, 80, 260, 660))')
rep('p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 280, 200, 40))', 'p1b.append(v("g_tool", "ghcr", PURPLE_LEAF, "<name>-dist:vX", 30, 310, 200, 40))')
rep('p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 460, 200, 40))', 'p1b.append(v("g_vk", "ghcr", PURPLE_LEAF, "vendor_kit:vN", 30, 490, 200, 40))')
rep('p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 570, 200, 40))', 'p1b.append(v("g_tool2", "ghcr", PURPLE_LEAF, "<name2>-dist:vY", 30, 600, 200, 40))')
rep('"專案 repo（使用工具的專案）", 740, 80, 770, 640))', '"專案 repo（使用工具的專案）", 740, 80, 770, 660))')
rep('"安裝容器（<name>-dist:vX）", 20, 270, 300, 60))', '"安裝容器（<name>-dist:vX）", 20, 300, 300, 60))')
rep('"以使用者身分執行，跑完即刪", 20, 332, 200, 20))', '"以使用者身分執行，跑完即刪", 20, 362, 200, 20))')
rep('"使用者檔案（進 git）", 300, 380, 220, 125))', '"使用者檔案（進 git）", 300, 400, 220, 125))')
rep('".<name>/（不進 git）", 540, 380, 220, 125))', '".<name>/（不進 git）", 540, 400, 220, 125))')
rep('".<name2>/（另一個工具）", 540, 565, 220, 50))', '".<name2>/（另一個工具）", 540, 595, 220, 50))')
rep('p1b.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1600, 80, 160, 640))', 'p1b.append(v("host", "1", SW(YELLOW), "使用者的電腦", 1600, 80, 160, 660))')
rep('"Docker\\n（跑所有容器）", 20, 418, 120, 50))', '"Docker\\n（跑所有容器）", 20, 437.5, 120, 50))')
rep('p1b.append(e("f8", "p_just", "p_eng", "工具名、版本、使用者身分、專案路徑", (0.5, 1), (0.8, 0), vert="left"))',
    'p1b.append(e("f8", "p_just", "p_eng", "工具名、版本、使用者身分、專案路徑", (0.5, 1), (0.8, 0), vert=True, pos=0.6))')
rep('p1b += legend("p1b", 40, 730,', 'p1b += legend("p1b", 40, 770,')
rep('p1b += terms("p1b", 40, 840, [', 'p1b += terms("p1b", 40, 880, [')
open("gen32.py", "w").write(src); print("ok2")
