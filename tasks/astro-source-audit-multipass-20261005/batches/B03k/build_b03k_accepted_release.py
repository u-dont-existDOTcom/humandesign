#!/usr/bin/env python3
"""Accepted original-documentary Chapter LXV archive with extraction and replay."""
from pathlib import Path
import json,hashlib,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
q=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
dl=Path(q.stdout.strip()) if q.returncode==0 and q.stdout.strip() else Path.home()/'Téléchargements'
dl.mkdir(parents=True,exist_ok=True)
OUT=dl/'Astrology-Lilly-Chapter-LXV-Waller-Hopton-Documentary-20261015.zip'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
names=[
 'build_b03k_source_first.py','test_b03k_source_first.py',
 'freeze_b03k_documentary_source.py','test_b03k_documentary_admission.py',
 'build_b03k_accepted_release.py',
 'SOURCE_FIRST_CLAUSES_DRAFT.json','ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',
 'SOURCE_ORDER_DRAFT.json','SOURCE_WINDOW_MANIFEST.json',
 'UNRESOLVED_SOURCE_LIMITS.json','CLAIM_LEDGER.json',
 'SOURCE_FIRST_IMAGE_AUDIT_20261015.md',
 'RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
 'CLAIM_LEDGER_ACCEPTED_LOCAL.json','ACCEPTANCE.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'evidence/pdf_1647-433.jpg','evidence/pdf_1647-434.jpg','evidence/pdf_1647-435.jpg'
]
assert all((B/n).is_file() for n in names)
members={n:{'sha256':sha((B/n).read_bytes()),'bytes':(B/n).stat().st_size} for n in names}
proof={'batch':'B03k','kind':'ORIGINAL_LILLY1647_SOURCE_ONLY',
 'original_pdf_pages':[433,434,435],'source_units':40,'source_spans':10,
 'chart_date':'29 March 1644','chart_time':'10:12 AM',
 'source_author_reported_favorable_outcome':1,
 'independently_verified_precise_news_timing':0,
 'new_empirical_predictions':0,'new_runtime_rules':0,
 'canonical_publication_pending':True,'members':members}
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for n in sorted(names):z.write(B/n,arcname='B03k/'+n)
 z.writestr('B03k/RELEASE_SHA256_MANIFEST.json',
  json.dumps(proof,indent=2)+'\n')
with zipfile.ZipFile(OUT,'r') as z,tempfile.TemporaryDirectory(prefix='lilly-b03k-replay-') as td:
 assert z.testzip() is None
 z.extractall(td)
 E=Path(td)/'B03k'
 assert json.loads((E/'RELEASE_SHA256_MANIFEST.json').read_text())==proof
 for n,x in members.items():
  data=(E/n).read_bytes()
  assert len(data)==x['bytes'] and sha(data)==x['sha256']
 run=subprocess.run(['python3','-m','unittest','-q',
  'test_b03k_source_first','test_b03k_documentary_admission'],
  cwd=E,capture_output=True,text=True)
 print(run.stderr[-1200:])
 assert run.returncode==0 and 'Ran 19 tests' in run.stderr
receipt={'batch':'B03k','status':'CRC_SHA256_ORIGINAL_EXTRACTED_19_SOURCE_TESTS_VERIFIED',
 'download_path':str(OUT),'zip_sha256':sha(OUT.read_bytes()),
 'archive_bytes':OUT.stat().st_size,
 'zip_crc_pass':True,'member_hashes_match':True,'actual_extraction_pass':True,
 'extracted_test_count':19,'extracted_test_exit_code':run.returncode,
 'original_source_rules_sha256':members['RULES.json']['sha256'],
 'new_historical_units_if_published':40,
 'author_reported_favorable_battle_cases':1,
 'independently_validated_battle_predictions':0,
 'new_runtime_rules':0,'remote_publication_verified':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').write_text(
 json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
