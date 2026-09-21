"""第十輪 patch 第四段：install(1) ie6n 不再交叉 ie6lf（i4x 移到引擎欄、第一次路徑走左側匯流排）；band 標題一行；s11n 同寬；i4f 清單短名。"""
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:90])
    src = src.replace(old, new)

rep('''b.box("i4e", E, 10, v2(D12), "薄殼已存在？", 260, ax="l")
b.box("i4en", E, 10, v2(W12), "否：第一次 = 全新建", 120, ax="r")
b.box("i4x", U, 11, v2(O12), fl("否 → 1：被改過，列差異不動（git checkout 還原後再跑）"), 220)
b.box("i4q", E, 11, v2(D12), "薄殼 == 上次產物？（首行 hash）", 260, ax="l")''',
'''b.box("i4en", E, 10, v2(W12), "否：第一次 = 全新建", 120, ax="l")
b.box("i4e", E, 10, v2(D12), "薄殼已存在？", 250, ax="r")
b.box("i4x", E, 11, v2(O12), fl("否 → 1：被改過，列差異不動"), 130, ax="l")
b.box("i4q", E, 11, v2(D12), "薄殼 == 上次產物？（首行 hash）", 250, ax="r")''')
rep('b.H("ie5n", "i4e", "i4en", "否"); b.D("ie5y", "i4e", "i4q", "是", al=True); b.H("ie5x", "i4q", "i4x", "否")',
    'b.H("ie5n", "i4e", "i4en", "否"); b.D("ie5y", "i4e", "i4q", "是", al=True); b.H("ie5x", "i4q", "i4x", "否")   # i4x 在引擎欄右（r10：左側留給第一次路徑）')
rep('b.D("ie6", "i4q", "i4l", "是", al=True); b.D("ie6n", "i4en", "i4b", al=True)   # 第一次 = 全新建 → 直接建檔，不再問「第一次？」（r8）',
    'b.D("ie6", "i4q", "i4l", "是", al=True); b.UL("ie6n", "i4en", "i4b", "", busx=560, row=10)   # 第一次 = 全新建 → 走左側匯流排直接建檔，不跨「寫」線（r8／r10）')
rep('b.files("i4f", P, 13, "＋薄殼四檔＋config.toml（進 git）", [".vendor_kit/.gitignore", ".vendor_kit/entry.just", ".vendor_kit/vendor.just", ".vendor_kit/ci/check.sh", ".vendor_kit/config.toml（第一次才建）"], 360, cols=2)',
    'b.files("i4f", P, 13, "＋.vendor_kit/ 薄殼四檔＋config.toml（進 git）", [".gitignore", "entry.just", "vendor.just", "ci/check.sh", "config.toml（第一次才建）"], 360, cols=2)')
rep('b.box("s11n", L, 2, v2(D12), "docker image inspect：本機有？", 280, ax=20)', 'b.box("s11n", L, 2, v2(D12), "docker image inspect：本機有？", 260, ax=20)')
rep('"5b add <repo>[@<tag>]（bootstrap.sh 對每個 -t 呼叫；也可直接打）= launcher_start → engine_start → resolve',
    '"5b add <repo>[@<tag>]（bootstrap.sh 代呼叫或直接打）= launcher_start → engine_start → resolve')
rep('"sync（工具 recipe 的自動前置；CI 為真 → frozen）：第 1 段 = launcher_start → 比對 gen/.stamp（install／upgrade vendor_kit 跳過）→ 快路徑 grep 全相符 → 寫 sync_fast_path、launcher_exit → 0；有差 → inspect → 引擎 resolve sync（「sync（1′）」頁）"',
    '"sync（recipe 自動前置；CI 為真 → frozen）第 1 段：launcher_start → 比對 gen/.stamp（install／upgrade vendor_kit 跳過）→ 快路徑 grep 全相符 → 寫 sync_fast_path、launcher_exit → 0；有差 → 引擎 resolve sync（「sync（1′）」頁）"')
rep('"E(c)（1）upgrade vendor_kit[@<tag>]（單段救援）：launcher_start → grep 第一行 → inspect → pull → 拿鎖、重驗',
    '"E(c)（1）upgrade vendor_kit[@<tag>]：launcher_start → grep 第一行 → inspect／pull → 拿鎖、重驗')
open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("patch 4 ok")
