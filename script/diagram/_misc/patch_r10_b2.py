"""第十輪 patch 第二段：v2.12 操作紀錄檔（launcher_start／engine_start 格、sync 快路徑 log、.dockerignore 四行、config.toml、名詞表三條）＋ 第一段檢查後的修正。"""
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:90])
    src = src.replace(old, new)

LOG_BOX = 'fl("建 log 檔並寫 launcher_start（失敗 → 1 + 6-38，零寫入）")'
ENG_BOX = '"append engine_start 到同一 log 檔（失敗 → 1 + 6-38，不進 resolve）"'

# ---- 第一段修正：band 標題一行、名詞鍵不超寬、x5ef 欄寬、a9z 列號 ----
rep('"5a′ bootstrap.sh 後半（承「bootstrap.sh（1）」頁：install 成功）：--local → 寫 version.local.toml → 對每個 -t <repo>[@<tag>] 呼叫 add（resolve → docker → apply）→ 本次 add 失敗 → 立即中止 1（列出已完成部分，後續 -t 不執行）；全部成功 → 0；不自刪"',
    '"5a′ bootstrap.sh 後半（承「bootstrap.sh（1）」頁）：--local → 寫 version.local.toml → 對每個 -t 呼叫 add（resolve → docker → apply）→ 本次 add 失敗 → 立即中止 1（後續 -t 不執行）；全部成功 → 0；不自刪"')
rep('"E(c)（1）upgrade vendor_kit[@<tag>]（單段救援）：寫 launcher_start → grep 第一行 → inspect → 無才 pull → 拿鎖、重驗 → 薄殼 == 上次產物？（否 → 1 零寫入）→ @舊版無法無損讀 → 3 → frozen 不查／@<tag> 為目標／查 registry → 目標 ≠ 現 ref → 建日誌 → 改第一行 → 新引擎再跑；否則見「E(c)（2）」頁"',
    '"E(c)（1）upgrade vendor_kit[@<tag>]（單段救援）：launcher_start → grep 第一行 → inspect → pull → 拿鎖、重驗 → 薄殼 == 上次產物？→ @舊版無法無損讀 → 3 → frozen 不查／@<tag>／查 registry → 目標 ≠ 現 ref → 建日誌 → 改第一行 → 新引擎再跑；否則見「E(c)（2）」頁"')
rep('"uninstall（2）寫入段（承「uninstall（1）」頁：已拿鎖、重驗、非 dry-run）：建日誌 → 逐工具 remove（保護模式）→ 只刪 hash 相符的自產檔（gen/、baseline/ 根檔各一步，v2.8 §1）→ justfile 那行、.dockerignore 四行問後逐行刪（只刪仍相同的）→ 刪日誌 → 空才 rmdir"',
    '"uninstall（2）寫入段（承「uninstall（1）」頁）：建日誌 → 逐工具 remove（保護模式）→ 只刪 hash 相符的自產檔（gen/、baseline/ 根檔各一步，v2.8 §1）→ justfile 那行、.dockerignore 四行問後逐行刪 → 刪日誌 → 空才 rmdir"')
rep(' ("進度日誌 .tmp.upgrade.<id>.toml（v2.11）", "upgrade vendor_kit 也建進度日誌（統一規則，無例外）：改 version.toml 第一行之前建，',
    ' ("進度日誌（upgrade vendor_kit；v2.11）", "upgrade vendor_kit 也建進度日誌 .tmp.upgrade.<id>.toml（統一規則，無例外）：改 version.toml 第一行之前建，')
rep('b.files("x5ef", P, 7, "－baseline/ 根檔（進 git）", ["baseline/.gitkeep", "baseline/.vendor_kit.toml"], 360, cols=2)',
    'b.files("x5ef", P, 7, "－baseline/ 根檔（進 git）", ["baseline/.gitkeep", "baseline/.vendor_kit.toml"], 360, cw=(140, 198))')
rep('b.box("a9z", L, 15, LBL,', 'b.box("a9z", L, 14, LBL,')

# ---- E(c)(1)：頁高（菱形加寬／文字精簡）----
rep('b.box("s10", U, 0, v2(G12), fl("(c) just vendor_kit upgrade vendor_kit[@<tag>]（(b) 提示後由使用者打；也可直接打）"), 220)',
    'b.box("s10", U, 0, v2(G12), fl("(c) upgrade vendor_kit[@<tag>]（(b) 提示後打；也可直接打）"), 220)')
rep('b.box("s11n", L, 2, v2(D12), "docker image inspect：本機有？", 220, ax=20)', 'b.box("s11n", L, 2, v2(D12), "docker image inspect：本機有？", 280, ax=20)')
rep('b.box("s11v", L, 4, v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？"), 220, ax=20)', 'b.box("s11v", L, 4, v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？"), 280, ax=20)')
rep('b.box("s10a", U, 5, ENTRY, fl("來自「E. 自身升級 (a)(b)」頁：(a) 啟動器已用新引擎 ref（不再走 grep／inspect；已寫 launcher_start）"), 220)',
    'b.box("s10a", U, 5, ENTRY, fl("來自「E(a)(b)」頁：啟動器已用新引擎 ref（不走 grep／inspect；已寫 launcher_start）"), 220)')
rep('b.box("s12s", E, 7, v2(D12), "薄殼 == 上次產物？（首行自描述 hash、未被改）", 260, ax="l")', 'b.box("s12s", E, 7, v2(D12), "薄殼 == 上次產物？（首行自描述 hash、未被改）", 340, ax="l")')
rep('b.box("s12dx", U, 8, v2(O12), fl("是 → 3：印 6-10（目標引擎無法無損讀現有檔；零寫入，要退回請 git revert）"), 220)',
    'b.box("s12dx", U, 8, v2(O12), fl("是 → 3：印 6-10（無法無損讀現有檔；零寫入）"), 220)')
rep('b.box("s12d", E, 8, v2(D12), fl("是 → @<tag> 為舊版且無法無損讀現有檔（P／schema）？"), 260, ax="l")',
    'b.box("s12d", E, 8, v2(D12), fl("是 → @<tag> 為舊版且無法無損讀？（P／schema）"), 340, ax="l")')
rep('b.box("s12hz", U, 14, v2(ENTRY), fl("續跑入口：用新引擎回到本頁「docker run 該引擎」格再跑一次（同一次指令內；第二次第一行又變 → 1 印 6-2b）"), 220)',
    'b.box("s12hz", U, 14, v2(ENTRY), fl("續跑：新引擎回到本頁「docker run 該引擎」格再跑一次（第二次第一行又變 → 1 + 6-2b）"), 220)')

# =====================================================================
# 名詞表三條（所有 T 表；放 EXIT3 之前）
# =====================================================================
rep('''# ================= P5：bootstrap.sh（1）=================
T5 = [''',
'''# ================= P5：bootstrap.sh（1）=================
LOGT = [   # v2.12 操作紀錄檔（每頁名詞表共用）
 ("操作紀錄檔／log（v2.12）", ".vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，每次執行一檔（JSON Lines：timestamp、event_name、body、trace_id、attributes）；啟動器先建檔並寫 launcher_start 才動手，引擎 resolve 前 append engine_start（皆失敗 → 1 + 6-38）；印到 tty 的訊息同句進 body；結束時 prune（最近 30 天且最多 50 檔）；不進 git、不進 image"),
 ("config.toml（v2.12）", ".vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 第一次建（含註解與預設值），upgrade 三方合併；缺檔／缺鍵 = 預設，非正整數 → 預設 + 警告"),
 ("6-38", "log 檔建不了或寫不進（launcher_start／engine_start 失敗）→ 1，零寫入、不進 resolve；附清空間提示；所有動詞一致（含 help），無 --no-log"),
]
T5 = [''')
rep(" EXIT3,\n]", " *LOGT, EXIT3,\n]", 8)

# =====================================================================
# bootstrap(1)：a0l 格；a9f 清單加 config.toml、.dockerignore 四行；T5 文字
# =====================================================================
rep('b.box("a0", U, 0, G12, "執行 bootstrap.sh -t <repo>[@<tag>]…", 220)\n',
    'b.box("a0", U, 0, G12, "執行 bootstrap.sh -t <repo>[@<tag>]…", 220)\nb.box("a0l", L, 0, v2(W12), ' + LOG_BOX + ', 280)\n')
