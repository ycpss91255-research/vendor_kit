"""第十一輪 patch 5：dev、dev vendor_kit、undev、undev vendor_kit、remove(1)(2)、uninstall(1)(2)。"""
src = open("disc_v1_b.py", encoding="utf-8").read()
def rep(old, new, n=1):
    global src
    c = src.count(old); assert c == n, (c, old[:90])
    src = src.replace(old, new)

# ---- T8 ----
rep(''' ("resolve／apply", "undev 分兩段：resolve 只讀只算（列要拉的鎖定版 image、輸出指紋，不寫檔）→ 啟動器拉 image → apply 拿 flock、重驗指紋、建日誌後才刪覆寫、拆 symlink、重新 materialize；dev 不拉 image"),
 ("version.local.toml", ".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 <repo> = \\"path:<dir>\\" 或 vendor_kit = \\"<tag>\\" + image ID（成對，undev 一起撤）"),''',
''' RA_T, VL_T,''')

# ---- P8 dev：de1x 否線改同列 H；頁尾 launcher_exit ----
rep('''b.box("d1q", L, 1, v2(D12), "<dir>/dist/ 內有 init.toml？", 240, ax="r")
b.box("d1x", U, 2, v2(O12), "否 → 1：<dir>/dist/init.toml 不存在", 220)''',
'''b.box("d1x", U, 1, v2(O12), "否 → 1：<dir>/dist/init.toml 不存在", 220)
b.box("d1q", L, 1, v2(D12), "<dir>/dist/ 內有 init.toml？", 240, ax="r")''')
rep('''b.box("d8", U, 10, v2(G12), "0：之後每次 just 用 <dir>", 220)''',
'''b.box("d8", U, 10, v2(G12), "0：之後每次 just 用 <dir>", 220)
b.box("d8l", L, 10, v2(W12), LXT, 280)''')
rep('''b.H("de1", "d0", "d0l"); b.D("de1l", "d0l", "d1q", al=True); b.DL("de1x", "d1q", "d1x", "否", 0.15); b.D("de1y", "d1q", "d1m", "是", 0.65, 0.5, al=True); b.D("de1m", "d1m", "d1", al=True)   # launcher_start（v2.12）''',
'''b.H("de1", "d0", "d0l"); b.D("de1l", "d0l", "d1q", al=True); b.H("de1x", "d1q", "d1x", "否"); b.D("de1y", "d1q", "d1m", "是", 0.65, 0.5, al=True); b.D("de1m", "d1m", "d1", al=True)   # launcher_start（v2.12）；否線同列橫出，不壓 d1m 框緣（r10）''')
rep('''b.D("de12", "d7", "d7b"); b.H("de13", "d7b", "d7bf", "寫"); b.DL("de14", "d7b", "d8", "", 0.1)''',
'''b.D("de12", "d7", "d7b"); b.H("de13", "d7b", "d7bf", "寫"); b.D("de14", "d7b", "d8l", "", 0.1, 0.5); b.H("de14l", "d8l", "d8")   # 頁尾 launcher_exit（v2.14-2）''')

# ---- P8ccc dev vendor_kit：engine_start 格；頁尾 launcher_exit ----
rep('''b.box("v1", L, 1, v2(W12), fl("docker run 引擎 dev vendor_kit -i <tag>，image ID 一併交給引擎（引擎容器內不呼叫 docker）"), 280)''',
'''b.box("v1", L, 1, v2(W12), fl("docker run 引擎 dev vendor_kit -i <tag>，image ID 一併交給引擎（引擎容器內不呼叫 docker）"), 280)
b.box("v1e", E, 1, v2(SUB), EST, 400)   # 單段容器（v2.14-2）''')
rep('''b.box("v2z", U, 5, v2(G12), "0：之後每次 just 用該本機 image", 220)''',
'''b.box("v2zl", L, 5, v2(W12), LXT, 280)
b.box("v2z", U, 5, v2(G12), "0：之後每次 just 用該本機 image", 220)''')
rep('''b.H("ve1", "v0", "v1i"); b.D("ve1i", "v1i", "v1"); b.D("ve2", "v1", "v2q"); b.H("ve3", "v2q", "v2x", "是");''',
'''b.H("ve1", "v0", "v1i"); b.D("ve1i", "v1i", "v1"); b.H("ve2", "v1", "v1e"); b.D("ve2e", "v1e", "v2q", al=True); b.H("ve3", "v2q", "v2x", "是");''')
rep('''b.D("ve5c", "v2b", "v2c"); b.H("ve5cf", "v2c", "v3c", "寫"); b.H("ve6", "v2c", "v2z")''',
'''b.D("ve5c", "v2b", "v2c"); b.H("ve5cf", "v2c", "v3c", "寫"); b.H("ve6", "v2c", "v2zl"); b.H("ve6l", "v2zl", "v2z")   # 頁尾 launcher_exit（v2.14-2）''')

