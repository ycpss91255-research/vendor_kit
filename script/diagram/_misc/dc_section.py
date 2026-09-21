# ================= 討論 DC：對外契約（PRD，待拍板） =================
import math as _math
dc = [v("title", "1", TITLE, "對外契約（PRD）── vendor_kit 要做什麼、使用者只需要三個指令、其他一律自動", 40, 20, 900, 34)]
dc.append(v("dc_pend", "1", PEND.replace("strokeColor=#d6b656", "strokeColor=#b85450"),
 "⚠ 待你回覆（與先前決議不同的地方）：\n(a) add 併進 init <repo>（不另開 add）？ (b) verify 失敗改成自動重裝（推翻 #12「中止不重裝」）？\n(c) vendor_kit 自身升級自動 re-exec，不停下來要你重跑？ (d) diff／accept 併進 upgrade（三方合併＋衝突標記，baseline 自動更新）？\n(e) undev 併成 dev <repo> 不帶 -p？ (f) upgrade 要不要 --to <tag> 選項（指定版本）？",
 960, 12, 620, 96))
DC_K = TERM_K; DC_V = TERM_V
DC_H = "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999999;fontSize=12;fontStyle=1;align=center;strokeWidth=1;"
DC_R = TERM_V + "strokeColor=#b85450;strokeWidth=2;fontColor=#b85450;"
def dc_tbl(prefix, parent, x, y, cols, rows, red=()):
    """cols: [(標題, 寬)]；rows: [[cell...]]；red: {(r,c)} 用紅框；列高依內容自動算。回傳結束 y。"""
    cx = x
    for i, (h, w) in enumerate(cols):
        dc.append(v(f"{prefix}_h{i}", parent, DC_H, h, cx, y, w, 30)); cx += w
    cy = y + 30
    for r, row in enumerate(rows):
        rh = _math.ceil(max(need_h(c, 12, w) for c, (_, w) in zip(row, cols))) + 4
        cx = x
        for i, (cell, (_, w)) in enumerate(zip(row, cols)):
            st = DC_R if (r, i) in red else (DC_K if i == 0 else DC_V)
            dc.append(v(f"{prefix}_r{r}c{i}", parent, st, cell, cx, cy, w, rh)); cx += w
        cy += rh
    return cy
Y = 130
# ---- A. 目的與角色 ----
dc.append(v("dcA", "1", SW(NEUTRAL), "A. 目的與角色", 40, Y, 1560, 150))
dc.append(v("dcA_goal", "dcA", LEAF(), "目的（一句話）：工具 repo（例：base）把自己的 dist 打包成 GHCR image；下游專案只要三個指令就能拿到工具檔、跟上新版、在本機開發工具本身。\n契約只對右邊前兩個角色承諾：他們照契約用一定可以，改了介面就要升版並公告。",
 20, 50, 700, 84).replace("fontSize=14", "fontSize=12;align=left;spacingLeft=8"))