rep('b.D("ae1", "a0", "a1"); b.H("ae2", "a1", "a2", "否")', 'b.H("ae1", "a0", "a0l"); b.D("ae1l", "a0l", "a1", al=True); b.H("ae2", "a1", "a2", "否")')
rep('"根 justfile（無 → import 行 + default recipe；有 → 加 import 一行）", "根 .dockerignore 三行（有 → 問後加）"], 360, cols=2)',
    '"config.toml（註解＋預設 keep=50／days=30）", "根 justfile（無 → import 行 + default recipe；有 → 加 import 一行）", "根 .dockerignore 四行（含 log/；有 → 問後加）"], 360, cols=2)')
rep(' ("bootstrap.sh", "release 附的 POSIX sh 薄層：檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref',
    ' ("bootstrap.sh", "release 附的 POSIX sh 薄層：建 log 檔寫 launcher_start → 檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref')
rep('根 .dockerignore 三行問後加）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）"),',
    '根 .dockerignore 四行問後加；建 config.toml）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）"),')
rep(' ("薄殼 .vendor_kit/", ".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、baseline/（進 git）＋ cache/、gen/、version.local.toml、.tmp.*（不進 git）"),',
    ' ("薄殼 .vendor_kit/", ".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、config.toml、baseline/（進 git）＋ cache/、gen/、log/、version.local.toml、.tmp.*（不進 git）"),')

# =====================================================================
# install(1)：i0l／i1e 格；config.toml 產檔；全部列 +1（config 再 +1）
# =====================================================================
rep('''b.box("i0", U, 0, G12, "just vendor_kit install（-y、--no-justfile）", 220)
b.box("i1", L, 0, W12, "docker run <引擎> install …\\n（啟動器不鎖；鎖在引擎）", 280)
b.box("i3", U, 1, O12, "1：請先 git init（不代做）", 220)
b.box("i2", E, 1, D12, "是 git repo？", 220, ax="l")
b.box("i2x", U, 2, v2(O12), fl("是 → 1：<dir> 已有 .vendor_kit/，不允許巢狀；請到該目錄執行或先 uninstall"), 220)
b.box("i2n", E, 2, v2(D12), fl("上層或下層已有 .vendor_kit/？（禁止巢狀，Q20）"), 300, ax="l")
b.box("i4a", E, 3, v2(SUB), "否：flock 專案目錄（60 秒）", 400)
b.box("i4", E, 4, v2(SUB), fl("產 .gitignore 到暫存（首行自描述）"), 400)
b.box("i4n", P, 4, NOTE, fl("第一次 install（薄殼不存在）：不建進度日誌，任一步失敗 → 丟棄暫存、移除已寫到正式位置的檔，專案不留任何檔 → 1（「不留半成品」只對第一次成立，v2.2 C）；修復型 install：建 .vendor_kit/.tmp.install.<id>.toml 進度日誌（第一個寫入前），失敗 → 1 列已完成／未完成，收尾（install（2））後刪（v2.8 §2）"), 360)
b.box("i4_2", E, 5, v2(SUB), fl("產 entry.just 到暫存（首行自描述）"), 400)
b.box("i4_3", E, 6, v2(SUB), fl("產 vendor.just 到暫存（首行自描述）"), 400)
b.box("i4_4", E, 7, v2(SUB), fl("產 ci/check.sh 到暫存（自描述在第二行）"), 400)
b.box("i4e", E, 8, v2(D12), "薄殼已存在？", 240, ax="l")
b.box("i4en", E, 8, v2(W12), "否：第一次 = 全新建", 130, ax="r")
b.box("i4x", U, 9, v2(O12), fl("否 → 1：被改過，列差異不動（git checkout 還原後再跑）"), 220)
b.box("i4q", E, 9, v2(D12), "薄殼 == 上次產物？（首行自描述 hash）", 240, ax="l")
b.box("i4qn", P, 9, v2(NOTE), fl("自描述（Q17）：薄殼每檔首行 # vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 LF 正規化 hash>；引擎重算 + 對 image 內模板二次比對；不用 gen/.stamp（不進 git，重新 clone 後也不存在）"), 360)
b.box("i4l", E, 10, v2(W12), fl("是（修復型）：建進度日誌 .tmp.install.<id>.toml（第一個寫入前）"), 240, ax="l")
b.box("i4lf", P, 10, v2(F12), "＋.vendor_kit/.tmp.install.<id>.toml（進度日誌，不進 git；修復型才有，收尾後刪；第一次 install 不建，失敗整包丟棄）", 360)
b.box("i4b", E, 11, v2(SUB), fl("薄殼四檔逐檔原子替換（暫存 → 正式位置）"), 400)
b.files("i4f", P, 11, "＋薄殼四檔（進 git）", [".vendor_kit/.gitignore", ".vendor_kit/entry.just", ".vendor_kit/vendor.just", ".vendor_kit/ci/check.sh"], 360)
b.box("i4c", E, 12, v2(SUB), fl("寫 version.toml：第一行 = 引擎 ref（＋schema、written_by；已有則不動）"), 400)
b.box("i4cf", P, 12, F12, "＋version.toml（第一行引擎 ref、schema、written_by；進 git）", 360)
b.box("i4d", E, 13, v2(SUB), "寫 gen/.stamp（只記引擎 ref）", 400)
b.box("i4df", P, 13, F12, "＋gen/.stamp（不進 git）", 360)
b.box("i4g", E, 14, v2(SUB), fl("建 baseline/.gitkeep（git 不追蹤空目錄；metadata 到 add 才建）"), 400)
b.box("i4gf", P, 14, F12, "＋baseline/.gitkeep（進 git）", 360)
b.box("i5z", E, 15, LBL, "↓ 續「install（2）」頁：根 justfile 與根 .dockerignore", 300, 24, ax="l", minh=24)
b.H("ie1", "i0", "i1"); b.D("ie2", "i1", "i2"); b.H("ie3", "i2", "i3", "否")
b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是")
b.D("ie4", "i2n", "i4a", "否", al=True); b.D("ie4b", "i4a", "i4"); b.D("ie4c", "i4", "i4_2"); b.D("ie4d", "i4_2", "i4_3"); b.D("ie4e", "i4_3", "i4_4"); b.D("ie5", "i4_4", "i4e", al=True)''',
'''b.box("i0", U, 0, G12, "just vendor_kit install（-y、--no-justfile）", 220)
b.box("i0l", L, 0, v2(W12), ''' + LOG_BOX + ''', 220)
b.box("i1", L, 1, W12, "docker run <引擎> install …\\n（啟動器不鎖；鎖在引擎）", 280)
b.box("i1e", E, 1, v2(SUB), ''' + ENG_BOX + ''', 400)
b.box("i3", U, 2, O12, "1：請先 git init（不代做）", 220)
b.box("i2", E, 2, D12, "是 git repo？", 220, ax="l")
b.box("i2x", U, 3, v2(O12), fl("是 → 1：<dir> 已有 .vendor_kit/，不允許巢狀；請到該目錄執行或先 uninstall"), 220)
b.box("i2n", E, 3, v2(D12), fl("上層或下層已有 .vendor_kit/？（禁止巢狀，Q20）"), 340, ax="l")
b.box("i4a", E, 4, v2(SUB), "否：flock 專案目錄（60 秒）", 400)
b.box("i4", E, 5, v2(SUB), fl("產 .gitignore 到暫存（首行自描述；排除 cache/、gen/、log/、version.local.toml、.tmp.*）"), 400)
b.box("i4n", P, 5, NOTE, fl("第一次 install（薄殼不存在）：不建進度日誌，任一步失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔 → 1（v2.2 C）；修復型 install：建 .tmp.install.<id>.toml 進度日誌（第一個寫入前），失敗 → 1 列已完成／未完成，收尾後刪（v2.8 §2）"), 360)
b.box("i4_2", E, 6, v2(SUB), fl("產 entry.just 到暫存（首行自描述）"), 400)
b.box("i4_3", E, 7, v2(SUB), fl("產 vendor.just 到暫存（首行自描述）"), 400)
b.box("i4_4", E, 8, v2(SUB), fl("產 ci/check.sh 到暫存（自描述在第二行）"), 400)
b.box("i4_5", E, 9, v2(SUB), fl("產 config.toml 到暫存（含註解與預設 schema=1、[log] keep=50、days=30；已有 → 不產、不動，v2.12）"), 400)
b.box("i4e", E, 10, v2(D12), "薄殼已存在？", 240, ax="l")
b.box("i4en", E, 10, v2(W12), "否：第一次 = 全新建", 130, ax="r")
b.box("i4x", U, 11, v2(O12), fl("否 → 1：被改過，列差異不動（git checkout 還原後再跑）"), 220)
b.box("i4q", E, 11, v2(D12), "薄殼 == 上次產物？（首行自描述 hash）", 300, ax="l")
b.box("i4qn", P, 11, v2(NOTE), fl("自描述（Q17）：薄殼每檔首行 # vendor_kit-shell/<P> engine=<vX> sha256=<其餘內容 LF 正規化 hash>；引擎重算 + 對 image 內模板二次比對；不用 gen/.stamp（不進 git，重新 clone 後也不存在）"), 360)
b.box("i4l", E, 12, v2(W12), fl("是（修復型）：建進度日誌 .tmp.install.<id>.toml（第一個寫入前）"), 240, ax="l")
b.box("i4lf", P, 12, v2(F12), "＋.vendor_kit/.tmp.install.<id>.toml（進度日誌，不進 git；修復型才有，收尾後刪；第一次 install 不建，失敗整包丟棄）", 360)
b.box("i4b", E, 13, v2(SUB), fl("薄殼四檔（＋第一次的 config.toml）逐檔原子替換（暫存 → 正式位置）"), 400)
b.files("i4f", P, 13, "＋薄殼四檔＋config.toml（進 git）", [".vendor_kit/.gitignore", ".vendor_kit/entry.just", ".vendor_kit/vendor.just", ".vendor_kit/ci/check.sh", ".vendor_kit/config.toml（第一次才建；註解＋預設 keep=50／days=30）"], 360)
b.box("i4c", E, 14, v2(SUB), fl("寫 version.toml：第一行 = 引擎 ref（＋schema、written_by；已有則不動）"), 400)
b.box("i4cf", P, 14, F12, "＋version.toml（第一行引擎 ref、schema、written_by；進 git）", 360)
b.box("i4d", E, 15, v2(SUB), "寫 gen/.stamp（只記引擎 ref）", 400)
b.box("i4df", P, 15, F12, "＋gen/.stamp（不進 git）", 360)
b.box("i4g", E, 16, v2(SUB), fl("建 baseline/.gitkeep（git 不追蹤空目錄；metadata 到 add 才建）"), 400)
b.box("i4gf", P, 16, F12, "＋baseline/.gitkeep（進 git）", 360)
b.box("i5z", E, 17, LBL, "↓ 續「install（2）」頁：根 justfile 與根 .dockerignore", 300, 24, ax="l", minh=24)
b.H("ie1", "i0", "i0l"); b.D("ie1l", "i0l", "i1", al=True); b.H("ie1e", "i1", "i1e"); b.D("ie2", "i1e", "i2", al=True); b.H("ie3", "i2", "i3", "否")   # launcher_start／engine_start（v2.12）
b.D("ie2n", "i2", "i2n", "是", al=True); b.H("ie2x", "i2n", "i2x", "是")
b.D("ie4", "i2n", "i4a", "否", al=True); b.D("ie4b", "i4a", "i4"); b.D("ie4c", "i4", "i4_2"); b.D("ie4d", "i4_2", "i4_3"); b.D("ie4e", "i4_3", "i4_4"); b.D("ie4f", "i4_4", "i4_5"); b.D("ie5", "i4_5", "i4e", al=True)''')
rep('b = F.band("bI", "5a′ install：專案層動詞（bootstrap.sh 代打，也可自己打）；再跑 = 引擎重寫薄殼（先比對首行自描述 hash）= 冪等修復；第一次不建日誌、修復型建 .tmp.install.<id>.toml（v2.8 §2）；禁止巢狀（Q20）", v2=True)',
    'b = F.band("bI", "5a′ install：專案層動詞（bootstrap.sh 代打，也可自己打）；launcher_start → engine_start → 產薄殼四檔＋config.toml；再跑 = 引擎重寫薄殼（先比對首行自描述 hash）= 冪等修復；第一次不建日誌、修復型建 .tmp.install.<id>.toml（v2.8 §2）；禁止巢狀（Q20）", v2=True)')

