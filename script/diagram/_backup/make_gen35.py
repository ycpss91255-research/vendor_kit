"""gen34 → gen35：平台定為 Linux amd64+arm64 → #13 flock 鎖畫回第 1／5 頁；第 2／8 頁註明 multi-arch"""
src = open("gen34.py").read()

def rep(old, new, count=1):
    global src
    assert src.count(old) == count, (src.count(old), old[:90])
    src = src.replace(old, new)

# ---- 頁 1：專案檔案存取加「鎖」單元 ----
rep('p1.append(v("wr_base", "m_write", LEAF(), "讀寫基準", 104, 92, 88, 40))',
    'p1.append(v("wr_lock", "m_write", LEAF(), "鎖（專案\\n目錄）", 104, 92, 88, 40))\np1.append(v("wr_base", "m_write", LEAF(), "讀寫基準", 196, 92, 88, 40))')
rep(''' ("基準（baseline）", ".vendor_kit/baseline/<name>/：你上次確認過的那版模板副本；diff 用它分出「工具改了什麼」「你改了什麼」；init／accept 寫、人不改"),''',
    ''' ("基準（baseline）", ".vendor_kit/baseline/<name>/：你上次確認過的那版模板副本；diff 用它分出「工具改了什麼」「你改了什麼」；init／accept 寫、人不改"),
 ("鎖（專案目錄）", "同一專案同時只有一個 install 在跑：對專案目錄上鎖（flock），後到的等前一個裝完；verify 拿共享鎖；程序被殺系統自動解鎖"),''')

# ---- 頁 2：安裝容器先上鎖；GHCR image multi-arch ----
rep('"以使用者身分執行，跑完即刪", 20, 392, 300, 20))', '"以使用者身分執行，跑完即刪；先對專案目錄上鎖", 20, 392, 300, 20))')
rep('"tag 不覆蓋；被引用的版本不刪；\\nimage 附註：版本、來源 repo 與 commit", 10, 40, 240, 40))',
    '"tag 不覆蓋；被引用的版本不刪；每個 image 都是\\nmulti-arch（amd64 + arm64）；附註版本、來源 commit", 10, 40, 240, 40))')
rep(''' ("tag / digest", "image 的版本名稱（v0.43.0）／內容指紋（sha256:…）；.version 兩者都記，工具只認 digest"),''',
    ''' ("tag / digest", "image 的版本名稱（v0.43.0）／內容指紋（sha256:…）；.version 兩者都記，工具只認 digest"),
 ("multi-arch", "同一個 image 名稱同時提供 amd64 與 arm64 兩種處理器版本，Docker 依主機自動選；支援平台 = Linux（含 WSL2）amd64／arm64"),''')

# ---- 頁 3：便條 ----
rep('\\n同一專案兩個 just 同時跑怎麼互斥：方案審中（issue #24），第 5 頁先留一格。", 20, 1240, 1620, 60))',
    '\\n同一專案兩個 just 同時跑：容器先對專案目錄上鎖，後到的等前一個裝完再檢查（第 5 頁）。", 20, 1240, 1620, 60))')

# ---- 頁 5：install 取鎖／逾時；verify 共享鎖；accept 排他鎖 ----
rep('''p4.append(v("l1", "install", NOTE, "取得安裝權（同一專案同時只能一個 install；\\n怎麼互斥方案審中，issue #24）", 90, 130, 280, 50))
p4.append(v("l2", "install", LEAF(), "重讀版本檔與印記第一行", 130, 330, 200, 40))''',
'''p4.append(v("l1", "install", LEAF(), "對專案目錄上鎖（排他）\\n拿不到：1 秒後印訊息，最多等 60 秒", 90, 130, 280, 50).replace("fontSize=14", "fontSize=12"))
p4.append(v("l1q", "install", RHOMBUS, "拿到鎖？", 140, 210, 180, 80))
p4.append(v("l_err", "install", ELLIPSE(RED), "逾時或鎖不支援：\\n中止，不動任何檔", 15, 325, 190, 60).replace("fontSize=14", "fontSize=12"))
p4.append(v("l2", "install", LEAF(), "重讀版本檔與印記第一行", 130, 330, 200, 40))''')
rep('''p4.append(v("l7", "install", LEAF(), "刪舊 .<name>/、暫存目錄改名\\n（整批覆蓋）", 130, 730, 200, 60).replace("fontSize=14", "fontSize=12"))
p4.append(v("l8", "install", LEAF(), "釋放安裝權", 130, 820, 200, 40))
p4.append(v("l9", "install", ELLIPSE(GREEN), "成功結束", 150, 890, 160, 40))
p4.append(v("ln", "install", NOTE, "任一步失敗即中止，舊 .<name>/ 不動；啟動器不會執行 .<name>/ 內的腳本。\\n主機要能用在 Linux、macOS Docker Desktop、Windows WSL2（notes §2）。", 30, 950, 400, 50))
p4.append(e("le0", "l0", "l1")); p4.append(e("le1", "l1", "l2"))
p4.append(e("le3", "l2", "l3"))''',
'''p4.append(v("l7", "install", LEAF(), "刪舊 .<name>/、暫存目錄改名\\n（整批覆蓋；空窗由鎖遮住）", 130, 730, 200, 60).replace("fontSize=14", "fontSize=12"))
p4.append(v("l8", "install", LEAF(), "釋放鎖", 130, 820, 200, 40))
p4.append(v("l9", "install", ELLIPSE(GREEN), "成功結束", 150, 890, 160, 40))
p4.append(v("ln", "install", NOTE, "任一步失敗即中止，舊 .<name>/ 不動；啟動器不會執行 .<name>/ 內的腳本。\\n支援平台：Linux（含 WSL2）amd64／arm64；鎖不支援的檔案系統（NFS 等）直接中止。", 30, 950, 400, 50))
p4.append(e("le0", "l0", "l1")); p4.append(e("le1", "l1", "l1q"))
p4.append('<mxCell id="le_err" value="否" style="' + EDGE + 'align=right;verticalAlign=middle;spacingRight=6;spacingBottom=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="install" source="l1q" target="l_err"><mxGeometry x="0.4" relative="1" as="geometry"><Array as="points"><mxPoint x="110" y="250"/></Array></mxGeometry></mxCell>')
p4.append(e("le2", "l1q", "l2", "是", (0.5, 1), (0.5, 0), vert=True))
p4.append(e("le3", "l2", "l3"))''')
rep('p4.append(v("v1", "verify", LEAF(), "讀印記第一行（已裝版本）", 130, 130, 200, 40))',
    'p4.append(v("v1", "verify", LEAF(), "對專案目錄上鎖（共享）\\n讀印記第一行（已裝版本）", 130, 130, 200, 40).replace("fontSize=14", "fontSize=12"))')
