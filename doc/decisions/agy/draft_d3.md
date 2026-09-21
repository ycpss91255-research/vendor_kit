討論 #13：兩個 just 同時安裝 ── 要不要 lock、怎麼做
前例（agy，10 個工具）：apt/dpkg、Cargo、Nix、Bazel、uv、Go 都用 flock/fcntl 檔案鎖（核心自動釋放、沒有殘鎖問題）；Git 用 O_EXCL 建 index.lock（立即失敗，殺掉後要手動刪）；npm/pnpm 的 store 用 mkdir 目錄鎖 + mtime 判殘鎖（常出「stale lock」問題）；Terraform 用 lock 紀錄，永不過期要 force-unlock。
前例沒有人拿「暫存目錄存在」當鎖（rsync、apt、Nix、Go、Maven 都是另外持鎖）。
重要發現：我們現在的「先 rmtree 舊目錄再 rename 暫存目錄」不是原子替換 —— 中間有一瞬間 .<name>/ 不存在；兩個 install 交錯時第二個 rename 會失敗（目標非空）。
<b>A：不鎖，靠暫存目錄 + rename</b>
每個 install 用自己的暫存目錄名（加 pid、亂數）。
優：沒有殘鎖問題。
缺：替換那一瞬間的競態還在；N 個 shell 就重裝 N 次；崩潰留下的暫存目錄要另外清。
<b>B：mkdir .<name>.lock/ 當鎖</b>
有目錄 = 有人在裝 → 等 N 秒再失敗。
優：所有檔案系統（含 NFS、macOS Docker Desktop、WSL）都可靠、實作最簡單。
缺：容器被殺（Ctrl-C、OOM）會留殘鎖；用 mtime／PID 判殘鎖在容器裡都不可靠（PID 空間不同、時鐘偏差）。
<b>C（agy 建議）：flock 檔案鎖</b>
.vendor_kit/<name>.lock 用 flock：先試非阻塞，拿不到就印「等另一個 just」再阻塞 + 逾時。
優：核心自動釋放，零殘鎖；後到者醒來看印記已是新版就直接跳過，不重工。
缺：macOS Docker Desktop（virtiofs）、WSL 的 /mnt/c 上主機↔容器互鎖不可靠（同一 VM 內的容器互鎖仍可）。
方案 C 的 install（第 5 頁 install 泳道會改成這樣）
開始 install
flock .vendor_kit/<name>.lock
（拿不到：印訊息、等最多 N 秒）
拿到鎖後：印記
已是目標版本？
寫暫存目錄（唯一名）→ 寫印記
→ 刪舊 .<name>/ → 改名（全程在鎖內）
釋放鎖
成功結束
跳過（別人剛裝好）
逾時：中止並提示
「另一個 just 卡住了」
verify 也拿同一把鎖（共享模式），所以不會讀到「刪舊、改名」中間那一瞬間。
拿到
逾時
否
是
要決定：
1. 採 C（flock）？主機都是 Linux 的話 C 沒有缺點；如果要支援 macOS Docker Desktop／WSL，改 B（mkdir 鎖）或 C 失敗時退回 B。
2. 等待上限 N 秒？（建議 60；CI 可用環境變數拉長）
3. agy 另建議「symlink 切換」（.<name> 是指向 .vendor_kit/versions/<name>-<ver>/ 的連結，改連結才是真正原子）—— 我建議先不要：多一層目錄、要清舊版，鎖已經把替換視窗蓋住了。
淺灰：情境分組（無狀態意義）
黃：判斷
綠：起點／終點
紅：錯誤終止
紫：子命令（在容器內執行）
白：步驟
便條：補充說明
實線 = 執行順序（指向檔案時 = 寫入／讀取）
本頁名詞
flock
Linux 的檔案鎖：程序結束或被殺，核心自動解鎖，不會留殘鎖
殘鎖（stale lock）
拿鎖的程序死了但鎖檔還在，後面的人永遠等不到；mkdir 鎖的典型問題
原子替換
外面的人看到的不是完整舊版就是完整新版，沒有中間狀態；目前的 rmtree + rename 做不到，要靠鎖蓋住
virtiofs / 9p
macOS Docker Desktop 與 WSL 把主機目錄掛進容器用的檔案系統，檔案鎖在上面不可靠