# =====================================================================
# install(2)：.dockerignore 四行（＋.vendor_kit/log/）；入口文字
# =====================================================================
rep('根 justfile（無 → 新建 import 行 + default recipe；有 → 問後加一行）→ 根 .dockerignore（無 → 建三行；有 → 問後 append）", pad=40, v2=True)',
    '根 justfile（無 → 新建 import 行 + default recipe；有 → 問後加一行）→ 根 .dockerignore（無 → 建四行；有 → 問後 append；v2.12 加 log/）", pad=40, v2=True)')
rep('b.box("i5e", E, 0, ENTRY, "來自「install（1）」頁：薄殼與 .vendor_kit/ 各檔已寫", 300, ax="l")',
    'b.box("i5e", E, 0, ENTRY, "來自「install（1）」頁：薄殼與 .vendor_kit/ 各檔已寫（已寫 launcher_start）", 300, ax="l")')
rep('b.box("ign", E, 6, v2(W12), fl("無：建 .dockerignore（三行，逐字見右）"), 120, ax=280)', 'b.box("ign", E, 6, v2(W12), fl("無：建 .dockerignore（四行，逐字見右）"), 120, ax=280)')
rep('b.box("ignf", P, 6, v2(PRE), "＋.dockerignore（新建，三行）：\\n.vendor_kit/cache/\\n.vendor_kit/gen/\\n.vendor_kit/.tmp.*", 360)',
    'b.box("ignf", P, 6, v2(PRE), "＋.dockerignore（新建，四行）：\\n.vendor_kit/cache/\\n.vendor_kit/gen/\\n.vendor_kit/log/\\n.vendor_kit/.tmp.*", 360)')
rep('b.box("igq", E, 7, v2(D12), "有 → 問「要在 .dockerignore 加這三行嗎」同意？（-y 免問；已含則跳過）", 250, ax="l")',
    'b.box("igq", E, 7, v2(D12), "有 → 問「要在 .dockerignore 加這四行嗎」同意？（-y 免問；已含則跳過）", 250, ax="l")')
rep('b.box("igy", E, 8, v2(W12), fl("是：append 三行"), 250, ax="l")', 'b.box("igy", E, 8, v2(W12), fl("是：append 四行"), 250, ax="l")')
rep('b.box("igyf", P, 8, v2(PRE), ".dockerignore（尾端＋三行；Q22 補）：\\n.vendor_kit/cache/\\n.vendor_kit/gen/\\n.vendor_kit/.tmp.*", 360)',
    'b.box("igyf", P, 8, v2(PRE), ".dockerignore（尾端＋四行；Q22 補、v2.12）：\\n.vendor_kit/cache/\\n.vendor_kit/gen/\\n.vendor_kit/log/\\n.vendor_kit/.tmp.*", 360)')
rep('b.box("igx", U, 8, v2(G12), fl("0：不寫 .dockerignore、印指示（含 justfile 結果）"), 220)', 'b.box("igx", U, 8, v2(G12), fl("0：不寫 .dockerignore、印指示（四行；含 justfile 結果）"), 220)')

