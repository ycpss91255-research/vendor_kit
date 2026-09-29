## 必改

- **位置：** [03_interface.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:3)、同檔第 11、21、67、68、78 行  
  **問題：** repo 內連結以 `/doc/...`、`/CONTEXT.md` 開頭。這是網站根目錄路徑；在 GitHub 上不會指向此 repo，實際解析為 `github.com/doc/...` 等錯誤位置。  
  **建議：** 全部改成相對於 `doc/decisions/review/` 的路徑，例如 `02_invariants.md`、`../../../CONTEXT.md`、`../../adr/0007-….md`、`01_purpose.md`。  
  **出處：** Markdown 相對連結解析；對照 01、02 與 ADR-0010 現有的相對路徑寫法。

- **位置：** [03_interface.md:18](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:18)、[README.md:20](/home/cyc/Desktop/vendor-kit_ws/src/README.md:20)、[README.md:24](/home/cyc/Desktop/vendor-kit_ws/src/README.md:24)  
  **問題：** `releases/latest/download/bootstrap.sh` 目前實際回傳 HTTP 404；對外文件卻寫成現在即可下載與執行。issue #27 仍是 open，交付項目也尚未完成。  
  **建議：** 送審前要嘛先發布含 `bootstrap.sh` 的 release，要嘛明確標示尚未可用；不能保留成可直接照做的現行說明。  
  **出處：** 實際 URL 回應 404；issue #27「先記錄、不實作」及未完成 checklist。

- **位置：** [0010-dev-self-and-acceptance.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0010-dev-self-and-acceptance.md:3)、[0010-dev-self-and-acceptance.md:63](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0010-dev-self-and-acceptance.md:63)  
  **問題：** 修訂只說「第 1、5、6 節」的舊寫法已改，但 `Serves` 與 `Consequences` 也仍以現在式使用 `dev vendor_kit -i`。它們不在修訂宣告的涵蓋範圍內，因此第一次閱讀者仍可能把舊寫法當現行介面。第 19、41、43 行則確實是被修訂涵蓋的歷史正文，不算漏改。  
  **建議：** 不必改寫歷史正文；在修訂段明列「本檔所有 `dev vendor_kit -i …` 舊拼法，包括 `Serves` 與 `Consequences`，現均讀作 `dev --engine -i …`」，或逐項列出受修訂位置。  
  **出處：** issue #65；ADR-0010 第 54–59 行；`doc/adr/README.md` 第 26 行的修訂規則。

- **位置：** [03_interface.md:67](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:67)  
  **問題：** 「工具的 image」沒有使用名詞表正式詞「工具 image」，也容易與本次新增、專指引擎來源的「本機 image」混淆。  
  **建議：** 改成「從本機取得工具 image」。  
  **出處：** `CONTEXT.md`「工具 image」「本機開發來源」。

## 建議

- **位置：** [0010-dev-self-and-acceptance.md:19](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0010-dev-self-and-acceptance.md:19)、同檔第 59 行；[03_interface.md:33](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:33)  
  **問題：** ADR 把值寫成 `<本機 image tag>`，公開介面則寫 `<image>`。讀者無法判斷 `-i` 是否只接受 tag，還是也接受 image ID 或其他本機 image 引用。  
  **建議：** 若只接受 tag，在 03 明寫限制並把 placeholder 統一成 `<tag>`；若接受一般本機 image，ADR 不要再限定為 tag。  
  **出處：** `CONTEXT.md`「tag」「image 引用」「本機開發來源」；issue #65 使用 `<image>`。

- **位置：** [02_invariants.md:282](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:282)  
  **問題：** 「本機開發 VK 自己」把代表承諾方的「VK」與實際被替換的「引擎」混在一起；新介面的目的正是把對象說清楚。  
  **建議：** 改成「本機開發引擎時使用 `dev --engine -i <image>`」。  
  **出處：** `CONTEXT.md`「VK」「引擎」「本機開發來源」；issue #65 的對象／來源拆分。

- **位置：** [0010-dev-self-and-acceptance.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0010-dev-self-and-acceptance.md:3)  
  **問題：** `Serves` 單句塞入多種機制、兩條不變量及退版理由，過長且難以辨認主旨。  
  **建議：** 仍維持規定的一行，但只摘要「如何服務不變量 9、10」；fixture、矩陣、覆寫與舊引擎限制留給 Decision。  
  **出處：** `doc/adr/README.md` 第 19 行要求 `Serves` 說明服務對象與方式，未要求在此重列全部機制。

- **位置：** [03_interface.md:47](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:47)  
  **問題：** 同一段依序解釋七個名詞，再接指令數量與相容性承諾，第一次閱讀很難把說明對回上方清單。  
  **建議：** 將名詞說明與「常用三個／進階八個／同一個 X」拆成兩段；完整定義繼續交給名詞表。  
  **出處：** `CONTEXT.md` 已分別定義這些詞；02 第 8、10 條分屬介面數量與相容性。

- **位置：** [02_invariants.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:3)  
  **問題：** 一段同時說明不變量與 ADR 的分工、機制可替換性，以及第 5、7、11 條的格式例外。  
  **建議：** 把三條格式例外另起一段，讓文件層級規則與排版例外分開。  
  **出處：** 易讀性；`AGENTS.md` 的固定分工是「ADR 記機制與理由；不變量頁只記必須成立的性質」。

四份文件未命中 `CONTEXT.md` 明列的 `_Avoid_` 詞；指令清單對齊未跑掉；除上述問題外，條號與 ADR 章節引用相符。ADR-0010 的修訂標題、`Amendment status`、六個必要段落及順序符合 `doc/adr/README.md`；四檔沒有殘留 `undev vendor_kit`。