"""Build, extract, replay and deliver historical-documentary-only B02v source packet.

B02v local admission is source TEXT inventory only. Never alter canonical
index or scientific prediction model. Original source PNGs in packet.
"""
from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,tempfile,subprocess,shutil,re
B=Path(__file__).resolve().parent
ZIP_NAME="Astrology-Lilly-Chapter-L-Documentary-Source-Acceptance-20261015.zip"
OUT=B/"independent_review"/ZIP_NAME
RECEIPT=B/"independent_review/DOCUMENTARY_SOURCE_RELEASE_RECEIPT_U75_20261015.json"
assert not OUT.exists() and not RECEIPT.exists(),"Release packet/receipt exists; never silently overwrite."
SRC="2cb53e20e122ffc6e47917ba10241f6c49687cd7a4696f3b5db655a2a1aab28b"
sha=lambda data:hashlib.sha256(data).hexdigest()
rd=lambda name:json.loads((B/name).read_text())
A=rd("ACCEPTANCE.json")
R=rd("RULES.json")
U=rd("UNRESOLVED.json")
C=rd("ACCEPTANCE_CANDIDATE.json")
assert A["accepted"] and A["kind"]=="HISTORICAL_SOURCE_DOCUMENTARY_ONLY"
assert A["source_only_tests_passed"]==109 and A["prior_accepted_lilly"]==2572
assert R["record_count"]==402 and len(R["rules"])==402
assert U["retained_count"]==75 and C["new_source_units"]==402
assert A["original_source_pdf_sha256"]==SRC and not A["canonical_published"]
for key,name in (("rules_sha256","RULES.json"),("unresolved_sha256","UNRESOLVED.json"),("source_order_sha256","SOURCE_ORDER.json"),("claim_ledger_sha256","CLAIM_LEDGER.json")):
 assert A[key]==sha((B/name).read_bytes()),key
chosen=[]
for p in B.rglob("*"):
 if not p.is_file() or p.is_symlink():continue
 rel=p.relative_to(B)
 if "__pycache__" in rel.parts or "review_images" in rel.parts:continue
 if "crops" in rel.parts:continue
 if rel.name.startswith(".") or rel.name.endswith(".zip"):continue
 if p.suffix not in {".json",".md",".py",".png"}:continue
 chosen.append(rel)
