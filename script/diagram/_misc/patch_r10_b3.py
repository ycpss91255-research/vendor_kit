"""第十輪 patch 第三段：頁高 ≤ 2400（名詞表三條壓到 3+1+1 行；菱形／橢圓文字精簡；檔案清單一行一檔精簡）＋ 檢查修正。"""
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:90])
    src = src.replace(old, new)

# ---- 名詞表三條壓行 ----
rep(''' ("操作紀錄檔／log（v2.12）", ".vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，每次執行一檔（JSON Lines：timestamp、event_name、body、trace_id、attributes）；啟動器先建檔並寫 launcher_start 才動手，引擎 resolve 前 append engine_start（皆失敗 → 1 + 6-38）；印到 tty 的訊息同句進 body；結束時 prune（最近 30 天且最多 50 檔）；不進 git、不進 image"),
 ("config.toml（v2.12）", ".vendor_kit/config.toml（進 git）：schema = 1、[log] keep = 50、days = 30；install 第一次建（含註解與預設值），upgrade 三方合併；缺檔／缺鍵 = 預設，非正整數 → 預設 + 警告"),
 ("6-38", "log 檔建不了或寫不進（launcher_start／engine_start 失敗）→ 1，零寫入、不進 resolve；附清空間提示；所有動詞一致（含 help），無 --no-log"),''',
''' ("操作紀錄檔／log（v2.12）", ".vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，每次執行一檔（JSON Lines：timestamp、event_name、body、trace_id…）；啟動器先建檔寫 launcher_start、引擎 resolve 前 append engine_start（失敗 → 1 + 6-38）；tty 訊息同句進 body；結束時 prune（30 天／50 檔）；不進 git"),
 ("config.toml（v2.12）", ".vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解），upgrade 三方合併；缺 = 預設"),
 ("6-38", "log 檔建不了／寫不進 → 1，零寫入、不進 resolve；附清空間提示；所有動詞一致，無 --no-log"),''')

# ---- band 標題一行 ----
rep('"5a′ install：專案層動詞（bootstrap.sh 代打，也可自己打）；launcher_start → engine_start → 產薄殼四檔＋config.toml；再跑 = 引擎重寫薄殼（先比對首行自描述 hash）= 冪等修復；第一次不建日誌、修復型建 .tmp.install.<id>.toml（v2.8 §2）；禁止巢狀（Q20）"',
    '"5a′ install（bootstrap.sh 代打或自己打）：launcher_start → engine_start → 產薄殼四檔＋config.toml；再跑 = 引擎重寫薄殼（比對首行自描述 hash）= 冪等修復；第一次不建日誌、修復型建 .tmp.install（v2.8 §2）；禁止巢狀（Q20）"')
rep('"5b add <repo>[@<tag>]（bootstrap.sh 對每個 -t 呼叫；使用者也直接打）= launcher_start → engine_start → 引擎 resolve（不寫；私有 image 未指定 @<tag> 且無憑證 → 1 + 6-3）→ 啟動器 docker（inspect → 無才 pull → create → cp → rm）；續「add（1′）」「add（2）」頁"',
    '"5b add <repo>[@<tag>]（bootstrap.sh 對每個 -t 呼叫；也可直接打）= launcher_start → engine_start → resolve（不寫；私有 image 未指定 @<tag> 且無憑證 → 1 + 6-3）→ 啟動器 docker（inspect → pull → create → cp → rm）；續「add（1′）」「add（2）」頁"')
rep('"sync（工具 recipe 的自動前置；CI 為真 → frozen）：第 1 段 = launcher_start → 啟動器比對 gen/.stamp（install／upgrade vendor_kit 跳過）→ 快路徑 grep 全相符 → 寫 sync_fast_path、launcher_exit → 0 不起容器；有差 → inspect → 引擎 resolve sync（見「sync（1′）」頁）"',
    '"sync（工具 recipe 的自動前置；CI 為真 → frozen）：第 1 段 = launcher_start → 比對 gen/.stamp（install／upgrade vendor_kit 跳過）→ 快路徑 grep 全相符 → 寫 sync_fast_path、launcher_exit → 0；有差 → inspect → 引擎 resolve sync（「sync（1′）」頁）"')
