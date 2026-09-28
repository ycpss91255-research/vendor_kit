# r12 codex 審查 — 第 4 組（v1p8bcc, v1p9, v1p9c, v1p10, v1p11, v1p12, v1p15, v1p15c, v1p16, v1p16c, v1p16cc）

來源：`r12_codex/out4.md`（codex exec，一次跑完，有答案；tokens used 156,912）。以下逐條整理 codex 原文，不加審查者意見。附件 L 已列的兩條 termcov（v1p10 pend 6-5、v1p12 pend 6-9）codex 未重複。

## 逐條發現

| # | 頁 id | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|---|
| 1 | v1p8bcc | x5c「刪 version.local.toml（有的話；hash 相符者）」 | A | 規格要求 uninstall 刪除 `version.local.toml`，沒有「hash 相符才刪」條件；會把仍存在的本機覆寫誤留在專案 | 必修 |
| 2 | v1p8bcc | x5ef_0「baseline/.gitkeep」 | A | 規格的 install 建空 `baseline/`，未定義 `.gitkeep` 為薄殼或自產檔；圖卻把它當 uninstall 刪除目標。應刪除此項，或先在規格明定 | 必修 |
| 3 | v1p8bcc | lx → x5y／x4x | B | 同一個 `launcher_exit` 無判斷節點卻同時連到 0 與 1，讀者無法知道依哪個狀態分流；應在寫 `launcher_exit` 前保存／判斷實際結果 | 必修 |
| 4 | v1p8bcc | x6 無分支 → x8「請自行移除 import 那行」 | F | 判斷是「沒有我們那一行」，再叫使用者自行移除該行語意矛盾；應改成「不動 justfile／該行已不存在」 | 必修 |
| 5 | v1p8bcc | x5af「薄殼五檔（保護清單內的保留）」 | F | 上游動作寫「刪 hash 相符者」，檔案框卻寫「保護清單內的保留」，同一框同時像刪除清單與保留清單。應拆成「已刪」與「保留」兩個結果 | 必修 |
| 6 | v1p8bcc | 下半部 justfile／.dockerignore 分支線 | E | 兩組回流線在中央合流、繞過多個判斷框，且 `無／否` 共用文字，使「不存在」與「使用者拒絕」難以追蹤。建議各自收斂到明確的「不動」節點後再合流 | 選修 |
| 7 | v1p9 | q9「--dry-run？」→ q9y | A | 規格定義 `--dry-run` 是 `apply prune --dry-run`；圖在主機列完候選後直接結束，完全跳過第二段 apply、flock 與指紋重驗 | 必修 |
| 8 | v1p9 | q10「問 6-32」 | A | 缺「無 tty／EOF 且無 `-y` → 1 + 6-4」分支；現在只有同意與拒絕 | 必修 |
| 9 | v1p9 | q10 → q11l | B | 「是」出口在抽取邊中沒有標籤，縮圖也依賴旁邊敘述猜測，與「否」出口不對稱。應直接在邊上標「是」 | 必修 |
| 10 | v1p9 | q1e、q6 等失敗文字 | B | `engine_start` 寫失敗及 vk-resolve 驗證失敗只寫在框內，沒有通往 `log_prune → launcher_exit → 1` 的流程線 | 必修 |
| 11 | v1p9 | q9l／q10l | C | 各框同時執行 `log_prune` 與 `launcher_exit` 兩件事；依一格一事規則應拆開 | 必修 |
| 12 | v1p9c | q13l 在 q13「有刪除失敗？」之前 | A | `launcher_exit` 必須記錄最終 exit code，但圖先寫 `launcher_exit` 才判斷回 0 或 1，順序顛倒 | 必修 |
| 13 | v1p9c | q12e／q12a／q12b | B | engine_start、flock、指紋失敗都沒有連到結束處；目前只有文字中的錯誤碼，實線流程仍只能往成功寫入走 | 必修 |
| 14 | v1p9c | q13l「寫 log_prune、launcher_exit」 | C | 單格放兩個有嚴格先後的動作，且因此掩蓋了 exit code 尚未決定的問題 | 必修 |
| 15 | v1p9c | q12c「.tmp.dist.*／（trap 沒清到的）」 | F | 斜線後缺名詞，句子不完整；一般讀者無法判斷刪除範圍 | 選修 |
| 16 | v1p10 | u1 憑證組裝 | A | 缺 `_TOKEN` 與 `_TOKEN_FILE` 同時設定時回 1 的互斥檢查 | 必修 |
| 17 | v1p10 | u5～u7 registry 分支 | A | 只畫「公開成功」與「無憑證」，缺錯 token、網路錯誤、registry 回應錯誤、SemVer／分頁解析失敗等查詢失敗分支；這些都應記該目標為 1 並繼續彙總 | 必修 |
| 18 | v1p10 | u3x 未完成交易出口 | A | 規格說 update 末行固定印 6-15；此出口直接以 6-33 結束，沒有 6-15 | 必修 |
| 19 | v1p10 | u10l 位於 u11／u12 之前 | A | 最終 0／1／2 尚未判定便寫 `launcher_exit`，無法記正確 exit code。應先彙總決定結果，再寫結束紀錄 | 必修 |
| 20 | v1p10 | u10l、u3l | C | 同格包含 `log_prune` 與 `launcher_exit` | 必修 |
| 21 | v1p10 | u1「只在 update／upgrade 的 resolve 傳」 | F | 本頁 update 是單段子命令，不是 resolve；文字會使讀者誤以為 token 不該傳給單段 update。應寫「update 單段及 upgrade resolve」 | 必修 |
| 22 | v1p11 | s0 到各狀態 | A | 缺 `strategy=append` 且目標檔不存在時的轉入規則；圖只涵蓋「檔已存在且同意插入」 | 必修 |
| 23 | v1p11 | up_m | A | managed 狀態缺新版 N 已刪除該檔時「不刪專案檔、只 warn」的分支 | 必修 |
| 24 | v1p11 | up_m「baseline 推到 N」 | A | 寫成無條件推進，未在框內保留「合併後 TOML／just 解析失敗時基準版不推」的例外；只在名詞表補述不足以消除主流程誤導 | 必修 |
| 25 | v1p11 | 五個狀態欄 | C | 每欄同時塞入狀態定義、轉入條件、upgrade 行為及 dry-run 輸出；雖標題聲稱「每格一件事」，實際依靠多張便條堆疊四類資訊。建議狀態圖只留狀態與轉移，行為另做表 | 選修 |
| 26 | v1p11 | 多條自環及上方轉入線 | E | 五欄的長直線與自環標籤離狀態框很遠，尤其 managed／declined／appended 的自環容易誤配。應把條件貼近對應自環 | 選修 |
| 27 | v1p12 | bT1「所有可寫動詞的 apply 段」 | A | install、dev、`upgrade vendor_kit` 是單段，不是 apply；此頁把所有可寫動詞都描述成 resolve→apply | 必修 |
| 28 | v1p12 | t4f 日誌位置 | A | 完全漏掉 dev 的 `.tmp.dev.<id>.toml` | 必修 |
| 29 | v1p12 | r3n／p12_tv5「可寫動詞」 | A | 可寫動詞清單漏 dev，導致 dev 遇未完成交易時不會走「先恢復再繼續」 | 必修 |
| 30 | v1p12 | r4 泛稱依 done／pending 恢復 | A | `upgrade vendor_kit` 的恢復契約是重跑 `upgrade vendor_kit`，第一次 install 失敗則依清除清單移除半成品；不能全部畫成相同的 pending 補做流程 | 必修 |
| 31 | v1p12 | t6x | A | 同一終點同時寫「日誌留著」與「第一次 install 依日誌清半成品」，未說清 install 清理成功後日誌如何處置，也把一般交易失敗與首次接入回滾混成一條 | 必修 |
| 32 | v1p12 | t5n 固定寫入順序 | A | 規格只硬性要求 `gen/tools.just` 最後寫且與 cache 同一 apply 原子替換、version.toml 最後寫；圖自行定義一套所有動詞共用的完整順序，超出規格且未必適用各動詞 | 必修 |
| 33 | v1p12 | t5q → t6 | B | 只有「所有步驟跑完」後才詢問是否中斷；逐步寫入 ①／②／③ 的任一失敗沒有實線出口，無法表達中途故障 | 必修 |
| 34 | v1p12 | t8「0（或 2 有衝突）」 | D | 結束碼 2 是需人處理，依色彩規則應為橙，不應與 0 共用綠色終點 | 必修 |
| 35 | v1p15 | v4a～v5d「驗收 §7.4」 | A | 只畫出部分驗收；規格 §7.4 尚要求 just 矩陣、原生雙平台完整流程、私有 registry／token、append 換行、空白路徑、worktree、rootless／Podman、prune、多工具、F1、無 tty、Renovate、動詞集合及紀錄 fail-closed 等案例。頁面若宣稱「§7.4 驗收」就不能略成目前幾格後直接判定全部通過 | 必修 |
| 36 | v1p15 | v5a、v5b、v5c、v5d | C | 每格各放數個彼此可獨立失敗的驗收案例，違反一格一事，也無法指出哪一項失敗。應按驗收群組拆格或改成「執行完整 §7.4 矩陣」單一引用節點 | 必修 |
| 37 | v1p15 | v3n | C | 同一便條同時描述 rootless、Podman、兩個 just 版本及 QEMU 政策，資訊類型混雜 | 選修 |
| 38 | v1p15 | v7z | B | 跨頁出口是普通文字，不是白虛線橢圓；與本組其他跨頁入口／出口表現不一致 | 必修 |
| 39 | v1p15c | v8b 與 v11a | F | v8b 已用 `-t vendor_kit:vN` 發布 image tag，v11a 又寫「打正式 tag vN」但其實是 git tag；同名 tag 的兩種物件未區分，容易誤讀成 image tag 到最後才發布。應明寫「GHCR image tag」與「Git tag」 | 必修 |
| 40 | v1p15c | v10d「SHA256SUMS（列所有資產）」 | A | 在 Release notes 尚未生成、Release 尚未組裝前宣稱「所有資產」語意不精確；應明列 checksum 涵蓋的檔案集合，並排除 `SHA256SUMS` 自身 | 選修 |
| 41 | v1p15c | v11b | C | 同一格包含建立 Release、上傳多種資產、寫 release notes 三件可獨立失敗的事 | 選修 |
| 42 | v1p15c | v8cx | B | index 驗證失敗後已經存在 `vendor_kit:vN` GHCR tag；節點只說「不打正式 tag」而沒有說明這個已發布候選 image tag 如何處理，與「失敗不進正式 tag」容易衝突。應明定使用候選 tag，或將正式 GHCR tag 延後到驗證後 | 必修 |
| 43 | v1p16 | o2s → o5／o6 | A | bootstrap 規格明定先驗 git repo、just 版本，再建 `log/bootstrap/` 並寫 `launcher_start`；圖反過來先寫 log | 必修 |
| 44 | v1p16 | o5x、o6x | B | 因圖已先建紀錄，這兩個前置檢查失敗出口就必須寫 `log_prune／launcher_exit`；目前直接終止，留下缺尾筆的 log。修正正確順序後則應在建 log 前退出 | 必修 |
| 45 | v1p16 | o8e／o8f | A | 第一次 install 必須在第一個寫入前建 `.tmp.install.<id>.toml`，圖完全未畫 | 必修 |
| 46 | v1p16 | o8e、o8f_1「baseline/.gitkeep」 | A | 規格未定義 install 建 `.gitkeep`；應改為空 `baseline/` 及明定的 config 基準副本／metadata | 必修 |
| 47 | v1p16 | o8 → o8q 的平行線 | B | 判斷「install 失敗？」直接從 docker run 框分出，視覺上繞過 `engine_start` 與 install 寫入節點，像是在 install 執行前判斷結果。應由 install／engine_exit 後進入判斷 | 必修 |
| 48 | v1p16 | o8e | C | 單格同時包含建五個薄殼、stamp、baseline、config、version.toml 等多個寫入；至少應拆出進度檔、核心 install 寫入、完成／清理三段 | 必修 |
| 49 | v1p16 | o3bx／o3cx／o4x／o3tx／o8x | B | 多個非零出口未接到共同的 `log_prune → launcher_exit`，執行紀錄流程懸空 | 必修 |
| 50 | v1p16c | o10 命令框 | A | add 的合法選項還有 `--source`、`--dry-run`、`--timeout`；圖只列 `[-y]`，且完全沒有 dry-run 分支 | 必修 |
| 51 | v1p16c | o10re2 → o10p | A | 缺啟動器「收完整份 vk-resolve、驗首尾／筆數／kind」步驟及 6-30 失敗出口，卻直接進 docker create/cp | 必修 |
| 52 | v1p16c | o10e2 → o10e3 | A | apply 第一個寫入前應先在 metadata 建 `[progress]`；圖直接寫 metadata 的 `source + local_image_id` | 必修 |
| 53 | v1p16c | o10e3／o10f | A | 只列 cache 與 stamp，未表現初始檔、baseline、完整 metadata、`gen/tools.just` 最後原子寫入；以「見 add（2）」代替後，這一頁卻仍直接接 version.toml，會使跨頁流程缺口看似被跳過 | 必修 |
| 54 | v1p16c | o10qx、o10bx | A | 規格要求不是存在的 tar 使用 6-24 的 add `--local` 分句；圖只寫一般「1」，旁檔缺失也未呈現規格要求的失敗說明 | 必修 |
| 55 | v1p16c | 各失敗框 | B | tar 無效、旁檔缺失、resolve／apply 失敗均沒有連到 `log_prune → launcher_exit` | 必修 |
| 56 | v1p16c | o10e3「其餘寫入見 add（2）」 | B | 跨頁引用只是框內文字，沒有白虛線入口／出口或實線銜接；頁間責任界線不清 | 必修 |
| 57 | v1p16cc | w2「inspect version.toml 的正式 ref」 | A | bootstrap `--local` 成功後引擎覆寫在 `version.local.toml`，啟動器必須優先 inspect 本機 tag 並核對 `vendor_kit_image_id`；只 inspect version.toml 的正式 ref@digest 可能找不到 docker load 的本機 image | 必修 |
| 58 | v1p16cc | w3 無 → w3x | A | 規格是 inspect 不到後嘗試 `docker pull`，再依原因回 6-24 或逾時 6-31；圖把「本機沒有」直接等同「6-31 拉取逾時」，且根本沒畫 pull | 必修 |
| 59 | v1p16cc | w4 resolve 後直接 w4q | A | resolve 的 extract 計畫應由啟動器執行 docker create/cp，把 `/dist` 掛給 apply；圖缺整個展開階段 | 必修 |
| 60 | v1p16cc | w4p「apply sync（暫存唯讀掛進 /dist）」 | B | 前面沒有任何節點建立該暫存，因而 `/dist` 來源懸空 | 必修 |
| 61 | v1p16cc | w4e2「重展開 cache」 | A | 引擎 apply 不碰 docker daemon；它只能從啟動器已展開並掛入的 `/dist` 寫 cache。此框把主機取件與引擎寫 cache 混成引擎工作 | 必修 |
| 62 | v1p16cc | w4e3 | A | 圖先重寫 cache 再做 `--verify`；規格是先驗既有 cache，驗證失敗才重裝並 warn。順序顛倒 | 必修 |
| 63 | v1p16cc | w4p～w4e3 | A | apply sync 缺 flock、指紋重驗，以及不同時 6-12 的出口 | 必修 |
| 64 | v1p16cc | w4q「印記相符？」 | A | `apply\|no` 不能只看單一工具印記；還要考慮 cache、`gen/tools.just`、全部工具、未完成交易、metadata 完成標記、CI／verify 等計畫條件 | 必修 |
| 65 | v1p16cc | w1q「全相符且非 --verify／CI 為真？」 | F | 布林句歧義，可能讀成「非 verify 或 CI 為真」；正確應是「全相符、未指定 `--verify`、且非 CI 模式？」 | 必修 |
| 66 | v1p16cc | w3x 及其他失敗出口 | B | 沒有接到 `log_prune／launcher_exit`，會留下缺結尾的執行紀錄 | 必修 |

## 統計

- 共 66 條：必修 59、選修 7。
- 依類別：A 35、B 14、C 8、D 1、E 2、F 6。
- 依頁：v1p8bcc 6、v1p9 5、v1p9c 4、v1p10 6、v1p11 5、v1p12 8、v1p15 4、v1p15c 4、v1p16 7、v1p16c 7、v1p16cc 10。

## 沒問題的頁

無。本組 11 頁 codex 每頁皆有至少一條發現。

## 總評（codex 原文）

本組頁面目前不能交給使用者看；交易頁、bootstrap 離線流程、斷網 sync、prune dry-run 與多個 `launcher_exit` 順序仍有會誤導實作的必修錯誤。
