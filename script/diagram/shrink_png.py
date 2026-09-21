"""三階段 draw.io 審查工具鏈 ─ 第 3 步：縮圖。
用法: python3 shrink_png.py <pngdir> <outdir> [scale=0.5] [page_id ...]
把 <pngdir>/*.png 用 PIL 縮到 scale（預設 50%，LANCZOS），白底保留（RGBA 先貼到白底再轉 RGB），輸出同名到 <outdir>；
另寫 <outdir>/pngs.json = [{page, path}]（page = 檔名去 .png，即頁 id；path 為絕對路徑），可直接當 workflow 的 pngs 參數。
只讀 <pngdir>，不寫回。
"""
import sys, os, glob, json
from PIL import Image

def main():
    if len(sys.argv) < 3: print(__doc__); sys.exit(2)
    src, dst = sys.argv[1], sys.argv[2]
    scale = 0.5; want = set()
    for a in sys.argv[3:]:
        try: scale = float(a)
        except ValueError: want.add(a)
    os.makedirs(dst, exist_ok=True)
    out = []
    for f in sorted(glob.glob(os.path.join(src, '*.png'))):
        page = os.path.splitext(os.path.basename(f))[0]
        if want and page not in want: continue
        im = Image.open(f)
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[-1]); im = bg
        elif im.mode != 'RGB': im = im.convert('RGB')
        w, h = im.size; nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
        im = im.resize((nw, nh), Image.LANCZOS)
        op = os.path.abspath(os.path.join(dst, os.path.basename(f)))
        im.save(op, optimize=True)
        out.append(dict(page=page, path=op))
        print(f"{page:10s} {w}x{h} → {nw}x{nh}  {os.path.getsize(op) // 1024} KB")
    json.dump(out, open(os.path.join(dst, 'pngs.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"共 {len(out)} 張 → {dst}/ （pngs.json 可當 workflow 的 pngs）")

if __name__ == '__main__':
    main()
