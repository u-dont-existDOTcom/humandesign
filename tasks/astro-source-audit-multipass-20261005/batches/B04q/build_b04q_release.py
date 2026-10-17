from pathlib import Path
import json,hashlib,tempfile,subprocess,zipfile
B=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=subprocess.run(["xdg-user-dir","DOWNLOAD"],text=True,capture_output=True)
D=Path(r.stdout.strip()) if r.returncode==0 and r.stdout.strip() else Path.home()/"Téléchargements"
D.mkdir(exist_ok=True,parents=True)
OUT=D/"Astrology-Lilly-Chapter-XCVII-Release-Documentary-20261017.zip"
names=["SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json","SOURCE_FIRST_CLAUSES_DRAFT.json",
"ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json","SOURCE_WINDOW_MANIFEST.json",
"UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
"RULES.json","SOURCE_ORDER.json","UNRESOLVED.json",
"ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","ACCEPTANCE.json",
"build_b04q_source_first.py","freeze_b04q_documentary_source.py",
"test_b04q_source_first.py","test_b04q_documentary_admission.py",
"build_b04q_release.py"]+[f"evidence/pdf_1647-{n}.jpg" for n in (505,506,507)]
assert all((B/f).is_file() for f in names)
m={f:{"bytes":(B/f).stat().st_size,"sha256":h(B/f)} for f in names}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in names:z.write(B/f,"B04q/"+f)
 z.writestr("B04q/SHA256_MANIFEST.json",json.dumps(m,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory() as tmp:
 assert z.testzip() is None;z.extractall(tmp);E=Path(tmp)/"B04q"
 assert json.loads((E/"SHA256_MANIFEST.json").read_text())==m
 for f,v in m.items():assert h(E/f)==v["sha256"] and (E/f).stat().st_size==v["bytes"]
 t=subprocess.run(["python3","-m","unittest","-q","test_b04q_source_first","test_b04q_documentary_admission"],cwd=E,capture_output=True,text=True)
 assert t.returncode==0 and "Ran 14 tests" in t.stderr,t.stderr
a=json.loads((B/"ACCEPTANCE.json").read_text());assert h(B/"RULES.json")==a["rules_sha256"]
rec={"batch":"B04q","status":"CRC_SHA256_FULL_EXTRACT_14_TESTS",
 "owner_download_path":str(OUT),"archive_sha256":h(OUT),
 "archive_bytes":OUT.stat().st_size,"zip_crc_pass":True,"sha256_pass":True,
 "full_extract_pass":True,"extracted_tests_passed":14,
 "rules_sha256":a["rules_sha256"],"new_empirical_validations":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
