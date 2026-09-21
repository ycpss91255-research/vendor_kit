方案 A（目前草案）：bootstrap.sh + upgrade + dev；接第二個工具 = 再跑 bootstrap.sh 或手動加 .version 一行，ensure 第一次自動 init；沒有 remove/undev/add/init。
方案 B（成對、對齊 base）：bootstrap.sh 只做第一次；之後 `just vendor_kit add <repo> [--tag]` ↔ `remove <repo> [--purge]`；`update`（只查）↔ `upgrade [<repo>] [--tag]`；`dev <repo> -p <dir>` ↔ `undev <repo>`；`init`（修復：同步專案到 .version 狀態、補初始檔）；`uninstall`（把 vendor_kit 從專案拔掉）。ensure 只碰不進 git 的東西（.<repo>/、gen/），絕不寫初始檔／baseline。`just vendor_kit` 列表分「常用：add upgrade dev」「進階：remove undev update init uninstall」。
方案 C（折衷）：B 的成對動詞，但 init 拿掉（修復交給 ensure + add 冪等：`add <repo>` 對已存在的工具 = 補初始檔、warn 不覆蓋）；bootstrap.sh 支援非互動參數並在偵測到 .version 時改用該版引擎（即 bootstrap.sh 第二次跑 = add）。
我方傾向：C（或 B），關鍵理由是疑點 1（ensure 自動 init 在 CI 會生出沒 commit 的檔）。請獨立判斷傾向是否站得住。
