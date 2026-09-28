# verify

## 一致
- A 和 B 的基準都是跟被驗檔同一個使用者可寫的印記，只能防「不小心改到」，防不了「故意改」；改檔案順便改印記就過關。所以本地印記不能當信任根。
- 驗證基準應該來自 `.version` 鎖定的 image（notes §6 原本的主張），而且 verify 本來就在那個工具 image 的容器裡跑（已核對 vendor.just `_vk` 與 Dockerfile.dist），所以「C 要多起容器、要上網」這個成本假設是錯的，草稿傾向 B 的主因不成立。
- B 的 size/mtime stat 快取第一版不要做：同長度改寫＋復原 mtime 就漏抓、mtime 粒度在部分檔案系統是秒級、要多兩條驗證路徑；而且速度收益還沒量過。
- 檢查範圍要比 A 寬：檔案集合（缺檔、多餘檔都算失敗）＋內容 sha256＋執行位＋檔案型別／symlink；不比 mtime、owner。
- 多餘檔應該中止而不是警告：理由是 `.<name>/` 是工具整批替換的目錄（下次升級會無聲刪掉），以及「警告不可強制、中止才可以」；不是安全理由。前提是工具執行期不能往 `.<name>/` 寫 log／cache。
- 印記不需要簽章：私鑰只能放在 image 或使用者機器上，等於沒簽。讓基準來自 image 就解除印記的信任責任。
- agy 的前例表不可信：Go、Terraform、pip 三列都查出寫反或把規格當實作，引用編號錯置，效能數字沒來源，Composer 段還被 timeout 截斷；未查證的列只能當線索。
- 原型的 `rglob` + `is_file()` 會跟隨 symlink，A/B 都沒處理 symlink（讀到樹外、DoS）；walk 要改用 lstat。
- 0.5 秒閘門目前只塞 200 個 1–3 byte 的檔、又是 CI wall-clock，量不到真實工作量；要固定「檔數＋總 MB」並分開量「容器內函式」和「含 docker run 的端到端」。

## 分歧（含判斷）
- C 的基準用什麼：直接逐檔讀 /dist，還是建置時預先產生一份清單（manifest）：第一版採 Claude 的做法。清單多一個「清單和 /dist 會不會不一致」的問題要另外驗，等於多一層基準；而 /dist 本身已經是不可寫、digest 鎖定的，直接讀它最短。目前規模下 2×hash 只多 20 ms。等 dist 上百 MB 再考慮清單或 stat 快取。
- 印記要不要也拿來比對（印記 vs image）：兩者其實不衝突但 codex 多此一舉：基準是 image 時，改檔案本身就會被 /dist 比對抓到，印記改不改都沒差。印記只需要驗第一行（決定要不要重裝），其餘 hash 行留著給人追溯即可。不過我同意 codex 一點：印記格式不合法（缺第一行、有 `..`、絕對路徑）要視為「不可讀」走重裝路徑。
- A/B 是否「符合限制」：codex 的判讀比較貼題：#12 就是在決定要不要落實 §6，A/B 等於否決 §6。但這不影響結論，兩邊都選 C。
- 執行權限比到哪一位：採 Claude：只比「該 +x 的有沒有 +x」（單向，跟 Nix NAR 一樣只記 executable 一個 bit）。完整 mode 在 macOS／Windows 掛載上會誤報，而 umask 也會讓 0644/0755 正規化失效。特殊位（setuid/setgid/sticky）一律拒絕這點採 codex。
- symlink 政策：先看 dist 裡到底有沒有 symlink（問使用者）。沒有就採 codex 直接禁止（install 拒絕、verify 遇到就失敗），最省事；有才採 Claude 的 target 字串比對。無論哪種，walk 都要 lstat 不跟隨。
- 印記第一行的來源與 §10 的 digest 循環：codex 對，已核對 `ARG REF; RUN echo "$REF" > /dist/VERSION` 確實有這個問題。解法現成：`_vk` 已經 `--self "$image"` 把 `.version` 的字串傳進容器，印記第一行直接用它，/dist/VERSION 只留 tag 或 base commit 當人看的資訊。Claude 的「斷言 == /dist/VERSION」要改成「== --self」。

## 對前例資料的更正
- Go：`go mod verify` 比的是 module cache 裡的 `.ziphash` 和解壓目錄，不是 go.sum 也不查 checksum database；它的基準跟我們的印記一樣是本地可寫檔。
- Terraform：plan／apply 每次都會用 lockfile 的 h1 對快取的 provider 目錄重算比對（`providerFactoriesFromLocks` → `MatchesAnyHash`），不是「只有 init 驗」。這反而是最貼近本案的前例（鎖檔進 git、本地目錄每次重 hash），agy 歸類寫反了。
- pip：不驗 RECORD 的 hash（PEP 815 明講 pip／uv 都沒實作），`pip check` 只查依賴相容，跟完整性無關。
- pnpm：`verify-store-integrity` 先看 mtime 是否晚於 checkedAt 才比 size、再算 hash；原始碼註解明寫「不能讓被不受信任使用者可寫的 store 變安全」，不能拿來支持本地印記當防線。
- Git：不只 size/mtime，還有 ctime、inode、型別與 racy-git 特例，草稿的 stat 快取不是完整 Git 機制。
- Nix：NAR 只記目錄結構、內容、symlink target、executable 一個 bit，不含完整 mode／owner／mtime；「唯讀 store」靠 root 擁有，不能套用到使用者自己擁有的目錄；`nix store verify` 的旗標是 `--no-contents`，`--check-contents` 是舊 CLI 的；「未註冊頂層目錄視為 dead 回收」在引用文件裡找不到。
- 方案 C：不需要多起容器、不需要上網、不需要解包——verify 本來就在含 /dist 的工具 image 內跑，image 在 §4 第 2 步已依 digest pull 好。實測 200 檔 6.4 MB 雙邊 hash 42 ms，docker run 本身 250 ms。
- 簽章（cosign／minisign）保護印記：私鑰無處可放，簽了等於沒簽；cosign 正確用途是 pull 時驗 image，另立決議。
- 「多餘檔可能是劫持的 wrapper」的安全論述：能塞檔的人也能改印記，安全理由不成立；多餘檔中止的理由是營運（升級整批替換）。
- 效能數字（SHA-256 1.5–3 GB/s、stat 0.5–2 µs、快 100–1000 倍）沒來源也沒基準；實測瓶頸在容器啟動不在 hash。
- 「沒有人每次執行都從來源重取」是全稱斷言，只能說「未找到相同前例」；Terraform 其實就是。
- Bazel／Composer／npm／Homebrew／Cargo／pre-commit 各列：輸出被 timeout 截斷、引用編號錯置（rpm 標 [2][3] 但 3 是 Nix；pre-commit 標 [23] 但 23 是 pip check），列為未查證。

