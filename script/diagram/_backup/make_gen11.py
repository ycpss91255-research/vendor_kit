s = open("gen10.py", encoding="utf-8").read()

# ---------- land → install（全檔） ----------
s = s.replace('"land"', '"install"').replace("land（安裝／upgrade）", "install（安裝）").replace("開始 land", "開始 install")
s = s.replace("啟動安裝容器，執行 land", "啟動安裝容器，執行 install").replace("land 內部步驟見第 5 頁", "install 內部步驟見第 5 頁")
s = s.replace("docker run\\n… land", "docker run\\n… install").replace("（不進 git，land 寫出）", "（不進 git，install 寫出）")
s = s.replace("執行 just → 啟動器用新版 image 重新安裝", "執行 just → 啟動器自動 install 新版")

# ---------- 第 3 頁重寫：使用者指令 → 子命令 ----------
s3 = s.index("# ================= Page 3: 流程：啟動器 =================")
e3 = s.index("# ================= Page 3: 流程：版本生命週期 =================")
p3 = r'''# ================= Page 3: 流程：使用者指令 =================
p2 = [v("title", "1", TITLE, "流程：使用者下的每個指令，啟動器叫了哪個子命令、專案裡發生什麼", 40, 20, 1200, 30)]
COLS = [("使用者", 40), ("啟動器（justfile，在主機）", 380), ("安裝容器（vendor_kit）", 800), ("專案目錄", 1240)]
for name, x in COLS:
    p2.append(v(f"h_{x}", "1", "text;html=1;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;", name, x, 60, 360 if x != 40 else 300, 24))
def band(bid, title, y, h):
    p2.append(v(bid, "1", SW(NEUTRAL), title, 20, y, 1620, h))
# ---- A 第一次 ----
band("bA", "第一次接上 base：just init", 100, 270)
p2.append(v("a_u", "bA", ELLIPSE(GREEN), "just init", 60, 70, 180, 50))
p2.append(v("a_l1", "bA", LEAF(), "讀 .version", 380, 75, 140, 40))
p2.append(v("a_l2", "bA", LEAF(), ".base/ 不存在\n→ 要安裝", 560, 70, 160, 50))
p2.append(v("a_c1", "bA", PURPLE_LEAF, "install\ndist/ 全部 → .base/，寫印記", 800, 65, 340, 60))
p2.append(v("a_p1", "bA", LEAF(), ".base/（新）", 1240, 75, 200, 40))
p2.append(v("a_c2", "bA", PURPLE_LEAF, "init\n照 init.toml 複製初始檔（已存在則跳過）", 800, 160, 340, 60))
p2.append(v("a_p2", "bA", LEAF(), "Dockerfile、entrypoint、\nhooks…（新，之後歸你）", 1240, 160, 200, 60))
p2.append(e("ae1", "a_u", "a_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae2", "a_l1", "a_l2", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae3", "a_l2", "a_c1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ae4", "a_c1", "a_p1", "寫入", (1, 0.5), (0, 0.5)))
p2.append(e("ae5", "a_c1", "a_c2", "", (0.5, 1), (0.5, 0)))
p2.append(e("ae6", "a_c2", "a_p2", "建立", (1, 0.5), (0, 0.5)))
# ---- B 日常 ----
band("bB", "日常：just build（run / exec / stop 同）", 400, 300)
p2.append(v("b_u", "bB", ELLIPSE(GREEN), "just build", 60, 70, 180, 50))
p2.append(v("b_l1", "bB", LEAF(), "讀 .version", 380, 75, 140, 40))
p2.append(v("b_l2", "bB", RHOMBUS, "印記的版本\n= .version？", 550, 55, 180, 80))
p2.append(v("b_c1", "bB", PURPLE_LEAF, "verify\n.base/ 每檔指紋 = 印記？", 800, 65, 340, 60))
p2.append(v("b_l3", "bB", LEAF(), "執行 .base/ 內的\nbuild 腳本", 560, 190, 160, 50))
p2.append(v("b_p1", "bB", LEAF(), "docker compose build", 1240, 195, 200, 40))
p2.append(v("b_err", "bB", ELLIPSE(RED), "中止：.base/ 被改過\n請重新安裝", 60, 185, 180, 60))
p2.append(v("b_c0", "bB", PURPLE_LEAF, "install（同「升級」那條）", 800, 160, 340, 40))
p2.append(e("be1", "b_u", "b_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("be2", "b_l1", "b_l2", "", (1, 0.5), (0, 0.5)))
p2.append(e("be3", "b_l2", "b_c1", "相同", (1, 0.5), (0, 0.5)))
p2.append(e("be4", "b_l2", "b_c0", "不同", (0.5, 1), (0, 0.5)))
p2.append(e("be5", "b_c1", "b_l3", "相符", (0.5, 1), (1, 0.3), vert=True))
p2.append(e("be6", "b_c0", "b_l3", "", (0, 0.5), (1, 0.7)))
p2.append(e("be7", "b_l3", "b_p1", "", (1, 0.5), (0, 0.5)))
p2.append('<mxCell id="be8" value="不符" style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="bB" source="b_c1" target="b_err"><mxGeometry x="0.5" relative="1" as="geometry"><Array as="points"><mxPoint x="1180" y="95"/><mxPoint x="1180" y="265"/><mxPoint x="300" y="265"/><mxPoint x="300" y="215"/></Array></mxGeometry></mxCell>')
# ---- C 升級 ----
band("bC", "升級：Renovate 開的 PR 被 merge（或 just upgrade）", 730, 270)
p2.append(v("c_u", "bC", ELLIPSE(GREEN), "merge PR\n（.version 改了）", 60, 65, 180, 60))
p2.append(v("c_l1", "bC", LEAF(), "下次 just：\n印記版本 ≠ .version", 380, 70, 160, 50))
p2.append(v("c_c1", "bC", PURPLE_LEAF, "install\n整批換成新版 .base/", 800, 65, 340, 60))
p2.append(v("c_p1", "bC", LEAF(), ".base/（新版）", 1240, 75, 200, 40))
p2.append(v("c_c2", "bC", PURPLE_LEAF, "diff\n新版模板 vs 你的 Dockerfile 等", 800, 160, 340, 60))
p2.append(v("c_u2", "bC", ELLIPSE(GREEN), "看差異，自己決定\n要不要改", 60, 165, 180, 60))
p2.append(e("ce1", "c_u", "c_l1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ce2", "c_l1", "c_c1", "", (1, 0.5), (0, 0.5)))
p2.append(e("ce3", "c_c1", "c_p1", "覆蓋", (1, 0.5), (0, 0.5)))
p2.append(e("ce4", "c_c1", "c_c2", "just diff", (0.5, 1), (0.5, 0), vert=True))
p2.append(e("ce5", "c_c2", "c_u2", "印出差異", (0, 0.5), (1, 0.5)))
p2.append(v("p2n", "1", NOTE, "紫框 = 四個子命令各自出現的地方：install（第一次、升級、版本不同時）、init（只有第一次）、verify（每次日常）、diff（升級後）。\nRenovate 是 GitHub 上的機器人：GHCR 有新版就自動開 PR 改 .version；沒有它時用 just upgrade 手動改。", 20, 1010, 1620, 50))
p2 += legend_flow("p2", 40, 1080)

'''
s = s[:s3] + p3 + s[e3:]
s = s.replace('page("p2", "3. 流程：啟動器", p2)', 'page("p2", "3. 流程：使用者指令", p2, w=1700, h=1180)')
open("gen11.py", "w", encoding="utf-8").write(s)
print("ok")
