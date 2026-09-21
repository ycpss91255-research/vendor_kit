# diff3

## 一致
- 採方案 B（三方、只顯示不寫回）；C 直接違反「工具不改使用者檔」的規則，兩位都否決。
- 基準（舊模板副本）放在進 git 的 `.vendor_kit/base/<name>/`，不能放 `.<name>/`（會被 install/upgrade 整批覆蓋、fresh clone 也沒有）。
- 但 notes §12「vendor_kit 升級時整個 `.vendor_kit/` 換新」跟 base/ 衝突，必須先改規則（只換程式檔、或程式與持久狀態分子目錄）。我查 notes 第 142/161/263 行，確實寫「整個換新」，兩位都對。
- 更新基準要用獨立指令（`just accept` / `just baseline-accept`），不要在 diff 結尾問 y/N。Claude 給的技術理由（`docker run --rm` 沒 -it，stdin 不是 TTY；notes 第 91 行確認是 `docker run --rm`）＋ codex 給的語意理由（推進基準本身是決策）互補。
- (iii) 用舊 image digest 重取不該當一般 diff 的自動備援；頂多當明確執行的復原/匯入功能。缺基準時退回二方，並明確標示。
- 第一版只做「檔案層級分類」（dpkg 四格式 / codex 的五類 B、N、U 關係）＋兩份 B→N、B→U 差異；不承諾行級衝突判定。
- 「兩份二方 diff 取 hunk 重疊」不是正確的衝突判定：使用者已手動套上同樣改動會被誤判為衝突（兩位都指出）。
- agy 對 dpkg「只能說改過/沒改」說得太窄：只存舊版 hash 就能做檔案層級三方分類。
- agy 對 Copier/Cruft「只記 commit 就便宜重建」說得太簡：它們還依賴 answers/變數與模板來源，不能推論優於完整快照；對應到 #14 引入變數後 (iii) 就得存變數並解析舊 dist。
- agy 的 Yeoman 選項表漏了 r（reload），小錯不影響結論。
- 新增/移除/改名的模板檔要處理：不能只遍歷新版 init.toml，要取新舊聯集；現 proto 對新增檔完全不報。
- 多工具 init 到同一 dest（.gitignore、hooks）的擁有權沒定義，兩位都列為待決。

## 分歧（含判斷）
- 行級（hunk）衝突判定要不要做、怎麼做：codex 的陷阱清單是對的，Claude 的「區段重疊」若不處理這三點會出假結果；但 Claude 的分期路線可行。折衷：第一版只做檔案層級分類＋兩份 diff，行級只標「可能重疊」；第二版直接做真 diff3（Claude 的估算合理，但要把 codex 的三個陷阱寫成測試案例）。不要做中間那個「區段重疊＋特判」版本，省得做兩次。
- B+：`just diff --patch` 輸出合併提案讓使用者用主機 git apply 自己套：B+ 值得放進待決，但依賴真 diff3 且「工具給 patch、人自己 apply」是否算合規要問使用者。第一期不做。
- B0（只存 hash、dpkg 式）要不要當獨立階段：既然 init 從第一版就要寫基準，直接存完整副本（旁邊附 sha256 與版本）成本差不多，B0 單獨當一期沒必要；但 B0 的四格分類邏輯就是第一版 diff 的核心，應吸收進 B 第一版。
- accept 的語意：兩者不矛盾。採 codex 的語意定義與寫入來源（新版模板，不是使用者檔），保留 Claude 的逐檔粒度作為選項問使用者。
- agy 對 Cruft 的描述哪裡錯：codex 更精確；兩位都同意 agy 把 Copier inline 標記與 Cruft .rej 混成一種。更正時採 codex 版本。
- (iii) 的缺點怎麼寫：兩者同向，合併即可：不採 (iii) 為自動備援，理由用 Claude 的「備援比主路徑複雜」，並依 codex 刪掉「必被刪除／pull 較慢」這兩句無據說法。

