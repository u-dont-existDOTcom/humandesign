"""Create/verify B02w source-first historical documentary ZIP, UNACCEPTED.

This is portable proof of preserved original scanned page images, normalized
historical text units, tests and handoff. Full 142MB original PDF remains
local on authorized laptop, identified by exact SHA; not uploaded to Git.
"""
from pathlib import Path,PurePosixPath
import hashlib, json, zipfile, tempfile, subprocess, shutil

B=Path(__file__).resolve().parent
OUT=B/"Astrology-Lilly-Chapter-LI-Source-First-Provisional-20261015.zip"
DEST=Path("/mnt/hdd/home/joel/Téléchargements")/OUT.name
RECEIPT=B/"SOURCE_FIRST_PROVISIONAL_PACKET_RECEIPT_20261015.json"
def h(blob):return hashlib.sha256(blob).hexdigest()
def load(name):return json.loads((B/name).read_text())
S=load("RULES_DRAFT.json");W=load("SOURCE_WINDOW_MANIFEST.json")
assert not S["accepted"] and S["newly_accepted_documentary_records"]==0
assert len(S["records"])==42
assert W["closing"]["last_chapter_LI_pdf_page"]==402
assert W["closing"]["next_heading_pdf_page"]==403
assert not OUT.exists() and not RECEIPT.exists(),"Already packaged; compare or version rather than overwrite"
paths=[]
for path in B.rglob("*"):
    if not path.is_file() or path.is_symlink() or path.suffix not in {".json",".md",".py",".png"}:continue
    rel=path.relative_to(B)
    if "__pycache__" in rel.parts or rel.name.startswith("."):continue
    if rel.name.startswith("Astrology-Lilly-"):continue
    if rel.name=="SOURCE_FIRST_PACKET_MANIFEST.json":continue
    paths.append(rel)
paths=sorted(paths,key=lambda x:x.as_posix())
members={p.as_posix() for p in paths}
for name in ["RULES_DRAFT.json","SOURCE_FIRST_CLAUSES_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "SOURCE_ORDER_DRAFT.json","UNRESOLVED_DRAFT.json","test_b02w_staging.py",
 "LI_SOURCE_FIRST_INVENTORY_NOTES_20261015.md",
 "RETAINED_LILLY_INDEX_BEFORE_B02w.json","evidence/pdf-400.png",
 "evidence/pdf-401.png","evidence/pdf-402.png","evidence/pdf-403.png"]:
 assert name in members,name
files=[]
for rel in paths:
    blob=(B/rel).read_bytes()
    files.append({"path":rel.as_posix(),"bytes":len(blob),"sha256":h(blob)})
manifest={
 "kind":"UNACCEPTED_B02w_LILLY_CHAPTER_LI_SOURCE_FIRST_DOCUMENTARY",
 "source_authority":"William Lilly Christian Astrology 1647 original Wellcome b30338724",
 "original_full_pdf_sha256":"2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b",
 "original_pdf_excluded_from_zip_by_design":True,
 "source_window_original_pdf_pages":[400,401,402],
 "source_boundary_next_chapter_heading_pdf_page":403,
 "pdf404_is_additional_next_chapter_preview_not_LI_text":True,
 "previous_lilly_accepted":2974,
 "provisional_source_units":42,
 "accepted_new_source_units":0,
 "uncertainties":11,
 "empirical_cases_added":0,
 "independent_diplomatic_source_certification_completed":False,
 "files":files
}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
    for rel in paths:z.write(B/rel,arcname=rel.as_posix())
    z.writestr("SOURCE_FIRST_PACKET_MANIFEST.json",json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")
with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None
    assert set(z.namelist())==members|{"SOURCE_FIRST_PACKET_MANIFEST.json"}
    assert json.loads(z.read("SOURCE_FIRST_PACKET_MANIFEST.json"))==manifest
    for f in files:
        blob=z.read(f["path"])
        assert len(blob)==f["bytes"] and h(blob)==f["sha256"],f["path"]
    with tempfile.TemporaryDirectory(prefix="lilly-LI-replay-") as tmp:
        for info in z.infolist():
            p=PurePosixPath(info.filename)
            assert not p.is_absolute() and ".." not in p.parts
        z.extractall(tmp)
        for f in files:
            assert h((Path(tmp)/f["path"]).read_bytes())==f["sha256"]
        result=subprocess.run(["python3",str(Path(tmp)/"test_b02w_staging.py")],
                  capture_output=True,text=True,timeout=120)
        if result.returncode!=0:
            print(result.stdout+result.stderr)
            raise AssertionError("extracted staging test did not pass")
        test_output=(result.stdout+result.stderr).splitlines()[-6:]
        assert any("Ran 16 tests" in line for line in test_output),test_output
DEST.parent.mkdir(parents=True,exist_ok=True)
digest=h(OUT.read_bytes())
if DEST.exists():
    assert h(DEST.read_bytes())==digest,"Destination exists with different content, refusing overwrite"
else:
    with DEST.open("xb") as out, OUT.open("rb") as source:shutil.copyfileobj(source,out)
assert h(DEST.read_bytes())==digest
receipt={
 "kind":manifest["kind"],
 "status":"VERIFIED_DELIVERED_PROVISIONAL_NOT_ACCEPTED",
 "source_pages":[400,401,402],
 "next_boundary_page":403,
 "provisional_records":42,
 "source_image_count_in_window":4,
 "source_issues_retained":11,
 "file_payload_count":len(files),
 "zip_size_bytes":OUT.stat().st_size,
 "zip_sha256":digest,
 "delivery_path":str(DEST),
 "delivery_sha256":h(DEST.read_bytes()),
 "crc_pass":True,
 "every_file_hash_pass":True,
 "actual_extraction_pass":True,
 "extracted_suite":"test_b02w_staging.py",
 "extracted_tests_passed":16,
 "source_documentary_accepted":False,
 "scientifically_validated_predicted_outcomes":0,
 "test_last_lines":test_output
}
RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(receipt,ensure_ascii=False,indent=2))
