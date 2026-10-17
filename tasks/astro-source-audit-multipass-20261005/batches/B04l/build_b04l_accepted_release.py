#!/usr/bin/env python3
"""Original 1647 source archive; prove CRC/member hashes/full extraction/tests."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-XCII-Captive-Original-20261017.zip"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files=[
 "SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",
 "build_b04l_source_first.py","test_b04l_source_first.py",
 "freeze_b04l_documentary_source.py","test_b04l_documentary_admission.py",
 "build_b04l_accepted_release.py",
 "SOURCE_FIRST_CLAUSES_DRAFT.json","ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",
 "SOURCE_WINDOW_MANIFEST.json","SOURCE_ORDER_DRAFT.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json",
 "evidence/pdf_1647-497.jpg","evidence/pdf_1647-498.jpg"]
assert all((B/f).is_file() for f in files)
manifest={"batch":"B04l","kind":"ORIGINAL_HISTORICAL_CAPTIVE_SOURCE_NOT_EMPIRICAL",
 "documentary_annotations":31,"source_passages":5,
 "retained_uncertainties":19,
 "independent_captive_outcomes":0,"new_empirical_validations":0,
 "members":{f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04l/"+f)
 z.writestr("B04l/RELEASE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="lilly-b04l-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B04l"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,v in manifest["members"].items():
  assert (E/f).stat().st_size==v["bytes"] and H(E/f)==v["sha256"],f
 t=subprocess.run(["python3","-m","unittest","-q","test_b04l_source_first",
                   "test_b04l_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-350:])
 assert t.returncode==0 and "Ran 17 tests" in t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B04l","status":"CRC_SHA256_EXTRACTED_17_TEST_REPLAY_VERIFIED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,
 "zip_crc_pass":True,"member_hashes_pass":True,
 "full_extraction_pass":True,"extracted_tests_passed":17,
 "extracted_exit_code":t.returncode,"accepted_rules_sha256":A["rules_sha256"],
 "source_annotations_if_published":31,
 "independently_authenticated_captive_outcomes":0,
 "new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,indent=2))
