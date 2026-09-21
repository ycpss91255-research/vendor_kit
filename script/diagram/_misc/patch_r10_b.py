"""第十輪 patch（v2.11 + v2.12 + review_v2r9_findings.md 本檔範圍）：只改頁內容，helper 段不動。"""
import re
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:90])
    src = src.replace(old, new)

# ---- header note ----
rep("、.v9（第八輪前）、.v10（第九輪前）。",
    "、.v9（第八輪前）、.v10（第九輪前）、.v11（第十輪前）。\n"
    "第十輪（v2.11 + v2.12 + review_v2r9_findings.md）：upgrade vendor_kit 改回建進度日誌 .tmp.upgrade.<id>.toml（E(a) s2d／s2df、E(c)(1) s12j、E(c)(2) s13d 由新引擎刪；撤回 v2.10-4）；\n"
    "操作紀錄檔：啟動器起點後「建 log 檔並寫 launcher_start」一格（bootstrap(1) a0l、install(1) i0l、add(1) c0l、sync(1) n0l、B(1) b0l、E(c)(1) s10l、dev d0l、remove(1) m0l、uninstall(1) x0l），引擎 append engine_start 一格（i1e／c1e／b1e／d1e／m1e／x1e）或入口文字帶過；\n"
    "sync(1) 快路徑寫 sync_fast_path／launcher_exit（nql）；install(2) .dockerignore 四行（＋.vendor_kit/log/）；install(1) 建 config.toml（i4_5）；名詞表加操作紀錄檔／config.toml／6-38；\n"
    "--local 名詞：bootstrap tag 形 digest = 既有 version.toml 或內嵌引擎 ref、add --local 只收存在的 .tar；bootstrap(2) 本次 add 失敗即中止（a10x）；E(a) se6vr／E(c)(1) se11vr 補「否」線；s12hz 改續跑入口樣式；E(c)(1) @tag／frozen 拆開；dev vendor_kit v9 橙；uninstall(2) x5d 拆 gen/／baseline/ 兩格。")

# =====================================================================
# A1. 名詞表 --local（T5：bootstrap／install 四頁共用；T5B：add 三頁共用）
# =====================================================================
rep(''' ("--local <image tag 或 tar>", "離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 消歧；前置檢查（git repo／just 版本）兩形都先做；version.toml 仍寫正式 ref（tar 形 digest 由 .digest 取得；tag 形不讀 .digest，digest 用 version.toml／metadata 既有值），version.local.toml 記 tag + image ID"),''',
    ''' ("--local <image tag 或 tar>（只有 bootstrap.sh 收 tag 形）", "離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 + 6-37；前置檢查兩形都先做；version.toml 仍寫正式 ref@digest：tar 形由 .digest 旁檔取；tag 形不讀 .digest —— 專案已有 version.toml → 用該行，第一次接入 → 用 bootstrap.sh 內嵌引擎 ref（v2.10 §2）；version.local.toml 記 tag + image ID；add --local 只收存在的 .tar（v2.10 §3）"),''')
rep(''' ("--local／tar／.digest（Q26）", "值含 / 或以 .tar 結尾 → tar 路徑（docker save 存的工具 image 檔）先 docker load；其餘 → 本機 image tag；每個 tar 附同名 .digest 旁檔 = 正式 index digest，寫進 version.toml；metadata 記 image ID ↔ digest 對照供離線驗證；只涵蓋 install／add --local"),''',
    ''' ("--local <tar>／.digest（Q26、v2.10 §3）", "add --local 只收存在的 .tar（docker save 存的工具 image 檔；值不是存在的 .tar → 1 + 6-24 類提示，橙；不提供 --digest；tag 形只有 bootstrap.sh 有意義）：先 docker load，讀同名 .digest 旁檔 = 正式 index digest 寫進 version.toml（旁檔缺 → 1）；metadata 記 image ID ↔ digest 對照供離線驗證"),''')

# =====================================================================
# A2. bootstrap(2)：本次 add 失敗 → 立即中止；移除「任一 add 失敗？」彙總
# =====================================================================
rep('b = F.band("bA2", "5a′ bootstrap.sh 後半（承「bootstrap.sh（1）」頁：install 成功）：--local → 寫 version.local.toml → 對每個 -t <repo>[@<tag>] 呼叫 add（resolve → docker → apply；一個失敗即中止）→ 彙總結束碼；不自刪", v2=True)',
    'b = F.band("bA2", "5a′ bootstrap.sh 後半（承「bootstrap.sh（1）」頁：install 成功）：--local → 寫 version.local.toml → 對每個 -t <repo>[@<tag>] 呼叫 add（resolve → docker → apply）→ 本次 add 失敗 → 立即中止 1（列出已完成部分，後續 -t 不執行）；全部成功 → 0；不自刪", v2=True)')
rep('b.box("a9e2", L, 0, ENTRY, "來自「bootstrap.sh（1）」頁：install 成功（薄殼、version.toml、gen/.stamp 已寫）", 300)',
    'b.box("a9e2", L, 0, ENTRY, "來自「bootstrap.sh（1）」頁：install 成功（薄殼、version.toml、gen/.stamp 已寫；已寫 launcher_start）", 300)')
