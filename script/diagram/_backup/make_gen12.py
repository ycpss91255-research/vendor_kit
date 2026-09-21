s = open("gen11.py", encoding="utf-8").read()

# legend_flow：可關掉紫色項、加「虛線框 = 專案裡的檔案」
s = s.replace('def legend_flow(prefix, x, y):\n    c = []',
              'FILE = LEAF() + "dashed=1;"\ndef legend_flow(prefix, x, y, purple=True, files=False):\n    c = []')
s = s.replace('''    c.append(v(f"{prefix}_lg4", "1", PURPLE_LEAF, "紫：在容器內執行", x + 670, y + 10, 160, 40))
    c.append(v(f"{prefix}_lg5", "1", LEAF(), "白：步驟", x + 850, y + 10, 88, 40))
    c.append(v(f"{prefix}_lg6", "1", TEXT(12) + "align=left;", "實線 = 執行順序", x + 960, y, 260, 60))''',
'''    if purple:
        c.append(v(f"{prefix}_lg4", "1", PURPLE_LEAF, "紫：子命令（在容器內執行）", x + 670, y + 10, 200, 40))
    c.append(v(f"{prefix}_lg5", "1", LEAF(), "白：步驟", x + 890, y + 10, 88, 40))
    if files:
        c.append(v(f"{prefix}_lg7", "1", FILE, "虛線框：專案裡的檔案", x + 1000, y + 10, 160, 40))
    c.append(v(f"{prefix}_lg6", "1", TEXT(12) + "align=left;", "實線 = 執行順序", x + 1180, y, 200, 60))''')

s3 = s.index("# ================= Page 3: 流程：使用者指令 =================")
e3 = s.index("# ================= Page 3: 流程：版本生命週期 =================")
p3 = r'''# ================= Page 3: 流程：使用者指令 =================
p2 = [v("title", "1", TITLE, "流程：使用者下的每個指令 → 啟動器叫哪個子命令 → 專案裡發生什麼", 40, 20, 1200, 30)]
for name, x, w in [("使用者", 40, 300), ("啟動器（justfile，在主機）", 380, 360), ("安裝容器（vendor_kit）", 800, 360), ("專案目錄", 1240, 360)]:
    p2.append(v(f"h_{x}", "1", "text;html=1;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;", name, x, 60, w, 24))
def band(bid, title, y, h):
    p2.append(v(bid, "1", SW(NEUTRAL), title, 20, y, 1620, h))
# ---- A 第一次 ----
band("bA", "第一次接上 base：just init", 100, 280)
p2.append(v("a_u", "bA", ELLIPSE(GREEN), "just init", 60, 70, 180, 50))
p2.append(v("a_l1", "bA", LEAF(), "讀 .version", 380, 75, 140, 40))
p2.append(v("a_l2", "bA", LEAF(), ".base/ 不存在\n→ 要安裝", 560, 70, 160, 50))
p2.append(v("a_c1", "bA", PURPLE_LEAF, "install\ndist/ 全部 → .base/\n並寫印記（.base/.stamp：版本 + 每檔指紋）", 800, 55, 340, 70))
p2.append(v("a_p1", "bA", FILE, ".base/（新）", 1240, 70, 200, 40))
p2.append(v("a_c2", "bA", PURPLE_LEAF, "init\n照 init.toml 複製初始檔（已存在則跳過）", 800, 165, 340, 60))
p2.append(v("a_p2", "bA", FILE, "Dockerfile、entrypoint、hooks…\n（新；之後由你維護）", 1240, 165, 200, 60))
p2.append(e("ae1", "a_u", "a_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae2", "a_l1", "a_l2", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae3", "a_l2", "a_c1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae4", "a_c1", "a_p1", "寫入", (1, 0.5), (0, 0.5)))
p2.append(e("ae5", "a_c1", "a_c2", "", (0.5, 1), (0.5, 0)))
p2.append(e("ae6", "a_c2", "a_p2", "建立", (1, 0.5), (0, 0.5)))
# ---- B 日常 ----
band("bB", "日常：just build（run / exec / stop 同）", 410, 390)
p2.append(v("b_u", "bB", ELLIPSE(GREEN), "just build", 60, 70, 180, 50))
p2.append(v("b_l1", "bB", LEAF(), "讀 .version", 380, 75, 140, 40))
p2.append(v("b_l2", "bB", RHOMBUS, "印記的版本\n= .version？", 550, 55, 180, 80))
p2.append(v("b_c0", "bB", PURPLE_LEAF, "install\n換成 .version 指定的版本", 800, 65, 340, 60))
p2.append(v("b_p0", "bB", FILE, ".base/（換新）", 1240, 75, 200, 40))
p2.append(v("b_c1", "bB", PURPLE_LEAF, "verify\n.base/ 每檔指紋是否仍等於印記", 800, 170, 340, 60))
p2.append(v("b_l3", "bB", LEAF(), "執行 .base/ 內的 build 腳本", 380, 260, 340, 50))
p2.append(v("b_p1", "bB", FILE, "docker compose build", 1240, 320, 200, 40))
p2.append(v("b_err", "bB", ELLIPSE(RED), "中止：.base/ 被改過\n刪除 .base/ 再 just build", 60, 255, 200, 60))
p2.append(e("be1", "b_u", "b_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("be2", "b_l1", "b_l2", "", (1, 0.5), (0, 0.5)))
p2.append(e("be3", "b_l2", "b_c0", "不同", (1, 0.5), (0, 0.5)))
p2.append(e("be4", "b_l2", "b_c1", "相同", (0.5, 1), (0, 0.5), vert=True))
p2.append(e("be5", "b_c0", "b_p0", "覆蓋", (1, 0.5), (0, 0.5)))
p2.append(e("be6", "b_p0", "b_l3", "", (0.5, 1), (1, 0.5)))
p2.append(e("be7", "b_c1", "b_l3", "通過", (0.5, 1), (1, 0.5), vert=True))
p2.append(e("be8", "b_c1", "b_err", "失敗", (0, 0.5), (1, 0.5)))
p2.append(e("be9", "b_l3", "b_p1", "", (0.5, 1), (0, 0.5)))
# ---- C 升級 ----
band("bC", "升級：Renovate 開的 PR 被 merge（或 just upgrade）", 830, 300)
p2.append(v("c_u", "bC", ELLIPSE(GREEN), "merge PR\n（.version 改了）", 60, 60, 180, 60))
p2.append(v("c_l1", "bC", LEAF(), "下次 just build 走上面\n「不同」分支 → install 新版", 380, 65, 340, 50))
p2.append(v("c_p1", "bC", FILE, ".base/（新版）", 1240, 70, 200, 40))
p2.append(v("c_u2", "bC", ELLIPSE(GREEN), "just diff", 60, 160, 180, 50))
p2.append(v("c_c2", "bC", PURPLE_LEAF, "diff\n新版模板 vs 你的初始檔", 800, 155, 340, 60))
p2.append(v("c_p2", "bC", FILE, "Dockerfile 等（你的）", 1240, 165, 200, 40))
p2.append(v("c_u3", "bC", ELLIPSE(GREEN), "看差異，自己決定\n要不要改", 60, 230, 180, 55))
p2.append(e("ce1", "c_u", "c_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ce2", "c_l1", "c_p1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ce3", "c_u2", "c_c2", "", (1, 0.5), (0, 0.5)))
p2.append(e("ce4", "c_p2", "c_c2", "讀", (0, 0.5), (1, 0.5)))
p2.append('<mxCell id="ce5" value="印出差異" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="bC" source="c_c2" target="c_u3"><mxGeometry x="0.4" relative="1" as="geometry"><Array as="points"><mxPoint x="970" y="258"/><mxPoint x="300" y="258"/></Array></mxGeometry></mxCell>')
p2.append(v("p2n", "1", NOTE, "四個紫框 = 四個子命令：install（第一次、版本改變時）、init（只有第一次）、verify（每次日常）、diff（升級後由使用者呼叫）。\nRenovate：GitHub 上的機器人，GHCR 有新版就自動開 PR 改 .version；沒有它時用 just upgrade 手動改。", 20, 1150, 1620, 50))
p2 += legend_flow("p2", 40, 1220, files=True)

'''
s = s[:s3] + p3 + s[e3:]
s = s.replace('page("p2", "3. 流程：使用者指令", p2, w=1700, h=1180)', 'page("p2", "3. 流程：使用者指令", p2, w=1700, h=1320)')

