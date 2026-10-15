from pathlib import Path
import hashlib,json
B=Path("/home/joel/humandesign-worktrees/astro-lilly-b02v-20261014/tasks/astro-source-audit-multipass-20261005/batches/B02w")
f=B/"lilly-1647-b30338724-original.pdf"
assert f.stat().st_size==141842963
assert hashlib.sha256(f.read_bytes()).hexdigest()=="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
arr=[]
for pg in range(401,405):
 p=B/"evidence"/f"pdf-{pg}.png"
 assert p.exists()
 arr.append({"original_pdf_page":pg,"printed_page":pg-34,"path":f"evidence/pdf-{pg}.png","sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size})
j={"batch":"B02w","source":"William Lilly Christian Astrology 1647 original b30338724","original_pdf_size":f.stat().st_size,"original_pdf_sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"render_command":"pdftoppm -f 401 -l 404 -scale-to-y 1700 -png exact-original-PDF evidence/pdf","original_images":arr,"opening_page_400_reuses_accepted_B02v_original_image":True,"source_records_accepted":0}
(B/"SOURCE_IMAGE_MANIFEST_OPENING_20261015.json").write_text(json.dumps(j,indent=2)+"\n")
print(json.dumps({"pages":len(arr),"source_sha256":j["original_pdf_sha256"],"rendered":[x["original_pdf_page"] for x in arr]},indent=2))
