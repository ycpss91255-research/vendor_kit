"""gen56 → gen57：溢字修正（check_overflow 0 筆）——helper（標題高度、名詞表動態列高、圖例寬度）＋第 2、6 頁個別方塊。
乙版全頁改版的 patch 草稿另存 draft_make_gen_乙版全頁.py（等第 1 頁架構定型後再用）。"""
import re
src = open("gen56.py").read()

def rep(old, new, cnt=1):
    global src
    assert src.count(old) == cnt, (src.count(old), old[:90])
    src = src.replace(old, new)

# ---- helper ----
# 標題：fontSize 18 一行需 23.4+8 → 高 34
src, n = re.subn(r'(v\("title", "1", TITLE, "[^"]*", 40, 20, \d+), 30\)', r'\1, 34)', src)
assert n == 12, n
# 名詞表：列高依內容估算（與 check_overflow 同一套估法）
rep('''def terms(prefix, x, y, rows, kw=170, vw=900, rh=30):
    c = [v(f"{prefix}_th", "1", TEXT(13) + "align=left;fontStyle=1;", "本頁名詞", x, y - 24, 200, 20)]
    for i, (k, d) in enumerate(rows):
        c.append(v(f"{prefix}_tk{i}", "1", TERM_K, k, x, y + i * rh, kw, rh))
        c.append(v(f"{prefix}_tv{i}", "1", TERM_V, d, x + kw, y + i * rh, vw, rh))
    return c''',
'''def need_h(text, fs, w):
    """跟 check_overflow 同一套估法：行數×fs×1.3 + 8。"""
    from check_overflow import wrap
    lines = sum(wrap(ln, fs, w - 16)[0] for ln in text.split("\\n"))
    return lines * fs * 1.3 + 8
def terms(prefix, x, y, rows, kw=170, vw=900, rh=30):
    import math
    c = [v(f"{prefix}_th", "1", TEXT(13) + "align=left;fontStyle=1;", "本頁名詞", x, y - 34, 200, 28)]
    cy = y
    for i, (k, d) in enumerate(rows):
        h = max(rh, math.ceil(max(need_h(k, 12, kw), need_h(d, 12, vw))) + 2)
        c.append(v(f"{prefix}_tk{i}", "1", TERM_K, k, x, cy, kw, h))
        c.append(v(f"{prefix}_tv{i}", "1", TERM_V, d, x + kw, cy, vw, h))
        cy += h
    return c''')
# 圖例：兩行的項目加寬到一行
rep(' "pimg":   (PURPLE_LEAF,        "紫：image / container", 180, 40, 10),', ' "pimg":   (PURPLE_LEAF,        "紫：image / container", 200, 40, 10),')
rep(' "pstage": (PURPLE_LEAF,        "紫：image（每個 stage 都是一個 image）", 270, 40, 10),', ' "pstage": (PURPLE_LEAF,        "紫：image（每個 stage 都是一個 image）", 320, 40, 10),')
rep(' "filebox":(FILE,               "虛線框：檔案", 120, 40, 10),', ' "filebox":(FILE,               "虛線框：檔案", 120, 40, 10),\n "optfile":(FILE,               "虛線框：可有可無的檔", 170, 40, 10),')

