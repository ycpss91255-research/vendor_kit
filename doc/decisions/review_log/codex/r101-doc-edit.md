## 必改

1. **位置：`script/mark_changes.py:64–69`；影響 `doc/decisions/review/README.md:33–38`、`AGENTS.md:19`、`script/README.md:34–40`**

   - **問題：** 文件都宣稱「每跑一次版本號 N 加一」，但程式只從被 `.gitignore` 排除的 `doc/decisions/_marked/.<鍵>.rev` 取號。換電腦、清掉本機產物或新 clone 後，`.rev` 不存在，下一版會從 `v1` 重新開始，即使正式檔已寫著 `> 版本 v10`。這不符合「檔名要帶版本、讓新 agent 對齊」的定案目的。
   - **建議：** `next_rev()` 在 `.rev` 不存在時，至少讀正式檔現有的 `> 版本 vN`，下一版取 `N+1`；若 `.rev` 與正式檔同時存在，取兩者較大值再加一。文件則寫清楚真正的取號來源。
   - **出處：** 維護者 2026-09-30 定案、issue #64；[審閱頁說明第 3 步](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:33)；[工具說明「每跑一次」](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:34)。

2. **位置：`script/mark_changes.py:132–167`；影響 `doc/decisions/review/README.md:33–39`、`script/README.md:34–44`**

   - **問題：** 程式先用尚未更新版本號的正式檔產生 `out`，之後才呼叫 `stamp()`。因此正文副本是 `vN`，但標示版正文仍保留前一個版本號，或根本沒有版本號；只有 HTML 註解聲稱它是 `vN`。兩個交付檔不是同一版內容，與文件「同一版的正文副本」「檔頭版本號跟同編號標示版對齊」不一致。
   - **建議：** 先取得新版本號並更新正式檔，再讀取正式檔產生 diff；或在產生的標示版中同步替換版本行。應加測試確認正式檔、正文副本及標示版三者都含相同的 `> 版本 vN`。
   - **出處：** [工具說明第 3、5 步](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:34)；`mark_changes.py` 的 `build()` 實際順序。

3. **位置：`doc/decisions/review/README.md:27`、`AGENTS.md:18`；`.claude/workflows/doc-edit.js:14–38`**

   - **問題：** 文件把 round 規定為「現有最大 `pre_rNN` 加一、不能重用」，但 workflow 只驗證 round 是非空字串；重用時還明確建立 `.pre_<round>.2.md`，並不拒絕。新 agent 即使照 AGENTS.md 找到流程，輸入錯誤 round 也不會被護欄攔住。
   - **建議：** workflow 應驗證 `round` 符合 `rNN`、等於現有最大值加一，且任何同 round 備份存在時立即失敗；不要以 `.2` 容許重用。若刻意允許重跑同一 round，文件就不能寫「不能重用」，必須另定義重跑語意。
   - **出處：** 維護者 2026-09-30「流程要讓新 agent 能對齊」；issue #64；[審閱頁說明第 2 步](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:27)。

4. **位置：`script/README.md:9–16`**

   - **問題：** 同一段先稱後綴為 `pre_rNN`，隨後又說備份檔名「加上 `.pre_<後綴>`」。按字面會得到 `.pre_pre_r65.md`，但範例與程式實際接受的是 `.pre_r65.md`。
   - **建議：** 統一拆成兩個名詞，例如「round 是 `r65`；基準後綴及備份尾碼是 `pre_r65`」，並把命名公式寫成 `<鍵>.pre_<round>.md`。
   - **出處：** `doc-edit.js:16–17, 49` 的 `round: "r90"` 與 `.pre_${round}.md`；`mark_changes.py:87–108` 的實際查找規則。

5. **位置：`script/README.md:9`**

   - **問題：** 「走 doc-edit workflow 時自動備份；手動改才自己備份」暗示手動改是可接受分支；另外兩份文件則明定所有文件改動「一律／照樣走 doc-edit workflow」。三份文件對是否存在手動流程說法不一致。
   - **建議：** 刪除「手動改才自己備份」，或明確標成歷史／救援情境，並說正常改動不得繞過 doc-edit。
   - **出處：** [審閱頁說明第 2 步](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:27)；[AGENTS.md 文件流程](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:16)。

6. **位置：`script/README.md:18`**

   - **問題：** 「改（派子代理做，主對話只協調）」被寫成整套標示工具的一般流程，但真正擁有這項行為的是 `doc-edit.js`；`mark_changes.py` 並不派代理。離開該 workflow 單看工具說明，讀者會誤以為腳本有代理編排能力。
   - **建議：** 改成「由 doc-edit workflow 的改寫階段派子代理修改；本工具只在修改完成後產生標示版」，並連到具名的 workflow 說明。
   - **出處：** `.claude/workflows/doc-edit.js:5–10, 62–78`；`mark_changes.py` 僅處理版本、差異及輸出檔。

