## 結論

套用已定案的 1／2 對調後，`0／1／2／3` 的語意與「取最大值」彼此一致，也與 `diff`、`grep`、argparse 的主要慣例相容；問題在於 03、04 尚未同步，以及數個會影響腳本的介面契約仍未定義。真正無理由偏離主流慣例的地方有八項：`--engine@<tag>`、未承諾 `--`、沒有 `--version`、help／用法錯誤的串流未定、一般輸出的 stdout／stderr 未分流、錯誤無固定前綴、顏色未定、CI 模式由通用環境變數暗中改變核心行為。

## 理由

### 1. 03、04 仍是舊碼義；全部引用必須一起換，不能只改總表

現況仍定義：

- `1`＝失敗或需人處理、`2`＝完成但要人接手：[03_messages.md:20–29](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_messages.md:20)
- 13 條訊息仍把失敗／需人處理寫成 `1`：[03_messages.md:42](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_messages.md:42)
- 04 的位置錯誤、用法錯誤、非互動拒絕、CI 拒絕等仍寫 `1`：[04_interface.md:116](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:116)、[04_interface.md:133](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:133)、[04_interface.md:174](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:174)、[04_interface.md:254](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:254)
- `update --exit-code` 查到新版仍寫 `2`：[04_interface.md:183](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:183)

已定案內容則明確要求 `1`／`2` 對調且取最大值：[discussion_queue.md:35](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review_log/discussion_queue.md:35)。

建議改法：

- `1`：完成但有條件要呼叫端處理，包括合併衝突、`update --exit-code` 查到新版。
- `2`：失敗、需人處理、用法錯誤、未知選項、缺參數、無 TTY 且缺 `-y`。
- `3`：版本組合不合。
- 聚合結果直接取 `max(results)`，刪除所有優先序特例。
- 03 第 42–54 行目前所有 `1` 都應改成 `2`；`3` 不動；04 所有上述 `1` 同步改成 `2`，`update --exit-code` 的 `2` 改成 `1`。

