src = open("gen23.py").read()
def rep(old, new):
    global src
    assert src.count(old) == 1, (src.count(old), old[:90])
    src = src.replace(old, new)
S12 = '.replace("fontSize=14", "fontSize=12")'
rep('p2.append(v("a_l1", "bA", LEAF(), "讀 .version", 380, 75, 140, 40))',
    'p2.append(v("a_l1", "bA", LEAF(), "讀 .version\\n（一行一個工具，逐行做）", 380, 75, 140, 40)' + S12 + ')')
rep('p2.append(v("b_l1", "bB", LEAF(), "讀 .version", 380, 75, 140, 40))',
    '''p2.append(v("b_l1", "bB", LEAF(), "讀 .version\\n（一行一個工具，逐行做）", 380, 75, 140, 40)''' + S12 + ''')
p2.append(v("b_note", "bB", NOTE, ".version 每一行 = 一個工具，key 就是工具名：\\n<name> = \\"…-dist:vX@sha256:…\\"  → 裝到 .<name>/\\n<name2> = \\"…\\"  → 裝到 .<name2>/\\n每一行各跑一次右邊的流程；.<name>/.stamp 第一行\\n記的就是那一行的 image，兩者相同才算「版本相同」", 40, 135, 290, 100))''')
rep('p2.append(v("b_l2", "bB", RHOMBUS, "印記可讀且版本\\n= .version？", 550, 55, 180, 80))',
    'p2.append(v("b_l2", "bB", RHOMBUS, ".<name>/.stamp 第一行\\n= .version 那一行？", 550, 55, 180, 80)' + S12 + ')')
rep(''' ("印記", ".<name>/.stamp：install 寫下的「版本 + 每檔指紋」；日常每次 just 都拿它比對"),''',
    ''' ("印記", ".<name>/.stamp：install 寫下的「第一行 = 裝的 image，之後每行 = 一個檔的指紋」；日常每次 just 都拿它比對"),''')
rep(''' (".version", "專案裡的版本清單（TOML）：一個工具一行，記工具名與 image 版本"),''',
    ''' (".version", "專案裡的版本清單（TOML）：一個工具一行 key = \\"image\\"；key 就是工具名，決定安裝目錄 .<key>/ 和要比對哪個印記"),''')
open("gen24.py", "w").write(src); print("ok")
