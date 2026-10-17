#!/usr/bin/env python3
"""Hermetic first-edition Lilly historical lifespan source archive with replay tests."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(p.stdout.strip()) if p.returncode==0 and p.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-CIV-Historical-Lifespan-Source-20261017.zip"
files=[
 "SOURCE_GROUPS_PART1_20261017.json","SOURCE_GROUPS_PART2_20261017.json",
 "SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",
 "SOURCE_FIRST_CLAUSES_DRAFT.json","ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",
 "SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json",
 "build_b05b_source_first.py","test_b05b_source_first.py",
 "freeze_b05b_documentary_source.py","test_b05b_documentary_admission.py",
 "build_b05b_release.py","evidence/pdf_1647-559.jpg","evidence/pdf_1647-560.jpg",
 "evidence/pdf_1647-561.jpg"]
assert all((B/f).is_file() for f in files)
manifest={"batch":"B05b","kind":"ORIGINAL_1647_INFANT_SURVIVAL_ASTROLOGY_HISTORICAL_ONLY",
 "historic_annotations":65,"source_groups":6,"primary_image_pages":[559,560,561],
 "separate_Hyleg_heading_on_shared_page":561,
 "clinical_survival_predictions_validated":False,
 "new_empirical_validations":0,"runtime_promotions":0,
 "members":{f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B05b/"+f)
 z.writestr("B05b/RELEASE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="lilly-b05b-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B05b"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,m in manifest["members"].items():
  assert H(E/f)==m["sha256"] and (E/f).stat().st_size==m["bytes"],f
 t=subprocess.run(["python3","-m","unittest","-q","test_b05b_source_first",
  "test_b05b_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-400:])
 assert t.returncode==0 and "Ran 19 tests" in t.stderr,t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B05b","status":"CRC_SHA256_FULL_EXTRACT_19_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,"crc_pass":True,
 "member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":19,"accepted_rules_sha256":A["rules_sha256"],
 "documentary_records_if_published":65,
 "independent_survival_prognoses_verified":0,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
