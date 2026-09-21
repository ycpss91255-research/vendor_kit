"""gen35 → gen36：第 1 頁右欄四條線拉開、標籤縮短"""
src = open("gen35.py").read()
def rep(old, new, count=1):
    global src
    assert src.count(old) == count, (src.count(old), old[:90])
    src = src.replace(old, new)
rep('p1.append(e("a6", "m_list", "m_write", "dist 全部（安裝寫入、verify 比對）", (1, 0.3), (0, 0.232)))', 'p1.append(e("a6", "m_list", "m_write", "dist 全部", (1, 0.3), (0, 0.232)))')
rep('p1.append(v("p_base", "proj", LEAF(), ".<name>/", 56, 300, 88, 40))', 'p1.append(v("p_base", "proj", LEAF(), ".<name>/", 56, 296, 88, 40))')
rep('p1.append(v("p_user", "proj", LEAF(), "使用者檔案", 56, 350, 88, 40))', 'p1.append(v("p_user", "proj", LEAF(), "使用者檔案", 56, 342, 88, 40))')
rep('p1.append(v("p_bl", "proj", LEAF(), "基準\\n（baseline）", 56, 400, 88, 40))', 'p1.append(v("p_bl", "proj", LEAF(), "基準\\n（baseline）", 56, 420, 88, 40))')
rep('p1.append(e("a11", "m_write", "p_base", "dist 全部", (1, 0.318), (0, 0.5), both=True))', 'p1.append(e("a11", "m_write", "p_base", "dist 全部", (1, 0.3), (0, 0.5), both=True))')
rep('p1.append(e("a12", "m_write", "p_user", "初始檔（init 時）", (1, 0.5), (0, 0.25)))', 'p1.append(e("a12", "m_write", "p_user", "初始檔（init 時）", (1, 0.4636), (0, 0.25)))')
rep('p1.append(e("a12b", "p_user", "m_write", "現有內容（diff 時）", (0, 0.76), (1, 0.5927), vert="below"))', 'p1.append(e("a12b", "p_user", "m_write", "現有內容（diff 時）", (0, 0.76), (1, 0.5564), vert="below"))')
rep('p1.append(e("a12c", "m_write", "p_bl", "基準（init／accept 寫，diff 讀）", (1, 0.7727), (0, 0.5), both=True))', 'p1.append(e("a12c", "m_write", "p_bl", "基準（init/accept 寫、diff 讀）", (1, 0.8636), (0, 0.5), both=True))')
rep('p1.append(e("a16", "m_diff", "m_report", "差異、結束狀態", (1, 0.5), (0, 0.5)))', 'p1.append(e("a16", "m_diff", "m_report", "差異、\\n結束狀態", (1, 0.5), (0, 0.5)))')
open("gen36.py", "w").write(src); print("ok")