rep('''b.box("a10q", L, 7, v2(D12), "還有下一個 -t？", 200)
b.box("a12", U, 8, v2(R12), fl("是 → 1：明列已完成／未完成（多工具彙總：1 > 2 > 0）"), 220)
b.box("a11", L, 8, D12, "任一 add 失敗？", 200)
b.box("a13", U, 9, G12, "0：印摘要與要 git add 的清單", 220)''',
'''b.box("a10x", L, 7, v2(D12), "本次 add 失敗？", 200)
b.box("a12", E, 7, v2(R12), fl("是 → 1：立即中止（印該 add 的錯誤；列出已完成／未完成，後續 -t 不執行）"), 240, ax="l")
b.box("a10q", L, 8, v2(D12), "還有下一個 -t？", 200)
b.box("a13", U, 9, G12, "全部成功 → 0：印摘要與要 git add 的清單", 220)''')
rep('''b.D("ae22", "a10a", "a10q", al=True); b.LL("ae22y", "a10q", "a10", "是：下一個 -t", busx=330); b.D("ae22n", "a10q", "a11", "否", al=True)   # 迴圈菱形（r8）
b.H("ae23", "a11", "a12", "是"); b.DL("ae24", "a11", "a13", "否")''',
'''b.D("ae22", "a10a", "a10x", al=True); b.H("ae23", "a10x", "a12", "是"); b.D("ae22q", "a10x", "a10q", "否", al=True)   # 一個失敗即中止（r9）
b.LL("ae22y", "a10q", "a10", "是：下一個 -t", busx=330); b.DL("ae24", "a10q", "a13", "否")   # 迴圈菱形（r8）''')
rep('b.box("a9z", L, 14, LBL, "否 ↓ 續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add → 彙總", 460, 24, minh=24)',
    'b.box("a9z", L, 15, LBL, "否 ↓ 續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add（一個失敗即中止）", 460, 24, minh=24)')