# =====================================================================
# add(1)：c0l／c1e 格，列 +2；add 前清單 .dockerignore 四行＋config.toml；add(1′)(2) 入口文字
# =====================================================================
rep('''b.box("c0", U, 0, G12, "just vendor_kit add <repo>[@<tag>]（-y、--dry-run…）", 220)
b.box("c1", L, 0, v2(W12), fl("docker run <引擎> resolve add <repo>\\n（--local：tar 先 docker load，讀同名 .digest）"), 280)
b.box("c2a", E, 0, v2(SUB), "resolve（不寫任何檔）：讀 version.toml", 400)
b.box("c2b", E, 1, v2(SUB), fl("查 tag（預設最新正式版／@<tag>）與 index digest（--source 改來源）"), 400)
b.box("c3", G, 1, IMG, "ghcr.io/<org>/<repo>-dist\\n（工具 image；多架構 index digest）", 220)
b.box("c2px", U, 2, v2(O12), "是 → 1：印 6-3（私有 image：請指定 @<tag> 或提供 registry 憑證）", 220)
b.box("c2pq", E, 2, v2(D12), fl("私有 image 且未指定 @<tag> 且無憑證？"), 310, ax="l")   # v2.9 §2
b.box("c4", E, 3, D12, "已接入 <repo>？", 310, ax="l")
b.box("c5", E, 4, D12, "metadata 有完成標記？", 310, ax="l")
b.box("c6x", U, 5, v2(O12), "是 → 1：@<tag> 與鎖定不同，請改用 upgrade", 220)
b.box("c5t", E, 5, D12, "@<tag> 與鎖定不同？", 220, ax=45)
b.box("c8", E, 5, W12, fl("否：續作，只做缺的步驟（不補刻意刪的檔）"), 120, ax="r")
b.box("c6", U, 6, G12, "否 → 0：已接入且完成，無變更", 220)
b.box("c2c", E, 7, v2(SUB), fl("resolve 完 → 產生執行計畫（要拉的 image@digest、mount、apply 與否）"), 400)
b.box("c2d", E, 8, v2(SUB), fl("產生輸入指紋（version.toml、metadata、要動的使用者檔 hash、鎖定 digest）→ 計畫＋指紋以 stdout 回啟動器"), 400)
b.box("c9a", L, 9, v2(D12), "docker image inspect：本機有？", 170, ax="l")
b.box("c9p", L, 10, v2(W12), "無：docker pull", 100, ax="r")
b.box("c9g", G, 10, IMG, "<repo>-dist@digest\\n（鎖定的那一版）", 220)
b.box("c9b", L, 11, v2(W12), "docker create <image> /x", 280)
b.box("c9c", L, 12, v2(W12), "docker cp c:/dist/. <tmp>/<repo>/（主機暫存）", 280)
b.box("c9d", L, 13, v2(W12), "docker rm 該容器", 280)
b.box("c9z", L, 14, LBL, "↓ 續「add（1′）」頁：docker run 引擎 apply add → 前置檢查", 280, 24, minh=24)
b.H("ce1", "c0", "c1"); b.H("ce2", "c1", "c2a"); b.D("ce2b", "c2a", "c2b"); b.H("ce3", "c2b", "c3", "查")''',
'''b.box("c0", U, 0, G12, "just vendor_kit add <repo>[@<tag>]（-y、--dry-run…）", 220)
b.box("c0l", L, 0, v2(W12), ''' + LOG_BOX + ''', 220)
b.box("c1", L, 1, v2(W12), fl("docker run <引擎> resolve add <repo>\\n（--local：存在的 .tar 先 docker load，讀同名 .digest）"), 280)
b.box("c1e", E, 1, v2(SUB), ''' + ENG_BOX + ''', 400)
b.box("c2a", E, 2, v2(SUB), "resolve（不寫任何檔）：讀 version.toml", 400)
b.box("c2b", E, 3, v2(SUB), fl("查 tag（預設最新正式版／@<tag>）與 index digest（--source 改來源）"), 400)
b.box("c3", G, 3, IMG, "ghcr.io/<org>/<repo>-dist\\n（工具 image；多架構 index digest）", 220)
b.box("c2px", U, 4, v2(O12), "是 → 1：印 6-3（私有 image：請指定 @<tag> 或提供 registry 憑證）", 220)
b.box("c2pq", E, 4, v2(D12), fl("私有 image 且未指定 @<tag> 且無憑證？"), 310, ax="l")   # v2.9 §2
b.box("c4", E, 5, D12, "已接入 <repo>？", 310, ax="l")
b.box("c5", E, 6, D12, "metadata 有完成標記？", 310, ax="l")
b.box("c6x", U, 7, v2(O12), "是 → 1：@<tag> 與鎖定不同，請改用 upgrade", 220)
b.box("c5t", E, 7, D12, "@<tag> 與鎖定不同？", 220, ax=45)
b.box("c8", E, 7, W12, fl("否：續作，只做缺的步驟（不補刻意刪的檔）"), 120, ax="r")
b.box("c6", U, 8, G12, "否 → 0：已接入且完成，無變更", 220)
b.box("c2c", E, 9, v2(SUB), fl("resolve 完 → 產生執行計畫（要拉的 image@digest、mount、apply 與否）"), 400)
b.box("c2d", E, 10, v2(SUB), fl("產生輸入指紋（version.toml、metadata、要動的使用者檔 hash、鎖定 digest）→ 計畫＋指紋以 stdout 回啟動器"), 400)
b.box("c9a", L, 11, v2(D12), "docker image inspect：本機有？", 170, ax="l")
b.box("c9p", L, 12, v2(W12), "無：docker pull", 100, ax="r")
b.box("c9g", G, 12, IMG, "<repo>-dist@digest\\n（鎖定的那一版）", 220)
b.box("c9b", L, 13, v2(W12), "docker create <image> /x", 280)
b.box("c9c", L, 14, v2(W12), "docker cp c:/dist/. <tmp>/<repo>/（主機暫存）", 280)
b.box("c9d", L, 15, v2(W12), "docker rm 該容器", 280)
b.box("c9z", L, 16, LBL, "↓ 續「add（1′）」頁：docker run 引擎 apply add → 前置檢查", 280, 24, minh=24)
b.H("ce1", "c0", "c0l"); b.D("ce1l", "c0l", "c1", al=True); b.H("ce2", "c1", "c1e"); b.D("ce2e", "c1e", "c2a"); b.D("ce2b", "c2a", "c2b"); b.H("ce3", "c2b", "c3", "查")   # launcher_start／engine_start（v2.12）''')
rep('_cf0 = ["justfile（＋import 行）", ".dockerignore（＋三行）", "version.toml（vendor_kit 行）", "version.local.toml（--local 時）", "薄殼四檔：.gitignore、entry.just、vendor.just、ci/check.sh", "gen/.stamp", "baseline/.gitkeep"]',
    '_cf0 = ["justfile（＋import 行）", ".dockerignore（＋四行，含 log/）", "version.toml（vendor_kit 行）", "config.toml（keep／days 預設）", "version.local.toml（--local 時）", "薄殼四檔：.gitignore、entry.just、vendor.just、ci/check.sh", "gen/.stamp", "baseline/.gitkeep"]')
rep('b = F.band("bB", "5b add <repo>[@<tag>]（bootstrap.sh 對每個 -t 呼叫；使用者也直接打）= 引擎 resolve（不寫；私有 image 未指定 @<tag> 且無憑證 → 1 + 6-3）→ 啟動器 docker（inspect → 無才 pull → create → cp → rm）；續「add（1′）」「add（2）」頁", v2=True)',
    'b = F.band("bB", "5b add <repo>[@<tag>]（bootstrap.sh 對每個 -t 呼叫；使用者也直接打）= launcher_start → engine_start → 引擎 resolve（不寫；私有 image 未指定 @<tag> 且無憑證 → 1 + 6-3）→ 啟動器 docker（inspect → 無才 pull → create → cp → rm）；續「add（1′）」「add（2）」頁", v2=True)')
rep('b.box("c9e", L, 0, ENTRY, "來自「add（1）」頁：/dist/<repo> 已在主機暫存", 280)', 'b.box("c9e", L, 0, ENTRY, "來自「add（1）」頁：/dist/<repo> 已在主機暫存（已寫 launcher_start）", 280)')
rep('b.box("c13c", E, 0, ENTRY, "來自「add（1′）」頁：apply 檢查通過（非 dry-run）", 300)', 'b.box("c13c", E, 0, ENTRY, "來自「add（1′）」頁：apply 檢查通過（非 dry-run；已寫 launcher_start）", 300)')

