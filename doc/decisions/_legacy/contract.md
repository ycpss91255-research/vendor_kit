# contract

## 一致
- 兩邊都認定草稿「單一 LABEL 版本、不相等即拒絕」不能採用：改 `.version` 的 vendor_kit 行只換啟動器，工具 image 內嵌的引擎要等工具重發才會動，所以「新啟動器 × 舊引擎」是常態不是例外，只支援相等等於每次 bump 全下游同時紅。
- 相容條件要看「能力集合／協定」而不是 release 版號相等；協定號要和 vendor_kit 的 release 版號分開。
- 要有明確的支援視窗，而且「退出舊協定支援」本身就是破壞性變更，必須提前公告，不能用「協定沒改」帶過。
- 兩個方向都要測：舊啟動器 × 新引擎（bootstrap 那一次永遠是這個方向）、新啟動器 × 舊引擎（工具 image 沒重建），還有一個專案內多個工具各嵌不同引擎版本。
- bootstrap 那條 docker run 要永久凍結，且要凍結完整呼叫方式（子命令、必要 mount、預設值、可寫範圍），不只凍結名字。
- `ensure` 是工具 recipe 要呼叫的整合 API，必須公開且凍結，原型用底線私有命名是錯的。
- baseline 是持久資料，不能和可重建的印記／.vendor_kit/ 用同一套「刪掉重建」處理；需要自己的 schema／format 欄位與遷移政策。
- 檢查責任要分層：啟動器用 `docker image inspect --format` 讀 LABEL 做前置檢查（主機不需 jq）、引擎在容器內做權威判定、發布 CI 驗證宣告屬實；而且要對「這次真正要跑的工具 image」查，不是只查 .version 的 vendor_kit image。
- 相容矩陣必須用真實的舊啟動器與舊 image，不能用新程式模擬舊版本；矩陣是「每工具」不是「每專案」。
- agy 的「刷新 recipe 後自動用新 recipe 接續原任務」不成立：just 已把 `_ensure` 內文讀進記憶體，後續子行程卻讀到新檔，會新舊混用；正確做法是中止並要求重跑（Gradle 跑兩次的前例正好對應）。
- agy 的「改回 .version 就能完整 rollback」只對可重建的目錄成立，baseline、使用者設定、啟動器產物不會跟著退。
- agy 的 Renovate 段落有缺口：Claude 指出 Mend 託管版不能跑 postUpgradeTasks（.vendor_kit/ 不會在 PR 內再生成）、codex 指出範例 regex 的 ^ 不是每行開頭（抓不到 [tools] 後面的行）；兩點互補，都要修。
- agy 引用的 `.installed_version`、`.<name>/template/`、頂層 `just init` 都不是目前定案的介面，不能照抄進第 11／12 頁。
- 「新增能力只走環境變數或檔案」不能當硬規則，至少不能單獨成立。

