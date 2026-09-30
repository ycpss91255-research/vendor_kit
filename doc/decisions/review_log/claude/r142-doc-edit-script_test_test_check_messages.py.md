# r142 審查：script/test/test_check_messages.py

範圍：拿 `doc/decisions/_backup/script_test_test_check_messages.pre_r142.md` 跟現檔 diff（任務寫的備份檔名 `...test_check_messages.py.pre_r142.md` 不存在，實際檔名少了 `.py`）。`python3 -m unittest script/test/test_check_messages.py` 41 個測試全過，`python3 script/check_messages.py` 的結果是 OK。

## 必改

無。逐條對照 map #78 的「Decisions so far」與 #117 之後，這一輪沒有違反定案：warn→1、error→2、fatal→3 跟 03_messages.md:22、:82 一致。01、02 沒動，code、level、處置、next_step 的語意也沒變。這是測試檔，沒有對外連結、「出處：」行或名詞問題。

## 建議

1. **位置**：CodeTest.test_retired_must_be_empty（第 168–173 行）
   **問題**：retired 列只驗 `message`、`next_step` 要清空，新加的 `exit_code`、`description` 沒驗。03_messages.md:82 明寫「`retired` 列留空」，check_messages.py:170–172 靠 RETIRED_KEEP 泛用檢查，但沒有測試釘住。
   **建議**：在這個測試另外設定 `rows[3][HEADER.index("exit_code")] = "2"` 與 `rows[3][HEADER.index("description")] = "舊說明"`，斷言 `VK0004:exit_code: retired 列只留`、`VK0004:description: retired 列只留`。
   **證據**：doc/contract/03_messages.md:82；script/check_messages.py:42、170–172；script/test/test_check_messages.py:168–173。

2. **位置**：FieldTest.test_message_must_be_english（第 193–195 行）
   **問題**：只測漢字。check_messages.py:62 的 CHINESE 只收 CJK 統一漢字（U+3400–4DBF、4E00–9FFF、F900–FAFF），全形標點（`：`、`，`、`。`，U+3000–303F、FF00–FFEF）不在內，所以 `Try again。` 會通過。維護者要求訊息本文寫英文，理由是避免編碼與相容問題，全形標點一樣有這個問題。check_review_pages 也以第一個非 ASCII 字（含全形標點）當指令的結束點，message 裡混進全形標點會切斷指令。
   **建議**：加一個反例，例如 `message="Could not write <path>。Try again."` 斷言失敗，同時把 check_messages.py:62 的範圍擴到全形標點。要求更嚴的話，直接規定 message 只准 ASCII。
   **證據**：script/check_messages.py:62、183–184；script/README.md:103（「範圍從 `just vendor_kit` 起到第一個非 ASCII 字（中文、全形標點）」）。

3. **位置**：FieldTest.test_placeholder_is_not_html（第 244 行）
   **問題**：例子裡的 `<加上 -y 的原指令>` 是本輪改掉的舊占位符名。good_rows 已改成 `<original command with -y>`，真實 CSV 用的是 `<command_with_y>`。這個例子放在 situation 欄仍然合法，但讀者會以為占位符還是中文名。
   **建議**：改成 `<P> 與 <repo> 與 <command_with_y> 是占位符`。
   **證據**：script/test/test_check_messages.py:24–25、244；doc/contract/03_messages.csv VK0002 列。

4. **位置**：FormatTest.test_strict_parse（第 132 行）
   **問題**：`malformed` 的 9 個值是照欄位順序手排的，`'"a"b'` 要落在 message 欄只能靠人去數。表頭再加欄時，這裡會悄悄對不上。
   **建議**：改用 `row(code="VK0005", status="active", level="warn", exit_code="1", situation="x", description="x")`，並把 message 位置換成 `'"a"b'`。或者在這行加註解，寫明第 7 欄是 message。
   **證據**：script/check_messages.py:35–37；script/test/test_check_messages.py:132。
