from pathlib import Path
import json,hashlib,tempfile,subprocess,zipfile
B=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
D=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements";D.mkdir(parents=True,exist_ok=True)
OUT=D/"Astrology-Lilly-Unnumbered-Essex-May1644-20261017.zip"
files=sorted(set([f.name for f in B.glob("*.json")]+[f.name for f in B.glob("*.py")]+[f.name for f in B.glob("*.md")]+["evidence/pdf_1647-507.jpg","evidence/pdf_1647-508.jpg"]))
assert all((B/p).is_file() for p in files)
m={p:{"sha256":h(B/p),"bytes":(B/p).stat().st_size} for p in files}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for p in files:z.write(B/p,"B04s/"+p)
 z.writestr("B04s/RELEASE_SHA256_MANIFEST.json",json.dumps(m,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="Lilly-Essex-") as tmp:
 assert z.testzip() is None;z.extractall(tmp);E=Path(tmp)/"B04s"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==m
 for p,v in m.items():assert h(E/p)==v["sha256"] and (E/p).stat().st_size==v["bytes"]
 t=subprocess.run(["python3","-m","unittest","-q","test_b04s_source_first","test_b04s_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-250:])
 assert t.returncode==0 and "Ran 14 tests" in t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert h(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B04s","status":"CRC_SHA256_FULL_EXTRACT_14_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":h(OUT),"archive_bytes":OUT.stat().st_size,
 "zip_crc_pass":True,"member_hashes_pass":True,"full_extract_pass":True,"replayed_tests":14,
 "accepted_rules_sha256":A["rules_sha256"],"documentary_records_if_published":43,
 "independent_military_event_corroboration":True,"independent_astro_forecast_validation":False,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
