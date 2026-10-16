#!/usr/bin/env python3
"""Reproducible original-source-only historical chapter ZIP + extraction/test replay."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
result=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DL=Path(result.stdout.strip()) if result.returncode==0 and result.stdout.strip() else Path.home()/"Téléchargements"
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/"Astrology-Lilly-Chapter-LXVI-Reading-Siege-Documentary-20261016.zip"
SHA=lambda raw:hashlib.sha256(raw).hexdigest()
FILES=[
 "build_b03l_source_first.py","test_b03l_source_first.py",
 "freeze_b03l_documentary_source.py","test_b03l_documentary_admission.py",
 "build_b03l_accepted_release.py",
 "SOURCE_FIRST_CLAUSES_DRAFT.json","ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",
 "SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","CLAIM_LEDGER.json",
 "SOURCE_FIRST_IMAGE_AUDIT_20261016.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json",
 "CLAIM_LEDGER_ACCEPTED_LOCAL.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json"
]+[f"evidence/pdf_1647-{n}.jpg" for n in range(435,439)]
for f in FILES:assert (B/f).is_file(),f
metadata={"batch":"B03l","kind":"ORIGINAL_1647_DOCUMENTARY_SOURCE_NOT_EMPIRICAL_VALIDATION",
 "source_original_pdf_pages":[435,436,437,438],
 "documentary_source_annotations":76,"original_visual_source_passages":19,
 "source_original_year_chart":"1643","source_original_surrender_year_printed":"1644",
 "historically_corrob_surrender_year":"1643","surrender_missed_author_deadline_by_days":3,
 "independent_case_prediction_validation":0,"runtime_promotions":0,
 "remote_publication_pending":True,
 "files":{f:{"sha256":SHA((B/f).read_bytes()),"bytes":(B/f).stat().st_size} for f in FILES}}
with zipfile.ZipFile(OUT,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
    for f in sorted(FILES):z.write(B/f,arcname="B03l/"+f)
    z.writestr("B03l/RELEASE_SHA256_MANIFEST.json",
               json.dumps(metadata,indent=2,ensure_ascii=False)+"\n")
with zipfile.ZipFile(OUT,"r") as z,tempfile.TemporaryDirectory(prefix="lilly-b03l-extracted-") as tmp:
    assert z.testzip() is None
    z.extractall(tmp)
    E=Path(tmp)/"B03l"
    proof=json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())
    assert proof==metadata
    for name,item in metadata["files"].items():
        raw=(E/name).read_bytes()
        assert len(raw)==item["bytes"] and SHA(raw)==item["sha256"],name
    run=subprocess.run(["python3","-m","unittest","-q",
                        "test_b03l_source_first","test_b03l_documentary_admission"],
                       cwd=E,capture_output=True,text=True)
    print(run.stderr[-1800:])
    assert run.returncode==0 and "Ran 26 tests" in run.stderr
receipt={"batch":"B03l",
         "status":"ACCEPTED_SOURCE_ZIP_CRC_SHA256_EXTRACTED_26_TESTS_REPLAY_VERIFIED",
         "download_path":str(OUT),
         "release_zip_sha256":SHA(OUT.read_bytes()),
         "release_zip_bytes":OUT.stat().st_size,
         "zip_crc_pass":True,"all_member_hashes_pass":True,
         "real_extraction_pass":True,
         "extracted_source_tests_passed":26,
         "extracted_test_exit_code":run.returncode,
         "accepted_rules_sha256":metadata["files"]["RULES.json"]["sha256"],
         "source_original_surrender_year_printed":"1644",
         "independent_historical_surrender_year":"1643",
         "historical_documentary_source_units":76,
         "new_empirically_validated_forecasts":0,
         "runtime_promotions":0,"canonical_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").write_text(
    json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(receipt,indent=2,ensure_ascii=False))
