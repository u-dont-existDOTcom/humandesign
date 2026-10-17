#!/usr/bin/env python3
"""Original 1647 Lilly natal-prejudgment source ZIP, CRC/SHA/extracted unit tests."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-CIII-Natal-Prejudgment-1647-20261017.zip"
files=[
 "SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",
 "SOURCE_FIRST_CLAUSES_DRAFT.json","ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",
 "SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json",
 "build_b05a_source_first.py","test_b05a_source_first.py",
 "freeze_b05a_documentary_source.py","test_b05a_documentary_admission.py",
 "build_b05a_release.py","evidence/pdf_1647-558.jpg","evidence/pdf_1647-559.jpg"]
assert all((B/f).is_file() for f in files)
M={"batch":"B05a","kind":"ORIGINAL_1647_NATAL_PREJUDGMENT_CONDITIONALS_NOT_EMPIRICAL",
 "historic_documentary_annotations":29,"original_body_pdf_page":558,
 "following_separate_lifespan_heading_pdf_page":559,
 "original_antiscia_proximity_threshold_specified":False,
 "original_fixed_star_latitude_threshold_specified":False,
 "independent_person_predictions_validated":0,
 "members":{f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B05a/"+f)
 z.writestr("B05a/RELEASE_SHA256_MANIFEST.json",json.dumps(M,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="lilly-b05a-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B05a"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==M
 for f,m in M["members"].items():
  assert H(E/f)==m["sha256"] and (E/f).stat().st_size==m["bytes"],f
 t=subprocess.run(["python3","-m","unittest","-q","test_b05a_source_first",
 "test_b05a_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-350:])
 assert t.returncode==0 and "Ran 17 tests" in t.stderr,t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
receipt={"batch":"B05a","status":"CRC_SHA256_FULL_EXTRACT_17_TEST_REPLAY",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,
 "crc_pass":True,"member_hashes_pass":True,"full_extraction_pass":True,
 "archive_replayed_tests":17,"accepted_rules_sha256":A["rules_sha256"],
 "historic_records_if_published":29,
 "independent_predictive_validations":0,"runtime_promotions":0,
 "remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
