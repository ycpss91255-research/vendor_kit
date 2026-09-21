# lock

## 一致
- 結論一致：要鎖，而且用 flock（方案 C）。A（不鎖只靠唯一暫存目錄）只能避免「兩邊寫同一個 .tmp」，擋不住 rmtree(.<name>) → rename 之間的空窗，同版本也會互刪；B（mkdir 目錄鎖）在 SIGKILL / OOM / docker stop 逾時後必留殘鎖，而「超齡就刪鎖」會把第二個 writer 放進來，心跳只能降低誤判、不能消除。
- 鎖檔絕不能放在 .vendor_kit/ 或 .<name>/ 裡：這兩個目錄會被整批替換，flock 鎖在 inode 上，替換後新程序開到的是新 inode，兩把鎖互不可見，互斥直接失效。鎖的身分必須固定、建立後不刪不改名。
- 一把專案級（repo-wide）鎖比每工具一把好：實作最簡單、沒有鎖序問題，而且順便蓋住共用產物（tools.just 等）的寫入。
- 不要自動退回 B。flock 與 mkdir 是兩種原語，沒有共同的互斥保證，部分程序用 C、部分用 B 等於沒鎖。
- 鎖只蓋住容器內持鎖的 install / verify，蓋不到主機端 wrapper、IDE、Docker build context、Compose 的後續讀檔。草稿說「鎖已蓋住替換視窗，所以可以先不做原子替換」這句不成立——只對持鎖讀者成立。
- 拿到鎖之後必須重讀 .version 與印記，不能用鎖前讀到的版本做決定；兩次呼叫版本可能不同（一邊在 git checkout），要定義「這次任務用哪份版本快照」。
- 逾時處理：可設定、0 = 立即失敗（給 CI）；逾時只回非零、不刪鎖、不殺持鎖者、不開始寫入。取鎖前先做 image pull 等不需互斥的事。
- flock 不等於崩潰復原：核心只釋放鎖，不會把 rmtree 到一半的舊目錄還原；「下一次能修好」和「任何瞬間都完整」是兩個不同層級的保證，要分開決定。
- agy 的資料有多處引錯或捏造（Nix 用 fcntl、WSL#3574、Debian#928347、lockfile 預設 10 秒、Bazel/pnpm/pip issue 引錯題），核心結論（用 flock）沒錯，但它的來源不能直接當定案依據。
- macOS Docker Desktop（virtiofs）不能當作「同 VM 內容器互鎖可用」：agy 這句沒有依據。兩位都主張明寫「不保證互斥」，不為它退回 B。
- 需要真正的雙容器並行測試當作閘門：同版本 / 不同版本同時裝、中途 docker kill 再重跑、逾時與不支援時不動使用者檔案。

