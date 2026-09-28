# 第十三輪 codex 審查 — 第 1 組（v1p2, v1p3, v1p3b, v1p3c, v1p3d, v1p4, v1p5, v1p5i, v1p5ccc, v1p5c, v1p5cw, v1p5cc, v1p5b）

來源：`r13_codex/out1.md`（codex exec 0.155.1，read-only，13 張縮圖；brief1.txt 392 KB = task.txt ＋ 附件 S 規格 v3.5 §0–§9 ＋ 附件 P 本組 13 頁抽取文字 ＋ 附件 R = `r12_codex/findings1.md` ＋ `findings2.md` ＋ 附件 L lint；exit=0，無圖片載入錯誤，tokens used 196,200）。以下為 codex 結論的逐條整理，未加整理者意見。codex 聲明：不重複附件 L 已列的機械 lint；執行紀錄依新版圖例約定審查，不要求逐格補 `engine_exit`／`launcher_exit`。

## (a) 附件 R 逐條核對統計

本組相關共 **66 條：已修 59、未修 4、改壞 3**。

各頁：

| 頁 | 條數 | 已修 | 未修 | 改壞 |
|---|---|---|---|---|
| v1p2 | 7 | 6 | 1（#7） | 0 |
| v1p3 | 4 | 4 | 0 | 0 |
| v1p3b | 9 | 8 | 0 | 1（#2） |
| v1p3c | 5 | 5 | 0 | 0 |
| v1p4 | 6 | 5 | 1（#6） | 0 |
| v1p5 | 4 | 3 | 0 | 1（#1） |
| v1p5i | 4 | 4 | 0 | 0 |
| v1p5ccc | 5 | 4 | 0 | 1（#1） |
| v1p5c | 4 | 4 | 0 | 0 |
| v1p5cw | 5 | 5 | 0 | 0 |
| v1p5cc | 5 | 4 | 1（#5） | 0 |
| v1p5b（取 findings2 中 G1、G2、G4 ＋ 本頁 1–5） | 8 | 7 | 1（G4） | 0 |

### 未修清單

| 頁 | R# | 原條目 | codex 核對結果 |
|---|---|---|---|
| v1p2 | 7 | 縮圖左欄目錄樹密度過高（E，選修） | 左欄仍非常密集，`baseline/`、`gen/`、`log/` 的樹線與多層框仍難快速辨識。 |
| v1p4 | 6 | 容器右側長距離共線與折返（E） | 容器右側仍有多條長距離共線與折返，模組到檔案的端點需沿線追蹤才能辨識。 |
| v1p5cc | 5 | `i5e` 跨頁承接語意 | 仍只寫「已寫 launcher_started」，未明說承接同一 install 容器；跨頁仍可能被誤認為新呼叫。 |
| v1p5b | G4 | 頁首流程帶與名詞表大量重複（F，選修） | 頁首沿革、重複名詞與共通規則仍占大量版面，主流程辨識度偏低。 |

### 改壞清單

| 頁 | R# | 原條目 | codex 核對結果 |
|---|---|---|---|
| v1p3b | 2 | `s2b`「查 registry 最新 tag／digest」被畫成每次 resolve 固定步驟 | 雖不再涵蓋所有動詞，卻把單段 `update` 畫在 resolve 內，且未排除 CI 模式；仍會導出錯誤編排。 |
| v1p5 | 1 | 缺 LABEL 最低介面版檢查 | 已新增檢查，但放在 inspect／pull 之後；規格要求最低介面版檢查先於任何上網。 |
| v1p5ccc | 1 | add 失敗分支 | 已補 resolve／文法、docker、apply 失敗分支，但全部匯成結束 1；bootstrap.sh 應原樣傳出 add 的 2／3。 |

### 已修條目（codex 核對依據摘錄）

