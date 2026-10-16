from pathlib import Path
import hashlib,json,tempfile,subprocess,zipfile
B=Path(__file__).resolve().parent
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-LXXXIV-Professions-Documentary-20261016.zip"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files=["SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json","SOURCE_FIRST_CLAUSES_DRAFT.json",
 "ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json","SOURCE_WINDOW_MANIFEST.json",
 "SOURCE_ORDER_DRAFT.json","SOURCE_FIRST_IMAGE_AUDIT_20261016.md","UNRESOLVED_SOURCE_LIMITS.json",
 "CLAIM_LEDGER.json","RULES.json","SOURCE_ORDER.json","UNRESOLVED.json",
 "ACCEPTANCE.json","ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",
 "build_b04d_source_first.py","freeze_b04d_documentary_source.py",
 "test_b04d_source_first.py","test_b04d_documentary_admission.py",
 "build_b04d_accepted_release.py"]+[f"evidence/pdf_1647-{n}.jpg" for n in (484,485,486)]
assert all((B/f).is_file() for f in files)
members={f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}
m={"batch":"B04d","historical_profession_source_annotations":79,"source_spans":15,
 "original_Mars_Venus_glyph_verified":True,"independent_vocational_validations":0,"members":members}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04d/"+f)
 z.writestr("B04d/RELEASE_SHA256_MANIFEST.json",json.dumps(m,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="lilly-b04d-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B04d"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==m
 for f,v in members.items():
  assert H(E/f)==v["sha256"] and (E/f).stat().st_size==v["bytes"]
 t=subprocess.run(["python3","-m","unittest","-q","test_b04d_source_first","test_b04d_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-290:])
 assert t.returncode==0 and "Ran 15 tests" in t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B04d","status":"CRC_SHA256_FULL_EXTRACT_15_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),"archive_bytes":OUT.stat().st_size,
 "zip_crc_pass":True,"member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":15,"accepted_rules_sha256":A["rules_sha256"],
 "documentary_records_if_published":79,"independent_empirical_vocational_validations":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