# =====================================================================
# A3 + B. E(a)(b)：s2lv「否」線補上；建日誌改記三欄、不由舊引擎刪；加 launcher_start 格（移除 s2g 後列數不變）
# =====================================================================
rep('''b.box("s0", U, 0, v2(G12), "(a) upgrade 不帶 repo（含 vendor_kit 自身）", 220)
b.box("s1", L, 0, v2(W12), "docker run 舊引擎 resolve upgrade（全部）", 280)
b.box("s2a", E, 0, v2(SUB), fl("resolve：先完整預檢（含 dev 中工具 → 1 提示 undev）"), 360)
b.box("s2n", U, 1, v2(G12), "否 → 只升工具（走「B. 手動路徑（1）」頁，對每個工具；Q27 彙總）", 220)
b.box("s2q", E, 1, v2(D12), "引擎有新版？", 240, ax="l")
b.box("s2b", E, 2, v2(SUB), "是：apply（舊引擎）：flock 專案目錄", 360)
b.box("s2c", E, 3, v2(SUB), "重驗指紋（不同 → 1「請重跑」，橙）", 360)
b.box("s2d", E, 4, v2(SUB), "建進度日誌（第一個寫入前）", 360)
b.box("s2e", E, 5, v2(SUB), fl("只改 version.toml 第一行 → 新引擎 ref（其餘工具等重跑原指令）"), 360)
b.box("s2f", P, 5, F12, "version.toml 第一行 = 新引擎 ref", 280)
b.box("s2g", E, 6, v2(SUB), "刪進度日誌（最後一步）", 360)
b.box("s2h", L, 7, v2(W12), fl("apply 後再 grep version.toml 第一行（local 覆寫 vendor_kit= 優先；v2.6 §5，不從 stdout 讀）"), 280)
b.box("s2hx", U, 8, v2(R12), fl("否 → 1：apply 未改第一行（印 apply 的錯誤）"), 220)
b.box("s2h2", L, 8, v2(D12), fl("第一行變了且 == 計畫的 engine？"), 240)
b.box("s2ln", L, 9, v2(D12), "是 → docker image inspect：本機有？", 220, ax=50)
b.box("s2lp", L, 10, v2(W12), "無：docker pull 新引擎", 80, ax="r")
b.box("s2gi", G, 10, IMG, "vendor_kit:vY\\n（新引擎）", 200)
b.box("s2lv", L, 11, v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？"), 220, ax=50)
b.box("s2lx", E, 11, v2(R12), fl("拉不到／image ID 不符 → 1 + 6-2b（引擎已鎖定為 <vY>，薄殼尚未重產）"), 240, ax="l")
b.box("s4", U, 12, v2(G12), fl("→ 接「E(c) upgrade vendor_kit」頁的「docker run 該引擎」格（同一次指令內；第二次第一行又變 → 1 不再重跑）"), 220)
b.box("s2r", L, 12, v2(W12), "docker run 新引擎 upgrade vendor_kit", 320)
b.box("s5", U, 13, v2(G12), "(b) 別人 pull 後（第一行已變）打任何 just", 220)
b.box("s6a", L, 13, v2(W12), "啟動器：grep version.toml 第一行", 280)
b.box("s8", U, 14, v2(O12), fl("否 → 1：印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」→ 使用者打 (c)（「E(c)」頁）"), 220)
b.box("s6q", L, 14, v2(D12), "gen/.stamp 的引擎 ref == 第一行？", 240)
b.box("s6y", L, 15, G12, "是 → 正常跑（「sync（1）」頁）", 240)
b.H("se1", "s0", "s1"); b.H("se2", "s1", "s2a"); b.D("se2q", "s2a", "s2q", al=True); b.H("se2n", "s2q", "s2n", "否")
b.D("se3", "s2q", "s2b", "是", al=True); b.D("se3c", "s2b", "s2c"); b.D("se3d", "s2c", "s2d"); b.D("se3e", "s2d", "s2e"); b.H("se4", "s2e", "s2f", "寫")
b.D("se3g", "s2e", "s2g"); b.D("se5", "s2g", "s2h", "", 0.2, 0.5); b.D("se5h", "s2h", "s2h2", al=True); b.H("se5x", "s2h2", "s2hx", "否")
b.D("se5l", "s2h2", "s2ln", "是", al=True)
b.RD("se6p", "s2ln", "s2lp", "無"); b.H("se6", "s2gi", "s2lp", "拉"); b.D("se6y", "s2ln", "s2lv", "有", al=True)
b.D("se6pv", "s2lp", "s2lv", "", 0.25, 0.5); b.D("se6px", "s2lp", "s2lx", "失敗", 0.75, 0.25, dy=8); b.H("se6vx", "s2lv", "s2lx", "是")   # 失敗線進紅橢圓頂端，不 T 接（r8）; b.D("se6vr", "s2lv", "s2r", "否", al=True)
b.H("se7", "s2r", "s4")''',
'''b.box("s0", U, 0, v2(G12), "(a) upgrade 不帶 repo（含 vendor_kit 自身）", 220)
b.box("s0l", L, 0, v2(W12), fl("建 log 檔並寫 launcher_start（失敗 → 1 + 6-38，零寫入）"), 280)
b.box("s1", L, 1, v2(W12), "docker run 舊引擎 resolve upgrade（全部）", 280)
b.box("s2a", E, 1, v2(SUB), fl("resolve（已 append engine_start）：先完整預檢（含 dev 中工具 → 1 提示 undev）"), 360)
b.box("s2n", U, 2, v2(G12), "否 → 只升工具（走「B. 手動路徑（1）」頁，對每個工具；Q27 彙總）", 220)
b.box("s2q", E, 2, v2(D12), "引擎有新版？", 240, ax="l")
b.box("s2b", E, 3, v2(SUB), "是：apply（舊引擎）：flock 專案目錄", 360)
b.box("s2c", E, 4, v2(SUB), "重驗指紋（不同 → 1「請重跑」，橙）", 360)
b.box("s2d", E, 5, v2(SUB), fl("建進度日誌 .tmp.upgrade.<id>.toml（記舊引擎 ref、目標引擎 ref、計畫 image ID；改第一行之前，v2.11）"), 360)
b.box("s2df", P, 5, v2(F12), "＋.vendor_kit/.tmp.upgrade.<id>.toml（進度日誌，不進 git；新引擎重產薄殼完成後才刪）", 280)
b.box("s2e", E, 6, v2(SUB), fl("只改 version.toml 第一行 → 新引擎 ref（其餘工具等重跑原指令；日誌留給新引擎）"), 360)
b.box("s2f", P, 6, F12, "version.toml 第一行 = 新引擎 ref", 280)
b.box("s2h", L, 7, v2(W12), fl("apply 後再 grep version.toml 第一行（local 覆寫 vendor_kit= 優先；v2.6 §5，不從 stdout 讀）"), 280)
b.box("s2hx", U, 8, v2(R12), fl("否 → 1：apply 未改第一行（印 apply 的錯誤）"), 220)
b.box("s2h2", L, 8, v2(D12), fl("第一行變了且 == 計畫的 engine？"), 240)
b.box("s2ln", L, 9, v2(D12), "是 → docker image inspect：本機有？", 220, ax=50)
b.box("s2lp", L, 10, v2(W12), "無：docker pull 新引擎", 80, ax="r")
b.box("s2gi", G, 10, IMG, "vendor_kit:vY\\n（新引擎）", 200)
b.box("s2lv", L, 11, v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？"), 220, ax=50)
b.box("s2lx", E, 11, v2(R12), fl("拉不到／image ID 不符 → 1 + 6-2b（引擎已鎖定為 <vY>，薄殼尚未重產；日誌保留）"), 240, ax="l")
b.box("s4", U, 12, v2(G12), fl("→ 接「E(c) upgrade vendor_kit」頁的「docker run 該引擎」格（同一次指令內；第二次第一行又變 → 1 不再重跑）"), 220)
b.box("s2r", L, 12, v2(W12), "否：docker run 新引擎 upgrade vendor_kit", 320)
b.box("s5", U, 13, v2(G12), "(b) 別人 pull 後（第一行已變）打任何 just", 220)
b.box("s6a", L, 13, v2(W12), "啟動器：grep version.toml 第一行（已寫 launcher_start）", 280)
b.box("s8", U, 14, v2(O12), fl("否 → 1：印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」→ 使用者打 (c)（「E(c)」頁）"), 220)
b.box("s6q", L, 14, v2(D12), "gen/.stamp 的引擎 ref == 第一行？", 240)
b.box("s6y", L, 15, G12, "是 → 正常跑（「sync（1）」頁）", 240)
b.H("se1", "s0", "s0l"); b.D("se1l", "s0l", "s1"); b.H("se2", "s1", "s2a"); b.D("se2q", "s2a", "s2q", al=True); b.H("se2n", "s2q", "s2n", "否")
b.D("se3", "s2q", "s2b", "是", al=True); b.D("se3c", "s2b", "s2c"); b.D("se3d", "s2c", "s2d"); b.H("se3df", "s2d", "s2df", "寫"); b.D("se3e", "s2d", "s2e"); b.H("se4", "s2e", "s2f", "寫")
b.D("se5", "s2e", "s2h", "", 0.2, 0.5); b.D("se5h", "s2h", "s2h2", al=True); b.H("se5x", "s2h2", "s2hx", "否")
b.D("se5l", "s2h2", "s2ln", "是", al=True)
b.RD("se6p", "s2ln", "s2lp", "無"); b.H("se6", "s2gi", "s2lp", "拉"); b.D("se6y", "s2ln", "s2lv", "有", al=True)
b.D("se6pv", "s2lp", "s2lv", "", 0.25, 0.5); b.D("se6px", "s2lp", "s2lx", "失敗", 0.75, 0.25, dy=8); b.H("se6vx", "s2lv", "s2lx", "是")   # 失敗線進紅橢圓頂端，不 T 接（r8）
b.D("se6vr", "s2lv", "s2r", "否", al=True)   # 成功入口（r9）
b.H("se7", "s2r", "s4")''')
rep('b = F.band("uE", "E. vendor_kit 自身升級（v2.3 §2 統一版、v2.5 §7、v2.6 §5）：(a) upgrade 不帶 repo 當次換新引擎並重產薄殼；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit 見「E(c)」頁；install 修復也走同樣比對", v2=True)',
    'b = F.band("uE", "E. vendor_kit 自身升級（v2.3 §2 統一版、v2.5 §7、v2.6 §5、v2.11）：(a) upgrade 不帶 repo 當次換新引擎並重產薄殼（舊引擎建 .tmp.upgrade 日誌、改第一行；新引擎重產後刪日誌）；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit 見「E(c)」頁", v2=True)')
