# 剩餘五題 Q5–Q9 —— 雙軌分析（2026-09-18）

狀態：**草案，待使用者拍板**。

## 一致
- Q5 採 (1)：由有推送權限的維護者在本機接手（跑 upgrade -y、commit、push），CI 只驗證不寫入；(2) CI bot commit 與 (3) 只鎖版本 兩者都不採。理由一致：不需要 bot 寫權限、GitHub/GitLab 通吃、符合「自動化只碰不進 git 的東西」。
- Q5 兩邊都指出：「baseline 落後 → CI 紅燈」目前不是既定事實。我另查 dist_distribution_notes.md #15 D 已寫「baseline 落後或超前 .version 都是合法中間狀態，CI 只警告不紅」，所以 (1) 的流程現在沒有觸發點，要另外定規則。
- Q6 兩邊都不同意我方傾向 (c)，改採 (a)「只 warn、工具改設計」。理由一致：(c) 等於偷改「既有檔不納管／永不覆蓋／永不刪」的所有權規則；標記區塊要做對需要一整套 managed-block 協定（舊區塊基準、手改判定、重複/破損標記、remove 保留），不是加一個 init.toml 欄位。
- Q6 兩邊都要求 warn 訊息必須列出「工具想加什麼、人要怎麼手動加」，不能只說「已存在，跳過」。
- Q7 採 (c)：引擎 image 公開、工具自決、認證是主機/CI/Renovate 各自的事，vendor_kit 不引進 credential helper。兩邊都提醒主機 pull、CI pull、Renovate 查版本是三套獨立認證，要分別寫清楚。
- Q8 維持 just ≥ 1.33.0，不降也不升；提高到 1.40 沒有具體功能收益。兩邊都要求以 1.33.0 實跑完整 fixture（含 fresh clone、optional module 缺檔、巢狀模組、非根目錄呼叫、自身升級停下、amd64/arm64/WSL2）後才算定案。
- Q9 採 (1)：自身升級後停下、印明確訊息、退出 1、要求重跑；不做 recipe 內 exec 重跑。兩邊都同意：recipe 內 exec 只取代該行 shell，舊父 just 會用舊定義續跑造成重複執行；透明續跑只有 gradlew 式外層 wrapper 能做，但違反「主機只需 docker+git+just」。
- Q9 兩邊都要求：更新檢查必須在任何有副作用的動作之前；停下前一次把薄殼 + gen 全部重寫完，重跑不得再停第二次；成功後才寫 stamp。

## 分歧與取捨
### Q5 (4) Renovate postUpgradeTasks 是否列入方案
- Claude：列為自架 Renovate（GitLab 必然自架）時的可選加速，條件：allowedCommands 由執行端允許、命令直接用凍結的 bootstrap 契約 docker run …、Renovate 環境要有 docker、fileFilters 涵蓋路徑；衝突時退回 (1)。
- codex：不合限制：同樣違反「自動化只碰不進 git 的東西」，且允許 shell 命令不代表有 docker、registry 認證和安全隔離。
- 取捨：採 codex 的保守立場當第一版：契約只寫 (1)，(4) 降為文件附註「自架 Renovate 可自行加 postUpgradeTasks，vendor_kit 不出貨 preset 片段、不承諾支援」。理由：兩邊對「自動化不改需提交檔案」的解讀一致，(4) 本質上就是 bot commit，只是換 Renovate 做；而 upgrade.md C-6 若已記 (4)，應改成附註而非契約。

### Q9 (2) 是「做不到」還是「不值得」
- Claude：在「_ensure 是相依」模型下結構上做不到：just 沒有取原始 argv 的內建、recipe 內 exec 會雙重執行。
- codex：並非做不到：外層 launcher 持有 argv 就能可靠重啟（2′），只是不值得。
- 取捨：兩邊其實不衝突，只是切的範圍不同：recipe 內 exec 做不到（雙方同意），外層 wrapper 做得到但違反主機三工具原則（雙方同意）。契約措辭用「同一次 just 呼叫內不會看到新 recipe；不提供自動續跑」即可，不需寫「做不到」。