## 分歧（含判斷）
- 鎖的對象放哪裡：選 Claude 的做法。codex 的 .vendor_kit-state/ 仍需要使用者改 .gitignore，正好撞到硬性限制；鎖目錄本身把三個問題一次解掉，而且 flock(2)/flock(1) 都明載支援目錄。唯一要注意：如果日後本來就要新增一個不被替換的狀態目錄，再改成該目錄下永久鎖檔即可，兩者互斥語意相同。
- flock 不支援（NFS、ENOTSUP/EOPNOTSUPP/ENOSYS/ENOLCK）時怎麼辦：偏 codex，但留逃生口：預設失敗並印清楚訊息，提供 VENDOR_KIT_NO_LOCK=1 讓使用者明確接受風險後放行。Cargo 敢放行是因為它的輸出大多可重入、不會 rmtree 共用目錄；我們的 install 是刪舊再換新，不鎖就跑等於回到 A 的互刪問題。Claude 自己在 open_questions 也把這點列為待決。
- 等待逾時預設值與逾時訊息：數字現在沒有實測依據，先用 60 秒 + 可覆寫（0 / -1），之後拿 Jetson 實測資料調整；codex 說 apt 的 120 是非互動模式、互動模式是 -1，所以「對齊 apt」本身站不住。訊息採 Claude 的方向但用 codex 的措辭：flock 由核心釋放，持鎖者的程序確實還存在（可能在跑、也可能被 docker pause 或卡住），所以可以說「另一個 vendor_kit 程序仍持有鎖，請用 docker ps 查看」，不要說「一定在正常跑」。
- 發布原子性：要不要改成 symlink 切換 / 不可變版本目錄：這是最大的分歧，兩邊各對一半。codex 對問題的診斷正確：任何目錄層級的原子替換（symlink 或 RENAME_EXCHANGE）都只保證「單一瞬間」完整，wrapper 跨多個檔案的讀取仍可能混版，只有版本固定能解。但 codex 的方案是整套重新設計（路徑契約、首次遷移、GC、wrapper 改走版本路徑），它自己列的前提（base 路徑契約能否容納 symlink、Dockerfile COPY、Compose）都還沒確認，不該現在定案。Claude 對成本的判斷正確：symlink 的代價在遷移與 GC，不在原子性。建議：第一版只做鎖 + 唯一暫存 + 鎖內 rmtree+rename，把「install 期間主機端讀者可能撞到空窗或混版」白紙黑字寫進限制；原子替換等使用者回答「要不要保護主機端讀者」後再選，若要，RENAME_EXCHANGE 是最小改動，若要跨檔案一致，才走版本固定。
- 後到者拿到鎖後印記已符合目標版本，要不要跳過：codex 對。跳過複製、但仍跑一次 verify（hash 比對），成本低，也符合 §6 驗證閘門的精神。
- A 與 B 算不算「符合硬性限制」：不是真的分歧，兩邊在回答不同問題：Claude 講的是「主機只准 Docker+git+just」這條依賴限制，codex 講的是正確性。結論一致：三案都不需主機額外工具，但只有 C 正確。
- mtime 判死不可靠的原因：codex 對原生 Linux 是正確的；Claude 的時鐘偏差只在 Docker Desktop VM（睡眠後時鐘漂移是已知問題）成立。既然 B 已被否決，此點不影響結論，但寫進文件時應用 codex 的理由。
- macOS Docker Desktop #7004 的嚴重程度：Claude 提供了更具體的查證（根因、版本），採 Claude 的描述；codex 的保留態度也對，寫文件時用「已知未修、不保證互斥」而非「必定壞」。實務結論相同：macOS 不列為支援互斥的平台。

