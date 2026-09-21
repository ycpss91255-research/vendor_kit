"""第八輪：disc_v1_c.py（v2.9 + review_v2r7_findings.md 必修＋選修）。"""
p = "disc_v1_c.py"; s = open(p, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:100])
    s = s.replace(old, new)

# ================= P16 離線包（1）：前置檢查（o5/o6）移到 --local 判別之前；tag 形只跳過 docker load／讀 .digest；o3t 不再與 o3b 重疊 =================
start = s.index('b = F.band("bO1", ')
end = s.index('b.close()\nfoot(p16, "p16"')
new16 = '''b = F.band("bO1", "離線接入（1）只涉及引擎：離線包 →（可選 local_bootstrap.sh 挑 tar）→ bootstrap.sh --local <引擎 tar>（契約入口；不帶 -t）→ 前置檢查（git repo／just，不分 tar／tag）→ 判別值三分支 → tar 形 docker load + 讀 .digest（tag 形跳過）→ image ID → install → version.local.toml", v2=True)
b.box("o0", UO, 0, G12, "有網路的機器下載 vendor_kit-vN-local.tar.gz（SHA256SUMS 驗）→ 帶到離線機", 230)
b.box("o1", UO, 1, W12, "解開：bootstrap.sh、各平台引擎 tar + .tar.digest（另附 local_bootstrap.sh）；不含工具 tar", 230)
b.box("o1w", UO, 2, LBL, "【便利包裝，非契約】（可選）sh local_bootstrap.sh [-y] 做三步：", 230, 24, ax="l", minh=24)
b.box("o1a", UO, 3, W12, "docker version --format '{{.Server.Arch}}' 偵測 daemon 架構", 230)
b.box("o1b", UO, 4, W12, "挑該平台的引擎 tar（vendor_kit-vN-<arch>.tar）", 230)
b.box("o1c", UO, 5, W12, "exec ./bootstrap.sh --local <tar> \\"$@\\"", 230)
b.box("o2", UO, 6, W12, "sh bootstrap.sh --local <引擎 tar> [-y]（契約入口；-t <repo> 走 registry 需網路，離線機不帶）", 230)
b.box("o2l", SH, 6, LBL, "↓ 前置檢查（v2.9-1：不分 --local 值是 tar 還是 tag，一律先做）", 400, 24, ax="l", minh=24)
b.box("o5x", UO, 7, O12, "否 → 1 + 6-16：請先 git init", 230)
b.box("o5", SH, 7, D12, "在 git repo 內？", 300, ax="l")
b.box("o6x", UO, 8, O12, "否 → 1 + 6-23：請裝 GitHub release 版 just", 230)
b.box("o6", SH, 8, D12, "just ≥ 1.33.0？", 300, ax="l")
b.box("o3", SH, 9, D12, "--local 值含 / 或以 .tar 結尾？", 300, ax="l")
b.box("o3n", P, 9, RULE, "已定（B1；grilling 2026-09-19 末條、v2.7-2、v2.8-4、v2.9-1）三分支：值含 / 或以 .tar 結尾 → 檔案路徑（先驗存在，否則 1）→ docker load；其餘 → image tag（不 load、不讀 .digest）；既存檔且可解讀為 tag → 1 + 6-37 消歧（請寫 ./<v> 或完整 ref）；前置檢查（git repo／just）不分型別一律先做", 280)
b.box("o3bx", UO, 10, R12, "否 → 1：檔案路徑必須存在", 230)
b.box("o3b", SH, 10, D12, "該路徑的檔案存在？", 240, ax="l")
b.box("o3t", SH, 10, W12, "否 → image tag 形：不 docker load、不讀 .digest；本機須已有該 image（inspect 無 → 1）", 140, ax="r")
b.box("o3cx", UO, 11, R12, "是 → 1 + 6-37：既是存在的檔案也可解讀為 image tag（請寫 ./<v> 或完整 ref）", 230)
b.box("o3c", SH, 11, D12, "值同時可解讀為 image tag？", 240, ax="l")
b.box("o4x", UO, 12, R12, "否 → 1：同名 .tar.digest 旁檔缺", 230)
b.box("o4", SH, 12, D12, "同名 .tar.digest 存在？", 240, ax="l")
b.box("o6c", SH, 13, W12, "docker load < <引擎 tar>", 300, ax="l")
b.box("o6d", DK, 13, IMG, "本機 image vendor_kit:vN（只有 tag、無 RepoDigests）", 170, ax="l")
b.box("o7a", SH, 14, W12, "讀 <tar>.digest → 正式 index digest", 300, ax="l")
b.box("o7b", SH, 15, W12, "docker image inspect --format '{{.Id}}' → image ID（tag 形由此匯入：跳過 load 與 .digest）", 400)
b.box("o7bd", DK, 15, W12, "回 image ID（sha256:<hex64>）", 170, ax="l")
b.box("o8", SH, 16, W12, "docker run 本機 image install（本機有 → 不 pull）", 400)
b.box("o8e", E, 16, SUB, "install：建薄殼四檔、gen/.stamp、baseline/.gitkeep；version.toml 第一行 = 正式 ref@digest（tar 形來自 .digest；tag 形用既有 version.toml 值）", 320)
b.files("o8f", P, 16, "install 寫", ["version.toml 第一行（正式 ref@sha256:<index digest>）", "薄殼四檔、gen/.stamp、baseline/.gitkeep、根 justfile 一行、.dockerignore 三行"], 280)
b.box("o9", SH, 17, W12, "install 成功後寫 version.local.toml：vendor_kit = \\"vendor_kit:vN\\" + vendor_kit_image_id（失敗清除）", 400)
b.box("o9f", P, 17, F12, "version.local.toml（不進 git）：本機 tag + image ID", 280)
b.box("o9z", SH, 18, LBL, "↓ 續「離線包（2）」頁：工具由使用者另備工具 tar，逐一 add <repo> --local <工具 tar>；之後斷網 sync", 400, 24, ax="l", minh=24)
b.D("oe0", "o0", "o1"); b.D("oe1", "o1", "o1w", al=True); b.D("oe1a", "o1w", "o1a", al=True); b.D("oe1b", "o1a", "o1b"); b.D("oe1c", "o1b", "o1c"); b.D("oe1w", "o1c", "o2")
b.H("oe2", "o2", "o2l"); b.D("oe2l", "o2l", "o5", al=True)
b.H("oe6x", "o5", "o5x", "否"); b.D("oe6b", "o5", "o6", "是", al=True); b.H("oe6bx", "o6", "o6x", "否"); b.D("oe6c", "o6", "o3", "是", al=True)
b.RD("oe3t", "o3", "o3t", "否"); b.D("oe3b", "o3", "o3b", "是", al=True); b.H("oe3bx", "o3b", "o3bx", "否")
b.D("oe3c", "o3b", "o3c", "是", al=True); b.H("oe3cx", "o3c", "o3cx", "是")
b.D("oe4", "o3c", "o4", "否", al=True); b.H("oe5", "o4", "o4x", "否"); b.D("oe7", "o4", "o6c", "是", al=True)
b.H("oe8", "o6c", "o6d", "載"); b.D("oe9", "o6c", "o7a"); b.D("oe9b", "o7a", "o7b", al=True); b.H("oe9d", "o7b", "o7bd"); b.D("oe10", "o7b", "o8")
_A = geo(b); _tx, _ty, _tw, _th = _A["o3t"]; _bx, _by, _bw, _bh = _A["o7b"]; _gy = _by - F.gap / 2   # tag 形匯入：繞 daemon 欄右側（x=910）下來，從列間縫隙進 o7b 頂端（不穿「載」線）
b.P("oe3tj", "o3t", "o7b", "tag 形：跳過 load／.digest，直接 inspect", (1, 0.5), (round((650 - _bx) / _bw, 3), 0), [(910, _ty + _th / 2), (910, _gy), (650, _gy)], pos=-0.85, vert="below")
b.H("oe11", "o8", "o8e"); b.H("oe12", "o8e", "o8f", "寫")
b.D("oe13", "o8", "o9"); b.H("oe14", "o9", "o9f", "寫"); b.D("oe15", "o9", "o9z", al=True)
'''
s = s[:start] + new16 + s[end:]
rep('''p16, F = newpage_c("流程 v2：離線包（1）── bootstrap.sh --local <引擎 tar> → load → install（#27、Q26、§4.8）", N16, COLS_OF)''',
    '''p16, F = newpage_c("流程 v2：離線包（1）── bootstrap.sh --local <引擎 tar> → load → install（#27、Q26、§4.8）", N16, COLS_OF, gap=16)''')
