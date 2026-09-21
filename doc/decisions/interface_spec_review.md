# 介面規格審查 —— 雙軌（2026-09-19）

## 一致
- §3.1 `--pull never` 在 docker 19.03 不存在（20.10 才加）。兩方都查過來源（PR #1498／19.03.15 vs 20.10.0 的 create.go）。解法一致：不提高最低版本，改用 `docker image inspect` 驗本機 image ID 後直接 run。
- §9 B2 白名單漏了 `VENDOR_KIT_NO_LOCK`；§5 說引擎讀它，不轉發就永遠無效。`VENDOR_KIT_PULL_TIMEOUT`、`TMPDIR` 由啟動器自讀、不轉發。
- `VENDOR_KIT_REGISTRY_TOKEN_FILE` 只用 `-e` 傳主機路徑，容器讀不到；必須 `-v <file>:<容器內路徑>:ro` 並改傳容器內路徑。
- uninstall 在 proposal v2.5-10 已改成 resolve→apply 兩段＋重驗指紋，§3.1「單段」是漏更新。codex 另指出導言的來源優先序根本沒列 v2.5，這是根因。
- resolve 絕不能加 `-t`（docker TTY 會把 stdout/stderr 合流、換行變 CRLF），apply 若要互動就不能拿 stdout 當協定通道；「引擎已變」不該從 apply stdout 讀。
- §9 F1 的「gen/tools.just 加前置 recipe 依賴」不可行：違反「tools.just 零 recipe」定案，且 just 1.33 兄弟模組之間不能相依（Claude 實測 1.33／1.53 皆失敗，codex 引 README）。唯一路徑是工具模組自己用 shell 呼叫 `just vendor_kit sync`，且呼叫前必須 `cd` 回專案根。
- §9 E2 檔案位置與 extends 字串互相矛盾：`github>owner/repo` 只讀根目錄 `default.json`，子目錄要寫 `//renovate/default`。
- C1 `min_reader`：grilling 把「寫入者版本」與「最低讀取版本」混在一起，兩者語意不同；不能只因寫入者較新就拒讀，否則破壞「同 schema／N−1 可讀 N」承諾。
- C3 version.local.toml 與 version.toml 同形（頂層 `vendor_kit`／`vendor_kit_image_id`，工具放 `[tools]`）；undev vendor_kit 要一起撤掉 image ID 欄位；local 檔也要有 schema 與寫入者欄位。
- 結束碼 3 = 版本／協定／schema 不合、需先升級或退回；兩方都傾向此定義，但都要求文字收緊：Claude 加「回 3 時零寫入、新舊以 schema/P 比不用 SemVer」，codex 加「stamp 不符、薄殼被改、自身升級完成等既定回 1 的情境不得因提示含 upgrade 就改 3」。
- vk-resolve 是「執行計畫」不是事實；啟動器要先收完整份、驗結束碼與文法（首行、`end` 計數）再動 docker；整份計畫要原樣掛進 apply 供重驗指紋；指紋無法涵蓋新版新增檔（resolve 時 image 未展開）；`sync` 無待辦的快路徑要明確表達，不起第二個容器。
- prune 由主機（啟動器）執行 docker ls/rm，引擎只產生保留／刪除清單，不掛 docker socket。共享 image 不能只憑 label 一律刪。
- 工具 image 的 label 只能在 build 時加，pull 不能追加；B5 的「專案絕對路徑 label」不能放到 image 上（codex），且工具 Dockerfile.dist 必須自帶 LABEL 才掃得到（Claude）。
- §4.3 metadata 的 declined／managed 等列舉需要整理：Claude 指出兩套列舉重疊，codex 指出所有權與本次互動狀態混在一起、declined 缺內容 hash 無法實作 Q15「新版有更新再問」。
- `--local <tar>` 離線 add 寫哪個 digest 未定（`docker load` 無 RepoDigests、單平台 tar 沒 index digest）；codex 另反對以副檔名猜 tag／tar。
- `bootstrap.sh -t` 指引擎版還是工具版未定；`local_bootstrap.sh`（§7.4-16）規格內未定義。
- regex 不可攜：`\s` 不是 POSIX BRE，`grep -m1` 不驗唯一性；要定義 `vendor_kit =` 行的唯一正規形。
- 啟動器實際用到的主機命令（id、mktemp、git、docker inspect/load/ls/rm、timeout 替代品）超出 §3.1／§5 自稱的白名單，必須明列。

## 分歧與取捨
### C1 min_reader 怎麼修
- Claude：改成資訊欄 `written_by`，讀取門檻只看 `schema`；min_reader 冗餘或與「同 schema 必可讀」矛盾。
- codex：拆成 `written_by` 與 `min_reader` 兩個欄位並存。
- 取捨：採 Claude。既然定案是「同 schema 只加不改、讀時忽略未知欄位」，能不能讀已由 `schema` 決定，`min_reader` 沒有任何情境會與 schema 給出不同答案，留著只會讓實作者多一條判斷、多一個可矛盾的來源。若將來真需要「同 schema 但舊版讀不了」，那就是 schema 該 +1 的訊號。

### vk-resolve/1 格式細節
- Claude：TAB 分隔定位欄位；kind ∈ pull/extract/mount/engine/fingerprint/apply/end/keep；dev 路徑原樣放最後一欄（`IFS=tab read -r` 天然吃到行尾）；`apply yes|no`；自身升級由啟動器 apply 後 grep 第一行前後差異決定是否重跑，不需要 apply 結果檔。
- codex：`|` 分隔；多 request/todo/next 記錄與排序規則；路徑以 hex 編碼；另設 `vk-apply/1` 結果檔（原子改名）回報 status/engine；apply 帶 `--plan /vk/plan`。
- 取捨：骨架取 codex（先收完再驗、計畫原樣掛給 apply、`next done` 快路徑），細節取 Claude。理由：(1) TAB 比 `|` 安全（路徑可含 `|`，但 TAB 極少見且 POSIX `read` 原生支援），hex 編碼路徑在 POSIX sh 沒有現成解碼器，會逼啟動器自寫 sed 迴圈；(2) codex 的 todo／排序規則多數是引擎內部事，啟動器用不到，放進協定只是增加 P+1 的機會；(3) `vk-apply/1` 結果檔是對的方向但可以簡化：啟動器只需 grep version.toml 第一行前後差異就能可靠判斷「第一行已提交」，不必再定一個格式。若之後要區分「第一行改了但重產失敗」，再加結果檔即可。

### F1 工具 recipe 自動 sync 的落點
- Claude：F1-A：工具 `<ns>.just` 內私有 `_sync` recipe（固定體 `cd "{{justfile_directory()}}" && just vendor_kit sync`），公開 recipe 相依它；check.sh --dist 用 `just --dump --dump-format json` lint。
- codex：不接受任一版本就結案：recipe 執行前 just 已解析所有模組，cache 缺檔／語法壞掉時 sync 進不去；sync 重建後外層 just 仍持舊定義；還缺 help/sync/install 等例外集合與 1.33 fixture。
- 取捨：兩方互補，不衝突。Claude 的 A 方案是「已能載入時」的正確做法；codex 指出的「載入期就掛」在我這裡實測屬實（`mod` 指向缺檔時任何 `just` 都 exit 1），但 Claude 的 `mod?` 建議剛好就是解法（實測 `mod?` 缺檔仍能跑其他 recipe）。所以定案應是：gen/tools.just 用 `mod?` ＋ F1-A ＋ 明列例外集合（vendor_kit 自身動詞不前置）。另 codex 對 `cd "{{justfile_directory()}}"` 的注入疑慮成立，改用 `cd "$JD"` 由 recipe 以環境變數或 `{{quote(justfile_directory())}}` 傳。

### B1 `--local` 值的判別
- Claude：存在的檔案路徑 → tar 並 `docker load`，否則視為 tag。
- codex：要明確前綴 `image:`／`tar:`，歧義回 1，不猜。
- 取捨：採 codex 的精神但保留 Claude 的簡潔：規則改成「值含 `/` 或以 `.tar` 結尾 → 路徑，必須存在否則 1；其餘視為 tag；同時滿足兩邊（例如 tag 含 `/` 又存在同名檔）→ 1 並提示用 `./` 或完整 ref 消歧」。前綴語法要使用者拍板，因為它改 proposal/#27 已用的介面。

