# devmode

## 一致
- 方案 (b) `upgrade --local` 出局：兩邊都認為它挪用了 upgrade 的「換到已發佈新版」語意（base 是 apt 對齊，一個動詞一個動作），沒有對稱的退出動作，而且既定規則是「.version.local 有 entry 就啟用」，再加一個 flag 當開關會出現兩套啟用依據。
- 方案 (c) 純手寫不是獨立方案，而是 (a) 的底層：不管有沒有指令，`_ensure` 都必須讀 .version.local、做路徑驗證、雙 mount、警告。指令只是「會做驗證的寫檔 sugar」，手寫檔案與打指令效果必須完全相同。
- agy 的 14 列前例表大半是「有本地路徑機制」而非「有不進 git 的覆蓋檔」，且 A/B/C 回答的是上一題「檔案放哪」，不是本題「指令長什麼樣」；不能直接套用它的結論。
- agy 的 Option D（加環境變數優先層）違反使用者已定的硬約束（不用環境變數，出問題要能從檔案追），直接排除。
- Terraform dev_overrides 的描述錯：官方文件明說 `terraform init` 仍會選正式 provider 寫 lockfile，只有 plan/apply 等操作改用本機來源；不是「跳過 init、完全繞過 lockfile」。
- Go/Cargo 的引用被加料：Go 官方是「通常不建議提交 go.work」並列出例外；Cargo 文件雖說 config 通常不進版控，但接著建議能用 Cargo.toml `[patch]` 就優先用它——agy 只引前半句。
- 「.gitignore 就零誤提交風險」不成立：筆記 §2 已把 `.gitignore` 定為 init.toml 類（init 建一次、之後歸使用者、工具不改），與 §8 #6「bootstrap 寫進 .gitignore」互相矛盾；既有 15 個 repo 都已有 .gitignore，bootstrap 不會動它。`dev` 指令必須自己檢查（`git check-ignore`）。
- 決議紀錄的 mount 寫法 `-v <path>/dist:/dist:ro` 不完整：至少缺 init.toml（兩邊都指出），Claude 進一步指出原型 image 佈局是 `/dist/files` + `/dist/init.toml` + `/dist/VERSION`，直接掛到 `/dist` 會讓三者都找不到。要嘛雙 mount，要嘛掛 repo 根並讓 dist_reader 支援 repo 佈局。
- dev 模式下 `accept` 第一版應拒絕：否則會把未發佈、不可重現的模板存進 baseline 並進 git，metadata 只記得 `path:../tool`。正常流程是先發佈正式版→undev→升 pin→diff→accept。
- 一般 `upgrade` 遇到被 .version.local 覆蓋的工具應明確報出並跳過，不能悄悄改了正式 pin 卻沒真的測到。
- dev 模式每次進 ensure 都重新完整同步 dist、不做 mtime 捷徑、來源缺失就中止不偷用舊快取；verify 跳過但每次向 stderr 印醒目警告（工具名、來源路徑、「完整性驗證已跳過」）。
- 路徑基準 = 相對專案根（.version.local 所在處）；用 `--mount type=bind,readonly` 而非 `-v`，因為 `-v` 對不存在的來源會自動建一個 root 擁有的空目錄、靜默失敗；主機端先驗證路徑存在。
- just 參數轉送要處理含空白的路徑（`set positional-arguments` + `"$@"`），base 現在用 `{{args}}` 未加引號的做法不能照抄。
- agy 的示範實作不能直接用：`$PWD` 不是專案根、`vendor_kit:latest` 沒鎖版本、主機 realpath 是未聲明依賴、mtime 判斷違反「每次同步」決策。

## 分歧（含判斷）
- 停用指令的形式：`undev <name>` 獨立動詞，還是 `dev <name> --off`：傾向 Claude。筆記 §11 原文是「給路徑 vs 選項式」，爭點是「路徑要不要當 positional」，不是「要不要兩個動詞」；`--off` 這種「一個動詞靠 flag 反轉語意」在 base 裡沒有前例（base 是 `completions install|uninstall` 分兩個子動詞），反而離 base 更遠。undev 已在決議紀錄和 bootstrap 產出清單裡。但這一點終究是使用者對「用 opt」的定義，要問。
- 印記第一行寫什麼：`dev:<路徑>` 還是 `--self` 收到的原字串 `path:<路徑>`：採 Claude。issue #23 契約是「第一行 = --self 原字串」，一個地方寫 `path:` 另一個寫 `dev:` 是同一資訊兩種拼法，一定會有人在啟動器裡「順手修好」相等比較然後 dev 模式就不重裝了。統一寫 `path:<原字串>`，dev 分支的判斷明寫在 `_ensure`（有效版本以 path: 開頭 → 一律 install、不 verify），codex 的「以有效設定為準、不信 stamp」在這做法下自然成立。
- `--path` 用 flag 的理由，以及是否納入 `--image <本地 tag>` 第二來源：第一版只做 `--path`，`--image` 留成擴充點但不實作。Claude 的「flag 能擴充」是選 flag 的好理由，但 codex 說得對：覆蓋 vendor_kit 自身會連動 bootstrap 重寫 `.vendor_kit/`，跟「覆蓋一個工具的 dist」是不同問題，不該在本題順便定。要問使用者是否要把它列成後續題。
- `.gitignore` 未忽略 .version.local 時，`dev` 是警告後繼續還是拒絕：採 codex 的「拒絕」為預設，因為這是唯一能真正擋住誤 commit 的點，而且修法只要一行。但 Claude 的 `.git/info/exclude` 是好的折衷：它不是使用者檔、不進 git、工具寫它不違反「不改使用者檔」——建議 `dev` 檢查到未被 ignore 時，自動寫 `.git/info/exclude` 並印一句說明，這樣既不改 .gitignore 也不用拒絕。CI 防呆兩邊不衝突，一起採。要問使用者接不接受工具寫 `.git/info/exclude`。
- 誰寫 .version.local：主機 bash 還是容器：兩邊其實一致：容器寫、install 成功才寫。codex 補的順序約束（先裝後寫、鎖內重讀）是必要的，採納；undev 反向：先移 entry 再依 .version 重裝正式版，且 undev 不得先跑一般 ensure（本機目錄已刪時會卡死）——這條只有 codex 提到，重要。