rep('''--local 值三分支：含 / 或 .tar 結尾 → 檔案（先驗存在，否則 1）、其餘 tag、既存檔且可解讀為 tag → 1 + 6-37；每個 tar 附同名 .digest 旁檔；''',
    '''前置檢查（git repo？just ≥ 1.33？）不分 --local 值型別一律先做（v2.9-1）；--local 值三分支：含 / 或 .tar 結尾 → 檔案（先驗存在，否則 1）、其餘 tag（不 load、不讀 .digest，只 inspect image ID）、既存檔且可解讀為 tag → 1 + 6-37；每個 tar 附同名 .digest 旁檔；''')
rep(''' ("bootstrap.sh --local（契約入口）", "離線接入的契約入口 = bootstrap.sh --local <引擎 tar>（interface_spec §1.2）：只涉及引擎（docker load → install）；-t <repo> 仍是 add <repo>[@tag]，走 registry、需網路，離線機不帶 -t；--local 值的判別（B1）：含 / 或以 .tar 結尾 → 檔案路徑（先驗存在，否則 1）；其餘 → image tag；兩者皆成立（既存檔且可解讀為 tag）→ 1 + 6-37「請寫 ./<v> 或完整 ref」"),''',
    ''' ("bootstrap.sh --local（契約入口）", "離線接入的契約入口 = bootstrap.sh --local <引擎 tar>（interface_spec §1.2）：只涉及引擎（docker load → install）；-t <repo> 仍是 add <repo>[@tag]，走 registry、需網路，離線機不帶 -t；前置檢查（git repo、just ≥ 1.33.0）不分值型別一律先做；--local 值的判別（B1）：含 / 或以 .tar 結尾 → 檔案路徑（先驗存在，否則 1）→ docker load + 讀 .digest；其餘 → image tag（不 load、不讀 .digest，只 inspect image ID）；兩者皆成立（既存檔且可解讀為 tag）→ 1 + 6-37「請寫 ./<v> 或完整 ref」"),''')

