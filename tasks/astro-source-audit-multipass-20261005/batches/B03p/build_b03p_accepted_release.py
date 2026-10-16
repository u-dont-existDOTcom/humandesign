#!/usr/bin/env python3
"""Historical original Lilly Chapter LXX release, hash/extract/replay verified."""
from pathlib import Path
import zipfile,json,hashlib,subprocess,tempfile
B=Path(__file__).resolve().parent
q=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
dl=Path(q.stdout.strip()) if q.returncode==0 and q.stdout.strip() else Path.home()/'Téléchargements'
dl.mkdir(parents=True,exist_ok=True)
OUT=dl/'Astrology-Lilly-Chapter-LXX-Spouse-Case-Documentary-20261016.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
files=sorted(p.relative_to(B).as_posix() for p in B.iterdir() if p.is_file() and p.suffix in ('.md','.json','.py') and not p.name.startswith('PUBLICATION_') and not p.name.startswith('SOURCE_DOCUMENTARY_RELEASE_'))
files += [f'evidence/pdf_1647-{n}.jpg' for n in (449,450,451)]
assert all((B/f).is_file() for f in files)
manifest={'batch':'B03p','kind':'SOURCE_HISTORICAL_UNVERIFIED_CASE',
 'original_images':[449,450,451],'historical_source_annotations':45,
 'source_passages':14,'author_reported_outcome_cases':1,
 'independent_verified_outcomes':0,'empirically_validated_predictions':0,
 'members':{f:{'bytes':(B/f).stat().st_size,'sha256':sha((B/f).read_bytes())} for f in files}}
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,arcname='B03p/'+f)
 z.writestr('B03p/RELEASE_SHA256_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix='lilly-b03p-') as tmp:
 assert z.testzip() is None
 z.extractall(tmp);e=Path(tmp)/'B03p'
 assert json.loads((e/'RELEASE_SHA256_MANIFEST.json').read_text())==manifest
 for f,m in manifest['members'].items():
  raw=(e/f).read_bytes()
  assert len(raw)==m['bytes'] and sha(raw)==m['sha256']
 out=subprocess.run(['python3','-m','unittest','-q','test_b03p_source_first',
  'test_b03p_documentary_admission'],cwd=e,capture_output=True,text=True)
 print(out.stderr[-1100:])
 assert out.returncode==0 and 'Ran 12 tests' in out.stderr
receipt={'batch':'B03p','status':'SOURCE_ZIP_CRC_SHA256_EXTRACTION_AND_12_REPLAY_TESTS_VERIFIED',
 'local_owner_zip_path':str(OUT),'archive_sha256':sha(OUT.read_bytes()),
 'archive_bytes':OUT.stat().st_size,'crc_pass':True,'member_hash_pass':True,
 'extracted_pass':True,'replayed_tests':12,'test_exit_code':out.returncode,
 'rules_sha256':manifest['members']['RULES.json']['sha256'],
 'author_reported_cases':1,'independently_validated_cases':0,
 'new_empirical_accuracy':0,'canonical_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
