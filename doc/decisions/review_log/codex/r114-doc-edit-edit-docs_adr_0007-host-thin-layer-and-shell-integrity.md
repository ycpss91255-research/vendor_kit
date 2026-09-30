已完成；未 commit、未 push、未執行任何 git 寫入指令。

備份：
`doc/decisions/_backup/docs_adr_0007-host-thin-layer-and-shell-integrity.pre_r114.md`

指定檢查全部通過：

- `check_terms.py`：`OK: 掃 30 個 .md 檔、21 個 _Avoid_ 詞、白名單 0 筆`
- `check_context.py`：`OK: 分群 9、名詞 67、_Avoid_ 詞 21`
- `check_review_pages.py`：`OK: 掃 5 個對外文件`
- 腳本確認舊 `6-N` 殘留：0
- 腳本確認 21 個具名連結及本機目標：全部有效
- 腳本確認成品恰為備份套用指定換號的結果

改動：

- [docs/adr/0007-host-thin-layer-and-shell-integrity.md:16](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:16)：`6-39、6-40` 改為 `M11、M12`。
- [docs/adr/0007-host-thin-layer-and-shell-integrity.md:17](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:17)：`6-23` 改為 `M7`。
- [docs/adr/0007-host-thin-layer-and-shell-integrity.md:19](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:19)：`6-28` 改為 `M8`。
- [docs/adr/0007-host-thin-layer-and-shell-integrity.md:28](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:28)：`6-28` 改為 `M8`。
- [docs/adr/0007-host-thin-layer-and-shell-integrity.md:31](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:31)：`6-36` 改為 `M9`。