chosen.sort(key=lambda x:x.as_posix())
names={p.as_posix() for p in chosen}
needed={"ACCEPTANCE.json","ACCEPTANCE_CANDIDATE.json","RULES.json","UNRESOLVED.json","CLAIM_LEDGER.json",
"SOURCE_ORDER.json","TEST_RUN_SUMMARY.json","RULES_DRAFT.json","SOURCE_IMAGE_MANIFEST.json",
"independent_review/FINITE_HIGH_RISK_SOURCE_PASS_U75_20261015.json",
"independent_review/REVERSE_SOURCE_COVERAGE_20P_U75_20261015.json"}
assert needed<=names
assert {f"evidence/pdf-{i}.png" for i in range(381,401)}<=names
assert "evidence/errata-888.png" in names
assert len([n for n in names if n.startswith("evidence/") and n.endswith(".png")])==21
manifest={
 "kind":"HISTORICAL_SOURCE_DOCUMENTARY_ONLY_B02v_LOCALLY_ADMITTED_CANONICAL_INTEGRATION_PENDING",
 "batch":"B02v","accepted_historical_editorial_source_units":402,
 "new_real_world_empirical_validation":0,"prior_accepted_lilly":2572,
 "lilly_after_successful_canonical_integration":2974,
 "accepted_chapter":"L","next_chapter":"LI",
 "source_original_pdf_sha256":SRC,
 "retained_source_interpretation_issues":75,
 "original_images":21,
 "source_finite_high_risk_review_done":True,
 "complete_independent_diplomatic_reconstruction_proven":False,
 "raw_source_image_and_record_companions_present":True,
 "all_files":[{"path":p.as_posix(),"size_bytes":(B/p).stat().st_size,"sha256":sha((B/p).read_bytes())} for p in chosen]
}
with zipfile.ZipFile(OUT,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for f in chosen:z.write(B/f,f.as_posix())
 z.writestr("DOCUMENTARY_SOURCE_MANIFEST.json",json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
tests=("test_source_integrity_v18.py","test_reverse_20p_u75.py","test_b02v_staging.py",
"independent_review/test_reconciled_draft.py","test_documentary_admission_u75.py")
results={}
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None
 assert set(z.namelist())==names|{"DOCUMENTARY_SOURCE_MANIFEST.json"}
 assert json.loads(z.read("DOCUMENTARY_SOURCE_MANIFEST.json"))==manifest
 for f in manifest["all_files"]:
  content=z.read(f["path"])
  assert (len(content),sha(content))==(f["size_bytes"],f["sha256"]),f["path"]
 with tempfile.TemporaryDirectory(prefix="lilly-b02v-source-admission-") as tmp:
  base=Path(tmp)
  for item in z.infolist():
   src=PurePosixPath(item.filename)
   assert not src.is_absolute() and ".." not in src.parts
  z.extractall(base)
  for f in manifest["all_files"]:
   data=(base/f["path"]).read_bytes()
   assert sha(data)==f["sha256"]
  for name in tests:
   run=subprocess.run(["python3",str(base/name)],capture_output=True,text=True,timeout=180)
   output=run.stderr+"\n"+run.stdout
   match=re.search(r"Ran (\d+) tests? in",output)
   count=int(match.group(1)) if match else None
   results[name]={"exit_code":run.returncode,"tests_run":count,"output_last_lines":output.strip().splitlines()[-5:]}
   if run.returncode!=0 or count is None or "OK" not in output:
    print(json.dumps({"failure":results[name]},indent=2))
    raise AssertionError(f"Extracted test failed: {name}")
assert [results[x]["tests_run"] for x in tests]==[61,6,18,12,12]
downloads=subprocess.check_output(["xdg-user-dir","DOWNLOAD"],text=True).strip()
assert downloads and downloads.startswith("/")
dest=Path(downloads)/ZIP_NAME
dest.parent.mkdir(parents=True,exist_ok=True)
digest=sha(OUT.read_bytes())
if dest.exists():
 assert sha(dest.read_bytes())==digest,"Existing owner Downloads packet differs; refusal to overwrite"
else:
 with dest.open("xb") as f,OUT.open("rb") as src:shutil.copyfileobj(src,f)
assert sha(dest.read_bytes())==digest
receipt={
 "kind":manifest["kind"],"status":"SUCCESS_LOCAL_DOCUMENTARY_ONLY_RELEASE_PACKET_DELIVERED",
 "batch":"B02v","local_documentary_admission":True,
 "canonical_index_published":False,
 "original_pdf_sha256":SRC,
 "accepted_documentary_source_records":402,
 "retained_textual_uncertainties":75,
 "number_archived_files":len(chosen),"number_original_source_images":21,
 "archive_size_bytes":OUT.stat().st_size,
 "archive_sha256":digest,"destination_os_downloads":str(dest),
 "destination_sha256":sha(dest.read_bytes()),
 "manifest_member_sha256_pass":True,
 "zip_crc_pass":True,
 "actual_zip_extraction_pass":True,
 "extracted_per_file_sha256_pass":True,
 "actual_extracted_tests":results,
 "distinct_source_only_tests_passed":sum(x["tests_run"] for x in results.values()),
 "original_source_claims_empirically_validated":False,
 "full_independent_diplomatic_transcription_claimed":False
}
RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"source_only_admitted_locally":True,
 "files":len(chosen),"original_images":21,"bytes":OUT.stat().st_size,
 "sha256":digest,"downloads_path":str(dest),
 "extracted_tests":receipt["distinct_source_only_tests_passed"],
 "canonical_integrated":False},indent=2))
