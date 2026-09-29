## 必改

- [`script/diagram/gen_disc.py:1`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/gen_disc.py:1)「每題一頁」：不可沿用成重畫原則，應先核准整組目標頁清單，再依資訊架構合併舊頁。
- [`script/diagram/gen_disc.py:577`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/gen_disc.py:577)「提案 v1」：新圖不得由目前依賴 `_legacy/` 規格的舊產生器重生，否則舊模型會再次覆蓋新圖。
- [`script/diagram/README.md:3`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/README.md:3)「77 頁提案圖＋討論」：應把 `discussion.drawio` 明確降為史料，不再稱為現行討論圖或重畫輸入。
- [`CONTEXT.md`「角色與情境」](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:104)：所有頁只能呈現「使用者 ↔ VK」兩方，以及導入、出貨兩個情境，不得保留三方角色或由舊頁推導第三方。
- [`CONTEXT.md`「VK recipe 與用途」](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:357)：頁面清單與流程覆蓋表必須只認 11 個 VK recipe 加 `bootstrap.sh`，不得出現 `ensure`、`verify`、`init` 或以「動詞／子命令」統稱。
- [`doc/decisions/review/02_invariants.md`「8. 使用者介面極少；recipe 語意固定」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:227)：重畫前先批准一份頁面 manifest，至少列「頁名、回答的問題、真本來源、包含與刻意省略內容、前後頁關係」。
- [`script/diagram/review_v2_README.md`「流程」](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/review_v2_README.md:38)：審查粒度改成兩層閘門——先一次核准全圖 manifest 與流程分組，再維持「一次一頁、該頁未 OK 不畫下一頁正式內容」。
- [`script/diagram/review_v2_README.md`「xref-forward」](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/review_v2_README.md:85)：跨兩頁以上的流程應先審整組 storyboard／分頁邊界，之後才逐頁審內容，避免單頁 OK 後才發現切頁錯誤而全部返工。
- [`doc/decisions/review/02_invariants.md`「9. 對外承諾必須黑箱可驗」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:271)：每個流程頁須畫出公開入口、可觀察結果、寫入範圍、結束碼及失敗／續作出口，不能以引擎內部實作代替契約。
- [`doc/decisions/review/02_invariants.md`「6. 引擎版本由安裝目錄鎖定」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:188)：主要架構頁必須清楚分出使用者、薄殼／啟動器、引擎、工具 image、registry 與 repo／安裝目錄的邊界，並保持「啟動器不解讀 repo 意義」。
- [`doc/decisions/review/02_invariants.md`「1–4」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:19)：資料與流程頁必須標出 repo 檔和 VK 檔的所有權、何時詢問、進度檔時序、版本鎖定行最後寫及失敗可辨識等不可省略的寫入邊界。
- [`doc/decisions/_legacy/README.md`「引用這裡的事實之前」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_legacy/README.md:11)：舊圖只能作版面與問題清單參考，任何保留下來的事實都必須逐項回查四組真本，不能以舊圖自證。

## 建議

