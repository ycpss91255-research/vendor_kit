已完成，未 commit、未 push、未執行任何 git 寫入指令。

備份：`doc/decisions/_backup/doc_decisions_scope_roadmap.pre_r114.md`

驗證結果：

- `check_terms.py`：OK，掃描 30 個 Markdown 檔
- `check_context.py`：OK，分群 9、名詞 67
- `check_review_pages.py`：OK，掃描 5 個對外文件
- 舊訊息編號殘留檢查：`[]`
- `M1` 獨立出現次數：1

修改清單：

- [doc/decisions/scope_roadmap.md](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/scope_roadmap.md:35)：將訊息代號 `6-3` 改為 `M1`。
- [doc/decisions/scope_roadmap.md](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/scope_roadmap.md:36)：移除未列入新編號對照表的舊訊息引用 `6-21`，保留原有行為敘述。