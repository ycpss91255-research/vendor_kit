"""粗略渲染 .drawio（方塊 + 線 + 文字前幾行）供自看版面，非正式輸出。用法: rough_render.py <file> <page_id> <out.png> [scale]"""
import sys, re
from PIL import Image, ImageDraw, ImageFont
from drawio_common import load, absbox, vertices, edges
from check_overflow import strip_tags
path, pid, out = sys.argv[1:4]; sc = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 11) if __import__('os').path.exists("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc") else ImageFont.load_default()
for p, name, cells in load(path):
    if p != pid: continue
    W = H = 0
    for c in vertices(cells):
        x, y, w, h = absbox(cells, c['id']); W = max(W, x + w); H = max(H, y + h)
    im = Image.new("RGB", (int((W + 40) * sc), int((H + 40) * sc)), "white"); d = ImageDraw.Draw(im)
    for c in sorted(vertices(cells), key=lambda c: 0 if c['shape'] == 'swimlane' else 1):
        x, y, w, h = absbox(cells, c['id']); st = c['style']
        fill = st.get('fillColor', '#ffffff'); fill = None if fill in ('none',) else fill
        stroke = st.get('strokeColor', '#000'); stroke = '#000' if 'light-dark' in stroke or stroke == 'default' else stroke
        try: d.rectangle([x*sc, y*sc, (x+w)*sc, (y+h)*sc], fill=fill, outline=stroke, width=max(1, int(float(st.get('strokeWidth', 1)) * sc)))
        except Exception: d.rectangle([x*sc, y*sc, (x+w)*sc, (y+h)*sc], outline='#000')
        txt = strip_tags(c['value']).split('\n')[:6]
        for i, t in enumerate(txt): d.text(((x+4)*sc, (y+3+i*13)*sc), t[:60], fill='#000', font=font)
    for ed in edges(cells):
        a = ed['attrs']; st = ed['style']
        if a.get('source') not in cells or a.get('target') not in cells: continue
        sx, sy, sw, sh = absbox(cells, a['source']); tx, ty, tw, th = absbox(cells, a['target'])
        p0 = (sx + float(st.get('exitX', .5))*sw, sy + float(st.get('exitY', .5))*sh)
        p1 = (tx + float(st.get('entryX', .5))*tw, ty + float(st.get('entryY', .5))*th)
        pts = [p0] + ed['points'] + [p1]
        # 無轉折點：以 L 形補正交
        if not ed['points'] and abs(p0[0]-p1[0]) > 1 and abs(p0[1]-p1[1]) > 1:
            if float(st.get('exitY', .5)) in (0, 1): pts = [p0, (p0[0], p1[1]), p1]
            else: pts = [p0, (p1[0], p0[1]), p1]
        d.line([(px*sc, py*sc) for px, py in pts], fill='#c00', width=2)
        d.ellipse([p1[0]*sc-3, p1[1]*sc-3, p1[0]*sc+3, p1[1]*sc+3], fill='#c00')
        lab = strip_tags(ed['value']).split('\n')
        if lab and lab[0]:
            mx, my = pts[len(pts)//2] if len(pts) > 2 else ((p0[0]+p1[0])/2, (p0[1]+p1[1])/2)
            for i, t in enumerate(lab): d.text((mx*sc+3, (my-14+i*12)*sc), t, fill='#0000c0', font=font)
    im.save(out); print(out, im.size)
