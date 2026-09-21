import re
P = "disc_v1_a.py"; s = open(P, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (c, old[:80])
    s = s.replace(old, new)

# ---------- 名詞表：term-diff 統一 ----------
rep(' "sync": ("sync", "每次工具 recipe 的自動前置（_sync）：比印記、比 gen/.stamp；只寫 cache/<repo>/、gen/tools.just、gen/<repo>.stamp，不碰薄殼、不寫 gen/.stamp；引擎 ref ≠ gen/.stamp 就退出 1 印 6-1（install／upgrade vendor_kit 不被擋）；無參數走快路徑"),',
    ' "sync": ("sync", "工具 recipe 的前置（工具模組內私有 _sync recipe 相依；vendor_kit 自身動詞不前置）：可寫範圍只有 cache/<repo>/、gen/tools.just、gen/<repo>.stamp（永不寫薄殼、永不寫 gen/.stamp）；範圍 = 全部工具；sync（無參數）先走快路徑"),')
rep(' "resolveapply": ("resolve／apply", "動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④"),',
    ' "resolveapply": ("resolve／apply", "會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁"),')
rep(' "symlink": ("symlink", "指向另一個路徑的捷徑檔；dev 時 cache/<repo>/ 就是指向 <dir>/dist 的 symlink（唯讀性只在容器 mount 上成立）；工具 dist/files/ 裡第一版禁止"),',
    ' "symlink": ("symlink", "指向另一個路徑的捷徑；工具的 dist/ 第一版禁止含 symlink，引擎展開時驗到就拒絕"),')
rep(' "frozen": ("frozen（CI 為真）", "CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響"),',
    ' "frozen": ("frozen（CI 為真）", "CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）。frozen 下只准寫 cache/、gen/；不查最新版（只拉鎖定版）；任何需要寫 tracked 檔的情況 → 1 印清單（-y 不解除）；警告升為失敗：薄殼不符、baseline 落後、未完成接入、任何 version.local.toml 覆寫 → 1"),')
rep(' "exit": ("結束碼 0／1／2／3", "0 成功（含 warn）；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級已改第一行後要求重跑也回 1）；2 = 有衝突要你處理，或 update --exit-code 有新版；3 = 版本／協定／schema 不合，須先升級或退回，回 3 時零寫入"),',
    ' "exit": ("結束碼 0／1／2／3", "0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）"),')
rep(' "protocol": ("--protocol P", "薄殼每次呼叫引擎都附的協定整數（第一版 P=1，在子命令之前）；引擎接受 [floor_P, current_P] 並依呼叫方 P 回應；太舊 → 一般動詞乾淨回 3 印 6-36，救援路徑永久可用"),',
    ' "protocol": ("--protocol P", "薄殼每次呼叫引擎都附的協定整數（第一版 P=1，全域旗標在子命令之前）；引擎接受 [floor_P, current_P] 並依呼叫方 P 輸出 vk-resolve/P 行別與結束碼語意；太舊 → 一般動詞乾淨回 3 印 6-36，救援路徑永久可用；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1"),')
rep(' "digestfile": (".digest 旁檔", "離線包 <name>.tar 旁的 <name>.tar.digest：一行 sha256:<hex64> = 該 image 的正式多架構 index digest；--local 用它寫 version.toml（正式 ref@digest），metadata 記 local_image_id 對照；旁檔缺 → 1"),',
    ' "digestfile": (".digest 旁檔", "<name>.tar 旁的 <name>.tar.digest：一行 sha256:<hex64> = 該 image 的正式多架構 index digest；同名旁檔須同在（缺 → 1）；--local 用它寫 version.toml（正式 ref@digest，與線上接入一模一樣，不寫本機 tag），metadata 記 local_image_id 對照"),')
rep(' "metadata": ("metadata", "baseline/<repo>/.vendor_kit.toml：schema + written_by、source（來源 ref@digest = 最後合併版本）、local_image_id、complete（完成標記）、conflicts、[[file]] dest／state／declined_hash／lines、[progress] 進度日誌"),',
    ' "metadata": ("metadata", "baseline/<repo>/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新"),')
rep(' "fingerprint": ("輸入指紋", "resolve 輸出的 sha256：對 version.toml、version.local.toml、每個 metadata、managed／appended 的 dest、gen/*.stamp 第一行、.tmp.* 清單、鎖定 digest、本機引擎 image ID、正規化 argv 串接後算；apply 拿鎖後重算，不同 → 1 印 6-12"),',
    ' "fingerprint": ("輸入指紋", "resolve 把它讀過的 version.toml、metadata、要動的使用者檔的 hash＋鎖定 digest 一起輸出；apply 拿到 flock 後重驗，不同（中間有人改了）→ 1「請重跑」"),')
rep(' "progress": ("進度日誌", "add／upgrade 記 metadata [progress]（state=in-progress、started、verb、id、done／pending）；修復型 install／remove／uninstall／undev／prune 放 .vendor_kit/.tmp.<verb>.<id>.toml（第一次 install 不建）；第一個寫入前建、最後一步刪；可寫動詞先恢復再繼續；sync／update 偵測未完成交易 → 印 6-33 結束 1；help 印 6-33 但仍 0"),',
    ' "progress": ("進度日誌", "記錄交易進度的 TOML：state=\\"in-progress\\"、verb、id、started（UTC ISO 8601）、targets、done／pending（步驟清單）、consents（已取得的同意）；存在 = 上次沒走完；add／upgrade <repo> 記在 metadata [progress]，其餘可寫動詞放 .vendor_kit/.tmp.<verb>.<id>.toml（第一次 install 不建）；可寫動詞先恢復、sync／update 印 6-33 結束 1、help 仍 0"),')
rep(' "floor": ("floor", "相容承諾的下限：固定 release 常數（第一個正式版 v1.0.0、P=1、schema=1），只能經 ADR 提高；低於 floor → 3 印 6-18 零寫入；floor 檢查在任何上網之前（啟動器可先 inspect 引擎 LABEL）"),',
    ' "floor": ("floor", "相容承諾的下限：固定 release 常數 = 第一個正式版（v1.0.0、P=1、schema=1），只能經 ADR + major 提高；低於 floor → 3 印 6-18 零寫入；floor 檢查先於任何上網（斷網也回 3；啟動器可先 inspect 引擎 LABEL）"),')
rep(' "multi": ("多工具彙總（Q27）", "不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 > 衝突 2 > 有新版 2 > 0；update 同時遇 1 與 2 → 1；訊息全列"),',
    ' "multi": ("多工具彙總（Q27）", "不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 > 衝突 2 > 有新版 2 > 0；update 同時遇 1 與 2 → 1；訊息全列（每個目標一行「現版 → 最新」）；不可同時宣稱「已是最新」；舊薄殼對未知碼原樣傳出、不吞"),')
rep(' "gitkeepline": ("gen/.stamp", "只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 <tag>）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行"),',
    ' "gitkeepline": ("gen/.stamp", "不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit"),')
rep(' "offline": ("離線可用（Q26）", "啟動器先 docker image inspect，本機有就不 pull；斷網 + 本機已有 image → sync／build 必須成功（驗收）；斷網 + 無 image → 1 印 6-31 不 hang（逾時）；離線 upgrade 不支援"),',
    ' "offline": ("離線可用（Q26）", "啟動器一律先 docker image inspect <ref>：本機有 → 不 pull（不用 --pull never，docker 19.03 無此旗標）；斷網 + 本機已有 image → sync／build 必須成功（驗收）；斷網 + 無 image → 1 + 6-31 在 --timeout 內結束、不 hang；離線 upgrade 不支援"),')
rep(' "localtoml": ("version.local.toml", "同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].<repo> = \\"path:<dir>\\" 或 vendor_kit = \\"<tag>\\" + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1"),',
    ' "localtoml": ("version.local.toml", ".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 <repo> = \\"path:<dir>\\" 或 vendor_kit = \\"<tag>\\" + image ID（成對，undev 一起撤）"),')
rep(' "initfile": ("初始檔", "工具 init.toml 列出、add 時建到專案的檔（例 Dockerfile）；歸使用者，進 git；已存在就不納管；upgrade 逐檔問；五態記在 metadata"),',
    ' "initfile": ("初始檔", "init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）"),')
# 白名單／log 名詞（v2.13 P7、v2.14-1；base 不當實例）
rep('"啟動器（POSIX sh）只准用：sh（printf、read、trap、kill、cd）、grep、sed、id、mktemp、rm、sleep、git rev-parse、docker {',
    '"啟動器（POSIX sh）只准用：sh（printf、read、trap、kill、cd）、grep、sed、id、mktemp、mkdir、date、od、tr、rm、sleep、git rev-parse、docker {')
rep('"v2.12：操作紀錄的唯一入口 log_event()（事件名 + k=v）；移植 base log.sh 到 POSIX sh 給啟動器、引擎用 Python logging + JSON formatter；事件名須在 log-events.txt 註冊（未註冊即 FATAL）；每個動詞目錄各留最近 30 天且最多 50 檔（config.toml 可調），啟動器結束時 prune"',
    '"v2.12：操作紀錄的唯一入口 log_event()（事件名 + k=v）；引擎用 Python logging + JSON formatter append 同一檔；事件註冊表 log-events.txt 真本在引擎 image（未註冊即 FATAL）；trace_id、log.sh、保留清理（keep／days）都在啟動器，引擎不做"')
rep('log.sh 由 base 移植（POSIX）、hash 記 gen/.stamp"', 'log.sh（自前身專案移植成 POSIX）同樣帶自描述首行；gen/.stamp 只記引擎 ref"')
rep(' "shellline": ("薄殼自描述首行", "entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行：',
    ' "shellline": ("薄殼自描述首行", "entry.just／vendor.just／log.sh／.gitignore 第一行、ci/check.sh 第二行：')

# ---------- v1p2 目錄樹 ----------
rep('"<b>log.sh</b> ── 進 git：啟動器 log 函式（base log.sh 移植成 POSIX；內嵌啟動器事件白名單）；hash 記 gen/.stamp\\n寫：引擎 launcher-gen｜改：人不改"',
    '"<b>log.sh</b> ── 進 git：啟動器 log 函式（自前身專案移植成 POSIX；內嵌啟動器事件白名單）；第一行自描述 # vendor_kit-shell/<P> engine=<vX> sha256=…（同其他薄殼檔）\\n寫：引擎 launcher-gen｜改：人不改"')
rep('"<b>.stamp</b> ── 引擎 ref（local 覆寫時為 <tag>）＋ log.sh hash；≠ version.toml 正規行 → sync 退出 1 印 6-1（不重寫）\\n寫：只由 install／upgrade vendor_kit｜改：人不改"',
    '"<b>.stamp</b> ── 只記引擎 ref（一行；local 覆寫時為 <tag>；不承擔薄殼 hash）；≠ version.toml 正規行 → sync 退出 1 印 6-1（不重寫）\\n寫：只由 install／upgrade vendor_kit｜改：人不改"')
rep('"<b>log/</b> ── 不進 git（目錄自帶 .gitignore：*／!.gitignore）：操作紀錄，每個動詞一個子目錄；每個子目錄各留最近 30 天且最多 50 檔（config.toml [log]）\\n寫：啟動器建檔並先寫 launcher_start（失敗 → 1 印 6-38 零寫入），引擎 append 同一檔；啟動器結束時 prune（best-effort）｜改：人不改"',
    '"<b>log/</b> ── 不進 git（目錄內 .gitignore：*／!.gitignore，由啟動器第一次建 log/ 時一起建）：操作紀錄，每個動詞一個子目錄；每個子目錄各留最近 30 天且最多 50 檔（config.toml [log]）\\n寫：啟動器 mkdir 建目錄與 .gitignore、建檔並先寫 launcher_start（失敗 → 1 印 6-38 零寫入），引擎 append 同一檔；啟動器結束時 log_prune、launcher_exit（best-effort）｜改：人不改"')
rep('rex("p2_sh", "薄殼自描述首行（entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行）"',
    'rex("p2_sh", "薄殼自描述首行（entry.just／vendor.just／log.sh／.gitignore 第一行、ci/check.sh 第二行）"')
rep(' ["自描述首行", "entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行（第一行 shebang）：',
    ' ["自描述首行", "entry.just／vendor.just／log.sh／.gitignore 第一行、ci/check.sh 第二行（第一行 shebang）：')

# ---------- v1p3b 契約④ ----------
rep('c, Y = nopend("p3b", 1260, 12, 340, "vk-resolve/1 文法（Q24）；主機命令白名單（16 條必修）；規則框逐條對應 interface_spec §3、§5，皆已定")\np3b.append(c); Y = max(Y + 16, 96)',
    'P3B_NOTE = "<b>本頁決議狀態（v2.13 結案）</b>\\n-e VENDOR_KIT_LOG_FILE 已定（v2.13 P8，spec §3.1／§5 白名單同步）；白名單加 mkdir、date、od、tr（P7）；vk-resolve/1 文法（Q24）；規則框逐條對應 interface_spec §3、§5"\np3b.append(vb("p3b_pend", "1", NP_NOTE, P3B_NOTE, 1260, 12, 340, hv(P3B_NOTE, 340, pad=10))); Y = max(12 + hv(P3B_NOTE, 340, pad=10) + 16, 96)')
rep('WL_T = ("<b>主機命令白名單（16 條必修；lint 擋清單外）</b>：sh（含內建 printf、read、trap、kill、cd）、grep、sed、id、mktemp、rm、sleep、git rev-parse、"',
    'WL_T = ("<b>主機命令白名單（16 條必修；lint 擋清單外）</b>：sh（含內建 printf、read、trap、kill、cd）、grep、sed、id、mktemp、mkdir、date、od、tr（v2.13 P7：建 log/、時間戳、trace_id）、rm、sleep、git rev-parse、"')
rep('"前提：.vendor_kit/.gitignore 明列 cache/、gen/、version.local.toml、.tmp.*；install 把 .vendor_kit/cache/、gen/、.tmp.*、log/ 加進根 .dockerignore。',
    '"前提：.vendor_kit/.gitignore 明列 cache/、gen/、log/、version.local.toml、.tmp.*；install 把 .vendor_kit/cache/、gen/、.tmp.*、log/ 加進根 .dockerignore；快路徑仍先寫 launcher_start、結束寫 sync_fast_path／launcher_exit。')
# ④′ 結束格：s4 下方
rep('S4 = "④ docker run 引擎\\napply <動詞>（掛 /dist:ro）\\n→ 結束碼 0／1／2／3 回 just"',
    'S4 = "④ docker run 引擎\\napply <動詞>（掛 /dist:ro）\\n→ 結束碼 0／1／2／3 回 just"\nS4X = "④′ 引擎結束寫 engine_exit；\\n啟動器結束寫 log_prune、\\nlauncher_exit（best-effort）"')
rep('W2 = {"s3a": 110, "s3b": 100, "s3c": 100, "s3d": 130, "s3e": 90, "s4": 180}',
    'W2 = {"s3a": 110, "s3b": 100, "s3c": 100, "s3d": 130, "s3e": 90, "s4": 180, "s4x": 230}')
rep('h2 = {k: hv(t, W2[k]) for k, t in (("s3a", S3A), ("s3b", S3B), ("s3c", S3C), ("s3d", S3D), ("s3e", S3E), ("s4", S4))}',
    'h2 = {k: hv(t, W2[k]) for k, t in (("s3a", S3A), ("s3b", S3B), ("s3c", S3C), ("s3d", S3D), ("s3e", S3E), ("s4", S4), ("s4x", S4X))}')
rep('p3b.append(v("s4", "p3L2", L12, S4, x, r2c - h2["s4"] / 2, W2["s4"], h2["s4"]))',
    'p3b.append(v("s4", "p3L2", L12, S4, x, r2c - h2["s4"] / 2, W2["s4"], h2["s4"]))\ns4xx = x + W2["s4"] / 2 - W2["s4x"] / 2\np3b += vt("s4x", "p3L2", L12, S4X, s4xx, okY, W2["s4x"], h2["s4x"], tagged=True)\np3b.append(e("s4x_e", "s4", "s4x", "", (0.5, 1), (0.5, 0), vert=True))')
rep('r3y = r2y + max(row2h, eh) + 24\nokY = r3y\nr4y = okY + okh + 24',
    'r3y = r2y + max(row2h, eh) + 24\nokY = r3y\nr4y = okY + max(okh, h2["s4x"]) + 24')

# ---------- v1p3c 驗收矩陣 35 條 ----------
rep('"契約⑤ CI 與驗收矩陣（interface_spec §7；下游 check.sh；工具 repo check.sh --dist；自身分層 + 驗收 28 條）"', '"契約⑤ CI 與驗收矩陣（interface_spec §7；下游 check.sh；工具 repo check.sh --dist；自身分層 + 驗收 35 條）"')
rep(' ["28", "驗收動詞集合", "由 vendor.just 實際列出推導（含 help、參數轉發、失敗碼）；刪掉受測物必紅"],\n]',
    ' ["28", "驗收動詞集合", "由 vendor.just 實際列出推導（含 help、參數轉發、失敗碼）；刪掉受測物必紅"],\n'
    ' ["29", "操作紀錄檔（v2.12）", "每個情境結束後 log/<verb>/ 每檔逐行 json.loads；首筆 launcher_start、末筆 launcher_exit；同檔 trace_id 單一值且 = 進度日誌 <id>；event_name 全在註冊表（CI 靜態擋未註冊者）；6-xx 同句進 body 且 message_id 相符；sync 快路徑亦有檔；自身升級接手後兩個引擎寫同一檔"],\n'
    ' ["30", "啟動器 argv 跳脫（bats）", "餵 \\"、\\\\、換行、[、]、非 ASCII、-n foo、空字串、以 \\\\ 結尾 → launcher_start.attributes.argv 經 json.loads 還原後逐項相等；dash 與 busybox sh 各跑一次"],\n'
    ' ["31", "config.toml", "keep／days 各為 0、負數、非數字、非整數、重複、缺鍵、缺檔 → 預設 50／30，除缺鍵／缺檔外印警告（與 config_read 同句）；放 51 檔或 31 天前的檔 → 任一動詞結束後被 prune，本次的檔與 .gitignore 不刪；upgrade vendor_kit 對改過的 config.toml 三方合併並詢問"],\n'
    ' ["32", "磁碟不可寫 6-38", "log/ 唯讀或磁碟滿：每個動詞（含 help、prune、sync 快路徑、--dry-run）→ 1 + 6-38、零寫入（version.toml、cache/、gen/、進度日誌、.tmp.dist.* 皆不動、不起容器）；只給引擎唯讀 → append 失敗 1 + 6-38、resolve 未執行"],\n'
    ' ["33", "bootstrap.sh 逐 -t 中止", "三個 -t，第二個故意失敗（不存在的 repo）→ 第一個 add 完成且保留、第三個未執行、整體 1 並列出已完成／未處理"],\n'
    ' ["34", "E(c) 分支", "upgrade vendor_kit@<tag>（≠ 現 ref、同 P／schema）→ 不查 registry、建 .tmp.upgrade.<id>.toml、改第一行、接手重產、刪日誌 → 1 + 6-2；CI=true upgrade vendor_kit → 不查、薄殼相符 → 0；中途殺掉接手的新引擎 → 日誌留存，sync 印 6-33 結束 1、help 印 6-33 結束 0、重跑 upgrade vendor_kit 恢復"],\n'
    ' ["35", "help 遇未完成交易", "留一個 .tmp.remove.<id>.toml → help 印 6-33 結束 0；sync／update 印 6-33 結束 1；三者除操作紀錄檔外不寫任何檔"],\n]')
rep('half = 14\nACC_COLS', 'half = 18\nACC_COLS')
rep('"驗收 §7.4 條 1–13 缺任一不得出貨；', '"驗收 §7.4 條 1–13、29–35 缺任一不得出貨；')

# ---------- v1p4 架構圖 ----------
rep('"下列為責任單元；命令步驟見流程頁與 p3b；log 前置（先寫 launcher_start 才開始）見 p12")',
    '"下列為責任單元；命令步驟見流程頁與 p3b；log 前置（先寫 launcher_start 才開始）與結束（log_prune、launcher_exit）見 p3b 契約④")')
rep('H4U = ["讀引擎 ref", "trace_id", "log_event()（log.sh）", "取得引擎／工具 image", "展開 /dist 到暫存", "起引擎容器", "vk-resolve 驗文法",\n       "協定旗標 --protocol", "清理（trap）", "pull 逾時", "資源 label", "log prune（keep／days）"]',
    'H4U = ["讀引擎 ref", "trace_id", "log_event()（log.sh：使用）", "取得引擎／工具 image", "展開 /dist 到暫存", "起引擎容器", "vk-resolve 驗文法",\n       "協定旗標 --protocol", "清理（trap）", "pull 逾時", "資源 label", "log prune（keep／days）", "launcher_exit"]')
rep('["薄殼五檔", "自描述首行", "log.sh（移植）", "tools.just（mod?）", "check.sh", ".stamp", "justfile 四行", ".dockerignore 四行"], True),',
    '["薄殼五檔", "自描述首行", "log.sh（產生）", "tools.just（mod?）", "check.sh", ".stamp", "justfile 四行", ".dockerignore 四行"], True),')
rep('("m_log", "<b>log</b>：操作紀錄（輔助模組）", ["log_event()", "log.sh（POSIX）", "Python logging", "log-events.txt", "跳脫", "trace_id", "prune keep／days"], True),',
    '("m_log", "<b>log</b>：操作紀錄（輔助模組）", ["log_event()", "Python logging", "log-events.txt", "跳脫"], True),')
rep('p4.append(e("w_cfg", "f_cfg", "m_log", "keep／days", (0, 0.5), rel("m_log", fmid("f_cfg"))))',
    'p4.append(e("w_cfg", "f_cfg", "m_log", "config_read（TOML parser；\\nupgrade 三方合併）", (0, 0.5), rel("m_log", fmid("f_cfg"))))')
# 頁首便條縮短、LY 間距、底邊兩線與標籤（w_cfg_l 上線標籤在兩線之間、w_log_l 下線標籤在其下）
rep('        "載入順序／操作順序／sync 判斷／拉取條件／退出流程一律見流程頁（p5～）。啟動器在主機跑、不算引擎模組（右上紅框）；log 為輔助模組，核心只透過 log_event() 呼叫（v2.12）。"\n        "專案根整個 -v <專案根>:/repo -w /repo 掛進引擎（可寫），引擎只寫箭頭指到的路徑；工具檔另從 .tmp.dist.<id>/ 唯讀掛 /dist/<repo>")',
    '        "順序與判斷一律見流程頁（p5～）。啟動器在主機跑、不算引擎模組（右上紅框）；log 為輔助模組，核心只透過 log_event() 呼叫（v2.12）；trace_id、log.sh、保留清理在啟動器。"\n        "專案根 -v <專案根>:/repo -w /repo 掛進引擎（可寫），引擎只寫箭頭指到的路徑；工具檔另從 .tmp.dist.<id>/ 唯讀掛 /dist/<repo>")')
rep('LY = max(HB, GB) + 70\n', 'LY = max(HB, GB) + 60\n')
rep('pts = [(HX, GY + h4h * 0.72), (22, GY + h4h * 0.72), (22, YB + 40), (log_x, YB + 40), (log_x, LY + P["f_log"] + next(h for q, y, h in pf if q == "f_log"))]\np4.append(ew("w_log_l", "h4", "f_log", "launcher_* 事件（先寫 launcher_start 才開始；與引擎 append 同一檔）", (0, 0.72), (0.65, 1), pts[1:-1], pos=pos_at(pts, 2, x=700)))',
    'pts = [(HX, GY + h4h * 0.72), (22, GY + h4h * 0.72), (22, YB + 44), (log_x, YB + 44), (log_x, LY + P["f_log"] + next(h for q, y, h in pf if q == "f_log"))]\np4.append(ew("w_log_l", "h4", "f_log", "↑ 下線：launcher_* 事件（先寫 launcher_start 才開始、結束 log_prune／launcher_exit；與引擎 append 同一檔）", (0, 0.72), (0.65, 1), pts[1:-1], lab="below", pos=pos_at(pts, 2, x=700)))')
rep('p4.append(ew("w_cfg_l", "f_cfg", "h4", "keep 正規行（grep）", (0.5, 1), (0, 0.86), pts[1:-1], lab="below", pos=pos_at(pts, 1, x=1000)))\nY = LY + LH + 50',
    'p4.append(ew("w_cfg_l", "f_cfg", "h4", "↑ 上線：keep 正規行（grep）", (0.5, 1), (0, 0.86), pts[1:-1], lab="below", pos=pos_at(pts, 1, x=1000)))\nY = LY + LH + 76')
open(P, "w", encoding="utf-8").write(s); print("ok")