## 對前例資料的更正
- npm/pnpm/yarn 那列「link CLI 不碰 package.json」已過時：pnpm v10 起 `pnpm link <dir>` 會寫 override 進 root package.json（v11 改寫進 pnpm-workspace.yaml），都是進 git 的檔。這例子反而顯示「用指令寫覆蓋設定」是主流做法。
- Terraform：官方 config-file 頁面說 `terraform init` 仍會選一個已發佈版本寫進 lock file，只有其他操作對被覆蓋的 provider 用本機來源；不是「跳過 init、完全繞過 lockfile」。該頁也沒提 warning banner，警告來自 CLI 實作且早期 plan 不印。
- Go proposal 45713 原文只說 replace 是「提交前要記得 revert 的改動」；「antipattern」「routinely committed」「breaking CI」是 agy 加的。go.dev/ref/mod 是「一般不建議提交 go.work」並列出例外，不是無條件 gitignore。
- Cargo 文件原句是「not usually checked into source control」，但同段接著建議優先用 Cargo.toml `[patch]`、config 層 patch 只適合外部工具自動產生的情況——agy 漏掉官方其實是勸你不要靠 config 檔做 override。
- Compose override 文件只規定自動合併，沒說 override 必須不進 git；mise 說 local 設定不應提交，不等於 Git 自動忽略。「用途」與「忽略規則」是兩件事。
- Bazel「local_path_override 關掉完整性驗證、從 lockfile 剝除」、Nix「完全在記憶體」引的是總覽頁，查不到明確段落；Helm/Gradle/Dagger/Copier 四列與本題關聯很弱，屬湊數。「14 個工具一致採不進 git 的覆蓋檔」不成立，表格本身就混了 manifest、CLI 參數、symlink、venv metadata。
- 「所有本機來源都不算 checksum、改印警告」是 agy 的推論，不是前例共識；vendor_kit 跳過 verify 應列為自己的產品決策。
- Option B「zero chance of accidental commit」只在 .version.local 真的被 ignore 時成立；已追蹤的檔不受 ignore 影響；`.gitignore` 是 init.toml 類使用者檔，bootstrap 不會改既有的。
- Option D（ENV > .version.local > .version）違反使用者硬約束「不用環境變數」，排除。
- 整份報告回答的是上一題「檔案放哪」，漏掉本題最直接的形式前例：`go work use ../dir`／`go work edit -dropuse`、`npm/pnpm/yarn link <dir>`／`unlink`、`cargo add --path <dir>`、`pip install -e <dir>`、`mise use --env local`、`uv add <dir>`——全是「一對指令寫覆蓋設定」。
- 示範實作的 `-v "$LOCAL_DIST:/dist:ro"`（草稿與決議紀錄照抄）與原型 image 佈局不合（`/dist/files` + `/dist/init.toml` + `/dist/VERSION`）；另 `$PWD` 非專案根、`vendor_kit:latest` 未鎖版、主機 realpath 是未聲明依賴、mtime 判斷違反每次同步決策、`dev:` 印記前綴不符 issue #23 契約。
- 「CLI flag 無法追蹤」混淆了兩件事：單次覆蓋來源的 flag（確實追不到）與寫進 .version.local 的管理指令（有效狀態仍在檔案，符合已定方向）。

