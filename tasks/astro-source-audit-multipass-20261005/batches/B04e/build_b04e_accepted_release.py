#!/usr/bin/env python3
"""Full original LXXXV archive with SHA256 member / CRC / extracted-test proof."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-LXXXV-Rupert-Essex-Documentary-20261016.zip"
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
files=["SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json",
 "build_b04e_source_first.py","test_b04e_source_first.py",
 "freeze_b04e_documentary_source.py","test_b04e_documentary_admission.py",
 "build_b04e_accepted_release.py","SOURCE_FIRST_CLAUSES_DRAFT.json",
 "ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json","SOURCE_ORDER_DRAFT.json",
 "SOURCE_WINDOW_MANIFEST.json","UNRESOLVED_SOURCE_LIMITS.json",
 "CLAIM_LEDGER.json","SOURCE_FIRST_IMAGE_AUDIT_20261016.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json"]+[f"evidence/pdf_1647-{n}.jpg" for n in (486,487,488,489)]
assert all((B/f).is_file() for f in files)
members={f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}
manifest={"batch":"B04e","kind":"ORIGINAL_AUTHOR_RETROSPECTIVE_RUPERT_ESSEX",
 "historical_documentary_units":72,"source_spans":11,"retained_uncertainties":25,
 "authorial_error_admitted":1,"pre_question_Edgehill_no_predictive_credit":True,
 "independently_verified_prediction_count":0,"members":members}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04e/"+f)
 z.writestr("B04e/RELEASE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="lilly-b04e-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B04e"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,v in members.items():
  assert (E/f).stat().st_size==v["bytes"] and H(E/f)==v["sha256"],f
 t=subprocess.run(["python3","-m","unittest","-q",
      "test_b04e_source_first","test_b04e_documentary_admission"],
      cwd=E,capture_output=True,text=True)
 print(t.stderr[-400:])
 assert t.returncode==0 and "Ran 17 tests" in t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B04e","status":"CRC_SHA256_FULL_EXTRACT_17_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,"zip_crc_pass":True,
 "member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":17,"extracted_exit_code":t.returncode,
 "accepted_rules_sha256":A["rules_sha256"],"historical_documentary_records_if_published":72,
 "authorial_partial_error_retained":True,"independent_predictive_validations":0,
 "remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
