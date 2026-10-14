from PIL import Image, ImageEnhance
from pathlib import Path
b=Path("/home/joel/humandesign-worktrees/astro-lilly-b02v-20261014/tasks/astro-source-audit-multipass-20261005/batches/B02v")
for name,part,rect in [
    ("p360-body","evidence/pdf-394.png",(500,325,1440,440)),
    ("p360-erratum","evidence/errata-888.png",(200,875,1550,1035)),
    ("p360-servant","evidence/pdf-394.png",(500,1250,1510,1480)),
]:
    im=Image.open(b/part).convert("RGB").crop(rect)
    im=ImageEnhance.Contrast(im).enhance(1.5)
    im=im.resize((im.width*3,im.height*3),Image.Resampling.LANCZOS)
    out=b/"independent_review"/"crops"/(name+"-review.png")
    im.save(out)
    print(name, im.size, out.stat().st_size)
