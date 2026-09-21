src = open("gen21.py").read()
def rep(old, new):
    global src
    assert src.count(old) == 1, (src.count(old), old[:90])
    src = src.replace(old, new)
# 頁 4：diff 由使用者呼叫；提交步驟分兩條路
rep('"執行 diff：init.toml 列的檔案\\n新版模板 vs 你的檔案有差異？", 70, 240, 280, 100))',
    '"使用者執行 just diff：\\n新版模板 vs 你的初始檔有差異？", 70, 240, 280, 100))')
rep('p3.append(v("c10", "up", LEAF(), "提交變更（.version + 使用者的修改）", 20, 460, 380, 40))',
    'p3.append(v("c10", "up", LEAF(), "提交使用者的修改\\n（just upgrade 那條路連 .version 一起提交；機器人 PR 那條路 .version 已在 merge 時提交）", 20, 455, 380, 56).replace("fontSize=14", "fontSize=12"))')
# 頁 5：便條不引用 notes；取下一項框加大
rep('"仍待決（notes §8 #11–13）：verify 要跟印記比', '"仍待決：verify 要跟印記比')
rep('p4.append(v("i3", "init", LEAF(), "取下一項\\n（image 內由 src 指定的檔 → 專案內的 dest）", 120, 315, 240, 50))',
    'p4.append(v("i3", "init", LEAF(), "取下一項\\n（image 內由 src 指定的檔 → 專案內的 dest）", 80, 312, 320, 56))')
# 頁 7：smoke 框加高、lint 描述、名詞表
rep('"smoke\\nFROM release；真的跑一次 install + verify", LX + 20, 690, LW, 50))',
    '"smoke\\nFROM release；真的 install + verify 一次", LX + 20, 690, LW, 60))')
rep('blackbox_check.py\\n寫法、架構契約、鏡射、黑箱"', 'blackbox_check.py\\n寫法檢查、import 分層契約、鏡射檢查、黑箱檢查"')
rep(''' ("鏡射", "test/ 的檔名跟 src/ 一一對應：src 有 cli.py，test 就必須有 test_cli.py"),''',
    ''' ("鏡射", "test/ 的檔名跟 src/ 一一對應：src 有 cli.py，test 就必須有 test_cli.py"),
 ("黑箱", "只從外面用、不看裡面：system / acceptance 測試不准 import vendor_kit，只能像使用者一樣 docker run 或打 just"),
 ("install / verify / just", "install = 把 dist 裝進 .<name>/ 並寫印記；verify = 檢查 .<name>/ 沒被手改；just = 使用者在主機打的指令跑器（第 3 頁）"),''')
open("gen22.py", "w").write(src); print("ok")
