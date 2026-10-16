#!/usr/bin/env python3
"""Original-source Chapter LXVIII ZIP, with CRC/sha/extraction and tests replay."""
from pathlib import Path
import zipfile,hashlib,json,tempfile,subprocess
B=Path(__file__).resolve().parent
q=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(q.stdout.strip()) if q.returncode==0 and q.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-LXVIII-Wife-Portion-Documentary-20261016.zip"
H=lambda x:hashlib.sha256(x).hexdigest()
files=sorted(p.relative_to(B).as_posix() for p in B.iterdir()
 if p.is_file() and p.suffix in (".json",".md",".py")
 and p.name not in ("SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json","PUBLICATION_RECEIPT_20261016.json"))
files += [f"evidence/pdf_1647-{n}.jpg" for n in (446,447,448)]
required=["RULES.json","ACCEPTANCE.json","SOURCE_FIRST_CLAUSES_DRAFT.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",
 "test_b03n_source_first.py","test_b03n_documentary_admission.py"]
assert all(x in files for x in required)
assert all((B/f).is_file() for f in files)
manifest={"batch":"B03n","kind":"ORIGINAL_1647_DOCUMENTARY_NO_INDEPENDENT_PAYMENT_CASE",
 "source_original_pdf_pages":[446,447,448],
 "locally_accepted_historical_annotations":44,
 "original_visual_passages":11,
 "independent_estate_cases":0,
 "empirical_astrological_predictions_validated":0,
 "runtime_rule_promotions":0,
 "files":{f:{"sha256":H((B/f).read_bytes()),"bytes":(B/f).stat().st_size} for f in files}}
with zipfile.ZipFile(OUT,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for name in files:z.write(B/name,arcname="B03n/"+name)
 z.writestr("B03n/RELEASE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT,"r") as z,tempfile.TemporaryDirectory(prefix="lilly-b03n-accepted-") as td:
 assert z.testzip() is None
 z.extractall(td);E=Path(td)/"B03n"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,v in manifest["files"].items():
  raw=(E/f).read_bytes()
  assert len(raw)==v["bytes"] and H(raw)==v["sha256"]
 run=subprocess.run(["python3","-m","unittest","-q","test_b03n_source_first",
   "test_b03n_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(run.stderr[-950:])
 assert run.returncode==0 and "Ran 16 tests" in run.stderr
receipt={"batch":"B03n","status":"ZIP_CRC_SHA256_EXTRACTED_16_TEST_REPLAY_VERIFIED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT.read_bytes()),
 "archive_bytes":OUT.stat().st_size,"zip_crc_pass":True,
 "member_sha256_pass":True,"actual_extraction_pass":True,
 "replay_tests_passed":16,"replay_test_exit_code":run.returncode,
 "source_rules_sha256":manifest["files"]["RULES.json"]["sha256"],
 "new_documentary_records_if_published":44,
 "independent_payment_cases":0,"new_empirical_validations":0,
 "new_runtime_rules":0,"canonical_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").write_text(
 json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
