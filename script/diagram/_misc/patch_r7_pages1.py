p = "disc_v1_b.py"; s = open(p, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:90])
    s = s.replace(old, new)

# ---- 小折修正（菱形入口改頂點後，把上下菱形置中對齊）----
rep('b.box("i5", E, 1, v2(D12), "--no-justfile？", 230, ax="l")', 'b.box("i5", E, 1, v2(D12), "--no-justfile？", 300, ax="l")')
rep('b.box("i6", E, 2, D12, "否 → 有根 justfile？", 230, ax="l")', 'b.box("i6", E, 2, D12, "否 → 有根 justfile？", 300, ax="l")')
rep('b.box("i8", E, 3, v2(D12), "有 → 已含 import 那行？", 240, ax="l")', 'b.box("i8", E, 3, v2(D12), "有 → 已含 import 那行？", 300, ax="l")')
rep('b.box("ig", E, 6, v2(D12), "有根 .dockerignore？", 200, ax="l")', 'b.box("ig", E, 6, v2(D12), "有根 .dockerignore？", 250, ax="l")')
rep('b.box("c4", E, 2, D12, "已接入 <repo>？", 240, ax="l")', 'b.box("c4", E, 2, D12, "已接入 <repo>？", 310, ax="l")')
rep('b.box("c5t", E, 4, D12, "@<tag> 與鎖定不同？", 240, ax="l")', 'b.box("c5t", E, 4, D12, "@<tag> 與鎖定不同？", 220, ax=45)')
rep('b.box("c8", E, 4, W12, fl("否：續作，只做缺的步驟（不補刻意刪的檔）"), 130, ax="r")', 'b.box("c8", E, 4, W12, fl("否：續作，只做缺的步驟（不補刻意刪的檔）"), 120, ax="r")')
rep('b.D("ce7", "c5", "c5t", "是", 0.35, 0.5, al=True)', 'b.D("ce7", "c5", "c5t", "是", 0.5, 0.5, al=True)')
rep('b.box("c14", E, 5, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax="l")', 'b.box("c14", E, 5, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax=30)')
rep('b.box("c13", E, 6, D12, "--dry-run？", 240, ax="l")', 'b.box("c13", E, 6, D12, "--dry-run？", 240, ax=80)')
for i in ("t1", "t2q", "t2"):
    pass
rep('b.box("t1", E, 3, v2(D12), "cache 缺或印記 ≠ 鎖定 digest？", 240, ax="l")', 'b.box("t1", E, 3, v2(D12), "cache 缺或印記 ≠ 鎖定 digest？", 250, ax="l")')
rep('b.box("t2q", E, 4, v2(D12), "否 → sync --verify 或 CI 為真？", 240, ax="l")', 'b.box("t2q", E, 4, v2(D12), "否 → sync --verify 或 CI 為真？", 250, ax="l")')
rep('b.box("t2", E, 5, D12, "是 → verify：每檔 sha256 ＝ 印記？", 240, ax="l")', 'b.box("t2", E, 5, D12, "是 → verify：每檔 sha256 ＝ 印記？", 250, ax="l")')
rep('b.box("t3", E, 6, D12, "metadata 有完成標記？", 310, ax="l")', 'b.box("t3", E, 6, D12, "metadata 有完成標記？", 250, ax="l")')
rep('b.box("t4", E, 7, D12, "最後合併版本 ＝ version.toml？", 260, ax="l")', 'b.box("t4", E, 7, D12, "最後合併版本 ＝ version.toml？", 250, ax="l")')
rep('b.box("t4c", E, 8, D12, "否（落後）→ CI 為真（frozen）？", 300, ax="l")', 'b.box("t4c", E, 8, D12, "否（落後）→ CI 為真（frozen）？", 250, ax="l")')
rep('b.box("b4", E, 3, D12, "有 baseline/<repo>/？", 340, ax="l")', 'b.box("b4", E, 3, D12, "有 baseline/<repo>/？", 340, ax=10)')
rep('b.box("b6", E, 4, v2(D12), "(1) 有待合併？", 220, ax="l")', 'b.box("b6", E, 4, v2(D12), "(1) 有待合併？", 170, ax="l")')
rep('b.box("s2ln", L, 9, v2(D12), "是 → docker image inspect：本機有？", 220, ax=20)', 'b.box("s2ln", L, 9, v2(D12), "是 → docker image inspect：本機有？", 220, ax=50)')
rep('b.box("m2", E, 1, D12, "已接入 <repo>？", 240, ax="l")', 'b.box("m2", E, 1, D12, "已接入 <repo>？", 280, ax="l")')
rep('b.box("m7", E, 10, D12, "--dry-run？", 240, ax="l")', 'b.box("m7", E, 10, D12, "--dry-run？", 240, ax=50)')
rep('b.box("x3", E, 10, D12, "--dry-run？", 240, ax="l")', 'b.box("x3", E, 10, D12, "--dry-run？", 240, ax=50)')