# ---- P8c undev：resolve／apply 容器 engine_start；u5p 紅出口；u6c 拆三格；頁尾 launcher_exit ----
rep('''b.box("u1", L, 0, v2(W12), "（已寫 launcher_start）docker run 引擎 resolve undev <repo>（引擎先 append engine_start）", 280)
b.box("u3", U, 1, G12, "否 → 0：未啟用 dev（提示）", 220)''',
'''b.box("u1", L, 0, v2(W12), "docker run 引擎 resolve undev <repo>（已寫 launcher_start）", 280)
b.box("u1e", E, 0, v2(SUB), EST, 400)   # resolve 容器（v2.14-2）
b.box("u3", U, 1, G12, "否 → 0：未啟用 dev（提示）", 220)''')
rep('''b.box("u5b", L, 4, v2(W12), "docker create <img> /x", 280)
b.box("u5c", L, 5, v2(W12), "docker cp c:/dist/. <tmp>/<repo>/（主機暫存）", 280)
b.box("u5d", L, 6, v2(W12), "docker rm 該容器", 280)
b.box("u5r", L, 7, v2(W12), fl("docker run … -v <tmp>:/dist:ro 引擎 apply undev <repo>"), 280)
b.box("u6a", E, 7, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("u6b", E, 8, v2(SUB), "重驗指紋", 240, ax="l")
b.box("u6bx", E, 8, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("u6l", E, 9, v2(SUB), "建進度日誌（.vendor_kit/.tmp.undev.<id>.toml；第一個寫入前）", 400)
b.box("u6lf", P, 9, F12, "＋.vendor_kit/.tmp.undev.<id>.toml（進度日誌，不進 git）", 360)
b.box("u6c", E, 10, v2(SUB), fl("刪 version.local.toml 該行（<repo> = \\"path:<dir>\\"；最後一個覆寫 → 刪整個檔）"), 400)
b.box("u6cf", P, 10, F12, "version.local.toml（少一行；空了就刪檔）", 360)
b.box("u6d", E, 11, v2(SUB), "拆掉 cache/<repo>/ 的 symlink", 400)
b.box("u6df", P, 11, F12, "cache/<repo>/（不再是 symlink）", 360)
b.box("u6e", E, 12, v2(SUB), fl("materialize 鎖定版：/dist/<repo> 展開到暫存目錄"), 400)
b.box("u6e2", E, 13, v2(SUB), fl("暫存 → cache/<repo>/（原子替換）"), 400)
b.box("u6ef", P, 13, F12, "cache/<repo>/（重新展開）", 360)
b.box("u6f", E, 14, v2(SUB), fl("寫 gen/<repo>.stamp（第一行 index digest，之後每檔 sha256）"), 400)
b.box("u6ff", P, 14, F12, "gen/<repo>.stamp（第一行 index digest）", 360)
b.box("u6x", U, 15, v2(R12), "失敗（任一步）→ 1：保留可恢復狀態（下次任何動詞先恢復）", 220)
b.box("u6g", E, 15, v2(SUB), "刪進度日誌（最後一步）", 400)
b.box("u7", U, 16, G12, "成功 → 0", 220)
b.H("ue1", "u0", "u1"); b.D("ue2", "u1", "u2"); b.H("ue3", "u2", "u3", "否"); b.H("ue4", "u2", "u4", "是")
b.D("ue5", "u4", "u5a", "", 0.5, 0.5); b.RD("ue5n", "u5a", "u5p", "無"); b.H("ue6", "u5g", "u5p", "拉 /dist"); b.D("ue5y", "u5a", "u5b", "有", al=True); b.D("ue5p", "u5p", "u5b", al=True)
b.D("ue5c", "u5b", "u5c"); b.D("ue5d", "u5c", "u5d"); b.D("ue7", "u5d", "u5r")
b.H("ue8", "u5r", "u6a"); b.D("ue8b", "u6a", "u6b", al=True); b.H("ue8x", "u6b", "u6bx"); b.D("ue9", "u6b", "u6l", al=True); b.H("ue9f", "u6l", "u6lf", "寫")
b.D("ue10", "u6l", "u6c"); b.H("ue10f", "u6c", "u6cf", "寫"); b.D("ue11", "u6c", "u6d"); b.H("ue11f", "u6d", "u6df", "寫")
b.D("ue12", "u6d", "u6e"); b.D("ue12b", "u6e", "u6e2"); b.H("ue12f", "u6e2", "u6ef", "寫"); b.D("ue13", "u6e2", "u6f"); b.H("ue13f", "u6f", "u6ff", "寫")
b.D("ue14", "u6f", "u6g", "成功", 0.6, 0.5, al=True); b.D("ue14x", "u6f", "u6x", "失敗", 0.2, 0.5); b.DL("ue15", "u6g", "u7")''',
'''b.box("u5px", E, 4, v2(R12), fl("失敗／逾時 → 1：印 6-24／6-31"), 240, ax="l")   # v2.14-5
b.box("u5b", L, 4, v2(W12), "docker create <img> /x", 280)
b.box("u5c", L, 5, v2(W12), "docker cp c:/dist/. <tmp>/<repo>/（主機暫存）", 280)
b.box("u5d", L, 6, v2(W12), "docker rm 該容器", 280)
b.box("u5r", L, 7, v2(W12), fl("docker run … -v <tmp>:/dist:ro 引擎 apply undev <repo>"), 280)
b.box("u5re", E, 7, v2(SUB), EST, 400)   # apply 容器（v2.14-2）
b.box("u6a", E, 8, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("u6b", E, 9, v2(SUB), "重驗指紋", 240, ax="l")
b.box("u6bx", E, 9, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("u6l", E, 10, v2(SUB), "建進度日誌（.vendor_kit/.tmp.undev.<id>.toml；第一個寫入前）", 400)
b.box("u6lf", P, 10, F12, "＋.vendor_kit/.tmp.undev.<id>.toml（進度日誌，不進 git）", 360)
b.box("u6c", E, 11, v2(SUB), fl("刪 version.local.toml 該行（<repo> = \\"path:<dir>\\"）"), 400)   # r10：拆三格（同 undev vendor_kit）
b.box("u6cf", P, 11, F12, "version.local.toml（少一行）", 360)
b.box("u6ce", E, 12, v2(D12), "還有其他覆寫行？", 200, ax="l")
b.box("u6ced", E, 12, v2(SUB), fl("否：刪整個 version.local.toml（最後一個覆寫已撤）"), 170, ax="r")
b.box("u6cedf", P, 12, v2(F12), "－version.local.toml（整個檔）", 360)
b.box("u6d", E, 13, v2(SUB), "是／已刪：拆掉 cache/<repo>/ 的 symlink", 400)
b.box("u6df", P, 13, F12, "cache/<repo>/（不再是 symlink）", 360)
b.box("u6e", E, 14, v2(SUB), fl("materialize 鎖定版：/dist/<repo> 展開到暫存目錄"), 400)
b.box("u6e2", E, 15, v2(SUB), fl("暫存 → cache/<repo>/（原子替換）"), 400)
b.box("u6ef", P, 15, F12, "cache/<repo>/（重新展開）", 360)
b.box("u6f", E, 16, v2(SUB), fl("寫 gen/<repo>.stamp（第一行 index digest，之後每檔 sha256）"), 400)
b.box("u6ff", P, 16, F12, "gen/<repo>.stamp（第一行 index digest）", 360)
b.box("u6x", U, 17, v2(R12), "失敗（任一步）→ 1：保留可恢復狀態（下次任何動詞先恢復）", 220)
b.box("u6g", E, 17, v2(SUB), "刪進度日誌（最後一步）", 400)
b.box("u7l", L, 18, v2(W12), LXT, 280)
b.box("u7", U, 18, G12, "成功 → 0", 220)
b.H("ue1", "u0", "u1"); b.H("ue1e", "u1", "u1e"); b.D("ue2", "u1e", "u2", al=True); b.H("ue3", "u2", "u3", "否"); b.H("ue4", "u2", "u4", "是")
b.D("ue5", "u4", "u5a", "", 0.5, 0.5); b.RD("ue5n", "u5a", "u5p", "無"); b.H("ue6", "u5g", "u5p", "拉 /dist"); b.D("ue5y", "u5a", "u5b", "有", al=True); b.D("ue5p", "u5p", "u5b", "", 0.25, 0.5); b.D("ue5px", "u5p", "u5px", "失敗", 0.75, 0.25, dy=8)
b.D("ue5c", "u5b", "u5c"); b.D("ue5d", "u5c", "u5d"); b.D("ue7", "u5d", "u5r")
b.H("ue8", "u5r", "u5re"); b.D("ue8e", "u5re", "u6a"); b.D("ue8b", "u6a", "u6b", al=True); b.H("ue8x", "u6b", "u6bx"); b.D("ue9", "u6b", "u6l", al=True); b.H("ue9f", "u6l", "u6lf", "寫")
b.D("ue10", "u6l", "u6c"); b.H("ue10f", "u6c", "u6cf", "寫"); b.D("ue10e", "u6c", "u6ce", al=True); b.H("ue10ed", "u6ce", "u6ced", "否"); b.H("ue10edf", "u6ced", "u6cedf", "刪")
b.D("ue11", "u6ce", "u6d", "是", al=True); b.D("ue11d", "u6ced", "u6d", al=True); b.H("ue11f", "u6d", "u6df", "寫")
b.D("ue12", "u6d", "u6e"); b.D("ue12b", "u6e", "u6e2"); b.H("ue12f", "u6e2", "u6ef", "寫"); b.D("ue13", "u6e2", "u6f"); b.H("ue13f", "u6f", "u6ff", "寫")
b.D("ue14", "u6f", "u6g", "成功", 0.6, 0.5, al=True); b.D("ue14x", "u6f", "u6x", "失敗", 0.2, 0.5); b.D("ue15", "u6g", "u7l"); b.H("ue15l", "u7l", "u7")   # 頁尾 launcher_exit（v2.14-2）''')

