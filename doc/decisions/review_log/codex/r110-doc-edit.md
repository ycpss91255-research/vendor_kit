## 必改

1. **位置：** [docs/adr/0001-why-not-existing-tools.md:20](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0001-why-not-existing-tools.md:20)  
   **問題：** 把 `git submodule` 和 `git subtree` 一起描述成「工具的 commit 與使用者的 commit 混在一起」，但同檔表格第 10 行正確寫的是 submodule 只有 gitlink 進入上層 repo 歷史。前後自相矛盾。  
   **建議：** 拆開描述：`subtree` 會把 commit 合入使用者 repo；`submodule` 不會，但引入額外 repo、初始化與更新狀態。  
   **證據：** [同檔表格:9-10](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0001-why-not-existing-tools.md:9)。

2. **位置：** [docs/adr/0001-why-not-existing-tools.md:37](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0001-why-not-existing-tools.md:37)  
   **問題：** 「兩邊要改，以本檔為準」把 ADR 放在對外契約之上；但 repo 已明定 `docs/contract/` 是對外契約的權威位置，ADR 只記決定與理由。兩邊若衝突，不能由 ADR 單方面覆蓋契約。  
   **建議：** 改成「01 留對外結論，本 ADR 留完整取捨；承諾改變時先依契約審閱流程修改契約」。  
   **證據：** [AGENTS.md:14](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:14)、[AGENTS.md:23](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:23)、[doc/decisions/README.md:15](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:15)。

3. **位置：** ADR-0002～0012 各檔的「內部機制（之後搬到實作 issue）」段，例如 [ADR-0002:19](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0002-vendor-kit-dir-layout-and-lock-line-form.md:19)、[ADR-0004:20](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0004-vk-recipe-interface-and-write-boundary.md:20)、[ADR-0012:19](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0012-deterministic-behavior-and-escaping.md:19)  
   **問題：** 已定案第 20 條明定「機制細節：使用者看得到的在 03／04，內部機制放 issue」，但十一份 ADR 仍整段保留待搬的實作細節。「之後搬」也是已過時的流程描述。  
   **建議：** ADR 只留難逆轉的決定、理由、被拒方案及非顯然後果；純檔名、欄位、時序、實作清單移到對應 issue。  
   **證據：** [discussion_queue.md:38](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review_log/discussion_queue.md:38)、[AGENTS.md:21-23](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:21)。

4. **位置：** [docs/adr/0004-vk-recipe-interface-and-write-boundary.md:19](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0004-vk-recipe-interface-and-write-boundary.md:19)  
   **問題：** 說薄殼不符的訊息編號「還沒列，記在 Q8」，但 03 已列出 6-28。這是過時事實。  
   **建議：** 改為直接連結訊息 6-28；不要再說尚未列出。  
   **證據：** [docs/contract/03_messages.md:49](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/03_messages.md:49)。

5. **位置：** [docs/adr/0006-tool-image-as-data-only.md:16](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0006-tool-image-as-data-only.md:16)  
   **問題：** 「`docker pull` 成功的機器上取件就會成功」是無條件 registry 承諾；已定案第 16 條及不變量 2 均把它限縮為「在支援的 registry 上」。  
   **建議：** 補上「在支援的 registry 上」及「支援範圍由驗收決定」。  
   **證據：** [discussion_queue.md:31](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review_log/discussion_queue.md:31)、[docs/contract/02_invariants.md:70](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:70)。

6. **位置：** [docs/adr/0007-host-thin-layer-and-shell-integrity.md:15](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:15)、[同檔:22](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:22)  
   **問題：** Docker／just 版本不足被描述為「第一次／任何寫入之前」停止，等於沒有先寫執行紀錄；不變量 4 卻要求執行紀錄早於任何副作用，且執行紀錄不可關閉。這項衝突目前仍明列在 Q12，不能在 ADR 中寫成已閉合機制。  
   **建議：** 在 Q12 定案前明標未決邊界；定案後同步統一 ADR-0004、0005、0007 與訊息 6-23／6-39／6-40。  
   **證據：** [docs/contract/02_invariants.md:99-102](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:99)、[ADR-0004:26](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0004-vk-recipe-interface-and-write-boundary.md:26)、[ADR-0005:23](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0005-run-log-and-event-registry.md:23)、[discussion_queue.md:107-111](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review_log/discussion_queue.md:107)。

