"""第十一輪 patch 2：名詞表瘦身（頁高 ≤ 2400）、bootstrap(1)／install 文字精簡。"""
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:90])
    src = src.replace(old, new)

rep(''' ("操作紀錄檔／log（v2.12）", ".vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，每次執行一檔（JSON Lines；不進 git）；事件順序：啟動器 mkdir log/（連同其 .gitignore：*／!.gitignore，缺才建）→ 建檔寫 launcher_start → 每個引擎容器（resolve、apply 各一個）先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔，best-effort）、launcher_exit（每個結束碼都寫）；sync 快路徑由啟動器寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件註冊表 log-events.txt 真本在引擎 image，log.sh 內嵌啟動器事件白名單"),
 ("config.toml（v2.12／v2.13）", ".vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）並存 baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設"),''',
''' ("操作紀錄檔／log（v2.12）", ".vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，一次執行一檔（JSON Lines，不進 git）：啟動器 mkdir log/（含其 .gitignore）→ 建檔寫 launcher_start → 每個引擎容器先 append engine_start、結束寫 engine_exit → 啟動器結束前 log_prune（30 天／50 檔）、launcher_exit；sync 快路徑寫 sync_fast_path；寫不進 → 1 + 6-38；tty 訊息同句進 body；事件表 log-events.txt 在引擎 image，log.sh 內嵌啟動器白名單"),
 ("config.toml（v2.12／v2.13）", ".vendor_kit/config.toml（進 git）：[log] keep = 50、days = 30；install 建（含註解）＋ baseline 副本 baseline/vendor_kit/config.toml；upgrade vendor_kit 三方合併；uninstall 只在 hash == 副本時刪；缺 = 預設"),''')
