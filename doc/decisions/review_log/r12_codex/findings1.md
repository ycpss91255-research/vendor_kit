# 第十二輪 codex 審查 — 第 1 組（v1p2, v1p3, v1p3b, v1p3c, v1p4, v1p5, v1p5i, v1p5ccc, v1p5c, v1p5cw, v1p5cc）

來源：`r12_codex/out1.md`（codex exec，11 張縮圖 + brief1.txt 376 KB，exit=0）。以下為 codex 結論的逐條整理，未加審查者意見。codex 聲明：不重複附件 L 已列的機械 lint，不回報舊名／新名問題。

## 逐條

### v1p2
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `t_vl` | A | 「uninstall hash 相符才刪」與規格不符；`version.local.toml` 是自有覆寫檔，uninstall 應刪除，不以內容 hash 為條件。 | 必修 |
| 2 | `t_tmp`、`p2_tv`、`p2_tv16` | A | `.tmp.<verb>.<id>.toml` 的適用動詞漏掉 `dev`；規格已要求 `dev` 在第一個寫入前建立 `.tmp.dev.<id>.toml`。 | 必修 |
| 3 | `p2_tv18`「sync 豁免」 | A | 規格已撤回 sync 的執行位置豁免；工具 `_sync` 是先 `cd` 到專案根，因此 sync 仍須通過相同位置檢查。 | 必修 |
| 4 | `t_bl` | A | 「有衝突仍推」寫得過度絕對；合併衝突可推基準版，但 TOML／just 解析失敗時該檔基準版不得推進。 | 必修 |
| 5 | `p2_tv15` | A | 「install 只建 baseline/.gitkeep」漏掉 `baseline/vendor_kit/config.toml` 與 `baseline/.vendor_kit.toml` 的 install 責任。 | 必修 |
| 6 | `t_vl` | C | 同一格同時描述檔案格式、dev／undev／bootstrap 寫入、uninstall、CI 行為，超出「一格一件事」；建議拆成「格式／寫入者」與「CI、移除行為」。 | 選修 |
| 7 | 縮圖左欄目錄樹 | E | 內容密度過高，數個虛線子框與樹線貼近文字，尤其 `baseline/`、`gen/`、`log/` 區難以快速辨識父子關係。 | 選修 |

### v1p3
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `d4_7` | A | 工具 repo CI 的摘要漏列「特殊檔禁止」；規格要求 symlink、hardlink、特殊檔三類都由 `check.sh --dist` 擋下。 | 必修 |
| 2 | `p3_off` | A | 只寫 tar 形離線入口，漏掉 release 離線包另附 `local_bootstrap.sh` 便利包裝及其非契約定位；若本格宣稱完整描述 Release 資產，應補上。 | 選修 |
| 3 | `d4_1` | C | 一格同時承擔出貨範圍、展開位置、三類檔案禁止與換行規則，閱讀負擔過高；可將驗證規則移到 CI 格。 | 選修 |
| 4 | `p3_syncr` | C | 一格混合 `_sync` 內容、公開 recipe 相依、lint、載入限制與 fixture 驗收五件事，應至少拆成「工具契約」及「lint／限制」。 | 選修 |

### v1p3b
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `d1`「gen/.stamp = 引擎 ref？」 | A | 此判斷被畫成所有兩段動詞進 resolve 前的共同閘門，會讓 add、remove、upgrade、undev、uninstall、prune 也錯誤地走 6-1；它只屬 sync 相容性路徑。 | 必修 |
| 2 | `s2b` | A | 「查 registry 最新 tag／digest」被畫成每次 resolve 的固定步驟；remove、sync、undev、uninstall、prune 不查最新版，指定 `@<tag>` 也不得查。 | 必修 |
| 3 | `s3a → s3b` | A／B | `docker image inspect` 後缺「本機已有 → 跳過 pull」分支，現圖看起來無論結果都會執行 pull。 | 必修 |
| 4 | `s3b → s3c` | A | 圖把每筆 pull 都接到 create／cp；`pull` kind 只拉 image，只有 `extract` kind 才 create／cp，remove、uninstall、prune 等也可能完全沒有展開。 | 必修 |
| 5 | `s2z…s2c` | A | resolve 容器缺 `engine_exit`；規格要求每個 resolve、apply、單段容器結束前各自 append `engine_exit`。 | 必修 |
| 6 | `p3_ok` | B | `apply|no` 直接到綠色終點，漏掉啟動器仍須寫 `sync_fast_path`、`log_prune`、`launcher_exit`。 | 必修 |
| 7 | `s0a`、`s0b` | C | 建目錄、建檔、寫 `launcher_start` 與失敗處理塞在同一格；依一格一事標準至少應拆成「建紀錄檔」與「寫 launcher_start」。 | 必修 |
| 8 | `s4`、`s4z` | F | 先畫「docker run apply」，下一格才畫容器第一個動作 `engine_start`，一般讀者容易理解成 apply 已開始後才記錄；應將 `engine_start` 明確置於 apply 動作之前或容器框內最上方。 | 選修 |
| 9 | 縮圖主流程 | E | `s3b` 的成功主線與「失敗」支線在狹窄區域交會，且 `s4` 後的線折返，條件歸屬不夠直觀。 | 選修 |