- [`doc/decisions/README.md`「兩個 .drawio 主檔」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:52)：建議採選項 **(c)**，把舊 `discussion.drawio` 與專屬舊產生器一併歸檔至 `_legacy/`，另建名稱明確的現行圖檔。
- [`doc/decisions/README.md`「已歸檔」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:34)：選項 (c) 的主要收益是保留查考能力又讓路徑表明「非真本」，代價是要同步修正 README、腳本引用、名詞檢查排除與可能的外部書籤。
- [`script/diagram/README.md:3`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/README.md:3)：選項 (a) 另開新檔但讓舊檔留在 repo 根的改動成本最低，代價是兩份圖看起來同樣有效、搜尋與自動化容易繼續誤用舊圖。
- [`script/diagram/gen_disc.py:589`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/gen_disc.py:589)：選項 (b) 原地改可保留既有路徑，代價是舊產生器可能覆寫、77 頁大 diff 難審、史料與現況混在同一檔且難以判斷哪些頁已重畫。
- [`doc/decisions/_legacy/README.md:3`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_legacy/README.md:3)：若採 (c)，歸檔位置應附一句「舊模型、不得作現況引用」，並讓 git 歷史承擔逐版保存，不再維護舊圖內容。
- [`doc/decisions/review/01_purpose.md`「VK 做的事」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:16)：建議把 77 頁收斂為約 8–10 頁，而不是預先指定固定數字，頁面是否存在以「是否回答一個主要架構或端到端流程問題」判定。
- [`doc/decisions/review/01_purpose.md`「承諾關係」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:35)：第一批建議只審「圖集導覽／兩個情境」與「主要架構／邊界」兩頁，先固定全圖閱讀方向和角色。
- [`doc/adr/0002-vendor-kit-dir-layout-and-lock-line-form.md`「Decision」](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0002-vendor-kit-dir-layout-and-lock-line-form.md:19)：第二批建議審「安裝目錄、版本鎖定行、cache／gen／metadata／進度檔與所有權」一頁，作為所有流程共同引用的資料架構。
- [`doc/adr/0007-host-thin-layer-and-shell-integrity.md`「Decision」](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:19)：第三批建議審「bootstrap／啟動器／引擎／工具 image 的啟動與取件路徑」一至兩頁。
- [`CONTEXT.md`「VK recipe 與用途」](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:357)：後續流程可分成「install／uninstall」、「add／remove／sync／prune」、「update／upgrade／基準版合併與回退」、「dev／undev」、「出貨／release／離線導入」五組，每組先審 storyboard、再逐頁 OK。
- [`doc/adr/0010-dev-self-and-acceptance.md`「驗收 recipe 矩陣與流程順序」](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0010-dev-self-and-acceptance.md:29)：最後一批建議審「CI／黑箱驗收／相容性與跨平台」一頁，並用它反查前面每頁是否具備可驗證出口。
- [`doc/adr/README.md`「決議流程」](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/README.md:30)：應先開 `needs-decision` issue「決定現行架構圖的頁面清單與審查粒度」，要問頁面數不是什麼，而是每頁回答什麼、哪些舊頁合併或不再畫、哪些流程允許跨頁，以及是否採 manifest→storyboard→逐頁 OK。
- [`doc/adr/README.md`「決議流程」](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/README.md:30)：應先開 `needs-decision` issue「決定舊 discussion.drawio 與舊產生器的歸檔方式」，要問採 (a)／(b)／(c)、現行圖檔名稱、舊產生器是否隨檔歸檔，以及哪些文件與檢查需同步改指向。
- [`AGENTS.md`「架構圖不是插圖」](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md)：應先開 `needs-decision` issue「決定架構圖與契約的追溯及驗收門檻」，要問每頁如何列真本來源、11 條不變量與 12 份 ADR 如何覆蓋、允許省略哪些細節，以及圖面 lint 何時成為合併閘門。
- [`doc/agents/issue-tracker.md`](/home/cyc/Desktop/vendor-kit_ws/src/doc/agents/issue-tracker.md)：三個決議完成後再開一個執行型 tracking issue，以核准頁面為 checklist 並記錄每頁 OK，不應用 77 個舊頁各開一票。
- [`doc/adr/README.md`「決議流程」](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/README.md:30)：上述三項先在 issue 定案即可，只有產生新的產品機制或改動既有 ADR 時才新增／修訂 ADR，單純圖檔路徑與審查流程不必冒充產品 ADR。
- [`doc/decisions/review/02_invariants.md`「目錄」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:5)：完成驗收應附一張「真本條目 → 圖頁／刻意不畫」覆蓋表，確保 11 條不變量、對外承諾及相關 ADR 沒有無聲遺漏。
- [`CONTEXT.md`「Language」](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:104)：語意驗收應確認所有專有名詞採 `CONTEXT.md` 正規名稱，禁用詞為零，且同一實體跨頁名稱、顏色、形狀與方向一致。
- [`doc/decisions/review/01_purpose.md`「VK 不做的事」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:27)：範圍驗收應確認圖沒有暗示 VK 執行或驗證工具內容、處理工具功能、維護工具相容矩陣或支援已排除的平台。
- [`doc/adr/0004-vk-recipe-interface-and-write-boundary.md`「Decision」](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:15)：流程驗收應逐頁檢查前置條件、讀寫對象、詢問點、CI 差異、成功／失敗／需人處理／版本不合出口及重跑行為。
- [`doc/adr/0008-protocol-and-file-schema-versions.md`「Decision」](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:17)：相容性驗收應確認介面版與檔案版未混為一物，版本不合為零寫入，救援路徑及退回舊版仍可辨識。
- [`doc/adr/0011-test-layers-and-ci-matrix.md`「Decision」](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0011-test-layers-and-ci-matrix.md:15)：最終驗收除圖面 lint 外，還應由獨立讀者只看圖回答「誰承諾誰、資料真本在哪、每個主要流程改什麼、失敗後怎麼辦」，答不出來即表示圖仍缺主要架構或流程。

## 沒問題

- [`script/diagram/review_v2_README.md:3`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/review_v2_README.md:3)：把機械檢查與人工判斷分開的原則仍適用，可直接保留。
- [`script/diagram/review_v2_README.md:21`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/review_v2_README.md:21)：只抽取指定頁審查的能力正好支援新流程中的逐頁 OK，無須恢復整份 77 頁一起審。
- [`script/diagram/review_v2_README.md`「已知限制」](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/review_v2_README.md:106)：lint 結果仍由人判讀而非自動當設計結論的做法正確，可延續到新圖。
- [`doc/decisions/_legacy/README.md:1`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_legacy/README.md:1)：`_legacy/` 已有清楚的「只作參考、不是正式內容」語意，因此是舊圖比 repo 根更合適的保存位置。
- [`doc/decisions/review/02_invariants.md`「9. 對外承諾必須黑箱可驗」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:271)：以重點流程和主要架構取代完整內部狀態展開，符合「只呈現公開入口與可觀察結果」的契約方向。