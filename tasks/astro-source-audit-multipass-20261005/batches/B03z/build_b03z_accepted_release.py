#!/usr/bin/env python3
"""Build and independently replay original 1647 LXXX source-only archive."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-LXXX-Presbytery-Documentary-20261016.zip"
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
files=[
 "SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json",
 "SOURCE_WINDOW_PROVISIONAL_20261016.json",
 "ORIGINAL_BOUNDARY_NOTES_20261016.md",
 "build_b03z_source_first.py","test_b03z_source_first.py",
 "freeze_b03z_documentary_source.py","test_b03z_documentary_admission.py",
 "build_b03z_accepted_release.py",
 "SOURCE_FIRST_CLAUSES_DRAFT.json","ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",
 "SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","CLAIM_LEDGER.json",
 "SOURCE_FIRST_IMAGE_AUDIT_20261016.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json"]
files += [f"evidence/pdf_1647-{n}.jpg" for n in (473,474,475,476)]
assert all((B/f).is_file() for f in files)
members={f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}
manifest={"batch":"B03z","kind":"ORIGINAL_HISTORICAL_PRESBYTERY_DOCUMENTARY_ONLY",
 "documentary_source_annotations":82,"source_passages":13,
 "original_chapter_body_pdf_pages":[473,474,475,476],
 "following_chapter_navigation_only":2,
 "unresolved_source_qualifications":24,
 "independent_prediction_validations":0,"runtime_promotions":0,
 "members":members}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B03z/"+f)
 z.writestr("B03z/RELEASE_SHA256_MANIFEST.json",
            json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="lilly-b03z-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp); E=Path(tmp)/"B03z"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,v in members.items():
  assert (E/f).stat().st_size==v["bytes"] and H(E/f)==v["sha256"],f
 t=subprocess.run(["python3","-m","unittest","-q",
     "test_b03z_source_first","test_b03z_documentary_admission"],
     cwd=E,capture_output=True,text=True)
 print(t.stderr[-450:])
 assert t.returncode==0 and "Ran 19 tests" in t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B03z","status":"CRC_SHA256_FULL_EXTRACT_19_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,
 "zip_crc_pass":True,"member_hashes_pass":True,
 "full_extraction_pass":True,"extracted_tests_passed":19,
 "extracted_exit_code":t.returncode,
 "accepted_rules_sha256":A["rules_sha256"],
 "source_records_if_published":82,"source_passages":13,
 "independent_empirical_case_validations":0,
 "runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").write_text(
 json.dumps(rec,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(rec,indent=2,ensure_ascii=False))
