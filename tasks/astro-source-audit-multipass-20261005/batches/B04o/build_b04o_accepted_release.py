#!/usr/bin/env python3
"""First-edition clinical/occult historical case exact archival replay."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
d=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(d.stdout.strip()) if d.returncode==0 and d.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-XCV-Bewitched-Illness-Documentary-20261017.zip"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files=["SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",
 "build_b04o_source_first.py","test_b04o_source_first.py",
 "freeze_b04o_documentary_source.py","test_b04o_documentary_admission.py",
 "build_b04o_accepted_release.py","SOURCE_FIRST_CLAUSES_DRAFT.json",
 "ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
files += [f"evidence/pdf_1647-{n}.jpg" for n in (502,503,504)]
assert all((B/f).is_file() for f in files)
manifest={"batch":"B04o","kind":"HISTORICAL_UNVERIFIED_WITCHCRAFT_AND_MEDICAL_CASE",
 "original_source_pdf_pages":[502,503,504],"historical_annotations":53,
 "source_passages":10,"unresolved_evidence_limits":22,
 "author_source_witchcraft_verdict_negative":True,
 "author_source_syphilis_not_confirmed":True,
 "author_reported_three_week_recovery":True,
 "independently_verified_medical_outcomes":0,
 "new_empirical_astrology_validations":0,
 "members":{f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04o/"+f)
 z.writestr("B04o/RELEASE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="lilly-b04o-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B04o"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,m in manifest["members"].items():
  assert H(E/f)==m["sha256"] and (E/f).stat().st_size==m["bytes"],f
 t=subprocess.run(["python3","-m","unittest","-q",
  "test_b04o_source_first","test_b04o_documentary_admission"],
  cwd=E,capture_output=True,text=True)
 print(t.stderr[-360:])
 assert t.returncode==0 and "Ran 21 tests" in t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B04o","status":"CRC_SHA256_EXTRACTED_21_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,
 "zip_crc_pass":True,"member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":21,"extracted_exit_code":t.returncode,
 "accepted_rules_sha256":A["rules_sha256"],
 "documentary_records_if_published":53,
 "independent_medical_diagnoses":0,"independent_treatment_outcomes":0,
 "independent_supernatural_cause_identifications":0,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
