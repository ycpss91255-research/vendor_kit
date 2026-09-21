"""第十一輪 patch 1：共用名詞常數（term-diff 一致）、LOGT 補事件、bootstrap(1)(2)、install(1)(2)。"""
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:90])
    src = src.replace(old, new)

# ---- 檔頭說明 ----
rep("＋ v2.6（2026-09-19 規格審查 16 條必修 + Q22–Q27，最高優先；decisions/interface_spec.md v2 為動詞行為／選項／結束碼／訊息逐字來源），",
    "＋ v2.6（2026-09-19 規格審查 16 條必修 + Q22–Q27，最高優先；decisions/interface_spec.md v2 為動詞行為／選項／結束碼／訊息逐字來源），\n"
    "第十一輪（v2.13 + v2.14 + review_v2r10_findings.md）：主路徑補線（B(1) b1q→b2→b2c、uninstall(1) x2→x2b…x2e）；每頁 resolve／apply 段各一格 engine_start、頁尾一格 log_prune／launcher_exit；\n"
    "藍 = 引擎、白 = 啟動器全檔核對；gen/.stamp 只記引擎 ref、log.sh 帶自描述首行；sync(1′) 6-33 菱形；工具 image pull 失敗紅出口；uninstall(2) 不刪 log/、config.toml 依 v2.13 P6；\n"
    "E(c)(2) config.toml 三方合併；install(2) igq 拆兩菱形；B(2) 逐檔改「情況菱形 → 同意？」兩層（每菱形兩出邊）；共用名詞改常數；備份：.v12（第十一輪前）。")

