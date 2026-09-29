## 必改

1. **位置：** [script/README.md:9](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:9)、[script/README.md:48](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:48)  
   **問題：** 手動建立 `*.pre_rNN.md` 的救援範例與目前的 round 護欄衝突。只要先建立 `pre_r66`，workflow 就會把最大編號視為 66，要求下一輪使用 `r67`；因此第 48–53 行宣稱該檔可作「下一輪」基準並不成立。它也可能覆寫 workflow 保證為「修改前原檔」的無序號備份。  
   **建議：** 移除一般流程中的手動 `cp`／`git show > ...pre_rNN.md`；說明下一輪應從 `main` 建立討論分支，再由 doc-edit 自動備份。若確實保留救援程序，需明定使用時機及後續必須換新 round，不能把它稱為下一輪可直接使用的備份。  
   **出處：** [.claude/workflows/doc-edit.js:51](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/doc-edit.js:51)、[.claude/workflows/doc-edit.js:69](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/doc-edit.js:69)、[doc/decisions/review/README.md:27](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:27)。

2. **位置：** [doc/decisions/review/README.md:13](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:13)、17、26、27、33、39、42、44  
   **問題：** 多個 repo 內連結以 `/` 開頭，例如 `/AGENTS.md`、`/README.md`、`/.claude/workflows/doc-edit.js`。在 GitHub Markdown 中，這會解析成網站根路徑，而不是目前 repository 根目錄；檔案雖存在，實際超連結目標不對。  
   **建議：** 全部改為從本檔位置出發的相對路徑，例如 `../../../AGENTS.md`、`../../../README.md`、`../../../.claude/workflows/doc-edit.js`。  
   **出處：** 本檔「寫法規則」第 20 行要求連結目標正確；上述目標檔案均存在於 repo，但不在 GitHub 網站根路徑。

3. **位置：** [script/README.md:5](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:5)、18、42  
   **問題：** repo 內連結同樣使用 `/doc/...`、`/.claude/...`、`/test/...`，在 GitHub 上不會指向本 repository。  
   **建議：** 改用相對於 `script/README.md` 的路徑，例如 `../doc/decisions/review/README.md`、`../.claude/workflows/doc-edit.js`、`../test/test_mark_changes.py`。第 95 行的 `diagram/README.md` 已是正確形狀。  
   **出處：** [doc/decisions/review/README.md:20](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:20)、[.claude/workflows/doc-edit.js:54](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/doc-edit.js:54)。

4. **位置：** [AGENTS.md:4](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:4)、7、10  
   **問題：** 三句都以「見 `路徑`」作交叉引用，但路徑只是行內程式碼，不是有名字的超連結，違反目前文件護欄。  
   **建議：** 改成 `[issue tracker 約定](doc/agents/issue-tracker.md)`、`[triage 標籤](doc/agents/triage-labels.md)`、`[domain 文件約定](doc/agents/domain.md)`。  
   **出處：** [doc/decisions/review/README.md:20](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:20)、[.claude/workflows/doc-edit.js:54](/home/cyc/Desktop/vendor-kit_ws/src/.claude/workflows/doc-edit.js:54)。

## 建議

1. **位置：** [doc/decisions/review/README.md:33](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:33)–39  
   **問題：** `<鍵>` 在第 35、37 行已經使用，到第 39 行才解釋。第一次操作的人必須先猜它是頁名、路徑還是檔名。  
   **建議：** 把第 39 行的鍵規則移到指令之前，並先給 `02_invariants → 02_invariants`、`README.md → README` 兩個例子。  
   **出處：** [script/README.md:40](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:40)、[script/mark_changes.py:84](/home/cyc/Desktop/vendor-kit_ws/src/script/mark_changes.py:84)。

2. **位置：** [doc/decisions/review/README.md:33](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:33)–37、[script/README.md:34](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:34)–40  
   **問題：** 「正式檔」「正文副本」「標示版」連續出現，但沒有先用一句話說清三者關係。第一次看的人容易把「正式檔」理解為已定案或已 merge 的版本；實際上它只是原路徑上的工作檔。  
   **建議：** 首次出現時定義：「正式檔＝原路徑上正在修改、會進 git 的檔；正文副本與標示版＝`_marked/` 下的本機送審產物。」  
   **出處：** [script/mark_changes.py:143](/home/cyc/Desktop/vendor-kit_ws/src/script/mark_changes.py:143)–177。

3. **位置：** [script/README.md:44](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:44)  
   **問題：** 「基準永遠是審閱者上次看過的那一版」寫成工具保證，但程式只依呼叫者提供的後綴找備份，無法判斷審閱者實際看過哪一版。  
   **建議：** 改成操作責任，例如「傳入的基準應是審閱者上次看過的版本；工具不會自行判定。」  
   **出處：** [script/mark_changes.py:143](/home/cyc/Desktop/vendor-kit_ws/src/script/mark_changes.py:143)–146。

4. **位置：** [script/README.md:5](/home/cyc/Desktop/vendor-kit_ws/src/script/README.md:5)  
   **問題：** 「審完只留最終版」不精確。程式每次執行就刪除同鍵舊產物，留下的是「最新產生版」，不一定已經定案或審完。  
   **建議：** 改成「每次產生時刪除同鍵舊產物，只留最新產生的一版」。  
   **出處：** [script/mark_changes.py:172](/home/cyc/Desktop/vendor-kit_ws/src/script/mark_changes.py:172)–177。

5. **位置：** [doc/decisions/review/README.md:40](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:40)  
   **問題：** `SendUserFile` 是未解釋的環境專名；新接手的 agent 不知道它指哪個工具，也不知道工具不存在時該怎麼交付。  
   **建議：** 補一句工具所在環境或替代方式；若名稱已過時，換成目前實際使用的傳檔方法。  
   **出處：** 本檔第 24 行宣稱本節供「新接手的 agent」直接依序操作。

6. **位置：** [AGENTS.md:18](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:18)–19、[AGENTS.md:23](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:23)、[AGENTS.md:30](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:30)  
   **問題：** 單句同時塞入規則、演算法、理由與失敗結果，尤其第 19 行的取號和三種輸出，掃讀困難。  
   **建議：** 第 18、19 行各拆成「規則」與「結果」兩句；第 23 行把 `Serves` 可連到的三類目標改成子清單；第 30 行把 push 規則與 CI workflow 規則拆成兩項。  
   **出處：** 同一資訊在 [doc/decisions/review/README.md:27](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:27)–40 已按步驟拆開，可作精簡依據。

7. **位置：** 三份文件整體  
   **問題：** 未發現與 01、02、CONTEXT.md 或 ADR 相反的產品承諾；所標的不變量 5、ADR 職責、對外／內部文件界線均對得上。`check_terms.py` 亦回報 21 個 `_Avoid_` 詞零殘留。其餘 Markdown 連結都有名稱，本機目標也都存在；issue #60、#64 亦存在。  
   **建議：** 不需為名詞或產品契約另作修改；只處理上述流程矛盾、連結解析及可讀性問題。  
   **出處：** [01_purpose.md](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md)、[02_invariants.md](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md)、[CONTEXT.md](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md)、ADR-0001～0012。