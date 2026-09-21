# ================= 討論 D0：使用方式（乙版）— 三個時刻，三條線；<repo> = 工具 repo 名 =================
d0 = [v("title", "1", TITLE, "使用方式（乙版）：三個時刻各一條線（<repo> = 工具 repo 名，例：base）", 40, 20, 1100, 30)]
def lane(bid, title, y, h=150):
    d0.append(v(bid, "1", SW(NEUTRAL), title, 40, y, 1500, h))
def chain(bid, items, y=55, x0=30, gap=30):
    x = x0; prev = None
    for cid, st, text, w in items:
        d0.append(v(cid, bid, st, text, x, y, w, 50))
        if prev: d0.append(e(f"{cid}_e", prev, cid, "", (1, 0.5), (0, 0.5)))
        prev = cid; x += w + gap
CODE = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;strokeWidth=1;fontSize=12;fontFamily=Courier New;align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;"
# ① 第一次
lane("L1", "① 第一次接上（使用者，只做一次）", 70, 300)
chain("L1", [
 ("a0", ELLIPSE(GREEN), "跑 bootstrap.sh", 150),
 ("a1", FILE, "生成\n• .version\n• justfile\n• .vendor_kit/", 150),
 ("a2", LEAF(), "bootstrap.sh 結尾印：\n「下一步：在 .version 加工具，\n然後 just vendor_kit init」", 230),
 ("a3", LEAF(), "在 .version 加一行：\n要用的工具 + 版本", 170),
 ("a4", ELLIPSE(GREEN), "just vendor_kit init", 170),
 ("a5", PURPLE_LEAF, "引擎：裝工具檔 .<repo>/\n複製初始檔", 180),
 ("a6", ELLIPSE(GREEN), "完成", 100),
])
d0.append(v("a_ex", "L1", CODE, "範例：從空 repo 到接上 base\n$ mkdir my_robot && cd my_robot && git init\n$ curl -LO https://github.com/…/vendor_kit/releases/latest/download/bootstrap.sh && sh bootstrap.sh\n  → 生成 .version / justfile / .vendor_kit/；印「下一步：在 .version 加工具，然後 just vendor_kit init」\n$ echo 'base = \"ghcr.io/…/base-dist:v1.0.0@sha256:…\"' >> .version\n$ just vendor_kit init\n  → 生成 .base/（工具檔，不進 git）與 Dockerfile、setup.toml、script/hooks/…（初始檔，你的）\n$ git add -A && git commit -m \"接上 base\"", 30, 120, 1440, 165))
# ② 日常
lane("L2", "② 日常（使用者，每天）", 400)
chain("L2", [
 ("b0", ELLIPSE(GREEN), "打工具的指令\n例：just docker build\n（指令與 Dockerfile 都是\n工具 base 提供的，不是 vendor_kit）", 230),
 ("b1", LEAF(), "自動：讀 .version", 130),
 ("b2", LEAF(), "自動：抓工具檔案\n（docker cp）", 150),
 ("b3", PURPLE_LEAF, "引擎：版本不同→重裝\n相同→檢查沒被改", 200),
 ("b4", LEAF(), "跑工具檔 .<repo>/\n裡的 build 腳本", 150),
 ("b5", ELLIPSE(GREEN), "完成", 100),
])
d0.append(v("b_err", "L2", ELLIPSE(RED), "被手改→中止", 1330, 55, 150, 50))
d0.append(e("b_err_e", "b3", "b_err", "", (0.5, 0), (0, 0.5)))
# ③ 升級
lane("L3", "③ 升級（Renovate 機器人 + 使用者）", 580, 200)
chain("L3", [
 ("c0", ELLIPSE(GREEN), "Renovate 開 PR\n改 .version 一行", 160),
 ("c1", LEAF(), "CI 腳本 1\n裝（install）", 120),
 ("c2", LEAF(), "CI 腳本 2\n驗（verify）", 120),
 ("c3", LEAF(), "CI 腳本 3\n工具的 build", 120),
 ("c4", RHOMBUS, "都過？", 120),
 ("c5", LEAF(), "merge → 下次 just\n自動裝新版（同②）", 170),
 ("c6", ELLIPSE(GREEN), "just vendor_kit diff <repo>\n比「工具的新版範本」vs\n「你的檔」（不是比 vendor_kit）", 230),
 ("c7", LEAF(), "看差異\n改自己的檔", 120),
 ("c8", ELLIPSE(GREEN), "just vendor_kit accept <repo>\n記住：這版範本我看過了", 200),
])
d0.append(v("c_err", "L3", ELLIPSE(RED), "不合併：PR 留著，\n使用者自己判斷原因", 480, 120, 200, 50))
d0.append(e("c_err_e", "c4", "c_err", "否", (0.5, 1), (0.5, 0), vert=True))
d0.append(v("z_n", "1", NOTE, "指令分層對齊 base：根 justfile 只 import；just vendor_kit … 是引擎的（init/diff/accept/upgrade）；just docker … 是工具自己帶的，vendor_kit 不定義它。\n乙版 = 工具 image 只放檔案；引擎只有 vendor_kit:vN 一份。②的「抓工具檔案」就是乙版多的一步。", 40, 800, 1500, 44))
d0 += legend_flow("d0", 40, 864, files=True, note=True)
pages.insert(0, ("d0", "使用方式（乙版）", d0))
