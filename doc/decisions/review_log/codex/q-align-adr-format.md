## 結論

要改，但不是把 12 份逐字塞進短模板：先以新版 skill 的三項門檻重審，成立的 ADR 濃縮成「標題＋1～3 句」，必要時才留選填段落；不成立的內容不應繼續冒充 ADR。`> Serves:`、固定六段、修訂段、索引表與自訂 `TEMPLATE.md` 都應退場；決策過程與歷次修訂留在 issue，對外機制進契約，內部機制由程式、schema、測試與架構圖承載。

## 理由

- 這題已由既定原則推出，不需要再問。維護者已決定 repo skill 更新到上游目前版本，而題設又指定「除對外契約外一律對齊 skill」；[#75](https://github.com/ycpss91255-research/vendor_kit/issues/75)正是這項更新。新版 `domain-modeling` 明定：只有「難逆轉、沒有脈絡會令人意外、確實取捨過」三者同時成立才寫 ADR；缺一就跳過。[SKILL.md](</home/cyc/Desktop/vendor-kit_ws/worktree/pr/76/.agents/skills/domain-modeling/SKILL.md:66>)

- 新格式不是「建議可以短一點」，而是明確把正常格式定為標題加 1～3 句，價值在記錄「做了什麼決定、為什麼」，不是填段落；Status、Considered Options、Consequences 也只有真正增加價值時才加入。[ADR-FORMAT.md](</home/cyc/Desktop/vendor-kit_ws/worktree/pr/76/.agents/skills/domain-modeling/ADR-FORMAT.md:7>) 因此現行強制六部分與固定順序直接衝突：[docs/adr/README.md](</home/cyc/Desktop/vendor-kit_ws/src/docs/adr/README.md:13>)；現行 53 行模板則把機制、擁有者、驗收、歷次修訂全部強制放進 ADR：[TEMPLATE.md](</home/cyc/Desktop/vendor-kit_ws/src/docs/adr/TEMPLATE.md:20>)。

- 現有 12 份 ADR 幾乎都自稱「機制決議，不建立不變量」，證明它們大量承擔的是設計規格，而不只是難逆轉取捨。例如 ADR-0003 把逐檔狀態機、metadata、命中次數和結束碼映射都放入 ADR：[0003](</home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0003-baseline-merge-and-line-records.md:17>)；ADR-0008 收納版號觸發清單、TOML 欄位、未知欄位和遷移規則：[0008](</home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:17>)。這正是應拆分內容歸屬，而非只改標題層級。

- `> Serves:` 是 repo 自訂的必填追蹤機制：[AGENTS.md](</home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:22>)；新版格式沒有它，而且契約已經反向列出每條不變量由哪些 ADR 建立或服務，例如不變量 1 的列表：[02_invariants.md](</home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:53>)。同一關係同時維護 `Serves`、契約清單及 README 索引，違反「一個概念一種寫法」；這是推論，但有現存三重來源為證：[ADR 索引表](</home/cyc/Desktop/vendor-kit_ws/src/docs/adr/README.md:37>)。

- 詳細決策紀錄應回到 issue。repo 的 issue 約定已明定「設計決議寫進 issue 本文」，留言只保存討論過程：[issue-tracker.md](</home/cyc/Desktop/vendor-kit_ws/src/docs/agents/issue-tracker.md:18>)。實例上，#65 的 issue 本文與維護者留言已保存介面改寫及追加決議；[#71](https://github.com/ycpss91255-research/vendor_kit/issues/71)也完整保存 U1～U6、Git 與 `check.sh` 的決策。ADR 只需留下將來讀程式碼時仍不可見的決定與理由，必要時在正文自然連回 issue，不另造 `Related` 欄位。

- 機制細節的歸屬可由既定文件邊界推出：

  - 使用者可觀察、將來手冊必須承諾的行為，放 `docs/contract/01～04`；例如 GNU 選項、指令寫法已放在介面頁：[04_interface.md](</home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:128>)。
  - 永遠必須成立的性質放 `02_invariants.md`，但不放實現方式；該頁自己明說只寫概念：[02_invariants.md](</home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:3>)。
  - 內部流程、資料格式、狀態機、擁有模組與驗證方式，實作後由程式碼、schema／設定、測試及受 lint 約束的架構圖表達；尚未實作的工作內容留在 issue。這一點是依「決策紀錄在 issue」「架構圖是測試依據」和新版 ADR 邊界作出的推論：[AGENTS.md](</home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:25>)。
  - 若某項「機制」本身就是難逆轉且令人意外的架構選擇，例如「工具 image 只搬不執行」，它就是決定本身，ADR 留一句選擇與理由；`docker create/cp` 的完整步驟、三層驗證等細節則不留在 ADR。新版格式也把 architectural shape、integration pattern 與 deliberate deviation 列為合格例子：[ADR-FORMAT.md](</home/cyc/Desktop/vendor-kit_ws/worktree/pr/76/.agents/skills/domain-modeling/ADR-FORMAT.md:39>)。

## 風險或反例

- 不能一次把 12 份機械式縮短後就刪掉原文。部分細節目前可能尚未落進契約、issue、程式或測試；若先刪，會造成唯一規格來源消失。遷移前應逐條建立「ADR 段落 → issue／契約／程式／測試／刪除」對照；這是遷移安全措施，不是新的永久文件格式。

- ADR-0001 的替代方案比較可能值得保留 `Considered Options`，因為重複提出 vendir、Copier 等方案的機率高；新版格式本來就允許在拒絕理由值得記住時保留該選填段落。[ADR-FORMAT.md](</home/cyc/Desktop/vendor-kit_ws/worktree/pr/76/.agents/skills/domain-modeling/ADR-FORMAT.md:17>) 因此「改新版格式」不等於強迫每份只剩三句。

- `README.md` 若只剩目錄導覽可以存在，但不應再維護手寫 ADR 索引、另一套格式規則或待拍板清單；檔案系統本身已被定為登錄，手寫表會形成第二來源。[docs/adr/README.md](</home/cyc/Desktop/vendor-kit_ws/src/docs/adr/README.md:5>) 這是依「一個概念一種寫法」作出的推論。

`ask_user:`