# ---------- 頁 5 補缺口 ----------
R = {
 'p4.append(v("i3", "init", LEAF(), "取下一項（src → dest）", 120, 320, 200, 40))': 'p4.append(v("i3", "init", LEAF(), "取下一項\\n（image 的 dist/src → 專案的 dest）", 110, 315, 220, 50))',
 'p4.append(v("ln", "install", NOTE, "任一步失敗即中止，舊 .base/ 不動；\\n啟動器不會執行工具檔", 60, 490, 260, 50))': 'p4.append(v("ln", "install", NOTE, "任一步失敗即中止，舊 .base/ 不動；\\n啟動器不會執行 .base/ 內的腳本", 60, 490, 260, 50))',
 'p4.append(v("d1", "diff", LEAF(), "對 init.toml 的每一項：\\n新版 src vs 專案內的 dest", 100, 130, 240, 50))': 'p4.append(v("d1", "diff", LEAF(), "對 init.toml 的每一項：\\nimage 內的新版 src vs 專案內的 dest", 100, 130, 240, 50))',
 'p4.append(v("d5", "diff", LEAF(), "顯示差異\\n（不改使用者檔案）", 240, 335, 180, 60))': 'p4.append(v("d5", "diff", LEAF(), "顯示差異", 240, 340, 180, 50))\np4.append(v("d6", "diff", ELLIPSE(GREEN), "結束（不改使用者檔案）", 220, 420, 220, 40))\np4.append(e("de5", "d5", "d6"))',
 'p4 += legend_flow("p4", 40, 900)': 'p4 += legend_flow("p4", 40, 900, purple=False)',
}
for k, val in R.items():
    assert s.count(k) == 1, (k, s.count(k))
    s = s.replace(k, val)
open("gen12.py", "w", encoding="utf-8").write(s)
print("ok")
