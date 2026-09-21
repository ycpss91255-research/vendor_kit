第 11 頁「流程：升級與回退」初版文字（四條路徑 A/B/C/D 與待決便條）：
流程：升級與回退 ── 四條路徑（初版，待決處以便條標示）
Renovate 機器人（GitHub 上）
啟動器（.vendor_kit/，在主機）
vendor_kit 容器
A. 自動：Renovate 發現 GHCR 有新版（正常情況走這條）
起點：GHCR 出現
<name>-dist 新 tag
開 PR：改 .version 那一行
（tag 與 digest 一起換）
CI 在 PR 上跑 just
（install + verify + 工具的煙霧測試）
看 CI 綠、merge PR
每個人下次打 just：
印記第一行 ≠ .version → install
install 新版
.<name>/（新版）
just diff → 跟進 → just accept
（第 5 頁 diff／accept 泳道）
.vendor_kit/baseline/<name>/（更新）
' + EDGE + 'exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;
geometry
merge 後
' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;
geometry
' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;
geometry
' + EDGE + 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;
geometry
待決：CI 在 PR 上要跑到哪一步（只 install+verify，還是連工具的 build 都跑）？Renovate 對 .version（自訂 TOML）用 regex manager，設定由 vendor_kit 出貨還是各專案自寫？
B. 手動：just upgrade <name>（沒有 Renovate、或想馬上升）
just upgrade <name>
起 vendor_kit 容器跑 upgrade 子命令
查 GHCR：<name>-dist 最新 tag + digest
（要網路；只查不裝）
.version 那一行改成新版
接著同 A：印記 ≠ .version → install
just diff → 跟進 → accept
→ commit .version 與修改
' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;
geometry
待決：upgrade 只改 .version 就停（讓使用者自己打 just 觸發 install），還是一路做到 install + diff？「查最新版」要在容器內用什麼查 GHCR（registry API）？要不要 --dry-run（只印不改）？
C. vendor_kit 自己升級（啟動器 .vendor_kit/ 換新）
.version 的 vendor_kit 那一行改了
（走 A 或 B，跟工具一樣）
下次 just：.vendor_kit/.stamp 第一行
≠ .version 的 vendor_kit 行
用新版 vendor_kit image 跑 bootstrap
只重寫 vendor.just / tools.just / .stamp
.vendor_kit/ 程式檔換新
（baseline/、justfile、.version 不動）
' + EDGE + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;
geometry
待決（issue #14）：新啟動器會呼叫「工具 image 內建」的舊 vendor_kit，兩者版本會不一樣——參數、印記格式、init.toml 格式跨版本要相容到什麼程度？誰檢查？不相容時是拒絕、還是要求工具重新出 image？
D. 回退（升上去發現壞了）
git revert 那個升級 commit
（.version 那行改回舊版）
下次 just：印記 ≠ .version
→ install 舊版
.<name>/（舊版）
待決：如果已經 just accept 過（baseline 變新版）才回退，git revert 同一個 commit 會把 baseline 一起退回，沒問題；但若 accept 是另一個 commit，就要一起 revert，否則 diff 會反向。要不要讓 accept 強制跟 .version 同一個 commit？
使用者自己改過的初始檔不會自動回復（工具不碰使用者檔）。
Renovate
GitHub 上的機器人：發現 GHCR 有新版就自動開 PR 改 .version；沒有它時用 just upgrade 手動
tag / digest
image 的版本名稱／內容指紋；.version 兩者都記，一起換
PR / merge / revert
GitHub 上的合併請求／接受它／用 git 把某次修改整個倒回去
.<name>/.stamp 第一行 = 裝的是哪個 image；跟 .version 那行不同就重裝（第 3 頁）
上次確認過的範本副本／告訴工具「這版我看完了」（第 5 頁、issue #22）
同第 10 頁的子命令，這裡只重寫 .vendor_kit/ 的程式檔
issue #14
相容性承諾這一題的 GitHub 討論串