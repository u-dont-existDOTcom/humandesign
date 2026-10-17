from pathlib import Path
import json,hashlib,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
p=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(p.stdout.strip()) if p.returncode==0 and p.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(exist_ok=True,parents=True)
OUT=DL/"Astrology-Lilly-Friends-Love-Original-20261016.zip"
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files=["SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json","SOURCE_FIRST_CLAUSES_DRAFT.json",
 "ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261016.md",
 "CLAIM_LEDGER.json","RULES.json","SOURCE_ORDER.json","UNRESOLVED.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","ACCEPTANCE.json",
 "build_b04i_source_first.py","accept_b04i.py","test_b04i_documentary.py",
 "build_b04i_release.py","evidence/pdf_1647-493.jpg","evidence/pdf_1647-494.jpg"]
assert all((B/f).is_file() for f in files)
members={f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04i/"+f)
 z.writestr("B04i/RELEASE_SHA256_MANIFEST.json",json.dumps(members,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory() as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B04i"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==members
 for f,m in members.items():assert H(E/f)==m["sha256"] and (E/f).stat().st_size==m["bytes"]
 t=subprocess.run(["python3","-m","unittest","-q","test_b04i_documentary"],cwd=E,capture_output=True,text=True)
 assert t.returncode==0 and "Ran 7 tests" in t.stderr,t.stderr
rec={"batch":"B04i","owner_download_path":str(OUT),"archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,"zip_crc_pass":True,"member_hash_pass":True,
 "full_extract_pass":True,"extracted_tests_passed":7,"accepted_rules_sha256":H(B/"RULES.json"),
 "new_empirical_validations":0}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