rep('"E(c)（1）upgrade vendor_kit[@<tag>]（單段救援）：launcher_start → grep 第一行 → inspect → pull → 拿鎖、重驗 → 薄殼 == 上次產物？→ @舊版無法無損讀 → 3 → frozen 不查／@<tag>／查 registry → 目標 ≠ 現 ref → 建日誌 → 改第一行 → 新引擎再跑；否則見「E(c)（2）」頁"',
    '"E(c)（1）upgrade vendor_kit[@<tag>]（單段救援）：launcher_start → grep 第一行 → inspect → pull → 拿鎖、重驗 → 薄殼 == 上次產物？→ @舊版無法無損讀 → 3 → frozen／@<tag>／查 registry → 目標 ≠ 現 ref → 建日誌 → 改第一行 → 新引擎再跑；否則「E(c)（2）」頁"')

# ---- bootstrap(1)：頁高 ----
rep('b.box("a1", L, 1, D12, "是 git repo？", 200)', 'b.box("a1", L, 1, D12, "是 git repo？", 220)')
rep('b.box("a3", L, 2, D12, "just ≥ 1.33.0？", 200)', 'b.box("a3", L, 2, D12, "just ≥ 1.33.0？", 240)')
rep('b.box("a5", L, 5, D12, "--local？", 140)', 'b.box("a5", L, 5, D12, "--local？", 160)')
rep('b.box("a8ex", U, 7, v2(O12), "否 → 1：--local 指定的檔案不存在（請檢查路徑）", 220)', 'b.box("a8ex", U, 7, v2(O12), "否 → 1：--local 檔案不存在（請檢查路徑）", 220)')
rep('b.box("a8tx", U, 8, v2(O12), fl("是 → 1：印 6-37（值既是既存檔案也可解讀為本機 image tag，請消歧）"), 220)', 'b.box("a8tx", U, 8, v2(O12), fl("是 → 1：印 6-37（既是檔案也是本機 image tag，請消歧）"), 220)')
rep('b.files("a9f", P, 12, "install 寫（見「install（1）（2）」頁）", [".vendor_kit/ 薄殼四檔（首行自描述）", "version.toml 第一行（引擎 ref）", "gen/.stamp（引擎 ref）", "baseline/.gitkeep", "config.toml（註解＋預設 keep=50／days=30）", "根 justfile（無 → import 行 + default recipe；有 → 加 import 一行）", "根 .dockerignore 四行（含 log/；有 → 問後加）"], 360, cols=2)',
    'b.files("a9f", P, 12, "install 寫（見「install（1）（2）」頁）", [".vendor_kit/ 薄殼四檔", "version.toml 第一行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep", "config.toml（含預設值）", "根 justfile（加 import 行）", "根 .dockerignore 四行"], 360, cols=2)')
rep('b.box("a9x", U, 13, v2(R12), "是 → 1：中止（第一次不留半成品；--local 檔未寫）", 220)\nb.box("a9q", L, 13, D12, "install 失敗？", 200)',
    'b.box("a9x", U, 13, v2(R12), "是 → 1：中止（不留半成品；--local 檔未寫）", 220)\nb.box("a9q", L, 13, D12, "install 失敗？", 220)')