rep('p4.append(v("v_ok", "verify", ELLIPSE(GREEN), "通過", 160, 560, 140, 50))',
    'p4.append(v("v_ok", "verify", ELLIPSE(GREEN), "通過（釋放鎖）", 160, 560, 140, 50).replace("fontSize=14", "fontSize=12"))')
rep('p4.append(v("a1", "accept", NOTE, "取得安裝權（跟 install 同一套，審中）", 110, 130, 200, 40))',
    'p4.append(v("a1", "accept", LEAF(), "對專案目錄上鎖（排他）", 110, 130, 200, 40))')
rep('p4.append(v("a4", "accept", LEAF(), "釋放安裝權", 110, 370, 200, 40))', 'p4.append(v("a4", "accept", LEAF(), "釋放鎖", 110, 370, 200, 40))')
rep('"已定案：verify 比 image 內的 /dist 而不是印記（issue #23）；diff 三方（#22）。安裝權怎麼互斥審中（#24，要同時能用在 Linux／macOS／WSL2）。本機開發模式見第 4 頁（#21）。"',
    '"已定案：verify 比 image 內的 /dist 而不是印記（issue #23）；diff 三方（#22）；install／verify／accept 對專案目錄上鎖（#24）。本機開發模式見第 4 頁（#21）。"')
rep(''' ("安裝權", "同一專案同時只能有一個 install／accept 在寫 .<name>/ 或基準；怎麼做到互斥（鎖）還在審（issue #24）"),''',
    ''' ("鎖（排他／共享）", "對專案目錄上鎖（flock）：排他 = 同時只有一個（install、accept）；共享 = 可多個一起但要等排他的放開（verify）。程序結束或被殺，系統自動解鎖，不會留殘鎖"),''')

# ---- 頁 7：repo_fs 描述 ----
rep('"專案檔案存取：唯一能寫專案目錄的模組；整批替換、讀寫基準都在這（安裝權互斥方案審中）"', '"專案檔案存取：唯一能寫專案目錄的模組；整批替換、專案目錄鎖（flock）、讀寫基準都在這"')
rep(''' ("基準（baseline）", "上次確認過的模板副本，diff 用它分出誰改了什麼"),''',
    ''' ("基準（baseline） / flock", "上次確認過的模板副本，diff 用它分出誰改了什麼／Linux 的檔案鎖，程序結束自動解鎖"),''')

# ---- 頁 8：CI 兩個架構 ----
rep('p8.append(v("d_ci", "repo", LEAF(), ".github/workflows/\\nbake validate → system/acceptance → bake release", 20, 1036, 380, 44))',
    'p8.append(v("d_ci", "repo", LEAF(), ".github/workflows/\\nbake validate → system/acceptance → bake release（amd64 + arm64 都 build）", 20, 1036, 380, 44).replace("fontSize=14", "fontSize=12"))')
rep('    ("g1", "BuildKit stage 依賴\\nrelease 只 FROM runtime → 測試碼、pytest 進不了產品 image"),',
    '    ("g1", "BuildKit stage 依賴\\nrelease 只 FROM runtime → 測試碼、pytest 進不了產品 image；release 同時 build amd64 + arm64（multi-arch）"),')

# ---- 頁 9：自動列 ----
rep('"第 3 頁的檢查：印記第一行 ≠ .version → install；相同 → verify（.<name>/ 跟 image 內的 dist 逐檔比）；失敗就中止"',
    '"第 3 頁的檢查：先對專案目錄上鎖 → 印記第一行 ≠ .version → install；相同 → verify（.<name>/ 跟 image 內的 dist 逐檔比）；失敗就中止"')

open("gen35.py", "w").write(src)
print("ok")