### B3 pull 逾時 `0` 是否表示無限
- Claude：`0` = 不限。
- codex：不接受 0；只允許正整數。
- 取捨：採 codex。`0` 在 shell 裡與「未設」太容易混淆，且 300 秒已夠寬；要無限就設一個大數。這條是純命名，可直採。

### B6 mktemp 與暫存目錄
- Claude：`mktemp -d "${TMPDIR:-/tmp}/vendor_kit.XXXXXX"`＋trap；備選放 `.vendor_kit/.tmp.dist.<pid>/`。
- codex：mktemp 不在嚴格白名單內，不能直接當合規實作。
- 取捨：採 Claude 的做法，但照 codex 的要求把 `mktemp`、`id`、`rm -rf` 正式寫進啟動器白名單。這裡真正的取捨是 codex I-48 提到的 remote docker context：bind mount 用的是 daemon 主機的路徑，`/tmp` 掛不進去；`.vendor_kit/.tmp.dist.<pid>/` 在專案內就沒這問題。傾向後者，但要問使用者。

### 自身升級 `upgrade vendor_kit` 第二次回 0 還是 1
- Claude：無新版且薄殼相符 → 0 無變更；只重產薄殼 → 1 + 6-2。
- codex：同版無需重產 → 0；只有確實更新薄殼才回 1。
- 取捨：兩方其實一致，只是 codex 額外點出 §7.4-1 寫「自身 upgrade 一律回 1」是矛盾，要改掉。

### -y 能否解除 frozen；未知 key 是否回 1；任何動詞先自動恢復
- Claude：未提。
- codex：A-02：CI 下 -y 不能解除 frozen，v2.5-1 已澄清；A-03：§4 通則「未知 key → 1」與 §8-7「忽略未知欄位」矛盾；A-15：唯讀動詞（sync/update/help）自動恢復會寫 tracked，與 frozen 衝突，應只偵測不執行。
- 取捨：三條 codex 都對，Claude 漏掉了。A-03 尤其重要，直接破壞向前相容定案。A-15 建議：唯讀動詞只偵測並提示「請重跑 <原動詞>」；需要寫檔的恢復只由可寫動詞執行。

### 根 justfile `default: @just --list`、`mod` vs `mod?`、CI=true、rootless -u、`local_bootstrap.sh`、二進位「未改才換」違反要改先問
- Claude：皆列為錯誤並實測（just 1.33/1.53）。
- codex：未提（codex 沒有 shell 可實測）。
- 取捨：我在本機 just 1.53.0 重跑：`default: @just --list` 確為語法錯誤、`mod` 缺檔讓所有 recipe 掛、`mod?` 正常。三條都成立且是「install 寫出來就壞」等級，優先度最高。CI=true 那條也對（GitHub Actions／GitLab 都是 `true`）。rootless 的 UID 映射說明正確。

## 規格與定案不符／超出來源
- 來源優先序漏列 proposal v2.5（附件四實際包含），導致 §3.1 uninstall 單段、-y 解除 frozen、所有拒絕變 declined 等多處與 v2.5 不一致；先把 v2.5 逐項核准納入。
- §3.1 `--pull never`：docker 19.03 不支援（20.10 才加）；來源 v2.2 B 本身寫錯。改為啟動器 `docker image inspect` 驗存在＋image ID 再 run。
- §1 install／§4.5 根 justfile 內容 `default: @just --list` 是 just 語法錯誤（1.33／1.53 實測），必須寫成兩行。
- §4.4 gen/tools.just 用 `mod` 指向缺失的 cache 檔會讓所有 `just` 呼叫（含修復入口）exit 1；改用 `mod?`（1.21 起可用）。
- §9 F1 「gen/tools.just 每個 mod 之前的 recipe 依賴」不可行：違反零 recipe 定案，且 just 1.33 兄弟模組間不能相依。刪除此選項。
- §0／§5 `CI=1`：GitHub Actions／GitLab 設的是 `CI=true`；要定義真值規則（非空且非 `0`/`false`）。
- §3.1 固定加 `-u $(id -u):$(id -g)` 在 rootless docker 下會映射成 subuid，對 /repo 無寫權；需偵測 rootless 分支（Podman 用 `--userns=keep-id`），否則 §7.4-21 必紅。
- §3.1 uninstall「單段」與 v2.5-10「兩段＋重驗指紋」衝突；把「需展開 image」與「兩段」分成兩個屬性。
- §4 通則「未知 key → 1」與 §8-7「忽略未知欄位、寫回保留」矛盾，違反相容性定案。
- §1 upgrade「CI 無 -y 又需改檔 → 1」：v2.5-1 已定 -y 不能解除 frozen；改為「CI 且需改 tracked → 1，與 -y 無關」。
- §0「任何動詞先恢復未完成操作」與 sync/update/help 唯讀及 frozen 衝突；改為「偵測並提示，需寫檔的恢復交給可寫動詞」。
- §4.7／§1 prune：image 的 label 只能在 build 時加，`docker pull` 無法追加；工具契約需加「Dockerfile.dist 必含 vendor_kit LABEL」並由 check.sh --dist 擋；B5 的專案路徑 label 不能放 image。
- §5 `VENDOR_KIT_REGISTRY_TOKEN_FILE` 以 `-e` 傳主機路徑容器讀不到；需 `-v` 唯讀掛載並傳容器內路徑。
- §9 B2 白名單漏 `VENDOR_KIT_NO_LOCK`。
- §9 E2：`renovate/default.json` 與 `extends: ["github>owner/repo"]` 互相矛盾；二擇一（根目錄 `default.json` 或 extends 加 `//renovate/default`）。
- §9 C1 min_reader：來源 grilling 把寫入者版本與最低讀取版本混用；兩者語意不同。
- §4.3 二進位／symlink「未改才換」未經詢問，違反 §0「要改先問」。
- §3.1「`-it` 只在互動」未排除 resolve；且 apply 的 stdout 不能當協定通道（TTY 合流）。
- §3.3 resolve 無副作用，不可能回報「引擎已變」這項已完成事實；引擎變更只能由 apply 之後判定。
- §7.4-16 `local_bootstrap.sh` 規格未定義；§1 只有 `bootstrap.sh --local`。
- §4.4 gen/<repo>.stamp 的 `image:<tag>` 沒有任何動詞會產生（`dev <repo> -i` 不存在），是 v2.3 §3 殘留。
- §1 `add --local <tar>` 寫 `tag@digest`，但 `docker load` 無 RepoDigests、單平台 tar 無 index digest；離線 add 寫哪個 digest 未定。
- §3.1 `grep -m1 '^vendor_kit *='` 與 §4.1 `^vendor_kit\s*=` 是兩個 regex，`\s` 非 POSIX BRE，`-m1` 不驗唯一性；需定義唯一正規行文法。
- §3.1／§5 主機命令白名單與實際需要（id、mktemp、git、docker inspect/load/ls/rm、逾時輪詢）不一致。
- §4.3 metadata 同時有兩套狀態列舉（managed/declined/unmanaged/deleted-by-user vs created/skipped-exists/appended/declined），且 declined 缺內容 hash 無法實作 Q15 的「新版有更新再問」。
- §2／§8-5「舊薄殼跑新 major 回 3」引 Q19，但 Q16 原文是回 1；屬推論，需使用者確認並回寫 grilling。
- §7.4-1「自身 upgrade 一律回 1」與「第二次應 0 無變更」不一致。
- §7.4-10 fresh clone「列出完整命名空間」：gen/、cache/ 都不存在時做不到工具命名空間，應改為只列 vendor_kit 命名空間。
- §6-24「升級失敗一律提示 --local」暗示離線 upgrade 可用，但 grilling 已定不支援。
- §7.4-15 要求引擎 image 兩平台位元組一致：amd64/arm64 binary 不可能一致，只有 COPY-only 的工具 dist 才能要求。

## 最終建議
這份規格還不能凍結 P=1 拆票。兩位審查員的結論高度重疊，差別主要在 codex 抓「來源與條文互斥」、Claude 抓「在最低環境跑不起來」，兩者都要修。

