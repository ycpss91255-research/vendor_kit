## 必改

1. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:15`**
   - **問題：** 同一句先概括承諾「版本不足……只在 stderr 印訊息、以結束碼 `2` 結束」，後面卻說已有安裝目錄且 just 版本不足時，由 just 自己報錯，VK 不承諾自己的訊息。這兩種說法互相衝突；也與 04 對所有 just 版本不足情況一律回 `2`、印訊息 6-23 的寫法不一致。
   - **建議：** 把範圍拆清楚：
     - Docker 版本不足與 Podman：首次導入、已有安裝目錄都由啟動器處理，承諾 VK 訊息及結束碼 `2`。
     - just 版本不足：只有 `bootstrap.sh` 情境承諾訊息 6-23 與結束碼 `2`；已有安裝目錄由 just 解析器拒絕，不承諾 VK 訊息及 VK 結束碼。
     - 同時使 04 的主機需求與這個區分一致。
   - **證據：** `docs/adr/0007-host-thin-layer-and-shell-integrity.md:15,22`；`docs/contract/03_messages.md:58` 明定 6-23 只由 `bootstrap.sh` 觸發；`docs/contract/04_interface.md:42-46` 未區分兩種 just 情況；`docs/adr/0004-vk-recipe-interface-and-write-boundary.md:26` 又說首次導入與已有安裝目錄「都一樣」。

2. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:29`**
   - **問題：** 舊薄殼遇到新 major 時允許留下執行紀錄，對不上不變量 10 與 ADR-0008 的「任何副作用之前判定、零寫入」。雖然不變量 4 與 03 的結束碼表容許執行紀錄例外，但目前較強的版本相容性條文沒有寫這個例外。
   - **建議：** 明確選定一個契約：若版本組合不合仍可寫執行紀錄，就在引用不變量 10／ADR-0008 時說明「零寫入不含執行紀錄」，並讓被引用文件有同樣例外；否則 0007 應移除執行紀錄例外。
   - **證據：** `docs/contract/02_invariants.md:94` 容許執行紀錄例外，但 `docs/contract/02_invariants.md:190` 要求任何副作用前判定並零寫入；`docs/contract/03_messages.md:24` 容許執行紀錄；`docs/adr/0008-protocol-and-file-schema-versions.md:3,29,31` 使用「零寫入」且沒有例外。

3. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:19`**
   - **問題：** 「白名單多一個主機命令……得先修訂不變量 5」說得過頭。不變量 5 已明文排除支援平台既有的 shell 與基本指令；若新增的是另一個基礎 userland 命令，只需變更 04 的明列清單與 lint，不必修訂不變量。只有新增額外安裝依賴才會改到不變量 5。
   - **建議：** 改成區分「新增基礎 userland 白名單命令」與「新增必須另行安裝的主機依賴」；前者改 04 與 lint，後者才須先修訂不變量 5。
   - **證據：** `docs/contract/02_invariants.md:110-116`；`docs/contract/04_interface.md:24-40`；`docs/adr/0007-host-thin-layer-and-shell-integrity.md:23` 自己也把 POSIX sh、基礎 userland 與 Docker 分開列。

## 建議

1. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:20`**
   - **問題：** 驗收案例只寫「低版本 just 各一條」，但本 ADR 已定義兩種不同路徑：首次導入由 `bootstrap.sh` 回 VK 訊息；已有安裝目錄由 just 在解析期自行失敗。一條案例無法覆蓋兩份不同承諾。
   - **建議：** 拆成兩個黑箱案例，分別驗證首次導入與已有安裝目錄；後者只驗證在任何 VK 副作用前被拒絕，不驗 VK 訊息。
   - **證據：** `docs/adr/0007-host-thin-layer-and-shell-integrity.md:15,20,22`；`docs/contract/03_messages.md:58`。

2. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:3`**
   - **問題：** 首段把主機依賴、薄殼完整性、規則邊界、兩段升級與跨 major 救援全部塞在一段；「舊薄殼遇上新 major」也混用了 `major` 與契約採用的 `X`，第一次閱讀不容易立即確認兩者是否同義。
   - **建議：** 拆成「主機命令邊界」「薄殼完整性」「升級與跨 X 救援」三句或三段，並將 `major` 統一寫成「較新的 X」。
   - **證據：** `docs/adr/0007-host-thin-layer-and-shell-integrity.md:3`；`docs/contract/01_purpose.md:85-90`、`docs/contract/02_invariants.md:178-190` 都使用 `X.Y.Z`／「X 變動」。

3. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:15`**
   - **問題：** 一個項目同時處理三種前置檢查、兩種安裝狀態、訊息承諾與執行紀錄時序，例外埋在句子中段，是本檔最容易誤讀之處。
   - **建議：** 改成小表格或兩個子項，按「檢查項目／首次導入／已有安裝目錄／訊息與結束碼／是否有執行紀錄」列出。
   - **證據：** `docs/adr/0007-host-thin-layer-and-shell-integrity.md:15`；兩種 just 行為另於 `:22` 重複一次，顯示目前段落難以承載這個分支。