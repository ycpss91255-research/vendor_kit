# ================= 討論 D3：#13 並行安裝的 lock =================
d3 = [v("title", "1", TITLE, "討論 #13：兩個 just 同時安裝 ── 要不要 lock、怎麼做", 40, 20, 1500, 30)]
d3.append(v("d3_pre", "1", NOTE, "前例（agy，10 個工具）：apt/dpkg、Cargo、Nix、Bazel、uv、Go 都用 flock/fcntl 檔案鎖（核心自動釋放、沒有殘鎖問題）；Git 用 O_EXCL 建 index.lock（立即失敗，殺掉後要手動刪）；npm/pnpm 的 store 用 mkdir 目錄鎖 + mtime 判殘鎖（常出「stale lock」問題）；Terraform 用 lock 紀錄，永不過期要 force-unlock。\n前例沒有人拿「暫存目錄存在」當鎖（rsync、apt、Nix、Go、Maven 都是另外持鎖）。\n重要發現：我們現在的「先 rmtree 舊目錄再 rename 暫存目錄」不是原子替換 —— 中間有一瞬間 .<name>/ 不存在；兩個 install 交錯時第二個 rename 會失敗（目標非空）。", 40, 60, 1500, 90))
d3.append(opt("d3_a", 40, 170, 480, 160, "A：不鎖，靠暫存目錄 + rename", "每個 install 用自己的暫存目錄名（加 pid、亂數）。\n優：沒有殘鎖問題。\n缺：替換那一瞬間的競態還在；N 個 shell 就重裝 N 次；崩潰留下的暫存目錄要另外清。"))
d3.append(opt("d3_b", 540, 170, 480, 160, "B：mkdir .<name>.lock/ 當鎖", "有目錄 = 有人在裝 → 等 N 秒再失敗。\n優：所有檔案系統（含 NFS、macOS Docker Desktop、WSL）都可靠、實作最簡單。\n缺：容器被殺（Ctrl-C、OOM）會留殘鎖；用 mtime／PID 判殘鎖在容器裡都不可靠（PID 空間不同、時鐘偏差）。"))
d3.append(opt("d3_c", 1040, 170, 500, 160, "C（agy 建議）：flock 檔案鎖", ".vendor_kit/<name>.lock 用 flock：先試非阻塞，拿不到就印「等另一個 just」再阻塞 + 逾時。\n優：核心自動釋放，零殘鎖；後到者醒來看印記已是新版就直接跳過，不重工。\n缺：macOS Docker Desktop（virtiofs）、WSL 的 /mnt/c 上主機↔容器互鎖不可靠（同一 VM 內的容器互鎖仍可）。", rec=True))
d3.append(v("d3_flow", "1", SW(NEUTRAL), "方案 C 的 install（第 5 頁 install 泳道會改成這樣）", 40, 360, 1500, 300))
d3.append(v("h0", "d3_flow", ELLIPSE(GREEN), "開始 install", 30, 60, 160, 50))
d3.append(v("h1", "d3_flow", LEAF(), "flock .vendor_kit/<name>.lock\n（拿不到：印訊息、等最多 N 秒）", 230, 60, 260, 50))
d3.append(v("h2", "d3_flow", RHOMBUS, "拿到鎖後：印記\n已是目標版本？", 530, 45, 200, 80))
d3.append(v("h3", "d3_flow", LEAF(), "寫暫存目錄（唯一名）→ 寫印記\n→ 刪舊 .<name>/ → 改名（全程在鎖內）", 780, 60, 320, 50))
d3.append(v("h4", "d3_flow", LEAF(), "釋放鎖", 1140, 60, 120, 50))
d3.append(v("h5", "d3_flow", ELLIPSE(GREEN), "成功結束", 1300, 60, 160, 50))
d3.append(v("h6", "d3_flow", LEAF(), "跳過（別人剛裝好）", 530, 170, 200, 50))
d3.append(v("h7", "d3_flow", ELLIPSE(RED), "逾時：中止並提示\n「另一個 just 卡住了」", 230, 160, 260, 60))
d3.append(v("h8", "d3_flow", NOTE, "verify 也拿同一把鎖（共享模式），所以不會讀到「刪舊、改名」中間那一瞬間。", 780, 160, 460, 40))
d3.append(e("he0", "h0", "h1", "", (1, 0.5), (0, 0.5)))
d3.append(e("he1", "h1", "h2", "拿到", (1, 0.5), (0, 0.5)))
d3.append(e("he2", "h1", "h7", "逾時", (0.5, 1), (0.5, 0), vert=True))
d3.append(e("he3", "h2", "h3", "否", (1, 0.5), (0, 0.5)))
d3.append(e("he4", "h2", "h6", "是", (0.5, 1), (0.5, 0), vert=True))
d3.append(e("he5", "h3", "h4", "", (1, 0.5), (0, 0.5)))
d3.append(e("he6", "h4", "h5", "", (1, 0.5), (0, 0.5)))
d3.append('<mxCell id="he7" value="" style="' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;" edge="1" parent="d3_flow" source="h6" target="h4"><mxGeometry relative="1" as="geometry"><Array as="points"><mxPoint x="1200" y="195"/></Array></mxGeometry></mxCell>')
d3.append(v("d3_q", "1", NOTE, "要決定：\n1. 採 C（flock）？主機都是 Linux 的話 C 沒有缺點；如果要支援 macOS Docker Desktop／WSL，改 B（mkdir 鎖）或 C 失敗時退回 B。\n2. 等待上限 N 秒？（建議 60；CI 可用環境變數拉長）\n3. agy 另建議「symlink 切換」（.<name> 是指向 .vendor_kit/versions/<name>-<ver>/ 的連結，改連結才是真正原子）—— 我建議先不要：多一層目錄、要清舊版，鎖已經把替換視窗蓋住了。", 40, 690, 1500, 80))
d3 += legend_flow("d3", 40, 800, note=True)
d3 += terms("d3", 40, 910, [
 ("flock", "Linux 的檔案鎖：程序結束或被殺，核心自動解鎖，不會留殘鎖"),
 ("殘鎖（stale lock）", "拿鎖的程序死了但鎖檔還在，後面的人永遠等不到；mkdir 鎖的典型問題"),
 ("原子替換", "外面的人看到的不是完整舊版就是完整新版，沒有中間狀態；目前的 rmtree + rename 做不到，要靠鎖蓋住"),
 ("virtiofs / 9p", "macOS Docker Desktop 與 WSL 把主機目錄掛進容器用的檔案系統，檔案鎖在上面不可靠"),
])
pages.append(("d3", "討論 #13：並行安裝 lock", d3))

# ================= 討論 D4：#12 verify 比什麼 =================
d4 = [v("title", "1", TITLE, "討論 #12：verify 的基準與範圍 ── 每次 just 都要跑，比什麼、比多細", 40, 20, 1500, 30)]
d4.append(v("d4_pre", "1", NOTE, "前例（agy，13 個工具）：安裝後的完整性檢查幾乎都「比本地存的清單」，沒有人每次執行都從來源重取 —— dpkg -V 只比 md5；rpm -V 比 size/mode/digest/owner/mtime；Nix 比整棵樹的 hash（含權限、symlink）並把目錄設唯讀；Go 比整目錄摘要且快取設唯讀；pip/npm/Homebrew/Terraform 只在安裝時驗、之後信任。\n多餘的檔案：dpkg/rpm/pip 忽略；Nix、Go 視為被改。\n效能：Git 的做法是先比 stat（size、mtime），沒變就不重算 hash；pnpm 先比 size 再算 sha512。", 40, 60, 1500, 90))
d4.append(opt("d4_a", 40, 170, 480, 150, "A：只比印記裡的內容 hash（現況）", "每檔 sha256 跟印記比。\n優：簡單，小目錄夠快。\n缺：抓不到多塞進來的檔、抓不到 chmod +x 之類的權限改動。"))
d4.append(opt("d4_b", 540, 170, 480, 150, "B（建議）：印記 + 檔案集合 + 權限位", "印記每列存 path、mode、size、mtime、sha256。\n先比檔案集合（缺檔、多檔）與 mode；再比 size/mtime，有變才重算 sha256。\n優：離線、完整（前例 rpm -V、Nix、Go 都這樣）、快。\n缺：印記格式變複雜一點。", rec=True))
d4.append(opt("d4_c", 1040, 170, 500, 150, "C：每次從 image 重取來比", "docker run 把 /dist 讀出來逐檔比。\n優：不依賴印記。\n缺：每次 just 多起一次容器、多讀一次 image；前例只在「修復」情境這樣做（nix-store --repair、go clean -modcache）。"))
d4.append(v("d4_flow", "1", SW(NEUTRAL), "方案 B 的 verify（第 5 頁 verify 泳道會改成這樣）", 40, 350, 1500, 250))
d4.append(v("k0", "d4_flow", ELLIPSE(GREEN), "開始 verify", 30, 60, 160, 50))
d4.append(v("k1", "d4_flow", LEAF(), "讀印記（含每檔 mode、size、mtime、sha256）", 230, 60, 300, 50))
d4.append(v("k2", "d4_flow", RHOMBUS, "檔案集合與\nmode 都相同？", 570, 45, 200, 80))
d4.append(v("k3", "d4_flow", LEAF(), "對 size 或 mtime 變了的檔\n重算 sha256 比對", 810, 60, 260, 50))
d4.append(v("k4", "d4_flow", RHOMBUS, "全部相符？", 1110, 45, 180, 80))
d4.append(v("k5", "d4_flow", ELLIPSE(GREEN), "通過", 1330, 60, 140, 50))
d4.append(v("k6", "d4_flow", ELLIPSE(RED), "失敗：列出缺／多／被改的檔", 570, 160, 300, 50))
d4.append(e("ke0", "k0", "k1", "", (1, 0.5), (0, 0.5)))
d4.append(e("ke1", "k1", "k2", "", (1, 0.5), (0, 0.5)))
d4.append(e("ke2", "k2", "k3", "是", (1, 0.5), (0, 0.5)))
d4.append(e("ke3", "k3", "k4", "", (1, 0.5), (0, 0.5)))
d4.append(e("ke4", "k4", "k5", "是", (1, 0.5), (0, 0.5)))
d4.append(e("ke5", "k2", "k6", "否", (0.5, 1), (0.5, 0), vert=True))
d4.append('<mxCell id="ke6" value="否" style="' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="d4_flow" source="k4" target="k6"><mxGeometry x="-0.6" relative="1" as="geometry"><Array as="points"><mxPoint x="1200" y="185"/></Array></mxGeometry></mxCell>')
d4.append(v("d4_q", "1", NOTE, "要決定：\n1. 採 B？\n2. 多餘的檔案（印記沒列的）視為「被改」→ 中止（跟 Nix、Go 一樣，因為多出來的可能是被塞進去的腳本）？還是只警告？\n3. 印記本身被改的防護：印記在 .<name>/ 裡、.<name>/ 不進 git；agy 建議可選簽章（cosign／minisign）—— 我建議先不做，先靠「印記第一行的 image digest 是鎖定的、重裝即可回到乾淨狀態」。", 40, 630, 1500, 80))
d4 += legend_flow("d4", 40, 740, note=True)
d4 += terms("d4", 40, 850, [
 ("mode / 權限位", "檔案的讀寫執行權限（例如可執行）；改了它不會動到內容 hash，所以要另外比"),
 ("stat / size / mtime", "不打開檔案就能拿到的資訊：大小、最後修改時間；先比這些能省掉大部分 hash 計算"),
 ("檔案集合", "印記列的檔名清單 vs 目錄裡實際有的檔名：少的 = 缺檔，多的 = 多餘檔"),
 ("cosign / minisign", "幫檔案簽名的工具，能證明印記是工具寫的不是別人偽造的；本題先不採用"),
])
pages.append(("d4", "討論 #12：verify 比什麼", d4))
