# ADR-NNNN：<標題——一句話說決定了什麼，不是主題名>

> Serves: 不變量 N（<不變量名稱>）——<一句話：這份 ADR 建立了它／是實現它的機制／是它在某個範圍的應用>。也服務不變量 M／設計原則 Pn（若有）。純機制決議寫「機制（服務不變量 N），不建立不變量」。
<!-- 不變量編號見 `docs/contract/02_invariants.md`；設計原則 P1–P6 見 `doc/decisions/design_principles.md`。 -->

- **Status:** Proposed <!-- Proposed | Accepted | Rejected | Superseded by ADR-NNNN -->
- **Date:** YYYY-MM-DD
- **Related:** issue #N（決議討論）、ADR-NNNN（被修訂／被取代／依賴）、`<圖檔>.drawio` 第 N 頁、`doc/decisions/review_log/<題目>.md`（雙軌分析）

## Context

<!--
為什麼現在要決定。寫當時的事實，不寫意見：
- 觸發的 issue 或量測（附數字與重現方式）。
- 既有決議、不變量或設計原則條文與這個問題的關係。
- 硬性限制（主機只有 docker + git + just；使用者的檔歸使用者；……）。
- 已查證的前例，只引一手來源；agy／記憶未查證的不引。
-->

## Decision

<!--
決定了什麼。性質與機制分開寫：
- 性質若已是不變量，只寫「見 `docs/contract/02_invariants.md` 第 N 條」並連結，不重述。
- 本檔記機制：具體規則、順序、邊界、結束狀態、逃生口（每個逃生口要有名字，見 P3）。
- 用編號小節（### 1. …）讓後續 ADR 能精確引用「ADR-NNNN §2」。
- 一條規則一個擁有者（P5）：寫明這條規則在哪個模組實作、誰只轉發。
-->

## Consequences

<!--
- 得到什麼、付出什麼（含使用者（導入那一端）要多做的事、使用者（出貨那一端）要多交的東西）。
- 哪些先前決議被修訂或取代：在那份 ADR 加修訂段（見下方「修訂」），這裡列出。
- 需要同步更新的東西：`docs/contract/02_invariants.md`（若建立新不變量）、`doc/decisions/design_principles.md`（若建立新原則）、根 `GLOSSARY.md` 名詞、架構圖頁碼、lint。
- 驗收案例：這份決議成立時，哪個測試層會抓到違反（見 ADR-0011）。
-->

## Alternatives

<!--
考慮過但沒採的選項，每個一段：選項是什麼、它會滿足什麼、為什麼不採（引用 `doc/decisions/design_principles.md` 的衝突優先序時，點名相衝的兩個性質）。
被 decision-review 雙軌分析否決的方案要列，讓下次不用重論。
-->

<!--
修訂（不新增第二個 Status 行；lint 只認第 0 欄恰好一次）：

### 修訂（YYYY-MM-DD，ADR-NNNN／issue #N）

- **Amendment status:** Accepted
- 改了哪一節、改成什麼、為什麼。原文保留，不改寫歷史。
-->