# =====================================================================
# sync(1)：n0l 格；快路徑 nql（sync_fast_path、launcher_exit）；列 +1／+2
# =====================================================================
rep('''b.box("n0", U, 0, G12, "打工具 recipe（_sync 自動前置）或 just vendor_kit sync", 220)
b.box("n1", L, 0, v2(W12), fl("grep version.toml 第一行取引擎 ref（version.local.toml 的 vendor_kit 覆寫優先）"), 280)
b.files("n2", P, 0, "讀", [".vendor_kit/version.toml（進 git）", ".vendor_kit/version.local.toml（不進 git，dev 用）"], 360)
b.box("n3n", U, 1, v2(O12), fl("否 → 1：印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」"), 220)
b.box("n3", L, 1, v2(D12), "gen/.stamp 的引擎 ref ＝ 第一行？", 260, ax="l")
b.box("n6", P, 1, v2(RULE), fl("統一提示（Q10 (2)、v2.3 §2）：啟動器發現 gen/.stamp ≠ 引擎 ref → 退出 1 印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」；不自動重寫、不自動續跑；install／upgrade vendor_kit 不受此關"), 360)
b.box("nq0", U, 2, v2(G12), fl("是 → 0：不起容器，接著跑原本的 recipe（快路徑）"), 220)
b.box("nq", L, 2, v2(D12), fl("快路徑：grep 全相符且非 frozen？"), 260, ax="l")
b.box("nqr", P, 2, v2(RULE), fl("快路徑（Q22）：啟動器只 grep：[tools] 每行 digest == gen/<repo>.stamp 第一行（或 path:<dir>）；gen/tools.just 存在；無 .tmp.<verb>.*.toml；CI 不為真；sync 無參數。全相符 → 0；否則起引擎；每檔 sha256 只在 sync --verify、CI 為真、或版本變動的那次才做（§3.6）"), 360)
b.box("n1i", L, 3, v2(D12), "docker image inspect：本機有？", 220, ax=20)
b.box("n6b", P, 3, v2(RULE), fl("薄殼重產（v2.2 A、Q10 (2)、Q17）：只由 install 與 upgrade vendor_kit 做；做之前比對現內容 == 上次產物（首行自描述 hash），相同 → 重產，被改過 → 1 列差異不動；sync 永不寫薄殼"), 360)
b.box("n1p", L, 4, v2(W12), "無：docker pull <引擎 ref>", 80, ax="r")
b.box("n1g", G, 4, IMG, "vendor_kit:vN@sha256:…\\n（引擎 image）", 220)
b.box("n1v", L, 5, v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？"), 220, ax=20)
b.box("n1x", E, 5, v2(R12), fl("拉不到／image ID 不符（同 tag 重 build）→ 1：印原因"), 240, ax="l")
b.box("n1b", L, 6, v2(W12), fl("否：docker run <引擎> resolve sync（永不 -t）"), 280)
b.box("n1z", E, 6, LBL, "→ 續「sync（1′）」頁：引擎 resolve sync（逐工具）", 300, 24, ax="l", minh=24)
b.H("ne1", "n0", "n1"); b.H("ne2", "n1", "n2", "讀"); b.D("ne3", "n1", "n3", al=True)
b.H("ne4", "n3", "n3n", "否"); b.D("ne5", "n3", "nq", "是", al=True); b.H("ne5q", "nq", "nq0", "是"); b.D("ne5n", "nq", "n1i", "否", al=True)''',
'''b.box("n0", U, 0, G12, "打工具 recipe（_sync 自動前置）或 just vendor_kit sync", 220)
b.box("n0l", L, 0, v2(W12), ''' + LOG_BOX + ''', 220)
b.box("n1", L, 1, v2(W12), fl("grep version.toml 第一行取引擎 ref（version.local.toml 的 vendor_kit 覆寫優先）"), 280)
b.files("n2", P, 1, "讀", [".vendor_kit/version.toml（進 git）", ".vendor_kit/version.local.toml（不進 git，dev 用）"], 360)
b.box("n3n", U, 2, v2(O12), fl("否 → 1：印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」"), 220)
b.box("n3", L, 2, v2(D12), "gen/.stamp 的引擎 ref ＝ 第一行？", 260, ax="l")
b.box("n6", P, 2, v2(RULE), fl("統一提示（Q10 (2)、v2.3 §2）：啟動器發現 gen/.stamp ≠ 引擎 ref → 退出 1 印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」；不自動重寫、不自動續跑；install／upgrade vendor_kit 不受此關"), 360)
b.box("nql", U, 3, v2(W12), fl("是：log 檔寫 sync_fast_path、launcher_exit（v2.12）"), 220)
b.box("nq", L, 3, v2(D12), fl("快路徑：grep 全相符且非 frozen？"), 260, ax="l")
b.box("nqr", P, 3, v2(RULE), fl("快路徑（Q22）：啟動器只 grep：[tools] 每行 digest == gen/<repo>.stamp 第一行（或 path:<dir>）；gen/tools.just 存在；無 .tmp.<verb>.*.toml；CI 不為真；sync 無參數。全相符 → 寫 log 後 0；否則起引擎；每檔 sha256 只在 sync --verify、CI 為真、或版本變動的那次才做（§3.6）"), 360)
b.box("nq0", U, 4, v2(G12), fl("0：不起容器，接著跑原本的 recipe（快路徑）"), 220)
b.box("n1i", L, 4, v2(D12), "docker image inspect：本機有？", 220, ax=20)
b.box("n6b", P, 4, v2(RULE), fl("薄殼重產（v2.2 A、Q10 (2)、Q17）：只由 install 與 upgrade vendor_kit 做；做之前比對現內容 == 上次產物（首行自描述 hash），相同 → 重產，被改過 → 1 列差異不動；sync 永不寫薄殼"), 360)
b.box("n1p", L, 5, v2(W12), "無：docker pull <引擎 ref>", 80, ax="r")
b.box("n1g", G, 5, IMG, "vendor_kit:vN@sha256:…\\n（引擎 image）", 220)
b.box("n1v", L, 6, v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？"), 220, ax=20)
b.box("n1x", E, 6, v2(R12), fl("拉不到／image ID 不符（同 tag 重 build）→ 1：印原因"), 240, ax="l")
b.box("n1b", L, 7, v2(W12), fl("否：docker run <引擎> resolve sync（永不 -t）"), 280)
b.box("n1z", E, 7, LBL, "→ 續「sync（1′）」頁：引擎 resolve sync（逐工具）", 300, 24, ax="l", minh=24)
b.H("ne1", "n0", "n0l"); b.D("ne1l", "n0l", "n1", al=True); b.H("ne2", "n1", "n2", "讀"); b.D("ne3", "n1", "n3", al=True)   # launcher_start（v2.12）
b.H("ne4", "n3", "n3n", "否"); b.D("ne5", "n3", "nq", "是", al=True); b.H("ne5q", "nq", "nql", "是"); b.D("ne5ql", "nql", "nq0", al=True); b.D("ne5n", "nq", "n1i", "否", al=True)   # 快路徑寫 log 才結束（v2.12）''')
rep('b = F.band("eA", "sync（工具 recipe 的自動前置；CI 為真 → frozen）：第 1 段 = 啟動器比對 gen/.stamp（install／upgrade vendor_kit 跳過）→ 快路徑 grep 全相符 → 0 不起容器；有差 → docker image inspect → 引擎 resolve sync（見「sync（1′）」頁）", v2=True)',
    'b = F.band("eA", "sync（工具 recipe 的自動前置；CI 為真 → frozen）：第 1 段 = launcher_start → 啟動器比對 gen/.stamp（install／upgrade vendor_kit 跳過）→ 快路徑 grep 全相符 → 寫 sync_fast_path、launcher_exit → 0 不起容器；有差 → inspect → 引擎 resolve sync（見「sync（1′）」頁）", v2=True)')
rep('b.box("n1e", E, 0, ENTRY, "來自「sync（1）」頁：docker run <引擎> resolve sync", 300)', 'b.box("n1e", E, 0, ENTRY, "來自「sync（1）」頁：docker run <引擎> resolve sync（已寫 launcher_start；已 append engine_start）", 300)')
rep('b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（resolve 的 stdout 清單，apply|yes）", 280)', 'b.box("m00", L, 0, ENTRY, "來自「sync（1′）」頁：有待辦（resolve 的 stdout 清單，apply|yes；已寫 launcher_start）", 280)')

# =====================================================================
# upgrade A（Renovate）：check.sh ① 已寫 launcher_start
# =====================================================================
rep('b.box("a4b", L, 3, W12, "check.sh ①：sync（CI 為真 → frozen；export CI=1）", 220)', 'b.box("a4b", L, 3, W12, "check.sh ①：sync（CI 為真 → frozen；export CI=1；已寫 launcher_start）", 220)')

