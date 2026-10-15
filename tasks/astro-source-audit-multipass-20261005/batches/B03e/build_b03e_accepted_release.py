#!/usr/bin/env python3
"""CRC, hash and extracted-test-replayed original-source archive."""
import pathlib,hashlib,json,tempfile,zipfile,subprocess
B=pathlib.Path(__file__).resolve().parent
OUT=pathlib.Path.home()/'Téléchargements'/'Astrology-Lilly-Chapter-LIX-Documentary-20261015.zip'
H=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
items=sorted(p.relative_to(B).as_posix() for p in B.rglob('*')
 if p.is_file() and p.suffix in ('.py','.json','.md','.jpg') and
 not any(k in p.parts for k in ('__pycache__','.git')) and
 p.name!='SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json')
assert all(f'evidence/pdf_1647-{n}.jpg' in items for n in (419,420,421,422,423))
assert 'RULES.json' in items and 'ACCEPTANCE.json' in items
meta={'batch':'B03e','kind':'HISTORICAL_1647_SOURCE_CHART_CASE_ARCHIVE_NOT_BLIND_VALIDATION',
 'source_body_pdf_pages':[419,420,421,422],
 'next_header_pdf_page':423,'historical_source_annotations':58,
 'original_image_passages':25,'independent_case_validation':0,
 'files':{n:{'sha256':H(B/n),'bytes':(B/n).stat().st_size} for n in items}}
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in items:z.write(B/f,arcname='B03e/'+f)
 z.writestr('B03e/RELEASE_FILE_SHA256_MANIFEST.json',
            json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix='lilly-b03e-') as t:
 assert z.testzip() is None
 z.extractall(t)
 ex=pathlib.Path(t)/'B03e'
 assert json.loads((ex/'RELEASE_FILE_SHA256_MANIFEST.json').read_text())==meta
 for f,v in meta['files'].items():
  assert H(ex/f)==v['sha256'] and (ex/f).stat().st_size==v['bytes']
 p=subprocess.run(['python3','-m','unittest','-v','test_b03e_source_first',
    'test_b03e_documentary_admission'],cwd=ex,text=True,capture_output=True)
 print(p.stderr[-1300:])
 assert p.returncode==0 and 'Ran 13 tests' in p.stderr
rec={'batch':'B03e','status':'ORIGINAL_CHART_CASE_ARCHIVE_REPLAY_VERIFIED_NOT_PUBLISHED',
 'archive_on_laptop':str(OUT),'archive_sha256':H(OUT),
 'archive_bytes':OUT.stat().st_size,
 'zip_crc_pass':True,'file_sha256_and_bytes_pass':True,
 'actual_extraction_pass':True,'extracted_source_test_count':13,
 'extracted_source_tests_exit_code':p.returncode,
 'accepted_rules_sha256':meta['files']['RULES.json']['sha256'],
 'new_historical_documentary_records_if_published':58,
 'independently_authenticated_case_outcomes':0,
 'empirically_validated_predictions':0,'runtime_promotions':0,'canonical_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').write_text(
 json.dumps(rec,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(rec,indent=2,ensure_ascii=False))
