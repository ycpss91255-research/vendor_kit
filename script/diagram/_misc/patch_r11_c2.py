P = "disc_v1_c.py"; s = open(P, encoding="utf-8").read()
def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (c, old[:80])
    s = s.replace(old, new)
rep('b.box("o5", SH, 7, D12, "前置檢查①（不分 tar／tag）：在 git repo 內？", 300, ax="l")', 'b.box("o5", SH, 7, D12, "前置①：在 git repo 內？", 300, ax="l")')
rep('b.box("o6", SH, 8, D12, "前置檢查②：just ≥ 1.33.0？", 300, ax="l")', 'b.box("o6", SH, 8, D12, "前置②：just ≥ 1.33.0？", 300, ax="l")')
rep('b.box("o8x", UO, 17, v2(R12), "是 → 1：中止（清半成品、保留 log/；version.local.toml 未寫）", 230)', 'b.box("o8x", UO, 17, v2(R12), "是 → 1：中止（清半成品、保留 log/）", 230)')
rep('b.box("o1w", UO, 2, LBL, "【便利包裝，非契約】（可選）sh local_bootstrap.sh [-y] 做三步：", 230, 24, ax="l", minh=24)', 'b.box("o1w", UO, 2, LBL, "【便利包裝，非契約】（可選）sh local_bootstrap.sh [-y] 做三步：", 500, 24, ax="l", minh=24)')
rep('b.box("o1a", UO, 3, W12, "docker version --format \'{{.Server.Arch}}\' 偵測 daemon 架構", 230)', 'b.box("o1a", UO, 3, W12, "docker version 偵測 daemon 架構（.Server.Arch）", 230)')
rep('N16 = "已定（Q26、v2.6-1、v2.7-1／-2、v2.8-4／-5、v2.13 P4、interface_spec §1.2、§4.8、§7.4-16／17）：契約入口 = bootstrap.sh --local <引擎 tar>，只涉及引擎（local_bootstrap.sh 為便利包裝、非契約）；先建 log/bootstrap/ 寫 launcher_start 才開始；前置檢查不分 --local 值型別一律先做；--local 三分支（檔案先驗存在／tag 不 load 不讀 .digest／兩者皆成立 → 1 + 6-37）；每個 tar 附同名 .digest；version.toml 寫正式 ref@digest；install 失敗 → 1 清半成品、保留 log/；離線接工具 = 另備工具 tar → add --local；離線 upgrade 不支援。"',
    'N16 = "已定（Q26、v2.6-1、v2.7-1／-2、v2.8-4／-5、v2.13 P4、interface_spec §1.2、§4.8、§7.4-16／17）：契約入口 = bootstrap.sh --local <引擎 tar>，只涉及引擎（local_bootstrap.sh 為便利包裝、非契約）；先寫 launcher_start 才開始；前置檢查不分 --local 值型別一律先做；--local 三分支（檔案／tag／歧義 → 1 + 6-37）；tar 附同名 .digest；version.toml 寫正式 ref@digest；install 失敗 → 1 清半成品、保留 log/；離線 upgrade 不支援。"')
open(P, "w", encoding="utf-8").write(s); print("ok")
