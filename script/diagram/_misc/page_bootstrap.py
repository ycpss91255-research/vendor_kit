# ================= Page 10: 流程：bootstrap（第一次把 vendor_kit 接進專案） =================
# 依使用者描述：release 附一個腳本 → 執行後展開 .vendor_kit/ → 問要不要跑 init → 做完腳本自己刪掉，只留 .vendor_kit/
p11 = [v("title", "1", TITLE, "流程：bootstrap ── 第一次把 vendor_kit 接進專案（release 附的腳本，跑完自己刪掉）", 40, 20, 1300, 30)]
for name, x, w in [("使用者", 40, 260), ("bootstrap.sh（在主機執行）", 340, 380), ("vendor_kit 容器", 760, 360), ("專案目錄", 1160, 360)]:
    p11.append(v(f"bh_{x}", "1", "text;html=1;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;", name, x, 60, w, 24))
p11.append(v("bs", "1", SW(NEUTRAL), "bootstrap：一次做完，之後都靠 just", 20, 100, 1520, 640))
# 使用者
p11.append(v("u0", "bs", ELLIPSE(GREEN), "下載 release 附的\nbootstrap.sh，在專案目錄執行", 30, 60, 240, 60))
p11.append(v("u1", "bs", ELLIPSE(GREEN), "完成：專案裡只剩\n.vendor_kit/、justfile、.version\n（＋ .<name>/、初始檔）", 30, 535, 240, 70))
# 腳本
p11.append(v("s1", "bs", RHOMBUS, "主機有 docker、\ngit、just？", 400, 50, 200, 80))
p11.append(v("s_err", "bs", ELLIPSE(RED), "中止：列出缺的軟體", 320, 160, 180, 50))
p11.append(v("s2", "bs", LEAF(), "docker run … vendor_kit:vN bootstrap\n（以使用者身分，掛載專案目錄）", 340, 260, 320, 50))
p11.append(v("s3", "bs", RHOMBUS, "要現在接一個\n工具嗎？", 400, 350, 200, 80))
p11.append(v("s4", "bs", LEAF(), "把 <name> = \"image\" 寫進 .version\n再執行 just init（第 3 頁「第一次」）", 340, 460, 320, 50))
p11.append(v("s5", "bs", LEAF(), "刪掉 bootstrap.sh 自己", 380, 550, 240, 40))
# 容器
p11.append(v("c1", "bs", PURPLE_LEAF, "bootstrap 子命令\n寫出啟動器與版本檔（不碰其他檔）", 760, 215, 340, 140))
# 專案目錄（虛線框 = 檔案）
p11.append(v("f1", "bs", FILE, ".vendor_kit/\n啟動器：install / init / diff / upgrade 等標準\n指令 ＋ 印記（vendor_kit 擁有，人不改，進 git）", 1160, 215, 340, 60))
p11.append(v("f2", "bs", FILE, "justfile（一行 import .vendor_kit/…；\n之後是使用者自己的指令，進 git）", 1160, 275, 340, 50))
p11.append(v("f3", "bs", FILE, ".version（先只有 vendor_kit = \"…\" 一行，進 git）", 1160, 325, 340, 40))
p11.append(v("f4", "bs", FILE, ".<name>/（不進 git）＋ 初始檔（進 git）", 1160, 465, 340, 40))
# 線
p11.append(e("be1", "u0", "s1", "", (1, 0.5), (0, 0.5)))
p11.append(e("be2", "s1", "s_err", "缺", (0.5, 1), (0.5, 0), vert="left", pos=-0.4))
p11.append('<mxCell id="be3" value="齊全" style="' + EDGE + 'align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="bs" source="s1" target="s2"><mxGeometry x="-0.6" relative="1" as="geometry"><Array as="points"><mxPoint x="690" y="90"/><mxPoint x="690" y="285"/></Array></mxGeometry></mxCell>')
p11.append(e("be4", "s2", "c1", "", (1, 0.5), (0, 0.5)))
p11.append(e("be5", "c1", "f1", "寫出", (1, 0.2143), (0, 0.5)))
p11.append(e("be6", "c1", "f2", "寫出", (1, 0.6071), (0, 0.5)))
p11.append(e("be7", "c1", "f3", "寫出", (1, 0.9286), (0, 0.5)))
p11.append(e("be8", "s2", "s3", "", (0.5, 1), (0.5, 0)))
p11.append(e("be9", "s3", "s4", "要", (0.5, 1), (0.5, 0), vert=True))
p11.append('<mxCell id="be10" value="先不要" style="' + EDGE + 'align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="bs" source="s3" target="s5"><mxGeometry x="0.2" relative="1" as="geometry"><Array as="points"><mxPoint x="310" y="390"/><mxPoint x="310" y="570"/></Array></mxGeometry></mxCell>')
p11.append(e("be11", "s4", "f4", "install + init 寫出", (1, 0.5), (0, 0.5)))
p11.append(e("be12", "s4", "s5", "", (0.5, 1), (0.5, 0)))
p11.append(e("be13", "s5", "u1", "", (0, 0.5), (1, 0.5)))
p11.append(v("bn", "1", NOTE, "之後：vendor_kit 出新版 → .version 的 vendor_kit 那行改掉（Renovate 或 just upgrade）→ .vendor_kit/ 整個換新，跟 .<name>/ 一樣；使用者的 justfile 永遠不會被動到。\nbootstrap.sh 的內容其實只有：檢查三個軟體 → 那一行 docker run → 問問題 → 自刪；主機不需要 Python。", 20, 760, 1520, 50))
p11 += legend_flow("p11", 40, 830, files=True, note=True)
p11 += terms("p11", 40, 940, [
 ("bootstrap", "第一次把工具接進專案的動作；這裡 = release 附的一個腳本，跑完自己刪掉"),
 ("啟動器 / .vendor_kit/", "just 要用的標準指令集，由 vendor_kit 寫出並擁有；使用者不改，升級整個換新"),
 ("justfile / import", "專案根目錄給 just 讀的指令清單；第一行 import 把 .vendor_kit/ 的標準指令接進來，其餘是使用者自己的"),
 (".version", "工具版本清單（TOML）；bootstrap 後先只有 vendor_kit 一行，接工具時再加一行 <name> = \"image\""),
 ("release", "vendor_kit 打 tag 發佈的一個版本：含 image（上傳 GHCR）與 bootstrap.sh（附在 GitHub release 頁）"),
 ("just init / install", "第 3 頁「第一次」流程：安裝 .<name>/ 並建立初始檔"),
 ("以使用者身分", "docker run -u UID:GID：容器寫出的檔案擁有者是你，不是 root"),
])