# ---- 共用名詞常數（放 LOGT 之後）----
rep('''LOGT = [   # v2.12 操作紀錄檔（每頁名詞表共用）
 ("操作紀錄檔／log（v2.12）", ".vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，每次執行一檔（JSON Lines：timestamp、event_name、body、trace_id…）；啟動器先建檔寫 launcher_start、引擎 resolve 前 append engine_start（失敗 → 1 + 6-38）；tty 訊息同句進 body；結束時 prune（30 天／50 檔）；不進 git；事件註冊表 log-events.txt 真本在引擎 image，log.sh 內嵌啟動器事件白名單"),
 ("config.toml（v2.12）", ".vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解），upgrade 三方合併；缺 = 預設"),
 ("6-38", "log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log"),
]''',
'''LOGT = [   # v2.12 操作紀錄檔（每頁名詞表共用）
 ("操作紀錄檔／log（v2.12）", ".vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，每次執行一檔（JSON Lines；不進 git）；事件順序：啟動器 mkdir log/（連同其 .gitignore：*／!.gitignore，缺才建）→ 建檔寫 launcher_start → 每個引擎容器（resolve、apply 各一個）先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔，best-effort）、launcher_exit（每個結束碼都寫）；sync 快路徑由啟動器寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件註冊表 log-events.txt 真本在引擎 image，log.sh 內嵌啟動器事件白名單"),
 ("config.toml（v2.12／v2.13）", ".vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）並存 baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設"),
 ("6-38", "log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log"),
]
LXT = fl("結束前：寫 log_prune、launcher_exit（每個結束碼都寫；引擎容器結束時已寫 engine_exit）")   # v2.14-2 頁尾一格（啟動器 = 白）
EST = "append engine_start 到同一 log 檔（失敗 → 1 + 6-38）"                                                # v2.14-2 每個引擎容器啟動第一格（引擎 = 藍）
# 共用名詞（term-diff：同名各頁同文；與 disc_v1_a／disc_v1_c 同名者抄其文）
RA_T = ("resolve／apply", "動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④")
RAD_T = ("resolve／apply／--dry-run", "resolve 只讀只算（查目標版或讀 metadata、列清單、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（要先拉 image；本機 → 0；CI 為真且需改 tracked 檔 → 1）")
BM_T = ("baseline／metadata", "baseline/<repo>/ = 上次合併的範本副本（歷史狀態，進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）、declined_hash、append 過的行、進度日誌（state=in-progress）；install 只建 baseline/.gitkeep（metadata 到 add 才建）；remove 先讀它（append 行）再刪整個 baseline/<repo>/")
FIP_T = ("flock／指紋／進度日誌", "flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata state=in-progress，其餘用 .vendor_kit/.tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑")
MP_T = ("materialize／印記", "引擎內部步驟：apply 決定套用後才把目標版 /dist/<repo> 複製到暫存目錄 → 原子替換到 cache/<repo>/；印記 = gen/<repo>.stamp，第一行 index digest，之後每檔 sha256（用來驗 cache 有沒有被改）")
GM_T = ("git merge-file --diff3", "git 的三方合併指令；衝突時在檔內留 <<<<<<< vendor_kit:baseline ||||||| ======= >>>>>>> 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為結束狀態 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 > 2 > 0，訊息全列")
MD_T = ("metadata", "baseline/<repo>/.vendor_kit.toml：schema + written_by、source（來源 ref@digest = 最後合併版本）、local_image_id、complete（完成標記）、conflicts、[[file]] dest／state／declined_hash／lines、[progress] 進度日誌")
SYM_T = ("symlink", "指向另一個路徑的捷徑檔；dev 時 cache/<repo>/ 就是指向 <dir>/dist 的 symlink（唯讀性只在容器 mount 上成立）；工具 dist/files/ 裡第一版禁止")
FROZEN_T = ("frozen（CI 為真）", "CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響")
SYNC_T = ("sync", "每次工具 recipe 的自動前置（_sync）：比印記、比 gen/.stamp；只寫 cache/<repo>/、gen/tools.just、gen/<repo>.stamp，不碰薄殼、不寫 gen/.stamp；引擎 ref ≠ gen/.stamp 就退出 1 印 6-1（install／upgrade vendor_kit 不被擋）；無參數走快路徑")
GS_T = ("gen/.stamp", "只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行")
VL_T = ("version.local.toml", "同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].<repo> = \\"path:<dir>\\" 或 vendor_kit = \\"<tag>\\" + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1")
INIT_T = ("初始檔", "工具 init.toml 列出、add 時建到專案的檔（例 Dockerfile）；歸使用者，進 git；已存在就不納管；upgrade 逐檔問；五態記在 metadata")
BDN_T = ("B／D／N", "B = baseline（上次合併的範本副本）、D = 磁碟上使用者的檔、N = 新版範本（讀自暫存 /dist/<repo>，不是 cache）；upgrade 逐檔判斷只對 state=managed 且無待解衝突")
BOOT_T = ("bootstrap.sh", "release 附的 POSIX sh 薄層，內嵌所屬引擎的完整 ref（ghcr.io/<org>/vendor_kit:vN@sha256:<index digest>）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local <tar>")
GT_T = ("gen/tools.just／mod?", "不進 git；每個工具 just/<ns>.just 一行 mod? <ns> '../cache/<repo>/just/<ns>.just'（帶問號 = 檔不在也不掛）；add／remove／upgrade／sync 重生；裡面沒有 recipe")
E2B_T = ("6-2b", "第一行已改但新引擎拉取／重產失敗，或第二次第一行又變 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」（.tmp.upgrade 進度日誌保留）")
E33_T = ("6-33（未完成交易）", "唯讀動詞偵測到 .tmp.<verb>.<id>.toml：「偵測到未完成的 <verb>（<id>）。請先重跑：just vendor_kit <verb> <targets>」；sync／update 印後結束 1、不恢復；help 印後仍 0；可寫動詞不印此句而是先恢復")''')

# ---- T5 ----
rep(''' ("bootstrap.sh", "release 附的 POSIX sh 薄層：先建 log/bootstrap/ 並寫 launcher_start → 檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止：清半成品但保留 log/）→ 對每個 -t <repo>[@<tag>] 呼叫 add；再跑 = install"),''',
''' BOOT_T,
 ("bootstrap.sh 流程", "先建 log/bootstrap/ 並寫 launcher_start → 檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止：清半成品但保留 log/）→ 對每個 -t <repo>[@<tag>] 呼叫 add；再跑 = install"),''')
