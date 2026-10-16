#!/usr/bin/env python3
"""Original 1647 historical dreams source ZIP with CRC/sha256/extracted source test replay."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
x=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
DL=Path(x.stdout.strip()) if x.returncode==0 and x.stdout.strip() else Path.home()/'Téléchargements'
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/'Astrology-Lilly-Chapter-LXXVII-Dreams-Documentary-20261016.zip'
H=lambda b:hashlib.sha256(b).hexdigest()
files=['build_b03w_source_first.py','test_b03w_source_first.py',
 'freeze_b03w_documentary_source.py','test_b03w_documentary_admission.py',
 'build_b03w_accepted_release.py','fetch_original_scans.py',
 'SOURCE_FIRST_CLAUSES_DRAFT.json','ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json',
 'SOURCE_ORDER_DRAFT.json','SOURCE_WINDOW_MANIFEST.json',
 'UNRESOLVED_SOURCE_LIMITS.json','CLAIM_LEDGER.json',
 'SOURCE_FIRST_IMAGE_AUDIT_20261016.md',
 'RULES.json','SOURCE_ORDER.json','UNRESOLVED.json','ACCEPTANCE.json',
 'ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json']
files += [f'evidence/pdf_1647-{n}.jpg' for n in (468,469,470)]
assert all((B/f).is_file() for f in files)
manifest={'batch':'B03w','kind':'ORIGINAL_HISTORICAL_DREAMS_SOURCE_ONLY',
 'original_pdf_pages':[468,469,470],'locally_admitted_records':38,
 'source_visual_passages':8,'retained_uncertainties':15,
 'independent_real_dream_cases':0,'new_empirical_validations':0,
 'members':{f:{'size':(B/f).stat().st_size,'sha256':H((B/f).read_bytes())} for f in files}}
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,'B03w/'+f)
 z.writestr('B03w/RELEASE_SHA256_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT,'r') as z,tempfile.TemporaryDirectory(prefix='lilly-b03w-') as tmp:
 assert z.testzip() is None
 z.extractall(tmp);E=Path(tmp)/'B03w'
 assert json.loads((E/'RELEASE_SHA256_MANIFEST.json').read_text())==manifest
 for f,item in manifest['members'].items():
  raw=(E/f).read_bytes()
  assert len(raw)==item['size'] and H(raw)==item['sha256'],f
 t=subprocess.run(['python3','-m','unittest','-q',
  'test_b03w_source_first','test_b03w_documentary_admission'],
  cwd=E,capture_output=True,text=True)
 print(t.stderr[-850:])
 assert t.returncode==0 and 'Ran 15 tests' in t.stderr
receipt={'batch':'B03w','status':'CRC_SHA256_FULL_EXTRACTION_15_TEST_REPLAY_VERIFIED',
 'owner_download_path':str(OUT),'archive_sha256':H(OUT.read_bytes()),
 'archive_bytes':OUT.stat().st_size,'zip_crc_pass':True,
 'member_hashes_pass':True,'full_extraction_pass':True,
 'extracted_tests_passed':15,'extracted_exit_code':t.returncode,
 'accepted_rules_sha256':manifest['members']['RULES.json']['sha256'],
 'historical_documentary_records_if_published':38,
 'independent_verified_dream_cases':0,'empirical_predictions_validated':0,
 'remote_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').write_text(
 json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2))