# ================= P16c 離線包（2）：o10p 拆 create/cp／docker run；o10e 拆 flock／重驗／寫入 =================
rep('''b.box("o10p", LA, 8, W12, "docker create／cp 取本機 image 的 dist（不 pull）→ docker run 引擎 apply add", 400)
b.box("o10e", E, 8, SUB, "apply add：flock → 重驗指紋 → 寫入（version.toml [tools] 正式 ref@digest；metadata 記 local_image_id）", 320)
b.files("o10f", P, 8, "add 寫", ["version.toml [tools] 行（正式 ref@digest）", "baseline/<repo>/.vendor_kit.toml：source + local_image_id", "cache/<repo>/、gen/<repo>.stamp（第一行 = index digest）"], 280)
b.box("o11", UO, 9, G12, "0：該工具離線接入完成；version.toml 與線上接入一模一樣（可 commit、Renovate 可讀）；下一個工具再跑一次 add", 230)''',
    '''b.box("o10p", LA, 8, W12, "docker create／cp 取本機 image 的 dist 到暫存（不 pull）", 400)
b.box("o10p2", LA, 9, W12, "docker run 引擎 apply add（暫存唯讀掛進 /dist）", 400)
b.box("o10e", E, 9, SUB, "apply add：拿 flock 專案目錄（60 秒；逾時 → 1 + 6-26）", 320)
b.box("o10e2", E, 10, SUB, "重驗指紋（與 vk-resolve 的 fingerprint 比；不同 → 1 + 6-12「請重跑」）", 320)
b.box("o10e3", E, 11, SUB, "寫入（見「add（2）」頁）：version.toml [tools] 正式 ref@digest；metadata 記 local_image_id", 320)
b.files("o10f", P, 11, "add 寫", ["version.toml [tools] 行（正式 ref@digest）", "baseline/<repo>/.vendor_kit.toml：source + local_image_id", "cache/<repo>/、gen/<repo>.stamp（第一行 = index digest）"], 280)
b.box("o11", UO, 12, G12, "0：該工具離線接入完成；version.toml 與線上接入一模一樣（可 commit、Renovate 可讀）；下一個工具再跑一次 add", 230)''')
rep('''b.H("oe26e", "o10p", "o10e"); b.H("oe27", "o10e", "o10f", "寫"); b.DL("oe28", "o10p", "o11")''',
    '''b.D("oe26b", "o10p", "o10p2"); b.H("oe26e", "o10p2", "o10e"); b.D("oe26f", "o10e", "o10e2"); b.D("oe26g", "o10e2", "o10e3"); b.H("oe27", "o10e3", "o10f", "寫"); b.DL("oe28", "o10e3", "o11")''')
