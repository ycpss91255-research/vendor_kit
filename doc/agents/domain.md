# Domain docs

工程類 skill 在探索這個 repo 時，應該怎麼使用領域文件。

## 動手之前先讀這些

- **`doc/decisions/review/01_purpose.md`**：對外契約與承諾（VK 做什麼、對誰承諾什麼）。
- **`doc/decisions/review/02_terms.md`**：名詞與縮寫；定稿後併入根目錄的 **`CONTEXT.md`**（專案的專有名詞表）。
- **`doc/decisions/review/03_invariants.md`**：不變量（承諾背後的固定性質，任何 ADR 不得違反）。
- **`doc/adr/`**：讀跟你要動的範圍有關的 ADR。

**注意**：ADR 0001（測試分層與強制閘門）、ADR 0002（引擎與工具 image 分離，乙版）目前放在 `../proto/vendor_kit/doc/adr/`，還沒整理回本 repo。在搬回來之前，先去那裡讀；本 repo 的 `doc/adr/` 可能是空的或不完整。

上面任一檔不存在時，**安靜略過**：不要指出它缺席，也不要建議先建它。`/domain-modeling` skill（經 `/grill-with-docs` 與 `/improve-codebase-architecture` 觸發）會在名詞或決議真的定下來時才建立。

## 檔案結構

本 repo 是單一語境（single-context）：

```
/
├── CONTEXT.md
├── doc/decisions/review/
│   ├── 01_purpose.md                               對外契約與承諾
│   ├── 02_terms.md                                 名詞（定稿後併入 CONTEXT.md）
│   └── 03_invariants.md                            不變量
├── doc/decisions/design_principles.md              設計原則 P1–P6 與衝突優先序
├── doc/decisions/scope_roadmap.md                  範圍、產品形狀、路線圖
├── doc/adr/
│   ├── 0001-test-layers-and-enforced-gates.md      ← 目前在 ../proto/vendor_kit/doc/adr/
│   └── 0002-engine-and-tool-image-separated.md     ← 同上
├── dist_distribution.drawio       主圖（12 頁）
├── discussion.drawio              討論圖（每題一頁，定案後搬進主圖）
└── dist_distribution_notes.md     討論紀錄
```

## 用名詞表的詞

輸出裡提到領域概念時（issue 標題、重構提案、假設、測試名），用 `CONTEXT.md` 定義的那個詞，不要滑到名詞表明列「避免的說法」裡的同義詞。

需要的概念不在名詞表裡，那是一個訊號：要嘛你在發明專案沒在用的語言（重新考慮），要嘛真的有缺口（記下來給 `/domain-modeling`）。

## 標出跟 ADR 衝突的地方

輸出跟既有 ADR 矛盾時，明講出來，不要默默蓋過：

> _跟 ADR-0002（引擎與工具 image 分離）矛盾，但值得重開，因為……_
