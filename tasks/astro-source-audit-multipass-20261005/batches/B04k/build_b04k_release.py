from pathlib import Path
import hashlib,json,tempfile,subprocess,zipfile
B=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(p.stdout.strip()) if p.returncode==0 and p.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(exist_ok=True,parents=True)
OUT=DL/"Astrology-Lilly-Imprisonment-Original-20261016.zip"
files=["SOURCE_CLAIM_GROUPS_AUTHORING_20261016.json","SOURCE_FIRST_CLAUSES_DRAFT.json",
"ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json","SOURCE_WINDOW_MANIFEST.json","UNRESOLVED_SOURCE_LIMITS.json",
"SOURCE_FIRST_IMAGE_AUDIT_20261016.md","RULES.json","SOURCE_ORDER.json",
"ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","ACCEPTANCE.json",
"build_accept_b04k.py","test_b04k_documentary.py","build_b04k_release.py",
"evidence/pdf_1647-495.jpg","evidence/pdf_1647-496.jpg","evidence/pdf_1647-497.jpg"]
assert all((B/f).is_file() for f in files)
m={f:{"bytes":(B/f).stat().st_size,"sha256":h(B/f)} for f in files}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04k/"+f)
 z.writestr("B04k/RELEASE_SHA256_MANIFEST.json",json.dumps(m,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory() as tmp:
 assert z.testzip() is None;z.extractall(tmp);E=Path(tmp)/"B04k"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==m
 for f,v in m.items():assert h(E/f)==v["sha256"] and (E/f).stat().st_size==v["bytes"]
 t=subprocess.run(["python3","-m","unittest","-q","test_b04k_documentary"],cwd=E,capture_output=True,text=True)
 assert t.returncode==0 and "Ran 8 tests" in t.stderr,t.stderr
rec={"batch":"B04k","owner_download_path":str(OUT),"archive_sha256":h(OUT),
"archive_bytes":OUT.stat().st_size,"zip_crc_pass":True,"member_hashes_pass":True,
"full_extract_pass":True,"replayed_tests":8,"rules_sha256":h(B/"RULES.json"),
"new_empirical_validations":0}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
