#!/usr/bin/env python3
"""Hermetic owner archive of historical Lord of Geniture source."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-CVI-Lord-Geniture-Original-20261017.zip"
files=["SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json","SOURCE_FIRST_CLAUSES_DRAFT.json",
 "ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json","SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json",
 "build_b05d_source_first.py","freeze_b05d_documentary_source.py",
 "test_b05d_source_first.py","test_b05d_documentary_admission.py","build_b05d_release.py"]
files += [f"evidence/pdf_1647-{n}.jpg" for n in [565,566,567]]
assert all((B/f).is_file() for f in files)
manifest={"batch":"B05d","kind":"HISTORICAL_1647_LORD_GENITURE_COMPETING_RULES_NOT_PERSONALITY_VALIDATION",
 "original_pdf_pages":[565,566,567],"documentary_records":32,
 "source_groups":6,"source_limitations":19,
 "Firmicus_method_source_rejected":True,
 "near_equal_planet_mix_not_numerically_specified":True,
 "independent_personality_validation":0,
 "members":{f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B05d/"+f)
 z.writestr("B05d/RELEASE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="Lilly-B05d-") as temp:
 assert z.testzip() is None
 z.extractall(temp);E=Path(temp)/"B05d"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,m in manifest["members"].items():
  assert H(E/f)==m["sha256"] and (E/f).stat().st_size==m["bytes"],f
 t=subprocess.run(["python3","-m","unittest","-q",
 "test_b05d_source_first","test_b05d_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-400:])
 assert t.returncode==0 and "Ran 17 tests" in t.stderr,t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
r={"batch":"B05d","status":"CRC_SHA256_FULL_EXTRACT_AND_17_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,"zip_crc_pass":True,
 "member_sha256_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":17,"accepted_rules_sha256":A["rules_sha256"],
 "historical_documentary_records_if_published":32,
 "independent_personality_predictive_validations":0,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(r,indent=2)+"\n")
print(json.dumps(r,indent=2))