## 建議

1. **位置：`AGENTS.md:4、7、10、14–15、23、30`**

   - **問題：** 多處以行內程式碼路徑代替可導航連結，例如「見 `doc/agents/issue-tracker.md`」「ADR 見 `doc/adr/`」。它們不是無名 Markdown 超連結，但實際承擔導覽用途，與本文件要求的「連結要有名字」不一致。新 agent 需自行複製路徑。
   - **建議：** 把承擔導覽用途的路徑改成 `[issue tracker 規則](doc/agents/issue-tracker.md)`、`[領域文件規則](doc/agents/domain.md)` 等具名連結；純粹描述檔名格式的路徑仍可保留行內程式碼。
   - **出處：** [審閱頁寫法規則](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:20)。現有 Markdown 超連結本身都有名稱，所有本機目標也都存在。

2. **位置：`AGENTS.md:16–20`**

   - **問題：** 新 agent 能從 AGENTS.md 找到完整流程，但摘要缺少「在 repo 根目錄執行」「審閱頁參數不含 `.md`、根 README 要傳 `README.md`」及版本計數狀態的位置。若 agent 只讀摘要而未跟連結，容易用錯參數。
   - **建議：** 在「重點」開頭明寫「以下只是摘要，執行前必須讀連結章節與工具說明」；不必把所有細節複製進 AGENTS.md。
   - **出處：** [審閱頁說明「版本怎麼迭代」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:22)；[工具說明一輪流程](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:7)。

3. **位置：`doc/decisions/review/README.md:27`**

   - **問題：** 一句同時承載 workflow 階段、備份時機、命名公式、round 生成規則及查詢指令引介，第一次閱讀很難辨認哪些由 workflow 自動完成、哪些要人在啟動前完成。
   - **建議：** 拆成「人先決定 round」與「workflow 在首次修改前備份」兩段；明確標出查最大編號是啟動 workflow 前的動作。
   - **出處：** `.claude/workflows/doc-edit.js:14–38` 的參數與護欄分工。

4. **位置：`script/README.md:40`**

   - **問題：** 一句混合舊檔清理、正式檔命名、鍵的算法及後綴用途，過長且「其他檔」範圍不清；本工具實際也接受 `doc/decisions/review/README.md` 這類內部文件路徑，儘管流程規定不應替內部文件產標示版。
   - **建議：** 分成「清理」「鍵」「基準後綴」三項，並補一句：工具雖能接受任意 Markdown 路徑，流程上只准對外文件使用。
   - **出處：** `mark_changes.py:73–84` 的 `target()`；[審閱頁說明內外文件界線](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:41)。

5. **位置：`AGENTS.md:30`**

   - **問題：** CI workflow、job、ruleset、未來 lint/test 拆分和 paths 限制全塞在同一句；「之後的程式碼 lint」也不清楚是已定案但未實作，還是單純規劃。
   - **建議：** 拆成現況與未來兩句，將尚未存在的部分明標「規劃」。
   - **出處：** `.github/workflows/docs.yml`；本檔「內部文件不准留過時資訊」規則。

6. **位置：三份受審文件的名詞標記**

   - **問題：** `_Avoid_` 自檢目前全數通過，沒有發現禁用詞；但 `<ins>` 使用不一致：審閱頁有標 `<ins>VK</ins>`、`<ins>契約</ins>` 等，AGENTS.md 與 script/README.md 的首次出現則未標。若「名詞底線用 `<ins>`」適用所有三份文件，後兩份沒有遵守。
   - **建議：** 明確決定規則範圍：若只適用對外審閱頁，就在寫法規則中寫明；若內部文件也適用，補上每份文件首次出現的正式名詞標記。不要把一般流程詞硬塞進 CONTEXT.md。
   - **出處：** [審閱頁寫法規則](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:15)；`CONTEXT.md`；`check_terms.py` 結果為 21 個 `_Avoid_` 詞零殘留。

7. **位置：整體正確性**

   - **問題：** 除上述流程／實作落差外，未發現三份文件把 01、02 或 ADR 的產品契約說錯。`AGENTS.md:36` 將「主機只需 Docker、Git、just」限定為 VK 對使用者的承諾，而非 repo 作者流程限制，這與不變量 5 及 ADR-0001、ADR-0007 一致。三份文件也沒有錯標 01、02 條號。
   - **建議：** 保留這個界線；修訂流程文件時不要把作者工具限制誤寫成不變量 5 的內容。
   - **出處：** `doc/decisions/review/02_invariants.md` 第 5 條；ADR-0001；ADR-0007。