from pathlib import Path
from PIL import Image,ImageEnhance
b=Path("/home/joel/humandesign-worktrees/astro-lilly-b02v-20261014/tasks/astro-source-audit-multipass-20261005/batches/B02v")
im=Image.open(b/"evidence/pdf-389.png").convert("RGB")
crop=im.crop((115,970,1440,1490))
crop=ImageEnhance.Contrast(crop).enhance(1.35)
crop=crop.resize((2650,1040),Image.Resampling.LANCZOS)
out=b/"independent_review/crops/p389-recovery-alternatives-review.png"
out.parent.mkdir(parents=True,exist_ok=True)
crop.save(out)
print(str(out),out.stat().st_size)
