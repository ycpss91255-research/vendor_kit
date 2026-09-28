## 必改

- [01_purpose.md:1](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:1)：標題仍用 CONTEXT.md 對 repo 的 `_Avoid_`「專案」，建議改成「vendor_kit 目的與承諾」。
- [01_purpose.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:3)：名詞已移到根 `CONTEXT.md`，不應再寫「詳細定義見第 02 頁」，建議直接連到 `../../../CONTEXT.md`，並移除已不存在的底線標記規則。
- [02_invariants.md:1](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:1)：檔案已改名為 02，但頁首仍是「03 不變量」，建議改成「02 不變量」。
- [02_invariants.md:93](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:93)：出處仍使用 `_Avoid_` 詞「專案檔」，建議改成「repo 檔」。
- [02_invariants.md:231](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:231)：第 5 條缺少六段結構中的「實際情形」，建議把版本下限與白名單等現況移入明列的 `**實際情形：**` 段。
- [02_invariants.md:293](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:293)：第 7 條缺少「實際情形」，建議將目前實作中的工具 image／引擎發版現況獨立成該段。
- [02_invariants.md:456](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:456)：第 11 條缺少「實際情形」，建議把現行支援平台與矩陣現況移入該段，再把可替換的驗證方法留在「機制」。
- [02_invariants.md:235](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:235)：第 5 條「一句話」沒有涵蓋真正性質中的固定依賴集合，建議直接說明主機額外依賴永遠只限 Docker、Git、just。
- [02_invariants.md:320](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:320)：第 8 條一句話只涵蓋 recipe 數量與相容性，漏掉成對可逆、查詢與套用分離、命名空間衝突及 append 規則，建議補出這些核心性質或拆條。
- [02_invariants.md:374](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:374)：第 9 條一句話漏掉「本機開發與正式啟動走同一入口」，建議把標題後半的性質寫進一句話。
- [02_invariants.md:239](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:239)：第 5 條性質段含「見第 11 條」節次，建議性質只陳述依賴邊界，交叉引用移到機制或出處。
- [02_invariants.md:297](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:297)：第 7 條性質段含「01 頁」及「第 10 條」節次，建議直接寫完整性質，引用移到出處。
- [02_invariants.md:326](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:326)：第 8 條性質段直接固定 `bootstrap.sh` 檔名，不符合性質段不得含檔名的要求，建議改稱 CONTEXT.md 已定義的「啟動器」，檔名移到實際情形。
- [01_purpose.md:23](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:23)：01 承諾 CI 檢查腳本會回報版本、快取、初始檔一致性，但 02 只把它列為公開入口，建議新增或併入一條明確性質，列出它必須覆蓋的三類一致性。
- [02_invariants.md:396](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:396)：仍寫「照 01–03 的名詞」，但名詞來源已是根 `CONTEXT.md` 且審閱頁只剩 01、02，建議改成「照 CONTEXT.md 的名詞」。
- [02_invariants.md:368](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:368)：出處寫「02 頁 VK recipe 表」，目前 02 就是本頁且沒有該表，建議改成有效的新來源或刪除失效引用。

## 建議

