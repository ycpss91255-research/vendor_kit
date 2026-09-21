import re
# ---- a ----
src = open("disc_v1_a.py", encoding="utf-8").read()
old = 'pendq(p3b, "待處理問題\\n無")'
assert src.count(old) == 1
src = src.replace(old, 'pendq(p3b, "待處理問題\\ns2c：「stdout vk-resolve/1（先收完整份並驗文法…）合法才繼續」一格同時是收 stdout 的步驟與「回 0？／文法合法？」的判斷（直接長出三條分支）；各動詞細頁都拆成 stdout 步驟＋「resolve 回 0？」＋「文法合法？」兩個黃格，應比照拆開。")')
old = 'c, Y = lgd("p4", 40, Y, ["v3img", "v4mod", "v4unit", "v4host", "v4hgrp", "v4egrp", "v4pgrp", "v2git", "v2no", "v2usr", "v2code", "v2tag", "v4other", "notep"], '
assert src.count(old) == 1
src = src.replace(old, old.replace('"v4other", "notep"]', '"v4other", "notep", "pendq"]'))
old = 'pages_v1_a.append(("v1p4", "架構圖 v2", p4))'
assert src.count(old) == 1
P4 = ["f_cfg：config.toml 只有讀箭頭 w_cfg（→ schema），沒有任何寫箭頭；但 install 建它、upgrade vendor_kit 三方合併它（§4.9）；baseline/vendor_kit/config.toml 與 baseline/.vendor_kit.toml 也沒出現為寫入目標（f_bl 只有 baseline/<repo>/）。",
      "m_res_u0_0：「讀版本鎖定行、算 keep」一格兩事（讀鎖定行 vs 算 prune 的 keep 清單），且 keep 清單已另有 m_prune_u0_0。",
      "run_cli／mount_dist／ret_cli：run_cli 標籤「動詞、參數、介面版旗標」與 mount_dist 標籤「本機覆寫 <dir>/dist → /dist/<repo>」互相壓字並壓到主機框 p4H 標題；ret_cli「結束碼、vk-resolve」貼在啟動器紅框下緣，縮圖讀不出各屬哪條線。"]
src = src.replace(old, 'pendq(p4, "待處理問題\\n' + "\\n".join(P4) + '")\n' + old)
open("disc_v1_a.py", "w", encoding="utf-8").write(src)
print("a: v1p3b 1, v1p4", len(P4))
# ---- c ----
src = open("disc_v1_c.py", encoding="utf-8").read()
C = {
 "p9c": ["q12_fail_bus：匯流格文字說「記 failed，繼續其餘項；全部完成後由『全部刪除成功？』分流」，但唯一出邊 qe19fe 直接接紅終點 q12_fail_end，沒有回到 q12c2／q13；同一件事有兩個紅終點（q12_fail_end 與 q13x），圖與文字矛盾（規格：失敗記下、續刪其餘、最後摘要）。",
         "fb_q12j：建進度檔 q12j 失敗也接到「記 failed 繼續其餘項」匯流，但進度檔建不成就無處可記、且規格要求第一個寫入前必有進度檔，應直接回 1 不再清理、不能繼續刪 .tmp.dist／.tmp.*。"],
 "p16c": ["o10re／o10rey：菱形寫「resolve 已拿 flock：偵測到既有進度檔？」且 o10rey 在 resolve 容器內做恢復（寫檔）；規格 §3.1／§3.2 鎖在 apply 一開始拿、resolve 不寫任何檔；add（1）頁 cpq 是在 docker run resolve 之前先恢復，本頁順序與誰做都不同。"],
 "p16cb": ["fb_o10pg／fb_o10e3／fb_o10e4：三條到失敗匯流格的線無「失敗」標籤，與同格另一條無標籤的正常順序線分不出哪條是失敗；且水平段離檔案框只有 7–8px（如 y=687），縮圖像從檔案框發出；建議加「失敗」標籤並把水平段移到檔案框之間留白更大處。"],
 "p16ccc": ["fb_w4r0／fb_w4r0s／fb_w4r0b：到失敗匯流格的線無標籤，w4r0 等格同時有無標籤的正常順序線與失敗線，看不出哪條是失敗。",
            "w4vq：把「版本變動那次」併入「先驗既有 cache、相符就 0 不重裝」分支，舊 cache 若仍符合舊印記會回 0 而不裝新版；規格 §1.2 sync 與 sync（2′）頁 m3→m3vd 是印記≠鎖定即先取件重寫、之後才逐檔驗；三頁名詞「sync 快路徑／--verify」說明文同此錯。"],
 "p16ccb": ["we6x／we6：「≠」失敗線與跨頁入口進入線在 y=381、x≈810–970 完全重疊、箭頭方向相反，縮圖像入口橢圓直接連到紅色「≠ → 1」，看不出失敗線來源是 resolve sync 菱形；建議 we6 從菱形頂端進入或 we6x 改由菱形下方繞出。"],
 "p9": ["qe12z：「是：只印差集」→ 續 prune（2）的線走在泳道外框左邊界上（x=20 與 bP 框線重合）幾乎看不出；標籤「續（2）：apply prune --dry-run（零刪除）」被擠到框外、貼到頁面最左緣（有裁切風險）。"],
 "p16cc": ["we2y：線標籤「相符：用本機 tag（不 pull）」橫跨 x≈525–670，被 we5（「有」分支，x=580 垂直幹線）從中穿過，標籤壓線（與已列的 we2n 不同元件）。"],
}
def q(s): return '"' + s.replace('"', '\\"') + '"'
for var, items in C.items():
    m = re.search(rf'^foot\({var}, "{var}", .*?pend=\[(.*?)\]\)', src, re.M)
    assert m, var
    cur = m.group(1)
    new = ", ".join(q(t) for t in items) if cur.strip() == '"無"' else cur + ", " + ", ".join(q(t) for t in items)
    src = src[:m.start(1)] + new + src[m.end(1):]
    print("c:", var, len(items), "(replaced 無)" if cur.strip() == '"無"' else "")
open("disc_v1_c.py", "w", encoding="utf-8").write(src)
