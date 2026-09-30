# r129 審查：doc/adr/0007-host-thin-layer-and-shell-integrity.md

範圍：這一輪只改了第 32 行（對照 `doc/decisions/_backup/doc_adr_0007-host-thin-layer-and-shell-integrity.pre_r129.md`）。

## 必改

無。

- 已定案：不帶指令時先印 `vendor_kit <版本>`，接著印用法，輸出到 stderr，結束碼 2，符合 #99 結論；多出的 `error[VK0024]` 診斷行符合 #115（非 0 結束碼要有同 level 的診斷）。沒有違反 #78「Decisions so far」任何一條。
- 對外承諾：順序與文字跟 03:35、03:83、03:104、04:127、GLOSSARY:251 一致，沒有改到 ask 以外的介面。
- 做完沒：ask 第 2 項指定的 ADR-0007:32 已照順序改好。第 3 項只要求 03:82 跟 ADR-0007:30 一致，ADR-0007:30 已經寫結束碼 `2`，03:82 現在是 error／需人處理／附下一步指令，所以 ADR 這邊不用改。
- 連結：`../contract/03_messages.md#結束碼` 用腳本算 slug，03 的標題 slug 有 `結束碼`，連得到；#106 的連結沒動。

## 建議

- 位置：ADR-0007:32。問題：ADR 把診斷全文 `vendor_kit: error[VK0024]: 未指定指令。` 抄了一份，03 的代碼表（03:83）已經有這段文字。之後 03 改本文時 ADR 會默默脫鉤，而 ADR 的分工是記決定，不是記訊息原文。建議：改成「第二行印 [`VK0024`](../contract/03_messages.md#訊息) 診斷」，不抄本文，或保留原文但加上連結，讓 xcheck 能對得上。證據：ADR-0007:32；03_messages.md:83。
- 位置：ADR-0007:32。問題：ADR 寫「接著印用法」，03:35／03:104 寫「簡短用法」，同一件事兩種寫法（04:127 與 GLOSSARY:251 也寫「用法」）。建議：統一用詞，照 03 在這四處都寫「簡短用法」，或把 03 改成「用法」。證據：03_messages.md:35、03_messages.md:104、ADR-0007:32。
