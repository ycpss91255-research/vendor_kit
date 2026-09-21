import sys
from PIL import Image
name=sys.argv[1]; n=int(sys.argv[2])
im=Image.open(f'png_v2/{name}.png'); w,h=im.size
for i in range(n):
    y0=max(0,i*h//n-30); y1=min(h,(i+1)*h//n+30)
    im.crop((0,y0,w,y1)).save(f'crops/{name}_{i}.png')
print(w,h)
