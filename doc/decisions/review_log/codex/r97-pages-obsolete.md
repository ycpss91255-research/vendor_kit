# 必改

## 整頁作廢

- `discussion.drawio`｜「01 名詞與縮寫」：整頁作廢；名詞唯一真本已是 `CONTEXT.md`，本頁仍使用「接入根／動詞／可寫動詞」等舊語言，不能保留第二份字典。
- `discussion.drawio`｜「02 不變量與角色（1）」：整頁作廢；核心是「下游開發者／下游使用者／VK」三方模型，直接違反 [`01_purpose.md:35`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:35) 的使用者 ↔ VK 兩方承諾。
- `discussion.drawio`｜「03 不變量與角色（2）」：整頁作廢；18 條舊不變量及例外結構已被 11 條正式不變量取代，不能逐條併回 [`02_invariants.md:5`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:5)。
- `discussion.drawio`｜「04 契約 v2：動詞介面表」：整頁作廢；分類軸就是已取消的「動詞」，目前契約是 11 個 VK recipe 與 `bootstrap.sh`，見 [`02_invariants.md:227`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:227)。
- `discussion.drawio`｜「05 契約 v2：規則、選項表、不開的動詞」：整頁作廢；雖然「不加 ensure 等別名」仍成立，但本頁以動詞、接入、專案根等舊模型組織，正確結論應併入新的 recipe 概覽，不保留原頁。
- `discussion.drawio`｜「08 契約 v2：動詞 × 檔案矩陣」：整頁作廢；矩陣的列、欄及寫入責任都建立在舊動詞模型，改標題不足以修正。
- `discussion.drawio`｜「69 對外契約（PRD，待拍板）」：整頁作廢；PRD 已移除，而且頁面仍含 `.version`、`ensure`、三方合併等舊決議。
- `discussion.drawio`｜「70 使用方式（乙版）」：整頁作廢；乙版介面及 `.version` 已失效，不能當現行使用流程。
- `discussion.drawio`｜「71 架構圖（乙版重畫，待定型）」：整頁作廢；它是未定型乙版，包含 `.version`、`ensure`、舊三方結構，不能與正式架構合併。
- `discussion.drawio`｜「72 討論 #11 圖解」：整頁作廢；issue 討論不是現行真本，其中「範本／三方」模型已由基準版合併正式定義取代。
- `discussion.drawio`｜「74 討論 #6：本地開發模式」：整頁作廢；舊 issue 路徑使用 `.version` 與舊介面，現行機制由 ADR-0010 的 `dev vendor_kit -i` 決議取代。
- `discussion.drawio`｜「75 討論 #11：diff 三方比對」：整頁作廢；「三方比對」不是現行用語，應只在新的 `upgrade`／基準版合併流程中畫一次。
- `discussion.drawio`｜「76 討論 #13：並行安裝 lock」：整頁作廢；舊 issue 圖不是現行決議來源，鎖若要出現，應畫在可寫 recipe 的共同時序／寫入邊界內。
- `discussion.drawio`｜「77 討論 #12：verify 比什麼」：整頁作廢；沒有 `verify` recipe，現行介面明列的 11 個 recipe 中不存在它。

## 結構必須重畫

- `discussion.drawio`｜「06 目錄樹與檔案範例」：重畫；它把 `init.toml` 當 `cache/<repo>/` 內容並混入大量舊責任說明，應改成「安裝目錄唯一版本鎖定行＋`.vendor_kit/` 所有權邊界」，依 ADR-0002 §1–4。
- `discussion.drawio`｜「09 下游 repo 契約③」：重畫；整頁用「下游」劃界，應改成同一使用者的導入／出貨兩個情境。
- `discussion.drawio`｜「10–11 啟動器 ↔ 引擎契約」：重畫；現圖讓啟動器承擔 registry 查詢、快路徑、版本語意等大量規則，與「啟動器不解讀 repo 內容」的界線不乾淨，見 [`02_invariants.md:188`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:188)。
- `discussion.drawio`｜「12–13 CI 契約與驗收矩陣」：重畫；現圖有 35 項驗收及 `verify` 步驟，但正式契約是 ADR-0010 的 13 項出貨閘門與固定 recipe 流程。
- `discussion.drawio`｜「14 架構圖 v2」：重畫；這是主要架構的核心，但目前仍以「下游／動詞／專案根」、8 個自訂模組及未定細節組圖；應直接按 ADR-0002、0005、0006、0007 的責任邊界重建。
- `discussion.drawio`｜「19–54 各 recipe 詳細流程」：重畫並合併；36 頁逐 recipe、逐 apply 階段的展開方式不符合「重點流程」，共同的啟動、執行紀錄、進度檔、預檢、寫入與鎖定行收尾應只畫一次。
- `discussion.drawio`｜「56 初始檔五態」：重畫；基準版合併值得保留，但舊「範本／三方」標籤及狀態分類不能只換字。
- `discussion.drawio`｜「57 交易與進度檔」：重畫；本頁以每個「動詞」展開 33 次，應收斂成所有可寫 recipe 共用的五步時序。
- `discussion.drawio`｜「58 相容性矩陣」：重畫；現圖以介面版矩陣為主，缺少正式的同一個 X 內相容、跨 X 才可能破壞及先公告的上層承諾，見 [`02_invariants.md:291`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:291)。
- `discussion.drawio`｜「59 結束碼決策表」：重畫；多工具優先序寫成「失敗 1 > 衝突 2 > 有新版 2 > 0」，但真本只定 `1 > 2 > 0`，且 `3` 是版本組合前置拒絕，不參與多工具彙總，見 [`02_invariants.md:139`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:139)。
- `discussion.drawio`｜「60–61 release」：重畫並合成一頁；現圖仍以 35 條驗收為閘門，正式 ADR-0010 是 13 項，release 資產則應依 ADR-0009。
- `discussion.drawio`｜「62–68 離線包」：重畫並合成一頁；七頁過細，主要契約只有「每平台 image tar＋同名 `.digest`＋`SHA256SUMS`、旁檔缺則 1」，見 ADR-0009 §1–2。
- `discussion.drawio`｜「73 just 與 vendor_kit 怎麼接」：不要整頁作廢，但必須重畫；「根 justfile → 薄殼 → 引擎 → 工具 recipe」是主要架構所需，舊頁的 `ensure`／`verify`／`.version` 全部移除。

