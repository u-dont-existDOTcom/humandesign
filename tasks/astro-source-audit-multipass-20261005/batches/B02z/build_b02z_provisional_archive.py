"""Create owner-local B02z PROVISIONAL package, replay tests after extracting.

No canonical acceptance, source index edit, actual trades, or third-party actions.
"""
import json,hashlib,zipfile,tempfile,subprocess,shutil
from pathlib import Path
B=Path(__file__).resolve().parent
DOWNLOADS=Path(subprocess.check_output(['xdg-user-dir','DOWNLOAD'],text=True).strip())
assert DOWNLOADS.is_dir()
NAME='Astrology-Lilly-Chapter-LIV-Source-First-Provisional-20261015.zip'
A=DOWNLOADS/NAME
REPORT=B/'PROVISIONAL_PACKET_RECEIPT_20261015.json'
assert not A.exists() and not REPORT.exists()
memberfiles=[
'build_b02z_source_first.py','SOURCE_WINDOW_MANIFEST.json',
'SOURCE_FIRST_CLAUSES_DRAFT.json','SOURCE_ORDER_DRAFT.json',
'build_b02z_coverage_and_limits.py','ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',
'UNRESOLVED_SOURCE_LIMITS.json','SOURCE_FIRST_IMAGE_AUDIT_20261015.md',
'test_b02z_source_first.py','CLAIM_LEDGER.json','HANDOFF_B02z_PROVISIONAL_20261015.md',
'build_b02z_provisional_archive.py',
'recovery/SOURCE_FIRST_IMAGE_AUDIT_BEFORE_SPAN_COUNT_FIX_20261015.md',
'recovery/EDITORIAL_COUNT_CORRECTION_20261015.json',
'evidence/pdf_1647-410.jpg','evidence/pdf_1647-411.jpg'
]
def sha(data):return hashlib.sha256(data).hexdigest()
payload=[]
for name in memberfiles:
 p=B/name
 assert p.is_file()
 blob=p.read_bytes()
 payload.append({'name':'batches/B02z/'+name,'sha256':sha(blob),'bytes':len(blob)})
assert len(payload)==len(set(p['name'] for p in payload))
summary={'batch':'B02z','archive_status':'UNACCEPTED_SOURCE_FIRST_PREDECESSOR_LIII_PENDING','payloads':payload,'payload_count':len(payload),'original_full_pdf_not_included':True,'accepted_Lilly_before':3071,'new_accepted_units':0,'empirical_results':0}
manifest=json.dumps(summary,ensure_ascii=False,indent=2).encode('utf8')+b'\n'
with zipfile.ZipFile(A,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for name in memberfiles:z.write(B/name,arcname='batches/B02z/'+name)
 z.writestr('SOURCE_FIRST_ARCHIVE_MANIFEST.json',manifest)
with zipfile.ZipFile(A,'r') as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(memberfiles)+1
 assert sha(z.read('SOURCE_FIRST_ARCHIVE_MANIFEST.json'))==sha(manifest)
 for f in payload:
  data=z.read(f['name'])
  assert len(data)==f['bytes'] and sha(data)==f['sha256']
 with tempfile.TemporaryDirectory(prefix='lilly-liv-provisional-') as t:
  z.extractall(t)
  root=Path(t)/'batches/B02z'
  run=subprocess.run(['python3','-m','unittest','-q','test_b02z_source_first.py'],cwd=root,text=True,capture_output=True)
  assert run.returncode==0,(run.stdout,run.stderr)
  assert 'Ran 12 tests' in run.stderr,run.stderr
  for f in payload:
   d=(Path(t)/f['name']).read_bytes()
   assert sha(d)==f['sha256']
source=hashlib.sha256(A.read_bytes()).hexdigest()
receipt={'batch':'B02z','status':'OWNER_LOCAL_PROVISIONAL_PACKET_VERIFIED_NOT_CANONICAL',
'archive_os_designated_downloads':str(A),'archive_sha256':source,
'archive_size_bytes':A.stat().st_size,'zip_crc_pass':True,'all_member_hashes_pass':True,
'actual_extraction_pass':True,'extracted_source_tests_passed':12,
'files_plus_manifest':len(payload)+1,'manifest_sha256':sha(manifest),
'accepted_Lilly_count_unchanged':3071,'new_accepted_documentary_units':0,
'predecessor_chapter_LIII_publication_gate_unresolved':True,
'new_empirical_validations':0,'runtime_promotions':0}
REPORT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
