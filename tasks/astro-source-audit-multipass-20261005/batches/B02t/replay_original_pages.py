"""Reproduce original-volume B02t source renderings; documentary provenance only."""
import os,hashlib,json,subprocess,tempfile
from pathlib import Path
from PIL import Image,ImageChops
B=Path(__file__).resolve().parent
SRC=Path(os.environ.get("LILLY1647_PDF","lilly-1647-b30338724-original.pdf"))
SHA="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert SRC.is_file() and hashlib.sha256(SRC.read_bytes()).hexdigest()==SHA
manifest=json.loads((B/"SOURCE_IMAGE_MANIFEST.json").read_text())
outcomes=[]
with tempfile.TemporaryDirectory(prefix="lilly-b02t-source-replay-") as tmp:
    t=Path(tmp)
    subprocess.run(["pdftoppm","-f","353","-l","369","-scale-to-y","1450","-png",str(SRC),str(t/"pdf")],check=True)
    subprocess.run(["pdftoppm","-f","400","-l","400","-scale-to-y","1450","-png","-singlefile",str(SRC),str(t/"next-chapter-boundary-pdf-400")],check=True)
    subprocess.run(["pdftoppm","-f","888","-l","888","-scale-to-y","1800","-png","-singlefile",str(SRC),str(t/"errata-888")],check=True)
    for e in manifest["images"]:
        name=Path(e["path"]).name
        a=Image.open(B/e["path"]).convert("RGB")
        z=Image.open(t/name).convert("RGB")
        same=a.size==z.size and ImageChops.difference(a,z).getbbox() is None
        assert same,("source page image differs from original full PDF",name)
        actual=hashlib.sha256((B/e["path"]).read_bytes()).hexdigest()
        assert actual==e["sha256"]
        outcomes.append({"pdf_page":e["pdf_page"],"pixels_identical":True,"image_sha256":actual,"width":a.width,"height":a.height})
receipt={"batch":"B02t","original_pdf_sha256":SHA,
         "images_pixel_replayed":len(outcomes),"all_rgb_pixel_identical":True,
         "source_scope_only":True,"accepted_documentary_records":0,
         "commands":"pdftoppm page353-369 scale1450; page400 scale1450; errata888 scale1800",
         "pages":outcomes}
(B/"SOURCE_REPLAY_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"batch":"B02t","pages":len(outcomes),"pixel_identical_all":True,"documentary_source_only":True}))
