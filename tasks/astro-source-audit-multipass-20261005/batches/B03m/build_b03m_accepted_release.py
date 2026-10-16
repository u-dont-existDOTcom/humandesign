#!/usr/bin/env python3
"""Chapter LXVII historical source archive: CRC, SHA, extraction and test replay."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
q=subprocess.run(["xdg-user-dir","DOWNLOAD"],capture_output=True,text=True)
DEST=Path(q.stdout.strip()) if q.returncode==0 and q.stdout.strip() else Path.home()/"Téléchargements"
DEST.mkdir(parents=True,exist_ok=True)
OUT=DEST/"Astrology-Lilly-Chapter-LXVII-Documentary-20261016.zip"
sha=lambda b:hashlib.sha256(b).hexdigest()
FILES=[
 "build_b03m_source_first.py","test_b03m_source_first.py",
 "freeze_b03m_documentary_source.py","test_b03m_documentary_admission.py",
 "build_b03m_accepted_release.py",
 "SOURCE_FIRST_CLAUSES_DRAFT.json","ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json",
 "SOURCE_ORDER_DRAFT.json","SOURCE_WINDOW_MANIFEST.json",
 "UNRESOLVED_SOURCE_LIMITS.json","CLAIM_LEDGER.json",
 "SOURCE_FIRST_IMAGE_AUDIT_20261016.md",
 "RULES.json","SOURCE_ORDER.json","UNRESOLVED.json",
 "CLAIM_LEDGER_ACCEPTED_LOCAL.json","ACCEPTANCE.json",
 "ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json",
 "SOURCE_WINDOW_PROVISIONAL.json","RECOVERY_TASK_STATUS.json",
 "LXVII_ORIGINAL_SOURCE_SCOPE_PROVISIONAL_20261016.md",
 "PROVISIONAL_SCOPE_RELEASE_RECEIPT_20261016.json",
 "freeze_source_window_provisional.py","test_b03m_original_scope.py",
 "build_source_scope_provisional_zip.py"
]+[f"evidence/pdf_1647-{n}.jpg" for n in range(438,447)]
assert len(FILES)==34 and all((B/f).is_file() for f in FILES)
manifest={"batch":"B03m","kind":"ORIGINAL_1647_HISTORICAL_SOURCE_ONLY_NOT_REAL_WORLD_PROGNOSIS",
  "original_pdf_pages":list(range(438,447)),
  "accepted_local_source_annotations":186,
  "accepted_local_original_source_passages":38,
  "unresolved_original_limits":31,
  "original_sourced_case_outcomes_verified_independently":0,
  "new_empirically_validated_astrological_outcomes":0,
  "runtime_rule_promotions":0,"remote_publication_pending":True,
  "members":{f:{"sha256":sha((B/f).read_bytes()),"bytes":(B/f).stat().st_size} for f in FILES}}
with zipfile.ZipFile(OUT,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
    for name in sorted(FILES):z.write(B/name,arcname="B03m/"+name)
    z.writestr("B03m/RELEASE_SHA256_MANIFEST.json",
               json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")
with zipfile.ZipFile(OUT,"r") as z,tempfile.TemporaryDirectory(prefix="lilly-b03m-accepted-") as td:
    assert z.testzip() is None
    z.extractall(td)
    E=Path(td)/"B03m"
    assert json.loads((E/"RELEASE_SHA256_MANIFEST.json").read_text())==manifest
    for n,item in manifest["members"].items():
        raw=(E/n).read_bytes()
        assert len(raw)==item["bytes"] and sha(raw)==item["sha256"],n
    run=subprocess.run(["python3","-m","unittest","-q",
       "test_b03m_source_first","test_b03m_documentary_admission"],
       cwd=E,capture_output=True,text=True)
    print(run.stderr[-1100:])
    assert run.returncode==0 and "Ran 25 tests" in run.stderr
receipt={"batch":"B03m",
 "status":"ORIGINAL_DOCUMENTARY_CRC_SHA256_EXTRACTION_AND_TEST_REPLAY_VERIFIED",
 "owner_os_download_path":str(OUT),
 "accepted_archive_sha256":sha(OUT.read_bytes()),
 "accepted_archive_bytes":OUT.stat().st_size,
 "zip_crc_pass":True,"member_sha256_and_size_match":True,
 "actual_extraction_pass":True,"extracted_source_tests_passed":25,
 "extracted_test_exit_code":run.returncode,
 "rules_sha256":manifest["members"]["RULES.json"]["sha256"],
 "historical_source_units_admitted_locally":186,
 "independently_verified_person_outcomes":0,
 "new_empirically_validated_predictions":0,
 "new_runtime_rules":0,"canonical_remote_published":False}
(B/"SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json").write_text(
  json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(receipt,indent=2,ensure_ascii=False))