## 缺漏或畫錯的必要內容

- [`01_purpose.md:35`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:35)｜兩方承諾關係：目前只有第 01 頁近似畫到；第 02 頁反而畫成三方。第 01 頁作廢後即完全缺漏，主要架構首頁必須補「使用者 ↔ VK」。
- [`01_purpose.md:42`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:42)｜導入／出貨兩情境：第 01 頁畫成「repo 的接入／出貨角色」，不是「同一使用者的兩個情境」；屬部分畫到但結構錯誤。
- [`02_invariants.md:227`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:227)｜常用三個／進階八個：第 04、05 頁有舊介面表，第 14 頁只寫 `[group('常用')]`／`[group('進階')]`，沒有正確列出 `add、upgrade、dev` 與其餘八個；等同未完整畫到。
- [`02_invariants.md:139`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:139)｜結束碼 0/1/2/3：第 59 頁有畫，但多工具優先序混入兩種 `2` 的細分，且沒有把 `3` 清楚隔離為版本組合前置判定；需要替換。
- [`02_invariants.md:148`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:148)｜多工具優先序：第 03、13、55、59 頁散落畫到；正確規則應集中成一處 `1 > 2 > 0`，並註明 `update` 同時查詢失敗與有新版時回 `1`。
- [`02_invariants.md:85`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:85)｜每個安裝目錄唯一版本鎖定行：第 06、07、14 頁有局部畫到，但都被「專案根」舊詞掩蓋；需要在主要架構明示唯一性的單位是安裝目錄，不是 repo。
- [`02_invariants.md:97`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:97)｜禁止巢狀安裝目錄：第 03 頁舊 I10、部分 install 流程有畫；廢掉第 03 頁並合併流程後必須補進安裝目錄圖，否則會消失。
- [`02_invariants.md:152`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:152)｜可寫 recipe 五步時序：第 10、19–54、57 頁分散且順序不一致；沒有一頁精確畫成「執行紀錄 → 進度檔 → 全部預檢 → 寫入 → 最後改版本鎖定行」，應新增共同時序圖。

# 建議

## 只需換詞，流程拓撲可保留

- `discussion.drawio`｜「07 schema」：核心的 `version.toml` 正規形、`schema`／`written_by`、未知欄位保留與檔案版拒絕規則對齊 ADR-0002、0008；可保留圖形，只改「下游使用者／動詞／專案根」等詞，並刪除不屬主要架構的逐欄細節。
- `discussion.drawio`｜「15–18 bootstrap.sh」：首次導入、選引擎、啟動 `install`、再處理工具的主幹仍可用；把「接入／下游／專案」改成「導入／使用者／repo 或安裝目錄」，四頁合成一頁。
- `discussion.drawio`｜「55 update」：唯讀、逐工具查詢、查詢失敗優先於有新版、`--exit-code` 有新版回 2 的決策拓撲符合 [`02_invariants.md:139`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:139)；只需改舊詞並刪除過度細的 registry 協定分支。

判斷界線：

- 只換詞：節點與箭頭在替換「動詞→recipe」「接入→導入」「專案根→安裝目錄」「專案檔→repo 檔」後，決策順序仍符合真本。
- 必須重畫：角色數量、責任擁有者、狀態集合、結束碼優先序或寫入順序本身不同；例如第 02 頁的三方角色、第 59 頁的碼值結構、第 57 頁按每個動詞重複交易流程。

## 建議收斂後的頁型

- `discussion.drawio`｜全檔：把 77 頁收斂為「承諾與情境、recipe 介面、主要架構、首次導入、日常導入／同步／升級、基準版合併、共同寫入時序、相容與結束碼、出貨與 release／離線」約 8–10 頁。
- `discussion.drawio`｜「19–54」：不要再為每個 recipe 畫 resolve/apply/docker/log 的重複段落；共同骨架畫一次，各 recipe 只標差異。
- `discussion.drawio`｜「60–68」：release 與離線導入各留一頁；平台 runner、候選 tag、每個 tar 檔名等細節留在 ADR，不塞回主要架構圖。

# 沒問題

- [`CONTEXT.md:108`](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:108)｜兩方角色、導入／出貨、安裝目錄、VK recipe 等正式詞已完整定義；新圖直接引用，不另建名詞頁。
- [`01_purpose.md:60`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:60)｜導入承諾與出貨承諾已分開且沒有第三方；可直接作新承諾圖的左右兩個情境。
- [`02_invariants.md:152`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:152)｜五步寫入時序已足夠精確，不需重新設計，只需忠實畫出。
- [`ADR-0004 §1「轉發形狀與分組」`](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:17)｜`vendor.just` 的一行轉發與常用／進階分組機制已定，可直接成為 recipe 介面圖的依據。
- [`ADR-0006 §2–3`](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0006-tool-image-as-data-only.md:25)｜`docker create → docker cp → 唯讀掛入引擎` 及三層內容驗證是可保留的主要取件架構。
- [`ADR-0009 §1–3`](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0009-release-assets-and-offline-import.md:17)｜release 資產、離線 digest 與永不刪的規則完整；問題只在現圖拆成七頁過度展開。