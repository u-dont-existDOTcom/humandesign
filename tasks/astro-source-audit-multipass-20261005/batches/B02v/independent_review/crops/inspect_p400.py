from pathlib import Path
from PIL import Image, ImageEnhance
b=Path("/home/joel/humandesign-worktrees/astro-lilly-b02v-20261014/tasks/astro-source-audit-multipass-20261005/batches/B02v")
im=Image.open(b/"evidence/pdf-400.png").convert("RGB")
print("original", im.size)
out=b/"independent_review/crops"
out.mkdir(parents=True,exist_ok=True)
for name, rect in [
 ("p400-last-capture",(550,1100,1460,1320)),
 ("p400-early-capture",(560,930,1510,1180)),
 ("p400-restitution",(520,360,1500,820))
]:
 clip=im.crop(rect)
 clip=clip.resize((clip.width*3,clip.height*3),Image.Resampling.LANCZOS)
 clip=ImageEnhance.Contrast(clip).enhance(1.35)
 clip.save(out/(name+".png"))
 print(name,clip.size)
