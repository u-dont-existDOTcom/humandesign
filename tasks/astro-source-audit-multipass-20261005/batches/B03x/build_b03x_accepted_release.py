#!/usr/bin/env python3
"""Produce original-source LXXVIII case archive; prove zip CRC, hashes and extraction."""
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile
B=Path(__file__).resolve().parent
cmd=subprocess.run(['xdg-user-dir','DOWNLOAD'],capture_output=True,text=True)
DL=Path(cmd.stdout.strip()) if cmd.returncode==0 and cmd.stdout.strip() else Path.home()/'Téléchargements'
DL.mkdir(parents=True,exist_ok=True)
OUT=DL/'Astrology-Lilly-Chapter-LXXVIII-Terrible-Dreams-Documentary-20261016.zip'
H=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
files=['build_b03x_source_first.py','test_b03x_source_first.py',
 'freeze_b03x_documentary_source.py','test_b03x_documentary_admission.py',
 'build_b03x_accepted_release.py','SOURCE_FIRST_CLAUSES_DRAFT.json',
 'ORIGINAL_TO_DRAFT_SOURCE_COVERAGE.json','SOURCE_WINDOW_MANIFEST.json',
 'UNRESOLVED_SOURCE_LIMITS.json','CLAIM_LEDGER.json',
 'SOURCE_FIRST_IMAGE_AUDIT_20261016.md','RULES.json','SOURCE_ORDER.json',
 'UNRESOLVED.json','ACCEPTANCE.json','ORIGINAL_TO_RECORD_SOURCE_FIRST_REVERSE_MAP.json',
 'evidence/pdf_1647-470.jpg','evidence/pdf_1647-471.jpg']
assert all((B/f).is_file() for f in files)
members={f:{'bytes':(B/f).stat().st_size,'sha256':H(B/f)} for f in files}
manifest={'batch':'B03x','kind':'RETROSPECTIVE_ORIGINAL_DREAM_CASE_SOURCE_ONLY',
 'source_passages':6,'historical_documentary_records':24,
 'author_asserted_success_reports':1,'independently_validated_predictions':0,
 'unresolved_source_limitations':14,'members':members}
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in files:z.write(B/f,'B03x/'+f)
 z.writestr('B03x/RELEASE_SHA256_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT) as z,tempfile.TemporaryDirectory(prefix='lilly-b03x-') as tmp:
 assert z.testzip() is None
 z.extractall(tmp)
 p=Path(tmp)/'B03x'
 assert json.loads((p/'RELEASE_SHA256_MANIFEST.json').read_text())==manifest
 for f,v in members.items():
  assert (p/f).stat().st_size==v['bytes'] and H(p/f)==v['sha256'],f
 t=subprocess.run(['python3','-m','unittest','-q',
  'test_b03x_source_first','test_b03x_documentary_admission'],
  cwd=p,capture_output=True,text=True)
 print(t.stderr[-300:])
 assert t.returncode==0 and 'Ran 14 tests' in t.stderr
A=json.loads((B/'ACCEPTANCE.json').read_text())
assert H(B/'RULES.json')==A['rules_sha256']
rec={'batch':'B03x','status':'CRC_SHA256_FULL_EXTRACTION_14_TEST_REPLAY_VERIFIED',
 'owner_download_path':str(OUT),'archive_sha256':H(OUT),'archive_bytes':OUT.stat().st_size,
 'zip_crc_pass':True,'member_hashes_pass':True,'full_extraction_pass':True,
 'extracted_tests_passed':14,'extracted_exit_code':t.returncode,
 'accepted_rules_sha256':A['rules_sha256'],
 'source_annotations_if_published':24,'author_asserted_success_reports':1,
 'independent_dream_outcomes':0,'new_empirical_validations':0,'remote_published':False}
(B/'SOURCE_DOCUMENTARY_RELEASE_RECEIPT_20261016.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
