src = open("gen20.py").read()
def rep(old, new):
    global src
    assert src.count(old) == 1, (src.count(old), old[:90])
    src = src.replace(old, new)

# 頁 1：vk 加寬讓 a9b 標籤不壓紫框；標籤兩行；名詞表補 TOML/just/PR、升級分兩條路
rep('p1.append(v("vk", "1", PURPLE_SW, "vendor_kit（一個 container）", VX, VY, 520, 860))',
    'p1.append(v("vk", "1", PURPLE_SW, "vendor_kit（一個 container）", VX, VY, 570, 860))')
rep('p1.append(e("a9b", "m_stamp", "m_write", "新指紋、比對結果", (0.9, 0), (0.945, 1), vert=True))',
    'p1.append(e("a9b", "m_stamp", "m_write", "新指紋、\\n比對結果", (0.9, 0), (0.945, 1), vert=True))')
rep(''' ("upgrade（升級）", "改 .version 換新版本：由機器人開 PR 或 just upgrade；下次 just 時 dist/ 整包換新"),''',
    ''' ("upgrade（升級）", "改 .version 換新版本。兩條路：機器人開 PR（人 merge 後，下次 just 才換新）；或 just upgrade（改完立即 install → diff）"),
 ("TOML / just / PR", "設定檔格式（key = \\"value\\"）／主機上的指令跑器，使用者打 just <指令>／GitHub 上的合併請求，merge = 接受修改"),''')
# 頁 2
rep(''' ("upgrade（升級）", "改 .version 換新版本：由機器人開 PR 或 just upgrade；下次 just 時 .<name>/ 整批換新"),''',
    ''' ("upgrade（升級）", "改 .version 換新版本。兩條路：機器人提出合併請求（PR，人 merge 後下次 just 才換新）；或 just upgrade（改完立即 install → diff）"),
 ("PR / merge", "GitHub 上的合併請求／接受它，修改才進 repo"),''')
# 頁 4：名詞表補模板 / dist
rep('''p3 += terms("p3", 40, 830, [''', '''p3 += terms("p3", 40, 830, [
 ("模板 / dist", "dist = 工具要出貨的檔案，整批放進 .<name>/；模板 = dist 裡給初始檔用的樣板，diff 拿新版模板跟你的檔案比"),''')
# 頁 5：待決便條改白話
rep('"仍待決（notes §8 #11–13）：verify 的驗證基準（印記 vs 從 image 重取）、diff 是否三方比對、並行安裝的 lock。"',
    '"仍待決（notes §8 #11–13）：verify 要跟印記比、還是重新從 image 拿來比；diff 要不要連舊版模板一起比（三方比對）；兩個 just 同時安裝時怎麼互斥（lock）。"')
# 頁 7：stage 外框改淺灰分組、g7 用語、名詞表
rep('p8.append(v("stages", "1", PURPLE_SW, "Dockerfile stage（BuildKit）", SX, 70, SW_ + 20, COLH))',
    'p8.append(v("stages", "1", SW(NEUTRAL), "Dockerfile stage（BuildKit）", SX, 70, SW_ + 20, COLH))')
rep('("g7", "時間預算\\nverify 200 個檔必須 < 0.5 秒（每次 just 都會跑它）")])',
    '("g7", "時間預算\\nverify 200 個檔必須 < 0.5 秒（已安裝且版本一致時，每次 just 都會跑它）")])')
rep(''' ("ruff / hadolint / import-linter", "Python 寫法檢查／Dockerfile 寫法檢查／檢查模組之間誰可以 import 誰（契約寫在設定檔）"),''',
    ''' ("ruff / import-linter", "Python 寫法檢查／檢查模組之間誰可以 import 誰（契約寫在設定檔）"),
 ("import / 純函式", "import = 一個模組引用另一個模組；純函式 = 只算結果、不碰檔案與網路的函式（template、diff、stamp、report）"),
 ("VERSION vs .version", "VERSION = fixtures 裡假 dist 的版本字串（image 內 /dist/VERSION，install 寫進印記）；.version = 專案 repo 記工具版本的檔"),''')
open("gen21.py", "w").write(src); print("ok")
