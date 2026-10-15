from PIL import Image,ImageEnhance,ImageOps
from pathlib import Path
B=Path("/home/joel/humandesign-worktrees/astro-lilly-b02v-20261014/tasks/astro-source-audit-multipass-20261005/batches/B02v")
image=Image.open(B/"evidence/errata-888.png").convert("RGB")
print("image size",image.size)
dest=B/"independent_review/crops"
dest.mkdir(parents=True,exist_ok=True)
for name,rect in [
 ("errata-p360-full-neighbor",(250,930,1500,1080)),
 ("errata-p360-target",(560,990,1450,1070))
]:
 clip=image.crop(rect)
 clip=ImageEnhance.Contrast(clip).enhance(1.7)
 clip=clip.resize((clip.width*3,clip.height*3),Image.Resampling.LANCZOS)
 clip.save(dest/(name+".png"))
 print(name,clip.size)
