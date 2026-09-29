## 結論

不一定算向後依賴。只要新的 03 總表把「下一步」欄中的字串明定為該訊息必須印出的完整、可直接執行指令，它就是在 03 首次定義具體用法；後面的 04 介面頁只是彙整並補全整體指令介面。反之，若 03 寫「指令語法見 04」或必須讀 04 才知道該字串是否合法，就確實是向後依賴。

## 理由

- `CONTEXT.md` 已先定義所有 VK recipe 的共同呼叫骨架是 `just vendor_kit <recipe>`，不是等介面頁才第一次定義。[CONTEXT.md:311](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:311)

- `CONTEXT.md` 已正式定義 `add`、`upgrade` 等 recipe 的名稱與基本語意；`<repo>`、`tag`、`-y`、一般選項也都已有定義。因此 `just vendor_kit add <repo>` 這類下一步可以只使用前置名詞組成。[CONTEXT.md:146](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:146)、[CONTEXT.md:197](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:197)、[CONTEXT.md:328](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:328)、[CONTEXT.md:332](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:332)、[CONTEXT.md:356](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:356)

- `upgrade --engine` 更沒有向後依賴問題：它已在 `CONTEXT.md` 的「救援路徑」定義中完整出現，包含完整呼叫 `just vendor_kit upgrade --engine -h`。[CONTEXT.md:396](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:396)

- 02 已經固定介面構造規則：所有 recipe 位於同一命名空間、位置參數只放 `<repo>`、引擎一律用 `--engine`、免問使用 `-y`。因此 `add <repo>`、`upgrade <repo> -y`、`upgrade --engine` 都能由前置文件直接判讀，不必依賴後面的介面頁。[02_invariants.md:239](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:239)、[02_invariants.md:243](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:243)、[02_invariants.md:263](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:263)

- 03 總表本身可以成為特定錯誤情境的定義來源。建議在表前明寫：

  > 「下一步」是該訊息逐字附帶、可直接執行的完整指令；本頁列出的寫法即為該情境的契約。全部指令與選項的總覽見下一頁，但理解或執行本頁指令不以下一頁為前提。

  這樣 `upgrade <repo>@<tag>` 等組合即由該列本身先行定義，04 再向後引用或彙整。這是文件所有權安排的推論，但符合「頁 N 只能用前面頁與 CONTEXT.md 名詞」：03 沒有借用 04 的定義。

- 現有草稿真正違反順序的是導言，而不是表格裡出現指令：它明確說結束碼意思見目前的介面頁，且連到 `03_interface.md`；換序後若仍指向新的 04，就是直接向後依賴。[04_messages.md:5](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_messages.md:5) 現有「下一步」欄已宣稱內容可直接複製執行，這個方向可以保留並強化為本頁自身的契約。[04_messages.md:9](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_messages.md:9)

- 把結束碼說明移入總表後，總表即可自行解釋每列的 `0`～`3`；目前這些語意已由 02 固定，可以直接以前頁為依據。[02_invariants.md:137](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:137)

- 舊訊息清單本來就把可複製指令視為訊息文字的一部分，而不是另頁介面定義的引用，例如 `add <repo>`、`upgrade <repo>` 與升引擎指令都直接寫在訊息列中。[interface_spec.md:521](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_legacy/interface_spec.md:521)、[interface_spec.md:530](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_legacy/interface_spec.md:530)、[interface_spec.md:540](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_legacy/interface_spec.md:540)、[interface_spec.md:563](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_legacy/interface_spec.md:563)

## 風險或反例

- 若 03 只列 `upgrade <repo>@<tag>`，卻把 `<repo>@<tag>` 的結合規則、必要參數或有效位置留到 04 才定義，讀者仍可能需要向後查證。最穩妥的做法是把每個「下一步」視為不可拆解的完整命令字串；不要在 03 展開通用文法。

- 03 與 04 都逐字維護同一批指令，可能漂移。應指定所有錯誤情境的可複製字串以 03 為準，04 只整理一般介面並向前引用 03；這是治理建議，屬推論。

- `just vendor_kit upgrade <repo>@<tag>` 雖然各組成名詞都已存在，但 `<repo>@<tag>` 這個組合目前是在介面頁才明列。[03_interface.md:56](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:56) 若不接受「03 該列就是首次定義」，便只能把這個組合提前定義到 `CONTEXT.md` 或其他前置頁；不能靠新的 04 補定義。

- 不宜把「下一步」降成 `upgrade`、`add` 之類的 recipe 名稱來避開問題。01 已承諾失敗會印出原因與下一步，02 更明定需人處理時要附可直接複製的指令；不完整片段不符合這項契約。[01_purpose.md:60](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:60)、[02_invariants.md:164](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:164)