# ---- 第 2 頁 ----
rep('"工具 repo（每個要出貨的工具一個）", 40, 290, 320, 260))', '"工具 repo（每個工具一個）", 40, 290, 320, 260))')
rep('"工具名 = <repo>；下面四樣是接上 vendor_kit 的必要條件", 10, 40, 300, 30))', '"工具名 = <repo>；下面四樣是接上 vendor_kit 的必要條件", 10, 38, 300, 40))')
rep('p1b.append(v("t_dist", "tool", LEAF(), "dist/\\n（要出貨的全部）", 20, 80, 135, 50))', 'p1b.append(v("t_dist", "tool", LEAF(), "dist/\\n（要出貨的全部）", 16, 80, 146, 50))')
rep('p1b.append(v("t_init", "tool", LEAF(), "init.toml\\n（初始檔清單）", 165, 80, 135, 50))', 'p1b.append(v("t_init", "tool", LEAF(), "init.toml\\n（初始檔清單）", 170, 80, 146, 50))')
rep('p1b.append(v("t_df", "tool", LEAF(), "Dockerfile.dist\\n（只放檔案，沒有程式）", 20, 145, 135, 50))', 'p1b.append(v("t_df", "tool", LEAF(), "Dockerfile.dist\\n（純檔案，無程式）", 16, 145, 146, 50))')
rep('p1b.append(v("t_ci", "tool", LEAF(), "CI：打 tag →\\n建置＋上傳 image", 165, 145, 135, 50))', 'p1b.append(v("t_ci", "tool", LEAF(), "CI：打 tag →\\n建置＋上傳 image", 170, 145, 146, 50))')
rep('p1b.append(v("vk_prog", "vk", LEAF(), "vendor_kit 程式", 20, 50, 135, 40))', 'p1b.append(v("vk_prog", "vk", LEAF(), "vendor_kit 程式", 16, 50, 146, 40))')
rep('p1b.append(v("vk_df", "vk", LEAF(), "Dockerfile", 165, 50, 135, 40))', 'p1b.append(v("vk_df", "vk", LEAF(), "Dockerfile", 170, 50, 146, 40))')
rep('"另一個工具 repo（<repo2>，同型）", 40, 720, 320, 60))', '"另一個工具 repo（<repo2>）", 40, 720, 320, 60))')
rep('"tag 不覆蓋；被引用的版本不刪\\nmulti-arch（amd64 + arm64）；附註來源 commit", 10, 40, 240, 40))', '"tag 不覆蓋；被引用的版本不刪\\nmulti-arch（amd64 + arm64）；附註來源 commit", 10, 40, 240, 56))')
rep('justfile 只用 mod? 掛它）；每個工具各自裝到 .<repo>/", 10, 40, 750, 30))', 'justfile 只用 mod? 掛它）；每個工具各自裝到 .<repo>/", 10, 38, 750, 40))')
rep('.version.local 有同名那行就優先（本機開發用，第 4 頁）", 12, 34, 676, 36))', '.version.local 有同名那行就優先（本機開發用，第 4 頁）", 12, 34, 676, 38))')
rep('p1b.append(v("p_just", "pa", LEAF(), "justfile", 250, 74, 78, 40))', 'p1b.append(v("p_just", "pa", LEAF(), "justfile", 250, 74, 88, 40))')
rep('p1b.append(e("f7b", "p_just", "p_vk", "mod?", (0.5, 1), (0.877, 0), vert=True))', 'p1b.append(e("f7b", "p_just", "p_vk", "mod?", (0.5, 1), (0.8924, 0), vert=True))')
rep('.stamp、baseline/<repo>/", 12, 142, 316, 50).replace("fontSize=14", "fontSize=12"))', '.stamp、baseline/<repo>/", 12, 142, 316, 56).replace("fontSize=14", "fontSize=12"))')
rep('"以使用者身分執行，跑完即刪；先對專案目錄上鎖", 20, 412, 300, 20))', '"以使用者身分執行，跑完即刪；先對專案目錄上鎖", 20, 412, 300, 24))')
rep('p1b.append(v("pb", "proj", SW(NEUTRAL), "使用者檔案（進 git）", 300, 440, 220, 125))', 'p1b.append(v("pb", "proj", SW(NEUTRAL), "使用者檔案（進 git）", 300, 440, 220, 145))')
rep('p1b.append(v("p_u1", "pb", LEAF(), "Dockerfile\\n（專案自己的）", 12, 45, 100, 50))', 'p1b.append(v("p_u1", "pb", LEAF(), "Dockerfile\\n（專案自己的）", 12, 45, 116, 50))')
rep('p1b.append(v("p_u2", "pb", LEAF(), "設定檔…", 122, 45, 86, 50))', 'p1b.append(v("p_u2", "pb", LEAF(), "設定檔…", 134, 45, 74, 50))')
rep('"init 建立；之後由使用者維護", 12, 98, 200, 18))', '"init 建立；之後由使用者維護", 12, 100, 200, 24))')
rep('p1b.append(v("pc", "proj", SW(NEUTRAL), ".<repo>/（不進 git）", 540, 440, 220, 125))', 'p1b.append(v("pc", "proj", SW(NEUTRAL), ".<repo>/（不進 git）", 540, 440, 220, 145))')
rep('印記檔 = 裝的 image + 每檔指紋", 6, 88, 210, 32))', '印記檔 = 裝的 image + 每檔指紋", 6, 86, 210, 52))')
rep('"需預先安裝這三個", 10, 40, 140, 20))', '"需預先安裝這三個", 10, 40, 140, 24))')
rep('p1b.append(v("h_just", "host", LEAF(GREY), "just\\n（執行 justfile）", 20, 70, 120, 50))', 'p1b.append(v("h_just", "host", LEAF(GREY), "just\\n（跑 justfile）", 10, 70, 140, 50))')
rep('p1b.append(v("h_git", "host", LEAF(GREY), "git\\n（管理專案 repo）", 20, 130, 120, 50))', 'p1b.append(v("h_git", "host", LEAF(GREY), "git\\n（專案 repo）", 10, 130, 140, 50))')
rep('p1b.append(v("h_docker", "host", LEAF(GREY), "Docker\\n（跑所有容器）", 20, 477.5, 120, 50))', 'p1b.append(v("h_docker", "host", LEAF(GREY), "Docker\\n（跑所有容器）", 10, 487.5, 140, 50))')
rep('p1b += [c.replace("虛線框：檔案", "虛線框：可有可無的檔") for c in legend("p1b", 40, 820, ["red", "green", "yellow", "pimg", "neutral", "white", "grey", "filebox"], "實線 = 傳輸內容\\n虛線箭頭 = 基底 image → 以它為底的 image；虛線框 = 可有可無的檔")]',
    'p1b += legend("p1b", 40, 820, ["red", "green", "yellow", "pimg", "neutral", "white", "grey", "optfile"], "實線 = 傳輸內容\\n虛線框 = 可有可無的檔")')