### Q6 warn 之後是否算成功（退出碼）
- Claude：warn 並列出內容即可（沿用 adopted=false 行為）。
- codex：若缺的條目影響必要功能（例如 .dockerignore 排除 build context），不能宣稱成功，應非零退出。
- 取捨：採 codex：把初始檔在工具 init.toml 分成 required / optional；required 目標已存在且內容不含工具需要的條目 → 退出 1 並印清單；optional → 只 warn。這也給工具作者壓力去用巢狀 .gitignore 等替代路徑。但注意 codex 的更正也對：.vendor_kit/.gitignore 只管該目錄下層，根層產物（如 build/）和 Docker context 排除仍需人手動加，所以 required 這條路要存在。

### Q7 (b) 一律私有是否符合限制
- Claude：不符：bootstrap 第一次拉引擎前必須 docker login，每台機器都要放 PAT。
- codex：符合，但首次啟動與 CI 都需認證準備。
- 取捨：雙方最終都不選 (b)，分歧只是「合不合限制」的評分，對結論無影響。取 Claude：bootstrap 免登入是既定目標，(b) 直接違反。

### Q8 逐功能最低版本表的可信度
- Claude：已對 changelog 逐項查證，並實測 1.53 下 --list-submodules 單獨用會 exit 2；[group] 放 mod 上要 1.33（#2263）；Ubuntu 24.04 = 1.21.0、26.04 = 1.45.0、Debian 13 = 1.40.0。
- codex：本次離線，所有版本號標「依記憶／不確定」。
- 取捨：採 Claude 的表（有出處），但仍照兩邊共識：定案前用 1.33.0 實跑 fixture。另外把 Claude 查到的「[group] 放 mod 上 1.33 才有」寫進 ADR-0002，這是 1.33 這個數字的真正來源，目前 ADR 只寫 1.27 會誤導。

