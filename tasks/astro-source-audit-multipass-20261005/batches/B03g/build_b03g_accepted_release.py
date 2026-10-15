#!/usr/bin/env python3
"""Source-only archival release with actual extraction and focused-test replay."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
proc=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
dl=Path(proc.stdout.strip()) if proc.returncode==0 and proc.stdout.strip() else Path.home()/'Téléchargements'
dl.mkdir(parents=True,exist_ok=True)
OUT=dl/'Astrology-Lilly-Chapter-LXI-Documentary-20261015.zip'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
FILES=[
 'build_b03g_source_first.py','test_b03g_source_first.py',
 'freeze_b03g_documentary_source.py','test_b03g_documentary_admission.py',
 'build_b03g_accepted_release.py',
 'SOURCE_SCOPE_NOTE.md','SOURCE_FIRST_IMAGE_AUDIT_20261015.md',
 'SOURCE_FIRST_CLAUSES_DRAFT.json','ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',
 'SOURCE_ORDER_DRAFT.json','SOURCE_WINDOW_MANIFEST.json',
 'UNRESOLVED_SOURCE_LIMITS.json','CLAIM_LEDGER.json',
 'RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
 'CLAIM_LEDGER_ACCEPTED_LOCAL.json','ACCEPTANCE.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'evidence/pdf_1647-424.jpg','evidence/pdf_1647-425.jpg','evidence/pdf_1647-426.jpg'
]
for f in FILES:assert (B/f).is_file(),f
manifest={'batch':'B03g','kind':'ORIGINAL_1647_SOURCE_ONLY_NOT_EMPIRICALLY_VALIDATED',
 'original_pdf_pages':[424,425,426],
 'source_first_annotations':35,'original_visual_passages':15,
 'historical_narrated_servant_return':1,'independent_authenticated_case_outcomes':0,
 'real_predictive_accuracies_established':0,'runtime_promotions':0,
 'canonical_published_at_creation':False,
 'members':{f:{'bytes':(B/f).stat().st_size,
                'sha256':sha((B/f).read_bytes())} for f in sorted(FILES)}}
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in sorted(FILES):
  z.write(B/f,arcname='B03g/'+f)
 z.writestr('B03g/SOURCE_RELEASE_SHA256_MANIFEST.json',
            json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
with zipfile.ZipFile(OUT,'r') as z,tempfile.TemporaryDirectory(prefix='lilly-b03g-replay-') as tmp:
 assert z.testzip() is None
 z.extractall(tmp)
 E=Path(tmp)/'B03g'
 received=json.loads((E/'SOURCE_RELEASE_SHA256_MANIFEST.json').read_text())
 assert received==manifest
 for name,proof in manifest['members'].items():
  raw=(E/name).read_bytes()
  assert sha(raw)==proof['sha256'] and len(raw)==proof['bytes'],name
 run=subprocess.run(['python3','-m','unittest','-q',
                     'test_b03g_source_first','test_b03g_documentary_admission'],
                     cwd=E,capture_output=True,text=True)
 print(run.stderr[-1450:])
 assert run.returncode==0 and 'Ran 21 tests' in run.stderr
receipt={'batch':'B03g',
 'status':'ORIGINAL_SOURCE_ZIP_CRC_MEMBER_SHA256_EXTRACTED_TEST_REPLAY_VERIFIED',
 'owner_designated_download_path':str(OUT),
 'archive_sha256':sha(OUT.read_bytes()),
 'archive_bytes':OUT.stat().st_size,
 'zip_crc_pass':True,'member_sha256_pass':True,
 'actual_extraction_pass':True,
 'extracted_source_tests_passed':21,
 'extracted_test_exit_code':run.returncode,
 'source_rules_sha256':manifest['members']['RULES.json']['sha256'],
 'local_documentary_units':35,'remote_canonical_published':False,
 'new_empirically_verified_predictions':0,'new_runtime_rules':0}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').write_text(
 json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