# ---- remove（2）：m9m 三出口標「零／唯一／多處」；m9h～m9m 置中對齊 ----
rep('b.box("m9h", E, 2, v2(D12), "metadata 有 append 過的行？", 240, ax="l")', 'b.box("m9h", E, 2, v2(D12), "metadata 有 append 過的行？", 300, ax=30)')
rep('b.box("m9q", E, 3, v2(D12), fl("有 → 問「要刪我們加在 X 的這幾行嗎」同意？（-y 免問）"), 300, ax="l")', 'b.box("m9q", E, 3, v2(D12), fl("有 → 問「要刪我們加在 X 的這幾行嗎」同意？（-y 免問）"), 300, ax=30)')
rep('b.box("m9s", E, 4, v2(W12), fl("是：找上次插入的行（CRLF／LF 視為相同、其餘精確）"), 200, ax=50)', 'b.box("m9s", E, 4, v2(W12), fl("是：找上次插入的行（CRLF／LF 視為相同、其餘精確）"), 200, ax=80)')
rep('b.box("m9z", E, 5, W12, "零命中：不刪、印清單", 90, ax="l")', 'b.box("m9z", E, 5, W12, "零命中：不刪、印清單", 70, ax="l")')
rep('b.box("m9m", E, 5, v2(D12), "命中幾處？", 160, ax=120)', 'b.box("m9m", E, 5, v2(D12), "命中幾處？", 140, ax=110)')
rep('b.box("m9d", E, 5, W12, "唯一：刪那幾行", 90, ax="r")', 'b.box("m9d", E, 5, W12, "唯一：刪那幾行", 100, ax="r")')
rep('b.box("m9w", E, 6, v2(W12), "多處：保留＋warn", 160, ax=120)', 'b.box("m9w", E, 6, v2(W12), "多處：保留＋warn", 140, ax=110)')
rep('b.H("me13z", "m9m", "m9z"); b.H("me13d", "m9m", "m9d"); b.D("me13w", "m9m", "m9w", al=True)',
    'b.H("me13z", "m9m", "m9z", "零"); b.H("me13d", "m9m", "m9d", "唯一"); b.D("me13w", "m9m", "m9w", "多處", al=True)')

# ---- sync（1′）：ncx 改橙（CI 拒絕 local 覆寫 = 需要人動作）----
rep('b.box("ncx", U, 1, v2(R12), "是 → 1：CI 拒絕本機覆寫（frozen）", 220)', 'b.box("ncx", U, 1, v2(O12), "是 → 1：CI 拒絕本機覆寫（frozen；請先 undev 或勿在 CI 用 local 覆寫）", 220)')

# ---- Renovate：a6c 拆 commit／push ----
rep('''b.box("a6c", U, 9, W12, "commit、push", 220)
b.box("a7", L, 9, W12, "PR 分支 CI 再跑完整流程（同上）→ 綠", 150, ax="l")
b.box("a8", RN, 10, G12, "merge PR（CI 綠後才 merge）", 180)''',
'''b.box("a6c", U, 9, W12, "commit（合併結果）", 220)
b.box("a6d", U, 10, W12, "push 到 PR 分支", 220)
b.box("a7", L, 10, W12, "PR 分支 CI 再跑完整流程（同上）→ 綠", 150, ax="l")
b.box("a8", RN, 11, G12, "merge PR（CI 綠後才 merge）", 180)''')
rep('b.D("ae6c", "a6b", "a6c"); b.H("ae7", "a6c", "a7")', 'b.D("ae6c", "a6b", "a6c"); b.D("ae6d", "a6c", "a6d"); b.H("ae7", "a6d", "a7")')

# ---- 逐檔判斷：cx0／cx1／cx2 中心對齊 ----
rep('''b.free("cx0", G12, "解完衝突後再跑 upgrade <repo>", 20, cy2 + 40, 220, 58)
b.free("cx1", v2(D12), "衝突檔仍含我們的標籤？", 730, cy2 + 35, 340, 50)
b.free("cx2", O12, "是 → 2：停（先解完標記再重跑）", 1100, cy2 + 36, 200, 58)''',
'''_cxc = cy2 + 69                                                                     # 三格中心同高（review r6：cx_e0／cx_e1 不再有小折）
_h0, _h1, _h2 = fit_h("解完衝突後再跑 upgrade <repo>", 220, 58, 0, G12), fit_h("衝突檔仍含我們的標籤？", 340, 50, 0, D12), fit_h("是 → 2：停（先解完標記再重跑）", 200, 58, 0, O12)
b.free("cx0", G12, "解完衝突後再跑 upgrade <repo>", 20, _cxc - _h0 / 2, 220, _h0)
b.free("cx1", v2(D12), "衝突檔仍含我們的標籤？", 730, _cxc - _h1 / 2, 340, _h1)
b.free("cx2", O12, "是 → 2：停（先解完標記再重跑）", 1100, _cxc - _h2 / 2, 200, _h2)''')