rep(''' ("薄殼 .vendor_kit/", ".gitignore、entry.just、vendor.just、log.sh、ci/check.sh 五檔（進 git；vendor_kit 自己的檔，人不改；log.sh 由 base 移植成 POSIX，hash 記 gen/.stamp）＋ version.toml、config.toml、baseline/（進 git）＋ cache/、gen/、log/、version.local.toml、.tmp.*（不進 git）"),''',
''' ("薄殼 .vendor_kit/", ".gitignore、entry.just、vendor.just、log.sh、ci/check.sh 五檔（進 git；vendor_kit 自己的檔，人不改；每檔都帶自描述首行，log.sh 亦同，v2.14）＋ version.toml、config.toml、baseline/（進 git）＋ cache/、gen/、log/、version.local.toml、.tmp.*（不進 git）"),''')
rep(''' ("gen/.stamp", "不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit"),
 ("暫存目錄／原子替換", "先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔（log/ 除外；只對第一次 install 成立）"),''',
''' GS_T, GT_T,
 ("進度日誌（.tmp.install；v2.13 P5）", "install 在第一個寫入前建 .vendor_kit/.tmp.install.<id>.toml（<id> = trace_id），最後一步刪；第一次 install 也建 —— 它同時是「不留半成品」的清除清單；未完成 → 下次可寫動詞先恢復"),
 ("暫存目錄／原子替換", "先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 依日誌丟棄暫存、移除已寫的檔，專案不留任何檔（log/ 除外；只對第一次 install 成立）"),''')
rep(''' ("resolve／apply", "會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁"),
 ("baseline／metadata", "baseline/<repo>/ = 上次合併的範本副本（進 git）；metadata = 其中的 .vendor_kit.toml，記來源版本、完成標記、append 過的行；install 只建 baseline/.gitkeep（git 不追蹤空目錄），metadata 到 add 才建"),''',
''' RA_T, BM_T,''')
rep('N5 = "已定（v2.4 Q17／Q18、v2.5 §8、v2.6）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；',
    'N5 = "已定（v2.4 Q17／Q18、v2.5 §8、v2.6、v2.13 P5）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；第一次 install 也建 .tmp.install 日誌（= 清除清單）；')

# ---- P5 bootstrap(1)：a6p pull 失敗紅出口、a8i inspect 失敗紅出口 ----
rep('''b.box("a7", G, 8, IMG, "ghcr.io/…/vendor_kit:vN\\n（引擎 image；多架構 amd64+arm64）", 180)
b.box("a8l", L, 9, v2(W12), "否：docker load <tar>", 230, ax="l")''',
'''b.box("a7", G, 8, IMG, "ghcr.io/…/vendor_kit:vN\\n（引擎 image；多架構 amd64+arm64）", 180)
b.box("a6px", E, 9, v2(R12), fl("失敗／逾時 → 1：印 6-24／6-31（不退回內嵌）"), 240, ax="l")   # v2.14-5
b.box("a8l", L, 9, v2(W12), "否：docker load <tar>", 230, ax="l")''')
rep('''b.box("a8i", L, 11, v2(W12), fl("docker image inspect 取 image ID（tag 形 = 值即本機 image tag，不讀 .digest）"), 230, ax="l")''',
'''b.box("a8ix", U, 11, v2(R12), fl("失敗 → 1：本機無此 image（tag 形；docker load 後才有）"), 220)   # v2.14-5
b.box("a8i", L, 11, v2(W12), fl("docker image inspect 取 image ID（tag 形 = 值即本機 image tag，不讀 .digest）"), 230, ax="l")''')
rep('''b.D("ae11", "a8i", "a9"); b.D("ae11b", "a6p", "a9", "", 0.3, 0.87)   # 直下一條線（x=621），不與 ae6y（x=545）交叉（r8）''',
'''b.H("ae8ix", "a8i", "a8ix", "失敗"); b.D("ae11", "a8i", "a9"); b.D("ae11b", "a6p", "a9", "", 0.3, 0.87)   # 直下一條線（x=621），不與 ae6y（x=545）交叉（r8）
b.D("ae6px", "a6p", "a6px", "失敗", 0.75, 0.25, dy=8)   # 引擎 pull 失敗紅出口（v2.14-5）''')

