src = open("gen5.py", encoding="utf-8").read()
start = src.index("# ================= Page 1: vendor_kit 架構圖 =================")
end = src.index("# ================= Page 2: 出貨路徑 =================")
new_p1 = r'''
# ================= Page 1: vendor_kit 架構圖 =================
p1 = [v("title", "1", TITLE, "vendor_kit 架構圖（模組 → 最小單元；線上文字 = 傳的資料）", 40, 20, 900, 30)]
VX, VY = 480, 140
p1.append(v("user", "1", SW(YELLOW), "使用者", 40, VY, 140, 740))
p1.append(v("u_cmd", "user", LEAF(GREY), "指令", 26, 90, 88, 40))
p1.append(v("u_out", "user", LEAF(GREY), "畫面", 26, 640, 88, 40))
p1.append(v("img", "1", SW(YELLOW), "image 內容", 200, 300, 180, 240))
p1.append(v("i_list", "img", LEAF(), "檔案清單", 46, 50, 88, 40))
p1.append(v("i_dist", "img", LEAF(GREY), "工具檔案", 46, 110, 88, 40))
p1.append(v("i_tpl", "img", LEAF(GREY), "模板", 46, 170, 88, 40))
p1.append(v("vk", "1", SW(RED), "vendor_kit", VX, VY, 480, 740))
p1.append(v("m_cli", "vk", SW(RED), "命令介面", 20, 50, 200, 140))
p1.append(v("cli_land", "m_cli", LEAF(), "land", 12, 45, 88, 40))
p1.append(v("cli_init", "m_cli", LEAF(), "init", 104, 45, 88, 40))
p1.append(v("cli_verify", "m_cli", LEAF(), "verify", 12, 92, 88, 40))
p1.append(v("cli_diff", "m_cli", LEAF(), "diff", 104, 92, 88, 40))
p1.append(v("m_list", "vk", SW(RED), "清單處理", 20, 210, 200, 170))
p1.append(v("ls_read", "m_list", LEAF(), "讀取", 12, 45, 88, 40))
p1.append(v("ls_check", "m_list", LEAF(), "驗證", 104, 45, 88, 40))
p1.append(v("ls_class", "m_list", LEAF(), "分類", 12, 92, 88, 40))
p1.append(v("ls_t", "m_list", TEXT(11), "工具檔／初始檔／選用檔", 104, 92, 92, 40))
p1.append(v("m_tpl", "vk", SW(RED), "模板", 20, 400, 200, 140))
p1.append(v("tp_render", "m_tpl", LEAF(), "渲染", 12, 45, 88, 40))
p1.append(v("tp_vars", "m_tpl", LEAF(), "變數", 104, 45, 88, 40))
p1.append(v("m_diff", "vk", SW(RED), "差異比對", 20, 560, 200, 140))
p1.append(v("df_cmp", "m_diff", LEAF(), "比對", 12, 45, 88, 40))
p1.append(v("df_patch", "m_diff", LEAF(), "產生差異", 104, 45, 88, 40))
p1.append(v("m_write", "vk", SW(RED), "檔案寫入", 260, 210, 200, 170))
p1.append(v("wr_copy", "m_write", LEAF(), "寫入", 12, 45, 88, 40))
p1.append(v("wr_read", "m_write", LEAF(), "讀回", 104, 45, 88, 40))
p1.append(v("wr_perm", "m_write", LEAF(), "權限設定", 12, 92, 88, 40))
p1.append(v("wr_atomic", "m_write", LEAF(), "整批替換", 104, 92, 88, 40))
p1.append(v("m_stamp", "vk", SW(RED, 16), "印記", 350, 400, 110, 140))
p1.append(v("st_hash", "m_stamp", LEAF(), "指紋計算", 11, 45, 88, 40))
p1.append(v("st_cmp", "m_stamp", LEAF(), "比對", 11, 92, 88, 40))
p1.append(v("m_report", "vk", SW(RED), "回報", 260, 560, 200, 140))
p1.append(v("rp_msg", "m_report", LEAF(), "訊息", 12, 45, 88, 40))
p1.append(v("rp_code", "m_report", LEAF(), "結束狀態", 104, 45, 88, 40))
p1.append(v("proj", "1", SW(YELLOW), "專案目錄", 1000, VY, 200, 740))
p1.append(v("p_stamp", "proj", LEAF(), "印記檔", 56, 241, 88, 40))
p1.append(v("p_base", "proj", LEAF(), ".base/", 56, 292, 88, 40))
p1.append(v("p_user", "proj", LEAF(GREY), "使用者檔案", 56, 343, 88, 40))
p1.append(e("a1", "u_cmd", "m_cli", "命令、參數", (1, 0.5), (0, 0.5)))
p1.append(e("a2", "m_cli", "m_list", "命令參數", (0.5, 1), (0.5, 0)))
p1.append(e("a3", "i_list", "m_list", "檔案清單", (1, 0.5), (0, 0.3)))
p1.append(e("a4", "i_dist", "m_list", "檔案內容", (1, 0.5), (0, 0.6)))
p1.append(e("a5", "i_tpl", "m_list", "模板", (1, 0.5), (0, 0.9)))
p1.append(e("a6", "m_list", "m_write", "工具檔", (1, 0.3), (0, 0.3)))
p1.append(e("a7", "m_list", "m_tpl", "初始檔清單", (0.5, 1), (0.5, 0)))
p1.append(e("a8", "m_tpl", "m_write", "初始檔內容", (0.8, 0), (0.1, 1)))
p1.append(e("a9", "m_write", "m_stamp", "指紋、印記", (0.8, 1), (0.64, 0), both=True))
p1.append(e("a10", "m_write", "p_stamp", "印記檔", (1, 0.3), (0, 0.5), both=True))
p1.append(e("a11", "m_write", "p_base", "工具檔", (1, 0.6), (0, 0.5), both=True))
p1.append(e("a12", "m_write", "p_user", "初始檔", (1, 0.9), (0, 0.5), dashed=True))
p1.append(e("a13", "m_write", "m_diff", "使用者檔案", (0.35, 1), (0.9, 0)))
p1.append(e("a14", "m_tpl", "m_diff", "新版模板", (0.5, 1), (0.5, 0)))
p1.append(e("a15", "m_stamp", "m_report", "檢查結果", (0.5, 1), (0.77, 0)))
p1.append(e("a16", "m_diff", "m_report", "差異", (1, 0.5), (0, 0.5)))
p1.append(e("a17", "m_report", "u_out", "訊息、結束狀態", (0.5, 1), (1, 0.5)))
p1 += legend_arch("p1", 40, 960)

'''
src = src[:start] + new_p1 + src[end:]
R = {
 'p1b.append(e("b10", "ds_engine", "sb", "初始檔案（僅首次）", (1, 0.2), (0.5, 1), dashed=True))': 'p1b.append(e("b10", "ds_engine", "sb", "初始檔", (1, 0.2), (0.5, 1), dashed=True))',
 'p1b.append(e("b9", "ds_engine", "sc", "工具檔案、印記檔", (1, 0.5), (0.5, 1), both=True))': 'p1b.append(e("b9", "ds_engine", "sc", "工具檔、印記檔", (1, 0.5), (0.5, 1), both=True))',
 '"基底", (0.5, 1), (0.5, 0), dashed=True': '"基底 image", (0.5, 1), (0.5, 0), dashed=True',
 '"基底", (1, 0.5), (1, 0.5), dashed=True': '"基底 image", (1, 0.5), (1, 0.5), dashed=True',
 '"進 git；只在第一次建立"': '"進 git；第一次安裝時建立"',
 '"不進 git；每次安裝整批覆蓋"': '"不進 git；每次安裝整批替換"',
 '"安裝容器（跑 base-dist:vX）"': '"安裝容器（base-dist:vX）"',
 '"以使用者身分執行、跑完即刪"': '"以使用者身分執行，跑完即刪"',
 'p1b.append(v("c_tools", "sc", LEAF(GREY), "工具檔案", 12, 50, 88, 40))': 'p1b.append(v("c_tools", "sc", LEAF(), "工具檔", 12, 50, 88, 40))',
 '"流程：啟動器（justfile）— 使用者每次打 just 指令時，背後發生什麼"': '"流程：啟動器（justfile）— 每次執行 just 指令"',
 '"使用者執行 just 指令"': '"執行 just 指令"',
 '"讀 .base-ref，取得要用的版本", 280, 140, 200, 40': '"讀取版本（.base-ref）", 280, 140, 200, 40',
 '"該版本 image\\n已在本機？"': '"image 已下載？"',
 '"從倉庫下載 image"': '"下載 image"',
 '".base/ 已安裝的版本\\n= .base-ref 的版本？"': '".base/ 版本\\n與 .base-ref 一致？"',
 '"啟動安裝工具的容器，執行 land\\n把工具檔案寫進 .base/（第一次會同時建立使用者檔案）"': '"啟動安裝容器，執行 land\\n（安裝工具檔到 .base/）"',
 '"安裝工具內部怎麼做，見第 4 頁"': '"land 內部步驟見第 5 頁"',
 '"執行 verify：\\n.base/ 沒被手動改過？"': '"執行 verify：\\n工具檔完整？"',
 '"停止並報錯：.base/ 被手動改過\\n請使用者重新安裝"': '"中止：.base/ 被改過\\n請重新安裝"',
 '"執行 .base/ 裡對應的指令腳本"': '"執行 .base/ 內對應指令"',
 '"啟動專案的容器"': '"啟動專案容器"',
 '"不同（要重新安裝）"': '"不一致"',
 '"相同", (0.5, 1), (0.5, 0)))\np2.append(e("c24"': '"一致", (0.5, 1), (0.5, 0)))\np2.append(e("c24"',
 '"是", (0.5, 1), (0.5, 0)))\np2.append(e("c31"': '"完整", (0.5, 1), (0.5, 0)))\np2.append(e("c31"',
 '"否", (0, 0.5), (1, 0.5)))\np2.append(e("c30"': '"被改過", (0, 0.5), (1, 0.5)))\np2.append(e("c30"',
 '"否", (0, 0.5), (1, 0.5)))\np2.append(e("c20"': '"還沒", (0, 0.5), (1, 0.5)))\np2.append(e("c20"',
 '"是", (0.5, 1), (0.5, 0)))\np2.append(e("c21"': '"已下載", (0.5, 1), (0.5, 0)))\np2.append(e("c21"',
 '"流程：版本生命週期（升級／回退／追查問題／本機開發）"': '"流程：版本生命週期"',
 '"把 .base-ref 改成新版本（手動改，或機器人自動開 PR）"': '"指定新版本（改 .base-ref；手動或機器人 PR）"',
 '"執行 just：啟動器發現版本不同，自動用新版 image 重新安裝"': '"執行 just → 啟動器用新版 image 重新安裝"',
 '".base/ 內的工具檔案：整批覆寫"': '".base/ 工具檔：整批替換"',
 '"新版有沒有要求\\n使用者檔案配合修改？"': '"執行 diff：\\n新版模板與使用者檔案有差異？"',
 '"執行 diff 列出建議修改\\n使用者自己決定要不要改；工具不碰使用者檔案、不自動 commit"': '"顯示差異，使用者自行決定是否修改\\n（工具不碰使用者檔案）"',
 '"commit .base-ref + 使用者自己的修改"': '"提交變更（.base-ref + 使用者的修改）"',
 '"重點：負責升級的程式在「新版 image」裡，\\n不是專案裡的舊腳本，\\n所以不會發生「舊工具幫自己升級」而失敗的問題。"': '"升級程式在新版 image 裡，不在專案的舊腳本裡，\\n所以不會有「舊工具幫自己升級」的問題。"',
 '"用 git 把 .base-ref 改回舊版本"': '"把 .base-ref 改回舊版本"',
 '"執行 just：用舊版 image 重新安裝\\n（.base/ 不進 git，所以不需要額外的回退紀錄）"': '"執行 just → 用舊版 image 重新安裝\\n（使用者檔案不會自動回復）"',
 '"追查問題（從出事的專案一路追到 base 原始碼）"': '"追查問題"',
 '"看那時的 .base-ref → 知道用的是哪個版本\\n（記版本名稱還是內容指紋，待決）"': '"該 commit 的 .base-ref → 用的版本"',
 'p3.append(v("c24", "bug", PURPLE_LEAF, "看那個版本 image 的附註 → 知道來自 base 的哪個 commit", 20, 210, 380, 50))': 'p3.append(v("c24", "bug", LEAF(), "該版本 image 的附註 → base 的 commit", 20, 210, 380, 50))',
 '"base repo 該 commit 的原始碼"': '"base 該 commit 的原始碼"',
 '"對 .base-ref 的修改紀錄做二分搜尋（git bisect），就能找出是哪次升級出問題"': '"對 .base-ref 做 git bisect 即可找出出問題的升級"',
 '"本機開發模式（自己在改 base 的時候）"': '"本機開發模式（待設計）"',
 '"把來源暫時指到自己電腦上的 base 原始碼\\n這樣改 base 不用每次都發佈 image，就能直接在專案裡測\\n（設計一開始就要預留這個開關）"': '"來源暫時指向本機的 base 原始碼\\n改 base 不必每次發佈 image 就能在專案裡測"',
 '"流程：安裝工具（vendor_kit）— 在容器內執行的三個子命令"': '"流程：安裝工具（vendor_kit）三個子命令"',
 '"verify（檢查）：.base/ 有沒有被手動改過"': '"verify（檢查）"',
 '"讀印記檔（安裝時記下的指紋）"': '"讀取印記"',
 '"重新算 .base/ 每個檔案現在的指紋"': '"重新計算工具檔指紋"',
 '"失敗：列出被改過的檔案"': '"失敗：列出被改的檔案"',
 '"diff（比對）：升級時列出使用者檔案建議怎麼改"': '"diff（比對）"',
 '"用新版模板產生一份\\n「新版應有的樣子」"': '"產生新版範本"',
 '"跟使用者現在的檔案比對"': '"與使用者檔案比對"',
 '"把建議的修改印到畫面上\\n（不直接動使用者的檔案）"': '"顯示差異\\n（不改使用者檔案）"',
}
for k, val in R.items():
    assert src.count(k) == 1, (k, src.count(k))
    src = src.replace(k, val)