- v1p2 #1 `t_vl2` 已明載 uninstall 直接刪 `version.local.toml`；#2 `t_tmp` 與進度檔範例已納入 `dev`；#3「sync 豁免」已移除、`_sync` 改為先 `cd` 專案根；#4 `t_bl` 已補「衝突仍推；解析失敗的檔不推」；#5 已列 `baseline/vendor_kit/config.toml` 與 `baseline/.vendor_kit.toml` 的 install 責任；#6 `t_vl`／`t_vl2` 已拆。
- v1p3 #1 `d4_7` 三類禁止；#2 `p3_off` 補 `local_bootstrap.sh` 便利包裝；#3 `d4_1` 縮成出貨與展開責任；#4 `_sync` 拆 `p3_syncr`／`p3_syncl`。
- v1p3b #1 `s1` 註明非 sync 跳過 `d1`；#3 補「本機有 → 跳過 pull」；#4 `s3c` 限定 extract kind；#5、#8 依圖例約定②；#6 `apply|no` 補快路徑事件；#7 拆 `s0a`／`s0b`／`s0c`；#9 pull 成功／失敗與 extract 主線已分開。
- v1p3c #1 候選 tag → release-test → 正式 release；#2 驗收 31 補「非整數」；#3 私有 registry 驗收索引含進度檔；#4 結束 1／3 拆 `k1f`／`k1g`；#5 35 條移至 v1p3d。
- v1p4 #1 `config.toml` 先流向 schema 再傳 `config_read` 至 log；#2 `log.sh` 獨立檔、由 `vendor.just` source；#3 使用者→根 justfile→entry.just→vendor.just／tools.just→工具命名空間均有連線；#4 交易責任集中 progress；#5 拆 `run_cli`／`ret_cli`。
- v1p5 #2 `a8z` 白色虛線橢圓；#3 各失敗原因保留自己終點；#4 `a8ix` 明載 tag 形 `--local` 不得 pull。
- v1p5i #1 `a9e` 只表達執行 install；#2 圖例約定②；#3 `a9h` 分流橙／紅出口；#4 `a9z` 白色虛線橢圓。
- v1p5ccc #2 圖例約定②；#3 移除共同 launcher 格分岔；#4 分別判斷 resolve＋文法、docker、apply；#5 `version.toml` 標「最後寫」。
- v1p5c #1 `.tmp.install.<id>.toml` 移到所有暫存寫入前；#2 config 存在直接略過；#3 圖例約定②；#4 失敗結果移往 v1p5cw 明確出口。
- v1p5cw #1 改判「本次是否因原本缺檔而產生 config」；#2 補建 config 時一併建基準版副本；#3 新增 `baseline/.vendor_kit.toml` `state=managed`；#4 先判 `version.toml` 缺失再寫；#5 `i5z` 白色虛線橢圓。
- v1p5cc #1 兩問句旁有無 tty／EOF 標示、圖例補 Ctrl-C；#2 `.dockerignore` symlink 分支一次性遷移指示；#3 建檔／symlink／已含／詢問／append 拒絕已拆開；#4 圖例約定②。
- v1p5b G1 圖例約定②；G2 移除共同 launcher 收尾格多出口；#1 `docker load` 與 `.digest` 各有失敗出口；#2 `c2d` 已列輸入；#3 `c2c` 收斂為「算執行計畫」；#4 `baseline/.gitkeep` 與現行定案一致；#5 add 前狀態不再宣稱 `add --local` 寫 version.local.toml。

## (b) 本輪新發現（不重複附件 L）

