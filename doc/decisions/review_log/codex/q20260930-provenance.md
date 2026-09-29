## 結論

不保留介面頁與根 README 中獨立的「出處：……」行。介面頁可保留必要的規範性前向引用，例如「依 02 第 8 條」；README 只保留使用者操作所需的文件、下載與進度連結，不把 ADR、issue 或歷史決議包裝成對外契約的「出處」。

## 理由

1. 「出處」混淆了權威契約與形成契約的歷史材料。介面頁本身就是對外契約的權威文件，不應呈現成由 ADR 或 issue 派生的摘要。[doc/decisions/README.md:15](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:15) 將 01 定義為對外契約的權威文件，[同檔第 17 行](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:17)也把介面頁定義為對外契約，且只要求規則標示 02 條號。相反地，ADR 負責機制與理由：[doc/adr/README.md:21](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/README.md:21)、[doc/adr/README.md:22](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/README.md:22)。

2. 對外頁引用 ADR 與 issue，會違反已定案的前向依賴規則。現有介面頁不只回指 01、02，還直接依賴 ADR 與 issue，例如主機需求引用 ADR-0007 與 issue #71（[03_interface.md:28](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:28)）、離線導入引用 ADR-0009（[03_interface.md:138](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:138)）、CI 模式引用 ADR-0004（[03_interface.md:174](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:174)）。依已定前提，介面成為 04 後只能依賴 01、02、新 03 與 `CONTEXT.md`；這些 ADR／issue 出處必須移除。保留「02 第 N 條」則是合法且有用途的規範對應。

3. `ADR-0007 §1` 不是穩定、已定義的引用格式。ADR 規則只定義六個必要部分，沒有定義 `§N` 語法或永久節號（[doc/adr/README.md:13](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/README.md:13)–[24](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/README.md:24)）；ADR-0007 實際標題是 `### 1. 主機依賴的版本下限`（[ADR-0007:19](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:19)–[24](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:24)）。因此 `§1` 只是人工約定的文字，既不是 Markdown 連結，也沒有規則保證重排後仍指同一內容。

4. 目前架構已經提供較可靠的反向追溯，不需要在每個對外敘述旁重複 provenance。02 明定「性質在本頁、機制和理由在 ADR」，並由各條列出服務它的 ADR（[02_invariants.md:5](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:5)）；例如不變量 6 回連 ADR-0007 與 ADR-0006（[02_invariants.md:211](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:211)–[215](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:215)）。ADR 端又必須以 `> Serves:` 回連它服務的不變量（[doc/adr/README.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/README.md:3)、[doc/adr/README.md:19](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/README.md:19)）。這種「ADR → 不變量」的責任方向比「每份對外頁 → ADR／issue」更符合既有分工。

5. README 的主要讀者需要可操作資訊，不需要決議流水帳。README 現有文件導覽已提供不變量、介面、名詞表與 ADR 的入口（[README.md:58](/home/cyc/Desktop/vendor-kit_ws/src/README.md:58)–[64](/home/cyc/Desktop/vendor-kit_ws/src/README.md:64)）；主機需求後再列 ADR、02、issue 三重出處（[README.md:27](/home/cyc/Desktop/vendor-kit_ws/src/README.md:27)）沒有增加操作資訊，反而模糊哪一份才是現行規範。下載尚未發布及追蹤進度則不同：issue #27 是即時狀態連結，現有警告確實需要它（[README.md:31](/home/cyc/Desktop/vendor-kit_ws/src/README.md:31)）。應保留為「進度見……」，而不是「下載網址出處」。

6. 不是 skill 的要求。repo 自己明說 `doc/decisions/` 不在 skill 結構中，對外契約頁是本 repo 刻意增設的文件體系（[doc/decisions/README.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:3)）。此外，現行 ADR 必要段落規則要求的是 ADR 自己的 `> Serves:`、Context、Decision 等結構，沒有要求 README 或介面頁逐段列「出處」（[doc/adr/README.md:15](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/README.md:15)–[24](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/README.md:24)）。「出處」行來自近期文件編修，不是 skill 所強制；這是依 git blame／歷史作出的判斷。

## 風險或反例

- 移除所有對應標記會降低審查時核對「介面規則受哪條不變量約束」的效率。因此不應連 `02 第 N 條` 一起刪掉；建議把它保留成簡短的規範標記，而不是稱為「出處」。介面頁目前也明定「這裡只標條號，不重述」（[03_interface.md:7](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:7)）。
- 某些外部連結不是 provenance，而是使用者完成操作所必需，例如軟體官方下載頁（[03_interface.md:21](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:21)）或尚未發布功能的進度 issue（[README.md:31](/home/cyc/Desktop/vendor-kit_ws/src/README.md:31)）。這些應依用途保留，不應因刪除「出處」行而一併刪除。
- 推論：若維護者仍需要「一句介面規則最初在哪個 issue 定案」的逐句追溯，應由 git 歷史、ADR Context 或內部審閱紀錄承擔；把它留在對外頁會同時製造依賴方向、權威來源及閱讀噪音三個問題。