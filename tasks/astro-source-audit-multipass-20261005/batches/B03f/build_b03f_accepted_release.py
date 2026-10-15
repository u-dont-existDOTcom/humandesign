#!/usr/bin/env python3
"""Build and extract-test the original-source-only Chapter LX documentary release."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
folder=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
download=Path(folder.stdout.strip()) if folder.returncode==0 and folder.stdout.strip() else Path.home()/'Téléchargements'
download.mkdir(parents=True,exist_ok=True)
OUT=download/'Astrology-Lilly-Chapter-LX-Documentary-20261015.zip'
SHA=lambda b:hashlib.sha256(b).hexdigest()
names=sorted(p.relative_to(B).as_posix() for p in B.rglob('*')
 if p.is_file() and p.suffix in ('.py','.json','.md','.jpg')
 and not any(x in p.parts for x in ('__pycache__','.git','tmp'))
 and p.name not in ('SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json','PUBLICATION_RECEIPT_20261015.json'))
for important in ('RULES.json','ACCEPTANCE.json',
                  'test_b03f_source_first.py','test_b03f_documentary_admission.py',
                  'evidence/pdf_1647-423.jpg','evidence/pdf_1647-424.jpg'):
 assert important in names,important
meta={'kind':'LILLY1647_CHAPTER_LX_ORIGINAL_DOCUMENTARY_ONLY',
 'original_pdf_pages':[423,424],'locally_documentary_accepted_records':31,
 'source_passages':13,'author_narrated_marriage_cases':1,
 'independently_authenticated_outcomes':0,
 'empirically_validated_predictions':0,'model_runtime_promotions':0,
 'archived_before_canonical_publication':True,
 'files':{n:{'sha256':SHA((B/n).read_bytes()),'bytes':(B/n).stat().st_size}
          for n in names}}
manifest=(json.dumps(meta,indent=2,ensure_ascii=False)+'\n').encode('utf-8')
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for n in names:z.write(B/n,arcname='B03f/'+n)
 z.writestr('B03f/RELEASE_SHA256_MANIFEST.json',manifest)
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix='lilly-b03f-test-') as td:
 assert z.testzip() is None
 z.extractall(td)
 E=Path(td)/'B03f'
 assert json.loads((E/'RELEASE_SHA256_MANIFEST.json').read_text())==meta
 for n,info in meta['files'].items():
  raw=(E/n).read_bytes()
  assert SHA(raw)==info['sha256'] and len(raw)==info['bytes'],n
 p=subprocess.run(['python3','-m','unittest','-q',
   'test_b03f_source_first','test_b03f_documentary_admission'],
   cwd=E,text=True,capture_output=True)
 print(p.stderr[-1800:])
 assert p.returncode==0 and 'Ran 18 tests' in p.stderr
receipt={'batch':'B03f',
 'status':'DOCUMENTARY_RELEASE_ZIP_INTEGRITY_EXTRACTION_SHA256_AND_REPLAY_VERIFIED',
 'owner_os_download_path':str(OUT),'archive_sha256':SHA(OUT.read_bytes()),
 'archive_bytes':OUT.stat().st_size,'zip_crc_pass':True,
 'all_member_hashes_pass':True,'actual_extraction_pass':True,
 'extracted_source_tests_passed':18,'extracted_test_exit_code':p.returncode,
 'source_rules_sha256':meta['files']['RULES.json']['sha256'],
 'provisional_source_original_preserved':True,
 'new_empirical_predictions_validated':0,'new_runtime_rules':0,
 'canonical_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').write_text(
 json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
