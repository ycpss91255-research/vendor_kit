討論 #6：本地開發模式 ── 改工具本身時，怎麼在專案裡立刻試，不用每改一行就 build + push image
前例（agy，14 個工具）：本地路徑一律放在「不進 git 的覆蓋檔」或 CLI 旗標，不改正式版本檔 —— Go 的 go.work（提案明寫「不應 check in」）、docker compose 的 compose.override.yaml、mise.local.toml、Cargo 的 .cargo/config.toml [patch]、Terraform 的 dev_overrides（放 CLI 設定檔，不放 .tf）。
本地路徑的東西一律不做 checksum（go.sum、Cargo.lock、pnpm lockfile 都不記），改成每次執行印醒目警告（Terraform：「Provider development overrides are in effect」）。
<b>A：.version 直接寫 path:../tool</b>
優：只有一個檔。
缺：git diff 被污染、容易誤 commit、CI 要另外擋；前例一致反對（Go 因此才做 go.work）。
<b>B：.version.local 覆蓋（gitignore）</b>
優：git 乾淨、零誤 commit；跟 go.work / compose.override 同一型。
缺：多一個檔要知道它存在。
<b>C：只用環境變數／指令旗標</b>
優：完全暫時，關掉 shell 就沒了。
缺：每個 shell 都要設，CI 與同事看不到你在用本地版。
<b>D（agy 建議）：B + C</b>
優先序：環境變數 > .version.local > .version。
平常用 B；臨時單次用 C。
再給兩個指令：just dev <name> <path>、just undev <name>。
方案 D 的流程
just dev <name> ../tool
寫 .version.local：
<name> = "path:../tool"
啟動器讀版本：環境變數 >
.version.local > .version
docker run vendor_kit:vN
-v ../tool/dist:/dist:ro --dev install
.<name>/（印記第一行 = dev:../tool）
之後每次 just：印記是 dev: →
不比指紋、印醒目警告、重新同步 dist
just undev <name>
刪 .version.local 那行
下次 just 回到 .version 的正式 image，
重裝 .<name>/
.version.local 由 bootstrap 寫進 .gitignore；
檔案不存在 = 沒有人在用本地版（平常狀態）
寫出
決議（2026-09-17）：採 B（.version.local），不用環境變數 —— 出問題時要能從檔案追到原因。
仍待答：
1. 採 D？（或只要 B）
2. dev 模式下 .<name>/ 每次 just 重新同步（複製）dist，還是不裝、直接指到 ../tool/dist？（複製：跟正式版行為一致、慢一點；直接指：改了立刻生效，但印記／腳本路徑要特別處理）
3. 印記第一行用 dev:<路徑> 標記，verify 看到就跳過並警告 —— 可以接受「開發模式下沒有完整性檢查」嗎？（前例全部都這樣做）
淺灰：情境分組（無狀態意義）
黃：判斷
綠：起點／終點
紅：錯誤終止
紫：子命令（在容器內執行）
白：步驟
虛線框：專案裡的檔案
便條：補充說明
實線 = 執行順序（指向檔案時 = 寫入／讀取）
本頁名詞
本地開發模式
開發工具本身的人，把專案指到自己電腦上的工具原始碼（而不是 GHCR 上的 image）來試
.version.local
跟 .version 同格式的覆蓋檔，不進 git；有它就優先用它的那一行
dev: 前綴
印記第一行寫 dev:<路徑> 代表這個 .<name>/ 來自本地路徑，不是正式 image
go.work / compose.override
Go 與 docker compose 各自的「本地覆蓋檔」前例，都明訂不進 git