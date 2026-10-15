#!/usr/bin/env python3
"""Reproducible source-only accepted documentary release, no empirical claims."""
from pathlib import Path
import zipfile,tempfile,subprocess,hashlib,json
B=Path(__file__).resolve().parent
look=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
dl=Path(look.stdout.strip()) if look.returncode==0 and look.stdout.strip() else Path.home()/'Téléchargements'
out=dl/'Astrology-Lilly-Chapter-LXII-Documentary-20261015.zip'
sha=lambda s:hashlib.sha256(s).hexdigest()
files=sorted(p for p in B.rglob('*') if p.is_file()
 and p.suffix in ('.py','.json','.md','.jpg')
 and '__pycache__' not in p.parts
 and not p.name.startswith('SOURCE_DOCUMENTARY_RELEASE_RECEIPT')
 and not p.name.startswith('PUBLICATION_RECEIPT'))
need=['RULES.json','ACCEPTANCE.json','evidence/pdf_1647-426.jpg',
 'evidence/pdf_1647-427.jpg','evidence/pdf_1647-428.jpg']
assert all((B/n).is_file() for n in need)
manifest={'batch':'B03h','status':'SOURCE_DOCUMENTARY_ACCEPTED_LOCALLY_NOT_YET_PUBLISHED',
 'source_editorial_units':43,'source_spans':14,'independent_outcomes':0,
 'empirical_predictions_validated':0,'runtime_promotions':0,
 'files':{str(p.relative_to(B)):{'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in files}}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(f,'B03h/'+str(f.relative_to(B)))
 z.writestr('B03h/RELEASE_SHA256_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(out,'r') as z,tempfile.TemporaryDirectory() as td:
 assert z.testzip() is None
 z.extractall(td)
 base=Path(td)/'B03h'
 for name,info in manifest['files'].items():
  raw=(base/name).read_bytes()
  assert len(raw)==info['bytes'] and sha(raw)==info['sha256'],name
 result=subprocess.run(['python3','-m','unittest','-q',
  'test_b03h_source_first','test_b03h_documentary_admission'],
  cwd=base,text=True,capture_output=True)
 print(result.stderr[-1400:])
 assert result.returncode==0 and 'Ran 17 tests' in result.stderr
receipt={'batch':'B03h','status':'ZIP_CRC_SHA256_EXTRACTION_AND_17_SOURCE_TESTS_VERIFIED',
 'download_path':str(out),'zip_sha256':sha(out.read_bytes()),'zip_bytes':out.stat().st_size,
 'zip_crc_pass':True,'members_sha256_pass':True,'extracted_test_count':17,
 'extracted_test_exit_code':result.returncode,'rules_sha256':manifest['files']['RULES.json']['sha256'],
 'empirical_predictions_validated':0,'canonical_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
