"""Fresh-pixel replay of B02s images from full, SHA256-authenticated 1647 PDF."""
from pathlib import Path
import hashlib,json,tempfile,subprocess
from PIL import Image,ImageChops
B=Path(__file__).resolve().parent
SOURCE=Path(__import__("os").environ.get("LILLY1647_PDF", "lilly-1647-b30338724-original.pdf"))
SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert SOURCE.is_file() and SOURCE.stat().st_size==141842963
h=hashlib.sha256()
with SOURCE.open("rb") as f:
 for chunk in iter(lambda:f.read(8*1024*1024),b""):h.update(chunk)
assert h.hexdigest()==SHA
rows=[]
with tempfile.TemporaryDirectory(prefix="b02s-replay-") as tmp:
 o=Path(tmp)
 subprocess.run(["pdftoppm","-f","336","-l","353","-scale-to-y","1400","-png",str(SOURCE),str(o/"pdf")],check=True,stdout=subprocess.DEVNULL)
 subprocess.run(["pdftoppm","-f","888","-l","888","-scale-to-y","1800","-png","-singlefile",str(SOURCE),str(o/"errata-888")],check=True,stdout=subprocess.DEVNULL)
 for n in [*range(336,354),888]:
  name="errata-888.png" if n==888 else f"pdf-{n}.png"
  a=Image.open(B/"evidence"/name).convert("RGB")
  z=Image.open(o/name).convert("RGB")
  same=a.size==z.size and ImageChops.difference(a,z).getbbox() is None
  assert same,(name,a.size,z.size)
  rows.append({"pdf_page":n,"same_rgb_pixels":same,"pixel_dimensions":list(a.size),"evidence_sha256":hashlib.sha256((B/"evidence"/name).read_bytes()).hexdigest()})
doc={"batch":"B02s","source_full_pdf_sha256":SHA,"source_full_pdf_bytes":SOURCE.stat().st_size,
 "all_rgb_replays_identical":True,"pages_replayed":len(rows),
 "renderer":"pdftoppm original PDF336–353 at height1400, original errata PDF888 at height1800",
 "scope":"Verifies included image authenticity, not source statement accuracy, clinical truth or predictions.",
 "results":rows}
(B/"SOURCE_REPLAY_RECEIPT.json").write_text(json.dumps(doc,indent=2)+"\n")
print(json.dumps({"original_source_verified":True,"pages":len(rows),"rgb_pixel_identical":True,"sha256":SHA}))
