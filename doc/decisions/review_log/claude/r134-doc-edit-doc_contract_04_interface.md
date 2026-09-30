# r134 審查：doc/contract/04_interface.md

這一輪 04 本身只改了第 98 行。定案核對：對照 map #78「Decisions so far」、#117、#114、#115、#122、#123，第 98 行的改動沒有違反任何定案，也沒有改 01 的承諾、02 的不變量或 03／04 的介面。四支 lint（check_context、check_messages、check_review_pages、check_terms）都回 0。下面列的必改是 03 新增的例子跟 04 對不上；照規則算在 04 身上，但要改的是 03。

## 必改

1. 位置：doc/contract/03_messages.md「結束碼」一節新增的輸出示意，B 那一行（對照 04 第 189 行）
   - 問題：04 第 189 行寫 `update --exit-code` 查到新版時「除了在 stdout 印出查詢結果，也在 stderr 印出 VK0022 警告」。示意裡 B 只有 stderr 的 VK0022，少了 stdout 的查詢結果，跟 04 對不上；A 的 stdout 行也就變成只有「最新」才印 stdout 的錯覺。
   - 建議：在 B 的 stderr 行前面補一行 `stdout: B 有新版：目前為 <current_tag>，新版為 <new_tag>。`（或同等的查詢結果示意），再接原本的 `stderr: vendor_kit: warn[VK0022]: …`。
   - 證據：doc/contract/04_interface.md 第 188～189 行；doc/contract/03_messages.md 新增示意（約第 31～38 行）。

2. 位置：doc/contract/03_messages.md 輸出示意，C 那一行 `just vendor_kit update C@<tag>`（對照 04 第 73～86 行、03_messages.csv VK0001 的 note）
   - 問題：04 的指令清單裡 `update` 不接受 `<repo>@<tag>`，帶 `@<tag>` 的只有 `add` 和 `upgrade`（第 73～76、86 行）。CSV VK0001 的 note 也寫明「update、upgrade 時是 upgrade」。示意寫成 `update C@<tag>`，跟 04 和 CSV 都衝突，還等於示範了 04 沒有的用法。
   - 建議：改成 `just vendor_kit upgrade C@<tag>`。
   - 證據：doc/contract/04_interface.md 第 74、76、86 行；doc/contract/03_messages.csv 第 2 行（VK0001）的 note 欄。

## 建議

1. 位置：doc/contract/04_interface.md 第 98 行 `- [名詞表](../../GLOSSARY.md#工具與出貨)的 `<repo>``
   - 問題：同一份清單其他項的連結文字就是名詞本身（工具、安裝目錄……），只有這項的連結文字是「名詞表」，格式不一致。第 95 行已經寫了「清單裡的名詞見名詞表」，再寫一次「名詞表的」是重複。
   - 建議：改成先列名詞、再附連結，例如 `- `<repo>`：見[名詞表](../../GLOSSARY.md#工具與出貨)`，或 `- [工具名](../../GLOSSARY.md#工具與出貨) `<repo>``（GLOSSARY 第 43 行：`<repo>` 也是工具名）。兩種寫法的連結文字都不含反引號。
   - 證據：doc/contract/04_interface.md 第 95～104 行；GLOSSARY.md 第 42～44 行。

2. 位置：doc/contract/04_interface.md 第 48～50 行（VK0001 的兩條路）
   - 問題：VK0001 在 `update` 時也會觸發，但「直接指定版本 `@<tag>`」只對 `add`、`upgrade` 有意義，`update` 沒有 `@<tag>` 形式。第一次看的人會以為 `update <repo>@<tag>` 可以用。這一輪 VK0001 改成「失敗」，這句是一般建議，跟判準不衝突，只是沒寫清楚。
   - 建議：第 50 行改成「改用 `add <repo>@<tag>` 或 `upgrade <repo>@<tag>` 直接指定版本」，跟 CSV note 一致。
   - 證據：doc/contract/04_interface.md 第 48～50、86 行；doc/contract/03_messages.csv VK0001 的 note。