## brief 事實錯誤（查證）
- Q5「要設定 Renovate 不 rebase 掉人的 commit」：不需要設定。Renovate 預設（gitIgnoredAuthors 文件）就把「別的作者推過 commit 的分支」視為已修改、不再 commit；會丟人 commit 的是人自己勾 PR 的 rebase/retry 核取方塊、或把作者列進 gitIgnoredAuthors。副作用：該分支之後也不再自動更新到更新版、衝突不自動 rebase。codex 離線只標「不確定」，Claude 有引文，採 Claude。
- Q5「PR 作者本機補合併」：Renovate PR 作者是 bot，改稱「有該分支推送權限的維護者接手」（codex 更正，正確）。
- Q5「CI 的 sync（frozen）會判 baseline 落後讓 PR 紅」：不是既定事實。dist_distribution_notes.md #15 D 現行決議是「baseline 落後或超前都是合法中間狀態，CI 只警告不紅」；且 sync 依定義不改需提交的檔。要讓 (1) 有觸發點，必須改 D 或另加 `upgrade --check` 規則。
- Q5「upgrade <repo> -y 會做合併 + 推 baseline」：與 notes #15 B「upgrade 只改 .version 那行就停、不裝、不 diff」矛盾，CONTEXT.md 標為待拍板 (d)。(1) 的流程依賴 upgrade 會做三方合併，這個前提要先定案。另 codex 提醒：此流程的 upgrade 必須合併到 PR 已鎖定的版本/digest，不能另抓最新。
- Q5「Renovate 只改 version.toml 一行」是我方預期配置，不是保證；同一 PR 可能同時更新多個相依或 tag+digest（codex）。「引擎在第一行」也不對：TOML 不依賴行序，要讀指定 key（codex）。
- Q5「postUpgradeTasks 必須 self-hosted」：不精確。Mend 託管付費方案也能開、免費方案封鎖；allowedCommands 是 global-only 由執行端設，repo 的 renovate.json 不能自行授權；另需 Renovate 環境有 docker、fileFilters 涵蓋路徑（Claude 有引文；codex 記憶一致）。
- Q6「標記區塊 append 是 conda init / nvm 的做法」：只有 conda 用標記區塊；nvm 是 grep 後直接 append 三行、無標記；oh-my-zsh 是整檔取代並備份。正式的「標記區塊 append/替換/移除」前例是 Ansible blockinfile。兩邊一致。
- Q6「.vendor_kit/.gitignore 可代替根層 ignore 需求」：只管該目錄及下層，根層產物與 Docker build context 排除都管不到（codex）。Claude 提的替代：巢狀 .gitignore（工具自建目錄）、<Dockerfile>.dockerignore（BuildKit，docker 19.03 需 DOCKER_BUILDKIT=1，待驗證）、子目錄 .editorconfig。
- Q6「三個檔幾乎必存在」：沒有專案樣本支持（codex）；但不影響結論，反正要有安全行為。
- Q6「宣告 mode=append 就符合不變量」：工具作者宣告 ≠ 使用者授權；且 ADR README 已記「不碰使用者 .gitignore」，(b)/(c) 都等於推翻既有決議（兩邊一致）。
- Q7「公開/私有可隨時切換」：GitHub 文件明寫 package 公開後不能改回私有；「工具自決」實際是「自決且不可反悔」（Claude）。「public repo = image 公開」也不成立，兩者分開設定與驗收（codex）。「私有一定要 credential helper」與「GitLab CI 一定要 bot PAT」都是常見途徑不是唯一途徑（codex）。
- Q8「[group] 是 1.27」：recipe 上 1.27.0，但放在 mod 上要 1.33.0（#2263）；tools.just 是對模組分組，所以 1.33 下限的來源是這條。「Ubuntu 22.04/24.04 apt 版本」：22.04 沒有 just 套件、24.04 = 1.21.0、26.04 = 1.45.0、Debian 13 = 1.40.0（Claude 查 Launchpad / sources.debian.org）。另：≥1.40 時 `--list-submodules` 必須與 `--list` 併用。
- Q8「justfile_directory() 一定回到專案根」：在 import/module 檔內是所屬 justfile 的位置，生成檔在 .vendor_kit/ 時要實測（codex）。
- Q9「(2) 的風險是無限迴圈 guard、argv 還原、環境變數」：問題不是風險而是 recipe 內 exec 結構上做不到（父 just 用舊定義續跑 → 雙重執行；just 無取原始 argv 的內建）；外層 wrapper 可做但違反主機三工具原則。
- 契約措辭：「永不覆蓋」與已同意的三方合併字面矛盾，建議改為「不得不經比對直接覆寫；允許已授權的合併」；根 justfile「移除完全相同行」是特例，不能推及所有初始檔（codex）。

