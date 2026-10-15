#!/usr/bin/env python3
"""Reproducible historical original-text release, with actual extracted test replay."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
download_result=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
DOWNLOAD=Path(download_result.stdout.strip()) if download_result.returncode==0 and download_result.stdout.strip() else Path.home()/'Téléchargements'
DOWNLOAD.mkdir(parents=True,exist_ok=True)
OUT=DOWNLOAD/'Astrology-Lilly-Chapter-LXIV-Fish-Stolen-Documentary-20261015.zip'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
names=[
 'build_b03j_source_first.py','test_b03j_source_first.py',
 'freeze_b03j_documentary_source.py','test_b03j_documentary_admission.py',
 'build_b03j_accepted_release.py',
 'SOURCE_FIRST_CLAUSES_DRAFT.json','ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',
 'SOURCE_ORDER_DRAFT.json','SOURCE_WINDOW_MANIFEST.json',
 'UNRESOLVED_SOURCE_LIMITS.json','CLAIM_LEDGER.json',
 'SOURCE_FIRST_IMAGE_AUDIT_20261015.md',
 'RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'CLAIM_LEDGER_ACCEPTED_LOCAL.json','ACCEPTANCE.json',
 'evidence/pdf_1647-431.jpg','evidence/pdf_1647-432.jpg','evidence/pdf_1647-433.jpg'
]
assert all((B/name).is_file() for name in names)
members={n:{'sha256':sha((B/n).read_bytes()),'bytes':(B/n).stat().st_size} for n in names}
proof={'batch':'B03j','kind':'ORIGINAL_1647_HISTORICAL_SOURCE_ONLY',
 'printed_chapter':'LIV','logical_sequential_chapter':'LXIV',
 'original_pdf_pages':[431,432,433],
 'source_editorial_units':59,'source_reverse_passages':18,
 'author_reported_partial_fish_recovery_cases':1,
 'author_reported_complete_fish_recovery_cases':0,
 'independently_authenticated_recovery_cases':0,
 'empirical_predictions_validated':0,'runtime_promotions':0,
 'global_canonical_publication_pending':True,'members':members}
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for n in sorted(names):
  z.write(B/n,arcname='B03j/'+n)
 z.writestr('B03j/RELEASE_SHA256_MANIFEST.json',
  json.dumps(proof,indent=2,ensure_ascii=False)+'\n')
with zipfile.ZipFile(OUT,'r') as z,tempfile.TemporaryDirectory(prefix='lilly-b03j-release-') as tmp:
 assert z.testzip() is None
 z.extractall(tmp)
 E=Path(tmp)/'B03j'
 assert json.loads((E/'RELEASE_SHA256_MANIFEST.json').read_text())==proof
 for n,info in proof['members'].items():
  raw=(E/n).read_bytes()
  assert len(raw)==info['bytes'] and sha(raw)==info['sha256'],n
 proc=subprocess.run(['python3','-m','unittest','-q',
  'test_b03j_source_first','test_b03j_documentary_admission'],
  cwd=E,capture_output=True,text=True)
 print(proc.stderr[-1500:])
 assert proc.returncode==0 and 'Ran 21 tests' in proc.stderr
receipt={'batch':'B03j',
 'status':'SOURCE_ONLY_RELEASE_ZIP_CRC_SHA256_EXTRACTED_21_TESTS_PASSED',
 'owner_os_download_path':str(OUT),
 'release_zip_sha256':sha(OUT.read_bytes()),
 'release_zip_bytes':OUT.stat().st_size,
 'zip_crc_pass':True,'all_member_hashes_match':True,
 'actual_extraction_pass':True,
 'extracted_focused_tests_passed':21,'extracted_test_exit_code':proc.returncode,
 'accepted_rules_sha256':members['RULES.json']['sha256'],
 'original_printed_heading':'LIV',
 'logical_sequential_chapter':'LXIV',
 'new_historical_documentary_units_if_published':59,
 'case_partial_recovery_independently_authenticated':False,
 'new_empirical_predictions_validated':0,'runtime_promotions':0,
 'canonical_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').write_text(
 json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