| # | 頁 id | 元件 id／引文 | 類別 | 說明 | 必修/選修 |
|---|---|---|---|---|---|
| 1 | v1p2 | `p2_ver_n`「第 1 行 = 唯一版本鎖定行」 | A | 規格明定第一行只是 install 的寫出慣例、不是契約；契約是頂層 `vendor_kit` 位於 `[tools]` 前且符合正規形。 | 必修 |
| 2 | v1p3b | `s2b` | A | `update` 是單段動詞，不應畫成 `resolve` 容器內的步驟；CI 模式下 upgrade 未指定 tag 也不得查最新版。 | 必修 |
| 3 | v1p3b | `p3_fast` 的 `--local` 判別 | A | 仍採「含 `/` 或 `.tar` 即檔案」及「用 `./`／完整 ref 消歧」的舊規則；v3.5 必須依 `.tar` → 同名檔消歧 → tag 的順序判定。 | 必修 |
| 4 | v1p4 | `m_res_u1_1`「token／逾時」 | A／F | pull timeout 是啟動器責任且不轉發引擎；與 registry 查詢 token 放在 resolve 模組會誤導責任邊界。 | 必修 |
| 5 | v1p5 | `a8q`、`a8e`、`a8t` | A | bootstrap `--local` 仍以「含 `/`」先判檔案，並以「本機有同名 image」判 6-37；正確條件是非 `.tar`、含 `/`、且存在同名檔，與 image 是否存在無關。 | 必修 |
| 6 | v1p5 | `a8p` | A | LABEL 檢查應在可能的 `docker pull` 前；現圖只有 image 到本機後才檢查，斷網時可能先回 pull 失敗而不是 3＋6-18。 | 必修 |
| 7 | v1p5i | `a9q`、`a9hx`、`a9x` | A | install 非 0 只畫兩個結束 1，漏掉 install 回 3 時 bootstrap.sh 必須原碼傳出 3。 | 必修 |
| 8 | v1p5ccc | `a10rq`／`a10d`／`a10x` → `a12` | A | resolve 或 apply 回 2／3 時被統一改成 1；bootstrap 逐 `-t` 中止正確，但結束碼必須保留失敗步驟原碼。 | 必修 |
| 9 | v1p5c | `i0l → i2` | A | 自己執行 install 時先嘗試建立執行紀錄、後檢查是否在 git repo；非 git 目錄無合法紀錄落點，應先做主機 git 前置檢查，再建紀錄。 | 必修 |
| 10 | v1p5cc | `igq0`「已含這四行？」 | A | 這是全有／全無判斷；若只已有其中幾行，後續 append 四行可能重複。應逐行辨識，只記實際新增的行。 | 必修 |
| 11 | v1p3d | 驗收 18 `p3d_acc_r17c2` | A | 詳表漏驗 `registry_query` URL 必須移除 userinfo；只有「grep 不到 token」不足以涵蓋 §7.4-18。 | 必修 |
| 12 | v1p3d | 驗收 19 `p3d_accb_r0c2` | A | 漏掉故意修改 `.dockerignore` 其中一行後，uninstall 應跳過該行並 warn、其餘原文相同行仍刪除的驗收。 | 必修 |
| 13 | v1p4 | 引擎模組鏈 `m_res → m_schema → m_prog → …` | F | 雖以資料名稱標線，整體仍像固定執行順序；架構頁應避免讓八模組被理解為每個動詞都依序經過全部模組。 | 選修 |
| 14 | v1p3d | 全頁 | F | 作為「逐條詳表」，多列已壓縮掉規格中的關鍵驗證子條件；建議保留可判定 pass/fail 的完整條件，否則改名為驗收摘要。 | 選修 |

計 14 條：必修 12、選修 2。類別分布：A 11（含 1 條 A／F）、F 3。無 B／C／D／E 類新發現。

## (c) 沒問題的頁

- **v1p3**：未發現附件 R 以外的新問題（R 4 條全已修）。
- **v1p3c**：未發現附件 R 以外的新問題（R 5 條全已修）。
- **v1p5cw**：R 5 條全已修，本輪無新發現（codex 逐頁結論未點名）。
- **v1p5b**：codex 稱「本身的舊問題大致已修，但版面仍過度重複共通資訊」（G4 未修，本輪無新發現）。

其餘頁狀況（codex 逐頁結論）：
- v1p3b、v1p5、v1p5i、v1p5ccc、v1p5c、v1p5cc：仍有會改變實作行為的必修問題。
- v1p2、v1p4、v1p3d：另有契約文字或架構表達問題。

## (d) 總評（codex 原文）

> 本組修正幅度很大，但 `--local` 判別、最低介面版檢查順序、bootstrap 原碼傳出及 install 前置順序仍可能導致錯誤實作，目前尚不能交給使用者看。
