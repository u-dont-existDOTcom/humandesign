"""UNEXECUTED OPTIONAL helper: execution was blocked by tool safety checks.

Small unaccepted review-evidence companion for existing v10 source-image ZIP.

No source acceptance; original images are retained in previous v10 source
packet, not duplicated in this review-data-only companion archive.
"""
from pathlib import Path,PurePosixPath
import hashlib,json,tempfile,zipfile,shutil
B=Path(__file__).resolve().parent
DEST=Path("/mnt/hdd/home/joel/Téléchargements")
name="Astrology-Lilly-B02v-Reverse-Audit-20-Pages-20261015.zip"
OUT=B/"independent_review"/name
cov=json.loads((B/"independent_review/REVERSE_SOURCE_COVERAGE_20P_20261015.json").read_text())
assert cov["source_reverse_pages_mapped"]==20 and cov["distinct_candidate_record_ids_mapped"]==402
assert not cov["independent_diplomatic_text_completeness"]
files=sorted({p["map_file"] for p in cov["page_map_manifest"]}|{
 "independent_review/REVERSE_SOURCE_COVERAGE_20P_20261015.json",
 "independent_review/REVERSE_SOURCE_20P_REPORT_20261015.md",
 "SOURCE_IMAGE_MANIFEST.json","SOURCE_ORDER_DRAFT.json","test_reverse_20p_20261015.py",
 "RULES_DRAFT.json"},key=str)
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest={"kind":"UNACCEPTED_B02v_BOUNDED_REVERSE_PAGE_REVIEW_COMPANION",
          "source_image_packet":"Astrology-Lilly-B02v-Provisional-Source-Packet-v10-20261015.zip",
          "source_images_included":False,
          "20_source_pages_mapped":True,"candidate_record_ids_mapped":402,
          "independent_full_source_text_completeness":False,
          "accepted_new_records":0,
          "files":[{"path":x,"bytes":(B/x).stat().st_size,"sha256":sha((B/x).read_bytes())} for x in files]}
OUT.parent.mkdir(parents=True,exist_ok=True)
assert not OUT.exists(),"review companion already exists; do not overwrite"
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for f in files:z.write(B/f,f)
 z.writestr("REVIEW_COMPANION_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None
 assert set(z.namelist())==set(files)|{"REVIEW_COMPANION_MANIFEST.json"}
 assert json.loads(z.read("REVIEW_COMPANION_MANIFEST.json"))==manifest
 for e in manifest["files"]:
  assert sha(z.read(e["path"]))==e["sha256"]
 with tempfile.TemporaryDirectory(prefix="lilly-20p-review-") as temp:
  for info in z.infolist():
   p=PurePosixPath(info.filename)
   assert not p.is_absolute() and ".." not in p.parts
  z.extractall(temp)
  for e in manifest["files"]:
   assert sha((Path(temp)/e["path"]).read_bytes())==e["sha256"]
digest=sha(OUT.read_bytes())
DEST.mkdir(parents=True,exist_ok=True)
target=DEST/name
if target.exists():
 assert sha(target.read_bytes())==digest,"existing Downloads file differs"
else:
 with target.open("xb") as f,OUT.open("rb") as src:shutil.copyfileobj(src,f)
assert sha(target.read_bytes())==digest
receipt={"status":manifest["kind"],"review_pages":20,
 "mapped_candidate_ids":402,"normalized_anchors":419,
 "payload_file_count":len(files),"zip_bytes":OUT.stat().st_size,
 "archive_sha256":digest,"download_path":str(target),
 "download_sha256":sha(target.read_bytes()),
 "crc_and_all_archived_sha256_pass":True,"real_extraction_sha256_pass":True,
 "source_diplomatic_completeness_accepted":False,"canonical_index_advanced":False}
(B/"independent_review/REVERSE_20P_COMPANION_DELIVERY_RECEIPT_20261015.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