rep('''p16c, F = newpage_c("流程 v2：離線包（2）── 另備工具 tar → add --local 逐工具 → 斷網 sync（Q26、§4.8、§7.4-17）", N16, COLS_OF2)''',
    '''p16c, F = newpage_c("流程 v2：離線包（2）── 另備工具 tar → add --local 逐工具 → 斷網 sync（Q26、§4.8、§7.4-17）", N16, COLS_OF2, gap=16)''')
rep('''：判別值 → docker load → 讀 .digest → inspect image ID → 引擎 resolve → apply", v2=True)''',
    '''：判別值 → docker load → 讀 .digest → inspect image ID → 引擎 resolve → create／cp → apply（flock → 重驗 → 寫入）", v2=True)''')

# ================= P9 prune：移除 q12 → q13 直達線；apply 段加 建 .tmp.prune.<id>.toml／刪日誌 =================
rep('''b.box("q12c", E, 17, SUB, "刪失效的啟動器暫存 .tmp.dist.*／（trap 沒清到的）", 340)
b.box("q12cf", P, 17, F12, ".vendor_kit/.tmp.dist.<id>/（刪）", 330)
b.box("q12d", E, 18, SUB, "刪已完成交易殘留的 .tmp.<verb>.<id>.toml（活躍的不刪，只列出）", 340)
b.box("q12df", P, 18, F12, ".vendor_kit/.tmp.<verb>.<id>.toml（殘留：刪；活躍：保留）", 330)
b.box("q13x", U, 19, R12, "是 → 1：摘要全列，失敗的標出", 200)
b.box("q13", L, 19, D12, "有刪除失敗？", 200)
b.box("q14", U, 20, G12, "否 → 0：印刪了什麼、保留什麼（含原因）", 200)''',
    '''b.box("q12j", E, 17, SUB, "建進度日誌 .tmp.prune.<id>.toml（第一個寫入前；state=in-progress、done／pending）", 340)
b.box("q12jf", P, 17, F12, "＋.vendor_kit/.tmp.prune.<id>.toml（prune 自己的交易日誌）", 330)
b.box("q12c", E, 18, SUB, "刪失效的啟動器暫存 .tmp.dist.*／（trap 沒清到的）→ 日誌 done", 340)
b.box("q12cf", P, 18, F12, ".vendor_kit/.tmp.dist.<id>/（刪）", 330)
b.box("q12d", E, 19, SUB, "刪已完成交易殘留的 .tmp.<verb>.<id>.toml（活躍的不刪，只列出）→ 日誌 done", 340)
b.box("q12df", P, 19, F12, ".vendor_kit/.tmp.<verb>.<id>.toml（殘留：刪；活躍：保留）", 330)
b.box("q12k", E, 20, SUB, "刪進度日誌 .tmp.prune.<id>.toml（最後一步）= 交易完成", 340)
b.box("q12kf", P, 20, F12, "－.vendor_kit/.tmp.prune.<id>.toml（刪）", 330)
b.box("q13x", U, 21, R12, "是 → 1：摘要全列，失敗的標出", 200)
b.box("q13", L, 21, D12, "有刪除失敗？", 200)
b.box("q14", U, 22, G12, "否 → 0：印刪了什麼、保留什麼（含原因）", 200)''')
rep('''b.H("qe18", "q12", "q12a"); b.D("qe18a", "q12a", "q12b"); b.D("qe18b", "q12b", "q12c"); b.H("qe19", "q12c", "q12cf", "刪")
b.D("qe18c", "q12c", "q12d"); b.H("qe19d", "q12d", "q12df", "刪"); b.D("qe20", "q12", "q13", al=True)''',
    '''b.H("qe18", "q12", "q12a"); b.D("qe18a", "q12a", "q12b"); b.D("qe18j", "q12b", "q12j"); b.H("qe19j", "q12j", "q12jf", "建"); b.D("qe18b", "q12j", "q12c"); b.H("qe19", "q12c", "q12cf", "刪")
b.D("qe18c", "q12c", "q12d"); b.H("qe19d", "q12d", "q12df", "刪"); b.D("qe18k", "q12d", "q12k"); b.H("qe19k", "q12k", "q12kf", "刪")
_A = geo(b); _qx, _qy, _qw, _qh = _A["q13"]
b.LD("qe20", "q12k", "q13", "", busx=_qx + _qw / 2)   # apply 走完（刪日誌後）才判定失敗；不再有 q12 → q13 直達線（v2.9-6）''')
rep('''→ 引擎 apply（flock → 重驗指紋 → 清 .tmp.dist.* → 清殘留 .tmp.*）→ 摘要", v2=True)''',
    '''→ 引擎 apply（flock → 重驗指紋 → 建 .tmp.prune.<id>.toml → 清 .tmp.dist.* → 清殘留 .tmp.* → 刪日誌）→ 摘要", v2=True)''')
