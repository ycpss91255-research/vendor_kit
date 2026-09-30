## 結論

五種情況都應補進 03，因為它們都會讓執行停止，且需要向使用者說明原因或下一步；漏列會使「總表」無法成為其他文件引用的唯一訊息契約。[03_messages.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_messages.md:3) [03_messages.md:5](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_messages.md:5)

編號應保留舊規格既有的 `6-4`、`6-28`、`6-38`；Docker 版本不足與 metadata 無法還原沒有舊編號，依序新增 `6-40`、`6-41`。文字以現行 02／ADR 的行為為準，舊規格只提供措辭底稿；凡含舊指令的地方改成 `upgrade --engine`，不得照抄 `upgrade vendor_kit`。

## 理由

1. **非互動又沒有 `-y`：補為 `6-4`。**

   舊總表已明確把它編成 `6-4`，文字是「需要確認但沒有終端可互動。請加 -y，或在終端執行。」並以 `1` 結束。[interface_spec.md:531](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_legacy/interface_spec.md:531) 現行名詞表仍把 `-y` 定義為預先回答詢問的選項，並確認短、長寫法為 `-y`／`--yes`。[CONTEXT.md:324](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:324) [CONTEXT.md:332](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:332)

   建議沿用原文與編號；它沒有過時指令，不需改寫。

2. **薄殼被修改：補為 `6-28`，但要重寫舊文字。**

   現行 02 明定「薄殼被改過必須能被發現並停下」。[02_invariants.md:130](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:130) ADR-0007 將結果具體化為結束碼 `1`、列出差異、不動任何檔。[0007-host-thin-layer-and-shell-integrity.md:35](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:35) ADR-0004 又明定「薄殼不符」是三種必須有固定訊息編號的情境之一，且指出目前總表缺少它。[0004-vk-recipe-interface-and-write-boundary.md:28](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:28) [0004-vk-recipe-interface-and-write-boundary.md:89](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:89)

   舊規格已給 `6-28`，但含過時的 `upgrade vendor_kit`，也把還原方式綁死為 `git checkout`。[interface_spec.md:555](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_legacy/interface_spec.md:555) 建議現行文字為：

   > `偵測到薄殼被修改：<files>。未重產任何薄殼。請先檢視下列差異；確認並手動還原後，再執行：just vendor_kit upgrade --engine`

   「不指定 `git checkout`」是推論：02 只要求停下及報告，且 VK 不讀、不改 git 資料；把特定 git 還原命令寫成唯一答案沒有現行契約依據。[02_invariants.md:82](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:82)

3. **建不出執行紀錄：補為 `6-38`。**

   現行 02 明定執行紀錄不可關閉，建立失敗時以失敗結束且不動任何檔。[02_invariants.md:99](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:99) [02_invariants.md:102](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:102) ADR-0004 規定執行紀錄早於任何寫入、拉 image 或啟動引擎。[0004-vk-recipe-interface-and-write-boundary.md:72](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:72)

   舊規格已有完整的 `6-38` 文字，且明列所有 recipe 一致、無停用選項。[interface_spec.md:565](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_legacy/interface_spec.md:565) 可沿用其核心文字：

   > `無法寫入執行紀錄 <path>：<原因>。vendor_kit 不在沒有紀錄的情況下執行。請清出磁碟空間（例如刪除 .vendor_kit/log/ 下的舊檔）或修正權限後重試。`

   不應再提舊 `help` recipe；現行救援介面已改成特定呼叫的印用法，而不是 `help` recipe。[CONTEXT.md:401](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:401)

4. **Docker 版本低於下限：新增 `6-40`。**

   ADR-0007 已定 Docker 下限為 19.03，且要求在任何寫入之前檢查。[0007-host-thin-layer-and-shell-integrity.md:21](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:21) [0007-host-thin-layer-and-shell-integrity.md:26](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:26) 04 也明定版本不足以 `1` 結束，但目前只替 just 連到 `6-23`，Docker 沒有對應訊息。[04_interface.md:41](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:41)

   舊清單 `6-1` 至 `6-39` 都已有用途，因此不應借用舊號；新增 `6-40` 是避免改變既有公開鍵的最小作法。[interface_spec.md:527](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_legacy/interface_spec.md:527) [interface_spec.md:566](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_legacy/interface_spec.md:566)

   建議文字：

   > `需要 Docker ≥ 19.03，目前為 <version>。請升級 Docker 後重試。`

   這段文字是**推論**：現行文件確定了門檻與停止行為，但 repo 中沒有已定案的逐字 Docker 低版本訊息。若要符合 ADR-0007 所稱「有可以照做的指令」，還必須另行決定各支援平台的安裝指令；目前證據不足以安全地虛構一條通用命令。[0007-host-thin-layer-and-shell-integrity.md:100](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:100)

5. **metadata 缺失且無法可靠還原：新增 `6-41`。**

   02 明定紀錄缺失且無法可靠還原時不得猜，必須停下並報告。[02_invariants.md:36](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:36) ADR-0003 重複相同決議，並涵蓋舊格式升級。[0003-baseline-merge-and-line-records.md:55](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0003-baseline-merge-and-line-records.md:55) 名詞表則確認 metadata 是記錄初始檔來源與納管狀態的 VK 檔。[CONTEXT.md:292](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:292)

   舊訊息清單沒有這一情境的編號或逐字文字；因此新增 `6-41`，而不是把其他舊號重新解釋。建議文字：

   > `無法處理 <file>：metadata 缺失，且無法可靠還原其納管紀錄。未修改任何檔。請從可信的備份或版本還原 metadata 後重試。`

   這段文字是**推論**。其中「可信的備份或版本」仍需確認實際 metadata 是否進 git；在該保存方式定案前，不應寫成特定 `git restore` 指令。

## 風險或反例

- `6-28` 的「薄殼被修改」與「薄殼只是版本落後」不能混成同一列。前者是完整性比對失敗；後者可能是正常升級流程。ADR-0007 明確區分重算標頭與對照引擎模板這兩種判定。[0007-host-thin-layer-and-shell-integrity.md:37](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:37) [0007-host-thin-layer-and-shell-integrity.md:40](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:40)

- Docker `6-40` 與 Podman `6-39` 也不能合併：前者是受支援產品的版本不足，後者是產品種類不受支援；兩者的處置不同。[0007-host-thin-layer-and-shell-integrity.md:23](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:23)

- metadata `6-41` 目前只能定義安全停止與原因，不能宣稱已有固定恢復命令。若 03 把它列為「需人處理」，依總表對結束碼 `1` 的定義應附可直接複製的指令；現有文件尚不足以提供這條指令。[03_messages.md:21](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_messages.md:21) 在保存位置未釐清前，較誠實的類別是「失敗」，下一步用文字說明而非杜撰命令。