# r13 codex 審查 — 第 3 組（v1p7bcc v1p7bcx v1p7bccc v1p7bccd v1p8 v1p8ccc v1p8c v1p8cc v1p8b v1p8bccc v1p8bc v1p8bcc v1p9）

來源：`r13_codex/out3.md`（codex exec 0.155.1，gpt-5.6-sol，reasoning low，read-only，tokens used 184,191；brief = `r13_codex/brief3.txt` 361,542 bytes = task.txt ＋附件 S 完整 `spec_0_9.md`（未縮減）＋附件 P 13 頁抽取文字＋附件 R（r12 `findings3.md`＋`findings4.md`）＋附件 L；另附 13 張 `review_v2_png/<id>.png`）。以下逐條整理 codex 原文，不加整理者意見。

**執行備註**：日誌有 `ERROR: Reconnecting... 2/5`～`5/5` 後 `Falling back from WebSockets to HTTPS transport`，之後正常完成（exit=0）；13 張 PNG 皆無 `unable to locate image` 錯誤。附件 R 沿用 r12 分組（r12 第 3 組含 v1p7bd、v1p7bc，r12 第 4 組含 v1p9c～v1p16cc），故 R 中有 7 條屬 v1p7bd／v1p7bc——這兩頁本輪在 `group2.json`，不在本組附件 P／PNG 內，codex 明說「無法證明已修，保守標為未修」；此 7 條應以第 2 組結果為準。

## (a) 附件 R 逐條核對統計

| 狀態 | 條數（含 v1p7bd／v1p7bc 7 條） | 條數（排除該 7 條） |
|---|---|---|
| 已修 | 50 | 50 |
| 未修 | 13 | 6 |
| 改壞 | 2 | 2 |
| 合計 | 65 | 58 |

分頁：跨頁共通 3（已修 2／未修 1）；v1p7bcc 5（全已修）；v1p7bcx 4（全已修）；v1p7bccc 6（已修 5／改壞 1）；v1p8 4（全已修）；v1p8ccc 4（全已修）；v1p8c 4（已修 3／未修 1）；v1p8cc 4（已修 3／未修 1）；v1p8b 4（全已修）；v1p8bccc 4（已修 2／未修 1／改壞 1）；v1p8bc 5（已修 4／未修 1）；v1p8bcc 6（全已修）；v1p9 5（已修 4／未修 1）；v1p7bd 3＋v1p7bc 4（未附，保守未修）。

### 未修清單（codex 原文）

| 頁 id | R 條目 | codex 核對結果 |
|---|---|---|
| 跨頁共通 | 名詞表過長、包含本頁未使用名詞 | 多頁仍重複放入 `flock／指紋`、6-38、升引擎全契約等大量非本頁核心內容。屬選修可讀性問題。 |
| v1p8c | 進度檔未記恢復所需資料 | 已補覆寫行與 symlink 目標，但仍未依規格明示 image ID。 |
| v1p8cc | 把下一次 sync 詳細流程畫在本頁 | 雖縮短成 ref／stamp 比對後跨頁，但仍在 undev 頁畫了下一次呼叫的前置流程。 |
| v1p8bccc | 「任一步失敗」只從最後一步出線 | 現在只從 `m10a`、`m10b`、`m10e` 接失敗；append 行、metadata、stamp 與刪進度檔失敗仍未完整接入。 |
| v1p8bc | 保護清單規則框孤立 | `x2r` 仍無連線，僅靠位置和文字聲稱約束後續。 |
| v1p9 | engine／vk-resolve 失敗沒有結束流程線 | 引擎事件可由圖例隱含，但 resolve 非 0 與文法錯仍未各自形成可追蹤分支；`q6x` 只承接文法判斷。 |
| v1p7bd（未附） | `uD／d2c2／d2c3` sync 缺重生 tools.just | 未附本版文字／縮圖，保守標未修 |
| v1p7bd（未附） | `d2c` 一格多事 | 同上 |
| v1p7bd（未附） | `d1px` 未保存 6-24／6-31 | 同上 |
| v1p7bc（未附） | `s2a／s2dq` 完整預檢不足 | 同上 |
| v1p7bc（未附） | `s2n` 跨頁出口懸空 | 同上 |
| v1p7bc（未附） | `s2r → s4` 跨頁表示不正確 | 同上 |
| v1p7bc（未附） | `s2lv` local 與 ID 判斷合併 | 同上 |

### 改壞清單（codex 原文）

| 頁 id | R 條目 | codex 核對結果 |
|---|---|---|
| v1p7bccc | 三方合併沒有衝突／解析失敗與碼 2 | 雖新增 `s13gc／s13gcx`，但把「合併衝突」和「解析失敗」合併後一律流入寫檔、推基準版；解析失敗依法應留原檔且不推基準版。 |
| v1p8bccc | 拒絕刪 append 行後仍刪所有權 metadata | 現在保留部分 metadata，但工具版本鎖定行仍刪掉，留下已解除接入卻殘存 `baseline/<repo>/.vendor_kit.toml` 的孤兒狀態，與規格的 remove 檔案矩陣不一致。 |

