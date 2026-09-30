# r137 doc-edit 審查：doc/contract/03_messages.md

範圍：`doc/decisions/_backup/doc_contract_03_messages.pre_r137.md` 不存在（這一輪沒有備份 03）；`git diff HEAD -- doc/contract/03_messages.md` 為空。這一輪 03 沒有改動。

逐項：
1. 已定案（map #78）：diff 為空，沒有可違反的改動。
2. 對外承諾：沒有改動，01／02 承諾與 03 介面不受影響。
3. 做完沒：03 所有連結的連結文字（02 不變量第 N 條、名詞表、結束碼、輸出、訊息、訊息表、NO_COLOR、02 不變量）都不含反引號，也不含 `<…>`；沒有「[通用連結](…)的 `程式碼名詞`」這種要合併的寫法。ask 在 03 沒有該做而沒做的項目。`check_review_pages.py` 掃 5 個對外文件 OK、`check_typography.py` OK。
4. 連結：03 共 12 個站內連結，用腳本算 slug 比對，檔案與 #錨點全部存在（沒有新增或改動的連結）。

## 必改

無。

## 建議

- 位置：doc/contract/03_messages.md 第 85、91 行（「情況與本文見[訊息](03_messages.csv) `VK0002`」「…`VK0005`」），以及第 60 行「[訊息表](03_messages.csv) (`doc/contract/03_messages.csv`)」
  - 問題：形狀和 ask 例子「[名詞表](…)的 `<repo>`」相同（通用連結＋緊接的程式碼名詞），這一輪 04 把 `<repo>` 那條合併了，但 `[訊息](03_messages.csv) \`VKxxxx\`` 在 03、04（第 33、48、110、112、117、127、130–132、148 行）都保留。維護者說「沒有例外」，讀者可能把這當成漏改。
  - 建議：不動，維持 03、04 一致；若要照 B 案合併，03 與 04 一起改成 `[VK0002](03_messages.csv)` 形式，不要只改一頁。由主對話決定是否列入下一輪。
  - 證據：doc/contract/03_messages.md:60、85、91；doc/contract/04_interface.md:33、48、110；04 本輪 diff 只改了 `<repo>` 一處。
