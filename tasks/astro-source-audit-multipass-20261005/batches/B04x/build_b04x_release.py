#!/usr/bin/env python3
"""Reproducible original Lilly Animodar source archive with extracted tests."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
d=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(d.stdout.strip()) if d.returncode==0 and d.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-C-Animodar-Original-Documentary-20261017.zip"
files=["SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",
 "SOURCE_FIRST_CLAUSES_DRAFT.json","ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",
 "SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json",
 "build_b04x_source_first.py","test_b04x_source_first.py",
 "freeze_b04x_documentary_source.py","test_b04x_documentary_admission.py",
 "build_b04x_release.py"]
files += [f"evidence/pdf_1647-{n}.jpg" for n in (539,540,541)]
assert all((B/f).is_file() for f in files)
manifest={"batch":"B04x","kind":"ORIGINAL_1647_HISTORICAL_ANIMODAR_AND_CAVEATS",
 "source_documentary_annotations":34,"source_page_groups":5,
 "original_pdf_pages":[539,540,541],
 "already_rectified_merchant_case_not_independent":True,
 "source_author_says_weaker_than_accident_rectification":True,
 "empirically_validated_predictions":0,
 "members":{f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04x/"+f)
 z.writestr("B04x/RELEASE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="Lilly-Animodar-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B04x"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,q in manifest["members"].items():
  assert (E/f).stat().st_size==q["bytes"] and H(E/f)==q["sha256"],f
 t=subprocess.run(["python3","-m","unittest","-q","test_b04x_source_first","test_b04x_documentary_admission"],
  cwd=E,capture_output=True,text=True)
 print(t.stderr[-350:])
 assert t.returncode==0 and "Ran 19 tests" in t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B04x","status":"CRC_SHA256_FULL_EXTRACT_19_TESTS_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,"zip_crc_pass":True,
 "member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":19,"accepted_rules_sha256":A["rules_sha256"],
 "documentary_records_if_published":34,
 "independent_birth_times_verified":0,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
