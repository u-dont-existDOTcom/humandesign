#!/usr/bin/env python3
"""Original 1647 chapter: deterministic archive replay and per-member SHA."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-XCIII-Witchcraft-Historical-20261017.zip"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files=["SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json",
 "build_b04m_source_first.py","test_b04m_source_first.py",
 "freeze_b04m_documentary_source.py","test_b04m_documentary_admission.py",
 "build_b04m_accepted_release.py",
 "SOURCE_FIRST_CLAUSES_DRAFT.json","ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",
 "SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json"]
files += [f"evidence/pdf_1647-{n}.jpg" for n in (498,499,500,501)]
assert all((B/f).is_file() for f in files)
members={f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}
manifest={"batch":"B04m","kind":"HISTORICAL_OCCULT_ASSERTIONS_NOT_TREATMENT",
 "first_edition_original_pages":[498,499,500,501],
 "documentary_source_annotations":75,"source_passage_groups":11,
 "unresolved_evidentiary_limits":28,
 "independently_authenticated_supernatural_causes":0,
 "independently_validated_treatments":0,
 "empirically_validated_astrology_predictions":0,
 "members":members}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04m/"+f)
 z.writestr("B04m/RELEASE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="lilly-b04m-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B04m"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,v in members.items():
  assert (E/f).stat().st_size==v["bytes"] and H(E/f)==v["sha256"],f
 t=subprocess.run(["python3","-m","unittest","-q",
       "test_b04m_source_first","test_b04m_documentary_admission"],
       cwd=E,capture_output=True,text=True)
 print(t.stderr[-350:])
 assert t.returncode==0 and "Ran 21 tests" in t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B04m","status":"CRC_SHA256_FULL_EXTRACTION_21_TESTS_VERIFIED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,"zip_crc_pass":True,
 "member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":21,"extracted_exit_code":t.returncode,
 "accepted_rules_sha256":A["rules_sha256"],
 "historical_source_annotations_if_published":75,
 "independent_verified_supernatural_causes":0,
 "independent_verified_treatments":0,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
print(json.dumps(rec,indent=2))