一、必修（會讓東西直接壞，不用問使用者）：
1. 根 justfile 改兩行 `default:` / `\t@just --list`。
2. gen/tools.just 改用 `mod?`。
3. 拿掉 `--pull never`，改 `docker image inspect` 驗 ID。
4. `CI` 真值規則：非空且不為 `0`/`false`；check.sh 自己 `export CI=1`。
5. 白名單補 `VENDOR_KIT_NO_LOCK`；TOKEN_FILE 改 `-v` 掛載。
6. resolve 永不 `-t`；「引擎已變」改由啟動器 apply 前後 grep version.toml 第一行比對，第一行變了就用新 ref 再跑一次 `upgrade vendor_kit`，第二次仍變 → 1。
7. 導言補 v2.5 為來源，並依 v2.5 修正：uninstall 兩段、-y 不解除 frozen。
8. §4「未知 key → 1」刪掉，改為忽略未知欄位＋寫回保留；只拒絕型別錯、重複宣告。
9. 唯讀動詞（sync/update/help）遇未完成交易：只偵測並提示重跑原動詞，不自動恢復。
10. 二進位／symlink「未改才換」改為「問後換」。
11. `vendor_kit =` 行定唯一正規形（整行 `vendor_kit = "<ref>"`，雙引號、無註解），regex 用 `[[:space:]]`，重複行 → 1。
12. 主機命令白名單明列：sh、grep、sed、id、mktemp、rm、git rev-parse、docker {pull,create,cp,run,rm,inspect,load,ls,image rm,network rm,volume rm}。
13. E2 取根目錄 `default.json`（vendor_kit 自身用 `renovate.json`）。
14. 工具契約加「Dockerfile.dist 必含 `LABEL io.github.<org>.vendor_kit=1`」，--dist 擋；專案路徑 label 只加在容器等資源，不加 image。
15. 刪 gen/<repo>.stamp 的 `image:<tag>`（或明寫留給 add --local）；`local_bootstrap.sh` 統一為 `bootstrap.sh --local`。
16. 拆 §7.4-15 為「工具 dist 兩平台位元組一致」與「引擎 image 只驗 protocol/schema label 一致」。

二、22 個待定的建議值（可直採者）：B2（如上修正）、B3（300 秒、只收正整數）、B5（`io.github.<org>.vendor_kit` 前綴；容器加 `.project`，image 只加 `=1`／`.protocol`／`.schema`）、B7（`-w /repo`、`--protocol P` 在子命令前）、C2（`vendor_kit_image_id`）、C3（同形、頂層鍵在 `[tools]` 前、undev 一起撤 image ID、local 也帶 schema/written_by）、C4（合成單一 `state`：managed|appended|declined|unmanaged|deleted，declined 附 `declined_hash`，另記 `source`、`complete`、`conflicts`）、C5（`.tmp.<verb>.<交易 id>.toml`，不用 `<repo>` 避免 uninstall 撞名）、C6（頂層 `description` 單行，src 相對 dist/）、D1（sync 用 6-1、重產完成用 6-2、Q9 舊句不用）、D2（採 codex 七則模板，但 6-19 改印「schema N 高於本引擎支援 M」）、E1（第一個失敗步驟的碼）、F2（依 Q10 只提示不重寫）、F4（`just --dump --dump-format json`）。

三、vk-resolve/1：採「先收完整份→驗首行與 `end <N>`→才動 docker→整份原樣掛進 apply 供重驗指紋」的骨架；TAB 分隔定位欄位、dev 路徑放最後一欄不編碼；kind = pull/extract/mount/engine/fingerprint/apply(yes|no)/end，prune 另加 keep。指紋覆蓋範圍明寫不含新版新增檔，apply 對新檔只建不存在者；apply 拿鎖後重算指紋，不同回 1。

四、結束碼 3：3 = 薄殼/檔案/引擎組合需先升級或退回，且零寫入；新舊以 schema/P 比不用 SemVer；floor 檢查先於任何上網；stamp 不符、薄殼被改、自身升級完成等既定回 1 的情境維持 1。

五、F1 定案建議：`mod?` ＋ 工具模組內私有 `_sync` recipe（用 `{{quote(justfile_directory())}}` 或環境變數傳路徑，不直接插字串）＋ 公開 recipe 相依它 ＋ --dist lint ＋ 例外集合（vendor_kit 自身動詞不前置）＋ sync 豁免 6-9。需要 1.33 fixture 驗證後才算結案。

真正要使用者拍板的：A1、C1、F1、B1、B4、B6、Q16→3、`upgrade vendor_kit` 語意、離線 digest、sync 快路徑。

## 要問使用者
- Q16「舊薄殼跑新 major 一般動詞回 1」是否正式改成 3 並回寫 grilling？6-19（舊引擎讀高 schema）是否也回 3？
- C1：接受把 min_reader 改成純資訊欄 `written_by`、讀取門檻只看 `schema`（Claude）？還是要 `written_by` 與 `min_reader` 兩欄並存（codex）？
- F1：接受「gen/tools.just 用 `mod?` ＋ 工具模組內私有 `_sync` 相依 ＋ --dist lint ＋ sync 豁免 6-9」嗎？哪些 vendor_kit 動詞明確不做自動前置（建議：全部 vendor_kit 自身動詞）？
- A1 prune：由啟動器執行 docker ls/rm（擴大白名單）而非掛 socket，可以嗎？image 清理範圍只限「本專案 version.toml 未引用且帶 vendor_kit label」還是整個 daemon？
- B4：vk-resolve 採 TAB 定位欄位、路徑原樣（Claude）還是 `|` 分隔、路徑 hex 編碼（codex）？是否需要獨立的 apply 結果檔（vk-apply/1），或用「啟動器 grep 第一行前後差異」就夠？
- B1 `--local`：接受明確前綴 `image:`／`tar:`（改 #27 已用介面）還是保留單一值＋歧義即回 1？
- B6 暫存目錄：`${TMPDIR:-/tmp}`（需 mktemp）還是專案內 `.vendor_kit/.tmp.dist.<id>/`（同檔案系統、remote docker context 也能掛）？
- `upgrade vendor_kit` 直接打：確認 = 查 registry（除非 -t/frozen）→ 有新版改第一行 → 啟動器用新引擎再跑一次重產薄殼 → 1；無新版且薄殼相符 → 0？（要改 §7.4-1 的「一律回 1」）
- `add --local <tar>` 寫哪個 digest？（release 附 `.digest` sidecar／`--digest` 參數／只寫 tag 並標記離線）
- sync 快路徑：允許啟動器只 grep 比對 stamp 第一行與 version.toml 各行、全相符時連 resolve 容器都不起（代價：一般指令不再每次 verify sha256）？
- rootless docker／Podman：接受「偵測 rootless 就不加 -u、Podman 加 --userns=keep-id」寫進契約嗎？
- `bootstrap.sh -t` 改成 `--tool <repo>[@<tag>]` 並刪 `-t`，可以嗎？`local_bootstrap.sh` 是否就是 `bootstrap.sh --local`？
- 拒絕合併後是否仍保有 managed 身分、另記 `declined_hash`（codex 建議），而不是 v2.5-4 的「所有拒絕都變 declined」？
- upgrade 多工具時某工具回 2，其餘工具做完再回 2？update 同時遇「需憑證 1」與「有新版 2」時回 1？
- 合併結果 TOML/just 解析失敗 → 2 留原檔時，baseline 不推、metadata 記 `parse-invalid`，可以嗎？

---
## 附：Claude 原文
# 一、歧義／遺漏／矛盾清單（逐條引節號）