# ---- P5ccc bootstrap(2)：a10re 接回主路徑；頁尾 launcher_exit ----
rep('''b.box("a13", U, 9, G12, "全部成功 → 0：印摘要與要 git add 的清單", 220)''',
'''b.box("a13l", L, 9, v2(W12), LXT, 300)
b.box("a13", U, 9, G12, "全部成功 → 0：印摘要與要 git add 的清單", 220)''')
rep('''b.D("ae19", "a10", "a10r"); b.H("ae19e", "a10r", "a10re"); b.D("ae20", "a10r", "a10d"); b.H("ae20g", "a10g", "a10d", "拉 /dist")''',
'''b.D("ae19", "a10", "a10r"); b.H("ae19e", "a10r", "a10re"); b.D("ae20", "a10re", "a10d"); b.H("ae20g", "a10g", "a10d", "拉 /dist")   # resolve 格接回主路徑（r10 dangling）''')
rep('''b.LL("ae22y", "a10q", "a10", "是：下一個 -t", busx=330); b.DL("ae24", "a10q", "a13", "否")   # 迴圈菱形（r8）''',
'''b.LL("ae22y", "a10q", "a10", "是：下一個 -t", busx=330); b.D("ae24", "a10q", "a13l", "否", al=True); b.H("ae24l", "a13l", "a13")   # 迴圈菱形（r8）；頁尾 launcher_exit（v2.14-2）''')