## 最終建議
採方案 (a)：`just vendor_kit dev <name> --path <dir>` 啟用、`just vendor_kit undev <name>` 停用；`--path` 用 flag 而非 positional。理由：base 的文法是「命名空間 + 動詞 + positional 物件 + 帶值 flag」（`upgrade [vX]`、`completions install --shell bash`），`dev <name> --path X` 與已定的 `accept <name>` 同構；apt 對齊要求一個動詞一個動作，所以停用用獨立動詞而非 `--off`；`--path` 用 flag 是為了未來 `--image` 等第二來源留位。但把 (c) 的原則寫進規格：`.version.local` 是唯一真相（同 .version 的 TOML 結構，有 entry 就啟用、移除就停用、空檔等於不存在、第一版只能覆蓋 .version 已宣告的工具），指令只是會做驗證的寫檔 sugar，手寫與打指令效果必須相同。\n\n定案前必修的五件事（跟指令形式無關，但原型會立刻踩到）：(1) mount 佈局改掉：`--path` 指工具 checkout 根，主機 realpath 後檢查 `<dir>/dist/` 與 `<dir>/init.toml` 存在，用 `--mount type=bind,readonly` 掛 `<dir>/dist → /dist/files` 與 `<dir>/init.toml → /dist/init.toml`（或掛 repo 根到 /src 並讓 dist_reader 支援 repo 佈局），VERSION 缺席時回傳 `--self` 字串；image 用 .version 鎖定的 vendor_kit。(2) 印記第一行放棄 `dev:` 拼法，直接寫 `--self` 收到的 `path:<原字串>`；`_ensure` 明寫「有效版本以 path: 開頭 → 一律 install、不 verify、每次完整同步、來源缺失即中止」，並向 stderr 印含來源路徑的醒目警告（非 TTY 也印）。(3) dev 模式下 `accept` 拒絕；`init` 允許但警告；`upgrade` 跳過被覆蓋的工具並提示；diff 照常三方比對並標明新模板來自 dev。(4) 防誤 commit：修正決議紀錄「bootstrap 寫進 .gitignore」（與 §2「.gitignore 歸使用者」矛盾）；`dev` 跑 `git check-ignore -q .version.local`，未忽略時寫 `.git/info/exclude` 並說明（不改使用者檔），或拒絕；啟動器在 CI 環境且 .version.local 存在時直接失敗。(5) 寫檔順序：容器內做 TOML 讀寫，鎖內重讀設定，install 成功後才寫 entry；undev 先移 entry 再依 .version 重裝正式版、不可先跑一般 ensure；只改目標工具那行不動其他 entry；entry 清空後刪檔。含空白路徑用 `set positional-arguments` + `\"$@\"`；路徑相對專案根，存使用者原字串。`--image` 與覆蓋 vendor_kit 自身另立題目，第一版不做。

## 要問使用者
- 「用 opt、不要直接給路徑」的確切意思：是只要路徑改成 `--path <dir>`（保留 dev/undev 兩個動詞）就好，還是希望只有一個動詞、用 `dev <name> --path X` / `dev <name> --off` 切換？兩位審查員在這點分歧，是本題唯一還要你拍板的形式問題。
- 停用指令名稱：保留已進決議的 `undev`，還是對齊 npm/pnpm/yarn 用 `link`/`unlink`？
- `--path` 指向工具 checkout 根（含 dist/ 與 init.toml）可以嗎？mount 要選「雙 mount 到 /dist/files + /dist/init.toml」還是「掛 repo 根到 /src、dist_reader 支援 repo 佈局」？（決議紀錄的 `-v <path>/dist:/dist:ro` 兩邊都認定是錯的）
- 印記第一行是否放棄 `dev:` 前綴、統一寫 `--self` 收到的 `path:<路徑>`？
- .gitignore 歸使用者（§2）與「bootstrap 寫進 .gitignore」（§8 #6）矛盾：要改成哪一邊？`dev` 發現 .version.local 未被忽略時，接不接受工具自動寫 `.git/info/exclude`？還是直接拒絕？
- dev 模式下 accept 拒絕、init 允許但警告、upgrade 跳過並提示——這三個預設可接受嗎？
- 啟動器在 CI 環境（CI=true / GITHUB_ACTIONS）且 .version.local 存在時直接失敗，可接受嗎？
- `--image <本地 tag>`（測 Dockerfile.dist 打包、開發 vendor_kit 自身）是否列為後續獨立題目？第一版只做 `--path`。
- 每次 just 都完整重新複製 dist（base 有幾百檔）的成本第一版接受嗎？（兩邊都建議不做 mtime 捷徑）
- 路徑含空白／符號連結要不要支援？第一版是否維持「禁 symlink」與「同步期間來源不得修改」的限制？
## 使用者定案（2026-09-17）
- 採 (a)：`just vendor_kit dev <name> --path <dir>` 啟用；`just vendor_kit undev <name>` 停用。
- 所有帶值選項同時要有短選項：`-p` = `--path`（對齊 base 的 `-t/--target`、`-s/--setup`、`-C/--chdir`）；undev 同樣對齊（若有選項也給短形式）。
- 其餘依最終建議：.version.local 是唯一真相、印記第一行寫 path:<原字串>、dev 模式一律重裝不 verify 並印醒目警告、accept 拒絕、init 警告、upgrade 跳過；dev 檢查 git check-ignore（未忽略 → 寫 .git/info/exclude，不改使用者 .gitignore）；CI 環境有 .version.local 直接失敗；mount 改掛 <dir>/dist → /dist/files 與 <dir>/init.toml → /dist/init.toml。