## 矛盾（規格內部或與定案不符）
1. **§3.1 `--pull never` vs §0 docker ≥ 19.03**：旗標是 20.10 才有（docker/cli #1498）。改為 `docker image inspect` 驗存在＋image ID，不用 `--pull`。
2. **§1 install／§4.5 根 justfile `default: @just --list`**：語法錯誤（1.33/1.53 實測）。改兩行。
3. **§3.1「uninstall 單段」vs proposal v2.5-10「uninstall 兩段＋重驗指紋」**：v2.5 優先。把「需展開 image」與「兩段」分成兩個屬性：需 create/cp = add/upgrade/sync/undev；兩段 = add/remove/upgrade/sync/undev/uninstall/prune；單段 = install/`upgrade vendor_kit`/update/dev/help。
4. **§4.3 二進位「未改才換」vs §0「要改先問」**：改「未改 → 問後換」。
5. **§2、§8-5 回 3 vs grilling Q16 回 1**：採 3，但要使用者拍板並回寫 Q16。
6. **§4 通則「寫入者版本」vs §9 C1 `min_reader`**：見 C1。
7. **§9 F1 選項「mod 之前的 recipe 依賴」vs §4.4「tools.just 零 recipe」與 just 模組規則**：刪掉此選項。
8. **§9 E2 檔案路徑 vs extends 字串**：`github>owner/repo` 只讀根目錄 `default.json`。
9. **§7.4-16 `local_bootstrap.sh` vs §1 只有 `bootstrap.sh --local`**：二擇一並定義。
10. **§4.4 gen/<repo>.stamp `image:<tag>`**：無產生者；刪或改給 `add --local`。
11. **§3.1 `-it` 只在互動 vs §3.3 stdout 被解析**：resolve 永不 `-t`。
12. **§0 EOF「→ 1」vs「視為拒絕、不套用」**：定義：EOF/Ctrl-C = 中止整個 apply 回 1、不記 declined（declined 只記明確回答「否」）。

## 遺漏（定案有、規格沒寫，或規格必須有才能實作）
13. **啟動器本體在哪個檔**：§4.5 只列四個薄殼檔，POSIX sh 啟動器（pull/create/cp/trap/解析 vk-resolve）不在其中；是 vendor.just 內的 shebang recipe 還是 `.vendor_kit/vk.sh`？若是獨立檔要進 Q17 自描述首行清單並算進薄殼 hash。
14. **rootless docker／Podman 的 `-u`**（§3.1 vs §7.4-21）：rootless 下不加 `-u`；Podman 用 `--userns=keep-id`。啟動器偵測方式（`docker info --format '{{.SecurityOptions}}'`）要寫進契約。
15. **`CI` 真值規則**（§0/§5）：`CI` 非空且不為 `0`/`false` → frozen；check.sh 自己 `export CI=1`。
16. **`VENDOR_KIT_REGISTRY_TOKEN_FILE` 的 mount**（§3.1/§5）。
17. **工具 image 的 LABEL**（§4.7/§1 prune）：工具契約加「Dockerfile.dist 必含 `LABEL <key>=1`」，check.sh --dist 擋；否則 prune 只能清引擎 image。
18. **`add --local <tar>` 寫哪個 digest**（§1 add、§4.1）。
19. **resolve→apply 指紋交接方式**（§3.2/§3.3）：見 vk-resolve 提案（`/dist/vk-resolve`）。
20. **`upgrade`（不帶 repo）遇引擎新版時工具不升**（v2.5-7 有、§1 沒寫）。
21. **`upgrade vendor_kit` 直接打時是否查 registry／改第一行**（§1 (b)、§3.4）：建議＝會（apt 語意、有 `-t`），機制見選項 5；無新版且薄殼相符 → 0 無變更；只重產薄殼 → 1 + 6-2。
22. **sync 與 §0 位置檢查**：sync 由工具 recipe 自動呼叫時應豁免 6-9（或契約強制先 cd）。
23. **update 的碼優先序**：同時有「需憑證 → 1」與「有新版 → 2（--exit-code）」時回哪個？建議 1 優先（查詢不完整不能宣稱結果）。
24. **upgrade 多工具遇 2**：某工具衝突後其餘工具是否繼續？建議：預檢全部 → 逐工具做完、任一 2 則最終回 2（不中途停，避免半套）。
25. **frozen 下 `update`**：§0「不查最新版」是否禁掉 update？建議 update 不受 frozen 影響（它不寫檔）。
26. **`sync` 是哪些 vendor_kit 動詞的前置**：建議只有工具 recipe；vendor_kit 自身動詞各自完整（add/upgrade 本來就 materialize）。
27. **version.toml 正規行文法**（§4.1）：`^vendor_kit = "<ref>"$` 整行、雙引號基本字串、無註解；regex 統一 `^vendor_kit[[:space:]]*=[[:space:]]*"\([^"]*\)"[[:space:]]*$`；`schema` 第二行改稱慣例；頂層鍵必在 `[tools]` 之前；範例補 C1 欄位。
28. **薄殼 hash 精確定義**（§4.5）：「其餘內容」= 首行（含其換行）之後的全部位元組，CRLF→LF 後 sha256；ci/check.sh 的 shebang 行算進內容。
29. **合併結果解析失敗 → 2 留原檔**（§4.3）：baseline 推不推？建議不推、metadata `conflicts` 記 `parse-failed`，否則下次 upgrade 三者皆異再合併再失敗成迴圈。
30. **`bootstrap.sh -t`** 是引擎 tag 還是工具 tag、多個 `--tool` 共用一個？建議改 `--tool <repo>[@<tag>]`、刪 `-t`。
31. **pull 逾時在 POSIX sh 的實作**：`timeout` 非 POSIX，需背景 + 輪詢 kill；寫進 B3。
32. **gen/tools.just 用 `mod?`**（§4.4）：見 agy_claims_wrong 3。
33. **B2 漏 `VENDOR_KIT_NO_LOCK`**。
34. **§4.3 metadata 兩套列舉**：合一。
35. **`dev vendor_kit -i` 的「舊」定義**：以 schema／P 比，不以 SemVer（dev 版號常是 0.0.0-dev）。

# 二、22 個 [待定] 建議值