# =====================================================================
# upgrade B(1)：b0l／b1e 格，列 +2；B(1′)(2)(2′) 入口文字
# =====================================================================
rep('''b.box("b0", U, 0, G12, "just vendor_kit upgrade <repo>[@<tag>]（-y、--dry-run）", 220)
b.box("b1", L, 0, v2(W12), "docker run <引擎> resolve upgrade <repo>\\n（啟動器不鎖）", 240)
b.box("b1x", U, 1, v2(O12), "是 → 1：請先 undev <repo>", 220)
b.box("b1q", E, 1, v2(D12), "<repo> 在 dev 覆寫中？", 280, ax="l")
b.box("b2c", U, 2, v2(O12), "是 → 2：先解完衝突再重跑", 220)
b.box("b2", E, 2, v2(D12), "(0) 衝突檔仍含我們的標籤？", 360, ax="l")
b.box("b2n", P, 2, NOTE, fl("標籤 = 我們自己產的 <<<<<<< vendor_kit:baseline 等；檔案失蹤不算已解；resolve 只偵測，「清除已解的衝突狀態」在 apply 內、建日誌之後（v2.5 §3）"), 280)
b.box("b5", U, 3, O12, "否 → 1：無 baseline，請先 add <repo>", 220)
b.box("b4", E, 3, D12, "有 baseline/<repo>/？", 340, ax=10)
b.box("b6", E, 4, v2(D12), "(1) 有待合併？", 170, ax="l")
b.box("b6y", E, 5, v2(W12), fl("是：目標版 = B（version.toml 那版），補到就停，不查最新"), 170, ax="r")
b.box("b7a", E, 6, v2(D12), "否 → @<tag> 指定？", 170, ax="l")
b.box("b7t", E, 6, v2(W12), fl("是：目標版 = @<tag>（比現版舊 → warn 仍執行）"), 170, ax="r")
b.box("b7b", E, 7, v2(D12), "否 → CI 為真（frozen）？", 170, ax="l")
b.box("b7z", E, 7, v2(W12), fl("是：不查最新；目標版 = 鎖定版（無事可做）"), 170, ax="r")
b.box("b7c", E, 8, v2(W12), fl("否：(2) 查 registry 最新正式版 = 目標版"), 170, ax="l")
b.box("b7s", E, 9, v2(SUB), fl("resolve 完 → stdout：目標 tag@digest ＋ 輸入指紋（version.toml、metadata、要動的使用者檔 hash、鎖定 digest）"), 360)
b.box("b8a", L, 10, v2(D12), "docker image inspect：本機有？", 170, ax="l")
b.box("b8p", L, 11, v2(W12), "無：docker pull", 70, ax="r")
b.box("b8g", G, 11, IMG, "<repo>-dist\\n目標 tag@digest", 180)
b.box("b8b", L, 12, v2(W12), "docker create <img> /x", 240)
b.box("b8c", L, 13, v2(W12), "docker cp c:/dist/. <tmp>/<repo>/（主機暫存）", 240)
b.box("b8d", L, 14, v2(W12), "docker rm 該容器", 240)
b.box("b8z", L, 15, LBL, "↓ 續「B（1′）」頁：docker run 引擎 apply upgrade → 前置檢查", 240, 24, minh=24)
b.H("be1", "b0", "b1"); b.D("be1q", "b1", "b1q"); b.H("be1x", "b1q", "b1x", "是")''',
'''b.box("b0", U, 0, G12, "just vendor_kit upgrade <repo>[@<tag>]（-y、--dry-run）", 220)
b.box("b0l", L, 0, v2(W12), ''' + LOG_BOX + ''', 240)
b.box("b1", L, 1, v2(W12), "docker run <引擎> resolve upgrade <repo>\\n（啟動器不鎖）", 240)
b.box("b1e", E, 1, v2(SUB), ''' + ENG_BOX + ''', 360)
b.box("b1x", U, 2, v2(O12), "是 → 1：請先 undev <repo>", 220)
b.box("b1q", E, 2, v2(D12), "<repo> 在 dev 覆寫中？", 280, ax="l")
b.box("b2c", U, 3, v2(O12), "是 → 2：先解完衝突再重跑", 220)
b.box("b2", E, 3, v2(D12), "(0) 衝突檔仍含我們的標籤？", 360, ax="l")
b.box("b2n", P, 3, NOTE, fl("標籤 = 我們自己產的 <<<<<<< vendor_kit:baseline 等；檔案失蹤不算已解；resolve 只偵測，「清除已解的衝突狀態」在 apply 內、建日誌之後（v2.5 §3）"), 280)
b.box("b5", U, 4, O12, "否 → 1：無 baseline，請先 add <repo>", 220)
b.box("b4", E, 4, D12, "有 baseline/<repo>/？", 340, ax=10)
b.box("b6", E, 5, v2(D12), "(1) 有待合併？", 170, ax="l")
b.box("b6y", E, 6, v2(W12), fl("是：目標版 = B（version.toml 那版），補到就停，不查最新"), 170, ax="r")
b.box("b7a", E, 7, v2(D12), "否 → @<tag> 指定？", 170, ax="l")
b.box("b7t", E, 7, v2(W12), fl("是：目標版 = @<tag>（比現版舊 → warn 仍執行）"), 170, ax="r")
b.box("b7b", E, 8, v2(D12), "否 → CI 為真（frozen）？", 170, ax="l")
b.box("b7z", E, 8, v2(W12), fl("是：不查最新；目標版 = 鎖定版（無事可做）"), 170, ax="r")
b.box("b7c", E, 9, v2(W12), fl("否：(2) 查 registry 最新正式版 = 目標版"), 170, ax="l")
b.box("b7s", E, 10, v2(SUB), fl("resolve 完 → stdout：目標 tag@digest ＋ 輸入指紋（version.toml、metadata、要動的使用者檔 hash、鎖定 digest）"), 360)
b.box("b8a", L, 11, v2(D12), "docker image inspect：本機有？", 170, ax="l")
b.box("b8p", L, 12, v2(W12), "無：docker pull", 70, ax="r")
b.box("b8g", G, 12, IMG, "<repo>-dist\\n目標 tag@digest", 180)
b.box("b8b", L, 13, v2(W12), "docker create <img> /x", 240)
b.box("b8c", L, 14, v2(W12), "docker cp c:/dist/. <tmp>/<repo>/（主機暫存）", 240)
b.box("b8d", L, 15, v2(W12), "docker rm 該容器", 240)
b.box("b8z", L, 16, LBL, "↓ 續「B（1′）」頁：docker run 引擎 apply upgrade → 前置檢查", 240, 24, minh=24)
b.H("be1", "b0", "b0l"); b.D("be1l", "b0l", "b1"); b.H("be1e", "b1", "b1e"); b.D("be1q", "b1e", "b1q", al=True); b.H("be1x", "b1q", "b1x", "是")   # launcher_start／engine_start（v2.12）''')
rep('b.box("b8e", L, 0, ENTRY, "來自「B（1）」頁：目標版 /dist 已在主機暫存", 240)', 'b.box("b8e", L, 0, ENTRY, "來自「B（1）」頁：目標版 /dist 已在主機暫存（已寫 launcher_start）", 240)')
rep('b.box("b10z", E, 0, ENTRY, "來自「B（1′）」頁：apply 檢查通過（非 dry-run）", 300)', 'b.box("b10z", E, 0, ENTRY, "來自「B（1′）」頁：apply 檢查通過（非 dry-run；已寫 launcher_start）", 360)')
rep('b.box("b15z", E, 0, ENTRY, fl("來自「B（2）」頁：通過解析的檔已原子替換；解析失敗的檔留原檔、已記 conflicts"), 300)', 'b.box("b15z", E, 0, ENTRY, fl("來自「B（2）」頁：通過解析的檔已原子替換；解析失敗的檔留原檔、已記 conflicts（已寫 launcher_start）"), 360)')

# ---- C/D 頁：D. 回退「下次 just」----
rep('b.box("d1a", L, 0, W12, "下次 just：docker run 引擎 resolve sync", 240)', 'b.box("d1a", L, 0, W12, "下次 just（已寫 launcher_start）：docker run 引擎 resolve sync", 240)')