old_land_start = src.index('p4.append(v("land", "1", SW(NEUTRAL)')
old_land_end = src.index('# verify')
new_land = r'''p4.append(v("land", "1", SW(NEUTRAL), "land（安裝）", 20, 60, 560, 820))
p4.append(v("l0", "land", ELLIPSE(GREEN), "開始 land", 200, 50, 160, 50))
p4.append(v("l1", "land", LEAF(), "讀取檔案清單", 180, 130, 200, 40))
p4.append(v("l1b", "land", LEAF(), "清空 .base/（整批替換）", 180, 190, 200, 40))
p4.append(v("l2", "land", LEAF(), "取下一個檔案", 180, 250, 200, 40))
p4.append(v("l3", "land", RHOMBUS, "檔案類別？", 190, 320, 180, 80))
p4.append(v("l4", "land", LEAF(), "工具檔：\n寫入 .base/，記指紋", 20, 430, 160, 50))
p4.append(v("l5", "land", RHOMBUS, "初始檔：\n專案裡已存在？", 190, 420, 180, 80))
p4.append(v("l6", "land", LEAF(), "選用檔：\n有指定才建立", 400, 430, 140, 50))
p4.append(v("l7", "land", LEAF(), "用模板建立（init）", 100, 530, 170, 40))
p4.append(v("l8", "land", LEAF(), "保留使用者版本", 290, 530, 170, 40))
p4.append(v("l9", "land", RHOMBUS, "還有檔案？", 190, 600, 180, 80))
p4.append(v("l10", "land", LEAF(), "寫入印記（版本 + 工具檔指紋）", 180, 710, 200, 40))
p4.append(v("l11", "land", ELLIPSE(GREEN), "成功結束", 200, 770, 160, 40))
p4.append(e("le0", "l0", "l1"))
p4.append(e("le1", "l1", "l1b"))
p4.append(e("le1b", "l1b", "l2"))
p4.append(e("le2", "l2", "l3"))
p4.append(e("le3", "l3", "l4", "工具檔", (0, 0.5), (0.5, 0)))
p4.append(e("le4", "l3", "l5", "初始檔", (0.5, 1), (0.5, 0)))
p4.append(e("le5", "l3", "l6", "選用檔", (1, 0.5), (0.5, 0)))
p4.append(e("le6", "l5", "l7", "沒有", (0, 0.5), (0.5, 0)))
p4.append(e("le7", "l5", "l8", "已有", (1, 0.5), (0.5, 0)))
p4.append(e("le8", "l4", "l9", "", (0.5, 1), (0, 0.5)))
p4.append(e("le9", "l7", "l9", "", (0.5, 1), (0.25, 0)))
p4.append(e("le10", "l8", "l9", "", (0.5, 1), (0.75, 0)))
p4.append(e("le11", "l6", "l9", "", (0.5, 1), (1, 0.5)))
p4.append(e("le12", "l9", "l10", "沒有了", (0.5, 1), (0.5, 0)))
p4.append(e("le13", "l10", "l11"))
p4.append('<mxCell id="le14" value="還有" style="' + EDGE + 'exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="land" source="l9" target="l2"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="10" y="640"/><mxPoint x="10" y="270"/></Array></mxGeometry></mxCell>')
'''
src = src[:old_land_start] + new_land + src[old_land_end:]
src = src.replace('page("p4", "5. 流程：安裝工具", p4)', 'page("p4", "5. 流程：安裝工具", p4, h=1150)')
src = src.replace('p4 += legend_flow("p4", 40, 1000)', 'p4 += legend_flow("p4", 40, 1050)')
open("gen6.py", "w", encoding="utf-8").write(src)
print("ok")
