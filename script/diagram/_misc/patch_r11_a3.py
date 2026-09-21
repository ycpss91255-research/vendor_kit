P = "disc_v1_a.py"; s = open(P, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (c, old[:80])
    s = s.replace(old, new)
rep('"vendor_kit 自身 CI 的前兩個 stage：env-test = smoke（環境檢查先於一切：docker、just 版本、runner 能力）；test-base FROM env-test = 之後 lint／unit／install／merge 各測試 stage 的共同基底，環境不對就沒有任何測試會跑"',
    '"vendor_kit 自身 CI 的前兩個 stage：env-test = smoke（環境檢查先於一切：docker、just 版本、runner 能力）；test-base FROM env-test = 之後各測試 stage 的共同基底，環境不對就沒有任何測試會跑"')
rep('"同一支腳本的供應端模式：在工具 repo 的 CI 驗 dist 佈局、init.toml、dest 規則、無 symlink／hardlink、無 CRLF、just 1.33.0 可解析、_sync lint、Dockerfile.dist 含 LABEL、image 可展開、兩平台位元組一致"',
    '"同一支腳本的供應端模式：在工具 repo 的 CI 驗 dist 佈局、init.toml、dest 規則、無 symlink／CRLF、just 1.33.0 可解析、_sync lint、LABEL、image 可展開、兩平台一致"')
rep('"相容承諾的下限：固定 release 常數 = 第一個正式版（v1.0.0、P=1、schema=1），只能經 ADR + major 提高；低於 floor → 3 印 6-18 零寫入；floor 檢查先於任何上網（斷網也回 3；啟動器可先 inspect 引擎 LABEL）"',
    '"相容承諾的下限：固定 release 常數 = 第一個正式版（v1.0.0、P=1、schema=1），只能經 ADR + major 提高；低於 floor → 3 印 6-18 零寫入；floor 檢查先於任何上網（斷網也回 3）"')
rep('"啟動器一律先 docker image inspect <ref>：本機有 → 不 pull（不用 --pull never，docker 19.03 無此旗標）；斷網 + 本機已有 image → sync／build 必須成功（驗收）；斷網 + 無 image → 1 + 6-31 在 --timeout 內結束、不 hang；離線 upgrade 不支援"',
    '"啟動器一律先 docker image inspect <ref>：本機有 → 不 pull（不用 --pull never）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → 1 + 6-31 在 --timeout 內結束、不 hang；離線 upgrade 不支援"')
rep(' ["resolveapply", "N", "frozen", "inspect", "digestfile", "state5", "rescue", "engine_changed"])',
    ' ["frozen", "resolveapply", "N", "digestfile", "inspect", "state5", "rescue", "engine_changed"])')
open(P, "w", encoding="utf-8").write(s); print("ok")
