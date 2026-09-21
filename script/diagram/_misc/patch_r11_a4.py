P = "disc_v1_a.py"; s = open(P, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (c, old[:80])
    s = s.replace(old, new)
rep(' ["frozen", "resolveapply", "N", "digestfile", "inspect", "state5", "rescue", "engine_changed"])',
    ' ["digestfile", "inspect", "state5", "rescue", "frozen", "resolveapply", "N", "engine_changed"])')
rep(' ["1", "已釋出版驅動候選", "floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 第一行改為候選 C → sync（1 印 6-1、零 tracked 寫入）→ upgrade vendor_kit（1 印 6-2、薄殼重產）→ sync 0 → 工具 recipe → upgrade 全；第二次 upgrade vendor_kit → 0；禁止由候選樹複製 fixture、禁 stub 引擎"],',
    ' ["1", "已釋出版驅動候選", "floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 第一行改為候選 C → sync（1 印 6-1）→ upgrade vendor_kit（1 印 6-2、薄殼重產）→ sync 0 → 工具 recipe → upgrade 全；第二次 upgrade vendor_kit → 0；禁由候選樹複製 fixture、禁 stub 引擎"],')
rep(' ["18", "私有工具", "add <repo>@<tag> 可拉；add <repo> 無 token → 1 印 6-3；update 無 token → 1 印 6-3 逐字；錯 token → 1；對 token → 列出；TOKEN_FILE（驗 -v 掛載、容器內路徑）；兩者同設 → 1；所有輸出與 metadata／log grep 不到 token"],',
    ' ["18", "私有工具", "add <repo>@<tag> 可拉；add／update 無 token → 1 印 6-3 逐字；錯 token → 1；對 token → 列出；TOKEN_FILE（驗 -v 掛載）；兩者同設 → 1；所有輸出與 metadata／log grep 不到 token"],')
rep(' ["30", "啟動器 argv 跳脫（bats）", "餵 \\"、\\\\、換行、[、]、非 ASCII、-n foo、空字串、以 \\\\ 結尾 → launcher_start.attributes.argv 經 json.loads 還原後逐項相等；dash 與 busybox sh 各跑一次"],',
    ' ["30", "啟動器 argv 跳脫（bats）", "餵 \\"、\\\\、換行、[、]、非 ASCII、-n foo、空字串、\\\\ 結尾 → launcher_start 的 argv 經 json.loads 還原後逐項相等；dash 與 busybox 各跑一次"],')
rep(' ["31", "config.toml", "keep／days 為 0、負數、非數字、非整數、重複、缺鍵、缺檔 → 預設 50／30（缺鍵／缺檔外印警告）；51 檔或 31 天前的檔 → 動詞結束後被 prune，本次的檔與 .gitignore 不刪；改過的 config.toml → upgrade vendor_kit 三方合併並詢問"],',
    ' ["31", "config.toml", "keep／days 為 0、負數、非數字、重複、缺鍵、缺檔 → 預設 50／30（缺鍵／缺檔外印警告）；51 檔或 31 天前的檔 → 結束後被 prune，本次的檔與 .gitignore 不刪；改過的 → upgrade vendor_kit 三方合併"],')
open(P, "w", encoding="utf-8").write(s); print("ok")