### v1p3c
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `c_d → c_e → c_f` | A | 自身 CI 先正式 release，再跑完整驗收矩陣；規格要求必要驗收不得缺少才可出貨，不能在發布不可刪資產後才決定候選是否合格。應把候選驗收放在正式 release 前，release-test 可留在發布後。 | 必修 |
| 2 | `p3_accb_r12c2`（驗收 31） | A | config.toml 異常值清單漏掉「非整數」；規格明列 0、負數、非數字、非整數、重複、缺鍵、缺檔。 | 必修 |
| 3 | `p3_acc_r17c2`（驗收 18） | A | 敏感值驗收只寫輸出、metadata、log，漏掉進度檔；規格要求 metadata、執行紀錄、進度檔全部 grep 不到 token。 | 必修 |
| 4 | `k1f` | C | 同一終點同時放四種結束 1 與結束 3，沒有指出 3 的具體相容性原因；至少應把「結束 3」拆成獨立橙色終點。 | 選修 |
| 5 | 驗收矩陣 | F | 單頁放 35 條完整敘述，字級與行距已低於快速審閱用途；建議本頁只放分組索引，完整逐條矩陣另頁呈現。 | 選修 |

### v1p4
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `f_cfg --config_read--> m_log` | A | 資料流把 config.toml 直接送到 log 模組，像是由 log 模組解析設定；規格是引擎以 TOML parser 讀設定，再透過 `log_event()` 記 `config_read`。 | 必修 |
| 2 | `h3`「vendor.just…含 log.sh」 | A | `log.sh` 是獨立薄殼檔，由 vendor.just source／使用，不是包含在 vendor.just 內；目前文字會誤導檔案邊界。 | 必修 |
| 3 | `h0`、`h1`、`h2`、`h3`、`g1`、`g2` | B | 抽取結果沒有使用者 → 根 justfile → entry.just → vendor.just／tools.just → 工具 recipe 的連線；主機側載入關係因而成為六個懸空方塊。 | 必修 |
| 4 | `m_ver_u2_0`「進度日誌」 | A | 把所有進度日誌歸給 version 模組不完整：工具 add／upgrade 的 `[progress]` 在 metadata，由 baseline 模組維護；應畫出兩類落點或把責任抽成交易模組。 | 必修 |
| 5 | `run_cli` | F | 同一條線同時標「動詞、參數、協定」與反向的「結束碼、vk-resolve 清單」，但箭頭並非清楚的雙向箭頭；應拆兩條資料流或使用明確雙箭頭。 | 選修 |
| 6 | 引擎容器區 | E | 模組、最小單元與專案檔的連線高度集中在容器右側，數條線共用長水平路徑，難以判定各自端點；建議按讀寫檔案群重新對齊模組。 | 選修 |

### v1p5
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `a0l` 之後至 `a6i/a6p` | A | 缺少引擎 LABEL 的最低介面版檢查；規格要求此檢查在任何上網／pull 之前，過舊須 3 + 6-18。 | 必修 |
| 2 | `a8z` | B／D | 跨頁出口只是普通文字，不是規定的白色虛線橢圓；與下一頁的虛線入口視覺語意不成對。 | 必修 |
| 3 | `a8e --否--> lp` 與其他失敗匯流 | B | 多個不同失敗先匯入共同收尾，再由 `launcher_exit` 無條件分岔到五個終點；圖上沒有保存「原失敗原因」的條件，出口歸屬歧義。 | 必修 |
| 4 | `a8ix` | F | 「本機無此 image」未標出 tag 形 `--local` 不得 pull，需回失敗；讀者需回看前文才能理解為何不是走一般 pull。 | 選修 |

### v1p5i
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `a9e` | C | 一格同時寫「建／重寫薄殼、根 justfile、根 .dockerignore」，跨越多個判斷與詢問，與後續 install 分頁也重複；應只寫「執行 install，詳見跨頁」。 | 必修 |
| 2 | `a9es…a9q` | A | 單段 install 容器缺 `engine_exit`，成功及失敗都必須在容器結束前寫入。 | 必修 |
| 3 | `a9x` | D | 所有 install 失敗都畫紅色，但 install 可能因 6-4、6-28 等「需人處理」而結束，這些應是橙色；紅色只適用寫入、驗證等真正失敗。 | 必修 |
| 4 | `a9z` | B／D | 成功跨頁出口不是白色虛線橢圓，與下一頁入口語意不一致。 | 必修 |

