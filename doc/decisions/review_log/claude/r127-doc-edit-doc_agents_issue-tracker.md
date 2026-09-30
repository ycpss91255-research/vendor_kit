# r127 審查：doc/agents/issue-tracker.md

檢查範圍：已定案（#78 Decisions so far）、對外承諾、ask 做完沒、連結。前兩項沒發現違反；diff 沒有新增或改動連結。

## 必改

1. **位置**：doc/agents/issue-tracker.md:26「慣例」的「關閉」
   - **問題**：`gh issue close ... --comment "..."` 跟新加的第 13 行「不用 `gh issue close --comment`，先留言再關」互相矛盾。內部文件不准留過時的做法。
   - **改法**：改成「先 `gh issue comment <number> -R ycpss91255-research/vendor_kit --body-file <檔>`，再 `gh issue close <number> -R ycpss91255-research/vendor_kit`」。
   - **證據**：doc/agents/issue-tracker.md:13、:26；CLAUDE.md「內部文件…不准留過時的資訊」
2. **位置**：doc/agents/issue-tracker.md:21「慣例」的「建立 issue」
   - **問題**：`--body "..."`、「多行本文用 heredoc」跟第 13 行「`gh issue create` 一律用 `--body-file`，issue 要帶標籤」矛盾。
   - **改法**：改成 `gh issue create -R ycpss91255-research/vendor_kit --title "..." --body-file <檔> --label "..."`，並刪掉 heredoc 那句。
   - **證據**：doc/agents/issue-tracker.md:13、:21
3. **位置**：doc/agents/issue-tracker.md:58 Map 條末的指令
   - **問題**：`gh issue create -R ... --label wayfinder:map` 沒帶 `--body-file`，不符合第 13 行。
   - **改法**：補上 `--title "..." --body-file <檔>`。
   - **證據**：doc/agents/issue-tracker.md:13、:58

## 建議

1. **位置**：doc/agents/issue-tracker.md:61 Frontier query
   - **問題**：還寫著「限定在 map 的 sub-issue／task list 範圍」，但這一輪第 59 行已經拿掉「把 child 加進 map 本文的 task list」，map 本文也不改，task list 已經沒有來源。
   - **建議**：改成「map 的 sub-issue，或本文有 `Part of #<map>`／留言記錄的 child」。
   - **證據**：doc/agents/issue-tracker.md:59、:61；備份 pre_r127 第 53 行
2. **位置**：doc/agents/issue-tracker.md:24、:63 留言指令
   - **問題**：兩處都用 `--body "..."`，沒寫到留言標記。agent 照這兩行抄，發出去的留言會沒有 `[claude]` 開頭，會被 hook 擋。
   - **建議**：範例改成 `--body "[claude] <標題>…"`，或加註「agent 留言第一行要帶標記（見總則）」。
   - **證據**：doc/agents/issue-tracker.md:9、:24、:63
