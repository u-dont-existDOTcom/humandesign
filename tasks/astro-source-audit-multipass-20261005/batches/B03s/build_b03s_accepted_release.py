#!/usr/bin/env python3
"""Original-source historical Chapter LXXIII ZIP, exact extraction and tests replay."""
from pathlib import Path
import json,zipfile,hashlib,subprocess,tempfile
B=Path(__file__).resolve().parent
x=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
DOWNLOAD=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/'Téléchargements'
DOWNLOAD.mkdir(parents=True,exist_ok=True)
OUT=DOWNLOAD/'Astrology-Lilly-Chapter-LXXIII-Promised-Portion-Documentary-20261016.zip'
sha=lambda v:hashlib.sha256(v).hexdigest()
names=[
 'build_b03s_source_first.py','test_b03s_source_first.py',
 'freeze_b03s_documentary_source.py','test_b03s_documentary_admission.py',
 'build_b03s_accepted_release.py',
 'SOURCE_FIRST_CLAUSES_DRAFT.json','ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',
 'SOURCE_ORDER_DRAFT.json','SOURCE_WINDOW_MANIFEST.json',
 'UNRESOLVED_SOURCE_LIMITS.json','CLAIM_LEDGER.json',
 'SOURCE_FIRST_IMAGE_AUDIT_20261016.md',
 'RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
 'ACCEPTANCE.json','ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'evidence/pdf_1647-455.jpg','evidence/pdf_1647-456.jpg'
]
assert all((B/n).is_file() for n in names)
proof={'batch':'B03s','kind':'LILLY_1647_HISTORICAL_DOCUMENTARY_ONLY',
 'original_pdf_pages':[455,456],
 'documentary_source_units':34,'reverse_source_passages':10,
 'unresolved_source_limits':17,
 'author_reported_confirmation':1,'independent_payment_receipts':0,
 'new_empirically_validated_predictions':0,'runtime_promotions':0,
 'remote_publication_pending':True,
 'members':{n:{'sha256':sha((B/n).read_bytes()),'bytes':(B/n).stat().st_size} for n in names}}
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for n in sorted(names):z.write(B/n,arcname='B03s/'+n)
 z.writestr('B03s/RELEASE_SHA256_MANIFEST.json',json.dumps(proof,indent=2)+'\n')
with zipfile.ZipFile(OUT,'r') as z,tempfile.TemporaryDirectory(prefix='lilly-b03s-') as td:
 assert z.testzip() is None
 z.extractall(td)
 E=Path(td)/'B03s'
 assert json.loads((E/'RELEASE_SHA256_MANIFEST.json').read_text())==proof
 for n,record in proof['members'].items():
  data=(E/n).read_bytes()
  assert len(data)==record['bytes'] and sha(data)==record['sha256'],n
 test=subprocess.run(['python3','-m','unittest','-q',
                      'test_b03s_source_first','test_b03s_documentary_admission'],
                      cwd=E,capture_output=True,text=True)
 print(test.stderr[-1000:])
 assert test.returncode==0 and 'Ran 17 tests' in test.stderr
receipt={'batch':'B03s','status':'ARCHIVE_CRC_SHA256_EXTRACTED_17_TEST_REPLAY_VERIFIED',
 'owner_download_path':str(OUT),'archive_sha256':sha(OUT.read_bytes()),
 'archive_bytes':OUT.stat().st_size,'zip_crc_pass':True,
 'every_member_hash_and_size_pass':True,'full_extraction_pass':True,
 'extracted_tests_passed':17,'extracted_exit_code':test.returncode,
 'rules_sha256':proof['members']['RULES.json']['sha256'],
 'new_documentary_records_if_published':34,
 'independently_verified_payment_outcomes':0,
 'new_empirical_predictions':0,'runtime_promotions':0,
 'remotely_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').write_text(
 json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
