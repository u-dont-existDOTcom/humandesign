from pathlib import Path
import hashlib,json,tempfile,zipfile,subprocess
B=Path(__file__).resolve().parent
r=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
D=Path(r.stdout.strip() if r.returncode==0 and r.stdout.strip() else Path.home()/"Téléchargements")
D.mkdir(exist_ok=True,parents=True)
out=D/"Astrology-Lilly-XCVI-Original-20261017.zip"
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files=[p.relative_to(B).as_posix() for p in B.glob("*.json")]
files += [p.name for p in B.glob("*.py")]
files += [p.name for p in B.glob("*.md")]
files += ["evidence/pdf_1647-504.jpg","evidence/pdf_1647-505.jpg"]
files=sorted(set(files))
m={f:{"sha256":h(B/f),"bytes":(B/f).stat().st_size} for f in files}
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04p/"+f)
 z.writestr("B04p/FILE_HASH_MANIFEST.json",json.dumps(m,indent=2)+"\n")
with zipfile.ZipFile(out) as z,tempfile.TemporaryDirectory() as t:
 assert z.testzip() is None;z.extractall(t)
 root=Path(t)/"B04p"
 for f,item in m.items():
  assert h(root/f)==item["sha256"] and (root/f).stat().st_size==item["bytes"]
 p=subprocess.run(["python3","-m","unittest","-q","test_b04p_source_first",
 "test_b04p_documentary_admission"],cwd=root,capture_output=True,text=True)
 print(p.stderr[-350:])
 assert p.returncode==0 and "Ran 18 tests" in p.stderr
a=json.loads((B/"ACCEPTANCE.json").read_text())
receipt={"batch":"B04p","status":"ARCHIVE_CRC_SHA256_EXTRACTED_18_TESTS_PASSED",
 "owner_download_path":str(out),"archive_sha256":h(out),
 "archive_bytes":out.stat().st_size,"members_count":len(files),
 "crc_pass":True,"member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":18,"accepted_rules_sha256":h(B/"RULES.json"),
 "historical_documentary_records":42,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
assert receipt["accepted_rules_sha256"]==a["rules_sha256"]
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
