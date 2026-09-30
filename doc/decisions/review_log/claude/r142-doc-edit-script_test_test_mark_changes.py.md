# r142 審查：script/test/test_mark_changes.py

範圍：`diff -u doc/decisions/_backup/script_test_test_mark_changes.pre_r142.md script/test/test_mark_changes.py`（備份檔名沒有 `.py`，任務給的路徑不存在，用這份）。
`python3 -m unittest script/test/test_mark_changes.py`：OK。

## 必改

（無）

逐條對照：本檔是文件工具的測試，不涉 #78 定案（#114、#115、#117、#122、#123）的語意；夾具的 level→exit_code 對應（warn→1、error→2）跟 #117 與 script/check_messages.py:177 的 EXIT_CODES 一致；表頭 script/test/test_mark_changes.py:275 逐字等於 script/check_messages.py:35-37 的 FIELDS 與 doc/contract/03_messages.csv 第 1 行；夾具 VK0001 的 next_step `Rerun <repo>.` 逐字出現在 message 裡（:282），符合 ask 的規則；message 夾具沒有中文字元，description 夾具是中文，符合 script/check_messages.py:181-184。沒有連結、沒有對外頁規則適用。

## 建議

1. 位置：script/test/test_mark_changes.py:383 `test_added_column`（CsvTest）
   問題：這一輪真正送審的遷移是舊表頭 `code,status,level,disposition,situation,message,next_step`（git HEAD 的 doc/contract/03_messages.csv 第 1 行）一次在中間插入 `exit_code` 與 `description` 兩欄；現有測試只驗「尾端少一欄 next_step」。插在中間、一次兩欄、以及 retired 列新欄為空不算改動，都沒有測試守住。
   建議：加一個測試，基準用少了 exit_code 與 description 的 7 欄表頭，斷言兩欄都出現「（本欄新增）」、active 列出現 `exit_code：（空）→ 2`、retired 列不因新增空欄而成段。
   證據：script/test/test_mark_changes.py:383-397；實跑 mark_changes.build 以 HEAD 版 CSV 為基準，輸出第 14-15 行正確標出兩欄新增、VK0001 標 `exit_code：（空）→ 2`——行為對，只是沒測試鎖住。

2. 位置：script/test/test_mark_changes.py:274 註解
   問題：「note、invariant、details 三欄已刪」是舊一輪的歷史，這一輪表頭又多了 exit_code、description，註解只說刪欄、沒說加欄，讀的人會以為表頭只是 7 欄減三欄。另外「照 check_messages.FIELDS」只是註解，沒有斷言，FIELDS 再改時夾具會靜默脫鉤。
   建議：註解改成「表頭照 check_messages.FIELDS」一句即可；另加 `self.assertEqual(self.HEAD.strip().split(","), check_messages.FIELDS)`（或直接用 `",".join(check_messages.FIELDS)` 組 HEAD）。
   證據：script/test/test_mark_changes.py:274-275；script/check_messages.py:35-37。

3. 位置：跨檔觀察（不在本檔，但由本檔的實跑發現）doc/contract/03_messages.csv VK0001、VK0002
   問題：ask 寫「占位符 `<…>` 保留原名」，但 CSV 把 `<指令>` 改成 `<command>`、`<加上 -y 的原指令>` 改成 `<command_with_y>`（situation 與 next_step 也跟著改）；04 仍用 `<指令>`（doc/contract/04_interface.md:70、133、146、151、156）。這跟 ask 另一條「message 不得含中文字元」互相衝突，需由主對話決定占位符是否改名，並讓 03、04、GLOSSARY 一致。
   建議：交主對話定奪；若採英文占位符，04 與 03.md 的佔位符說明一起改，並在回報中明講偏離了 ask 的「保留原名」。
   證據：標示版實跑輸出 VK0001 situation/message、VK0002 next_step `&lt;加上 -y 的原指令&gt; → &lt;command_with_y&gt;`；doc/contract/03_messages.csv 第 2-3 行。