# ---- install(1)：頁高＋ie5y 小折（i4e／i4q 同寬 260）----
rep('b.box("i0", U, 0, G12, "just vendor_kit install（-y、--no-justfile）", 220)', 'b.box("i0", U, 0, G12, "just vendor_kit install（-y…）", 220)')
rep('b.box("i2x", U, 3, v2(O12), fl("是 → 1：<dir> 已有 .vendor_kit/，不允許巢狀；請到該目錄執行或先 uninstall"), 220)', 'b.box("i2x", U, 3, v2(O12), fl("是 → 1：不允許巢狀（<dir> 已有 .vendor_kit/）"), 220)')
rep('b.box("i2n", E, 3, v2(D12), fl("上層或下層已有 .vendor_kit/？（禁止巢狀，Q20）"), 340, ax="l")', 'b.box("i2n", E, 3, v2(D12), fl("上層或下層已有 .vendor_kit/？（禁止巢狀，Q20）"), 400, ax="l")')
rep('b.box("i4n", P, 5, NOTE, fl("第一次 install（薄殼不存在）：不建進度日誌，任一步失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔 → 1（v2.2 C）；修復型 install：建 .tmp.install.<id>.toml 進度日誌（第一個寫入前），失敗 → 1 列已完成／未完成，收尾後刪（v2.8 §2）"), 360)',
    'b.box("i4n", P, 5, NOTE, fl("第一次 install（薄殼不存在）：不建進度日誌，任一步失敗 → 丟棄暫存、移除已寫的檔 → 1（不留半成品，v2.2 C）；修復型：建 .tmp.install.<id>.toml 日誌（第一個寫入前），失敗 → 1 列已完成／未完成，收尾後刪（v2.8 §2）"), 360)')
rep('b.box("i4e", E, 10, v2(D12), "薄殼已存在？", 240, ax="l")\nb.box("i4en", E, 10, v2(W12), "否：第一次 = 全新建", 130, ax="r")',
    'b.box("i4e", E, 10, v2(D12), "薄殼已存在？", 260, ax="l")\nb.box("i4en", E, 10, v2(W12), "否：第一次 = 全新建", 120, ax="r")')
rep('b.box("i4q", E, 11, v2(D12), "薄殼 == 上次產物？（首行自描述 hash）", 300, ax="l")', 'b.box("i4q", E, 11, v2(D12), "薄殼 == 上次產物？（首行 hash）", 260, ax="l")')
rep('b.files("i4f", P, 13, "＋薄殼四檔＋config.toml（進 git）", [".vendor_kit/.gitignore", ".vendor_kit/entry.just", ".vendor_kit/vendor.just", ".vendor_kit/ci/check.sh", ".vendor_kit/config.toml（第一次才建；註解＋預設 keep=50／days=30）"], 360)',
    'b.files("i4f", P, 13, "＋薄殼四檔＋config.toml（進 git）", [".vendor_kit/.gitignore", ".vendor_kit/entry.just", ".vendor_kit/vendor.just", ".vendor_kit/ci/check.sh", ".vendor_kit/config.toml（第一次才建）"], 360, cols=2)')

# ---- sync(1′)：頁高 ----
rep('b.box("n1e", E, 0, ENTRY, "來自「sync（1）」頁：docker run <引擎> resolve sync（已寫 launcher_start；已 append engine_start）", 300)',
    'b.box("n1e", E, 0, ENTRY, "來自「sync（1）」頁：docker run <引擎> resolve sync（已寫 launcher_start、engine_start）", 400)')
rep('b.box("ncx", U, 1, v2(O12), "是 → 1：CI 拒絕本機覆寫（frozen；請先 undev 或勿在 CI 用 local 覆寫）", 220)', 'b.box("ncx", U, 1, v2(O12), "是 → 1：CI 拒絕本機覆寫（frozen；請先 undev）", 220)')
rep('b.box("t2q", E, 4, v2(D12), fl("否 → sync --verify、CI 為真、版本變動那次？"), 250, ax="l")   # §3.6、v2.9 §3', 'b.box("t2q", E, 4, v2(D12), fl("否 → --verify／CI／版本變動那次？"), 250, ax="l")   # §3.6、v2.9 §3')
rep('b.box("t2", E, 5, D12, "是 → verify：每檔 sha256 ＝ 印記？", 250, ax="l")', 'b.box("t2", E, 5, D12, "是 → 每檔 sha256 ＝ 印記？", 250, ax="l")')
rep('b.box("t3a", U, 6, O12, fl("否 → 1：「<repo> 未完成接入，請執行：just vendor_kit add <repo>」"), 220)', 'b.box("t3a", U, 6, O12, fl("否 → 1：<repo> 未完成接入，請先 add <repo>"), 220)')
rep('b.box("t4r", U, 8, O12, fl("是 → 1：baseline 落後，印「請在本機 upgrade <repo> -y 後 commit 並 push」"), 220)', 'b.box("t4r", U, 8, O12, fl("是 → 1：baseline 落後（請在本機 upgrade <repo> -y 後 push）"), 220)')

