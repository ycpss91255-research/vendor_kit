你是圖面審查者。**只讀、不要改任何檔**。我要的是你**不同的建議**，不是替圖背書。

附圖是 vendor_kit（VK）「dev 流程」頁的匯出圖。原始檔是 `doc/decisions/research/diagram_proposals/proposal_claude_v3.drawio` 的頁 id `c-dev`。它畫的是：使用者 just vendor_kit dev 讓工具（dev <repo> -p <dir>）或引擎（dev vendor_kit -i <image>）改用本機開發來源的流程

## 先讀的東西（圖要對齊它們）
- `doc/decisions/review/01_purpose.md`
- `doc/decisions/review/02_invariants.md`
- `CONTEXT.md`
- `script/diagram/STYLE.md`
- `doc/adr/（全部）`

## 已經定下的規則（不要再建議推翻它們）
- 標題寫在頁名，頁面上不放標題
- 泳道 = 誰做（STYLE §4.4）；引擎寫進 repo 的動作放引擎欄
- 層級 = 使用者視角：執行紀錄、進度檔、預檢、退出碼 3、取件細節、要改先問的 -y／CI 規則另開共用頁，不要因為沒畫它們而列為缺漏
- 黃菱形 = 判斷、綠橢圓 = 起點／終點、紅橢圓 = 錯誤終止、橘橢圓 = 需人接手、白色圓角 = 步驟；終點裡的數字 = 退出碼
- 文字不壓線、不壓泳道邊界；版面要緊湊
- 契約出處：CONTEXT.md「dev / undev」「本機覆寫」「本機開發來源」；不變量 2（本機覆寫是開發模式的例外、`version.local.toml` 不進 git、CI 模式下有任何本機覆寫 → 1）；不變量 8（dev 是常用三個之一，與 undev 成對）；ADR-0010（`dev vendor_kit -i <image>` 寫 version.local.toml 的引擎覆寫）。舊規格 `doc/decisions/_backup/interface_spec.pre_r54.md` 的 dev 列（工具必須已在 version.toml、`<dir>/dist/init.toml` 必須存在、CI 拒絕）可參考，但以現行契約為準
- 這頁只畫 dev，不畫 undev

## 請回答
1. **正確性**：每個判斷、分支、順序、退出碼、步驟所在的泳道，跟契約有沒有對不上的地方？逐條列，附出處（檔名＋條號或節號）。
2. **缺漏**：這個流程中契約規定、使用者看得到、但圖上沒畫的判斷或結果？
3. **多餘**：不該出現在這一頁的東西？
4. **可讀性**：第一次看的人哪裡會看不懂或誤讀？指出是哪一格或哪一條線。
5. **你會怎麼畫得不一樣**：每一條寫理由，並說明跟上面已定的規則有沒有衝突。

輸出 markdown。每一條寫：位置、問題、建議、理由。分「必改（跟契約衝突）」「建議」「只是不同做法」三類。不要客套話。
