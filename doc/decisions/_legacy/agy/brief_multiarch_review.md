題目：多架構（amd64 + arm64，含 Jetson）與 CI／registry 平台隔離。
平台範圍：Ubuntu/Linux amd64+arm64（WSL2 視同 Linux，macOS 不在範圍）。.version 鎖 multi-arch index digest；dist 內容必須與架構無關（不含編譯二進位、不含 symlink）；vendor_kit 與工具 image 都要 multi-arch build；CI 可能是 GitHub Actions 或 GitLab CI，CI 檔只呼叫 vendor_kit 出貨的平台無關腳本 test/ci/check.sh；image 倉庫可能是 GHCR 或 GitLab Container Registry。
要回答：(1) vendor_kit 自己的 CI 矩陣：arm64 上要不要真的跑測試（GitHub arm64 runner / QEMU / 自架 Jetson runner）；(2) bake 的 multi-platform build 與 release-test 在兩個架構各跑一次的做法；(3) 工具 repo 的 CI 範本；(4) GitLab 拉 GHCR 私有 image 的 token（deploy token / PAT / CI_JOB_TOKEN）與是否同時推兩個 registry；(5) test/ci/check.sh 用 sh 還是 just recipe。
第 12 頁初版文字：
# ================= Page 12: 對外契約與 CI 隔離（初版，供討論） =================
p13 = [v("title", "1", TITLE, "對外契約 ── vendor_kit 對外承諾的每一個介面，以及 CI 怎麼隔離（GitHub / GitLab 都只呼叫我們的腳本）", 40, 20, 1500, 30)]
CT_H = "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999999;fontSize=12;fontStyle=1;align=center;strokeWidth=1;"
CT_C = "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#999999;fontSize=12;align=left;spacingLeft=6;strokeWidth=1;"
CT_K = CT_C + "fontStyle=1;"
CCOLS = [("契約", 190), ("誰對誰", 220), ("內容（承諾不會隨便改的部分）", 620), ("誰用它來測", 300)]
def ctable(prefix, parent, x, y, rows, rh=52):
    cx = x
    for i, (h, w) in enumerate(CCOLS):
        p13.append(v(f"{prefix}_h{i}", parent, CT_H, h, cx, y, w, 30)); cx += w
    for r, row in enumerate(rows):
        cx = x
        for i, (cell, (h, w)) in enumerate(zip(row, CCOLS)):
            p13.append(v(f"{prefix}_r{r}c{i}", parent, CT_K if i == 0 else CT_C, cell, cx, y + 30 + r * rh, w, rh)); cx += w
    return y + 30 + len(rows) * rh
