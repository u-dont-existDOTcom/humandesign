from pathlib import Path
import json,hashlib,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
res=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
D=Path(res.stdout.strip()) if res.returncode==0 and res.stdout.strip() else Path.home()/"Téléchargements"
D.mkdir(parents=True,exist_ok=True)
OUT=D/"Astrology-Lilly-BookIII-Introduction-Ascensions-Original-20261017.zip"
files=["SOURCE_GROUPS_PART1.json","SOURCE_GROUPS_PART2.json","SOURCE_GROUPS_PART3.json",
 "SOURCE_CLAIM_GROUPS_AUTHORING_20261017.json","SOURCE_FIRST_CLAUSES_DRAFT.json",
 "ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json","SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","SOURCE_FIRST_IMAGE_AUDIT_20261017.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json","CLAIM_LEDGER.json",
 "build_b04v_source_first.py","freeze_b04v_documentary_source.py",
 "test_b04v_source_first.py","test_b04v_documentary_admission.py","build_b04v_release.py"]
files.extend([f"evidence/pdf_1647-{n}.jpg" for n in range(521,535)])
assert all((B/f).is_file() for f in files)
m={"batch":"B04v","kind":"ORIGINAL_1647_BOOK_III_REFERENCE_TABLES_AND_INTRO_NOT_COMPLETE_DIGITIZATION",
 "source_documentary_annotations":71,"source_page_groups":14,
 "original_body_pages":list(range(521,534)),"next_heading_pdf":534,
 "original_numeric_tables_fully_machine_digitized":False,
 "original_arithmetic_ascendant_discrepancy_arcminutes":120,
 "independent_birth_time_predictions_verified":0,"members":{f:{"bytes":(B/f).stat().st_size,"sha256":h(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04v/"+f)
 z.writestr("B04v/RELEASE_SHA256_MANIFEST.json",json.dumps(m,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="Lilly-III-Intro-") as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/"B04v"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==m
 for f,q in m["members"].items():
  assert h(E/f)==q["sha256"] and (E/f).stat().st_size==q["bytes"]
 t=subprocess.run(["python3","-m","unittest","-q",
 "test_b04v_source_first","test_b04v_documentary_admission"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-500:])
 assert t.returncode==0 and "Ran 20 tests" in t.stderr,t.stderr
A=json.loads((B/"ACCEPTANCE.json").read_text())
assert h(B/"RULES.json")==A["rules_sha256"]
rec={"batch":"B04v","status":"CRC_SHA256_FULL_EXTRACT_20_TESTS_VERIFIED",
 "owner_download_path":str(OUT),"archive_sha256":h(OUT),
 "archive_bytes":OUT.stat().st_size,"zip_crc_pass":True,
 "member_hashes_pass":True,"full_extraction_pass":True,
 "extracted_tests_passed":20,"accepted_rules_sha256":A["rules_sha256"],
 "documentary_records_if_published":71,
 "original_numeric_table_cells_digitized":False,
 "original_numeric_inconsistency_preserved":True,
 "independent_birth_time_outcomes":0,"new_empirical_validations":0,
 "runtime_promotions":0,"remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261017.json").write_text(json.dumps(rec,indent=2)+"\n")
print(json.dumps(rec,indent=2))