## 分歧（含判斷）
- 協定號的形狀：單一整數 + 下限，還是 major/minor + 能力清單？：採 Claude 的單一整數 + floor。兩者語意其實一樣（minor＝P+1、major＝floor 上移），但整數版本比較少東西要解析（啟動器是 bash-in-just，越少邏輯越好），而且「floor」比「固定兩個 major」誠實：真正的支援範圍取決於工具多久沒重建，這是成本選擇，不該預設固定 N-1。codex 的規則「退出舊協定本身就是破壞性變更，要在啟動器下一個 release major 才能做」直接併進 floor 的治理。
- 引擎端握手要不要每次呼叫都送 `--protocol N`？：兩者相容，合起來用：LABEL 預檢（快、可讀、upgrade 前判斷）＋ 引擎收 `--protocol` 並在任何寫入之前判定（權威）＋ 發布 CI 驗證 LABEL 與引擎宣告一致。關鍵是 `--protocol` 必須從第一版就存在，否則舊引擎碰到它會 argparse exit 2，訊息不友善。
- 新增能力是否優先走環境變數？：codex 對。有了 per-verb 最低 P 表與 `--protocol` 握手後，新能力就直接走旗標／verb，被協定閘門擋下會有明確訊息；環境變數只留給「引擎不認得也無害」的東西（例如 log 等級）。啟動器轉發 `VENDOR_KIT_*` 仍值得做，但不是相容策略的支柱。
- init.toml 要不要進執行期相容矩陣？：採 Claude 的簡化，但保留 codex 的 `schema` 欄位。只要「讀 init.toml 的永遠是同一個 image 裡的引擎」這條成立，它就不會進執行期矩陣；要在契約④ 明寫這條前提，並在 tool repo 的 release-test 驗證。若日後有跨 image 讀 init.toml 的需求，再升級成 codex 的做法。
- baseline 降級怎麼處理？：Claude 的做法可行且省掉一整類反向相容程式碼，但它是使用者要接受的規則（降級＝revert 整個 commit，含 .version、.vendor_kit/、baseline/），不是技術上唯一解。建議先問使用者；若不接受，就採 codex 的「新引擎在過渡期只寫舊引擎讀得懂的 format」。
- 測試 runner 能不能在 CI 主機直接跑 pytest？：codex 對，而且和 Claude 自己提的「主機只保證有 docker CLI」一致。矩陣測試的驅動程式應該在容器裡跑，主機只負責 docker/just。
- exit code 要不要在本題重新編號？：兩邊都對：本題只「保留」一個專用碼給協定不合（不動 diff 的 0/1/2），完整的 exit code 表留給 #11／#23。啟動器把「未知子命令」的 exit 2 翻譯成友善訊息是啟動器層的事，可做。
- agy「先換自己」結論怎麼評價？：折衷：順序本身仍該是「先換啟動器」（新啟動器才知道要查什麼），但 agy 給的理由是錯的，而且這個順序只是必要不充分——真正的保證來自協定視窗。寫進定案時用 codex 的表述當理由。
- /dist 佈局要不要進契約②？：不衝突：佈局要有唯一版本（codex），但寫在契約④ 而不是②（Claude）。第 12 頁要改成引用④，不要重複描述。
- Gradle 前例的效力：兩邊都對一半：Gradle 證明「跑兩次」是業界可接受的使用者體驗，不證明我們的 bootstrap 已相容。當設計靈感引用即可，不當相容性論據。

## 對前例資料的更正
- Batect 已於 2023-10 停止維護（官方首頁公告），不宜當主要前例；引用的錨點也未查證。（僅 Claude 提出，建議在定稿前再開一次 batect.dev 確認。）
- rustup 沒有「先 self update 再 update 是官方標準指引」這回事；原始碼是 update 內部先跑 update_all_channels 再 self_update。這是 agy 的推論不是文件。
- 「刷新 recipe 後自動以新 recipe 接續原任務」在 just 裡不成立（內文已載入，子行程讀到新檔會混用），必須中止並要求重跑。
- `.installed_version`、`.<name>/template/`、頂層 `just init` 都是 agy 自創或舊介面，與已定案的 `.<name>/.stamp`（第一行＝--self）衝突。
- 「啟動器透過 Docker／遠端 API 查 GHCR 最新 tag」不可行：主機只有 docker CLI，沒有列 tag 指令；查 registry 應在容器內由 Python 做。
- Renovate：(a) Mend 託管版不能跑 postUpgradeTasks／allowedCommands，改了 .version 後 .vendor_kit/ 不會在 PR 內再生成；(b) 範例 regex 用 ^ 當每行開頭是錯的（Renovate 以整檔匹配），要用 (?m) 或處理換行；(c) autoReplaceStringTemplate 不是「必須」；(d) PR body 會附 Release Notes 是條件性的，不能當我方契約。
- Dependabot 現在分列 docker 與 docker-compose；可靠結論只有「標準設定沒有任意 TOML 的 regex manager」。
- 「因為啟動器由 image 產生所以必須先換自己」推論不成立；且先換自己不足以保證相容（工具 image 內嵌引擎不會跟著更新）。
- 「改回 .version 就能完整 rollback」只對可重建目錄成立；baseline、使用者設定、啟動器產物不會跟著退。
- 「延遲安裝就是安全審查」只審到版本宣告，image 程式仍會執行；要承諾的是各命令的寫入範圍。
- agy 前後不一致：前面說 upgrade 只改檔，後面手動路徑卻立即 install；後者較接近決策紀錄。
- Batect／rustup／uv 前例不能證明「某種順序絕不會傳舊參數」，只能輔助理解。
- 整份報告主題是升級流程，對 #14 真正要的「協定版本範圍、支援幾個舊協定、誰檢查、相容矩陣」沒有前例；可補的現成前例：Docker Engine API 版本協商＋最低 API 版本、Kubernetes version skew、Terraform provider protocol 5/6 並存、Cargo lockfile version、pre-commit minimum_pre_commit_version、just `set minimum-version`。
- Gradle 兩階段、Bazelisk／Nix／Terraform 回退行為、Dependabot 做不到——這幾條查證後正確，但只涵蓋升級順序不涵蓋契約。

