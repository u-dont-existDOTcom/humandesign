"""Pixel-verify every B02u original-page image against exact full 1647 source PDF."""
import os,json,hashlib,subprocess,tempfile
from pathlib import Path
from PIL import Image,ImageChops
B=Path(__file__).resolve().parent
ORIGINAL=Path(os.environ.get("LILLY1647_PDF", "/mnt/hdd/home/joel/ai-research-source-cache/lilly-1647-b30338724-original.pdf"))
SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert ORIGINAL.is_file() and ORIGINAL.stat().st_size==141842963
assert hashlib.sha256(ORIGINAL.read_bytes()).hexdigest()==SHA
m=json.loads((B/"SOURCE_IMAGE_MANIFEST.json").read_text())
assert len(m["original_images"])==20
rows=[]
with tempfile.TemporaryDirectory(prefix="b02u-original-pixel-replay-") as t:
 T=Path(t)
 subprocess.run(["pdftoppm","-f","364","-l","381","-scale-to-y","1450","-png",str(ORIGINAL),str(T/"pdf")],check=True)
 subprocess.run(["pdftoppm","-f","400","-l","400","-scale-to-y","1450","-png","-singlefile",str(ORIGINAL),str(T/"next-chapter-boundary-pdf-400")],check=True)
 subprocess.run(["pdftoppm","-f","888","-l","888","-scale-to-y","1800","-png","-singlefile",str(ORIGINAL),str(T/"errata-888")],check=True)
 for row in m["original_images"]:
  name=Path(row["relative_path"]).name
  A=Image.open(B/row["relative_path"]).convert("RGB")
  Z=Image.open(T/name).convert("RGB")
  identical=A.size==Z.size and ImageChops.difference(A,Z).getbbox() is None
  assert identical,(name,A.size,Z.size)
  digest=hashlib.sha256((B/row["relative_path"]).read_bytes()).hexdigest()
  assert digest==row["sha256"]
  rows.append({"source_pdf_page":row["source_pdf_page"],"image_sha256":digest,
               "same_rgb_pixels":True,"size":[A.width,A.height]})
assert len(rows)==20
receipt={"batch":"B02u","original_1647_pdf_sha256":SHA,"original_pdf_total_pages":894,
         "images_pixel_replayed":20,"all_rgb_identical":True,"first_content_pdf_page":364,
         "last_content_pdf_page":381,"includes_errata888":True,
         "includes_next_chapter_boundary400":True,
         "renderer":"pdftoppm scale-to-y1450 for body and page400; 1800 for errata",
         "source_only":True,"independently_verified_predictions":0,"pages":rows}
(B/"SOURCE_REPLAY_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"images_replayed":len(rows),"pixels_identical":True,"pdf_sha256":SHA}))
