#!/usr/bin/env python3
"""Archival first-edition Hyleg/Anareta/Alcochodon source bundle, not a mortality calculator."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
d=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(d.stdout.strip()) if d.returncode==0 and d.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-CV-Hyleg-Historical-Source-20261017.zip"
files=[
 "SOURCE_GROUPS_PART1_20261017.json","SOURCE_GROUPS_PART2_20261017.json",
 "SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",
 "SOURCE_FIRST_CLAUSES_DRAFT.json","ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",
 "SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json",
 "build_b05c_source_first.py","test_b05c_source_first.py",
 "freeze_b05c_documentary_source.py","test_b05c_documentary_admission.py",
 "build_b05c_release.py"]
files.extend(f"evidence/pdf_1647-{p}.jpg" for p in range(561,567))
assert all((B/f).is_file() for f in files)
manifest={"batch":"B05c","kind":"FIRST_EDITION_1647_HYLEG_ALCOCHODON_HISTORICAL_ONLY",
 "original_annotations":74,"source_passages":7,
 "original_body_pdf_pages":[561,562,563,564,565],
 "following_lord_geniture_heading_page":565,
 "author_explicit_uncertainty_about_rules":True,
 "human_survival_predictions_validated":False,
 "new_empirical_validations":0,
 "members":{f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B05c/"+f)
 z.writestr("B05c/RELEASE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="lilly-b05c-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B05c"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,m in manifest["members"].items():
  assert H(E/f)==m["sha256"] and (E/f).stat().st_size==m["bytes"],f
 t=subprocess.run(["python3","-m","unittest","-q",
 "test_b05c_source_first","test_b05c_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-400:])
 assert t.returncode==0 and "Ran 19 tests" in t.stderr,t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
receipt={"batch":"B05c","status":"CRC_SHA256_FULL_EXTRACTION_19_REPLAYED_TESTS",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),"archive_bytes":OUT.stat().st_size,
 "crc_pass":True,"member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":19,"accepted_rules_sha256":A["rules_sha256"],
 "historical_documentary_records_if_published":74,
 "independent_mortality_predicted_successes":0,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
