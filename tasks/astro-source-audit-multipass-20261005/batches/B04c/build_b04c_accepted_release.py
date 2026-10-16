from pathlib import Path
import hashlib,json,tempfile,subprocess,zipfile
B=Path(__file__).resolve().parent
outcmd=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(outcmd.stdout.strip()) if outcmd.returncode==0 and outcmd.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-LXXXIII-Restoration-Documentary-20261016.zip"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files=["SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json","SOURCE_FIRST_CLAUSES_DRAFT.json",
 "ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json","SOURCE_WINDOW_MANIFEST.json",
 "SOURCE_ORDER_DRAFT.json","SOURCE_FIRST_IMAGE_AUDIT_20261016.md","UNRESOLVED_SOURCE_LIMITS.json",
 "CLAIM_LEDGER.json","RULES.json","SOURCE_ORDER.json","UNRESOLVED.json",
 "ACCEPTANCE.json","ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",
 "build_b04c_source_first.py","freeze_b04c_documentary_source.py",
 "test_b04c_source_first.py","test_b04c_documentary_admission.py",
 "build_b04c_accepted_release.py"]+[f"evidence/pdf_1647-{p}.jpg" for p in (482,483,484)]
assert all((B/f).is_file() for f in files)
members={f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}
manifest={"batch":"B04c","original_text_annotations":46,"source_spans":8,
 "independent_validated_restorations":0,"members":members}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04c/"+f)
 z.writestr("B04c/RELEASE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="lilly-b04c-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B04c"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,v in members.items():
  assert H(E/f)==v["sha256"] and (E/f).stat().st_size==v["bytes"]
 test=subprocess.run(["python3","-m","unittest","-q","test_b04c_source_first","test_b04c_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(test.stderr[-400:])
 assert test.returncode==0 and "Ran 16 tests" in test.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert H(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B04c","status":"CRC_SHA256_FULL_EXTRACT_16_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":H(OUT),"archive_bytes":OUT.stat().st_size,
 "zip_crc_pass":True,"member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":16,"accepted_rules_sha256":A["rules_sha256"],
 "documentary_records_if_published":46,"empirical_validations":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
