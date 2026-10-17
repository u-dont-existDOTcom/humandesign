from pathlib import Path
import json,hashlib,subprocess,zipfile,tempfile
B=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
D=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements";D.mkdir(parents=True,exist_ok=True)
OUT=D/"Astrology-Lilly-Chapter-XCIX-Trutine-Hermes-Rectification-20261017.zip"
files=sorted(set([p.name for p in B.glob("*.json")]+[p.name for p in B.glob("*.py")]+[p.name for p in B.glob("*.md")]+[f"evidence/pdf_1647-{k}.jpg" for k in range(534,540)]))
files=[p for p in files if not p.startswith(("SOURCE_DOCUMENTARY_RELEASE_RECEIPT_","CANONICAL_INDEX_PREPARE_RECEIPT_","PUBLICATION_RECEIPT_","CONTINUATION_HANDOFF_"))]
assert all((B/p).is_file() for p in files)
manifest={"batch":"B04w","kind":"SOURCE_ONLY_TRUTINE_HERMES_CONCEPTION_AND_BIRTH_RECTIFICATION",
 "historical_documentary_records":99,"source_spans":13,"retained_uncertainties":27,
 "source_Trutine_exact_degree_often_fails":True,
 "source_author_dismisses_alternate_conception_hour_formula":True,
 "gestation_numeric_table_fully_machine_digitized":False,
 "empirical_birth_time_accuracy_proven":False,
 "members":{p:{"bytes":(B/p).stat().st_size,"sha256":h(B/p)} for p in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for p in files:z.write(B/p,"B04w/"+p)
 z.writestr("B04w/SOURCE_SHA256_MANIFEST.json",json.dumps(manifest,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="Lilly-Hermes-") as tmp:
 assert z.testzip() is None;z.extractall(tmp);E=Path(tmp)/"B04w"
 assert json.loads((E/"SOURCE_SHA256_MANIFEST.json").read_text())==manifest
 for p,v in manifest["members"].items():assert h(E/p)==v["sha256"] and (E/p).stat().st_size==v["bytes"]
 t=subprocess.run(["python3","-m","unittest","-q","test_b04w_source_first","test_b04w_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-350:])
 assert t.returncode==0 and "Ran 20 tests" in t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert h(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B04w","status":"CRC_SHA256_FULL_EXTRACTION_20_TEST_REPLAY_PASSED",
 "owner_download_path":str(OUT),"archive_sha256":h(OUT),
 "archive_bytes":OUT.stat().st_size,"member_count":len(files),
 "crc_pass":True,"sha256_members_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":20,"accepted_rules_sha256":A["rules_sha256"],
 "historical_records_if_published":99,"independently_validated_birth_time_accuracies":0,
 "numeric_gestation_table_complete":False,"empirical_predictions":0,
 "runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
