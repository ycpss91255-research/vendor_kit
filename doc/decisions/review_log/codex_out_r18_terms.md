已完成：

- 改寫 [terms.md](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/ws/doc/decisions/review/terms.md)
- 新建 [terms_moved.md](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/ws/doc/decisions/review/terms_moved.md)
- 同步 [disc_v1_a.py](/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/ws/script/diagram/disc_v1_a.py) 的 v1p0 與 `M()`
- 建立兩份指定備份
- `gen_disc.py` 執行成功，已產生 `discussion.drawio`
- 已驗證產生器允許範圍以外逐位元組不變

條數：

- `terms.md`：71 → 61 條
- `terms_moved.md`：35 條移出項目

偏離 brief：

- 唯一不可同時滿足之處：定案段要求逐字不動，但其中有 3 個「／」，與全檔禁用「／」衝突；依優先要求保留定案段原文。其餘禁詞均未出現。
- 未 commit、未 push、未執行 `git add`。