## 最終建議
採 C（基準 = 鎖定 image 內的 /dist），第一版不做 stat 快取、不做清單檔。具體：（1）基準：verify 在該工具自己的 image 容器內跑（現況 `_vk` 已如此），直接對 `/dist/files` 與 bind mount 的 `.<name>/` 做「兩棵樹 diff」，同一個函式給 install（決定寫什麼）、verify（報錯清單）、release-test 用；`cli.verify` 直接用已傳入的 `d`。（2）比對範圍：檔案集合（缺檔、多餘檔皆失敗，只豁免 `.stamp` 這一個路徑）＋內容 sha256＋執行位（只比 0o111 任一位、單向）＋檔案型別（lstat 不跟隨；symlink 若 dist 沒用到就直接禁止，有用到才比 target 字串；拒絕 setuid/setgid/sticky、FIFO、`..`、絕對路徑）；不比 mtime、owner、完整 mode。（3）印記：維持現格式（第 1 行版本、之後 `sha256  path`），第 1 行改用 launcher `--self` 傳入的 `.version` 字串（解掉 Dockerfile.dist 把 digest 寫進自身的循環），只當「已裝版本」快取鍵＋給人追溯，不簽章、不再拿裡面的 hash 當基準；格式不合法視為不可讀走重裝。（4）`.vendor_kit/` 特例：它的 image 是 vendor_kit 本體、沒有 /dist，基準改為「用 image 內 launcher.py 重新 render vendor.just／tools.just 再比」；並在 notes 明寫它是「.<name>/ 不進 git」的例外。（5）失敗處置：維持中止並提示手動刪除重裝，不自動重裝（會無聲毀掉手改）。（6）閘門：release-test 加「跑 wrapper smoke → verify 仍過」強制工具不往 `.<name>/` 寫執行期產物；功能測試涵蓋同長度改寫、竄改印記、增刪檔、chmod、symlink 替換；效能閘門改成固定「200 檔＋固定總 MB」，容器內函式與含 docker run 的端到端分開量。（7）日後 dist 上百 MB 再把印記升級成 git index 式 stat 快取疊在 C 上（image=object store、`.<name>/`=worktree、印記=index），現在做是過早最佳化。

## 要問使用者
- 威脅模型要防到哪層：只防誤改／殘留檔，還是也要防同一使用者蓄意改？（C 兩者都涵蓋；若還要防改 launcher／.version 或執行期競態，需要不同的權限架構，超出 #12。）
- 有沒有任何 wrapper／runtime 會在執行期往 `.<name>/` 寫東西（log、`__pycache__`、快取、產生的 compose）？若有，「多餘檔＝失敗」要先把這些輸出搬走或訂允許清單。
- dist 目前或未來會不會含 symlink、空目錄？沒有就第一版直接禁止 symlink、不追蹤空目錄。
- 支援的主機平台：Docker Desktop（macOS、Windows drvfs）、rootless／userns-remap 在不在範圍？在的話執行位只能單向比，且要明寫支援範圍。
- 多架構：`.version` 鎖 index digest 時，各架構的 dist 內容是否保證一致？若不一致，換平台後 verify 會要求重裝，可接受嗎？
- dist 的規模上限（檔數、總 MB）大概多少？這決定閘門的固定總大小，也決定何時才值得加 stat 快取。
- 0.5 秒從哪裡起算：容器內 verify 函式、單個 docker run、還是整個 `just` 的 `_ensure`（N 個工具各起一次容器，每次約 250 ms）？後者 2 個工具就超標，跟 hash 無關。
- 「每次 just 都驗」是驗當次用到的工具還是 `.version` 裡全部？要不要正式保留 §4「剛安裝後跳過 verify」的例外？
- verify 失敗時維持「中止＋提示手動刪除重裝」（我建議）還是允許自動重裝？
- 要不要把 `_ensure` 的「第一行 ≠ .version → install，否則 verify」判斷從 shell 搬進容器（一個 `ensure` 子命令）？C 之後容器內三者都有，可以縮小 shell 面積。
- `.vendor_kit/` 進 git但名稱符合 `.<name>/` 樣式，要不要在 notes 明寫成例外並定義它的 verify 基準（image 內 launcher.py 重新 render）？