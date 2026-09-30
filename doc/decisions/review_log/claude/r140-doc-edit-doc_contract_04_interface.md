# r140 doc-edit 審查：doc/contract/04_interface.md

範圍：`diff -u doc/decisions/_backup/doc_contract_04_interface.pre_r140.md doc/contract/04_interface.md`

## 必改

（無）

查核結果：
1. 已定案（map #78 Decisions so far）：diff 只有行內程式碼邊界補空白（約 27 處「`2`結束」→「`2` 結束」等）與第 126 行救援路徑清單，沒有碰到任何一條定案（#82、#83、#99、#91 等皆未受影響）。
2. 對外承諾：空白調整不改語意；第 126 行新增的清單與 doc/adr/0007-host-thin-layer-and-shell-integrity.md 第 32 行逐項一致（install、upgrade --engine、sync 的不符判定、四種印用法呼叫、長選項 --help 同），沒有新增或刪減承諾。
3. 做完沒：ask 第 1 項（04 的行內程式碼邊界）`check_typography.py doc/contract/04_interface.md` 回 OK；以 `[\p{Han}]`|`[\p{Han}]` 掃 04 無殘留。ask 第 2 項已在第 126 行直接列出救援路徑的呼叫，「救援路徑」仍連到 GLOSSARY。
4. 連結：第 126 行 `../../GLOSSARY.md#介面版與契約`：路徑存在（repo 根 GLOSSARY.md），錨點由腳本依 GitHub slug 規則從標題算出，`### 介面版與契約`（GLOSSARY.md 第 238 行）存在。其他改動行的連結文字與目標未變。

## 建議

- 位置：doc/contract/04_interface.md 第 126 行
  - 問題：句子前半講的是「版本組合不相符時 `-h` 怎麼反應」，接著「一定能用的只有救援路徑，也就是…」列出的清單包含 `install`、`upgrade --engine`、`sync` 的不符判定這三個不是 `-h` 的呼叫，讀者會以為這三個也是 `-h` 的形式，或誤以為清單是 `-h` 的例外表。
  - 建議：把清單拆成獨立一句，例如「…`-h` 怎麼反應，這一頁不定。不論版本組合是否相符都一定能用的只有[救援路徑](../../GLOSSARY.md#介面版與契約)：`install`、`upgrade --engine`、`sync` 的不符判定，以及四種印用法的呼叫：…（長選項 `--help` 同）」。
  - 證據：doc/contract/04_interface.md 第 126 行；doc/adr/0007-host-thin-layer-and-shell-integrity.md 第 32 行（原文把救援路徑定義為「不論…版本組合是否相符都永久可用」的呼叫，不限 `-h`）。
- 位置：doc/contract/04_interface.md 第 126 行連結錨點
  - 問題：`#介面版與契約` 指到 GLOSSARY 的整節（第 238 行），不是「救援路徑」詞條本身（第 249 行）；詞條是粗體段落，沒有自己的錨點，讀者要在節內自己找。非本輪引入，只提醒。
  - 建議：維持現狀即可；若之後 GLOSSARY 給詞條加錨點再改。
  - 證據：GLOSSARY.md 第 238、249 行。