# ---- B(1)：頁高 ----
rep('b.box("b0", U, 0, G12, "just vendor_kit upgrade <repo>[@<tag>]（-y、--dry-run）", 220)', 'b.box("b0", U, 0, G12, "just vendor_kit upgrade <repo>[@<tag>]（-y…）", 220)')
rep('b.box("b7a", E, 7, v2(D12), "否 → @<tag> 指定？", 170, ax="l")', 'b.box("b7a", E, 7, v2(D12), "否 → 指定 @<tag>？", 170, ax="l")')
rep('b.box("b7b", E, 8, v2(D12), "否 → CI 為真（frozen）？", 170, ax="l")', 'b.box("b7b", E, 8, v2(D12), "否 → CI 為真？", 170, ax="l")')
rep('b.box("b8a", L, 11, v2(D12), "docker image inspect：本機有？", 170, ax="l")', 'b.box("b8a", L, 11, v2(D12), "inspect：本機有？", 170, ax="l")')

# ---- B(2)：頁高 ----
rep('b.box("b14q1b", E, 7, v2(D12), fl("二進位／symlink：你沒改、新版改了 → 問「X 是二進位檔，要換成新版嗎？」"), 240, ax=0)', 'b.box("b14q1b", E, 7, v2(D12), fl("二進位／symlink 你沒改、新版改了 → 問「是二進位檔，換新版？」"), 240, ax=0)')
rep('b.box("b14q2", E, 8, v2(D12), fl("兩邊都改 → 問「你和新版都改了 X，要三方合併嗎？」"), 240, ax=0)', 'b.box("b14q2", E, 8, v2(D12), fl("兩邊都改 → 問「都改了 X，要三方合併嗎？」"), 240, ax=0)')
rep('新檔（B 無）被拒 → state=declined 從未建立；之後不再問；dry-run／check.sh 印「有 N 個範本你拒絕過」；dest 在 CI 路徑（.github/workflows/、.gitlab-ci.yml）時訊息醒目"), 280)',
    '新檔（B 無）被拒 → state=declined；之後不再問；dry-run／check.sh 印「有 N 個範本你拒絕過」；dest 在 CI 路徑時訊息醒目"), 280)')

# ---- uninstall(2)：頁高 ----
rep('b.box("x6", E, 9, D12, "根 justfile 有我們那一行（完全相同）？", 260, ax="r")', 'b.box("x6", E, 9, D12, "根 justfile 有我們那一行？", 260, ax="r")')
rep('b.box("x7", E, 10, v2(D12), "有 → 問「要刪這一行嗎」？（-y 免問）", 260, ax="r")', 'b.box("x7", E, 10, v2(D12), "有 → 問「要刪這一行嗎」？", 260, ax="r")')
rep('b.box("x9q", E, 14, v2(D12), fl("有 → 問「要刪這幾行嗎」？（-y 免問）"), 260, ax=120)', 'b.box("x9q", E, 14, v2(D12), fl("有 → 問「要刪這幾行嗎」？"), 260, ax=120)')

# ---- E(c)(1)：se11px 壓到 s11v 的 v2 標籤 → s11v 寬 260 ----
rep('b.box("s11v", L, 4, v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？"), 280, ax=20)', 'b.box("s11v", L, 4, v2(D12), fl("覆寫中且 .Id ≠ 記的 image ID？"), 260, ax=20)')

open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("patch 3 ok")