## 最終建議
| 題 | 裁定 | 前提／必要條件 |
|---|---|---|
| Q5 | **(1) 維護者本機接手**（upgrade -y → commit → push），CI 只驗證。(2)(3) 不採；(4) 只作文件附註（自架 Renovate 可自行加 postUpgradeTasks，vendor_kit 不出 preset、不承諾支援）。 | ① 先定 upgrade 語意：notes #15 B「只改 .version 就停」與 (1) 需要的「合併 + 推 baseline」矛盾，待拍板 (d) 要先解；且此流程要合併到 PR 鎖定的版本/digest。② 改 notes #15 D：CI 對「baseline 落後 version.toml」由「只警告」改為退出 1 並印「請在本機跑 just vendor_kit upgrade <repo> -y 後 commit/push」（超前仍只警告）。③ Renovate preset 用 prBodyNotes 放同一條指令與警語「推 commit 後不要勾 rebase/retry」。④ 不設 gitIgnoredAuthors、不改 rebaseWhen。⑤ 引擎自身那行同流程。⑥ 引擎版本讀 TOML key，不靠行序。 |
| Q6 | **(a) 只 warn + 明列替代路徑**，(b)(c) 不進第一版。 | ① 工具契約 + check.sh --dist lint：初始檔禁止以根 .gitignore/.dockerignore/.editorconfig 為目標，改用巢狀 .gitignore、<Dockerfile>.dockerignore、子目錄 .editorconfig。② warn 印出工具想加的條目全文與手動加入方式。③ init.toml 分 required/optional：required 目標已存在且缺條目 → 退出 1；optional → warn（吸收 codex「不能宣稱成功」）。④ 驗證 BuildKit 專屬 dockerignore 在 docker 19.03 可用。⑤ 若日後重開 (c)：先改 ADR「不碰使用者 .gitignore」決議，並採完整 blockinfile 級協定。 |
| Q7 | **(c) 引擎公開、工具自決、認證是主機的事**。 | ① 引擎與 vendor_kit 自家工具 image 公開，文件註明「公開後不可改回私有，不確定就先私有」。② repo 公開 ≠ package 公開，分開設定與驗收；驗收引擎匿名 pull。③ 錯誤訊息寫「不存在或無權限（GHCR 未登入一律 denied），私有請先 docker login <host>」。④ 明確區分主機 pull、CI pull、Renovate 查版本三套認證；CI 樣板預留 docker login 步驟；hostRules 依 host 不寫死 ghcr.io。⑤ 不要求 credential helper。 |
| Q8 | **維持 ≥ 1.33.0**，驗收後才算定案。 | ① ADR-0002 補正：1.33 的來源是「[group] 放在 mod 上」（#2263），不是 1.27。② 腳本一律 `just --list --list-submodules`。③ CI 矩陣 1.33.0 / 1.40.0 / 最新，跑完整 fixture（fresh clone、optional 缺檔、巢狀模組、非根目錄呼叫、自身升級停下、amd64/arm64/WSL2）。④ ADR 列禁用較新功能（[working-directory] 1.38、require()/which() 1.39、[default] 1.43、[script] 1.44、[parallel] 1.42、set unstable、跨模組相依 a: sub::r）並由 lint 擋。⑤ 實測 justfile_directory() 在 .vendor_kit/ 內生成檔的行為。⑥ bootstrap 檢查 just ≥ 1.33.0 並印下載指令。 |
| Q9 | **(1) 停下、退出 1、要求重跑**；契約寫「同一次 just 呼叫內不會看到新 recipe；不提供自動續跑」。 | ① 更新檢查在任何副作用之前；停下前一次重寫完薄殼 + gen（世代目錄切換），成功後才寫 stamp，重跑不得再停。② 重寫後印記仍不符 → 報「重寫失敗」不再叫人重跑。③ _ensure 加 [no-exit-message]，第一行固定可 grep，內容含「已更新 vendor_kit 舊→新，請重跑：<指令>」。④ CI 先明跑 `just vendor_kit sync`。⑤ stamp 要含有效引擎身分（含 dev 本機可變 tag 重 build 的情況）。 |

兩邊真正的分歧只有 Q5 (4) 的定位與 Q6 warn 後的退出碼，上表已各採保守方。其餘四題與我方傾向一致；Q6 兩邊一致反對我方傾向 (c)。