dc.append(v("dcA_r1", "dcA", LEAF(YELLOW).replace("fontSize=14", "fontSize=12"), "工具 repo 開發者（供應側）\n照 §E 規格出貨 dist 與 image", 760, 50, 250, 84))
dc.append(v("dcA_r2", "dcA", LEAF(YELLOW).replace("fontSize=14", "fontSize=12"), "使用者（下游專案）\n每天打 just 的人；只需要 §B 三個指令", 1030, 50, 250, 84))
dc.append(v("dcA_r3", "dcA", LEAF().replace("fontSize=14", "fontSize=12"), "vendor_kit 開發者（我們）\n維護引擎與啟動器；契約不對自己承諾", 1300, 50, 240, 84))
Y += 170
# ---- B. 使用者介面 ----
B_COLS = [("介面", 250), ("什麼時候用", 200), ("做什麼", 840), ("結束狀態", 230)]
B_ROWS = [
 ["bootstrap.sh\n（release 附的腳本，只跑一次）", "專案第一次接 vendor_kit", "問你「要接哪個工具、哪個版本」→ 寫 .version、根 justfile 一行 import、.vendor_kit/ 薄殼（進 git）→ 直接跑 install + init → 腳本自刪", "0 成功\n1 失敗（什麼都沒寫）"],
 ["just vendor_kit init [<repo>]", "加工具、或補初始檔", "不給 <repo>：把 .version 裡每個工具的初始檔補齊。給 <repo>：不在 .version 就問版本並寫進去（這就吃掉了 add），再 install + init。已存在的檔只 warn、不覆蓋", "0 成功\n1 失敗"],
 ["just vendor_kit upgrade [<repo>]", "想跟上新版（沒 Renovate、或想馬上升）", "查 GHCR 最新 → 改 .version → install → 三方合併初始檔（§D）→ 印摘要。不給 <repo> = 全部工具；含 vendor_kit 自己", "0 完成\n1 失敗（.version 不動）\n2 有衝突要你改"],
 ["just vendor_kit dev <repo> -p/--path <dir>", "開發工具本身，想在專案裡直接試", ".<repo>/ 改指向本機目錄（寫 .version.local，不進 git）；再打一次 dev <repo> 不帶 -p = 解除（不另開 undev）", "0 成功\n1 失敗"],
]
bh = 50 + 30 + sum(_math.ceil(max(need_h(c, 12, w) for c, (_, w) in zip(r, B_COLS))) + 4 for r in B_ROWS) + 20
dc.append(v("dcB", "1", SW(NEUTRAL), "B. 使用者介面：bootstrap.sh + 3 個指令（其他全部隱藏，見 C）", 40, Y, 1560, bh))
dc_tbl("dcB", "dcB", 20, 50, B_COLS, B_ROWS)
Y += bh + 20
# ---- C. ensure 自動做 ----
C_COLS = [("狀況", 360), ("以前的做法", 480), ("改成自動（每次打 just，ensure 先跑）", 680)]
C_ROWS = [
 ["clone 後 .<repo>/ 不存在", "ensure → install", "同：install 後才跑你要的指令"],
 [".version 被 pull／revert 改了", "印記第一行 ≠ .version → install", "同；回退 = git revert 那個 commit，沒有指令"],
 [".<repo>/ 被手改（verify 失敗）", "#12 決議：中止、不自動重裝", "改成自動重裝：.<repo>/ 不進 git、使用者本來就不該改，重裝沒有損失；只印一行 warn"],
 [".version 的 vendor_kit 那行變了", "upgrade C 案：先換自己、停下來要你重跑", "改成自動：啟動器換完 .vendor_kit/gen/ 後直接 exec 新版跑同一個指令，使用者無感"],
 ["Renovate 開 PR 升版", "走 upgrade 那條線", "不變：merge 後每個人下次打 just 就自動 install，零指令"],
 ["docker 沒裝／沒網路／鎖逾時", "報錯", "報錯（這種真的無法自動）：訊息要寫清楚缺什麼、怎麼補"],
]
ch = 50 + 30 + sum(_math.ceil(max(need_h(c, 12, w) for c, (_, w) in zip(r, C_COLS))) + 4 for r in C_ROWS) + 20
dc.append(v("dcC", "1", SW(NEUTRAL), "C. 其他全部由 ensure 自動做（每次打 just 都跑）── 紅框 = 與先前決議不同", 40, Y, 1560, ch))
dc_tbl("dcC", "dcC", 20, 50, C_COLS, C_ROWS, red={(2, 2), (3, 2)})
Y += ch + 20
# ---- D. 唯一無法自動化：三方合併 ----
dc.append(v("dcD", "1", SW(NEUTRAL), "D. 唯一無法自動化的地方：upgrade 後初始檔衝突（跟 git merge 一樣處理）", 40, Y, 1560, 300))
F12 = FILE.replace("fontSize=14", "fontSize=12")
L12 = LEAF().replace("fontSize=14", "fontSize=12")
dc.append(v("dcD_in1", "dcD", F12, "baseline\n.vendor_kit/baseline/<repo>/（上一版範本）", 20, 60, 280, 50))
dc.append(v("dcD_in2", "dcD", F12, "你現在的檔\n（專案裡的初始檔，可能改過）", 20, 130, 280, 50))
dc.append(v("dcD_in3", "dcD", F12, "新版範本\n（新版工具 image 的 init 檔）", 20, 200, 280, 50))
dc.append(v("dcD_m", "dcD", PURPLE_LEAF.replace("fontSize=14", "fontSize=12"), "upgrade 逐檔三方合併\n（git merge-file）", 400, 60, 200, 190))
dc.append(v("dcD_o1", "dcD", L12, "你沒改過 → 直接換成新版", 700, 60, 280, 50))
dc.append(v("dcD_o2", "dcD", L12, "只有你改、工具沒改 → 不動", 700, 130, 280, 50))
dc.append(v("dcD_o3", "dcD", L12.replace("strokeColor=light-dark(#000000,#9577A3)", "strokeColor=#b85450;strokeWidth=2"), "兩邊都改 → 檔案裡留 <<<<<<< 衝突標記\nupgrade 回 2 並列出檔名，你在編輯器解掉即可", 700, 200, 280, 50))
dc.append(v("dcD_note", "dcD", NOTE, "所以不需要 diff／accept 兩個指令：\n・baseline 由 upgrade 自動推到新版（合併完就是新基準），不需 accept\n・diff 變成 upgrade --dry-run（只印會動哪些檔，不寫）\n・解完衝突不用再打任何指令；下次 just 只會 ensure、不會再合併\n・二進位檔無法合併：保留你的，印 warn", 1020, 60, 520, 190))
# 三個輸入中心 y = 85/155/225；合併節點 y=60 h=190 → 分數 = (c-60)/190
_fr = [(85 - 60) / 190, (155 - 60) / 190, (225 - 60) / 190]
for i, f in enumerate(_fr, 1):
    dc.append(e(f"dcD_e{i}", f"dcD_in{i}", "dcD_m", "", (1, 0.5), (0, round(f, 4))))
    dc.append(e(f"dcD_f{i}", "dcD_m", f"dcD_o{i}", "", (1, round(f, 4)), (0, 0.5)))
