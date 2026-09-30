## 結論

版本組合不合時，所有已知 recipe 的 `-h`／`--help` 仍應把用法印到 stdout 並回 `0`；頂層 `just vendor_kit -h`／`--help` 也應列為永久可用的救援路徑。用法由薄殼依自己的介面版印出；裸呼叫 `just vendor_kit` 則維持 stderr、`2`。

## 理由

- `-h`／`--help` 已被定義為同一個跨指令概念：每個指令都支援、輸出 stdout、回 `0`。[04_interface.md:129](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:129)；第 8 條又要求「一個概念一種寫法」，不應讓同一選項因版本組合而從「成功顯示說明」變成版本錯誤。[02_invariants.md:150](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:150)  
  **推論：** 應修正 6-36 的例外，而不是削弱 04 的通則。

- [GitHub issue #71](https://github.com/ycpss91255-research/vendor_kit/issues/71) 已定 `-h`／`--help` 是共同的 GNU 式選項、說明只走這個入口，沒有定義「部分 recipe 的 help 在版本不合時改成別種行為」。討論佇列第 10 條又把「一個概念一種寫法」保留為已定案概念，並將 help 的具體行為交給 04。[discussion_queue.md:22](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review_log/discussion_queue.md:22)

- Python `argparse` 的慣例清楚區分 help 與用法錯誤：`-h`／`--help` 顯示說明後正常退出；無效參數則印到 stderr、回 `2`。[Python argparse：help](https://docs.python.org/3/library/argparse.html#add-help)、[Python argparse：error handling](https://docs.python.org/3/library/argparse.html#exit-on-error)。這支持：

  - 明確要求 help → stdout、`0`
  - 裸呼叫、缺參數、不認得選項 → stderr、`2`

  現行 04 對裸呼叫的分類已符合這個界線。[04_interface.md:133](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:133)

- 回 `3` 的意義是「版本組合不合，必須先升級或退回才能繼續」，不是「成功取得說明」。[03_messages.md:18](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/03_messages.md:18) 把明確的 help 請求回成 `3`，會讓結束碼描述與實際完成的工作不一致。

- 要在版本不合時保證 help 可用，不能依賴不相容的引擎介面；應由薄殼印出與其自身介面版相符的用法。ADR 已規定一般 recipe 會在啟動引擎前由薄殼擋下。[0007-host-thin-layer-and-shell-integrity.md:29](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:29)  
  **推論：** help 文字屬薄殼所暴露介面的自我說明，不是解讀 repo 內容的產品規則，因此不違反「薄殼只啟動與轉發」的界線。[02_invariants.md:126](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:126)

- 頂層 `-h`／`--help` 必須同樣回 `0`，否則同一個 help 概念在頂層與 recipe 層有兩種行為。裸呼叫則不是 help 請求，維持用法錯誤 `2`。這也與定案第 18 條「用法錯誤回 2」一致。[discussion_queue.md:35](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review_log/discussion_queue.md:35)

## 風險或反例

- 舊薄殼只能說明自己知道的介面，無法顯示新引擎新增的 recipe。這不是錯誤：版本不合時真正可呼叫的公開介面就是舊薄殼所暴露的那一版；help 應描述它，而不是描述目前無法安全轉發的新介面。**此為推論。**

- 這個結論會擴大目前救援路徑的集合：GLOSSARY 與 ADR-0007 現在只列三個 recipe 的 help，且明訂其他 help 回 `3`。[GLOSSARY.md:238](/home/cyc/Desktop/vendor-kit_ws/src/GLOSSARY.md:238)、[0007-host-thin-layer-and-shell-integrity.md:30](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:30)；03 的 6-36 也須刪掉「含其他 recipe 的 help」。[03_messages.md:50](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/03_messages.md:50)

- 若薄殼不保存完整 help 文字，而一定要由引擎產生，那麼「所有 help 在任何版本組合下成功」在機制上做不到。此時只能保留少數救援 help，但代價是明確違反 04 的「每個指令 help 回 0」以及一個概念一種寫法；因此不建議選這案。