## 要問使用者
- （兩邊一致才問）Q5 前提：upgrade 語意要定成哪一版？notes #15 B 是「只改 .version 那行就停」，但 (1) 需要 upgrade -y 直接做三方合併並推 baseline。要改 B 嗎？
- （兩邊一致才問）Q5：同意把 notes #15 D 改成「baseline 落後 version.toml → CI 退出 1 並印指令；超前仍只警告」嗎？不改就沒有觸發點。
- （兩邊一致才問）Q5：baseline 存在哪裡、乾淨 clone 怎麼拿到？以及衝突退出 2 後 baseline 是否推進、未解決狀態怎麼在 CI 被辨識？這是 (1) 能否在 CI 驗證的前提。
- （兩邊一致才問）Q6：base 現在要送進下游的 ignore 條目有哪些？哪些是必要功能（例如 Docker context 排除）、哪些只是便利？決定 required/optional 的分法，以及 (a) 是否零成本。
- （兩邊一致才問）Q6：接受把「初始檔禁止以根 .gitignore/.dockerignore/.editorconfig 為目標」寫進工具契約並由 check.sh --dist lint 擋嗎？
- （兩邊一致才問）Q7：vendor_kit 自家工具 image 是否一律公開？公開不可逆，發布前要決定。
- （兩邊一致才問）Q8：CI 矩陣三版（1.33.0 / 1.40.0 / 最新）與禁用功能清單進 ADR-0002 並由 lint 強制，可接受嗎？
- （兩邊一致才問）Q9：停下時要印使用者原本的完整指令（工具 recipe 把名字傳給 _ensure），還是統一印「請重跑上一個指令」？並確認：一次 just 呼叫多個 recipe 時，重跑整句是否可接受。
- （兩邊一致才問）主機「只需 docker、git、just」是否包含 bootstrap 與 just 安裝不得依賴 curl/wget/解壓工具？影響 install.sh 的交付方式。

---
## 附：Claude 分析原文
codex 與我方傾向比對：Q5 同意、Q6 不同意（改 a）、Q7 同意、Q8 暫定 1.33 但強調未查證、Q9 同意。注意：codex 本次離線（sandbox 啟動失敗、無網路），所有版本號與 Renovate/GitLab 行為均標示「依記憶／不確定」，未核對官方文件。

| 題 | 裁定 | 理由 | 實作必要條件 |
|---|---|---|---|
| Q5 | (1)，改稱「維護者本機接手」（非「PR 作者」，作者是 bot） | 同意原傾向；符合自動化限制且不依賴 CI 平台 | upgrade 在此流程必須合併至 PR 已鎖定的版本／digest，不得另挑新版；逐檔報告；衝突回 2；以實際 repo 驗證人工 commit 後 Renovate 行為 |
| Q6 | (a)，不同意目前的 (c) | 現行 (c) 偷渡初始檔所有權與刪除規則的變更；工具作者宣告 ≠ 使用者授權 | warn 要列出具體缺少條目及人工加入方式；可隔離產物放進自有目錄；若缺失影響必要功能應非零退出。未來若重開 (c)，需完整 managed block 協定（保存舊區塊基準、人工修改時合併或拒絕、重複／破損標記時停止、remove 預設保留） |
| Q7 | (c) | 同意原傾向；把核心可取得性與工具存取政策分開 | 引擎匿名拉取要驗收；沿用主機 Docker 認證；不要求 credential helper；明確區分主機、CI、Renovate 三處 registry 認證；repo 公開 ≠ package 公開，要分別設定驗收 |
| Q8 | 暫定 ≥1.33.0，驗收後才成為已證實下限 | 沒有可靠證據支持現在降版或升版；1.33.0 是待驗收的工程選擇，非由版本表推導 | 取得官方 changelog／對應 tag 文件逐項核對；以 1.33.0 跑全部實際入口及平台 fixture（fresh clone 無 gen、optional import/module 缺檔與存在、巢狀模組清單、含空白參數、非根目錄呼叫、自身升級後停止、amd64/arm64/WSL2）；有失敗再調整 |
| Q9 | (1)，更新後停下、回 1 | 同意原傾向；目前 just 入口不值得承擔自動重播風險；(2) 並非做不到（外層 launcher 持 argv 可做），但不值得 | 所有受影響操作前先檢查；只自動重建 ignored 產物；成功完成後才寫 stamp；顯示重跑指令及版本；引擎版本以 TOML key 讀取而非「第一行」 |

