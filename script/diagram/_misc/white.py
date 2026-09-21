import sys
from PIL import Image
for n in sys.argv[1:]:
    p=f'review/w{n}.png'; im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,'white'); bg.alpha_composite(im); bg.convert('RGB').save(p); print(n, im.size)