# =====================================================================
# dev：d0l／d1e 格，列 +2
# =====================================================================
rep('''b.box("d0", U, 0, G12, "just vendor_kit dev <repo> -p <dir>", 220)
b.box("d1q", L, 0, v2(D12), "<dir>/dist/ 內有 init.toml？", 240, ax="r")   # 不用長字串撐寬 → d0 右緣與菱形左頂點距 ≥ 40（v2.9 §9）
b.box("d1x", U, 1, v2(O12), "否 → 1：<dir>/dist/init.toml 不存在", 220)
b.box("d1m", L, 1, v2(W12), fl("是：準備掛載 -v <dir>/dist:/dist/<repo>:ro（唯讀）"), 200, ax="r")
b.box("d1", L, 2, v2(W12), fl("docker run 引擎 dev <repo> -p <dir>（不經 docker create/cp）"), 200, ax="r")
b.box("d3a", U, 3, O12, "是 → 1：CI 拒絕 dev", 220)
b.box("d2a", E, 3, D12, "CI 為真？", 130, ax="l")
b.box("d2b", E, 3, D12, "已接入 <repo>？", 240, ax="r")
b.box("d3c", U, 4, O12, "否 → 1：dist/ 或 init.toml 不合法", 220)
b.box("d2c", E, 4, D12, "dist 合法？", 180, ax="l")
b.box("d3b", E, 4, O12, "否 → 1：未接入，請先 add <repo>", 190, ax="r")
b.box("d6a", E, 5, v2(SUB), "是：flock 專案目錄（60 秒）", 400)
b.box("d6", E, 6, v2(SUB), fl("寫 version.local.toml：<repo> = \\"path:<dir>\\"（.vendor_kit/.gitignore 已排除它；不碰 .git/info/exclude）"), 400)
b.box("d6f", P, 6, F12, fl("＋version.local.toml（不進 git）：<repo> = \\"path:<dir>\\""), 360)
b.box("d7", E, 7, SUB, "cache/<repo>/ 改為 symlink → <dir>/dist（本機工具 repo 的 dist/，唯讀）", 400)
b.box("d7f", P, 7, F12, "cache/<repo>/ → <dir>/dist（symlink，內容不複製）", 360)
b.box("d7b", E, 8, v2(SUB), fl("寫印記 gen/<repo>.stamp 第一行 = path:<dir>（印記不放在 symlink 裡）"), 400)
b.box("d7bf", P, 8, F12, "gen/<repo>.stamp 第一行：path:<dir>（不進 git）", 360)
b.box("d8", U, 9, v2(G12), "0：之後每次 just 用 <dir>", 220)
b.box("d9", E, 9, v2(RULE), fl("dev 中的工具：sync 跳過它的 materialize／verify，仍檢查 metadata／baseline；upgrade <repo>／remove <repo> → 1 提示先 undev（v2.1 B、v2.5 §6）；不帶 repo 的 upgrade 預檢也會擋"), 300, ax="r")
b.H("de1", "d0", "d1q"); b.DL("de1x", "d1q", "d1x", "否", 0.15); b.D("de1y", "d1q", "d1m", "是", 0.65, 0.5, al=True); b.D("de1m", "d1m", "d1", al=True); b.D("de2", "d1", "d2a")''',
'''b.box("d0", U, 0, G12, "just vendor_kit dev <repo> -p <dir>", 220)
b.box("d0l", L, 0, v2(W12), ''' + LOG_BOX + ''', 220)
b.box("d1q", L, 1, v2(D12), "<dir>/dist/ 內有 init.toml？", 240, ax="r")
b.box("d1x", U, 2, v2(O12), "否 → 1：<dir>/dist/init.toml 不存在", 220)
b.box("d1m", L, 2, v2(W12), fl("是：準備掛載 -v <dir>/dist:/dist/<repo>:ro（唯讀）"), 200, ax="r")
b.box("d1", L, 3, v2(W12), fl("docker run 引擎 dev <repo> -p <dir>（不經 docker create/cp）"), 200, ax="r")
b.box("d1e", E, 3, v2(SUB), ''' + ENG_BOX + ''', 400)
b.box("d3a", U, 4, O12, "是 → 1：CI 拒絕 dev", 220)
b.box("d2a", E, 4, D12, "CI 為真？", 130, ax="l")
b.box("d2b", E, 4, D12, "已接入 <repo>？", 240, ax="r")
b.box("d3c", U, 5, O12, "否 → 1：dist/ 或 init.toml 不合法", 220)
b.box("d2c", E, 5, D12, "dist 合法？", 180, ax="l")
b.box("d3b", E, 5, O12, "否 → 1：未接入，請先 add <repo>", 190, ax="r")
b.box("d6a", E, 6, v2(SUB), "是：flock 專案目錄（60 秒）", 400)
b.box("d6", E, 7, v2(SUB), fl("寫 version.local.toml：<repo> = \\"path:<dir>\\"（.vendor_kit/.gitignore 已排除它；不碰 .git/info/exclude）"), 400)
b.box("d6f", P, 7, F12, fl("＋version.local.toml（不進 git）：<repo> = \\"path:<dir>\\""), 360)
b.box("d7", E, 8, SUB, "cache/<repo>/ 改為 symlink → <dir>/dist（本機工具 repo 的 dist/，唯讀）", 400)
b.box("d7f", P, 8, F12, "cache/<repo>/ → <dir>/dist（symlink，內容不複製）", 360)
b.box("d7b", E, 9, v2(SUB), fl("寫印記 gen/<repo>.stamp 第一行 = path:<dir>（印記不放在 symlink 裡）"), 400)
b.box("d7bf", P, 9, F12, "gen/<repo>.stamp 第一行：path:<dir>（不進 git）", 360)
b.box("d8", U, 10, v2(G12), "0：之後每次 just 用 <dir>", 220)
b.box("d9", E, 10, v2(RULE), fl("dev 中的工具：sync 跳過它的 materialize／verify，仍檢查 metadata／baseline；upgrade <repo>／remove <repo> → 1 提示先 undev（v2.1 B、v2.5 §6）；不帶 repo 的 upgrade 預檢也會擋"), 300, ax="r")
b.H("de1", "d0", "d0l"); b.D("de1l", "d0l", "d1q", al=True); b.DL("de1x", "d1q", "d1x", "否", 0.15); b.D("de1y", "d1q", "d1m", "是", 0.65, 0.5, al=True); b.D("de1m", "d1m", "d1", al=True)   # launcher_start（v2.12）
b.H("de2", "d1", "d1e"); b.D("de2e", "d1e", "d2a", al=True)   # engine_start（v2.12）''')

# ---- dev vendor_kit／undev／undev vendor_kit：入口（啟動器第一格）文字帶過 ----
rep('b.box("v1i", L, 0, v2(W12), fl("docker image inspect <tag> 取 .Id（主機側；本機無此 image → 1；tar 先自己 docker load）"), 280)',
    'b.box("v1i", L, 0, v2(W12), fl("（已寫 launcher_start）docker image inspect <tag> 取 .Id（主機側；本機無此 image → 1；tar 先自己 docker load）"), 280)')
rep('b.box("v6a", L, 7, v2(W12), fl("grep 引擎 ref：version.local.toml 覆寫優先 → 該 tag"), 280)', 'b.box("v6a", L, 7, v2(W12), fl("（已寫 launcher_start）grep 引擎 ref：version.local.toml 覆寫優先 → 該 tag"), 280)')
rep('b.box("u1", L, 0, W12, "docker run 引擎 resolve undev <repo>", 280)', 'b.box("u1", L, 0, v2(W12), "（已寫 launcher_start）docker run 引擎 resolve undev <repo>（引擎先 append engine_start）", 280)')
rep('b.box("w1", L, 0, v2(W12), "docker run 引擎 resolve undev vendor_kit", 280)', 'b.box("w1", L, 0, v2(W12), "（已寫 launcher_start）docker run 引擎 resolve undev vendor_kit（引擎先 append engine_start）", 280)')
rep('b.box("w5a", L, 11, v2(W12), "grep version.toml 第一行取引擎 ref（local 已無覆寫）", 280)', 'b.box("w5a", L, 11, v2(W12), "（已寫 launcher_start）grep version.toml 第一行取引擎 ref（local 已無覆寫）", 280)')

