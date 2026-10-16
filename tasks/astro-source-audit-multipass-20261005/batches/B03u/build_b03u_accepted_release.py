#!/usr/bin/env python3
"""Lilly LXXV original historical source archive with reproducible source-test replay."""
from pathlib import Path
import json,hashlib,zipfile,tempfile,subprocess
B=Path(__file__).resolve().parent
x=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/'Téléchargements'
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/'Astrology-Lilly-Chapter-LXXV-Original-Folio-Correction-Documentary-20261016.zip'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
FILES=[
 'build_b03u_source_first.py','test_b03u_source_first.py',
 'freeze_b03u_documentary_source.py','test_b03u_documentary_admission.py',
 'build_b03u_accepted_release.py',
 'SOURCE_FIRST_CLAUSES_DRAFT.json','ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',
 'SOURCE_ORDER_DRAFT.json','SOURCE_WINDOW_MANIFEST.json',
 'UNRESOLVED_SOURCE_LIMITS.json','CLAIM_LEDGER.json',
 'SOURCE_FIRST_IMAGE_AUDIT_20261016.md',
 'RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
 'ACCEPTANCE.json','ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
]+[f'evidence/pdf_1647-{p}.jpg' for p in (463,464,465,466)]
assert all((B/n).is_file() for n in FILES)
A=json.loads((B/'ACCEPTANCE.json').read_text())
assert A['new_documentary_records']==61
assert A['original_pdf_text_order']==[463,464,465,466]
assert A['original_imprinted_folio_numbers']==[429,431,430,432]
manifest={'batch':'B03u','kind':'LILLY_1647_PRIMARY_SOURCE_DOCUMENTARY_NOT_EMPIRICAL',
 'original_pdf_scan_order':[463,464,465,466],
 'literal_imprinted_folio_order':[429,431,430,432],
 'transposed_folio_numbering_preserved':True,
 'original_editorial_documentary_units':61,'source_visual_passages':16,
 'retained_source_issues':20,'independent_competency_cases':0,
 'independent_traveler_cases':0,
 'empirically_validated_astrology_predictions':0,
 'remote_publication_pending':True,
 'members':{f:{'sha256':sha((B/f).read_bytes()),'bytes':(B/f).stat().st_size} for f in FILES}}
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in sorted(FILES):z.write(B/f,arcname='B03u/'+f)
 z.writestr('B03u/RELEASE_SHA256_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT,'r') as z,tempfile.TemporaryDirectory(prefix='lilly-b03u-') as td:
 assert z.testzip() is None
 z.extractall(td)
 E=Path(td)/'B03u'
 assert json.loads((E/'RELEASE_SHA256_MANIFEST.json').read_text())==manifest
 for f,v in manifest['members'].items():
  raw=(E/f).read_bytes()
  assert sha(raw)==v['sha256'] and len(raw)==v['bytes'],f
 test=subprocess.run(['python3','-m','unittest','-q',
                      'test_b03u_source_first','test_b03u_documentary_admission'],
                      cwd=E,capture_output=True,text=True)
 print(test.stderr[-1200:])
 assert test.returncode==0 and 'Ran 20 tests' in test.stderr
receipt={'batch':'B03u','status':'ARCHIVE_CRC_SHA256_EXTRACTION_20_TEST_REPLAY_VERIFIED',
 'owner_download_path':str(OUT),'archive_sha256':sha(OUT.read_bytes()),
 'archive_size':OUT.stat().st_size,'zip_crc_pass':True,
 'every_member_sha256_and_size_match':True,'actual_extraction_pass':True,
 'extracted_source_tests_passed':20,'extracted_test_exit_code':test.returncode,
 'accepted_rules_sha256':manifest['members']['RULES.json']['sha256'],
 'new_historical_documentary_records_if_published':61,
 'empirically_validated_predictions':0,'runtime_promotions':0,
 'canonical_remotely_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').write_text(
 json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