# ---- P5c install(1) ----
rep('''b = F.band("bI", "5a′ install（bootstrap.sh 代打或自己打）：launcher_start → engine_start → 產薄殼五檔＋config.toml；再跑 = 引擎重寫薄殼（比對首行自描述 hash）= 冪等修復；第一次不建日誌、修復型建 .tmp.install（v2.8 §2）；禁止巢狀（Q20）", v2=True)''',
'''b = F.band("bI", "5a′ install（bootstrap.sh 代打或自己打）：launcher_start → engine_start → 產薄殼五檔＋config.toml；再跑 = 引擎重寫薄殼（比對首行自描述 hash）= 冪等修復；第一次與修復型都建 .tmp.install 日誌（v2.13 P5）；禁止巢狀（Q20）", v2=True)''')
rep('''b.box("i4n", P, 5, NOTE, fl("第一次 install（薄殼不存在）：不建進度日誌，任一步失敗 → 丟棄暫存、移除已寫的檔 → 1（不留半成品，v2.2 C）；修復型：建 .tmp.install.<id>.toml 日誌（第一個寫入前），失敗 → 1 列已完成／未完成，收尾後刪（v2.8 §2）"), 360)''',
'''b.box("i4n", P, 5, NOTE, fl("第一次 install：失敗 → 依日誌移除已寫的檔 → 1（不留半成品；log/ 保留，v2.13 P4／P5）；修復型：失敗 → 1 列已完成／未完成，下次可寫動詞先恢復；日誌在「install（2）」頁最後一步刪"), 360)''')
rep('''b.box("i4_3b", E, 8, v2(SUB), fl("產 log.sh 到暫存（由 base log.sh 移植的 POSIX 版；內嵌啟動器事件白名單）"), 400)''',
'''b.box("i4_3b", E, 8, v2(SUB), fl("產 log.sh 到暫存（首行自描述；移植自 base 的 log.sh，POSIX；內嵌啟動器事件白名單）"), 400)   # v2.14-1''')
rep('''b.box("i4_5", E, 10, v2(SUB), fl("產 config.toml 到暫存（含註解與預設 schema=1、[log] keep=50、days=30；已有 → 不產、不動，v2.12）"), 400)''',
'''b.box("i4_5", E, 10, v2(SUB), fl("產 config.toml 與其 baseline 副本到暫存（含註解與預設 schema=1、[log] keep=50、days=30；已有 → 不產、不動，v2.12／v2.13 P10）"), 400)''')
rep('''b.box("i4qn", P, 12, v2(NOTE), fl("自描述（Q17）：薄殼每檔首行 # vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 LF 正規化 hash>；引擎重算 + 對 image 內模板二次比對；不用 gen/.stamp（不進 git，重新 clone 後也不存在）"), 360)
b.box("i4l", E, 13, v2(W12), fl("是（修復型）：建進度日誌 .tmp.install.<id>.toml（第一個寫入前）"), 240, ax="l")
b.box("i4lf", P, 13, v2(F12), "＋.vendor_kit/.tmp.install.<id>.toml（進度日誌，不進 git；修復型才有，收尾後刪；第一次 install 不建，失敗整包丟棄）", 360)
b.box("i4b", E, 14, v2(SUB), fl("薄殼五檔（＋第一次的 config.toml）逐檔原子替換（暫存 → 正式位置）"), 400)
b.files("i4f", P, 14, "＋.vendor_kit/ 薄殼五檔＋config.toml（進 git）", [".gitignore", "entry.just", "vendor.just", "log.sh", "ci/check.sh", "config.toml（第一次才建）"], 360, cols=2)''',
'''b.box("i4qn", P, 12, v2(NOTE), fl("自描述（Q17）：薄殼每檔（含 log.sh）首行 # vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 LF 正規化 hash>；引擎重算 + 對 image 內模板二次比對；不用 gen/.stamp（不進 git）"), 360)
b.box("i4l", E, 13, v2(SUB), fl("建進度日誌 .tmp.install.<id>.toml（第一個寫入前；第一次也建 = 清除清單，v2.13 P5）"), 240, ax="l")
b.box("i4lf", P, 13, v2(F12), "＋.vendor_kit/.tmp.install.<id>.toml（進度日誌，不進 git；第一次 = 不留半成品的清除清單；收尾後刪）", 360)
b.box("i4b", E, 14, v2(SUB), fl("薄殼五檔（＋第一次的 config.toml 與其 baseline 副本）逐檔原子替換（暫存 → 正式位置）"), 400)
b.files("i4f", P, 14, "＋.vendor_kit/ 薄殼五檔＋config.toml（進 git）", [".gitignore", "entry.just", "vendor.just", "log.sh", "ci/check.sh", "config.toml（第一次才建）", "baseline/vendor_kit/config.toml（副本）"], 360, cols=2)''')
rep('''b.box("i4d", E, 16, v2(SUB), "寫 gen/.stamp（引擎 ref＋log.sh hash）", 400)''',
'''b.box("i4d", E, 16, v2(SUB), "寫 gen/.stamp（只記引擎 ref）", 400)   # v2.14-1''')
rep('''b.box("i4en", E, 11, v2(W12), "否：第一次 = 全新建", 120, ax="l")''',
'''b.box("i4en", E, 11, v2(SUB), "否：第一次 = 全新建", 120, ax="l")''')
rep('''b.D("ie6", "i4q", "i4l", "是", al=True); b.UL("ie6n", "i4en", "i4b", "", busx=560, row=11)   # 第一次 = 全新建 → 走左側匯流排直接建檔，不跨「寫」線（r8／r10）''',
'''b.D("ie6", "i4q", "i4l", "是", al=True); b.UL("ie6n", "i4en", "i4l", "", busx=560, row=11)   # 第一次 = 全新建 → 走左側匯流排也建日誌（v2.13 P5），不跨「寫」線（r8／r10）''')