# T7E 名詞表：不建日誌 → 統一建日誌
rep(''' ("resolve／apply", "同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run；拿鎖、重驗；不建日誌）"),
 ("upgrade vendor_kit 不建進度日誌（v2.10）", "進度日誌規則的明文例外：唯一寫入是 version.toml 第一行的單檔原子替換；未完成狀態由「第一行 ≠ gen/.stamp 第一行」辨識（sync → 6-1；upgrade vendor_kit 重跑即恢復；第一行已改但重產失敗 → 6-2b）"),''',
    ''' ("resolve／apply", "同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run；拿鎖、重驗、建日誌）"),
 ("進度日誌 .tmp.upgrade.<id>.toml（v2.11）", "upgrade vendor_kit 也建進度日誌（統一規則，無例外）：改 version.toml 第一行之前建，記舊引擎 ref、目標引擎 ref、計畫 image ID、done／pending；新引擎重產薄殼完成後由新引擎刪；重跑遇既有日誌 = 續作；未完成 → 可寫動詞先恢復（= 重跑 upgrade vendor_kit）、sync／update 印 6-33 結束 1、help 印 6-33 仍 0"),''')
rep('N7E = "已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5）：自身升級統一版 —— (a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行',
    'N7E = "已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5、v2.11）：自身升級統一版 —— (a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建 .tmp.upgrade 日誌）只改第一行')

# =====================================================================
# A4 + B + C. E(c)(1)：s11v「否」線；s12hz 續跑入口樣式；@tag／frozen 拆開；建日誌；launcher_start 格
# =====================================================================
rep('b = F.band("uE2", "E(c)（1）upgrade vendor_kit[@<tag>]（單段救援）：grep 第一行 → inspect → 無才 pull → 拿鎖、重驗（不建日誌）→ 薄殼 == 上次產物？（否 → 1 零寫入）→ @舊版無法無損讀 → 3 → 查 registry → 有新版 → 改第一行 → 新引擎再跑；否則見「E(c)（2）」頁", v2=True)',
    'b = F.band("uE2", "E(c)（1）upgrade vendor_kit[@<tag>]（單段救援）：寫 launcher_start → grep 第一行 → inspect → 無才 pull → 拿鎖、重驗 → 薄殼 == 上次產物？（否 → 1 零寫入）→ @舊版無法無損讀 → 3 → frozen 不查／@<tag> 為目標／查 registry → 目標 ≠ 現 ref → 建日誌 → 改第一行 → 新引擎再跑；否則見「E(c)（2）」頁", v2=True)')
