#!/usr/bin/env python3
"""ZIP exact 1647 LXXIX source with independent file replay, CRC and hashes."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
x=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/'Téléchargements'
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/'Astrology-Lilly-Chapter-LXXIX-Parsonage-Documentary-20261016.zip'
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
files=['build_b03y_source_first.py','test_b03y_source_first.py',
 'freeze_b03y_documentary_source.py','test_b03y_documentary_admission.py',
 'build_b03y_accepted_release.py','SOURCE_FIRST_CLAUSES_DRAFT.json',
 'ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json','SOURCE_WINDOW_MANIFEST.json',
 'UNRESOLVED_SOURCE_LIMITS.json','CLAIM_LEDGER.json',
 'SOURCE_FIRST_IMAGE_AUDIT_20261016.md','RULES.json','SOURCE_ORDER.json',
 'UNRESOLVED.json','ACCEPTANCE.json','ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'evidence/pdf_1647-471.jpg','evidence/pdf_1647-472.jpg','evidence/pdf_1647-473.jpg']
assert all((B/f).is_file() for f in files)
members={f:{'bytes':(B/f).stat().st_size,'sha256':H(B/f)} for f in files}
manifest={'batch':'B03y','kind':'ORIGINAL_AUTHOR-REPORTED_HISTORICAL_PARSONAGE_CASE',
 'historical_documentary_source_units':41,'source_passages':7,'unresolved_issues':17,
 'unverified_author_retrospective_failure_outcomes':1,'independent_validations':0,'members':members}
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,'B03y/'+f)
 z.writestr('B03y/RELEASE_SHA256_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix='lilly-b03y-') as tmp:
 assert z.testzip() is None
 z.extractall(tmp);p=Path(tmp)/'B03y'
 assert json.loads((p/'RELEASE_SHA256_MANIFEST.json').read_text())==manifest
 for f,v in members.items():
  assert H(p/f)==v['sha256'] and (p/f).stat().st_size==v['bytes'],f
 t=subprocess.run(['python3','-m','unittest','-q',
  'test_b03y_source_first','test_b03y_documentary_admission'],
  cwd=p,capture_output=True,text=True)
 print(t.stderr[-350:])
 assert t.returncode==0 and 'Ran 14 tests' in t.stderr
A=json.loads((B/'ACCEPTANCE.json').read_text())
assert H(B/'RULES.json')==A['rules_sha256']
receipt={'batch':'B03y','status':'CRC_SHA256_FULL_EXTRACT_14_TEST_REPLAY_PASSED',
 'owner_download_path':str(OUT),'archive_sha256':H(OUT),'archive_bytes':OUT.stat().st_size,
 'zip_crc_pass':True,'member_hashes_pass':True,'full_extraction_pass':True,
 'extracted_tests_passed':14,'extracted_exit_code':t.returncode,
 'accepted_rules_sha256':A['rules_sha256'],'source_records_if_published':41,
 'unverified_author_outcome_report':1,'independent_case_validation_count':0,
 'new_empirical_validations':0,'remote_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
