"""Non-destructive scaled crops for human/model visual collation of original B02v witness images."""
from pathlib import Path
from PIL import Image, ImageEnhance
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "evidence"
OUT = Path(__file__).resolve().parent / "crops"
OUT.mkdir(parents=True, exist_ok=True)
for source, region, name in [
    ("errata-888.png", (650, 880, 1490, 1070), "errata-p360-line4.png"),
    ("pdf-394.png", (450, 290, 1510, 540), "body-p360-first-lines.png"),
    ("pdf-381.png", (0, 1030, 1160, 1220), "body-p347-sun-moon.png"),
    ("pdf-394.png", (480, 1220, 1510, 1440), "body-p360-house-list.png"),
]:
    with Image.open(SRC/source) as img:
        clip = img.crop(region)
        clip = clip.resize((clip.width*3, clip.height*3), Image.Resampling.LANCZOS)
        clip.save(OUT/name)
        print(name, clip.size)
