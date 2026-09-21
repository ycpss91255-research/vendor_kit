"""第十一輪 patch 9：termcov（6-24／6-31、6-22、Renovate、gen/.stamp）只加在用到的頁；remove(2) m9m 拆兩菱形；bootstrap(1) a9f 一行一檔。"""
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:90])
    src = src.replace(old, new)
rep('''E33_T = (''', '''PULLX_T = ("6-24／6-31（pull 失敗）", "docker pull 失敗 → 1 + 6-24（原文 + 網路／認證／不存在／主機錯誤分類；bootstrap／add 另附「離線可用：--local <tar>」）；pull 逾時 → 1 + 6-31（--timeout <秒> 或 VENDOR_KIT_PULL_TIMEOUT 調整）")
E22_T = ("6-22（upgrade 逐檔問句）", "「<X> 換成新版？」／「你和新版都改了 <X>，要三方合併嗎？」／「要建 <X> 嗎」／「<X> 是二進位檔，要換成新版嗎？」；config.toml 三方合併也用它；-y 免問")
REN_T = ("Renovate", "GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：有新版就開 PR 改 version.toml 那一行；見「A. Renovate 路徑」頁")
E33_T = (''')
rep('''foot(p5, "p5", F.y, T5, ALL - {"inv", "tree", "pend"})''', '''foot(p5, "p5", F.y, T5 + [PULLX_T], ALL - {"inv", "tree", "pend"})''')
rep('''foot(p5b, "p5b", F.y, T5B, ALL - {"inv", "pend", "tree"})''', '''foot(p5b, "p5b", F.y, T5B + [PULLX_T], ALL - {"inv", "pend", "tree"})''')
rep('''foot(p6c, "p6c", F.y, T6, ALL - {"tree", "pend", "rule", "inv"} | {"entry"})''', '''foot(p6c, "p6c", F.y, T6 + [PULLX_T], ALL - {"tree", "pend", "rule", "inv"} | {"entry"})''')
rep('''foot(p7c, "p7c", F.y, T7, ALL - {"inv", "tree", "pend", "rule"})''', '''foot(p7c, "p7c", F.y, T7 + [PULLX_T], ALL - {"inv", "tree", "pend", "rule"})''')
rep('''foot(p7cc, "p7cc", F.y, T7, ALL - {"inv", "tree", "pend", "note"} | {"entry"})''', '''foot(p7cc, "p7cc", F.y, T7 + [E22_T], ALL - {"inv", "tree", "pend", "note"} | {"entry"})''')
rep('''foot(p7b, "p7b", F.y, T7B, ALL - {"inv", "tree", "pend", "rule"})''', '''foot(p7b, "p7b", F.y, T7B + [PULLX_T, REN_T], ALL - {"inv", "tree", "pend", "rule"})''')
rep('''foot(p7bcd, "p7bcd", F.y, T7E, ALL - {"inv", "tree", "pend", "rule"} | {"entry"})''', '''foot(p7bcd, "p7bcd", F.y, T7E + [E22_T], ALL - {"inv", "tree", "pend", "rule"} | {"entry"})''')
rep('''foot(p8c, "p8c", F.y, T8, ALL - {"inv", "pend", "tree", "rule"})''', '''foot(p8c, "p8c", F.y, T8 + [PULLX_T], ALL - {"inv", "pend", "tree", "rule"})''')
rep(''' ("gen／mod?／import", "gen/tools.just 每個 <ns>.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的四行也問後只刪原文相同的"),''',
''' ("gen／mod?／import", "gen/tools.just 每個 <ns>.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；gen/.stamp 只記引擎 ref，uninstall 一併刪；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的四行也問後只刪原文相同的"),''')
# bootstrap(1) a9f 一行一檔
rep('''b.files("a9f", P, 12, "install 寫（見「install（1）（2）」頁）", [".vendor_kit/ 薄殼五檔（含 log.sh）", "version.toml 第一行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep", "config.toml（含預設值）", "根 justfile（加 import 行）", "根 .dockerignore 四行"], 360, cols=2)''',
    '''b.files("a9f", P, 12, "install 寫（見「install（1）（2）」頁）", ["薄殼五檔（含 log.sh）", "version.toml 第一行", "gen/.stamp（引擎 ref）", "baseline/.gitkeep", "config.toml（預設值）", "根 justfile import 行", "根 .dockerignore 四行"], 360, cols=2)''')
# remove(2)：命中幾處？→ 有命中？／唯一？
rep('''b.box("m9z", E, 5, SUB, "零命中：不刪、印清單", 70, ax="l")
b.box("m9m", E, 5, v2(D12), "命中幾處？", 140, ax=110)
b.box("m9d", E, 5, SUB, "唯一：刪那幾行", 100, ax="r")
b.box("m9f", P, 5, F12, "初始檔（只移除我們 append 的行；其餘不動；永不刪檔）", 360)
b.box("m9w", E, 7, v2(SUB), "多處：保留＋warn", 140, ax=110)''',
'''b.box("m9z", E, 5, SUB, "否（零命中）：不刪、印清單", 90, ax="l")
b.box("m9m", E, 5, v2(D12), "有命中？", 140, ax=110)   # r11：三分支拆兩菱形（lint decision）
b.box("m9m2", E, 6, v2(D12), "是 → 唯一？", 140, ax=110)
b.box("m9d", E, 6, SUB, "是：刪那幾行", 100, ax="r")
b.box("m9f", P, 6, F12, "初始檔（只移除我們 append 的行；其餘不動；永不刪檔）", 360)
b.box("m9w", E, 7, v2(SUB), "否（多處）：保留＋warn", 140, ax=110)''')
rep('''b.H("me13z", "m9m", "m9z", "零"); b.H("me13d", "m9m", "m9d", "唯一"); b.D("me13w", "m9m", "m9w", "多處", al=True)''',
    '''b.H("me13z", "m9m", "m9z", "否"); b.D("me13y", "m9m", "m9m2", "是", al=True); b.H("me13d", "m9m2", "m9d", "是"); b.D("me13w", "m9m2", "m9w", "否", al=True)''')
open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("patch 9 ok")
