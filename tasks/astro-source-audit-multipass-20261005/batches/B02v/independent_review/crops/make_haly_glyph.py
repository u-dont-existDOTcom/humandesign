from PIL import Image,ImageEnhance
from pathlib import Path
b=Path("/home/joel/humandesign-worktrees/astro-lilly-b02v-20261014/tasks/astro-source-audit-multipass-20261005/batches/B02v")
im=Image.open(b/"evidence/pdf-386.png").convert("RGB")
print(im.size)
crop=im.crop((500,1450,1500,1610))
crop=ImageEnhance.Contrast(crop).enhance(1.4)
crop=crop.resize((3000,480),Image.Resampling.LANCZOS)
out=b/"independent_review/crops/haly-leo-glyph-review.png"
crop.save(out)
print(out.stat().st_size)
