#!/usr/bin/env python3
"""B03r historical source archive with actual extracted test replay."""
from pathlib import Path
import json,zipfile,hashlib,subprocess,tempfile
B=Path(__file__).resolve().parent
q=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
DOWNLOAD=Path(q.stdout.strip()) if q.returncode==0 and q.stdout.strip() else Path.home()/'Téléchargements'
DOWNLOAD.mkdir(parents=True,exist_ok=True)
OUT=DOWNLOAD/'Astrology-Lilly-Chapter-LXXII-Canterbury-Documentary-20261016.zip'
H=lambda v:hashlib.sha256(v).hexdigest()
names=sorted(p.name for p in B.iterdir() if p.is_file() and p.suffix in ('.json','.md','.py')
   and not p.name.startswith('SOURCE_DOCUMENTARY_RELEASE_RECEIPT_')
   and not p.name.startswith('PUBLICATION_RECEIPT_'))
names += [f'evidence/pdf_1647-{n}.jpg' for n in (453,454,455)]
assert all((B/name).is_file() for name in names)
required={'RULES.json','ACCEPTANCE.json','SOURCE_FIRST_IMAGE_AUDIT_20261016.md',
 'test_b03r_source_first.py','test_b03r_documentary_admission.py'}
assert required.issubset(set(names))
manifest={'batch':'B03r','kind':'HISTORICAL_DOCUMENTARY_SOURCE_NOT_PROSPECTIVE_ASTROLOGY',
 'original_pdf_pages':[453,454,455],'locally_accepted_records':43,
 'source_passages':11,'retained_limitations':18,
 'independently_confirmed_historical_execution':1,
 'independently_confirmed_prospective_horary_forecasts':0,
 'new_empirically_validated_astro_outcomes':0,
 'members':{n:{'bytes':(B/n).stat().st_size,'sha256':H((B/n).read_bytes())} for n in names}}
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as zip:
 for name in names:zip.write(B/name,'B03r/'+name)
 zip.writestr('B03r/RELEASE_SHA256_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT) as zip,tempfile.TemporaryDirectory(prefix='lilly-b03r-') as temp:
 assert zip.testzip() is None
 zip.extractall(temp); E=Path(temp)/'B03r'
 assert json.loads((E/'RELEASE_SHA256_MANIFEST.json').read_text())==manifest
 for n,item in manifest['members'].items():
  raw=(E/n).read_bytes()
  assert len(raw)==item['bytes'] and H(raw)==item['sha256'],n
 proc=subprocess.run(['python3','-m','unittest','-q',
  'test_b03r_source_first','test_b03r_documentary_admission'],
  cwd=E,capture_output=True,text=True)
 print(proc.stderr[-1000:])
 assert proc.returncode==0 and 'Ran 12 tests' in proc.stderr
receipt={'batch':'B03r','status':'CRC_SHA256_FULL_EXTRACTION_12_TESTS_REPLAY_VERIFIED',
 'owner_download_path':str(OUT),'archive_sha256':H(OUT.read_bytes()),
 'archive_size':OUT.stat().st_size,'zip_crc_pass':True,
 'member_hashes_pass':True,'actual_extraction_pass':True,
 'extracted_replay_tests_passed':12,'replay_exit_code':proc.returncode,
 'rules_sha256':manifest['members']['RULES.json']['sha256'],
 'historical_execution_confirmed':True,
 'prospective_forecast_independently_verified':False,
 'new_empirically_validated_predictions':0,'remote_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
