討論 #12：verify 的基準與範圍 ── 每次 just 都要跑，比什麼、比多細
前例（agy，13 個工具）：安裝後的完整性檢查幾乎都「比本地存的清單」，沒有人每次執行都從來源重取 —— dpkg -V 只比 md5；rpm -V 比 size/mode/digest/owner/mtime；Nix 比整棵樹的 hash（含權限、symlink）並把目錄設唯讀；Go 比整目錄摘要且快取設唯讀；pip/npm/Homebrew/Terraform 只在安裝時驗、之後信任。
多餘的檔案：dpkg/rpm/pip 忽略；Nix、Go 視為被改。
效能：Git 的做法是先比 stat（size、mtime），沒變就不重算 hash；pnpm 先比 size 再算 sha512。
<b>A：只比印記裡的內容 hash（現況）</b>
每檔 sha256 跟印記比。
優：簡單，小目錄夠快。
缺：抓不到多塞進來的檔、抓不到 chmod +x 之類的權限改動。
<b>B（建議）：印記 + 檔案集合 + 權限位</b>
印記每列存 path、mode、size、mtime、sha256。
先比檔案集合（缺檔、多檔）與 mode；再比 size/mtime，有變才重算 sha256。
優：離線、完整（前例 rpm -V、Nix、Go 都這樣）、快。
缺：印記格式變複雜一點。
<b>C：每次從 image 重取來比</b>
docker run 把 /dist 讀出來逐檔比。
優：不依賴印記。
缺：每次 just 多起一次容器、多讀一次 image；前例只在「修復」情境這樣做（nix-store --repair、go clean -modcache）。
方案 B 的 verify（第 5 頁 verify 泳道會改成這樣）
開始 verify
讀印記（含每檔 mode、size、mtime、sha256）
檔案集合與
mode 都相同？
對 size 或 mtime 變了的檔
重算 sha256 比對
全部相符？
通過
失敗：列出缺／多／被改的檔
是
是
否
否
要決定：
1. 採 B？
2. 多餘的檔案（印記沒列的）視為「被改」→ 中止（跟 Nix、Go 一樣，因為多出來的可能是被塞進去的腳本）？還是只警告？
3. 印記本身被改的防護：印記在 .<name>/ 裡、.<name>/ 不進 git；agy 建議可選簽章（cosign／minisign）—— 我建議先不做，先靠「印記第一行的 image digest 是鎖定的、重裝即可回到乾淨狀態」。
淺灰：情境分組（無狀態意義）
黃：判斷
綠：起點／終點
紅：錯誤終止
紫：子命令（在容器內執行）
白：步驟
便條：補充說明
實線 = 執行順序（指向檔案時 = 寫入／讀取）
本頁名詞
mode / 權限位
檔案的讀寫執行權限（例如可執行）；改了它不會動到內容 hash，所以要另外比
stat / size / mtime
不打開檔案就能拿到的資訊：大小、最後修改時間；先比這些能省掉大部分 hash 計算
檔案集合
印記列的檔名清單 vs 目錄裡實際有的檔名：少的 = 缺檔，多的 = 多餘檔
cosign / minisign
幫檔案簽名的工具，能證明印記是工具寫的不是別人偽造的；本題先不採用