7. **位置：** [docs/adr/0007-host-thin-layer-and-shell-integrity.md:30](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:30)  
   **問題：** 版本組合不合時，多數 recipe 的 `-h`／`--help` 回 `3`，直接違反 04「每個指令的 help 都回 0」；ADR 也沒有交代為何純說明查詢必須受版本相容性阻擋。GNU 與 Python argparse 的慣例都是 help 顯示後成功退出。  
   **建議：** 所有薄殼能辨識的 recipe help 都應維持 stdout＋`0`；若技術上確實做不到，須寫明理由並同步限縮 04 的無條件承諾。  
   **證據：** [docs/contract/04_interface.md:133](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:133)、[GNU `--help` 慣例](https://www.gnu.org/prep/standards/html_node/_002d_002dhelp.html)、[Python argparse](https://docs.python.org/3/library/argparse.html#add-help)。

8. **位置：** [docs/adr/0007-host-thin-layer-and-shell-integrity.md:30](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:30)、[docs/contract/04_interface.md:133-136](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:133)  
   **問題：** 沒有成功的頂層 `just vendor_kit -h`／`--help` 形狀；裸呼叫又是用法錯誤。這使入口只能靠「故意犯錯」取得總用法，且沒有說明偏離主流 CLI 慣例的理由。  
   **建議：** 明定 `just vendor_kit -h`／`--help` 為 stdout＋`0` 的救援路徑；裸呼叫維持 stderr＋`2` 可以成立。  
   **證據：** [GNU CLI standards](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html)、[Python argparse: invalid arguments use stderr and status 2](https://docs.python.org/3/library/argparse.html#exit-on-error)。

9. **位置：** [docs/adr/0008-protocol-and-file-schema-versions.md:3](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:3)、[同檔:21](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:21)、[同檔:26](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:26)  
   **問題：** 第 3 行斷言版本組合能在拉 image、起容器前判定；第 21 行卻承認本機沒有 image 時所需資料及其擁有者尚未決定。決定段把未閉合機制寫成已成立。  
   **建議：** 在 Q5 定案前明確標出 ADR 尚未證成離線判定機制；定案後再補足資料來源及核對責任。  
   **證據：** [docs/contract/02_invariants.md:180-190](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:180)、[discussion_queue.md:129-134](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review_log/discussion_queue.md:129)。

10. **位置：** [doc/decisions/README.md:24-25](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:24)、[同檔:76-82](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:76)  
    **問題：** 仍把「設計原則併入 ADR」寫成待處理事項，並要求待拍板項目使用已刪除的 `needs-decision` 標籤。現況地圖與已定案狀態、現行 triage 詞彙不一致。  
    **建議：** 更新為目前定案後的真實狀態；需要維護者拍板的一律用 `needs-triage`。  
    **證據：** [discussion_queue.md:38-39](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review_log/discussion_queue.md:38)、[AGENTS.md:7](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:7)。

## 建議

1. **位置：** `docs/adr/TEMPLATE.md`  
   **問題：** 檔案不存在，因此無內容可審；但這不是 repo 缺件，而是已定案第 20 條要求移除 TEMPLATE。  
   **建議：** 從後續審查清單移除，不要復原該檔。  
   **證據：** [discussion_queue.md:38](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review_log/discussion_queue.md:38)、[ADR 格式](/home/cyc/Desktop/vendor-kit_ws/src/.agents/skills/domain-modeling/ADR-FORMAT.md:7)。

2. **位置：** 多數 ADR 第 3 行，例如 [ADR-0001:3](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0001-why-not-existing-tools.md:3)、[ADR-0008:3](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:3)  
   **問題：** 單句以多個分號同時承擔背景、決定、理由及實作，第一次閱讀很難辨認哪部分是正式決定。  
   **建議：** 拆成 2～3 句：背景、決定、理由各自一件事。ADR-0008 尤其應分開 release 版、介面版及檔案版三層。  
   **證據：** [ADR-FORMAT.md:10-15](/home/cyc/Desktop/vendor-kit_ws/src/.agents/skills/domain-modeling/ADR-FORMAT.md:10)。

3. **位置：** [docs/adr/0005-run-log-and-event-registry.md:3](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0005-run-log-and-event-registry.md:3)、[同檔:15](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0005-run-log-and-event-registry.md:15)  
   **問題：** 拒絕 stdout 機器格式的理由完整，但沒有交代呼叫端如何無歧義找到「本次」JSONL 紀錄；併發執行時尤其不清楚。  
   **建議：** 補上本次紀錄的穩定定位方式，否則「執行紀錄可取代 porcelain」的前提不完整。  
   **證據：** Git 的 porcelain 格式刻意保證可供腳本穩定解析：[git-status porcelain](https://git-scm.com/docs/git-status#_porcelain_format_version_1)。

4. **位置：** [docs/adr/0008-protocol-and-file-schema-versions.md:25](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:25)  
   **問題：** 「新增選項」一律令 P+1 過寬；純新增且舊薄殼不需理解的選項，通常不構成 CLI 不相容。  
   **建議：** 收窄為「新增需要舊薄殼辨識、驗證或改變轉送語意的選項」。  
   **證據：** [GNU CLI standards](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html)。

5. **位置：** [docs/adr/0012-deterministic-behavior-and-escaping.md:22](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0012-deterministic-behavior-and-escaping.md:22)  
   **問題：** 「路徑一律加引號」「自由文字用八進位跳脫」沒有說是哪一層文法、哪些位元組被跳脫、接收端如何定界與解碼；這不足以讓兩端獨立實作出相同結果。  
   **建議：** 指定完整 wire grammar，或只在 ADR 記「使用無歧義、可逆的編碼」，把精確文法放進實作 issue。  
   **證據：** [ADR-0005:3](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0005-run-log-and-event-registry.md:3) 已把 `vk-resolve/<P>` 稱為正式文法。

6. **位置：** 全部受審現存檔案  
   **問題：** 未發現失效的 Markdown 本地路徑或錨點；連結都有可見名稱。README 與對外頁 01～04 也沒有「出處：」行。`check_terms.py` 與 `check_review_pages.py` 均通過。歷史段落出現「專案根」「導入根」「動詞」時，都明確標為舊名，不是現行名詞誤用。  
   **建議：** 這幾項不需修改；避免把歷史引用或真正的 cryptographic signature 誤判成 `_Avoid_` 詞誤用。  
   **證據：** [GLOSSARY.md:16-20](/home/cyc/Desktop/vendor-kit_ws/src/GLOSSARY.md:16)、[GLOSSARY.md:49-51](/home/cyc/Desktop/vendor-kit_ws/src/GLOSSARY.md:49)、[doc/decisions/README.md:42](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:42)。

其餘 CLI 決定中，合併衝突及 `update --exit-code` 回 `1`、一般失敗與用法錯誤回 `2`、help/version 用 stdout、診斷用 stderr、`--` 結束選項、GNU 式選項前後混排，都符合或已明確說明偏離主流慣例，不列問題。相關依據：[GNU diff3](https://www.gnu.org/software/diffutils/manual/html_node/Invoking-diff3.html)、[GNU grep exit status](https://www.gnu.org/software/grep/manual/html_node/Exit-Status.html)、[git diff `--exit-code`](https://git-scm.com/docs/git-diff#Documentation/git-diff.txt---exit-code)、[POSIX Utility Syntax Guidelines](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html)。