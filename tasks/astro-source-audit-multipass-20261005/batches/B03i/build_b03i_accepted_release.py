#!/usr/bin/env python3
"""Accepted historical-documentary chapter source ZIP, actual replay tested."""
from pathlib import Path
import hashlib,json,zipfile,tempfile,subprocess
B=Path(__file__).resolve().parent
proc=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
dl=Path(proc.stdout.strip()) if proc.returncode==0 and proc.stdout.strip() else Path.home()/'Téléchargements'
out=dl/'Astrology-Lilly-Chapter-LXIII-Documentary-20261015.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
files=sorted([p for p in B.iterdir() if p.is_file() and p.suffix in ('.json','.md','.py')
  and p.name!='SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json']
  +[B/'evidence'/f'pdf_1647-{n}.jpg' for n in range(428,432)])
required=['RULES.json','ACCEPTANCE.json','test_b03i_source_first.py',
 'test_b03i_documentary_admission.py','SOURCE_FIRST_CLAUSES_DRAFT.json']
assert all((B/n).is_file() for n in required)
meta={'batch':'B03i','status':'SOURCE_HISTORIC_ONLY_NO_INDEPENDENT_CASE_VALIDATION',
 'source_units':44,'reverse_source_spans':15,'original_body_pdf_pages':[428,429,430],
 'printed_next_chapter_label':'LIV','logical_next_chapter':'LXIV',
 'independently_authenticated_money_recovery_cases':0,'new_empirical_predictions':0,
 'files':{str(p.relative_to(B)):{'size':p.stat().st_size,'sha256':sha(p.read_bytes())}
  for p in files}}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(f,'B03i/'+str(f.relative_to(B)))
 z.writestr('B03i/RELEASE_SHA256_MANIFEST.json',json.dumps(meta,indent=2)+'\n')
with zipfile.ZipFile(out) as z,tempfile.TemporaryDirectory(prefix='lilly-b03i-test-') as temp:
 assert z.testzip() is None
 z.extractall(temp)
 E=Path(temp)/'B03i'
 for k,item in meta['files'].items():
  b=(E/k).read_bytes()
  assert len(b)==item['size'] and sha(b)==item['sha256'],k
 result=subprocess.run(['python3','-m','unittest','-q',
  'test_b03i_source_first','test_b03i_documentary_admission'],
  cwd=E,capture_output=True,text=True)
 print(result.stderr[-1300:])
 assert result.returncode==0 and 'Ran 19 tests' in result.stderr
receipt={'batch':'B03i','status':'ACCEPTED_SOURCE_ZIP_CRC_MEMBER_SHA256_EXTRACTED_19_TESTS_PASS',
 'download_path':str(out),'zip_sha256':sha(out.read_bytes()),
 'zip_bytes':out.stat().st_size,'crc_pass':True,'member_sha256_pass':True,
 'extracted_focused_tests_passed':19,'extracted_test_exit_code':result.returncode,
 'accepted_rules_sha256':meta['files']['RULES.json']['sha256'],
 'original_printed_next_heading':'LIV','canonical_published':False,
 'new_empirical_validations':0}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261015.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