rep('''b.box("s10", U, 0, v2(G12), fl("(c) just vendor_kit upgrade vendor_kit[@<tag>]（(b) 提示後由使用者打；也可直接打）"), 220)
b.box("s11a", L, 0, v2(W12), "grep version.toml 第一行取引擎 ref（local 覆寫 vendor_kit= 優先；跳過 gen/.stamp 比對）", 280)
b.box("s11n", L, 1, v2(D12), "docker image inspect：本機有？", 220, ax=20)
b.box("s11p", L, 2, v2(W12), "無：docker pull 該引擎", 80, ax="r")
b.box("s11g", G, 2, IMG, "vendor_kit:vN\\n（第一行指到的引擎）", 200)
b.box("s11v", L, 3, v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？"), 220, ax=20)
b.box("s11x", E, 3, v2(R12), fl("拉不到／image ID 不符（同 tag 重 build）→ 1：印原因"), 240, ax="l")
b.box("s10a", U, 4, ENTRY, fl("來自「E. 自身升級 (a)(b)」頁：(a) 啟動器已用新引擎 ref（不再走 grep／inspect）"), 220)
b.box("s11r", L, 4, v2(W12), "否：docker run 該引擎 upgrade vendor_kit", 320)
b.box("s12a", E, 4, v2(SUB), "flock 專案目錄（60 秒）", 360)
b.box("s12b", E, 5, v2(SUB), "重驗指紋", 220, ax="l")
b.box("s12bx", E, 5, v2(O12), "不同 → 1「請重跑」", 130, ax="r")
b.box("s12sx", U, 6, v2(O12), fl("否 → 1：偵測到薄殼被修改，列差異不動（零寫入；git checkout 還原後再跑）"), 220)
b.box("s12s", E, 6, v2(D12), "薄殼 == 上次產物？（首行自描述 hash、未被改）", 260, ax="l")
b.box("s12sn", P, 6, v2(NOTE), fl("「上次產物」= 薄殼首行自描述的 sha256 與其餘內容相符（Q17）；同一判斷 install 頁也用；在拿鎖重驗之後、任何寫入（含改第一行）之前檢查，不符 → 1 列差異、零寫入（v2.8 §3）"), 360)
b.box("s12dx", U, 7, v2(O12), fl("是 → 3：印 6-10「目標引擎無法無損讀取現有檔；未修改任何檔；要退回請 git revert」（零寫入）"), 220)
b.box("s12d", E, 7, v2(D12), fl("是 → @<tag> 為舊版且無法無損讀現有檔（P／schema）？"), 260, ax="l")
b.box("s12t", E, 8, v2(D12), fl("否 → @<tag> 指定或 CI 為真（frozen）？"), 260, ax="l")
b.box("s12tn", E, 8, v2(W12), fl("是：不查 registry"), 100, ax="r")
b.box("s12u", E, 9, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版"), 260, ax="l")
b.box("s12v", E, 10, v2(D12), "有新版？", 200, ax="l")
b.box("s12vz", E, 10, LBL, "否／不查 → 續「E(c)（2）」頁：薄殼比對與重產", 110, ax="r", minh=40)
b.box("s12hz", U, 11, v2(G12), fl("→ 用新引擎從本頁「docker run 該引擎」格再跑一次（同一次指令內；第二次第一行又變 → 1 印 6-2b）"), 220)
b.box("s12h", L, 11, v2(W12), fl("啟動器：apply 前後 grep 第一行 → 變了 → 用新引擎再跑 upgrade vendor_kit（接手邏輯同「E(a)(b)」頁）"), 300)
b.box("s12w", E, 11, v2(SUB), fl("是：改 version.toml 第一行 = 新引擎 ref（單檔原子替換；其餘不動、不建日誌）"), 260, ax="l")
b.box("s12wf", P, 11, F12, "version.toml 第一行 = 新引擎 ref（進 git）", 360)
b.H("se11", "s10", "s11a"); b.D("se11q", "s11a", "s11n", al=True)
b.RD("se11p", "s11n", "s11p", "無"); b.H("se11g", "s11g", "s11p", "拉"); b.D("se11v", "s11n", "s11v", "有", al=True)
b.D("se11pv", "s11p", "s11v", "", 0.25, 0.5); b.D("se11px", "s11p", "s11x", "失敗", 0.75, 0.25, dy=8); b.H("se11vx", "s11v", "s11x", "是")   # 失敗線進紅橢圓頂端，不 T 接（r8）; b.D("se11vr", "s11v", "s11r", "否", al=True)
b.H("se11e", "s10a", "s11r")
b.H("se12", "s11r", "s12a"); b.D("se12b", "s12a", "s12b", al=True); b.H("se12x", "s12b", "s12bx"); b.D("se12s", "s12b", "s12s", al=True); b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12d", "s12s", "s12d", "是", al=True)
b.H("se12dx", "s12d", "s12dx", "是"); b.D("se12t", "s12d", "s12t", "否", al=True); b.H("se12tn", "s12t", "s12tn", "是"); b.D("se12u", "s12t", "s12u", "否", al=True)
b.D("se12v", "s12u", "s12v", al=True); b.H("se12vn", "s12v", "s12vz", "否"); b.D("se12tv", "s12tn", "s12vz", al=True)
b.D("se12w", "s12v", "s12w", "是", al=True); b.H("se12wf", "s12w", "s12wf", "寫"); b.H("se12wh", "s12w", "s12h"); b.H("se12hz", "s12h", "s12hz")''',
'''b.box("s10", U, 0, v2(G12), fl("(c) just vendor_kit upgrade vendor_kit[@<tag>]（(b) 提示後由使用者打；也可直接打）"), 220)
b.box("s10l", L, 0, v2(W12), fl("建 log 檔並寫 launcher_start（失敗 → 1 + 6-38，零寫入）"), 280)
b.box("s11a", L, 1, v2(W12), "grep version.toml 第一行取引擎 ref（local 覆寫 vendor_kit= 優先；跳過 gen/.stamp 比對）", 280)
b.box("s11n", L, 2, v2(D12), "docker image inspect：本機有？", 220, ax=20)
b.box("s11p", L, 3, v2(W12), "無：docker pull 該引擎", 80, ax="r")
b.box("s11g", G, 3, IMG, "vendor_kit:vN\\n（第一行指到的引擎）", 200)
b.box("s11v", L, 4, v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？"), 220, ax=20)
b.box("s11x", E, 4, v2(R12), fl("拉不到／image ID 不符（同 tag 重 build）→ 1：印原因"), 240, ax="l")
b.box("s10a", U, 5, ENTRY, fl("來自「E. 自身升級 (a)(b)」頁：(a) 啟動器已用新引擎 ref（不再走 grep／inspect；已寫 launcher_start）"), 220)
b.box("s11r", L, 5, v2(W12), "否：docker run 該引擎 upgrade vendor_kit", 320)
b.box("s12a", E, 5, v2(SUB), "flock 專案目錄（60 秒；已 append engine_start）", 360)
b.box("s12b", E, 6, v2(SUB), "重驗指紋", 220, ax="l")
b.box("s12bx", E, 6, v2(O12), "不同 → 1「請重跑」", 130, ax="r")
b.box("s12sx", U, 7, v2(O12), fl("否 → 1：薄殼被改過，列差異不動（零寫入）"), 220)
b.box("s12s", E, 7, v2(D12), "薄殼 == 上次產物？（首行自描述 hash、未被改）", 260, ax="l")
b.box("s12sn", P, 7, v2(NOTE), fl("「上次產物」= 薄殼首行自描述的 sha256 與其餘內容相符（Q17）；同一判斷 install 頁也用；在拿鎖重驗之後、任何寫入之前檢查，不符 → 1 列差異、零寫入（git checkout 還原後再跑；v2.8 §3）"), 360)
b.box("s12dx", U, 8, v2(O12), fl("是 → 3：印 6-10（目標引擎無法無損讀現有檔；零寫入，要退回請 git revert）"), 220)
b.box("s12d", E, 8, v2(D12), fl("是 → @<tag> 為舊版且無法無損讀現有檔（P／schema）？"), 260, ax="l")
b.box("s12f", E, 9, v2(D12), fl("否 → CI 為真（frozen）？"), 260, ax="l")
b.box("s12fz", E, 9, LBL, "是：不查 registry、不改第一行 → 續「E(c)（2）」頁", 100, ax="r", minh=40)
b.box("s12t", E, 10, v2(D12), fl("否 → 指定 @<tag>？"), 260, ax="l")
b.box("s12tt", E, 10, v2(W12), fl("是：目標 = @<tag>（不查 registry）"), 100, ax="r")
b.box("s12u", E, 11, v2(SUB), fl("否：查 registry（GHCR）取引擎最新正式版 = 目標"), 260, ax="l")
b.box("s12v", E, 12, v2(D12), "目標引擎 ref ≠ 現 ref？", 240, ax="l")
b.box("s12vz", E, 12, LBL, "否 → 續「E(c)（2）」頁：薄殼比對與重產", 110, ax="r", minh=40)
b.box("s12j", E, 13, v2(SUB), fl("是：建進度日誌 .tmp.upgrade.<id>.toml（記舊引擎 ref、目標引擎 ref、計畫 image ID；改第一行之前，v2.11）"), 260, ax="l")
b.box("s12jf", P, 13, v2(F12), "＋.vendor_kit/.tmp.upgrade.<id>.toml（進度日誌，不進 git；新引擎重產薄殼完成後才刪）", 360)
b.box("s12hz", U, 14, v2(ENTRY), fl("續跑入口：用新引擎回到本頁「docker run 該引擎」格再跑一次（同一次指令內；第二次第一行又變 → 1 印 6-2b）"), 220)
b.box("s12h", L, 14, v2(W12), fl("啟動器：apply 前後 grep 第一行 → 變了 → 用新引擎再跑 upgrade vendor_kit（接手邏輯同「E(a)(b)」頁）"), 300)
b.box("s12w", E, 14, v2(SUB), fl("改 version.toml 第一行 = 新引擎 ref（單檔原子替換；其餘不動）"), 260, ax="l")
b.box("s12wf", P, 14, F12, "version.toml 第一行 = 新引擎 ref（進 git）", 360)
b.H("se11", "s10", "s10l"); b.D("se11l", "s10l", "s11a"); b.D("se11q", "s11a", "s11n", al=True)
b.RD("se11p", "s11n", "s11p", "無"); b.H("se11g", "s11g", "s11p", "拉"); b.D("se11v", "s11n", "s11v", "有", al=True)
b.D("se11pv", "s11p", "s11v", "", 0.25, 0.5); b.D("se11px", "s11p", "s11x", "失敗", 0.75, 0.25, dy=8); b.H("se11vx", "s11v", "s11x", "是")   # 失敗線進紅橢圓頂端，不 T 接（r8）
b.D("se11vr", "s11v", "s11r", "否", al=True)   # 成功入口（r9）
b.H("se11e", "s10a", "s11r")
b.H("se12", "s11r", "s12a"); b.D("se12b", "s12a", "s12b", al=True); b.H("se12x", "s12b", "s12bx"); b.D("se12s", "s12b", "s12s", al=True); b.H("se12sx", "s12s", "s12sx", "否"); b.D("se12d", "s12s", "s12d", "是", al=True)
b.H("se12dx", "s12d", "s12dx", "是"); b.D("se12f", "s12d", "s12f", "否", al=True); b.H("se12fz", "s12f", "s12fz", "是"); b.D("se12t", "s12f", "s12t", "否", al=True)
b.H("se12tt", "s12t", "s12tt", "是"); b.D("se12u", "s12t", "s12u", "否", al=True)   # @<tag>／frozen 拆開（r9）
b.D("se12v", "s12u", "s12v", al=True); b.D("se12tv", "s12tt", "s12v"); b.H("se12vn", "s12v", "s12vz", "否")
b.D("se12j", "s12v", "s12j", "是", al=True); b.H("se12jf", "s12j", "s12jf", "寫"); b.D("se12w", "s12j", "s12w", al=True); b.H("se12wf", "s12w", "s12wf", "寫"); b.H("se12wh", "s12w", "s12h"); b.H("se12hz", "s12h", "s12hz")''')

