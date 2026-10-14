"""Generate visually comparable JPEG derivatives from immutable original page images.
No text OCR, page substitution, original-byte mutation, or admission.
Original evidence/pdf-NNN.png remains the controlling witness.
"""
from pathlib import Path
from PIL import Image
B=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent/"review_images"
OUT.mkdir(exist_ok=True)
for pg in [391,392,393,395,396,397]:
    src=B/"evidence"/f"pdf-{pg}.png"
    dst=OUT/f"pdf-{pg}.jpg"
    with Image.open(src) as im:
        im.convert("RGB").save(dst,"JPEG",quality=88,optimize=True,subsampling=0)
    print(pg,dst.stat().st_size)