## 對前例資料的更正
- Nix 的 path lock 用 flock() 不是 fcntl（src/libstore/unix/pathlocks.cc lockFile()）；agy 引的 file-system.cc 裡沒有 lockFile。Nix 特意避開 fcntl 是因為 fcntl 鎖在同程序關掉該檔任一 fd 時就釋放，這反而是支持 flock 的理由。
- Cargo 在 Linux 用 flock，fcntl 只用於 Solaris；agy 漏掉最關鍵的策略：try_acquire() 用 statfs 偵測到 NFS 就完全不鎖直接放行（cargo#2615：NFS 上 LOCK_NB 也可能永遠阻塞），ENOTSUP/EOPNOTSUPP/ENOSYS 也視為拿到鎖。
- microsoft/WSL#3574 是 Kali WSL 的 nmap 被 Defender 誤判，與檔案鎖無關。相關的是 #12169（WSL1 lxfs fcntl 不互斥）與 #4689（Windows 端存取 \\wsl$ 不支援鎖）。WSL2 /mnt/c（9p）的 flock 行為沒有可查證來源，應標「未驗證」。
- Debian Bug #928347 是 shellcheck 打包 bug，與 apt 無關。DPkg::Lock::Timeout 選項存在，但「互動模式預設 120 秒」不對：查到的是互動模式 -1、非互動模式 120，且受 CLI 相容版本設定影響；此逾時實作也不能推廣到 lists/archives 的鎖。
- isaacs/lockfile 的 opts.stale 沒有預設值，未設定就永不過期；「預設 10 秒」是編出來的。
- Yarn Berry 的 xfs.lockPromise 是 O_EXCL 建鎖檔 + 定期 touch mtime + 逾時判殘鎖，屬 mtime 心跳型，不是核心鎖；--immutable / YN0028 是限制 lockfile 能否被修改，與併行互斥無關。
- Yarn Classic 的 mutex 用 proper-lockfile，含心跳與 stale 判定，不是「SIGKILL 後一定要手動刪」的存在鎖。
- Bazel「輪詢持鎖者 PID 判死」未驗證；lock 檔寫 PID 是為了錯誤訊息顯示。#13600 是 zipper 覆蓋 zip 內容的 issue，與鎖無關。
- pnpm #6499 是版本問題、pip #8799 是 --target/--upgrade 行為，都不是併行 race；npm/pnpm「都用 mkdir+mtime 目錄鎖」混淆了歷史版本與共用快取，現代 cacache 明載支援無鎖併行。
- Terraform 本地 state 在 Unix 用 fcntl(F_SETLK)，.lock.info 不是完整互斥機制；遠端鎖要逐 backend 說明，不能一概說「永不過期、要 force-unlock」。
- docker/for-mac#7004：不只是主機↔容器，同容器內兩個 process、兩個不同容器都能同時拿到 LOCK_EX（fakeowner 層與 virtiofs 是兩個 superblock），2026 年 Docker Desktop 4.78 仍未修。「同 VM 內容器互鎖仍可」是錯的，草稿第 16 行照抄了這句要改。
- open(O_EXCL) 在 NFS 上壞掉的說法省略了條件：open(2) 明載 Linux 2.6+ 且 NFSv3+ 支援，警告只針對更舊環境。rename(2) 對 NFS 的警告是「回報失敗時操作可能已完成」，不是「rename 必有空窗」。
- 「mkdir 在所有檔案系統都可靠、實作最簡單」把原語原子性偷換成整套鎖協定可靠：B 要加心跳執行緒、逾時策略、殘鎖清理，實作反而最複雜，而且 Python 作為容器 PID 1 預設不處理 SIGTERM，docker stop / CI cancel 幾乎必留殘鎖。
- symlink 切換 Pattern A「rename 嚴格原子、絕不回 ENOTEMPTY」只在 .<name> 已是 symlink 或普通檔時成立；現有 15 個 repo 的 .base/ 是真目錄，第一次遷移 rename(symlink → 目錄) 回 EISDIR，仍要先 rmtree。agy 沒提遷移、versions/ 的舊版清理、verify 走訪 symlink 的邊界。
- 「flock 提供 100% crash safety」錯把解鎖當復原：核心只釋放鎖，rmtree 中途被殺仍會留下半套安裝。
- 「前例沒人拿暫存目錄當鎖，所以 A 是無鎖方案」超出證據：若以 mkdir 成功與否決定唯一持有者，那就是 B。
- 「容器與主機時鐘偏差讓 mtime 判死不可靠」在原生 Linux 不成立（time namespace 不虛擬化 CLOCK_REALTIME）；mtime 判死的真正問題是活程序被暫停或跑太久。
- asdf / mise 採特定 staging+symlink 實作、WSL/9p 全面不可用：本次沒找到直接證據，不宜寫進定案依據。