## 最終建議
採 Claude 的方案 D 為骨架，用 codex 的「各契約分開治理」補齊，不採草稿的單一 LABEL 相等判定。定案內容：

1. 線協定（契約②）＝單一整數 P，語意是「功能等級」不是大版。image LABEL `io.vendor_kit.protocol` 由 FROM 自動繼承；啟動器每次呼叫都送 `--protocol P`（從第一版就有）。引擎接受 [floor, current]；新增 verb／旗標／exit code 語意／印記第一行語意 → P+1；floor 上移＝破壞性變更，必須提前一個 minor 公告、同步升 vendor_kit 大版、並維護舊 P 的 base image 線一段時間讓 tool repo 重建（多久要問使用者）。新引擎在過渡期也要接受舊啟動器的 P（因為工具 image 可能先於啟動器更新）。

2. bootstrap 那條 docker run 永久凍結且縮到最小（引擎自己讀 /repo/.version），凍結的是完整呼叫方式：子命令、必要 mount、預設值、可寫範圍。它在 P 之外，不受視窗影響。再 bootstrap 之後 `ensure` 必須中止並要求重跑，不自動接續。

3. 誰檢查、三層：啟動器對「這次真正要跑的工具 image」用 `docker image inspect --format` 讀 LABEL，配 per-verb 最低 P 表做前置檢查 → 引擎收 `--protocol` 在任何寫入之前做權威判定 → 發布 CI 驗證 LABEL 與引擎宣告一致，並跑相容矩陣。失敗分類：無共同協定→寫入前拒絕、印出雙方範圍與該動哪一行；LABEL 缺失→拒絕（除非列冊 legacy）；網路失敗不偽裝成協定不合；未知印記→視為不可信快取重建；未知 baseline format→中止並保留資料；舊啟動器無法自更新→給 digest 鎖定的 bootstrap 救援指令。協定不合保留一個專用 exit code，不動 diff 的 0/1/2，完整表留給 #11／#23。

4. 各契約分開：`.version` 那一行的 regex 是啟動器、引擎、Renovate preset 的單一來源，啟動器忽略不認得的行；印記只有第一行是契約；init.toml 是建置期契約（同 image 內讀寫），加 `schema` 欄位、大版治理，不進執行期矩陣；baseline 加 `format`，新引擎讀所有出過的 format，降級走 git revert 整個升級 commit（此規則要使用者確認，否則改為過渡期只寫舊 format）；公開 recipe/CLI 走 release semver，公開集合＝`vendor_kit` 命名空間內非底線非 `[private]`，`ensure` 必須公開，移除只在大版且前一 minor 先 alias+警告；新增能力走旗標／verb 由協定閘門擋，不以環境變數當硬規則。tools.just 與共用 metadata 統一由 .version 鎖定的 vendor_kit 引擎寫，工具內嵌引擎不寫。

