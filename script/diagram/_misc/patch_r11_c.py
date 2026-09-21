P = "disc_v1_c.py"; s = open(P, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (c, old[:80])
    s = s.replace(old, new)

MULTI = '("多工具彙總（Q27）", "不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 > 衝突 2 > 有新版 2 > 0；update 同時遇 1 與 2 → 1；訊息全列（每個目標一行「現版 → 最新」）；不可同時宣稱「已是最新」；舊薄殼對未知碼原樣傳出、不吞")'
FROZEN = '("frozen（CI 為真）", "CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）。frozen 下只准寫 cache/、gen/；不查最新版（只拉鎖定版）；任何需要寫 tracked 檔的情況 → 1 印清單（-y 不解除）；警告升為失敗：薄殼不符、baseline 落後、未完成接入、任何 version.local.toml 覆寫 → 1")'
# ---- 共用名詞（term-diff）----
rep('EXIT4 = ("結束碼 0／1／2／3", "0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）")',
    'EXIT4 = ("結束碼 0／1／2／3", "0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）")\n'
    'LOGT_C = ("操作紀錄檔／log（v2.12）", ".vendor_kit/log/<verb>/<UTC 時間戳>-<id8>.jsonl，每次執行一檔（JSON Lines：timestamp、event_name、body、trace_id…）；啟動器先建檔寫 launcher_start、引擎 resolve 前 append engine_start（失敗 → 1 + 6-38）；tty 訊息同句進 body；結束時 prune（30 天／50 檔）；不進 git；事件註冊表 log-events.txt 真本在引擎 image，log.sh 內嵌啟動器事件白名單")')
rep(' ("多工具彙總（Q27）", "做得完的做完；最後回最需要處理的碼：失敗 1 > 衝突 2 > 有新版 2 > 0；update 同時遇 1 與 2 → 1；訊息全列（每個目標一行「現版 → 最新」）；不可同時宣稱「已是最新」"),', ' ' + MULTI + ',')
rep(' ("多工具彙總（Q27）", "不帶 repo 的動詞先完整預檢（任一預檢失敗才整體不動）、做得完的做完，最後回最需要處理的碼：1 > 衝突 2 > 有新版 2 > 0；update 同時遇 1 與 2 → 1；訊息全列；舊薄殼對未知碼原樣傳出、不吞"),', ' ' + MULTI + ',')
rep(' ("frozen（CI 為真）", "CI 非空且不為 0／false → 不寫 tracked 檔、不查最新版；需改 tracked 檔 → 1 印清單（與 -y 無關）；6-6～6-8 提醒不紅燈；update 不受限"),', ' ' + FROZEN + ',')
rep(' ("--protocol P", "薄殼每次呼叫附 --protocol P（第一版起 P=1；全域旗標在子命令前）；引擎以呼叫方的 P 輸出 vk-resolve/P 行別與結束碼語意；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1"),',
    ' ("--protocol P", "薄殼每次呼叫引擎都附的協定整數（第一版 P=1，全域旗標在子命令之前）；引擎接受 [floor_P, current_P] 並依呼叫方 P 輸出 vk-resolve/P 行別與結束碼語意；太舊 → 一般動詞乾淨回 3 印 6-36，救援路徑永久可用；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1"),')
rep(' ("floor", "固定 release 常數 = 第一個正式版（v1.0.0、P=1、schema=1）；只能經 ADR + major 提高；低於 floor → 3 + 6-18 零寫入；floor 檢查先於任何上網（斷網也回 3）"),',
    ' ("floor", "相容承諾的下限：固定 release 常數 = 第一個正式版（v1.0.0、P=1、schema=1），只能經 ADR + major 提高；低於 floor → 3 印 6-18 零寫入；floor 檢查先於任何上網（斷網也回 3）"),')
rep(' ("驗收（§7.4）", "floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture 驅動候選（線性，非兩兩相乘）；連升 r_i → r_j → C；floor 直接跳升；降版；< floor 用唯一 synthetic；舊引擎讀新檔 3 零寫入；已釋出 image／Release 資產／fixture 永不刪"),',
    ' ("驗收（§7.4 相容性條）", "floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture 驅動候選（線性，非兩兩相乘）；連升 r_i → r_j → C；floor 直接跳升；降版；< floor 用唯一 synthetic；舊引擎讀新檔 3 零寫入；已釋出 image／Release 資產／fixture 永不刪"),')
rep(' ("bootstrap.sh", "release 附的 POSIX sh 薄層，內嵌所屬引擎的完整 ref（ghcr.io/<org>/vendor_kit:vN@sha256:<index digest>）；', ' ("bootstrap.sh（release 資產）", "release 附的 POSIX sh 薄層，內嵌所屬引擎的完整 ref（ghcr.io/<org>/vendor_kit:vN@sha256:<index digest>）；')
rep(' ("B／D／N", "B = baseline（上次合併的範本副本）、D = 磁碟上使用者的檔、N = 新版範本（讀自暫存 /dist/<repo>，不是 cache）；upgrade 逐檔判斷只對 state=managed 且無待解衝突"),',
    ' ("B／D／N", "B = baseline（上次合併時的範本副本，進 git）；D = 現況（專案裡你的那份檔）；N = 目標版範本 = 啟動器把目標版 image 展開到暫存、掛進引擎的 /dist/<repo>（不是 cache；v2.5 §2）；「D==B」= 你沒改過"),')
rep(' (".digest 旁檔", "<name>.tar.digest 一行 sha256:<hex64> = 該 image 的正式多架構 index digest；同名旁檔須同在（缺 → 1）；version.toml 仍寫正式 ref@digest（與線上接入一模一樣），不寫本機 tag"),',
    ' (".digest 旁檔", "<name>.tar 旁的 <name>.tar.digest：一行 sha256:<hex64> = 該 image 的正式多架構 index digest（同名旁檔須同在，缺 → 1）；--local 用它寫 version.toml 正式 ref@digest（不寫本機 tag），metadata 記 local_image_id"),')
rep(' ("version.local.toml", "不進 git；--local 時寫 vendor_kit = \\"<tag>\\" + vendor_kit_image_id（install 成功後才寫、失敗清除）；之後啟動器每次 docker image inspect 比對 ID、不 pull"),',
    ' ("version.local.toml", ".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 <repo> = \\"path:<dir>\\" 或 vendor_kit = \\"<tag>\\" + image ID（成對，undev 一起撤）"),')
rep(' ("離線可用（Q26）", "啟動器一律先 docker image inspect <ref>：本機有 → 不 pull（不用 --pull never，docker 19.03 無此旗標）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → 1 + 6-31 在 --timeout 內結束、不 hang"),',
    ' ("離線可用（Q26）", "啟動器一律先 docker image inspect <ref>：本機有 → 不 pull（不用 --pull never）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → 1 + 6-31 在 --timeout 內結束、不 hang；離線 upgrade 不支援"),')
# ---- 名詞表加操作紀錄檔（prune／update／離線包） ----
rep(' ("log/（不在 prune 範圍）", "log/<verb>/*.jsonl 舊檔（30 天且 ≤ 50 檔；config.toml 可調）由啟動器每次結束時自行清，不屬 prune；prune 不碰 log/"),',
    ' LOGT_C,\n ("log/（不在 prune 範圍）", "log/<verb>/*.jsonl 舊檔（30 天且 ≤ 50 檔；config.toml 可調）由啟動器每次結束時自行清（log_prune），不屬 prune；prune 不碰 log/"),')
rep(' ("frozen", "CI 非空且不為 0／false → frozen：不寫 tracked 檔、不查最新版；update 是唯讀動詞，不受 frozen 影響（CI 裡也能查）"),\n T_MSG, EXIT4,',
    ' ("frozen", "CI 非空且不為 0／false → frozen：不寫 tracked 檔、不查最新版；update 是唯讀動詞，不受 frozen 影響（CI 裡也能查）"),\n LOGT_C, T_MSG, EXIT4,')
rep(' ("sync 快路徑（Q22）／--verify（F5）", ', ' LOGT_C,\n ("sync 快路徑（Q22）／--verify（F5）", ')

# ---- 圖例：8 頁補 v2 ----
for pg in ("p9", "p10", "p15", "p15c", "p16", "p16c"):
    pass
rep('foot(p9, "p9", F.y, T9, ALLC - {"inv", "pend", "tree", "rule", "img", "v2", "state", "entry", "c0", "cx", "c1", "cell"})', 'foot(p9, "p9", F.y, T9, ALLC - {"inv", "pend", "tree", "rule", "img", "state", "entry", "c0", "cx", "c1", "cell"})')
rep('foot(p10, "p10", F.y, T10, ALLC - {"inv", "pend", "tree", "img", "v2", "state", "entry", "c0", "cx", "c1", "cell"})', 'foot(p10, "p10", F.y, T10, ALLC - {"inv", "pend", "tree", "img", "state", "entry", "c0", "cx", "c1", "cell"})')
rep('foot(p11, "p11", F.y, T11, {"note", "state"})', 'foot(p11, "p11", F.y, T11, {"note", "state", "v2"})')
rep('foot(p12, "p12", F.y, T12, {"note", "rule", "inv", "sub", "hdr", "entry"})', 'foot(p12, "p12", F.y, T12, {"note", "rule", "inv", "sub", "hdr", "entry", "v2"})')
rep('foot(p15, "p15", F.y, T15, ALLC - {"inv", "pend", "tree", "sub", "v2", "state", "entry", "c0", "cx", "c1", "cell"})', 'foot(p15, "p15", F.y, T15, ALLC - {"inv", "pend", "tree", "sub", "state", "entry", "c0", "cx", "c1", "cell"})')
rep('foot(p15c, "p15c", F.y, T15, ALLC - {"inv", "pend", "tree", "sub", "rule", "v2", "state", "c0", "cx", "c1", "cell"})', 'foot(p15c, "p15c", F.y, T15, ALLC - {"inv", "pend", "tree", "sub", "rule", "state", "c0", "cx", "c1", "cell"})')
rep('ALLC - {"inv", "pend", "tree", "v2", "state", "entry", "c0", "cx", "c1", "cell"})\npages_v1_c.append(("v1p16",', 'ALLC - {"inv", "pend", "tree", "state", "entry", "c0", "cx", "c1", "cell"})\npages_v1_c.append(("v1p16",')
rep('ALLC - {"inv", "pend", "tree", "v2", "state", "c0", "cx", "c1", "cell"})\npages_v1_c.append(("v1p16c",', 'ALLC - {"inv", "pend", "tree", "state", "c0", "cx", "c1", "cell"})\npages_v1_c.append(("v1p16c",')

# ---- p9 prune：daemon 欄結果框 → 便條（非步驟；lint dangling）----
rep('b.box("q7d", DK, 5, W12, "列出帶 label 的四類資源：容器、image、network、volume", 300)', 'b.box("q7d", DK, 5, NOTE, "結果：列出帶 label 的四類資源：容器、image、network、volume", 300)')
rep('b.box("q11ad", DK, 11, W12, "容器被刪", 300)', 'b.box("q11ad", DK, 11, NOTE, "結果：容器被刪", 300)')
rep('b.box("q11bd", DK, 12, W12, "image 被刪（keep 內的 image 保留）", 300)', 'b.box("q11bd", DK, 12, NOTE, "結果：image 被刪（keep 內的 image 保留）", 300)')
rep('b.box("q11cd", DK, 13, W12, "network 被刪", 300)', 'b.box("q11cd", DK, 13, NOTE, "結果：network 被刪", 300)')
rep('b.box("q11dd", DK, 14, W12, "volume 被刪", 300)', 'b.box("q11dd", DK, 14, NOTE, "結果：volume 被刪", 300)')

# ---- p11：轉入／upgrade 說明框 → 便條樣式 ----
for k in ("in_d", "in_m", "in_c", "in_a", "in_u", "up_d", "up_m", "up_c", "up_a", "up_u"):
    rep(f'b.box("{k}", ', f'b.box("{k}", ', 1)
import re as _re
s = _re.sub(r'b\.box\("(in_[dmcau]|up_[dmcau])", (S[DMCAU]), ([23]), W12, ', r'b.box("\1", \2, \3, NOTE, ', s)
assert s.count(', NOTE, "轉入：') == 5 and s.count(', NOTE, "upgrade 時') == 5

# ---- p12：dry-run 出口拆（CI 例外進規則框）；help 出口改成獨立菱形 ----
rep('b.box("t3y", U, 2, G12, "是 → 0：唯讀預覽（CI 為真且需改 tracked 檔 → 1）；不建日誌", 240)',
    'b.box("t3y", U, 2, G12, "是 → 0：唯讀預覽；不建日誌（CI 例外見右）", 240)')
rep('b.box("t3", EA, 2, D12, "--dry-run？", 200, ax="l")',
    'b.box("t3", EA, 2, D12, "--dry-run？", 200, ax="l")\nb.box("t3n", XA, 2, RULE, "已定：--dry-run = 唯讀預覽（本機一律 0）；CI 為真且需改 tracked 檔時回 1 印清單（契約⑤ p3c check.sh ③）；不建日誌、不寫任何檔", 390)')
rep('b.box("r3x", U, 5, O12, "否（sync／update）→ 1 + 6-33：請先重跑原動詞（不恢復、不寫檔）", 240)\nb.box("r3", EA, 5, D12, "本動詞可寫？（修復型 install／add／remove／upgrade／undev／uninstall）", 400, ax="l")',
    'b.box("r2hy", U, 4, G12, "是（help）→ 0：印 6-33 後照常印說明（不受影響）", 240)\nb.box("r2h", EA, 4, D12, "否：本動詞是 help？", 220, ax=90)\n'
    'b.box("r3x", U, 5, O12, "否（sync／update）→ 1 + 6-33：請先重跑原動詞（不恢復、不寫檔）", 240)\nb.box("r3", EA, 5, D12, "否：本動詞可寫？（修復型 install／add／remove／upgrade／undev／uninstall）", 400, ax="l")')
rep('b.box("r3hy", U, 6, G12, "否（help）→ 0：印 6-33 後照常印說明（不受影響）", 240)\n', '')
rep('b.D("re4", "r2", "r2p", "是", al=True); b.H("re4p", "r2p", "r2px", "是"); b.D("re4n", "r2p", "r3", "否", al=True)',
    'b.D("re4", "r2", "r2p", "是", al=True); b.H("re4p", "r2p", "r2px", "是"); b.D("re4n", "r2p", "r2h", "否", al=True)\nb.H("re4h", "r2h", "r2hy", "是"); b.D("re4hn", "r2h", "r3", "否", al=True)')
rep('_A = geo(b); _rx, _ry, _rw, _rh = _A["r3"]; _hx, _hy, _hw, _hh = _A["r3hy"]\nb.P("re5h", "r3", "r3hy", "", (0, 0.75), (1, 0.5), [(_rx - 10, _ry + 0.75 * _rh), (_rx - 10, _hy + _hh / 2)])   # help 的獨立出口：菱形左下邊出、進 r3hy 右側（v2.10-6）\n', '')
rep('"已定（v2.6-9、v2.10-6）：唯讀動詞遇未完成交易只提示重跑原動詞，不自動恢復；sync／update 印 6-33 結束 1；help 印 6-33 仍 0（獨立出口）"',
    '"已定（v2.6-9、v2.10-6）：唯讀動詞遇未完成交易只提示重跑原動詞，不自動恢復；sync／update 印 6-33 結束 1；help 印 6-33 仍 0（上一個菱形獨立出口）"')

# ---- p16 離線包(1)：launcher_start 獨立格、install 失敗紅出口 ----
rep('N16 = "已定（Q26、v2.4-10 19條-11、v2.6-1、v2.7-1／-2、v2.8-4／-5、interface_spec §1.2、§4.8、§7.4-16／17）：契約入口 = bootstrap.sh --local <引擎 tar>，只涉及引擎（local_bootstrap.sh 只是包內便利包裝、非契約）；-t <repo> 走 registry（需網路），離線接工具 = 使用者另備工具 tar（工具 repo 提供）→ add <repo> --local <工具 tar>；前置檢查（git repo？just ≥ 1.33？）不分 --local 值型別一律先做（v2.9-1）；--local 值三分支：含 / 或 .tar 結尾 → 檔案（先驗存在，否則 1）、其餘 tag（不 load、不讀 .digest，只 inspect image ID）、既存檔且可解讀為 tag → 1 + 6-37；每個 tar 附同名 .digest 旁檔；version.toml 寫正式 ref@digest、metadata／local 記 image ID；啟動器先 docker image inspect、本機有就不 pull；離線 upgrade 不支援。"',
    'N16 = "已定（Q26、v2.6-1、v2.7-1／-2、v2.8-4／-5、v2.13 P4、interface_spec §1.2、§4.8、§7.4-16／17）：契約入口 = bootstrap.sh --local <引擎 tar>，只涉及引擎（local_bootstrap.sh 為便利包裝、非契約）；先建 log/bootstrap/ 寫 launcher_start 才開始；前置檢查不分 --local 值型別一律先做；--local 三分支（檔案先驗存在／tag 不 load 不讀 .digest／兩者皆成立 → 1 + 6-37）；每個 tar 附同名 .digest；version.toml 寫正式 ref@digest；install 失敗 → 1 清半成品、保留 log/；離線接工具 = 另備工具 tar → add --local；離線 upgrade 不支援。"')
rep('b.box("o2", UO, 6, W12, "sh bootstrap.sh --local <引擎 tar> [-y]（契約入口；先建 log/bootstrap/ 並寫 launcher_start；-t <repo> 走 registry 需網路，離線機不帶）", 230)\nb.box("o2l", SH, 6, LBL, "↓ 前置檢查（v2.9-1：不分 --local 值是 tar 還是 tag，一律先做）", 400, 24, ax="l", minh=24)',
    'b.box("o2", UO, 6, W12, "sh bootstrap.sh --local <引擎 tar> [-y]（契約入口；-t <repo> 走 registry 需網路，離線機不帶）", 230)\nb.box("o2s", SH, 6, v2(W12), "先建 log/bootstrap/<ts>-<id8>.jsonl 並寫 launcher_start（失敗 → 1 + 6-38，零寫入）", 400)')
rep('b.box("o5", SH, 7, D12, "在 git repo 內？", 300, ax="l")', 'b.box("o5", SH, 7, D12, "前置檢查①（不分 tar／tag）：在 git repo 內？", 300, ax="l")')
rep('b.box("o6", SH, 8, D12, "just ≥ 1.33.0？", 300, ax="l")', 'b.box("o6", SH, 8, D12, "前置檢查②：just ≥ 1.33.0？", 300, ax="l")')
rep('b.box("o8", SH, 16, W12, "docker run 本機 image install（本機有 → 不 pull；失敗 → 1：清半成品、保留 log/）", 400)', 'b.box("o8", SH, 16, W12, "docker run 本機 image install（本機有 → 不 pull）", 400)')
rep('b.box("o9", SH, 17, W12, "install 成功後寫 version.local.toml：vendor_kit = \\"vendor_kit:vN\\" + vendor_kit_image_id（失敗清除）", 400)\nb.box("o9f", P, 17, F12, "version.local.toml（不進 git）：本機 tag + image ID", 280)\nb.box("o9z", SH, 18, LBL,',
    'b.box("o8x", UO, 17, v2(R12), "是 → 1：中止（清半成品、保留 log/；version.local.toml 未寫）", 230)\nb.box("o8q", SH, 17, D12, "install 失敗？", 220, ax="l")\n'
    'b.box("o9", SH, 18, W12, "否：install 成功後寫 version.local.toml：vendor_kit = \\"vendor_kit:vN\\" + vendor_kit_image_id", 400)\nb.box("o9f", P, 18, F12, "version.local.toml（不進 git）：本機 tag + image ID", 280)\nb.box("o9z", SH, 19, LBL,')
rep('b.H("oe2", "o2", "o2l"); b.D("oe2l", "o2l", "o5", al=True)', 'b.H("oe2", "o2", "o2s"); b.D("oe2l", "o2s", "o5", al=True)')
rep('b.D("oe13", "o8", "o9"); b.H("oe14", "o9", "o9f", "寫"); b.D("oe15", "o9", "o9z", al=True)',
    'b.D("oe13", "o8", "o8q", al=True); b.H("oe13x", "o8q", "o8x", "是"); b.D("oe13n", "o8q", "o9", "否", al=True); b.H("oe14", "o9", "o9f", "寫"); b.D("oe15", "o9", "o9z", al=True)')
rep('b.box("o7bd", DK, 15, W12, "回 image ID（sha256:<hex64>）", 170, ax="l")', 'b.box("o7bd", DK, 15, NOTE, "結果：回 image ID（sha256:<hex64>）", 170, ax="l")')
# ---- p16c：resolve 段接回、image ID 結果框、inspect 出線改由 w2 發 ----
rep('b.box("o10cd", DK, 7, W12, "回 image ID（sha256:<hex64>）", 240)', 'b.box("o10cd", DK, 7, NOTE, "結果：回 image ID（sha256:<hex64>）", 240)')
rep('b.box("o10re", E, 8, SUB, "resolve（不寫）：算計畫、指紋；stdout vk-resolve/1", 320)', 'b.box("o10re", E, 8, SUB, "resolve（不寫）：算計畫、指紋；stdout vk-resolve/1 回啟動器", 320)')
rep('b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.D("oe26", "o10r", "o10p")', 'b.D("oe25", "o10c", "o10r"); b.H("oe25e", "o10r", "o10re"); b.DL("oe26", "o10re", "o10p", "vk-resolve")')
rep('b.box("w3d", DK, 2, IMG, "本機已有 image（docker load 過的）", 240)', 'b.box("w3d", DK, 1, IMG, "本機已有 image（docker load 過的）", 240)')
rep('b.H("we4", "w3", "w3d", "inspect")', 'b.H("we4", "w2", "w3d", "inspect")')
open(P, "w", encoding="utf-8").write(s); print("ok")
