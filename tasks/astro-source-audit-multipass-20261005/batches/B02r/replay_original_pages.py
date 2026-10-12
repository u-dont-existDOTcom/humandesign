"""Original-volume SHA-256 and independent pixel replay, not source-semantic validation."""
from pathlib import Path
from PIL import Image,ImageChops
import hashlib,tempfile,subprocess,json
B=Path(__file__).resolve().parent
SRC=Path("/mnt/hdd/home/joel/ai-research-source-cache/lilly-1647-b30338724-original.pdf")
SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert SRC.is_file() and SRC.stat().st_size==141842963
assert hashlib.sha256(SRC.read_bytes()).hexdigest()==SHA
results=[]
with tempfile.TemporaryDirectory(prefix="b02r-pixel-replay-") as td:
 out=Path(td)
 subprocess.run(["pdftoppm","-f","330","-l","337","-scale-to-y","1700","-png",str(SRC),str(out/"pdf")],check=True)
 subprocess.run(["pdftoppm","-f","888","-l","888","-scale-to-y","1800","-png","-singlefile",str(SRC),str(out/"errata-888")],check=True)
 for pg in [*range(330,338),888]:
  f="errata-888.png" if pg==888 else f"pdf-{pg}.png"
  a=Image.open(B/"evidence"/f).convert("RGB")
  z=Image.open(out/f).convert("RGB")
  same=a.size==z.size and ImageChops.difference(a,z).getbbox() is None
  assert same, (f,a.size,z.size)
  results.append({"pdf_page":pg,"same_rgb_pixels":same,"dimensions":list(a.size),
                  "original_evidence_sha256":hashlib.sha256((B/"evidence"/f).read_bytes()).hexdigest()})
obj={"batch":"B02r","original_1647_pdf_sha256":SHA,"original_1647_pdf_bytes":SRC.stat().st_size,
     "all_rgb_replays_identical":all(r["same_rgb_pixels"] for r in results),"pages_replayed":len(results),
     "renderer":"pdftoppm pages330-337, scale-to-y1700; errata888 scale-to-y1800",
     "source_claim_scope":"Proves page-image authenticity against exact cached PDF, not correctness of paraphrases or astrology.", "results":results}
(B/"SOURCE_REPLAY_RECEIPT.json").write_text(json.dumps(obj,indent=2)+"\n")
print(json.dumps({"original_verified":True,"page_images":len(results),"pixels_match":True,"sha256":SHA}))