# =====================================================================
# remove(1)：m0l／m1e 格，列 +2；remove(2) 入口文字
# =====================================================================
rep('''b.box("m0", U, 0, G12, "just vendor_kit remove <repo>（-y、--dry-run）", 220)
b.box("m1", L, 0, v2(W12), fl("docker run <引擎> resolve remove <repo>（不經 docker create/cp）"), 280)
b.box("m3", U, 1, G12, "否 → 0：未接入（提示）", 220)
b.box("m2", E, 1, D12, "已接入 <repo>？", 280, ax="l")
b.box("m5", U, 2, O12, "是 → 1：請先 undev <repo>（v2.1 B）", 220)
b.box("m4", E, 2, D12, "有 dev path 覆寫？", 280, ax="l")
b.box("m6", E, 3, v2(SUB), fl("否：resolve（不寫）：讀 metadata（append 過的行、完成標記）"), 400)
b.box("m6b", E, 4, v2(SUB), fl("產生刪除清單：version.toml 行、cache/<repo>/、gen/<repo>.stamp、baseline/<repo>/、gen/tools.just 的 mod? 行"), 400)
b.box("m6c", E, 5, v2(SUB), fl("產生詢問清單：metadata 記的 append 行（有才問）"), 400)
b.box("m6d", E, 6, v2(SUB), fl("產生輸入指紋（version.toml、metadata、要動的使用者檔 hash）→ 計畫＋指紋以 stdout 回啟動器"), 400)
b.box("m8", L, 7, v2(W12), fl("docker run <引擎> apply remove <repo>（--dry-run 原樣轉發）"), 280)
b.box("m9a", E, 7, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("m9b", E, 8, v2(SUB), "重驗指紋", 240, ax="l")
b.box("m9x", E, 8, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("m7cx", U, 9, v2(O12), "是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）", 220)
b.box("m7c", E, 9, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax="l")
b.box("m7y", U, 10, v2(G12), "是 → 0：只印清單（會刪什麼、會問什麼）", 220)
b.box("m7", E, 10, D12, "--dry-run？", 240, ax=50)
b.box("m7z", E, 11, LBL, "否 ↓ 續「remove（2）」頁：建日誌 → 問 append 行 → 刪檔 → 刪日誌", 400, 24, ax="l", minh=24)
b.H("me1", "m0", "m1"); b.D("me2", "m1", "m2"); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)''',
'''b.box("m0", U, 0, G12, "just vendor_kit remove <repo>（-y、--dry-run）", 220)
b.box("m0l", L, 0, v2(W12), ''' + LOG_BOX + ''', 220)
b.box("m1", L, 1, v2(W12), fl("docker run <引擎> resolve remove <repo>（不經 docker create/cp）"), 280)
b.box("m1e", E, 1, v2(SUB), ''' + ENG_BOX + ''', 400)
b.box("m3", U, 2, G12, "否 → 0：未接入（提示）", 220)
b.box("m2", E, 2, D12, "已接入 <repo>？", 280, ax="l")
b.box("m5", U, 3, O12, "是 → 1：請先 undev <repo>（v2.1 B）", 220)
b.box("m4", E, 3, D12, "有 dev path 覆寫？", 280, ax="l")
b.box("m6", E, 4, v2(SUB), fl("否：resolve（不寫）：讀 metadata（append 過的行、完成標記）"), 400)
b.box("m6b", E, 5, v2(SUB), fl("產生刪除清單：version.toml 行、cache/<repo>/、gen/<repo>.stamp、baseline/<repo>/、gen/tools.just 的 mod? 行"), 400)
b.box("m6c", E, 6, v2(SUB), fl("產生詢問清單：metadata 記的 append 行（有才問）"), 400)
b.box("m6d", E, 7, v2(SUB), fl("產生輸入指紋（version.toml、metadata、要動的使用者檔 hash）→ 計畫＋指紋以 stdout 回啟動器"), 400)
b.box("m8", L, 8, v2(W12), fl("docker run <引擎> apply remove <repo>（--dry-run 原樣轉發）"), 280)
b.box("m9a", E, 8, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("m9b", E, 9, v2(SUB), "重驗指紋", 240, ax="l")
b.box("m9x", E, 9, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("m7cx", U, 10, v2(O12), "是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）", 220)
b.box("m7c", E, 10, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax="l")
b.box("m7y", U, 11, v2(G12), "是 → 0：只印清單（會刪什麼、會問什麼）", 220)
b.box("m7", E, 11, D12, "--dry-run？", 240, ax=50)
b.box("m7z", E, 12, LBL, "否 ↓ 續「remove（2）」頁：建日誌 → 問 append 行 → 刪檔 → 刪日誌", 400, 24, ax="l", minh=24)
b.H("me1", "m0", "m0l"); b.D("me1l", "m0l", "m1", al=True); b.H("me1e", "m1", "m1e"); b.D("me2", "m1e", "m2", al=True); b.H("me3", "m2", "m3", "否"); b.D("me4", "m2", "m4", "是", al=True)   # launcher_start／engine_start（v2.12）''')
rep('b.box("m9e", E, 0, ENTRY, "來自「remove（1）」頁：apply 檢查通過（非 dry-run）", 300)', 'b.box("m9e", E, 0, ENTRY, "來自「remove（1）」頁：apply 檢查通過（非 dry-run；已寫 launcher_start）", 300)')
rep('根 .dockerignore 我們加的三行也問後只刪原文相同的"),', '根 .dockerignore 我們加的四行也問後只刪原文相同的"),')

# =====================================================================
# uninstall(1)：x0l／x1e 格，列 +2；x2d 四行
# =====================================================================
rep('''b.box("x0", U, 0, G12, "just vendor_kit uninstall（-y、--dry-run）", 220)
b.box("x1", L, 0, v2(W12), "docker run <引擎> resolve uninstall（不經 docker create/cp）", 280)
b.box("x2x", U, 1, v2(O12), "否 → 1：預檢失敗（dev 中 → 請先 undev；未完成接入 → 請先 add）", 220)
b.box("x2", E, 1, v2(D12), "預檢全部工具通過？", 250, ax="l")
b.box("x2b", E, 2, v2(SUB), fl("是：算每個自產檔的 hash（薄殼、version.toml、gen/、cache/、baseline/；不動任何東西）"), 400)
b.box("x2bb", E, 3, v2(SUB), fl("分類：hash 相符 → 可刪清單；未知或被改的 → 保護清單（之後一律保留並回報）"), 400)
b.box("x2r", P, 3, v2(RULE), fl("保護清單在任何 remove 之前生效（v2.5 §10）；逐工具 remove 走保護模式：清單內的檔跳過"), 360)
b.box("x2c", E, 4, v2(SUB), fl("產生執行計畫：可刪清單＋保護清單（逐工具 remove 的順序）"), 400)
b.box("x2d", E, 5, v2(SUB), fl("產生詢問清單：append 行、根 justfile 那行、根 .dockerignore 三行"), 400)
b.box("x2e", E, 6, v2(SUB), fl("產生輸入指紋（version.toml、各 metadata、要動的使用者檔 hash）→ 計畫＋詢問清單＋指紋以 stdout 回啟動器"), 400)
b.box("x1b", L, 7, v2(W12), fl("docker run <引擎> apply uninstall（--dry-run 原樣轉發）"), 280)
b.box("x4a", E, 7, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("x4b", E, 8, v2(SUB), "重驗指紋", 240, ax="l")
b.box("x4bx", E, 8, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("x3cx", U, 9, v2(O12), "是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）", 220)
b.box("x3c", E, 9, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax="l")
b.box("x3y", U, 10, v2(G12), "是 → 0：只印會刪什麼、會問什麼", 220)
b.box("x3", E, 10, D12, "--dry-run？", 240, ax=50)
b.box("x4z", E, 11, LBL, "否 ↓ 續「uninstall（2）」頁：建日誌 → 逐工具 remove → 刪自產檔 → 根 justfile 那行 → 刪日誌", 400, 24, ax="l", minh=24)
b.H("xe1", "x0", "x1"); b.D("xe2", "x1", "x2"); b.H("xe3", "x2", "x2x", "否")''',
'''b.box("x0", U, 0, G12, "just vendor_kit uninstall（-y、--dry-run）", 220)
b.box("x0l", L, 0, v2(W12), ''' + LOG_BOX + ''', 220)
b.box("x1", L, 1, v2(W12), "docker run <引擎> resolve uninstall（不經 docker create/cp）", 280)
b.box("x1e", E, 1, v2(SUB), ''' + ENG_BOX + ''', 400)
b.box("x2x", U, 2, v2(O12), "否 → 1：預檢失敗（dev 中 → 請先 undev；未完成接入 → 請先 add）", 220)
b.box("x2", E, 2, v2(D12), "預檢全部工具通過？", 250, ax="l")
b.box("x2b", E, 3, v2(SUB), fl("是：算每個自產檔的 hash（薄殼、version.toml、gen/、cache/、baseline/；不動任何東西）"), 400)
b.box("x2bb", E, 4, v2(SUB), fl("分類：hash 相符 → 可刪清單；未知或被改的 → 保護清單（之後一律保留並回報）"), 400)
b.box("x2r", P, 4, v2(RULE), fl("保護清單在任何 remove 之前生效（v2.5 §10）；逐工具 remove 走保護模式：清單內的檔跳過"), 360)
b.box("x2c", E, 5, v2(SUB), fl("產生執行計畫：可刪清單＋保護清單（逐工具 remove 的順序）"), 400)
b.box("x2d", E, 6, v2(SUB), fl("產生詢問清單：append 行、根 justfile 那行、根 .dockerignore 四行"), 400)
b.box("x2e", E, 7, v2(SUB), fl("產生輸入指紋（version.toml、各 metadata、要動的使用者檔 hash）→ 計畫＋詢問清單＋指紋以 stdout 回啟動器"), 400)
b.box("x1b", L, 8, v2(W12), fl("docker run <引擎> apply uninstall（--dry-run 原樣轉發）"), 280)
b.box("x4a", E, 8, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("x4b", E, 9, v2(SUB), "重驗指紋", 240, ax="l")
b.box("x4bx", E, 9, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("x3cx", U, 10, v2(O12), "是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）", 220)
b.box("x3c", E, 10, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax="l")
b.box("x3y", U, 11, v2(G12), "是 → 0：只印會刪什麼、會問什麼", 220)
b.box("x3", E, 11, D12, "--dry-run？", 240, ax=50)
b.box("x4z", E, 12, LBL, "否 ↓ 續「uninstall（2）」頁：建日誌 → 逐工具 remove → 刪自產檔 → 根 justfile 那行 → 刪日誌", 400, 24, ax="l", minh=24)
b.H("xe1", "x0", "x0l"); b.D("xe1l", "x0l", "x1", al=True); b.H("xe1e", "x1", "x1e"); b.D("xe2", "x1e", "x2", al=True); b.H("xe3", "x2", "x2x", "否")   # launcher_start／engine_start（v2.12）''')

open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("patch C ok")
