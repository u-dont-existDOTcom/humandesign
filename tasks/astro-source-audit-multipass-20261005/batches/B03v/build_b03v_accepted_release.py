#!/usr/bin/env python3
"""Source-only LXXVI ZIP with full hash/extract/acceptance replay."""
from pathlib import Path
import json,hashlib,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
q=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
DL=Path(q.stdout.strip()) if q.returncode==0 and q.stdout.strip() else Path.home()/'Téléchargements'
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/'Astrology-Lilly-Chapter-LXXVI-Parsonage-Documentary-20261016.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
names=['build_b03v_source_first.py','test_b03v_source_first.py',
 'freeze_b03v_documentary_source.py','test_b03v_documentary_admission.py',
 'build_b03v_accepted_release.py',
 'SOURCE_FIRST_CLAUSES_DRAFT.json','ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',
 'SOURCE_ORDER_DRAFT.json','SOURCE_WINDOW_MANIFEST.json',
 'UNRESOLVED_SOURCE_LIMITS.json','CLAIM_LEDGER.json',
 'SOURCE_FIRST_IMAGE_AUDIT_20261016.md',
 'RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
names += [f'evidence/pdf_1647-{n}.jpg' for n in (466,467,468)]
assert all((B/n).is_file() for n in names)
manifest={'batch':'B03v','kind':'HISTORICAL_SOURCE_ONLY',
 'original_pdf_pages':[466,467,468],
 'source_units':62,'source_spans':16,'source_limitations':20,
 'independent_clergy_appointment_cases':0,'empirical_validations':0,
 'members':{n:{'bytes':(B/n).stat().st_size,'sha256':sha((B/n).read_bytes())} for n in names}}
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for n in sorted(names):z.write(B/n,'B03v/'+n)
 z.writestr('B03v/RELEASE_SHA256_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT,'r') as z,tempfile.TemporaryDirectory(prefix='lilly-b03v-') as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/'B03v'
 assert json.loads((E/'RELEASE_SHA256_MANIFEST.json').read_text())==manifest
 for n,x in manifest['members'].items():
  data=(E/n).read_bytes()
  assert len(data)==x['bytes'] and sha(data)==x['sha256'],n
 test=subprocess.run(['python3','-m','unittest','-q','test_b03v_source_first',
  'test_b03v_documentary_admission'],cwd=E,capture_output=True,text=True)
 print(test.stderr[-850:])
 assert test.returncode==0 and 'Ran 18 tests' in test.stderr
receipt={'batch':'B03v','status':'ZIP_CRC_SHA256_EXTRACTED_18_TEST_REPLAY_VERIFIED',
 'owner_download_path':str(OUT),'archive_sha256':sha(OUT.read_bytes()),
 'archive_bytes':OUT.stat().st_size,'zip_crc_pass':True,'member_sha256_pass':True,
 'actual_extraction_pass':True,'replayed_tests_passed':18,
 'test_exit_code':test.returncode,'rules_sha256':manifest['members']['RULES.json']['sha256'],
 'new_documentary_records_if_published':62,'independent_appointment_cases':0,
 'new_empirical_validations':0,'runtime_promotions':0,'remote_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').write_text(
 json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
