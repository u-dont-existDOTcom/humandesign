#!/usr/bin/env python3
"""Hermetic release of Lilly manners first-edition source, without personality assertions."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-CVIII-Manners-Original-20261017.zip"
files=["SOURCE_GROUPS_PART1_20261017.json","SOURCE_GROUPS_PART2_20261017.json",
 "SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json","SOURCE_FIRST_CLAUSES_DRAFT.json",
 "ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json","SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json",
 "build_b05f_source_first.py","test_b05f_source_first.py",
 "freeze_b05f_documentary_source.py","test_b05f_documentary_admission.py","build_b05f_release.py"]
files += [f"evidence/pdf_1647-{n}.jpg" for n in range(568,576)]
assert all((B/f).is_file() for f in files)
manifest={"batch":"B05f","kind":"HISTORICAL_1647_MANNERS_SIGN_FIXED_STAR_SOURCE_NOT_PERSONALITY_VALIDATION",
 "documentary_source_annotations":86,"source_passages":14,"retained_uncertainties":30,
 "original_pdf_pages":list(range(568,576)),
 "Angelus_rising_degree_method_rejected_by_Lilly":True,
 "severe_violent_moral_fixed_star_claims_not_independent_evidence":True,
 "actual_blinded_personality_validations":0,
 "members":{f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B05f/"+f)
 z.writestr("B05f/RELEASE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="Lilly-B05f-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B05f"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,v in manifest["members"].items():
  assert (E/f).stat().st_size==v["bytes"] and H(E/f)==v["sha256"],f
 t=subprocess.run(["python3","-m","unittest","-q",
  "test_b05f_source_first","test_b05f_documentary_admission"],
  cwd=E,capture_output=True,text=True)
 print(t.stderr[-360:])
 assert t.returncode==0 and "Ran 20 tests" in t.stderr,t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B05f","status":"CRC_SHA256_FULL_EXTRACTION_20_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,
 "crc_pass":True,"per_member_sha256_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":20,"accepted_rules_sha256":A["rules_sha256"],
 "historical_records_if_published":86,
 "independent_human_personality_matches":0,
 "independent_criminal_or_medical_classification":0,
 "empirical_validations":0,"runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
