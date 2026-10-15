"""Produce a source-first owner handoff; acceptance and canonical index remain unchanged."""
from pathlib import Path
import json,hashlib,zipfile,tempfile,subprocess
B=Path(__file__).resolve().parent
D=Path(subprocess.check_output(['xdg-user-dir','DOWNLOAD'],text=True).strip())
assert D.is_dir()
A=D/'Astrology-Lilly-Chapter-LV-Source-First-Provisional-20261015.zip'
R=B/'PROVISIONAL_PACKET_RECEIPT_20261015.json'
assert not (A.exists() or R.exists())
names=[
'build_b03a_source_first.py','SOURCE_WINDOW_MANIFEST.json','SOURCE_FIRST_CLAUSES_DRAFT.json',
'SOURCE_ORDER_DRAFT.json','build_b03a_reverse_map.py','ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',
'UNRESOLVED_SOURCE_LIMITS.json','SOURCE_FIRST_IMAGE_AUDIT_20261015.md',
'test_b03a_source_first.py','CLAIM_LEDGER.json','HANDOFF_B03a_PROVISIONAL_20261015.md',
'build_b03a_provisional_archive.py',
'evidence/pdf_1647-411.jpg','evidence/pdf_1647-412.jpg','evidence/pdf_1647-413.jpg',
'evidence/pdf_1647-412-part-fortune-check.png'
]
sha=lambda b:hashlib.sha256(b).hexdigest()
items=[]
for n in names:
 b=(B/n).read_bytes()
 items.append({'path':'batches/B03a/'+n,'bytes':len(b),'sha256':sha(b)})
manifest=json.dumps({'status':'UNACCEPTED_SOURCE_FIRST_PREDECESSORS_PENDING','batch':'B03a',
'canonical_accepted_units_added':0,'new_empirical_cases':0,'files':items,'file_count':len(items),'original_141mb_pdf_not_embedded':True},ensure_ascii=False,indent=2).encode()+b'\n'
with zipfile.ZipFile(A,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n in names:z.write(B/n,'batches/B03a/'+n)
 z.writestr('SOURCE_FIRST_ARCHIVE_MANIFEST.json',manifest)
with zipfile.ZipFile(A) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(items)+1
 for rec in items:
  blob=z.read(rec['path'])
  assert len(blob)==rec['bytes'] and sha(blob)==rec['sha256'],rec['path']
 assert sha(z.read('SOURCE_FIRST_ARCHIVE_MANIFEST.json'))==sha(manifest)
 with tempfile.TemporaryDirectory(prefix='lilly-lv-provisional-') as t:
  z.extractall(t)
  root=Path(t)/'batches/B03a'
  test=subprocess.run(['python3','-m','unittest','-q','test_b03a_source_first.py'],cwd=root,capture_output=True,text=True)
  assert test.returncode==0,(test.stdout,test.stderr)
  assert 'Ran 11 tests' in test.stderr
  for rec in items:
   assert sha((Path(t)/rec['path']).read_bytes())==rec['sha256']
result={'batch':'B03a','status':'PROVISIONAL_NOT_ACCEPTED_OWNER_DELIVERY_VERIFIED',
'owner_downloads_zip':str(A),'zip_sha256':sha(A.read_bytes()),'zip_bytes':A.stat().st_size,
'zip_crc_pass':True,'all_payload_sha256_pass':True,'actual_extracted_test_replay_pass':True,
'extracted_tests':11,'members_including_manifest':len(items)+1,
'manifest_sha256':sha(manifest),'accepted_lilly_records_unchanged':3071,
'new_empirical_cases':0,'runtime_promotions':0,
'predecessors':['LIII','LIV']}
R.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
