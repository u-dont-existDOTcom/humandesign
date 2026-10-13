from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent
p=B/"SOURCE_IMAGE_MANIFEST.json";d=json.loads(p.read_text())
assert len(d["original_images"])==19
f=B/"evidence/pdf-381.png";assert f.is_file()
d["original_images"].append({"source_pdf_page":381,"printed_page":347,
"relative_path":"evidence/pdf-381.png","bytes":f.stat().st_size,
"sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"role":"PAGE_TURN_CONTEXT_NOT_INDEXED"})
d["stage_pages"]=list(range(364,382))
d["next_page_turn"]="PDF381 starts Which way the Thief is gone, with further house and door subsections"
p.write_text(json.dumps(d,indent=2)+"\n")
t=B/"WORKING_CHECKPOINT.md";s=t.read_text().replace("PDF364–380","PDF364–381")
s=s.replace("PDF380's final catchword continues to PDF381","PDF380's catchword continues into original PDF381, which has been included and visually inspected")
t.write_text(s)
print("STAGED_ORIGINAL_IMAGES",len(d["original_images"]))