# ---- add（1）：cfe 兩框中心對齊 ----
rep('''b.free_files("cf0", "add 前（install 後）", ["justfile（＋import 行）", ".dockerignore（＋三行）", "version.toml（vendor_kit 行）", "version.local.toml（--local 時）", "薄殼四檔：.gitignore、entry.just、vendor.just、ci/check.sh", "gen/.stamp", "baseline/.gitkeep"], 1220, 72, 170)
b.free_files("cf1", "add 後（＋ = 新增）", ["＋version.toml [tools] <repo> 行", "＋cache/<repo>/（不進 git：files/、init.toml、just/）", "＋gen/<repo>.stamp", "＋初始檔（init.toml 的 dest；append 問後加）", "＋baseline/<repo>/ + .vendor_kit.toml", "＋gen/tools.just（每個 <ns>.just 一行 mod?）"], 1410, 72, 170)''',
'''_cf0 = ["justfile（＋import 行）", ".dockerignore（＋三行）", "version.toml（vendor_kit 行）", "version.local.toml（--local 時）", "薄殼四檔：.gitignore、entry.just、vendor.just、ci/check.sh", "gen/.stamp", "baseline/.gitkeep"]
_cf1 = ["＋version.toml [tools] <repo> 行", "＋cache/<repo>/（不進 git：files/、init.toml、just/）", "＋gen/<repo>.stamp", "＋初始檔（init.toml 的 dest；append 問後加）", "＋baseline/<repo>/ + .vendor_kit.toml", "＋gen/tools.just（每個 <ns>.just 一行 mod?）"]
def _fh(items, w): return 26 + sum(fit_h(t, w - 16, 26) for t in items) + 6 * len(items) + 4
_h0, _h1 = _fh(_cf0, 170), _fh(_cf1, 170); _cy = 72 + max(_h0, _h1) / 2          # 兩容器中心同高（review r6：cfe 不再有小折）
b.free_files("cf0", "add 前（install 後）", _cf0, 1220, round(_cy - _h0 / 2), 170)
b.free_files("cf1", "add 後（＋ = 新增）", _cf1, 1410, round(_cy - _h1 / 2), 170)''')

# ---- dev <repo>：d0 與 d1q 留 ≥ 40px（de1 看得到箭頭）----
rep('b.box("d1q", L, 0, v2(D12), "<dir>/dist/init.toml 存在？", 260)', 'b.box("d1q", L, 0, v2(D12), "<dir>/dist/init.toml 存在？", 240, ax="r")')

