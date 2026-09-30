## 必改

1. **位置：AGENTS.md 第 17 行**

   **問題：** 引用不存在的 `to-spec` skill，屬於已不存在做法。現行負責把 PRD 發到 issue tracker 的 skill 是 `to-prd`。

   **建議：** 把兩處 `to-spec` 改為 `to-prd`；若不想綁定 skill 名稱，可改成「會把規格發布到 issue tracker 的 skill」。

   **證據：** `.agents/skills/to-prd/SKILL.md` 第 2～3、19 行；AGENTS.md 第 24 行又明定內部文件不准保留已不存在的做法。

2. **位置：AGENTS.md 第 27 行**

   **問題：** 同一句先斷言架構圖「是測試的依據」，後面又承認相關 lint「尚未實作」。目前圖既未受測試強制，而且現存圖仍是舊模型，因此「是測試的依據」不是現況，容易讓 agent 錯把圖當成可靠真本。

   **建議：** 改成「架構圖預定成為測試依據」；在 lint 落地以前，明寫不得把圖當成已受強制的現況依據。

   **證據：** `doc/decisions/README.md` 第 54～60 行，尤其第 58 行明載「lint 還沒寫」及圖與現行名詞未同步；AGENTS.md 第 27 行自身也寫「目前尚未實作」。

## 建議

1. **位置：AGENTS.md 第 10 行**

   **問題：** 四個主要領域文件以行內路徑呈現，不可直接點擊。雖然這些不是錯誤的 Markdown 連結，而且路徑都存在，但第一次閱讀的人必須手動找檔，與本檔其他「見某文件」的寫法不一致。

   **建議：** 改成有名稱的超連結，例如 `[目的與承諾](docs/contract/01_purpose.md)`、`[名詞表](GLOSSARY.md)`。

   **證據：** `docs/contract/README.md` 第 23 行要求連結使用有名字的超連結；四個目標路徑均存在。

2. **位置：AGENTS.md 第 22 行**

   **問題：** 一句同時交代輸出目錄、兩種產物、版本號出現位置、版本計算方式、新 clone 行為及正式檔名，資訊過密，第一次看不容易分辨「正文副本」與「正式檔」。

   **建議：** 拆成三點：產物與位置、版本號規則、正式檔規則。

   **證據：** `docs/contract/README.md` 第 36～41 行已將相同內容分段表達。

3. **位置：AGENTS.md 第 32 行**

   **問題：** 單一項目混合分支保護、本機 hook、三類 workflow、job 命名、測試目錄歸屬及 `paths` 限制，閱讀時很難確認每條規則的適用範圍。

   **建議：** 至少拆成「進 main 的方式」「CI 分工」「必過 workflow 不設 paths 過濾」三個子項。

   **證據：** `.github/workflows/docs.yml` 第 1～31 行將同一規則拆成檔案註解、觸發條件及兩個 job；`.claude/hooks/guard.py` 第 399～439 行只負責阻擋 push 到 `main`。

4. **位置：AGENTS.md 第 13 行**

   **問題：** `pr/<N>`、`issue/<N>`、`branch/<名>` 看起來像已存在的固定目錄，而目前 `worktree/` 下只有 `pr/`。若這是在規定命名方式，句子沒有明說。

   **建議：** 改成「worktree 路徑約定為……」，避免被理解成三種目錄都已建立。

   **證據：** `/home/cyc/Desktop/vendor-kit_ws/worktree/` 目前只有 `pr/` 及其 worktree；AGENTS.md 第 13 行未區分現況與命名約定。