# =====================================================================
# B. E(c)(2)：重產完成後由新引擎刪日誌
# =====================================================================
rep('b = F.band("uE3", "E(c)（2）薄殼比對與重產（承「E(c)（1）」頁：無新版或不查，第一行未變；薄殼 == 上次產物已在 (1) 驗過）：已是本引擎產物？→ 是 → 0 無變更；否 → 重產薄殼四檔 + gen/.stamp + tools.just（不建日誌；未完成由第一行 ≠ gen/.stamp 辨識）→ 1", v2=True)',
    'b = F.band("uE3", "E(c)（2）薄殼比對與重產（承「E(c)（1）」頁：無新版或不查，第一行未變；薄殼 == 上次產物已在 (1) 驗過）：已是本引擎產物？→ 是 → 0 無變更；否 → 重產薄殼四檔 + gen/.stamp + tools.just → 刪 .tmp.upgrade 日誌（有的話；v2.11）→ 1", v2=True)')
rep('b.box("s12z0", E, 0, ENTRY, "來自「E(c)（1）」頁：無新版／不查（第一行未變；已拿鎖、重驗，且薄殼 == 上次產物）", 360)',
    'b.box("s12z0", E, 0, ENTRY, "來自「E(c)（1）」頁：無新版／不查（第一行未變；已拿鎖、重驗，且薄殼 == 上次產物；已寫 launcher_start）", 360)')
