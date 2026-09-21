# ================= Page 11: 流程：升級與回退（初版，供討論） =================
# 四條路徑：A Renovate 自動、B just upgrade 手動、C vendor_kit 自身升級、D 回退。待決處用便條標「待決」。
p12 = [v("title", "1", TITLE, "流程：升級與回退 ── 四條路徑（初版，待決處以便條標示）", 40, 20, 1300, 30)]
COLS_U = [("使用者", 40, 260), ("Renovate 機器人（GitHub 上）", 320, 240), ("啟動器（.vendor_kit/，在主機）", 580, 320), ("vendor_kit 容器", 920, 320), ("專案目錄", 1260, 300)]
for name, x, w in COLS_U:
    p12.append(v(f"uh_{x}", "1", "text;html=1;fontSize=14;fontStyle=1;align=center;verticalAlign=middle;", name, x, 60, w, 24))
def uband(bid, title, y, h):
    p12.append(v(bid, "1", SW(NEUTRAL), title, 20, y, 1560, h))

# ---- A：Renovate 自動 ----
uband("uA", "A. 自動：Renovate 發現 GHCR 有新版（正常情況走這條）", 100, 330)
p12.append(v("a0", "uA", ELLIPSE(GREEN), "起點：GHCR 出現\n<name>-dist 新 tag", 340, 55, 200, 50))
p12.append(v("a1", "uA", LEAF(), "開 PR：改 .version 那一行\n（tag 與 digest 一起換）", 340, 130, 200, 50))
p12.append(v("a2", "uA", LEAF(), "CI 在 PR 上跑 just\n（install + verify + 工具的煙霧測試）", 600, 130, 280, 50))
p12.append(v("a3", "uA", ELLIPSE(GREEN), "看 CI 綠、merge PR", 60, 130, 220, 50))
p12.append(v("a4", "uA", LEAF(), "每個人下次打 just：\n印記第一行 ≠ .version → install", 600, 215, 280, 50))
p12.append(v("a5", "uA", PURPLE_LEAF, "install 新版", 940, 215, 280, 50))
p12.append(v("a6", "uA", FILE, ".<name>/（新版）", 1280, 215, 260, 50))
p12.append(v("a7", "uA", ELLIPSE(GREEN), "just diff → 跟進 → just accept\n（第 5 頁 diff／accept 泳道）", 60, 215, 220, 60))
p12.append(v("a8", "uA", FILE, ".vendor_kit/baseline/<name>/（更新）", 1280, 280, 260, 40))
p12.append(e("ae1", "a0", "a1", "", (0.5, 1), (0.5, 0)))
p12.append(e("ae2", "a1", "a2", "PR", (1, 0.5), (0, 0.5)))
p12.append('<mxCell id="ae3" value="CI 結果" style="' + EDGE + 'exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="uA" source="a2" target="a3"><mxGeometry x="0.3" relative="1" as="geometry"><Array as="points"><mxPoint x="740" y="110"/><mxPoint x="170" y="110"/></Array></mxGeometry></mxCell>')
p12.append('<mxCell id="ae4" value="merge 後" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="uA" source="a3" target="a4"><mxGeometry x="0.5" relative="1" as="geometry"><Array as="points"><mxPoint x="170" y="240"/></Array></mxGeometry></mxCell>')
p12.append(e("ae5", "a4", "a5", "", (1, 0.5), (0, 0.5)))
p12.append(e("ae6", "a5", "a6", "寫入", (1, 0.5), (0, 0.5)))
p12.append('<mxCell id="ae7" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="uA" source="a4" target="a7"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="740" y="300"/><mxPoint x="170" y="300"/></Array></mxGeometry></mxCell>')
p12.append('<mxCell id="ae8" value="accept 寫入" style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="uA" source="a7" target="a8"><mxGeometry x="0.7" relative="1" as="geometry"><Array as="points"><mxPoint x="300" y="245"/><mxPoint x="300" y="300"/><mxPoint x="1250" y="300"/></Array></mxGeometry></mxCell>')
p12.append(v("an", "uA", NOTE, "待決：CI 在 PR 上要跑到哪一步（只 install+verify，還是連工具的 build 都跑）？Renovate 對 .version（自訂 TOML）用 regex manager，設定由 vendor_kit 出貨還是各專案自寫？", 940, 55, 600, 60))