rep(''' (".tmp.* 日誌／.tmp.dist.<id>/", "前者 = remove／uninstall／undev／prune 的進度日誌，未恢復（活躍）的 prune 不刪、只列出並印 6-33、不視為未完成交易（v2.7-7）；後者 = 啟動器暫存（展開的 dist、vk-resolve），trap 刪，殘留由 apply prune 清"),''',
    ''' (".tmp.* 日誌／.tmp.dist.<id>/", "前者 = 修復型 install／remove／uninstall／undev／prune 的進度日誌，未恢復（活躍）的 prune 不刪、只列出並印 6-33、不視為未完成交易（v2.7-7）；prune 自己的交易也建 .tmp.prune.<id>.toml（清理前建、清理後刪；v2.9-6）；後者 = 啟動器暫存（展開的 dist、vk-resolve），trap 刪，殘留由 apply prune 清"),''')
rep('''活躍的 .tmp.* 只列出不刪、不視為未完成交易；需問但無 tty 且無 -y → 1 + 6-4；選項只有 -y 與 --dry-run（無 -n）。"''',
    '''活躍的 .tmp.* 只列出不刪、不視為未完成交易；prune 自己的 apply 也走進度日誌（建 .tmp.prune.<id>.toml → 清理 → 刪日誌；v2.9-6）；需問但無 tty 且無 -y → 1 + 6-4；選項只有 -y 與 --dry-run（無 -n）。"''')

