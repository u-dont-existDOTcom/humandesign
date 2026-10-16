#!/usr/bin/env python3
"""Lilly source-only LXXIV release: CRC + SHA256 + extracted test replay."""
from pathlib import Path
import json,hashlib,zipfile,subprocess,tempfile
B=Path(__file__).resolve().parent
x=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
DOWNLOAD=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/'Téléchargements'
DOWNLOAD.mkdir(parents=True,exist_ok=True)
OUT=DOWNLOAD/'Astrology-Lilly-Chapter-LXXIV-Ninth-House-Documentary-20261016.zip'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
names=[
 'build_b03t_source_first.py','test_b03t_source_first.py',
 'freeze_b03t_documentary_source.py','test_b03t_documentary_admission.py',
 'build_b03t_accepted_release.py',
 'SOURCE_FIRST_CLAUSES_DRAFT.json','ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',
 'SOURCE_ORDER_DRAFT.json','SOURCE_WINDOW_MANIFEST.json',
 'UNRESOLVED_SOURCE_LIMITS.json','CLAIM_LEDGER.json',
 'SOURCE_FIRST_IMAGE_AUDIT_20261016.md',
 'RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
 'ACCEPTANCE.json','ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json'
]+[f'evidence/pdf_1647-{n}.jpg' for n in range(456,464)]
assert len(names)==25 and all((B/n).is_file() for n in names)
manifest={'batch':'B03t','kind':'ORIGINAL_1647_HISTORICAL_DOCUMENTARY_SOURCE_ONLY',
 'original_pdf_pages':list(range(456,464)),
 'locally_accepted_documentary_units':153,
 'source_visual_passages':28,'retained_original_source_limits':32,
 'independently_verified_journey_cases':0,
 'independently_verified_weather_cases':0,
 'new_empirically_validated_predictions':0,'runtime_promotions':0,
 'remote_publication_pending':True,
 'members':{n:{'bytes':(B/n).stat().st_size,
               'sha256':sha((B/n).read_bytes())} for n in names}}
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for n in sorted(names):z.write(B/n,arcname='B03t/'+n)
 z.writestr('B03t/RELEASE_SHA256_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT,'r') as z,tempfile.TemporaryDirectory(prefix='lilly-b03t-') as td:
 assert z.testzip() is None
 z.extractall(td);E=Path(td)/'B03t'
 assert json.loads((E/'RELEASE_SHA256_MANIFEST.json').read_text())==manifest
 for n,info in manifest['members'].items():
  raw=(E/n).read_bytes()
  assert len(raw)==info['bytes'] and sha(raw)==info['sha256'],n
 test=subprocess.run(['python3','-m','unittest','-q',
  'test_b03t_source_first','test_b03t_documentary_admission'],
  cwd=E,capture_output=True,text=True)
 print(test.stderr[-800:])
 assert test.returncode==0 and 'Ran 19 tests' in test.stderr
receipt={'batch':'B03t',
 'status':'CRC_SHA256_FULL_EXTRACTION_19_TEST_REPLAY_VERIFIED',
 'owner_download_path':str(OUT),'archive_sha256':sha(OUT.read_bytes()),
 'archive_size':OUT.stat().st_size,'crc_pass':True,
 'every_member_hash_pass':True,'actual_extraction_pass':True,
 'extracted_tests_passed':19,'extracted_test_exit_code':test.returncode,
 'accepted_rules_sha256':manifest['members']['RULES.json']['sha256'],
 'new_historical_documentary_units':153,
 'independent_cases_validated':0,'new_runtime_rules':0,
 'remote_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').write_text(
 json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