rep('''b.box("s13c", E, 4, v2(SUB), "重生 gen/tools.just（用本引擎的規則；mod? 行）", 360)
b.box("s13cf", P, 4, F12, "gen/tools.just（不進 git；mod? 行）", 360)
b.box("s14", U, 4, v2(O12), fl("成功 → 1：印「已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」"), 220)
b.box("s13x", U, 5, v2(O12), fl("是 → 1 + 6-2b：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」"), 220)
b.box("s13q", E, 5, v2(D12), fl("失敗 → 第一行已改（或又變）？"), 240, ax="r")
b.box("s13xn", E, 6, v2(O12), fl("否 → 1：印原因（第一行未變、引擎未鎖定新版；排除錯誤後再跑）"), 240, ax="r")
b.D("se13", "s12z0", "s12e", al=True)
b.H("se15z", "s12e", "s12z", "是"); b.D("se15l", "s12e", "s13", "否", al=True)
b.H("se16", "s13", "s13f", "寫")
b.D("se17", "s13", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
b.H("se18d", "s13c", "s14", "成功"); b.D("se18x", "s13c", "s13q", "失敗", 0.75, 0.5, al=True)   # 6-2b 只給第一行已改（v2.10-5）
b.H("se19", "s13q", "s13x", "是"); b.D("se19n", "s13q", "s13xn", "否", al=True)''',
'''b.box("s13c", E, 4, v2(SUB), "重生 gen/tools.just（用本引擎的規則；mod? 行）", 360)
b.box("s13cf", P, 4, F12, "gen/tools.just（不進 git；mod? 行）", 360)
b.box("s13d", E, 5, v2(SUB), fl("刪進度日誌 .tmp.upgrade.<id>.toml（有的話；最後一步，由新引擎刪，v2.11）"), 220, ax="l")
b.box("s13df", P, 5, v2(F12), "－.vendor_kit/.tmp.upgrade.<id>.toml（E(a)／E(c)(1) 建的進度日誌）", 360)
b.box("s14", U, 5, v2(O12), fl("成功 → 1：印「已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」"), 220)
b.box("s13x", U, 6, v2(O12), fl("是 → 1 + 6-2b：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（日誌保留）"), 220)
b.box("s13q", E, 6, v2(D12), fl("失敗 → 第一行已改（或又變）？"), 240, ax="r")
b.box("s13xn", E, 7, v2(O12), fl("否 → 1：印原因（第一行未變、引擎未鎖定新版；排除錯誤後再跑）"), 240, ax="r")
b.D("se13", "s12z0", "s12e", al=True)
b.H("se15z", "s12e", "s12z", "是"); b.D("se15l", "s12e", "s13", "否", al=True)
b.H("se16", "s13", "s13f", "寫")
b.D("se17", "s13", "s13b"); b.H("se18", "s13b", "s13bf", "寫"); b.D("se18b", "s13b", "s13c"); b.H("se18c", "s13c", "s13cf", "寫")
b.D("se18cd", "s13c", "s13d", "成功", 0.25, 0.5, al=True); b.H("se18df", "s13d", "s13df", "刪"); b.H("se18d", "s13d", "s14")
b.D("se18x", "s13c", "s13q", "失敗", 0.75, 0.5, al=True)   # 6-2b 只給第一行已改（v2.10-5）
b.H("se19", "s13q", "s13x", "是"); b.D("se19n", "s13q", "s13xn", "否", al=True)''')

# =====================================================================
# A5. dev vendor_kit：v9 改橙
# =====================================================================
rep('b.box("v9", U, 9, v2(G12), "→ 打 upgrade vendor_kit（「E(c) upgrade vendor_kit」頁）", 220)',
    'b.box("v9", U, 9, v2(O12), "需人動作：打 just vendor_kit upgrade vendor_kit（「E(c)」頁）", 220)')