# ---- P8cc undev vendor_kit ----
rep('''b.box("w1", L, 0, v2(W12), "（已寫 launcher_start）docker run 引擎 resolve undev vendor_kit（引擎先 append engine_start）", 280)
b.box("w3", U, 1, G12, "否 → 0：未啟用（提示）", 220)
b.box("w2q", E, 1, v2(D12), "version.local.toml 有 vendor_kit 行？", 300, ax="l")
b.box("w2s", E, 2, v2(SUB), fl("是：resolve（不寫）：無 image 要拉；輸出輸入指紋（version.local.toml hash）"), 400)
b.box("w1b", L, 3, v2(W12), "docker run 引擎 apply undev vendor_kit", 280)
b.box("w2a", E, 3, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("w2b", E, 4, v2(SUB), "重驗指紋", 240, ax="l")
b.box("w2bx", E, 4, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("w2l", E, 5, v2(SUB), "建進度日誌（.vendor_kit/.tmp.undev.<id>.toml；第一個寫入前）", 400)
b.box("w2lf", P, 5, F12, "＋.vendor_kit/.tmp.undev.<id>.toml（進度日誌，不進 git）", 360)
b.box("w2x", U, 6, v2(R12), "失敗 → 1：保留可恢復狀態（下次可寫動詞先恢復）", 220)
b.box("w2", E, 6, v2(SUB), fl("刪 version.local.toml 的 vendor_kit 行（tag＋vendor_kit_image_id 一起撤）"), 400)
b.box("w2f", P, 6, F12, "version.local.toml（少 vendor_kit 行與 vendor_kit_image_id 行）", 360)
b.box("w2e", E, 7, v2(D12), "還有其他覆寫行？", 200, ax="l")
b.box("w2ed", E, 7, v2(W12), fl("否：刪整個 version.local.toml（最後一個覆寫已撤）"), 170, ax="r")
b.box("w2edf", P, 7, v2(F12), "－version.local.toml（整個檔）", 360)
b.box("w2g", E, 8, v2(SUB), "是／已刪：刪進度日誌（最後一步）", 400)
b.box("w2z", U, 9, v2(G12), "0：本次結束（下次 just 用 version.toml 的引擎）", 220)
b.box("wb", L, 10, LBL, "═══ 下次 just（改用 version.toml 的引擎；啟動器先比對 gen/.stamp 再起容器）═══", 560, 24, ax="l", minh=24)
b.box("w4", U, 11, G12, "下次打任何 just", 220)
b.box("w5a", L, 11, v2(W12), "（已寫 launcher_start）grep version.toml 第一行取引擎 ref（local 已無覆寫）", 280)
b.box("w7", U, 12, v2(O12), fl("否 → 1：「vendor_kit 已更新，請執行：just vendor_kit upgrade vendor_kit」（不重寫）"), 220)
b.box("w6", L, 12, v2(D12), "gen/.stamp 的引擎 ref == 第一行？", 270, ax="l")
b.box("w5b", L, 13, v2(D12), "是 → docker image inspect：本機有？", 170, ax="l")
b.box("w5p", L, 14, W12, "無：docker pull 該引擎", 100, ax="r")
b.box("w5g", G, 14, IMG, "vendor_kit:vN（version.toml 的引擎）", 220)
b.box("w5c", L, 15, W12, "docker run 該引擎 resolve sync", 280)
b.box("w9", E, 15, G12, "0：正常跑（「sync（1）」頁）", 200, ax="l")
b.H("we1", "w0", "w1"); b.D("we2", "w1", "w2q"); b.H("we2n", "w2q", "w3", "否"); b.D("we2y", "w2q", "w2s", "是", al=True)
b.D("we2s", "w2s", "w1b", "", 0.2, 0.5); b.H("we2a", "w1b", "w2a"); b.D("we2b", "w2a", "w2b", al=True);''',
'''b.box("w1", L, 0, v2(W12), "docker run 引擎 resolve undev vendor_kit（已寫 launcher_start）", 280)
b.box("w1e", E, 0, v2(SUB), EST, 400)   # resolve 容器（v2.14-2）
b.box("w3", U, 1, G12, "否 → 0：未啟用（提示）", 220)
b.box("w2q", E, 1, v2(D12), "version.local.toml 有 vendor_kit 行？", 300, ax="l")
b.box("w2s", E, 2, v2(SUB), fl("是：resolve（不寫）：無 image 要拉；輸出輸入指紋（version.local.toml hash）"), 400)
b.box("w1b", L, 3, v2(W12), "docker run 引擎 apply undev vendor_kit", 280)
b.box("w1be", E, 3, v2(SUB), EST, 400)   # apply 容器（v2.14-2）
b.box("w2a", E, 4, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("w2b", E, 5, v2(SUB), "重驗指紋", 240, ax="l")
b.box("w2bx", E, 5, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("w2l", E, 6, v2(SUB), "建進度日誌（.vendor_kit/.tmp.undev.<id>.toml；第一個寫入前）", 400)
b.box("w2lf", P, 6, F12, "＋.vendor_kit/.tmp.undev.<id>.toml（進度日誌，不進 git）", 360)
b.box("w2x", U, 7, v2(R12), "失敗 → 1：保留可恢復狀態（下次可寫動詞先恢復）", 220)
b.box("w2", E, 7, v2(SUB), fl("刪 version.local.toml 的 vendor_kit 行（tag＋vendor_kit_image_id 一起撤）"), 400)
b.box("w2f", P, 7, F12, "version.local.toml（少 vendor_kit 行與 vendor_kit_image_id 行）", 360)
b.box("w2e", E, 8, v2(D12), "還有其他覆寫行？", 200, ax="l")
b.box("w2ed", E, 8, v2(SUB), fl("否：刪整個 version.local.toml（最後一個覆寫已撤）"), 170, ax="r")
b.box("w2edf", P, 8, v2(F12), "－version.local.toml（整個檔）", 360)
b.box("w2g", E, 9, v2(SUB), "是／已刪：刪進度日誌（最後一步）", 400)
b.box("w2zl", L, 10, v2(W12), LXT, 280)
b.box("w2z", U, 10, v2(G12), "0：本次結束（下次 just 用 version.toml 的引擎）", 220)
b.box("wb", L, 11, LBL, "═══ 下次 just（改用 version.toml 的引擎；啟動器先比對 gen/.stamp 再起容器）═══", 560, 24, ax="l", minh=24)
b.box("w4", U, 12, G12, "下次打任何 just", 220)
b.box("w5a", L, 12, v2(W12), "（已寫 launcher_start）grep version.toml 第一行取引擎 ref（local 已無覆寫）", 280)
b.box("w7", U, 13, v2(O12), fl("否 → 1：「vendor_kit 已更新，請執行：just vendor_kit upgrade vendor_kit」（不重寫）"), 220)
b.box("w6", L, 13, v2(D12), "gen/.stamp 的引擎 ref == 第一行？", 270, ax="l")
b.box("w5b", L, 14, v2(D12), "是 → docker image inspect：本機有？", 170, ax="l")
b.box("w5p", L, 15, W12, "無：docker pull 該引擎", 100, ax="r")
b.box("w5g", G, 15, IMG, "vendor_kit:vN（version.toml 的引擎）", 220)
b.box("w5c", L, 16, W12, "docker run 該引擎 resolve sync", 280)
b.box("w9", E, 16, G12, "0：正常跑（「sync（1）」頁）", 200, ax="l")
b.H("we1", "w0", "w1"); b.H("we1e", "w1", "w1e"); b.D("we2", "w1e", "w2q", al=True); b.H("we2n", "w2q", "w3", "否"); b.D("we2y", "w2q", "w2s", "是", al=True)
b.D("we2s", "w2s", "w1b", "", 0.2, 0.5); b.H("we2a", "w1b", "w1be"); b.D("we2ae", "w1be", "w2a"); b.D("we2b", "w2a", "w2b", al=True);''')
rep('''b.DL("we4", "w2g", "w2z")''', '''b.D("we4", "w2g", "w2zl"); b.H("we4l", "w2zl", "w2z")   # 頁尾 launcher_exit（v2.14-2）''')

