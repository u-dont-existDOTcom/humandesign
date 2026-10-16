#!/usr/bin/env python3
"""Provisional original-image source window ZIP; no accepted historical rules."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
x=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-LXVII-Source-Scope-Provisional-20261016.zip"
SHA=lambda data:hashlib.sha256(data).hexdigest()
FILES=["LXVII_ORIGINAL_SOURCE_SCOPE_PROVISIONAL_20261016.md",
       "SOURCE_WINDOW_PROVISIONAL.json","freeze_source_window_provisional.py",
       "test_b03m_original_scope.py","build_source_scope_provisional_zip.py"]
FILES += [f"evidence/pdf_1647-{n}.jpg" for n in range(438,447)]
assert all((B/n).is_file() for n in FILES)
info={"batch":"B03m","status":"PROVISIONAL_SOURCE_WINDOW_ONLY_NOT_RULE_ACCEPTANCE",
 "original_pdf_pages":list(range(438,447)),
 "accepted_previous_lilly":3746,"retained_ptolemy":1066,
 "new_documentary_rule_units_accepted":0,"empirically_validated_predictions":0,
 "files":{n:{"bytes":(B/n).stat().st_size,"sha256":SHA((B/n).read_bytes())} for n in FILES}}
with zipfile.ZipFile(OUT,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
    for n in sorted(FILES):z.write(B/n,"B03m/"+n)
    z.writestr("B03m/PROVISIONAL_RELEASE_MANIFEST.json",json.dumps(info,indent=2)+"\n")
with zipfile.ZipFile(OUT,"r") as z,tempfile.TemporaryDirectory(prefix="lilly-b03m-scope-") as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    E=Path(tmp)/"B03m"
    assert json.loads((E/"PROVISIONAL_RELEASE_MANIFEST.json").read_text())==info
    for f,proof in info["files"].items():
        raw=(E/f).read_bytes()
        assert SHA(raw)==proof["sha256"] and len(raw)==proof["bytes"]
    test=subprocess.run(["python3","-m","unittest","-q","test_b03m_original_scope"],
        cwd=E,capture_output=True,text=True)
    print(test.stderr[-1000:])
    assert test.returncode==0 and "Ran 4 tests" in test.stderr
receipt={"batch":"B03m","status":"PROVISIONAL_SOURCE_SCOPE_ZIP_VERIFIED_NOT_ACCEPTED",
         "owner_download_path":str(OUT),"archive_sha256":SHA(OUT.read_bytes()),
         "archive_bytes":OUT.stat().st_size,"original_scan_count":9,
         "all_member_sha256_verified":True,"zip_crc_pass":True,
         "actual_extraction_pass":True,"extracted_scope_tests_passed":4,
         "accepted_historical_source_records_added":0,
         "new_empirical_predictions":0}
(B/"PROVISIONAL_SCOPE_RELEASE_RECEIPT_20261016.json").write_text(
   json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt,indent=2))