Y += 320
# ---- E. 供應側 ／ F. 專案裡的檔 ----
dc.append(v("dcE", "1", SW(NEUTRAL), "E. 對工具 repo 的介面（供應側，不變）", 40, Y, 760, 250))
dc.append(v("dcE_1", "dcE", L12, "dist/：files/（要裝進 .<repo>/ 的全部檔）、init.toml（[[file]] src／dest 初始檔清單）、just/<repo>.just（工具自己的指令）", 20, 50, 720, 44))
dc.append(v("dcE_2", "dcE", L12, "Dockerfile.dist：FROM scratch，只 COPY dist/ 到 /dist；不 FROM vendor_kit、沒有程式", 20, 104, 720, 40))
dc.append(v("dcE_3", "dcE", L12, "image 命名 <repo>-dist:<tag>，多架構 amd64 + arm64（同一個 tag）", 20, 154, 720, 40))
dc.append(v("dcE_4", "dcE", L12, "工具自己的指令（just <repo> …、just docker …）由工具的 just 模組提供；vendor_kit 不定義、不出現在 §B", 20, 204, 720, 40))
dc.append(v("dcF", "1", SW(NEUTRAL), "F. 專案裡的檔（誰進 git）", 840, Y, 760, 250))
dc.append(v("dcF_g", "dcF", F12.replace("dashed=1;", "") + "align=left;spacingLeft=8;verticalAlign=top;spacingTop=6;", "進 git\n・.version（引擎一行 + 每個工具一行）\n・根 justfile 的一行 import '.vendor_kit/entry.just'\n・.vendor_kit/entry.just、vendor.just（薄殼）\n・.vendor_kit/ci/check.sh\n・.vendor_kit/baseline/<repo>/（三方合併的基準）\n・初始檔（init 複製出來、你的）", 20, 50, 350, 180).replace("rounded=1", "rounded=0"))
dc.append(v("dcF_n", "dcF", F12 + "align=left;spacingLeft=8;verticalAlign=top;spacingTop=6;", "不進 git（引擎隨時能重建）\n・.vendor_kit/gen/（ensure 每次重產的其餘指令）\n・.<repo>/（工具檔全部 + .stamp 印記）\n・.version.local（dev 模式的本機覆蓋）", 390, 50, 350, 180))
Y += 270
dc += legend("dc", 40, Y, ["yellow", "pimg", "white", "file", "note"], "實線 = 資料流向\n紅框 = 與先前決議不同的地方")
dc += terms("dc", 40, Y + 110, [
 ("對外契約", "我們承諾「這樣用一定可以、不會隨便改」的介面清單；改了就要升版並公告"),
 ("bootstrap.sh", "release 附的一次性腳本：詢問後寫出 .version／justfile／.vendor_kit/ 並跑 install + init，然後自刪"),
 ("ensure", "每次打 just 都先跑的自動檢查：.<repo>/ 缺、舊、被改都自動修好，vendor_kit 自己版本變了也自動換"),
 ("三方合併／baseline", "拿「上一版範本（baseline）、你現在的檔、新版範本」三份比對，能自動合的就合；baseline 存在 .vendor_kit/baseline/<repo>/"),
 ("衝突標記", "跟 git 一樣的 <<<<<<< ======= >>>>>>> 記號，寫在檔案裡讓你自己選要留哪邊"),
 (".version.local", "dev 模式寫的本機覆蓋檔（不進 git）：某個工具改用本機目錄而不是 image"),
 ("GHCR", "GitHub Container Registry；工具 image 放的地方，.version 記完整位址與 digest"),
 ("Renovate", "GitHub 上的機器人：發現 GHCR 有新版就自動開 PR 改 .version；自動升級那條線靠它"),
 ("結束狀態 0／1／2", "指令結束時的數字：0 成功、1 失敗（沒有寫任何東西）、2 完成但有衝突要你處理"),
 ("<repo>", "工具 repo 名（例：base）；.<repo>/ = 專案裡裝好的工具檔"),
])
