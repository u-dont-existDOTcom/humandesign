from PIL import Image,ImageEnhance,ImageFilter
from pathlib import Path
b=Path("/home/joel/humandesign-worktrees/astro-lilly-b02v-20261014/tasks/astro-source-audit-multipass-20261005/batches/B02v")
for name,path,rect in [
 ("errata-p360-single","evidence/errata-888.png",(1000,952,1530,1025)),
 ("body-p360-early","evidence/pdf-394.png",(400,317,1535,432))
]:
 im=Image.open(b/path).convert("RGB").crop(rect)
 im=ImageEnhance.Contrast(im).enhance(1.6)
 im=im.resize((im.width*4,im.height*4),Image.Resampling.LANCZOS)
 dest=b/"independent_review"/"crops"/(name+".png")
 im.save(dest)
 print(name, im.size)
