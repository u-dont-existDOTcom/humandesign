#!/usr/bin/env python3
"""Archive complete original first-edition source window without claiming rules admitted."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Accident-Rectification-Original-Source-Window-20261017.zip"
files=["SOURCE_WINDOW_PROVISIONAL_20261017.json","PARENT_INDEX_BEFORE_B04y.json",
 "ORIGINAL_ACCIDENT_RECTIFICATION_BOUNDARY_NOTES_20261017.md",
 "prepare_b04y_source_window.py","test_b04y_original_source_window.py",
 "build_b04y_source_window_release.py"]+[f"evidence/pdf_1647-{n}.jpg" for n in range(541,555)]
assert all((B/f).is_file() for f in files)
m={"batch":"B04y","kind":"PROVISIONAL_ORIGINAL_SOURCE_PAGES_NOT_FORMAL_RULES",
 "body_pages":[541,553],"next_heading_on_shared_page":553,
 "source_images_complete":14,"records_newly_admitted":0,
 "empirical_validations":0,
 "members":{f:{"bytes":(B/f).stat().st_size,"sha256":H(B/f)} for f in files}}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,"B04y/"+f)
 z.writestr("B04y/RELEASE_SHA256_MANIFEST.json",json.dumps(m,indent=2)+"\n")
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix="Lilly-Accidents-window-") as tmp:
 assert z.testzip() is None;z.extractall(tmp);E=Path(tmp)/"B04y"
 assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==m
 for f,v in m["members"].items():
  assert H(E/f)==v["sha256"] and (E/f).stat().st_size==v["bytes"],f
 t=subprocess.run(["python3","-m","unittest","-q","test_b04y_original_source_window"],cwd=E,capture_output=True,text=True)
 print(t.stderr[-230:])
 assert t.returncode==0 and "Ran 5 tests" in t.stderr
receipt={"batch":"B04y","status":"SOURCE_WINDOW_CRC_SHA256_FULL_EXTRACT_5_TESTS_PASSED",
 "owner_download_path":str(OUT),"owner_archive_sha256":H(OUT),
 "archive_bytes":OUT.stat().st_size,"crc_pass":True,"all_member_sha256_pass":True,
 "full_extraction_pass":True,"extracted_tests_passed":5,
 "original_images_preserved":14,"new_accepted_records":0,
 "empirical_validations":0,"remote_published":False}
(B/"SOURCE_WINDOW_ARCHIVE_RECEIPT_20261017.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
