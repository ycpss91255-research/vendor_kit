## 結論

6-3 的 `add` 分支目前沒有合法的「直接指定版本」指令；在現有介面下只能請使用者設定憑證後重跑 `just vendor_kit add <repo>`，不能寫成 `upgrade`。6-39 攑成「失敗」不對，因為訊息明確要求使用者更換 Docker 後重試；6-19 補 `just vendor_kit upgrade --engine` 原則上正確，但不是對所有未來檔案版都保證有效。

## 理由

1. 6-3 對 `add` 給 `upgrade <repo>@<tag>`，會操作錯誤的生命週期。

   - 6-3 明列觸發者包含 `add`，但下一步固定為 `just vendor_kit upgrade <repo>@<tag>`：[04_messages.md:15](doc/decisions/review/04_messages.md#L15)。
   - `add` 是「把工具納入」，`upgrade` 是「把已鎖定版本換成新版」：[03_interface.md:56](doc/decisions/review/03_interface.md#L56)、[03_interface.md:57](doc/decisions/review/03_interface.md#L57)。對尚未納入的工具執行 `upgrade`，語意不成立。
   - 現有介面只有 `add <repo>`、`add <repo> -i <image>`；只有 `upgrade` 定義了 `<repo>@<tag>`：[03_interface.md:56](doc/decisions/review/03_interface.md#L56)、[03_interface.md:58](doc/decisions/review/03_interface.md#L58)、[03_interface.md:138](doc/decisions/review/03_interface.md#L138)。
   - 因此，在不新增介面的前提下，`add` 情境應給：「設定 `VENDOR_KIT_REGISTRY_TOKEN`／`_TOKEN_FILE` 後，重跑 `just vendor_kit add <repo>`」。這是推論，但它是目前唯一已定義、可直接複製且不改變動詞語意的 VK 指令。
   - 02 又要求 6-3 提供「設定憑證」或「直接指定 `@<tag>`」兩條路：[02_invariants.md:109](doc/decisions/review/02_invariants.md#L109)。所以若維持兩條路，真正缺的是介面契約中的 `add <repo>@<tag>`；不能只在訊息表偷渡這個用法。`add -i` 是本機 image／tar 的離線路徑，不等同線上直接指定 tag：[03_interface.md:138](doc/decisions/review/03_interface.md#L138)。

2. 6-39 應維持「需人處理」，不是「失敗」。

   - 名詞表把「需人處理」定義為「VK 停下並要求使用者採取下一步」：[CONTEXT.md:340](CONTEXT.md#L340)。6-39 正是在要求使用者改用 Docker 後重試：[04_messages.md:22](doc/decisions/review/04_messages.md#L22)。
   - 舊清單也把同一句 6-39 分為「需人處理」：[interface_spec.md:566](doc/decisions/_legacy/interface_spec.md#L566)。
   - 改成「失敗」的實際理由似乎只是沒有可直接複製的安裝／切換 Docker 指令；但這是推論，而且「缺少通用指令」不會讓所需的人工作業消失。
   - 真正的問題是另一個：02 要求「需人處理」附可直接複製的指令：[02_invariants.md:166](doc/decisions/review/02_invariants.md#L166)，而 6-39 目前下一步為 `—`。應處理這個契約例外或改寫規則，不能靠改類別掩蓋。

3. 6-19 補 `just vendor_kit upgrade --engine` 是合理且可執行的主要下一步。

   - 6-19 是現有引擎讀到高於支援上限的檔案版；ADR 固定回 `3`、寫入前停止：[ADR-0008:59](doc/adr/0008-protocol-and-file-schema-versions.md#L59)。
   - `upgrade --engine` 是正式介面：[03_interface.md:66](doc/decisions/review/03_interface.md#L66)，並且引擎升級是永久救援路徑：[ADR-0007:61](doc/adr/0007-host-thin-layer-and-shell-integrity.md#L61)、[ADR-0007:71](doc/adr/0007-host-thin-layer-and-shell-integrity.md#L71)。
   - 結束碼 `3` 本來就表示版本組合不合，必須先升級或退回才能繼續：[03_interface.md:185](doc/decisions/review/03_interface.md#L185)。因此補上這條指令比舊文案「請使用支援此檔案版的引擎」更符合可操作性要求。

## 風險或反例

- 若檔案由尚未正式發布、dev 覆寫或未來版本寫成，當前最新版引擎也可能不支援檔案版 `<N>`；此時 `upgrade --engine` 仍會失敗。這是推論。建議文案不要宣稱該指令必定修復，只把它列為第一步，並保留 `<written_by>` 供診斷。
- 若把 6-3 拆成 `add` 與 `update`／`upgrade` 兩種文案，仍可共用編號，但「意思」與「下一步」必須明確按原始指令分支；否則自動化測試無法逐字斷言。
- 若堅持 6-39 必須因「沒有可複製指令」而列為失敗，就必須先收窄 `CONTEXT.md` 對「需人處理」的定義；以目前定義直接改類別，分類會自相矛盾。