src = open("gen30.py").read()
def rep(a, b):
    global src; assert src.count(a) == 1, a[:70]; src = src.replace(a, b)
# ===== 第 2 頁：啟動器一詞統一 =====
rep('p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器（進 git）", 20, 80, 300, 175))', 'p1b.append(v("pa", "proj", SW(NEUTRAL), "啟動器與版本檔（進 git）", 20, 80, 300, 175))')
rep('"必要條件：.version、justfile、.vendor_kit/（啟動器，由 vendor_kit 寫出）；.version 可列多個工具，各自安裝到自己的 .<name>/"',
    '"必要條件：.version、justfile、.vendor_kit/（啟動器本體，第 10 頁 bootstrap 寫出；justfile 只是 import 它）；.version 可列多個工具，各自安裝到自己的 .<name>/"')
rep('("專案 repo", "使用工具的專案；必須有 .version、justfile；可同時用多個工具"),', '("專案 repo", "使用工具的專案；必須有 .version、justfile、.vendor_kit/；可同時用多個工具"),')
rep('("just / justfile", "just 是主機上的指令跑器；justfile 是專案裡給它讀的指令清單，也就是啟動器"),',
    '("just / justfile / .vendor_kit/", "just = 主機上的指令跑器；.vendor_kit/ = 啟動器本體（vendor_kit 寫出的標準指令，人不改）；justfile = 專案自己的指令清單，第一行 import .vendor_kit/ 把標準指令接進來"),')
# ===== 第 7 頁 =====
rep('(2, "cli.py", True, "命令介面：讀參數、分派 install / init / verify / diff"),', '(2, "cli.py", True, "命令介面：讀參數、分派 install / init / verify / diff（第一次另有 bootstrap，第 10 頁）"),')
rep('(1, ".vendor_kit/", False, "進 git｜啟動器：vendor_kit 寫出的標準 just 指令，人不改，升級整個換新（第 10 頁）"),',
    '(1, ".vendor_kit/", False, "進 git｜啟動器本體：vendor_kit 寫出的標準 just 指令＋它自己的印記，人不改，升級整個換新（第 10 頁）"),')
# ===== 第 9 頁 =====
rep('"使用者介面：just 指令表（使用者只會碰這些；每個指令前都先自動檢查／安裝）"', '"使用者介面：指令表（bootstrap.sh 只在第一次；之後全是 just 指令，每個 just 指令前都先自動檢查／安裝）"')
rep('("子命令 / dist/", "子命令 = vendor_kit 容器裡的四個動作：install 把 dist 裝進 .<name>/ 並寫印記、init 建初始檔、verify 檢查 .<name>/ 有沒有被手改、diff 比模板；dist/ = 工具要出貨的檔案"),',
    '''("子命令 / dist/", "子命令 = vendor_kit 容器裡的動作：install 把 dist 裝進 .<name>/ 並寫印記、init 建初始檔、verify 檢查 .<name>/ 有沒有被手改、diff 比模板；bootstrap 只在第一次寫出啟動器（第 10 頁）；dist/ = 工具要出貨的檔案"),
 ("bootstrap / release", "bootstrap = 第一次把 vendor_kit 接進專案的腳本，不是 just 指令、也不會先自動檢查（那時啟動器還不存在）；release = vendor_kit 打 tag 發佈的版本，image 上傳 GHCR、bootstrap.sh 附在 GitHub release 頁"),''')
# ===== 第 10 頁 =====
rep('p11.append(v("s_err", "bs", ELLIPSE(RED), "中止：列出缺的軟體", 320, 160, 180, 50))', 'p11.append(v("s_err", "bs", ELLIPSE(RED), "中止：列出缺的軟體", 400, 160, 200, 50))')
rep('p11.append(e("be2", "s1", "s_err", "缺", (0.5, 1), (0.5, 0), vert="left", pos=-0.4))', 'p11.append(e("be2", "s1", "s_err", "缺", (0.5, 1), (0.5, 0), vert="left"))')
rep('''p11.append(e("be13", "s5", "u1", "", (0, 0.5), (1, 0.5)))''',
    '''p11.append('<mxCell id="be13" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="bs" source="s5" target="u1"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="500" y="620"/><mxPoint x="150" y="620"/></Array></mxGeometry></mxCell>')''')
rep('啟動器：install / init / diff / upgrade 等標準\\n指令 ＋ 印記（vendor_kit 擁有，人不改，進 git）"', '啟動器本體：install / init / diff / upgrade 等標準指令\\n＋ 它自己的印記 .vendor_kit/.stamp（記 vendor_kit 版本）；進 git，人不改"')
rep('''("啟動器 / .vendor_kit/", "just 要用的標準指令集，由 vendor_kit 寫出並擁有；使用者不改，升級整個換新"),''',
    '''("啟動器 / .vendor_kit/", "just 要用的標準指令集，由 vendor_kit 寫出並擁有；使用者不改，升級整個換新"),
 ("印記（.vendor_kit/.stamp）", "跟 .<name>/.stamp 同一種東西，但這份記的是 vendor_kit 自己的版本 + vendor.just 指紋；啟動器拿它跟 .version 的 vendor_kit 那行比"),
 ("docker / git / just", "主機要先裝的三個軟體：跑容器的／管理 repo 的／跑 justfile 指令的；bootstrap 只檢查有沒有，不幫你裝"),
 ("容器 / image / 掛載", "image = 打包好的環境；容器 = image 開起來的實例；掛載 = 把專案目錄接進容器，容器寫的檔就直接出現在專案裡"),
 ("GHCR / Renovate / tag / TOML", "GitHub 的 image 倉庫／自動開 PR 改 .version 的機器人／給 repo 打的版本記號／設定檔格式"),''')
rep('("just init / install", "第 3 頁「第一次」流程：安裝 .<name>/ 並建立初始檔"),', '("just init / install", "just init = 第 3 頁「第一次」流程：先 install（把工具的 dist 裝進 .<name>/），再 init（建立初始檔）"),')
open("gen31.py", "w").write(src); print("ok")
