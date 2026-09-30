## 必改

1. **位置：** [docs/contract/04_interface.md:42](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:42)、[docs/contract/03_messages.md:48](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/03_messages.md:48)

   **問題：** just、Docker、Podman 等主機前置檢查宣稱「在任何寫入之前」結束；但不變量要求「任何副作用之前」先寫執行紀錄，而且執行紀錄不可關閉。首次執行 `bootstrap.sh` 時甚至還沒有安裝目錄，文件沒有說執行紀錄寫在哪裡。兩項承諾目前無法同時成立。

   **建議：** 明定前置檢查是否是「不用執行紀錄」的例外；若不是，就定義首次導入前的紀錄位置與建立時序。不能同時保留現在兩種絕對說法。

   **證據：** [02_invariants.md:99](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:99)、[02_invariants.md:102](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:102)、[ADR-0004:72](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0004-vk-recipe-interface-and-write-boundary.md:72)、[ADR-0007:26](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:26)。

2. **位置：** [docs/contract/04_interface.md:141](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:141)

   **問題：** 「選項照 GNU 慣例」後同時引用 POSIX，會讓人理解成下列規則符合兩者；實際上：

   - `--engine` 有可選參數，違反 POSIX Guideline 7「option-arguments should not be optional」。
   - 選項可放在位置參數前後，違反 POSIX Guideline 9「所有 options 應在 operands 前」。
   - 這兩項是已定案介面，不應改介面，但目前的相容性宣稱不正確。

   **建議：** 改成「採 GNU 式長短選項與 `--`；以下兩點刻意不遵循 POSIX Guideline 7、9」，並直接列出例外。不要籠統聲稱整套「照 GNU／POSIX 慣例」。

   **證據：** [04_interface.md:144](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:144)、[04_interface.md:146](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:146)、[POSIX Utility Syntax Guidelines](https://pubs.opengroup.org/onlinepubs/9699919799.orig/basedefs/V1_chap12.html)。GNU `grep` 也明說其預設會把 operand 後的 option 移到前面，而 POSIX 模式不這樣做，證明這是 GNU 與 POSIX 的實質差異：[GNU grep manual](https://www.gnu.org/software/grep/manual/grep.pdf)。

3. **位置：** [docs/contract/03_messages.md:43](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/03_messages.md:43)

   **問題：** 訊息 6-4 用「`<原指令> -y`」產生可複製指令，不一定是合法命令：

   - 原指令若含 `--`，附加的 `-y` 會變成位置參數。
   - 原始 argv 若含空白、引號、`$`、換行等字元，直接串成字串不能保證可安全複製執行。
   - 這與文件自己承諾的 `--` 語意，以及 ADR 的逐項跳脫規則不一致。

   **建議：** 由 argv 重新序列化命令，依 POSIX shell 安全引用每一項，並把 `--yes` 插在 `--` 之前；不要用字串尾端直接附加 `-y`。

   **證據：** [04_interface.md:145](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:145)、[ADR-0012:33](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0012-deterministic-behavior-and-escaping.md:33)。GNU `diff` 同樣規定 `--` 後全部視為檔名／operand：[GNU Diffutils manual](https://www.gnu.org/software/diffutils/manual/diffutils.html)。

4. **位置：** [docs/contract/04_interface.md:83](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:83)、[docs/contract/04_interface.md:84](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:84)、[docs/contract/04_interface.md:197](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:197)、[README.md:53](/home/cyc/Desktop/vendor-kit_ws/src/README.md:53)

   **問題：** 多處承諾「最新版／新版」，但工具 `<tag>` 沒有格式、可比較順序、pre-release 規則或「最新版」定義。Registry tag 是字串且可被重新指向；只靠版本列舉無法唯一決定哪個是最新版。

   **建議：** 定義工具 tag 的合法格式及排序規則，例如只接受 `vX.Y.Z` 並明定 pre-release 是否參與；或者定義由 registry 的哪個不可歧義資料決定最新版。README 也要沿用同一定義。

   **證據：** [GLOSSARY.md:81](/home/cyc/Desktop/vendor-kit_ws/src/GLOSSARY.md:81)只說 tag 是可重新指向的版本標籤；[01_purpose.md:84](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/01_purpose.md:84)定義 `X.Y.Z` 相容語意，但未把工具 tag 限定成該格式。

5. **位置：** [docs/contract/04_interface.md:200](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:200)

   **問題：** `--timeout` 只有名稱，沒有參數寫法、單位、合法範圍、預設值、適用指令、逾時結束碼及訊息。該頁自稱列出全部選項，但這個選項不足以實作或使用。

   **建議：** 至少定義成明確文法，例如 `--timeout=<秒數>`，並寫清楚適用範圍、零值／負值處理、逾時結果及是否涵蓋拉 image、啟動與引擎執行。

   **證據：** [04_interface.md:3](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:3)、[04_interface.md:135](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:135)。POSIX Guideline 6、7 要求 option argument 的存在與分隔方式明確：[POSIX Utility Syntax Guidelines](https://pubs.opengroup.org/onlinepubs/9699919799.orig/basedefs/V1_chap12.html)。

6. **位置：** [docs/agents/issue-tracker.md:3](/home/cyc/Desktop/vendor-kit_ws/src/docs/agents/issue-tracker.md:3)

   **問題：** 「issue 與 spec 都放在 GitHub」和 repo 已定義的文件分工衝突：對外契約必須放 `docs/contract/`，不能放 issue。`spec` 未限定範圍，agent 很可能把對外規格發成 issue。

   **建議：** 改成「issue 與實作 ticket／issue-level spec 放 GitHub；對外契約只放 `docs/contract/`」，並連到工作約定。

   **證據：** [AGENTS.md:14](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:14)。

7. **位置：** [docs/contract/03_messages.md:18](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/03_messages.md:18)、[docs/contract/04_interface.md:184](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:184)

   **問題：** 現行對外頁已依定案改成 `1`＝有差異／完成後接手、`2`＝失敗或用法錯誤；引用的 ADR 仍大量使用舊碼，形成明確對不齊：

   - 合併衝突仍寫 `2`。
   - 建不出執行紀錄仍寫 `1`。
   - CI 模式拒絕仍寫 `1`。
   - 離線 digest 缺失仍寫 `1`。
   - Podman／低版本檢查仍寫 `1`。

   現行 `update --exit-code` 回 `1`、錯誤回 `2` 本身符合主流慣例：GNU `diff` 是 0＝相同、1＝有差異、2＝錯誤；Git `--exit-code` 沿用 diff；GNU `grep` 也是 0／1 表示查詢結果、2 表示錯誤。[GNU Diffutils](https://www.gnu.org/software/diffutils/manual/diffutils.html)、[git diff](https://git-scm.com/docs/git-diff)、[GNU grep](https://www.gnu.org/s/grep/manual/html_node/Exit-Status.html)。

   **建議：** 不要把 03／04 改回舊碼；在下一個 ADR PR 一次校正所有舊結束碼及舊命令拼法，並以 lint 防止 ADR 再出現舊對應。

   **證據：** [ADR-0003:15](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0003-baseline-merge-and-line-records.md:15)、[ADR-0005:46](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0005-run-log-and-event-registry.md:46)、[ADR-0004:27](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0004-vk-recipe-interface-and-write-boundary.md:27)、[ADR-0009:30](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0009-release-assets-and-offline-import.md:30)、[ADR-0007:23](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:23)。

8. **位置：** [docs/contract/04_interface.md:146](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:146)

   **問題：** 對外頁依定案使用 `upgrade --engine=<tag>`，但 ADR-0008 最新修訂仍使用 `upgrade --engine@<舊 tag>`。這不是單純保留的歷史原文，而是修訂段本身仍給錯誤的現行寫法。

   **建議：** 03／04 維持現在的 `=`；下一個 ADR PR 把 ADR-0008 最新有效修訂改成 `upgrade --engine=<tag>`。

   **證據：** [ADR-0008:85](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:85)。

## 建議

1. **位置：** [docs/contract/04_interface.md:224](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:224)

   **問題：** 「append 型」是會影響檔案所有權、導入與移除行為的核心概念，但 GLOSSARY 沒有定義；第一次看到的人也不知道它是出貨宣告、檔案類型還是合併策略。

   **建議：** 在 GLOSSARY 定義「append 型初始檔」，包含宣告位置、首次導入與移除時的意義；04 只引用定義。

   **證據：** [GLOSSARY.md:147](/home/cyc/Desktop/vendor-kit_ws/src/GLOSSARY.md:147)以下只有初始檔、納管、metadata、基準版與合併衝突；[ADR-0003:59](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0003-baseline-merge-and-line-records.md:59)才出現 `strategy = "append"` 的實際定義。

2. **位置：** [docs/contract/04_interface.md:191](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:191)

   **問題：** `<image>` 可以是已載入 image，也可以是 tar 檔，但沒有說兩者如何辨識；同名路徑與 image reference 衝突時行為不明。

   **建議：** 明定判別規則，或拆成不含糊的寫法，例如檔案明寫 `--image-file <path>`。若介面不改，至少寫清楚優先序與不存在時的錯誤。

   **證據：** [04_interface.md:192](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:192)、[04_interface.md:199](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:199)。

3. **位置：** [docs/contract/04_interface.md:220](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:220)

   **問題：** 第 220～221 行同時解釋所有權、合併保護、手改版本、薄殼處置及例外，句子過長；第一次閱讀很難分辨「檔案位於 `.vendor_kit/`」與「內容歸誰維護」是兩條不同軸線。

   **建議：** 改成小表格：檔案／是否進 git／擁有者／VK 能否重寫／使用者能否手改／改過後處置。

   **證據：** [02_invariants.md:30](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:30)已明確說界線是「內容是誰寫的」，不是目錄。

4. **位置：** [docs/contract/03_messages.md:40](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/03_messages.md:40)

   **問題：** 13 條訊息都塞在寬表格裡，「時機」與「意思」已是完整段落；在窄畫面難讀，而且其他頁只能連到整個「訊息」段，不能直接連到 6-23、6-40 等個別訊息。

   **建議：** 每條訊息改成 `### 訊息 6-23` 之類的標題與欄位清單。這會自然產生 GitHub／GitLab 錨點，不需 `<a>`，也能落實「能直接連到第 N 條就連」的規則。

   **證據：** [04_interface.md:45](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:45)目前「訊息 6-23」只能連到 `#訊息`。

5. **位置：** [docs/agents/issue-tracker.md:3](/home/cyc/Desktop/vendor-kit_ws/src/docs/agents/issue-tracker.md:3)、[AGENTS.md:10](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:10)

   **問題：** 這些路徑以反引號呈現，不是可點擊連結；同一段又是在做文件導覽。

   **建議：** 導覽用途改成有名稱的相對超連結；命令或精確檔名才保留 code span。

   **證據：** 同 repo 的 [GLOSSARY.md:5](/home/cyc/Desktop/vendor-kit_ws/src/GLOSSARY.md:5)已採有名稱超連結。

6. **位置：** [docs/contract/03_messages.md:21](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/03_messages.md:21)

   **問題：** 「做完了，但要人接手」包含 `update --exit-code` 查到新版，但這種結果可能只是 CI 判斷分支，不一定要人接手。結束碼正確，分類名稱偏窄。

   **建議：** 改為「完成，但結果有差異／需後續處理」之類能同時涵蓋合併衝突與版本差異的名稱；不改結束碼。

   **證據：** [04_interface.md:190](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:190)明說此碼也供 CI 或腳本判斷。

本次檢查另確認：

- README 與 01～04 沒有「出處：」行。
- 所有 Markdown 連結都有名稱。
- 本地目標路徑與標題錨點全部存在。
- `check_review_pages.py`、`check_terms.py` 都通過。
- 審查範圍內沒有命中 GLOSSARY 的 `_Avoid_` 詞。
- 未修改任何檔案。