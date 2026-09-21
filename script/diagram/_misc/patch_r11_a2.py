P = "disc_v1_a.py"; s = open(P, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (c, old[:80])
    s = s.replace(old, new)
rep('"<name>.tar 旁的 <name>.tar.digest：一行 sha256:<hex64> = 該 image 的正式多架構 index digest；同名旁檔須同在（缺 → 1）；--local 用它寫 version.toml（正式 ref@digest，與線上接入一模一樣，不寫本機 tag），metadata 記 local_image_id 對照"',
    '"<name>.tar 旁的 <name>.tar.digest：一行 sha256:<hex64> = 該 image 的正式多架構 index digest（同名旁檔須同在，缺 → 1）；--local 用它寫 version.toml 正式 ref@digest（不寫本機 tag），metadata 記 local_image_id"')
rep('"<b>log.sh</b> ── 進 git：啟動器 log 函式（自前身專案移植成 POSIX；內嵌啟動器事件白名單）；第一行自描述 # vendor_kit-shell/<P> engine=<vX> sha256=…（同其他薄殼檔）\\n寫：引擎 launcher-gen｜改：人不改"',
    '"<b>log.sh</b> ── 進 git：啟動器 log 函式（POSIX；內嵌啟動器事件白名單）；第一行自描述（同其他薄殼檔）\\n寫：引擎 launcher-gen｜改：人不改"')
rep('"<b>log/</b> ── 不進 git（目錄內 .gitignore：*／!.gitignore，由啟動器第一次建 log/ 時一起建）：操作紀錄，每個動詞一個子目錄；每個子目錄各留最近 30 天且最多 50 檔（config.toml [log]）\\n寫：啟動器 mkdir 建目錄與 .gitignore、建檔並先寫 launcher_start（失敗 → 1 印 6-38 零寫入），引擎 append 同一檔；啟動器結束時 log_prune、launcher_exit（best-effort）｜改：人不改"',
    '"<b>log/</b> ── 不進 git（目錄內 .gitignore：*／!.gitignore，啟動器建 log/ 時一起建）：操作紀錄，每個動詞一個子目錄，各留最近 30 天且最多 50 檔（config.toml [log]）\\n寫：啟動器建目錄、建檔並先寫 launcher_start（失敗 → 1 印 6-38 零寫入），引擎 append 同一檔；結束時 log_prune、launcher_exit｜改：人不改"')
rep(' ["29", "操作紀錄檔（v2.12）", "每個情境結束後 log/<verb>/ 每檔逐行 json.loads；首筆 launcher_start、末筆 launcher_exit；同檔 trace_id 單一值且 = 進度日誌 <id>；event_name 全在註冊表（CI 靜態擋未註冊者）；6-xx 同句進 body 且 message_id 相符；sync 快路徑亦有檔；自身升級接手後兩個引擎寫同一檔"],',
    ' ["29", "操作紀錄檔（v2.12）", "每個情境結束後 log/<verb>/ 每檔逐行 json.loads；首筆 launcher_start、末筆 launcher_exit；同檔 trace_id 單一且 = 進度日誌 <id>；event_name 全在註冊表；6-xx 同句進 body；sync 快路徑亦有檔；自身升級兩個引擎寫同一檔"],')
rep(' ["31", "config.toml", "keep／days 各為 0、負數、非數字、非整數、重複、缺鍵、缺檔 → 預設 50／30，除缺鍵／缺檔外印警告（與 config_read 同句）；放 51 檔或 31 天前的檔 → 任一動詞結束後被 prune，本次的檔與 .gitignore 不刪；upgrade vendor_kit 對改過的 config.toml 三方合併並詢問"],',
    ' ["31", "config.toml", "keep／days 為 0、負數、非數字、非整數、重複、缺鍵、缺檔 → 預設 50／30（缺鍵／缺檔外印警告）；51 檔或 31 天前的檔 → 動詞結束後被 prune，本次的檔與 .gitignore 不刪；改過的 config.toml → upgrade vendor_kit 三方合併並詢問"],')
rep(' ["32", "磁碟不可寫 6-38", "log/ 唯讀或磁碟滿：每個動詞（含 help、prune、sync 快路徑、--dry-run）→ 1 + 6-38、零寫入（version.toml、cache/、gen/、進度日誌、.tmp.dist.* 皆不動、不起容器）；只給引擎唯讀 → append 失敗 1 + 6-38、resolve 未執行"],',
    ' ["32", "磁碟不可寫 6-38", "log/ 唯讀或磁碟滿：每個動詞（含 help、prune、sync 快路徑、--dry-run）→ 1 + 6-38、零寫入、不起容器；只給引擎唯讀 → append 失敗 1 + 6-38、resolve 未執行"],')
rep(' ["34", "E(c) 分支", "upgrade vendor_kit@<tag>（≠ 現 ref、同 P／schema）→ 不查 registry、建 .tmp.upgrade.<id>.toml、改第一行、接手重產、刪日誌 → 1 + 6-2；CI=true upgrade vendor_kit → 不查、薄殼相符 → 0；中途殺掉接手的新引擎 → 日誌留存，sync 印 6-33 結束 1、help 印 6-33 結束 0、重跑 upgrade vendor_kit 恢復"],',
    ' ["34", "E(c) 分支", "upgrade vendor_kit@<tag>（≠ 現 ref、同 P／schema）→ 不查 registry、建 .tmp.upgrade.<id>.toml、改第一行、接手重產、刪日誌 → 1 + 6-2；CI=true 且薄殼相符 → 0；中途殺掉新引擎 → 日誌留存，sync 6-33 結束 1、help 6-33 結束 0、重跑恢復"],')
open(P, "w", encoding="utf-8").write(s); print("ok")