# ---- T8B ----
rep(''' ("uninstall（v2.2 E、v2.5 §10、v2.8 §1）", "全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含專案層 baseline/.gitkeep、baseline/.vendor_kit.toml，再刪空的 baseline/ → 根 justfile 那行問後刪 → 最後刪日誌 → 目錄空了才 rmdir）；不 rm -rf .vendor_kit/"),
 ("resolve／apply／--dry-run", "resolve 只讀只算（讀 metadata、列清單、輸出指紋，不寫檔）；apply 拿 flock、重驗指紋後才刪；--dry-run（無短形）只印會刪什麼、會問什麼，覆蓋所有刪改與詢問（本機 → 0；CI 為真且需改 tracked 檔 → 1）"),
 ("flock／指紋／進度日誌", "flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗（不同 → 1 請重跑，橙）；進度日誌 = 列已完成／未完成，第一個寫入前建、最後一步刪，失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑（remove／uninstall 用 .vendor_kit/.tmp.<verb>.<id>.toml，因 metadata 會被刪）"),
 ("baseline／metadata", "baseline/<repo>/ = 上次合併的範本副本（進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、append 過的行；remove 先讀它（append 行）再刪整個 baseline/<repo>/"),''',
''' ("uninstall（v2.2 E、v2.5 §10、v2.8 §1、v2.13 P6）", "全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含 config.toml（== baseline 副本才刪）、baseline/ 根檔，再 rmdir 空的子目錄 → 根 justfile 那行問後刪 → 最後刪日誌）；log/ 一律保留（uninstall 自己也在寫），所以 .vendor_kit/ 保留、不 rm -rf"),
 RAD_T, FIP_T, BM_T,''')
