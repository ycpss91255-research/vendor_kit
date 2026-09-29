## 必改

1. **位置：** [script/README.md:5](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:5)、[script/README.md:48](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:48)、[script/README.md:49](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:49)、[script/README.md:50](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:50)  
   **問題：** 標示規則與實作不一致。文件說新增用 `<mark>`、刪除用 `<del>`，又以 `## <ins>目錄</ins>` 示範；實作其實不產生 `<del>` 或用來標改動的 `<ins>`，新增與舊文字都用 `<mark style="background:…">`，分別是綠底與紅底。  
   **建議：** 全部統一寫成「新增文字用綠底 `<mark>`；刪除或被取代的舊文字用紅底 `<mark>`」，標題範例改為實際輸出形狀。不要再說有刪除線。  
   **出處：** [script/mark_changes.py:30](/home/cyc/Desktop/vendor-kit_ws/src/script/mark_changes.py:30)、[script/mark_changes.py:35](/home/cyc/Desktop/vendor-kit_ws/src/script/mark_changes.py:35)、[script/mark_changes.py:57](/home/cyc/Desktop/vendor-kit_ws/src/script/mark_changes.py:57)、[script/mark_changes.py:124](/home/cyc/Desktop/vendor-kit_ws/src/script/mark_changes.py:124)。

2. **位置：** [doc/decisions/README.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:3)、[doc/decisions/README.md:15](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:15)、[doc/decisions/README.md:70](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:70)–[76](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:76)  
   **問題：** 把 `doc/decisions/`、01、02 描述成終將分流、退場、消失的過渡產物，和已定案的文件流程正面衝突。01、02 是對外契約與不變量的 repo 內權威文件，不能再列成待決定落點。  
   **建議：** 刪除「每一份都是過渡產物」「01 拆完退場」「目錄分流完就該消失」及第 3 項的待選方案；改寫成這個目錄刻意承載對外契約、不變量、設計原則與範圍文件。  
   **出處：** [AGENTS.md「決議與文件流程」](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md)、[01_purpose.md](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md)、[02_invariants.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:3)。

3. **位置：** [doc/decisions/README.md:9](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:9)、[doc/decisions/README.md:15](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:15)–[16](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:16)、[doc/decisions/README.md:29](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:29)  
   **問題：** 現況仍寫「審閱中的兩頁」與「這輪（01–02）」，但 `review/03_interface.md` 已存在且已進 git；同一份文件沒有列它。  
   **建議：** 改成三頁並補上 03 的列與現況；若 03 不該算審閱頁，則應由權威流程明確說明，而不是讓兩份 README 互相矛盾。  
   **出處：** [review/README.md:7](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:7)–[11](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:11)、[03_interface.md](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md)。

4. **位置：** [doc/decisions/README.md:15](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:15)  
   **問題：** 「對三種角色各承諾什麼」不對。01 只定義兩方：使用者與 VK；後面三組是「導入、出貨、相容性」承諾，不是三種角色。  
   **建議：** 改成「對導入、出貨與相容性承諾什麼」。  
   **出處：** [01_purpose.md:35](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:35)–[40](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:40)、[01_purpose.md:60](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:60)–[83](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:83)。

5. **位置：** [doc/decisions/README.md:16](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:16)  
   **問題：** 說機制在 ADR 0002–0012，漏掉 0001。02 第 5 條明列 ADR-0001；ADR-0001 的 `Serves` 也明說服務不變量 5。  
   **建議：** 改成 0001–0012，或避免用連號概括，直接說「各條列出的 ADR」。  
   **出處：** [02_invariants.md:186](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:186)、[ADR-0001:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0001-why-not-existing-tools.md:3)。

6. **位置：** [doc/decisions/README.md:29](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:29)–[31](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:31)、[doc/decisions/README.md:88](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:88)、[doc/decisions/README.md:96](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:96)–[102](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:102)  
   **問題：** 數量與容量已過時：目前 `review_log/` 是 62 檔、約 1.5 MB；`_backup/` 是 100 檔、約 3.2 MB，不是 48／56 檔與 1.3／2.5 MB。第 102 行的舊輪次「21 個」依列名實際也已不是該數字。  
   **建議：** 更新數字；更穩妥的是移除易腐敗的精確檔數與容量，只保留用途和退場條件。  
   **出處：** 目前工作樹的 `find`、`du` 唯讀結果。

7. **位置：** [.claude/workflows/README.md:24](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/README.md:24)–[31](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/README.md:31)  
   **問題：** 「現有 workflow」只列 `doc-apply`、`doc-review`，漏掉現存且已被 `review/README.md` 指定為一律使用的 `doc-edit`。因此「兩個都有……」也無法涵蓋實際三個 workflow。  
   **建議：** 表格補 `doc-edit`，列出其 `round`、`files` 等必填欄位及流程；後面的共通欄位說明改成逐一準確描述。  
   **出處：** [.claude/workflows/doc-edit.js](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/doc-edit.js)、[review/README.md:27](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:27)。

