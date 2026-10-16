#!/usr/bin/env python3
"""Original-source LXXXI owner archive, CRC + exact hash + extracted-test replay."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-LXXXI-Philosophers-Stone-Documentary-20261016.zip"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files=["SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json",
 "build_b04a_source_first.py","test_b04a_source_first.py",
 "freeze_b04a_documentary_source.py","test_b04a_documentary_admission.py",
 "build_b04a_accepted_release.py",
 "SOURCE_FIRST_CLAUSES_DRAFT.json","ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",
 "SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","CLAIM_LEDGER.json",
 "SOURCE_FIRST_IMAGE_AUDIT_20261016.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json"]
files += [f"evidence/pdf_1647-{n}.jpg" for n in (476,477,478)]
assert all((B/f).is_file() for f in files)
members={f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}
m={"batch":"B04a","kind":"SOURCE_ONLY_ALCHEMY_AND_HEALTH_HISTORICAL_TEXT",
 "original_pdf_pages":[476,477,478],"historical_source_annotations":57,
 "source_spans":11,"unresolved_limits":20,
 "independent_proven_stones":0,"independent_medical_diagnoses":0,
 "independent_predictive_validations":0,"members":members}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04a/"+f)
 z.writestr("B04a/RELEASE_SHA256_MANIFEST.json",json.dumps(m,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="lilly-b04a-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B04a"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==m
 for f,v in members.items():
  assert (E/f).stat().st_size==v["bytes"] and H(E/f)==v["sha256"],f
 t=subprocess.run(["python3","-m","unittest","-q",
     "test_b04a_source_first","test_b04a_documentary_admission"],
     cwd=E,capture_output=True,text=True)
 print(t.stderr[-300:])
 assert t.returncode==0 and "Ran 17 tests" in t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
z={"batch":"B04a","status":"CRC_SHA256_FULL_EXTRACT_17_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,"zip_crc_pass":True,
 "member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":17,"extracted_exit_code":t.returncode,
 "accepted_rules_sha256":A["rules_sha256"],
 "source_records_if_published":57,"independent_elixir_successes":0,
 "independent_medical_cases":0,"new_empirical_validations":0,
 "remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").write_text(json.dumps(z,indent=2)+"\n")
print(json.dumps(z,indent=2))