rep(''' ("初始檔", "init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）"),''', ''' INIT_T,''')

# ---- P8b remove(1)：apply 容器 engine_start ----
rep('''b.box("m8", L, 8, v2(W12), fl("docker run <引擎> apply remove <repo>（--dry-run 原樣轉發）"), 280)
b.box("m9a", E, 8, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("m9b", E, 9, v2(SUB), "重驗指紋", 240, ax="l")
b.box("m9x", E, 9, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("m7cx", U, 10, v2(O12), "是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）", 220)
b.box("m7c", E, 10, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax="l")
b.box("m7y", U, 11, v2(G12), "是 → 0：只印清單（會刪什麼、會問什麼）", 220)
b.box("m7", E, 11, D12, "--dry-run？", 240, ax=50)
b.box("m7z", E, 12, LBL, "否 ↓ 續「remove（2）」頁：建日誌 → 問 append 行 → 刪檔 → 刪日誌", 400, 24, ax="l", minh=24)''',
'''b.box("m8", L, 8, v2(W12), fl("docker run <引擎> apply remove <repo>（--dry-run 原樣轉發）"), 280)
b.box("m8e", E, 8, v2(SUB), EST, 400)   # apply 容器（v2.14-2）
b.box("m9a", E, 9, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("m9b", E, 10, v2(SUB), "重驗指紋", 240, ax="l")
b.box("m9x", E, 10, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("m7cx", U, 11, v2(O12), "是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）", 220)
b.box("m7c", E, 11, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax="l")
b.box("m7y", U, 12, v2(G12), "是 → 0：只印清單（會刪什麼、會問什麼）", 220)
b.box("m7", E, 12, D12, "--dry-run？", 240, ax=50)
b.box("m7z", E, 13, LBL, "否 ↓ 續「remove（2）」頁：建日誌 → 問 append 行 → 刪檔 → 刪日誌", 400, 24, ax="l", minh=24)''')
rep('''b.H("me8", "m8", "m9a"); b.D("me8b", "m9a", "m9b", al=True);''', '''b.H("me8", "m8", "m8e"); b.D("me8e", "m8e", "m9a"); b.D("me8b", "m9a", "m9b", al=True);''')