# ================= P10 update：加「還有下一個目標？」迴圈回分流菱形 =================
rep('''b.box("u9", E, 10, SUB, "彙總（Q27）：全部目標查完；每個目標一行（查到的「現版 → 最新」、失敗的 6-3）；訊息全列", 400)
b.box("u10", E, 11, SUB, "末行固定印 6-15：「套用：just vendor_kit upgrade」", 400)
b.box("u11x", U, 12, O12, "是 → 1：查詢失敗（6-3：設 token 或指定 <repo>@<tag>；即使另有新版）", 220)
b.box("u11", E, 12, D12, "任一目標查詢失敗（1）？", 300, ax="l")
b.box("u12y", U, 13, O12, "是 → 2：有新版（給 CI 用）", 220)
b.box("u12", E, 13, D12, "有新版且 --exit-code？", 300, ax="l")
b.box("u13", U, 14, G12, "否 → 0：已列出（有新版也 0）", 220)''',
    '''b.box("u8q", E, 10, D12, "還有下一個目標？", 300, ax=50)
b.box("u9", E, 11, SUB, "否：彙總（Q27）：全部目標查完；每個目標一行（查到的「現版 → 最新」、失敗的 6-3）；訊息全列", 400)
b.box("u10", E, 12, SUB, "末行固定印 6-15：「套用：just vendor_kit upgrade」", 400)
b.box("u11x", U, 13, O12, "是 → 1：查詢失敗（6-3：設 token 或指定 <repo>@<tag>；即使另有新版）", 220)
b.box("u11", E, 13, D12, "任一目標查詢失敗（1）？", 300, ax="l")
b.box("u12y", U, 14, O12, "是 → 2：有新版（給 CI 用）", 220)
b.box("u12", E, 14, D12, "有新版且 --exit-code？", 300, ax="l")
b.box("u13", U, 15, G12, "否 → 0：已列出（有新版也 0）", 220)''')
rep('''b.DL("ue11", "u5g", "u8a"); b.DL("ue12", "u6g", "u8a"); b.D("ue13", "u7", "u9", "記失敗", al=True)
b.D("ue13b", "u8a", "u8b"); b.D("ue14", "u8b", "u9", al=True); b.D("ue15", "u9", "u10"); b.D("ue16", "u10", "u11", al=True)''',
    '''b.DL("ue11", "u5g", "u8a"); b.DL("ue12", "u6g", "u8a"); b.D("ue13", "u7", "u8q", "記失敗", al=True)
b.D("ue13b", "u8a", "u8b"); b.D("ue14", "u8b", "u8q", al=True)
b.LL("ue14y", "u8q", "u5", "是：下一個目標", busx=570); b.D("ue14n", "u8q", "u9", "否", al=True)
b.D("ue15", "u9", "u10"); b.D("ue16", "u10", "u11", al=True)''')
rep('''b.box("u4l", E, 3, LBL, "否 ↓ 對每個目標（[tools] 每工具 + vendor_kit 自身）查 registry", 400, 24, ax="l", minh=24)''',
    '''b.box("u4l", E, 3, LBL, "否 ↓ 對每個目標（[tools] 每工具 + vendor_kit 自身）逐一查 registry（迴圈）", 400, 24, ax="l", minh=24)''')