### v1p5ccc
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `a10re → a10d → a10a` | A | resolve 非 0、vk-resolve 驗證失敗、pull／extract 失敗都缺分支；現圖只能一路進 apply，與「resolve 非 0 不讀 stdout、不跑 docker／apply」矛盾。 | 必修 |
| 2 | `a10re0…a10re`、`a10ae0…a10ae` | A | resolve 與 apply 兩個容器都缺各自的 `engine_exit`。 | 必修 |
| 3 | `lx → a13`、`lx → a12` | B | `launcher_exit` 同時無條件連到成功與失敗終點，沒有保存 add 結果的條件，出口歧義。 | 必修 |
| 4 | `a10x` | F | 判斷放在 apply 後，文字卻叫「本次 add 失敗？」；應明確涵蓋 resolve、主機 docker、apply 任一階段，否則會被理解為只檢查 apply。 | 必修 |
| 5 | `a10f` | A | 檔案群把 version.toml 列在首項，容易暗示先寫；規格要求 version.toml 最後寫，建議在群組中直接標示「最後」。 | 選修 |

### v1p5c
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `i4` 至 `i4_5b` | A | 先在專案內產生多個暫存檔，下一頁才建 `.tmp.install.<id>.toml`；規格要求所有可寫動詞在第一個寫入前先建進度檔。 | 必修 |
| 2 | `i4_5b` | A | 不論 config.toml 是否已存在都接著產 baseline 副本；修復型中 config.toml 已存在時規格要求不動，不能用目前內容偷偷建立／覆蓋基準版。 | 必修 |
| 3 | `i1e…i4z` | A | install 容器在本頁及後續兩頁都沒有明確的 `engine_exit` 收尾點。 | 必修 |
| 4 | `i4n` | F | 便條把「第一次失敗清除」與「修復失敗保留進度」混在一段，且未指出哪些寫入已發生；建議移到各自失敗出口。 | 選修 |

### v1p5cw
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `i4bc` | A | 只在「第一次」建立 config.toml；規格要求修復型若 config.toml 缺失也要建立，存在才不動。 | 必修 |
| 2 | `i4bb` | A | baseline config 副本也只畫第一次建立；修復型補建缺失 config.toml 時必須同時建立相應基準版與 metadata。 | 必修 |
| 3 | `i4bc/i4bb/i4g` | A | 整頁未建立 `baseline/.vendor_kit.toml` 中 config.toml 的 `state=managed` metadata；下一頁只在 append `.dockerignore` 時寫該檔，無法涵蓋所有 install。 | 必修 |
| 4 | `i4c` | F | 「寫 version.toml」與括號「已有則不動」放在同格，動作與不動條件衝突；應先判斷缺檔，再只在缺檔分支寫。 | 選修 |
| 5 | `i5z` | B／D | 跨頁出口仍是普通文字，未採白色虛線橢圓。 | 必修 |

### v1p5cc
| # | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|
| 1 | `i12`、`igq` | A | 詢問只畫「是／否」，漏掉無 tty／EOF／Ctrl-C 分支；規格要求無 tty／EOF 且無 `-y` → 1 + 6-4，Ctrl-C 中止且不記 declined。 | 必修 |
| 2 | `igs --是--> idl` | A | 根 `.dockerignore` 是 symlink 時直接收尾，沒有像 justfile 一樣印一次性遷移指示；頁首又宣稱 symlink 會「不寫只印指示」，流程與自身說明不一致。 | 必修 |
| 3 | `im` | C | 一格同時處理建檔、append、已含、拒絕、symlink 五種結果與輸出，違反一格一件事，且遮蔽各分支是否真的寫檔。 | 必修 |
| 4 | `idl → lp → lx` | A | install 單段容器刪進度檔後直接進啟動器收尾，缺少容器的 `engine_exit`。 | 必修 |
| 5 | `i5e` | B | 跨頁入口只寫「已寫 launcher_start」，沒有承接上一頁已寫的 `engine_start` 與仍在同一引擎容器內，容易被誤讀為新呼叫。 | 選修 |

## 沒問題的頁
（無 — 11 頁 codex 都列出至少一條。）

## 統計
- 共 58 條：必修 42、選修 16。
- 類別分布：A 31、A／B 1、B 5、B／D 3、C 7、D 1、E 3、F 7。
- 反覆出現的主題：容器缺 `engine_exit`（v1p3b、v1p5i、v1p5ccc、v1p5c、v1p5cc）；跨頁出口未用白色虛線橢圓（v1p5、v1p5i、v1p5cw）；`launcher_exit` 無條件分岔至多個終點（v1p5、v1p5ccc）；install 進度檔／config baseline 責任（v1p2、v1p5c、v1p5cw）。

## 總評（codex 原文）
本組頁面目前仍有多項會改變實作行為的必修錯誤，尤其通用 resolve/apply 流程、執行紀錄收尾、install 進度檔順序與 config baseline；修正前不宜交給使用者看。
