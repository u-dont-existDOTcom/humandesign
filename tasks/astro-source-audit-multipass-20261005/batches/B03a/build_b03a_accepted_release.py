#!/usr/bin/env python3
"""Accepted documentary packet (distinct from frozen earlier provisional packet)."""
import hashlib,json,pathlib,subprocess,tempfile,zipfile
B=pathlib.Path(__file__).resolve().parent
OUT=pathlib.Path.home()/'Téléchargements'/'Astrology-Lilly-Chapter-LV-Documentary-20261015.zip'
H=lambda b:hashlib.sha256(b).hexdigest()
allowed={'.py','.json','.md','.jpg','.png'}
files=sorted(p.relative_to(B).as_posix() for p in B.rglob('*')
 if p.is_file() and p.suffix in allowed and
 not any(x in p.parts for x in ('__pycache__','.git')) and
 p.name not in ('SOURCE_DOCUMENTARY_ACCEPTED_RELEASE_RECEIPT_20261015.json',))
assert 'RULES.json' in files and 'SOURCE_FIRST_CLAUSES_DRAFT.json' in files
assert all(f'evidence/pdf_1647-{n}.jpg' in files for n in [411,412,413])
assert len(files)>=20
meta={'kind':'CHAPTER_LIV_SOURCE_DOCUMENTARY_ACCEPTED_LOCAL_NO_EMPIRICAL_TEST',
      'prior_provisional_snapshot_unmodified':True,
      'source_body_pdf_pages':[411,412,413],
      'locally_admitted_units':32,'source_spans':17,
      'globally_published':False,'new_empirical_predictions':0,'runtime_promotions':0,
      'files':{name:{'sha256':H((B/name).read_bytes()),
                     'bytes':(B/name).stat().st_size} for name in files}}
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for name in files:z.write(B/name,'B03a/'+name)
 z.writestr('B03a/ACCEPTED_RELEASE_SHA256_MANIFEST.json',
            json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix='lilly-b03a-accepted-') as temp:
 assert z.testzip() is None
 z.extractall(temp)
 E=pathlib.Path(temp)/'B03a'
 assert json.loads((E/'ACCEPTED_RELEASE_SHA256_MANIFEST.json').read_text())==meta
 for name,fields in meta['files'].items():
  b=(E/name).read_bytes()
  assert H(b)==fields['sha256'] and len(b)==fields['bytes'],name
 p=subprocess.run(['python3','-m','unittest','-v',
    'test_b03a_source_first','test_b03a_documentary_admission'],
    cwd=E,capture_output=True,text=True)
 print(p.stderr[-1200:])
 assert p.returncode==0 and 'Ran 18 tests' in p.stderr
rec={'batch':'B03a','status':'ACCEPTED_SOURCE_DOCUMENTARY_RELEASE_ARCHIVED_EXTRACTED_REPLAY_VERIFIED',
'archive_os_downloads':str(OUT),'archive_sha256':H(OUT.read_bytes()),
'archive_bytes':OUT.stat().st_size,'zip_crc_pass':True,
'file_sha256_and_bytes_pass':True,'extracted_focused_test_count':18,
'extracted_focused_test_exit_code':p.returncode,'rules_sha256':meta['files']['RULES.json']['sha256'],
'prior_provisional_snapshot_unmodified':True,
'local_documentary_source_units':32,'new_empirical_validations':0,
'canonical_published':False}
(B/'SOURCE_DOCUMENTARY_ACCEPTED_RELEASE_RECEIPT_20261015.json').write_text(
 json.dumps(rec,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(rec,indent=2))