- [02_invariants.md:179](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:179)：第 4 條一句話只表達「不靜默」，但性質還包含結束碼、進度可辨識、執行紀錄及寫入順序，建議擴寫一句話或拆成較聚焦的不變量。
- [02_invariants.md:257](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:257)：第 6 條一句話涵蓋鎖定與薄啟動器，但漏掉薄殼遭修改必須被發現、鎖定引擎拉不到不得 fallback，建議補入這兩項永久義務。
- [02_invariants.md:99](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:99)：第 2 條一句話未提安裝目錄不得巢狀及本機覆寫例外，建議至少補出例外邊界，避免一句話比性質更強。
- [01_purpose.md:22](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:22)：本機開發承諾分散在第 2、8、9 條，且第 9 條只明講 VK 自身開發，建議在 02 明確指出一般工具與 VK 自身各由哪條性質承接。
- [01_purpose.md:53](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:53)：「每一版不可變」目前只能由第 2 條的 digest、資產永不刪與決定性重建間接推出，建議在第 2 或第 7 條直接寫成性質。
- [01_purpose.md:54](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:54)：同一 repo 可同時導入與出貨在 02 沒有直接性質；若這是對外承諾，建議補入第 7 條，若只是情境說明則保留現狀即可。
- [02_invariants.md:140](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:140)：第 3 條的「自動化不得寫進 git 的檔、不得碰 git」是 01 未明說的新增承諾，建議回到 01 補成對外承諾或確認它只屬內部設計約束。
- [02_invariants.md:255](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:255)：第 6 條的薄殼邊界、竄改偵測及禁止 fallback 是 01 未承諾的性質，建議決定是否要在 01 公開承諾。
- [02_invariants.md:318](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:318)：第 8 條固定完整 recipe 集合與細部語意，超出 01 的一般相容性承諾，建議在 01 說明「recipe 名稱與語意屬契約」。
- [02_invariants.md:372](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:372)：第 9 條的黑箱可驗及開發／正式共用入口在 01 沒有承諾，建議標明它是驗證原則，或把它提升為 01 的對外承諾。
- [02_invariants.md:456](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:456)：第 11 條的跨平台同輸入同結果強於 01 僅列出的平台範圍，建議在 01 補上跨支援平台的一致性承諾。
- [02_invariants.md:93](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:93)：多處出處使用「01 頁拍板」而不是可追溯 issue，建議依既定決議流程改成具體 GitHub issue 來源。
- [02_invariants.md:291](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:291)：多條 ADR 行引用「在 proto」及 `ADR-xxxx`，來源邊界不明且可能指向舊資料，建議改成現行 `doc/adr/` 的有效 ADR 或清楚標記尚無 ADR，避免間接依賴 `_legacy`。
- [02_invariants.md:362](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:362)：`<name>` 雖不是用來表示 repo 名，仍會與 CONTEXT.md 對 `<repo>` 的 `_Avoid_` 混淆，建議換成 `<recipe>`。

## 沒問題

- [01_purpose.md:62](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:62)：不刪、不覆蓋 repo 檔已由第 1 條直接承接，無須調整。
- [01_purpose.md:63](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:63)：相同版本鎖定行得到相同內容已由第 2、7、11 條共同承接，無須調整。
- [01_purpose.md:64](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:64)：升版可修改範圍已由第 1、3、8 條承接，無須調整。
- [01_purpose.md:65](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:65)：退版與 git 還原已由第 2、10 條承接，無須調整。
- [01_purpose.md:66](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:66)：失敗必須顯示原因與下一步已由第 4 條直接承接，無須調整。
- [01_purpose.md:67](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:67)：主機只需 Git、Docker、just 已由第 5 條直接承接，無須調整。
- [01_purpose.md:71](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:71)：符合出貨格式即可搬運已由第 7 條端到端性質承接，無須調整。
- [01_purpose.md:72](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:72)：只搬檔、不執行、不驗證已由第 7 條直接承接，無須調整。
- [01_purpose.md:73](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:73)：出貨與導入內容逐檔相同已由第 7、11 條承接，無須調整。
- [01_purpose.md:77](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:77)：`X.Y.Z`、同一 X 相容、破壞性變更先公告及引擎內部不屬契約，均由第 10 條完整承接。
- [02_invariants.md:7](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:7)：目錄 11 個連結文字、錨點與各條標題逐一相符，未發現錯鏈。
- [02_invariants.md:19](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:19)：第 1、2、3、4、6、8、9、10 條都有六種段落標記，只有上列第 5、7、11 條缺「實際情形」。
- [02_invariants.md:23](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:23)：除第 5、7、8 條已列問題外，其餘性質段未發現檔名、訊息碼、節次引用或以 VK 為主詞的違規。