# ================= P12 交易狀態機：t5 拆「寫暫存檔」「原子替換」「更新日誌 done」三格 =================
rep('''b.box("t5", EA, 4, SUB, "逐步寫入：每步「暫存 → 原子替換 → 日誌 done += 步驟」（詢問取得的同意也記進 consents）", 480)
b.box("t5f", PA, 4, F12, "日誌 done[]／pending[] 每步更新（合併也在暫存完成）", 380)
b.box("t5n", XA, 4, NOTE, "順序固定：清除衝突狀態 → append／初始檔 → baseline → metadata → cache → gen/tools.just（最後寫、與 cache 同一 apply 內原子替換）→ version.toml 最後", 390)
b.box("t6x", U, 5, R12, "是 → 1：明列已完成／未完成；日誌留著（state 仍 in-progress）；第一次 install：整包丟棄、無日誌", 240)
b.box("t6", EA, 5, D12, "中斷？（寫入失敗／Ctrl-C／斷電）", 300, ax="l")
b.box("t7", EA, 6, SUB, "否：最後一步刪日誌（uninstall：在根 justfile 那行之後才刪）", 480)
b.box("t7f", PA, 6, F12, "日誌刪除 = 交易完成（.tmp.<verb>.<id>.toml 刪／[progress] 移除）", 380)
b.box("t8", U, 7, G12, "0（或 2 有衝突）：印摘要", 240)''',
    '''b.box("t5", EA, 4, SUB, "逐步寫入 ①：寫暫存檔（合併也在暫存完成；詢問取得的同意先記進 consents）", 480)
b.box("t5af", PA, 4, F12, "暫存檔（目標檔旁；未換上前目標檔不動）", 380)
b.box("t5n", XA, 4, NOTE, "每一步都是 ①②③ 三個可獨立失敗的動作；步驟順序固定：清除衝突狀態 → append／初始檔 → baseline → metadata → cache → gen/tools.just（最後寫、與 cache 同一 apply 內原子替換）→ version.toml 最後", 390)
b.box("t5b", EA, 5, SUB, "逐步寫入 ②：原子替換（rename 暫存檔 → 目標檔；一檔一次換上）", 480)
b.box("t5bf", PA, 5, F12, "目標檔（換上；中斷只會留下「已換上」「未換上」兩種）", 380)
b.box("t5c", EA, 6, SUB, "逐步寫入 ③：更新日誌 done += 步驟（pending 移出）；還有步驟 → 回 ①", 480)
b.box("t5f", PA, 6, F12, "日誌 done[]／pending[] 每步更新", 380)
b.box("t6x", U, 7, R12, "是 → 1：明列已完成／未完成；日誌留著（state 仍 in-progress）；第一次 install：整包丟棄、無日誌", 240)
b.box("t6", EA, 7, D12, "中斷？（寫入失敗／Ctrl-C／斷電）", 300, ax="l")
b.box("t7", EA, 8, SUB, "否：最後一步刪日誌（uninstall：在根 justfile 那行之後才刪）", 480)
b.box("t7f", PA, 8, F12, "日誌刪除 = 交易完成（.tmp.<verb>.<id>.toml 刪／[progress] 移除）", 380)
b.box("t8", U, 9, G12, "0（或 2 有衝突）：印摘要", 240)''')
rep('''b.D("te4", "t3", "t4", "否", al=True); b.H("te5", "t4", "t4f", "建"); b.D("te6", "t4", "t5"); b.H("te7", "t5", "t5f", "寫")
b.D("te8", "t5", "t6", al=True);''',
    '''b.D("te4", "t3", "t4", "否", al=True); b.H("te5", "t4", "t4f", "建"); b.D("te6", "t4", "t5"); b.H("te7a", "t5", "t5af", "寫")
b.D("te6b", "t5", "t5b"); b.H("te7b", "t5b", "t5bf", "換上"); b.D("te6c", "t5b", "t5c"); b.H("te7", "t5c", "t5f", "寫")
b.D("te8", "t5c", "t6", al=True);''')
rep('''p12, F = newpage_c("狀態機 v2：交易與進度日誌（interface_spec §0、§3.2 apply、§4.3 [progress]、§4.6）", N12, COLS_TX)''',
    '''p12, F = newpage_c("狀態機 v2：交易與進度日誌（interface_spec §0、§3.2 apply、§4.3 [progress]、§4.6）", N12, COLS_TX, gap=16)''')
rep('''：拿鎖 → 重驗指紋 → dry-run 分支 → 建日誌 → 逐步寫入（每步記 done）→ 刪日誌；中斷 → 1、日誌留著", v2=True)''',
    '''：拿鎖 → 重驗指紋 → dry-run 分支 → 建日誌 → 逐步寫入（每步 ① 寫暫存 ② 原子替換 ③ 日誌 done）→ 刪日誌；中斷 → 1、日誌留著", v2=True)''')
rep(''' ("prune 特例（v2.7-7）", "prune 遇活躍（未恢復）日誌：只列出並印 6-33、不刪、不視為未完成交易（不擋 prune、不恢復）；prune 自己的日誌 .tmp.prune.<id>.toml 與其他可寫動詞一樣走恢復"),''',
    ''' ("prune 特例（v2.7-7）", "prune 遇活躍（未恢復）日誌：只列出並印 6-33、不刪、不視為未完成交易（不擋 prune、不恢復）；prune 自己的 apply 也建 .tmp.prune.<id>.toml（清理前建、清理後刪；v2.9-6），與其他可寫動詞一樣走恢復"),''')

# ================= P14 結束碼表：help 列 3 欄補 P < floor → 3 + 6-18；其他動詞 3 欄同規則 =================
rep(''' ["help／h", "永遠 0（不觸網、不安裝）", "—", "—", "—", "—"],''',
    ''' ["help／h", "印說明（不觸網、不安裝）", "—", "—", "—", "P < floor → 3 + 6-18（零寫入；任何動詞含 help、救援路徑皆同）"],''')
