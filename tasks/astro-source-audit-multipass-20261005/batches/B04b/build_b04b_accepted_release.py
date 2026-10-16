#!/usr/bin/env python3
"""Original-source LXXXII office historical archive: independent SHA/CRC/test replay."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-LXXXII-Office-Preferment-Documentary-20261016.zip"
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
files=[
 "SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json",
 "build_b04b_source_first.py","test_b04b_source_first.py",
 "freeze_b04b_documentary_source.py","test_b04b_documentary_admission.py",
 "build_b04b_accepted_release.py","SOURCE_FIRST_CLAUSES_DRAFT.json",
 "ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json","SOURCE_ORDER_DRAFT.json",
 "SOURCE_WINDOW_MANIFEST.json","UNRESOLVED_SOURCE_LIMITS.json",
 "CLAIM_LEDGER.json","SOURCE_FIRST_IMAGE_AUDIT_20261016.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json",
 "ACCEPTANCE.json","ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json"]
files += [f"evidence/pdf_1647-{n}.jpg" for n in (478,479,480,481,482)]
assert all((B/f).is_file() for f in files)
members={f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}
m={"batch":"B04b","kind":"1647_OFFICE_PREFERMENT_AND_TENURE_HISTORICAL_TEXT",
 "historical_source_annotations":141,"source_passages":21,
 "unresolved_source_qualifications":26,
 "original_pdf_pages":[478,479,480,481,482],
 "independent_predictions_verified":0,"runtime_promotions":0,
 "members":members}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04b/"+f)
 z.writestr("B04b/RELEASE_SHA256_MANIFEST.json",json.dumps(m,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="lilly-b04b-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B04b"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==m
 for f,v in members.items():
  assert (E/f).stat().st_size==v["bytes"] and H(E/f)==v["sha256"],f
 t=subprocess.run(["python3","-m","unittest","-q","test_b04b_source_first",
                   "test_b04b_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-350:])
 assert t.returncode==0 and "Ran 18 tests" in t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
z={"batch":"B04b","status":"CRC_SHA256_FULL_EXTRACT_18_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,"zip_crc_pass":True,
 "member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":18,"extracted_exit_code":t.returncode,
 "accepted_rules_sha256":A["rules_sha256"],
 "source_records_if_published":141,
 "independently_verified_office_cases":0,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").write_text(json.dumps(z,indent=2)+"\n")
print(json.dumps(z,indent=2))