### 已修清單（codex 核對結果摘錄）

- 跨頁共通：共用 `launcher_exit` 扇出——本版取消，改由終點搭配圖例約定；逐格 `engine_exit`——圖例統一約定 `docker run 引擎` 格隱含開始與結束。
- v1p7bcc：只剩 `flock`、未再畫指紋重驗；`s12j → s12jr` 補 `.tmp.upgrade` 恢復；目標引擎 inspect／pull 拆到 v1p7bcx；`s11px` 明列 6-24／6-31；降版與能否無損讀拆成 `s12d1`、`s12d2`。
- v1p7bcx：`s12hi`～`s12hox` 補目標 ref inspect／pull 與失敗分支；第一行變動後判定移到 v1p7bccd；`s12hz` 改白虛線橢圓接 E(c)(2)；本頁不再修改第一行、只建進度檔後結束該引擎。
- v1p7bccc：`s13gp → s13gpa` 補 config.toml 缺檔詢問；`s13gm／s13gmf` 補更新 `baseline/.vendor_kit.toml`；`s12n` 與跨頁失敗出口說明進度檔保留、按 done／pending 續跑；v1p7bccd 拆 `s14` 與 `s14b`（同引擎修復 vs vX → vY）；v1p7bccd 拆 `s13q`、`s13h`、`s13q2`。
- v1p8：`.tmp.dev` 建立、內容、刪除及失敗保留已補；工具覆寫改 `[tools].<repo>`；`d1q` 主機側存在性、`d2c` 引擎完整驗證；`d3c` 改紅。
- v1p8ccc：`.tmp.dev` 生命週期已補；`v1l／v1lq／v1lx` 補 LABEL 介面版／檔案版判定與碼 3；`v2b` 兩行一次原子更新；「下次打任何 just」改成 vendor_kit 動詞或帶 `_sync` 的工具 recipe。
- v1p8c：`u6gf` 補刪進度檔節點；`u6c`、`u6d`、`u6e2`、`u6f` 均有失敗線；「是／已刪」改「拆掉 cache symlink」。
- v1p8cc：`w2l` 明列兩行及 image ID；「下次打任何 just」已限縮；pull 移出本頁、白虛線出口接 sync 頁。
- v1p8b：stdout 只列指紋與 `apply|yes`；`m6c` 明寫由 apply 執行、不交啟動器；`m7z` 改跨頁出口、邊標「否」；起點改 `remove <repo> [-y] [--dry-run]`。
- v1p8bccc：無 tty 小標與圖例 EOF／Ctrl-C 已加；tools.just 與 cache 同一步原子替換、version.toml 最後刪（符合 I17）。
- v1p8bc：stdout 只畫指紋與 `apply|yes`；完整預檢明示逐工具檢查、任一不過整體不動、原因全列；`x2b` 拆 tracked 自產檔與本機產物；`x4z` 改白虛線跨頁出口。
- v1p8bcc：`x5c` 直接刪、不看 hash；`.gitkeep` 明示為 VK 自產檔（依指示不再質疑）；共用扇出已移除；`x8` 改「不動；該行不存在」；`x5af` 標「已刪 hash 相符者」、保留項由摘要回報；justfile／dockerignore 增「不動」節點後才匯流。
- v1p9：`q9y` 接 `q11z` 續跑 `apply prune --dry-run`；`q10t → q10tx` 補無 tty／EOF 6-4；`q10 → q11l` 標「是」；`log_prune`＋`launcher_exit` 同格已不再畫。

## (b) 本輪新發現（codex 原文，已排除附件 L）