這套新語意本身沒有問題：GNU `diff` 是 `0` 無差異、`1` 有差異、`2` 出錯；GNU `grep` 是 `0` 有匹配、`1` 無匹配、`2` 出錯；argparse 用法錯誤也是 `2`。[GNU diff exit status](https://www.gnu.org/software/diffutils/manual/html_node/Invoking-diff.html)、[GNU grep exit status](https://www.gnu.org/software/grep/manual/html_node/Exit-Status.html)、[argparse exiting methods](https://docs.python.org/3/library/argparse.html#exiting-methods)

### 2. `--engine@<tag>` 不是 GNU 長選項寫法

04 同時列出：

- `upgrade --engine`
- `upgrade --engine@<tag>`

證據：[04_interface.md:91–94](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:91)。

GNU 長選項的帶值形式是 `--option=value` 或在必要參數時寫成下一個 argv；argparse 同樣接受 `--foo BAR` 與 `--foo=BAR`。`--engine@v1` 會被一般 parser 看成名為 `engine@v1` 的整個選項，而不是 `--engine` 的值。[GNU argument syntax](https://ftp.gnu.org/old-gnu/Manuals/glibc-2.2.5/html_node/Argument-Syntax.html)、[argparse option-value syntax](https://docs.python.org/3/library/argparse.html#option-value-syntax)

建議改成：

```text
upgrade --engine
upgrade --engine=<tag>
```

並明定 `--engine <tag>` 是否接受。若 `<tag>` 是 optional argument，GNU 慣例以 `=` 避免下一個 token 的歧義，因此只接受 `--engine=<tag>` 反而合理。

### 3. 沒有承諾接受 `--`，使以 `-` 開頭的 `<repo>` 無法可靠表示

04 宣稱「選項照 GNU 慣例」，但只列短長選項，未定義獨立的 `--`：[04_interface.md:132–140](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:132)。`<repo>` 又是唯一位置參數：[04_interface.md:135](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:135)。

POSIX Utility Syntax Guideline 10 與 GNU 都把獨立 `--` 定義成選項結束符；其後即使以 `-` 開頭也必須當 operand。[POSIX Utility Syntax Guidelines](https://pubs.opengroup.org/onlinepubs/7908799/xbd/utilconv.html)、[GNU CLI standards](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html)

建議明定所有入口接受：

```text
just vendor_kit add -- -repo
```

以及 `--` 後不再解析任何選項。這也應適用 `bootstrap.sh` 和 `.vendor_kit/ci/check.sh`。

### 4. 缺少 `--version`

完整選項清單沒有 `--version`：[04_interface.md:128–140](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:128)。這是 GNU Coding Standards 明定所有程式都應有的標準選項；Cargo、npm、just 也都提供。[GNU CLI standards](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html)、[GNU `--version`](https://www.gnu.org/prep/standards/html_node/_002d_002dversion.html)、[Cargo options](https://doc.rust-lang.org/cargo/commands/cargo.html)、[npm version](https://docs.npmjs.com/cli/v11/using-npm/config/#version)、[just manual](https://just.systems/man/en/)

建議至少提供：

```text
just vendor_kit --version
```

行為定為：

- stdout。
- 結束碼 `0`。
- 不寫執行紀錄、不啟動容器、不做版本相容性檢查。
- 第一行固定且容易解析，例如 `vendor_kit 1.2.3`。
- 若薄殼版與引擎版都重要，另列具名欄位，不要只印一個無法判斷所指對象的版本。

### 5. `-h`／`--help` 的 stdout、成功碼及優先級未定義

04 只說 help「印出用法」，沒有說串流、結束碼，也沒有說與錯誤參數並存時是否仍成功：[04_interface.md:128–134](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:128)。

GNU 的明確慣例是：

- help 印到 stdout；
- 結束碼 `0`；
- 看到 `--help` 後忽略其他 options／arguments；
- 不執行正常功能。

Python argparse 與本 repo 要求的 just 也採 help→stdout、成功退出。[GNU `--help`](https://www.gnu.org/prep/standards/html_node/_002d_002dhelp.html)、[argparse help](https://docs.python.org/3/library/argparse.html#the-add-help-argument)

建議把契約補成：

```text
-h/--help：stdout，exit 0，不產生任何產品副作用。
```

缺指令、缺參數、未知選項則是另一條路徑：usage 與診斷印 stderr，依新碼義退出 `2`。POSIX 明定未知選項或缺 option argument 要診斷到 stderr 並非零退出；argparse 具體採 `2`。[POSIX utility introduction](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap01.html)、[argparse error](https://docs.python.org/3/library/argparse.html#exiting-methods)

### 6. 人類結果與診斷沒有 stdout／stderr 分流契約

03 逐字固定了 13 條訊息，卻沒有任何一條說輸出到哪個 stream：[03_messages.md:32–54](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_messages.md:32)。04 對一般結果、警告、錯誤、usage 也沒有分流規則。

這會直接影響：

```sh
result=$(just vendor_kit update)
```

呼叫端無法知道 `result` 是正常資料、警告、失敗說明，還是三者混在一起。GNU 將錯誤與診斷放 stderr；機器輸出通常放 stdout。[GNU standard streams](https://www.gnu.org/software/libc/manual/2.35/html_node/Standard-Streams.html)、[GNU error messages](https://www.gnu.org/software/libc/manual/2.32/html_node/Error-Messages.html)

建議定一條全域規則：

- stdout：正常結果、`--help`、`--version`、明確定義的機器格式。
- stderr：錯誤、警告、usage error、提示與進度。
- 若某條訊息由多行組成，整條必須在同一 stream。
- 不依重導向狀態改變核心語意。

### 7. 錯誤訊息沒有穩定前綴，難以辨識訊息來源

03 的固定訊息直接以「無法……」「需要……」「偵測到……」開頭，沒有程式名稱或嚴重度前綴：[03_messages.md:42–54](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_messages.md:42)。

在 just、啟動器、Docker、引擎可能連續輸出的情況下，使用者和 log aggregator 無法可靠判斷哪一層發出訊息。GNU 慣例是非互動程式使用：

```text
program: message
```

並輸出到 stderr；argparse 則採 `prog: error: message`。[GNU Errors](https://www.gnu.org/prep/standards/html_node/Errors.html)、[glibc Error Messages](https://www.gnu.org/software/libc/manual/2.32/html_node/Error-Messages.html)

建議固定為：

```text
vendor_kit: error: …
vendor_kit: warning: …
vendor_kit: action required: …
```

若必須保留中文，可固定中文類別，但 `vendor_kit:` 前綴應保持穩定。不要依顏色單獨表達類別。

### 8. 顏色行為完全未定義

03／04 沒有說：

- 是否輸出 ANSI 色碼；
- 非 TTY 是否關閉；
- stdout 與 stderr 是否分開判斷；
- 如何強制關閉；
- 機器輸出是否保證無色。

這會影響 redirect、CI log、字串比較與機器解析。Cargo 和 just 採 `--color always|auto|never`，預設 `auto`；npm 只在適當 TTY 上預設著色並考慮 `NO_COLOR`；Git porcelain 強制無色。[Cargo display options](https://doc.rust-lang.org/cargo/commands/cargo.html)、[npm color](https://docs.npmjs.com/cli/v11/using-npm/config/#color)、[Git porcelain format](https://git-scm.com/docs/git-status#_porcelain_format_v1)

建議：

- 預設 `auto`，逐一依目標 stream 是否為 TTY 判斷。
- 支援 `--color=always|auto|never`；若不想新增公開選項，至少支援 `NO_COLOR`。
- 非 TTY、機器格式及寫入執行紀錄的文字一律無 ANSI。
- 訊息即使去掉顏色也必須保留完整語意。

### 9. `CI` 通用環境變數會暗中改變核心寫入語意

04 規定只要 `CI` 有值且不是 `0`／`false` 就進入 CI 模式，並改變是否允許寫入及某些結果碼：[04_interface.md:252–258](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:252)。這不是只關閉顏色或進度，而是改變 recipe 的核心行為。

主流工具確實常用 CI 偵測調整呈現；例如 npm 用它決定是否顯示 progress。但 `-y` 仍是獨立、明示的確認選項，CI 不等於 yes。[npm progress](https://docs.npmjs.com/cli/v11/using-npm/config/#progress)、[npm yes](https://docs.npmjs.com/cli/v11/using-npm/config/#yes)

此處的安全目標有理由——CI 不應寫進 git 的檔——但使用通用、無正式跨工具規格的 `CI` 真值規則來切換核心模式，沒有相應理由。任一父程序殘留 `CI=1` 都會令本機命令突然拒絕操作。

建議：

- `.vendor_kit/ci/check.sh` 明確進入 CI 模式，因為入口本身已表達意圖。
- 日常入口改用專屬 `VENDOR_KIT_CI=1` 或明示 `--ci`。
- 若仍保留通用 `CI` 自動偵測，至少提供明示覆寫，並在拒絕時說明是由哪個環境變數觸發。
- 無 TTY 且缺 `-y` 的既有處理可以保留：拒絕、零修改、exit `2`，不能把 CI 或 EOF 當同意。現行這部分符合安全慣例：[04_interface.md:161–179](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:161)。

## 風險或反例

- 選項放在 operand 後面，例如 `upgrade <repo> -y`，[04_interface.md:157](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:157)，偏離 POSIX Guideline 9，但符合文件自己選定的 GNU 解析方式；GNU `getopt` 通常允許 options 與 operands 交錯。因此這不是需要修改的無理由偏離，只需明定所有選項順序等價、互斥情況除外。
- `--dry-run` 仍寫執行紀錄，[04_interface.md:167–172](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:167)，確實比 just 的「不做，只印會做什麼」更有副作用；但 repo 已以「永不靜默失敗、任何執行可追溯」作出理由：[02_invariants.md:88–104](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:88)。因此不列為「沒有理由」的偏離。仍應在 help 中醒目標示 dry-run 會寫哪個 log、會不會拉 image、建立 cache 或連網。
- 沒有 `--porcelain`／`--json` 不必然是缺陷：ADR 已明確選擇由執行紀錄承擔結構化結果，避免維護第二套平行輸出：[0005-run-log-and-event-registry.md:55](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0005-run-log-and-event-registry.md:55)。但對外文件必須明說一般訊息不是穩定機器格式，並公布腳本應讀取的執行紀錄格式；否則使用者仍會被迫解析 03 的中文句子。
- 結束碼 `3` 沒有跨工具通用語意，但 POSIX 只要求成功為 `0`、失敗為非零；Cargo甚至用 `101` 表示一般失敗。因此保留 `3` 表示版本組合不合不是慣例違反。真正要求是所有入口一致採用同一語意，且聚合時按已定案規則取最大值。