# ---- 第 6 頁 ----
for old in ['"原始碼（進 git，人維護）", 40, 70, 300, 20))', '"產物（不進 git；原型在本機建置，正式版由 CI 建置＋上傳）", 640, 70, 420, 20))', '"使用端（前三樣進 git）", 1080, 70, 300, 20))']:
    rep(old, old.replace(', 20))', ', 24))'))
for old in ['"= proto/vendor_kit/", 10, 40, 280, 18))', '"= proto/tool/", 10, 40, 280, 18))', '"= proto/project/", 10, 40, 320, 18))']:
    rep(old, old.replace(', 18))', ', 24))'))
rep('p7.append(v("f_vk", "r_vk", LEAF(), "vendor_kit\\n（安裝工具程式）", 20, 70, 120, 50))', 'p7.append(v("f_vk", "r_vk", LEAF(), "vendor_kit\\n（引擎程式）", 20, 70, 120, 50))')
rep('p7.append(v("f_init", "r_tool", LEAF(), "init.toml\\n（init 清單）", 20, 130, 120, 50))', 'p7.append(v("f_init", "r_tool", LEAF(), "init.toml\\n（init 清單）", 16, 130, 124, 50))')
rep('p7.append(v("f_tdf", "r_tool", LEAF(), "Dockerfile.dist\\n（出貨食譜）", 160, 130, 120, 50))', 'p7.append(v("f_tdf", "r_tool", LEAF(), "Dockerfile.dist\\n（出貨食譜）", 148, 130, 146, 50))')
rep('工具 image 與引擎 image 各自獨立升級", 10, 450, 320, 36))', '工具 image 與引擎 image 各自獨立升級", 10, 446, 320, 40))')

open("gen57.py", "w").write(src)
print("ok")