| # | 頁 id | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|---|
| N1 | v1p7bcc | `s12j --是→ s12jr → s12v` | A | 有既有升級進度檔時直接跳到目標比較，繞過 `s12s` 的薄殼完整性檢查；規格的直接 `upgrade vendor_kit` 主流程先檢查薄殼被改，再恢復進度檔。 | 必修 |
| N2 | v1p7bccc | `s13gpa --否→ s13gw` | A | 拒絕建立 config.toml 後仍進入「config.toml 原子替換」並連到檔案框，圖面實際表示仍會寫檔；應直接略過寫檔，僅記拒絕狀態後續行。 | 必修 |
| N3 | v1p7bccc | `s13gcx → s13gw → s13gb` | A | 合併衝突與解析失敗被合成同一路徑；解析失敗依法應保留原檔且不推基準版，不能和衝突標記路徑一起原子替換並推進 baseline。 | 必修 |
| N4 | v1p7bccc | `s13gn／s13gw／s13gb` | B | config.toml 建立、原子替換及基準版推進的寫入失敗都沒有實線接到 `s13qx`，只有薄殼重產及 metadata 有失敗出口。 | 必修 |
| N5 | v1p8、v1p8ccc、v1p8c、v1p8cc、v1p8b、v1p8bc | 各動詞進入主流程前 | A | 這些都是可寫動詞，但圖中都未畫「偵測既有未完成交易 → 先恢復 → 恢復失敗 6-27」的共通前置；只在失敗終點寫「下次會恢復」不足以表示實際入口。 | 必修 |
| N6 | v1p8ccc | `v1lq`「介面版／檔案版 ≥ 薄殼自描述首行的？」 | F | 薄殼自描述首行含介面版、引擎版本與 hash，並不含可直接比較的「檔案版」；句子把 image LABEL 與現有檔案 schema 的比較來源混成一個。 | 必修 |
| N7 | v1p8c | `u4b` | C | undev 工具計畫只有鎖定版 `extract`，格內卻列「pull／extract／mount 清單」，會誤導為本次也掛載 dev path；應只寫實際可能輸出的記錄。 | 選修 |
| N8 | v1p8b、v1p8bccc | 名詞 `resolve／apply／--dry-run` | A | 名詞表仍說 `--dry-run`「要先拉 image」；remove 依規格不展開 image，dry-run 也不拉。 | 必修 |
| N9 | v1p8bc、v1p8bcc | 名詞 `resolve／apply／--dry-run` | A | 同樣誤稱 uninstall dry-run 要先拉 image；uninstall 不需展開 image。 | 必修 |
| N10 | v1p8bccc | `m10k → m10b → … → m10e` | A | 拒絕刪 append 行時保留工具 metadata，但後續仍刪 cache、stamp 與版本鎖定行，造成「工具已移除、metadata 卻仍宣稱擁有專案行」的孤兒狀態；需重新定義拒絕後的完整提交狀態。 | 必修 |
| N11 | v1p8bcc | `x5z` | B | 「刪進度檔」沒有對應檔案節點或刪除線，和本頁所有其他刪檔表示不一致，也看不出 `.tmp.uninstall.<id>.toml` 確實被移除。 | 選修 |
| N12 | v1p9 | `q0l` | B | 格內寫「失敗 → 1 + 6-38」，但沒有失敗終點或流程線；此處不是可由終點圖例補足的已到達終點，而是實際懸空分支。 | 必修 |
| N13 | v1p9 | `q1 → q2 → … → q6` | A | 缺少 resolve 非 0 的獨立判斷；目前不論 resolve 是否成功都像會讀 stdout 並繼續，`q6x` 只能表達文法不合，不能代替「非 0 時不讀 stdout、原碼傳出」。 | 必修 |
| N14 | v1p9 | `q11l`「失敗的記下、續刪其餘」 | B | 四類 docker 刪除後未在本頁保存「是否有任何刪除失敗」供下一頁決定最終碼；跨頁出口只說進 apply 與摘要。 | 必修 |
| N15 | 多頁 | 圖例事件名 `launcher_started／completed|failed`、`engine_started／completed|failed` | A | 規格事件註冊表使用 `launcher_start／launcher_exit／engine_start／engine_exit`；圖例改成另一組名稱會讓實作者誤以為這些才是正式 `event_name`。可保留「開始／結束」自然語言，但事件名須與規格一致。 | 必修 |

新發現統計：15 條；必修 13、選修 2；類別 A 9、B 4、C 1、F 1（N5、N8、N9、N15 各跨多頁）。

## (c) 沒問題的頁（codex 原文）

- v1p7bcx：本輪未發現附件 L 以外的新問題。
- v1p7bccd：本輪未發現附件 L 以外的新問題。

（v1p7bcx 的 4 條 R 條目全部已修；v1p7bccd 為本版新頁、R 無條目。N15 的圖例事件名為「多頁」共通，codex 未列明是否含此兩頁。）

### codex 逐頁結論（原文）

- v1p7bcc：仍有恢復路徑繞過薄殼檢查。
- v1p7bcx：本輪未發現附件 L 以外的新問題。
- v1p7bccc：config.toml 拒絕、衝突與解析失敗路徑仍不正確。
- v1p7bccd：本輪未發現附件 L 以外的新問題。
- v1p8：主要舊問題已修，但缺共通交易恢復入口。
- v1p8ccc：缺交易恢復，且 LABEL／檔案版比較文字不成立。
- v1p8c：仍缺完整恢復資訊與入口。
- v1p8cc：下一次 sync 流程仍侵入本頁，且缺交易恢復入口。
- v1p8b：remove 主流程大致改善，但 dry-run 說明錯且缺恢復入口。
- v1p8bccc：拒絕 append 後留下孤兒 metadata，失敗線亦不完整。
- v1p8bc：完整預檢已改善，但缺恢復入口，dry-run 說明錯。
- v1p8bcc：主要 R 條目已修；另有進度檔刪除表示不一致。
- v1p9：dry-run 與無 tty 已修，但 resolve 非 0、6-38 及刪除失敗跨頁狀態仍懸空。

## (d) 總評（codex 原文）

> 本組頁面目前仍不能交給使用者看；自身升級的 config.toml 分支、所有可寫動詞的交易恢復入口、remove 拒絕後狀態，以及 prune 的失敗／跨頁結果仍有必修錯誤。

codex 開頭聲明：「以下已排除附件 L 的機械 lint 條目，也不再要求逐格畫 `engine_exit`／`launcher_exit`；圖例約定可成立。」
