# ================= 討論 D0b：just 與 vendor_kit 怎麼接（五層 + 兩個例子逐步追） =================
def vb(id, parent, style, value, x, y, w, h):
    """同 v()，但 <b>…</b> 保留成真的粗體（esc 會把它變成字面文字）。"""
    return v(id, parent, style, value, x, y, w, h).replace("&amp;lt;b&amp;gt;", "&lt;b&gt;").replace("&amp;lt;/b&amp;gt;", "&lt;/b&gt;")
BOXF = OPT + "dashed=1;"                                                     # 專案裡的檔（虛線）
BOXP = OPT.replace("fillColor=#ffffff", f"fillColor={PURPLE}").replace("strokeColor=#000000", "strokeColor=#9673a6")
BOXG = OPT.replace("fillColor=#ffffff", f"fillColor={GREEN}") + "dashed=1;"  # 工具檔（綠虛線）
F12, W12, P12, G12, R12 = FILE + "fontSize=12;", LEAF() + "fontSize=12;", PURPLE_LEAF + "fontSize=12;", ELLIPSE(GREEN) + "fontSize=12;", ELLIPSE(RED) + "fontSize=12;"
ROWLBL = TEXT(12) + "align=left;fontStyle=1;"
d0b = [v("title", "1", TITLE, "just 與 vendor_kit 怎麼接：你打的指令怎麼一層一層傳到引擎、再回到專案檔案（<repo> = 工具 repo 名，例：base）", 40, 20, 1500, 30)]
# ---- 上半：五層 ----
d0b.append(v("M", "1", SW(NEUTRAL), "五層：一個 just 指令會經過哪些檔（左→右 = 呼叫方向；誰擁有、進不進 git 寫在框內）", 40, 60, 1620, 330))
d0b.append(vb("m1", "M", ELLIPSE(GREEN), "<b>① 使用者</b>\n打 just <指令>\n（主機終端機）", 30, 70, 170, 120))
d0b.append(vb("m2", "M", BOXF, "<b>② 根 justfile</b>\n使用者的；進 git\n只有一行：\nimport '.vendor_kit/entry.just'\n想加自己的指令加在下面", 240, 70, 260, 120))
d0b.append(vb("m3", "M", BOXF, "<b>③ .vendor_kit/（薄殼）</b>\nvendor_kit 的；進 git，人不改\nentry.just：接兩邊（mod + import?）\nvendor.just：只有 ensure\n　＋ 一行 docker run 叫引擎", 540, 70, 280, 120))
d0b.append(vb("m4", "M", BOXF, "<b>④ .vendor_kit/gen/</b>\n引擎每次 ensure 產生；不進 git\nvendor_kit.just：init / diff /\n　accept / upgrade / dev 這些 recipe\ntools.just：把每個工具的\n　.<repo>/just/docker.just 掛進來", 860, 70, 300, 120))
d0b.append(vb("m5", "M", BOXP, "<b>⑤ 引擎容器 vendor_kit:vN</b>\ndocker run，掛 專案:/repo、暫存:/dist\n真正做事：install / verify / init /\n　diff / accept …\n寫回專案：.<repo>/、初始檔、baseline/", 1200, 70, 300, 120))
d0b.append(vb("m6", "M", BOXG, "<b>工具檔 .<repo>/</b>（不進 git，由引擎裝）\n裡面的 just/docker.just 提供\njust docker build / run / exec / stop", 860, 225, 300, 80))
d0b.append(vb("m7", "M", BOXF, "<b>歸你的檔</b>（進 git）：Dockerfile、\nsetup.toml、script/…（init 生成）\n.vendor_kit/baseline/（accept 換新）", 1240, 225, 220, 80))
d0b.append(e("me1", "m1", "m2", "讀", (1, 0.5), (0, 0.5)))
d0b.append(e("me2", "m2", "m3", "import", (1, 0.5), (0, 0.5)))
d0b.append(e("me3", "m3", "m4", "mod ＋ import?", (1, 0.5), (0, 0.5)))
d0b.append(e("me4", "m4", "m5", "一行 docker run", (1, 0.5), (0, 0.5)))
d0b.append(e("me5", "m5", "m4", "ensure 時：引擎重新產生 gen/", (0.5, 0), (0.5, 0), dashed=True))
d0b.append(e("me6", "m5", "m6", "install：裝工具檔", (0, 0.75), (1, 0.5), vert="below"))
d0b.append(e("me7", "m6", "m4", "tools.just 掛進來", (0.5, 0), (0.5, 1), vert=True))
d0b.append(e("me8", "m5", "m7", "init / accept 寫入", (0.5, 1), (0.5, 0), vert=True))
# ---- 下半：兩個例子逐步追 ----
def trace(bid, title, y, h, row1, row2, lbl1, lbl2, x0=140, gap=20):
    d0b.append(v(bid, "1", SW(NEUTRAL), title, 40, y, 1620, h))
    d0b.append(v(f"{bid}_l1", bid, ROWLBL, lbl1, 20, 70, 110, 50))
    d0b.append(v(f"{bid}_l2", bid, ROWLBL, lbl2, 20, 175, 110, 50))
    prev = None
    for ry, items in ((70, row1), (175, row2)):
        x = x0
        for cid, st, text, w in items:
            d0b.append(v(cid, bid, st, text, x, ry, w, 50))
            if prev:
                if ry == 175 and x == x0: d0b.append(e(f"{cid}_e", prev, cid, "", (0.5, 1), (0.5, 0)))   # 換列：右下 → 左上
                else: d0b.append(e(f"{cid}_e", prev, cid, "", (1, 0.5), (0, 0.5)))
            prev = cid; x += w + gap
