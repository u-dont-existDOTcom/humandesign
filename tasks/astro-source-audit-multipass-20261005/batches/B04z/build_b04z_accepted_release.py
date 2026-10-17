#!/usr/bin/env python3
"""Hermetic 1647 Regiomontanus chart method source archive with independent replay."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
D=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements"
D.mkdir(parents=True,exist_ok=True)
OUT=D/"Astrology-Lilly-Chapter-CII-Regiomontanus-Original-20261017.zip"
files=[
 "SOURCE_GROUPS_PART1_20261017.json","SOURCE_GROUPS_PART2_20261017.json",
 "SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json","SOURCE_FIRST_CLAUSES_DRAFT.json",
 "ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json","SOURCE_ORDER_DRAFT.json",
 "SOURCE_WINDOW_MANIFEST.json","SOURCE_NUMERIC_ARITHMETIC_AUDIT_20261017.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json",
 "build_b04z_source_first.py","test_b04z_source_first.py",
 "freeze_b04z_documentary_source.py","test_b04z_documentary_admission.py",
 "build_b04z_accepted_release.py"]
files.extend(f"evidence/pdf_1647-{n}.jpg" for n in range(553,559))
assert all((B/f).is_file() for f in files)
m={"batch":"B04z","kind":"HISTORICAL_1647_REGIOMONTANUS_METHOD_UNVERIFIED_NATAL_OUTCOME",
 "historical_source_annotations":70,"original_source_passages":6,
 "original_pdf_pages":list(range(553,559)),
 "source_original_birth_time_verified":False,
 "solar_RA_MC_rounding_effect_seconds":10,
 "ascendant_approx_three_arcminutes_discrepancy":True,
 "entire_astrological_ephemeris_chart_parity":False,
 "empirical_predictions_validated":0,
 "members":{f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04z/"+f)
 z.writestr("B04z/RELEASE_SHA256_MANIFEST.json",json.dumps(m,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="Lilly-B04z-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B04z"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==m
 for f,q in m["members"].items():
  assert H(E/f)==q["sha256"] and (E/f).stat().st_size==q["bytes"],f
 t=subprocess.run(["python3","-m","unittest","-q",
 "test_b04z_source_first","test_b04z_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-350:])
 assert t.returncode==0 and "Ran 20 tests" in t.stderr,t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B04z","status":"CRC_SHA256_FULL_EXTRACTION_20_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,"zip_crc_pass":True,
 "member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":20,"accepted_rules_sha256":A["rules_sha256"],
 "historical_records_if_published":70,
 "independent_birth_times_verified":0,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
