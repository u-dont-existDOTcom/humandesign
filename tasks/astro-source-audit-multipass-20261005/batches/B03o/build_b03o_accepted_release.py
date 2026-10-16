#!/usr/bin/env python3
"""CRC+SHA+real extraction/test replay: historical original Lilly Chapter LXIX."""
from pathlib import Path
import json,zipfile,hashlib,subprocess,tempfile
B=Path(__file__).resolve().parent
res=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
dest=Path(res.stdout.strip()) if res.returncode==0 and res.stdout.strip() else Path.home()/'Téléchargements'
dest.mkdir(parents=True,exist_ok=True)
OUT=dest/'Astrology-Lilly-Chapter-LXIX-Fear-Documentary-20261016.zip'
H=lambda v:hashlib.sha256(v).hexdigest()
files=sorted(p.relative_to(B).as_posix() for p in B.iterdir() if p.is_file() and p.suffix in ('.json','.md','.py') and not p.name.startswith('PUBLICATION_RECEIPT') and not p.name.startswith('SOURCE_DOCUMENTARY_RELEASE_RECEIPT'))
files += [f'evidence/pdf_1647-{n}.jpg' for n in (448,449)]
assert all((B/f).is_file() for f in files)
proof={'batch':'B03o','kind':'ORIGINAL_HISTORICAL_SOURCE_ONLY',
 'original_pdf_pages':[448,449],'accepted_documentary_annotations':31,
 'source_spans':12,'independent_real_danger_cases':0,
 'new_empirical_predictions':0,'new_runtime_rules':0,
 'members':{f:{'sha256':H((B/f).read_bytes()),'bytes':(B/f).stat().st_size} for f in files}}
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,arcname='B03o/'+f)
 z.writestr('B03o/RELEASE_SHA256_MANIFEST.json',json.dumps(proof,indent=2)+'\n')
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix='lilly-b03o-replay-') as td:
 assert z.testzip() is None
 z.extractall(td);E=Path(td)/'B03o'
 assert json.loads((E/'RELEASE_SHA256_MANIFEST.json').read_text())==proof
 for f,v in proof['members'].items():
  raw=(E/f).read_bytes()
  assert H(raw)==v['sha256'] and len(raw)==v['bytes'],f
 proc=subprocess.run(['python3','-m','unittest','-q','test_b03o_source_first',
  'test_b03o_documentary_admission'],cwd=E,capture_output=True,text=True)
 print(proc.stderr[-1000:])
 assert proc.returncode==0 and 'Ran 17 tests' in proc.stderr
receipt={'batch':'B03o','status':'SOURCE_ZIP_CRC_SHA256_EXTRACTED_17_TEST_REPLAY_VERIFIED',
 'owner_local_path':str(OUT),'zip_sha256':H(OUT.read_bytes()),
 'zip_bytes':OUT.stat().st_size,'zip_crc_pass':True,'member_hash_pass':True,
 'full_extraction_pass':True,'replayed_tests_passed':17,'replay_exit_code':proc.returncode,
 'accepted_rules_sha256':proof['members']['RULES.json']['sha256'],
 'new_documentary_units_if_published':31,'new_empirical_validations':0,
 'remote_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
