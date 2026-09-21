s = open("gen7.py", encoding="utf-8").read()

# 1) e() 支援 vert（標籤放直線右側）與 pos（標籤沿線位置）
old_e = s[s.index("def e(id, src, tgt"):s.index("def page(")]
new_e = '''def e(id, src, tgt, label="", exit=None, entry=None, dashed=False, both=False, vert=False, pos=None):
    st = EDGE
    if exit:  st += f"exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;"
    if entry: st += f"entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
    if dashed: st += "dashed=1;"
    if both: st += "startArrow=block;startFill=1;"
    if vert: st += "align=left;verticalAlign=middle;spacingLeft=6;spacingBottom=0;"
    geo = '<mxGeometry relative="1" as="geometry"/>' if pos is None else f'<mxGeometry x="{pos}" relative="1" as="geometry"/>'
    return (f'<mxCell id="{id}" value="{esc(label)}" style="{st}" edge="1" parent="1" source="{src}" target="{tgt}">'
            f'{geo}</mxCell>')

'''
s = s.replace(old_e, new_e)

R = {
 # ---- 頁 1 直線標籤 ----
 'p1.append(e("a2", "m_cli", "m_list", "命令參數", (0.5, 1), (0.5, 0)))': 'p1.append(e("a2", "m_cli", "m_list", "命令參數", (0.5, 1), (0.5, 0), vert=True))',
 'p1.append(e("a7", "m_list", "m_tpl", "初始檔清單", (0.5, 1), (0.5, 0)))': 'p1.append(e("a7", "m_list", "m_tpl", "初始檔／選用檔清單、模板", (0.5, 1), (0.5, 0), vert=True))',
 'p1.append(e("a9", "m_write", "m_stamp", "檔案內容／指紋", (0.8, 1), (0.64, 0), both=True))': 'p1.append(e("a9", "m_write", "m_stamp", "內容、既有印記 ⇄ 新指紋", (0.8, 1), (0.64, 0), both=True, vert=True))',
 'p1.append(e("a14", "m_tpl", "m_diff", "新版模板", (0.5, 1), (0.5, 0)))': 'p1.append(e("a14", "m_tpl", "m_diff", "新版模板", (0.5, 1), (0.5, 0), vert=True))',
 'p1.append(e("a15", "m_stamp", "m_report", "檢查結果", (0.5, 1), (0.77, 0)))': 'p1.append(e("a15", "m_stamp", "m_report", "檢查結果", (0.5, 1), (0.77, 0), vert=True))',
 '<mxCell id="a13" value="使用者檔案" style="\' + EDGE + \'exitX=0.35;exitY=1;exitDx=0;exitDy=0;entryX=0.9;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="m_write" target="m_diff"><mxGeometry relative="1" as="geometry">':
 '<mxCell id="a13" value="使用者檔案" style="\' + EDGE + \'exitX=0.35;exitY=1;exitDx=0;exitDy=0;entryX=0.9;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="m_write" target="m_diff"><mxGeometry x="0.55" relative="1" as="geometry">',
 # ---- 頁 2 ----
 'p1b.append(v("other", "1", SW(RED), "其他工具", 40, 540, 240, 130))': 'p1b.append(v("other", "1", SW(GREEN), "其他工具", 40, 540, 240, 130))',
 'p1b.append(v("ds", "1", SW(RED), "使用 base 的專案", 700, 80, 720, 380))': 'p1b.append(v("ds", "1", SW(GREEN), "使用 base 的專案", 700, 80, 720, 380))',
 'p1b.append(v("g_other", "ghcr", PURPLE_LEAF, "其他工具-dist:vY", 30, 520, 200, 40))': 'p1b.append(v("g_other", "ghcr", PURPLE_LEAF, "其他工具-dist:vY", 30, 520, 200, 40))\np1b.append(v("g_t", "ghcr", TEXT(11), "tag 不覆蓋；image 附註版本與來源 commit；\\n舊版保留策略待定", 10, 40, 240, 40))',
 'p1b.append(v("sa", "ds", SW(RED), "啟動器", 20, 50, 200, 100))': 'p1b.append(v("sa", "ds", SW(RED), "啟動器", 20, 50, 200, 115))\np1b.append(v("sa_t", "sa", TEXT(11), "契約版本與更新方式：待設計", 12, 90, 180, 18))',
 'p1b.append(v("ds_engine", "ds", PURPLE_LEAF, "安裝容器（base-dist:vX）", 20, 170, 200, 60))': 'p1b.append(v("ds_engine", "ds", PURPLE_LEAF, "安裝容器（base-dist:vX）", 20, 185, 200, 60))',
 'p1b.append(v("ds_t", "ds", TEXT(11), "以使用者身分執行，跑完即刪", 20, 232, 200, 20))': 'p1b.append(v("ds_t", "ds", TEXT(11), "以使用者身分執行，跑完即刪", 20, 247, 200, 20))',
 'p1b.append(v("sb", "ds", SW(RED), "使用者檔案", 260, 260, 200, 110))': 'p1b.append(v("sb", "ds", SW(RED), "使用者檔案", 260, 265, 200, 100))',
 'p1b.append(v("sc", "ds", SW(RED), ".base/", 500, 260, 200, 110))': 'p1b.append(v("sc", "ds", SW(RED), ".base/", 500, 265, 200, 100))',
 'p1b.append(e("b4", "g_vk", "g_base", "基底 image", (0.5, 0), (0.5, 1), dashed=True))': 'p1b.append(e("b4", "g_vk", "g_base", "基底 image", (0.5, 0), (0.5, 1), dashed=True, vert=True))',
 'p1b.append(e("b5", "g_vk", "g_other", "基底 image", (0.5, 1), (0.5, 0), dashed=True))': 'p1b.append(e("b5", "g_vk", "g_other", "基底 image", (0.5, 1), (0.5, 0), dashed=True, vert=True))',
 'p1b.append(e("b8", "c_just", "ds_engine", "版本、身分、路徑", (0.5, 1), (0.74, 0)))': 'p1b.append(e("b8", "c_just", "ds_engine", "版本、使用者身分、專案路徑", (0.5, 1), (0.74, 0), vert=True))',
 'p1b.append(e("b9", "ds_engine", "sc", "工具檔、印記檔", (1, 0.7), (0.5, 0), both=True))': 'p1b.append(e("b9", "ds_engine", "sc", "工具檔、印記檔", (1, 0.3), (0.5, 0), both=True))',
 'p1b.append(e("b10", "ds_engine", "sb", "初始檔", (1, 0.3), (0.5, 0), dashed=True))': 'p1b.append(e("b10", "ds_engine", "sb", "初始檔", (1, 0.7), (0.5, 0), dashed=True))',
 # ---- 頁 3 ----
 'p2.append(e("c20", "c6", "c8", "已下載", (0.5, 1), (0.5, 0)))': 'p2.append(e("c20", "c6", "c8", "已下載", (0.5, 1), (0.5, 0), vert=True))',
 'p2.append(e("c22", "c8", "c9", "不一致或尚未安裝", (1, 0.5), (0, 0.5)))': 'p2.append(e("c22", "c8", "c9", "不一致、尚未安裝或印記不可讀", (1, 0.5), (0, 0.5)))',
 'p2.append(e("c23", "c8", "c12", "一致", (0.5, 1), (0.5, 0)))': 'p2.append(e("c23", "c8", "c12", "一致", (0.5, 1), (0.5, 0), vert=True))',
 'p2.append(e("c24", "c9", "c15", "安裝完成", (0.5, 1), (1, 0.5)))': 'p2.append(e("c24", "c9", "c15", "安裝完成（剛寫入，不再 verify）", (0.5, 1), (1, 0.5)))',
 'p2.append(e("c30", "c13", "c15", "完整", (0.5, 1), (0.5, 0)))': 'p2.append(e("c30", "c13", "c15", "完整", (0.5, 1), (0.5, 0), vert=True))',
 # ---- 頁 4 ----
 'p3.append(e("c14", "c8", "c9", "是", (0.5, 1), (0.5, 0)))': 'p3.append(e("c14", "c8", "c9", "有", (0.5, 1), (0.5, 0), vert=True))',
 '<mxCell id="c14b" value="否"': '<mxCell id="c14b" value="無"',
 # ---- 頁 5 ----
 '"流程：安裝工具（vendor_kit）三個子命令"': '"流程：安裝工具（vendor_kit）三個子命令 — 全部在安裝容器內執行"',
 'p4.append(e("le2", "l9", "l2", "有", (0.5, 1), (0.5, 0)))': 'p4.append(e("le2", "l9", "l2", "有", (0.5, 1), (0.5, 0), vert=True))',
 'p4.append(e("le4", "l3", "l5", "初始檔", (0.5, 1), (0.5, 0)))': 'p4.append(e("le4", "l3", "l5", "初始檔", (0.5, 1), (0.5, 0), vert=True))',
 'p4.append(e("le6", "l5", "l7", "沒有", (1, 0.5), (0.5, 0)))': 'p4.append(e("le6", "l5", "l7", "沒有", (1, 0.5), (0.5, 0), vert=True))',
 'p4.append(e("le7", "l5", "l8", "已有", (0.5, 1), (0.5, 0)))': 'p4.append(e("le7", "l5", "l8", "已有", (0.5, 1), (0.5, 0), vert=True))',
 'p4.append(e("le6b", "l6", "l6b", "有", (0.5, 1), (0.5, 0)))': 'p4.append(e("le6b", "l6", "l6b", "有", (0.5, 1), (0.5, 0), vert=True))',
 'p4.append(v("l6b", "land", LEAF(), "用模板建立", 470, 650, 150, 40))': 'p4.append(v("l6b", "land", LEAF(), "缺少才建立\\n（已有則保留）", 470, 645, 150, 50))',
 'p4.append(e("ve3", "v3", "v4", "是", (0, 0.5), (0.5, 0)))': 'p4.append(e("ve3", "v3", "v4", "是", (0, 0.5), (0.5, 0), vert=True))',
 'p4.append(e("ve4", "v3", "v5", "否", (1, 0.5), (0.5, 0)))': 'p4.append(e("ve4", "v3", "v5", "否", (1, 0.5), (0.5, 0), vert=True))',
 'p4.append(e("de3", "d3", "d4", "否", (0, 0.5), (0.5, 0)))': 'p4.append(e("de3", "d3", "d4", "否", (0, 0.5), (0.5, 0), vert=True))',
 'p4.append(e("de4", "d3", "d5", "是", (1, 0.5), (0.5, 0)))': 'p4.append(e("de4", "d3", "d5", "是", (1, 0.5), (0.5, 0), vert=True))',
 # ---- 頁 6 ----
 '("印記檔", "安裝時寫下的紀錄：版本 + 每個檔案的指紋")': '("印記檔", "安裝時寫下的紀錄：版本 + 每個工具檔的指紋（不含使用者檔案）")',
}
for k, val in R.items():
    assert s.count(k) == 1, (k, s.count(k))
    s = s.replace(k, val)
# 頁 2 圖例：綠含「既有專案」
s = s.replace('("綠：現有模組（本體不變）", GREEN)', '("綠：現有模組（本體不變）", GREEN)')
open("gen8.py", "w", encoding="utf-8").write(s)
print("ok")