5. 五個契約補三處：① 主機最低版本（just ≥1.31、docker/compose v2、Linux amd64/arm64、rootless／遠端 daemon 不支援聲明）；③ 根 justfile 那一行（`mod?` vs `import` 先定）與 `.version` 行 regex；⑤ runner 前提（daemon 與 checkout 同檔案系統，否則提供 docker cp 路徑）。不承諾：② 裡的 /dist 佈局（唯一版本寫在④）、docker run 旗標細節、印記第二行以後、tools.just 內容、`just upgrade`／`dev`／`undev` 的形式。

6. 相容矩陣（發布 CI，測試驅動程式容器化，amd64 全跑、arm64 一格 smoke）：L(cur)×E(floor..cur) 五個 verb；L(floor..cur-1)×E(cur) 重點在 ensure→bootstrap 自我升級；新 L × 一個專案內多工具混合 E；E(cur) 讀 E(floor..cur-1) 寫的 baseline／印記；只回退工具行、只回退 vendor_kit 行、git revert 整個 commit；超出視窗／LABEL 缺失／未知 format；fresh clone／啟動器缺失／冷快取；just 最低版×最新版。樣本＝每 release 提交 golden 啟動器到 test/compat/launchers/<P>/ 並發布 `vendor_kit-fixture-dist:<tag>`，registry 保留規則列為不可刪。GitHub／GitLab 各跑一條真實整合路徑，共用測試核心。

## 要問使用者
- 「工具 image FROM vendor_kit」是不可談的硬限制，還是原型的方便？若可談，方案 E（純資料 image）能把矩陣砍成一維；若不可談，是否接受「工具一次 release 就把該專案的協定上限釘住，直到工具重發」？
- 契約② 的 argv 到底是哪一套：原型的五個子命令（install/init/verify/diff/bootstrap，無旗標），還是 brief 語料裡 ADR-00000013/17/20 的介面（-q/-v、--json、--porcelain=v1、exit 10/11/100）？brief 的四個 frozen entry-point paths 與這些舊承諾是否仍有效，需要一張新舊對照表。
- floor（最舊支援協定）的視窗怎麼定：用「一個 minor」還是「6 個月」計？vendor_kit 是否承諾維護舊 P 的 base image 線給 tool repo 重建、多久？誰負責在視窗關閉前重建工具（目前 14 個 repo 停在 v0.41 的實況）？
- 降級規則「只能 git revert 整個升級 commit（含 .version、.vendor_kit/、baseline/）」接不接受？若不接受，就要引擎在過渡期只寫舊 format，成本較高。`accept` 是否負責把舊 format 的 baseline 遷移到新 format？
- 主機最低版本承諾到哪：just 以 1.31（模組穩定）為底？要不要用 1.55 才有的 `set minimum-version`？docker 最低版（Jetson JetPack 5 的 20.10 要不要支援）？rootless／userns-remap／遠端 daemon 明寫不支援？Compose／Buildx plugin 要不要算在基線裡？
- Renovate 改了 .version 的 vendor_kit 行後，.vendor_kit/ 再生成在哪裡發生：PR CI 直接紅並要求人跑 `just` 再推，還是 CI bot 自動 commit？普通工具命令自動更新 .vendor_kit/ 是否允許弄髒工作樹？
- 根 justfile 那一行凍結成 `mod? vendor_kit '.vendor_kit/vendor.just'` 還是 `import`？（原型與 notes §11 不一致，而這一行寫出後歸使用者、永不再由工具改。）
- 協定不合的專用 exit code 要幾號？啟動器要不要把引擎的 exit 2（未知子命令）翻譯成「工具太舊」訊息？
- /dist 的唯一 canonical layout 是哪一個？第 12 頁寫 files/、init.toml、VERSION，決策紀錄另寫 init.toml 與 dist 並列、/dist/VERSION 只供辨識，要選一個寫進契約④。
- 契約⑤ 的 check.sh 是否承諾在 GitLab docker:dind 與 GitHub container job 裡可用（bind mount 路徑問題），還是只承諾 shell executor／plain runner？GitLab 端的 just 從哪裡來？
- 每個 release 是否提交 golden 啟動器到 test/compat/ 並發布 `vendor_kit-fixture-dist:<tag>`？registry 保留規則（§5）要不要把 fixture image 列為不可刪？