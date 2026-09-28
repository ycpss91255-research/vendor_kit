# _legacy/workflows — 已停用的 workflow 腳本

`.claude/workflows/` 裡跑過但已經不再用的腳本。留著是為了看當初的 prompt 結構與護欄措辭，不要再調用。

- `diagram-review.js` — draw.io 圖檔雙軌審查（Claude 子代理看圖 + codex 獨立審查，交叉比對後逐條驗證）；圖已停在第十五版不再修改，審查流程沒有對象了。
- `diagram-review-claude.js` — 同上的單軌版（codex 不可用時，改用兩個獨立 Claude 子代理）；同樣因為圖不再修改而停用。
- `diagram-review-v2.js` — 三階段 draw.io 審查（機械抽取＋lint 先跑，代理只做內容／連接、排版縮圖、一格一事判定，最後逐條驗證）；圖已停在第十五版不再修改。
- `decision-review.js` — 設計決議雙軌分析，綁 agy 前例研究的輸出（agy 報告＋brief＋草稿一起送兩軌交叉比對）；agy 研究階段結束，已由 `.claude/workflows/doc-review.js` 取代。
