#!/usr/bin/env python3
"""Owner delivery: original source image packet, deterministic SHA256 manifest, tests."""
import hashlib,json,pathlib,subprocess,tempfile,zipfile
B=pathlib.Path(__file__).resolve().parent
OUT=pathlib.Path.home()/'Téléchargements'/'Astrology-Lilly-Chapter-LVII-Documentary-20261015.zip'
H=lambda b:hashlib.sha256(b).hexdigest()
allowed=['build_b03c_source_first.py','test_b03c_source_first.py',
  'freeze_b03c_documentary_source.py','test_b03c_documentary_admission.py',
  'build_b03c_accepted_release.py',
  'SOURCE_FIRST_CLAUSES_DRAFT.json','ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',
  'SOURCE_ORDER_DRAFT.json','SOURCE_WINDOW_MANIFEST.json',
  'CLAIM_LEDGER.json','UNRESOLVED_SOURCE_LIMITS.json',
  'SOURCE_FIRST_IMAGE_AUDIT_20261015.md',
  'RULES.json','SOURCE_ORDER.json','UNRESOLVED.json',
  'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
  'ACCEPTANCE.json','evidence/pdf_1647-414.jpg','evidence/pdf_1647-415.jpg','evidence/pdf_1647-416.jpg','evidence/pdf_1647-417.jpg']
assert all((B/f).exists() for f in allowed)
meta={
 'kind':'B03c_WILLIAM_LILLY_1647_DOCUMENTARY_SOURCE_REPLAY_NOT_PREDICTIVE_VALIDATION',
 'book':'II','chapter':'LVI','source_pdf_pages':[414,415,416,417],
 'first_numbered_source_record':3249,'last_numbered_source_record':3322,
 'new_locally_admitted_documentary_records':74,
 'original_source_reverse_passages':26,
 'blind_independent_complete_diplomatic_reading':False,
 'accepted_source_not_evidence_of_predicted_outcomes':True,
 'new_model_runtime_promotions':0,
 'files':{f:{'sha256':H((B/f).read_bytes()),'bytes':(B/f).stat().st_size}
          for f in sorted(allowed)}
}
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for file in sorted(allowed):z.write(B/file,arcname='B03c/'+file)
 z.writestr('B03c/ACCEPTED_RELEASE_SHA256_MANIFEST.json',
  json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix='b03c-replay-') as temp:
 assert z.testzip() is None
 z.extractall(temp)
 d=pathlib.Path(temp)/'B03c'
 m=json.loads((d/'ACCEPTED_RELEASE_SHA256_MANIFEST.json').read_text())
 assert meta==m
 for f,v in m['files'].items():
  b=(d/f).read_bytes()
  assert H(b)==v['sha256'] and len(b)==v['bytes'],f
 cmd=['python3','-m','unittest','-v',
  'test_b03c_source_first','test_b03c_documentary_admission']
 p=subprocess.run(cmd,cwd=d,capture_output=True,text=True)
 print(p.stderr[-1250:])
 assert p.returncode==0 and 'Ran 17 tests' in p.stderr
receipt={
 'batch':'B03c',
 'status':'ORIGINAL_IMAGE_DOCUMENTARY_RELEASE_ZIP_AND_ACTUAL_EXTRACTED_REPLAY_VERIFIED',
 'archive_on_laptop':str(OUT),
 'archive_sha256':H(OUT.read_bytes()),
 'archive_bytes':OUT.stat().st_size,
 'zip_crc_pass':True,'member_sha256_pass':True,
 'actual_extraction_pass':True,'extracted_17_tests_exit_code':p.returncode,
 'extracted_test_count':17,'accepted_rules_sha256':meta['files']['RULES.json']['sha256'],
 'local_historical_source_units':74,
 'new_empirical_predictions_validated':0,
 'runtime_promotions':0,'published_to_canonical_research_branch':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').write_text(
 json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
