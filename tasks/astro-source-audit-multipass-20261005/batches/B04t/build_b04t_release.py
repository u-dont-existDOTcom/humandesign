from pathlib import Path
import hashlib,json,zipfile,tempfile,subprocess
B=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
d=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
D=Path(d.stdout.strip()) if d.returncode==0 and d.stdout.strip() else Path.home()/"Téléchargements"
D.mkdir(parents=True,exist_ok=True)
OUT=D/"Astrology-Lilly-Planetary-Hour-Table-Original-Scans-20261017.zip"
files=sorted(set([p.name for p in B.glob("*.json")]+[p.name for p in B.glob("*.py")]+[p.name for p in B.glob("*.md")]+[f"evidence/pdf_1647-{n}.jpg" for n in range(508,517)]))
assert all((B/f).is_file() for f in files)
manifest={"batch":"B04t","scope":"8 original planetary-hour table leaves preserved by image; cells not fully digitized",
 "image_pages":list(range(508,517)),"historical_source_annotations":10,
 "numeric_cells_complete":False,"estimated_numeric_boundary_cells":1488,
 "empirical_validations":0,"members":{f:{"sha256":h(B/f),"bytes":(B/f).stat().st_size} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04t/"+f)
 z.writestr("B04t/FILE_HASH_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory() as t:
 assert z.testzip() is None;z.extractall(t);E=Path(t)/"B04t"
 assert json.loads((E/"FILE_HASH_MANIFEST.json").read_text())==manifest
 for f,x in manifest["members"].items():assert (E/f).stat().st_size==x["bytes"] and h(E/f)==x["sha256"]
 t=subprocess.run(["python3","-m","unittest","-q","test_b04t_table_source_first","test_b04t_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-320:])
 assert t.returncode==0 and "Ran 15 tests" in t.stderr
rec={"batch":"B04t","owner_download_path":str(OUT),"archive_sha256":h(OUT),
 "archive_bytes":OUT.stat().st_size,"archive_members":len(files),
 "crc_pass":True,"member_sha256_pass":True,"full_extract_pass":True,
 "archive_tests_replayed":15,"rules_sha256":h(B/"RULES.json"),
 "historical_annotations_if_published":10,"numeric_cells_fully_digitized":False,
 "new_empirical_validations":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
