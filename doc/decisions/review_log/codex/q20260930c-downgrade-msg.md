## 結論

6-10 應只適用於引擎降版，不應拆成兩條，也不應改成模糊的共同文字。工具降版時雖然仍由「目前引擎」執行，但不存在將要接手讀取 VK 檔的「目標引擎」；ADR-0008 第 7 節把工具降版也套入這項檢查，本身才是需要修正的機制矛盾。

## 理由

- 工具與引擎是兩個獨立的升降版對象。`upgrade <repo>@<tag>` 更換工具版本，`upgrade --engine@<tag>` 才更換引擎版本；因此只有後者產生「目標引擎」。證據：[CONTEXT.md:364](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:364)。

- 工具 image 是純資料，既不執行，也不攜帶引擎；實際讀取與判斷仍由安裝目錄目前鎖定的那一份引擎完成。證據：[CONTEXT.md:181](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:181)、[ADR-0006:21](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0006-tool-image-as-data-only.md:21)、[ADR-0006:27](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0006-tool-image-as-data-only.md:27)、[ADR-0006:45](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0006-tool-image-as-data-only.md:45)。

- 不變量明定同一個 X 內工具與引擎不綁發版；若工具降版還必須找到一個與該工具版本相配的「目標引擎」，實質上就重新建立了工具—引擎相容矩陣，違反這項邊界。證據：[02_invariants.md:138](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:138)、[ADR-0006:47](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0006-tool-image-as-data-only.md:47)。

- ADR-0008 所謂「無損讀現有檔」檢查的是引擎能否讀取 VK 寫出的 TOML：每個檔以 `schema` 作讀取門檻，未知欄位必須保留。這是新、舊引擎之間的相容性，不是新、舊工具內容之間的相容性。證據：[ADR-0008:46](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:46)、[ADR-0008:53](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:53)、[CONTEXT.md:395](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:395)。

- 6-10 現文同時列兩種降版，卻只描述「目標引擎」的介面版與檔案版，語意只能完整套用 `upgrade --engine@<tag>`。證據：[03_messages.md:44](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_messages.md:44)。

- ADR-0008 第 7 節同樣把兩種命令放在一起，再以「目標引擎」作共同條件；這不是訊息措辭能消除的問題。其 Context 也把 `upgrade <repo>@<舊 tag>` 說成需要「引擎之間」比較，前後缺少能把舊工具版本映射成另一個引擎的機制。證據：[ADR-0008:11](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:11)、[ADR-0008:66](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:66)。

- **推論：**正確切法應是：工具降版仍由目前引擎讀現有 VK 檔、取出舊工具資料並執行既有的基準版合併；只有引擎降版需要在交棒前證明舊引擎能無損讀取現有 VK 檔。因此 6-10 的「時機」應只列 `upgrade --engine@<tag>`，訊息保留「目標引擎」反而最精確。

## 風險或反例

- 工具降版仍可能失敗，例如舊工具 image 的出貨格式不受目前引擎支援、舊初始檔造成合併衝突，或 registry 中取不到舊版。但這些是「目前引擎無法處理目標工具資料」或一般合併／取件問題，不是「目標引擎無法讀現有 VK 檔」；若需要固定訊息，應依各自原因另列，不能拆出一條換皮的 6-10。這是依工具 image 純資料邊界作出的**推論**。

- 跨 X 時可能事先公告要求工具重發版或人工遷移；不變量明確保留這種可能性。但它仍不是把某個工具舊 tag 視為「目標引擎」，不構成共用 6-10 的理由。證據：[02_invariants.md:142](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:142)、[02_invariants.md:186](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:186)。

- 若實作其實讓工具版本決定某套 VK 檔 schema 或引擎版本，才會出現工具降版的「目標引擎」；但那會直接牴觸工具 image 純資料、引擎不因工具分身及兩邊各自發版的既定設計。證據：[ADR-0006:47](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0006-tool-image-as-data-only.md:47)、[ADR-0006:49](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0006-tool-image-as-data-only.md:49)。