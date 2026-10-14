"""Re-render exact authenticated 1647 original PDF and verify all B02v PNGs.
A pixel match authenticates the included visual witness, not its interpretation.
"""
from pathlib import Path
from PIL import Image,ImageChops
import hashlib,json,tempfile,subprocess,os
B=Path(__file__).resolve().parent
manifest=json.loads((B/"SOURCE_IMAGE_MANIFEST.json").read_text())
SOURCE=Path(os.environ.get("LILLY1647_PDF", "lilly-1647-b30338724-original.pdf"))
EXPECTED="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
assert SOURCE.is_file() and SOURCE.stat().st_size==141842963
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
assert [x["pdf_page"] for x in manifest["images"] if x["pdf_page"]!=888]==list(range(381,401))
receipts=[]
with tempfile.TemporaryDirectory(prefix="lilly-B02v-source-replay-") as tmp:
    t=Path(tmp)
    subprocess.run(["pdftoppm","-f","381","-l","400","-scale-to-y","1700","-png",str(SOURCE),str(t/"pdf")],check=True)
    subprocess.run(["pdftoppm","-f","888","-l","888","-scale-to-y","1800","-png","-singlefile",str(SOURCE),str(t/"errata-888")],check=True)
    for entry in manifest["images"]:
        name=Path(entry["path"]).name
        original_image=B/entry["path"]
        replay=t/name
        assert original_image.is_file() and replay.is_file(),name
        before=Image.open(original_image).convert("RGB")
        after=Image.open(replay).convert("RGB")
        identical=before.size==after.size and ImageChops.difference(before,after).getbbox() is None
        digest=hashlib.sha256(original_image.read_bytes()).hexdigest()
        assert original_image.stat().st_size==entry["bytes"] and digest==entry["sha256"]
        assert identical, ("Raster mismatch",name)
        receipts.append({"pdf_page":entry["pdf_page"],"image_sha256":digest,
                         "rgb_pixel_identical":True,"size_pixels":list(before.size)})
receipt={"batch":"B02v","original_pdf_sha256":EXPECTED,"original_pdf_bytes":SOURCE.stat().st_size,
        "source_body_pages":20,"original_errata_pages":1,
        "all_source_image_renders_replayed_rgb_identical":True,
        "scope":"Original page provenance only; historical astrology and person-identification validity not tested",
        "render_command":"pdftoppm PDF381-400 scale-to-y1700; PDF888 scale-to-y1800",
        "images":receipts}
(B/"SOURCE_REPLAY_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"images_verified":len(receipts),"source_sha256":EXPECTED,"all_rgb_pixels_identical":True}))