| 編號 | 分類 | 建議值 | 依據 |
|---|---|---|---|
| A1 | **取捨** | `prune [-n] [-y]`；兩段：`resolve prune` 輸出 `keep <name> <ref@digest>`（version.toml + local 引用的全部）；啟動器 `docker {container,image,network,volume} ls --filter label=<key>` 列出、扣掉 keep、`-y` 或詢問後 rm；`.tmp.*` 由 apply 刪。啟動器允許的 docker 子命令要擴為 pull/create/cp/run/rm/inspect/ls/image rm/network rm/volume rm。不掛 docker socket。 | 引擎不碰主機 docker、rootless 下 socket 路徑不固定 |
| B1 | 命名（直採） | `--local <tag 或 tar>`：是存在的檔案路徑 → `docker load` 並從輸出 `Loaded image:` sed 出 tag；否則視為 tag | proposal/#27 已用 |
| B2 | 命名（直採，修正） | 轉發：`CI`、`VENDOR_KIT_REGISTRY_TOKEN`/`_USER`/`_TOKEN_FILE`（後者改掛 `-v <file>:/run/vk-token:ro` 並傳容器內路徑；三者只在 update/upgrade 的 resolve）、`VENDOR_KIT_NO_LOCK`。啟動器自讀不轉發：`VENDOR_KIT_PULL_TIMEOUT`、`TMPDIR`。其餘不轉發。 | §5 NO_LOCK 由引擎讀 |
| B3 | 命名（直採） | `VENDOR_KIT_PULL_TIMEOUT` 秒，預設 `300`，`0` = 不限；POSIX 實作＝背景 pull + 每秒輪詢 + kill；逾時訊息屬 6-24 網路類 | 無 POSIX `timeout` |
| B4 | 直採（本提案） | 見第三節 | — |
| B5 | 命名（直採） | 鍵前綴 `io.github.<org>.vendor_kit`（OCI/Docker 建議反向 DNS；`io.github.*` 慣例）；容器/資源：`…=1`、`….project=<專案根絕對路徑>`；引擎 image：`….protocol=<floor_P>-<current_P>`、`….schema=<N>`（啟動器可 inspect 先判 floor，不必起容器）；工具 image：`…=1`（契約強制、--dist 擋） | image 不能 pull 時加 label |
| B6 | 命名（直採） | `mktemp -d "${TMPDIR:-/tmp}/vendor_kit.XXXXXX"`；`trap 'rm -rf "$tmp"; docker rm -f … ' EXIT INT TERM`；備選（問使用者，見開放問題）放 `.vendor_kit/.tmp.dist.<pid>/` | — |
| B7 | 命名（直採） | `-w /repo`；`--protocol P` 為全域旗標放子命令前：`<ref> --protocol P <verb\|resolve <verb>\|apply <verb>> [args]` | — |
| C1 | **取捨** | 欄位名 `written_by = "v1.2.0"`（資訊欄）；讀取門檻只看 `schema`；6-19 改印「schema N，本引擎最高支援 M」。若使用者堅持 min_reader 語意，必須放棄「同 schema 必可讀」 | 語意衝突 |
| C2 | 命名（直採） | `vendor_kit_image_id = "sha256:…"` | drawio p2 |
| C3 | 命名（直採） | 同 version.toml 形：頂層 `vendor_kit`、`vendor_kit_image_id`，`[tools]` 內 `<repo> = "path:<dir>"`；頂層鍵必在表頭前 | 同一套讀寫器 |
| C4 | 命名（直採） | `schema`、`written_by`、`source`（= 來源 ref@digest = 最後合併版本，合一）、`complete`（bool）、`conflicts = []`、`[[file]] dest/state/lines`（state ∈ managed\|appended\|declined\|unmanaged\|deleted；lines 只在 appended）、`[progress] state/started/done/pending` | Q15、Q13、v2.2 C |
| C5 | 命名（直採） | `.vendor_kit/.tmp.progress.<verb>[.<repo>].toml`，內容 = C4 的 `[progress]` 表 + `schema`/`written_by`；prune 與成功結束時刪 | grilling 進度日誌 |
| C6 | 命名（直採） | 頂層 `description`（單行、無換行，寫成 `# <description>` 註解）；`src` 相對 `dist/` | base_pitfalls 2-4 |
| D1 | 命名（直採） | `vendor_kit 已更新 <vX> → <vY>，請執行：just vendor_kit upgrade vendor_kit`（結束 1）；Q9 那句不再用（已被 Q10 取代） | Q10 |
| D2 | 命名（直採，加規則） | 實作票定逐字；規則：每句含可直接複製的指令；6-19 結束碼 3；6-18/6-19/6-10 都保證零寫入 | — |
| E1 | 命名（直採） | check.sh = 第一個失敗步驟的碼；③ 有衝突標記回 2；version.local.toml 被 track → 1 | — |
| E2 | 命名（直採，修正） | 根目錄 `default.json`，下游 `extends: ["github>ycpss91255-research/vendor_kit"]`；vendor_kit 自身設定用 `renovate.json` | Renovate 文件 |
| F1 | **取捨** | 建議 F1-A：工具 `<ns>.just` 內私有 `_sync` recipe（固定體 `cd "{{justfile_directory()}}" && just vendor_kit sync`），公開 recipe 相依它；check.sh --dist 以 `just --dump-format json` 檢查；sync 豁免 6-9 | 1.33 兄弟模組相依實測不可行 |
| F2 | 直採 | 依 Q10：只提示不重寫；undev vendor_kit 後 gen/.stamp（`<tag>`）≠ version.toml ref → 6-1 | Q10 |
| F3 | 待實測（不是取捨） | 引擎不讀 .git，只剩主機 `git rev-parse --is-inside-work-tree`，在 submodule（.git 是檔）應可；寫進 7.4-20 實測後定 | 19條-10 |
| F4 | 直採 | 採 base_pitfalls 1-6；add 預檢用 `just --dump --dump-format json` 取根檔既有 recipe/module 名（v2.5-5） | — |

分類小結：直採 17 條（B1、B2、B3、B4、B5、B6、B7、C2、C3、C4、C5、C6、D1、D2、E1、E2、F2、F4 中 F3 待實測）；要問使用者 3 條：**A1、C1、F1**（另加下方開放問題）。

# 三、`vk-resolve/1` 完整格式提案

**呼叫**：`docker run --rm [-u …] -v "<root>:/repo" -w /repo [-e CI …] <引擎> --protocol P resolve <verb> [args]`，**永不加 `-t`**、不互動、不寫任何檔。啟動器把 stdout 整份存到 `<tmp>/vk-resolve`，之後以 `-v "<tmp>:/dist:ro"` 掛進 apply（apply 讀 `/dist/vk-resolve` 取指紋重驗）。

**結束碼**：resolve 非 0 → 啟動器不讀 stdout，原碼傳出（1/2/3）。

**文法**（P=1）：
```
vk-resolve/<P>          ← 第一行，P = 呼叫方 --protocol 的值（不是引擎的 current_P）
<kind>TAB<f1>[TAB<f2>…] ← 每行一筆；欄位以單一 TAB 分隔；欄位不得含 TAB/CR/LF/NUL；UTF-8；LF 結尾；無空行、無註解
endTAB<N>               ← 最後一行；N = 記錄行數（不含首行與 end）
```
`<kind>`、`<name>` ∈ `[A-Za-z0-9_.-]+`；`<ref>` ∈ `[A-Za-z0-9_.:/@-]+`；`<dir>` 任意（可含空白與 `$`），啟動器以 `IFS=<tab> read -r kind a b c` 讀，一律加引號、不 eval。