rep('''BM_T = ("baseline／metadata", "baseline/<repo>/ = 上次合併的範本副本（歷史狀態，進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）、declined_hash、append 過的行、進度日誌（state=in-progress）；install 只建 baseline/.gitkeep（metadata 到 add 才建）；remove 先讀它（append 行）再刪整個 baseline/<repo>/")''',
'''BM_T = ("baseline／metadata", "baseline/<repo>/ = 上次合併的範本副本（進 git；upgrade 的三方合併共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state／declined_hash、append 行、進度日誌；install 只建 baseline/.gitkeep（metadata 到 add 才建）；remove 先讀它再刪整個 baseline/<repo>/")''')
rep('''FIP_T = ("flock／指紋／進度日誌", "flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata state=in-progress，其餘用 .vendor_kit/.tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑")''',
'''FIP_T = ("flock／指紋／進度日誌", "flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」（橙）；進度日誌 = 第一個寫入前建、最後一步刪：add／upgrade <repo> 記在 metadata，其餘用 .tmp.<verb>.<id>.toml（.tmp.install／.tmp.remove／.tmp.uninstall／.tmp.undev／.tmp.upgrade）；失敗後下次可寫動詞先恢復")''')
# T5：拿掉「bootstrap.sh 流程」（band 標題已寫）、精簡 --local／inspect
rep(''' BOOT_T,
 ("bootstrap.sh 流程", "先建 log/bootstrap/ 並寫 launcher_start → 檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止：清半成品但保留 log/）→ 對每個 -t <repo>[@<tag>] 呼叫 add；再跑 = install"),''',
''' BOOT_T,''')
rep(''' ("--local <image tag 或 tar>（只有 bootstrap.sh 收 tag 形）", "離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 + 6-37；前置檢查兩形都先做；version.toml 仍寫正式 ref@digest：tar 形由 .digest 旁檔取；tag 形不讀 .digest —— 專案已有 version.toml → 用該行，第一次接入 → 用 bootstrap.sh 內嵌引擎 ref（v2.10 §2）；version.local.toml 記 tag + image ID；add --local 只收存在的 .tar（v2.10 §3）"),''',
''' ("--local <image tag 或 tar>（只有 bootstrap.sh 收 tag 形）", "離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 + 6-37；version.toml 仍寫正式 ref@digest：tar 形由 .digest 旁檔取，tag 形不讀 .digest（專案已有 version.toml → 用該行，第一次 → 內嵌引擎 ref，v2.10 §2）；version.local.toml 記 tag + image ID；add --local 只收存在的 .tar"),''')
rep(''' ("docker image inspect／image ID", "啟動器每次 docker run 前先 docker image inspect <ref>：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 inspect 的 .Id 必須等於 version.local.toml 記的 image ID（同一個 tag 重新 build 過才會被發現），否則 1；不用 --pull never（docker 19.03 無此旗標）"),''',
''' ("docker image inspect／image ID", "啟動器每次 docker run 前先 docker image inspect <ref>：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1；不用 --pull never"),''')
rep(''' ("進度日誌（.tmp.install；v2.13 P5）", "install 在第一個寫入前建 .vendor_kit/.tmp.install.<id>.toml（<id> = trace_id），最後一步刪；第一次 install 也建 —— 它同時是「不留半成品」的清除清單；未完成 → 下次可寫動詞先恢復"),''',
''' ("進度日誌（.tmp.install；v2.13 P5）", "install 在第一個寫入前建 .vendor_kit/.tmp.install.<id>.toml，最後一步刪；第一次也建 = 「不留半成品」的清除清單；未完成 → 下次可寫動詞先恢復"),''')
rep(''' ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 把另一個 just 檔載進根 justfile 的那一行；新建根 justfile 還有 default recipe（default: ＋ 下一行縮排的 @just --list；寫成一行是語法錯誤）"),''',
''' ("just／recipe／import／default", "just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 根 justfile 載入 .vendor_kit/entry.just 的那一行；新建根 justfile 另有 default recipe（兩行；寫成一行是語法錯誤）"),''')
rep('''T5I = [t for t in T5 if not t[0].startswith(("release／tar", "--local"))]   # install(1) 不談離線包''',
'''T5I = [t for t in T5 if not t[0].startswith(("release／tar", "--local", "bootstrap.sh", "docker image inspect"))]   # install 兩頁不談離線包／bootstrap''')
rep('''foot(p5cc, "p5cc", F.y, T5, ALL - {"inv", "tree", "pend", "rule"} | {"entry"})''', '''foot(p5cc, "p5cc", F.y, T5I, ALL - {"inv", "tree", "pend", "rule"} | {"entry"})''')
# bootstrap(1) 文字精簡
rep('''b.box("a3", L, 2, D12, "just ≥ 1.33.0？", 240)''', '''b.box("a3", L, 2, D12, "just ≥ 1.33.0？", 300)''')
rep('''b.box("a8tx", U, 8, v2(O12), fl("是 → 1：印 6-37（既是檔案也是本機 image tag，請消歧）"), 220)''', '''b.box("a8tx", U, 8, v2(O12), fl("是 → 1：印 6-37（既是檔案也是 image tag，請消歧）"), 220)''')
rep('''b.box("a8ix", U, 11, v2(R12), fl("失敗 → 1：本機無此 image（tag 形；docker load 後才有）"), 220)   # v2.14-5''', '''b.box("a8ix", U, 11, v2(R12), fl("失敗 → 1：本機無此 image（tag 形）"), 220)   # v2.14-5''')
rep('''b.box("a9x", U, 13, v2(R12), "是 → 1：中止（清半成品、保留 log/；--local 檔未寫）", 220)''', '''b.box("a9x", U, 13, v2(R12), "是 → 1：中止（清半成品、保留 log/）", 220)''')
# install(1)
rep('''b.box("i4l", E, 13, v2(SUB), fl("建進度日誌 .tmp.install.<id>.toml（第一個寫入前；第一次也建 = 清除清單，v2.13 P5）"), 240, ax="l")''', '''b.box("i4l", E, 13, v2(SUB), fl("建進度日誌 .tmp.install.<id>.toml（第一次也建；第一個寫入前）"), 240, ax="l")''')
# install(2)
rep('''b.box("i12", E, 4, D12, "否 → 問「要在 justfile 加這一行嗎」同意？（-y 免問）", 300, ax="l")''', '''b.box("i12", E, 4, D12, "否 → 問「要加這一行嗎」同意？（-y 免問）", 300, ax="l")''')
rep('''b.box("igz", E, 7, v2(G12), fl("0：印結果（建了四行／已含不再加；含 justfile 結果）"), 120, ax="r")''', '''b.box("igz", E, 7, v2(G12), fl("0：印結果（建了／已含）"), 120, ax="r")''')
rep('''b.box("igq", E, 8, v2(D12), "否 → 問「要在 .dockerignore 加這四行嗎」同意？（-y 免問）", 250, ax="l")''', '''b.box("igq", E, 8, v2(D12), "否 → 問「要加這四行嗎」同意？（-y 免問）", 250, ax="l")''')
rep('''b.box("igx", U, 9, v2(G12), fl("0：不寫 .dockerignore、印指示（四行；含 justfile 結果）"), 220)''', '''b.box("igx", U, 9, v2(G12), fl("0：不寫 .dockerignore；印指示（四行）"), 220)''')
rep('''b.box("ixl", L, 12, v2(W12), LXT, 140)''', '''b.box("ixl", E, 12, v2(W12), LXT, 250, ax="l")''')
rep('''b.D("ie24", "igm", "idl", al=True); b.H("ie24f", "idl", "idlf", "刪"); b.D("ie25", "idl", "ixl"); b.H("ie25l", "ixl", "iz")   # 頁尾 launcher_exit（v2.14-2）''',
    '''b.D("ie24", "igm", "idl", al=True); b.H("ie24f", "idl", "idlf", "刪"); b.D("ie25", "idl", "ixl", al=True); b.H("ie25l", "ixl", "iz")   # 頁尾 launcher_exit（v2.14-2）''')
open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("patch 2 ok")