# ---- P8bccc remove(2)：藍白；頁尾 launcher_exit ----
rep('''b.box("m9s", E, 4, v2(W12), fl("是：找上次插入的行（CRLF／LF 視為相同、其餘精確）"), 200, ax=80)''', '''b.box("m9s", E, 4, v2(SUB), fl("是：找上次插入的行（CRLF／LF 視為相同、其餘精確）"), 200, ax=80)''')
rep('''b.box("m9z", E, 5, W12, "零命中：不刪、印清單", 70, ax="l")
b.box("m9m", E, 5, v2(D12), "命中幾處？", 140, ax=110)
b.box("m9d", E, 5, W12, "唯一：刪那幾行", 100, ax="r")''',
'''b.box("m9z", E, 5, SUB, "零命中：不刪、印清單", 70, ax="l")
b.box("m9m", E, 5, v2(D12), "命中幾處？", 140, ax=110)
b.box("m9d", E, 5, SUB, "唯一：刪那幾行", 100, ax="r")''')
rep('''b.box("m9w", E, 7, v2(W12), "多處：保留＋warn", 140, ax=110)''', '''b.box("m9w", E, 7, v2(SUB), "多處：保留＋warn", 140, ax=110)''')
rep('''b.box("m11", U, 14, G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", 220)''',
'''b.box("m11l", L, 14, v2(W12), LXT, 280)
b.box("m11", U, 14, G12, "0：印「以下初始檔保留，若不需要請 git rm：…」", 220)''')
rep('''b.D("me16", "m10e", "m10g", "成功", 0.6, 0.5, al=True); b.D("me16x", "m10e", "m10x", "失敗", 0.2, 0.5); b.DL("me17", "m10g", "m11")''',
'''b.D("me16", "m10e", "m10g", "成功", 0.6, 0.5, al=True); b.D("me16x", "m10e", "m10x", "失敗", 0.2, 0.5); b.D("me17", "m10g", "m11l"); b.H("me17l", "m11l", "m11")   # 頁尾 launcher_exit（v2.14-2）''')

# ---- P8bc uninstall(1)：主路徑補線；apply 容器 engine_start ----
rep('''b.box("x1b", L, 8, v2(W12), fl("docker run <引擎> apply uninstall（--dry-run 原樣轉發）"), 280)
b.box("x4a", E, 8, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("x4b", E, 9, v2(SUB), "重驗指紋", 240, ax="l")
b.box("x4bx", E, 9, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("x3cx", U, 10, v2(O12), "是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）", 220)
b.box("x3c", E, 10, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax="l")
b.box("x3y", U, 11, v2(G12), "是 → 0：只印會刪什麼、會問什麼", 220)
b.box("x3", E, 11, D12, "--dry-run？", 240, ax=50)
b.box("x4z", E, 12, LBL, "否 ↓ 續「uninstall（2）」頁：建日誌 → 逐工具 remove → 刪自產檔 → 根 justfile 那行 → 刪日誌", 400, 24, ax="l", minh=24)
b.H("xe1", "x0", "x0l"); b.D("xe1l", "x0l", "x1", al=True); b.H("xe1e", "x1", "x1e"); b.D("xe2", "x1e", "x2", al=True); b.H("xe3", "x2", "x2x", "否")   # launcher_start／engine_start（v2.12）; b.D("xe4", "x2", "x2b", "是", al=True); b.D("xe4b", "x2b", "x2bb"); b.D("xe4c", "x2bb", "x2c"); b.D("xe4d", "x2c", "x2d"); b.D("xe4e", "x2d", "x2e")
b.D("xe5", "x2e", "x1b", "", 0.2, 0.5); b.H("xe5b", "x1b", "x4a"); b.D("xe5c", "x4a", "x4b", al=True);''',
'''b.box("x1b", L, 8, v2(W12), fl("docker run <引擎> apply uninstall（--dry-run 原樣轉發）"), 280)
b.box("x1be", E, 8, v2(SUB), EST, 400)   # apply 容器（v2.14-2）
b.box("x4a", E, 9, v2(SUB), "apply：flock 專案目錄（60 秒）", 400)
b.box("x4b", E, 10, v2(SUB), "重驗指紋", 240, ax="l")
b.box("x4bx", E, 10, v2(O12), "不同 → 1「請重跑」", 140, ax="r")
b.box("x3cx", U, 11, v2(O12), "是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）", 220)
b.box("x3c", E, 11, v2(D12), "CI 為真（frozen）且需改 tracked 檔？", 340, ax="l")
b.box("x3y", U, 12, v2(G12), "是 → 0：只印會刪什麼、會問什麼", 220)
b.box("x3", E, 12, D12, "--dry-run？", 240, ax=50)
b.box("x4z", E, 13, LBL, "否 ↓ 續「uninstall（2）」頁：建日誌 → 逐工具 remove → 刪自產檔 → 根 justfile 那行 → 刪日誌", 400, 24, ax="l", minh=24)
b.H("xe1", "x0", "x0l"); b.D("xe1l", "x0l", "x1", al=True); b.H("xe1e", "x1", "x1e"); b.D("xe2", "x1e", "x2", al=True); b.H("xe3", "x2", "x2x", "否")   # launcher_start／engine_start（v2.12）
b.D("xe4", "x2", "x2b", "是", al=True); b.D("xe4b", "x2b", "x2bb"); b.D("xe4c", "x2bb", "x2c"); b.D("xe4d", "x2c", "x2d"); b.D("xe4e", "x2d", "x2e")   # r10：第十版註解吃掉這段主路徑
b.D("xe5", "x2e", "x1b", "", 0.2, 0.5); b.H("xe5b", "x1b", "x1be"); b.D("xe5be", "x1be", "x4a"); b.D("xe5c", "x4a", "x4b", al=True);''')