## 對前例資料的更正
- 方案 C 描述「Copier/Cruft：沒衝突自動套、有衝突留標記」是混寫：Copier 預設 `git apply --reject` 產 .rej，只有 `--conflict inline` 才留 <<<<<<< 標記；Cruft 是 `git apply -3`，失敗且工作區仍乾淨時才退回 `--reject`，一律 .rej、無標記。
- 「Copier/Cruft 存 git commit、重 clone 便宜」不成立：它們用 answers/變數重新渲染舊模板，Copier 文件明列外部資源消失、extension 不相容等重建失敗情況；對應我們，#14 引入變數後 (iii) 要同時存變數、新版 vendor_kit 要能解析舊 dist 的 init.toml。
- 「dpkg 只存 md5 所以只能說改過/沒改」太窄：dpkg 用舊版 hash 分別判斷本地與新版是否變動，足以做四格判斷（不動/留使用者/裝新版/詢問）；不足的是無法還原舊內容與顯示逐行差異。另外 hash 存在 status 的 Conffiles 欄位，不是 *.conffiles 清單。
- 「進 git 的舊版副本 = ucf 做法」只對一半：ucf 確實快取完整舊內容＋diff3，但存在系統狀態目錄，不是專案內受 git 管理，不能拿它證明分支/PR/回退行為。
- 「容器內沒 3-way 工具要帶 merge3 或 git」不是 C 的核心缺點：merge3 是 GPL-2.0-or-later（來源清單沒標）；真 diff3 用 difflib 自寫約 100–150 行即可。C 的真正問題只有違反「不改使用者檔」。
- 「兩邊都改＝衝突」、「兩份二方 diff 取 hunk 交集」錯：同值修改結果一致、不同行修改也可能語意矛盾；hunk 含上下文、插入是零長度範圍、行號要投影到舊模板；difflib 沒有三方 API。
- Yeoman 選項漏了 r（reload），且 force 會跳過詢問；不是穩定契約。
- Rails 不「依賴」RailsDiff（那是獨立的跨版本產出庫）；Thor 逐檔互動不等於內建舊模板基準。
- Projen 是「多數」產生檔唯讀，不是全部永遠覆寫；Nx migration 不是模板三方比較前例。
- Cookiecutter #784 只證明有人用 template branch 保存產生結果再 merge；「官方拒絕 update 的完整理由」與「Copier 因此誕生」未經查證。
- 「前例沒人這樣做」應改成「本次查閱未找到」；HTTP 200 只代表網址可存取；agy 本次未成功執行，附件不能當 Gemini 的結論。
- 對 (iii) 的批評「舊 image 必被刪除、pull 比 clone 慢」無據：notes §5/§6 已決定保留被引用的 image；要補的是保留政策是否納入基準 metadata 的引用。
- 方案 A 不是「零成本」，是「新增成本最低」；且現 proto 對新版新增的檔（使用者沒有時）什麼都不印。
- 三方的實作前提不只「容器內只有標準庫」：主機有 git，使用者自己在主機 `git apply` 工具輸出的 patch 是一條可能合規的路，前例研究沒考慮。

## 最終建議
#11 定案：採 B（三方比對、只顯示、不寫回）。基準存 `.vendor_kit/base/<name>/` 進 git，內容是渲染後的初始檔副本＋metadata（image ref/digest、每檔 sha256、展開後 src→dest 對應、schema 版本）；為此必須先改 notes §12/第 161、263 行的「`.vendor_kit/` 整個換新」為「只換程式檔（vendor.just/tools.just/.stamp），base/ 是持久狀態不動」。init 從第一版就寫基準（不管三方何時上），否則之後所有已 init 專案都沒基準。更新基準用獨立指令 `just accept <name>`，語意是「全部已採納或明確拒絕」，寫入來源是剛檢視的新版模板；diff 結尾只印提示不詢問（`docker run --rm` 無 TTY，且要保持可管線）。缺基準時退回二方並明確標示「無基準，這是本地相對新版的差異」。不做 (iii) 舊 image 自動重取；若日後要，當明確執行的復原功能。C 不採，若日後想自動合併，放進 #10 `just upgrade --migrate` 的明確 opt-in。分期：第一版 = 檔案層級分類（沒人改／只有工具改／只有你改／兩邊都改／已套用相同內容）＋兩份 B→N、B→U diff，行級只標「可能重疊」，處理新增/移除檔（取新舊 init.toml 聯集）；第二版 = 自寫真 diff3（difflib，附 unit test，測試要含 codex 的三個陷阱：上下文重疊、零長度插入、行號投影），再視使用者對合規邊界的答覆決定要不要加 `--patch` 合併提案輸出。

## 要問使用者
- §12「vendor_kit 升級時整個 .vendor_kit/ 換新」可以改成只換程式檔、base/ 豁免嗎？base/ 要不要納入 .stamp 的 verify 印記（納入 = 人不能手改基準；不納入 = 可手改但不受保護）？
- init 對「已存在、被跳過」的檔（#7 遷移的 15 個 repo）要不要也寫基準？寫的話基準 = onboarding 當時的模板，diff 會把「你改了」算成相對那份模板；不寫的話那些檔永遠只有二方。
- accept 的語意採「全部已採納或明確拒絕」（有待辦就不推進）可以嗎？粒度要整個工具一次，還是可逐檔 `just accept <name> Dockerfile`？
- 「工具不改使用者檔」的邊界：`just diff --patch` 印合併提案、使用者自己在主機 `git apply`，算合規嗎？整條 `just diff` 前面 `_ensure` 會先 install 工具檔，這算不算「diff 不改檔」的例外？
- 第一版只做檔案層級分類＋兩份 diff、行級只標「可能重疊」，可以接受嗎？還是要求第一版就做真 diff3？（影響 test_diff.py 範圍與鏡射檢查）
- `just diff` 要不要有 exit code 語意（0 無差異 / 1 工具有改動 / 2 有衝突或可能重疊）給 CI / Renovate PR 用？要的話 `_ensure` 失敗碼要另訂。
- #14 模板變數：基準存「渲染後」內容定案嗎？專案之後改變數（例如改名）時，基準照舊比對還是重渲染？
- 兩個工具 init 到同一 dest（.gitignore、hooks）時，擁有權與基準歸屬怎麼定？要不要在 init 直接禁止撞路徑？
- 第一版支援哪些檔案型態？目錄展開、symlink、可執行權限、二進位、非 UTF-8 是否先一律標「無法比對」？
- 回退時只 revert `.version` 是否足夠，還是要一起回退 base/？（回退 .version 不保證恢復原本的差異報告）