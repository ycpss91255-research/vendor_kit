import os; D=os.path.dirname(os.path.abspath(__file__))   # 原本指向 scratchpad
b=open(f"{D}/codex_r9/brief.md").read()
head=b.split("# 附件：決策紀錄（interface_spec.md 全文）")[0]
spec=open(f"{D}/decisions/interface_spec.md").read()
cx=open(f"{D}/codex_r9/compact.xml").read()
note='''# 附件：drawio XML（v2_only.drawio，精簡版）

注意：因輸入長度上限，drawio XML 以精簡格式貼上（內容、id、顏色、字級、連線來源／目標與幾何皆保留，僅移除 whiteSpace／html／align／spacing／strokeWidth／labelBackground 等排版樣板）。格式說明：
- `<page name="頁名">` … `</page>` = 一頁。
- `<c .../>` = 一個 mxCell：`id`、`edge`（有＝線段）、`source`／`target`（線段兩端 id）、`parent`（省略＝根層）、`v`＝顯示文字（含 HTML 實體）、`g="x,y,w,h"`＝幾何、`pts`＝線段路徑點。
- `st` 樣式縮寫：`f`=fillColor、`s`=strokeColor、`fc`=fontColor、`fs`=fontSize（省略＝12）、`b`=fontStyle（1 粗體）、`es`=edgeStyle、`swf`=swimlaneFillColor；其餘（dashed／ellipse／rhombus／shape／swimlane／container／collapsible／startSize／text）原樣保留。

```xml
'''
open(f"{D}/codex_r9/brief2.md","w").write(head+"# 附件：決策紀錄（interface_spec.md 全文）\n\n"+spec+"\n\n---\n\n"+note+cx+"\n```\n")