# =====================================================================
# A6. uninstall(2)：x5d 拆 gen/ 與 baseline/ 兩格；壓縮菱形文字（頁高）
# =====================================================================
rep('''b.box("x5d", E, 6, v2(SUB), fl("刪 gen/ 與 baseline/ 內剩下的自產檔（hash 相符者；v2.8 §1）"), 400)
b.files("x5df", P, 6, "－gen/ 兩檔（不進 git）、baseline/ 根檔（進 git）", ["gen/.stamp", "gen/tools.just", "baseline/.gitkeep", "baseline/.vendor_kit.toml"], 360, cw=(140, 198))
b.box("x5dd", E, 7, v2(SUB), fl("刪已空的子目錄 baseline/（gen/、cache/、ci/ 亦同；rmdir，不 rm -rf）"), 400)
b.box("x6", E, 8, D12, "根 justfile 有我們寫的那一行（完全相同）？", 260, ax="r")
b.box("x5r", P, 8, v2(RULE), fl("初始檔留著（永不刪，印清單）；使用者的 .gitignore／.dockerignore 只動我們 append 過且你同意的那幾行（v2.1 A、Q22 補）"), 360)
b.box("x8", E, 9, W12, fl("無／否：印指示（請自行移除 import 那行）"), 100, ax=0)
b.box("x7", E, 9, v2(D12), "有 → 問「要刪這一行嗎」同意？（-y 免問）", 260, ax="r")
b.box("x7y", E, 10, W12, "是：只刪那一行", 140, ax=200)
b.box("x7f", P, 10, F12, "justfile（少一行：import '.vendor_kit/entry.just'）", 360)
b.box("x9a", E, 11, v2(D12), "根 .dockerignore 存在？", 260, ax=120)
b.box("x9b", E, 12, v2(D12), fl("有 → 逐行比對：仍有與紀錄原文相同的行？（CRLF／LF 等價）"), 260, ax=120)
b.box("x9r", P, 12, v2(RULE), fl("append 行逐行比對（§4.3、v2.9 §5）：對紀錄的每一行 —— 仍與原文相同 → 刪該行；不同／缺 → 跳過並 warn；不是全有／全無；零命中 → 不動"), 360)
b.box("x9q", E, 13, v2(D12), fl("有 → 問「要刪這幾行嗎」同意？（-y 免問）"), 260, ax=120)
b.box("x9z", E, 14, v2(W12), fl("無／否：不動 .dockerignore"), 110, ax="l")
b.box("x9y", E, 14, v2(W12), fl("是：逐行只刪仍相同的行；不同／缺的行跳過 warn"), 230, ax="r")
b.box("x9f", P, 14, v2(F12), ".dockerignore（只少仍相同的那幾行；其餘不動）", 360)
b.box("x5z", E, 15, v2(SUB), "刪進度日誌（最後一步；根 justfile 那行之後）= 交易完成", 400)
b.box("x5n", U, 16, v2(G12), "否 → 0：保留目錄與保護清單內的檔並回報；印摘要", 220)
b.box("x5q", E, 16, v2(D12), ".vendor_kit/ 已空？", 200, ax="l")
b.box("x5y", U, 17, v2(G12), "0：印摘要", 220)
b.box("x5t", E, 17, v2(SUB), "是：刪空目錄（rmdir；不 rm -rf）", 400)
b.D("xe7", "x4e", "x4l"); b.H("xe7f", "x4l", "x4lf", "寫"); b.D("xe8", "x4l", "x4")
b.H("xe9", "x4", "x4x", "失敗"); b.D("xe10", "x4", "x5a"); b.H("xe10f", "x5a", "x5af", "刪"); b.D("xe10b", "x5a", "x5b"); b.H("xe10bf", "x5b", "x5bf", "刪")
b.D("xe10c", "x5b", "x5c"); b.H("xe10cf", "x5c", "x5cf", "刪"); b.D("xe10d", "x5c", "x5d"); b.H("xe10df", "x5d", "x5df", "刪"); b.D("xe10e", "x5d", "x5dd")''',
'''b.box("x5d", E, 6, v2(SUB), fl("刪 gen/ 內剩下的自產檔（hash 相符者）"), 400)
b.files("x5df", P, 6, "－gen/ 兩檔（不進 git）", ["gen/.stamp", "gen/tools.just"], 360, cols=2)
b.box("x5e", E, 7, v2(SUB), fl("刪 baseline/ 內剩下的自產檔（hash 相符者；v2.8 §1）"), 400)
b.files("x5ef", P, 7, "－baseline/ 根檔（進 git）", ["baseline/.gitkeep", "baseline/.vendor_kit.toml"], 360, cols=2)
b.box("x5dd", E, 8, v2(SUB), fl("刪已空的子目錄 baseline/（gen/、cache/、log/、ci/ 亦同；rmdir，不 rm -rf）"), 400)
b.box("x6", E, 9, D12, "根 justfile 有我們那一行（完全相同）？", 260, ax="r")
b.box("x5r", P, 9, v2(RULE), fl("初始檔留著（永不刪，印清單）；使用者的 .gitignore／.dockerignore 只動我們 append 過且你同意的那幾行（v2.1 A、Q22 補）"), 360)
b.box("x8", E, 10, W12, fl("無／否：印指示（請自行移除 import 那行）"), 100, ax=0)
b.box("x7", E, 10, v2(D12), "有 → 問「要刪這一行嗎」？（-y 免問）", 260, ax="r")
b.box("x7y", E, 11, W12, "是：只刪那一行", 140, ax=200)
b.box("x7f", P, 11, F12, "justfile（少一行：import '.vendor_kit/entry.just'）", 360)
b.box("x9a", E, 12, v2(D12), "根 .dockerignore 存在？", 260, ax=120)
b.box("x9b", E, 13, v2(D12), fl("有 → 仍有與紀錄原文相同的行？"), 260, ax=120)
b.box("x9r", P, 13, v2(RULE), fl("append 行逐行比對（§4.3、v2.9 §5；CRLF／LF 等價）：紀錄的每一行仍與原文相同 → 刪該行；不同／缺 → 跳過並 warn；不是全有／全無；零命中 → 不動"), 360)
b.box("x9q", E, 14, v2(D12), fl("有 → 問「要刪這幾行嗎」？（-y 免問）"), 260, ax=120)
b.box("x9z", E, 15, v2(W12), fl("無／否：不動 .dockerignore"), 110, ax="l")
b.box("x9y", E, 15, v2(W12), fl("是：逐行只刪仍相同的行；不同／缺的行跳過 warn"), 230, ax="r")
b.box("x9f", P, 15, v2(F12), ".dockerignore（只少仍相同的那幾行；其餘不動）", 360)
b.box("x5z", E, 16, v2(SUB), "刪進度日誌（最後一步；根 justfile 那行之後）= 交易完成", 400)
b.box("x5n", U, 17, v2(G12), "否 → 0：保留目錄與保護清單內的檔；印摘要", 220)
b.box("x5q", E, 17, v2(D12), ".vendor_kit/ 已空？", 200, ax="l")
b.box("x5y", U, 18, v2(G12), "0：印摘要", 220)
b.box("x5t", E, 18, v2(SUB), "是：刪空目錄（rmdir；不 rm -rf）", 400)
b.D("xe7", "x4e", "x4l"); b.H("xe7f", "x4l", "x4lf", "寫"); b.D("xe8", "x4l", "x4")
b.H("xe9", "x4", "x4x", "失敗"); b.D("xe10", "x4", "x5a"); b.H("xe10f", "x5a", "x5af", "刪"); b.D("xe10b", "x5a", "x5b"); b.H("xe10bf", "x5b", "x5bf", "刪")
b.D("xe10c", "x5b", "x5c"); b.H("xe10cf", "x5c", "x5cf", "刪"); b.D("xe10d", "x5c", "x5d"); b.H("xe10df", "x5d", "x5df", "刪")
b.D("xe10dd", "x5d", "x5e"); b.H("xe10ef", "x5e", "x5ef", "刪"); b.D("xe10e", "x5e", "x5dd")   # gen/／baseline/ 拆兩格（r9）''')
rep('b.box("x4e", E, 0, ENTRY, "來自「uninstall（1）」頁：apply 檢查通過（非 dry-run）", 300)',
    'b.box("x4e", E, 0, ENTRY, "來自「uninstall（1）」頁：apply 檢查通過（非 dry-run；已寫 launcher_start）", 300)')
rep('b = F.band("vD2", "uninstall（2）寫入段（承「uninstall（1）」頁：已拿鎖、重驗、非 dry-run）：建日誌 → 逐工具 remove（保護模式）→ 只刪 hash 相符的自產檔（含 baseline/ 根檔，v2.8 §1）→ justfile 那行、.dockerignore 行問後逐行刪（只刪仍相同的）→ 刪日誌 → 空才 rmdir", v2=True)',
    'b = F.band("vD2", "uninstall（2）寫入段（承「uninstall（1）」頁：已拿鎖、重驗、非 dry-run）：建日誌 → 逐工具 remove（保護模式）→ 只刪 hash 相符的自產檔（gen/、baseline/ 根檔各一步，v2.8 §1）→ justfile 那行、.dockerignore 四行問後逐行刪（只刪仍相同的）→ 刪日誌 → 空才 rmdir", v2=True)')

open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("patch A/B ok")
