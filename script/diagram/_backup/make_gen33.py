src = open("gen32.py").read()
def rep(a, b):
    global src; assert src.count(a) == 1, a[:70]; src = src.replace(a, b)
rep(''' ("TOML", "一種設定檔格式（key = \\"value\\"）；.version、init.toml 都用它"),
])''', ''' ("TOML", "一種設定檔格式（key = \\"value\\"）；.version、init.toml 都用它"),
 ("install / init / verify / diff", "安裝容器的四個子命令：把 dist 裝進 .<name>/ 並寫印記檔／第一次建立初始檔／檢查 .<name>/ 沒被手改／升級後比對新版模板"),
])''')
rep(''' ("<name> / just", "工具名（= .version 的 key，安裝目錄 .<name>/）／主機上的指令跑器"),
])''', ''' ("<name> / just", "工具名（= .version 的 key，安裝目錄 .<name>/）／主機上的指令跑器"),
 ("install / init / verify / diff / bootstrap", "vendor_kit 的子命令：把 dist 裝進 .<name>/ 並寫印記／建立初始檔／檢查 .<name>/ 沒被手改／比對新版模板／第一次寫出啟動器（第 10 頁）"),
])''')
rep('p9.append(e("ce4", "c3", "c5", "", (1, 0.5), (0, 0.1)).replace(\'endFill=1;\', \'endFill=1;entryPerimeter=0;\', 1))', 'p9.append(e("ce4", "c3", "c5", "", (1, 0.5), (0.2, 0.1)).replace(\'endFill=1;\', \'endFill=1;entryPerimeter=0;\', 1))')
rep('p9.append(e("ce5", "c4", "c5", "", (1, 0.5), (0, 0.9)).replace(\'endFill=1;\', \'endFill=1;entryPerimeter=0;\', 1))', 'p9.append(e("ce5", "c4", "c5", "", (1, 0.5), (0.2, 0.9)).replace(\'endFill=1;\', \'endFill=1;entryPerimeter=0;\', 1))')
rep('".version（先只有 vendor_kit = \\"…\\" 一行，進 git；已存在就不動）", 1160, 331, 340, 36)', '".version（先只有 vendor_kit 一行，進 git；已存在就不動）", 1160, 331, 340, 36)')
rep(''' ("以使用者身分", "docker run -u UID:GID：容器寫出的檔案擁有者是你，不是 root"),''',
    ''' ("以使用者身分", "docker run -u UID:GID：容器寫出的檔案擁有者是你，不是 root"),
 ("diff / PR", "diff = 升級後比對新版模板與你的初始檔的子命令（不改檔）／PR = GitHub 上的合併請求，人 merge 才生效"),''')
open("gen33.py", "w").write(src); print("ok")