Q8 逐功能最低版本（codex 離線盤點，非查證結果）：
| 功能 | 首次提供 | 可信度 |
|---|---|---|
| mod | 1.19.0（依記憶） | 1.31.0 穩定化（依記憶，未核對） |
| mod? | 不確定 | 不能因 mod 在 1.19 出現就推定 optional 同版 |
| import? | 不確定 | 須單獨查 optional import |
| [group] | 1.27.0（依記憶，與 brief 相符） | 未核對 |
| set positional-arguments | 不確定 | 須查該 setting |
| justfile_directory() | 不確定 | 另需驗證 imported/module recipe 中的路徑語意 |
| [no-cd] | 不確定 | 須確認首次 release |
| --list-submodules | 不確定 | mod 穩定化不代表此旗標同時存在 |
| set allow-duplicate-recipes | 不確定 | 須確認首次 release 及 import 順序下的覆蓋規則 |

Ubuntu apt 差距（依記憶、不確定）：22.04 官方套件庫未提供 just；24.04 約 1.21.0 系列，若成立則低於 1.33.0。

## 附：codex 分析原文
| 題 | 裁定 | 理由 | 實作必要條件 |
|---|---|---|---|
| Q5 | **(1) PR 作者本機補合併**為預設；**(4) postUpgradeTasks** 作為自架 Renovate（GitLab 必然）時的可選加速，(2)(3) 不採。與我方傾向一致，但把 upgrade.md C-6 的 (4) 併進來。 | (1) 不需要任何 bot 寫權限、GitHub/GitLab 通吃、不受 #25 影響；Renovate 預設就不再碰有人推 commit 的分支。(2) 需 PAT/App token 或 GitLab project token 且 bot commit 會被 rebase 洗掉，違反「自動化只碰不進 git 的東西」。(3) 讓主分支處於工具新版+初始檔舊版的不一致狀態且無人通知。 | ① 契約明寫 CI 檢查規則：`sync`（或 `upgrade --check`）偵測 baseline 落後於 version.toml → 退出 1、印出「請在本機執行 `just vendor_kit upgrade <repo> -y` 後 commit/push」；② Renovate preset 用 `prBodyNotes` 放同一條指令與警語「推了 commit 後不要勾 rebase/retry，會丟掉你的 commit；請儘快合併」；③ 引擎自身那行同樣流程（tracked 薄殼若變也由人 commit）；④ (4) 的條件：allowedCommands 允許、命令直接用凍結 bootstrap 契約 `docker run … --self <新 image> upgrade <repo> -y`（Renovate 端不裝 just）、Renovate 執行環境有 docker、fileFilters 含 `.vendor_kit/**` 與 `**/*`、失敗（衝突退出 2）時退回 (1)；⑤ 不設 gitIgnoredAuthors、不改 rebaseWhen。 |
| Q6 | **(a) 只 warn + 明列替代路徑**；**不同意 (c)** 進第一版，(b)/(c) 降為 v2 待議。 | isolation.md 已定案「禁止初始檔機制以 .gitignore 為目標」，(c) 等於推翻；且三個檔都有不需 append 的替代：巢狀 `.gitignore`（工具自己建的目錄）、`.vendor_kit/.gitignore`、`<Dockerfile>.dockerignore`（BuildKit）、子目錄 `.editorconfig`。conda init 改 rc 檔是被抱怨最多的行為；區塊語意（手改、重複、移除）需要一整套 blockinfile 級規則，不符第一版「指令極少」。 | ① 工具契約 + `check.sh --dist` lint：初始檔清單禁止根 `.gitignore`/`.dockerignore`/`.editorconfig`；② add 遇已存在檔的 warn 要印出工具想要的內容（cache 內路徑 + 建議手動加入的行）；③ 驗證 Dockerfile 專屬 ignore 在 docker 19.03 + DOCKER_BUILDKIT=1 可用（不行就把 .dockerignore 案例列為已知限制）；④ 若 v2 要做 (c)：先改 isolation 決議、採 Ansible blockinfile 語意（固定 marker 含工具名、marker 不完整就報錯不插入、區塊內三方合併、remove 只刪區塊且詢問）。 |
| Q7 | **(c) 引擎公開、工具自決、認證是主機的事**。與我方傾向一致，加兩條補充。 | 引擎公開是 bootstrap 免登入的前提；工具的可見性是各 repo 的政策，契約只承諾「主機 docker 能 pull 就能用」。GHCR 公開 package 匿名 pull 免認證（GitHub 文件），私有則各處（主機 login、GitLab CI PAT、Renovate hostRules、容器內 upgrade token）都要配，這些都已在 upgrade.md 列過。 | ① 引擎與 vendor_kit 自家工具 image 設公開，並註明「公開後不可改回私有」（GitHub 文件明寫），工具作者不確定就先私有；② 錯誤訊息寫「image 不存在或無權限（GHCR 未登入時一律回 denied），私有請先 `docker login <host>`」，不要承諾能區分兩者；③ ci_bridge #25 的 CI 樣板預留 `docker login` 步驟（secret 變數，缺就跳過並印 warn）；④ Renovate preset hostRules 依 host 設 token，不寫死 ghcr.io；⑤ 跨 org 的 base-dist 若私有，下游 GITHUB_TOKEN 拉不到，文件要寫要 PAT。 |
| Q8 | **維持 1.33.0**。與我方傾向一致（查證後確認）。 | 逐功能最低版：`mod` 1.19（unstable）→1.31 穩定；`mod?`/`import?` 1.21；`[group]` recipe 1.27、**放 `mod` 上 1.33**；`set positional-arguments` 0.9.1；`justfile_directory()` 0.5.4；`just_executable()` 0.8.6；`quote()` 0.10.4；`[no-cd]` 1.9；`[private]` 1.9；`--list-submodules` 1.28（1.40 起須與 `--list` 併用）；`set allow-duplicate-recipes` 0.11.1；`[no-exit-message]` 1.7。1.33 也含子模組 backtick/shell() 工作目錄修正（#2285）。apt 現況：Ubuntu 22.04 無、24.04 = 1.21.0、26.04 = 1.45.0、Debian 13 = 1.40.0；提高到 1.40 沒有具體新功能收益。 | ① 所有腳本一律 `just --list --list-submodules`；② CI 矩陣 1.33.0 / 1.40.0 / 最新 三版跑完整 fixture 流程；③ ADR 列「禁用的較新功能」清單（`[working-directory]` 1.38、`require()`/`which()` 1.39、`[default]` 1.43、`[script]` 1.44、`[parallel]` 1.42、`set unstable`），`check.sh --dist` lint 擋；④ 契約禁止跨模組相依 `a: sub::r`（1.42 才有且 1.42.0–1.42.2 有工作目錄 bug）；⑤ install.sh/bootstrap 檢查 `just --version` ≥ 1.33.0 並印出下載指令。 |
| Q9 | **(1) 停下、退出 1、要求重跑**；(2) 判定為結構上做不到，不只是不值得。與我方傾向一致。 | just 啟動時整份解析、無內建取原始 argv；recipe 內 exec 只取代該行 shell，父程序會用舊定義續跑造成雙重執行；唯一乾淨的透明續跑是 gradlew 式 wrapper，違反「主機只需 docker+git+just」。 | ① 一次停下前完成薄殼 + gen/ 的全部重寫（世代目錄切換），重跑不得再停；② 重寫後印記仍不符 → 報「重寫失敗」（用帶印記的剛重寫標記檔判斷），不再叫人重跑；③ `_ensure` 加 `[no-exit-message]`，訊息第一行固定可 grep，內容含「已更新 vendor_kit <舊>→<新>，請重跑：<指令>」；④ CI 規則：先明跑 `just vendor_kit sync`（終點步驟、不需重跑），工具 recipe 之後不會再停；⑤ 契約明寫「同一次 just 呼叫內不會看到新 recipe」，避免之後有人再提 re-exec。 |