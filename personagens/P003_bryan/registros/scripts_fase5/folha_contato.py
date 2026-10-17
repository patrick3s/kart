import sys, os
from PIL import Image, ImageDraw
d, saida, vista = sys.argv[1], sys.argv[2], sys.argv[3]
poses = sys.argv[4].split(",")
cols = 5; w = 260
rows = (len(poses)+cols-1)//cols
img = Image.new("RGB", (cols*w, rows*(w+18)), "white"); dr = ImageDraw.Draw(img)
for i, p in enumerate(poses):
    im = Image.open(f"{d}/{p}__{vista}.png").convert("RGB").resize((w, w))
    x, y = (i%cols)*w, (i//cols)*(w+18)
    img.paste(im, (x, y+18)); dr.text((x+4, y+3), f"{p} {vista}", fill="black")
img.save(saida)
