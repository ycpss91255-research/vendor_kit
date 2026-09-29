## 必改

- 位置：[scope_roadmap.md:18](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/scope_roadmap.md:18)  
  問題：「結束狀態 0/1/2」漏掉契約中的結束碼 `3`。  
  建議：改成「結束狀態 0/1/2/3」。  
  出處：[02 第 4 條](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:139)、[03「結束碼」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:84)。

- 位置：[scope_roadmap.md:18](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/scope_roadmap.md:18)  
  問題：仍把 `--porcelain` 列為第一版介面，但 ADR-0005 已決定不提供它。  
  建議：刪除 `--porcelain`。  
  出處：[ADR-0005 Decision §1](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0005-run-log-and-event-registry.md:19)、[Consequences](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0005-run-log-and-event-registry.md:47)。

- 位置：[scope_roadmap.md:21](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/scope_roadmap.md:21)  
  問題：`dev -p <dir>` 漏掉必要的工具對象 `<repo>`，與其餘文件的新寫法不一致。  
  建議：改成 `dev <repo> -p <dir>`。  
  出處：[issue #65](https://github.com/ycpss91255-research/vendor_kit/issues/65)、[ADR-0010 修訂](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0010-dev-self-and-acceptance.md:54)、[03 常用指令](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:28)。

- 位置：[03_interface.md「各指令專用選項」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:68)  
  問題：文件開頭宣稱列出「全部指令、選項」，但漏掉已定案的 `bootstrap.sh -i <image>`，也漏掉可重複的 `-t/--tool <repo>[@<tag>]`。因此 `bootstrap.sh` 的 `-i` 新寫法沒有進入對外介面文件。  
  建議：補列兩個選項，並註明 `<image>` 可以是已載入的本機 image 或 image tar 檔。  
  出處：[issue #65 追加決議](https://github.com/ycpss91255-research/vendor_kit/issues/65)、[issue #27 最新決議留言](https://github.com/ycpss91255-research/vendor_kit/issues/27)。

- 位置：[scope_roadmap.md:41](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/scope_roadmap.md:41)  
  問題：「tracked 的 `.vendor_kit/files/<repo>/`」使用了名詞表的 _Avoid_ 詞。  
  建議：改成「進 git 的 `.vendor_kit/files/<repo>/`」。  
  出處：[CONTEXT.md「進 git 的檔」](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:226)。

## 建議

- 位置：[scope_roadmap.md:8](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/scope_roadmap.md:8)、[scope_roadmap.md:29](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/scope_roadmap.md:29)  
  問題：「宣告」「宣告檔名」被用作 `version.toml`／版本鎖定行的同義詞，但 `CONTEXT.md` 沒有定義這個名詞。  
  建議：分別改成「版本鎖定行」與「`version.toml` 檔名」。  
  出處：[CONTEXT.md「version.toml」](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:211)、[「版本鎖定行」](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:267)。

- 位置：[02_invariants.md:69](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:69)  
  問題：「工具宣告為 append 的那些檔」中的「宣告」未定義，也沒指出在哪裡或用哪個欄位宣告。第一次閱讀無法判斷判準。  
  建議：改成能指出正式欄位的寫法，例如「工具將 `strategy` 設為 `append` 的初始檔」。  
  出處：[CONTEXT.md「初始檔」](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:285)、[同檔 append 型規則](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:252)。

- 位置：[03_interface.md:18](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:18)  
  問題：單一項目同時承載用途、下載方式、未發布警告、執行位置、git repo 前提、引擎下載、`install` 與修復語意，過長且難掃讀。  
  建議：仿 README，把未發布警告、操作前提及執行效果拆成緊接的短段。  
  出處：[README「第一次導入」](/home/cyc/Desktop/vendor-kit_ws/src/README.md:15)。

- 位置：[03_interface.md:71](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:71)  
  問題：新語法實際記在 ADR-0009 的修訂段，但出處只標「§2」；雖然修訂規定 §2 要按新寫法理解，讀者仍須自行找修訂。  
  建議：出處改成「ADR-0009 §2 與 2026-09-29 修訂」。  
  出處：[ADR-0009 修訂](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0009-release-assets-and-offline-import.md:38)。

- 位置：[scope_roadmap.md:35](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/scope_roadmap.md:35)、[scope_roadmap.md:36](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/scope_roadmap.md:36)  
  問題：每個表格儲存格塞入多條獨立規則、例外與錯誤處置，難以定位個別結論。  
  建議：在儲存格內分句列項，或連到承載正式機制的 ADR／決議段落。  
  出處：易讀性。

- 核對結果：九檔中的 Markdown 連結都有具名文字，目標檔與錨點存在；README shell 範例中的下載 URL 另有具名來源連結。五份 ADR 的必要段落、順序、`Amendment status` 均符合 [ADR 規則](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/README.md:21)，修訂段也涵蓋各檔全部舊寫法。README 與 03 的「用法＋常用指令」逐字一致。