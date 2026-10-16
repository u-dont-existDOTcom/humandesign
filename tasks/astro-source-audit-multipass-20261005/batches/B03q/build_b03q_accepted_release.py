#!/usr/bin/env python3
"""Reproducible original-source archive and extracted-source test replay."""
from pathlib import Path
import json,zipfile,hashlib,subprocess,tempfile
B=Path(__file__).resolve().parent
q=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
DL=Path(q.stdout.strip()) if q.returncode==0 and q.stdout.strip() else Path.home()/'Téléchargements'
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/'Astrology-Lilly-Chapter-LXXI-Husband-at-Sea-Documentary-20261016.zip'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
files=sorted(p.relative_to(B).as_posix() for p in B.iterdir() if p.is_file() and p.suffix in ('.py','.json','.md') and not p.name.startswith('PUBLICATION_RECEIPT') and not p.name.startswith('SOURCE_DOCUMENTARY_RELEASE_RECEIPT'))
files += [f'evidence/pdf_1647-{n}.jpg' for n in (451,452,453)]
assert all((B/n).is_file() for n in files)
manifest={'batch':'B03q','kind':'LILLY_1647_ORIGINAL_DOCUMENTARY_ONLY',
 'source_editorial_annotations':41,'source_passages':10,'original_pdf_pages':[451,452,453],
 'reported_false_early_rumor':1,'reported_may_news':1,'reported_july_return':1,
 'independently_authenticated_outcomes':0,'validated_astrology_predictions':0,
 'members':{n:{'bytes':(B/n).stat().st_size,'sha256':sha((B/n).read_bytes())} for n in files}}
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for n in files:z.write(B/n,'B03q/'+n)
 z.writestr('B03q/RELEASE_SHA256_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT,'r') as z,tempfile.TemporaryDirectory(prefix='lilly-b03q-') as td:
 assert z.testzip() is None
 z.extractall(td);E=Path(td)/'B03q'
 assert json.loads((E/'RELEASE_SHA256_MANIFEST.json').read_text())==manifest
 for n,x in manifest['members'].items():
  raw=(E/n).read_bytes()
  assert len(raw)==x['bytes'] and sha(raw)==x['sha256'],n
 proc=subprocess.run(['python3','-m','unittest','-q',
  'test_b03q_source_first','test_b03q_documentary_admission'],cwd=E,capture_output=True,text=True)
 print(proc.stderr[-1200:])
 assert proc.returncode==0 and 'Ran 10 tests' in proc.stderr
receipt={'batch':'B03q','status':'ZIP_CRC_SHA256_FULL_EXTRACTION_10_TEST_REPLAY_VERIFIED',
 'local_owner_path':str(OUT),'archive_sha256':sha(OUT.read_bytes()),
 'archive_bytes':OUT.stat().st_size,'zip_crc_pass':True,'member_sha256_pass':True,
 'full_extraction_pass':True,'tests_replayed':10,'test_exit_code':proc.returncode,
 'rules_sha256':manifest['members']['RULES.json']['sha256'],
 'new_documentary_records_if_published':41,'independent_outcomes':0,
 'new_empirical_validations':0,'remote_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
