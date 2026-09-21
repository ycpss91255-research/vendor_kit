src = open("gen27.py").read()
def rep(a, b):
    global src; assert src.count(a) == 1, a[:60]; src = src.replace(a, b)
# 第 7 頁：兩棵小樹檔名欄加寬；名詞表 key 溢出
rep('tree("tl", "r_tool", 20, 50, 240, 480, TL)', 'tree("tl", "r_tool", 20, 50, 300, 420, TL)')
rep('tree("pj", "r_proj", 20, 50, 240, 480, PJ)', 'tree("pj", "r_proj", 20, 50, 300, 420, PJ)')
rep(' ("smoke / lint / unit / integration / system / acceptance", "測試層級，分別 = 環境能跑／不執行的檢查／單一模組／一個子命令走到底／整個 image／真的打 just（第 8 頁）"),',
    ' ("測試層級名稱", "smoke = 環境能跑；lint = 不執行的檢查；unit = 單一模組；integration = 一個子命令走到底；system = 整個 image；acceptance = 真的打 just（第 8 頁）"),')
open("gen28.py", "w").write(src); print("ok")

# ---- 第 8 頁：列距重排讓 FROM 標籤有空間；去掉壓到標題的 d_note ----
src = open("gen28.py").read()
rep('p8.append(v("repo", "1", SW(RED), "vendor_kit repo", 40, 70, 420, COLH))', 'p8.append(v("repo", "1", SW(RED), "vendor_kit repo（只列跟測試有關的；完整見第 7 頁）", 40, 70, 420, COLH))')
rep('p8.append(v("d_note", "repo", TEXT(11), "完整資料夾架構見第 7 頁；這裡只列跟測試有關的", 20, 30, 380, 18))\n', '')
rep('COLH = 1080\n# 欄 1：repo 目錄', 'COLH = 1100\n# 欄 1：repo 目錄')
rep('"test/（先分測試工具、再分層級）", 20, 200, 380, 681))', '"test/（先分測試工具、再分層級）", 20, 200, 380, 703))')
rep('"env/check.sh\\n環境檢查：image 內 python3、tomllib、vendor_kit 進入點、toml-bridge", 12, 45, TW, 44)', '"env/check.sh\\n環境檢查：Python、tomllib、進入點、toml-bridge 都能跑", 12, 45, TW, 44)')
rep('"fixtures/\\n假的 dist/、init.toml、VERSION、假專案", 12, 100, TW, 44))', '"fixtures/\\n假的 dist/、init.toml、VERSION、假專案", 12, 110, TW, 44))')
for tid, y0 in [("t_lint", 185), ("t_unit", 240), ("t_inst", 295), ("t_init", 350), ("t_ver", 405), ("t_diff", 460), ("t_sys", 515), ("t_acc", 570), ("t_conf", 625)]:
    import re
    m = re.search(r'(p8\.append\(v\("%s", "d_test", LEAF\(\), ".*?", 12, )%d(, TW, 44\))' % (tid, y0), src)
    assert m, tid
    src = src[:m.start()] + m.group(1) + str(y0 + 22) + m.group(2) + src[m.end():]
rep('"Dockerfile（中欄的 stage）", 20, 900, 180, 40))', '"Dockerfile（中欄的 stage）", 20, 920, 180, 40))')
rep('"docker-bake.hcl（group）", 220, 900, 180, 40))', '"docker-bake.hcl（group）", 220, 920, 180, 40))')
rep('"doc/adr/\\n測試分層與閘門（本頁的決策）", 20, 960, 380, 44))', '"doc/adr/\\n測試分層與閘門（本頁的決策）", 20, 980, 380, 44))')
rep('bake validate → system/acceptance → bake release", 20, 1016, 380, 44))', 'bake validate → system/acceptance → bake release", 20, 1036, 380, 44))')
rep('"test-base = env-test + pytest + fixtures", LX, 302, LW, 40)', '"test-base = env-test + pytest + fixtures", LX, 312, LW, 40)')
rep('GY = 350\n', 'GY = 372\n')
rep('"release\\n= runtime（最終產物）", LX + 20, 740, LW, 50))', '"release\\n= runtime（最終產物）", LX + 20, 760, LW, 50))')
rep('"release-test\\nFROM release；真的 install + verify 一次", LX + 20, 830, LW, 60))', '"release-test\\nFROM release；真的 install + verify 一次", LX + 20, 850, LW, 60))')
rep('它們要 docker run，所以在 CI 主機上跑", 20, 905, 440, 40))', '它們要 docker run，所以在 CI 主機上跑", 20, 925, 440, 40))')
rep('group release = [release, release-test]", 20, 950, 440, 40))', 'group release = [release, release-test]", 20, 965, 440, 40))')
rep('<mxPoint x="475" y="75"/><mxPoint x="475" y="765"/>', '<mxPoint x="475" y="75"/><mxPoint x="475" y="785"/>')
rep('p8.append(e("s1b", "s_env", "s_tb", "FROM（環境不對就到此為止）", (0.5, 1), (0.5, 0), vert=True))', 'p8.append(e("s1b", "s_env", "s_tb", "FROM（環境不對 → 到此為止）", (0.5, 1), (0.5, 0), vert=True))')
open("gen28.py", "w").write(src); print("ok2")

# ---- 第 8 頁：標題溢出、閘門框字擠 ----
src = open("gen28.py").read()
rep('"vendor_kit repo（只列跟測試有關的；完整見第 7 頁）", 40, 70, 420, COLH))', '"vendor_kit repo（測試相關）", 40, 70, 420, COLH))\np8.append(v("d_note", "repo", TEXT(11), "完整資料夾架構見第 7 頁", 20, 1090, 380, 18))')
rep('COLH = 1100\n# 欄 1：repo 目錄', 'COLH = 1130\n# 欄 1：repo 目錄')
rep('''    h = 30 + len(gates) * 60 + 10
    p8.append(v(gid, "gates", GSW, title, 20, y, 420, h))
    for i, (k, t) in enumerate(gates):
        p8.append(v(k, gid, LEAF().replace("fontSize=14", "fontSize=12"), t, 10, 40 + i * 60, 400, 50))''',
'''    h = 30 + len(gates) * 64 + 10
    p8.append(v(gid, "gates", GSW, title, 20, y, 420, h))
    for i, (k, t) in enumerate(gates):
        p8.append(v(k, gid, LEAF().replace("fontSize=14", "fontSize=12"), t, 10, 40 + i * 64, 400, 56))''')
rep('("g0", "環境檢查先於一切\\ntest-base FROM env-test：python3、tomllib、vendor_kit 進入點、toml-bridge 任一不對，六個測試 stage 都不會跑")',
    '("g0", "環境檢查先於一切\\ntest-base FROM env-test：Python、tomllib、進入點、toml-bridge 任一不對，六個測試 stage 都不會跑")')
open("gen28.py", "w").write(src); print("ok3")