| kind | 欄位 | 啟動器動作 |
|---|---|---|
| `pull` | `<name> <ref>` | `docker pull <ref>`（本機已有相同 digest 則略；逾時／失敗 → 6-24）。name = `vendor_kit` 或 `<repo>` |
| `extract` | `<repo> <ref>` | pull（同上）→ `docker create --label <key>=1 <ref> /x` → `docker cp c:/dist/. "<tmp>/<repo>/"` → `docker rm`；apply 見 `/dist/<repo>/` |
| `mount` | `<repo> <dir>` | dev 覆寫：驗 `<dir>/dist/init.toml` 存在（缺 → 1）→ `-v "<dir>/dist:/dist/<repo>:ro"` |
| `engine` | `<ref>` | 只在 upgrade：apply 會把第一行改成此 ref。啟動器先 pull；apply 結束後 grep 第一行 == ref → `docker run … <ref> --protocol P upgrade vendor_kit`，其碼原樣傳出（預期 1 + 6-2）。第二次第一行又變 → 1 報錯，不再重跑 |
| `fingerprint` | `<sha256 hex>` | 不解析，只隨檔交給 apply。引擎算法：對「version.toml、version.local.toml（缺記 `-`）、每個 baseline/*/.vendor_kit.toml、metadata 中 state=managed/appended 的每個 dest、gen/.stamp 第一行、每個 gen/<repo>.stamp 第一行、本次 verb argv」依路徑排序，串接 `<path>\0<sha256(content)或->\n` 再 sha256。**不含**新版新增檔（resolve 時 N 未展開；apply 對新檔只建不存在者） |
| `apply` | `yes` \| `no` | 恰一筆；`no` → 啟動器直接 exit 0（sync 快路徑，不起第二個容器）；`yes` → docker 階段後跑 `apply <verb> [--dry-run] [args]` |
| `end` | `<N>` | 必為最後一行；缺、N 不符、首行不是 `vk-resolve/<P>`、未知 kind、`apply`/`fingerprint` 多筆 → 啟動器 1「引擎輸出不完整或不相容」，不得繼續 |

**範例 1：`upgrade`（不帶 repo）遇引擎新版**（v2.5-7：只改第一行、工具不升）
```
vk-resolve/1
pull	vendor_kit	ghcr.io/org/vendor_kit:v1.3.0@sha256:aaaa…
engine	ghcr.io/org/vendor_kit:v1.3.0@sha256:aaaa…
fingerprint	9f2c…e1
apply	yes
end	4
```
**範例 2：`sync`，一個 cache 過期、一個 dev 工具**
```
vk-resolve/1
extract	base	ghcr.io/org/base-dist:v2.3.0@sha256:bbbb…
mount	robot_tools	/home/me/robot tools
fingerprint	1c0e…77
apply	yes
end	4
```
**範例 3：`sync` 無待辦**
```
vk-resolve/1
fingerprint	1c0e…77
apply	no
end	2
```
**範例 4：`prune`（A1 若採兩段）**
```
vk-resolve/1
keep	vendor_kit	ghcr.io/org/vendor_kit:v1.2.0@sha256:…
keep	base	ghcr.io/org/base-dist:v2.3.0@sha256:…
apply	yes
end	3
```
（`keep` 為 P=1 的第 8 種 kind；只在 prune 出現。）

**P 提高規則**：新 kind／新欄位／欄位語意變 → P+1；引擎對 `--protocol P_old` 只能輸出 P_old 認識的 kind。

# 四、結束碼 3 邊界（建議寫進 §2）
3 = 「現有薄殼／檔案／引擎的組合需先升級或退回才能繼續」，且**零寫入**：(a) 薄殼 P < 引擎 floor_P（6-18）；(b) 引擎讀到 schema > 支援上限（6-19）；(c) `upgrade vendor_kit -t` 目標引擎 schema/P 低於現有檔（6-10）；(d) `dev vendor_kit -i` 的引擎 schema/P 低於薄殼首行者要重產薄殼；(e) 舊薄殼跑新 major 一般動詞。「舊」一律以 schema/P 比，不以 SemVer。網路／認證／不存在 → 1；順序：floor 檢查在任何上網之前。

## 附：codex 原文
（程序備註：codex 首輪 580 秒逾時未輸出最終答案，經 `codex exec resume --last` 續跑後取得完整答案；以下全為 codex 的結論，未加入本代理意見。）

codex 總結：這份規格尚不能作為「每張票唯一的 input／output 定義」。問題不只在 22 個待定值；有幾處既有條文彼此衝突，或缺少實作所必需的傳遞機制。建議先修正來源與互斥條文，再凍結 P=1。

═══════════════════════════════════════
C-1．vk-resolve/1 完整格式提案
═══════════════════════════════════════
用途與邊界：
- resolve 輸出的是「執行計畫」，不是已完成事實。
- 啟動器只解讀固定記錄，組合固定 Docker 指令；不得把輸出當 shell 指令。
- apply 必須收到同一份完整計畫，拿鎖後重新驗證。
- 「引擎已變」只允許出現在 apply 完成回報。
- 救援路徑仍可單段執行，不依賴此格式或 gen/。
- 主格式涵蓋 add／upgrade／sync／undev，以及採納 v2.5 後的 uninstall。prune 的 Docker 資源清單另立格式。

傳輸文法（ASCII、LF、固定位置欄位，分隔符 `|`）：
```
vk-resolve/1
request|<verb>|<scope>|<mode>
fingerprint|inputs|sha256:<hex64>
image|<repo>|<ref>|<purpose>
bind|<repo>|<host-dist-path-hex>
todo|<action>|<subject>
next|<step>
end|<record-count>
```
精確規則：
- 第一行只能是 `vk-resolve/1`。
- 每行以 LF 結尾（含最後一行）；禁止 CR、NUL、BOM。
- 不允許空欄位；不適用值用 `-`。各記錄欄位數固定。
- 記錄順序：request、fingerprint、全部 image、全部 bind、全部 todo、next、end。
- request、fingerprint、next、end 各一筆；其餘零至多筆。
- 同 repo 的 image／bind 不得重複；相同 todo 不得重複。
- image／bind 依 repo 的 ASCII 位元組順序；todo 依 action、subject 排序（todo 順序不是寫檔順序）。
- `end` 後必須立即 EOF；count 為首行與 end 以外的記錄數。
- 診斷全部走 stderr；resolve 不詢問、不配置 TTY。
- 先完整接收、確認 resolve 結束碼及整份文法，再執行任何計畫中的 Docker 動作；不能邊讀邊 pull／刪除。
- 支援的 P 下格式損壞／缺 end／未知記錄 → 1；真正不支援的協定 → 3。均不得繼續。

固定欄位定義：
- request：verb＝六個動詞之一；scope＝`all`、repo 或 `-`（uninstall 用 `-`）；mode＝`apply`／`preview`。
- fingerprint：固定 `inputs`；`sha256:`＋64 個小寫 hex。
- image：repo；完整 `name:tag@sha256:…`；purpose＝`extract`（取得 /dist）／`handoff`（自身升級預定接手引擎）。
- bind：repo；絕對 dist/ 路徑原始位元組的小寫 hex（引擎已解析 local 覆寫；主機解碼後掛至 /dist/<repo>:ro）。
- todo：action＝`materialize`、`add`、`upgrade`、`undev`、`uninstall`、`tools-just`、`engine-ref`；subject＝repo 或 `-`。
- next：`apply`／`done`（done 僅能用於已完成全部檢查、沒有待辦的快路徑）。
- end：非負十進位整數。

補充約束：
- repo 建議限為 `[A-Za-z0-9_][A-Za-z0-9_.-]*`，不得是 `.`、`..`；`vendor_kit` 保留（新增名稱限制，須先確認）。
- ref 必須經引擎的 image-reference parser 驗證；不能只靠字元白名單。
- bind 的 hex 解碼只能使用固定解碼程序；結果作為單一、有引號的 argv，不得 eval、source 或插入 shell 程式碼。
- 空白、中文、$、引號均可經 hex 傳遞。NUL 不合法；換行及 Docker mount 語法特殊字元的支援範圍另須定案。
- 同一 repo 不得同時有 extract image 與 bind。
- handoff image 只能是 vendor_kit；有 handoff 時，本次不得夾帶工具升級寫入。
- preview 可以 pull／展開至暫存，但不能改 cache、gen、metadata、使用者檔或版本檔。
- `next|done` 不得附有 image、todo 或待執行 bind。

指紋覆蓋範圍（第一版採保守規則，因第一次 resolve 尚未看到新版 init.toml，不知道全部新 dest）：
- 請求：P、動詞、正規化 argv、dry-run／-y／frozen、實際引擎身分。
- 計畫：request、image、bind、todo、next 的規範化位元組；不含 fingerprint 與 end。
- 控制資料：version.toml、version.local.toml、相關 metadata、baseline、薄殼、相關恢復日誌；缺檔也是狀態。
- 使用者檔：add／upgrade／uninstall 對 /repo 可作為初始檔目的地的樹建立快照，排除 .git、cache/、gen/、本次暫存。
- cache／gen：若計畫依賴其現況，納入相關檔案、印記與 tools.just；不能只驗第一行。
- 路徑狀態：檔案種類、相對路徑、內容、相關 mode、symlink 目標；不跟隨 symlink 越界。
- Docker／local：鎖定 index digest、本機引擎 image ID、local 覆寫內容。
內部雜湊序列（長度前綴）：
```
field := uint64_be(byte_length) || raw_bytes
entry := field(path) || field(kind) || field(mode) || field(content_or_link_target)
```
entry 按路徑原始位元組排序；區分類型與缺檔；不做 LF 正規化；不納入 mtime；SHA-256 由引擎計算；apply 拿鎖後重算，不同即 1「請重跑」。代價是大型專案雜湊較慢；替代方案是展開後再做一次唯讀 planning（增加內部階段，須明列為取捨）。

計畫交給 apply：
```
--protocol 1 apply <verb> --plan /vk/plan -- [原動詞參數]
```
啟動器把 resolve 原始 stdout 保存在自己擁有的暫存檔，唯讀掛至 /vk/plan；image 展開內容掛至 /dist/<repo>:ro；apply 不重新選最新版；原 argv 與計畫中正規化請求不一致 → 1；暫存檔與恢復日誌生命週期分開。

範例一：add
```
vk-resolve/1
request|add|tool_a|apply
fingerprint|inputs|sha256:aaaa…(64 hex)
image|tool_a|ghcr.io/example/tool_a-dist:v2.3.0@sha256:bbbb…(64 hex)|extract
todo|add|tool_a
todo|materialize|tool_a
todo|tools-just|-
next|apply
end|7
```
範例二：sync 無待辦（啟動器確認完整輸出及 resolve 回 0 即結束；不起第二個引擎容器）
```
vk-resolve/1
request|sync|all|apply
fingerprint|inputs|sha256:cccc…(64 hex)
next|done
end|3
```
範例三：預定自身升級（沒有 engine-changed，因為尚未寫入第一行）
```
vk-resolve/1
request|upgrade|all|apply
fingerprint|inputs|sha256:dddd…(64 hex)
image|vendor_kit|ghcr.io/example/vendor_kit:v1.1.0@sha256:eeee…(64 hex)|handoff
todo|engine-ref|vendor_kit
next|apply
end|5
```
apply 完成回報（另定 vk-apply/1，寫到啟動器提供的結果目錄，先暫存再原子改名為固定 `result`）：
```
vk-apply/1
fingerprint|inputs|sha256:<hex64>
status|<status>
engine|<ref-or-dash>
end|3
```
status 僅允許：ok、preview、engine-changed（內部階段成功）；conflict（對應 2）；failed（對應 1）；incompatible（對應 3）。除 engine-changed 外 engine 欄位必須是 `-`。啟動器只有在程序成功、結果檔完整、指紋一致、status 為 engine-changed 時才接手新引擎；不能靠「回 1」猜測。最後對使用者仍依定案回 1。互動 apply 的人類輸出與結果檔分離（Docker TTY 會合流 stdout/stderr，不能一面 -it 一面假設 stdout 是乾淨協定通道）。

═══════════════════════════════════════
C-2．22 條 [待定] 建議值表
═══════════════════════════════════════
| 編號 | 建議值 | 分類 | 依據／限制 |
|---|---|---|---|
| A1 | `prune [-n/--dry-run] [-y/--yes]`。先列候選，問「要刪除以上 vendor_kit 資源嗎？」；主機執行 Docker，不掛 socket。只清已確認失效的暫存，活躍恢復日誌不得刪。 | 取捨（問使用者） | 動詞已定；詢問、共享 image 範圍、跨專案保護未定。 |
| B1 | 保留 `--local`；值明確區分 `image:<tag>` 與 `tar:<path>`，並保留既有未加前綴輸入的相容解析。明確路徑當 tar；歧義則回 1，不靠副檔名猜。 | 取捨（問使用者） | 旗標名可直採；值的判別、相容範圍及多 image tar 是行為。工具 add --local 仍只收 tar。 |
| B2 | 白名單：CI、VENDOR_KIT_NO_LOCK；registry 三變數僅授權的查詢階段；pull timeout 由主機讀。其餘不自動轉發。 | 命名（直採；修正遺漏） | 保留 Q11 憑證限制及已有 NO_LOCK；TOKEN_FILE 必須另有唯讀 mount 與容器內路徑轉換。 |
| B3 | `VENDOR_KIT_PULL_TIMEOUT=300`，正整數秒；不接受 0 表示無限。定義為單次 pull 的總經過時間，逾時回 1 並指出 ref。 | 取捨（問使用者） | 300 是建議預設；目前限定命令集合沒有直接可用的通用 watchdog。 |
| B4 | 採 C-1 固定位置 `|` 分隔格式；路徑 hex；end 計數；完整計畫交 apply；另設 apply 結果通道。 | 取捨（問使用者） | 分隔符可直採；指紋範圍、快照成本、結果通道及傳遞 argv 是契約。 |
| B5 | 功能鍵 `io.vendor_kit.managed=1`、`.kind`、`.protocol`；專案 label 只用於專案建立的容器等資源。image 使用建置時的 managed/kind/protocol，不放專案路徑。 | 取捨（問使用者） | 字串可直採；image 共享及 prune 所有權不可。reverse-DNS 前綴應確認命名權。 |
| B6 | 暫存目錄樣式 `vendor_kit.<唯一識別>`；主機暫存與 `.tmp.<verb>.<id>.toml` 日誌分開。 | 命名（直採） | mktemp -d 目前不在嚴格命令白名單內，不能直接當合規實作。 |
| B7 | Docker `-w /repo`；引擎全域旗標 `--protocol P` 一律在子命令之前；所有 argv 原樣傳遞。 | 命名（直採） | 不得依賴 image 的預設 WORKDIR。 |
| C1 | 拆成 `written_by = "vX"` 與 `min_reader = "vY"`。 | 取捨（問使用者） | 解開來源自身混用語意；否則破壞 N−1 可讀 N。 |
| C2 | `vendor_kit_image_id = "sha256:<hex64>"` | 命名（直採） | 沿用 tag＋ID 定案。 |
| C3 | 工具覆寫放 `[tools]`；vendor_kit 與 image ID 放頂層。 | 命名（直採） | 與 version.toml 同形。 |
| C4 | `source`、`last_merged`、`complete`、`[files."<dest>"]`、`[appended."<dest>"]`、`conflicts`、`[progress]`；另記 `offered_hash`／`declined_hash`、進度前後 hash。 | 取捨（問使用者） | 名稱可直採；四態所有權、拒絕後重問、復原模型須決策。last_merged 建議完整 ref@digest。 |
| C5 | `.tmp.<verb>.<transaction-id>.toml`；含 schema、writer、verb、targets、phase、每步前後 hash、done/pending、已取得的同意。 | 取捨（問使用者） | 固定 `.tmp.<verb>.<repo>` 會碰撞，uninstall 是多工具交易。 |
| C6 | 頂層 `description`；`src` 相對 dist/。src／dest 均做正規化與越界檢查；description 每行輸出都必須成為註解。 | 命名（直採） | 不能讓換行 description 注入 just 語法。 |
| D1 | sync 用 6-1；完成重產用 6-2；Q9 舊句不另立活躍分支。 | 命名（直採；行為已定） | Q10 取代 Q9 的 sync 自動重寫。 |
| D2 | 採七則文字模板（見下）；不得留「實作票定」。 | 命名（直採） | 唯一介面參考必須在拆票前固定文字。 |
| E1 | check.sh 回第一個失敗步驟的碼；工具測試原碼傳出。1/2/3 是 vendor_kit 自身語意，不限制工具測試碼。 | 命名（直採；規則補齊） | 不吞錯；③ 的衝突保持 2。 |
| E2 | 保留 `renovate/default.json`，extends 改為 `github>ycpss91255-research/vendor_kit//renovate/default`。 | 命名（直採） | 原本無路徑的 extends 會找 repo 根的 default.json（Renovate preset 格式）。 |
| F1 | 工具公開入口在任何工具副作用前呼叫 sync；可用 shell 子呼叫，但尚不能宣稱完成自動前置契約。 | 取捨（問使用者） | 不接受 gen/tools.just 加 recipe；解析失敗救援與舊 recipe 執行問題須先解決。 |
| F2 | undev vendor_kit 撤掉 tag 與 ID；下次若薄殼不符，只回 1＋6-1，不重寫。 | 命名（直採；已定） | Q10 優先。 |
| F3 | 「已初始化且有工作樹的 submodule 可作專案根」，受禁止巢狀規則限制；正式承諾以完整 fixture 通過為條件。 | 取捨（問使用者） | 目前沒有實測結果。 |
| F4 | 主機 just 用 `--dump --dump-format json` 取得完整結構，交引擎解析；檢查 recipe、alias、module 及保留名。禁止用 --summary 作唯一來源。 | 命名（直採；需驗收） | 1.33 有 JSON dump；summary 會省略 private 名稱。 |

D1 自身升級訊息分派：
- sync 確認薄殼版本與選用引擎不符 → 1：「vendor_kit 已更新 <vX> → <vY>，請 just vendor_kit upgrade vendor_kit」
- upgrade vendor_kit 確實完成重產 → 1：「已升級引擎 <vX>→<vY> 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」
- 第一行已改但新引擎拉取／重產失敗 → 1：「引擎版本已鎖定為 <vY>，但薄殼尚未重產；請排除上述錯誤後執行 just vendor_kit upgrade vendor_kit」
- Q9 舊句「請再跑一次剛才的指令」不獨立保留。
- 缺 gen/.stamp 時不能憑空產生 <vX>；應讀薄殼自描述判定。

D2 七則逐字模板：
- 6-16：「目前目錄不在 Git repository 內。請先自行執行 git init，再重新執行 bootstrap.sh。」
- 6-17：「install 不接受工具名稱。接入工具請執行：just vendor_kit add <repo>」
- 6-18：「目前薄殼或引擎低於支援下限 <floor>。請以 bootstrap.sh 重建。」
- 6-19：「無法讀取 <file>：schema <N> 高於本引擎支援的 <M>；寫入者為 vendor_kit <written_by>。請使用支援此 schema 的引擎，或使用 version.toml 指定的引擎。」（刻意不說「需要 ≥ 寫入者版本」）
- 6-23：「需要 just ≥ 1.33.0，目前為 <version>。請使用 GitHub release 版。」接固定兩行「下載：<平台對應 URL>」「安裝：<不覆蓋既有檔的安裝指令>」（不得新增 curl/tar 主機依賴、不得覆蓋既有 just）
- 6-28：「偵測到薄殼被修改：<files>。未重產任何薄殼。請先檢視下列差異；確認並手動還原後，再執行 just vendor_kit upgrade vendor_kit。」
- 6-29：「注意：新版範本將建立或修改 CI 設定 <X>。請確認下列內容後再決定是否套用。」

═══════════════════════════════════════
C-3．歧義／遺漏／矛盾清單（逐條引節號）
═══════════════════════════════════════
- I-01 矛盾｜導言、§10｜漏 v2.5；先固定實際來源集合。
- I-02 矛盾｜§0、§1 upgrade、§7.1｜frozen 不受 -y 解除；警告變失敗須使用明列集合，不能把 Q15 明定不紅燈的提醒也升為失敗。
- I-03 矛盾｜§0、§1 update/help/sync、§4.6｜任意動詞自動恢復可能破壞唯讀或 frozen。應先偵測；需 tracked 寫入的恢復交由明確可寫動詞。
- I-04 矛盾｜§4、§8-7｜未知欄位應保留；不能同時一律報錯。
- I-05 歧義｜§3.1、§4.1、§4.2｜`^vendor_kit *=` 與 `^vendor_kit\s*=` 接受集合不同；`\s` 不是可攜 POSIX BRE。須固定允許的空白、引號、尾端註解及 local 缺鍵規則。
- I-06 遺漏｜§3.1、§4.1｜`grep -m1` 不能驗證唯一性。重複 vendor_kit 行、表內同名鍵、異常 local 檔不能悄悄選第一筆或退回正式版。
- I-07 矛盾｜§3.1、§5、§8-1｜嚴格命令白名單與 id、mktemp、git、load、inspect、資源掃描／刪除及 timeout 不相容。
- I-08 矛盾｜§1 dev、§3.1、§7.4-2｜Docker 19.03 不支援 --pull never；改實作而非改最低版本。
- I-09 遺漏｜§3.1、§3.3｜resolve 禁止 -t；互動 apply 必須有獨立結果通道。
- I-10 遺漏｜§3.2、§3.3｜沒有 plan 傳入 apply 的 argv／mount，也沒有已提交結果回報格式。
- I-11 矛盾｜§3.3｜resolve 無副作用，不能輸出「引擎已變」這項已完成事實。
- I-12 遺漏｜§3.3、§4.7｜未展開新版前不知道新 dest，無法只 hash「要動的使用者檔」。
- I-13 遺漏｜§3.1、§4.3｜project flock 不能阻止編輯器。詢問後、替換前仍須重查目標前像。
- I-14 歧義｜§3.1、§4.4、§8-9｜多個 cache 目錄與 tools.just 不能靠多次 rename 成為跨檔原子交易。須定義鎖定讀者、提交點及故障恢復。
- I-15 矛盾｜§1 sync、§4.4、§7.4-10｜fresh clone 缺 gen/.stamp，但只准 install／自身 upgrade 寫它。須從薄殼自描述判斷相容。
- I-16 遺漏｜§4.5、§8-6｜新引擎要比對「上次產物」，須有歷史版本模板／合法 hash 對照，且不依賴 gen/。
- I-17 矛盾｜§1、§4.4、§4.5、§9 F1｜工具 recipe 第一行 sync 太晚，救不了解析失敗，也不能更新外層已載入的 recipe。
- I-18 遺漏｜§1、§9 F1｜自動前置例外集合缺失：help、sync 自身、install、upgrade vendor_kit 及恢復動詞。
- I-19 歧義｜§7.4-10｜「完整命名空間」是 vendor_kit 還是包含工具？
- I-20 遺漏｜§1 upgrade、§4.7｜upgrade 新版新增 namespace 或 dest 也須做全域撞名預檢。
- I-21 遺漏｜§4.3｜declined 需要內容版本／hash，才能實作 Q15。
- I-22 歧義｜§4.3、v2.5-4｜managed、declined、unmanaged、deleted-by-user 混合所有權與互動狀態。
- I-23 遺漏｜§4.3、§4.7｜append 必須定義片段邊界、順序、末行無 LF、部分行原已存在、多片段及多處命中。
- I-24 矛盾／歧義｜§4.3、§2｜TOML／just 合併解析失敗「回 2 留原檔」卻可能沒有標記，下次會誤判已解。應另記 parse-invalid 狀態。
- I-25 遺漏｜§4.3、§2｜git merge-file 的真正錯誤不能映射為衝突 2；I/O／執行錯誤回 1。
- I-26 歧義｜§1 upgrade、§6-14｜「有待合併只補到 B、不查最新」卻必須印確切新版 vX。
- I-27 歧義｜§1 upgrade、§7.4-1｜自身 upgrade 一律回 1，與第二次應 0 無變更不一致。
- I-28 遺漏｜§1 upgrade、§3.4、§8-10｜upgrade vendor_kit -t 的目標引擎取得、唯讀可讀性預檢、何時更新第一行沒有完整流程。
- I-29 歧義｜§3.2、§3.4、§8-2～5｜引擎接受 [floor_P,current_P] 與永久救援相容如何共存？release floor、P floor、schema 是三個維度。
- I-30 遺漏｜§1、§2｜工具層 1 不動 version.toml，與 uninstall 已完成部分、多工具 upgrade 中途失敗的聚合語意未對齊。
- I-31 遺漏｜§4.2、§4.6｜local 缺 schema／writer；undev 日誌位置、引擎覆寫的雙欄位撤除，以及最後一個覆寫移除後保留何種檔案未定。
- I-32 遺漏｜§1 uninstall、§4.3、§4.5｜uninstall 用什麼可信 hash 判斷可刪 version/local/baseline？metadata 不能先刪掉再以它證明歸屬。
- I-33 矛盾｜§1 prune、§4.6｜prune 不能把未恢復的 .tmp.* 當一般垃圾。
- I-34 歧義｜§1 prune、§9 B5｜單一專案的 version.toml 無法代表其他專案的 image 引用；index digest、平台子 manifest 與本機 image ID 不是同一身分。
- I-35 遺漏｜§1 bootstrap/add、§5｜add 預設最新需要列舉版本，但 token 只准 update／upgrade 使用。私有 add 未指定 -t 時應明確拒絕並提示 -t。
- I-36 遺漏｜§5 TOKEN_FILE｜只傳主機檔案路徑給容器讀不到；須定 mount、容器路徑、權限及與直接 TOKEN 同時設定時的規則。
- I-37 矛盾｜§3.1、§6-24｜denied 不一定能分辨不存在／無權限；disk-full、daemon 不可用不屬三分類。
- I-38 矛盾｜§6-24、§1 upgrade｜升級失敗一律提示 --local 會暗示離線 upgrade 可用；grilling 已定不支援。
- I-39 遺漏｜§1 bootstrap、§7.4-16｜離線包缺清單格式、架構選擇、tar 到正式 ref／index digest 的對照，以及 --tool 如何取得對應 tar。
- I-40 遺漏｜§1 bootstrap｜-t 究竟指定引擎版、全部工具版或某工具版未定；與 Q18 的優先關係。
- I-41 遺漏｜§4.7、§7.2｜src、dest 父目錄 symlink、特殊檔案、hardlink 及覆寫路徑型別變化未完整限制。
- I-42 歧義｜§4.7｜「唯讀 symlink」不會讓主機透過 symlink 寫入變成唯讀；唯讀是容器 mount 的性質。
- I-43 矛盾｜§4.7、§7.4-15｜工具 COPY-only dist 可要求兩平台位元組一致；引擎的 amd64／arm64 binary 不能要求整個 image 內容一致。
- I-44 遺漏｜§7.1｜「工具 check 若有」「專案測試」的發現方式、順序、無測試行為，以及防止 check 遞迴呼叫 check.sh 未定。
- I-45 矛盾｜§7.1、§0｜引擎不讀 index，卻要拒絕 local 被 track，並保證 frozen 不寫實際 tracked cache/gen。相關檢查須由主機 git 提供。
- I-46 矛盾｜§9 E2、§7.3｜preset 檔案路徑與 extends 不匹配；monorepo 的 regex 還須匹配各子專案的 .vendor_kit/version.toml。
- I-47 遺漏｜§0、§1 install｜第一次 install 尚無 .vendor_kit/，須另定候選專案根＝呼叫目錄；禁止巢狀只查祖先漏掉「在已有子專案上方再 install」。
- I-48 遺漏｜§3.1、§7.4｜Docker bind mount 使用 daemon 主機的路徑；remote Docker context 不能假設可掛 client 的 $PWD。