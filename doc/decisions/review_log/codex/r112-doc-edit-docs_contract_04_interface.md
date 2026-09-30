## 必改

- **位置：** `docs/contract/04_interface.md:42-46`  
  **問題：** 把所有版本不足都寫成「結束碼 `2`」，並稱 just 版本不足會印訊息 6-23；這只適用首次導入。已有安裝目錄時，低版本 just 會在解析 justfile 時自行失敗，VK 啟動器不會執行，因此不保證 VK 的結束碼、訊息 6-23 或執行紀錄。  
  **建議：** 將「版本不足時」拆成首次導入與已有安裝目錄兩種情況；只對 `bootstrap.sh` 承諾訊息 6-23 與結束碼 `2`。Docker／Podman 檢查則可保留兩種情況均由啟動器處理的說法。  
  **證據：** `docs/adr/0007-host-thin-layer-and-shell-integrity.md:15,22`；`docs/contract/03_messages.md:58` 明定 6-23 的觸發者是 `bootstrap.sh`。

- **位置：** `docs/contract/04_interface.md:143-145`、`docs/contract/04_interface.md:259-260`  
  **問題：** 長短選項清單把「只有長」列成 `--engine`、`--exit-code`，漏掉同頁定義的 `--dist`。以目前「具體寫法」的語氣，清單看起來是完整清單，造成介面規格自相矛盾，也違反介面寫法一致的不變量。  
  **建議：** 把 `--dist` 加進「只有長」清單，或明說該清單只適用 `just vendor_kit`、另列 CI 腳本選項。  
  **證據：** `docs/contract/04_interface.md:145,260`；`docs/contract/02_invariants.md:150-158`。

## 建議

- **位置：** `docs/contract/04_interface.md:79`  
  **問題：** 用法摘要只呈現 `[參數] [選項]`，但後文允許選項放在位置參數之前或之後。第一次閱讀會把摘要理解成只能後置。  
  **建議：** 改成不暗示固定順序的摘要，或並列兩種順序。  
  **證據：** `docs/contract/04_interface.md:143,146`；POSIX 的通常順序是選項在 operand 前，而本頁刻意放寬，因此更需要在摘要表達清楚：[POSIX Utility Syntax Guidelines](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html)、[Git CLI conventions](https://git-scm.com/docs/gitcli)。

- **位置：** `docs/contract/04_interface.md:86-87,174,178,195-196`  
  **問題：** 第 144 行承諾 `-y`／`--yes`、`-i`／`--image`、`-p`／`--path` 等價，但所有具體用法只展示短式；尤其 `bootstrap.sh -i` 會讓人不確定 `bootstrap.sh --image` 是否也屬契約。  
  **建議：** 第一次展示時並列長短式，或明說後文一律以短式代表兩者。  
  **證據：** `docs/contract/04_interface.md:144`；GNU 慣例會並列等價的短、長選項：[GNU diff options](https://www.gnu.org/software/diffutils/manual/html_node/Invoking-diff.html)。

- **位置：** `docs/contract/04_interface.md:135`  
  **問題：** 沒有頂層 `--version` 偏離 GNU 通用 CLI 慣例；文件雖已說明 just 路由限制，但沒有明確告訴腳本使用者目前怎麼取得版本。裸呼叫雖會印版本，卻走 stderr 並回 `2`。  
  **建議：** 明說目前唯一可觀察方式及其 stderr／結束碼行為；若不打算把它當機器介面，也應明說。  
  **證據：** `docs/contract/04_interface.md:134-135`；[GNU Command-Line Interfaces](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html)。

- **位置：** `docs/contract/04_interface.md:48-50`、`docs/contract/04_interface.md:37`  
  **問題：** `registry`、`repo`、`安裝目錄` 都是 GLOSSARY 專有名詞，但首次出現沒有依對外頁慣例標底線；`repo` 到第 71 行才標示，`registry` 與 `安裝目錄` 在本頁未於首次出現標示。沒有使用 `_Avoid_` 詞，但專有名詞標示不一致。  
  **建議：** 在首次正文出現處標示；標題中的 `registry` 是否算首次出現也應採一致規則。  
  **證據：** `docs/contract/01_purpose.md:3`；`GLOSSARY.md:38-40,49-51,75-76`。

- **位置：** `docs/contract/04_interface.md:198`  
  **問題：** 「image tar 檔」沒有說是哪種可接受格式。第一次閱讀無法判斷是 `docker save` 產物、OCI archive，還是任意包含 image 的 tar。  
  **建議：** 指名格式或產生它的既有命令。  
  **證據：** `GLOSSARY.md:68-86` 只定義工具 image、引擎 image、image 引用、tag 與 digest，沒有定義 image tar。