# ---- B：手動 just upgrade ----
uband("uB", "B. 手動：just upgrade <name>（沒有 Renovate、或想馬上升）", 460, 260)
p12.append(v("b0", "uB", ELLIPSE(GREEN), "just upgrade <name>", 60, 60, 220, 50))
p12.append(v("b1", "uB", LEAF(), "起 vendor_kit 容器跑 upgrade 子命令", 600, 60, 280, 50))
p12.append(v("b2", "uB", PURPLE_LEAF, "查 GHCR：<name>-dist 最新 tag + digest\n（要網路；只查不裝）", 940, 60, 280, 50))
p12.append(v("b3", "uB", FILE, ".version 那一行改成新版", 1280, 60, 260, 50))
p12.append(v("b4", "uB", LEAF(), "接著同 A：印記 ≠ .version → install", 600, 150, 280, 50))
p12.append(v("b5", "uB", ELLIPSE(GREEN), "just diff → 跟進 → accept\n→ commit .version 與修改", 60, 145, 220, 60))
p12.append(e("be1", "b0", "b1", "", (1, 0.5), (0, 0.5)))
p12.append(e("be2", "b1", "b2", "", (1, 0.5), (0, 0.5)))
p12.append(e("be3", "b2", "b3", "改一行", (1, 0.5), (0, 0.5)))
p12.append('<mxCell id="be4" value="" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="uB" source="b3" target="b4"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="1410" y="130"/><mxPoint x="740" y="130"/></Array></mxGeometry></mxCell>')
p12.append(e("be5", "b4", "b5", "", (0, 0.5), (1, 0.5)))
p12.append(v("bn", "uB", NOTE, "待決：upgrade 只改 .version 就停（讓使用者自己打 just 觸發 install），還是一路做到 install + diff？「查最新版」要在容器內用什麼查 GHCR（registry API）？要不要 --dry-run（只印不改）？", 940, 130, 600, 60))

# ---- C：vendor_kit 自身升級 ----
uband("uC", "C. vendor_kit 自己升級（啟動器 .vendor_kit/ 換新）", 750, 240)
p12.append(v("c0", "uC", FILE, ".version 的 vendor_kit 那一行改了\n（走 A 或 B，跟工具一樣）", 1280, 55, 260, 50))
p12.append(v("c1", "uC", LEAF(), "下次 just：.vendor_kit/.stamp 第一行\n≠ .version 的 vendor_kit 行", 600, 55, 280, 50))
p12.append(v("c2", "uC", PURPLE_LEAF, "用新版 vendor_kit image 跑 bootstrap\n只重寫 vendor.just / tools.just / .stamp", 940, 55, 280, 50))
p12.append(v("c3", "uC", FILE, ".vendor_kit/ 程式檔換新\n（baseline/、justfile、.version 不動）", 1280, 130, 260, 50))
p12.append(e("ce1", "c0", "c1", "", (0, 0.5), (1, 0.5)))
p12.append(e("ce2", "c1", "c2", "", (1, 0.5), (0, 0.5)))
p12.append('<mxCell id="ce3" value="寫入" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="uC" source="c2" target="c3"><mxGeometry x="0.6" relative="1" as="geometry"><Array as="points"><mxPoint x="1080" y="155"/></Array></mxGeometry></mxCell>')
p12.append(v("cn", "uC", NOTE, "待決（issue #14）：新啟動器會呼叫「工具 image 內建」的舊 vendor_kit，兩者版本會不一樣——參數、印記格式、init.toml 格式跨版本要相容到什麼程度？誰檢查？不相容時是拒絕、還是要求工具重新出 image？", 60, 130, 800, 70))

# ---- D：回退 ----
uband("uD", "D. 回退（升上去發現壞了）", 1020, 220)
p12.append(v("d0", "uD", ELLIPSE(GREEN), "git revert 那個升級 commit\n（.version 那行改回舊版）", 60, 55, 220, 60))
p12.append(v("d1", "uD", LEAF(), "下次 just：印記 ≠ .version\n→ install 舊版", 600, 60, 280, 50))
p12.append(v("d2", "uD", FILE, ".<name>/（舊版）", 1280, 60, 260, 50))
p12.append(e("de1", "d0", "d1", "", (1, 0.5), (0, 0.5)))
p12.append(e("de2", "d1", "d2", "寫入", (1, 0.5), (0, 0.5)))
p12.append(v("dn", "uD", NOTE, "待決：如果已經 just accept 過（baseline 變新版）才回退，git revert 同一個 commit 會把 baseline 一起退回，沒問題；但若 accept 是另一個 commit，就要一起 revert，否則 diff 會反向。要不要讓 accept 強制跟 .version 同一個 commit？\n使用者自己改過的初始檔不會自動回復（工具不碰使用者檔）。", 60, 125, 1480, 70))

p12 += legend_flow("p12", 40, 1270, files=True, note=True)
p12 += terms("p12", 40, 1380, [
 ("Renovate", "GitHub 上的機器人：發現 GHCR 有新版就自動開 PR 改 .version；沒有它時用 just upgrade 手動"),
 ("tag / digest", "image 的版本名稱／內容指紋；.version 兩者都記，一起換"),
 ("PR / merge / revert", "GitHub 上的合併請求／接受它／用 git 把某次修改整個倒回去"),
 ("印記第一行", ".<name>/.stamp 第一行 = 裝的是哪個 image；跟 .version 那行不同就重裝（第 3 頁）"),
 ("baseline / accept", "上次確認過的範本副本／告訴工具「這版我看完了」（第 5 頁、issue #22）"),
 ("bootstrap（在 C 裡）", "同第 10 頁的子命令，這裡只重寫 .vendor_kit/ 的程式檔"),
 ("issue #14", "相容性承諾這一題的 GitHub 討論串"),
])
