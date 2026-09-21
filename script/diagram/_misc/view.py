"""用法: python3 view.py <pid> [top_frac=0.7] [scale=0.5]  → r14png/<pid>_v.png（白底、裁到流程區、縮圖）"""
import sys
from PIL import Image
pid = sys.argv[1]; frac = float(sys.argv[2]) if len(sys.argv) > 2 else 0.7; sc = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
im = Image.open(f"r14png/{pid}.png").convert("RGBA"); bg = Image.new("RGBA", im.size, "white"); bg.alpha_composite(im); im = bg.convert("RGB")
w, h = im.size; im = im.crop((0, 0, w, int(h * frac))); im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS); im.save(f"r14png/{pid}_v.png"); print(im.size)