trace("A", "例 (a)：just docker build ── 工具自己的指令（vendor_kit 不定義它，只保證工具檔在、沒被改）", 410, 310,
 [("a0", G12, "just docker build", 150),
  ("a1", F12, "根 justfile\nimport entry.just", 150),
  ("a2", F12, ".vendor_kit/entry.just\nimport? gen/tools.just", 180),
  ("a3", F12, "gen/tools.just\nmod? docker（指到工具檔）", 190),
  ("a4", F12, ".<repo>/just/docker.just\nbuild: _ensure", 190)],
 [("a5", W12, "build 先跑依賴 _ensure：\njust vendor_kit ensure", 210),
  ("a6", F12, "vendor.just（薄殼）ensure\n→ gen/ 的 _tools", 200),
  ("a7", W12, "docker create / cp\n抓工具 image 的 /dist", 170),
  ("a8", P12, "引擎容器 verify\n.<repo>/ 沒被改？", 160),
  ("a9", W12, "回到 build：跑\n.<repo>/script/…/build.sh", 210),
  ("a10", G12, "畫面：[verify] OK\n[build] …", 160)],
 "1 找 recipe\n（just 只讀檔）", "2 執行 recipe\n（先 ensure）")
d0b.append(v("a_err", "A", R12, "被手改 → 中止", 780, 250, 160, 40))
d0b.append(e("a_err_e", "a8", "a_err", "有", (0.5, 1), (0.5, 0), vert=True))
d0b.append(v("a_n", "A", NOTE, "剛 clone 下來時 .<repo>/ 還不在 → mod? 略過 → just 說「找不到 recipe」\n→ 先打 just vendor_kit ensure 把工具檔裝好（見 d0 頁②）", 1110, 70, 480, 50))
trace("B", "例 (b)：just vendor_kit diff <repo> ── 引擎自己的指令（走模組 vendor_kit，不經過工具）", 740, 250,
 [("b0", G12, "just vendor_kit diff base", 200),
  ("b1", F12, "根 justfile\nimport entry.just", 150),
  ("b2", F12, ".vendor_kit/entry.just\nmod vendor_kit 'vendor.just'", 220),
  ("b3", F12, "vendor.just（薄殼）\nimport? gen/vendor_kit.just", 220),
  ("b4", F12, "gen/vendor_kit.just\n的 diff recipe", 160)],
 [("b5", W12, "先 just vendor_kit ensure\n（同 (a) 的第 2 列）", 200),
  ("b6", W12, "docker create / cp\n抓工具 image 的 /dist", 170),
  ("b7", P12, "引擎容器 diff：讀 baseline、\n新範本、你的檔", 240),
  ("b8", W12, "印三段差異\n（不改任何檔）", 150),
  ("b9", G12, "畫面：diff 結果", 150)],
 "1 找 recipe\n（just 只讀檔）", "2 執行 recipe\n（先 ensure）")
d0b.append(v("z_n", "1", NOTE, "主圖第 5 頁畫的是第 5 層「引擎容器裡面」每個子命令（install / verify / init / diff / accept …）的細節；這頁是它的前情：指令怎麼從 just 一路傳到那裡、結果又寫回專案哪裡。", 40, 1010, 1500, 44))
# 圖例（本頁沒有判斷菱形，不用 legend_flow）
_lg = [(LEGEND_BOX(NEUTRAL), "淺灰：分組（無狀態意義）", 200, 60, 0), (ELLIPSE(GREEN), "綠：起點／終點", 130, 40, 10), (ELLIPSE(RED), "紅：錯誤終止", 130, 40, 10),
       (PURPLE_LEAF, "紫：引擎（在容器內執行）", 190, 40, 10), (LEAF(), "白：步驟", 88, 40, 10), (FILE, "虛線框：專案裡的檔案", 170, 40, 10),
       (LEAF(GREEN) + "dashed=1;", "綠虛線框：工具檔（不進 git）", 210, 40, 10), (NOTE, "便條：補充說明", 130, 40, 10)]
_x = 40
for _i, (_st, _t, _w, _h, _dy) in enumerate(_lg):
    d0b.append(v(f"d0b_lg{_i}", "1", _st, _t, _x, 1074 + _dy, _w, _h)); _x += _w + 20
d0b.append(v("d0b_lgt", "1", TEXT(12) + "align=left;", "實線 = 呼叫／執行順序（指向檔案 = 寫入）\n虛線箭頭 = 引擎反過來產生 gen/", _x, 1074, 300, 60))
d0b += terms("d0b", 40, 1170, [
 ("薄殼", ".vendor_kit/ 裡進 git 的兩個小檔（entry.just、vendor.just）：只負責把 just 接到引擎，本身沒有邏輯；引擎升級時整個換新"),
 ("gen/", ".vendor_kit/gen/：引擎每次 ensure 依 .version 產生的 recipe 與工具清單；不進 git，壞了刪掉再跑 just vendor_kit ensure 就回來"),
 ("模組（mod）", "just 的 mod：把另一個 justfile 掛成自己的命名空間，指令變成 just <命名空間> <recipe>（例：just vendor_kit diff、just docker build）"),
 ("import", "just 的 import：把另一個檔的 recipe 直接併進來（同一層、不加前綴）；import? / mod? 的問號 = 檔不在就略過、不報錯"),
 ("ensure", "引擎的自動檢查：引擎版本對了嗎 → gen/ 要不要重產生 → 每個工具裝了沒、有沒有被改；工具的每個指令都先跑它"),
 ("引擎", "vendor_kit:vN 這個 image：所有真正的工作（install / verify / init / diff / accept …）都在它的容器裡跑；主機只需要 docker + git + just"),
], vw=1200)
pages.insert(1, ("d0b", "just 與 vendor_kit 怎麼接", d0b))

