"""Verify and copy the already-published archive/report/handoff to owner's OS Downloads.

Use ONLY after a verified nonforce GitHub content publication and canonical
source index readback. Do not overwrite unrelated same-named owner files.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
B=Path(__file__).resolve().parent
ART=B.parent/"deliverables"
manifest=json.loads((B/"DELIVERABLES_MANIFEST.json").read_text())
accept=json.loads((B/"ACCEPTANCE.json").read_text())
packet=json.loads((B/"PACKET_USABILITY.json").read_text())
assert accept["accepted"] and packet["actual_extraction"]
assert accept["criminal_or_medical_validity"] is False and accept["prospective_frozen_predictions"] == 0
dir_text=subprocess.check_output(["xdg-user-dir","DOWNLOAD"],text=True).strip()
DEST=Path(dir_text)
assert DEST.is_dir() and DEST.is_absolute(), "OS Downloads directory inaccessible"
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipt_rows=[]
for e in manifest["files"]:
 src=ART/e["filename"];dst=DEST/e["filename"]
 assert src.is_file() and src.stat().st_size==e["bytes"] and H(src)==e["sha256"],src
 if dst.exists():
  assert dst.is_file() and H(dst)==e["sha256"],"Refuse to overwrite nonmatching existing owner file: "+str(dst)
 else:shutil.copy2(src,dst)
 assert dst.stat().st_size==e["bytes"] and H(dst)==e["sha256"],dst
 receipt_rows.append({**e,"download_path":str(dst),"hash_matched":True})
rec={"batch":"B02t","delivery":"Owner OS Downloads (xdg-user-dir)",
     "directory":str(DEST),"files":receipt_rows,
     "all_destination_hashes_match_exact_published_manifest":True,
     "independent_clinical_or_predictive_validation":False,
     "archive_sha256":packet["sha256"],
     "extracted_tests_replayed":packet["extracted_tests_run"],
     "original_source_pdf_not_packaged":"Original 1647 PDF is separately cached with its SHA256; cropped original source pages and errata are in ZIP"}
(B/"DELIVERY_RECEIPT.json").write_text(json.dumps(rec,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"delivered":len(receipt_rows),"bytes":sum(q["bytes"] for q in receipt_rows),
                  "destination":str(DEST),"all_sha256_matched":True,"files":[q["filename"] for q in receipt_rows]}))
