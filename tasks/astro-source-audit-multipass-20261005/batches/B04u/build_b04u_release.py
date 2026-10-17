from pathlib import Path
import json,hashlib,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
D=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements";D.mkdir(parents=True,exist_ok=True)
OUT=D/"Astrology-Lilly-Chapter-XCVIII-Planetary-Hours-Method-20261017.zip"
files=sorted(set([p.name for p in B.glob("*.json")]+[p.name for p in B.glob("*.py")]+[p.name for p in B.glob("*.md")]+[f"evidence/pdf_1647-{k}.jpg" for k in range(516,522)]))
files=[f for f in files if not f.startswith(("SOURCE_DOCUMENTARY_RELEASE_RECEIPT_", "CANONICAL_INDEX_PREPARE_RECEIPT_", "PUBLICATION_RECEIPT_", "CONTINUATION_HANDOFF_"))]
assert all((B/f).is_file() for f in files)
manifest={"batch":"B04u","kind":"FIRST_EDITION_HISTORICAL_PLANETARY_HOUR_METHOD_NOT_HUMAN_PREDICTIVE",
 "historical_records":114,"source_groups":13,"original_body_pages":[516,517,518,519,520],
 "following_book_title_pdf":521,"worked_clock_examples_internal_replay":3,
 "prior_table_numeric_cells_fully_digitized":False,
 "empirically_validated_predictions":0,"members":{f:{"bytes":(B/f).stat().st_size,"sha256":h(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04u/"+f)
 z.writestr("B04u/RELEASE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="Lilly-finalmethod-") as tmp:
 assert z.testzip() is None;z.extractall(tmp);E=Path(tmp)/"B04u"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
 for f,v in manifest["members"].items():assert h(E/f)==v["sha256"] and (E/f).stat().st_size==v["bytes"]
 t=subprocess.run(["python3","-m","unittest","-q","test_b04u_source_first","test_b04u_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-370:])
 assert t.returncode==0 and "Ran 20 tests" in t.stderr,t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert h(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B04u","status":"CRC_SHA256_FULL_EXTRACT_20_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":h(OUT),
 "archive_bytes":OUT.stat().st_size,"archive_members":len(files),
 "crc_pass":True,"member_hashes_pass":True,
 "full_extraction_pass":True,"archive_tests_replayed":20,
 "accepted_rules_sha256":A["rules_sha256"],
 "historical_documentary_records_if_published":114,
 "numeric_table_fully_machine_verified":False,
 "new_empirical_validations":0,"runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
