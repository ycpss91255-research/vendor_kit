P = "disc_v1_a.py"; s = open(P, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (c, old[:80])
    s = s.replace(old, new)
rep(' ["1", "已釋出版驅動候選", "floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 第一行改為候選 C → sync（1 印 6-1）→ upgrade vendor_kit（1 印 6-2、薄殼重產）→ sync 0 → 工具 recipe → upgrade 全；第二次 upgrade vendor_kit → 0；禁由候選樹複製 fixture、禁 stub 引擎"],',
    ' ["1", "已釋出版驅動候選", "floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 第一行改為候選 C → sync（1 印 6-1）→ upgrade vendor_kit（1 印 6-2）→ sync 0 → 工具 recipe → upgrade 全 → 再 upgrade vendor_kit 0；禁由候選樹複製 fixture、禁 stub 引擎"],')
rep(' ["18", "私有工具", "add <repo>@<tag> 可拉；add／update 無 token → 1 印 6-3 逐字；錯 token → 1；對 token → 列出；TOKEN_FILE（驗 -v 掛載）；兩者同設 → 1；所有輸出與 metadata／log grep 不到 token"],',
    ' ["18", "私有工具", "add <repo>@<tag> 可拉；add／update 無 token → 1 印 6-3；錯 token → 1；對 token → 列出；TOKEN_FILE（驗 -v 掛載）；兩者同設 → 1；輸出、metadata、log 都 grep 不到 token"],')
open(P, "w", encoding="utf-8").write(s); print("ok")