8. **位置：** [.claude/workflows/README.md:128](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/README.md:128)–[134](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/README.md:134)  
   **問題：** 宣稱 codex 指令形狀「固定」，但 `doc-review` 直接放 `"<brief>"`，`doc-edit` 則先寫暫存檔，再用 `"$(cat <暫存檔>)"`。不是一字不差的共同形狀。  
   **建議：** 只固定真正共同的部分：`codex exec --skip-git-repo-check -C … -o …`、不加 sandbox、stdin 來自 `/dev/null`；分別列出兩種 prompt 傳遞方式。  
   **出處：** [.claude/workflows/doc-review.js:125](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/doc-review.js:125)–[132](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/doc-review.js:132)、[.claude/workflows/doc-edit.js:153](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/doc-edit.js:153)–[160](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/doc-edit.js:160)。

9. **位置：** [script/README.md:86](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:86)、[doc/decisions/README.md:15](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:15)–[23](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:23)、[.claude/workflows/README.md:151](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/README.md:151)  
   **問題：** 這些連結以裸路徑作連結文字，例如 `diagram/README.md`、`review/01_purpose.md`、`../../doc/decisions/_legacy/workflows/`，違反本 repo 自己訂的「連結要有名字，不要把路徑當連結文字」。  
   **建議：** 分別改為「圖面工具說明」「01 專案目的與承諾」「02 不變量」「設計原則」「範圍與路線圖」「已歸檔 workflows」等描述性文字。  
   **出處：** [review/README.md:20](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:20)。

10. **位置：** [doc/decisions/review/README.md:11](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:11)  
    **問題：** 使用「全部指令」，但 `CONTEXT.md` 對 VK 的正式名稱是「VK recipe」；「指令」沒有定義。這不是一般敘述裡偶然出現，而是在描述 03 的契約內容。  
    **建議：** 改成「全部 VK recipe、選項、結束碼」，或先在 `CONTEXT.md` 明確定義「指令」與 recipe 的關係。  
    **出處：** [CONTEXT.md:312](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:312)–[315](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:315)。

## 建議

1. **位置：** [script/README.md:16](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:16)  
   **問題：** 「加上 `.pre_<後綴>`」容易讓人把命令參數 `pre_r65` 再加一次 `pre_`。實作把傳入的舊版後綴原樣接到點號後；workflow 的 `round` 才是另外轉成 `pre_<round>`。  
   **建議：** 區分兩層名稱：workflow 的輪次 `r65` 產生備份後綴 `pre_r65`；`mark_changes.py` 接收的則是完整舊版後綴 `pre_r65`。  
   **出處：** [mark_changes.py:86](/home/cyc/Desktop/vendor-kit_ws/src/script/mark_changes.py:86)–[99](/home/cyc/Desktop/vendor-kit_ws/src/script/mark_changes.py:99)、[doc-apply.js:55](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/doc-apply.js:55)。

2. **位置：** [script/README.md:9](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:9)–[16](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:16)、[doc/decisions/README.md:30](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:30)  
   **問題：** 兩處介紹 `_backup/`，卻沒有當場說它與 `_marked/` 一樣只在本機、不進 git；只有 `review/README.md` 說完整。第一次只讀其中一份的人容易誤判。  
   **建議：** 第一次介紹 `_backup/` 時補一句「只在本機，已由 `.gitignore` 排除」。  
   **出處：** [.gitignore:4](/home/cyc/Desktop/vendor-kit_ws/src/.gitignore:4)–[8](/home/cyc/Desktop/vendor-kit_ws/src/.gitignore:8)、[review/README.md:33](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:33)。

3. **位置：** [doc/decisions/README.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:3)、[doc/decisions/README.md:70](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:70)–[84](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:84)  
   **問題：** 句子同時塞入 skill 結構、文件定位、退場路線和未決方案；即使修正內容，第一次閱讀仍很難分清「現在的權威位置」和「歷史整理計畫」。  
   **建議：** 首段只回答「這裡現在放什麼、哪份是權威」；歷史清理另立一節，且只保留仍未完成的項目。  
   **出處：** [AGENTS.md「Agent skills」與「決議與文件流程」](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md)。

4. **位置：** [.claude/workflows/README.md:7](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/README.md:7)–[12](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/README.md:12)  
   **問題：** 第 9 行過長，一句內解釋控制流、資料、迷你語言與 `meta` 限制；新讀者要反覆拆句。  
   **建議：** 拆成「流程為何必須是 JS」與「`meta` 為何不算流程」兩段。  
   **出處：** 同檔實際 workflow 結構。

5. **位置：** 四份文件整體  
   **問題：** 沒有發現 `review/_marked` 或 `doc/decisions/review/_marked` 的現行殘留；排除 `.git/`、`review_log/`、`_backup/`、`_legacy/` 後 grep 為零。所有列出的超連結目標也都存在；issue #60 存在且標題吻合。`check_terms.py` 通過：掃描 30 個 Markdown、21 個 `_Avoid_` 詞，沒有未豁免殘留。  
   **建議：** 不要為這三項再改內容；只修上面列出的連結文字與「指令」用詞。  
   **出處：** 全 repo 唯讀 grep、[check_terms.py](/home/cyc/Desktop/vendor-kit_ws/src/script/check_terms.py)、GitHub issue #60 查核結果。