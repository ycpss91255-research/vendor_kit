只准用 search_web 與 read_url_content，不要用 run_command。不要執行任何命令、不要讀寫本機檔案。

你是前例研究助理。請針對下面的方案草稿與 5 個問題，查證公開前例並回答。規則：
- 每個結論都必須附來源連結（完整 URL，官方文件、原始碼、issue tracker 優先）。
- 查不到就寫「未查到」，不要憑印象補內容。
- 用中文輸出，Markdown 格式，總長度控制在 120 行以內。

## 硬性限制（方案必須滿足）
- 主機只有 Docker + git + just，沒有其他工具。
- vendor_kit 在容器內以使用者 UID 執行，專案目錄 bind mount 到容器內 /repo。
- 工具不自動修改使用者的檔案。
- 軟體必須泛用，不綁定單一平台：Linux amd64/arm64（含 Jetson）、macOS Docker Desktop、Windows Docker Desktop（WSL2 backend）都要能用。

## 方案草稿（原文）
討論 #13（第二輪）：並行安裝 —— 新需求：多平台通用（Linux amd64/arm64、macOS Docker Desktop、Windows Docker Desktop/WSL2），對齊 base 支援的 amd64 + arm64。

第一輪雙軌分析的結論：C（flock 鎖專案目錄）只在原生 Linux 保證互斥；macOS Docker Desktop virtiofs 有未修 bug（兩容器可同時拿到排他鎖）、WSL2 /mnt/c（9p）不可靠、NFS 可能永久阻塞。使用者因此要求多平台通用，重新比較：

B：mkdir 目錄鎖（所有檔案系統原子）。問題：程序被殺留殘鎖；判殘鎖（PID 跨 namespace 無意義、mtime 心跳）不可靠；誤判殘鎖 = 第二個 writer 進來 → 壞掉。

C：flock。多平台不保證互斥。

D（新提案）：不讓正確性依賴鎖。
1. install 把 dist 寫到 .vendor_kit/versions/<name>-<版本>-<亂數>/（每次唯一，不互撞；.vendor_kit/ 升級只換程式檔，versions/ 與 baseline/ 是持久狀態不動）。
2. 寫完後把 `.<name>` 這個 symlink 用 rename(新 symlink → .<name>) 一次切換：所有檔案系統原子；讀者永遠看到完整的舊版或完整的新版；兩個 install 交錯最多「後者贏」。
3. 舊版目錄由下一次 install 清（只留目前指向的 + 上一份）。
4. mkdir .vendor_kit/lock/<name> 當「租約」只用來省工：第二個人等一下、看到已裝好就跳過；租約有心跳與過期；過期誤判的後果只是重工，不是壞掉。
5. Linux 上額外拿 flock（有就用、沒有就算）。
代價：.<name>/ 變成 symlink（wrapper 腳本、docker compose 相對路徑、Dockerfile COPY 要確認能跟隨；bind mount 進容器後 symlink 指向 /repo 內相對路徑要用相對 symlink）；第一次從舊專案（真目錄 .base/）遷移要先 rmtree，那一次仍有空窗；多一層 versions/ 要 GC；verify 走訪要處理 symlink（第 #12 決議禁止 dist 內 symlink，但 .<name> 本身是 symlink 是例外）。

多架構相關：base 支援 amd64 + arm64（Jetson）；.version 鎖的是 multi-arch index digest；RENAME_EXCHANGE 系統呼叫號依架構不同（x86_64=316、aarch64=276）且 Alpine/musl 無 wrapper → D 不需要它是優點。

要回答：
1. D 在 macOS Docker Desktop（virtiofs、gRPC-FUSE）、Windows Docker Desktop（WSL2 backend；repo 在 WSL ext4 vs /mnt/c）、Linux amd64/arm64 上，symlink rename 的原子性與 bind mount 內 symlink 跟隨是否都成立？Windows 端若用 Git for Windows 開專案，.<name> symlink 會不會出問題（core.symlinks、開發者模式）？
2. D 的租約鎖：心跳與過期怎麼設計才不會誤傷慢機器（Jetson）；過期誤判時 D 是否真的只是重工。
3. 第一次遷移（真目錄 → symlink）的空窗怎麼處理。
4. GC 舊版目錄：什麼時候可以安全刪除（有人正在用舊版目錄？）。
5. 比較 B / C / D，在「多平台 + amd64/arm64」下給建議；或提出 E。

## 請特別查證的前例（每項附連結）

### A. 「版本目錄 + symlink 原子切換」前例
對以下每個工具，分別說明：(1) 怎麼切換（是否用 rename 覆蓋 symlink、是否先建臨時 symlink 再 rename）、(2) 怎麼 GC 舊版（保留幾份、何時刪）、(3) 切換時正在使用舊版的程序怎麼處理：
- asdf / mise 的 shims 與 installs 目錄
- Capistrano 的 releases/ + current symlink（keep_releases、deploy:cleanup）
- Nix profiles（generation + profile symlink、nix-collect-garbage、GC roots）
- Homebrew 的 Cellar + opt symlink
- Kubernetes ConfigMap/Secret volume 的 ..data symlink 原子更新（AtomicWriter，pkg/volume/util/atomic_writer.go）
- systemd / OSTree 的 deployment symlink（ostree deploy、/ostree/boot.1）

### C. mkdir 租約鎖的前例
- proper-lockfile（npm）：如何用 mkdir 建鎖、mtime 更新間隔（update）、stale 判定（stale 預設 10 秒）、時鐘偏差如何處理。
- Kubernetes Lease（coordination.k8s.io）與 leader election：leaseDurationSeconds、renewDeadline、retryPeriod 預設值與比例關係、對時鐘偏差的說明。
- etcd lease：TTL、keepalive 間隔、時鐘偏差的處理。
- 結論：心跳間隔與過期時間的比例建議，以及對慢機器（Jetson）的考量。

## 本次只回答上面 A 與 C 兩部分，不用回答草稿的 5 個問題。