# ---- P5cc install(2)：藍白、igq 拆兩菱形、頁尾 launcher_exit ----
rep('''b = F.band("bI2", "5a″ install 收尾（承「install（1）」頁：薄殼、version.toml、gen/.stamp、baseline/.gitkeep 已寫）：根 justfile（無 → 新建 import 行 + default recipe；有 → 問後加一行）→ 根 .dockerignore（無 → 建四行；有 → 問後 append；v2.12 加 log/）", pad=40, v2=True)''',
'''b = F.band("bI2", "5a″ install 收尾（承「install（1）」頁：薄殼、version.toml、gen/.stamp、baseline/.gitkeep 已寫）：根 justfile（無 → 新建 import 行 + default recipe；有 → 問後加一行）→ 根 .dockerignore（無 → 建四行；有 → 已含跳過／問後 append；v2.12 加 log/）→ 刪日誌 → 0", pad=40, v2=True)''')
rep('''b.box("i7", E, 2, W12, fl("無：建 justfile（四行，逐字見右）"), 120, ax="r")''', '''b.box("i7", E, 2, SUB, fl("無：建 justfile（四行，逐字見右）"), 120, ax="r")''')
rep('''b.box("i11", E, 4, W12, "是：append 那一行", 120, ax="r")''', '''b.box("i11", E, 4, SUB, "是：append 那一行", 120, ax="r")''')
rep('''b.box("im", E, 5, W12, fl("印 justfile 結果（建了／加了一行／跳過／已含不再加／拒絕不動）"), 360, ax=-60)''', '''b.box("im", E, 5, SUB, fl("印 justfile 結果（建了／加了一行／跳過／已含不再加／拒絕不動）"), 360, ax=-60)''')
rep('''b.box("ign", E, 6, v2(W12), fl("無：建 .dockerignore（四行，逐字見右）"), 120, ax=280)   # 中車道（720..840）；右端留給 igz
b.box("ignf", P, 6, v2(PRE), "＋.dockerignore（新建，四行）：\\n.vendor_kit/cache/\\n.vendor_kit/gen/\\n.vendor_kit/log/\\n.vendor_kit/.tmp.*", 360)
b.box("idlx", U, 7, v2(W12), fl("否：刪進度日誌 .tmp.install.<id>.toml（修復型才有；最後一步）"), 220)
b.box("igq", E, 7, v2(D12), "有 → 問「要在 .dockerignore 加這四行嗎」同意？（-y 免問；已含則跳過）", 250, ax="l")
b.box("idlz", E, 7, v2(W12), fl("刪進度日誌（修復型才有；最後一步）"), 120, ax=280)   # 檔名見主路徑 idl；短文字讓框保持 120 寬，與 igz 距 40
b.box("igx", U, 8, v2(G12), fl("0：不寫 .dockerignore、印指示（四行；含 justfile 結果）"), 220)
b.box("igz", E, 7, v2(G12), fl("0：印建立了什麼（含 justfile 結果）"), 120, ax="r")
b.box("igy", E, 8, v2(W12), fl("是：append 四行"), 250, ax="l")
b.box("igyf", P, 8, v2(PRE), ".dockerignore（尾端＋四行；Q22 補、v2.12）：\\n.vendor_kit/cache/\\n.vendor_kit/gen/\\n.vendor_kit/log/\\n.vendor_kit/.tmp.*", 360)
b.box("igm", E, 9, v2(SUB), fl("插入的行記在 baseline/.vendor_kit.toml（lines）"), 250, ax="l")
b.box("igmf", P, 9, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 的 append 行；進 git）", 360)
b.box("idl", E, 10, v2(SUB), fl("刪進度日誌 .tmp.install.<id>.toml（修復型才有；最後一步）"), 250, ax="l")
b.box("idlf", P, 10, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（修復型才有）", 360)
b.box("iz", U, 11, G12, "0：印建立／修改了什麼（含加的行）", 220)''',
'''b.box("ign", E, 6, v2(SUB), fl("無：建 .dockerignore（四行，逐字見右）"), 120, ax=280)   # 中車道（720..840）；右端留給 igz
b.box("ignf", P, 6, v2(PRE), "＋.dockerignore（新建，四行）：\\n.vendor_kit/cache/\\n.vendor_kit/gen/\\n.vendor_kit/log/\\n.vendor_kit/.tmp.*", 360)
b.box("igq0", E, 7, v2(D12), "有 → 已含這四行？", 250, ax="l")   # r10：「已含跳過」與「問同意」拆兩菱形
b.box("idlz", E, 7, v2(SUB), fl("刪進度日誌 .tmp.install.<id>.toml（最後一步）"), 120, ax=280)   # 短文字讓框保持 120 寬，與 igz 距 40
b.box("igz", E, 7, v2(G12), fl("0：印結果（建了四行／已含不再加；含 justfile 結果）"), 120, ax="r")
b.box("idlx", U, 8, v2(SUB), fl("否：刪進度日誌 .tmp.install.<id>.toml（最後一步）"), 220)
b.box("igq", E, 8, v2(D12), "否 → 問「要在 .dockerignore 加這四行嗎」同意？（-y 免問）", 250, ax="l")
b.box("igx", U, 9, v2(G12), fl("0：不寫 .dockerignore、印指示（四行；含 justfile 結果）"), 220)
b.box("igy", E, 9, v2(SUB), fl("是：append 四行"), 250, ax="l")
b.box("igyf", P, 9, v2(PRE), ".dockerignore（尾端＋四行；Q22 補、v2.12）：\\n.vendor_kit/cache/\\n.vendor_kit/gen/\\n.vendor_kit/log/\\n.vendor_kit/.tmp.*", 360)
b.box("igm", E, 10, v2(SUB), fl("插入的行記在 baseline/.vendor_kit.toml（lines）"), 250, ax="l")
b.box("igmf", P, 10, v2(F12), "baseline/.vendor_kit.toml（記 .dockerignore 的 append 行；進 git）", 360)
b.box("idl", E, 11, v2(SUB), fl("刪進度日誌 .tmp.install.<id>.toml（最後一步）"), 250, ax="l")
b.box("idlf", P, 11, v2(F12), "－.vendor_kit/.tmp.install.<id>.toml（第一次與修復型都有）", 360)
b.box("ixl", L, 12, v2(W12), LXT, 140)
b.box("iz", U, 12, G12, "0：印建立／修改了什麼（含加的行）", 220)''')
rep('''b.H("ie20", "ig", "ign", "無"); b.H("ie20f", "ign", "ignf", "寫"); b.D("ie21", "ig", "igq", "有", al=True)
b.D("ie20z", "ign", "idlz", al=True); b.H("ie20zz", "idlz", "igz")   # 刪日誌獨立格（r8）
b.H("ie22", "igq", "idlx", "否"); b.D("ie22x", "idlx", "igx", al=True); b.D("ie23", "igq", "igy", "是", al=True); b.H("ie23f", "igy", "igyf", "寫")
b.D("ie23m", "igy", "igm", al=True); b.H("ie23mf", "igm", "igmf", "寫")
b.D("ie24", "igm", "idl", al=True); b.H("ie24f", "idl", "idlf", "刪"); b.DL("ie25", "idl", "iz", "")''',
'''b.H("ie20", "ig", "ign", "無"); b.H("ie20f", "ign", "ignf", "寫"); b.D("ie21", "ig", "igq0", "有", al=True)
b.D("ie20z", "ign", "idlz", al=True); b.H("ie20zz", "idlz", "igz")   # 刪日誌獨立格（r8）
b.H("ie21y", "igq0", "idlz", "是"); b.D("ie21n", "igq0", "igq", "否", al=True)   # 已含 → 跳過（r10）
b.H("ie22", "igq", "idlx", "否"); b.D("ie22x", "idlx", "igx", al=True); b.D("ie23", "igq", "igy", "是", al=True); b.H("ie23f", "igy", "igyf", "寫")
b.D("ie23m", "igy", "igm", al=True); b.H("ie23mf", "igm", "igmf", "寫")
b.D("ie24", "igm", "idl", al=True); b.H("ie24f", "idl", "idlf", "刪"); b.D("ie25", "idl", "ixl"); b.H("ie25l", "ixl", "iz")   # 頁尾 launcher_exit（v2.14-2）''')
open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("patch 1 ok")