# ---- dev vendor_kit：inspect 移到啟動器泳道，image ID 交引擎；v2x 改橙 ----
rep('''b.box("v1", L, 0, v2(W12), "docker run 引擎 dev vendor_kit -i <tag>\\n（tar 先自己 docker load）", 280)
b.box("v2x", U, 1, R12, "是 → 1：CI 拒絕 dev", 220)
b.box("v2q", E, 1, D12, "CI 為真？", 130, ax="l")
b.box("v2a", E, 2, v2(SUB), "否：flock 專案目錄（60 秒）", 400)
b.box("v2b", E, 3, v2(SUB), fl("寫 version.local.toml：vendor_kit = \\"<tag>\\"（不動薄殼）"), 400)
b.box("v3", P, 3, F12, "＋version.local.toml：vendor_kit = \\"<tag>\\"（不進 git）", 360)
b.box("v2c", E, 4, v2(SUB), fl("寫 version.local.toml：vendor_kit_image_id = docker image inspect <tag> 的 .Id"), 400)
b.box("v3c", P, 4, F12, "version.local.toml：＋vendor_kit_image_id 行（同 tag 重 build 才會被發現）", 360)
b.box("v2z", U, 4, v2(G12), "0：之後每次 just 用該本機 image", 220)
b.box("v5", U, 6, G12, "下次打任何 just", 220)
b.box("v6a", L, 6, v2(W12), fl("grep 引擎 ref：version.local.toml 覆寫優先 → 該 tag"), 280)
b.box("vb", L, 5, LBL, "═══ 下次 just（改用該本機 image；啟動器先比對 gen/.stamp 再起容器）═══", 560, 24, ax="l", minh=24)
b.box("v8", U, 7, v2(O12), fl("否 → 1：「vendor_kit 已更新，請執行：just vendor_kit upgrade vendor_kit」"), 220)
b.box("v7", L, 7, v2(D12), "gen/.stamp 的引擎 ref == 該 tag？", 270)
b.box("v9", U, 8, v2(G12), "→ 打 upgrade vendor_kit（「E(c) upgrade vendor_kit」頁）", 220)
b.box("v6b", L, 8, v2(D12), fl("是：docker image inspect <tag> 的 .Id == 記的 image ID？"), 270)
b.box("v6x", E, 8, v2(R12), fl("否 → 1：本機 image 已變（同 tag 重 build）或不存在"), 240, ax="l")
b.box("v6c", L, 9, v2(W12), fl("是：docker run <tag> resolve sync（不 pull）"), 280)
b.box("v10", E, 9, G12, "0：正常跑（用該本機 image）", 240, ax="l")
b.H("ve1", "v0", "v1"); b.D("ve2", "v1", "v2q"); b.H("ve3", "v2q", "v2x", "是"); b.D("ve4", "v2q", "v2a", "否", al=True); b.D("ve4b", "v2a", "v2b"); b.H("ve5", "v2b", "v3", "寫")''',
'''b.box("v1i", L, 0, v2(W12), fl("docker image inspect <tag> 取 .Id（主機側；本機無此 image → 1；tar 先自己 docker load）"), 280)
b.box("v1", L, 1, v2(W12), fl("docker run 引擎 dev vendor_kit -i <tag>，image ID 一併交給引擎（引擎容器內不呼叫 docker）"), 280)
b.box("v2x", U, 2, v2(O12), "是 → 1：CI 拒絕 dev（請在本機執行）", 220)
b.box("v2q", E, 2, D12, "CI 為真？", 130, ax="l")
b.box("v2a", E, 3, v2(SUB), "否：flock 專案目錄（60 秒）", 400)
b.box("v2b", E, 4, v2(SUB), fl("寫 version.local.toml：vendor_kit = \\"<tag>\\"（不動薄殼）"), 400)
b.box("v3", P, 4, F12, "＋version.local.toml：vendor_kit = \\"<tag>\\"（不進 git）", 360)
b.box("v2c", E, 5, v2(SUB), fl("寫 version.local.toml：vendor_kit_image_id = 啟動器交來的 image ID"), 400)
b.box("v3c", P, 5, F12, "version.local.toml：＋vendor_kit_image_id 行（同 tag 重 build 才會被發現）", 360)
b.box("v2z", U, 5, v2(G12), "0：之後每次 just 用該本機 image", 220)
b.box("v5", U, 7, G12, "下次打任何 just", 220)
b.box("v6a", L, 7, v2(W12), fl("grep 引擎 ref：version.local.toml 覆寫優先 → 該 tag"), 280)
b.box("vb", L, 6, LBL, "═══ 下次 just（改用該本機 image；啟動器先比對 gen/.stamp 再起容器）═══", 560, 24, ax="l", minh=24)
b.box("v8", U, 8, v2(O12), fl("否 → 1：「vendor_kit 已更新，請執行：just vendor_kit upgrade vendor_kit」"), 220)
b.box("v7", L, 8, v2(D12), "gen/.stamp 的引擎 ref == 該 tag？", 270)
b.box("v9", U, 9, v2(G12), "→ 打 upgrade vendor_kit（「E(c) upgrade vendor_kit」頁）", 220)
b.box("v6b", L, 9, v2(D12), fl("是：docker image inspect <tag> 的 .Id == 記的 image ID？"), 270)
b.box("v6x", E, 9, v2(R12), fl("否 → 1：本機 image 已變（同 tag 重 build）或不存在"), 240, ax="l")
b.box("v6c", L, 10, v2(W12), fl("是：docker run <tag> resolve sync（不 pull）"), 280)
b.box("v10", E, 10, G12, "0：正常跑（用該本機 image）", 240, ax="l")
b.H("ve1", "v0", "v1i"); b.D("ve1i", "v1i", "v1"); b.D("ve2", "v1", "v2q"); b.H("ve3", "v2q", "v2x", "是"); b.D("ve4", "v2q", "v2a", "否", al=True); b.D("ve4b", "v2a", "v2b"); b.H("ve5", "v2b", "v3", "寫")''')
rep('b = F.band("vI", "dev vendor_kit -i <本機 image tag>：引擎 tag 覆寫（v2.1 B／v2.2 B）—— 只能 tag：docker load 後無 RepoDigests（實測），另記 image ID；驗收測試用同一機制", v2=True)',
    'b = F.band("vI", "dev vendor_kit -i <本機 image tag>：引擎 tag 覆寫（v2.1 B／v2.2 B）—— 只能 tag：docker load 後無 RepoDigests（實測），另記 image ID（由啟動器 docker image inspect 取得後交給引擎，v2.8 §6）；驗收測試用同一機制", v2=True)')
open(p, "w", encoding="utf-8").write(s); print("ok")