rep(''' ["dev <repo>／vendor_kit", "覆寫寫入 version.local.toml", "工具不在 version.toml；缺 <dir>/dist/init.toml；CI 拒絕；-p／-i 互斥用錯", "—", "—", "-i 舊引擎 P／schema 低於薄殼首行且要重產 tracked 薄殼 → 拒絕"],''',
    ''' ["dev <repo>／vendor_kit", "覆寫寫入 version.local.toml", "工具不在 version.toml；缺 <dir>/dist/init.toml；CI 拒絕；-p／-i 互斥用錯", "—", "—", "6-18／6-19；-i 舊引擎 P／schema 低於薄殼首行且要重產 tracked 薄殼 → 拒絕"],''')
rep(''' ["prune", "完成（印刪了什麼、保留什麼；活躍 .tmp.* 只列出）；dry-run 零刪除", "vk-resolve 不合（6-30）；無 tty 需問（6-4）", "任一 docker rm／image rm／network rm／volume rm 失敗（摘要全列）", "—", "6-18"],''',
    ''' ["prune", "完成（印刪了什麼、保留什麼；活躍 .tmp.* 只列出）；dry-run 零刪除", "vk-resolve 不合（6-30）；無 tty 需問（6-4）", "任一 docker rm／image rm／network rm／volume rm 失敗（摘要全列）", "—", "6-18／6-19"],''')
rep(''' ["ci/check.sh", "⓪～⑤ 全過", "⓪ version.local.toml 被 track；① sync 的 1；② verify 印記不符；③ upgrade --dry-run 需改 tracked 檔（印清單）", "④⑤ 工具／專案測試原碼傳出", "③ 仍有衝突標記", "① 的 3"],''',
    ''' ["ci/check.sh", "⓪～⑤ 全過", "⓪ version.local.toml 被 track；① sync 的 1；② verify 印記不符；③ upgrade --dry-run 需改 tracked 檔（印清單）", "④⑤ 工具／專案測試原碼傳出", "③ 仍有衝突標記", "① 的 3（P < floor 6-18／6-19）"],''')
rep(''' ("結束碼 3（Q23）", "現有薄殼／檔案／引擎的組合需先升級或退回：(a) P < floor 6-18 (b) schema 高於支援 6-19 (c) 降版無法無損讀 6-10 (d) dev -i 舊引擎要重產薄殼 (e) 舊薄殼跑新 major 一般動詞 6-36；零寫入、無任何例外；以 P／schema 比"),''',
    ''' ("結束碼 3（Q23）", "現有薄殼／檔案／引擎的組合需先升級或退回：(a) P < floor 6-18 (b) schema 高於支援 6-19 (c) 降版無法無損讀 6-10 (d) dev -i 舊引擎要重產薄殼 (e) 舊薄殼跑新 major 一般動詞 6-36；任何動詞（含 help、救援路徑）在 P < floor 都回 3 + 6-18（v2.9-7）；零寫入、無任何例外；以 P／schema 比"),''')
rep('''版本／協定／schema 不合，須先升級或退回才能繼續；回 3 時零寫入、無任何例外（救援路徑亦同）；''',
    '''版本／協定／schema 不合，須先升級或退回才能繼續；P < floor → 任何動詞（含 help、救援路徑）都回 3 + 6-18；回 3 時零寫入、無任何例外；''')
rep('''3 = 版本／協定／schema 不合且零寫入（無任何例外）；既定回 1 的情境維持 1；''',
    '''3 = 版本／協定／schema 不合且零寫入（無任何例外；P < floor 時任何動詞含 help 都回 3 + 6-18，v2.9-7）；既定回 1 的情境維持 1；''')

# ---- 檔頭說明 ----
rep('''proposal_v2.md v2.4～v2.7（v2.7 最高優先）、review_v2r5_findings.md 八頁段落（第六輪必修＋選修）''',
    '''proposal_v2.md v2.4～v2.9（v2.9 最高優先）、review_v2r7_findings.md 本檔十頁段落（第八輪必修＋選修；備份 .v9）''')
open(p, "w", encoding="utf-8").write(s); print("ok")