CW = sum(w for _, w in CCOLS)
p13.append(v("ct", "1", SW(RED), "對外契約（五個介面）", 40, 70, CW + 40, 440))
yc = ctable("ct", "ct", 20, 50, [
 ("① 使用者介面", "使用者 → 啟動器", "just 指令名與行為：init / diff / accept / upgrade / dev / undev（第 9 頁）；bootstrap.sh 的用法；結束狀態（0 成功／非 0 失敗；diff 為 0 無差異／1 工具有改／2 可能重疊）", "acceptance 測試（第 8 頁）；下游的 CI"),
 ("② 啟動器 ↔ 容器", ".vendor_kit/vendor.just → vendor_kit 容器", "docker run 的參數：-u UID:GID、-v 專案:/repo；argv：--name --self --repo --dist + 子命令 install / init / verify / diff / accept / bootstrap / upgrade；結束狀態 0/1/2；image 內 /dist 的佈局（files/、init.toml、VERSION）", "system 測試（docker run 每個子命令）"),
 ("③ 專案裡的檔", "vendor_kit → 專案 repo", ".version 格式（TOML，[tools] 一行一工具 <name> = \"image:tag@sha256\"，含 vendor_kit 行）；.version.local；.vendor_kit/ 佈局（vendor.just、tools.just、.stamp、baseline/<name>/）；.<name>/.stamp 格式（第一行 image，之後 sha256 路徑）", "integration 測試（bootstrap / install 寫出的檔）"),
 ("④ 工具 repo 要交的", "工具 repo → vendor_kit", "dist/（全部出貨、與架構無關、不含 symlink）；init.toml 格式（[[file]] src/dest）；dist/just/tool.just（工具自己的指令）；Dockerfile.dist（FROM vendor_kit + COPY）；image 命名 <name>-dist:tag，multi-arch（amd64 + arm64）", "env-test / release-test（用 fixtures 假工具）；工具 repo 的 CI"),
 ("⑤ 給下游的 CI 腳本", "vendor_kit → 專案／工具 repo 的 CI", "一組平台無關的測試腳本（下方），內容 = 上面四條契約的檢查；GitHub / GitLab 的 CI 檔只負責呼叫它", "下游 CI（GitHub Actions 或 GitLab CI 皆可）"),
])
p13.append(v("ct_n", "ct", NOTE, "待決（issue #14）：契約版本號寫在哪（.vendor_kit/.stamp？image label？），哪些改動算破壞相容（要升大版）、誰檢查啟動器與容器內 vendor_kit 版本不合。", 20, yc + 10, CW, 44))
# CI 隔離
p13.append(v("ci", "1", SW(NEUTRAL), "CI 隔離：CI 平台檔只呼叫我們的腳本，換平台不用改測試", 40, 540, CW + 40, 300))
p13.append(v("ci_gh", "ci", LEAF(YELLOW), "GitHub Actions\n.github/workflows/*.yaml（薄：只呼叫）", 20, 50, 320, 50))
p13.append(v("ci_gl", "ci", LEAF(YELLOW), "GitLab CI\n.gitlab-ci.yml（薄：只呼叫）", 20, 120, 320, 50))
p13.append(v("ci_sc", "ci", LEAF(), "vendor_kit 出貨的測試腳本（平台無關）\ntest/ci/check.sh：bootstrap 檢查 → install → verify → diff 結束狀態\n（只需要 docker + git + just）", 420, 50, 420, 120))
p13.append(v("ci_bake", "ci", PURPLE_LEAF, "docker buildx bake validate / release\n（vendor_kit 自己的測試，第 8 頁）", 920, 50, 380, 50))
p13.append(v("ci_reg", "ci", LEAF(YELLOW), "image 倉庫：GHCR 或 GitLab Container Registry\n（.version 記完整位址，docker login 就能拉；Renovate 兩邊都支援）", 920, 120, 380, 60))
p13.append(e("cie1", "ci_gh", "ci_sc", "呼叫", (1, 0.5), (0, 0.2083)))
p13.append(e("cie2", "ci_gl", "ci_sc", "呼叫", (1, 0.5), (0, 0.7917)))
p13.append(e("cie3", "ci_sc", "ci_bake", "vendor_kit repo 內", (1, 0.2083), (0, 0.5)))
p13.append(e("cie4", "ci_sc", "ci_reg", "拉 image", (1, 0.8333), (0, 0.5)))
p13.append(v("ci_n", "ci", NOTE, "待決：GitLab 拉 GHCR 私有 image 要放 token（GitLab CI 變數）；要不要同時推到兩個 registry？測試腳本用 sh 還是 just recipe（just 在 CI runner 也要裝）？", 20, 200, 1300, 44))
p13 += legend("p13", 40, 870, ["red", "yellow", "pimg", "neutral", "white"], "實線 = 呼叫／依賴方向")
p13 += terms("p13", 40, 980, [
 ("對外契約", "我們承諾「這樣用一定可以、不會隨便改」的介面清單；改了就要升版並公告"),
 ("啟動器", ".vendor_kit/ 裡 vendor_kit 寫出的 just 指令（第 2、10 頁）"),
 ("argv / 子命令", "傳給容器內程式的參數／install、init 這些動作名"),
 ("GitHub Actions / GitLab CI", "兩家平台各自的自動化流程；設定檔格式不同，所以我們的測試不寫在裡面，寫在自己的腳本"),
 ("GHCR / GitLab Container Registry", "GitHub 與 GitLab 各自的 image 倉庫；都是標準 Docker registry，位址不同而已"),
 ("multi-arch", "同一個 image 名稱同時有 amd64 與 arm64 版本；.version 鎖的 digest 是這組的索引"),
 ("issue #14", "相容性承諾這一題的 GitHub 討論串"),
])
