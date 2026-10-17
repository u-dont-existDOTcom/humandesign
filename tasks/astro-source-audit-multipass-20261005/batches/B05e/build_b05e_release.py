#!/usr/bin/env python3
"""Reproducible source-only 1647 temperament archive; no psychological validation."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
d=subprocess.run(["xdg-user-dir","DOWNLOAD"],text=True,capture_output=True)
DL=Path(d.stdout.strip()) if d.returncode==0 and d.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-CVII-Temperament-Original-20261017.zip"
files=["SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",
 "SOURCE_FIRST_CLAUSES_DRAFT.json","ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",
 "SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json",
 "build_b05e_source_first.py","test_b05e_source_first.py",
 "freeze_b05e_documentary_source.py","test_b05e_documentary_admission.py","build_b05e_release.py"]
files += [f"evidence/pdf_1647-{n}.jpg" for n in range(566,570)]
assert all((B/f).is_file() for f in files)
manifest={"batch":"B05e","kind":"ORIGINAL_1647_FOUR_HUMOUR_TESTIMONY_COUNTING_SOURCE_ONLY",
 "historical_annotations":59,"source_passages":9,"source_unresolved_limits":23,
 "original_images":[566,567,568,569],
 "conditional_malefic_Saturn_Mars_override":True,
 "equal_opposed_quality_cancellation":True,
 "conditional_threefold_lord_asc":True,
 "conditional_double_moon_asc":True,
 "independent_clinical_or_personality_accuracy":False,
 "members":{f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B05e/"+f)
 z.writestr("B05e/SOURCE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="Lilly-B05e-") as t:
 assert z.testzip() is None
 z.extractall(t);E=Path(t)/"B05e"
 assert json.loads((E/"SOURCE_SHA256_MANIFEST.json").read_text())==manifest
 for f,m in manifest["members"].items():
  assert H(E/f)==m["sha256"] and (E/f).stat().st_size==m["bytes"],f
 p=subprocess.run(["python3","-m","unittest","-q","test_b05e_source_first","test_b05e_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(p.stderr[-330:])
 assert p.returncode==0 and "Ran 19 tests" in p.stderr,p.stderr
a=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==a["rules_sha256"]
receipt={"batch":"B05e","status":"CRC_SHA256_FULL_EXTRACT_19_TESTS_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,"crc_pass":True,
 "all_member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":19,"accepted_rules_sha256":a["rules_sha256"],
 "source_documentary_records_if_published":59,
 "independent_personality_accuracy":0,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