## 最終建議
採方案 C（flock），並依下列修正定案：
1. 鎖對象：flock /repo 目錄本身（open O_RDONLY|O_DIRECTORY 後 fcntl.flock，務必用 flock 不用 lockf），一個專案一把鎖；不新增鎖檔、不動 .gitignore、沒有 inode 替換問題。install 取 LOCK_EX，verify 取 LOCK_SH；tools.just 等共用產物的寫入也在同一把鎖內。
2. 拿到鎖後重讀 .version 與印記；印記已符合目標版本就跳過複製，但仍跑 verify（hash 比對）。取鎖前先做 image pull 等不需互斥的事。
3. 逾時：預設 60 秒（可覆寫 VENDOR_KIT_LOCK_TIMEOUT，0 = 立即失敗給 CI，-1 = 無限），非阻塞 + monotonic deadline 短間隔重試；1 秒後開始印「另一個 vendor_kit 程序仍持有鎖，可用 docker ps 查看」，每 5 秒重印；逾時只回非零、不刪鎖、不殺持鎖者、不寫入。等有 Jetson 實測資料再調數字。
4. 鎖不支援（ENOTSUP/EOPNOTSUPP/ENOSYS/ENOLCK）或 I/O、權限錯誤：直接失敗並印清楚訊息，提供 VENDOR_KIT_NO_LOCK=1 讓使用者明確接受風險後放行；絕不自動退回 B。
5. 暫存目錄：.<name>.tmp.<urandom 8 hex>（容器內 pid 恆為 1 沒辨識力），持鎖時順手清掉所有殘留 .<name>.tmp.*；docker run 加 --init 讓 SIGTERM 能傳給 Python 做清理。
6. 發布：第一版維持鎖內 rmtree+rename，並把「install 期間主機端 wrapper 可能撞到空窗或混版」明寫進限制。原子替換等使用者回答第 2 題後再決定：只要「任何瞬間目錄完整」→ renameat2(RENAME_EXCHANGE) + 失敗退回 rmtree+rename；要「跨檔案版本一致」→ 才做不可變版本目錄 + 版本固定，且要先確認 base 路徑契約能容納。不做單純的 symlink 切換。
7. 支援範圍：明寫「互斥保證僅限原生 Linux 主機 + 本機檔案系統（ext4/XFS/overlay）」；macOS Docker Desktop（for-mac#7004 未修）、WSL2 /mnt/c、NFS 列為不保證互斥並印警告。
8. 測試閘門：雙容器同版本 / 不同版本 / 不同工具同時 install（含 tools.just 更新）、複製與發布前後 docker kill 再重跑、verify 後立刻另一個 install、鎖逾時與不支援時不寫入且使用者檔不變。
9. 草稿與 agy 資料的錯誤依 agy_corrections 逐條修正，尤其第 16 行「同 VM 內容器互鎖仍可」與 .vendor_kit/<name>.lock 的鎖檔位置。

## 要問使用者
- 目標平台：macOS Docker Desktop 與 WSL2 /mnt/c 是「明寫不保證互斥、印警告」就好，還是必須支援？若必須，唯一可靠原語是 mkdir（B），代價是殘鎖策略。NFS / SMB / FUSE / 跨主機共用 repo 要不要支援？
- 鎖要不要保護主機端 wrapper 的執行？（另一個 shell 在 just build 跑到一半時 .<name>/ 被換掉）三個層級選一個：(a) 接受空窗、寫進限制；(b) 目錄任何瞬間都完整 → RENAME_EXCHANGE；(c) 同一次任務跨檔案都是同版本 → 不可變版本目錄 + 版本固定，需確認 base 路徑契約、Dockerfile COPY、Compose 是否依賴實體 .base/。
- 鎖不支援時：預設失敗 + VENDOR_KIT_NO_LOCK=1 逃生口（建議），還是照 Cargo 警告後放行？
- 等待逾時預設 60 或 120 秒？Jetson 上 base dist 整批複製實測要多久？CI 是否固定用 0（立即失敗）？
- 同一 repo 允許不同版本的 install 重疊嗎？A 執行中 .version 被改成 v2，A 是照原快照裝完 v1、還是取消？（影響「後到者重讀印記」的規則）
- 多工具（base、harness）共用一把專案級鎖可以嗎？有沒有「同時 install 兩個工具」的計畫？每次 install 重寫 tools.just 的行為要不要保留？
- 中斷保證到哪一層：只要 SIGKILL 後下一次能修好、任何瞬間都完整、還是含主機斷電（要定義 fsync 順序）？
- docker run 要不要加 --init？（影響殘留 .<name>.tmp.* 的數量，與鎖本身無關）
- verify 取共享鎖後發現印記已不是 .version 的版本（另一 shell 剛升級）：回報「請重跑 just」還是就地改成 install？