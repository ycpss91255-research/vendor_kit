# ================= 討論 D2a：#11 圖解（先看這頁） =================
CODE = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;fontSize=12;fontFamily=Courier New;align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;dashed=1;"
d2a = [v("title", "1", TITLE, "#11 圖解：just diff 為什麼要「三方」── 用一個 Dockerfile 的例子", 40, 20, 1200, 30)]
# 三份檔
d2a.append(v("x_t", "1", TEXT(14) + "fontStyle=1;align=left;", "三份東西", 40, 70, 300, 24))
d2a.append(v("x1", "1", CODE, "<b>範本 v1</b>（你當初 init 拿到的）\nFROM ubuntu:22.04\nRUN apt install curl", 40, 100, 300, 80))
d2a.append(v("x2", "1", CODE, "<b>你的 Dockerfile</b>（你改過：加了 git）\nFROM ubuntu:22.04\nRUN apt install curl git", 380, 100, 300, 80))
d2a.append(v("x3", "1", CODE, "<b>範本 v2</b>（工具升級後，在 image 裡：改成 24.04）\nFROM ubuntu:24.04\nRUN apt install curl", 720, 100, 340, 80))
# 二方
d2a.append(v("g_two", "1", SW(NEUTRAL), "現在的做法：二方 ── 只拿「範本 v2」跟「你的檔」比", 40, 220, 700, 200))
d2a.append(v("t1", "g_two", CODE, "diff 你的檔 → 範本 v2\n- FROM ubuntu:22.04\n+ FROM ubuntu:24.04\n- RUN apt install curl git\n+ RUN apt install curl", 20, 50, 320, 110))
d2a.append(v("t2", "g_two", NOTE, "兩種改動混在一起：\n22.04→24.04 是工具改的（你該跟進）\ngit 被拿掉 是因為你自己加的（不該動）\n看 diff 的人分不出來", 360, 50, 320, 110))
# 三方
d2a.append(v("g_three", "1", SW(NEUTRAL), "三方 ── 多留一份「範本 v1」當基準，就能拆開", 780, 220, 760, 200))
d2a.append(v("u1", "g_three", CODE, "範本 v1 → 範本 v2 = 工具改了什麼\n- FROM ubuntu:22.04\n+ FROM ubuntu:24.04", 20, 50, 350, 70))
d2a.append(v("u2", "g_three", CODE, "範本 v1 → 你的檔 = 你改了什麼\n- RUN apt install curl\n+ RUN apt install curl git", 390, 50, 350, 70))
d2a.append(v("u3", "g_three", NOTE, "兩邊改的不是同一行 → 沒有衝突：你只要把 FROM 改成 24.04 就跟進完成。\n若兩邊改到同一行 → 標「兩邊都改」，由你決定。", 20, 130, 720, 50))
# 基準的一生
d2a.append(v("g_life", "1", SW(NEUTRAL), "「範本 v1」（基準）放哪、怎麼更新", 40, 450, 1500, 230))
d2a.append(v("l0", "g_life", ELLIPSE(GREEN), "just init", 30, 60, 140, 50))
d2a.append(v("l1", "g_life", FILE, "初始檔（Dockerfile…）\n歸你，之後隨你改", 210, 60, 220, 50))
d2a.append(v("l2", "g_life", FILE, ".vendor_kit/base/<name>/\n= 範本 v1 的副本（進 git，人不改）", 470, 60, 260, 50))
d2a.append(v("l3", "g_life", ELLIPSE(GREEN), "升級後 just diff", 30, 150, 140, 50))
d2a.append(v("l4", "g_life", LEAF(), "三方比對：base vs image 裡的新範本 vs 你的檔\n只印出來，不改任何檔", 210, 150, 340, 50))
d2a.append(v("l5", "g_life", ELLIPSE(GREEN), "你看完、跟進完\njust accept <name>", 800, 150, 200, 50))
d2a.append(v("l6", "g_life", FILE, ".vendor_kit/base/<name>/\n換成範本 v2（下次升級的基準）", 1060, 150, 300, 50))
d2a.append(v("l7", "g_life", NOTE, "為什麼不放 .<name>/：升級時整批換掉、換台電腦 clone 也沒有 → 需要它的時候剛好不在。", 790, 60, 570, 50))
d2a.append(e("le0", "l0", "l1", "建立", (1, 0.5), (0, 0.5)))
d2a.append(e("le1", "l1", "l2", "同時存一份副本", (1, 0.5), (0, 0.5)))
d2a.append(e("le2", "l3", "l4", "", (1, 0.5), (0, 0.5)))
d2a.append(e("le3", "l4", "l5", "", (1, 0.5), (0, 0.5)))
d2a.append(e("le4", "l5", "l6", "寫入", (1, 0.5), (0, 0.5)))
d2a += legend_flow("d2a", 40, 710, files=True, note=True)
d2a += terms("d2a", 40, 820, [
 ("範本 / 初始檔", "範本 = 工具 dist 裡給你的樣板；初始檔 = init 從範本複製到專案、之後歸你的檔"),
 ("基準（base）", "你上一次確認過的那版範本副本；三方比對的第三份"),
 ("diff 的 - / +", "- 是這邊有、那邊沒有的行；+ 相反"),
 ("just accept", "告訴工具「這版我看完了」，把基準換成新版範本"),
])
pages.insert(1, ("d2a", "討論 #11 圖解", d2a))
