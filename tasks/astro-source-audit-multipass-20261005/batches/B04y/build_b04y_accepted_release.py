#!/usr/bin/env python3
"""Hermetic owner archive, original Lilly accident rectification 1647 witness and rules."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(r.stdout.strip()) if r.returncode==0 and r.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-CI-Accident-Rectification-Documentary-20261017.zip"
files=[
 "PARENT_INDEX_BEFORE_B04y.json",
 "ORIGINAL_ACCIDENT_RECTIFICATION_BOUNDARY_NOTES_20261017.md",
 "SOURCE_WINDOW_PROVISIONAL_20261017.json",
 "SOURCE_GROUPS_PART1_20261017.json","SOURCE_GROUPS_PART2_20261017.json",
 "SOURCE_GROUPS_PART3_20261017.json","SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",
 "SOURCE_FIRST_CLAUSES_DRAFT.json","ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",
 "SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json",
 "prepare_b04y_source_window.py","build_b04y_source_first.py","freeze_b04y_documentary_source.py",
 "test_b04y_original_source_window.py","test_b04y_source_first.py",
 "test_b04y_documentary_admission.py","build_b04y_accepted_release.py"]
files.extend(f"evidence/pdf_1647-{n}.jpg" for n in range(541,555))
assert all((B/f).is_file() for f in files)
manifest={"batch":"B04y","kind":"ORIGINAL_1647_RETROSPECTIVE_ACCIDENT_FIT_SOURCE_ONLY",
 "historical_source_annotations":188,"source_passages":13,
 "original_body_pages":list(range(541,554)),"next_heading_pdf":553,
 "original_all_speculum_numeric_cells_transcribed":False,
 "reported_original_merchant_fever_age":"20y10m",
 "author_subsequently_fitted_age":"19y10m10d",
 "historical_age_discrepancy_unresolved":True,
 "page546_biquintile_misprint":"105deg44",
 "page547_correct_value":"205deg44",
 "independent_human_birth_time_accuracies":0,
 "new_empirical_validations":0,"runtime_promotions":0,
 "members":{f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04y/"+f)
 z.writestr("B04y/RELEASE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="lilly-b04y-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B04y"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,m in manifest["members"].items():
  assert H(E/f)==m["sha256"] and (E/f).stat().st_size==m["bytes"],f
 t=subprocess.run(["python3","-m","unittest","-q",
  "test_b04y_original_source_window","test_b04y_source_first",
  "test_b04y_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-500:])
 assert t.returncode==0 and "Ran 28 tests" in t.stderr,t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
receipt={"batch":"B04y","status":"CRC_SHA256_FULL_EXTRACT_28_REPLAYED_TESTS_VERIFIED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,"zip_crc_pass":True,
 "per_member_sha256_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":28,"accepted_rules_sha256":A["rules_sha256"],
 "documentary_records_if_published":188,
 "independent_birth_time_matches":0,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
