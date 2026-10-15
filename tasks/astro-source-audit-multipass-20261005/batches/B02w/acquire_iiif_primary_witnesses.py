"""Obtain original Wellcome IIIF page images, not PDF-byte-identical renders."""
from pathlib import Path
from PIL import Image
import hashlib,json,subprocess
B=Path(__file__).resolve().parent
manifest_path=Path("/tmp/wellcome-b30338724-iiifv3-manifest.json")
assert manifest_path.is_file()
m=json.loads(manifest_path.read_text())
assert len(m["items"])==894 and m["type"]=="Manifest"
rows=[]
for pdf_page in range(400,408):
    canvas=m["items"][pdf_page-1]
    assert canvas["label"]["none"]==[str(pdf_page-34)]
    body=canvas["items"][0]["items"][0]["body"]
    service=body["service"][0]["@id"]
    assert service.startswith("https://iiif.wellcomecollection.org/image/b30338724_")
    assert service.endswith(f"_0{pdf_page}.jp2")
    url=service+"/full/1800,/0/default.jpg"
    dest=B/"evidence"/f"pdf-{pdf_page}-iiif.jpg"
    if not dest.exists():
        temp=dest.with_suffix(".part")
        assert not temp.exists(),"Ambiguous incomplete prior attempt"
        result=subprocess.run(["curl","-fsSL","--retry","2","--max-time","60","-o",str(temp),url],capture_output=True,text=True)
        assert result.returncode==0,result.stderr[-600:]
        temp.replace(dest)
    with Image.open(dest) as im:
        im.load()
        assert im.format=="JPEG" and im.size[0]>=1700 and im.size[1]>=2100
        size=list(im.size)
    blob=dest.read_bytes()
    rows.append({"pdf_page":pdf_page,"printed_page":pdf_page-34,"canvas":canvas["id"],
                 "iiif_service":service,"derived_url":url,"path":str(dest.relative_to(B)),
                 "bytes":len(blob),"sha256":hashlib.sha256(blob).hexdigest(),"image_pixels":size})
output={"batch":"B02w","source_id":"LILLY1647_WELLCOME_B30338724",
        "iiif_manifest":"https://iiif.wellcomecollection.org/presentation/v3/b30338724",
        "iiif_manifest_sha256":hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "accepted_prior_original_full_PDF_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
        "image_kind":"DERIVED_WELLCOME_IIIF_JPEG_NOT_PDF_RENDER_PIXEL_IDENTICAL",
        "source_public_domain":True,"pages":rows,
        "page400_comparison_to_accepted_image":"PENDING_MANUAL_VISUAL_REVIEW",
        "source_text_accepted":False,"empirical_cases":0}
p=B/"IIIF_SOURCE_WITNESS_MANIFEST.json"
assert not p.exists(),"Existing manifest: verify, do not overwrite"
p.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"images":len(rows),"bytes":sum(z["bytes"] for z in rows),"pages":[z["pdf_page"] for z in rows],"manifest_hash":hashlib.sha256(p.read_bytes()).hexdigest()},indent=2))