# ---- P8bcc uninstall(2)：config.toml 依 P6；不 rmdir log/；.vendor_kit/ 保留；藍白；頁尾 launcher_exit ----
rep('''b = F.band("vD2", "uninstall（2）寫入段（承「uninstall（1）」頁）：建日誌 → 逐工具 remove（保護模式）→ 只刪 hash 相符的自產檔（gen/、baseline/ 根檔各一步，v2.8 §1）→ justfile 那行、.dockerignore 四行問後逐行刪 → 刪日誌 → 空才 rmdir", v2=True)''',
'''b = F.band("vD2", "uninstall（2）寫入段（承「uninstall（1）」頁）：建日誌 → 逐工具 remove（保護模式）→ 只刪 hash 相符的自產檔（config.toml == baseline 副本才刪，v2.13 P6；gen/、baseline/ 根檔各一步）→ justfile 那行、.dockerignore 四行問後逐行刪 → 刪日誌 → .vendor_kit/ 保留（只剩 log/）", v2=True)''')
rep('''b.box("x5d", E, 6, v2(SUB), fl("刪 gen/ 內剩下的自產檔（hash 相符者）"), 400)
b.files("x5df", P, 6, "－gen/ 兩檔（不進 git）", ["gen/.stamp", "gen/tools.just"], 360, cols=2)
b.box("x5e", E, 7, v2(SUB), fl("刪 baseline/ 內剩下的自產檔（hash 相符者；v2.8 §1）"), 400)
b.files("x5ef", P, 7, "－baseline/ 根檔（進 git）", ["baseline/.gitkeep", "baseline/.vendor_kit.toml"], 360, cw=(140, 198))
b.box("x5dd", E, 8, v2(SUB), fl("刪已空的子目錄 baseline/（gen/、cache/、log/、ci/ 亦同；rmdir，不 rm -rf）"), 400)
b.box("x6", E, 9, D12, "根 justfile 有我們那一行？", 260, ax="r")
b.box("x5r", P, 9, v2(RULE), fl("初始檔留著（永不刪，印清單）；使用者的 .gitignore／.dockerignore 只動我們 append 過且你同意的那幾行（v2.1 A、Q22 補）"), 360)
b.box("x8", E, 10, W12, fl("無／否：印指示（請自行移除 import 那行）"), 100, ax=0)
b.box("x7", E, 10, v2(D12), "有 → 問「要刪這一行嗎」？", 260, ax="r")
b.box("x7y", E, 11, W12, "是：只刪那一行", 140, ax=200)
b.box("x7f", P, 11, F12, "justfile（少一行：import '.vendor_kit/entry.just'）", 360)
b.box("x9a", E, 12, v2(D12), "根 .dockerignore 存在？", 260, ax=120)
b.box("x9b", E, 13, v2(D12), fl("有 → 仍有與紀錄原文相同的行？"), 260, ax=120)
b.box("x9r", P, 13, v2(RULE), fl("append 行逐行比對（§4.3、v2.9 §5；CRLF／LF 等價）：紀錄的每一行仍與原文相同 → 刪該行；不同／缺 → 跳過並 warn；不是全有／全無；零命中 → 不動"), 360)
b.box("x9q", E, 14, v2(D12), fl("有 → 問「要刪這幾行嗎」？"), 260, ax=120)
b.box("x9z", E, 15, v2(W12), fl("無／否：不動 .dockerignore"), 110, ax="l")
b.box("x9y", E, 15, v2(W12), fl("是：逐行只刪仍相同的行；不同／缺的行跳過 warn"), 230, ax="r")
b.box("x9f", P, 15, v2(F12), ".dockerignore（只少仍相同的那幾行；其餘不動）", 360)
b.box("x5z", E, 16, v2(SUB), "刪進度日誌（最後一步；根 justfile 那行之後）= 交易完成", 400)
b.box("x5n", U, 17, v2(G12), "否 → 0：保留目錄與保護清單內的檔；印摘要", 220)
b.box("x5q", E, 17, v2(D12), ".vendor_kit/ 已空？", 200, ax="l")
b.box("x5y", U, 18, v2(G12), "0：印摘要", 220)
b.box("x5t", E, 18, v2(SUB), "是：刪空目錄（rmdir；不 rm -rf）", 400)''',
'''b.box("x5cg", E, 6, v2(SUB), fl("刪 config.toml（hash == baseline/vendor_kit/config.toml 副本才刪；被改過 → 保留並列出，v2.13 P6）"), 400)
b.box("x5cgf", P, 6, v2(F12), "－config.toml（進 git；只刪未改過的）", 360)
b.box("x5d", E, 7, v2(SUB), fl("刪 gen/ 內剩下的自產檔（hash 相符者）"), 400)
b.files("x5df", P, 7, "－gen/ 兩檔（不進 git）", ["gen/.stamp", "gen/tools.just"], 360, cols=2)
b.box("x5e", E, 8, v2(SUB), fl("刪 baseline/ 內剩下的自產檔（hash 相符者；v2.8 §1）"), 400)
b.files("x5ef", P, 8, "－baseline/ 根檔（進 git）", ["baseline/.gitkeep", "baseline/.vendor_kit.toml", "baseline/vendor_kit/config.toml（副本）"], 360, cw=(140, 198))
b.box("x5dd", E, 9, v2(SUB), fl("刪已空的子目錄 baseline/、gen/、cache/、ci/（rmdir，不 rm -rf；log/ 不刪，v2.14-6）"), 400)
b.box("x6", E, 10, D12, "根 justfile 有我們那一行？", 260, ax="r")
b.box("x5r", P, 10, v2(RULE), fl("初始檔留著（永不刪，印清單）；使用者的 .gitignore／.dockerignore 只動我們 append 過且你同意的那幾行（v2.1 A、Q22 補）"), 360)
b.box("x8", E, 11, SUB, fl("無／否：印指示（請自行移除 import 那行）"), 100, ax=0)
b.box("x7", E, 11, v2(D12), "有 → 問「要刪這一行嗎」？", 260, ax="r")
b.box("x7y", E, 12, SUB, "是：只刪那一行", 140, ax=200)
b.box("x7f", P, 12, F12, "justfile（少一行：import '.vendor_kit/entry.just'）", 360)
b.box("x9a", E, 13, v2(D12), "根 .dockerignore 存在？", 260, ax=120)
b.box("x9b", E, 14, v2(D12), fl("有 → 仍有與紀錄原文相同的行？"), 260, ax=120)
b.box("x9r", P, 14, v2(RULE), fl("append 行逐行比對（§4.3、v2.9 §5；CRLF／LF 等價）：紀錄的每一行仍與原文相同 → 刪該行；不同／缺 → 跳過並 warn；不是全有／全無；零命中 → 不動"), 360)
b.box("x9q", E, 15, v2(D12), fl("有 → 問「要刪這幾行嗎」？"), 260, ax=120)
b.box("x9z", E, 16, v2(SUB), fl("無／否：不動 .dockerignore"), 110, ax="l")
b.box("x9y", E, 16, v2(SUB), fl("是：逐行只刪仍相同的行；不同／缺的行跳過 warn"), 230, ax="r")
b.box("x9f", P, 16, v2(F12), ".dockerignore（只少仍相同的那幾行；其餘不動）", 360)
b.box("x5z", E, 17, v2(SUB), "刪進度日誌（最後一步；根 justfile 那行之後）= 交易完成", 400)
b.box("x5k", E, 18, v2(SUB), fl("不 rmdir .vendor_kit/（只剩 log/；uninstall 自己也在寫 log，v2.14-6）"), 400)
b.box("x5yl", L, 19, v2(W12), LXT, 280)
b.box("x5y", U, 19, v2(G12), fl("0：印摘要（.vendor_kit/log/ 留存、可手動刪；保護清單內的檔保留）"), 220)''')
rep('''b.D("xe10c", "x5b", "x5c"); b.H("xe10cf", "x5c", "x5cf", "刪"); b.D("xe10d", "x5c", "x5d"); b.H("xe10df", "x5d", "x5df", "刪")''',
'''b.D("xe10c", "x5b", "x5c"); b.H("xe10cf", "x5c", "x5cf", "刪"); b.D("xe10cg", "x5c", "x5cg"); b.H("xe10cgf", "x5cg", "x5cgf", "刪"); b.D("xe10d", "x5cg", "x5d"); b.H("xe10df", "x5d", "x5df", "刪")   # config.toml 依 v2.13 P6''')
rep('''b.D("xe17", "x5z", "x5q", al=True); b.H("xe18", "x5q", "x5n", "否"); b.D("xe19", "x5q", "x5t", "是", al=True); b.H("xe20", "x5t", "x5y")''',
'''b.D("xe17", "x5z", "x5k"); b.D("xe19", "x5k", "x5yl"); b.H("xe20", "x5yl", "x5y")   # .vendor_kit/ 保留（v2.14-6）；頁尾 launcher_exit（v2.14-2）''')
open("disc_v1_b.py", "w", encoding="utf-8").write(src)
print("patch 5 ok")
