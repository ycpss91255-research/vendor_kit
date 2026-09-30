## 結論

應寫成 `upgrade --engine=@<tag>`；未指定版本仍是 `upgrade --engine`。這是既有定案原則可直接推出的答案，`ask_user` 留空。

## 理由

- `--engine@<tag>` 不符合 GNU 語法：一般 parser 會把 `engine@<tag>` 視為完整選項名稱。GNU 長選項帶值應使用 `--option=value`；可省略的 option argument 尤其應以 `=` 連接。[GNU Argument Syntax](https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html)；repo 內稽核亦得到相同判斷（`doc/decisions/review_log/codex/q-cli-conventions-cli-audit.md:28-46`）。

- 不能只改成稽核建議的 `--engine=<tag>`。已定案第 17 條把指定工具版本固定為 `<repo>@<tag>`，理由正是「相同概念與對齊 UX」（`doc/decisions/review_log/discussion_queue.md:33`）；目前 `add`、`upgrade` 也都以此表示指定版本（`docs/contract/04_interface.md:81-84`）。拿掉引擎版本前的 `@`，會讓「指定 tag」變成工具用 `@<tag>`、引擎直接用 `<tag>`，違反「同一概念在所有指令裡都用同一種寫法」（`docs/contract/02_invariants.md:150-162`）。

- `--engine=@<tag>` 同時保留兩個已定案概念：
  - 對象是引擎仍一律由 `--engine` 表示，符合 issue [#65](https://github.com/ycpss91255-research/vendor_kit/issues/65#issuecomment-5893277424) 及介面規則（`docs/contract/04_interface.md:135-139`）。
  - 指定版本仍一律附加 `@<tag>`：`<repo>@<tag>`、`--engine=@<tag>`。`=`只是 GNU 用來分隔長選項名稱與其值的語法符號，不是版本表示法的一部分。這一點是依 GNU 語法與既有決議作出的推論。

- 相應用法應一致寫成：
  ```text
  upgrade --engine
  upgrade --engine=@<tag>
  ```
  並同步套用到訊息 6-10（現為 `docs/contract/03_messages.md:45`）、指令清單（`docs/contract/04_interface.md:92-93`）、名詞表（`GLOSSARY.md:211-213`）及 ADR-0008 現行修訂文字（`docs/adr/0008-protocol-and-file-schema-versions.md:72-85`）。

## 風險或反例

- `--engine=@v1.2.3` 比常見的 `--engine=v1.2.3` 少見，使用者可能誤以為 `@` 是值的一部分；但它正是保住已定案 `<target>@<tag>` 語彙所需的代價。這是可讀性風險，不是解析歧義。

- parser 必須把 `--engine` 定義成「可不帶值、也可帶值的長選項」，並只在帶值時接受 `--engine=@<tag>`。不應再接受 `--engine@<tag>`、`--engine=<tag>` 或 `--engine @<tag>`，否則會違反「第二種寫法不開」（`docs/contract/02_invariants.md:154-162`）。

- 若未來願意推翻第 17 條，另一套整齊方案是全面改成 `add <repo> --tag=<tag>`、`upgrade <repo> --tag=<tag>`、`upgrade --engine --tag=<tag>`；但在本題「第 17 條不可質疑」的前提下，這不是可採答案。