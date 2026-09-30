# r142 審查：script/check_review_pages.py

這一輪 `script/check_review_pages.py` 沒有改（`diff -u doc/decisions/_backup/script_check_review_pages.pre_r142.md script/check_review_pages.py` 無輸出；`git diff HEAD` 也無輸出）。指令掃描欄 `CSV_COMMAND_FIELDS = ("situation", "message", "next_step")`（第 176 行）本來就符合 ask 第 4 點。沒有碰到 #78 的任何定案，也沒有改 01～04 的對外介面。`python3 script/check_review_pages.py` 結果 OK，單元測試全過。

## 必改

1. **位置**：script/check_review_pages.py 第 174 行註解（CMD_CSV 上方）；跨檔 script/README.md 第 103 行
   **問題**：註解寫「從 just vendor_kit 起取到第一個非 ASCII 字（中文、全形標點）或欄尾」。這套切法預設指令後面接中文。`message` 改成英文以後，指令後面的英文句子會一路吃到欄尾，算進指令裡。這一輪的測試就是這樣寫的：script/test/test_check_review_pages.py 斷言的指令是 `just vendor_kit upgrade <repo> -z and retry.`。所以註解與 README 描述的邊界只對 `situation` 還成立，對 `message` 已經過時。內部文件不准留過時資訊（CLAUDE.md「其他都是內部文件…不准留過時的資訊」）。
   **建議**：二選一。(a) 改註解與 script/README.md 第 103 行，寫明 `message` 是英文，指令範圍一路到欄尾，後面的英文句子也會掃；只有 `situation` 會停在第一個中文字。(b) 比較好：收緊 `CMD_CSV`，遇到句讀就停，例如 `just vendor_kit [ -~]*?(?=[;,(]|\.(?:\s|$)|[^ -~]|$)`，再同步改註解、README 與測試斷言（斷言改回 `just vendor_kit upgrade <repo> -z`）。
   **證據**：script/check_review_pages.py:174-175；script/README.md:103；script/test/test_check_review_pages.py（`"03_m.csv:VK0002:message: 指令 \`just vendor_kit upgrade <repo> -z and retry.\` 用了 -z"`）；doc/contract/03_messages.csv:2（VK0001 的 message 在指令後接「 (pulling uses the host's Docker credentials).」）

## 建議

1. **位置**：script/check_review_pages.py 第 184 行 `command_errors` 的選項 regex，搭配第 175 行
   **問題**：英文句子被算進指令後，句子裡任何以 `-`／`--` 開頭的字（例如「-- see docs」、英文說明裡提到的其他旗標）都會被當成選項，要求它在 GLOSSARY.md、01、02 出現過，造成誤報；錯誤訊息裡印出的「指令」也會是整句英文，不好讀。現有 CSV 還沒踩到。
   **建議**：照必改 1(b) 收緊範圍，一起解決。
   **證據**：script/check_review_pages.py:175、184；doc/contract/03_messages.csv:4、5、19、27（英文 message 都在指令後接句尾標點或別的字）

2. **位置**：script/check_review_pages.py 第 176 行 `CSV_COMMAND_FIELDS`
   **問題**：新的 `description` 欄（中文）也寫了完整指令，例如 VK0001「just vendor_kit <command> <repo>@<tag>」、VK0003、VK0004、VK0006、VK0007。ask 指定只掃 situation、message、next_step，所以 description 裡的指令寫法沒人檢查，跟 message 的指令不一致也不會被發現。
   **建議**：維持 ask 的欄位。之後要補的話，在 check_messages.py 加一條「description 裡的 just vendor_kit 指令要跟 message 裡的一致」，不要放進本檔。這一條記進佇列即可，不在這一輪改。
   **證據**：doc/contract/03_messages.csv:2、4、5、11、12（description 欄）
